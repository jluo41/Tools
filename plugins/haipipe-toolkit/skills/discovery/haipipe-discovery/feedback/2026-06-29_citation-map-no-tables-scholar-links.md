---
status: fixed
created: 2026-06-29
updated: 2026-07-03
occurrences: 1
context: §3 theory citation map formatting
fixed_in: "2.4.0"
regressed: ""
---

When discovery produces citation lists or source inventories, NEVER use tables. Each citation/source is its own markdown section (### heading) with the full paper title in the heading (e.g., `### Graziano, Jensen-Campbell, & Hair (1996). Perceiving interpersonal conflict and reacting to it.`). Below the heading, bullet-point fields: Key, Journal, Status, Scholar link, Summary. Tables are unreadable when each item carries rich metadata. The paper title in the heading is required so the user knows what each citation IS at a glance. Always include a clickable Google Scholar search URL so the user can verify and grab BibTeX directly without switching files.

Fix: v2.4.0 — the sources.md schema template and every paper-listing output format in the layer (arxiv, semantic-scholar, exa-search, deepxiv, comm-lit-review, novelty-check) now use one-source-one-subsection with the full title in the heading; the sources.md template carries the Scholar search URL field. Same recurrence as 1_search/feedback/2026-06-22_sources-per-section-not-table.md (also fixed).
