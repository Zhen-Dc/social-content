# SOP: Film Director

## Purpose

Use this SOP to direct cinematic scenes, shotlists, image prompts, or video-generation prompt packages. This skill is the directing layer above prompt writing.

It is for deciding dramatic intent, blocking, performance, camera, lighting, sound, continuity, and prompt structure.

## Skill Files

- Skill folder: `C:\Social Content\skills\film-director`
- Main instructions: `SKILL.md`
- Director package template: `templates\director-package.md`
- Shotlist source: `references\shotlist-builder-source\SKILL.md`
- Seedance source: `references\seedance-2-pro-director-source\SKILL.md`

## Inputs Needed

- Scene idea, script excerpt, chapter, screenplay, or rough prompt.
- Desired output: director note, scene plan, prompt package, shotlist, HTML shotlist, or repair pass.
- Target generator if known: Seedance, Higgsfield, ComfyUI stills, or generic.
- Available character, location, prop, style, image, audio, or video references.
- Runtime, aspect ratio, platform, and final use when known.

## Where To Save Assets

For story projects:

```text
asset/<Story Name>/director/
  director-package.md
  shotlist.md
  blocking-map.md
  generation-prompts.md
```

For image-based story video packages:

```text
asset/<Story Name>/scene-beats.json
asset/<Story Name>/character-bible.json
asset/<Story Name>/image-prompts.md
```

For general reusable direction work:

```text
Asset/director/
```

If an HTML shotlist is produced, save it as a file in the project package instead of only pasting it in chat.

## Workflow

1. Read `SKILL.md`.
2. Classify the request:
   - single prompt or single shot
   - scene plan
   - full script or multi-scene shotlist
   - repair of an existing prompt or shotlist
3. Read the relevant source reference based on the classification.
4. Identify the scene's dramatic turn, focal character, conflict, and final image.
5. Build or request character, costume, location, prop, and style references.
6. Lock spatial blocking before writing generation prompts.
7. Convert generic emotions into physical acting notes.
8. Choose camera and lighting based on the focal character's emotion.
9. Write the director package, shot plan, or prompts.
10. QA continuity, prompt complexity, final frame, and sound.

## Required Directing Detail

For every important scene include:

- story function
- focal character
- emotional objective
- screen position and depth
- body orientation and eyeline
- physical distance between characters
- contact points with floor, chair, wall, table, or prop
- performance micro-beats
- lens feel, shot size, angle, and camera movement
- motivated lighting and color
- sound, silence, Foley, or music cue
- continuity risks

## Output Contract

For a director package, include:

```text
Director's Interpretation
Visual Strategy
Blocking
Performance Direction
Shot Plan
Generation Prompts
QA
```

For a single prompt package, include:

```text
Director's Interpretation
Spatial Blocking Map
Reference Plan
Final Prompt
Positive Constraints
QA Checklist
```

## Quality Checks

- Scene has a clear dramatic turn.
- Character positions and eyelines are unambiguous.
- Performance notes describe muscles, breath, gaze, posture, and restraint.
- Camera choice matches emotion.
- Prompt is split if one shot has too many actions or camera moves.
- References have explicit roles.
- Final frame is specific.
- Sound is intentionally designed or intentionally minimal.

## Handoff

- Send still-image prompts to `skills/cinematic-image-prompt-director` or `skills/comfyui-media-generator`.
- Send story video scene plans to `skills/social-story-video-maker`.
- Send timeline-ready scene plans to `skills/hyperframes`.
