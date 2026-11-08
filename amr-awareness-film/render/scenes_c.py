"""Scenes 5-7: hospital admission, the doctors, final message and end card."""
import math
import skia
from gfx import *
from characters import Person, STUDENT1, MOTHER, PHYSICIAN, MICRO, GOWN, blink_at
from microbes import bacterium, amoxicillin, virus, burst, rbc
from timing import S, BEAT, talking

s1 = Person(STUDENT1)
patient = Person(dict(STUDENT1, **GOWN, tie=None, crest=False, bag=None))
mom, phys, micro = Person(MOTHER), Person(PHYSICIAN), Person(MICRO)

AST = [("AMX", "Amoxicillin", "R"), ("AMC", "Co-amoxiclav", "R"), ("CRO", "Ceftriaxone", "R"),
       ("CIP", "Ciprofloxacin", "R"), ("MEM", "Meropenem", "S"), ("AK", "Amikacin", "S")]


# ---------------- sets ----------------
def ward_bg(cv, t):
    cv.drawRect(skia.Rect.MakeXYWH(-200, -200, W + 400, 1000), lin((0, 0), (0, 800), [hexc("e3f1ef"), hexc("cfe5e1")]))
    cv.drawRect(skia.Rect.MakeXYWH(-200, 780, W + 400, 600), lin((0, 780), (0, H), [hexc("d9dfe2"), hexc("b9c3c8")]))
    for k in range(-2, 24):
        cv.drawLine(k * 110, 780, k * 160 - 600, H + 200, stroke(alpha(hexc("9aa6ad"), 0.35), 2))
    cv.drawRect(skia.Rect.MakeXYWH(-200, 760, W + 400, 22), fill(hexc("9fb8b4")))
    rrect(cv, 1380, 140, 380, 300, 8, fill(hexc("bfe3f5")))
    rrect(cv, 1380, 140, 380, 300, 8, stroke(hexc("ffffff"), 14))
    cv.drawLine(1570, 140, 1570, 440, stroke(hexc("ffffff"), 8))
    for k in range(6):  # curtain
        cv.drawRect(skia.Rect.MakeXYWH(40 + k * 40, 60, 40, 700), fill(hexc("9fd3c7" if k % 2 else "8ec9bc")))
    cv.drawLine(20, 60, 300, 60, stroke(hexc("8a99a8"), 8))


def bed(cv, x, y, t, patient_pose=None, sit=0.0):
    rrect(cv, x - 380, y - 40, 760, 60, 12, fill(hexc("8a99a8")))
    rrect(cv, x - 400, y - 330, 30, 360, 10, fill(hexc("9aa7b4")))
    rrect(cv, x + 370, y - 230, 30, 260, 10, fill(hexc("9aa7b4")))
    rrect(cv, x - 370, y - 120, 740, 90, 20, fill(hexc("f7fbff")))
    for wx in (x - 330, x + 330):
        cv.drawCircle(wx, y + 50, 22, fill(hexc("3d4650")))
    rrect(cv, x - 360, y - 210 - sit * 30, 200, 110, 40, fill(hexc("ffffff")))
    pp = dict(patient_pose or {})
    patient.draw(cv, x - 190, y + 180 - sit * 10, 0.82, upper_only=True, **pp)
    # blanket
    bl = path([("M", x - 300, y - 150), ("Q", x, y - 200, x + 370, y - 150), ("L", x + 370, y - 30), ("L", x - 300, y - 30), ("Z",)])
    cv.drawPath(bl, lin((0, y - 200), (0, y), [hexc("a5c8e8"), hexc("7fa6cf")]))
    cv.drawLine(x - 300, y - 150, x + 370, y - 150, stroke(hexc("ffffff"), 10))


def monitor(cv, x, y, t):
    cv.drawLine(x, y + 120, x, y + 520, stroke(hexc("8a99a8"), 10))
    rrect(cv, x - 120, y - 80, 240, 200, 14, fill(hexc("2b3138")))
    rrect(cv, x - 104, y - 64, 208, 150, 6, fill(hexc("061a10")))
    pth = skia.Path()
    for i in range(80):
        px = x - 100 + i * 2.5
        ph = (i * 0.05 - t * 1.2) % 1.0
        py = y + 10 - (60 if 0.0 < ph < 0.03 else -20 if 0.03 < ph < 0.06 else 0)
        (pth.moveTo if i == 0 else pth.lineTo)(px, py)
    cv.drawPath(pth, stroke(hexc("33ff88"), 3))
    text(cv, "HR 118", x + 20, y + 72, 26, hexc("ffd54f"))


def iv_stand(cv, x, y):
    cv.drawLine(x, y, x, y - 520, stroke(hexc("9aa7b4"), 8))
    cv.drawLine(x - 50, y - 520, x + 50, y - 520, stroke(hexc("9aa7b4"), 8))
    rrect(cv, x + 10, y - 510, 60, 100, 14, fill(alpha(hexc("e3f2fd"), 0.9)))
    rrect(cv, x + 16, y - 470, 48, 56, 10, fill(alpha(hexc("90caf9"), 0.8)))
    cv.drawPath(path([("M", x + 40, y - 410), ("Q", x - 60, y - 200, x - 280, y - 230)]), stroke(alpha(hexc("e3f2fd"), 0.9), 4))


def report(cv, x, y, w, h, hl=0.0):
    rrect(cv, x, y, w, h, 12, fill(hexc("ffffff")))
    rrect(cv, x, y, w, 80, 12, fill(hexc("1f3a68")))
    text(cv, "MICROBIOLOGY REPORT", x + 30, y + 52, 34, skia.ColorWHITE)
    text(cv, "Specimen: Blood culture", x + 30, y + 125, 28, hexc("333333"), font=FONT_REG)
    text(cv, "Isolate: Bacterium (multi-drug resistant)", x + 30, y + 165, 28, hexc("b71c1c"))
    text(cv, "Antibiotic susceptibility", x + 30, y + 220, 28, hexc("1f3a68"))
    for k, (code, name, res) in enumerate(AST):
        ry = y + 250 + k * 52
        if res == "S" and hl > 0:
            rrect(cv, x + 20, ry - 2, w - 40, 48, 8, fill(alpha(hexc("c8e6c9"), hl)))
        text(cv, name, x + 40, ry + 34, 28, hexc("222222"), font=FONT_REG)
        col = hexc("c62828") if res == "R" else hexc("2e7d32")
        rrect(cv, x + w - 130, ry + 4, 80, 38, 8, fill(col))
        text(cv, res, x + w - 90, ry + 34, 28, skia.ColorWHITE, align="center")


def ast_plate(cv, x, y, r, t, grow=1.0):
    cv.drawCircle(x, y, r + 14, fill(alpha(hexc("e8eef2"), 0.9)))
    cv.drawCircle(x, y, r, rad((x - r * 0.3, y - r * 0.3), r * 1.4, [hexc("e9c97a"), hexc("caa24f")]))
    rr = rng(3)
    for _ in range(int(160 * grow)):  # bacterial lawn
        a, d = rr(0, 6.28), math.sqrt(rr(0, 1)) * r * 0.95
        cv.drawCircle(x + math.cos(a) * d, y + math.sin(a) * d, rr(3, 7), fill(alpha(hexc("f3e3b5"), 0.8)))
    for k, (code, name, res) in enumerate(AST):
        a = k / len(AST) * 2 * math.pi - math.pi / 2
        dx, dy = x + math.cos(a) * r * 0.58, y + math.sin(a) * r * 0.58
        zone = (r * 0.3 if res == "S" else r * 0.06) * grow
        cv.drawCircle(dx, dy, zone + 18, fill(alpha(hexc("d9b866"), 0.95)))
        cv.drawCircle(dx, dy, 18, fill(hexc("ffffff")))
        text(cv, code, dx, dy + 6, 14, hexc("333333"), align="center")


def corridor(cv):
    cv.drawRect(skia.Rect.MakeXYWH(-300, -300, W + 600, H + 600), lin((0, 0), (0, H), [hexc("f4f8fa"), hexc("dfe8ec")]))
    vx, vy = 960, 470
    poly(cv, [(-300, H + 300), (W + 300, H + 300), (vx + 160, vy + 160), (vx - 160, vy + 160)], fill(hexc("cfd9de")))
    for k in range(-8, 9):
        cv.drawLine(vx + k * 20, vy + 160, vx + k * 260, H + 300, stroke(alpha(hexc("aab7bf"), 0.45), 2))
    for side in (-1, 1):
        for k in range(3):
            d = 1 - k * 0.3
            x0 = vx + side * (240 + 520 * d)
            rrect(cv, x0 - 60 * d, vy - 260 * d + 120, 120 * d, 360 * d, 6, fill(hexc("b8d4e3")))
    for k in range(4):
        y = 40 + k * 70
        rrect(cv, vx - 300 + k * 60, y, 600 - k * 120, 20, 10, fill(alpha(hexc("ffffff"), 0.9)))


