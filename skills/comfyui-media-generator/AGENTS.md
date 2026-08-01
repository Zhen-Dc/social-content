# Repository Guidelines

## Project Structure & Module Organization

This skill lives at `C:\Social Content\skills\comfyui-media-generator` and is tied to the active project copy at `C:\Social Content`.

- `SKILL.md` is the main routing file for agents.
- `references\setup.md` documents the portable ComfyUI setup, model locations, runtime fixes, and known working workflows.
- `scripts\comfyui_api.py` submits ComfyUI API workflows and copies completed outputs into the project asset folders.
- `scripts\start_comfyui_portable.cmd` starts the portable server without the crashing direct `Start-Process` route. It prefers `8190`, falls back through `8191`-`8199`, and records the live URL in `.tmp\comfyui_server.json`.
- `agents\openai.yaml` stores agent-facing metadata.
- Generated media belongs in `C:\Social Content\Asset\images` or `C:\Social Content\Asset\videos`.
- Successful reusable workflow JSON files belong in `C:\Social Content\Asset\workflows`.

## Build, Test, and Development Commands

Start portable ComfyUI:

```powershell
& "C:\Social Content\skills\comfyui-media-generator\scripts\start_comfyui_portable.cmd"
```

Run an API workflow:

```powershell
& "C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\python_embeded\python.exe" "C:\Social Content\skills\comfyui-media-generator\scripts\comfyui_api.py" --workflow "C:\Social Content\Asset\workflows\workflow.json" --asset-root "C:\Social Content\Asset" --kind image
```

Validate Python syntax after script edits:

```powershell
& "C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\python_embeded\python.exe" -m py_compile "C:\Social Content\skills\comfyui-media-generator\scripts\comfyui_api.py"
```

## Coding Style & Naming Conventions

Use Python 3 style with four-space indentation, `snake_case` for functions and variables, and descriptive CLI option names. Keep workflow filenames lowercase and hyphenated, for example `random-africans-krea2-01.json`. Keep generated user-facing media prefixed with `comfyui_` when copied into `Asset`.

## Testing Guidelines

For script changes, run `py_compile` and at least one small ComfyUI API workflow. Verify the output file exists in `Asset\images` or `Asset\videos` and visually inspect image/video results when the change affects generation quality.

## Commit & Pull Request Guidelines

`C:\Social Content` is not currently a Git repository, so no local commit history convention is available. If this skill is later versioned, use concise Conventional Commits such as `feat: add qwen vae workflow` or `fix: handle comfyui timeout`. Pull requests should describe the workflow tested, list model or path changes, and include output screenshots for visual-generation changes.

## Agent-Specific Instructions

Use portable ComfyUI only. Do not switch to ComfyUI Desktop for generation. Do not tell the user to uninstall Desktop until the needed models are copied and a portable generation has succeeded. For Krea2 workflows, use `qwen_image_vae.safetensors`; `ae.safetensors` is a Flux VAE and can produce grid artifacts with local Krea2.
