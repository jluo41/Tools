# standalone-page-labeling-v1 · round 5 expectation ledger

Frozen before the fifth independent field run on 2026-09-13. The field desk
does not receive this file. The same strict safe-file whitelist applies.

## Baseline

| artifact | sha256 |
|---|---|
| haipipe-run/SKILL.md | `e651e9d537e5fdc5a929ee5bdb64ca6fb85d5a3796e2a3353cdd69823200a7f7` |
| subjective-label-workflow/SKILL.md | `a33961be7bd056ab53b491f0127ed33aed34cc31e0e9fb0222412be8f429cb94` |
| label-building-workflow/SKILL.md | `d5262deae63fffeb046502a069e8a009049f944b5383154dd5dea5ef8f6bbff7` |
| engine/job.py | `6f980a8547997edb208bd589c2d9192336d0b266495419e15ebe671f5790c2f4` |
| rl01 Run | `42fe86c0eef35e2a4f7aa9789e08ed5d1bae9e3dbc97f3b7a1678f49e69c1e7c` |
| rl01 runtime | `9b3c4d98064fdb70e40c403deeff138200db39511334dddda28b027fbdc532cc` |
| rl01 Result | `b4afde9c2e0c89bf9d59470bf663bc1e033876643c4999236052ce331512f958` |

## Expected behavior

| step | law exercised | expected behavior | expected evidence |
|---:|---|---|---|
| 1 | base runtime | rl01 runtime includes frozen `inputs` and offset-bearing RFC 3339 start/finish values | exact safe envelope fields |
| 2 | P0 cardinality | one required corpus-contract plus only independently commissioned optional D/G/T/E Runs; current actual count remains one | formula and live inventory |
| 3 | status precision | status uses `p0_contract_integrity_valid: true`, `g0_receipt_valid: false`, and no ambiguous `g0_integrity` key | exact status JSON |
| 4 | strict safety | only three named Run-envelope files are directly read/hashed; no direct corpus/test/sealed/manifest/config/policy/receipt access; no writes | stable hashes and explicit attestation |

## Settlement

Convergence requires **4 MATCH**, zero new friction, zero writes, and zero
direct protected-file reads.
