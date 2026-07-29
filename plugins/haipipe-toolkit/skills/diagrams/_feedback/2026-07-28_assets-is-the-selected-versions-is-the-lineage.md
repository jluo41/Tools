---
status: open
created: 2026-07-28
updated: 2026-07-28
occurrences: 1
kind: convention
context: display unit folders
lands_in: "the display skills + asset-manifest.py"
session: "the 2026-07-27 MISQ §3 Theory + display session (board: examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/0-lifecycle)"
fixed_in: ""
regressed: ""
---
JL, verbatim: "I think the final selected one will go to .../assets, so
.../versions/research-model-v2.pdf could this one got the the assets?"

Not a new convention: 7 of the 9 units already pointed float.tex at `assets/`, and display01a and
display01b were the only two reaching into `versions/`. display01b was worse than bypassed, it was
INVERTED: float.tex pulled from `versions/` while `assets/` held an unused parked render.

The rule: `assets/` holds the selected artifact plus its generated manifest. `versions/` and
`candidates/` hold the lineage. float.tex points at the stable asset path and NEVER at versions/,
so promoting a new winner is one copy over the asset path and float.tex never changes.

Also learned: promoting means rebuilding `preview.pdf` in the same pass. Every preview I inspected
this session was a stale build showing a render the manuscript would not print.
