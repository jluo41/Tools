SOP — Application Ladder Restage (stage 1 → 1a/1b/1c/1d), 2026-07-09
======================================================================

Status: EXECUTED same-session (JL approved "please go ahead and don't stop until you have a very clean results", 2026-07-09). Remaining: live bench exam (§8) on the next real intervention + archive this SOP into haipipe-application/CHANGELOG.md and delete (round-1/2 convention).
Owner: JL. Executor: CC.
Baseline: application @ paper-alignment round 2 (SOP archived pending; family 5.1.0). Paper untouched except a claims-stage preamble note (§4 row P).

1. Target mental model
----------------------

One sentence: stage 1 (venue-FREE evidence work) splits from one claims ledger into a four-rung evidence LADDER — 1a-descriptions → 1b-themes → 1c-claims → 1d-principles — echoing D→I→K→W, because an intervention artifact (unlike a manuscript) carries none of the ladder in its own body, and its dataset is dynamic (iterate keeps refreshing it).

```text
1a-descriptions   what the data looks like        anchored summaries only (pointer + number + as-of date)
1b-themes         what patterns/topics emerge     thematic extraction from 1a + discovery probes
1c-claims         what generalizes                the claim ledger (statuses, settlement, campaign) — the old stage, slimmed
1d-principles     what to do                      design directives, each derived from ≥1 claim — THE DELIVERABLE RUNG
```

JL rulings absorbed (2026-07-09 session): each stage is a mission controller for one aim, releasing probes as satellites until the result is solid; "claims are not the things we want to get the experiment dataset" — application stage-1 evidence is mostly existing knowledge (discovery + task), so the ladder climbs to W (paper delivers K, application delivers W); insights KB downplayed to optional deposit — judgment lives in PP-card verdicts; Descriptions/Themes/Claims/Principles sounds like D/I/K/W without reusing the KB's letter names.

2. Invariants (must survive)
----------------------------

- PPNN card anatomy, `_PROBE/` per stage folder, `1-probe-plans/README.md` index, checker glob `0-lifecycle/*/_PROBE/PP*.md` (lettered folders match `*`) — unchanged.
- DPRC phase engine, the one-door probe rule, VERIFY + gate checkers — unchanged.
- Venue machinery: pin between stage 1 and pitch; stages_skipped; claims_settlement read against 1c's Evidence Campaign — unchanged.
- Seed's `[FORWARD -> CLAIMS]` pointer TOKEN unchanged (grep-stable, paper-aligned); only the consumer moves (R5).
- Paper's own 1-claims stage keeps its single-ledger shape (Hypotheses play the theme role; Methods/Results carry D/I in the manuscript body). Recorded as an intentional delta, guarded by the alignment watch.
- Zero upstream contract changes to probe/discovery/task/insight skills.

3. Design resolutions (CC defaults, JL veto here)
--------------------------------------------------

