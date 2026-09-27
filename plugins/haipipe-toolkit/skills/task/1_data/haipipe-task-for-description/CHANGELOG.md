haipipe-task-for-description — Changelog
========================================

Skill-scoped changelog (never loaded at invocation; read on demand).
Versions match SKILL.md frontmatter `version:`.
Newest first.

## [0.3.1] — 2026-09-27

- `templates/describe_table.py`: real `##` section headings numbered in plain digits (`## 1. Grain`), and `# notebook: hide-code`, so the Table Card notebook opens on its outputs (notebook-cell-python 0.4.1, rules 2 and 7).

## [0.3.0] — 2026-09-27

- Rule 9: every section of a card page or notebook answers one question, named in its title,
  answer first. Rule 10: keep only what helps a person read the data; the page leads with its
  notebook link. Rule 11: a notebook is named for what it shows and keeps one short call per
  question, its drawing code in the Block's `src/`. WellDoc Proj01 `b00` follows all three.

## [0.2.0] — 2026-09-27

- "What every card answers": seven questions every card answers in order (files, row, people,
  time, every column, links, flags), and the column roles that decide what a card may show.
- Second way to make the card: a raw table in any format (CSV, Excel, XML, parquet, per-person
  JSON) gets it from its full-read Run as `description.json`, built while every row is read once
  (`code/haiutils/haistep/table_card.py`); the Run fails when a question is left open.
- Rules 7 (every column, every time) and 8 (raw tables from the full read, never a sample).
- Reference: WellDoc Proj01 `b00_rawdata`, `r07_full_scan` of 280 tables in 14 drops.

## [0.1.0] — 2026-09-27

- New skill. One Task per stored table writes its Table Card: `table_card.md`,
  an executed notebook, `columns.csv`, `grain.csv`, `gotchas.csv`, pictures.
- Facts computed by `templates/describe_table.py`; meanings typed in one
  column dictionary per table family (`ref/dictionary.md`), seeded by
  `templates/seed_dictionary.py` from existing contracts, never invented.
- Reference: DrFirst Raw2AIData `b00_A_sms_rawdata`, Task
  `t12_describe_cohort_table` in each of the 8 release Jobs, dictionary
  `b00_A_sms_rawdata/src/column_dictionary.yaml` (108 columns, 85 seeded from
  the b01 ProcName contracts).
