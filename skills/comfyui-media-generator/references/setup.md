# ComfyUI Portable Setup

## Project Paths

- Project root: `C:\Social Content`
- Portable root: `C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable`
- ComfyUI root: `C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI`
- Embedded Python: `C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\python_embeded\python.exe`
- Image assets: `C:\Social Content\Asset\images`
- Video/audio assets: `C:\Social Content\Asset\videos`

## Old Desktop Model Source

ComfyUI Desktop shared models were found at:

```text
C:\Users\DELL\AppData\Local\Comfy-Desktop\ComfyUI-Shared\models
```

Important local model files found there:

- `diffusion_models\krea2_turbo_fp8_scaled.safetensors`
- `diffusion_models\z_image_turbo_bf16.safetensors`
- `loras\krea2_darkbrush.safetensors`
- `text_encoders\qwen_3_4b.safetensors`
- `text_encoders\qwen3vl_4b_fp8_scaled.safetensors`
- `vae\ae.safetensors`
- `vae\qwen_image_vae.safetensors`

Because C: drive free space was limited, the initial portable migration copied only:

- `krea2_turbo_fp8_scaled.safetensors`
- `krea2_darkbrush.safetensors`
- `qwen3vl_4b_fp8_scaled.safetensors`
- `ae.safetensors`

Later Krea2 testing showed `ae.safetensors` is the Flux.1 autoencoder and produces grid-like artifacts when used with local Krea2. Copy this VAE from ComfyUI Desktop into portable before local Krea2 image generation:

```text
C:\Users\DELL\AppData\Local\Comfy-Desktop\ComfyUI-Shared\models\vae\qwen_image_vae.safetensors
```

Portable destination:

```text
C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\models\vae\qwen_image_vae.safetensors
```

## Questions To Ask Before Generation

Ask what is missing:

1. Media type: image, audio, video, or image-to-video?
2. Prompt and negative prompt?
3. Model/workflow: Krea 2, Flux Krea, Z-Image, Qwen, Wan, LTX, Stable Audio, or existing workflow JSON?
4. Aspect ratio and resolution?
5. Number of outputs?
6. Seed: random or fixed?
7. Style references or LoRA strength?
8. Where should final outputs go if not `Asset`?

## Operating Rules

- Use portable ComfyUI, not ComfyUI Desktop.
- Do not uninstall Desktop until portable has generated successfully with the needed model.
- Prefer exact workflow JSON from the Desktop app if available.
- If a blueprint references model files that are not present, either copy those files, choose another local workflow, or ask the user before downloading.
- Save successful outputs into `Asset\images` or `Asset\videos`.

## Current Runtime Finding

As of 2026-06-29, portable ComfyUI starts successfully in GPU mode with `8190` as the preferred port:

```text
http://127.0.0.1:8190
```

Start it with the safe launcher. The launcher prefers `8190`, falls back through `8191`-`8199` if a port is busy or unhealthy, and saves the chosen server URL to `C:\Social Content\.tmp\comfyui_server.json`.

```powershell
& "C:\Social Content\skills\comfyui-media-generator\scripts\start_comfyui_portable.cmd"
```

Do not use `Start-Process` directly for this portable launch on this machine. PowerShell can crash with `Item has already been added. Key in dictionary: 'Path' Key being added: 'PATH'` because the inherited environment contains duplicate path keys. The safe launcher uses .NET `ProcessStartInfo`, normalizes the child `PATH`, starts hidden, and waits for `/system_stats` on the selected port. The `.cmd` wrapper runs the PowerShell launcher with `-ExecutionPolicy Bypass`, because direct `.ps1` execution is blocked on this Windows profile.

The API helper defaults to `--server auto`. It first checks `.tmp\comfyui_server.json`, then scans `8190`-`8199`, so image generation follows the port that actually launched.

The bundled portable PyTorch was replaced because `2.12.0+cu130` did not support the Quadro P5200 `sm_61` GPU. The working install is:

```text
torch 2.7.0+cu118
torchvision 0.22.0+cu118
torchaudio 2.7.0+cu118
```

Verification output showed CUDA available, the Quadro P5200 selected as `cuda:0`, and the PyTorch CUDA arch list included `sm_61`.

The tiny local Krea test workflow at:

```text
C:\Social Content\Asset\workflows\krea2-local-test-api.json
```

generated successfully and copied the output to:

```text
C:\Social Content\Asset\images\social_content_krea2_test_00001_.png
```

This was a low-resolution smoke test, not a final production image. Later tests showed the smoke workflow used the wrong VAE for Krea2, producing grid artifacts.

The corrected local Krea2 workflow uses:

- `UNETLoader`: `krea2_turbo_fp8_scaled.safetensors`
- `CLIPLoader`: `qwen3vl_4b_fp8_scaled.safetensors`, type `krea2`
- `VAELoader`: `qwen_image_vae.safetensors`

Corrected API workflow:

```text
C:\Social Content\Asset\workflows\nigerian-boy-playing-in-mud-krea2-api-fixed-qwen-vae-512.json
```

Corrected output:

```text
C:\Social Content\Asset\images\comfyui_nigerian_boy_playing_in_mud_fixed_qwen_vae_512_00001_.png
```

Possible next fixes:

- Build a higher-quality Krea image workflow now that the GPU path is working.
- Use a paid/cloud Krea API node only after the user approves any account/auth/cost requirement.
- Keep ComfyUI Desktop installed until the user confirms the portable setup covers the needed image/video workflows.
