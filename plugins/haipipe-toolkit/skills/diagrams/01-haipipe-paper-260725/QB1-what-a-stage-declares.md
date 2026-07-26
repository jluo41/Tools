# Twenty-four fields in seven blocks, and the three readers of a stage
state: 🟡 PARTIAL
owner: JL
method: give every field a named reader; a field no reader asks for is decoration, and a reader that fails silently is where a stage half-works

## Question
What does one stage have to declare in order to actually run, and who reads each thing it declares? Adding a stage is cheap and we are open to more of them: one row in `stages/index.yml`, one folder, two files, no new skill and no version bump. The number of stages has never been the constraint. What is expensive is a stage that half-works, and every stage in this system is half-working in some field right now.

A stage is not an object anywhere in the code. It IS its `stage.md` frontmatter: twenty-four required fields in seven blocks, plus a conditional set. So "make one stage work well" is a concrete question about those fields, not an abstract one about design. Every field exists because some reader asks for it, and there are exactly three readers: the ROUTER that picks which stage is meant, the CREATOR that makes its page, and the EXECUTOR that does the work.

Only the first two are programs. `stages/index.yml` gives the router five fields, and `create-page.py` calls `values.get()` on exactly seven: `key`, `title`, `one_line`, `board_family`, `board_unit`, `template`, `artifact`. The other seventeen required fields are read by an AGENT, as prose. That asymmetry is the whole of this face. A field a program reads fails loudly, at run time, in front of somebody. A field an agent reads fails silently, and the symptom arrives weeks later as prose nobody can trace.

The failures are already on disk and they are all in the silent half. `4-display` declares `runs: once` while its work is eleven independently gated assets, so its gate accumulated a thirteen-record checklist and never closed. Twenty-two of thirty-one declared paths pointed at files that did not exist. Five of eight templates instruct a drafter to fill a filename retired in the S-face restructure, and nothing failed, because no program reads that line. `2a-venue` declares ten `done_criteria` and not one of them is machine-checkable. `gate_mode` acquired two contradictory homes and neither is populated. Every one of these is a field that only an agent reads.

So the useful test is not whether something deserves to be a stage. It is whether all three readers find what they need, and whether the seventeen fields nobody executes are being held up by anything other than attention. A ninth stage is welcome. What it costs is one more copy of the silent seventeen.

## Boundary
- ✅ Covered here
  What a stage declares, which reader consumes each block, where the silent failures are, and what it costs to add one.
- ↪ Covered elsewhere
  The PRODUCT block's template is `QB3` and its output is `QB6`; the BOARD block is `QB4`; the EXECUTION block is `QB7`; the EVIDENCE block is `QB9`; the CLOSING block is `QB11`; the conditional variation fields are `QB2`.

