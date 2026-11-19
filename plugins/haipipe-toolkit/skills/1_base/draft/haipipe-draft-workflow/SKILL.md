---
name: haipipe-draft-workflow
description: "The Page workflow controller: dispatches context (PREPARE), structure (SHAPE, SURVEY), evidence (LAND, EMBED), writing (WRITE) and check over a Run Spec graph. Use to design, run, resume or audit a Page lifecycle. Trigger: Page workflow, run a page, Run Spec graph, /haipipe-draft-workflow."
metadata:
  version: "0.67.1"
  last_updated: "2026-10-26"
  # version history: ./CHANGELOG.md
---

# /haipipe-draft-workflow · route one persistent Page by authority

At adoption, build, or release, apply `../haipipe-draft/ref/release-decisions.md`
for profile precedence and reuse of existing human decisions.

## 🧬 Canonical ontology

The Page workflow uses the neutral Run ontology. A **Workflow is a list of
Runs**: the definition lists Run Specs and the runtime lists actual Instances.
The Workflow owns the dependency graph compiled from Spec Routes, entry rules,
and legal terminal rules; it is not a second Route authority. A **Run Type** supplies reusable defaults and the allowed
action/result grammar. A **Run Spec** owns the bounded goal/target, actor,
gates, routes, and references to Cells that bind skills and Workspaces. A **Run Instance** owns
the stable id, status, result, receipt, and attempt history. A **Workspace**
owns presentation and interaction only. A Step is an internal action inside
one Run and is never a workflow row.

Fixed-scope Page writing is one persistent Run. Human feedback is an internal
Step. Reopening the same target and goal creates a new Version in that Run;
changing the goal or target is `NEW_RUN`. A separately commissioned later
Section session may also receive a new `run-section-<slug>` under the Page profile.
Acceptance is the Run exit gate,
subject to the declared dependency and mechanical close semantics.

The four interactive routes are:

```text
SELF / next Step     same Run and current Version
NEW_VERSION          same Run, same target and goal, new Version
CLOSE / next Run     close this Run, then select the next bounded scope
NEW_RUN              new commissioned Run for a changed goal or target
```

These transitions do not create extra Workflow Table rows. The fixed-scope
writing behavior remains one parameterized Run Spec row: feedback appends
Steps, reopen appends a Version to the same Instance, and `NEW_RUN` allocates a
second Instance under that row unless the Workflow definition truly changes.

Human, automatic, agent, and hybrid are valid gate and route modes.
Inputs and dependencies may be empty or omitted. Entry defaults to `open`;
exit may inherit a Run Type default, but its close semantics are required.
Even when a Result payload is optional, a terminal outcome and durable receipt
are required.

The formal controller/API serialization carries `run`, `cycle`, and
`next_cycle` fields. They are controller dispatch/progress labels only, never
semantic workflow authority, Run Specs, or Steps. The `route`, `reason`,
artifacts, evidence, findings, and human-gate pointer in each receipt remain
the truthful audit of the controller action.

## 🧭 Workflow Runtime boundary

One automated Page workflow pass is one Workflow Runtime execution, not a
Page Run. The canonical aggregate identity is `workflow_runtime_id`; the
existing `run_id` packet/result field remains a low-level adapter alias and
must equal it for new packets. `rp-*` identities remain reserved for
independently commissioned interactive Page Runs. Gate and route evaluations
are Runtime control records; RP/RE/RD children keep their owner-native ids.

Load every Page controller label through one canonical order:

```text
haipipe-draft
  → haipipe-draft-workflow
  → current Run Workflow / Run Spec owner skill
  → Folder-owning workflow or canonical family skill
  → Page Face owner skill
  → Run Spec references and narrative/style policy
  → haipipe-draft/ref/page-run-families.md when naming RP, RE, or RD
  → ref/structure-run.md when allocating or resuming the Page Structure Run
  → haipipe-run + selected workers, only when this controller label
    materializes Run Instances
```

