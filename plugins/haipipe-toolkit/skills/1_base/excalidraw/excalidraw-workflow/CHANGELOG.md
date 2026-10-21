## 0.2.0 · 2026-10-19 · The paper flow, and the map read from a drawn telling

- New `scripts/paperflow_drawing.py` for a paper's `s04-paper-workflow` (haipipe-paper-plan; JL 261019: "please think
  about to make the s03 to be the paper-dataflow, and s04 to be the s04-paper-workflow"): the Sections as stairs with
  their questions, words and displays, what each must do, each display with its Run, and the dated steps to the send.
- The building map, now a paper's `s03-paper-dataflow`, reads a drawn telling (haipipe-paper-story 0.23): its
  `**The paper's question**:` as the question line, a claim from several hypotheses (`from 1a, 1b · …`), each
  question's `Research question`, and the short T table, whose `state` decides ran or not.
- From a fresh-agent test: a T row's folders come from its `where` cell when it names them (`feeds` held question
  names, so T5 drew "no task folder yet" beside "ran"); a claim from two hypotheses is drawn once and named beside the
  second, not "no claim of its own"; an analysis card shows its answer from `numbers:`; the builder writes the .png;
  `make`'s starting yaml matches haipipe-paper-plan's `ref/faces.md` and has no `figures:` key over s04's displays.
- paperflow_drawing.py: a person's step is marked 🙋 by its verb (marks, presses, reads, signs, sends …), no name
  built in; Discovery rows count as evidence; a row counts toward the cap unless it says `(outside the count)`; the
  key reads "Budget: … · Send: …"; a legend says what ✅ 🔶 ⬜ mean; the title starts with a capital.
- A foundation card's `count:` can read an object's values (`say: "{rows:,} rows"`), not only count a list.
- The "in the paper" card names the displays the Board's `s04-paper-workflow` gives each question; a question with
  no contribution no longer prints "a reader gains: none yet".

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
