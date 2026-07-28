"""Prepare story-time rewrite packages with the required asset layout."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


NAME_BANKS = {
    "english": {
        "male": ["Andrew", "Fred", "Marcus", "Daniel", "Peter", "Victor"],
        "female": ["Lisa", "Clara", "Grace", "Hannah", "Nora", "Rachel"],
        "neutral": ["Morgan", "Taylor", "Robin", "Casey"],
    },
    "french": {
        "male": ["Luc", "Etienne", "Adrien", "Marcel", "Thierry"],
        "female": ["Claire", "Elise", "Camille", "Adele", "Manon"],
        "neutral": ["Claude", "Dominique", "Sacha"],
    },
    "yoruba": {
        "male": ["Adewale", "Tunde", "Bamidele", "Femi", "Segun"],
        "female": ["Yetunde", "Bisi", "Folake", "Kemi", "Sade"],
        "neutral": ["Taiwo", "Kehinde", "Damilola"],
    },
    "igbo": {
        "male": ["Chinedu", "Emeka", "Obinna", "Ikenna", "Kelechi"],
        "female": ["Adaeze", "Chinwe", "Ngozi", "Amaka", "Ifunanya"],
        "neutral": ["Chidera", "Somto", "Uche"],
    },
    "hausa": {
        "male": ["Musa", "Bello", "Sani", "Abubakar", "Kabir"],
        "female": ["Amina", "Zainab", "Fatima", "Hauwa", "Maryam"],
        "neutral": ["Nasiru", "Sadiya", "Salihu"],
    },
    "arabic": {
        "male": ["Omar", "Karim", "Yusuf", "Samir", "Nabil"],
        "female": ["Layla", "Aisha", "Mariam", "Nadia", "Samira"],
        "neutral": ["Noor", "Iman", "Samar"],
    },
    "neutral": {
        "male": ["Adrian", "Julian", "Theo", "Evan", "Micah"],
        "female": ["Maya", "Elena", "Iris", "Mila", "Nina"],
        "neutral": ["Alex", "Jordan", "Riley", "Sam", "Quinn", "Avery"],
    },
}

KNOWN_NAMES = {
    "jack": ("english", "male"),
    "john": ("english", "male"),
    "mary": ("english", "female"),
    "andrew": ("english", "male"),
    "lisa": ("english", "female"),
    "fred": ("english", "male"),
    "jean": ("french", "male"),
    "pierre": ("french", "male"),
    "marie": ("french", "female"),
    "luc": ("french", "male"),
    "claire": ("french", "female"),
    "akande": ("yoruba", "male"),
    "ade": ("yoruba", "male"),
    "funmi": ("yoruba", "female"),
    "bisi": ("yoruba", "female"),
    "chidi": ("igbo", "male"),
    "ada": ("igbo", "female"),
    "ngozi": ("igbo", "female"),
    "musa": ("hausa", "male"),
    "amina": ("hausa", "female"),
    "fatima": ("hausa", "female"),
    "omar": ("arabic", "male"),
    "aisha": ("arabic", "female"),
    "layla": ("arabic", "female"),
}

STOP_NAMES = {
    "Chapter",
    "Part",
    "Story",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
    "A",
    "After",
    "Although",
    "Before",
    "But",
    "Even",
    "Everyone",
    "Finally",
    "For",
    "From",
    "He",
    "Her",
    "His",
    "However",
    "I",
    "If",
    "In",
    "It",
    "Later",
    "Meanwhile",
    "My",
    "No",
    "Nobody",
    "Nothing",
    "Once",
    "Our",
    "She",
    "So",
    "Somebody",
    "Someone",
    "That",
    "The",
    "Then",
    "There",
    "They",
    "This",
    "Though",
    "Until",
    "We",
    "When",
    "While",
    "With",
    "Yes",
    "Yet",
}


def sanitize_story_name(name: str) -> str:
    clean = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "", name).strip().rstrip(".")
    clean = re.sub(r"\s+", " ", clean)
    return clean or "Untitled Story"


def infer_story_name(input_path: Path, story_name: str | None) -> str:
    if story_name:
        return sanitize_story_name(story_name)
    return sanitize_story_name(input_path.stem.replace("_", " ").replace("-", " "))


def detect_names(text: str, limit: int) -> list[dict[str, object]]:
    pattern = re.compile(r"\b[A-Z][a-z]+(?:['-][A-Z]?[a-z]+)?\b")
    counts: dict[str, int] = {}
    first_seen: dict[str, int] = {}
    for match in pattern.finditer(text):
        name = match.group(0)
        if name in STOP_NAMES:
            continue
        counts[name] = counts.get(name, 0) + 1
        first_seen.setdefault(name, match.start())
    ranked = sorted(counts, key=lambda n: (-counts[n], first_seen[n], n.lower()))
    return [{"name": name, "mentions": counts[name]} for name in ranked[:limit]]


def classify_name(name: str) -> tuple[str, str]:
    return KNOWN_NAMES.get(name.lower(), ("neutral", "neutral"))


def replacement_for(origin: str, gender: str, used: set[str], original: str) -> str:
    bank = NAME_BANKS.get(origin, NAME_BANKS["neutral"])
    candidates = bank.get(gender, []) + bank.get("neutral", []) + NAME_BANKS["neutral"]["neutral"]
    for candidate in candidates:
        if candidate.lower() != original.lower() and candidate not in used:
            used.add(candidate)
            return candidate
    suffix = 2
    while True:
        candidate = f"{candidates[0]} {suffix}"
        if candidate not in used:
            used.add(candidate)
            return candidate
        suffix += 1


def build_name_map(detected: list[dict[str, object]]) -> dict[str, dict[str, object]]:
    used: set[str] = set()
    mapping: dict[str, dict[str, object]] = {}
    for item in detected:
        original = str(item["name"])
        origin, gender = classify_name(original)
        replacement = replacement_for(origin, gender, used, original)
        mapping[original] = {
            "replacement": replacement,
            "origin": origin,
            "gender": gender,
            "mentions": item["mentions"],
            "confidence": "known-name-bank" if origin != "neutral" or gender != "neutral" else "fallback-neutral",
        }
    return mapping


def rewrite_prompt(story_name: str, name_map: dict[str, dict[str, object]]) -> str:
    lines = [
        f"Rewrite package for: {story_name}",
        "",
        "Task:",
        "- Rewrite original script into story-time narration.",
        "- Preserve the full plot closely. Do not invent a new story.",
        "- Use first-person POV from the main protagonist when the protagonist is present.",
        "- For scenes the protagonist did not witness, use a voice-over narration style instead of pretending first-person access.",
        "- If the protagonist is unclear, choose the most central character by presence, agency, and plot impact.",
        "- Change every character name throughout the story using name_map.json.",
        "- Preserve the cultural/origin feel of known names. Use culturally neutral replacements for unclear names.",
        "- Match the story's emotional tone. Sad stories should sound sad; suspense stories should sound suspenseful.",
        "- Save only the final rewritten script as edited.txt.",
        "",
        "Name map:",
    ]
    if name_map:
        for original, data in name_map.items():
            lines.append(f"- {original} -> {data['replacement']} ({data['origin']}, {data['gender']})")
    else:
        lines.append("- No names were detected automatically. Identify characters manually before rewriting.")
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a story-time rewrite asset package.")
    parser.add_argument("--input", required=True, help="Path to the source story/script text file.")
    parser.add_argument("--story-name", help="Story folder name. Defaults to input filename.")
    parser.add_argument("--output-root", default="asset", help="Root output folder. Defaults to asset.")
    parser.add_argument("--edited-file", help="Optional completed rewrite to copy into edited.txt.")
    parser.add_argument("--name-limit", type=int, default=40, help="Maximum detected names to map.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    source_text = input_path.read_text(encoding="utf-8-sig")
    story_name = infer_story_name(input_path, args.story_name)
    story_folder = Path(args.output_root) / story_name
    original_folder = story_folder / "original script"
    edited_folder = story_folder / "edited script"
    original_folder.mkdir(parents=True, exist_ok=True)
    edited_folder.mkdir(parents=True, exist_ok=True)

    detected = detect_names(source_text, args.name_limit)
    name_map = build_name_map(detected)

    (original_folder / "original.txt").write_text(source_text, encoding="utf-8")
    (edited_folder / "name_map.json").write_text(
        json.dumps(name_map, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (edited_folder / "rewrite_prompt.md").write_text(
        rewrite_prompt(story_name, name_map),
        encoding="utf-8",
    )

    if args.edited_file:
        edited_text = Path(args.edited_file).read_text(encoding="utf-8-sig")
        (edited_folder / "edited.txt").write_text(edited_text, encoding="utf-8")

    print(json.dumps({
        "story_folder": str(story_folder),
        "original": str(original_folder / "original.txt"),
        "edited": str(edited_folder / "edited.txt"),
        "name_map": str(edited_folder / "name_map.json"),
        "rewrite_prompt": str(edited_folder / "rewrite_prompt.md"),
        "detected_names": len(name_map),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
