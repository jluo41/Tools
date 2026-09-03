---
name: haipipe-page-outline
description: >-
  The OUTLINE phase of a Board Page and the THINKING half of its OUTLINE part:
  two planning cycles, SHAPE (brief → propose → react → revise; name every typed
  Evidence Item, compact Label, and expected ready payload) and SURVEY (inventory zero-to-many
  Execution/Discovery Supporting Runs, zero-to-many exact PageX bindings, plus
  exactly one local Page Evidence Item Run declaration). Writes the versioned plan,
  Evidence Item table, open threads and log;
  records evidence-to-Run lineage but allocates no Ticket and executes no material. Trigger: page outline, OUTLINE
  phase, shape the plan, survey the evidence items, evidence item table, review,
  check, read, or approve the outline, fold evidence into the plan,
  /haipipe-page-outline.
metadata:
  version: "0.19.0"
  last_updated: "2026-09-03"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-outline · SHAPE the plan, then SURVEY what it owes

Load the concrete chain, in order:

```text
haipipe-page-workflow
  → haipipe-page-outline
  → haipipe-plugin-outline/ref/plan-grammar.md
  → haipipe-plugin-outline/ref/item-table.md
  → haipipe-plugin-outline/ref/evidence/pagex.md (when SURVEY considers a cross-Folder source)
  → haipipe-plugin-outline/ref/review-packet.md (only for a human review or approval)
  → the exact owning workflow-phase skill, for example haipipe-paper-narrative
```

The owning workflow phase supplies the Page's outline/narrative/style policy.
Do not route through `haipipe-page-for-task`; that compatibility variant is no
longer part of this design. Load no sibling Page and no board-wide checker
output before reading the target Page.

The page workflow has two PARTS (haipipe-page-workflow §🔁): the OUTLINE part
decides what is true and what the page will therefore say; the DRAFT part
writes it. This phase owns the OUTLINE part's two HUMAN-gated cycles; its
sibling `haipipe-page-evidence` owns the two machine-gated ones (LAND, EMBED).
The reader sees this authority as one Outline plugin with two primary surfaces:
**Bullet Workspace** for the plan and **Evidence Workspace** for what each
bullet needs. Requirement/Discussion/Feedback are Plan Context; Files/Log are
Page Records. None of these records is copied back into `page.md`.

```text
OUTLINE part
  SHAPE    this file    plan + typed item expectation          👤 approved:
  SURVEY   this file    classify routes + PageX + Local Input + Run   👤 Decide, per item
  LAND     evidence     allocate planned routes, execute → Result     ⚙ every make-item ready
  EMBED    evidence     fold ready Results into plan v<N+1>     ⚙ back to SHAPE
```

## ⚡ Brief

```text
Q        what will this page say, division by division, bullet by bullet;
         what does each bullet owe; and where in tasks/ does each owed thing
         come from?
READS    outline/<stem>-requirement.md (V1 to V4) · outline/<stem>-feedback.md
         (open rows) · outline/<stem>-evidence.md (the table joined to the
         disk) · the owning workflow phase's outline policy · the page · the current plan ·
         the project's tasks/ tree and unified Evidence PageX shortlist
         (SURVEY only)
WRITES   outline/<stem>-outline-v<N>.md · outline/<stem>-evidence-items.md ·
         outline/<stem>-discussion.md (D<nn>) · outline/<stem>-log.md (one
         record) · outline/evidence/supporting-runs/<stem>-run-bindings.md
         (generated pointers) · never the page
CHECKS   ⓪ ARC ① COVERAGE ② ADDRESS ③ VALUE ④ SHAPE, all pass before the
         person is asked (SHAPE); every make-item has an audited Supporting/Local
         Run map, valid PageX/input, and one decision (SURVEY)
ENDS     SHAPE: a person ticks approved: (or a chat approval is transcribed
         with the quote) · SURVEY: every row carries a signed Decide and each make-Run is classified
WALLS    writes no prose · raises no card · executes nothing and lands no Result ·
         mints no Aim · names no division the type refuses · ticks nothing ·
         changes a ✅ plan only as v<N+1> · never writes a Status word
ROUTES   SHAPE → SURVEY (approved, marks owed) · SHAPE → the DRAFT part
         (approved, every item folded) · SURVEY → LAND (every item graph classified and decided) ·
         either → SHAPE again · HOLD (the person is unavailable)
RECEIPT  §🧾, one block per pass, `cycle: SHAPE | SURVEY`; field law:
         ../haipipe-page-workflow/ref/page-run-contract.md §Receipt step
```

## ⓪ Boot · load little, trust the plan

- **Load**: this brief, the owning workflow phase's outline policy (`fixed` lists the
  divisions · `grammar` fixes a first-word set and an order rule · `resolved`
  points at a source outside the type · no key means the base section order),
  `ref/plan-grammar.md`, the page, and the eight files under `outline/`. The
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
2 PROPOSE   the AI writes plan v1 from the brief + owning phase policy + venue;
            every owed thing is a named typed Evidence Item with Label + Expected + Accept
3 REACT     the person reads the rendered plan on the 🧭 tab: ticks, comments, redirects
4 REVISE    the AI folds the rulings into v2
loop 3 ⇄ 4 until the person ticks approved:
```

Steps 2 and 4 are the chat's verbs (`propose`, `revise`); step 3 is the person
on the 🧭 tab. "Draft" and "Brief" are not cycle names: DRAFT is the second
part of the workflow, and Brief is the design family's D0.

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
  the budget; a division V3 refuses fails ④ here and never reaches the DRAFT
  part. Terms are defined inline the first time; the plan never quotes the
  sentence it plans.
- **A hole is specified, never answered.** Add
  `Evidence: E<NN>-<TYPE>-<slug> · <expected ready evidence>` and its immediate
  `Accept: <observable checks>` under the bullet. TYPE is `VALUE`, `CITE`, or
  `DISPLAY`; a bare `E01` or an icon-only hole is invalid. SHAPE also creates
  the matching record in `<stem>-evidence-items.md` with Target, Label, Need,
  Expected, and Acceptance. `Label` is a stable 1–12 character ASCII
  alphanumeric display name such as `LBPEffect`; it is not inferred from the
  full readable name. SHAPE does not plan or allocate a Run.
- **The fold appends to the bullet that asked** (EMBED's write, read here): a
  landed value becomes `Answered:`, a built unit's README claim becomes
  `Drawn:`, a served Round row becomes `Routed:`; never a new bullet, never an
  edit to the head.
- **An older-grammar plan is rewritten into the current grammar on this
  pass**: in place while ⬜, as `v<N+1>` after a tick.

### ③ Threads and the log record

- **Every open ask becomes a `D<nn>` record** in `outline/<stem>-discussion.md`
  (Ask · Options · We lean · Decide), id allocated board-wide
  (`ref/record-shape.md`); a settled one is a log record. An ask with no Aim
  is a thread, never a minted Aim.
- **Every open feedback row is served or declined**: `Routed: <RD> <row id>`
  on the bullet that serves it, or `declined: <RD> <row id> · <reason>` in the
  plan head. `check.py` reports `feedback-unserved` on a row with neither.
- **One log record per pass**: `### YYMMDD HHMM · SHAPE v<N>: <what changed
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
since v<N>” line under Current Shape.

### 🧑 The tick ends the cycle, and it carries the fork

- **A person reads the 🧭 tab and ticks `approved:`.** The job there is to
  BREAK the plan: the division that argues nothing, the figure that shows the
  wrong thing, the answer that dodges its ask. The tick means "I tried to
  break it and failed", the one meaning left after a machine checked the
  arithmetic.
- **A chat approval is transcribed, never decided**:
  `approved: ✅ JL 260831 0146 · in chat: "ok, good, I approve this outline"`.
  A machine writes `checked:` for itself and nothing more.
- **A tick belongs to the version it ticked.** Evidence that changes an
  approved plan makes `v<N+1>`; `v<N>` is kept, because it was right at its
  date.
- **The tick is where the OUTLINE part exits.** EMBED always returns here with
  plan v<N+1>; `approved:` with every table row `folded` releases the DRAFT
  part, `approved:` with fresh marks sends the page to SURVEY again. The
  machine never decides that the part is over.

## 🔍 SURVEY · map the Run graph for each ready-evidence contract

SURVEY runs only after SHAPE has named every item and the outline is approved.
It inventories the current `task/` and `discoveries/` libraries, classifies
each selected route as existing Result, Ticket only, rerun, or new design, and
writes the evidence-to-Run lineage. It does not allocate an `rNN`, scaffold a
Ticket, execute a worker, materialize a Result, or write prose.

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
- **Use one Run identity in two typographies.** Records store the canonical
  compact id `bNNjNNtNNrNN`; the reader-facing table may display the same id as
  `bNN.jNN.tNN.rNN`. The dotted form is a hyperlink label, not a different
  identity. A planned parent `bNNjNNtNN` has no `rNN` until the owning workflow
  allocates a real Run.
- **Bind PageX sources, zero to many.** Write `PageX Bindings: []` when the
  item uses no cross-Folder Page material. Otherwise name each exact
  repo-relative file or Result plus its authority using
  `haipipe-plugin-outline/ref/evidence/pagex.md`. PageX is not a Run family, action, or
  Result type. A whole-Folder link is navigation only and cannot satisfy an
  item until an exact accepted source inside it is selected.
