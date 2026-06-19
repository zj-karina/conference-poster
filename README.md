# conference-poster

A [Claude Code](https://claude.com/claude-code) **skill** that turns a paper into a
print-ready academic conference poster.

Give it a paper (a preprint link or a local PDF) and a venue (a conference/workshop
name, or explicit dimensions). It researches the venue's poster spec (size +
orientation), pulls the title / key results / figures out of the paper, lays them out
in a billboard-style ([Morrison "Better Poster"](https://www.youtube.com/watch?v=1RwJbhkCA58))
design, and exports:

- a **self-contained, browser-editable `index.html`**, and
- an **exact-size print-ready `poster.pdf`** with a QR code to the paper.

Works for any venue. Ships with presets for common ones (e.g. ICML workshop = portrait
24×36 in / 61×91 cm).

---

## What you can say

Once installed, just ask Claude Code things like:

- *"Make a poster for **NeurIPS 2025**, paper: https://arxiv.org/abs/2403.12345"*
- *"Build a **48×36 landscape** poster from `~/papers/mywork.pdf`"*
- *"Turn this OpenReview link into an **ICML workshop** poster: <url>"*

It will confirm the poster size with you, then produce the files under
`./poster/<paper-slug>/`.

---

## Requirements

- **Claude Code** (the skill runs inside it).
- **Python 3** — the figure/QR scripts auto-install their deps (`pymupdf`, `segno`,
  `Pillow`) on first use; or install them up front with `pip install -r requirements.txt`.
- **Google Chrome / Chromium** — used headless to export the PDF at the exact size.
- *Optional:* `poppler` (`pdfimages`/`pdftoppm`). **Not required** — figure extraction
  uses PyMuPDF specifically so it works without it.

---

## Install

### Option A — one-line installer (recommended)

```bash
git clone https://github.com/zj-karina/conference-poster.git
cd conference-poster
./install.sh
```

`install.sh` symlinks the skill into `~/.claude/skills/conference-poster` so
`git pull` keeps it up to date. Pass `--copy` to copy instead of symlink.

### Option B — manual

Clone (or copy) the repo straight into your Claude Code skills directory:

```bash
git clone https://github.com/zj-karina/conference-poster.git \
  ~/.claude/skills/conference-poster
```

Then restart Claude Code (or start a new session). Confirm it loaded by asking Claude
Code to "make a conference poster" — it should pick up the `conference-poster` skill.

---

## How it works

| Step | What happens | Script |
|------|--------------|--------|
| 0 | Resolve the venue's poster spec (preset or web research), confirm size with you | `reference/poster-specs.md` |
| 1 | Resolve a preprint URL / arXiv id / OpenReview link → local PDF | `scripts/fetch_pdf.py` |
| 2 | Extract text + figures (vector PDFs rasterized, whitespace-trimmed) | `scripts/fig_to_png.py`, `scripts/extract_figures.py` |
| 3 | Fill the parametric billboard template at the right size/orientation | `assets/template.html` |
| 4 | Generate the QR code | `scripts/make_qr.py` |
| 5 | Export to PDF at the exact physical size + verify dimensions | `scripts/export_pdf.sh` |

All scripts are usable standalone, e.g.:

```bash
python3 scripts/fetch_pdf.py 2403.12345 paper.pdf
python3 scripts/fig_to_png.py figures/fig1.pdf centerpiece.png --dpi 300
python3 scripts/make_qr.py https://arxiv.org/abs/2403.12345 qr.png
bash    scripts/export_pdf.sh index.html poster.pdf 24 36   # verify 24×36 in
```

---

## Customizing

- **Size / orientation:** set `:root --w/--h` **and** `@page { size: ... }` in
  `index.html` (must match). Portrait = taller; landscape = wider (also widen
  `.support` to 3 columns).
- **Look:** accent color and type sizes are CSS variables at the top of the template.
- **Add a venue preset:** edit the table in `reference/poster-specs.md`.

See `reference/design-rules.md` for the billboard-poster design checklist.

---

## ⚠️ Before printing

AI can misrender equations, numbers, citations — and even the poster *size*. Verify
every metric, figure label, author name, and the physical dimensions against the
official venue page before you order a print.

---

## License

[MIT](LICENSE).
