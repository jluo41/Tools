---
status: open
created: 2026-06-24
updated: 2026-06-24
occurrences: 1
context: display stage, ProjB Paper-Personality2Opioid-MISQ2026 (cross-cutting: applies to every lifecycle stage skill)
fixed_in: ""
regressed: ""
---
"this should be in the skills? I think for each skill in the lifecycle we should have a markdown named checklist."

Cross-cutting structural convention: EVERY lifecycle stage skill (seed, pitch,
claims, narrative, display, minimap, ...) should carry its own `CHECKLIST.md`
done-gate. The boilerplate that currently gets baked into the produced ARTIFACT
(e.g. the gallery-requirements paragraph written into 4-display.tex, the
done-criteria recited inline at each stage) belongs in the skill's checklist
instead, so the artifact stays clean and the gate lives next to the code.

What prompted it: the display gallery 4-display.tex had a "gallery requirements"
boilerplate paragraph embedded in the file. JL asked why that lives in the
artifact rather than the skill, and generalized it: each lifecycle skill should
own a named checklist markdown. I created `haipipe-paper-display/CHECKLIST.md`
live for the display stage, but the GENERAL rule (one CHECKLIST.md per lifecycle
stage skill) is not yet applied across the spine.

FIX (proposed): give each `1-lifecycle/haipipe-paper-<stage>/` skill a
`CHECKLIST.md` done-gate (gallery/stage requirements + exit criteria), have the
stage skill reference it instead of reciting boilerplate into the produced .tex,
and have the artifact point to the checklist by path. Roll out display's pattern
to seed/pitch/claims/narrative/minimap.

Fix:
