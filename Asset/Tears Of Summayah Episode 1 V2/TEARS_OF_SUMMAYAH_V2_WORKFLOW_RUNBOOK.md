# Tears Of Summayah Episode 1 V2 Workflow Runbook

Generated: 2026-07-06  
Project root: `C:\Social Content`  
Package: `C:\Social Content\asset\Tears Of Summayah Episode 1 V2`  
Final video: `C:\Social Content\asset\Tears Of Summayah Episode 1 V2\output\final.mp4`

## 1. Purpose Of This Document

This document explains the full workflow used to create the V2 story video for `Tears Of Summayah Episode 1`.

It is written as a repeatable, beginner-friendly runbook. Follow it when you want to turn a web story or saved story text into a cinematic vertical social video with:

- preserved original story text
- rewritten first-person story-time script
- production script
- scene beat map
- character bible
- shotlist
- image prompts
- GPT image generation
- narration audio
- cinematic still images
- captions with slide-up and zoom animation
- background music
- timed sound effects
- HyperFrames render
- QA files
- final MP4

The most important idea: do not jump straight from a story to `final.mp4`. The workflow is a controlled pipeline. Each stage creates files that the next stage depends on.

## 2. What This Workflow Does

The workflow turns a story into a picture-and-narration video.

The finished video is a vertical `9:16` social video. It uses generated cinematic still images as the visual layer, a continuous narration track as the main audio layer, animated captions as the text layer, a quiet music bed as the emotional layer, and sound effects as emphasis cues.

For this V2 project, the workflow fixed the main V1 problem: V1 had only 6 image scenes for a 7-minute narration. That made each image hold for too long. V2 rebuilt the story as 37 visual beats so the image changes match the narration, actions, dialogue, reactions, and emotional turns.

## 3. Final Result Summary

Final package:

```text
C:\Social Content\asset\Tears Of Summayah Episode 1 V2
```

Final video:

```text
C:\Social Content\asset\Tears Of Summayah Episode 1 V2\output\final.mp4
```

Final specs:

```text
Resolution: 1080x1920
Aspect ratio: 9:16
Frame rate: 30 fps
Duration: 428.202667 seconds
Duration display: 00:07:08.20
Final size: 203,182,213 bytes
Approx display size: 193.8 MB
Video codec: H.264
Audio codec: AAC stereo, 48 kHz
```

Validation result:

```text
story_video_pipeline.py status: complete
HyperFrames lint: passed, 0 errors, 0 warnings
HyperFrames validate: passed, no console errors, 10 text elements pass WCAG AA
HyperFrames inspect: passed, 0 layout issues across 6 samples
Final render: passed
FFprobe: passed
Visual contact sheet: created and inspected
```

## 4. Important Rules Before You Start

### 4.1 Preserve The Original Story

Always save the full original story before rewriting anything.

For this project:

```text
C:\Social Content\asset\Tears Of Summayah Episode 1 V2\original script\original.txt
```

Never continue from a summary unless the user explicitly asks for a summary video.

### 4.2 Keep Rights Notes

If source rights are unclear, mark the project as private/internal review only.

For this project, the manifest records:

```text
Private internal review only until source rights are cleared.
```

### 4.3 Use The Gatekeeper

The local gatekeeper is:

```text
C:\Social Content\tools\story_video_pipeline.py
```

Use it to check status before and after major work.

### 4.4 Do Not Treat Project Skills As Magic Commands

In this workspace, project skills live as folders and scripts. Do not assume `$skill` commands exist.

Read the folder and run the script directly.

Example skill folder:

```text
C:\Social Content\skills\social-story-video-maker
```

### 4.5 Use GPT Image Generation For This V2 Route

For this V2, the user requested GPT image generation instead of ComfyUI.

That means:

- Build prompts exactly as usual.
- Generate the visual stills with the built-in GPT image route.
- Do not start ComfyUI for image generation on this V2 route.
- Keep canonical generated PNGs in the package `images` folder.

## 5. Folder Contract

Every story version should live in its own package folder.

For this V2:

```text
C:\Social Content\asset\Tears Of Summayah Episode 1 V2
```

The final folder structure was:

```text
asset/Tears Of Summayah Episode 1 V2/
  audio/
    narration-full.wav
    narration-manifest.json
    chunks/
    chunk-text/
  director/
    scene-prompts.json
  edited script/
    edited.txt
    name_map.json
    rewrite_prompt.md
  images/
    v2-s001.png
    ...
    v2-s028.png
    v2-s009b.png
    ...
  original script/
    original.txt
  output/
    final.mp4
    thumbnail.png
    production_manifest.json
  screenwriter/
    production-script.md
  shotlist/
    sentence-shotlist.md
    asset-plan.md
  video/
    hyperframes/
      index.html
      README.md
      vendor/
        gsap.min.js
      media/
        audio/
        images/
        music/
        sfx/
    verify/
      render-contact-sheet.jpg
  character-bible.json
  image-contact-sheet-v2.jpg
  image-prompts.md
  metadata.json
  scene-beats.json
  v2-restart-analysis.md
```

Do not collapse this into only a final MP4. The intermediate files are what make the video debuggable and reusable.

## 6. The High-Level Workflow

The reusable workflow is:

```text
1. Analyze workspace and package
2. Confirm source and rights note
3. Preserve original story text
4. Rewrite story into first-person social narration
5. Build character bible
6. Split script into narration/visual beats
7. Create production script
8. Create shotlist
9. Create image prompt package
10. Generate or reuse narration audio
11. Generate GPT images
12. QA generated images
13. Optimize images for HyperFrames
14. Build HyperFrames timeline
15. Add captions and animation
16. Add background music
17. Add timed sound effects
18. Validate HyperFrames composition
19. Render final MP4
20. Probe final MP4
21. Create thumbnail and contact sheet
22. Write production manifest
23. Run final gatekeeper status
```

## 7. Step 1: Analyze The Workspace

Start in:

```powershell
cd 'C:\Social Content'
```

Read the workspace rules:

```powershell
Get-Content -LiteralPath 'C:\Social Content\AGENTS.md'
```

Important rules from the workspace:

- Use `tools/story_video_pipeline.py` as the strict stage gatekeeper.
- Generated story packages belong under `asset/<Story Name>/`.
- Use PowerShell and explicit Windows paths.
- Preserve source rights notes in `metadata.json`.
- For video/HyperFrames work, verify layout and renderability before final output.

Check the package:

```powershell
Get-ChildItem -LiteralPath 'C:\Social Content\asset\Tears Of Summayah Episode 1 V2' -Force
```

Check pipeline status:

```powershell
& 'C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\python_embeded\python.exe' `
  'C:\Social Content\tools\story_video_pipeline.py' `
  --story-name 'Tears Of Summayah Episode 1 V2' status
```

Expected final result after the full workflow:

```text
state: complete
```

## 8. Step 2: Understand Why V2 Was Needed

V1 was technically complete but structurally weak.

V1 had:

```text
1 narration file
6 narration chunks
6 scene beats
6 generated images
1 HyperFrames composition
1 final MP4
```

The narration was about 428 seconds. Six images across seven minutes meant some images stayed on screen for more than one minute.

That is too slow for a story video because the story includes:

- studying at night
- family-room tension
- father speaking
- mother reacting
- Zahra responding
- shock
- silence
- grief
- final resolve

V2 fixed this by using 37 visual beats.

## 9. Step 3: Preserve Existing Good Assets

Do not throw everything away when restarting as V2.

For this V2, these assets were kept from V1:

```text
original script/original.txt
edited script/edited.txt
edited script/name_map.json
edited script/rewrite_prompt.md
audio/narration-full.wav
audio/narration-manifest.json
audio/chunks/*.wav
audio/chunk-text/*.txt
character-bible.json
```

These assets were rebuilt:

```text
scene-beats.json
screenwriter/production-script.md
shotlist/sentence-shotlist.md
shotlist/asset-plan.md
image-prompts.md
director/scene-prompts.json
images/*.png
video/hyperframes/index.html
output/final.mp4
output/production_manifest.json
```

Beginner rule: keep what is still correct, rebuild what is structurally wrong.

## 10. Step 4: Build The V2 Beat Map

