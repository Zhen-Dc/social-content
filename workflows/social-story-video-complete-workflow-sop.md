# Social Story Video Complete Workflow SOP

Last updated: 2026-07-06

This document explains the complete workflow for turning an online story into a long-form vertical picture-and-narration story video using local tools in `C:\Social Content`.

It is written so a weak or inexperienced model can follow it without improvising the important parts.

## Purpose

The purpose of this workflow is to create a social story video from a web story while preserving the story's engagement, dialogue, emotional beats, character consistency, image quality, narration quality, captions, SFX, music, transitions, and final render quality.

The final video should be a 9:16 vertical story video where:

- The story is rewritten into first-person narration.
- Character names are changed.
- The script keeps dialogue and interactions instead of becoming a short summary.
- Each sentence or small story beat has its own image or image clip.
- Images are generated with ComfyUI.
- Voiceover is generated with Chatterbox TTS.
- The narrator voice matches the narrator identity.
- Captions are the only text shown on the video.
- No generated image contains baked-in text, captions, logos, title cards, watermarks, or typography.
- The video is assembled in HyperFrames with synced narration, captions, transitions, SFX, and background music or ambience.
- A QA pass is performed on generated images and the rendered video before delivery.

## Core Rule

Do not skip stages.

The required order is:

1. Scrape the exact story from the website.
2. Save the exact story word-for-word.
3. Rewrite the story with changed names and first-person narration.
4. Pass the rewrite through the screenwriter stage.
5. Pass the production script through the shotlist builder.
6. Pass the shotlist into the film director prompt stage.
7. Generate images with ComfyUI.
8. QA all images.
9. Regenerate failed images.
10. Generate TTS audio with Chatterbox.
11. Build HyperFrames video with captions, SFX, music, and transitions.
12. Render final output.
13. QA the rendered video.
14. Save manifests and final outputs.

If a story is long, do not summarize it. Split it into sections and process the sections one by one.

## Workspace Contract

Root workspace:

```text
C:\Social Content
```

Generated story packages belong under:

```text
C:\Social Content\Asset\<Story Name>
```

Scraped story packages belong under:

```text
C:\Social Content\stories\<Story Name>
```

Workflow SOPs belong under:

```text
C:\Social Content\workflows
```

Reusable skills belong under:

```text
C:\Social Content\skills\<skill-name>
```

Deterministic helper scripts belong under:

```text
C:\Social Content\tools
```

## Required Skills And Tools

Use these local capabilities in this order:

- `webscraper`: scrape the exact story text from the website.
- `story-time-rewriter`: rewrite the story into first-person narration with changed names.
- `screenwriter`: make the rewritten story production-ready.
- `shotlist-builder`: convert the production script into cinematic shot decisions.
- `film director`: turn shotlist items into direct, detailed image prompts.
- `comfy ui media generator`: generate images through ComfyUI API.
- `chatterbox-tts`: generate voiceover audio.
- `hyperframes` and `video-use`: assemble, caption, animate, add audio, render, and verify the video.

Do not replace ComfyUI image generation with static text cards.

## Story Scraping Rules

The scraper must capture the exact story word-for-word.

Do:

- Save the original story text before rewriting.
- Preserve dialogue and scene interactions.
- Preserve the sequence of events.
- If the story is too long, split it into sections such as `section-001`, `section-002`, and so on.
- Keep metadata showing where the story came from.
- Preserve rights notes in `metadata.json`.

Do not:

- Scrape only a summary.
- Rewrite before saving the source.
- Collapse long scenes into one short paragraph.
- Remove dialogue just because it is long.

Example scraper command:

```powershell
& "C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\python_embeded\python.exe" `
  ".\skills\webscraper\scripts\web_scraper.py" `
  --url "https://www.ebonystory.com/story/stolen-innocence/episode-1" `
  --output-root ".\stories" `
  --make-script
```

If the scraper cannot capture the full text, stop and ask for pasted or authorized source text.

## Rewrite Rules

The rewrite must:

- Change character names.
- Convert the story into first-person narration.
- Make the protagonist the narrator.
- Keep dialogue and interactions.
- Keep emotional beats.
- Keep the story long and engaging.
- Preserve the original event order.
- Avoid summary-style compression.