# ---------------- Scene 5 ----------------
def scene5(cv, t):
    if t < 101.3:
        return calendar(cv, t)
    if t < 102.3:
        return sick_bed(cv, t)
    if t < BEAT["ward"]:
        return hospital_arrival(cv, t)
    if t < BEAT["lab_montage"]:
        return ward_scene(cv, t)
    return lab_montage(cv, t)


def calendar(cv, t):
    cv.drawRect(skia.Rect.MakeWH(W, H), lin((0, 0), (0, H), [hexc("f3e3c3"), hexc("e3cc9f")]))
    with Cam(cv, 960, 540, keys(t, [(100, 1.0), (101.3, 1.08)])):
        rrect(cv, 660, 180, 600, 720, 16, fill(hexc("ffffff")))
        rrect(cv, 660, 180, 600, 150, 16, fill(hexc("c62828")))
        text(cv, "NOVEMBER", 960, 280, 72, skia.ColorWHITE, align="center")
        day = 12 + min(3, int((t - 100) / 0.36))
        u = ((t - 100) / 0.36) % 1.0 if day < 15 else 1.0
        text(cv, str(day + (1 if u >= 1 else 0)), 960, 700, 300, hexc("222222"), align="center")
        if day < 15:
            cv.save()
            cv.translate(960, 340)
            cv.scale(1, max(0.0, 1 - u * 1.4))
            cv.translate(-960, -340)
            rrect(cv, 660, 340, 600, 560, 10, fill(hexc("fafafa")))
            text(cv, str(day), 960, 700, 300, hexc("222222"), align="center")
            cv.restore()
        for k in range(8):
            cv.drawCircle(720 + k * 68, 190, 12, fill(hexc("555555")))
    vignette(cv, 0.3)
    if t < 100.35:
        fade(cv, 1 - (t - 100) / 0.35)


def sick_bed(cv, t):
    with Cam(cv, 900, 560, keys(t, [(101.3, 1.25), (102.3, 1.35)])):
        cv.drawRect(skia.Rect.MakeXYWH(-200, -200, W + 400, H + 400), lin((0, 0), (0, H), [hexc("d8c8a8"), hexc("b7a27e")]))
        rrect(cv, 1300, 160, 360, 280, 8, fill(hexc("6b7d99")))
        sh = wobble(t, 6, 3)
        bed(cv, 960 + sh, 820, t, dict(blink=0.5, sick=1.0, sweat=1.0, brow="worried", smile=-0.5, tilt=-8,
                                       mouth=0.1, la=(10, 120), ra=(10, 120)))
    vignette(cv, 0.45)


def hospital_arrival(cv, t):
    u = ease(t, 102.3, BEAT["ward"])
    with Cam(cv, 960 + u * 60, 540, 1.0):
        cv.drawRect(skia.Rect.MakeXYWH(-200, -200, W + 400, H + 400), lin((0, 0), (0, 700), [hexc("8fc8ef"), hexc("eaf4fb")]))
        cv.drawRect(skia.Rect.MakeXYWH(200, 200, 1600, 520), fill(hexc("f5f7f9")))
        for r_ in range(3):
            for k in range(10):
                rrect(cv, 260 + k * 150, 260 + r_ * 140, 90, 90, 6, fill(hexc("8fb7d6")))
        rrect(cv, 700, 110, 600, 110, 14, fill(hexc("1f3a68")))
        text(cv, "GENERAL HOSPITAL", 1000, 185, 54, skia.ColorWHITE, align="center")
        rrect(cv, 610, 120, 26, 90, 4, fill(hexc("e53935")))
        rrect(cv, 578, 152, 90, 26, 4, fill(hexc("e53935")))
        rrect(cv, 880, 500, 260, 220, 6, fill(hexc("a8d0e6")))
        cv.drawRect(skia.Rect.MakeXYWH(-200, 720, W + 400, 500), fill(hexc("c9cfd3")))
        x = lerp(300, 820, u)
        ph_ = t * 6
        s1.draw(cv, x + 120, 1010, 0.8, legs="walk", phase=ph_, sick=1.0, sweat=0.8, brow="worried", blink=0.4,
                smile=-0.4, tilt=6, lean=4, la=(30, 40), no_bag=True)
        mom.draw(cv, x, 1010, 0.82, legs="walk", phase=ph_ + 1, brow="worried", look=(0.8, 0), turn=0.3,
                 rh=(150, -430), blink=blink_at(t, 4), mouth=talking("mother", t))


def ward_scene(cv, t):
    exam = BEAT["exam"]
    close = t > exam
    cx, cy, z = keys(t, [(BEAT["ward"], (960, 560, 1.0)), (exam - 0.3, (980, 560, 1.05)),
                         (exam, (760, 580, 1.4)), (BEAT["lab_montage"], (760, 580, 1.5))])
    with Cam(cv, cx, cy, z):
        ward_bg(cv, t)
        monitor(cv, 260, 380, t)
        iv_stand(cv, 1060, 900)
        pp = dict(blink=max(0.4, blink_at(t, 1)), sick=1.0, sweat=0.8, brow="worried", smile=-0.4, tilt=-6,
                  la=(8, 10), ra=(8, 10))
        bed(cv, 700, 860, t, pp)
        if not close:
            mom.draw(cv, 1240, 1060, 0.95, brow="worried", mouth=talking("mother", t), look=(0.8, 0), turn=0.4,
                     lh=(-30, -400), rh=(30, -400), blink=blink_at(t, 4),
                     tilt=wobble(t, 2, 2) if talking("mother", t) > 0.1 else 0)
            phys.draw(cv, 1620, 1060, 0.95, mouth=talking("phys", t), look=(-0.8, 0), turn=-0.4, blink=blink_at(t, 6),
                      smile=0.3, brow="neutral", ra=(40, 60) if talking("phys", t) > 0 else (8, 10))
        else:
            # physician examines: stethoscope to chest
            phys.draw(cv, 860, 1100, 1.0, mouth=talking("phys", t), look=(-1, 0.4), turn=-0.5, blink=blink_at(t, 6),
                      smile=0.2, lh=(-250, -520), litem=lambda c, x, y: c.drawCircle(x - 10, y, 16, fill(hexc("c9cfd6"))))
    vignette(cv, 0.3)


def lab_montage(cv, t):
    t0 = BEAT["lab_montage"]
    shots = [t0, t0 + 0.55, t0 + 1.1, t0 + 1.55, 115.0]
    k = sum(1 for s_ in shots[1:] if t >= s_)
    lt = t - shots[min(k, 3)]
    cv.drawRect(skia.Rect.MakeWH(W, H), lin((0, 0), (0, H), [hexc("e8f0f4"), hexc("c9d6de")]))
    with Cam(cv, 960, 540, 1.0 + lt * 0.08):
        if k == 0:   # blood draw
            cv.drawLine(300, 640, 1700, 600, stroke(hexc("a86f4c"), 170))
            rrect(cv, 700, 420, 120, 360, 10, fill(hexc("4a90e2")))
            rrect(cv, 1030, 520, 300, 46, 10, fill(alpha(hexc("eceff1"), 0.95)))
            rrect(cv, 1050, 526, 120 + 80 * clamp(lt / 0.5), 34, 6, fill(hexc("b71c1c")))
            cv.drawLine(1030, 543, 960, 560, stroke(hexc("b0bec5"), 5))
            rrect(cv, 1330, 525, 80, 36, 6, fill(hexc("90a4ae")))
            label_c(cv, "Blood sample", 960, 960)
        elif k == 1:  # culture bottles
            for i, cap in enumerate(("1e88e5", "43a047", "1e88e5", "8e24aa")):
                bx = 560 + i * 260
                rrect(cv, bx, 360, 170, 420, 50, fill(alpha(hexc("e3f2fd"), 0.95)))
                rrect(cv, bx + 10, 520, 150, 250, 40, fill(alpha(hexc("c62828"), 0.55 + 0.1 * i)))
                rrect(cv, bx + 30, 300, 110, 80, 12, fill(hexc(cap)))
                rrect(cv, bx + 20, 560, 130, 110, 6, fill(hexc("ffffff")))
                text(cv, "BLOOD", bx + 85, 600, 24, hexc("333333"), align="center")
                text(cv, "CULTURE", bx + 85, 635, 24, hexc("333333"), align="center")
            label_c(cv, "Blood culture bottles", 960, 960)
        elif k == 2:  # incubator
            rrect(cv, 460, 200, 1000, 700, 20, fill(hexc("eceff1")))
            rrect(cv, 520, 260, 880, 560, 12, fill(hexc("37474f")))
            for r_ in range(3):
                cv.drawLine(540, 420 + r_ * 140, 1380, 420 + r_ * 140, stroke(hexc("90a4ae"), 6))
                for i in range(7):
                    rrect(cv, 560 + i * 115, 340 + r_ * 140, 50, 80, 12, fill(alpha(hexc("e3f2fd"), 0.9)))
            text(cv, "37.0 °C", 1300, 245, 34, hexc("2e7d32"), align="center")
            label_c(cv, "Incubation: bacteria grow", 960, 990)
        else:  # AST plate
            ast_plate(cv, 960, 520, 340, t, grow=clamp(lt / 0.4))
            label_c(cv, "Antibiotic susceptibility test", 960, 980)
    vignette(cv, 0.3)


def label_c(cv, s, x, y):
    y = 110  # keep clear of the subtitles at the bottom
    w = text_width(s, 40) + 50
    rrect(cv, x - w / 2, y - 48, w, 64, 32, fill(alpha(hexc("1f3a68"), 0.85)))
    text(cv, s, x, y - 2, 40, skia.ColorWHITE, align="center")


# ---------------- Scene 6 ----------------
def scene6(cv, t):
    if t < BEAT["micro_walk"]:
        return lab_computer(cv, t)
    if t < BEAT["review"]:
        return consult_room(cv, t, walking=True)
    if t < BEAT["family"]:
        return consult_room(cv, t, walking=False)
    if BEAT["virus_cut"] <= t < S["s6f"]["end"] + 0.15:
        return virus_cut(cv, t)
    if BEAT["bact_cut"] <= t < S["s6h"]["end"] + 0.1:
        return bact_cut(cv, t)
    if BEAT["report_cut"] <= t < S["s6i"]["end"] - 1.2:
        return report_cut(cv, t)
    return bedside_talk(cv, t)


def lab_computer(cv, t):
    with Cam(cv, 960, 540, keys(t, [(115, 1.0), (BEAT["micro_walk"], 1.08)])):
        cv.drawRect(skia.Rect.MakeXYWH(-200, -200, W + 400, H + 400), lin((0, 0), (0, H), [hexc("eef3f6"), hexc("d3dde3")]))
        for k in range(4):
            cv.drawRect(skia.Rect.MakeXYWH(0, 150 + k * 150, 600, 14), fill(hexc("b0bec5")))
            for i in range(6):
                rrect(cv, 30 + i * 95, 90 + k * 150, 50, 60, 10, fill(alpha(hexc(["90caf9", "a5d6a7", "ffe082"][i % 3]), 0.9)))
        micro.draw(cv, 520, 1150, 1.05, mouth=talking("micro", t), look=(1, 0.2), turn=0.5, blink=blink_at(t, 7),
                   brow="neutral", smile=0.1, rh=(160, -500))
        rrect(cv, 760, 760, 1200, 60, 8, fill(hexc("8d6e52")))
        rrect(cv, 1180, 700, 60, 70, 6, fill(hexc("455a64")))
        rrect(cv, 820, 220, 1000, 500, 20, fill(hexc("263238")))
        rrect(cv, 840, 240, 960, 460, 8, fill(hexc("eceff1")))
        ast_plate(cv, 1060, 470, 180, t)
        cv.save(); cv.translate(1280, 250); cv.scale(0.52, 0.52)
        report(cv, 0, 0, 900, 600)
        cv.restore()
    vignette(cv, 0.3)
    if t < 115.3:
        fade(cv, 1 - (t - 115) / 0.3)


def consult_room(cv, t, walking):
    mw, rv = BEAT["micro_walk"], BEAT["review"]
    if walking:
        u = ease(t, mw, mw + 2.2)
        mx = lerp(-100, 760, u)
        cam = (960, 560, 1.0)
    else:
        mx = 760
        cam = keys(t, [(rv, (1010, 520, 1.1)), (BEAT["family"], (1010, 500, 1.3))])
    with Cam(cv, *cam):
        cv.drawRect(skia.Rect.MakeXYWH(-200, -200, W + 400, H + 400), lin((0, 0), (0, H), [hexc("e8eef5"), hexc("cad6e2")]))
        cv.drawRect(skia.Rect.MakeXYWH(-200, 820, W + 400, 500), fill(hexc("a1887f")))
        rrect(cv, 1300, 160, 420, 300, 8, fill(hexc("bfe3f5")))
        rrect(cv, 1300, 160, 420, 300, 8, stroke(hexc("ffffff"), 14))
        rrect(cv, 300, 180, 300, 220, 6, fill(hexc("fafafa")))
        text(cv, "Consultant Physician", 450, 300, 30, hexc("1f3a68"), align="center")
        holding = lambda c, x, y: (c.save(), c.translate(x - 70, y - 120), c.scale(0.16, 0.16), report(c, 0, 0, 900, 900, 0), c.restore())
        talking_p = talking("phys", t)
        phys.draw(cv, 1200, 1060, 0.98, mouth=talking_p, look=(-0.8, 0.3 if not walking else 0), turn=-0.4,
                  blink=blink_at(t, 6), smile=0.2, brow="neutral" if walking else "worried",
                  lh=(-170, -480) if not walking else None)
        micro.draw(cv, mx, 1060, 0.98, mouth=talking("micro", t), look=(0.8, 0.3 if not walking else 0), turn=0.4,
                   blink=blink_at(t, 7), smile=0.1, legs="walk" if walking and mx < 755 else "stand", phase=t * 7,
                   rh=(170, -480), ritem=holding)
        rrect(cv, 400, 860, 1100, 50, 10, fill(hexc("6d4c41")))
    vignette(cv, 0.3)


def bedside_talk(cv, t):
    me = BEAT["micro_explain"]
    micro_in = t >= me
    cam = keys(t, [(BEAT["family"], (900, 520, 1.15)), (me - 0.2, (920, 520, 1.2)), (me, (1000, 520, 1.05)), (155, (1000, 520, 1.12))])
    with Cam(cv, *cam):
        ward_bg(cv, t)
        monitor(cv, 260, 380, t)
        bed(cv, 640, 900, t, dict(blink=0.55, sick=0.7, brow="neutral", smile=0.0, tilt=-6, la=(8, 10), ra=(8, 10)))
        mom.draw(cv, 1060, 1080, 0.98, brow="worried", look=(0.8, 0), turn=0.4, lh=(-30, -400), rh=(30, -400),
                 blink=blink_at(t, 4), mouth=0.0)
        tp = talking("phys", t)
        phys.draw(cv, 1420, 1080, 0.98, mouth=tp, look=(-0.8, 0), turn=-0.4, blink=blink_at(t, 6), smile=0.3,
                  ra=(55 + wobble(t, 0.7, 15), 70) if tp > 0 else (8, 10))
        if micro_in:
            u = ease(t, me, me + 0.8)
            micro.draw(cv, lerp(2100, 1760, u), 1080, 0.98, mouth=talking("micro", t), look=(-0.8, 0), turn=-0.4,
                       blink=blink_at(t, 7), smile=0.2, la=(60 + wobble(t, 0.6, 12), 70) if talking("micro", t) else (8, 10),
                       legs="walk" if u < 1 else "stand", phase=t * 7)
    vignette(cv, 0.3)


def cut_frame(cv, title, col="1f3a68"):
    w = text_width(title, 46) + 60
    rrect(cv, 960 - w / 2, 40, w, 76, 38, fill(alpha(hexc(col), 0.9)))
    text(cv, title, 960, 93, 46, skia.ColorWHITE, align="center")


