haipipe-paper-probe-values — Changelog
======================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## 3.1.0 — 2026-07-14 — the HARVEST gate reads the target's state line (R19/R20)

Phase 3 opened a QA file and transcribed its value anchors with NO state check. On the normal path paper-probe's ⑤ INTERPRET gates it, but the DIRECT invocation form (`harvest <stage> <qa_file>`) is published and was unguarded:

- pointed at a `working` file (whose `## Answer` is EMPTY BY CONSTRUCTION) it harvested ZERO anchors and reported a silent no-op — HIDING a live claim;
- pointed at a `superseded-by:` file it transcribed STALE sources into `_VALUES_`, where PLACE then auto-places source-verified numbers INTO THE MANUSCRIPT. That is the day-1/day-40 stale-read bug arriving through the HARVEST lane, where the checker's `read-target-superseded` tooth cannot see it.

HARVEST now reads `sed -n 's/^- state:[[:space:]]*//p' <file> | head -1` first: REFUSE on `working` (report "in progress since <started>"), FOLLOW THE CHAIN on `superseded-by:`, REFUSE on a missing state line (`qa-no-state`). Read-only — the harvester still NEVER writes a QA file. Twin: `haipipe-paper-probe-citation` 3.1.0.

## 3.0.1 — 2026-07-14

- "PP card refs / value_refs" -> the probe section's `values:` lane and `target:` QA file (pointer-following, unchanged in substance).
- "probe plan" -> question SECTION in the ROUTE phase, the phase table, and the method-claims rule.

## [2.1.2] -- 2026-07-10
## 3.0.0 — 2026-07-14

- PROBE REDESIGN (Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, approved JL 2026-07-14 — R1-R18). 1-probe-plans/ -> 1-probes/ (PPNN_<topic>.md, one file per TOPIC, one SECTION per question: serves/target/state/commission/reading + ONE `## Why` per file holding the stake). Binding is by PATH: a section's `target:` points at the answering `<leaf>/QA/<n>-<slug>.md` in the bank. DELETED: `## Verdict`, the `verdicted` and `dispatched` states, `_ASK/`/`_ANS/` stubs, `answers:`, and Agent(haipipe-probe-orchestrator-agent) (the GATEWAY — archived + de-registered). A claim's STATUS now lives ONLY in 0-lifecycle/1b-claims/1b-claims.md. Dispatch is now DIRECT: the section's `commission:` block, VERBATIM, to Agent(haipipe-task-orchestrator-agent) / Agent(haipipe-discovery-orchestrator-agent).
- The PAPER-LOCAL SWEEP's dead `read|verdicted` PP-card predicate becomes `answered | read | answered-local` probe SECTIONS, reading the `values:` lane / `target:` QA file.

Fixed (fresh-agent audit, C10)
- AUDIT and PLACE target the section WORKING .md ({VAL:?} slots + literal numbers); tex only post-sync (was tex-only, impossible at PROBE time in the md-first pipeline).

## [2.1.1] -- 2026-07-10

Changed (JL: "we prefer to probe previous stages' outcome")
- Sweep tier clarified: ANY stage's read|verdicted PP cards count (seed, claims, display included), via value_refs OR refs.

## [2.1.0] -- 2026-07-10

Changed (JL: "will it search the previous lifecycle stages's content and display as well?")
- ROUTE gains the PAPER-LOCAL SWEEP tier between named-source and probe-plan: sibling/prior _VALUES_*.md, read|verdicted PP cards' value_refs, 0-displays/*/source/ (metrics.json, source_data.csv), _EVIDENCE_1b-claims.md. Exempt from the trace-as-grep ban: these are the paper's own curated indexes.
- Adopt the pointer, never the verdict: reused entries enter ⬜ with `Note: pointer via <file>` and PLACE re-verifies against the ORIGINAL source (Hard Boundary 4 untouched).

## [2.0.0] — 2026-07-07

Changed (Part-0 harvester ruling, JL: "they are the harveste agents... just one step within the whole probe")
- BREAKING: Phase 2 TRACE-as-grep retired → Phase 2 ROUTE. Pointer-following only: the worker reads paths already NAMED (PP card refs/value_refs, _DISPLAY_ registry, _CITATION_, inline derivations) and may NOT grep tasks//code/ to discover sources — "which task has this number" is gateway SWEEP work. Unmatched numbers become probe-plan suggestions; the gateway returns value_refs; Phase 3 harvests them into _VALUES_ entries under the lane's OWED→accepted machinery (mechanical acceptance incl. the number-matches-source grep in harvest-acceptance.md).
- allowed-tools: Agent dropped (harvest dispatch is the hub's job; this skill is read headless by the harvester subagent).
- B4 (earlier this session): self-referential predecessors fixed to name haipipe-paper-manual-review-values.

## [1.1.0] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER->PROBE, POLISH->REVISE).

## [1.0.0] — 2026-07-02

- merged manual-review-values (pre-submission number walk) into one skill with 6 phases. Defined hard boundaries. Defined _VALUES_ format.

## [0.0.1] — 2026-06-29

- stub with scope only.
