---
name: story-time-rewriter
description: Rewrite full stories or scripts from another skill into story-time narration packages. Use when the user wants an original story/script preserved under asset/{Story Name}/original script/original.txt, rewritten closely into edited script/edited.txt, narrated from the main protagonist's POV with voice-over for unseen scenes, and all character names changed with a tracked name_map.json.
---

# Story Time Rewriter

Read `SOP.md` before using this skill independently. It defines the rewrite workflow, exact asset package, commands, QA checks, and handoff rules.

## Core Workflow

1. Accept a source story/script from another skill or from a user-provided text file. The input is usually a full story, but may be a shorter script.
2. Determine the story name from the user, source metadata, or input filename.
3. Run `scripts/story_time_package.py` to create the required folder layout, copy the source text to `original.txt`, generate `name_map.json`, and write `rewrite_prompt.md`.
4. Read `references/rewrite_rules.md` before rewriting if the task involves uncertain POV, character names, or folder placement.
5. Rewrite the story into story-time narration and save the completed rewrite as `asset/<Story Name>/edited script/edited.txt`.
6. Verify the package before finishing. Do not migrate or modify the workspace `story/` folder for this skill.

## Required Output Contract

Use this exact layout:

```text
asset/<Story Name>/
  original script/original.txt
  edited script/edited.txt
  edited script/name_map.json
  edited script/rewrite_prompt.md
```

The folder names must contain spaces exactly as shown: `original script` and `edited script`.

## Quick Command

Run from the workspace root:

```powershell
& "<python>" ".\skills\story-time-rewriter\scripts\story_time_package.py" --input ".\path\to\source.txt" --story-name "Story Name"
```

If an edited rewrite already exists, copy it into the package:

```powershell
& "<python>" ".\skills\story-time-rewriter\scripts\story_time_package.py" --input ".\path\to\source.txt" --story-name "Story Name" --edited-file ".\path\to\edited.txt"
```

Replace `<python>` with the available Python executable for the environment.

## Rewrite Rules

- Preserve the full plot closely.
- Use first-person narration from the main protagonist when the protagonist is present.
- Use voice-over narration for scenes the protagonist did not witness.
- If the protagonist is not obvious, auto-pick the most central character.
- Change every character's name entirely.
- Preserve name origin/culture and gender when clear; use culturally neutral replacement names when unclear.
- Let the story's tone drive the voice. Sad stories should sound sad, suspense stories suspenseful, and so on.
- Track all character-name replacements in `edited script/name_map.json`.
- Keep `edited script/rewrite_prompt.md` beside the final rewrite so future agents can inspect the rewrite basis.

## Name Map Handling

The script generates a first-pass `name_map.json` from detected proper names. Review it before writing `edited.txt`:

- Remove false positives that are not characters.
- Add missed character names, surnames, nicknames, and aliases.
- Ensure replacements are not the same as original names.
- Apply the final map consistently throughout the rewrite.

## References

- Read `references/rewrite_rules.md` for the complete packaging, POV, name-change, and quality-check rules.
