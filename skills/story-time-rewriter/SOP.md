# SOP: Story Time Rewriter

## Purpose

Use this SOP to convert a full story or script into a first-person story-time narration package while preserving the original source text and changing all character names.

This skill produces a script package. It does not scrape websites, generate audio, create images, or render video by itself.

## Skill And Tool

- Skill folder: `C:\Social Content\skills\story-time-rewriter`
- Script: `scripts\story_time_package.py`
- Reference: `references\rewrite_rules.md`

## Inputs Needed

- Source story or script file.
- Story name.
- Protagonist if known.
- Tone, language, and target platform when supplied.
- Optional already-edited rewrite file.

## Where To Save Assets

Use this exact package layout:

```text
asset/<Story Name>/
  original script/original.txt
  edited script/edited.txt
  edited script/name_map.json
  edited script/rewrite_prompt.md
```

The folder names must contain spaces exactly as shown:

```text
original script
edited script
```

Do not move this skill's output into the workspace `story/` folder.

## Workflow

1. Read `SKILL.md`.
2. Read `references\rewrite_rules.md` when POV, names, or folder placement need care.
3. Choose the story name from the user, metadata, or source filename.
4. Run `scripts\story_time_package.py` to create the folder contract.
5. Review the generated `name_map.json`.
6. Remove false character names and add missed names, nicknames, surnames, and aliases.
7. Rewrite into first-person protagonist POV.
8. Use voice-over narration for scenes the protagonist did not witness.
9. Preserve the full plot closely unless the user asks for a looser adaptation.
10. Save the final rewrite to `edited script/edited.txt`.
11. Verify the folder contract before handing off.

## Commands

Create the package:

```powershell
& "<python>" ".\skills\story-time-rewriter\scripts\story_time_package.py" --input ".\path\to\source.txt" --story-name "Story Name"
```

Create the package with an existing edited rewrite:

```powershell
& "<python>" ".\skills\story-time-rewriter\scripts\story_time_package.py" --input ".\path\to\source.txt" --story-name "Story Name" --edited-file ".\path\to\edited.txt"
```

Use the portable workspace Python when no normal Python is on PATH:

```powershell
& "C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\python_embeded\python.exe" ".\skills\story-time-rewriter\scripts\story_time_package.py" --input ".\path\to\source.txt" --story-name "Story Name"
```

## Rewrite Rules

- Change every character name.
- Preserve name culture and gender when clear.
- Keep the plot close to the original.
- Narrate in first person from the protagonist.
- Do not switch narrator unless the user explicitly asks.
- Keep story tone: sad, suspenseful, romantic, angry, or reflective as appropriate.
- Preserve important dialogue but adapt it into story-time narration when needed.

## Quality Checks

- `original.txt` contains the unchanged source.
- `edited.txt` exists and is complete.
- `name_map.json` includes every character replacement.
- No original character names remain in `edited.txt` unless intentionally preserved as non-character words.
- POV is consistent.
- The rewrite can be read aloud naturally as narration.

## Handoff

- Send `edited.txt` to `skills\chatterbox-tts` for narration audio.
- Send story beats to `skills\film-director` for scene planning.
- Keep the package under `asset/<Story Name>/` for the full video workflow.
