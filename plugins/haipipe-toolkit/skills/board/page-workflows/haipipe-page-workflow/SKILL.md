---
name: haipipe-page-workflow
description: >-
  The Page workflow router: 00 CONTEXT/PREPARE, 01 OUTLINE/SHAPE+SURVEY,
  02 EVIDENCE/LAND+EMBED, 03 CONTENT/WRITE, and 04 CHECK. It selects the
  exact phase skill, Page Type, policy, Outline workspace, Level-4 Run graph,
  legal backward route, and auditable receipt for one persistent Page. Use to
  design, run, resume, or audit the complete Page lifecycle. Trigger: Page
  workflow, workflow table, run a page, page phase, SHAPE SURVEY LAND EMBED,
  page context, page content, /haipipe-page-workflow.
metadata:
  version: "0.26.1"
  last_updated: "2026-09-04"
  # version history: ./CHANGELOG.md
---

# /haipipe-page-workflow · route one persistent Page by authority

Load every Page phase through one canonical order:

```text
haipipe-page
  → haipipe-page-workflow
  → current phase skill
  → Folder-owning workflow skill
  → exact Page Type skill
  → phase references and narrative/style policy
  → haipipe-run + selected workers, only when this phase commissions Runs
  → haipipe-plugin-outline, for CONTEXT/OUTLINE/EVIDENCE presentation
```

Resolve the Folder's owning workflow and exact Page Type before acting. Load
only the current phase references and the workers for Runs it actually
commissions. A phase skill may abbreviate this chain, but it may not reorder
authority or omit the Page Type.

For an in-place Folder, the authoritative `workflow/phase.yaml` resolves the
owning workflow and Folder kind before Page frontmatter or legacy names. The
current evidence graph never creates a new `probe/` lane; an old lane is
read-only migration input. Legacy outbound-card history is read-only.

The full canonical table is `ref/workflow-table.md`; the compact phase cards
are `ref/phase-cards.md`; the executable packet/receipt law is
`ref/page-run-contract.md`.

## ⚡ The result

One Page has five numbered phases. The three middle phases make the Page; the
front phase prepares their context and the last phase judges their result:

```text
00 CONTEXT     haipipe-page-context     PREPARE · Collect, Resolve, Freeze
01 OUTLINE     haipipe-page-outline     SHAPE · SURVEY
02 EVIDENCE    haipipe-page-evidence    LAND · EMBED
03 CONTENT     haipipe-page-content     WRITE · Draft, Revise, Build, Pre-check
04 CHECK       haipipe-page-check       CHECK · whole-Page close gate
```

`Outline` and `Content` align with the Page's two substantive structures:
Outline plans what the Page will say; Content is what it says. Draft and
Revise are no longer Page phases. They are movements inside CONTENT/WRITE.

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
                       │ plan v<N+1>
                       └──────────▶ SHAPE re-approval
                                        │ approved + all make-items folded
                                        ▼
                                  CONTENT/WRITE
                                        │ exact built version
                                        ▼
                                  CHECK/CHECK ──▶ CLOSE
                                      │
                                      └─ route to the authority that owns a finding
```

The flow is a routing grammar, not a conveyor belt. CONTEXT reopens when its
authorities change; SHAPE and SURVEY may repeat; LAND works item graphs in
parallel; EMBED always returns to SHAPE; CONTENT may loop; CHECK may route to
any earlier owning phase.

## 📊 Canonical workflow table

| Index | Phase / cycle | Primary skill | Main L3 write | Level-4 Runs | Exit |
|---:|---|---|---|---|---|
| `00` | CONTEXT / PREPARE | `haipipe-page-context` | `outline/<stem>-context.md` | none | context resolved and fresh |
| `01A` | OUTLINE / SHAPE | `haipipe-page-outline` | plan + Evidence Item specification | none | approved evidence-aware Shape |
| `01B` | OUTLINE / SURVEY | `haipipe-page-outline` | Supporting routes + Local Input + indexed Local Run plan | none | complete decided Run graph |
| `02A` | EVIDENCE / LAND | `haipipe-page-evidence` | Tickets, Results, frozen input, bindings | `0..N` Supporting + `1` local per make-item | accepted typed local Results |
| `02B` | EVIDENCE / EMBED | `haipipe-page-evidence` | plan v<N+1> bindings | none | all ready Results folded; back to SHAPE |
| `03` | CONTENT / WRITE | `haipipe-page-content` | Page Content + delivery + promotion trace | normally `1` Division Writing Run per commissioned division | fresh pre-check says ready |
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
LAND         Runs exist: Supporting Execution/Discovery, then local Evidence Item
EMBED        no Run; it interprets ready Results into the plan
CONTENT      Division Writing Runs exist when divisions are independently closable
CHECK        no Run; it is a version gate
```

