# SOP: Chatterbox TTS

## Purpose

Use this SOP to generate narration, voice-over, character lines, or story audio with the local Chatterbox TTS install.

This SOP is independent. It can be used for any audio-only task or as the audio stage inside a larger social video workflow.

## Skill And Tool

- Skill folder: `C:\Social Content\skills\chatterbox-tts`
- Script: `C:\Social Content\skills\chatterbox-tts\scripts\chatterbox_tts.py`
- Reference: `C:\Social Content\skills\chatterbox-tts\references\chatterbox-local.md`
- Default Chatterbox install: `C:\Ai Tools\Chatterbox -TTS with Turbo\Chatterbox TTS with Turbo`

## Inputs Needed

- Text, text file, or narration chunks.
- Voice choice. If none is provided, list voices first and prefer `Paul_male` for fast English narration.
- Persona choice. Use the age/gender persona map when a narrator profile is specified.
- Output destination.
- Optional emotion tags such as `[sigh]`, `[laugh]`, or `[chuckle]`.
- Optional reference voice sample for registration.

## Where To Save Assets

Use the most specific project folder available:

```text
asset/<Story Name>/audio/
  narration-001.wav
  narration-002.wav
  narration-manifest.json
```

For general audio not tied to a story package, use:

```text
Asset/audio/chatterbox/
```

For user-provided voice samples, use:

```text
Asset/voices/
```

Never save generated audio inside the skill folder except for deliberate tool tests.

Persona aliases live at:

```text
Asset/voices/personas.json
```

Current narration persona map:

| Persona | Voice |
| --- | --- |
| young woman | `Rho_female` |
| young man | `Tayo_male` |
| middle aged woman | `Ngozi_female` |
| middle aged man | `Ejike_male` |
| little girl / little girls | `Bonnie_female` |
| little boy / little boys | `Ade_male` |
| old woman | `Morganna_female` |
| old man | `Joje_male` |

## Workflow

1. Read `SKILL.md`.
2. Read `references/chatterbox-local.md` before changing paths, defaults, or voice behavior.
3. Confirm the source text and voice.
4. If the user did not name a voice, run `list-voices`.
5. Split long narration into retry-safe chunks before generation.
6. Generate WAV files with `scripts/chatterbox_tts.py`.
7. Save every output to the target asset folder.
8. Create or update a manifest when there is more than one audio file.
9. Listen or inspect durations before handing audio to video assembly.

## Commands

Use an available Python executable. In this workspace, the portable Python usually works:

```powershell
& "C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\python_embeded\python.exe" ".\skills\chatterbox-tts\scripts\chatterbox_tts.py" doctor
```

List voices:

```powershell
& "<python>" ".\skills\chatterbox-tts\scripts\chatterbox_tts.py" list-voices
```

Generate one line:

```powershell
& "<python>" ".\skills\chatterbox-tts\scripts\chatterbox_tts.py" generate --model turbo --voice Paul_male --text "Tonight, everything changed." --output ".\Asset\audio\chatterbox\line-001.wav"
```

Generate from a text file:

```powershell
& "<python>" ".\skills\chatterbox-tts\scripts\chatterbox_tts.py" generate --model turbo --voice Paul_male --text-file ".\asset\Story Name\edited script\edited.txt" --output ".\asset\Story Name\audio\narration.wav"
```

Register a user voice sample:

```powershell
& "<python>" ".\skills\chatterbox-tts\scripts\chatterbox_tts.py" register-voice --sample ".\Asset\voices\sample.wav" --name narrator --gender male --language en
```

Register an old-woman persona voice:

```powershell
& "<python>" ".\skills\chatterbox-tts\scripts\chatterbox_tts.py" register-voice --sample ".\Asset\voices\Morganna_source.mp3" --name Morganna --gender female --language en --persona "old woman"
```

Generate old-woman narration:

```powershell
& "<python>" ".\skills\chatterbox-tts\scripts\chatterbox_tts.py" generate --model turbo --persona "old woman" --text-file ".\asset\Story Name\edited script\edited.txt" --output ".\asset\Story Name\audio\narration.wav"
```

## Manifest Contract

For multi-file narration, create:

```text
asset/<Story Name>/audio/narration-manifest.json
```

Track:

- chunk id
- source text or source text file and line range
- voice
- persona alias, when used
- model
- output path
- duration
- generation date
- retry notes

## Quality Checks

- Audio file exists and is non-empty.
- Voice matches the requested gender, tone, and language.
- Narration is clear and not clipped.
- Chunk order matches the script.
- Emotional tags improve delivery and do not sound unnatural.
- File names sort in playback order, such as `narration-001.wav`.

## Handoff

- Send narration WAV files and `narration-manifest.json` to `skills\hyperframes` for editable timeline composition.
- Send final narration files to `skills\video-use` when footage-first editing or final MP4 assembly is needed.
- For story videos, keep all audio under `asset/<Story Name>/audio/` so scene beats, captions, and images can reference stable paths.

## Failure Handling

- If Chatterbox cannot be found, run `doctor` and confirm the install path.
- If model loading is slow, wait before retrying; the first run can take several minutes.
- If one chunk fails, regenerate only that chunk.
- If pronunciation is wrong, edit the source chunk and regenerate only the affected audio.
- If a custom voice sample fails, keep the sample in `Asset/voices/` and retry registration with a short stable name.
