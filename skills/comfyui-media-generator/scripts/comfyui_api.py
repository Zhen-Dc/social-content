#!/usr/bin/env python3
"""Submit ComfyUI API workflows and copy generated media into project assets."""

from __future__ import annotations

import argparse
import json
import shutil
import socket
import time
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_PORTS = tuple(range(8190, 8200))
STATE_FILE = Path(r"C:\Social Content\.tmp\comfyui_server.json")


def post_json(url: str, data: dict) -> dict:
    body = json.dumps(data).encode("utf-8")
    request = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def get_json(url: str, timeout: int = 30) -> dict:
    with urllib.request.urlopen(url, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def server_is_ready(server: str) -> bool:
    try:
        get_json(f"{server.rstrip('/')}/system_stats", timeout=5)
        return True
    except (ConnectionResetError, TimeoutError, socket.timeout, urllib.error.URLError, OSError):
        return False


def resolve_server(server: str) -> str:
    if server != "auto":
        return server.rstrip("/")

    if STATE_FILE.exists():
        try:
            saved = json.loads(STATE_FILE.read_text(encoding="utf-8-sig"))
            saved_server = str(saved.get("server", "")).rstrip("/")
            if saved_server and server_is_ready(saved_server):
                return saved_server
        except (OSError, json.JSONDecodeError):
            pass

    for port in DEFAULT_PORTS:
        candidate = f"http://127.0.0.1:{port}"
        if server_is_ready(candidate):
            return candidate

    raise RuntimeError(
        "No ComfyUI API server found on ports 8190-8199. "
        r"Start it with C:\Social Content\skills\comfyui-media-generator\scripts\start_comfyui_portable.cmd."
    )


def queue_prompt(server: str, workflow: dict) -> str:
    result = post_json(f"{server}/prompt", {"prompt": workflow})
    return result["prompt_id"]


def wait_for_outputs(server: str, prompt_id: str, timeout: int, poll_interval: float = 2.0) -> list[dict]:
    deadline = time.time() + timeout
    transient_errors = 0
    while time.time() < deadline:
        try:
            history = get_json(f"{server}/history/{prompt_id}")
        except (ConnectionResetError, TimeoutError, socket.timeout, urllib.error.URLError):
            transient_errors += 1
            if transient_errors > 30:
                raise
            time.sleep(min(10, poll_interval + transient_errors))
            continue
        transient_errors = 0
        item = history.get(prompt_id)
        if item:
            outputs = []
            for node in item.get("outputs", {}).values():
                for key in ("images", "videos", "gifs", "audio"):
                    outputs.extend(node.get(key, []))
            if outputs:
                return outputs
        time.sleep(poll_interval)
    raise TimeoutError(f"Timed out waiting for ComfyUI prompt {prompt_id}")


def is_complete_png(path: Path, settle_seconds: float = 2.0) -> bool:
    """Return true only after ComfyUI has finished writing a valid PNG."""
    try:
        first_size = path.stat().st_size
        if first_size <= 0:
            return False
        time.sleep(settle_seconds)
        second_size = path.stat().st_size
        if second_size != first_size:
            return False
        try:
            from PIL import Image  # type: ignore

            with Image.open(path) as image:
                image.load()
            return True
        except ImportError:
            return path.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
    except Exception:
        return False


def media_is_complete(path: Path, kind: str, settle_seconds: float) -> bool:
    if kind == "image" and path.suffix.lower() == ".png":
        return is_complete_png(path, settle_seconds=settle_seconds)
    try:
        first_size = path.stat().st_size
        if first_size <= 0:
            return False
        time.sleep(settle_seconds)
        return path.stat().st_size == first_size
    except OSError:
        return False


def copy_outputs(outputs: list[dict], comfy_root: Path, asset_root: Path, kind: str, settle_seconds: float) -> list[Path]:
    destination = asset_root / ("images" if kind == "image" else "videos")
    destination.mkdir(parents=True, exist_ok=True)
    copied: list[Path] = []
    for output in outputs:
        filename = output.get("filename")
        subfolder = output.get("subfolder") or ""
        output_type = output.get("type") or "output"
        if not filename:
            continue
        source = comfy_root / output_type / subfolder / filename
        if not source.exists():
            source = comfy_root / "output" / subfolder / filename
        if not source.exists():
            continue
        if not media_is_complete(source, kind, settle_seconds):
            raise RuntimeError(f"ComfyUI output is incomplete or invalid: {source}")
        target = destination / source.name
        if target.exists():
            target = destination / f"{source.stem}-{int(time.time())}{source.suffix}"
        shutil.copy2(source, target)
        if not media_is_complete(target, kind, min(settle_seconds, 0.5)):
            raise RuntimeError(f"Copied output is incomplete or invalid: {target}")
        copied.append(target)
    return copied


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workflow", required=True, help="ComfyUI API workflow JSON.")
    parser.add_argument("--server", default="auto", help="ComfyUI API URL, or 'auto' to use the saved/scanned local server.")
    parser.add_argument("--comfy-root", default=r"C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI")
    parser.add_argument("--asset-root", default=r"C:\Social Content\Asset")
    parser.add_argument("--kind", choices=["image", "video"], default="image")
    parser.add_argument("--timeout", type=int, default=3600)
    parser.add_argument("--settle-seconds", type=float, default=2.0)
    args = parser.parse_args()

    server = resolve_server(args.server)
    workflow = json.loads(Path(args.workflow).read_text(encoding="utf-8"))
    prompt_id = queue_prompt(server, workflow)
    outputs = wait_for_outputs(server, prompt_id, args.timeout)
    copied = copy_outputs(outputs, Path(args.comfy_root), Path(args.asset_root), args.kind, args.settle_seconds)
    print(json.dumps({"server": server, "prompt_id": prompt_id, "copied": [str(path) for path in copied]}, indent=2))
    return 0 if copied else 1


if __name__ == "__main__":
    raise SystemExit(main())
