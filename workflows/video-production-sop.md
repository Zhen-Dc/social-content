# SOP: Video Production

## Purpose

Use this SOP when a story, script, raw footage, voiceover, caption set, or social-content package needs to become an editable video workflow inside this project.

For story videos made from pictures plus narration voice-over, follow the dedicated WAT workflow first:

```text
workflows/picture-narration-story-video-sop.md
```

The goal is to keep story production, transcript-based editing, HyperFrames timeline work, captions, overlays, and final renders organized under the Social Content workspace.

## Related Skill And Tooling

- Video editing skill: `skills/video-use/SKILL.md`
- HyperFrames skill: `skills/hyperframes/SKILL.md`
- Story scraping skill: `skills/webscraper/SKILL.md`
- Story rewriting skill: `skills/story-time-rewriter/SKILL.md`
- Picture narration orchestrator: `skills/social-story-video-maker/SKILL.md`

## Skill Routing

Use `video-use` when the work starts from video footage or audio that needs transcript-aware editing, cuts, grading, burned subtitles, or final MP4 assembly.

Use `hyperframes` when the work needs editable HTML video timelines, title cards, motion graphics, captions, overlays, visual scenes, voiceover-driven animation, or preview-first composition work.

Use both together when a story or script needs a previewable timeline before final render:

1. Prepare or approve the script.
2. Build voiceover, captions, scenes, and overlays as separate editable assets.
3. Create a HyperFrames composition for preview and timing review.
4. Render only after the editable preview is approved.
5. Use `video-use` for transcript/cut assembly when source footage is part of the job.

Use `social-story-video-maker` when the whole route starts from a web story or supplied story and must become a social media picture narration video. That route coordinates web scraping, first-person story-time rewriting, Chatterbox TTS, film-director prompts, ComfyUI image generation, HyperFrames composition, SFX/music, and final render.

## Output Layout

For story-derived videos, keep outputs with the story package when possible:

```text
stories/
  Story Name/
    story.txt
    video_script.txt
    video_plan.json
    video/
      hyperframes/
      assets/
      captions/
      audio/
      renders/
```

For footage-first edits, follow `video-use` and place session output under the source media folder's `edit/` directory.

## Preview Rule

For editable social video work, give the user a previewable timeline before final render whenever practical. Do not collapse source assets, captions, scenes, audio, and overlays into one irreversible render until the user approves the preview.

## Setup Notes

- The project-local skill copies live under `skills/`.
- `video-use` was installed without its source `.env`; put API keys only in an approved local environment or the user's existing secure skill setup.
- `hyperframes` commands expect a project directory containing `index.html`, not a single HTML file path.
- Run HyperFrames checks from the composition directory:

```powershell
npx hyperframes lint
npx hyperframes validate
```

Use `npx hyperframes inspect` for layout verification on substantial new compositions.
