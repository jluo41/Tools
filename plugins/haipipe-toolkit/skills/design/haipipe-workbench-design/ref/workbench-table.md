Design Workbench Table
======================

Shape and check: `skills/0_utils/table-workbench/SKILL.md`. Rows run input →
process → output. `(new)` marks a skill or agent planned but not built yet.

Two design agents: `haipipe-designer-agent` makes, `haipipe-design-reviewer-agent`
judges and never sees its own work. `haipipe-design-workflow` routes Runs and
enforces the gates; it is no row's Skill.

| Level | Space | View | Run type | Agent | Skill | Person signs |
|---|---|---|---|---|---|---|
| board | Design Tasks | Task list | Add design tasks | haipipe-designer-agent | haipipe-design-brief | the task list |
| board | Design Tasks | Shared rules | Set shared rules | haipipe-designer-agent | haipipe-design-brief | the rules |
| board | Theory of Design | Design theory | none | none | none | none |
| board | Theory of Design | Domain | Add a theory | haipipe-discovery-orchestrator-agent | haipipe-design-theory (new) | the source check |
| page | Design Goal | Aim | Frame the aim | haipipe-designer-agent | haipipe-design-goal | the aim |
| page | Design Goal | Venue | Pin the venue | haipipe-designer-agent | haipipe-design-goal | none |
| page | Design Goal | Rules | Set the rules | haipipe-designer-agent | haipipe-design-goal | the rules |
| page | Design Goal | Resources | Gather resources | haipipe-designer-agent | haipipe-design-goal | none |
| page | Design Goal | Leave out | Set what to leave out | haipipe-designer-agent | haipipe-design-goal | the rules |
| page | Design | Variables | Map variables | haipipe-designer-agent | haipipe-design-frame (new) | none |
| page | Design | Cards | Add a design | haipipe-designer-agent | haipipe-design-frame (new) | none |
| page | Design | Cards | Commission | haipipe-designer-agent | haipipe-design-commission (new) | release or hold |
| page | Design | Cards | Generate | haipipe-designer-agent | haipipe-design-unit | none |
| page | Design | Cards | Verify | haipipe-design-reviewer-agent (new) | haipipe-design-unit | none |
| page | Delivery | Designs | Passed review | haipipe-design-reviewer-agent (new) | haipipe-design-unit | none |
| page | Delivery | Test plan | Plan the test | haipipe-designer-agent | haipipe-design-testplan (new) | the test plan |

Notes
-----

- Commission: the agent assembles and freezes one design's goal, rules and
  inputs; only the named person releases or holds it, with the workbench's button.
- The five Design Goal views are the five blocks of the board's `design-goal.md`
  (Aim · Venue · Rules · Resources · Leave out), which the served Design Goal
  Space already reads (`design.py`, `design_input`).
- The Venue view shows the venue pack (`skills/design/venue/venue-sms` for SMS);
  the skill pins it to the design task, it does not restate it.
- As served at 0.14.0 the Runs panel reads its run types from the cards,
  `skills/design/haipipe-design-workflow/references/run-cards.md` (`design.py`,
  `design_run_types`). A `(new)` skill shows as such on its button. No Space has
  separate view tabs yet; a card's `views` names where it will go.
