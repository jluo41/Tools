---
status: open
created: 2026-06-27
updated: 2026-06-27
occurrences: 1
context: sl-init
fixed_in: ""
regressed: ""
---

Init Step 3 should be two phases, not one:

Phase 1 "Shallow talk": Moderator eyeballs ~10 items per round from the corpus, applies the draft guideline, surfaces to researcher. Fast, cheap, iterative. Exit when no new rules for 1 round. Goal: stabilize the guideline.

Phase 2 "Deep talk": LLM panel (3 personas) labels 100+ items systematically. Find exemplars (cleanest HIGH/LOW/NONE) and edges (panel disagrees). Surface edges to researcher for adjudication. Build the gold gallery + anchor set from this. Goal: validate the guideline and populate the gallery.

Current protocol jumps straight to "show 10-15 items" which is neither shallow (too many at once) nor deep (no panel, no systematic coverage). The two-phase split respects researcher attention in Phase 1 and uses LLM compute in Phase 2 only after the guideline stabilizes.

## Recurrences
