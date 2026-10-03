Paper Workbench Table
=====================

Shape and check: `skills/0_utils/table-workbench/SKILL.md`. Rows run input →
process → output: the Guide, then Ideation, Story, Sections and Delivery, the
order the paper moves.

The Paper Workbench (`servers/workbench-paper/paper.py`) is one Board-level
screen, so every row is Level `board`. Each working row is one `🔘 BUTTON` of
`haipipe-paper-workflow/ref/run-cards.md`; its `🤖 AGENT`, `🧩 SKILL` and
`✍️ SIGNS` lines are the row's Agent, Skill and Person signs. The Guide rows have
no card: Guide's own Runs panel reads them from this table.

Makers and judges stay apart: every row that reviews or checks (Idea review,
Claim review, Task review, Narrative review, Page check, Check) is done by an
agent that makes nothing on this screen. `(new)` marks an agent or skill
planned but not built yet.

| Level | Space | View | Run type | Agent | Skill | Person signs |
|---|---|---|---|---|---|---|
| board | Guide | Description | none | none | none | none |
| board | Guide | Method | none | none | none | none |
| board | Guide | RoadMap Draw | Redraw the Workbench design | haipipe-studio-agent (new) | haipipe-workbench-paper | none |
| board | Guide | Related Paper | Add a paper | haipipe-discovery-orchestrator-agent | haipipe-discovery | the source check |
| board | Ideation | Ideas | Generate ideas | haipipe-ideation-agent (new) | haipipe-ideation-generate | none |
| board | Ideation | Ideas | Test idea | haipipe-ideation-agent (new) | haipipe-ideation-test | none |
| board | Ideation | Ideas | Idea review | haipipe-board-reviewer-agent | haipipe-paper-ideation | none |
| board | Ideation | Ideas | Select idea | haipipe-ideation-agent (new) | haipipe-ideation-select | the admitted idea (G0) |
| board | Story | Spine | Story revise | haipipe-page-writing-agent | haipipe-paper-story | the Story version |
| board | Story | RoadMap Draw | Redraw | haipipe-studio-agent (new) | haipipe-paper-story | none |
| board | Story | High-level logic + Low-level work | Task runs | haipipe-task-orchestrator-agent | haipipe-task | none |
| board | Story | High-level logic + Low-level work | Task review | haipipe-board-reviewer-agent | haipipe-paper-story | release of Task work (G1) |
| board | Story | High-level logic + Low-level work | Claim review | haipipe-board-reviewer-agent | haipipe-paper-story | the claim state (G2) |
| board | Story | Related Papers | Discovery runs | haipipe-discovery-orchestrator-agent | haipipe-discovery | none |
| board | Sections | Table | Draft runs | haipipe-page-writing-agent | haipipe-paper-section | none |
| board | Sections | Evidence | Evidence runs | haipipe-page-evidence-agent | haipipe-page-evidence | none |
| board | Sections | Narrative | Narrative review | haipipe-board-reviewer-agent | haipipe-paper-story | release of one Section (G3) |
| board | Sections | Table | Delivery runs | haipipe-page-writing-agent | haipipe-page-delivery | none |
| board | Sections | Table | Page check | haipipe-page-check-agent | haipipe-page-check | none |
| board | Delivery | Preview · Artifacts | Build | haipipe-paper-assemble-agent (new) | haipipe-paper-assemble | none |
| board | Delivery | Checks | Check | haipipe-page-check-agent | haipipe-paper-assemble | submission readiness (G4) |
| board | Delivery | Cover letter | Cover letter | haipipe-page-writing-agent | haipipe-paper-assemble | the letter |
| board | Delivery | Rounds | Response | haipipe-page-writing-agent | haipipe-paper-round | every response answered (G5) |

Notes
-----

- **One skill per row.** The cards for Story revise and Draft runs used to name
  two skills (`haipipe-paper-story · haipipe-writing`, `haipipe-paper-section ·
  haipipe-page-writing`); the row names the one that owns the work, and the
  writing skill is loaded by it.
- **Gates.** Person signs carries the gates G0–G5 of `haipipe-workbench-paper`:
  the screen shows them, the person closes them; no run closes a gate.
- **Section runs are the Section Page's.** Draft, Evidence, Delivery runs and
  Page check run on one Section Page through `haipipe-workbench-page`; this
  screen only lists them under the selected Section.
