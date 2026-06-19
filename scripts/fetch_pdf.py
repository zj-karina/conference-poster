#!/usr/bin/env python3
"""Resolve a preprint link to a local PDF file.

Handles the common cases so the rest of the pipeline always gets a real .pdf:
  - arXiv:        abs/<id>, pdf/<id>, or a bare 2403.12345 -> arxiv.org/pdf/<id>
  - OpenReview:   forum?id=X / pdf?id=X -> the PDF endpoint
  - direct .pdf:  downloaded as-is
  - already local: if the arg is an existing file, just echo its path

Usage:
  python3 fetch_pdf.py <url|arxiv-id|local-path> <out.pdf>

Uses only the stdlib (urllib). Prints the final local path on success.
"""
import os
import re
import sys
import urllib.request


UA = "Mozilla/5.0 (poster-skill) Python-urllib"


def resolve_url(s):
    s = s.strip()
    # Bare arXiv id, e.g. 2403.12345 or 2403.12345v2
    if re.fullmatch(r"\d{4}\.\d{4,5}(v\d+)?", s):
        return f"https://arxiv.org/pdf/{s}"
    # arXiv URL in any form -> pdf endpoint
    m = re.search(r"arxiv\.org/(abs|pdf)/([^\s?#]+)", s)
    if m:
        aid = m.group(2)
        aid = re.sub(r"\.pdf$", "", aid)
        return f"https://arxiv.org/pdf/{aid}"
    # OpenReview forum/pdf
    m = re.search(r"openreview\.net/(forum|pdf)\?id=([^\s&#]+)", s)
    if m:
        return f"https://openreview.net/pdf?id={m.group(2)}"
    return s  # assume it's already a direct link


def download(url, out):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    if not data[:5] == b"%PDF-":
        # Maybe an HTML landing page; warn but still save for inspection.
        print(f"WARNING: {url} did not return a PDF (got {data[:16]!r}). "
              "Pass a direct PDF link or download manually.", file=sys.stderr)
    with open(out, "wb") as f:
        f.write(data)
    return out


def main():
    if len(sys.argv) < 3:
        print(__doc__, file=sys.stderr)
        sys.exit(1)
    src, out = sys.argv[1], sys.argv[2]

    if os.path.isfile(src):
        print(os.path.abspath(src))
        return

    url = resolve_url(src)
    print(f"fetching: {url}", file=sys.stderr)
    try:
        download(url, out)
    except Exception as e:
        print(f"ERROR: could not download {url}: {e}", file=sys.stderr)
        print("Download the PDF manually and pass the local path instead.",
              file=sys.stderr)
        sys.exit(1)
    print(os.path.abspath(out))


if __name__ == "__main__":
    main()
