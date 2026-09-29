# Labeling Space · UI ↔ Page Folder ↔ Run mapping

This is the orientation contract for the Board Labeling surface of
`haipipe-workbench-labeling` (`plugins/subjective-label/servers/workbench-labeling/labeling.py`). It uses one location word:
**Space = Workspace** (one concept). The current adapter retains P0-P5 in the
Workflow drawer's Phases card (`?drawer=workflow`) as compatibility capability tags. They
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
| 1 | **Data** | Contract · Embedding | What is one item, what does the corpus hold, and how does an item become a vector? | `config.yaml` (corpus) · `corpus/manifest.json` · `corpus/imported_label_summary.json` · `test/sealed/status.json` · `cache/embeddings/<version>/manifest.json` |
| 2 | **Labeling** | Definition · Rounds · Guideline | What does each label mean and is that confirmed, which items does each round label in chat, and what does the guideline say now? | `config.yaml` (labels) · `gates/g0/receipt.json` · `gates/meaning-revisions/` · `../results/<definition-discussion run>/ledger.yaml` · `rounds/round_NN/human_batch.jsonl` · `rounds/round_NN/sessions/events.jsonl` · `corpus/items.jsonl` (Rounds only) · `policy/current` · `policy/versions/<G>/guideline.md` |
| 3 | **Quality** | Test · Evaluation · Audit | Is the sealed test safe, and what evidence qualifies an executor and the final corpus? | `test/sealed/status.json` · `test/final/lock.json` · `evaluation/registry.yaml` · `audit/final_*/` |
| 4 | **Delivery** | Handoff · Scan · Final labels | What is handed over, how is the corpus labeled under it, and what can a reader receive? | `handoff/label-v1.yaml` · `production/run_<n>/` · `corpus/final/D_star.jsonl` |

All paths are relative to the Page's `labeling/` folder, except the engine
call. A view exists only because Runs live in it (JL 260928): Schema merged
into Contract, Discussion and Label merged into Definition, and Scan joined
Delivery. Guideline is a view inside Labeling. The older Human tab and the Run
Space are gone, and so is the page bar (v3, 260927). Runs live in three places:

| where | what it shows | sources |
|---|---|---|
| the **Runs panel**, right of every Space | the current view's built Run types with counts, then the selected Run (Resume/Rerun, folded Prompt + Copy, Running process, Results) | `../runs/*.yaml` · `../results/*/runtime.yaml` · `../results/*/result.yaml` · this file's Workflow map `view` column |
| `?drawer=workflow` (no button) | Phases (P0-P5 compatibility tags), then the SOP, then the Workflow map | `engine/job.py status()` · this file's `## SOP` and `## Workflow map` |
| `?drawer=allruns` (no button) | one row per Ticket: what ran, state, result | `../runs/*.yaml` · `../results/*/runtime.yaml` |

`../runs/` and `../results/` sit in the Page folder beside `labeling/`. The
Workflow map's `view` column decides which view's Runs panel lists a type; a
type not built yet stays in the map only. The panel lists a view's types in
`step` order.

## View skills

Each view has exactly one skill, and no other view uses it (JL 260929). Every
Run card in a view names that skill; the Runs panel reads this table.

| view | skill |
|---|---|
| Data · Contract | `subjective-label-contract` |
| Data · Embedding | `subjective-label-embedding` |
| Labeling · Definition | `subjective-label-definition` |
| Labeling · Rounds | `subjective-label-rounds` |
| Labeling · Guideline | `subjective-label-guideline` |
| Quality · Test | `subjective-label-test` |
| Quality · Evaluation | `subjective-label-evaluation` |
| Quality · Audit | `subjective-label-audit` |
| Delivery · Handoff | `subjective-label-handoff` |
| Delivery · Scan | `subjective-label-scan` |
| Delivery · Final labels | `subjective-label-final-labels` |

## SOP

This is the supported first-use path in the current build. It ends after round 1:
guideline learning, measurement, round closure, round 2+, handoff, executor
evaluation, production scanning, audit, and D* materialization do not have
workers yet. Do not treat the 26-row Workflow map as a promise that those
operations can be run. `Run type` names the Run written by a step
(`—` means no Run; `gate G0` is a human confirmation, not a Run).

