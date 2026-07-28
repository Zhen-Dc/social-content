#!/usr/bin/env python3
"""Scrape story pages, qualify viral metrics, and save text/script packages."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import os
import re
import sys
import textwrap
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

DISCOVERY_SEEDS = {
    "wattpad": [
        "https://www.wattpad.com/stories/drama/hot",
        "https://www.wattpad.com/stories/romance/hot",
        "https://www.wattpad.com/stories/shortstory/hot",
    ],
    "ebonystory": [
        "https://www.ebonystory.com/short-stories",
        "https://www.ebonystory.com/stories",
    ],
}


class StoryHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.meta: dict[str, str] = {}
        self.links: list[str] = []
        self.text_parts: list[str] = []
        self.script_json: list[str] = []
        self._capture_title = False
        self._capture_text = False
        self._capture_script = False
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {k.lower(): v or "" for k, v in attrs}
        tag = tag.lower()

        if tag in {"script", "style", "noscript", "svg"}:
            self._skip_depth += 1
            if tag == "script":
                script_type = attr.get("type", "").lower()
                script_id = attr.get("id", "").lower()
                self._capture_script = "json" in script_type or script_id == "__next_data__"
            return

        if self._skip_depth:
            return

        if tag == "title":
            self._capture_title = True
        elif tag == "meta":
            key = attr.get("property") or attr.get("name") or attr.get("itemprop")
            content = attr.get("content")
            if key and content:
                self.meta[key.lower()] = html.unescape(content).strip()
        elif tag == "a":
            href = attr.get("href")
            if href:
                self.links.append(href)
        elif tag in {
            "article",
            "main",
            "section",
            "p",
            "h1",
            "h2",
            "h3",
            "div",
            "span",
            "li",
            "blockquote",
        }:
            self._capture_text = True

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"script", "style", "noscript", "svg"} and self._skip_depth:
            self._skip_depth -= 1
            self._capture_script = False
            return
        if tag == "title":
            self._capture_title = False
        if tag in {"p", "h1", "h2", "h3", "li", "blockquote"}:
            self.text_parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self._capture_script:
            data = data.strip()
            if data:
                self.script_json.append(data)
            return
        if self._skip_depth:
            return
        cleaned = normalize_space(data)
        if not cleaned:
            return
        if self._capture_title:
            self.title += cleaned + " "
        if self._capture_text:
            self.text_parts.append(cleaned)


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value or "")).strip()


def fetch_url(url: str, timeout: int) -> str:
    request = urllib.request.Request(url, headers=DEFAULT_HEADERS)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def absolute_url(base: str, href: str) -> str:
    return urllib.parse.urljoin(base, href)


def slugify(value: str, fallback: str = "untitled-story") -> str:
    value = re.sub(r"[^\w\s-]", "", value, flags=re.ASCII).strip().lower()
    value = re.sub(r"[-\s]+", "-", value)
    return value[:80].strip("-") or fallback


def parse_count(raw: str | int | float | None) -> int | None:
    if raw is None:
        return None
    if isinstance(raw, (int, float)):
        return int(raw)
    text = str(raw).strip().lower().replace(",", "")
    match = re.search(r"(\d+(?:\.\d+)?)\s*([kmb])?", text)
    if not match:
        return None
    value = float(match.group(1))
    multiplier = {"k": 1_000, "m": 1_000_000, "b": 1_000_000_000}.get(match.group(2), 1)
    return int(value * multiplier)


def parse_date(raw: str | None) -> str | None:
    if not raw:
        return None
    text = normalize_space(raw)
    text = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", text, flags=re.I)
    candidates = [
        text,
        text.replace("Z", "+00:00"),
        re.sub(r"\s+at\s+", " ", text, flags=re.I),
    ]
    formats = [
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%B %d, %Y",
        "%b %d, %Y",
        "%d %B %Y",
        "%d %b %Y",
        "%m/%d/%Y",
        "%d/%m/%Y",
    ]
    for candidate in candidates:
        try:
            return dt.datetime.fromisoformat(candidate).date().isoformat()
        except ValueError:
            pass
        for fmt in formats:
            try:
                return dt.datetime.strptime(candidate, fmt).date().isoformat()
            except ValueError:
                continue
    return None


def walk_json(value: Any) -> list[Any]:
    found = [value]
    if isinstance(value, dict):
        for child in value.values():
            found.extend(walk_json(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(walk_json(child))
    return found


def extract_json_objects(script_chunks: list[str]) -> list[Any]:
    objects: list[Any] = []
    for chunk in script_chunks:
        chunk = chunk.strip()
        if not chunk:
            continue
        try:
            objects.append(json.loads(chunk))
            continue
        except json.JSONDecodeError:
            pass
        for match in re.finditer(r"({.*?})", chunk):
            try:
                objects.append(json.loads(match.group(1)))
            except json.JSONDecodeError:
                continue
    return objects


def extract_from_json(objects: list[Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    text_bits: list[str] = []
    author_bits: list[str] = []

    title_keys = {"title", "name", "headline"}
    body_keys = {"text", "description", "articlebody", "storytext", "body"}
    author_keys = {"author", "username", "displayname"}
    view_keys = {"views", "viewcount", "readcount", "reads"}
    like_keys = {"likes", "likecount", "votecount", "votes", "hearts"}
    date_keys = {"datepublished", "publisheddate", "published", "datecreated", "dateupdated", "updated"}

    for item in objects:
        for node in walk_json(item):
            if not isinstance(node, dict):
                continue
            lower = {str(k).lower(): v for k, v in node.items()}
            for key in title_keys:
                if key in lower and not result.get("title") and isinstance(lower[key], str):
                    result["title"] = normalize_space(lower[key])
            for key in body_keys:
                if key in lower and isinstance(lower[key], str):
                    text = normalize_space(lower[key])
                    if len(text) > 80:
                        text_bits.append(text)
            for key in author_keys:
                if key in lower:
                    value = lower[key]
                    if isinstance(value, str):
                        author_bits.append(normalize_space(value))
                    elif isinstance(value, dict):
                        name = value.get("name") or value.get("username")
                        if isinstance(name, str):
                            author_bits.append(normalize_space(name))
            for key in view_keys:
                if key in lower and result.get("views") is None:
                    result["views"] = parse_count(lower[key])
            for key in like_keys:
                if key in lower and result.get("likes") is None:
                    result["likes"] = parse_count(lower[key])
            for key in date_keys:
                if key in lower:
                    parsed = parse_date(str(lower[key]))
                    if parsed and not result.get("date"):
                        result["date"] = parsed

    if text_bits:
        result["story_text"] = "\n\n".join(dedupe_keep_order(text_bits))
    if author_bits:
        result["author"] = dedupe_keep_order(author_bits)[0]
    return result


def dedupe_keep_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        key = value.lower()
        if key and key not in seen:
            seen.add(key)
            out.append(value)
    return out


def extract_metrics_from_text(text: str) -> dict[str, int | None]:
    lowered = text.lower().replace(",", "")
    views = None
    likes = None
    view_patterns = [
        r"(\d+(?:\.\d+)?\s*[kmb]?)\s*(?:views|reads|read count)",
        r"(?:views|reads|read count)\s*[:\-]?\s*(\d+(?:\.\d+)?\s*[kmb]?)",
    ]
    like_patterns = [
        r"(\d+(?:\.\d+)?\s*[kmb]?)\s*(?:likes|votes|hearts|reactions)",
        r"(?:likes|votes|hearts|reactions)\s*[:\-]?\s*(\d+(?:\.\d+)?\s*[kmb]?)",
    ]
    for pattern in view_patterns:
        match = re.search(pattern, lowered)
        if match:
            views = parse_count(match.group(1))
            break
    for pattern in like_patterns:
        match = re.search(pattern, lowered)
        if match:
            likes = parse_count(match.group(1))
            break
    return {"views": views, "likes": likes}


def extract_date_from_text(text: str) -> str | None:
    patterns = [
        r"(?:published|posted|updated|modified)\s*(?:on|:)?\s*([A-Za-z]+\s+\d{1,2},\s+\d{4})",
        r"(?:published|posted|updated|modified)\s*(?:on|:)?\s*(\d{4}-\d{2}-\d{2})",
        r"(?:published|posted|updated|modified)\s*(?:on|:)?\s*(\d{1,2}\s+[A-Za-z]+\s+\d{4})",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.I)
        if match:
            parsed = parse_date(match.group(1))
            if parsed:
                return parsed
    return None


def clean_story_text(parts: list[str]) -> str:
    lines: list[str] = []
    joined = " ".join(parts)
    joined = re.sub(r"\s+([,.!?;:])", r"\1", joined)
    sentences = re.split(r"(?<=[.!?])\s+", joined)
    buffer: list[str] = []
    for sentence in sentences:
        sentence = normalize_space(sentence)
        if not sentence:
            continue
        if len(sentence) < 2:
            continue
        buffer.append(sentence)
        if len(" ".join(buffer)) > 450:
            lines.append(" ".join(buffer))
            buffer = []
    if buffer:
        lines.append(" ".join(buffer))
    return "\n\n".join(dedupe_keep_order(lines))


def extract_story(url: str, page_html: str) -> dict[str, Any]:
    parser = StoryHTMLParser()
    parser.feed(page_html)
    json_data = extract_from_json(extract_json_objects(parser.script_json))
    visible_text = clean_story_text(parser.text_parts)
    metrics = extract_metrics_from_text(visible_text)

    title = (
        json_data.get("title")
        or parser.meta.get("og:title")
        or parser.meta.get("twitter:title")
        or normalize_space(parser.title)
        or "Untitled Story"
    )
    title = re.sub(r"\s*[-|]\s*(Wattpad|EbonyStory).*$", "", title, flags=re.I).strip()

    date = (
        json_data.get("date")
        or parse_date(parser.meta.get("article:published_time"))
        or parse_date(parser.meta.get("article:modified_time"))
        or parse_date(parser.meta.get("date"))
        or extract_date_from_text(visible_text)
    )

    story_text = json_data.get("story_text") or visible_text
    if len(story_text) < 200:
        description = parser.meta.get("og:description") or parser.meta.get("description")
        if description:
            story_text = normalize_space(description) + "\n\n" + story_text

    return {
        "source_url": url,
        "title": title,
        "author": json_data.get("author") or parser.meta.get("author"),
        "views": json_data.get("views") if json_data.get("views") is not None else metrics.get("views"),
        "likes": json_data.get("likes") if json_data.get("likes") is not None else metrics.get("likes"),
        "date": date,
        "story_text": story_text.strip(),
        "links": parser.links,
    }


def eligibility(story: dict[str, Any], min_views: int, min_likes: int, months: int) -> dict[str, Any]:
    reasons: list[str] = []
    views = story.get("views")
    likes = story.get("likes")
    date_value = story.get("date")
    cutoff = dt.date.today() - dt.timedelta(days=months * 31)

    if views is None:
        reasons.append("views_unknown")
    elif int(views) < min_views:
        reasons.append("views_below_threshold")

    if likes is None:
        reasons.append("likes_unknown")
    elif int(likes) < min_likes:
        reasons.append("likes_below_threshold")

    if not date_value:
        reasons.append("date_unknown")
    else:
        try:
            story_date = dt.date.fromisoformat(str(date_value))
            if story_date < cutoff:
                reasons.append("outside_recency_window")
        except ValueError:
            reasons.append("date_unparseable")

    return {
        "eligible": not reasons,
        "reasons": reasons,
        "cutoff_date": cutoff.isoformat(),
        "min_views": min_views,
        "min_likes": min_likes,
        "months": months,
    }


def make_video_script(story: dict[str, Any], max_words: int = 220) -> str:
    title = story.get("title") or "this story"
    text = normalize_space(story.get("story_text") or "")
    words = text.split()
    excerpt = " ".join(words[:max_words])
    if len(words) > max_words:
        excerpt += "..."

    return textwrap.dedent(
        f"""
        TITLE: {title}

        HOOK:
        I found a story that starts quietly, then turns into the kind of confession you cannot stop watching.

        NARRATION:
        {excerpt}

        PACING NOTES:
        - Open on the central conflict in the first 3 seconds.
        - Keep sentences short for captions.
        - Add a pause before the turning point.
        - End with either a cliffhanger or a direct question for comments.

        RIGHTS CHECK:
        Do not publish this as a direct adaptation until ownership, license, or permission is confirmed.
        """
    ).strip() + "\n"


def make_video_plan(story: dict[str, Any]) -> dict[str, Any]:
    return {
        "format": "vertical_9_16",
        "estimated_duration_seconds": 60,
        "scenes": [
            {"slot": "hook", "duration": 5, "visual": "bold text over moody story image"},
            {"slot": "setup", "duration": 15, "visual": "character/environment visuals"},
            {"slot": "conflict", "duration": 25, "visual": "fast caption pacing with emotional cutaways"},
            {"slot": "ending", "duration": 15, "visual": "cliffhanger or comment prompt"},
        ],
        "source_title": story.get("title"),
        "source_url": story.get("source_url"),
    }


def split_text_by_words(text: str, max_words: int) -> list[str]:
    words = text.split()
    if max_words <= 0 or len(words) <= max_words:
        return [text]
    sections: list[str] = []
    for start in range(0, len(words), max_words):
        sections.append(" ".join(words[start : start + max_words]))
    return sections


def write_story_sections(folder: Path, text: str, max_words: int) -> list[str]:
    sections = split_text_by_words(text, max_words)
    if len(sections) <= 1:
        return []
    section_dir = folder / "sections"
    section_dir.mkdir(exist_ok=True)
    written: list[str] = []
    for index, section in enumerate(sections, start=1):
        path = section_dir / f"section-{index:03d}.txt"
        path.write_text(section.strip() + "\n", encoding="utf-8")
        written.append(str(path.name))
    return written


def save_story(
    story: dict[str, Any],
    output_root: Path,
    make_script: bool,
    eligibility_data: dict[str, Any],
    verbatim_ok: bool,
    section_word_limit: int,
) -> Path:
    title = story.get("title") or "Untitled Story"
    url_hash = hashlib.sha1(str(story.get("source_url", "")).encode("utf-8")).hexdigest()[:8]
    folder = output_root / f"{slugify(title)}-{url_hash}"
    folder.mkdir(parents=True, exist_ok=True)

    metadata = {k: v for k, v in story.items() if k not in {"story_text", "links"}}
    metadata["eligibility"] = eligibility_data
    metadata["verbatim_capture"] = {
        "enabled": verbatim_ok,
        "note": (
            "Full extracted text was saved because verbatim capture was explicitly allowed."
            if verbatim_ok
            else "Full verbatim capture was not enabled; use --verbatim-ok only for owned, licensed, public-domain, or user-provided text."
        ),
    }

    story_text = story.get("story_text", "")
    (folder / "story.txt").write_text(story_text, encoding="utf-8")
    if verbatim_ok:
        metadata["verbatim_capture"]["section_files"] = write_story_sections(folder, story_text, section_word_limit)
    (folder / "metadata.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")

    if make_script:
        (folder / "video_script.txt").write_text(make_video_script(story), encoding="utf-8")
        (folder / "video_plan.json").write_text(
            json.dumps(make_video_plan(story), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    return folder


def discover_urls(site: str, limit: int, timeout: int) -> list[str]:
    urls: list[str] = []
    for seed in DISCOVERY_SEEDS.get(site.lower(), []):
        try:
            page = fetch_url(seed, timeout)
        except Exception as exc:
            print(f"[WARN] discovery failed for {seed}: {exc}", file=sys.stderr)
            continue
        parser = StoryHTMLParser()
        parser.feed(page)
        for href in parser.links:
            full = absolute_url(seed, href)
            if site == "wattpad" and re.search(r"wattpad\.com/\d+", full):
                urls.append(full.split("?")[0])
            elif site == "ebonystory" and "ebonystory.com/" in full and re.search(r"/(short-story|story)/", full):
                urls.append(full.split("?")[0])
            if len(dedupe_keep_order(urls)) >= limit:
                return dedupe_keep_order(urls)[:limit]
    return dedupe_keep_order(urls)[:limit]


def process_url(url: str, args: argparse.Namespace) -> dict[str, Any]:
    page = fetch_url(url, args.timeout)
    story = extract_story(url, page)
    status = eligibility(story, args.min_views, args.min_likes, args.months)
    if status["eligible"] or args.include_ineligible:
        folder = save_story(
            story,
            Path(args.output_root),
            args.make_script,
            status,
            args.verbatim_ok,
            args.section_word_limit,
        )
        return {"url": url, "saved": str(folder), "eligible": status["eligible"], "reasons": status["reasons"]}
    return {"url": url, "saved": None, "eligible": False, "reasons": status["reasons"]}


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Scrape viral story pages and save story/script packages.")
    parser.add_argument("--url", action="append", default=[], help="Story URL to scrape. Can be repeated.")
    parser.add_argument("--discover", action="append", choices=sorted(DISCOVERY_SEEDS), default=[], help="Discover story URLs from a site.")
    parser.add_argument("--discover-limit", type=int, default=10, help="Maximum URLs per discovered site.")
    parser.add_argument("--output-root", default="stories", help="Folder where story folders are saved.")
    parser.add_argument("--min-views", type=int, default=50_000)
    parser.add_argument("--min-likes", type=int, default=20_000)
    parser.add_argument("--months", type=int, default=2)
    parser.add_argument("--include-ineligible", action="store_true", help="Save stories even when metrics are missing or below threshold.")
    parser.add_argument("--make-script", action="store_true", help="Create video_script.txt and video_plan.json.")
    parser.add_argument(
        "--verbatim-ok",
        action="store_true",
        help="Confirm the text may be saved verbatim because it is owned, licensed, public-domain, or user-provided.",
    )
    parser.add_argument(
        "--section-word-limit",
        type=int,
        default=2500,
        help="When --verbatim-ok is set, split long story text into section files at this word count.",
    )
    parser.add_argument("--timeout", type=int, default=25)
    return parser


def main() -> int:
    args = build_arg_parser().parse_args()
    urls = list(args.url)
    for site in args.discover:
        urls.extend(discover_urls(site, args.discover_limit, args.timeout))
    urls = dedupe_keep_order(urls)

    if not urls:
        print("No URLs provided. Use --url or --discover.", file=sys.stderr)
        return 2

    Path(args.output_root).mkdir(parents=True, exist_ok=True)
    results: list[dict[str, Any]] = []
    for url in urls:
        try:
            result = process_url(url, args)
            results.append(result)
            marker = "SAVED" if result["saved"] else "SKIPPED"
            print(f"[{marker}] {url} eligible={result['eligible']} reasons={','.join(result['reasons']) or 'none'}")
            if result["saved"]:
                print(f"        {result['saved']}")
        except (urllib.error.URLError, TimeoutError, ValueError, OSError) as exc:
            results.append({"url": url, "error": str(exc)})
            print(f"[ERROR] {url}: {exc}", file=sys.stderr)

    summary_path = Path(args.output_root) / "scrape_summary.json"
    summary_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[SUMMARY] {summary_path}")
    return 0 if any(item.get("saved") for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
