# Changelog

## 0.2.1 · 2026-10-03 · Guide rows need no card

- `--check --cards` skips rows whose Space is Guide: Guide's Runs panel (workbench-shared) reads its run types from the table, so they never have a run card (asked by the Paper workbench session; its 2 Guide rows were the only findings).

## 0.2.0 · 2026-10-02 · Folder column (JL 261002)

- Optional eighth column Folder: where the run writes, or none. `read_table` accepts the seven
  columns with or without it; `--check` flags an empty Folder cell; blocks print `writes`.

## 0.1.0 · 2026-10-01 · Cards check (JL 261001)

- `--check --cards <run-cards.md>`: every run type of the table is one card with the same
  🤖 AGENT, 🧩 SKILL and ✍️ SIGNS lines, and every card is a row.

## 0.1.0 · 2026-10-01 · First version (JL 261001)

- The Workbench Table: one row per run type, seven columns (Level · Space · View ·
  Run type · Agent · Skill · Person signs). Every run names an agent and one small
  skill; the person only signs.
- `ref/render_workbench_table.py`: `--format md|blocks` and `--check` (empty cells, a
  person as Agent, a `-workflow` skill as a row's Skill, a judging row whose agent also
  makes, names not found under Tools/plugins unless marked `(new)`).
- First instance: `skills/design/haipipe-workbench-design/ref/workbench-table.md`.
