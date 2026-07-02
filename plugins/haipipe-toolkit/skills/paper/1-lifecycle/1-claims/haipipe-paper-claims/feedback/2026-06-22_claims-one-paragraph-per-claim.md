---
status: fixed (structure-claims v1.1.0: matrix + per-claim \subsection* detail)
created: 2026-06-22
context: haipipe-paper-claims ledger layout; how 2-claims.tex should present each claim. Extends 2026-06-22_claims-ledger-thin-no-status-no-evidence and 2026-06-22_claims-need-probe-orchestrated-evidence.
fixed_in: ""
---
I think here each claim should be one single paragraph after the claim-evidence matrix, how do you think about it. So we can know more details about it.

Distilled ask:
- The claim stage should present TWO layers: (1) the claim-evidence MATRIX (at-a-glance: ID / claim / status), then (2) ONE dedicated PARAGRAPH per claim below the matrix carrying the details.
- The per-claim paragraph is where the solid evidence lives: the real result (coefficient, significance, N, spec), the interpretation, the caveat, and the source. The matrix stays scannable; the paragraph gives depth.

Suggested fix direction (skill):
- haipipe-paper-claims template = matrix table + a "Per-claim detail" section with one banner+paragraph per claim ([claims.c1], [claims.c2], ...), each in the %% ---- Pn.Sm ---- sentence format.
- Per-claim paragraph slots: (S1) claim + verdict, (S2) the verified statistic/source, (S3) interpretation, (S4) caveat. This is the natural home for the aris (value, source) evidence + the honest qualifier.
- Replaces cramming evidence into table cells (unreadable) with a matrix-then-detail layout.

Fix:
