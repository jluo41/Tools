Design Workbench Table
======================

Shape and check: `skills/0_utils/table-workbench/SKILL.md`. Rows run input →
process → output; Folder is where the run writes (Board › and Page › are the
board and the Design page folders, Tools › the workbench's own `ref/`). `(new)` marks a skill or agent planned but not built yet.

Two design agents: `haipipe-designer-agent` makes, `haipipe-design-reviewer-agent`
judges and never sees its own work. `haipipe-design-workflow` routes Runs and
enforces the gates; it is no row's Skill.

| Level | Space | View | Run type | Agent | Skill | Person signs | Folder |
|---|---|---|---|---|---|---|---|
| board | Guide | Description | none | none | none | none | none |
| board | Guide | Method | Add a method | haipipe-designer-agent | haipipe-workbench-design | none | Tools › haipipe-workbench-design/ref/methods/ |
| board | Guide | RoadMap Draw | none | none | none | none | none |
| board | Guide | Related Paper | Add a paper | haipipe-discovery-orchestrator-agent | haipipe-discovery | the source check | Tools › haipipe-workbench-design/ref/design-papers.md |
| board | Design Tasks | Task list | Add design tasks | haipipe-designer-agent | haipipe-design-brief | the task list | Board › 0-BR-brief/ |
| board | Design Tasks | Shared rules | Set shared rules | haipipe-designer-agent | haipipe-design-brief | the rules | Board › 0-BR-brief/ |
| page | Design Task | Aim | Frame the aim | haipipe-designer-agent | haipipe-design-goal | the aim | Board › design-goal.md |
| page | Design Task | Requirements | Pin the venue | haipipe-designer-agent | haipipe-design-goal | none | Board › design-goal.md |
| page | Design Task | Requirements | Set the rules | haipipe-designer-agent | haipipe-design-goal | the rules | Board › design-goal.md |
| page | Design Task | Resources | Gather resources | haipipe-designer-agent | haipipe-design-goal | none | Board › design-goal.md |
| page | Design Task | Resources | Add a theory | haipipe-discovery-orchestrator-agent | haipipe-design-theory (new) | the source check | Board › design-theory.md |
| page | Design Task | Leave out | Set what to leave out | haipipe-designer-agent | haipipe-design-goal | the rules | Board › design-goal.md |
| page | Design Item | Variables | Map variables | haipipe-designer-agent | haipipe-design-frame (new) | none | Page › draft/<stem>-design-items.md |
| page | Design Item | Cards | Add a design | haipipe-designer-agent | haipipe-design-frame (new) | none | Page › draft/<stem>-design-items.md |
| page | Design Item | Cards | Commission | haipipe-designer-agent | haipipe-design-commission (new) | release or hold | Page › runs/ |
| page | Design Item | Cards | Generate | haipipe-designer-agent | haipipe-design-unit | none | Page › results/<run>/ |
| page | Design Item | Cards | Verify | haipipe-design-reviewer-agent (new) | haipipe-design-unit | none | Page › results/<run>/ |
| page | Delivery | Designs | Passed review | haipipe-design-reviewer-agent (new) | haipipe-design-unit | none | Page › results/<run>/ |
| page | Delivery | Test plan | Plan the test | haipipe-designer-agent | haipipe-design-testplan (new) | the test plan | Page › draft/ |

Notes
-----

- Commission: the agent assembles and freezes one design's goal, rules and
  inputs; only the named person releases or holds it, with the workbench's button.
- The four Design Task views (Aim · Requirements · Resources · Leave out) read the
  five blocks of the board's `design-goal.md` (Aim · Venue · Rules · Resources ·
  Leave out); Requirements holds Venue and Rules (`design.py`, `design_input`).
- The Requirements view shows the venue pack (`skills/design/venue/venue-sms` for SMS);
  the skill pins it to the design task, it does not restate it.
- As served at 0.14.0 the Runs panel reads its run types from the cards,
  `skills/design/haipipe-design-workflow/references/run-cards.md` (`design.py`,
  `design_run_types`). A `(new)` skill shows as such on its button. No Space has
  separate view tabs yet; a card's `views` names where it will go.
