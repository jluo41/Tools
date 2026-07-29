---
status: open
created: 2026-07-28
updated: 2026-07-28
occurrences: 2
kind: defect
context: captions and records
lands_in: "the display skills + haipipe-paper-draft-values"
session: "the 2026-07-27 MISQ §3 Theory + display session (board: examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/0-lifecycle)"
fixed_in: ""
regressed: ""
---
JL fixed a caption that read "metformin claims" under the heading "prescribing intensity". The
claims ledger records the diabetes outcome as WHETHER each drug class is prescribed, a binary, not
an intensity.

The same defect had been found independently from the evidence side hours earlier: four cohort
coefficients are on `mme_ttl` while metformin's -0.0007151 is on `is_metformin_rx`, an OLS linear
probability model. So metformin is the falsification test and never a rung on the MME gradient.

Two findings, one error, discovered from opposite directions on the same day. Both records now
cross-reference rather than sitting as two silent repairs.

The rule: an outcome named in a caption or a record must match the ledger's VARIABLE TYPE, not just
its name. Binary and intensity are different claims, and a gradient table that mixes them is
comparing incomparable numbers.
