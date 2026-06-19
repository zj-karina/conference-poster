#!/usr/bin/env python3
"""Hand a rendered poster image to fal.ai Nano Banana Pro (edit) to paint cohesive
themed decoration ON TOP of it — big, integrated art like a real illustrated poster,
instead of small clip-art stickers.

Workflow: build a CLEAN content poster (normal palette, no emoji, no decor), export it
to a PNG, then run this with a theme prompt. The image model decorates the margins
around the content in one cohesive style.

Usage:
  FAL_KEY=... python3 decorate_poster_fal.py <in_poster.png> <out.png>
             --theme "<theme/style, e.g. cute pastel My Little Pony ponies>"
             [--resolution 1K|2K|4K] [--aspect auto|3:4|2:3] [--key <FAL_KEY>]
             [--extra "<extra instructions>"]

The prompt hard-instructs the model to KEEP all text, numbers, figures and layout
exactly as-is and fully legible, and to decorate ONLY the empty margins/border. Output
defaults to 4K for print. Exits non-zero (caller falls back) if no key / on error.
Stdlib only.
"""
import base64
import json
import os
import sys
import urllib.request

ENDPOINT = "https://fal.run/fal-ai/nano-banana-pro/edit"

GUARD = (
    "This is a finished academic conference poster. DECORATE ONLY the empty margins, "
    "borders and corners around the existing content. ABSOLUTELY DO NOT change, redraw, "
    "move, recolor, cover or obscure any existing text, numbers, equations, charts, "
    "figures, the QR code, or the layout — every word and figure must stay pixel-identical "
    "and fully legible. Add large, cohesive, tasteful themed illustrations that frame the "
    "poster like a professionally illustrated poster (not small scattered stickers). "
    "Keep the same overall page proportions. Theme: "
)


def parse(argv):
    if len(argv) < 3:
        print(__doc__, file=sys.stderr); sys.exit(2)
    a = {"in": argv[1], "out": argv[2], "theme": "", "extra": "",
         "resolution": "4K", "aspect": "auto",
         "key": os.environ.get("FAL_KEY", "")}
    i = 3
    while i < len(argv):
        t = argv[i]
        if t == "--theme": a["theme"] = argv[i + 1]; i += 2
        elif t == "--extra": a["extra"] = argv[i + 1]; i += 2
        elif t == "--resolution": a["resolution"] = argv[i + 1]; i += 2
        elif t == "--aspect": a["aspect"] = argv[i + 1]; i += 2
        elif t == "--key": a["key"] = argv[i + 1]; i += 2
        else: print(f"unknown arg: {t}", file=sys.stderr); sys.exit(2)
    return a


def main():
    a = parse(sys.argv)
    if not a["key"]:
        print("NO_FAL_KEY: set FAL_KEY or --key. Falling back to manual decor.",
              file=sys.stderr)
        sys.exit(3)
    if not a["theme"]:
        print("ERROR: --theme is required.", file=sys.stderr); sys.exit(2)
    if not os.path.isfile(a["in"]):
        print(f"ERROR: input image not found: {a['in']}", file=sys.stderr); sys.exit(2)

    with open(a["in"], "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    data_uri = "data:image/png;base64," + b64

    prompt = GUARD + a["theme"]
    if a["extra"]:
        prompt += " . " + a["extra"]

    payload = json.dumps({
        "prompt": prompt,
        "image_urls": [data_uri],
        "output_format": "png",
        "resolution": a["resolution"],
        "aspect_ratio": a["aspect"],
        "num_images": 1,
    }).encode()

    req = urllib.request.Request(
        ENDPOINT, data=payload, method="POST",
        headers={"Authorization": f"Key {a['key']}",
                 "Content-Type": "application/json"})
    try:
        resp = json.load(urllib.request.urlopen(req, timeout=300))
    except Exception as e:
        body = e.read()[:300] if hasattr(e, "read") else b""
        print(f"FAL_ERROR: {e} {body!r}", file=sys.stderr)
        print("Falling back to manual decor.", file=sys.stderr)
        sys.exit(1)

    images = resp.get("images") or []
    url = images[0].get("url") if images else None
    if not url:
        print(f"FAL_ERROR: no image in response: {str(resp)[:300]}", file=sys.stderr)
        sys.exit(1)
    out_data = urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}),
        timeout=180).read()
    with open(a["out"], "wb") as f:
        f.write(out_data)
    w = images[0].get("width", "?"); h = images[0].get("height", "?")
    print(f"OK -> {a['out']}  ({w}x{h})")


if __name__ == "__main__":
    main()
