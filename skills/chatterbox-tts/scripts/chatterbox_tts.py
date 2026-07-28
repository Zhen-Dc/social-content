#!/usr/bin/env python3
"""Wrapper for the user's local Chatterbox TTS install."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


DEFAULT_ROOT = Path(r"C:\Ai Tools\Chatterbox -TTS with Turbo\Chatterbox TTS with Turbo")
DEFAULT_VOICE = "Paul_male"
DEFAULT_OUTPUT_DIR = Path(r"C:\Social Content\Asset\audio\chatterbox")
DEFAULT_NUMBA_CACHE = Path(r"C:\Social Content\.tmp\numba-cache")
DEFAULT_PERSONA_REGISTRY = Path(r"C:\Social Content\Asset\voices\personas.json")
DEFAULT_PERSONA_ALIASES = {
    "old woman": "Morganna_female",
    "elderly woman": "Morganna_female",
    "old female narrator": "Morganna_female",
    "elder female narrator": "Morganna_female",
}
WORKER_FLAG = "_worker_generate"


def voice_dir(root: Path) -> Path:
    return root / "modules" / "voice_samples"


def chatterbox_python(root: Path) -> Path:
    return root / "python" / "python.exe"


def normalize_stem(value: str) -> str:
    value = value.strip().strip('"')
    if value.lower().endswith(".wav"):
        value = value[:-4]
    return value


def normalize_persona_key(value: str) -> str:
    return re.sub(r"[\s_-]+", " ", value.strip().strip('"').lower())


def load_voice_personas() -> dict[str, str]:
    aliases = dict(DEFAULT_PERSONA_ALIASES)
    if not DEFAULT_PERSONA_REGISTRY.exists():
        return aliases

    try:
        data = json.loads(DEFAULT_PERSONA_REGISTRY.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid persona registry: {DEFAULT_PERSONA_REGISTRY}: {exc}") from exc

    personas = data.get("personas", data) if isinstance(data, dict) else {}
    if not isinstance(personas, dict):
        raise SystemExit(f"Persona registry must be a JSON object: {DEFAULT_PERSONA_REGISTRY}")

    for key, value in personas.items():
        if isinstance(key, str) and isinstance(value, str):
            aliases[key] = value
    return aliases


def save_voice_persona(persona: str, voice_name: str) -> None:
    DEFAULT_PERSONA_REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    data: dict[str, object] = {"personas": {}}
    if DEFAULT_PERSONA_REGISTRY.exists():
        try:
            existing = json.loads(DEFAULT_PERSONA_REGISTRY.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Invalid persona registry: {DEFAULT_PERSONA_REGISTRY}: {exc}") from exc
        if isinstance(existing, dict):
            data.update(existing)

    personas = data.get("personas")
    if not isinstance(personas, dict):
        personas = {}
    personas[persona] = voice_name
    data["personas"] = personas
    DEFAULT_PERSONA_REGISTRY.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def resolve_persona_alias(value: str) -> str:
    requested = normalize_persona_key(value)
    for persona, voice_name in load_voice_personas().items():
        if normalize_persona_key(persona) == requested:
            return voice_name
    return value


def list_voice_files(root: Path) -> list[Path]:
    directory = voice_dir(root)
    if not directory.exists():
        return []
    return sorted(directory.glob("*.wav"), key=lambda p: p.stem.lower())


def resolve_voice(root: Path, voice: str | None) -> Path | None:
    if not voice or voice.lower() in {"builtin", "default", "none"}:
        return None

    voice = resolve_persona_alias(voice)
    raw = Path(voice)
    if raw.exists():
        return raw.resolve()

    requested = normalize_stem(voice)
    files = list_voice_files(root)

    for path in files:
        if path.stem == requested or path.name == voice:
            return path

    lowered = requested.lower()
    for path in files:
        if path.stem.lower() == lowered:
            return path

    compact = re.sub(r"[\s_-]+", "", lowered)
    for path in files:
        if re.sub(r"[\s_-]+", "", path.stem.lower()) == compact:
            return path

    raise SystemExit(f"Voice not found: {voice}. Run list-voices to see available names.")


def read_text(args: argparse.Namespace) -> str:
    if args.text_file:
        return Path(args.text_file).read_text(encoding="utf-8")
    if args.text:
        return args.text
    raise SystemExit("Provide --text or --text-file.")


def chunk_text(text: str, max_words: int = 40) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+|\n+", text.strip())
    chunks: list[str] = []
    current: list[str] = []
    count = 0
    for part in parts:
        part = part.strip()
        if not part:
            continue
        words = len(part.split())
        if current and count + words > max_words:
            chunks.append(" ".join(current))
            current = [part]
            count = words
        else:
            current.append(part)
            count += words
    if current:
        chunks.append(" ".join(current))
    return chunks or [text]


def register_voice(args: argparse.Namespace) -> None:
    root = Path(args.chatterbox_root)
    sample = Path(args.sample)
    if not sample.exists():
        raise SystemExit(f"Sample not found: {sample}")
    if not args.name.strip():
        raise SystemExit("--name cannot be empty.")
    if args.gender not in {"male", "female"}:
        raise SystemExit("--gender must be male or female.")

    safe_name = re.sub(r"[^A-Za-z0-9 _-]+", "", args.name).strip().replace(" ", "_")
    if not safe_name:
        raise SystemExit("Voice name became empty after sanitizing.")

    stem = f"{safe_name}_{args.gender}"
    if args.language and args.language != "en":
        stem = f"{stem}_{args.language}"

    directory = voice_dir(root)
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / f"{stem}.wav"
    if target.exists() and not args.force:
        raise SystemExit(f"Voice already exists: {target}. Add --force to overwrite.")

    shutil.copy2(sample, target)
    print(str(target))
    for persona in args.persona or []:
        save_voice_persona(persona, stem)
        print(f"persona: {persona} -> {stem}")


def list_voices(args: argparse.Namespace) -> None:
    root = Path(args.chatterbox_root)
    files = list_voice_files(root)
    if not files:
        raise SystemExit(f"No voices found in {voice_dir(root)}")
    for path in files:
        marker = " *default" if path.stem == DEFAULT_VOICE else ""
        print(f"{path.stem}{marker}")


def list_personas(args: argparse.Namespace) -> None:
    for persona, voice_name in sorted(load_voice_personas().items(), key=lambda item: item[0].lower()):
        print(f"{persona}: {voice_name}")


def doctor(args: argparse.Namespace) -> None:
    root = Path(args.chatterbox_root)
    py = chatterbox_python(root)
    checks = [
        ("root", root.exists(), root),
        ("embedded_python", py.exists(), py),
        ("source", (root / "src" / "chatterbox").exists(), root / "src" / "chatterbox"),
        ("voices", voice_dir(root).exists(), voice_dir(root)),
    ]
    for name, ok, path in checks:
        print(f"{name}: {'OK' if ok else 'MISSING'} {path}")
    print(f"voice_count: {len(list_voice_files(root))}")
    print(f"default_voice: {DEFAULT_VOICE}")
    print(f"persona_registry: {DEFAULT_PERSONA_REGISTRY}")
    print(f"persona_count: {len(load_voice_personas())}")


def generate(args: argparse.Namespace) -> None:
    root = Path(args.chatterbox_root)
    py = chatterbox_python(root)
    if not py.exists():
        raise SystemExit(f"Chatterbox embedded Python not found: {py}")

    text = read_text(args)
    output = Path(args.output) if args.output else DEFAULT_OUTPUT_DIR / "chatterbox-output.wav"
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    voice_request = args.persona if args.persona else args.voice
    voice_path = resolve_voice(root, voice_request)

    cmd = [
        str(py),
        "-u",
        str(Path(__file__).resolve()),
        WORKER_FLAG,
        "--chatterbox-root",
        str(root),
        "--model",
        args.model,
        "--output",
        str(output),
        "--temperature",
        str(args.temperature),
        "--exaggeration",
        str(args.exaggeration),
        "--cfg-weight",
        str(args.cfg_weight),
        "--seed",
        str(args.seed),
        "--max-words",
        str(args.max_words),
    ]
    if voice_path is not None:
        cmd.extend(["--voice-path", str(voice_path)])
    if args.chunk_output_dir:
        cmd.extend(["--chunk-output-dir", str(Path(args.chunk_output_dir).resolve())])
    cmd.extend(["--text", text])

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    env["HF_HUB_VERBOSITY"] = env.get("HF_HUB_VERBOSITY", "info")
    DEFAULT_NUMBA_CACHE.mkdir(parents=True, exist_ok=True)
    env["NUMBA_CACHE_DIR"] = env.get("NUMBA_CACHE_DIR", str(DEFAULT_NUMBA_CACHE))
    env["PYTHONPATH"] = str(root / "src") + os.pathsep + str(root) + os.pathsep + env.get("PYTHONPATH", "")

    print(f"chatterbox_python: {py}", flush=True)
    print(f"model: {args.model}", flush=True)
    print(f"voice_request: {voice_request}", flush=True)
    print(f"voice: {voice_path if voice_path else 'builtin'}", flush=True)
    print(f"output: {output}", flush=True)
    subprocess.run(cmd, cwd=str(root), env=env, check=True)
    print(str(output))


def worker_generate(args: argparse.Namespace) -> None:
    root = Path(args.chatterbox_root)
    os.chdir(root)
    DEFAULT_NUMBA_CACHE.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("NUMBA_CACHE_DIR", str(DEFAULT_NUMBA_CACHE))
    sys.path.insert(0, str(root / "src"))
    sys.path.insert(0, str(root))

    import random

    import numpy as np
    import soundfile as sf
    import torch

    if args.seed:
        seed = int(args.seed)
        torch.manual_seed(seed)
        random.seed(seed)
        np.random.seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"worker_device: {device}", flush=True)
    if args.model == "turbo":
        print("importing_model_module: turbo", flush=True)
        from chatterbox.tts_turbo import ChatterboxTurboTTS

        print("loading_model: turbo", flush=True)
        model = ChatterboxTurboTTS.from_pretrained(device=device)
    else:
        print("importing_model_module: tts", flush=True)
        from chatterbox.tts import ChatterboxTTS

        print("loading_model: tts", flush=True)
        model = ChatterboxTTS.from_pretrained(device=device)

    generated = []
    chunks = chunk_text(args.text, max_words=args.max_words)
    print(f"chunks: {len(chunks)}", flush=True)
    chunk_dir = Path(args.chunk_output_dir) if args.chunk_output_dir else None
    if chunk_dir:
        chunk_dir.mkdir(parents=True, exist_ok=True)
    for index, chunk in enumerate(chunks, start=1):
        print(f"generating_chunk: {index}/{len(chunks)}", flush=True)
        kwargs = {"audio_prompt_path": args.voice_path}
        if args.model == "tts":
            kwargs.update(
                {
                    "temperature": args.temperature,
                    "exaggeration": args.exaggeration,
                    "cfg_weight": args.cfg_weight,
                }
            )
        wav = model.generate(chunk, **kwargs)
        if chunk_dir:
            chunk_audio = wav.squeeze(0).detach().cpu().numpy()
            sf.write(chunk_dir / f"narration-{index:03d}.wav", chunk_audio, model.sr)
        generated.append(wav)

    full = torch.cat(generated, dim=-1) if len(generated) > 1 else generated[0]
    audio = full.squeeze(0).detach().cpu().numpy()
    sf.write(args.output, audio, model.sr)
    print(args.output)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate speech with local Chatterbox TTS.")
    parser.add_argument("--chatterbox-root", default=str(DEFAULT_ROOT))
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list-voices").set_defaults(func=list_voices)
    sub.add_parser("list-personas").set_defaults(func=list_personas)
    sub.add_parser("doctor").set_defaults(func=doctor)

    reg = sub.add_parser("register-voice")
    reg.add_argument("--sample", required=True)
    reg.add_argument("--name", required=True)
    reg.add_argument("--gender", choices=["male", "female"], required=True)
    reg.add_argument("--language", default="en")
    reg.add_argument("--persona", action="append", help="Persona alias to route to this voice, e.g. 'old woman'.")
    reg.add_argument("--force", action="store_true")
    reg.set_defaults(func=register_voice)

    gen = sub.add_parser("generate")
    gen.add_argument("--text")
    gen.add_argument("--text-file")
    gen.add_argument("--voice", default=DEFAULT_VOICE)
    gen.add_argument("--persona", help="Persona alias to resolve before voice lookup, e.g. 'old woman'.")
    gen.add_argument("--model", choices=["turbo", "tts"], default="turbo")
    gen.add_argument("--output")
    gen.add_argument("--temperature", type=float, default=0.8)
    gen.add_argument("--exaggeration", type=float, default=0.5)
    gen.add_argument("--cfg-weight", type=float, default=0.5)
    gen.add_argument("--seed", type=int, default=0)
    gen.add_argument("--max-words", type=int, default=40)
    gen.add_argument("--chunk-output-dir")
    gen.set_defaults(func=generate)

    worker = sub.add_parser(WORKER_FLAG)
    worker.add_argument("--chatterbox-root", required=True)
    worker.add_argument("--model", choices=["turbo", "tts"], required=True)
    worker.add_argument("--output", required=True)
    worker.add_argument("--text", required=True)
    worker.add_argument("--voice-path")
    worker.add_argument("--chunk-output-dir")
    worker.add_argument("--temperature", type=float, default=0.8)
    worker.add_argument("--exaggeration", type=float, default=0.5)
    worker.add_argument("--cfg-weight", type=float, default=0.5)
    worker.add_argument("--seed", type=int, default=0)
    worker.add_argument("--max-words", type=int, default=40)
    worker.set_defaults(func=worker_generate)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
