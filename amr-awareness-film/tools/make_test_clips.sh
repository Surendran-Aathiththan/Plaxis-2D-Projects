#!/usr/bin/env bash
# Make labelled placeholder clips (and optional test audio stems) to dry-run
# assemble_film.sh before the real animation exists. Sizes, frame rates and
# lengths are deliberately a little wrong to exercise the normaliser.
# Usage: tools/make_test_clips.sh OUT_DIR [--stems]
set -euo pipefail
OUT="${1:?output folder}"; mkdir -p "$OUT"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
names=("1 School" "2 Cycling to the pharmacy" "3 Pharmacy" "4 Inside the body" "5 Hospital admission" "6 Physician + Microbiologist" "7 Final message")
durs=(29.6 15.4 15 35 18.5 40 25)          # scene 5 short on purpose
sizes=(1920x1080 1280x720 1920x1080 1920x816 1920x1080 1440x1080 1920x1080)
fps=(24 30 25 24 25 30 24)
cols=(0x2e7d32 0x1565c0 0x6a1b9a 0xb71c1c 0x37474f 0x00695c 0xf9a825)
for i in 0 1 2 3 4 5 6; do
  ffmpeg -v error -y -f lavfi -i "color=c=${cols[$i]}:s=${sizes[$i]}:r=${fps[$i]}:d=${durs[$i]}" \
    -vf "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='SCENE ${names[$i]}':fontcolor=white:fontsize=h/12:x=(w-tw)/2:y=h/3,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf:text='%{pts\:hms}':fontcolor=white:fontsize=h/18:x=(w-tw)/2:y=h/2" \
    -c:v libx264 -preset ultrafast -pix_fmt yuv420p "$OUT/scene$((i+1)).mp4"
done
if [[ "${2:-}" == "--stems" ]]; then
  mkdir -p "$HERE/audio"
  # "Dialogue": 1 kHz beeps during every subtitle cue, so sync can be eyeballed.
  expr=$(python3 - "$HERE/subtitles/amr_film_en.srt" <<'PY'
import re,sys
t=lambda s:sum(float(x)*m for x,m in zip(s.replace(',','.').split(':'),(3600,60,1)))
cues=re.findall(r'(\d\d:\d\d:\d\d,\d+) --> (\d\d:\d\d:\d\d,\d+)',open(sys.argv[1]).read())
print('+'.join(f'between(t,{t(a):.2f},{t(b):.2f})' for a,b in cues))
PY
)
  ffmpeg -v error -y -f lavfi -i "aevalsrc='0.3*sin(2*PI*1000*t)*($expr)':s=48000:d=180" -ac 2 "$HERE/audio/dialogue.wav"
  ffmpeg -v error -y -f lavfi -i "aevalsrc='0.25*sin(2*PI*220*t)':s=48000:d=180" -ac 2 "$HERE/audio/music.wav"
  echo "Test stems written to $HERE/audio/ (delete before adding real stems)"
fi
echo "Placeholder clips written to $OUT"
