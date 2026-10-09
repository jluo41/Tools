# j01 · Utility skills

job-of: b01_haipipe-toolkit (the Block `b01_utils` until 261009; its questions, studio and runs moved with it)
spine: Design questions about the small cross-cutting skills in `plugins/haipipe-toolkit/skills/0_utils/`: how chat replies are shaped, how questions are tracked, and the helpers every session shares.
close: Each recorded question has a report Page with an answer status, and every answered question names the skill change that settled it.

## Topic

The `0_utils` skillset holds skills every session leans on: `response-format` (how chat replies
are shaped), `diagram-ascii`, `draw-logic-tree`, `table-workbench`, `remote-error`, `call-peer`, `notebook-cell-python` and two
personal connectors. Its questions are about the skills themselves: what a skill should own,
where an instruction should live, and how a rule should be phrased. The question skills
(`haipipe-question`, `ask-questions`) left `0_utils` for `skills/1_base/question/` on 2026-10-03; how
questions are recorded and answered stays a question of this Block until it outgrows it.

Most answers here are a change to a `SKILL.md`, its `CHANGELOG.md` or an instruction file that
points to it, not a Task Run. A Question may therefore have no work entries; its report links
the changed files. A Task folder joins only when a change needs a tested Run.

Excluded: the large skillsets (page, task, paper, insight, design, discovery, display, writing,
board), which get their own Blocks.

## Pipeline

```text
chat section -> Related question (recorded, or proposed + folder offer) -> haipipe-question -> skill change -> report Page
```

## Pages

No Jobs yet: the first questions are answered by skill changes.

## Questions

```yaml
questions:
- id: Q01
  title: Point to a skill or restate it
  question: Should an instruction file such as AGENTS.md restate a skill’s rules,
    or only point to the skill?
  hypothesis: 'Only point: the skill is the one source, and a restated copy drifts
    from it as soon as the skill changes.'
  acceptance: Answered when the instruction file holds a one-line pointer and the
    skill’s change history shows how quickly a copy would have gone stale.
  work: []
  report: reports/q01_point_or_restate/q01_point_or_restate.md
- id: Q02
  title: How are questions recorded and answered?
  question: What is a board question, how big should it be, where does it live, and
    how does a chat reply link it?
  hypothesis: A question is a topic that many sections feed and that grows into its
    report; one skill owns it and the others point to it.
  acceptance: Answered when one skill owns the question contract, the reply format
    links questions at topic size, and a proposed question can become a folder.
  work: []
  report: reports/q02_questions/q02_questions.md
- id: Q03
  title: How does a pull sync every repo?
  question: How does one pull bring DrFirst-SPACE, the Tools-SPACE clone behind its
    Tools symlink, and every submodule up to date, and what breaks along the way?
  hypothesis: 'A per-repo loop works where git submodule commands fail: fast-forward
    the root, restore the Tools symlink, fast-forward each submodule on its own branch,
    then relink skills; a root pin can still name a commit never pushed.'
  acceptance: Answered when the steps are written once, each failure seen so far (empty
    Tools folder, missing ignore setting, unpushed pin, false fetch errors) has its
    fix, and one more pull runs from the steps alone.
  work: []
  report: reports/q03_repo_sync/q03_repo_sync.md
- id: Q04
  title: Can one Project live in two SPACEs?
  question: 'Can one Project be a submodule of two SPACEs at once, and what has to
    stay in step: paths, data stores, receipts, pushes?'
  hypothesis: Code and pages travel through git; the _WorkSpace data store, old receipts
    and push order do not, so one SPACE must own the active work.
  acceptance: A rule for which SPACE owns a shared Project, how its data store is
    copied, and the push order for a rename or move.
  work: []
  report: reports/q04_project_two_spaces/q04_project_two_spaces.md
- id: Q05
  title: Where does labeling work live in a Project?
  question: Where does labeling work live in a Project, and what are its Block, Job,
    Task and Run?
  hypothesis: labelings/ beside tasks/; a Block is any grouping, and one labeling
    of one dataset with one label is the unit the engine runs.
  acceptance: One layout used by all labeling Projects, each level named, and the
    labeling workbench opening every labeling Page in it.
  work: []
  report: reports/q05_labeling_world/q05_labeling_world.md
```

## Related resources

```yaml
resources:
- title: response-format skill (SKILL.md and CHANGELOG.md)
  url: https://github.com/jluo41/Tools/tree/main/plugins/haipipe-toolkit/skills/0_utils/response-format
  questions:
  - Q01
  - Q02
  contribution: The chat reply format every session loads; its change history is the
    evidence for Q01.
  notes: AGENTS.md rule 5 in the SPACE now points here instead of restating it.
- title: ask-questions skill
  url: https://github.com/jluo41/Tools/tree/main/plugins/haipipe-toolkit/skills/1_base/question/ask-questions
  questions:
  - Q01
  - Q02
  contribution: Matches a chat section to a recorded board question, or proposes a
    topic question on the board that owns the work.
  notes: The route by which chat questions reach this register.
- title: question skillset (haipipe-question, ask-questions)
  url: https://github.com/jluo41/Tools/tree/main/plugins/haipipe-toolkit/skills/question
  questions:
  - Q02
  contribution: Owns what a board question is, its topic size, its folder and how
    a reply links it.
  notes: ''
```
