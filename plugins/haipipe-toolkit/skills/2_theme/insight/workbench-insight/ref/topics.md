# Insight topics

The Insight theme's topics, one section each (the repository's AGENTS.md § Report). A topic is the one thing
behind a message or a Report, not the case it showed up in. `fixed` means the case that raised it passes and
something keeps it passing (the guard); `open` names the work still owed.

```text
T01  what a question delivers                  fixed
T02  which check reads a ladder Board          fixed
T03  editing a version that is not signed      fixed
T04  an answer goes stale silently             open
T05  a refused Run looks like a missing Run    fixed
T06  Question Book gaps a check could catch    open
T07  a Question Book in /lab; host basics      fixed (host launch passed on)
T08  Executive questions on top of the map     fixed
T09  the Questions list: Executive first, closed  fixed
```

## T01 · What a question delivers, and how its output is reviewed · fixed

- **From**: the user, relayed by the session Insight-QB-SMS, 261115: "for each question here, besides the code, do
  we have the things / prompt about how to evalue the output? I mean for each task, what are the delivery to want
  to have for each task? report, figures, etc? like run the code, and the agent will review the results to give
  the report."
- **Questions**: does a question say what it delivers? Is there a test for the part an agent writes? Which figure
  answers the ask? When is "no figure" a decision and not an oversight?
- **Answer**: the question file already is the list: `output:` (tables), `figures:` (per table), `pass:` (the
  review test). No second block. Added: `pass:` on a judge need; `{table: <file>.csv, kind: none}` for one table
  (a `figures: []` drops every figure of the need); the check prompts ask for one verdict per need; the Task
  page's Needs section shows Need, Delivers, Counts when.
- **Case**: a 55-question version went from 24 judge needs with no test and 41 tables with no figure to 0 notes.
  Six first-draft judge `pass:` lines were returned as vague; the rule now says what checkable means.
- **Guard**: `haipipe-insight/tests/test_deliverables.py`; `haipipe-insight/ref/deliverables.py` (notes) and
  `ref/deliverables.md` (worked patterns); `haipipe-insight-evidence-plan` SKILL.md steps 6 and 7.

## T02 · Which check reads a ladder Board · fixed

- **From**: Report, Insight-QB-SMS, 261115: `check_block.py <Board>` printed "is not board-kind: task-block with
  workbench: insight" and "0 questions"; given a Job it raised FileNotFoundError.
- **Questions**: which script says a Run is stale on a Board of question-vN × data-vM Jobs? Why did the old one
  not say it was the wrong tool?
- **Answer**: `check_block.py` reads only the older Insight Block. It now says so and names the tools:
  `insight_ladder.py audit <Board>` (layout, hash, stale receipts) and `insight_ladder.py review <Board>`.
- **Case**: on the reported Board `audit` printed receipts 0 and hash 1, the true state after the edit.
- **Guard**: the rule at the top of `haipipe-insight-check` SKILL.md § Run it; the refusal text in
  `check_block.py` `run()`.

## T03 · Editing a version that is not signed, in place · fixed

- **From**: Report, Insight-QB-SMS, 261115: after editing question.md files the Board Job's hash is stale; "the
  order that worked: edit, update --apply, rerun the tickets, audit. That order is not written in one place."
- **Questions**: may an open version be edited in place? What goes stale, and in what order is it made current?
- **Answer**: yes while `signed: ''`. Order: edit, agree, re-pin, rerun, audit, review.
- **Guard**: `haipipe-insight/ref/deliverables.md` § Editing a version that is not signed yet, linked from
  `ref/release.md` § Signing.

## T04 · An answer goes stale silently · open

- **From**: Report, Insight-QB-SMS, 261115: written Task faces predate new figures and pass lines and nothing
  marks them; `check:` is empty on every face; a full check is one agent per Task.
- **Questions**: what tells a reader an answer is older than its results? How is a whole Job's check started?
- **Answer so far**: `insight_ladder.py review <Board>` (read-only) lists each answer that owes a reread (no
  `results-read:`, or one before a Run's `content_since`) and each with no ✅ check. A whole-Job check is many
  agents, so it starts only when the person asks (`ref/deliverables.md` § Reviewing every answer of a Job).
- **Guard**: `test_deliverables.py` (the three `review` tests).
- **Still owed**: the Task and Job pages do not mark an answer that owes a reread (the list is only in the
  command); a face written by hand has no `results-read:` line, so it always counts as owing one; a check made
  before a question's `pass:` lines changed is not told apart from a current one.

## T05 · A refused Run looks like a missing Run · fixed

- **From**: Report, Insight-QB-SMS, 261115: two segments of one Knowledge question refuse as thin; "the Task page
  should show refused: thin rather than look like a missing Run."
- **Questions**: where is the reason kept? Does the page show it?
- **Answer**: the reason was only in the receipt, so the page fell back to a stock sentence. `run_job.py` now
  writes `reason:` on the Run card, and the page reads the receipt for a card written before that.
- **Case**: the reported Task page shows each refusal's own reason.
- **Guard**: `servers/workbench-insight/tests/test_insight_plan_c.py` `RefusedRunTest`.

## T06 · Question Book gaps a check could catch · open

- **From**: Report, Insight-QB-SMS, 261115: every segment's `why` is empty; a Knowledge question has no links in
  the map though a lower question's text says it is read; some files carry an extra `signed: ''` key; one cite
  borrows points where the reader wants rates.
- **Questions**: which of these can a script name without judging?
- **Answer so far**: `insight_ladder.py review` notes a segment with no `why`, and a Knowledge or Wisdom question
  that cites no need below it (a suspect, since a script may read the level below through `ctx.result`).
- **Guard**: `test_deliverables.py` `test_review_reads_the_question_book_a_board_pins`.
- **Still owed**: a link a script makes through `ctx.result` is not read, so the links note over-reports; unknown
  front-matter keys are not listed; a cite whose unit does not fit its reader is a question-review judgment
  (`haipipe-insight-question`), with no mechanical check.

## T07 · A Question Book in /lab; host basics · fixed

- **From**: Report, Insight-QB-SMS, 261115: a `board-kind: prototype` Block had to be special-cased for `/lab`;
  the host's launch line needs modules neither local Python has; a Tools change needs a host restart to show.
- **Answer**: `lab.py` `lab_theme()` opens a Question Book as an insight lab; the restart rule is written at the
  end of this skill's SKILL.md. The host launch line is the shared host's topic and was passed to its owner by
  the sender.
- **Guard**: `skills/1_base/workbench/lab/tests/test_lab.py` `test_a_question_book_opens_as_an_insight_lab`.

## T08 · The Executive questions sit on top of the question map · fixed

- **From**: the user, relayed by the session Insight-QB-SMS with a screenshot of the map's right edge, 261115:
  "for the dot, how do you think you can make the X in the top? what is your thoughts?" Then, on the design
  Insight-QB-SMS proposed (a top row in number order, each a card with its title, the four levels as columns
  under it, an Executive question's lines only on hover or pin): "plsae go ahead and do it".
- **Questions**: which style drew Executive last? Does the layout assume one column a level everywhere? Does a top
  row fit six questions, and ten? What happens to the lines, since an Executive question cites every level? Does
  the phone need a change?
- **Answer**: only the Dots style (`question_canvas.py` `drawNet`) drew Executive as a fifth column, in an order
  chosen to cross fewer lines. Cards already had the Executive row on top and the phone leads with its Executive
  tab. Dots now draws Executive as a row of titled cards across the top in number order (it wraps and centres a
  short last row when the canvas has no room for all: six fit from about 780 px, ten wrap to two rows there), the
  four evidence levels as columns of dots under it, and no line to or from an Executive question until that
  question, or one in its chain, is hovered or pinned. The phone list is untouched. The segment picker, hover card and pinned
  panel read a card's own position, so nothing else assumed a column.
- **Case**: on the reported Question Book at 828 px the six Executive cards sit in one row, X01 to X06 left to
  right, with none of their 34 lines showing; hovering X03 draws its chain in green.
- **Guard**: `servers/workbench-insight/tests/test_insight_focus.py`
  `test_the_dots_map_keeps_executive_on_top`; the rule in this skill's SKILL.md (the question map).

## T09 · The Questions list leads with Executive and starts closed · fixed

- **From**: the user, relayed by the session Insight-QB-SMS with a screenshot of the Question Book page's section
  "1 · Questions" (groups headed Data, Information, …), 261115: "for things here, could we make the X to be the
  top and each group to be collapsed? do you understand what I mean?"
- **Questions**: is the level order one constant shared with the map and the phone tabs? Does a link that jumps
  to a question open the closed group it lands in? Does the same list render on a Board Job's page? What does a
  closed group's bar say?
- **Answer**: the list read `ORDER = "DIKWX"`, the order the work is done in, which the Work views still need.
  Reading lists now use `READ_ORDER = "XDIKW"` (`insight_prototype_facts.py`), the order the map and the phone
  tabs already show. On the Question Book's page each level is a closed fold (`insight_prototype_parts.py`
  `_by_level(fold=True)`); a link to `#<question id>` opens the fold and the page section it lands in. A version's
  own page keeps its level tabs, now Executive first too. A Board Job's page draws its own list (level tabs or
  folds from `insight_view_parts.py`), already Executive first and closed.
- **A bar's words**: the level's name, and ✓ once every question in it is agreed and scripted. No count and no
  tally ("Executive · 6 · 6 script written" was the sender's suggestion): the repository's AGENTS.md § Page words
  keeps counts and progress tallies off a label; each question shows its own state in its row.
- **Case**: on the reported Question Book the folds read Executive, Data, Information, Knowledge, Wisdom, all
  closed; opening the page at `#K05` opens Knowledge and the Questions section and scrolls K05 into view.
- **Guard**: `servers/workbench-insight/tests/test_insight_focus.py`
  `test_the_questions_list_leads_with_executive_and_starts_closed`; the rule at the end of this skill's SKILL.md.
