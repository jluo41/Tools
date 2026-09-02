# subjective-label-workflow · CHANGELOG

## 0.8.0 · 2026-09-01

Publish the first concrete Phase × Run Map under the generic `haipipe-run`
schema, joining P0-P5 purpose, episode, operations, symbolic count, human gate,
and closing handoff in one table.

## 0.7.0 · 2026-09-01

Route one exact P0-P5 operation at a time through the 25-kind Labeling Run
Profile. Treat Round/Test/Scan/Audit as episodes, keep bare human actions as
gates, and return actual versus assumed planned counts separately.

## 0.6.0 · 2026-09-01

Add the phase-owned Labeling Run Profile: P1/P3/P4/P5 own four addressable
operations, while P0/P2 remain job transitions and candidate predictions stay
internal Qualification Test attempts.

## 0.5.0 · 2026-08-30

First versioned edition of the three-layer family (goal session, Stages A+B). LAW doors (`label-building`, `label-scanning`), ORDER machines (`label-building-workflow`, `label-scanning-workflow`), and the CROSSING (`subjective-label-workflow`: P0-P5, G0-G6, handoff, invalidation). Round unit + register + rendered views in `ref-assets.md` §1/§3/§6a; exercised by `fixtures/job-mini/` and its board `fixtures/job-mini-board-260830/`. Cold-run defects fixed same day: G2/G3 split (stop vs freeze signature), P3 single authority artifact, registry single definition with the Final Evaluator as writer, use-vs-define rule for phase numbers.
