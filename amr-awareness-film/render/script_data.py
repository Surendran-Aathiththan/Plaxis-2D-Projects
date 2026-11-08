"""Dialogue for the film, split into subtitle-sized segments.

Each segment is one English subtitle cue and the Tamil words spoken under it.
`t` is the target start time in seconds (from the shot list). The layout step
in make_voices.py keeps each segment as close to its target as the real audio
length allows, never letting a line cross into the next scene.
"""

SCENES = [  # (start, end) seconds
    (0, 30), (30, 45), (45, 60), (60, 100), (100, 115), (115, 155), (155, 180)
]

# speaker -> edge-tts voice settings (+ optional post-processing chain)
VOICES = {
    "s1":       dict(voice="ta-LK-KumarNeural",   rate="+18%", pitch="+14Hz"),
    "s2":       dict(voice="ta-SG-AnbuNeural",    rate="+22%", pitch="+20Hz"),
    "boss":     dict(voice="ta-MY-SuryaNeural",   rate="+22%", pitch="-12Hz",
                     fx="bass=g=4,aecho=0.8:0.6:35:0.25"),
    "smartbug": dict(voice="ta-SG-AnbuNeural",    rate="+25%", pitch="+48Hz"),
    "narrator": dict(voice="ta-IN-ValluvarNeural", rate="+8%", pitch="-14Hz",
                     fx="aecho=0.8:0.7:60|120:0.3|0.2"),
    "mother":   dict(voice="ta-LK-SaranyaNeural", rate="+15%", pitch="+0Hz"),
    "phys":     dict(voice="ta-IN-ValluvarNeural", rate="+16%", pitch="-4Hz"),
    "micro":    dict(voice="ta-LK-KumarNeural",   rate="+18%", pitch="-8Hz"),
    "phys_en":  dict(voice="en-IN-PrabhatNeural", rate="-5%", pitch="-6Hz"),
    "micro_en": dict(voice="en-GB-RyanNeural",    rate="-5%", pitch="-10Hz"),
}

