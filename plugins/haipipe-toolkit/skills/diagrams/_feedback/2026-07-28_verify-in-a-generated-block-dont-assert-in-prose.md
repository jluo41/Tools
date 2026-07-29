---
status: open
created: 2026-07-28
updated: 2026-07-28
occurrences: 3
kind: preference
context: provenance and counts
lands_in: "check.py + build.py"
session: "the 2026-07-27 MISQ §3 Theory + display session (board: examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/0-lifecycle)"
fixed_in: ""
regressed: ""
---
The pattern that actually worked this session, twice.

1. Asset provenance was ASSERTED in three hand-maintained places (float.tex header comments, the
   unit README, the S-Display page) and had drifted in all three. Replaced with a hashed manifest in
   a `# --- manifest:begin (generated) ---` block. Provenance became provable rather than claimed.
2. Adding ONE verification to that generator, "does float.tex actually point into assets/", instantly
   caught display01b pointing into `versions/` while its `assets/` held an unused parked render.
   No amount of careful reading had caught it.

Contrast: the citation count was wrong in two hand-written places and right only in the GENERATED
`form:` block.

The rule: if a claim can be measured, put it in a marker-delimited generated block with its
regenerate command. If it can be checked against disk, make the generator check it rather than
restating it in prose. Never write a header claim the generator does not verify: mine said
"assets/ holds the SELECTED artifact that float.tex points at" and did not check, which is exactly
how display01b's inversion hid.
