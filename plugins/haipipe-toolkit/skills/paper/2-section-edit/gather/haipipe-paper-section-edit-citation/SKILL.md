---
name: haipipe-paper-section-edit-citation
description: "citation gather worker for section-edit. One skill, one working doc (_CITATION_), full lifecycle: AUDIT (mechanical cross-ref + gap identification) → SEARCH (find candidates) → CANDIDATE (write to _CITATION_ with SEARCH markers) → [HUMAN GATE] → PLACE (verified → .bib + tex) → REVIEW (pre-submission 3-axis walk). Merges former check-reference + manual-review-citations. Hard boundary: agent NEVER generates bibtex, NEVER adds to .bib, NEVER places \\citep{} for unverified papers. Trigger: citation, cite, gather citations, check references, audit references, citation review, manual review citations."
argument-hint: "[verb] [section-name-or-number] [paper-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Agent, WebFetch, WebSearch
metadata:
  version: "1.0.0"
  last_updated: "2026-07-02"
  summary: "Unified citation gather worker. AUDIT→SEARCH→CANDIDATE→[HUMAN]→PLACE→REVIEW lifecycle. Single working doc = _CITATION_. Absorbs check-reference + manual-review-citations."
  changelog:
    - "1.0.0 (2026-07-02): merged check-reference (mechanical audit) + manual-review-citations (pre-submission 3-axis walk) + 4 feedback items into one skill with 6 phases. Defined hard boundaries. Defined _CITATION_ candidate format."
    - "0.0.1 (2026-06-29): stub with scope only."
  predecessors:
    - "haipipe-paper-section-edit-citation (mechanical \\label/\\ref/\\cite audit) — MERGED as Phase 1"
    - "haipipe-paper-section-edit-citation (pre-submission 3-axis walk) — MERGED as Phase 6"
  absorbs_feedback:
    - "2026-07-01_no-bibtex-in-citation-map.md → Rule 1"
    - "2026-07-01_citation-map-format-unified.md → _CITATION_ format spec"
    - "2026-07-01_citation-summary-depth.md → Rule 3"
    - "2026-06-30_bibtex-sync-from-citation-map.md (from section-edit/) → Rule 2"
---

Skill: haipipe-paper-section-edit-citation
==================================

citation gather worker for `haipipe-paper-section-edit`. One skill owns
the full citation lifecycle for one section, from gap identification through
pre-submission verification. The single working document is
`_CITATION_N-section.md`.

```
/haipipe-paper-section-edit-citation                            → status dashboard
/haipipe-paper-section-edit-citation audit <section>            → Phase 1: mechanical check + gap ID
/haipipe-paper-section-edit-citation search <section>           → Phase 2-3: find candidates, write to _CITATION_
/haipipe-paper-section-edit-citation place <section>            → Phase 5: verified entries → .bib + tex
/haipipe-paper-section-edit-citation review <section>           → Phase 6: pre-submission 3-axis walk
```

## Hard Boundaries

These are non-negotiable. Every agent invoking this skill must obey them.

1. **NEVER generate bibtex from memory.** LLM-generated bibtex is unreliable
   (hallucinated authors, wrong year, wrong journal, wrong pages). The agent
   may copy bibtex that already exists in the `.bib` file into the citation
   map for reference, but must NEVER author a new bibtex block.

2. **NEVER add entries to .bib directly.** The `.bib` file is the TARGET, not
   the source. Only the human adds bibtex to `.bib` (by copying from Google
   Scholar after verification). The agent may place `\citep{}` in tex ONLY
   for keys that already exist in `.bib`.

3. **NEVER place `\citep{}` for unverified papers.** A paper is "verified"
   when the human marks it `> ✅ SEARCH` in the citation map AND the key
   exists in `.bib`. Until both conditions hold, the agent must not touch
   the tex.

4. **NEVER remove JL comments from the outline.** Preserve `> JL:` comments
   verbatim. When a comment is resolved, add a `> CC:` response below it
   explaining the resolution. The comment itself stays.