- R1 — folder shape: skill tree gains `1-lifecycle/1a-descriptions/`, `1b-themes/`, `1d-principles/`; existing `1-claims/` git-mv'd to `1c-claims/`. Intervention folders mirror: `0-lifecycle/1a-descriptions/1a-descriptions.md` (+ `_LOG` + `_PROBE/`) etc. Always four files, every venue (light venues just keep them short) — mechanical checkability beats file-count thrift.
- R2 — ids + traceability: ladder-local ids `D<n>` (descriptions), `T<n>` (themes), `C<n>` (claims), `P<n>` (principles); every downstream entry cites its upstream ids (`C2 (T1; D3)`, `P1 (C2)`). Ids are ladder-local — no relation to insight-KB card ids or PPNN cards.
- R3 — staleness (the dynamic-data contract): every 1a entry carries an as-of date on its anchor. Refreshing an entry stamps its downstream dependents with a `[STALE <id> refreshed <date>]` tag (grep-mechanical); a rung's CHECK fails on unresolved STALE tags in its own doc. Iterate's backfill writes 1a and triggers the stamp pass.
- R4 — verbs + routing: router gains `descriptions | themes | principles` verbs and a composite `ladder` verb (runs 1a→1d as one sweep); `claims` now targets 1c only. Old aliases: "K/W", "what must be true" → claims; "data profile", "how does the data look" → descriptions; "design principles", "social norms", "message principles" → principles.
- R5 — FORWARD consumption moves to 1a: the ladder's first rung DRAFT consumes seed's `[FORWARD -> CLAIMS]` pointers — data-profile needs become 1a probe plans; verdict-shaped needs are materialized as planned PP skeletons in 1c's Probes section. Both count as consumed; 1a CHECK fails on unconsumed pointers (enforcement single-homed at the rung that always runs first).
- R6 — gate batching, venue-scaled (extends wiki/08): light venues = ONE combined inline gate at 1d covering all four rungs (one approval writes four ledger rows); medium = combined gate at 1c (covers 1a-1c) + gate at 1d; full = four individual gates. Every rung still gets its ledger row — approval is batched, never skipped.
- R7 — insights downplayed: "scan insights/INDEX.md first" becomes optional; claims anchor directly to task results and discovery sources via PP verdicts (judgment = the full-mode probe verdict, never a raw unjudged number); 1d deposits surviving principles as W cards ON-REQUEST only. PHILOSOPHY boundaries updated: insight = optional deposit layer.
- R8 — `_VALUES_` placement: stays with 1c (`_VALUES_1c-claims.md`, claim-backing numbers). 1a needs no satellite — the 1a doc IS the anchored-numbers doc (one line = statistic + anchor + as-of date).
- R9 — downstream readers: pitch/narrative/display/artifact/review/claim-audit read `1d-principles.md` as the primary input (the ladder's deliverable) with `1c-claims.md` as the evidence backstop; claim-audit traces artifact → principle → claim → anchor.

4. Change list — phase 1 (load-bearing)
----------------------------------------

| # | File | Change |
|---|------|--------|
| 1 | 1-lifecycle/1-claims/ → 1c-claims/ | git mv; SKILL.md → 6.0.0: slimmed to pure K-work (claims cite T/D ids; Hypotheses stay absent; FORWARD reader clause moves out to 1a; keeps statuses, settlement, campaign, _VALUES_) |
| 2 | 1-lifecycle/1a-descriptions/haipipe-application-descriptions/ | NEW skill 1.0.0: anchored data summaries, as-of dates, task-profile probe lane, FORWARD consumer, staleness stamp duty |
| 3 | 1-lifecycle/1b-themes/haipipe-application-themes/ | NEW skill 1.0.0: thematic extraction, each theme cites ≥1 D id or discovery source, discovery-probe lane |
| 4 | 1-lifecycle/1d-principles/haipipe-application-principles/ | NEW skill 1.0.0: P<n> directives from ≥1 claim, W-actionability test, contrast with venue Artifact Principles, on-request W deposit |
| 5 | haipipe-application/SKILL.md → 6.0.0 | verbs (descriptions/themes/principles/ladder), strip example, routing notes, delivery-need paths |
| 6 | 1-lifecycle/haipipe-application-lifecycle/SKILL.md → 4.0.0 | ladder in pipeline order, dispatch map, frontier list, loopback, relation diagram |
| 7 | haipipe-application/stage-strip.sh | keys gain descriptions/themes/principles; prefix-normalization handles `1a-` |
| 8 | 2-phase/1-probe/.../ref/per-stage-dispatch.md | per-stage rows 1a/1b/1c/1d (modes: light/light/full/rare) |
| 9 | wiki/08-stage-gate.md | R6 gate batching |
| 10 | 1-lifecycle/0-seed/haipipe-application-seed/SKILL.md | FORWARD consumer = 1a (token unchanged); handoff → ladder |
| 11 | 1-lifecycle/*/ref/<stage>-template.md (9 files) + draft 1.2.0 registry | JL follow-up same session: every stage skill carries its canonical artifact template (paper convention); draft worker WRITE reads it via a registry table; SKILL.md pointer lines added |

5. Phase 2 — periphery sweep
-----------------------------

PHILOSOPHY.md (lifecycle, stage table, boundaries, design prompt) · README.md (layouts, delta table, retired names) · wiki/03 (folder contract, stage table, maturity, loopback, comparison) · wiki/05 (spine, open-needs rows) · wiki/06 (tree, stage map, router rule, current_layer vocab) · enter SKILL (stage docs, handoff, needs, loopback) · pitch/narrative/display/section-edit/venue/artifact/review/claim-audit reads (R9 paths) · iterate (backfill-1a wiring) · 2-phase README/USAGE/WIRING + draft/revise/check stage enumerations · fn/probe-plans.md + fn/feedback.md paths · PREFERENCES.md (alignment-watch: stage-1 divergence is intentional, ports must not re-converge it) · probe SKILL `_VALUES_` path · CHANGELOG rollups + family 6.0.0.

6. What deliberately does NOT change
-------------------------------------

Venue packs, audience packs, deploy, round, Gate Ledger format (rows only multiply), check worker persona/attendance machinery, checks.sh, check-probe-cards.sh (glob already letter-compatible), paper spine and paper 2-phase (except the claims Data Context preamble note), probe/discovery/task/insight upstream contracts, bench folders (round-1/2 history).

7. Rollback
-----------

Scoped commits on Tools main, clustered: (a) new rung skills + mv (rows 1-4), (b) router/lifecycle/strip/dispatch (rows 5-8), (c) gates + seed (rows 9-10), (d) periphery + paper note. Rollback = git revert the cluster; no project-side data migration. Legacy interventions: one-time folder rename `0-lifecycle/1-claims/` → `0-lifecycle/1c-claims/` (+ create empty sibling rung folders) when next opened; skills do not dual-read old layouts.

8. Exam (bench validation, next real intervention)
---------------------------------------------------

1. Ladder sweep on a light venue: one combined 1d gate, four ledger rows on one approval, strip renders `descriptions ✅ themes ✅ claims ✅ principles 🔥🚀`.
2. FORWARD handoff: seed pointer → consumed at 1a DRAFT (data need → 1a plan; verdict need → 1c PP skeleton); delete the consumption, 1a CHECK fails.
3. Staleness: refresh a 1a entry → dependents in 1b/1c/1d gain STALE tags → downstream CHECK fails until resolved.
4. Traceability: claim-audit walks artifact → P → C → anchor on a drafted artifact.

9. Round-1 walkthrough rulings (JL, 2026-07-09, in-file > CC:/> JL: threads)
-----------------------------------------------------------------------------

- Display-unit ids: D<nn> -> U<nn> (T1, EXECUTED). Illustration blocks: ascii `====`/`----` style (T8, EXECUTED across seed/pitch/narrative/display).
- FORWARD token stays `[FORWARD -> CLAIMS]` (T2, paper-twin symmetry).
- P status enum: `stale` DROPPED -> `active | caveated`; staleness lives solely in the [STALE] tag (T4, EXECUTED).
- Bare `claims` verb: ladder-virgin guard added to router dispatch notes (T6, EXECUTED).
- Gate batching depths: PARKED, test at the 01_sms_young_male bench (T5).
- Ladder routing invariant codified in wiki/08: rung CHECK = approve advances / revise reruns / loopback upstream (1c -> 1a stale data, 1c -> 1b wrong theme); ladder exits to venue ONLY through the 1d gate.

10. Round-2 candidates (JL walkthrough thoughts, 2026-07-09 — NOT yet designed)
--------------------------------------------------------------------------------

- **Cumulative DIKW reading (ADOPTED as canon):** descriptions=D, themes=D+I, claims=D+I+K, principles=D+I+K+W — each rung CONTAINS its lower layers, not just sits atop. Consequence: a theme may carry theme-scoped descriptive content in its own part (anchored: pointer + date); numbers that become load-bearing across rungs promote to 1a D entries.
- **1d rename question (RESOLVED 2026-07-09, executed same session):** JL ruled **ADVICE** ("rename the principles to advise... later we can use them or not use them") — folder `1d-advice`, skill `haipipe-application-advice`, ids `A<n>`, maturity `advised`, verbs advice|advise|recommendation (+ legacy `principles` alias). The ruling's second half became the ADOPTION contract: advice is counsel, not mandate; venue-ALIGNED stages record adopted/declined A-ids with a why; declined entries persist; claim-audit chain = artifact -> adopted A -> C -> anchor. ("insights" was REJECTED — collides with the insight KB layer.)
- **explore | exploit role tag on P (PROPOSED, 1d thread):** derivation bars apply to exploit-Ps; an explore-P may derive from weak/GAP claims IF tagged, bounded by compliance rails, and wired to the C<n> its deployed arm settles (iterate -> 1a backfill -> C flips -> explore-P graduates or moves to Rejected). Deploy becomes an evidence probe (test-to-learn).
- **Design lifecycle stage (PROPOSED, wiki/06 + router threads):** for design venues (message set + design report), the venue-ALIGNED middle becomes pitch(light: venue-fit) -> 2-design -> draft; 2-design owns the design matrix (segments x arms x framings, cells cite P ids + explore/exploit tags); narrative/display skipped via the venue pack. Also needs a venue-design-doc pack (message set + rationale). Spec source: run the bench with the current spine first; where pitch/draft strain IS the spec.
- **Per-rung maturity (`themed`) (OPEN, lean no):** maturity marks capability jumps only; the strip already shows rungs.

11. Done criteria
-----------------

- [x] JL approval to execute (2026-07-09, "go ahead ... very clean results")
- [x] Phase-1 rows 1-10 landed
- [x] Phase-2 sweep landed
- [x] Paper-side Data Context preamble note + skill CHANGELOG
- [x] Validation greps: zero live `1-claims` references app-side outside archives/changelogs/SOPs; frontmatter names unique; strip renders with new keys
- [ ] Live bench exam (§8) on the next real intervention
- [ ] This SOP archived into haipipe-application/CHANGELOG.md and deleted
