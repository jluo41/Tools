# haipipe-insight-check · version history

## 0.1.0 · 2026-10-01 · First version (JL 261001)

- `ref/check_evidence.py <board>`: one verdict per answered register cell (OK · GAP · STALE · UNBOUND · UNPLANNED) from the register's evidence needs, the page's `answers.yaml`, its tickets, results (status, files, fields) and text citations; a ✅ cell that fails is an overclaim (exit 1). Reads both row-major and transposed Queue grids.
- `tests/test_check_evidence.py`: a fixture board, one fit answer and each way it breaks (uncited, missing field, reasoned compute need, stale, unbound, illegal kind).
