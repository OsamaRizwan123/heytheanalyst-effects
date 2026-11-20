"""More looks (imported into looks/styles.py STYLES).

  code_body     you turn into glowing code: your body is redrawn as monospace characters over a dark code background
  letter_dive   a giant word; your video shows through the letters, then the camera dives into one letter until it fills the screen
  layer_explode the frame splits into 3D layers (background, you, text, waveform) with white wireframe edges, then snaps back
"""
import sys, os, math, random
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from PIL import Image, ImageDraw, ImageFilter
from reelkit.fx import font, blank, fade, W, H, RED, WHITE
from reelkit.style import back, ease

CODE = ("def story(data): return situation(data) + complication(data) + resolution(data) "
        "SELECT city, SUM(orders) FROM orders GROUP BY city ORDER BY 2 DESC; "
        "df.groupby('cohort')['retained'].mean() # retention curve chart.title = 'the answer' ").replace("  ", " ")

class CodeBody:
    needs_mask = True; mask_front_only = True
    def __init__(self, start=0.0, end=4.0, text=CODE, cell=30, tint=(150, 40, 70)):
        self.s, self.e, self.text, self.cell, self.tint = start, end, text, cell, tint
        self.f = font("DejaVuSansMono-Bold.ttf", int(cell * 1.05)); self.fs = font("DejaVuSansMono-Bold.ttf", 26)
    def sfx(self, d): return [{"t": self.s, "type": "whoosh", "dur": 0.5}, {"t": self.e - 0.4, "type": "whoosh", "dur": 0.4}]
    def frame_mask(self, t, fr, mask):
        if not (self.s <= t <= self.e): return None, None
        a = ease((t - self.s) / 0.35) * (1 - ease((t - self.e + 0.35) / 0.35))
        cw, ch = int(self.cell * 0.62), self.cell; cols, rows = W // cw + 1, H // ch + 1
        small = np.asarray(fr.convert("L").resize((cols, rows), Image.BILINEAR)).astype(float) / 255
        msk = np.asarray(mask.resize((cols, rows), Image.BILINEAR)).astype(float) / 255
        o = Image.new("RGBA", (W, H), (8, 14, 12, int(250 * a))); d = ImageDraw.Draw(o)
        off = int(t * 12); n = len(self.text)
        for r in range(rows):
            for c in range(cols):
                ch_ = self.text[(r * cols + c + off * (r % 3 + 1)) % n]; x, y = c * cw, r * ch
                if msk[r, c] > 0.5:
                    v = 0.25 + 0.75 * small[r, c]; col = (int(60 + 195 * v), int(60 + 195 * v), int(50 + 180 * v))
                    if r > rows * 0.55: col = (int(self.tint[0] + 105 * v), int(self.tint[1] + 60 * v), int(self.tint[2] + 70 * v))
                    if small[r, c] > 0.55: d.rectangle([x, y, x + cw, y + ch], fill=(30, 30, 26, int(200 * a)))
                    d.text((x, y), ch_, font=self.f, fill=col + (int(255 * a),))
                elif (r + c) % 2 == 0:
                    d.text((x, y), ch_, font=self.f, fill=(40, 70, 52, int(160 * a)))
        return None, o

class LetterDive:
    needs_mask = False
    def __init__(self, start=0.0, end=3.0, word="DATA", letter=1, bg=(14, 16, 20)):
        self.s, self.e, self.word, self.li, self.bg = start, end, word.upper(), letter, bg
        f = font("Poppins-Bold.ttf", 330); m = Image.new("L", (W, H), 0); d = ImageDraw.Draw(m)
        tw = d.textlength(self.word, font=f)
        if tw > W - 60: f = font("Poppins-Bold.ttf", int(330 * (W - 60) / tw)); tw = d.textlength(self.word, font=f)
        x0 = (W - tw) / 2; d.text((x0, H / 2), self.word, font=f, fill=255, anchor="lm")
        pre = d.textlength(self.word[:self.li], font=f); lw = d.textlength(self.word[self.li], font=f)
        bb = d.textbbox((x0 + pre, H / 2), self.word[self.li], font=f, anchor="lm")
        arr = np.asarray(m)[int(bb[1]):int(bb[3]), int(bb[0]):int(bb[2])] > 128
        ys, xs = np.nonzero(arr)
        if len(ys):
            from scipy.ndimage import distance_transform_edt
            dist = distance_transform_edt(arr); yy, xx = np.unravel_index(np.argmax(dist), dist.shape)   # thickest part of the stroke
            self.fx, self.fy = bb[0] + xx, bb[1] + yy
        else: self.fx, self.fy = x0 + pre + lw / 2, H / 2
        self.mask = m
    def sfx(self, d): return [{"t": self.s, "type": "pop_low"}, {"t": self.s + 0.9, "type": "whoosh", "dur": 0.9}]
    def frame(self, t):
        if not (self.s <= t <= self.e): return None, None
        dive = ease((t - self.s - 0.9) / (self.e - self.s - 0.9)) if self.e - self.s > 1 else 1
        z = math.exp(dive * math.log(40)); a = ease((t - self.s) / 0.2)
        if z > 39: return None, None
        m = self.mask.transform((W, H), Image.AFFINE, (1 / z, 0, self.fx - self.fx / z + (W / 2 - self.fx) * dive * 0 , 0, 1 / z, self.fy - self.fy / z), resample=Image.BILINEAR)
        inv = Image.eval(m, lambda p: int((255 - p) * a))
        o = Image.new("RGBA", (W, H), self.bg + (255,)); o.putalpha(inv); return None, o

class LayerExplode:
    needs_mask = True; mask_front_only = True
    def __init__(self, start=0.0, end=4.0, title="layer\nexplode", labels=("ROOM", "YOU", "TYPE", "SOUND")):
        self.s, self.e, self.title, self.labels = start, end, title, labels
    def sfx(self, d): return [{"t": self.s, "type": "whoosh", "dur": 0.6}, {"t": self.e - 0.5, "type": "whoosh", "dur": 0.5}]
    @staticmethod
    def _quad(k, depth):
        sc = 1 - 0.42 * k - 0.04 * depth * k; cx = W / 2 + (depth - 1.5) * 150 * k; cy = H / 2 + (depth - 1.5) * 120 * k
        skew = 0.16 * k
        w, h = W * sc, H * sc
        return [(cx - w / 2, cy - h / 2 + h * skew * 0.3), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2 - h * skew * 0.3)]
    @staticmethod
    def _warp(img, quad):
        src = [(0, 0), (W, 0), (W, H), (0, H)]
        A = []; B = []
        for (x, y), (u, v) in zip(quad, src):
            A += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]; B += [u, v]
        coef = np.linalg.solve(np.array(A), np.array(B))
        return img.transform((W, H), Image.PERSPECTIVE, tuple(coef), resample=Image.BILINEAR)
    def frame_mask(self, t, fr, mask):
        if not (self.s <= t <= self.e): return None, None
        k = ease((t - self.s) / 0.7) * (1 - ease((t - self.e + 0.7) / 0.7))
        o = Image.new("RGBA", (W, H), (12, 13, 14, 255)); d = ImageDraw.Draw(o)
        room = fr.copy(); person = fr.copy(); person.putalpha(mask)
        txt = blank(); td = ImageDraw.Draw(txt); y = 420
        for line in self.title.split("\n"): td.text((110, y), line, font=font("DejaVuSerif-Bold.ttf", 190), fill=(240, 236, 228, 255)); y += 210
        wave = blank(); wd = ImageDraw.Draw(wave); rng = np.random.default_rng(int(t * 30))
        for i in range(70):
            h_ = 30 + 150 * abs(math.sin(i * 0.37 + t * 6)) * rng.uniform(0.5, 1); x = 500 + i * 8
            wd.line([(x, 1560 - h_ / 2), (x, 1560 + h_ / 2)], fill=((235, 120, 140) if i > 35 else (240, 240, 240)) + (255,), width=4)
        layers = [room, person, txt, wave]
        for depth, L in enumerate(layers):
            q = self._quad(k, depth); w_ = self._warp(L, q); o.alpha_composite(w_)
            if k > 0.02:
                d.line(q + [q[0]], fill=(235, 235, 235, int(230 * k)), width=3)
                d.text((q[0][0] + 10, q[0][1] - 40), self.labels[depth], font=font("DejaVuSansMono-Bold.ttf", 30), fill=(220, 220, 220, int(255 * k)))
        return None, o
