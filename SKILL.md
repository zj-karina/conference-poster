---
name: conference-poster
description: >
  Turn a paper into a print-ready academic conference poster. Give it a paper
  (a preprint URL like arXiv/OpenReview, or a local PDF) and a target venue
  (conference/workshop name, or explicit dimensions); it researches the venue's
  poster spec (size + orientation), builds a billboard-style (Morrison "Better
  Poster") layout, and outputs a self-contained browser-editable HTML file plus
  an exact-size print-ready PDF with a QR code to the paper. Triggers when the
  user wants to make/build/create a conference or workshop poster, or turn a
  paper PDF/preprint link into a poster. Works for any venue; has presets for
  common ones (e.g. ICML workshop = portrait 24x36 in).
---

# Conference Poster Builder

Turn a paper into a print-ready academic poster for **any** conference, with minimal
effort and full control. The user supplies a paper (link or PDF) and a venue; the
skill figures out the required poster size, builds the layout, and exports a PDF at the
exact physical size. Output is one self-contained HTML file (editable live in the
browser) plus the PDF.

## What you require from the user (in this order)

1. **The venue** (FIRST, required): a link to the workshop / conference / paper page, or its
   name. You then **research the poster requirements** for it (size, orientation, board/tape,
   print deadline).
2. **The paper** (required): a **preprint link** (arXiv / OpenReview / direct `.pdf`) **or** an
   uploaded **PDF** of their paper.
3. **The style** (interview — see step 0C).
4. Optional: logos, exact author list, which figure is the centerpiece, QR target URL.

## Workflow

Do these in order. Keep generated files in a working dir like `./poster/<paper-slug>/`
(create it; never write into the skill folder). Scripts live in this skill's `scripts/`.
Use **AskUserQuestion** for the interview; ask in this sequence, don't interrogate, and skip
anything already given.

### 0A. Venue → research the poster spec (ask first)

Ask for the **workshop / conference / paper link or name**. Resolve its poster spec from
`reference/poster-specs.md`: presets table first; else **web-search the official
instructions**, extract orientation + max W×H (convert to inches) + board/tape/deadline rules.
**Confirm the final WIDTH × HEIGHT + orientation with the user** (a wrong size = a wasted
print). Fallback: A0 portrait (33.1×46.8 in), flagged.

### 0B. Paper

Ask for the **preprint link or a PDF**. (Fetched in step 1.)

### 0C. Style interview (formal vs informal, then branch)

Ask whether they want it **formal** or **informal / fun** — let them **describe in their own
words what they want**; if they're unsure, **propose a style** (offer 2–3 concrete ideas, incl.
a relevant association with their topic). Once they agree, branch:

- **FORMAL.** Ask them to describe the design approximately — **fonts and colors**. Build a
  clean academic poster: their palette (or a sober preset: Indigo / Ocean-ICML blue / Slate
  mono / Crimson), the requested fonts, **no `.decor`, no emoji, no slang**, logos only, lots
  of whitespace ("Clean academic mode" in `reference/styles.md`).

- **INFORMAL / fun.** Ask if they have a **fal.ai API key** (offer it — it gives by far the
  best result; get it via AskUserQuestion "Other" → paste, or `FAL_KEY`; never hard-code/log it).
  - **No key → web-preset flow** (like the original Floppa build). Pull a real, trendy palette
    (`scripts/extract_palette.py` / curated-Pantone, cite it) and **real themed art from the
    web** (`scripts/fetch_image.py`), and place the images **only where there is no text** —
    margins / whitespace / beside figures, composed HERO-first (decoration-forward layout in
    `reference/styles.md`). Never emoji-only from memory.
  - **Key given → paint-over flow** (best). (a) Build a **clean base poster first** — nice
    colors, **no decor/emoji**, roomy empty margins (`.poster` padding ~1.4in) — and rasterize
    it to `base.png`. (b) Hand it to Nano Banana Pro to paint cohesive themed decoration in the
    user's style: `scripts/decorate_poster_fal.py base.png decorated.png --theme "<their
    style>" --resolution 4K`. (c) ⚠️ The image model **corrupts text/numbers** — overlay the
    pixel-exact content back: `scripts/composite_content.py index.html decorated.png
    poster_final.png` (transparent re-render, decoration stays integrated, data stays exact).
    (d) Wrap to PDF: `scripts/img_to_pdf.py poster_final.png poster.pdf <W_in> <H_in>`.

### 0D. Logos (optional)

Ask which org/lab logos to include. The user can **name them**; fetch each with
`python3 scripts/fetch_logo.py <name|domain|url> ./poster/<slug>/logo-<n>.png` (web-search the
official domain / a Wikimedia SVG for a clean result). Drop them into the header `.logos` block.

### 1. Get the PDF + real metadata

- **PDF.** If given a **URL or arXiv id**: `python3 scripts/fetch_pdf.py <url|id>
  ./poster/<slug>/paper.pdf` (resolves arXiv/OpenReview to the real PDF; stdlib-only).
  If given a **local path**: use it directly. If a download fails (paywall/landing page),
  ask the user to drop the PDF in.
- **Authors (important).** If the paper is on **OpenReview**, the PDF is often anonymized
  but the real author list is public — fetch it:
  `python3 scripts/fetch_openreview_meta.py <forum-id-or-url>` returns title, **full author
  list**, and venue. Use these authors verbatim (don't trust an "Anonymous Authors" PDF).
  For arXiv, the PDF/abs page authors are reliable.

### 2. Extract content + figures from the PDF

Pull text and figures. Helpers are PyMuPDF-based and need **no poppler**:

- Read the PDF with the Read tool to get title, authors, affiliations, abstract,
  contributions, method, key results, references.
- **Figures shipped as separate files** (often vector `.pdf`): rasterize each, auto-trimmed:
  `python3 scripts/fig_to_png.py fig.pdf ./poster/<slug>/centerpiece.png --dpi 300`
  (works on `.pdf` pages and `.png/.jpg`; trims whitespace).
- **Only the paper PDF**: `python3 scripts/extract_figures.py paper.pdf ./poster/<slug>/_figs`
  dumps embedded rasters + renders every page with a manifest; pick a centerpiece, then
  clean it with `fig_to_png.py`.
- Legacy fallback if poppler *is* present: `pdfimages -all` / `pdftoppm -png -r 200`.
- If extraction fails entirely, proceed with placeholders and ask for figure PNGs.

Capture specifically:
- **Title**, **authors**, **affiliations**, **venue line**.
- The **single headline finding** in plain language → the giant central takeaway. A
  complete sentence a non-expert grasps in 5 seconds. This carries ~90% of the poster —
  spend real effort here.
- 3–5 **contributions / key results** as short bullets (with the actual numbers).
- A 1–2 sentence **method** summary.
- The **centerpiece figure** + 1–3 **supporting figures**.
- 3–6 **key references** (short form).

### 3. Build the poster HTML at the right size

Copy `assets/template.html` into the working dir as `index.html`, then:

1. **Set the physical size** from step 0 in BOTH places (they must match): the `:root`
   `--w` / `--h` variables AND the `@page { size: <W> <H> }` rule. Use real units (in/cm).
2. For **landscape** posters, widen `.support` to 3 columns (noted inline in the template).
3. Fill the marked `<!-- FILL: ... -->` sections with the paper content.
4. **Apply the style from step 0C:** set the `:root` palette + fonts; for **formal** and for
   the **paint-over (informal+key)** flows build this as the *clean* poster (no `.decor`, no
   emoji; paint-over also uses roomy ~1.4in margins). For **informal without a key**, also
   place the web-sourced art in the `.decor` layer (HERO-first, only where there's no text).

Design rules to honor (Morrison "Better Poster" + ML-conference norms — see
`reference/design-rules.md`):
- **One giant plain-language takeaway** dominates the center (the hero).
- **Minimal text.** ~40–50% of area = visuals/whitespace. Cut ruthlessly. The poster is
  the tools for a 5–10 min pitch, not a copy of the paper.
- **Type sizes** scale with poster size; the template's CSS vars are tuned for ~24×36 —
  bump them up for A0/larger. Body must be readable from ~4–6 ft.
- **QR ≥ ~4 in**, near the takeaway, labeled "Scan for the paper". Sans-serif, one accent
  color, generous margins.

Generate the QR with `python3 scripts/make_qr.py <url> ./poster/<slug>/qr.png` (auto-installs
`segno`). Embed it (the template references `qr.png`).

### 4. Render the PDF at the exact size

`bash scripts/export_pdf.sh ./poster/<slug>/index.html ./poster/<slug>/poster.pdf <W_in> <H_in>`
(pass the target width/height in inches so it verifies the output). Uses headless Chrome
honoring the CSS `@page` size, then checks it's a single page at the expected dimensions.
If size/page count is wrong, fix `@page`/`:root` to match and re-run.

**For the paint-over (informal + fal.ai key) flow**, this export is the *clean base*: rasterize
it to `base.png`, then run the decorate → composite → `img_to_pdf` chain from step 0C to produce
the final decorated `poster.pdf`.

### 4b. Design review (composes with the Anthropic "Design" plugin)

Before handoff, run a design + accessibility pass on the rendered poster — see
`reference/design-review.md`.
- Render a `preview.png` (e.g. `python3 -c "import fitz; fitz.open('poster.pdf')[0]
  .get_pixmap(matrix=fitz.Matrix(110/72,110/72)).save('preview.png')"`) and look at it.
- **Always run** `python3 scripts/contrast_check.py ./poster/<slug>/index.html` — it audits
  the `:root` colors + `.takeaway` gradient stops against WCAG (a vibrant band gradient often
  fails white text at its lightest stop; darken that stop). Fix failures, re-export, re-check.
- If the **Design plugin** is installed, invoke its `design-critique` and
  `accessibility-review` skills on the preview/HTML and apply the high-severity findings
  (hierarchy, consistency, contrast, legibility). If not, use the distilled checklist in
  `reference/design-review.md`. Then re-export.

### 5. Hand off

Report to the user:
- Paths to `index.html` (editable) and `poster.pdf` (print-ready), and the final size.
- How to **edit**: open `index.html` in Chrome; text is editable inline; swap images by
  replacing files; tweak accent color / sizes via the CSS variables; re-run step 4.
- **Print/logistics**: the size + orientation, the print deadline and mounting rules you
  found in step 0 (tape vs pins, board location), and recommended 100–300 DPI at full size.
  For ICML workshop specifically, see `reference/icml-2026-spec.md`.
- ⚠️ **Proofread before printing**: AI can misrender equations, numbers, citations, and
  the poster *size*. Tell the user to verify every metric, figure label, author name, and
  the physical dimensions against the official venue page.

## Files

- `assets/template.html` — self-contained billboard poster template (inline CSS),
  parametric size (set `:root --w/--h` + `@page`); portrait or landscape.
- `scripts/fetch_pdf.py` — resolve a preprint URL / arXiv id to a local PDF (stdlib only).
- `scripts/fetch_openreview_meta.py` — title + full author list + venue from an OpenReview
  submission (the real authors, even when the PDF is anonymized). Stdlib only.
- `scripts/fetch_logo.py` — download an org logo as PNG by name / domain / image URL
  (Clearbit + favicon fallback). For a name, web-search the real domain first.
- `scripts/fetch_image.py` — download themed decoration art (transparent PNG/SVG) by direct
  URL(s) for "described" styles; preserves transparency, resizes sanely.
- `scripts/extract_palette.py` — pull a real, on-trend color palette (hex + role
  suggestions) from a reference image / the hero asset, for the style-discovery flow.
- `scripts/gen_asset_fal.py` — OPTIONAL: generate bespoke transparent-PNG themed art via
  fal.ai Nano Banana Pro (Gemini 3 Pro Image) when the user supplies a `FAL_KEY`; auto-cuts
  the rendered checkerboard with rembg; exits non-zero (fall back) if no key.
- `scripts/decorate_poster_fal.py` — OPTIONAL (preferred themed flow): hand a clean rendered
  poster PNG to Nano Banana Pro (edit) to paint cohesive themed decoration into the margins.
- `scripts/composite_content.py` — re-render the clean HTML with a transparent background and
  overlay it on the decorated image, so data stays pixel-exact AND the decoration stays
  integrated (not boxed). Mandatory after decorate (the edit model corrupts text/numbers).
- `scripts/img_to_pdf.py` — wrap a full-bleed poster image into a single PDF page at exact size.
- `scripts/extract_figures.py` — dump embedded images + render pages from a paper PDF
  (PyMuPDF, no poppler), with a manifest, to pick a centerpiece.
- `scripts/fig_to_png.py` — rasterize one figure (vector PDF page or image) to a
  whitespace-trimmed, high-DPI PNG ready for the poster.
- `scripts/make_qr.py` — QR PNG generator (auto-installs `segno`).
- `scripts/contrast_check.py` — WCAG 2.1 contrast audit of the poster's palette (parses
  `:root` + the `.takeaway` gradient); also checks a single fg/bg pair.
- `scripts/export_pdf.sh` — headless-Chrome HTML→PDF at the poster's exact size; verifies
  single page + dimensions (PyMuPDF fallback when poppler is absent).
- `reference/poster-specs.md` — how to research any venue's spec + a presets table.
- `reference/styles.md` — named color/style presets + the research-driven "described styles".
- `reference/design-review.md` — design + accessibility review pass; composes with the
  Anthropic "Design" plugin (design-critique / accessibility-review) or runs a distilled
  print-poster checklist standalone.
- `reference/icml-2026-spec.md` — detailed ICML 2026 workshop spec + logistics (one preset).
- `reference/design-rules.md` — billboard / Better-Poster design checklist.
