# haipipe-paper-plan · changelog

## 0.2.0 · 2026-11-01 · s06-paper-displays: the display plan, by the venue's rules

- JL 261101: "in the /haipipe-paper-plan, we should also have the plan for the displays"; "the display like that
  should also follow the venue, the venue we are using". New topic `s06-paper-displays`: one row per display
  (`Display A`, its name, type, what it shows, the question, the Section, main or supplement, the Run, the state)
  and a sketch per display; its paper number is counted from the row order, never typed.
- New `scripts/display_plan.py`: `check <Board>` against the venue's `call.md` `## Displays` rules (limits, labels,
  width × resolution, format, caption words; exit 1 on a ❗), `seed <Board> [--apply]` the j01 pool Tasks.
- Drawn by excalidraw-workflow's new `displayplan_drawing.py` (① the displays, ② the venue's rules, ③ the check).
- s04 keeps only the display names in its Sections table; `paperflow_drawing.py` reads s06 when a Board has it.
- Found by slug (`sNN-paper-displays`); `seed` keeps one letter sequence in the pool (no main/supplement split);
  a row's `made by` Run is the version the check reads (PhyAbsence session's questions, 261101).
- A Display cell may be the printed label (Table B1, MISQ's appendix lettering); a pool face matches by
  `display-plan:`, a "Display X" `label:`, or `number:` (AgreeableRx session's report, 261101).
- Tested on Tools' Paper-Example (three displays; the check finds its placeholder figure too narrow for 7 in at
  300 dpi).

## 0.1.2 · 2026-11-01 · b16 review 261101: current paper names

- version Jobs are named `jNN_writing_v<MMDD>_<desk>` (from j11), no longer `jNN_v<MMDD>_<desk>` (timeline and naming, ref/faces.md Feeds).
- `_studio_groups.txt` replaces `studio/_groups.txt` in the steps.
- The topic table adds s05 paper checklist (haipipe-paper, `paper_check.py --write`) and s10 related work (haipipe-paper-related).

## [0.1.1] — 2026-10-26

Shorter description (1154 -> 451 characters): what it does, when to use it, its trigger words; aliases and old command names kept (diagnostics/descriptions/261026.yaml). (describe 261026)

## 0.1.0 · 2026-10-19 · A paper's plan: s03 the data flow, s04 the paper flow

- New skill (JL 261019: "你觉得我们需要一个 plan 吗？haipipe-paper-plan / plan for the data flow and plan for the paper
  flow"; "should make the s03-paper-dataflow-plan and s04-paper-workflow-plan"; "please think about to make the s03 to
  be the paper-dataflow, and s04 to be the s04-paper-workflow").
- `s03-paper-dataflow`: the building map, drawn by excalidraw-workflow's `workflow_drawing.py`; its yaml holds only the
  data, matching and table cards, each number read from a Result's metrics file; the question rows come from the story.
- `s04-paper-workflow`: three tables (Sections, Displays, Timeline) and two lines (`**Budget:**`, `**Send:**`), drawn by
  excalidraw-workflow's new `paperflow_drawing.py`; a figures topic folds into it.
- One owner per fact: the questions, E rows, T rows and venues stay on the s02 face; the plan reads them.
- `ref/faces.md`: both faces as templates. First Board: Physician-SPACE Project-Example-B `Paper-Example-B`.
- A fresh-agent test on a made-up paper (food apps against a map search) found 16 gaps; fixed here and in
  excalidraw-workflow 0.2.0: the paper door routes to this skill, `where` names a T row's folders, `numbers:` puts a
  Run's answer on its card, words "(outside the count)", a budget with no desk record is an own estimate, a person's
  step names its verb, Results follow the story's order, the version's desk is the story topic's, s03's Decided holds
  only what planning decided, and the reviewer uses this skill's four questions.
- A second fresh-agent test passed the core (routing, numbers on cards, every claim, 🙋 on every person's step,
  check.py) and found smaller gaps, fixed: a story that disagrees with disk is listed in Open, never edited; a
  version is named by its send date; a near-match or partial desk record; s04's template has a Files block; an
  agent's decision is "proposed by"; `numbers:` takes a list; the card shows a T row's Run ids.
