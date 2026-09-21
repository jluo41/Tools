# label-building-workflow · CHANGELOG

## 0.10.0 · 2026-09-20

Clarify that local CLI and Board receipts are caller-attested, not identity
authentication, and document the guarded upgrade path for previously bound G0
receipts. Add setup-only skill routing, distinguish class values from separate
constructs, and state that a scratch check needs a temporary Page and writes
temporary artifacts because there is no non-writing dry-run command; remove
the entire scratch workspace afterward. Correct repository-root script paths
and mark the historical example corpus as external. The engine now carries
eligible corpus rows only into Page lanes, resolves managed v2 inputs against
the canonical eligible corpus, and fails closed on missing or unknown job
schemas.

## 0.9.0 · 2026-09-16

Match the built engine. P0 names `engine/fence_source.py` as the way to build
the fenced source that `create` imports (seeded sealed draw, optional
stratification, `population_status` on every row, G_00 from config meanings),
records the stronger `status` checks (no raise, `integrity_errors`, `hold`,
G0 bound to the current P0 files), and adds the Board `Confirm meaning` button
as a second channel into the same `confirm_meaning`. P1 now says what
`engine/calibration.py` builds (CARD and PREPARE for round_01's random draw,
JUDGE events) and what it does not (weak-prelabel, LEARN, MEASURE, CLOSE, and
later rounds), so the machine stops after round_01 is judged. The
`sessions/events.jsonl` shape and the exact change types are documented. P0
step 5 now has a real writer, `engine/embedding_build.py build`: development
items only, response-then-context input, a versioned
`cache/embeddings/<version>/` folder, and one `rlNN_embedding-build_<version>`
Run, not gated on G0 because a vector sets no label. The embedder is chosen
from an open-weight catalog, one folder and one Run per model.

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
