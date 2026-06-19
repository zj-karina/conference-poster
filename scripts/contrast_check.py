#!/usr/bin/env python3
"""WCAG 2.1 contrast checker for a poster's color choices.

Print mode (manual):   python3 contrast_check.py <fg-hex> <bg-hex>
Audit mode (a poster): python3 contrast_check.py <index.html>

Audit mode parses the :root CSS variables (--ink, --muted, --accent, --bg,
--panel, --band-ink) and the .takeaway background gradient stops, then checks the
text/background pairs that actually occur on a poster and flags low contrast.

WCAG 2.1 AA thresholds: 4.5:1 for normal text, 3:1 for large text (>=24pt bold or
>=18.66pt). Poster body/headers are large by design, so 3:1 is the practical floor;
fine print (captions/refs) should still target 4.5:1. Pure stdlib.
"""
import re
import sys


def _lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hexstr):
    h = hexstr.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def ratio(fg, bg):
    l1, l2 = luminance(fg), luminance(bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def verdict(r, large=False):
    thr = 3.0 if large else 4.5
    return f"{r:4.1f}:1  {'PASS' if r >= thr else 'FAIL'} (need {thr}:1, {'large' if large else 'normal'})"


def parse_root(html):
    root = {}
    m = re.search(r":root\s*\{(.*?)\}", html, re.S)
    block = m.group(1) if m else html
    for name, val in re.findall(r"(--[\w-]+)\s*:\s*(#[0-9a-fA-F]{3,6})", block):
        root[name] = val
    grad = re.search(r"\.takeaway\{[^}]*?background:[^;]*?gradient\(([^)]*)\)", html, re.S)
    stops = re.findall(r"#[0-9a-fA-F]{3,6}", grad.group(1)) if grad else []
    return root, stops


def audit(path):
    html = open(path).read()
    r, stops = parse_root(html)
    g = r.get
    print(f"Contrast audit (WCAG 2.1 AA) — {path}\n")
    rows = []
    if g("--ink") and g("--bg"):
        rows.append(("body text on background", g("--ink"), g("--bg"), False))
    if g("--ink") and g("--panel"):
        rows.append(("body text on card/panel", g("--ink"), g("--panel"), False))
    if g("--muted") and g("--panel"):
        rows.append(("caption/muted on panel", g("--muted"), g("--panel"), False))
    if g("--accent") and g("--panel"):
        rows.append(("section header on panel", g("--accent"), g("--panel"), True))
    if g("--accent") and g("--bg"):
        rows.append(("accent on background", g("--accent"), g("--bg"), True))
    for i, stop in enumerate(stops):
        if g("--band-ink"):
            rows.append((f"band text on gradient stop {i + 1}", g("--band-ink"), stop, True))

    worst_fail = False
    for label, fg, bg, large in rows:
        r_ = ratio(fg, bg)
        thr = 3.0 if large else 4.5
        ok = r_ >= thr
        worst_fail = worst_fail or not ok
        mark = "ok  " if ok else "FAIL"
        print(f"  [{mark}] {label:32} {fg} on {bg}  {r_:4.1f}:1  (need {thr})")
    print("\n" + ("All checked pairs pass." if not worst_fail
                  else "Some pairs FAIL — darken the text or the offending background "
                       "(e.g. band gradient light stop), or enlarge/bolden that text."))
    return 0 if not worst_fail else 1


def main():
    a = sys.argv[1:]
    if len(a) == 1 and a[0].endswith((".html", ".htm")):
        sys.exit(audit(a[0]))
    if len(a) == 2:
        r = ratio(a[0], a[1])
        print(f"{a[0]} on {a[1]}")
        print("  normal text:", verdict(r, False))
        print("  large text :", verdict(r, True))
        sys.exit(0)
    print(__doc__, file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
