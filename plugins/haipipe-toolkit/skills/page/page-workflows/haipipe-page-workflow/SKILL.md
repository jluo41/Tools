---
name: haipipe-page-workflow
description: >-
  The Page workflow controller: 00 CONTEXT/PREPARE, 01 OUTLINE/SHAPE+SURVEY,
  02 EVIDENCE/LAND+EMBED, 03 CONTENT/WRITE, and 04 CHECK are dispatch labels
  over a Run Spec × Workspace graph. It owns persistent fixed-scope
  human-interaction Writing Runs, including Scratch capture, across planning and prose iteration. It selects the
  exact Run Workflow/Run Spec owner skill, Page Face owner, policy, Outline workspace, Level-4 Run
  Specs, legal routes, and auditable receipts for one persistent Page. Use to
  design, run, resume, or audit the complete Page lifecycle. Trigger: Page
  workflow, workflow table, run a page, Run Spec, SHAPE SURVEY LAND EMBED,
  page context, page content, /haipipe-page-workflow.
metadata:
  version: "0.59.0"
  last_updated: "2026-09-15"
  # version history: ./CHANGELOG.md
---

# /haipipe-page-workflow · route one persistent Page by authority

## 🧬 Canonical ontology

The Page workflow uses the neutral Run ontology. A **Workflow** owns the
directed graph compiled from Run Spec Routes, entry rules, and legal terminal
rules; it is not a second Route authority. A **Run Type** supplies reusable defaults and the allowed
action/result grammar. A **Run Spec** owns the bounded goal/target, actor,
gates, routes, skill bindings, and Workspace bindings. A **Run Instance** owns
the stable id, status, result, receipt, and attempt history. A **Workspace**
owns presentation and interaction only. A Step is an internal action inside
one Run and is never a workflow row.

Fixed-scope Page writing is one persistent Run. Human feedback is an internal
Step. Reopening the same target and goal creates a new Version in that Run;
changing the goal or target is `NEW_RUN`. Acceptance is the Run exit gate,
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

The formal controller/API serialization still carries `phase`, `cycle`, and
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
haipipe-page
  → haipipe-page-workflow
  → current Run Workflow / Run Spec owner skill
  → Folder-owning workflow or canonical family skill
  → Page Face owner skill
  → Run Spec references and narrative/style policy
  → haipipe-page/ref/page-run-families.md when naming RP, RE, or RD
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
`haipipe-plugin-outline`; the Page surface has already installed that plugin
as the shared presenter. A low-level adapter label may abbreviate this chain, but it may
not reorder authority or omit the Page Face owner. The label does not become a
second semantic authority beside the Workflow and its Run Specs.

## ⚡ Fast feedback Step is the default

For wording feedback on an open Page Run, do not execute the full workflow
chain again. Use the already loaded context, read only the current Run resume
view, latest Version tail, named paragraph slice, dependent Bullet, and frozen
Mermaid description. Make one bounded patch, update only the required Run
projections and candidate preview, perform one narrow check, and return. Aim
to finish under two minutes. No sub-agent, broad reread, plan rewrite,
outline pass, build, export, browser check, full test suite, or post-run
analysis belongs in this path. A wording-only Step never edits the Page source,
delivery, or plan metadata. If a required input is absent, return one blocker
and stop instead of searching the whole repository.

For an in-place Folder, the physical controller record `workflow/phase.yaml`
resolves the owning workflow and Folder kind before Page frontmatter or legacy
names; its filename does not create Phase authority. The
current evidence graph never creates a new `probe/` lane; a stored old lane and
outbound-card history are historical read-only input.

The Run Spec × Workspace map is summarized in the middle of this file;
`ref/workflow-table.md` and the physically named `ref/phase-cards.md` are
current Run Spec projections. The executable packet/receipt law is
`ref/page-run-contract.md`.

## 🤝 Interactive writing first

For collaborative drafting or feedback-led revision, load
`ref/interactive-writing-run.md` and its `ref/writing-step-template.md` before
editing. One Page owns many sibling Page Runs. RP allocation states its scope
explicitly:

```text
rp-struct-NN          Page Structure Run: SHAPE + SURVEY
rp-scratch-NN_<target> Human Scratch capture: Section/Subsection/paragraph
rp-sec-NN             Section-level writing
rp-para-NN_Pxx[-Pyy]  Paragraph-level writing
```

`rp-struct-01` is the initial Structure Run. It is one shared Run for the
Page's SHAPE and SURVEY cycles: it settles direction, coverage/non-coverage,
high-level section flow, ordered Bullets, paragraph jobs, Point roles, typed
Evidence Item decisions, and the Mermaid representation. It does not write
adopted prose or execute material evidence work. Several people may contribute
Steps to this same Run; record `participants` on the Run and `contributors` on
each Step, and do not create a child Run per person. The full contract is
`ref/structure-run.md`. After the Structure Run closes, Section Runs use
`rp-sec-NN`, and fixed paragraph or paragraph-group Runs use
`rp-para-NN_Pxx[-Pyy]`.
`rp-struct-02` and later ids are reserved for a genuinely independent
post-closure structural goal, not for a Survey pass or a new participant.
Scratch is available once a selected Outline exists. It records a person's
rough thinking at Section (`C1`), Subsection/paragraph group (`C1.P1`); the B
rows are reading material only. Save keeps the Scratch Run open,
and a human-confirmed Summary closes it. Scratch does not edit `Draft:` prose
and does not replace the later Structure, Section, or Paragraph Run.
Human feedback advances Steps inside the selected Run's Version. A chat turn
or review window alone does not create another Run. A later independently
commissioned Section drafting/revision session does create a new `rp-sec-NN`
Run; a complete draft → review/rating → diagnose → revise cycle inside that
session is one Step, not a new Run. For a paragraph target, reopen the same
Run in a new Version when the target and goal remain fixed. `rp` means Run of
Page; its typed sequences are independent from one another and from the
native `rNN` sequence used by delegated Task Runs. New allocation uses only
the explicit kind tokens; retired compact identities remain readable history.
A mismatched kind or paragraph target is Held and cannot unlock later work.

If the closed index has `N` paragraphs, paragraph candidates satisfy
`1 <= K <= N`; the paragraph serial/range is recorded separately from the RP
sequence number.

When a person enters, continues, resumes, or asks to review an open Page Run
before giving feedback, return the pre-Step review packet from
`../../haipipe-page/ref/user-check-packet.md`: show the latest complete
candidate, the frozen Mermaid Structure description for each selected
paragraph, chat-only `S1...Sn` labels, the exact review scope, the proposed next
Step number, and the three direct workspace links. Do not append a new Step
until feedback, acceptance, or an explicit close arrives.

New interaction candidates are proposed through
`../../haipipe-page/fn/runs.md`. Proposal is read-only planning, not allocation:
it creates no typed RP identity, Ticket, Result, runtime receipt, or live Runs
row. After human selection, resume a matching open Page Run; otherwise allocate
the next typed RP only for a genuinely independent goal. A direct bounded feedback request is an
implicit selection and need not be proposed back to the person first.

While the current structure Run is open, resume it and show no Section or
paragraph candidates. After the structure contract closes, show unallocated
Section candidates and paragraph-group candidates in frozen `P01..PN` reading
order, but allocate only the selected next candidate from the matching kind.
Sequential work is the default; parallel Page Runs require explicit selection
and non-overlapping targets. If the plan changes, recompute unallocated
candidates only and never renumber an allocated typed RP.

Code, search, Discovery, data, rendering, build, and other independently
testable output work stays in the owner-native Task Run lane. A later human
acceptance gate does not convert the producing Task Run into a Page Run.

Use three commit boundaries during interactive work:

```text
Step            current candidate + dependent Bullets → live Draft Space
Page Run close  accepted paragraph group + explicit ready Evidence contract
Page release    all RP Runs + required RE Results → Content + RD delivery + CHECK
```

The foreground Step is deliberately small. Save the verbatim feedback, complete
candidate, affected Bullets, narrow source/protected-scope check, and current
Version/Step; then return the passage. Do not block it on a full build, complete
test suite, export, or browser verification. Evidence records change during a
Step only when the feedback changes a citation, value, or figure requirement.
For every material wording change, save clean Before/After text, a short local
change label, and why the edit was made. Do not infer a broader preference in
the foreground Step. The Runs presenter derives granular visual Track Changes;
neither diff markup nor an unconfirmed preference enters Page Content or shared
policy. Do not duplicate classification in a separate table; status,
navigation, acceptance-only, and presenter-only Steps use `Changes` without a
Track Changes card.

For ordinary follow-up wording feedback, use the rapid foreground budget:
reuse stable context already loaded in the session, read only `working.md`, the
latest saved-result tail, the exact target slice, and its dependent Bullet, then
make one bounded file patch and one narrow hash/scope check. Do not reread the
whole Page or Version, run `outline-pass.py`, rebuild the Board, run full tests,
verify the browser, or generate delivery before returning the current Step.
Keep the Step record complete but compact; broader preference synthesis and
whole-Page review wait for a checkpoint or an explicit request.

Each ordinary Step is record-first. It captures the person's feedback, performs
the requested edit, records a local reason, and returns the candidate. It does
not perform preference inference, taxonomy building, or whole-Run analysis.
After explicit Page Run closure, prepare one output-only post-run analysis
proposal according to `ref/post-run-analysis.md`. If it is heavy, ask for
explicit approval before dispatching it. Do not wait for approval or analysis
before starting the next Page Run, and never let it mutate the closed writing
record or Page Content. Follow `ref/interactive-execution-policy.md` for all
inter-Run and inter-Step work.

Closing one RP Run never adopts Content or builds delivery. It settles that
Run's text and Bullets and requires every Evidence obligation to be explicit
and ready (`none` or a bound CITE, VALUE, or DISPLAY Result). Required
Discovery, citation, figure, or computation work remains a Supporting Run
feeding an RE and must be ready before the RP becomes complete. CONTENT begins
only after every planned RP is complete and every required RE Result is bound;
one Page-level CONTENT pass then adopts all accepted candidates and commissions
the declared web/LaTeX/Word delivery through one or more `RD` Runs.

SHAPE and SURVEY remain planning cycles inside the one `rp-struct-01`, not one
Run each. They can be used inside this independently closable interactive Run.
`haipipe-writing`
owns prose revision; `haipipe-page-content` adopts agreed wording and builds
delivery. Do not redraft accepted paragraphs at that handoff. This protocol
uses agent-authored Markdown records; it adds no runtime service or UI controls.

## ⚡ The result

One Page Run Workflow is a directed graph of bounded Run Specs. The five labels
below are retained as a compact controller/API adapter projection; they
dispatch Run Specs and Workspaces, but they are not five Level-4 Run kinds or a
second semantic authority. A concrete Page may add, omit, branch, or repeat
Run Specs according to its declared Workflow Definition:

```text
00 CONTEXT     haipipe-page-context     PREPARE · Collect, Resolve, Freeze
01 OUTLINE     haipipe-page-outline     SHAPE · SURVEY
02 EVIDENCE    haipipe-page-evidence    LAND · EMBED
03 CONTENT     haipipe-page-content     WRITE · Adopt, Integrate, Build, Pre-check
04 CHECK       haipipe-page-check       CHECK · whole-Page close gate
```

`Outline` and `Content` align with the Page's two substantive Workspace
projections:
Outline holds the plan and the frequently revised candidate prose; Content is
the adopted Page text. Draft and Revise are writing movements, not separate
Run Specs. Interactive Steps and Page Run closures remain in Outline; after all
planned Page Run Instances and their required evidence are complete, one
Page-level CONTENT controller pass performs adoption and delivery.

Every user-facing completion after a Page-changing action follows
`../../haipipe-page/ref/user-check-packet.md`. Routine writing returns the
exact Run/Version/Step heading, saved selected paragraphs, a brief change
explanation, and three final Draft Space, Evidence Space, and Current Run links.
Formal delivery also provides current evidence surfaces and the Page-level PDF. Only the new `outline/evidence/display/`,
`outline/evidence/bibex/` and `delivery/latex/` lanes are eligible. The workflow receipt remains the audit record; it is not the primary
user-facing answer.

## 🧭 One Outline plugin serves three Workspaces

CONTEXT, OUTLINE, and EVIDENCE all use `haipipe-plugin-outline`:

```text
haipipe-plugin-outline
├── Draft Space          Mermaid + Bullet/Draft table; read-only projection
├── Evidence Space       typed Result cards; read-only projection
└── Run Space            Page Writing + Page Evidence + Supporting Runs
```

This is shared storage and presentation, not shared semantic authority. Context
records remain off-stage and are opened through Folder inspection. Never create
`haipipe-plugin-context` or a second Evidence plugin. The Run Spec owner skills write;
the plugin reads and presents.

## 🔁 Controller-label flow

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

The flow is a controller routing grammar, not a conveyor belt. CONTEXT reopens
when its authorities change; SHAPE and SURVEY may repeat inside the Structure
Run; LAND works item graphs in parallel; EMBED returns a `v0.*` fold to SHAPE
and a `G>=1` evidence fold to CONTENT; CONTENT may loop; CHECK may route to
any earlier authority. The labels shown in this diagram are dispatch/progress
coordinates only. The Run Spec graph and actual Run Instance receipts decide
what work exists and whether it can close.

## 📊 Run Spec × Workspace projections

The detailed map is `ref/workflow-table.md`. It is a Run Spec × Workspace
projection, not a controller-owned Run inventory. A controller-only row records
dispatch work without minting a Level-4 Run Instance.

| Run Spec or controller projection | Run Type | Bounded target / action | Actor | Entry / exit gate | Legal routes | Cardinality | Workspace projection | Controller labels |
|---|---|---|---|---|---|---:|---|---|
| controller/context | controller dispatch | resolve Page/Folder identity, policy, requirements, and fresh context | agent / hybrid | entry open; exit requires a resolved Context record or truthful HOLD | SELF / next dispatch, OUTLINE, HOLD | no Run Instance | Folder inspection and off-stage Context record | 00 CONTEXT / PREPARE |
| rp-struct-01 | page.interactive-writing.structure | whole-Page map, Mermaid, ordered Bullets, paragraph jobs, Point roles, typed Evidence Item decisions | human / agent / hybrid | entry open; exit requires accepted Shape + Survey contract | SELF / next Step, NEW_VERSION, CLOSE / next Run, NEW_RUN | exactly 1 initial Structure Run per Page | Draft, Evidence, and Run Spaces | 01 OUTLINE / SHAPE+SURVEY |
| rp-scratch-NN_<target> | page.interactive-writing.scratch | rough human thinking for Section, Subsection, or whole paragraph group; no B/symbol target | human | entry open; exit requires a non-empty human Summary | SELF / Save, CLOSE / Finish Scratch, NEW_RUN | 0..N per target | Draft Space Scratch view and Run Space | 01 OUTLINE / SCRATCH |
| rp-sec-NN | page.interactive-writing.section | one named Section's bounded candidate and review cycle | human / agent / hybrid | entry open; exit requires scoped acceptance and declared dependencies ready | SELF / next Step, NEW_VERSION, CLOSE / next Run, NEW_RUN | 0..S selected Section Runs | Draft Space and Run Space | 01 OUTLINE / SHAPE and 03 CONTENT / WRITE |
| rp-para-NN_Pxx[-Pyy] | page.interactive-writing.paragraph | one fixed paragraph or contiguous paragraph group | human / agent / hybrid | entry open; exit requires acceptance, settled Bullets, and ready evidence obligations | SELF / next Step, NEW_VERSION, CLOSE / next Run, NEW_RUN | 0..K, 1 <= K <= N | paragraph Draft Space, Evidence Space, Run Space | 01 OUTLINE / SHAPE and 03 CONTENT / WRITE |
| re-value-NN_<slug>, re-cite-NN_<slug>, re-display-NN_<slug> | page.evidence-item | one focal VALUE, CITE, or DISPLAY Result for one make-item | agent / automatic / hybrid | entry open; exit requires typed Result acceptance and any declared verification | SELF / next attempt, CLOSE / next Run, NEW_RUN, HOLD | exactly 1 Page RE per make-item, plus 0..N Supporting Runs | Evidence Space and paired Run/Result records | 02 EVIDENCE / LAND+EMBED |
| rdNN_<target> | page.delivery | one declared web, LaTeX, Word, or render delivery target | agent / automatic | entry open; exit requires build receipt and current artifact | SELF / next attempt, CLOSE / next Run, NEW_RUN, HOLD | one per declared delivery target | delivery projection and build receipt | 03 CONTENT / WRITE |
| controller/check | controller gate | judge one immutable built Page version and route the next authority | fresh agent / hybrid | entry open; exit is CLOSE or a named finding route | CLOSE, CONTEXT, OUTLINE, EVIDENCE, CONTENT, HOLD | no Run Instance | read-only Draft/Evidence/Run views plus check receipt | 04 CHECK / CHECK |

The formal API may serialize the controller labels as phase, cycle, and
next_cycle. Those names do not change the Run Type, Run Spec, Run Instance, or
Workspace semantics above.

## 🧱 Workflow orchestration and Run identity

The Page Run Workflow Definition/Runtime is the orchestration authority. A
Level-4 Run is one independently closable Ticket → Result attempt. A Run Spec
is the planned node that gives that Run its bounded target, actor, gates, routes,
skill binding, and Result contract:

```text
CONTEXT      adapter dispatch; Run Specs resolve planning inputs
SHAPE        inside shared rp-struct-01; it defines Bullet and Evidence Item contracts
SURVEY       inside shared rp-struct-01; it inventories/references/reserves the graph
LAND         Runs exist: Supporting Execution/Discovery/Insight, then one Page RE per item
EMBED        no Run; it interprets ready Results into the plan
CONTENT      after the Page release barrier, adopts all agreed Writing Results and commissions RD delivery
CHECK        no Run; it is a version gate
```

For interactive writing, `rp-struct-01` records the human exchange for the
closable Page map through both SHAPE and SURVEY; each sibling Page Run records
its own independently closable Section or paragraph-group goal. Planning or a
`fn/Runs` proposal alone still does not allocate a Run. A writing Version's
human closure is not the whole-Page CHECK/CLOSE verdict.

The two evidence layers are mandatory and named separately:

```text
Supporting Runs  0..N  Execution, Discovery, or accepted Insight item execution
                         ↓ Results
Local Input        1    one frozen envelope per Evidence Item
                         ↓
Page RE            1    Page · Evidence Item execution lineage
                         ↓
Typed Result       1    VALUE | CITE | DISPLAY
```

There is no active PageX binding layer. Cross-Folder evidence must enter
through a Supporting Run Result. A governed page-local static source may be
named and frozen in Local Input. Related Page links belong to Context
Workspace for navigation and constraints; they do not become evidence by
being linked.

## 🆔 Run references

Use full real addresses for reuse and rerun:

```text
global Supporting Run    b01j02t03r04
Task-local new-run plan  b01j02t03        parent until LAND allocates rNN
Task-local allocated     b01j02t03r05
Page Evidence lineage   re-cite-01_prior-work → owner-native Ticket/Result
Page Delivery lineage   rd01_web | rd02_latex | rd03_word | rd04_render
Other local Run plan     <owner-native parent or permitted reserved address> · plan
local Ticket filename    r05_page-evidence-item_e03-cite-prior-work
Delegated writing Task   r06_page-writing_c02-p01
Structure + Bullets      rp-struct-01 or rp-struct-02
Section-level writing    rp-sec-01 or rp-sec-02
Paragraph-level writing  rp-para-01_P03 or rp-para-02_P04-P05
```

SURVEY names the real owner/parent for every new local route. The Page's RE or
RD is the stable Page-local lineage identity; any underlying owner-native
Ticket/Result keeps its own naming contract. A full address may be reserved
only when that owner contract permits it; the route remains `new-run` with no
Ticket. LAND allocates the owner-native Run id and records it under the RE/RD
lineage. The interactive workflow creates
the structure/Bullet Run first, then a Section-level or paragraph-level Page Run
for each selected writing scope;
CONTENT consumes its accepted output.
Those allocations do not consume one another's counters: RP, RE, RD, and Task
Run `rNN` sequences are independent. Task or Discovery identities are never
rewritten with an `rp`, `re`, or `rd` prefix.
The single-paragraph delegated profile remains available when explicitly selected.

