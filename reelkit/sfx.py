"""Quiet synthesized sound effects, placed on a timeline.

events.json: [{"t": 1.2, "type": "pop"}, {"t": 3, "type": "typing", "dur": 2.4}, ...]
types: pop, pop_low, pop_high, whoosh (dur), ding, click, typing (dur)
Usage:
  python -m reelkit.sfx events.json --duration 30 -o sfx.wav
"""
import argparse, json, wave
import numpy as np
SR = 48000
_rng = np.random.default_rng(3)

def pop(f0=800, f1=500, d=0.09, amp=0.4):
    tt = np.arange(int(SR * d)) / SR; ph = 2 * np.pi * np.cumsum(np.linspace(f0, f1, len(tt))) / SR
    return amp * np.sin(ph) * np.exp(-tt * 38)
def whoosh(d=0.5, amp=0.2):
    n = int(SR * d); x = np.convolve(_rng.normal(0, 1, n), np.ones(14) / 14, "same")
    return amp * x * np.sin(np.linspace(0, np.pi, n)) ** 2
def ding(amp=0.3, d=0.9):
    tt = np.arange(int(SR * d)) / SR
    return amp * (np.sin(2 * np.pi * 1320 * tt) + 0.5 * np.sin(2 * np.pi * 2640 * tt)) * np.exp(-tt * 5) / 1.5
def click(): return pop(2400, 2000, 0.025, 0.12)

def render(events, duration):
    out = np.zeros(int(SR * duration))
    def add(t, s):
        i = int(t * SR)
        if 0 <= i < len(out): out[i:i + len(s)] += s[:len(out) - i]
    for e in events:
        t, k = e["t"], e["type"]
        if k == "pop": add(t, pop())
        elif k == "pop_low": add(t, pop(500, 300, 0.12, 0.35))
        elif k == "pop_high": add(t, pop(1100, 800, 0.08, 0.35))
        elif k == "whoosh": add(t, whoosh(e.get("dur", 0.5)))
        elif k == "ding": add(t, ding())
        elif k == "click": add(t, click())
        elif k == "typing":
            n = int(e.get("dur", 1.5) * 25)
            for c in range(n): add(t + c * e.get("dur", 1.5) / n, click())
    return out

def save(out, path):
    with wave.open(path, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("events"); ap.add_argument("--duration", type=float, required=True)
    ap.add_argument("-o", default="sfx.wav"); a = ap.parse_args()
    save(render(json.load(open(a.events)), a.duration), a.o)

if __name__ == "__main__": main()
