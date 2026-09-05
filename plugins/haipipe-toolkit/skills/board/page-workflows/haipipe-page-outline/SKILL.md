---
name: haipipe-page-outline
description: >-
  The 01 OUTLINE phase of a Board Page. Treats the addressed Bullet as the
  primary plan-evidence-content unit:
  two planning cycles, SHAPE (brief → propose → react → revise; name every typed
  Evidence Item, compact Label, and expected ready payload) and SURVEY (inventory zero-to-many
  Execution/Discovery Supporting Runs, one Local Input, and exactly one local
  Page Evidence Item Run declaration). Writes the versioned plan,
  Evidence Item table, open threads and log;
  records evidence-to-Run lineage but allocates no Ticket and executes no material. Trigger: page outline, OUTLINE
  phase, shape the plan, survey the evidence items, evidence item table, review,
  check, read, or approve the outline, fold evidence into the plan,
  /haipipe-page-outline.
metadata:
  version: "0.25.0"
  last_updated: "2026-09-04"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-outline · SHAPE the plan, then SURVEY what it owes

Enter through the canonical Page chain, in order:

```text
haipipe-page
  → haipipe-page-workflow
  → haipipe-page-outline
  → the exact Folder-owning workflow or canonical family skill
  → the exact Page Face owner skill
  → the exact narrative/style policy, when applicable
  → haipipe-plugin-outline/ref/plan-grammar.md
  → haipipe-plugin-outline/ref/item-table.md
  → haipipe-plugin-outline/ref/review-packet.md (only for a human review or approval)
  → haipipe-run + selected workers (SURVEY inventory only; no dispatch)
```

The Page surface has already installed `haipipe-plugin-outline` as the shared
presenter. The refs above are this phase's schema/material dependencies; the
presenter skill is not another execution step.

The current `haipipe-page-context` PREPARE record must be fresh before this
chain acts. The Folder owner and Page Face owner supply the Page's
outline/narrative/style policy.
Do not route through a separate Task Page-Type layer. The owning workflow or
canonical family skill already supplies the Page contract. For a Task Folder,
`haipipe-task` fills both owner roles and is loaded once. Load no sibling Page
and no board-wide checker output before reading the target Page.

The Page workflow gives OUTLINE two planning cycles. Its sibling
`haipipe-page-evidence` owns LAND and EMBED; `haipipe-page-content` owns the
later WRITE cycle. All governing context must first be resolved by
`haipipe-page-context`.

The reader sees these authorities through one Outline plugin with three
workspaces: **Context Workspace** for governing inputs, **Bullet Workspace**
for the plan, and **Evidence Workspace** for what each Bullet needs.
Requirement, Discussion, Feedback, Files, Log, and Skills remain separate
records on disk but appear together inside Context Workspace. None is copied
back into `page.md`.

Both the main Page and the Outline plan card expose the same compact numbered
workflow strip: `1 SHAPE  2 SURVEY  3 LAND  4 EMBED`, with the current cycle
highlighted. Arrow notation describes phase flow, not literal UI separators.
The planning surface does not show a Shape-versus-Content mismatch alarm;
Content may correctly be empty before EMBED/CONTENT. Any structural mismatch
that matters is evaluated by the owning phase's checker at its boundary.

```text
OUTLINE part
  SHAPE    this file    plan + typed item expectation          👤 approved:
  SURVEY   this file    classify supports + Local Input + Local Run    👤 Decide, per item
  LAND     evidence     allocate planned routes, execute → Result     ⚙ every make-item ready
  EMBED    evidence     fold ready Results into next working plan vN.<k+1> ⚙ back to SHAPE
```

## 🧱 Bullet · the Outline's primary unit

A **Bullet** is one planned reader move with a stable `C<n>.P<m>.B<k>` address.
It is smaller than a paragraph and more durable than a sentence: a Section Page
normally realizes one Bullet as one sentence, while another Page type may use
one or more sentences. Its head names the job the prose must do, not the final
prose itself.