Narrator identity must be identified before voice generation.

Narrator categories:

- Little girl
- Little boy
- Young woman
- Young man
- Middle aged woman
- Middle aged man
- Old woman
- Old man

For Stolen Innocence continuation, the narrator was:

```text
Young woman first-person Amara, recalling childhood events.
```

So the TTS voice was a young woman voice.

## Screenwriter Stage

Before any generation, pass the rewritten story through the screenwriter stage.

The screenwriter output should produce a production-ready script with:

- Clear narration paragraphs.
- Dialogue preserved.
- Scene flow preserved.
- Emotional pacing improved.
- No missing interactions.
- No summary-only sections.

For the Stolen Innocence continuation, the production script was saved here:

```text
C:\Social Content\Asset\Stolen Innocence\continuation-part-001\screenwriter\production-script.md
```

## Shotlist Builder Stage

After the screenwriter stage, pass the script to the shotlist builder.

The shotlist builder must decide:

- Exact shot type.
- Camera angle.
- Character blocking.
- Who is visible.
- What each visible character is doing.
- Whether the shot is single-character, two-character, or group.
- Whether a speaker's mouth should be open.
- Lighting source.
- Environment.
- Props.
- Continuity locks.

The image prompt generator must not be asked to choose between shot types.

Bad prompt pattern:

```text
Use the specified over-the-shoulder, facing-each-other, side-by-side, or close-up reaction composition.
```

Good prompt pattern:

```text
Use a tight 85mm over-the-shoulder shot from behind Amara's left shoulder, with Elder Okoro facing her across the fence.
```

The shotlist must choose one composition, not list options.

For the Stolen Innocence continuation, the shotlist was saved here:

```text
C:\Social Content\Asset\Stolen Innocence\continuation-part-001\shotlist\shotlist.json
```

## Image Prompt Rules

Every image prompt must be direct, detailed, and exact.

Each prompt must include:

- Shot ID.
- Story beat.
- Exact camera angle.
- Exact shot type.
- Exact number of visible characters.
- Character locks.
- Clothing locks.
- Hair locks.
- Prop locks.
- Lighting source.
- Time of day.
- Facial expression.
- Body pose.
- One action per visible character.
- No text anywhere in the image.
- Negative prompt.

Do not put multiple actions for one character in one prompt.

Bad:

```text
Amara wakes up, sees the dog eating her food, runs toward it, grabs a stick, and chases it.
```

Good split:

```text
Shot A: Somto sneaks out through the doorway while Amara sleeps.
Shot B: Amara wakes on her mat, confused and hungry.
Shot C: Koko is the main focus, eating from the bowl while Amara is absent.
Shot D: Amara runs toward Koko with panic on her face and both hands stretched forward.
Shot E: Amara chases Koko with a stick as the dog runs away from the already eaten food.
```

## Multi-Character Prompt Rules

One visible character:

- Show that character in the middle of one action.
- Do not make them stare plainly into the camera unless the shot requires it.

Two visible characters:

- Choose exactly one composition:
  - Over-the-shoulder shot.
  - Facing-each-other shot.
  - Side-by-side shot.
  - Close-up reaction shot with the other character partially visible.
- Do not tell the model to decide.

More than two visible characters:

- Avoid flat group portraits.
- Use over-the-shoulder from one character looking at the others.
- Or use over-the-shoulder from the group looking at one character.
- Or use a close-up of one character with the others blurred behind them.
- Or show the group as background silhouettes if the scene needs atmosphere.

## Speaking Mouth Rule

Only make a character's mouth open when that character is speaking in that exact shot.

Do not force open mouth for silent listeners.

If a character is speaking, the prompt should say:

```text
The speaking character's lips are visibly separated, dark mouth interior visible, cheeks tense mid-sentence.
```

If a character is not speaking, describe their listening expression instead.

## Character Continuity Rules

Character details must stay consistent across the whole story.

Example Stolen Innocence locks:

Amara:

```text
Nigerian girl age 12, slim, warm dark-brown skin, visible pores, faint chicken-pox marks, almond dark-brown eyes, full lips, natural black cornrow braids falling back from forehead and down shoulders, faded mustard-yellow cotton dress, no low cut, no short hair.
```

Somto:

```text
Nigerian teenage cousin around 14, youthful round face, warm brown skin, tiny acne marks, neat black braids, green patterned blouse with yellow leaf motifs, dark wrapper, not adult, not tall.
```

Elder Okoro:

```text
Elderly Nigerian man late 60s, thin angular face, deep forehead lines, grey stubble, sunken cheeks, clouded brown eyes, rough weathered dark-brown skin, faded off-white short-sleeve shirt, loose brown trousers, worn leather sandals.
```

Calabash:

```text
Small tan dried gourd, honey-brown mottled matte surface, rounded lower belly, smaller upper bulb, short narrow neck, subtle dark speckles and scratches, faded red cotton thread around the waist.
```

Never let Amara switch from braids to low cut hair.

Never let Somto become an adult woman or become too tall.

Never let the calabash change shape every time it appears.

## Lighting Rules

The prompt must specify the real light source.

If a girl is holding a lamp, the lamp must be the only light source.

Bad:

```text
She holds a lamp in a brightly lit room with soft studio fill.
```

Good:

```text
The kerosene lamp in her right hand is the only light source; warm light falls upward across her cheeks and hands while the room behind her falls into darkness.
```

Night scenes must look like night.

For "That night," use a night sky, moon, dim village light, or darkness. Do not turn it into daytime.

## Important Scene Splitting Examples

Dog food scene:

Original beat:

```text
Somto slipped out to meet her friends, and when hunger woke me, I found our dog Koko eating the food she had left for me.
```

Correct split:

1. Somto sneaks out.
2. Amara wakes up hungry.
3. Koko is the main focus eating the food while Amara is absent.
4. Amara runs toward Koko in panic or chases Koko away.

Gathering scene:

Original beat:

```text
That night, I found myself in a terrifying gathering of people dressed in black, and Elder Okoro told me I now belonged among special people.
```

Correct split:

1. Night sky with moon.
2. Amara in the middle of the night gathering.
3. Side profile close-up of Elder Okoro speaking to Amara.

Calabash instruction scene:

Original beat:

```text
He gave me a calabash in that dream and told me to hide it under my parents' bamboo bed if I wanted my father to become rich.
```

Correct split:

1. Low-angle first-person POV shot of Elder Okoro handing the calabash toward the camera.
2. Elder gives the instruction.
3. Amara reacts with fear and hope.

Under-bed scene:

Original beat:

```text
When I woke up and saw the same calabash beside my bed, fear and hope confused me, so I obeyed.
```

Correct shot:

```text
Shot from under the bamboo bed. The calabash is in view under the bed, while Amara looks under the bed in shock.
```

## ComfyUI Image Generation

ComfyUI must be used for story images.

Do not use text cards as a substitute.

Recommended ComfyUI server:

```text
http://127.0.0.1:8190
```

Safe launcher used during Stolen Innocence:

```text
C:\Social Content\tools\run_comfyui_8190_safe.cmd
```

Safe launcher mode:

```text
--windows-standalone-build --disable-cuda-malloc --listen 127.0.0.1 --port 8190
```

ComfyUI should remain running while generating multiple images.

Do not restart ComfyUI for every single image. Restart only when:

- The API is dead.
- The queue is stuck.
- GPU memory is unrecoverable.
- ComfyUI crashes.
- The model is in a bad state after repeated failures.

Check API health:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8190/system_stats"
```

Check queue:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8190/queue"
```

Check ComfyUI process:

```powershell
Get-CimInstance Win32_Process |
  Where-Object { $_.Name -eq 'python.exe' -or $_.Name -eq 'cmd.exe' } |
  Select-Object ProcessId,ParentProcessId,Name,CommandLine
```

If image generation helper scripts are stuck, stop only the helper process. Do not kill ComfyUI unless ComfyUI itself is the problem.

## GPU Confirmation

Do not assume GPU usage just because Task Manager shows GPU activity. Other apps may be using the GPU.

Confirm ComfyUI itself is using the GPU by checking:

- ComfyUI API `/system_stats`.
- ComfyUI process command line.
- NVIDIA process list if available.
- Logs showing `cuda:0`.

During Stolen Innocence, ComfyUI reported:

```text
cuda:0 Quadro P5200 : native
```

