---
status: open
created: 2026-06-24
updated: 2026-06-24
occurrences: 1
context: minimap stage, ProjB Paper-Personality2Opioid-MISQ2026
fixed_in: ""
regressed: ""
---
"we don't need the coverage check."

The minimap's Coverage Check (claim/display crosswalk table) is redundant with the inline claim tags (`\cl`) and the display callouts (`\dcall`) already placed in each paragraph, so it is not needed by default. NOTE: the MedJournal exemplar includes one and JL kept it there, but removed it for the MISQ minimap, so make it OPTIONAL (off by default), not a mandatory section.

How to apply: do not emit the Coverage Check section by default; offer it only on request. The orphan-claim / orphan-display check can run as a SILENT lint (warn if a supported claim or a planned display is unplaced) instead of a printed table.

Fix:
