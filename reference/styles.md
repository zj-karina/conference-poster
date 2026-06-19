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
neon", "vintage botanical", "minimal Scandinavian"), don't fall back to a preset —
**translate the description into four concrete choices and build it literally:**

1. **Palette** — set `--accent`, `--accent-2`, `--panel`, `--bg`, `--ink`, and the
   `.takeaway` background gradient to colors that match the vibe.
2. **Fonts** — swap the Google Fonts `<link>` and `body`/heading `font-family` to a pairing
   that fits (e.g. rounded display for cute, mono for techy, serif for classic). Keep body
   legible from a few feet.
3. **Motifs** — pick a small set of theme emoji/symbols (4–8) and scatter them in the
   `.decor` layer: cluster a few in 2–3 corners, sprinkle the rest along the page edges and
   in the whitespace beside wide figures. Vary `font-size`, `opacity` (~0.5–1.0), and
   `transform:rotate(...)`. Keep them OUT of text and figure boxes. Color emoji render in
   headless Chrome (Noto Color Emoji).
4. **Optional themed images** — for richer decor (a character, a crest), place transparent
   PNGs via `.decor img` in corners, or fetch one with `scripts/fetch_logo.py <image-url>
   out.png` (it accepts any direct image URL). ⚠️ Watch copyright/print rights for
   character art — prefer the user's own assets or clearly-licensed clip-art; emoji/CSS
   decor is always safe.

Keep the **content** untouched and accurate — theme the chrome, not the data. Don't let
decoration reduce legibility; if in doubt, fewer, larger motifs in the margins.

### Worked example — "Sailor Moon" 🌙
- Palette: `--accent:#ff1e9c; --accent-2:#ff7ad9; --panel:#ffe1f4; --bg:#fff0fa;
  --ink:#6b1145; --gold:#ffd23f;` band gradient
  `linear-gradient(120deg,#ff1e9c,#ff5cc4 50%,#ff9ad5)` with a dashed `--gold` border.
- Fonts: rounded display — `Baloo 2` / `Fredoka` (cute, bubbly).
- Motifs: 🌙 ⭐ 💖 🎀 ✨ 👑 🐈‍⬛ 🪄 — clustered top-left + bottom-right, sprinkled along edges
  and beside the (wide) centerpiece figure.
- Tone (optional): playful section titles ("the drama / the recipe / the receipts / the
  proof") and copy — only if the user wants the humor, not by default.

Other quick mappings: *cyberpunk* → near-black bg, neon `#39ff14`/`#ff00e6`, mono font,
⚡🛰️🌃 motifs. *Botanical* → cream bg, forest green + terracotta, serif, 🌿🍃🌸. *Scandi
minimal* → white bg, one muted slate accent, no motifs, lots of whitespace.
Combine with any palette for a bolder hero: make the takeaway band near-black with a
colored sub-line instead of the gradient. In the `.takeaway` rule swap
`background:linear-gradient(...)` for `background:#14151a;` and keep `--band-ink:#ffffff`.

## Tips
- Match the accent loosely to the centerpiece figure's dominant color, or deliberately
  contrast it — avoid clashing (e.g. a green accent over an all-red heatmap).
- Keep ONE accent. The two accent vars should read as a family, not two colors.
- For accessibility/print, keep band text white on these (all dark enough).
