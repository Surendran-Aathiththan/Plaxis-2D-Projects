#!/usr/bin/env python3
"""Synthesise the music stem (audio/music.wav) and the sound-effects stem
(audio/sfx.wav), timed to the same story beats as the picture."""
import math, sys, wave
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from timing import S, BEAT, ROOT

SR, TOTAL = 48000, 180
rng = np.random.default_rng(7)


def buf():
    return np.zeros(SR * TOTAL + SR, np.float32)


def place(b, t, sig, gain=1.0):
    i = int(t * SR)
    if i < 0 or i >= len(b):
        return
    n = min(len(sig), len(b) - i)
    b[i:i + n] += sig[:n] * gain


def tt(d):
    return np.arange(int(d * SR)) / SR


def hz(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def env(d, a=0.005, r=0.05, dec=None):
    t = tt(d)
    e = np.minimum(1, t / max(a, 1e-4))
    if dec:
        e *= np.exp(-t * dec)
    rel = np.clip((d - t) / max(r, 1e-4), 0, 1)
    return e * rel


# ---------- instruments ----------
def marimba(n, d=0.5):
    f, t = hz(n), tt(d)
    return (np.sin(2 * np.pi * f * t) * np.exp(-t * 7) + 0.35 * np.sin(2 * np.pi * f * 3.93 * t) * np.exp(-t * 22)) * env(d, 0.002)


def pluck(n, d=0.4, dec=9):
    f, t = hz(n), tt(d)
    s = sum(np.sin(2 * np.pi * f * k * t) * np.exp(-t * dec * k) / k for k in range(1, 6))
    return s * env(d, 0.002) * 0.7


def piano(n, d=1.6):
    f, t = hz(n), tt(d)
    s = sum(np.sin(2 * np.pi * f * k * (1 + 0.0004 * k * k) * t) * np.exp(-t * (1.2 + k * 0.9)) / (k ** 1.3) for k in range(1, 8))
    return s * env(d, 0.003, 0.2) * 0.6


def pad(n, d, a=0.6, r=0.8, bright=4):
    f, t = hz(n), tt(d)
    s = np.zeros_like(t)
    for det in (-0.004, 0.0, 0.005):
        s += sum(np.sin(2 * np.pi * f * (1 + det) * k * t + k) / k for k in range(1, bright + 1))
    return s * env(d, a, r) * 0.12


def bass(n, d=0.4):
    f, t = hz(n), tt(d)
    return (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)) * env(d, 0.005, 0.06, dec=2.5) * 0.8


def tuba(n, d=0.35):
    f, t = hz(n), tt(d)
    s = sum(np.sin(2 * np.pi * f * k * t) * (0.8 ** k) for k in range(1, 7))
    return s * env(d, 0.03, 0.08, dec=2) * 0.45


def whistle(n, d=0.4, slide=0):
    t = tt(d)
    f = hz(n) * (1 + 0.012 * np.sin(2 * np.pi * 5.5 * t)) * (2 ** (slide * t / d / 12))
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * env(d, 0.04, 0.08) * 0.35


def noise(d):
    return rng.standard_normal(int(d * SR)).astype(np.float32)


def hp(x, k=0.95):
    y = np.empty_like(x)
    prev_x = prev_y = 0.0
    y = x - np.concatenate(([0], x[:-1])) * k
    return y


def lp(x, a=0.1):
    # one-pole low-pass via cumulative trick (vectorised approximation)
    out = np.empty_like(x)
    acc = 0.0
    from scipy.signal import lfilter  # type: ignore
    return lfilter([a], [1, -(1 - a)], x).astype(np.float32)


def kick(d=0.35):
    t = tt(d)
    f = 50 + 90 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9) * 0.9


def clap(d=0.18):
    return lp(hp(noise(d)), 0.5) * env(d, 0.001, 0.02, dec=28) * 0.5


def hat(d=0.06):
    return hp(noise(d), 0.99) * env(d, 0.001, 0.01, dec=60) * 0.18


def shaker(d=0.09):
    return hp(noise(d), 0.97) * env(d, 0.02, 0.03) * 0.1


def snap(d=0.08):
    return hp(noise(d), 0.9) * env(d, 0.0005, 0.01, dec=80) * 0.45


def tabla(n, d=0.3):
    t = tt(d)
    f = hz(n) * (1 + 0.25 * np.exp(-t * 25))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 11) * 0.5


def timpani(n, d=1.6):
    t = tt(d)
    f = hz(n)
    return (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 1.5 * t)) * np.exp(-t * 2.2) * env(d, 0.004) * 0.7


def bell(f, d=1.2):
    t = tt(d)
    s = sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t * dd) for m, a, dd in ((1, 1, 3), (2.76, 0.5, 5), (5.4, 0.3, 8), (8.9, 0.15, 12)))
    return s * env(d, 0.001) * 0.5


CH = {"C": [48, 52, 55], "Am": [45, 48, 52], "F": [41, 45, 48], "G": [43, 47, 50], "Dm": [50, 53, 57],
      "Bb": [46, 50, 53], "A": [45, 49, 52], "Em": [40, 43, 47], "Gm": [43, 46, 50]}


def music():
    m = buf()
    # ---- M1 school: playful marimba, C Am F G at 110 bpm ----
    beat = 60 / 110
    end1 = BEAT["phone_zoom"]
    prog = ["C", "Am", "F", "G"]
    t = 0.3
    bar = 0
    while t < end1:
        ch = CH[prog[bar % 4]]
        for i in range(8):
            tn = t + i * beat / 2
            if tn >= end1:
                break
            n = ch[[0, 1, 2, 1, 0, 2, 1, 2][i]] + 24
            place(m, tn, marimba(n, 0.4), 0.22)
            place(m, tn, shaker(), 0.6 if i % 2 else 0.3)
        place(m, t, bass(ch[0] - 12, beat * 1.8), 0.35)
        place(m, t + 2 * beat, bass(ch[2] - 12, beat * 1.8), 0.3)
        if bar % 2 == 1:
            place(m, t + 3.5 * beat, tabla(62), 0.4)
            place(m, t + 3.75 * beat, tabla(67), 0.35)
        t += 4 * beat
        bar += 1
    # comic "uh-oh" as Student 2 waves the warning away
    place(m, S["s1d"]["start"] - 0.5, whistle(79, 0.25), 0.5)
    place(m, S["s1d"]["start"] - 0.25, whistle(76, 0.4, slide=-2), 0.5)
    # ---- M2 cycle song: bouncy, bars aligned to the sung lines ----
    barlen = 1.55
    origin = S["s2a"]["start"]
    prog = ["C", "F", "G", "C"]
    for b in range(-1, 9):
        t0 = origin + b * barlen
        if t0 >= 43.4 or t0 + barlen < 30.0:
            continue
        ch = CH[prog[b % 4]]
        for i in range(4):
            tb = t0 + i * barlen / 4
            if 30.0 <= tb < 43.4:
                place(m, tb, kick() if i % 2 == 0 else clap(), 0.35 if i % 2 == 0 else 0.5)
                place(m, tb, bass(ch[0] - 12 + (7 if i % 2 else 0), barlen / 4), 0.35)
                place(m, tb + barlen / 8, hat(), 1.0)
                for n in ch:
                    place(m, tb + barlen / 8, pluck(n + 12, 0.18), 0.12)
    tune = [72, 74, 76, 79, 76, 74, 72, 67]
    for b in range(8):
        for i, n in enumerate(tune[(b % 2) * 4:(b % 2) * 4 + 4]):
            tn = origin + b * barlen + i * barlen / 4 + 0.05
            if 30 <= tn < 43.3 and b % 2 == 1:
                place(m, tn, whistle(n, barlen / 4.5), 0.28)
    for n in (60, 64, 67, 72):  # ta-da on the laugh
        place(m, 43.4, pluck(n, 1.2, 3), 0.25)
    # ---- M3 pharmacy: theme slowed and slightly detuned ----
    beat3 = 60 / 96
    t = 45.2
    k = 0
    while t < BEAT["leave"] + 1.2:
        if BEAT["handover"] - 0.2 < t < S["s3b"]["start"] - 0.1:
            t += beat3
            k += 1
            continue
        ch = CH[["C", "F", "G", "C"][(k // 4) % 4]]
        place(m, t, marimba(ch[k % 3] + 24 + (0.0 if k % 2 else -0.3), 0.5), 0.16)
        if k % 2 == 0:
            place(m, t, bass(ch[0] - 12, beat3), 0.25)
        t += beat3
        k += 1
    # ominous sting at the hand-over
    ho = BEAT["handover"]
    place(m, ho, timpani(36, 2.0), 0.6)
    for n in (36, 37, 43):
        place(m, ho, pad(n, 1.9, 0.05, 0.6, 6), 0.9)
    # ---- M4 villain swing (D minor, 120 bpm, swung) ----
    beat4 = 0.5
    stop = BEAT["music_stop"]
    t = 60.6
    k = 0
    while t < stop:
        ch = CH[["Dm", "Dm", "Bb", "A"][(k // 4) % 4]]
        bt = k % 4
        place(m, t, tuba(ch[0] - 12 + (0 if bt in (0, 1) else 7), 0.4), 0.55 if bt in (0, 2) else 0.0)
        place(m, t + beat4 * 0.66, pluck(ch[(k * 2) % 3] + 12, 0.25, 14), 0.3)
        if bt in (1, 3):
            place(m, t, snap(), 0.7)
        if t > BEAT["dance"]:
            place(m, t, kick(), 0.5 if bt in (0, 2) else 0)
            place(m, t + beat4 * 0.66, hat(), 1.4)
            if bt == 0:
                for n in ch:
                    place(m, t, tuba(n + 12, 0.25), 0.25)
        if k % 8 == 7:
            place(m, t + 0.25, tabla(57), 0.5)
            place(m, t + 0.37, tabla(62), 0.5)
        t += beat4
        k += 1
    # ---- M5 dark drone under the threat + narrator ----
    place(m, stop + 0.6, pad(26, 100 - stop - 0.6, 1.5, 1.2, 3), 0.45)
    place(m, stop + 0.6, pad(33, 100 - stop - 0.6, 2.0, 1.2, 3), 0.35)
    # ---- M6 hospital: sparse piano + low strings, A minor 70 bpm ----
    beat6 = 60 / 70
    t = 100.4
    k = 0
    while t < 154.6:
        ch = CH[["Am", "F", "C", "G"][(k // 4) % 4]]
        if k % 4 == 0:
            place(m, t, pad(ch[0] - 12, beat6 * 4 + 0.6, 1.0, 1.0, 3), 0.7)
            place(m, t, piano(ch[0], 2.5), 0.22)
        place(m, t + beat6 * 0.5, piano(ch[(k + 1) % 3] + 12, 1.4), 0.12)
        t += beat6
        k += 1
    # ---- M7 hope: C G Am F, swell to the slogan, resolve on the end card ----
    beat7 = 60 / 88
    t = 155.0
    k = 0
    sl, ec = BEAT["slogan"], BEAT["endcard"]
    while t < ec:
        ch = CH[["C", "G", "Am", "F"][(k // 4) % 4]]
        lvl = 0.6 + 0.6 * (t > sl)
        if k % 4 == 0:
            for n in ch:
                place(m, t, pad(n, beat7 * 4 + 0.5, 0.4, 0.8, 5), 0.5 * lvl)
            place(m, t, bass(ch[0] - 12, beat7 * 3.5), 0.35 * lvl)
        for i in range(2):
            place(m, t + i * beat7 / 2, piano(ch[(k + i) % 3] + 24, 1.0), 0.1 * lvl)
        if t > 162:
            place(m, t, kick(), 0.25 * lvl if k % 2 == 0 else 0)
        t += beat7
        k += 1
    for i in range(int((sl - 167.0) / 0.06)):  # timpani roll into the slogan
        place(m, 167.0 + i * 0.06, timpani(36, 0.3), 0.12 + 0.3 * i / max(1, (sl - 167.0) / 0.06))
    sw = noise(1.6) * np.linspace(0, 1, int(1.6 * SR)) ** 2
    place(m, sl - 1.6, lp(sw, 0.2), 0.15)
    for n in (48, 55, 60, 64, 67, 72):  # final resolving chord
        place(m, ec, pad(n, 5.0, 0.3, 1.6, 5), 0.5)
    for i, n in enumerate((84, 88, 91, 96)):
        place(m, ec + 0.3 + i * 0.18, bell(hz(n), 2.0), 0.08)
    return m


def sfx():
    s = buf()
    # school ambience: soft air + birds + distant chatter
    amb = lp(noise(29.5), 0.02) * 0.05
    place(s, 0, amb * np.minimum(1, tt(29.5) / 1.0))
    for k in range(28):
        tb = 0.4 + k * 1.05 + rng.uniform(0, 0.6)
        f0 = rng.uniform(2500, 4200)
        d = 0.12
        t = tt(d)
        chirp = np.sin(2 * np.pi * np.cumsum(f0 + 1500 * np.sin(t * 60)) / SR) * env(d, 0.005, 0.03)
        place(s, tb, chirp, 0.05)
        place(s, tb + 0.15, chirp, 0.04)
    place(s, 1.5, bell(1320, 2.5), 0.05)   # distant school bell
    # phone taps + ping
    for i in range(22):
        place(s, BEAT["phone_type"] + i * 0.09, snap(0.03), 0.25)
    place(s, BEAT["phone_reply"], bell(1760, 0.6), 0.25)
    place(s, BEAT["phone_reply"] + 0.1, bell(2350, 0.6), 0.2)
    whoosh = lambda d, up=True: lp(noise(d), 0.15) * (np.linspace(0, 1, int(d * SR)) if up else np.linspace(1, 0, int(d * SR))) ** 2
    place(s, BEAT["phone_zoom"], whoosh(0.9), 0.5)
    # cycling: chain ticks, bells, three-wheeler, birds
    for i in range(int(14.8 / 0.11)):
        place(s, 30.1 + i * 0.11, snap(0.02), 0.06)
    place(s, 30, lp(noise(14.8), 0.03) * 0.08)
    for tb in (BEAT["bell1"], BEAT["bell2"]):
        place(s, tb, bell(2100, 0.9), 0.35)
        place(s, tb, bell(2650, 0.7), 0.2)
    t = tt(4.0)
    eng = np.sign(np.sin(2 * np.pi * (70 + 8 * np.sin(t * 3)) * t)) * 0.5 + np.sin(2 * np.pi * 140 * t) * 0.3
    eng = lp(eng.astype(np.float32), 0.08) * np.exp(-((t - 2.0) ** 2) / 0.9)
    place(s, 38.5, eng, 0.18)
    # pharmacy: door chime, fan hum, packet rattle, pop + gulp, dive
    place(s, 45.15, bell(1568, 1.2), 0.3)
    place(s, 45.55, bell(1245, 1.4), 0.3)
    place(s, 45.3, lp(noise(BEAT["leave"] - 45.3), 0.01) * 0.12)
    for i in range(10):
        place(s, BEAT["handover"] + 0.3 + i * 0.05, snap(0.03), 0.3)
    place(s, BEAT["swallow"] - 0.35, snap(0.05), 0.6)
    gl = np.sin(2 * np.pi * np.cumsum(220 - 120 * tt(0.25) / 0.25) / SR) * env(0.25, 0.01, 0.05)
    place(s, BEAT["swallow"] + 0.3, gl, 0.4)
    place(s, BEAT["dive"] - 0.3, whoosh(1.3), 0.6)
    place(s, 59.5, kick(0.5), 0.4)
    # microscopic world
    place(s, 60, lp(noise(BEAT["music_stop"] - 60), 0.01) * 0.08)
    for k in range(60):
        tb = 60.2 + k * 0.48 + rng.uniform(0, 0.3)
        if tb > BEAT["music_stop"]:
            break
        t = tt(0.12)
        place(s, tb, np.sin(2 * np.pi * np.cumsum(300 + 900 * t / 0.12) / SR) * env(0.12, 0.005, 0.03), 0.06)
    from scenes_b import SENS, GOOD  # pops in sync with the picture
    for (x, y, ph, v, tb) in SENS:
        t = tt(0.15)
        place(s, tb, np.sin(2 * np.pi * np.cumsum(900 - 600 * t / 0.15) / SR) * env(0.15, 0.001, 0.04), 0.35)
        place(s, tb, snap(0.04), 0.4)
    gh = BEAT["good_hit"]
    for x, y, k in GOOD:
        t = tt(0.4)
        place(s, gh + k * 0.28, np.sin(2 * np.pi * np.cumsum(700 - 400 * t / 0.4) / SR) * env(0.4, 0.01, 0.1), 0.18)
    for k in range(10):  # enzyme snips
        place(s, 63 + k * 1.3, snap(0.02), 0.3)
        place(s, 63.05 + k * 1.3, snap(0.02), 0.3)
    d1, d2 = BEAT["divide"] + 0.3, BEAT["divide"] + 1.7
    for tb, n in ((d1 + 0.7, 4), (d2 + 0.7, 8)):
        for i in range(n):
            t = tt(0.12)
            place(s, tb + i * 0.03, np.sin(2 * np.pi * np.cumsum(200 + 500 * t / 0.12) / SR) * env(0.12), 0.12)
    for i in range(int((BEAT["music_stop"] - BEAT["dance"]) / 0.86)):
        place(s, BEAT["dance"] + i * 0.86, clap(0.1), 0.5)   # high fives
    # record scratch + silence, then heartbeat
    t = tt(0.45)
    scr = np.sin(2 * np.pi * np.cumsum(600 * (1 - t / 0.45) + 200 * np.sin(t * 40)) / SR) * env(0.45, 0.005, 0.05)
    place(s, BEAT["music_stop"], scr + hp(noise(0.45), 0.9) * 0.2 * env(0.45), 0.4)
    for i in range(int((100 - (S["s4j"]["start"])) / 0.85) + 1):
        tb = S["s4j"]["start"] + i * 0.85
        place(s, tb, kick(0.3), 0.8)
        place(s, tb + 0.28, kick(0.3), 0.5)
    place(s, BEAT["black"], timpani(31, 2.0), 0.6)
    # calendar flips + clock
    for i in range(4):
        place(s, 100.05 + i * 0.36, lp(noise(0.12), 0.4) * env(0.12, 0.01, 0.05), 0.4)
    # hospital ambience, monitor beeps
    place(s, 102.3, lp(noise(52), 0.01) * 0.15)
    for i in range(int((BEAT["lab_montage"] - BEAT["ward"]) / 0.51)):
        place(s, BEAT["ward"] + i * 0.51, np.sin(2 * np.pi * 1000 * tt(0.08)) * env(0.08, 0.005, 0.02), 0.07)
    lm = BEAT["lab_montage"]
    place(s, lm + 0.1, snap(0.05), 0.5)
    place(s, lm + 0.6, bell(3000, 0.3), 0.15)
    place(s, lm + 0.65, bell(3300, 0.3), 0.12)
    place(s, lm + 1.15, kick(0.2), 0.4)
    place(s, lm + 1.6, snap(0.06), 0.4)
    # lab hum, keyboard, paper
    place(s, 115, np.sin(2 * np.pi * 100 * tt(4.5)) * 0.03)
    for i in range(14):
        place(s, 115.3 + i * 0.13 + rng.uniform(0, 0.05), snap(0.02), 0.15)
    place(s, BEAT["micro_walk"], lp(noise(0.3), 0.3) * env(0.3, 0.02, 0.1), 0.3)
    for i in range(int(2.2 / 0.45)):
        place(s, BEAT["micro_walk"] + i * 0.45, kick(0.1), 0.08)   # footsteps
    for i in range(int((155 - BEAT["family"]) / 0.51)):
        place(s, BEAT["family"] + i * 0.51, np.sin(2 * np.pi * 1000 * tt(0.08)) * env(0.08, 0.005, 0.02), 0.05)
    # cutaway whooshes
    for tb in (BEAT["virus_cut"], BEAT["bact_cut"], BEAT["report_cut"]):
        place(s, tb - 0.2, whoosh(0.4), 0.25)
    # slogan impacts + end shimmer
    seg = S["s7e"]
    dur = seg["end"] - seg["start"]
    for f in (0, 0.36, 0.74):
        place(s, BEAT["slogan"] + dur * f, kick(0.6), 0.7)
        place(s, BEAT["slogan"] + dur * f, timpani(29, 1.5), 0.4)
    for i in range(12):
        place(s, BEAT["endcard"] + 0.1 + i * 0.07, bell(hz(96 - (i % 4) * 3), 0.8), 0.04)
    return s


def write(path, x, target):
    """Scale to a fixed peak so the stems keep sensible relative levels."""
    x = x[:SR * TOTAL]
    peak = np.max(np.abs(x)) or 1
    x = x * (target / peak)
    with wave.open(str(path), "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())


if __name__ == "__main__":
    (ROOT / "audio").mkdir(exist_ok=True)
    m = music()
    write(ROOT / "audio" / "music.wav", m, 0.42)
    write(ROOT / "audio" / "sfx.wav", sfx(), 0.55)
    print("music.wav and sfx.wav written")
