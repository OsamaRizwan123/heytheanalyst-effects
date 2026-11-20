"""Explainer animations.

  checklist  a card next to your head; items appear and tick green on cue
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from PIL import Image, ImageDraw, ImageFilter
from reelkit.fx import font, blank, fade, W, H, RED, INK, GREEN
from reelkit.style import back, ease

class Checklist:
    needs_mask = False
    def __init__(self, start=0.0, end=5.0, title="Make charts like a consultant",
                 items=("Remove clutter", "Sort the bars", "Highlight one thing", "Title = the answer"), ticks=None, x=60, y=300, w=560):
        self.s, self.e, self.title, self.items = start, end, title, list(items)
        span = (end - start - 1.0); self.ticks = ticks or [start + 0.8 + span * (i + 0.5) / len(items) for i in range(len(items))]
        self.x, self.y, self.w = x, y, w
    def sfx(self, d): return [{"t": self.s, "type": "pop"}] + [{"t": t, "type": "pop_high"} for t in self.ticks]
    def frame(self, t):
        if not (self.s <= t <= self.e): return None, None
        a = ease((t - self.s) / 0.25) * (1 - ease((t - self.e + 0.25) / 0.25)); rh = 86; h = 120 + rh * len(self.items)
        card = Image.new("RGBA", (self.w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
        d.rounded_rectangle([0, 0, self.w - 1, h - 1], radius=28, fill=(255, 255, 255, 240))
        d.text((32, 34), self.title, font=font("Poppins-Bold.ttf", 32), fill=INK)
        for i, it in enumerate(self.items):
            ai = ease((t - self.s - 0.3 - i * 0.15) / 0.25); y = 105 + i * rh
            if ai <= 0: continue
            done = t >= self.ticks[i]; k = back((t - self.ticks[i]) / 0.25) if done else 0
            d.rounded_rectangle([32, y + 8, 82, y + 58], radius=12, fill=(GREEN if done else (255, 255, 255)) + (int(255 * ai),), outline=(GREEN if done else (190, 196, 206)) + (int(255 * ai),), width=4)
            if done and k > 0.2: d.line([(44, y + 33), (54, y + 45), (72, y + 20)], fill=(255, 255, 255, 255), width=6, joint="curve")
            d.text((104, y + 33), it, font=font("Poppins-Bold.ttf" if done else "Poppins-Regular.ttf", 32), fill=(INK if done else (122, 132, 148)) + (int(255 * ai),), anchor="lm")
        o = blank(); sh = Image.new("RGBA", (self.w + 60, h + 60), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle([30, 40, 30 + self.w, 40 + h], radius=28, fill=(0, 0, 0, 90)); sh = sh.filter(ImageFilter.GaussianBlur(14)); sh.alpha_composite(card, (30, 30))
        slide = int(-80 * (1 - ease((t - self.s) / 0.35)))
        o.alpha_composite(fade(sh, a), (self.x - 30 + slide, self.y - 30)); return None, o

STYLES = {"checklist": Checklist}
