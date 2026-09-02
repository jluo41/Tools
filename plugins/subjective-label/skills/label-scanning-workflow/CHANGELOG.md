# label-scanning-workflow · CHANGELOG

## 0.6.0 · 2026-09-01

Allocate and order granular P3-P5 Run envelopes, including one prediction and
score per candidate and one production Run per shard. Preserve gold-before-
prediction, all-predictions-before-score, blind audit, and phase promotion gates.

## 0.5.1 · 2026-09-01

Add Run allocation and `runtime.yaml` rules for Qualification Test, Production
Scan, and Final Audit; normalize candidate executor work to internal attempts.

## 0.5.0 · 2026-08-30

First versioned edition of the three-layer family (goal session, Stages A+B). LAW doors (`label-building`, `label-scanning`), ORDER machines (`label-building-workflow`, `label-scanning-workflow`), and the CROSSING (`subjective-label-workflow`: P0-P5, G0-G6, handoff, invalidation). Round unit + register + rendered views in `ref-assets.md` §1/§3/§6a; exercised by `fixtures/job-mini/` and its board `fixtures/job-mini-board-260830/`. Cold-run defects fixed same day: G2/G3 split (stop vs freeze signature), P3 single authority artifact, registry single definition with the Final Evaluator as writer, use-vs-define rule for phase numbers.
