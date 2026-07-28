#!/usr/bin/env python3
"""Rebuild the Stolen Innocence package for sentence-level ComfyUI generation."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path


ROOT = Path(r"C:\Social Content")
PACKAGE = ROOT / "Asset" / "Stolen Innocence"
WORKFLOW_TEMPLATE = ROOT / "Asset" / "workflows" / "nigerian-boy-playing-in-mud-krea2-api-fixed-qwen-vae-512.json"
OUTPUT_PREFIX = "stolen_innocence_v8"


BASE_NEGATIVE = (
    "text, captions, subtitles, logo, watermark, signature, poster typography, title card, "
    "split screen, multi-panel, triptych, diptych, collage, storyboard, comic panels, contact sheet, "
    "same person repeated, same character repeated, multiple ages, multiple outfits, "
    "direct eye contact with camera, looking at camera, passport photo, mugshot, static portrait pose, "
    "cartoon, anime, illustration, CGI, plastic skin, waxy skin, over-smoothed face, blurry, "
    "pixelated, low resolution, malformed hands, extra fingers, missing fingers, deformed face, "
    "duplicate people, distorted limbs, gore, nudity, sexualized child, explicit violence"
)

SINGLE_SUBJECT_NEGATIVE = "group photo, crowd, multiple people, two people, three people, multiple faces, multiple bodies, background person, distant person, blurred person, human silhouette"
TWO_SUBJECT_NEGATIVE = "group photo, crowd, three people, more than two people, extra faces, extra bodies"
GROUP_SUBJECT_NEGATIVE = "crowd collage, many repeated faces, extra foreground characters"
ANIMAL_SUBJECT_NEGATIVE = "person, people, child, girl, boy, woman, man, human face, human body, human silhouette, background person, blurred person"


PRODUCTION_SCRIPT = """I was twelve when trouble entered our house wearing the face of kindness.
My parents and older siblings had gone to the farm, and because chicken pox covered my skin, they left me at home with my cousin Somto.
Somto slipped out to meet her friends, and when hunger woke me, I found our dog Koko eating the food she had left for me.
That was when Elder Okoro, our lonely neighbor and family friend, called me over and gave me food from his kitchen.
I was a child, so I thought he was helping me.
I did not know that one meal would open a door I would spend years trying to close.
That night, I found myself in a terrifying gathering of people dressed in black, and Elder Okoro told me I now belonged among special people.
He gave me a small calabash in that dream and told me to hide it under my parents' bamboo bed if I wanted my father to become rich.
He also warned me that if I told anyone, my father would die.
When I woke and saw the same calabash beside my bed, fear and hope confused me, so I obeyed.
Three days later, my mother's scream tore me out of sleep.
My father was lying on the bed with his leg covered and swollen, and Elder Okoro blamed me, saying I had placed the calabash wrongly.
I was only a child, but guilt became heavier than my own body.
My father never recovered.
The hospital called it cancer, but Elder Okoro kept whispering that I had caused it, and when my father died, I believed him.
After the burial, I tried to avoid that man and the dark meetings, but they kept appearing in my dreams.
For a while, my family began to breathe again.
My sister Nkechi married a wealthy man in the city, and my brother Chidera gained admission to university.
Then one night, after Somto heard me begging my dead father for forgiveness in my sleep, she threatened to tell my mother.
Before I could explain, Somto collapsed in our room and never woke up.
Elder Okoro smiled at me while everyone cried and said he had only done what my anger had wished.
From that day, I became afraid of my own thoughts.
I avoided friends, avoided laughter, and avoided anyone who got too close, because people around me kept dying.
After a cruel teacher punished me at school, she drowned soon after.
When Auntie Ese visited and her daughter Tega shared my room, I stayed awake all night trying to protect her.
By morning, Tega was gone too.
That was when Elder Okoro told me the truth he wanted me to live under.
Every year, he said, I was expected to offer someone, and if I refused, they would choose for me.
My mother must have sensed that something dark was circling me, because after the family arguments and accusations, she sent me to live with my sister Nkechi in Warri.
I hoped distance would save the people I loved.
Warri felt like another world, full of tarred roads, tall buildings, and a room that looked too beautiful for someone like me.
At dinner, Nkechi's husband Tare asked me to pray before eating.
When he said the name of Jesus, heat rushed through me, and for the first time in years, the night passed without that evil gathering.
For six days, morning and night devotion kept the dreams away.
I started lessons for my exams and tried to live like a normal girl, but fear still sat beside me.
Then I met Kene, a smiling boy who noticed me when I tried to disappear.
I ignored him because I did not want another innocent person pulled into my curse.
But when I got lost after class, Kene walked me safely to my sister's gate and left before I could even thank him.
That was the first time I wondered if my life could still hold kindness without turning it into death.
I was not free yet.
Elder Okoro and the darkness had not been defeated.
But in that new house, with prayer covering the walls and a stranger refusing to treat me like a monster, I began to believe that stolen innocence might still find its way back to light."""


CHARACTERS = {
    "Amara": {
        "role": "protagonist and narrator",
        "age_voice": "young woman reflecting on childhood trauma",
        "visual_lock": (
            "Amara, a slim Nigerian girl, age 12 in village scenes and 15 in Warri scenes, "
            "warm dark-brown skin with visible pores, faint chicken-pox marks on her cheeks and arms, "
            "slight under-eye shadows, almond-shaped dark brown eyes, full lips, small rounded nose, "
            "natural black cornrow braids; in village home scenes she wears a faded mustard-yellow cotton dress, "
            "in school scenes a dull blue school uniform with white collar, in Warri scenes a pale lavender blouse and dark navy skirt"
        ),
    },
    "Elder Okoro": {
        "role": "neighbor and manipulator",
        "visual_lock": (
            "Elder Okoro, elderly Nigerian man in his late 60s, thin angular face, deep forehead lines, "
            "grey stubble, sunken cheeks, clouded brown eyes, rough weathered dark-brown skin with visible pores, "
            "wearing a faded off-white short-sleeve shirt, loose brown trousers, and worn leather sandals"
        ),
    },
    "Somto": {
        "role": "cousin",
        "visual_lock": (
            "Somto, teenage Nigerian girl around 14, warm brown skin with tiny acne marks, round face, "
            "neat black braids, expressive eyes, wearing a green patterned blouse and dark wrapper"
        ),
    },
    "Mother": {
        "role": "Amara's mother",
        "visual_lock": (
            "Amara's mother, Nigerian woman in her early 40s, tired compassionate face, dark-brown skin with natural texture, "
            "tied black headscarf, simple rust-orange blouse and wrapper"
        ),
    },
    "Father": {
        "role": "Amara's father",
        "visual_lock": (
            "Amara's father, Nigerian man in his late 40s, lean frame, short black hair, sparse beard, "
            "wearing a faded cream singlet and brown wrapper, shown weak but non-graphic"
        ),
    },
    "Nkechi": {
        "role": "older sister",
        "visual_lock": (
            "Nkechi, Nigerian woman in her late 20s, smooth dark-brown skin with realistic pores, oval face, "
            "neatly braided hair, wearing a modest teal dress in Warri home scenes"
        ),
    },
    "Tare": {
        "role": "Nkechi's husband",
        "visual_lock": (
            "Tare, Nigerian man in his early 30s, clean-shaven, calm face, medium-brown skin, "
            "wearing a crisp light-blue button-down shirt"
        ),
    },
    "Kene": {
        "role": "kind classmate",
        "visual_lock": (
            "Kene, Nigerian teenage boy around 16, medium-brown skin with light acne texture, short cropped black hair, "
            "bright attentive eyes, wearing a neat white school shirt and charcoal trousers"
        ),
    },
}


VISUAL_LOCKS = {
    "Amara village": (
        "Amara only, one slim Nigerian girl age 12, warm dark-brown skin with visible pores, "
        "faint chicken-pox marks on her cheeks and arms, slight under-eye shadows, almond-shaped dark brown eyes, "
        "full lips, small rounded nose, same natural black cornrow braids falling back from her forehead, never low cut, never short hair, wearing one faded mustard-yellow cotton dress"
    ),
    "Amara school": (
        "Amara only, one Nigerian teenage girl age 15, slim build, warm dark-brown skin with visible pores, "
        "faint old chicken-pox marks on her cheeks, almond-shaped dark brown eyes, full lips, small rounded nose, "
        "same natural black braids, never low cut, never short hair, wearing one dull blue school uniform with a white collar"
    ),
    "Amara Warri": (
        "Amara only, one Nigerian teenage girl age 15, slim build, warm dark-brown skin with visible pores, "
        "faint old chicken-pox marks on her cheeks, almond-shaped dark brown eyes, full lips, small rounded nose, "
        "same natural black braids, never low cut, never short hair, wearing one pale lavender blouse and one dark navy skirt"
    ),
    "Elder Okoro": (
        "Elder Okoro only, one elderly Nigerian man in his late 60s, thin angular face, deep forehead lines, "
        "grey stubble, sunken cheeks, clouded brown eyes, rough weathered dark-brown skin with visible pores, "
        "wearing one faded off-white short-sleeve shirt, loose brown trousers, and worn leather sandals"
    ),
    "Somto": (
        "Somto only, one teenage Nigerian girl around 14, warm brown skin with tiny acne marks, round face, "
        "neat black braids, expressive eyes, wearing one green patterned blouse and dark wrapper"
    ),
    "Mother": (
        "Amara's mother only, one Nigerian woman in her early 40s, tired compassionate face, dark-brown skin with natural texture, "
        "tied black headscarf, wearing one simple rust-orange blouse and wrapper"
    ),
    "Father": (
        "Amara's father only, one Nigerian man in his late 40s, lean frame, short black hair, sparse beard, "
        "wearing one faded cream singlet and brown wrapper, shown weak but non-graphic"
    ),
    "Nkechi": (
        "Nkechi only, one Nigerian woman in her late 20s, smooth dark-brown skin with realistic pores, oval face, "
        "neatly braided hair, wearing one modest teal dress"
    ),
    "Tare": (
        "Tare only, one Nigerian man in his early 30s, clean-shaven calm face, medium-brown skin, "
        "wearing one crisp light-blue button-down shirt"
    ),
    "Kene": (
        "Kene only, one Nigerian teenage boy around 16, medium-brown skin with light acne texture, short cropped black hair, "
        "bright attentive eyes, wearing one neat white school shirt and charcoal trousers"
    ),
}


def amara_lock(sentence: str, index: int) -> str:
    s = sentence.lower()
    if index >= 31 or any(word in s for word in ("warri", "dinner", "pray", "jesus", "devotion", "nkechi", "tare", "room that looked", "new house", "light")):
        return VISUAL_LOCKS["Amara Warri"]
    if any(word in s for word in ("school", "teacher", "lessons", "exams", "class", "kene", "sister's gate")):
        return VISUAL_LOCKS["Amara school"]
    return VISUAL_LOCKS["Amara village"]


def split_sentences(text: str) -> list[str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return lines


def allow_with_others(lock: str) -> str:
    return lock.replace(" only,", ",").replace(" only", "")


def pick_visual(sentence: str, index: int) -> tuple[str, str, str, str, str]:
    s = sentence.lower()
    if "farm" in s or "chicken pox" in s:
        return ("Village bedroom", "single", amara_lock(sentence, index), "the girl sits weakly on the edge of a bamboo bed, one hand touching the chicken-pox marks on her arm, worried eyes turned slightly away from camera", "small rural Nigerian bedroom with bamboo bed, cracked mud wall, morning daylight; no other people visible")
    if "dog koko" in s or "food" in s and "kitchen" not in s:
        people = "Koko, one small lean brown village dog with short fur, dusty paws, realistic wet nose, and natural dog anatomy; Amara, one slim Nigerian girl age 12 with the same natural black cornrow braids falling back from her forehead, never low cut, never short hair, wearing one faded mustard-yellow cotton dress"
        return ("Dog ran from the eaten food", "two", people, "the dog bolts away from an almost-empty metal plate with crumbs and scattered food, body low and mid-run; the girl rushes after the dog from behind with one arm stretched out and panic on her face, her black cornrow braids clearly visible and moving with her, caught mid-motion, not calmly watching", "rural Nigerian compound courtyard, low stool with almost-empty metal plate, spilled crumbs on dusty ground, urgent afternoon action, exactly one dog and one girl visible")
    if "elder okoro" in s and ("food" in s or "kitchen" in s or "called" in s):
        people = allow_with_others(amara_lock(sentence, index)) + "; " + allow_with_others(VISUAL_LOCKS["Elder Okoro"])
        return ("Neighbor kitchen", "two", people, "the girl hesitantly receives an enamel bowl of rice with both hands, cautious expression, the elderly man leaning forward from the foreground", "dim old neighbor kitchen, over-the-shoulder shot from behind the elderly man's shoulder toward the girl holding an enamel bowl of rice; exactly two people visible")
    if "gathering" in s or "black" in s or "special people" in s:
        return ("Night fear", "group", allow_with_others(amara_lock(sentence, index)), "the girl turns sharply over her shoulder in terror, lips parted, hands drawn close to her chest, body half-twisted as if trying to escape", "close-up reaction shot of the girl's face in moonlight, with a distant small group of black-clothed adults only as soft blurred silhouettes behind her, no clear extra faces, no collage")
    if "calabash" in s and "bed" in s:
        return ("Calabash under bed", "single", amara_lock(sentence, index), "the girl crouches beside the bamboo bed, one hand pushing a small plain calabash underneath, face tight with fear and confusion", "rural bedroom at night, bamboo bed, small plain calabash on woven mat, lantern light; no other people visible")
    if "warned" in s or "father would die" in s:
        people = allow_with_others(VISUAL_LOCKS["Elder Okoro"]) + "; " + allow_with_others(amara_lock(sentence, index))
        return ("Threat warning", "two", people, "the elderly man leans close and raises one warning finger, hard stare, the girl recoils in the foreground with hunched shoulders", "tight tense over-the-shoulder shot from behind the girl toward the elderly man near a doorway, deep evening shadows; exactly two people visible")
    if "mother" in s and "scream" in s:
        return ("Mother screams", "single", VISUAL_LOCKS["Mother"], "the mother throws one hand to her mouth mid-scream, eyes wide, body leaning toward the bed in panic", "rural bedroom dawn, mother frozen in panic beside a rumpled mosquito net, no other people visible")
    if "father" in s and ("bed" in s or "recovered" in s or "hospital" in s or "died" in s):
        return ("Father illness", "single", VISUAL_LOCKS["Father"], "the father lies weakly on a bed, one hand gripping the sheet, face strained and exhausted, covered leg kept non-graphic", "modest bedroom or hospital corner, muted light, covered leg, non-graphic illness, no other people visible")
    if "burial" in s:
        return ("Burial grief", "group", allow_with_others(amara_lock(sentence, index)), "the girl wipes tears with the back of her hand, shoulders collapsed, looking down rather than at camera", "close-up reaction shot of the girl grieving in a rural compound, with a distant blurred burial gathering in the background, red earth, overcast sky, no readable signs, no collage")
    if "nkechi married" in s or "university" in s:
        return ("Family relief", "single", amara_lock(sentence, index), "the girl sits at a table touching an unreadable paper, a fragile half-smile on her face, cautious relief in her posture", "family room with modest celebration implied by blurred decorations and an unreadable paper on a table, no other people visible")
    if "somto" in s and ("sleep" in s or "collapsed" in s or "woke up" in s):
        people = allow_with_others(VISUAL_LOCKS["Somto"]) + "; " + allow_with_others(amara_lock(sentence, index))
        return ("Somto tragedy", "two", people, "the cousin slumps beside a sleeping mat while the girl reaches toward her in panic, both bodies caught mid-motion, non-graphic", "small shared bedroom at night, over-the-shoulder shot from behind the girl toward her cousin, kerosene lantern, frightened stillness, non-graphic collapse implied; exactly two people visible")
    if "smiled" in s and "cried" in s:
        return ("Cold smile", "group", allow_with_others(VISUAL_LOCKS["Elder Okoro"]), "the elderly man gives a small controlled smile while turning away from crying mourners, eyes cold, body relaxed in a disturbing way", "close-up front view of the elderly man in a village room doorway, blurred mourners at the edge of frame looking toward him, sinister calm focus, no collage")
    if "school" in s or "teacher" in s:
        return ("School fear", "single", amara_lock(sentence, index), "the girl clutches her school books against her chest, shoulders raised, eyes lowered in shame and fear, body angled away from camera", "Nigerian classroom with wooden desks, chalkboard blurred with no readable text, dusty daylight, no other people visible")
    if "auntie" in s or "tega" in s:
        return ("Sleepless protection", "single", amara_lock(sentence, index), "the girl sits upright all night beside a sleeping mat, tense hands clasped around her knees, eyes fixed anxiously toward the doorway", "guest bedroom at night, two sleeping mats, the girl sitting awake alone, lantern glow, no other people visible")
    if "every year" in s or "offer someone" in s or "choose for me" in s:
        people = allow_with_others(VISUAL_LOCKS["Elder Okoro"]) + "; " + allow_with_others(amara_lock(sentence, index))
        return ("Ultimatum", "two", people, "the elderly man points toward the girl while speaking, the girl steps backward with one hand raised defensively, tension in both bodies", "dark narrow footpath under heavy trees, over-the-shoulder shot from behind the girl toward the elderly man, oppressive dusk; exactly two people visible")
    if "warri" in s or "tarred roads" in s or "tall buildings" in s:
        return ("Arrival in Warri", "single", amara_lock(sentence, index), "the teenage girl stands at a painted compound gate gripping a small bag, head tilted upward in overwhelmed wonder and fear", "Warri street with tarred road and painted compound gate, warm city afternoon, no other people visible")
    if "dinner" in s or "pray" in s or "jesus" in s or "devotion" in s:
        people = allow_with_others(amara_lock(sentence, index)) + "; " + allow_with_others(VISUAL_LOCKS["Tare"]) + "; " + allow_with_others(VISUAL_LOCKS["Nkechi"])
        return ("Prayer at dinner", "group", people, "the man bows his head and extends one hand in prayer, the woman watches quietly beside him, the girl partly foregrounded with tense shoulders", "front-view composition of the man leading prayer and the woman beside him looking toward the girl at the dinner table, the girl partly foregrounded from behind, warm bulb light, no readable text")
    if "lessons" in s or "exams" in s:
        return ("Exam lessons", "single", amara_lock(sentence, index), "the teenage girl bends over an exercise book with a pencil in hand, brows furrowed, trying to concentrate while anxiety remains in her posture", "small lesson classroom, exercise books with no readable writing, window light, cautious hope, no other people visible")
    if "kene" in s or "smiling boy" in s or "sister's gate" in s:
        people = allow_with_others(VISUAL_LOCKS["Kene"]) + "; " + allow_with_others(amara_lock(sentence, index))
        return ("Kene kindness", "two", people, "the boy walks beside the girl at a respectful distance, one hand gesturing toward the safe path, the girl turns slightly toward him with guarded surprise", "quiet Warri street near compound gate, side-by-side walking shot with respectful distance, late afternoon; exactly two people visible")
    if "not free" in s or "darkness" in s:
        return ("Unfinished shadow", "single", amara_lock(sentence, index), "the teenage girl sits on the bed edge with both hands clenched in her lap, staring toward a dark corner with guarded fear", "quiet bedroom at night, soft prayer light on wall, dark corner receding, no symbols or text, no other people visible")
    if "light" in s:
        return ("Hope returns", "single", amara_lock(sentence, index), "the teenage girl slowly opens a curtain at dawn, sunlight crossing her face, cautious hope in her eyes and relaxed shoulders", "Warri bedroom at dawn, sunlight crossing the girl's face, hopeful but cautious expression, no other people visible")
    return ("Reflective close-up", "single", amara_lock(sentence, index), "side-profile candid close-up from a 45-degree angle, the girl pauses mid-breath with one hand at her chest, head turned left, eyes looking down toward the floor, not facing camera", "cinematic close-up in rural Nigerian home, natural light, emotional first-person memory, no other people visible")


def make_prompt(sentence: str, index: int) -> dict:
    title, visual_mode, people, action, setting = pick_visual(sentence, index)
    if visual_mode == "single":
        subject_rule = (
            f"Selected visible subject: {people}. Only this one human subject is visible in the frame. "
            "Do not show other named characters, friends, relatives, crowds, or repeated versions of the same person. "
        )
        negative_prompt = BASE_NEGATIVE + ", " + SINGLE_SUBJECT_NEGATIVE
    elif visual_mode == "two":
        subject_rule = (
            f"Visible subjects: {people}. Exactly two visible subjects are in one natural interaction shot. "
            "Use the specified over-the-shoulder, facing-each-other, side-by-side, or close-up reaction composition; do not add a third person or repeat either character. "
        )
        negative_prompt = BASE_NEGATIVE + ", " + TWO_SUBJECT_NEGATIVE + ", extra animals, duplicate dog, duplicate girl, low cut hair, shaved head, buzz cut, short cropped hair"
    else:
        subject_rule = (
            f"Visible composition: {people}. Use the specified controlled multi-character composition: over-the-shoulder, close-up reaction of one character, or front-view people looking toward one character. "
            "Keep one clear viewpoint and control other people as background or edge-of-frame figures. "
            "Do not make a group portrait, collage, contact sheet, or repeated-character layout. "
        )
        negative_prompt = BASE_NEGATIVE + ", " + GROUP_SUBJECT_NEGATIVE
    if visual_mode == "animal":
        subject_rule = (
            f"Selected visible subject: {people}. Only this one animal subject is visible in the frame. "
            "Do not show Amara or any human character; the story context is carried by the caption, not by extra people in the image. "
        )
        negative_prompt = BASE_NEGATIVE + ", " + ANIMAL_SUBJECT_NEGATIVE
    prompt = (
        f"Ultra-realistic cinematic Nigerian drama still, vertical portrait composition, single full-frame photograph only, one continuous image, no panels, no split-screen, no storyboard. "
        f"Moment: {title}. "
        "The caption sentence is handled separately, so do not add story text or extra named characters into the image. "
        f"{subject_rule}"
        f"Action and expression: {action}. "
        "Do not pose the subject plainly looking into the camera; use a candid three-quarter angle, side gaze, downward gaze, or gaze toward another character/object in the scene. "
        "Capture an active candid story moment with matching facial expression, body movement, hands, posture, and emotional tension. "
        f"Environment: {setting}. "
        "Photography style: high-quality live-action film still, one camera angle, one moment, natural skin texture with visible pores, faint facial imperfections, "
        "realistic fabric weave, believable Nigerian home and street details, expressive eyes, emotionally restrained performance, "
        "shallow depth of field, soft natural lighting, subtle film grain, detailed shadows, no exaggerated horror, no gore, "
        "no text in the image, no captions, no signage, no watermark, no logo."
    )
    return {
        "id": f"scene-{index:03d}",
        "title": title,
        "visual_mode": visual_mode,
        "sentence": sentence,
        "prompt": prompt,
        "negative_prompt": negative_prompt,
    }


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    sentences = split_sentences(PRODUCTION_SCRIPT)
    prompts = [make_prompt(sentence, i + 1) for i, sentence in enumerate(sentences)]
    now = datetime.now().isoformat(timespec="seconds")

    (PACKAGE / "screenwriter").mkdir(parents=True, exist_ok=True)
    (PACKAGE / "shotlist").mkdir(parents=True, exist_ok=True)
    (PACKAGE / "director" / "prompts").mkdir(parents=True, exist_ok=True)
    (PACKAGE / "comfyui-workflows").mkdir(parents=True, exist_ok=True)
    (PACKAGE / "audio").mkdir(parents=True, exist_ok=True)

    screenplay_lines = [
        "# Stolen Innocence - Production Narration Script",
        "",
        f"Generated: {now}",
        "Narrator identity: young Nigerian woman, first-person reflective voice, recalling events that began when she was twelve.",
        "Voice persona for Chatterbox: young woman -> Rho_female.",
        "Visual rule: one ComfyUI image for every sentence below; images must contain no text.",
        "",
        "## Narration Sentences",
        "",
    ]
    for item in prompts:
        screenplay_lines.append(f"### {item['id']}")
        screenplay_lines.append(item["sentence"])
        screenplay_lines.append("")
    write_text(PACKAGE / "screenwriter" / "production-script.md", "\n".join(screenplay_lines).rstrip() + "\n")
    write_text(PACKAGE / "audio" / "narration-lines.txt", "\n".join(sentences) + "\n")

    character_bible = {
        "generated_at": now,
        "story": "Stolen Innocence",
        "narrator": {
            "persona": "young woman",
            "voice": "Rho_female",
            "reason": "The story is narrated by Amara as an older version of the girl who experienced the events.",
        },
        "characters": CHARACTERS,
        "visual_locks_note": "Reuse these descriptions in every prompt to preserve face, clothing, age, and texture continuity.",
    }
    write_text(PACKAGE / "character-bible.json", json.dumps(character_bible, indent=2, ensure_ascii=False) + "\n")

    shotlist = []
    md = ["# Stolen Innocence - Sentence-Level Shotlist", ""]
    for item in prompts:
        shot = {
            "id": item["id"],
            "sentence": item["sentence"],
            "shot_type": "vertical cinematic still",
            "image_path_target": str(PACKAGE / "images" / f"{item['id']}.png"),
            "caption": item["sentence"],
            "prompt_path": str(PACKAGE / "director" / "prompts" / f"{item['id']}.txt"),
            "workflow_path": str(PACKAGE / "comfyui-workflows" / f"{item['id']}-workflow.json"),
        }
        shotlist.append(shot)
        md.extend([
            f"## {item['id']} - {item['title']}",
            f"Sentence: {item['sentence']}",
            "Shot: Vertical ultra-realistic cinematic still, 9:16, no baked-in text.",
            f"Target image: `{shot['image_path_target']}`",
            "",
        ])
        write_text(PACKAGE / "director" / "prompts" / f"{item['id']}.txt", item["prompt"] + "\n\nNegative prompt: " + item["negative_prompt"] + "\n")
    write_text(PACKAGE / "shotlist" / "shotlist.md", "\n".join(md).rstrip() + "\n")
    write_text(PACKAGE / "shotlist" / "shotlist.json", json.dumps({"generated_at": now, "shots": shotlist}, indent=2, ensure_ascii=False) + "\n")
    write_text(PACKAGE / "scene-beats.json", json.dumps({"generated_at": now, "scene_count": len(prompts), "scenes": prompts}, indent=2, ensure_ascii=False) + "\n")

    image_prompt_md = ["# Stolen Innocence - ComfyUI Image Prompts", ""]
    template = json.loads(WORKFLOW_TEMPLATE.read_text(encoding="utf-8"))
    for i, item in enumerate(prompts, start=1):
        image_prompt_md.extend([f"## {item['id']} - {item['title']}", item["prompt"], "", f"Negative: {item['negative_prompt']}", ""])
        workflow = json.loads(json.dumps(template))
        workflow["3"]["inputs"]["text"] = item["prompt"] + " Negative prompt: " + item["negative_prompt"]
        workflow["5"]["inputs"]["width"] = 576
        workflow["5"]["inputs"]["height"] = 864
        workflow["6"]["inputs"]["seed"] = 71000000 + i * 137
        workflow["6"]["inputs"]["steps"] = 28
        workflow["9"]["inputs"]["filename_prefix"] = f"{OUTPUT_PREFIX}_{item['id']}"
        write_text(PACKAGE / "comfyui-workflows" / f"{item['id']}-workflow.json", json.dumps(workflow, indent=2, ensure_ascii=False) + "\n")
    write_text(PACKAGE / "image-prompts.md", "\n".join(image_prompt_md).rstrip() + "\n")

    manifest = {
        "generated_at": now,
        "story": "Stolen Innocence",
        "source_url": "https://www.ebonystory.com/story/stolen-innocence/episode-1",
        "rights": "Unconfirmed source rights; use as private review unless rights are cleared.",
        "scene_count": len(prompts),
        "narrator": character_bible["narrator"],
        "workflow_template": str(WORKFLOW_TEMPLATE),
        "outputs": {
            "production_script": str(PACKAGE / "screenwriter" / "production-script.md"),
            "shotlist": str(PACKAGE / "shotlist" / "shotlist.json"),
            "scene_beats": str(PACKAGE / "scene-beats.json"),
            "image_prompts": str(PACKAGE / "image-prompts.md"),
            "narration_lines": str(PACKAGE / "audio" / "narration-lines.txt"),
            "comfyui_workflows": str(PACKAGE / "comfyui-workflows"),
        },
    }
    write_text(PACKAGE / "restart-production-manifest.json", json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"package": str(PACKAGE), "scene_count": len(prompts)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