Resolve the Folder owner and Page Face owner before acting. A Page Face owner
is the exact Run Workflow/Run Spec owner skill, canonical family skill, or unmigrated Page
Type skill that owns this Folder's readable contract; load it only once when it
is also the Folder owner. Load
only the current Run Spec references and the workers for Run Instances it actually
commissions. For CONTEXT, OUTLINE, and EVIDENCE those references live under
`workbench-task-draft`; the Page surface has already installed that workbench
as the shared presenter. A low-level adapter label may abbreviate this chain, but it may
not reorder authority or omit the Page Face owner. The label does not become a
second semantic authority beside the Workflow and its Run Specs.

## ⚡ Fast feedback Step is the default

**Run bookends (JL 260928).** The person opens a writing Run and later says it
is over. `page.py open-run` writes the Run's one ticket at the open. In between, only the
Draft file changes; the Run journal, `working.md`, `runtime.yaml`, log entry, evidence notes and receipts
are written once at the close, from the conversation. Adopting the Draft into Page Content and
the web → LaTeX → Word delivery lanes follow only when the person asks. The
contract is the first section of `ref/interactive-writing-run.md`.

For wording feedback on an open Page Run, do not execute the full workflow
chain again. Use the already loaded context, read only the named paragraph
slice in the Draft file, its dependent Bullet, and the frozen Structure
description. Make one bounded patch to the Draft, perform one narrow check, and
return. Aim
to finish under two minutes. No sub-agent, broad reread, plan rewrite,
outline pass, build, export, browser check, full test suite, or post-run
analysis belongs in this path. A wording-only Step never edits the Page source,
delivery, or plan metadata. If a required input is absent, return one blocker
and stop instead of searching the whole repository.

For an in-place Folder, the resource identity record `workflow/folder.yaml`
resolves the owning workflow and Folder kind before Page frontmatter or legacy
names; it records resource identity, never execution progress. The
current evidence graph never creates a new `probe/` lane; a stored old lane and
outbound-card history are historical read-only input.

The Run Spec × Workspace map is summarized in the middle of this file;
`ref/workflow-table.md` and `ref/run-cards.md` are
current Run Spec projections. The executable packet/receipt law is
`ref/page-run-contract.md`.

## 🤝 Interactive writing first → [`ref/interactive-page-runs.md`](ref/interactive-page-runs.md)

## ⚡ The result

One Page Run Workflow is a directed graph of bounded Run Specs. The five labels
below are retained as a compact controller/API adapter projection; they
dispatch Run Specs and Workspaces, but they are not five Level-4 Run kinds or a
second semantic authority. A concrete Page may add, omit, branch, or repeat
Run Specs according to its declared Workflow Definition:

```text
context     haipipe-draft-logic (ref/context.md)     PREPARE · Collect, Resolve, Freeze
structure     haipipe-draft-logic (ref/structure.md)     SHAPE · SURVEY
evidence    haipipe-evidence    LAND · EMBED
writing     haipipe-draft-writing     WRITE · Adopt, Integrate, Build, Pre-check
check       haipipe-draft-review       CHECK · whole-Page close gate
```

`Outline` and `Content` align with the Page's two substantive Workspace
projections:
Outline holds the plan and the frequently revised candidate prose; Content is
the adopted Page text. Draft and Revise are writing movements, not separate
Run Specs. Interactive Steps and Page Run closures remain in Outline; after all
planned Page Run Instances and their required evidence are complete, one
Page-level CONTENT controller pass performs adoption and delivery.

