haipipe-application — Changelog
===============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.

## [5.3.0] — 2026-07-14 — probe-redesign residue sweep

Fixed
- **`fn/probe-plans.md` → `fn/probes.md`.** The paper twin was renamed to `fn/probes.md` during the redesign; the application twin kept the retired-vocabulary filename and justified it in-file ("the FILENAME is legacy and stays"), while `skills/STRUCTURE.md:63` lists `1-probe-plans/` among the layer's dead words. Two names for one thing, with a rationale the other bucket had already falsified. Renamed, and all six live referrers repointed in one pass (`haipipe-application/SKILL.md:94`, `-claims:147`, `-draft:48`, `-probe:498`, `wiki/README.md:19`, `wiki/11-delivery-need.md:58`). The "legacy filename" apologies in `fn/probes.md` and `wiki/README.md` are deleted.
- **`fn/feedback.md` routing table keyed on a retired noun.** The row read `probe, evidence dispatch, PPNN card -> haipipe-application-probe`. The route target was right, so nothing hard-failed — but this table is the keyword index a session greps to place a piece of feedback, and it advertised "PPNN card" as live vocabulary in a bucket whose own checker (`check-probe-cards.sh` check #10) FAILs card-era words. Exactly the kind of surviving noun that re-seeds the retired model into new writing. Now: `probe, evidence dispatch, probe file, question section, commission`.

## [5.2.0] — 2026-07-14

Changed (PROBE LAYER REDESIGN — Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, approved JL 2026-07-14)
- The `probe` verb re-points at `1-probes/PPNN_<topic>.md`: `"<question>"` RAISES it as a SECTION in the right topic's probe file; bare `probe` SHOWS the board (DERIVED from disk, never a stored status); `run [PPNN]` hands the open sections to `haipipe-application-probe`, which runs the five-step loop. The per-stage `_PROBE/` buffer and the `1-probe-plans/README.md` index are RETIRED.
- The evidence-composition diagram now shows the real path: MATCH the bank's QA corpus first, then dispatch the `commission` block VERBATIM to `Agent(haipipe-task-orchestrator-agent)` / `Agent(haipipe-discovery-orchestrator-agent)`. 💀 the probe GATEWAY agent is retired — there is no tier in between.
- Delivery-need routing: a question with no intervention behind it goes straight to `/haipipe-task qa` or `/haipipe-discovery qa` (the QA file IS the receipt); a claim's STATUS lands in `1-claims.md`, never in a probe.
- `enter` get-or-create scaffolds `1-probes/` instead of `1-probe-plans/README.md`.
- `fn/probe-plans.md` (filename kept — it is referenced from several skills) rewritten as the probe-FILE convention: the flat `1-probes/` pool, the section anatomy, the six derived states, path binding, the QA-file contract, and the loop.
- States: `verdicted` and `dispatched` are DELETED. `planned | commissioned | answered | read | answered-local | failed`.

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
