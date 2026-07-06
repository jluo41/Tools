# SOP — Application Paper-Alignment Refactor (2026-07-06)

Status: PHASES 1+2 EXECUTED (JL approved 2026-07-06). Commits: 3da6f6a (1a structure moves) · 8d9e3af (1b load-bearing rewrites) · 45f75b2 (2 peripheral sweep) · +close-out commit (persona/attendance/input-contract ask-residue patches, data-contract-schema archived, SOP status). Workspace-side: 7 dangling pre-v4 `.claude/skills/haipipe-application-*` symlinks removed. Remaining: bench exams (§8) → then archive this SOP into haipipe-application/CHANGELOG.md and delete.
Owner: JL. Executor: CC.
Decision record: JL 2026-07-06 — R1 spine reorder APPROVED; R2 stage-5 resolution APPROVED (minimap retires, section-edit venue-gated); R3 ask RETIRES ("maybe just retire it" — entry = /haipipe-application enter, paper pattern; recoverable from _archive/ if a batch-research need reappears); R4 DPRC "we will do the same" = FULL 2-phase/ parity with paper.

## 1. Target mental model

One sentence: application becomes paper's structural twin — same spine order (claims before venue), same venue-FREE/venue-ALIGNED coupling, same DPRC phase workers, same folderless probe door, same console/strip/gate machinery — differing ONLY in its declared deltas (deliverable = venue artifact not manuscript; _audience/ axis; venue-gated stage skipping; claims settlement depth; deploy/iterate tail).

```text
BEFORE (v4, 2026-06-23)                          AFTER (v5)
seed → pitch → [venue] → claims → narrative      seed → claims → [venue] → pitch → narrative
  → display → minimap → draft → review             → display → section-edit° → draft(artifact)
  → deploy → iterate                               → review → deploy → iterate   (° = venue-gated)
venue change "invalidates claims+"               claims venue-FREE; retarget re-runs venue + pitch only
no phase axis; gate fires between stages         every stage runs DRAFT→PROBE→REVISE→CHECK (2-phase/)
1-probe-plans/PP## flat plan files;              per-stage _PROBE/PPNN cards = single source of truth;
  route `/haipipe-probe plan from-need`;           1-probe-plans/README.md = index only; the 2-phase
  verdict word "confirmed"                         probe worker is the ONLY door; enum supported|refuted|inconclusive
ask = 4-phase session machinery (dead refs:      RETIRED; entry = enter console; ad-hoc questions =
  -plan/-context/-loop/-bridge)                    /haipipe-probe "<question>" direct ask
no closing block; ref/stage-strip.sh = stale     Closing Block in router SKILL.md; application
  PAPER copy (wrong spine for both families)       stage-strip.sh, venue-aware (skipped stages render `--`)
enter maturity ladder = pre-v4 names             enter rewritten on paper-enter model (gate ledger,
  (rationale/design/variants/delivery-plan)        get-or-create, derive-from-disk)
```

## 2. Invariants (must survive the refactor)

- The four evidence principles (paper/wiki/00-evidence-principles.md): land-at-home, review-on-write, layered orders, trim-ceremony-never-principle.
- Application's intentional deltas stay: _audience/ axis; venue-gated stage firing; claims settlement depth scales with venue; 0-artifacts/ markdown deliverables; deploy/iterate tail; interventions live in-project (plain folders, no repo backing).
- Insight boundary: application READS insight always; WRITES via filing at iterate/probe-deposit; insight never reads applications/.
- Stage skills own WHAT, 2-phase workers own HOW, users invoke stage skills only — phase workers never user-facing.
- Evidence discipline verbatim from paper: stage → worker → gateway agent → discovery/task; no inline searching anywhere; fresh evidence must land; TRUST THE LEDGER; shape honesty; background dispatch for fresh runs; mechanical acceptance wherever transcription is delegated.
- probe/discovery/task/insight layers: ZERO upstream contract changes — application adopts, nothing moves on their side.

## 3. Design resolutions (interpret R1–R4; JL vetoes here at review)

