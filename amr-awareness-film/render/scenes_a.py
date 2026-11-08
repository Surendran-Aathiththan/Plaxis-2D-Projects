"""Scenes 1-3: school, cycling, pharmacy (+ swallow and dive)."""
import math
import skia
from gfx import *
from characters import (Person, STUDENT1, STUDENT2, PHARMACIST, bicycle, rider, phone, blink_at)
from timing import S, BEAT, talking

s1, s2, ph = Person(STUDENT1), Person(STUDENT2), Person(PHARMACIST)
EXTRA_SPECS = [dict(STUDENT1, hair_style="short", skin=hexc("7d4b2e"), bag=hexc("2e7d32")),
               dict(STUDENT2, hair_style="part", skin=hexc("b07a52"), bag=hexc("5d4037"), width=0.95),
               dict(STUDENT1, hair_style="curly", skin=hexc("6d3f25"), bag=hexc("37474f"))]
extras = [Person(sp) for sp in EXTRA_SPECS]


# ---------------- shared bits ----------------
def sky(cv, top="8ec9f2", bot="fdf1d8"):
    cv.drawRect(skia.Rect.MakeWH(W, H), lin((0, 0), (0, H * 0.7), [hexc(top), hexc(bot)]))


def sun(cv, x, y):
    glow(cv, x, y, 260, hexc("fff3c4"), 0.7)
    cv.drawCircle(x, y, 70, fill(hexc("fff8e1")))


def cloud(cv, x, y, s):
    for dx, dy, r in ((0, 0, 50), (50, -20, 60), (110, 0, 48), (55, 12, 50)):
        cv.drawCircle(x + dx * s, y + dy * s, r * s, fill(alpha(skia.ColorWHITE, 0.92)))


def palm(cv, x, y, h, t, sway=1.0):
    top = (x + 30 + wobble(t, 0.25, 6 * sway), y - h)
    cv.drawPath(path([("M", x, y), ("Q", x + 10, y - h * 0.5, top[0], top[1])]), stroke(hexc("8d6e52"), 16))
    for k in range(9):
        a = -math.pi + k * math.pi / 8 + wobble(t, 0.3, 0.05 * sway, k)
        ex, ey = top[0] + math.cos(a) * 130, top[1] + math.sin(a) * 60 + 40
        cv.drawPath(path([("M", top[0], top[1]), ("Q", (top[0] + ex) / 2, top[1] - 40 + (ey - top[1]) * 0.2, ex, ey)]),
                    stroke(hexc("3f8f3a" if k % 2 else "2f7a32"), 14))
    for k in range(3):
        cv.drawCircle(top[0] - 10 + k * 12, top[1] + 12, 10, fill(hexc("6d4c2f")))


def tree(cv, x, y, s, t):
    cv.drawPath(path([("M", x - 30 * s, y), ("Q", x - 10 * s, y - 200 * s, x - 40 * s, y - 330 * s),
                      ("L", x + 40 * s, y - 330 * s), ("Q", x + 10 * s, y - 200 * s, x + 30 * s, y), ("Z",)]),
                fill(hexc("6b4a35")))
    for dx, dy, r, c in ((-170, -380, 150, "2e7d32"), (150, -390, 160, "2e7d32"), (0, -470, 190, "388e3c"),
                         (-90, -520, 130, "43a047"), (110, -510, 140, "43a047"), (0, -380, 160, "33691e")):
        cv.drawCircle(x + (dx + wobble(t, 0.2, 4, dx)) * s, y + dy * s, r * s, fill(hexc(c)))
        cv.drawCircle(x + (dx - r * 0.3) * s, y + (dy - r * 0.3) * s, r * 0.45 * s, fill(alpha(hexc("9ccc65"), 0.35)))


def bird(cv, x, y, t, s=1.0):
    f = math.sin(t * 14) * 14 * s
    cv.drawPath(path([("M", x - 18 * s, y - f), ("Q", x - 8 * s, y - 4 * s, x, y), ("Q", x + 8 * s, y - 4 * s, x + 18 * s, y - f)]),
                stroke(hexc("2b2b2b"), 3.5 * s))


def school_building(cv, x, y, w, h):
    cv.drawRect(skia.Rect.MakeXYWH(x, y, w, h), lin((x, y), (x, y + h), [hexc("fbf0d9"), hexc("ead7b4")]))
    roof = [(x - 40, y + 4), (x + w / 2, y - 120), (x + w + 40, y + 4)]
    for k in range(2):
        yy = y + k * h / 2
        poly(cv, [(x - 30, yy + 6), (x + w + 30, yy + 6), (x + w + 10, yy - 40), (x - 10, yy - 40)], fill(hexc("b5482e")))
        for i in range(int(w / 24) + 2):
            cv.drawLine(x - 20 + i * 24, yy + 4, x - 4 + i * 24, yy - 38, stroke(alpha(hexc("7f2c1a"), 0.5), 2))
    cv.drawRect(skia.Rect.MakeXYWH(x, y + h / 2 - 2, w, 14), fill(hexc("d9c39a")))
    for row in range(2):
        for i in range(int(w / 120)):
            wx = x + 40 + i * 120
            wy = y + 40 + row * h / 2
            rrect(cv, wx, wy, 64, 100, 6, fill(hexc("6e8faa")))
            rrect(cv, wx, wy, 64, 100, 6, stroke(hexc("8a6a48"), 5))
            cv.drawLine(wx + 32, wy, wx + 32, wy + 100, stroke(hexc("8a6a48"), 3))
            cv.drawRect(skia.Rect.MakeXYWH(wx + 4, wy + 4, 24, 40), fill(alpha(skia.ColorWHITE, 0.18)))
    for i in range(int(w / 240) + 1):  # pillars
        cv.drawRect(skia.Rect.MakeXYWH(x + i * 240 - 10, y + h / 2, 20, h / 2), fill(hexc("f4e6c8")))


def ground(cv, horizon, col1="e8d2a6", col2="d4b98a"):
    cv.drawRect(skia.Rect.MakeXYWH(-2000, horizon, W + 4000, H + 2000), lin((0, horizon), (0, H), [hexc(col1), hexc(col2)]))


def dissolve(cv, a, c=skia.ColorWHITE):
    fade(cv, a, c)


# ---------------- Scene 1 ----------------
def scene1(cv, t):
    zt = BEAT["phone_zoom"]
    in_phone = BEAT["phone_type"] - 0.15 <= t < S["s1d"]["start"] - 0.25
    if in_phone:
        return phone_shot(cv, t)
    # camera per shot
    hx1, hx2 = 1060, 1290
    cams = [(0.0, (900, 560, 1.0)), (S["s1a"]["start"] - 0.6, (1060, 600, 1.12)),
            (S["s1a"]["start"] - 0.3, (1050, 540, 1.85)), (S["s1b"]["start"] - 0.3, (1050, 540, 1.85)),
            (S["s1b"]["start"] - 0.05, (1175, 600, 1.45)), (S["s1c"]["start"] - 0.25, (1175, 600, 1.45)),
            (S["s1c"]["start"] - 0.05, (1060, 560, 1.8)), (BEAT["phone_type"], (1060, 560, 1.8)),
            (S["s1d"]["start"] - 0.25, (1250, 580, 1.6)), (S["s1f"]["start"] - 0.25, (1250, 580, 1.6)),
            (S["s1f"]["start"] - 0.05, (1175, 600, 1.45)), (zt, (1175, 600, 1.5)), (30.0, (1110, 640, 5.0))]
    # cuts: hard switch when consecutive keys are < 0.3s apart
    cx, cy, z = keys(t, cams)
    with Cam(cv, cx, cy, z):
        sky(cv)
        sun(cv, 300, 200)
        for k, (x0, y0, s_) in enumerate(((100, 150, 1.0), (900, 110, 0.8), (1500, 190, 1.2))):
            cloud(cv, (x0 + t * 12 * (k + 1)) % 2200 - 150, y0, s_)
        ground(cv, 690)
        school_building(cv, 160, 330, 1500, 360)
        tree(cv, 220, 860, 1.0, t)
        for k in range(4):
            bird(cv, (200 + t * (90 + k * 15) + k * 140) % 2400 - 200, 140 + k * 35 + wobble(t, 0.5, 10, k), t + k, 0.9)
        # background students walking / playing
        for k, ex in enumerate(extras):
            dirn = 1 if k % 2 == 0 else -1
            x = (300 + k * 520 + dirn * t * 55) % 2200 - 150
            ex.draw(cv, x, 790 + k * 12, 0.36, legs="walk", phase=t * 7 + k, look=(dirn, 0),
                    mouth=0.4 * max(0, math.sin(t * 6 + k)), blink=blink_at(t, k + 3))
        # cricket kids near the tree
        extras[0].draw(cv, 520, 770, 0.33, ra=(120 + 30 * math.sin(t * 4), 20), blink=blink_at(t, 9))
        # Student 2 walks in during the opening
        x2 = keys(t, [(0.0, 1900.0), (S["s1a"]["start"] - 0.7, hx2)])
        walking = x2 > hx2 + 2
        sing = 0.5 + 0.5 * math.sin(t * 9) if t < S["s1a"]["start"] - 0.5 else 0.0
        # Student 1 (sick, hand on throat while speaking)
        speaking1 = talking("s1", t)
        holding_phone = S["s1c"]["start"] + 1.0 < t < S["s1d"]["start"]
        p1 = dict(mouth=speaking1, blink=blink_at(t, 1), sick=0.35, brow="worried", smile=-0.1,
                  look=(0.6, 0) if t > S["s1a"]["end"] else (0.2, 0.1), tilt=-3)
        if t < S["s1b"]["start"] or (S["s1a"]["start"] < t < S["s1a"]["end"]):
            p1["lh"] = (-6, -478)
        if holding_phone:
            p1["rh"] = (70, -420)
            p1["ritem"] = lambda c, x, y: (rrect(c, x - 22, y - 60, 44, 80, 8, fill(hexc("1b1d21"))),
                                           rrect(c, x - 18, y - 56, 36, 70, 6, fill(hexc("9fd3ff"))))
            p1["look"] = (0.4, 0.8)
        if t >= S["s1f"]["start"] - 0.2:
            p1.update(smile=0.6, brow="up", ra=(150, 25), sick=0.2)
            p1.pop("lh", None)
        s1.draw(cv, hx1, 1000, 0.85, **p1)
        # Student 2
        m2 = talking("s2", t)
        p2 = dict(mouth=max(m2, sing * 0.6), blink=blink_at(t, 2), smile=0.8, brow="up", look=(-0.8, 0), cheeks=True)
        if walking:
            p2.update(legs="walk", phase=t * 8, bob=abs(math.sin(t * 8)) * 6)
        if S["s1b"]["start"] - 0.1 < t < S["s1b"]["end"] + 0.3:
            p2.update(brow="worried", smile=0.0, lh=(-80, -430))
        if S["s1d"]["start"] - 0.3 < t < S["s1d"]["end"]:
            p2.update(rh=(10, -440), brow="up")  # thumps own chest
        if S["s1e"]["start"] - 0.1 < t < S["s1e"]["end"] + 0.4:
            p2.update(lh=(-170, -480), ra=(140, 20))
        s2.draw(cv, x2, 1000, 0.84, **p2)
    # zoom-to-phone transition
    if t > zt:
        u = ease(t, zt, 30.0)
        fade(cv, u * 0.9, skia.ColorWHITE)
    if t < 0.6:
        fade(cv, 1 - t / 0.6)


def phone_shot(cv, t):
    t0, tr = BEAT["phone_type"], BEAT["phone_reply"]
    q = "I have a sore throat and fever. What medicine should I take?"
    n = int(clamp((t - t0) / 2.0) * len(q))
    cv.drawRect(skia.Rect.MakeWH(W, H), lin((0, 0), (W, H), [hexc("e9d8b8"), hexc("c7ab80")]))
    cv.drawRect(skia.Rect.MakeWH(W, H), blurred(fill(alpha(hexc("ffffff"), 0.2)), 40))
    z = keys(t, [(t0, 1.0), (t0 + 6, 1.06)])
    with Cam(cv, 1010, 560, z):
        # hand
        ellipse(cv, 1000, 1020, 230, 160, fill(hexc("a86f4c")))
        phone(cv, 710, 110, 600, 900, scale_text=1.15, typed=q[:n] + ("|" if n < len(q) and int(t * 4) % 2 else ""),
              reply="Do not self-medicate with antibiotics. Consult a healthcare professional.",
              reply_a=ease(t, tr, tr + 0.4))
        for k in range(3):
            ellipse(cv, 1320, 640 + k * 70, 60, 34, fill(hexc("a86f4c")))
        ellipse(cv, 712, 760, 46, 90, fill(hexc("9c6444")))


