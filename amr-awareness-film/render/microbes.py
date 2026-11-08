"""Microscopic cast: bacteria (sensitive / beneficial / resistant / boss), red
blood cells, amoxicillin molecules, virus, burst effect."""
import math
import skia
from gfx import fill, stroke, rad, lin, ellipse, path, hexc, alpha, shade, clamp, rrect, blurred, glow

KINDS = {
    "sensitive":  dict(body=hexc("5bb8f2"), body2=hexc("6fd6a8"), size=(46, 30), pili=False),
    "beneficial": dict(body=hexc("2fbfa8"), body2=hexc("7ccf6a"), size=(62, 26), pili=False, heart=True),
    "resistant":  dict(body=hexc("c2185b"), body2=hexc("7b1fa2"), size=(80, 40), pili=True, capsule=True),
    "boss":       dict(body=hexc("9c1458"), body2=hexc("5e1a8a"), size=(150, 74), pili=True, capsule=True),
}


def bacterium(cv, x, y, kind, t=0.0, sc=1.0, rot=0.0, mouth=0.0, mood="happy", squash=0.0,
              look=(0, 0), hand=None, alpha_=1.0, var=0, wilt=0.0, split=0.0):
    k = KINDS[kind]
    rx, ry = k["size"]
    col = k["body"] if var % 2 == 0 else k["body2"]
    if wilt:
        col = _desat(col, wilt)
    cv.save()
    cv.translate(x, y)
    cv.rotate(rot)
    cv.scale(sc * (1 + squash), sc * (1 - squash))
    if alpha_ < 1:
        cv.saveLayerAlpha(None, int(255 * clamp(alpha_)))
    # flagellum
    if kind in ("resistant", "boss", "beneficial"):
        fl = skia.Path()
        fl.moveTo(-rx, 0)
        for i in range(1, 9):
            fl.lineTo(-rx - i * rx * 0.16, math.sin(t * 9 + i * 0.9) * ry * 0.35)
        cv.drawPath(fl, stroke(hexc("e2b23f") if kind == "boss" else shade(col, -0.25), 6 if kind == "boss" else 3))
    # pili
    if k.get("pili"):
        for i in range(14):
            a = i / 14 * 2 * math.pi
            px, py = math.cos(a) * rx, math.sin(a) * ry
            cv.drawLine(px, py, px * 1.22, py * 1.3, stroke(shade(col, -0.3), 3 if kind == "boss" else 2))
    # capsule glow
    if k.get("capsule"):
        rrect(cv, -rx - 10, -ry - 10, 2 * rx + 20, 2 * ry + 20, ry + 10, fill(alpha(hexc("ff6ad5"), 0.22)))
    split_gap = split * rx * 0.9
    for sgn in ((0,) if split <= 0 else (-1, 1)):
        cv.save()
        cv.translate(sgn * split_gap, 0)
        w = rx if split <= 0 else rx * (1 - 0.35 * split)
        rrect(cv, -w, -ry, 2 * w, 2 * ry, ry, lin((0, -ry), (0, ry), [shade(col, 0.28), col, shade(col, -0.25)]))
        rrect(cv, -w, -ry, 2 * w, 2 * ry, ry, stroke(shade(col, -0.35), 3))
        rrect(cv, -w + 6, -ry + 6, 2 * w - 12, 2 * ry - 12, ry - 6, stroke(alpha(skia.ColorWHITE, 0.25), 2))
        ellipse(cv, -w * 0.35, -ry * 0.45, w * 0.35, ry * 0.18, fill(alpha(skia.ColorWHITE, 0.35)))
        cv.restore()
    if split <= 0.05:
        _face(cv, rx, ry, kind, mood, mouth, look, t, wilt)
    if k.get("heart") and wilt < 0.9:
        hx, hy = rx * 0.55, -ry * 0.1
        a = 0.8 * (1 - wilt)
        cv.drawPath(path([("M", hx, hy + 6), ("C", hx - 10, hy - 2, hx - 6, hy - 12, hx, hy - 6),
                          ("C", hx + 6, hy - 12, hx + 10, hy - 2, hx, hy + 6), ("Z",)]), fill(alpha(hexc("ff8fb1"), a)))
    if hand:
        hx, hy = hand
        cv.drawLine(rx * 0.3, ry * 0.4, hx, hy, stroke(shade(col, -0.2), 10))
        cv.drawCircle(hx, hy, 12, fill(shade(col, 0.1)))
    if alpha_ < 1:
        cv.restore()
    cv.restore()


def _desat(c, u):
    r, g, b = (c >> 16) & 255, (c >> 8) & 255, c & 255
    m = (r + g + b) / 3
    f = lambda v: int(v + (m * 0.8 - v) * u)
    return skia.Color(f(r), f(g), f(b))


def _face(cv, rx, ry, kind, mood, mouth, look, t, wilt):
    big = kind == "boss"
    es = ry * (0.30 if not big else 0.26)
    ex = rx * (0.22 if kind != "beneficial" else 0.18)
    ey = -ry * 0.18
    villain = kind in ("resistant", "boss")
    for sg in (-1, 1):
        cx = sg * ex + rx * 0.12
        ellipse(cv, cx, ey, es, es * 1.15, fill(hexc("fffdf5")))
        px, py = cx + look[0] * es * 0.35, ey + look[1] * es * 0.35
        cv.drawCircle(px, py, es * 0.55, fill(hexc("1b0b14")))
        cv.drawCircle(px - es * 0.2, py - es * 0.22, es * 0.18, fill(skia.ColorWHITE))
        if villain:  # heavy lids + brows
            if mood != "scared":
                cv.save()
                cv.clipRect(skia.Rect.MakeLTRB(cx - es * 1.2, ey - es * 1.3, cx + es * 1.2, ey - es * 0.25))
                ellipse(cv, cx, ey, es * 1.05, es * 1.2, fill(shade(KINDS[kind]["body"], -0.15)))
                cv.restore()
            by = ey - es * 1.25
            inner = by + (es * 0.5 if mood in ("evil", "menace") else es * 0.2)
            cv.drawLine(cx + sg * es * 0.95, by - es * 0.25, cx - sg * es * 0.55, inner, stroke(hexc("2a0a1c"), es * 0.35))
        elif wilt > 0.3:
            cv.drawLine(cx - es, ey - es * 1.3, cx + es, ey - es * 1.1 + sg * es * 0.3, stroke(hexc("1b3a4a"), es * 0.2))
    my = ry * 0.38
    mw = rx * (0.32 if not big else 0.36)
    if mouth > 0.06:
        h = ry * (0.12 + 0.42 * mouth)
        mp = path([("M", -mw + rx * 0.12, my - 2), ("Q", rx * 0.12, my - 8, mw + rx * 0.12, my - 2),
                   ("Q", rx * 0.12, my + h * 2, -mw + rx * 0.12, my - 2), ("Z",)])
        cv.drawPath(mp, fill(hexc("3a0418")))
        if villain:
            cv.save(); cv.clipPath(mp, doAntiAlias=True)
            for i in range(5):  # jagged teeth
                tx = -mw + rx * 0.12 + (i + 0.5) * (2 * mw / 5)
                cv.drawPath(path([("M", tx - mw / 5, my - 4), ("L", tx, my + ry * 0.12), ("L", tx + mw / 5, my - 4), ("Z",)]),
                            fill(hexc("fff8e8")))
            cv.restore()
    else:
        curve = {"happy": 0.35, "evil": 0.5, "menace": 0.15, "sad": -0.3, "scared": -0.2}.get(mood, 0.3)
        if wilt > 0.3:
            curve = -0.3
        cv.drawPath(path([("M", -mw + rx * 0.12, my), ("Q", rx * 0.12, my + ry * curve, mw + rx * 0.12, my)]),
                    stroke(hexc("2a0a1c") if villain else hexc("12384a"), 4 if not big else 7))


def rbc(cv, x, y, r, rot=0.0, a=1.0):
    cv.save()
    cv.translate(x, y)
    cv.rotate(rot)
    cv.scale(1.0, 0.82)
    cv.drawCircle(0, 0, r, rad((-r * 0.3, -r * 0.3), r * 1.3, [alpha(hexc("ff4d4d"), a), alpha(hexc("c41616"), a), alpha(hexc("7d0a0a"), a)]))
    cv.drawCircle(0, 0, r * 0.5, fill(alpha(hexc("8f0d0d"), 0.55 * a)))
    cv.drawCircle(-r * 0.35, -r * 0.4, r * 0.18, fill(alpha(skia.ColorWHITE, 0.18 * a)))
    cv.restore()


def wbc(cv, x, y, r, t):
    pth = skia.Path()
    for i in range(25):
        a = i / 24 * 2 * math.pi
        rr = r * (1 + 0.08 * math.sin(a * 5 + t * 2))
        (pth.moveTo if i == 0 else pth.lineTo)(x + math.cos(a) * rr, y + math.sin(a) * rr)
    pth.close()
    cv.drawPath(pth, rad((x - r * 0.3, y - r * 0.3), r * 1.3, [hexc("fbf6ff"), hexc("d9cdea")]))
    for i in range(3):
        cv.drawCircle(x + math.cos(i * 2.1) * r * 0.3, y + math.sin(i * 2.1) * r * 0.3, r * 0.22, fill(hexc("a58fc7")))


def amoxicillin(cv, x, y, s=1.0, rot=0.0, a=1.0, cut=0.0):
    """Glowing beta-lactam style molecule: a 4-ring fused to a 5-ring."""
    cv.save()
    cv.translate(x, y)
    cv.rotate(rot)
    cv.scale(s, s)
    glow(cv, 0, 0, 46, hexc("fff59d"), 0.45 * a)
    col = alpha(hexc("fff3b0"), a)
    edge = alpha(hexc("e0a800"), a)
    sq = [(-22, -12), (-2, -12), (-2, 8), (-22, 8)]
    pent = [(-2, -12), (16, -20), (30, -4), (20, 14), (-2, 8)]
    off = cut * 18
    for pts, dx in ((sq, -off), (pent, off)):
        pth = skia.Path()
        pth.moveTo(pts[0][0] + dx, pts[0][1])
        for q in pts[1:]:
            pth.lineTo(q[0] + dx, q[1])
        pth.close()
        cv.drawPath(pth, fill(alpha(hexc("fffbe0"), 0.55 * a)))
        cv.drawPath(pth, stroke(edge, 4))
    cv.drawCircle(-22 - off, -12, 4, fill(col))
    cv.drawLine(-22 - off, 8, -30 - off, 18, stroke(edge, 3))
    cv.restore()


def scissors(cv, x, y, s, t):
    """Beta-lactamase enzyme as tiny snipping scissors."""
    cv.save()
    cv.translate(x, y)
    cv.scale(s, s)
    o = 0.35 + 0.35 * math.sin(t * 18)
    for sg in (-1, 1):
        cv.save()
        cv.rotate(sg * o * 30)
        cv.drawLine(0, 0, 34, 0, stroke(hexc("e7d6ff"), 6))
        cv.drawCircle(-10, sg * 8, 8, stroke(hexc("b388ff"), 4))
        cv.restore()
    cv.restore()


def virus(cv, x, y, r, t, mood="happy"):
    for i in range(14):
        a = i / 14 * 2 * math.pi + t * 0.3
        cv.drawLine(x + math.cos(a) * r, y + math.sin(a) * r, x + math.cos(a) * r * 1.35, y + math.sin(a) * r * 1.35,
                    stroke(hexc("8e7cc3"), 6))
        cv.drawCircle(x + math.cos(a) * r * 1.38, y + math.sin(a) * r * 1.38, 8, fill(hexc("b4a7d6")))
    cv.drawCircle(x, y, r, rad((x - r * 0.3, y - r * 0.3), r * 1.3, [hexc("c9bde8"), hexc("7d6aa8")]))
    for sg in (-1, 1):
        cv.drawCircle(x + sg * r * 0.3, y - r * 0.12, r * 0.16, fill(skia.ColorWHITE))
        cv.drawCircle(x + sg * r * 0.3, y - r * 0.1, r * 0.08, fill(hexc("1d1530")))
    cv.drawPath(path([("M", x - r * 0.3, y + r * 0.3), ("Q", x, y + r * 0.55, x + r * 0.3, y + r * 0.3)]), stroke(hexc("1d1530"), 5))


def burst(cv, x, y, u, col, seed=0):
    """Bacterium popping: expanding ring + flying fragments, u in 0..1."""
    if u <= 0 or u >= 1:
        return
    a = 1 - u
    cv.drawCircle(x, y, 20 + 90 * u, stroke(alpha(col, 0.8 * a), 6 * a + 1))
    for i in range(9):
        ang = i / 9 * 2 * math.pi + seed
        d = 30 + 110 * u
        cv.drawCircle(x + math.cos(ang) * d, y + math.sin(ang) * d, 9 * a + 2, fill(alpha(col, a)))
    glow(cv, x, y, 70 * (1 - u * 0.5), skia.ColorWHITE, 0.5 * a)