- **Plan exactly one Local Input.** State whether its one future frozen
  envelope contains Supporting Results, PageX bindings, named pre-existing
  local paths, or `item contract only`. When PageX bindings exist, the field
  must explicitly say they are frozen. A sibling item's future local Result is
  not a local source; both items must name the shared upstream
  Execution/Discovery Run instead.
- **Map exactly one Local Run declaration.** It is always
  `Page · Evidence Item · reuse | rerun | registered · bNNjNNtNNrNN` when a
  real local Ticket already exists. When it does not, use the same hierarchy
  precisely: `new-run · bNNjNNtNN`, `new-task · bNNjNN`, `new-job · bNN`, or
  `new-block · <bounded block name>`, and leave the local Ticket unallocated.
  Do not use a free-text dash placeholder as an action. Its future frozen input envelope may
  include every Supporting Result plus local source material. Its future Result
  must satisfy the item's typed Acceptance contract. Page interpretation is not
  part of this Run.
- **Keep family and action separate.** Discovery is a Supporting Run family,
  not an action. Existing accepted work is `reuse`; an existing Ticket that
  must be executed again is `rerun`; a real never-attempted Ticket is
  `registered`. Changed target/input/acceptance needs a new designed route.
  `new-run`, `new-task`, `new-job`, and `new-block` are explicit inventory
  findings; they have no `rNN` until the owning workflow allocates a Ticket.
  There is no `found`, `person`, or `none` action.
- **Citations use the same graph.** A `CITE` item may reuse or commission a
  Discovery Run, then its local Page Evidence Item Run produces the focal,
  verified citation claim. It is not routed to a special `person` outcome.
- **A SURVEY row is complete** when every declared Supporting and Local route
  is honestly classified (existing Result, Ticket only, rerun, or new design),
  PageX bindings are valid, one Local Input is explicit, the derived
  `outline/evidence/supporting-runs/` map is current, and Decide is signed (`☑ make`, `☑ defer`,
  or `☑ drop`). A planned route is a plan, not `Ready` evidence. LAND refuses
  `☐`, an ambiguous route, or a fake/guessed Run identity.

The Outline plugin's Evidence Workspace joins the generated evidence snapshot
and `outline/evidence/supporting-runs/` map into one card per Evidence Item. Its identity is the same
compact `E<n><kind>.<Label>` used by the Outline Table; Supporting and Local
Runs are grouped Run items inside that card. Reader-facing links are `Run` and
`Result`, with exact paths collapsed behind `Run & Result paths`. SURVEY does
not make the overview carry logs, commands, or output trees.

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
SHAPE  five pass, items owed, approved ✅     SURVEY
SHAPE  five pass, every item folded, ✅       the DRAFT part (haipipe-page-draft)
SHAPE  approved ⬜, person unavailable        HOLD
SURVEY route ambiguous or Decide open          SURVEY · HOLD when human input is required
SURVEY every make graph classified + decided  LAND (haipipe-page-evidence)
SURVEY item cannot be specified truthfully    SHAPE, naming item and target bullet
owning phase policy refuses the shape         fix the plan, unless the mismatch is a real
                                              finding against that policy
```

OUTLINE never routes to the DRAFT part's REVISE or CHECK.

## 🧾 Receipt

```text
phase: OUTLINE
cycle: SHAPE | SURVEY
file: <page>/outline/<stem>-outline-v<N>.md | <page>/outline/<stem>-evidence-items.md
supersedes: v<N-1> | none
requirement: V1 V2 V3 V4 read ✅
feedback: n routed · n served · n declined
items: n typed · n specified · n planned · n decided · by type VALUE/CITE/DISPLAY
runs-mapped: existing supporting n (Execution n · Discovery n) · planned n · local n
pagex-bindings: n exact · n unresolved/invalid
checks: ⓪ ✅ ① ✅ ② ✅ ③ ✅ ④ ✅        (SHAPE)
counts: divisions · paragraphs · bullets · Evidence Items by type
threads: D<nn> opened … · D<nn> settled …
approved: ✅ <who> <date> | ⬜ waiting
next: SHAPE | SURVEY | LAND | DRAFT | HOLD
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
`ref/specimen-section-plan.md`); PageX binding semantics are
`haipipe-plugin-outline/ref/evidence/pagex.md`; the two-part loop and the receipt law are
`haipipe-page-workflow`'s; the six-field card of every phase is
`../haipipe-page-workflow/ref/phase-cards.md`; the next phase is
`haipipe-page-evidence` (LAND, EMBED), and after the part exits,
`haipipe-page-draft`. The design page is `QPw1-outline` on
`BoardSkillBoard-260722`.
