---
name: comfyui-media-generator
description: Generate images, audio, and videos with the portable ComfyUI setup inside C:\Social Content. Use when the user asks to set up ComfyUI portable, migrate ComfyUI Desktop models, generate Krea/Flux/Qwen/Z-Image images, create audio or video through ComfyUI workflows, save media into Asset/images or Asset/videos, or manage reusable ComfyUI generation workflows.
---

# ComfyUI Media Generator

Read `SOP.md` before using this skill independently. It defines the ComfyUI API workflow, asset locations, runtime checks, QA checks, and failure handling.

## Workspace

Use this project copy:

```text
C:\Social Content
```

Portable ComfyUI:

```text
C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable
```

Generated assets:

```text
C:\Social Content\Asset\images
C:\Social Content\Asset\videos
```

## Core Workflow

1. Read `references/setup.md` before moving models, starting ComfyUI, or generating media.
2. For image generation, read `SOP.md` and follow its backend/API workflow.
3. Ask only the missing production questions: media type, prompt, aspect ratio, style/model, output count, and whether to use an existing workflow JSON.
4. Prefer the portable ComfyUI Python at `python_embeded\python.exe`.
5. Keep models inside the portable `ComfyUI\models\` tree unless a workflow explicitly uses `extra_model_paths.yaml`.
6. Start ComfyUI with `scripts/start_comfyui_portable.cmd` when the API is not already responding. It prefers port `8190`, falls back through `8191`-`8199`, records the live URL in `.tmp\comfyui_server.json`, avoids the duplicate `Path`/`PATH` crash seen with `Start-Process`, and bypasses local PowerShell script-policy blocking.
7. Generate outputs through the ComfyUI API when possible. Use `scripts/comfyui_api.py` to submit API workflows and copy completed files into the project `Asset` folders. Leave `--server` unset or use `--server auto` unless a specific server URL is required.
8. Save images to `Asset\images` and videos/audio to `Asset\videos` unless the user requests another path.
9. Do not tell the user to uninstall ComfyUI Desktop until the required models are copied and a generation has succeeded from the portable setup.

## Quick Commands

Start ComfyUI from the portable folder:

```powershell
& "C:\Social Content\skills\comfyui-media-generator\scripts\start_comfyui_portable.cmd"
```

Submit an API workflow:

```powershell
& "C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\python_embeded\python.exe" "C:\Social Content\skills\comfyui-media-generator\scripts\comfyui_api.py" --workflow "C:\path\workflow_api.json" --asset-root "C:\Social Content\Asset" --kind image
```

## Outputs

- Keep original ComfyUI outputs in `ComfyUI\output`.
- Copy final user-facing images into `Asset\images`.
- Copy final user-facing videos/audio into `Asset\videos`.
- Store workflow JSONs used for successful generations in `Asset\workflows` when useful.

## Current Krea Setup

The Krea-focused files copied from ComfyUI Desktop into portable are:

- `models\diffusion_models\krea2_turbo_fp8_scaled.safetensors`
- `models\loras\krea2_darkbrush.safetensors`
- `models\text_encoders\qwen3vl_4b_fp8_scaled.safetensors`
- `models\vae\ae.safetensors`

If a workflow asks for Flux.1 Krea Dev files, verify those exact filenames are present first. The bundled Flux Krea blueprint expects `flux1-krea-dev_fp8_scaled.safetensors`, `clip_l.safetensors`, `t5xxl_fp16.safetensors`, and `ae.safetensors`.
