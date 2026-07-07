haipipe-paper-draft — Changelog
===============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [3.5.0] — 2026-07-07

Fixed (skillset-diagnose FIX round; findings A1/A2/A4/A6 + thread T3)
- Template registry (A1, 🔴): all five `../ref/<stage>-template.md` rows were off by one level (resolved to nonexistent `1-lifecycle/<stage>/ref/`); now `ref/<stage>-template.md` relative to each stage skill's OWN folder, with the resolution rule spelled out.
- Artifact-spec path (A2): `1-lifecycle/{stage}/SKILL.md` → `1-lifecycle/{stage}/haipipe-paper-{stage}/SKILL.md`.
- Archive pointer (A4): "2-phase/_archive/" → paper-root `_archive/` (the real location).
- Duplication (A6): the seed stage-note no longer restates the fuel-not-evidence rule; it back-references Step 4 (the one normative home).
- FORWARD handoff (T3, JL: "同意。"): seed note now states the claims stage CONSUMES the `[FORWARD -> CLAIMS]` pointers at its open; claims stage-note gains the reader line. Reader clause itself lives in haipipe-paper-claims 4.1.0.

## [3.4.0] — 2026-07-07

Changed (DRAFT may orient via WebSearch -- validated by the Paper-CGMtoCyclePhase session where inline CGM-x-cycle search drafted the seed, then the real PROBE ran)
- allowed-tools gains WebSearch, WebFetch.
- Step 4: inline search is DRAFTING FUEL, not evidence -- two legal destinations (prose with (Author Year) placeholders; buffered `status: planned` PP skeletons). FORBIDDEN: findings/refs/takeaways into a PP card. The line is card state; CHECK-gate checker blocks planned/empty-ref cards from going green.
- seed stage-note: PROBE is FEASIBILITY only (novelty + external-data-obtainable); internal-data profiling forward-points to CLAIMS via a `[FORWARD -> CLAIMS]` _LOG pointer. (Also corrected the stale "seed PROBE: n/a" line.)

## [3.3.0] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER->PROBE, POLISH->REVISE).

## [3.2.0] — 2026-07-03

- DRAFT-oriented cleanup. Archived leftover venue LaTeX templates (templates/) and the 3 write-* style skills to 2-phase/_archive/ (venue knowledge belongs in _venue/ packs, prose style in POLISH). Step 1 now reads the stage's template from 1-lifecycle/ via an explicit registry table; this skill carries no templates of its own. Added venue guard: venue-ALIGNED stages STOP with status: blocked when no venue is pinned or no pack matches; missing per-section style file proceeds with a flagged warning, never silently invented norms.

## [3.1.0] — 2026-07-03

- reframed as internal worker. Users invoke stage skills (seed, claims, pitch...), not this skill directly. Stage skills call this during their DRAFT phase.

## [3.0.0] — 2026-07-03

- rewritten as generic stage-aware DRAFT hub. Section-specific outline format moved to 1-lifecycle/5-section-edit/ref/outline-format.md. Draft now works for all stages (seed, claims, pitch, narrative, display, section-edit).

## [2.0.0] — 2026-07-02

- complete rewrite for section-edit outline creation.

## [1.1.0] — 2026-06-05

- renamed from paper-write to haipipe-paper-section-edit-write.

## [1.0.0] — 2026-05-31

- baseline metadata added.
