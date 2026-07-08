haipipe-insight — Changelog
===========================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.

## [3.1.0] — 2026-07-05

- Narrative layer references DELETED throughout (JL skill-set review: "现在已经没有narrative了，insight只会被probe call。直接都删掉。"): caller model is now probe (Deposit step) or the user directly; narrative rows dropped from the flow diagram, boundary block, and relation table; application row is READ-side only.
- `.insight-console.yaml` routing signal removed from feedback capture (JL: "删掉吧"; no insight skill ever created that file).
- views/ line reworded to the dual-mode contract (JL: "auto是在subagent call这个skill的时候，会走auto"): co-pilot with a human, --auto when a subagent calls (was "auto: ...", a promise nothing implemented).
- Stale roster line fixed: K reviewer entry no longer advertises a "probe gate" (contradicted this file's own Review Funnel since 3.0.0).
- "Three Jobs" heading corrected to Five Jobs; Step 5 accumulation check relabeled Job 3 (was Job 2).
- Path depth fixes: ../play/README.md, ../scripts/export_okf.py.
- Changelog reordered newest-first (was 2.0.0 → 1.0.0 → 2.6.0 → 3.0.0).
- ask-session REMOVED as a review scope (JL D1 follow-up: "delete it."): command signature, path-based auto-detect row, and Step 2a detection dropped; application keeps only READ-side citations and the outbound question redirect.
- Write boundary softened per JL E5 ruling (option A): permanent artifacts only under insights/; the INSIGHT_REVIEW.yaml checklist lands in the reviewed scope folder (matches dogfood practice).

## [3.0.0] — 2026-06-22

- DIKW model recut to in-sample-vs-generalization (JL). D/I describe ONE named dataset (require `dataset:`, no p/CI); K is the generalization layer where p/CI/confidence live and has NO probe gate (low-confidence and negative K are recorded); W reads K confidence to set risk posture. Removed the I->K controlled-comparison-probe gate. Updated dikw-boundaries, insight-md-schema, K writer, K/D/I reviewers, review specialist, agents README.

## [2.6.0] — 2026-06-20

- renamed user-facing archive flow to review/apply.

## [2.0.0] — 2026-06-11

- DIKW producer partition; post-file accumulation check; 3-job design (route + check + dashboard); step-by-step protocol.

## [1.0.0] — 2026-05-31

- baseline metadata added.
