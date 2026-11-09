#!/usr/bin/env python3
"""Generates GEMINI_PROMPTS.md: one self-contained, copy-paste Veo prompt per
8-second clip, with locked character, voice and style text repeated in each."""
from pathlib import Path

STYLE = ("High-end stylised 3D animated feature-film look: rounded appealing character designs, soft global "
         "illumination, subsurface skin shading, detailed fabric and hair, expressive eyes and natural lip-sync, "
         "smooth cinematic camera, shallow depth of field, rich warm colour grade, 16:9 widescreen.")

CHAR = {
    "S1": ("STUDENT 1", "16-year-old Tamil schoolboy, slim, medium-brown skin, short neat black hair parted on the left, "
           "all-white school uniform (short-sleeved shirt with maroon crest on pocket, white trousers), maroon-and-gold "
           "striped tie, navy backpack, green bicycle",
           "young male teen voice, slightly hoarse and tired, casual Chennai Tamil"),
    "S2": ("STUDENT 2", "16-year-old Tamil schoolboy, slightly chubby, darker brown skin, thick curly black hair, big "
           "cheeky grin, same white uniform with loose maroon-and-gold tie, red backpack, red bicycle with a bell",
           "energetic, cheeky young male teen voice, fast and funny, street-style Chennai Tamil"),
    "PH": ("PHARMACIST", "man about 40, neat moustache, rectangular glasses, white pharmacist coat over a light-blue shirt",
           "silent"),
    "MO": ("MOTHER", "Tamil woman about 45, hair in a low bun, small red pottu, simple maroon cotton saree with gold border, thin gold chain",
           "anxious, emotional middle-aged woman's voice, natural Chennai Tamil"),
    "DR": ("CONSULTANT PHYSICIAN", "doctor about 52, salt-and-pepper hair, rimless glasses, white coat over light-blue shirt "
           "and navy tie, stethoscope around neck, hospital ID badge",
           "calm, warm, mature male voice, polite spoken Chennai Tamil mixed with English medical words"),
    "MB": ("CONSULTANT MICROBIOLOGIST", "doctor about 40, short black hair, neatly trimmed beard, square black glasses, white "
           "lab coat over grey shirt, ID badge on a blue lanyard",
           "clear, confident male teacher-like voice, spoken Chennai Tamil mixed with English medical words"),
    "BOSS": ("THE BOSS (resistant bacterium)", "large glossy crimson-purple rod-shaped bacterium with a thick glowing capsule, "
             "spiky pili, golden whip-like flagellum, cartoon villain face with heavy eyebrows and a jagged-tooth grin",
             "funny, sly comic-villain voice, theatrical laugh, Chennai Tamil slang"),
    "SMART": ("SMART BACTERIUM", "smaller red resistant rod-shaped bacterium with spiky pili and a know-it-all face",
              "squeaky, smug little voice, Chennai Tamil"),
    "NAR": ("NARRATOR", "off-screen", "deep, serious, measured male voice, clear neutral Tamil"),
}

VOICE_RULE = ("All speech must sound like real human voice actors from Chennai: natural colloquial Chennai Tamil, relaxed "
              "conversational pace, real breaths and emotion, natural intonation. Not robotic, not text-to-speech, not "
              "formal written Tamil. English words (Amoxicillin, antibiotic, report) are said the way Chennai people "
              "naturally say them.")
NO_TEXT = "No subtitles, no captions, no on-screen text or logos."

