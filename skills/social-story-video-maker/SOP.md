# SOP: Social Story Video Maker

## Purpose

Use this SOP to create social media story videos for YouTube, Facebook, TikTok, Shorts, Reels, and similar platforms.

The format is still cinematic images plus narration voice-over. The workflow turns a scraped or supplied story into a first-person story-time script, sentence-level audio, sentence-level image prompts, ComfyUI stills, an editable HyperFrames timeline, synced captions, and a final rendered video.

This is the top-level WAT workflow for picture-narration story videos in `C:\Social Content`.

## Non-Negotiable Rules

1. Never scrape only a summary when the task is to scrape a story. Scrape the exact story text word for word.
2. If the full story is too long for one file or one request, split it into ordered sections and save every section separately.
3. Preserve the original source before rewriting anything.
4. Confirm rights or user authorization before making a publishable adaptation.
5. Keep the edited script in first-person protagonist POV unless the user says otherwise.
6. When requested, make every sentence exactly one image/clip.
7. Captions must match narration word-for-word when the user asks for exact captions.
8. Generated images must not contain baked-in text unless the user explicitly asks for text in the image.
9. Keep the project editable until the final render is approved.

## Skill Files

- Skill folder: `C:\Social Content\skills\social-story-video-maker`
- Main instructions: `SKILL.md`
- Output contract: `references\output-contract.md`
- Canonical workflow: `C:\Social Content\workflows\picture-narration-story-video-sop.md`
- Example completed package: `C:\Social Content\asset\Eve Introduction v2`

## Required Inputs

Collect or infer these before starting:

- Source story URL, discovery request, or pasted story text.
- Rights status: owned, licensed, public domain, permission granted, or private internal review.
- Story title and version folder, for example `asset\Eve Introduction v2`.
- Target platform and aspect ratio. Default short-form is vertical `9:16`.
- Narration style and voice. Use a female voice for female first-person narration unless told otherwise.
- Caption style. Default social captions are bold white text with shadow.
- Music/SFX/transitions. If the user says narration + captions only, do not add music or SFX.
- Image motion. Default is still cinematic shots with Ken Burns motion.
- Color policy. If the user says no color grade, do not add filters or grading.

## Folder Contract

Create one package per story version:

```text
asset/<Story Name>/
  original script/
    original.txt
    sections/
      section-001.txt
      section-002.txt
  edited script/
    edited.txt
    name_map.json
    rewrite_prompt.md
  screenwriter/
    production-script.md
  shotlist/
    asset-plan.md
    sentence-shotlist.md
  director/
    director-package.md
    scene-prompts.json
  audio/
    narration-full.wav
    narration-manifest.json
    chunks/
      narration-001.wav
      narration-002.wav
  images/
    scene-001.png
    scene-002.png
  comfyui-workflows/
    scene-001-workflow.json
    scene-002-workflow.json
  video/
    hyperframes/
    captions/
    verify/
  output/
    final.mp4
  character-bible.json
  scene-beats.json
  image-prompts.md
  render-manifest.json
```

Do not collapse the package into only `final.mp4`.

## Golden Route: Strict Local Pipeline

Use the canonical runner before starting, resuming, or handing off a story-video package:

```powershell
& "C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\python_embeded\python.exe" "C:\Social Content\tools\story_video_pipeline.py" doctor
& "C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\python_embeded\python.exe" "C:\Social Content\tools\story_video_pipeline.py" --story-name "<Story Name>" status
& "C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\python_embeded\python.exe" "C:\Social Content\tools\story_video_pipeline.py" --story-name "<Story Name>" plan
```

Project skills are local folders under `C:\Social Content\skills`. Read their `SKILL.md` and run their scripts directly. Do not invoke `$webscraper`, `$social-story-video-maker`, or any other `$skill` name unless the current runtime explicitly exposes it.

The runner is the gatekeeper. Each stage writes `asset/<Story Name>/pipeline-status/<stage>.json` and stops on the first missing or invalid artifact. Never continue to the next stage after a failed gate.

Canonical stage order:

1. `import-source`
2. `package-rewrite`
3. `rewrite-verification`
4. `screenwriter-shotlist`
5. `prompt-package`
6. `tts`
7. `comfyui-images`
8. `hyperframes-render`
9. `final-qa`

`screenwriter` and `shotlist-builder` are external/global Codex skills, not project-local folders in `C:\Social Content\skills`. If they are unavailable, create the same local handoff artifacts manually before continuing:

```text
asset/<Story Name>/screenwriter/production-script.md
asset/<Story Name>/shotlist/sentence-shotlist.md
asset/<Story Name>/shotlist/asset-plan.md
```

Webscraper output is normalized through `story-time-rewriter`: `stories/<Story>/story.txt` becomes `asset/<Story Name>/original script/original.txt`. Do not skip this handoff.

## Step 1: Scrape The Exact Story

Use `skills\webscraper`.

1. Save metadata first: source URL, title, author if available, scrape date, rights note, and access notes.
2. Scrape the story body exactly as displayed by the source. Do not summarize. Do not paraphrase.
3. If one scrape cannot hold the full text, save chunks:

```text
asset/<Story Name>/original script/sections/section-001.txt
asset/<Story Name>/original script/sections/section-002.txt
asset/<Story Name>/original script/sections/section-003.txt
```

4. Combine the sections into:

```text
asset/<Story Name>/original script/original.txt
```

5. If the site blocks scraping, rights are unclear, or the scraper only returns a summary, stop and ask for pasted or authorized full text. Do not invent missing story text.

Quality check:

- `original.txt` contains the complete verbatim story, not a summary.
- Section files are numbered in reading order.
- Source URL and rights status are recorded.

## Step 2: Rewrite Into First-Person Story-Time

Use `skills\story-time-rewriter`, then pass the result through `screenwriter`.

1. Change all character names.
2. Save every name change in:

```text
asset/<Story Name>/edited script/name_map.json
```

3. Rewrite the story in first-person POV from the protagonist's perspective.
4. Preserve the plot, emotional logic, setting, and key story turns.
5. Use a story-time narration voice suitable for TikTok, Shorts, Facebook, and YouTube.
6. Keep the rewrite sentence-friendly if the user wants one sentence per clip.
7. Save:

```text
asset/<Story Name>/edited script/edited.txt
asset/<Story Name>/screenwriter/production-script.md
```

Production script requirements:

- Narration is ready to be spoken.
- Scene direction is clear.
- Dialogue or reported speech is converted into visible action cues.
- The protagonist remains the narrator.

## Step 3: Split Into Sentence Clips

When the user asks for one sentence per image/clip:

1. Split `edited.txt` into exact narration sentences.
2. Each sentence becomes one `scene-###`.
3. Do not merge two sentences into one clip.
4. Do not split one sentence across two clips unless the user approves.
5. Build:

```text
asset/<Story Name>/scene-beats.json
asset/<Story Name>/shotlist/sentence-shotlist.md
asset/<Story Name>/shotlist/asset-plan.md
```

Each beat must include:

- Scene id.
- Exact sentence.
- Visible action.
- Setting.
- Characters present.
- Emotional beat.
- Camera idea.
- Image filename.
- Audio filename.
- Caption text.

## Step 4: Build The Character Bible

Create:

```text
asset/<Story Name>/character-bible.json
```

For every recurring character, define:

- New name.
- Age range.
- Gender presentation.
- Ethnicity and setting-specific cultural details.
- Skin tone, facial structure, scars, pores, texture, freckles, asymmetry, hairline, hairstyle, and imperfections.
- Body type and posture.
- Exact clothing color, garment type, fabric, accessories, footwear, and condition.
- Emotional baseline.
- Continuity notes.

Costume example:

```text
Nara wears a torn indigo wrapper, a faded red waist sash, bare feet, wet braided hair, and no jewelry until the story changes it.
```

Every image prompt must reuse these details.

## Step 5: Build The Shotlist

Use `skills\shotlist-builder`.

For each sentence, write a production-ready scene entry:

- Scene id.
- Sentence/narration.
- Location and time.
- Shot size.
- Lens feel.
- Camera height and angle.
- Blocking.
- Performance direction.
- Lighting.
- Props and environment.
- Transition or cut behavior.

When narration says someone speaks, show the speaker/listener relationship visually. Use eyeline, shoulder angle, distance, foreground/background, or over-the-shoulder/back-view framing.

Example:

```text
Narration: Wendy told David she hated him.
Image: Wendy in foreground left, shoulders tight, wet lower eyelids, facing David in midground right. David is half-turned away, jaw clenched, listening. Camera is over David's shoulder so Wendy's expression carries the scene.
```

## Step 6: Write Film-Director Image Prompts

Use `skills\film-director`.

Write one detailed prompt per sentence/scene. Each prompt must include:

- Character identity lock.
- Exact clothing lock.
- Facial imperfections and skin pores.
- Realistic texture.
- Acting and micro-expression.
- Blocking and eyeline.
- Camera/lens/framing.
- Lighting and weather.
- Environment and props.
- Continuity constraints.
- Negative prompt: no text, no watermark, no logo, no extra limbs, no distorted hands, no plastic skin, no cartoon, no low-res artifacts.

Save:

```text
asset/<Story Name>/image-prompts.md
asset/<Story Name>/director/director-package.md
asset/<Story Name>/director/scene-prompts.json
```

## Step 7: Generate Chatterbox TTS Audio

Use `skills\chatterbox-tts`.

Recommended local Python runtime:

```text
C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\python_embeded\python.exe
```

Important fix from Eve v2:

- `python` was not available on PATH.
- Use the embedded Python path above when normal `python` fails.
- The Chatterbox script supports `--chunk-output-dir` so each sentence can be saved as its own WAV while also generating a full narration file.
- When the narrator profile gives an age/gender persona, use `--persona` so Chatterbox selects the registered voice: `young woman` = Rho, `young man` = Tayo, `middle aged woman` = Ngozi, `middle aged man` = Ejike, `little girl` = Bonnie, `little boy` = Ade, `old woman` = Morganna, `old man` = Joje.

Example command:

```powershell
& 'C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\python_embeded\python.exe' `
  '.\skills\chatterbox-tts\scripts\chatterbox_tts.py' generate `
  --model turbo `
  --voice 'Carissa_female' `
  --text-file 'C:\Social Content\asset\<Story Name>\edited script\edited.txt' `
  --output 'C:\Social Content\asset\<Story Name>\audio\narration-full.wav' `
  --chunk-output-dir 'C:\Social Content\asset\<Story Name>\audio\chunks' `
  --max-words 1 `
  --seed 240630
```

For persona-routed narration, replace `--voice 'Carissa_female'` with a persona such as `--persona "young woman"` or `--persona "old man"`.

Use `--max-words 1` only when each paragraph or line is already one sentence and the script should force one audio chunk per sentence-like segment. If it creates bad splits, prepare a clean sentence file first.

Save:

```text
asset/<Story Name>/audio/narration-full.wav
asset/<Story Name>/audio/chunks/narration-001.wav
asset/<Story Name>/audio/chunks/narration-002.wav
asset/<Story Name>/audio/narration-manifest.json
```

Manifest must include:

- Voice name.
- Model.
- Seed.
- Sentence text.
- Chunk path.
- Start time.
- Duration.
- End time.

## Step 8: Generate ComfyUI Images

Use `skills\comfyui-media-generator`.

### ComfyUI Must Not Restart For Every Image

Do not restart ComfyUI for each image. That wastes time and can lose model cache.

Correct process:

1. Start ComfyUI once.
2. Wait until `http://127.0.0.1:8190/system_stats` responds.
3. Submit multiple workflow JSON files to the same running API server.
4. Generate in small batches if the machine is unstable.
5. Restart ComfyUI only when the server is dead, unresponsive, out of VRAM, or a workflow corrupts the session.

Recommended persistent start command:

```powershell
Start-Process `
  -FilePath 'C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\python_embeded\python.exe' `
  -ArgumentList '.\main.py --listen 127.0.0.1 --port 8190' `
  -WorkingDirectory 'C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI' `
  -WindowStyle Hidden
```

Health check:

```powershell
Invoke-WebRequest -UseBasicParsing 'http://127.0.0.1:8190/system_stats'
```

Submit command:

```powershell
& 'C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\python_embeded\python.exe' `
  'C:\Social Content\skills\comfyui-media-generator\scripts\comfyui_api.py' `
  --server 'http://127.0.0.1:8190' `
  --workflow 'C:\Social Content\asset\<Story Name>\comfyui-workflows\scene-001-workflow.json' `
  --asset-root 'C:\Social Content\asset\<Story Name>' `
  --kind image `
  --timeout 900
```

### Eve v2 ComfyUI Fixes To Preserve

The stable base workflow was:

```text
C:\Social Content\Asset\workflows\nigerian-boy-playing-in-mud-krea2-api-fixed-qwen-vae-512.json
```

Known working model settings:

```text
UNETLoader: krea2_turbo_fp8_scaled.safetensors
CLIPLoader: qwen3vl_4b_fp8_scaled.safetensors
CLIP type: krea2
CLIP device: cpu
VAELoader: qwen_image_vae.safetensors
Sampler: euler/simple
Resolution: 512x912
Steps: 28
```

Known failures:

- `832x1472` at 32 steps timed out or crashed.
- `640x1136` at 28 steps timed out or crashed.
- `512x912` at 28 steps succeeded but took about 9 to 11 minutes per image.
- Missing or wrong VAE caused bad output. Use `qwen_image_vae.safetensors`.
- The first scene may need a retry with a new seed when the action is wrong.

Quality rule:

- Use the highest resolution the local ComfyUI setup can reliably finish.
- If high resolution crashes twice, drop to the last proven stable resolution and document it in `render-manifest.json`.

Current limitation:

- Character identity may drift if no reference-image/IPAdapter/ControlNet workflow is available.
- Proper future fix is to add a reference-image workflow and reuse approved character reference images across scenes.

Save:

```text
asset/<Story Name>/images/scene-001.png
asset/<Story Name>/images/scene-002.png
asset/<Story Name>/comfyui-workflows/scene-001-workflow.json
asset/<Story Name>/video/verify/image-contact-sheet.jpg
```

Reject and regenerate images that contain:

- Text, logo, watermark, or caption baked into the image.
- Wrong character clothing.
- Wrong scene geography.
- Wrong speaker/listener relationship.
- Broken hands, distorted face, plastic skin, or low-resolution artifacts.
- Character identity drift too severe for the story.

## Step 9: Build HyperFrames Timeline

Use `skills\hyperframes`.

Rules:

- Use vertical `9:16` first unless the user requests another format.
- Use one image per sentence if requested.
- Set clip duration from the matching narration WAV duration.
- Add only narration and captions when the user asks for no SFX/BGM.
- Do not color grade when the user asks for natural output.
- Copy media into the HyperFrames project. Avoid `../` paths.
- Use Ken Burns motion for still images: slow push, subtle pan, or hold.
- Captions should be bold white social-media captions with shadow unless the user asks for another style.
- Caption text must match narration word-for-word when requested.

Recommended files:

```text
asset/<Story Name>/video/hyperframes/index.html
asset/<Story Name>/video/hyperframes/timeline.json
asset/<Story Name>/video/hyperframes/media/images/scene-001.png
asset/<Story Name>/video/hyperframes/media/audio/chunks/narration-001.wav
asset/<Story Name>/video/captions/<story-name>.srt
```

Eve v2 HyperFrames fixes:

- `npx hyperframes lint` expects the project directory, not the HTML file.
- `npx hyperframes render` expects the project directory plus `index.html`, not only the composition id.
- Adjacent audio clips on one track can trigger microscopic floating-point overlap warnings. Fix by putting each audio clip on a unique `data-track-index`.
- If `npx` fails with network or permission errors, rerun with approved escalation.

Commands:

```powershell
npx.cmd hyperframes lint 'C:\Social Content\asset\<Story Name>\video\hyperframes'

npx.cmd hyperframes inspect 'C:\Social Content\asset\<Story Name>\video\hyperframes' `
  --composition <composition-id> `
  --time 4

npx.cmd hyperframes render 'C:\Social Content\asset\<Story Name>\video\hyperframes' index.html `
  --output 'C:\Social Content\asset\<Story Name>\output\final.mp4'
```

## Step 10: Export Captions

Create a separate `.srt` file from the exact narration chunk timings.

Example:

```text
1
00:00:00,000 --> 00:00:02,400
I used to think betrayal was just a wound.

2
00:00:02,400 --> 00:00:03,960
Then I died inside it.
```

Save:

```text
asset/<Story Name>/video/captions/<story-name>.srt
```

## Step 11: Verify Render

Use FFmpeg/FFprobe when available.

Known local FFmpeg path:

```text
C:\Users\DELL\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin
```

Verify:

```powershell
& '<ffmpeg-bin>\ffprobe.exe' -v error `
  -show_entries format=duration:stream=index,codec_type,width,height,r_frame_rate,duration `
  -of json `
  'C:\Social Content\asset\<Story Name>\output\final.mp4'
```

Create contact sheet:

```powershell
& '<ffmpeg-bin>\ffmpeg.exe' -y `
  -i 'C:\Social Content\asset\<Story Name>\output\final.mp4' `
  -vf "fps=1/6,scale=180:320,tile=4x3" `
  -frames:v 1 `
  'C:\Social Content\asset\<Story Name>\video\verify\render-contact-sheet.jpg'
```

Check:

- Final video exists.
- Duration matches narration.
- Resolution is correct.
- Captions are readable and do not overflow.
- No unwanted text appears in images.
- Narration is audible.
- No SFX/BGM exists if the user requested narration + captions only.
- Render manifest records failures, fixes, and residual risks.

## Step 12: Write Render Manifest

Save:

```text
asset/<Story Name>/render-manifest.json
```

Include:

- Project name.
- Status.
- Aspect ratio, width, height, fps, duration.
- Skills used.
- Source story path.
- Edited script path.
- Voice.
- Image model/workflow.
- Caption file.
- Final video path.
- QA results.
- Known limitations.

Example limitation from Eve v2:

```text
Some ComfyUI stills show character identity drift because no image-reference/IPAdapter workflow was available in the local ComfyUI setup.
```

## Common Failure Fixes

### Scraper Only Gets A Summary

Stop. Do not continue with the summary. Use a better scraper, scrape sections, or ask the user for the full authorized text.

### Story Is Too Long

Save verbatim sections under `original script/sections/`, then combine them into `original.txt`.

### Python Is Not Found

Use:

```text
C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\python_embeded\python.exe
```

### ComfyUI Will Not Start

1. Check whether port `8190` is already in use.
2. Start ComfyUI with `Start-Process`.
3. Wait for `/system_stats`.
4. If it still fails, inspect ComfyUI console logs.

### ComfyUI Dies After Each Command

Do not start it inside a short-lived shell command that exits with the server attached. Start it as a background process with `Start-Process`, then submit jobs to that persistent server.

### Image Generation Times Out

1. Keep the same running server.
2. Reduce batch size.
3. Reduce resolution to last known stable size.
4. Increase API timeout.
5. Save the failed workflow and error in the manifest.

### Character Identity Drifts

1. Tighten `character-bible.json`.
2. Reuse exact clothing and facial details in every prompt.
3. Regenerate only affected scenes.
4. Best future fix: use reference-image/IPAdapter/ControlNet workflow.

### HyperFrames Lint Says Audio Clips Overlap

If adjacent audio clips touch at the same timestamp, put each audio clip on a unique track instead of trimming audio.

### Render Duration Looks Wrong In CLI Summary

Confirm with `ffprobe`. In Eve v2, the CLI summary looked like elapsed render time, but `ffprobe` confirmed the MP4 was `63.5s`.

## Eve Introduction v2 Proven Settings

Use these as a working reference, not as a permanent limit:

```text
Package: C:\Social Content\asset\Eve Introduction v2
Format: 720x1280, 30fps, 9:16
Duration: 63.509s
Voice: Carissa_female
Images: 26
Audio chunks: 26
Caption file: video/captions/eve-introduction-v2.srt
ComfyUI resolution: 512x912
ComfyUI steps: 28
Render: HyperFrames MP4
QA: lint 0 errors, inspect 0 layout issues, ffprobe duration matched audio
```

## Final Handoff

Return only the important paths:

```text
Final video: asset/<Story Name>/output/final.mp4
SRT captions: asset/<Story Name>/video/captions/<story-name>.srt
Manifest: asset/<Story Name>/render-manifest.json
Preview/contact sheet: asset/<Story Name>/video/verify/render-contact-sheet.jpg
```

Mention any residual risk, such as image identity drift, missing rights confirmation, or source access limits.

## Stolen Innocence 2026-07-02 SOP Update

This section is the dummy-proof process learned during the `Stolen Innocence` production run. Follow it for every future story-video project unless the user explicitly changes the workflow.

### The Correct End-To-End Order

Do the work in this exact order:

1. Scrape the story with `skills/webscraper`.
2. Save the exact source story word-for-word under `original script/`.
3. If the story is too long, split it into ordered verbatim files under `original script/sections/`. Never replace the story with a summary.
4. Rewrite with `skills/story-time-rewriter`: change all names, preserve the full plot, preserve dialogue and interactions, and narrate in first-person protagonist POV.
5. Pass the rewritten script through `screenwriter` and save a production-ready script.
6. Pass the production script through `shotlist-builder`.
7. The shotlist must choose the camera, framing, blocking, lighting, action, and visible characters for each shot. Do not let the image prompt decide between multiple camera choices.
8. Pass each shot to `film-director` for detailed image prompts.
9. Generate the actual images through `skills/comfyui-media-generator`.
10. Generate narration chunks through `skills/chatterbox-tts`, using the persona that matches narrator age/gender.
11. Combine images, audio, captions, SFX, music, and transitions with HyperFrames and/or `video-use`.
12. Render to `asset/<Story Name>/output/` and write the production manifest.

### Verbatim Scraping Rule

When scraping a story from the internet:

- Do not scrape only a summary.
- Do not summarize because the story is long.
- Do not continue production from a short synopsis unless the user explicitly requests a summary video.
- Save the exact story text from the website word-for-word.
- If the full story cannot fit in one file, save sections:

```text
asset/<Story Name>/original script/sections/section-001.txt
asset/<Story Name>/original script/sections/section-002.txt
asset/<Story Name>/original script/sections/section-003.txt
```

- Then combine the sections into:

```text
asset/<Story Name>/original script/original.txt
```

If access, rights, or a site blocker prevents exact scraping, stop and ask for authorized pasted text. Do not invent the missing story.

### Rewrite Rule: Preserve Length, Dialogue, And Interaction

The story-time rewrite must preserve story substance. Do not compress it into a short summary.

Required:

- Preserve dialogue and interaction scenes.
- Preserve the order of events.
- Preserve the emotional pauses and decisions.
- Change character names consistently and save `name_map.json`.
- Use first-person POV from the protagonist.
- Use voice-over for events the protagonist did not directly witness.
- If the rewritten script becomes too long, split it into parts and process the first part. Do not summarize the part.

Bad rewrite pattern:

```text
My cousin left me, the dog ate my food, and the elder helped me. That night I joined a dark gathering.
```

Good rewrite pattern:

```text
Somto pushed the kitchen door with her hip and pointed at the covered plate.
"If you get hungry, eat that one," she said.
"Where are you going?" I asked.
She did not answer me properly. She only tightened her wrapper and looked toward the path.
```

### Sentence Splitting Is Not Blind

The rule "one sentence gets one image" is a guide, not an excuse to overload or under-direct a scene.

Split one sentence into multiple image beats when the sentence contains multiple visual actions.

Example:

```text
Somto slipped out to meet her friends, and when hunger woke me, I found our dog Koko eating the food she had left for me.
```

Correct visual split:

1. Somto sneaks out of the compound.
2. Amara wakes from her bed/mat hungry.
3. Koko is eating the food while Amara is absent or just rushing in.
4. Optional action beat: Amara chases Koko away.

Do not create one overloaded prompt containing Somto leaving, Amara waking, Koko eating, and Amara chasing in the same frame.

### Shotlist Builder Must Make Decisions

The shotlist must decide the shot. Never write vague choices such as:

```text
Use the specified over-the-shoulder, facing-each-other, side-by-side, or close-up reaction composition.
```

That is wrong because it asks the image model to choose. The prompt must choose one:

```text
85mm over-the-shoulder from behind Amara toward Elder Okoro at the fence.
```

or:

```text
Strict left-facing side-profile close-up of Elder Okoro speaking to Amara off-camera.
```

For every shot, specify:

- shot size
- lens feel
- camera height
- camera angle
- foreground/midground/background
- exact visible characters
- exact action or pose for each character
- exact lighting source
- exact prop placement

### One Prompt, One Main Action Per Character

An image prompt must not contain multiple actions for one character.

Wrong:

```text
Amara wakes, grabs the calabash, crawls under the bed, hides it, then looks afraid.
```

Correct split:

1. Amara wakes beside Somto.
2. The calabash is visible near her mat.
3. Amara tiptoes out with the calabash.
4. Amara pushes the calabash under the bamboo bed.

If a character is speaking, the action is speaking. Do not also make the same character walk, point, grab, and turn in the same still.

