---
status: open
created: 2026-07-01
updated: 2026-07-01
occurrences: 1
context: §1 introduction citation gather (L6)
fixed_in: ""
regressed: ""
---

When the citation gather layer (L6) places references in the tex, the outline-narrative .md file (e.g. 1-introduction.md) must also be updated with inline parenthetical references on each sentence. The outline is the working document -- if it shows "naked" sentences without references while the tex has \citep{}, the outline becomes stale and misleading. The gather workflow should sync references back into the outline as part of L6 completion, not leave it to a separate manual pass.

Rule: after placing citations in tex during L6, update the corresponding outline sentence with parenthetical references (e.g. "sentence text (Author et al. Year).").