# (title, frame, keep_seconds, chars, setting, action, camera, dialogue[(char, delivery, tamil, english)], audio)
CLIPS = [
    ("School morning: the sore throat", 1, 6, ["S1", "S2"],
     "A bright school campus in Chennai in the morning: cream two-storey buildings with red-tile roofs, a big shady tree, sandy ground, students in white uniforms in the background.",
     "STUDENT 1 stands near the building, touching his throat, looking feverish. STUDENT 2 walks in happily, humming, and stops beside him.",
     "Slow crane down from a wide establishing shot to a medium two-shot.",
     [("S1", "hoarse, tired", "டேய் மச்சி, தொண்டை ரொம்ப வலிக்குதுடா… காய்ச்சல் மாதிரியும் இருக்கு.",
       "Machi, my throat really hurts, da… feels like a fever too.")],
     "school ambience, birds chirping, distant children playing; no background music"),
    ("Doctor? No, ask AI", 2, 6, ["S1", "S2"],
     "Same school campus, morning.",
     "STUDENT 2 looks concerned and asks. STUDENT 1 waves it off and pulls out his smartphone with a sly smile.",
     "Medium two-shot, gentle push-in.",
     [("S2", "concerned", "என்னடா ஆச்சு? டாக்டர்கிட்ட போலாமா?", "What happened, da? Shall we go to the doctor?"),
      ("S1", "dismissive, casual", "அதெல்லாம் வேணாம் டா. ChatGPT-ல கேட்டுப் பாக்கலாம்.", "No need for all that, da. Let's ask ChatGPT.")],
     "school ambience"),
    ("Phone close-up", 3, 4, ["S1"],
     "Close-up of STUDENT 1's hands holding a smartphone; generic chat app with no logo; the screen glows brightly and is kept softly out of focus (text will be added in editing).",
     "His thumbs type a message; a reply bubble pops up; he glances at it and shrugs.",
     "Over-the-shoulder close-up, slow push-in.",
     [],
     "phone keyboard taps, a soft notification ping, faint school ambience"),
    ("The wrong advice", 4, 7, ["S1", "S2"],
     "Same school campus, morning.",
     "STUDENT 2 pushes the phone down playfully, thumps his chest proudly and gives confident advice. STUDENT 1 grins and agrees, raising a fist.",
     "Medium two-shot favouring STUDENT 2, then a quick push-in.",
     [("S2", "proud, confident", "டேய், எனக்கும் முன்னாடி இப்படித்தான் இருந்துச்சு. நான் Amoxicillin எடுத்தேன். நீயும் எடுத்துக்கோ டா!",
       "Da, I had the same thing before. I took Amoxicillin. You take it too, da!"),
      ("S1", "cheerful", "சரி டா! வா, pharmacy போலாம்!", "OK da! Come, let's go to the pharmacy!")],
     "school ambience"),
    ("Cycling song, part 1", 5, 7, ["S1", "S2"],
     "A sunny Chennai neighbourhood street: coconut palms, colourful houses, a temple gopuram in the distance.",
     "Both boys ride their bicycles side by side. STUDENT 2 sings a funny gaana-style song with big gestures, one hand off the handlebar; STUDENT 1 smiles weakly.",
     "Side-tracking shot at handlebar height, moving with the bikes.",
     [("S2", "sung, off-key, Chennai gaana style, a cappella", "ஊசி போட உடம்பு இருந்தா… டாக்டர்கிட்ட போகணுமா?",
       "♪ If you've got a body for injections… do we really have to see a doctor? ♪")],
     "bicycle chains, two rings of a bicycle bell, birds, light traffic; no background music"),
    ("Cycling song, part 2", 6, 7, ["S1", "S2"],
     "Same Chennai street; a small pharmacy with a green cross sign comes into view.",
     "STUDENT 2 finishes the song, rings his bell, and both boys burst out laughing as they reach the pharmacy. An auto-rickshaw passes in the background.",
     "Front tracking shot, then wide as they arrive.",
     [("S2", "sung, Chennai gaana style", "Pharmacy-க்கு சைக்கிள் மிதிச்சு… மாத்திரை வாங்கிப் போடலாமா?",
       "♪ Let's pedal to the pharmacy… shall we just buy pills and pop them? ♪")],
     "bicycle bell, laughter, auto-rickshaw passing; no background music"),
    ("At the pharmacy counter", 7, 7, ["S1", "S2", "PH"],
     "A small, cluttered community pharmacy: shelves packed with colourful medicine boxes, a glass counter, a ceiling fan.",
     "STUDENT 1 asks at the counter, hand on his throat. The PHARMACIST, without asking for a prescription, slides a strip of amoxicillin capsules across the counter. The lighting dims slightly at the hand-over (this is bad practice).",
     "Medium wide from behind the counter, then a close-up of the hand-over.",
     [("S1", "hoarse, polite", "அண்ணா, Amoxicillin இருக்கா? தொண்டை வலியும் காய்ச்சலும் இருக்கு.",
       "Anna, do you have Amoxicillin? I have a sore throat and fever.")],
     "door chime, ceiling fan hum, rustle of a medicine strip, a low ominous note at the hand-over"),
    ("'So easy!'", 8, 5, ["S1", "S2"],
     "Same pharmacy, at the door.",
     "STUDENT 2 waves the medicine strip triumphantly; both walk out into the sunlight.",
     "Medium two-shot tracking them to the door.",
     [("S2", "triumphant", "பாத்தியா டா! எவ்ளோ easy-ஆ மாத்திரை வாங்கிட்டோம்!", "See, da! We got the tablets so easily!"),
      ("S1", "relieved", "ஆமாடா! வா, வீட்டுக்குப் போலாம்!", "Yeah da! Come, let's go home!")],
     "street ambience as the door opens"),
    ("Swallow and dive", 9, 4, ["S1"],
     "A simple home kitchen in Chennai.",
     "STUDENT 1 pops a capsule from the strip and swallows it with a glass of water. The camera rushes into his mouth and down the throat, through a glowing red tunnel, into a blood vessel.",
     "Medium shot, then a fast dramatic push-in transition into the body.",
     [],
     "capsule popping from the blister, a gulp, a deep whoosh and a muffled heartbeat"),
    ("Inside the body: the antibiotic arrives", 10, 7, ["BOSS"],
     "Microscopic world inside a blood vessel: crimson plasma, red blood cells tumbling past. Small friendly blue and green SENSITIVE bacteria and teal GOOD bacteria float along; a few red-purple RESISTANT bacteria hide among them.",
     "Glowing yellow amoxicillin molecules stream in; wherever they touch blue and green bacteria, the bacteria burst like soap bubbles. The resistant ones survive. THE BOSS slides into view, laughing, and speaks to the camera.",
     "Flowing dolly along the vessel, ending on a low-angle hero shot of THE BOSS.",
     [("BOSS", "laughing, mocking", "அடேய்… முட்டாள் மனுஷங்களா! கொஞ்சம் கூட யோசிக்க மாட்டீங்களாடா?",
       "Hey… you foolish humans! Can't you think even a little?")],
     "liquid whooshing, bubbly pops as bacteria burst, playful villain swing music (pizzicato, tuba, finger snaps)"),
    ("The Boss mocks", 11, 6, ["BOSS"],
     "Same microscopic blood vessel; resistant bacteria gang behind the Boss; tiny enzyme 'scissors' snip antibiotic molecules near them.",
     "THE BOSS counts on his little arm, mocking humans; the gang laughs behind him.",
     "Medium shot on THE BOSS, slight handheld wobble for comedy.",
     [("BOSS", "sing-song, sarcastic", "தொண்டை வலிச்சா antibiotic! காய்ச்சல் வந்தா antibiotic! எதுக்குன்னே தெரியாம மாத்திரைய போட்டுக்கிறீங்க!",
       "Sore throat? Antibiotic! Fever? Antibiotic! You pop pills without even knowing why!")],
     "villain swing music, gang laughter"),
    ("Know-it-all bacterium", 12, 4, ["SMART"],
     "Same microscopic blood vessel.",
     "The SMART BACTERIUM steps forward and raises its little arm like a know-it-all student.",
     "Push-in to medium close-up.",
     [("SMART", "smug", "Antibiotics வைரஸுக்கு வேலை செய்யாதுன்னு உங்களுக்குத் தெரியாதா?",
       "Don't you know antibiotics don't work against viruses?")],
     "villain swing music, comic 'ding'"),
    ("Good bacteria harmed", 13, 5, ["BOSS"],
     "Same microscopic world, lower part of the vessel where friendly teal and green GOOD bacteria live.",
     "Antibiotic molecules hit the good bacteria; they wilt, turn grey and droop sadly. THE BOSS gestures at them mockingly.",
     "Slow pan across the good bacteria, ending on THE BOSS.",
     [("BOSS", "mocking", "உங்கள பாதுகாக்குற நல்ல bacteria-வையும் பாதிக்கிறீங்க!",
       "You even harm the good bacteria that protect you!")],
     "sad descending blips, villain swing music"),
    ("Survivors multiply", 14, 6, ["BOSS"],
     "Same microscopic world.",
     "The resistant bacteria split in two (binary fission), again and again, quickly filling the frame. THE BOSS gloats.",
     "Wide shot, slight zoom out as the numbers grow.",
     [("BOSS", "gloating", "எங்கள அழிச்சிட்டோம்னு நினைக்கிறீங்க… ஆனா எங்கள்ல சில பேரு உயிர் பொழச்சு பெருகுறோம்!",
       "You think you're destroying us… but some of us survive and multiply!")],
     "wet 'boop' sounds as cells split, villain music building"),
    ("Villain dance", 15, 7, ["BOSS"],
     "Same microscopic world, now crowded with resistant bacteria.",
     "The resistant gang high-fives and does a silly synchronised bouncing dance with squash-and-stretch; THE BOSS dances in the centre.",
     "Circling camera with a slight tilt, comic energy.",
     [("BOSS", "laughing, triumphant", "ஹா ஹா ஹா! எங்கள எதிர்க்குற மருந்து குறைஞ்சா… எங்க ஆட்டத்த யாருடா நிறுத்துவீங்க?",
       "Ha ha ha! When the medicines that fight us run out… who's going to stop our game?")],
     "upbeat villain dance music, high-five slaps"),
    ("The threat", 16, 5, ["BOSS"],
     "Same microscopic world; music stops, everything freezes, the light turns dark purple.",
     "THE BOSS slowly turns to the camera; his grin fades into a menacing look; eyes glint.",
     "Slow push-in to an extreme close-up of his face, lit from below.",
     [("BOSS", "slow, low, threatening whisper", "இதுதான் Antimicrobial Resistance! சில infections-க்கு மருந்தே வேலை செய்யலைன்னா… என்ன பண்ணுவீங்கடா?",
       "This is Antimicrobial Resistance! When medicines stop working for some infections… what will you do?")],
     "record scratch, then silence, then a low drone"),
    ("Black screen: narrator", 17, 5, ["NAR"],
     "The image fades to black; a faint red glow pulses with a heartbeat.",
     "Darkness, pulsing red vignette in time with the heartbeat.",
     "Static.",
     [("NAR", "serious, slow", "தேவையில்லாம antibiotics பயன்படுத்துறது, resistant bacteria உயிர் பொழச்சு பெருகுறதுக்கு வழிவகுக்கலாம்.",
       "Unnecessary antibiotic use allows resistant bacteria to survive and multiply.")],
     "heavy heartbeat, low boom"),
    ("Days later: hospital", 18, 6, ["S1", "MO", "DR"],
     "A wall calendar flips three days; then a modern Chennai hospital ward: clean beds, monitor, IV stand.",
     "STUDENT 1 lies weak and sweaty in a light-blue hospital gown. His MOTHER hurries to the CONSULTANT PHYSICIAN, hands clasped, pleading.",
     "Calendar insert, then a medium wide shot of the ward.",
     [("MO", "worried, breathless", "டாக்டர், காய்ச்சல் குறையவே இல்ல. இப்போ அவனுக்கு ரொம்ப முடியல!",
       "Doctor, the fever hasn't come down at all. He's really unwell now!")],
     "calendar pages flipping, hospital ambience, monitor beeps"),
    ("The physician reassures", 19, 7, ["S1", "MO", "DR"],
     "Same hospital ward.",
     "The CONSULTANT PHYSICIAN raises a calming hand, then examines STUDENT 1 with his stethoscope and checks his forehead.",
     "Medium two-shot, then over to the bedside.",
     [("DR", "calm, reassuring", "கவலைப்படாதீங்கம்மா. அவன செக் பண்ணி, தேவையான investigations பண்ணலாம். Infection எதனால வந்துச்சுன்னு கண்டுபிடிக்கறது முக்கியம்.",
       "Don't worry, amma. We'll examine him and do the necessary investigations. Finding the cause of the infection is important.")],
     "hospital ambience, monitor beeps"),
    ("Lab montage", 20, 4, [],
     "A modern hospital microbiology laboratory.",
     "Quick realistic montage: a nurse draws blood from an arm; blood goes into blood-culture bottles; a lab technician loads them into an incubator; bacterial colonies on an agar plate; an antibiotic susceptibility plate with small paper discs and clear zones.",
     "Quick cuts, about one second each, macro lens.",
     [],
     "lab hum, glass clinks, incubator door"),
    ("The culture report", 21, 5, ["MB"],
     "Hospital microbiology lab; a computer monitor shows an agar plate photo and a table of antibiotics marked R and S.",
     "The CONSULTANT MICROBIOLOGIST studies the report on screen and speaks, then picks up the printed report.",
     "Over-the-shoulder on the monitor, then medium on him.",
     [("MB", "clear, concerned", "Doctor, culture report-ல இந்த bacteria நிறைய antibiotics-க்கு resistant-ஆ இருக்கு.",
       "Doctor, the culture report shows this bacterium is resistant to many antibiotics.")],
     "keyboard clicks, lab hum"),
    ("Microbiologist meets physician", 22, 5, ["MB", "DR"],
     "The consultant physician's office.",
     "The CONSULTANT MICROBIOLOGIST walks in holding the printed report and shows it to the CONSULTANT PHYSICIAN.",
     "Walking shot into a medium two-shot.",
     [("MB", "clear, firm", "Susceptibility results-ஐ வச்சுதான் treatment-ஐ select பண்ணணும்.",
       "We must choose treatment based on the susceptibility results.")],
     "footsteps, paper rustle"),
    ("Deciding treatment", 23, 6, ["MB", "DR"],
     "Same office.",
     "Both doctors lean over the report together; the CONSULTANT PHYSICIAN nods and replies.",
     "Two-shot over the desk, slow push-in.",
     [("DR", "thoughtful, decisive", "சரி. Patient-ஓட clinical condition-உம் report-உம் பாத்து சரியான treatment முடிவு பண்ணலாம்.",
       "Alright. We'll decide the right treatment based on the patient's clinical condition and the report.")],
     "quiet office ambience"),
    ("Explaining to the mother", 24, 7, ["DR", "MO", "S1"],
     "Hospital ward bedside; STUDENT 1 resting in bed.",
     "The CONSULTANT PHYSICIAN explains gently to the MOTHER, using small hand gestures; she listens carefully.",
     "Medium shot favouring the physician, the mother in the foreground.",
     [("DR", "gentle, explaining", "Antibiotics எல்லா நோய்க்கும் தீர்வு இல்லம்மா. தொண்டை வலி, காய்ச்சல் வந்தாலே antibiotic வேணும்னு அர்த்தம் இல்ல.",
       "Antibiotics aren't the answer to every illness. A sore throat or fever doesn't mean you need an antibiotic.")],
     "soft hospital ambience"),
    ("Virus cutaway", 25, 6, ["DR"],
     "A simple animated insert: a cute spiky purple virus floating in a dark violet space.",
     "Glowing yellow antibiotic molecules fly at the virus and bounce off harmlessly; the virus smiles, unaffected. (The physician's voice continues over the insert.)",
     "Static centred shot with gentle drift.",
     [("DR", "gentle, explaining (voice-over)", "நிறைய infections வைரஸால தான் வருது; antibiotics வைரஸுக்கு வேலை செய்யாது.",
       "Many infections are caused by viruses; antibiotics don't work against viruses.")],
     "soft 'boing' bounces"),
    ("Bacteria resist, not people", 26, 7, ["MB", "DR", "MO"],
     "Hospital ward bedside.",
     "The CONSULTANT MICROBIOLOGIST joins and explains to the MOTHER. Cut briefly to an insert of blue bacteria bursting while red resistant bacteria survive.",
     "Medium shot of the microbiologist, quick insert, back to him.",
     [("MB", "clear, teacher-like", "Antimicrobial resistance-ங்கறது மனுஷங்களுக்கு வர்ற resistance இல்ல; bacteria தான் antibiotics-ஐ எதிர்க்குற சக்திய பெறுது.",
       "Antimicrobial resistance isn't resistance in humans; it's the bacteria that gain the ability to resist antibiotics.")],
     "soft hospital ambience"),
    ("Misuse makes it worse", 27, 5, ["MB"],
     "Insert of the printed laboratory report on a clipboard: rows of antibiotics marked R (red) and S (green); a doctor's pen ticks the effective ones. Then back to the microbiologist.",
     "The pen ticks the S rows; the microbiologist finishes his point.",
     "Close-up on the report, then medium close-up of the microbiologist.",
     [("MB", "serious", "தேவையில்லாத, தப்பான antibiotic பயன்பாடு இந்தப் பிரச்சனைய இன்னும் அதிகமாக்கலாம்.",
       "Unnecessary and incorrect antibiotic use can make this problem worse.")],
     "pen scratch, soft ambience"),
    ("Final message: physician", 28, 7, ["DR", "MB", "S1", "MO"],
     "A bright, clean hospital corridor. In the soft-focus background, through a ward doorway, STUDENT 1 sits up in bed on an IV drip, recovering, with his MOTHER beside him.",
     "Both doctors stand side by side looking straight into the camera; the CONSULTANT PHYSICIAN speaks warmly and confidently.",
     "Medium two-shot at eye level, slow push-in.",
     [("DR", "warm, confident", "டாக்டர் ஆலோசனை இல்லாம antibiotics எடுக்காதீங்க. குடுத்த dose-ஐயும் duration-ஐயும் முழுசா follow பண்ணுங்க.",
       "Don't take antibiotics without a doctor's advice. Follow the prescribed dose and duration fully.")],
     "soft hospital room tone, gentle inspiring music begins"),
    ("Final message: microbiologist", 29, 7, ["DR", "MB"],
     "Same bright hospital corridor.",
     "The CONSULTANT MICROBIOLOGIST speaks to the camera with conviction.",
     "Same set-up, slight reframe onto the microbiologist.",
     [("MB", "inspiring, sincere", "Antibiotics-ஐ பொறுப்பா use பண்றது நம்ம எல்லாரோட கடமை. இன்னைக்கும் நாளைக்கும் அது உயிர காப்பாத்தணும்.",
       "Using antibiotics responsibly is the duty of all of us. They must keep saving lives, today and tomorrow.")],
     "inspiring music rising"),
    ("Slogan", 30, 5, ["DR", "MB"],
     "Same corridor, light becoming brighter and warmer, gentle lens bloom.",
     "Both doctors say the slogan together, powerfully, looking into the camera. Leave clear empty space in the upper half of the frame for titles added in editing.",
     "Low-angle medium shot, slow push-in.",
     [("DR+MB", "together, powerful, in English", "Use antibiotics wisely. Stop antimicrobial resistance. Save our future!",
       "USE ANTIBIOTICS WISELY. STOP ANTIMICROBIAL RESISTANCE. SAVE OUR FUTURE!")],
     "cinematic impact hits on each phrase, inspiring orchestral swell"),
]


