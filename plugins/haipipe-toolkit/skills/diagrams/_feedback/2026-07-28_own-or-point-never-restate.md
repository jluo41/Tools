---
status: open
created: 2026-07-28
updated: 2026-07-28
occurrences: 4
kind: defect
context: cross-page references
lands_in: "check.py + ref/writing-rules.md"
session: "the 2026-07-27 MISQ §3 Theory + display session (board: examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/0-lifecycle)"
fixed_in: ""
regressed: ""
---
Every stale record this session was a fact COPIED from a page that owned it.

Worst class: an S page quoting another unit's file paths. `S-Main-3`'s `> Display:` lane named
`versions/research-model-v2.pdf`, `assets/figure.png`, and the unit README's Status string. All
three went false within the hour when the unit changed. Pointing at
`3-display/S-Display-1a-hero-concept.md` instead would have stayed true, because that page is the
thing that gets updated when the unit changes.

The rule: a record either OWNS a fact or POINTS at its owner. It never restates it. An S page names
another unit's S PAGE, never its files.

Mechanizable: flag an S page quoting `versions/…`, `assets/…` or `candidates/…` of a unit it does
not own.
