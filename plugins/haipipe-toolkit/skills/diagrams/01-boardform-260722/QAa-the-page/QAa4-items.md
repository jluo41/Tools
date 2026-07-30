# Page Items to Finish: the testable gap
state: 🟡 PARTIAL · rules settled on QAa0, carved 260729; face awaits JL
owner: CC
method: every checkbox is a condition another person can judge; a tick means verified

## Question
What makes `## Items to Finish` a definition of done rather than a task list, and what does a tick mean?
A checkbox is a condition another person can judge true or false, the heading counts automatically, and a tick means the condition was VERIFIED, never merely attempted (`SKILL.md`'s sync rule: never tick what was not verified).
On S pages each Q-consumer stays one complete record and closes only after its answer is interpreted and woven into Content.

## Boundary
- ✅ Covered here
  Checkbox semantics, the auto count, the verified-tick rule, and the Q-consumer record shape inside the list.
- ↪ Covered elsewhere
  The write-back trigger (work done ⇒ tick in the same round): `SKILL.md`'s sync verb, enforced by `check.py`'s `open-with-done-items`.
  Where the answer behind a Q-consumer comes from: the probe layer (`/haipipe-probe`).

## Diagram

/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/board.excalidraw&frame=QAa4

## Content
### 1 · Items to Finish: define the gap
Items to Finish is the testable definition of done, not a loose task list.
Every checkbox must describe a condition that another person can judge true or false, and the heading reports the completed count automatically.
On S, each Q-consumer remains one complete record and closes only after its answer is interpreted and integrated into Content.
Under the base/variant model on `QAa0`, this section is frame: a page kind may contribute a record shape into the list, which is what the S Q-consumer record is, and the checkbox semantics, the auto count, and the verified-tick rule hold for every kind.



### 2 · The source: testable completion
Write `## Items to Finish` as checkboxes that another person can judge true or false.
The rendered heading counts them automatically.
On S, each former Q-consumer stays together as one recognizable record and closes only after its answer is interpreted and integrated into Content.

## Items to Finish
- [ ] 🧠 JL confirms this face owns Items to Finish
      Carved 260729 from QA4 §4 with the text verbatim; the history stays on `QAa0`.

## Where we are
Settled and enforced: the auto count ships, `check.py` catches state/tick disagreement, and the Q-consumer record shape is live on the MISQ board.

## Files
- `src/page_question.py`
  The auto-counted heading and checklist rendering.
- `check.py`
  `open-with-done-items` / `partial-with-nothing-open`.

## Log
260729 · Marked frame under the base/variant model on QAa0: a kind contributes a record shape, never the checkbox semantics
260729 · Opened by carving QA4 §4 out to its own face, text verbatim
