#!/usr/bin/env python3
"""Wrap a full-bleed poster image into a single PDF page at an exact physical size.

Used for the AI-decorated path, whose final poster is a raster image: place it on a
W x H inch page (default 24x36) so the print file is the right physical size.

Usage:
  python3 img_to_pdf.py <in.png> <out.pdf> [W_in H_in]

Uses PyMuPDF (auto-installed). Verifies the page size on save.
"""
import subprocess
import sys


def _ensure(mod, pip=None):
    try:
        return __import__(mod)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", pip or mod])
        return __import__(mod)


def main():
    if len(sys.argv) < 3:
        print(__doc__, file=sys.stderr); sys.exit(2)
    inp, out = sys.argv[1], sys.argv[2]
    w_in = float(sys.argv[3]) if len(sys.argv) > 3 else 24.0
    h_in = float(sys.argv[4]) if len(sys.argv) > 4 else 36.0
    fitz = _ensure("fitz", "pymupdf")
    w_pt, h_pt = w_in * 72, h_in * 72
    doc = fitz.open()
    page = doc.new_page(width=w_pt, height=h_pt)
    page.insert_image(fitz.Rect(0, 0, w_pt, h_pt), filename=inp)
    doc.save(out)
    r = fitz.open(out)[0].rect
    print(f"OK -> {out}  ({r.width/72:.2f}x{r.height/72:.2f} in, 1 page)")


if __name__ == "__main__":
    main()
