Labeling workbench: the structure of every View
================================================

The Labeling workbench laid out the way `workbench-design` lays out the Design
workbench: the tree of levels, Spaces and Views first, then each View block by block (what
it reads, what it shows in order, its Run types, who writes), then the files the page reads
and the questions a reader can answer from it. Served by
`servers/workbench-labeling/labeling.py`; the Space roster, Run types and their Views come
from `haipipe-labeling-building/ref/ref-space-mapping.md`.

Each View lists **Today**, the blocks the page shows now, and **To add**, blocks that would
make it more complete. Every block reads a file that already exists on disk or a row of
`ref-space-mapping.md`; none invents a state or claims a gate passed.

Built on 2026-10-03 (0.25.0), on every Page:

1. **A brief at the top of every Space**, above its View tabs: label over value.
   - Data: items · to label · held back · contract · embedding builds.
   - Labeling: meanings (G0) · meaning changes · rounds · open round · labeled · guideline.
   - Quality: held-back test · models scored · audits.
   - Delivery: handoff · production runs · final labels.
2. **Steps in this view** at the end of every View: each Run type the Workflow map (or, for
   Preparation, the Corpus Preparation table) gives the View, in step order, with what it
   writes and its state on this job: `done` or `in progress` with its latest Run, else
   `not built yet` or `not started`. A View whose result does not exist yet now shows its
   steps instead of a blank.
3. **Data › Contract**: *The job* (job, target, question, labels decided by, test kept by,
   created, by Run, contract check) and *Labels* (labels, kind, regions, how sure).
4. **Labeling › Definition**: an undefined in-between case says `not defined yet`, and
   *Meaning history* lists every revision in `gates/meaning-revisions/`.
5. **Labeling › Rounds**: *All rounds* (round, state, labeled, changed after the reveal, how
   drawn, guideline) and *How the final labels fall* (counts per label per round).
6. **Labeling › Guideline**: *Versions* (version, status, from, made by, used by; the current
   one marked).
7. **Jobs** (board level): each card adds Phase, Meanings and Rounds.

The **To add** lists below keep what is still open.


The tree
--------

```text
🏷 Labeling · board level (every labeling job on one Board)          /w/<board>
├── Guide (shared)     Description · Method · RoadMap Draw (Workbench design) · Related Paper
└── Jobs               one card per job, the ones waiting on you first · Pages before Contract

🏷 Labeling · page level (one labeling job)                          /w/<board>/<page>/labeling
├── header             title · all labeling jobs · band: phase · round · guideline · HOLD
├── Guide (shared)     the same four Views as the board level
├── Data               input
│   ├── Preparation    Raw corpus · Items to label (20 at a time) · Corpus Preparation
│   ├── Contract       Data counts · Imported labels · What you see after you lock an answer
│   └── Embedding      Embedding model · From item to vector · Worked example · Map · Groups · Build record
├── Labeling           process
│   ├── Definition     Label definitions · Discussion · Meaning (G0)
│   ├── Rounds         Start round 1 · one box per round: its card and its item table
│   └── Guideline      the current guideline version
├── Quality            checks
│   ├── Test           Held-back test items
│   ├── Evaluation     (blank until evaluation/registry.yaml exists)
│   └── Audit          (blank until audit/final_* exists)
├── Delivery           output
│   ├── Handoff        (blank until handoff/label-v1.yaml exists)
│   ├── Scan           (blank until production/run_* exists)
│   └── Final labels   (blank until corpus/final/D_star.jsonl exists)
├── Runs panel         right of every Space, folded at first; the current View's Run types
└── drawers            ?drawer=workflow (Phases · SOP · Workflow map) · ?drawer=allruns (every Ticket)
```


Board level
-----------

| Space | Reads | Shows | Writes through |
|---|---|---|---|
| Guide | `servers/workbench-labeling/guide/guide.yaml` (with `guide/method.md`, `guide/methods/`); `ref/workbench-table.md`; `servers/workbench-labeling/related/papers.md`; `Tools/designs/b15_theme_labeling/studio/s02-labeling-workbench/labeling-workbench-ui.excalidraw` | Description, Method, RoadMap Draw, Related Paper | none (Guide never saves) |
| Jobs | every Page on the Board through `_board_pages()`; each job through the same view model as the page level | the band (jobs, waiting, next step); "Waiting for you", then "Other jobs": one card each with id, question, badge, Target, Data, Labeler, Next; "Pages before Contract" | none |

**Jobs · To add**: built (Phase, Meanings, Rounds on each card).


Page level · the header
-----------------------

