# Checking the page after every change
state: 🟡 PARTIAL
owner: CC
method: two instruments cover four failure classes on one planned trigger: a mechanical checker tests structure and detectable interaction/status contradictions; a zero-background reviewer tests readability and visible staleness

## Question
How should every board change trigger the checks that catch broken structure, unreadable prose, and stale or contradictory claims before the round closes?

Authors miss these failures because they carry the intended result and missing context in their heads.
A mechanical checker and a fresh reader see different evidence, so neither can replace the other.
The hard part is making both run at the right scope and deciding what a red result stops.
This page succeeds when every change produces a clear, repeatable review instead of waiting for a reader to notice the damage.


## Boundary
- ✅ Covered here: the mechanical checker, the fresh reviewer, their four failure classes, their shared trigger, and the report produced when either instrument is red.
- ↪ Covered elsewhere: `QB4` owns the page template and one Content division per section; `QF2` owns the separate fresh-agent usability acceptance for a revised skill; `QF3` owns browser behavior.

## Diagram

```
  a change lands
       │   src/ · assets/board.css · any page's prose
       ▼
  ┌────────────────────────────────────────────────────────┐
  │  ONE TRIGGER, TWO INSTRUMENTS                           │
  └───────────┬──────────────────────────┬──────────────────┘
              │                          │
      MECHANICAL                    FRESH REVIEWER
      fixed test input: template    input: changed pages in board context
      plus the live board           as their authors actually wrote them
        ├─ a Q page                 run by a fresh-context agent that
        └─ an S page                has never seen the project
              │                          │
        build.py + check.py         answers exactly three things
              │                      ① which sentence is unreadable
        read the html                ② which word is never defined
              │                      ③ what premise is missing
        assert structure and              │
        detectable contradictions        │
              │                          │
        fact per row                readability + visible staleness
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
  division               ### heading           details.csec
  paragraph heading      #### heading          div.ph, and never 🔹
  job line               (…) under a ####      div.pj
  group title            **a whole line**      div.gt > span.gi, keeps 🔹
  sentence apparatus     sentence then > lines details.sent
  sentence badge         attached-lane count   span.sbadge
  typed lane             > Citation: …         div.lane with its icon
  item with detail       - ICON head + indent  details.it.row
  finish count           - [ ] / - [x]         n/m in the section heading
  dated item             260723 CC · head      span.stmp
  code block             a fenced block        details.codef
  excalidraw canvas      /_excalidraw/...      div.xcal

  ✗ the author re-reading their own page in the same conversation
    catches none of the four classes: too much unwritten context is already loaded
```

/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/board.excalidraw&frame=QA9

## Content
### The two instruments answer different questions
The structural check asks a question with a fact for an answer, and the prose check asks one that requires judgment.
Whether `####` produced `div.ph` is decidable by a regex in milliseconds and is either true or false.
Whether a sentence packs three things into one is decidable only by a reader who does not already know which three, which is why it needs a fresh context and cannot be a pattern match.
Their inputs differ for the same reason: the structural check uses `ref/page-template.md` as a fixed test input and also checks the live Board, while the prose check reads the actual changed pages, because prose is only unreadable or stale in the specific words someone wrote.
Merging them into one instrument would lose the more valuable one, since a structural pass is compatible with a page nobody can read, and that combination is exactly what the second cold read found.

### Why they share a trigger anyway
Neither check has ever failed because it was the wrong check.
Both have failed because nothing ran them: the structural regressions were verified by one-off scripts that were written and thrown away, and the cold read has always been a fresh agent someone remembered to dispatch.
That is one defect with one fix, so the trigger, the report, and the rule about what a red result costs are shared, and only the instruments differ.

### Why the structural fixed test input is the template
A real Board exercises whatever its authors happened to use, so it cannot by itself prove that the complete grammar still renders.
The template is fixed, small, and the only file whose job is to demonstrate everything, so an assertion that fails on it is always a defect in the template or the renderer and never a stylistic choice by an author.
It is also the cheapest possible fixed test input because the file already exists and is already maintained.

### Two kinds of structural failure, reported differently
- The renderer drifted
  The template exercises the construct, the documentation names a class, and the page does not produce it.
  The fix belongs in `src/` or `assets/board.css`, and the report should name the construct in words rather than a selector, because the useful sentence is "the job line stopped rendering".
- The template has a hole
  The documentation names a construct that the template never demonstrates, so a new page inherits no example of it and the check has nothing to assert.
  The fix belongs in `ref/page-template.md`, and this half is the reason to run against the template at all, since a renderer-only test would pass while the hole stayed open.

### "After every change" is scoped to the SPACE, not to the board you edited
The live layer runs one server per repo root and serves every board beneath it, which `QA0` argues in full.
That makes the blast radius of a change asymmetric, and this face is where the asymmetry has to be paid.
A change to one board's `.md` touches one board, so checking that board is enough.
A change to anything shared, meaning the inlined `assets/`, the `src/` renderer, or the engine's scripts, silently changes every board under the root, so checking only the board in front of you proves nothing about the other five.

260731 is the worked example.
An assets stamp was added to `page_board.py` for one board's problem, and it altered the `<head>` of every board the family renders, so all five sibling design boards plus the paper's `0-lifecycle` had to be rebuilt and re-checked before the change could be called done.
The same day, a restructure of this board broke three of the paper board's cross-board `## Links`, which no check of this board could ever have caught.

The rule that follows is short: a shared change is checked across the root, and a board-local change is checked on its board.
A checker that only ever runs where the edit happened will keep reporting green while boards it never opened go red.

### The zero-background reader, and why it cannot be simulated
The reviewer is a separately started agent that sees only the markdown files it is handed, not the conversation that produced them.
Its brief is fixed and narrow, and it is told not to praise or summarize: name the unreadable sentence and quote it, list the undefined word and say where it first appears, state the missing premise.
It grades each page clear, half, or unreadable, where half means the reader can restate what is asked but not why it matters or what counts as done.
The prompt and the rules it enforces live in `ref/writing-rules.md`, so the check and its standard are one document rather than a habit.

## Items to Finish
### The template fixture
- [x] 🧪 The shared template exercises both Q and S renderer modes
      Copying `ref/page-template.md` twice and renaming the copies must be enough to exercise one Q render path and one S render path before the author replaces the guide prose.
      The two paths have broken independently, so checking one proves little about the other: Stage Contract exists only on S, Why this matters moves between Opening and Content depending on the kind, and the Content heading names the stage on S while counting subsections on Q.
      This fixture checks renderer placement, not whether an author finished the source or generated a synchronized S contract.
      Ticked 260726: `check.py` copies the template into a temp board twice, once as `QT1-template.md` and once as `S-Main-1-template.md`, and builds both without hand editing.
      It separately asserts Q rationale placement and counted Content, plus S rationale placement, Stage Contract placement, and the stage-named Content heading.
- [x] 📋 Every construct in this page's structural table is checked
      The 15-row Diagram table is a manually maintained acceptance set in `CONSTRUCTS`, with broader syntax families still owned by `ref/board-form.md`.
      The assertion should name the construct in words a reader recognizes, since the value of the check is that it says the job line stopped rendering, not that a selector count changed.
      Ticked 260726: the 15 constructs from this page's own Diagram are the table in `check.py`, each reported by name and by class, so a failure reads `job line · div.pj` rather than a count.
- [x] 🕳 Gaps in the template are reported as gaps, not silently skipped
      When the documentation names a construct the template never demonstrates, the check reports a hole to fill rather than passing by default.
      This is the half that improves the template over time, and it is the half a renderer-only test would miss entirely.
      Ticked 260726, and it earned itself on the first run by making template holes measurable instead of assumed complete.
      The source-aware check now reports renderer drift as ERROR only when the source exercises a construct, and reports a missing source example as GAP.
- [ ] 🧰 The template demonstrates every structural-table construct
      The source-aware check currently reports two explicit fixture gaps: a group title and an Excalidraw canvas.
      These remain open rather than being hidden by an output-only regex; the Excalidraw example needs a portable placeholder that cannot point a copied page at the wrong Board.

### The mechanical checker
- [ ] 🔎 `check.py` verifies a 🧩 Skills landed row
      A row claiming `ref/board-form.md §1 · landed` is checkable by grep, so rot becomes a warning instead of a silent lie; the current Files/action-map convention is owned by `QB4` §6.
