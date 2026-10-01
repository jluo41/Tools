# InsightBoard resource and citation laws

Read when scaffolding a board, answering a question, writing a report, or
settling a register.

## One dataset, one board, one folder (JL 261001)

An InsightBoard reads exactly one prepared extract. It lives in the Project's
`insights/` world, one folder per dataset:

```text
<Project>/insights/<Dataset>-InsightBoard/      e.g. DatasetA-InsightBoard · DatasetB-InsightBoard
```

```text
a new source extract        ──▶ a NEW InsightBoard folder in insights/
a new question              ──▶ a new register row INSIDE the board
a subgroup of the extract   ──▶ a PARTITION inside the board, never a board
a subgroup + SPLIT verdict  ──▶ MAY become a child board · the verdict is its birth
                                certificate, necessary and not sufficient: the child
                                still needs its own consumer (partition.md)
```

Re-extracting a subgroup's rows into their own parquet does not make them "a
new source extract": a new extract is new SCOPE (rows or fields the old one did
not carry), never the same rows re-cut. The child-board path always runs
through the SPLIT verdict, and a re-extract cannot launder around it.

The code that answers questions is NOT in the board. It lives in the
Project's `tasks/` world, shared by every dataset (one DIKW Block, below): the
engine. The board is the dataset wrapper: it owns its questions, and each
answering page folder is also a task folder holding the page, the tickets that
call the engine, and their results.

## The three columns · Logic, Work, Report

Every answer is read in three parts, which are also the three things a board
holds (the Insight workbench draws them as three columns):

```text
LOGIC    the question       MT01–MT04 register rows       what is asked, why, its evidence needs
WORK     the runs           <page>/runs/ + <page>/results/   what was computed, on which cut
                            <page>/answers.yaml              which file answers which need
REPORT   what it says       <page>/<page>.md               the answer in words, each need cited
```

The three meet at the evidence need, `<QID>.E<n>` (`evidence-needs.md`): the
register lists it before any run, `answers.yaml` binds it to the narrowest
result files whose fields carry its `pass:`, and the page cites it. Three
grains (one ask, a run with many groupings, a page with several questions)
line up only at that id.

A page rests on the runs its own tickets call (`ref/report.md`):

```bash
# 2-alpha/I02-alpha-<slug>/runs/run_b5Nj21t02r02_alpha_contrast.sh
PAGE="$(cd "$(dirname "$0")/.." && pwd)"
export RUN_TICKET="${PAGE}/runs/$(basename "$0")"
export RESULT_DIR="${PAGE}/results/$(basename "$0" .sh)"
exec "${PAGE}/../../../../tasks/b5N_<topic>_dikw/j21_information_<topic>/t02_contrast/runs/r02_<dataset>_alpha.sh"
```

The task config the ticket runs names the extract, the cut and the questions:

```yaml
# tasks/b5N_<topic>_dikw/j21_information_<topic>/t01_rates/scripts/config/r02_<dataset>_alpha.yaml
input:      {parquet_path: _WorkSpace/7-AgentStore/…/<dataset>/…parquet}   # the board's ONE extract
population: {name: alpha, where: [{column: <column>, eq: <value>}]}
answers:    [QI1, QI2, QI3, QI4, QI5, QI6]        # derived from the pages' answers.yaml; a cross-check
```

The task config never names a board or a result folder: the page ticket
decides where the result lands (`results/<ticket name>/` in the page folder),
and `runtime.yaml` records both the page ticket and the task ticket. The page
ticket says which run a page rests on; `answers.yaml` says which of its files
answers which need. `answers:` only cross-checks that the called run serves
the questions its pages bind.

## The Climb Law · each level rests on the level below

Authority to conclude lifts one level at a time. Each level's answer cites
named results below it:

```text
① MT00       the board's ONE extract and its partitions · set at scaffold
② Data         a run observes exact sources            its results ARE the answer · the page says what was observed
③ Information  a run derives rates and contrasts        its results ARE the answer · the report says what they show
④ Knowledge    a report claims from named results      strength · rivals · boundary
⑤ Wisdom       a page counsels from named reports      contextual · verdict-conditioned
⑥ Handoff      exports Wisdom, signed ✋                never re-derives · the ONLY bindable level
```

- Data and Information are computations: a task run answers them, and the
  run's `results/<run>/` (receipt, tables, metrics, QA note) is the evidence.
- A Knowledge answer is a report (`ref/report.md`) whose `runs:` header names
  every run it read, and whose body cites them by result file and need. Every
  test its ask or its rivals name is a compute need with a run of its own.
- A Wisdom answer stays a Page Folder, because it carries the person-signed
  Design Handoff a DesignBoard binds by path. Its counsel cites Knowledge
  reports by question id.

Level-skipping is a CHECK routing failure, with exactly two exceptions, both
inside the cross group: the contrast Information answer derives from MIRRORED
Information results of each partition (I-from-I), and the pooling verdict
cites the heterogeneity Knowledge report (K-from-K), because its subject is a
claim about claims.

The pre-climbed external-parent bridge is not a third skip: the selected Task
Insight `riNN` item's accepted Result CHECK-closes the complete
`D→I→K→W→RF` chain. Its packet carries the RI execution id, the base-R pointer,
dataset binding, Result path, and RF id; a bare `rNN` cannot identify the
rebound data execution. Historical items-v1 `#rNN@vNNN` packets remain
readable under their recorded contract. Open sibling items do not invalidate
that Result. GI4 verifies that authority before local Wisdom performs the new
InsightBoard-contextual operation; see `haipipe-insight-workflow`.

## The two births of a question

```text
need-first        a Brief raises the need OUT; it lands on the rung register it faces,
                  carrying the Brief's need id, and G4 later checks the round trip
curiosity-first   a reader of the inventory becomes curious; the register row names the
                  raiser and no consumer, because data may land before anyone knows its use
```

Either way the question is written ONCE, on the one register facing its rung
(QD/QI/QK/QW ids), with target, raiser, what-would-answer and a state cell, and
an optional **Expected** line written before any run exists (the board's
hypothesis; `haipipe-insight-question`). Its derived Question Group is
`partition × target rung`: `QI3` under alpha belongs to `QG-alpha-I`,
while the same `QI3` under full belongs to `QG-full-I`. The id is never duplicated or
partition-suffixed (`QK1` spans all eligible partitions; there is no `QK1-alpha`).
`question-groups.md` owns membership, cross routing, state, and sorting.

## The three pens · who may write what

The workflow coordinates Runs and control actions; this door states the pens,
and they never cross:

```text
register     writes STATE, never a finding         MT01-MT04 cells, including the
                                                   ⬜ annotations (`⬜ calc`) — notes
                                                   about work ARE state · haipipe-insight-question's
                                                   vocabulary · ✅/🚫/🟡-final settle
page         writes FINDINGS, never its own cell   the answering page's .md, written by the
                                                   level's folder skill from its own results
handoff      EXPORTS, never re-derives             the Wisdom page's signed division
```

A run's results are generated, never written by a pen: a run writes them and a
rerun replaces them. The join is a round trip through one question id: the
register cell cites the answering page (`✅ <L><NN>-<partition>`), and the page's state line
names the register's id back (`answers QI2`).
`board.md`'s spine and close are DERIVED HEADERS of the same record: the
registers are authoritative, a header that disagrees with them is stale, and
reconciling it is register-pen work. Final settlement is recorded in the
register at GI6, so a Design page reads a signed handoff and never a Data,
Information or Knowledge answer directly; two consumers can never keep
separate books.

## The board, concretely

```text
insights/<Dataset>-InsightBoard/              Block: one extract
├── board.md                    spine · close · extract (no store: results live in pages)
├── 0-MT-meta/
│   ├── MT00-meta/              the ONE extract · partitions (one config name per cut) · thresholds
│   └── MT01-MT04/              the four registers: Queue grid + one division per question
├── <n>-<partition>/                         Job: one partition (1-full, 2-<partition>, …, 9-cross)
│   └── <L><NN>-<partition>-<slug>/          Task: one answering page (id <L><NN>-<partition>)
│       ├── <L><NN>-<partition>-<slug>.md    REPORT · the page says what its results show
│       ├── answers.yaml                      WORK · each evidence need → its result files
│       ├── runs/run_bNNjNNtNNrNN_<partition>_<task>.sh   WORK · calls a task run
│       └── results/<ticket>/                 WORK · generated, light: tables, figures, receipt
└── board/                      the built site, generated
```

- `results/` holds only light output: receipts, aggregate tables, metrics and
  the run's `fig_*.png`. A file over 10 MB, a model or a row-level table goes to
  `_WorkSpace/ProjectResult/<Project>/<page path>/results/<ticket>/` with a
  `heavy.yaml` pointer in the result (AGENTS.md rule 10).
- Every result is aggregate. No row-level patient value is ever written to a
  board.
- A result is generated: never edited by hand. Rerun its ticket.

## The DIKW Block in tasks/

The code a board runs lives in one Block of the Project's `tasks/` world, in
the auxiliary range (`haipipe-task` § Block number ranges), with Jobs grouped
by level so the Work column reads in the same order as the questions:

```text
tasks/b5N_<topic>_dikw/          board.md (board-kind: task-block) · src/ shared by every Job
├── j1N_data_<topic>/            Data: extract shape, catalogs, balance checks
├── j2N_information_<topic>/     Information: rates, crossings, features
├── j3N_knowledge_<topic>/       Knowledge computations (heterogeneity, prediction), when any
└── j4N_wisdom_<topic>/          Wisdom computations, when any
```

A range with no work has no Job. A new dataset or a new partition is a new
config and run in an existing Task, never a new Task. Every worker ends with a
Look step (a shared `src/` figures helper in the DIKW Block) that draws the run's tables
into `fig_*.png` beside them.

## Folder owners

```text
MT00        haipipe-insight-meta          what data EXISTS · one per board
MT01-MT04   haipipe-insight-question      what is ASKED of one rung · four per board
Data        haipipe-insight-data          a run observes · its report, when written
Information haipipe-insight-information   a run derives · its report says what it shows
Knowledge   haipipe-insight-knowledge     a report claims from named results · never advises
Wisdom      haipipe-insight-wisdom        counsel page + the signed Design Handoff
```

These are resource contracts. Each named skill owns its level's report or
page contract, closure and handoff. They live under `folder-kinds/`. Actual
work selects the Run Specs defined by the controller; a folder kind never
creates a Run identity. Legacy `page-type:` keys resolve to these owners.

## Boards made before page tickets

A board scaffolded before 261001 keeps its results in
`_WorkSpace/InsightBoardResult/<board>/` and its pages cite them there. Such
boards sit in `insights/_old/<board>/` (they lived in `applications/`, which is
retired; `haipipe-project`). Rebuilding one is: write each
answering page's tickets, rerun them, check the tables against the old store,
then rewrite each page's citations to its own `results/` and embed its
figures. Signed Wisdom pages are not edited. `migration.md` in
`haipipe-insight-workflow` owns the move of such a board into `insights/`.
