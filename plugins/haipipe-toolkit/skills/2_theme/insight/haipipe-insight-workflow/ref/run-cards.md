# Insight Run cards

What the insight workbench shows in each level's Runs panel: one card per button, each with the skill, agent and sign
of its Run and the prompt the button copies. The cards follow the insight ladder (`haipipe-insight/ref/insight-ladder.md`;
b11 s11 · s12 · s13 · s21, JL 261007 plan C): the Question Book (its Block, a release, a question) and the insight Board
(its Block, a Job, a Task). The owning skills keep their authority; `haipipe-insight-workflow` routes the Runs and is
no card's skill: each card names the skill that does the work.

A `🔘 BUTTON` line is `label · <Level> › <Space> · ticket pattern · views <names>`. Level is the insight Board's
`Block`, `Job` or `Task`, the Question Book's `Question Book`, `Release` or `Question`, or the `Guide` (on every tab); Space is one of the older tabbed screen's six, still the keys here
(Description · Idea Studio · Audience Report · Work Details · Runs · Delivery). The pattern is a regular expression on
the Run's folder name: `run-<type>-<target>/` for a soft Run, `rNN_<segment>/` for a hard one. `views` names the
views the button shows in, lowercase-kebab, from either row (`map`, `findings`, `vs-previous`, `cross`); none = every
view of the Space. `🧩 SKILL` names the one skill that does the work, `🤖 AGENT` who does the Run (a review, a check or
an alignment is never the agent that made the thing), `✍️ SIGNS` what a person signs on it, or `none`. `💬 PROMPT` is
the text the button copies; `{folder}` is the Board, Job, Task or release the frame shows, `<…>` the row picked. The
base frame adds its own (Add a topic); a "… ↗" link opens a file and makes no Run, so it has no card.


## Guide › Method · Related Paper (every tab)

🔘 BUTTON   Add a method · Guide › Method · ^run-add-method- · views method
🧩 SKILL    workbench-insight
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /workbench-insight add a method card to the insight Guide: servers/workbench-insight/guide/methods/<slug>.md (its move, what it reads and returns, its tests, its source, the skill that names it), as run-add-method-<slug>.

🔘 BUTTON   Add a paper · Guide › Related Paper · ^run-add-paper- · views related-paper
🧩 SKILL    haipipe-discovery
🤖 AGENT    haipipe-discovery-orchestrator-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-discovery add a related paper to the insight Guide's related/papers.md (its claim, the method it backs, its citation), as run-add-paper-<slug>.

## Block › Description · Map, Question Book, Dataset, Segments

🔘 BUTTON   Add a data version · Block › Description · ^run-add-version-data-v\d+$ · views map dataset
🧩 SKILL    haipipe-insight-meta
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-meta add the next data version to {folder}: one entry in board.md versions: (version · folder, the SPACE-relative data folder · frozen · what is new; a lone file: extract · rows) and a line in meta/meta.md, as run-add-version-data-v<M>; the extract is frozen once added, and say whether it accumulates the earlier rows.

🔘 BUTTON   Add a Job · Block › Description · ^run-add-j\d+$ · views map
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight add a Job to {folder}: one signed release × one data version, jNN_question-vN-<slug>_data-vM/ with a Task per question and a ticket per asked segment (insight_ladder.py job), as run-add-j<NN>; tell me which one clock moved from the Job before it (data or code), never both.

🔘 BUTTON   Propose a segment · Block › Description · ^run-propose-cut- · views segments
🧩 SKILL    haipipe-insight-question
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-question propose a segment for the Question Book {folder} reads: one file proposals/<slug>.md (kind: cut · its filter · from <the Job or reading> · why), as run-propose-cut-<slug>; a segment is part of the plan, so it lands in the next release, never on this Board.

## Block › Idea Studio

🔘 BUTTON   Draw the question map · Block › Idea Studio · ^run-map-questions$
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight draw the question map of {folder} into studio/ from the release's question files (ref/question_map.py), as run-map-questions; it is generated, view only.

## Block › Audience Report · Segment × Reading: Coverage · Tracks · Consistency · Findings

