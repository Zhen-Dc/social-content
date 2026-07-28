from __future__ import annotations

import html
import json
import math
import re
import shutil
import struct
import wave
from pathlib import Path


ROOT = Path(r"C:\Social Content")
PART = ROOT / "Asset" / "Stolen Innocence" / "continuation-part-001"
VIDEO = PART / "video" / "hyperframes"
MEDIA_IMAGES = VIDEO / "media" / "images"
MEDIA_AUDIO = VIDEO / "media" / "audio"
CAPTIONS_DIR = PART / "video" / "captions"
VERIFY_DIR = PART / "video" / "verify"
OUTPUT_DIR = PART / "output"

WIDTH = 1080
HEIGHT = 1920
FPS = 30
VOICE = "young woman"


def chunk_text(text: str, max_words: int = 35) -> list[str]:
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


def wav_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as handle:
        return handle.getnframes() / float(handle.getframerate())


def srt_time(seconds: float) -> str:
    millis = int(round(seconds * 1000))
    hours = millis // 3_600_000
    millis %= 3_600_000
    minutes = millis // 60_000
    millis %= 60_000
    secs = millis // 1000
    millis %= 1000
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"


def write_wave(path: Path, samples: list[float], sample_rate: int = 24_000) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(sample_rate)
        frames = bytearray()
        for sample in samples:
            clipped = max(-1.0, min(1.0, sample))
            frames.extend(struct.pack("<h", int(clipped * 32767)))
        handle.writeframes(bytes(frames))


def make_ambient_bed(path: Path, duration: float, sample_rate: int = 24_000) -> None:
    total = int(duration * sample_rate)
    samples: list[float] = []
    for i in range(total):
        t = i / sample_rate
        fade_in = min(1.0, t / 8.0)
        fade_out = min(1.0, max(0.0, (duration - t) / 10.0))
        env = min(fade_in, fade_out)
        slow = math.sin(2 * math.pi * 0.018 * t) * 0.008
        tone_a = math.sin(2 * math.pi * 73.42 * t) * 0.020
        tone_b = math.sin(2 * math.pi * 109.0 * t + 0.7) * 0.013
        tone_c = math.sin(2 * math.pi * 146.8 * t + 1.9) * 0.007
        samples.append((tone_a + tone_b + tone_c + slow) * env)
    write_wave(path, samples, sample_rate)


def make_whoosh(path: Path, sample_rate: int = 24_000) -> None:
    duration = 0.55
    total = int(duration * sample_rate)
    samples: list[float] = []
    for i in range(total):
        t = i / sample_rate
        p = t / duration
        env = math.sin(math.pi * p) ** 1.8
        freq = 180 + 720 * p
        sample = math.sin(2 * math.pi * freq * t) * 0.035 * env
        sample += math.sin(2 * math.pi * (freq * 0.51) * t + 0.9) * 0.016 * env
        samples.append(sample)
    write_wave(path, samples, sample_rate)


def make_chime(path: Path, sample_rate: int = 24_000) -> None:
    duration = 1.45
    total = int(duration * sample_rate)
    samples: list[float] = []
    for i in range(total):
        t = i / sample_rate
        env = math.exp(-2.9 * t)
        sample = math.sin(2 * math.pi * 392.0 * t) * 0.055 * env
        sample += math.sin(2 * math.pi * 587.33 * t) * 0.032 * env
        samples.append(sample)
    write_wave(path, samples, sample_rate)


