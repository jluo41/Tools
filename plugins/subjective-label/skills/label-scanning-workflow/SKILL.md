---
name: label-scanning-workflow
description: >-
  The Scanning step order of the subjective-label Workflow: which Run comes
  next, allocation, receipts, and repair routes for test, production, and
  audit work; each Run's own steps live in its view skill. P3-P5 are compatibility capability tags, not
  lifecycle owners. The shared Workflow Definition owns the Run graph and
  Routes; this guide owns no semantic law, gate authority, or separate
  frontier. Use when deciding which Scanning Run comes next, allocating a Run
  address, or checking Scanning receipts, or /label-scanning-workflow.
metadata:
  version: "0.8.0"
  last_updated: "2026-09-29"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /label-scanning-workflow · the Scanning step order

Load `subjective-label` (family), `subjective-label-workflow` (the Run Spec
graph and Routes), and `label-scanning` (semantic authority and restrictions)
first. **A Workflow is a list of Runs.** The operation names below are Run
Types used by the shared Workflow's Run Specs. This file gives their
Scanning-side order; each Run's internal Steps are in its view skill; the source Run Spec owns its
commission, actor, entry/exit gates, Route, and completion rule. P3-P5 are
compatibility capability tags only and do not create a separate frontier.
Every Scanning Run binds the exact Label Handoff version in its Ticket.

## Run allocation

Read `../label-building/ref/ref-run.md` before allocating. P3-P5 use these Runs:

```text
P3 (compat tag)  test-gold-lock → executor-predict* → executor-score* → executor-select
P4 (compat tag)  scan-preflight → scan-shard* → risk-route → human-review → reconcile
P5 (compat tag)  audit-sample → audit-human-gold → audit-analyze → dstar-materialize
```

The registry, production manifest, and audit design commission an episode;
they do not create umbrella Test, Scan, or Audit Runs. Write every operation's
Ticket to `<Page>/runs/<RUNNAME>.yaml` and its runtime/Result envelope to
`<Page>/results/<RUNNAME>/`, beside `labeling/`. Point the Result at canonical artifacts without copying
protected data. Parallelize only the starred Runs after their prerequisite
closes.

## Steps and their view skills

Each Run's own steps live in the one skill of the workbench view that shows it
(JL 260929: one skill per view, never shared). This file keeps only the order.

```text
step  run                          view                      skill
14    run-test-gold-lock           Quality › Test            subjective-label-test
15    run-executor-predict*        Quality › Evaluation      subjective-label-evaluation
16    run-executor-score*          Quality › Evaluation      subjective-label-evaluation
17    run-executor-select          Quality › Evaluation      subjective-label-evaluation
18    run-scan-preflight           Delivery › Scan           subjective-label-scan
19    run-scan-shard*              Delivery › Scan           subjective-label-scan
20    run-risk-route               Delivery › Scan           subjective-label-scan
21    run-human-review             Delivery › Scan           subjective-label-scan
22    run-reconcile                Delivery › Scan           subjective-label-scan
23    run-audit-sample             Quality › Audit           subjective-label-audit
24    run-audit-human-gold         Quality › Audit           subjective-label-audit
25    run-audit-analyze            Quality › Audit           subjective-label-audit
26    run-dstar-materialize        Delivery › Final labels   subjective-label-final-labels
```

`*` one per candidate model (15, 16) or corpus shard (19), run in parallel after
their prerequisite closes. The audit repair loop and its routes are in
`subjective-label-audit`.

## Receipts this machine writes

```text
<Page>/runs/<RUNNAME>.yaml     one authored operation Ticket, beside labeling/
<Page>/results/<RUNNAME>/      runtime.yaml + safe result.yaml for that operation
evaluation/registry.yaml       input bound by test-gold-lock; G3 is its compatibility predicate
test/final/lock.json           GOLD locked; SCORE may start
evaluation/summary.md          executor-select Run Result: qualified route or none
production/run_<n>/run_report.md   reconcile Run Result: one terminal per id
audit/final_<n>/receipt.json   audit-analyze Run Result: route and, on pass, the D* version
```

Each operation Result carries job, lineage, handoff version, Run address,
actor, assertions, input and output paths, route, timestamp, and prior receipt.

## Return

Return the bound handoff version, current Run address or `none`, Run Spec/operation and
episode, files written this Run, actual allocated Run count, queue length still
owed to a human, receipt Route, and exactly one next runnable Run Spec or
named human gate.
