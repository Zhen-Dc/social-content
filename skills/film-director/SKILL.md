---
name: film-director
description: Direct cinematic AI-video scenes like a working film director. Use when the user wants script-to-screen direction, scene coverage, actor blocking, camera/lens/light/sound decisions, production shotlists, Higgsfield or Seedance prompts, image/reference planning, continuity repair, or a full director package from a screenplay, rough scene idea, story chapter, or single prompt request.
---

# Film Director

Read `SOP.md` before using this skill independently. It defines the directing workflow, asset locations, output contracts, QA checks, and handoff rules.

Use this skill as the directing layer above prompt writing. Treat the work as a real director would: interpret dramatic intent, design the scene, control actors and camera, protect continuity, and produce assets the generation pipeline can execute.

This skill combines two source systems:
- `references/shotlist-builder-source/` for screenplay-to-shotlist workflow, asset requests, spatial blocking, HTML production output, prompt density, style blocks, camera-emotion sync, and micro-beat performance direction.
- `references/seedance-2-pro-director-source/SKILL.md` for single-shot Seedance 2.0 prompt control, character anchoring, screen coordinates, reference roles, state locks, motion hierarchy, final-frame control, and QA.

## Routing

Classify the request before producing output.

- **Single shot or prompt:** read `references/seedance-2-pro-director-source/SKILL.md`; produce a director interpretation, spatial map, final prompt, constraints, and QA.
- **Scene direction without full screenplay:** use this SKILL.md plus Seedance source as needed; build a compact director package with performance, camera, lighting, sound, and prompt-ready shot blocks.
- **Full script, chapter, screenplay, or multi-scene breakdown:** read `references/shotlist-builder-source/SKILL.md`; follow its phased process and supporting references. Do not skip asset planning or spatial blocking.
- **Shotlist HTML or production table:** read `references/shotlist-builder-source/SKILL.md` and its `templates/HTML_TEMPLATE.md`.
- **Fix an existing prompt/shotlist:** diagnose the failure mode first, then edit the artifact or rewrite only the broken blocks.

Ask a question only when a missing choice changes the direction materially: genre, scene scope, asset identity, ambiguous reference mapping, or a generic emotion with multiple physical meanings. Otherwise make strong directorial choices.

## Director Workflow

### 1. Interpret the scene

Extract the director's intent before touching prompts:
- story function: what changes in the scene
- emotional objective: what the audience should feel by the final frame
- focal character: whose psychology drives the camera
- conflict: what visual pressure exists between people, objects, space, or time
- visual promise: the one image the scene must deliver

Do not simply restate the user's plot. Translate it into playable, visible decisions.

### 2. Choose the format

Pick the smallest format that solves the user's request:
- **Director's note:** short interpretation plus visual approach.
- **Scene plan:** blocking, performance, camera, lighting, sound, and 3-8 shot beats.
- **Prompt package:** one or more generation-ready prompts with reference roles and QA.
- **Shotlist:** table or HTML with shot rows, duration, lens, movement, action, performance, prompt text, and continuity warnings.
- **Production pass:** revise existing prompts, repair continuity, improve acting beats, or reduce overloaded shots.

### 3. Build assets and references

For multi-scene work, list required references before writing prompts:
- characters, costumes, variants, wounds, age states
- locations and time-of-day variants
- hero props, readable documents, screens, vehicles, weapons
- style references, lighting references, composition references
- video/audio references and exactly what each controls

Never auto-assign ambiguous files. Use explicit mappings such as: `Image 1 controls Character A identity; Image 2 controls costume; Image 3 controls room layout; Video 1 controls camera movement only`.

### 4. Lock blocking

For every important frame, define:
- screen position: left third, center, right third, or x/y percentage
- depth: foreground, midground, background
- body orientation and eyeline
- distance between characters or between character and prop
- contact points: feet, hands, chair, wall, table, vehicle
- crossing rules: who may move, who must not swap sides
- final frame composition

For any multi-character scene or key prop placement, create or request a top-down blocking map before final prompts. Use `references/shotlist-builder-source/reference/SPATIAL_BLOCKING.md` when detailed schema rules are needed.

### 5. Direct performance

