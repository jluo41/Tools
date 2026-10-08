---
name: haipipe-run
description: >-
  Define, allocate, resume, count, or audit HAIPIPE Runs using their owning
  domain contracts. Use when deciding Run versus Step, resolving
  Ticket/Result/receipt identity, choosing reuse versus new work, or composing
  Workflow Run Specs. Covers Execution, Discovery, Page, Insight, Design,
  Paper, and Labeling profiles. A Run is one folder in runs/, hard (result/,
  evidence; rNN_<slug>, or run-<type>-<target> where its theme names every Run so,
  as Design does, with kind: in run.yaml) or soft (run-<type>-<target>, writes into
  its scope), with passes and a run.yaml card. Names every workbench button's Run and owning skill, Space by Space,
  and writes a soft Run's card and passes. Trigger: Run contract, Run catalogue, hard or
  soft Run, pass, run.yaml, Run ticket, runtime receipt, orphan Result, which skill owns
  this button, run types by Space, soft_run.py, /haipipe-run.
metadata:
  version: "0.33.0"
  last_updated: "2026-10-07"
---

# /haipipe-run · one commission, one identity, preserved history

A Run is one durable, addressable commission for a bounded target and close
rule, kept in one folder. The ladder is Block → Job → Task → Run → pass: a Run
sits in its scope's `runs/`, and each execution or round of work on it is a
pass. A Run may contain several Steps; Result is a hard Run's generated output,
not another hierarchy level.

```text
Run type → (Run Spec) → Run = runs/<run>/ → pass = passes/pNN-<MMDD>/
Run identity = folder name = ticket stem = run.yaml run:
```

## Hard and soft Runs

A Run is **hard** or **soft**, decided by where its output lands (JL 261006).

| | Hard | Soft |
|---|---|---|
| Name | `rNN_<slug>` | `run-<type>-<target>`, no date (the date is in its passes) |
| Ticket | `rNN_<slug>.sh`, or a runner's `.yaml` | `run-<type>-<target>.md` |
| Output | only its own `result/` (generated) | its scope's items: `draft/`, `studio/`, `reports/`, `delivery/` |
| Counts as | evidence | work, not evidence |
| Where | a work Task only | a Block, a Job or a Task; a Page Task has soft Runs only |
| New pass | a retry or rerun of the same ticket and inputs | one more round on the same target |
| New Run | new inputs, data, goal, target or close rule | a new target |

A hard Run may carry several type tags (`type: [fit, evaluate]`) while one close
rule settles it; two close rules make two Runs. A Page reads finished hard
Results only (select, round, format, plot, quote) and computes no new facts: its
display, value and citation Runs are soft, and their code stays in the Page with
its display (`displays/<fig>/recipe/ · assets/`). A new number needs a hard Run
in a work Task. A Task is known by its name (`tNN_<task>/` with its face
`tNN_<task>.md`), not by what its `runs/` holds. A person's decision (signing a
design goal, a design Job's release) is soft.

## The Run folder

```text
runs/
├── r03_<slug>/                 hard
│   ├── run.yaml                the card
│   ├── r03_<slug>.sh           the ticket
│   ├── config.yaml             its frozen inputs
│   ├── result/                 generated: receipt, metrics, small tables, figures, heavy.yaml
│   └── passes/p01-<MMDD>/      log · runtime.yaml, one per execution
└── run-section-<target>/       soft
    ├── run.yaml
    ├── run-section-<target>.md the ticket: target, ask, close rule
    └── passes/p01-<MMDD>/      ask · before/after of the target · ledger · touched.yaml
```

`run.yaml` is the one lookup card, the same fields for both kinds, written only
by tools (the scaffolder, the ticket, the soft-Run writer, haipipe-project
`update`); a reader lists, counts and shows Runs from it without opening a
ticket or a receipt. Fields: `run · kind · type · scope · target · ticket ·
skill · agent · signs · status · passes · writes · feeds`; an unknown value is
null. The schema and an example: [Receipts and inventory](ref/receipts-and-inventory.md).

Older layouts (`runs/<run>.sh` beside `results/<run>/`, dated soft names) stay
readable until haipipe-project `update` moves them, one Block at a time.
haipipe-project `audit` checks every folder against this shape.

