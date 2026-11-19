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

## T10 · No insight Block makes a data version · open

- **From**: the user, 261116, beside a screenshot of `insight/` (Insight-SMSR2v1, InsightQuestionBook-SMSExperiment):
  "we have the InsightQuestion, Insight, how do you think we should have InsightDataPrep, which means how we will
  pepare the dataset in the good format, and ask the questions, and check the background etc. Do you think this is
  a good idea." Then Report, drfirst-space-b7 (SMSDesign insight), 261116, quoting JL: "I want to create the
  InsightDataPrep block, to develop the tools to deal with a set of data ... like InsightDataPrep-DrFirstExp".
- **What happened**: the ladder has two Blocks for two clocks (`haipipe-insight/ref/insight-ladder.md` § The two
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
- **Answer**: the contract is `haipipe-insight/ref/dataprep.md` (linked from `ref/insight-ladder.md` and the SKILL.md
  route table). `insight_ladder.py` makes each level (`scripts/insight_ladder_prep.py`: `dataprep`, `dataset`, `prep`,
  `step`, `sign`, `run <step> dataset`), `data --prep` refuses an unsigned prep version, and `audit` has a `prep` row
  for a Board a DataPrep Block serves. A step's Run carries haipipe-task's own ticket, which now admits an
  `InsightDataPrep-*` Block in `insight/` and no other (`haipipe-task` 2.0.4). Six run cards at the Data Prep, Prep and
  Step levels; the Workbench Table regenerated.
- **Case**: on the example Board (`blueprints/Project-Ladder/insight/Insight-Example`), with a DataPrep Block serving
  it, `audit` printed `prep 2` (its two hand-made versions); a scratch step's ticket passed every shape check and
  stopped at its missing worker.
- **Guard**: `haipipe-insight/tests/test_dataprep.py` (six tests: names, versions and signature, `--prep` and the audit
  row, a Board no DataPrep serves, a Board in another Project, the ticket); `run_cards.py --check` (77 cards, 0 problems).
- **Still owed**: the workbench page. A DataPrep Block now opens on the base frame's fallback (MindMap, Plan +
  Results), whose header calls it "Insight Board · Dataset investigation". It needs its own page (Background ·
  Datasets · Versions · Steps, a step's checks per dataset, and a Board's data version linking to its prep) and a signed
  example in `blueprints/Project-Ladder/insight/`. `folder-kinds` has no DataPrep row.

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
- **Guard**: `test_dataprep.py` (the config stub); the review card and `haipipe-insight-reviewer-agent` rule 5.
- **Passed on**: whether the Task ticket should export a config's `env:` is haipipe-task's call; no session owns it
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
  it takes a hook in haipipe-task's ticket that runs before the worker (a no-op by default) and that a DataPrep ticket
  fills with this check: haipipe-task's call, put to the user.

## T13 · Audit could not read a DataPrep Block · fixed

- **From**: Report, drfirst-space-b7, 261116, topic C: `audit <InsightDataPrep-DrFirstExp>` printed only "board.md
  names no dataset: or prototype:".
- **Answer**: `audit` sends a DataPrep Block to its own checks (`insight_ladder_prep.audit`): serves, workers, configs,
  outputs, agreed, hash.
- **Case**: on b7's Block: serves 0 · workers 0 · configs 0 · outputs 11 · agreed 2 · hash 0.
- **Guard**: the same test (every row, and each one moving when its case is made).

## T14 · The step review's agent could not write agreed · fixed

- **From**: Report, drfirst-space-b7, 261116, topic D: the card gave run-review-steps to haipipe-task-reviewer-agent,
  whose tools are Read, Grep and Glob, and asked it to mark `agreed:`.
- **Answer**: the review is haipipe-insight-reviewer-agent's (it already writes `agreed:` on a plan it agrees): the
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
- **Guard**: `servers/workbench-insight/tests/test_data_view_shapes.py`; `haipipe-insight/tests/test_dataprep.py`
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
- **Answer so far** (the map sent to the sender, read from the example pair under `blueprints/Project-Ladder/insight/`
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

