#!/usr/bin/env python3
"""Build the long-form continuation package from Elder Okoro encounter onward."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


ROOT = Path(r"C:\Social Content")
PACKAGE = ROOT / "Asset" / "Stolen Innocence"
WORKFLOW_TEMPLATE = ROOT / "Asset" / "workflows" / "nigerian-boy-playing-in-mud-krea2-api-fixed-qwen-vae-512.json"
PART = "continuation-part-001"
OUTPUT_PREFIX = "stolen_innocence_long_p1"


BASE_NEGATIVE = (
    "text, captions, subtitles, logo, watermark, signature, poster typography, title card, split screen, multi-panel, "
    "triptych, diptych, collage, storyboard, comic panels, contact sheet, same person repeated, same character repeated, "
    "multiple ages, multiple outfits, direct eye contact with camera unless specified, passport photo, mugshot, static portrait pose, "
    "cartoon, anime, illustration, CGI, plastic skin, waxy skin, over-smoothed face, blurry, pixelated, low resolution, "
    "malformed hands, extra fingers, missing fingers, deformed face, duplicate people, distorted limbs, gore, nudity, sexualized child"
)


CHARACTER_LOCKS = {
    "Amara": "Amara, Nigerian girl age 12, slim, warm dark-brown skin with visible pores and faint chicken-pox marks on cheeks and arms, almond dark-brown eyes, full lips, same natural black cornrow braids falling back from forehead, faded mustard-yellow cotton dress, no low cut, no short hair",
    "Somto": "Somto, Nigerian teenage girl around 14, warm brown skin with tiny acne marks, round face, neat black braids, green patterned blouse and dark wrapper",
    "Elder Okoro": "Elder Okoro, elderly Nigerian man late 60s, thin angular face, deep forehead lines, grey stubble, sunken cheeks, clouded brown eyes, rough weathered dark-brown skin, faded off-white short-sleeve shirt, loose brown trousers, worn leather sandals",
    "Mother": "Amara's mother, Nigerian woman early 40s, tired compassionate face, dark-brown textured skin, tied black headscarf, rust-orange blouse and wrapper",
    "Father": "Amara's father, Nigerian man late 40s, lean frame, short black hair, sparse beard, faded cream singlet and brown wrapper",
    "Koko": "Koko, small lean brown village dog with short fur, dusty paws, realistic wet nose and natural dog anatomy",
}


SHOT_CHARACTERS = {
    "p001-s001": ["Amara", "Elder Okoro"],
    "p001-s002": ["Amara", "Elder Okoro"],
    "p001-s003": ["Amara", "Elder Okoro"],
    "p001-s004": ["Elder Okoro"],
    "p001-s005": ["Amara"],
    "p001-s006": ["Amara", "Elder Okoro"],
    "p001-s007": [],
    "p001-s008": ["Amara"],
    "p001-s009": ["Elder Okoro"],
    "p001-s010": ["Somto"],
    "p001-s011": ["Amara", "Somto"],
    "p001-s012": ["Somto"],
    "p001-s013": ["Amara", "Mother", "Father"],
    "p001-s014": ["Amara", "Somto", "Father"],
    "p001-s015": ["Mother"],
    "p001-s016": [],
    "p001-s017": ["Amara"],
    "p001-s018": ["Amara", "Elder Okoro"],
    "p001-s019": ["Amara", "Elder Okoro"],
    "p001-s020": ["Elder Okoro"],
    "p001-s021": ["Amara"],
    "p001-s022": ["Amara"],
    "p001-s023": ["Elder Okoro"],
    "p001-s024": [],
    "p001-s025": ["Elder Okoro"],
    "p001-s026": ["Elder Okoro"],
    "p001-s027": ["Amara"],
    "p001-s028": ["Amara", "Somto"],
    "p001-s029": ["Amara"],
    "p001-s030": ["Amara", "Somto"],
    "p001-s031": ["Amara"],
    "p001-s032": [],
    "p001-s033": ["Amara", "Father"],
    "p001-s034": ["Amara", "Mother", "Elder Okoro"],
    "p001-s035": ["Amara", "Mother", "Elder Okoro"],
    "p001-s036": ["Amara"],
}


EXACT_MOMENTS = {
    "p001-s001": "Amara stands still on her side of the fence, facing Elder Okoro; Elder Okoro leans on the fence and studies her face.",
    "p001-s002": "Elder Okoro's mouth is open mid-sentence while he greets Amara; Amara listens with her hands hanging at her sides.",
    "p001-s003": "Elder Okoro's lower jaw is dropped mid-word, lips separated, dark mouth interior and a few teeth visible as he mentions the chicken pox; Amara lowers her chin and keeps her eyes on him.",
    "p001-s004": "Elder Okoro is captured in a three-quarter left-facing speaking close-up; his mouth is open wide mid-question as if pronouncing the word alone, lower jaw dropped, lips stretched apart, dark mouth interior and uneven teeth clearly visible; his eyes look left toward Amara off-camera.",
    "p001-s005": "Amara is captured mid-sentence while saying Koko ate my food; her mouth is wide open in a clear ah-shape, lower jaw dropped, lips separated, dark mouth interior and small teeth visible; her eyes look down with embarrassed hunger.",
    "p001-s006": "Elder Okoro's mouth is open mid-invitation as he tells Amara to come; his hands stay relaxed at his sides while Amara remains rooted near the fence.",
    "p001-s007": "A warm enamel bowl of food rests alone on a rough wooden surface.",
    "p001-s008": "Amara sits near Elder Okoro's doorway and eats from the enamel bowl.",
    "p001-s009": "Elder Okoro watches from the doorway with both hands resting on the door frame.",
    "p001-s010": "Somto is caught mid-sneak as she slips sideways through the compound doorway, one shoulder leading, torso twisted away from the camera, eyes looking left into the room instead of at the camera, her loose dark wrapper trailing behind her.",
    "p001-s011": "Amara's mouth is open mid-sentence as she tells Somto what happened; Somto turns her face toward the kitchen instead of toward Amara.",
    "p001-s012": "Somto stirs the pot quickly, her eyes fixed toward the compound entrance.",
    "p001-s013": "Amara is seen from behind while Mother bends toward her and Father stands beside the doorway with his cutlass lowered.",
    "p001-s014": "Amara's mouth is open mid-lie in the foreground; Somto stays blurred in the far corner with her shoulders lowered.",
    "p001-s015": "Mother's mouth is open mid-sentence as she decides to thank Elder Okoro.",
    "p001-s016": "A half moon hangs above the thatched roofs in an empty night sky.",
    "p001-s017": "Amara stands alone at the center of the black-gowned circle, turning her head in panic while the figures remain still.",
    "p001-s018": "Elder Okoro stands still in the midground between two soft black-gowned shoulders; Amara's shoulder stays blurred in the foreground.",
    "p001-s019": "Amara's mouth is open mid-cry as she asks Elder Okoro to take her home.",
    "p001-s020": "Elder Okoro's mouth is open mid-sentence in side profile as he tells Amara she is among special people.",
    "p001-s021": "Amara holds still in close-up, tears on her cheeks and her eyes lifted with dangerous hope.",
    "p001-s022": "Amara's mouth is open mid-question as she asks whether her father can become rich.",
    "p001-s023": "Elder Okoro extends both hands toward the camera, holding the calabash as the closest object in frame.",
    "p001-s024": "The dark calabash with a red thread sits alone in sharp focus.",
    "p001-s025": "Elder Okoro's mouth is open mid-instruction while he holds the calabash low against his body.",
    "p001-s026": "Elder Okoro's mouth is open mid-warning, his jaw tight and his eyes fixed off-frame toward Amara.",
    "p001-s027": "Amara clutches the calabash to her chest and whispers with her mouth slightly open.",
    "p001-s028": "Amara jolts upright on the sleeping mat while Somto sleeps beside her facing away.",
    "p001-s029": "From under the bamboo bed, the calabash sits in the foreground while Amara looks under the bed with wide eyes, raised brows, and parted lips.",
    "p001-s030": "Amara tiptoes past the sleeping mat while holding the calabash in both hands; Somto remains asleep behind her.",
    "p001-s031": "Amara stands at the threshold of her parents' room and looks toward the bamboo bed.",
    "p001-s032": "Amara's hand pushes the calabash under the bamboo bed.",
    "p001-s033": "Amara watches Father from the room edge with a small secret smile.",
    "p001-s034": "Mother's mouth is open mid-thank-you at Elder Okoro's doorway; Amara hides beside Mother's wrapper.",
    "p001-s035": "Elder Okoro's mouth is open mid-sentence as he says Amara is like his own child.",
    "p001-s036": "Amara looks back over her shoulder while walking away from Elder Okoro's compound.",
}


def lighting_for_shot(shot_id: str) -> str:
    if shot_id == "p001-s016":
        return "Night exterior: the half moon is the only visible light source; no lantern, no fill, no artificial glow."
    if shot_id in {"p001-s017", "p001-s018", "p001-s019", "p001-s020", "p001-s021", "p001-s022", "p001-s023", "p001-s024", "p001-s025", "p001-s026", "p001-s027"}:
        return "Dream night exterior: cold moonlight is the only light source; faces fall into natural shadow, no fire glow, no fill light."
    if shot_id in {"p001-s028", "p001-s029", "p001-s030", "p001-s031", "p001-s032"}:
        return "Night bedroom: one small kerosene lamp near Amara is the only light source; all shadows and highlights come from that lamp only."
    if shot_id in {"p001-s013", "p001-s014", "p001-s015", "p001-s033", "p001-s034", "p001-s035", "p001-s036"}:
        return "Daytime natural light only from the open doorway and visible sky; no fill, no extra light source."
    return "Daytime natural light only from the visible sky and open compound; no fill, no extra light source."


LONG_REWRITE = """As I came out of our kitchen, still hungry and confused, I saw Elder Okoro standing close to the fence that separated our compound from his.

He was an old man who lived alone, and because he was a family friend, I did not think there was anything strange about him calling me.

"Amara," he said, leaning on the rough wooden fence as if he had been waiting there for me, "how are you?"

I wiped my hands on my faded yellow dress and answered, "Good afternoon, sir. I am fine."

His eyes moved over my face and arms, where the chicken pox had left angry little marks. "I heard you have chicken pox," he said. "That is why you could not follow your parents to the farm today."

"Yes, sir," I said quietly.

He looked past me into our compound. The house was silent. The kitchen door was still open. Somto was nowhere around.

"So you are alone?" he asked.

For a moment I did not want to answer. My mother had told us not to advertise that nobody was home, but Elder Okoro was not a stranger. He had eaten in our house before. My father greeted him like an elder.

"Yes, sir," I said.

He tilted his head and studied me again. "You do not look happy. What is wrong?"

My throat tightened because I was hungry and embarrassed. "Koko ate my food," I said. "Somto left food for me in the kitchen, but when I woke up, the dog was already eating it."

"Ah," Elder Okoro said softly, as if my small trouble pained him. "Poor child. You are sick, and they left you hungry."

"It is not like that, sir," I said quickly. "They went to the farm. They had to harvest maize."

He waved his hand. "Come. Do not worry. I have food in my kitchen."

