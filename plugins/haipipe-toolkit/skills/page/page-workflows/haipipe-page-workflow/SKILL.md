---
name: haipipe-page-workflow
description: >-
  The Page workflow router: 00 CONTEXT/PREPARE, 01 OUTLINE/SHAPE+SURVEY,
  02 EVIDENCE/LAND+EMBED, 03 CONTENT/WRITE, and 04 CHECK. Owns persistent
  human-feedback Writing Runs across planning and prose iteration. It selects the
  exact phase skill, Page Face owner, policy, Outline workspace, Level-4 Run graph,
  legal backward route, and auditable receipt for one persistent Page. Use to
  design, run, resume, or audit the complete Page lifecycle. Trigger: Page
  workflow, workflow table, run a page, page phase, SHAPE SURVEY LAND EMBED,
  page context, page content, /haipipe-page-workflow.
metadata:
  version: "0.54.0"
  last_updated: "2026-09-13"
  # version history: ./CHANGELOG.md
---

# /haipipe-page-workflow · route one persistent Page by authority

Load every Page phase through one canonical order:

```text
haipipe-page
  → haipipe-page-workflow
  → current phase skill
  → Folder-owning workflow or canonical family skill
  → Page Face owner skill
  → phase references and narrative/style policy
  → haipipe-page/ref/page-run-families.md when naming RP, RE, or RD
  → haipipe-run + selected workers, only when this phase commissions Runs
```

Resolve the Folder owner and Page Face owner before acting. A Page Face owner
is the exact workflow-phase skill, canonical family skill, or unmigrated Page
Type skill that owns this Folder's readable contract; load it only once when it
is also the Folder owner. Load
only the current phase references and the workers for Runs it actually
commissions. For CONTEXT, OUTLINE, and EVIDENCE those references live under
`haipipe-plugin-outline`; the Page surface has already installed that plugin
as the shared presenter. A phase skill may abbreviate this chain, but it may
not reorder authority or omit the Page Face owner.

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

For an in-place Folder, the authoritative `workflow/phase.yaml` resolves the
owning workflow and Folder kind before Page frontmatter or legacy names. The
current evidence graph never creates a new `probe/` lane; an old lane is
read-only migration input. Legacy outbound-card history is read-only.

The full canonical table is `ref/workflow-table.md`; the compact phase cards
are `ref/phase-cards.md`; the executable packet/receipt law is
`ref/page-run-contract.md`.

## 🤝 Interactive writing first

For collaborative drafting or feedback-led revision, load
`ref/interactive-writing-run.md` and its `ref/writing-step-template.md` before
editing. One Page owns many sibling Page Runs. The first Run is always
`rp00_mermaid-structure`, where human and agent iterate on the whole-Page
Mermaid argument map and Page-global `P01..PN` paragraph index until explicit closure.
Only then may the `N` numbered paragraphs be partitioned into `K`
independently reviewable groups, where `1 <= K <= N`. Each selected group uses
the short identity `rpNN_pNN[-pNN]` and one independently closable human
question. Human feedback advances Steps inside that Run's Version. A new chat
session or review window does not create another Run. Ordinary waiting for
feedback is not a failure, and local edits do not invoke the complete phase
controller. Reserve `rp00` for that structure Run, then allocate paragraph Page
Runs as `rp01`, `rp02`, and so on. `rp` means Run of Page; its counter is
independent from the native `rNN` sequence used by delegated Task Runs.
No earlier spelling is accepted: a noncanonical `interactive-writing`
identity is Held and cannot stand in for `rp00` or a paragraph Run.

When a person enters, continues, resumes, or asks to review an open Page Run
before giving feedback, return the pre-Step review packet from
`../../haipipe-page/ref/user-check-packet.md`: show the latest complete
candidate, the frozen Mermaid Structure description for each selected
paragraph, chat-only `S1...Sn` labels, the exact review scope, the proposed next
Step number, and the three direct workspace links. Do not append a new Step
until feedback, acceptance, or an explicit close arrives.

New interaction candidates are proposed through
`../../haipipe-page/fn/runs.md`. Proposal is read-only planning, not allocation:
it creates no `rpNN`, Ticket, Result, runtime receipt, or live Runs row. After
human selection, resume a matching open Page Run; otherwise allocate `rpNN`
only for a genuinely independent goal. A direct bounded feedback request is an
implicit selection and need not be proposed back to the person first.

While `rp00_mermaid-structure` is open, resume it and show no paragraph candidates. After
it closes, show all unallocated paragraph-group candidates in frozen `P01..PN`
reading order, but allocate only the selected next candidate. Sequential work is the default; parallel
Page Runs require explicit selection and non-overlapping targets. If the plan
changes, recompute unallocated candidates only and never renumber an allocated
`rpNN`.

