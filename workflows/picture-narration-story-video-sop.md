# SOP: Picture Narration Story Video

## Purpose

Use this workflow to create social media videos for YouTube, Facebook, TikTok, Shorts, Reels, and similar platforms when the format is still images plus narrated voice-over, with cinematic story scenes, synced SFX, background music, transitions, and a final rendered video.

This is the canonical WAT route for story-derived picture narration videos in `C:\Social Content`.

For the full dummy-proof operating manual, including the verbatim scraping rule, Eve v2 ComfyUI failures/fixes, Chatterbox TTS chunking, HyperFrames render commands, QA checks, and final handoff format, read:

```text
C:\Social Content\skills\social-story-video-maker\SOP.md
```

Before using this workflow on a sentence-level story video, read the `Stolen Innocence 2026-07-05 Execution Addendum` in that SOP. It contains the current strict rules for verbatim scraping, long-form rewrites, shotlist decisions, one-action prompts, speaking-mouth handling, multi-character blocking, ComfyUI Krea2 workflow selection, GPU verification, and mandatory image QA/regeneration.

## WAT Roles

- **Workflow:** this SOP defines the production sequence and output contract.
- **Agent:** coordinate decisions, inspect each stage output, preserve continuity, and recover from errors.
- **Tools:** use local project skills and scripts for scraping, packaging, TTS, image generation, timeline assembly, and rendering.

## Required Inputs

- Source story URL, discovery request, or user-provided story text.
- Rights status: owned, licensed, public domain, permission granted, or private internal review only.
- Target platform and aspect ratio. Default to vertical `9:16` for TikTok, Reels, Shorts, and Facebook short-form.
- Desired length, narrator voice, niche, language, and tone when supplied.

If rights are unclear, scrape only allowed metadata or ask for authorized text. Do not create a public adaptation from unauthorized verbatim story text.

## Canonical Production Sequence

### 1. Source And Scrape

Use `skills/webscraper/SKILL.md`.

1. Read source rules when the source, rights, or eligibility are unclear.
2. Scrape or discover stories with `skills/webscraper/scripts/web_scraper.py`.
3. Capture the exact story word-for-word. Do not scrape only a summary when the requested asset is the story.
4. If the full story is too long for one scrape or one file, split it into ordered verbatim sections and save every section.
5. Save story material under `stories/<Story Name>/`.
6. Preserve `metadata.json` and the source URL.
7. Confirm the story can be adapted before rewriting or rendering a publishable video.

Expected outputs:

```text
stories/<Story Name>/story.txt
stories/<Story Name>/metadata.json
```

### 2. Rewrite Into First-Person Story Time

Use `skills/story-time-rewriter/SKILL.md`.

1. Change every character name.
2. Preserve the full plot closely.
3. Rewrite in first-person POV from the protagonist's perspective.
4. Use voice-over narration for events the protagonist did not witness.
5. Keep one continuous narrator voice unless the user explicitly asks for character dialogue voices.
6. Track all name changes in `name_map.json`.

Required package:

```text
asset/<Story Name>/
  original script/original.txt
  edited script/edited.txt
  edited script/name_map.json
  edited script/rewrite_prompt.md
```

### 3. Split Narration Into Audio Chunks

Use `skills/chatterbox-tts/SKILL.md`.

1. Split `edited.txt` into scene-safe narration chunks. Keep each chunk short enough for clean TTS retry and timeline syncing.
2. Keep emotional tags only when they improve delivery, such as `[sigh]` for grief or `[chuckle]` for nervous laughter.
3. Generate WAV narration with Chatterbox TTS.
4. Save audio in the story package, not a shared loose folder.

Recommended layout:

```text
asset/<Story Name>/audio/
  narration-001.wav
  narration-002.wav
  narration-manifest.json
```

The manifest should track chunk id, source text, voice, file path, duration, and retry notes.

### 4. Build Scene Beats

Convert narration chunks into scene beats before writing image prompts.

Each beat should include:

- `scene_id`
- narration chunk id
- exact story moment
- visible characters
- speaker or narrated action
- emotional turn
- setting and time of day
- image count needed
- transition idea
- SFX or music cue

When a sentence says someone is talking, make the image show the relationship physically. Example: if the narration says Wendy sadly told David she hated him, the scene can show Wendy facing David, David facing Wendy, or an over-the-shoulder/back-view composition that makes their eyelines and emotional distance clear.

### 5. Direct Cinematic Image Prompts

Use `skills/film-director/SKILL.md` as the directing layer. Use `skills/cinematic-image-prompt-director` only when a pure still-image prompt pass is needed.

For each scene, write detailed image prompts that include:

- Character identity lock: age range, body type, face shape, hair, complexion, scars, freckles, facial asymmetry, skin pores, under-eye texture, expression lines, and other realistic imperfections.
- Costume lock: exact clothing color, garment type, fabric texture, fit, footwear, accessories, and condition. Preserve it across the entire story unless the plot changes it.
- Performance direction: brow, eyes, mouth, jaw, neck, shoulders, hands, posture, breathing, and restraint.
- Blocking: who is foreground, midground, background, left/right/center, eyeline, body orientation, and distance.
- Camera: shot size, lens feel, angle, depth of field, camera height, composition, and focal subject.
- Lighting: motivated light source, contrast, color temperature, shadows, practical lights, and time of day.
- Environment: location, weather, props, surfaces, background action, and readable context.
- Texture: realistic skin texture, pores, fabric weave, dust, sweat, tears, scars, imperfect hair, and natural lens artifacts.
- Continuity constraints: repeated character, costume, location, prop, and mood locks.

Do not use generic emotions alone. Replace "sad" with visible acting behavior such as wet lower eyelids, tense lips, lowered chin, shallow breathing, and shoulders held still to avoid crying.

### 6. Generate Images

Use `skills/comfyui-media-generator/SKILL.md`.

1. Start or verify portable ComfyUI before submitting jobs.
2. Submit prompt-ready API workflows with `skills/comfyui-media-generator/scripts/comfyui_api.py` when possible.
3. Save final images inside the story package and copy reusable finals to `Asset/images` when useful.
4. Keep the workflow JSON used for successful generation.

Recommended layout:

```text
asset/<Story Name>/images/
  scene-001-a.png
  scene-001-b.png
  scene-002-a.png
asset/<Story Name>/comfyui-workflows/
  scene-001-workflow.json
```

Reject images that break character identity, clothing color, eyeline, scene geography, hands, face quality, or story emotion.

### 7. Compose Editable Video

Use `skills/hyperframes/SKILL.md` for the previewable timeline and `skills/video-use/SKILL.md` for final assembly or transcript-aware editing.

1. Build an editable HyperFrames project with all images, narration chunks, captions, transitions, SFX, and music as separate assets.
2. Set scene duration from narration audio duration first.
3. Use subtle image motion: slow push, parallax, pan, rack-focus simulation, or still hold when emotion needs silence.
4. Add captions when appropriate for the platform.
5. Keep preview editable before final render.

Recommended layout:

```text
asset/<Story Name>/video/
  hyperframes/
  timeline/
  captions/
  sfx/
  music/
  renders/
```

### 8. Add And Sync SFX, Music, And Transitions

1. Add SFX only where they support story comprehension or emotion.
2. Keep background music under narration and duck it during dialogue-heavy sections.
3. Match transitions to story rhythm: cuts for tension, dissolves for memory, push/slide for location change, hard black for shock.
4. Verify SFX does not obscure words.
5. Keep all source audio files editable in the package.

### 9. Render Final Output

1. Run HyperFrames lint/validate where applicable.
2. Preview the timeline before final render whenever practical.
3. Render the approved final video.
4. Save final outputs under:

```text
asset/<Story Name>/output/
  final.mp4
  final_with_captions.mp4
  thumbnail.png
  production_manifest.json
```

The production manifest should include source story, rights note, rewritten script path, TTS voice, image workflow paths, final render path, platform, aspect ratio, and date.

## Quality Gate

Before calling the video complete, verify:

- Rights status is recorded.
- Character names are changed and `name_map.json` exists.
- Narration is first-person protagonist POV.
- Every major scene has a cinematic image prompt and at least one generated image.
- Character clothing and identity remain consistent.
- Images show who is talking or reacting when dialogue is narrated.
- Audio chunks line up with scenes.
- SFX and music are synced and not too loud.
- The HyperFrames timeline remains editable.
- Final render is saved in `asset/<Story Name>/output/`.

## Failure Handling

- If scraping fails, inspect the error and source rules. Ask for pasted or authorized text when access or rights block scraping.
- If TTS fails, retry only the failed chunk and update the manifest.
- If ComfyUI fails, preserve the prompt and workflow JSON, inspect logs, fix the workflow, and regenerate only affected images.
- If continuity breaks, update the character bible and regenerate the affected scene images.
- If render fails, validate the HyperFrames project directory and asset paths before changing creative assets.
