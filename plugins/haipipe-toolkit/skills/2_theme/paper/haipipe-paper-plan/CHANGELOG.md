# haipipe-paper-plan · changelog

## 0.1.0 · 2026-10-19 · A paper's plan: s03 the data flow, s04 the paper flow

- New skill (JL 261019: "你觉得我们需要一个 plan 吗？haipipe-paper-plan / plan for the data flow and plan for the paper
  flow"; "should make the s03-paper-dataflow-plan and s04-paper-workflow-plan"; "please think about to make the s03 to
  be the paper-dataflow, and s04 to be the s04-paper-workflow").
- `s03-paper-dataflow`: the building map, drawn by excalidraw-workflow's `workflow_drawing.py`; its yaml holds only the
  data, matching and table cards, each number read from a Result's metrics file; the question rows come from the story.
- `s04-paper-workflow`: three tables (Sections, Displays, Timeline) and two lines (`**Budget:**`, `**Send:**`), drawn by
  excalidraw-workflow's new `paperflow_drawing.py`; a figures topic folds into it.
- One owner per fact: the questions, E rows, T rows and venues stay on the s02 face; the plan reads them.
- `ref/faces.md`: both faces as templates. First Board: Physician-SPACE Project-LLMRec-Physician `Paper-LLMRecPhy-Jama`.
- A fresh-agent test on a made-up paper (food apps against a map search) found 16 gaps; fixed here and in
  excalidraw-workflow 0.2.0: the paper door routes to this skill, `where` names a T row's folders, `numbers:` puts a
  Run's answer on its card, words "(outside the count)", a budget with no desk record is an own estimate, a person's
  step names its verb, Results follow the story's order, the version's desk is the story topic's, s03's Decided holds
  only what planning decided, and the reviewer uses this skill's four questions.
- A second fresh-agent test passed the core (routing, numbers on cards, every claim, 🙋 on every person's step,
  check.py) and found smaller gaps, fixed: a story that disagrees with disk is listed in Open, never edited; a
  version is named by its send date; a near-match or partial desk record; s04's template has a Files block; an
  agent's decision is "proposed by"; `numbers:` takes a list; the card shows a T row's Run ids.
