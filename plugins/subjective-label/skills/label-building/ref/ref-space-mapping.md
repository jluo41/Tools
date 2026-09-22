# Labeling Space · UI ↔ Page Folder ↔ Run mapping

This is the orientation contract for the Board Labeling surface of
`haipipe-workbench-labeling` (`plugins/subjective-label/servers/workbench-labeling/labeling.py`). It uses one location word:
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

This is the supported first-use path in the current build. It ends after round 1:
guideline learning, measurement, round closure, round 2+, handoff, executor
evaluation, production scanning, audit, and D* materialization do not have
workers yet. Do not treat the 25-row Workflow map as a promise that those
operations can be run. `Run type` names the Run written by a step
(`—` means no Run; `gate G0` is a human confirmation, not a Run).

| step | what happens | you do | the chat or engine does | where | Run type |
|---|---|---|---|---|---|
| 1 | Create one labeling job | On a real Page, give Studio Chat `/subjective-label`, the source corpus and target, and identify the semantic human and sealed-test custodian (one person may hold both roles) | Fences the source before development reads, imports the corpus and held-back test, records the initial guideline, and writes the first Run | Studio Chat → Data · Contract | `corpus-contract` |
| 2 | Confirm what the labels mean | The configured human reviews the question and definitions, then presses Confirm meaning and attests as that human | Checks the contract, records the G0 receipt, and makes round 1 eligible; the local Board records the supplied id but does not authenticate identity | Data · Contract | gate G0 |
| 3 | Build a map (optional) | After the P0 files pass integrity checks and the job is not on HOLD, choose a model and press Run embedding; G0 is not required | Builds the requested embedding and shows its map and groups | Data · Embedding | `embedding-build` |
| 4 | Release round 1 | After G0 passes, choose the batch size and press Start round 1 | Draws eligible items only and writes the prepared-round Run | Labeling · Rounds | `round-prepare` |
| 5 | Label the open round | Copy the prompt for this open round, paste it into Studio Chat in this repository, and give your first answer and final label for each item | Opens each item through the calibration writer; records first, lock, reveal, and final in order. The human-calibration Run starts when the first item is opened | Labeling · Rounds + Studio Chat | `human-calibration` |
| 6 | Stop after round 1 is judged | Check the round and Run inventory. Do not try to release round 2 | Preserves the judgments and stops at the missing Checkpoint Keeper; no gold is promoted and the guideline remains G_00 | Labeling · Rounds · Run → Runs | `round-close` |

The actual Tickets and their runtime status/outcome are in `Run → Runs`.
The Workflow map below is a Run Type catalogue, not a list of work that has
already happened. A displayed count is not a substitute for the matching
Ticket or its status.

## Workflow map

One row per Run Type (the 25 operation kinds in `ref-run.md` §3), with one
column per artifact Space. The table is deliberately a definition, not an
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
a count. The separate `Run → Runs` inventory reads allocated Tickets and
runtime receipts and is the source for each actual Run's id, status, and
outcome. Never synthesize a matching Run/status from a catalogue row. The
current presenter does not yet show owner/worker Skills, bounded target,
prerequisites, or a matching Ticket/status inside this matrix; those need a
host-adapter change before the map can claim to render them.