## 🧠 Exact skill routing

For every Run Workflow dispatch, record exact owner names rather than generic labels:

```text
haipipe-page-workflow
  → current Run Workflow / Run Spec owner skill
  → Folder-owning workflow or canonical family skill
  → exact Page Face owner skill
  → exact narrative/style/outline policy skill, when applicable
  → haipipe-run + worker skills, only when the Run Spec commissions Runs
```

For the first three planning dispatches, append the exact
`haipipe-plugin-outline/ref/...` material contracts needed by the Run Spec; do
not append the presenter skill as an execution dependency.

Example for a paper Section Shape:

```text
haipipe-page
  → haipipe-page-workflow
  → haipipe-page-outline
  → haipipe-paper-workflow
  → haipipe-paper-section
  → haipipe-paper-story             (the §8 Section Narrative row the Section executes)
  → haipipe-plugin-outline/ref/plan-grammar.md
  → haipipe-plugin-outline/ref/item-table.md
```

Do not insert a separate Task Page-Type layer. `haipipe-task` is both canonical
Folder owner and Page Face owner for a Task Folder, so load it once. Also load
its `haipipe-page-task` reader-facing companion for the Task Page's display
and prose requirements; this companion adds no execution or closure authority.

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
CONTEXT   haipipe-page-context-agent    producer
OUTLINE   haipipe-page-outline-agent    producer
EVIDENCE  haipipe-page-evidence-agent   producer
CONTENT   haipipe-page-content-agent    producer
CHECK     haipipe-page-check-agent      fresh read-only judge
builder   separate mechanical actor     build/check/hash only
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
| plan `approved:` | SHAPE when the person wants a durable plan tick; for the interactive Page profile, an explicit user next-step instruction is sufficient for CONTENT |
| per-item `Decide` | SURVEY; branching choice, never auto-deferred |
| CITE item `Verified` and any worker-specific verification | LAND |
| Page/display `accepted:` and Folder ruling | CHECK |

No machine writes a person's act. An auto run may continue under the declared
policy while a review tick is owed, but it must HOLD at SURVEY when `Decide`
is unsigned; a prior explicit durable decision/default policy may be consumed,
never invented. `page_ruling: none | domain-gate | local` comes from the
Folder-owning workflow. Do not invent a duplicate Page gate.

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
`../../../board/haipipe-board/ref/page-lifecycle.workflow.js`. The deterministic
auditor is `../../../board/haipipe-board/src/page_lifecycle.py`.

## 🧾 Receipts and terminal states

Every controller dispatch appends one receipt with the serialized `phase`
RunType label, cycle, actor, role,
source/render versions, route, reason, artifacts, evidence, findings, and
human-gate pointer. Dispatch receipts are workflow audit records; they are not
Level-4 Runs or Results.

Only CHECK may emit `CLOSE`. `HOLD` preserves a named missing input, conflict,
failed work, unresolved gate, concurrency mismatch, or exhausted bound. A
route name without a reason and owning authority is invalid.

Audit the durable bundle with:

```bash
python3 <haipipe-board>/cli/pageflow.py audit <board>/_runs/page/<page-id>/<run-id>.json
```

## 📂 Files

```text
haipipe-page-workflow/
├── SKILL.md
├── CHANGELOG.md
└── ref/
    ├── interactive-writing-run.md  persistent human-feedback Run protocol
    ├── writing-step-template.md    original input, full output, scoped decisions
    ├── workflow-table.md       canonical design/adoption table
    ├── phase-cards.md          physically named compact Run Spec cards
    ├── ../../haipipe-page/ref/page-run-families.md  RP/RE/RD and evidence bindings
    ├── page-run-contract.md    packet, receipts, legal routes, adapter mapping
    ├── producer-contract.md    shared Run worker packet and return
    └── measured-cost.md        prior measured dispatch costs
```