def virus_cut(cv, t):
    lt = t - BEAT["virus_cut"]
    cv.drawRect(skia.Rect.MakeWH(W, H), rad((W / 2, H / 2), W * 0.7, [hexc("3a2a5c"), hexc("150d26")]))
    virus(cv, 960 + wobble(t, 0.4, 20), 500, 130, t)
    for k in range(8):
        ph = (lt * 0.9 + k / 8) % 1.0
        ang = k / 8 * 2 * math.pi
        d = 520 - 330 * (1 - abs(ph * 2 - 1))  # fly in, bounce back out
        amoxicillin(cv, 960 + math.cos(ang) * d, 500 + math.sin(ang) * d, 1.0, rot=t * 90 + k * 40)
        if abs(ph - 0.5) < 0.05:
            glow(cv, 960 + math.cos(ang) * 200, 500 + math.sin(ang) * 200, 50, skia.ColorWHITE, 0.6)
    text(cv, "VIRUS", 960, 220, 64, hexc("d1c4e9"), align="center")
    cut_frame(cv, "Antibiotics do not work against viruses", "5e35b1")
    vignette(cv, 0.4)


def bact_cut(cv, t):
    lt = t - BEAT["bact_cut"]
    cv.drawRect(skia.Rect.MakeWH(W, H), rad((W / 2, H / 2), W * 0.7, [hexc("8e1b2c"), hexc("2a0410")]))
    for k in range(6):
        x, y = 360 + (k % 3) * 220, 380 + (k // 3) * 240
        tb = 0.5 + k * 0.25
        if lt < tb:
            bacterium(cv, x, y, "sensitive", t, 1.4, var=k, mood="scared" if lt > tb - 0.4 else "happy")
            amoxicillin(cv, lerp(x - 260, x - 40, clamp(lt / tb)), y - 40, 0.9, rot=t * 90)
        else:
            burst(cv, x, y, (lt - tb) / 0.6, hexc("8fd3ff"), k)
    for k in range(3):
        x, y = 1350 + (k % 2) * 220, 330 + k * 200
        bacterium(cv, x, y + wobble(t, 1.5, 8, k), "resistant", t, 1.3, var=k, mood="evil", mouth=0.4 * abs(math.sin(t * 8 + k)))
    text(cv, "Sensitive: killed", 580, 220, 46, hexc("b3e5fc"), align="center")
    text(cv, "Resistant: survive", 1460, 220, 46, hexc("ff80ab"), align="center")
    cut_frame(cv, "Bacteria become resistant, not people", "ad1457")
    vignette(cv, 0.4)


def report_cut(cv, t):
    lt = t - BEAT["report_cut"]
    cv.drawRect(skia.Rect.MakeWH(W, H), lin((0, 0), (0, H), [hexc("eef3f6"), hexc("cfd8dc")]))
    with Cam(cv, 960, 520, 1.0 + lt * 0.03):
        report(cv, 510, 150, 900, 600 + 60, hl=ease(lt, 0.6, 1.2))
        # pen ticks the effective antibiotics
        u = ease(lt, 1.0, 1.8)
        if u > 0:
            for k in (4, 5):
                ry = 150 + 250 + k * 52
                cv.drawPath(path([("M", 1240, ry + 26), ("L", 1256, ry + 40), ("L", 1290, ry + 6)]), stroke(hexc("2e7d32"), 7))
    cut_frame(cv, "Treatment chosen using susceptibility results")


# ---------------- Scene 7 ----------------
def scene7(cv, t):
    sl, ec = BEAT["slogan"], BEAT["endcard"]
    if t >= ec:
        return end_card(cv, t)
    z = keys(t, [(155, 1.0), (sl, 1.12), (ec, 1.16)])
    with Cam(cv, 960, 560, z):
        # blurred background: corridor + patient recovering through the doorway
        bp = skia.Paint(ImageFilter=skia.ImageFilters.Blur(4, 4))
        cv.saveLayer(None, bp)
        corridor(cv)
        rrect(cv, 700, 250, 520, 420, 10, fill(hexc("dcefeb")))
        rrect(cv, 700, 250, 520, 420, 10, stroke(hexc("9fb8b4"), 16))
        cv.save(); cv.clipRect(skia.Rect.MakeXYWH(700, 250, 520, 420))
        cv.translate(960, 600); cv.scale(0.5, 0.5); cv.translate(-700, -760)
        iv_stand(cv, 1060, 900)
        bed(cv, 640, 860, t, dict(blink=blink_at(t, 1), sick=0.1, smile=0.6, brow="neutral", la=(8, 10), ra=(30, 60)), sit=1.0)
        mom.draw(cv, 1150, 1060, 0.9, smile=0.6, look=(-0.8, 0), turn=-0.4, blink=blink_at(t, 4), lh=(-80, -420))
        cv.restore()
        cv.restore()
        cv.restore()
        glow(cv, 960, 300, 700, hexc("fff3d6"), 0.35)
        mp, mm = talking("phys", t), talking("micro", t)
        phys.draw(cv, 740, 1180, 1.12, mouth=mp, look=(0, 0), blink=blink_at(t, 6), smile=0.45,
                  ra=(50 + wobble(t, 0.6, 10), 70) if mp > 0 and t < sl else (8, 10))
        micro.draw(cv, 1180, 1180, 1.1, mouth=mm, look=(0, 0), blink=blink_at(t, 7), smile=0.45,
                   la=(50 + wobble(t, 0.6, 10), 70) if mm > 0 and t < sl else (8, 10))
    if t >= sl:
        slogan(cv, t)
    vignette(cv, 0.25)
    if t < 155.3:
        fade(cv, 1 - (t - 155) / 0.3)


def slogan(cv, t):
    sl = BEAT["slogan"]
    seg = S["s7e"]
    dur = seg["end"] - seg["start"]
    fade(cv, 0.68 * ease(t, sl, sl + 0.4), hexc("06121f"))
    lines = [("USE ANTIBIOTICS WISELY.", "ffffff", 0.0), ("STOP ANTIMICROBIAL RESISTANCE.", "ffd54f", dur * 0.36),
             ("SAVE OUR FUTURE!", "69f0ae", dur * 0.74)]
    for k, (s_, col, dt) in enumerate(lines):
        t0 = sl + dt
        if t < t0:
            continue
        u = ease(t, t0, t0 + 0.35)
        size = 92 if k != 1 else 74
        sc = lerp(1.5, 1.0, u)
        y = 300 + k * 170
        cv.save()
        cv.translate(960, y)
        cv.scale(sc, sc)
        text(cv, s_, 4, 6, size, alpha(skia.ColorBLACK, 0.5 * u), font=FONT_BOLD, align="center")
        text(cv, s_, 0, 0, size, alpha(hexc(col), u), font=FONT_BOLD, align="center")
        cv.restore()
        if t - t0 < 0.3:
            fade(cv, 0.35 * (1 - (t - t0) / 0.3), skia.ColorWHITE)


def end_card(cv, t):
    ec = BEAT["endcard"]
    cv.drawRect(skia.Rect.MakeWH(W, H), lin((0, 0), (W, H), [hexc("0b2a4a"), hexc("0f5c5c")]))
    for k in range(30):
        x = (k * 173 + t * 20) % W
        y = (k * 97) % H
        cv.drawCircle(x, y, 2 + k % 3, fill(alpha(skia.ColorWHITE, 0.15)))
    u = ease(t, ec, ec + 0.8)
    cv.save()
    cv.translate(960, 330)
    cv.rotate(-30)
    cv.scale(lerp(0.6, 1.0, u), lerp(0.6, 1.0, u))
    glow(cv, 0, 0, 220, hexc("80deea"), 0.5 * u)
    rrect(cv, -150, -55, 150, 110, 55, fill(alpha(hexc("ef5350"), u)))
    rrect(cv, 0, -55, 150, 110, 55, fill(alpha(hexc("fafafa"), u)))
    ellipse(cv, -80, -25, 50, 14, fill(alpha(skia.ColorWHITE, 0.35 * u)))
    cv.restore()
    a = ease(t, ec + 0.4, ec + 1.1)
    text(cv, "ANTIMICROBIAL RESISTANCE", 960, 590, 78, alpha(skia.ColorWHITE, a), font=FONT_BOLD, align="center")
    text(cv, "AWARENESS WEEK", 960, 690, 78, alpha(skia.ColorWHITE, a), font=FONT_BOLD, align="center")
    b = ease(t, ec + 1.2, ec + 1.9)
    cv.drawLine(660, 750, 1260, 750, stroke(alpha(hexc("80deea"), b), 4))
    text(cv, "“USE WISELY. PRESERVE THEIR POWER.”", 960, 840, 58, alpha(hexc("ffd54f"), b), align="center")
    if t > 179.2:
        fade(cv, (t - 179.2) / 0.8)
