---
status: open
created: 2026-06-24
updated: 2026-06-24
occurrences: 1
context: minimap stage, ProjB Paper-Personality2Opioid-MISQ2026
fixed_in: ""
regressed: ""
---
"too verbose, especially for narrative things." + "'demoted, defense' <- things here is very weird, we should remove it."

The per-paragraph narrative notes (`\nnote`) must be LEAN, on two counts. (1) LENGTH: one sharp clause (~10-15 words), not a multi-clause paragraph; the first MISQ draft averaged ~29 words/note (up to 39) and was condensed to ~16. (2) NO EDITORIAL PREFIX: drop the "verb, role." tag (keep/add/demoted/cut + role, e.g. "demoted, defense."); it is an internal interrogation tag carried over from the narrative and reads weird to a reader.

How to apply: when condensing the narrative `\rev{}` comments into minimap `\nnote`, strip the verb-role prefix and keep only the substantive one-clause note; cap the note length.

Fix:
