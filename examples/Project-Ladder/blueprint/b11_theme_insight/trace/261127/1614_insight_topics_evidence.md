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
T07  a Question Book in /hai-lab; host basics      fixed (host launch passed on)
T08  Executive questions on top of the map     fixed
T09  the Questions list: Executive first, closed  fixed
T10  no insight Block makes a data version     open
T11  a step's worker reads a config nothing exports   fixed
T12  a prep Run can overwrite a folder made before    open
T13  audit could not read a DataPrep Block       fixed
T14  the step review's agent could not write agreed   fixed
T15  a step reads more than its raw export      fixed
T16  a step writes outside a folder of its own   fixed
T17  no prep step checks the stated experiment   fixed
T18  a page could show a record value            fixed
T19  the Board's Data view shows records        fixed
T20  a new prep version cannot order its steps  fixed
T21  three linked views: Folder, Element, Session  open (map sent, no code yet)
T22  a new prep version copies the Runs' notebooks  fixed
T23  a description from another pull stops a dataset  fixed
T24  a later step does not wait for the card    fixed
T25  a signature does not freeze a called library  fixed
T26  DataPrep holds code; the Board runs it     fixed
T27  a step cannot read a per-Board setting     fixed
T28  a cut key nobody reads is ignored          fixed
T29  a step's Result has no light summary       fixed
T30  a Board Job pins three versions           fixed
T31  a Run holds numbers and no reading        fixed
T32  a Run report cannot cite a row count      fixed
T33  structure needs its own types and names   fixed
T34  shared Job UI loses Insight distinctions  open
T35  organization must branch as a mind map    fixed
T36  reuse the existing map inside its Block   open
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
- **Guard**: `hai-insight/tests/test_deliverables.py`; `hai-insight/ref/deliverables.py` (notes) and
  `ref/deliverables.md` (worked patterns); `hai-insight-evidence-plan` SKILL.md steps 6 and 7.

## T02 · Which check reads a ladder Board · fixed

- **From**: Report, Insight-QB-SMS, 261115: `check_block.py <Board>` printed "is not board-kind: task-block with
  workbench: insight" and "0 questions"; given a Job it raised FileNotFoundError.
- **Questions**: which script says a Run is stale on a Board of question-vN × data-vM Jobs? Why did the old one
  not say it was the wrong tool?
- **Answer**: `check_block.py` reads only the older Insight Block. It now says so and names the tools:
  `insight_ladder.py audit <Board>` (layout, hash, stale receipts) and `insight_ladder.py review <Board>`.
- **Case**: on the reported Board `audit` printed receipts 0 and hash 1, the true state after the edit.
- **Guard**: the rule at the top of `hai-insight-check` SKILL.md § Run it; the refusal text in
  `check_block.py` `run()`.

## T03 · Editing a version that is not signed, in place · fixed

- **From**: Report, Insight-QB-SMS, 261115: after editing question.md files the Board Job's hash is stale; "the
  order that worked: edit, update --apply, rerun the tickets, audit. That order is not written in one place."
- **Questions**: may an open version be edited in place? What goes stale, and in what order is it made current?
- **Answer**: yes while `signed: ''`. Order: edit, agree, re-pin, rerun, audit, review.
- **Guard**: `hai-insight/ref/deliverables.md` § Editing a version that is not signed yet, linked from
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
  (`hai-insight-question`), with no mechanical check.

## T07 · A Question Book in /hai-lab; host basics · fixed

- **From**: Report, Insight-QB-SMS, 261115: a `board-kind: prototype` Block had to be special-cased for `/hai-lab`;
  the host's launch line needs modules neither local Python has; a Tools change needs a host restart to show.
- **Answer**: `lab.py` `lab_theme()` opens a Question Book as an insight lab; the restart rule is written at the
  end of this skill's SKILL.md. The host launch line is the shared host's topic and was passed to its owner by
  the sender.
- **Guard**: `skills/1_base/workbench/hai-lab/tests/test_lab.py` `test_a_question_book_opens_as_an_insight_lab`.

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

## T10 · No insight Block makes a data version · open

- **From**: the user, 261116, beside a screenshot of `insight/` (Insight-SMSR2v1, InsightQuestionBook-SMSExperiment):
  "we have the InsightQuestion, Insight, how do you think we should have InsightDataPrep, which means how we will
  pepare the dataset in the good format, and ask the questions, and check the background etc. Do you think this is
  a good idea." Then Report, drfirst-space-b7 (SMSDesign insight), 261116, quoting JL: "I want to create the
  InsightDataPrep block, to develop the tools to deal with a set of data ... like InsightDataPrep-DrFirstExp".
- **What happened**: the ladder has two Blocks for two clocks (`hai-insight/ref/insight-ladder.md` § The two
  trees, "Two clocks"), but the data clock has no maker: rule 6 only has `run-add-version-data-vM` append a
  `folder:` built outside insight, and `scripts/insight_ladder.py` knows two face kinds (prototype, board). Today a
  work Block in another Project makes the data (`examples-2-analysis/Project-ExpAnalysis-SMSEngagement/work/
  b01_sms_cohort_foundation/j01_sms_cohort_preparation/t01_prepare_cohort_data`, nine Runs) into
  `_WorkSpace/7-AgentStore/A0-DIKW-Prepare/<DATE>_<COHORT>/`; a Board's version names that folder and no prep code,
  prep version or receipt. Row-level derivations sit in a question release's `src/`, so fixing one takes a new
  question version.
- **Questions**: what a DataPrep Block's Job, Task and Run are; how a Board's data version names the prep that made
  it; whether the worker in b01 is carried in or pointed at; where a Set that feeds several Projects lives; which
  derivations move from a release's `src/` to prep, and what becomes of the receipts that used them; where a prep
  check ends and a Data (D) question begins; where patient-level rows may sit.
- **Decided** (the user, 261116, each the recommended choice): drfirst-space-b7's shape, not a Job per data version:
  `insight/InsightDataPrep-<Set>/`, `board-kind: insight-dataprep`, `<Set>` a family of datasets; one Job per prep
  version `jNN_prep-vK_<slug>`, frozen once signed; a Task per step; a hard Run per dataset, whose output folder a
  Board adds as `data-vM` with `prep:`. The b01 worker is carried in as prep-v1 (`--from`), b01 left as it is. The
  DrFirstExp Block lives in SMSDesign and names the Boards of other Projects in `serves:` by their SPACE path. Only a
  row-level column that reads no outcome moves from a question version's `src/` to prep; a signed question version is
  never edited, so no receipt carries over. Patient-level rows stay in the store a Run writes to.
- **Answer**: the contract is `hai-insight/ref/dataprep.md` (linked from `ref/insight-ladder.md` and the SKILL.md
  route table). `insight_ladder.py` makes each level (`scripts/insight_ladder_prep.py`: `dataprep`, `dataset`, `prep`,
  `step`, `sign`, `run <step> dataset`), `data --prep` refuses an unsigned prep version, and `audit` has a `prep` row
  for a Board a DataPrep Block serves. A step's Run carries hai-task's own ticket, which now admits an
  `InsightDataPrep-*` Block in `insight/` and no other (`hai-task` 2.0.4). Six run cards at the Data Prep, Prep and
  Step levels; the Workbench Table regenerated.
- **Case**: on the example Board (`examples/Project-Ladder/insight/Insight-Example`), with a DataPrep Block serving
  it, `audit` printed `prep 2` (its two hand-made versions); a scratch step's ticket passed every shape check and
  stopped at its missing worker.
- **Guard**: `hai-insight/tests/test_dataprep.py` (six tests: names, versions and signature, `--prep` and the audit
  row, a Board no DataPrep serves, a Board in another Project, the ticket); `run_cards.py --check` (77 cards, 0 problems).
- **Still owed**: the workbench page. A DataPrep Block now opens on the base frame's fallback (MindMap, Plan +
  Results), whose header calls it "Insight Board · Dataset investigation". It needs its own page (Background ·
  Datasets · Versions · Steps, a step's checks per dataset, and a Board's data version linking to its prep) and a signed
  example in `examples/Project-Ladder/insight/`. `folder-kinds` has no DataPrep row.

## T11 · A step's worker reads a config nothing exports · fixed

- **From**: Report, drfirst-space-b7, 261116, topic A: "The ticket never exports a config's env:, so a carried worker
  builds the wrong cohort without saying so." `run <step> dataset` wrote `env: DATASET:`; the Task ticket exports only
  `HAIPIPE_CONFIG` and `RUN_CONFIG`; the carried `1_prep.py` reads `COHORT` from the environment and defaults to SMSR4.
- **Questions**: who exports a config's `env:`? What stops a worker from building a default dataset in silence?
- **Answer**: nobody does. The Task contract is that the worker reads `$HAIPIPE_CONFIG`; b01's tickets carried a
  hand-added export. The config stub now writes `dataset:` and `output:` and no `env:`, and says the worker reads the
  file and stops without a dataset. `ref/dataprep.md` rule 3 forbids a default dataset and lets a carried worker keep its
  maker's env export until the next prep version. The step review checks for both (run card, reviewer rule 5).
- **Case**: a new Run's config has no `env:` key and names its dataset; b7's nine carried tickets export b01's env.
- **Guard**: `test_dataprep.py` (the config stub); the review card and `hai-insight-reviewer-agent` rule 5.
- **Passed on**: whether the Task ticket should export a config's `env:` is hai-task's call; no session owns it
  now, so it went to the user. The carried `1_prep.py` default is prep-v1's to fix, and its review returns it.

## T12 · A prep Run can overwrite a folder made before · open

- **From**: Report, drfirst-space-b7, 261116, topic B: "Running or signing prep-v1 overwrites a frozen data version."
  The carried `r03_smsr2v1` config writes `A0-DIKW-Prepare/20250616_SMSR2v1`, which is Insight-SMSR2v1's data-v1.
- **Questions**: which folder may a Run write? What refuses the others, and when? How does a carried version sign
  without rerunning into the maker's folders?
- **Answer**: a Run writes only a new folder named for its version, `<name>@prep-vK` (rule 4). `audit <Block>` lists
  each config whose `output.prepare_dir` or `env.OUT_NAME` breaks that (`outputs`), `sign` refuses while one is left,
  the stub writes `@prep-vK`, and the next version re-aims copied configs. A carried version reruns into `@prep-v1`
  and compares with the folder it reproduces (§ Carrying an existing maker).
- **Case**: on b7's Block `audit` printed `outputs 11`, naming all nine t01 Runs, `r03_smsr2v1` among them.
- **Guard**: `test_dataprep.py` `test_a_run_never_writes_a_folder_made_before_and_audit_reads_the_block`.
- **Still owed**: nothing refuses at run time. A ticket run before `audit` writes whatever its config names. Closing
  it takes a hook in hai-task's ticket that runs before the worker (a no-op by default) and that a DataPrep ticket
  fills with this check: hai-task's call, put to the user.

## T13 · Audit could not read a DataPrep Block · fixed

- **From**: Report, drfirst-space-b7, 261116, topic C: `audit <InsightDataPrep-DrFirstExp>` printed only "board.md
  names no dataset: or prototype:".
- **Answer**: `audit` sends a DataPrep Block to its own checks (`insight_ladder_prep.audit`): serves, workers, configs,
  outputs, agreed, hash.
- **Case**: on b7's Block: serves 0 · workers 0 · configs 0 · outputs 11 · agreed 2 · hash 0.
- **Guard**: the same test (every row, and each one moving when its case is made).

