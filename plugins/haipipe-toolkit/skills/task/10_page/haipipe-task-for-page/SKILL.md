---
name: haipipe-task-for-page
description: >-
  Task-type specialist for a PAGE-SERVING execution job: one job per Board
  Page that produces reusable Supporting Run Results for typed Evidence Items.
  It reads upstream task folders, computes or extracts owed values into
  values.yaml + QA digests, and proposes the upstream task when a value has no
  source yet. Called by /haipipe-task when task-type=page; its Results are
  selected by SURVEY and consumed by LAND. Trigger: page
  collection job, collect the values, serve the page's cards, values.yaml,
  propose the missing task, task-type page, /haipipe-task-for-page.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.3.4"
  last_updated: "2026-09-04"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-task-for-page · one job answers one page's numbers with code

Load `haipipe-task` first (the hierarchy, the four phases, the QA door); this
file owns the delta for `task-type: page`. The consumer side is a typed row in
`outline/<stem>-evidence-items.md`; SURVEY maps this job's full Run id as a
Supporting Run and LAND consumes its Result. This job never edits the Page,
because it stands on the executor side of the wall.

## ⚡ Brief

```text
Q        every number this page needs: computed by execution, from named
         upstream runs, re-runnable — and every number with no source yet:
         proposed as the task that would produce it
READS    a frozen consumer-neutral input batch (expected payload + acceptance,
         with Page claims removed) · upstream task folders' report.yaml ·
         results/ · QA/
WRITES   its own job only: plan.yaml · scripts/<collector>.py ·
         scripts/config/rNN · $OUTPUT_ROOT/results/<task>/<run>/values.yaml · QA/<n>-<slug>.md ·
         workflow/proposals.md
NEVER    a consumer/ file or any stake · the page or its outline/ · a sibling
         job's folder · a value it computed nowhere (GATE-3: a name that does
         not resolve must raise)
EXITS    Report: every question answered in values.yaml + QA, or carried as
         an owed row with its proposal
```

## 🧱 One job per page, linked where the page already looks

```text
project or Application                          any Folder's Page Face
tasks/                                           <page>/
└── b<NN>_page_service/         one service      ├── outline/<stem>-evidence-items.md
    ├── j01_values_<pageA>/     block per project│     E<NN>-VALUE-<slug> · Supporting Runs
    │   ├── t01_collect_values/                  ├── runs/pj<JJ>t<EE>r<RR>.sh
    │   │   ├── t01_collect_values.md            └── results/pj<JJ>t<EE>r<RR>/
    │   │   ├── scripts/
    │   │   │   ├── collect_values.py
    │   │   │   └── config/r01_<batch>.yaml
    │   │   └── runs/r01_<batch>.sh
    │   ├── workflow/  plan.yaml · report.yaml · proposals.md
    │   ├── results/t01_collect_values/r01_<batch>/values.yaml
    │   └── QA/1-<slug>.md …
    └── j02_values_<pageB>/
```

- **The Evidence Item is not copied here.** Its `E<NN>-VALUE-<slug>` id stays
  Page-local. This task-side executor produces a consumer-neutral Result; the
  Page maps its full `b<NN>j<NN>t<NN>r<NN>` address under Supporting Runs and
  the Local Page Run selects the needed `values.yaml` rows.
- **One job per Page Face, one service block per project**; three served Pages
  hold three sibling jobs, whether their owning Folder belongs to Paper,
  Application, or another Board family. The canonical stranger-test names are
  `b<NN>_page_service` and `j<NN>_values_<page-stem>`. A project with an
  established compatible service block may reuse it; legacy
  `b<NN>_paper_service` remains readable but is never required for non-Paper
  work. A run config is one batch (`r01_<batch>.yaml`), and a refresh is a new
  run of the same ticket, never a new Folder.
- **The Page links Results, not a whole Folder copy.** SURVEY records the
  exact Supporting Run id; Context Workspace may separately list the related
  Task Page when it helps a reader. There is no PageX, `task/`, or Probe lane.

## 🚪 How work arrives · the same doors, never a new one

```text
SURVEY       selects this existing/needed Execution Run as a Supporting route
executor     for each neutral question: /haipipe-task qa "<question>" <this job>
             gate ① existing QA answer → path · ② results/ hold it → digest ·
             ③ neither → ENTER the lifecycle HERE: extend the collection
             script, rerun the ticket, complete the QA file at Report
LAND         validates the Supporting Result, freezes it into Local Input, and
             executes the Page-local Evidence Item Run; changed values reopen EMBED
```

A phase producer still never calls this specialist directly, and this job
never learns which page sentence wants which answer: it sees stripped
questions and serves `values.yaml` rows to whoever binds them.

## 📐 values.yaml · the machine-readable half of the answer

One file per Run under resolved `$OUTPUT_ROOT`, beside the Run's other Results;
the QA digest cites it.
Every row resolves or is `owed` — a computed row with an unresolvable
`source:` raises at run time, never defaults.

```yaml
# $OUTPUT_ROOT/results/t01_collect_values/r01_intro_batch/values.yaml
computed: "260831 1710"
upstream:                            # every folder this run read, pinned
  - examples/ProjB/tasks/R01_Reg_TraitOpioid · report.yaml 260828
values:
  - id: adjusted-effect              # consumer-neutral Result key
    question: 2-agreeableness-effect # QA/2-agreeableness-effect.md
    value: "-0.083"
    unit: "SD opioid days per SD agreeableness"
    source: "R01_Reg_TraitOpioid/results/j02_reg_pain/r01_baseline/coef_table.csv#agreeable.b"
    state: landed
  - id: review-coverage
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
diff against the previous run's copy names every drifted value → each mapped
Evidence Item is a stale binding EVIDENCE re-lands and OUTLINE absorbs
(`v<N+1>` if the plan was ✅). The page never goes stale silently, because the
join from sentence to lane to card to values row to upstream run is walkable
in both directions.

## 🔄 The four phases, specialized

```text
Plan     workflow/plan.yaml: input = the batch's questions + the upstream
         folders each should read; process = extract | compute | join;
         output = values.yaml rows + QA files. IPO schema:
         task/haipipe-workflow/ref/plan-schema.md
Build    scripts/collect_values.py + scripts/config/r<NN>_<batch>.yaml: one entry per
         question (id, upstream path, extraction); CODE_REVIEW.md Gate 1
Execute  bash runs/r<NN>_<batch>.sh with `TASK_NAME="collect_values"`,
         family `Execution`, operation `collect-page-values`, target `<batch>`, and
         `REQUIRED_RESULTS=("values.yaml")`
         `RUN_INPUTS` pins every upstream Result path/hash named by the batch.
         → values.yaml + per-question artifacts
         The generic Run scaffolder writes the complete `status: planned`
         runtime receipt before this Ticket may launch.
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
anatomy this job writes). The Page-side contracts it serves but never edits are
`haipipe-page-outline`, `haipipe-page-evidence`, and
`haipipe-plugin-outline/ref/item-table.md`.