# ---------------- Scene 2 ----------------
def scene2(cv, t):
    lt = t - 30
    speed = 430.0
    d = lt * speed
    zoom = keys(t, [(30, 1.0), (38.0, 1.0), (38.6, 1.18), (42.6, 1.18), (43.3, 1.0)])
    cx = keys(t, [(30, 960.0), (38.0, 960.0), (38.6, 1080.0), (42.6, 1080.0), (43.3, 960.0)])
    with Cam(cv, cx, 560, zoom):
        sky(cv, "7fc4f0", "fff0d2")
        sun(cv, 1600, 160)
        for k in range(3):
            cloud(cv, (k * 800 - d * 0.03) % 2400 - 200, 120 + k * 40, 1.0)
        # far hills + kovil
        cv.drawPath(path([("M", -2000, 560), ("Q", 0, 440, 900, 520), ("Q", 1800, 600, 4000, 500), ("L", 4000, 700), ("L", -2000, 700), ("Z",)]),
                    fill(hexc("9cc59a")))
        kx = 1500 - (d * 0.08) % 2600
        gop = [(kx, 560), (kx + 30, 420), (kx + 50, 420), (kx + 80, 560)]
        poly(cv, gop, fill(hexc("e8b86d")))
        for k in range(5):
            cv.drawLine(kx + 8 + k * 3, 540 - k * 26, kx + 72 - k * 3, 540 - k * 26, stroke(hexc("c98f3e"), 4))
        # palms (mid)
        for k in range(8):
            px = (k * 330 - d * 0.35) % 2640 - 300
            palm(cv, px, 690, 300 + (k % 3) * 40, t + k)
        # houses + walls (near-mid)
        for k in range(5):
            hx = (k * 620 - d * 0.6) % 3100 - 400
            cv.drawRect(skia.Rect.MakeXYWH(hx, 560, 300, 150), fill(hexc(["f2d8b0", "e9e0c9", "f5c9a8", "d8e6c6", "efe3d0"][k])))
            poly(cv, [(hx - 20, 566), (hx + 150, 470), (hx + 320, 566)], fill(hexc("b5482e")))
            rrect(cv, hx + 40, 600, 60, 70, 4, fill(hexc("6e8faa")))
            rrect(cv, hx + 190, 610, 70, 100, 4, fill(hexc("7b5236")))
        for k in range(30):
            wx = (k * 120 - d * 0.75) % 3600 - 300
            cv.drawRect(skia.Rect.MakeXYWH(wx, 680, 118, 60), fill(hexc("e6dccb")))
            cv.drawRect(skia.Rect.MakeXYWH(wx, 680, 118, 10), fill(hexc("cdbfa8")))
        # road
        cv.drawRect(skia.Rect.MakeXYWH(-1000, 740, W + 2000, 400), lin((0, 740), (0, H), [hexc("6f7378"), hexc("4d5156")]))
        for k in range(14):
            lx = (k * 260 - d) % 3640 - 400
            rrect(cv, lx, 1040, 140, 12, 6, fill(hexc("f2f2f2")))
        cv.drawRect(skia.Rect.MakeXYWH(-1000, 740, W + 2000, 14), fill(hexc("a29a8c")))
        # three-wheeler passing the other way (far lane, behind the bikes)
        if 38.5 < t < 42.5:
            u = (t - 38.5) / 4.0
            tuk(cv, lerp(2600, -900, u), 800, 0.62, t)
        # bikes: Student 1 behind, Student 2 in front
        pts1 = bicycle(cv, 700 + wobble(t, 0.4, 6), 930, 0.82, hexc("2e8b57"), d)
        sing = talking("s2", t)
        laugh = t >= BEAT["laugh"]
        rider(cv, s1, pts1, 0.78, dict(mouth=talking("s1", t) if laugh else 0.0, blink=blink_at(t, 1), sick=0.3,
                                      smile=0.5 if laugh else 0.2, look=(0.6, 0), turn=0.4, no_bag=False))
        pts2 = bicycle(cv, 1150 + wobble(t, 0.5, 8, 1), 1010, 0.86, hexc("c62828"), d * 1.02, bell=True)
        beat = math.sin(lt * math.pi * 2 * 1.07)
        pose2 = dict(mouth=max(sing, 0.7 * laugh * abs(math.sin(t * 10))), blink=blink_at(t, 2), smile=0.9, brow="up",
                     look=(-0.7, 0), turn=-0.3, tilt=beat * 6)
        if 31 < t < 43.3 and not (BEAT["bell1"] - 0.2 < t < BEAT["bell2"] + 0.3):
            pose2["rh"] = (60 + beat * 40, -560 + beat * 30)
        rider(cv, s2, pts2, 0.82, pose2)
        # pharmacy sign approaching
        if t > 42.6:
            u = ease(t, 42.6, 45.0)
            sx = lerp(2300, 1500, u)
            pharmacy_front(cv, sx, 760)
    vignette(cv, 0.25)
    if t > 44.6:
        fade(cv, (t - 44.6) / 0.4 * 0.8, skia.ColorWHITE)


