"""Call-to-action styles for the end of a reel.

  end_card      an image card (e.g. your PDF cover) plus "Comment X" text
  comment_box   an Instagram-style comment field types your keyword and posts it
  follow_button a profile card whose Follow button flips to Following
  save_prompt   a bookmark icon fills in with "Save this for later"
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from PIL import Image, ImageDraw, ImageFilter
from reelkit.fx import font, blank, outlined, fade, W, H, RED, INK, WHITE, NAVY
from reelkit.style import back, ease

IGBLUE = (0, 149, 246)

class CTA:
    needs_mask = False
    def __init__(self, start=0.0, end=5.0, keyword="CHART", handle="@heytheanalyst", image=None, line1="", line2="", y=None):
        self.s, self.e, self.kw, self.handle, self.image, self.l1, self.l2, self.y = start, end, keyword, handle, image, line1, line2, y
    def a(self, t, fin=0.3, fout=0.25): return ease((t - self.s) / fin) * (1 - ease((t - self.e + fout) / fout))
    def active(self, t): return self.s <= t <= self.e
    def caption(self, d, text, y, al, hl=()):
        f = font("Poppins-Bold.ttf", 60); x = (W - d.textlength(text, font=f)) / 2
        for w in text.split():
            outlined(d, (x, y), w, f, RED if w.strip(".,!?").lower() in [h.lower() for h in hl] else WHITE, w=4, alpha=int(255 * al)); x += d.textlength(w + " ", font=f)

def _card(im, w, h, r=26):
    im = im.convert("RGB").resize((w, h), Image.LANCZOS).convert("RGBA")
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=255); im.putalpha(m)
    sh = Image.new("RGBA", (w + 80, h + 80), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([40, 50, 40 + w, 50 + h], radius=r, fill=(0, 0, 0, 110))
    sh = sh.filter(ImageFilter.GaussianBlur(18)); sh.alpha_composite(im, (40, 40)); return sh

class EndCard(CTA):
    def frame(self, t):
        if not self.active(t): return None, None
        o = blank(); d = ImageDraw.Draw(o)
        if self.image:
            c = _card(Image.open(self.image), 900, 600); s = back((t - self.s) / 0.4); al = self.a(t)
            c2 = c.resize((max(1, int(c.width * (0.85 + 0.15 * min(s, 1.04)))), max(1, int(c.height * (0.85 + 0.15 * min(s, 1.04))))), Image.BILINEAR)
            o.alpha_composite(fade(c2, al), (int(W / 2 - c2.width / 2), int((self.y or 620) - c2.height / 2)))
        self.caption(d, self.l1 or f"Comment {self.kw}", 1440, ease((t - self.s - 0.3) / 0.3) * self.a(t), [self.kw])
        if self.l2: self.caption(d, self.l2, 1520, ease((t - self.s - 1.0) / 0.3) * self.a(t))
        return None, o
    def sfx(self, d): return [{"t": self.s, "type": "ding"}]

class CommentBox(CTA):
    def frame(self, t):
        if not self.active(t): return None, None
        al = self.a(t); o = blank(); d = ImageDraw.Draw(o); y = self.y or 1300
        rise = int(80 * (1 - ease((t - self.s) / 0.3))); y += rise
        d.rounded_rectangle([90, y, 990, y + 120], radius=60, fill=(30, 30, 30, int(235 * al)))
        d.ellipse([115, y + 22, 191, y + 98], fill=NAVY + (int(255 * al),))
        d.text((153, y + 60), self.handle[1:2].upper(), font=font("Poppins-Bold.ttf", 36), fill=WHITE + (int(255 * al),), anchor="mm")
        tstart = self.s + 0.5; n = int(len(self.kw) * ease((t - tstart) / 0.8)); typed = self.kw[:n]
        ft = font("Poppins-Regular.ttf", 44)
        d.text((215, y + 60), typed if typed else "Add a comment...", font=ft, fill=(WHITE if typed else (150, 150, 150)) + (int(255 * al),), anchor="lm")
        posted = t > tstart + 1.3
        d.text((955, y + 60), "Post", font=font("Poppins-Bold.ttf", 40), fill=(IGBLUE if n == len(self.kw) else (70, 110, 150)) + (int(255 * al),), anchor="rm")
        if posted:
            b = back((t - tstart - 1.3) / 0.35); by = y - 170
            w2 = int(760 * min(b, 1.03)); x0 = (W - w2) // 2
            d.rounded_rectangle([x0, by, x0 + w2, by + 130], radius=36, fill=(255, 255, 255, int(245 * al)))
            if b > 0.6:
                d.text((x0 + 40, by + 42), self.handle, font=font("Poppins-Bold.ttf", 32), fill=INK + (int(255 * al),), anchor="lm")
                d.text((x0 + 40, by + 90), self.kw, font=font("Poppins-Bold.ttf", 40), fill=RED + (int(255 * al),), anchor="lm")
                hx = x0 + w2 - 70; hy = by + 65; r = 18
                d.ellipse([hx - r, hy - r, hx, hy], fill=RED + (int(255 * al),)); d.ellipse([hx, hy - r, hx + r, hy], fill=RED + (int(255 * al),))
                d.polygon([(hx - r, hy - 6), (hx + r, hy - 6), (hx, hy + r + 4)], fill=RED + (int(255 * al),))
        return None, o
    def sfx(self, d): return [{"t": self.s, "type": "pop"}, {"t": self.s + 0.5, "type": "typing", "dur": 0.8}, {"t": self.s + 1.8, "type": "pop_high"}]

class FollowButton(CTA):
    def frame(self, t):
        if not self.active(t): return None, None
        al = self.a(t); s = back((t - self.s) / 0.35); o = blank(); d = ImageDraw.Draw(o); y = self.y or 1330
        w2 = int(820 * min(s, 1.03)); x0 = (W - w2) // 2
        d.rounded_rectangle([x0, y, x0 + w2, y + 160], radius=40, fill=(255, 255, 255, int(245 * al)))
        if s > 0.7:
            d.ellipse([x0 + 30, y + 30, x0 + 130, y + 130], fill=NAVY + (int(255 * al),))
            d.text((x0 + 80, y + 80), self.handle[1:2].upper(), font=font("Poppins-Bold.ttf", 46), fill=WHITE + (int(255 * al),), anchor="mm")
            d.text((x0 + 155, y + 62), self.handle, font=font("Poppins-Bold.ttf", 38), fill=INK + (int(255 * al),), anchor="lm")
            d.text((x0 + 155, y + 108), "Charts like a consultant", font=font("Poppins-Regular.ttf", 28), fill=(122, 132, 148, int(255 * al)), anchor="lm")
            done = t > self.s + 1.4; bx1 = x0 + w2 - 30; bx0 = bx1 - (230 if done else 200)
            press = 0.92 if self.s + 1.25 < t < self.s + 1.45 else 1.0
            cy = y + 80; hh = int(36 * press)
            d.rounded_rectangle([bx0, cy - hh, bx1, cy + hh], radius=18, fill=((225, 228, 233) if done else IGBLUE) + (int(255 * al),))
            d.text(((bx0 + bx1) / 2, cy), "Following" if done else "Follow", font=font("Poppins-Bold.ttf", 32), fill=(INK if done else WHITE) + (int(255 * al),), anchor="mm")
        return None, o
    def sfx(self, d): return [{"t": self.s, "type": "pop"}, {"t": self.s + 1.4, "type": "ding"}]

class SavePrompt(CTA):
    def frame(self, t):
        if not self.active(t): return None, None
        al = self.a(t); s = back((t - self.s) / 0.35); o = blank(); d = ImageDraw.Draw(o); y = self.y or 1300
        sc = min(s, 1.05); cx = W / 2; w2, h2 = 120 * sc, 160 * sc
        pts = [(cx - w2 / 2, y), (cx + w2 / 2, y), (cx + w2 / 2, y + h2), (cx, y + h2 * 0.72), (cx - w2 / 2, y + h2)]
        filled = t > self.s + 0.9
        d.polygon(pts, fill=(RED if filled else (0, 0, 0, 0)) + ((int(255 * al),) if filled else ()), outline=WHITE + (int(255 * al),), width=10)
        f = font("Poppins-Bold.ttf", 60); txt = self.l1 or "Save this for later"
        outlined(d, (W / 2, y + 230), txt, f, WHITE, w=4, alpha=int(255 * al * ease((t - self.s - 0.3) / 0.3)), anchor="mm")
        return None, o
    def sfx(self, d): return [{"t": self.s, "type": "pop"}, {"t": self.s + 0.9, "type": "pop_high"}]

STYLES = {"end_card": EndCard, "comment_box": CommentBox, "follow_button": FollowButton, "save_prompt": SavePrompt}
