# QY3-for-view regression report

Fresh-context run against `haipipe-page-for-view` and `haipipe-view`, isolated to `_runs/skill-forward/QY3/`. QY1 and QY2 were not opened.

## What was built

- `QY3-for-view.md` (page-type: view) + `views/QY3-for-view/` resource folder, created with `view.py create`.
- Two reused QBt1 Probes copied verbatim into `views/QY3-for-view/input/QA-probes/`: `1-canonical-definition.md`, `3-measurement-boundary.md`. The observable-signal Probe was deliberately excluded.
- QBt1's `references.bib` copied verbatim into `views/QY3-for-view/input/sources/references.bib`; `\citep{john1999bigfive}` resolves against it.
- One owner-indexed table Display, `QY3-Display1-trait-boundary-table/`, with `output.md`, `float.tex`, `assets/table.tex`, `preview.pdf`, and `preview.png` (rendered with `xelatex` + `pdftoppm`, matching the QBt1 pipeline).
- The Display Card in Content 3 carries a real `Binding:` to `output.md` plus a `Files:` field with backtick-quoted, real `preview.png`, `preview.pdf`, and `float.tex` paths.
- One local consumer Page, `consumers/QY3-Consumer-boundary-note.md`, inside the QY3 run folder (not the shared `QS-consumers` group). C1 targets it and stays `planned`.
- Generated TeX/PDF/DOCX review projections under `views/QY3-for-view/build/review/`.

## Commands run

```
python3 view.py create <QY3 run dir> QY3-for-view --title "..."
python3 view.py check  QY3-for-view.md   → valid · 2 QA probes · 1 displays · 1 consumers · acceptance waiting
python3 view.py status QY3-for-view.md   → Displays QY3-Display1:rendered/waiting · Consumers C1:planned
python3 view.py build  QY3-for-view.md   → built .../build/review · tex + pdf + docx · canonical Page unchanged
python3 view.py build  QY3-for-view.md --check → current .../build/review · tex + pdf + docx
```

All four ran clean with no ERROR lines. One manifest fix was needed mid-run: the Consumer `target` path started at three `../` segments (copied from QBt1's shared-group depth) but the local consumer sits one level shallower inside the run folder, so it was corrected to two `../` segments before `check` passed.

## Gate state (unchanged by this run)

- View acceptance: `waiting`.
- QY3-Display1 acceptance: `waiting`.
- C1 consumer status: `planned`, blocked on View and Display acceptance.
- A current review build is not human acceptance; nothing here was written on JL's behalf.

## Scope

Every file written or copied lives under `_runs/skill-forward/QY3/`. No file outside that folder was read for write purposes and none was modified; QBt1's Probe and bibliography files were only read and copied, not edited. QY1 and QY2 were not inspected, per instruction.