```text
Bullet
├── Address       stable C.P.B identity
├── Head          planned reader move
├── Note          bounded rationale or constraint
├── Evidence      zero-to-many typed Evidence Items
└── Realization   CONTENT-written Page sentence(s), linked with realizes:
```

The Bullet is the shared unit across Bullet Workspace and Evidence Workspace.
SHAPE revises its intended move; SURVEY maps what supports it without changing
its meaning; LAND and EMBED return ready material; CONTENT alone writes its Page
prose. Evidence Items serve a Bullet—they do not become competing outline rows.

## ⚡ Brief

```text
Q        what will this page say, division by division, bullet by bullet;
         what does each bullet owe; and where in tasks/ does each owed thing
         come from?
READS    outline/<stem>-requirement.md (V1 to V4) · outline/<stem>-feedback.md
         (open rows) · outline/<stem>-evidence.md (the table joined to the
         disk) · the owning workflow phase's outline policy · the page · the current plan ·
         the project's Execution/Discovery Run inventories (SURVEY only) ·
         outline/<stem>-context.md · outline/skill/<stem>.md when present
WRITES   outline/<stem>-outline-v<N>.<k>.md · outline/<stem>-evidence-items.md ·
         outline/<stem>-discussion.md (D<nn>) · outline/<stem>-log.md (one
         record) · outline/evidence/supporting-runs/<stem>-run-bindings.md
         (generated pointers) · never the page
CHECKS   ⓪ ARC ① COVERAGE ② ADDRESS ③ VALUE ④ SHAPE, all pass before the
         person is asked (SHAPE); every make-item has an audited Supporting/Local
         Run map, one explicit Local Input, and one decision (SURVEY)
ENDS     SHAPE: copilot records a person's approved: tick; auto may record the
         owed review and follow the declared gate policy · SURVEY: every row
         has an explicit durable make/defer/drop decision
WALLS    writes no prose · raises no card · executes nothing and lands no Result ·
         mints no Aim · names no division the type refuses · ticks nothing ·
         changes a ✅ vN.0 plan only as working revision vN.1 · never writes a Status word
ROUTES   SHAPE → SURVEY (agreed or auto-forwarded, marks owed) · SHAPE → CONTENT
         (evidence-aware and allowed forward) · SURVEY → LAND (every item graph classified) ·
         either → SHAPE again · HOLD (copilot waits, or a real input/stop blocks auto)
RECEIPT  §🧾, one block per pass, `cycle: SHAPE | SURVEY`; field law:
         ../haipipe-page-workflow/ref/page-run-contract.md §Receipt step
```

## ⓪ Boot · load little, trust the plan

- **Load**: this brief, the owning workflow phase's outline policy (`fixed` lists the
  divisions · `grammar` fixes a first-word set and an order rule · `resolved`
  points at a source outside the type · no key means the base section order),
  `ref/plan-grammar.md`, the page, the generated Context record, and the other
  process records under `outline/`. A missing, stale, or conflicting required
  Context row routes to CONTEXT before SHAPE or SURVEY continues. The
  policy sits in the phase skill's contract, which the Skill
  tool strips: read the file's first 20 lines with the Read tool. Read the
  page once, with the Read tool; a page piped through `cat` into a persisted
  output is read twice.
