---
status: open
created: 2026-07-28
updated: 2026-07-28
occurrences: 1
kind: defect
context: Q-page structure
lands_in: "ref/page-template.md + ref/writing-rules.md"
session: "the 2026-07-27 MISQ §3 Theory + display session (board: examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/0-lifecycle)"
fixed_in: ""
regressed: ""
---
JL, verbatim: "read it yourself, this is not good, hard to follow, not structured."

The headache tick row had grown to 33 lines carrying three `CC 260727 ·` analysis blocks, which
were near-duplicates of the argument already sitting in the owning entry in Items to Finish. The
options and the lean were buried under the commentary, so the row no longer showed what was being
decided.

The shape that survived: question (1 line) · options on ONE line (A · B · C) · `-> lean` with its
reason · `commits:` naming what ticking that option binds the prose to · `unblocks:` if it releases
other work. Rebuilt: 147 lines to 74, longest row 33 to 7.

Two rules fall out.
1. Self-contained on the DECISION, pointer for the ARGUMENT. This resolves a real conflict between
   two existing hard rules, "Each question is self-contained" and "Clear out stale text", which
   pull in opposite directions and are not reconciled anywhere.
2. "One sentence per source line" is correct about line breaks and silent about ROW LENGTH. It needs
   a companion cap (about six lines for a decision row); past that, argument has leaked in. Following
   the line rule exactly is what produced the wall.
