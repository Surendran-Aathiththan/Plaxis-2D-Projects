# Gemini (Veo) prompts: 3D version with Chennai Tamil voices

These prompts remake *Use Antibiotics Wisely* as a **3D animated** film in **Gemini (Veo)**, using the rendered 2D film ([`../AMR_Awareness_Film_1080p.mp4`](../AMR_Awareness_Film_1080p.mp4)) as the storyboard. The dialogue is rewritten in **natural colloquial Chennai Tamil**, with the same meaning and the same science as the original screenplay.

## Workflow

Veo makes clips of about **8 seconds**, so the film is split into **30 clips**. Each prompt below is self-contained: copy the whole grey block. Veo has no memory between clips, which is why the character and voice descriptions are repeated every time.

1. **Make the 3D character sheets once** (Gemini image generation). Upload `reference_frames/characters.png` and `reference_frames/microbes.png` and use the *Step 1* prompts. Save the results; they are your consistency references.
2. **For each clip, make a 3D start frame.** Upload `reference_frames/clipNN.png` together with the 3D character sheet and use the *Step 2* prompt. You get a 3D image with the same composition as the 2D film.
3. **Generate the clip** in Gemini video (Veo). Upload that 3D start frame as the starting image (or, in Google Flow, add the character sheets as reference *ingredients*) and paste the clip prompt. Generate 2–4 takes and keep the one with the best Tamil speech and lip-sync.
4. **Edit** (CapCut, Premiere, DaVinci Resolve or similar): put the clips in order and trim each to the *Keep* time. That adds up to about **2:55**, plus the 5-second end card = **3:00**. Then add the English subtitles listed under each clip, the phone-screen text (clip 3), the slogan titles (clip 30) and the end card. Details are under [Editing](#editing) at the end.

**Tips for natural Chennai Tamil voices**

- Keep the Tamil in Tamil script, exactly as written. If Veo mispronounces a line, regenerate; small wording changes (for example adding `டா` or `மச்சி`) often make delivery more natural.
- Veo picks a new voice each generation. Generate several takes and choose the ones closest to each character's voice description. For a perfectly consistent cast, have real Chennai Tamil speakers (friends, a college drama club) record the lines below on a phone, then replace the clip audio in the editor.
- If a line gets cut off at 8 seconds, use Veo's **Extend** option on that clip, or split the line across two generations.
- Every prompt asks for *no on-screen text*, because Veo garbles text. Add all text in the editor.

## Step 1: 3D character sheets (Gemini image generation)

Upload `reference_frames/characters.png`, then:

```
Recreate these six characters as a high-end stylised 3D animated feature-film character lineup, full body, standing on a plain light-grey studio background, soft studio lighting. Keep every design detail exactly: faces, skin tones, hairstyles, glasses, beard, moustache, pottu, clothes and colours. Left to right: Student 1 (16, slim, neat side-parted hair, white school uniform, maroon-and-gold tie, navy backpack), Student 2 (16, chubby, curly hair, big grin, same uniform, loose tie, red backpack), Pharmacist (40, moustache, rectangular glasses, white coat over light-blue shirt), Mother (45, low bun, red pottu, maroon saree with gold border), Consultant Physician (52, salt-and-pepper hair, rimless glasses, white coat, navy tie, stethoscope, ID badge), Consultant Microbiologist (40, trimmed beard, square black glasses, white lab coat, grey shirt, blue lanyard badge). Appealing, expressive, realistic proportions slightly stylised. No text.
```

Upload `reference_frames/microbes.png`, then:

```
Recreate these microbes as glossy, high-end 3D animated characters on a dark crimson background, scientifically recognisable as bacteria (rod or round shapes, visible cell wall, pili, flagella) with simple cartoon faces: small friendly blue and green sensitive bacteria; friendly teal good bacteria with a gentle smile; larger crimson and purple resistant bacteria with a glowing capsule, spiky pili and mischievous villain faces; the Boss, the largest crimson-purple resistant bacterium with a golden whip-like flagellum and a jagged-tooth grin; glowing yellow amoxicillin molecules; a cute spiky purple virus. No text.
```

## Step 2: 3D start frame for each clip

Upload `reference_frames/clipNN.png` and the 3D character sheet from Step 1, then:

```
Recreate the first image as a single frame from a high-end stylised 3D animated feature film. Keep the same composition, camera angle, characters, poses and setting, but render everything in rich 3D with soft global illumination, detailed textures, realistic lighting and depth of field. The characters must match the 3D character sheet exactly. Remove all text, labels and captions. 16:9.
```

## The 30 clip prompts

### Clip 01: School morning: the sore throat

Start frame: `reference_frames/clip01.png` · **Keep:** 6 s (cumulative 6 s)

```
High-end stylised 3D animated feature-film look: rounded appealing character designs, soft global illumination, subsurface skin shading, detailed fabric and hair, expressive eyes and natural lip-sync, smooth cinematic camera, shallow depth of field, rich warm colour grade, 16:9 widescreen.

Setting: A bright school campus in Chennai in the morning: cream two-storey buildings with red-tile roofs, a big shady tree, sandy ground, students in white uniforms in the background.
Characters (keep exactly this design):
- STUDENT 1: 16-year-old Tamil schoolboy, slim, medium-brown skin, short neat black hair parted on the left, all-white school uniform (short-sleeved shirt with maroon crest on pocket, white trousers), maroon-and-gold striped tie, navy backpack, green bicycle.
- STUDENT 2: 16-year-old Tamil schoolboy, slightly chubby, darker brown skin, thick curly black hair, big cheeky grin, same white uniform with loose maroon-and-gold tie, red backpack, red bicycle with a bell.
Action: STUDENT 1 stands near the building, touching his throat, looking feverish. STUDENT 2 walks in happily, humming, and stops beside him.
Camera: Slow crane down from a wide establishing shot to a medium two-shot.
Dialogue (spoken in Tamil, lip-synced):
- STUDENT 1 (hoarse, tired; voice: young male teen voice, slightly hoarse and tired, casual Chennai Tamil): "டேய் மச்சி, தொண்டை ரொம்ப வலிக்குதுடா… காய்ச்சல் மாதிரியும் இருக்கு."
All speech must sound like real human voice actors from Chennai: natural colloquial Chennai Tamil, relaxed conversational pace, real breaths and emotion, natural intonation. Not robotic, not text-to-speech, not formal written Tamil. English words (Amoxicillin, antibiotic, report) are said the way Chennai people naturally say them.
Audio: school ambience, birds chirping, distant children playing; no background music.
No subtitles, no captions, no on-screen text or logos.
```

English subtitles:

- Machi, my throat really hurts, da… feels like a fever too.

### Clip 02: Doctor? No, ask AI

Start frame: `reference_frames/clip02.png` · **Keep:** 6 s (cumulative 12 s)

```
High-end stylised 3D animated feature-film look: rounded appealing character designs, soft global illumination, subsurface skin shading, detailed fabric and hair, expressive eyes and natural lip-sync, smooth cinematic camera, shallow depth of field, rich warm colour grade, 16:9 widescreen.

Setting: Same school campus, morning.
Characters (keep exactly this design):
- STUDENT 1: 16-year-old Tamil schoolboy, slim, medium-brown skin, short neat black hair parted on the left, all-white school uniform (short-sleeved shirt with maroon crest on pocket, white trousers), maroon-and-gold striped tie, navy backpack, green bicycle.
- STUDENT 2: 16-year-old Tamil schoolboy, slightly chubby, darker brown skin, thick curly black hair, big cheeky grin, same white uniform with loose maroon-and-gold tie, red backpack, red bicycle with a bell.
Action: STUDENT 2 looks concerned and asks. STUDENT 1 waves it off and pulls out his smartphone with a sly smile.
Camera: Medium two-shot, gentle push-in.
Dialogue (spoken in Tamil, lip-synced):
- STUDENT 2 (concerned; voice: energetic, cheeky young male teen voice, fast and funny, street-style Chennai Tamil): "என்னடா ஆச்சு? டாக்டர்கிட்ட போலாமா?"
- STUDENT 1 (dismissive, casual; voice: young male teen voice, slightly hoarse and tired, casual Chennai Tamil): "அதெல்லாம் வேணாம் டா. ChatGPT-ல கேட்டுப் பாக்கலாம்."
All speech must sound like real human voice actors from Chennai: natural colloquial Chennai Tamil, relaxed conversational pace, real breaths and emotion, natural intonation. Not robotic, not text-to-speech, not formal written Tamil. English words (Amoxicillin, antibiotic, report) are said the way Chennai people naturally say them.
Audio: school ambience.
No subtitles, no captions, no on-screen text or logos.
```

English subtitles:

- What happened, da? Shall we go to the doctor?
- No need for all that, da. Let's ask ChatGPT.

### Clip 03: Phone close-up

Start frame: `reference_frames/clip03.png` · **Keep:** 4 s (cumulative 16 s)

```
High-end stylised 3D animated feature-film look: rounded appealing character designs, soft global illumination, subsurface skin shading, detailed fabric and hair, expressive eyes and natural lip-sync, smooth cinematic camera, shallow depth of field, rich warm colour grade, 16:9 widescreen.

Setting: Close-up of STUDENT 1's hands holding a smartphone; generic chat app with no logo; the screen glows brightly and is kept softly out of focus (text will be added in editing).
Characters (keep exactly this design):
- STUDENT 1: 16-year-old Tamil schoolboy, slim, medium-brown skin, short neat black hair parted on the left, all-white school uniform (short-sleeved shirt with maroon crest on pocket, white trousers), maroon-and-gold striped tie, navy backpack, green bicycle.
Action: His thumbs type a message; a reply bubble pops up; he glances at it and shrugs.
Camera: Over-the-shoulder close-up, slow push-in.
No dialogue.
Audio: phone keyboard taps, a soft notification ping, faint school ambience.
No subtitles, no captions, no on-screen text or logos.
```

### Clip 04: The wrong advice

Start frame: `reference_frames/clip04.png` · **Keep:** 7 s (cumulative 23 s)

```
High-end stylised 3D animated feature-film look: rounded appealing character designs, soft global illumination, subsurface skin shading, detailed fabric and hair, expressive eyes and natural lip-sync, smooth cinematic camera, shallow depth of field, rich warm colour grade, 16:9 widescreen.

Setting: Same school campus, morning.
Characters (keep exactly this design):
- STUDENT 1: 16-year-old Tamil schoolboy, slim, medium-brown skin, short neat black hair parted on the left, all-white school uniform (short-sleeved shirt with maroon crest on pocket, white trousers), maroon-and-gold striped tie, navy backpack, green bicycle.
- STUDENT 2: 16-year-old Tamil schoolboy, slightly chubby, darker brown skin, thick curly black hair, big cheeky grin, same white uniform with loose maroon-and-gold tie, red backpack, red bicycle with a bell.
Action: STUDENT 2 pushes the phone down playfully, thumps his chest proudly and gives confident advice. STUDENT 1 grins and agrees, raising a fist.
Camera: Medium two-shot favouring STUDENT 2, then a quick push-in.
Dialogue (spoken in Tamil, lip-synced):
- STUDENT 2 (proud, confident; voice: energetic, cheeky young male teen voice, fast and funny, street-style Chennai Tamil): "டேய், எனக்கும் முன்னாடி இப்படித்தான் இருந்துச்சு. நான் Amoxicillin எடுத்தேன். நீயும் எடுத்துக்கோ டா!"
- STUDENT 1 (cheerful; voice: young male teen voice, slightly hoarse and tired, casual Chennai Tamil): "சரி டா! வா, pharmacy போலாம்!"
All speech must sound like real human voice actors from Chennai: natural colloquial Chennai Tamil, relaxed conversational pace, real breaths and emotion, natural intonation. Not robotic, not text-to-speech, not formal written Tamil. English words (Amoxicillin, antibiotic, report) are said the way Chennai people naturally say them.
Audio: school ambience.
No subtitles, no captions, no on-screen text or logos.
```

English subtitles:

- Da, I had the same thing before. I took Amoxicillin. You take it too, da!
- OK da! Come, let's go to the pharmacy!

### Clip 05: Cycling song, part 1

Start frame: `reference_frames/clip05.png` · **Keep:** 7 s (cumulative 30 s)

```
High-end stylised 3D animated feature-film look: rounded appealing character designs, soft global illumination, subsurface skin shading, detailed fabric and hair, expressive eyes and natural lip-sync, smooth cinematic camera, shallow depth of field, rich warm colour grade, 16:9 widescreen.

Setting: A sunny Chennai neighbourhood street: coconut palms, colourful houses, a temple gopuram in the distance.
Characters (keep exactly this design):
- STUDENT 1: 16-year-old Tamil schoolboy, slim, medium-brown skin, short neat black hair parted on the left, all-white school uniform (short-sleeved shirt with maroon crest on pocket, white trousers), maroon-and-gold striped tie, navy backpack, green bicycle.
- STUDENT 2: 16-year-old Tamil schoolboy, slightly chubby, darker brown skin, thick curly black hair, big cheeky grin, same white uniform with loose maroon-and-gold tie, red backpack, red bicycle with a bell.
Action: Both boys ride their bicycles side by side. STUDENT 2 sings a funny gaana-style song with big gestures, one hand off the handlebar; STUDENT 1 smiles weakly.
Camera: Side-tracking shot at handlebar height, moving with the bikes.
Dialogue (spoken in Tamil, lip-synced):
- STUDENT 2 (sung, off-key, Chennai gaana style, a cappella; voice: energetic, cheeky young male teen voice, fast and funny, street-style Chennai Tamil): "ஊசி போட உடம்பு இருந்தா… டாக்டர்கிட்ட போகணுமா?"
All speech must sound like real human voice actors from Chennai: natural colloquial Chennai Tamil, relaxed conversational pace, real breaths and emotion, natural intonation. Not robotic, not text-to-speech, not formal written Tamil. English words (Amoxicillin, antibiotic, report) are said the way Chennai people naturally say them.
Audio: bicycle chains, two rings of a bicycle bell, birds, light traffic; no background music.
No subtitles, no captions, no on-screen text or logos.
```

English subtitles:

- ♪ If you've got a body for injections… do we really have to see a doctor? ♪

### Clip 06: Cycling song, part 2

Start frame: `reference_frames/clip06.png` · **Keep:** 7 s (cumulative 37 s)

```
High-end stylised 3D animated feature-film look: rounded appealing character designs, soft global illumination, subsurface skin shading, detailed fabric and hair, expressive eyes and natural lip-sync, smooth cinematic camera, shallow depth of field, rich warm colour grade, 16:9 widescreen.

Setting: Same Chennai street; a small pharmacy with a green cross sign comes into view.
Characters (keep exactly this design):
- STUDENT 1: 16-year-old Tamil schoolboy, slim, medium-brown skin, short neat black hair parted on the left, all-white school uniform (short-sleeved shirt with maroon crest on pocket, white trousers), maroon-and-gold striped tie, navy backpack, green bicycle.
- STUDENT 2: 16-year-old Tamil schoolboy, slightly chubby, darker brown skin, thick curly black hair, big cheeky grin, same white uniform with loose maroon-and-gold tie, red backpack, red bicycle with a bell.
Action: STUDENT 2 finishes the song, rings his bell, and both boys burst out laughing as they reach the pharmacy. An auto-rickshaw passes in the background.
Camera: Front tracking shot, then wide as they arrive.
Dialogue (spoken in Tamil, lip-synced):
- STUDENT 2 (sung, Chennai gaana style; voice: energetic, cheeky young male teen voice, fast and funny, street-style Chennai Tamil): "Pharmacy-க்கு சைக்கிள் மிதிச்சு… மாத்திரை வாங்கிப் போடலாமா?"
All speech must sound like real human voice actors from Chennai: natural colloquial Chennai Tamil, relaxed conversational pace, real breaths and emotion, natural intonation. Not robotic, not text-to-speech, not formal written Tamil. English words (Amoxicillin, antibiotic, report) are said the way Chennai people naturally say them.
Audio: bicycle bell, laughter, auto-rickshaw passing; no background music.
No subtitles, no captions, no on-screen text or logos.
```

English subtitles:

- ♪ Let's pedal to the pharmacy… shall we just buy pills and pop them? ♪

### Clip 07: At the pharmacy counter

Start frame: `reference_frames/clip07.png` · **Keep:** 7 s (cumulative 44 s)

```
High-end stylised 3D animated feature-film look: rounded appealing character designs, soft global illumination, subsurface skin shading, detailed fabric and hair, expressive eyes and natural lip-sync, smooth cinematic camera, shallow depth of field, rich warm colour grade, 16:9 widescreen.

Setting: A small, cluttered community pharmacy: shelves packed with colourful medicine boxes, a glass counter, a ceiling fan.
Characters (keep exactly this design):
- STUDENT 1: 16-year-old Tamil schoolboy, slim, medium-brown skin, short neat black hair parted on the left, all-white school uniform (short-sleeved shirt with maroon crest on pocket, white trousers), maroon-and-gold striped tie, navy backpack, green bicycle.
- STUDENT 2: 16-year-old Tamil schoolboy, slightly chubby, darker brown skin, thick curly black hair, big cheeky grin, same white uniform with loose maroon-and-gold tie, red backpack, red bicycle with a bell.
- PHARMACIST: man about 40, neat moustache, rectangular glasses, white pharmacist coat over a light-blue shirt.
Action: STUDENT 1 asks at the counter, hand on his throat. The PHARMACIST, without asking for a prescription, slides a strip of amoxicillin capsules across the counter. The lighting dims slightly at the hand-over (this is bad practice).
Camera: Medium wide from behind the counter, then a close-up of the hand-over.
Dialogue (spoken in Tamil, lip-synced):
- STUDENT 1 (hoarse, polite; voice: young male teen voice, slightly hoarse and tired, casual Chennai Tamil): "அண்ணா, Amoxicillin இருக்கா? தொண்டை வலியும் காய்ச்சலும் இருக்கு."
All speech must sound like real human voice actors from Chennai: natural colloquial Chennai Tamil, relaxed conversational pace, real breaths and emotion, natural intonation. Not robotic, not text-to-speech, not formal written Tamil. English words (Amoxicillin, antibiotic, report) are said the way Chennai people naturally say them.
Audio: door chime, ceiling fan hum, rustle of a medicine strip, a low ominous note at the hand-over.
No subtitles, no captions, no on-screen text or logos.
```

English subtitles:

- Anna, do you have Amoxicillin? I have a sore throat and fever.

### Clip 08: 'So easy!'

Start frame: `reference_frames/clip08.png` · **Keep:** 5 s (cumulative 49 s)

```
High-end stylised 3D animated feature-film look: rounded appealing character designs, soft global illumination, subsurface skin shading, detailed fabric and hair, expressive eyes and natural lip-sync, smooth cinematic camera, shallow depth of field, rich warm colour grade, 16:9 widescreen.

Setting: Same pharmacy, at the door.
Characters (keep exactly this design):
- STUDENT 1: 16-year-old Tamil schoolboy, slim, medium-brown skin, short neat black hair parted on the left, all-white school uniform (short-sleeved shirt with maroon crest on pocket, white trousers), maroon-and-gold striped tie, navy backpack, green bicycle.
- STUDENT 2: 16-year-old Tamil schoolboy, slightly chubby, darker brown skin, thick curly black hair, big cheeky grin, same white uniform with loose maroon-and-gold tie, red backpack, red bicycle with a bell.
Action: STUDENT 2 waves the medicine strip triumphantly; both walk out into the sunlight.
Camera: Medium two-shot tracking them to the door.
Dialogue (spoken in Tamil, lip-synced):
- STUDENT 2 (triumphant; voice: energetic, cheeky young male teen voice, fast and funny, street-style Chennai Tamil): "பாத்தியா டா! எவ்ளோ easy-ஆ மாத்திரை வாங்கிட்டோம்!"
- STUDENT 1 (relieved; voice: young male teen voice, slightly hoarse and tired, casual Chennai Tamil): "ஆமாடா! வா, வீட்டுக்குப் போலாம்!"
All speech must sound like real human voice actors from Chennai: natural colloquial Chennai Tamil, relaxed conversational pace, real breaths and emotion, natural intonation. Not robotic, not text-to-speech, not formal written Tamil. English words (Amoxicillin, antibiotic, report) are said the way Chennai people naturally say them.
Audio: street ambience as the door opens.
No subtitles, no captions, no on-screen text or logos.
```

English subtitles:

- See, da! We got the tablets so easily!
- Yeah da! Come, let's go home!

### Clip 09: Swallow and dive

Start frame: `reference_frames/clip09.png` · **Keep:** 4 s (cumulative 53 s)

```
High-end stylised 3D animated feature-film look: rounded appealing character designs, soft global illumination, subsurface skin shading, detailed fabric and hair, expressive eyes and natural lip-sync, smooth cinematic camera, shallow depth of field, rich warm colour grade, 16:9 widescreen.

Setting: A simple home kitchen in Chennai.
Characters (keep exactly this design):
- STUDENT 1: 16-year-old Tamil schoolboy, slim, medium-brown skin, short neat black hair parted on the left, all-white school uniform (short-sleeved shirt with maroon crest on pocket, white trousers), maroon-and-gold striped tie, navy backpack, green bicycle.
Action: STUDENT 1 pops a capsule from the strip and swallows it with a glass of water. The camera rushes into his mouth and down the throat, through a glowing red tunnel, into a blood vessel.
Camera: Medium shot, then a fast dramatic push-in transition into the body.
No dialogue.
Audio: capsule popping from the blister, a gulp, a deep whoosh and a muffled heartbeat.
No subtitles, no captions, no on-screen text or logos.
```

### Clip 10: Inside the body: the antibiotic arrives

Start frame: `reference_frames/clip10.png` · **Keep:** 7 s (cumulative 60 s)

```
High-end stylised 3D animated feature-film look: rounded appealing character designs, soft global illumination, subsurface skin shading, detailed fabric and hair, expressive eyes and natural lip-sync, smooth cinematic camera, shallow depth of field, rich warm colour grade, 16:9 widescreen.

Setting: Microscopic world inside a blood vessel: crimson plasma, red blood cells tumbling past. Small friendly blue and green SENSITIVE bacteria and teal GOOD bacteria float along; a few red-purple RESISTANT bacteria hide among them.
Characters (keep exactly this design):
- THE BOSS (resistant bacterium): large glossy crimson-purple rod-shaped bacterium with a thick glowing capsule, spiky pili, golden whip-like flagellum, cartoon villain face with heavy eyebrows and a jagged-tooth grin.
Action: Glowing yellow amoxicillin molecules stream in; wherever they touch blue and green bacteria, the bacteria burst like soap bubbles. The resistant ones survive. THE BOSS slides into view, laughing, and speaks to the camera.
Camera: Flowing dolly along the vessel, ending on a low-angle hero shot of THE BOSS.
Dialogue (spoken in Tamil, lip-synced):
- THE BOSS (resistant bacterium) (laughing, mocking; voice: funny, sly comic-villain voice, theatrical laugh, Chennai Tamil slang): "அடேய்… முட்டாள் மனுஷங்களா! கொஞ்சம் கூட யோசிக்க மாட்டீங்களாடா?"
All speech must sound like real human voice actors from Chennai: natural colloquial Chennai Tamil, relaxed conversational pace, real breaths and emotion, natural intonation. Not robotic, not text-to-speech, not formal written Tamil. English words (Amoxicillin, antibiotic, report) are said the way Chennai people naturally say them.
Audio: liquid whooshing, bubbly pops as bacteria burst, playful villain swing music (pizzicato, tuba, finger snaps).
No subtitles, no captions, no on-screen text or logos.
```

English subtitles:

- Hey… you foolish humans! Can't you think even a little?

### Clip 11: The Boss mocks

Start frame: `reference_frames/clip11.png` · **Keep:** 6 s (cumulative 66 s)

```
High-end stylised 3D animated feature-film look: rounded appealing character designs, soft global illumination, subsurface skin shading, detailed fabric and hair, expressive eyes and natural lip-sync, smooth cinematic camera, shallow depth of field, rich warm colour grade, 16:9 widescreen.

Setting: Same microscopic blood vessel; resistant bacteria gang behind the Boss; tiny enzyme 'scissors' snip antibiotic molecules near them.
Characters (keep exactly this design):
- THE BOSS (resistant bacterium): large glossy crimson-purple rod-shaped bacterium with a thick glowing capsule, spiky pili, golden whip-like flagellum, cartoon villain face with heavy eyebrows and a jagged-tooth grin.
Action: THE BOSS counts on his little arm, mocking humans; the gang laughs behind him.
Camera: Medium shot on THE BOSS, slight handheld wobble for comedy.
Dialogue (spoken in Tamil, lip-synced):
- THE BOSS (resistant bacterium) (sing-song, sarcastic; voice: funny, sly comic-villain voice, theatrical laugh, Chennai Tamil slang): "தொண்டை வலிச்சா antibiotic! காய்ச்சல் வந்தா antibiotic! எதுக்குன்னே தெரியாம மாத்திரைய போட்டுக்கிறீங்க!"
All speech must sound like real human voice actors from Chennai: natural colloquial Chennai Tamil, relaxed conversational pace, real breaths and emotion, natural intonation. Not robotic, not text-to-speech, not formal written Tamil. English words (Amoxicillin, antibiotic, report) are said the way Chennai people naturally say them.
Audio: villain swing music, gang laughter.
No subtitles, no captions, no on-screen text or logos.
```

English subtitles:

- Sore throat? Antibiotic! Fever? Antibiotic! You pop pills without even knowing why!

### Clip 12: Know-it-all bacterium

Start frame: `reference_frames/clip12.png` · **Keep:** 4 s (cumulative 70 s)

```
High-end stylised 3D animated feature-film look: rounded appealing character designs, soft global illumination, subsurface skin shading, detailed fabric and hair, expressive eyes and natural lip-sync, smooth cinematic camera, shallow depth of field, rich warm colour grade, 16:9 widescreen.

Setting: Same microscopic blood vessel.
Characters (keep exactly this design):
- SMART BACTERIUM: smaller red resistant rod-shaped bacterium with spiky pili and a know-it-all face.
Action: The SMART BACTERIUM steps forward and raises its little arm like a know-it-all student.
Camera: Push-in to medium close-up.
Dialogue (spoken in Tamil, lip-synced):
- SMART BACTERIUM (smug; voice: squeaky, smug little voice, Chennai Tamil): "Antibiotics வைரஸுக்கு வேலை செய்யாதுன்னு உங்களுக்குத் தெரியாதா?"
All speech must sound like real human voice actors from Chennai: natural colloquial Chennai Tamil, relaxed conversational pace, real breaths and emotion, natural intonation. Not robotic, not text-to-speech, not formal written Tamil. English words (Amoxicillin, antibiotic, report) are said the way Chennai people naturally say them.
Audio: villain swing music, comic 'ding'.
No subtitles, no captions, no on-screen text or logos.
```

English subtitles:

- Don't you know antibiotics don't work against viruses?

### Clip 13: Good bacteria harmed

Start frame: `reference_frames/clip13.png` · **Keep:** 5 s (cumulative 75 s)

```
High-end stylised 3D animated feature-film look: rounded appealing character designs, soft global illumination, subsurface skin shading, detailed fabric and hair, expressive eyes and natural lip-sync, smooth cinematic camera, shallow depth of field, rich warm colour grade, 16:9 widescreen.

Setting: Same microscopic world, lower part of the vessel where friendly teal and green GOOD bacteria live.
Characters (keep exactly this design):
- THE BOSS (resistant bacterium): large glossy crimson-purple rod-shaped bacterium with a thick glowing capsule, spiky pili, golden whip-like flagellum, cartoon villain face with heavy eyebrows and a jagged-tooth grin.
Action: Antibiotic molecules hit the good bacteria; they wilt, turn grey and droop sadly. THE BOSS gestures at them mockingly.
Camera: Slow pan across the good bacteria, ending on THE BOSS.
Dialogue (spoken in Tamil, lip-synced):
- THE BOSS (resistant bacterium) (mocking; voice: funny, sly comic-villain voice, theatrical laugh, Chennai Tamil slang): "உங்கள பாதுகாக்குற நல்ல bacteria-வையும் பாதிக்கிறீங்க!"
All speech must sound like real human voice actors from Chennai: natural colloquial Chennai Tamil, relaxed conversational pace, real breaths and emotion, natural intonation. Not robotic, not text-to-speech, not formal written Tamil. English words (Amoxicillin, antibiotic, report) are said the way Chennai people naturally say them.
Audio: sad descending blips, villain swing music.
No subtitles, no captions, no on-screen text or logos.
```

English subtitles:

- You even harm the good bacteria that protect you!

### Clip 14: Survivors multiply

Start frame: `reference_frames/clip14.png` · **Keep:** 6 s (cumulative 81 s)

```
High-end stylised 3D animated feature-film look: rounded appealing character designs, soft global illumination, subsurface skin shading, detailed fabric and hair, expressive eyes and natural lip-sync, smooth cinematic camera, shallow depth of field, rich warm colour grade, 16:9 widescreen.

Setting: Same microscopic world.
Characters (keep exactly this design):
- THE BOSS (resistant bacterium): large glossy crimson-purple rod-shaped bacterium with a thick glowing capsule, spiky pili, golden whip-like flagellum, cartoon villain face with heavy eyebrows and a jagged-tooth grin.
Action: The resistant bacteria split in two (binary fission), again and again, quickly filling the frame. THE BOSS gloats.
Camera: Wide shot, slight zoom out as the numbers grow.
Dialogue (spoken in Tamil, lip-synced):
- THE BOSS (resistant bacterium) (gloating; voice: funny, sly comic-villain voice, theatrical laugh, Chennai Tamil slang): "எங்கள அழிச்சிட்டோம்னு நினைக்கிறீங்க… ஆனா எங்கள்ல சில பேரு உயிர் பொழச்சு பெருகுறோம்!"
All speech must sound like real human voice actors from Chennai: natural colloquial Chennai Tamil, relaxed conversational pace, real breaths and emotion, natural intonation. Not robotic, not text-to-speech, not formal written Tamil. English words (Amoxicillin, antibiotic, report) are said the way Chennai people naturally say them.
Audio: wet 'boop' sounds as cells split, villain music building.
No subtitles, no captions, no on-screen text or logos.
```

English subtitles:

- You think you're destroying us… but some of us survive and multiply!

### Clip 15: Villain dance

Start frame: `reference_frames/clip15.png` · **Keep:** 7 s (cumulative 88 s)

```
High-end stylised 3D animated feature-film look: rounded appealing character designs, soft global illumination, subsurface skin shading, detailed fabric and hair, expressive eyes and natural lip-sync, smooth cinematic camera, shallow depth of field, rich warm colour grade, 16:9 widescreen.

Setting: Same microscopic world, now crowded with resistant bacteria.
Characters (keep exactly this design):
- THE BOSS (resistant bacterium): large glossy crimson-purple rod-shaped bacterium with a thick glowing capsule, spiky pili, golden whip-like flagellum, cartoon villain face with heavy eyebrows and a jagged-tooth grin.
Action: The resistant gang high-fives and does a silly synchronised bouncing dance with squash-and-stretch; THE BOSS dances in the centre.
Camera: Circling camera with a slight tilt, comic energy.
Dialogue (spoken in Tamil, lip-synced):
- THE BOSS (resistant bacterium) (laughing, triumphant; voice: funny, sly comic-villain voice, theatrical laugh, Chennai Tamil slang): "ஹா ஹா ஹா! எங்கள எதிர்க்குற மருந்து குறைஞ்சா… எங்க ஆட்டத்த யாருடா நிறுத்துவீங்க?"
All speech must sound like real human voice actors from Chennai: natural colloquial Chennai Tamil, relaxed conversational pace, real breaths and emotion, natural intonation. Not robotic, not text-to-speech, not formal written Tamil. English words (Amoxicillin, antibiotic, report) are said the way Chennai people naturally say them.
Audio: upbeat villain dance music, high-five slaps.
No subtitles, no captions, no on-screen text or logos.
```

English subtitles:

- Ha ha ha! When the medicines that fight us run out… who's going to stop our game?

### Clip 16: The threat

Start frame: `reference_frames/clip16.png` · **Keep:** 5 s (cumulative 93 s)

```
High-end stylised 3D animated feature-film look: rounded appealing character designs, soft global illumination, subsurface skin shading, detailed fabric and hair, expressive eyes and natural lip-sync, smooth cinematic camera, shallow depth of field, rich warm colour grade, 16:9 widescreen.

Setting: Same microscopic world; music stops, everything freezes, the light turns dark purple.
Characters (keep exactly this design):
- THE BOSS (resistant bacterium): large glossy crimson-purple rod-shaped bacterium with a thick glowing capsule, spiky pili, golden whip-like flagellum, cartoon villain face with heavy eyebrows and a jagged-tooth grin.
Action: THE BOSS slowly turns to the camera; his grin fades into a menacing look; eyes glint.
Camera: Slow push-in to an extreme close-up of his face, lit from below.
Dialogue (spoken in Tamil, lip-synced):
- THE BOSS (resistant bacterium) (slow, low, threatening whisper; voice: funny, sly comic-villain voice, theatrical laugh, Chennai Tamil slang): "இதுதான் Antimicrobial Resistance! சில infections-க்கு மருந்தே வேலை செய்யலைன்னா… என்ன பண்ணுவீங்கடா?"
All speech must sound like real human voice actors from Chennai: natural colloquial Chennai Tamil, relaxed conversational pace, real breaths and emotion, natural intonation. Not robotic, not text-to-speech, not formal written Tamil. English words (Amoxicillin, antibiotic, report) are said the way Chennai people naturally say them.
Audio: record scratch, then silence, then a low drone.
No subtitles, no captions, no on-screen text or logos.
```

English subtitles:

- This is Antimicrobial Resistance! When medicines stop working for some infections… what will you do?

### Clip 17: Black screen: narrator

Start frame: `reference_frames/clip17.png` · **Keep:** 5 s (cumulative 98 s)

```
High-end stylised 3D animated feature-film look: rounded appealing character designs, soft global illumination, subsurface skin shading, detailed fabric and hair, expressive eyes and natural lip-sync, smooth cinematic camera, shallow depth of field, rich warm colour grade, 16:9 widescreen.

Setting: The image fades to black; a faint red glow pulses with a heartbeat.
Characters (keep exactly this design):
- NARRATOR: off-screen.
Action: Darkness, pulsing red vignette in time with the heartbeat.
Camera: Static.
Dialogue (spoken in Tamil, lip-synced):
- NARRATOR (serious, slow; voice: deep, serious, measured male voice, clear neutral Tamil): "தேவையில்லாம antibiotics பயன்படுத்துறது, resistant bacteria உயிர் பொழச்சு பெருகுறதுக்கு வழிவகுக்கலாம்."
All speech must sound like real human voice actors from Chennai: natural colloquial Chennai Tamil, relaxed conversational pace, real breaths and emotion, natural intonation. Not robotic, not text-to-speech, not formal written Tamil. English words (Amoxicillin, antibiotic, report) are said the way Chennai people naturally say them.
Audio: heavy heartbeat, low boom.
No subtitles, no captions, no on-screen text or logos.
```

English subtitles:

- Unnecessary antibiotic use allows resistant bacteria to survive and multiply.

### Clip 18: Days later: hospital

Start frame: `reference_frames/clip18.png` · **Keep:** 6 s (cumulative 104 s)

```
High-end stylised 3D animated feature-film look: rounded appealing character designs, soft global illumination, subsurface skin shading, detailed fabric and hair, expressive eyes and natural lip-sync, smooth cinematic camera, shallow depth of field, rich warm colour grade, 16:9 widescreen.

Setting: A wall calendar flips three days; then a modern Chennai hospital ward: clean beds, monitor, IV stand.
Characters (keep exactly this design):
- STUDENT 1: 16-year-old Tamil schoolboy, slim, medium-brown skin, short neat black hair parted on the left, all-white school uniform (short-sleeved shirt with maroon crest on pocket, white trousers), maroon-and-gold striped tie, navy backpack, green bicycle.
- MOTHER: Tamil woman about 45, hair in a low bun, small red pottu, simple maroon cotton saree with gold border, thin gold chain.
- CONSULTANT PHYSICIAN: doctor about 52, salt-and-pepper hair, rimless glasses, white coat over light-blue shirt and navy tie, stethoscope around neck, hospital ID badge.
Action: STUDENT 1 lies weak and sweaty in a light-blue hospital gown. His MOTHER hurries to the CONSULTANT PHYSICIAN, hands clasped, pleading.
Camera: Calendar insert, then a medium wide shot of the ward.
Dialogue (spoken in Tamil, lip-synced):
- MOTHER (worried, breathless; voice: anxious, emotional middle-aged woman's voice, natural Chennai Tamil): "டாக்டர், காய்ச்சல் குறையவே இல்ல. இப்போ அவனுக்கு ரொம்ப முடியல!"
All speech must sound like real human voice actors from Chennai: natural colloquial Chennai Tamil, relaxed conversational pace, real breaths and emotion, natural intonation. Not robotic, not text-to-speech, not formal written Tamil. English words (Amoxicillin, antibiotic, report) are said the way Chennai people naturally say them.
Audio: calendar pages flipping, hospital ambience, monitor beeps.
No subtitles, no captions, no on-screen text or logos.
```

English subtitles:

- Doctor, the fever hasn't come down at all. He's really unwell now!

### Clip 19: The physician reassures

Start frame: `reference_frames/clip19.png` · **Keep:** 7 s (cumulative 111 s)

```
High-end stylised 3D animated feature-film look: rounded appealing character designs, soft global illumination, subsurface skin shading, detailed fabric and hair, expressive eyes and natural lip-sync, smooth cinematic camera, shallow depth of field, rich warm colour grade, 16:9 widescreen.

Setting: Same hospital ward.
Characters (keep exactly this design):
- STUDENT 1: 16-year-old Tamil schoolboy, slim, medium-brown skin, short neat black hair parted on the left, all-white school uniform (short-sleeved shirt with maroon crest on pocket, white trousers), maroon-and-gold striped tie, navy backpack, green bicycle.
- MOTHER: Tamil woman about 45, hair in a low bun, small red pottu, simple maroon cotton saree with gold border, thin gold chain.
- CONSULTANT PHYSICIAN: doctor about 52, salt-and-pepper hair, rimless glasses, white coat over light-blue shirt and navy tie, stethoscope around neck, hospital ID badge.
Action: The CONSULTANT PHYSICIAN raises a calming hand, then examines STUDENT 1 with his stethoscope and checks his forehead.
Camera: Medium two-shot, then over to the bedside.
Dialogue (spoken in Tamil, lip-synced):
- CONSULTANT PHYSICIAN (calm, reassuring; voice: calm, warm, mature male voice, polite spoken Chennai Tamil mixed with English medical words): "கவலைப்படாதீங்கம்மா. அவன செக் பண்ணி, தேவையான investigations பண்ணலாம். Infection எதனால வந்துச்சுன்னு கண்டுபிடிக்கறது முக்கியம்."
All speech must sound like real human voice actors from Chennai: natural colloquial Chennai Tamil, relaxed conversational pace, real breaths and emotion, natural intonation. Not robotic, not text-to-speech, not formal written Tamil. English words (Amoxicillin, antibiotic, report) are said the way Chennai people naturally say them.
Audio: hospital ambience, monitor beeps.
No subtitles, no captions, no on-screen text or logos.
```

English subtitles:

- Don't worry, amma. We'll examine him and do the necessary investigations. Finding the cause of the infection is important.

### Clip 20: Lab montage

Start frame: `reference_frames/clip20.png` · **Keep:** 4 s (cumulative 115 s)

```
High-end stylised 3D animated feature-film look: rounded appealing character designs, soft global illumination, subsurface skin shading, detailed fabric and hair, expressive eyes and natural lip-sync, smooth cinematic camera, shallow depth of field, rich warm colour grade, 16:9 widescreen.

Setting: A modern hospital microbiology laboratory.
Action: Quick realistic montage: a nurse draws blood from an arm; blood goes into blood-culture bottles; a lab technician loads them into an incubator; bacterial colonies on an agar plate; an antibiotic susceptibility plate with small paper discs and clear zones.
Camera: Quick cuts, about one second each, macro lens.
No dialogue.
Audio: lab hum, glass clinks, incubator door.
No subtitles, no captions, no on-screen text or logos.
```

### Clip 21: The culture report

Start frame: `reference_frames/clip21.png` · **Keep:** 5 s (cumulative 120 s)

```
High-end stylised 3D animated feature-film look: rounded appealing character designs, soft global illumination, subsurface skin shading, detailed fabric and hair, expressive eyes and natural lip-sync, smooth cinematic camera, shallow depth of field, rich warm colour grade, 16:9 widescreen.

Setting: Hospital microbiology lab; a computer monitor shows an agar plate photo and a table of antibiotics marked R and S.
Characters (keep exactly this design):
- CONSULTANT MICROBIOLOGIST: doctor about 40, short black hair, neatly trimmed beard, square black glasses, white lab coat over grey shirt, ID badge on a blue lanyard.
Action: The CONSULTANT MICROBIOLOGIST studies the report on screen and speaks, then picks up the printed report.
Camera: Over-the-shoulder on the monitor, then medium on him.
Dialogue (spoken in Tamil, lip-synced):
- CONSULTANT MICROBIOLOGIST (clear, concerned; voice: clear, confident male teacher-like voice, spoken Chennai Tamil mixed with English medical words): "Doctor, culture report-ல இந்த bacteria நிறைய antibiotics-க்கு resistant-ஆ இருக்கு."
All speech must sound like real human voice actors from Chennai: natural colloquial Chennai Tamil, relaxed conversational pace, real breaths and emotion, natural intonation. Not robotic, not text-to-speech, not formal written Tamil. English words (Amoxicillin, antibiotic, report) are said the way Chennai people naturally say them.
Audio: keyboard clicks, lab hum.
No subtitles, no captions, no on-screen text or logos.
```

English subtitles:

- Doctor, the culture report shows this bacterium is resistant to many antibiotics.

### Clip 22: Microbiologist meets physician

Start frame: `reference_frames/clip22.png` · **Keep:** 5 s (cumulative 125 s)

```
High-end stylised 3D animated feature-film look: rounded appealing character designs, soft global illumination, subsurface skin shading, detailed fabric and hair, expressive eyes and natural lip-sync, smooth cinematic camera, shallow depth of field, rich warm colour grade, 16:9 widescreen.

Setting: The consultant physician's office.
Characters (keep exactly this design):
- CONSULTANT MICROBIOLOGIST: doctor about 40, short black hair, neatly trimmed beard, square black glasses, white lab coat over grey shirt, ID badge on a blue lanyard.
- CONSULTANT PHYSICIAN: doctor about 52, salt-and-pepper hair, rimless glasses, white coat over light-blue shirt and navy tie, stethoscope around neck, hospital ID badge.
Action: The CONSULTANT MICROBIOLOGIST walks in holding the printed report and shows it to the CONSULTANT PHYSICIAN.
Camera: Walking shot into a medium two-shot.
Dialogue (spoken in Tamil, lip-synced):
- CONSULTANT MICROBIOLOGIST (clear, firm; voice: clear, confident male teacher-like voice, spoken Chennai Tamil mixed with English medical words): "Susceptibility results-ஐ வச்சுதான் treatment-ஐ select பண்ணணும்."
All speech must sound like real human voice actors from Chennai: natural colloquial Chennai Tamil, relaxed conversational pace, real breaths and emotion, natural intonation. Not robotic, not text-to-speech, not formal written Tamil. English words (Amoxicillin, antibiotic, report) are said the way Chennai people naturally say them.
Audio: footsteps, paper rustle.
No subtitles, no captions, no on-screen text or logos.
```

English subtitles:

- We must choose treatment based on the susceptibility results.

### Clip 23: Deciding treatment

Start frame: `reference_frames/clip23.png` · **Keep:** 6 s (cumulative 131 s)

```
High-end stylised 3D animated feature-film look: rounded appealing character designs, soft global illumination, subsurface skin shading, detailed fabric and hair, expressive eyes and natural lip-sync, smooth cinematic camera, shallow depth of field, rich warm colour grade, 16:9 widescreen.

Setting: Same office.
Characters (keep exactly this design):
- CONSULTANT MICROBIOLOGIST: doctor about 40, short black hair, neatly trimmed beard, square black glasses, white lab coat over grey shirt, ID badge on a blue lanyard.
- CONSULTANT PHYSICIAN: doctor about 52, salt-and-pepper hair, rimless glasses, white coat over light-blue shirt and navy tie, stethoscope around neck, hospital ID badge.
Action: Both doctors lean over the report together; the CONSULTANT PHYSICIAN nods and replies.
Camera: Two-shot over the desk, slow push-in.
Dialogue (spoken in Tamil, lip-synced):
- CONSULTANT PHYSICIAN (thoughtful, decisive; voice: calm, warm, mature male voice, polite spoken Chennai Tamil mixed with English medical words): "சரி. Patient-ஓட clinical condition-உம் report-உம் பாத்து சரியான treatment முடிவு பண்ணலாம்."
All speech must sound like real human voice actors from Chennai: natural colloquial Chennai Tamil, relaxed conversational pace, real breaths and emotion, natural intonation. Not robotic, not text-to-speech, not formal written Tamil. English words (Amoxicillin, antibiotic, report) are said the way Chennai people naturally say them.
Audio: quiet office ambience.
No subtitles, no captions, no on-screen text or logos.
```

English subtitles:

- Alright. We'll decide the right treatment based on the patient's clinical condition and the report.

### Clip 24: Explaining to the mother

Start frame: `reference_frames/clip24.png` · **Keep:** 7 s (cumulative 138 s)

```
High-end stylised 3D animated feature-film look: rounded appealing character designs, soft global illumination, subsurface skin shading, detailed fabric and hair, expressive eyes and natural lip-sync, smooth cinematic camera, shallow depth of field, rich warm colour grade, 16:9 widescreen.

Setting: Hospital ward bedside; STUDENT 1 resting in bed.
Characters (keep exactly this design):
- CONSULTANT PHYSICIAN: doctor about 52, salt-and-pepper hair, rimless glasses, white coat over light-blue shirt and navy tie, stethoscope around neck, hospital ID badge.
- MOTHER: Tamil woman about 45, hair in a low bun, small red pottu, simple maroon cotton saree with gold border, thin gold chain.
- STUDENT 1: 16-year-old Tamil schoolboy, slim, medium-brown skin, short neat black hair parted on the left, all-white school uniform (short-sleeved shirt with maroon crest on pocket, white trousers), maroon-and-gold striped tie, navy backpack, green bicycle.
Action: The CONSULTANT PHYSICIAN explains gently to the MOTHER, using small hand gestures; she listens carefully.
Camera: Medium shot favouring the physician, the mother in the foreground.
Dialogue (spoken in Tamil, lip-synced):
- CONSULTANT PHYSICIAN (gentle, explaining; voice: calm, warm, mature male voice, polite spoken Chennai Tamil mixed with English medical words): "Antibiotics எல்லா நோய்க்கும் தீர்வு இல்லம்மா. தொண்டை வலி, காய்ச்சல் வந்தாலே antibiotic வேணும்னு அர்த்தம் இல்ல."
All speech must sound like real human voice actors from Chennai: natural colloquial Chennai Tamil, relaxed conversational pace, real breaths and emotion, natural intonation. Not robotic, not text-to-speech, not formal written Tamil. English words (Amoxicillin, antibiotic, report) are said the way Chennai people naturally say them.
Audio: soft hospital ambience.
No subtitles, no captions, no on-screen text or logos.
```

English subtitles:

- Antibiotics aren't the answer to every illness. A sore throat or fever doesn't mean you need an antibiotic.

### Clip 25: Virus cutaway

Start frame: `reference_frames/clip25.png` · **Keep:** 6 s (cumulative 144 s)

```
High-end stylised 3D animated feature-film look: rounded appealing character designs, soft global illumination, subsurface skin shading, detailed fabric and hair, expressive eyes and natural lip-sync, smooth cinematic camera, shallow depth of field, rich warm colour grade, 16:9 widescreen.

Setting: A simple animated insert: a cute spiky purple virus floating in a dark violet space.
Characters (keep exactly this design):
- CONSULTANT PHYSICIAN: doctor about 52, salt-and-pepper hair, rimless glasses, white coat over light-blue shirt and navy tie, stethoscope around neck, hospital ID badge.
Action: Glowing yellow antibiotic molecules fly at the virus and bounce off harmlessly; the virus smiles, unaffected. (The physician's voice continues over the insert.)
Camera: Static centred shot with gentle drift.
Dialogue (spoken in Tamil, lip-synced):
- CONSULTANT PHYSICIAN (gentle, explaining (voice-over); voice: calm, warm, mature male voice, polite spoken Chennai Tamil mixed with English medical words): "நிறைய infections வைரஸால தான் வருது; antibiotics வைரஸுக்கு வேலை செய்யாது."
All speech must sound like real human voice actors from Chennai: natural colloquial Chennai Tamil, relaxed conversational pace, real breaths and emotion, natural intonation. Not robotic, not text-to-speech, not formal written Tamil. English words (Amoxicillin, antibiotic, report) are said the way Chennai people naturally say them.
Audio: soft 'boing' bounces.
No subtitles, no captions, no on-screen text or logos.
```

English subtitles:

- Many infections are caused by viruses; antibiotics don't work against viruses.

### Clip 26: Bacteria resist, not people

Start frame: `reference_frames/clip26.png` · **Keep:** 7 s (cumulative 151 s)

```
High-end stylised 3D animated feature-film look: rounded appealing character designs, soft global illumination, subsurface skin shading, detailed fabric and hair, expressive eyes and natural lip-sync, smooth cinematic camera, shallow depth of field, rich warm colour grade, 16:9 widescreen.

Setting: Hospital ward bedside.
Characters (keep exactly this design):
- CONSULTANT MICROBIOLOGIST: doctor about 40, short black hair, neatly trimmed beard, square black glasses, white lab coat over grey shirt, ID badge on a blue lanyard.
- CONSULTANT PHYSICIAN: doctor about 52, salt-and-pepper hair, rimless glasses, white coat over light-blue shirt and navy tie, stethoscope around neck, hospital ID badge.
- MOTHER: Tamil woman about 45, hair in a low bun, small red pottu, simple maroon cotton saree with gold border, thin gold chain.
Action: The CONSULTANT MICROBIOLOGIST joins and explains to the MOTHER. Cut briefly to an insert of blue bacteria bursting while red resistant bacteria survive.
Camera: Medium shot of the microbiologist, quick insert, back to him.
Dialogue (spoken in Tamil, lip-synced):
- CONSULTANT MICROBIOLOGIST (clear, teacher-like; voice: clear, confident male teacher-like voice, spoken Chennai Tamil mixed with English medical words): "Antimicrobial resistance-ங்கறது மனுஷங்களுக்கு வர்ற resistance இல்ல; bacteria தான் antibiotics-ஐ எதிர்க்குற சக்திய பெறுது."
All speech must sound like real human voice actors from Chennai: natural colloquial Chennai Tamil, relaxed conversational pace, real breaths and emotion, natural intonation. Not robotic, not text-to-speech, not formal written Tamil. English words (Amoxicillin, antibiotic, report) are said the way Chennai people naturally say them.
Audio: soft hospital ambience.
No subtitles, no captions, no on-screen text or logos.
```

English subtitles:

- Antimicrobial resistance isn't resistance in humans; it's the bacteria that gain the ability to resist antibiotics.

### Clip 27: Misuse makes it worse

Start frame: `reference_frames/clip27.png` · **Keep:** 5 s (cumulative 156 s)

```
High-end stylised 3D animated feature-film look: rounded appealing character designs, soft global illumination, subsurface skin shading, detailed fabric and hair, expressive eyes and natural lip-sync, smooth cinematic camera, shallow depth of field, rich warm colour grade, 16:9 widescreen.

Setting: Insert of the printed laboratory report on a clipboard: rows of antibiotics marked R (red) and S (green); a doctor's pen ticks the effective ones. Then back to the microbiologist.
Characters (keep exactly this design):
- CONSULTANT MICROBIOLOGIST: doctor about 40, short black hair, neatly trimmed beard, square black glasses, white lab coat over grey shirt, ID badge on a blue lanyard.
Action: The pen ticks the S rows; the microbiologist finishes his point.
Camera: Close-up on the report, then medium close-up of the microbiologist.
Dialogue (spoken in Tamil, lip-synced):
- CONSULTANT MICROBIOLOGIST (serious; voice: clear, confident male teacher-like voice, spoken Chennai Tamil mixed with English medical words): "தேவையில்லாத, தப்பான antibiotic பயன்பாடு இந்தப் பிரச்சனைய இன்னும் அதிகமாக்கலாம்."
All speech must sound like real human voice actors from Chennai: natural colloquial Chennai Tamil, relaxed conversational pace, real breaths and emotion, natural intonation. Not robotic, not text-to-speech, not formal written Tamil. English words (Amoxicillin, antibiotic, report) are said the way Chennai people naturally say them.
Audio: pen scratch, soft ambience.
No subtitles, no captions, no on-screen text or logos.
```

English subtitles:

- Unnecessary and incorrect antibiotic use can make this problem worse.

### Clip 28: Final message: physician

Start frame: `reference_frames/clip28.png` · **Keep:** 7 s (cumulative 163 s)

```
High-end stylised 3D animated feature-film look: rounded appealing character designs, soft global illumination, subsurface skin shading, detailed fabric and hair, expressive eyes and natural lip-sync, smooth cinematic camera, shallow depth of field, rich warm colour grade, 16:9 widescreen.

Setting: A bright, clean hospital corridor. In the soft-focus background, through a ward doorway, STUDENT 1 sits up in bed on an IV drip, recovering, with his MOTHER beside him.
Characters (keep exactly this design):
- CONSULTANT PHYSICIAN: doctor about 52, salt-and-pepper hair, rimless glasses, white coat over light-blue shirt and navy tie, stethoscope around neck, hospital ID badge.
- CONSULTANT MICROBIOLOGIST: doctor about 40, short black hair, neatly trimmed beard, square black glasses, white lab coat over grey shirt, ID badge on a blue lanyard.
- STUDENT 1: 16-year-old Tamil schoolboy, slim, medium-brown skin, short neat black hair parted on the left, all-white school uniform (short-sleeved shirt with maroon crest on pocket, white trousers), maroon-and-gold striped tie, navy backpack, green bicycle.
- MOTHER: Tamil woman about 45, hair in a low bun, small red pottu, simple maroon cotton saree with gold border, thin gold chain.
Action: Both doctors stand side by side looking straight into the camera; the CONSULTANT PHYSICIAN speaks warmly and confidently.
Camera: Medium two-shot at eye level, slow push-in.
Dialogue (spoken in Tamil, lip-synced):
- CONSULTANT PHYSICIAN (warm, confident; voice: calm, warm, mature male voice, polite spoken Chennai Tamil mixed with English medical words): "டாக்டர் ஆலோசனை இல்லாம antibiotics எடுக்காதீங்க. குடுத்த dose-ஐயும் duration-ஐயும் முழுசா follow பண்ணுங்க."
All speech must sound like real human voice actors from Chennai: natural colloquial Chennai Tamil, relaxed conversational pace, real breaths and emotion, natural intonation. Not robotic, not text-to-speech, not formal written Tamil. English words (Amoxicillin, antibiotic, report) are said the way Chennai people naturally say them.
Audio: soft hospital room tone, gentle inspiring music begins.
No subtitles, no captions, no on-screen text or logos.
```

English subtitles:

- Don't take antibiotics without a doctor's advice. Follow the prescribed dose and duration fully.

### Clip 29: Final message: microbiologist

Start frame: `reference_frames/clip29.png` · **Keep:** 7 s (cumulative 170 s)

```
High-end stylised 3D animated feature-film look: rounded appealing character designs, soft global illumination, subsurface skin shading, detailed fabric and hair, expressive eyes and natural lip-sync, smooth cinematic camera, shallow depth of field, rich warm colour grade, 16:9 widescreen.

Setting: Same bright hospital corridor.
Characters (keep exactly this design):
- CONSULTANT PHYSICIAN: doctor about 52, salt-and-pepper hair, rimless glasses, white coat over light-blue shirt and navy tie, stethoscope around neck, hospital ID badge.
- CONSULTANT MICROBIOLOGIST: doctor about 40, short black hair, neatly trimmed beard, square black glasses, white lab coat over grey shirt, ID badge on a blue lanyard.
Action: The CONSULTANT MICROBIOLOGIST speaks to the camera with conviction.
Camera: Same set-up, slight reframe onto the microbiologist.
Dialogue (spoken in Tamil, lip-synced):
- CONSULTANT MICROBIOLOGIST (inspiring, sincere; voice: clear, confident male teacher-like voice, spoken Chennai Tamil mixed with English medical words): "Antibiotics-ஐ பொறுப்பா use பண்றது நம்ம எல்லாரோட கடமை. இன்னைக்கும் நாளைக்கும் அது உயிர காப்பாத்தணும்."
All speech must sound like real human voice actors from Chennai: natural colloquial Chennai Tamil, relaxed conversational pace, real breaths and emotion, natural intonation. Not robotic, not text-to-speech, not formal written Tamil. English words (Amoxicillin, antibiotic, report) are said the way Chennai people naturally say them.
Audio: inspiring music rising.
No subtitles, no captions, no on-screen text or logos.
```

English subtitles:

- Using antibiotics responsibly is the duty of all of us. They must keep saving lives, today and tomorrow.

### Clip 30: Slogan

Start frame: `reference_frames/clip30.png` · **Keep:** 5 s (cumulative 175 s)

```
High-end stylised 3D animated feature-film look: rounded appealing character designs, soft global illumination, subsurface skin shading, detailed fabric and hair, expressive eyes and natural lip-sync, smooth cinematic camera, shallow depth of field, rich warm colour grade, 16:9 widescreen.

Setting: Same corridor, light becoming brighter and warmer, gentle lens bloom.
Characters (keep exactly this design):
- CONSULTANT PHYSICIAN: doctor about 52, salt-and-pepper hair, rimless glasses, white coat over light-blue shirt and navy tie, stethoscope around neck, hospital ID badge.
- CONSULTANT MICROBIOLOGIST: doctor about 40, short black hair, neatly trimmed beard, square black glasses, white lab coat over grey shirt, ID badge on a blue lanyard.
Action: Both doctors say the slogan together, powerfully, looking into the camera. Leave clear empty space in the upper half of the frame for titles added in editing.
Camera: Low-angle medium shot, slow push-in.
Dialogue (spoken in Tamil, lip-synced):
- BOTH DOCTORS together (together, powerful, in English): "Use antibiotics wisely. Stop antimicrobial resistance. Save our future!"
All speech must sound like real human voice actors from Chennai: natural colloquial Chennai Tamil, relaxed conversational pace, real breaths and emotion, natural intonation. Not robotic, not text-to-speech, not formal written Tamil. English words (Amoxicillin, antibiotic, report) are said the way Chennai people naturally say them.
Audio: cinematic impact hits on each phrase, inspiring orchestral swell.
No subtitles, no captions, no on-screen text or logos.
```

English subtitles:

- USE ANTIBIOTICS WISELY. STOP ANTIMICROBIAL RESISTANCE. SAVE OUR FUTURE!

## Editing

- **Order and length:** clips 01–30 in order, each trimmed to its *Keep* time (175 s), then the end card (5 s) for a total of 180 s. Trim the dead air at the start and end of each clip rather than cutting speech.
- **End card:** reuse the last 5 seconds of the 2D film (`../AMR_Awareness_Film_1080p.mp4`, 02:55–03:00). It already has clean typography: *ANTIMICROBIAL RESISTANCE AWARENESS WEEK* / *“USE WISELY. PRESERVE THEIR POWER.”*
- **Clip 03 phone screen:** overlay the question bubble *“I have a sore throat and fever. What medicine should I take?”* and then the reply *“Do not self-medicate with antibiotics. Consult a healthcare professional.”* (you can screenshot `reference_frames/clip03.png`).
- **Clip 07:** add a small red tag *“No prescription asked!”* at the hand-over so the scene is not read as good practice.
- **Clip 30 titles:** bold white text, one line at a time on the beat: **USE ANTIBIOTICS WISELY.** / **STOP ANTIMICROBIAL RESISTANCE.** (yellow) / **SAVE OUR FUTURE!** (green).
- **Subtitles:** white sans-serif, bottom centre, on a semi-transparent dark box, timed to the speech. Use the English lines under each clip.
- **Music:** most prompts ask Veo for ambience and effects only, so the music doesn't jump between clips. Lay one music track per mood in the editor (playful for clips 1–9, comic villain for 10–15, dark for 16–17, soft piano for 18–27, inspiring for 28–30), kept well below the dialogue. If Veo adds music anyway, lower or mute it under the speech.
- **Captions in the 2D film:** to keep the teaching labels from the 2D film (*Sensitive bacteria*, *Good bacteria harmed too*, *Antibiotics do not work against viruses*, *Bacteria become resistant, not people*), add them as titles at the top of the frame on clips 10, 13, 25 and 26.

Regenerate this file with `python3 gemini/make_prompts.py`.