The two evidence layers are mandatory and named separately:

```text
Supporting Runs  0..N  Execution or Discovery
                         ↓ Results
Local Input        1    one frozen envelope per Evidence Item
                         ↓
Local Run          1    Page · Evidence Item
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
Paper-local Run plan     pj01t03r01     shown as P j01.t03.r01 plan
allocated local Run      r04_page-evidence-item_e03-cite-prior-work
Division Writing Run     r05_page-division-writing_c02
```

SURVEY may reserve the Paper-local address but creates no Ticket. LAND creates
the Evidence Item Ticket. CONTENT creates a Division Writing Ticket only when
the work independently satisfies the `haipipe-run` tests.

## 🧠 Exact skill routing

For every phase, record exact names rather than generic labels:

```text
haipipe-page-workflow
  → current phase skill
  → Folder-owning workflow skill
  → exact Page Type skill
  → exact narrative/style/outline policy skill, when applicable
  → haipipe-run + worker skills, only when the phase commissions Runs
  → haipipe-plugin-outline, when presenting Context/Outline/Evidence
```

Example for a paper Section Shape:

```text
haipipe-page-workflow
  → haipipe-page-outline
  → haipipe-paper-section
  → haipipe-paper-narrative
  → haipipe-plugin-outline/ref/plan-grammar.md
```

Do not restore `haipipe-page-for-task`; the Folder-owning workflow and Page
Type supply their own Page contract.

## 🔀 Route by broken authority

| Finding | Route |
|---|---|
| Page/Folder identity, policy, requirements, related context, or context freshness | CONTEXT |
| argument, division shape, Bullet contract, item expectation, or Aim promise | OUTLINE |
| Supporting/local evidence graph, input, Result, acceptance, or fold freshness | EVIDENCE |
| prose realization, citations in prose, caption, build, or division promotion | CONTENT |
| exact built version needs independent judgment | CHECK |
| all closing rules and human gates pass | CLOSE, from CHECK only |
| required authority/input cannot safely resolve | HOLD |

Legal current-phase routes:

```text
CONTEXT  → CONTEXT | OUTLINE | HOLD
OUTLINE  → CONTEXT | OUTLINE | EVIDENCE | CONTENT | HOLD
EVIDENCE → CONTEXT | OUTLINE | EVIDENCE | HOLD
CONTENT  → CONTEXT | OUTLINE | EVIDENCE | CONTENT | CHECK | HOLD
CHECK    → CLOSE | CONTEXT | OUTLINE | EVIDENCE | CONTENT | HOLD
```

Stored DRAFT, REVISE, COMPILE, and PROBE receipts remain auditable through
the compatibility rules in `ref/page-run-contract.md`; new dispatch never
emits those phases.

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
auto      plugin acts defer to the owed ledger; an explicit stop still wins
```

The acts remain at their authorities:

| Act | Owner |
|---|---|
| plan `approved:` | SHAPE |
| per-item `Decide` | SURVEY |
| worker-specific verification | LAND worker |
| Page/display `accepted:` and Folder ruling | CHECK |

No machine writes a person's act. `page_ruling: none | domain-gate | local`
comes from the Folder-owning workflow. Do not invent a duplicate Page gate.

## 🔁 Run one Page lifecycle

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
`../../haipipe-board/ref/page-lifecycle.workflow.js`. The deterministic
auditor is `../../haipipe-board/src/page_lifecycle.py`.

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
    ├── workflow-table.md       canonical design/adoption table
    ├── phase-cards.md          compact six-field operating cards
    ├── page-run-contract.md    packet, receipts, legal routes, compatibility
    ├── producer-contract.md    shared phase-agent packet and return
    └── measured-cost.md        prior measured dispatch costs
```