### Character Visibility And Prompt Leakage

Only describe characters who should appear in the image.

If Somto is not supposed to appear, do not include Somto's clothing or character lock in that prompt. During `Stolen Innocence`, including Somto's continuity in a two-person Elder/Amara prompt caused ComfyUI to add Somto as an unwanted third person.

Correct prompt structure:

```text
Only these named characters may appear clearly in this frame: Amara, Elder Okoro.
Visible character locks: Amara ...; Elder Okoro ...
```

Do not include unused character locks.

### Multi-Character Composition Rules

For 1 person:

- Use a clear single-subject shot.
- The person must be doing the scene action, not standing blankly at the camera.

For 2 people:

- Use a chosen composition: over-the-shoulder, facing each other, side-by-side, or close-up reaction.
- Do not list multiple composition options.
- Show eyelines and body orientation.

For more than 2 people:

- Prefer over-the-shoulder from one side toward the others.
- Or show a close-up of one character with the others soft/blurred behind.
- Or show a wide establishing group shot when the story requires the group, such as a ritual gathering.
- Avoid flat group portraits.

### Speaking Mouth Rule

Only use an open-mouth mid-sentence instruction when the visible character is actually speaking in that exact shot.

Do not force an open mouth for listening, reacting, watching, walking, hiding, eating, sleeping, crying, fear, shock, or silent action shots. For silent shots, describe the correct expression instead, such as lips pressed tight, mouth slightly parted in fear, jaw tense, or silent shock.

When the scene line is spoken by a visible character, the image prompt must say the speaker's mouth is open mid-sentence.

Weak wording may fail:

```text
Elder speaks mid-sentence.
```

Stronger wording:

```text
Elder Okoro's lower jaw is dropped mid-word, lips separated, dark mouth interior and a few teeth visible.
```

Add negative prompt text for speaking shots:

```text
closed mouth on speaking character, sealed lips on speaking character
```

If a two-person shot refuses to show the mouth open, split it:

1. Use the two-person wide/medium shot as setup.
2. Generate a single-character close-up of the speaker.
3. Use both images back-to-back in the video as a push-in.

If a strict side-profile close-up hides the speaker's mouth, change the chosen shot to a three-quarter speaking close-up. Do not ask the generator to choose. Replace the shot direction with one exact instruction such as:

```text
Three-quarter left-facing 85mm head-and-shoulders close-up of Elder Okoro at the fence, Amara off-camera. Elder Okoro is captured mid-question; his mouth is open wide, lower jaw dropped, lips stretched apart, dark mouth interior and uneven teeth clearly visible.
```

If ComfyUI still produces a slightly closed mouth after two clean retries, keep the best valid setup and close-up as an edit pair, note the limitation in QA, and continue generating the remaining story. Do not lose the whole production pass on one stubborn expression.

### Using Two Images As A Push-In

If two generated images both work, keep both instead of discarding one.

Example from `Stolen Innocence`:

```text
p001-s003a-wide-setup.png
p001-s003b-medium-closeup.png
```

Use the wider setup first, then the tighter shot second. In the video this feels like the camera zooms or cuts closer to the speaking man.

Save the override:

```text
asset/<Story Name>/images/image-sequence-overrides.json
```

Example:

```json
{
  "p001-s003": [
    "p001-s003a-wide-setup.png",
    "p001-s003b-medium-closeup.png"
  ]
}
```

### Lighting Source Rule

Describe only the physical light source that exists in the scene.

If the girl is using a lamp, the lamp is the only light source:

```text
Night bedroom: one small kerosene lamp near Amara is the only light source; all shadows and highlights come from that lamp only.
```

Do not add moonlight, fill light, cinematic side light, or an unseen softbox unless that source is visible or physically justified.

For dream night scenes:

```text
Cold moonlight is the only light source; faces fall into natural shadow, no fire glow, no fill light.
```

For daytime compound scenes:

```text
Daytime natural light only from the visible sky and open compound; no fill, no extra light source.
```

### Specific Stolen Innocence Scene Rules

When Amara is left in the house with Somto, Somto must appear in at least one image so it does not look like Amara was alone from the start.

For the dog-food scene:

- Use two images if needed.
- First image: Koko eating the food while Amara is absent, or Koko eating as Amara rushes in.
- Second image: Amara chases Koko away.
- Koko must be the main focus when the narration says the dog ate her food.

For the night gathering:

1. Night sky with half/full moon.
2. Amara in the middle of the black-gowned gathering at night.
3. Side-profile close-up of Elder Okoro speaking to Amara.

For the calabash handoff:

- Use a front-view low-angle POV from Amara's eye line.
- Elder Okoro hands the calabash directly toward the camera.
- The camera represents Amara.

For the real calabash beside/under the bed:

- Use an under-the-bed POV.
- The calabash is large in the foreground.
- Amara looks under the bed in shock.
- Lamp is the only light source if she is using a lamp.

### ComfyUI: Do Not Restart For Every Image

ComfyUI should not restart for every image. The correct target state is:

1. Start ComfyUI once.
2. Submit image jobs to the persistent API server.
3. Generate in batches when stable.
4. Generate one image at a time only while diagnosing instability.
5. Restart only when ComfyUI crashes, becomes unresponsive, runs out of VRAM, or corrupts its model state.

During `Stolen Innocence`, ComfyUI crashed with:

```text
exit_code=-1073741819
Windows fatal exception: access violation
```

The stack trace showed the crash during Krea2 GPU/model movement:

```text
comfy_kitchen\tensor\base.py
comfy\model_patcher.py
comfy\model_management.py
Requested to load Krea2
```

The port disappeared because the ComfyUI Python process died. The port itself did not crash.

### ComfyUI Safe Launch Fix

Use the safe launcher when the normal Krea2 launch crashes:

```text
C:\Social Content\tools\run_comfyui_8190_safe.cmd
```

This starts ComfyUI with:

```text
--windows-standalone-build --disable-cuda-malloc --listen 127.0.0.1 --port 8190
```

Why:

- The crash happened in CUDA memory/model movement.
- `--disable-cuda-malloc` switches the device from `cudaMallocAsync` to native CUDA allocation.
- This prevented the repeated access-violation crash on `p001-s003`.

Expected system stats should show:

```text
"argv": ["--disable-cuda-malloc", "--listen", "127.0.0.1", "--port", "8190"]
"name": "cuda:0 Quadro P5200 : native"
```

