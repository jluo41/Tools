haipipe-discovery-synthesize — Changelog
=========================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions
match SKILL.md frontmatter `version:`. Newest first.

## 0.2.0 · 2026-09-08

- Add external synthesis procedures for thematic organization, citation
  genealogy, Result-to-Claim support, and post-synthesis citation audits.
- Require external worker output to be normalized and verified before Page
  CONTENT is written; no external worker gains Run, Result, or Bib authority.
- Reserve citation-fidelity and reference-verify for per-Result checks; only
  citation-audit may hold the cross-Result/Page CHECK.

## 0.1.0 · 2026-09-07

- Add the live `3_synthesize` capability family for cross-Result Discovery
  synthesis and the D1 SYNTHESIZE → Page CONTENT handoff.
- Separate per-Subject review from cross-paper integration without creating an
  additional Run, Result, or Bib authority.
