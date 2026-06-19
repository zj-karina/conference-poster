# Poster style presets

Pick one in the opening mini-interview, then set the matching CSS variables in
`:root` of `index.html`. Only the palette variables change — layout stays the same.
The user can always tweak `--accent` etc. afterward.

Each preset lists the four variables that define its look:
`--accent` (bands/rules/headers), `--accent-2` (gradient end / bullets),
`--panel` (card fill), `--band-ink` (text on the takeaway band).

## 1. Indigo (default)
Clean, modern ML look. Good neutral default.
```
--accent:#3b2fb0; --accent-2:#6a5cff; --panel:#f4f5fb; --band-ink:#ffffff;
```

## 2. Crimson academic
Warm, authoritative; pairs well with red/orange figures.
```
--accent:#9e1b32; --accent-2:#e0533d; --panel:#faf3f1; --band-ink:#ffffff;
```

## 3. Forest
Calm green; good for bio / systems / sustainability work.
```
--accent:#176b53; --accent-2:#3fb27f; --panel:#eef6f1; --band-ink:#ffffff;
```

## 4. Slate mono
Understated, high-print-fidelity, near-grayscale with one cool accent.
```
--accent:#2b3242; --accent-2:#5b6b8c; --panel:#f1f3f7; --band-ink:#ffffff;
```

## 5. Ocean / ICML blue
Conference-friendly blue.
```
--accent:#15508c; --accent-2:#2e9bd6; --panel:#eef4fa; --band-ink:#ffffff;
```

## 6. Sunset
High-energy, eye-catching from across the hall.
```
--accent:#b23a00; --accent-2:#f5a623; --panel:#fdf4e8; --band-ink:#ffffff;
```

## 7. Sailor Moon 🌙
Playful pink + blue + gold. Use a 3-stop band gradient for the full effect.
```
--accent:#e23a7e; --accent-2:#4f6ee0; --panel:#fdeef6; --band-ink:#ffffff;
/* also add: --gold:#ffcf3f;  and swap the .takeaway background to: */
/* background:linear-gradient(120deg,#e23a7e 0%,#b25fd0 48%,#4f6ee0 100%);
   border:.05in solid var(--gold); */
```

## Freeform / described styles (user describes a vibe in words)

When the user describes a style in their own words ("make it Sailor Moon", "cyberpunk
neon", "vintage botanical"), **don't invent emoji-only decor from memory** — that reads as
generic AI slop. Instead **research the style on the web** and build it from real assets:

**1. Research the palette (use real, curated colors — cite the source).**
Web-search e.g. `"<theme>" color palette hex`, `"<theme>" brand colors`, or
`Pantone <theme> palette`. Prefer curated sources (brand palettes, ColorsWall, SchemeColor,
coolors, Pantone trend reports) and pull the **actual hex codes**. Set `--accent`,
`--accent-2`, `--ink`, `--bg`, `--panel`, and the `.takeaway` gradient from them. Note the
source in your handoff so the user can verify.

**2. Fonts.** Swap the Google Fonts `<link>` and `body`/heading `font-family` to a pairing
that fits the vibe (rounded display for cute, mono for techy, serif for classic, condensed
for editorial). Keep body legible from a few feet.

**3. Find real themed art (the key step).** Web-search for **transparent PNGs** of the
theme's signature elements (characters, crests, ornaments, props):
`"<theme>" transparent png`, and good asset hosts (pngimg.com, openclipart.org, Wikimedia
Commons, stickpng). Use `WebFetch` on the gallery page to extract direct image URLs, then
download a spread with `scripts/fetch_image.py out.png <url1> <url2> ...` (saves
`out_1.png`, `out_2.png`, …, preserves transparency). Eyeball a contact sheet, pick the
best 4–8, and place them as `.decor img` with inline `top/left/right/bottom` + `width` in
the **whitespace zones**: the header logo slot (left of title), the strip above/below and
the sides of the (usually wide) centerpiece figure, and the page corners. Vary size and add
a slight `transform:rotate(...)`. Color emoji (🌈⭐✨) are fine as light *filler between*
the real images — not the main event.

**4. Keep content untouched and legible.** Theme the chrome, never the data. Decor must not
cover text, figures, or numbers — place in true whitespace; if unsure, fewer/larger pieces
in the margins. Render a preview and nudge positions until clean.

⚠️ **Rights:** themed/character art is usually copyrighted. `fetch_image.py` downloads what
you point it at; using it for a personal conference poster is one thing, redistributing is
another. Prefer the user's own assets, public-domain/CC, or clearly-licensed clip-art, and
flag this to the user.

### Worked example — "My Little Pony" 🦄 (research-driven, the right way)
- Palette (researched, ColorsWall #4144 / SchemeColor MLP): `--accent:#822b99;
  --accent-2:#ec058e; --ink:#351858; --bg:#f8f1fb; --panel:#f1e9f8;` band gradient
  `linear-gradient(120deg,#822b99,#ec058e 52%,#13b5d0)`, dashed white border.
- Fonts: `Quicksand` (body) + `Baloo 2` (display).
- Art: real transparent character PNGs from pngimg.com (`/uploads/my_pony/…`) — Twilight in
  the header logo slot; Rainbow Dash + Sunset in the strip above the matrix; Pinkie + Rarity
  flanking it. Emoji 🌈⭐💜 as filler. (See `~/poster/mzgEXubB5M/` for the built result.)

### Earlier example — "Sailor Moon" 🌙 (emoji-only; acceptable fallback when no assets found)
- Palette: `--accent:#ff1e9c; --accent-2:#ff7ad9; --panel:#ffe1f4; --bg:#fff0fa;` gradient
  `linear-gradient(120deg,#ff1e9c,#ff5cc4 50%,#ff9ad5)`, dashed `--gold` border; `Baloo 2`.
- Motifs: 🌙⭐💖🎀✨👑🐈‍⬛🪄 in corners/edges/figure sides. Use this lighter approach only if
  real transparent art can't be sourced or licensed.

Quick palette starting points (still verify per theme): *cyberpunk* → near-black bg, neon
`#39ff14`/`#ff00e6`, mono font. *Botanical* → cream bg, forest green + terracotta, serif.
*Scandi minimal* → white bg, one muted slate accent, no motifs, lots of whitespace.
Combine with any palette for a bolder hero: make the takeaway band near-black with a
colored sub-line instead of the gradient. In the `.takeaway` rule swap
`background:linear-gradient(...)` for `background:#14151a;` and keep `--band-ink:#ffffff`.

## Tips
- Match the accent loosely to the centerpiece figure's dominant color, or deliberately
  contrast it — avoid clashing (e.g. a green accent over an all-red heatmap).
- Keep ONE accent. The two accent vars should read as a family, not two colors.
- For accessibility/print, keep band text white on these (all dark enough).
