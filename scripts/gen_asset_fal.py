#!/usr/bin/env python3
"""Generate a themed, transparent-background asset with fal.ai (Nano Banana Pro).

Optional, higher-quality path for "described" styles: instead of scraping clip-art,
generate bespoke on-theme art with Google's Nano Banana Pro (Gemini 3 Pro Image) via
fal.ai. Better quality, no copyright scraping, exactly the subject you describe.

Needs a fal.ai API key (the user supplies it): set FAL_KEY or pass --key.
If no key is given, this exits non-zero so the skill falls back to web-sourced art.

Usage:
  FAL_KEY=... python3 gen_asset_fal.py "<subject prompt>" out.png
                       [--resolution 1K|2K|4K] [--aspect 1:1|16:9|9:16|4:3|3:4]
                       [--n N] [--key <FAL_KEY>] [--no-transparent] [--no-cutout]

Nano Banana Pro tends to render a transparency *checkerboard* instead of real alpha,
so by default the result is post-processed with rembg (auto-installed) to a clean
transparent cutout. Pass --no-cutout to keep the raw image. Generate the hero + a few
supporting poses with the SAME style prefix in the prompt for a cohesive set.

Example:
  gen_asset_fal.py "a majestic fluffy caracal cat, full body, sitting regally,
                    cute mascot illustration" hero.png --resolution 2K --aspect 3:4

A transparency instruction is appended to the prompt automatically (Nano Banana Pro
honors it and PNG keeps alpha) unless --no-transparent. Stdlib only.
"""
import json
import os
import sys
import urllib.request

ENDPOINT = "https://fal.run/fal-ai/nano-banana-pro"
TRANSPARENT_SUFFIX = (
    " . Isolated subject, centered, full subject visible, on a fully transparent "
    "background (alpha channel, no backdrop, no scene, no ground shadow), "
    "die-cut sticker style, clean edges."
)


def parse(argv):
    if len(argv) < 3:
        print(__doc__, file=sys.stderr); sys.exit(2)
    a = {"prompt": argv[1], "out": argv[2], "resolution": "2K",
         "aspect": "3:4", "n": 1, "key": os.environ.get("FAL_KEY", ""),
         "transparent": True, "cutout": True}
    i = 3
    while i < len(argv):
        t = argv[i]
        if t == "--resolution": a["resolution"] = argv[i + 1]; i += 2
        elif t == "--aspect":   a["aspect"] = argv[i + 1]; i += 2
        elif t == "--n":        a["n"] = int(argv[i + 1]); i += 2
        elif t == "--key":      a["key"] = argv[i + 1]; i += 2
        elif t == "--no-transparent": a["transparent"] = False; i += 1
        elif t == "--no-cutout": a["cutout"] = False; i += 1
        else: print(f"unknown arg: {t}", file=sys.stderr); sys.exit(2)
    return a


def cutout_bg(path):
    """Nano Banana renders a checkerboard instead of true alpha — strip it to real
    transparency with rembg (auto-installed). No-op if rembg can't be set up."""
    try:
        import subprocess as sp, sys as _s
        try:
            import rembg  # noqa: F401
        except ImportError:
            sp.check_call([_s.executable, "-m", "pip", "install", "--quiet",
                           "rembg", "onnxruntime"])
        from rembg import remove
        from PIL import Image
        remove(Image.open(path).convert("RGB")).save(path)
        return True
    except Exception as e:
        print(f"  (cutout skipped: {e}; image kept as-is)", file=sys.stderr)
        return False


def main():
    a = parse(sys.argv)
    if not a["key"]:
        print("NO_FAL_KEY: no fal.ai key (set FAL_KEY or --key). "
              "Falling back to web-sourced assets.", file=sys.stderr)
        sys.exit(3)

    prompt = a["prompt"] + (TRANSPARENT_SUFFIX if a["transparent"] else "")
    payload = json.dumps({
        "prompt": prompt,
        "num_images": a["n"],
        "output_format": "png",
        "resolution": a["resolution"],
        "aspect_ratio": a["aspect"],
    }).encode()

    req = urllib.request.Request(
        ENDPOINT, data=payload, method="POST",
        headers={"Authorization": f"Key {a['key']}",
                 "Content-Type": "application/json"})
    try:
        resp = json.load(urllib.request.urlopen(req, timeout=180))
    except Exception as e:
        body = getattr(e, "read", lambda: b"")() if hasattr(e, "read") else b""
        print(f"FAL_ERROR: {e} {body[:300]!r}", file=sys.stderr)
        print("Falling back to web-sourced assets.", file=sys.stderr)
        sys.exit(1)

    images = resp.get("images") or []
    if not images:
        print(f"FAL_ERROR: no images in response: {str(resp)[:300]}", file=sys.stderr)
        sys.exit(1)

    stem, ext = os.path.splitext(a["out"])
    saved = []
    for idx, im in enumerate(images):
        url = im.get("url")
        if not url:
            continue
        dest = a["out"] if len(images) == 1 else f"{stem}_{idx + 1}{ext or '.png'}"
        data = urllib.request.urlopen(
            urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}),
            timeout=120).read()
        with open(dest, "wb") as f:
            f.write(data)
        if a["transparent"] and a["cutout"]:
            cutout_bg(dest)  # strip the rendered checkerboard -> real alpha
        print(f"OK -> {dest}  ({im.get('width','?')}x{im.get('height','?')})")
        saved.append(dest)
    if not saved:
        sys.exit(1)


if __name__ == "__main__":
    main()
