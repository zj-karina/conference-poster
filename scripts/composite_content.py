#!/usr/bin/env python3
"""Composite the crisp, correct poster content back over an AI-decorated image.

Why: the image model (decorate_poster_fal.py) paints beautiful cohesive decoration,
but it RE-RENDERS the whole image and will silently corrupt text, numbers, figure
labels — fatal for a scientific poster. So we keep the decoration only in the margins
and paste the pixel-exact content back on top from the clean render.

Usage:
  python3 composite_content.py <clean_base.png> <decorated.png> <out.png>
          [--margin-top IN] [--margin-side IN] [--margin-bottom IN]
          [--w-in W] [--h-in H]

Margins must match the clean poster's `.poster` padding (default 1.4 / 1.4 / 1.2 in
on a 24x36 poster). The inset content rectangle from <clean_base.png> is scaled to the
decorated image and alpha-composited on top; the painted art remains in the border frame.
Pillow (auto-installed).
"""
import os
import subprocess
import sys


def _ensure(mod, pip=None):
    try:
        return __import__(mod)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", pip or mod])
        return __import__(mod)


def parse(argv):
    if len(argv) < 4:
        print(__doc__, file=sys.stderr); sys.exit(2)
    a = {"base": argv[1], "dec": argv[2], "out": argv[3],
         "mt": 1.4, "ms": 1.4, "mb": 1.2, "w": 24.0, "h": 36.0}
    i = 4
    while i < len(argv):
        t = argv[i]
        if t == "--margin-top": a["mt"] = float(argv[i + 1]); i += 2
        elif t == "--margin-side": a["ms"] = float(argv[i + 1]); i += 2
        elif t == "--margin-bottom": a["mb"] = float(argv[i + 1]); i += 2
        elif t == "--w-in": a["w"] = float(argv[i + 1]); i += 2
        elif t == "--h-in": a["h"] = float(argv[i + 1]); i += 2
        else: print(f"unknown arg: {t}", file=sys.stderr); sys.exit(2)
    return a


def main():
    a = parse(sys.argv)
    _ensure("PIL", "Pillow")
    from PIL import Image
    base = Image.open(a["base"]).convert("RGBA")
    dec = Image.open(a["dec"]).convert("RGBA")
    W, H = a["w"], a["h"]
    bx, by = base.width / W, base.height / H
    dx, dy = dec.width / W, dec.height / H
    # inset content rectangle in inches -> px in each image
    bl = (int(a["ms"] * bx), int(a["mt"] * by),
          int((W - a["ms"]) * bx), int((H - a["mb"]) * by))
    dl = (int(a["ms"] * dx), int(a["mt"] * dy),
          int((W - a["ms"]) * dx), int((H - a["mb"]) * dy))
    crop = base.crop(bl).resize((dl[2] - dl[0], dl[3] - dl[1]), Image.LANCZOS)
    out = dec.copy()
    out.alpha_composite(crop, (dl[0], dl[1]))
    out.convert("RGB").save(a["out"])
    print(f"OK -> {a['out']}  ({out.width}x{out.height})  "
          "(crisp content restored over decoration)")


if __name__ == "__main__":
    main()
