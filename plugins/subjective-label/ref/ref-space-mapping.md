# Labeling Space · UI ↔ Page Folder ↔ Run mapping

This is the orientation contract for the Board Labeling surface of
`haipipe-plugin-labeling` (`live/labeling.py`). It uses one location word:
**Space = Workspace** (one concept). The current adapter retains P0-P5 in the
`Run → Phases` view and `Next:` header as compatibility capability tags. They
are not Workflow nodes, Run owners, or routing authority. The adapter may use
them to choose a presentation Space only; Run eligibility and Routes come from
the shared Run Spec graph and native Run receipts.

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
| 2 | **Labeling** | Label · Rounds · Guideline | What does each label mean, which items does each round label in chat, and what does the guideline say now? | `config.yaml` (Label) · `rounds/round_NN/human_batch.jsonl` · `rounds/round_NN/sessions/events.jsonl` · `corpus/items.jsonl` (Rounds only) · `policy/current` · `policy/versions/<G>/guideline.md` |
| 3 | **Quality** | Test · Evaluation · Audit | Is the sealed test safe, and what evidence qualifies an executor and the final corpus? | `test/sealed/status.json` · `test/final/lock.json` · `evaluation/registry.yaml` · `audit/final_*/` |
| 4 | **Run** | Runs · Phases · Workflow map | Which `rlNN` Runs exist, which gate blocks the job, and which Space does what for each Run type? | `runs/*.yaml` · `results/*/runtime.yaml` · `results/*/result.yaml` · `engine/job.py status()` · this file's `## Workflow map` |
| 5 | **Delivery** | Handoff · Final labels | What can a reader receive? | `handoff/label-v1.yaml` · `corpus/final/D_star.jsonl` |

All paths are relative to the Page's `labeling/` folder, except the engine
call. Guideline is a view inside Labeling. The older Human tab is gone; the
Workflow map, with the SOP above it, is a view inside the Run Space.

## SOP

The standard operating procedure: what one labeling job does, in order, and who
does each step. The Workflow map below is the reference (every Run type); this
is the path a person walks. `Run type` names the Run a step writes (`—` for a
step that writes no Run, `gate G0` for the meaning receipt). The Board's
`Run → Workflow map` view shows this table first and adds where this job is.

| step | what happens | you do | the chat or engine does | where | Run type |
|---|---|---|---|---|---|
| 1 | Set up the job | ask in chat: /subjective-label | writes config.yaml, the items, the held-back test, and guideline G_00 | Data → Contract | `corpus-contract` |
| 2 | Confirm what the labels mean | read the meanings, tick, press Confirm meaning | saves the meaning receipt; labeling can start | Data → Contract | gate G0 |
| 3 | Build a map (optional) | pick a model, press Run embedding | turns each item into a vector, groups them, draws the map | Data → Embedding | `embedding-build` |
| 4 | Define the labels better (any time) | press ⧉ chat and answer the chat's questions | proposes clearer wording; writes nothing until you approve | Labeling → Label | — |
| 5 | Start a round | pick how many items, press Start round 1 | draws items at random, never a held-back one | Labeling → Rounds | `round-prepare` |
| 6 | Label the round in chat | press Copy chat prompt; give each item a first answer, then keep or change it | saves first, lock, reveal, final; shows the raters' votes and its own view only after your first answer | Labeling → Rounds | `human-calibration` |
| 7 | Learn the guideline | rule on each proposed change | drafts guideline changes from your answers | Labeling → Guideline | `guideline-learn` |
| 8 | Measure the round | nothing | counts agreement, coverage, and risk | Labeling → Rounds | `round-measure` |
| 9 | Close the round | nothing | the Checkpoint Keeper checks the round, saves gold labels and the new guideline, and picks another round or freeze | Labeling → Rounds | `round-close` |
| 10 | Repeat steps 5 to 9 | decide when the guideline has stopped changing | starts the next round from what the last one missed | Labeling → Rounds | — |
| 11 | Freeze the labels | sign the handoff | freezes the guideline and the gold labels | Delivery → Handoff | `handoff-freeze` |
| 12 | Test, label the corpus, audit | label the test and audit samples | picks a labeling model, labels every item, audits the result | Quality · Delivery | `test-gold-lock` |

## Workflow map

One row per Run type (the 25 operations of `ref-run.md` §3), one column per
Space. A cell says what the Space does with that Run type: `start` means a
button there starts it, `shows` means its Result is read there, `—` means
nothing. Every Run is also listed in `Run → Runs`, so the Run Space has no
column. `started by` names the button or the channel; `not built yet` means no
engine writer exists today. The Board's `Run → Workflow map` view projects this
table and adds how many Runs of each type the job has. A definition, not an
inventory.

