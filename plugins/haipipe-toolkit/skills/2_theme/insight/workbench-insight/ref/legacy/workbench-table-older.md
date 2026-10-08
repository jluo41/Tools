Insight Workbench Table
=======================

Shape and check: `skills/0_utils/table-workbench/SKILL.md`. Rows run input →
process → output. `(new)` marks a skill or agent planned but not built yet.

Two Insight agents: `haipipe-insight-agent` makes (plans, writes reports and
counsel), `haipipe-insight-reviewer-agent` judges and never checks its own
page. Runs come from `haipipe-task`'s orchestrator. `haipipe-insight-workflow`
routes Runs and evaluates the GI gates; it is no row's Skill.

| Level | Space | View | Run type | Agent | Skill | Person signs | Folder |
|---|---|---|---|---|---|---|---|
| board | Guide | Description | none | none | none | none | none |
| board | Guide | Method | Add a method | haipipe-insight-agent | workbench-insight | none | Tools › servers/workbench-insight/guide/methods/ |
| board | Guide | RoadMap Draw | none | none | none | none | none |
| board | Guide | Related Paper | Add a paper | haipipe-discovery-orchestrator-agent | haipipe-discovery | none | Tools › servers/workbench-insight/related/papers.md |
| board | Scope | Dataset | Record the extract | haipipe-insight-agent | haipipe-insight-meta | none | Prototype › 0-Meta/meta.md |
| board | Scope | Partitions | none | none | none | none | none |
| board | Scope | Questions | Ask | haipipe-insight-agent | haipipe-insight-question | the question | Prototype › <q>/<L><NN>-<name>.md |
| board | Prototype | Meta | Carry a board over | haipipe-insight-agent | haipipe-insight | none | Prototype › board.md · 0-Meta/ · <level>/level.md · <q>/ |
| board | Prototype | Meta | Register a cut | haipipe-insight-agent | haipipe-insight-partition (new) | the cut | Prototype › 0-Meta/partitions.md |
| board | Prototype | Data · Information · Knowledge · Wisdom | Review the questions | haipipe-insight-reviewer-agent | haipipe-question-review | a change | Prototype › <q>/<L><NN>-<name>.md (a signed change) |
| board | Prototype | Data · Information · Knowledge · Wisdom | Plan the evidence | haipipe-insight-agent | haipipe-insight-evidence-plan | none | Prototype › <q>/<L><NN>-<name>.md (needs) |
| board | Prototype | Data · Information · Knowledge · Wisdom | Review the evidence plan | haipipe-insight-reviewer-agent | haipipe-insight-evidence-plan | none | Prototype › <q>/<L><NN>-<name>.md (agreed:) |
| board | Prototype | Data · Information · Knowledge · Wisdom | Write the script | haipipe-task-creator-agent | haipipe-insight | none | Prototype › <q>/scripts/ |
| board | Prototype | Data · Information · Knowledge · Wisdom | Review the script | haipipe-task-reviewer-agent | haipipe-insight | none | none |
| board | Prototype | RoadMap Draw | Draw the question map | haipipe-insight-agent | haipipe-insight | none | Prototype › studio/question-map.excalidraw (generated) |
| board | Insight | each partition | Run a partition | haipipe-task-orchestrator-agent | haipipe-insight | none | Instance › <q>/results/<partition>/ · reports/<partition>/ |
| board | Insight | each partition | Write the Data report | haipipe-insight-agent | haipipe-insight-data | none | Instance › <q>/<L><NN>-<name>.md · draft/ |
| board | Insight | each partition | Write the Information report | haipipe-insight-agent | haipipe-insight-information | none | Instance › <q>/<L><NN>-<name>.md · draft/ |
| board | Insight | each partition | Write the Knowledge report | haipipe-insight-agent | haipipe-insight-knowledge | none | Instance › <q>/<L><NN>-<name>.md · draft/ |
| board | Insight | each partition | Check alignment | haipipe-insight-reviewer-agent | haipipe-insight-check | none | none |
| board | Insight | each partition | Pool or split | haipipe-insight-agent | haipipe-insight-knowledge | none | Instance › <q>/<L><NN>-<name>.md (the cross section) |
| board | Check | Gates | none | none | none | none | none |
| board | Check | Checks | Review an answer | haipipe-page-check-agent | haipipe-insight-check | none | Instance › <q>/runs/run-check-<MMDD>-<slug>.md |
| board | Check | Runtime | none | none | none | none | none |
| board | Delivery | Handoff | Write the counsel | haipipe-insight-agent | haipipe-insight-wisdom | none | Instance › 4-Wisdom/W<NN>-<name>/W<NN>-<name>.md |
| board | Delivery | Handoff | Draft the handoff | haipipe-insight-agent | haipipe-insight-wisdom | the handoff | Instance › 4-Wisdom/W<NN>-<name>/W<NN>-<name>.md (signed:) |

Notes
-----

- **The Views.** Every View is a tab the workbench shows (JL 261003): Guide's four, the
  Prototype's Meta, its four levels (one row stands for all four: the same runs on each) and
  RoadMap Draw, Scope's three, Insight's partitions (one row stands for every partition),
  Check's three, Delivery's Handoff. The Work and Report columns live inside each partition's table.
- **The Folder column.** Where the run writes. `<q>` is a question's task folder,
  `jNN_<level>/tNN_<name>` in the Insight Block
  (`haipipe-insight/ref/block-contract.md`); `none` writes no file, only a verdict.
- **The question rows.** "Carry a board over" moves a register board's
  questions into an Insight Block word for word (`../../haipipe-insight/ref/carry_over.py`);
  "Review the questions" judges each by Q1-Q7 and proposes keep, split, merge or
  move, and a person signs any change (`haipipe-question-review`, with Insight's level
  rule from `haipipe-insight-question`).
- **The alignment rows.** "Plan the evidence" writes each question's evidence
  needs before any run, and "Review the evidence plan" has a different agent agree
  them; in an Insight Block the question owns its code, so "Write the
  script" writes `scripts/<name>.py` from its live needs, a different agent reviews
  it, and "Run a partition" runs `runs/<dataset>_<partition>.sh` into `results/` and a
  generated `reports/` (`../../haipipe-insight/ref/block-contract.md`). "Check
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
  `Tools/designs/b11_theme_insight/studio/s02-insight-workbench/insight-workbench-design.excalidraw` draws
  Spaces, views, run types and skills; it should be drawn from this table, not
  hand-kept beside it (planned: a drawer in `table-workbench`).
- **As served.** The Work column reads each page's `answers.yaml` and shows
  every need with its bound files; the Runs panel does not read this table yet.
  Part 1 of the studio drawing is drawn from this table.
