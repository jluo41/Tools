# label-scanning · CHANGELOG

## 0.6.0 · 2026-09-01

Split P3-P5 into human-gold, per-executor predict/score, selection, preflight,
per-shard scan, routing/review/reconcile, and audit/materialization operations.
Test, Scan, and Audit now group Runs without becoming umbrella Runs.

## 0.5.1 · 2026-09-01

Name the P3/P4/P5 operations Qualification Test, Production Scan, and Final
Audit Runs; candidate predictions are internal attempts, not separate Runs.

## 0.5.0 · 2026-08-30

First versioned edition of the three-layer family (goal session, Stages A+B). LAW doors (`label-building`, `label-scanning`), ORDER machines (`label-building-workflow`, `label-scanning-workflow`), and the CROSSING (`subjective-label-workflow`: P0-P5, G0-G6, handoff, invalidation). Round unit + register + rendered views in `ref-assets.md` §1/§3/§6a; exercised by `fixtures/job-mini/` and its board `fixtures/job-mini-board-260830/`. Cold-run defects fixed same day: G2/G3 split (stop vs freeze signature), P3 single authority artifact, registry single definition with the Final Evaluator as writer, use-vs-define rule for phase numbers.
