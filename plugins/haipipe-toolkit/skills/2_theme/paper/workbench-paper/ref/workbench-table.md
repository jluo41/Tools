Paper Workbench Table
=====================

Shape and check: `skills/0_utils/table-workbench/SKILL.md`. Rows run input →
process → output, level by level: the Guide, then the Board (Block), then a
version (Job), each in the order of its six Spaces (b16 Q05, JL 261007).

The paper workbench (`servers/workbench-paper/paper_theme.py`) draws the shared
frame's levels Guide · Block · Job · Task. Each working row is one `🔘 BUTTON`
of `haipipe-paper-workflow/ref/run-cards.md`, whose Space field is
`<Level> › <Space>`; its `🤖 AGENT`, `🧩 SKILL` and `✍️ SIGNS` lines are the row's
Agent, Skill and Person signs. View is the third-row view the button shows in
(All = every view of the Space). The Guide rows have no card: Guide's own Runs
panel reads them from this table. A Section (the Task level) is a Page Task:
its rows are the Page Workbench Table's (`workbench-page/ref/workbench-table.md`).

Makers and judges stay apart: every row that reviews or checks (Idea review,
Claim review, Task review, Narrative review, Review for an audience, Review the
report, Check the rules, Check the letter, Page check, Check) is done by an
agent that makes nothing at its level. `(new)` marks an agent or skill planned
but not built yet.

| Level | Space | View | Run type | Agent | Skill | Person signs |
|---|---|---|---|---|---|---|
| block | Guide | Description | none | none | none | none |
| block | Guide | Method | Add a method | haipipe-page-writing-agent | workbench-paper | none |
| block | Guide | RoadMap Draw | Redraw the Workbench design | haipipe-studio-agent (new) | workbench-paper | none |
| block | Guide | Related Paper | Add a paper | haipipe-discovery-orchestrator-agent | haipipe-discovery | the source check |
| block | Description | scope | Update the Board | haipipe-page-writing-agent | haipipe-paper | none |
| block | Description | scope · venue | Add a venue | haipipe-page-writing-agent | haipipe-paper-venue | none |
| block | Description | venue | Check the rules | haipipe-page-check-agent | haipipe-paper-venue | none |
| block | Description | resources | Add a resource | haipipe-page-writing-agent | haipipe-paper | none |
| block | Description | related | Add a related item | haipipe-page-writing-agent | haipipe-paper | none |
| block | Description | related | Read a paper | haipipe-discovery-orchestrator-agent | haipipe-discovery | the source check |
| block | Idea Studio | All | Redraw | haipipe-studio-agent (new) | haipipe-studio | none |
| block | Audience Report | ideation · related-questions | Ask a Question | haipipe-page-writing-agent | haipipe-question | none |
| block | Audience Report | ideation | Generate ideas | haipipe-ideation-agent (new) | haipipe-ideation-generate | none |
| block | Audience Report | ideation | Test idea | haipipe-ideation-agent (new) | haipipe-ideation-test | none |
| block | Audience Report | ideation | Idea review | haipipe-board-reviewer-agent | haipipe-paper-ideation | none |
| block | Audience Report | ideation | Select idea | haipipe-ideation-agent (new) | haipipe-ideation-select | the admitted idea (G0) |
| block | Audience Report | narrative | Story revise | haipipe-page-writing-agent | haipipe-paper-story | the Story version |
| block | Audience Report | narrative | Narrative review | haipipe-board-reviewer-agent | haipipe-paper-story | release of one Section (G3) |
| block | Audience Report | narrative | Review for an audience | haipipe-board-reviewer-agent | haipipe-paper-story | none |
| block | Audience Report | logic-work | Claim review | haipipe-board-reviewer-agent | haipipe-paper-story | the claim state (G2) |
| block | Audience Report | logic-work | Task review | haipipe-board-reviewer-agent | haipipe-paper-story | release of Task work (G1) |
| block | Audience Report | logic-work · related-questions | Write the report | haipipe-page-writing-agent | haipipe-report | none |
| block | Audience Report | logic-work · related-questions | Review the report | haipipe-page-check-agent | haipipe-report | the answer (G2) |
| block | Audience Report | logic-work · related-questions | Rebuild report drawing | haipipe-page-writing-agent | haipipe-report | none |
| block | Audience Report | logic-work | Task runs | haipipe-task-orchestrator-agent | haipipe-task | none |
| block | Audience Report | logic-work | Discovery runs | haipipe-discovery-orchestrator-agent | haipipe-discovery | none |
| block | Work Details | All | Open a version | haipipe-page-writing-agent | haipipe-paper | none |
| block | Runs | All | Update the Board status | haipipe-page-writing-agent | haipipe-paper | none |
| job | Description | version | Update the version | haipipe-page-writing-agent | haipipe-paper | none |
| job | Description | venue-rules | Check the rules | haipipe-page-check-agent | haipipe-paper-venue | none |
| job | Idea Studio | All | Redraw the paper map | haipipe-studio-agent (new) | excalidraw-section | none |
| job | Audience Report | questions | Ask a Question | haipipe-page-writing-agent | haipipe-question | none |
| job | Audience Report | questions | Write the report | haipipe-page-writing-agent | haipipe-report | none |
| job | Audience Report | questions | Review the report | haipipe-page-check-agent | haipipe-report | the answer (G2) |
| job | Audience Report | questions | Rebuild report drawing | haipipe-page-writing-agent | haipipe-report | none |
| job | Audience Report | draft-main · draft-appendix | Narrative review | haipipe-board-reviewer-agent | haipipe-paper-story | release of one Section (G3) |
| job | Audience Report | draft-main · draft-appendix | Release a Section | haipipe-page-writing-agent | haipipe-paper-story | release of one Section (G3) |
| job | Audience Report | comments | Add comments | haipipe-page-writing-agent | haipipe-paper-comments | none |
| job | Audience Report | comments | Route an item | haipipe-page-writing-agent | haipipe-paper-comments | none |
| job | Audience Report | comments | Reply to an item | haipipe-page-writing-agent | haipipe-paper-comments | none |
| job | Audience Report | cover-letter | Write the cover letter | haipipe-page-writing-agent | haipipe-paper-assemble | the letter |
| job | Audience Report | cover-letter | Check the letter | haipipe-page-check-agent | haipipe-paper-assemble | none |
| job | Work Details | main · appendix | Add a Section | haipipe-page-writing-agent | haipipe-paper-section | none |
| job | Work Details | main · appendix | Draft runs | haipipe-page-writing-agent | haipipe-paper-section | none |
| job | Work Details | main · appendix | Evidence runs | haipipe-page-evidence-agent | haipipe-page-evidence | none |
| job | Work Details | main · appendix | Delivery runs | haipipe-page-writing-agent | haipipe-page-delivery | none |
| job | Work Details | main · appendix | Page check | haipipe-page-check-agent | haipipe-page-check | none |
| job | Work Details | letters | Add a letter | haipipe-page-writing-agent | haipipe-paper-section | none |
| job | Work Details | letters | Cover letter | haipipe-page-writing-agent | haipipe-paper-assemble | the letter |
| job | Work Details | letters | Response | haipipe-page-writing-agent | haipipe-paper-comments | every response answered (G5) |
| job | Runs | All | Update the version | haipipe-page-writing-agent | haipipe-paper | none |
| job | Delivery | All | Build | haipipe-paper-assemble-agent (new) | haipipe-paper-assemble | none |
| job | Delivery | All | Check | haipipe-page-check-agent | haipipe-paper-assemble | submission readiness (G4) |
| job | Delivery | All | Send | haipipe-paper-assemble-agent (new) | haipipe-paper-assemble | the send |

Notes
-----

- **One skill per row.** The cards for Story revise and Draft runs used to name
  two skills (`haipipe-paper-story · haipipe-writing`, `haipipe-paper-section ·
  haipipe-page-writing`); the row names the one that owns the work, and the
  writing skill is loaded by it.
- **Gates.** Person signs carries the gates G0–G5 of `workbench-paper`:
  the screen shows them, the person closes them; no run closes a gate.
- **Section runs are the Section Task's.** Draft, Evidence, Delivery runs and
  Page check run on one Section through its Task tab (the Page workflow); a
  version lists them in Work Details › Main and Appendix.
- **One label, one card per Space.** Ask a Question, Write the report, Review the
  report, Narrative review, Check the rules and Update the version show at two
  levels or Spaces; each row is its own card with the same agent, skill and sign.
- **Add a method.** Guide › Method's run writes one card in
  `servers/workbench-paper/guide/methods/<family>/`, adds its row to `guide/method.md`, and its
  papers to `related/papers.md` (checked `--online` first). The methods canvas,
  `guide/methods.excalidraw`, is then edited on
  the canvas: it is the source, and `method-canvas.py --force` redraws it only when the
  person asks.
