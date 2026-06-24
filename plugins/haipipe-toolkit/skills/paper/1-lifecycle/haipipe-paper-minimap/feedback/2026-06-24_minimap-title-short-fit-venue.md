---
status: open
created: 2026-06-24
updated: 2026-06-24
occurrences: 1
context: minimap stage, ProjB Paper-Personality2Opioid-MISQ2026 (MISQ)
fixed_in: ""
regressed: ""
---
"for the title, could you just make it short? like 'LLM-Perceived Physician Traits and Prescriptions'." + "this one should fit the venue."

The minimap `\title` should be SHORT: the paper's own working title, with no long
descriptive subtitle. The MISQ minimap was generated with a second subtitle line
("A Behavioral-Signal Account, Tested on Medicare Opioid Prescribing"), which JL
cut. The title should also FIT THE VENUE pinned in STATUS: a MISQ minimap title
reads like an IS-journal title, a JAMA minimap title reads clinical.

How to apply (haipipe-paper-minimap): set `\title` to the paper's title only
(short), shaped to the STATUS `venue`; do NOT append a descriptive subtitle to the
minimap title.

Fix:
