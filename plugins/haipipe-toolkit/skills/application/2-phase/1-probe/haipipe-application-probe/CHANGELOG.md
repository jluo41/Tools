haipipe-application-probe — Changelog
================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [0.3.2] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 3.2.0; older entries below keep their original numbers).

## [3.2.0] — 2026-07-19

- Owner ruling, 2026-07-19 (JL): "宪法 don't use this name, just use `probe`." The nickname
  "THE CONSTITUTION" / "the constitution" for `probe/haipipe-probe/SKILL.md` is dropped everywhere;
  each site now names either `probe` or the actual path.
  Touched: SKILL.md (frontmatter summary, model pointer, Rules header, PHASE SPLIT header, ⑤ INTERPRET,
  the checker note, Hard-boundaries header, Reference block), `ref/per-stage-dispatch.md`,
  `ref/harvest-acceptance.md`, and two `check-probe-cards.sh` comments.
- `ref/per-stage-dispatch.md` seed section: dropped the retired FIELD notation `a-consumer:` while keeping the
  live concept — the a-consumer (in 0-seed.md) feeds the opportunity, mechanism hypothesis, and kill criteria.
  Matches the paper twin (`paper/2-phase/1-probe/haipipe-paper-probe/ref/per-stage-dispatch.md`). Vocabulary: `a-consumer:` as a PROBE-FILE FIELD is gone — the probe entry's answer subsection is
  `### a-executor` (the copy of the answering QA file's answer, the consumer-side single source of truth).
  The a-consumer CONCEPT is untouched: it remains the per-consumer interpretation written in the STAGE DOC
  (station 2, anchored `[source: PP<NN>]`).

## [3.1.1] — 2026-07-19

- Probe constitution v9.5.0 sync (Q-executor-entry probe-file format), mirroring the paper family. A question is now a `## QX<n>` ENTRY (topic-local) with four `###` subsections: `### q-executor` (was `q-executor:`; carries Deliverable/Accepted), `### q-consumer` (was `serves:`; one bullet per stage-doc Q-consumer id + that consumer's ORIGINAL question), `### bank binding` (`route` · `bank` — was `match: EXISTS/NONE` — · `target` · `state`), and `### a-executor` (was the probe-file `a-consumer:`; a COPY of the answering QA file's answer). `## Why` DROPPED: the stake lives in the stage-doc Q-consumer. `a-consumer` SURVIVES as the stage-doc concept (station ②), anchored `[source: PP<NN>]` back to the `### a-executor` copy.
- Model A phase split adopted: DRAFT authors ①ORGANIZE + ②MATCH; this worker runs ③DISPATCH → ④POINT → ⑤INTERPRET and does NOT re-match (`route`/`bank` are AUTHORITATIVE). ①+② became a documented PRECONDITION section; the collector agent runs ③④ (was ②③④). Added a "Rules" pointer block to the constitution's PROBE-phase rules, mirroring haipipe-paper-probe.
- Harvest (the application no-sidecar delta, unchanged in substance) folds into `### a-executor` rather than the probe-file `a-consumer:`; numbers/citations stay inline with their `[→ target QA]` anchor.
- Archaeology strip: `PASS 1 R19/R20`, the `2026-07-18` date tags, and the retired `_VALUES_`/`_CITATION_`/`_DISPLAY_`/`_DESCRIPTIONS/` sidecar enumerations removed — reason kept, citation cut. `1-probes/` is the only consumer-side source of truth; `_LOG` is the only kept sidecar.
- `ref/per-stage-dispatch.md` and `ref/harvest-acceptance.md` synced to the same anatomy and stripped (both are unversioned refs in this skill dir).

## [3.1.0] — 2026-07-18

- No-sidecar harvest (JL, application-only; paper handled separately). Retired the `values:`/`sources:`/`displays:` harvest LANES and the `_VALUES_`/`_CITATION_`/`_DISPLAY_`/`_DESCRIPTIONS/` sidecar docs. ⑤ INTERPRET now writes the answer's numbers/citations INLINE in the section's `a-consumer:`, each anchored `[→ target QA]`; the already-verified `target:` (PASS 1 R19/R20) is the fabrication anchor. Updated: ⑤, the venue-hook section → "Harvest — no sidecar", T1 whitelist, VERIFY, return contract, frontmatter. Checker PASS 2 removed; `harvest-acceptance.md` rewritten.

## [3.0.0] — 2026-07-15

Changed (probe-redesign port; application catches up to paper probe 5.0.0 + the constitution haipipe-probe 9.0.0)
- Rebuilt as THIN DELTAS over the probe constitution (`../../../../probe/haipipe-probe/SKILL.md`): the model — probe-file anatomy, QA state-line contract, cost ladder T0–T4, the two LAWS, derived states, checker FAIL codes — is the constitution's; this file is only the application-side deltas.
- Loop: the 4-step BOOKKEEP→DISPATCH→TRANSLATE→VERIFY becomes the constitution's five-step ORGANIZE → MATCH → DISPATCH → POINT → INTERPRET (⑤ = HARVEST, the worker's own).
- Probe files: per-stage `0-lifecycle/<stage>/_PROBE/PPNN_*.md` cards + the `1-probe-plans/README.md` index RETIRED → flat `1-probes/PPNN_<topic>.md`, one file per TOPIC, each question a SECTION (serves/target/state/q-executor/a-consumer + `## Why`). ORGANIZE migrates a legacy card on first touch.
- Dispatch: the `haipipe-probe-orchestrator-agent` "gateway" framing → the shared `haipipe-probe-q-executor-agent` collector, which runs ②③④ (MATCH/DISPATCH/POINT) in stake-free clean context and writes each `target:`.
- Claim settling: `## Verdict` block, the `verdicted` state, and the G1/G2/G3 review gate DELETED — a probe is communication, not judgment; a full-mode answer's status is written by the author into `0-lifecycle/1c-claims/1c-claims.md` (C-line + Evidence Campaign row), never in the probe file. States drop `dispatched` for the constitution's set.
- Harvest lanes renamed to the constitution's field names — `values:` / `sources:` / `displays:` (were value_refs / pick_list / unit_refs); still venue-scaled HOOKS (application delta), not sub-worker skills.
- `check-probe-cards.sh` replaced by a faithful fork of paper's redesigned 784-line checker (intervention_root vocab, LAW-2 leak lint retuned to intervention vocab, dead-vocab FAIL for `verdicted`/`## Verdict`), minus the paper-only resource-stage pass.
- `ref/per-stage-dispatch.md` and `ref/harvest-acceptance.md` rewritten to the new vocabulary and the collector-dispatch model.