| compatibility tag | Run type | in words | started by | Data | Labeling | Quality | Delivery | writes to |
|---|---|---|---|---|---|---|---|---|
| P0 | `corpus-contract` | Set up the job | Chat command · in Studio Chat, invoke `/subjective-label`; no page control | Shown here · read-only · Contract and Schema after setup | — | Shown here · read-only · held-back count only | — | `gates/p0-contract/receipt.json` |
| P0 | `discovery-search` | Search outside evidence | not built yet | — | — | — | — | `discovery/search_<n>/result.json` |
| P0 | `guideline-seed` | Draft a guideline candidate | not built yet | — | Shown here · read-only · G_00 is created by corpus-contract, not this Run | — | — | `policy/versions/G_00/` |
| P0 | `test-reserve` | Hold back test items | not built yet | Shown here · read-only · setup's held-back count | — | Shown here · read-only · sealed-test status | — | `test/sealed/status.json` |
| P0 | `embedding-build` | Build a map | Start here · Data → Embedding button; explicit human model choice; P0 integrity valid and no HOLD; G0 not required | Start here + Shown here · read-only · Embedding | Shown here · read-only · map groups in Rounds | — | — | `cache/embeddings/<version>/` |
| P1 | `round-prepare` | Draw one round | Start here · Start round 1 after G0 passes; the identified human releases it | — | Start here + Shown here · read-only · Rounds | — | — | `rounds/round_NN/` |
| P1 | `weak-prelabel` | Pre-label one prepared round | not built yet | — | — | — | — | `rounds/round_NN/prelabels/` |
| P1 | `human-calibration` | You label one round | Copy request → paste and send · only for a released open round with items left; first item open starts the Run | — | Shown here · read-only · Rounds; actual Ticket/status is in Runs | — | — | `rounds/round_NN/sessions/events.jsonl` |
| P1 | `guideline-learn` | Draft a guideline from accepted judgments | not built yet | — | Not built · no policy-draft result is produced or shown | — | — | `rounds/round_NN/policy_draft/` |
| P1 | `round-measure` | Measure one completed judgment set | not built yet | — | Not built · no round metrics are produced or shown | — | — | `rounds/round_NN/metrics.json` |
| P1 | `round-close` | Close a measured round | not built yet | — | Not built · no checkpoint or guideline promotion is produced | — | — | `rounds/round_NN/checkpoint.json` |
| P2 | `handoff-freeze` | Freeze a stopped labeling lineage | not built yet | — | — | — | Not built · Handoff result has no writer | `handoff/label-v1.yaml` |
| P3 | `test-gold-lock` | Lock blind answers for the final test | not built yet | — | — | Not built · no final test lock is produced | — | `test/final/lock.json` |
| P3 | `executor-predict` | Have one registered model predict the test | not built yet | — | — | Not built · no predictions are produced | — | `evaluation/predictions/` |
| P3 | `executor-score` | Score one closed set of predictions | not built yet | — | — | Not built · no scorecards are produced | — | `evaluation/scorecards/` |
| P3 | `executor-select` | Select from the complete scorecard set | not built yet | — | — | Not built · no selection is produced | — | `evaluation/summary.md` |
| P4 | `scan-preflight` | Check one frozen production plan | not built yet | — | — | Not built · future Scan view is not in current Quality navigation | — | `production/run_<n>/preflight.json` |
| P4 | `scan-shard` | Label one frozen corpus shard | not built yet | — | — | Not built · future Scan view is not in current Quality navigation | — | `production/run_<n>/` |
| P4 | `risk-route` | Route risky production items to review | not built yet | — | — | Not built · future Scan view is not in current Quality navigation | — | `production/run_<n>/risk_queue.jsonl` |
| P4 | `human-review` | Review one frozen production risk queue | not built yet | — | — | Not built · future Quality/Scan review; not calibration Rounds | — | `production/run_<n>/human_final.jsonl` |
| P4 | `reconcile` | Reconcile reviewed items into a candidate corpus | not built yet | — | — | Not built · candidate result belongs to future Quality/Scan; it is not D* | — | `production/run_<n>/run_report.md` |
| P5 | `audit-sample` | Draw from one frozen audit design | not built yet | — | — | Not built · no audit sample is produced | — | `audit/final_<n>/sample.jsonl` |
| P5 | `audit-human-gold` | Blind-label one audit sample | not built yet | — | — | Not built · Quality/Audit only; not calibration Rounds | — | `audit/final_<n>/human_gold.jsonl` |
| P5 | `audit-analyze` | Analyze one completed audit sample | not built yet | — | — | Not built · no audit receipt is produced | — | `audit/final_<n>/receipt.json` |
| P5 | `dstar-materialize` | Publish an accepted audited corpus | not built yet | — | — | — | Not built · D* requires the later audit path | `corpus/final/D_star.jsonl` |

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
`../../label-building-workflow/haipipe-workbench-labeling/SKILL.md`.

## Projection law

The five Spaces are views over one page-local `labeling/` folder, not storage
folders. A Run is `rlNN_<operation>_<target>`, with its Ticket at
`labeling/runs/<run>.yaml` and its Result at `labeling/results/<run>/`. The 25
operation kinds and the count law are in `ref-run.md`. A round is an episode
that groups Runs. Each item judgment is an event inside the
`rlNN_human-calibration_round-NN` Run, never a Run of its own.
