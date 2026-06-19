# Conference Poster Specs — research guide + presets

The skill must produce a poster at the **size and orientation the target venue
requires**. Specs vary a lot (portrait vs landscape; inches vs cm; A0 vs custom).
Never guess silently — resolve the spec, then confirm it with the user before building.

## How to resolve the spec for a named conference

1. **Check the presets table below** first. If the venue+year+track matches, use it.
2. Otherwise **web-search** for the official instructions. Good queries:
   - `"<conference> <year>" poster size instructions`
   - `"<conference> <year>" call for posters dimensions portrait landscape`
   - For workshops: add `workshop poster format` (workshop specs often differ from
     the main track — e.g. ICML main track is landscape, workshops are portrait).
3. **Prefer the official source**: the conference website (`*.cc`, `*.org`), the
   author/presenter guide, or the poster-printing partner page. Ignore random blogs.
4. **Extract**: orientation (portrait/landscape), max width × height **with units**,
   any board/mounting rules, print deadline, and the printing partner if named.
5. **Convert to inches** for the build (1 in = 2.54 cm). A0 = 33.1 × 46.8 in
   (84.1 × 118.9 cm). A1 = 23.4 × 33.1 in (59.4 × 84.1 cm).
6. **Confirm with the user** the final WIDTH × HEIGHT + orientation before building —
   this is the most error-prone step and a wrong size means a wasted print.

If research is inconclusive, ask the user for the exact size, or fall back to a safe
default (A0 portrait, 33.1 × 46.8 in) and clearly flag the assumption.

## Presets (verify against the official page if printing is imminent)

| Venue / track            | Orientation | Size (W × H)              | Notes |
|--------------------------|-------------|--------------------------|-------|
| ICML 2026 **workshop**   | portrait    | 24 × 36 in (61 × 91 cm)  | mandatory portrait; Hall A boards, conference tape only; order by Jun 15 2026 (forceposter.com). Full detail in `icml-2026-spec.md`. |
| ICML / NeurIPS main track| landscape   | up to 48 × 36 in         | wide; confirm exact max for the year. |
| NeurIPS (recent)         | portrait    | ~ A0 portrait (33.1 × 46.8 in) | confirm per year — has changed. |
| Generic A0 portrait      | portrait    | 33.1 × 46.8 in (84.1 × 118.9 cm) | safe default for many EU venues. |
| Generic A0 landscape     | landscape   | 46.8 × 33.1 in           | rotate A0. |
| US foam-board common     | landscape   | 48 × 36 in               | typical US easel board. |

> Sizes drift year to year. For any imminent print, re-verify on the official site;
> treat this table as a starting point, not gospel.

## Build checklist (any venue)

- [ ] Orientation + size confirmed with user, set in BOTH `:root --w/--h` and `@page`.
- [ ] Landscape? widen `.support` to 3 columns; portrait keeps 2.
- [ ] One giant plain-language takeaway, readable across the room (see `design-rules.md`).
- [ ] QR points to the correct paper URL (TEST it).
- [ ] Exported PDF verified: single page, exact target size (`export_pdf.sh` checks this).
- [ ] Every metric, equation, figure label, author name proofread (AI can err).
- [ ] Print deadline + mounting rules (tape/pins) noted to the user.
