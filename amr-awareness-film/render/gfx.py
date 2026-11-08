"""Drawing helpers on top of skia-python."""
import math
import skia

W, H = 1920, 1080
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FONT_SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
_TF = {}


def tf(path):
    if path not in _TF:
        _TF[path] = skia.Typeface.MakeFromFile(path)
    return _TF[path]


# ---------- maths / easing ----------
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def lerp(a, b, u):
    return a + (b - a) * u


def smooth(u):
    u = clamp(u)
    return u * u * (3 - 2 * u)


def ease(t, t0, t1):
    """0..1 smooth ramp from t0 to t1."""
    if t1 <= t0:
        return 1.0 if t >= t1 else 0.0
    return smooth((t - t0) / (t1 - t0))


def keys(t, kf):
    """Piecewise smooth interpolation through [(t, value_or_tuple), ...]."""
    if t <= kf[0][0]:
        return kf[0][1]
    for (t0, v0), (t1, v1) in zip(kf, kf[1:]):
        if t < t1:
            u = smooth((t - t0) / (t1 - t0))
            if isinstance(v0, tuple):
                return tuple(lerp(a, b, u) for a, b in zip(v0, v1))
            return lerp(v0, v1, u)
    return kf[-1][1]


def hexc(h, a=255):
    h = h.lstrip("#")
    return skia.Color(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def mix(c1, c2, u):
    return skia.Color(*(int(lerp(getattr_c(c1, i), getattr_c(c2, i), u)) for i in range(4)))


def getattr_c(c, i):
    # skia Color is ARGB int
    return [(c >> 16) & 255, (c >> 8) & 255, c & 255, (c >> 24) & 255][i]


def shade(c, f):
    """Lighten (f>0) or darken (f<0) a colour."""
    r, g, b, a = (getattr_c(c, i) for i in range(4))
    if f >= 0:
        r, g, b = (int(lerp(x, 255, f)) for x in (r, g, b))
    else:
        r, g, b = (int(x * (1 + f)) for x in (r, g, b))
    return skia.Color(r, g, b, a)


def alpha(c, a):
    return (c & 0x00FFFFFF) | (int(clamp(a, 0, 1) * 255) << 24)


# ---------- paints ----------
def fill(c, aa=True):
    return skia.Paint(Color=c, AntiAlias=aa, Style=skia.Paint.kFill_Style)


def stroke(c, w, cap=skia.Paint.kRound_Cap):
    return skia.Paint(Color=c, AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w,
                      StrokeCap=cap, StrokeJoin=skia.Paint.kRound_Join)


def lin(p0, p1, colors, pos=None):
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(*p0), skia.Point(*p1)], colors, pos))
    return p


def rad(c, r, colors, pos=None):
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial(skia.Point(*c), max(r, 0.1), colors, pos))
    return p


def blurred(paint, sigma):
    paint.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, sigma))
    return paint


# ---------- shapes ----------
def rrect(cv, x, y, w, h, r, paint):
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r), paint)


def ellipse(cv, cx, cy, rx, ry, paint):
    cv.drawOval(skia.Rect.MakeLTRB(cx - rx, cy - ry, cx + rx, cy + ry), paint)


def poly(cv, pts, paint, close=True):
    p = skia.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    if close:
        p.close()
    cv.drawPath(p, paint)


def path(cmds):
    """Build a path from [('M',x,y),('L',x,y),('Q',cx,cy,x,y),('C',...),('Z',)]."""
    p = skia.Path()
    for c in cmds:
        k = c[0]
        if k == "M":
            p.moveTo(c[1], c[2])
        elif k == "L":
            p.lineTo(c[1], c[2])
        elif k == "Q":
            p.quadTo(c[1], c[2], c[3], c[4])
        elif k == "C":
            p.cubicTo(c[1], c[2], c[3], c[4], c[5], c[6])
        elif k == "Z":
            p.close()
    return p


def soft_shadow(cv, cx, cy, rx, ry, a=0.28):
    ellipse(cv, cx, cy, rx, ry, blurred(fill(skia.Color(0, 0, 0, int(255 * a))), max(rx, ry) * 0.18))


def glow(cv, cx, cy, r, c, a=0.5):
    cv.drawCircle(cx, cy, r, rad((cx, cy), r, [alpha(c, a), alpha(c, 0)]))


# ---------- text ----------
def text(cv, s, x, y, size, c, font=FONT_SANS_BOLD, align="left"):
    f = skia.Font(tf(font), size)
    w = f.measureText(s)
    if align == "center":
        x -= w / 2
    elif align == "right":
        x -= w
    cv.drawString(s, x, y, f, fill(c))
    return w


def text_width(s, size, font=FONT_SANS_BOLD):
    return skia.Font(tf(font), size).measureText(s)


# ---------- camera ----------
class Cam:
    """Usage: with Cam(cv, cx, cy, zoom): draw world (1920x1080 design space)."""

    def __init__(self, cv, cx=W / 2, cy=H / 2, zoom=1.0, rot=0.0):
        self.cv, self.cx, self.cy, self.z, self.rot = cv, cx, cy, zoom, rot

    def __enter__(self):
        cv = self.cv
        cv.save()
        cv.translate(W / 2, H / 2)
        if self.rot:
            cv.rotate(self.rot)
        cv.scale(self.z, self.z)
        cv.translate(-self.cx, -self.cy)
        return self

    def __exit__(self, *a):
        self.cv.restore()


def vignette(cv, strength=0.45):
    cv.drawRect(skia.Rect.MakeWH(W, H), rad((W / 2, H / 2), W * 0.75,
                [skia.Color(0, 0, 0, 0), skia.Color(0, 0, 0, 0), skia.Color(0, 0, 0, int(255 * strength))], [0, 0.55, 1]))


def fade(cv, a, c=skia.ColorBLACK):
    if a > 0:
        cv.drawRect(skia.Rect.MakeWH(W, H), fill(alpha(c, a)))


def rng(seed):
    """Tiny deterministic pseudo-random generator (frame-independent)."""
    x = [seed * 2654435761 % 4294967296 or 1]

    def r(a=0.0, b=1.0):
        x[0] = (1103515245 * x[0] + 12345) % 2147483648
        return a + (b - a) * x[0] / 2147483648
    return r


def wobble(t, f=1.0, a=1.0, ph=0.0):
    return math.sin(t * f * 2 * math.pi + ph) * a
