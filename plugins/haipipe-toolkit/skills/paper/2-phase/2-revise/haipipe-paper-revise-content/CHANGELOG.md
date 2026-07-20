haipipe-paper-revise-content — Changelog
========================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## 1.4.0 — 2026-07-19 — placeholder contract updated; comment-first residue removed from ref/

From the `paper/2-phase` review (`../../../_console/260719-02-PHASE-BOUNDARY-REFACTOR.md`).

### Changed (JL: "\\cite{TOADD} [Q-XXX-N] So I want something like this.")
Every placeholder this worker leaves or checks now carries the id of the question that will settle it — `{VAL:? <what>} [Q-<Stage>-<n>]`, `\cite{TOADD} [Q-<Stage>-<n>]` — two markers side by side, never fused. A placeholder without a bracket is a hole nobody owns.

### Changed — scope boundary restated
The skill said it defers verification to two workers that no longer exist. It now points at `haipipe-paper-check-evidence` for verification and notes that `haipipe-paper-revise-place` has ALREADY run, so any placeholder still standing when this worker sees it is genuinely still owed — leave it, and leave its bracket intact.

### Fixed — 🔴 `ref/content-edit.md` instructed the opposite of the skill
The ref opened with "In Round 1 each failed checkbox becomes one comment … **you change no prose**. The fixes described below happen only in Round 2, after the human replies `accept` / `modify`" — pre-DPRC residue contradicting this skill's own "REVISE is fully automatic … applies changes directly, no human gate". A worker loading that ref would refuse to edit anything. Rewritten as an edit list.


## [1.3.0] -- 2026-07-10

Changed (fresh-agent audit, C8 -- R1 alignment)
- Retired % TODO[values] / % TODO[cite] placeholders throughout SKILL + ref/content-edit.md + ref/weaving.md; the conventions are {VAL:? <what>} and \cite{TOADD} (+ _CITATION_ row).

## [1.2.0] — 2026-07-07

Added (T7, JL: "我们需要weaving吗？如果不需要的话，可以就删掉吗？" → "maybe just go into Content")
- Absorbed the retired haipipe-paper-revise-weaving skill: the pass is now section → paragraph → WEAVE → sentence. The weave step (ARC / HINGES / RHYTHM, 🔴🟡🟢 severity discipline, role-emoji vocabulary) lives in `ref/weaving.md`; `ref/write-principles.md` + `ref/example-intro-logic-flow.txt` moved in from the weaving skill. The retired skill's orchestration apparatus (routing, approval gates, embedded %%@ plan blocks — pre-DPRC comment-first machinery that contradicted fully-automatic REVISE and fought the router, finding C11) is archived at paper/_archive/paper-revise-weaving-skill/, not carried over. C9/C10/C11 are moot with the retirement.

## [1.1.1] — 2026-07-07

Fixed (skill-family quality sweep)
- Frontmatter normalized to the family baseline: added the two missing standard keys `argument-hint` and `allowed-tools` (Bash, Read, Write, Edit, Grep, Glob — leaf worker, no Skill dispatch), added the standard `metadata.summary`, and dropped the three nonstandard keys `status` / `stage` / `topic`.

## [1.1.0] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER->PROBE, POLISH->REVISE).

## [1.0.0] — 2026-07-03

- removed comment-first protocol. POLISH is now fully automatic (apply directly, leave explanatory comments for CHECK). Aligned with DGPC architecture where only CHECK is human-involved.

## [0.1.0] — 2026-06-29

- initial version with comment-first protocol.