I hesitated at the edge of our compound. "Sir, my mother is not around."

"Amara, am I not your father's friend?" he asked. His voice was gentle, but it also sounded like a question I was not supposed to refuse.

I followed him through the small side path to his house. His compound was quieter than ours. Even the air seemed heavier there. He entered his kitchen and came back with food in an enamel bowl.

"Eat," he said, placing it in my hands.

The food was warm. Steam rose into my face, and my stomach answered before my mind could think properly. I sat near his doorway and began to eat.

"Good girl," he said.

I looked up once, and he was watching me with a calm smile that I did not understand then. I only saw an old man helping a hungry child.

By the time Somto came back, the sun had shifted and my belly was full. She entered our room like someone who had been running, her wrapper tied carelessly and her eyes bright from whatever fun she had gone to enjoy.

"You are awake?" she asked.

"Koko ate my food," I told her.

She stopped for only a second. "Eh?"

"I woke up and saw him eating it. Elder Okoro gave me food from his house."

Somto did not look worried. She only rushed toward the kitchen. "Our parents will soon come back. I need to cook before they know I left."

"I will not tell them," I said.

She glanced at me, relieved but still pretending not to care. "You better not. You know you were sleeping when I went out."

When my parents returned from the farm, their clothes smelled of sun, soil, and maize leaves. My mother came to my mat first and touched my forehead.