def load_audio_manifest() -> dict:
    text = (PART / "audio" / "narration-text.txt").read_text(encoding="utf-8")
    chunks = chunk_text(text, max_words=35)
    chunk_dir = PART / "audio" / "chunks"
    wavs = sorted(chunk_dir.glob("narration-*.wav"))
    if len(chunks) != len(wavs):
        raise RuntimeError(f"caption chunk count {len(chunks)} does not match wav count {len(wavs)}")

    rows = []
    start = 0.0
    for index, (chunk, wav) in enumerate(zip(chunks, wavs), start=1):
        duration = wav_duration(wav)
        rows.append(
            {
                "id": f"narration-{index:03d}",
                "text": chunk,
                "file": str(wav),
                "start": round(start, 3),
                "duration": round(duration, 3),
                "end": round(start + duration, 3),
                "voice": VOICE,
                "model": "turbo",
            }
        )
        start += duration

    full_path = PART / "audio" / "narration-full.wav"
    full_duration = wav_duration(full_path)
    manifest = {
        "project": "Stolen Innocence",
        "part": "continuation-part-001",
        "voice": VOICE,
        "narrator": "young woman first-person Amara, recalling childhood events",
        "model": "turbo",
        "seed": 240705,
        "sample_rate": 24000,
        "total_duration": round(full_duration, 3),
        "chunks": rows,
        "source_text": str(PART / "audio" / "narration-text.txt"),
        "full_audio": str(full_path),
    }
    (PART / "audio" / "narration-manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def write_srt(chunks: list[dict]) -> Path:
    CAPTIONS_DIR.mkdir(parents=True, exist_ok=True)
    path = CAPTIONS_DIR / "continuation-part-001.srt"
    blocks = []
    for index, row in enumerate(chunks, start=1):
        blocks.append(
            f"{index}\n{srt_time(row['start'])} --> {srt_time(row['end'])}\n{row['text']}\n"
        )
    path.write_text("\n".join(blocks), encoding="utf-8")
    return path


def selected_images() -> list[dict]:
    shotlist = json.loads((PART / "shotlist" / "shotlist.json").read_text(encoding="utf-8"))
    by_id = {shot["id"]: shot for shot in shotlist["shots"]}
    overrides_path = PART / "image-sequence-overrides.json"
    overrides = json.loads(overrides_path.read_text(encoding="utf-8-sig")) if overrides_path.exists() else {}
    result: list[dict] = []
    for number in range(1, 37):
        shot_id = f"p001-s{number:03d}"
        names = overrides.get(shot_id, [f"{shot_id}.png"])
        for variant_index, name in enumerate(names, start=1):
            source = PART / "images" / name
            if not source.exists():
                raise FileNotFoundError(source)
            result.append(
                {
                    "shot_id": shot_id,
                    "variant": variant_index,
                    "title": by_id.get(shot_id, {}).get("title", shot_id),
                    "beat": by_id.get(shot_id, {}).get("beat", ""),
                    "source": source,
                }
            )
    return result


def copy_media(images: list[dict], total_duration: float) -> list[dict]:
    MEDIA_IMAGES.mkdir(parents=True, exist_ok=True)
    MEDIA_AUDIO.mkdir(parents=True, exist_ok=True)
    VERIFY_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    copied: list[dict] = []
    for index, image in enumerate(images, start=1):
        target_name = f"clip-{index:03d}-{image['shot_id']}-v{image['variant']}.png"
        target = MEDIA_IMAGES / target_name
        shutil.copy2(image["source"], target)
        copied.append({**image, "media": f"media/images/{target_name}"})

    shutil.copy2(PART / "audio" / "narration-full.wav", MEDIA_AUDIO / "narration-full.wav")

    vendor_source = ROOT / "Asset" / "Tears Of Summayah Episode 1 V2" / "video" / "hyperframes" / "vendor" / "gsap.min.js"
    vendor_dir = VIDEO / "vendor"
    vendor_dir.mkdir(parents=True, exist_ok=True)
    if vendor_source.exists():
        shutil.copy2(vendor_source, vendor_dir / "gsap.min.js")

    make_ambient_bed(MEDIA_AUDIO / "ambient-bed.wav", total_duration)
    make_whoosh(MEDIA_AUDIO / "soft-whoosh.wav")
    make_chime(MEDIA_AUDIO / "calabash-chime.wav")
    return copied


def build_visual_timeline(images: list[dict], total_duration: float) -> list[dict]:
    clip_duration = total_duration / len(images)
    rounded_starts = [round(index * clip_duration, 3) for index in range(len(images))]
    rounded_starts.append(round(total_duration, 3))
    rows: list[dict] = []
    for index, image in enumerate(images, start=1):
        start = rounded_starts[index - 1]
        end = rounded_starts[index]
        rows.append(
            {
                "id": f"scene-{index:03d}",
                "shot_id": image["shot_id"],
                "title": image["title"],
                "beat": image["beat"],
                "media": image["media"],
                "start": start,
                "duration": round(max(0.001, end - start), 3),
                "end": end,
            }
        )
    return rows


def short_caption(text: str) -> str:
    cleaned = re.sub(r"\s+", " ", text.strip())
    if len(cleaned) <= 170:
        return cleaned
    words = cleaned.split()
    result: list[str] = []
    count = 0
    for word in words:
        if count + len(word) + 1 > 170:
            break
        result.append(word)
        count += len(word) + 1
    return " ".join(result).rstrip(" ,;:") + "..."


def write_html(visuals: list[dict], chunks: list[dict], total_duration: float) -> None:
    scene_html = []
    for row in visuals:
        scene_html.append(
            f'''      <section class="scene clip" id="{row["id"]}" data-start="{row["start"]}" data-duration="{row["duration"]}" data-track-index="1">
        <div class="scene-frame" data-layout-allow-overflow><img class="scene-image" src="{html.escape(row["media"])}" alt="" /></div>
        <div class="shade"></div><div class="grain"></div><div class="vignette"></div>
      </section>'''
        )

    caption_html = []
    for index, row in enumerate(chunks, start=1):
        caption_html.append(
            f'''      <div class="caption-group clip" id="caption-{index:03d}" data-start="{row["start"]}" data-duration="{row["duration"]}" data-track-index="6" data-layout-allow-occlusion>{html.escape(short_caption(row["text"]))}</div>'''
        )

    transition_html = []
    sfx_html = []
    transition_count = 0
    for index, row in enumerate(visuals[1:], start=2):
        start = max(0.0, row["start"] - 0.42)
        transition_count += 1
        transition_html.append(
            f'''      <div id="transition-{transition_count:03d}" class="transition-wash clip" data-start="{start:.3f}" data-duration="0.72" data-track-index="8"></div>'''
        )
        if transition_count % 2 == 1:
            sfx_html.append(
                f'''    <audio id="sfx-whoosh-{transition_count:03d}" data-start="{start:.3f}" data-duration="0.55" data-track-index="12" src="media/audio/soft-whoosh.wav" data-volume="0.16"></audio>'''
            )

    key_chimes = []
    keywords = ("calabash", "father will die", "special people", "moon")
    for row in chunks:
        text = row["text"].lower()
        if any(word in text for word in keywords):
            key_chimes.append(row["start"])
    for index, start in enumerate(key_chimes[:8], start=1):
        sfx_html.append(
            f'''    <audio id="sfx-chime-{index:03d}" data-start="{start:.3f}" data-duration="1.45" data-track-index="13" src="media/audio/calabash-chime.wav" data-volume="0.12"></audio>'''
        )

    scenes_json = json.dumps(
        [{"id": row["id"], "start": row["start"], "duration": row["duration"]} for row in visuals],
        separators=(",", ":"),
    )
    captions_json = json.dumps(
        [{"id": f"caption-{i:03d}", "start": row["start"], "duration": row["duration"], "text": row["text"]} for i, row in enumerate(chunks, start=1)],
        separators=(",", ":"),
    )

    html_text = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Stolen Innocence Continuation Part 001</title>
    <style>
      html,
      body {{
        width: 100%;
        height: 100%;
        margin: 0;
        background: #050403;
        overflow: hidden;
        font-family: Georgia, "Times New Roman", serif;
      }}

      #root-composition {{
        position: relative;
        width: {WIDTH}px;
        height: {HEIGHT}px;
        overflow: hidden;
        background: #050403;
        color: #fff8ec;
      }}

      .scene {{
        position: absolute;
        inset: 0;
        z-index: 1;
        opacity: 0;
        overflow: hidden;
        background: #050403;
      }}

      .scene-frame,
      .scene-image {{
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
      }}

      .scene-frame {{
        overflow: hidden;
        transform-origin: center center;
      }}

      .scene-image {{
        object-fit: cover;
        transform-origin: center center;
        filter: contrast(1.045) saturate(0.97) brightness(0.93);
      }}

      .shade,
      .grain,
      .vignette,
      .transition-wash,
      .caption-group {{
        position: absolute;
        pointer-events: none;
      }}

      .shade {{
        inset: 0;
        z-index: 2;
        background:
          linear-gradient(180deg, rgba(5, 4, 3, 0.16), rgba(5, 4, 3, 0) 25%, rgba(5, 4, 3, 0.62) 100%),
          radial-gradient(circle at 24% 18%, rgba(227, 175, 86, 0.16), rgba(227, 175, 86, 0) 35%);
        mix-blend-mode: multiply;
      }}

      .grain {{
        inset: 0;
        z-index: 3;
        opacity: 0.13;
        background-image:
          radial-gradient(circle at 15% 25%, rgba(255, 255, 255, 0.14) 0 1px, rgba(255, 255, 255, 0) 1px),
          radial-gradient(circle at 82% 67%, rgba(255, 255, 255, 0.1) 0 1px, rgba(255, 255, 255, 0) 1px);
        background-size: 18px 18px, 23px 23px;
        mix-blend-mode: screen;
      }}

      .vignette {{
        inset: 0;
        z-index: 4;
        background: radial-gradient(ellipse at center, rgba(5, 4, 3, 0) 45%, rgba(5, 4, 3, 0.74) 100%);
      }}

      .caption-group {{
        left: 72px;
        right: 72px;
        bottom: 188px;
        z-index: 40;
        min-height: 106px;
        padding: 30px 36px 34px;
        box-sizing: border-box;
        border-left: 7px solid rgba(232, 179, 92, 0.96);
        background: rgba(8, 7, 6, 0.62);
        color: #fff8ec;
        box-shadow: 0 26px 92px rgba(0, 0, 0, 0.45);
        font-size: 43px;
        line-height: 1.16;
        font-weight: 600;
        text-align: left;
        text-wrap: balance;
        opacity: 0;
      }}

      .transition-wash {{
        inset: 0;
        z-index: 18;
        opacity: 0;
        background:
          linear-gradient(105deg, rgba(5, 4, 3, 0) 0%, rgba(242, 214, 161, 0.72) 45%, rgba(5, 4, 3, 0) 65%),
          radial-gradient(circle at 58% 42%, rgba(110, 29, 29, 0.42), rgba(5, 4, 3, 0.84) 62%);
        filter: blur(4px);
        transform: translateX(-1080px) scale(1.06);
      }}
    </style>
  </head>
  <body>
    <div
      data-composition-id="stolen-innocence-continuation-part-001"
      id="root-composition"
      data-start="0"
      data-width="{WIDTH}"
      data-height="{HEIGHT}"
      data-duration="{total_duration:.3f}"
    >
{chr(10).join(scene_html)}
{chr(10).join(caption_html)}
{chr(10).join(transition_html)}
    </div>

    <audio id="narration" data-start="0" data-duration="{total_duration:.3f}" data-track-index="20" src="media/audio/narration-full.wav" data-volume="1"></audio>
    <audio id="ambient-bed" data-start="0" data-duration="{total_duration:.3f}" data-track-index="21" src="media/audio/ambient-bed.wav" data-volume="0.18"></audio>
{chr(10).join(sfx_html)}

    <script src="vendor/gsap.min.js"></script>
    <script>
      window.__timelines = window.__timelines || {{}};
      var scenes = {scenes_json};
      var captions = {captions_json};
      var tl = gsap.timeline({{ paused: true }});

      scenes.forEach(function (scene, index) {{
        var root = "#" + scene.id;
        var start = scene.start;
        var duration = scene.duration;
        var pan = index % 2 === 0 ? -30 : 30;
        tl.fromTo(root, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.68, ease: "sine.inOut" }}, start);
        tl.fromTo(root + " .scene-frame", {{ opacity: 0, y: 22, scale: 1.012 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.74, ease: "power3.out" }}, start + 0.12);
        tl.fromTo(root + " .scene-image", {{ scale: index % 2 === 0 ? 1.035 : 1.095, x: -pan * 0.4 }}, {{ scale: index % 2 === 0 ? 1.105 : 1.035, x: pan, duration: duration, ease: "sine.inOut" }}, start);
        tl.fromTo(root + " .grain", {{ opacity: 0.09 }}, {{ opacity: 0.16, duration: duration, ease: "sine.inOut" }}, start + 0.3);
        if (index < scenes.length - 1) {{
          tl.to(root, {{ opacity: 0, duration: 0.64, ease: "sine.inOut" }}, scene.start + duration - 0.64);
        }} else {{
          tl.to(root, {{ opacity: 0, duration: 1.15, ease: "power2.in" }}, scene.start + duration - 1.25);
        }}
      }});

      captions.forEach(function (caption, index) {{
        var id = "#" + caption.id;
        var len = caption.text.length;
        var fontSize = len > 155 ? 36 : len > 120 ? 39 : 43;
        tl.set(id, {{ fontSize: fontSize + "px" }}, caption.start);
        tl.fromTo(id, {{ opacity: 0, y: 34, scale: 0.985 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.34, ease: "power3.out" }}, caption.start + 0.08);
        var exitAt = Math.max(caption.start + 0.55, caption.start + caption.duration - 0.18);
        tl.to(id, {{ opacity: 0, y: -12, scale: 0.992, duration: 0.14, ease: "power2.in" }}, exitAt);
        tl.set(id, {{ opacity: 0, visibility: "hidden" }}, caption.start + caption.duration);
      }});

      Array.prototype.forEach.call(document.querySelectorAll(".transition-wash"), function (el) {{
        var start = Number(el.dataset.start);
        var id = "#" + el.id;
        tl.fromTo(id, {{ opacity: 0, x: -1080, scale: 1.04 }}, {{ opacity: 1, x: 0, scale: 1.07, duration: 0.28, ease: "power3.in" }}, start);
        tl.to(id, {{ opacity: 0, x: 1080, scale: 1.02, duration: 0.38, ease: "power2.out" }}, start + 0.3);
      }});

      captions.forEach(function (caption, index) {{
        var el = document.getElementById(caption.id);
        if (!el) return;
        tl.seek(caption.start + caption.duration + 0.01);
        var computed = window.getComputedStyle(el);
        if (computed.opacity !== "0" && computed.visibility !== "hidden") {{
          console.warn("[caption-lint] " + caption.id + " still visible after exit");
        }}
      }});
      tl.seek(0);

      window.__timelines["stolen-innocence-continuation-part-001"] = tl;
    </script>
  </body>