The identity is owner-qualified. Insight keeps its own naming beneath its
binding; see the identity reference.
Design names every Run `run-<type>-<target>/`, hard ones too (JL 261007: "unify the name to be
run-xxx-xxx"): its `run.yaml` `kind:` says hard or soft, and a repeat names what it reads
(`run-verify-d04-v2`), never a counter. A design hard Run's ticket is its `run.yaml` (an agent runs it under
its skill, no `.sh`), it retries in place while open, and its `result/` never changes once closed; its card adds
`by · started_at · finished_at · usage` to the card fields above. See haipipe-design `ref/design-ladder.md` and
haipipe-design-workflow `references/run-profile.md`.

A Workflow is a list of Runs. Its definition describes planned work as Run
Specs; its runtime lists the actual Run Instances. Dependencies and routes
connect those entries and permit branching, waiting, and parallel execution.
A list does not impose serial execution or allocate future identities.

## Runs by Space

Every Run button of the workbench frame names its owning skill (a `skills:` field on its
run type; b03 s21, 261007), and the button's Run is a soft Run named for its target. The
panel shows that name as the button (`run-draw-<sNN>`, `run-face-b03`), what it does in small
under it; buttons that make one Run are one button (JL 261007):

```text
Description      Update the description   haipipe-board · haipipe-job · haipipe-task   run-face-<level>
Idea Studio      add · redraw · save       haipipe-studio                               run-draw-<sNN> (one button)
Audience Report  Ask                       haipipe-question                             run-ask-<qNN>
                 Write · Drawing · Check   haipipe-report                               run-report|figures|check-<qNN>
Work Details     Add a Job · Add a Task    haipipe-board · haipipe-job                  run-add-<jNN|tNN>
                 Build the Task            haipipe-task                                 run-build-<tNN>
Runs             Run                       haipipe-run                                  run-<type>-<target> · rNN_<slug>
Delivery         Build the delivery        the level's skill                          run-delivery-<target>
```

The full table, with the Page Task's own buttons: [Run types by Space](ref/run-types-by-space.md).
A soft Run's card and passes are written by a tool, never typed:

```bash
S=Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-run/scripts
python $S/soft_run.py new  <scope> --type <type> --target <target> [--skill S] [--feeds …]
python $S/soft_run.py pass <scope>/runs/run-<type>-<target> --title '…' [--ask …] [--changed …]
```

`new` refuses a target that looks like a date and a second Run for the same target (a new
round is a pass); `pass` adds `passes/pNN-<MMDD>/pass.md` and updates `passes`, `status` and
`writes` in `run.yaml`.

## When and by whom

| Reader | Use this contract for |
|---|---|
| Workflow / Paper / Ideation planner | deciding which bounded work deserves a Spec and which native profile applies |
| Task / Discovery / Page / Insight / Design / Paper / Labeling owner | allocation, reuse, history, receipt, and closure invariants |
| Selected worker | the commissioned Ticket and its output/authority boundary |
| Run presenter / Task or Workflow table | locating, diagnosing, and counting the same native records |
| Direct user request | explaining or auditing Runs and the next required action |

Resolve the owner and selected Workflow/Spec before allocation. For an audit,
missing ownership is a finding, not a reason to hide the record. Load only the
relevant owner profile after this contract. Workers do not reload every family
for each call. Ordinary shell commands do not automatically become Runs.

| Request | Read next |
|---|---|
| Select or define a type/profile; see what kinds exist | [Run catalogue](ref/run-catalog.md) and the selected owner |
| Which skill owns a workbench button, and the Run it makes | [Run types by Space](ref/run-types-by-space.md) |
| Allocate, reuse, retry, reopen, or resolve storage | [Identity and history](ref/identity-and-history.md) |
| Scaffold/read receipts, report status, count, or audit | [Receipts and inventory](ref/receipts-and-inventory.md) |
| Compose multiple Runs or maintain a shared frontier | [Workflow](../../task/haipipe-workflow/SKILL.md) and its [runtime contract](../../task/haipipe-workflow/ref/workflow-runtime.md) |
| Present Runs in a Page | [Run presenter](../../page/workbench-page/ref/run-space.md) |

## What earns a Run

Allocate only when all six hold:

1. A bounded goal or target is named.
2. A stable type/profile resolves and the owner can allocate an address.
3. A Ticket/Spec commissions an actor and action or interaction.
4. A close rule can settle success or truthful non-success.
5. The outcome has a durable Result/receipt.
6. Closure is independent of the caller's presentation surface.

Planning candidates and SURVEY reservations have no allocated Run inventory
row. Human decisions qualify only under these same tests. A click, signature,
comment, gate evaluation, script, tool/API call, or retry is internal when it
serves an existing Run's target and close rule. A separate commission may make
review its own Run; a label such as Gate 1 does not establish that commission.
Do not count both an umbrella episode and the independently closable work it
groups. A control-only Workflow invocation can truthfully have `runs: []`.

## Ownership and planned versus actual work

| Object / authority | Owns |
|---|---|
| Shared Run contract | qualification, identity/history facts, lifecycle and inventory invariants |
| Folder/domain profile | native naming/storage, operations, schemas, acceptance and promotion authority |
| Run Type | reusable defaults, allowed actor/action/Result, and default close rule |
| Run Spec | bounded goal, actor, action, inputs/dependencies, gates/routes, cardinality and internal Steps |
| Workflow definition | Spec list, dependency/Route graph, entry and overall completion rules |
| Run Instance | allocated address, frozen type/contract, state, attempts, Result and receipt |
| Worker | execution method and declared outputs within the commission |
| Run Spec × Workspace Cell | skill bindings, interaction, authority and projection for that surface |
| Presenter | read-only views of native records |

A Workspace never becomes the execution owner. Do not create a horizontal
`run-for-<folder-kind>` owner. Use the existing native owner and selected worker.
When a Workflow declares Workspaces, bind its Cells in the
family's own `ref/workflow-table.md`; a standalone Run does
not require inventing a Workbench roster or aggregate controller.

A Spec can materialize zero, one, or many instances. Symbolic cardinality is
planned demand; only allocated native records describe actual work. A Runtime
may index reused Results without allocating or executing them again. When a
shared frontier is useful, `workflow_runtime_id` identifies its aggregate
receipt; it is never a child Run address.

Gate/Route modes are `human | automatic | agent | hybrid`. Entry may default
open; exit semantics are mandatory and may be inherited from the type. A
terminal route may default to `CLOSE`; nonterminal routes are explicit.
Inputs, dependencies and a domain payload can be empty; target, actor, action,
close rule and durable outcome cannot. Resolve required facts through the
profile/Ticket/receipt rather than copying every field into every dialect.
A controller `Run()` label is adapter metadata, not an authority or Run node.

## Choose the next action

| Situation | Action |
|---|---|
| Exact accepted Result satisfies the request | reuse its full identity, version, path and hash |
| Matching open commission exists | resume through its owner |
| Same frozen contract failed | preserve the failed pass; add the next pass |
| Open soft Run receives feedback within its goal | append a Step to the open pass |
| Same target is worked on again (a later session, a reopen) | the same Run, a new pass; closed passes stay as they are |
| Frozen data, goal, target, or acceptance changes materially | new Run; record supersedes only for an actual replacement |
| Input/authority/profile is missing | report the gap; do not invent a Ticket, identity, approval, or completed Result |

Interactive history is a scoped exception: do not apply evolving soft-Run
feedback to frozen Execution or Discovery inputs. A pass is append-only while
open and immutable after closure; the Run's history is its `passes/`, kept in
the Run folder (no separate journal folder). New participants, sentences,
labels, Steps, or passes do not allocate child Runs.

## Lifecycle

1. **Plan:** resolve owner, profile, bounded commission, dependencies and close
   rule. Check for reusable Results or a compatible open Run.
2. **Allocate/scaffold:** the owner chooses a collision-free identity, creates
   `runs/<run>/` with its ticket and `run.yaml` (`status: planned`) before
   expensive work. Freeze required inputs (`config.yaml`) before dispatch.
3. **Execute:** invoke the selected worker through the ticket and native runner.
   Each execution or round is a pass, `passes/pNN-<MMDD>/`; earlier passes stay.
4. **Validate/settle:** apply the owner's Result gate; record actual outcome,
   errors and route. Process exit alone cannot establish completion.
5. **Bind/promote:** the authorized consumer references the exact Result and
   separately records any evidence admission, Page release, or promotion.

Timestamps describe actual events. Unstarted/unfinished/unknown values remain
null; non-null new timestamps use RFC 3339 with an explicit UTC offset.
Scaffolding is not proof of completion. Waiting for a human is a normal state.
A complete bounded decision can record `hold` while its Workflow remains held.

## Example: one commission, several activities

A Workflow commissions one model fit and a separate independent evaluation.
Its definition has two Specs with an evaluation dependency. The Task owner
allocates the fit, `r01_fit_<slug>`; its internal calls and an unchanged-input
retry remain one Run with two passes. Only when commissioned and ready does evaluation get
its own Ticket and receipt. Two Pages can reuse that fit Result without new
fit Runs. The eventual inventory has two native Runs, not a row for every
call, retry, Result file, consumer, or controller invocation.

## Result, evidence, and closure

**A Result is light.** It holds the receipt, metrics, small tables, figures,
reports, and pointers: whatever a reader or a Page needs to see what the Run
found. A Run's heavy output (a model, an array, a cache, a row-level table
beyond a small sample, any file over 10 MB) lives outside the Result, and the
Result records a pointer to it: a SPACE-relative path with each file's size and
hash. A Task Run's heavy output has its own folder,
`_WorkSpace/ProjectResult/<Project>/<block>/<job>/<task>/<run>/`, the Run's
address below `tasks/` (the Ticket exports it as `HEAVY_DIR`, and writes the
pointer `heavy.yaml` into the Result); a pipeline asset (a SourceSet, an
ExternalStore version) goes to its stage store instead. Never a copy of the heavy file in the Result or its Folder, and never a
symlink to an absolute path or into the heavy store: such a link stores an
absolute path and dangles on every other machine. A relative link inside the
repository (a shared `_run.sh`) is fine (JL 260929). How a Task does it: [Artifact placement](../../task/haipipe-task/ref/authoring-conventions.md#artifact-placement).

Evidence is a hard Run's Result. A soft Run's output is the item it wrote
(a draft section, a drawing, a delivery build), recorded in its passes.

A Result may be a checked artifact, judgment, or truthful failure.
The Result gate belongs to its profile. Evidence admission and downstream
promotion are separate facts; an unused valid Result stays valid. Feedback
and accepted writing history are authoritative records, not regenerable caches.
When upstream data changes, preserve the historical Result and mark affected
downstream bindings stale until new work or valid reuse resolves them.

For a Task-to-Page handoff: Page proposes work, Task allocates/executes its
native Run, Task returns the Result/receipt, and Page binds the full identity
and fingerprint. Neither face can close the other's obligations; use the
[Task/Page closure contract](../../task/haipipe-task/ref/task-page.md).
RE labels and Cards are projections of one focal Result. Supporting Runs keep
their native identities. Accepted RP prose does not prove RE evidence ready
or close whole-Page CHECK. A Page's delivery builds are one fixed Run per lane (`run-delivery-<lane>`); a design Job's
delivery is written by its soft `run-release-j<NN>` from the kept, verified designs (haipipe-design-delivery).

## Inventory and boundaries

State the inventory scope and grain. Enumerate the union of native Tickets
and receipts/Results; diagnose missing pairs and duplicate addresses. Count
one row per owner-qualified logical Run and keep recovery-needed records
visible. Separate valid allocated, reused, planned, and incomplete records;
never silently treat missing receipts as valid allocations. Historical
execution versions may be expanded with an explicit execution count.

Use the [receipt/inventory procedure](ref/receipts-and-inventory.md) before
claiming completion or totals. Presenters cannot repair records on read,
allocate Runs, or turn their display states into domain acceptance. Keep
artifacts in their governed stores with safe pointers; no credentials, private
tokens, PHI, or raw sensitive rows in shared receipts.

## Files

The `ref/` files own the shared catalogue, identity/history, receipt/audit detail,
and the Run types by Space; `scripts/soft_run.py` writes a soft Run's card and passes, and
`tests/` checks both. Domain references linked by the catalogue own their concrete profiles.
`agents/openai.yaml` supplies invocation metadata; `CHANGELOG.md` records
changes. Do not duplicate domain schemas or fabricate a missing implementation.
