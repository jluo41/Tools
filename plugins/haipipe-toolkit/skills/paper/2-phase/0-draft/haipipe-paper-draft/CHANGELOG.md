haipipe-paper-draft — Changelog
===============================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## 4.1.0 — 2026-07-14

- The RAISED-QUESTIONS destination points at `haipipe-paper/fn/probes.md` (renamed from fn/probe-plans.md).
- FORBIDDEN-in-DRAFT restated in section vocabulary: no `reading:`, no `target:`, no finding written into a probe section; the DRAFT/PROBE line is SECTION STATE.
- resource stage note: the PROBE WORKER opens the section and writes the `-> PP<NN>` backlink (was "the gateway mints the card").

## [3.10.0] -- 2026-07-14
## 4.0.0 — 2026-07-14

- PROBE REDESIGN (Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, approved JL 2026-07-14 — R1-R18). 1-probe-plans/ -> 1-probes/ (PPNN_<topic>.md, one file per TOPIC, one SECTION per question: serves/target/state/commission/reading + ONE `## Why` per file holding the stake). Binding is by PATH: a section's `target:` points at the answering `<leaf>/QA/<n>-<slug>.md` in the bank. DELETED: `## Verdict`, the `verdicted` and `dispatched` states, `_ASK/`/`_ANS/` stubs, `answers:`, and Agent(haipipe-probe-orchestrator-agent) (the GATEWAY — archived + de-registered). A claim's STATUS now lives ONLY in 0-lifecycle/1-claims/1-claims.md. Dispatch is now DIRECT: the section's `commission:` block, VERBATIM, to Agent(haipipe-task-orchestrator-agent) / Agent(haipipe-discovery-orchestrator-agent).
- DRAFT is the birthplace of the QUESTIONS: it now RAISES each gap as a `state: planned` SECTION in 1-probes/PPNN_<topic>.md (writing the `commission:` in general language, NEVER the `## Why`), instead of buffering a `status: planned` PP-card skeleton with Need/Why/Route + empty refs — a shape the rewritten checker FAILs (no-state-field / no-commission). Ports the application DRAFT worker's already-landed v1.2.

Fixed (the RESOURCE stage was unreachable from the DRAFT worker)
- The new venue-FREE `resource` stage (`1-lifecycle/1-resource/haipipe-paper-resource/`) resolved NEITHER an artifact-spec row NOR a template path here, so a `resource` DRAFT had no format source at all. Added:
  - Step 1 registry row: spec `1-lifecycle/1-resource/haipipe-paper-resource/SKILL.md`, template `ref/resource-template.md` (the template itself now exists, shipped with the stage).
  - Step 2 upstream row: `resource` reads seed (Tentative Claim Shape + `_LOG_0-seed.md` forward pointers); `claims` now reads seed + resource.
  - Step 3 "Settle structure" line: resource = the two sections (Demand `N<n>` / Questions `Q<n>` + `A`), nothing else.
  - Stage-specific notes `### resource`: output path, the two-section artifact (and the sections JL CUT), the glyph- and legacy-tolerant `[FORWARD -> RESOURCE|CLAIMS]` consume grep, "the stage ASKS -- no PP ids, no probe types, never executes", "PROBE = exactly ONE worker call per pass, never inline", "no sidecars", ends at the GATE-1 hard STOP (which approves the QUESTIONS, not the SPEND -- spend is authorized at the stage's GATE 1b, per haipipe-paper-resource 1.1.0).
  - "Who calls this skill" row for `haipipe-paper-resource`.
- Venue guard: the venue-FREE set was stale (`seed, claims`) -- it is now `seed, resource and claims`.

Fixed (forward-pointer DOUBLE CONSUMPTION -- companion to haipipe-paper-claims 4.5.0)
- Stage-specific notes named CLAIMS as the consumer of seed's FORWARD pointers, while the new `### resource` note (above) named RESOURCE. Two consumers for the same 7 live pointers = a permanent deadlock at the claims CHECK gate (resource takes the pointer; the pointer LINE still sits in `_LOG_0-seed.md`, so claims' old "no unconsumed pointer" bar could never clear) -- or a double-dispatch of the same build if the agent re-materialized it as a PP entry. RESOURCE is now the SOLE consumer:
  - `### seed`: internal-data profiling forward-points to `[FORWARD -> RESOURCE]` (was `CLAIMS`); an unconsumed pointer fails the RESOURCE done-criteria, not claims'.
  - `### claims`: the "grep seed `_LOG` for `[FORWARD -> CLAIMS]`" line is GONE. Claims reads `_LOG_1-resource.md` and picks up ONLY the pointers resource explicitly DECLINED to it.

## [3.9.0] -- 2026-07-10

Changed (JL ruling: real citations from .bib in the draft)
- Draft prose writes real `\citep{key}` for keys grep-verified in the paper's .bib (check .bib + _CITATION_ FIRST); `\cite{TOADD}` + `_CITATION_` row where no key fits. Supersedes `[CITE: <topic>]` and "(Author Year)" placeholders. A key that does not grep in .bib is an invented citation.

## [3.8.0] -- 2026-07-09

Changed (JL 2026-07-09: "draft = review the section + propose what probes to do")
- section-edit stage note: drafts end with the "Probes proposed by this draft" block per the stage template; heavier needs buffered as planned PP skeletons; the STOP presentation includes the block.

## [3.7.0] -- 2026-07-09

Changed (JL ruling 2026-07-09 (LLMTrait-Section session postmortem): normalize the writing process)
- Section drafts are REAL prose: complete sentences close to submission register, {VAL:? <what>} / [CITE: <topic>] placeholders, never invented numbers/citations. Argument docs unchanged (working prose).
- Step 5 renamed to "STOP -- present for review, then iterate": writing done -> end the turn; the user's verb/"go" is the gate. Never start PROBE/REVISE/commit on your own.
- Step 6 hand-off writes the [GATE] draft-review: approved line quoting the user; skips require a logged verdict.

## [3.6.0] — 2026-07-08

Changed (venue lockfile wiring)
- Venue guard + style-source table repointed: primary venue read = the paper's `0-lifecycle/2-venue/2-venue.md` (Writing Principles + Structural Blueprint block); direct `_venue/` pack reads demoted to fallback (2-venue.md absent) or deep dives via its `[source: ...]` tags; pinned-but-no-pack STOP kept in the fallback branch.

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
