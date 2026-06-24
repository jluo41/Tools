---
status: open
created: 2026-06-24
updated: 2026-06-24
occurrences: 1
context: display stage, ProjB Paper-Personality2Opioid-MISQ2026 (Figure 4 discretion gradient)
fixed_in: ""
regressed: ""
---
"remove the text block... why something not necessary like the text box and text caption baked in the figure? did you use /haipipe-paper-display-figure?"

A data figure produced by display-figure must be CLEAN: just the plotted axes /
panels. Do NOT bake a text block, a title banner, an inline caption, or an
annotation box (e.g. a metformin call-out) INTO the rendered PNG/PDF. The caption
and any explanatory text belong in the LaTeX float (`float.tex` `\caption{...}`),
where they are editable, selectable, and consistent with the manuscript's
typography.

What went wrong: Figure 4 was rendered with a baked-in title + text block + a
metformin annotation box drawn inside the matplotlib canvas, making the figure
look thin/cluttered and duplicating what the LaTeX caption should carry. The fix
was to rebuild it single-panel via the display-figure method (gen script +
shared plot style), strip all baked text, and move the metformin note to the
LaTeX caption.

FIX (proposed): haipipe-paper-display-figure should render axis/data only and
emit the caption text to the unit float.tex, never onto the canvas. A self-check:
if the figure PNG contains a sentence, a title bar, or a boxed annotation, it is
wrong; move that text to `\caption{}`.

Fix:
