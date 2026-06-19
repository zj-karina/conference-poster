# conference-poster

A skill for Claude Code that generates a print-ready academic conference poster from a
paper.

Input: a paper (preprint URL or local PDF) and a target venue (conference/workshop name
or explicit dimensions). Output:

- a self-contained, browser-editable `index.html`, and
- a print-ready `poster.pdf` at the exact physical size, with a QR code to the paper.

The skill opens with a short interview (poster size, color style, logos), resolves the
venue's size requirements, extracts the title/results/figures from the paper, fetches the
real author list from OpenReview when the PDF is anonymized, and lays everything out in a
billboard format (Morrison "Better Poster").

Presets are included for common venues (e.g. ICML workshop: portrait 24x36 in / 61x91 cm)
and several color styles.

## Requirements

- Claude Code.
- Python 3. The figure and QR scripts auto-install their dependencies (`pymupdf`,
  `segno`, `Pillow`) on first use, or install them with `pip install -r requirements.txt`.
- Google Chrome or Chromium, used headless to export the PDF at the exact size.
- Optional: `poppler`. Not required; figure extraction uses PyMuPDF.
- Optional: a **fal.ai API key** (`FAL_KEY`) — for higher-quality, bespoke themed art
  generated with Nano Banana Pro when you describe a custom style. Without it, the skill
  uses web-sourced art instead.

## Install

Clone and run the installer:

```bash
git clone https://github.com/zj-karina/conference-poster.git
cd conference-poster
./install.sh
```

`install.sh` symlinks the skill into `~/.claude/skills/conference-poster`, so `git pull`
keeps it current. Use `--copy` to copy instead of symlink.

Manual alternative, clone directly into the skills directory:

```bash
git clone https://github.com/zj-karina/conference-poster.git \
  ~/.claude/skills/conference-poster
```

Restart Claude Code or start a new session.

## Usage

Examples:

- Make a poster for NeurIPS 2025, paper: `https://arxiv.org/abs/2403.12345`
- Build a 48x36 landscape poster from `~/papers/mywork.pdf`
- Turn an OpenReview link into an ICML workshop poster

Output is written to `./poster/<paper-slug>/`.

## How it works

| Step | Action | Script / reference |
|------|--------|--------------------|
| 0 | Interview: confirm size (preset or research), pick a style (preset or a described theme — researches a real palette + themed art; optionally generates art via fal.ai Nano Banana Pro if you provide a key), choose logos | `reference/poster-specs.md`, `reference/styles.md`, `scripts/fetch_logo.py`, `scripts/fetch_image.py`, `scripts/gen_asset_fal.py` |
| 1 | Resolve preprint URL / arXiv id / OpenReview link to a local PDF; fetch authors | `scripts/fetch_pdf.py`, `scripts/fetch_openreview_meta.py` |
| 2 | Extract text and figures (vector PDFs rasterized and trimmed) | `scripts/fig_to_png.py`, `scripts/extract_figures.py` |
| 3 | Fill the parametric template at the target size, style, and logos | `assets/template.html` |
| 4 | Generate the QR code | `scripts/make_qr.py` |
| 5 | Export to PDF at the exact size and verify dimensions | `scripts/export_pdf.sh` |

The scripts are usable standalone:

```bash
python3 scripts/fetch_pdf.py 2403.12345 paper.pdf
python3 scripts/fetch_openreview_meta.py https://openreview.net/forum?id=XXXX
python3 scripts/fig_to_png.py figures/fig1.pdf centerpiece.png --dpi 300
python3 scripts/fetch_logo.py openai.com logo.png
python3 scripts/make_qr.py https://arxiv.org/abs/2403.12345 qr.png
bash    scripts/export_pdf.sh index.html poster.pdf 24 36
```

## Customizing

- Size and orientation: set `:root --w/--h` and `@page { size: ... }` in `index.html`
  (they must match). Portrait is taller; landscape is wider, in which case widen
  `.support` to three columns.
- Color and type: accent color and type sizes are CSS variables at the top of the
  template. Named palettes are in `reference/styles.md`.
- Venue presets: edit the table in `reference/poster-specs.md`.

Design checklist: `reference/design-rules.md`.

## Before printing

Verify every metric, figure label, author name, and the physical dimensions against the
official venue page. Generated content can contain errors in numbers, equations,
citations, and size.

## License

MIT. See `LICENSE`.
