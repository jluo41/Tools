# Lesson 14: Regen grid size — 3×3 by default — and slice by central component

## The Problem
When regenerating a section's icons as one grid to slice (Lesson 13), a **dense grid bleeds**:
with a 4×4 grid the cells are small, and the model draws some icons — especially **human
figures** (a patient, a doctor) — larger than their cell, so they overflow the equal-division
cut line into the neighbour cell. The sliced neighbour then contains a stray chunk of the
oversized icon.

## The Symptom
A patch-oval crop with a blue slab across the top (the patient's shirt from the cell above);
a weight-scale crop with a stray dark line (the smartwatch above it).

## The Solution
- **Default to a 3×3 grid** (≤9 icons/grid) — it came out clean in practice and balances
  resolution/cost.
- **Drop to 2×2** for sections dense in human/photoreal figures (extra margin = bleed-proof).
- **Never 4×4** — that's where it bled.
- Prompt for **~60% cell fill with large margins**.
- Make the slicer **keep only the connected component(s) that reach the cell's CENTER** and drop
  blobs sitting only in the outer margin — removes residual neighbour-bleed regardless of grid size.

## Why It Works
Bigger cells give each icon a wide margin so overflow can't cross the cut. Central-component keep
exploits that bleed enters through an *edge* (far from centre) while the real icon straddles the
*centre*. 3×3 = ~5 grids for 37 icons; 2×2 is safest but ~2× the gen calls; 4×4 is too tight.

## When to Apply
Any grid-regeneration slice. Prefer 2×2 when a section is dominated by people/photoreal icons
the model tends to oversize; otherwise 3×3.

## Caveats
A genuinely multi-part icon (icon + a *detached* speech bubble) can lose the detached part if it
doesn't reach the central box — widen the central threshold for those, or generate them alone.
