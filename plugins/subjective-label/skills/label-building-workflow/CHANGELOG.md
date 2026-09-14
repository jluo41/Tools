# label-building-workflow · CHANGELOG

## 0.8.0 · 2026-09-13

Document the exact read-only `status` invocation, make optional P0 sidecars
explicitly skippable before G0, and record that `create` now allocates the one
completed `rlNN_corpus-contract_*` envelope without speculative Runs.

## 0.7.0 · 2026-09-13

Separate the P0 phase frontier from its first blocked gate, which is reported
unambiguously as `G0 · human meaning confirmation`.

## 0.6.0 · 2026-09-01

Allocate one Run per independently closable P0-P2 operation through root
Ticket/Result envelopes. Keep the Card/checkpoint folder as a round episode,
and expose the missing live allocator honestly while the planner remains safe.

## 0.5.5 · 2026-09-01

Allocate the job-wide Run address and `runtime.yaml` only when a person releases
the round Card; return and resume by the same Calibration Round Run identity.

## 0.5.0 · 2026-08-30

First versioned edition of the three-layer family (goal session, Stages A+B). LAW doors (`label-building`, `label-scanning`), ORDER machines (`label-building-workflow`, `label-scanning-workflow`), and the CROSSING (`subjective-label-workflow`: P0-P5, G0-G6, handoff, invalidation). Round unit + register + rendered views in `ref-assets.md` §1/§3/§6a; exercised by `fixtures/job-mini/` and its board `fixtures/job-mini-board-260830/`. Cold-run defects fixed same day: G2/G3 split (stop vs freeze signature), P3 single authority artifact, registry single definition with the Final Evaluator as writer, use-vs-define rule for phase numbers.
