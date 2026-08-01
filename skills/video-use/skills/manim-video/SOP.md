# SOP: Manim Video

## Purpose

Use this SOP to create mathematical, technical, algorithmic, architecture, paper-explainer, or 3Blue1Brown-style animations using Manim Community Edition.

This subskill creates programmatic animation projects. It can be used independently from the parent `video-use` editing workflow.

## Skill And Tooling

- Skill folder: `C:\Social Content\skills\video-use\skills\manim-video`
- Main instructions: `SKILL.md`
- Setup script: `scripts\setup.sh`
- References: `references\`
- Runtime requirements: Python 3.10+, Manim CE, LaTeX, and ffmpeg.

## Inputs Needed

- Topic, equation, algorithm, system architecture, data story, or paper.
- Target audience and desired depth.
- Output length and resolution.
- Narration requirement, if any.
- Visual style or palette, if supplied.

## Where To Save Assets

For standalone Manim projects:

```text
Asset/manim/<Project Name>/
  plan.md
  script.py
  concat.txt
  final.mp4
  media/
```

For story or social packages:

```text
asset/<Story Name>/video/manim/
  plan.md
  script.py
  final.mp4
  media/
```

Do not save generated project files inside the `manim-video` skill folder.

## Workflow

1. Read `SKILL.md`.
2. Read the relevant reference file:
   - `references\scene-planning.md` for concept explainers.
   - `references\equations.md` for derivations.
   - `references\graphs-and-data.md` for algorithms or data.
   - `references\camera-and-3d.md` for 3D scenes.
   - `references\rendering.md` for output and ffmpeg.
   - `references\troubleshooting.md` when renders fail.
3. Write `plan.md` before code.
4. Define the narrative arc, misconception, aha moment, scene list, palette, and voiceover script.
5. Write one `script.py` with one Manim class per scene.
6. Render drafts with `-ql`.
7. Inspect preview stills and draft video.
8. Render production with `-qh` only after the draft is clean.
9. Stitch scene clips with ffmpeg when needed.
10. Save `final.mp4` in the project folder.

## Commands

Check dependencies:

```bash
bash scripts/setup.sh
```

Render draft:

```bash
manim -ql script.py Scene1_Introduction Scene2_CoreConcept
```

Render production:

```bash
manim -qh script.py Scene1_Introduction Scene2_CoreConcept
```

Render a still for inspection:

```bash
manim -ql --format=png -s script.py Scene2_CoreConcept
```

Stitch clips:

```bash
ffmpeg -y -f concat -safe 0 -i concat.txt -c copy final.mp4
```

## Project Contract

Every Manim project should keep:

```text
plan.md
script.py
concat.txt
final.mp4
media/
```

Use monospace fonts for text, `MathTex` for equations, and shared constants for palette and typography.

## Quality Checks

- `plan.md` explains the teaching arc and aha moment.
- Every scene is independently renderable.
- Text is readable and not crowded near edges.
- Important reveals have breathing room with `self.wait()`.
- Equations use raw strings for LaTeX.
- Palette and typography stay consistent across scenes.
- Draft render is inspected before production render.
- `final.mp4` plays and teaches the intended concept.

## Handoff

- Send `final.mp4` to `skills\video-use` when it needs subtitles, grading, music, or assembly with other footage.
- Send Manim clips to `skills\hyperframes` when they need HTML motion graphics or composition with other visual layers.
- Keep `plan.md` and `script.py` with the final render so future agents can revise the animation.

## Failure Handling

- If LaTeX fails, check raw strings, missing packages, and `MathTex` syntax.
- If layout is crowded, reduce simultaneous objects and use opacity layering.
- If render time is slow, iterate with `-ql` and render production only at the end.
- If ffmpeg stitching fails, verify `concat.txt` paths and use forward slashes when needed.