| step | what happens | you do | the chat or engine does | where | Run type |
|---|---|---|---|---|---|
| 1 | Create one labeling job | On a real Page, give Studio Chat `/subjective-label`, the source corpus and target, and identify the semantic human and sealed-test custodian (one person may hold both roles) | Fences the source before development reads, imports the corpus and held-back test, records the initial guideline, and writes the first Run | Studio Chat → Data · Contract | `corpus-contract` |
| 2 | Discuss what the labels mean | Copy `+ New Run` (or `Resume`) from the Runs panel of Labeling → Definition into Studio Chat, then settle each label: keep its wording or give your own | Asks one question at a time, proposes wording and made-up edge cases (never a round item), and records only your decisions; closing writes the ledger and, if any wording changed, one meaning revision that retires the old G0 | Labeling · Definition + Studio Chat | `definition-discussion` |
| 3 | Confirm what the labels mean | The configured human reviews the question and definitions, then presses Confirm meaning and attests as that human | Checks the contract, records the G0 receipt, and makes round 1 eligible; the local Board records the supplied id but does not authenticate identity | Labeling · Definition | gate G0 |
| 4 | Build a map (optional) | After the P0 files pass integrity checks and the job is not on HOLD, choose a model and press Run embedding; G0 is not required | Builds the requested embedding and shows its map and groups | Data · Embedding | `embedding-build` |
| 5 | Release round 1 | After G0 passes, choose the batch size and press Start round 1 | Draws eligible items only and writes the prepared-round Run | Labeling · Rounds | `round-prepare` |
| 6 | Label the open round | Copy `Resume` on this round's `human-calibration` Run in the Runs panel, paste it into Studio Chat in this repository, and give your first answer and final label for each item | Opens each item through the calibration writer; records first, lock, reveal, and final in order. The human-calibration Run starts when the first item is opened | Labeling · Rounds + Studio Chat | `human-calibration` |
| 7 | Stop after round 1 is judged | Check the round and Run inventory. Do not try to release round 2 | Preserves the judgments and stops at the missing Checkpoint Keeper; no gold is promoted and the guideline remains G_00 | Labeling · Rounds · All runs | `round-close` |

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
- `Chat command`: setup starts from a command sent in Studio Chat. It is not a
  page button or a copy-prompt affordance.
- `Copy request → paste and send`: copy-only text for one concrete next
  interaction. The person must paste and send it in Studio Chat; copying does
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
card names its view's one skill from `## View skills`; bounded target,
prerequisites, and a matching Ticket/status are not rendered inside this matrix.

| step | compatibility tag | Run type | in words | started by | Data | Labeling | Quality | Delivery | writes to | view |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | P0 | `corpus-contract` | Set up the job | Chat command · in Studio Chat, invoke `/subjective-label`; no page control | Shown here · read-only · Contract after setup | — | Shown here · read-only · held-back count only | — | `gates/p0-contract/receipt.json` | Data · Contract |
| 2 | P0 | `test-reserve` | Hold back test items | not built yet | Shown here · read-only · setup's held-back count | — | Shown here · read-only · sealed-test status | — | `test/sealed/status.json` | Quality · Test |
| 3 | P0 | `embedding-build` | Build a map | Start here · Data → Embedding button; explicit human model choice; P0 integrity valid and no HOLD; G0 not required | Start here + Shown here · read-only · Embedding | Shown here · read-only · map groups in Rounds | — | — | `cache/embeddings/<version>/` | Data · Embedding |
| 4 | P0 | `discovery-search` | Search outside evidence | not built yet | — | — | — | — | `discovery/search_<n>/result.json` | Labeling · Definition |
| 5 | P0 | `definition-discussion` | Discuss the label meanings | Copy request → paste and send · `+ New Run` or `Resume` in the Runs panel of Labeling → Definition; the chat records only the human's stated decisions; only before any item is judged | — | Start here + Shown here · read-only · Definition shows each label before and after, then Confirm meaning | — | — | `results/<run>/ledger.yaml` · `gates/meaning-revisions/<seq>.json` | Labeling · Definition |
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
| 21 | P4 | `human-review` | Review one frozen production risk queue | not built yet | — | — | — | Not built · Scan review of the risk queue; not calibration Rounds | `production/run_<n>/human_final.jsonl` | Delivery · Scan |
| 22 | P4 | `reconcile` | Reconcile reviewed items into a candidate corpus | not built yet | — | — | — | Not built · Scan; the candidate corpus is not D* | `production/run_<n>/run_report.md` | Delivery · Scan |
| 23 | P5 | `audit-sample` | Draw from one frozen audit design | not built yet | — | — | Not built · no audit sample is produced | — | `audit/final_<n>/sample.jsonl` | Quality · Audit |
| 24 | P5 | `audit-human-gold` | Blind-label one audit sample | not built yet | — | — | Not built · Quality/Audit only; not calibration Rounds | — | `audit/final_<n>/human_gold.jsonl` | Quality · Audit |
| 25 | P5 | `audit-analyze` | Analyze one completed audit sample | not built yet | — | — | Not built · no audit receipt is produced | — | `audit/final_<n>/receipt.json` | Quality · Audit |
| 26 | P5 | `dstar-materialize` | Publish an accepted audited corpus | not built yet | — | — | — | Not built · D* requires the later audit path | `corpus/final/D_star.jsonl` | Delivery · Final labels |

### Run ownership and card fields

The shared `subjective-label-workflow` Skill owns the graph and Routes. P0–P2
use `label-building` for domain law and `label-building-workflow` for
procedures; P3–P5 use `label-scanning` and `label-scanning-workflow`.
These are family-level Skills, not per-Run worker assignments. The current
Ticket contract has `worker.kind/name`, but no canonical `owner_skill` or
`worker_skill` field. For the implemented paths, the worker is an engine
module (for example `engine/job.py`, `engine/embedding_build.py`, or
`engine/calibration.py`), not a Skill. For unbuilt operations there is no
worker. Never infer a Skill owner or worker from P0–P5.

The supported Run paths and their current entry points are:

| Run Type | bounded work | workflow and domain Skills | actor and prerequisites | implemented worker and entry |
|---|---|---|---|---|
| `corpus-contract` | One imported, fenced corpus snapshot and target | `subjective-label-workflow`; `label-building` + `label-building-workflow` | The identified semantic human and sealed-test custodian; a real Page, eligible source, target, and named owners | `fence_source.py` + `job.py create`; invoke `/subjective-label` in Studio Chat. There is no in-page copy control today. |
| `embedding-build` | One corpus × embedder version | `subjective-label-workflow`; `label-building` + `label-building-workflow` | A named human chooses a catalog model/settings; P0 files pass integrity and the job is not on HOLD. G0 is not required. | `embedding_build.py`; Start here in Data → Embedding. |
| `round-prepare` | One released Card; only round 1 is supported today | `subjective-label-workflow`; `label-building` + `label-building-workflow` | The identified human releases the Card after valid G0, with no HOLD | `calibration.release_round`; Start round 1 in Labeling → Rounds. |
| `human-calibration` | One frozen human batch | `subjective-label-workflow`; `label-building` + `label-building-workflow` | The configured semantic human labels a released round with G0 passed, no HOLD, and an item remaining | `calibration.open_item`, `record_first`, and `record_final`; copy the open-round prompt into Studio Chat. Copying is inert; the first item open allocates the Run. |

These Skills describe the workflow and domain; they are not worker Skill
assignments recorded on those Tickets. The current map can truthfully show a
Start entry for embedding and round preparation and a Copy entry for human
calibration. It can show the chat command for contract setup, but must not call
that a copy prompt while the page has no such control. The other 21 Run Types
have no prompt or start affordance today.

The current human-calibration prompt binds the job folder, question, label
names, round progress, pending items, and JUDGE-by-chat instructions. It does
not yet carry a stable Board/Folder/Page identity, exact target field, matching
Ticket id/status, or explicit prerequisite result. Per-Run worker Skills are
not declared in the Ticket contract, so the prompt cannot truthfully name one.
The prompt is useful for the current open round, but it does not yet meet the
full context-card contract above. A future setup prompt for `corpus-contract`
is valid only before a job exists and only when it can bind this Page, source,
target, semantic human, custodian, relevant Skills, and the no-existing-Run
state; it must remain clipboard-only until the person pastes and sends it.

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
`group_examples`) or one picked dot (action `embedding_item_text`). Items
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
and the open round's `Resume` only copy text; the discussion writes
through `engine/definition_discussion.py` in chat, never through the door. `Data → Embedding`
holds five: `build_embedding`, `embedding_status`, `embedding_item`,
`group_examples`, `embedding_item_text`. Quality and Delivery have no
write control, and a Runs panel only copies prompts. The checks behind each action are the
write-and-authority law in
`../../label-building-workflow/haipipe-workbench-labeling/SKILL.md`.

## Projection law

The four Spaces are views over one page-local `labeling/` folder, not storage
folders. A Run is `rlNN_<operation>_<target>`, with its Ticket at
`<Page>/runs/<run>.yaml` and its Result at `<Page>/results/<run>/`, beside
`labeling/`. Receipt paths are relative to the Page. The 26
operation kinds and the count law are in `ref-run.md`. A round is an episode
that groups Runs. Each item judgment is an event inside the
`rlNN_human-calibration_round-NN` Run, never a Run of its own.
