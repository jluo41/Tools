# Labeling Space · UI ↔ Page Folder ↔ Run mapping

This is the orientation contract for the Labeling Workbench surface of
`workbench-labeling` (`plugins/haipipe-toolkit/servers/workbench-labeling/labeling.py`). It uses one location word:
**Space = Workspace** (one concept). The current adapter retains P0-P5 in the
Workflow drawer's Phases card (`?drawer=workflow`) as compatibility capability tags. They
are not Workflow nodes, Run owners, or routing authority. The adapter may use
them to choose a presentation Space only; Run eligibility and Routes come from
the shared Run Spec graph and native Run receipts.

## Two levels

The Board level (`<DOMAIN>/w/<board-slug>`, which redirects to
`/_board/labeling-board?path=<board.md>`) lists one card
per Page with an attached preparation owner, a linked accepted package, or a `labeling/` job; a
card opens that Page's surface below.
It also gives empty `S-Label-*` Pages a separate **Pages before Contract** link.
A flat Board source first needs its own Page folder; an already-folded Page can
start upstream work. Neither state invents a job or a Run.
The `all labeling jobs` link under the Page's title returns to the Board level.
The Board level has Guide and one Jobs Space and no writes. The rest of this file
is the Page level.

The dedicated Labeling host also opens a canonical Page folder directly at
`/workbench/labeling?file=<Page>/<Page>.md`, relative to its served root. That
Page has the same Spaces, Views, Runs panel, and checked action door without a
Board, generated Page URL, or Board overview. On either route, copy a Run
request into your agent conversation. Copying a request never starts a Run.

## Space roster

| order | Space | views | first question | canonical sources |
|---|---|---|---|---|
| 1 | **Data** | Preparation · Contract · Embedding | How is one transcript turned into a checked item, what does the corpus hold, and how does an item become a vector? | `corpus/source.yaml` (raw folder and column mapping) · `preparation-owner.yaml` (source attachment) · `preparation-ref.yaml` (accepted Result bindings) · `config.yaml` (corpus) · `corpus/manifest.json` · `test/sealed/status.json` · `cache/embeddings/<version>/manifest.json` |
| 2 | **Labeling** | Definition · Rounds · Guideline | What does each label mean and is that confirmed, which items does each round label in chat, and what does the guideline say now? | `config.yaml` (labels) · `gates/g0/receipt.json` · `gates/meaning-revisions/` · `../results/<definition-discussion run>/ledger.yaml` · `rounds/round_NN/human_batch.jsonl` · `rounds/round_NN/sessions/events.jsonl` · `corpus/items.jsonl` (Rounds only) · `policy/current` · `policy/versions/<G>/guideline.md` |
| 3 | **Quality** | Test · Evaluation · Audit · External gold (only for a `labeling/` Job with a gold Task) | Is the sealed test safe, and what evidence qualifies an executor and the final corpus? External gold: what the dataset's own labels say, and how ours score against them | `test/sealed/status.json` · `test/final/lock.json` · `evaluation/registry.yaml` · `audit/final_*/` · External gold reads the Job's sibling Tasks' `results/<run>/runtime.yaml` and `metrics.json` |
| 4 | **Delivery** | Handoff · Scan · Final labels | What is handed over, how is the corpus labeled under it, and what can a reader receive? | `handoff/label-v1.yaml` · `production/run_<n>/` · `corpus/final/D_star.jsonl` |

All paths in this roster are relative to the Page's `labeling/` folder;
Preparation Tickets and Results remain in the referenced source owner's
`corpus-preparation/` folder. A view exists only because Runs live in it (JL 260928): Schema merged
into Contract, Discussion and Label merged into Definition, and Scan joined
Delivery. Guideline is a view inside Labeling. The older Human tab and the Run
Space are gone, and so is the page bar (v3, 260927). Runs live in three places:

| where | what it shows | sources |
|---|---|---|
| the **Runs panel**, right of every Space | the current view's built Run types with counts, then the selected Run (Resume/Rerun, folded Prompt + Copy, Running process, Results) | `../runs/*.yaml` · `../results/*/runtime.yaml` · `../results/*/result.yaml` · linked `<source>/corpus-preparation/runs/*.yaml` and `results/*/` for Data → Preparation · this file's Run Type tables |
| `?drawer=workflow` (no button) | Phases (P0-P5 compatibility tags), then the SOP, then the Workflow map | `engine/job.py status()` · this file's `## SOP` and `## Workflow map` |
| `?drawer=allruns` (no button) | one row per Ticket: what ran, state, result | Page `../runs/*.yaml` and `../results/*/runtime.yaml` · linked source-owned Corpus Runs |

`../runs/` and `../results/` sit in the Page folder beside `labeling/`. Linked
Corpus Preparation Runs remain under the source folder and appear only when
their accepted package binds them to this Page. The Workflow map's `view`
column decides which view's Labeling Runs panel lists a type; the Corpus
Preparation table assigns its source-owned types to Data → Preparation. A type
not built yet stays in the map only. The panel lists a view's types in `step`
order.

Raw transcripts require a prior unit recipe and preparation. `Data →
Preparation` reads the five source-owned Run Types below. They are separate
from the current four-Space, 26-job-Run-Type catalogue; see
[`CORPUS-PREPARATION.md`](../../CORPUS-PREPARATION.md).
After a source owner is attached, its panel offers a new Run request only for
the next unfinished preparation step. It keeps completed Tickets readable;
once a package or Contract is bound to the Page, it offers no new source Run
from that Page.

## Corpus Preparation Run Types

| step | Run Type | in words | Skill | writes to |
|---:|---|---|---|---|
| 1 | `source-normalize` | Normalize source | `haipipe-labeling-preparation` | source snapshot, normalized conversations, reject ledger |
| 2 | `unit-recipe` | Choose labeling unit | `haipipe-labeling-preparation` | accepted target/context/group recipe |
| 3 | `unit-materialize` | Create candidate items | `haipipe-labeling-preparation` | private candidate set and lineage |
| 4 | `unit-check` | Check candidate items | `haipipe-labeling-preparation` | public QA receipt |
| 5 | `initial-group-reserve` | Reserve source groups | `haipipe-labeling-preparation` | source-level frame and fenced package |

## Run Type skills

Each row declares the Skills relevant to one Run Type. The Workflow map below
assigns that type to one Space and View. The eleven `haipipe-labeling-<view>`
Skills provide context for their respective Views; the other Skills are shared
across Run Types. In particular, `Quality · Test` contains both a Building and
a Scanning Run Type, so its View alone cannot determine the full Skill set.
The four entries in each current row describe the family architecture:
cross-view Run graph, Building/Scanning law, Building/Scanning order, and the
View's Run procedure. The View Skill is the primary procedure. Its current
instructions tell an agent performing the Run to load the other three and the
family entry Skill first. Four is not a rule for future Run Types or a claim
that a UI read or engine call loads them. The engine's checked writer still
owns execution and authorization.
`haipipe-labeling` is the family entry door and `workbench-labeling` is
the page surface; neither is a per-Run worker. The engine or named human is
the worker. These are **declared** Skills, not evidence that a historical Run
loaded them; current Tickets do not record Skill identities or versions.

