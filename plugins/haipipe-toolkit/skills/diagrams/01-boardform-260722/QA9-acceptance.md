# Checking the page after every change
state: 🟡 PARTIAL
owner: CC
method: two checks on one trigger: assert that every documented construct still renders, and have a zero-background agent read the prose

## Question
After anything on a board changes, how do we find out that the page has stopped delivering what it promised, in structure or in prose, without waiting for JL to notice it?

A board is worth exactly what a second person can get out of it, so it can fail in two ways that look nothing alike from the inside.
It fails structurally when a construct stops rendering what the documentation says it renders, and it fails as writing when the sentences stop being followable by someone who was not in the room.
Both failures are invisible to the person who made them, and for the same reason: the author reads the page with everything they know already loaded, so a broken construct still looks like what they meant and an unreadable sentence still reads fine.
Both have happened repeatedly and both were caught by a human noticing, which is the part that does not scale.
On the structural side, three regressions landed on 260725 and 260726, and every one of them left the build green: `####` was flattened into the group-title construct so 113 paragraphs claimed to lead a run of items, the Opening disclosure moved onto the section name and left a shut row with the ruling's scope invisible inside it, and the drawer under the lead question ended up half iconed with its prose in the page's metadata voice.
On the writing side, the second cold read of this board graded one face incomprehensible and five half-understood while every structural check on those faces was passing, and the first one came back with the line that still describes the failure best: it explains the format of a recipe without ever saying what the dish is.
JL's rule sits above both: if it is not easy to read, writing that much is rubbish, and unreadable equals unwritten.
The two checks are different instruments and must stay different, but they answer to one trigger, because the thing that keeps failing is not either check: it is that nothing runs after a change.

## Boundary
- ✅ Covered here
  Both checks and the single trigger they share: asserting that each documented construct renders with the class the documentation names, running a zero-background reader over the prose, and deciding what happens when either comes back red.
  The rules the prose check enforces live in `ref/writing-rules.md`, which is this face's deliverable.
- ↪ Covered elsewhere
  What the template should say is `QA2` and what the page layout should be is `QA4`; this face only checks that what we generate is faithful to both.
  Whether a stranger can open a board at all from `SKILL.md` alone is `QB2`, which tests the handover rather than any one page.

## Diagram
```
  a change lands
       │   src/ · assets/board.css · any face's prose
       ▼
  ┌────────────────────────────────────────────────────────┐
  │  ONE TRIGGER, TWO CHECKS                                │
  └───────────┬──────────────────────────┬──────────────────┘
              │                          │
      STRUCTURE                     PROSE
      fixture: ref/q-template.md    fixture: every face of a real board
      copied twice, no editing      as its authors actually wrote it
        ├─ a Q face                 run by a fresh-context agent that
        └─ an S face                has never seen the project
              │                          │
        build.py                    answers exactly three things
              │                      ① which sentence is unreadable
        read the html                ② which word is never defined
              │                      ③ what premise is missing
        assert each construct             │
              │                          │
        boolean per row             a graded report per face
              │                          │
              └────────────┬─────────────┘
                           ▼
                  report, and JL decides
                  whether red blocks a change

  constructs asserted on the structural side
  ───────────────────────────────────────────────────────────
  lead is the door       ## Question lead      details.it.row.qd > summary
  Opening never folds    (renderer)            div.ch.opening-head
  drawer is flat         Boundary, contract    div.fh, no details inside
  drawer headings bare   (renderer)            no icon on any div.fh
  division               ### heading           details.csec
  paragraph heading      #### heading          div.ph, and never 🔹
  job line               (…) under a ####      div.pj
  group title            **a whole line**      div.gt > span.gi, keeps 🔹
  sentence apparatus     sentence then > lines details.sent > span.sbadge
  typed lane             > Citation: …         div.lane with its icon
  item with detail       - ICON head + indent  details.it.row
  finish count           - [ ] / - [x]         n/m in the section heading
  dated item             260723 CC · head      span.stmp
  code block             a fenced block        details.codef
  comment anchor         - [ ] JL 「sentence」  mark on that sentence

  ✗ the author re-reading their own page in the same conversation
    catches neither kind: too much unwritten context is already loaded
```

## Content
### The two checks are different instruments
The structural check asks a question with a fact for an answer, and the prose check asks one that requires judgment.
Whether `####` produced `div.ph` is decidable by a regex in milliseconds and is either true or false.
Whether a sentence packs three things into one is decidable only by a reader who does not already know which three, which is why it needs a fresh context and cannot be a pattern match.
Their fixtures differ for the same reason: the structural check runs on `ref/q-template.md`, the one file whose job is to be complete, while the prose check runs on a real board, because prose is only unreadable in the specific words someone wrote.
Merging them into one instrument would lose the more valuable one, since a structural pass is compatible with a page nobody can read, and that combination is exactly what the second cold read found.

### Why they share a trigger anyway
Neither check has ever failed because it was the wrong check.
Both have failed because nothing ran them: the structural regressions were verified by one-off scripts that were written and thrown away, and the cold read has always been a fresh agent someone remembered to dispatch.
That is one defect with one fix, so the trigger, the report, and the rule about what a red result costs are shared, and only the instruments differ.

### Why the structural fixture is the template and not a real board
A real board exercises whatever its authors happened to use, so a check that runs on one measures habits rather than grammar.
The template is fixed, small, and the only file whose job is to demonstrate everything, so an assertion that fails on it is always a defect in the template or the renderer and never a stylistic choice by an author.
It is also the cheapest possible fixture, because it is not a fixture at all: the file already exists and is already maintained.

### Two kinds of structural failure, reported differently
- The renderer drifted
  The template exercises the construct, the documentation names a class, and the page does not produce it.
  The fix belongs in `src/` or `assets/board.css`, and the report should name the construct in words rather than a selector, because the useful sentence is "the job line stopped rendering".
- The template has a hole
  The documentation names a construct that the template never demonstrates, so a new face inherits no example of it and the check has nothing to assert.
  The fix belongs in `ref/q-template.md`, and this half is the reason to run against the template at all, since a renderer-only test would pass while the hole stayed open.

### The zero-background reader, and why it cannot be simulated
The reviewer is a separately started agent that sees only the markdown files it is handed, not the conversation that produced them.
Its brief is fixed and narrow, and it is told not to praise or summarize: name the unreadable sentence and quote it, list the undefined word and say where it first appears, state the missing premise.
It grades each face clear, half, or unreadable, where half means the reader can restate what is asked but not why it matters or what counts as done.
The prompt and the rules it enforces live in `ref/writing-rules.md`, so the check and its standard are one document rather than a habit.

## Items to Finish
- [x] 📏 The rules for plain language are written down
      `ref/writing-rules.md` holds them, and `SKILL.md` excerpts the three deadliest with a pointer to the rest.
      No invented terms, stale sentences purged when the board changes, and a fresh-agent cold read after every revision.
      This was ticked on 260723 under QA5 and is inherited unchanged.
- [x] 📄 The cold read has a report format that produces usable findings
      It has run twice and both times returned findings that were acted on rather than argued with.
      The format is fixed: unreadable sentences quoted, undefined words listed with the file they first appear in, missing premises named, then a grade per face.
      The evidence that the format works is that its output changed the board: `## Topic` and `## Pipeline` exist because the first run said the files explain a recipe's format without ever saying what the dish is.
- [ ] 🧪 The template renders as both a Q face and an S face with no hand editing
      Copying `ref/q-template.md` twice and renaming the copies must be enough to produce one valid Q page and one valid S page.
      The two paths have broken independently, so checking one proves little about the other: Stage Contract exists only on S, Why this matters moves between Opening and Content depending on the kind, and the Content heading names the stage on S while counting subsections on Q.
      If the template cannot render as both without editing, that is itself a finding, because the documentation says one file serves both kinds.
- [ ] 📋 Every construct the documentation names is asserted with its class
      The list in the Diagram is the starting set, and it should be derived from `ref/board-form.md` rather than from the renderer, so a construct dropped from the code fails instead of quietly disappearing from both sides.
      The assertion should name the construct in words a reader recognizes, since the value of the check is that it says the job line stopped rendering, not that a selector count changed.
- [ ] 🕳 Gaps in the template are reported as gaps, not silently skipped
      When the documentation names a construct the template never demonstrates, the check reports a hole to fill rather than passing by default.
      This is the half that improves the template over time, and it is the half a renderer-only test would miss entirely.
- [ ] 🤖 A standing zero-background reviewer, not one summoned by hand
      Today the cold read is a fresh agent someone remembers to dispatch, with the prompt copied out of `ref/writing-rules.md` each time.
      The rules and the prompt are written down, but they are not packaged so that one command runs the review over a board and returns the report.
      Inherited open from QA5, where it has been the blocking item since 260723.
- [ ] 📐 The cold read's convergence criterion is quantified
      `ref/writing-rules.md` carries a first version, which is to run until no new unreadable findings appear, and that is a stopping rule rather than a standard.
      What is missing is what counts as passing when findings keep arriving but get smaller, since without it the review either never ends or ends whenever someone is tired of it.
      Inherited open from QA5.
- [ ] 🔁 One trigger runs both checks after a change, and the result is reported
      An edit to `src/`, to `assets/board.css`, or to any face's prose should be followed by the checks, with the result stated rather than assumed.
      This single item is why the two questions merged: it was open on both, worded almost identically, and it is the only reason either check keeps failing to happen.
      The structural half is fast enough to run on every renderer edit, and the prose half is slow enough that it should run per revision rather than per keystroke, so the trigger dispatches them at different rates from one place.
- [ ] 🧠 JL rules whether a red result blocks a change or only reports it
      A blocking gate is honest but stops work when the check itself is wrong, and a reporting gate is cheap but is only as good as whoever reads it.
      The two checks may deserve different answers, since a failed construct assertion is a fact and a cold-read grade is a judgment.
      This is a decision about how we work rather than about the code, so it is JL's, and until it is made both checks report.

## Where we are
Neither check runs by itself, and that has been the state since 260723.
The writing rules exist and the cold read has run twice by hand; the structural check has never been built, and today's verification was done with one-off scripts that were written, run once, and discarded.

- 260726 JL · 🔗 QA5 merged into this face
  CC argued for keeping them apart, because a boolean construct assertion and a graded cold read are different instruments with different fixtures and different runners.
  JL ruled to merge, and the merge is on the trigger: both faces were carrying the same unbuilt item about running automatically after a change, and splitting one mechanism across two faces is what left it unbuilt on both.
  The instruments stay distinct inside this face, and QA5's ticked history came with it rather than being restarted.

- 260726 JL · 🧭 Opened as a face rather than written as a script
  CC was about to write the structural checker directly, and JL stopped it: an unsettled ruling gets a face first, and the code follows the ruling instead of preceding it.
  Writing the script first would have produced a check whose acceptance nobody had agreed.

- 260723 CC · 📉 The second cold read graded this board honestly and it was not good
  Nine faces: two clear, six half-understood, one incomprehensible, and the incomprehensible one was QA4.
  Its three sharpest findings were that the word board is ambiguous in a self-referential context so the reader guesses throughout, that QA2's diagram said top and bottom while QA4's body said side by side about the same fact, and that `build.py`, skill, `/html-ppt`, and focus mode appear across five files and are defined nowhere.
  The two self-contradictions were fixed the same day; the undefined-terms finding is still open, which is why it is worth saying that a structural check would have passed all nine.

- 260722 CC · 📉 The first cold read, seven faces, and the line that still stings
  One clear, five vague, one incomprehensible, with roughly 35 terms used and never explained.
  The verdict was that the files explain the format of a recipe without ever saying what the dish is, and `## Topic` and `## Pipeline` exist because of it.

- 260723 CC · 🪤 The trap the writer falls into is inventing words
  A coined translation for battery, plus outward anchoring, act one, and three-set gate, none of which appear in any source document.
  These do the most damage of any writing fault, because the reader assumes they are jargon, goes looking for a definition, and finds nothing, so they lose confidence in the whole page rather than in one phrase.

## Files
- `ref/writing-rules.md`
  The prose check's deliverable and its standard: the hard writing rules, the zero-background review prompt, and the convergence criterion.
- `ref/q-template.md`
  The structural check's fixture and subject: the file copied for every new face, and the one whose promises the check verifies.
- `ref/board-form.md`
  The syntax table the structural assertions should be derived from, section 5 for the body grammar and section 4 for the section mapping.
- `src/page_question.py`
  The face renderer, which owns the Opening drawer, the Content subsections, and the Stage Contract.
- `src/body.py`
  The body grammar: paragraph headings, job lines, group titles, sentence apparatus, typed lanes, and code folds.
- `assets/board.css`
  Where a construct's meaning can change without any Python changing, which is how the drawer ended up in the metadata voice.
- `build.py`
  The generator, and the only check that runs today: it asserts the body survives with every script stripped.
- `SKILL.md`
  Its writing section excerpts the three deadliest rules and points at `ref/writing-rules.md`.

## Glossary
zero-background reader: someone who has never touched this project, played by a freshly started agent because it genuinely does not know, while the author knows too much unwritten context to test anything themselves.
subagent: a separately started Claude that sees only the files it is handed, not the conversation that produced them.
construct: one grammar element the documentation promises, such as a paragraph heading or a job line, together with the class it must render as.

## Discussion
> JL: I want a new Q about how to write a Q's body so people can actually understand it. We can have a subagent review every md so someone with limited knowledge can still follow.
> JL: QA5 Writing it so people understand this one can be absorbed into QA9 Checking the template against its own page, right?
>> CC0726: merged on JL's ruling. The two instruments stay distinct inside this face; what merged is the trigger, which was the item open on both.

## Log
260726 · QA5 merged in on JL's ruling: title widened from "Checking the template against its own page", the cold read and its two ticked items came across with their history, and the duplicated "runs automatically after a change" item became one. File renamed `QA9-rendercheck.md` to `QA9-acceptance.md`; the id is unchanged so `#QA9` still resolves
260726 · opened as QA9 after three construct-level regressions in two days (`####` rendering as a group title, the Opening fold moving onto the section name, the drawer's half-iconed headings), each caught by JL reading a page rather than by anything we run
260724 1242 · (from QA5) Translated to English (JL 260724: everything on the board in English)
260723 1710 · (from QA5) Ticked during the board-wide review: `ref/writing-rules.md` written and the cold read run twice, so state went 🟡; the automation half stayed open and is still open here
260723 0945 · (from QA5) Fixed the two self-contradictions the second cold read found: QA4's side-by-side against the actual stacked layout, and the three names one section was going by
260723 0925 · (from QA5) Second cold read, nine faces: two clear, six half, one incomprehensible
260723 0915 · (from QA5) JL: "if it is not easy to read, writing that much is rubbish", opened as a question
260722 1900 · (from QA5) Added `## Topic` and `## Pipeline` after the first cold read; terms moved into per-face `## Glossary`
260722 1830 · (from QA5) First cold read, seven faces: one clear, five vague, one incomprehensible, roughly 35 unexplained terms
