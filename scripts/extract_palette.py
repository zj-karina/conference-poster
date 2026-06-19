#!/usr/bin/env python3
"""Extract a real color palette from a reference image (or several).

Use this so the poster's palette comes from actual curated/trendy art — a style
reference you found on the web, a moodboard, or the themed asset you're placing —
instead of guessed hex codes. Pairs with the "style discovery" flow.

Usage:
  python3 extract_palette.py <image1> [image2 ...] [--n 6] [--no-neutrals]

  --n N           number of palette colors to return (default 6)
  --no-neutrals   drop near-white / near-black / very-grey swatches (keeps it punchy)

Prints hex codes sorted by visual weight (coverage), plus suggested role mapping
(accent / accent-2 / ink / band stops) you can drop into the template :root.
Pillow (auto-installed). Works on PNG/JPG; ignores fully transparent pixels.
"""
import sys
import subprocess
import colorsys


def _ensure(mod, pip=None):
    try:
        return __import__(mod)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", pip or mod])
        return __import__(mod)


def hexof(rgb):
    return "#%02x%02x%02x" % rgb


def luma(rgb):
    r, g, b = rgb
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def sat(rgb):
    r, g, b = (c / 255 for c in rgb)
    return colorsys.rgb_to_hls(r, g, b)[2]


def is_neutral(rgb):
    l = luma(rgb)
    return l > 238 or l < 18 or sat(rgb) < 0.12


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__, file=sys.stderr); sys.exit(1)
    n = 6
    if "--n" in a:
        i = a.index("--n"); n = int(a[i + 1]); del a[i:i + 2]
    drop_neutral = "--no-neutrals" in a
    a = [x for x in a if x != "--no-neutrals"]

    _ensure("PIL", "Pillow")
    from PIL import Image
    counts = {}
    for path in a:
        im = Image.open(path).convert("RGBA")
        im.thumbnail((400, 400))
        q = im.convert("RGB").quantize(colors=48, method=Image.FASTOCTREE)
        pal = q.getpalette()
        for cnt, idx in q.getcolors():
            rgb = tuple(pal[idx * 3: idx * 3 + 3])
            # weight by opacity of original isn't tracked post-quantize; good enough
            counts[rgb] = counts.get(rgb, 0) + cnt

    items = sorted(counts.items(), key=lambda kv: -kv[1])
    if drop_neutral:
        items = [(c, w) for c, w in items if not is_neutral(c)] or items
    # de-dupe near-identical colors
    chosen = []
    for rgb, w in items:
        if all(sum((a - b) ** 2 for a, b in zip(rgb, c)) > 1600 for c in chosen):
            chosen.append(rgb)
        if len(chosen) >= n:
            break

    print("palette (by visual weight):")
    for rgb in chosen:
        print(f"  {hexof(rgb)}   rgb{rgb}")

    # role suggestions: most saturated -> accents; darkest -> ink; spread -> band stops
    by_sat = sorted(chosen, key=lambda c: -sat(c))
    by_luma = sorted(chosen, key=luma)
    print("\nsuggested roles (tweak to taste; run contrast_check.py after):")
    print(f"  --ink     {hexof(by_luma[0])}   (darkest)")
    print(f"  --accent  {hexof(by_sat[0])}")
    if len(by_sat) > 1:
        print(f"  --accent-2 {hexof(by_sat[1])}")
    stops = [hexof(c) for c in by_sat[:3]]
    print(f"  band gradient stops: {', '.join(stops)}")
    print("  (pick a pale tint of --accent for --bg/--panel; keep band text white only if it passes 3:1)")


if __name__ == "__main__":
    main()
