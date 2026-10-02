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
| board | Scope | Methods | Add a method | haipipe-insight-agent (new) | haipipe-workbench-insight | none |
| board | Scope | Methods | Add a paper | haipipe-discovery-orchestrator-agent | haipipe-discovery | none |
| board | Scope | Questions | Ask | haipipe-insight-agent (new) | haipipe-insight-question | the question |
| board | Scope | Questions | Carry a board over | haipipe-insight-agent (new) | haipipe-insight | none |
| board | Scope | Questions | Review the questions | haipipe-insight-reviewer-agent (new) | haipipe-insight-question | a change |
| board | Insight | Question | Plan the evidence | haipipe-insight-agent (new) | haipipe-insight-evidence-plan | none |
| board | Insight | Question | Review the evidence plan | haipipe-insight-reviewer-agent (new) | haipipe-insight-evidence-plan | none |
| board | Insight | Work | Write the question's script | haipipe-task-creator-agent | haipipe-insight | none |
| board | Insight | Work | Review the script | haipipe-task-reviewer-agent | haipipe-insight | none |
| board | Insight | Work | Run a partition | haipipe-task-orchestrator-agent | haipipe-insight | none |
| board | Insight | Data report | Write the Data report | haipipe-insight-agent (new) | haipipe-insight-data | none |
| board | Insight | Information report | Write the Information report | haipipe-insight-agent (new) | haipipe-insight-information | none |
| board | Insight | Knowledge report | Write the Knowledge report | haipipe-insight-agent (new) | haipipe-insight-knowledge | none |
| board | Insight | Report | Check alignment | haipipe-insight-reviewer-agent (new) | haipipe-insight-check | none |
| board | Insight | Cross | Pool or split | haipipe-insight-agent (new) | haipipe-insight-knowledge | none |
| board | Check | Gates | none | none | none | none |
| board | Check | Checks | Review an answer | haipipe-page-check-agent | haipipe-insight-check | none |
| board | Delivery | Counsel | Write the counsel | haipipe-insight-agent (new) | haipipe-insight-wisdom | none |
| board | Delivery | Handoff | Draft the handoff | haipipe-insight-agent (new) | haipipe-insight-wisdom | the handoff |

Notes
-----

- **The question rows.** "Carry a board over" moves a register board's
  questions into a Prototype word for word (`../../haipipe-insight/ref/carry_over.py`);
  "Review the questions" judges each by Q1-Q7 and proposes keep, split, merge or
  move, and a person signs any change (`haipipe-insight-question`).
- **The alignment rows.** "Plan the evidence" writes each question's evidence
  needs before any run, and "Review the evidence plan" has a different agent agree
  them; on a Prototype board the question owns its code, so "Write the question's
  script" writes `scripts/<name>.py` from its live needs, a different agent reviews
  it, and "Run a partition" runs `runs/<partition>.sh` into `results/` and a
  generated `reports/` (`../../haipipe-insight/ref/prototype-contract.md`). "Check
  alignment" and "Review an answer" run `haipipe-insight-check`; a cell's status is
  computed, never settled by hand. Contract:
  `../../haipipe-insight/ref/evidence-needs.md`.
- **Make and judge apart.** The agent that writes a report never runs its
  check; a cell turns ✅ only when a CHECK by another agent closed after its run.
- **Person signs.** Only what leaves the board or changes its meaning: the question
  a person asks, a change the question review proposes, a new cut, and the Wisdom
  handoff (`signed:`). The evidence plan, its release of new
  computation and each page's plan are decided by agents: one drafts, a different
  one agrees or closes.
- **The studio drawing.** Part 1 of
  `servers/workbench-insight/studio/insight-workbench-design.excalidraw` draws
  Spaces, views, run types and skills; it should be drawn from this table, not
  hand-kept beside it (planned: a drawer in `table-workbench`).
- **As served.** The Work column reads each page's `answers.yaml` and shows
  every need with its bound files; the Runs panel does not read this table yet.
  Part 1 of the studio drawing is drawn from this table.
