haipipe-application-probe — Changelog
================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.

## [4.3.0] — 2026-07-14 — R19 hardening (consumer side)

Mirrors constitution `haipipe-probe` 8.3.0; IDENTICAL to `haipipe-paper-probe` 4.2.0.

- **② MATCH: R14 is SCOPED to `state: answered`.** A `working` file's `## Answer` is EMPTY BY CONSTRUCTION, so it can never pass R14's literally-answers test — and R14's remedy is DISPATCH. Read as written, the second consumer re-dispatches the run the first is still executing. A `working` file is now matched on its `# Q —` LINE: same question ⇒ HIT-IN-FLIGHT ⇒ commission + point, NO dispatch.
- **② MATCH: `owner:` and `eta:` for a HIT-IN-FLIGHT are DERIVED from the target**, not invented at the gate: `owner:` := the target's `by:` (or `bank`), `eta:` := its `started:` + QA_CLAIM_TTL_HOURS. One clock, not two.
- **④ POINT: the ASYNC re-resolve is now ENFORCED.** `commissioned-target-answered` FAILs a section whose answer landed and was never harvested (the in-flight path has no live return, so this is its only road to `read`); `commissioned-target-superseded` FAILs a stale target.
- **A QA file with NO state line is MALFORMED, not legacy.** Do not bind `target:` at it (`read-target-no-state`); only its owner may complete it.
- **check-probe-cards.sh:** new codes `qa-no-state` · `read-target-no-state` · `commissioned-target-answered` · `commissioned-target-superseded` · `commissioned-target-no-state`; the `commissioned-overdue` message now reports the target's ACTUAL state instead of asserting "no QA file" about a file that has been on disk for weeks; a missing `<intervention_root>` fails fast instead of HANGING FOREVER (the `cd` was unchecked and the ancestor walk spun on `dirname "" → . → .`).
- Fixtures re-run on BOTH copies: A (clean read→answered) PASS exit 0 · G (legit in-flight commissioned→working) PASS exit 0 · B/C/D/E/F and the four new ones FAIL exit 1.

## [4.2.0] — 2026-07-14 — the consumer side of the QA STATE LINE (R19/R20/R21)

Follows constitution `haipipe-probe` 8.2.0 (JL ruling 2026-07-14; Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ PART 3b, `>> CC0714`). **Vocabulary is IDENTICAL to the paper twin (4.1.0)** and to the task/discovery executors — the field names, the state values, the TTL constant and the FAIL codes are one set, not four. The twins drifted before; they do not drift here.

**The hole this closes.** Two consumers ask the same question a week apart. The first dispatches an expensive P-B-E-R run. The second, while that run is STILL GOING, sees no QA file — because a QA file was written ONCE, at REPORT, complete, and its EXISTENCE was the only signal — and dispatches THE SAME RUN AGAIN. Nothing prevented it.

