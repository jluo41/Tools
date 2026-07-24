haipipe-paper-enter — Changelog
===============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [0.4.1] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 4.1.1; older entries below keep their original numbers).

## 4.1.1 — 2026-07-19 — vocabulary: a probe question is an ENTRY, not a SECTION

### Changed
The probe file's unit of one question was renamed `## Q-<Stage>-<n>` SECTION (flat `serves:` /
`target:` / `a-consumer:` fields) -> `## QX<n>` ENTRY (four `###` subsections) when the probe model
changed. This file still said SECTION, so an agent reading it wrote the OLD flat structure, which
`check-probe-cards.sh` FAILs as `stale-old-format` -- that stage's PROBE phase could then never go
green. Mechanical rename, no design change. (JL ruling 2026-07-19, board 260719-04-SEED-2PHASE D5:
"如果这样的话，那还是叫entry 吧". Swept 31 lines across 15 files; phrase-level, because "section"
also legitimately means a MANUSCRIPT section in these docs.)

## 4.1.0 — 2026-07-19

Changed (JL 2026-07-19, paper/2-phase refactor — the sidecar model is retired: `1-probes/` is the only consumer-side source of truth)

- **The console no longer SCORES a document nobody writes.** The phase-derivation rules read `cite ✅ if _CITATION_ all placed and density >= venue norm` and `val ✅ if _VALUES_ all verified` — a metric the Console could not compute, over files that are not created. Re-rooted onto what exists on disk: `draft` now checks that every hole is FILLED or OWNED (each `\cite{TOADD}` / `{VAL:?` carries a `[Q-<Stage>-<n>]` id; `🕳️ N` counts unowned holes), and `probe` reads the paper's `1-probes/` entries (`**state**` + whether `### a-executor` is filled; `📨 N` counts entries still open).
- **The phase strip is FOUR glyphs, one per phase, at every stage** — `draft │ probe │ revise │ check`. The `probe: cite X val X disp X` sub-track split is gone from the Line-2 spec and from both rendered examples; it mirrored three lane workers that no longer exist, and it made section-edit render a different strip shape than every other stage.
- **Read Order step 4** re-rooted: scan `5-section-edit/` for section `.md` + `_LOG_*` files (was: + `_CITATION_*`, `_VALUES_*`). New step **4b** reads `1-probes/PP*.md` — named as the source the `probe` glyph derives from, so the Console reads the questions before it reports on them.

## 4.0.2 — 2026-07-19

