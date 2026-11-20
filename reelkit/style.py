"""Shared brand style: colours, fonts and easing helpers."""
import os
NAVY = "#0b3d91"; NAVY_DARK = "#0b1f4b"; RED = "#e8392b"; GREEN = "#2e9e5b"
INK = "#1c2433"; MUTED = "#7a8494"; GREY = "#c9ced6"
FONT = "Poppins"
FONT_DIRS = ["/usr/share/fonts/truetype/google-fonts", os.path.expanduser("~/.fonts"),
             os.path.expanduser("~/Library/Fonts"), "/Library/Fonts", "C:/Windows/Fonts"]

def font_path(name="Poppins-Bold.ttf"):
    for d in FONT_DIRS:
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
    raise FileNotFoundError(f"{name} not found. Install Poppins from fonts.google.com/specimen/Poppins")

def clamp(x): return max(0.0, min(1.0, x))
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)
def back(x):
    """Ease-out with a small overshoot, for 'pop' animations."""
    x = clamp(x); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
