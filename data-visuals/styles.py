"""Data visuals.

  number_chart  a white card beside your head: bars grow and a big number counts up (e.g. +42%)
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from PIL import Image, ImageDraw, ImageFilter
from reelkit.fx import font, blank, fade, W, H, RED, INK, NAVY, GREEN
from reelkit.style import back, ease

class NumberChart:
    needs_mask = False
    def __init__(self, start=0.0, end=4.0, value=42, prefix="+", suffix="%", label="Conversion rate",
                 bars=(30, 34, 33, 38, 41, 47, 55, 62), x=640, y=300, w=400, h=420, color="red"):
        self.s, self.e, self.v, self.pre, self.suf, self.label, self.bars = start, end, value, prefix, suffix, label, bars
        self.x, self.y, self.w, self.h = x, y, w, h; self.col = RED if color == "red" else (GREEN if color == "green" else NAVY)
    def sfx(self, d): return [{"t": self.s, "type": "pop"}, {"t": self.s + 0.4, "type": "typing", "dur": 1.2}, {"t": self.s + 1.7, "type": "ding"}]
    def frame(self, t):
        if not (self.s <= t <= self.e): return None, None
        a = ease((t - self.s) / 0.25) * (1 - ease((t - self.e + 0.25) / 0.25)); sc = back((t - self.s) / 0.35)
        card = Image.new("RGBA", (self.w, self.h), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
        d.rounded_rectangle([0, 0, self.w - 1, self.h - 1], radius=30, fill=(255, 255, 255, 240))
        d.text((32, 34), self.label, font=font("Poppins-Regular.ttf", 28), fill=(122, 132, 148))
        k = ease((t - self.s - 0.4) / 1.2); val = self.v * k
        txt = f"{self.pre}{val:.0f}{self.suf}" if abs(self.v) >= 10 else f"{self.pre}{val:.1f}{self.suf}"
        d.text((30, 70), txt, font=font("Poppins-Bold.ttf", 96), fill=self.col)
        n = len(self.bars); mx = max(self.bars); bw = (self.w - 64) / n; base = self.h - 34
        for i, b in enumerate(self.bars):
            g = ease((t - self.s - 0.4 - i * 0.08) / 0.5); bh = (self.h - 230) * b / mx * g
            c = self.col if i == n - 1 else (205, 211, 220)
            d.rounded_rectangle([32 + i * bw + 5, base - bh, 32 + (i + 1) * bw - 5, base], radius=6, fill=c)
        o = blank(); s2 = min(sc, 1.04)
        cc = card.resize((max(1, int(self.w * s2)), max(1, int(self.h * s2))), Image.BILINEAR)
        sh = Image.new("RGBA", (cc.width + 60, cc.height + 60), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([30, 40, 30 + cc.width, 40 + cc.height], radius=30, fill=(0, 0, 0, 90))
        sh = sh.filter(ImageFilter.GaussianBlur(14)); sh.alpha_composite(cc, (30, 30))
        o.alpha_composite(fade(sh, a), (int(self.x + self.w / 2 - sh.width / 2), int(self.y + self.h / 2 - sh.height / 2)))
        return None, o

STYLES = {"number_chart": NumberChart}
