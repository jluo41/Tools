haipipe-paper-probe-values — Changelog
======================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [2.1.2] -- 2026-07-10

Fixed (fresh-agent audit, C10)
- AUDIT and PLACE target the section WORKING .md ({VAL:?} slots + literal numbers); tex only post-sync (was tex-only, impossible at PROBE time in the md-first pipeline).

## [2.1.1] -- 2026-07-10

Changed (JL: "we prefer to probe previous stages' outcome")
- Sweep tier clarified: ANY stage's read|verdicted PP cards count (seed, claims, display included), via value_refs OR refs.

## [2.1.0] -- 2026-07-10

Changed (JL: "will it search the previous lifecycle stages's content and display as well?")
- ROUTE gains the PAPER-LOCAL SWEEP tier between named-source and probe-plan: sibling/prior _VALUES_*.md, read|verdicted PP cards' value_refs, 0-displays/*/source/ (metrics.json, source_data.csv), _EVIDENCE_1-claims.md. Exempt from the trace-as-grep ban: these are the paper's own curated indexes.
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
