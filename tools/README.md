# Tool Route Map

This workspace follows WAT. Root `tools/` can hold deterministic wrappers, while the current production scripts live inside project-local skill folders.

## Active Tool Routes

- Strict story-video pipeline gatekeeper: `tools/story_video_pipeline.py`
- Web scraping: `skills/webscraper/scripts/web_scraper.py`
- Story-time packaging: `skills/story-time-rewriter/scripts/story_time_package.py`
- Chatterbox TTS: `skills/chatterbox-tts/scripts/chatterbox_tts.py`
- ComfyUI API submission: `skills/comfyui-media-generator/scripts/comfyui_api.py`

Use `story_video_pipeline.py doctor`, `plan`, and `status` before resuming a story-video package. Use `run-stage` or `run-all` only when the previous gate is complete. The runner treats `screenwriter` and `shotlist-builder` as external/global skills and requires their local handoff artifacts before continuing.

Before adding a new root tool, check whether a project skill already has the script.