"How is your body now?" she asked.

"Better, Mama," I said.

My father dropped his cutlass near the door and asked, "Did you eat?"

I nodded. "Koko ate my food, but Elder Okoro gave me food."

My mother's face changed. "Koko ate your food?"

I nodded again.

"Where was Somto?" my father asked.

Somto looked at me from the corner of the room. I could feel her fear like heat.

"She was sleeping," I lied. "I did not want to wake her."

My mother sighed, tired from the farm. "That man did well. Tomorrow I will go and thank him."

Somto avoided my eyes for the rest of the evening. I thought I had saved her from trouble. I did not know I had opened the wrong door.

That night, after the house became quiet, I slept beside Somto as usual. The chicken pox made my body itch, and the heat under the thatch roof made sleep uncomfortable, but sometime deep in the night, everything changed.

First, there was only the night sky.

The moon looked too large, hanging above the village like an eye. The clouds moved slowly across it, and the wind sounded like people whispering far away.

Then I was no longer on my mat.

I found myself standing in the middle of a gathering of people dressed in black gowns. They formed a wide circle around me. I was the youngest person there, and every face seemed hidden by shadow.

My breath caught. I turned around, searching for a door, a path, any way back home.

Then I saw Elder Okoro among them.

"Sir!" I cried, running toward him. "Please take me home. I want to go home."

He did not look surprised to see me. He looked as if he had expected me.

"Do not be afraid, Amara," he said.

"Where am I?" I asked. "Why am I here?"

"You are among special people now," he said. "People who can receive what ordinary people beg for."

I shook my head. "I do not want to be here."

"You are a child," he said, bending slightly so his face came closer to mine. "You do not understand yet. Here, wishes can become real. Requests can be answered. Poverty can leave a family."

That word caught me.

Poverty.

I thought of my father returning from the farm with cracked palms. I thought of my mother counting garri and soup like every spoon mattered. I thought of my older siblings walking long distances because there was no money for transport.

My crying slowed.

Elder Okoro noticed. His voice became softer. "What do you want for your family?"

I swallowed. "Can you make my father rich?"

A few people in the circle murmured, but I could not understand their words.

Elder Okoro stretched out his hands, and someone placed a small calabash into them.

He turned back to me.

From where I stood, it felt as if the calabash was being handed straight into my hands.

"Take it," he said. "Hide it under your parents' bamboo bed."

I stared at it. The calabash was smooth and dark, tied with a thin red thread around its neck.

"If I put it there, my father will be rich?" I asked.

"Your family will begin to rise," he said.

"Can I tell my mother?"

His face hardened so quickly that I stepped back.

"You must not tell anyone," he said. "Not your mother. Not your father. Not Somto. Nobody."

"Why?"

"Because if you tell them," he said slowly, "your father will die."

The circle became silent.

I held the calabash against my chest with shaking hands. I was afraid, but I was also thinking of my father becoming rich. I was twelve. I did not understand traps that looked like help.

"I will not tell," I whispered.

The moon above us went dark.

I woke up breathing fast.

For a moment I thought it had only been a dream. Somto was still sleeping beside me, turned away with one arm under her head. The room was quiet. The only sound was the night insects outside.

Then I saw the calabash beside my mat.

My whole body went cold.

It was the same one from the dream, smooth and dark, with the red thread around its neck.

I looked at Somto. She did not move.

I picked up the calabash with both hands and tiptoed out of the room. Every step sounded too loud. The floor creaked. My heart beat so hard I thought it would wake everyone.

My parents' room was dim. The bamboo bed stood against the wall, and I could hear my father breathing in his sleep.

I crouched beside the bed and pushed the calabash underneath.

"Let Papa become rich," I whispered.

Then I ran back to my mat and lay down beside Somto, pretending I had never moved.

