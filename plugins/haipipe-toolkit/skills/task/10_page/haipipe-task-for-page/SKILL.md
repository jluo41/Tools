---
name: haipipe-task-for-page
description: >-
  Task-type specialist for a PAGE-SERVING collection job: one job per Board
  Page that answers the page's task-route probe cards with CODE — it reads
  upstream task folders, computes or extracts every owed value into
  values.yaml + QA digests, and PROPOSES the upstream task when the value has
  no source yet. Called by /haipipe-task when task-type=page; dispatched
  through the probe crossing, never directly by a phase. Trigger: page
  collection job, collect the values, serve the page's cards, values.yaml,
  propose the missing task, task-type page, /haipipe-task-for-page.
argument-hint: "[page-path] [--job <job-path>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.1.0"
  last_updated: "2026-08-31"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-task-for-page · one job answers one page's numbers with code

Load `haipipe-task` first (the hierarchy, the four phases, the QA door); this
file owns the delta for `task-type: page`. The page side of the crossing is
`board/page-plugins/haipipe-plugin-probe` (the card) and
`board/page-workflows/haipipe-page-evidence` (the binding); this job never
loads either, because it stands on the executor side of the wall.

## ⚡ Brief

```text
Q        every number this page promises: computed by code, from named
         upstream runs, re-runnable — and every number with no source yet:
         proposed as the task that would produce it
READS    the page's stripped executor questions (executor/q-executor.md,
         handed in the dispatch batch) · upstream task folders' report.yaml ·
         results/ · QA/
WRITES   its own job only: plan.yaml · the collection script · config/rNN ·
         results/<task>/<run>/values.yaml · QA/<n>-<slug>.md ·
         workflow/proposals.md
NEVER    a consumer/ file or any stake · the page or its outline/ · a sibling
         job's folder · a value it computed nowhere (GATE-3: a name that does
         not resolve must raise)
EXITS    Report: every question answered in values.yaml + QA, or carried as
         an owed row with its proposal
```

## 🧱 One job per page, linked where the page already looks

```text
paper project                                    the page
tasks/                                           <page>/
└── b<NN>_paper_service/        one block per    ├── probe/PP<NN>-<slug>/   the ADDRESS stays here:
    ├── j01_values_<pageA>/     paper's pages    │     card.md · executor/ · proof/
    │   ├── t01_collect_values/                  │     ## Values → PP<NN>.v<n>
    │   │   ├── t01_collect_values.py            └── task/<stem>.md         this job's path,
    │   │   ├── t01_collect_values.md                  ranked FIRST (plugin-task lane)
    │   │   ├── config/r01_<batch>.yaml
    │   │   └── runs/r01_<batch>.sh
    │   ├── workflow/  plan.yaml · report.yaml · proposals.md
    │   ├── results/t01_collect_values/r01_<batch>/values.yaml
    │   └── QA/1-<slug>.md …
    └── j02_values_<pageB>/
```

- **The card is not replaced.** `PP<NN>.v<n>` stays the page-side address for
  every value (`haipipe-plugin/ref/roster.md`: a number filed a second time is
  one thing filed twice). This job is the task-side EXECUTOR that answers a
  whole page's task-route cards in one place; EVIDENCE ④ POINT binds each
  card's `target:` to this job's QA file and pulls its value rows from
  `values.yaml`.
- **One job per page, one block per paper's service jobs**; a paper with three
  drafted pages holds three sibling jobs. The block and job names pass the
  stranger test (`b<NN>_paper_service`, `j<NN>_values_<page-stem>`); a run
  config is one BATCH of questions (`r01_<batch>.yaml`), and a refresh is a
  new run of the same ticket, never a new folder.
- **The page links the job in its `task/` lane** (`<page>/task/<stem>.md`,
  `haipipe-plugin-task`), ranked first; the 🗂 tab then shows the job's
  planned/reported state beside the page.

## 🚪 How work arrives · the same doors, never a new one

```text
② PROBE      raises cards, MATCHes, and hands the batch out through
             haipipe-probe-q-executor-agent — the ONE door (JL 260820)
executor     for each task-route question: /haipipe-task qa "<question>" <this job>
             gate ① existing QA answer → path · ② results/ hold it → digest ·
             ③ neither → ENTER the lifecycle HERE: extend the collection
             script, rerun the ticket, complete the QA file at Report
③ EVIDENCE   binds card target: → the QA path · allocates PP<NN>.v<n> from
             values.yaml · a changed value reopens OUTLINE
```

A phase producer still never calls this specialist directly, and this job
never learns which page sentence wants which answer: it sees stripped
questions and serves `values.yaml` rows to whoever binds them.

## 📐 values.yaml · the machine-readable half of the answer

One file per run, beside the run's other results; the QA digest cites it.
Every row resolves or is `owed` — a computed row with an unresolvable
`source:` raises at run time, never defaults.

```yaml
# results/t01_collect_values/r01_intro_batch/values.yaml
computed: "260831 1710"
upstream:                            # every folder this run read, pinned
  - examples/ProjB/tasks/R01_Reg_TraitOpioid · report.yaml 260828
values:
  - id: PP03.v1                      # the page-side address, given in the batch
    question: 2-agreeableness-effect # QA/2-agreeableness-effect.md
    value: "-0.083"
    unit: "SD opioid days per SD agreeableness"
    source: "R01_Reg_TraitOpioid/results/j02_reg_pain/r01_baseline/coef_table.csv#agreeable.b"
    state: landed
  - id: PP05.v1
    question: 3-review-coverage
    state: owed                      # no upstream produces it yet
    proposal: workflow/proposals.md#P2
```

## 🕳 The propose half · a missing value becomes a named task, not a guess

- **A question no upstream folder can answer is never computed around**: the
  row lands `state: owed`, its QA file lands `state: answered` with a body
  stating the absence and pointing at the proposal (`fn/qa.md`'s state set is
  frozen; `concern` is the page-side CARD's word, never a QA file's — the
  refresh writes the superseding QA file when the upstream lands), and one
  proposal record is appended to `workflow/proposals.md`.
- **A proposal names the MEASUREMENT and its home**: `### P<n> · <headline>`,
  then `Block:` `Job:` `Task:` (stranger-test names), `Produces:` (the exact
  file and field the owed row would bind), `Needs:` (inputs that exist today).
  It never states the hoped direction or size of the result.
- **This job scaffolds nothing outside itself**: a job never reaches into a
  sibling job, so the proposal is executed by a person or by
  `haipipe-task-orchestrator-agent` against the OWNING block, and the next
  refresh run flips the row to `landed` when the upstream appears.

## 🔒 The wall, restated for code

The stake stays behind `consumer/`, which this job never receives. Code has
one stake-leak of its own: a collection script that checks the answer against
the hoped value ("assert b < 0") is the leak in executable form. The script
asserts RESOLUTION (the file, the row, the field exist: GATE-3) and never
DIRECTION; direction belongs to the page's prose after EVIDENCE lands.

## 🔁 A rerun is the refresh, and staleness is mechanical

Upstream reran → rerun this job's ticket → `values.yaml` regenerates whole →
diff against the previous run's copy names every drifted value → each drifted
`PP<NN>.v<n>` is a stale binding EVIDENCE re-lands and OUTLINE absorbs
(`v<N+1>` if the plan was ✅). The page never goes stale silently, because the
join from sentence to lane to card to values row to upstream run is walkable
in both directions.

## 🔄 The four phases, specialized

```text
Plan     workflow/plan.yaml: input = the batch's questions + the upstream
         folders each should read; process = extract | compute | join;
         output = values.yaml rows + QA files. IPO schema:
         task/haipipe-workflow/ref/plan-schema.md
Build    t01_collect_values.py + config/r<NN>_<batch>.yaml: one entry per
         question (id, upstream path, extraction); CODE_REVIEW.md Gate 1
Execute  bash runs/r<NN>_<batch>.sh → values.yaml + per-question artifacts
Report   report.yaml mirrors plan · RUN_AUDIT.md Gate 2 · QA/<n>-<slug>.md
         completed per answered question · proposals.md rows for the owed
```

## 📂 Files

```text
haipipe-task-for-page/
├── SKILL.md                     this specialist
├── ref/specimen-page-values.md  one worked job, frozen (illustrative numbers)
└── CHANGELOG.md                 version history
```

The base is `haipipe-task` (hierarchy, phases, `fn/qa.md` for the QA-file
anatomy this job writes). The page-side contracts it serves but never loads:
`haipipe-plugin-probe` (the card and the wall), `haipipe-page-evidence`
(the binding), `haipipe-plugin-task` (the lane the page links this job in).
The design record is QPf13 (task lane) on `BoardSkillBoard-260722`.
