# Repository Guidelines

## Project Structure & Module Organization

This repository is a Windows-first social content workspace built around WAT: Workflows, Agents, Tools. Root guidance lives in `CLAUDE.md`. SOPs live in `workflows/`, including `workflows/picture-narration-story-video-sop.md` for picture+narration story videos. Reusable capabilities live in `skills/<skill-name>/` with `SKILL.md`, `SOP.md`, optional `references/`, `scripts/`, and `agents/openai.yaml`. Deterministic helper routes are summarized in `tools/README.md`. Generated media belongs in `Asset/` or a project package such as `asset/<Story Name>/`; scraped story packages belong in `stories/<Story Name>/`.

For picture+narration story videos, use `tools/story_video_pipeline.py` as the strict stage gatekeeper. Project-local skills are folders/scripts, not guaranteed `$skill` commands.

## Build, Test, and Development Commands

Validate a skill after editing:

```powershell
& "C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\python_embeded\python.exe" "C:\Users\DELL\.codex\skills\.system\skill-creator\scripts\quick_validate.py" ".\skills\social-story-video-maker"
```

Run a scraper package:

```powershell
& "<python>" ".\skills\webscraper\scripts\web_scraper.py" --url "URL" --output-root ".\stories" --make-script
```

Inspect or resume a story-video package:

```powershell
& "<python>" ".\tools\story_video_pipeline.py" doctor
& "<python>" ".\tools\story_video_pipeline.py" --story-name "Story Name" status
& "<python>" ".\tools\story_video_pipeline.py" --story-name "Story Name" plan
```

Run HyperFrames checks from a composition directory:

```powershell
npx hyperframes lint
npx hyperframes validate
npx hyperframes inspect
```

## Coding Style & Naming Conventions

Use concise Markdown with actionable steps. Keep skill folders lowercase hyphen-case, for example `story-time-rewriter`. Keep generated story assets in stable, descriptive folders. Prefer PowerShell commands and explicit Windows paths. Use ASCII in new files unless an existing file requires Unicode.

## Testing Guidelines

There is no single global test suite. Validate edited skills with `quick_validate.py`. For script changes, run the smallest representative command and inspect output files. For video or HyperFrames work, verify layout and renderability before final output.

## Commit & Pull Request Guidelines

Git history is not currently readable in this checkout, so no local commit convention can be inferred. Use clear imperative commit messages such as `Add SOP for Chatterbox TTS`. PRs should describe changed workflows, list touched skills/scripts, include validation commands run, and attach screenshots or render paths for media changes.

## Security & Configuration Tips

Do not commit secrets, API keys, voice samples, or large generated renders unless explicitly required. Keep credentials in `.env` or the user-approved local tool location. Preserve source rights notes in `metadata.json` before adapting scraped stories.
