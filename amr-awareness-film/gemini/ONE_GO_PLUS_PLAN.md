# One-go method for the Gemini Plus plan

**Why not one video prompt?** No Gemini plan can make a 3-minute film from one prompt. The video model (Veo) makes about 8 seconds per generation, and the Plus plan only allows a small number of videos, so the 30-clip plan in `GEMINI_PROMPTS.md` would take weeks of daily limits.

**What works on Plus:** Gemini makes the **3D pictures** in one chat; image generation is far less limited than video. Claude then turns them into the **full 3-minute 1080p video**:

- slow camera moves and transitions on every picture;
- the Chennai Tamil voice track;
- English subtitles;
- music and sound effects.

The result looks like a 3D animated "motion comic". The pictures move, but the characters' lips don't. If you have any video generations left, add up to 3 moving "hero shots" (step 3).

## Step 1: one Gemini chat, one master prompt

1. Open **gemini.google.com** (or the app) and start a **new chat**.
2. Tap **+** and upload `reference_frames/characters.png` and `reference_frames/microbes.png` from the kit.
3. Copy the whole grey block below, paste it, and send.
4. Gemini first makes the character sheet, then picture 1. Type **next** each time to get the next picture, until picture 30.
5. Download every picture and name them `01.png` … `30.png` in order. If one looks wrong (a different face, or text in it), type **redo** plus what to fix, for example `redo 12, keep the Boss's golden tail`.

```
You are the art director of a 3-minute 3D animated educational film for Antimicrobial Resistance Awareness Week, set in Chennai, India. Create high-end stylised 3D animated feature-film images: rounded appealing characters, soft global illumination, subsurface skin shading, detailed fabric and hair, expressive faces, cinematic lighting and depth of field. Every image must be 16:9 landscape and contain NO text, letters, captions or logos.

The two uploaded images are the 2D designs. Keep every character exactly the same in every image (face, skin tone, hair, glasses, clothes, colours):
- STUDENT 1: 16-year-old Tamil schoolboy, slim, medium-brown skin, short neat black hair parted on the left, all-white school uniform with a maroon crest on the pocket, maroon-and-gold striped tie, navy backpack, green bicycle.
- STUDENT 2: 16-year-old Tamil schoolboy, slightly chubby, darker brown skin, thick curly black hair, big cheeky grin, same uniform with a loose tie, red backpack, red bicycle.
- PHARMACIST: man about 40, moustache, rectangular glasses, white coat over a light-blue shirt.
- MOTHER: Tamil woman about 45, low bun, red pottu, maroon cotton saree with a gold border.
- CONSULTANT PHYSICIAN: about 52, salt-and-pepper hair, rimless glasses, white coat, light-blue shirt, navy tie, stethoscope, ID badge.
- CONSULTANT MICROBIOLOGIST: about 40, trimmed beard, square black glasses, white lab coat over a grey shirt, blue lanyard ID badge.
- BACTERIA (recognisably bacteria, with cartoon faces): small friendly blue and green SENSITIVE bacteria; friendly teal GOOD bacteria; larger crimson and purple RESISTANT bacteria with glowing capsules and mischievous villain faces; THE BOSS, the largest crimson-purple resistant bacterium with a golden whip-like tail and a jagged-tooth grin. AMOXICILLIN = small glowing yellow molecules.

First, make one 3D character lineup of all the people and bacteria. Then make picture 1. After each picture, wait until I type "next", then make the next one. Make ONE picture per reply and say its number.

1. Wide shot of a sunny Chennai school campus in the morning (cream buildings, red-tile roofs, a big shady tree); STUDENT 1 near the building touching his sore throat, feverish; STUDENT 2 walking towards him smiling.
2. Medium two-shot: STUDENT 2 looks concerned; STUDENT 1 waves it off and pulls out a smartphone with a sly smile.
3. Close-up of STUDENT 1's hands holding a smartphone; the chat screen glows with blank message bubbles.
4. Two-shot: STUDENT 2 thumps his chest proudly giving advice; STUDENT 1 grins with a fist raised.
5. Side view: both boys cycling side by side on a sunny Chennai street with coconut palms, colourful houses and a temple gopuram; STUDENT 2 singing, one hand in the air.
6. Both boys laughing on their bicycles as they arrive at a small pharmacy with a green cross sign; an auto-rickshaw passes.
7. Pharmacy interior with shelves of colourful medicine boxes: STUDENT 1 at the glass counter asking, hand on throat; the PHARMACIST behind the counter; STUDENT 2 beside him.
8. Close-up: the PHARMACIST's hand sliding a strip of capsules across the counter into the boy's hand, no prescription; slightly dim, ominous light.
9. STUDENT 2 waving the medicine strip triumphantly as both walk out of the pharmacy into sunlight.
10. Simple home kitchen: STUDENT 1 swallowing a capsule with a glass of water.
11. Microscopic world inside a blood vessel: red blood cells; blue and green sensitive bacteria bursting like bubbles as glowing yellow amoxicillin molecules hit them; a few red-purple resistant bacteria unharmed.
12. Low-angle hero shot: THE BOSS laughing, his gang of resistant bacteria behind him.
13. THE BOSS mocking humans, counting on his little arm; the gang laughing.
14. A small red resistant bacterium stepping forward with its arm raised like a know-it-all student.
15. Teal good bacteria wilting and turning grey as antibiotic molecules hit them; THE BOSS pointing at them mockingly.
16. Resistant bacteria splitting in two (binary fission), multiplying until they fill the frame.
17. A crowd of resistant bacteria high-fiving and dancing, THE BOSS dancing in the centre.
18. Extreme close-up: THE BOSS turning to the camera with a menacing look, dark purple light from below.
19. A wall calendar with pages flying off to show days passing (no readable numbers).
20. STUDENT 1 sick in bed at home, pale and sweating.
21. Modern hospital ward: STUDENT 1 weak in bed in a light-blue gown; the MOTHER pleading with the CONSULTANT PHYSICIAN.
22. The CONSULTANT PHYSICIAN examining STUDENT 1 with his stethoscope.
23. Modern microbiology lab: blood-culture bottles and an agar plate with small antibiotic discs (susceptibility test).
24. The CONSULTANT MICROBIOLOGIST at a computer studying a lab report showing an agar plate and a table with red and green marks.
25. The MICROBIOLOGIST showing the printed report to the CONSULTANT PHYSICIAN in his office; both lean over it.
26. Hospital bedside: the CONSULTANT PHYSICIAN explaining gently to the MOTHER; STUDENT 1 resting in bed.
27. A cute spiky purple virus in a dark violet space; yellow antibiotic molecules bouncing off it harmlessly.
28. Hospital bedside: the CONSULTANT MICROBIOLOGIST explaining to the MOTHER, the PHYSICIAN beside him.
29. Bright hospital corridor: both doctors side by side looking into the camera, confident and warm; through a ward doorway in soft focus, STUDENT 1 sits up in bed on an IV drip, recovering, with the MOTHER beside him.
30. The same two doctors, low angle, warmer and brighter light, with empty space in the top half of the image.
```

