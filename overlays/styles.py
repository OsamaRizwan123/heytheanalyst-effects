"""Overlays.

  head_stack   white label blocks drop one by one and stack on top of your head (follows your head)
  post_wall    a wall of squares fills in behind you while a counter ticks up ("1,711 POSTS")
  live_cursor  a cursor glides to points and clicks (with a ripple), e.g. to point at a chart
(orbit lives in overlays/orbit/)
"""
import sys, os, math
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from PIL import Image, ImageDraw, ImageFilter
from reelkit.fx import font, blank, fade, W, H, RED, INK, WHITE
from reelkit.style import back, ease

def head_top(mask):
    a = np.asarray(mask.resize((W // 4, H // 4))) > 128
    rows = np.where(a.any(1))[0]
    if len(rows) == 0: return W / 2, H * 0.4
    top = rows[0]; xs = np.where(a[top:top + 25].any(0))[0]
    return float(xs.mean() * 4), float(top * 4)

class HeadStack:
    needs_mask = True; mask_front_only = True
    def __init__(self, start=0.0, end=5.0, labels=("Pareto", "MECE", "SCR", "Driver tree", "2x2 matrix"), small=None, every=0.45):
        self.s, self.e, self.labels, self.every = start, end, list(labels), every
        self.small = small or ["chart", "rule", "story", "tree", "grid"]
        self.blocks = [self._block(l, self.small[i % len(self.small)], (-4, 3, -2, 4, -3)[i % 5]) for i, l in enumerate(self.labels)]
        self.cx = None
    def _block(self, big, small, rot):
        fb = font("DejaVuSansMono-Bold.ttf", 54); fs = font("DejaVuSansMono-Bold.ttf", 28)
        d0 = ImageDraw.Draw(Image.new("RGBA", (1, 1))); w = int(d0.textlength(big, font=fb) + d0.textlength(" " + small, font=fs) + 70); h = 92
        im = Image.new("RGBA", (w + 40, h + 50), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([20, 30, 20 + w, 30 + h], radius=10, fill=(0, 0, 0, 90)); im = im.filter(ImageFilter.GaussianBlur(8)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([20, 22, 20 + w, 22 + h], radius=10, fill=(196, 196, 190, 255))
        d.rounded_rectangle([20, 10, 20 + w, 10 + h], radius=10, fill=(246, 246, 242, 255))
        x = 55; d.text((x, 56), big, font=fb, fill=(60, 60, 60), anchor="lm"); x += d.textlength(big + " ", font=fb)
        d.text((x, 62), small, font=fs, fill=(110, 110, 110), anchor="lm")
        return im.rotate(rot, resample=Image.BICUBIC, expand=True)
    def sfx(self, d): return [{"t": self.s + i * self.every + 0.25, "type": "pop_low"} for i in range(len(self.labels))]
    def frame_mask(self, t, fr, mask):
        if not (self.s <= t <= self.e): return None, None
        cx, top = head_top(mask); self.cx = cx if self.cx is None else self.cx * 0.8 + cx * 0.2
        o = blank(); a = 1 - ease((t - self.e + 0.3) / 0.3); y = top - 20
        for i, b in enumerate(self.blocks):
            k = (t - self.s - i * self.every) / 0.35
            if k <= 0: break
            drop = (1 - back(k)) * -700; y -= 96
            o.alpha_composite(fade(b, a * min(1, k * 3)), (int(self.cx - b.width / 2 + (i % 2) * 18 - 9), int(y - b.height / 2 + drop)))
        return None, o

class PostWall:
    needs_mask = True
    def __init__(self, start=0.0, end=5.0, total=1711, unit="POSTS", day_label="DAY 564", cols=31, rows=14, x=13, y=380, cell=34, seed=3):
        self.s, self.e, self.total, self.unit, self.day, self.cols, self.rows, self.x, self.y, self.cell = start, end, total, unit, day_label, cols, rows, x, y, cell
        rng = np.random.default_rng(seed); pal = [(40, 52, 44), (122, 134, 116), (166, 176, 158), (205, 168, 92), (236, 232, 220)]
        self.colors = [pal[i] for i in rng.choice(len(pal), cols * rows, p=[.25, .3, .2, .1, .15])]
        self.order = rng.permutation(cols * rows)
    def sfx(self, d): return [{"t": self.s, "type": "whoosh", "dur": 0.5}, {"t": self.s + 0.3, "type": "typing", "dur": 2.0}]
    def frame_mask(self, t, fr, mask):
        if not (self.s <= t <= self.e): return None, None
        a = ease((t - self.s) / 0.3) * (1 - ease((t - self.e + 0.3) / 0.3)); k = ease((t - self.s - 0.2) / 2.2)
        o = blank(); d = ImageDraw.Draw(o); n = int(len(self.order) * k); filled = set(self.order[:n].tolist())
        for idx in range(self.cols * self.rows):
            r, c = divmod(idx, self.cols); x0 = self.x + c * self.cell; y0 = self.y + r * self.cell
            if idx in filled: d.rectangle([x0 + 3, y0 + 3, x0 + self.cell - 3, y0 + self.cell - 3], fill=self.colors[idx] + (int(255 * a),))
            else: d.rectangle([x0 + 3, y0 + 3, x0 + self.cell - 3, y0 + self.cell - 3], outline=(90, 96, 90, int(200 * a)), width=2)
        d.text((self.x + 30, self.y - 30), "■ " + self.day, font=font("DejaVuSansMono-Bold.ttf", 30), fill=(230, 226, 214, int(255 * a)), anchor="lm")
        num = f"{int(self.total * k):,}"; fb = font("DejaVuSerif-Bold.ttf", 84)
        tx = self.x + self.cols * self.cell - 160; d.text((tx, self.y - 30), num, font=fb, fill=(214, 180, 104, int(255 * a)), anchor="rm")
        d.text((tx + 14, self.y - 30), self.unit, font=font("DejaVuSansMono-Bold.ttf", 30), fill=(230, 226, 214, int(255 * a)), anchor="lm")
        return o, None

class LiveCursor:
    needs_mask = False
    def __init__(self, start=0.0, end=5.0, points=((900, 1500, 0.0), (700, 520, 1.2), (330, 760, 2.6)), clicks=(1.4, 2.8), select=None):
        self.s, self.e = start, end; self.pts = [(x, y, start + dt) for x, y, dt in points]; self.clicks = [start + c for c in clicks]
        self.select = select   # optional [x0, y0, x1, y1, t_start, t_end]: drag a blue selection box
        cur = Image.new("RGBA", (70, 100), (0, 0, 0, 0)); d = ImageDraw.Draw(cur)
        poly = [(8, 6), (8, 76), (26, 60), (38, 90), (50, 85), (38, 56), (62, 56)]
        sh = Image.new("RGBA", (70, 100), (0, 0, 0, 0)); ImageDraw.Draw(sh).polygon([(x + 4, y + 5) for x, y in poly], fill=(0, 0, 0, 110))
        cur.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4))); d.polygon(poly, fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=4); self.cur = cur
    def sfx(self, d): return [{"t": c, "type": "click"} for c in self.clicks]
    def pos(self, t):
        p = self.pts
        if t <= p[0][2]: return p[0][:2]
        for (x0, y0, t0), (x1, y1, t1) in zip(p, p[1:]):
            if t <= t1: k = ease((t - t0) / max(0.01, t1 - t0)); return x0 + (x1 - x0) * k, y0 + (y1 - y0) * k
        return p[-1][:2]
    def frame(self, t):
        if not (self.s <= t <= self.e): return None, None
        a = ease((t - self.s) / 0.2) * (1 - ease((t - self.e + 0.25) / 0.25)); x, y = self.pos(t); o = blank(); d = ImageDraw.Draw(o)
        if self.select:
            x0, y0, x1, y1, ts, te = self.select; k = ease((t - self.s - ts) / max(0.1, te - ts))
            if k > 0:
                xe, ye = x0 + (x1 - x0) * k, y0 + (y1 - y0) * k
                d.rectangle([x0, y0, xe, ye], fill=(0, 122, 255, int(50 * a)), outline=(0, 122, 255, int(255 * a)), width=4)
        for c in self.clicks:
            k = (t - c) / 0.5
            if 0 <= k <= 1:
                r = 20 + 60 * ease(k); d.ellipse([x - r, y - r, x + r, y + r], outline=(255, 255, 255, int(220 * (1 - k) * a)), width=6)
        press = 0.85 if any(0 <= t - c < 0.12 for c in self.clicks) else 1.0
        cc = self.cur.resize((int(70 * press), int(100 * press)), Image.BILINEAR)
        o.alpha_composite(fade(cc, a), (int(x - 8 * press), int(y - 6 * press))); return None, o

STYLES = {"head_stack": HeadStack, "post_wall": PostWall, "live_cursor": LiveCursor}
