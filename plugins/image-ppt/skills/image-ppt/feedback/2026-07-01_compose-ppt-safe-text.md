---
status: open
created: 2026-07-01
updated: 2026-07-01
occurrences: 1
context: figure-to-svg-replica
fixed_in: ""
regressed: ""
---
compose_svg emits multi-line labels as tspans, which COLLAPSE to overlapping text when the SVG is
imported into PowerPoint via Insert SVG -> Convert to Shape (PPT ignores tspan dy line breaks).
Add a PPT-safe text mode: one absolutely-positioned <text> per line — ideally one per SENTENCE,
single line, overflow allowed — so each becomes one editable text box. Keep TWO variants from one
config: wrapped (for the visual original-vs-replica diff) and one-line (for PPT).

Also: sample panel/banner/gradient colours from the source instead of defaulting fills — a guessed
gray-blue panel was wrong; the originals were white panels with a darker navy banner and left->right
gradient headers. compose_svg should take measured panel fill + gradient endpoints.
See lesson/16, lesson/17.

Fix:
