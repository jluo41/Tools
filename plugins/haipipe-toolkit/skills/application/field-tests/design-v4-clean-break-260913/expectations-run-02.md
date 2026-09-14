# Design v4 clean-break field test · run 02 expectation ledger

Baseline frozen: Design v4.0.1, 2026-09-13.
Different real slice: the DrFirst Board-level entry and Design directory shape,
not the DS01 candidate/status content inspected in run 01.
The field desk must not see this file.

| Step | Law exercised | Expected behavior | Expected artifacts |
|---|---|---|---|
| R2E1 | shipped-skill discovery | Load Design v4.0.1 and its current workflow/unit contracts | timestamped report only |
| R2E2 | decisive-marker stop | Use Board/DS directory structure to detect PageX or `design/DU*/`, then stop before candidate content | explicit unsupported hold |
| R2E3 | no compatibility language | Call old Design bytes unsupported; never readable/read-only/migration history or input | no compatibility wording |
| R2E4 | independent Run namespaces | Report Page `rpNN` and Design `rdNN_generate_*` / `rdNN_verify_*` separately | both counters named |
| R2E5 | authority/non-mutation | Infer no release/adoption and make no writes or migration | no target writes or receipts |
| R2E6 | friction semantics and stop | Friction rows cover skill-instruction defects only; stop after one bounded next action | numbered log, no target-debt rows |

Settlement status: all six rows MATCH; see `settlement-run-02.md`.