The edited story had 106 sentence-like narration beats. V2 did not make 106 images because that would be heavy for image generation and rendering. Instead, V2 grouped the narration into 37 meaningful visual beats.

Each visual beat includes:

- scene id
- image filename
- sentence range
- start time
- duration
- moment
- setting
- visible characters
- speaker or action
- emotional turn
- transition
- caption
- camera role

Example from `scene-beats.json`:

```text
scene_id: v2-s001
image: images/v2-s001.png
start: 0.0
duration: 5.086
moment: Night is where Zahra believes her dreams are safe.
setting: study room, night
visible_characters: Zahra
caption: I used to believe night was the only place where my dreams were safe.
camera_role: primary angle
```

Create or update:

```text
C:\Social Content\asset\Tears Of Summayah Episode 1 V2\scene-beats.json
```

## 11. Step 5: Conversation Camera Policy

The user specifically requested that conversation scenes should not hold one shot throughout.

So the middle dialogue section uses:

- setup shot
- speaker close-up
- listener reaction close-up
- side angle
- over-the-shoulder angle
- insert shot when the emotion is internal

The V2 package inserted extra dialogue cut-ins such as:

```text
v2-s009b
v2-s010b
v2-s010c
v2-s014b
v2-s016b
v2-s017b
v2-s018b
v2-s020b
v2-s023b
```

These extra scenes make the family-room conversation feel edited like a real scene instead of a slideshow.

Beginner rule: if a character is speaking an important line, consider cutting to that person's close-up. If another character's silent reaction is the emotional point, cut to the listener.

## 12. Step 6: Build Production Script, Shotlist, And Asset Plan

Create:

```text
C:\Social Content\asset\Tears Of Summayah Episode 1 V2\screenwriter\production-script.md
C:\Social Content\asset\Tears Of Summayah Episode 1 V2\shotlist\sentence-shotlist.md
C:\Social Content\asset\Tears Of Summayah Episode 1 V2\shotlist\asset-plan.md
```

These files translate the story into production instructions.

The production script says what the video is about.

The shotlist says what the camera sees.

The asset plan says what must be created.

For each visual beat, the shotlist should decide:

- exact shot size
- exact angle
- visible characters
- who is speaking
- who is listening
- environment
- props
- lighting
- emotional expression
- camera role

Bad shotlist instruction:

```text
Use close-up, over-the-shoulder, or side angle.
```

Good shotlist instruction:

```text
Tight 85mm speaker close-up of Mallam Ibrahim, seated in warm lamplight, eyes fixed slightly off-camera toward Zahra.
```

The image model should not have to choose the shot. You choose the shot before prompting.

## 13. Step 7: Build Image Prompts

Create:

```text
C:\Social Content\asset\Tears Of Summayah Episode 1 V2\image-prompts.md
C:\Social Content\asset\Tears Of Summayah Episode 1 V2\director\scene-prompts.json
```

Each prompt should include:

- scene id
- image filename
- character identity details
- clothing continuity
- setting
- camera angle
- shot size
- lighting
- action
- emotion
- negative prompt

Important image prompt rules:

1. Use one main action per character.
2. Do not bake captions or story text into the image.
3. Only request open mouth if the person is speaking in that exact shot.
4. Keep clothing and character identity consistent.
5. Use close-ups for dialogue emphasis.
6. Use listener reactions where silence carries the emotion.

Negative prompt should include ideas like:

```text
no text, no watermark, no logo, no caption, no distorted hands, no extra limbs, no cartoon, no low-resolution artifacts
```

## 14. Step 8: Generate Images With GPT Image Route

The user requested GPT image generation instead of ComfyUI.

For this run:

- 37 expected V2 images were generated.
- Canonical PNG files were saved in:

```text
C:\Social Content\asset\Tears Of Summayah Episode 1 V2\images
```

The images were:

```text
v2-s001.png
v2-s002.png
...
v2-s028.png
v2-s009b.png
v2-s010b.png
v2-s010c.png
v2-s014b.png
v2-s016b.png
v2-s017b.png
v2-s018b.png
v2-s020b.png
v2-s023b.png
```

The generated originals also remained in the Codex generated-images cache:

```text
C:\Users\DELL\.codex\generated_images\019f2f21-5c65-7ea3-937a-2cc6c08dd40a
```

Beginner rule: the `images` folder in the story package is the canonical folder for the project. The generated-images cache is a backup/history location, not the package output contract.

## 15. Step 9: QA The Images

Create a contact sheet:

```text
C:\Social Content\asset\Tears Of Summayah Episode 1 V2\image-contact-sheet-v2.jpg
```

Check:

- Are all expected images present?
- Do the characters look consistent enough?
- Are dialogue close-ups present?
- Are listener reactions present?
- Are any captions or random text baked into the image?
- Is the framing vertical and usable?
- Are the hands/faces acceptable?
- Does the image match the intended beat?

For this run, the image count check passed:

```text
37 valid PNGs for 37 expected scenes
```

Note from visual QA:

```text
v2-s019 had a medical-looking book or diagram, but no obvious readable baked text. It was accepted.
```

## 16. Step 10: Optimize Images For HyperFrames

The canonical generated images stayed as PNG files under:

```text
C:\Social Content\asset\Tears Of Summayah Episode 1 V2\images
```

For render performance, optimized JPG copies were placed in:

```text
C:\Social Content\asset\Tears Of Summayah Episode 1 V2\video\hyperframes\media\images
```

Why this helps:

- HyperFrames renders faster with smaller media.
- The timeline loads more reliably.
- The original PNGs remain untouched for future regeneration or QA.

Beginner rule: keep master images in `images`, use optimized copies in `video/hyperframes/media/images`.

## 17. Step 11: Build The HyperFrames Project

Create:

```text
C:\Social Content\asset\Tears Of Summayah Episode 1 V2\video\hyperframes\index.html
```

The composition settings were:

```text
Composition id: tears-summayah-episode-1-v2
Width: 1080
Height: 1920
Duration: 428.165 seconds
```

The root composition line looked like:

```html
<div id="root-composition" data-composition-id="tears-summayah-episode-1-v2" data-start="0" data-width="1080" data-height="1920" data-duration="428.165">
```

HyperFrames media layout:

```text
video/hyperframes/
  index.html
  README.md
  vendor/
    gsap.min.js
  media/
    audio/
      narration-full.wav
    images/
      v2-s001.jpg
      ...
    music/
      background-bed.mp3
    sfx/
      page-soft.mp3
      father-call-low.mp3
      room-tension.mp3
      reveal-hit.mp3
      heartbeat-soft.mp3
      door-exit.mp3
      night-grief.mp3
      dawn-resolve.mp3
```

## 18. Step 12: Add Narration Audio

The narration file was:

```text
C:\Social Content\asset\Tears Of Summayah Episode 1 V2\audio\narration-full.wav
```

It was copied into the HyperFrames project:

```text
C:\Social Content\asset\Tears Of Summayah Episode 1 V2\video\hyperframes\media\audio\narration-full.wav
```

In `index.html`, narration was attached as an audio clip:

```html
<audio id="narration" data-start="0" data-duration="428.165" data-track-index="2" src="media/audio/narration-full.wav" data-volume="1"></audio>
```

Beginner rule: narration is the main audio, so it stays at volume `1`. Music and sound effects should be lower so they do not fight the voice.

## 19. Step 13: Add Background Music

A background bed was created and saved as:

```text
C:\Social Content\asset\Tears Of Summayah Episode 1 V2\video\hyperframes\media\music\background-bed.mp3
```

In `index.html`, it was attached like this:

```html
<audio id="music-bed" data-start="0" data-duration="428.165" data-track-index="3" src="media/music/background-bed.mp3" data-volume="0.11"></audio>
```

Why volume `0.11`:

- Narration must stay clear.
- The story tone is emotional, not action-heavy.
- Music should support the mood without becoming distracting.

## 20. Step 14: Add Sound Effects

Eight unique sound effect assets were used:

```text
page-soft.mp3
father-call-low.mp3
room-tension.mp3
reveal-hit.mp3
heartbeat-soft.mp3
door-exit.mp3
night-grief.mp3
dawn-resolve.mp3
```

They were saved in:

```text
C:\Social Content\asset\Tears Of Summayah Episode 1 V2\video\hyperframes\media\sfx
```

The timeline used 11 timed SFX cues:

```text
sfx-01  4.800s    page-soft.mp3        volume 0.18
sfx-02  66.474s   father-call-low.mp3  volume 0.16
sfx-03  101.638s  room-tension.mp3     volume 0.10
sfx-04  167.948s  reveal-hit.mp3       volume 0.18
sfx-05  177.774s  heartbeat-soft.mp3   volume 0.15
sfx-06  227.254s  heartbeat-soft.mp3   volume 0.11
sfx-07  242.067s  reveal-hit.mp3       volume 0.11
sfx-08  309.077s  heartbeat-soft.mp3   volume 0.14
sfx-09  367.854s  door-exit.mp3        volume 0.13
sfx-10  392.706s  night-grief.mp3      volume 0.13
sfx-11  413.614s  dawn-resolve.mp3     volume 0.16
```

Beginner rule: place sound effects on emotional beats, not every scene. Too many effects make the video feel noisy.

## 21. Step 15: Add Caption Styling

The caption block used:

```css
.caption {
  position: absolute;
  left: 64px;
  right: 64px;
  bottom: 104px;
  z-index: 4;
  box-sizing: border-box;
  padding: 24px 30px;
  border-left: 6px solid rgba(232,179,92,.92);
  background: rgba(8,7,6,.58);
  box-shadow: 0 20px 80px rgba(0,0,0,.34);
  font-size: 42px;
  line-height: 1.13;
  font-weight: 600;
  text-wrap: balance;
  opacity: 0;
  visibility: hidden;
  transform-origin: center bottom;
  will-change: transform, opacity;
}
```

The small camera-role label used:

```css
.caption small {
  display: block;
  margin-top: 10px;
  color: #e7c994;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 22px;
  font-weight: 700;
  letter-spacing: 0;
  text-transform: uppercase;
}
```

Beginner rule: captions must be readable on a phone. Do not make them tiny, low-contrast, or too close to the edge.

## 22. Step 16: Add Caption Animation

The user requested:

- zoom in and out
- slide up animation
- animated captions

The implemented caption animation does this:

1. Caption becomes visible.
2. Caption slides up from below.
3. Caption scales from `0.92` to `1.0`.
4. Caption subtly zooms down to `0.985`.
5. Caption zooms back to `1.0`.
6. Caption slides upward and fades out.
7. Caption is hard-hidden after exit.

The GSAP timeline code used:

```js
tl.set(caption, { visibility: "visible" }, start + capIn);
tl.fromTo(
  caption,
  { opacity: 0, y: 46, scale: 0.92 },
  { opacity: 1, y: 0, scale: 1.0, duration: 0.38, ease: "back.out(1.25)" },
  start + capIn
);
tl.to(caption, { scale: 0.985, duration: 0.24, ease: "sine.inOut" }, start + capIn + 0.38);
tl.to(
  caption,
  {
    scale: 1.0,
    duration: Math.min(1.0, Math.max(0.45, duration * 0.16)),
    yoyo: true,
    repeat: 1,
    ease: "sine.inOut"
  },
  start + capIn + 0.78
);
tl.to(caption, { opacity: 0, y: -28, scale: 0.95, duration: 0.18, ease: "power2.in" }, capOut);
tl.set(caption, { opacity: 0, visibility: "hidden" }, capOut + 0.19);
```

Why the hard-hide matters:

HyperFrames seeks the timeline non-linearly during validation and render. Without the final `visibility: "hidden"` set, old captions can sometimes remain visible when they should be gone.

## 23. Step 17: Use Local GSAP

The final HyperFrames file uses:

```html
<script src="vendor/gsap.min.js"></script>
```

The local file is:

```text
C:\Social Content\asset\Tears Of Summayah Episode 1 V2\video\hyperframes\vendor\gsap.min.js
```

Why local GSAP is better:

- The render does not depend on a CDN.
- Network issues are avoided during validation and rendering.
- The composition is more portable.

## 24. Step 18: Validate HyperFrames Before Rendering

Run these from `C:\Social Content`:

```powershell
npx.cmd hyperframes lint 'C:\Social Content\asset\Tears Of Summayah Episode 1 V2\video\hyperframes'
```

Expected result:

```text
0 errors, 0 warnings
```

Then:

```powershell
npx.cmd hyperframes validate 'C:\Social Content\asset\Tears Of Summayah Episode 1 V2\video\hyperframes' --timeout 60000
```

Expected result:

```text
No console errors
Text elements pass WCAG AA
```

Then:

```powershell
npx.cmd hyperframes inspect 'C:\Social Content\asset\Tears Of Summayah Episode 1 V2\video\hyperframes' --samples 6 --timeout 90000
```

Expected result:

```text
0 layout issues across 6 samples
```

Beginner rule: do not render before lint, validate, and inspect are clean. Rendering a 7-minute video can take a long time.

## 25. Step 19: Render The Final MP4

Create the output folder:

```powershell
New-Item -ItemType Directory -Force -Path 'C:\Social Content\asset\Tears Of Summayah Episode 1 V2\output' | Out-Null
```

Render:

```powershell
npx.cmd hyperframes render 'C:\Social Content\asset\Tears Of Summayah Episode 1 V2\video\hyperframes' index.html `
  --output 'C:\Social Content\asset\Tears Of Summayah Episode 1 V2\output\final.mp4' `
  --quality standard `
  --fps 30
```

Important: the render command expects the project directory plus `index.html`.

Correct:

```text
npx.cmd hyperframes render '<hyperframes-folder>' index.html --output '<final.mp4>'
```

Wrong:

```text
npx.cmd hyperframes render '<path-to-index.html-only>'
```

This final render took about:

```text
19 minutes 15.6 seconds
```

## 26. Step 20: Probe The Final MP4

Use FFprobe:

```powershell
& 'C:\Users\DELL\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.2-full_build\bin\ffprobe.exe' `
  -v error `
  -show_entries format=duration,size,bit_rate:stream=index,codec_type,width,height,r_frame_rate,duration `
  -of json `
  'C:\Social Content\asset\Tears Of Summayah Episode 1 V2\output\final.mp4'
```

Result:

```json
{
  "streams": [
    {
      "index": 0,
      "codec_type": "video",
      "width": 1080,
      "height": 1920,
      "r_frame_rate": "30/1",
      "duration": "428.166667"
    },
    {
      "index": 1,
      "codec_type": "audio",
      "r_frame_rate": "0/0",
      "duration": "428.202667"
    }
  ],
  "format": {
    "duration": "428.202667",
    "size": "203182213",
    "bit_rate": "3796000"
  }
}
```

Beginner rule: always probe the final MP4. A file can exist but still have missing audio, wrong dimensions, or wrong duration.

## 27. Step 21: Create Thumbnail And Contact Sheet

Create thumbnail:

```powershell
& 'C:\Users\DELL\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.2-full_build\bin\ffmpeg.exe' `
  -y `
  -ss 00:00:08 `
  -i 'C:\Social Content\asset\Tears Of Summayah Episode 1 V2\output\final.mp4' `
  -frames:v 1 `
  -update 1 `
  'C:\Social Content\asset\Tears Of Summayah Episode 1 V2\output\thumbnail.png'
```

Create render contact sheet:

```powershell
New-Item -ItemType Directory -Force -Path 'C:\Social Content\asset\Tears Of Summayah Episode 1 V2\video\verify' | Out-Null

& 'C:\Users\DELL\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.2-full_build\bin\ffmpeg.exe' `
  -y `
  -i 'C:\Social Content\asset\Tears Of Summayah Episode 1 V2\output\final.mp4' `
  -vf 'fps=1/45,scale=180:320,tile=4x3' `
  -frames:v 1 `
  -update 1 `
  'C:\Social Content\asset\Tears Of Summayah Episode 1 V2\video\verify\render-contact-sheet.jpg'
