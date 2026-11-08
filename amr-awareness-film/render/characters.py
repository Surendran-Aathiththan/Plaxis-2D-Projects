"""Cartoon character rig: people (parametric), bicycles, phone."""
import math
import skia
from gfx import (fill, stroke, lin, rad, rrect, ellipse, poly, path, soft_shadow, shade,
                 hexc, alpha, blurred, clamp, lerp, text, FONT_SANS_BOLD, FONT_REG)

# ---------------- character specs (locked designs) ----------------
STUDENT1 = dict(skin=hexc("a86f4c"), hair=hexc("15110f"), hair_style="part", shirt=hexc("f7f7f2"),
                trousers=hexc("efefe8"), tie=hexc("7a1730"), tie2=hexc("d9a521"), crest=True,
                shoes=hexc("1b1b1b"), bag=hexc("1f2f5c"), height=1.0, width=0.95)
STUDENT2 = dict(skin=hexc("8a5636"), hair=hexc("120e0c"), hair_style="curly", shirt=hexc("f7f7f2"),
                trousers=hexc("efefe8"), tie=hexc("7a1730"), tie2=hexc("d9a521"), crest=True, loose_tie=True,
                shoes=hexc("1b1b1b"), bag=hexc("b3261e"), height=0.98, width=1.12, cheeks=True)
PHARMACIST = dict(skin=hexc("9c6644"), hair=hexc("1a1512"), hair_style="short", shirt=hexc("a9cdee"),
                  trousers=hexc("3b3f4a"), coat=True, coat_len=0.55, glasses="rect", moustache=True,
                  shoes=hexc("2a1d14"), height=1.12, width=1.05, badge=True, long_sleeve=True)
MOTHER = dict(skin=hexc("a3694a"), hair=hexc("17120f"), hair_style="bun", saree=hexc("8a1c2b"),
              border=hexc("e0b13a"), blouse=hexc("6e1220"), pottu=True, chain=True,
              shoes=hexc("6b3e22"), height=1.04, width=1.0, female=True)
PHYSICIAN = dict(skin=hexc("94603f"), hair=hexc("6d6a68"), hair_style="salt", shirt=hexc("9fc6ea"),
                 trousers=hexc("2f3440"), tie=hexc("1f3a68"), coat=True, coat_len=0.95, glasses="rimless",
                 stethoscope=True, badge=True, shoes=hexc("1a1a1a"), height=1.16, width=1.05, long_sleeve=True)
MICRO = dict(skin=hexc("8f5b3b"), hair=hexc("141110"), hair_style="short", shirt=hexc("8c9198"),
             trousers=hexc("2b2f38"), coat=True, coat_len=0.95, glasses="square", beard=True,
             lanyard=hexc("2364c8"), badge=True, shoes=hexc("1a1a1a"), height=1.14, width=1.0, long_sleeve=True)
GOWN = dict(gown=hexc("8fc3e6"))


def _dir(a_deg, sgn):
    a = math.radians(a_deg)
    return sgn * math.sin(a), math.cos(a)


