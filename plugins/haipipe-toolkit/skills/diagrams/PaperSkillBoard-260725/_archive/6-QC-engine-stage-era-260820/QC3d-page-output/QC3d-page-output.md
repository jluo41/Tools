# Which of the two files is the paper, and what is only generated from it?
state: 🟡 PARTIAL
owner: JL
method: one direction, no exceptions; then say what the rule means for the stages whose output is not prose

## Opening
A stage produces a page on the board and, downstream, the manuscript carries LaTeX that says the same things. Which of those two is the paper?
The answer has to be one of them, because the moment both are writable there are two manuscripts, only one of them is being reviewed, and the human editing either one cannot tell which they are looking at. That is the oldest failure in this system and it is not a subtle one: whichever copy somebody edits, the other is silently wrong from that instant.

The rule is that the `.md` is the paper and the `.tex` is a build product, generated in one direction and never read back. Prose authored into a `.tex` sits outside the record a human reviews, so sync will either overwrite it or silently keep it, and both of those are defects. Section-edit's own contract already warns that a second backward fill would overwrite authored prose with a build product.

What keeps it from being settled is no longer the mechanism. How a page becomes a `.tex`, what an extractor reads, and what happens when a coauthor edits the output are the sentence layer's questions, and they moved to `QBe3 §3` and `QBe3 §4` on 260726. What stays here is the part that is about a STAGE rather than about a section, and measuring it on 260727 moved both halves. The rule is declared on two stages, not one, under three different field names. And it is unstated for pitch and narrative, each of which has a standalone `.tex` sitting beside its S page on the MISQ paper that no field on either contract names. The sharper finding is that the rule is not merely unstated there: it is already broken in `appendices/`, where thirty-eight lines of authored prose live in a `.tex` that has no S page at all.

Scope: This page covers What a stage authors, what is generated from it, the direction, and the stages whose output is not prose. Neighbouring pages cover What the page is called is `QC3b`; what a re-run does to it is `QC3c`; the sentence-level shape an extractor relies on is `QC5`; HOW a page becomes LaTeX is `QBe3 §3` and how it becomes Word is `QBe3 §4`.

## Diagram
```
   ➡️ ONE DIRECTION, AND ONLY ONE

      S page  ## Content        THE PAPER: authored, reviewed, gated
           │
           │  sync              ✅  .md ──▶ .tex
           ▼                    ⛔  .tex ──▶ .md    NEVER
      sections/*.tex            A BUILD PRODUCT

   ── why it is not negotiable ──────────────────────────────────────
      two writable copies of one prose is the oldest failure here.
      Whichever one a human edits, the other is silently wrong, and
      the human cannot tell which one they are reading.

   ── what an extractor reads ───────────────────────────────────────
      ↪ NOT HERE. The `### §6.1` / `#### P1.` / `> lane` grammar and
        what each becomes is `QC5` and `QBe3 §3`. This face rules the
        DIRECTION; the sentence layer rules the mechanism.

   ── the open edge: the stages whose product is not a section ──────
      5-section-edit   .md ──▶ .tex                ✅ exact here
      4-display        generated: 4-display.tex    ✅ COVERED, and it
                       compiled:  4-display.pdf       says so itself:
                       "rebuilt wholesale by sync; hand-editing is a
                        defect". The computed ASSET is QD6's, not this
                        face's.
      2b-pitch         2b-pitch.tex     173 lines  ⛔ NO FIELD
      3-narrative      3-narrative.tex  211 lines  ⛔ NO FIELD
      measured 260727 on the MISQ paper: both sit in 0-lifecycle/
      2-venue/ beside their S pages, both last written 2026-07-18
      against pages last written 2026-07-26. 384 lines of .tex that
      no contract names and nothing declares stale.

   ── the rule IS a contract field, under THREE NAMES on TWO stages ─
      5-section-edit:53  output: sections/*.tex
                         # GENERATED from the .md by sync;
                         #   NEVER hand-authored
      4-display:36       generated: 0-lifecycle/3-display/4-display.tex
      4-display:37       compiled:  0-lifecycle/3-display/4-display.pdf
      ✅ those comments ARE this face's Law, declared where a machine
         reads it. `output:` is the only `output:` in the eight, which
         is literally true and hid the other two declarations of the
         same rule for a day.
      ⚠️ one law, three field names, and `../../paper/haipipe-paper-stage/stages/CONTRACT.md` lists
         them as unrelated stage-specific fields.
      📍 `sections/` is UNNUMBERED now (QA6's delete test), so a
         generated file ships and its source does not. The direction
         and the delete test agree, which is why both survive.

   ── the state it is in right now ──────────────────────────────────
      the rule       declared on two stages, with the reason
      the mechanism  ↪ NOT HERE. There is no generator, and what an
                     extraction step would have to do is `QBe3 §3`.
      ⚠️ so the direction is a DISCIPLINE, not a build step, and
         nothing on this face can be diffed. What CAN be checked here
         is not the content of a .tex but whether it has a source at
         all, and the measurement below says two of them do not.

   ── AND IT IS ALREADY BROKEN ON DISK  (measured 260727) ───────────
      the master .tex \inputs   9 section wrappers + 6 appendix ones
      all 15 pair to an S page in 4-main/ or 5-appendix/       ✅
      the two .tex files it does NOT \input are exactly the two with
      no S page anywhere:
        appendices/B_robustness_tables.tex        7 lines, 1 \input
        appendices/D_extended_literature_review.tex   38 lines of
          authored prose: \section + 4 \subsection + \citep keys.
          Its heading and every distinctive sentence in it appear on
          no S page in 0-lifecycle/, so no board check has ever
          resolved a single line of it
      ⇒ that is the two-manuscript failure this face's Law forbids,
        sitting in the repository. The pairing holds exactly where the
        master compiles and breaks exactly where it does not.

   ── WHO READS THESE FIELDS, AND HOW THEY FAIL ────────────────────
      ⚠️ SPLIT, like QC3a, and for the same reason.
      artifact:   reader ② THE CREATOR      fails 🔊 LOUD      → QC2
                  the page must resolve, and it does.
      output:     reader ③ THE EXECUTOR     fails 🔇 SILENT
      generated:  reader ③ THE EXECUTOR     fails 🔇 SILENT
                  and doubly so: nothing performs the step, so the
                  fields describe a discipline, and two of the eight
                  stages that need one declare no field at all.
      ⇒ the direction is a LAW with a loud half and an unexecuted half,
        which is exactly how a discipline decays without anyone noticing.
      to bind  `conform`'s check_structure.sh already walks BOTH trees:
               section G checks the `sections/` naming grammar and its
               numbering gaps, and the pass at :199 counts how many
               times each `.tex` is `\input`. Add one assertion: every
               wrapper `.tex` resolves to an S page in `4-main/` or
               `5-appendix/`, and every such page has a wrapper. That
               catches drift in both directions with no generator, and
               run today it fails on the two files above.
```

## Content
### Two copies is the failure, not the format
Nothing here is against LaTeX. The rule is about how many places a sentence can be authored, and the answer has to be one. A `.tex` that is generated is a projection and is safe to delete and rebuild; a `.tex` that somebody typed into is a second manuscript wearing the same name.

One consequence of that belongs here and the rest does not. What the direction requires of an extractor is that it be mechanical rather than interpretive, because an extractor that decides what a heading probably meant is writing prose nobody reviewed. What that extraction actually reads, drops and wires is `QBe3 §3`'s to rule, and is not restated here.

The coauthor who edits the `.tex` or the Word file and sends it back is `QBe3 §4`'s ruling, for the reason `QBe3 §4` gives: the edit is not hypothetical in the abstract, it is what happens when you hand somebody a Word file, so it settles where that file is made.

### Where this rule stops being exact
Section-edit produces prose and the rule fits it perfectly. Display fits it too, and says so on its own contract: `generated:` and `compiled:` name its `.tex` and its `.pdf`, and the comment beside them reads "rebuilt wholesale by sync; hand-editing is a defect". Its computed asset is a different question and it is `QD6`'s.

The two stages the rule does not reach are pitch and narrative. Each has produced a standalone `.tex` that lives beside its S page and is declared by nothing: 173 lines and 211 lines on the MISQ paper, both last written eight days before the pages they came from. That is not a rule about prose stages misapplied to non-prose ones, which is how this face had it. It is two stages that generate a document and declare no output at all, so nothing on disk says which of the two files is authored.

### The Law is already broken, and disk says where
`appendices/D_extended_literature_review.tex` is thirty-eight lines of authored prose with a `\section`, four `\subsection`s and its own citations, and no S page anywhere in `0-lifecycle/` carries its heading or any sentence in it. `appendices/B_robustness_tables.tex` is the same failure at seven lines: a `\section`, one paragraph, and an `\input` of a leaf whose only reference is that line, so the leaf is unreachable too. Neither wrapper is `\input` by the master, so neither is compiled, and both are invisible to every check that starts from a page.

That is the two-manuscript failure in its literal form: prose that exists only as a build product. It also settles the argument about whether this face's rule is theoretical. The rule is stated, the reason is stated, and the repository contains two counterexamples to it that nobody had looked for.

## Aims
- [~] ↪ MOVED to `QBe3 §3` · rule what sync reads · there is no generator · round-trip one section
      Three items left this page 260726 when JL opened the delivery columns. They are extraction and generation questions, which is what `QBe3 §3` owns; this face keeps the authority ruling, which is which of the two files is the paper.
- [~] ↪ MOVED to `QBe3 §4` · rule the external edit
      A coauthor edits the `.tex` or the Word file. The ruling belongs where the Word file is made, because that is the only reason the edit happens.
- [x] 📐 One direction only, declared where a machine reads it
      `../../paper/S06-main/section-edit/stage.md:53`: `output: sections/*.tex  # GENERATED from the .md by sync; NEVER hand-authored`. Measured 260727: the same law is also declared at `4-display/stage.md:36-37` as `generated:` and `compiled:`, so it is on two of the eight stages, not one.
- [ ] 🧠 Rule what an orphan `.tex` means
      `appendices/D_extended_literature_review.tex` is 38 lines of prose that exists only as a build product, which this face's Law forbids and the repository already contains; `appendices/B_robustness_tables.tex` is the same at 7 lines. Three answers: write the missing S page and regenerate, delete the file as abandoned, or declare that `appendices/` may carry hand-authored material and give up the direction for that folder. Nothing on disk says which, and both files are uncompiled, so the choice is free today and irreversible once somebody wants the text back.
- [ ] 🔍 Assert every delivered `.tex` resolves to an S page
      Measured 260727: the MISQ master `\input`s 9 section wrappers and 6 appendix wrappers and all 15 pair to a page in `0-lifecycle/4-main/` or `5-appendix/`; the two `.tex` files it does not `\input` are exactly the two with no page. `../../paper/container/haipipe-paper-conform/scripts/check_structure.sh` already walks both trees (section G, and the `\input`-count pass at line 199), so this is one added assertion to an existing script, and it fails today.
- [ ] 🔧 Give pitch and narrative a field for their `.tex`
      `0-lifecycle/2-venue/2b-pitch.tex` (173 lines, standalone `\documentclass`) and `3-narrative.tex` (211 lines) sit beside `S-Venue-1-pitch.md` and `S-Venue-2-narrative.md`, both written 2026-07-18 against pages written 2026-07-26. Neither `../../paper/S01-opening/pitch/stage.md` nor `../../paper/S02-work/narrative/stage.md` declares any output field, so 384 lines of `.tex` are governed by nothing.
- [ ] 📐 Declare the direction under ONE field name
      `output:` at `5-section-edit/stage.md:53`, `generated:` and `compiled:` at `4-display/stage.md:36-37`. One law, three names, listed in `../../paper/haipipe-paper-stage/stages/CONTRACT.md` as unrelated stage-specific fields. Pick one and record it there, or the next stage that generates something invents a fourth.

## States
The rule holds and is stated with its reason, on two contracts under three field names. It is unexecuted, because nothing performs the step; that is `QBe3 §3`'s to close and is not restated here.

What changed on 260727 is that "respected in practice on the MISQ paper" turned out to be true of everything the master compiles and false of everything it does not. Fifteen wrappers pair to a page. Two `.tex` files do not, and one of them is thirty-eight lines of prose with no page anywhere. So this face's state is not "a rule awaiting a mechanism"; it is a rule with two known violations and no check that would have found them.

The two stages the rule does not reach are pitch and narrative, each with an undeclared standalone `.tex` beside its page. Display is covered and says so itself.

## Files
- `../../paper/S06-main/section-edit/stage.md`
  Line 53 carries the law as `output:`, with the reason in the comment beside it.
- `../../paper/S05-display/display/stage.md`
  Lines 36 and 37, `generated:` and `compiled:`. The second stage that declares the direction, under two other names.
- `../../paper/S01-opening/pitch/stage.md` · `../../paper/S02-work/narrative/stage.md`
  The two contracts with no output field, whose pages each have a standalone `.tex` beside them.
- `appendices/D_extended_literature_review.tex` · `appendices/B_robustness_tables.tex`
  The two counterexamples: prose in a `.tex` with no S page, and neither one `\input` by the master.
- `../../paper/container/haipipe-paper-conform/scripts/check_structure.sh`
  Already walks `sections/`, `appendices/` and `0-lifecycle/`. Where the pairing assertion goes.

## Law

- The `.md` is the paper. The `.tex` is a build product, generated from it in one direction, and nothing reads back. A compiled artifact may never become the source of a claim, because at that moment two manuscripts exist and only one of them is reviewed.
- A delivered `.tex` with no S page behind it is not a build product, it is a second manuscript, whatever its filename says.
- Extraction is mechanical, not interpretive: an extractor that decides what a heading meant is a second author. That is a constraint the direction imposes on the extraction ruling; the ruling itself is `QBe3 §3`'s.

## Discussion
> CC 260727: on the orphan, I recommend writing the S page rather than deleting the file, and the two files should not get the same answer. `D_extended_literature_review.tex` is thirty-eight lines of real review prose with its own citations; deleting it costs nothing today and costs a rewrite the first time a reviewer asks for an extended literature treatment. The cost of the page is also real and worth naming: an `S-Appendix-<letter>` page is a gate, and this paper already carries forty S pages of which sixteen report an unconfirmed or blocked gate, so adding one adds a thing to confirm. `B_robustness_tables.tex` is seven lines and one `\input`, duplicating a letter `B_validation_details.tex` already owns, so it is the cheap opposite case and should probably just go. If you want one answer for both, delete both and accept that the review text is gone.

## Log
- 260726 · JL raised opening `QBe3 §3`/`QBe3 §4` for converting a stage page's Content into the sections, appendices, displays and a `paper-xxx.docx`. Routed here instead of opened: this face already owns the direction and the missing generator, `QD7` owns the several projections, `QBe3 §5` owns the adapters, and `QA6` ⑦ owns where the generated files land on disk. Splitting the same open items across a third group would have made four faces answer one question. Nothing about the question is new; what is missing is that this face's items are still open.
260726 · Carried from `_archive/QB9-artifact-and-tex.md` and retitled to the fork it actually turns on: what a stage AUTHORS versus what is merely generated. The format-projection half moved out to `QD7`, where Word and HTML already live.
260726 · Aligned against `QA6`, which had moved well past this group. `output: sections/*.tex` in the section-edit contract IS this face's Law declared where a machine reads it, and it is the only `output:` in the eight. `sections/` is unnumbered under the delete test, so the generation direction and the delete test agree.

260726 · Corrected while mapping the on-disk chain for `QC2`: the claim here had been that the generator's input path was stale. There is no generator. No script in the family turns a page into a section, so md-to-tex is a discipline an agent follows, and the round-trip test has nothing to diff against.

260726 · The move to `QB9a`/`QB9b` completed on this side. The pointers had been added while the four originals stayed open, so each item sat in two queues at once; the originals are gone and the pointers remain. What is left here is the stage-level half: the DIRECTION law, which governs all eight stages, and the one gap it does not cover, the two stages whose product is not prose. The mechanism (extraction, the missing generator, the round trip, the external edit) belongs to the sentence layer and is no longer restated here.

260727 · Measured against disk, and two claims moved. First, the direction is declared on TWO stages under THREE field names: `output:` at `5-section-edit/stage.md:53`, and `generated:` plus `compiled:` at `4-display/stage.md:36-37`, whose comment already reads "rebuilt wholesale by sync; hand-editing is a defect". So `output:` is the only `output:` and not the only declaration, and display is the covered stage rather than an uncovered one; its computed asset is `QD6`'s. What is uncovered is pitch AND narrative: `0-lifecycle/2-venue/2b-pitch.tex` (173 lines) and `3-narrative.tex` (211 lines) are standalone documents beside their S pages, written 2026-07-18 against pages written 2026-07-26, and no field on either contract names them. Second, and this is the finding, the Law is already broken on disk. The MISQ master `\input`s 9 section wrappers and 6 appendix wrappers and all 15 pair to an S page; the two `.tex` files it does not `\input` are exactly the two with no page, and `appendices/D_extended_literature_review.tex` is 38 lines of authored prose whose heading and sentences appear nowhere in `0-lifecycle/`. That turned an abstract "restate the rule" item into a ruling over named files, and it makes the pairing assertion the cheapest useful thing on this face: `../../paper/container/haipipe-paper-conform/scripts/check_structure.sh` already walks both trees and would fail today.

260727 · Cut what `QB9a` and `QB9b` own. The missing-generator block left the Diagram and `## Where we are`, which now point at `QB9a`; the coauthor-edits-the-output paragraph left `## Content`, which now points at `QB9b` with `QB9b`'s own reason; and the Law's extraction sentence is kept as a constraint the direction imposes but hands the ruling to `QB9a`. Deleted the display half of "restate the rule for non-prose artifacts": `4-display` already declares `generated:` and `compiled:`, so that half was asking for something the contract does. What was left of the item is the pitch-and-narrative gap, which is now its own item with line counts and dates.