- [x] 🥀 A page that stopped describing its own work is reported
      An additional failure turned up on 260726: a page can render perfectly and read well while saying something that is no longer true.
      `QA4a` carried `state: 🔴 OPEN` and "nothing is built and nothing is decided" on the day its whole route was built, wired into 28 pages, and running, because the session did the work from chat and never went back to the page that owned it.
      `check.py` now reports `open-with-done-items` and `partial-with-nothing-open` on Q pages, which is the cheapest signal that exists: a ruling state and its own boxes disagreeing.
      It never applies that heuristic to an S page, whose state is a human lifecycle gate independent of follow-up checklist work.
      On Q pages it sees `state:` and the checkboxes and nothing else, so it catches the shape and never the content; the rule it backs up is `SKILL.md`'s `sync`, which now says the trigger is substantive work in the session rather than opening a page.
- [x] 🖱 A construct that RENDERS but cannot be USED is reported
      An additional failure appeared on 260726. A broad CSS selector, `.fig{}`, matched both images and hidden chip panels. Its `display:block` rule forced five invisible panels to cover the page and swallow mouse clicks, even though the page rendered and read correctly.
      `check.py` now has `check_css`, which fails on any bare class selector colliding with a panel class token. Verified both ways: reintroducing `.fig` makes it fire, scoping it to `img.fig` makes it silent.
      The first diagnosis was wrong because the synthetic `element.click()` method bypasses the browser's check for what lies under the pointer. Checking the element at each control's centre found 11 of 11 unreachable and named the covering panel.
- [ ] 🎯 An interaction check that a static reader cannot fake
      `check_css` catches this one collision class. It does not catch an element covered by anything else, an off-screen panel, or a control whose click does nothing. The missing instrument is a headless browser that checks which element lies at each control's centre and then confirms that the opened panel stays inside the viewport. An ad hoc standard-library-only driver using Chrome DevTools Protocol (CDP) found the 260726 bug, but it was not kept.
      Whether that belongs in `check.py` at all is the open question: it needs a browser, so it breaks this page's "standard library, runs anywhere" property. A separate opt-in script is the likelier answer.
- [ ] 🏷 A retired id can be told apart from a live one
      Every `unresolved-id` warning on the first run was a deliberate historical mention: `QCb1`-`QCb4` in QA8 recording what the ids used to be, and the former QF group's QF2 in QB3 naming a retired ruling.
      A live reference and a historical one are typographically identical today, so no check can separate them and neither can a reader.
      This closes when the convention exists, whichever way it goes: a retired id written without backticks, or marked, or listed once on the board.
- [ ] 🧩 A board can declare which rules it opts out of
      `settled-with-open-items` is a Q-only rule and never applies to lifecycle S pages.
      This Board uses it, while the paper family's design Board opts its Q pages out because their `state:` is about the decision and implementation lives in the item list.
      `check.py` currently detects that Q-board variant by pattern-matching the sentence the design Board happens to use to say so, which works and is fragile.
      This closes when a board can state its own variant in `board.md` rather than having it guessed from prose.
- [ ] 🔎 A 🧩 Skills row that claims "landed" is verifiable by the checker
      `QB4` §6 carries the current convention: a page's Files action map may name the skill file or section it governs, each with a landed / NOT landed verdict when verification matters.
      A landed claim is greppable, so `check.py` can warn when the named section no longer exists or the claim rots; until it does, the convention has no mechanical half.

### The fresh reviewer and the cold read
- [x] 📏 The rules for plain language are written down
      `ref/writing-rules.md` holds them, and `SKILL.md` excerpts the three deadliest with a pointer to the rest.
      No invented terms, stale sentences purged when the board changes, and a fresh-agent cold read after every revision.
      This was ticked on 260723 under QA5 and is inherited unchanged.
- [x] 📄 The cold read has a report format that produces usable findings
      It has run twice and both times returned findings that were acted on rather than argued with.
      The format is fixed: unreadable sentences quoted, undefined words listed with the file they first appear in, missing premises named, then a grade per page.
      The evidence that the format works is that its output changed the board: `## Topic` and `## Pipeline` exist because the first run said the files explain a recipe's format without ever saying what the dish is.
- [x] 🥀 Staleness is caught in the PROSE, not only in the state line
      The mechanical check would have missed `QA4a` entirely if the state had been flipped and the paragraph left alone, which is the more likely half of this failure.
      `haipipe-board-reviewer-agent` now compares each scoped page's state, finish list, current-status prose, links, and directly cited artifacts; it reports stale or contradictory claims and says `not verifiable` when evidence is unavailable.
      Ticked 260726 with the standing reviewer implementation; the mechanical state-line checks remain a cheaper backstop.
- [x] 🤖 A registered standing reviewer, no longer an ad hoc prompt
      `haipipe-board-reviewer-agent` now packages the read-only review: it reads the Board rules, runs `check.py --strict`, cold-reads the changed pages using `ref/writing-rules.md`, checks visible state/status contradictions, and returns `pass | revise | blocked`.
      It has no write or edit tools. The original session remains the writer and must repair every finding, preserving builder ≠ judge.
      Ticked 260726 after JL promoted Board to a first-class family and explicitly approved the reviewer role. Dispatch is still manual until the trigger item below is closed.
- [ ] 📐 The cold read's convergence criterion is quantified
      `ref/writing-rules.md` defines the current pass condition: no page is unreadable, and every reason for a `half` grade is either fixed or recorded as a known gap.
      What remains unquantified is when a growing set of known gaps is acceptable, and which count or severity should block the revision.
      Inherited open from QA5.

### The shared trigger and the red-result ruling
- [ ] 🔁 One trigger runs both checks after a change, and the result is reported
      An edit to `src/`, to `assets/board.css`, or to any page's prose should be followed by the checks, with the result stated rather than assumed.
      This single item is why the two questions merged: it was open on both, worded almost identically, and it is the only reason either check keeps failing to happen.
      The structural half is fast enough to run on every renderer edit, and the prose half is slow enough that it should run per revision rather than per keystroke, so the trigger dispatches them at different rates from one place.
- [ ] 🧠 JL rules whether a red result blocks a change or only reports it
      A blocking gate is honest but stops work when the check itself is wrong, and a reporting gate is cheap but is only as good as whoever reads it.
      The two checks may deserve different answers, since a failed construct assertion is a fact and a cold-read grade is a judgment.
      This is a decision about how we work rather than about the code, so it is JL's, and until it is made both checks report.

## Where we are

- 260801 JL · 🔬 A THIRD instrument exists, and this face's two were green through every failure it catches
  `QF3` opened on 260801 after a browser run passed 36 of 36 assertions.
  What it changes here is the claim this face makes: the two instruments named above are a mechanical checker and a zero-background reader, and BOTH of them read text.
  Six failures shipped on 260731 with this face's checker green and a reader who would have found nothing: the index rendering as inline links because invented class names matched no CSS, the left rail missing from a template, six ASCII figures never emitted, every write from a tree page failing silently, a CSS fix that never reached the page for want of cache-busting, and a stray triangle that survived two fixes on a specificity tie.
  Every one lived in what the BROWSER did with text that was itself correct, which is the boundary between this face and `QF3`.
  The shared trigger argument in §"Why they share a trigger anyway" now covers three instruments rather than two.

## Where we are
Both instruments now exist and have a registered runner.
`check.py` is the mechanical instrument; `haipipe-board-reviewer-agent` is the read-only fresh-context runner that combines its report with the prose and staleness review.
The checker now reads the same state contract as the renderer: the first emoji is the four-value machine status, optional text is human detail, and live `/_board/` plus `/_excalidraw` routes are not mistaken for missing files.
Seven decisions or implementations remain open: the two template examples, a full browser interaction check, a retired-id convention, Board-level rule opt-outs, a quantified policy for known cold-read gaps, automatic dispatch after changes, and whether a red result blocks the revision.

- 260731 JL · 🌐 The trigger's scope is the SPACE, because the server's is
  JL settled that the live layer is SPACE-level: one server per repo root serving every board under it, with `--root` as the served tree, `.haipipe-board/` at the root, and terminal keys hashed from the absolute page path so two boards' `QD3` cannot collide.
  The consequence lands here rather than on `QA0`, which owns the scope itself: a change to anything shared changes every board at once, so "after every change" means across the root for a shared change and on one board for a local one.
  Two failures the same day are the evidence, a `<head>` change that touched six boards and a restructure that broke three cross-board Links on a board nobody had opened.

- 260726 CC · 🔩 The checker follows the live renderer contract
  Real paper pages use state detail such as `✅ PINNED · MISQ 2026`, and generated Excalidraw links are server routes rather than disk files.
  `check.py` now validates the normalized first emoji and ignores only the two declared live-route families, while continuing to fail on an invalid state token or a genuinely missing local file.

- 260726 JL · 🤖 Board gained its first family-level agent
  JL promoted Board beside paper, probe, and task and approved a dedicated reviewer.
  The registered agent is deliberately read-only and lives at `skills/board/agents/`; session attachment, synchronization, repair, and rebuilding remain with the main Board skill and the current writer.

- 260726 JL · 🔗 QA5 merged into this page
  CC argued for keeping them apart, because a boolean construct assertion and a graded cold read are different instruments with different fixed inputs and different runners.
  JL ruled to merge, and the merge is on the trigger: both pages were carrying the same unbuilt item about running automatically after a change, and splitting one mechanism across two pages is what left it unbuilt on both.
  The instruments stay distinct inside this page, and QA5's ticked history came with it rather than being restarted.

- 260726 JL · 🧭 Opened as a page rather than written as a script
  CC was about to write the structural checker directly, and JL stopped it: an unsettled ruling gets a page first, and the code follows the ruling instead of preceding it.
  Writing the script first would have produced a check whose acceptance nobody had agreed.

- 260723 CC · 📉 The second cold read graded this board honestly and it was not good
  Nine pages: two clear, six half-understood, one incomprehensible, and the incomprehensible one was QA4.
  Its three sharpest findings were that the word board is ambiguous in a self-referential context so the reader guesses throughout, that QA2's diagram said top and bottom while QA4's body said side by side about the same fact, and that `build.py`, skill, `/html-ppt`, and focus mode appear across five files and are defined nowhere.
  The two self-contradictions were fixed the same day; the undefined-terms finding is still open, which is why it is worth saying that a structural check would have passed all nine.

- 260722 CC · 📉 The first cold read, seven pages, and the line that still stings
  One clear, five vague, one incomprehensible, with roughly 35 terms used and never explained.
  The verdict was that the files explain the format of a recipe without ever saying what the dish is, and `## Topic` and `## Pipeline` exist because of it.

- 260723 CC · 🪤 The trap the writer falls into is inventing words
  A coined translation for battery, plus outward anchoring, act one, and three-set gate, none of which appear in any source document.
  These do the most damage of any writing fault, because the reader assumes they are jargon, goes looking for a definition, and finds nothing, so they lose confidence in the whole page rather than in one phrase.

- 260726 CC · 🧰 The structural half exists and runs
  `check.py <board-dir>` covers four families: required Board structure against disk, required Q/S source structure plus state and references, the built page's links and tag balance and id uniqueness, and the shared template rendered through both modes with the 15-row acceptance set checked.
  It shares `ALIAS`, `STN`, and `page_files` with the renderer through `src/common.py`, while keeping independent structural assertions that compare the documented contract with what the renderer accepts.
  Default mode reports and exits 0; `--strict` exits 1 when ERROR findings exist, while the broader workflow decision about whether that red result blocks a revision remains open.
  The first run found 0 error, 31 warn, and 3 gap on this Board, plus 3 error and 8 warn on the paper Board.
  It found two things on its first outing that a person had missed for a day, and two of its own rules were wrong in ways only a real run exposes: it counted `<details>` inside CSS comments, and it applied this Board's settled-items rule to a Board that had ruled otherwise.
  Both are fixed, and both are the argument for running the checker rather than describing it.

### Decision Now
These are the calls only JL can make; CC ticks nothing here.

- [ ] 🧠 Rule whether a red result blocks a change or only reports it
      The page already states the fork: a blocking gate is honest but stops work when the check itself is wrong, and a reporting gate is cheap but is only as good as whoever reads it.
      The two checks may deserve different answers, since a failed construct assertion is a fact and a cold-read grade is a judgment.
      A tick here also closes the same row in Items to Finish.

## Files
### The two instruments
- `check.py`
  The mechanical half. Four families, the 15-construct table, and the gap report. Read-only.
- `haipipe-board-reviewer-agent.md`
  The standing zero-background runner for the mechanical, prose, and visible-staleness review. It returns findings and never edits.

### The standards and fixed inputs they read
- `ref/writing-rules.md`
  The prose check's deliverable and its standard: the hard writing rules, the zero-background review prompt, and the convergence criterion.
- `ref/page-template.md`
  The structural check's fixed test input and subject: the file copied for every new page, and the one whose promises the check verifies.
- `ref/board-form.md`
  The syntax table the structural assertions should be derived from, section 5 for the body grammar and section 4 for the section mapping.
- `SKILL.md`
  Its writing section excerpts the three deadliest rules and points at `ref/writing-rules.md`.

### The renderer under test
- `src/page_question.py`
  The page renderer, which owns the Opening drawer, the Content subsections, and the Stage Contract.
- `src/body.py`
  The body grammar: paragraph headings, job lines, group titles, sentence apparatus, typed lanes, and code folds.
- `assets/board.css`
  Where a construct's meaning can change without any Python changing, which is how ordinary drawer prose ended up styled like small metadata labels.
- `build.py`
  The generator. Its built-in assertion checks that the body survives with every script stripped; `check.py` and the fresh reviewer are separate checks.

## Glossary
zero-background reader: someone who has never touched this project, played by a freshly started agent because it genuinely does not know, while the author knows too much unwritten context to test anything themselves.
subagent: a separately started Claude that sees only the files it is handed, not the conversation that produced them.
construct: one grammar element the documentation promises, such as a paragraph heading or a job line, together with the class it must render as.
fixed test input: a small, maintained file whose expected output is known in advance; here it is `ref/page-template.md`.
Opening: the always-visible opening section that states a page's question and scope before any collapsible detail.

## Discussion
> JL: I want a new Q about how to write a Q's body so people can actually understand it. We can have a subagent review every md so someone with limited knowledge can still follow.
> JL: QA5 Writing it so people understand this one can be absorbed into QA9 Checking the template against its own page, right?
>> CC0726: merged on JL's ruling. The two instruments stay distinct inside this page; what merged is the trigger, which was the item open on both.
> JL: Board should be a first-class family, and it should have a reviewer agent.

## Log
260801 · QF3 opened as the third instrument: a browser run, because this face's two instruments both read text and six 260731 failures lived in what the browser did with it
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260731 · The trigger's scope written down: a shared change is checked across the root, a board-local change on its board, because one server serves every board under the SPACE (QA0)
260726 · fixed a Q/S boundary exposed by the real Paper lifecycle Board: checkbox/state staleness is now tested only on Q rulings; an S page's emoji is an independent human gate, so a gated stage may retain follow-up boxes without a false Q warning
260726 · aligned the checker claim with its real boundary: canonical required Board/Q/S structure is now enforced, the shared-template item names renderer-mode coverage rather than completed-source validity, and the 15-row table is explicitly manual
260726 · strengthened the template fixture after a fresh reviewer found output-only claims: source-vs-render drift is now distinguished, Q/S-specific placements are asserted, the Diagram matches the 15 checks, and two actual template gaps remain explicit
260726 · aligned `check.py` with the renderer's state token and allowlisted the Board's two live route families, removing false failures on real paper and Excalidraw pages without weakening local-file checks
260726 · added `skills/board/agents/haipipe-board-reviewer-agent.md`; standing-reviewer item ticked, while automatic dispatch and the red-result policy remain open
260726 · an additional failure named and half instrumented (JL: "during the session when we use /haipipe-board, you should think about how to update the related Q along the session"): a page can render and read while no longer being true, `check.py` now reports the state-against-its-own-boxes shape, and the prose half is open as a cold-read finding class
260726 · `check.py` written and run (JL: "do you think you need to write a python script to check the basic webpage and Q-md structure"): 🧪 📋 🕳 ticked, two new items opened by what the first run exposed (retired-id convention, board-local rules); the cold-read half and the shared trigger stay open
260726 · QA5 merged in on JL's ruling: title widened from "Checking the template against its own page", the cold read and its two ticked items came across with their history, and the duplicated "runs automatically after a change" item became one. File renamed `QA9-rendercheck.md` to `QA9-acceptance.md`; the id is unchanged so `#QA9` still resolves
260726 · opened as QA9 after three construct-level regressions in two days (`####` rendering as a group title, the Opening fold moving onto the section name, the drawer's half-iconed headings), each caught by JL reading a page rather than by anything we run
260724 1242 · (from QA5) Translated to English (JL 260724: everything on the board in English)
260723 1710 · (from QA5) Ticked during the board-wide review: `ref/writing-rules.md` written and the cold read run twice, so state went 🟡; the automation half stayed open and is still open here
260723 0945 · (from QA5) Fixed the two self-contradictions the second cold read found: QA4's side-by-side against the actual stacked layout, and the three names one section was going by
260723 0925 · (from QA5) Second cold read, nine pages: two clear, six half, one incomprehensible
260723 0915 · (from QA5) JL: "if it is not easy to read, writing that much is rubbish", opened as a question
260722 1900 · (from QA5) Added `## Topic` and `## Pipeline` after the first cold read; terms moved into per-page `## Glossary`
260722 1830 · (from QA5) First cold read, seven pages: one clear, five vague, one incomprehensible, roughly 35 unexplained terms
