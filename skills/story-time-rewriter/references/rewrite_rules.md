# Story-Time Rewrite Rules

## Output Layout

Write every package under the workspace `asset/` folder:

```text
asset/<Story Name>/
  original script/original.txt
  edited script/edited.txt
  edited script/name_map.json
  edited script/rewrite_prompt.md
```

Do not write this skill's output into `story/` or `stories/`.

## Rewrite Standard

- Preserve the full plot closely.
- Rewrite as story-time narration, not summary notes.
- Use the main protagonist's first-person POV when the protagonist is present.
- For scenes the protagonist did not witness, switch to voice-over narration. Do not falsely narrate those scenes as direct first-person experience.
- If the protagonist is unclear, pick the character with the strongest combination of presence, agency, and plot impact.
- Match the emotional tone to the source story. A sad story should read sad; a suspense story should read suspenseful; a comic story may be lighter.
- Keep continuity, chronology, motivations, relationships, and key reveals intact.

## Character Name Changes

- Change every character's name entirely.
- Preserve the original name's cultural/origin feel when known.
- Preserve gender presentation when reasonably inferable.
- If the origin is unclear, use culturally neutral replacement names.
- Track every replacement in `edited script/name_map.json`.
- Apply the name map consistently in `edited.txt`.
- Keep place names unless they are clearly character names or the user asks to fictionalize locations.

## Quality Check

Before finishing, verify:

- `original script/original.txt` contains the source text.
- `edited script/edited.txt` exists and contains the rewritten story.
- `edited script/name_map.json` covers all character names used in the rewrite.
- `edited script/rewrite_prompt.md` documents the rewrite rules used.
- The old `story/` folder was not modified.
