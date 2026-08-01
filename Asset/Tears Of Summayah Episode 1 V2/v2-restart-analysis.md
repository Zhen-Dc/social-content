# V2 Restart Analysis

## Current Package Read

V1 is complete according to `tools/story_video_pipeline.py`, but it is structurally too compressed for the story. The final video uses:

- 1 full narration file: `audio/narration-full.wav`
- 6 narration chunks
- 6 scene beats
- 6 generated images
- 1 HyperFrames composition
- 1 final MP4

The narration is 428.165 seconds, so each V1 image carries too much story:

- Scene 001: about 66 seconds
- Scene 002: about 35 seconds
- Scene 003: about 66 seconds
- Scene 004: about 59 seconds
- Scene 005: about 82 seconds
- Scene 006: about 119 seconds

That is why the video does not feel like a full story video. The still images do not change often enough to match the narrated actions, dialogue, reactions, memories, and emotional turns.

## Script Read

The edited script has 106 sentence-like narration beats. V1 grouped those into only 6 visual scenes. V2 should not use one image per full narration chunk. It should use a visual beat map inside each audio chunk.

The first v2 visual structure used 28 scenes. After reviewing the conversation-heavy middle section, v2 now uses 37 image beats. This is a practical middle path:

- More detailed than the six-scene compression.
- Still feasible for GPT image generation and HyperFrames rendering.
- Each scene has one clear action, emotional turn, or camera cut.
- Timings remain tied to the existing narration manifest.

## Conversation Camera Policy

Conversation scenes must not hold one wide shot throughout. V2 uses edit pairs and triples:

- Establishing family-room shot to orient geography.
- Speaker close-up when Mallam Ibrahim, Zahra, or Hajia Amina is talking.
- Listener reaction close-up when the emotional meaning is in silence.
- Over-the-shoulder or side-angle shots to show eyeline and power distance.
- Insert shots for inward narration, such as the university list, open book, or pillow grief.

## V2 Direction

V2 should keep:

- `original script/original.txt`
- `edited script/edited.txt`
- `edited script/name_map.json`
- `audio/narration-full.wav`
- `audio/narration-manifest.json`
- the existing character bible as the continuity base

V2 must rebuild:

- `scene-beats.json`
- `screenwriter/production-script.md`
- `shotlist/sentence-shotlist.md`
- `shotlist/asset-plan.md`
- `image-prompts.md`
- `director/scene-prompts.json`
- all images under `images/`
- `video/hyperframes/index.html`
- `output/final.mp4`
- `output/production_manifest.json`

## Key Fix

The HyperFrames timeline should use 37 image clips timed to the narration. The audio can remain continuous, but the visual layer must switch images at the v2 scene start times. Captions should also follow the v2 beat text instead of only six broad captions.

## Rights Note

Source rights remain unclear. V2 remains private internal review only until rights are cleared.