| step | Run Type | declared Skills |
|---:|---|---|
| 1 | `corpus-contract` | `haipipe-labeling-workflow`, `haipipe-labeling-building`, `haipipe-labeling-contract` |
| 2 | `test-reserve` | `haipipe-labeling-workflow`, `haipipe-labeling-building`, `haipipe-labeling-test` |
| 3 | `embedding-build` | `haipipe-labeling-workflow`, `haipipe-labeling-building`, `haipipe-labeling-embedding` |
| 4 | `discovery-search` | `haipipe-labeling-workflow`, `haipipe-labeling-building`, `haipipe-labeling-definition` |
| 5 | `definition-discussion` | `haipipe-labeling-workflow`, `haipipe-labeling-building`, `haipipe-labeling-definition` |
| 6 | `guideline-seed` | `haipipe-labeling-workflow`, `haipipe-labeling-building`, `haipipe-labeling-guideline` |
| 7 | `round-prepare` | `haipipe-labeling-workflow`, `haipipe-labeling-building`, `haipipe-labeling-rounds` |
| 8 | `weak-prelabel` | `haipipe-labeling-workflow`, `haipipe-labeling-building`, `haipipe-labeling-rounds` |
| 9 | `human-calibration` | `haipipe-labeling-workflow`, `haipipe-labeling-building`, `haipipe-labeling-rounds` |
| 10 | `guideline-learn` | `haipipe-labeling-workflow`, `haipipe-labeling-building`, `haipipe-labeling-guideline` |
| 11 | `round-measure` | `haipipe-labeling-workflow`, `haipipe-labeling-building`, `haipipe-labeling-rounds` |
| 12 | `round-close` | `haipipe-labeling-workflow`, `haipipe-labeling-building`, `haipipe-labeling-rounds` |
| 13 | `handoff-freeze` | `haipipe-labeling-workflow`, `haipipe-labeling-building`, `haipipe-labeling-handoff` |
| 14 | `test-gold-lock` | `haipipe-labeling-workflow`, `haipipe-labeling-scanning`, `haipipe-labeling-test` |
| 15 | `executor-predict` | `haipipe-labeling-workflow`, `haipipe-labeling-scanning`, `haipipe-labeling-evaluation` |
| 16 | `executor-score` | `haipipe-labeling-workflow`, `haipipe-labeling-scanning`, `haipipe-labeling-evaluation` |
| 17 | `executor-select` | `haipipe-labeling-workflow`, `haipipe-labeling-scanning`, `haipipe-labeling-evaluation` |
| 18 | `scan-preflight` | `haipipe-labeling-workflow`, `haipipe-labeling-scanning`, `haipipe-labeling-scan` |
| 19 | `scan-shard` | `haipipe-labeling-workflow`, `haipipe-labeling-scanning`, `haipipe-labeling-scan` |
| 20 | `risk-route` | `haipipe-labeling-workflow`, `haipipe-labeling-scanning`, `haipipe-labeling-scan` |
| 21 | `human-review` | `haipipe-labeling-workflow`, `haipipe-labeling-scanning`, `haipipe-labeling-scan` |
| 22 | `reconcile` | `haipipe-labeling-workflow`, `haipipe-labeling-scanning`, `haipipe-labeling-scan` |
| 23 | `audit-sample` | `haipipe-labeling-workflow`, `haipipe-labeling-scanning`, `haipipe-labeling-audit` |
| 24 | `audit-human-gold` | `haipipe-labeling-workflow`, `haipipe-labeling-scanning`, `haipipe-labeling-audit` |
| 25 | `audit-analyze` | `haipipe-labeling-workflow`, `haipipe-labeling-scanning`, `haipipe-labeling-audit` |
| 26 | `dstar-materialize` | `haipipe-labeling-workflow`, `haipipe-labeling-scanning`, `haipipe-labeling-final-labels` |

## Run Type agents

Each row names the agent that carries out one Run Type and the decision the person
signs on it. The agent prepares the Run and calls the engine's checked writer; the
engine still owns execution and authorization, and the person never does a Run, only
signs what is theirs. A row that checks or measures another row's output (`unit-check`,
`round-measure`, `executor-score`, `scan-preflight`, `audit-analyze`) names an agent that
did not make it; the two checks belong to one checker that makes nothing. `(new)` marks an agent planned but not written yet. The Workbench Table
(`workbench-labeling/ref/workbench-table.md`) is
generated from this table, `## Corpus Preparation Run Types`, `## Run Type skills` and the
`view` column of the Workflow map; change a row here, then rerun its generator.

| step | Run Type | agent | person signs |
|---|---|---|---|
| 0a | `source-normalize` | corpus-preparer-agent (new) | none |
| 0b | `unit-recipe` | corpus-preparer-agent (new) | the labeling unit: target, context and grouping |
| 0c | `unit-materialize` | corpus-preparer-agent (new) | none |
| 0d | `unit-check` | labeling-checker-agent (new) | none |
| 0e | `initial-group-reserve` | corpus-preparer-agent (new) | the held-back test groups (custodian) |
| 1 | `corpus-contract` | moderator-agent | the contract: target, labeler and custodian |
| 2 | `test-reserve` | sampler-agent | the sealed test set (custodian) |
| 3 | `embedding-build` | embedder-agent | the embedding model |
| 4 | `discovery-search` | haipipe-discovery-orchestrator-agent | none |
| 5 | `definition-discussion` | moderator-agent | each label's meaning (G0) |
| 6 | `guideline-seed` | moderator-agent | none |
| 7 | `round-prepare` | sampler-agent | release of the round |
| 8 | `weak-prelabel` | labeler-panel-agent | none |
| 9 | `human-calibration` | moderator-agent | each item's final label |
| 10 | `guideline-learn` | moderator-agent | the guideline draft |
| 11 | `round-measure` | disagreement-analyzer-agent | none |
| 12 | `round-close` | gallery-keeper-agent | the checkpoint and its guideline |
| 13 | `handoff-freeze` | gallery-keeper-agent | the frozen handoff |
| 14 | `test-gold-lock` | gallery-keeper-agent | the blind test answers |
| 15 | `executor-predict` | labeler-panel-agent | none |
| 16 | `executor-score` | validator-agent | none |
| 17 | `executor-select` | validator-agent | the selected executor |
| 18 | `scan-preflight` | labeling-checker-agent (new) | the frozen production plan |
| 19 | `scan-shard` | labeler-panel-agent | none |
| 20 | `risk-route` | classifier-agent | none |
| 21 | `human-review` | moderator-agent | each reviewed item's label |
| 22 | `reconcile` | gallery-keeper-agent | none |
| 23 | `audit-sample` | sampler-agent | none |
| 24 | `audit-human-gold` | moderator-agent | the audit labels |
| 25 | `audit-analyze` | validator-agent | none |
| 26 | `dstar-materialize` | gallery-keeper-agent | release of the final labels |

## SOP

This is the supported first-use path in the current build. It ends after round 1:
guideline learning, measurement, round closure, round 2+, handoff, executor
evaluation, production scanning, audit, and D* materialization do not have
workers yet. Do not treat the 26-row Workflow map as a promise that those
operations can be run. `Run type` names the Run written by a step
(`—` means no Run; `gate G0` is a human confirmation, not a Run).
For an already-unitized single-unit legacy source, the older fenced-source
path can begin at step 1; steps 0a–0e do not acquire retrospective Runs.

| step | what happens | you do | the chat or engine does | where | Run type |
|---|---|---|---|---|---|
| 0a | Attach and normalize a transcript source | Give your agent conversation the transcript JSONL and source folder; attach its preparation owner to this Page, then use the copied `source-normalize` prompt | The Page shows each source Run as it closes; normalization validates ordered turns and source groups and writes a reject ledger | Data · Preparation | `source-normalize` |
| 0b | Choose the labeling unit | As preparation owner, choose final or every assistant reply and its earlier-context window | Freezes one accepted recipe | Data · Preparation | `unit-recipe` |
| 0c | Create candidate items | Use the copied `unit-materialize` prompt for that source and recipe | Writes deterministic private targets, prior context, and lineage | Data · Preparation | `unit-materialize` |
| 0d | Check the candidate set | Review the unit choices and run `unit-check` | Recomputes units and verifies IDs, context, lineage, and group identity | Data · Preparation | `unit-check` |
| 0e | Reserve source groups and link | Name the custodian, seed, and count of whole source groups; run `initial-group-reserve`, then link its accepted package to the Page | Keeps sealed text under source custody, writes an eligible-only package and Page reference | Data · Preparation | `initial-group-reserve` |
| 1 | Create one labeling job | On the linked Page, copy the Data → Contract request into your agent conversation with `/haipipe-labeling`, the accepted package and target, and the semantic human | Verifies preparation and custody receipts, imports eligible data, records the initial guideline, and writes the first Labeling Run | Agent conversation → Data · Contract | `corpus-contract` |
| 2 | Discuss what the labels mean | Select `+ New Run` then `Copy` (or use `Resume`) in Labeling → Definition; paste into your agent conversation, then settle each label: keep its wording or give your own | Asks one question at a time, proposes wording and made-up edge cases (never a round item), and records only your decisions; closing writes the ledger and, if any wording changed, one meaning revision that retires the old G0 | Labeling · Definition + agent conversation | `definition-discussion` |
| 3 | Confirm what the labels mean | Once every label has nonblank wording and any discussion is closed, the configured human reviews the question and definitions, then presses Confirm meaning and attests as that human. If an intact earlier attestation exists but only G0 is missing, press Restore G0 receipt instead. | Checks the contract, records G0, and makes round 1 eligible. Restore uses the earlier semantic attestation; a new confirmation cannot retroactively authorize a released round. | Labeling · Definition | gate G0 |
| 4 | Build a map (optional) | After the P0 files pass integrity checks and the job is not on HOLD, choose a model and press Run embedding; G0 is not required | Builds the requested embedding and shows its map and groups | Data · Embedding | `embedding-build` |
| 5 | Release round 1 | After G0 passes, choose the batch size and press Start round 1 | Draws eligible items only and writes the prepared-round Run | Labeling · Rounds | `round-prepare` |
| 6 | Label the open round | Select `+ New Run` for `human-calibration` before the first item, then `Copy`; use `Resume` once its Run exists. Paste the request into your agent conversation and give your first and final labels for each item | Opens each item through the calibration writer; records first, lock, reveal, and final in order. The human-calibration Run starts when the first item is opened | Labeling · Rounds + agent conversation | `human-calibration` |
| 7 | Stop after round 1 is judged | Check the round and Run inventory. If every item has a final event but the calibration Result is still running, use its `Resume` request to finalize the same Run; do not release round 2 | Preserves the judgments and stops at the missing Checkpoint Keeper; no gold is promoted and the guideline remains G_00 | Labeling · Rounds · All runs | `round-close` |

The actual Tickets and their runtime status/outcome are in the Runs panels and `?drawer=allruns`.
The Workflow map below is a Run Type catalogue, not a list of work that has
already happened. A displayed count is not a substitute for the matching
Ticket or its status.

## Workflow map

One row per Run Type (the 26 operation kinds in `ref-run.md` §3), with one
column per artifact Space. The `view` column names the Space view whose Runs
panel lists the type (the labeling workbench reads it; a view shows only its own
types, in `step` order). Every type has exactly one view. The table is deliberately a definition, not an
inventory: it must never imply that a Run exists just because its type has a
row. Use these action words consistently:

- `Start here`: a real, visible page control exists at the named location and
  its listed prerequisites pass. The map itself is not a start button.
- `Chat command`: setup starts from a command sent in the agent conversation. It is not a
  page button or a copy-prompt affordance.
- `Copy request → paste and send`: copy-only text for one concrete next
  interaction. The person must paste and send it in the agent conversation; copying does
  not call a writer, create a Run, or change job state.
- `Shown here · read-only`: this view reads an existing canonical artifact;
  it does not mean the named Run Type ran.
- `not built yet`: no worker can execute this Run Type today. Keep this exact
  value in `started by` because the current SOP presenter uses it to mark
  unbuilt steps.
- `—`: this Space has no result or action for this Run Type; it does not mean
  “not yet” or “not built.”

The Board currently projects the plain name and Run Type, `started by`, the
four artifact-Space cells, output path, and a per-type count. The count is only
a count. The separate Runs panels and `?drawer=allruns` read allocated Tickets and
runtime receipts and is the source for each actual Run's id, status, and
outcome. Never synthesize a matching Run/status from a catalogue row. Each Run
card names its Run Type's declared Skills from `## Run Type skills`; bounded target,
prerequisites, and a matching Ticket/status are not rendered inside this matrix.

| step | compatibility tag | Run type | in words | started by | Data | Labeling | Quality | Delivery | writes to | view |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | P0 | `corpus-contract` | Set up the job | Copy request → paste and send · Data → Contract after an accepted Corpus Preparation package is linked to this Page; `/haipipe-labeling` validates the package and creates the job | Start here + Shown here · read-only · Contract after setup | — | Shown here · read-only · held-back count only | — | `gates/p0-contract/receipt.json` | Data · Contract |
| 2 | P0 | `test-reserve` | Hold back test items | not built yet | Shown here · read-only · setup's held-back count | — | Shown here · read-only · sealed-test status | — | `test/sealed/status.json` | Quality · Test |
| 3 | P0 | `embedding-build` | Build a map | Start here · Data → Embedding button; explicit human model choice; P0 integrity valid and no HOLD; G0 not required | Start here + Shown here · read-only · Embedding | Shown here · read-only · map groups in Rounds | — | — | `cache/embeddings/<version>/` | Data · Embedding |
| 4 | P0 | `discovery-search` | Search outside evidence | not built yet | — | — | — | — | `discovery/search_<n>/result.json` | Labeling · Definition |
| 5 | P0 | `definition-discussion` | Discuss the label meanings | Copy request → paste and send · `+ New Run` or `Resume` in the Runs panel of Labeling → Definition; the chat records only the human's stated decisions; close it before releasing a round | — | Start here + Shown here · read-only · Definition shows each label before and after, then Confirm meaning | — | — | `results/<run>/ledger.yaml` · `gates/meaning-revisions/<seq>.json` | Labeling · Definition |
| 6 | P0 | `guideline-seed` | Draft a guideline candidate | not built yet | — | Shown here · read-only · G_00 is created by corpus-contract, not this Run | — | — | `policy/versions/G_00/` | Labeling · Guideline |
| 7 | P1 | `round-prepare` | Draw one round | Start here · Start round 1 after G0 passes; the identified human releases it | — | Start here + Shown here · read-only · Rounds | — | — | `rounds/round_NN/` | Labeling · Rounds |
| 8 | P1 | `weak-prelabel` | Pre-label one prepared round | not built yet | — | — | — | — | `rounds/round_NN/prelabels/` | Labeling · Rounds |
| 9 | P1 | `human-calibration` | You label one round | Copy request → paste and send · only for a released open round with items left; first item open starts the Run | — | Shown here · read-only · Rounds; actual Ticket/status is in Runs | — | — | `rounds/round_NN/sessions/events.jsonl` | Labeling · Rounds |
| 10 | P1 | `guideline-learn` | Draft a guideline from accepted judgments | not built yet | — | Not built · no policy-draft result is produced or shown | — | — | `rounds/round_NN/policy_draft/` | Labeling · Guideline |
| 11 | P1 | `round-measure` | Measure one completed judgment set | not built yet | — | Not built · no round metrics are produced or shown | — | — | `rounds/round_NN/metrics.json` | Labeling · Rounds |
| 12 | P1 | `round-close` | Close a measured round | not built yet | — | Not built · no checkpoint or guideline promotion is produced | — | — | `rounds/round_NN/checkpoint.json` | Labeling · Rounds |
| 13 | P2 | `handoff-freeze` | Freeze a stopped labeling lineage | not built yet | — | — | — | Not built · Handoff result has no writer | `handoff/label-v1.yaml` | Delivery · Handoff |
| 14 | P3 | `test-gold-lock` | Lock blind answers for the final test | not built yet | — | — | Not built · no final test lock is produced | — | `test/final/lock.json` | Quality · Test |
| 15 | P3 | `executor-predict` | Have one registered model predict the test | not built yet | — | — | Not built · no predictions are produced | — | `evaluation/predictions/` | Quality · Evaluation |
| 16 | P3 | `executor-score` | Score one closed set of predictions | not built yet | — | — | Not built · no scorecards are produced | — | `evaluation/scorecards/` | Quality · Evaluation |
| 17 | P3 | `executor-select` | Select from the complete scorecard set | not built yet | — | — | Not built · no selection is produced | — | `evaluation/summary.md` | Quality · Evaluation |
| 18 | P4 | `scan-preflight` | Check one frozen production plan | not built yet | — | — | — | Not built · Scan | `production/run_<n>/preflight.json` | Delivery · Scan |
| 19 | P4 | `scan-shard` | Label one frozen corpus shard | not built yet | — | — | — | Not built · Scan | `production/run_<n>/` | Delivery · Scan |
| 20 | P4 | `risk-route` | Route risky production items to review | not built yet | — | — | — | Not built · Scan | `production/run_<n>/risk_queue.jsonl` | Delivery · Scan |
| 21 | P4 | `human-review` | You label one production risk queue | not built yet | — | — | — | Not built · Scan review of the risk queue; not calibration Rounds | `production/run_<n>/human_final.jsonl` | Delivery · Scan |
| 22 | P4 | `reconcile` | Reconcile reviewed items into a candidate corpus | not built yet | — | — | — | Not built · Scan; the candidate corpus is not D* | `production/run_<n>/run_report.md` | Delivery · Scan |
| 23 | P5 | `audit-sample` | Draw from one frozen audit design | not built yet | — | — | Not built · no audit sample is produced | — | `audit/final_<n>/sample.jsonl` | Quality · Audit |
| 24 | P5 | `audit-human-gold` | Blind-label one audit sample | not built yet | — | — | Not built · Quality/Audit only; not calibration Rounds | — | `audit/final_<n>/human_gold.jsonl` | Quality · Audit |
| 25 | P5 | `audit-analyze` | Analyze one completed audit sample | not built yet | — | — | Not built · no audit receipt is produced | — | `audit/final_<n>/receipt.json` | Quality · Audit |
| 26 | P5 | `dstar-materialize` | Publish an accepted audited corpus | not built yet | — | — | — | Not built · D* requires the later audit path | `corpus/final/D_star.jsonl` | Delivery · Final labels |

### Run ownership and card fields

The shared `haipipe-labeling-workflow` Skill owns the graph and Routes. The
table above explicitly assigns the Building or Scanning domain/procedure
Skills to each Run Type, along with its View context Skill. These are
Run Type guidance, not per-Run worker assignments. The current
Ticket contract has `worker.kind/name`, but no canonical `owner_skill` or
`worker_skill` field. For the implemented paths, the worker is an engine
module (for example `engine/job.py`, `engine/embedding_build.py`, or
`engine/calibration.py`), not a Skill. For unbuilt operations there is no
worker. Never infer a Skill owner or worker from P0–P5.

The supported Run paths and their current entry points are:

| Run Type | bounded work | workflow and domain Skills | actor and prerequisites | implemented worker and entry |
|---|---|---|---|---|
| `corpus-contract` | One imported, fenced corpus snapshot and target | `haipipe-labeling-workflow`; `haipipe-labeling-building` + `haipipe-labeling-building` | The identified semantic human and sealed-test custodian; a real Page, accepted preparation package, target, and named owners | Data → Contract offers a copy request only after the package is linked and before a job exists. Paste it into your agent conversation for `/haipipe-labeling` to validate the package and call `job.py create`. |
| `definition-discussion` | One version of the target's label meanings before round release | `haipipe-labeling-workflow`; `haipipe-labeling-building` + `haipipe-labeling-building`; `haipipe-labeling-definition` | The configured semantic human settles each label's meaning; a valid Contract and no released round are required | Labeling → Definition offers `+ New Run` or `Resume` in the Runs panel. Copy its request into your agent conversation; `definition_discussion.py` records the decisions and closes the Run. |
| `embedding-build` | One corpus × embedder version | `haipipe-labeling-workflow`; `haipipe-labeling-building` + `haipipe-labeling-building` | A named human chooses a catalog model/settings; P0 files pass integrity and the job is not on HOLD. G0 is not required. | `embedding_build.py`; Start here in Data → Embedding. |
| `round-prepare` | One released Card; only round 1 is supported today | `haipipe-labeling-workflow`; `haipipe-labeling-building` + `haipipe-labeling-building` | The identified human releases the Card after valid G0, with no HOLD or open definition discussion | `calibration.release_round`; Start round 1 in Labeling → Rounds. |
| `human-calibration` | One frozen human batch | `haipipe-labeling-workflow`; `haipipe-labeling-building` + `haipipe-labeling-building` | The configured semantic human labels a released round with G0 passed, no HOLD, and an item remaining | `calibration.open_item`, `record_first`, and `record_final`; select `+ New Run` then `Copy` before the first item, or use `Resume` after the Run exists. Paste the request into your agent conversation. Copying is inert; the first item open allocates the Run. If the last final event preceded an interrupted close, `calibration.py finalize` completes that same Result. |

These Skills describe the workflow and domain; they are not worker Skill
assignments recorded on those Tickets. The current map can truthfully show a
Start entry for embedding and round preparation and a Copy entry for human
calibration. It can show a bounded Contract copy request only after the accepted
source package is linked. The other 21 Run Types
have no prompt or start affordance today.

The current human-calibration prompt binds the Board, Page, job folder, Run
Type and round target, declared Run Type Skills, G0 and Card prerequisites,
matching Ticket id/status when it exists, question, label names, progress,
pending items, and JUDGE-by-chat instructions. It names no worker Skill,
because the Ticket contract declares no such field. The current
`corpus-contract` copy request
binds the Page folder and accepted package path, then asks the agent to confirm
the target, job ID, semantic human, and custodian before it writes. It remains
clipboard-only until the person pastes and sends it.

Every future per-Run card should show the Run Type and plain name, one bounded
target, graph/domain Skills, declared actor, exact prerequisites, truthful
action state, and only an actual matching Ticket's id/status/outcome. For
prompts, include the Board/Folder/Page, target, Run Type, relevant Skills,
prerequisite state, matching Run if present, and the next permitted human or
agent action. Hide the copy affordance when there is no concrete next
interaction or the operation is held/not built. Copying text remains inert:
it must not send a message, allocate a Run, or write a receipt. The live
adapter needs a host-side change to render these fields in the matrix.

## Opening Space

The page opens on the Space that holds the next step. Engine status decides
it, checked in this order (the first match wins):

1. no `labeling/` job yet → `Data`
2. HOLD → `Data`
3. an integrity error → `Data`
4. compatibility tag P0 → `Data` (presentation only)
5. compatibility tag P1 → `Labeling` (presentation only)
6. any later compatibility tag → `Data` (presentation only)

A `?space=&view=` URL wins. Next comes the browser's saved choice, keyed by
Board source plus Page file. Only then does the next-step Space apply. An
unknown Space falls back to the next-step Space; an unknown view falls back to
that Space's first view.

## Item text

Overview views never render item text, sealed ids, or private judgments in the
page HTML. They show meanings, counts, and states. An item waiting in
a round's frozen batch (`human_batch.jsonl`) is first shown by the chat,
which records its `show` event (`calibration.open_item`). Once shown, its text
appears in the item table of the round's card in `Labeling → Rounds`, so
the person reads the round while labeling it in chat; an item never shown stays
"not opened yet" there. `Data → Embedding` may fetch the text of other
development items, only when the person asks: a group's typical items (action
`group_examples`) or one picked dot (action `embedding_item_text`); `Data →
Preparation` pages through the items to label (action `item_page`). Items
waiting in a round are never returned there, so the first look at them, and
their `show` event, stays with the round. Every such fetch appends one line
to `labeling/exposure/group_examples.jsonl` (time, human, build, group, item
ids), so a later round can tell a fresh item from one already seen. The reveal
after a locked first answer shows reference observations, not gold. A sealed
item is never drawn, shown, or revealed.

## Write door

`POST /_board/labeling/act` is the only write. `Labeling → Definition` holds
the `Confirm meaning` button (`confirm_meaning`). `Labeling → Rounds` holds
`release_round` (`Start round 1`); `open_item`, `first`, and `final` stay in the
door but have no page button, since answers come from the chat. The
`definition-discussion` Run's `+ New Run` and `Resume` (Labeling → Definition)
and the open round's `human-calibration` `+ New Run` or `Resume` only copy text; the discussion writes
through `engine/definition_discussion.py` in chat, never through the door. `Data → Embedding`
holds five: `build_embedding`, `embedding_status`, `embedding_item`,
`group_examples`, `embedding_item_text`; `Data → Preparation` holds `item_page`. Quality and Delivery have no
write control, and a Runs panel only copies prompts. The checks behind each action are the
write-and-authority law in
`../../workbench-labeling/SKILL.md`.

## Projection law

The four Spaces are views over one page-local `labeling/` folder, not storage
folders. A new Labeling Run is `run-labeling-<operation>-<MMDD>-<target>`, with its Ticket at
`<Page>/runs/<run>.yaml` and its Result at `<Page>/results/<run>/`, beside
`labeling/`. Receipt paths are relative to the Page. The 26
operation kinds and the count law are in `ref-run.md`. A round is an episode
that groups Runs. Each item judgment is an event inside the
`run-labeling-human-calibration-<MMDD>-round-NN` Run, never a Run of its own.
