"""Looks.

  spotlight  the room goes dark, you stay lit, and a glowing word appears behind you (needs a person cut-out)
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from PIL import Image, ImageDraw, ImageFilter
from reelkit.fx import font, blank, W, H, RED, WHITE
from reelkit.style import ease

class Spotlight:
    needs_mask = True
    def __init__(self, start=0.0, end=4.0, word="DATA", cx=540, cy=900, glow="red"):
        self.s, self.e, self.word, self.cx, self.cy = start, end, word.upper(), cx, cy
        self.glow = RED if glow == "red" else (255, 214, 120)
        yy, xx = np.mgrid[0:H, 0:W]; r = np.sqrt(((xx - cx) / 520.0) ** 2 + ((yy - cy) / 760.0) ** 2)
        self.vign = np.clip((r - 0.35) / 0.65, 0, 1)
    def sfx(self, d): return [{"t": self.s, "type": "whoosh", "dur": 0.5}, {"t": self.s + 0.5, "type": "pop_low"}]
    def frame(self, t):
        if not (self.s <= t <= self.e): return None, None
        a = ease((t - self.s) / 0.5) * (1 - ease((t - self.e + 0.4) / 0.4))
        dark = (np.clip(0.55 + 0.4 * self.vign, 0, 0.95) * 255 * a).astype(np.uint8)
        o = Image.new("RGBA", (W, H), (0, 0, 0, 0)); o.putalpha(Image.fromarray(dark))
        aw = ease((t - self.s - 0.4) / 0.4) * (1 - ease((t - self.e + 0.4) / 0.4))
        if aw > 0:
            f = font("Poppins-Bold.ttf", 260); txt = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(txt)
            size = d.textlength(self.word, font=f)
            if size > W - 60: f = font("Poppins-Bold.ttf", int(260 * (W - 60) / size))
            d.text((W / 2, 640), self.word, font=f, fill=self.glow + (int(255 * aw),), anchor="mm")
            glow = txt.filter(ImageFilter.GaussianBlur(26)); o.alpha_composite(glow); o.alpha_composite(glow); o.alpha_composite(txt)
        return o, None

STYLES = {"spotlight": Spotlight}
