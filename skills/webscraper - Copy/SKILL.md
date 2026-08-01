---
name: webscraper
description: Scrape story websites such as Wattpad and EbonyStory, qualify viral stories by recency and engagement, save each story as text inside a folder named after the story, and turn eligible stories into short-form video script packages. Use when the user asks to find viral stories, scrape Wattpad or EbonyStory pages, save story text, prepare story-based scripts, or build a story-to-video workflow from web sources.
---

# Webscraper

Read `SOP.md` before using this skill independently. It defines the scraping workflow, rights rules, output folders, commands, QA checks, and handoff rules.

This is a project-local skill folder, not necessarily a globally invokable `$webscraper` command. In this workspace, read `C:\Social Content\skills\webscraper\SKILL.md` and run `scripts\web_scraper.py` directly or through `C:\Social Content\tools\story_video_pipeline.py`.

## Core Workflow

1. Ask the intake questions in `references/source_rules.md` when the user has not already provided answers, especially source URLs, rights, eligibility filters, and whether to scrape live pages now.
2. Use `scripts/web_scraper.py` for deterministic scraping and saving. Do not manually copy page text unless the tool fails and the user approves a fallback.
3. Save every story under the workspace `stories/` folder. Each story must have its own sanitized folder named after the story.
4. Treat the default viral threshold as: at least `50000` views, at least `20000` likes, and published or updated in the last `2` months.
5. If a site does not expose views, likes, or dates in the HTML, mark the story as `unknown` or ineligible unless the user provides the missing metrics or explicitly asks to include unknowns.
6. Do not summarize, shorten, or omit story text merely because it is long when verbatim capture is allowed. Use section files for long captures instead.
7. Use verbatim capture only when the user owns the story, has permission/license, the text is public-domain or appropriately licensed, or the user provides the story text.
8. Generate video-ready script drafts only for stories the user owns, has permission to adapt, can legally license, or wants summarized for private internal review.

## Quick Commands

Run from the workspace root:

```powershell
& "<python>" ".\skills\webscraper\scripts\web_scraper.py" --url "https://www.wattpad.com/1547045517-chapter-one" --url "https://www.ebonystory.com/short-story/before-the-morning-sun" --output-root ".\stories" --make-script
```

Use `--verbatim-ok` only after rights/permission/licensing is confirmed. This saves the full extracted story text and splits long text into `sections/` files:

```powershell
& "<python>" ".\skills\webscraper\scripts\web_scraper.py" --url "URL" --output-root ".\stories" --verbatim-ok --section-word-limit 2500
```

Use `--include-ineligible` when the user wants archived research even if a page does not meet the threshold:

```powershell
& "<python>" ".\skills\webscraper\scripts\web_scraper.py" --url "URL" --output-root ".\stories" --include-ineligible --make-script
```

Use discovery mode only as a first pass. Verify discovered URLs before using them in a final script:

```powershell
& "<python>" ".\skills\webscraper\scripts\web_scraper.py" --discover wattpad --discover ebonystory --discover-limit 10 --output-root ".\stories"
```

Replace `<python>` with the available Python executable for the environment.

## Outputs

For each saved story folder, expect:

- `story.txt`: scraped story text in plain text format.
- `sections/section-001.txt`, `section-002.txt`, etc.: long verbatim captures split into smaller files when `--verbatim-ok` is used.
- `metadata.json`: source URL, title, author when found, metrics, dates, and eligibility.
- `video_script.txt`: a draft short-form narration script when `--make-script` is used.
- `video_plan.json`: simple scene plan for building a vertical video.

## Video Creation Handoff

After scraping:

1. Review `story.txt` and `metadata.json`.
2. Confirm adaptation rights and target platform.
3. For the full picture-narration story-video workflow, normalize the scraper output through the strict pipeline:

```powershell
& "<python>" ".\tools\story_video_pipeline.py" --story-name "Story Name" --story-folder ".\stories\<Story Folder>" run-stage package-rewrite
```

4. That handoff copies `stories/<Story Folder>/story.txt` into `asset/<Story Name>/original script/original.txt` through `story-time-rewriter`. Do not skip directly from `video_script.txt` to video assembly.
5. Edit `video_script.txt` only when the user wants a short draft or private research script.
6. Keep generated videos editable until the user approves a final render.

## References

- Read `references/source_rules.md` for source-specific notes, intake questions, eligibility rules, and safety constraints.