## T14 · The step review's agent could not write agreed · fixed

- **From**: Report, drfirst-space-b7, 261116, topic D: the card gave run-review-steps to hai-task-reviewer-agent,
  whose tools are Read, Grep and Glob, and asked it to mark `agreed:`.
- **Answer**: the review is hai-insight-reviewer-agent's (it already writes `agreed:` on a plan it agrees): the
  scaffold's run type, the card, and the agent's run types and rule 5. Its one write is `agreed:` on a step it passes.
- **Guard**: `test_dataprep.py` (the review card's agent); `run_cards.py --check`.

## T15 · A step reads more than its raw export · fixed

- **From**: Report, drfirst-space-b7, 261116, topic E, quoting JL: "I want the raw input should just be the raw data
  from _WorkSpace/0-RawStore". The carried `1_prep.py` read a shared SourceStore cache, seven stage-1 configs set
  `use_cache: true`, two Runs skipped stage 1, and OptTimeR1's raw folder no longer exists. Then, 261118, from the
  prep-v1 review: haipipe's `source_pipeline.py:539-547` copies the raw export into the shared raw store whenever a
  config sets `raw_data_path`, so `use_cache` never applies and `save_cache` overwrites the shared source cache; a name
  that differs from the raw folder's makes a second full copy in the raw store.
- **Questions**: what may a step read? Where does an intermediate go? Is a shared source stage ever a way in? Are the
  external reference joins (area and prescriber tables) a dataset's input?
- **Answer**: a step reads only its dataset's `raw:` folder and earlier steps of its prep version, and loads the raw
  export itself; anything in between goes under its own `@prep-vK` place (`ref/dataprep.md` rule 3). `audit` names any
  config with `raw_data_path`, `source_config`, `save_cache` or `use_cache` (`inputs`) and a dataset whose `raw:`
  folder is gone (`raw`). The checks moved to `scripts/insight_ladder_prep_checks.py`.
- **Case**: b7 took stage 1 out of prep-v1, and on its Block `audit` reads `inputs 0`, `raw 2` (OptTimeR1 and its old
  cut, whose export is gone).
- **Guard**: `test_dataprep.py` `test_a_step_reads_only_its_raw_export_and_shows_no_record_value`; reviewer rule 5.
- **Passed on**: whether the reference joins are inputs is JL's call (asked by b7). An output root for haipipe's
  source stage is the haipipe code owner's; prep does not need it, since a step loads the raw export itself.

## T16 · A step writes outside a folder of its own · fixed

- **From**: Report, drfirst-space-b7, 261116, topic F: `summarize_cohorts.py` wrote `<store>/cohort_summary.*`
  whatever its config said and scanned every folder in the store.
- **Answer**: a Run config that names no output folder is refused like one that writes a folder made before
  (`outputs`, and `sign`); a compare step reads only its prep version's folders (rule 4). That a worker writes where
  its config says is the step review's check (reviewer rule 5).
- **Case**: t02's config now names `cohort-summary@prep-v1` and reads `*@prep-v1`, and its worker writes there; a
  config naming no folder is listed (the test).
- **Guard**: the same test; reviewer rule 5.

## T17 · No prep step checks the stated experiment · fixed

- **From**: Report, drfirst-space-b7, 261116, topic G, quoting JL: "I also want it to check what is the Experiment
  settings, time, etc information". Raw exports carry their own settings and timing documents; no step compares
  them with the rows.
- **Direction**: each prep version's first step reads only the `raw:` folder and writes an experiment card in its
  Result, aggregates only: settings (experiment ids, arms and their counts, batches, message content) and time (the
  invitation range in UTC and local time, active days, gaps, daily volume, send hours). Its checks compare stated with
  observed and block on a mismatch; a dataset with no documents gets a card from the rows marked "nothing stated",
  never a guess. Questions cite the card; D01 and D02 stay the reader's description.
- **Answer**: `ref/dataprep.md` rule 7, the step review (reviewer rule 5), and a gate: `sign` refuses a version whose
  first step has a Run without `result/experiment_card.json` and `.md`, or no Run; `audit` row `card`. A carried
  version owes none (§ Carrying).
- **Case**: the card worker (prep-v2 `t01_experiment`, built by Insight-Use-Case) passes every check on SMSR4,
  SMSR3Extended and OptTimeR1v3, says "nothing stated" on the four exports with no description, and "not checkable"
  for a blackout the rows carry no time zone for; on the DrFirstExp Block `audit` reads `card 1` until it runs.
- **Guard**: `test_dataprep.py` `test_a_new_version_signs_on_its_experiment_cards_and_leaves_notebooks_behind`.

## T18 · A page could show a record value · fixed

- **From**: Report, drfirst-space-b7, 261118, from the prep-v1 review: the Result's `data_dictionary.csv` carried a
  `sample_value` column (each column's first value) and the notebook showed a table's first three rows.
- **Questions**: which artifacts can a page show? Can a script name a line that takes a record's value without
  drowning the reader in aggregates?
- **Answer**: a Result, a notebook, and every dictionary, manifest or summary beside the rows (the Board's
  Description › Dataset shows them) carry shapes, counts and names, never a record value (`ref/dataprep.md` rule 4).
  `audit` names each worker line that takes rows by head, tail or sample (not an aggregate's: top-N counts are
  counts), each dictionary key `sample_value`, and each Result dictionary with a sample column (`records`).
- **Case**: on b7's Block the first pattern flagged ten lines, eight of them top-N counts and arithmetic; the
  narrowed one flags the two that are real (`1_prep.py:584,593` still write `sample_value` into the store's
  dictionary, which the Dataset view shows).
- **Guard**: the same test (an aggregate passes; a first value and a dictionary key are named); reviewer rule 5.

## T19 · The Board's Data view shows records · fixed

- **From**: Report, drfirst-space-b7, 261118: the frozen data-v1 folder's `data_dictionary.csv` (made by b01) has a
  `sample_value` column of first record values, as does every older store folder; "Board Description › Dataset shows
  it". b7 leaves the frozen folder alone and asks whether the view stops showing it or a data version is flagged.
- **What the code shows**: the Data view draws five random rows from a data version's file and hides only columns
  whose names look like identifiers (`insight_plan_c.py` `HIDDEN`, `insight_focus_board.py` `_version_panel`,
  `insight_view_board.py` `_version`); the dictionary's link opens the whole file, sample column included (its
  parsed table leaves that column out). Pages are also what a session reads when it checks one, so a row on a page
  is a row in a session's context.
- **Questions**: does a page show any row of a data version at all? How does a dictionary reach a page without its
  sample column? Is a data version whose files beside the rows hold record values flagged, given the folder is frozen?
- **Decided** (the user, 261118): shapes only.
- **Answer**: no row of a data version reaches a page. The row sampler is gone (`insight_plan_c.py`: no
  `sample_rows`, no `HIDDEN`), and the dictionary drops its sample columns as it is read (`SAMPLE_KEYS`). Both Data
  views (`insight_focus_board.py` `_version_panel`, `insight_view_board.py` `_version`) show the columns table
  (`columns_table`: name, type, null %, distinct, notes) and no link to the raw dictionary; an older board.md's
  `preview:` is not read. `insight_ladder.py audit <Board>` has a `records` row naming a data version whose
  dictionary holds a sample column: the frozen folder is named, never edited.
- **Case**: a data version whose dictionary carries a sample value renders on neither view, nor does its sample
  column or a link to the file; Insight-SMSR2v1's data-v1 is the version the `records` row names.
- **Guard**: `servers/workbench-insight/tests/test_data_view_shapes.py`; `hai-insight/tests/test_dataprep.py`
  `test_a_data_version_whose_dictionary_holds_record_values_is_named`.

## T20 · A new prep version cannot order its steps · fixed

- **From**: Report, Insight-Use-Case (drfirst-space-b7), 261119, topic I: opening prep-v2, `prep` copies prep-v1's
  steps as they are and `step` always takes the next number, so the experiment step would land third while rule 7
  puts it first, and the raw-only source step must come before prepare-cohort. Renaming step folders by hand would
  break their Runs and cards.
- **Questions**: where is a step's place set? What happens to a kept step's face, configs and Runs when it moves?
- **Answer**: `prep … --steps experiment,source,prepare-cohort,compare-cohorts` names the new version's steps in
  order: a kept step is copied to its new number (its face renamed with it), a new one is made empty, and one left out
  is not carried. A new version copies no Runs, so nothing that a Run names moves. A copied step keeps one config per
  dataset, the newest, and the first `run <step> dataset <name>` takes it under its new Run's name
  (`ref/dataprep.md` rule 2). `--before`, renumbering folders that hold Runs, was not built.
- **Case**: on the DrFirstExp Block, the dry run of that command lists t01_experiment, t02_source, t03_prepare-cohort,
  t04_compare-cohorts, and writes nothing.
- **Guard**: `test_dataprep.py` `test_a_new_prep_version_names_its_step_order`.

## T21 · Three linked views of the theme: Folder, Element, Session · open

- **From**: the user, relayed by the session tools-space-bc, 261117: "For the theme design, we should have three
  views. Folder Structure: how things are stored in the file system. Element Structure: how the UI presents the
  Folder Structure on the website. Session Structure: a view that records the important session history; the
  session keeps recording chat progress to the history, and shows how each session episode relates to each Folder
  and Element." The sender asked for this theme's map only, no code change, and no edit of the shared `frame_*`
  files.
- **Questions**: which folder kinds exist at each level? Which view and section shows each? Where does a session
  already leave a trace? Is "path relative to the Block" enough as the key that joins the three?
- **Answer so far** (the map sent to the sender, read from the example pair under `examples/Project-Ladder/insight/`
  and the `*_views` functions in `servers/workbench-insight/insight_focus_*.py`):
  - **Folder**: two Blocks. A Question Book (`board.md`, `proposals/`, `runs/`, a Job per question version with
    `release.yaml`, `partitions.md`, `thresholds.yaml`, `src/`, a Task per question holding `question.md` and
    `scripts/`). A Board (`board.md` naming its `prototype:`, `data/data-vN/`, `meta/`, `delivery/`, `runs/`,
    `sNN-<topic>/`, a Job per question version × data version, a Task per question, a Run per segment
    `runs/rNN_<segment>/` with `run.sh`, `run.yaml`, `result/`).
  - **Element**: Board views Findings, Questions, Data, Advice, Jobs; Job views Findings, Changes, Progress; Task
    views Answer, Changes, Method; Question Book views Questions, Ideas, Versions. Not one to one: a segment Run
    is drawn on the Task (By segment), the Job (Progress) and the Board (Findings).
  - **Session**: the `session:` line on a Board or Job face; a soft Run `runs/run-<verb>-<target>/` with `run.yaml`
    (`agent:`, `skill:`, `writes:`) and `passes/pNN-<MMDD>/pass.md` (Ask, Summary, Changed); a Task face's
    `results-read:` and `check:` lines; a Studio topic's own passes. A segment Run is a script and has no chat.
- **What does not fit the proposed shape**: one episode often writes both Blocks (a question edited in the Question
  Book, rerun on the Board), so the join key must be relative to the Project, not the Block; one episode is one
  pass of a soft Run and may start many segment Runs, so "one episode = one Run" holds only for soft Runs; the
  Element map is many to many; a transcript kept on a Board must obey the theme's law (counts and aggregates only,
  no row of the extract), so the digest is shown and a raw transcript is not; the map must be read from the focus
  views, since `Theme.spaces` here covers only the older layout's Spaces.
