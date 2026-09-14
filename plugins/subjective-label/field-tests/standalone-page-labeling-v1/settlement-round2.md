# standalone-page-labeling-v1 · round 2 settlement

Joined on 2026-09-13 from the round-2 frozen ledger, Pascal's cold transcript,
live HTTP evidence, and before/after Run hashes.

## Ledger

| step | settlement | observed evidence |
|---:|---|---|
| 1 | MATCH | The live row now reads `corpus-contract · Local`; Labeling remains the native family. |
| 2 | MATCH | Five internal workspaces and standalone Codex-task transport were unambiguous; no fake chat backend appeared. |
| 3 | MATCH | The repaired P0/G0/G2/G3 receipt-chain summary matched disk and no promotion was skipped. |
| 4 | SKILL GAP | Inventory and pairing were correct, but the standalone presenter called completed `rl01` the current Run instead of returning `none`. |
| 5 | SKILL GAP | Phase and next action were correct, but the first blocked gate was worded `P0 human meaning confirmation` instead of unambiguously naming G0. |
| 6 | SKILL GAP | The protected boundary passed, but the contract did not distinguish the current destination custodian from imported source-custodian provenance. |
| 7 | MATCH | Seven Run/Result files retained identical hashes; no receipt, Run, round, or semantic source changed. |

Tally: **4 MATCH · 3 SKILL GAP · 0 EXPECTATION GAP**.

## Friction disposition

| # | class | disposition | patch / tooth |
|---:|---|---|---|
| 1 | wrong | fixed | The presenter now selects only nonterminal Runs as current. The standalone integration test requires the completed-only fixture to render `Run = none`. |
| 2 | unclear | fixed | Status and Building workflow now separate phase `P0 Contract` from blocked gate `G0 · human meaning confirmation`; an engine assertion pins the exact gate label. |
| 3 | unclear | fixed | Labeling law now defines current custody from destination `test/sealed/status.json:custodian`; imported `source_custodian` is provenance only. |

## Scorecard

| measure | result |
|---|---|
| time | Field desk 00:31:16→00:39:19 ET = **8m03s**. Design-desk overhead was not independently metered. |
| tokens | Field-task token receipt unavailable; no estimate substituted. |
| format | 7 live/raw route probes; 60 protected values checked; 7 Run/Result hashes stable. Repair checks: 2 skills structurally valid, 24 standalone tests and 14 engine tests passed after correcting one over-specific test expectation. |
| semantic | 4 MATCH · 3 SKILL GAP · 0 EXPECTATION GAP; 3 precise frictions; independent verdict: mostly conformant, not dry. |
| tax | A third cold run was forced by conflating latest with current and phase with gate, plus one unstated provenance rule. Lesson: presenters must derive active state from terminality, and every displayed frontier field must declare whether it names a phase, gate, or action. |
| rate | 7 expectation rows / 8m03s = **0.87 settled rows/min**, repair-grade; token rate unavailable. |

Verdict: **repair required; round 2 is not converged**. Round 3 narrows to
current-vs-latest, exact G0 naming, custody provenance, and the unchanged safety
boundary.
