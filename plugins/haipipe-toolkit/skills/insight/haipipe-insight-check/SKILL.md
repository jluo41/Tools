---
name: haipipe-insight-check
description: >-
  Check that every answered cell of an InsightBoard fits its question: each
  evidence need planned on the register, bound in the page's answers.yaml to
  files of a current ok result that carry its pass condition, and cited in the
  page text. Returns OK, GAP, STALE, UNBOUND or UNPLANNED per cell and flags a
  ✅ cell that overclaims. Read-only. The Insight workbench's "Check
  alignment" and "Review an answer" runs. Trigger: check alignment, insight
  check, does the work fit the question, overclaim, stale page, check
  evidence needs, /haipipe-insight-check.
allowed-tools: Bash, Read, Grep, Glob
metadata:
  version: "0.1.0"
  last_updated: "2026-10-01"
  # version history: ./CHANGELOG.md
---

# /haipipe-insight-check · does the answer fit the ask?

The contract is `../haipipe-insight/ref/evidence-needs.md` (§ 4 the verdicts).
The check is mechanical and read-only: it never edits a page, a binding, a
result or a register cell.

## Run it

```bash
.venv/bin/python Tools/plugins/haipipe-toolkit/skills/insight/haipipe-insight-check/ref/check_evidence.py <board>
    --format text|json     # text (default): counts, then every cell that is not OK
    --strict               # UNPLANNED cells fail too
    --question <QID>       # one question
    --page <L><NN>-<partition>   # one page
```

Exit 0: no overclaim. Exit 1: a `✅` cell is GAP, STALE or UNBOUND (or, under
`--strict`, a cell is UNPLANNED). Exit 2: not an InsightBoard.

## What it checks, per cell that names a page

```text
planned   the question has live need lines; kinds are legal at its rung;
          compute has pass:, cite and judge have from:, a cite stays within
          the rung rule
bound     the page's answers.yaml has the question and every live need
fit       compute: the ticket is in runs/, its runtime.yaml says ok, each file
          exists, each field is a column of the CSV header or a dotted key of
          the JSON · cite: the cited page exists and binds the borrowed need ·
          refused: only on a 🟡 or 🚫 cell
cited     each need's id appears as [<QID>.E<n>] in the page text (a cite need
          may carry the borrowed id)
current   no bound result ended after the page's results-read: line
agreed    reported, never failed: a ⬜ Needs agreed line is a note
```

## Who runs it

A person, or an agent other than the one that wrote the page (make and judge
apart): `haipipe-insight-bind` runs it after binding, the Report run's
reviewer runs it before a cell may settle ✅, and a rerun of any ticket makes
it worth running again, because a newer result turns its page STALE.

## Reading the result

- **GAP** names each need and what is missing. A compute need answered by
  pointing at another page's prose shows here as "binds ticket and files".
- **STALE** names the ticket that ended after the reading: reread and rewrite
  the page, then update `results-read:`.
- **UNBOUND** means the page never recorded which file answers which need.
- **UNPLANNED** is a question from before the contract: plan it with
  `haipipe-insight-evidence-plan`.

A ✅ cell that fails is an overclaim. The register owner drops it to 🟡 until
the page is fixed; this skill only reports it.

## Files

- `ref/check_evidence.py` · the check
- `tests/test_check_evidence.py` · a fixture board, one fit answer and each way it breaks
