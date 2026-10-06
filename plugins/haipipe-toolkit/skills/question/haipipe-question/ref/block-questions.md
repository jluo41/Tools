# Block Questions and Report Pages

Read for question-driven Block work, a Question's Report, or its related
resources. `haipipe-question` owns this register and the report's header lines
(moved from `haipipe-task`, 2026-10-03); `haipipe-task` owns the Task work a
Question cites; `haipipe-page` owns writing each report; `haipipe-workbench-task`
presents them. What makes a good Question (a topic, not a decision) is
`../SKILL.md` § A question is a topic.

## Placement

```text
tasks/bNN_<block>/
├── board.md                         Question and resource registers
├── studio/*.excalidraw              drawings the whole Block shares (the question map)
├── reports/
│   └── q01_<topic>/
│       ├── q01_<topic>.md            ordinary same-stem Page: Opening → Content
│       ├── page.toml                explicit registration with the native Page reader
│       ├── studio/                  this report's own drawings; scripts in studio/_build/
│       ├── draft/                   created by the normal Page writing flow
│       └── runs/, results/          only the Page's own Runs, when needed
└── jNN_<job>/tNN_<task>/             executable work and its native Results
```

One Question, one drawing (JL 261005: "for each question we should just have one
excalidraw"). A report has exactly one `.excalidraw`, linked once from its `### Evidence`:
more views are frames inside it, and a screenshot or figure the report cites is an image
inside it too ("some png can be put into the excalidraw as well"), never a second link
(`excalidraw-report` rules 6, 9 and 11). It lives in the report's folder (JL 261004), as
`reports/qNN_<topic>/studio/<name>.excalidraw` or, drawn by a Block builder, as
`reports/qNN_<topic>/qNN_<topic>.excalidraw` beside the Page; its build script, when a script
draws it, sits in that `studio/_build/` or the Block's. The Block's `studio/` keeps only the
drawings the whole Block shares: the question map, the road map, and any drawing several
Questions or Jobs use. `--drawing <name>` (once) makes the blank drawing in the report's
`studio/` and lists it under `### Evidence`. The workbenches show the first drawing a report
links (else its own, unlinked); a second drawing or a linked picture is a finding in Check.

A CoWork Block (`cowork/bNN_<topic>/board.md`, `board-kind: cowork-block`, owned by
`haipipe-cowork`) keeps the same register and `reports/` folder. There a Question's
`work:` names files inside the Block (a ticket page, a design note) instead of Task
Folders; the helper below checks that each named file exists.

A report Folder is reading material, not an executable `tNN` Task. It gets no
BJTR address and creates no Job, native `rNN`, or Task workflow. Page-owned
writing/evidence/check/delivery Runs may live inside that report Folder under
the Page contract. The Block root acquires no executable lane.

The Task Page already explains its own Task. A Block report synthesizes the
answer to a Question and may reference several Tasks. Reference original
Results and Task Pages; do not copy them into another result registry.

## Register in board.md

Use one YAML fence in each optional section. Existing Blocks need no migration;
unassigned Tasks remain visible. An id is `Q` and two or more digits (`Q01`), or
`Q-<word>-<number>` with a lower-case word (`Q-food-1`, `Q-exercise-2`; JL 261004), for a
register cut by a word such as an event type. Its report folder is the id in lower case
(`q01_<topic>`, `q-food-1_<topic>`). The Workbench shows `Q01` as "Question 1" and a
named id as itself. Question ids are stable within the Block; reordering cards does not
rename their ids or report files. `title` is optional: without one the question is the
title and is shown once. A good entry reads as a slug, then the question, then its aim
(JL 261004): `title` is the topic in two or three words; `question` is one short question
read at a glance, about 12 words, with no brackets and no "done when" (JL 261004: long
questions are hard to read on the card); `acceptance` holds its parts and what counts as
done, in short sentences (no numbers or verdicts), shown under More; and the optional `aim`
says what answering it achieves, one line, so a series of questions reads as a story where
each aim feeds the next. The Workbench shows the aim under the question.

````markdown
## Questions

```yaml
questions:
  - id: Q01
    title: Comparable conditions
    group: Setup
    question: Can both methods use the same data and evaluation rules?
    aim: Compare the two methods on equal terms.
    hypothesis: Identical inputs and rules allow a fair comparison.
    acceptance: Record the data version, split and metric.
    work:
      - path: j01_data_checks/t01_source_audit
        stage: Data
        role: Establish which records can be compared.
    report: reports/q01_comparable_conditions/q01_comparable_conditions.md
```

## Related resources

```yaml
resources:
  - title: Evaluation reference
    url: https://example.test/evaluation
    questions: [Q01]
    contribution: A reference protocol for this comparison.
    notes: Review whether its assumptions apply here.
```
````

Optional `group` names the series a Question belongs to (free text, for example the
datasets read one by one and the topics read across them). The Task Workbench shows one
Task View per group, in the order the register first names it; a register without groups
is one View, Questions. A group changes no id, report or execution state.

`work` also accepts plain Task path strings. On a mapping, optional `stage`
is the reader-facing Work label (for example Data, Training or Evaluation),
and `role` explains why this Task helps this Question. It creates no new
lifecycle stage and does not change the Task's `task-type`. Without a label,
the Workbench uses `task-type`, then Task; it never guesses a type from the
folder name. Work rows retain their authored order.

Paths are relative to the Block;
they must identify existing direct `jNN_*/tNN_*` Task Folders. A Task may
support several Questions. A Question may have `work: []` and reach an answer
through reasoning or existing evidence. Missing reports remain visibly open.
Resource URLs are http(s); their Question references are optional.

The helper authors the register, an empty Page frame and its `page.toml`:

```sh
python <skill>/ref/block_questions.py add-question <block> \
  --id Q01 --slug comparable_conditions --title 'Comparable conditions' \
  --question 'Can both methods use the same data and evaluation rules?' \
  --hypothesis 'Identical inputs and rules allow a fair comparison.' \
  --acceptance 'Record the data version, split and metric.' \
  --work j01_data_checks/t01_source_audit

python <skill>/ref/block_questions.py add-report <block> \
  --id Q-food-1 --slug input_forms --drawing api_food

python <skill>/ref/block_questions.py add-resource <block> \
  --title 'Evaluation reference' --url https://example.test/evaluation \
  --question Q01 --contribution 'A reference protocol for this comparison.'
```

`add-report` frames the report of a Question already in the register and writes its
`report:` line; `--evidence 'label|path'` (repeatable, a file inside the Block) lists that
file under the frame's `### Evidence`, percent-encoded, so a linked `.excalidraw` shows in
the Workbench's Report column. `--drawing <name>` (once: one Question, one drawing) makes the
report's blank drawing at `reports/<id>_topic/studio/<name>.excalidraw` and lists it the same way. Evidence links are pointers, not an answer: the
frame keeps `answer-status: open` and writes no `results-read:`, so Check shows "Evidence
review time is not recorded" until someone reads the evidence.

The helper depends on the same plugin's `servers/workbench-task/task_questions.py`
and PyYAML. It refuses duplicate ids, existing report folders and invalid work
references. An existing Question is edited in its current register entry;
an existing Report is opened in place through Page.

## Report contract and writing

The Report is a `haipipe-page` Page, with its normal Opening, Content, Draft,
evidence records, adoption, CHECK and release. Load
`../../../page/haipipe-page/SKILL.md` before writing it. Do not apply the
executable Task Page grammar or `folder-kind: task` to this report Folder.
No new Folder kind is needed for an ordinary report Page.

For a manually created report, register it with the ordinary Page manifest:

```toml
version = 1
source = "q01_comparable_conditions.md"
title = "Comparable conditions"
```

The `source` must match the report Folder's same-stem Markdown. Registration
enables the existing Page workbench; it does not record writing or approval.

Task adds three header lines to the report Page:

- `answers: Q01` (comma-separated ids if a report answers multiple Questions).
- `answer-status: open | partial | answered` describes the Question's answer.
  It is independent of the Page's native `state:` and of execution completion.
- `results-read: <ISO-8601 time with timezone>` records when its linked
  evidence was actually read. Set it after the reading, never merely on save.

Opening states the current answer in plain language. For the compact reading
in the Task Workbench, use these Content division names (normal Page numbered
paragraphs, Draft Bullets and evidence bindings still apply):

1. **Answer** — reasoning and interpretation supporting Opening.
2. **Evidence** — Markdown links to exact Result files or source Pages. Resolve
   file links relative to the report Folder, e.g.
   `../../j01_data_checks/t01_source_audit/results/r01_example/metrics.json`.
3. **Limits** — remaining uncertainty, missing evidence or scope boundaries.
4. **Next** — the concrete action to continue; an answered Question may instead
   state the downstream use or that no further action is needed.

Write through the Page flow: plan Structure and evidence needs, draft,
adopt when authorized, then the owning CHECK/release gates. The scaffold
contains no answer, accepted Content, fabricated receipt or completed review.
Do not type final prose directly into generated Content.

The Workbench reads Opening and these Content divisions. It shows declared
answer status and Page state separately. Task and Progress share this source;
there is no separately maintained progress file. Linked local evidence newer
than `results-read` is flagged for review without rewriting the report.
External links and unlinked changes cannot be freshness-certified by this
projection; use the Page's own evidence and CHECK workflow for closure.

## Routing the word report

- `haipipe-task report <tNN folder>` is P-B-E-R: `workflow/report.yaml` and
  execution audit, as defined in `fn/stage-report.md`.
- “Report for Q01 / answer this Block Question” uses this reference and the
  report's Page workflow. It can lead to a request for Task work when evidence
  is missing, but does not execute work implicitly.
- The Workbench is a reading/editing surface over these owners. Run completion
  alone never marks a Question answered or a report Page released.
