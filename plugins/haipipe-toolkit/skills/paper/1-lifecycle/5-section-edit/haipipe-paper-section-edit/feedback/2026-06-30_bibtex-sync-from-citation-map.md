---
status: open
created: 2026-06-30
updated: 2026-06-30
occurrences: 1
context: §3 theory citation workflow
fixed_in: ""
regressed: ""
---

When adding BibTeX entries to .bib, ALWAYS extract them programmatically from _CITATION_*.md (where the user pastes them after Scholar verification). Never manually type or re-author BibTeX entries into .bib. Use a script to extract @article/@incollection blocks from the citation map and append to .bib, then verify consistency between the two files. The _CITATION file is the source of truth for BibTeX; .bib is the target. Manual entry causes key mismatches and content divergence.
