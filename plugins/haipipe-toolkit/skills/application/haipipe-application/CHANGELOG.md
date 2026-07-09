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

## [5.1.0] — 2026-07-07

- FAMILY ROLLUP (paper-alignment round 2, porting paper b2c5a23 enforcement): probe worker 2.0.0 gains STEP 4 VERIFY (check-probe-cards.sh fork) + PROOF 1-4 blocks + venue-scaled `harvest: OWED` lane debts (_VALUES_ always, _CITATION_ sectioned venues only, _DISPLAY_ only with display units) + ref/ dispatch tables; check worker 4.0.0 gains gate wiring (card-checker FAIL blocks green) + markdown-safe checks.sh (em-dash, AI-voice tells, TODO/FIXME, bibtex-in-md) + `> CHECK:` seeding in stage docs only, artifact findings → Gate Ledger notes (R2c, JL ruled 2026-07-07); draft 1.1.0 gains WebSearch/WebFetch as DRAFT-only orientation fuel — "DRAFT may search; PROBE must dispatch"; seed 3.2.0 narrows probe scope to feasibility + registers [FORWARD → CLAIMS] pointers in _LOG_0-seed.md, claims 5.1.0 DRAFT consumes them (unconsumed pointer fails claims CHECK); PREFERENCES.md gains the family-generic real-probe entry + the paper-drift alignment-watch line (R6); 2-phase/ gains thin USAGE.md + WIRING.md + the ONE-pipeline/HARVEST note in README.md; router SKILL.md + wiki 03/06/08 one-line mentions. Round-2 SOP archives below on close-out (same convention as round 1).


Archived SOP — paper-alignment refactor (2026-07-06, executed; archived 2026-07-07)
-----------------------------------------------------------------------------------

Condensed from the executed SOP-paper-alignment.md (deleted per its own close-out step; full text recoverable from git history at Tools 0364482).