Safe launcher logs:

```text
C:\Social Content\.tmp\comfyui-logs\runner-safe-stdout.log
C:\Social Content\.tmp\comfyui-logs\runner-safe-stderr.log
C:\Social Content\.tmp\comfyui-logs\runner-safe-exit.txt
```

### Recovering From A ComfyUI Crash

1. Check server:

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:8190/system_stats' -TimeoutSec 5
```

2. Check queue:

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:8190/queue' -TimeoutSec 5
```

3. Check stranded generators:

```powershell
Get-CimInstance Win32_Process |
  Where-Object { $_.Name -in @('python.exe','powershell.exe','cmd.exe') -and ($_.CommandLine -match 'generate_stolen_continuation|ComfyUI|main.py') } |
  Select-Object ProcessId,ParentProcessId,Name,CommandLine
```

4. Stop stranded generator processes that are waiting on a dead server.
5. Read crash tail:

```powershell
Get-Content 'C:\Social Content\.tmp\comfyui-logs\runner-stderr.log' -Tail 120
```

6. Start safe ComfyUI:

```powershell
Start-Process -FilePath 'C:\Social Content\tools\run_comfyui_8190_safe.cmd' -WindowStyle Hidden
```

7. Verify `/system_stats`.
8. Resume from the first missing shot, not from the beginning.

### Freeing VRAM Between Risky Jobs

When ComfyUI is alive but VRAM is almost full, call:

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:8190/free' `
  -Method Post `
  -ContentType 'application/json' `
  -Body '{"unload_models": true, "free_memory": true}' `
  -TimeoutSec 10
```

Use this before a retry after a failed or rejected image.

### ComfyUI Workflow Rules

Do not append the negative prompt into the positive prompt node. This mistake caused prompt confusion.

Wrong:

```python
workflow["3"]["inputs"]["text"] = item["prompt"] + " Negative prompt: " + item["negative_prompt"]
```

Correct:

```python
workflow["3"]["inputs"]["text"] = item["prompt"]
```

If the workflow does not have a real negative conditioning node, keep the negative prompt in documentation and use positive constraints carefully.

### Complete PNG Copy Rule

ComfyUI may create the output PNG path before the file is fully written. Do not copy a file just because it appears in `ComfyUI\output`.

Before copying a generated PNG into the package image folder or canonical shot filename:

1. Check that file size is greater than zero.
2. Wait briefly.
3. Check that file size did not change.
4. Open it with PIL and call `image.load()`.
5. Only then copy it to `images/<shot-id>.png`.

If this is skipped, a file can look like a successful render in the folder but later fail with:

```text
OSError: image file is truncated
```

`C:\Social Content\tools\generate_stolen_continuation_images.py` includes this safeguard in `is_complete_png()`. Keep that check in place for all future ComfyUI batch generators.

Known working local Krea2 settings from `Stolen Innocence`:

```text
Workflow template: C:\Social Content\Asset\workflows\nigerian-boy-playing-in-mud-krea2-api-fixed-qwen-vae-512.json
UNET: krea2_turbo_fp8_scaled.safetensors
CLIP: qwen3vl_4b_fp8_scaled.safetensors
CLIP type: krea2
VAE: qwen_image_vae.safetensors
Resolution: 576x864 for continuation shots
Steps: 28
Sampler: euler
Scheduler: simple
CFG: 1.0
```

If the normal server crashes, use safe launch. If the safe server is stable, continue without restarting for every image.

### GPU Verification And CLIP Device

Do not assume GPU use from render speed alone. Confirm it from both ComfyUI and Windows/NVIDIA process counters.

Check ComfyUI device:

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:8190/system_stats' -TimeoutSec 5
```

Expected device line:

```text
cuda:0 Quadro P5200 : native
```

Check which process is using the GPU:

```powershell
nvidia-smi --query-compute-apps=pid,process_name,used_gpu_memory --format=csv,noheader,nounits
Get-Counter '\GPU Engine(*)\Utilization Percentage' -SampleInterval 1 -MaxSamples 3
```

During `Stolen Innocence`, ComfyUI process PID `24100` showed GPU Engine utilization above 80%, proving ComfyUI itself was using the GPU, not just another app.

Krea2 workflow node `2` is `CLIPLoader`. Its supported device values are:

```text
default
cpu
```

Older local templates used:

```json
"device": "cpu"
```

That keeps the text encoder on CPU while the diffusion model still uses GPU. If the user wants ComfyUI to use GPU as much as possible, set node `2` to:

```json
"device": "default"
```

Confirm in ComfyUI logs:

```text
CLIP/text encoder model load device: cuda:0
```

If GPU memory errors return, switch only the CLIPLoader back to `cpu`; keep the diffusion model on CUDA.

### Current Helper Scripts

Continuation package builder:

```text
C:\Social Content\tools\rebuild_stolen_innocence_continuation_part01.py
```

Continuation image generator:

```text
C:\Social Content\tools\generate_stolen_continuation_images.py
```

Safe ComfyUI launcher:

```text
C:\Social Content\tools\run_comfyui_8190_safe.cmd
```

Generation command:

```powershell
& 'C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\python_embeded\python.exe' `
  'C:\Social Content\tools\generate_stolen_continuation_images.py' `
  --start 3 --end 3 --timeout 3600
```

Generate in small ranges only after stability is proven:

```powershell
& 'C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\python_embeded\python.exe' `
  'C:\Social Content\tools\generate_stolen_continuation_images.py' `
  --start 5 --end 8 --timeout 3600
```

### Chatterbox TTS Rules

Use `skills/chatterbox-tts`.

Narrator selection:

- Little girl: `--persona "little girl"`
- Little boy: `--persona "little boy"`
- Young woman: `--persona "young woman"`
- Young man: `--persona "young man"`
- Middle aged woman: `--persona "middle aged woman"`
- Middle aged man: `--persona "middle aged man"`
- Old woman: `--persona "old woman"`
- Old man: `--persona "old man"`

For `Stolen Innocence`, the story is narrated by a female child/young woman protagonist depending on the chosen narration framing. If the narration is adult Amara telling her childhood story, use young woman. If the narration is performed as twelve-year-old Amara in the moment, use little girl.

Generate chunks, not one uneditable monolith:

```powershell
& 'C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\python_embeded\python.exe' `
  'C:\Social Content\skills\chatterbox-tts\scripts\chatterbox_tts.py' generate `
  --model turbo `
  --persona "young woman" `
  --text-file 'C:\Social Content\asset\<Story Name>\edited script\edited.txt' `
  --output 'C:\Social Content\asset\<Story Name>\audio\narration-full.wav' `
  --chunk-output-dir 'C:\Social Content\asset\<Story Name>\audio\chunks'
