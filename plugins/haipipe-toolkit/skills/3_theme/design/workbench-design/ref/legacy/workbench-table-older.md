Design Workbench Table (older board page)
======================

Shape and check: `skills/0_utils/table-workbench/SKILL.md`. Rows run input →
process → output; Folder is where the run writes (Board › and Page › are the
board and the Design page folders, Tools › the workbench's own `ref/`). `(new)` marks a skill or agent planned but not built yet.

Two design agents: `hai-designer-agent` makes, `hai-design-reviewer-agent`
judges and never sees its own work. `hai-design-workflow` routes Runs and
enforces the gates; it is no row's Skill.

| Level | Space | View | Run type | Agent | Skill | Person signs | Folder |
|---|---|---|---|---|---|---|---|
| board | Guide | Description | none | none | none | none | none |
| board | Guide | Method | Add a method | hai-designer-agent | workbench-design | none | Tools › servers/workbench-design/guide/methods/ |
| board | Guide | RoadMap Draw | none | none | none | none | none |
| board | Guide | Related Paper | Add a paper | hai-discovery-orchestrator-agent | hai-discovery | the source check | Tools › servers/workbench-design/related/papers.md |
| board | Design Tasks | Task list | Add design tasks | hai-designer-agent | hai-design-brief | the task list | Board › 0-BR-brief/ |
| board | Design Tasks | Shared rules | Set shared rules | hai-designer-agent | hai-design-brief | the rules | Board › 0-BR-brief/ |
| page | Design Task | Aim | Frame the aim | hai-designer-agent | hai-design-goal | the aim | Board › design-goal.md |
| page | Design Task | Requirements | Pin the venue | hai-designer-agent | hai-design-goal | none | Board › design-goal.md |
| page | Design Task | Requirements | Set the rules | hai-designer-agent | hai-design-goal | the rules | Board › design-goal.md |
| page | Design Task | Resources | Gather resources | hai-designer-agent | hai-design-goal | none | Board › design-goal.md |
| page | Design Task | Resources | Add a theory | hai-discovery-orchestrator-agent | hai-design-theory (new) | the source check | Board › design-theory.md |
| page | Design Task | Leave out | Set what to leave out | hai-designer-agent | hai-design-goal | the rules | Board › design-goal.md |
| page | Design Item | Variables | Map variables | hai-designer-agent | hai-design-frame (new) | none | Page › draft/<stem>-design-items.md |
| page | Design Item | Cards | Add a design | hai-designer-agent | hai-design-frame (new) | none | Page › draft/<stem>-design-items.md |
| page | Design Item | Cards | Commission | hai-designer-agent | hai-design-commission (new) | release or hold | Page › runs/ |
| page | Design Item | Cards | Generate | hai-designer-agent | hai-design-unit | none | Page › results/<run>/ |
| page | Design Item | Cards | Verify | hai-design-reviewer-agent (new) | hai-design-unit | none | Page › results/<run>/ |
| page | Delivery | Designs | Passed review | hai-design-reviewer-agent (new) | hai-design-unit | none | Page › results/<run>/ |
| page | Delivery | Test plan | Plan the test | hai-designer-agent | hai-design-testplan (new) | the test plan | Page › draft/ |

Notes
-----

- Commission: the agent assembles and freezes one design's goal, rules and
  inputs; only the named person releases or holds it, with the workbench's button.
- The four Design Task views (Aim · Requirements · Resources · Leave out) read the
  five blocks of the board's `design-goal.md` (Aim · Venue · Rules · Resources ·
  Leave out); Requirements holds Venue and Rules (`design.py`, `design_input`).
- The Requirements view shows the venue pack (`skills/3_theme/design/venue/venue-sms` for SMS);
  the skill pins it to the design task, it does not restate it.
- As served at 0.14.0 the Runs panel reads its run types from the cards,
  `skills/3_theme/design/hai-design-workflow/references/run-cards.md` (`design.py`,
  `design_run_types`). A `(new)` skill shows as such on its button. No Space has
  separate view tabs yet; a card's `views` names where it will go.
