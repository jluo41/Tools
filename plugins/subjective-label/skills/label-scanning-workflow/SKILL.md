---
name: label-scanning-workflow
description: >-
  The ORDER machine of the Scanning side of the subjective-label family: drives
  P3 Test (GOLD locked before SCORE), P4 Scan (manifest, preflight, shards,
  risk queue, reconcile), and P5 Audit (design, blind sample, findings, route,
  repair loop) as independently closable Labeling operations on
  disk, owns Run-level resume and receipts, and hands
  the crossing back to subjective-label-workflow. It owns no law: boundary,
  human gates and forbidden acts live in label-scanning. Use when running or
  resuming an evaluation, a production scan, a risk queue, an audit or a
  repair, or /label-scanning-workflow.
metadata:
  version: "0.6.0"
  last_updated: "2026-09-01"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /label-scanning-workflow · one Scanning operation at a time

Load `subjective-label` (family), `subjective-label-workflow` (phase numbers,
gates G3-G6) and `label-scanning` (the law) first. This file says only in what
ORDER the Scanning side runs, what it resumes, and which receipt each step
writes. Nothing here may start without a valid Label Handoff; the first step of each
phase binds its checksum into that phase's registry or manifest.

## Run allocation

Read `../../ref/ref-run.md` before allocating. P3-P5 use these Runs:

```text
P3  test-gold-lock → executor-predict* → executor-score* → executor-select
P4  scan-preflight → scan-shard* → risk-route → human-review → reconcile
P5  audit-sample → audit-human-gold → audit-analyze → dstar-materialize
```

The registry, production manifest, and audit design commission an episode;
they do not create umbrella Test, Scan, or Audit Runs. Write every operation's
Ticket to `runs/<RUNNAME>.yaml` and its runtime/Result envelope to
`results/<RUNNAME>/`. Point the Result at canonical artifacts without copying
protected data. Parallelize only the starred Runs after their prerequisite
closes.

## P3 Test · order

The human step is first and locks before any executor runs.

```text
GOLD
 1 bind       rehash the handoff; the Final Evaluator writes evaluation/registry.yaml
              with the fields ref-assets.md §8 lists (handoff checksum, candidates,
              wrappers, baseline, metrics, repeats, floors, selection rule)
                                                                  → evaluation/registry.yaml
 2 allocate   registry freezes; allocate test-gold-lock
 3 release    Test Custodian authorizes test text release, logs it → test/sealed/access_log.jsonl
 4 first      blind human record per test item, executor outputs hidden
                                                                  → test/final/human_first.jsonl
 5 consistency re-judge the declared repeat subset                → test/final/consistency.json
 6 lock       close test-gold-lock; T* gold locked                → test/final/human_gold.jsonl
                                                                    test/final/lock.json
SCORE
 7 predict    allocate one executor-predict per registered candidate and baseline, gold hidden;
              every Run closes before any score is computed       → evaluation/predictions/<executor>.jsonl
                                                                    evaluation/baselines/
 8 score      allocate one executor-score per closed prediction: absolute, per class,
              per region, uplift, held-out family, stability, cost, failures, intervals
                                                                  → evaluation/scorecards/<executor>.json
 9 select     allocate executor-select; apply the preregistered rule
                                                                  → evaluation/summary.md
```

Step 7 may not start before `lock.json` exists; step 8 may not start while any
candidate prediction Run is open. A registry edited after step 3 invalidates the episode.

## P4 Scan · order

```text
0 manifest    freeze the episode commission: handoff checksum · qualified executor + wrapper · route · thresholds ·
              abstention · risk rules · budget · shards · audit design
                                                            → production/run_<n>/manifest.yaml
1 preflight   allocate scan-preflight on a declared sample; preserve it even when
              a new manifest follows                        → production/run_<n>/preflight.json
2 shards      allocate one scan-shard per frozen shard; append-only, idempotent by item + Run,
              every row carries version and
              input checksums                               → production/run_<n>/attempts.jsonl
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

## P5 Audit · order

```text
0 design     freeze the episode commission: population, strata, seed, inclusion probabilities, blind protocol,
             thresholds, protected claims, frozen BEFORE any production label is
             shown to the auditor                              → audit/final_<n>/design.yaml
1 sample     allocate audit-sample; draw under the design       → audit/final_<n>/sample.jsonl
2 gold       allocate audit-human-gold; blind human judgment    → audit/final_<n>/human_gold.jsonl
3 analyze    allocate audit-analyze; weighted error with intervals; failures by route, executor, class,
             region, protected stratum                         → audit/final_<n>/findings.json
             pass · repair · rescan · semantic · limit          → audit/final_<n>/receipt.json
4 repair     declared strata repaired, versioned, then back to design under
             final_<n+1>                                       → audit/final_<n>/repairs.jsonl
5 close      on pass or accepted limit, allocate dstar-materialize
             and materialize D* with provenance shares
                                                               → corpus/final/D_star.jsonl + manifest.yaml
                                                               → audit/final_<n>/report.md
```

The repair loop is steps 4 → 0 under a new folder; a receipt is never edited.
`rescan` returns to P4 with `run_<n+1>`; `semantic` returns the job to the
family workflow, which reopens Building under a new lineage and writes the
invalidation receipt.

## Receipts this machine writes

```text
runs/<RUNNAME>.yaml            one authored operation Ticket
results/<RUNNAME>/             runtime.yaml + safe result.yaml for that operation
evaluation/registry.yaml       G3 receipt: frozen before release
test/final/lock.json           GOLD locked; SCORE may start
evaluation/summary.md          G4 receipt: qualified route or none
production/run_<n>/run_report.md   G5 receipt: one terminal per id
audit/final_<n>/receipt.json   G6 receipt: route and, on pass, the D* checksum
```

Each operation Result carries job, lineage, handoff checksum, Run address,
actor, assertions, input/output checksums, route, timestamp, and prior receipt.

## Return

Return the bound handoff checksum, current Run address or `none`, operation and
episode, files written this Run, actual allocated Run count, queue length still
owed to a human, receipt route, and exactly one next runnable operation or
named human gate.
