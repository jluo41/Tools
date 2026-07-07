haipipe-application — Changelog
===============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [1.0.0] — 2026-05-31

- baseline.

## [2.0.0] — 2026-06-22

- restructured around intervention lifecycle.

## [3.0.0] — 2026-06-23

- rename stages to paper vocabulary; add venue; venue-driven stage requirements.

## [4.0.0] — 2026-06-23

- remove format specialists (message/ui/report) — absorbed into venue profiles; remove context + plan skills — absorbed into lifecycle orchestrator and claims stage; single draft skill reads venue profile.

## [5.0.0] — 2026-07-06

- FAMILY ROLLUP: claims-before-venue spine (R1); minimap retired into display, section-edit venue-gated (R2); ask retired to _archive/, enter console is the entry (R3); full DPRC 2-phase/ bucket — draft/probe/revise workers NEW, gate renamed check (R4). Folderless probe adopted: per-stage _PROBE/PPNN cards + 1-probe-plans/README.md index, plan-from-need + confirmed enum retired. Buckets renumbered 0-enter/1-lifecycle/2-phase/3-build-deploy/4-iterate; wiki/ replaces both ref/ homes; root README+PHILOSOPHY added; Closing Block + venue-aware stage-strip.sh added; draft skill renamed haipipe-application-artifact (paper-alignment refactor; executed SOP archived below).


Archived SOP — paper-alignment refactor (2026-07-06, executed; archived 2026-07-07)
-----------------------------------------------------------------------------------

Condensed from the executed SOP-paper-alignment.md (deleted per its own close-out step; full text recoverable from git history at Tools 0364482).

- **Target**: application becomes paper's structural twin — same spine order (claims before venue), same venue-FREE/venue-ALIGNED coupling, same DPRC phase workers, same folderless probe door, same console/strip/gate machinery — differing ONLY in declared deltas (deliverable = venue artifact not manuscript; _audience/ axis; venue-gated stage skipping; claims settlement depth; deploy/iterate tail).
- **Decision record (JL 2026-07-06)**: R1 spine reorder APPROVED (claims venue-FREE, settlement depth becomes a gate read, slot-mapping moves venue-side); R2 minimap RETIRES into display per-unit contracts, section-edit venue-gated; R3 ask RETIRES to _archive/ (entry = enter console; ad-hoc questions = /haipipe-probe direct ask); R4 FULL 2-phase/ DPRC parity (gate → 3-check rename, persona/attendance kept; ONE revise worker, paper's content/humanizer/results split deferred; probe worker mirrors paper's BOOKKEEP → DISPATCH → TRANSLATE).
- **Commits (Tools main, post-rebase ids)**: fca4bc8 structure moves · 10e8aef load-bearing rewrites · a5c1659 peripheral sweep · 1659aa7 ask-residue close-out · 0e37e0d + a7446b6 three bench-found stage-strip.sh bugs (both families) · f330280 phase-3 port of paper 765696f (evidence-campaign claims 5.0.0, venue 3.0.0 stage doc, _EVIDENCE_ → _VALUES_) + 11 audit fixes from an 18-agent adversarial-verify workflow.
- **Bench exams (both PASSED, JL approved 2026-07-06)**: light path examples/ProjApp-SMSDesign/applications/03_bench_refill_timing_sms (seed→claims→venue→pitch→draft; fresh light probe, 18 verified sources, round-1 fabrication caught+rebuilt; strip renders `--` on skipped stages) · full path 04_bench_timing_report (all stages incl. section-edit; reused full probe → G1/G2/G3 verdict in PPNN card ## Verdict + campaign flip + _VALUES_; report assembled from 0-sections/).
- **Execution notes**: data-contract-schema.md archived with ask (data/contract.yaml stays in the intervention schema); gate-persona.md + attendance-modes.md kept with the check worker (SESSION_STATE plumbing → flag/Gate-Ledger wiring); fn/digest.md "even if confirmed" untouched (digest confirm-gate semantics, not the verdict enum); latent paper-side stage-strip greedy-sed bug found+fixed while adapting; 7 dangling pre-v4 .claude/skills/haipipe-application-* symlinks removed workspace-side.
- **Deliberately unchanged**: _venue/ + _audience/ pack structure; 0-artifacts/ naming; PPNN numbering + _PROBE/ + 1-probe-plans/README.md index names; probe/discovery/task/insight layer contracts; legacy applications/ask/ + existing intervention folders = dead history, no migration.
