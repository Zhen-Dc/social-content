#!/usr/bin/env python3
"""Generate canonical sentence-level ComfyUI images for Stolen Innocence."""

from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path


ROOT = Path(r"C:\Social Content")
PACKAGE = ROOT / "Asset" / "Stolen Innocence"
COMFY_HELPER = ROOT / "skills" / "comfyui-media-generator" / "scripts" / "comfyui_api.py"
COMFY_ROOT = ROOT / "ComfyUI_windows_portable_nvidia" / "ComfyUI_windows_portable" / "ComfyUI"
OUTPUT_PREFIX = "stolen_innocence_v8"


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


def latest_existing(scene_id: str) -> Path | None:
    candidates = sorted((PACKAGE / "images").glob(f"{OUTPUT_PREFIX}_{scene_id}_*.png"), key=lambda p: p.stat().st_mtime)
    return candidates[-1] if candidates else None


def latest_comfy_output(scene_id: str, min_mtime: float | None = None) -> Path | None:
    candidates = []
    for path in COMFY_ROOT.joinpath("output").glob(f"{OUTPUT_PREFIX}_{scene_id}_*.png"):
        if min_mtime is None or path.stat().st_mtime >= min_mtime:
            candidates.append(path)
    candidates.sort(key=lambda p: p.stat().st_mtime)
    return candidates[-1] if candidates else None


def wait_for_scene_output(helper, server: str, prompt_id: str, scene_id: str, timeout: int, min_mtime: float) -> Path | list[dict]:
    deadline = time.time() + timeout
    while time.time() < deadline:
        recovered = latest_comfy_output(scene_id, min_mtime=min_mtime)
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
                if item.get("status", {}).get("completed"):
                    recovered = latest_comfy_output(scene_id, min_mtime=min_mtime)
                    if recovered:
                        return recovered
        except Exception:
            pass
        time.sleep(5)
    raise TimeoutError(f"Timed out waiting for {scene_id} / {prompt_id}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--end", type=int, default=42)
    parser.add_argument("--skip-existing", action="store_true")
    parser.add_argument("--timeout", type=int, default=1800)
    args = parser.parse_args()

    helper = load_helper()
    server = helper.resolve_server("auto")
    images_dir = PACKAGE / "images"
    workflows_dir = PACKAGE / "comfyui-workflows"
    images_dir.mkdir(parents=True, exist_ok=True)
    progress_log = PACKAGE / "images" / "generation-progress.log"
    manifest_path = PACKAGE / "images" / "image-generation-manifest.json"

    manifest: dict[str, object] = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "server": server,
        "items": [],
    }

    log(progress_log, f"batch_start server={server} start={args.start} end={args.end} skip_existing={args.skip_existing}")
    for number in range(args.start, args.end + 1):
        scene_id = f"scene-{number:03d}"
        workflow_path = workflows_dir / f"{scene_id}-workflow.json"
        canonical_path = images_dir / f"{scene_id}.png"
        if args.skip_existing and canonical_path.exists() and canonical_path.stat().st_size > 0:
            log(progress_log, f"skip_existing {scene_id} canonical={canonical_path}")
            manifest["items"].append({"scene_id": scene_id, "status": "skipped", "canonical": str(canonical_path)})
            continue
        recovered = latest_comfy_output(scene_id)
        if recovered and recovered.stat().st_size > 0:
            local_copy = images_dir / recovered.name
            if not local_copy.exists():
                shutil.copy2(recovered, local_copy)
            shutil.copy2(recovered, canonical_path)
            log(progress_log, f"recovered {scene_id} source={recovered} canonical={canonical_path}")
            manifest["items"].append({"scene_id": scene_id, "status": "recovered", "source": str(recovered), "canonical": str(canonical_path)})
            manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
            continue
        if not workflow_path.exists():
            log(progress_log, f"missing_workflow {scene_id} workflow={workflow_path}")
            manifest["items"].append({"scene_id": scene_id, "status": "missing_workflow", "workflow": str(workflow_path)})
            continue

        log(progress_log, f"queue {scene_id} workflow={workflow_path}")
        workflow = json.loads(workflow_path.read_text(encoding="utf-8"))
        started = time.time()
        prompt_id = helper.queue_prompt(server, workflow)
        result = wait_for_scene_output(helper, server, prompt_id, scene_id, args.timeout, min_mtime=started - 5)
        if isinstance(result, list):
            copied = helper.copy_outputs(result, COMFY_ROOT, PACKAGE, "image")
            if not copied:
                raise RuntimeError(f"{scene_id} produced no copied image")
            generated_path = copied[0]
        else:
            generated_path = images_dir / result.name
            if not generated_path.exists():
                shutil.copy2(result, generated_path)
        shutil.copy2(generated_path, canonical_path)
        elapsed = round(time.time() - started, 1)
        log(progress_log, f"done {scene_id} seconds={elapsed} generated={generated_path} canonical={canonical_path}")
        manifest["items"].append(
            {
                "scene_id": scene_id,
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