For the final HyperFrames render, Chrome reported Intel UHD Graphics 630, which is separate from ComfyUI image generation.

## Workflow Selection Notes

The user-provided Krea workflow was:

```text
C:\Users\DELL\Downloads\image_krea2_turbo_t2i (1).json
```

It was tested against the previous workflow.

Important result:

- Default Krea workflow was used as a base.
- 1080x1920 at 28 steps was slower.
- Portrait 9:16 was required.
- The working story generation used custom per-shot workflow copies based on the Krea workflow.
- Common working settings were around `720x1280`, 9:16, about 8 steps for speed, then regenerating failed shots as needed.

Do not blindly force 1080x1920 for all image generations if it makes production too slow. Use a practical resolution for batch generation, then increase quality selectively when needed.

## Image QA Rules

Every generated image must be QA checked before video assembly.

Reject images with:

- Stacked frames.
- Split screen.
- Multi-panel layout.
- Contact sheet look.
- Text, captions, logos, or watermarks inside the image.
- Wrong character hair.
- Wrong clothing.
- Wrong age.
- Bad anatomy.
- Short or deformed legs.
- Deformed hands.
- Duplicate character.
- Extra people.
- Wrong prop.
- Calabash shape inconsistency.
- Wrong lighting.
- Daytime instead of night.
- Characters staring plainly at the camera when the scene needs action.
- Wrong character placement.

For contact sheets, create QA sheets showing many images at once.

Example Stolen Innocence QA output:

```text
C:\Social Content\Asset\Stolen Innocence\continuation-part-001\qa\qa-contact-013-036-final-pass.jpg
```

Rejected images should be archived, not silently overwritten.

Example rejected archive:

```text
C:\Social Content\Asset\Stolen Innocence\continuation-part-001\qa\rejected-before-regen
```

## Stolen Innocence Image Failures And Fixes

The following real failures happened and were fixed.

### Wrong Hair

Problem:

Amara had braids in earlier images, but one chase image gave her low cut hair.

Fix:

Regenerate with a stronger lock:

```text
same natural black cornrow braids, no low cut, no short hair, no shaved head
```

### Dog Food Scene Wrong Focus

Problem:

The scene looked like the girl was calmly watching the dog eat.

Fix:

Split into before and after:

- Dog is the main focus eating the food while Amara is absent.
- Amara later rushes or chases the dog in panic.

### Somto Too Tall Or Too Different

Problem:

Shot `p001-s014` made Somto look too tall and too adult.

Fix:

Regenerate with Somto seated low in the doorway, younger, green patterned blouse, dark wrapper, same braids, not adult, not tall.

### Stacked Frames

Problem:

Some images looked like stacked panels or multiple frames in one image.

Affected examples:

- `p001-s025`
- `p001-s027`
- `p001-s031`
- `p001-s032`

Fix:

Add strong single-frame instructions:

```text
single unbroken true 9:16 frame, no split screen, no multi-panel, no duplicate rows, no stacked frames
```

### Calabash Changed

Problem:

The calabash shape and appearance changed across images.

Fix:

Add a repeated prop lock:

```text
one small tan dried gourd, honey-brown mottled matte surface, rounded lower belly, smaller upper bulb, short narrow neck, faded red cotton thread around the waist
```

### Short Legs

Problem:

Shot `p001-s030` made the lady's legs too short.

Fix:

Regenerate with normal full-body anatomy and natural leg proportions.

### Speaking Mouth Failures

Problem:

Some speaking shots kept closed mouths even when the prompt requested open mouth.

Fix:

Use stronger speaking lock:

```text
mouth visibly open mid-sentence, lips separated, lower jaw dropped, dark mouth interior visible, a few teeth visible
```

If repeated attempts still fail, keep the best image if it passes all other critical QA and document the limitation.

## Chatterbox TTS

Use Chatterbox for narration.

Read the script body, not metadata headers.

For Stolen Innocence continuation:

Narration text:

```text
C:\Social Content\Asset\Stolen Innocence\continuation-part-001\audio\narration-text.txt
```

Generated full narration:

```text
C:\Social Content\Asset\Stolen Innocence\continuation-part-001\audio\narration-full.wav
```

Generated chunks:

```text
C:\Social Content\Asset\Stolen Innocence\continuation-part-001\audio\chunks
```

TTS command used:

```powershell
& "C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\python_embeded\python.exe" `
  "C:\Social Content\skills\chatterbox-tts\scripts\chatterbox_tts.py" generate `
  --model turbo `
  --persona "young woman" `
  --text-file "C:\Social Content\Asset\Stolen Innocence\continuation-part-001\audio\narration-text.txt" `
  --output "C:\Social Content\Asset\Stolen Innocence\continuation-part-001\audio\narration-full.wav" `
  --chunk-output-dir "C:\Social Content\Asset\Stolen Innocence\continuation-part-001\audio\chunks" `
  --max-words 35 `
  --seed 240705
```

Result:

- Full narration: 602.70 seconds.
- Sample rate: 24000 Hz.
- Channels: mono.
- Chunks: 53 WAV files.

Failure:

The TTS process output became too long and got truncated in the terminal.

Fix:

After truncation, check process and files instead of assuming failure.

Check if Chatterbox is still running:

```powershell
Get-CimInstance Win32_Process |
  Where-Object { $_.Name -eq 'python.exe' -and $_.CommandLine -match 'chatterbox_tts.py|tts_turbo|Chatterbox' } |
  Select-Object ProcessId,ParentProcessId,Name,CommandLine
```

Check generated files:

```powershell
Get-ChildItem -LiteralPath "C:\Social Content\Asset\Stolen Innocence\continuation-part-001\audio" -Force
Get-ChildItem -LiteralPath "C:\Social Content\Asset\Stolen Innocence\continuation-part-001\audio\chunks" -Force
```

## Audio Manifest

If Chatterbox does not create a manifest, create one.

The manifest should include:

- Project.
- Part.
- Voice.
- Narrator.
- Model.
- Seed.
- Sample rate.
- Total duration.
- Chunk text.
- Chunk audio file path.
- Chunk start time.
- Chunk duration.
- Chunk end time.

For Stolen Innocence continuation:

```text
C:\Social Content\Asset\Stolen Innocence\continuation-part-001\audio\narration-manifest.json
```

## HyperFrames Video Assembly

Use HyperFrames for video assembly.

The final video should include:

- Approved ComfyUI images.
- Voiceover audio.
- Captions synced to narration chunks.
- Gentle image motion.
- Scene transitions.
- Background ambience or music.
- SFX for transitions and key story beats.

For Stolen Innocence continuation, a helper script was created:

```text
C:\Social Content\tools\build_stolen_continuation_hyperframes.py
```

It produced:

```text
C:\Social Content\Asset\Stolen Innocence\continuation-part-001\video\hyperframes\index.html
C:\Social Content\Asset\Stolen Innocence\continuation-part-001\video\captions\continuation-part-001.srt
C:\Social Content\Asset\Stolen Innocence\continuation-part-001\video\timeline-manifest.json
C:\Social Content\Asset\Stolen Innocence\continuation-part-001\video\hyperframes\media\audio\ambient-bed.wav
C:\Social Content\Asset\Stolen Innocence\continuation-part-001\video\hyperframes\media\audio\soft-whoosh.wav
C:\Social Content\Asset\Stolen Innocence\continuation-part-001\video\hyperframes\media\audio\calabash-chime.wav
```

The builder copied approved image clips into:

```text
C:\Social Content\Asset\Stolen Innocence\continuation-part-001\video\hyperframes\media\images
```

The builder did not edit the approved source images.

## HyperFrames Checks

Run these before rendering:

```powershell
npx.cmd hyperframes lint
npx.cmd hyperframes validate
npx.cmd hyperframes inspect --samples 12
```

Run from:

```text
C:\Social Content\Asset\Stolen Innocence\continuation-part-001\video\hyperframes
```

Stolen Innocence continuation result:

- `lint`: passed with density warnings only.
- `validate`: passed.
- `inspect --samples 12`: 0 layout issues.

Density warnings are acceptable for a long generated story timeline if there are no errors.

## HyperFrames Render

Render command used:

```powershell
npx.cmd hyperframes render `
  --output "C:\Social Content\Asset\Stolen Innocence\continuation-part-001\output\continuation-part-001.mp4" `
  --fps 30 `
  --quality standard
