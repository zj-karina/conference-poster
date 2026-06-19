#!/usr/bin/env python3
"""Composite the crisp, correct poster content back over an AI-decorated image —
keeping the decoration *integrated* (visible in every gap/margin), not boxed.

Why: decorate_poster_fal.py paints a beautiful cohesive scene, but the image model
re-renders everything and WILL corrupt text, numbers and figure labels — fatal for a
scientific poster. Fix: re-render the clean poster with a TRANSPARENT background and
overlay it on the decorated image. Only the real ink (band, panels, text, figures) is
opaque and covers the corrupted content; everywhere else the decoration shows through —
so it stays integrated, not a hard rectangle.

Usage:
  python3 composite_content.py <clean.html> <decorated.png> <out.png>
          [--w-in W] [--h-in H] [--scale S]

Needs headless Chrome (same as export). Pillow auto-installed. Output matches the
decorated image's pixels; wrap to a print PDF afterward with img_to_pdf.py.
"""
import os
import re
import subprocess
import sys
import tempfile


def _ensure(mod, pip=None):
    try:
        return __import__(mod)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", pip or mod])
        return __import__(mod)


def find_chrome():
    for c in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome"):
        if subprocess.call(["bash", "-lc", f"command -v {c}"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
            return c
    print("ERROR: no Chrome/Chromium found (needed to render the overlay).", file=sys.stderr)
    sys.exit(1)


def parse(argv):
    if len(argv) < 4:
        print(__doc__, file=sys.stderr); sys.exit(2)
    a = {"html": argv[1], "dec": argv[2], "out": argv[3],
         "w": 24.0, "h": 36.0, "scale": 2.0}
    i = 4
    while i < len(argv):
        t = argv[i]
        if t == "--w-in": a["w"] = float(argv[i + 1]); i += 2
        elif t == "--h-in": a["h"] = float(argv[i + 1]); i += 2
        elif t == "--scale": a["scale"] = float(argv[i + 1]); i += 2
        else: print(f"unknown arg: {t}", file=sys.stderr); sys.exit(2)
    return a


def main():
    a = parse(sys.argv)
    _ensure("PIL", "Pillow")
    from PIL import Image

    html = open(a["html"]).read()
    # force a transparent background so only the real content is opaque
    override = ("<style>html,body{background:transparent!important}"
                ".poster{background:transparent!important}</style>")
    html_t = html.replace("</head>", override + "\n</head>", 1)
    d = os.path.dirname(os.path.abspath(a["html"]))
    tmp = tempfile.NamedTemporaryFile("w", suffix=".html", dir=d, delete=False)
    tmp.write(html_t); tmp.close()

    css_w, css_h = int(a["w"] * 96), int(a["h"] * 96)   # 96 CSS px/in
    overlay_png = tmp.name + ".png"
    chrome = find_chrome()
    subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
                    "--hide-scrollbars", "--default-background-color=00000000",
                    f"--force-device-scale-factor={a['scale']}",
                    f"--window-size={css_w},{css_h}",
                    f"--screenshot={overlay_png}", "file://" + tmp.name],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.unlink(tmp.name)
    if not os.path.exists(overlay_png):
        print("ERROR: overlay screenshot failed.", file=sys.stderr); sys.exit(1)

    ov = Image.open(overlay_png).convert("RGBA")
    dec = Image.open(a["dec"]).convert("RGBA").resize(ov.size, Image.LANCZOS)
    out = dec.copy()
    out.alpha_composite(ov)
    out.convert("RGB").save(a["out"])
    os.unlink(overlay_png)
    print(f"OK -> {a['out']}  ({out.width}x{out.height})  "
          "(crisp content over integrated decoration)")


if __name__ == "__main__":
    main()