| compatibility tag | Run type | in words | started by | Data | Labeling | Quality | Delivery | writes to |
|---|---|---|---|---|---|---|---|---|
| P0 | `corpus-contract` | Set up the job | Chat: /subjective-label | shows · Contract, Schema | — | shows · Test (held-back count) | — | `gates/p0-contract/receipt.json` |
| P0 | `discovery-search` | Search outside evidence | not built yet | — | — | — | — | `discovery/search_<n>/result.json` |
| P0 | `guideline-seed` | Draft the guideline | part of setup (no Run of its own yet) | — | shows · Guideline | — | — | `policy/versions/G_00/` |
| P0 | `test-reserve` | Hold back test items | part of setup, before the job (no Run of its own yet) | shows · Contract | — | shows · Test | — | `test/sealed/status.json` |
| P0 | `embedding-build` | Build a map | Run embedding button | start + shows · Embedding | shows · map groups in Rounds | — | — | `cache/embeddings/<version>/` |
| P1 | `round-prepare` | Draw a round | Start round button | — | start + shows · Rounds | — | — | `rounds/round_NN/` |
| P1 | `weak-prelabel` | Weak models pre-label | not built yet | — | shows · comparison after you lock | — | — | `rounds/round_NN/prelabels/` |
| P1 | `human-calibration` | You label a round | your answers in chat | — | shows · Rounds | — | — | `rounds/round_NN/sessions/events.jsonl` |
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
| P4 | `human-review` | You review risky items | not built yet | — | shows · Rounds | — | — | `production/run_<n>/human_final.jsonl` |
| P4 | `reconcile` | Combine into final labels | not built yet | — | — | — | shows · Final labels | `production/run_<n>/run_report.md` |
| P5 | `audit-sample` | Draw an audit sample | not built yet | — | — | shows · Audit | — | `audit/final_<n>/sample.jsonl` |
| P5 | `audit-human-gold` | You label the audit sample | not built yet | — | shows · Rounds | shows · Audit | — | `audit/final_<n>/human_gold.jsonl` |
| P5 | `audit-analyze` | Analyze the audit | not built yet | — | — | shows · Audit | — | `audit/final_<n>/receipt.json` |
| P5 | `dstar-materialize` | Publish the final labeled corpus | not built yet | — | — | — | shows · Final labels | `corpus/final/D_star.jsonl` |

## Opening Space

The page opens on the Space that holds the next step. Engine status decides
it, checked in this order (the first match wins):

1. no `labeling/` job yet → `Data`
2. HOLD → `Data`
3. an integrity error → `Run`
4. compatibility tag P0 → `Data` (presentation only)
5. compatibility tag P1 → `Labeling` (presentation only)
6. any later compatibility tag → `Run` (presentation only)

A `?space=&view=` URL wins. Next comes the browser's saved choice, keyed by
Board source plus Page file. Only then does the next-step Space apply. An
unknown Space falls back to the next-step Space; an unknown view falls back to
that Space's first view.

## Item text

Overview views never render item text, sealed ids, or private judgments in the
page HTML. They show meanings, counts, checksums, and states. An item waiting in
a round's frozen batch (`human_batch.jsonl`) is first shown by the chat,
which records its `show` event (`calibration.open_item`). Once shown, its text
appears in the item table of the round's card in `Labeling → Rounds`, so
the person reads the round while labeling it in chat; an item never shown stays
"not opened yet" there. `Data → Embedding` may fetch the text of other
development items, only when the person asks: a group's typical items (action
`group_examples`) or one picked dot (action `embedding_item_text`). Items
waiting in a round are never returned there, so the first look at them, and
their `show` event, stays with the round. Every such fetch appends one line
to `labeling/exposure/group_examples.jsonl` (time, human, build, group, item
ids), so a later round can tell a fresh item from one already seen. The reveal
after a locked first answer shows reference observations, not gold. A sealed
item is never drawn, shown, or revealed.

## Write door

`POST /_board/labeling/act` is the only write. `Data → Contract` holds the
`Confirm meaning` button (`confirm_meaning`). `Labeling → Rounds` holds
`release_round` (`Start round 1`); `open_item`, `first`, and `final` stay in the
door but have no page button, since answers come from the chat. The
`Copy chat prompt` and `⧉ chat` buttons in `Labeling → Label` (the label
definitions) and `Labeling → Rounds` (the open round) only copy text. `Data → Embedding`
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