def tuk(cv, x, y, s, t):
    cv.save(); cv.translate(x, y); cv.scale(s, s)
    poly(cv, [(-160, 40), (-160, -120), (-40, -170), (150, -170), (170, 40)], fill(hexc("2e7d32")))
    poly(cv, [(-150, -110), (-50, -158), (-50, -40), (-150, -40)], fill(hexc("bfe3f7")))
    rrect(cv, -170, -190, 340, 30, 12, fill(hexc("1b5e20")))
    rrect(cv, -60, -60, 210, 100, 8, fill(hexc("e8f5e9")))
    for wx in (-120, 120):
        cv.drawCircle(wx, 50, 38, fill(hexc("1c1c1c")))
        cv.drawCircle(wx, 50, 14, fill(hexc("9e9e9e")))
    cv.restore()


def pharmacy_front(cv, x, y):
    cv.drawRect(skia.Rect.MakeXYWH(x, y - 380, 620, 400), fill(hexc("f4f7f5")))
    rrect(cv, x + 20, y - 370, 580, 90, 10, fill(hexc("1b8a4c")))
    text(cv, "PHARMACY", x + 310, y - 305, 58, skia.ColorWHITE, align="center")
    cx, cy = x + 70, y - 325
    rrect(cv, cx - 12, cy - 34, 24, 68, 4, fill(skia.ColorWHITE))
    rrect(cv, cx - 34, cy - 12, 68, 24, 4, fill(skia.ColorWHITE))
    rrect(cv, x + 60, y - 250, 220, 270, 6, fill(hexc("9cc9df")))
    rrect(cv, x + 340, y - 250, 220, 160, 6, fill(hexc("9cc9df")))
    for k in range(4):
        cv.drawRect(skia.Rect.MakeXYWH(x + 350 + k * 52, y - 230, 40, 30), fill(hexc(["ef5350", "42a5f5", "ffca28", "66bb6a"][k])))


# ---------------- Scene 3 ----------------
_shelf = None


def shelves(cv):
    global _shelf
    if _shelf is None:
        r = rng(7)
        cols = ["e53935", "1e88e5", "fdd835", "43a047", "8e24aa", "fb8c00", "00acc1", "f06292", "ffffff"]
        _shelf = [(row, x, r(30, 70), r(40, 90), cols[int(r(0, len(cols)))]) for row in range(5)
                  for x in range(0, 1920, 1)]
        out, xx = [], {}
        for row in range(5):
            x = 40
            while x < 1880:
                w = r(34, 80)
                h = r(44, 96)
                out.append((row, x, w, h, cols[int(r(0, len(cols)))]))
                x += w + r(4, 12)
        _shelf = out
    cv.drawRect(skia.Rect.MakeWH(W, H), lin((0, 0), (0, H), [hexc("e8efe9"), hexc("d4ddd6")]))
    for row in range(5):
        y = 120 + row * 130
        cv.drawRect(skia.Rect.MakeXYWH(20, y + 100, 1880, 16), fill(hexc("a07850")))
    for row, x, w, h, c in _shelf:
        y = 120 + row * 130 + 100 - h
        rrect(cv, x, y, w, h, 3, fill(hexc(c)))
        rrect(cv, x + 4, y + h * 0.3, w - 8, h * 0.25, 2, fill(alpha(skia.ColorWHITE, 0.7)))
        cv.drawRect(skia.Rect.MakeXYWH(x, y, 6, h), fill(alpha(skia.ColorBLACK, 0.12)))