Every user-facing completion after a Page-changing action follows
`../haipipe-draft/ref/user-check-packet.md`. Routine writing returns the
exact Run/Version/Step heading, saved selected paragraphs, a brief change
explanation, and three final Draft Space, Evidence Space, and Current Run links.
Formal delivery also provides current evidence surfaces and the Page-level PDF. DISPLAY evidence
is a typed Result at `results/<re-run>/result.yaml` with its unit under
`results/<re-run>/payload/<unit>/` (a draft Task since 2026-10-16: `display/Display<n>-<slug>/`); it appears in Outline's Evidence Space and is consumed by
current Delivery exporters. `draft/evidence/bibex/` and `delivery/latex/` remain current lanes;
`outline/evidence/display/` is migration-only. The workflow receipt remains the audit record; it is not the primary
user-facing answer.

## 🧭 One Outline workbench serves three Workspaces

CONTEXT, OUTLINE, and EVIDENCE all use `workbench-task-draft`:

```text
workbench-task-draft
├── Draft Space          Structure list + Bullet/Draft table; read-only projection
├── Evidence Space       typed Result cards; read-only projection
└── Run Space            Page Writing + Page Evidence + Supporting Runs
```

This is shared storage and presentation, not shared semantic authority. Context
records remain off-stage and are opened through Folder inspection. Never create
`workbench-context` or a second Evidence workbench. The Run Spec owner skills write;
the workbench reads and presents.

## 🔁 Run routes

```text
CONTEXT/PREPARE
  └─ resolved context
       ▼
OUTLINE/SHAPE ── evidence owed ──▶ OUTLINE/SURVEY
       ▲                                  │ decided graph
       │                                  ▼
       └──────── EVIDENCE/EMBED ◀── EVIDENCE/LAND
                       │ next evidence revision v<G>.<S>.<E+1>
                       ├─ G=0 ───▶ SHAPE; Content remains closed
                       └─ checked Shape or explicit user CONTENT instruction ─▶ CONTENT/WRITE
                                        │ exact built version
                                        ▼
                                  CHECK/CHECK ──▶ CLOSE
                                      │
                                      └─ route to the authority that owns a finding
```

Each Run Spec in this table has one owner (a skill, or a `ref/` page of one), named by the Run:
`haipipe-draft-logic (ref/context.md)`, `haipipe-draft-logic (ref/structure.md)` (rp-struct), `haipipe-draft-logic (ref/scratch.md)`
(rp-scratch), `haipipe-draft-writing` (rp-sec, rp-para), `haipipe-evidence (ref/page-evidence.md)`
(re-*), `haipipe-draft-writing (ref/revise.md)` (rp-revise), `haipipe-delivery (ref/page-delivery.md)` (rd), and
`haipipe-draft-review` (the gate). The CONTEXT/OUTLINE/EVIDENCE/CONTENT/CHECK
words below are the old Run names; they survive as route and Step names,
not as skill names.

The flow is a controller routing grammar, not a conveyor belt. CONTEXT reopens
when its authorities change; SHAPE and SURVEY may repeat inside the Structure
Run; LAND works item graphs in parallel; EMBED returns a `v0.*` fold to SHAPE
and a `G>=1` evidence fold to CONTENT; CONTENT may loop; CHECK may route to
any earlier authority. The labels shown in this diagram are dispatch/progress
coordinates only. The Run Spec graph and actual Run Instance receipts decide
what work exists and whether it can close.

## 📊 Run Spec × Workspace projections

The detailed map is `ref/workflow-table.md`. It is a Run Spec × Workspace
projection of actual Run units. Controller operations are listed separately below and never enter the Run inventory.

| Run Spec | Run Type | Bounded target / action | Actor | Entry / exit gate | Legal routes | Cardinality | Workspace projection | Run names |
|---|---|---|---|---|---|---:|---|---|
| `run-structure-<slug>` | page.interactive-writing.structure | whole-Page map, ordered Bullets, paragraph jobs, Point roles, typed Evidence Item decisions | human / agent / hybrid | entry open; exit requires accepted Shape + Survey contract | SELF / next Step, NEW_VERSION, CLOSE / next Run, NEW_RUN | exactly 1 initial Structure Run per Page | Draft, Evidence, and Run Spaces | structure / SHAPE+SURVEY |
| `run-scratch-<slug>` | page.interactive-writing.scratch | rough human thinking for Section or whole paragraph group in the current Outline grammar; no B/symbol target | human | person manually triggers Finish Scratch; AI returns a non-empty Summary | SELF / Save, CLOSE / Finish Scratch, NEW_RUN | 0..N per target | Draft Space Scratch view and Run Space | structure / SCRATCH |
| `run-section-<slug>` | page.interactive-writing.section | one named Section's bounded candidate and review cycle | human / agent / hybrid | entry open; exit requires scoped acceptance and declared dependencies ready | SELF / next Step, NEW_VERSION, CLOSE / next Run, NEW_RUN | 0..S selected Section Runs | Draft Space and Run Space | structure / SHAPE and writing / WRITE |
| `run-paragraph-<slug>` | page.interactive-writing.paragraph | one fixed paragraph or contiguous paragraph group | human / agent / hybrid | entry open; exit requires acceptance, settled Bullets, and ready evidence obligations | SELF / next Step, NEW_VERSION, CLOSE / next Run, NEW_RUN | 0..K, 1 <= K <= N | paragraph Draft Space, Evidence Space, Run Space | structure / SHAPE and writing / WRITE |
| `run-revise-<slug>` | page.interactive-writing.revise | compare two frozen texts of one target (two Versions of a writing Run, an accepted Version against a delegated paragraph Result, or two built Page versions) and settle every change | fresh agent / human, never the writer of the candidate | entry requires both inputs by path and version number; exit requires every ledger row decided | SELF / next Step, CLOSE / hand accepted text to the writing Run as NEW_VERSION, NEW_RUN, HOLD | 0..N per target | Run Space Revise card; Draft Space read-only | REVISE |
| `run-value-<slug>`, `run-citation-<slug>`, `run-display-<slug>` | page.evidence-item | one focal VALUE, CITE, or DISPLAY Result for one make-item | agent / automatic / hybrid | entry open; exit requires typed Result acceptance and any declared verification | SELF / next attempt, CLOSE / next Run, NEW_RUN, HOLD | exactly 1 Page RE per make-item, plus 0..N Supporting Runs | Evidence Space and paired Run/Result records | evidence / LAND+EMBED |
| run-delivery-<lane> | page.delivery | one lane (webpage, latex, word); one fixed Run per lane, rerun in place | agent / automatic | open any time; Done while the lane's files are at least as new as the Page | SELF (rerun), HOLD | one per lane, never numbered |

### Controller operations (outside the Run list)

| Operation | Responsibility | Record |
|---|---|---|
| Context | Resolve and freeze inputs for selected Runs | Context record and compatibility receipt; no Run Instance |
| Adoption | Adopt the accepted candidate after the release decision | Release decision and references to the existing writing Results |
| Check | Independently judge one immutable built version and route findings | Check receipt and owed decisions; no Run Instance unless separately commissioned |

The formal API may serialize the Run names as Run, cycle, and
next_cycle. Those names do not change the Run Type, Run Spec, Run Instance, or
Workspace semantics above.

## 🧱 Workflow orchestration and Run identity → [`ref/run-identity.md`](ref/run-identity.md)

## 🆔 Run references → [`ref/run-identity.md`](ref/run-identity.md)

## 🧠 Exact skill routing

For every Run Workflow dispatch, record exact owner names rather than generic labels:

```text
haipipe-draft-workflow
  → current Run Workflow / Run Spec owner skill
  → Folder-owning workflow or canonical family skill
  → exact Page Face owner skill
  → exact narrative/style/outline policy skill, when applicable
  → haipipe-run + worker skills, only when the Run Spec commissions Runs
```

For the first three planning dispatches, append the exact
`workbench-task-draft/ref/...` material contracts needed by the Run Spec; do
not append the presenter skill as an execution dependency.