Code, search, Discovery, data, rendering, build, and other independently
testable output work stays in the owner-native Task Run lane. A later human
acceptance gate does not convert the producing Task Run into a Page Run.

Use three commit boundaries during interactive work:

```text
Step            current candidate + dependent Bullets → live Bullet Workspace
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

SHAPE and SURVEY remain planning capabilities, not one Run each. They can be
used inside this independently closable interactive Run. `haipipe-writing`
owns prose revision; `haipipe-page-content` adopts agreed wording and builds
delivery. Do not redraft accepted paragraphs at that handoff. This protocol
uses agent-authored Markdown records; it adds no runtime service or UI controls.

## ⚡ The result

One Page has five numbered phases. The three middle phases make the Page; the
front phase prepares their context and the last phase judges their result:

```text
00 CONTEXT     haipipe-page-context     PREPARE · Collect, Resolve, Freeze
01 OUTLINE     haipipe-page-outline     SHAPE · SURVEY
02 EVIDENCE    haipipe-page-evidence    LAND · EMBED
03 CONTENT     haipipe-page-content     WRITE · Adopt, Integrate, Build, Pre-check
04 CHECK       haipipe-page-check       CHECK · whole-Page close gate
```

`Outline` and `Content` align with the Page's two substantive structures:
Outline holds the plan and the frequently revised candidate prose; Content is
the adopted Page text. Draft and Revise are writing movements, not separate
phases. Interactive Steps and Page Run closures remain in Outline; after all
planned Page Runs and their required evidence are complete, one Page-level
CONTENT pass performs adoption and delivery.

Every user-facing completion after a Page-changing action follows
`../../haipipe-page/ref/user-check-packet.md`. Routine writing returns the
exact Run/Version/Step heading, saved selected paragraphs, a brief change
explanation, and three final Bullet Workspace, Evidence Workspace,
and Current Run links.
Formal delivery also provides current evidence surfaces and the Page-level PDF. Only the new `outline/evidence/display/`,
`outline/evidence/bibex/` and `delivery/latex/` lanes are eligible. The workflow receipt remains the audit record; it is not the primary
user-facing answer.

## 🧭 One Outline plugin serves three phases

CONTEXT, OUTLINE, and EVIDENCE all use `haipipe-plugin-outline`:

```text
haipipe-plugin-outline
├── Context Workspace    CONTEXT prepares; every later phase reads
├── Bullet Workspace     OUTLINE shapes; EVIDENCE embeds into the plan
└── Evidence Workspace   OUTLINE surveys; EVIDENCE lands Results
```

This is shared storage and presentation, not shared semantic authority. Never
create `haipipe-plugin-context` or a second Evidence plugin. The phase skills
write; the plugin reads and presents.

## 🔁 Complete flow

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

The flow is a routing grammar, not a conveyor belt. CONTEXT reopens when its
authorities change; SHAPE and SURVEY may repeat; LAND works item graphs in
parallel; EMBED returns a `v0.*` fold to SHAPE and a `G>=1` evidence fold to
CONTENT; CONTENT may loop; CHECK may route to
any earlier owning phase.

## 📊 Canonical workflow table

| Index | Phase / cycle | Primary skill | Main L3 write | Level-4 Runs | Exit |
|---:|---|---|---|---|---|
| `00` | CONTEXT / PREPARE | `haipipe-page-context` | `outline/<stem>-context.md` | none | context resolved and fresh |
| `01A` | OUTLINE / SHAPE | `haipipe-page-outline` | plan + Evidence Item specification | none | approved evidence-aware Shape |
| `01B` | OUTLINE / SURVEY | `haipipe-page-outline` | Supporting routes + Local Input + indexed RE plan | none | complete decided Run graph |
| `02A` | EVIDENCE / LAND | `haipipe-page-evidence` | Tickets, Results, frozen input, bindings | `0..N` Supporting + `1` RE per make-item | ready typed local Results/Cards |
| `02B` | EVIDENCE / EMBED | `haipipe-page-evidence` | next working plan bindings | none | ready Results folded; `G=0` returns to SHAPE; `G>=1` may route to CONTENT only for a pure evidence revision or an explicit CONTENT instruction after all remaining gates are named |
| `03` | CONTENT / WRITE | `haipipe-page-content` | all agreed prose → Page Content + RD delivery + adoption trace | enters once all RP Runs and required RE Results are complete | fresh pre-check says ready |
| `04` | CHECK / CHECK | `haipipe-page-check` | check receipt/findings only | none | CLOSE or a named backward route |

Do not use this compact table for design decisions. Use
`ref/workflow-table.md`, which also records required inputs, exact skill chain,
Outline workspace, L3 mutations, L4 cardinality, outputs, and handoffs.

## 🧱 Planning and Runs stay different

The Page workflow phase is Level 3 authority. A Level-4 Run is one independently
closable Ticket → Result attempt:

```text
CONTEXT      no Run; it resolves planning inputs
SHAPE        no Run; it defines Bullet and Evidence Item contracts
SURVEY       no Run; it inventories/references/reserves the graph
LAND         Runs exist: Supporting Execution/Discovery/Insight, then one Page RE per item
EMBED        no Run; it interprets ready Results into the plan
CONTENT      after the Page release barrier, adopts all agreed Writing Results and commissions RD delivery
CHECK        no Run; it is a version gate
```

For interactive writing, each sibling Page Run records the human exchange for
its independently closable Plan/map or paragraph-group goal; planning or a
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
Page Evidence lineage   re01_e03-cite-prior-work → owner-native Ticket/Result
Page Delivery lineage   rd01_web | rd02_latex | rd03_word | rd04_render
Other local Run plan     <owner-native parent or permitted reserved address> · plan
local Ticket filename    r05_page-evidence-item_e03-cite-prior-work
Delegated writing Task   r06_page-writing_c02-p01
Mermaid Structure        rp00_mermaid-structure
Interactive paragraph    rp01_p01 or rp02_p02-p03
```

SURVEY names the real owner/parent for every new local route. The Page's RE or
RD is the stable Page-local lineage identity; any underlying owner-native
Ticket/Result keeps its own naming contract. A full address may be reserved
only when that owner contract permits it; the route remains `new-run` with no
Ticket. LAND allocates the owner-native Run id and records it under the RE/RD
lineage. The interactive workflow creates
`rp00_mermaid-structure` first, then one `rpNN_pNN[-pNN]` Page Run for each selected
paragraph group;
CONTENT consumes its accepted output.
Those allocations do not consume one another's counters: RP, RE, RD, and Task
Run `rNN` sequences are independent. Task or Discovery identities are never
rewritten with an `rp`, `re`, or `rd` prefix.
The single-paragraph delegated profile remains available when explicitly selected.

## 🧠 Exact skill routing

For every phase, record exact names rather than generic labels:

```text
haipipe-page-workflow
  → current phase skill
  → Folder-owning workflow or canonical family skill
  → exact Page Face owner skill
  → exact narrative/style/outline policy skill, when applicable
  → haipipe-run + worker skills, only when the phase commissions Runs
```

For the first three phases, append the exact
`haipipe-plugin-outline/ref/...` material contracts needed by the phase; do
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

Legal current-phase routes:

```text
CONTEXT  → CONTEXT | OUTLINE | HOLD
OUTLINE  → CONTEXT | OUTLINE | EVIDENCE | CONTENT | HOLD
EVIDENCE → CONTEXT | OUTLINE | EVIDENCE | CONTENT | HOLD
CONTENT  → CONTEXT | OUTLINE | EVIDENCE | CONTENT | CHECK | HOLD
CHECK    → CLOSE | CONTEXT | OUTLINE | EVIDENCE | CONTENT | HOLD
```

The EVIDENCE → CONTENT edge is only for a pure EMBED under an approved G>=1
Shape. Stored retired-phase receipts are read-only input under
`ref/page-run-contract.md#legacy-compatibility-only`.

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

This bounded controller is for phase dispatch and formal completion, not the
human-feedback journal. Its `step`, limits, `HOLD` and `CLOSE` do not count or
terminate interactive writing Steps/Versions. Finish a chat turn while waiting;
resume from the Writing Run files when new feedback arrives.

The `/run` spelling is a compatibility command verb. The durable controller
bundle is a **Page workflow pass**, not a Page Run. Reserve the Page Run noun
for `family: page`, `operation: interactive-writing`, whose Version/Step history
is owned by the Page and shown in the Page Runs lane.

The packet minimally names:

```yaml
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
- an existing Page with a known stale authority begins at that phase;
- an existing Page with unknown next need begins at CHECK, whose judge routes
  it without editing;
- a Page may skip evidence work only when SHAPE owes no make-item.

The executable controller is
`../../../board/haipipe-board/ref/page-lifecycle.workflow.js`. The deterministic
auditor is `../../../board/haipipe-board/src/page_lifecycle.py`.

## 🧾 Receipts and terminal states

Every attempted phase appends one receipt with phase, cycle, actor, role,
source/render versions, route, reason, artifacts, evidence, findings, and
human-gate pointer. Phase receipts are workflow audit records; they are not
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
    ├── phase-cards.md          compact six-field operating cards
    ├── ../../haipipe-page/ref/page-run-families.md  RP/RE/RD and evidence bindings
    ├── page-run-contract.md    packet, receipts, legal routes, compatibility
    ├── producer-contract.md    shared phase-agent packet and return
    └── measured-cost.md        prior measured dispatch costs
```
