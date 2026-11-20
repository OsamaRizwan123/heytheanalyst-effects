"""Text overlays.

  glass_type  a frosted-glass card (blurs what's behind it) where your line types out
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from reelkit.fx import font, blank, fade, W, H, RED, INK, WHITE
from reelkit.style import back, ease

class GlassType:
    needs_mask = False
    def __init__(self, start=0.0, end=4.0, text="AI does the analysis.\nYou tell the story.", highlight=("story.",), x=90, y=300, w=900, h=300, label="heytheanalyst"):
        self.s, self.e, self.text, self.hl, self.x, self.y, self.w, self.h, self.label = start, end, text, [h.lower() for h in highlight], x, y, w, h, label
    def sfx(self, d): return [{"t": self.s, "type": "whoosh", "dur": 0.4}, {"t": self.s + 0.4, "type": "typing", "dur": len(self.text) * 0.035}]
    def frame_bg(self, t, fr):
        if not (self.s <= t <= self.e): return None, None
        a = ease((t - self.s) / 0.3) * (1 - ease((t - self.e + 0.25) / 0.25)); sc = 0.92 + 0.08 * ease((t - self.s) / 0.35)
        w, h = int(self.w * sc), int(self.h * sc); x = self.x + (self.w - w) // 2; y = self.y + (self.h - h) // 2
        reg = fr.crop((x, y, x + w, y + h)).convert("RGB").filter(ImageFilter.GaussianBlur(28))
        reg = ImageEnhance.Brightness(reg).enhance(0.9).convert("RGBA")
        tint = Image.new("RGBA", (w, h), (15, 18, 26, 120)); reg.alpha_composite(tint)
        m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius=40, fill=255); reg.putalpha(m)
        d = ImageDraw.Draw(reg); d.rounded_rectangle([1, 1, w - 2, h - 2], radius=40, outline=(255, 255, 255, 170), width=3)
        d.ellipse([34, 34, 50, 50], fill=RED); d.text((62, 42), self.label, font=font("Poppins-Regular.ttf", 26), fill=(255, 255, 255, 230), anchor="lm")
        n = int(len(self.text) * ease((t - self.s - 0.4) / max(0.5, len(self.text) * 0.035))); shown = self.text[:n]
        f = font("Poppins-Bold.ttf", 58); yy = 90
        for li, line in enumerate(shown.split("\n")):
            xx = 34
            for wd in line.split(" "):
                d.text((xx, yy), wd, font=f, fill=(RED if wd.lower() in self.hl else WHITE)); xx += d.textlength(wd + " ", font=f)
            yy += 76
        o = blank(); o.alpha_composite(fade(reg, a), (x, y)); return None, o

STYLES = {"glass_type": GlassType}