```

Why `-update 1` is used:

It avoids FFmpeg warnings when writing one image file from an image sequence-style output.

## 28. Step 22: Write Production Manifest

Create:

```text
C:\Social Content\asset\Tears Of Summayah Episode 1 V2\output\production_manifest.json
```

The manifest should record:

- project name
- status
- source URL
- rights note
- version
- reason for restart
- scene count
- conversation camera policy
- image generation route
- audio assets
- caption animation
- validation results
- render specs
- output paths
- limitations

For this project, manifest status is:

```json
{
  "project": "Tears Of Summayah Episode 1 V2",
  "status": "complete"
}
```

## 29. Step 23: Run Final Pipeline Status

After final render and manifest creation, run:

```powershell
& 'C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\python_embeded\python.exe' `
  'C:\Social Content\tools\story_video_pipeline.py' `
  --story-name 'Tears Of Summayah Episode 1 V2' status
```

Final expected result:

```text
state: complete
OK: package
OK: original
OK: name_map
OK: rewrite_prompt
OK: edited
OK: production_script
OK: shotlist
OK: asset_plan
OK: character_bible
OK: scene_beats
OK: image_prompts
OK: scene_prompts
OK: narration_full
OK: narration_manifest
OK: audio_chunks
OK: hyperframes_project
OK: final_mp4
OK: manifest
OK: source_word_count
OK: not_summary_like
OK: image_count
```

For this project:

```text
source_word_count: 2786 words
image_count: 37 valid PNGs for 37 expected scenes
```

## 30. Failures We Hit And How To Avoid Them

### Failure 1: V1 Was Too Compressed

Problem:

```text
The first completed version used only 6 visual scenes for a 7-minute narration.
```

Why that was bad:

```text
Each image stayed on screen too long, so dialogue and emotional turns had no visual coverage.
```

Fix:

```text
Restart as V2, preserve useful assets, rebuild scene-beats, shotlist, prompts, images, and HyperFrames timeline with 37 visual beats.
```

Avoid next time:

```text
Before generating images, compare narration duration to scene count. If each still image must hold more than about 10 to 20 seconds during dialogue-heavy story material, the scene map is probably too compressed.
```

### Failure 2: Conversation Scenes Held Too Much In One Shot

Problem:

```text
Dialogue scenes can feel flat if the camera stays on one wide shot.
```

Fix:

```text
Add speaker close-ups, listener reaction close-ups, and alternate angles inside the conversation.
```

Avoid next time:

```text
For every conversation, mark which line needs a speaker close-up and which silence needs a listener reaction.
```

### Failure 3: Wrong HyperFrames Skill Path

Problem:

This path was tried first:

```text
C:\Users\DELL\.codex\skills\master\hyperframes\SKILL.md
```

It failed because the file did not exist.

Fix:

Use the actual skill path:

```text
C:\Users\DELL\.agents\skills\master\hyperframes\SKILL.md
```

Avoid next time:

```powershell
Get-ChildItem -LiteralPath 'C:\Users\DELL\.agents\skills\master\hyperframes' -Force
```

Then read the actual `SKILL.md`.

### Failure 4: Render Failed With NPM EACCES / Network Cache Issue

Problem:

The first render attempt failed with:

```text
npm error code EACCES
npm error FetchError: request to https://registry.npmjs.org/hyperframes failed
npm error The operation was rejected by your operating system.
npm error Log files were not written due to an error writing to C:\Users\DELL\AppData\Local\npm-cache\_logs
```

Cause:

```text
The sandboxed run could not access npm cache/network resources correctly.
```

Fix:

Rerun the same render command with approved elevated access.

The successful command was:

```powershell
npx.cmd hyperframes render 'C:\Social Content\asset\Tears Of Summayah Episode 1 V2\video\hyperframes' index.html `
  --output 'C:\Social Content\asset\Tears Of Summayah Episode 1 V2\output\final.mp4' `
  --quality standard `
  --fps 30
```

Avoid next time:

```text
If lint/validate/inspect pass but render fails with npm EACCES or registry/cache errors, treat it as an environment permission issue. Rerun render with approved access instead of changing the composition.
```

### Failure 5: Broad Searches Can Return Too Much Text

Problem:

Broad documentation or memory searches can dump too much output.

Fix:

Use narrow commands and exact paths.

Better:

```powershell
Select-String -LiteralPath '<file>' -Pattern 'caption|sfx|background-bed' -Context 1,2
```

