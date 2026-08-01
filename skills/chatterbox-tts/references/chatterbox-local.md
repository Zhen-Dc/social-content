# Local Chatterbox Notes

Install root:

```text
C:\Ai Tools\Chatterbox -TTS with Turbo\Chatterbox TTS with Turbo
```

Important paths:

- Embedded Python: `python\python.exe`
- Chatterbox source package: `src\chatterbox`
- Sample voice folder: `modules\voice_samples`
- Workspace voice samples and persona aliases: `C:\Social Content\Asset\voices`
- Gradio launcher: `Run Chatterbox TTS.bat`

Backend facts:

- `app.py` exposes a Gradio UI, but no stable API names are assigned to the generation handlers.
- `modules\generation_functions.py` calls the backend models, but importing it also imports `modules.config`, which prints emoji and imports multilingual support at import time. On Windows consoles this can fail without UTF-8 output and can be slow.
- The skill wrapper imports `chatterbox.tts` and `chatterbox.tts_turbo` directly from `src`, avoiding Gradio and avoiding the heavy UI modules until generation is actually needed.
- Built-in sample voices are files in `modules\voice_samples`. Some files have `.wav` names but MP3-style headers; this is okay because Chatterbox loads prompts through librosa.
- Turbo reference prompts should generally be longer than 5 seconds. If Turbo rejects a short prompt, choose another built-in voice or use the standard `tts` model.
- Set `NUMBA_CACHE_DIR` to `C:\Social Content\.tmp\numba-cache` before importing Chatterbox. Without this, librosa/numba can hang while creating cache files in the default Windows temp area.

Current conservative default:

```text
Paul_male
```

Persona routing:

```text
young woman -> Rho_female
young man -> Tayo_male
middle aged woman -> Ngozi_female
middle aged man -> Ejike_male
little girl / little girls -> Bonnie_female
little boy / little boys -> Ade_male
old woman -> Morganna_female
old man -> Joje_male
```

Use user-supplied voice samples only when the user has rights/permission to use that voice. Avoid presenting generated audio as a real person's authentic speech unless the user explicitly has consent and the output is clearly labeled.