By morning, fear had turned into excitement. I kept looking at my father's face, waiting to see if richness would appear on him like new clothes.

Before going to the farm, my mother said, "Come, Amara. Let us greet Elder Okoro and thank him for feeding you yesterday."

I followed her to his compound.

Elder Okoro came out with the same calm face.

"Good morning," my mother said. "Thank you for helping my child yesterday."

"She is like my own child," he replied.

He looked at me when he said it, and I lowered my eyes.

My mother did not know what he had done. My father did not know. Somto did not know.

Only I knew there was now a calabash under my parents' bed, and I was proud of myself for helping my family.

If only I had known that the thing I carried into that room was not wealth.

It was trouble."""


SHOTS = [
    ("p001-s001", "Elder at the fence", "Amara sees Elder Okoro at the fence after leaving the kitchen.", "two", "50mm medium shot from Amara's side, Elder framed across the fence, tense quiet afternoon", "Amara pauses with hungry uncertainty; Elder leans calmly on the fence."),
    ("p001-s002", "Greeting", '"Amara, how are you?" / "Good afternoon, sir. I am fine."', "two", "50mm dialogue two-shot, fence line separating them", "Elder's smile is gentle but watchful; Amara keeps her shoulders small."),
    ("p001-s003", "Chicken pox noticed", "Elder notices the chicken-pox marks while speaking to Amara.", "two", "tight 85mm over-the-shoulder from behind Amara's pox-marked cheek and shoulder; Elder Okoro's speaking face fills the right half of the frame at the fence", "Elder Okoro speaks with his lower jaw dropped mid-word while Amara holds still in the foreground."),
    ("p001-s004", "Alone question", '"So you are alone?"', "single", "three-quarter left-facing 85mm head-and-shoulders close-up of Elder Okoro at the fence, Amara is off-camera", "Elder Okoro asks the question with his mouth open wide mid-word, lower jaw dropped and uneven teeth visible, eyes aimed left toward Amara."),
    ("p001-s005", "Amara admits hunger", '"Koko ate my food."', "single", "three-quarter close-up of Amara looking slightly downward, kitchen doorway behind her", "Amara is caught mid-sentence with her mouth wide open in a clear ah-shape, embarrassed and hungry."),
    ("p001-s006", "Elder invites her", '"Come. Do not worry. I have food in my kitchen."', "two", "low 50mm shot along side path to Elder's house", "Elder speaks the invitation with his hands relaxed at his sides; Amara stays at the threshold."),
    ("p001-s007", "Enamel bowl", "Elder returns with warm food in an enamel bowl.", "prop", "insert shot of warm food in an enamel bowl on a rough wooden surface, steam rising", "The bowl sits alone, still and inviting."),
    ("p001-s008", "Amara eats", "Amara sits near his doorway and eats.", "single", "50mm candid side shot, bowl in her lap", "She eats quickly, still weak, unaware she is being watched."),
    ("p001-s009", "Elder watches", "Elder watches her with a calm smile.", "single", "85mm side-profile close-up on Elder", "Slow blink, small controlled smile, eyes fixed off-camera at Amara."),
    ("p001-s010", "Somto returns", "Somto rushes back home, trying to hide that she went out.", "single", "35mm candid side-angle action shot from inside the doorway", "Somto slips sideways into the house with her torso twisted away from the camera, trying not to be noticed."),
    ("p001-s011", "Somto does not care", "Amara tells Somto about the dog and Elder's food.", "two", "side-by-side interior two-shot", "Amara explains; Somto looks toward the kitchen instead of comforting her."),
    ("p001-s012", "Evening cooking", "Somto rushes to cook before the parents return.", "single", "kitchen action shot, smoky practical light", "Somto stirs food fast, glancing toward the compound entrance."),
    ("p001-s013", "Parents return", "The parents return from the farm smelling of soil and maize leaves.", "group", "over-the-shoulder from behind Amara toward Mother and Father entering with farm tools", "Mother bends toward Amara; father drops his cutlass by the door; Amara stands small at the doorway edge."),
    ("p001-s014", "Amara lies for Somto", '"She was sleeping. I did not want to wake her."', "group", "over-the-shoulder from behind Father toward Amara in the foreground, Somto blurred in the far corner", "Amara avoids Somto's eyes; Somto's shoulders loosen with relief."),
    ("p001-s015", "Mother will thank Elder", '"Tomorrow I will go and thank him."', "single", "50mm close-up on Mother tying headscarf tighter", "Mother sighs from exhaustion and gratitude."),
    ("p001-s016", "Night sky", "That night, the moon hangs above the village.", "environment", "35mm establishing shot, full or half moon above thatched roofs", "Clouds drift; village is quiet and ominous."),
    ("p001-s017", "Dream circle", "Amara stands in the middle of black-gowned people.", "group", "wide night shot, Amara small in center of circle", "She turns in panic, searching for an exit."),
    ("p001-s018", "Finds Elder", "She sees Elder Okoro among them.", "group", "85mm over-the-shoulder from behind Amara through two soft black-gowned shoulders toward Elder Okoro in the midground", "Her breathing catches; Elder remains still, separated from the group by a thin strip of moonlight."),
    ("p001-s019", "Take me home", '"Sir, please take me home. I want to go home."', "two", "50mm handheld dialogue shot, Amara reaching toward Elder", "Her eyes widen, mouth trembles, hand reaches and stops short."),
    ("p001-s020", "Special people", '"You are among special people now."', "single", "side-profile close-up of Elder speaking at night", "Elder bends slightly, voice calm, eyes fixed on her."),
    ("p001-s021", "Poverty catches her", "The promise of helping her poor family makes Amara stop crying.", "single", "tight close-up on Amara, moonlight, black silhouettes behind", "Tears pause; her brows soften with dangerous hope."),
    ("p001-s022", "Wish request", '"Can you make my father rich?"', "single", "85mm close-up, Amara looking up toward Elder not camera", "She swallows, voice small, fingers gripping dress fabric."),
    ("p001-s023", "Calabash POV", "Elder hands the calabash toward her.", "single", "front-view low-angle POV shot from Amara's eye line; Elder extends calabash toward camera", "His arms stretch forward; calabash fills foreground."),
    ("p001-s024", "Calabash insert", "The calabash is smooth, dark, tied with red thread.", "prop", "45mm macro insert, focus locked on calabash and red thread", "Object still, background fully blurred."),
    ("p001-s025", "Instruction", '"Hide it under your parents bamboo bed."', "single", "side-profile close-up of Elder holding calabash low", "His mouth forms the words slowly; his face is controlled."),
    ("p001-s026", "Warning", '"If you tell anyone, your father will die."', "single", "85mm tight close-up on Elder, moonlight shadow across face", "His smile disappears; jaw tightens, eyes harden."),
    ("p001-s027", "Promise", '"I will not tell."', "single", "close-up on Amara clutching calabash", "Hands shake; lips barely move; shoulders curl inward."),
    ("p001-s028", "Wake up", "Amara wakes beside Somto.", "two", "dim bedroom, Somto asleep on mat, Amara jolting awake", "Amara lifts her head sharply, breath fast."),
    ("p001-s029", "Real calabash", "Amara sees the same calabash after waking.", "single", "under-the-bed POV shot from floor level beneath the bamboo bed, calabash large in the foreground, Amara's shocked face visible beyond it", "Amara looks under the bed in shock at the calabash."),
    ("p001-s030", "Tiptoe", "Amara tiptoes out while Somto sleeps.", "two", "low angle from floor, Amara carrying calabash, Somto asleep behind", "Amara moves carefully, toes placed silently."),
    ("p001-s031", "Parents room", "She enters her parents' dim room.", "single", "over-the-shoulder from behind Amara toward bamboo bed", "She freezes at father's breathing."),
    ("p001-s032", "Under bed", "She pushes the calabash under the bamboo bed.", "prop", "low floor-level shot, hand pushing calabash under bamboo bed", "Her hand trembles; bed legs loom above."),
    ("p001-s033", "Morning excitement", "By morning, fear turns into excitement.", "single", "warm morning close-up, Amara looking at father off-camera", "Her smile is small and secret, eyes bright."),
    ("p001-s034", "Thank you visit", "Mother takes Amara to thank Elder Okoro.", "group", "over-the-shoulder from behind Mother at Elder's compound doorway; Elder faces her in the doorway, Amara half-hidden beside Mother's wrapper", "Mother speaks warmly with one hand lifted; Amara lowers her eyes and grips the cloth at her side."),
    ("p001-s035", "Like my own child", '"She is like my own child."', "group", "over-the-shoulder from behind Mother toward Elder and Amara, Elder in sharp focus, Amara small at frame edge", "Elder's eyes land on Amara as he says it; Amara's mouth tightens without looking up."),
    ("p001-s036", "Final dread", "Only Amara knows the calabash is under the bed.", "single", "side-profile close-up of Amara walking away from Elder's compound", "Her pride flickers into unease; she looks back once."),
]


def prompt_for_shot(shot: tuple[str, str, str, str, str, str]) -> dict[str, str]:
    shot_id, title, beat, mode, camera, action = shot
    characters = SHOT_CHARACTERS[shot_id]
    exact_moment = EXACT_MOMENTS[shot_id]
    lighting = lighting_for_shot(shot_id)
    visible = {
        "single": "one clearly visible human subject",
        "two": "exactly two clearly visible human subjects",
        "group": "the listed named characters plus only the required soft background figures named by the camera note",
        "prop": "the prop is the only sharp subject",
        "environment": "environment-only shot with no people",
    }[mode]
    if characters:
        continuity = "Visible character locks: " + "; ".join(CHARACTER_LOCKS[name] for name in characters) + ". "
        cast_lock = f"Only these named characters may appear clearly in this frame: {', '.join(characters)}. "
    else:
        continuity = "No named character is visible in this frame. "
        cast_lock = "No people or human figures appear clearly in this frame. "
    speaking_lock = ""
    if "mouth is open" in exact_moment or "mouth slightly open" in exact_moment or "lower jaw is dropped" in exact_moment:
        speaking_lock = (
            "Speaking lock: the speaking character's lips are visibly separated, the dark mouth interior is visible, "
            "and the cheeks show mid-sentence tension; closed lips on the speaking character are incorrect. "
        )
    prompt = (
        "STORYBOARD IMAGE PROMPT - single cinematic still frame, not video. "
        "Create a photorealistic vertical 9:16 Nigerian village drama photograph with pore-level skin texture, realistic fabric weave, natural body proportions, and no text anywhere in the image. "
        f"Shot {shot_id}: {title}. "
        f"Frame purpose: {beat} "
        f"Composition: {camera}. This is the exact chosen camera angle and shot type; do not change it to another composition. "
        f"Visible subject rule: {visible}. "
        f"{cast_lock}"
        f"{continuity}"
        f"Exact still moment: {exact_moment} "
        f"{speaking_lock}"
        f"Lighting: {lighting} "
        "Performance rule: one frozen action or pose per visible character, no extra gestures, no second action in the same character. "
        "Environment: rural Nigerian compound or room details only when they belong to this frame, with real contact shadows and grounded props. "
        "Style: 8K hyper-real cinematic photograph, physical cinema lens, shallow depth of field only where the chosen shot implies it, no CGI, no illustration, no cartoon, no poster design."
    )
    mode_negative = {
        "single": ", low cut hair, shaved head, short cropped hair, wrong outfit, repeated girl, duplicate Elder, extra people",
        "two": ", low cut hair, shaved head, short cropped hair, wrong outfit, repeated girl, duplicate Elder, third person, extra people",
        "group": ", low cut hair, shaved head, short cropped hair, wrong outfit, repeated girl, duplicate Elder, duplicated crowd faces, crowd clutter, more than necessary people",
        "prop": ", hands with extra fingers, duplicate prop, person as main subject, extra people",
        "environment": ", people, human figures, faces, text signs",
    }[mode]
    if speaking_lock:
        mode_negative += ", closed mouth on speaking character, sealed lips on speaking character"
    if shot_id == "p001-s004":
        mode_negative += ", crouching, squatting, knees visible, full body, front-facing portrait, looking into camera, hands on ground"
    negative = BASE_NEGATIVE + mode_negative
    return {"id": shot_id, "title": title, "beat": beat, "mode": mode, "camera": camera, "action": action, "prompt": prompt, "negative_prompt": negative}


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    now = datetime.now().isoformat(timespec="seconds")
    part_root = PACKAGE / PART
    prompt_dir = part_root / "director" / "prompts"
    workflow_dir = part_root / "comfyui-workflows"
    image_dir = part_root / "images"
    for path in (part_root / "screenwriter", part_root / "shotlist", prompt_dir, workflow_dir, image_dir):
        path.mkdir(parents=True, exist_ok=True)

    write(part_root / "screenwriter" / "long-form-rewrite.md", "# Stolen Innocence - Long-Form Continuation Part 001\n\n" + LONG_REWRITE + "\n")

    production = [
        "# Stolen Innocence - Production Script Continuation Part 001",
        "",
        f"Generated: {now}",
        "Scope: Continue after Amara sees Elder Okoro, preserving dialogue and interactions through the calabash under the bed and the thank-you visit.",
        "Narrator: Young woman first-person Amara, recalling childhood events.",
        "",
        "## Script",
        "",
        LONG_REWRITE,
        "",
    ]
    write(part_root / "screenwriter" / "production-script.md", "\n".join(production))

    prompts = [prompt_for_shot(shot) for shot in SHOTS]
    write(part_root / "shotlist" / "shotlist.json", json.dumps({"generated_at": now, "scope": PART, "shots": prompts}, indent=2, ensure_ascii=False) + "\n")

    shot_md = ["# Stolen Innocence - Shotlist Continuation Part 001", ""]
    image_prompt_md = ["# Stolen Innocence - Image Prompts Continuation Part 001", ""]
    workflow_template = json.loads(WORKFLOW_TEMPLATE.read_text(encoding="utf-8"))
    for i, item in enumerate(prompts, start=1):
        shot_md.extend([
            f"## {item['id']} - {item['title']}",
            f"Beat: {item['beat']}",
            f"Camera: {item['camera']}",
            f"Performance: {item['action']}",
            "",
        ])
        image_prompt_md.extend([f"## {item['id']} - {item['title']}", item["prompt"], "", f"Negative: {item['negative_prompt']}", ""])
        write(prompt_dir / f"{item['id']}.txt", item["prompt"] + "\n\nNegative prompt: " + item["negative_prompt"] + "\n")
        workflow = json.loads(json.dumps(workflow_template))
        if "2" in workflow and "inputs" in workflow["2"] and "device" in workflow["2"]["inputs"]:
            workflow["2"]["inputs"]["device"] = "default"
        workflow["3"]["inputs"]["text"] = item["prompt"]
        workflow["5"]["inputs"]["width"] = 576
        workflow["5"]["inputs"]["height"] = 864
        workflow["6"]["inputs"]["seed"] = 82000000 + i * 149
        workflow["6"]["inputs"]["steps"] = 28
        workflow["9"]["inputs"]["filename_prefix"] = f"{OUTPUT_PREFIX}_{item['id']}"
        write(workflow_dir / f"{item['id']}-workflow.json", json.dumps(workflow, indent=2, ensure_ascii=False) + "\n")
    write(part_root / "shotlist" / "shotlist.md", "\n".join(shot_md).rstrip() + "\n")
    write(part_root / "image-prompts.md", "\n".join(image_prompt_md).rstrip() + "\n")

    manifest = {
        "generated_at": now,
        "part": PART,
        "source_sections": ["section-001", "section-002"],
        "name_changes": str(PACKAGE / "edited script" / "name_map.json"),
        "shot_count": len(prompts),
        "outputs": {
            "long_form_rewrite": str(part_root / "screenwriter" / "long-form-rewrite.md"),
            "production_script": str(part_root / "screenwriter" / "production-script.md"),
            "shotlist_json": str(part_root / "shotlist" / "shotlist.json"),
            "image_prompts": str(part_root / "image-prompts.md"),
            "workflows": str(workflow_dir),
            "images": str(image_dir),
        },
    }
    write(part_root / "part-manifest.json", json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"part": PART, "shot_count": len(prompts), "root": str(part_root)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