def counter(cv, x, y, w):
    rrect(cv, x, y, w, 420, 10, lin((0, y), (0, y + 420), [hexc("c7dde6"), hexc("9fb9c4")]))
    rrect(cv, x - 10, y - 20, w + 20, 30, 8, fill(hexc("7b5236")))
    for k in range(int(w / 140)):
        cv.drawRect(skia.Rect.MakeXYWH(x + 30 + k * 140, y + 60, 100, 70), fill(hexc(["ef9a9a", "90caf9", "fff59d", "a5d6a7"][k % 4])))
    cv.drawRect(skia.Rect.MakeXYWH(x, y + 10, w, 420), fill(alpha(skia.ColorWHITE, 0.25)))


def fan(cv, x, y, t):
    cv.drawLine(x, 0, x, y, stroke(hexc("555555"), 6))
    for k in range(3):
        a = t * 9 + k * 2.094
        cv.save(); cv.translate(x, y); cv.scale(1, 0.25); cv.rotate(math.degrees(a))
        rrect(cv, 0, -18, 180, 36, 18, fill(hexc("8d6e63")))
        cv.restore()
    cv.drawCircle(x, y, 20, fill(hexc("5d4037")))


def packet(cv, x, y, s=1.0):
    cv.save(); cv.translate(x, y); cv.scale(s, s)
    rrect(cv, -60, -40, 120, 80, 6, fill(hexc("f5f0e1")))
    rrect(cv, -60, -40, 120, 80, 6, stroke(hexc("bdb39a"), 2))
    for k in range(5):
        rrect(cv, -50 + k * 21, -14, 16, 30, 8, fill(hexc("e57373")))
        rrect(cv, -50 + k * 21, -14, 16, 15, 8, fill(hexc("fff176")))
    text(cv, "AMOXICILLIN", 0, -22, 13, hexc("333333"), align="center")
    cv.restore()


def scene3(cv, t):
    ho, lv, sw = BEAT["handover"], BEAT["leave"], BEAT["swallow"]
    if t < ho:
        pharmacy_wide(cv, t, phase="ask")
    elif t < S["s3b"]["start"] - 0.1:
        handover_closeup(cv, t)
    elif t < lv:
        pharmacy_wide(cv, t, phase="leave")
    else:
        home_swallow(cv, t)
    if t < 45.4:
        fade(cv, (45.4 - t) / 0.4 * 0.8, skia.ColorWHITE)


def pharmacy_wide(cv, t, phase):
    z = keys(t, [(45, 1.0), (46.5, 1.08)]) if phase == "ask" else 1.0
    with Cam(cv, 960, 560, z):
        shelves(cv)
        fan(cv, 960, 70, t)
        ph.draw(cv, 560, 1060, 0.95, mouth=0.0, blink=blink_at(t, 5), smile=0.5, look=(0.8, 0), turn=0.3,
                rh=(120, -470) if phase == "ask" else None)
        counter(cv, 200, 720, 760)
        if phase == "ask":
            p1 = dict(mouth=talking("s1", t), blink=blink_at(t, 1), sick=0.35, brow="worried", look=(-0.8, 0), turn=-0.3,
                      lh=(-10, -478))
            s1.draw(cv, 1180, 1050, 0.92, **p1)
            s2.draw(cv, 1480, 1060, 0.9, blink=blink_at(t, 2), smile=0.7, look=(-0.8, 0), turn=-0.4)
        else:
            u = ease(t, S["s3b"]["start"], BEAT["leave"])
            x1 = lerp(1180, 1700, u)
            x2 = lerp(1450, 2000, u)
            walking = u > 0.02
            s2.draw(cv, x2, 1060, 0.9, mouth=talking("s2", t), blink=blink_at(t, 2), smile=0.9, brow="up",
                    look=(-0.6, 0), legs="walk" if walking else "stand", phase=t * 8,
                    rh=(40 + wobble(t, 2, 30), -640), ritem=lambda c, x, y: packet(c, x, y - 40, 0.8))
            s1.draw(cv, x1, 1050, 0.92, mouth=talking("s1", t), blink=blink_at(t, 1), smile=0.6, sick=0.25,
                    look=(0.6, 0), legs="walk" if walking else "stand", phase=t * 8 + 1)
    vignette(cv, 0.2)


