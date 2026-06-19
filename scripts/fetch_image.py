#!/usr/bin/env python3
"""Download themed decoration image(s) by direct URL, preserving transparency.

For "described" styles, after web-searching for real themed assets (transparent
PNGs / SVGs of the motif — characters, crests, ornaments), download them here and
place them in the poster's .decor layer as <img>.

Usage:
  python3 fetch_image.py <out.png> <url> [<url2> ...] [--max N] [--prefix name]

  single URL -> saved to <out.png>
  many URLs  -> saved next to <out.png> as <stem>_1.png, <stem>_2.png, ...
  --max N    longest side cap in px when re-encoding (default 900; keeps files sane)
  --prefix   override the per-file stem for multi-URL mode

Validates each download is a real image; flattens nothing (keeps alpha). SVGs are
saved as-is. Stdlib + Pillow (auto-installed).

NOTE on rights: themed/character art is often copyrighted. Use assets the user is
entitled to (their own, CC/public-domain, or clearly-licensed). The skill fetches
what it's pointed at; licensing is the user's call.
"""
import io
import os
import subprocess
import sys
import urllib.request

UA = "Mozilla/5.0 (poster-skill)"


def _ensure(mod, pip=None):
    try:
        return __import__(mod)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", pip or mod])
        return __import__(mod)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read(), r.headers.get("Content-Type", "")


def save(data, ctype, out, mx):
    if ("svg" in (ctype or "")) or data[:4] == b"<svg" or data[:5] == b"<?xml":
        svg = os.path.splitext(out)[0] + ".svg"
        open(svg, "wb").write(data)
        return svg, "svg"
    _ensure("PIL", "Pillow")
    from PIL import Image
    img = Image.open(io.BytesIO(data))
    img = img.convert("RGBA")
    if max(img.size) > mx:
        img.thumbnail((mx, mx), Image.LANCZOS)
    img.save(out, "PNG")
    return out, f"{img.width}x{img.height}"


def main():
    a = sys.argv[1:]
    if len(a) < 2:
        print(__doc__, file=sys.stderr); sys.exit(1)
    mx = 900
    if "--max" in a:
        i = a.index("--max"); mx = int(a[i + 1]); del a[i:i + 2]
    prefix = None
    if "--prefix" in a:
        i = a.index("--prefix"); prefix = a[i + 1]; del a[i:i + 2]
    out, urls = a[0], a[1:]

    if len(urls) == 1:
        targets = [(urls[0], out)]
    else:
        stem, ext = os.path.splitext(out)
        base = prefix or stem
        targets = [(u, f"{base}_{i + 1}{ext or '.png'}") for i, u in enumerate(urls)]

    n_ok = 0
    for url, dest in targets:
        try:
            data, ctype = fetch(url)
            if len(data) < 80:
                raise ValueError("empty response")
            saved, info = save(data, ctype, dest, mx)
            print(f"OK -> {saved}  ({info})")
            n_ok += 1
        except Exception as e:
            print(f"FAIL {url} -> {e}", file=sys.stderr)
    if n_ok == 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