- **Target**: application becomes paper's structural twin — same spine order (claims before venue), same venue-FREE/venue-ALIGNED coupling, same DPRC phase workers, same folderless probe door, same console/strip/gate machinery — differing ONLY in declared deltas (deliverable = venue artifact not manuscript; _audience/ axis; venue-gated stage skipping; claims settlement depth; deploy/iterate tail).
- **Decision record (JL 2026-07-06)**: R1 spine reorder APPROVED (claims venue-FREE, settlement depth becomes a gate read, slot-mapping moves venue-side); R2 minimap RETIRES into display per-unit contracts, section-edit venue-gated; R3 ask RETIRES to _archive/ (entry = enter console; ad-hoc questions = /haipipe-probe direct ask); R4 FULL 2-phase/ DPRC parity (gate → 3-check rename, persona/attendance kept; ONE revise worker, paper's content/humanizer/results split deferred; probe worker mirrors paper's BOOKKEEP → DISPATCH → TRANSLATE).
- **Commits (Tools main, post-rebase ids)**: fca4bc8 structure moves · 10e8aef load-bearing rewrites · a5c1659 peripheral sweep · 1659aa7 ask-residue close-out · 0e37e0d + a7446b6 three bench-found stage-strip.sh bugs (both families) · f330280 phase-3 port of paper 765696f (evidence-campaign claims 5.0.0, venue 3.0.0 stage doc, _EVIDENCE_ → _VALUES_) + 11 audit fixes from an 18-agent adversarial-verify workflow.
- **Bench exams (both PASSED, JL approved 2026-07-06)**: light path examples/ProjApp-SMSDesign/applications/03_bench_refill_timing_sms (seed→claims→venue→pitch→draft; fresh light probe, 18 verified sources, round-1 fabrication caught+rebuilt; strip renders `--` on skipped stages) · full path 04_bench_timing_report (all stages incl. section-edit; reused full probe → G1/G2/G3 verdict in PPNN card ## Verdict + campaign flip + _VALUES_; report assembled from 0-sections/).
- **Execution notes**: data-contract-schema.md archived with ask (data/contract.yaml stays in the intervention schema); gate-persona.md + attendance-modes.md kept with the check worker (SESSION_STATE plumbing → flag/Gate-Ledger wiring); fn/digest.md "even if confirmed" untouched (digest confirm-gate semantics, not the verdict enum); latent paper-side stage-strip greedy-sed bug found+fixed while adapting; 7 dangling pre-v4 .claude/skills/haipipe-application-* symlinks removed workspace-side.
- **Deliberately unchanged**: _venue/ + _audience/ pack structure; 0-artifacts/ naming; PPNN numbering + _PROBE/ + 1-probe-plans/README.md index names; probe/discovery/task/insight layer contracts; legacy applications/ask/ + existing intervention folders = dead history, no migration.

## [6.0.0] — 2026-07-09

- FAMILY ROLLUP (ladder restage; SOP-ladder-restage.md at the family root archives here on close-out): stage 1 split into the venue-FREE EVIDENCE LADDER `1a-descriptions -> 1b-themes -> 1c-claims -> 1d-principles`, echoing D->I->K->W without reusing the insight-KB letter names (JL rulings 2026-07-09: "claims are not the things we want to get the experiment dataset"; Descriptions/Themes/Claims/Principles "sounds like D, I, K, W"; paper delivers K, application delivers W — the artifact carries no D/I body and lives on dynamic data, so application climbs one more rung than paper).
- NEW rung skills: haipipe-application-descriptions 1.0.0 (anchored data summaries + as-of dates, FORWARD consumer, staleness stamp duty), haipipe-application-themes 1.0.0 (grounded thematic extraction), haipipe-application-principles 1.0.0 (P<-C directives, W-actionability test, on-request W deposit, ladder gate host); claims 6.0.0 slimmed to rung 1c (folder git-mv'd 1-claims/ -> 1c-claims/; theme tags; FORWARD reader moved out).
- Ladder mechanics: ladder-local id chain P<-C<-T<-D mandatory (R2); `[STALE <id> refreshed <date>]` staleness propagation from 1a refreshes, CHECK fails on unresolved tags (R3); venue-scaled GATE BATCHING — light: one combined gate at 1d writing four ledger rows, medium: 1c+1d, full: four (R6, wiki/08); insights downgraded to optional deposit — judgment lives in PP-card verdicts (R7); `_VALUES_` stays with 1c, the 1a doc IS the anchored-numbers doc (R8); downstream readers (pitch/narrative/display/section-edit/venue/artifact/review/claim-audit) now read 1d-principles as primary input with 1c-claims as evidence backstop, claim-audit traces artifact -> P -> C -> anchor (R9).
- Wiring: router 6.0.0 (verbs descriptions/themes/principles + composite `ladder`), lifecycle orchestrator 4.0.0, stage-strip.sh keys + `1a-` prefix normalization (tested: frontier collapse + loopback split render correctly), probe ref/per-stage-dispatch 1a-1d rows, check worker per-rung exit criteria + argument-hint, seed FORWARD consumer note + handoff -> ladder, iterate Step 4 backfills fresh A/B numbers into 1a BEFORE triage, enter console read-order/diagnosis/maturity/needs/loopback, wiki 03/05/06/08, PHILOSOPHY + README (delta table + retired-names rows), fn/probe-plans + fn/feedback paths, PREFERENCES alignment-watch ladder caveat (ports map paper claims-stage changes onto 1c, never re-converge).
- Migration: legacy interventions rename `0-lifecycle/1-claims/` -> `0-lifecycle/1c-claims/` (+ create sibling rung folders) on next open; skills do not dual-read old layouts. Live bench exam (SOP §8) pending on the next real intervention.
- Templates (JL follow-up, same session: "no ref/ no template ... what the stage generated markdown looks like"): every 1-lifecycle stage skill gains `ref/<stage>-template.md` (seed, descriptions, themes, claims, principles, pitch, narrative, display, venue — 9 files, paper convention), each SKILL.md gains a canonical-template pointer line, and draft worker 1.2.0 gains the template registry table (WRITE reads the stage's template; the worker carries none of its own).
