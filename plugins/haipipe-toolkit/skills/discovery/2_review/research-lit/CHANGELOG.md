research-lit — Changelog
========================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.

## 0.2.2 · 2026-09-07

- Adapt the Science Superpowers prior-work lens into HAI terms: methods,
  confounds, effect sizes, and relationship-to-prior-work are evidence-backed
  fields, not a second novelty verdict.
- Make Research Wiki ingestion explicitly standalone-only so durable
  Discovery dispatches cannot write outside the D1 Folder authority boundary.

## 0.2.1 · 2026-09-07

- Normalize the `gemini-search` Discovery worker name to the `gemini` source ID.
- Add explicit clinical PubMed/medRxiv coverage and Crossref/PubMed resolver
  guidance.
- Add a Discovery output mode that returns Result-backed synthesis to the
  dispatcher instead of writing a competing citation table or `references.bib`.
- Scope the standalone `references.bib` snippet to one-off calls only.
- Clarify that load-bearing cross-Task papers require a local paper-analysis
  Run before entering the current Task's derived Bib; non-paper Subjects retain
  source-analysis.

## 0.2.0 · 2026-09-07

- Add opt-in OpenAlex and Gemini source adapters from ARIS `0472e53`.
- Keep the HAI Discovery dispatcher as the authority for canonical Subjects,
  per-paper Runs, Result Cards, and Bib verification.

## [0.1.1] — 2026-09-04

- Move the invocation hint under supported metadata and repair the canonical
  reviewer-routing and integration-contract links.

## [0.1.0] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.0.0; older entries below keep their original numbers).

## [1.0.0] — 2026-05-31

- baseline metadata added.