```

Run from:

```text
C:\Social Content\Asset\Stolen Innocence\continuation-part-001\video\hyperframes
```

Final output:

```text
C:\Social Content\Asset\Stolen Innocence\continuation-part-001\output\continuation-part-001.mp4
```

Final render stats:

- File size: 228,971,967 bytes.
- Duration: 602.73 seconds.
- Format: MP4.
- Video: H.264.
- Audio: AAC.
- Size: 1080x1920.
- FPS: 30.
- Aspect ratio: 9:16.

Important note:

HyperFrames reported browser GPU auto mode using Intel UHD Graphics 630 for the video render. This is separate from ComfyUI image generation.

## Rendered Video QA

After rendering, probe the final video:

```powershell
ffprobe -v error -show_entries format=duration,size -show_streams -of json "C:\Social Content\Asset\Stolen Innocence\continuation-part-001\output\continuation-part-001.mp4"
```

Create a contact sheet:

```powershell
& "C:\Users\DELL\Master Project\provix cut\node_modules\ffmpeg-static\ffmpeg.exe" `
  -y `
  -i "C:\Social Content\Asset\Stolen Innocence\continuation-part-001\output\continuation-part-001.mp4" `
  -vf "fps=1/60,scale=216:384,tile=5x3" `
  -frames:v 1 `
  "C:\Social Content\Asset\Stolen Innocence\continuation-part-001\video\verify\render-contact-sheet.jpg"
```

Extract full-size sample frames:

```powershell
& "C:\Users\DELL\Master Project\provix cut\node_modules\ffmpeg-static\ffmpeg.exe" `
  -y `
  -ss 25 `
  -i "C:\Social Content\Asset\Stolen Innocence\continuation-part-001\output\continuation-part-001.mp4" `
  -frames:v 1 `
  "C:\Social Content\Asset\Stolen Innocence\continuation-part-001\video\verify\frame-000025.jpg"