Added
- **② MATCH reads the STATE LINE of every candidate QA file. Existence is no longer the signal.** `answered` → a T2 HIT. `working` → ⏳ IN FLIGHT: the question is ALREADY BEING ANSWERED, so the section goes `state: commissioned`, `target:` points at that QA file, and there is **NO SECOND DISPATCH**. `superseded-by:` → FOLLOW THE CHAIN to the live answer; never bind `target:` to a superseded file. No state line → LEGACY (pre-R19), treat as `answered`.
- **④ POINT: `ls` no longer settles the section's state.** The TARGET'S state line does: absent|`working` ⇒ `commissioned` · `answered` ⇒ `answered` · superseded ⇒ re-point. A target still `working` past `QA_CLAIM_TTL_HOURS` (24) means the run is DEAD ⇒ back through ③ DISPATCH.
- **⑤ INTERPRET is legal ONLY against a target that is `answered` and NOT superseded.** Reading a `working` file is reading an EMPTY `## Answer`; reading a superseded one is a reading that is true of an answer that is no longer true.
- **PART 2 states the invariant out loud: ONE WRITER — the EXECUTOR, and nobody else, EVER.** "Write-once" was never the real rule; ONE WRITER was. Two writes by the same owner (the CLAIM at the qa gate's ③ decision, the COMPLETION at REPORT) is fine. This worker must NEVER create, claim, edit, complete or supersede a QA file — not even one it commissioned, not even to clear a zombie claim. A consumer-planted `working` file is the retired `_ASK/` stub wearing a `QA/` costume. Also added as a hard boundary.
- PROOF 2 and PROOF 4 now require the `- state:` line of the file the worker branched on.

**check-probe-cards.sh — FIVE NEW TEETH** (filename unchanged: 65 refs across 33 files; internals only). Each catches a bug that was SILENT before:
- `read-target-working` — a section at `state: read` whose `target:` is a QA file that is `state: working`. The artifact claims it read an UNFINISHED answer.
- `read-target-superseded` — a section at `state: read` whose `target:` carries `superseded-by:`. **THE DAY-1/DAY-40 SILENT-FALSE-CLAIM BUG**: every file internally consistent, nothing a lie, and the claim now FALSE. Nothing fired before.
- `qa-working-no-started` — a `working` QA file with no `started:`: an UNEXPIRABLE claim, so every future reader defers to it forever.
- `qa-working-expired` — a `working` QA file older than `QA_CLAIM_TTL_HOURS`: a ZOMBIE claim from a dead run.
- `qa-answered-empty` — `state: answered` with an EMPTY `## Answer`: a LYING RECEIPT.

Changed
- The new state-line logic is factored into **ONE shared block (`QA_STATE`)**, called by the PASS-1 section-target test and the PASS-3 bank scan — exactly as the LAW-2 lint (`LEAK_AWK`) now is. The two hand-copied checkers had already drifted into IDENTICAL bugs once (4.1.0's entry below); the state block is byte-identical across both copies (verified by diff), and the TTL is referenced by NAME (`QA_CLAIM_TTL_HOURS=24`), never as a literal.
- A QA file with no state line asserts NOTHING (legacy, pre-R19). A gate that FAILs correct work is worse than one that misses.

Verified (fixtures under a temp project, BOTH checker copies, byte-identical output)
- A clean: `state: read` → `state: answered` QA file with a real `## Answer`, **including the false-positive bait** (a commission naming a real path `tasks/.../C3-Visual-ForecastScaling/` and forecast horizons H1/H6) → **PASS exit 0**. The gate was not broken.
- B `read` → `working` target → FAIL. C `read` → superseded target → FAIL. D `working`, no `started:` → FAIL. E `working`, started 3 days ago → FAIL (`72h >= QA_CLAIM_TTL_HOURS=24`). F `answered`, empty `## Answer` → FAIL. All exit 1.
- **G LEGIT IN-FLIGHT**: `state: commissioned` section → `state: working` QA file with a FRESH `started:` → **PASS exit 0**. The change WORKS, rather than merely failing things.
- Regression: the LAW-2 lints still fire on both surfaces — the A03-form bare-label bank leak (`- C6: … → NO`, the slash pair `C6/C7`) and a stake-disclosing commission → FAIL exit 1.

## [4.1.1] — 2026-07-14 — one name per thing

Changed
- Convention pointer repointed: `../../../haipipe-application/fn/probe-plans.md` → `fn/probes.md`. The document is unchanged; only its name is. The paper twin was already `fn/probes.md`, and `skills/STRUCTURE.md:63` lists `1-probe-plans/` among the layer's dead words — so the application bucket was the last place preserving the retired noun as a live filename. One name per thing.

## [4.0.0] — 2026-07-14
## 4.1.0 — 2026-07-14

- DISPATCH prompt now uses the executor orchestrators' OWN input spelling (`action: qa` / `project:` / `question:` / `leaf:`). The v4.0 keys (`project_root`/`qa`/`target`/`deliverable`) matched NONE of their four declared input forms — the payload carried no `action:` at all, which is the field their input spec switches on.
- INTERPRET now actually DISPATCHES `Agent(haipipe-probe-reviewer-agent)` for a `mode: full` section and lands the judgment in 1-claims.md. In v4.0 `mode: full` was documented but UNREACHABLE: no live skill dispatched the reviewer, so a full-mode section could never be judged.
- **check-probe-cards.sh: BOTH LAW-2 LINTS REBUILT ON ONE SHARED PATTERN SET (`LEAK_AWK`).** The v4.0 file carried two hand-copied regex sets, and BOTH had the same two holes: (1) the path-strip deleted EVERY whitespace-delimited token containing a `/`, which ate `C6/C7` and `H1/H2` before any regex saw them; (2) an H/C id was flagged only on a line ALSO carrying claim vocabulary — but the CANONICAL leak is a bare bullet label (`- C6: does WellDoc record any cycle indicator? -> NO`, verbatim what A03's result.md carries), which has no such vocabulary. Net effect: the gate PASSED the exact incident its own header comment claimed it "would have caught", stamping the words `probe-unaware` onto a file soaked in consumer claim ids. Now: narrow path-strip (URLs, known bank/consumer prefixes, extension-bearing slashed tokens — never a claim-id pair) + three independent rules (VOCAB, LABEL, PAIR), with a horizon-aware carve-out in H-space so `- H1: 12.4 mg/dL` and `horizons H1..H6` keep PASSing.
- FIXTURE-VERIFIED, both families: clean probe + clean bank -> all PASS, EXIT=0. Leaked commission (`claim C6 is supported`), bare-label commission (`- C6:` / `- C7 feasibility:` / `- H3:`), dangling `target:`, `state: planned`, overdue `commissioned`, `answered`-not-read, and three contaminated bank QA files (stage words, `C6/C7`+`H1/H2` slash pairs, the real A03 content) -> all FAIL, EXIT=1. FALSE-POSITIVE CONTROL (real path `tasks/C3-Visual-ForecastScaling/`, forecast horizons H1..H6, cohort arms C1/C2, `- H1: 12.4 mg/dL`) -> PASS, on both surfaces.

Changed (PROBE LAYER REDESIGN — Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, APPROVED by JL 2026-07-14, rulings R1-R18; mirrors the paper PROBE-phase worker exactly, application deltas preserved)
- A PROBE IS NOW AN APPLICATION-LEVEL DOCUMENT AND NOTHING ELSE: `1-probes/PPNN_<topic>.md`, one file per TOPIC, one SECTION per question (`serves` / `target` / `state` / `commission` / `reading`), plus ONE `## Why` per file holding the stake — which never leaves the file, is never dispatched, and is never copied. The per-stage `_PROBE/` folder and the `1-probe-plans/` index are RETIRED (legacy locations are globbed and reported as MIGRATE, never silently passed).
- The 4-step procedure (BOOKKEEP -> DISPATCH -> TRANSLATE -> VERIFY) is REPLACED by the FIVE-STEP LOOP: ① ORGANIZE (collect the DRAFT's questions into probe files by topic; write each commission — the T1 translate-down) ② MATCH (grep the bank's QA corpus and READ the hits) ③ DISPATCH ④ POINT ⑤ INTERPRET. The PROOF-per-step enforcement is PRESERVED and extended to six proofs.
- R1 BINDING BY PATH, NOT BY ID: a section's `target:` is a PATH to the answering file. PP numbers are APPLICATION-LOCAL footnote numbers — an application and a paper may both carry a PP03 with nothing to reconcile. No ledger, no renumbering, and **no PP id ever crosses to the bank**.
- R2 THE BANK IS PROBE-UNAWARE: `_ASK/`, `_ANS/`, the `answers:` field, and PP ids under `tasks/`/`discoveries/` are DEAD. The executor answers plain questions through its OWN `qa` verb (`/haipipe-task qa`, `/haipipe-discovery qa`; gate ① QA SCAN ② DIGEST ③ P-B-E-R, or REFUSE) and returns `<leaf>/QA/<n>-<slug>.md`.
- CC-8 THE PROBE CAUSES A QA FILE; THE EXECUTOR AUTHORS IT. This worker now writes NOTHING project-side, ever — the deferred `_ASK` stub write (the one project-side write v3.4 permitted) is GONE. A bare `results/` with no digest gets a DISPATCHED digest-only run, not an inline write. Rationale on disk: `tasks/A03_welldoc_cycle_check/result.md` carries "C6"/"C7" because a consumer session with the stake in context wrote a bank file.
- 💀 THE PROBE GATEWAY IS RETIRED. `Agent(haipipe-probe-orchestrator-agent)` no longer exists; its SWEEP became step ② MATCH, and its dispatch is now a DIRECT `Agent(haipipe-task-orchestrator-agent)` / `Agent(haipipe-discovery-orchestrator-agent)` call. Their clean context IS the wall. (The `haipipe-probe-review` skill + reviewer agent SURVIVE — consumer-side claim judging.)
- R13 COST LADDER (T0 JOIN / T1 LOCAL / T2 REUSE / T3 ENRICH / T4 FRESH): only T3/T4 summon an agent, and **most sections should land on T2** — the bank fills autonomously from executor sessions (R17), so a commission is the EXCEPTION, not the norm. A probe file whose every section is T3/T4 is a smell the worker must name.
- R14 MATCH ON THE ANSWER, NEVER ON THE TOPIC: a hit counts only if the QA file LITERALLY ANSWERS the question. READ it; topic similarity is not evidence.
- R15 the ENRICH DEPTH LADDER (read | new run | new script | new leaf) is the EXECUTOR's private business — this worker never learns which depth was used, and never asks.
- R7 "VERDICT" IS DEAD: the `## Verdict` block and the `verdicted` state are DELETED. A claim's status (`supported | refuted | inconclusive` + confidence + claim_type + G1/G2/G3) lands in `1-claims.md` — per-claim, per-consumer, private. (A DISCOVERY's own `verdict.md` terminal file is a DIFFERENT thing and SURVIVES.)
- THE TWO LAWS, cited verbatim and now mechanically enforced. LAW 1: a consumer session never executes task/discovery work inline — dispatch = hand the `commission` block, verbatim, nothing else. LAW 2: lint BOTH surfaces (probe commissions carry no consumer vocabulary or stake; bank `QA/*.md` carry no consumer vocabulary).
- PRESERVED, unchanged in substance: the BUILD-lane `commissioned` state (JL rulings C4+C6, 2026-07-14) with `owner:`/`eta:`/`blocks:`/`cross-project:` — a FUTURE eta PASSES the gate, an OVERDUE one HARD FAILs; the venue-scaled harvest lanes as HOOKS (no probe sub-workers): `values:` always, `sources:` sectioned venues only, `displays:` display-unit venues only; the display-request reroute; the `--stage` filter that keeps one in-flight build from redding every downstream gate.

Changed — check-probe-cards.sh (KEEPS ITS FILENAME; 65 refs across 33 files. INTERNALS rewritten.)
- Now checks probe FILES made of question SECTIONS, not cards. THREE PASSES: (1) per-section — state derivation, `target:` resolution on disk, `planned` FAILs as probe-not-run, `answered`-but-unread FAILs, `commissioned` requires owner+eta+blocks+cross-project with a FUTURE eta (overdue = HARD FAIL), LAW-2 commission lint, `harvest: OWED` FAILs, no markdown tables, exactly one `## Why`, dead vocabulary (`verdicted`/`## Verdict`/`## Takeaways`/`answers:`/`_ASK`/`_ANS`) FAILs; (2) working docs — no bibtex, no tables in `_CITATION_`; (3) **THE BANK** — every `{tasks,discoveries}/**/QA/*.md` linted for consumer vocabulary and stake disclosure, PP ids in a bank filename FAIL, and the RETIRED `_ASK/`/`_ANS/` mailboxes FAIL if they exist. Pass 3 is what would have caught A03, which had no `_ASK` at all — the v1 bridge pass could never have seen it.
- The section lint is deliberately CONTEXT-AWARE (an H/C id is flagged only where it is used AS A CLAIM ID, on a line also carrying claim vocabulary; paths are stripped first). This domain legitimately uses `H1` (a forecast horizon), `C2` (a cohort arm), and real task paths — a gate that fails correct work gets muted, and takes the real detections down with it.
- Three portability bugs found and fixed while smoke-testing the rewrite, each of which would have produced CONFIDENT WRONG ANSWERS rather than errors: a printf arg/format mismatch; TAB as the record separator (tab is IFS-whitespace, so every empty field silently SHIFTED the record); and `{n}` regex intervals (unsupported by default in mawk, so EVERY eta would have read as absent and an overdue build would have reported as "no eta" instead of OVERDUE).

Changed — refs
- `ref/per-stage-dispatch.md`: re-derived for the five-step loop, the cost ladder, and the retired gateway; per-stage list keyed on `serves:`; phase-status gate rule now also fails a `planned` section and an OVERDUE `commissioned` one.
- `ref/harvest-acceptance.md`: the harvest now reads the ANSWER (the QA file's anchors), not the bank. Lane names follow the section fields (`values:`/`sources:`/`displays:`). Adds an explicit "what a hook may NEVER do": write under `tasks/`/`discoveries/`, or search.

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
