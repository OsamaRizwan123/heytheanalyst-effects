"""Caption styles. Each takes word timings [[start,end,'word'],...] and keywords to colour red.

Styles:
  keyword_red   3-4 word chunks on your chest, white with black outline, keywords in red (Poppins)
  word_pop      one word at a time, big, pops in (Poppins)
  karaoke       a full line; the word being spoken sits on a red pill (Inter Black)
  boxed         black text on a white rounded box (Poppins)
  handwritten   marker-style handwriting, slight tilt (Caveat)
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from PIL import Image, ImageDraw
from reelkit.fx import font, blank, outlined, W, RED, INK, WHITE
from reelkit.style import back, ease

def _chunks(words, n=4, max_chars=22):
    out, cur = [], []
    for w in words:
        if cur and (len(cur) >= n or len(" ".join(x[2] for x in cur + [w])) > max_chars): out.append(cur); cur = []
        cur.append(w)
    if cur: out.append(cur)
    return out

def _is_kw(word, kws): return word.strip(".,!?:;\"'").lower() in [k.lower() for k in kws]

class Base:
    needs_mask = False
    def __init__(self, words, keywords=(), y=1430): self.words, self.kws, self.y = words, keywords, y; self.chunks = _chunks(words)
    def active_chunk(self, t):
        for i, c in enumerate(self.chunks):
            end = self.chunks[i + 1][0][0] if i + 1 < len(self.chunks) else c[-1][1] + 0.4
            if c[0][0] <= t < end: return c
        return None

class KeywordRed(Base):
    def frame(self, t):
        c = self.active_chunk(t)
        if not c: return None, None
        o = blank(); d = ImageDraw.Draw(o); f = font("Poppins-Bold.ttf", 66)
        text = " ".join(w[2] for w in c); x = (W - d.textlength(text, font=f)) / 2
        for w in c:
            outlined(d, (x, self.y), w[2], f, RED if _is_kw(w[2], self.kws) else WHITE, w=4)
            x += d.textlength(w[2] + " ", font=f)
        return None, o

class WordPop(Base):
    def frame(self, t):
        cur = next((w for w in self.words if w[0] <= t < w[1] + 0.05), None)
        if not cur: return None, None
        s = back((t - cur[0]) / 0.18); o = blank(); d = ImageDraw.Draw(o)
        f = font("Poppins-Bold.ttf", max(10, int(110 * min(s, 1.08))))
        outlined(d, (W / 2, self.y), cur[2].upper(), f, RED if _is_kw(cur[2], self.kws) else WHITE, w=5, anchor="mm")
        return None, o

class Karaoke(Base):
    def frame(self, t):
        c = self.active_chunk(t)
        if not c: return None, None
        o = blank(); d = ImageDraw.Draw(o); f = font("Inter-Black.otf", 62)
        text = " ".join(w[2] for w in c); x = (W - d.textlength(text, font=f)) / 2
        for w in c:
            wl = d.textlength(w[2], font=f)
            if w[0] <= t < w[1] + 0.05: d.rounded_rectangle([x - 14, self.y - 10, x + wl + 14, self.y + 76], radius=18, fill=RED + (255,))
            outlined(d, (x, self.y), w[2], f, WHITE, w=3 if not (w[0] <= t < w[1] + 0.05) else 0)
            x += d.textlength(w[2] + " ", font=f)
        return None, o

class Boxed(Base):
    def frame(self, t):
        c = self.active_chunk(t)
        if not c: return None, None
        a = ease((t - c[0][0]) / 0.12); o = blank(); d = ImageDraw.Draw(o); f = font("Poppins-Bold.ttf", 58)
        text = " ".join(w[2] for w in c); tw = d.textlength(text, font=f); x = (W - tw) / 2
        d.rounded_rectangle([x - 30, self.y - 18, x + tw + 30, self.y + 84], radius=22, fill=(255, 255, 255, int(240 * a)))
        for w in c:
            d.text((x, self.y), w[2], font=f, fill=(RED if _is_kw(w[2], self.kws) else INK) + (int(255 * a),)); x += d.textlength(w[2] + " ", font=f)
        return None, o

class Handwritten(Base):
    def frame(self, t):
        c = self.active_chunk(t)
        if not c: return None, None
        o = blank(); d = ImageDraw.Draw(o); f = font("Caveat.ttf", 124)
        text = " ".join(w[2] for w in c); tw = d.textlength(text, font=f); x = (W - tw) / 2
        for w in c:
            if t >= w[0] - 0.05:
                outlined(d, (x, self.y), w[2], f, RED if _is_kw(w[2], self.kws) else WHITE, outline=(20, 20, 20), w=3)
            x += d.textlength(w[2] + " ", font=f)
        o = o.rotate(-3, center=(W / 2, self.y + 40), resample=Image.BICUBIC)
        return None, o

STYLES = {"keyword_red": KeywordRed, "word_pop": WordPop, "karaoke": Karaoke, "boxed": Boxed, "handwritten": Handwritten}
