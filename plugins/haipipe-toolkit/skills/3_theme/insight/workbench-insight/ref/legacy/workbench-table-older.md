Insight Workbench Table
=======================

Shape and check: `skills/0_utils/table-workbench/SKILL.md`. Rows run input →
process → output. `(new)` marks a skill or agent planned but not built yet.

Two Insight agents: `hai-insight-agent` makes (plans, writes reports and
counsel), `hai-insight-reviewer-agent` judges and never checks its own
page. Runs come from `hai-task`'s orchestrator. `hai-insight-workflow`
routes Runs and evaluates the GI gates; it is no row's Skill.

| Level | Space | View | Run type | Agent | Skill | Person signs | Folder |
|---|---|---|---|---|---|---|---|
| board | Guide | Description | none | none | none | none | none |
| board | Guide | Method | Add a method | hai-insight-agent | workbench-insight | none | Tools › servers/workbench-insight/guide/methods/ |
| board | Guide | RoadMap Draw | none | none | none | none | none |
| board | Guide | Related Paper | Add a paper | hai-discovery-orchestrator-agent | hai-discovery | none | Tools › servers/workbench-insight/related/papers.md |
| board | Scope | Dataset | Record the extract | hai-insight-agent | hai-insight-meta | none | Question Book › 0-Meta/meta.md |
| board | Scope | Segments | none | none | none | none | none |
| board | Scope | Questions | Ask | hai-insight-agent | hai-insight-question | the question | Question Book › <q>/<L><NN>-<name>.md |
| board | Question Book | Meta | Carry a board over | hai-insight-agent | hai-insight | none | Question Book › board.md · 0-Meta/ · <level>/level.md · <q>/ |
| board | Question Book | Meta | Register a segment | hai-insight-agent | hai-insight-partition (new) | the segment | Question Book › 0-Meta/partitions.md |
| board | Question Book | Data · Information · Knowledge · Wisdom | Review the questions | hai-insight-reviewer-agent | hai-report | a change | Question Book › <q>/<L><NN>-<name>.md (a signed change) |
| board | Question Book | Data · Information · Knowledge · Wisdom | Plan the evidence | hai-insight-agent | hai-insight-evidence-plan | none | Question Book › <q>/<L><NN>-<name>.md (needs) |
| board | Question Book | Data · Information · Knowledge · Wisdom | Review the evidence plan | hai-insight-reviewer-agent | hai-insight-evidence-plan | none | Question Book › <q>/<L><NN>-<name>.md (agreed:) |
| board | Question Book | Data · Information · Knowledge · Wisdom | Write the script | hai-task-creator-agent | hai-insight | none | Question Book › <q>/scripts/ |
| board | Question Book | Data · Information · Knowledge · Wisdom | Review the script | hai-task-reviewer-agent | hai-insight | none | none |
| board | Question Book | RoadMap Draw | Draw the question map | hai-insight-agent | hai-insight | none | Question Book › studio/question-map.excalidraw (generated) |
| board | Insight | each segment | Run a segment | hai-task-orchestrator-agent | hai-insight | none | Instance › <q>/results/<segment>/ · reports/<segment>/ |
| board | Insight | each segment | Write the Data report | hai-insight-agent | hai-insight-data | none | Instance › <q>/<L><NN>-<name>.md · draft/ |
| board | Insight | each segment | Write the Information report | hai-insight-agent | hai-insight-information | none | Instance › <q>/<L><NN>-<name>.md · draft/ |
| board | Insight | each segment | Write the Knowledge report | hai-insight-agent | hai-insight-knowledge | none | Instance › <q>/<L><NN>-<name>.md · draft/ |
| board | Insight | each segment | Check alignment | hai-insight-reviewer-agent | hai-insight-check | none | none |
| board | Insight | each segment | Pool or split | hai-insight-agent | hai-insight-knowledge | none | Instance › <q>/<L><NN>-<name>.md (the cross section) |
| board | Check | Gates | none | none | none | none | none |
| board | Check | Checks | Review an answer | hai-draft-check-agent | hai-insight-check | none | Instance › <q>/runs/run-check-<MMDD>-<slug>.md |
| board | Check | Runtime | none | none | none | none | none |
| board | Delivery | Handoff | Write the counsel | hai-insight-agent | hai-insight-wisdom | none | Instance › 4-Wisdom/W<NN>-<name>/W<NN>-<name>.md |
| board | Delivery | Handoff | Draft the handoff | hai-insight-agent | hai-insight-wisdom | the handoff | Instance › 4-Wisdom/W<NN>-<name>/W<NN>-<name>.md (signed:) |

Notes
-----

- **The Views.** Every View is a tab the workbench shows (JL 261003): Guide's four, the
  Question Book's Meta, its four levels (one row stands for all four: the same runs on each) and
  RoadMap Draw, Scope's three, Insight's segments (one row stands for every segment),
  Check's three, Delivery's Handoff. The Work and Report columns live inside each partition's table.
- **The Folder column.** Where the run writes. `<q>` is a question's task folder,
  `jNN_<level>/tNN_<name>` in the Insight Block
  (`hai-insight/ref/block-contract.md`); `none` writes no file, only a verdict.
- **The question rows.** "Carry a board over" moves a register board's
  questions into an Insight Block word for word (`../../hai-insight/ref/carry_over.py`);
  "Review the questions" judges each by Q1-Q7 and proposes keep, split, merge or
  move, and a person signs any change (`hai-report`, with Insight's level
  rule from `hai-insight-question`).
- **The alignment rows.** "Plan the evidence" writes each question's evidence
  needs before any run, and "Review the evidence plan" has a different agent agree
  them; in an Insight Block the question owns its code, so "Write the
  script" writes `scripts/<name>.py` from its live needs, a different agent reviews
  it, and "Run a segment" runs `runs/<dataset>_<segment>.sh` into `results/` and a
  generated `reports/` (`../../hai-insight/ref/block-contract.md`). "Check
  alignment" and "Review an answer" run `hai-insight-check`; a cell's status is
  computed, never settled by hand. Contract:
  `../../hai-insight/ref/evidence-needs.md`.
- **Make and judge apart.** The agent that writes a report never runs its
  check; a cell turns ✅ only when a CHECK by another agent closed after its run.
- **Person signs.** Only what leaves the board or changes its meaning: the question
  a person asks, a change the question review proposes, a new segment, and the Wisdom
  handoff (`signed:`). The evidence plan, its release of new
  computation and each page's plan are decided by agents: one drafts, a different
  one agrees or closes.
- **The studio drawing.** Part 1 of
  `Tools/plugins/haipipe-toolkit/servers/workbench-insight/studio/insight-workbench-design.excalidraw` draws
  Spaces, views, run types and skills; it should be drawn from this table, not
  hand-kept beside it (planned: a drawer in `table-workbench`).
- **As served.** The Work column reads each page's `answers.yaml` and shows
  every need with its bound files; the Runs panel does not read this table yet.
  Part 1 of the studio drawing is drawn from this table.
