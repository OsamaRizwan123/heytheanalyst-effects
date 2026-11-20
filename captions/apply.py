"""Burn captions onto a video.

  python captions/apply.py --video raw.mp4 --segs segs.json --style karaoke --keywords consultant chart -o out.mp4
--segs: output of `python -m reelkit.transcribe` (fix the wording first). Styles: see captions/styles.py
"""
import argparse, json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from reelkit.fx import run, words_from_segments
from styles import STYLES

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--video", required=True); ap.add_argument("--segs", required=True)
    ap.add_argument("--style", default="keyword_red", choices=list(STYLES)); ap.add_argument("--keywords", nargs="*", default=[])
    ap.add_argument("--y", type=int, default=1430); ap.add_argument("-o", default="captioned.mp4"); a = ap.parse_args()
    words = words_from_segments(json.load(open(a.segs)))
    run(a.video, STYLES[a.style](words, a.keywords, a.y), a.o); print("->", a.o)
