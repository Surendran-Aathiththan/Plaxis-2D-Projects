#!/usr/bin/env python3
"""Check the SRT: numbering, overlaps, cues crossing scene cuts, line length and reading speed."""
import re, sys
path = sys.argv[1] if len(sys.argv) > 1 else "subtitles/amr_film_en.srt"
CUTS = [0, 30, 45, 60, 95, 115, 155, 180]          # scene boundaries (s)
MAX_LINE, MAX_CPS = 50, 20
def sec(s): h, m, rest = s.split(":"); return int(h)*3600 + int(m)*60 + float(rest.replace(",", "."))
blocks = [b for b in open(path, encoding="utf-8").read().strip().split("\n\n")]
problems, prev_end = 0, 0.0
for n, b in enumerate(blocks, 1):
    lines = b.splitlines()
    a, z = (sec(x) for x in re.match(r"(\S+) --> (\S+)", lines[1]).groups())
    text = lines[2:]
    chars = sum(len(l) for l in text)
    cps = chars / (z - a)
    scene = next(i for i in range(7) if CUTS[i] <= a < CUTS[i+1]) + 1
    notes = []
    if int(lines[0]) != n: notes.append("bad number")
    if a < prev_end: notes.append("overlaps previous cue")
    if z > CUTS[scene]: notes.append(f"crosses cut at {CUTS[scene]}s")
    if any(len(l) > MAX_LINE for l in text): notes.append(f"line > {MAX_LINE} chars")
    if len(text) > 2: notes.append("more than 2 lines")
    if cps > MAX_CPS: notes.append(f"fast: {cps:.0f} chars/s")
    if notes:
        problems += 1
        print(f"#{n:>2} scene {scene} {a:7.2f}-{z:7.2f}  " + "; ".join(notes))
    prev_end = z
print(f"{len(blocks)} cues checked, {problems} flagged")
