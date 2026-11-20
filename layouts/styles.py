"""Layouts.

  phone_mockup  a phone slides up holding a screenshot/chart (your app, a dashboard, a post)
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from PIL import Image, ImageDraw, ImageFilter
from reelkit.fx import font, blank, fade, W, H
from reelkit.style import back, ease

class PhoneMockup:
    needs_mask = False
    def __init__(self, start=0.0, end=4.0, image=None, x=540, y=820, h=1000, tilt=-6):
        self.s, self.e, self.x, self.y, self.h, self.tilt = start, end, x, y, h, tilt
        pw = int(h * 0.49); sw, shh = pw - 36, h - 36
        ph = Image.new("RGBA", (pw + 80, h + 80), (0, 0, 0, 0)); d = ImageDraw.Draw(ph)
        d.rounded_rectangle([40, 50, 40 + pw, 50 + h], radius=70, fill=(0, 0, 0, 110)); ph = ph.filter(ImageFilter.GaussianBlur(20)); d = ImageDraw.Draw(ph)
        d.rounded_rectangle([40, 40, 40 + pw, 40 + h], radius=70, fill=(20, 22, 26, 255))
        scr = Image.open(image).convert("RGB") if image else Image.new("RGB", (sw, shh), (245, 246, 248))
        r = min(sw / scr.width, shh / scr.height); scr = scr.resize((int(scr.width * r), int(scr.height * r)), Image.LANCZOS)
        canvas = Image.new("RGB", (sw, shh), (255, 255, 255)); canvas.paste(scr, ((sw - scr.width) // 2, (shh - scr.height) // 2)); scr = canvas.convert("RGBA")
        m = Image.new("L", (sw, shh), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, sw - 1, shh - 1], radius=56, fill=255); scr.putalpha(m)
        ph.alpha_composite(scr, (58, 58)); d = ImageDraw.Draw(ph)
        d.rounded_rectangle([40 + pw / 2 - 70, 70, 40 + pw / 2 + 70, 104], radius=17, fill=(20, 22, 26, 255))
        self.phone = ph.rotate(tilt, resample=Image.BICUBIC, expand=True)
    def sfx(self, d): return [{"t": self.s, "type": "whoosh", "dur": 0.5}, {"t": self.e - 0.3, "type": "whoosh", "dur": 0.3}]
    def frame(self, t):
        if not (self.s <= t <= self.e): return None, None
        a = ease((t - self.s) / 0.2) * (1 - ease((t - self.e + 0.3) / 0.3))
        rise = (1 - back((t - self.s) / 0.5)) * 900 + ease((t - self.e + 0.3) / 0.3) * 900
        o = blank(); o.alpha_composite(fade(self.phone, a), (int(self.x - self.phone.width / 2), int(self.y - self.phone.height / 2 + rise))); return None, o

STYLES = {"phone_mockup": PhoneMockup}
