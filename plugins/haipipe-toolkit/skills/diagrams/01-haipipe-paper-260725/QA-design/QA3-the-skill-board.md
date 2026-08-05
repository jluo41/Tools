# The skill board: what is argued here, and what leaves

state: 🟡 PARTIAL · the record-versus-manual rule and graduation are ruled; most settled faces still carry no Law to graduate
owner: JL
method: keep the reasoning here, copy only the ruling out, and never let runtime depend on either

## Opening

What belongs on a design board, and what happens to a question once it is answered?
This folder looks like documentation and is not: `skills/paper/SKILL.md` is what a worker follows, and this is the argument that produced it.
Mistake one for the other and the board becomes a second manual that drifts from the first, with nothing saying which binds.
The argument stays, only the Law is copied out, and nothing may depend on either.

**Where this page sits**: `QA1` says which folder a thing belongs in; this page says what one KIND of folder holds.
`QA7` is its deliberate opposite, because nothing graduates out of a paper board.
Where any board lives on disk, and its page grammar, are ruled on the board tool's own board at `QC1@boardform` and `QA2@boardform`.

**What we want at the end**: a board that could be deleted without breaking anything.
If a skill ever needs a Q page in order to run, something has been filed in the wrong folder, and the delete test is how you find out.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4@boardform`**: the page grammar, the section order, and the sentence rules come from `../01-boardform-260722/QB-delivery/QB4-overall.md` and are not restated here.

**Never state how many pairs or folders there are**: that number is `QA1`'s and it has changed twice.
This page carried "the easiest of the eight" and "there are four such pairs" long after both were wrong, because a count restated away from its owner is a count nobody revisits.

**Say which of the two things a sentence is about**: the argument, or the instruction.
Every defect this page exists to prevent is one being mistaken for the other, so ambiguity here is not a style problem.

**A graduation claim names BOTH targets or neither**: seven groups land in the paper skill and the board tool.
Writing only one is how a ruling gets applied to half of itself, twice on 260726.

## Diagram

**Graduation**: the one part of a face that is meant to leave, and where it lands.

```text
 ┌────────────────────────────────────────────────────────────────┐
 │ ② SKILL BOARD   skills/diagrams/01-haipipe-paper-260725/       │
 │   🧭 Opening    the question in its own words                  │
 │   📚 Content    the alternatives rejected, the evidence        │
 │   🎯 Aims       what is still owed                             │
 │   ⚖️ Law   ◀──── the ONE part that is meant to LEAVE           │
 └───────────────────────────┬────────────────────────────────────┘
                             │  state: ✅  ━▶  COPY the Law out
              ┌──────────────┴──────────────┐
              ▼                             ▼
   ┌────────────────────┐        ┌────────────────────────┐
   │ ① haipipe-paper    │        │ ③ haipipe-board        │
   │   the paper family │        │   the board family     │
   └────────────────────┘        └────────────────────────┘
     from here on THIS binds       and for SEVEN groups, so
     and the board does not        does this. Both, or neither

 📋 the Law is COPIED, never cut: the face stays as the record of WHY
 🗑 delete this whole folder and BOTH skills still run
```

**Where each group's Law lands**: the graduation edge, made addressable.

```text
 group                     ━▶ ① haipipe-paper          ━▶ ③ haipipe-board
 ───────────────────────    ────────────────────────     ──────────────────
 QA1  the folder map        README · folder-anatomy      —
 QA2  the skill set         the tree · the one door      —
 QA3  the skill board       — it rules ② itself          —
 QA6  the paper             the door: fn/folder · enter  —
 QA7  the paper board       S10-round/round stage data   the S-family list
 QA4  the tool              create-page.py               the whole package
 QA8  who owns a region     create-page.py               stage.py · serve.py
 QA9  driving work          the door's STAGE step        page RUN · serve.py
 QA10 the prose verb        revise-humanizer             haipipe-board-sentence
 QC2-3   adding a stage     index.yml · CONTRACT.md      —
 QC3b-d  the page written   create-page.py               stage.py
 QC4-4d  the four phases    the stages' craft: files     page-phases/
 QC5     the sentence       citation/revise craft files  src/body.py
```

## Content

### 1 · What a face holds, and what leaves it

**Record against manual**: the same rule stated from both sides.

```text
 📋 THE FACE keeps                   📖 THE SKILL gets
 ──────────────────────────          ─────────────────────────
 the question in its own words       the ruling, as procedure
 the alternatives REJECTED           nothing else
 the evidence that decided it
 the Law, as a COPY                  ⚖️ the Law, as the binding text

 🎓 ✅ means the Law has been copied out, not that work finished
 🚫 a worker following a procedure never reads a face
 ✂️ copied, never cut: the WHY is exactly what a procedure must not carry
