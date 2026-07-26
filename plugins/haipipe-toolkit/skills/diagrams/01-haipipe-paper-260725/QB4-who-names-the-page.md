# Which page does a stage write, and who names it?
state: 🟡 PARTIAL
owner: JL
method: a contract declares what the page IS; board tooling composes what it is CALLED

## Question
A stage writes one page onto the board inside the paper, and two things have to be decided before it can: which page, and what that page is called. The naming half is settled and has teeth. The addressing half turns out to be more open than anyone noticed, because `QA6`'s one-family-one-folder ruling made the board's folders follow the S FAMILY, and the family list is not the stage list.

Naming first. A contract used to hold both a stable identity and a literal filename, and the literal copy went wrong silently. Two contracts broke on a single day from renames that were one-line moves on the board side: narrative moved family, display was split into eleven. Neither rename was wrong; both left this skill holding a stale name it does not own, and a wrong path fails when somebody runs the stage, not when they save the file. So a contract now declares `board_family` + `board_unit` + `board_slug`, and `haipipe-board/stage.py` composes `S-<Family>-<unit>-<slug>.md`.

Addressing second, and this is the open half. Eight stages write into eight families and the mapping is not one to one in either direction. Three stages write into Venue. Two write into Work. Section-edit writes into Main or Appendix depending on the section, so one stage spans two families. And two families, Submission and Round, have no stage at all. "One stage, one artifact" and "one family, one folder" are both true and they are not the same statement, which nothing on either board says out loud.

## Boundary
- ✅ Covered here
  Which page a stage addresses, which side owns the filename, and what a contract stores instead.
- ↪ Covered elsewhere
  What the folders are is `QA6`; what a family means on the board is `QA7`; how many pages a stage makes is `QB2`; what happens when the page already exists is `QB5`; what goes into it is `QB6`.

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
      (NO STAGE)              Round              7-round/       ⚠️

      3 stages ──▶ 1 family (Venue)
      1 stage  ──▶ 2 families (section-edit, decided per section)
      2 families ──▶ NO stage at all

      ❓ so "one stage, one artifact" and "one family, one folder"
         are two true sentences about different taxonomies, and the
         second one is what the folders are actually named after.

   ── how the address is resolved TODAY ─────────────────────────────
      create-page.py
        directory  =  dirname(artifact) with "0-lifecycle/" stripped
        family     =  board_family.title()      "Main or Appendix,
        unit       =  board_unit.upper()         according to
                                                 section_kind"  ⚠️
      ⛔ a dynamic family FAILS the resolver: "dynamic stage requires
         --family". section-edit must be told, per run, which family
         it is writing into. That is correct and it is undocumented.

   ── the one address that still dangles ────────────────────────────
      4-display   artifact: 0-lifecycle/3-display/4-display.md
                  ⚠️ not an S-face name at all, and declared
                     `blocked_on: QB2`. Its family folder is right and
                     its filename is pre-restructure.

   ── the cost this ruling accepts, stated fairly ───────────────────
      a literal path is greppable and needs nothing to follow. Remove
      it and a reader of stage.md, including an agent that has run
      nothing, cannot see which page is meant. For a file whose whole
      purpose is to be READ BEFORE ACTING that is a real loss. We took
      it anyway, because a silent wrong path is worse than an indirect
      right one.
```

## Content
### Why the rename was nobody's fault
A skill that stores another skill's filenames inherits every rename that skill makes, and inherits it silently. Neither the narrative move nor the display split was a mistake, and both produced breakage in a third place, which is the signature of ownership sitting in the wrong file. `board_family: Venue` and `board_unit: "2"` are true regardless of what the file ends up called, and the board's tooling already turns a family and a unit into a filename, because that is what creates the page.

### The two taxonomies, and why the difference is real work
A STAGE is a unit of running: one question, one gate, one contract, one router row. A FAMILY is a unit of reading: where a page sits on the board so a person can find it. Those are different jobs and they were never going to line up, which is fine. What is not fine is that only one of them names the folders, so the folder tree answers "where do I read this" and says nothing about "what produced it".

The two families with no stage are the sharp end. Submission and Round both hold pages and neither is written by anything in `stages/index.yml`, so either the lifecycle is not the only thing that writes to the board, or those two are stages that were never declared. Round is the more interesting case, because it was deliberately made a family rather than a stage.

### The transitional case, and why it is declared
Papers that predate the S-face restructure carry their stage file under the old name. Each repointed contract declares `artifact_fallback:` for as long as any live paper is in that state, and a run must say which of the two it used. A deliberate exception with an expiry, not a second naming rule.

## Items to Finish
- [x] 🧠 Rule the naming
      Family plus unit plus slug, with resolution in board tooling.
- [x] 📐 Write the consequence down
      The mapping stated once, in `stage.py`, so two implementations cannot disagree.
- [x] 🔧 Strip `board_face` from every contract
      All eight carry identity only; `create-page.py` delegates the filename to `haipipe-board/stage.py`.
- [x] 🛟 Declare the transitional fallback
      `artifact_fallback:` on each repointed contract, with the rule that a run says which it used.
- [ ] 🧠 Rule what a family with no stage means
      Submission and Round both hold pages and neither appears in `stages/index.yml`. Either the lifecycle is not the only writer to the board, or those two are undeclared stages. Round was made a family on purpose, so the answer is probably the first, and it is not written down.
- [ ] 📐 State the stage-to-family mapping somewhere
      Three stages write Venue, one writes Main or Appendix depending on the section. Nothing on either board says the two lists differ, so a reader assumes a folder per stage and finds a folder per family.
- [ ] 📐 Document the dynamic-family run
      `create-page.py` refuses a `board_family` that is not a literal and demands `--family`. Correct behaviour, stated in an error string and nowhere else.
- [ ] 🔧 Give display a real S-face address
      `artifact: 0-lifecycle/3-display/4-display.md` is a pre-restructure filename in a correct family folder, declared `blocked_on: QB2`.

## Where we are
Naming is implemented on both sides. All eight live contracts carry identity without `board_face`, `create-page.py` shells out to the Board primitive, and `resolve_filename()` is the single home of the pattern. The accepted cost is real and visible: reading a contract no longer tells you the filename, and nothing has gone wrong because of it.

Addressing is where this page reopened. `QA6`'s one-family-one-folder ruling landed on 260726 and made the board's folders follow the family, and nothing since has said what that means for a stage. Two families have no stage, one stage has two families, and the resolver already refuses a dynamic family with an error message that is the only documentation of the case.

## Files
- `stages/*/stage.md`
  All eight carry `board_family`, `board_unit` and `board_slug`, without `board_face`.
- `haipipe-paper-stage/create-page.py`
  Resolves the contract, strips `0-lifecycle/` off `artifact:` for the directory, and calls the Board's naming primitive. Refuses a non-literal family.
- `haipipe-board/stage.py`
  `resolve_filename(family, unit, slug)` and the `resolve` verb: the one home of the rule.
- `stages/4-display/stage.md`
  The one contract whose `artifact:` is still a pre-restructure filename.

## Law
A Paper stage declares the stable identity, `board_family` + `board_unit` + `board_slug`. Board tooling owns the literal `S-<Family>-<unit>-<slug>.md` filename and resolves or creates it from that identity. No stage contract stores a filename, and no layer repeats the pattern; anything that needs a name calls `stage.py`.

A declared path that cannot be resolved carries `blocked_on: <Q page>` with the reason. A dangling path with no `blocked_on` is a defect, and nothing may report it as green.

A stage repointed onto a new layout declares `artifact_fallback:` for as long as any live paper predates that layout, and a run says which of the two it used.

## Log
260726 · Carried from `_archive/QB10-who-names-files.md`, which was ✅ and had teeth. Reopened to 🟡 the same day: `QA6` ruled one family one folder, which made the board's folders follow the S family, and measuring the eight contracts showed the family list and the stage list differ in both directions. Three stages write Venue, section-edit writes Main or Appendix per section, and Submission and Round are families no stage writes at all. The naming half stays settled; the addressing half was never asked.
260726 · Aligned against `QA6`, which had moved well past this group. This is where most of the misalignment landed, and it reopened the face: see the Log entry above.