🔘 BUTTON   Update the coverage · Block › Audience Report · ^run-coverage$ · views coverage
🧩 SKILL    haipipe-insight-check
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-check update the coverage of {folder}: which question × segment × Job has an answer, read from the Jobs' run cards and receipts, never the data, as run-coverage.

🔘 BUTTON   Propose questions · Block › Audience Report · ^run-propose-coverage$ · views coverage
🧩 SKILL    haipipe-insight-question
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-question turn the coverage gaps of {folder} (a DIKW level with no question, a segment with no answer) into proposals in the Question Book's proposals/<slug>.md (kind · level · from: coverage · why), as run-propose-coverage; it writes nothing else.

🔘 BUTTON   Draw a track · Block › Audience Report · ^run-track- · views tracks
🧩 SKILL    haipipe-insight-check
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-check draw one question's track across the Jobs of {folder}: its answer in each Job, which clock moved between them, as run-track-<q>.

🔘 BUTTON   Check consistency · Block › Audience Report · ^run-consistency- · views consistency
🧩 SKILL    haipipe-insight-knowledge
🤖 AGENT    haipipe-insight-reviewer-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-knowledge check two Jobs of {folder} against each other: each shared question held, changed or not comparable, and why, as run-consistency-<jA>-<jB>.

🔘 BUTTON   Ask a Block question · Block › Audience Report · ^run-ask-q\d+$ · views findings
🧩 SKILL    haipipe-report
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-report ask a Board question of {folder}: a row in board.md ## Questions and reports/qNN_<topic>/, answered across Jobs, as run-ask-q<NN>; another agent agrees it before it stands.

🔘 BUTTON   Write the report · Block › Audience Report · ^run-report-q\d+$ · views findings
🧩 SKILL    haipipe-report
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-report write a Board question's report in {folder}/reports/qNN_<topic>/ from the Jobs and readings it cites, as run-report-q<NN>; another agent checks it.

🔘 BUTTON   Check a report · Block › Audience Report · ^run-check-q\d+$ · views findings
🧩 SKILL    haipipe-report
🤖 AGENT    haipipe-draft-check-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-report check a Board question's report in {folder} in a fresh context, as run-check-q<NN>: every claim cites a Job, every number traces to a Run.

## Block › Work Details · the Jobs

🔘 BUTTON   Add a Job · Block › Work Details · ^run-add-j\d+$
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight add a Job to {folder}: one signed release × one data version, jNN_question-vN-<slug>_data-vM/ with a Task per question and a ticket per asked segment (insight_ladder.py job), as run-add-j<NN>; tell me which one clock moved from the Job before it (data or code), never both.

🔘 BUTTON   Close a Job · Block › Work Details · ^run-close-j\d+$
🧩 SKILL    haipipe-insight-check
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    the close
💬 PROMPT   /haipipe-insight-check close a Job of {folder} once every page is checked and its comparison written, as run-close-j<NN>; show me what it froze, and I sign the close.

## Block › Runs · All · soft · from below

🔘 BUTTON   Add a Job · Block › Runs · ^run-add-j\d+$
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight add a Job to {folder}: one signed release × one data version, jNN_question-vN-<slug>_data-vM/ with a Task per question and a ticket per asked segment (insight_ladder.py job), as run-add-j<NN>; tell me which one clock moved from the Job before it (data or code), never both.

🔘 BUTTON   Update the coverage · Block › Runs · ^run-coverage$
🧩 SKILL    haipipe-insight-check
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-check update the coverage of {folder}: which question × segment × Job has an answer, read from the Jobs' run cards and receipts, never the data, as run-coverage.

🔘 BUTTON   Check consistency · Block › Runs · ^run-consistency-
🧩 SKILL    haipipe-insight-knowledge
🤖 AGENT    haipipe-insight-reviewer-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-knowledge check two Jobs of {folder} against each other: each shared question held, changed or not comparable, and why, as run-consistency-<jA>-<jB>.

## Block › Delivery · Handoff

🔘 BUTTON   Write the counsel · Block › Delivery · ^run-write-counsel$ · views handoff
🧩 SKILL    haipipe-insight-wisdom
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-wisdom write the Wisdom counsel of {folder} from the latest closed Job's Knowledge pages, tested before a person reads it, as run-write-counsel.

