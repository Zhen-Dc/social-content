# Agent Instructions

This workspace follows the WAT framework: Workflows, Agents, Tools.

## WAT Operating Model

### Workflows

Workflows are Markdown SOPs in `workflows/`. They define the objective, required inputs, approved skill/tool route, output folders, quality checks, and failure handling.

For picture-based narration videos, use:

```text
workflows/picture-narration-story-video-sop.md
```

### Agents

The agent coordinates the work. Read the relevant workflow first, then route each stage to the correct local skill or deterministic script. Do not manually improvise around a stage when an existing project skill or script handles it.

### Tools

Deterministic execution lives in local scripts. In this workspace, most production tools are currently bundled inside skill folders under `skills/*/scripts/`; `tools/README.md` maps the active tool routes.

## Core Rule

Use AI reasoning for story decisions, directing, prompt quality, and creative continuity. Use deterministic tools for scraping, packaging, TTS generation, ComfyUI submission, timeline assembly, and rendering wherever a local script exists.

## Social Story Video Route

When the user asks for social media videos made from pictures plus narration, use the strict local pipeline first:

```text
tools/story_video_pipeline.py doctor
tools/story_video_pipeline.py --story-name "<Story Name>" status
tools/story_video_pipeline.py --story-name "<Story Name>" plan
```

Project skills are folders under `C:\Social Content\skills`, not guaranteed global `$skill` commands. Read each `SKILL.md` and run local scripts directly.

Route through:

1. `skills/webscraper`
2. `skills/story-time-rewriter`
3. external/global `screenwriter` and `shotlist-builder`, or equivalent local artifacts
4. `skills/chatterbox-tts`
5. `skills/film-director`
6. `skills/comfyui-media-generator`
7. `skills/hyperframes`
8. `skills/video-use`

Keep the work editable until the user approves the final render. Do not continue after a failed pipeline gate.
