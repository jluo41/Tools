# Who names the files: the skill, or the board?
state: ✅ SETTLED
owner: JL
method: rule whether a contract stores a path or a family plus unit

## Question
Should a stage contract hardcode the filename of the page it writes, or declare what the page IS and let the board resolve the name?

Today it does both. Each contract carries `board_family` and `board_unit`, which are stable facts about the work, and `board_face`, which is a literal path. Whenever the board renames a page, the literal copy is silently wrong.

## Boundary
- ✅ Covered here
  Which side owns filenames, and what a contract stores.
- ↪ Covered elsewhere
  How many files there are is `QB4`; what is in them is `QC1`.

## Content
### The evidence
Two contracts broke on a single day, both from renames that were one-line moves on the board side: the narrative page moved family, and the display page was split into eleven. Neither rename was wrong; both left this skill holding a stale copy of a name it does not own.

A skill that stores another skill's filenames inherits every rename that skill makes, and inherits it silently, because a wrong path fails at run time rather than at edit time.

### The alternative
`board_family: Venue` and `board_unit: "2"` are true regardless of what the file is called. The board's own tooling already turns a family and a unit into a filename, because that is what creates the page. Resolution belongs where the naming rule lives.

### The counter-argument, stated fairly
A literal path is greppable and needs nothing to follow. Remove it and a reader of `stage.md`, including an agent that has not run anything yet, cannot see which page is meant. For a file whose whole purpose is to be read before acting, that is a real loss.

## Law
A Paper stage declares the stable identity, `board_family` + `board_unit`. Board tooling owns the literal `S-<Family>-<unit>-<slug>.md` filename and resolves or creates it from that identity.

The public Paper creator may ask the Board primitive to name the page; no stage contract stores `board_face`.

## Items to Finish
- [x] 🧠 Rule it
      Family plus unit with resolution in the board's tooling; or keep the literal path and accept a rename duty on both sides.
- [x] 📐 Write the consequence down
      If resolved: the mapping, in one sentence, so both skills implement the same one. If literal: that a board rename is incomplete until the contract naming it is updated, written where the renamer will see it.

## Where we are
Implemented in the Paper Stage contract and creator. All eight live stage contracts now carry identity only; `create-page.py` delegates filename construction to `haipipe-board/stage.py`.

## Files
- `stages/*/stage.md`
  All eight carry `board_family` and `board_unit`, without `board_face`.
- `haipipe-paper-stage/create-page.py`
  Resolves the selected contract and calls the Board's naming primitive.
