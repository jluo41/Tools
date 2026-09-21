---
name: haipipe-task-for-page
description: >-
  Task-type specialist for a PAGE-SERVING execution job: one job per Board
  Page that produces reusable Supporting Run Results for typed Evidence Items.
  It reads upstream task folders, computes or extracts owed values into
  values.yaml + Result receipts, and proposes the upstream task when a value has no
  source yet. Called by /haipipe-task when task-type=page; its Results are
  selected by SURVEY and consumed by LAND. Trigger: page
  collection job, collect the values, serve the page's cards, values.yaml,
  propose the missing task, task-type page, /haipipe-task-for-page. Also
  owns the one-subagent-per-Page reorganization job that moves a Discovery
  Page into one Content division per Run. Trigger: one division per run,
  reorganize the pages by run, each run one division.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.4.0"
  last_updated: "2026-09-19"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-task-for-page · one job answers one page's numbers with code

Load `haipipe-task` first (the hierarchy, the four lifecycle commands, and Run/Result law); this
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
         results/ · workflow/report.yaml
WRITES   its own job only: plan.yaml · scripts/<collector>.py ·
         scripts/config/rNN · $OUTPUT_ROOT/<task>/results/<run>/values.yaml · runtime/report receipts ·
         workflow/proposals.md
NEVER    a consumer/ file or any stake · the page or its outline/ · a sibling
         job's folder · a value it computed nowhere (GATE-3: a name that does
         not resolve must raise)
EXITS    Report: every question answered in values.yaml + its Run/Result receipt, or carried as
         an owed row with its proposal
```

## 🧱 One job per page, linked where the page already looks

```text
project or owning family                          any Folder's Page Face
tasks/                                           <page>/
└── b<NN>_page_service/         one service      ├── outline/<stem>-evidence-items.md
    ├── j01_values_<pageA>/     block per project│     E<NN>-VALUE-<slug> · Supporting Runs
    │   ├── t01_collect_values/                  ├── runs/<owner-native-Run-Ticket>
    │   │   ├── t01_collect_values.md            └── results/<owner-native-Run>/
    │   │   ├── scripts/
    │   │   │   ├── collect_values.py
    │   │   │   └── config/r01_<batch>.yaml
    │   │   ├── runs/r01_<batch>.sh
    │   │   └── workflow/  plan.yaml · report.yaml · proposals.md
    │   └── [OUTPUT_ROOT]/t01_collect_values/results/r01_<batch>/values.yaml
    └── j02_values_<pageB>/
```

`[OUTPUT_ROOT]` denotes the generated projection after output-root resolution; it is not a literal directory to scaffold.
The consumer-side Ticket/Result labels above are owned by that consumer and are never allocated by this Task.

- **The Evidence Item is not copied here.** Its `E<NN>-VALUE-<slug>` id stays
  Page-local. This task-side executor produces a consumer-neutral Result; the
  Page maps its full `b<NN>j<NN>t<NN>r<NN>` address under Supporting Runs and
  the Local Page Run selects the needed `values.yaml` rows.
- **One job per Page Face, one service block per project**; three served Pages
  hold three sibling jobs, whether their owning Folder belongs to Paper,
  Insight, Design, or another Board family. The canonical stranger-test names are
  `b<NN>_page_service` and `j<NN>_values_<page-stem>`. A project with an
  established compatible service block may reuse it; legacy
  `b<NN>_paper_service` remains readable but is never required for non-Paper
  work. A run config is one batch (`r01_<batch>.yaml`), and a refresh allocates a new
  rNN config/Ticket pair using the same worker, never a new Folder.
- **The Page links Results, not a whole Folder copy.** SURVEY records the
  exact Supporting Run id; Context Workspace may separately list the related
  Task Page when it helps a reader. There is no PageX, `task/`, or Probe lane.

## 🚪 How work arrives · the same doors, never a new one

```text
SURVEY       selects this existing/needed Execution Run as a Supporting route
executor     for each neutral question: reuse a Run/Result or open a new Run
             at the shallowest depth; execute the ticket and publish its Result
LAND         validates the Supporting Result, freezes it into Local Input, and
             executes the Page-local Evidence Item Run; changed values reopen EMBED
```

An owning controller/producer still never calls this specialist directly, and this job
never learns which page sentence wants which answer: it sees stripped
questions and serves `values.yaml` rows to whoever binds them.

## 📐 values.yaml · the machine-readable half of the answer

One file per Run under resolved `$OUTPUT_ROOT`, beside the Run's other Results;
the Result receipt cites it.
Every row resolves or is `owed` — a computed row with an unresolvable
`source:` raises at run time, never defaults.

```yaml
# $OUTPUT_ROOT/t01_collect_values/results/r01_intro_batch/values.yaml
computed: "260831 1710"
upstream:                            # every folder this run read, pinned
  - examples/ProjB/tasks/R01_Reg_TraitOpioid · report.yaml 260828
values:
  - id: adjusted-effect              # consumer-neutral Result key
    question: 2-agreeableness-effect # the Page Evidence Item's question
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
  row lands `state: owed`, records the missing input and one proposal in
  `workflow/proposals.md`, and waits for a new Supporting Run. No separate
  question ticket or digest is created.
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

Upstream reran → allocate a new rNN config/Ticket using this job's worker → `values.yaml` regenerates whole →
diff against the previous run's copy names every drifted value → each mapped
Evidence Item is a stale binding EVIDENCE re-lands and OUTLINE absorbs
(`v<N+1>` if the plan was ✅). The page never goes stale silently, because the
join from sentence to lane to card to values row to upstream run is walkable
in both directions.

## 🔄 The four lifecycle commands, specialized

