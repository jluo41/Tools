<!-- Folded from the haipipe-labeling-scanning skill on 2026-10-07 (JL): the Scanning step order,
     its text kept, with its own name updated. Its law is ../SKILL.md. -->

# /haipipe-labeling-scanning · the Scanning step order

Load `haipipe-labeling` (family), `haipipe-labeling-workflow` (the Run Spec
graph and Routes), and `haipipe-labeling-scanning` (semantic authority and restrictions)
first. **A Workflow is a list of Runs.** The operation names below are Run
Types used by the shared Workflow's Run Specs. This file gives their
Scanning-side order; each Run's internal Steps are in its view skill; the source Run Spec owns its
commission, actor, entry/exit gates, Route, and completion rule. P3-P5 are
compatibility capability tags only and do not create a separate frontier.
Every Scanning Run binds the exact Label Handoff version in its Ticket.

## Run allocation

Read `../../haipipe-labeling-building/ref/ref-run.md` before allocating. P3-P5 use these Runs:

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
step  Run Type                     view                      skill
14    test-gold-lock           Quality › Test            haipipe-labeling-test
15    executor-predict*        Quality › Evaluation      haipipe-labeling-evaluation
16    executor-score*          Quality › Evaluation      haipipe-labeling-evaluation
17    executor-select          Quality › Evaluation      haipipe-labeling-evaluation
18    scan-preflight           Delivery › Scan           haipipe-labeling-scan
19    scan-shard*              Delivery › Scan           haipipe-labeling-scan
20    risk-route               Delivery › Scan           haipipe-labeling-scan
21    human-review             Delivery › Scan           haipipe-labeling-scan
22    reconcile                Delivery › Scan           haipipe-labeling-scan
23    audit-sample             Quality › Audit           haipipe-labeling-audit
24    audit-human-gold         Quality › Audit           haipipe-labeling-audit
25    audit-analyze            Quality › Audit           haipipe-labeling-audit
26    dstar-materialize        Delivery › Final labels   haipipe-labeling-final-labels
```

`*` one per candidate model (15, 16) or corpus shard (19), run in parallel after
their prerequisite closes. The audit repair loop and its routes are in
`haipipe-labeling-audit`.

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