```

Save the narration manifest and use chunk durations to time images.

### QA Before Continuing A Batch

Before continuing image generation, inspect the last generated image.

Reject or repair if:

- It contains a character who was not supposed to appear.
- It omits a character who must appear.
- Hair changes, especially Amara's braids becoming low-cut or short hair.
- Speaker mouth is closed when the shot is a speaking shot.
- Body is static and plainly camera-facing when action is required.
- Lighting uses sources not in the scene.
- A multi-person scene becomes a flat group portrait.
- The prompt contains multiple actions for one character.
- The prompt tells the model to choose between shot types.

Use alternate images when useful. A wider shot followed by a medium close-up can create a camera push-in effect in the video.

## Stolen Innocence 2026-07-05 Execution Addendum

Use this addendum as the dummy-proof checklist for the full social story video skill process. It records the exact workflow and failure fixes learned during `Stolen Innocence`.

### What This Skill Does

The skill turns a web story or supplied story into a narrated vertical social video:

1. Capture the full story source.
2. Rewrite it as a first-person story-time narration with changed names.
3. Convert the rewrite into a production-ready script.
4. Build a sentence/beat shotlist with exact camera decisions.
5. Write one detailed image prompt per visual beat.
6. Generate Chatterbox narration chunks.
7. Generate ComfyUI still images.
8. QA every generated image.
9. Build an editable HyperFrames/video-use timeline with captions, SFX, music, and transitions.
10. Render the final video into `asset/<Story Name>/output/`.

Never skip from rewrite straight to video. The required chain is:

```text
webscraper -> story-time-rewriter -> screenwriter -> shotlist-builder -> film-director -> comfyui-media-generator -> chatterbox-tts -> hyperframes/video-use -> final QA
```

### Source Capture Must Be Verbatim

When the input is a website story, scrape the exact story word for word.

Do not:

- Use only a website summary.
- Summarize because the story is long.
- Remove dialogue to make the rewrite shorter.
- Continue production from a synopsis unless the user explicitly asks for a summary video.

If the story is too long, split the original into numbered source files:

```text
asset/<Story Name>/original script/sections/section-001.txt
asset/<Story Name>/original script/sections/section-002.txt
asset/<Story Name>/original script/sections/section-003.txt
```

Then combine them into:

```text
asset/<Story Name>/original script/original.txt
```

### Rewrite Must Stay Long And Dramatic

The story-time rewrite must preserve the full story experience, not summarize it.

Required:

- Change character names and save `name_map.json`.
- Narrate in first-person protagonist POV.
- Preserve dialogue and interaction scenes.
- Preserve small actions that set up later consequences.
- Keep emotional beats, pauses, fear, hesitation, and conflict.
- If the rewrite is too long, split it into parts and process the first part. Do not compress it into a short recap.

For `Stolen Innocence`, the mistake was making the rewrite too short and removing dialogue. The fix is to continue from the last approved point and preserve every interaction from the source.

### Sentence Splitting Must Be Visual, Not Mechanical

The rule "one sentence per image" means every narration sentence needs visual coverage. It does not mean a sentence with many actions must become one overloaded image.

If one sentence contains multiple visual actions, split it into multiple beats.

Example:

```text
Somto slipped out to meet her friends, and when hunger woke me, I found our dog Koko eating the food she had left for me.
```

Correct split:

1. Somto sneaks out.
2. Amara wakes hungry.
3. Koko eats the food while Amara is absent or just rushing in.
4. Amara chases Koko away.

Wrong:

```text
Somto sneaks out while Amara wakes and Koko eats food and Amara chases the dog in the same image.
```

### Shotlist Builder Must Decide The Shot

The shotlist must choose one exact composition per image.

Never write:

```text
Use the specified over-the-shoulder, facing-each-other, side-by-side, or close-up reaction composition.
```

That is bad because it asks the image generator to choose.

Write one direct instruction instead:

```text
Tight over-the-shoulder medium close-up from behind Father's right shoulder toward Amara.
```

or:

```text
Three-quarter left-facing 85mm close-up of Elder Okoro speaking to Amara off-camera.
```

Every shotlist item must specify:

- exact visible characters
- exact action or pose for each character
- shot size
- lens feel
- camera height
- camera angle
- foreground, midground, and background
- light source
- prop placement
- whether the character is speaking or silent

### Prompt Rule: One Main Action Per Character

Do not put multiple actions for one character in a single image prompt.

Wrong:

```text
Amara wakes, grabs the calabash, tiptoes, hides it under the bed, and looks afraid.
```

Correct split:

1. Amara wakes.
2. Amara sees the calabash.
3. Amara carries the calabash.
4. Amara hides the calabash under the bed.

The more direct the prompt, the better the image.

### Multi-Character Prompt Rules

For one person:

- Show the person doing the scene action.
- Avoid blank camera-facing portraits unless the scene is literally a selfie or direct address.

For two people:

- Use one chosen composition: over-the-shoulder, facing each other, side by side, or close-up reaction.
- Show eyeline, body orientation, and emotional distance.

For more than two people:

- Use an over-the-shoulder shot from one character toward the others, or from the group toward one character.
- Or use a close-up of one character with the others blurred behind.
- Use a wide group shot only when the story requires the full group.
- Avoid flat group portraits.

If a scene needs both a full-body shot and a close-up, generate both and use them back-to-back. In the edit this reads as a camera push-in.

### Speaking Mouth Rule

Only request an open mouth when the character is speaking in that exact image.

Use open-mouth instructions for visible speakers:

```text
Amara is caught mid-sentence: lower jaw dropped, lips separated, visible dark mouth interior and a hint of teeth.
```

Do not request open mouths for:

- listening
- walking
- hiding
- sleeping
- silent fear
- shock
- crying
- chasing
- watching

If a speaking shot keeps rendering with closed lips after two good retries, split the scene into a setup shot and a close-up of the speaker. Keep the best valid pair and continue.

### Character Consistency Locks

Create and obey a character bible before images.

For `Stolen Innocence`, keep these locks:

```text
Amara: Nigerian girl age 12, slim, warm dark-brown skin, faint chicken-pox marks, dark-brown eyes, full lips, black cornrow braids down her shoulders, faded mustard-yellow cotton dress, no low cut, no short hair.
Somto: Nigerian teenage cousin around 14, youthful round face, warm brown skin with tiny acne marks, neat black braids pulled back, green patterned blouse with yellow leaf motifs, dark wrapper tied at the waist, not adult, not tall.
Calabash: small tan dried gourd, honey-brown mottled matte surface, rounded lower belly, smaller upper bulb, short narrow neck, subtle dark speckles and scratches, faded red cotton thread around the waist.
```

Do not include a character lock in a prompt unless that character should appear. Extra character descriptions can cause ComfyUI to add unwanted people.

### Specific Stolen Innocence Fixes

Use these as examples for future QA.

`p001-s014`: Somto looked too different and too tall.

Fix:

- Do not show Somto standing full-height behind Amara.
- Seat Somto low on a small wooden stool in the doorway shadow.
- Show only head, shoulders, and upper chest.
- Keep her head lower than Amara's head.
- Keep the same green patterned blouse, dark wrapper, and braids.
- Keep Father as blurred foreground shoulder.
- If Amara is speaking, her mouth must be open mid-sentence; Somto's mouth stays closed.

`p001-s030`: Amara's legs looked too short.

Fix:

- Add normal body proportion language.
- Specify normal leg length, normal knees, normal ankles, grounded feet.
- Avoid low-angle distortion that crops or compresses the legs.

`p001-s031`: image had stacked/letterboxed structure.

Fix:

- Require a single full-frame 9:16 vertical photograph.
- Negative prompt: no split screen, no black bars, no letterbox, no stacked frames, no collage.
- Inspect the final PNG before continuing.

Calabash drift:

Fix:

- Repeat the exact calabash lock in every calabash prompt.
- Do not allow black pots, bottles, gourds with long necks, or decorative vases.

Text in image:

Fix:

- Remove any story text from the positive prompt body.
- Add: no text, no caption, no typography, no watermark, no logo.
- Remember: story text belongs in video captions, not baked into ComfyUI images.

### Krea2 ComfyUI Workflow Used In Stolen Innocence

The user supplied:

```text
C:\Users\DELL\Downloads\image_krea2_turbo_t2i (1).json
```

Use it as a base workflow when testing speed and quality, but story shots may need a controlled custom copy per scene.

The story-version settings used during this run:

```text
UNET: krea2_turbo_fp8_scaled.safetensors
CLIP/text encoder: qwen3vl_4b_fp8_scaled.safetensors
VAE: qwen_image_vae.safetensors
Sampler: euler
Scheduler: simple
CFG: 1
Steps: 8 for default Krea2 turbo tests
Resolution: 720x1280 for 9:16 portrait tests
Prompt refiner: off
LoRA: off
CLIP device: default when trying more GPU use
```

If the user requests higher quality, test carefully. `1080x1920` at `28` steps can be much slower and may increase OOM risk on the local GPU. Do not assume it is better for batch production until one image completes and passes QA.

### ComfyUI Stability Rules From This Run

Do not restart ComfyUI for every image.

Correct process:

1. Start ComfyUI once.
2. Confirm `http://127.0.0.1:8190/system_stats` responds.
3. Submit workflows to the same server.
4. Generate in small batches.
5. Restart only if ComfyUI dies, is unresponsive, runs out of VRAM, or corrupts output.