def voice_line(c):
    if c == "DR+MB":
        return "BOTH DOCTORS"
    return CHAR[c][0]


def prompt(clip):
    title, frame, keep, chars, setting, action, camera, dlg, audio = clip
    lines = [STYLE, "", f"Setting: {setting}"]
    if chars:
        lines.append("Characters (keep exactly this design):")
        for c in chars:
            n, look, _ = CHAR[c]
            lines.append(f"- {n}: {look}.")
    lines += [f"Action: {action}", f"Camera: {camera}"]
    if dlg:
        lines.append("Dialogue (spoken in Tamil, lip-synced):")
        for c, how, ta, _ in dlg:
            if c == "DR+MB":
                lines.append(f'- BOTH DOCTORS together ({how}): "{ta}"')
            else:
                lines.append(f'- {CHAR[c][0]} ({how}; voice: {CHAR[c][2]}): "{ta}"')
        lines.append(VOICE_RULE)
    else:
        lines.append("No dialogue.")
    lines += [f"Audio: {audio}.", NO_TEXT]
    return "\n".join(lines)


def main():
    out = []
    w = out.append
    w("# Gemini (Veo) prompts: 3D version with Chennai Tamil voices\n")
    w("These prompts remake *Use Antibiotics Wisely* as a **3D animated** film in **Gemini (Veo)**, using the rendered "
      "2D film ([`../AMR_Awareness_Film_1080p.mp4`](../AMR_Awareness_Film_1080p.mp4)) as the storyboard. The dialogue is "
      "rewritten in **natural colloquial Chennai Tamil**, with the same meaning and the same science as the original screenplay.\n")
    w("## Workflow\n")
    w("Veo makes clips of about **8 seconds**, so the film is split into **30 clips**. Each prompt below is self-contained: "
      "copy the whole grey block. Veo has no memory between clips, which is why the character and voice descriptions are repeated every time.\n")
    w("1. **Make the 3D character sheets once** (Gemini image generation). Upload `reference_frames/characters.png` and "
      "`reference_frames/microbes.png` and use the *Step 1* prompts. Save the results; they are your consistency references.")
    w("2. **For each clip, make a 3D start frame.** Upload `reference_frames/clipNN.png` together with the 3D character "
      "sheet and use the *Step 2* prompt. You get a 3D image with the same composition as the 2D film.")
    w("3. **Generate the clip** in Gemini video (Veo). Upload that 3D start frame as the starting image (or, in Google Flow, "
      "add the character sheets as reference *ingredients*) and paste the clip prompt. Generate 2–4 takes and keep the "
      "one with the best Tamil speech and lip-sync.")
    w("4. **Edit** (CapCut, Premiere, DaVinci Resolve or similar): put the clips in order and trim each to the *Keep* time. "
      "That adds up to about **2:55**, plus the 5-second end card = **3:00**. Then add the English subtitles listed under "
      "each clip, the phone-screen text (clip 3), the slogan titles (clip 30) and the end card. Details are under "
      "[Editing](#editing) at the end.\n")
    w("**Tips for natural Chennai Tamil voices**\n")
    w("- Keep the Tamil in Tamil script, exactly as written. If Veo mispronounces a line, regenerate; small wording changes "
      "(for example adding `டா` or `மச்சி`) often make delivery more natural.")
    w("- Veo picks a new voice each generation. Generate several takes and choose the ones closest to each character's voice description. "
      "For a perfectly consistent cast, have real Chennai Tamil speakers (friends, a college drama club) record the lines "
      "below on a phone, then replace the clip audio in the editor.")
    w("- If a line gets cut off at 8 seconds, use Veo's **Extend** option on that clip, or split the line across two generations.")
    w("- Every prompt asks for *no on-screen text*, because Veo garbles text. Add all text in the editor.\n")
    w("## Step 1: 3D character sheets (Gemini image generation)\n")
    w("Upload `reference_frames/characters.png`, then:\n")
    w("```\nRecreate these six characters as a high-end stylised 3D animated feature-film character lineup, full body, "
      "standing on a plain light-grey studio background, soft studio lighting. Keep every design detail exactly: faces, "
      "skin tones, hairstyles, glasses, beard, moustache, pottu, clothes and colours. Left to right: Student 1 (16, slim, "
      "neat side-parted hair, white school uniform, maroon-and-gold tie, navy backpack), Student 2 (16, chubby, curly hair, "
      "big grin, same uniform, loose tie, red backpack), Pharmacist (40, moustache, rectangular glasses, white coat over "
      "light-blue shirt), Mother (45, low bun, red pottu, maroon saree with gold border), Consultant Physician (52, "
      "salt-and-pepper hair, rimless glasses, white coat, navy tie, stethoscope, ID badge), Consultant Microbiologist (40, "
      "trimmed beard, square black glasses, white lab coat, grey shirt, blue lanyard badge). Appealing, expressive, "
      "realistic proportions slightly stylised. No text.\n```\n")
    w("Upload `reference_frames/microbes.png`, then:\n")
    w("```\nRecreate these microbes as glossy, high-end 3D animated characters on a dark crimson background, scientifically "
      "recognisable as bacteria (rod or round shapes, visible cell wall, pili, flagella) with simple cartoon faces: small "
      "friendly blue and green sensitive bacteria; friendly teal good bacteria with a gentle smile; larger crimson and "
      "purple resistant bacteria with a glowing capsule, spiky pili and mischievous villain faces; the Boss, the largest "
      "crimson-purple resistant bacterium with a golden whip-like flagellum and a jagged-tooth grin; glowing yellow "
      "amoxicillin molecules; a cute spiky purple virus. No text.\n```\n")
    w("## Step 2: 3D start frame for each clip\n")
    w("Upload `reference_frames/clipNN.png` and the 3D character sheet from Step 1, then:\n")
    w("```\nRecreate the first image as a single frame from a high-end stylised 3D animated feature film. Keep the same "
      "composition, camera angle, characters, poses and setting, but render everything in rich 3D with soft global "
      "illumination, detailed textures, realistic lighting and depth of field. The characters must match the 3D character "
      "sheet exactly. Remove all text, labels and captions. 16:9.\n```\n")
    w("## The 30 clip prompts\n")
    total = 0
    for i, clip in enumerate(CLIPS, 1):
        title, frame, keep, chars, setting, action, camera, dlg, audio = clip
        total += keep
        w(f"### Clip {i:02d}: {title}\n")
        w(f"Start frame: `reference_frames/clip{frame:02d}.png` · **Keep:** {keep} s (cumulative {total} s)\n")
        w("```\n" + prompt(clip) + "\n```\n")
        if dlg:
            w("English subtitles:\n")
            for c, how, ta, en in dlg:
                w(f"- {en}")
            w("")
    w("## Editing\n")
    w(f"- **Order and length:** clips 01–30 in order, each trimmed to its *Keep* time ({total} s), then the end card (5 s) for a total of {total + 5} s. "
      "Trim the dead air at the start and end of each clip rather than cutting speech.")
    w("- **End card:** reuse the last 5 seconds of the 2D film (`../AMR_Awareness_Film_1080p.mp4`, 02:55–03:00). It already has clean typography: "
      "*ANTIMICROBIAL RESISTANCE AWARENESS WEEK* / *“USE WISELY. PRESERVE THEIR POWER.”*")
    w("- **Clip 03 phone screen:** overlay the question bubble *“I have a sore throat and fever. What medicine should I take?”* "
      "and then the reply *“Do not self-medicate with antibiotics. Consult a healthcare professional.”* (you can screenshot `reference_frames/clip03.png`).")
    w("- **Clip 07:** add a small red tag *“No prescription asked!”* at the hand-over so the scene is not read as good practice.")
    w("- **Clip 30 titles:** bold white text, one line at a time on the beat: **USE ANTIBIOTICS WISELY.** / "
      "**STOP ANTIMICROBIAL RESISTANCE.** (yellow) / **SAVE OUR FUTURE!** (green).")
    w("- **Subtitles:** white sans-serif, bottom centre, on a semi-transparent dark box, timed to the speech. Use the English lines under each clip.")
    w("- **Music:** most prompts ask Veo for ambience and effects only, so the music doesn't jump between clips. Lay one "
      "music track per mood in the editor (playful for clips 1–9, comic villain for 10–15, dark for 16–17, soft piano for 18–27, "
      "inspiring for 28–30), kept well below the dialogue. If Veo adds music anyway, lower or mute it under the speech.")
    w("- **Captions in the 2D film:** to keep the teaching labels from the 2D film (*Sensitive bacteria*, *Good bacteria harmed too*, "
      "*Antibiotics do not work against viruses*, *Bacteria become resistant, not people*), add them as titles at the top of the frame on clips 10, 13, 25 and 26.\n")
    w("Regenerate this file with `python3 gemini/make_prompts.py`.")
    Path(__file__).with_name("GEMINI_PROMPTS.md").write_text("\n".join(out), encoding="utf-8")
    print(f"{len(CLIPS)} clips, {total} s + 5 s end card")


if __name__ == "__main__":
    main()
