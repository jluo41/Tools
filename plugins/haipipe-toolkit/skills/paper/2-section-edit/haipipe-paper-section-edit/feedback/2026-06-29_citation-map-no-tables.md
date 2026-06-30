---
status: open
created: 2026-06-29
updated: 2026-06-29
occurrences: 1
context: §3 theory citation map formatting
fixed_in: ""
regressed: ""
---

Citation map files (_CITATION_*.md) must NEVER use tables. Each citation is its own markdown section (### heading) with bullet-point fields (Assertion, Key, Journal, Status, Scholar link, Summary). Tables are unreadable for this content because each citation carries too much metadata for a single row. The Scholar link must be a clickable Google Scholar search URL so the user can verify and grab BibTeX directly from the citation map without switching to a separate search-list file.