| Block | Today | To add |
|---|---|---|
| Title | the job's question (`config.yaml` construct), the next step as its tooltip | — |
| Link | `all labeling jobs` (Board-backed Pages only) | — |
| Band | phase · round n: x of y labeled · guideline G_nn · HOLD or no HOLD | a phase strip P0 → P5 with G0 marked, from `engine/job.py status()`; it replaces nothing and opens the Workflow drawer |


Data Space · input
------------------

| View | Reads | Run types | Writes through |
|---|---|---|---|
| Preparation | `corpus/source.yaml`, `corpus/manifest.json`, `preparation-owner.yaml`, `preparation-ref.yaml`, the source owner's Corpus Runs | Normalize source · Choose labeling unit · Create candidate items · Check candidate items · Reserve source groups | `haipipe-labeling-preparation` |
| Contract | `config.yaml`, `corpus/manifest.json`, `test/sealed/status.json`, `corpus/imported_label_summary.json` | Set up the job | `/haipipe-labeling` (`job.create_contract`) |
| Embedding | `cache/embeddings/<version>/manifest.json` and its files | Build a map | the door action `build_embedding` |

**Preparation · Today**

1. Before a job: *Page folder needed* (the Page file to create, a copy request), or
   *Corpus Preparation* (attach a source owner, a copy request; then source, owner, Run
   Types finished n of 5, next; then the accepted package: snapshot, recipe, item set,
   partition, development and held-back counts, status, owner).
2. With a job: **Raw corpus** (source, folder, one row is, one item is, raw column → item
   field, the other column names, built), then **Items to label** (one item is, counts,
   text and context fields with word counts, kept together across the held-back test),
   with **Show items**, 20 at a time, each fetch logged as an exposure.

**Preparation · To add**

1. When the job predates source-owned Preparation (no Runs here), one line saying so and
   naming `corpus/source.yaml` as the file that would fill Raw corpus.

**Contract · Today**

1. Before a job: *Labeling Contract* (create the Page folder first, or the accepted package
   and a copy request, or finish Preparation first).
2. With a job: **Data** (source, items, to label, held back, embedding), **Imported labels**
   when an outside rating set came with the corpus, **What you see after you lock an answer**
   (from, vote counts, other fields).

**Contract · To add**: built (*The job*, *Labels*).

**Embedding · Today**

1. **Embedding model**: how many builds, and *Run a new embedding* (model, settings).
2. With a build: **From item to vector** (the pieces), **Worked example** (made up, not a
   corpus item), **Map** (2D or 3D, color by group or label, zoom, pick a dot to see its
   neighbors), **Groups** (k-means; typical items on request, logged), **Build record** (run,
   built, model, folder, files, map, groups, rebuild command).

**Embedding · To add**: nothing; it is the most complete View.


Labeling Space · process
------------------------

| View | Reads | Run types | Writes through |
|---|---|---|---|
| Definition | `config.yaml` labels and meanings, `gates/g0/receipt.json`, `gates/meaning-revisions/`, discussion `results/<run>/ledger.yaml` | Discuss the label meanings (Search outside evidence: not built) | `definition_discussion`; Confirm meaning through `POST /_board/labeling/act` |
| Rounds | `rounds/round_NN/` (card, human batch, events, finals), `corpus/items.jsonl` for items already shown | Draw one round · You label one round (Pre-label, Measure, Close: not built) | the door actions `release_round`, `open_item`, `first`, `final` |
| Guideline | `policy/current`, `policy/versions/<G>/guideline.md` | (Draft a guideline candidate, Draft from judgments: not built) | `gallery-keeper` (not built) |

**Definition · Today**

1. **Label definitions**: question, judge, scope, confirmed (by whom, when); one row per
   label with what it means; *In-between cases* (HL, LN, HN, HLN) with what each means;
   how-sure levels.
2. **Discussion**: per discussion Run, each label before and after, and what is still open.
3. **Meaning** (G0): confirmed ✓ with who and when, or the Confirm form, or *Define label
   meanings first*, *Meaning discussion open*, *Restore G0 receipt*, or the HOLD reason.

**Definition · To add**: built (`not defined yet`, *Meaning history*).

**Rounds · Today**

1. With no open round: *Start round 1* (batch size, Start), through the door.
2. One box per round, newest open: its card (state, started by and when, how drawn, each
   item's chance, guideline), then **The items this round drew**: #, item, text (only items
   already shown), group, state, feedback.

**Rounds · To add**: built (*All rounds*, *How the final labels fall*); a per-region count
is still open.

**Guideline · Today**

1. **Guideline G_nn**: `guideline.md` rendered (question, classes, regions, uncertainty).

**Guideline · To add**: built (*Versions*); a diff between versions is still open.


Quality Space · checks
----------------------

| View | Reads | Run types | Writes through |
|---|---|---|---|
| Test | `test/sealed/status.json`, `test/final/lock.json` | (Hold back test items, Lock blind answers: not built) | the fence at Contract; `gallery-keeper` (not built) |
| Evaluation | `evaluation/registry.yaml`, `evaluation/predictions/`, `evaluation/scorecards/`, `evaluation/summary.md` | (Predict, Score, Select: not built) | `labeler-panel`, `validator` (not built) |
| Audit | `audit/final_<n>/` | (Draw, Blind-label, Analyze: not built) | `sampler`, `validator` (not built) |

**Test · Today**: **Held-back test items** (items, how drawn, keeper, state, locked for scoring).

**Evaluation · Today**: blank until `evaluation/registry.yaml` exists, then one row, registry present.

**Audit · Today**: blank until an audit exists, then the number of audits.

**Quality · To add**

1. Built as *Steps in this view* on every View.
2. Evaluation, once it exists: one row per scored model (metric values from
   `evaluation/scorecards/`), the selected one marked from `summary.md`.


Delivery Space · output
-----------------------

| View | Reads | Run types | Writes through |
|---|---|---|---|
| Handoff | `handoff/label-v1.yaml` | (Freeze a stopped labeling lineage: not built) | `gallery-keeper` (not built) |
| Scan | `production/run_<n>/` | (Check plan, Label shard, Route risky items, You label the risk queue, Reconcile: not built) | `labeler-panel`, `classifier`, `moderator` (not built) |
| Final labels | `corpus/final/D_star.jsonl` | (Publish an accepted audited corpus: not built) | `gallery-keeper` (not built) |

**Today**: each View is blank until its file exists; then one row (handoff status, number
of production runs, D* materialized).

**Delivery · To add**: built as *Steps in this view*.


The Runs panel and the drawers
------------------------------

| Part | Today | To add |
|---|---|---|
| Runs panel | the shared panel, folded at first; only Run types that can run now, or have run on this job; a View with none says `No runs yet.` | list every Run type of the View, the unbuilt ones greyed `not built yet` with count 0, as the Task workbench does |
| `?drawer=workflow` | Phases (P0-P5), SOP, Workflow map; no button opens it | open it from the phase strip in the band |
| `?drawer=allruns` | one row per Ticket; no button opens it | open it from the Runs panel's header |


What the page reads
-------------------

```text
config.yaml                              question, labels, meanings, regions, reveal, rounds
corpus/source.yaml · manifest.json       raw folder, items, counts
corpus/items.jsonl                       item text, only for items already shown (Rounds) or fetched on request
corpus/imported_label_summary.json       an outside rating set's counts
preparation-owner.yaml · preparation-ref.yaml   the source owner and the accepted package
test/sealed/status.json · test/final/lock.json  the held-back test
gates/p0-contract/ · gates/g0/ · gates/meaning-revisions/   Contract, meaning confirmation, its history
cache/embeddings/<version>/              builds, map, groups
rounds/round_NN/                         card, human batch, events, finals, feedback
policy/current · policy/versions/<G>/    the guideline
evaluation/ · audit/ · handoff/ · production/ · corpus/final/   later phases
../runs/*.yaml · ../results/*/            Tickets and Results beside labeling/
```

It never renders item text outside Rounds, sealed ids, or private judgments, and it never
treats an observed file as a passed gate.


Reader contract
---------------

From one tab, without opening a file, a reader can answer:

| Question | Where | Today |
|---|---|---|
| Where does this job stand, and what is next? | band, title tooltip | partly: no phase strip |
| What is the corpus, what is one item, and what is held back? | Data › Preparation, Contract | yes |
| Who decides the labels, and who keeps the held-back test? | Data › Contract | not shown (To add 1) |
| What does each label mean, who confirmed it, and how has it changed? | Labeling › Definition | yes, except the history |
| How far has labeling got across all rounds, and how do the labels fall? | Labeling › Rounds | one round at a time only |
| Which guideline version is current, and which rounds used which? | Labeling › Guideline | current version only |
| What must happen before models can be checked, scanned and delivered? | Quality, Delivery | no: those Views are blank |
| Which Runs exist, which Run types are still to come? | Runs panel, `?drawer=allruns` | partly: unbuilt types hidden, drawer has no button |


Minimal by rule
---------------

Two earlier rules shape what is shown. A View exists only because Runs live in it
(260928): every View has Run types, so no View was added. The page shows content and the
controls that act on it, never hints or explanation sentences (260927): each block is read
from a file or the Workflow map, not written as help text. The one change to an earlier
rule: a View whose result does not exist yet was left blank (260927, "no placeholder
lines"); since 2026-10-03, asked for directly ("show the details of each space and each
view"), it shows its *Steps in this view* instead, which are real Run types and their state.
