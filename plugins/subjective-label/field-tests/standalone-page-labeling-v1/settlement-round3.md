# standalone-page-labeling-v1 · round 3 settlement

Joined on 2026-09-13 from the round-3 frozen ledger, Hypatia's cold transcript,
live HTTP evidence, and the reported before/after Run inventory digest.

## Ledger

| step | settlement | observed evidence |
|---:|---|---|
| 1 | MATCH | Completed `rl01` remained in history and the live current-Run metric was exactly `none`. |
| 2 | SKILL GAP | P0/G0/action output was correct, but the Building skill omitted the exact read-only status invocation and made optional embedding appear ordered before G0. |
| 3 | SKILL GAP | Active custodian `JL` was valid and source custody was correctly treated as provenance, but the Quality surface did not expose that distinction. |
| 4 | MATCH | The exact Codex-task prompt carried the gate and action; no Run or event was created. |
| 5 | EXPECTATION GAP | All protected routes and rendered surfaces passed, but the commission's read fence did not explicitly forbid a whole-folder hash. The field desk performed one aggregate hash that read protected bytes without displaying them. |

Tally: **2 MATCH · 2 SKILL GAP · 1 EXPECTATION GAP**. Behavioral checks were
5/5 pass; protocol was not clean because of the read-scope breach.

## Friction disposition

| # | class | disposition | patch / tooth |
|---:|---|---|---|
| 1 | missing | fixed | Building workflow now gives the exact `job.py status --job-root …` command. |
| 2 | unclear | fixed | P0 sidecars are explicitly optional and skippable before G0; `create` truthfully owns exactly one completed corpus-contract Run. |
| 3 | missing | fixed | Canonical status returns safe custody metadata and Quality renders `active custodian` plus `source custody: provenance only`; engine and integration assertions pin both. |
| protocol | commission gap | fixed for next run | The next commission limits hashing to an explicit Run/Result whitelist and forbids directory recursion, corpus, test, sealed, and manifest reads. |

## Scorecard

| measure | result |
|---|---|
| time | Field desk 00:44:17→00:56:15 EDT = **11m58s**. Design-desk overhead was not independently metered. |
| tokens | Field-task token receipt unavailable; no estimate substituted. |
| format | 5 behavioral checks passed; 3 protected routes returned 404; Run inventory digest remained identical. Repair checks: 2 skills structurally valid, 14 engine and 24 standalone tests passed. |
| semantic | 2 MATCH · 2 SKILL GAP · 1 EXPECTATION GAP; 3 rule/UI frictions; behavioral PASS but protocol breach. |
| tax | The 11m58s run exposed three useful gaps, but one whole-folder checksum was avoidable protected-read tax caused by an insufficiently explicit commission fence. Lesson: enumerate the exact safe files a field desk may hash; never ask for an unspecialized folder digest near sealed data. |
| rate | 5 expectation rows / 11m58s = **0.42 settled rows/min**, repair-grade; token rate unavailable. |

Verdict: **behavior passes, protocol does not converge**. A fourth cold run is
required with a strict safe-file read whitelist and the repaired operator-facing
status/custody surfaces.
