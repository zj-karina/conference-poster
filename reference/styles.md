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

## Dark takeaway band (modifier, optional)
Combine with any palette for a bolder hero: make the takeaway band near-black with a
colored sub-line instead of the gradient. In the `.takeaway` rule swap
`background:linear-gradient(...)` for `background:#14151a;` and keep `--band-ink:#ffffff`.

## Tips
- Match the accent loosely to the centerpiece figure's dominant color, or deliberately
  contrast it — avoid clashing (e.g. a green accent over an all-red heatmap).
- Keep ONE accent. The two accent vars should read as a family, not two colors.
- For accessibility/print, keep band text white on these (all dark enough).
