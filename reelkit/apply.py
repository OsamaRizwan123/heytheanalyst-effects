"""Run any style from any section folder.

  python -m reelkit.apply data-visuals number_chart --video raw.mp4 --params '{"start": 2, "end": 6, "value": 42}' -o out.mp4
  python -m reelkit.apply looks spotlight --video raw.mp4 --params '{"start": 1, "end": 4, "word": "DATA"}'
Params are the style's constructor arguments (see the section's styles.py).
"""
import argparse, importlib.util, json, os, sys
from .fx import run

ROOT = os.path.join(os.path.dirname(__file__), "..")

def load(section):
    spec = importlib.util.spec_from_file_location(f"{section}_styles", os.path.join(ROOT, section, "styles.py"))
    m = importlib.util.module_from_spec(spec); sys.path.insert(0, ROOT); spec.loader.exec_module(m); return m

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("section"); ap.add_argument("style"); ap.add_argument("--video", required=True)
    ap.add_argument("--params", default="{}"); ap.add_argument("--masks"); ap.add_argument("-o", default="out.mp4"); a = ap.parse_args()
    eff = load(a.section).STYLES[a.style](**json.loads(a.params))
    run(a.video, eff, a.o, masks=a.masks); print("->", a.o)