## Diagram
```
   A STAGE IS NOT AN OBJECT. It is 24 fields, and 3 readers of them.
   Two of the three are programs. The third is an agent, and that is
   where every measured failure lives.

   ┌─────────────────┬───────────────────────────┬───────────────────┐
   │ ① THE ROUTER    │ stages/index.yml          │  5 fields         │
   │   which stage   │ key order dir triggers    │  EVERY invocation │
   │   is meant      │ migrated                  │  fails 🔊 LOUD    │
   ├─────────────────┼───────────────────────────┼───────────────────┤
   │ ② THE CREATOR   │ create-page.py            │  7 fields         │
   │   make its page │ key title one_line        │  once per page    │
   │                 │ board_family board_unit   │  fails 🔊 LOUD    │
   │                 │ template artifact         │                   │
   ├─────────────────┼───────────────────────────┼───────────────────┤
   │ ③ THE EXECUTOR  │ an AGENT reading the      │ 17 fields         │
   │   do the work   │ contract as prose         │  every phase      │
   │                 │ everything else           │  fails 🔇 SILENT  │
   └─────────────────┴───────────────────────────┴───────────────────┘

   ── the seven blocks, and who asks for each ──────────────────────
      IDENTITY   key order title one_line             ① ②
      BOARD      board_family board_unit board_slug   ②        → QB4
      EXECUTION  phases gates probe_depth runs
                 needs_paper                             ③     → QB7
      PRODUCT    artifact template                    ②
                 sections formatting output              ③  → QB3 QB6
      EVIDENCE   probes q_id_pattern q_anchor            ③     → QB9
      GRAPH      upstream downstream handoff             ③
      CLOSING    done_criteria closed_when exit_when     ③     → QB11
      conditional  venue_aligned | venue_role
                   runs · unit · units · units_from       ③     → QB2
                   artifact_fallback · blocked_on      ②

   ── the silent seventeen, measured ───────────────────────────────
      4-display     runs: once, over 11 independently gated assets
                    ▸ a 13-record checklist that never closed
      31 paths      22 pointed at files that did not exist
      5 of 8        templates name a filename retired in the S-face
      templates     restructure. NOTHING FAILED: no program reads it
      2a-venue      10 done_criteria, 0 machine-checkable
      gate_mode     two declared homes that disagree, neither populated
      ⚠️ every one of these is in block ③. Not one is in ① or ②.

   ── the two blocks that no program will EVER read ────────────────
      GRAPH    upstream · downstream · handoff
               craft orientation, and explicitly NOT authoritative:
               the binding dependency is the S page's own `requires:`,
               which carries the upstream page's live gate state.
               Two declarations of the same thing, one of them advisory.
      CLOSING  done_criteria · closed_when · exit_when
               73 criteria across the eight; 7 machine-checkable.
               66 are judgments, and most of them SHOULD be.
      ⚖️ so "give it to a program" is not the answer to everything.
         The answer is to know which of the two a field is, and to
         stop the advisory ones from LOOKING binding.

   ── adding one costs four files, and nothing else ────────────────
      1  stages/index.yml            + ONE ROW, read on every run
      2  stages/<order>-<key>/       + ONE FOLDER
      3    stage.md                    24 required fields
      4    template.md                 the shape DRAFT fills   → QB3
      ✅ no new skill · no version bump · no router edit
      📍 the whole procedure is SKILL.md:193, one sentence.
      ⚠️ and the folder you ADD is not the folder it WRITES INTO:
         `artifact:` points into `0-lifecycle/<FAMILY>/`.      → QB4
```

## Content
### The three readers, and why only the third one hurts
```
 ① ROUTER    stages/index.yml       5 fields   every invocation
 ② CREATOR   create-page.py         7 fields   once per page
 ③ EXECUTOR  an agent, reading      17 fields  every phase
```
`①` and `②` are code, so their fields are load-bearing in the ordinary sense: get one wrong and something raises. `create-page.py` refuses a contract with no `template`, refuses an `artifact` that does not name a lifecycle directory, and refuses a `board_family` that is not a literal. Those refusals are the design working.

`③` is an agent reading prose, and it has no refusal at all. A wrong `probe_depth` does not raise; it changes what gets commissioned. A wrong `runs` does not raise; it produces a gate nobody can answer. A `done_criteria` list that cannot be checked does not raise; it produces a gate somebody passes anyway. This is why the eight stages have accumulated their defects in one place: seventeen twenty-fourths of every contract is enforced by attention.

### What "make one stage work well" actually means
It means closing the gap for the silent seventeen, and there are only three ways to do it. Move a field to a program, which is what `check-contracts.py` did for every declared path and what `check-probe-cards.sh` does for `probes:`. Move it to a human at a moment they are already looking, which is what `done_criteria` does at CHECK. Or delete it, which is what happened to `log:` and `inputs:`.

A field that is none of those three is decoration that looks like a contract, and decoration is worse than absence, because a reader trusts it.

### The block that declares the same thing twice
`upstream`, `downstream` and `handoff` describe which stages feed this one and what it passes on. None of them binds. The authoritative dependency is the S page's own `requires:`, because that one carries the upstream page's live gate state and cannot go stale. So the GRAPH block is orientation for a person, sitting in the same frontmatter, in the same syntax, as the fields that decide behaviour.

That is the sharpest instance of the general problem. Nothing in the file's shape tells you which fields are binding and which are advice, and a reader has no reason to guess correctly.

### A ninth stage is welcome, and here is its real price
Adding one is four files and no version bump, and the lifecycle is not a closed set. Compile, submit and answer-reviewers all sit outside the eight today, and none of those exclusions was argued in writing, so if one of them should become a stage the argument is available rather than blocked.

The price is not the row in the index. It is that a ninth stage arrives carrying seventeen fields that nothing checks, written by copying whichever neighbour the author happened to open. That is how `2a-venue` ended up with a three-phase list and no machine-checkable criterion, and how five templates kept a dead path: not by decision, by inheritance.

