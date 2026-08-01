---
name: social-story-video-maker
description: Orchestrate WAT-style social media story videos made from still images plus narration. Use when creating YouTube, Facebook, TikTok, Shorts, or Reels content from web stories or supplied stories, including scraping, first-person story-time rewriting, Chatterbox TTS narration, cinematic image prompt direction, ComfyUI image generation, HyperFrames timeline composition, SFX/music syncing, and final video rendering.
---

# Social Story Video Maker

Read `SOP.md` before using this skill independently. Start with its "Golden Route: Strict Local Pipeline" section. It defines the complete picture narration workflow, asset package, verbatim scraping rule, ComfyUI persistence rule, Chatterbox TTS process, HyperFrames render process, QA checks, and failure handling.

Use this as the orchestration layer for picture-based narration videos. Follow the WAT framework: read the workflow, coordinate the local project skills, and rely on deterministic scripts for execution. Project skills are folders under `C:\Social Content\skills`; do not invoke `$social-story-video-maker` or `$webscraper` unless the current runtime explicitly exposes those names.

## Required Workflow

Read `../../workflows/picture-narration-story-video-sop.md` before starting production or changing the process.

Read `references/output-contract.md` when checking whether a package is complete.

## Route

Use the local project skills in this order:

1. `skills/webscraper` for source discovery, scraping, metadata, and rights-aware story capture.
2. `skills/story-time-rewriter` for first-person protagonist POV, changed names, and the required `asset/<Story Name>/` script package.
3. `skills/chatterbox-tts` for narration chunk audio and voice manifests.
4. `skills/film-director` for cinematic scene blocking, acting, camera, lighting, and prompt continuity.
5. `skills/comfyui-media-generator` for generated still images through portable ComfyUI.
6. `skills/hyperframes` for editable timeline, image motion, captions, transitions, SFX, and music.
7. `skills/video-use` for final assembly, audio/video finishing, and render support when needed.

Use `C:\Social Content\tools\story_video_pipeline.py` for `doctor`, `plan`, `status`, `run-stage`, and `run-all`. The runner is the stage gatekeeper and must stop production when required artifacts are missing.

`screenwriter` and `shotlist-builder` are external/global Codex skills. If unavailable, create their required local artifacts manually before continuing: `screenwriter/production-script.md`, `shotlist/sentence-shotlist.md`, and `shotlist/asset-plan.md`.

## Operating Rules

- Confirm rights before creating publishable adaptations from scraped text.
- When scraping a story, capture the exact story word-for-word. Never continue from only a summary unless the user explicitly asks for a summary workflow.
- If the full story is too long, split it into ordered verbatim section files and then combine them into `original script/original.txt`.
- Keep the story package editable until final approval.
- Preserve the exact story-time rewriter folder contract.
- Maintain a character bible before image generation: names, replacement names, facial details, clothing, props, and continuity changes.
- Make every prompt scene-specific and cinematic. Include facial imperfections, skin pores, realistic textures, exact clothing color/style, blocking, performance, camera, lighting, and continuity locks.
- When narration mentions someone speaking, make the image show the speaker/listener relationship through eyeline, body orientation, distance, or over-the-shoulder/back-view composition.
- Save final renders to `asset/<Story Name>/output/`.
- Start ComfyUI once, health-check the API server, and submit image workflows to the persistent server. Restart only when the server is dead, unresponsive, out of VRAM, or corrupted by a failed workflow.

## Handoff Artifacts

At minimum, produce or preserve:

- `metadata.json`
- `original script/original.txt`
- `edited script/edited.txt`
- `edited script/name_map.json`
- `audio/narration-manifest.json`
- `scene-beats.json`
- `character-bible.json`
- `image-prompts.md`
- `video/hyperframes/`
- `output/final.mp4`
- `output/production_manifest.json`
