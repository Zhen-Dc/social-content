# SOP: HyperFrames

## Purpose

Use this SOP to create editable HTML-based video compositions, title cards, motion graphics, captions, overlays, image-motion scenes, voiceover-driven timelines, audio-reactive visuals, and transitions.

HyperFrames is the preview-first composition layer. HTML is the source of truth.

## Skill Files

- Skill folder: `C:\Social Content\skills\hyperframes`
- Main instructions: `SKILL.md`
- House style: `house-style.md`
- Visual styles: `visual-styles.md`
- Patterns: `patterns.md`
- Data/motion patterns: `data-in-motion.md`
- References: `references\`

Read task-specific references before building:

- `references\video-composition.md` for multi-scene compositions.
- `references\typography.md` for any text.
- `references\motion-principles.md` for any animation.
- `references\captions.md` for captions or subtitles.
- `references\transitions.md` for scene transitions.
- `references\audio-reactive.md` for beat or voice reactive visuals.

## Inputs Needed

- Script, narration, scene plan, storyboard, or existing media.
- Target format: vertical, horizontal, square, or custom.
- Duration and platform.
- Assets: images, video clips, audio, captions, fonts, logos, SFX, music.
- Brand or design direction, ideally `design.md`.

## Where To Save Assets

For story video packages:

```text
asset/<Story Name>/video/hyperframes/
asset/<Story Name>/video/captions/
asset/<Story Name>/video/sfx/
asset/<Story Name>/video/music/
asset/<Story Name>/video/renders/
```

For general video projects:

```text
stories/<Story Name>/video/hyperframes/
stories/<Story Name>/video/assets/
stories/<Story Name>/video/captions/
stories/<Story Name>/video/renders/
```

For standalone experiments:

```text
.tmp/hyperframes/<Project Name>/
```

Do not save a production composition only in the skill folder.

## Composition Structure

A HyperFrames project directory should contain:

```text
index.html
assets/
fonts/
audio/
captions/
renders/
.hyperframes/
```

The main standalone `index.html` must put the `data-composition-id` div directly in `<body>`. Do not wrap the main composition in `<template>`.

## Workflow

1. Read `SKILL.md`.
2. Read required references based on the task.
3. Create or choose the project folder.
4. Gather all media assets into the project folder.
5. Build the final static layout first.
6. Add timing with `data-*` attributes and a seekable GSAP timeline.
7. Add captions, audio, SFX, music, transitions, and image motion.
8. Preview and inspect before rendering.
9. Render only after the editable timeline is usable.
10. Save renders under the project package.

## Commands

Run commands from the composition directory, not from a single HTML file path.

```powershell
npx hyperframes lint
npx hyperframes validate
npx hyperframes inspect
```

Use `npx hyperframes inspect --json` when you need machine-readable layout issues.

For TTS or transcription through HyperFrames:

```powershell
npx hyperframes tts "Your script here" --voice af_nova --output narration.wav
npx hyperframes transcribe narration.wav
```

## Quality Checks

- `index.html` exists in the project directory.
- Text has stable dimensions and no overflow.
- Every animated element has a correct final layout before motion.
- Animations are attached to the seekable timeline.
- Captions are synced and readable.
- Transitions do not flash black or expose unstyled frames.
- `npx hyperframes lint` passes.
- `npx hyperframes validate` passes or warnings are intentionally handled.
- `npx hyperframes inspect` passes for substantial compositions.

## Handoff

- Hand final renders to `skills/video-use` when transcript-aware finishing or final MP4 assembly is needed.
- Hand editable timeline folders back to the user for preview and revision.
- In story workflows, keep HyperFrames files inside `asset/<Story Name>/video/hyperframes/`.
