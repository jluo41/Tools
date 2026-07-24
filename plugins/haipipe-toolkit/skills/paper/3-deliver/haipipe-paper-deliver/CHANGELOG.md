haipipe-paper-deliver — Changelog
=================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first. Rollup: layer-level `paper/CHANGELOG.md`.


## [0.1.0] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.0.1; older entries below keep their original numbers).

## 1.0.1 — 2026-07-19

- WIKI RETIREMENT — the retired wiki folder's `13-tex-quality.md` (8 referrers) absorbed here as the **Lifecycle TeX Quality Standard** section; this skill is now its ONE home, and every referrer points at the section instead of the file. It lands in the group that PRODUCES compiled artifacts (`3-polish` mutates the draft, `4-ship` compiles it), while binding upstream writers too — the scope note keeps it explicit that `1-lifecycle/4-display` and `5-section-edit` meet the same bar when they write tex.
  - Carried intact: the scope limit (display `4-display.tex` + `0-sections/*.tex` ONLY; all other stages are markdown and do not compile), the three rules (SELF-CONTAINED with its minimal preamble, REAL PROSE — a tex compiling to a blank page is a defect, SENTENCE-INDEXED with `Pn.Sm` tags + the 3-line paragraph banner), the compile rule (twice when refs/citations present, then clean aux; a stale PDF is a defect and the SKILL not the user must compile), and the .gitignore note (display PDFs are tracked deliverables).
  - The `\needprobe{}` cross-reference repoints from `ref/evidence-routing.md` to the Evidence Routing Protocol section in `../../haipipe-paper/SKILL.md`; the sentence-format pointer resolves to `../../2-phase/REF/sentence-format.md`.
- First CHANGELOG for this skill.
