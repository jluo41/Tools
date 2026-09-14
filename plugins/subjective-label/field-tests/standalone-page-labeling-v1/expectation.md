# standalone-page-labeling-v1 · expectation ledger

Frozen before the independent field run on 2026-09-13. The field desk does
not receive this file.

## Baseline

| artifact | sha256 |
|---|---|
| haipipe-page/SKILL.md | `64cca86d33b5a2a3a51ed5019d9cd84cb44555a4e8ec0acd5f15d5bef505982d` |
| haipipe-plugin-runs/SKILL.md | `82d344d0eee4a928c1d11d3ff64a6ed31a388d350b5c3b610163f92d059d3f04` |
| haipipe-run/SKILL.md | `0a759ec8b054054b5110fe6d03e33a6c92b24835d8b72f7e86e422c43464ed55` |
| haipipe-plugin-labeling/SKILL.md | `56a9c470555608c90ca082ab6264020b0d73178b75bcdfc196078a66aa47b88b` |
| subjective-label-workflow/SKILL.md | `78c372a0ff1f557c6d9dbda95b6aa5638ebf995f5c96e5835efaf8ca6c4feb62` |
| ref-run.md | `dd699a8e4798aed1dc2af89aab03d5fa1e27f6afa9f34822136f8a68a8c0b732` |
| engine/page_plugin.py | `808a4efd2ccb510e32c943b1d8109ba60141fc66434591ea560498377ce1e308` |

## Expected behavior

| step | law exercised | expected behavior | expected evidence |
|---:|---|---|---|
| 1 | skill routing | Load Page, plugin, Runs, Run, Labeling, and workflow contracts; treat the Page Folder as the target, not a Board | cited skill/path observations |
| 2 | spaces | Distinguish five top-level standalone plugins from the five internal Labeling workspaces; Codex Chat is transport, not a sixth Labeling workspace | `Outline · Runs · Delivery · Folder · Labeling`; `Workflow · Data · Guideline · Human · Quality` |
| 3 | native Run identities | Find one root Page setup `r01` and one nested Labeling `rl01` in the same generic Task Runs lane; find no allocated `rpNN` | exact two Run ids and origins |
| 4 | receipt-first frontier | Report `rl01_corpus-contract_job-v1` complete while the job remains at P0 human meaning confirmation | status output and Labeling Workflow view |
| 5 | protected boundary | Confirm raw `labeling/corpus/items.jsonl` returns 404 and protected item text is absent from rendered surfaces | HTTP status plus bounded content check |
| 6 | human gate | Stop without confirming meaning, creating gold, or allocating Round 1 | no semantic writes; next action remains human meaning confirmation |

## Settlement

Pending independent run. Classify each row as MATCH, SKILL GAP, or EXPECTATION
GAP from transcript and disk evidence only.
