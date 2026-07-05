# Source / Paper Presentation Format (canonical)

THE one home for how papers and sources are presented anywhere in the discovery layer — sources.md files, landscape references, prior-art listings, and inline chat results. Every skill that lists sources points here.

## The rule

ONE SOURCE = ONE SUBSECTION, full title in the heading. NEVER a table — tables of papers are not for humans to read (long titles wrap badly in cells; you cannot scan one source at a glance). Tables stay allowed only for short-field analytical matrices (score grids, confound rankings), never for citation/source metadata.

## sources.md — papers

```md
# Sources

### S001 — Hou et al. (2024). Large Language Models are Zero-Shot Rankers for Recommender Systems.
- ECIR 2024 · doi:10.1007/978-3-031-56060-6_24 · arXiv:2305.08845
- Scholar: https://scholar.google.com/scholar?q=Large+Language+Models+are+Zero-Shot+Rankers
- role: adjacent method · verification: VERIFIED
- summary: Frames recommendation as a conditional ranking task and tests whether
  off-the-shelf LLMs can rank candidate items zero-shot from a user's interaction
  history. On two public benchmarks, LLMs beat non-tuned baselines but trail
  fully tuned models, and the rankings shift with candidate order and item
  popularity; the authors add prompting strategies to partially correct both.
- finding: LLMs rank zero-shot but are sensitive to candidate position and popularity.
```

Fields per entry:
- FIRST LINE = the journal/venue line: venue + year, then locators (DOI / arXiv id / URL).
- Scholar search URL — so the human can verify and grab BibTeX without switching files.
- role · verification flag (`VERIFIED` = exact title + authors + venue/id confirmed via independent lookup; anything less = `NEEDS-VERIFICATION`).
- `summary:` — 2-4 sentences on what the paper itself is about (question, method, result). May run longer when the paper is load-bearing.
- `finding:` — ONE plain-language line: why this paper matters for OUR question.

S-ids are FOLDER-LOCAL by default (S001 restarts per discovery-folder). A group may declare group-global S-ids (one numbering shared across its folders, so a source cited twice keeps one id) — state that choice at the top of each sources.md it applies to.

## sources.md — non-paper sources (news / surveys / reports)

Same shape; the heading carries outlet + year + title, the bullets carry what fits:

```md
### 7 — rater8 (2025). Patient Choice Report.
- vendor survey · <URL>
- verification: VERIFIED
- summary: (optional, when the source needs context) annual vendor consumer survey
  on how patients research and pick providers.
- supports: 31% use genAI to research providers; 26% AI-influenced choice.
```

## notes.md — per-source readings

```md
# Notes

## S001 — Hou et al. (2024)
- claim/method/result actually found in the source, in plain language
- limits or caveats relevant to our question
```

## Inline chat results (one-off searches, no folder)

Numbered list, one paper per entry — never a table:

```text
1. Hou et al. (2024). Large Language Models are Zero-Shot Rankers for Recommender Systems.
   ECIR 2024 · arXiv:2305.08845 · 1,364 citations
2. ...
```

## Reference lists inside landscape.md / analyses

Numbered "References (full, verified)" list, one self-contained line per paper, is fine (it is a list, not a table). Full citation discipline (full names, collision disambiguation, verification flags) is the Review Output Contract in `2_review/haipipe-discovery-review/SKILL.md`.

## Filled example on disk

`examples/ProjC-LLMRecPhysicain/discoveries/L01_rank-divergence-landscape/01_llm-healthcare-search-rank-divergence/sources.md` — seven real papers plus four local sources in this exact format.
