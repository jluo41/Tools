# haipipe-insight-check · version history

## 0.5.0 · 2026-10-02 · Question file v2 (JL 261002)

- `ref/check_instance.py` reads question file v2: requires question, name, ask, Why now and What would answer it; the compute spec is the register's (cut, unit, measure, by, uncertainty, rivals, output); retired needs are history; a cite of a retired need is a problem; power uses the board-wide smallest effect or a reasoned override. Coverage and cause words are no longer problems: Q1, Q2, Q4 and Q6 suspects are notes for the question review.
- New `tests/test_carry_over.py` (the carry-over on a toy register board); `tests/test_check_instance.py` moved to v2, with retired needs, json keys, the effect override, one division per partition and a new Instance board.
- STALE follows the shared modules a question's scripts import, not the whole `src/` (test: a run rests only on the modules it imports).
- A retired question names its successors (`superseded_by`), keeps no scripts, and computes "—" everywhere; a cite of any need of a retired question is a problem.
- STALE follows only the thresholds sections a question's code names (test added).

## 0.4.0 · 2026-10-02 · Prototype and Instance boards (JL 261002)

- New `ref/check_instance.py`: checks a Prototype's questions and computes every cell of one Instance from its runs and page CHECK records (— · 🚫 · 🟡 · ✅ <YYMMDD> · STALE). Tests: `tests/test_check_instance.py`, 10 cases (a fit run; an unnamed column; one row per input row; a changed script is STALE; an underpowered partition refused before any contrast; an unasked page folder; a causal or uncovered ask; a cite on the same rung; a run before agreement; a checked current page settles). Both suites: 25 passed.

## 0.3.0 · 2026-10-02 · The question owns its run (JL 261002)

- `ref/check_evidence.py` enforces the hard rules: a missing ask, a causal Data/Information ask, an `**Ask covered**:` phrase not in the ask or an ask word no phrase covers, a compute spec's measure/by without an ask phrase, and a run config serving more than one question are each a GAP. Tests: 15 passed.

## 0.2.0 · 2026-10-01 · Work specs and the page flow (JL 261001)

- Reads the work spec: required output files and columns come from the spec; checks the spec's cut, that the ticket's config lists the need id, that a refusal is bound to its probe run, and citations through the page's Evidence Items and realized sentences (inline tags still read on older pages). 11 tests.

## 0.1.0 · 2026-10-01 · First version (JL 261001)

- `ref/check_evidence.py <board>`: one verdict per answered register cell (OK · GAP · STALE · UNBOUND · UNPLANNED) from the register's evidence needs, the page's `answers.yaml`, its tickets, results (status, files, fields) and text citations; a ✅ cell that fails is an overclaim (exit 1). Reads both row-major and transposed Queue grids.
- `tests/test_check_evidence.py`: a fixture board, one fit answer and each way it breaks (uncited, missing field, reasoned compute need, stale, unbound, illegal kind).