- **Still owed**: the theme's hook, once the shared Session view exists; a guard that every soft Run's `writes:`
  names real paths (the join depends on it).

- **Also from**: the user, 261121: "What I want to have is. File Systems for skill folder structure, and block folder
  structure, and chat folder structure? (I am not sure whether the chat should go to the block folder structure as
  well) and UI Systems how the file system is mapped to the UI system so we will have the things like the File System
  Structure." Then: "File System and UI System, we are just working on here."
- **Answer so far (261121)**: `PRINCIPLE.md` (pulled 2500309c7) settles the frame: a plugin is a Folder System and a
  UI System and the map between them; a Block holds `jNN` Jobs, `sNN` Studio topics and `cNN` Chats side by side. A
  kept chat is `cNN_<slug>/` at its Block, kept as QAs (hai-chat, `ref/chat-contract.md`); the transcript stays in
  `~/.claude/projects/<dir>/`; the Session view reads chats and passes alike (`servers/workbench/ref/three-views.md`). Since 261126 the cNN chat and hai-chat are retired: a Block's work is kept as traces in `trace/` (hai-trace).
  The map page, `examples/Project-Ladder/blueprint/b11_theme_insight/delivery/insight-board-site/` (a private
  Artifact), follows it: views Overview · Folder System · UI System · The Map, one page per part. My first answer (a
  digest only as a Run's `pass.md`) is replaced by the `cNN` contract. Found while mapping: no server code draws a
  DataPrep Block, a prep version or a step.
- **Still owed (261121)**, insight's part of three-views § 6 and § 8: the element map generated from
  `insight_focus_*_views`; a test that every insight folder kind has a page part; 🧵 beside insight content items; a
  check that every soft Run's `writes:` names real paths; pages for the DataPrep levels; the Board's Jobs view lists a
  Job of three versions (T30).

## T22 · A new prep version copies the Runs' notebooks · fixed

- **From**: Report, Insight-Use-Case, 261119, topic J: `prep --steps` made prep-v2 in the right order but copied
  prep-v1's generated notebooks (`_source.ipynb` and one per Run, a pruned Run's among them) into the kept steps, so
  prep-v2 showed a history it never had.
