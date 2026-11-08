"""Scene 4: inside the body - selection of resistant bacteria."""
import math
import skia
from gfx import *
from microbes import bacterium, rbc, wbc, amoxicillin, scissors, burst, KINDS
from timing import S, BEAT, talking

T0 = 60.0
R = rng(42)
SENS = [(R(150, 1750), R(200, 880), R(0, 6.28), int(R(0, 2))) for _ in range(14)]
# each sensitive bacterium is reached by "its" molecule at a staggered time
for k in range(len(SENS)):
    x, y, ph, v = SENS[k]
    SENS[k] = (x, y, ph, v, 60.75 + k * 0.1 + (x / 1920) * 0.35)
GOOD = [(260 + k * 280, 820 + (k % 2) * 50, k) for k in range(6)]
GANG_HIDE = [(1250, 380), (1400, 650), (960, 700), (1560, 460)]
GANG_POS = [(820, 360), (1540, 340), (800, 740), (1560, 740)]
BOSS_POS = (1180, 540)
RBCS = [(R(0, 2400), R(140, 940), R(30, 64), R(0, 360), R(60, 140), k % 3) for k in range(26)]


def vessel(cv, t):
    cv.drawRect(skia.Rect.MakeXYWH(-400, -400, W + 800, H + 800), rad((W / 2, H / 2), W * 0.8, [hexc("8e1b2c"), hexc("5a0b1d"), hexc("2a0410")], [0, 0.6, 1]))
    for sg, y0 in ((1, 0), (-1, H)):
        pth = skia.Path()
        pth.moveTo(-400, y0 - sg * 400)
        for i in range(0, 56):
            x = i * 50 - 400
            y = y0 + sg * (110 + 22 * math.sin(i * 0.7 + t * 1.3))
            pth.lineTo(x, y)
        pth.lineTo(W + 400, y0 - sg * 400)
        pth.close()
        cv.drawPath(pth, lin((0, y0), (0, y0 + sg * 170), [hexc("ff8a9e"), hexc("b0233f")]))
        for i in range(0, 40):
            x = i * 52 - 30
            y = y0 + sg * (70 + 22 * math.sin(i * 0.7 + t * 1.3))
            ellipse(cv, x, y, 22, 14, fill(alpha(hexc("ffd0d8"), 0.35)))
    for k in range(40):  # plasma particles
        x = (k * 97 + t * (40 + k % 5 * 12)) % (W + 40) - 20
        y = 160 + (k * 53) % 760
        cv.drawCircle(x, y, 2 + k % 3, fill(alpha(hexc("ffc2cc"), 0.35)))


def cells(cv, t, layer):
    for x0, y, r, rot, v, l in RBCS:
        if l != layer:
            continue
        x = (x0 + t * v) % (W + 400) - 200
        rbc(cv, x, y, r * (0.7 + 0.25 * l), rot + t * 20, a=0.55 + 0.2 * l)


def label(cv, s, x, y, a, col=skia.ColorWHITE):
    if a <= 0:
        return
    w = text_width(s, 34) + 40
    rrect(cv, x - w / 2, y - 40, w, 54, 27, fill(alpha(hexc("1a0610"), 0.65 * a)))
    text(cv, s, x, y - 2, 34, alpha(col, a), align="center")


def gang_positions(t):
    """Resistant bacteria positions with two rounds of binary fission."""
    rev = BEAT["boss_reveal"]
    d1, d2 = BEAT["divide"] + 0.3, BEAT["divide"] + 1.7
    u1, u2 = ease(t, d1, d1 + 0.8), ease(t, d2, d2 + 0.8)
    out = []
    for k in range(4):
        hx, hy = GANG_HIDE[k]
        gx, gy = GANG_POS[k]
        m = ease(t, rev, rev + 1.2)
        px, py = lerp(hx, gx, m), lerp(hy, gy, m)
        if u1 <= 0:
            out.append((px, py, 0.0, k))
            continue
        if u1 < 1:
            out.append((px, py, u1, k))
            continue
        for sg in (-1, 1):
            cx, cy = px + sg * 120, py + (18 if sg > 0 else -18)
            if u2 <= 0:
                out.append((cx, cy, 0.0, k))
            elif u2 < 1:
                out.append((cx, cy, u2, k + 1))
            else:
                for sg2 in (-1, 1):
                    out.append((cx + sg2 * 60, cy + sg2 * 95, 0.0, k + sg2))
    return out