Never leave generic emotions in the prompt. Convert them into actor notes:
- muscles: jaw, brow, nostrils, eyelids, lips, neck, shoulders
- breath: inhale, held breath, swallow, release
- gaze: locked, avoided, delayed, shifted to a specific point
- timing: pre-line beat, during-line emphasis, post-line hold
- restraint: what the actor is trying not to reveal

For complex emotions, use `references/shotlist-builder-source/reference/MICRO_BEATS.md`. If the user says "surprised", "sad", "angry", "tense", "scared", or "in love" and the variant is unclear, offer 3-4 physical variants and ask the user to pick.

### 6. Make the camera the emotional double

Choose camera, lens, and movement from the focal character's emotional state:
- anger or tension: handheld breathing, irregular micro-drift, no fake chaos
- control or confidence: smooth, restrained handheld or locked composure
- vulnerability: slow, low, softened movement
- shock or revelation: freeze, then a very slow push or pull
- action: clear motion, readable geography, no over-cut confusion
- final verdict: held frame or top-shot freeze when appropriate

Use `references/shotlist-builder-source/reference/CAMERA_EMOTION.md` when mapping camera to emotion in detail.

### 7. Write executable prompts

For Seedance-style prompts, use this order:

1. Output settings: duration, aspect ratio, mode, number of shots.
2. Reference plan: what each image, video, or audio file controls.
3. Spatial blocking: frame zones, depth, distance, eyelines, crossing rules.
4. Character anchors: identity, costume, pose, state, contact points, locks.
5. Action: one dominant action per shot or timed block.
6. Motion hierarchy: subject, internal motion, camera, environment.
7. Camera: shot size, angle, lens, movement, focus, composition.
8. Environment and production design.
9. Lighting and color, motivated by visible sources.
10. Audio: ambience, Foley, dialogue, music, silence.
11. Continuity constraints and final frame.

Prefer positive constraints over negative prompts. Instead of "no drifting", write "her boots stay planted on the same floor marks while only her eyes, breathing, and coat fabric move."

### 8. Protect complexity

One shot gets one main idea, one main action, and one main camera strategy. Split the scene when it has:
- more than two strong actions
- more than two camera moves
- more than three important characters
- a major location change
- a complex transformation, fight, chase, or VFX event

Use 4-8 seconds for one strong action, 8-12 seconds for action plus reveal, and 12-15 seconds for 2-3 simple timed beats.

## Output Contracts

### Director package

Use this when the user wants a scene directed but not necessarily a full HTML shotlist:

```markdown
## Director's Interpretation
[What the scene must do emotionally and dramatically.]

## Visual Strategy
- Genre/texture:
- Focal character:
- Camera principle:
- Lighting principle:
- Sound principle:
- Final image:

## Blocking
[Screen zones, depth, eyelines, contact points, movement limits.]

## Performance Direction
[Specific actor beats, breath, gaze, physical restraint, dialogue timing.]

## Shot Plan
| Shot | Duration | Lens/Camera | Action | Performance | Continuity |
|---|---:|---|---|---|---|

## Generation Prompts
[Seedance/Higgsfield-ready prompt blocks.]

## QA
[Identity, position, state, motion, camera, audio, final frame, failure risks.]
```

### Single-shot Seedance output

Use this when the user asks for one prompt:

```markdown
## Director's Interpretation
## Spatial Blocking Map
## Reference Plan
## Final Seedance 2.0 Prompt
## Positive Constraints
## QA Checklist
```

### Full shotlist output

For full screenplay work, follow the source shotlist builder's phase order:
1. read script
2. output asset request
3. wait for uploaded assets and scope
4. confirm spatial blocking
5. generate shotlist/table/HTML

Do not collapse these phases unless the user explicitly asks for a quick draft without assets.

## QA Checklist

Before final delivery, verify:
- the scene has a clear dramatic turn
- every character has identity, position, state, pose, eyeline, and contact points
- the camera choice matches the focal emotion
- performance notes are physical, not generic adjectives
- reference roles are explicit
- prompt complexity is split when needed
- positive constraints lock continuity
- final frame is specific
- sound is either intentionally designed or intentionally minimal
- any HTML/table artifact is saved as a file, not only pasted in chat

If a prompt reads like a template, rewrite it until it feels like notes from a director who has watched the rehearsal.
