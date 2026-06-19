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

## Inputs (ask for whatever is missing — don't block on optional ones)

- **The paper** (required), as either:
  - a **preprint URL** — arXiv (`abs/`, `pdf/`, or bare id), OpenReview, or a direct
    `.pdf` link; or
  - a **local PDF path**.
- **The target venue** (required to size it), as either:
  - a **conference/workshop name** (e.g. "ICML 2026 workshop", "NeurIPS 2025", "CVPR
    2026") — the skill researches the spec; or
  - **explicit dimensions** ("A0 portrait", "48x36 in landscape", "61x91 cm").
- **The QR target URL** (strongly recommended) — usually the same preprint link. If
  unknown, leave a placeholder and tell the user to swap it before printing.
- **Optional:** lab/affiliation logos, accent color (hex), exact author list +
  affiliations, and which figure is the "centerpiece" (the single best main-result /
  causal / ablation figure). If not given, infer from the PDF.

## Workflow

Do these in order. Keep generated files in a working dir like `./poster/<paper-slug>/`
(create it; never write into the skill folder). Scripts live in this skill's `scripts/`.

### 0. Opening mini-interview (ask first, then build)

Before building, run a SHORT interview with the **AskUserQuestion** tool to lock the
look and logistics. Keep it to one batch of questions — don't interrogate. Skip any
question the user already answered in their request. Ask about:

1. **Poster size / venue** — confirm the final WIDTH × HEIGHT + orientation. Resolve it
   from `reference/poster-specs.md`: use explicit dims if given; else look up the venue
   in the presets table; else **web-search the official instructions** (queries + source
   vetting in that file), convert units to inches, and note board/tape/deadline rules.
   A wrong size = a wasted print, so always confirm. Fallback: A0 portrait (33.1×46.8 in),
   flagged.
2. **Style / palette** — offer the named presets in `reference/styles.md` (Indigo default,
   Crimson, Forest, Slate mono, Ocean/ICML blue, Sunset) and the optional dark band. The
   user may also **describe a style any way they like** — a named aesthetic ("Sailor Moon"),
   a vibe, or even **an association with the paper** ("my work is about weight-space geometry,
   it feels like star charts"). Run the **style-discovery pipeline** in `reference/styles.md`:
   interpret the description into concrete visual directions (web-search; offer 1–2 options via
   AskUserQuestion if open-ended) → pull a **trendy, real palette** (`scripts/extract_palette.py`
   from a reference image, or curated/Pantone sources, cite it) → get themed art and compose
   **HERO-first** (one big iconic image + a few supporting, emoji only as filler) in the
   `.decor` layer. Never emoji-only from memory. Then run `scripts/contrast_check.py`. Theme the
   chrome, never the data; mind asset licensing.
   - **Offer fal.ai (better quality).** As part of this question, tell the user that for
     **noticeably higher-quality, bespoke, copyright-safe** themed art you can use **fal.ai's
     Nano Banana Pro** (Gemini 3 Pro Image) — if they paste a fal.ai API key, generate assets
     with `scripts/gen_asset_fal.py "<subject>" out.png` (transparent PNG). **If they decline
     or have no key, proceed without it** using web-sourced art (`scripts/fetch_image.py`). Get
     the key via AskUserQuestion (they pick "Other" and paste it) or ask them to set `FAL_KEY`;
     never hard-code or log it.
3. **Logos** — ask which org/lab/university logos to include (if any). The user can just
   **name them** — fetch each with `python3 scripts/fetch_logo.py <name|domain|url>
   ./poster/<slug>/logo-<n>.png`. For a bare name, web-search the org's official domain
   first (or a Wikimedia SVG logo URL) and pass that for a clean, high-res result.
4. *(optional)* anything ambiguous: accent color override, which result is the centerpiece.

Apply the chosen palette by setting the CSS variables in `:root` (values in
`reference/styles.md`) and drop the fetched logos into the header `.logos` block.

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
  fal.ai Nano Banana Pro (Gemini 3 Pro Image) when the user supplies a `FAL_KEY`; exits
  non-zero (so you fall back to web-sourced art) if no key.
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