Worse:

```powershell
Get-Content '<large file>'
```

Avoid next time:

```text
Search for exact terms when you only need implementation details.
```

### Failure 6: Rendering Is Slow

Problem:

The final render took about 19 minutes.

Why:

```text
The project is 7 minutes long, 1080x1920, 30 fps, with 37 images, captions, music, and SFX.
```

Fix:

Do not restart if it is progressing. Wait for it to finish.

Avoid next time:

```text
Run lint, validate, and inspect first. Rendering should be the final expensive step, not the debugging step.
```

## 31. Quick Copy-Paste Checklist For Next Story

Use this section when running the next project.

### 31.1 Start

```powershell
cd 'C:\Social Content'
Get-Content -LiteralPath 'C:\Social Content\AGENTS.md'
& 'C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\python_embeded\python.exe' 'C:\Social Content\tools\story_video_pipeline.py' doctor
```

### 31.2 Create Or Check Package

```powershell
$story = 'Your Story Name V2'
Get-ChildItem -LiteralPath "C:\Social Content\asset\$story" -Force
& 'C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\python_embeded\python.exe' 'C:\Social Content\tools\story_video_pipeline.py' --story-name $story status
```

### 31.3 Required Files Before Images

Check that these exist:

```text
original script/original.txt
edited script/edited.txt
edited script/name_map.json
edited script/rewrite_prompt.md
character-bible.json
scene-beats.json
screenwriter/production-script.md
shotlist/sentence-shotlist.md
shotlist/asset-plan.md
image-prompts.md
director/scene-prompts.json
audio/narration-full.wav
audio/narration-manifest.json
```

### 31.4 Image QA

```powershell
(Get-ChildItem -LiteralPath "C:\Social Content\asset\$story\images" -Filter '*.png').Count
```

Expected:

```text
Count must match expected scene count.
```

### 31.5 HyperFrames Checks

```powershell
npx.cmd hyperframes lint "C:\Social Content\asset\$story\video\hyperframes"
npx.cmd hyperframes validate "C:\Social Content\asset\$story\video\hyperframes" --timeout 60000
npx.cmd hyperframes inspect "C:\Social Content\asset\$story\video\hyperframes" --samples 6 --timeout 90000
```

### 31.6 Render

```powershell
New-Item -ItemType Directory -Force -Path "C:\Social Content\asset\$story\output" | Out-Null
npx.cmd hyperframes render "C:\Social Content\asset\$story\video\hyperframes" index.html --output "C:\Social Content\asset\$story\output\final.mp4" --quality standard --fps 30
```

### 31.7 Final Status

```powershell
& 'C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\python_embeded\python.exe' 'C:\Social Content\tools\story_video_pipeline.py' --story-name $story status
```

Expected:

```text
state: complete
```

## 32. What To Improve Next Time

1. Create a small script to generate the V2 beat map from narration manifest plus manual camera-role edits.
2. Create a reusable HyperFrames template for story videos with built-in caption animation, music bed, and SFX tracks.
3. Store SFX cue rules in JSON instead of hardcoding them in HTML.
4. Add a preview step before full render if the user wants timeline review.
5. Add automatic contact sheet creation after every image batch.
6. Add a `gpt-images` stage name to the gatekeeper so GPT image workflows do not appear under old ComfyUI wording.
7. Keep source rights status visible in both `metadata.json` and `production_manifest.json`.

## 33. Exact Output Files From This Run

Final video:

```text
C:\Social Content\asset\Tears Of Summayah Episode 1 V2\output\final.mp4
```

Thumbnail:

```text
C:\Social Content\asset\Tears Of Summayah Episode 1 V2\output\thumbnail.png
```

Render contact sheet:

```text
C:\Social Content\asset\Tears Of Summayah Episode 1 V2\video\verify\render-contact-sheet.jpg
```

Production manifest:

```text
C:\Social Content\asset\Tears Of Summayah Episode 1 V2\output\production_manifest.json
```

This runbook:

```text
C:\Social Content\asset\Tears Of Summayah Episode 1 V2\TEARS_OF_SUMMAYAH_V2_WORKFLOW_RUNBOOK.md
```
