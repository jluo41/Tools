# Which page does a stage write, how many of them, and who names it?
state: 🟡 PARTIAL
owner: JL
method: a contract declares what the page IS; board tooling composes what it is CALLED

## Question
A stage writes pages onto the board inside the paper, and three things have to be decided before it can: how many, which one, and what each is called. The naming half is settled and has teeth. The grain half, `runs:`, was ruled on 260726 and arrived here when its own face dissolved, because the identity fields that decide how many pages exist already lived on this page. The addressing half turns out to be more open than anyone noticed, because `QA6`'s one-family-one-folder ruling made the board's folders follow the S FAMILY, and the family list is not the stage list.

Naming first. A contract used to hold both a stable identity and a literal filename, and the literal copy went wrong silently. Two contracts broke on a single day from renames that were one-line moves on the board side: narrative moved family, display was split into eleven. Neither rename was wrong; both left this skill holding a stale name it does not own, and a wrong path fails when somebody runs the stage, not when they save the file. So a contract now declares `board_family` + `board_unit` + `board_slug`, and `haipipe-board/stage.py` composes `S-<Family>-<unit>-<slug>.md`.

Addressing second, and this is the open half. Board tooling knows seven families and eight stages write into six of them, so the mapping is not one to one in either direction. Three stages write into Venue. Two write into Work. Section-edit writes into Main or Appendix depending on the section, so one stage spans two families. Submission is a family with four pages and no stage. And Round, which `QA6` lists as an eighth family, is not a family that either program accepts. "One stage, one artifact" and "one family, one folder" are both true and they are not the same statement, and the difference between them is where every remaining open item on this page lives.

## Boundary
- ✅ Covered here
  How many pages a stage writes, which page each addresses, which side owns the filename, and what a contract stores instead of one.
- ↪ Covered elsewhere
  What the folders are is `QA6`; what a family means on the board is `QA7`; what shapes the page once it exists is `QB2a`; what happens when the page already exists is `QB2c`; what goes into it is `QB2d`.

