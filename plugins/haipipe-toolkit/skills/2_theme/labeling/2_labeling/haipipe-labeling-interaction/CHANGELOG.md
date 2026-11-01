# haipipe-labeling-interaction · changes

## 0.2.0 · 2026-11-01

- The whole 🧭 meaning Task, one section per step the workbench's meaning page copies a prompt for: Frame, Report,
  Preferences, Update (b15 s58, stage 2; JL 261101: "how will you update the skills ... Please make them work").
- The Task's layout, read by `engine/meaning_versions.py`: Loop NN's Runs end in `_mNN`; `meaning/mNN.mindmap.md` and
  the sign `mNN.approved.yaml`.
- Update is `engine/meaning_update.py labels`, then the guideline written by the agent, then the flags; only the person
  signs (the page's Approve mNN).
- Preferences: one send (s58-D15, Q5): the page copies the prompt, the notes and the form's answer block together.

## 0.1.0 · 2026-11-01

- First version: a loop's report as one collect Run (report_form.py, collect.py), use case 2's draw (label_audit.py).
