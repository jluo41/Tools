---
name: haipipe-insight-check
description: >-
  Check that every answered cell of an InsightBoard fits its question: each
  evidence need planned on the register with its work spec, bound in the
  page's answers.yaml to a current ok result that writes the spec's files and
  columns through a config that lists the need, and cited by a realized page
  sentence through its Evidence Item. Returns OK, GAP, STALE, UNBOUND or UNPLANNED per cell and flags a
  ✅ cell that overclaims. Read-only. The Insight workbench's "Check
  alignment" and "Review an answer" runs. Trigger: check alignment, insight
  check, does the work fit the question, overclaim, stale page, check
  evidence needs, /haipipe-insight-check.
allowed-tools: Bash, Read, Grep, Glob
metadata:
  version: "0.7.0"
  last_updated: "2026-10-05"
  # version history: ./CHANGELOG.md
---

# /haipipe-insight-check · does the answer fit the ask?

The contract is `../haipipe-insight/ref/evidence-needs.md` (§ 4 the verdicts).
The check is mechanical and read-only: it never edits a page, a binding, a
result or a register cell.

## Run it

An Insight Block (`../haipipe-insight/ref/block-contract.md`):

```bash
.venv/bin/python Tools/plugins/haipipe-toolkit/skills/2_theme/insight/haipipe-insight-check/ref/check_block.py <Block>
    --strict               # 🟡 and STALE cells fail too
    --write                # the grid also goes to <Block>/meta/status.md
```

It checks every question.md (question, name, ask, Why now, What would answer it,
partitions and power, live needs and their specs, cites one level below, script and
SPEC line; retired needs are kept and never run or cited), prints question-review
suspects as notes (Q1 the ask joins two questions, Q2 a need no judge reads, Q4 a cause
word in a Data or Information ask, Q6 two questions compute the same table;
haipipe-insight-question judges them), and computes every question × run cell
(`<dataset>_<partition>`): — not asked · 🚫 refused · 🟡 owed · ✅ <YYMMDD> (the page's
latest CHECK closed CLOSE after its results' content_since, results-read current, every
need cited) · STALE (the script, question file, shared src, or a result it read changed).
Exit 1 on any problem.

A board made before it (registers and a task Block):

```bash
.venv/bin/python Tools/plugins/haipipe-toolkit/skills/2_theme/insight/haipipe-insight-check/ref/check_evidence.py <board>
    --format text|json     # text (default): counts, then every cell that is not OK
    --strict               # UNPLANNED cells fail too
    --question <QID>       # one question
    --page <L><NN>-<partition>   # one page
```

Exit 0: no overclaim. Exit 1: a `✅` cell is GAP, STALE or UNBOUND (or, under
`--strict`, a cell is UNPLANNED). Exit 2: not an InsightBoard.

## What it checks, per cell that names a page

```text
planned   the question has live need lines; every compute need has all seven
          work-spec keys and pass:; kinds are legal at its level; cite and
          judge have from:, a cite stays within the level rule
bound     the page's answers.yaml has the question and every live need
fit       compute: the ticket is in runs/, its runtime.yaml says ok, every spec
          output file is bound and exists, every spec column is in its CSV
          header or JSON keys, the spec's cut is the page's partition, and the
          config the ticket calls lists the need id under answers: · cite: the
          cited page exists and binds the borrowed need · refused: only on a 🟡
          or 🚫 cell, and bound to its probe run
cited     a realized Page sentence carries the need: through an Evidence Item
          whose **Need** names it, a Bullet `Evidence: none · judge <id>`, or an
          inline [<id>] tag on an older page; an item's Artifact is a bound file
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

- `ref/check_evidence.py` · the check of a register board made before Insight Blocks
- `ref/check_block.py` · the check of an Insight Block
- `tests/test_check_block.py` · a toy Insight Block, a fit run and each way it breaks
- `tests/test_check_evidence.py` · a fixture board, one fit answer and each way it breaks
