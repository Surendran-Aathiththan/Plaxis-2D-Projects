"""Shared timing: dialogue segments from build/timeline.json plus key story
beats derived from them, so picture, music and sound effects stay in sync."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FPS = 25
SCENES = [(0, 30), (30, 45), (45, 60), (60, 100), (100, 115), (115, 155), (155, 180)]

_TL = json.loads((ROOT / "build" / "timeline.json").read_text())
SEG = {s["id"]: s for s in _TL}


def seg(i):
    return SEG[i]


def talking(speaker, t, ids=None):
    """Mouth-open amount 0..1 for a speaker at film time t (from audio RMS)."""
    for s in _TL:
        if (s["speaker"] == speaker or (s["speaker"] == "both" and speaker in ("phys", "micro"))) \
                and s["start"] <= t < s["end"] and (ids is None or s["id"] in ids):
            k = int((t - s["start"]) * FPS)
            env = s["env"]
            return env[k] if k < len(env) else 0.0
    return 0.0


def is_speaking(speaker, t, pad=0.0):
    return any((s["speaker"] == speaker) and s["start"] - pad <= t < s["end"] + pad for s in _TL)


S = SEG
# ---- story beats (film seconds) ----
BEAT = {}
BEAT["phone_type"] = S["s1c"]["end"] + 0.25
BEAT["phone_reply"] = BEAT["phone_type"] + 2.4
BEAT["phone_zoom"] = S["s1f"]["end"] - 0.1
BEAT["bell1"], BEAT["bell2"] = 38.2, 38.55
BEAT["laugh"] = S["s2e"]["start"]
BEAT["handover"] = S["s3a"]["end"] + 0.25
BEAT["leave"] = S["s3c"]["end"] + 0.1
BEAT["swallow"] = BEAT["leave"] + 0.9
BEAT["dive"] = 59.0
BEAT["boss_reveal"] = S["s4a"]["start"] - 0.4
BEAT["smartbug"] = S["s4d"]["start"] - 0.3
BEAT["good_hit"] = S["s4e"]["start"]
BEAT["divide"] = S["s4f"]["start"]
BEAT["dance"] = S["s4g"]["start"]
BEAT["music_stop"] = S["s4i"]["start"] - 0.75
BEAT["black"] = S["s4k"]["start"] - 0.25
BEAT["calendar_end"] = 102.0
BEAT["ward"] = S["s5a"]["start"] + 1.2
BEAT["exam"] = S["s5b"]["start"] + 0.8
BEAT["lab_montage"] = S["s5c"]["start"]
BEAT["micro_walk"] = S["s6a"]["start"] + 2.2
BEAT["review"] = S["s6c"]["start"]
BEAT["family"] = S["s6d"]["start"] - 0.6
BEAT["virus_cut"] = S["s6f"]["start"]
BEAT["micro_explain"] = S["s6g"]["start"] - 0.3
BEAT["bact_cut"] = S["s6h"]["start"]
BEAT["report_cut"] = S["s6i"]["start"]
BEAT["slogan"] = S["s7e"]["start"]
BEAT["endcard"] = 175.0
