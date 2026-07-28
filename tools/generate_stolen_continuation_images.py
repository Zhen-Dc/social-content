#!/usr/bin/env python3
"""Generate ComfyUI images for Stolen Innocence continuation packages."""

from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

from PIL import Image


ROOT = Path(r"C:\Social Content")
PACKAGE = ROOT / "Asset" / "Stolen Innocence"
COMFY_HELPER = ROOT / "skills" / "comfyui-media-generator" / "scripts" / "comfyui_api.py"
COMFY_ROOT = ROOT / "ComfyUI_windows_portable_nvidia" / "ComfyUI_windows_portable" / "ComfyUI"
OUTPUT_PREFIX = "stolen_innocence_long_p1"


def load_helper():
    spec = importlib.util.spec_from_file_location("comfyui_api", COMFY_HELPER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {COMFY_HELPER}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["comfyui_api"] = module
    spec.loader.exec_module(module)
    return module


def log(path: Path, message: str) -> None:
    line = f"{datetime.now().isoformat(timespec='seconds')} {message}"
    print(line, flush=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def latest_comfy_output(shot_id: str, min_mtime: float | None = None) -> Path | None:
    candidates = []
    for path in COMFY_ROOT.joinpath("output").glob(f"{OUTPUT_PREFIX}_{shot_id}_*.png"):
        if min_mtime is None or path.stat().st_mtime >= min_mtime:
            candidates.append(path)
    candidates.sort(key=lambda p: p.stat().st_mtime)
    for candidate in reversed(candidates):
        if is_complete_png(candidate):
            return candidate
    return None


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
        with Image.open(path) as image:
            image.load()
        return True
    except Exception:
        return False


def wait_for_output(helper, server: str, prompt_id: str, shot_id: str, timeout: int, min_mtime: float):
    deadline = time.time() + timeout
    while time.time() < deadline:
        recovered = latest_comfy_output(shot_id, min_mtime=min_mtime)
        if recovered:
            return recovered
        try:
            history = helper.get_json(f"{server}/history/{prompt_id}", timeout=10)
            item = history.get(prompt_id)
            if item:
                outputs = []
                for node in item.get("outputs", {}).values():
                    for key in ("images", "videos", "gifs", "audio"):
                        outputs.extend(node.get(key, []))
                if outputs:
                    return outputs
        except Exception:
            pass
        time.sleep(5)
    raise TimeoutError(f"Timed out waiting for {shot_id} / {prompt_id}")


def shot_id(number: int) -> str:
    return f"p001-s{number:03d}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--part", default="continuation-part-001")
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--end", type=int, default=36)
    parser.add_argument("--skip-existing", action="store_true")
    parser.add_argument("--timeout", type=int, default=2400)
    args = parser.parse_args()

    helper = load_helper()
    server = helper.resolve_server("auto")
    part_root = PACKAGE / args.part
    workflows_dir = part_root / "comfyui-workflows"
    images_dir = part_root / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    progress_log = images_dir / "generation-progress.log"
    manifest_path = images_dir / "image-generation-manifest.json"

    manifest: dict[str, object] = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "server": server,
        "part": args.part,
        "items": [],
    }

    log(progress_log, f"batch_start server={server} part={args.part} start={args.start} end={args.end}")
    for number in range(args.start, args.end + 1):
        sid = shot_id(number)
        workflow_path = workflows_dir / f"{sid}-workflow.json"
        canonical_path = images_dir / f"{sid}.png"
        if args.skip_existing and canonical_path.exists() and is_complete_png(canonical_path, settle_seconds=0.1):
            log(progress_log, f"skip_existing {sid} canonical={canonical_path}")
            manifest["items"].append({"shot_id": sid, "status": "skipped", "canonical": str(canonical_path)})
            continue
        if not workflow_path.exists():
            log(progress_log, f"missing_workflow {sid} workflow={workflow_path}")
            manifest["items"].append({"shot_id": sid, "status": "missing_workflow", "workflow": str(workflow_path)})
            continue

        log(progress_log, f"queue {sid} workflow={workflow_path}")
        workflow = json.loads(workflow_path.read_text(encoding="utf-8-sig"))
        started = time.time()
        prompt_id = helper.queue_prompt(server, workflow)
        result = wait_for_output(helper, server, prompt_id, sid, args.timeout, min_mtime=started - 5)
        if isinstance(result, list):
            copied = helper.copy_outputs(result, COMFY_ROOT, part_root, "image", settle_seconds=2.0)
            if not copied:
                raise RuntimeError(f"{sid} produced no copied image")
            generated_path = copied[0]
        else:
            generated_path = images_dir / result.name
            if not generated_path.exists():
                shutil.copy2(result, generated_path)
        if not is_complete_png(generated_path, settle_seconds=0.5):
            raise RuntimeError(f"{sid} copied image is incomplete or invalid: {generated_path}")
        shutil.copy2(generated_path, canonical_path)
        if not is_complete_png(canonical_path, settle_seconds=0.5):
            raise RuntimeError(f"{sid} canonical image is incomplete or invalid: {canonical_path}")
        elapsed = round(time.time() - started, 1)
        log(progress_log, f"done {sid} seconds={elapsed} generated={generated_path} canonical={canonical_path}")
        manifest["items"].append(
            {
                "shot_id": sid,
                "status": "generated",
                "prompt_id": prompt_id,
                "seconds": elapsed,
                "generated": str(generated_path),
                "canonical": str(canonical_path),
            }
        )
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    log(progress_log, "batch_complete")
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
