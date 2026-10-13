# Changelog

## 1.0.0 · 2026-10-13 · Its own skill, out of excalidraw-read

- JL 261013, on b01_irb's CIR 2 topic: "I think we want to have the /excalidraw-revise, a new skill for this type
  of tasks"; then "please go ahead and continue and do it". excalidraw-read's revise mode (its 0.3.0 to
  0.4.0; that CHANGELOG keeps the history) moves here: `ref/read_revise.py`, `ref/track_changes.py`, `ref/revise-spec.md`.
  `read_revise.py` still draws with excalidraw-read's `ref/read_paper.py`, found through the sibling folder.
- A file without Heading 1: the plan's `sections` lists its headings in order (`head`, `name`, `find`), for the
  page cuts, the draft's divisions and the delivery (b01_irb s03, JHM IRB eForm A, 261012).
- `seed` writes the tracked Word file from the plan's changes when it does not exist yet, so a file of our own
  needs no hand-made tracked copy first (b01_irb s03).
- `deliver` asks for no paragraph break where a draft paragraph already starts a file paragraph: a form's
  one-word paragraph ("recommendations.") repeats and cannot be found once (b01_irb s03).
- The copy is read from `related/files/` (haipipe-related's name) as well as `related/materials/`.
- The drawing's writer source is `excalidraw-revise/ref/read_revise.py`; every builder and delivery script that
  called the old path was moved to the new one (SHIFT b02, b03, b04; Samsung b01_irb; b31 s04 and s21).
