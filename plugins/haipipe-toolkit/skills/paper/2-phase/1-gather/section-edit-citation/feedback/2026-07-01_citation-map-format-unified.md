---
date: 2026-07-01
status: open
source: MISQ-Literature-literature session
---

# _CITATION_ map format must be unified across sections

## Problem

Different sessions produced _CITATION_ files in inconsistent formats. The intro and theory maps follow a rich format; the literature map was generated with a stripped-down format missing critical elements. JL flagged: "you don't even have the paper title."

## Unified format (derived from §1-introduction and §3-theory exemplars)

Every entry in a `_CITATION_N-section.md` file must follow this template:

```
### [emoji] P#.S# -- Full Author List (Year). Full Paper Title.

- **Key:** `bibtex_key`
- **Journal:** Full Journal Name Vol(Num), Pages
- **Assertion:** the specific claim this citation supports in this sentence
- **Status:** [emoji] description
- **Scholar:** [search](google-scholar-url)
- **Summary:** one-line summary of the paper's contribution

```bibtex
@article{key, ...full entry...}
```
```

### Emoji legend (place in file header)

- ✅ = in bib + placed in tex
- 📌 = in bib, not yet placed in this section's tex
- ⚠️ = in bib but needs fix (entry type, casing, wrong paper, etc.)
- 🔍 = NOT in bib, needs adding

### Required elements (every entry)

1. **Full paper title** in the heading (not just a short description)
2. **Full author list** in the heading (not "et al." shorthand)
3. **Bold field labels** (`**Key:**`, `**Journal:**`, etc.)
4. **Journal with volume/number/pages** (not just journal name)
5. **Scholar as markdown link** `[search](url)` (not bare URL)
6. **Bibtex block** for any entry that is 🔍, ⚠️, or 📌 (entries needing action). Optional for ✅ entries.

### Organization

- Group by paragraph (P1, P2, ...) matching the section structure, not by subsection
- Preserve `> JL:` comments verbatim

## Why

Without the full title, a human scanning the map cannot tell whether the cited paper actually matches the assertion. The intro/theory maps caught errors (wrong madanay paper, wrong Lewin year) precisely because the full title was visible. The literature map hid the same madanay error behind a vague description.