🔘 BUTTON   Draft the handoff · Block › Delivery · ^run-draft-handoff$ · views handoff
🧩 SKILL    haipipe-insight-wisdom
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    the handoff
💬 PROMPT   /haipipe-insight-wisdom draft the Design handoff of {folder} into delivery/handoff-<W>.md: the finding, its strength and the Knowledge results it rests on, its boundary, its pair (question-vN × data-vM), the design consequence and what it must not be read to say, as run-draft-handoff; I sign it (signed: ✅ <YYMMDD>).

## Job › Audience Report · Overall Report, then Segment × Period: Current · vs previous

🔘 BUTTON   Write the overall report · Job › Audience Report · ^run-overall-j\d+$ · views overall-report
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight write the Overall Report of {folder}: each Executive question's page (tNN_X<NN>_<slug>.md: a one-line answer, how sure, numbered points each citing the Task it rests on as (K01 · t30), and in its face one figure under figures: whose title says the outcome and whose table is a cited Run's result table) from the answers below it and nothing else, then draw the figures and print it with ref/overall_report.py, as run-overall-j<NN>; another agent checks each page.

🔘 BUTTON   Write the Data report · Job › Audience Report · ^run-write-t\d+$ · views current
🧩 SKILL    haipipe-insight-data
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-data write the page of data question a question in {folder} from its Runs' generated reports, a part per segment, saying no more than the Data level allows, as run-write-t<NN>; another agent checks it.

🔘 BUTTON   Write the Information report · Job › Audience Report · ^run-write-t\d+$ · views current
🧩 SKILL    haipipe-insight-information
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-information write the page of information question a question in {folder} from its Runs' generated reports, a part per segment, saying no more than the Information level allows, as run-write-t<NN>; another agent checks it.

🔘 BUTTON   Write the Knowledge report · Job › Audience Report · ^run-write-t\d+$ · views current
🧩 SKILL    haipipe-insight-knowledge
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-knowledge write the page of knowledge question a question in {folder} from its Runs' generated reports, a part per segment, saying no more than the Knowledge level allows, as run-write-t<NN>; another agent checks it.

🔘 BUTTON   Write the Wisdom report · Job › Audience Report · ^run-write-t\d+$ · views current
🧩 SKILL    haipipe-insight-wisdom
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-wisdom write the page of wisdom question a question in {folder} from its Runs' generated reports, a part per segment, saying no more than the Wisdom level allows, as run-write-t<NN>; another agent checks it.

🔘 BUTTON   Check a report · Job › Audience Report · ^run-check-t\d+$ · views current overall-report
🧩 SKILL    haipipe-report
🤖 AGENT    haipipe-draft-check-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-report check a question's page in {folder} in a fresh context, as run-check-t<NN>: one verdict per need against its pass: line (haipipe-insight ref/deliverables.py <Task> lists them), every number traces to its Run's result/, every need is cited, and nothing claims more than its level allows.

🔘 BUTTON   Pool or split · Job › Audience Report · ^run-pool-t\d+$ · views cross
🧩 SKILL    haipipe-insight-knowledge
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-knowledge read a question's Cross Run in {folder} (rNN_cross) under the release's thresholds and write its verdict, POOL, SPLIT or UNDETERMINED, as run-pool-t<NN>; one test of the difference, never two partitions' significance compared.

🔘 BUTTON   Compare with the Job before · Job › Audience Report · ^run-compare-j\d+$ · views vs-previous
🧩 SKILL    haipipe-insight-knowledge
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-knowledge compare {folder} with the Job before it into reports/vs-<prev>.md, one row per question (held · changed · new finding · new question · dropped · not comparable) and why (which clock moved); a kept question's tables must match by sha256 when only the code moved; as run-compare-j<prev>.

🔘 BUTTON   Propose questions · Job › Audience Report · ^run-propose-j\d+$ · views vs-previous
🧩 SKILL    haipipe-insight-question
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-question file each new or changed question, and each gap {folder} could not answer, as one proposals/<slug>.md in the Question Book (kind · level · from: this Job · why), as run-propose-j<NN>; it writes nothing else.

