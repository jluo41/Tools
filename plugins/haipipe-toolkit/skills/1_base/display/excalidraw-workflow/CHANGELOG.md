## 0.1.0 · 2026-10-14 · A paper's building map, with the review overlay

- New skill (JL 261014: "could you highlight that which part the reviewers wanted us to change, and how will our new
  field experiment and analsysis will fix it?"; "we should keep the current structure, it will serverd as the building
  map"; "How do you think we can add it to the themes/paper skills set"; "or call it /excalidraw-workflow").
- `scripts/workflow_drawing.py`, lifted from Paper-TestToLearn-MS2026's `make_paper_workflow.py` (itself copied from
  WellDoc's Paper-ScalingGlucose-NatSeries2026): the same six columns, light version and question rows. `draw <topic>`
  and `make <topic>`; the words in `<topic>-drawing.yaml`.
- Generalized: the foundation columns are cards in the yaml (`task:` reads a §7 row, `tasks_of:` a question's Tasks,
  `group:` a dashed box of small cards, `count:` a number counted from a JSON file), joined by `links:`; the questions
  come from the Board Questions' reports (`#### 3.N` blocks), the telling from board.md `story-current:`, the Tasks
  from the Project's `work/`, a Task's state from its Runs' `result/`.
- The review overlay: each Review Item's `hits` and `fixed by` cells (haipipe-paper-comments 1.3.0) draw a red border
  and ❗ line on what the reviewers attacked and a green border and 🛠 line on the work that answers it; items fixed only
  in the writing, or by nothing, are listed under the map.
- Written through haipipe-studio's canvas.write in Nunito, so a person's marks survive a rebuild.
- First user: Paper-TestToLearn-MS2026's s04-paper-workflow (20 Review Items, 19 on cards).