- **Trust the plan's `Answered:` and `Drawn:` lines as written.** Re-read only
  a card whose line ends `· recount` (it counts the run's own artifacts), plus
  one spot-check; a mismatch there means the plan is stale, and the route is
  this phase again, never a quiet correction.
- **In session or as an agent, the trace is the same**: the plan file (or the
  table), the log record, the receipt. `haipipe-page-outline-agent` runs the
  pass in a fresh context when the RUN loop dispatches it; a pass typed in a
  person's own session (the 🎨 Studio chat) is equally a pass.

## 🧩 SHAPE · brief → propose → react → revise, until the shape is agreed

The cycle where the human and the AI shape the plan together. Named for what
BOTH sides do; it ends when the shape is agreed, never earlier.

```text
1 BRIEF     the person says the narrative in a few lines: what this page must argue
2 PROPOSE   the AI writes plan v0.1 from the brief + owning phase policy + venue;
            every owed thing is a named typed Evidence Item with Label + Expected + Accept
3 REACT     the person reads the rendered plan on the 🧭 tab: ticks, comments, redirects
4 REVISE    the AI folds each material human-facing revision into v0.2, v0.3, …
loop 3 ⇄ 4 until the person ticks approved:
```

The first channel approval copies the selected `v0.<k>` plan into frozen
`v1.0`. After an approved baseline `vN.0`, the same loop uses `vN.1`,
`vN.2`, … . A later channel approval copies the selected revision into the
next frozen agreement `v<N+1>.0`; a frozen `.0` is never minted before that
approval. Mechanical repairs needed to make one proposed revision pass its
checks stay in place and do not consume another minor number.

Steps 2 and 4 are the chat's verbs (`propose`, `revise`); step 3 is the person
on the 🧭 tab. "Draft" and "Brief" are not cycle names: Draft is an internal
movement of the later CONTENT/WRITE phase, while Brief is SHAPE input.

### ① Prepare · one command runs the mechanical half

```bash
python3 <haipipe-board>/cli/outline-pass.py <page>.md
```

It regenerates the three derived files, runs the plan checks for this page
(hard), runs `cli/check.py` scoped to the page, rebuilds the board (skip with
`--no-build`) and prints a receipt-lite. Run it TWICE: once before the plan is
written, to read; once after, to measure, because the counts and the checks
describe the plan on disk. The log record is written after the second run, so
its folded receipt carries measured numbers:

```text
requirement  V1 Shape · V2 Size · V3 Refused · V4 Moves   read before a bullet is written
feedback     n routed · n open · n served · n declined     an open row is served or declined this pass
             evidence     cycle: … · items n · decided n/n · <status tally>   what the table says
checks       plan-shape-off-type · bullet-missing-note · plan-no-arc ·
             feedback-unserved · head-too-long · head-too-short ·
             note-too-long · note-quotes-page · serves anchors   0 ❌ before the tick
tab          🧭 chips rebuilt                               open it and look
```

Run by hand, it is the three generators (`cli/requirement.py`,
`cli/feedback.py collect`, `cli/evidence-status.py`), the plan checks
(`src/plan_shape.py`, as `checks/outline.py --boards <board>` runs them),
`cli/check.py <board>`, and `cli/build.py <board>`.

### ② Plan · the owning phase gives the words, this pass gives the argument

- **Read the phase policy first.** `fixed`: fill the listed divisions, add none, drop
  none. `grammar`: choose how many of each first word, write the free title
  after it. `resolved`: resolve the source the type names; a missing source
  is a hole, never a licence to invent a shape or copy a sibling's.
- **One `## C<n>` per Content division of the page.** A flat Section page
  (one `### §1`) is one `C1` with `P1` to `P<n>`; the SM00 specimen has three
  because its page has three parts.
- **`arc:` is one sentence that argues.** Every adjacent pair of divisions
  (or, on a one-division page, of paragraphs) passes the swap test: name why N
  must precede N+1 ("Method before Result, or the number cannot be believed");
  a date, a run order or a config order is not a reason. The heaviest finding
  has its own division, or its own paragraph on a one-division page; a finding
  a reader cannot reach from the list is mis-weighted.
- **The Narrative row's order binds.** A Round's proposed reader order is an
  input served through that row; where the two differ, follow the row and
  open a `D<nn>` naming the Round's row, because the Narrative ratifies order
  changes, not a Section.
- **A Section page plans sentence slots.** One bullet per slot in the
  Narrative row's order; the venue's moves (V4) are the slots' jobs; V2 sets
  the budget; a division V3 refuses fails ④ here and never reaches CONTENT
  part. Terms are defined inline the first time; the plan never quotes the
  sentence it plans.
- **A hole is specified, never answered.** Add
  `Evidence: E<NN>-<TYPE>-<slug> · <expected ready evidence>` and its immediate
  `Accept: <observable checks>` under the bullet. TYPE is `VALUE`, `CITE`, or
  `DISPLAY`; a bare `E01` or an icon-only hole is invalid. SHAPE also creates
  the matching record in `<stem>-evidence-items.md` with Target, Label, Need,
  Expected, and Acceptance; a CITE row also initializes `Verified: ⬜` for
  LAND's later human gate. `Label` is a stable 1–12 character ASCII
  alphanumeric display name such as `LBPEffect`; it is not inferred from the
  full readable name. SHAPE does not plan or allocate a Run.
- **The fold appends to the bullet that asked** (EMBED's write, read here): a
  landed value becomes `Answered:`, a built unit's README claim becomes
  `Drawn:`, a served Round row becomes `Routed:`; never a new bullet, never an
  edit to the head.
- **An older-grammar plan is rewritten into the current grammar on this
  pass**: as the next working minor (`v0.<k+1>` while no `v1.0` exists,
  `vN.<k+1>` under an approved `vN.0`). It becomes the next `.0` only when a
  person approves that revision in the channel. A legacy integer chain
  `v1 … vN` first renumbers one to one to `v0.1 … v0.N` (`ref/plan-grammar.md`
  §6) and its old ticks reset to `⬜`; `outline-pass.py` fails an integer-only
  latest plan.

### ③ Threads and the log record

- **Every open ask becomes a `D<nn>` record** in `outline/<stem>-discussion.md`
  (Ask · Options · We lean · Decide), id allocated board-wide
  (`ref/record-shape.md`); a settled one is a log record. An ask with no Aim
  is a thread, never a minted Aim.
- **Every open feedback row is served or declined**: `Routed: <RD> <row id>`
  on the bullet that serves it, or `declined: <RD> <row id> · <reason>` in the
  plan head. `check.py` reports `feedback-unserved` on a row with neither.
- **One log record per pass**: `### YYMMDD HHMM · SHAPE v<N>.<k>: <what changed
  in one line>` (or `SURVEY: <n> rows …`), the receipt folded under it when
  no run folder holds it.

### ④ Five checks, before the person is asked

```text
⓪ ARC       arc: present and an argument · adjacent pairs pass the swap test ·
            the heaviest finding has a division
① COVERAGE  every Evidence line has a typed id, expectation, Accept line, and
            exactly one matching Evidence Item record with a compact Label · every unit on disk is
            cited or retired · every open feedback row is
            served or declined
② ADDRESS   every card and Evidence Item Target names a bullet this plan has
③ VALUE     every 🧮 number recomputes (checks/values.py)
④ SHAPE     divisions match the type's mode · heads 4 to 11 words · Notes
            ≤ 30 words · no Note quotes the page · nothing V3 refuses
```

Any ❌ is fixed in the plan here; the person is not asked yet. ⓪ is half a
judgment: `arc:` present is mechanical, whether it argues is this pass's call
and the person may overturn it at the tick.

### 🤝 Human review and approval · present the packet before asking for a decision

When a person says **review**, **check**, **read**, or **approve** an outline,
load `haipipe-plugin-outline/ref/review-packet.md` and give the human its
four-part packet before seeking a response.  The packet is a compact map of
the records already on disk, not a second plan and not a prose draft:

1. **Current Shape** — link the current versioned plan, state `approved:`,
   quote its `arc:`, and show the C/P reader path in a compact map.
2. **Evidence owed** — link the Evidence Item table and report typed/status
   counts.  Show the items that determine the page's central claim: target,
   expected evidence, acceptance, and the surveyed source/Run path.
3. **What shaped it** — link and summarize only the feedback rows,
   requirements, and open discussion threads that materially changed a
   division or bullet.  State the exact `Routed:` address or say that no such
   record exists; never imply a feedback row landed merely because it was read.
4. **Human decision** — say precisely what can be approved now, what still
   blocks approval, and which choice belongs to the human.  An `approved:` or
   `Decide:` tick is never inferred from a vague positive reaction.

Use clickable local-file links in the response when the host supports them.
If the packet would be long, preserve all four parts but collapse routine
items into counts and show only material evidence/feedback rows; offer the
full linked records rather than omitting the provenance.  The same packet is
required when revising an already-reviewed outline, with a short “changed
since v<N>.0” line under Current Shape.

### 🧑 The tick governs the fork; mode governs whether work waits

- **A person reads the 🧭 tab and ticks `approved:`.** The job there is to
  BREAK the plan: the division that argues nothing, the figure that shows the
  wrong thing, the answer that dodges its ask. The tick means "I tried to
  break it and failed", the one meaning left after a machine checked the
  arithmetic.
- **A chat approval is transcribed, never decided**:
  `approved: ✅ JL 260831 0146 · in chat: "ok, good, I approve this outline"`.
  A machine writes `checked:` for itself and nothing more.
- **Copilot waits; auto may defer review debt.** In `copilot`, an unticked
  person-reserved gate routes to HOLD. In `auto`, the machine may follow the
  checked plan while recording `approved:` on the owed ledger. `Decide` is
  different: it selects `make`, `defer`, or `drop`, so auto must HOLD at
  SURVEY unless the packet already contains an explicit durable decision or
  owner-approved default policy. The machine never converts an owed decision
  into `make`. Deferral is not approval and never supplies durable evidence
  for a Page Face owner's closing gate that requires a person.
- **A tick promotes rather than previews a major.** Working revisions after
  approved `vN.0` are `vN.1`, `vN.2`, … . A person's channel approval freezes
  the selected content as `v<N+1>.0` with the approval quote; all earlier
  frozen and working files remain as history.
- **The gate is where the planning loop exits.** EMBED always returns here with
  the next working minor. In copilot, an approved major with every table row `folded` releases
  CONTENT and fresh marks send the Page to SURVEY. In auto, the same fork is
  taken from `checked:` plus the declared gate policy while the missing human
  act remains owed.

## 🔍 SURVEY · map the Run graph for each ready-evidence contract

SURVEY runs only after SHAPE has named every item and the outline is either
approved in copilot or allowed forward under the explicit auto gate policy.
It inventories the current `task/` and `discoveries/` libraries, classifies
each selected route as existing Result, Ticket only, rerun, or new design, and
writes the evidence-to-Run lineage. It does not scaffold a Ticket, execute a
worker, materialize a Result, or write prose. A new local route normally names
its real owner/parent and receives `rNN` only when LAND allocates the Ticket.
For a Paper-local Run only, SURVEY may reserve the proposed
`P jNN.tNN.rNN` address so the Run remains indexable before LAND; `new` still
means that no Run Ticket exists.

- **Preserve SHAPE's contract.** Item id, type, name, Target, Label, Need,
  Expected, and Acceptance are frozen inputs to SURVEY. If they are insufficient or
  impossible, route the item back to SHAPE; do not repair the meaning here.
- **Map Supporting Runs, zero to many.** Each existing Run is
  `Execution | Discovery · reuse | rerun | registered · bNNjNNtNNrNN`.
  Read the actual Ticket, receipt, and Result before choosing: an accepted
  Result is `reuse`; a real Ticket with no completed attempt is `registered`
  and has the derived availability state `Ticket only`; a failed, smoke-only,
  invalid, or explicitly stale attempt is `rerun`. When the task exists but no
  Ticket exists, write `new-run · bNNjNNtNN`; when the task is absent, write
  `new-task · bNNjNN`; when the job is absent, write `new-job · bNN`; use
  `new-block` only for a bounded block not yet placed in that hierarchy. Do not
  mint an `rNN` during inventory. Write `[]` when no upstream support is needed.
- **Use one global Run identity in two typographies.** Supporting records store the canonical
  compact id `bNNjNNtNNrNN`; the reader-facing table may display the same id as
  `bNN.jNN.tNN.rNN`. The dotted form is a hyperlink label, not a different
  identity. A planned parent `bNNjNNtNN` has no `rNN` until the owning workflow
  allocates a real Run.
- **Plan exactly one Local Input.** State whether its one future frozen
  envelope contains Supporting Results, named governed page-local static
  paths, or `item contract only`. Cross-Folder evidence must enter through a
  Supporting Run Result; Related Page links from Context Workspace are
  navigation/constraints only. A sibling item's future local Result is
  not a local source; both items must name the shared upstream
  Execution/Discovery Run instead.
- **Map exactly one Local Run declaration in the owner's namespace.** An
  existing route uses `registered`, `reuse`, or `rerun` plus its full Run id.
  A Task-local route with no Ticket is
  `Page · Evidence Item · new-run · bNNjNNtNN`; LAND allocates the next `rNN`
  and writes back `bNNjNNtNNrNN`. Another Folder-local owner names its stable
  Folder address and follows its Run Profile. Paper alone may reserve a full
  compact `pjNNtNNrNN`, displayed as `P jNN.tNN.rNN`, before allocation: `P`
  is the fixed Paper block, `jNN` indexes the Page, `tNN` preserves the stable
  Evidence Item number, and `rNN` indexes the proposed attempt (`r01` first).
  In every dialect, `new-run` means proposed, not allocated.
  Do not use a free-text dash placeholder as an action. Its future frozen input envelope may
  include every Supporting Result plus local source material. Its future Result
  must satisfy the item's typed Acceptance contract. Page interpretation is not
  part of this Run.
- **Keep family and action separate.** Discovery is a Supporting Run family,
  not an action. Existing accepted work is `reuse`; an existing Ticket that
  must be executed again is `rerun`; a real never-attempted Ticket is
  `registered`. Changed target/input/acceptance needs a new designed route.
  Supporting `new-run`, `new-task`, `new-job`, and `new-block` routes remain
  inventory findings and do not invent an external `rNN`. Paper-local
  reservation is the bounded exception: SURVEY may reserve its full P/J/T/R
  index, while LAND remains the first phase allowed to create its Ticket.
  There is no `found`, `person`, or `none` action.
- **Citations use the same graph.** A `CITE` item may reuse or commission a
  Discovery Run, then its local Page Evidence Item Run produces the focal,
  verified citation claim. It is not routed to a special `person` outcome.
- **A SURVEY row is complete** when every declared Supporting and Local route
  is honestly classified (existing Result, Ticket only, rerun, or new design),
  one Local Input is explicit, the derived
  `outline/evidence/supporting-runs/` map is current, and Decide is signed (`☑ make`, `☑ defer`,
  or `☑ drop`). A planned route is a plan, not `Ready` evidence. LAND refuses
  `☐`, an ambiguous route, or a fake/guessed Run identity.

The Outline plugin's Evidence Workspace joins the generated evidence snapshot
and `outline/evidence/supporting-runs/` map into one card per Evidence Item. Its identity is the same
compact `E<n><kind>.<Label>` used by the Outline Table; Supporting and Local
Runs are grouped Run items inside that card. The internal `Evidences` lens
explains each Evidence contract; the internal `Runs` lens groups by Evidence
and renders every mapped Supporting or local route as its own Run card.
It reports both mapping and unique-Run counts because shared Runs may appear in
several Evidence groups. This is SURVEY's source inventory, not proof that a
planned route has been allocated. Reader-facing paths are `Run` and
`Result`, with exact paths collapsed behind `Run & Result paths`. SURVEY does
not make the overview carry logs, commands, or output trees.

Each Run item must also answer “what is this for?” Existing Runs take their
Purpose from the real Ticket plus the owning Evidence Item. A proposed route
shows a Plan synthesized from Expected, Acceptance, and Local Input, which
remain authored in `<stem>-evidence-items.md`; SURVEY creates no second plan
file. Present `Availability` separately from `Next action`: existence is
`Planned | Run exists · Result missing | Run + Result | Paths unresolved`,
while action is `Allocate and run | Run | Rerun | Reuse Result | Resolve path`.
Do not present `new`, `rerun`, `run only`, and `ready` as one status scale.

### 🧑 The Decide ends the cycle

A person reads the table on the 🧭 tab (the Evidence Workspace lens, which renders
the table joined to the disk with a derived Status chip per row) and writes
one Decide per row. A machine may transcribe a chat decision with the quote;
it never ticks `☑` on its own. `cli/evidence-status.py` prints the classified
lineage and `cycle: SURVEY · decided n/n` until every row is signed and mapped,
then `cycle: LAND`.

## 🔀 Routes

```text
SHAPE  any of the five ❌                     fix the plan here; no tick yet
SHAPE  five pass, items owed, gate allows      OUTLINE / SURVEY
SHAPE  five pass, every item folded, allowed   CONTENT / WRITE
SHAPE  approved ⬜ in copilot                   HOLD
SHAPE  approved ⬜ in auto                      record owed; follow declared gate policy
SURVEY route ambiguous                         OUTLINE / SURVEY
SURVEY Decide open without durable policy      HOLD at OUTLINE / SURVEY
SURVEY every make graph classified + allowed  EVIDENCE / LAND
SURVEY item cannot be specified truthfully    SHAPE, naming item and target bullet
owning phase policy refuses the shape         fix the plan, unless the mismatch is a real
                                              finding against that policy
```

OUTLINE never routes directly to CHECK; a Page version must first pass CONTENT.

## 🧾 Receipt

```text
phase: OUTLINE
cycle: SHAPE | SURVEY
file: <page>/outline/<stem>-outline-v<N>.<k>.md | <page>/outline/<stem>-evidence-items.md
supersedes: v<N>.<k-1> | v<N-1>.0 | none
requirement: V1 V2 V3 V4 read ✅
feedback: n routed · n served · n declined
items: n typed · n specified · n planned · n decided · by type VALUE/CITE/DISPLAY
runs-mapped: existing supporting n (Execution n · Discovery n) · planned n · local n
checks: ⓪ ✅ ① ✅ ② ✅ ③ ✅ ④ ✅        (SHAPE)
counts: divisions · paragraphs · bullets · Evidence Items by type
threads: D<nn> opened … · D<nn> settled …
approved: ✅ <who> <date> | ⬜ waiting/owed
route: CONTEXT | OUTLINE | EVIDENCE | CONTENT | HOLD
next_cycle: PREPARE | SHAPE | SURVEY | LAND | WRITE  # omit on HOLD
```

## 📂 Files

```text
haipipe-page-outline/
├── SKILL.md            this phase: the SHAPE and SURVEY cycles
└── CHANGELOG.md        version history, and the only home for what this phase used to say
```

Owns no scripts. The base is `haipipe-page`; the folder, the tab, the plan
grammar and the item table's grammar are `haipipe-plugin-outline`'s
(`ref/plan-grammar.md`, `ref/item-table.md`, `ref/record-shape.md`,
`ref/specimen-section-plan.md`); the Page loop and receipt law are
`haipipe-page-workflow`'s; the six-field card of every phase is
`../haipipe-page-workflow/ref/phase-cards.md`; the next phase is
`haipipe-page-evidence` (LAND, EMBED), and after the plan exits,
`haipipe-page-content`. The design page is `QPw1-outline` on
`BoardSkillBoard-260722`.
