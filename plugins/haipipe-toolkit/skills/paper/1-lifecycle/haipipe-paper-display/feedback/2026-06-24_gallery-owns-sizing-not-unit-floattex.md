---
status: open
created: 2026-06-24
updated: 2026-06-24
occurrences: 1
context: display stage, ProjB Paper-Personality2Opioid-MISQ2026 (compacting the gallery PDF)
fixed_in: ""
regressed: ""
---
"no, don't change things here. please change .../0-lifecycle/4-display/4-display.tex"

Gallery-level PRESENTATION knobs live in the gallery file
`0-lifecycle/4-display/4-display.tex`, NOT in the unit `float.tex` or its source
(JSON / plot script). When JL asks to make the compiled gallery PDF more compact,
the size control (figure width cap, float `[H]` pinning, vertical-spacing
tightening, compact header) goes in the gallery preamble. The unit float.tex keeps
its OWN native full size, so the same display renders full-size when it is
`\input` into the manuscript or the minimap.

What went wrong: to compact the gallery I started editing a unit's source
(research-design.json width / unit float.tex). JL stopped it: presentation tweaks
for the gallery belong in 4-display.tex. The pattern that worked: a gallery-only
`\renewcommand{\includegraphics}` width cap (e.g. 0.42\textwidth) plus float
pinning in the 4-display.tex preamble, leaving every unit untouched.

Sibling: this is the SAME "4-display.tex is the single control surface" principle
as persist-user-display-comments-into-float-tex.md, but for SIZING rather than
comments; kept separate because it is a distinct mechanism (preamble layout knobs
vs a per-display comment log).

FIX (proposed): haipipe-paper-display must put all gallery-level presentation
(figure sizing / width cap, float pinning, spacing, header) in the 4-display.tex
preamble and NEVER mutate a unit float.tex or its source to change how the gallery
looks; units stay canonical/native size for the manuscript + minimap.

Fix:
