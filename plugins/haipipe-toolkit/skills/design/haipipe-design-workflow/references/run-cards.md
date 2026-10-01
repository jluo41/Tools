# Design Run cards

What the Design workbench shows in each Space's Runs panel: one card per run
type, each with the button a person sees, the agent that does the run, the skill
it uses, and the prompt the button copies. It is the Workbench Table
(`skills/design/haipipe-workbench-design/ref/workbench-table.md`) written as
cards; the two must agree, and `table-workbench --check` checks the table.

The format is the Paper workbench's (`skills/paper/haipipe-paper-workflow/ref/run-cards.md`)
plus one line:

- `🔘 BUTTON   label · Space · ticket pattern · views <names>`. Space is one of
  `Tasks`, `Theory` (board level) or `Goal`, `Design`, `Delivery` (page level).
  The pattern is a regular expression on the run record's file name; `-` means the
  button only copies a prompt. `views` names the views it shows in.
- `🤖 AGENT    the agent that does the run.`
- `🧩 SKILL    the one small skill the agent loads.`
- `✍️ SIGNS    what the person signs on this run, or none.`
- `💬 PROMPT   the text the button copies.` `{board}` is the board's `board.md`,
  `{page}` the Design Folder's page, `{target}` the selected design.

`haipipe-design-workflow` routes the Runs and enforces their gates; it is no
card's skill. A `(new)` name is planned and not built yet.


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

🔘 BUTTON   Add a theory · Theory · - · views domain
🤖 AGENT    haipipe-discovery-orchestrator-agent
🧩 SKILL    haipipe-design-theory (new)
✍️ SIGNS    the source check
💬 PROMPT   /haipipe-design-theory {board}: add one theory a design here could rest on to the board's design-theory.md: what it says, the one variable it moves and a checked published source. Show me the row first.


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
