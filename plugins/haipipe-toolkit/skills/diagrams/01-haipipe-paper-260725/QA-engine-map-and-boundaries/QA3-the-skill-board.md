# ② The skill board: what is argued, and what leaves
state: ✅ SETTLED · the Law-copy and the no-dependency proof are open in Items
owner: JL
method: keep the reasoning here, copy only the ruling out, and never let runtime depend on either

## Question
What belongs on the design board for a skill, and what happens to a question once it is answered? This is the folder you are reading, and it is the easiest of the eight to get wrong, because it looks like documentation and is not: documentation is what a worker follows, and this is the argument that produced it.

This is the folder you are reading. It is the easiest of the eight to get wrong, because it looks like documentation and is not: documentation is what a worker follows, and this is the argument that produced it. The failure mode is that it becomes a second manual, drifts from the first, and a fresh agent cannot tell which one binds.


The way through is to keep the reasoning here and copy only the ruling out, so a `## Law` graduates into the skill it governs while the argument that produced it stays behind. What we want at the end is a board that could be deleted without breaking anything: if a skill ever needs a Q page to run, something has been filed in the wrong folder.
## Boundary
- ✅ Covered here
  What a design board holds, what leaves it when a question closes, and why nothing may depend on it.
- ↪ Covered elsewhere
  The paper board is the opposite object and is `QA7`; the skill a ruling graduates into is `QA2`; where any board lives on disk, and its face grammar, are ruled on the boardform board at its `QC1@boardform` and `QA2@boardform`.

## Diagram
```
   ┌──────────────────────────────────────────────────────────────────┐
   │  ② SKILL BOARD    skills/diagrams/01-haipipe-paper-260725/       │
   │                                                                   │
   │   Q face          the argument, the alternatives that were        │
   │    ├ Question     rejected, the evidence, and the ruling once     │
   │    ├ Content      it is made                                      │
   │    ├ Items        what is still owed                              │
   │    └ Law    ◀───── the ONE part that is meant to LEAVE            │
   └───────────────────────────┬──────────────────────────────────────┘
                               │  state: ✅  →  copy the Law out
              ┌────────────────┴────────────────┐
              ▼                                 ▼
   ┌────────────────────────┐        ┌────────────────────────────────┐
   │ ① haipipe-paper        │        │ ③ haipipe-board                │
   │      paper family      │        │  first-class Board family     │
   └────────────────────────┘        └────────────────────────────────┘
     from here on THIS binds,          and for many rulings, SO DOES
     not the board                     THIS. Both halves, or neither.

```

```
   ── which group lands where ────────────────────────────────────────
      group                    → ①  haipipe-paper        → ③  haipipe-board
      ──────────────────────   ─────────────────────────  ─────────────────
      QA1  eight folders         README · PHILOSOPHY        —
      QA2  the skill set       the tree · front door      —
      QA3  the skill board     —  (it rules ② itself)     —
      QA6  the paper           paper-folder · enter       —
      QA7  the paper board     paper-round  ← owed        the S-family list
      QA4  the tool            create-page.py             the whole package
      QA8  who owns a region   create-page.py             stage.py · serve.py
      QA9  driving work        haipipe-paper-stage        serve.py
      QB1-3  adding a stage   index.yml · CONTRACT.md    —
      QB2b-6  the page written create-page.py · stage.py  —
      QB3-11 the four phases  2-phase/ · ref/08-stage   —
      QC   the sentence        draft-* · revise-place     src/body.py
                               5-section-edit/template    src/dialect_paper.py
      QD   the display         1-lifecycle/4-display/     (display/ family)

```

```
   ── the failure this two-headed arrow exists to name ───────────────
      SEVEN groups land in ③ as well as ①. A Law applied to one side
      only leaves a page and an implementation that disagree, and
      nothing detects it. Twice on 260726:
        chips SHIPPED in ③, four faces here still called them unbuilt
        the round ruling landed HERE, haipipe-paper-round still
          described the layer it removed
      A ruling that touches both halves is not graduated until it has
      landed in both. Applied to one, it is a defect, not partial
      success.

```

```
   ── and the face itself does not move ──────────────────────────────
      the Law is COPIED, never cut. The face stays as the record of
      WHY, which neither skill carries, because a worker reading a
      procedure pays for every line of it.

      ✗ delete this whole folder and BOTH skills still run.
        if that is ever untrue, something has been placed wrong.
```

## Content
### What a Q face holds
The argument, not the instruction. A face carries the question in its own words, the alternatives that were considered and rejected, the evidence that decided it, and the ruling as a `## Law` once there is one. A worker following a procedure should never need to read it.

