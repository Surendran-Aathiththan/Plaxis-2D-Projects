# Use Antibiotics Wisely: AMR awareness short film

A 3-minute (180 s), 1920×1080 animated educational short for **Antimicrobial Resistance Awareness Week**, with Sri Lankan Tamil dialogue and English subtitles.

**Rendered film:** [`AMR_Awareness_Film_1080p.mp4`](AMR_Awareness_Film_1080p.mp4). It is 180 s, 1920×1080, 25 fps, H.264 video with AAC stereo audio at 48 kHz, loudness −15.5 LUFS. It is a complete **2D animated** version of the film, generated entirely by code in [`render/`](render):

- **Picture:** vector cartoon animation (skia), with characters that blink, gesture, walk and cycle. Mouths are driven by the loudness of the Tamil audio, so lip movement follows the speech.
- **Voices:** every Tamil line from the screenplay, spoken by Microsoft neural Tamil voices: Sri Lankan (ta-LK Kumar, Saranya), Indian, Malaysian and Singaporean Tamil. Each character has its own voice and pitch. The final slogan is in English, as in the screenplay.
- **Subtitles:** 41 English cues, burned in, timed to the real audio.
- **Music and sound effects:** synthesised to the cue sheets (playful → villain swing → hospital piano → inspiring finale), with music ducked under the dialogue.

This is not the 3D film with human voice actors described in the brief. Producing that still needs a 3D animation or video-generation tool and real voice actors. The shot list, production bible and assembly script below are the kit for it, and the rendered film works as a full-length animatic or as a usable awareness video in its own right.

Rebuild everything from scratch with `./build_film.sh`. It takes about 8 minutes on 4 CPU cores and needs `pip install -r render/requirements.txt`, ffmpeg, libegl1, and network access to `speech.platform.bing.com` for the voices.

| File | What it is |
|---|---|
| [SHOT_LIST.md](SHOT_LIST.md) | 35 timed shots across the 7 scenes: camera, action, a ready-to-paste generation prompt, and every Tamil line with its exact time slot and English subtitle |
| [PRODUCTION_BIBLE.md](PRODUCTION_BIBLE.md) | Locked character and style descriptions for consistency, the science lock for the microscopic scene, voice casting, music cue sheet and SFX cue sheet |
| [subtitles/amr_film_en.srt](subtitles/amr_film_en.srt) | 41 synchronised English subtitle cues, the timing master for the whole film |
| [assemble_film.sh](assemble_film.sh) | Joins the 7 scene clips into the final 180 s film, mixes the audio stems (music ducked under dialogue, loudness normalised to −16 LUFS) and burns in the subtitles |
| [tools/check_subtitles.py](tools/check_subtitles.py) | Checks the subtitles for overlaps, cues crossing scene cuts, line length and reading speed |
| [tools/make_test_clips.sh](tools/make_test_clips.sh) | Makes placeholder clips and test audio to dry-run the assembly |
| [build_film.sh](build_film.sh) | Builds the rendered film end to end |
| `render/script_data.py` | All dialogue (Tamil + English) split into subtitle-sized segments, voice casting per character |
| `render/make_voices.py` | Tamil speech synthesis, fits lines into scene timing, writes the dialogue stem, the subtitles and the lip-sync timeline |
| `render/make_audio.py` | Music and sound-effects synthesis |
| `render/characters.py`, `render/microbes.py` | Character rig and microscopic cast |
| `render/scenes_a.py`, `render/scenes_b.py`, `render/scenes_c.py` | Scenes 1–3, Scene 4, Scenes 5–7 |
| `render/render_scenes.py` | Renders `clips/scene1..7.mp4` in parallel (`--still T out.png` renders one frame) |

## Scene map

| # | Scene | Time | Length |
|---|---|---|---|
| 1 | School: the beginning | 00:00–00:30 | 30 s |
| 2 | Cycling to the pharmacy | 00:30–00:45 | 15 s |
| 3 | Pharmacy | 00:45–01:00 | 15 s |
| 4 | Inside the body: the bacteria strike back | 01:00–01:40 | 40 s |
| 5 | Hospital admission | 01:40–01:55 | 15 s |
| 6 | Consultant physician and consultant microbiologist | 01:55–02:35 | 40 s |
| 7 | The final message and end card | 02:35–03:00 | 25 s |

## Production workflow

