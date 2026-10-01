Insight Workbench Table
=======================

Shape and check: `skills/0_utils/table-workbench/SKILL.md`. Rows run input →
process → output. `(new)` marks a skill or agent planned but not built yet.

Two Insight agents: `haipipe-insight-agent` makes (plans, writes reports and
counsel), `haipipe-insight-reviewer-agent` judges and never checks its own
page. Runs come from `haipipe-task`'s orchestrator. `haipipe-insight-workflow`
routes Runs and evaluates the GI gates; it is no row's Skill.

| Level | Space | View | Run type | Agent | Skill | Person signs |
|---|---|---|---|---|---|---|
| board | Scope | Dataset | Record the extract | haipipe-insight-agent (new) | haipipe-insight-meta | none |
| board | Scope | Partitions | Register a cut | haipipe-insight-agent (new) | haipipe-insight-partition (new) | the cut |
| board | Scope | Questions | Ask | haipipe-insight-agent (new) | haipipe-insight-question | the question |
| board | Insight | Question | Plan the evidence | haipipe-insight-agent (new) | haipipe-insight-evidence-plan | the evidence needs |
| board | Insight | Work | Bind the work | haipipe-task-orchestrator-agent | haipipe-insight-bind | release new computation |
| board | Insight | Work | Run a ticket | haipipe-task-orchestrator-agent | haipipe-task | none |
| board | Insight | Data report | Write the Data report | haipipe-insight-agent (new) | haipipe-insight-data | none |
| board | Insight | Information report | Write the Information report | haipipe-insight-agent (new) | haipipe-insight-information | none |
| board | Insight | Knowledge report | Write the Knowledge report | haipipe-insight-agent (new) | haipipe-insight-knowledge | none |
| board | Insight | Report | Check alignment | haipipe-insight-reviewer-agent (new) | haipipe-insight-check | none |
| board | Insight | Cross | Pool or split | haipipe-insight-agent (new) | haipipe-insight-knowledge | none |
| board | Check | Gates | none | none | none | none |
| board | Check | Checks | Review an answer | haipipe-page-check-agent | haipipe-insight-check | none |
| board | Check | Checks | Settle the cell | haipipe-insight-agent (new) | haipipe-insight-question | none |
| board | Delivery | Counsel | Write the counsel | haipipe-insight-agent (new) | haipipe-insight-wisdom | none |
| board | Delivery | Handoff | Draft the handoff | haipipe-insight-agent (new) | haipipe-insight-wisdom | the handoff |

Notes
-----

- **The alignment rows.** "Plan the evidence" writes each question's evidence
  needs before any run, and a person agrees them; "Bind the work" ties each
  need to the narrowest result files in the page's `answers.yaml`; "Check
  alignment" and "Review an answer" run `haipipe-insight-check`, which fails a
  ✅ cell whose needs are not bound, fit, cited and current. Contract:
  `../../haipipe-insight/ref/evidence-needs.md`.
- **Make and judge apart.** The agent that writes a report never runs its
  check; "Settle the cell" waits for a check with no overclaim.
- **Person signs.** The question, its evidence needs, a new cut, any new
  computation (the release), and the Wisdom handoff (`signed:`). Settling a
  cell is a register action on a passing check, not a signature.
- **The studio drawing.** Part 1 of
  `servers/workbench-insight/studio/insight-workbench-design.excalidraw` draws
  Spaces, views, run types and skills; it should be drawn from this table, not
  hand-kept beside it (planned: a drawer in `table-workbench`).
- **As served.** The Runs panel does not read this table yet; the Work column
  reads page tickets. Reading `answers.yaml` to show each need with its files
  is the next server change.
