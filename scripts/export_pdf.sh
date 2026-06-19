#!/usr/bin/env bash
# Export an HTML poster to a print-ready PDF at the exact physical size
# defined by the poster's own  @page { size: <W> <H> }  rule.
#
# Usage:  bash export_pdf.sh <input.html> <output.pdf> [WIDTH_IN HEIGHT_IN]
#
# WIDTH_IN/HEIGHT_IN (inches, optional) are only used to VERIFY the result.
# The actual size always comes from the HTML's @page rule — set that correctly
# when you build the poster for whatever conference/size you target.
#
# Uses headless Chrome with --no-pdf-header-footer so the CSS @page size is
# honored 1:1 (e.g. 24x36 in == 1728x2592 pt, single page).
#
# Troubleshooting:
#  - Wrong size / Letter page: ensure the HTML has  @page{ size:<W> <H>; margin:0 }
#    with real units (in/cm), matching the :root --w/--h variables.
#  - Blank figures: image src paths must be relative to the HTML file and exist.
#    Run this from the poster working dir, or pass absolute paths.
#  - Fonts/QR not loading: Chrome needs a moment for webfont; we pass a render delay.
set -euo pipefail

IN="${1:?usage: export_pdf.sh <input.html> <output.pdf> [WIDTH_IN HEIGHT_IN]}"
OUT="${2:?usage: export_pdf.sh <input.html> <output.pdf> [WIDTH_IN HEIGHT_IN]}"
EXP_W="${3:-}"
EXP_H="${4:-}"

# Resolve a Chrome-like binary.
CHROME=""
for c in google-chrome google-chrome-stable chromium chromium-browser chrome; do
  if command -v "$c" >/dev/null 2>&1; then CHROME="$c"; break; fi
done
if [ -z "$CHROME" ]; then
  echo "ERROR: no Chrome/Chromium found. Install Chrome, or open $IN in a browser" >&2
  echo "and Print -> Save as PDF with a custom page size matching the poster." >&2
  exit 1
fi

# Absolute file:// URL so relative image paths resolve correctly.
ABS_IN="$(cd "$(dirname "$IN")" && pwd)/$(basename "$IN")"

"$CHROME" \
  --headless=new \
  --disable-gpu \
  --no-sandbox \
  --no-pdf-header-footer \
  --run-all-compositor-stages-before-draw \
  --virtual-time-budget=4000 \
  --print-to-pdf="$OUT" \
  "file://$ABS_IN" 2> >(grep -v -E "DevTools|Fontconfig|GPU|Vulkan|GL " >&2 || true)

if [ ! -f "$OUT" ]; then
  echo "ERROR: PDF was not produced." >&2
  exit 1
fi
echo "OK -> $OUT"

# Verify page count + physical size. Prefer pdfinfo (poppler); fall back to
# PyMuPDF, which is commonly available. EXP_W/EXP_H (inches) checked if given.
if command -v pdfinfo >/dev/null 2>&1; then
  pdfinfo "$OUT" | grep -E "Pages|Page size" || true
fi
python3 - "$OUT" "${EXP_W:-0}" "${EXP_H:-0}" <<'PY' || true
import sys
try:
    import fitz
except ImportError:
    sys.exit(0)  # no verifier available; export already succeeded
out, ew, eh = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
d = fitz.open(out)
r = d[0].rect
w_in, h_in = r.width / 72, r.height / 72
print("verify: %d page(s), %.2f x %.2f in (%.0f x %.0f pt)"
      % (d.page_count, w_in, h_in, r.width, r.height))
if d.page_count != 1:
    print("  WARNING: expected a single page — check the .poster fixed sizing", file=sys.stderr)
if ew and eh:
    ok = abs(w_in - ew) <= 0.05 and abs(h_in - eh) <= 0.05
    print("  expected %.2f x %.2f in -> %s" % (ew, eh, "OK" if ok else "MISMATCH"))
    if not ok:
        print("  size mismatch — fix @page/:root in the HTML to match the target", file=sys.stderr)
PY