## Six Phases

```
Phase 1: AUDIT        mechanical cross-ref + identify uncited factual assertions
Phase 2: SEARCH       find candidate papers for gaps
Phase 3: CANDIDATE    write 🔍 entries to _CITATION_ with > SEARCH markers
═══════════════════   HUMAN GATE ═══════════════════════════════════════════
Phase 4: (human)      JL clicks Scholar links, verifies, copies bibtex → .bib
Phase 5: PLACE        verified entries → \citep{} in tex + sync outline
Phase 6: REVIEW       pre-submission 3-axis walk (existence, metadata, context)
```

Phases 1-3 run together when the user says "gather citations" or "search."
Phase 4 is human-only (the agent waits).
Phase 5 runs when the user says "place" after verification.
Phase 6 runs before submission when the user says "review" or "manual review."


## Phase 1: AUDIT

Two sub-checks run together.

### 1a. Mechanical cross-reference audit (from check-reference)

Scan the section's tex file for marker integrity:

- Every `\cite{key}` resolves to a `@type{key, ...}` entry in the `.bib`
- No orphan bib entries cited only in this section
- No `\label`/`\ref` breaks in the section
- `\phantomsection\label{}` positioned correctly relative to `\section*{}`

Tool: run `check_refs.py` (co-located in this skill folder) on the paper root.
The script is Python stdlib only, no external deps.

```bash
python3 <skill-dir>/check_refs.py <paper-root-dir> -o <output.md>
```

### 1b. Gap identification

Read the section outline and tex. For each sentence:

- Is it a factual assertion (not "our study does X")?
- Does it have a citation?
- If cited, does the cited paper plausibly support the claim?

Output: a gap list in chat (not written to files yet). Each gap is:
```
P#.S# | sentence text | gap type (uncited / wrong-context / weak)
```

