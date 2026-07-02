---
status: open
created: 2026-06-24
context: display stage; the 4-display.tex gallery PDF for Paper-Personality-Opioid-MedJournal
fixed_in: ""
---
The display PDF should flow in the logic of the mini-map or the narrative. They should be consistent.

Right now the display-stage gallery (`0-lifecycle/4-display/4-display.tex` -> `4-display.pdf`) orders its inlined display units by an ad-hoc Main/Supplement grouping that the author sets by hand. The order the reader meets the figures/tables in the gallery should instead MIRROR the order they are referenced in the narrative beats (`3-narrative`) and the minimap paragraph jobs (`5-minimap`): Figure 1, Table 1, Table 2, Figure 2 ... in the same sequence the manuscript introduces them. When the minimap or narrative reorders or re-anchors a display, the gallery `\input` order should update to match.

How to apply (later revision pass of the display stage skill, haipipe-paper-display / haipipe-paper-lifecycle display):
- Derive the gallery order from the minimap's per-paragraph display anchors (or the narrative beat order) rather than hand-set it; at minimum, cross-check the gallery order against the minimap/narrative and flag drift.
- Keep Main vs Supplement, but within each, order by first-reference in the narrative/minimap.
- Add a consistency check: every display referenced in the minimap appears in the gallery in reference order, and vice versa (no orphan displays, no out-of-order floats).
