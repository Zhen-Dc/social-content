# SOP: Video Use

## Purpose

Use this SOP for transcript-aware video editing, footage assembly, cuts, grading, subtitles, overlays, preview renders, and final MP4 output.

This skill works on real media files. It should not write outputs into the skill folder.

## Skill Files

- Skill folder: `C:\Social Content\skills\video-use`
- Main instructions: `SKILL.md`
- Install notes: `install.md`
- Helpers: `helpers\`

## Inputs Needed

- Folder containing source video or audio files.
- Editing goal and platform.
- Target format: horizontal, vertical, square, or custom.
- User-approved editing strategy before cuts are executed.
- Optional captions, overlays, animations, music, SFX, or brand style.

## Where To Save Assets

All session outputs must go in the source media folder's `edit/` directory:

```text
<videos_dir>/
  <source files>
  edit/
    project.md
    takes_packed.md
    edl.json
    transcripts/
    animations/
    clips_graded/
    master.srt
    preview.mp4
    final.mp4
```

For story video packages, use:

```text
asset/<Story Name>/video/renders/
asset/<Story Name>/output/
```

Do not write session outputs inside `C:\Social Content\skills\video-use`.

## Workflow

1. Read `SKILL.md`.
2. Use `install.md` only for first-time setup or reconnect.
3. Verify `ffmpeg` and `ffprobe` are available.
4. Verify the transcription API key only when transcription is required.
5. Inventory source media with `ffprobe`.
6. Transcribe sources and cache transcripts.
7. Pack transcripts into `takes_packed.md`.
8. Propose a plain-English edit strategy and wait for approval.
9. Build `edl.json`.
10. Use timeline views only at decision points.
11. Render a preview.
12. Self-check cut boundaries, audio pops, captions, overlays, and visual jumps.
13. Render final output after approval.
14. Append important decisions to `project.md`.

## Helper Commands

The helpers are invoked relative to the skill folder:

```powershell
python ".\skills\video-use\helpers\transcribe_batch.py" "<videos_dir>"
python ".\skills\video-use\helpers\pack_transcripts.py" --edit-dir "<videos_dir>\edit"
python ".\skills\video-use\helpers\timeline_view.py" "<video>" 10 20
python ".\skills\video-use\helpers\render.py" "<videos_dir>\edit\edl.json" -o "<videos_dir>\edit\preview.mp4" --preview
python ".\skills\video-use\helpers\render.py" "<videos_dir>\edit\edl.json" -o "<videos_dir>\edit\final.mp4" --build-subtitles
```

If normal `python` is unavailable, use the workspace portable Python or the environment that has the helper dependencies installed.

## Hard Rules

- Confirm the strategy before executing cuts.
- Never cut inside a word.
- Pad cut edges by 30 to 200 ms.
- Cache transcripts and do not re-transcribe unchanged sources.
- Apply subtitles last in the filter chain.
- Use output-timeline offsets for `master.srt`.
- Put all outputs in `<videos_dir>/edit/`.

## Quality Checks

- `takes_packed.md` exists before edit decisions.
- `edl.json` references valid source files.
- Preview render plays.
- Captions are synced and visible.
- Audio has no pops at cuts.
- Overlays do not hide subtitles.
- Final output is in the requested aspect ratio and platform format.

## Handoff

- Use `skills\hyperframes` for HTML timeline, motion graphics, and editable visual scenes.
- Use `video-use` for finishing, subtitles, grading, and final MP4 assembly.
- For picture narration videos, return final renders to `asset/<Story Name>/output/`.