# (id, scene, speaker, target_start, tamil, english_subtitle or None)
# A speaker of "both" plays phys_en + micro_en together.
SEGMENTS = [
    # ---------------- Scene 1: school ----------------
    ("s1a", 1, "s1", 5.2, "டேய் மச்சான், எனக்குத் தொண்டை ரொம்ப வலிக்குதுடா. காய்ச்சல் மாதிரியும் இருக்கு.",
     "Machan, my throat really hurts, da.\nFeels like a fever too."),
    ("s1b", 1, "s2", 10.1, "என்னடா ஆச்சு? டாக்டர்ட போகலாமா?",
     "What happened, da?\nShall we go to the doctor?"),
    ("s1c", 1, "s1", 12.8, "அதெல்லாம் வேண்டாம் டா. ChatGPT-ல கேட்டுப் பார்ப்போம்.",
     "No need for all that, da.\nLet's ask ChatGPT."),
    ("s1d", 1, "s2", 22.0, "டேய், எனக்கு முன்னாடி இப்படித்தான் இருந்தது. நான் Amoxicillin எடுத்தேன்.",
     "Da, I had the same thing before.\nI took Amoxicillin."),
    ("s1e", 1, "s2", 24.7, "நீயும் அதை எடுத்துக்கலாம் டா!",
     "You can take it too, da!"),
    ("s1f", 1, "s1", 27.2, "சரி டா! வா, Pharmacy-க்குப் போவோம்!",
     "OK da! Come, let's go to the pharmacy!"),
    # ---------------- Scene 2: cycling song ----------------
    ("s2a", 2, "s2", 31.2, "ஊசி போட உடம்பு இருந்தா…", "♪ If you've got a body for injections… ♪"),
    ("s2b", 2, "s2", 34.3, "டாக்டர்ட போக வேண்டாமா?", "♪ Do we really need to see a doctor? ♪"),
    ("s2c", 2, "s2", 37.4, "Pharmacy-க்கு சைக்கிள் ஓட்டி…", "♪ Let's cycle to the pharmacy… ♪"),
    ("s2d", 2, "s2", 40.5, "மாத்திரை வாங்கிப் போடலாமா?", "♪ Shall we just buy some pills and pop them? ♪"),
    ("s2e", 2, "s2", 43.4, "ஹா ஹா ஹா!", None),
    ("s2f", 2, "s1", 43.6, "ஹா ஹா!", None),
    # ---------------- Scene 3: pharmacy ----------------
    ("s3a", 3, "s1", 45.8, "அண்ணா, Amoxicillin இருக்கா? எனக்குத் தொண்டை வலியும் காய்ச்சலும் இருக்கு.",
     "Anna, do you have Amoxicillin?\nI have a sore throat and fever."),
    ("s3b", 3, "s2", 52.5, "பார்த்தியா டா! எவ்வளவு easy-ஆ மாத்திரை வாங்கிட்டோம்!",
     "See, da! We got the tablets so easily!"),
    ("s3c", 3, "s1", 55.0, "ஆமாடா! வா, வீட்டுக்குப் போவோம்!",
     "Yeah, da! Come, let's go home!"),
    # ---------------- Scene 4: inside the body ----------------
    ("s4a", 4, "boss", 62.6, "அடேய்… முட்டாள் மனுசங்களா! கொஞ்சமாவது யோசிக்க மாட்டீங்களாடா?",
     "Hey… you foolish humans!\nCan't you think even a little?"),
    ("s4b", 4, "boss", 67.3, "தொண்டை வலிச்சா antibiotic! காய்ச்சல் வந்தா antibiotic!",
     "Sore throat? Antibiotic!\nFever? Antibiotic!"),
    ("s4c", 4, "boss", 69.8, "எதுக்காக எடுத்துக்கிறீங்கன்னே தெரியாம மாத்திரையைப் போட்டுக்கிறீங்க!",
     "You pop pills without even knowing\nwhy you're taking them!"),
    ("s4d", 4, "smartbug", 72.5, "Antibiotics வைரஸுக்கு எதிராக வேலை செய்யாதுன்னு தெரியாதா உங்களுக்கு?",
     "Don't you know antibiotics\ndon't work against viruses?"),
    ("s4e", 4, "boss", 75.5, "உங்களைப் பாதுகாக்கிற நல்ல bacteria-களையும் பாதிக்கிறீங்க!",
     "You even harm the good bacteria\nthat protect you!"),
    ("s4f", 4, "boss", 78.0, "எங்களை அழிக்கிறோம்னு நினைக்கிறீங்க… ஆனா எங்களில் சிலர் உயிர்வாழ்ந்து பெருகுறோம்!",
     "You think you're destroying us…\nbut some of us survive and multiply!"),
    ("s4g", 4, "boss", 81.5, "ஹா ஹா ஹா! நாங்க உயிர்வாழ்ந்து பெருகுறோம்!",
     "Ha ha ha! We survive and multiply!"),
    ("s4h", 4, "boss", 83.3, "எங்களை எதிர்க்கிற மருந்துகள் குறையும்போது… எங்க ஆட்டத்தை யாரு நிறுத்தப் போறீங்கடா?",
     "When the medicines that can fight us run out…\nwho's going to stop our game, eh?"),
    ("s4i", 4, "boss", 87.5, "இதைத்தான் Antimicrobial Resistance-னு சொல்றீங்க!",
     "This is what you call\nAntimicrobial Resistance!"),
    ("s4j", 4, "boss", 89.3, "சில infections-க்கு மருந்து வேலை செய்யாத நிலை வந்தா, என்ன செய்வீங்கடா?",
     "When medicines stop working for some infections,\nwhat will you do?"),
    ("s4k", 4, "narrator", 91.9, "Antibiotics-ஐத் தேவையில்லாமல் பயன்படுத்துவது, resistant bacteria உயிர்வாழ்ந்து பெருகுவதற்கு வழிவகுக்கலாம்.",
     "Unnecessary antibiotic use allows\nresistant bacteria to survive and multiply."),
    # ---------------- Scene 5: hospital admission ----------------
    ("s5a", 5, "mother", 102.2, "டாக்டர், காய்ச்சல் குறையவே இல்லை. இப்போ ரொம்ப முடியாமல் இருக்கிறான்!",
     "Doctor, the fever hasn't come down at all.\nHe's really unwell now!"),
    ("s5b", 5, "phys", 105.0, "சரி, கவலைப்படாதீர்கள். நோயாளியைப் பரிசோதித்து, தேவையான investigations செய்வோம்.",
     "Alright, please don't worry. We'll examine him\nand do the necessary investigations."),
    ("s5c", 5, "phys", 109.5, "Infection-க்கான காரணத்தைக் கண்டறிவது முக்கியம்.",
     "Finding the cause of the infection\nis important."),
    # ---------------- Scene 6: physician + microbiologist ----------------
    ("s6a", 6, "micro", 117.6, "Doctor, culture report-ல் இந்த bacteria பல antibiotics-க்கு resistant-ஆக இருப்பது தெரிய வருகிறது.",
     "Doctor, the culture report shows this bacterium\nis resistant to many antibiotics."),
    ("s6b", 6, "micro", 122.1, "Susceptibility results அடிப்படையில் treatment தேர்ந்தெடுப்பது முக்கியம்.",
     "It's important to choose treatment\nbased on the susceptibility results."),
    ("s6c", 6, "phys", 125.7, "சரி. நோயாளியின் clinical condition மற்றும் report-ஐ வைத்து சரியான treatment-ஐத் தீர்மானிப்போம்.",
     "Alright. We'll decide the right treatment based on\nthe patient's clinical condition and the report."),
    ("s6d", 6, "phys", 131.0, "Antibiotics எல்லா நோய்களுக்கும் தீர்வல்ல.",
     "Antibiotics are not the answer\nto every illness."),
    ("s6e", 6, "phys", 133.5, "தொண்டை வலி, காய்ச்சல் வந்தாலே antibiotic தேவை என்று அர்த்தமில்லை.",
     "A sore throat or fever doesn't mean\nyou automatically need an antibiotic."),
    ("s6f", 6, "phys", 137.0, "பல infections வைரஸ்களால் ஏற்படுகின்றன; antibiotics வைரஸ்களுக்கு எதிராக வேலை செய்யாது.",
     "Many infections are caused by viruses;\nantibiotics don't work against viruses."),
    ("s6g", 6, "micro", 142.5, "Antimicrobial resistance என்பது மனிதர்களுக்கு ஏற்படும் resistance அல்ல;",
     "Antimicrobial resistance is not resistance\nthat develops in humans;"),
    ("s6h", 6, "micro", 145.8, "bacteria-கள்தான் antibiotics-ஐ எதிர்க்கும் திறனைப் பெறுகின்றன.",
     "it's the bacteria that gain\nthe ability to resist antibiotics."),
    ("s6i", 6, "micro", 149.3, "தேவையற்ற மற்றும் தவறான antibiotic பயன்பாடு இந்தப் பிரச்சினையை அதிகரிக்கலாம்.",
     "Unnecessary and incorrect antibiotic use\ncan make this problem worse."),
    # ---------------- Scene 7: final message ----------------
    ("s7a", 7, "phys", 156.4, "மருத்துவரின் ஆலோசனையின்றி antibiotics எடுத்துக்கொள்ளாதீர்கள்.",
     "Don't take antibiotics\nwithout a doctor's advice."),
    ("s7b", 7, "phys", 159.6, "பரிந்துரைக்கப்பட்ட dose மற்றும் duration-ஐப் பின்பற்றுங்கள்.",
     "Follow the prescribed dose and duration."),
    ("s7c", 7, "micro", 162.6, "Antibiotics-ஐப் பொறுப்புடன் பயன்படுத்துவது நம் அனைவரின் கடமை.",
     "Using antibiotics responsibly\nis the duty of every one of us."),
    ("s7d", 7, "micro", 165.6, "அவை இன்றும் நாளையும் உயிர்களைக் காப்பாற்ற உதவ வேண்டும்.",
     "They must keep helping to save lives,\ntoday and tomorrow."),
    ("s7e", 7, "both", 169.6, "Use antibiotics wisely. Stop antimicrobial resistance. Save our future!",
     "USE ANTIBIOTICS WISELY.\nSTOP ANTIMICROBIAL RESISTANCE. SAVE OUR FUTURE!"),
]

# Latest time (scene-relative end) dialogue may run to in each scene, leaving
# room for transitions / end card.
SCENE_DIALOGUE_LIMIT = {1: 29.4, 2: 44.8, 3: 57.6, 4: 99.6, 5: 114.6, 6: 154.6, 7: 175.0}

# Layout: scene 2 (the song) keeps its target times on the beat. All other
# scenes start at their first segment's target, then pack lines with natural
# gaps; PREPAUSE adds a hold before a line where the picture needs time.
TARGET_SCENES = {2}
PREPAUSE = {"s1d": 4.6, "s3b": 1.6, "s4d": 0.3, "s4g": 0.2, "s4i": 0.8, "s4k": 0.5,
            "s5b": 0.2, "s6c": 0.3, "s6d": 1.0, "s6g": 0.6, "s7c": 0.3, "s7e": 0.6}
