"""Make burned-in captions (.ass) with keywords highlighted in red.

captions.json: [[start, end, "text"], ...]  (copy from segs.json and fix the wording)
Usage:
  python -m reelkit.captions captions.json -o captions.ass --keywords consultant "80%" --max-chars 28
"""
import argparse, json, re

HDR = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Poppins,{size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,3,4,2,60,60,{marginv},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def chunk(text, max_chars):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > max_chars and cur: lines.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    if cur: lines.append(cur)
    return lines

def ts(x): return f"0:{int(x // 60):02d}:{x % 60:05.2f}"

def build(segs, keywords, max_chars=28, size=74, marginv=175):
    lines = []
    for a, b, text in segs:
        parts = chunk(text, max_chars); tot = sum(len(p) + 4 for p in parts); t = a
        for p in parts: d = (b - a) * (len(p) + 4) / tot; lines.append([t, t + d, p]); t += d
    for i in range(len(lines) - 1): lines[i][1] = min(lines[i + 1][0], lines[i][1] + 0.5)
    def hi(c):
        for k in sorted(keywords, key=len, reverse=True):
            c = re.sub(r"(?<![\w{])(" + re.escape(k) + r")(?![\w])", r"{\\c&H2B39E8&}\1{\\c&HFFFFFF&}", c, flags=re.I)
        return c
    out = HDR.format(size=size, marginv=marginv)
    for a, b, c in lines: out += f"Dialogue: 0,{ts(a)},{ts(b)},Cap,,0,0,0,,{hi(c)}\n"
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("segs"); ap.add_argument("-o", default="captions.ass")
    ap.add_argument("--keywords", nargs="*", default=[]); ap.add_argument("--max-chars", type=int, default=28)
    ap.add_argument("--size", type=int, default=74); ap.add_argument("--margin-v", type=int, default=175)
    a = ap.parse_args()
    open(a.o, "w").write(build(json.load(open(a.segs)), a.keywords, a.max_chars, a.size, a.margin_v))

if __name__ == "__main__": main()
