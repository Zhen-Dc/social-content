# SOP: Webscraper

## Purpose

Use this SOP to discover, scrape, save, and package story website content for later rewriting or video production.

This skill handles source capture and metadata. It does not rewrite the story, generate audio, create images, or render video by itself.

## Skill And Tool

- Skill folder: `C:\Social Content\skills\webscraper`
- Script: `scripts\web_scraper.py`
- Source rules: `references\source_rules.md`
- Default output root: `C:\Social Content\stories`

## Inputs Needed

- Source URLs or discovery sources.
- Rights status: owned, licensed, public domain, permission granted, or private internal review.
- Whether verbatim capture is allowed.
- Whether ineligible/unknown-metric stories should be saved.
- Whether to make a draft video script.
- Target output root if not `stories/`.

## Rights Rule

Only save full verbatim story text when the user owns it, has permission, has a license, provides the text, or the work is public-domain or appropriately licensed.

If rights or access are unclear, save metadata and ask for authorized text before creating a publishable adaptation.

## Where To Save Assets

Default scraper output:

```text
stories/<Story Name>/
  story.txt
  metadata.json
  video_script.txt
  video_plan.json
  sections/
```

Use `sections/` for long verbatim captures:

```text
stories/<Story Name>/sections/section-001.txt
stories/<Story Name>/sections/section-002.txt
```

Do not save scraped story packages inside the skill folder.

## Workflow

1. Read `SKILL.md`.
2. Read `references\source_rules.md` when source rules, intake questions, rights, or eligibility are unclear.
3. Confirm source URLs or discovery mode.
4. Confirm rights and whether `--verbatim-ok` is allowed.
5. Run `scripts\web_scraper.py`.
6. Save every story in its own sanitized folder under `stories/`.
7. Review `metadata.json` for title, author, source URL, dates, metrics, and eligibility.
8. Mark missing metrics as unknown unless the user supplies them.
9. Use default viral threshold unless the user gives a different one:
   - at least `50000` views
   - at least `20000` likes
   - published or updated in the last `2` months
10. Create `video_script.txt` and `video_plan.json` only when requested or when the workflow needs them.
11. Hand authorized story text to `skills\story-time-rewriter`.

## Commands

Scrape URLs and make a draft script:

```powershell
& "<python>" ".\skills\webscraper\scripts\web_scraper.py" --url "URL" --output-root ".\stories" --make-script
```

Scrape multiple URLs:

```powershell
& "<python>" ".\skills\webscraper\scripts\web_scraper.py" --url "URL_1" --url "URL_2" --output-root ".\stories" --make-script
```

Save verbatim text only after rights are confirmed:

```powershell
& "<python>" ".\skills\webscraper\scripts\web_scraper.py" --url "URL" --output-root ".\stories" --verbatim-ok --section-word-limit 2500
```

Save research even when metrics are missing or ineligible:

```powershell
& "<python>" ".\skills\webscraper\scripts\web_scraper.py" --url "URL" --output-root ".\stories" --include-ineligible --make-script
```

Discover candidate stories:

```powershell
& "<python>" ".\skills\webscraper\scripts\web_scraper.py" --discover wattpad --discover ebonystory --discover-limit 10 --output-root ".\stories"
```

Use the portable workspace Python when no normal Python is on PATH:

```powershell
& "C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\python_embeded\python.exe" ".\skills\webscraper\scripts\web_scraper.py" --url "URL" --output-root ".\stories"
```

## Quality Checks

- Each story has its own folder.
- `metadata.json` includes source URL and eligibility status.
- `story.txt` exists only when text capture is allowed or provided.
- Long captures are split into `sections/`.
- Draft `video_script.txt` is treated as a first draft, not final copy.
- Unauthorized text is not adapted into a public video script.

## Failure Handling

- If scraping is blocked, preserve the error and ask for pasted or authorized text.
- If robots, login, paywall, or site access prevents capture, do not bypass it.
- If metrics are missing, mark unknown and use `--include-ineligible` only when the user wants research saved.
- If the scraper fails due to site changes, fix the script and retest on one safe URL before bulk scraping.

## Handoff

- Send authorized `story.txt` to `skills\story-time-rewriter`.
- Send `video_script.txt` to video planning only after human/agent review.
- Keep `metadata.json` with every downstream package for source traceability.