Safe launcher:

```text
C:\Social Content\tools\run_comfyui_8190_safe.cmd
```

Use it when Krea2 crashes with access violation or CUDA memory movement errors. It adds:

```text
--disable-cuda-malloc --listen 127.0.0.1 --port 8190
```

Before restarting after an interruption, check for stranded jobs:

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:8190/queue' -TimeoutSec 5

Get-CimInstance Win32_Process |
  Where-Object { $_.Name -in @('python.exe','powershell.exe','cmd.exe') -and ($_.CommandLine -match 'generate_stolen_continuation|ComfyUI|main.py') } |
  Select-Object ProcessId,ParentProcessId,Name,CommandLine
```

If the API is down but a generator process is still waiting on it, treat it as stranded. Stop only the stranded generator or dead ComfyUI process after confirming it is not the user's unrelated job.

### GPU Verification Rule

Do not infer ComfyUI GPU usage only from total GPU utilization. Other software may be using the GPU.

Confirm all three:

1. `/system_stats` reports `cuda:0`.
2. `nvidia-smi` shows the ComfyUI Python PID and GPU memory use.
3. Windows GPU counters show utilization for that same process.

Useful checks:

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:8190/system_stats' -TimeoutSec 5
nvidia-smi --query-compute-apps=pid,process_name,used_gpu_memory --format=csv,noheader,nounits
Get-Counter '\GPU Engine(*)\Utilization Percentage' -SampleInterval 1 -MaxSamples 3
```

If CLIP is set to `cpu`, diffusion can still run on GPU. If the user wants more GPU use, set the Krea2 CLIPLoader device to `default` and verify logs. If VRAM errors return, move CLIP back to `cpu`.

### Mandatory Image QA Before Video Assembly

After image generation, create a QA contact sheet and inspect individual failures.

Reject and regenerate any image with:

- stacked frames, collage layout, letterbox bars, or split-screen output
- baked-in text, logo, watermark, caption, or typography
- wrong character height, age, hairstyle, outfit, or skin details
- Amara without braids
- Somto looking adult or too tall
- wrong calabash shape/color
- short or deformed legs
- wrong character placement
- character blankly facing camera when the scene needs action
- mouth open on a silent character
- mouth closed on a visible speaking character
- impossible lighting source
- extra people added by prompt leakage

Copy rejected images to:

```text
asset/<Story Name>/qa/rejected-before-regen/
```

Patch the workflow JSON and prompt document before regenerating, so the fix survives future resumes.

### Resume Order After QA Fixes

When interrupted:

1. Check ComfyUI queue.
2. Check stranded process list.
3. Inspect the latest canonical image.
4. If the last attempted image failed QA, archive it in `qa/rejected-before-regen/`.
5. Patch `image-prompts.md` and the exact `comfyui-workflows/<shot>-workflow.json`.
6. Regenerate only the bad shot.
7. QA the regenerated shot.
8. Continue from the next missing shot, not from the beginning.

For the current `Stolen Innocence` continuation, after s014 is accepted, continue QA on p020, p024, p025, p027, p028, p031, then generate missing p032-p036.
