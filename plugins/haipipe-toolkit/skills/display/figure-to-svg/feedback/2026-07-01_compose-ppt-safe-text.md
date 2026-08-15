---
status: fixed
created: 2026-07-01
updated: 2026-07-04
occurrences: 1
context: figure-to-svg
fixed_in: "v1.2.0"
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

Fix: 2026-07-04 — compose_svg.py now writes BOTH variants in one run: the main output is PPT-safe
(one absolutely-positioned <text> per line; an optional per-item `content_ppt` list gives one
single-line <text> per sentence) and `*_wrapped.svg` keeps tspans for the visual diff
(`--no-wrapped` to skip). Panels also accept a measured `gradient` field
(`{"from","to","direction"}`) emitted as a <linearGradient>, so banner/header gradients come from
sampled colours instead of guessed flat fills.