```

Check:

- Video opens.
- Duration is correct.
- Resolution is 1080x1920.
- Audio exists.
- Captions are readable.
- Captions do not cover faces.
- No generated image contains baked-in text.
- No frames are stacked.
- No key scene is broken.
- Night scenes remain night.
- Calabash remains consistent.
- Character continuity holds.

For Stolen Innocence continuation, QA files were:

```text
C:\Social Content\Asset\Stolen Innocence\continuation-part-001\video\verify\render-contact-sheet.jpg
C:\Social Content\Asset\Stolen Innocence\continuation-part-001\video\verify\frame-000025.jpg
C:\Social Content\Asset\Stolen Innocence\continuation-part-001\video\verify\frame-000326.jpg
C:\Social Content\Asset\Stolen Innocence\continuation-part-001\video\verify\frame-000527.jpg
```

## Real Failures During Video Assembly And Fixes

### Python Not On PATH

Problem:

Running `python` failed:

```text
python : The term 'python' is not recognized
```

Fix:

Use the bundled portable Python:

```text
C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\python_embeded\python.exe
```

### UTF-8 BOM In JSON

Problem:

Reading `image-sequence-overrides.json` failed:

```text
JSONDecodeError: Unexpected UTF-8 BOM
```

Fix:

Read the file with `utf-8-sig`.

### HyperFrames Tiny Clip Overlaps

Problem:

HyperFrames lint failed because some clips overlapped by `0.001s`.

Cause:

Floating-point rounding when dividing the total duration across many image clips.

Fix:

Precompute rounded start times and set each clip duration as the difference between consecutive rounded starts.

### Missing caption-overrides.json

Problem:

HyperFrames validate failed:

```text
404 loading caption-overrides.json
```

Fix:

Create an empty file:

```json
{}
```

Saved as:

```text
C:\Social Content\Asset\Stolen Innocence\continuation-part-001\video\hyperframes\caption-overrides.json
```

### Caption Occlusion Warning

Problem:

HyperFrames inspect reported captions as hidden beneath image elements.

Fix:

- Put captions above scene images using a higher `z-index`.
- Mark caption overlay relationship with `data-layout-allow-occlusion`.

### ffmpeg Not On PATH

Problem:

`ffmpeg` was not found on PATH.

Fix:

Use an existing local ffmpeg binary:

```text
C:\Users\DELL\Master Project\provix cut\node_modules\ffmpeg-static\ffmpeg.exe
```

## Final Stolen Innocence Continuation Outputs

Final MP4:

```text
C:\Social Content\Asset\Stolen Innocence\continuation-part-001\output\continuation-part-001.mp4
```

Production manifest:

```text
C:\Social Content\Asset\Stolen Innocence\continuation-part-001\output\continuation-production-manifest.json
```

HyperFrames source:

```text
C:\Social Content\Asset\Stolen Innocence\continuation-part-001\video\hyperframes\index.html
```

Audio manifest:

```text
C:\Social Content\Asset\Stolen Innocence\continuation-part-001\audio\narration-manifest.json
```

Caption file:

```text
C:\Social Content\Asset\Stolen Innocence\continuation-part-001\video\captions\continuation-part-001.srt
```

Rendered QA contact sheet:

```text
C:\Social Content\Asset\Stolen Innocence\continuation-part-001\video\verify\render-contact-sheet.jpg
```

## Simple End-To-End Checklist

Use this checklist every time.

### Source

- [ ] Get story URL.
- [ ] Scrape exact story word-for-word.
- [ ] Save original text.
- [ ] Save metadata and rights notes.
- [ ] If long, split into sections.

### Rewrite

- [ ] Change names.
- [ ] Rewrite in first-person POV.
- [ ] Keep dialogue.
- [ ] Keep interactions.
- [ ] Keep story long and engaging.
- [ ] Identify narrator age and gender.

### Script

- [ ] Run screenwriter stage.
- [ ] Save production script.
- [ ] Confirm script is not a summary.

### Shotlist

- [ ] Run shotlist builder.
- [ ] Each beat has exact shot choice.
- [ ] No prompt asks model to choose a shot.
- [ ] Each visible character has one action.
- [ ] Speaking mouth open only for speaking character.

### Image Prompts

- [ ] Add character locks.
- [ ] Add clothing locks.
- [ ] Add hair locks.
- [ ] Add prop locks.
- [ ] Add lighting locks.
- [ ] Add no-text negative prompt.
- [ ] Split complex beats into multiple prompts.

### ComfyUI

- [ ] Start ComfyUI once.
- [ ] Confirm API health.
- [ ] Confirm GPU use.
- [ ] Generate images.
- [ ] Do not restart per image.

### Image QA

- [ ] Create contact sheet.
- [ ] Check every image.
- [ ] Reject bad anatomy.
- [ ] Reject text in images.
- [ ] Reject stacked/multi-panel images.
- [ ] Reject wrong hair/clothing/props.
- [ ] Regenerate failed images.
- [ ] Archive rejected images.

### Audio

- [ ] Generate narration with Chatterbox.
- [ ] Use correct narrator voice.
- [ ] Save full WAV.
- [ ] Save chunk WAVs.
- [ ] Create audio manifest.
- [ ] Verify duration.

### Video

- [ ] Build HyperFrames project.
- [ ] Copy approved images into media folder.
- [ ] Add narration audio.
- [ ] Add captions.
- [ ] Add ambience/music.
- [ ] Add SFX.
- [ ] Add transitions.
- [ ] Add subtle image motion.

### HyperFrames QA

- [ ] Run lint.
- [ ] Run validate.
- [ ] Run inspect.
- [ ] Fix errors.
- [ ] Render MP4.

### Render QA

- [ ] Probe final MP4.
- [ ] Create contact sheet.
- [ ] Extract full-size sample frames.
- [ ] Check captions.
- [ ] Check image quality.
- [ ] Check no baked text.
- [ ] Check no stacked frames.
- [ ] Save production manifest.

## Non-Negotiable Reminders

- Do not summarize a long story unless the user explicitly asks for a summary.
- Do not remove dialogue and interactions.
- Do not generate text cards instead of ComfyUI images.
- Do not put text inside generated images.
- Do not make the image prompt vague.
- Do not let the image model choose the shot.
- Do not combine multiple actions for one character in one prompt.
- Do not make all characters stare at the camera.
- Do not force open mouth unless the character is speaking.
- Do not restart ComfyUI for every image.
- Do not skip image QA.
- Do not skip rendered video QA.

