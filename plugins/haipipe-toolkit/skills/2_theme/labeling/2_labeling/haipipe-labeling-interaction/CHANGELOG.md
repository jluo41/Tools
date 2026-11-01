# haipipe-labeling-interaction · changes

## 0.2.1 · 2026-11-01

- From a fresh agent's run-through of the Preferences prompt (save, Update, guideline, flags): Update keeps an earlier loop's record for an item the new report does not show (meaning_update.py lost it); it writes the Update Run's card and receipt and takes the prompt's notes (`--notes`); save takes a file; a rule's note starts with the card that set it; the mind map checker named; which answers get flags; earlier deferred cards asked again; the reply link and the session line said.

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
