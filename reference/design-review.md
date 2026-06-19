# Design review (composes with the Anthropic "Design" plugin)

This skill builds the poster; the **Design** plugin (Anthropic's `knowledge-work-plugins`
marketplace) knows how to *critique* one. Run a design review pass before handoff.

- **If the Design plugin is installed**, hand it the rendered `preview.png` (and the
  `index.html`) and invoke its skills:
  - `design-critique` — first-impression, visual hierarchy, consistency, usability.
  - `accessibility-review` — WCAG 2.1 AA (contrast, readability).
  Apply the findings, re-export, re-check.
- **If it isn't installed**, run the distilled checklist below (same frameworks, adapted
  for a print poster). Either way, `scripts/contrast_check.py` automates the contrast part.

## What carries over from screen → print poster

Posters are print, viewed from 1–3 m, non-interactive. So **drop** the interaction-only
WCAG items (keyboard nav, focus order, touch targets, screen-reader/ARIA, time limits) and
**keep**:

### Critique (from `design-critique`)
1. **First impression (2 s):** does the eye land on the takeaway first? Is the one finding
   graspable from across the room?
2. **Visual hierarchy:** clear reading order (title → takeaway → centerpiece → support →
   refs)? Right things emphasized? Whitespace doing work (~40–50% visuals/space)?
3. **Consistency:** one accent family, consistent spacing, aligned cards, uniform caption
   style. Decoration in margins/whitespace only — never over text, figures, or numbers.
4. **Legibility from distance:** body ≥ ~24 pt at full size; nothing critical below it.

### Accessibility (from `accessibility-review`, WCAG 2.1 AA, print-relevant)
- **1.4.3 / 1.4.11 Contrast:** body text ≥ 4.5:1; large/bold text and UI/graphic strokes
  ≥ 3:1. **Run `python3 scripts/contrast_check.py index.html`** — it parses the `:root`
  vars + the `.takeaway` gradient stops and flags failing pairs (a vibrant band gradient
  often fails white text at its lightest stop — darken that stop or the text).
- **1.1.1 Alt text:** give every `<img>` a meaningful `alt` (figures, logos) — matters for
  any accessible PDF/Web version.
- **1.4.1 Don't rely on color alone:** if a figure encodes meaning by color, ensure labels
  exist (usually the paper's figures already do).
- **Readability:** generous line-height, not all-caps for long strings, adequate type size.

## Output

Produce a short critique in the `design-critique` / `accessibility-review` table format
(Finding | Severity 🔴/🟡/🟢 | Recommendation), then **apply the high-severity fixes**,
re-export, and re-run `contrast_check.py` until it passes. Report what changed.

## Claude Design (Anthropic Labs) bridge

[Claude Design](https://claude.ai/design) is a hosted visual-creation tool (claude.ai/design,
Pro/Max/Team/Enterprise). It has **no API/plugin**, so the bridge is manual — via its export
and its built-in **handoff to Claude Code**:

- **Design-system → palette.** Build/copy a design system (brand colors, type) in Claude
  Design, then plug those hex values into the poster's `:root` (and run `contrast_check.py`).
  This is the cleanest way to get a real, on-brand palette instead of guessed colors.
- **Concept/decor → assets.** Explore a layout or generate decorative/illustration assets in
  Claude Design, **export to HTML or PNG/PDF**, and bring them in: crop figures/ornaments
  with `fig_to_png.py`, place transparent art via the `.decor` layer.
- **Handoff back.** This skill's `index.html` is self-contained; share its look in Claude
  Design for stakeholder review, then apply comments here and re-export.

Keep this skill's `export_pdf.sh` as the source of truth for the **exact print size** — round-
trip through other tools, but verify the final PDF is the single correct page before printing.

## Contrast helper

```
python3 scripts/contrast_check.py index.html        # audit the poster's palette pairs
python3 scripts/contrast_check.py "#ffffff" "#13b5d0"  # check one fg/bg pair
```