def handover_closeup(cv, t):
    ho = BEAT["handover"]
    u = ease(t, ho + 0.15, S["s3b"]["start"] - 0.5)
    with Cam(cv, 960, 540, keys(t, [(ho, 1.0), (ho + 2, 1.08)])):
        cv.drawRect(skia.Rect.MakeWH(W, H), lin((0, 0), (0, H), [hexc("c9d6cc"), hexc("9fb0a3")]))
        cv.drawRect(skia.Rect.MakeXYWH(0, 640, W, 440), fill(hexc("7b5236")))
        cv.drawRect(skia.Rect.MakeXYWH(0, 640, W, 20), fill(hexc("9c6b45")))
        # pharmacist hand (coat sleeve) from left
        hx = lerp(560, 900, u)
        cv.drawLine(-100, 700, hx - 60, 760, stroke(hexc("f4f7f9"), 120))
        packet(cv, hx + 90, 730, 2.8)
        ellipse(cv, hx, 770, 70, 50, fill(hexc("9c6644")))
        # boy's hand reaching from right
        bx = lerp(1700, 1260, u)
        cv.drawLine(2100, 700, bx + 60, 780, stroke(hexc("a86f4c"), 90))
        ellipse(cv, bx, 780, 66, 46, fill(hexc("a86f4c")))
    # ominous tint + caution tag
    fade(cv, 0.22 * ease(t, ho, ho + 0.6), hexc("2a0a0a"))
    a = ease(t, ho + 0.4, ho + 0.8)
    rrect(cv, 60, 60, 520, 70, 14, fill(alpha(hexc("b71c1c"), 0.85 * a)))
    text(cv, "No prescription asked!", 320, 108, 38, alpha(skia.ColorWHITE, a), align="center")
    vignette(cv, 0.4)


def home_swallow(cv, t):
    lv, sw, dv = BEAT["leave"], BEAT["swallow"], BEAT["dive"]
    z = keys(t, [(lv, 1.0), (dv, 1.25), (60.0, 9.0)])
    with Cam(cv, 960, keys(t, [(lv, 560.0), (dv, 500.0), (60.0, 452.0)]), z):
        cv.drawRect(skia.Rect.MakeWH(W, H), lin((0, 0), (0, H), [hexc("f6e7c8"), hexc("e8d2a8")]))
        rrect(cv, 1250, 140, 420, 320, 10, fill(hexc("a9d8f5")))
        rrect(cv, 1250, 140, 420, 320, 10, stroke(hexc("8d6e52"), 14))
        cv.drawLine(1460, 140, 1460, 460, stroke(hexc("8d6e52"), 8))
        rrect(cv, 150, 780, 700, 40, 8, fill(hexc("8d6e52")))
        rrect(cv, 220, 700, 60, 80, 8, fill(alpha(hexc("bbdefb"), 0.8)))
        drinking = sw < t
        glass = lambda c, x, y: (rrect(c, x - 26, y - 70, 52, 80, 8, fill(alpha(hexc("bbdefb"), 0.85))),
                                 rrect(c, x - 22, y - 30, 44, 36, 6, fill(alpha(hexc("64b5f6"), 0.8))))
        pose = dict(blink=blink_at(t, 1), sick=0.35, smile=0.2, look=(0, 0), mouth=0.0)
        if t < sw:
            pose.update(rh=(40, -560), mouth=0.5 if t > sw - 0.4 else 0.0,
                        ritem=lambda c, x, y: rrect(c, x - 8, y - 22, 16, 30, 8, fill(hexc("e57373"))))
        else:
            pose.update(rh=(30, -600), ritem=glass, tilt=-8, look=(0, -0.6), mouth=0.15)
        s1.draw(cv, 960, 1160, 1.1, **pose)
    if t > dv - 0.2:
        u = ease(t, dv - 0.2, 60.0)
        cv.drawRect(skia.Rect.MakeWH(W, H), rad((W / 2, H / 2), W * (0.2 + 1.2 * u),
                    [alpha(hexc("7a0b1e"), u), alpha(hexc("c2185b"), u * 0.8), alpha(hexc("2a0010"), u)]))