```text
Plan     workflow/plan.yaml: input = the batch's questions + the upstream
         folders each should read; process = extract | compute | join;
         output = values.yaml rows + Result receipts. IPO schema:
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
Report   report.yaml mirrors plan · RUN_AUDIT.md Gate 2 · Result receipts
         for answered questions · proposals.md rows for the owed
```

## 🧩 Reorganize a Discovery Page into one division per Run

This separate mode is entered only when the user explicitly asks to reorganize Discovery Pages; ordinary value collection never triggers it.
Load the current Discovery owner contract before editing, keep the selected Page scope, and use its layout rules.
This is the one exception to "this job never edits
the Page": a Discovery Page that files one source per Run (a video knowledge
page, for example) is moved from the four-division layout into
`layout: one-division-per-run`, so each Run is one Content division. The
layout rule itself lives in `haipipe-discovery/ref/page-types.md`, where the
checker reads it; this section is the job that applies it, one Page at a time.

1. **One subagent per Page folder**: the main session fans out within the selected Page scope, using the configured model.
2. **The subagent moves text, never rewrites it**: notes stay word for word.
3. **One reviewer per Page**: `haipipe-discovery-reviewer-agent`, one fix round.
4. **Three checks close a Page**: checker clean, nothing lost, reviewer pass.

**Who runs it.** The main session lists the Page folders (every Page whose
Runs are all one-source Runs), then runs one Workflow `pipeline()` over them:
a writer agent per Page , then a reviewer agent
(`agentType: 'haipipe-discovery-reviewer-agent'`), then one
fixer round for a Page the reviewer fails. Each writer edits only its own
`<task>/<task>.md`, creates no file, and runs no git. The main session presents the combined changes; commit only when explicitly requested.

**The target layout**, top to bottom:

```text
frontmatter     add  layout: one-division-per-run   (every other field kept)
Opening         question line unchanged; second line becomes
                "This page files N videos. Each video is one Content division
                below, and the table in division 1 shows which ones are checked."
### 1 · Concept · <concept in a few words>
  **Concept**: the idea in plain words first, then one row per video.
  text block    the old division 1 Scope block, unchanged (Page, Block, Job,
                Sources, Nearby, Related, Uses)
  What it is · How it works · Why it matters      unchanged
  **The videos on this page**:
  | # | Run | Video | Length | Interview | State |    one row per Run;
                Video = the same English gist as that Run's heading;
                Interview = ★ or ·; State = drafted (checked once verified)
  How the videos fit · Interview questions        unchanged
### k · rNN · <English gist, a few plain words>     one per Run, Run order
  **rNN**: one sentence on what this video says
  text block    Video → url · Title → original title · Creator → name ·
                length · interview-marked: yes|no · Result → results/<stem>/ ·
                State → drafted from the transcript; claims not checked
                against the video
  [Bilibili video](...) · [Result Card](...)
  alias line, Key points, Interview hook, Check before reuse      unchanged
### N · Limits · what is still open
  **Limits**: what this page does not support yet.
  text block    Transcripts → <catalog path> (outside git); automatic speech
                recognition, terms and numbers may be misheard
                Source list → <b00 source list> · Citations → ... · Next move → ...
  the old Limits prose, unchanged
## Aims          one Aim per division, same names, same order
  A1            the old A2 item(s) with their Done when and Now lines
  A2..A(N-1)    🔨 rNN's key claims are checked against the original video.
                Done when: every item under its Check before reuse is
                confirmed or corrected against the video.
  AN            🔨 Notes drawn from transcripts are not treated as checked
                claims. Done when: every Run's State in the table reads checked.
                Any old A4 Now line moves here.
```

**What is dropped, and why nothing is lost.** The old division 1 stock
sentence ("This page answers the one question in the Opening...") is the same
on every Page. The old Payload text block (`rNN ★ <title>`) becomes the table
plus each Run's Title line. The old Evidence map text block becomes each Run's
Result line plus the Limits block's Transcripts and Source list lines. The old
A1 and A3 Aims described the four-division layout and go with it. The only
edits to kept text are cross-references: "section 3" or "division 2" is
renumbered to where the text now sits.

**The checks.** `paper_runs.py check <task folder>` prints no `ERROR`. The loss
check compares the Page with `git show HEAD:<page>`: every line of the old
Page must appear unchanged in the new one (section numbers aside), except the
layout lines the move replaces (division, Aim, and `####` card headings; the
Payload and Evidence map text blocks; the old `**Scope**`/`**Payload**`/
`**Evidence map**` labels; the card link line; the Opening's second line; the
stock division-1 sentence; Aim item and Done-when lines; the old Transcripts
line). The counts of notes blocks, video links, Result Card links, and
`**Now:**` lines must match. The reviewer
reads the old and new Page side by side and fails it for lost or reworded
notes, a gist that misstates its notes, non-English headings, or em-dashes.
Rebuild the Board afterwards (`haipipe-board/cli/build.py <block>`) and open
one Page to see the divisions render.

**New Pages start in this layout.** A generator that writes new video Pages
(Proj10's `import_bilibili_archive.mjs`) writes this layout directly, with a
placeholder gist (`rNN · gist to be written`) that the page writer replaces.

## 📂 Files

```text
haipipe-task-for-page/
├── SKILL.md                     this specialist
├── ref/specimen-page-values.md  one worked job, frozen (illustrative numbers)
└── CHANGELOG.md                 version history
```

The base is `haipipe-task` (hierarchy, lifecycle commands, and Run/Result anatomy). The
Page-side contracts it serves but never edits are
`haipipe-page-outline`, `haipipe-page-evidence`, and
`haipipe-plugin-outline/ref/item-table.md`.
