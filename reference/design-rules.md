# Billboard / "Better Poster" Design Rules

Based on Morrison's "Better Poster" + ML-conference (CVPR-style) norms. Apply these
when filling the template.

## The core idea

A poster is the **tools for a 5–10 minute pitch**, not a shrunk paper. The title /
central takeaway carries ~90% of the communication. A passer-by should grasp the
finding in ~5 seconds from across the room.

## Layout (this template, portrait 24×36)

1. **Header** — venue line, title, authors, affiliations, logos.
2. **Takeaway band** — ONE giant plain-language finding (the hero) + QR code.
3. **Centerpiece** — the single best causal/ablation/main-result figure, large.
4. **Supporting columns** — left = "silent presenter" (problem + method, standalone
   readable while you're busy); right = results numbers + one backup figure ("ammo").
5. **Footer** — short references + contact.

## Hard rules

- **One takeaway.** Plain language, complete sentence, with the headline number.
- **Minimal text.** ~40–50% of area = visuals + whitespace. Cut everything optional.
  Method details and extra ablations go in the side columns, never the center.
- **Type sizes** (full size, via CSS vars): title 72–110pt; takeaway 90–150pt;
  headers 44–64pt; body 24–36pt (readable at 4–6 ft). Never below ~24pt for body.
- **Few, large, expressive figures.** No tiny multi-panel grids. Label clearly.
- **One accent color**, sans-serif throughout, generous margins.
- **QR ≥ ~4 in**, labeled "Scan for the paper".

## Interpretability-specific

- Centerpiece = what the paper uniquely **built or measured**: the mechanism/circuit,
  the causal ablation, or the steering/intervention dose-response.
- Headline takeaway = the actionable claim ("feature X mediates behavior Y; ablating it
  changes Z by N%"), not the methodology.
- Reserve side "ammo" figures for the Q&A questions you expect (generalization across
  models, capability-retention controls, baselines).

## Common failure modes to avoid

- Copy-pasting the abstract as body text.
- Landscape layout (violates the ICML workshop portrait rule).
- Five small figures instead of one big one.
- Tiny fonts; dense paragraphs; no clear reading path.
