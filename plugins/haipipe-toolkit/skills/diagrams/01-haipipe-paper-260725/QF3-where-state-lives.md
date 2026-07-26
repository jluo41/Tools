# Where paper-level state lives
state: 🟡 PARTIAL
owner: JL
method: one register; everything else mirrors it

## Question
Which page is the paper currently working on, and which record answers that question?

For most of this skill's life the answer lived in `STATUS.md`: a `current_layer` field plus a gate ledger, both hand-maintained. On 2026-07-25 that answer changed on the consuming paper, and the change is worth generalizing or rejecting deliberately rather than by drift.

## Boundary
- ✅ Covered here
  Where the frontier and the gate record live, and which copy is authoritative.
- ↪ Covered elsewhere
  What a gate MEANS is `QB3`; the two orthogonal axes of frontier and maturity are design vocabulary from `PHILOSOPHY.md`.

## Content
### What went wrong with the hand-maintained version
`STATUS.md` disagreed with itself. Its restart note and its gate ledger pointed at different frontiers, and an embedded check block recorded that `current_layer` had been left untouched because the contradiction needed a human ruling. A whole board face existed for months to resolve which of two fields in one file was true.

### The ruling that replaced it
The frontier is READ, not stored: it is the earliest page in the pipeline whose gate has not passed, and every page carries its own `state:`. `STATUS.md` mirrors the board rather than deciding it. A hand-written pointer to the current stage is exactly what started disagreeing with the gate record, so it stopped being written.

### What is unsettled
That ruling was made on one paper. The skill still describes `STATUS.md` as the machine state each stage updates, so a stage worker following its contract would keep writing a field that no longer decides anything. Either the skill adopts the ruling, or the paper is out of step with its own skill.

## Items to Finish
- [x] 🧭 The frontier is derived, on the consuming paper
      Read off the pipeline from the pages' own `state:` lines; `STATUS.md` mirrors.
- [ ] 🧠 Rule whether this generalizes
      Adopt it in the skill, or state that the MISQ paper is an exception and say what makes it one.
- [ ] 📐 Say what `STATUS.md` is still FOR
      Maturity, round state and the human gate ledger may still belong to it. Frontier does not. Draw that line rather than leaving the file half-authoritative.

## Where we are
Ruled on one paper, unadopted by the skill. The two are currently in a state where following the contract would undo the ruling.

## Files
- `PHILOSOPHY.md`
  The frontier and maturity axes.
- `0-lifecycle/board.md`
  Carries the ruling in its Topic and Pipeline.
