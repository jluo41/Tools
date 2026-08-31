# Draft: turn the approved bullets into sentences, and name what each one is missing
state: 🟡 IN PROGRESS · the phase ships; the scaffold form has never been produced by a real run · open: 5
owner: CC
method: separate the promise from its realization, then show the conversion on a worked Point; every boundary here names the phase on the other side of it
session: ec8c7879-3e0f-484e-a3fe-b41b1bfb50fc

## Opening
Once a plan is approved, what does the page actually promise, and what does it lose if a hole never gets filled?

DRAFT is phase ② and it does one visible thing: it turns each approved Outline Point into one or more sentence scaffolds, keeping every unresolved dependency visible at the place where it will be used.
It also does one invisible thing that decides the rest of the loop: it writes the page's purpose and Aims, and the Aim attached to a hole IS the stake that a probe card will later have to carry.
That is why no card may exist before this phase ends, a rule that reversed a 260816 ruling on 260817.
Its risk runs in one direction only: presenting an unavailable answer as settled fact, because a hole hidden here reaches print wearing the same face as a real number.

## Writing Style
How this page must be written. Read it before editing, and edit to it.

**The promise and its realization are different subjects, and this page is only about the promise**: adding a paragraph for an existing Aim is REVISE, and adding an Aim is DRAFT.
Any sentence here describing how prose should read belongs on `QPw5` instead.

**A hole is written, never implied**: every rule about a missing fact must show the visible marker and the Aim it costs, side by side.
A rule that says "record the uncertainty" without showing where it lands is unimplementable and reads like advice.

**Say which phase is on the other side of every boundary**: this phase is defined by four handoffs, to OUTLINE behind it and to PROBE, EVIDENCE, and REVISE ahead.
A boundary stated without naming its neighbour cannot be checked.

**Language and sentences**: English only, in the source and in the render.
Write one sentence per line, so a paragraph is consecutive lines rather than one long line.
No em-dashes: use a colon, a semicolon, a comma, parentheses, or simply start a new sentence.

## Diagram
The conversion this phase performs, and the one thing it produces that nothing else can.

```text
✏️ DRAFT · phase ② of 7
                    ENTERS on an approved outline
                              │
   C3.P1.B4 · Establish robustness across specifications      ← the POINT
                              │
                              ▼  instantiate
   C3.P1.S1 · The primary estimate is <VALUE HOLE>.           ← the SCAFFOLDS
   C3.P1.S2 · It remains <ROBUSTNESS HOLE> across specifications.
   C3.P1.S3 · <DISPLAY HOLE> compares the estimates.
              <!-- realizes: C3.P1.B4 -->   ← the machine-readable join

┌─────────────────────────────────────────────────────────────────┐
│ OWNS   purpose · Aims · the page's promise · the visible hole    │
│ 🚫 MAY invent a number, a citation, an interpretation, or a       │
│    NOT  rendered display · name a division the plan did not name │
│    NOT  open a file under probe/                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
    the Aim a hole belongs to  =  THE STAKE
    what the page LOSES if the answer never comes
                              │
                              ▼
    ③ PROBE copies that stake into the card's consumer/ side
```
📌 This is the FIRST half of the conversion; REVISE performs the second half by replacing the holes and citing the landed ids.

## Content

### 1 · One Point becomes one or more sentence scaffolds
**The conversion rule**: a Point is a content unit and not necessarily one sentence, so the scaffold count is chosen here rather than assumed.

```text
the POINT              an approved plan bullet, addressed C<n>.P<n>.B<n>
  ↓ DRAFT
the SCAFFOLD           C<n>.P<n>.S<m> · prose with a VISIBLE hole
                       plus  <!-- realizes: C3.P1.B4 -->

what the scaffold may     the shape of the sentence, its hole markers,
DECIDE                    how many sentences one Point needs
what it may NOT           a number · a citation · an interpretation ·
INVENT                    a rendered display
```
📌 The Point address is the join key, so REVISE may later expand, merge, or split a scaffold and the `realizes:` backlink still resolves.

