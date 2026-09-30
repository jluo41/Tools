---
name: subjective-label-scan
description: >-
  The Delivery › Scan view skill of the subjective-label family: it
  labels the whole corpus under the frozen handoff with the selected executor, routes risky items to human review, and reconciles one terminal label per item. Every Run in this view names this skill, and no other view uses it.
  Use for production scan, scan-preflight, scan-shard, risk-route, human-review, reconcile, risk queue, labeling the corpus, or /subjective-label-scan.
metadata:
  version: "0.1.0"
  last_updated: "2026-09-29"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /subjective-label-scan · Delivery Space › Scan

This skill owns the Runs of the labeling workbench's Delivery › Scan
view: every Run card there names it, and no other view uses it (JL 260929:
one skill per view). Load `subjective-label` (the family door),
`subjective-label-workflow` (the Run graph) and `label-scanning` (who decides what) first. Which Run
comes before and after these is in `label-scanning-workflow`.

## Runs in this view

```text
step  Run Type                     state
18    scan-preflight       not built
19    scan-shard           not built · one per frozen shard
20    risk-route           not built
21    human-review         not built
22    reconcile            not built
```

A new Run uses `run-labeling-<operation>-<MMDD>-<target>` on disk and
on the page. Older short-named Tickets remain readable. Its Ticket is
`<Page>/runs/<run>.yaml`
and its Result `<Page>/results/<run>/`, beside `labeling/`.

```text
0 manifest    freeze the episode commission: handoff version · qualified executor + wrapper · route · thresholds ·
              abstention · risk rules · budget · shards · audit design
                                                            → production/run_<n>/manifest.yaml
1 preflight   allocate scan-preflight on a declared sample; preserve it even when
              a new manifest follows                        → production/run_<n>/preflight.json
2 shards      allocate one scan-shard per frozen shard; append-only, idempotent by item + Run,
              every row carries the executor, wrapper
              and input versions                              → production/run_<n>/attempts.jsonl
3 route       allocate risk-route after every shard closes; declared disagreement,
              uncertainty, novelty, drift, protected strata,
              failures, shared-error neighborhoods          → production/run_<n>/risk_queue.jsonl
4 review      allocate human-review; human decisions on the frozen queue, append-only
                                                            → production/run_<n>/human_final.jsonl
5 reconcile   allocate reconcile; exactly one terminal disposition per in-scope item
                                                            → production/run_<n>/terminal_labels.jsonl
                                                            → production/run_<n>/run_report.md
```

Resume `scan-shard` at its first unattempted item, `human-review` at the first
queue row with no human final, and `reconcile` at the first id with no terminal
row. A changed threshold, executor, or wrapper creates a new production episode
and new downstream Runs.

## Return

Return the Run address or `none`, the files written, and exactly one next
runnable Run or named human gate.
