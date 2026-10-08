# 2026-09-04 · D1 workflow fresh-context behavior test

This is the dated fresh-context behavioral receipt accepted by the Workflow
Table coverage contract. It is not a claim that the separate full
`/field-test` method (live target, preregistered ledger, settlement, and
scorecard) was run.

## Scenario

A fresh agent loaded the installed `haipipe-discovery` door, resolved the D1
Inquiry phase and canonical Workflow Table, and created a temporary Discovery
Folder for this bounded question:

> What architectural contribution did *Attention Is All You Need* make?

The supplied canonical Subject was arXiv `1706.03762`. The fixture lived at
`/private/tmp/haipipe-discovery-field-test.8PDBMr`; no repository source file
was changed by the test.

## Observed behavior

| Gate | Observation |
|---|---|
| BJTR | explicit `b01_` / `j01_` / `t01_` / `r01_` names |
| SCOPE | `source-reading` question and admission boundary frozen |
| PREPARE | skipped with `instrument.needed: false`; no empty `scripts/` |
| ACQUIRE | one executable Run and one same-stem complete Result for the Subject |
| Duplicate | unchanged arXiv identity and intent reused `r01`; no `r02` |
| Bib | one Result Bib projected into the derived aggregate |
| SYNTHESIZE | not falsely completed; Page receipts were absent |
| CLOSE | not entered; human citation verification remained pending |

## Deterministic evidence

```text
runs: blocked=0 complete=1 planned=0 running=0 superseded=0 unresolved=0
citation-verification: invalid=0 pending=1 verified=0
STRUCTURE_OK discovery-page-and-run contract · CLOSURE_HELD citation-verification=1
RUN_COUNT_BEFORE=1
RUN_COUNT_AFTER=1
R02_EXISTS=false
```

The ticket passed `bash -n`, was executable, Result Bib equaled the derived
aggregate, the legacy root `evidence/` lane stayed absent, 31 `paper_runs`
unit tests passed, and the Folder-contract checker reported zero findings.

## Verdict

PASS for `haipipe-discovery` + `haipipe-discovery-inquiry`. The test confirms
correct Run cardinality, duplicate reuse, honest verification debt, and the
Page-before-D1 closure boundary. It does not field-test every source/review/
idea worker; their coverage rows remain `?`.
