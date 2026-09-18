# Labeling Space · UI ↔ Page Folder ↔ Run mapping

This is the orientation contract for the Board Labeling surface of
`haipipe-plugin-labeling` (`live/labeling.py`). It uses one location word:
**Space = Workspace** (one concept). Workflow phases P0-P5 are phase state, not
a Space. They show in `Run → Phases` and in the one-line `Next:` header.

## Two levels

The Board level (`GET /_board/labeling-board?path=<board.md>`) lists one card
per Page that owns a `labeling/` job; a card opens that Page's surface below.
The Page header's `← All labeling jobs` link returns to the Board level. The
Board level has no Spaces and no writes. The rest of this file is the Page
level.

## Space roster

| order | Space | views | first question | canonical sources |
|---|---|---|---|---|
| 1 | **Data** | Contract · Schema · Embedding | What is one item, what do the labels mean, is that meaning confirmed, and how does an item become a vector? | `config.yaml` · `corpus/manifest.json` · `corpus/imported_label_summary.json` · `test/sealed/status.json` · `gates/g0/receipt.json` · `cache/embeddings/<version>/manifest.json` |
| 2 | **Labeling** | Label · Rounds · Guideline | Which item do I judge next, and what does the guideline say now? | `rounds/round_NN/human_batch.jsonl` · `rounds/round_NN/sessions/events.jsonl` · `corpus/items.jsonl` (Label only) · `policy/current` · `policy/versions/<G>/guideline.md` |
| 3 | **Quality** | Test · Evaluation · Audit | Is the sealed test safe, and what evidence qualifies an executor and the final corpus? | `test/sealed/status.json` · `test/final/lock.json` · `evaluation/registry.yaml` · `audit/final_*/` |
| 4 | **Run** | Runs · Phases · Workflow map | Which `rlNN` Runs exist, which gate blocks the job, and which Space does what for each Run type? | `runs/*.yaml` · `results/*/runtime.yaml` · `results/*/result.yaml` · `engine/job.py status()` · this file's `## Workflow map` |
| 5 | **Delivery** | Handoff · Final labels | What can a reader receive? | `handoff/label-v1.yaml` · `corpus/final/D_star.jsonl` |

All paths are relative to the Page's `labeling/` folder, except the engine
call. Guideline is a view inside Labeling. The older Human tab and the Workflow
map are gone.

## Workflow map

One row per Run type (the 25 operations of `ref-run.md` §3), one column per
Space. A cell says what the Space does with that Run type: `start` means a
button there starts it, `shows` means its Result is read there, `—` means
nothing. Every Run is also listed in `Run → Runs`, so the Run Space has no
column. `started by` names the button or the channel; `not built yet` means no
engine writer exists today. The Board's `Run → Workflow map` view projects this
table and adds how many Runs of each type the job has. A definition, not an
inventory.

| phase | Run type | in words | started by | Data | Labeling | Quality | Delivery | writes to |
|---|---|---|---|---|---|---|---|---|
| P0 | `corpus-contract` | Set up the job | Chat: /subjective-label | shows · Contract, Schema | — | shows · Test (held-back count) | — | `gates/p0-contract/receipt.json` |
| P0 | `discovery-search` | Search outside evidence | not built yet | — | — | — | — | `discovery/search_<n>/result.json` |
| P0 | `guideline-seed` | Draft the guideline | part of setup (no Run of its own yet) | — | shows · Guideline | — | — | `policy/versions/G_00/` |
| P0 | `test-reserve` | Hold back test items | part of setup, before the job (no Run of its own yet) | shows · Contract | — | shows · Test | — | `test/sealed/status.json` |
| P0 | `embedding-build` | Build a map | Run embedding button | start + shows · Embedding | shows · map groups in Rounds | — | — | `cache/embeddings/<version>/` |
| P1 | `round-prepare` | Draw a round | Start round button | — | start + shows · Label, Rounds | — | — | `rounds/round_NN/` |
| P1 | `weak-prelabel` | Weak models pre-label | not built yet | — | shows · comparison after you lock | — | — | `rounds/round_NN/prelabels/` |
| P1 | `human-calibration` | You label a round | your answers on the Label screen | — | start + shows · Label, Rounds | — | — | `rounds/round_NN/sessions/events.jsonl` |
| P1 | `guideline-learn` | Learn the guideline | not built yet | — | shows · Guideline | — | — | `rounds/round_NN/policy_draft/` |
| P1 | `round-measure` | Measure a round | not built yet | — | shows · Rounds | — | — | `rounds/round_NN/metrics.json` |
| P1 | `round-close` | Close a round | not built yet | — | shows · Rounds, Guideline | — | — | `rounds/round_NN/checkpoint.json` |
| P2 | `handoff-freeze` | Freeze the labels | not built yet | — | — | — | shows · Handoff | `handoff/label-v1.yaml` |
| P3 | `test-gold-lock` | Lock the test answers | not built yet | — | — | shows · Test | — | `test/final/lock.json` |
| P3 | `executor-predict` | A labeling model predicts the test | not built yet | — | — | shows · Evaluation | — | `evaluation/predictions/` |
| P3 | `executor-score` | Score a labeling model | not built yet | — | — | shows · Evaluation | — | `evaluation/scorecards/` |
| P3 | `executor-select` | Pick the labeling model | not built yet | — | — | shows · Evaluation | — | `evaluation/summary.md` |
| P4 | `scan-preflight` | Check before labeling the corpus | not built yet | — | — | — | — | `production/run_<n>/preflight.json` |
| P4 | `scan-shard` | Label one part of the corpus | not built yet | — | — | — | — | `production/run_<n>/` |
| P4 | `risk-route` | Send risky items to you | not built yet | — | — | — | — | `production/run_<n>/risk_queue.jsonl` |
| P4 | `human-review` | You review risky items | not built yet | — | shows · Label | — | — | `production/run_<n>/human_final.jsonl` |
| P4 | `reconcile` | Combine into final labels | not built yet | — | — | — | shows · Final labels | `production/run_<n>/run_report.md` |
| P5 | `audit-sample` | Draw an audit sample | not built yet | — | — | shows · Audit | — | `audit/final_<n>/sample.jsonl` |
| P5 | `audit-human-gold` | You label the audit sample | not built yet | — | shows · Label | shows · Audit | — | `audit/final_<n>/human_gold.jsonl` |
| P5 | `audit-analyze` | Analyze the audit | not built yet | — | — | shows · Audit | — | `audit/final_<n>/receipt.json` |
| P5 | `dstar-materialize` | Publish the final labeled corpus | not built yet | — | — | — | shows · Final labels | `corpus/final/D_star.jsonl` |

## Opening Space

The page opens on the Space that holds the next step. Engine status decides
it, checked in this order (the first match wins):

1. no `labeling/` job yet → `Data`
2. HOLD → `Data`
3. an integrity error → `Run`
4. phase P0 → `Data`
5. phase P1 → `Labeling`
6. any later phase → `Run`

A `?space=&view=` URL wins. Next comes the browser's saved choice, keyed by
Board source plus Page file. Only then does the next-step Space apply. An
unknown Space falls back to the next-step Space; an unknown view falls back to
that Space's first view.

## Item text

Overview views never render item text, sealed ids, or private judgments in the
page HTML. They show meanings, counts, checksums, and states. An item waiting in
a round's frozen batch (`human_batch.jsonl`) shows its text only on
`Labeling → Label`, one item at a time, fetched with a POST to the write door
(action `open_item`). `Data → Embedding` may fetch the text of other
development items, only when the person asks: a group's typical items (action
`group_examples`) or one picked dot (action `embedding_item_text`). Items
waiting in a round are never returned there, so the first look at them, and
their `show` event, stays on the Label screen. Every such fetch appends one line
to `labeling/exposure/group_examples.jsonl` (time, human, build, group, item
ids), so a later round can tell a fresh item from one already seen. The reveal
after a locked first answer shows reference observations, not gold. A sealed
item is never drawn, shown, or revealed.

## Write door

`POST /_board/labeling/act` is the only write. `Data → Contract` holds the
`Confirm meaning` button (`confirm_meaning`). `Labeling → Label` holds four
actions: `release_round`, `open_item`, `first`, `final`. `Data → Embedding`
holds five: `build_embedding`, `embedding_status`, `embedding_item`,
`group_examples`, `embedding_item_text`. Quality, Run, and Delivery have no
write control. The checks behind each action are the
write-and-authority law in
`../skills/page-plugins/haipipe-plugin-labeling/SKILL.md`.

## Projection law

The five Spaces are views over one page-local `labeling/` folder, not storage
folders. A Run is `rlNN_<operation>_<target>`, with its Ticket at
`labeling/runs/<run>.yaml` and its Result at `labeling/results/<run>/`. The 25
operation kinds and the count law are in `ref-run.md`. A round is an episode
that groups Runs. Each item judgment is an event inside the
`rlNN_human-calibration_round-NN` Run, never a Run of its own.