- **Answer**: a kept step copies its face, scripts and configs, never `runs/`, `results/` or `notebooks/`
  (`Plan.copy(also=...)`; `ref/dataprep.md` rule 2). `audit` row `notebooks` names a step notebook whose Run is not
  in that step.
- **Case**: on the DrFirstExp Block the prep-v2 opened before the fix reads `notebooks 9`; a version opened now
  carries none.
- **Guard**: the same test.

## T23 · A description from another pull stops a dataset · fixed

- **From**: Report, Insight-Use-Case, 261119, topic K: SMSR3Full's data description states an earlier pull's range
  and patients, so the experiment card fails four of five checks against a later export. JL chose (261119) to match
  by stamp.
- **Answer**: `ref/dataprep.md` rule 7: a document stamped with a pull's time is compared only with the export
  carrying the same stamp; one from another pull is listed on the card, its stated values shown and not checked;
  with no stamp on either file, they are compared. A setting the rows cannot test is "not checkable", never passed.
- **Case**: SMSR3Full builds, its card saying "nothing stated for this export (1 description from another pull)".
- **Guard**: the rule, read by the step review (reviewer rule 5); the card worker is prep-v2's.

## T24 · A later step does not wait for the experiment card · fixed

- **From**: Report, Insight-Use-Case, 261120, from the prep-v2 review (topic L): "nothing makes a later step wait for
  the experiment card. t02 builds even if t01 failed; only sign catches it."
- **Questions**: should a dataset's later steps refuse while its card has not passed? Where is "passed" read from?
- **Answer** (with T26): `ref/run_prep.py` refuses a step until the step before it is done, and fails a first step
  that wrote no experiment card; the chain stops at the first step that refuses or fails.
- **Guard**: `test_dataprep.py` `test_a_data_job_refuses_out_of_order_without_a_card_or_on_changed_code`.

## T25 · A signature does not freeze a library a step calls · fixed

- **From**: Report, Insight-Use-Case, 261120 (topic M): the prep hash covers `src/` and the step folders, not a
  library a step calls (`code/haifn/fn_source/<SourceFn>.py`); each receipt records its sha256, but a change after the
  signature goes unseen.
- **Questions**: how does a step name a library it depends on? What does `sign` pin, and what does `audit` compare?
- **Answer** (Insight-Use-Case's, 261120): a step that imports a library pins its sha256 in its own code and refuses
  when the library differs; the prep hash covers the step's code, so the signature freezes the pin. No face-level
  `libraries:` key. `ref/dataprep.md` rule 3 says so.
- **Case**: prep-v1's `source.py` carries `PINNED = {SourceFn: sha256}` and stops on a changed haifn file.
- **Guard**: the rule, read by the step review (reviewer rule 5 and the review card).

## T26 · DataPrep holds code; the Board runs it · fixed

- **From**: Report, Insight-Use-Case, 261120 (topic N), quoting JL: "the prep-v1 and just like the things we do in the
  questionbook-v1, they are code only … the real data processing and real question processing are in the insight
  block"; "what we want to deliver is like a script … input is the raw_folder, and output is
  ready_for_insight_folder"; "each tNN is a script, maybe we can follow them".
- **Questions**: what does a prep version hold, and what a step? Where does a prep version run, and how does its
  output become a data version? What becomes of the per-dataset Runs, configs and their checks?
- **Answer**: `ref/dataprep.md` rewritten. A prep version is code only: a step is `step.md` and a script exposing
  `run(ctx)`. A Board names its raw export and DataPrep Block (`datasource`) and opens a data Job (`datajob`), one Task
  per step and one hard Run each; `ref/run_prep.py` runs them in order with `ctx` (raw, out, prev, cut, refs, refuse),
  writes the card, the heavy middle and the ready folder, copies the scripts and their sha256 into each Run's
  provenance, and registers the ready folder as the Board's next data version (`prep`, `made-by`). Question Jobs and
  data Jobs share one count. The per-dataset Runs, `--again`, configs and their checks are gone.
- **Case**: on a placeholder SPACE a signed three-step version runs on a Board's raw export and becomes data-v1;
  out of order, without a card, on changed code, on a step's own refusal or with a sample column, it stops as the rule
  says.
- **Guard**: `test_dataprep.py` (nine tests); `run_cards.py --check`.
- **Still owed**: the workbench pages for a DataPrep Block and a Board data Job (the frame's fallback shows them);
  `hai-task`'s ticket still admits an `InsightDataPrep-*` Block, which no longer runs one.

## T27 · A step cannot read a per-Board setting · fixed

- **From**: Report, Insight-Use-Case, 261120 (topic O): the source step must pick the source function per Board (two
  exports with the same columns need different ones), and `ctx` carried only the cut.
- **Answer**: `datasource … --param key=value` writes the Board's `params:`; a data Job pins `cut:` and `params:` on its
  face when it opens, and `ref/run_prep.py` passes them as `ctx.cut` and `ctx.params` ({} when none) and records the
  params in each Run's receipt. A later edit to the Board does not change a Job already open.
- **Guard**: `test_dataprep.py` `test_a_board_runs_a_signed_prep_version_and_adds_its_data_version` (a param changed
  after the Job opened keeps its pinned value).

## T28 · A cut key nobody reads is ignored · fixed

- **From**: Report, Insight-Use-Case, 261120 (topic P): a reply from this session suggested `--cut end_date=…` while
  prep-v1's steps read `ctx.cut['start']` and `['end']`; the step would have seen no cut and made the whole export
  (751,110 rows, not data-v1's 444,691), and every gate would have passed.
- **Questions**: what ties a Board's cut and params keys to the keys a prep version's steps read? What does a step do
  with a key it does not know?
- **Answer**: a step declares the keys it reads, `step.md` `cut:` and `params:`; `datajob` refuses a Board key no step
  of the prep version declares, and `ref/run_prep.py` refuses it again for a Job opened before; a step refuses a key it
  does not know rather than ignore it (`ref/dataprep.md` rule 3; reviewer rule 5 and the review card).
  Read per dict (the step review's question, 261120): every step sees the whole ctx, so a step refuses an unknown key
  in a dict it reads (cut or params) and leaves a dict it does not read alone.
- **Case**: a Board with `cut: {end: …}` for a step that reads `end_date` is refused at `datajob`; a Job whose pinned
  params name a key no step reads is refused at its first step.
- **Guard**: `test_dataprep.py` `test_a_board_key_no_step_reads_is_refused`.

## T29 · A step's Result has no light summary · fixed

- **From**: Report, Insight-Use-Case, 261120, a question from the prep-v1 step review: may a middle or last step write a
  light `result/metrics.json`? prep-v1's t02 and t03 did, and were returned under the strict reading of rule 4.
- **Answer**: yes. Every step may write one light `ctx.result/metrics.json` (shapes, counts, check outcomes, under
  256 KB): what a reader opens first. A middle or last step writes nothing else into `result/`, which is the runner's;
  `ref/run_prep.py` fails a step that does, and a `metrics.json` over the size (rule 4; reviewer rule 5, the card).
- **Guard**: `test_dataprep.py` `test_a_step_adds_one_light_metrics_json_to_its_result_and_nothing_else`.

## T30 · A Board Job pins three versions · fixed

- **From**: Report, Insight-Use-Case, 261120 (topic Q), quoting JL on the data Job of T26: "Job here is a data prep
  version as a task, and then the question book as a task sequences. try to follow this." Then, exactly: "please
  recreate the j02 which has the data version and dataprep version and the question version. I think it should be
  three versions." And, comparing a DataPrep step with a question: no `runs/README.md`, no second face file.
- **Questions**: what is a data version once prep is code? Where does the prep version run, and what do the question
  Tasks read? How do one-clock Jobs work with three versions? What becomes of a Job of the withdrawn shape?
- **Answer**: a data version is the raw data, `versions: [{version, raw, cut, params}]` (`data … --raw`). A Job
  `jNN_data-vM_prep-vK_question-vN/` (`job --data --prep --release`) moves one version from the Job before; its
  `t01_prep-vK_<slug>/` runs the whole prep version in one Run (`ref/run_prep.py`) and writes the ready folder
  `<store>/<dataset>_data-vM@prep-vK/` and the Job's `ready:`; the question Tasks, one place after their release
  number, read it (`ref/run_job.py`) and are refused until it exists. A step is `step.md` and `scripts/`.
  `drop-datajob` undoes the withdrawn shape. `ref/dataprep.md` rewritten again.
- **Case**: on a placeholder SPACE, data-v1 × prep-v1 × question-v1 runs t01 (three steps, one Run), its question
  Task resolves its extract inside the ready folder, the next Job (question-v2) reuses the folder, and a Job moving data
  and question together is refused; the withdrawn j02 shape is dropped with its data version and folder.
- **Guard**: `test_dataprep.py` (ten tests); `run_cards.py --check`.
- **Still owed**: the workbench pages for a Job of three versions (the Board page reads question Jobs by name);
  `insight_plan_c.py` does not list these Jobs yet.


## T31 · A Run holds numbers and no reading of them · fixed

- **From**: Report, Insight-Use-Case, 261120 (topic R). JL opened `j02_…/t06_D05_levels-too-thin-to-read/runs/r0N_*/result/`
  and asked where the interpretation is: a Run holds csv, png, `metrics.json` and the generated `result/report.md` (the
  ask and the tables, no reading). JL: "after each task run, we can have the AI to summarize it a bit, to make it as a
  report". The only reading is the Task face (`answer:`, `how-sure:`, `takeaways:`), written once after every Run.
- **Questions**: where does a Run's reading live, so that rerunning the ticket (which owns `result/`) keeps it and marks
  it stale? Who writes it and who checks it, and how does a checker know each number is in the tables? What does the
  generated `result/report.md` become? How does the Task's answer use the readings? Can a Run whose tables match an
  earlier Job's carry its reading over? Does the prep Task's Run get one?
- **Answer**: each hard Run gets `runs/rNN_<segment>/report.md`, beside `result/` (the ticket clears only `result/`,
  so a rerun keeps it): a headline, a few sentences each citing the result file its numbers come from, a caveat. It
  pins `result-sha256`; a changed result makes it stale (❗ on the Run's page; the Task's page refuses to be written
  over it). `hai-insight/ref/run_report.py` (todo · write · check · carry): the maker writes a spec, the tool lays it
  out; `check` refuses the maker, a stale report, and a number not in the file its sentence cites unless the checker
  confirms it by hand (`--accept`); `--reject` returns it. A Run whose result equals an earlier Job's (same question,
  segment, hash) carries that checked report. The prep Task's Run gets one (the card and the steps' checks). The
  generated `result/report.md` is now `result/tables.md` (readers fall back). `write_answer_page.py` takes a missing
  takeaway from the Run's headline, so `takeaways:` are the reports' headlines; the workbench shows the headline until
  the page is written. Run types `report` and `check-report` (Job, Task, Prep Task), their cards and the gate
  "a Run reported"; `ref/run-report.md`.
- **Case**: `run_report.py todo` on the real j02 lists 163 Runs with no report (162 ok question Runs and t01's prep Run;
  the 19 failed ones are skipped). On a copy of `t06_D05…/runs/r01_full`, a four-sentence report was written, refused
  to its writer as checker, and passed by the reviewer with every number traced into `grouping_audit.csv`.
- **Guard**: `hai-insight/tests/test_run_report.py` (nine tests: kept by a rerun, stale on a changed result, the
  maker never checks, numbers traced, names not numbers, a refused Run's reason, carry, the prep Run, the Task page's
  takeaways, the workbench's hash equal to the runner's); `servers/workbench-insight/tests/test_run_report_page.py`;
  `run_cards.py --check`.
- **Still owed**: the Board page does not list a Job of three versions yet (T30), so j02's Runs and their reports open
  by link, not from the Board's Job list.


## T32 · A Run's report cannot cite a count of rows · fixed

- **From**: Report, Insight-Use-Case, 261120, the first real use of T31 (six D05 reports on Insight-SMSR2v1 j02):
  1. "Headline numbers are never traced: `untraced()` reads only `sentences`, yet the Task page quotes the headline."
  2. "Row counts cannot be cited: '17 of 29 groupings' is a count of rows of grouping_audit.csv, so every Data report
     needs `--accept` by hand, and some such counts pass only because the same number is a cell elsewhere." Asked: a
     sentence marks a number as derived, with its rule, so the checker verifies the rule.
  3. "Two files named report.md per Run: Runs made today still write `result/report.md`, not `tables.md`."
  4. "One file per sentence: a sentence cannot join the segment's rows (partition_power.csv) with the audit table, so
     no share can be stated. Allow `files: [a, b]`."
  5. For the Question Book (not the tool): D05's result gives counts per grouping, not the levels; filed by the sender.
- **Questions**: what may a headline say that its sentences do not? How does a derived number name its rule so a tool
  can compute it, and what happens to a rule it cannot compute? Which file does a rule read when a sentence cites two?
  What becomes of a Run's older `result/report.md` without rerunning 162 tickets?
- **Answer**: (1) a headline gives only numbers its sentences give; `check` names a headline number with no source.
  (2) a sentence names a number no cell holds under `derived: [{value, how}]`; the rule (`count rows [in <file>]
  [where <col> <op> <value> and …]`, `sum|min|max|mean <col>`, or arithmetic over the report's numbers) is computed by
  `hai-insight/ref/run_report_numbers.py` at `write` and at `check`: a wrong count stops the writer, and a derived
  number is never looked up, so one that a cell elsewhere holds no longer passes. A rule the tool cannot read stays
  for the checker (`--accept`, with the tool's reason). (3) not the generator: run_job.py writes `tables.md` since
  748db8958; j02's 181 Runs ran before it (12:48, the switch 13:30). `run_report.py tables <Job>` renames a generated
  `result/report.md` to `tables.md` without a rerun; the result's hash reads no `.md`, so no report goes stale.
  (4) `files: [a, b]`; a rule names its table with `in <file>` when there are two. (5) the sender's, for question-v2.
  A spec that is not YAML is refused with its reason, not a traceback. `ref/run-report.md`, the cards' prompts.
- **Case**: on the six real D05 reports (read only), the trace now names exactly the row counts the maker reported:
  29 in each, and 17, 16 or 14 where no cell holds them (r03 and r05's 17 had passed as a cell elsewhere). On a copy
  of r02 with its counts derived (17, 29, 12) and a share across two files (44.1% = 23535 / 53342), `check` passed with
  no `--accept`; written as 16, `write` refused: "`count rows where n_levels_suppressed > 0` gives 17".
- **Guard**: `test_run_report.py` `test_a_headline_gives_only_numbers_its_sentences_give`,
  `test_a_count_of_rows_is_derived_by_its_rule`, `test_a_sentence_may_join_two_files`,
  `test_an_older_runs_generated_report_becomes_tables`.

## T33 · Insight structure needs its own types and names · fixed

Date: 2026-11-27. User, verbatim:

> 这里的话你不应该再用 general name 了吧，因为你现在我们是 insight，是一个具体的 blog。那你这个 job topic 什么的，这名字应该都是要具体一些了吧，不能是 topic 1234。我之前那个是给 Walk 讲的，Walk 是 general 的嘛，Walk 那个 blog type 是 general structure。然后你这个是具体到一个 insight，那你这个 structure 应该是要具体一些，比如说 job group 什么名字呀，然后 path 什么名字啊，就是说应该是 propose 1234，propose 一下，你知道吗。

Follow-up from Work theme design: block skill (01a21d6c-cdee-7580-aeda-b1852ffb4a14),
verified against the user's message: explicitly show Job Type / Job Name / Task Type /
Task Name, update each theme's plan and execute. Full text is retained in
`examples/Project-Ladder/blueprint/b11_theme_insight/trace/261127/1057_insight_structure_types.md`.

Questions: Which responsibilities are types? Which are names or UI groups? How does the
Book include kept questions? Where do preparation steps execute? Which Studio topics are real?

Cause: a general Work placeholder tree was reused for specialized Blocks. The old type
inventory also described first/updated data versions as distinct analysis types, omitted
DataPrep, and represented neither Book question definitions nor its retained references.

Work: `ref/block-structure.md` defines the distinction. b11 s01/s02/s03 share real-folder
models between Structure and Draw, with source paths and explicit live-reader gaps.

Guard and acceptance: `delivery/structure/check_structure.py` checks actual Block kinds,
Board questions against their pinned releases, retained Book members, preparation ownership,
source paths, shared manifests and generated freshness. Fresh-context skill validation passed.
The actual b11 Studio showed all four fields, retained references, linked Draw, Skills and
the embedded DataPrep Block; 390 × 844 viewport inspection passed. Live-reader gaps are T34.

## T34 · The shared Job UI loses Insight Block distinctions · open

Date: 2026-11-27. Found while repeating T33's example through the actual shared page.

- **Questions**: how should the shared reader resolve retained Question Book members, show
  each Block's groups and identify the Block itself without creating a separate theme frame?
- **Case**: question-v2's Structure shows eight retained questions and K02. The shared Job
  reader enumerates only its one local Task. The DataPrep Examples iframe opens the correct
  Block, but its header says "Insight Board" and its use case "Dataset investigation".
- **Cause**: `servers/workbench/page/job_task_views/focus_jobs.py:78` groups on `release:` or
  a decade; `:135` enumerates local Task directories. `page/block_index_page/focus_identity.py:87`
  classifies every Insight Block as Insight Board, without reading the specialized Block kind.
- **Still owed**: coordinate a shared adapter for Book membership, Book/Prep groups and the
  Board's Preparation label; correct Block identity. Add source-contract regression checks
  and repeat the three live examples. No shared server was changed in T33's structure scope.

## T35 · Organization must branch as a mind map · fixed

The private drawing that initially passed this case is superseded by T36's shared renderer.

- **From**: user in Work theme design: block skill, 2026-11-27, verified message
  01a21dc6-b587-73e3-b35a-f84402b7989b: "不是，我意思是做一个mind map一样的炊，你懂吗。"
  Work relayed it to Insight. The preceding user message explicitly rejects a table and
  names the four columns Job Type, Job Name, Task Type, Task Name.
- **Questions**: how does a parent appear once while showing all its branches? Can the
  same map serve Structure and Draw and remain readable on a phone?
- **Cause**: `delivery/structure/build_structure.py` emitted repeated table rows while
  `structure.js` drew a vertical outline, so neither showed the requested horizontal map.
- **Work**: group the verified organization nodes by Job Type and lay out connected
  branches in four horizontal levels. A missing Task layer ends at the Job. Preserve source
  links and retained-question marks. Fit and actual-size controls follow Work's pattern.
- **Guard and acceptance**: `check_structure.py` checks unique parents, edges, no-Task
  branches and a shared map without table/select output. Fresh-context validation passed.
  Real browser inspection confirmed all three maps, no Board-node overlap, retained Book
  sources, and fit/actual-size switching with horizontal scrolling at 390 × 844.
  Live Job UI integration remains T34.

## T36 · Reuse the existing map inside its owning Block · open

- **From**: user, 2026-11-27, verbatim:
  "为什么不在 block里面打开？你每一次都要记住默认打开自己的对应的 work的这个 block。"
  "然后这个也睡得不好，你为啥不用我们现有的这个mind map跟 schedule来设计呢？你为什么要设计一个自己新的呢？我操。 记得我们是有 mind map skill的呀。"
- **Questions**: why was an internal HTML the entry? Why did the theme build another map
  layout despite the existing skill? How are readable folds and original sources preserved?
- **Cause**: the session delivered static preview URLs; `build_structure.py` laid out its
  own SVG nodes, with `structure.js` shrinking the map to width. Parent nodes left the
  initial viewport and labels became tiny. The old mindmap outline also put its tree after
  a second-level heading, so the canonical grammar treated it as notes rather than nodes.
- **Work**: `CONSTITUTION.md` A01/A02 fix the default Block entry and shared-renderer rule.
  The adapter now uses canonical grammar, `mmmap.draw`, default folds and shared refresh;
  private layout/zoom code is removed. Original outline text remains in the source history.
- **Guard and acceptance**: shared-renderer/source guard and fresh-context validation pass.
  The initial guard wrongly rejected authored branches; it now checks required identities
  and ownership while preserving authored words, notes and descendants. All three maps
  were opened inside b11; folds, Book retained-source details and DataPrep Draw passed.
  Labels use the shared 14px size without scaling. Desktop closed view fits its container.
- **Still owed**: at 390px the shared horizontal map needs panning even when closed; the
  root and first type do not fit together. Improve through the shared owner, not a theme
  renderer. Schedule's specific component remains unidentified; the user was asked for its
  existing name/entry. No schedule was invented, and this combined topic remains open.

