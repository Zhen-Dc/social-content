# SOP: ComfyUI Media Generator

## Purpose

Use this SOP to generate images, video, or audio through the portable ComfyUI setup in `C:\Social Content`.

This SOP is independent. It covers backend/API generation, asset saving, workflow reuse, and basic verification.

## Skill And Tool

- Skill folder: `C:\Social Content\skills\comfyui-media-generator`
- Main instructions: `SKILL.md`
- Setup reference: `references\setup.md`
- API helper: `scripts\comfyui_api.py`
- Safe launcher: `scripts\start_comfyui_portable.cmd`
- Portable ComfyUI root: `C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable`
- ComfyUI app root: `C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI`
- Embedded Python: `C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\python_embeded\python.exe`

## Inputs Needed

- Media type: image, video, or audio.
- Prompt and optional negative prompt.
- Workflow JSON or model/style preference.
- Aspect ratio or resolution.
- Output count.
- Seed policy: fixed seed or random variations.
- Target save folder.

## Where To Save Assets

For general project assets:

```text
Asset/images/
Asset/videos/
Asset/workflows/
```

For story video packages:

```text
asset/<Story Name>/images/
asset/<Story Name>/comfyui-workflows/
asset/<Story Name>/video/renders/
```

Keep original ComfyUI outputs in:

```text
ComfyUI_windows_portable_nvidia/ComfyUI_windows_portable/ComfyUI/output/
```

Copy user-facing outputs into the appropriate `Asset/` or `asset/<Story Name>/` folder.

## Workflow

1. Read `SKILL.md`.
2. Read `references\setup.md` before moving models, starting ComfyUI, or changing model paths.
3. Confirm the prompt, workflow, aspect ratio, model, and output count.
4. Check whether ComfyUI is already running.
5. Start portable ComfyUI with `scripts\start_comfyui_portable.cmd` if needed. It prefers `8190`, then falls back through `8191`-`8199` and records the live server URL in `.tmp\comfyui_server.json`.
6. Submit the API workflow with `scripts\comfyui_api.py` when possible. Use the default auto server discovery unless a workflow needs a specific URL.
7. Copy completed outputs into the target asset folder.
8. Save the workflow JSON used for any successful generation.
9. Inspect the result and reject outputs with broken identity, hands, faces, text, clothing, or composition.

## Runtime Commands

Check the server:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8190/system_stats"
```

If the launcher used a fallback port, check the saved server instead:

```powershell
Get-Content "C:\Social Content\.tmp\comfyui_server.json"
```

Start ComfyUI:

```powershell
& "C:\Social Content\skills\comfyui-media-generator\scripts\start_comfyui_portable.cmd"
```

Submit an API workflow:

```powershell
& "C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\python_embeded\python.exe" "C:\Social Content\skills\comfyui-media-generator\scripts\comfyui_api.py" --workflow "C:\path\workflow_api.json" --asset-root "C:\Social Content\Asset" --kind image
```

## Current Krea Setup

Known Krea files in the portable setup:

```text
models\diffusion_models\krea2_turbo_fp8_scaled.safetensors
models\loras\krea2_darkbrush.safetensors
models\text_encoders\qwen3vl_4b_fp8_scaled.safetensors
models\vae\ae.safetensors
```

If a workflow asks for Flux.1 Krea Dev files, verify those exact filenames first.

## Quality Checks

- ComfyUI server responds before job submission on the saved or auto-discovered URL.
- Workflow JSON is API-compatible.
- Output exists in ComfyUI output and copied project folder.
- Prompt and workflow are saved for repeatability.
- Character identity, costume, eyeline, and scene mood match the prompt.
- Final filename clearly identifies scene or purpose.

## Handoff

- Send generated images to `skills\hyperframes` for editable still-image video composition.
- Send prompt or workflow failures back to `skills\film-director` or `skills\cinematic-image-prompt-director` for prompt repair.
- For story videos, keep final images under `asset/<Story Name>/images/` and workflow JSON under `asset/<Story Name>/comfyui-workflows/`.

## Failure Handling

- If the API is unreachable, run `scripts\start_comfyui_portable.cmd` and retry the server check.
- If a node or model is missing, inspect the workflow JSON and model folders before changing prompts.
- If output is poor but the workflow succeeds, improve prompt/directing first.
- If image continuity fails, update the character bible and regenerate only affected scenes.
- If generation uses paid or external services, ask before retrying credit-consuming runs.