## Step 2: send the pictures back to Claude

Upload the 30 pictures here in this chat. Alternatively, on github.com, open this branch, go to `amr-awareness-film/gemini/`, choose **Add file → Upload files**, and put them in a folder named `3d_frames`. Claude then builds:

- **Video:** 3:00, 1920×1080, with each picture shown at its moment in the story with slow pans, zooms and transitions.
- **Voices:** the dialogue in **Chennai Tamil**, from the prompt kit.
- **Text:** English subtitles, the "No prescription asked!" tag, the slogan titles and the end card.
- **Sound:** music and sound effects.

**Voices:** there are two options.

- **Synthetic voices.** Claude generates the track with Indian Tamil neural voices. These are still synthetic; there are only two Indian Tamil voices (one male, one female), so the male characters are told apart by pitch.
- **Real people (most natural).** Have Chennai Tamil speakers read the lines from `GEMINI_PROMPTS.md` into a phone, one audio file per line, named by clip number (`clip01.m4a` …), and send them with the pictures. Claude fits them into the film.

## Step 3 (optional): up to 3 moving hero shots

If your plan still has video generations, spend them on the moments that benefit most from motion. In Gemini, choose **Video**, upload the matching 3D picture as the starting image, and paste the prompt from `GEMINI_PROMPTS.md`:

| Use picture | Prompt in GEMINI_PROMPTS.md | Moment |
|---|---|---|
| 11 | Clip 10 | Antibiotic arrives, sensitive bacteria burst |
| 17 | Clip 15 | Villain dance |
| 5 | Clip 05 | Cycling song |

Send these clips back too. Claude swaps them in for the still pictures; their audio is replaced by the film's voice track.
