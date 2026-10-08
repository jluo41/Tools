# Insight Run cards

What the insight workbench shows in each level's Runs panel: one card per button, each with the skill, agent and sign
of its Run and the prompt the button copies. The cards follow the insight ladder (`haipipe-insight/ref/insight-ladder.md`;
b11 s11 · s12 · s13 · s21, JL 261007 plan C): the Prototype (its Block, a release, a question) and the insight Board
(its Block, a Job, a Task). The owning skills keep their authority; `haipipe-insight-workflow` routes the Runs and is
the card's skill only where it signs, launches or closes.

A `🔘 BUTTON` line is `label · <Level> › <Space> · ticket pattern · views <names>`. Level is the insight Board's
`Block`, `Job` or `Task`, the Prototype's `Prototype`, `Release` or `Question`, or the `Guide` (on every tab); Space is one of the six
(Description · Idea Studio · Audience Report · Work Details · Runs · Delivery). The pattern is a regular expression on
the Run's folder name: `run-<type>-<target>/` for a soft Run, `rNN_<partition>/` for a hard one. `views` names the
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

## Block › Description · Map, Prototype, Dataset, Partitions

🔘 BUTTON   Add a data version · Block › Description · ^run-add-version-v\d+$ · views map dataset
🧩 SKILL    haipipe-insight-meta
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-meta add the next data version to {folder}: one entry in board.md versions: (version · extract, SPACE-relative · frozen · rows · what is new) and a line in meta/meta.md, as run-add-version-v<M>; the extract is frozen once added, and say whether it accumulates the earlier rows.

🔘 BUTTON   Add a Job · Block › Description · ^run-add-j\d+$ · views map
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight add a Job to {folder}: one signed release × one data version, jNN_pN_<D>vM/ with a Task per question and a ticket per asked cut (insight_ladder.py job), as run-add-j<NN>; tell me which one clock moved from the Job before it (data or code), never both.

🔘 BUTTON   Propose a cut · Block › Description · ^run-propose-cut- · views partitions
🧩 SKILL    haipipe-insight-question
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-question propose a cut for the Prototype {folder} reads: one file proposals/<slug>.md (kind: cut · its filter · from <the Job or reading> · why), as run-propose-cut-<slug>; a cut is part of the plan, so it lands in the next release, never on this Board.

## Block › Idea Studio

🔘 BUTTON   Draw the question map · Block › Idea Studio · ^run-map-questions$
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight draw the question map of {folder} into studio/ from the release's question files (ref/question_map.py), as run-map-questions; it is generated, view only.

## Block › Audience Report · Partition × Reading: Coverage · Tracks · Consistency · Findings

🔘 BUTTON   Update the coverage · Block › Audience Report · ^run-coverage$ · views coverage
🧩 SKILL    haipipe-insight-check
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-check update the coverage of {folder}: which question × cut × Job has an answer, read from the Jobs' run cards and receipts, never the data, as run-coverage.

🔘 BUTTON   Propose questions · Block › Audience Report · ^run-propose-coverage$ · views coverage
🧩 SKILL    haipipe-insight-question
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-question turn the coverage gaps of {folder} (a DIKW level with no question, a cut with no answer) into proposals in the Prototype's proposals/<slug>.md (kind · level · from: coverage · why), as run-propose-coverage; it writes nothing else.

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
🧩 SKILL    haipipe-question
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-question ask a Board question of {folder}: a row in board.md ## Questions and reports/qNN_<topic>/, answered across Jobs, as run-ask-q<NN>; another agent agrees it before it stands.

🔘 BUTTON   Write the report · Block › Audience Report · ^run-report-q\d+$ · views findings
🧩 SKILL    haipipe-report
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-report write a Board question's report in {folder}/reports/qNN_<topic>/ from the Jobs and readings it cites, as run-report-q<NN>; another agent checks it.

🔘 BUTTON   Check a report · Block › Audience Report · ^run-check-q\d+$ · views findings
🧩 SKILL    haipipe-report
🤖 AGENT    haipipe-page-check-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-report check a Board question's report in {folder} in a fresh context, as run-check-q<NN>: every claim cites a Job, every number traces to a Run.

## Block › Work Details · the Jobs

🔘 BUTTON   Add a Job · Block › Work Details · ^run-add-j\d+$
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight add a Job to {folder}: one signed release × one data version, jNN_pN_<D>vM/ with a Task per question and a ticket per asked cut (insight_ladder.py job), as run-add-j<NN>; tell me which one clock moved from the Job before it (data or code), never both.

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
💬 PROMPT   /haipipe-insight add a Job to {folder}: one signed release × one data version, jNN_pN_<D>vM/ with a Task per question and a ticket per asked cut (insight_ladder.py job), as run-add-j<NN>; tell me which one clock moved from the Job before it (data or code), never both.

🔘 BUTTON   Update the coverage · Block › Runs · ^run-coverage$
🧩 SKILL    haipipe-insight-check
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-check update the coverage of {folder}: which question × cut × Job has an answer, read from the Jobs' run cards and receipts, never the data, as run-coverage.

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
💬 PROMPT   /haipipe-insight-wisdom draft the Design handoff of {folder} into delivery/handoff-<W>.md: the finding, its strength and the Knowledge results it rests on, its boundary, its pair (pN × vM), the design consequence and what it must not be read to say, as run-draft-handoff; I sign it (signed: ✅ <YYMMDD>).

## Job › Audience Report · Partition × Period: Current · vs previous

🔘 BUTTON   Write the Data report · Job › Audience Report · ^run-write-t\d+$ · views current
🧩 SKILL    haipipe-insight-data
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-data write the page of data question a question in {folder} from its Runs' generated reports, a part per cut, saying no more than the Data level allows, as run-write-t<NN>; another agent checks it.

🔘 BUTTON   Write the Information report · Job › Audience Report · ^run-write-t\d+$ · views current
🧩 SKILL    haipipe-insight-information
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-information write the page of information question a question in {folder} from its Runs' generated reports, a part per cut, saying no more than the Information level allows, as run-write-t<NN>; another agent checks it.

🔘 BUTTON   Write the Knowledge report · Job › Audience Report · ^run-write-t\d+$ · views current
🧩 SKILL    haipipe-insight-knowledge
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-knowledge write the page of knowledge question a question in {folder} from its Runs' generated reports, a part per cut, saying no more than the Knowledge level allows, as run-write-t<NN>; another agent checks it.

🔘 BUTTON   Write the Wisdom report · Job › Audience Report · ^run-write-t\d+$ · views current
🧩 SKILL    haipipe-insight-wisdom
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-wisdom write the page of wisdom question a question in {folder} from its Runs' generated reports, a part per cut, saying no more than the Wisdom level allows, as run-write-t<NN>; another agent checks it.

🔘 BUTTON   Check a report · Job › Audience Report · ^run-check-t\d+$ · views current
🧩 SKILL    haipipe-report
🤖 AGENT    haipipe-page-check-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-report check a question's page in {folder} in a fresh context, as run-check-t<NN>: every number traces to its Run's result/, every need is cited, and nothing claims more than its level allows.

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
💬 PROMPT   /haipipe-insight-question file each new or changed question, and each gap {folder} could not answer, as one proposals/<slug>.md in the Prototype (kind · level · from: this Job · why), as run-propose-j<NN>; it writes nothing else.

## Job › Work Details · the Job → Task → Run tree

🔘 BUTTON   Run the Job · Job › Work Details · ^run-launch-j\d+$
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-task-orchestrator-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight run the Job {folder}: check power per cut first (run-power-j<NN>), then every Task's tickets runs/rNN_<partition>/run.sh, as run-launch-j<NN>; report each Run ok, refused (with its reason) or failed.

🔘 BUTTON   Run a partition · Job › Work Details · ^r\d\d_
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-task-orchestrator-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight run one question of {folder} on one cut: runs/rNN_<partition>/run.sh (ref/run_job.py reads the question and script from the release, writes only result/ and run.yaml); a refusal is an answer.

🔘 BUTTON   Check alignment · Job › Work Details · ^run-check-alignment-t\d+$
🧩 SKILL    haipipe-insight-check
🤖 AGENT    haipipe-insight-reviewer-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-check check each answered cut of a question in {folder} against its question and plan, in a fresh context, as run-check-alignment-t<NN>; write only the checker's output.

## Job › Runs · All · hard · soft · launch · power · compare · propose · close

🔘 BUTTON   Run the Job · Job › Runs · ^run-launch-j\d+$
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-task-orchestrator-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight run the Job {folder}: check power per cut first (run-power-j<NN>), then every Task's tickets runs/rNN_<partition>/run.sh, as run-launch-j<NN>; report each Run ok, refused (with its reason) or failed.

🔘 BUTTON   Measure the power · Job › Runs · ^run-power-j\d+$ · views power
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight measure n and power per cut of {folder} before any outcome is read, against the release's thresholds.yaml, as run-power-j<NN>; a cut that cannot answer is refused with its minimum detectable effect.

🔘 BUTTON   Run a partition · Job › Runs · ^r\d\d_ · views hard
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-task-orchestrator-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight run one question of {folder} on one cut: runs/rNN_<partition>/run.sh (ref/run_job.py reads the question and script from the release, writes only result/ and run.yaml); a refusal is an answer.

🔘 BUTTON   Compare with the Job before · Job › Runs · ^run-compare-j\d+$ · views compare
🧩 SKILL    haipipe-insight-knowledge
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-knowledge compare {folder} with the Job before it into reports/vs-<prev>.md, one row per question (held · changed · new finding · new question · dropped · not comparable) and why (which clock moved); a kept question's tables must match by sha256 when only the code moved; as run-compare-j<prev>.

🔘 BUTTON   Propose questions · Job › Runs · ^run-propose-j\d+$ · views propose
🧩 SKILL    haipipe-insight-question
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-question file each new or changed question, and each gap {folder} could not answer, as one proposals/<slug>.md in the Prototype (kind · level · from: this Job · why), as run-propose-j<NN>; it writes nothing else.

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
💬 PROMPT   /haipipe-insight-data write the page of data question {folder} from its Runs' generated reports, a part per cut, saying no more than the Data level allows, as run-write-t<NN>; another agent checks it.

🔘 BUTTON   Write the Information report · Task › Audience Report · ^run-write-t\d+$
🧩 SKILL    haipipe-insight-information
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-information write the page of information question {folder} from its Runs' generated reports, a part per cut, saying no more than the Information level allows, as run-write-t<NN>; another agent checks it.

🔘 BUTTON   Write the Knowledge report · Task › Audience Report · ^run-write-t\d+$
🧩 SKILL    haipipe-insight-knowledge
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-knowledge write the page of knowledge question {folder} from its Runs' generated reports, a part per cut, saying no more than the Knowledge level allows, as run-write-t<NN>; another agent checks it.

🔘 BUTTON   Write the Wisdom report · Task › Audience Report · ^run-write-t\d+$
🧩 SKILL    haipipe-insight-wisdom
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-wisdom write the page of wisdom question {folder} from its Runs' generated reports, a part per cut, saying no more than the Wisdom level allows, as run-write-t<NN>; another agent checks it.

🔘 BUTTON   Check a report · Task › Audience Report · ^run-check-t\d+$
🧩 SKILL    haipipe-report
🤖 AGENT    haipipe-page-check-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-report check the page of {folder} in a fresh context, as run-check-t<NN>: every number traces to its Run's result/, every need is cited, and nothing claims more than its level allows.

🔘 BUTTON   Pool or split · Task › Audience Report · ^run-pool-t\d+$ · views reading
🧩 SKILL    haipipe-insight-knowledge
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-knowledge read the Cross Run of {folder} (rNN_cross) under the release's thresholds and write its verdict, POOL, SPLIT or UNDETERMINED, as run-pool-t<NN>; one test of the difference, never two partitions' significance compared.

## Task › Work Details · Partitions

🔘 BUTTON   Run a partition · Task › Work Details · ^r\d\d_
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-task-orchestrator-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight run {folder} on one cut: runs/rNN_<partition>/run.sh (ref/run_job.py reads the question and script from the release, writes only result/ and run.yaml); a refusal is an answer.

🔘 BUTTON   Check alignment · Task › Work Details · ^run-check-alignment-t\d+$
🧩 SKILL    haipipe-insight-check
🤖 AGENT    haipipe-insight-reviewer-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-check check each answered cut of {folder} against its question and plan, in a fresh context, as run-check-alignment-t<NN>; write only the checker's output.

## Task › Runs · All · hard · soft

🔘 BUTTON   Run a partition · Task › Runs · ^r\d\d_ · views hard
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-task-orchestrator-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight run {folder} on one cut: runs/rNN_<partition>/run.sh (ref/run_job.py reads the question and script from the release, writes only result/ and run.yaml); a refusal is an answer.

🔘 BUTTON   Check alignment · Task › Runs · ^run-check-alignment-t\d+$ · views soft
🧩 SKILL    haipipe-insight-check
🤖 AGENT    haipipe-insight-reviewer-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-check check each answered cut of {folder} against its question and plan, in a fresh context, as run-check-alignment-t<NN>; write only the checker's output.

## Prototype › Description · the releases, the proposals

🔘 BUTTON   Take the proposals · Prototype › Description · ^run-triage-proposals-p\d+$ · views proposals
🧩 SKILL    haipipe-insight-question
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight-question triage the open proposals of {folder} into one batch for the next release: each taken (taken-in: pN), declined with a reason, or left open, as run-triage-proposals-p<N>; one release per batch, never per proposal.

🔘 BUTTON   Open a release · Prototype › Description · ^run-open-version-p\d+$ · views releases
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight open the next release of {folder} from the newest signed one (insight_ladder.py version --slug <what-it-is>): every question kept and pointed back, the cuts, thresholds and src/ copied, as run-open-version-p<N>; then apply the triaged batch.

## Prototype › Idea Studio

🔘 BUTTON   Draw the question map · Prototype › Idea Studio · ^run-map-questions$
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight draw the question map of {folder}'s newest release into studio/ (ref/question_map.py), as run-map-questions; it is generated, view only.

## Prototype › Runs

🔘 BUTTON   Carry a board over · Prototype › Runs · ^run-carry-
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

🔘 BUTTON   Review the questions · Release › Work Details · ^run-review-questions-p\d+$
🧩 SKILL    haipipe-question-review
🤖 AGENT    haipipe-insight-reviewer-agent
✍️ SIGNS    a change
💬 PROMPT   /haipipe-question-review review the new and changed questions of {folder} (Q1–Q7) in a fresh context, as run-review-questions-p<N>: propose keep, split, merge or move, never reword; I sign each change.

## Release › Description · its cuts

🔘 BUTTON   Set the cuts · Release › Description · ^run-set-cuts-p\d+$ · views partitions
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    the cuts
💬 PROMPT   /haipipe-insight set the cuts of {folder} before any outcome is seen: partitions.md (full, each filter, cross) and thresholds.yaml (power.smallest_effect_pp, alphas, floors), each with why, as run-set-cuts-p<N>; I sign the cuts.

## Release › Delivery · the signature

🔘 BUTTON   Sign the release · Release › Delivery · ^run-sign-release-p\d+$
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-insight-agent
✍️ SIGNS    the release
💬 PROMPT   /haipipe-insight get {folder} ready to sign, as run-sign-release-p<N>: every new or changed question agreed by another agent, every script reviewed, the cuts signed; show me the release, and record my signature (insight_ladder.py sign --date YYMMDD). It is frozen after.

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
💬 PROMPT   /haipipe-insight write the one script of {folder}: scripts/<slug>.py with its SPEC and COLUMNS lines, returning exactly the agreed needs' output files, reading no path and naming no dataset or cut, as run-write-script-<l><nn>.

🔘 BUTTON   Review the script · Question › Work Details · ^run-review-script-[dikw]\d\d$
🧩 SKILL    haipipe-insight
🤖 AGENT    haipipe-task-reviewer-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-insight review the script of {folder} against its agreed needs in a fresh context, as run-review-script-<l><nn>: it computes what each spec says and nothing else; return it with what is wrong, never fix it yourself.


## Gates

Each gate belongs to one level and one Run; the Run that passes it records it, and the scaffold refuses to go past
it (`haipipe-insight/scripts/insight_ladder.py`).

```text
gate                     level      Run that passes it          what must hold
a question agreed        Question   run-review-plan-<l><nn>     another agent agreed its needs (agreed: ✅)
a script reviewed        Question   run-review-script-<l><nn>   another agent passed it against the agreed needs
the cuts set             Release    run-set-cuts-p<N>           full and every cut named, each with why; a person signed
a release signed         Release    run-sign-release-p<N>       the three above for every new or changed question;
                                                                a person signed (signed: ✅ <YYMMDD>); frozen after
a data version frozen    Block      run-add-version-v<M>        in board.md versions:, SPACE-relative, never edited
a Job added              Block      run-add-j<NN>               a signed release × a frozen data version, a new pair,
                                                                one clock moved
power before contrast    Job        run-power-j<NN>, rNN_…      the cut can answer (MDE ≤ the smallest effect), else refused
the output gated         Task       rNN_<partition>             the tables equal the spec's outputs; no row-level table
a page checked           Task       run-check-t<NN>             another agent's CHECK closed after the Run's content
a Job closed             Job        run-close-j<NN>             every page checked, the comparison written; a person signed
a handoff signed         Block      run-draft-handoff           a person signed; Design reads only a signed handoff
```