### Graduation is a copy, not a move
When a face reaches `✅`, its `## Law` is copied into the owning skill: a `SKILL.md`, a stage contract, or a file under `ref/`. From that moment the skill binds and the board does not.

The face itself stays. It is the only record of why the rule is what it is, and that is exactly what a skill file must not carry, because a worker reading a procedure pays for every line of it.

### `state:` here means the ruling only
On this board the four values are about the DECISION and nothing else: `✅` the question is ruled, `🟡` the direction is ruled but a named sub-ruling is open, `🔴` nothing is decided, `⏸️` deliberately not deciding. Whether the code exists is a different fact and lives in `## Items to Finish`.

That was settled on 260726. Before it, a page sat `🟡` because an implementation was missing rather than because anything was undecided, which made the board's close condition unreachable and made 17 already-decided questions read as open.

### Not a runtime dependency
No skill may import from here, read a Q face at runtime, or require one to exist. Delete this folder and `①` still works. The board is where the skill was designed, not part of how it runs.

### What crosses this folder's edge
```
 ② ──▶ ①  the skill set     OUT, and it is the only outward edge that exists.
                            A ruling reaches ✅, its ## Law is COPIED into a
                            SKILL.md, a stage contract, or a ref/ file. The
                            face stays behind as the record of WHY.

 ② ──▶ ⑦  the paper         NOTHING. A paper never reads this folder.
 ② ──▶ ⑧  the paper board   NOTHING, at runtime. The MISQ paper appears on
                            these pages only as EVIDENCE cited in an argument
                            ("11 of 16 settled faces carry no Law"), which is
                            a reading, not a dependency.

 ① ──▶ ②                    FORBIDDEN. No skill may import, read, or require
                            a Q page. Delete this folder and ① still runs;
                            if that is ever untrue, something is placed wrong.

 the wall                   NOT THIS FOLDER'S EDGE. A design board never asks
                            the banks anything. It argues about the rules for
                            asking, which is `QB3b`'s subject, not its own.
```
The asymmetry is the point: one edge out, none in, and everything else forbidden. That is what makes this folder deletable, and being deletable is how you know a design record has not quietly become a runtime dependency.

## Items to Finish
- [x] 📚 A design board is a record, not a manual
      Q faces hold the argument; the skill holds the instruction.
- [x] 🎓 Graduation is a copy of the Law
      `✅` means the Law is copied into the owning skill file, and the face stays as the record of why.
- [x] 🧭 `state:` means the ruling, not the code
      Applied to all 34 faces on 260726; implementation status lives in Items.
- [x] 🗺 Say where each group's Law lands, in BOTH skills
      Seven of thirteen groups land in `③` as well as `①` (260726).
- [ ] 🧾 Write the Law on every settled face
      11 of the 16 `✅` faces carry no `## Law`, so nothing can graduate from them. That is the largest gap on this board.
- [ ] 🧪 Prove the no-dependency rule
      Nothing has ever checked that no runtime skill references a Q page. `QA1` owes the same check from the other side.

## Where we are
The record-versus-manual distinction and the graduation rule are ruled and in use. The `state:` vocabulary was pinned on 260726.

The gap is graduation itself: most settled faces have no `## Law` to copy, so the mechanism is ruled and mostly unexercised. The board's own close condition depends on it.

## Files
- `board.md`
  This board's index, close condition, and the `state:` vocabulary.
- `../01-boardform-260722/`
  The board tool's own board, which rules what a board IS.
- `PHILOSOPHY.md`
  One of the graduation targets named in the close condition.

## Law
EVERY thing has a board, and a board holds the argument while the thing holds the instruction. A worker following a procedure never reads a Q face.

There are four such pairs: `①`/`②` the paper skill, `③`/`④` the board tool, `⑤`/`⑥` the probe layer, `⑦`/`⑧` one manuscript. The first two behave alike, as a record whose rulings graduate out. The third is the exception ruled at `QA7`, because nothing graduates out of a paper board.

When a face reaches `✅`, its `## Law` is COPIED into the owning skill file and the skill binds from then on. The face stays, as the record of why. A settled face with no `## Law` has nothing to graduate and is not finished.

`state:` on a design board is about the decision only. No runtime skill may import, read, or require a Q page: delete the board and the skill still runs.

## Log
260727 · Audited against `board.md`'s decision-only rule, which says `state:` is about the DECISION and that implementation does not gate this board. Every open item here is implementation or a test, not an undecided question, so the page was reporting itself as open because code was missing. Flipped with no ruling made.
260726 · `state:` pinned to mean the ruling only, and applied to all faces; 17 moved 🟡→✅ without a ruling being made. The graduation diagram now shows BOTH targets, `①` and `③`, because seven of thirteen groups land in both. Law generalized from one board to every thing/board pair.