## Job › Work Details · the Job's steps: 1 · Launch · 2 · Run · 3 · Write · 4 · Check · 5 · Compare · 6 · Close

Each step is a tab of the Job's Work (b11 s12, 261022): its work panel (the step's input, the first card's prompt with
the person's notes, what is running, what a person signs) over its result. `views` names the step a card belongs to.

🔘 BUTTON   Run the Job · Job › Work Details · ^run-launch-j\d+$ · views launch
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-task-orchestrator-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight run the Job {folder}: check power per segment first (run-power-j<NN>), then every Task's tickets runs/rNN_<segment>/run.sh, as run-launch-j<NN>; report each Run ok, refused (with its reason) or failed.

🔘 BUTTON   Measure the power · Job › Work Details · ^run-power-j\d+$ · views launch
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight measure n and power per segment of {folder} before any outcome is read, against the release's thresholds.yaml, as run-power-j<NN>; a segment that cannot answer is refused with its minimum detectable effect.

🔘 BUTTON   Run a segment · Job › Work Details · ^r\d\d_ · views run
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-task-orchestrator-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight run one question of {folder} on one segment: runs/rNN_<segment>/run.sh (ref/run_job.py reads the question and script from the release, writes only result/ and run.yaml); a refusal is an answer.

🔘 BUTTON   Pool or split · Job › Work Details · ^run-pool-t\d+$ · views run
🧩 SKILL    haipipe-insight-knowledge
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-knowledge read a question's Cross Run in {folder} (rNN_cross) under the release's thresholds and write its verdict, POOL, SPLIT or UNDETERMINED, as run-pool-t<NN>; one test of the difference, never two partitions' significance compared.

🔘 BUTTON   Write the Data report · Job › Work Details · ^run-write-t\d+$ · views write
🧩 SKILL    haipipe-insight-data
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-data write the page of each data question in {folder} not written yet, from its Runs' generated reports, a part per segment, saying no more than the Data level allows, as run-write-t<NN>; another agent checks it.

🔘 BUTTON   Write the Information report · Job › Work Details · ^run-write-t\d+$ · views write
🧩 SKILL    haipipe-insight-information
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-information write the page of each information question in {folder} not written yet, from its Runs' generated reports, a part per segment, saying no more than the Information level allows, as run-write-t<NN>; another agent checks it.

🔘 BUTTON   Write the Knowledge report · Job › Work Details · ^run-write-t\d+$ · views write
🧩 SKILL    haipipe-insight-knowledge
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-knowledge write the page of each knowledge question in {folder} not written yet, from its Runs' generated reports, a part per segment, saying no more than the Knowledge level allows, as run-write-t<NN>; another agent checks it.

🔘 BUTTON   Write the Wisdom report · Job › Work Details · ^run-write-t\d+$ · views write
🧩 SKILL    haipipe-insight-wisdom
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-wisdom write the page of each wisdom question in {folder} not written yet, from the checked answers below it, saying no more than the Wisdom level allows, as run-write-t<NN>; a person signs the counsel, and another agent checks it.

🔘 BUTTON   Write the overall report · Job › Work Details · ^run-overall-j\d+$ · views write
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight write the Overall Report of {folder}: each Executive question's page (tNN_X<NN>_<slug>.md: a one-line answer, how sure, numbered points each citing the Task it rests on as (K01 · t30), and in its face one figure under figures: whose title says the outcome and whose table is a cited Run's result table) from the answers below it and nothing else, then draw the figures and print it with ref/overall_report.py, as run-overall-j<NN>; another agent checks each page.

🔘 BUTTON   Check alignment · Job › Work Details · ^run-check-alignment-t\d+$ · views check
🧩 SKILL    haipipe-insight-check
🤖 AGENT    haipipe-insight-reviewer-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-check check each answered segment of a question in {folder} against its question and plan, in a fresh context, as run-check-alignment-t<NN>; write only the checker's output.

🔘 BUTTON   Check a report · Job › Work Details · ^run-check-t\d+$ · views check
🧩 SKILL    haipipe-report
🤖 AGENT    haipipe-draft-check-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-report check each written page in {folder} not checked yet, in a fresh context, as run-check-t<NN>: one verdict per need against its pass: line (haipipe-insight ref/deliverables.py <Task> lists them), every number traces to its Run's result/, every need is cited, and nothing claims more than its level allows; write the verdict on the page's check: line.

🔘 BUTTON   Compare with the Job before · Job › Work Details · ^run-compare-j\d+$ · views compare
🧩 SKILL    haipipe-insight-knowledge
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-knowledge compare {folder} with the Job before it into reports/vs-<prev>.md, one row per question (held · changed · new finding · new question · dropped · not comparable) and why (which clock moved); a kept question's tables must match by sha256 when only the code moved; as run-compare-j<prev>.

🔘 BUTTON   Propose questions · Job › Work Details · ^run-propose-j\d+$ · views compare
🧩 SKILL    haipipe-insight-question
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-question file each new or changed question, and each gap {folder} could not answer, as one proposals/<slug>.md in the Question Book (kind · level · from: this Job · why), as run-propose-j<NN>; it writes nothing else.

🔘 BUTTON   Close the Job · Job › Work Details · ^run-close-j\d+$ · views close
🧩 SKILL    haipipe-insight-check
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    the close
💬 PROMPT   /haipipe-insight-check close {folder} once every page is checked and its comparison written, as run-close-j<NN>; show me what it froze, and I sign the close.

## Job › Runs · All · hard · soft · launch · power · compare · propose · close

🔘 BUTTON   Run the Job · Job › Runs · ^run-launch-j\d+$
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-task-orchestrator-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight run the Job {folder}: check power per segment first (run-power-j<NN>), then every Task's tickets runs/rNN_<segment>/run.sh, as run-launch-j<NN>; report each Run ok, refused (with its reason) or failed.

🔘 BUTTON   Measure the power · Job › Runs · ^run-power-j\d+$ · views power
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight measure n and power per segment of {folder} before any outcome is read, against the release's thresholds.yaml, as run-power-j<NN>; a segment that cannot answer is refused with its minimum detectable effect.

🔘 BUTTON   Run a segment · Job › Runs · ^r\d\d_ · views hard
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-task-orchestrator-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight run one question of {folder} on one segment: runs/rNN_<segment>/run.sh (ref/run_job.py reads the question and script from the release, writes only result/ and run.yaml); a refusal is an answer.

🔘 BUTTON   Compare with the Job before · Job › Runs · ^run-compare-j\d+$ · views compare
🧩 SKILL    haipipe-insight-knowledge
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-knowledge compare {folder} with the Job before it into reports/vs-<prev>.md, one row per question (held · changed · new finding · new question · dropped · not comparable) and why (which clock moved); a kept question's tables must match by sha256 when only the code moved; as run-compare-j<prev>.

🔘 BUTTON   Propose questions · Job › Runs · ^run-propose-j\d+$ · views propose
🧩 SKILL    haipipe-insight-question
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-question file each new or changed question, and each gap {folder} could not answer, as one proposals/<slug>.md in the Question Book (kind · level · from: this Job · why), as run-propose-j<NN>; it writes nothing else.

🔘 BUTTON   Close the Job · Job › Runs · ^run-close-j\d+$ · views close
🧩 SKILL    haipipe-insight-check
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    the close
💬 PROMPT   /haipipe-insight-check close {folder} once every page is checked and its comparison written, as run-close-j<NN>; show me what it froze, and I sign the close.

## Task › Audience Report · Table · Reading

🔘 BUTTON   Write the Data report · Task › Audience Report · ^run-write-t\d+$
🧩 SKILL    haipipe-insight-data
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-data write the page of data question {folder} from its Runs' generated reports, a part per segment, saying no more than the Data level allows, as run-write-t<NN>; another agent checks it.

🔘 BUTTON   Write the Information report · Task › Audience Report · ^run-write-t\d+$
🧩 SKILL    haipipe-insight-information
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-information write the page of information question {folder} from its Runs' generated reports, a part per segment, saying no more than the Information level allows, as run-write-t<NN>; another agent checks it.

🔘 BUTTON   Write the Knowledge report · Task › Audience Report · ^run-write-t\d+$
🧩 SKILL    haipipe-insight-knowledge
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-knowledge write the page of knowledge question {folder} from its Runs' generated reports, a part per segment, saying no more than the Knowledge level allows, as run-write-t<NN>; another agent checks it.

🔘 BUTTON   Write the Wisdom report · Task › Audience Report · ^run-write-t\d+$
🧩 SKILL    haipipe-insight-wisdom
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-wisdom write the page of wisdom question {folder} from its Runs' generated reports, a part per segment, saying no more than the Wisdom level allows, as run-write-t<NN>; another agent checks it.

🔘 BUTTON   Check a report · Task › Audience Report · ^run-check-t\d+$
🧩 SKILL    haipipe-report
🤖 AGENT    haipipe-draft-check-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-report check the page of {folder} in a fresh context, as run-check-t<NN>: one verdict per need against its pass: line (haipipe-insight ref/deliverables.py <Task> lists them), every number traces to its Run's result/, every need is cited, and nothing claims more than its level allows.

🔘 BUTTON   Pool or split · Task › Audience Report · ^run-pool-t\d+$ · views reading
🧩 SKILL    haipipe-insight-knowledge
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-knowledge read the Cross Run of {folder} (rNN_cross) under the release's thresholds and write its verdict, POOL, SPLIT or UNDETERMINED, as run-pool-t<NN>; one test of the difference, never two partitions' significance compared.

## Task › Work Details · Segments

🔘 BUTTON   Run a segment · Task › Work Details · ^r\d\d_
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-task-orchestrator-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight run {folder} on one segment: runs/rNN_<segment>/run.sh (ref/run_job.py reads the question and script from the release, writes only result/ and run.yaml); a refusal is an answer.

🔘 BUTTON   Check alignment · Task › Work Details · ^run-check-alignment-t\d+$
🧩 SKILL    haipipe-insight-check
🤖 AGENT    haipipe-insight-reviewer-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-check check each answered segment of {folder} against its question and plan, in a fresh context, as run-check-alignment-t<NN>; write only the checker's output.

## Task › Runs · All · hard · soft

🔘 BUTTON   Run a segment · Task › Runs · ^r\d\d_ · views hard
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-task-orchestrator-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight run {folder} on one segment: runs/rNN_<segment>/run.sh (ref/run_job.py reads the question and script from the release, writes only result/ and run.yaml); a refusal is an answer.

🔘 BUTTON   Check alignment · Task › Runs · ^run-check-alignment-t\d+$ · views soft
🧩 SKILL    haipipe-insight-check
🤖 AGENT    haipipe-insight-reviewer-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-check check each answered segment of {folder} against its question and plan, in a fresh context, as run-check-alignment-t<NN>; write only the checker's output.

## Question Book › Description · the releases, the proposals

🔘 BUTTON   Take the proposals · Question Book › Description · ^run-triage-proposals-question-v\d+$ · views proposals
🧩 SKILL    haipipe-insight-question
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-question triage the open proposals of {folder} into one batch for the next release: each taken (taken-in: question-vN), declined with a reason, or left open, as run-triage-proposals-question-v<N>; one release per batch, never per proposal.

🔘 BUTTON   Open a release · Question Book › Description · ^run-open-version-question-v\d+$ · views releases
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight open the next release of {folder} from the newest signed one (insight_ladder.py version --slug <what-it-is>): every question kept and pointed back, the segments, thresholds and src/ copied, as run-open-version-question-v<N>; then apply the triaged batch.

## Question Book › Idea Studio

🔘 BUTTON   Draw the question map · Question Book › Idea Studio · ^run-map-questions$
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight draw the question map of {folder}'s newest release into studio/ (ref/question_map.py), as run-map-questions; it is generated, view only.

## Question Book › Runs

🔘 BUTTON   Carry a board over · Question Book › Runs · ^run-carry-
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    the carry
💬 PROMPT   /haipipe-insight carry an older Insight Block into a release of {folder} word for word (ref/prototype_from_block.py; a register board first through ref/carry_over.py), as run-carry-<board>; verify every field is equal, and leave the old one as it is.

## Release › Work Details · its questions

🔘 BUTTON   Ask a question · Release › Work Details · ^run-ask-[dikw]\d\d$
🧩 SKILL    haipipe-insight-question
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-question ask one question into the open release {folder} from plain words: its level, id (never reused) and Task tNN_<L><NN>_<slug>/question.md (insight_ladder.py question), as run-ask-<l><nn>; never answer it here.

🔘 BUTTON   Review the questions · Release › Work Details · ^run-review-questions-question-v\d+$
🧩 SKILL    haipipe-report
🤖 AGENT    haipipe-insight-reviewer-agent
✍️ SIGNS    a change
💬 PROMPT   /haipipe-report review the new and changed questions of {folder} (Q1–Q7) in a fresh context, as run-review-questions-question-v<N>: propose keep, split, merge or move, never reword; I sign each change.

## Release › Description · its segments

🔘 BUTTON   Set the segments · Release › Description · ^run-set-segments-question-v\d+$ · views segments
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    the segments
💬 PROMPT   /haipipe-insight set the segments of {folder} before any outcome is seen: partitions.md (full, each filter, cross) and thresholds.yaml (power.smallest_effect_pp, alphas, floors), each with why, as run-set-segments-question-v<N>; I sign the segments.

## Release › Delivery · the signature

🔘 BUTTON   Sign the release · Release › Delivery · ^run-sign-release-question-v\d+$
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    the release
💬 PROMPT   /haipipe-insight get {folder} ready to sign, as run-sign-release-question-v<N>: every new or changed question agreed by another agent, every script reviewed, the segments signed; show me the release, and record my signature (insight_ladder.py sign --date YYMMDD). It is frozen after.

## Question › Work Details · its plan and script

🔘 BUTTON   Plan the evidence · Question › Work Details · ^run-plan-evidence-[dikw]\d\d$
🧩 SKILL    haipipe-insight-evidence-plan
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-evidence-plan plan the needs of the question {folder} from its ask alone (compute · cite · judge; each compute need its nine spec fields), as run-plan-evidence-<l><nn>; another agent agrees them.

🔘 BUTTON   Review the evidence plan · Question › Work Details · ^run-review-plan-[dikw]\d\d$
🧩 SKILL    haipipe-insight-evidence-plan
🤖 AGENT    haipipe-insight-reviewer-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-evidence-plan review the needs of {folder} in a fresh context, as run-review-plan-<l><nn>: agree them (agreed: ✅ <YYMMDD>) or return them with what is missing; never rewrite them.

🔘 BUTTON   Write the script · Question › Work Details · ^run-write-script-[dikw]\d\d$
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-task-creator-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight write the one script of {folder}: scripts/<slug>.py with its SPEC and COLUMNS lines, returning exactly the agreed needs' output files, reading no path and naming no dataset or segment, as run-write-script-<l><nn>.

🔘 BUTTON   Review the script · Question › Work Details · ^run-review-script-[dikw]\d\d$
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-task-reviewer-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight review the script of {folder} against its agreed needs in a fresh context, as run-review-script-<l><nn>: it computes what each spec says and nothing else; return it with what is wrong, never fix it yourself.


## Data Prep › Work Details · the prep versions (ref/dataprep.md)

🔘 BUTTON   Open a prep version · Data Prep › Work Details · ^run-open-version-prep-v\d+$
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight open the next prep version of {folder} from the newest signed one (insight_ladder.py prep --slug <what-it-changes>), as run-open-version-prep-v<N>: every step carried, its agreed line cleared; name the change it is for.

## Prep › Work Details · its steps

🔘 BUTTON   Review the steps · Prep › Work Details · ^run-review-steps-prep-v\d+$
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-insight-reviewer-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight review every step of {folder} in a fresh context, as run-review-steps-prep-v<N>: each step's script does what its step.md says it reads, writes and checks, through run(ctx) only (ctx.raw, ctx.prev, ctx.refs; nothing else read, nothing written but ctx.out and one light ctx.result/metrics.json); every check on the spec is enforced (ctx.refuse), not only listed; nothing it writes beside the rows, and nothing in a Result, shows a record value (insight_ladder.py audit shows records 0, or you read each line); the first step writes the experiment card and stops on a stated-versus-observed mismatch; step.md cut: and params: name every key its script reads, and the script refuses an unknown key in a dict it reads and leaves a dict it does not read alone; a step that imports a library pins its sha256 in its own code and refuses when it differs; no step reads an outcome. Write agreed: ✅ <YYMMDD> in a step's step.md when it passes (your one write); return the rest with what is wrong, never fix them yourself.

🔘 BUTTON   Sign the prep version · Prep › Delivery · ^run-sign-prep-v\d+$
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    the prep version
💬 PROMPT   /haipipe-insight get {folder} ready to sign, as run-sign-prep-v<N>: every step agreed, every step's script exposing run(ctx); show me the steps and their checks, and record my signature (insight_ladder.py sign --date YYMMDD). It is frozen after, its code's hash pinned; a Board runs it in a data Job.

## Step › Work Details · its script and its datasets

🔘 BUTTON   Write the step's script · Step › Work Details · ^run-write-script-t\d+$
🧩 SKILL    haipipe-task-for-data
🤖 AGENT    haipipe-task-creator-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-task-for-data write the worker of {folder}: scripts/<worker>.py doing what its face says it reads, writes and checks, one config per dataset in scripts/config/, writing rows only to the store, as run-write-script-t<NN>.

🔘 BUTTON   Review the step's script · Step › Work Details · ^run-review-script-t\d+$
🧩 SKILL    haipipe-task-for-data
🤖 AGENT    haipipe-task-reviewer-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-task-for-data review the worker of {folder} against its face in a fresh context, as run-review-script-t<NN>: it reads, writes and checks what the face says and nothing else, no outcome shapes a row; return it with what is wrong, never fix it yourself.


## Data Job › Runs · a Board runs a signed prep version (ref/dataprep.md)

🔘 BUTTON   Run a data step · Data Job › Runs · ^r\d\d_
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-task-orchestrator-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight run the data Job {folder} (python ref/run_prep.py {folder}, or a step's own run.sh), as rNN_<dataset>: its steps in order on the Board's raw export, each stopping the chain when it refuses or fails; the last step's folder becomes the Board's next data version. Report each step's status and reason, never a row.


## Gates

Each gate belongs to one level and one Run; the Run that passes it records it, and the scaffold refuses to go past
it (`haipipe-insight/scripts/insight_ladder.py`).

```text
gate                     level      Run that passes it          what must hold
a question agreed        Question   run-review-plan-<l><nn>     another agent agreed its needs (agreed: ✅)
a script reviewed        Question   run-review-script-<l><nn>   another agent passed it against the agreed needs
the segments set             Release    run-set-segments-question-v<N>           full and every segment named, each with why; a person signed
a release signed         Release    run-sign-release-question-v<N>       the three above for every new or changed question;
                                                                a person signed (signed: ✅ <YYMMDD>); frozen after
a data version frozen    Block      run-add-version-data-v<M>        in board.md versions:, SPACE-relative, never edited
a Job added              Block      run-add-j<NN>               a signed release × a frozen data version, a new pair,
                                                                one clock moved
power before contrast    Job        run-power-j<NN>, rNN_…      the segment can answer (MDE ≤ the smallest effect), else refused
the output gated         Task       rNN_<segment>             the tables equal the spec's outputs; no row-level table
a page checked           Task       run-check-t<NN>             another agent's CHECK closed after the Run's content
a Job closed             Job        run-close-j<NN>             every page checked, the comparison written; a person signed
a handoff signed         Block      run-draft-handoff           a person signed; Design reads only a signed handoff
a step agreed            Step       run-review-steps-prep-v<N>  another agent passed its script against its face (agreed: ✅)
a prep version signed    Prep       run-sign-prep-v<N>          every step agreed and its script run(ctx); a person
                                                                signed; the code's hash pinned
a data version made      Data Job   rNN_<dataset> (last step)   every step done in order on the Board's raw export;
                                                                the ready folder registered with prep: and made-by:
```
