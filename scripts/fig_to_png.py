#!/usr/bin/env python3
"""Rasterize a single figure (vector PDF page, or any image) to a poster-ready PNG.

Most ML papers ship figures as *vector* PDFs (e.g. fig1.pdf). Those cannot be
embedded in an HTML poster directly and must be rasterized at high DPI. This
renders the figure crisply and auto-trims the surrounding whitespace so it sits
cleanly in the poster's figure boxes.

Usage:
  python3 fig_to_png.py <input.pdf|input.png|...> <out.png> [--dpi N] [--page K]
                        [--pad PX] [--no-trim] [--bg R,G,B]

  --dpi N     render resolution (default 300; keep >=200 for print sharpness)
  --page K    page index for multi-page PDFs (0-based, default 0)
  --pad PX    whitespace padding kept around content after trim (default 24)
  --no-trim   skip the auto-crop of surrounding whitespace
  --bg R,G,B  background color flattened behind transparency (default 255,255,255)

Auto-installs Pillow (for trim) and relies on PyMuPDF (`fitz`) for PDF rendering.
For non-PDF inputs it just trims+pads and re-saves as PNG.
"""
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
    a = {"in": argv[1], "out": argv[2], "dpi": 300, "page": 0,
         "pad": 24, "trim": True, "bg": (255, 255, 255)}
    i = 3
    while i < len(argv):
        t = argv[i]
        if t == "--dpi":
            a["dpi"] = int(argv[i + 1]); i += 2
        elif t == "--page":
            a["page"] = int(argv[i + 1]); i += 2
        elif t == "--pad":
            a["pad"] = int(argv[i + 1]); i += 2
        elif t == "--no-trim":
            a["trim"] = False; i += 1
        elif t == "--bg":
            a["bg"] = tuple(int(x) for x in argv[i + 1].split(",")); i += 2
        else:
            print(f"unknown arg: {t}", file=sys.stderr); sys.exit(1)
    return a


def render_pdf_page(path, page, dpi):
    fitz = _ensure("fitz", "pymupdf")
    doc = fitz.open(path)
    if page >= doc.page_count:
        print(f"ERROR: page {page} out of range (doc has {doc.page_count})",
              file=sys.stderr)
        sys.exit(1)
    pix = doc[page].get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72), alpha=False)
    _ensure("PIL", "Pillow")
    import io
    from PIL import Image
    return Image.open(io.BytesIO(pix.tobytes("png")))


def main():
    a = parse_args(sys.argv)
    _ensure("PIL", "Pillow")
    from PIL import Image as PImage, ImageChops

    if a["in"].lower().endswith(".pdf"):
        img = render_pdf_page(a["in"], a["page"], a["dpi"])
    else:
        img = PImage.open(a["in"])

    # Flatten transparency onto a solid background.
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGBA")
        bg = PImage.new("RGBA", img.size, a["bg"] + (255,))
        img = PImage.alpha_composite(bg, img)
    img = img.convert("RGB")

    if a["trim"]:
        bg = PImage.new("RGB", img.size, a["bg"])
        diff = ImageChops.difference(img, bg)
        box = diff.getbbox()
        if box:
            p = a["pad"]
            box = (max(0, box[0] - p), max(0, box[1] - p),
                   min(img.width, box[2] + p), min(img.height, box[3] + p))
            img = img.crop(box)

    img.save(a["out"], "PNG", optimize=True)
    print(f"OK -> {a['out']}  ({img.width}x{img.height}px, dpi~{a['dpi']})")


if __name__ == "__main__":
    main()
