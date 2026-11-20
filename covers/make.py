"""Reel covers (1080x1920, with the important part inside Instagram's 3:4 grid crop: y 240-1680).

  big_text         a frame of you + dark fade + huge 2-line title, one red word
  card_over_face   an image card (PDF cover, chart) above your head + caption on your chest
  drawing_plus_face a drawing/chart on a white top half, you on the bottom, title in a pill above your head

  python covers/make.py big_text --video raw.mp4 --time 1.0 --line1 "12 charts" --line2 "like a consultant" --highlight consultant -o cover.jpg
  python covers/make.py card_over_face --video raw.mp4 --time 19 --image assets/pdf_cover.png --line1 "Comment CHART" --highlight chart
  python covers/make.py drawing_plus_face --video raw.mp4 --time 0.1 --image covers/previews/drawing.png --title "12 charts like a consultant" --highlight consultant
"""
import argparse, subprocess, sys, os, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from PIL import Image, ImageDraw, ImageFilter
from reelkit.fx import font, outlined, W, H, RED, INK, WHITE

def grab(video, t):
    p = tempfile.mktemp(suffix=".png")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(t), "-i", video, "-frames:v", "1", "-vf", f"scale={W}:{H}", p], check=True)
    return Image.open(p).convert("RGB")

def words(d, text, y, f, hl, fill=WHITE, outline=True, anchor_center=True):
    x = (W - d.textlength(text, font=f)) / 2
    for w in text.split():
        c = RED if w.strip(".,!?").lower() in hl else fill
        if outline: outlined(d, (x, y), w, f, c, w=5)
        else: d.text((x, y), w, font=f, fill=c)
        x += d.textlength(w + " ", font=f)

def big_text(a):
    im = grab(a.video, a.time).convert("RGBA"); g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    for y in range(H // 2, H): gd.line([(0, y), (W, y)], fill=(0, 0, 0, int(200 * (y - H / 2) / (H / 2))))
    im.alpha_composite(g); d = ImageDraw.Draw(im); f = font("Poppins-Bold.ttf", 120)
    words(d, a.line1, 1240, f, a.highlight)
    if a.line2: words(d, a.line2, 1380, f, a.highlight)
    return im.convert("RGB")

def card_over_face(a):
    im = grab(a.video, a.time).convert("RGBA"); c = Image.open(a.image).convert("RGB")
    cw = 900; ch = int(c.height * cw / c.width); c = c.resize((cw, ch), Image.LANCZOS).convert("RGBA")
    m = Image.new("L", (cw, ch), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, cw - 1, ch - 1], radius=26, fill=255); c.putalpha(m)
    sh = Image.new("RGBA", (cw + 80, ch + 80), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([40, 50, 40 + cw, 50 + ch], radius=26, fill=(0, 0, 0, 110))
    sh = sh.filter(ImageFilter.GaussianBlur(18)); sh.alpha_composite(c, (40, 40)); im.alpha_composite(sh, ((W - sh.width) // 2, 280))
    d = ImageDraw.Draw(im); f = font("Poppins-Bold.ttf", 62)
    if a.line1: words(d, a.line1, 1440, f, a.highlight)
    if a.line2: words(d, a.line2, 1520, f, a.highlight)
    return im.convert("RGB")

def drawing_plus_face(a):
    fr = grab(a.video, a.time); out = Image.new("RGB", (W, H), "white")
    out.paste(fr.crop((0, 430, W, 1430)), (0, 920))
    dr = Image.open(a.image).convert("RGB"); dw = 1000; dh = int(dr.height * dw / dr.width)
    if dh > 600: dh = 600; dw = int(dr.width * dh / dr.height)
    out.paste(dr.resize((dw, dh), Image.LANCZOS), ((W - dw) // 2, 290))
    d = ImageDraw.Draw(out); f = font("PatrickHand-Regular.ttf", 80); tw = d.textlength(a.title, font=f); x = (W - tw) / 2; y = 1050
    d.rounded_rectangle([x - 34, y - 62, x + tw + 34, y + 56], radius=56, fill="white")
    for w in a.title.split():
        d.text((x, y), w, font=f, fill=RED if w.lower() in a.highlight else (17, 17, 17), anchor="lm"); x += d.textlength(w + " ", font=f)
    return out

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("style", choices=["big_text", "card_over_face", "drawing_plus_face"])
    ap.add_argument("--video", required=True); ap.add_argument("--time", type=float, default=0.5); ap.add_argument("--image")
    ap.add_argument("--line1", default=""); ap.add_argument("--line2", default=""); ap.add_argument("--title", default="")
    ap.add_argument("--highlight", nargs="*", default=[]); ap.add_argument("-o", default="cover.jpg"); a = ap.parse_args()
    a.highlight = [h.lower() for h in a.highlight]
    {"big_text": big_text, "card_over_face": card_over_face, "drawing_plus_face": drawing_plus_face}[a.style](a).save(a.o, quality=95); print("->", a.o)
