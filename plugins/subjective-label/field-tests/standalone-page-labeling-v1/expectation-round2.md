# standalone-page-labeling-v1 · round 2 expectation ledger

Frozen before the second independent field run on 2026-09-13. The field desk
does not receive this file. This run targets the four gaps found in round 1
while rechecking the safety and human-gate invariants.

## Baseline

| artifact | sha256 |
|---|---|
| haipipe-page/SKILL.md | `64cca86d33b5a2a3a51ed5019d9cd84cb44555a4e8ec0acd5f15d5bef505982d` |
| haipipe-plugin-runs/SKILL.md | `3c708fba74eeac97c5714acca383eb1c7161213f969076ef28f12d1009307d2b` |
| haipipe-run/SKILL.md | `0a759ec8b054054b5110fe6d03e33a6c92b24835d8b72f7e86e422c43464ed55` |
| haipipe-plugin-labeling/SKILL.md | `b3de2287e4cc417bd67f954ac6adbb8d67e14893c0b2f9533309a88fd6e03eed` |
| subjective-label-workflow/SKILL.md | `561a47bec51f126af45c5a9c6eaa0900aaf0e8d6d2244542e67972076e47ae92` |
| ref-run.md | `dd699a8e4798aed1dc2af89aab03d5fa1e27f6afa9f34822136f8a68a8c0b732` |
| engine/page_plugin.py | `808a4efd2ccb510e32c943b1d8109ba60141fc66434591ea560498377ce1e308` |
| live/runs.py | `c513f5f716570e9ed9227ff6439339215595e2b86c6673e61d46e97b70081553` |

## Expected behavior

| step | law exercised | expected behavior | expected evidence |
|---:|---|---|---|
| 1 | Kind / Where | `rl01` keeps Labeling family, uses `corpus-contract` as Kind, and shows physical Where `Local` | exact live row text `corpus-contract · Local` |
| 2 | host transport | five Labeling workspaces remain stable; Board owns Studio Chat while this standalone host names the current Codex task | no sixth Chat workspace and no fake HTTP chat backend |
| 3 | receipt chain | distinguish P0 setup receipt, G0 meaning receipt, final checkpoint at G2, and handoff plus registry at G3 | exact skill-contract observations |
| 4 | Run inventory | root `r01` and nested `rl01` share the generic Task Runs lane; no `rpNN` or speculative Round Run exists | exact inventory and paired envelopes |
| 5 | frontier | P0 integrity passes, `rl01` is complete, and human meaning confirmation remains the sole next action | canonical status plus live Labeling surface |
| 6 | protected boundary | direct raw corpus route is 404 and protected ids/text do not occur on root, Runs, or Labeling surfaces | bounded HTTP/content check |
| 7 | stopping law | make no writes and do not cross G0 | before/after inventory and explicit no-write report |

## Settlement

Pending second independent run. Classify each row as MATCH, SKILL GAP, or
EXPECTATION GAP from transcript and disk evidence only.
