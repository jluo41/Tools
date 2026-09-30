# Labeling Workbench · Space, View, Run Type, Skill

A walk-through table for reviewing the Labeling Workbench one row at a time.
The page itself reads `skills/label-building/ref/ref-space-mapping.md`; when a
review changes a row, change it there too. Written 2026-09-30.

Part 1 of `labeling-workbench-design.excalidraw` is this table as a drawing. It
is generated from this file: edit this file, then run
`labeling-workbench-run-table.py` beside it.

## Words

- **Space**: a top tab of the Workbench (Data, Labeling, Quality, Delivery).
- **View**: a sub-tab inside a Space (what JL called a subspace).
- **Run Type**: one kind of operation, such as `human-calibration`.
- **Run**: one execution of a Run Type, with a Ticket in `runs/` and a Result in `results/`.
- **Run name**: `run-<family>-<run type>-<MMDD>-<target>`; family is `corpus` or `labeling`.
- **View Skill**: the one Skill that says how to do the Runs of that View.
- **Does**: what the Run does, in one line.
- **Engine worker**: the Python function that actually writes the Run.
- **G0**: the Confirm meaning gate; a human button, not a Run.

## Spaces

- **Data**: How does raw data become items, and what does the corpus hold?
- **Labeling**: What do the labels mean, and how is each round labeled?
- **Quality**: Is the test sealed, and which executor and final corpus pass?
- **Delivery**: What is handed over, scanned, and delivered?

## Table

Built: ✅ an engine worker exists; ⬜ no worker yet. Review: tick when JL has
gone through the row.

| # | Space › View | Run name | Does | View Skill | Engine worker | Built | S-Label-4 has | Review |
|---|---|---|---|---|---|---|---|---|
| 0a | Data › Preparation | `run-corpus-source-normalize` | Parse the raw transcript records | `subjective-label-preparation` | `corpus_preparation.normalize` | ✅ | none | ⬜ |
| 0b | Data › Preparation | `run-corpus-unit-recipe` | Choose target, context, and grouping | `subjective-label-preparation` | `corpus_preparation.recipe` | ✅ | none | ⬜ |
| 0c | Data › Preparation | `run-corpus-unit-materialize` | Build candidate items with lineage | `subjective-label-preparation` | `corpus_preparation.materialize` | ✅ | none | ⬜ |
| 0d | Data › Preparation | `run-corpus-unit-check` | Validate units and source groups | `subjective-label-preparation` | `corpus_preparation.check` | ✅ | none | ⬜ |
| 0e | Data › Preparation | `run-corpus-initial-group-reserve` | Hold out complete groups; bind the package | `subjective-label-preparation` | `corpus_preparation.reserve` | ✅ | none | ⬜ |
| 1 | Data › Contract | `run-labeling-corpus-contract` | Create the Page job from the accepted package | `subjective-label-contract` | `job.create_contract` | ✅ | `rl01` | ⬜ |
| 3 | Data › Embedding | `run-labeling-embedding-build` | Build a map of the accepted items | `subjective-label-embedding` | `embedding_build.build` | ✅ | `rl02` `rl05` `rl06` `rl07` | ⬜ |
| 4 | Labeling › Definition | `run-labeling-discovery-search` | Search outside sources on what the label means | `subjective-label-definition` | none | ⬜ | none | ⬜ |
| 5 | Labeling › Definition | `run-labeling-definition-discussion` | Discuss each label's meaning with you | `subjective-label-definition` | `definition_discussion.start` · `say` · `decide` · `close` | ✅ | `rl08` (blocked) | ⬜ |
| G0 | Labeling › Definition | Confirm meaning (gate) | your button here; a gate, not a run | `subjective-label-definition` | `job.confirm_meaning` | ✅ | invalid | ⬜ |
| 7 | Labeling › Rounds | `run-labeling-round-prepare` | Draw one round of items | `subjective-label-rounds` | `calibration.release_round` | ✅ | `rl03` | ⬜ |
| 8 | Labeling › Rounds | `run-labeling-weak-prelabel` | Small models pre-label the round | `subjective-label-rounds` | none | ⬜ | none | ⬜ |
| 9 | Labeling › Rounds | `run-labeling-human-calibration` | You label the round, in chat | `subjective-label-rounds` | `calibration.open_item` · `record_first` · `record_final` | ✅ | `rl04` (0 labels) | ⬜ |
| 11 | Labeling › Rounds | `run-labeling-round-measure` | Measure agreement and coverage | `subjective-label-rounds` | none | ⬜ | none | ⬜ |
| 12 | Labeling › Rounds | `run-labeling-round-close` | Close the round; promote gold and guideline | `subjective-label-rounds` | none | ⬜ | none | ⬜ |
| 6 | Labeling › Guideline | `run-labeling-guideline-seed` | Draft a first guideline | `subjective-label-guideline` | none | ⬜ | none | ⬜ |
| 10 | Labeling › Guideline | `run-labeling-guideline-learn` | Draft the next guideline from your answers | `subjective-label-guideline` | none | ⬜ | none | ⬜ |
| 2 | Quality › Test | `run-labeling-test-reserve` | Re-draw the held-back test, only if needed | `subjective-label-test` | none | ⬜ | none | ⬜ |
| 14 | Quality › Test | `run-labeling-test-gold-lock` | You label the held-back test, blind | `subjective-label-test` | none | ⬜ | none | ⬜ |
| 15 | Quality › Evaluation | `run-labeling-executor-predict` | One model predicts the test (x K) | `subjective-label-evaluation` | none | ⬜ | none | ⬜ |
| 16 | Quality › Evaluation | `run-labeling-executor-score` | Score one model's predictions (x K) | `subjective-label-evaluation` | none | ⬜ | none | ⬜ |
| 17 | Quality › Evaluation | `run-labeling-executor-select` | Pick the model from the scorecards | `subjective-label-evaluation` | none | ⬜ | none | ⬜ |
| 23 | Quality › Audit | `run-labeling-audit-sample` | Draw an audit sample of the final labels | `subjective-label-audit` | none | ⬜ | none | ⬜ |
| 24 | Quality › Audit | `run-labeling-audit-human-gold` | You label the audit sample, blind | `subjective-label-audit` | none | ⬜ | none | ⬜ |
| 25 | Quality › Audit | `run-labeling-audit-analyze` | Analyze the audit | `subjective-label-audit` | none | ⬜ | none | ⬜ |
| 13 | Delivery › Handoff | `run-labeling-handoff-freeze` | Freeze the guideline and gold for scanning | `subjective-label-handoff` | none | ⬜ | none | ⬜ |
| 18 | Delivery › Scan | `run-labeling-scan-preflight` | Check the production plan | `subjective-label-scan` | none | ⬜ | none | ⬜ |
| 19 | Delivery › Scan | `run-labeling-scan-shard` | The model labels one corpus shard (x S) | `subjective-label-scan` | none | ⬜ | none | ⬜ |
| 20 | Delivery › Scan | `run-labeling-risk-route` | Send risky items to review | `subjective-label-scan` | none | ⬜ | none | ⬜ |
| 21 | Delivery › Scan | `run-labeling-human-review` | You review the risky items | `subjective-label-scan` | none | ⬜ | none | ⬜ |
| 22 | Delivery › Scan | `run-labeling-reconcile` | Merge the reviewed items into the corpus | `subjective-label-scan` | none | ⬜ | none | ⬜ |
| 26 | Delivery › Final labels | `run-labeling-dstar-materialize` | Publish the audited final labels | `subjective-label-final-labels` | none | ⬜ | none | ⬜ |

`#` is the order the Runs happen in. Steps 7 to 12 repeat every round. Building
is steps 1 to 13; Scanning is steps 14 to 26. `rlNN` is the old Ticket name
S-Label-4 still has on disk; new Tickets get the full `run-...` name.

Preparation rows (0a to 0e) declare only their View Skill. Every Building row
(1 to 13) also declares three shared Skills:
`subjective-label-workflow`, `label-building`, `label-building-workflow`.
Every Scanning row (14 to 26) declares `subjective-label-workflow`,
`label-scanning`, `label-scanning-workflow`. The Run card on the page currently
prints all four.

## The Skills we have

| Skill | Version | Role |
|---|---|---|
| `subjective-label` | 0.9.1 | door: starts or resumes a job and routes the request |
| `subjective-label-workflow` | 0.12.1 | order across both sides: which Run may start, which gate follows |
| `label-building` | 0.7.0 | rules for Building: who decides what, what is forbidden |
| `label-building-workflow` | 0.11.0 | step order for Building (steps 1 to 13) |
| `label-scanning` | 0.7.0 | rules for Scanning |
| `label-scanning-workflow` | 0.8.0 | step order for Scanning (steps 14 to 26) |
| `haipipe-workbench-labeling` | 0.23.16 | the Workbench page itself; not a Run Skill |
| `subjective-label-preparation` | 0.1.1 | View Skill · Data › Preparation |
| `subjective-label-contract` | 0.1.1 | View Skill · Data › Contract |
| `subjective-label-embedding` | 0.1.0 | View Skill · Data › Embedding |
| `subjective-label-definition` | 0.1.4 | View Skill · Labeling › Definition |
| `subjective-label-rounds` | 0.1.3 | View Skill · Labeling › Rounds |
| `subjective-label-guideline` | 0.1.0 | View Skill · Labeling › Guideline |
| `subjective-label-test` | 0.1.1 | View Skill · Quality › Test |
| `subjective-label-evaluation` | 0.1.0 | View Skill · Quality › Evaluation |
| `subjective-label-audit` | 0.1.0 | View Skill · Quality › Audit |
| `subjective-label-handoff` | 0.1.0 | View Skill · Delivery › Handoff |
| `subjective-label-scan` | 0.1.0 | View Skill · Delivery › Scan |
| `subjective-label-final-labels` | 0.1.0 | View Skill · Delivery › Final labels |

19 Skills: 6 shared, 1 page, 12 View Skills (one per View, never shared).

## Counts

- 4 Spaces, 12 Views, 31 Run Types (5 corpus + 26 labeling), 1 gate.
- Built: 10 Run Types (5 corpus + 5 labeling) plus G0.
- Not built: 21 labeling Run Types.
