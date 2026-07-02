---
date: 2026-07-01
status: open
source: MISQ-Literature-literature session
recurrence: 2026-07-01 (clarified bibtex copy rule + SEARCH markers)
---

# Bibtex in _CITATION_ maps: copy OK, generate NO, mark SEARCH

## Rule

CC must NEVER generate bibtex entries from memory (unreliable, may hallucinate fields). CC CAN copy/paste bibtex that already exists in the `.bib` file into the citation map for reference.

For papers NOT yet in the `.bib`, CC marks them with `> SEARCH` so JL knows to manually find the entry on Google Scholar and add it to the `.bib`.

For papers already in the `.bib`, CC marks them with `> ✅ SEARCH` so JL knows no manual work is needed.

## SEARCH markers

Every entry in `_CITATION_N-section.md` must end with one of:

- `> SEARCH` -- paper is NOT in the `.bib`. JL needs to find it on Google Scholar and copy the bibtex into the `.bib` file.
- `> ✅ SEARCH` -- paper IS already in the `.bib`. No manual work needed.

## Bibtex blocks

- CC may include a bibtex block ONLY if it is copied verbatim from the existing `.bib` file (for JL's convenience when reviewing).
- CC must NEVER author/generate a bibtex block from scratch. The risk of hallucinated authors, wrong year, wrong journal, or wrong pages is too high.
- If the paper is 🔍 (not in bib), do NOT generate a bibtex block. Instead mark `> SEARCH` and provide the Scholar link so JL can find and copy the real entry.

## What the citation map SHOULD contain per entry

- Heading with full authors, year, title
- **Key**, **Journal** (with vol/pages), **Assertion**, **Status**, **Scholar** link, **Summary**
- `> JL:` / `> CC:` comment threads
- `> SEARCH` or `> ✅ SEARCH` marker
- Optional: bibtex block copied from `.bib` (never generated)

## How to apply

When generating or updating `_CITATION_` maps:
1. For each entry, check whether the key exists in the `.bib`
2. If yes: mark `> ✅ SEARCH`, optionally copy the bibtex from `.bib`
3. If no: mark `> SEARCH`, provide the Scholar search link, do NOT generate bibtex