```

📋 Establishes what a design board is for, what graduation moves, and what `state:` on this board measures.

#### 1.1 · A face holds the argument, and the skill holds the instruction
(the single distinction every other rule on this page depends on)
A face carries the question in its own words, the alternatives that were considered and rejected, the evidence that decided it, and the ruling as a `## Law` once there is one.
A worker following a procedure should never need to read it, because a procedure charges the reader for every line.

#### 1.2 · Graduation is a copy, not a move
(the face is the only record of WHY, and that is what a skill file must not carry)
When a face reaches `✅`, its `## Law` is copied into the owning skill: a `SKILL.md`, a stage contract, or a file under `ref/`.
From that moment the skill binds and the board does not.
The face stays behind.

#### 1.3 · `state:` here means the ruling only
(whether the code exists is a different fact, and it lives in Aims)
The four values are about the DECISION: `✅` ruled, `🟡` direction ruled with a named sub-ruling open, `🔴` nothing decided, `⏸️` deliberately not deciding.
That was settled on 260726, after pages sat `🟡` because an implementation was missing rather than because anything was undecided, which made the board's close condition unreachable and made 17 already-decided questions read as open.

#### 1.4 · A settled face with no Law is not finished
(graduation is ruled and mostly unexercised, and this is the board's largest gap)
Eleven of the sixteen `✅` faces carry no `## Law`, so nothing can graduate from them.
The board's own close condition depends on the mechanism that those faces never reach.

### 2 · Both halves, or neither

**The two-headed arrow**: why a graduation claim names both targets.

```text
 SEVEN groups land in ③ as well as ①.
 A Law applied to ONE side leaves a page and an implementation that
 disagree, and nothing detects it. Twice on 260726:

 ❌ chips SHIPPED in ③        while four faces here still called them unbuilt
 ❌ the round ruling landed    while haipipe-paper-round still described the
    HERE                       layer that ruling removed

 ⚖️ applied to one half, a ruling is a DEFECT, not partial success
```

🎓 Establishes that a ruling touching two skills is not graduated until it has landed in both.

#### 2.1 · The failure is silent, which is why the arrow is drawn with two heads
(nothing compares a board's Law against the two files it should have reached)
Both 260726 incidents were found by a person reading, not by a check.
Until something compares them, "graduated" means somebody remembered, and the table in `## Diagram` is the list of places to look.

### 3 · Not a runtime dependency

**One edge out, none in**: what may cross this folder's boundary.

```text
 ② ━▶ ① the skill set    OUT, and the ONLY outward edge that exists.
                         A ruling hits ✅, its Law is COPIED into a SKILL.md,
                         a stage contract, or a ref/ file
 ② ━▶ ⑦ the paper        NOTHING. A paper never reads this folder
 ② ━▶ ⑧ its board        NOTHING at runtime. A paper appears here only as
                         EVIDENCE inside an argument, which is a reading
 ① ━▶ ②                  🚫 FORBIDDEN. No skill may import, read, or require
                         a Q page
 🧱 the wall              NOT THIS FOLDER'S EDGE. A design board never asks
                         the banks anything; it argues about the rules for
                         asking, which is QC4b's subject
```

🗑 Establishes the asymmetry that makes this folder deletable, which is the only proof a design record has not become a runtime dependency.

#### 3.1 · Being deletable is the test, and it has never been run
(one edge out, none in, and everything else forbidden)
Delete this folder and `①` still works.
Nothing has ever checked that no runtime skill references a Q page, and `QA1` owes the same check from the other side, so the rule is stated twice and verified nowhere.

## Aims

### A1 · 📋 What a face holds, and what leaves it
- A1.1 · A face holds the argument and the skill holds the instruction.
  **Done when:** no face on this board carries a procedure a worker would follow, and no skill file carries the reasoning that produced its rule.
- A1.2 · Graduation copies the Law into the owning skill and leaves the face standing.
  **Done when:** every `✅` face names the file its Law was copied into, and that file contains it.
- A1.3 · `state:` on this board reports the decision, never the implementation.
  **Done when:** no page is 🟡 because code is missing, and implementation status appears only in Aims.
- A1.4 · Every settled face carries the Law it graduated.
  **Done when:** zero `✅` faces have no `## Law`.

### A2 · 🎓 Both halves, or neither
- A2.1 · A ruling that touches two skills lands in both before it counts as graduated.
  **Done when:** each of the seven two-target groups names both files, and something compares the board's Law against them.

### A3 · 🗑 Not a runtime dependency
- A3.1 · No runtime skill requires a Q page to exist.
  **Done when:** a check reports zero runtime references into this folder, from either side.

### P · 🏁 Page-level
- P1 · This page states no count that another page owns.
  **Done when:** no sentence here gives a number of folders, pairs or faces that `QA1` is the authority for.

## States

### A1 · 📋 What a face holds, and what leaves it
- ✅ A1.1 · Ruled and in use. The record-versus-manual distinction is the page's oldest settled content.
- ✅ A1.2 · Ruled. The copy-not-cut rule is stated and the graduation targets are tabulated in `## Diagram`.
- ✅ A1.3 · Pinned 260726 and applied to all faces then live; 17 moved 🟡 to ✅ without a ruling being made.
- ⬜ A1.4 · Eleven of sixteen `✅` faces carry no `## Law`. This is the largest gap on the board, and the close condition depends on it.

### A2 · 🎓 Both halves, or neither
- 🔨 A2.1 · The table exists and names both targets per group. Nothing compares it against the files, so both 260726 incidents would recur undetected.

### A3 · 🗑 Not a runtime dependency
- ⬜ A3.1 · Never checked, from either side. `QA1`'s `A2.3` owes the same check.

### P · 🏁 Page-level
- 🔨 P1 · Two stale counts were removed on 260802: "the easiest of the eight" and "there are four such pairs", both of which had outlived `QA1`'s map. The rule preventing a third is now in `## Writing Style`.

## Files

### 📋 Contracts · what CARRIES a rule to other pages
- `board.md`
  This board's index, its close condition, and the `state:` vocabulary this page rules.
- `../01-boardform-260722/`
  The board tool's own board, which rules what a board IS. Consulted here, never written.

### 🧪 Checks · what CATCHES a page breaking a rule
- `../../board/haipipe-board/cli/check.py`
  Reports page structure. It cannot tell whether a Law reached the skill it names, which is why `A2.1` is 🔨 rather than ✅.

### 📤 Output files · what a BUILD writes
- `../board/QA/QA3-the-skill-board.html`
  ⚠️ Generated by `cli/build.py`. Never hand-edit.

## Law

- A board holds the argument while the thing holds the instruction. A worker following a procedure never reads a Q face.
- When a face reaches `✅`, its `## Law` is COPIED into the owning skill file and the skill binds from then on. The face stays, as the record of why. A settled face with no `## Law` has nothing to graduate and is not finished.
- A ruling that touches two skills is graduated only when it has landed in both. Applied to one, it is a defect rather than partial success.
- `state:` on a design board is about the decision only. Whether the implementation exists is a separate fact and belongs in Aims.
- No runtime skill may import, read, or require a Q page: delete the board and the skill still runs. That delete test is the only proof available, because nothing else distinguishes a design record from a dependency.

## Lesson

- A count restated away from its owner is a count nobody revisits. This page said "the easiest of the eight" and "there are four such pairs" through two corrections to `QA1`'s map, because a reader fixing the map has no reason to grep for every page that quoted it.

## Glossary

- **Graduation**: copying a settled face's `## Law` into the skill it governs, after which the skill binds and the board does not.
- **The delete test**: removing a design board and checking that every skill still runs, which is the only available proof that a record has not become a dependency.

## Log

- 260806 0720 · [REVISE-CC] swept to the thin architecture (one door + stage data + board rental); the graduation table's landing files renamed to their live owners, since the routers and phase hubs they named are retired to `_old/`.

260802 · Migrated to the `QB4` page contract: Writing Style added, Content numbered into three divisions each with a face figure and caption, Aims regrouped as A1-A3 plus P with `Done when`, States mirrored one row per Aim, Files grouped by action. Two stale counts removed, and the rule preventing a third written into Writing Style. `QA10` added to the graduation table, which had not been updated when the prose verb was placed.

260727 · Audited against `board.md`'s decision-only rule, which says `state:` is about the DECISION and that implementation does not gate this board. Every open item was implementation or a test rather than an undecided question, so the page had been reporting itself as open because code was missing. Flipped with no ruling made.

260726 · `state:` pinned to mean the ruling only, and applied to all faces; 17 moved 🟡 to ✅ without a ruling being made. The graduation diagram now shows BOTH targets, because seven of thirteen groups land in both. Law generalized from one board to every thing/board pair.