- R1 — claims venue-FREE: the ledger states what must be true + evidence status (C-slots, supported|weak|GAP, roles), NO venue slot-mapping. Venue-scaled depth becomes a SETTLEMENT GATE read at gate time ("how much of the ledger must be supported before artifact work"), not a content mode. Slot-mapping moves to the venue-ALIGNED side (pitch/narrative/artifact composition). Light venues still write a real (small) ledger.
- R2 — stage 5: minimap RETIRES (unit jobs absorb into 4-display per-unit contracts, paper's move). 5-section-edit = venue-gated final lifecycle stage (req for report/dashboard-like venues; skip for sms/push/reminder), generalized from section-editing v3; its hardcoded 6-section list moves to _venue/venue-report as pack knowledge.
- R3 — ask RETIRES to _archive/ together with its private refs (session-state-schema.md, report-template.md). Router gains paper-parity discover/task verbs for non-claim utility; ad-hoc evidence questions route to /haipipe-probe direct ask. Legacy applications/ask/<NN>/ folders = dead history: nothing reads, nothing writes (probes/-folder precedent, JL 2026-07-05).
- R4 — full DPRC: new 2-phase/ bucket with 0-draft, 1-probe, 2-revise, 3-check. Existing gate skill MOVES to 3-check (renamed haipipe-application-check; persona + attendance machinery kept as the application delta; venue-scaled gate depth kept). NEW thin draft + revise workers (ONE revise worker; paper's content/humanizer/weaving split deferred until artifacts demand it). NEW haipipe-application-probe mirrors haipipe-paper-probe's contract: RE-INVOKE PER RUN, BOOKKEEP → DISPATCH (always Agent(haipipe-probe-orchestrator-agent); light default, full for claims verdicts; bg for fresh) → TRANSLATE (anchored takeaways → card; full verdict → ## Verdict + claims-ledger flip in the same pass). No citation/values/display doc-worker sub-skills at first — venue-scaled hooks inside the worker, split out only if a venue needs them.
- Naming collision: the artifact generator (current 3-draft/haipipe-application-draft) RENAMES to haipipe-application-artifact and re-homes to 3-build-deploy/; the user verb `draft` routes there; the 2-phase DRAFT worker takes the haipipe-application-draft name (paper parallel). Artifact skill keeps the v4 principle "the venue profile IS the instruction set" and runs DPRC internally when composing.
- Bucket renumber to paper semantics: 0-enter/ (enter + round moves in), 1-lifecycle/ (numbered stage subfolders 0-seed..5-section-edit + venue + lifecycle at bucket root), 2-phase/ (DPRC workers), 3-build-deploy/ (artifact, review, claim-audit, deploy), 4-iterate/, _venue/, _audience/, wiki/ (replaces BOTH ref/ homes), _archive/ (new).
- Closing block icon: 🎯 application (proposed; JL may swap). Strip spine keys: seed claims venue pitch narrative display section-edit review; venue-skipped stages render `--` (read from the pinned venue's stage table; STATUS.md gate ledger stays the ✅ source).

## 4. Change list — phase 1 (load-bearing)

| # | File | Change |
|---|------|--------|
| 1 | application/README.md | NEW canonical root doc mirroring paper/README.md: intervention = delivery contract; intervention-folder layout (stage FOLDERS + _PROBE/); skill-tree layout; references table; retired-names table |
| 2 | application/PHILOSOPHY.md | NEW mirroring paper/PHILOSOPHY.md: lifecycle, stage questions, two orthogonal axes, evidence routing, boundaries, console, copilot policy, design prompt (application spine) |
| 3 | haipipe-application/SKILL.md → 5.0.0 | New spine + venue-coupling rules (seed/claims venue-FREE; venue pins between claims and pitch; downstream venue-ALIGNED); verbs: probe = BUFFER/SHOW/`run` via the 2-phase worker (umbrella NEVER calls /haipipe-probe), discover/task added (non-claim utility), draft → artifact, gate → check alias, ask REMOVED (pointer to /haipipe-probe direct ask); Closing Block section (🎯 · two-line strip · `--` for venue-skipped); routing resolution order; no-arg chooser; specialist return contract; structure pointers; retired-names table |
| 4 | haipipe-application/stage-strip.sh | NEW venue-aware renderer co-located with the Closing Block spec (paper convention); DELETE ref/stage-strip.sh (stale paper copy with paper's spine) |
| 5 | 0-enter/haipipe-application-enter → 2.0.0 | Rewrite on paper-enter model: derive-from-disk, Gate-Ledger-aware ✅, get-or-create (confirm-gated scaffold, no repo backing), CURRENT maturity ladder (drop rationale/design/variants/delivery-plan), closing-block inheritance, loopback diagnosis |
| 6 | 2-rounds/haipipe-application-round | MOVE → 0-enter/ (paper pattern); verify 1-rounds/vYYMMDD contract parity with paper/wiki/07-paper-rounds.md |
| 7 | 1-lifecycle/ re-bucket | Numbered stage subfolders 0-seed/ 1-claims/ 2-pitch/ 3-narrative/ 4-display/ 5-section-edit/, each holding its skill; haipipe-application-venue + -lifecycle stay at bucket root |
| 8 | haipipe-application-lifecycle → 3.0.0 | New spine; venue-pin checkpoint moves between claims and pitch; frontier detection on stage FOLDERS; loopback fix ("venue wrong" → re-run venue + pitch, claims survives); each stage drives the 2-phase workers |
| 9 | haipipe-application-claims → 4.0.0 | Venue-free ledger; body catches up to its own v3 frontmatter: stage folder 0-lifecycle/1-claims/ with 1-claims.md + _LOG + _EVIDENCE_ + _PROBE/PPNN cards + index row in 1-probe-plans/README.md; settlement-depth-at-gate; kill `plan from-need`; enum supported|refuted|inconclusive |
| 10 | 2-phase/1-probe/haipipe-application-probe | NEW phase worker per §3-R4 (the ONLY evidence door for application stages) |
| 11 | 2-phase/0-draft + 2-phase/2-revise | NEW thin workers: stage-doc structure + sentences; venue style-profile + audience-profile prose pass |
| 12 | shared/haipipe-application-gate | MOVE → 2-phase/3-check/haipipe-application-check: CHECK-phase framing, approve/revise/done, writes STATUS.md Gate Ledger rows; persona/attendance kept; gate-persona.md + attendance-modes.md move next to it |
| 13 | 3-draft/haipipe-application-draft | RENAME → haipipe-application-artifact, MOVE → 3-build-deploy/ (see §3 naming collision); composes 0-artifacts/<slug>-v{N}.md (simple venues: claims + venue template; sectioned venues: assemble from 0-sections/) |
| 14 | 4-review-deploy/{review,claim-audit,deploy} | MOVE → 3-build-deploy/; old-spine-word sweep rides along |
| 15 | 5-iterate/haipipe-application-iterate | MOVE → 4-iterate/ |
| 16 | 1-lifecycle/haipipe-application-minimap | RETIRE → _archive/ (jobs → display per-unit contracts) |
| 17 | 1-lifecycle/haipipe-application-section-editing | → 5-section-edit/haipipe-application-section-edit: generalize (hardcoded 6-section list → _venue/venue-report), venue-gated, per-section DPRC |
| 18 | shared/haipipe-application-ask | RETIRE → _archive/ (+ session-state-schema.md, report-template.md) |
| 19 | wiki/ | NEW single docs home: 03-intervention-lifecycle (rewritten: spine, stage folders, folderless evidence flow, maturity), 05-intervention-dashboard, 06-application-skill-structure (NEW, mirrors paper/wiki/06), 08-stage-gate (application rewrite: Gate Ledger, md artifacts, venue-scaled gates), 11-delivery-need (SINGLE copy; routes = buffer + probe run). DELETE application/ref/ and prune haipipe-application/ref/ (remaining refs re-homed or archived per phase-2 review) |
| 20 | haipipe-application/fn/probe-plans.md | NEW buffer convention adapted from paper/haipipe-paper/fn/probe-plans.md (per-stage _PROBE/ + index README) |
| 21 | paper/PHILOSOPHY.md (upstream fix) | Design prompt spine → current (0-seed > 1-claims > [venue] > 2-pitch > 3-narrative > 4-display > 5-section-edit) so application aligns to the true model |

## 5. Phase 2 — peripheral sweep (after phase 1 lands)

- seed/pitch/venue/narrative/display SKILL.mds: stage numbers, stage-file → stage-folder paths, venue-coupling lines (pitch re-couples [primary] + RQ framing on retarget); display absorbs minimap's per-unit job contract.
- _venue/ packs (8 profiles + _SCHEMA): stage tables (minimap row out, section-edit row in), gate field semantics, slot-mapping ownership note; venue-report gains the report section structure from section-editing v3.
- fn/feedback.md keyword→skill map (ask/minimap out; probe/check/artifact in); fn/digest.md untouched except examples.
- Enum + verb sweep: `confirmed` → `supported` (review, venue-report style-profile, digest example); any `plan from-need` stragglers; dead-skill references (-plan/-context/-loop/-bridge) all die with ask's archive.
- intervention-dashboard.md: strip markers per Closing Block; maturity per new ladder.
- CHANGELOGs: one rollup entry per touched skill; family-level rollup in haipipe-application/CHANGELOG.md.
- Registration: confirm retired skills (ask, minimap) drop out of skill discovery and renamed skills (check, artifact, section-edit) register; fresh session to verify.

## 6. What deliberately does NOT change

- _venue/ + _audience/ pack structure (README + style-profile [+ exemplars]); venues/audiences = knowledge, never verbs.
- 0-artifacts/ versioned artifact naming; data/contract.yaml; .intervention-console.yaml (schema refreshed, name kept).
- PPNN numbering, _PROBE/ folder name, 1-probe-plans/README.md index name — shared with paper as-is.
- probe/discovery/task/insight layer contracts.
- Legacy applications/ask/ + existing intervention folders: dead history, NO migration; the new contract applies to new work; anything valuable re-enters only by a human pointing at it.

## 7. Rollback

Scoped commits on Tools main, clustered: (a) structure moves (git mv only), (b) load-bearing rewrites, (c) phase-2 sweep. Rollback = git revert the cluster; no project-side data migration to undo.

## 8. Exam (bench validation, after phase 1)

1. Light path: one SMS intervention seed → claims(light settlement) → venue → pitch → artifact. Watch: no ask/minimap invoked; claims stage folder + _PROBE/ card + index row; gateway bg dispatch (light); enum correct; strip renders `--` on narrative/display/section-edit; artifact cites K/W.
2. Full path: one report/dashboard intervention through section-edit with ≥1 full-mode claims verdict: G1/G2/G3 land in the card's ## Verdict; ledger flips at TRANSLATE; Gate Ledger rows written; check worker approves.
3. Console: /haipipe-application enter on both; dashboard derives from disk; closing block renders exactly one 🔥 and one 🚀.

## 9.5 Phase 3 — port of paper 765696f (evidence-campaign claims + venue stage doc; JL approved 2026-07-06)

Paper moved again mid-exam (765696f: claims 4.0.0 evidence-campaign brain, venue 2.0.0 Writing-Principles stage doc, per-stage Probes sections). Port table; rulings: mirror dual-2 numbering (2-venue/ + 2-pitch/, flag collision upstream once) · NO Hypotheses section app-side (mechanism lives in seed/pitch) · _CITATION_ venue-scaled (sectioned venues only), _VALUES_ always · bench resumes ON the ported spec.

| # | File | Change |
|---|------|--------|
| P1 | haipipe-application-claims → 5.0.0 | three sections (Claims short / Probes full / Evidence Campaign with dispatch order + deps); _EVIDENCE_ → _VALUES_; settlement gate reads the campaign; `=====`/`-----` + one-sentence-per-line artifact formatting |
| P2 | haipipe-application-venue → 3.0.0 | produces 0-lifecycle/2-venue/2-venue.md + _LOG + _PROBE/ with Artifact Principles (template/slots, limits, tone-by-audience, element types, section structure, gate depth) as the downstream contract; still writes the 3 STATUS rows |
| P3 | seed/pitch/narrative/display SKILL.mds | + visible Probes section in the stage doc + artifact formatting block |
| P4 | probe worker + check | TRANSLATE values → _VALUES_; claims exit criteria = campaign complete |
| P5 | wiki/03 + wiki/06 + README + router | folder contract rows (2-venue/, _VALUES_), stage table, venue verb line |
| P6 | bench reconciliation | 04 PP01 reset planned → re-dispatch; both bench ledgers reshaped to campaign format; exam finishes under the ported spec |

## 9. Done criteria

- [x] JL approved execution ("please go ahead and do it", 2026-07-06); §3 resolutions stand unless vetoed on review
- [x] Phase-1 rows 1–21 landed (3da6f6a + 8d9e3af)
- [x] Phase-2 sweep landed (45f75b2 + close-out commit)
- [ ] Light-path exam passed (8.1)
- [ ] Full-path exam passed (8.2)
- [ ] This SOP archived into haipipe-application/CHANGELOG.md + deleted (no parallel bookkeeping files long-term)

Execution notes (deliberate, flagged 2026-07-06):
- `data-contract-schema.md` ARCHIVED with ask (its lifecycle was ask's Phase-1 A1 machinery); `data/contract.yaml` stays in the intervention schema — a data-consuming venue writes a fresh contract doc when one is actually needed.
- `gate-persona.md` + `attendance-modes.md` kept with the check worker, SESSION_STATE plumbing replaced with flag/Gate-Ledger wiring; the persona/threshold logic preserved verbatim.
- `fn/digest.md` line "even if confirmed" untouched — that is digest's confirm-gate semantics, not the verdict enum.
- Latent paper-side bug found+fixed while adapting stage-strip.sh: `| current_layer |` table-row extraction used a greedy sed that returned empty (masked by the old-format fallback); both scripts now use the anchored pattern.
- Skill re-registration (renamed check/artifact/section-edit, new draft/probe/revise, retired ask/minimap) needs a fresh session to verify in the harness skill list.
