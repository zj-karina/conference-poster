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

## Clean academic mode (the serious default)

Themed decoration is **opt-in**. If the user wants a normal, professional academic poster —
or just doesn't ask for anything playful — do this and DON'T run the discovery pipeline:
- Pick a sober preset (Indigo / Ocean-ICML blue / Slate mono / Crimson), or match the
  centerpiece figure's color.
- **No `.decor` layer, no emoji, no slang/jokes.** Keep the worked-example tone neutral.
- Logos only (real org logos via `fetch_logo.py`), generous whitespace, crisp hierarchy.
- Still run `contrast_check.py`.

Make this an explicit choice in the opening interview ("Clean academic" vs "Themed/fun"),
and default to clean unless the user signals they want a vibe. Everything below is only for
the themed/fun path.

## Style discovery (turn ANY description into a real, on-trend design)

The input can be **anything**: a named aesthetic ("Sailor Moon", "cyberpunk"), a vibe
("cozy", "brutalist"), or even **an association with the paper itself** ("my work is about
weight-space geometry — it feels like cartography / star charts / topographic maps"). Never
fall back to a few emoji from memory — that reads as generic AI slop. Run this pipeline:

**0. Interpret → concrete visual directions.** If the description is indirect (a topic or
association), web-search it to turn it into 1–3 concrete aesthetics with signature elements,
e.g. `"<topic>" visual motifs aesthetic`, `"<association>" design inspiration`,
`<topic> poster moodboard`. If two strong directions emerge, offer them to the user with
**AskUserQuestion** (one line each) before committing — otherwise pick the best fit and say so.

**1. Trendy, real palette (cite the source).** Two good ways, prefer whichever gives richer
color:
   - **From a reference image:** find an on-aesthetic reference (moodboard, key art, the hero
     asset you'll use) and run `python3 scripts/extract_palette.py <ref.png> --no-neutrals` —
     it returns real hex codes by visual weight + role suggestions. This keeps the palette and
     the art coherent (and genuinely on-trend, since it's pulled from real design).
   - **From curated sources:** web-search `Pantone <theme> palette`, `"<theme>" color palette
     hex`, `<theme> brand colors` (ColorsWall, SchemeColor, coolors, Pantone trend reports).
   Then set `--ink/--accent/--accent-2/--bg/--panel` + the `.takeaway` gradient. Keep text
   colors dark enough and run `scripts/contrast_check.py` (extracted pastels are pretty but
   often fail as text — use them for `--bg/--panel` tints, keep a dark `--ink`).

**2. Fonts.** Swap the Google Fonts `<link>` and `body`/heading `font-family` to a pairing
that fits the vibe (rounded display for cute, mono for techy, serif for classic, condensed
for editorial). Keep body legible from a few feet.

**3. Get themed art and compose HERO-first (the wow factor).** Two sources:
   - **Best — generate it (fal.ai Nano Banana Pro), if the user gave a key.** Bespoke,
     high-quality, copyright-safe, exactly the subject you want, on a transparent background:
     `FAL_KEY=… python3 scripts/gen_asset_fal.py "<subject, e.g. a regal fluffy caracal
     mascot, full body>" hero.png --resolution 2K --aspect 3:4`. Generate the hero + a couple
     supporting pieces. (The script appends a transparency instruction and outputs PNG.)
   - **Fallback — find it on the web** (no key, or generation declined). Web-search
     **transparent PNGs**: `"<theme>" transparent png`, on asset hosts (pngimg.com,
     openclipart.org, Wikimedia Commons, stickpng). `WebFetch` the gallery page to extract
     direct image URLs, then download with `scripts/fetch_image.py out.png <url1> <url2> ...`.
   Eyeball a contact sheet either way, then compose like a designer, not by sprinkling:
   - **BE BOLD with size — this is the #1 mistake.** Timid little corner stickers look weak
     and don't read across a room. Assets should be **prominent**: a HERO at least
     ~4–6 in on its long side, supporting pieces ~2.5–3.5 in. If you catch yourself placing
     1–2 in images, they're too small — go bigger.
   - **One HERO image, large** — the single most iconic asset (a character, a group shot, a
     crest). Make it genuinely big and place it where it commands attention. It's fine for a
     hero to **bleed off the page edge** or sit partly behind a panel's empty corner — that
     reads as intentional design.
   - **2–4 supporting pieces, medium (not tiny)**, framing the content in the side/corner
     whitespace; let them overlap the page margin/edges rather than shrinking.
   - **Emoji (🌈⭐✨) only as light filler** between the real images — never the main event.
   Place each as `.decor img` with inline `top/left/right/bottom` + `width`; vary size and a
   slight `transform:rotate(...)`. A subtle on-theme background tint (from the extracted
   palette) ties it together.

**RECOMMENDED for themed posters — the decoration-forward layout (gives the reference look).**
The default grid is too dense for big art, so don't cram heroes into gaps or shrink them into
tiny stickers. Instead **inset the content and frame it with big perimeter art**, like a
proper illustrated poster:
- **Inset the content:** widen `.poster` side `padding` to ~1.6–1.9 in (from 0.6) so there
  are real left/right margins. The matrix/cards get a bit narrower — that's the trade-off.
- **Run BIG characters (~3 in) down BOTH margins**, 2–3 per side (top/middle/bottom), each
  anchored to the edge with `left:-0.5in`/`right:-0.5in` so it **bleeds off the page**
  (`overflow:hidden` clips cleanly). Mirror one with `transform:scaleX(-1)` for variety.
  This frames the whole poster the way illustrated reference posters do.
- Verify the bleeding art overlaps only **margins/card padding, not text** (crop and check
  the band's text edge and each card's inner text).
- **Bleed a single hero** at one corner if you want one dominant figure instead of a frame.
- Mention the small content trade-off and let the user pick — this is the path to the "wow".

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