- WIKI RETIREMENT — the retired wiki folder's `05-paper-dashboard.md` absorbed here as the **Dashboard Spec** section (inserted between Read Order and Diagnosis Rules, where the console actually uses it). It IS this skill's dashboard spec, so this skill is its ONE home.
  - Carried intact: the Golden Rule (never report a stage done because STATUS.md says so; disk wins, the gap is DRIFT), the lifecycle-frontier spine + per-stage done-predicate table + next-action commands, the note that `1-resource`/`1-claims` share the number 1 on purpose (`stage-strip.sh` strips the digit), the OK/ACTIVE/TODO/DRIFT/BLOCKED glyphs, the 5-step shallow check, the render skeleton (paper header → Story line → 进度 spine) with its per-stage glyph legend and the worked MedJournal example, the field-source table, and the Open needs block.
  - Deduped rather than duplicated, since this file already restated parts of the spec: the resource exemption keeps its single full statement in Diagnosis Rules (the spec's frontier table points there), and the maturity ladder is MERGED into the existing evidence→maturity table, which gains the rungs the wiki carried and this file lacked (`scaffold`, `display-map`, `submitted`, `accepted/published`) plus the fuller `resource` / `resource-blocked` definitions.
- Reference rewiring after the wiki retirement: `Read first:` drops the dashboard entry (the spec is in this file now) and repoints rounds -> `../haipipe-paper-round/SKILL.md`, skill structure -> `../../README.md`, delivery need -> `../../haipipe-paper/SKILL.md`; the stale-deliverable flag now cites the Lifecycle TeX Quality Standard in `../../3-deliver/haipipe-paper-deliver/SKILL.md`.

## 4.0.1 — 2026-07-14

- Need-diagnosis table: "a BUILD card whose eta: has passed" -> "a BUILD section"; "the gateway mints the PP and picks the type" -> "the PROBE worker opens the SECTION and routes it".

## [3.3.0] — 2026-07-14
## 4.0.0 — 2026-07-14

- PROBE REDESIGN (Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, approved JL 2026-07-14 — R1-R18). 1-probe-plans/ -> 1-probes/ (PPNN_<topic>.md, one file per TOPIC, one SECTION per question: serves/target/state/commission/reading + ONE `## Why` per file holding the stake). Binding is by PATH: a section's `target:` points at the answering `<leaf>/QA/<n>-<slug>.md` in the bank. DELETED: `## Verdict`, the `verdicted` and `dispatched` states, `_ASK/`/`_ANS/` stubs, `answers:`, and Agent(haipipe-probe-orchestrator-agent) (the GATEWAY — archived + de-registered). A claim's STATUS now lives ONLY in 0-lifecycle/1b-claims/1b-claims.md. Dispatch is now DIRECT: the section's `commission:` block, VERBATIM, to Agent(haipipe-task-orchestrator-agent) / Agent(haipipe-discovery-orchestrator-agent).
- 'landing a settled verdict in a 1-probe-plans/PPNN card' -> 'landing a settled claim status in 0-lifecycle/1b-claims/1b-claims.md'.

Fixed
- **The console shipped the 7-stage spine and contradicted its own script.** `stage-strip.sh` had rendered 9 stages since the resource ruling landed, while this SKILL.md mentioned `resource` zero times — every strip example, the frontier table, the maturity table and the routing table were all pre-resource. Repaired throughout.
- Frontier-diagnosis table: `seed exists but claims are absent/thin -> 0-seed -> 1-claims` (seed handing straight to claims) SPLIT into `0-seed -> 1-resource` and `1-resource -> 1-claims`.
- **Resource exemption carried into the console (`n/a` COUNTS AS PASS).** Every live paper predates the stage (shipped 2026-07-14); without the exemption every one of their frontiers REGRESSES to `resource` and the console reports DRIFT on seeds JL personally approved. Backwards-only and per-paper: a paper seeded after 2026-07-14 gets no exemption. Also states that `resource ⬜` in the strip is the strip's artifact test, not drift.
- Maturity table: added the `resource` and `resource-blocked` rungs (the latter from the stage's `park` exit).
- Free-form routing table: added the `resource` verb (+ prereq / "do we have the data" / "does the checkpoint exist").
- Open-needs table: added the `1-resource` surface (unanswered `Q<n>`, or a BUILD card whose `eta:` has passed).
- Loopback table: added `1-resource` (resource cannot carry the claim) and `0-seed` via resource's `reseed` exit (every demand row unobtainable).
- Read Order: added `0-lifecycle/1a-resource/1a-resource.md`.
- All six stage-strip examples regenerated to the real 9-stage output of `stage-strip.sh` (verified against live papers Paper-ScalingGlucose-NatSeries2026 and Paper-PersonalizedGlucoseModel), including a new resource-stage example.

## [3.2.2] — 2026-07-03

Fixed
- Focus Strip: added the exactly-one-🔥-one-🚀-never-zero rule with the virgin-paper collapse case (`draft 🔥🚀`); examples reordered so the frontier/default case leads and a fresh-paper-at-seed example added (loopback examples kept, labeled as such).

## [3.2.1] — 2026-07-03

Fixed
- Return Contract still carried the retired 4-field tail (status / paper_root / current_layer / next); the live test session rendered it. Replaced with the umbrella Closing Block shape (status merged with active stage, no paper_root/current_layer) and pointed to haipipe-paper/SKILL.md as the single source of truth.

## [3.2.0] — 2026-07-03

- GET-OR-CREATE absorbed (JL: 直接去掉create，enter的时候没有就call create): a missing path now offers to create the paper -- confirm-gated (repo creation is outward-facing), org resolved per invocation, repo-backed inside Project-* repos per the papers-inside recipe, contents scaffolded via haipipe-paper-lifecycle folder, double-bump, then straight into the console. The umbrella's create verb is retired (haipipe-paper 2.4.0).

## [3.1.1] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER -> PROBE, POLISH -> REVISE); phase strip line now 'draft │ probe: cite val disp │ revise │ check' (stages without sub-tracks show just 'probe').

## [3.1.0] — 2026-07-03

- focus strip dual markers -- 🔥 (active now) + 🚀 (frontier reached); both appear on stage and phase lines, collapse to 🔥🚀 when coincident; convention codified in 01-focus-strip-markers.md; added a shared-reference folder parallel to feedback/.

## [3.0.0] — 2026-07-02

- lifecycle reorder (seed -> claims -> venue -> pitch -> narrative -> display -> section-edit); claims is stage 1 (venue-free), pitch is stage 2 (venue-aligned); minimap removed; section-edit replaces write/edit with per-section DGPC status grid (DRAFT/GATHER/POLISH auto, CHECK human); updated file paths, stage strip, diagnosis rules, free-form routing, and dashboard format.

## [2.1.0] — 2026-06-22

- dashboard leads with pitch summary + stage strip before operational details; read order prioritizes 1-pitch.tex; return contract enforces structured tail + failed status; stale-deliverable flag from 13-tex-quality.md.

## [2.0.0] — 2026-06-22

- reframed as the Paper Console; added derive-from-disk frontier, free-form routing, copilot policy, and .paper-console.yaml session state.

## [1.2.0] — 2026-06-21

- open-needs paper session loader.
