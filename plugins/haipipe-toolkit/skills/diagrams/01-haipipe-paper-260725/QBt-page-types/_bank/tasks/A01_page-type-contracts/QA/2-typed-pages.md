# Q — Across every board under `skills/diagrams/`, how many pages exist and how many of them declare a type key in their head?
- state:   answered
- started: 2026-08-07T18:11
- by:      A02_measure_estate/measure_typed_pages.py

## Answer

```text
  board                    pages  typed
  -----------------------  -----  -----
  BoardSkillBoard-260722      67      9
  01-haipipe-paper-260725     61      0
  01-haipipe-task-260726      19      0

```

3 boards · 147 pages · 9 declare a type key (6%)

A page is counted the way `src/common.py` counts one: a `.md` whose name starts `Q`, `S`, `Agent-` or `Meeting-`, with `_` and `.` segments and `fig/` skipped. A page counts as typed if its head carries `page-type:` or `route:`.

Every one of the nine is on `BoardSkillBoard-260722`, and eight of those nine are the `QBt` specimens themselves. So the type system is today a design with one worked example set rather than a property of the estate.

One limit travels with it: this counts pages that DECLARE a key, not pages that declare the right one.
