---
status: open
created: 2026-06-24
updated: 2026-06-24
occurrences: 1
context: minimap stage, ProjB Paper-Personality2Opioid-MISQ2026
fixed_in: ""
regressed: ""
---
"for the C1, C2, I think we need to show the content, instead of just using the index."

Claim tags in the minimap (`\cl{C1}`) must carry a short CONTENT gloss, not a bare index. `[C1]` alone forces the reader to flip to a crosswalk; `[C1: beyond rating]` is self-explanatory. The MedJournal exemplar already does this (`[C0: cohort & measures]`, `[C1: main intensity, primary]`).

How to apply: the `\cl` macro should auto-gloss each claim id to a short label via a per-paper lookup (C0..Cn -> short phrase), and multi-claim tags spell the glosses out. Seed the lookup from the claim titles in `2-claims.tex` so the minimap and the ledger stay consistent.

Fix:
