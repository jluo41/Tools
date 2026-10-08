# Design Run cards

What the design workbench shows in each level's Runs panel: one card per button, each with the skill, agent and sign
of its Run and the prompt the button copies. The cards follow the design ladder (`haipipe-design/ref/design-ladder.md`;
b12 s11 · s12 · s13 · s21, JL 261007): a Block, a Job, a Task. The Run types are in `run-profile.md`; the owning skills
keep their authority; `haipipe-design-workflow` routes the Runs and is no card's skill except Close.

A `🔘 BUTTON` line is `label · <Level> › <Space> · ticket pattern · views <names>`. Level is `Block`, `Job` or `Task`;
Space is one of the six (Description · Idea Studio · Audience Report · Work Details · Runs · Delivery). The pattern is
a regular expression on the Run's folder name, `run-<type>-<target>/`. `views` names the third-row views the button
shows in, lowercase-kebab (`predicted-vs-observed`); none = every view of the Space. `🧩 SKILL` names the one skill
that does the work, `🤖 AGENT` who does the Run (a verify or a rank is never the agent that generated), `✍️ SIGNS`
what the person signs on it, or `none`. `💬 PROMPT` is the text the button copies; `{folder}` is the Block, Job or
Task the frame shows, `<…>` the row picked. The base frame adds its own (Add a topic, Redraw a topic).

The cards of the older board (the Design Folder page) stay word for word at the end, under their own heading: that
page's workbench (`servers/workbench-design/design.py`) reads them, and their one-word Spaces (`Tasks`, `Theory`,
`Goal`, `Design`, `Delivery`) never match a ladder card's `<Level> › <Space>`.


## Block › Description · goals, methods, inputs, the Map

🔘 BUTTON   Add a goal · Block › Description · ^run-add-goal- · views goals
🧩 SKILL    haipipe-design-goal
🤖 AGENT    haipipe-designer-agent
✍️ SIGNS    the goal
💬 PROMPT   /haipipe-design-goal add a goal to {folder}/board.md ## Goals (id · aim · who · venue · n · its own rules · leave out), as run-add-goal-<goal>; show me the line before writing, and I sign it.

🔘 BUTTON   Set the shared rules · Block › Description · ^run-setup-rules · views goals
🧩 SKILL    haipipe-design-goal
🤖 AGENT    haipipe-designer-agent
✍️ SIGNS    the rules
💬 PROMPT   /haipipe-design-goal set the rules every goal of {folder} keeps in design-goal.md, each checkable on the text alone, as run-setup-rules; show me the changes first.

🔘 BUTTON   Add an inputs version · Block › Description · ^run-add-inputs- · views inputs
🧩 SKILL    haipipe-design-goal
🤖 AGENT    haipipe-designer-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-design-goal freeze a new inputs version of {folder}: inputs/iN/ (the rules, theory, the insight handoff copied in) and its manifest.yaml with each file's sha256, as run-add-inputs-i<N>; say what is new against the last version.

🔘 BUTTON   Launch a Job · Block › Description · ^run-add-job- · views map
🧩 SKILL    haipipe-design
🤖 AGENT    haipipe-designer-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-design launch a Job in {folder}: a signed goal × a registered method version × a frozen inputs version, jNN_<goal>_<method>/ with its pins, as run-add-job-j<NN>; tell me which one clock moved from the Job before it.

🔘 BUTTON   Propose a method change · Block › Description · ^run-propose-method- · views methods
🧩 SKILL    haipipe-design-method
🤖 AGENT    haipipe-designer-agent
✍️ SIGNS    the proposal
💬 PROMPT   /haipipe-design-method propose a change to a registered method from what {folder}'s Jobs and scores show, as run-propose-method-<slug>; the registry cuts the next version, never this Block.

## Block › Audience Report · questions, cost, predicted vs observed, the scorecard

🔘 BUTTON   Propose questions · Block › Audience Report · ^run-propose-questions · views questions
🧩 SKILL    haipipe-question
🤖 AGENT    haipipe-designer-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-question propose {folder}'s report questions from the Map, the scores and the scorecard into board.md ## Questions, as run-propose-questions; another agent agrees before they stand.

🔘 BUTTON   Write a report · Block › Audience Report · ^run-report- · views questions
🧩 SKILL    haipipe-report
🤖 AGENT    haipipe-page-writing-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-report write the report of one Block question in {folder}/reports/qNN_<topic>/ from the Jobs it names, as run-report-q<NN>; another agent checks it.

🔘 BUTTON   Add the Exp's data · Block › Audience Report · ^run-add-observed- · views predicted-vs-observed
🧩 SKILL    haipipe-design-method
🤖 AGENT    haipipe-designer-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-design-method add what an Exp returned to {folder}: observed/eNN_<exp>/arms.csv (arm · job · design · n · observed: the arm's outcome total), source.md and a frozen manifest, from a signed handoff or a per-arm report; per-arm totals only, never rows; as run-add-observed-e<NN>.

🔘 BUTTON   Score the predictions · Block › Audience Report · ^run-score- · views predicted-vs-observed method-scorecard
🧩 SKILL    haipipe-design-method
🤖 AGENT    haipipe-design-reviewer-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-design-method score every arm's design of one Exp in {folder} against its frozen prediction (direction · in range · error) into runs/run-score-e<NN>/scores.csv, as run-score-e<NN>.

## Block › Idea Studio

🔘 BUTTON   Draw a topic · Block › Idea Studio · ^run-draw-
🧩 SKILL    excalidraw-report
🤖 AGENT    haipipe-designer-agent
✍️ SIGNS    none
💬 PROMPT   /excalidraw-report draw a studio topic of {folder}: studio/sNN-<topic>/ with its builder, as run-draw-s<NN>; keep every mark a person made.

## Job › Description · goal, method, inputs

🔘 BUTTON   Set up the goal · Job › Description · ^run-setup-goal- · views goal
🧩 SKILL    haipipe-design-goal
🤖 AGENT    haipipe-designer-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-design-goal confirm {folder}'s face pins a signed goal of the Block's goal list and its n matches, as run-setup-goal-j<NN>; it writes nothing else (inputs/goal.md is run-setup-inputs').

🔘 BUTTON   Set up the method · Job › Description · ^run-setup-method- · views method
🧩 SKILL    haipipe-design-method
🤖 AGENT    haipipe-designer-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-design-method pin {folder}'s registered method version: copy it into inputs/method.md and write method-sha on the face, as run-setup-method-j<NN>.

🔘 BUTTON   Set up the inputs · Job › Description · ^run-setup-inputs- · views inputs
🧩 SKILL    haipipe-design-goal
🤖 AGENT    haipipe-designer-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-design-goal build {folder}'s fence: inputs/ with links into the pinned inputs version, chosen by the method's step ①, and manifest.yaml with each file's source and sha256 (first 12 hex), plus inputs/goal.md from the goal list, once inputs/method.md is pinned, as run-setup-inputs-j<NN>.

🔘 BUTTON   Close the Job · Job › Description · ^run-close- · views goal
🧩 SKILL    haipipe-design-workflow
🤖 AGENT    haipipe-designer-agent
✍️ SIGNS    the close
💬 PROMPT   /haipipe-design-workflow close {folder} once every design is released or dropped, as run-close-j<NN>; I sign the close.

## Job › Work Details and Runs · ideas, designs, the review of the whole

🔘 BUTTON   Reason ideas · Job › Work Details · ^run-reason- · views reason-ideas
🧩 SKILL    haipipe-design-unit
🤖 AGENT    haipipe-designer-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-design-unit reason ideas for {folder} in t00_reason-ideas/, from inputs/ only: ideas.yaml (each with a short name), chains.yaml (each step's from: a manifest file or own knowledge) and topics.md, as run-reason-t00.

🔘 BUTTON   Open the design Tasks · Job › Work Details · ^run-open-designs- · views reason-ideas
🧩 SKILL    haipipe-design
🤖 AGENT    haipipe-designer-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-design open one design Task per idea of {folder} (tNN_d<NN>_<name>/), then t99, as run-open-designs-j<NN>, only after its fence-check pass (passes/pNN-<MMDD>/fence-check.md, written by the reviewer agent) ends in pass.

🔘 BUTTON   Generate a design · Job › Work Details · ^run-generate- · views conduct-review
🧩 SKILL    haipipe-design-unit
🤖 AGENT    haipipe-designer-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-design-unit generate one design of {folder} from its idea, reading inputs/ only, with its elements.yaml, as run-generate-d<NN> in its Task; then project the draft (haipipe-design-workflow project_draft.py draft).

🔘 BUTTON   Verify a design · Job › Work Details · ^run-verify- · views conduct-review
🧩 SKILL    haipipe-design-unit
🤖 AGENT    haipipe-design-reviewer-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-design-unit verify one design draft of {folder} in a fresh context (T0 rules · T1 sources in the manifest · T2 critique when the method lists it), as run-verify-d<NN>-v<k>, k its draft; then project the verdict (project_draft.py verdict).

🔘 BUTTON   Revise a design · Job › Work Details · ^run-revise- · views conduct-review
🧩 SKILL    haipipe-design-unit
🤖 AGENT    haipipe-designer-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-design-unit revise a design of {folder} whose review failed, from its frozen feedback, as a new pass of run-revise-d<NN>; then project the draft and verify it.

🔘 BUTTON   Rank the designs · Job › Work Details · ^run-rank- · views review-whole
🧩 SKILL    haipipe-design-unit
🤖 AGENT    haipipe-design-reviewer-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-design-unit rank {folder}'s passed designs in t99_review-whole/ (rank · predicted · why · kept), keep the top N (T3 pretest on the kept when the method asks), as run-rank-t99; then project the predictions (haipipe-design-workflow project_predictions.py).

## Job › Audience Report and Delivery · predictions and the release

🔘 BUTTON   Freeze the predictions · Job › Audience Report · ^run-freeze-predictions- · views predicted-vs-observed performance
🧩 SKILL    haipipe-design-delivery
🤖 AGENT    haipipe-designer-agent
✍️ SIGNS    the predictions, with the release
💬 PROMPT   /haipipe-design-delivery freeze the kept designs' predictions of {folder} (frozen: <date>), as run-freeze-predictions-j<NN>; I sign them together with the release.

🔘 BUTTON   Release · Job › Delivery · ^run-release-
🧩 SKILL    haipipe-design-delivery
🤖 AGENT    haipipe-designer-agent
✍️ SIGNS    the release
💬 PROMPT   /haipipe-design-delivery release {folder}'s kept, passed designs: delivery/designs.json and designs.md, word for word, added to the Block's delivery/, as run-release-j<NN>; I sign the release.

## Task › Runs · a design Task's own buttons

🔘 BUTTON   Reason ideas · Task › Runs · ^run-reason-
🧩 SKILL    haipipe-design-unit
🤖 AGENT    haipipe-designer-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-design-unit reason ideas in {folder} (t00), from the Job's inputs/ only, as run-reason-t00.

🔘 BUTTON   Generate · Task › Runs · ^run-generate-
🧩 SKILL    haipipe-design-unit
🤖 AGENT    haipipe-designer-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-design-unit generate this design ({folder}) from its idea, with its elements.yaml, as run-generate-d<NN>.

🔘 BUTTON   Verify · Task › Runs · ^run-verify-
🧩 SKILL    haipipe-design-unit
🤖 AGENT    haipipe-design-reviewer-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-design-unit verify this design's latest draft ({folder}) in a fresh context, as run-verify-d<NN>-v<k>.

🔘 BUTTON   Revise · Task › Runs · ^run-revise-
🧩 SKILL    haipipe-design-unit
🤖 AGENT    haipipe-designer-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-design-unit revise this design ({folder}) from its frozen feedback, a new pass of run-revise-d<NN>.

🔘 BUTTON   Rank · Task › Runs · ^run-rank-
🧩 SKILL    haipipe-design-unit
🤖 AGENT    haipipe-design-reviewer-agent
✍️ SIGNS    none
💬 PROMPT   /haipipe-design-unit rank the Job's passed designs in {folder} (t99), keep the top N, as run-rank-t99.


## Older board (the Design Folder page)

The cards below are the older page's, unchanged: its header read as follows.

>
> What the Design workbench shows in each Space's Runs panel: one card per run
> type, each with the button a person sees, the agent that does the run, the skill
> it uses, and the prompt the button copies. It is the Workbench Table
> (`skills/2_theme/design/workbench-design/ref/workbench-table.md`) written as
> cards; the two must agree, and `table-workbench --check` checks the table.
>
> The format is the Paper workbench's (`skills/2_theme/paper/haipipe-paper-workflow/ref/run-cards.md`)
> plus one line:
>
> - `🔘 BUTTON   label · Space · ticket pattern · views <names>`. Space is one of
>   `Tasks`, `Theory` (board level) or `Goal`, `Design`, `Delivery` (page level).
>   The pattern is a regular expression on the run record's file name; `-` means the
>   button only copies a prompt. `views` names the views it shows in.
> - `🤖 AGENT    the agent that does the run.`
> - `🧩 SKILL    the one small skill the agent loads.`
> - `✍️ SIGNS    what the person signs on this run, or none.`
> - `💬 PROMPT   the text the button copies.` `{board}` is the board's `board.md`,
>   `{page}` the Design Folder's page, `{target}` the selected design.
>
> `haipipe-design-workflow` routes the Runs and enforces their gates; it is no
> card's skill. A `(new)` name is planned and not built yet.
>
>

## Board · Design Tasks

🔘 BUTTON   Add design tasks · Tasks · - · views task-list
🤖 AGENT    haipipe-designer-agent
🧩 SKILL    haipipe-design-brief
✍️ SIGNS    the task list
💬 PROMPT   /haipipe-design-brief add design tasks to {board}: one per subgroup (who receives it), with their job, the venue and how many designs, and open a Design Folder for each. Ask me for the subgroups first.

🔘 BUTTON   Set shared rules · Tasks · - · views shared-rules
🤖 AGENT    haipipe-designer-agent
🧩 SKILL    haipipe-design-brief
✍️ SIGNS    the rules
💬 PROMPT   /haipipe-design-brief {board}: list the rules every design task keeps, each checkable on the text alone, and show me the changes before writing.


## Board · Theory of Design

🔘 BUTTON   Add a paper · Theory · - · views papers
🤖 AGENT    haipipe-discovery-orchestrator-agent
🧩 SKILL    haipipe-discovery
✍️ SIGNS    the source check
💬 PROMPT   /haipipe-discovery add one paper behind this board's design methods as a Paper Run in the Project's Discovery, check its record (title, authors, year, journal, DOI), then add its row to the design workbench's servers/workbench-design/related/papers.md (group · role · key · paper · venue · doi · why here · pdf); when the Run saved a free copy under an open license (CC BY), copy it into related/papers/, name it in the row's pdf cell and list it in related/papers/README.md. Show me the row first.


## Page · Design Goal · the five blocks of the board's design-goal.md

🔘 BUTTON   Frame the aim · Goal · - · views aim
🤖 AGENT    haipipe-designer-agent
🧩 SKILL    haipipe-design-goal
✍️ SIGNS    the aim
💬 PROMPT   /haipipe-design-goal aim for {page}: fill the Aim lines of the design-goal.md beside {board} (value wanted, their moment, for whom, measured by, baseline), each with its source; ask me what no file says.

🔘 BUTTON   Pin the venue · Goal · - · views venue
🤖 AGENT    haipipe-designer-agent
🧩 SKILL    haipipe-design-goal
✍️ SIGNS    none
💬 PROMPT   /haipipe-design-goal venue for {page}: read the venue profile, then write only the Venue lines this board fixes or narrows in the design-goal.md beside {board}, each with its source.

🔘 BUTTON   Set the rules · Goal · - · views rules
🤖 AGENT    haipipe-designer-agent
🧩 SKILL    haipipe-design-goal
✍️ SIGNS    the rules
💬 PROMPT   /haipipe-design-goal rules for {page}: list each rule every design must keep, checkable on the text alone, in the design-goal.md beside {board}; keep the register's acceptance lines in step and show me the changes first.

🔘 BUTTON   Gather resources · Goal · - · views resources
🤖 AGENT    haipipe-designer-agent
🧩 SKILL    haipipe-design-goal
✍️ SIGNS    none
💬 PROMPT   /haipipe-design-goal resources for {page}: list what the designer may draw on (starting text, past designs and what became of them, theory, budget) in the design-goal.md beside {board}, each with its source.

🔘 BUTTON   Add a theory · Goal · - · views resources
🤖 AGENT    haipipe-discovery-orchestrator-agent
🧩 SKILL    haipipe-design-theory (new)
✍️ SIGNS    the source check
💬 PROMPT   /haipipe-design-theory {board}: add one theory a design here could rest on to the board's design-theory.md: what it says, the one variable it moves and a checked published source. Show me the row first.

🔘 BUTTON   Set what to leave out · Goal · - · views leave-out
🤖 AGENT    haipipe-designer-agent
🧩 SKILL    haipipe-design-goal
✍️ SIGNS    the rules
💬 PROMPT   /haipipe-design-goal leave out for {page}: list each thing that must never appear in the message, and why, in the design-goal.md beside {board}; show me the changes first.


## Page · Design

🔘 BUTTON   Map variables · Design · - · views variables
🤖 AGENT    haipipe-designer-agent
🧩 SKILL    haipipe-design-frame (new)
✍️ SIGNS    none
💬 PROMPT   /haipipe-design-frame variables for {page}: name the variables a design here can change and the options of each, against the baseline, before any draft.

🔘 BUTTON   Add a design · Design · - · views cards
🤖 AGENT    haipipe-designer-agent
🧩 SKILL    haipipe-design-frame (new)
✍️ SIGNS    none
💬 PROMPT   /haipipe-design-frame add a design to {page}: the one variable it changes, the rule it follows (because), what should happen and what would prove it wrong. Ask me what to design first.

🔘 BUTTON   Commission · Design · ^(?:rd\d+_|run-design-)commission[_-] · views cards
🤖 AGENT    haipipe-designer-agent
🧩 SKILL    haipipe-design-commission (new)
✍️ SIGNS    release or hold
💬 PROMPT   /haipipe-design-commission {target} in {page}: assemble and freeze its goal, rules and inputs, and show them to me; I record Release or Hold with the workbench's button.

🔘 BUTTON   Generate · Design · ^(?:rd\d+_|run-design-)generate[_-] · views cards
🤖 AGENT    haipipe-designer-agent
🧩 SKILL    haipipe-design-unit
✍️ SIGNS    none
💬 PROMPT   /haipipe-design-unit generate {target} in {page}: dispatch haipipe-designer-agent on its released Commission and return the receipt.

🔘 BUTTON   Verify · Design · ^(?:rd\d+_|run-design-)verify[_-] · views cards
🤖 AGENT    haipipe-design-reviewer-agent (new)
🧩 SKILL    haipipe-design-unit
✍️ SIGNS    none
💬 PROMPT   /haipipe-design-unit verify {target} in {page} with haipipe-design-reviewer-agent, in a context that never saw the draft made; record pass, fail or the open gaps.


## Page · Delivery

🔘 BUTTON   Passed review · Delivery · ^(?:rd\d+_|run-design-)verify[_-] · views designs
🤖 AGENT    haipipe-design-reviewer-agent (new)
🧩 SKILL    haipipe-design-unit
✍️ SIGNS    none
💬 PROMPT   /haipipe-design-unit {target} in {page}: show the design whose Verify passed, word for word, and say whether it is still current.

🔘 BUTTON   Plan the test · Delivery · - · views test-plan
🤖 AGENT    haipipe-designer-agent
🧩 SKILL    haipipe-design-testplan (new)
✍️ SIGNS    the test plan
💬 PROMPT   /haipipe-design-testplan {page}: plan one arm per variable with salience as the control, and say what the test will decide. Show me the plan first.
