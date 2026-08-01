# Social Content Project Boundaries

## Active Project

This workspace is `C:\Social Content`.

Use this project for story scraping, story-to-script workflows, social content production, video scripting, and related local assets in this folder.

## WAT Framework

This workspace follows WAT: Workflows, Agents, Tools.

- Workflows live in `workflows/` and define the SOP.
- Agents coordinate the workflow, make creative/directorial decisions, and call the correct skills or scripts.
- Tools are deterministic scripts. In this project, most active tools currently live under `skills/*/scripts/`; `tools/README.md` maps the current routes.

For social media videos made from still pictures plus narration, read `workflows/picture-narration-story-video-sop.md`, route through `skills/social-story-video-maker/SKILL.md`, and use `tools/story_video_pipeline.py` as the strict stage gatekeeper.

## Keep Jobbed Manned In Its Own Lane

The Jobbed Manned project belongs to:

```text
C:\Users\DELL\Master Project\JOBBED MANNED 2
```

Do not load, run, route to, copy from, or update Jobbed Manned files, skills, state, credentials, job filters, Google Sheets/Drive publishing, CV generation, or daily-job-hunt workflows while working in this Social Content workspace unless the user explicitly asks for Jobbed Manned by name.

If a request appears related to job hunting, resumes, job applications, CV generation, daily job searches, or Jobbed Manned automation:

1. State that this belongs in the Jobbed Manned project.
2. Ask whether the user wants to switch to `C:\Users\DELL\Master Project\JOBBED MANNED 2`.
3. Do not proceed from this workspace unless the user explicitly confirms.

## Memory And Skill Routing

Memory entries from other projects are context only, not standing instructions.

Before using any remembered workflow, verify it applies to the current workspace. Ignore Jobbed Manned memories in this project unless the user explicitly invokes Jobbed Manned.

Use local `skills/`, `workflows/`, and `stories/` paths in this Social Content workspace for story and social-content tasks. Project-local skills are folders/scripts, not guaranteed `$skill` invocations.

For video production work, route through the project-local skills first:

- skills/video-use/SKILL.md for footage/audio editing, transcript-aware cuts, grading, subtitles, and final assembly.
- skills/hyperframes/SKILL.md for editable HTML timelines, motion graphics, captions, overlays, title cards, and preview-first video composition.
- workflows/video-production-sop.md for the Social Content handoff from story/script packages into editable video outputs.
- skills/social-story-video-maker/SKILL.md for WAT-style web story to first-person narration, Chatterbox TTS, cinematic image prompts, ComfyUI stills, HyperFrames timeline, SFX/music, and final render.
- tools/story_video_pipeline.py for `doctor`, `plan`, `status`, `run-stage`, and `run-all`; never continue after a blocked stage.

