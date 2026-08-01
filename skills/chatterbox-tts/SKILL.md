---
name: chatterbox-tts
description: Generate speech audio with the user's local Chatterbox TTS install at C:\Ai Tools\Chatterbox -TTS with Turbo\Chatterbox TTS with Turbo. Use when the user asks to create narration, voice-over, story audio, TTS WAV files, list built-in Chatterbox voices, or register a supplied voice sample for later video generation.
---

# Chatterbox TTS

Read `SOP.md` before using this skill independently. It defines the audio workflow, asset locations, manifest contract, QA checks, and failure handling.

## Workflow

1. Use `scripts/chatterbox_tts.py` for all Chatterbox operations. It calls the portable Chatterbox Python runtime and keeps generated audio in this workspace by default.
2. Run `list-voices` before choosing a voice unless the user names one.
3. Prefer `generate --model turbo --voice Paul_male` for fast English narration. Use `--voice builtin` to use the model's built-in conditionals without a reference clip.
4. Use `register-voice` when the user supplies a voice sample. Give it a short stable name and include `--gender male|female` and `--language en` unless the user says otherwise.
5. Use persona aliases for age/gender narration voices. For example, `--persona "young woman"` resolves to `Rho_female`, and `--persona "old woman"` resolves to `Morganna_female`.
6. Save generated video narration under a project-specific folder, usually `Asset/audio/chatterbox/` or the current story/video package.

## Commands

List installed sample voices:

```powershell
& "<python>" ".\skills\chatterbox-tts\scripts\chatterbox_tts.py" list-voices
```

Generate speech:

```powershell
& "<python>" ".\skills\chatterbox-tts\scripts\chatterbox_tts.py" generate --text "Tonight, everything changed." --voice Paul_male --output ".\Asset\audio\chatterbox\line-001.wav"
```

Generate from a text file:

```powershell
& "<python>" ".\skills\chatterbox-tts\scripts\chatterbox_tts.py" generate --text-file ".\story\edited-script.txt" --voice Paul_male --output ".\Asset\audio\chatterbox\narration.wav"
```

Register a supplied sample for later use:

```powershell
& "<python>" ".\skills\chatterbox-tts\scripts\chatterbox_tts.py" register-voice --sample ".\Asset\voices\my-sample.wav" --name narrator --gender male --language en
```

Register a persona-routed sample:

```powershell
& "<python>" ".\skills\chatterbox-tts\scripts\chatterbox_tts.py" register-voice --sample ".\Asset\voices\Morganna_source.mp3" --name Morganna --gender female --language en --persona "old woman"
```

Generate by persona:

```powershell
& "<python>" ".\skills\chatterbox-tts\scripts\chatterbox_tts.py" generate --model turbo --persona "old woman" --text "I knew that house remembered me." --output ".\Asset\audio\chatterbox\morganna-test.wav"
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

Run a local environment check:

```powershell
& "<python>" ".\skills\chatterbox-tts\scripts\chatterbox_tts.py" doctor
```

## Notes

- The script defaults to Chatterbox at `C:\Ai Tools\Chatterbox -TTS with Turbo\Chatterbox TTS with Turbo`. Override with `--chatterbox-root` if the install moves.
- Persona aliases are stored in `C:\Social Content\Asset\voices\personas.json`.
- The first real generation may download or load model weights through Chatterbox and can take several minutes.
- Turbo supports tags such as `[chuckle]`, `[laugh]`, and `[sigh]` in English text.
- Read `references/chatterbox-local.md` before changing paths, defaults, or voice handling.