Paper's bounded work is declared in
`2_theme/paper/haipipe-paper-workflow/ref/run-workflow.md`. Resolve the exact Paper
PageType through the Paper router; an Ideation Page loads
`haipipe-paper-ideation`, which delegates semantic work to `haipipe-ideation`.
That does not make every Page an Ideation consumer. Sync and gate recording
remain controls; actual RP/RE/RD and supporting executions keep native IDs.

Example for a paper Section Shape:

```text
haipipe-draft
  → haipipe-draft-workflow
  → haipipe-draft-logic (ref/structure.md)
  → haipipe-paper-workflow
  → haipipe-paper-draft
  → haipipe-paper-story             (the §8 Section Narrative row the Section executes)
  → workbench-task-draft/ref/plan-grammar.md
  → workbench-task-draft/ref/item-table.md
```

Do not insert a separate Task Page-Type layer. `haipipe-task` is both canonical
Folder owner and Page Face owner for a Task Folder, so load it once; its
`ref/task-page.md` (§ Displays) holds the Task Page's display and prose
requirements, with no execution or closure authority of its own.

## 🔀 Route by broken authority

| Finding | Route |
|---|---|
| Page/Folder identity, policy, requirements, related context, or context freshness | CONTEXT |
| argument, division shape, Bullet contract, item expectation, or Aim promise | OUTLINE |
| Supporting/local evidence graph, input, Result, acceptance, or fold freshness | EVIDENCE |
| candidate prose/feedback in interactive mode | current Writing Step; SHAPE for dependent plan changes |
| adopted prose, citations in prose, caption, build, or paragraph promotion | CONTENT |
| exact built version needs independent judgment | CHECK |
| all closing rules and human gates pass | CLOSE, from CHECK only |
| required authority/input cannot safely resolve | HOLD |

Legal adapter routes:

```text
CONTEXT  → CONTEXT | OUTLINE | HOLD
OUTLINE  → CONTEXT | OUTLINE | EVIDENCE | CONTENT | HOLD
EVIDENCE → CONTEXT | OUTLINE | EVIDENCE | CONTENT | HOLD
CONTENT  → CONTEXT | OUTLINE | EVIDENCE | CONTENT | CHECK | HOLD
CHECK    → CLOSE | CONTEXT | OUTLINE | EVIDENCE | CONTENT | HOLD
```

The EVIDENCE → CONTENT edge is only for a pure EMBED under an approved G>=1
Shape. Stored controller receipts are read-only input under
`ref/page-run-contract.md#historical-adapter-receipts`.

## 👷 Actors

```text
CONTEXT   haipipe-draft-context-agent    producer
OUTLINE   haipipe-draft-structure-agent    producer
EVIDENCE  haipipe-draft-evidence-agent   producer
CONTENT   haipipe-draft-writing-agent    producer
CHECK     haipipe-draft-check-agent      fresh read-only judge
builder   separate mechanical actor     build/check only
human     only the declared person-reserved decisions
```

Every producer follows `ref/producer-contract.md`. The actor that produced a
source/render version may not judge it. A missing registered agent may use a
stand-in only after the stand-in reads that exact agent file as its identity.

## 🧑 Human gates and run mode

The same person-reserved acts exist in `copilot` and `auto`; only waiting
behavior changes:

```text
copilot   an unanswered selected act may pause the loop
auto      review ticks may defer to the owed ledger; an explicit stop still wins
```

The acts remain at their authorities:

| Act | Owner |
|---|---|
| plan `approved:` | SHAPE, written by `page.py sign` from the person's own words; CONTENT runs only on a signed plan, and a next-step instruction never replaces the sign (JL 261111) |
| per-item `Decide` | SURVEY; branching choice, never auto-deferred |
| CITE item `Verified` and any worker-specific verification | LAND |
| Page/display `accepted:` and Folder ruling | CHECK |

No machine writes a person's act. An auto run may continue under the declared
policy while a review tick is owed, but it must HOLD at SURVEY when `Decide`
is unsigned; a prior explicit durable decision/default policy may be consumed,
never invented. `page_ruling: none | domain-gate | local` comes from the
Folder-owning workflow. Do not invent a duplicate Page gate.

## 🔁 Auto revise · rounds until good enough

Run on the person's ask ("auto revise C2"), s41-D13. Each round the controller dispatches two different agents:

```text
1 writer    haipipe-draft-writing   revise candidate.md (small fixes applied, big ones held)   ref/auto-revise.md
2 reviewer  haipipe-draft-review    a FRESH agent: the four rubric axes + anti_slop score     never the writer
3 record    cli/auto_revise.py record <run> <round.yaml>
4 check     cli/auto_revise.py check <run>  →  STOP or CONTINUE
```

Stop on the reviewer's verdict (no NEEDS WORK), no improvement, or 3 rounds; then `auto_revise.py cards <run>` writes
the decision cards for the Revise area. The controller never writes the Draft: the person's picks go in through the
next writing pass.

## 🔁 Execute one automated Page workflow pass

This bounded controller is for Run Workflow dispatch and formal completion, not the
human-feedback journal. Its `step`, limits, `HOLD` and `CLOSE` do not count or
terminate interactive writing Steps/Versions. Finish a chat turn while waiting;
resume from the Writing Run files when new feedback arrives.

The `/run` spelling is a controller command verb. The durable controller
bundle is a **Page workflow pass**, not a Page Run. Reserve the Page Run noun
for `family: page`, `operation: interactive-writing`, whose Version/Step history
is owned by the Page and shown in the Page Runs lane.

The packet minimally names:

```yaml
workflow_runtime_id: <durable aggregate id>
run_id: <durable id>
board: <absolute board path>
page: <board-relative Page path>
start_phase: CONTEXT
intent: <bounded purpose>
mode: copilot
sources: []
constraints: []
page_ruling: none
human_gate:
  required: false
  rule: ""
limits:
  max_steps: 12
  max_rounds: 3
```

Entry rules:

- a new Page begins at CONTEXT;
- an existing Page with a known stale authority begins at that dispatch label;
- an existing Page with unknown next need begins at CHECK, whose judge routes
  it without editing;
- a Page may skip evidence work only when SHAPE owes no make-item.

The executable controller is
`ref/page-lifecycle.workflow.js`. The deterministic
auditor is `../haipipe-draft/src/page_lifecycle.py`.

## 🧾 Receipts and terminal states

Every controller dispatch appends one receipt with the adapter dispatch label (serialized as `run`), cycle, actor, role,
source/render versions, route, reason, artifacts, evidence, findings, and
human-gate pointer. Dispatch receipts are workflow audit records; they are not
Level-4 Runs or Results.

Only CHECK may emit `CLOSE`. `HOLD` preserves a named missing input, conflict,
failed work, unresolved gate, concurrency mismatch, or exhausted bound. A
route name without a reason and owning authority is invalid.

Audit the durable bundle with:

```bash
python3 <haipipe-draft>/cli/pageflow.py audit <board>/_runs/page/<page-id>/<run-id>.json
```

## 📂 Files

```text
haipipe-draft-workflow/
├── SKILL.md
├── CHANGELOG.md
└── ref/
    ├── interactive-page-runs.md    Page Run kinds, allocation, Step budget, close
    ├── interactive-writing-run.md  persistent human-feedback Run protocol
    ├── run-identity.md             Run identity, evidence layers, full addresses
    ├── writing-step-template.md    original input, full output, scoped decisions
    ├── workflow-table.md       canonical design/adoption table
    ├── run-cards.md          compact Run Spec cards
    ├── ../../haipipe-draft/ref/page-run-families.md  RP/RE/RD and evidence bindings
    ├── page-run-contract.md    packet, receipts, legal routes, adapter mapping
    ├── producer-contract.md    shared Run worker packet and return
    └── measured-cost.md        prior measured dispatch costs
```