## Diagram
```
   🏷 A NAME IS OWNED BY WHOEVER MAKES IT

   BEFORE, both sides held one          THE RULING
   ┌ stage.md ──────────────┐          ┌ stage.md ──────────────┐
   │ board_family: Venue    │ stable   │ board_family: Venue    │
   │ board_unit:   "2"      │ stable   │ board_unit:   "2"      │
   │ board_slug:   narrative│ stable   │ board_slug:   narrative│
   │ board_face:            │          └───────────┬────────────┘
   │  S-Venue-2-narrative ⚠️│ literal              │ resolve
   └────────────────────────┘          ┌───────────▼─────────────┐
                                       │ haipipe-board/stage.py  │
    a rename on the board side         │ resolve_filename()      │
    silently invalidated the copy      │ S-<Family>-<unit>-<slug>│
                                       └─────────────────────────┘

   ── the evidence: two contracts broke on ONE day ──────────────────
      3-narrative   moved FAMILY          one-line move, board side
      4-display     split into ELEVEN     one-line move, board side
      a wrong path fails at RUN time, not at edit time.

   ⚠️ ─────────────── AND THE HALF NOBODY RULED ─────────────────── ⚠️
      QA6 made the folders follow the FAMILY. The family list is not
      the stage list, in BOTH directions.

      STAGE              ──▶  FAMILY / unit      FOLDER (QA6)
      0-seed                  Seed 0             0-lifecycle/0-seed/
      1a-resource       ─┐    Work 0        ─┐
      1b-claims         ─┴──▶ Work 1        ─┴─  1-work/
      2a-venue          ─┐    Venue 0       ─┐
      2b-pitch           │    Venue 1        │
      3-narrative       ─┴──▶ Venue 2       ─┴─  2-venue/
      4-display               Display 0          3-display/
      5-section-edit    ─┬──▶ Main  <n>     ───  4-main/
                        └──▶ Appendix <A>   ───  5-appendix/
      ─────────────────────  ────────────────────────────────────
      (NO STAGE)              Submission         6-submission/  ⚠️
      (NOT A FAMILY)          Round ⛔           7-round/       ⚠️

      3 stages ──▶ 1 family (Venue)
      1 stage  ──▶ 2 families (section-edit, decided per section)
      1 family ──▶ NO stage: Submission, and it has 4 live pages

      ⛔ AND ROUND IS NOT A FAMILY, in either program.
         FAMILIES = (Seed Work Venue Display Main Appendix
                     Submission)      haipipe-board/stage.py:25
                                      check-contracts.py:40
         resolve_filename("Round", …) raises "family must be one of".
         The MISQ board.md has no `### S-Round` group, and 7-round/
         holds only _archive/ (the old 1-rounds/). QA6:192 lists it
         as the eighth family. The board and the code disagree.

      ❓ so "one stage, one artifact" and "one family, one folder"
         are two true sentences about different taxonomies, and the
         second one is what the folders are actually named after.

   ── how the address is resolved TODAY ─────────────────────────────
      create-page.py
        directory  =  dirname(artifact) with "0-lifecycle/" stripped
        family     =  board_family.title()      "Main or Appendix,
        unit       =  board_unit.upper()         according to
                                                 section_kind"  ⚠️
        slug       =  --slug OR board_slug OR key            :295
      ⛔ a dynamic family FAILS the resolver: "dynamic stage requires
         --family" :284, and a unit with a space fails at :286.
         section-edit must be told, per run, which family it is
         writing into. That is correct and it is undocumented.
      ⚠️ AND THE SLUG DOES NOT FAIL. It falls back to `key`, silently.
         It is the ONE field in this block with no refusal, and
         4-display is the one contract that has no `board_slug`, so
         the fallback takes key=display and composes
         S-Display-0-display.md, while the live page is
         S-Display-0-design.md. Off by one word, silently.

   ── the one address that still dangles ────────────────────────────
      4-display   artifact: 0-lifecycle/3-display/4-display.md
                  ⚠️ not an S-face name at all, and declared
                     `blocked_on: QB2b`. Its family folder is right and
                     its filename is pre-restructure. The file it names
                     is archived at 3-display/_archive/4-display.md;
                     the live brain is S-Display-0-design.md.
                  ⚠️ and 4-display/template.md:2 ALREADY says to copy
                     to S-Display-<N>-<slug>.md, so on this one point
                     the template is ahead of the contract.  → QB2a

   ── AND `blocked_on:` SUPPRESSES MORE THAN ITS OWN PATH ───────────
      check-contracts.py:101
        if runs == "once":
          if "blocked_on" in f:     ──▶ NOTE, and the branch ENDS
          elif no board_slug:       ──▶ problem
          else: compose + compare artifact filename
      ⇒ one line meant to excuse ONE unresolvable path also silences
        the board_slug requirement and the filename-agreement check.
        That is exactly why 4-display's MISSING `board_slug` has never
        been reported by anything. Six of eight contracts carry the
        field; 5-section-edit correctly omits it (CONTRACT.md:89: the
        slug is per unit when `runs: per-unit`); 4-display omits it
        with `runs: once`, which is a defect wearing a note.

   ── AND HOW MANY PAGES: `runs:` decides that, by the same gate ───
   once | per-unit ───────────────────────────────────────
      TEST   could a human APPROVE one unit and REJECT another?

      BEFORE  one artifact for 4-display
      ┌──────────────────────────────────────────────────┐
      │ gate: "is the display stage done?"               │
      │   display01 … display02 … display03 …  ×11       │
      │   different statuses · different source data ·   │
      │   different blockers                             │
      │   13-record checklist   ──▶   NEVER CLOSED  ⚠️    │
      └──────────────────────────────────────────────────┘
      AFTER   one page per asset
      ┌────────────┐┌────────────┐┌────────────┐
      │ display01  ││ display02  ││ display04  │  …
      │ gate: ✅    ││ gate: ⏳    ││ gate: ✅    │
      └────────────┘└────────────┘└────────────┘
       each question answerable in ONE sentence

      per-unit     4-display  ⚠️ still declares `once`
                   5-section-edit  ✅ already true
      once         0-seed · 1a-resource · 1b-claims ·
                   2a-venue · 2b-pitch · 3-narrative

      ⚠️ the rule is NOT "everything is per-unit". It is "per-unit
         where the WORK is per-unit", and the gate is the test.

      📍 ON DISK the AFTER picture already exists: 3-display/ holds
         12 pages, S-Display-0-design plus S-Display-1 through -11.
         So the split shipped, the brain became a page (0-design),
         and only the CONTRACT was left behind.

      ── and the grain is ALREADY half-checked ──────────────────────
         check-contracts.py:101  runs: once ⇒ board_slug, and the
                                 artifact filename must equal
                                 resolve_filename(family,unit,slug)
                          :114  runs: per-unit ⇒ unit + units_from
         CONTRACT.md:89-91       states both, in words
         ⛔ but `units:` is in neither REQUIRED nor any reader, so
            4-display naming its units with `runs: once` passes.
            THAT direction is the one assertion still missing.

   ── the cost this ruling accepts, stated fairly ───────────────────
      a literal path is greppable and needs nothing to follow. Remove
      it and a reader of stage.md, including an agent that has run
      nothing, cannot see which page is meant. For a file whose whole
      purpose is to be READ BEFORE ACTING that is a real loss. We took
      it anyway, because a silent wrong path is worse than an indirect
      right one.

   ── WHO READS THESE FIELDS, AND HOW THEY FAIL ────────────────────
      fields   board_family · board_unit · board_slug · artifact
      reader   ② THE CREATOR · create-page.py                   → QB1
      fails    🔊 LOUD on three of the four, and this is still the
               only face in the group whose block a program reads end
               to end. It refuses a missing family, a non-literal
               family, a family outside FAMILIES, an artifact outside
               the lifecycle directory, and two faces resolving one
               unit.
      ⚠️ ONE EXCEPTION, found 260727: `board_slug` has no refusal in
         create-page.py, only a silent fallback to `key` (:295). The
         loud check for it lives in check-contracts.py:104, and
         `blocked_on:` short-circuits past it three lines earlier.
      ⇒ which is why the naming half of this face reached ✅ and stayed
        there. Loud enforcement is not a coincidence here; it is the
        cause, and the one field with no refusal is the one field
        that turned out to be missing.
      to bind  the REOPENED half has no field at all. "a family with no
               stage" is an ABSENCE, and nothing can read an absence.
               It becomes checkable only by diffing `index.yml`'s
               families against FAMILIES and against the folders in
               `0-lifecycle/`. That diff is what would have caught
               Round, which is a folder no resolver can name.