def scene4(cv, t):
    stop = BEAT["music_stop"]
    tm = min(t, stop)            # motion freezes when the music stops
    rev = BEAT["boss_reveal"]
    # ---- camera ----
    cam = [(60.0, (960, 540, 1.15)), (rev, (1000, 540, 1.0)), (rev + 0.8, (1120, 530, 1.25)),
           (S["s4c"]["end"], (1150, 520, 1.3)), (BEAT["smartbug"], (900, 520, 1.25)),
           (S["s4d"]["end"], (820, 560, 1.35)), (BEAT["good_hit"] - 0.1, (960, 640, 1.0)),
           (BEAT["divide"], (1000, 560, 0.98)), (BEAT["dance"], (1000, 540, 1.0)),
           (stop, (1000, 540, 1.02)), (stop + 0.6, (1000, 540, 1.02)),
           (S["s4i"]["start"] + 0.9, (BOSS_POS[0] + 20, BOSS_POS[1] - 10, 2.5)), (100.0, (BOSS_POS[0] + 20, BOSS_POS[1] - 10, 2.8))]
    cx, cy, z = keys(t, cam)
    rot = 0.0
    if BEAT["dance"] < t < stop:
        rot = math.sin(t * 2.2) * 3
        z *= 1.06 + 0.02 * abs(math.sin(t * math.pi / 0.43))
    with Cam(cv, cx, cy, z, rot):
        vessel(cv, tm)
        cells(cv, tm, 0)
        wbc(cv, (300 + tm * 25) % 2300 - 200, 260, 70, tm)
        cells(cv, tm, 1)
        # ---- sensitive bacteria and their molecules ----
        for k, (x, y, ph, v, tb) in enumerate(SENS):
            bx = x + wobble(tm, 0.3, 14, ph)
            by = y + wobble(tm, 0.25, 12, ph + 1)
            if t < tb:
                near = ease(t, tb - 0.6, tb)
                bacterium(cv, bx, by, "sensitive", tm, 1.0, rot=wobble(tm, 0.2, 8, ph), var=v,
                          mood="scared" if near > 0.3 else "happy", mouth=0.5 * near, look=(-1, 0) if near > 0.2 else (0, 0))
                ms = 60.2 + k * 0.03
                if t > ms:
                    u = clamp((t - ms) / (tb - ms))
                    amoxicillin(cv, lerp(-120, bx - 30, u), lerp(by + 60 * math.sin(k), by, u), 0.9, rot=t * 90 + k * 30)
            else:
                burst(cv, bx, by, (t - tb) / 0.55, hexc("8fd3ff") if v == 0 else hexc("9be7c3"), k)
        # ---- beneficial bacteria (normal flora) ----
        gh = BEAT["good_hit"]
        for x, y, k in GOOD:
            hit = gh + k * 0.28
            wilt = ease(t, hit, hit + 0.9)
            if t > hit - 0.7 and t < hit + 0.2:
                u = clamp((t - (hit - 0.7)) / 0.7)
                amoxicillin(cv, lerp(x - 260, x - 20, u), lerp(y - 160, y, u), 0.85, rot=t * 120)
            if t > hit:
                burst(cv, x, y, (t - hit) / 0.6, hexc("ffe082"), k)
            bacterium(cv, x + wobble(tm, 0.3, 10, k), y + wobble(tm, 0.3, 6, k) + wilt * 30, "beneficial", tm, 1.1,
                      rot=wilt * 25 * (1 if k % 2 else -1), var=k, mood="sad" if wilt > 0.2 else "happy",
                      wilt=wilt, alpha_=1 - 0.35 * wilt)
        cells(cv, tm, 2)
        # ---- resistant gang ----
        dancing = BEAT["dance"] < t
        beat = 0.43
        for i, (x, y, split, k) in enumerate(gang_positions(tm)):
            bob = squash = 0.0
            if dancing:
                ph = ((tm - BEAT["dance"]) / beat) % 1.0
                bob = -abs(math.sin(ph * math.pi)) * 40
                squash = 0.12 * math.cos(ph * 2 * math.pi)
            elif t > rev:
                bob = wobble(tm, 1.6, 6, i)
            smart = (i == 0 and BEAT["smartbug"] < t < S["s4d"]["end"] + 0.6 and split == 0)
            sc = 1.0
            px, py = x, y + bob
            hand = None
            if smart:
                u = ease(t, BEAT["smartbug"], BEAT["smartbug"] + 0.5) * (1 - ease(t, S["s4d"]["end"], S["s4d"]["end"] + 0.6))
                px, py, sc = lerp(x, 760, u), lerp(y, 520, u), 1 + 0.5 * u
                hand = (70, -90)
            laugh = 0.6 * abs(math.sin(tm * 9 + i)) if (rev + 0.5 < t < S["s4c"]["end"] or dancing) and not smart else 0.0
            mood = "evil"
            mouth = talking("smartbug", t) if smart else laugh
            if dancing and i % 2 == 0:
                ph = ((tm - BEAT["dance"]) / (beat * 2)) % 1.0
                if ph < 0.25:  # high five sparkle
                    glow(cv, px + 95, py - 60, 46, hexc("fff59d"), 0.8 * (1 - ph * 4))
                    hand = (95, -70)
            bacterium(cv, px, py, "resistant", tm, sc, rot=wobble(tm, 0.4, 6, i) + (squash * 40 if dancing else 0),
                      mood=mood, mouth=mouth, squash=squash, split=split, var=k, look=(-0.6, 0) if smart else (0, 0), hand=hand)
            # enzyme scissors snipping antibiotic near some resistant cells
            if not dancing and t > 60.9 and i % 2 == 0 and split == 0:
                cyc = (tm * 0.7 + i * 0.37) % 1.0
                mx, my = px - 150 + cyc * 70, py - 70
                amoxicillin(cv, mx, my, 0.75, rot=20, a=1 - max(0, cyc - 0.6) * 2.5, cut=max(0, cyc - 0.55) * 2)
                scissors(cv, mx + 30, my - 30, 0.8, tm)
        # ---- the boss ----
        if t > rev:
            u = ease(t, rev, rev + 0.9)
            bx, by = lerp(2200, BOSS_POS[0], u), BOSS_POS[1]
            bob = 0.0
            squash = 0.0
            if dancing:
                ph = ((tm - BEAT["dance"]) / beat) % 1.0
                bob = -abs(math.sin(ph * math.pi)) * 50
                squash = 0.1 * math.cos(ph * 2 * math.pi)
            else:
                bob = wobble(tm, 0.8, 10)
            close = t > stop
            mood = "menace" if close else "evil"
            look = (0, 0) if close else (-0.4, 0.1)
            turn_u = ease(t, stop + 0.2, S["s4i"]["start"])
            boss_rot = wobble(tm, 0.3, 4) if not close else lerp(12, 0, turn_u)
            bacterium(cv, bx, by + bob, "boss", tm, 1.25, rot=boss_rot, mood=mood, mouth=talking("boss", t),
                      squash=squash, look=look, hand=(150, -60) if S["s4e"]["start"] < t < S["s4f"]["end"] else None)
            if close:
                glow(cv, bx, by + 160, 260, hexc("7c4dff"), 0.35 * turn_u)
        # ---- educational labels ----
        label(cv, "Amoxicillin (antibiotic)", 360, 210, ease(t, 60.4, 60.8) * (1 - ease(t, 62.0, 62.3)), hexc("fff59d"))
        label(cv, "Sensitive bacteria", 1300, 1000, ease(t, 60.5, 60.9) * (1 - ease(t, 61.8, 62.1)), hexc("b3e5fc"))
        label(cv, "Resistant bacteria survive", 1180, 210, ease(t, rev + 0.9, rev + 1.3) * (1 - ease(t, rev + 3.4, rev + 3.8)), hexc("ff80ab"))
        label(cv, "Good bacteria (normal flora) harmed too", 960, 990, ease(t, gh, gh + 0.4) * (1 - ease(t, gh + 3.0, gh + 3.4)), hexc("a7ffeb"))
        label(cv, "Survivors multiply", 1000, 200, ease(t, BEAT["divide"] + 0.4, BEAT["divide"] + 0.8) * (1 - ease(t, BEAT["dance"] - 0.4, BEAT["dance"])), hexc("ff80ab"))
    # mood lighting + transitions
    if t > stop:
        cv.drawRect(skia.Rect.MakeWH(W, H), rad((W / 2, H / 2), W * 0.7, [skia.Color(0, 0, 0, 0), alpha(hexc("12001f"), 0.75)]))
    vignette(cv, 0.5)
    if t < 60.5:
        cv.drawRect(skia.Rect.MakeWH(W, H), rad((W / 2, H / 2), W * (0.1 + 1.6 * ease(t, 60, 60.5)),
                    [skia.Color(0, 0, 0, 0), skia.Color(0, 0, 0, 0), hexc("2a0010")], [0, 0.9, 1]))
    bl = BEAT["black"]
    if t > bl:
        fade(cv, ease(t, bl, bl + 0.45))
        # heartbeat pulse in the dark
        hb = (t - bl) % 0.85
        pulse = max(0, 1 - hb / 0.25) + 0.6 * max(0, 1 - abs(hb - 0.3) / 0.15)
        cv.drawRect(skia.Rect.MakeWH(W, H), rad((W / 2, H / 2), W * 0.6, [alpha(hexc("5a0010"), 0.0), alpha(hexc("5a0010"), 0.5 * pulse * ease(t, bl + 0.4, bl + 0.8))]))
