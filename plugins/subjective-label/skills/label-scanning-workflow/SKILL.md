---
name: label-scanning-workflow
description: >-
  The ORDER machine of the Scanning side of the subjective-label family: drives
  P3 Test (GOLD locked before SCORE), P4 Scan (manifest, preflight, attempts,
  risk queue, reconcile), and P5 Audit (design, blind sample, findings, route,
  repair loop) as runs on disk, owns run-level resume and run receipts, and hands
  the crossing back to subjective-label-workflow. It owns no law: boundary,
  human gates and forbidden acts live in label-scanning. Use when running or
  resuming an evaluation, a production scan, a risk queue, an audit or a
  repair, or /label-scanning-workflow.
---

# /label-scanning-workflow · one run at a time, one-way

Load `subjective-label` (family), `subjective-label-workflow` (phase numbers,
gates G3-G6) and `label-scanning` (the law) first. This file says only in what
ORDER the Scanning side runs, what it resumes, and which receipt each step
writes. Nothing here may start without a valid Label Handoff checksum bound
in the run's manifest.

## P3 Test · order

The human step is first and locks before any executor runs.

```text
GOLD
 1 bind       rehash the handoff; write evaluation/registry.yaml binding its checksum,
              candidate executors, families, wrappers, baseline, metrics, repeats,
              quality floors, selection rule                      → evaluation/registry.yaml
 2 release    Test Custodian authorizes test text release, logs it → test/sealed/access_log.jsonl
 3 first      blind human record per test item, executor outputs hidden
                                                                  → test/final/human_first.jsonl
 4 consistency re-judge the declared repeat subset                → test/final/consistency.json
 5 lock       T* gold locked                                      → test/final/human_gold.jsonl
                                                                    test/final/lock.json
SCORE
 6 predict    each registered executor and the baseline run independently, gold hidden;
              every run closes before any score is computed       → evaluation/predictions/<run>.jsonl
                                                                    evaluation/baselines/
 7 score      absolute, per class, per region, uplift, held-out family, stability, cost,
              failures, with intervals                            → evaluation/scorecards/<executor>.json
 8 select     apply the preregistered rule; qualified route or none → evaluation/summary.md
```

Step 6 may not start before `lock.json` exists; step 7 may not start while any
prediction run is open. A registry edited after step 2 invalidates the test.

## P4 Scan · order

```text
1 manifest    handoff checksum · qualified executor + wrapper · route · thresholds ·
              abstention · risk rules · budget · shards · audit design
                                                            → production/run_<n>/manifest.yaml
2 preflight   the frozen route on a declared preflight sample; preserved even when
              a new manifest follows                        → production/run_<n>/preflight.json
3 attempts    append-only, idempotent by item + run, every row carries version and
              input checksums                               → production/run_<n>/attempts.jsonl
4 route       declared disagreement, uncertainty, novelty, drift, protected strata,
              failures, shared-error neighborhoods          → production/run_<n>/risk_queue.jsonl
5 review      human decisions on the queue, append-only     → production/run_<n>/human_final.jsonl
6 reconcile   exactly one terminal disposition per in-scope item
                                                            → production/run_<n>/terminal_labels.jsonl
7 report      route shares, dispositions, cost, failures    → production/run_<n>/run_report.md
```

Resume rule: the open item is the first in-scope id with no terminal row;
attempts already written are never re-run under the same manifest. A changed
threshold, executor, or wrapper is a new `run_<n+1>` with its own preflight.

## P5 Audit · order

```text
1 design     population, strata, seed, inclusion probabilities, blind protocol,
             thresholds, protected claims, frozen BEFORE any production label is
             shown to the auditor                              → audit/final_<n>/design.yaml
2 sample     drawn under the design                            → audit/final_<n>/sample.jsonl
3 gold       blind human judgment per sampled item             → audit/final_<n>/human_gold.jsonl
4 compare    weighted error with intervals; failures by route, executor, class,
             region, protected stratum                         → audit/final_<n>/findings.json
5 route      pass · repair · rescan · semantic · limit          → audit/final_<n>/receipt.json
6 repair     declared strata repaired, versioned, then back to step 1 under
             final_<n+1>                                       → audit/final_<n>/repairs.jsonl
7 close      on pass or accepted limit: D* materialized with provenance shares
                                                               → corpus/final/D_star.jsonl + manifest.yaml
                                                               → audit/final_<n>/report.md
```

The repair loop is steps 6 → 1 under a new folder; a receipt is never edited.
`rescan` returns to P4 with `run_<n+1>`; `semantic` returns the job to the
family workflow, which reopens Building under a new lineage and writes the
invalidation receipt.

## Receipts this machine writes

```text
evaluation/registry.yaml       G3 receipt: frozen before release
test/final/lock.json           GOLD locked; SCORE may start
evaluation/summary.md          G4 receipt: qualified route or none
production/run_<n>/run_report.md   G5 receipt: one terminal per id
audit/final_<n>/receipt.json   G6 receipt: route and, on pass, the D* checksum
```

Each receipt carries job, lineage, handoff checksum, run id, actor, assertion
results, input and output checksums, route, timestamp, previous receipt.

## Return

Return the bound handoff checksum, the run id and its open step, the files
written this run, the queue length still owed to a human, the receipt route,
and exactly one next runnable step.
