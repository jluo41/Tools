---
status: open
created: 2026-07-01
updated: 2026-07-01
occurrences: 1
context: figure-to-svg-replica
fixed_in: ""
regressed: ""
---
crop_qc.py assumes dark ink on a light background, so it over-flags white-on-dark icons (footer /
header bands) as LOOSE / OFF-CTR / CLIP and would tighten them to noise under --apply. It should
auto-detect inverted polarity (light glyph on a dark fill) — e.g. sample the crop's corner/median
background and invert the ink test accordingly — or at least accept a `--invert` / per-item polarity
hint so its geometry checks and --apply behave correctly on footer-style icons. Same background
assumption also caps color scoring on tiny anti-aliased crops. (See lesson/03, lesson/04.)

Fix:
