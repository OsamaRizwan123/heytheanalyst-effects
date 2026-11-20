"""Hook styles for the first 1-3 seconds.

  hook_caption   big two-line line on your chest, red key word (Poppins)
  headline_box   two-line headline at the top; line 2 sits in a white box
  backdrop_word  a giant word drops in BEHIND you (needs a person cut-out)
  red_stamp      a red stamp ("MYTH", "WRONG") slams onto the screen
  typed_question a white card where a question types itself out
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from PIL import Image, ImageDraw
from reelkit.fx import font, blank, outlined, fade, W, H, RED, INK, WHITE
from reelkit.style import back, ease

class Hook:
    needs_mask = False
    def __init__(self, line1, line2="", highlight=(), start=0.0, end=2.5, y=None):
        self.l1, self.l2, self.hl, self.s, self.e = line1, line2, [h.lower() for h in highlight], start, end; self.y = y
    def alpha(self, t, fin=0.25, fout=0.2): return ease((t - self.s) / fin) * (1 - ease((t - self.e + fout) / fout))
    def active(self, t): return self.s <= t <= self.e
    def sfx(self, d): return [{"t": self.s, "type": "pop"}]
    def _line(self, d, text, y, f, a, center=True):
        x = (W - d.textlength(text, font=f)) / 2
        for w in text.split():
            c = RED if w.strip(".,!?").lower() in self.hl else WHITE
            outlined(d, (x, y), w, f, c, w=5, alpha=int(255 * a)); x += d.textlength(w + " ", font=f)

class HookCaption(Hook):
    def frame(self, t):
        if not self.active(t): return None, None
        a = self.alpha(t); s = back((t - self.s) / 0.3); o = blank(); d = ImageDraw.Draw(o)
        f = font("Poppins-Bold.ttf", max(10, int(84 * min(s, 1.05)))); y = self.y or 1330
        self._line(d, self.l1, y, f, a)
        if self.l2: self._line(d, self.l2, y + 104, f, a)
        return None, o

class HeadlineBox(Hook):
    def frame(self, t):
        if not self.active(t): return None, None
        a = self.alpha(t); o = blank(); d = ImageDraw.Draw(o); y = self.y or 330
        f1 = font("Poppins-Bold.ttf", 70); f2 = font("Poppins-Bold.ttf", 76)
        dy = int(-60 * (1 - ease((t - self.s) / 0.35)))
        self._line(d, self.l1, y + dy, f1, a)
        if self.l2:
            a2 = ease((t - self.s - 0.35) / 0.25) * (1 - ease((t - self.e + 0.2) / 0.2)); tw = d.textlength(self.l2, font=f2); x = (W - tw) / 2
            sx = int((tw + 60) * ease((t - self.s - 0.35) / 0.3))
            d.rectangle([x - 30, y + 100, x - 30 + sx, y + 200], fill=(255, 255, 255, int(255 * a2)))
            if a2 > 0.5: d.text((x, y + 108), self.l2, font=f2, fill=INK + (int(255 * a2),))
        return None, o
    def sfx(self, d): return [{"t": self.s, "type": "whoosh", "dur": 0.4}, {"t": self.s + 0.35, "type": "pop_high"}]

class BackdropWord(Hook):
    needs_mask = True
    def frame(self, t):
        if not self.active(t): return None, None
        a = self.alpha(t, 0.2, 0.3); o = blank(); d = ImageDraw.Draw(o)
        drop = 1 - back((t - self.s) / 0.45); f = font("DejaVuSerif-Bold.ttf", 300)
        word = self.l1.upper(); y = (self.y or 760) - int(500 * drop)
        size = d.textlength(word, font=f)
        if size > W - 40: f = font("DejaVuSerif-Bold.ttf", int(300 * (W - 40) / size))
        d.text((W / 2, y), word, font=f, fill=(255, 255, 255, int(235 * a)), anchor="mm")
        if self.l2: d.text((W / 2, y - 200), self.l2, font=font("Poppins-Bold.ttf", 54), fill=RED + (int(255 * a),), anchor="mm")
        return o, None
    def sfx(self, d): return [{"t": self.s + 0.25, "type": "pop_low"}]

class RedStamp(Hook):
    def frame(self, t):
        if not self.active(t): return None, None
        a = self.alpha(t, 0.05, 0.25); k = (t - self.s) / 0.18; sc = 2.2 - 1.2 * ease(k)
        f = font("Poppins-Bold.ttf", 150); word = self.l1.upper()
        tmp = Image.new("RGBA", (1000, 360), (0, 0, 0, 0)); d = ImageDraw.Draw(tmp)
        tw = d.textlength(word, font=f); bx = (1000 - tw) / 2 - 40
        d.rounded_rectangle([bx, 60, bx + tw + 80, 300], radius=24, outline=RED + (255,), width=16)
        d.text((500, 180), word, font=f, fill=RED + (255,), anchor="mm")
        tmp = tmp.rotate(-12, resample=Image.BICUBIC, expand=True)
        tmp = tmp.resize((int(tmp.width * sc), int(tmp.height * sc)), Image.BILINEAR)
        shake = int(10 * math.sin(t * 90) * max(0, 1 - (t - self.s - 0.18) / 0.2)) if t > self.s + 0.18 else 0
        o = blank(); o.alpha_composite(fade(tmp, a * min(1, k * 3)), (int(W / 2 - tmp.width / 2 + shake), int((self.y or 520) - tmp.height / 2)))
        return None, o
    def sfx(self, d): return [{"t": self.s + 0.17, "type": "pop_low"}, {"t": self.s + 0.19, "type": "pop_low"}]

class TypedQuestion(Hook):
    def frame(self, t):
        if not self.active(t): return None, None
        a = self.alpha(t, 0.2, 0.25); o = blank(); d = ImageDraw.Draw(o); f = font("Poppins-Bold.ttf", 58)
        q = self.l1; n = int(len(q) * min(1, (t - self.s - 0.25) / max(0.6, len(q) * 0.045))); y = self.y or 360
        tw = max(d.textlength(q, font=f), 300); x = (W - tw) / 2
        d.rounded_rectangle([x - 40, y - 50, x + tw + 40, y + 70], radius=30, fill=(255, 255, 255, int(245 * a)))
        d.text((x, y), q[:max(0, n)], font=f, fill=INK + (int(255 * a),), anchor="lm")
        if int(t * 3) % 2 == 0 or n < len(q):
            cx = x + d.textlength(q[:max(0, n)], font=f) + 6; d.rectangle([cx, y - 32, cx + 5, y + 32], fill=RED + (int(255 * a),))
        return None, o
    def sfx(self, d):
        dur = max(0.6, len(self.l1) * 0.045); return [{"t": self.s, "type": "pop"}, {"t": self.s + 0.25, "type": "typing", "dur": dur}]

STYLES = {"hook_caption": HookCaption, "headline_box": HeadlineBox, "backdrop_word": BackdropWord, "red_stamp": RedStamp, "typed_question": TypedQuestion}