Also process any `> JL:` comments requesting citations (e.g., "needs cite
here", "find a paper about X").


## Phase 2: SEARCH

For each gap from Phase 1, search for candidate papers.

### Search routing

| Gap type | Search method |
|---|---|
| Single paper lookup ("find the JAMA paper about X") | WebSearch agent |
| Targeted topic ("IS papers on physician reviews") | WebSearch + Semantic Scholar |
| Broad field gap (needs literature landscape) | Dispatch /haipipe-discovery |
| Claim-level evidence question | Route to /haipipe-probe |

For WebSearch agents, launch them in parallel (one per gap) via the Agent
tool. Each agent returns: candidate paper(s) with title, authors, year,
journal, and a 2-3 sentence summary.


## Phase 3: CANDIDATE → _CITATION_

Write search results as 🔍 CANDIDATE entries in `_CITATION_N-section.md`.

### Candidate entry format

```markdown
### 🔍 CANDIDATE for P#.S# -- Full Author List (Year). Full Paper Title.

- **Key:** `proposed_bibtex_key`
- **Journal:** Full Journal Name Vol(Num), Pages
- **Assertion:** the specific claim this citation would support
- **Status:** 🔍 candidate (CC-found, not yet verified)
- **Target sentence:** "the sentence text where this would be placed"
- **Placement:** cite alongside "phrase" in P#.S#

> SEARCH: [Scholar](https://scholar.google.com/scholar?q=search+terms+here)
- **Summary:** 2-3 sentences: what the paper did (method, data, scale),
  key finding relevant to the assertion, why it matters for this manuscript.
```

Rules for the candidate entry:

- **Full paper title** in the heading (not a short description)
- **Full author list** in the heading (not "et al.")
- **Journal with volume/number/pages** when known
- **Scholar link** as a clickable markdown link (not bare URL)
- **2-3 sentence summary** with method + finding + relevance (not one-liner)
- **NO bibtex block** (never generate bibtex from memory)
- **NO .bib edit** (never add to .bib)
- **NO .tex edit** (never place \citep{})
- **Placement recommendation** so the human knows where to cite after verifying

### Existing entry format (already in bib)

Entries already in the `.bib` and already placed use:

```markdown
### ✅ P#.S# -- Full Author List (Year). Full Paper Title.

- **Key:** `bibtex_key`
- **Journal:** Full Journal Name Vol(Num), Pages
- **Assertion:** the specific claim this citation supports
- **Status:** ✅ placed

> ✅ SEARCH: [Scholar](https://scholar.google.com/scholar?q=...)
- **Summary:** 2-3 sentences.
```

### Status emoji legend (place in file header)

```
✅ = in bib + placed in tex + verified on Scholar
📌 = in bib, not yet placed in this section's tex
⚠️ = in bib but needs fix (wrong paper, metadata drift, wrong context)
🔍 = NOT in bib, candidate found by CC, needs user verification
```

### SEARCH markers

Every entry ends with one of:
- `> SEARCH: [Scholar](url)` -- NOT verified. JL needs to click, verify, copy bibtex → .bib
- `> ✅ SEARCH: [Scholar](url)` -- verified by JL. In .bib and ready to place.

### Citation issue entries

When Phase 1 finds a problem with an EXISTING citation (wrong context, metadata
drift, citation doesn't hold), write it as:

```markdown
### ⚠️ P#.S# -- Citation issue: key may not support claim

- **Current claim:** "the sentence text"
- **Current cite:** bibtex_key
- **Problem:** description of what's wrong
- **Recommendation:** keep / replace / soften claim
- **Alternative candidates:** (if applicable)
```


## Phase 4: HUMAN GATE (agent does not execute this)

The human:
1. Clicks `> SEARCH` Scholar links in the citation map
2. Reads the paper abstract, confirms it supports the assertion
3. Marks verified entries as `> ✅ SEARCH`
4. Copies bibtex from Scholar → `.bib` file
5. Optionally adds `> JL:` comments with corrections or questions

The agent does NOT participate in Phase 4. When the user returns and says
"place" or "I've verified these," proceed to Phase 5.


## Phase 5: PLACE

After the human verifies candidates and adds bibtex to `.bib`:

1. Check that the key exists in `.bib` (grep for `@...{key,`)
2. Update the _CITATION_ entry status: 🔍 → ✅
3. Place `\citep{key}` in the section tex at the recommended location
4. Sync the outline (add parenthetical reference on the cited sentence)
5. Update the density table in the citation map

Only place citations whose key exists in `.bib` AND whose SEARCH marker
is `> ✅ SEARCH`. If either condition fails, skip and report why.


## Phase 6: REVIEW (pre-submission)

The slow, paranoid, human-paced verification pass. Run before a top-tier
submission when one wrong-context cite is a desk-reject risk.

For each `\cite{key}` in the section, verify three independent axes:

### Axis 1: Existence
The paper actually exists at the claimed identifier.
- Resolve DOI URL, arXiv ID, or publisher page
- Failure mode: hallucinated paper (no canonical record exists)

### Axis 2: Metadata correctness
Author, year, venue, title match the canonical record.
- Check author names AND order against publisher page
- Check year (venue year, not preprint year if published)
- Check venue name, title (arXiv v1 vs v3 drift)
- Failure mode: real paper, copied wrong

### Axis 3: Context appropriateness
The cited paper actually supports the surrounding claim.
- Read the sentence the cite appears in
- Read the cited paper's abstract or relevant passage
- Failure mode: real paper, wrong context

**Three sources of truth, in order:**
1. Publisher page / DOI resolver (canonical)
2. arXiv / venue official record
3. Crossref / PubMed / DBLP / Semantic Scholar (cross-check)

Google Scholar is a fallback discovery aid, never the primary source for
verification. Scholar's metadata is scraped and often wrong.

**One cite at a time. One human approval per fix. No batching.**

Show the user a 5-line summary per cite:
```
P#.S# line NN: "...sentence text..."
  cite:      \citep{key}
  existence: ✓ resolves at https://doi.org/...
  metadata:  ✓ Author et al. Year, Journal Vol(Num)
  context:   ✓ supports claim that X
  status:    exact_match
```

Wait for explicit user approval before any edit.

### Cross-section consistency (multi-section review only)

For cite keys used in 2+ sections, check the cite is used for the same
purpose in each location. The lit-review use is usually right (drafted while
reading the paper); the intro use may be wrong (drafted from memory).

### Wrong-context audit patterns

High-risk patterns to actively hunt:
- Famous-author proxy cites (Kahneman, Cialdini cited for a specific claim)
- "Standard practice" cites (one paper standing in for a whole literature)
- Method-claim cites (cited method ≠ implemented method)
- Self-cites (easiest to get wrong due to self-trust)


## _CITATION_ file organization

```markdown
# §N Section-Name: Citation Map

Density: K unique keys / S sentences = D keys/sentence.
M/S sentences carry at least one cite (R).

Venue norm: [venue-specific sentence-with-cite ratio]

[Status emoji legend from above]

---

## P1. Paragraph headline (N sentences)

### [emoji] P1.S2 -- Author List (Year). Paper Title.
[entry fields as defined above]

### [emoji] P1.S3 -- Author List (Year). Paper Title.
[entry fields as defined above]

---

## P2. Paragraph headline (N sentences)
...

---

## Density by paragraph

| P | Sentences | Cited | Keys | Density | Note |
|---|---|---|---|---|---|
| P1 | 7 | 4 | 5 | 0.71 | ... |
| P2 | 5 | 1 | 2 | 0.40 | ... |

## Open items

- [describe any remaining gaps, probe plans, or issues]
```

Organization rules:
- Group by paragraph (P1, P2, ...) matching the section outline structure
- Preserve `> JL:` comments verbatim with `> CC:` responses below
- Keep density table and open items updated after each phase


## Relation to sibling skills

```
gather/
  haipipe-paper-section-edit-citation     ← THIS (citation, _CITATION_.md)
  haipipe-paper-section-edit-values       ← values, _VALUES_.md
  haipipe-paper-section-edit-display      ← display, 0-displays/ units
```

All three follow the same shape: AUDIT → SEARCH → CANDIDATE → [HUMAN] → PLACE → REVIEW.
Each owns one working document type. Each has the same human gate boundary.


## Relation to other skills

| If the author wants ... | Use |
|---|---|
| Gather citations for a section (search + candidate) | **this skill**, Phase 1-3 |
| Place verified citations into tex | **this skill**, Phase 5 |
| Pre-submission citation walk | **this skill**, Phase 6 |
| Broad literature search (field landscape) | /haipipe-discovery |
| Claim-level evidence question | /haipipe-probe |
| Quick bib hygiene (placeholders, duplicates) | /citation-verifier |
| Cross-model autonomous citation audit | /citation-audit |


## Done criteria

citation is done when:
- [ ] All `> JL:` citation comments are resolved (candidate found or acknowledged)
- [ ] All factual assertions have citations or are explicitly uncited-by-design
- [ ] All candidates are written to _CITATION_ with > SEARCH markers
- [ ] Density meets venue norm
- [ ] No ⚠️ entries remaining (all issues resolved)
- [ ] No 🔍 entries remaining (all candidates verified or dropped)
- [ ] _LOG updated with citation gather summary


## Anti-patterns

- ❌ Generating bibtex from memory or search results (hallucination risk)
- ❌ Adding entries to .bib directly (human-only operation)
- ❌ Placing \citep{} for unverified papers (skips human gate)
- ❌ Writing one-line summaries ("Evaluates the effect of X") instead of
  method + finding + relevance
- ❌ Using "et al." shorthand in entry headings instead of full author list
- ❌ Removing JL comments after resolving them (preserve with CC response)
- ❌ Trusting bib metadata over the publisher page (publisher page decides)
- ❌ Skipping the abstract-read for "obvious" cites (obvious ≠ verified)
- ❌ Batching fixes in Phase 6 (one cite, one approval, no batching)
