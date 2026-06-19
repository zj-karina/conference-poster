#!/usr/bin/env python3
"""Generate a high-contrast QR PNG pointing at the paper URL.

Usage:  python3 make_qr.py <url> <out.png> [scale]

Auto-installs `segno` (pure-python, no deps) if missing. `scale` controls pixel
density of the PNG (default 16 -> a crisp ~1000px image that prints sharply at
4 inches). Quiet-zone border kept for reliable scanning.
"""
import subprocess
import sys


def ensure_segno():
    try:
        import segno  # noqa: F401
        return
    except ImportError:
        print("installing segno ...", file=sys.stderr)
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--quiet", "segno"]
        )


def main():
    if len(sys.argv) < 3:
        print("usage: make_qr.py <url> <out.png> [scale]", file=sys.stderr)
        sys.exit(1)
    url, out = sys.argv[1], sys.argv[2]
    scale = int(sys.argv[3]) if len(sys.argv) > 3 else 16

    ensure_segno()
    import segno

    # error="m" (~15% recovery) is plenty for a clean poster QR.
    qr = segno.make(url, error="m")
    qr.save(out, scale=scale, border=4, dark="#14151a", light="#ffffff")
    print(f"OK -> {out}  (url: {url})")


if __name__ == "__main__":
    main()
