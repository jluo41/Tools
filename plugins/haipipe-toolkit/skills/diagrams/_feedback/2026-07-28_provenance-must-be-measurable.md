---
status: open
created: 2026-07-28
updated: 2026-07-28
occurrences: 1
kind: preference
context: display assets
lands_in: "asset-manifest.py + the display skills"
session: "the 2026-07-27 MISQ §3 Theory + display session (board: examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/0-lifecycle)"
fixed_in: ""
regressed: ""
---
JL, verbatim: "how do we know where is this figure comes from? maybe have a readme me in
.../assets? How do you think?"

Yes, with two changes to the idea: generated rather than hand-written, and hashed rather than
described. The unit's own hand-written README was stale in four ways at that moment, so a
hand-maintained provenance note would have rotted the same way.

Running the resulting manifest across all 10 units was the real payoff:
  2 of 12 assets traceable to any file on disk
  9 assets stale against their own source/
  display02 and display03 figure assets match NOTHING in versions/, candidates/ or source/
  6 table-body.tex files are generated, not promoted, so "matches nothing" is expected for them and
    the manifest records their kind and input instead of flagging them

The staleness flag also automates a defect S-Main-6 was carrying by hand: display02's assets are
older than the source CSV, so the manuscript compiles a figure drawn before its numbers were re-run.
