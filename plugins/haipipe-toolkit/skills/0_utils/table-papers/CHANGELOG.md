# Changelog

## 0.1.0 · 2026-10-03 · The shared Related Paper rule (JL 261003)

- The eight-column table the Design and Insight workbenches already kept, written down as
  one rule: `group · role · key · paper · venue · doi · why here · pdf`, plus the role
  `practice` and a `doi` cell that may hold the https page of a work with no DOI.
- `ref/check_papers_table.py`: offline rules, and `--online` looks every DOI up on
  OpenAlex, Crossref and DataCite (OpenAlex mapped an arXiv DOI to another work; DataCite
  holds arXiv DOIs). Design (76 rows) and Insight (114 rows) pass; Insight warns that
  `all methods (design)` has no ★.
- The renderer moved from `servers/workbench-design/designboard.py` to
  `servers/workbench-shared/related_papers.py`; Design re-exports it under its old names,
  Insight imports it, and Guide › Related Paper renders a family's `papers_table`.
