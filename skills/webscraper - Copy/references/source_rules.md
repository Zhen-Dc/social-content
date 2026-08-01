# Webscraper Source Rules

## Default Sources

- Wattpad example: `https://www.wattpad.com/1547045517-chapter-one`
- EbonyStory example: `https://www.ebonystory.com/short-story/before-the-morning-sun`

## Eligibility

Use these defaults unless the user changes them:

- Minimum views: `50000`
- Minimum likes/votes: `20000`
- Recency: published or updated within the last `2` months
- Unknown metrics: ineligible unless the user asks to include unknowns for research

Accept synonyms:

- views: reads, read count, views, impressions
- likes: likes, votes, reactions, hearts
- date: published, posted, updated, modified

## Intake Questions

Ask the most relevant questions before scraping, scripting, paid API usage, or rendering. Do not overwhelm the user if the task is urgent; ask the minimum needed and continue with stated assumptions.

1. Which story sources should I search: only the two provided URLs, all of Wattpad/EbonyStory, or a specific genre/category?
2. Should I scrape live now, or create the workflow and wait for your approval before network calls?
3. Do you own the story, have permission/license to save it verbatim, is it public-domain/appropriately licensed, or do you only want a private research summary?
4. Should stories with unknown metrics be saved for review or excluded?
5. Should the date rule use published date, updated date, or either one?
6. What genre should I prioritize: romance, drama, horror, confession, betrayal, revenge, mystery, inspirational, or another niche?
7. What language should the final script use?
8. What target platform is the video for: TikTok, Reels, Shorts, Facebook, or another channel?
9. What duration should the video be: 30 seconds, 60 seconds, 90 seconds, 3 minutes, or another length?
10. Should the script preserve the original plot closely, summarize it, or transform it into a new commentary-style narration?
11. What voice should the narrator use: dramatic, documentary, gossip, emotional, cinematic, calm, or conversational?
12. Should the story be split into episodes?
13. Should the hook reveal the conflict immediately or build suspense slowly?
14. Should the ending be complete, cliffhanger, or loop back to the opening?
15. Should character names be preserved, anonymized, or changed?
16. Should sensitive content be softened for platform compliance?
17. Do you want captions, scene prompts, image prompts, voiceover text, or all of them?
18. Which video production tool should receive the script after scraping?
19. Where should finished video assets be saved?
20. Should I keep raw scraped text after scripting, or archive only metadata and the adapted script?

## Rights And Platform Safety

Public web pages are not automatically safe to reuse in monetized videos. Before producing a final publishable script, confirm that the user has rights, permission, license, or a transformation strategy that is acceptable for their use case. If rights are unclear, produce a private research summary or a substantially transformed original script inspired by themes rather than a direct adaptation.

## Verbatim Capture

When verbatim capture is allowed, do not summarize or truncate the story because it is long. Save the full extracted story text in `story.txt`. If the story is too long for a single convenient file, split it into `sections/section-001.txt`, `sections/section-002.txt`, and so on.

Use verbatim capture only when one of these is true:

- The user owns the story.
- The user has permission or a license to store/adapt the story.
- The story is public-domain or clearly licensed for reuse.
- The user directly provided the full text.

Save metadata, source links, short permitted excerpts if appropriate, and non-verbatim research summaries.

## Failure Handling

- If scraping is blocked, save the error in the command output and ask whether to retry, use an approved browser workflow, or accept manually provided text.
- If metrics are missing, save the story only when `--include-ineligible` is used or the user provides the metrics.
- If a confirmed verbatim story is long, split it into section files instead of summarizing it.
- If the script generates a folder with a duplicate title, append a short hash from the URL.