def ik(p0, p1, l1, l2, bend_sign):
    """Two-bone IK: returns joint position between p0 and p1."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    d = max(1e-3, math.hypot(dx, dy))
    d2 = min(d, l1 + l2 - 1e-3)
    a = (l1 * l1 - l2 * l2 + d2 * d2) / (2 * d2)
    h = math.sqrt(max(0.0, l1 * l1 - a * a))
    ux, uy = dx / d, dy / d
    mx, my = p0[0] + ux * a, p0[1] + uy * a
    return mx - uy * h * bend_sign, my + ux * h * bend_sign


class Person:
    def __init__(self, spec):
        self.s = dict(spec)

    # pose keys: mouth, blink, look(dx,dy), tilt, turn, brow, smile, la, ra (arm angles
    # (shoulder, elbow)) or lh/rh hand targets, lean, legs ('stand'|'walk'|'none'|('ik', lf, rf)),
    # phase, sick, sweat, upper_only, scale
    def draw(self, cv, x, y, sc=1.0, **p):
        s = self.s
        hgt, wid = s.get("height", 1.0), s.get("width", 1.0)
        leg = 250 * hgt if not s.get("female") else 250 * hgt
        torso_h, torso_w = 225 * hgt, 168 * wid
        cv.save()
        cv.translate(x, y)
        cv.scale(sc, sc)
        if not p.get("no_shadow") and not p.get("upper_only"):
            soft_shadow(cv, 0, 4, 120 * wid, 22)
        cv.rotate(p.get("lean", 0.0))
        bob = p.get("bob", 0.0)
        hip_y = -leg + bob
        sh_y = hip_y - torso_h + 22
        neck_y = hip_y - torso_h
        head_y = neck_y - 92
        legs = p.get("legs", "stand")
        pants = s.get("trousers", hexc("333333"))
        if s.get("gown"):
            pants = s["gown"]
        # ---- legs ----
        if not p.get("upper_only") and legs != "none":
            l1, l2 = leg * 0.52, leg * 0.5
            hips = [(-torso_w * 0.22, hip_y), (torso_w * 0.22, hip_y)]
            if legs == "stand":
                feet = [(-torso_w * 0.24, -8), (torso_w * 0.24, -8)]
                hips = [(-torso_w * 0.24, hip_y), (torso_w * 0.24, hip_y)]
            elif legs == "walk":
                ph = p.get("phase", 0.0)
                feet = []
                for k, sg in enumerate((1, -1)):
                    sw = math.sin(ph + k * math.pi)
                    feet.append((hips[k][0] + sw * 38, -8 - max(0, math.cos(ph + k * math.pi)) * 16))
            else:  # ('ik', left_foot, right_foot) in local coords
                feet = [legs[1], legs[2]]
            for k in (0, 1):
                hx, hy = hips[k]
                fx, fy = feet[k]
                if legs == "stand":
                    kx, ky = (hx + fx) / 2, (hy + fy) / 2
                else:
                    kx, ky = ik((hx, hy), (fx, fy), l1, l2, -1)
                if s.get("saree"):
                    continue
                pw = 50 * wid
                cv.drawPath(path([("M", hx, hy), ("L", kx, ky), ("L", fx, fy - 6)]), stroke(shade(pants, -0.08), pw))
                cv.drawPath(path([("M", hx, hy), ("L", kx, ky), ("L", fx, fy - 6)]), stroke(pants, pw * 0.82))
                ellipse(cv, fx + 10 * (1 if k else -1), fy + 2, 34, 15, fill(s.get("shoes", hexc("222222"))))
                ellipse(cv, fx + 4 * (1 if k else -1), fy - 3, 18, 5, fill(alpha(skia.ColorWHITE, 0.15)))
        # ---- saree skirt ----
        if s.get("saree") and not p.get("upper_only"):
            sar, bd = s["saree"], s["border"]
            sk = path([("M", -torso_w * 0.42, hip_y - 10), ("L", torso_w * 0.42, hip_y - 10),
                       ("Q", torso_w * 0.6, -leg * 0.4, torso_w * 0.62, -4), ("L", -torso_w * 0.62, -4),
                       ("Q", -torso_w * 0.6, -leg * 0.4, -torso_w * 0.42, hip_y - 10), ("Z",)])
            cv.drawPath(sk, lin((0, hip_y), (0, 0), [shade(sar, 0.08), shade(sar, -0.15)]))
            for k in range(-3, 4):  # pleats
                cv.drawLine(k * 16, hip_y + 40, k * 26, -10, stroke(alpha(shade(sar, -0.3), 0.45), 3))
            rrect(cv, -torso_w * 0.62, -34, torso_w * 1.24, 30, 4, fill(bd))
            rrect(cv, -torso_w * 0.62, -26, torso_w * 1.24, 6, 2, fill(shade(bd, -0.25)))
            for k in (-1, 1):
                ellipse(cv, k * 30, -4, 26, 9, fill(s.get("shoes")))
        # ---- coat tails (behind legs top) ----
        coat = s.get("coat")
        # ---- torso ----
        shirt = s.get("gown") or s.get("blouse") or s.get("shirt", hexc("ffffff"))
        tor = path([("M", -torso_w / 2, sh_y + 10), ("Q", -torso_w / 2 - 6, neck_y + 2, -torso_w * 0.2, neck_y),
                    ("L", torso_w * 0.2, neck_y), ("Q", torso_w / 2 + 6, neck_y + 2, torso_w / 2, sh_y + 10),
                    ("L", torso_w * 0.46, hip_y + 12), ("Q", 0, hip_y + 22, -torso_w * 0.46, hip_y + 12), ("Z",)])
        if coat:
            cl = s.get("coat_len", 0.9)
            ct = path([("M", -torso_w / 2 - 8, sh_y + 6), ("Q", -torso_w / 2 - 10, neck_y, -torso_w * 0.2, neck_y - 2),
                       ("L", torso_w * 0.2, neck_y - 2), ("Q", torso_w / 2 + 10, neck_y, torso_w / 2 + 8, sh_y + 6),
                       ("L", torso_w * 0.56, hip_y + leg * cl * 0.62), ("L", -torso_w * 0.56, hip_y + leg * cl * 0.62), ("Z",)])
            if not p.get("upper_only"):
                cv.drawPath(ct, lin((-torso_w / 2, 0), (torso_w / 2, 0), [hexc("e9eef2"), hexc("ffffff"), hexc("d5dde4")]))
        cv.drawPath(tor, lin((-torso_w / 2, sh_y), (torso_w / 2, hip_y), [shade(shirt, 0.12), shirt, shade(shirt, -0.14)]))
        if s.get("gown"):
            for gx in range(-3, 4):
                for gy in range(0, 5):
                    cv.drawCircle(gx * 22, neck_y + 30 + gy * 40, 3, fill(alpha(skia.ColorWHITE, 0.5)))
        # collar
        if not s.get("saree") and not s.get("gown"):
            col = shade(s.get("shirt", hexc("ffffff")), -0.04)
            poly(cv, [(-4, neck_y + 4), (-38, neck_y - 4), (-30, neck_y + 26)], fill(col))
            poly(cv, [(4, neck_y + 4), (38, neck_y - 4), (30, neck_y + 26)], fill(col))
            poly(cv, [(-4, neck_y + 4), (-38, neck_y - 4), (-30, neck_y + 26)], stroke(alpha(skia.ColorBLACK, 0.15), 2))
            poly(cv, [(4, neck_y + 4), (38, neck_y - 4), (30, neck_y + 26)], stroke(alpha(skia.ColorBLACK, 0.15), 2))
            if not coat:  # buttons
                for k in range(4):
                    cv.drawCircle(0, neck_y + 40 + k * 44, 3.5, fill(alpha(skia.ColorBLACK, 0.18)))
        # tie
        if s.get("tie"):
            off = 8 if s.get("loose_tie") else 0
            tp = path([("M", -9, neck_y + 8 + off), ("L", 9, neck_y + 8 + off), ("L", 14, neck_y + 120),
                       ("L", 0, neck_y + 140), ("L", -14, neck_y + 120), ("Z",)])
            cv.drawPath(tp, fill(s["tie"]))
            if s.get("tie2"):
                cv.save(); cv.clipPath(tp, doAntiAlias=True)
                for k in range(-2, 8):
                    cv.drawLine(-20, neck_y + 10 + k * 22, 20, neck_y - 6 + k * 22, stroke(s["tie2"], 5))
                cv.restore()
            ellipse(cv, 0, neck_y + 10 + off, 11, 9, fill(shade(s["tie"], -0.15)))
        if s.get("crest") and not coat:
            rrect(cv, torso_w * 0.12, neck_y + 52, 38, 34, 4, fill(alpha(skia.ColorBLACK, 0.06)))
            poly(cv, [(torso_w * 0.12 + 10, neck_y + 56), (torso_w * 0.12 + 28, neck_y + 56),
                      (torso_w * 0.12 + 28, neck_y + 70), (torso_w * 0.12 + 19, neck_y + 80), (torso_w * 0.12 + 10, neck_y + 70)],
                 fill(hexc("7a1730")))
        # backpack straps
        if s.get("bag") and not p.get("no_bag"):
            for k in (-1, 1):
                cv.drawLine(k * torso_w * 0.32, neck_y + 4, k * torso_w * 0.36, hip_y - 10, stroke(s["bag"], 16))
        # saree pallu over torso
        if s.get("saree"):
            sar, bd = s["saree"], s["border"]
            pl = path([("M", torso_w * 0.36, neck_y + 2), ("L", torso_w * 0.56, sh_y + 16), ("L", -torso_w * 0.2, hip_y + 4),
                       ("L", -torso_w * 0.48, hip_y - 20), ("Z",)])
            cv.drawPath(pl, lin((torso_w / 2, neck_y), (-torso_w / 2, hip_y), [shade(sar, 0.1), shade(sar, -0.1)]))
            cv.drawLine(torso_w * 0.56, sh_y + 16, -torso_w * 0.2, hip_y + 4, stroke(bd, 12))
        # coat front panels + lapels
        if coat:
            cl = s.get("coat_len", 0.9)
            bottom = hip_y + (leg * cl * 0.62 if not p.get("upper_only") else 30)
            for sg in (-1, 1):
                pan = path([("M", sg * torso_w * 0.18, neck_y), ("L", sg * (torso_w / 2 + 9), sh_y + 6),
                            ("L", sg * torso_w * 0.56, bottom), ("L", sg * torso_w * 0.12, bottom),
                            ("L", sg * torso_w * 0.1, neck_y + 120), ("Z",)])
                cv.drawPath(pan, lin((sg * torso_w * 0.1, 0), (sg * torso_w * 0.56, 0), [hexc("ffffff"), hexc("e3e9ee")]))
                cv.drawPath(pan, stroke(alpha(hexc("8a99a8"), 0.5), 2))
                lap = path([("M", sg * torso_w * 0.18, neck_y - 2), ("L", sg * torso_w * 0.36, neck_y + 10),
                            ("L", sg * torso_w * 0.26, neck_y + 40), ("L", sg * torso_w * 0.11, neck_y + 120), ("Z",)])
                cv.drawPath(lap, fill(hexc("eef2f5")))
                cv.drawPath(lap, stroke(alpha(hexc("8a99a8"), 0.6), 2))
                if not p.get("upper_only"):
                    rrect(cv, sg * torso_w * 0.42 - (36 if sg > 0 else 0), hip_y + 10, 36, 30, 4, stroke(alpha(hexc("8a99a8"), 0.6), 2))
            rrect(cv, -torso_w * 0.36, neck_y + 64, 36, 26, 3, stroke(alpha(hexc("8a99a8"), 0.6), 2))
            if s.get("lanyard"):
                cv.drawPath(path([("M", -26, neck_y + 4), ("L", -4, neck_y + 96), ("L", 26, neck_y + 4)]),
                            stroke(s["lanyard"], 6, skia.Paint.kButt_Cap))
                rrect(cv, -22, neck_y + 92, 40, 54, 4, fill(hexc("ffffff")))
                rrect(cv, -22, neck_y + 92, 40, 54, 4, stroke(hexc("9aa7b4"), 2))
                rrect(cv, -14, neck_y + 100, 24, 22, 2, fill(hexc("c8a17e")))
                rrect(cv, -16, neck_y + 128, 30, 4, 1, fill(hexc("2364c8")))
            elif s.get("badge"):
                bx = torso_w * 0.2
                rrect(cv, bx, neck_y + 70, 42, 54, 4, fill(hexc("ffffff")))
                rrect(cv, bx, neck_y + 70, 42, 54, 4, stroke(hexc("9aa7b4"), 2))
                rrect(cv, bx + 8, neck_y + 78, 26, 22, 2, fill(hexc("c8a17e")))
                rrect(cv, bx + 6, neck_y + 106, 30, 5, 1, fill(hexc("1f3a68")))
            if s.get("stethoscope"):
                cv.drawPath(path([("M", -30, neck_y - 2), ("C", -60, neck_y + 40, -50, neck_y + 120, -30, neck_y + 150)]),
                            stroke(hexc("33373d"), 7))
                cv.drawPath(path([("M", 30, neck_y - 2), ("C", 60, neck_y + 40, 52, neck_y + 100, 40, neck_y + 120)]),
                            stroke(hexc("33373d"), 7))
                cv.drawCircle(-30, neck_y + 158, 13, fill(hexc("c9cfd6")))
                cv.drawCircle(-30, neck_y + 158, 7, fill(hexc("8a929b")))
        # ---- neck ----
        rrect(cv, -22, neck_y - 26, 44, 40, 14, fill(shade(s["skin"], -0.12)))
        if s.get("chain"):
            cv.drawPath(path([("M", -26, neck_y - 2), ("Q", 0, neck_y + 26, 26, neck_y - 2)]), stroke(hexc("e2b23f"), 3))
        # ---- arms ----
        sleeve = shirt if not coat else hexc("f4f7f9")
        if s.get("saree"):
            sleeve = s["blouse"]
        for side, sg in (("l", -1), ("r", 1)):
            shx = sg * (torso_w / 2 - 6)
            shy = sh_y + 14
            ua, fa = 112 * hgt, 104 * hgt
            tgt = p.get(side + "h")
            if tgt is not None:
                ex, ey = ik((shx, shy), tgt, ua, fa, 1 if sg < 0 else -1)
                hx, hy = tgt
                if p.get(side + "flip"):
                    ex, ey = ik((shx, shy), tgt, ua, fa, -1 if sg < 0 else 1)
            else:
                a, e = p.get(side + "a", (8, 10))
                dx, dy = _dir(a, sg)
                ex, ey = shx + dx * ua, shy + dy * ua
                dx2, dy2 = _dir(a - e, sg)
                hx, hy = ex + dx2 * fa, ey + dy2 * fa
            aw = 36 * wid
            long = s.get("long_sleeve") or coat
            cv.drawPath(path([("M", shx, shy), ("L", ex, ey)]), stroke(shade(sleeve, -0.12), aw + 4))
            cv.drawPath(path([("M", shx, shy), ("L", ex, ey)]), stroke(sleeve, aw))
            if long:
                cv.drawPath(path([("M", ex, ey), ("L", hx, hy)]), stroke(shade(sleeve, -0.12), aw + 2))
                cv.drawPath(path([("M", ex, ey), ("L", lerp(ex, hx, 0.85), lerp(ey, hy, 0.85))]), stroke(sleeve, aw - 2))
            else:
                mx, my = lerp(shx, ex, 0.55), lerp(shy, ey, 0.55)
                cv.drawPath(path([("M", mx, my), ("L", ex, ey), ("L", hx, hy)]), stroke(shade(s["skin"], -0.1), aw * 0.78))
                cv.drawPath(path([("M", mx, my), ("L", ex, ey), ("L", hx, hy)]), stroke(s["skin"], aw * 0.66))
            cv.drawCircle(hx, hy, 19 * wid, fill(shade(s["skin"], -0.05)))
            cv.drawCircle(hx - 4, hy - 4, 8, fill(alpha(skia.ColorWHITE, 0.12)))
            item = p.get(side + "item")
            if item:
                item(cv, hx, hy)
        # ---- head ----
        self.head(cv, 0, head_y, p)
        cv.restore()

    def head(self, cv, cx, cy, p):
        s = self.s
        skin = s["skin"]
        sick = p.get("sick", 0.0)
        if sick:
            skin = lerp_color(skin, hexc("b7a58f"), sick * 0.45)
        tilt = p.get("tilt", 0.0)
        turn = p.get("turn", 0.0)
        cv.save()
        cv.translate(cx, cy + 60)
        cv.rotate(tilt)
        cv.translate(0, -60)
        rx, ry = 80, 90
        fx = turn * 18  # facial feature shift for 3/4 look
        hair = s["hair"]
        # back hair / bun
        if s["hair_style"] == "bun":
            cv.drawCircle(-turn * 30, -78, 34, fill(shade(hair, 0.05)))
            ellipse(cv, 0, -10, rx + 8, ry + 6, fill(hair))
        # ears
        for sg in (-1, 1):
            ex = sg * (rx - 4) - turn * 10
            ellipse(cv, ex, 8, 15, 22, fill(shade(skin, -0.08)))
            ellipse(cv, ex, 8, 8, 13, fill(shade(skin, -0.2)))
        # face
        ellipse(cv, 0, 0, rx, ry, rad((-24 + fx, -30), rx * 1.35, [shade(skin, 0.14), skin, shade(skin, -0.16)], [0, 0.55, 1]))
        if s.get("beard"):
            bp = path([("M", -rx + 6, 10), ("Q", -rx + 4, 70, 0 + fx, 92), ("Q", rx - 4, 70, rx - 6, 10),
                       ("Q", rx - 14, 50, 30 + fx, 52), ("Q", fx, 44, -30 + fx, 52), ("Q", -rx + 14, 50, -rx + 6, 10), ("Z",)])
            cv.drawPath(bp, fill(alpha(hair, 0.85)))
        if s.get("cheeks"):
            for sg in (-1, 1):
                ellipse(cv, sg * 46 + fx, 32, 16, 9, fill(alpha(hexc("d9534f"), 0.22)))
        if sick:
            for sg in (-1, 1):
                ellipse(cv, sg * 32 + fx, 20, 18, 7, fill(alpha(hexc("6b4a52"), 0.35 * sick)))
        # eyes
        look = p.get("look", (0.0, 0.0))
        blink = p.get("blink", 0.0)
        for sg in (-1, 1):
            exx, eyy = sg * 30 + fx, -4
            ellipse(cv, exx, eyy, 17, 20, fill(hexc("fbfaf7")))
            ix, iy = exx + look[0] * 6 + turn * 3, eyy + look[1] * 6 + 2
            cv.drawCircle(ix, iy, 11, fill(hexc("4a2c1a")))
            cv.drawCircle(ix, iy, 6, fill(hexc("120a06")))
            cv.drawCircle(ix - 4, iy - 4, 3.5, fill(skia.ColorWHITE))
            lid = blink if not sick else max(blink, 0.35 * sick)
            if lid > 0:
                cv.save()
                cv.clipRect(skia.Rect.MakeLTRB(exx - 20, eyy - 22, exx + 20, eyy - 22 + 44 * lid))
                ellipse(cv, exx, eyy, 18, 21, fill(shade(skin, -0.04)))
                cv.restore()
                cv.drawLine(exx - 16, eyy - 20 + 42 * lid, exx + 16, eyy - 20 + 42 * lid, stroke(shade(skin, -0.35), 2.5))
            ellipse(cv, exx, eyy, 17, 20, stroke(alpha(shade(skin, -0.5), 0.5), 2))
        # brows
        brow = p.get("brow", "neutral")
        bw = 6 if not s.get("female") else 4
        bcol = shade(hair, -0.1) if s["hair_style"] != "salt" else hexc("4a4644")
        for sg in (-1, 1):
            inner, outer = -34, -36
            if brow == "worried":
                inner, outer = -44, -32
            elif brow == "up":
                inner, outer = -46, -46
            elif brow == "angry":
                inner, outer = -26, -42
            elif brow == "sly":
                inner, outer = (-28, -40) if sg < 0 else (-44, -50)
            ix, ox = sg * 12 + fx, sg * 48 + fx
            cv.drawPath(path([("M", ix, inner), ("Q", (ix + ox) / 2, min(inner, outer) - 7, ox, outer)]), stroke(bcol, bw))
        # glasses
        g = s.get("glasses")
        if g:
            gc = hexc("1c1c1c") if g != "rimless" else alpha(hexc("9aa0a6"), 0.9)
            gw = 4 if g != "rimless" else 2
            for sg in (-1, 1):
                ex = sg * 30 + fx
                if g == "rect":
                    rrect(cv, ex - 24, -24, 48, 36, 8, stroke(gc, gw))
                elif g == "square":
                    rrect(cv, ex - 25, -26, 50, 42, 5, stroke(gc, gw + 1))
                else:
                    rrect(cv, ex - 24, -22, 48, 36, 12, stroke(gc, gw))
                cv.drawLine(ex - 24 * -sg + (0 if sg < 0 else 0), -6, sg * (rx - 4) - turn * 10, -2, stroke(gc, 2))
                ellipse(cv, ex - 8, -12, 8, 4, fill(alpha(skia.ColorWHITE, 0.25)))
            cv.drawLine(-6 + fx, -8, 6 + fx, -8, stroke(gc, gw))
        # nose
        cv.drawPath(path([("M", 2 + fx + turn * 6, 4), ("Q", 12 + fx + turn * 8, 26, -2 + fx + turn * 6, 30)]),
                    stroke(shade(skin, -0.28), 3.5))
        # moustache
        if s.get("moustache") or s.get("beard"):
            mp = path([("M", -26 + fx, 44), ("Q", fx, 32, 26 + fx, 44), ("Q", fx, 40, -26 + fx, 44), ("Z",)])
            cv.drawPath(mp, fill(shade(hair, 0.0)))
            cv.drawPath(mp, stroke(shade(hair, 0.0), 6))
        # mouth
        m = clamp(p.get("mouth", 0.0))
        smile = p.get("smile", 0.3)
        my = 54
        if m > 0.06:
            mw, mh = 18 + 10 * m + max(0, smile) * 6, 5 + 20 * m
            mp = path([("M", -mw + fx, my), ("Q", fx, my - 6 - smile * 4, mw + fx, my),
                       ("Q", fx, my + mh * 2 + smile * 4, -mw + fx, my), ("Z",)])
            cv.drawPath(mp, fill(hexc("5a1a1d")))
            cv.save(); cv.clipPath(mp, doAntiAlias=True)
            rrect(cv, -mw + fx, my - 8, mw * 2, 10, 3, fill(hexc("f7f2ea")))
            ellipse(cv, fx, my + mh * 1.6, mw * 0.7, mh * 0.6, fill(hexc("d4636b")))
            cv.restore()
        else:
            w0 = 20 + max(0, smile) * 8
            cv.drawPath(path([("M", -w0 + fx, my - smile * 2), ("Q", fx, my + smile * 16, w0 + fx, my - smile * 2)]),
                        stroke(hexc("5a2a22"), 4))
        if s.get("pottu"):
            cv.drawCircle(fx, -46, 5, fill(hexc("c8102e")))
        # hair front
        self.hair_front(cv, rx, ry, turn, hair)
        # sweat
        if p.get("sweat", 0) > 0:
            for k, (sx, sy) in enumerate(((-62, -30), (60, -10))):
                a = p["sweat"]
                dp = path([("M", sx, sy), ("Q", sx + 8, sy + 14, sx, sy + 18), ("Q", sx - 8, sy + 14, sx, sy), ("Z",)])
                cv.drawPath(dp, fill(alpha(hexc("bfe6ff"), 0.85 * a)))
        cv.restore()

    def hair_front(self, cv, rx, ry, turn, hair):
        st = self.s["hair_style"]
        hl = shade(hair, 0.22)
        if st == "part":
            hp = path([("M", -rx - 4, 8), ("C", -rx - 14, -70, -40, -ry - 22, 10, -ry - 16),
                       ("C", 60, -ry - 12, rx + 12, -60, rx + 4, 6), ("Q", rx - 6, -40, 40, -52),
                       ("Q", -20, -40, -46, -66 + 4), ("Q", -60, -40, -rx + 8, -10), ("Z",)])
            cv.drawPath(hp, lin((0, -ry), (0, 0), [hl, hair]))
            cv.drawPath(path([("M", -38, -74), ("Q", 10, -98, 50, -78)]), stroke(alpha(skia.ColorWHITE, 0.18), 4))
        elif st == "curly":
            cv.drawPath(path([("M", -rx - 2, 6), ("C", -rx - 10, -80, rx + 10, -80, rx + 2, 6), ("Q", rx - 10, -40, 0, -50),
                              ("Q", -rx + 10, -40, -rx - 2, 6), ("Z",)]), fill(hair))
            pts = [(-74, -26), (-70, -58), (-48, -82), (-18, -96), (16, -98), (46, -86), (68, -62), (76, -30),
                   (-40, -60), (-6, -70), (30, -64), (54, -48)]
            for k, (hx, hy) in enumerate(pts):
                cv.drawCircle(hx, hy, 24 if k < 8 else 20, fill(hair))
                cv.drawCircle(hx - 6, hy - 7, 7, fill(alpha(hl, 0.7)))
        elif st in ("short", "salt"):
            col = hair
            hp = path([("M", -rx - 2, 0), ("C", -rx - 8, -80, -30, -ry - 14, 4, -ry - 12),
                       ("C", 50, -ry - 10, rx + 8, -70, rx + 2, 0), ("Q", rx - 8, -46, 30, -60),
                       ("Q", 0, -66, -34, -60), ("Q", -rx + 8, -46, -rx - 2, 0), ("Z",)])
            cv.drawPath(hp, lin((0, -ry), (0, 0), [shade(col, 0.2), col]))
            if st == "salt":
                for k in range(7):
                    a = -2.5 + k * 0.32
                    cv.drawLine(math.cos(a) * 62, math.sin(a) * 74 - 6, math.cos(a + 0.12) * 74, math.sin(a + 0.12) * 86 - 6,
                                stroke(alpha(hexc("eeeeea"), 0.35), 4))
        elif st == "bun":
            hp = path([("M", -rx - 4, 10), ("C", -rx - 8, -80, -10, -ry - 14, 0, -ry - 8),
                       ("C", 10, -ry - 14, rx + 8, -80, rx + 4, 10), ("Q", rx - 6, -40, 4, -70),
                       ("Q", -rx + 6, -40, -rx - 4, 10), ("Z",)])
            cv.drawPath(hp, lin((0, -ry), (0, 0), [hl, hair]))
            cv.drawLine(0, -ry - 6, 2, -70, stroke(shade(hair, -0.4), 2))


def lerp_color(c1, c2, u):
    a = [(c1 >> 16) & 255, (c1 >> 8) & 255, c1 & 255]
    b = [(c2 >> 16) & 255, (c2 >> 8) & 255, c2 & 255]
    r = [int(lerp(x, y, u)) for x, y in zip(a, b)]
    return skia.Color(r[0], r[1], r[2], (c1 >> 24) & 255)


def blink_at(t, seed=0):
    """Natural blinking: returns lid closure 0..1."""
    period = 3.1 + (seed % 5) * 0.37
    ph = (t + seed * 0.71) % period
    return max(0.0, 1 - abs(ph - 0.08) / 0.08) if ph < 0.16 else 0.0


# ---------------- bicycle ----------------
def bicycle(cv, x, y, sc, color, dist, bell=False):
    """Side-view bicycle with ground contact at (x, y). Returns key points in world coords."""
    r = 92
    cv.save()
    cv.translate(x, y)
    cv.scale(sc, sc)
    rear, front = (-150, -r), (150, -r)
    bb = (-10, -r + 8)
    seat = (-58, -r - 150)
    head = (110, -r - 150)
    ang = dist / r
    for wx, wy in (rear, front):
        cv.drawCircle(wx, wy, r, stroke(hexc("1d1d1d"), 14))
        cv.drawCircle(wx, wy, r - 9, stroke(hexc("9aa0a6"), 3))
        for k in range(12):
            a = ang + k * math.pi / 6
            cv.drawLine(wx, wy, wx + math.cos(a) * (r - 9), wy + math.sin(a) * (r - 9), stroke(alpha(hexc("c9ced3"), 0.8), 1.6))
        cv.drawCircle(wx, wy, 8, fill(hexc("7b8187")))
    fc = stroke(color, 13)
    for a_, b_ in ((rear, bb), (bb, seat), (seat, rear), (bb, head), (seat, (head[0] - 12, head[1] + 14)), (head, front)):
        cv.drawLine(a_[0], a_[1], b_[0], b_[1], fc)
    cv.drawLine(seat[0], seat[1], seat[0] - 6, seat[1] - 30, stroke(hexc("444444"), 9))
    rrect(cv, seat[0] - 40, seat[1] - 44, 70, 18, 9, fill(hexc("222222")))
    cv.drawLine(head[0], head[1], head[0] - 8, head[1] - 46, stroke(hexc("555555"), 9))
    cv.drawLine(head[0] - 8, head[1] - 46, head[0] - 46, head[1] - 52, stroke(hexc("333333"), 9))
    if bell:
        cv.drawCircle(head[0] - 26, head[1] - 60, 9, fill(hexc("d8d8d8")))
    # crank & pedals
    ca = dist / 60.0
    pedals = []
    for k in (0, 1):
        a = ca + k * math.pi
        px, py = bb[0] + math.cos(a) * 40, bb[1] + math.sin(a) * 40
        cv.drawLine(bb[0], bb[1], px, py, stroke(hexc("6c7075"), 7))
        rrect(cv, px - 16, py - 5, 32, 10, 3, fill(hexc("2b2b2b")))
        pedals.append((px, py))
    cv.drawCircle(bb[0], bb[1], 20, stroke(hexc("6c7075"), 4))
    cv.restore()
    to_w = lambda q: (x + q[0] * sc, y + q[1] * sc)
    return dict(seat=to_w((seat[0] - 4, seat[1] - 40)), bar=to_w((head[0] - 46, head[1] - 52)),
                pedals=[to_w(q) for q in pedals])


def rider(cv, person, bike_pts, sc, pose, near_pedal=0):
    """Draw a person seated on a bike (pose: head/arm/mouth keys)."""
    sx, sy = bike_pts["seat"]
    # place person so that hips sit on seat: hip is at -leg*height from feet
    hgt = person.s.get("height", 1.0)
    leg = 250 * hgt
    ox, oy = sx, sy + leg * sc
    to_l = lambda q: ((q[0] - ox) / sc, (q[1] - oy) / sc)
    lf, rf = to_l(bike_pts["pedals"][near_pedal]), to_l(bike_pts["pedals"][1 - near_pedal])
    bar = to_l(bike_pts["bar"])
    p = dict(pose)
    p.setdefault("lh", bar)
    p.setdefault("rh", (bar[0] + 10, bar[1] + 4))
    p["legs"] = ("ik", lf, rf)
    p["lean"] = 8
    p["no_shadow"] = True
    person.draw(cv, ox, oy, sc, **p)


# ---------------- phone ----------------
def phone(cv, x, y, w, h, typed="", reply="", reply_a=0.0, scale_text=1.0):
    rrect(cv, x - 8, y - 8, w + 16, h + 16, 46, fill(hexc("15171a")))
    rrect(cv, x, y, w, h, 38, lin((x, y), (x, y + h), [hexc("f3f6fa"), hexc("e6ecf3")]))
    rrect(cv, x + w / 2 - 60, y + 14, 120, 26, 13, fill(hexc("15171a")))
    rrect(cv, x, y + 54, w, 90, 0, fill(hexc("ffffff")))
    cv.drawCircle(x + 70, y + 99, 28, fill(hexc("10a37f")))
    text(cv, "AI", x + 70, y + 110, 28, skia.ColorWHITE, align="center")
    text(cv, "AI Chat Assistant", x + 116, y + 108, 30, hexc("222222"))
    fs = 34 * scale_text
    if typed:
        lines = wrap(typed, fs, w - 170)
        bh = 30 + len(lines) * fs * 1.25
        rrect(cv, x + 110, y + 190, w - 140, bh, 26, fill(hexc("2f7bf6")))
        for k, ln in enumerate(lines):
            text(cv, ln, x + 136, y + 190 + 18 + fs + k * fs * 1.25, fs, skia.ColorWHITE, font=FONT_REG)
    if reply and reply_a > 0:
        lines = wrap(reply, fs, w - 170)
        top = y + 440
        bh = 30 + len(lines) * fs * 1.25
        rrect(cv, x + 30, top, w - 140, bh, 26, fill(alpha(hexc("ffffff"), reply_a)))
        rrect(cv, x + 30, top, w - 140, bh, 26, stroke(alpha(hexc("f0b429"), reply_a), 4))
        for k, ln in enumerate(lines):
            text(cv, ln, x + 56, top + 18 + fs + k * fs * 1.25, fs, alpha(hexc("1d1d1d"), reply_a), font=FONT_SANS_BOLD)
    rrect(cv, x + 24, y + h - 100, w - 48, 64, 32, fill(hexc("ffffff")))
    rrect(cv, x + 24, y + h - 100, w - 48, 64, 32, stroke(hexc("c9d2dc"), 2))


def wrap(s, size, maxw):
    from gfx import text_width
    words, lines, cur = s.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if text_width(trial, size, FONT_REG) > maxw and cur:
            lines.append(cur)
            cur = wd
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines
