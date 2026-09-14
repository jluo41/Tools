# standalone-page-labeling-v1 · round 4 settlement

Joined on 2026-09-13 from the strict-whitelist ledger, Lovelace's cold
transcript, exact safe-envelope hashes, and GET-only HTTP evidence.

## Ledger

| step | settlement | observed evidence |
|---:|---|---|
| 1 | SKILL GAP | Status invocation and optional-sidecar behavior passed, but the P0 workflow formula still counted optional sidecars as mandatory and the emitted runtime lacked required `inputs` plus unambiguous date-time precision. |
| 2 | MATCH | Current Run was `none`; Quality showed active custodian `JL` and source custody as provenance only. |
| 3 | SKILL GAP | Gate/action/transport agreed, but status field `g0_integrity: true` was easily mistaken for a passed G0 while its receipt was false. |
| 4 | MATCH | The desk directly hashed only the three whitelisted safe envelopes; hashes were stable, six raw routes returned 404, and there were zero writes/direct protected reads. |

Tally: **2 MATCH · 2 SKILL GAP · 0 EXPECTATION GAP**. The two skill-gap rows
contain four friction entries.

## Friction disposition

| # | class | disposition | patch / tooth |
|---:|---|---|---|
| 1 | wrong | fixed | P0 runtime now copies the frozen `inputs` envelope; engine test asserts the exact path/hash. |
| 2 | unclear | fixed | New Run receipts require offset-bearing RFC 3339 date-times; date-only is legacy. Writer and real rl01 runtime now use a full timestamp. |
| 3 | self-contradictory | fixed | P0 cardinality is now `1 + D + G + T + E`, with optional variables defined; happy-path formula updated. |
| 4 | unclear | fixed | Canonical status field renamed from `g0_integrity` to `p0_contract_integrity_valid`; Board adapter and tests consume the precise name. |

## Scorecard

| measure | result |
|---|---|
| time | Field desk 01:02:31→01:05:03 EDT = **2m32s**. Design-desk overhead was not independently metered. |
| tokens | Field-task token receipt unavailable; no estimate substituted. |
| format | 4 runtime/privacy steps passed; 3 exact envelope hashes stable; zero direct protected reads. Repair checks: 3 skills structurally valid, 14 engine, 19 Board-Labeling, and 24 standalone tests passed. |
| semantic | 2 MATCH · 2 SKILL GAP · 0 EXPECTATION GAP; 4 precise contract frictions; runtime/privacy behavior passed. |
| tax | A fifth short cold run is forced by envelope/schema debt that could have been caught by validating generated rl01 against the generic runtime minimum immediately. Lesson: every new dialect needs a fixture assertion for every base receipt field and exact timestamp grammar. |
| rate | 4 expectation rows / 2m32s = **1.58 settled rows/min**, repair-grade; token rate unavailable. |

Verdict: **runtime behavior passes, contract is not dry**. Round 5 is limited
to the corrected safe envelope, P0 count formula, precise status field, and the
same strict no-protected-read fence.
