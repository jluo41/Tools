---
status: open
created: 2026-07-28
updated: 2026-07-28
occurrences: 1
kind: convention
context: display naming
lands_in: "the display skills"
session: "the 2026-07-27 MISQ §3 Theory + display session (board: examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/0-lifecycle)"
fixed_in: ""
regressed: ""
---
JL renamed the caption noun from "Research model" to "Theory model" and the label key from
`fig:research-model` to `fig:theory-model`.

The reason is the transferable part: the unit README, S-Display-0 and S-Main-3's Q-Sec3Theory-2 all
ALREADY called it the theory model. Only the caption disagreed, and it sat one section away from
display01b's "Research design", so the two floats read as a near-duplicate pair.

The rule: when every page names a unit one way and one artifact names it another, the artifact is
the odd one out. Check the caption noun and the label key against what the pages call the unit
before the label is referenced anywhere, because renaming after a reference exists breaks pointers
silently.