#### 1.1 · The backlink is a comment, not reader-facing prose
(`<!-- realizes: C3.P1.B4 -->` on the scaffold line)
The join has to survive rewriting, so it is written where a reader never sees it and a machine always can.
Putting the address in the visible sentence would make the page read like its own build system, which is the failure `QPw00 §🪞` names for the whole loop.

#### 1.2 · A hole marker is a promise about a phase, not a placeholder
(`<VALUE HOLE>` waits on the bank, `<DISPLAY HOLE>` waits on a render, `<ROBUSTNESS HOLE>` waits on both)
Each marker names which later phase owes the fill, so a reader of the draft can tell what is missing and who is expected to bring it.
An undifferentiated `TODO` cannot route, and a page full of them cannot be checked.

### 2 · The Aim attached to a hole IS the stake
**The stake rule**: what the page loses if an answer never comes is an Aim, and Aims are written here, which is why the card cannot come earlier.

```text
target prose     "The effect is <HOLE>."  [Q-<local-id>]
the Aims section   the Aim that hole belongs to
the States section that Aim's honest current row
                          │
                          ▼
③ PROBE copies exactly this pairing into probe/PP<NN>-<slug>/consumer/
```
📌 So DRAFT names the hole and its owner, and opens no file: the card's number, its Q-executor, its `serves:` line, and its dispatch all belong to PROBE.

#### 2.1 · DRAFT created the card until 260817, and two reasons ended it
(the second reason is the one that decides it)
The first is duplication: a card that only repeats the plan's mark is a second copy of the plan, which `QPw00 §🪞` forbids for every plugin.
The second is the stake: a card raised before this phase ends cannot carry its own stake, because the stake is an Aim and the Aim does not exist yet.
This reversed a 260816 ruling that let DRAFT raise the card in OWED state, and nothing replaced the move: the mark stays the proposal.

