#!/usr/bin/env python3
"""Fetch title + author list from an OpenReview submission.

Useful because OpenReview lists the real authors even when the PDF is anonymized
for review — so the poster gets the correct, complete author line.

Usage:
  python3 fetch_openreview_meta.py <forum-id-or-url> [out.json]

Prints a human-readable summary to stderr and JSON to stdout (or to out.json).
Stdlib only. Tries the v2 API first, then the legacy API.
"""
import json
import re
import sys
import urllib.request


def forum_id(s):
    m = re.search(r"[?&]id=([^&#\s]+)", s)
    if m:
        return m.group(1)
    return s.strip()


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return json.load(urllib.request.urlopen(req, timeout=30))


def val(content, key):
    v = content.get(key)
    return v.get("value") if isinstance(v, dict) else v


def main():
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        sys.exit(1)
    fid = forum_id(sys.argv[1])
    out = sys.argv[2] if len(sys.argv) > 2 else None

    note = None
    for base in ("https://api2.openreview.net", "https://api.openreview.net"):
        try:
            notes = get(f"{base}/notes?forum={fid}").get("notes", [])
            if notes:
                note = notes[0]
                break
        except Exception as e:
            print(f"{base}: {e}", file=sys.stderr)
    if not note:
        print(f"ERROR: could not fetch OpenReview note for forum '{fid}'.",
              file=sys.stderr)
        sys.exit(1)

    c = note.get("content", {})
    meta = {
        "forum": fid,
        "title": val(c, "title"),
        "authors": val(c, "authors") or [],
        "authorids": val(c, "authorids") or [],
        "venue": val(c, "venue") or val(c, "venueid"),
        "abstract": val(c, "abstract"),
        "pdf": f"https://openreview.net/pdf?id={fid}",
        "forum_url": f"https://openreview.net/forum?id={fid}",
    }

    print("title  :", meta["title"], file=sys.stderr)
    print("authors:", ", ".join(meta["authors"]) or "(none listed)", file=sys.stderr)
    if meta["venue"]:
        print("venue  :", meta["venue"], file=sys.stderr)

    text = json.dumps(meta, ensure_ascii=False, indent=2)
    if out:
        with open(out, "w") as f:
            f.write(text)
        print(f"OK -> {out}", file=sys.stderr)
    else:
        print(text)


if __name__ == "__main__":
    main()
