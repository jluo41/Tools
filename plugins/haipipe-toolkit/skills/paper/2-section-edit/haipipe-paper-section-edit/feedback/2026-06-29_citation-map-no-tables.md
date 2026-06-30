---
status: open
created: 2026-06-29
updated: 2026-06-29
occurrences: 1
context: §3 theory citation map formatting
fixed_in: ""
regressed: ""
---

Citation map files (_CITATION_*.md) must NEVER use tables. Each citation is its own markdown section (### heading) with the full paper title in the heading (e.g., `### P1.S2 — Graziano, Jensen-Campbell, & Hair (1996). Perceiving interpersonal conflict and reacting to it: The case for agreeableness.`). Below the heading, bullet-point fields: Key, Journal, Assertion, Status, Scholar link, Summary. Tables are unreadable for this content because each citation carries too much metadata for a single row. The Scholar link must be a clickable Google Scholar search URL so the user can verify and grab BibTeX directly from the citation map without switching to a separate search-list file. The paper title in the heading is required so the user knows what each citation IS without clicking anything.
