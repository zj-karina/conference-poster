#!/usr/bin/env python3
"""Pull figures out of a paper PDF — no poppler required (pure PyMuPDF).

Two extraction modes run together so you always get something usable:
  1. EMBEDDED  — saves each embedded raster image (img_p<page>_<n>.png). Best
     when the paper's figures are bitmaps. Tiny images (icons, logos, math
     glyphs) below --min-px are skipped.
  2. PAGES     — renders every page to page_<n>.png at --dpi. Best when figures
     are *vector* drawings (common in ML papers): pick the page with your figure
     and crop it, or use fig_to_png.py on the original figure file instead.

Usage:
  python3 extract_figures.py <paper.pdf> <out_dir> [--dpi N] [--min-px N] [--pages-only] [--embedded-only]

  --dpi N         page-render resolution (default 200)
  --min-px N      skip embedded images whose max side < N px (default 200)
  --pages-only    skip embedded-image extraction
  --embedded-only skip whole-page rendering

Prints a manifest so you can quickly choose a centerpiece. Relies on PyMuPDF.
"""
import os
import subprocess
import sys


def _ensure(mod, pip_name=None):
    try:
        return __import__(mod)
    except ImportError:
        print(f"installing {pip_name or mod} ...", file=sys.stderr)
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--quiet", pip_name or mod]
        )
        return __import__(mod)


def parse_args(argv):
    if len(argv) < 3:
        print(__doc__, file=sys.stderr)
        sys.exit(1)
    a = {"pdf": argv[1], "out": argv[2], "dpi": 200, "min_px": 200,
         "pages": True, "embedded": True}
    i = 3
    while i < len(argv):
        t = argv[i]
        if t == "--dpi":
            a["dpi"] = int(argv[i + 1]); i += 2
        elif t == "--min-px":
            a["min_px"] = int(argv[i + 1]); i += 2
        elif t == "--pages-only":
            a["embedded"] = False; i += 1
        elif t == "--embedded-only":
            a["pages"] = False; i += 1
        else:
            print(f"unknown arg: {t}", file=sys.stderr); sys.exit(1)
    return a


def main():
    a = parse_args(sys.argv)
    fitz = _ensure("fitz", "pymupdf")
    os.makedirs(a["out"], exist_ok=True)
    doc = fitz.open(a["pdf"])
    saved = []

    if a["embedded"]:
        for pno in range(doc.page_count):
            for n, img in enumerate(doc[pno].get_images(full=True)):
                xref = img[0]
                base = doc.extract_image(xref)
                w, h = base.get("width", 0), base.get("height", 0)
                if max(w, h) < a["min_px"]:
                    continue
                ext = base.get("ext", "png")
                fn = os.path.join(a["out"], f"img_p{pno + 1}_{n}.{ext}")
                with open(fn, "wb") as f:
                    f.write(base["image"])
                saved.append((fn, f"{w}x{h}", "embedded"))

    if a["pages"]:
        m = fitz.Matrix(a["dpi"] / 72, a["dpi"] / 72)
        for pno in range(doc.page_count):
            pix = doc[pno].get_pixmap(matrix=m, alpha=False)
            fn = os.path.join(a["out"], f"page_{pno + 1}.png")
            pix.save(fn)
            saved.append((fn, f"{pix.width}x{pix.height}", "page"))

    print(f"--- extracted {len(saved)} file(s) to {a['out']} ---")
    for fn, size, kind in saved:
        print(f"  [{kind:8}] {size:>11}  {os.path.basename(fn)}")
    if not saved:
        print("  (nothing met the size threshold; try --min-px 0 or --pages-only)")
    print("\nNext: pick a centerpiece, then tidy/crop it with fig_to_png.py if needed.")


if __name__ == "__main__":
    main()