### Declaring something new on a stage
```
 a new lifecycle step                 →  index.yml row + folder + 2 files
 a new thing the stage PRODUCES       →  PRODUCT block         → QB3 QB6
 a new thing it must ASK for          →  EVIDENCE block        → QB9
 a new condition for being DONE       →  CLOSING block         → QB11
 a new way it VARIES per paper/venue  →  the conditional block → QB2
 a fact only a human needs            →  the craft prose BELOW the
                                         frontmatter, never a field
 a path that cannot resolve yet       →  `blocked_on: <Q page>` beside it
```

## Items to Finish
- [x] 📝 The eight questions are written down
      `PHILOSOPHY.md` carries them as a table; each `stage.md` repeats its own as `one_line`.
- [x] 📐 State the required fields, by measurement
      `CONTRACT.md`, from all eight contracts: 24 required, 43 stage-specific, plus the conditional set and two retired fields.
- [x] 🗂 Adding a stage costs four files and no more
      One index row, one folder, one contract, one template. No new skill, no version bump.
- [x] 🔧 Move every declared PATH to a program
      `check-contracts.py` resolves them; 22 of 31 were dead when it was first run.
- [ ] 🧠 Give each of the silent seventeen a named reader
      For every field: checked by a program, read by a human at a named moment, or deleted. A field that is none of the three is decoration that looks like a contract.
- [ ] 📐 Mark the advisory fields as advisory in the file
      `upstream`/`downstream`/`handoff` do not bind and sit in the same syntax as the fields that do. Nothing in the shape says which is which.
- [ ] ✍️ Put the add procedure where an adder will find it
      Four files, the seven blocks, the three readers. Today it is one sentence at `SKILL.md:193` and a field list in `CONTRACT.md`.
- [ ] 🧪 Write a ninth stage from the docs alone
      The acceptance test for this face, and the only way to find out what a copying author inherits.

## Where we are
The form is measured rather than inferred, and the loud half is in good shape: the router and the creator both refuse malformed contracts, and every declared path now resolves or carries `blocked_on:` with a reason.

The silent half is the work. Seventeen of twenty-four required fields are read by an agent as prose, and every measured defect in the eight contracts is in that group. Two of its three blocks will never be programs, which is correct and means the answer there is honesty about which fields bind rather than more automation.

Nothing here argues for fewer stages. It argues that a ninth should cost less than eight copies of the same unchecked seventeen.

## Files
- `stages/CONTRACT.md`
  The required core, measured across all eight, plus the conditional and retired fields.
- `stages/index.yml`
  Reader `①`. Its header states why it must stay small: it is read on every invocation.
- `haipipe-paper-stage/create-page.py`
  Reader `②`. Seven `values.get()` calls, and three explicit refusals.
- `haipipe-paper-stage/check-contracts.py`
  The one thing that moved a field out of the silent group.
- `haipipe-paper-stage/SKILL.md`
  Line 193 is the entire current add procedure.

## Law
A stage is not an object. It IS its `stage.md` frontmatter: twenty-four required fields in seven blocks, plus a conditional set, and a face that cannot name the field it would change has not finished its work.

Every field answers to a named reader. The ROUTER reads `stages/index.yml` on every invocation and it holds only what is needed to CHOOSE. The CREATOR reads seven fields to make the page. The EXECUTOR reads the rest, as prose, and cannot refuse anything.

A field must be checked by a program, read by a human at a named moment, or deleted. A field that is none of the three is decoration that looks like a contract, and a reader will trust it.

`upstream`, `downstream` and `handoff` are craft orientation and do not bind. The authoritative dependency is the S page's own `requires:`, because it carries the upstream page's live gate state and cannot go stale.

Adding a stage costs four files and nothing else: one row in `stages/index.yml`, one folder at `stages/<order>-<key>/`, its `stage.md`, its `template.md`. No new skill, no version bump, no router edit. The lifecycle is not a closed set, and a new stage is argued on what it must declare, not on whether it is allowed to exist.

A declared path that cannot resolve carries `blocked_on: <Q page>` with the reason. A dangling path with no `blocked_on` is a defect, and nothing may report it as green.

## Log
260726 · Rewritten twice. First from `_archive/QB1-what-is-a-stage.md`, which asked what a stage IS and answered it, into a gatekeeping question about refusing a ninth stage. JL corrected the premise the same day: adding stages is open, and the work is making ONE stage run well. Rebuilt again in `QA1`'s style around the enumeration that makes that concrete: 24 fields, 7 blocks, 3 readers. Counting the readers is what produced the finding, that `create-page.py` reads exactly seven fields and an agent reads seventeen, and that every measured defect across the eight contracts sits in the seventeen.
