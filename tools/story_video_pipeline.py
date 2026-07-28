#!/usr/bin/env python3
"""Strict, resumable pipeline guard for Social Content story videos."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
import wave
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(r"C:\Social Content")
ASSET_ROOT = ROOT / "asset"
STORIES_ROOT = ROOT / "stories"
EMBEDDED_PYTHON = ROOT / "ComfyUI_windows_portable_nvidia" / "ComfyUI_windows_portable" / "python_embeded" / "python.exe"
WEB_SCRAPER = ROOT / "skills" / "webscraper" / "scripts" / "web_scraper.py"
STORY_PACKAGER = ROOT / "skills" / "story-time-rewriter" / "scripts" / "story_time_package.py"
CHATTERBOX = ROOT / "skills" / "chatterbox-tts" / "scripts" / "chatterbox_tts.py"
COMFY_API = ROOT / "skills" / "comfyui-media-generator" / "scripts" / "comfyui_api.py"
COMFY_SAFE_LAUNCHER = ROOT / "tools" / "run_comfyui_8190_safe.cmd"
COMFY_STATE = ROOT / ".tmp" / "comfyui_server.json"
DEFAULT_COMFY_TIMEOUT = 3600


LOCAL_SKILLS = [
    "webscraper",
    "story-time-rewriter",
    "chatterbox-tts",
    "film-director",
    "comfyui-media-generator",
    "hyperframes",
    "video-use",
    "social-story-video-maker",
]

EXTERNAL_SKILLS = ["screenwriter", "shotlist-builder"]

STAGE_ORDER = [
    "import-source",
    "package-rewrite",
    "rewrite-verification",
    "screenwriter-shotlist",
    "prompt-package",
    "tts",
    "comfyui-images",
    "hyperframes-render",
    "final-qa",
]


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    severity: str = "error"


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def preferred_python() -> Path:
    if EMBEDDED_PYTHON.exists():
        return EMBEDDED_PYTHON
    return Path(sys.executable)


def normalize_story_name(value: str) -> str:
    cleaned = "".join(ch for ch in value if ch not in '<>:"/\\|?*').strip().rstrip(".")
    return " ".join(cleaned.split()) or "Untitled Story"


def package_path(args: argparse.Namespace) -> Path | None:
    if getattr(args, "package", None):
        return Path(args.package)
    if getattr(args, "story_name", None):
        return ASSET_ROOT / normalize_story_name(args.story_name)
    return None


def stage_dir(pkg: Path) -> Path:
    return pkg / "pipeline-status"


def write_stage_status(pkg: Path, stage: str, status: str, details: dict[str, Any] | None = None) -> None:
    directory = stage_dir(pkg)
    directory.mkdir(parents=True, exist_ok=True)
    payload = {"stage": stage, "status": status, "updated_at": now_iso(), "details": details or {}}
    (directory / f"{stage}.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def run_checked(cmd: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=str(cwd), text=True, capture_output=True, check=True)


def file_ok(path: Path, min_bytes: int = 1) -> bool:
    try:
        return path.exists() and path.is_file() and path.stat().st_size >= min_bytes
    except OSError:
        return False


def dir_has_files(path: Path, pattern: str) -> bool:
    return path.exists() and any(path.glob(pattern))


def valid_png(path: Path, settle_seconds: float = 0.0) -> bool:
    try:
        first = path.stat().st_size
        if first <= 0:
            return False
        if settle_seconds:
            time.sleep(settle_seconds)
            if path.stat().st_size != first:
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


def wav_duration(path: Path) -> float | None:
    try:
        with wave.open(str(path), "rb") as handle:
            frames = handle.getnframes()
            rate = handle.getframerate()
            return round(frames / float(rate), 3) if rate else None
    except Exception:
        return None


def expected_scene_count(pkg: Path) -> int | None:
    candidates = [
        pkg / "scene-beats.json",
        pkg / "director" / "scene-prompts.json",
        pkg / "audio" / "narration-manifest.json",
    ]
    for path in candidates:
        if not path.exists():
            continue
        try:
            data = read_json(path)
        except Exception:
            continue
        if isinstance(data, list):
            return len(data)
        if isinstance(data, dict):
            for key in ("scenes", "beats", "items", "chunks"):
                value = data.get(key)
                if isinstance(value, list):
                    return len(value)
    return None


def package_checks(pkg: Path) -> list[Check]:
    checks: list[Check] = []
    original = pkg / "original script" / "original.txt"
    edited = pkg / "edited script" / "edited.txt"
    name_map = pkg / "edited script" / "name_map.json"
    rewrite_prompt = pkg / "edited script" / "rewrite_prompt.md"
    production_script = pkg / "screenwriter" / "production-script.md"
    shotlist = pkg / "shotlist" / "sentence-shotlist.md"
    asset_plan = pkg / "shotlist" / "asset-plan.md"
    character_bible = pkg / "character-bible.json"
    scene_beats = pkg / "scene-beats.json"
    image_prompts = pkg / "image-prompts.md"
    scene_prompts = pkg / "director" / "scene-prompts.json"
    narration_full = pkg / "audio" / "narration-full.wav"
    narration_manifest = pkg / "audio" / "narration-manifest.json"
    chunks_dir = pkg / "audio" / "chunks"
    images_dir = pkg / "images"
    hyperframes = pkg / "video" / "hyperframes" / "index.html"
    final_mp4 = pkg / "output" / "final.mp4"
    render_manifest = pkg / "render-manifest.json"
    production_manifest = pkg / "output" / "production_manifest.json"

    checks.extend(
        [
            Check("package", pkg.exists(), str(pkg)),
            Check("original", file_ok(original), str(original)),
            Check("name_map", file_ok(name_map), str(name_map)),
            Check("rewrite_prompt", file_ok(rewrite_prompt), str(rewrite_prompt), "warning"),
            Check("edited", file_ok(edited), str(edited)),
            Check("production_script", file_ok(production_script), str(production_script)),
            Check("shotlist", file_ok(shotlist), str(shotlist)),
            Check("asset_plan", file_ok(asset_plan), str(asset_plan)),
            Check("character_bible", file_ok(character_bible), str(character_bible)),
            Check("scene_beats", file_ok(scene_beats), str(scene_beats)),
            Check("image_prompts", file_ok(image_prompts), str(image_prompts)),
            Check("scene_prompts", file_ok(scene_prompts), str(scene_prompts)),
            Check("narration_full", file_ok(narration_full), str(narration_full)),
            Check("narration_manifest", file_ok(narration_manifest), str(narration_manifest)),
            Check("audio_chunks", dir_has_files(chunks_dir, "narration-*.wav"), str(chunks_dir)),
            Check("hyperframes_project", file_ok(hyperframes), str(hyperframes)),
            Check("final_mp4", file_ok(final_mp4, 1024), str(final_mp4)),
            Check("manifest", file_ok(render_manifest) or file_ok(production_manifest), f"{render_manifest} or {production_manifest}"),
        ]
    )

    if file_ok(original):
        text = original.read_text(encoding="utf-8-sig", errors="replace")
        words = len(text.split())
        checks.append(Check("source_word_count", words >= 120, f"{words} words", "warning"))
        prefix = text[:600].lower()
        summary_like = "summary" in prefix or "this story is about" in prefix or "in this story" in prefix
        checks.append(Check("not_summary_like", not summary_like, "source does not look like a summary"))

    metadata = pkg / "metadata.json"
    if metadata.exists():
        try:
            data = read_json(metadata)
            verbatim = data.get("verbatim_capture", {})
            if isinstance(verbatim, dict) and verbatim.get("enabled") is False:
                checks.append(Check("verbatim_capture", False, "metadata says verbatim capture was not enabled"))
        except Exception as exc:
            checks.append(Check("metadata_readable", False, f"{metadata}: {exc}", "warning"))

    expected = expected_scene_count(pkg)
    pngs = sorted(images_dir.glob("*.png")) if images_dir.exists() else []
    valid_pngs = [path for path in pngs if valid_png(path)]
    if expected is not None:
        checks.append(Check("image_count", len(valid_pngs) >= expected, f"{len(valid_pngs)} valid PNGs for {expected} expected scenes"))
    else:
        checks.append(Check("image_count", bool(valid_pngs), f"{len(valid_pngs)} valid PNGs", "warning"))

    if file_ok(final_mp4) and not file_ok(hyperframes):
        checks.append(Check("editable_timeline_for_final", False, "final.mp4 exists but video/hyperframes/index.html is missing"))

    return checks


def package_state(pkg: Path) -> tuple[str, list[Check]]:
    checks = package_checks(pkg)
    errors = [item for item in checks if not item.ok and item.severity == "error"]
    final_names = {"final_mp4", "manifest", "hyperframes_project"}
    if not errors:
        return "complete", checks
    if any(item.name in final_names for item in errors) and file_ok(pkg / "original script" / "original.txt") and file_ok(pkg / "edited script" / "edited.txt"):
        return "ready", checks
    return "blocked", checks


def print_checks(state: str, checks: list[Check]) -> None:
    print(f"state: {state}")
    for item in checks:
        marker = "OK" if item.ok else ("WARN" if item.severity == "warning" else "BLOCKED")
        print(f"{marker}: {item.name}: {item.detail}")


def find_source(args: argparse.Namespace) -> Path:
    if args.source_file:
        path = Path(args.source_file)
    elif args.story_folder:
        path = Path(args.story_folder) / "story.txt"
    else:
        raise SystemExit("Provide --source-file or --story-folder for this stage.")
    if not file_ok(path):
        raise SystemExit(f"Source text not found or empty: {path}")
    return path


def stage_import_source(args: argparse.Namespace) -> None:
    pkg = package_path(args)
    if not pkg:
        raise SystemExit("Provide --story-name or --package.")
    source = find_source(args)
    pkg.mkdir(parents=True, exist_ok=True)
    write_stage_status(pkg, "import-source", "ready", {"source": str(source)})
    print(f"source_ready: {source}")


def stage_package_rewrite(args: argparse.Namespace) -> None:
    pkg = package_path(args)
    if not pkg:
        raise SystemExit("Provide --story-name or --package.")
    source = find_source(args)
    story_name = normalize_story_name(args.story_name or pkg.name)
    cmd = [
        str(preferred_python()),
        str(STORY_PACKAGER),
        "--input",
        str(source),
        "--story-name",
        story_name,
        "--output-root",
        str(ASSET_ROOT),
    ]
    if args.edited_file:
        cmd.extend(["--edited-file", str(Path(args.edited_file))])
    result = run_checked(cmd)
    print(result.stdout.strip())
    write_stage_status(ASSET_ROOT / story_name, "package-rewrite", "complete", {"source": str(source)})


def require_before(pkg: Path, stage: str) -> None:
    required_by_stage = {
        "rewrite-verification": [pkg / "original script" / "original.txt", pkg / "edited script" / "edited.txt", pkg / "edited script" / "name_map.json"],
        "screenwriter-shotlist": [
            pkg / "edited script" / "edited.txt",
            pkg / "screenwriter" / "production-script.md",
            pkg / "shotlist" / "sentence-shotlist.md",
            pkg / "shotlist" / "asset-plan.md",
        ],
        "prompt-package": [
            pkg / "screenwriter" / "production-script.md",
            pkg / "shotlist" / "sentence-shotlist.md",
            pkg / "shotlist" / "asset-plan.md",
            pkg / "character-bible.json",
            pkg / "scene-beats.json",
            pkg / "image-prompts.md",
            pkg / "director" / "scene-prompts.json",
        ],
        "tts": [pkg / "edited script" / "edited.txt"],
        "comfyui-images": [pkg / "director" / "scene-prompts.json"],
        "hyperframes-render": [pkg / "audio" / "narration-manifest.json", pkg / "video" / "hyperframes" / "index.html"],
        "final-qa": [pkg / "output" / "final.mp4", pkg / "video" / "hyperframes" / "index.html"],
    }
    missing = [str(path) for path in required_by_stage.get(stage, []) if not file_ok(path)]
    if missing:
        write_stage_status(pkg, stage, "blocked", {"missing": missing})
        raise SystemExit(f"{stage} blocked. Missing:\n- " + "\n- ".join(missing))


def stage_rewrite_verification(args: argparse.Namespace) -> None:
    pkg = require_package(args)
    require_before(pkg, "rewrite-verification")
    original = (pkg / "original script" / "original.txt").read_text(encoding="utf-8-sig", errors="replace").strip()
    edited = (pkg / "edited script" / "edited.txt").read_text(encoding="utf-8-sig", errors="replace").strip()
    if original == edited:
        write_stage_status(pkg, "rewrite-verification", "blocked", {"reason": "edited.txt matches original.txt"})
        raise SystemExit("rewrite-verification blocked: edited.txt matches original.txt.")
    if len(edited.split()) < max(80, int(len(original.split()) * 0.25)):
        write_stage_status(pkg, "rewrite-verification", "blocked", {"reason": "edited.txt is too short compared with original.txt"})
        raise SystemExit("rewrite-verification blocked: edited.txt looks too short for a full rewrite.")
    write_stage_status(pkg, "rewrite-verification", "complete")
    print("rewrite_verification: complete")


def stage_artifact_gate(args: argparse.Namespace, stage: str) -> None:
    pkg = require_package(args)
    require_before(pkg, stage)
    write_stage_status(pkg, stage, "complete")
    print(f"{stage}: complete")


def build_narration_manifest(pkg: Path, voice: str, persona: str | None, model: str) -> None:
    chunks = []
    for path in sorted((pkg / "audio" / "chunks").glob("narration-*.wav")):
        chunks.append({"file": str(path.relative_to(pkg)), "duration": wav_duration(path)})
    payload = {
        "generated_at": now_iso(),
        "text_file": "edited script/edited.txt",
        "full_audio": "audio/narration-full.wav",
        "voice": voice,
        "persona": persona,
        "model": model,
        "chunks": chunks,
    }
    (pkg / "audio" / "narration-manifest.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def stage_tts(args: argparse.Namespace) -> None:
    pkg = require_package(args)
    require_before(pkg, "tts")
    audio = pkg / "audio"
    chunks = audio / "chunks"
    audio.mkdir(parents=True, exist_ok=True)
    chunks.mkdir(parents=True, exist_ok=True)
    cmd = [
        str(preferred_python()),
        str(CHATTERBOX),
        "generate",
        "--model",
        args.model,
        "--text-file",
        str(pkg / "edited script" / "edited.txt"),
        "--output",
        str(audio / "narration-full.wav"),
        "--chunk-output-dir",
        str(chunks),
    ]
    if args.persona:
        cmd.extend(["--persona", args.persona])
    else:
        cmd.extend(["--voice", args.voice])
    subprocess.run(cmd, cwd=str(ROOT), check=True)
    build_narration_manifest(pkg, args.voice, args.persona, args.model)
    write_stage_status(pkg, "tts", "complete", {"manifest": str(audio / "narration-manifest.json")})
    print(f"tts: complete {audio / 'narration-manifest.json'}")


def get_json_url(url: str, timeout: int = 5) -> dict[str, Any] | None:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except (ConnectionResetError, TimeoutError, socket.timeout, urllib.error.URLError, OSError, json.JSONDecodeError):
        return None


def discover_comfy_server() -> str | None:
    if COMFY_STATE.exists():
        try:
            server = str(read_json(COMFY_STATE).get("server", "")).rstrip("/")
            if server and get_json_url(f"{server}/system_stats"):
                return server
        except Exception:
            pass
    for port in range(8190, 8200):
        server = f"http://127.0.0.1:{port}"
        if get_json_url(f"{server}/system_stats"):
            return server
    return None


def ensure_comfy_server(start: bool) -> str:
    server = discover_comfy_server()
    if server:
        return server
    if not start:
        raise SystemExit("ComfyUI API is not responding on ports 8190-8199.")
    if not COMFY_SAFE_LAUNCHER.exists():
        raise SystemExit(f"Safe ComfyUI launcher is missing: {COMFY_SAFE_LAUNCHER}")
    subprocess.Popen([str(COMFY_SAFE_LAUNCHER)], cwd=str(ROOT), creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    deadline = time.time() + 180
    while time.time() < deadline:
        server = discover_comfy_server()
        if server:
            return server
        time.sleep(3)
    raise SystemExit("Timed out waiting for ComfyUI after safe launcher start.")


def canonical_image_for_workflow(pkg: Path, workflow: Path) -> Path:
    stem = workflow.stem
    if stem.endswith("-workflow"):
        stem = stem[: -len("-workflow")]
    return pkg / "images" / f"{stem}.png"


def stage_comfyui_images(args: argparse.Namespace) -> None:
    pkg = require_package(args)
    require_before(pkg, "comfyui-images")
    workflows = sorted((pkg / "comfyui-workflows").glob("*.json"))
    if not workflows:
        raise SystemExit(f"No workflow JSON files found in {pkg / 'comfyui-workflows'}")
    server = ensure_comfy_server(start=not args.no_start_comfyui)
    completed = []
    for workflow in workflows:
        canonical = canonical_image_for_workflow(pkg, workflow)
        canonical.parent.mkdir(parents=True, exist_ok=True)
        if args.skip_existing and canonical.exists() and valid_png(canonical, settle_seconds=0.1):
            completed.append(str(canonical))
            continue
        cmd = [
            str(preferred_python()),
            str(COMFY_API),
            "--workflow",
            str(workflow),
            "--server",
            server,
            "--asset-root",
            str(pkg),
            "--kind",
            "image",
            "--timeout",
            str(args.comfy_timeout),
        ]
        result = run_checked(cmd)
        payload = json.loads(result.stdout)
        copied = [Path(path) for path in payload.get("copied", [])]
        if not copied:
            raise SystemExit(f"ComfyUI returned no copied image for {workflow}")
        newest = copied[0]
        if not valid_png(newest, settle_seconds=0.5):
            raise SystemExit(f"ComfyUI copied image is incomplete or invalid: {newest}")
        if newest.resolve() != canonical.resolve():
            shutil.copy2(newest, canonical)
        if not valid_png(canonical, settle_seconds=0.5):
            raise SystemExit(f"Canonical image is incomplete or invalid: {canonical}")
        completed.append(str(canonical))
    write_stage_status(pkg, "comfyui-images", "complete", {"server": server, "images": completed})
    print(json.dumps({"server": server, "images": completed}, indent=2))


def stage_hyperframes_render(args: argparse.Namespace) -> None:
    pkg = require_package(args)
    require_before(pkg, "hyperframes-render")
    npx = shutil.which("npx.cmd") or shutil.which("npx")
    if not npx:
        raise SystemExit("npx was not found on PATH; cannot run HyperFrames.")
    project = pkg / "video" / "hyperframes"
    output = pkg / "output" / "final.mp4"
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([npx, "hyperframes", "lint", str(project)], cwd=str(ROOT), check=True)
    subprocess.run([npx, "hyperframes", "render", str(project), "index.html", "--output", str(output)], cwd=str(ROOT), check=True)
    write_stage_status(pkg, "hyperframes-render", "complete", {"output": str(output)})
    print(f"hyperframes_render: complete {output}")


def stage_final_qa(args: argparse.Namespace) -> None:
    pkg = require_package(args)
    require_before(pkg, "final-qa")
    state, checks = package_state(pkg)
    manifest = {
        "generated_at": now_iso(),
        "state": state,
        "checks": [check.__dict__ for check in checks],
    }
    (pkg / "render-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    write_stage_status(pkg, "final-qa", "complete" if state == "complete" else "blocked", {"state": state})
    print_checks(state, checks)
    if state != "complete":
        raise SystemExit("final-qa blocked: package is not complete.")


def require_package(args: argparse.Namespace) -> Path:
    pkg = package_path(args)
    if not pkg:
        raise SystemExit("Provide --story-name or --package.")
    if not pkg.exists():
        raise SystemExit(f"Package not found: {pkg}")
    return pkg


def cmd_status(args: argparse.Namespace) -> int:
    pkg = require_package(args)
    state, checks = package_state(pkg)
    print_checks(state, checks)
    return 0 if state in {"ready", "complete"} else 1


def cmd_plan(args: argparse.Namespace) -> int:
    pkg = package_path(args)
    print("canonical_stage_order:")
    for index, stage in enumerate(STAGE_ORDER, start=1):
        print(f"{index}. {stage}")
    if pkg and pkg.exists():
        print()
        state, checks = package_state(pkg)
        print_checks(state, checks)
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    py = preferred_python()
    print(f"workspace: {ROOT}")
    print(f"python: {'OK' if py.exists() else 'MISSING'} {py}")
    print("local_skills:")
    for skill in LOCAL_SKILLS:
        path = ROOT / "skills" / skill / "SKILL.md"
        print(f"  {skill}: {'OK' if path.exists() else 'MISSING'} {path}")
    print("external_skills:")
    external_roots = [Path.home() / ".codex" / "skills", Path.home() / ".agents" / "skills"]
    for skill in EXTERNAL_SKILLS:
        matches = [root / skill / "SKILL.md" for root in external_roots if (root / skill / "SKILL.md").exists()]
        detail = str(matches[0]) if matches else r"not local to C:\Social Content"
        print(f"  {skill}: {'OK' if matches else 'EXTERNAL_OR_MISSING'} {detail}")

    print("webscraper_cli:")
    try:
        result = run_checked([str(py), str(WEB_SCRAPER), "--help"])
        flags = sorted({word for word in result.stdout.replace(",", " ").split() if word.startswith("--")})
        print("  flags: " + " ".join(flags))
        print(f"  unsupported_source_file_flag: {'--source-file' not in flags}")
    except Exception as exc:
        print(f"  ERROR: {exc}")

    personas = ROOT / "Asset" / "voices" / "personas.json"
    try:
        data = read_json(personas) if personas.exists() else {}
        count = len(data.get("personas", data)) if isinstance(data, dict) else 0
        print(f"chatterbox_personas: {'OK' if personas.exists() else 'MISSING'} {personas} count={count}")
    except Exception as exc:
        print(f"chatterbox_personas: ERROR {exc}")

    server = discover_comfy_server()
    print(f"comfyui_server: {'OK ' + server if server else 'NOT_RUNNING'}")
    npx = shutil.which("npx.cmd") or shutil.which("npx")
    print(f"hyperframes_npx: {'OK' if npx else 'MISSING'} {npx or ''}")
    return 0


def cmd_run_stage(args: argparse.Namespace) -> int:
    stage = args.stage
    runners = {
        "import-source": stage_import_source,
        "package-rewrite": stage_package_rewrite,
        "rewrite-verification": stage_rewrite_verification,
        "screenwriter-shotlist": lambda parsed: stage_artifact_gate(parsed, "screenwriter-shotlist"),
        "prompt-package": lambda parsed: stage_artifact_gate(parsed, "prompt-package"),
        "tts": stage_tts,
        "comfyui-images": stage_comfyui_images,
        "hyperframes-render": stage_hyperframes_render,
        "final-qa": stage_final_qa,
    }
    runners[stage](args)
    return 0


def cmd_run_all(args: argparse.Namespace) -> int:
    for stage in STAGE_ORDER:
        args.stage = stage
        print(f"== {stage} ==")
        cmd_run_stage(args)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Strict Social Content story-video pipeline runner.")
    parser.add_argument("--story-name", help="Story package name under C:\\Social Content\\asset.")
    parser.add_argument("--package", help="Explicit story package path.")
    parser.add_argument("--source-file", help="Source story text file.")
    parser.add_argument("--story-folder", help="Webscraper story folder containing story.txt.")
    parser.add_argument("--edited-file", help="Completed rewrite to copy during package-rewrite.")
    parser.add_argument("--voice", default="Paul_male")
    parser.add_argument("--persona")
    parser.add_argument("--model", choices=["turbo", "tts"], default="turbo")
    parser.add_argument("--comfy-timeout", type=int, default=DEFAULT_COMFY_TIMEOUT)
    parser.add_argument("--no-start-comfyui", action="store_true")
    parser.add_argument("--skip-existing", action=argparse.BooleanOptionalAction, default=True)

    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor")
    sub.add_parser("plan")
    sub.add_parser("status")
    run_stage = sub.add_parser("run-stage")
    run_stage.add_argument("stage", choices=STAGE_ORDER)
    sub.add_parser("run-all")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    commands = {
        "doctor": cmd_doctor,
        "plan": cmd_plan,
        "status": cmd_status,
        "run-stage": cmd_run_stage,
        "run-all": cmd_run_all,
    }
    return commands[args.command](args)


if __name__ == "__main__":
    raise SystemExit(main())
