# label-building · CHANGELOG

## 0.6.0 · 2026-09-01

Split P0-P2 Building work into contract, search, seed, reservation, embedding,
round preparation/prelabel/human/learn/measure/close, and handoff operations.
A round is now an episode; release, STOP, and freeze signature remain gates.

## 0.5.1 · 2026-09-01

Define a released round as a Calibration Round Run. A proposed Card remains
planning; human release allocates the Run and P0/P2 allocate none.

## 0.5.0 · 2026-08-30

First versioned edition of the three-layer family (goal session, Stages A+B). LAW doors (`label-building`, `label-scanning`), ORDER machines (`label-building-workflow`, `label-scanning-workflow`), and the CROSSING (`subjective-label-workflow`: P0-P5, G0-G6, handoff, invalidation). Round unit + register + rendered views in `ref-assets.md` §1/§3/§6a; exercised by `fixtures/job-mini/` and its board `fixtures/job-mini-board-260830/`. Cold-run defects fixed same day: G2/G3 split (stop vs freeze signature), P3 single authority artifact, registry single definition with the Final Evaluator as writer, use-vs-define rule for phase numbers.