1. **Lock the look.** Make one reference image per character from the locked descriptions in the production bible (front, three-quarter and side views) and one style frame per act. Reuse them for every shot.
2. **Record the voices first.** Record every Tamil line into its slot in the shot list (read the matching subtitle timings while recording). Export one continuous 180 s `audio/dialogue.wav` with each line placed at its timecode, and keep each line as a separate file for lip-sync.
3. **Generate the shots.** Work through the shot list with your video tool. For talking shots, generate the performance and then run a lip-sync pass with that shot's recorded line, so mouths match the Tamil audio.
4. **Edit each scene** to its exact length and export `clips/scene1.mp4` … `clips/scene7.mp4`. If you lip-synced in the clip, its audio can stay embedded. Otherwise leave the clips silent and rely on the stems.
5. **Music and SFX.** Build `audio/music.wav` and `audio/sfx.wav` (both 180 s) from the cue sheets.
6. **Assemble:**

   ```bash
   ./assemble_film.sh            # reads clips/ and audio/, writes output/AMR_Awareness_Film_1080p.mp4
   ```

   Each clip is scaled and padded to 1920×1080 at 25 fps and trimmed (or its last frame held) to the exact scene length. A clip that comes back a little short or long therefore never pushes the later subtitles out of sync. The script warns when a clip is off by more than 0.5 s and fails if the output is not 180 s.

7. For YouTube or other platforms, upload `subtitles/amr_film_en.srt` as a caption track as well as the burned-in version.

Requires `ffmpeg` built with libass (standard on Ubuntu and Homebrew builds).

### Dry run

```bash
tools/make_test_clips.sh /tmp/amr_test --stems    # placeholder clips + beep "dialogue" on every subtitle cue
./assemble_film.sh /tmp/amr_test /tmp/amr_test/film.mp4
rm -r audio                                        # remove the test stems before adding real ones
```

This was run on the kit. The output was 180.000 s, 1920×1080, 25 fps, H.264/AAC 48 kHz stereo at −15.8 LUFS integrated. Scene cuts landed on 30/45/60/95/115/155 s, and the short Scene 5 test clip was correctly held to 20 s.

Scenes 4 and 5 use option A below. The scripted Scene 4 dialogue is about 42 s of natural Tamil speech, which cannot fit in 35 s, so Scene 4 runs 01:00–01:40 and Scene 5 runs 01:40–01:55. Every other boundary matches the brief. The times in SHOT_LIST.md are the original plan. `subtitles/amr_film_en.srt` holds the timing actually used in the rendered film.

## Timing pressure (decide before recording)

`tools/check_subtitles.py` flags 11 of 41 cues as reading faster than 20 characters per second, almost all in **Scene 4** (about 31 s of dialogue in 35 s) and the long doctor explanations in **Scene 6**. Keeping the brief's exact timestamps works only if those lines are delivered briskly. If the recorded takes run long, pick one option:

- **A (keeps the dialogue word for word):** move 5 s from Scene 5 to Scene 4 (Scene 4 01:00–01:40, Scene 5 01:40–01:55) by shortening the calendar and lab montage, then shift the subtitle times to match.
- **B (keeps the timestamps):** tighten a few Scene 4 lines in the Tamil script itself.

## Script and science review notes

The supplied dialogue is scientifically sound. A few points were handled in the visuals, or need a decision from you:

- **Selection, not decision.** Resistant bacteria are shown already present in small numbers before the tablet. The antibiotic kills the sensitive ones and the resistant few multiply. Amoxicillin is drawn as beta-lactam-ring molecules that burst sensitive cells (cell-wall damage), while resistant cells survive via enzyme "scissors" (beta-lactamase). Both are accurate, simplified mechanisms.
- **Virus cutaway (Scene 6):** antibiotic molecules bounce off a virus, which supports "antibiotics don't work against viruses".
- **"Parents" in Scene 6:** only the mother is designed, so the physician speaks to the mother. Add a father character to the bible if you want both parents.
- **Narrator subtitle:** the Tamil says *"…can lead to resistant bacteria surviving and multiplying"* (வழிவகுக்கலாம்). The subtitle uses your requested wording, *"…allows resistant bacteria to survive and multiply."* Both are accurate.
- **Song lines (Scene 2):** the subtitles follow the joking, rhetorical sense of the lyrics ("Do we really need to see a doctor?").
- **Brand name:** the dialogue says "ChatGPT", as scripted, but the phone screen is drawn as a generic chat app with no logo, to avoid trademark issues in a public campaign. Replace the word with "AI-ல" if you want the film fully brand-free.
- **Pharmacy scene:** dispensing without a prescription is shown with a darker light change and an ominous music sting, so it doesn't read as recommended practice.
- **Final slogan:** it is spoken in English, as in the screenplay. The on-screen typography and the subtitle carry the same words.

Working folders (`clips/`, `audio/`, `output/`, `build/`) are git-ignored. Only the finished film is committed.
