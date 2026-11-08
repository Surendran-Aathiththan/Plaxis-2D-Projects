#!/usr/bin/env bash
# Build the complete film from scratch:
#   Tamil voices -> music + SFX -> animation -> final 180 s MP4 with subtitles.
# Needs: python3 with edge-tts, skia-python, numpy, scipy; ffmpeg with libass;
# libegl1 (for skia); network access to speech.platform.bing.com for the voices.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
python3 render/make_voices.py      # build/voices, audio/dialogue.wav, subtitles, build/timeline.json
python3 render/make_audio.py       # audio/music.wav, audio/sfx.wav
python3 render/render_scenes.py    # clips/scene1..7.mp4 (4 parallel workers)
./assemble_film.sh                 # output/AMR_Awareness_Film_1080p.mp4