</html>
'''
    VIDEO.mkdir(parents=True, exist_ok=True)
    (VIDEO / "index.html").write_text(html_text, encoding="utf-8")
    (VIDEO / "caption-overrides.json").write_text("{}\n", encoding="utf-8")


def main() -> None:
    manifest = load_audio_manifest()
    srt_path = write_srt(manifest["chunks"])
    images = selected_images()
    copied = copy_media(images, manifest["total_duration"])
    visuals = build_visual_timeline(copied, manifest["total_duration"])
    write_html(visuals, manifest["chunks"], manifest["total_duration"])

    timeline_manifest = {
        "project": "Stolen Innocence",
        "part": "continuation-part-001",
        "status": "hyperframes_ready",
        "width": WIDTH,
        "height": HEIGHT,
        "fps": FPS,
        "duration_seconds": manifest["total_duration"],
        "voice": VOICE,
        "audio_manifest": str(PART / "audio" / "narration-manifest.json"),
        "caption_file": str(srt_path),
        "hyperframes_index": str(VIDEO / "index.html"),
        "visual_clip_count": len(visuals),
        "narration_chunk_count": len(manifest["chunks"]),
        "image_mode": "ComfyUI cinematic stills only; no text baked into images",
        "music_and_sfx": {
            "background": str(MEDIA_AUDIO / "ambient-bed.wav"),
            "transition_sfx": str(MEDIA_AUDIO / "soft-whoosh.wav"),
            "story_chime": str(MEDIA_AUDIO / "calabash-chime.wav"),
        },
        "output_target": str(OUTPUT_DIR / "continuation-part-001.mp4"),
    }
    (PART / "video" / "timeline-manifest.json").write_text(json.dumps(timeline_manifest, indent=2), encoding="utf-8")
    print(json.dumps(timeline_manifest, indent=2))


if __name__ == "__main__":
    main()
