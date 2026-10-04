# b01 · Utility skills

board-kind: task-block
spine: Design questions about the small cross-cutting skills in `plugins/haipipe-toolkit/skills/0_utils/`: how chat replies are shaped, how questions are tracked, and the helpers every session shares.
close: Each recorded question has a report Page with an answer status, and every answered question names the skill change that settled it.

## Topic

The `0_utils` skillset holds skills every session leans on: `response-format` (how chat replies
are shaped), `diagram-ascii`, `draw-logic-tree`, `table-workbench`, `remote-error`, `call-peer`, `notebook-cell-python` and two
personal connectors. Its questions are about the skills themselves: what a skill should own,
where an instruction should live, and how a rule should be phrased. The question skills
(`haipipe-question`, `ask-questions`) left `0_utils` for `skills/question/` on 2026-10-03; how
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
  url: https://github.com/jluo41/Tools/tree/main/plugins/haipipe-toolkit/skills/question/ask-questions
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
