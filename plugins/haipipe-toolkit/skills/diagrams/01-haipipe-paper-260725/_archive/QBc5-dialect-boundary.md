# The board runs paper code: where is that boundary?

state: ✅ RULED
owner: JL
method: keep the dialect inside the board, and make "the board does not depend on it" a test rather than a habit

## Question

To resolve `\citep{}` and `{VAL:?}`, the Board had to learn what a `.bib` is, what `1-probes/` is, and what a probe `state:` means. That code now sits in `haipipe-board/src/dialect_paper.py`. So a general-purpose rendering tool carries one specific paper's vocabulary. Is that the right place for it, and what stops it spreading?

`QBc1` already ruled the FILE question: one lifecycle page, two skills writing it. This is the CODE question, which that ruling does not reach. It surfaced on 260726 while building `QC1` and `QC2`, and it was worth naming rather than absorbing.

## Boundary

- ✅ Covered here
  Where dialect code lives, what a dialect module may contain, and the test that keeps the Board independent of it.
- ↪ Covered elsewhere
  Who owns which SECTION of a shared page is `QBc1`. What the markers mean is `QC1` through `QC4`. What a Display renderer may own is `QD1`.

## Diagram
```
 THE BOARD LEARNED WHAT A .bib IS. WHERE IS THAT ALLOWED TO LIVE?

 THE THREE SHAPES
  A  the BOARD ships the dialect                            ◄ CHOSEN
     one build pass · chips can never be stale · one place
     enforces the board's own invariants
     cost: board/ carries paper words
  B  the PAPER ships it, the board loads it by convention
     clean ownership
     cost: a plugin ABI to version, and the board can no longer
           GUARANTEE what a dialect emits
  C  pre-resolve into the .md before the build
     ⛔ REJECTED: rewrites authored files, and goes stale the
        moment the .bib changes

 WHY A IS SAFE: THE CUT ALREADY FELL IN THE RIGHT PLACE
 ┌ dialect_paper.py ─────────┐   ┌ body.py ────────────────────┐
 │ GRAMMAR + RESOLUTION      │   │ MECHANISM                   │
 │ what \citep{} looks like  │──►│ WHEN a marker may be         │
 │ what a probe state means  │   │   rewritten                  │
 │ where .bib / 1-probes live│   │ what a chip IS · title= as    │
 │ returns (state,label,tip, │   │   the floor · the panel       │
 │          meta) — DATA     │   │ never inside a code span      │
 │ ⛔ never renders           │   │ ⛔ never learns what a paper is│
 └───────────────────────────┘   └─────────────────────────────┘
 the module boundary MATCHES the ownership boundary.

 THE LAW, AND IT IS EXECUTABLE
   ┌──────────────────────────────────────────────────────────┐
   │ delete src/dialect_paper.py and the board still builds.  │
   │ every board that does not declare `dialect: paper`        │
   │ renders BYTE-IDENTICAL.                                   │
   └──────────────────────────────────────────────────────────┘
   verified 260726:  design board  0b9b8fca ──► 0b9b8fca  ✅
                     MISQ board    degrades to plain text  ✅

 WHY A DELETE-TEST AND NOT A PRINCIPLE
   nobody will move dialect_paper.py into body.py.
   what WILL happen is one paper-shaped `if` inside a generic
   function, and that breaks the hash.
```

## Content

### Why shape A, stated as a trade rather than a preference
The Diagram lays out the three. B is the one that deserves an argument rather than a dismissal: it buys clean ownership and sells the single property that makes a chip trustworthy, which is that the board can assert what came out of a dialect. Every invariant the board enforces (no chip inside a code span, no evidence that vanishes when scripts are stripped, no marker rewritten in a discussion lane) is enforceable only because the board owns the rewriting step.

With exactly one dialect in existence, a plugin ABI is a cost with no buyer. The trigger for revisiting is named rather than left to taste: a SECOND dialect.

### The law is a test, and that is the point
`build.py` guards the import behind the declaration and catches `ImportError`, so a missing dialect degrades to plain text rather than crashing. Verified 260726 by moving the module aside and rebuilding both boards.

Stating it as a delete-test rather than a principle is what catches the real failure. Nobody is going to move `dialect_paper.py` into `body.py`; what will happen is one paper-shaped `if` inside a generic function, and that breaks the hash.

### What a dialect module may not do

- It may not render. It returns `(state, label, tooltip)`; `body.py` decides what a chip is.
- It may not write. It reads a paper tree and holds an index, and nothing else.
- It may not be reached unless a board declared it. The declaration is on the board, never a default.

## Items to Finish

- [x] 🧠 Rule where dialect code lives
      Shape A, inside the board, with the boundary stated rather than assumed.
- [x] 🔒 Make the independence claim executable
      Guarded import in `build.py`, plus the byte-identical delete-test.
- [ ] 🧪 Put the delete-test in the build rather than in a session
      It was run by hand. It should run as an assertion or a small check, or it decays into a claim.
- [ ] 📐 Write the rule where a dialect author reads it
      `SKILL.md` says nothing about dialects, so the second one will be written by copying the first and its constraints will travel only by imitation.
- [ ] 🧠 Decide the trigger for revisiting shape B
      Name the condition, most likely a second dialect, so the choice is not re-argued from scratch each time.

## Where we are

Ruled and enforced for the one dialect that exists. The rule is verified but not automated, and it is not written anywhere a future dialect author would look. Both gaps are items above, and neither blocks the remaining `QC` and `QD` slices.

## Law

- Dialect code may hold grammar and resolution. Rendering, invariants and file writing stay with the Board.
- A dialect is DELETABLE: the board must build without it, and boards that do not declare it must render byte-identical.
- A dialect is opted into by a declaration on the board, never by detection.

## Log

- 260726 · Raised while building `QC2`, when JL asked whether paper work keeps forcing changes to `haipipe-board`. It does, and `QBc1` did not cover it: that page rules the shared FILE, this one rules the shared CODE. Ruled A, and turned the independence claim into a test the same day.

## Files

- `haipipe-board/src/dialect_paper.py`
  The only paper-aware module in the Board.
- `haipipe-board/build.py`
  The guarded import and the declaration check.
- `haipipe-board/src/body.py`
  The mechanism half: `cite_chips()` and the code-span guard.