## [2.0.0] — 2026-07-07

Changed (round-2 paper-alignment SOP §4 rows 1-3, resolutions R1 + R5; port of paper probe 3.1.0 enforcement)
- Rebuilt as the 4-step procedure: BOOKKEEP -> DISPATCH -> TRANSLATE -> VERIFY, each step ending in a mandatory PROOF shown in the reply (project_root + ls, the literal Agent call(s), per-card refs + ls + harvest proofs, checker output). A step without its proof did not happen.
- NEW `check-probe-cards.sh` (family-local fork of paper's, stage-strip.sh precedent): read/verdicted ⇒ refs resolve under project_root (brace-aware expand_ref); planned/dispatched cards FAIL (probe-not-run); `harvest: OWED` lane lines FAIL (harvest skipped); no tables, ≤80 lines, status:failed surfaced; working docs scanned for bibtex/tables. Presence-driven exactly like paper's — venue-scaling happens at lane CREATION, so the fork needs no venue lookup. Run at STEP 4 and re-run by the stage CHECK gate.
- Lane obligations: TRANSLATE writes `harvest: OWED` on the lane line FIRST, then dispatches the harvester hook and accepts mechanically; acceptance flips the line to `harvest: accepted (...)`. A skipped harvest now leaves disk residue the checker FAILs.
- Harvester vocabulary: ONE pipeline — ACQUIRE (gateway, the only door) -> HARVEST (venue-scaled lane hooks, pointer-following transcribers). Intervention-side may follow pointers; only the gateway may find things.
- Venue-hook contract (R5, application delta): still NO sub-worker skills — the lanes are hooks that fire venue-scaled (_VALUES_ always; _CITATION_ sectioned venues only; _DISPLAY_ only if the artifact has display units; simple venues have no document lanes) and, when they fire, MUST follow paper's 2.0.0 sub-worker contract: pointer-following + gateway dispatch only, mechanical acceptance greps, no inline search.
- NEW `ref/per-stage-dispatch.md` (re-derived for the application spine: 0-seed, 1-claims, 2-venue, 2-pitch, 3-narrative, 4-display, 5-section-edit; modes light default / full for claims verdicts / background for fresh runs; venue-scaled lane rules; strip forms + OWED gate rule) and `ref/harvest-acceptance.md` (paper's literal greps adapted per lane; citation card format spec stays paper-side, single source of truth).
- Application deltas preserved: claims C-line + Evidence Campaign row flip at TRANSLATE (enum supported | refuted | inconclusive); `_VALUES_` landing; venue scaling; `fn/probe-plans.md` buffer convention.
- Housekeeping: frontmatter still said 1.0.0 while this CHANGELOG already had 1.1.0 (the 765696f port bumped the log only) — resolved by this 2.0.0 bump; entry order corrected to newest-first.

## [1.1.0] — 2026-07-06

- 765696f port: TRANSLATE lands verified numbers in _VALUES_ and flips the Evidence Campaign row alongside the C-line.

## [1.0.0] — 2026-07-06

- NEW phase worker (paper-alignment refactor, SOP archived in haipipe-application/CHANGELOG.md §5.0.0; full-DPRC ruling R4).

## [2.1.0] — 2026-07-09

- BENCH RULINGS (Test-Haipipe-Application): STEP 1.5 RELEASE GATE — planned cards dispatch only on the user's explicit release (`probe run PPNN` / "release PP02" / "release all"); stage handoffs and bare from-buffer sweeps present the planned roster and STOP (PROOF 1.5). No exception for cheap probes.
- PHI-adjacent task dispatches pin the MINIMAL aggregate-safe column allow-list in the prompt by default (aggregates-only outputs); restricted-vs-full is never asked mid-flow; org PHI gates apply on top.
- (Earlier same day, logged under family 6.1.1: two-level _PROBE glob fix in check-probe-cards.sh.)

## [2.2.0] — 2026-07-09

- GROW-loop support: the values lane REDIRECTS for rung 1a — descriptions-stage probes land their harvest in `_DESCRIPTIONS/DS<n>_<name>.md` (per-dataset profile sheet: field inventory + Field Disposition + readable landed profile; quoted-only, anchored + dated). Same OWED/accepted debt bookkeeping; the 1a doc keeps one-line D entries.
