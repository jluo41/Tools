# Page and group proposals
state: 🔴 OPEN
owner: JL
method: derive a proposal procedure from real boards, then test whether a fresh agent produces clear pages and coherent groups

## Opening
How should Board `open` and `add` turn a topic into a clear set of pages and groups before writing any files?

This page defines the proposal a user reviews for page scope, names, finish conditions, and group ownership.
The file grammar says how to store an accepted page, but it cannot decide which decisions or stages deserve pages of their own.
Without a decomposition test, an agent can create overlap, vague titles, and arbitrary groups that render cleanly but cannot steer the work.
The proposal succeeds when the user can see complete, non-overlapping ownership before approving any new file.

**Covered elsewhere**: File membership and numbering are `QB1`; the Q/S source shape is `QB4` (the template moved there when QA2 merged, 260729); Board-Webpage-Index rendering and structure controls are `QB2`; prose inside an accepted page is checked by `QF1`.


## Diagram

```
topic + files + throughline + finish condition
                     |
                     v
           candidate decisions or stages
                     |
                     v
         remove overlap and expose gaps
                     |
                     v
       cluster by one enduring responsibility
                     |
                     v
       name page questions, titles, and groups
                     |
                     v
            user reviews one proposal table
                     |
                     v
              write ## Pages and page files
```

## Content
### 1 · Terms and inputs
A **throughline** is one sentence stating what all pages collectively advance. A **finish condition** is the evidence that the board's topic is resolved. A **Q page** owns one answerable decision; an **S page** owns one ordered lifecycle stage and the outputs needed to finish that stage. A **group** contains pages that share one enduring responsibility, not merely similar words.

**Files in scope** are existing source or evidence files that constrain the topic, not the page files that the action may create. **Known constraints** are requirements and exclusions stated by the user or the project. From these inputs, the agent writes a requirements inventory: the decisions or stage outputs that the proposed pages must cover.

For `open`, the procedure receives the topic, files in scope, throughline, finish condition, and known constraints. For `add`, it also receives the existing board index and the new concern to place. A short assumptions block and the requirements inventory appear before the proposal table. Missing inputs are drafted there for review instead of being silently invented.

### 2 · Deliverable
Before writing files, the action shows one proposal table with these columns:

| Field | What the user must be able to judge |
|---|---|
| Page type | Q decision or S lifecycle stage |
| Proposed title | Short, concrete label unique on this board |
| Actual question or stage | The self-contained lead the page will own |
| Boundary | What belongs here and what belongs elsewhere |
| Finish condition | What permits this page to close |
| Proposed group | The index section that will contain the page |
| Group reason | One sentence true of every page in that group |

An `open` proposal shows the whole candidate board. An `add` proposal shows the requested change plus every existing page or group needed to judge overlap and placement. For a group-only addition, the table lists every proposed member.

The settled procedure will be recorded as `ref/proposal-rules.md` and invoked by the `open` and `add` sections of `SKILL.md`, and by the `propose` verb of `haipipe-board-routing`, which absorbed board-structure proposals on 260802; those two descriptions are corrected together. This QA2 page records the design discussion and evidence until those rules are settled.

### 3 · What exists today
The `open` action asks for a list of pages and requires user approval, but it gives the agent no method for producing that list. Since 260802, `haipipe-board-routing`'s board altitude owns `propose` and `materialize` for an agent: it shows a six-line structure proposal (spine, close, groups, pages, connections, skills) and stops for approval, but it too has no test for judging the decomposition. `page-template.md` says a page title is a short phrase and its lead is an actual question. `writing-rules.md` requires a self-contained question and a short heading. `board-form.md` defines ids, slugs, and the `## Pages` grammar. `QB2` defines how accepted groups and rows appear on the Board-Webpage-Index. `serve.py` can add a group or question from a title (through `live/structure.py` since the 260731 live split), but it does not judge the title or group.

### 4 · What is missing
A page proposal needs a test for whether each page owns one independently closable decision or stage, whether two pages overlap, whether an item in the requirements inventory has no page, and whether the title distinguishes the page without repeating the full question. A group proposal needs an enduring responsibility: a shared function, output, stakeholder, or lifecycle segment that applies to every member and distinguishes those pages from pages outside the group. It must not merely cluster similar words.

If page scope, coverage, or separation fails, revise the decomposition. If the pages pass those tests but share no coherent responsibility, leave them ungrouped. Do not invent a miscellaneous group to make the index look complete.

### 5 · Acceptance dimensions to operationalize
- **Scope:** every page owns one decision or stage and one observable finish condition.
- **Coverage:** every item in the approved requirements inventory appears on one page.
- **Separation:** no two pages claim the same decision, output, or finish condition.
- **Name:** the title distinguishes the page in the index without restating its full lead.
- **Group:** one responsibility sentence applies to every member and distinguishes them from pages outside the group.
- **Fallback:** pages with no coherent shared responsibility remain ungrouped.
- **Review:** no files are created until the user accepts or revises the proposal table.

## Aims
### The proposal method's tests
- [ ] 🧭 Settle how candidate pages are derived
      Define how the approved requirements inventory becomes candidate decision pages or ordered lifecycle-stage pages.
- [ ] ✂️ Settle the page-scope test
      Make the scope, coverage, and separation tests operational enough that two reviewers reach the same result.
- [ ] 🏷️ Settle the page-name test
      Define measurable title checks for length, concreteness, uniqueness, and stability as the work evolves.
- [ ] 🗂️ Settle the group proposal test
      Define when a new group is earned, whether a one-page group is ever valid, how its title and responsibility sentence are written, and which weak groupings are rejected.

### The deliverable and its trial
- [ ] 📋 Settle the proposal shown for approval
      Decide whether the table above is sufficient for both `open` and `add`, then place the final format in the Board reference file.
- [ ] 🧪 Test the method on real boards
      Freeze two fixture packets and answer keys: one decision board with independent questions and one lifecycle board with ordered stages and outputs. A fresh agent receives only `ref/proposal-rules.md` plus each packet and produces a proposal table. An independent reviewer scores both tables on the acceptance dimensions. After an accepted table is materialized, a second cold reader sees only `board.md` and must match the answer key for every page title's ownership and every group's reason without opening page bodies. Finish conditions are judged from the proposal table, not inferred from `board.md`.

## States
Only fragments exist: titles must be short phrases, questions must be self-contained, ids and slugs have a grammar, and groups have an index representation. No rule currently tells an agent how to propose the pages or groups themselves.

- 260731 JL · 🗂 The groups settled at six
  The QD split and flatten produced `QD` Working · `QE` Sharing · `QF` Execute behind the unchanged three-layer core, so this board now demonstrates the full shape twice over.
  Any proposal method this page designs should treat Working · Sharing · Execute as the standing tail groups of a Skill-Board.
- 260730 JL · 🧭 This board's own groups were restructured to the three-layer model
  Seven groups became five: QA Design (what the system is) → QB Delivery (Board → Group → Page → Section → Sentence) → QC Engine (how it is made and shipped), QE Execute (what actually ran: QA9's checker, QF2's fresh-agent run), QD Working and sharing (the live layer, absorbing the former QE Sharing).
  The same Delivery → Engine → Execute split had just been field-tested on the paper family's Skill-Board.
  Every page kept its id, because a page's letter is the group it was OPENED under, and the lane cells travelled with their pages (`lanes.py collect_kept`).
  Any future proposal method this page designs should propose groups in these three layers.
- 260726 JL · 🧩 The missing design layer was named
  JL observed that current question names, page names, and especially proposed page groups are not consistently good, and asked for a dedicated place to design a better proposal method.
- 260726 Cold read · 🧱 Inputs and acceptance tests were missing
  A fresh reader rated the first draft half-clear because its action names, board types, page types, inputs, deliverable, and pass criteria were undefined. This revision defines those premises without deciding the still-open proposal algorithm.
- 260726 Cold read 2 · 🧪 The design brief is clear; the test needed separation
  A second fresh reader rated QA2 clear as an open design brief. It found that generation and index-reading tests were conflated and that `board.md` could not expose finish conditions. The tests now have separate agents, artifacts, answer keys, and judging sources.

### Decision Now
These are the calls only JL can make; CC ticks nothing here.

- [ ] 📋 Approve the proposal table in Content §2 as the deliverable
      Both `open` and `add` would show this seven-column table before writing any file.
      → CC's proposal: yes as drawn; its columns already carry every acceptance dimension listed in §5.
- [ ] 🗂 Ratify the three-layer group default for a Skill-Board
      Design → Delivery → Engine as the core, with Working · Sharing · Execute as the standing tail.
      → CC's proposal: yes; it has now been field-tested twice, on the paper family's Skill-Board and on this board itself.
- [ ] ✍️ Decide when `ref/proposal-rules.md` gets drafted
      A · draft it now from §4 and §5, which gives a fresh agent something to be handed and exposes what §4 still leaves undefined.
      B · keep designing on this page until the tests in Items are settled, which delays the fixture test that needs the file.
      → CC's proposal: A; the fixture test in Items needs a rules file a fresh agent can be handed, and drafting it will expose exactly what §4 still leaves undefined.
- [ ] 🧱 Approve or reject the two remaining proposed pages on the live read/write architecture
      JL 260731 asked what the best method is for interacting with markdown as the backend, and which Q pages should exist for it; three decisions were homeless.
      Overtaken by absorption, noted at the 260806 sweep: neither proposed page still needs a ruling, and every id below is retired in `board.md`'s Links table.
      The approved write-path question lives on after the 260801 renumbering as `QC-engine/QC4-roundtrip.md`, with the write path itself split out to `QC4a-writepath.md`.
      `QC9`, the unit of change, was absorbed by `QC4-roundtrip.md`, whose method rules the unit of change; the 1.6MB refetch was measured and closed on `QD-working/QD7-pagecost.md`.
      `QD9`, what the page shows before the server answers, was absorbed by `QE-sharing/QE3-whereitruns.md`, now settled; poll against SSE is `QC4-roundtrip.md`'s own remaining open item; concurrent writers stay with `QE4`.
      → CC's proposal: strike this row; nothing here is left for JL to approve.

## Files
### Engines
- `../../board/haipipe-board/SKILL.md`
  The `open` action requires page-list approval but does not explain how the list is proposed.
- `../../board/haipipe-board/live/structure.py`
  `_slugify`, `Q_STUB`, and `structure_op` materialize a supplied title without judging it; they moved here in the 260731 live split, and `cli/serve.py` imports them.
- `../../board/haipipe-board/cli/check.py`
  A future structural check could detect duplicate or weak page and group proposals after the human rule is settled.

### Input files
- `../../board/haipipe-board/ref/page-template.md`
  Defines the title as a short phrase and the lead as the full question.
- `../../board/haipipe-board/ref/writing-rules.md`
  Requires short headings and self-contained questions, but has no naming or decomposition test.
- `../../board/haipipe-board/ref/board-form.md`
  Defines ids, slugs, groups, and `## Pages` after the proposal has already been accepted.
- `QB-delivery/QB2-board-webpage-design.md`
  Owns how groups and page rows render and how they are edited, not how they are conceived.

## Discussion
> JL: The current question names, page names, and especially proposed page groups are not consistently good. We need a dedicated question for how the Board should propose reasonable pages and groups.

## Log
- 260806 2124 · [REVISE-CC] swept to the 260806 architecture; the 🧱 Decision Now row's QC9/QD9 asks marked overtaken (both ids retired into QC4-roundtrip and QE3-whereitruns via the Links table), QA2b corrected to QB2, structure_op repointed to live/structure.py, routing's 260802 propose verb added to the inventory
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260731 · The unit-of-change proposal renumbered QC8 to QC9 after a concurrent session opened QC8 for the live-layer split: a live id beats a proposed one
260731 · QC7 approved by JL and opened the same round; QC8 and QD9 still awaiting a ruling
260731 · Three pages proposed on the live read/write architecture (QC7 write path, QC8 unit of change, QD9 optimistic echo), awaiting JL; the stack half was already settled on QE3
260731 · Groups settled at six after the QD split (QD Working · QE Sharing · QF Execute); stale pointers moved to live ids
260730 · The board's seven groups were restructured into the Design → Delivery → Engine three-layer model with Execute and Working; every page kept its id
260726 · Opened from JL's request to design a better question, page-name, and page-group proposal method
260726 · Revised after cold read to define inputs, terms, deliverable, fallback, fixtures, and acceptance tests
260726 · Revised after second cold read to clarify `add`, group fallback, and two-stage validation
