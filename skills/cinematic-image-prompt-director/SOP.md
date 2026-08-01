# SOP: Cinematic Image Prompt Director

## Purpose

Use this SOP to create production-ready still-image prompts for story scenes, character sheets, thumbnails, posters, reference frames, ComfyUI images, Kie/Nano Banana images, fal.ai images, or image-to-video keyframes.

This skill produces prompts and prompt packages. It does not generate images by itself.

## Skill Files

- Skill folder: `C:\Social Content\skills\cinematic-image-prompt-director`
- Main instructions: `SKILL.md`
- Prompt reference: `references\prompt-patterns.md`

## Inputs Needed

- Scene, chapter, script excerpt, or rough visual idea.
- Target output type: single prompt, prompt pack, character reference, location reference, thumbnail, poster, or keyframe.
- Platform/model if known: ComfyUI, Kie, Nano Banana, fal.ai, SD-style, or generic.
- Aspect ratio and style.
- Character continuity details when the prompt is part of a series.

## Where To Save Assets

Save prompt artifacts beside the project they support:

```text
asset/<Story Name>/image-prompts.md
asset/<Story Name>/character-bible.json
asset/<Story Name>/scene-beats.json
```

For general reusable prompt work, use:

```text
Asset/prompts/
```

For generated images made later by ComfyUI, save outputs under:

```text
asset/<Story Name>/images/
Asset/images/
```

Do not save prompts only in chat when they are part of a production package. Write the prompt file.

## Workflow

1. Read `SKILL.md`.
2. Read `references/prompt-patterns.md` when the user needs reusable prompt formulas, prompt packs, or model-specific variants.
3. Identify the image's job: story beat, character identity, location, thumbnail, poster, insert, or video keyframe.
4. Build continuity locks before writing the prompt.
5. Specify character identity, facial imperfections, skin texture, hair, wardrobe, props, and environment.
6. Specify camera, lens feel, framing, lighting, color, texture, and production design.
7. Write a clean positive prompt and a separate negative prompt when the target model supports one.
8. Add aspect ratio, seed guidance, model notes, and continuity warnings.
9. QA for contradictions before handing the prompt to an image generator.

## Character Continuity Requirements

For recurring story characters, document:

- replacement name and role
- age range
- face shape and distinctive imperfections
- complexion and skin texture
- hair color, texture, and style
- exact clothing color, garment type, fit, fabric, and accessories
- repeated props
- emotional baseline
- allowed changes by scene

## Prompt Output Contract

For each prompt include:

```text
Prompt title:
Purpose:
Aspect ratio:
Positive prompt:
Negative prompt:
Continuity locks:
Model notes:
Failure risks:
```

## Quality Checks

- One dominant subject and one visual goal.
- Clothing and identity match the character bible.
- Emotion is described with visible physical acting, not a generic adjective.
- Camera and lighting do not contradict each other.
- The prompt can be pasted into the target generator without extra explanation.
- Negative prompt removes likely failures without fighting the positive prompt.

## Handoff

- Hand still-image prompts to `skills/comfyui-media-generator`.
- Hand full scene direction or shot planning to `skills/film-director`.
- Hand final image assets to `skills/hyperframes` or `skills/video-use` for video composition.
