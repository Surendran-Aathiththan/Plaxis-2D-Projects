#!/usr/bin/env bash
# Assemble the seven scene clips into one 180-second, 1920x1080 film with
# burned-in English subtitles and a mixed, loudness-normalised soundtrack.
#
# Usage:
#   ./assemble_film.sh [CLIPS_DIR] [OUTPUT_FILE]
#
# Inputs (relative to this script's folder unless given):
#   CLIPS_DIR/scene1.(mp4|mov|mkv) ... scene7.(mp4|mov|mkv)   required
#   audio/dialogue.wav   optional, full 180 s Tamil dialogue + narrator stem
#   audio/music.wav      optional, full 180 s music stem (ducked under dialogue)
#   audio/sfx.wav        optional, full 180 s sound-effects stem
#   subtitles/amr_film_en.srt                                  required
#
# Each clip is scaled/padded to 1920x1080, converted to 25 fps, and trimmed or
# extended (last frame held) to its exact scene length, so a clip that comes
# back from a video generator slightly short or long never shifts the
# subtitles that follow it. Audio inside a clip is kept (e.g. a lip-synced
# take); if a clip has no audio, silence is used.

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

CLIPS_DIR="${1:-clips}"
OUT="${2:-output/AMR_Awareness_Film_1080p.mp4}"
SRT="subtitles/amr_film_en.srt"
WORK="output/.work"

# Scene lengths in seconds (00:00-00:30, 00:30-00:45, ... 02:35-03:00).
DUR=(30 15 15 35 20 40 25)
TOTAL=180
FPS=25

# Subtitle look: white sans-serif, bottom centre, semi-transparent dark box.
# (libass draws the BorderStyle=3 box in OutlineColour; &H80 = ~50% alpha.)
SUB_STYLE="FontName=Arial,FontSize=18,PrimaryColour=&H00FFFFFF,OutlineColour=&H80000000,BackColour=&H00000000,BorderStyle=3,Outline=1.2,Shadow=0,Alignment=2,MarginV=18,Bold=0"

command -v ffmpeg >/dev/null || { echo "ffmpeg is required" >&2; exit 1; }
[[ -f "$SRT" ]] || { echo "Missing $SRT" >&2; exit 1; }
mkdir -p "$WORK" "$(dirname "$OUT")"

has_audio() {
  [[ -n "$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$1")" ]]
}
duration_of() {
  ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$1"
}

: > "$WORK/list.txt"
for i in 1 2 3 4 5 6 7; do
  d=${DUR[$((i-1))]}
  src=""
  for ext in mp4 mov mkv; do
    [[ -f "$CLIPS_DIR/scene$i.$ext" ]] && { src="$CLIPS_DIR/scene$i.$ext"; break; }
  done
  [[ -n "$src" ]] || { echo "Missing $CLIPS_DIR/scene$i.(mp4|mov|mkv)" >&2; exit 1; }

  actual=$(duration_of "$src")
  diff=$(awk -v a="$actual" -v t="$d" 'BEGIN{x=a-t; if(x<0)x=-x; print (x>0.5)?1:0}')
  if [[ "$diff" == 1 ]]; then
    echo "WARNING: scene$i is ${actual}s, target ${d}s; it will be trimmed or its last frame held." >&2
  fi

  vf="scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,fps=$FPS,format=yuv420p,tpad=stop_mode=clone:stop_duration=$d,trim=duration=$d,setpts=PTS-STARTPTS"
  if has_audio "$src"; then
    af="[0:a]aresample=48000,aformat=channel_layouts=stereo,apad,atrim=duration=$d,asetpts=PTS-STARTPTS[a]"
    ffmpeg -v error -y -i "$src" \
      -filter_complex "[0:v]$vf[v];$af" -map "[v]" -map "[a]" \
      -c:v libx264 -preset fast -crf 14 -c:a pcm_s16le -t "$d" "$WORK/s$i.mkv"
  else
    ffmpeg -v error -y -i "$src" -f lavfi -t "$d" -i anullsrc=r=48000:cl=stereo \
      -filter_complex "[0:v]$vf[v]" -map "[v]" -map 1:a \
      -c:v libx264 -preset fast -crf 14 -c:a pcm_s16le -t "$d" "$WORK/s$i.mkv"
  fi
  echo "file 's$i.mkv'" >> "$WORK/list.txt"
  echo "scene$i ready (${d}s)"
done

ffmpeg -v error -y -f concat -safe 0 -i "$WORK/list.txt" -c copy "$WORK/joined.mkv"

# ---- Audio mix -------------------------------------------------------------
inputs=(-i "$WORK/joined.mkv")
labels="[0:a]"
n=1
filter=""
dlg_idx=""
if [[ -f audio/dialogue.wav ]]; then
  inputs+=(-i audio/dialogue.wav); dlg_idx=$n
  filter+="[$n:a]aresample=48000,aformat=channel_layouts=stereo,apad,atrim=duration=$TOTAL,asplit=2[dlg][dlgkey];"
  labels+="[dlg]"; n=$((n+1))
fi
if [[ -f audio/music.wav ]]; then
  inputs+=(-i audio/music.wav)
  filter+="[$n:a]aresample=48000,aformat=channel_layouts=stereo,apad,atrim=duration=$TOTAL[mus0];"
  if [[ -n "$dlg_idx" ]]; then
    # Duck music by up to ~12 dB whenever someone speaks.
    filter+="[mus0][dlgkey]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=450:makeup=1[mus];"
  else
    filter+="[mus0]anull[mus];"
  fi
  labels+="[mus]"; n=$((n+1))
elif [[ -n "$dlg_idx" ]]; then
  filter+="[dlgkey]anullsink;"
fi
if [[ -f audio/sfx.wav ]]; then
  inputs+=(-i audio/sfx.wav)
  filter+="[$n:a]aresample=48000,aformat=channel_layouts=stereo,apad,atrim=duration=$TOTAL[sfx];"
  labels+="[sfx]"; n=$((n+1))
fi
filter+="${labels}amix=inputs=$n:normalize=0:duration=first,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[aout]"
echo "Mixing $n audio source(s)"

# ---- Final encode with burned-in subtitles ---------------------------------
filter="[0:v]subtitles=filename=$SRT:force_style='$SUB_STYLE'[vout];$filter"
ffmpeg -v error -y "${inputs[@]}" -filter_complex "$filter" \
  -map "[vout]" -map "[aout]" -t "$TOTAL" \
  -c:v libx264 -preset slow -crf 18 -profile:v high -pix_fmt yuv420p -r $FPS \
  -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$OUT"

final=$(duration_of "$OUT")
res=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 "$OUT")
echo "Done: $OUT  (${final}s, ${res})"
awk -v f="$final" -v t="$TOTAL" 'BEGIN{x=f-t; if(x<0)x=-x; exit (x>0.1)}' \
  || { echo "ERROR: output is ${final}s, expected ${TOTAL}s" >&2; exit 1; }