#### 2.2 · Never invent a value or a source to avoid a hole
(the phase's one directional risk)
A hidden hole reaches print wearing the same face as a real number, and no later phase can tell the two apart.
A visible hole is cheap at every later phase and a fabricated fill is unrecoverable, so the asymmetry decides the rule.

### 3 · Three layers own a page's shape, and only the third is DRAFT's
**The altitude rule**: DRAFT's first move is to find out which layer already answered.

```text
layer      owner                     fixes                    for
──────────────────────────────────────────────────────────────────────────
FRAME      haipipe-page · QPs1       the SECTION ORDER        every page kind
CONTENT    the matching Page Type    the DIVISION SHAPE       one page kind
INSTANCE   DRAFT                     THIS page's outline      one page
```
📌 Inventing a division shape when the Page Type declares one is the defect, and so is proposing an outline when no `page-type:` key claims the page at all.

#### 3.1 · The three outline modes decide what DRAFT is even allowed to choose
(`fixed`, `grammar`, and `resolved`, declared in each Page Type's own frontmatter)
Under `fixed` the type lists its divisions outright and DRAFT fills them without adding, dropping, or reordering.
Under `grammar` the type fixes a closed first-word set and an order rule, and DRAFT chooses how many of each and writes the free title, which is how `page-type: task` gets `Data · Why · Result(×n) · Meaning(last)`.
Under `resolved` the outline lives outside the type and must be resolved before a variant is chosen, and a missing source is a HOLE rather than a licence to invent one.

#### 3.2 · A container-shaped Page Type still takes the subject at division level
(the `page-type: view` failure JL read on 260816)
A seven-result-family regression report written to `for-view` printed `QA inputs` and `Displays` as top-level sections and buried main OLS, robustness, IV, DID, and heterogeneity as subsections of `View body`.
That is a readable View and an unreadable report.
The subject's families go under the division the type leaves free, numbered, and the mismatch is recorded as a finding against the Page Type rather than fixed by silently reshaping it.

### 4 · The phase is identified by authority, and the diff cannot tell
**The DRAFT versus REVISE test**: both may add, delete, move, and rewrite, so only the reason separates them.

```text
the edit                                        phase
──────────────────────────────────────────────────────────
add a paragraph serving an existing Aim          REVISE
add a new Aim                                    DRAFT
remove a promised result                         DRAFT
change what the page is FOR                      DRAFT
rewrite a sentence under a fixed promise         REVISE
```
📌 Returning to DRAFT because purpose or Aims changed starts a NEW ROUND on the same persistent page; it is not a failure and it is not forbidden.

#### 4.1 · DRAFT may run on an empty page, repeat, or reopen a mature one
(an empty file does not mean DRAFT and first typing does not either)
A page with polished prose may be reopened by DRAFT when its purpose moves, and that is the loop working rather than the page regressing.
`QPw00 §5.2` carries the rule that REVISE to DRAFT is a restart and not a forbidden edge.

### 5 · Exit and routing, with no mandatory next phase
**The routing rule**: DRAFT exits when the promise is stable enough to test, investigate, or realize, and the next phase is chosen by what the page now needs.

```text
a promised claim has no support yet     ──▶  ③ PROBE
the promise is stable, realization needs work ──▶  ⑤ REVISE
the version is ready for judgment      ──▶  ⑦ CHECK
the promise is still unsettled         ──▶  ② DRAFT again
```
📌 DRAFT never routes directly to CLOSE and never calls its own output checked; a Page Type may declare a gate and DRAFT never invents one.

#### 5.1 · A repeated DRAFT in the same unsettled round does not reopen the promise
(`reopens_promise: false` in the receipt)
Two DRAFT passes before any handoff are one round still settling, not two rounds.
If DRAFT was entered from a later phase, the controller already opened the new round and DRAFT records it rather than incrementing it again.

## Aims

### Decision Now
- [ ] 🗣 Rule whether the hole MARKER vocabulary is closed or free
      📍 `Part` §1.2, a hole marker is a promise about a phase
      🔔 `Why now` the contract shows `<VALUE HOLE>`, `<ROBUSTNESS HOLE>` and `<DISPLAY HOLE>` in one example without saying whether those three are the set, and a checker cannot warn on an unroutable marker until it knows
      ⭐ `A ·` closed set of three, one per later phase that can fill a hole (bank, render, both), which makes every marker routable and lets a checker warn on anything else
      `B ·` free text, which reads more naturally in prose but means no checker can ever tell a routable hole from a note to self
      🛑 `Blocks` A1.2, and any `unroutable-hole` check
      🤖 `If nobody answers` A takes effect, because the three in the contract's own example already form a complete set over the phases that can fill a hole


### A1 · 🧱 One Point becomes one or more sentence scaffolds
- ✅ A1.1 · The conversion is shown on a worked Point rather than described.
  Done when one Point and its three scaffolds appear with the `realizes:` comment in place.
  **Now:** Met. `C3.P1.B4` and its three scaffolds are worked in the Diagram and in `§1`.
- ⬜ A1.2 · A real run has produced scaffolds in this form on a live page.
  Done when one page on any board carries `C<n>.P<n>.S<m>` scaffold lines written by a DRAFT run.
  **Now:** Not started. The scaffold form shipped in `haipipe-page-draft` 0.7.0 on 260817 and no run has produced one on a live page.


### A2 · 🕳 The Aim attached to a hole IS the stake
- ✅ A2.1 · The stake pairing is stated so PROBE can copy it without interpretation.
  Done when the prose hole, its Aim, and its State row are named as one unit.
  **Now:** Met. The three-line pairing is stated in `§2` and is what PROBE copies.
- ⬜ A2.2 · No page on this board carries a fabricated value in place of a hole.
  Done when every unfilled claim on this board shows a visible marker.
  **Now:** Not measured. No sweep of this board's unfilled claims has been run.


### A3 · 🧬 Three layers own a page's shape, and only the third is DRAFT's
- ✅ A3.1 · The three outline modes are readable without opening a Page Type.
  Done when `fixed`, `grammar`, and `resolved` each name what DRAFT may choose under them.
  **Now:** Met. `§3.1` states what DRAFT may choose under each of the three modes.


### A4 · 🛠 The phase is identified by authority, and the diff cannot tell
- ✅ A4.1 · The DRAFT versus REVISE boundary is testable on a concrete edit list.
  Done when five edits are classified and each names its phase.
  **Now:** Met. Five edits are classified in `§4`.


### A5 · 🔀 Exit and routing, with no mandatory next phase
- ✅ A5.1 · The four routes are stated with the condition that selects each.
  Done when each route names the page condition that chooses it.
  **Now:** Met. Four routes with their selecting conditions are in `§5`.


## Files
### 📋 Contracts · what CARRIES a rule to other pages
- `page-workflows/haipipe-page-draft/SKILL.md`
  The phase contract itself, at 0.7.0, and the authority on its procedure.
- `page-types/`
  The Page Type variants whose `outline:` blocks decide what DRAFT may choose. The type wins over this page on division shape.
### 📤 Output files · what a BUILD writes
- `board/QPw/QPw2-draft.html`
  ⚠️ Generated by `cli/build.py`. Never hand-edit it; the markdown is the only source.

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `continues · ALL` · [QPw1 §5](5-QPw-page-workflow/QPw1-outline/QPw1-outline.md)
  The phase behind this one: the approved plan and its marks, which DRAFT executes and may not exceed.
- `constrained by · ALL` · [QPw00 §6](5-QPw-page-workflow/QPw00-page-loop/QPw00-page-loop.md)
  The rule that an operation never names a phase, which is what makes the DRAFT versus REVISE test necessary.
- `contrasts · EVIDENCE` · [QPw4 §5](5-QPw-page-workflow/QPw4-evidence/QPw4-evidence.md)
  The phase that lands what these holes are waiting for, and the one forbidden to touch the purpose and Aims this phase owns.

## Law
- 260817 JL · 🃏 **DRAFT creates NO card**: the outline's mark is the proposal and PROBE turns it into a folder
  This reversed the 260816 ruling that let DRAFT raise a card in OWED state, on two grounds: a card repeating the mark is a second copy of the plan, and a card raised before this phase ends cannot carry its own stake because the stake is an Aim.
  The option rejected was keeping the OWED state with a stricter rule about when it may be written, which loses because the stake problem is a matter of ordering and no rule can reorder it.
- 260817 JL · 🗂 **The outline left this phase**: agreeing the shape and executing it are separate phases with separate reports
  DRAFT now enters on an approved plan and names no division the plan did not name; when the plan is wrong that is a return to OUTLINE and a `v2`, not a quiet edit here.
- 🕳 **Never invent a value or a source to avoid a hole**: a hidden hole reaches print wearing the face of a real number
  A visible hole is cheap at every later phase and a fabricated fill is unrecoverable, so the asymmetry decides it.
- 🛠 **Authority names the phase, not the diff**: adding a paragraph for an existing Aim is REVISE and adding an Aim is DRAFT
  Every phase in this loop may add, delete, move, and rewrite, so a visible change can never identify the phase that produced it.

## Glossary
- 🧱 **sentence scaffold**: a draft sentence at `C<n>.P<n>.S<m>` carrying a visible hole and a `realizes:` backlink to its Point.
- 🕳 **hole**: a named missing fact left visible in the target prose, paired with the Aim it costs.
- ⚖️ **stake**: what the page loses if a hole is never filled, which is an Aim, and which PROBE copies into a card's `consumer/` side.
- 🧬 **outline mode**: how a Page Type supplies its divisions, one of `fixed`, `grammar`, or `resolved`, declared in the type's own frontmatter.

## Log
- 260818 · [DRAFT-CC] page created on JL's ruling that each workflow step gets its own page. Written from `haipipe-page-draft` 0.7.0. JL's own summary opened it: "the draft is about convert the outline's bullet point into the sentences, right?", which is the phase's visible half and is now `§1`; its invisible half, that the Aim behind a hole IS the stake a card will carry, is `§2` and is the reason the 260817 no-card ruling had to go that way. Five divisions: the Point-to-scaffold conversion, the stake, the three shape layers, the authority test against REVISE, and routing. The hole-marker vocabulary turned out to be undecided in the contract, so it is the Decision Now row rather than a silently invented set.

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0