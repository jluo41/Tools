Paper Workbench Table
=====================

Shape and check: `skills/0_utils/table-workbench/SKILL.md`. Rows run input →
process → output, level by level: the Guide, then the Board (Block), then a
version (Job), each in the order of its Spaces (b16 Q05, JL 261007); Related is the Block's alone.

The paper workbench (`servers/workbench-paper/paper_theme.py`) draws the shared
frame's levels Guide · Block · Job · Task. Each working row is one `🔘 BUTTON`
of `hai-paper-workflow/ref/run-cards.md`, whose Space field is
`<Level> › <Space>`; its `🤖 AGENT`, `🧩 SKILL` and `✍️ SIGNS` lines are the row's
Agent, Skill and Person signs. View is the third-row view the button shows in
(All = every view of the Space). The Guide rows have no card: Guide's own Runs
panel reads them from this table. A Section (the Task level) is a Page Task:
its rows are the Page Workbench Table's (`workbench-task-draft/ref/workbench-table.md`).

Makers and judges stay apart: every row that reviews or checks (Idea review,
Claim review, Task review, Narrative review, Review for an audience, Review the
report, Check the rules, Check the letter, Page check, Check) is done by an
agent that makes nothing at its level. `(new)` marks an agent or skill planned
but not built yet.

| Level | Space | View | Run type | Agent | Skill | Person signs |
|---|---|---|---|---|---|---|
| block | Guide | Description | none | none | none | none |
| block | Guide | Method | Add a method | hai-draft-writing-agent | workbench-paper | none |
| block | Guide | RoadMap Draw | Redraw the Workbench design | hai-studio-agent (new) | workbench-paper | none |
| block | Guide | Related Paper | Add a paper | hai-discovery-orchestrator-agent | hai-discovery | the source check |
| block | Description | scope | Update the Board | hai-draft-writing-agent | hai-paper | none |
| block | Description | scope · venue | Add a venue | hai-draft-writing-agent | hai-paper-venue | none |
| block | Description | venue | Check the rules | hai-draft-check-agent | hai-paper-venue | none |
| block | Description | resources | Add a resource | hai-draft-writing-agent | hai-paper | none |
| block | Related | All | Add a related item | hai-draft-writing-agent | hai-paper | none |
| block | Related | All | Read a paper | hai-discovery-orchestrator-agent | hai-discovery | the source check |
| block | Idea Studio | All | Redraw | hai-studio-agent (new) | hai-studio | none |
| block | Idea Studio | All | Redraw the paper map | hai-studio-agent (new) | hai-draw draft | none |
| block | Audience Report | ideation · related-questions | Ask a Question | hai-draft-writing-agent | hai-report | none |
| block | Audience Report | ideation | Generate ideas | hai-ideation-agent (new) | hai-ideation generate | none |
| block | Audience Report | ideation | Test idea | hai-ideation-agent (new) | hai-ideation test | none |
| block | Audience Report | ideation | Idea review | hai-block-reviewer-agent | hai-paper-ideation | none |
| block | Audience Report | ideation | Select idea | hai-ideation-agent (new) | hai-ideation select | the admitted idea (G0) |
| block | Audience Report | narrative | Story revise | hai-draft-writing-agent | hai-paper-story | the Story version |
| block | Audience Report | narrative | Narrative review | hai-block-reviewer-agent | hai-paper-story | release of one Section (G3) |
| block | Audience Report | narrative | Review for an audience | hai-block-reviewer-agent | hai-paper-story | none |
| block | Audience Report | logic-work | Claim review | hai-block-reviewer-agent | hai-paper-story | the claim state (G2) |
| block | Audience Report | logic-work | Task review | hai-block-reviewer-agent | hai-paper-story | release of Task work (G1) |
| block | Audience Report | logic-work · related-questions | Write the report | hai-draft-writing-agent | hai-report | none |
| block | Audience Report | logic-work · related-questions | Review the report | hai-draft-check-agent | hai-report | the answer (G2) |
| block | Audience Report | logic-work · related-questions | Rebuild report drawing | hai-draft-writing-agent | hai-report | none |
| block | Audience Report | logic-work | Task runs | hai-task-orchestrator-agent | hai-task | none |
| block | Audience Report | logic-work | Discovery runs | hai-discovery-orchestrator-agent | hai-discovery | none |
| block | Work Details | All | Open a version | hai-draft-writing-agent | hai-paper | none |
| block | Runs | All | Update the Board status | hai-draft-writing-agent | hai-paper | none |
| job | Description | version | Update the version | hai-draft-writing-agent | hai-paper | none |
| job | Description | venue-rules | Check the rules | hai-draft-check-agent | hai-paper-venue | none |
| job | Audience Report | questions | Ask a Question | hai-draft-writing-agent | hai-report | none |
| job | Audience Report | questions | Write the report | hai-draft-writing-agent | hai-report | none |
| job | Audience Report | questions | Review the report | hai-draft-check-agent | hai-report | the answer (G2) |
| job | Audience Report | questions | Rebuild report drawing | hai-draft-writing-agent | hai-report | none |
| job | Audience Report | draft-main · draft-appendix | Narrative review | hai-block-reviewer-agent | hai-paper-story | release of one Section (G3) |
| job | Audience Report | draft-main · draft-appendix | Release a Section | hai-draft-writing-agent | hai-paper-story | release of one Section (G3) |
| job | Audience Report | comments | Add comments | hai-draft-writing-agent | hai-paper-comments | none |
| job | Audience Report | comments | Route an item | hai-draft-writing-agent | hai-paper-comments | none |
| job | Audience Report | comments | Reply to an item | hai-draft-writing-agent | hai-paper-comments | none |
| job | Audience Report | cover-letter | Write the cover letter | hai-draft-writing-agent | hai-paper-assemble | the letter |
| job | Audience Report | cover-letter | Check the letter | hai-draft-check-agent | hai-paper-assemble | none |
| job | Work Details | main · appendix | Add a Section | hai-draft-writing-agent | hai-paper-draft | none |
| job | Work Details | main · appendix | Draft runs | hai-draft-writing-agent | hai-paper-draft | none |
| job | Work Details | main · appendix | Evidence runs | hai-draft-evidence-agent | hai-evidence | none |
| job | Work Details | main · appendix | Delivery runs | hai-draft-writing-agent | hai-delivery | none |
| job | Work Details | main · appendix | Page check | hai-draft-check-agent | hai-draft-review | none |
| job | Work Details | letters | Add a letter | hai-draft-writing-agent | hai-paper-draft | none |
| job | Work Details | letters | Cover letter | hai-draft-writing-agent | hai-paper-assemble | the letter |
| job | Work Details | letters | Response | hai-draft-writing-agent | hai-paper-comments | every response answered (G5) |
| job | Runs | All | Update the version | hai-draft-writing-agent | hai-paper | none |
| job | Delivery | All | Build | hai-paper-assemble-agent (new) | hai-paper-assemble | none |
| job | Delivery | All | Check | hai-draft-check-agent | hai-paper-assemble | submission readiness (G4) |
| job | Delivery | All | Send | hai-paper-assemble-agent (new) | hai-paper-assemble | the send |

Notes
-----

- **One skill per row.** The cards for Story revise and Draft runs used to name
  two skills (`hai-paper-story · hai-draft`, `hai-paper-draft ·
  hai-draft-writing`); the row names the one that owns the work, and the
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
