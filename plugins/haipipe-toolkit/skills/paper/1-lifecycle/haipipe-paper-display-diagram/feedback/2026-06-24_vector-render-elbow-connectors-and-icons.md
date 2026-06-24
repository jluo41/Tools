---
status: open
created: 2026-06-24
context: display stage (vector renders), ProjB Paper-Personality2Opioid-MISQ2026
fixed_in: ""
---
"for the Figure 1's vector render, could we have the rectangle linked lines,
instead of curve lines [...] I think it is much better."
"for the vector results, do you think you have the ability to add the icon
things? I want to understand it."

Two requests about the FigureSpec vector renderer used for research-model /
research-design figures (haipipe-paper-display-diagram, scripts/figure_renderer.py).

1. ELBOW (rectangle) connectors -- APPLIED 2026-06-24.
   The renderer previously offered only curved (quadratic bezier) or straight
   diagonal edges. Added an `"ortho": true` edge option = right-angle / Manhattan
   elbow routing, with gap-based axis selection (route along the axis with the
   larger box-to-box clearance) so wide boxes do not backtrack. Set the MISQ
   research model's edges to `ortho`. JL: "much better." For MISQ/ISR/MS-IS
   research-model figures, elbow connectors should be the DEFAULT, not curves.

2. ICONS per construct -- OPEN.
   JL wants the vector render to optionally carry a small icon per node/construct
   (e.g. clinician, pill/dose, star/reputation, clipboard/controls) so the figure
   is easier to understand at a glance. The renderer currently has NO icon
   primitive (boxes + text + edges only). Options to weigh:
     (a) a small built-in vector glyph set (hand-authored SVG paths) keyed by a
         node `"icon": "<name>"` field -- crisp, scalable, grayscale-safe, on-brand;
         cost = authoring ~5-8 glyphs;
     (b) emoji/unicode in labels -- cheap but rsvg/font rendering is unreliable
         (tofu / monochrome), risky for print;
     (c) lean on the image-2 RASTER render for iconography (its strength) and keep
         the vector clean -- i.e. icons become a reason to pick the raster candidate.

FIX (proposed): (1) document `ortho` in the FigureSpec schema (done) and make
elbow the default for UTD-IS research-model figures in the display-diagram skill;
(2) decide the icon approach with the user -- if (a), add an `"icon"` node field +
a small glyph library to figure_renderer.py and document it.

Fix:
