# Page and group proposals
state: 🔴 OPEN
owner: JL
method: derive a proposal procedure from real boards, then test whether a fresh agent produces clear pages and coherent groups

## Question
How should Board `open` and `add` turn a topic into a reviewable proposal of page questions, page titles, and page groups?

`open` creates a board; `add` extends an existing board with a page or group. The current rules define the file grammar, short-title form, numbering, slug, group storage, and index display, but they never explain how to discover the right pages or decide why several pages belong together. Without that method, an agent can produce overlapping questions, vague names, and arbitrary groups that render correctly but do not help anyone steer the work. This question owns the proposal the user reviews before those actions write files.

## Boundary
- ✅ Covered here
  The procedure for proposing page scope, page names, group membership, group names, and the evidence used to judge that proposal.
- ↪ Covered elsewhere
  File membership and numbering are `QA1`; the Q/S source shape is `QAa0` (the template moved there when QA2 merged, 260729); index rendering and structure controls are `QA10`; prose inside an accepted page is checked by `QA9`.

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

The settled procedure will be recorded as `ref/proposal-rules.md` and invoked by the `open` and `add` sections of `SKILL.md`. This QC4 page records the design discussion and evidence until those rules are settled.

### 3 · What exists today
The `open` action asks for a list of pages and requires user approval, but it gives the agent no method for producing that list. `q-template.md` says a page title is a short phrase and its lead is an actual question. `writing-rules.md` requires a self-contained question and a short heading. `board-form.md` defines ids, slugs, and the `## Pages` grammar. `QA10` defines how accepted groups and rows appear on the index. `serve.py` can add a group or question from a title, but it does not judge the title or group.

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

## Items to Finish
- [ ] 🧭 Settle how candidate pages are derived
      Define how the approved requirements inventory becomes candidate decision pages or ordered lifecycle-stage pages.
- [ ] ✂️ Settle the page-scope test
      Make the scope, coverage, and separation tests operational enough that two reviewers reach the same result.
- [ ] 🏷️ Settle the page-name test
      Define measurable title checks for length, concreteness, uniqueness, and stability as the work evolves.
- [ ] 🗂️ Settle the group proposal test
      Define when a new group is earned, whether a one-page group is ever valid, how its title and responsibility sentence are written, and which weak groupings are rejected.
- [ ] 📋 Settle the proposal shown for approval
      Decide whether the table above is sufficient for both `open` and `add`, then place the final format in the Board reference file.
- [ ] 🧪 Test the method on real boards
      Freeze two fixture packets and answer keys: one decision board with independent questions and one lifecycle board with ordered stages and outputs. A fresh agent receives only `ref/proposal-rules.md` plus each packet and produces a proposal table. An independent reviewer scores both tables on the acceptance dimensions. After an accepted table is materialized, a second cold reader sees only `board.md` and must match the answer key for every page title's ownership and every group's reason without opening page bodies. Finish conditions are judged from the proposal table, not inferred from `board.md`.

## Where we are
Only fragments exist: titles must be short phrases, questions must be self-contained, ids and slugs have a grammar, and groups have an index representation. No rule currently tells an agent how to propose the pages or groups themselves.

- 260726 JL · 🧩 The missing design layer was named
  JL observed that current question names, page names, and especially proposed page groups are not consistently good, and asked for a dedicated place to design a better proposal method.
- 260726 Cold read · 🧱 Inputs and acceptance tests were missing
  A fresh reader rated the first draft half-clear because its action names, board types, page types, inputs, deliverable, and pass criteria were undefined. This revision defines those premises without deciding the still-open proposal algorithm.
- 260726 Cold read 2 · 🧪 The design brief is clear; the test needed separation
  A second fresh reader rated QC4 clear as an open design brief. It found that generation and index-reading tests were conflated and that `board.md` could not expose finish conditions. The tests now have separate agents, artifacts, answer keys, and judging sources.

## Files
- `../../board/haipipe-board/SKILL.md`
  The `open` action requires page-list approval but does not explain how the list is proposed.
- `../../board/haipipe-board/ref/q-template.md`
  Defines the title as a short phrase and the lead as the full question.
- `../../board/haipipe-board/ref/writing-rules.md`
  Requires short headings and self-contained questions, but has no naming or decomposition test.
- `../../board/haipipe-board/ref/board-form.md`
  Defines ids, slugs, groups, and `## Pages` after the proposal has already been accepted.
- `QC2-indexdesign.md`
  Owns how groups and page rows render and how they are edited, not how they are conceived.
- `../../board/haipipe-board/serve.py`
  `_slugify`, `Q_STUB`, and `structure_op` materialize a supplied title without judging it.
- `../../board/haipipe-board/check.py`
  A future structural check could detect duplicate or weak page and group proposals after the human rule is settled.

## Discussion
> JL: The current question names, page names, and especially proposed page groups are not consistently good. We need a dedicated question for how the Board should propose reasonable pages and groups.

## Log
260726 · Opened from JL's request to design a better question, page-name, and page-group proposal method
260726 · Revised after cold read to define inputs, terms, deliverable, fallback, fixtures, and acceptance tests
260726 · Revised after second cold read to clarify `add`, group fallback, and two-stage validation
