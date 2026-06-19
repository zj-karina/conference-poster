#!/usr/bin/env python3
"""Download an organization logo as a PNG, by domain, name, or direct image URL.

Resolution order:
  - a direct image URL (http...png/svg/jpg/...)  -> downloaded as-is
  - a domain (e.g. "openai.com", "mit.edu")       -> Clearbit logo, then favicon
  - a bare name (e.g. "OpenAI")                    -> guess <name>.com via Clearbit
    (BEST: let Claude web-search the official domain first, then pass that here)

Usage:
  python3 fetch_logo.py <domain|name|image-url> <out.png> [--size N]

  --size N   target longest side in px when re-encoding (default 512; favicon path)

Notes:
  - Clearbit Logo API (logo.clearbit.com/<domain>) needs no key and covers most
    companies + many universities. Favicon fallback is lower quality.
  - SVG inputs are saved as-is (Chrome renders them in the poster); other formats
    are normalized to PNG. Transparency is preserved.
Stdlib + Pillow (auto-installed) for validation/conversion.
"""
import io
import os
import re
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
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read(), r.headers.get("Content-Type", "")


def looks_like_url(s):
    return s.startswith("http://") or s.startswith("https://")


def looks_like_domain(s):
    return bool(re.fullmatch(r"[a-z0-9.-]+\.[a-z]{2,}", s.lower())) and " " not in s


def candidates(arg):
    """Yield (url, label) attempts for a domain/name/url."""
    if looks_like_url(arg):
        yield arg, "direct-url"
        return
    if looks_like_domain(arg):
        domain = arg.lower()
    else:
        # bare name -> naive .com guess (Claude should pass a real domain instead)
        domain = re.sub(r"[^a-z0-9]", "", arg.lower()) + ".com"
    yield f"https://logo.clearbit.com/{domain}?size=512", f"clearbit:{domain}"
    yield f"https://www.google.com/s2/favicons?domain={domain}&sz=256", f"favicon:{domain}"


def save_image(data, ctype, out, size):
    # SVG: keep vector.
    if ctype and "svg" in ctype or out.lower().endswith(".svg") or data[:5] == b"<?xml" or data[:4] == b"<svg":
        svg_out = os.path.splitext(out)[0] + ".svg"
        with open(svg_out, "wb") as f:
            f.write(data)
        return svg_out, "svg"
    _ensure("PIL", "Pillow")
    from PIL import Image
    img = Image.open(io.BytesIO(data))
    img = img.convert("RGBA")
    if max(img.size) > size:
        img.thumbnail((size, size), Image.LANCZOS)
    img.save(out, "PNG")
    return out, f"{img.width}x{img.height}"


def main():
    if len(sys.argv) < 3:
        print(__doc__, file=sys.stderr)
        sys.exit(1)
    arg, out = sys.argv[1], sys.argv[2]
    size = 512
    if "--size" in sys.argv:
        size = int(sys.argv[sys.argv.index("--size") + 1])

    last_err = None
    for url, label in candidates(arg):
        try:
            data, ctype = fetch(url)
            if len(data) < 80:  # empty/placeholder
                raise ValueError("empty response")
            saved, info = save_image(data, ctype, out, size)
            print(f"OK -> {saved}  ({label}, {info})")
            return
        except Exception as e:
            last_err = f"{label}: {e}"
            print(f"  tried {label} -> failed ({e})", file=sys.stderr)

    print(f"ERROR: could not fetch a logo for '{arg}'. Last: {last_err}\n"
          "Tip: web-search the org's official domain or a direct logo image URL "
          "(Wikipedia/Wikimedia SVG works well) and pass that.", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