```

## Content
### Why the name and the count are one question
This page holds two halves because the code holds them in one field group. `runs:` does not only say how many pages a stage writes; it decides WHICH identity fields the stage must carry. `check-contracts.py` branches on it: under `runs: once` a stage owes a `board_slug` and its `artifact:` filename must equal what `resolve_filename()` composes, and under `runs: per-unit` it owes `unit` and `units_from` instead, while its slug becomes a per-unit fact rather than a per-stage one. `CONTRACT.md:89-91` states the same pairing in words.

So there is no seam to weld here. Asking how many pages exist and asking what each is called are two readings of one block, and a stage that gets the grain wrong cannot get the name right: `4-display` declares `once`, therefore owes a slug, has none, and its `artifact:` names a file that was archived when the split shipped. One wrong field, three visible symptoms.

### Why the rename was nobody's fault
A skill that stores another skill's filenames inherits every rename that skill makes, and inherits it silently. Neither the narrative move nor the display split was a mistake, and both produced breakage in a third place, which is the signature of ownership sitting in the wrong file. `board_family: Venue` and `board_unit: "2"` are true regardless of what the file ends up called, and the board's tooling already turns a family and a unit into a filename, because that is what creates the page.

### The two taxonomies, and why the difference is real work
A STAGE is a unit of running: one question, one gate, one contract, one router row. A FAMILY is a unit of reading: where a page sits on the board so a person can find it. Those are different jobs and they were never going to line up, which is fine. What is not fine is that only one of them names the folders, so the folder tree answers "where do I read this" and says nothing about "what produced it".

The family with no stage is the sharp end, and it is one family, not two. Submission holds four pages (`S-Submission-0-reconcile` through `-3-submit`), is a real member of `FAMILIES`, and is written by nothing in `stages/index.yml`. So either the lifecycle is not the only thing that writes to the board, or Submission is a stage that was never declared.

Round is a different problem wearing the same coat. `QA6` records it as an eighth family made deliberately, but neither program agrees: `FAMILIES` has seven names, `resolve_filename()` refuses anything else, the MISQ `board.md` lists no `S-Round` group, and `7-round/` currently holds only the archived `1-rounds/`. So Round is a folder with no naming rule and no pages, which is not the same as a family with no stage, and merging the two cases is what hid that.

### The transitional case, and why it is declared
Papers that predate the S-face restructure carry their stage file under the old name. Each repointed contract declares `artifact_fallback:` for as long as any live paper is in that state, and a run must say which of the two it used. A deliberate exception with an expiry, not a second naming rule.

## Items to Finish
- [x] 🧠 Rule the naming
      Family plus unit plus slug, with resolution in board tooling.
- [x] 📐 Write the consequence down
      The pattern lives once, at `haipipe-board/stage.py:219-237`, so two implementations cannot disagree.
- [x] 🔧 Strip `board_face` from every contract
      Gone from all eight; the only surviving mention anywhere under `skills/paper/` is `haipipe-paper-stage/CHANGELOG.md:93`, as history.
- [x] 📐 Declare the transitional fallback
      `artifact_fallback:` on the six repointed contracts (`4-display` and `5-section-edit` have none), with the rule that a run says which it used.
- [x] 🧠 Rule the grain, with the test
      Per-unit exactly when units gate independently; one artifact otherwise.
- [x] 📐 Confirm which stages stay single
      Seed, resource, claims, venue, pitch and narrative are single-artifact by the same test, so it reads as a decision rather than as an omission.
- [x] 🔍 Half the grain check is already written
      `check-contracts.py:101-113` asserts `runs: once` implies a `board_slug` and an `artifact:` filename equal to `resolve_filename()`; `:114-117` asserts `runs: per-unit` implies `unit` and `units_from`; `CONTRACT.md:89-91` states both in words. Found 260727, and it means the remaining gap is one direction, not the whole rule.
- [ ] 🔧 Repoint `4-display`: add `board_slug: design`, move `artifact:`
      One contract, two lines, and they must land together because `check-contracts.py:108` composes the filename FROM the slug and compares it to `artifact:`. Today `stage.md:8-9` gives family and unit with no slug, and `:29` names `0-lifecycle/3-display/4-display.md`, which is archived at `3-display/_archive/4-display.md`; the live brain is `S-Display-0-design.md`. This is the item every other `blocked_on: QB2b` waits on.
- [ ] 🔧 Narrow `blocked_on:` so it stops hiding assertions
      `check-contracts.py:102-103` turns the entire filename branch into a note whenever `blocked_on:` is present, so `4-display`'s missing `board_slug` and its wrong `artifact:` filename are both suppressed by a field that was meant to excuse one unresolvable path. It should excuse the named path and nothing else.
- [ ] 🔧 Decide whether `Round` is a family at all
      `FAMILIES` at `haipipe-board/stage.py:25` and `check-contracts.py:40` both list seven names without Round, so `resolve_filename("Round", …)` raises; the MISQ `board.md` has no `S-Round` group and `7-round/` holds only `_archive/`. `QA6:192` lists Round as the eighth family. Either add it to both tuples or stop calling it a family.
- [ ] 📐 Migrate display to per-unit, and it is half done
      `5-section-edit` has the full set: `runs: per-unit`, `unit: section`, `units_from:` pointing at the narrative page, and a `board_family` resolved per section. `4-display/stage.md:25` still says `runs: once` while `:39` declares `units: displays/displayNN-<slug>/`, so it names its units and does not iterate them. Twelve pages already exist in `3-display/` (`S-Display-0-design` plus `-1` through `-11`), so what is missing is only `unit:`, `units_from:`, and an artifact pattern rather than a path.
- [ ] 🔍 Assert that `units:` implies `runs: per-unit`
      One line beside `check-contracts.py:114`. `units:` is in neither `REQUIRED` (`:31-39`) nor any reader, so `4-display` declaring units under `runs: once` passes every check today. This is the one direction of the grain rule that no program holds.
- [ ] 🧠 Rule what a family with no stage means
      `Submission` is a real family with four pages on disk (`S-Submission-0-reconcile` through `-3-submit`) and no row in `stages/index.yml`. Either the lifecycle is not the only writer to the board, or Submission is an undeclared stage. Round is not a second instance of this; it is the item above.
- [ ] 📐 Document the dynamic-family run
      `create-page.py:283-286` refuses a `board_family` containing " or " and a `board_unit` containing a space, demanding `--family` and `--unit` per run. Correct behaviour, stated in two error strings and nowhere else, and `5-section-edit` is the only stage it applies to.

## Where we are
Naming is implemented on both sides. `board_face` is gone from all eight contracts, `create-page.py` shells out to the Board primitive, and `resolve_filename()` is the single home of the pattern. The accepted cost is real and visible: reading a contract no longer tells you the filename, and nothing has gone wrong because of it.

One thing did go wrong, and it was found on 260727 rather than ruled: six of the eight contracts carry `board_slug`. `5-section-edit` omits it correctly, because a per-unit stage's slug is a per-unit fact. `4-display` omits it while declaring `runs: once`, which `check-contracts.py:104` exists to catch and never reports, because `blocked_on:` short-circuits the branch three lines earlier. So the naming half is settled as a RULING and has one contract out of compliance with it.

Addressing is where this page reopened. `QA6`'s one-family-one-folder ruling landed on 260726 and made the board's folders follow the family, and nothing since has said what that means for a stage. Submission is a family with pages and no stage, section-edit is one stage with two families, Round is a folder that no resolver can name, and the dynamic-family case is documented only in the error string that refuses it.

## Files
- `stages/*/stage.md`
  All eight carry `board_family` and `board_unit`, none carries `board_face`. Six carry `board_slug`: `4-display` and `5-section-edit` do not.
- `haipipe-paper-stage/create-page.py`
  Resolves the contract, strips `0-lifecycle/` off `artifact:` for the directory, and calls the Board's naming primitive. Refuses a non-literal family (:283) and a spaced unit (:286); falls back silently to `key` for the slug (:295).
- `haipipe-board/stage.py`
  `resolve_filename(family, unit, slug)` at :219-237 and the `resolve` verb: the one home of the rule. `FAMILIES` at :25 is the closed set of seven.
- `haipipe-paper-stage/check-contracts.py`
  :101-117, where `runs:` decides which identity fields are owed, and :102-103, where `blocked_on:` suppresses all of it.
- `stages/4-display/stage.md`
  The one contract with a pre-restructure `artifact:` (:29), no `board_slug`, and `units:` under `runs: once`.
- `stages/4-display/template.md`
  Line 2 already names the S-face target the contract does not.

## Law
A Paper stage declares the stable identity, `board_family` + `board_unit` + `board_slug`. Board tooling owns the literal `S-<Family>-<unit>-<slug>.md` filename and resolves or creates it from that identity. No stage contract stores a filename, and no layer repeats the pattern; anything that needs a name calls `stage.py`.

A declared path that cannot be resolved carries `blocked_on: <Q page>` with the reason. A dangling path with no `blocked_on` is a defect, and nothing may report it as green.

The unit follows the human gate, not the folder called a stage. A stage is `per-unit` exactly when one unit can be approved while another is rejected. By this rule Display and Section Edit are per-unit; Seed, Resource, Claims, Venue, Pitch and Narrative are single-output.

A stage repointed onto a new layout declares `artifact_fallback:` for as long as any live paper predates that layout, and a run says which of the two it used.

## Discussion
> CC 260727: the two family items are one judgment with two faces, and it is JL's. `FAMILIES` is a closed tuple of seven in two programs; a family is therefore whatever those tuples say, and everything else on the board is a folder. Under that reading Submission is a family with no stage, which is legal and means the lifecycle is not the only writer to the board, and Round is simply not a family, so `7-round/` is a folder holding an archive and `QA6:192` is the thing that is wrong.
> My recommendation: keep `FAMILIES` at seven and stop calling Round a family. Its cost is that when rounds do get pages, they cannot be S faces, so they get no `state:`, no gate, no `requires:` and no place in the board's `## Pages` grouping, which is most of what makes a lifecycle page useful. The alternative, adding "Round" to both tuples, costs one line in each and immediately owes an answer to "what writes an `S-Round-<n>` page", since no stage does. That is the same unanswered question as Submission, which is why I would settle Submission first and let Round follow it rather than deciding Round on its own.

## Log
260726 · Carried from `_archive/QB10-who-names-files.md`, which was ✅ and had teeth. Reopened to 🟡 the same day: `QA6` ruled one family one folder, which made the board's folders follow the S family, and measuring the eight contracts showed the family list and the stage list differ in both directions. Three stages write Venue, section-edit writes Main or Appendix per section, and Submission and Round are families no stage writes at all. The naming half stays settled; the addressing half was never asked.
260726 · Aligned against `QA6`, which had moved well past this group. This is where most of the misalignment landed, and it reopened the face: see the Log entry above.

260727 · The absorbed `runs:` half was welded to the naming half rather than left glued beside it, and measuring the eight contracts to do that turned up the defect the halves were hiding between them. `runs:` decides WHICH identity fields a stage owes (`check-contracts.py:101-117`, `CONTRACT.md:89-91`), so the count and the name are one block read two ways, and a new Content section says so first. Three claims on this page were wrong. Six of eight contracts carry `board_slug`, not eight: `5-section-edit` omits it correctly because a per-unit slug is per unit, and `4-display` omits it while declaring `runs: once`, which is a defect. Nothing reports that defect because `blocked_on:` at `check-contracts.py:102` short-circuits the whole filename branch, including the `board_slug` requirement and the filename-agreement assertion, so one field meant to excuse one path silences three checks. And Round is not a family: `FAMILIES` is seven names in both `haipipe-board/stage.py:25` and `check-contracts.py:40`, `resolve_filename` refuses anything else, the MISQ board has no `S-Round` group, and `7-round/` holds only the archived `1-rounds/`, so "two families with no stage" was one family (Submission, four pages) plus a folder with no naming rule. Also corrected: `board_slug` is the one field in this block with no loud refusal in `create-page.py`, which falls back to `key` at :295, so the face's "🔊 LOUD end to end" claim needed an exception, and the display split is 12 pages on disk rather than an intention. One item deleted as already true: "State the stage-to-family mapping somewhere" claimed nothing on either board says the two lists differ, while `QA6:191-192` and this face's own Diagram both say it. One `[x]` added for the half of the grain check that already exists.
