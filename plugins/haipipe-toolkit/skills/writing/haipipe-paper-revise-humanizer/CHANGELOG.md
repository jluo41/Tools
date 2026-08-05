## 0.2.6 — 2026-08-05

- Shared prose rules repointed to `paper/haipipe-paper/ref/prose-quality.md`
  (ex `paper/workers/REF/`, dissolved in thin-paper phase 2). Frontmatter also
  catches up with the 0.2.5 entry below, which had not been reflected there.

## 0.2.5 — 2026-08-01

- Layer 1 of `ref/pattern-catalog.md` moved to
  `skills/writing/haipipe-writing/ref/ai-tells.md` (JL). It is register-agnostic
  and no paper owned it. Layers 2 to 6 stay: they are academic.
- Candidate diffs are now COMPUTED by `haipipe-writing/cli/wdiff.py` instead of
  written by hand. The notation still differs per host; the computation does not.

haipipe-paper-revise-humanizer — Changelog
==========================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [0.2.3] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 2.3.0; older entries below keep their original numbers).

## [2.3.0] — 2026-07-07

Changed (JL: "Could you copy the content from refences to our skillset? Our skill should never refer to the references content.")
- Pattern catalog VENDORED into the skill: `ref/pattern-catalog.md` (from AIScientists-Dev/academic-humanizer @ 02281d8, MIT) + `ref/before-after.md` examples. All runtime pointers at `Tools/references/...` removed; the references/ submodule is archival provenance only. House rule codified in the Reference section: skills are self-contained, never depend on references/ content at runtime.
- Relation box updated: weaving merged into content (T7).

## [2.2.0] — 2026-07-07

Fixed (skillset-diagnose T6, JL: "做B" — re-vendor now, don't soften)
- The "empty catalog" mystery solved: `Tools/references/academic-humanizer/` was a half-registered git SUBMODULE (gitlink 02281d8 committed, but no .gitmodules mapping — so fresh checkouts silently got an empty dir). Fixed by cloning AIScientists-Dev/academic-humanizer at the exact pinned commit and adding the missing .gitmodules entry. The full pattern catalog (SKILL.md + examples/ + assets/) is on disk again; C7/C8 contradictions dissolve because the assertions are now true.
- NOTE rewritten: documents the submodule + `git submodule update --init` recovery, keeps the inline Six-layer audit as the offline fallback.
- Added the missing `feedback/` inbox (C12 — was the only revise worker without one).

## [2.1.1] — 2026-07-07

Fixed (skill-family quality sweep)
- Broken reference path: the "Path:" line resolved to `skills/references/academic-humanizer/` (4 levels up lands in `skills/`, wrong). Corrected to the canonical repo-root `Tools/references/academic-humanizer/SKILL.md` (7 levels up as a relative path). Added an honest NOTE that the reference catalog dir is currently empty in this checkout, so the inline Six-layer audit is self-sufficient; re-vendoring the catalog is a separate task.

## [2.1.0] — 2026-07-03

- phase spine renamed DGPC -> DPRC (GATHER->PROBE, POLISH->REVISE).

## [2.0.0] — 2026-07-03

- removed comment-first protocol. POLISH is now fully automatic (apply directly, leave explanatory comments for CHECK). Aligned with DGPC architecture where only CHECK is human-involved.

## [1.0.0] — 2026-06-29

- created from academic-humanizer repo. Integrated into POLISH phase with comment-first workflow.