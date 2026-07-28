#!/usr/bin/env python3
"""Write manual scene image overrides for the Stolen Innocence edit."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


PACKAGE = Path(r"C:\Social Content\Asset\Stolen Innocence")


def main() -> int:
    overrides = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "notes": [
            "Scene 003 is intentionally a two-image beat under one narration sentence.",
            "First image shows the dog eating the food before the girl knows.",
            "Second image shows the aftermath/chase when she discovers it.",
        ],
        "scene_image_overrides": {
            "scene-003": [
                {
                    "id": "scene-003a-before",
                    "path": str(PACKAGE / "images" / "scene-003a-before.png"),
                    "role": "before",
                    "description": "Koko eating the food while Amara is absent.",
                },
                {
                    "id": "scene-003b-after",
                    "path": str(PACKAGE / "images" / "scene-003b-after.png"),
                    "role": "after",
                    "description": "Koko running from the eaten plate while Amara rushes after him.",
                },
            ]
        },
    }
    path = PACKAGE / "scene-image-overrides.json"
    path.write_text(json.dumps(overrides, indent=2), encoding="utf-8")
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
