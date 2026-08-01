---
name: cinematic-image-prompt-director
description: Create detailed cinematic image-generation prompts for AI art, story visuals, character sheets, scene stills, posters, thumbnails, reference frames, and image-to-video keyframes. Use when the user asks for image prompts, detailed prompts, Nano Banana/Kie/ComfyUI/fal.ai prompts, character or location references, visual style prompts, prompt repair, prompt expansion, or prompt packs for film, story, social, or video projects.
---

# Cinematic Image Prompt Director

Read `SOP.md` before using this skill independently. It defines the prompt workflow, prompt file locations, continuity requirements, QA checks, and handoff rules.

Use this skill to turn ideas, scripts, scenes, chapters, or rough visual notes into production-grade image prompts. Act like a visual director: define what the image must communicate, then specify subject, camera, light, composition, texture, continuity, and model constraints.

This skill is the still-image layer below `film-director`. Use `film-director` for full scene direction and shot planning; use this skill when the deliverable is one or more still-image prompts or image reference frames.

## Routing

Choose the smallest useful output:

- **Single prompt:** one polished final prompt plus negative prompt and model notes.
- **Prompt pack:** 3-8 alternate prompts for character, location, poster, thumbnail, insert, or keyframe use.
- **Continuity reference:** locked character/location prompt with repeatable identity, costume, props, and palette.
- **Prompt repair:** diagnose a weak prompt, then rewrite it with stronger visual hierarchy.
- **Image-to-video keyframe:** create a still prompt that can anchor a video generation shot.

If the user provides a script or full scene and asks for directing decisions, route through `film-director` first, then convert the chosen shot or visual promise into image prompts.

## Workflow

1. **Find the visual job.** Decide whether the image is a character reference, scene still, establishing shot, prop insert, poster, thumbnail, mood frame, or image-to-video keyframe.
2. **Extract continuity anchors.** Lock identity, age, body type, wardrobe, wounds, props, environment, time of day, color palette, and any reference-image roles.
3. **Choose the camera.** Specify shot size, angle, lens feeling, depth of field, focus target, and framing. Avoid vague "cinematic" without visible camera choices.
4. **Design the light.** Name the motivated light source, direction, contrast level, color temperature, shadows, and atmosphere.
5. **Direct the pose and emotion.** Convert emotions into physical details: gaze, jaw, shoulders, hands, breath, posture, distance, tension, and restraint.
6. **Add production design.** Include set dressing, textures, era, weather, materials, clutter level, and visual symbolism only when it serves the image.
7. **Write model-ready output.** Provide a clean final prompt, negative prompt, aspect ratio, generation notes, and continuity warnings.
8. **QA the prompt.** Check that the prompt has one clear subject, a readable composition, locked continuity, and no contradictory style/camera instructions.

## Prompt Anatomy

Use this order for final prompts:

1. Image type and aspect ratio.
2. Primary subject and identity anchors.
3. Action, pose, gaze, and emotion.
4. Environment and time of day.
5. Composition and screen placement.
6. Camera, lens, depth of field, and focus.
7. Lighting, color palette, atmosphere.
8. Texture, wardrobe, props, and production design.
9. Style boundary: photoreal, editorial, cinematic still, concept art, poster, thumbnail, etc.
10. Continuity locks and exclusions.

Prefer concrete visual language over long adjective chains. Replace "beautiful cinematic dramatic scene" with physical details such as "low-angle 35mm frame, rain beads on her black coat, sodium streetlight from camera left, face half-shadowed, eyes fixed past the lens."

## Output Contracts

### Single Image Prompt

```markdown
## Visual Intent
[What the image must communicate.]

## Continuity Anchors
- Subject:
- Wardrobe/props:
- Location:
- Palette:
- Reference roles:

## Final Prompt
[Detailed image-generation prompt.]

## Negative Prompt
[Artifacts, wrong identity, extra limbs, text/logos, unwanted style drift, bad anatomy, continuity errors.]

## Model Notes
- Aspect ratio:
- Best use:
- If using image references:
- Continuity risks:
```

### Prompt Pack

```markdown
## Prompt Pack Strategy
[How the prompts work together.]

| Prompt | Use | Aspect | Visual Goal |
|---|---|---:|---|

## Prompts
### 1. [Name]
- Prompt:
- Negative prompt:
- Continuity notes:
```

### Prompt Repair

```markdown
## Diagnosis
- Missing:
- Contradictory:
- Too vague:
- Continuity risk:

## Rewritten Prompt
...

## Why This Works
...
```

## Model-Specific Notes

- **Kie / Nano Banana:** prioritize concise visual hierarchy, exact subject identity, reference-image roles, and clear style boundaries.
- **ComfyUI / SD-style workflows:** include a clean positive prompt, a separate negative prompt, aspect ratio, seed/variation guidance if requested, and avoid contradictory tag piles.
- **fal.ai media workflows:** include model intent and output size; ask before paid generation or credit-consuming runs.
- **Image-to-video:** include a stable starting frame, visible motion potential, clear final-frame intention, and avoid overloading the still with multiple actions.

Read `references/prompt-patterns.md` when the user needs reusable prompt formulas, prompt packs, or model-specific variants.

## Quality Gate

Before final delivery, verify:

- the prompt has one dominant subject and one visual goal
- identity, costume, props, and location are repeatable
- emotion is physical, not generic
- composition says where the subject sits in frame
- light has a visible source and direction
- camera/lens instructions do not conflict
- style is specific enough to guide generation
- negative prompt removes likely failure modes without fighting the positive prompt
- model notes tell the next agent how to generate or iterate
