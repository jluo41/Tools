---
name: haipipe-paper-edit-manual-review-citations
description: "Section-by-section, citation-by-citation manual verification of every \\cite{...} in the paper, with a human approval gate at every fix. Verifies three independent axes per cite: existence (paper resolves at the claimed DOI/arXiv/venue), metadata correctness (author, year, venue, title), and context appropriateness (cited paper actually supports the surrounding claim). Use when user says \"manually review the citations\", \"逐个核对引用\", \"walk through every cite\", \"pre-submission citation pass\", or before any high-stakes submission where one wrong-context or hallucinated cite is unacceptable."
argument-hint: "[paper-directory]"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, WebFetch, WebSearch
metadata:
  version: "1.1.0"
  last_updated: "2026-05-31"
  summary: "Section-by-section, citation-by-citation manual verification of every \\\\cite{...} in the paper, with a human approval gate at every fix."
  changelog:
    - "1.1.0 (2026-06-05): renamed from paper-manual-review-citations to haipipe-paper-edit-manual-review-citations; consolidated into 3-write-edit/ (haipipe-paper-* name unification)."
    - "1.0.0 (2026-05-31): baseline metadata added."
---

# Paper Manual Review (Citations): Walk Every Cite, Approve Every Fix

Walk every `\cite{...}` invocation in the paper at: **$ARGUMENTS**

## Why This Exists

`/citation-audit` runs a one-shot autonomous review via a fresh cross-model reviewer (GPT-5.4 with web access) and writes a JSON+MD verdict. That is fast and good enough for routine checks — but it is not what you want before a top-tier submission.

This skill is the slow, paranoid, human-paced version. Its job is to:

1. Re-verify every `\cite` against canonical sources (publisher page / DOI / arXiv / DBLP / Crossref / PubMed) — not against memory and not against "do other papers cite it the same way?"
2. Show the user the verification chain (URLs opened, fields compared) for every proposed fix
3. Wait for explicit user approval per cite before editing the `.bib` or `.tex`
4. Hunt for **wrong-context** cites (real paper, but it does not establish the claim it is being used to support) — this is the highest-value class of error and the one autonomous skills miss most often
5. Hunt for **silent metadata drift** (arXiv v1 vs v3 with different titles; preprint year cited when the published year is one later; co-author dropped in a copied BibTeX)

The goal is not speed. The goal is that after this skill finishes, the user can defend every cite in the paper to a reviewer who asks "where in that paper does it say X?"

## How This Differs From Sibling Skills

| Skill | Mode | Verification depth | Output | When to use |
|-------|------|---------------------|--------|-------------|
| `/citation-verifier` | local-only | bib hygiene (placeholders / duplicates / missing IDs) | report | quick pre-write hygiene |
| `/reference-audit-guide` | principles only | (no workflow) | n/a | reference for citation discipline |
| `/citation-audit` | autonomous, one-shot | fresh GPT-5.4 with web lookups | JSON+MD | routine pre-submission check |
| **`/haipipe-paper-edit-manual-review-citations`** | **interactive, human-paced** | **agent + web lookups + human at every gate** | **edits applied + change log** | **high-stakes final submission** |

The autonomous skill answers "did anything obvious slip through?" This skill answers "can the user defend every cite under cross-examination?"

## Core Principle — Three Verification Axes

Per `\cite{key}`, run three independent checks. A cite is clean only when all three pass.

1. **Existence** — the paper actually exists at the claimed identifier.
   - Resolve the DOI URL. Or the arXiv ID. Or the publisher page from venue + title.
   - If no DOI/arXiv ID is in the bib entry, fall back to publisher page or PubMed/DBLP.
   - Failure mode: hallucinated paper (no canonical record exists).

2. **Metadata correctness** — author, year, venue, title match the canonical record.
   - Check author names AND order against the canonical source — copied BibTeX often drops a co-author or reorders.
   - Check year. For arXiv preprints later published at a venue, use the venue year (and venue), not the preprint year.
   - Check venue. "Proceedings of NeurIPS" vs "NeurIPS" vs "Conference on Neural..." — pick the form the bib style expects, but the paper must exist there.
   - Check title. arXiv v1 → v3 sometimes change titles silently.
   - Failure mode: real paper, copied wrong.

3. **Context appropriateness** — the cited paper actually supports the surrounding claim.
   - Read the sentence the `\cite` appears in. What is the cite supposed to establish?
   - Open the cited paper (publisher page abstract, arXiv abstract, or PDF if accessible) and find the supporting passage.
   - If the paper is famous (e.g., Cialdini 2009 "Influence"), at least confirm the cited *concept* is in the cited *book/paper*, not just somewhere in the author's broader corpus.
   - Failure mode: real paper, wrong context — citing Self-Refine for "self-feedback produces correlated errors" when Self-Refine actually argues the opposite.

**Three sources of truth, in this order:**

1. **Publisher page / DOI resolver** — the canonical source. `https://doi.org/<doi>` is always the first stop.
2. **arXiv / venue official record** — for preprints or open-access conference proceedings.
3. **Crossref / PubMed / DBLP / Semantic Scholar** — for metadata cross-checking when the publisher page is paywalled.

**Google Scholar is a fallback discovery aid, never the primary source.** Scholar's metadata is scraped and often wrong (especially venue and year for ambient-author or self-archived PDFs).

**One cite at a time. One human approval per fix. No batching.**

## Inputs

1. **Paper directory** (the argument)
2. **`.bib` file(s)** — typically `0-*.bib` or `references.bib`
3. **Section `.tex` files** — every file containing `\cite{...}` (typically `0-sections/*.tex` or `sections/*.tex`)
4. **Internet access** — `WebFetch` and `WebSearch` are mandatory; this skill is useless without them
5. **No interpretive artifacts** — do NOT trust `EXPERIMENT_LOG.md`, `NARRATIVE_REPORT.md`, or any prior audit summary. The point is independent re-verification.

## Workflow

### Phase 0: Confirm scope and set up

Before touching any cite:

1. Locate the paper master `.tex` file(s) and all `\input`'d sections.
2. Locate the `.bib` file(s). Confirm with the user: which bib is canonical for this paper? (Some papers have a working bib + a submission bib — check both.)
3. Confirm with the user: which sections are in scope for this pass? (Default: every section that has `\cite`.)
4. Build a minimal **citation map** showing the user the count and distribution:

```
CITATION MAP
├── Bib file: 0-TestToLearn-MS2026.bib  (N entries)
├── §1 Introduction (01_introduction.tex)        K1 \cite invocations / U1 unique keys
├── §2 Literature (02_literature_review.tex)     K2 / U2
├── §3 Method (03_method.tex)                    K3 / U3
├── §4 Results (04-*.tex)                        K4 / U4
└── §5 Discussion (05_discussion.tex)            K5 / U5

Total cites: ΣK   |   Total unique keys cited: ΣU
Bib entries never cited: <list>   (orphans)
Cite keys never resolved in bib: <list>  (broken — would error at compile)
```

Show the user. If anything looks off (wrong bib, missing section), fix it before Phase 1.

### Phase 1: Build the cite list

For each `\cite{key1,key2,...}` invocation in scope:

- Record the cite keys (one row per key, even if multi-cite)
- Record file + line number
- Record the surrounding sentence (≥ 1 full sentence around the cite — needed for the context check)
- Record the bib entry: `@type{key, ...}`

Skip `%%` and `%` comment lines — those don't render. Do NOT skip table or appendix `.tex` files; cites lurk in tables and methods sections.

Output: `MANUAL_REVIEW_CITATIONS.tsv` with columns:

```
key    file:line    surrounding_sentence    bib_entry_excerpt    status    decision
```

Show the user the row count and the breakdown by section before starting verification.

### Phase 2: Section-by-section walkthrough

For each section, in order:

1. Announce: "Now reviewing §X — N cites to verify."
2. For each cite in that section:
   - **Axis 1 (existence)**: `WebFetch` the DOI URL (or arXiv URL, or publisher page). Confirm the paper resolves.
   - **Axis 2 (metadata)**: compare bib fields against the canonical record. Flag any drift.
   - **Axis 3 (context)**: read the surrounding sentence. Read the cited paper's abstract (or relevant passage). Decide whether the cite supports the claim.
   - **Classify** the status (see "Status taxonomy" below).
   - **Show the user** a 5-line summary:
     ```
     §1 line 508: "...69.8\% CTR, 6.5\% above the Stage~2 baseline."
       cite:     \citep{milkman2021megastudies}
       existence: ✓ resolves at https://doi.org/10.1038/s41586-021-04128-4
       metadata:  ✓ Milkman, Gromet, Ho et al. 2021, Nature 600, "Megastudies..."
       context:   ✓ supports claim that megastudies are a standard tool
       status:    exact_match
     ```
   - **Wait for user response**: approve / reject / discuss. Never edit without explicit approval.
   - **Apply edit** (to `.bib` or `.tex`) only after approval.
   - **Log** the decision in `MANUAL_REVIEW_CITATIONS_LOG.md`.

3. At end of section, summarize: N cites, K approved fixes, M deferred, J flagged.

Do not proceed to the next section until the user signals to continue.

### Phase 3: Bib hygiene pass

This is the local-only sweep that `/citation-verifier` does. Run it once over the whole bib regardless of which sections are in scope, since hygiene problems compile silently.

For the entire `.bib` file, check:

- **Placeholders**: `[CITATION NEEDED]`, `\CITE_*`, `PLACEHOLDER_*`, `TODO:`, `??`, `\citet{?}`, etc. Grep for these patterns; flag every match.
- **Duplicate bibkeys**: any key defined more than once. The second silently overwrites the first.
- **Orphan entries**: bib entries never `\cite`d anywhere. Optional cleanup — flag, don't auto-remove (they may be staged for an upcoming section).
- **Broken refs**: `\cite{key}` invocations where `key` doesn't exist in the bib. These would generate `Citation undefined` warnings at compile.
- **Missing identifiers**: entries with no DOI, arXiv ID, or PMID for papers that should have one (i.e., non-book, non-website entries from after ~2000). Note: this is a quality flag, not necessarily a bug.
- **Inconsistent author formatting**: mixed "Last, First" vs "First Last" within the same bib.
- **Inconsistent venue formatting**: `Proc. NeurIPS` vs `Advances in Neural Information Processing Systems` vs `NeurIPS` for the same conference series. Pick one form and propose normalization.

Output a per-issue list in `MANUAL_REVIEW_CITATIONS_LOG.md` and let the user approve fixes one at a time.

### Phase 4: Cross-section consistency pass

For each unique cite key used in 2+ sections, check the cite is used **for the same purpose** in each location.

This catches a subtle failure mode: a paper is cited in §2 lit review for what it actually argues, then cited again in §1 intro for a different (wrong) claim, because the §1 author didn't re-read §2's source paper. The intro version is wrong-context; the lit-review version is right.

For each multi-section cite, show the user:

```
\citep{almaatouq2024beyond}
  §1 line 75:  "...has been criticized as hampering the advance of social science"
               (uses cite for: cumulative-learning critique → matches the paper's argument? YES)
  §2 line 43:  "...amounts to playing 20 questions with nature..."
               (uses cite for: integrative-probe-design critique → matches paper's argument? YES)
  → consistent: same paper, two compatible aspects of its argument
```

When uses disagree, the parquet-equivalent here is the **cited paper itself** — read its abstract/intro and decide which use is right. Do not silently align to the majority.

### Phase 5: Wrong-context audit

This is the phase the autonomous skills miss most often, and the one most likely to embarrass the paper at review time.

Beyond the per-cite context check in Phase 2, do a focused sweep on **high-risk cite patterns**:

- **Famous-author proxy cites**: when a famous name is cited (Kahneman, Cialdini, Thaler, Watts, Sunstein, etc.), authors often cite a general work (e.g., *Thinking Fast and Slow*) as a placeholder for a specific claim that actually appears in a different paper by the same author. Flag every cite to a household-name book and verify the specific concept appears in the *cited* work.
- **"Standard practice" cites**: phrases like "standard tool", "well-established", "commonly used" are red flags for cites that point to one specific paper as if it owns a whole literature. The cite must be either THE seminal paper or representative of the practice; otherwise replace.
- **Method-claim cites**: any cite that backs a methodological claim ("Holm-Bonferroni corrected", "propensity-weighted", "cluster-robust SEs"). The cited paper must describe the method, AND the surrounding code must actually implement it. Cross-reference with the corresponding `haipipe-paper-edit-manual-review-values` Phase 5 if that audit was run.
- **Self-cites**: cites to the user's own prior work. These are the easiest to get wrong (year off by one, wrong arXiv version, draft title vs published title) because the author trusts them. Verify every self-cite against the canonical record.

For each flag, show the user the high-risk pattern and propose: (a) keep with confirmation, (b) replace with a better-fitting cite, (c) drop if no good cite exists, (d) rewrite the surrounding prose to a softer claim that the existing cite does support.

### Phase 6: Write the change log

After all phases complete, write `MANUAL_REVIEW_CITATIONS_LOG.md`:

```markdown
# Paper Manual Review (Citations) — Change Log

**Date**: <ISO-8601>
**Paper**: <paper directory>
**Reviewer**: claude (interactive, human-approved)

## Summary
- Total cites walked: N (across S sections)
- Unique cite keys: U
- Bib entries: B (orphans: O)
- Edits applied to .bib: K1
- Edits applied to .tex (cite swaps, prose rewrites): K2
- Bib hygiene fixes: K3
- Deferred: M
- Flagged for further investigation: J

## Cite-level fixes applied

| # | Section / Line | Cite key | Axis failed | Before | After | Reason |
|---|---------------|----------|------------|--------|-------|--------|
| 1 | §1 line 508 | milkman2021megastudies | metadata | year=2022 | year=2021 | publisher record shows Nature 600 (2021) |
| 2 | §1 line 75 | almaatouq2024beyond | context | cited for "scale problem" | cited for "cumulative-learning critique" | replaced with Kohavi for scale claim |
| ... |

## Bib hygiene fixes

| Type | Key | Action |
|------|-----|--------|
| placeholder | \CITE_healthcare_nudge_effectiveness | replaced with patel2018nudge |
| duplicate | smith2020 | second entry deleted (different paper — renamed to smith2020b) |
| orphan | jones2019 | flagged; user kept (planned for §3 expansion) |
| ... |

## Wrong-context flags

| Cite | Section | Was cited for | Cited paper actually argues | Resolution |
|------|---------|---------------|-----------------------------|-----------|
| madaan2023selfrefine | §2 line 13 | "self-feedback produces correlated errors" | iterative self-improvement *works* | replaced with huang2023llmcantfix |
| ... |

## Deferred (see MANUAL_REVIEW_CITATIONS_TODO.md)

- §4 line Z: \cite{X} — needs publisher PDF access to confirm specific claim
- ...

## Citation map snapshot
[bib path, section file paths, cite counts]
```

This file is the audit trail. It is what the user shows their advisor or co-authors to demonstrate the paper went through a real citation review.

## Verification recipes

Per axis, the agent runs the corresponding recipe and shows the user the result.

### Axis 1 — Existence

**With DOI in bib:**
```
WebFetch https://doi.org/<doi>
```
Confirm the page resolves to a paper matching the bib title. If the DOI 404s or redirects to an unrelated record, flag.

**With arXiv ID in bib:**
```
WebFetch https://arxiv.org/abs/<arxiv-id>
```
Confirm title + authors match.

**With neither:**
```
WebSearch "<first-author> <year> <title-keywords> <venue>"
```
Find the canonical record, then DOI-resolve it.

### Axis 2 — Metadata

After resolving the canonical record, compare bib fields:

| Bib field | Compare against |
|-----------|----------------|
| author | publisher page author block (full names AND order) |
| year | venue year (NOT preprint year if published) |
| journal/booktitle | publisher's official venue name |
| title | publisher page title (watch for arXiv v1 vs v3 drift) |
| volume/number/pages | publisher record |
| doi | publisher canonical DOI |

Flag every drift, even if cosmetic (the user decides whether to fix).

### Axis 3 — Context

Read the surrounding sentence in the `.tex`. Identify the **specific claim** the cite is supposed to support.

Then either:

- **For an abstract-level claim** ("megastudies are a standard tool"): the cite's abstract must establish the claim. Fetch the abstract.
- **For a specific finding** ("CTR rose 12 pp"): the cited paper's results section must establish the finding. Fetch the PDF if accessible.
- **For a methodological claim** ("Holm-Bonferroni corrected"): the cited paper must describe the method.

If the abstract alone settles it, log `context_verified_abstract`. If you fetched the full PDF and confirmed, log `context_verified_pdf`. If the publisher page is paywalled and you cannot fetch the PDF, log `context_paywalled` and ask the user — they may have institutional access.

### High-risk pattern recipes

**Famous-author proxy:**
```
grep -E "\\\\cite[pt]?\{(cialdini|kahneman|thaler|watts|sunstein|...)" 0-sections/*.tex
```
For each hit, ensure the cited *work* (not just the cited *author*) establishes the surrounding claim.

**Self-cite:**
```
# extract author list from your bib's "self" entries — typically by checking author surname matches paper authors
grep -E "\\\\cite[pt]?\{(<your-self-cite-keys>)\}" 0-sections/*.tex
```
For each, fetch the canonical record. Verify year, title, venue.

**Method-claim cites:**
```
grep -E "\\\\cite[pt]?\{[^}]*\}" 0-sections/*.tex | grep -i -E "corrected|adjusted|weighted|robust|cluster"
```
For each, do Phase 5 method-claim audit (cross-reference with code).

## Status taxonomy

Per cite, classify as:

- `exact_match` — all three axes clean
- `metadata_drift_minor` — cosmetic metadata mismatch (e.g., venue formatting); does not affect identification
- `metadata_drift_major` — author/year/title differs in a way that could mislead a reader
- `nonexistent` — paper does not resolve at any canonical source (hallucinated)
- `version_drift` — preprint cited but published version exists with different metadata
- `wrong_context` — paper exists but does not support the surrounding claim
- `context_partial` — paper supports a *related* claim, not exactly the cited claim; rewrite needed
- `placeholder` — bib key like `[CITATION NEEDED]` / `\CITE_*` / `??`
- `duplicate_bibkey` — key defined twice in the bib; second overwrites first
- `broken_ref` — `\cite{key}` where `key` doesn't exist in the bib
- `missing_identifier` — bib entry has no DOI/arXiv/PMID for a paper that should have one
- `self_cite_drift` — self-citation with year/title/venue mismatch
- `paywalled_unverifiable` — publisher page paywalled, cannot fetch full text to confirm context
- `context_verified_abstract` — context confirmed via abstract only
- `context_verified_pdf` — context confirmed via full PDF read
- `unverifiable` — not enough information to verify (typically books or pre-2000 sources without ISBN/DOI)

## Failure modes to actively hunt (lessons from real misses)

1. **Wrong-context cites to famous papers.** Citing *Thinking Fast and Slow* for a specific claim about "extracting design knowledge" — the book doesn't cover this; the author cited it because Kahneman is a recognizable name in the neighborhood of the topic. Always verify the *specific* claim is in the *specific* cited work.

2. **arXiv preprint cited when published version exists.** Paper went arXiv 2023 → ICML 2024. Bib still says `arxiv2023.xxxxx` with year 2023. The reader looking up the cite gets the preprint, not the version of record. Always check the venue page for the most recent published version.

3. **Title drift v1 → v3.** Authors retitled the paper between arXiv submissions. The bib has the v1 title; the canonical record now has the v3 title. Reader fails to find the paper by searching the v1 title.

4. **Author hallucination via "et al."** Bib says "Smith and others"; you don't notice that the canonical record has 7 authors and the second author (which the cite is actually about) is missing. Always read the full canonical author list at least once.

5. **Year off by one for own work.** Self-cites are the easiest to get wrong because the author "remembers" the year. Always verify against the canonical record.

6. **Method-claim cite with no implementation.** Same as `haipipe-paper-edit-manual-review-values` Phase 5: paper says "Holm-Bonferroni" cited to a methods textbook, but the analysis script computes raw p-values. The cite is real but the method isn't applied. Cross-reference with the values audit.

7. **Same cite, two uses, only one correct.** A cite gets reused across sections. The lit-review use is right (drafted while reading the paper); the introduction use is wrong (drafted from memory of "what that paper is about"). Phase 4 catches this.

8. **Citing a paper for the opposite of what it argues.** *(See: madaan2023selfrefine cited for "self-feedback produces correlated errors" — Self-Refine actually argues iterative self-improvement works.)* Read the abstract before approving any cite that supports a contrarian or critical claim.

9. **Duplicate bibkey silently overwriting.** Two `@article{smith2020, ...}` entries with different content. The second silently replaces the first; cites resolve to the wrong paper. Phase 3 catches this.

10. **Placeholder shipped to submission.** `\CITE_healthcare_nudge_effectiveness` left in the .tex. Compiles cleanly because the bib has a stub for it. Never appears in the rendered PDF as a placeholder, so a final-pass read misses it. Always grep for placeholder patterns.

## Output contract

Always write four artifacts to the paper directory:

1. **`MANUAL_REVIEW_CITATIONS.tsv`** — one row per `\cite` invocation, with file:line, key, axes verdicts, surrounding sentence, status, decision (approved/rejected/deferred).
2. **`MANUAL_REVIEW_CITATIONS_LOG.md`** — human-readable change log (see Phase 6 template).
3. **`MANUAL_REVIEW_CITATIONS_TODO.md`** — deferred cites the user explicitly asked to revisit later (typically paywalled-unverifiable or "needs co-author input").
4. **`MANUAL_REVIEW_CITATIONS_BIBHYGIENE.md`** — bib-level hygiene findings from Phase 3 (duplicates, orphans, placeholders, missing identifiers).

Edits to `.tex` files (cite-key swaps, prose rewrites for wrong-context fixes) go directly via `Edit` tool — but only after explicit user approval per edit.
Edits to the `.bib` file (metadata corrections, dedup, placeholder replacement) likewise.

**Do not bulk-apply** — even when 10 cites all need the same trivial fix (e.g., venue normalization), run them one at a time so the user can spot-check.

## Anti-patterns

- ❌ "The bib was generated by Zotero / Mendeley / Scholar export, the metadata is fine." (Scraped exports are wrong constantly. Always verify against the publisher page.)
- ❌ "I'll batch the small metadata fixes and apply them together." (No batching. One approval per edit.)
- ❌ "The paper has been through co-authors, the cites are probably fine." (Co-authors trust each other's cites. You're the only one re-deriving from the publisher page.)
- ❌ "I recognize the cite key, no need to fetch the URL." (Recognition is not verification. Fetch.)
- ❌ "The cite supports a related concept, that's close enough." (Close enough is wrong context. Either find a cite that supports the *exact* claim or rewrite the prose to fit the cite.)
- ❌ "It's a famous paper, the metadata can't be wrong." (Famous papers attract bad copies. Always verify.)
- ❌ "I'll skip the abstract-read for cites in the lit review since they were verified when the lit review was drafted." (The lit review may have been drafted from memory too. Trust nothing.)
- ❌ "The DOI 404s but the cite is correct, the publisher page must be temporarily down." (Re-check from a different angle — Crossref, Semantic Scholar — before assuming server-side flakiness.)
- ❌ "Self-cites don't need verification, I wrote the paper." (Especially likely to be wrong precisely because of self-trust.)
- ❌ "The arXiv preprint year is fine, everyone knows the published year is one later." (No they don't. Reviewers check the bib and don't excavate the arXiv-vs-published distinction unless explicitly told.)

## When to run

Run this skill:

1. **After `/citation-audit`** — the autonomous audit catches obvious issues fast; this skill catches the subtle ones (especially wrong-context).
2. **Before submission to a top-tier venue** — when one wrong-context cite is a desk-reject risk.
3. **After a major intro/method/related-work rewrite** — when many cites were added or repositioned.
4. **When a co-author flags "I don't trust these cites"** — this skill produces the audit trail to settle it.

Do not run this skill:

- During early drafting (cites churn too fast; use `/citation-verifier` for hygiene and `/citation-audit` for periodic semantic checks instead).
- Without internet access (`WebFetch`/`WebSearch` are mandatory; the skill is useless offline).

## Notes for the agent running this skill

- You will be tempted to skip the abstract-read for cites that "obviously" support the claim. Don't. The point is paranoid thoroughness; the obvious cases are not where the bugs hide.
- You will be tempted to claim "all cites verified" after walking only a subset. Don't.
- You will be tempted to trust the bib's metadata over the publisher page. The publisher page decides.
- When the user pushes back on a status, **fetch the URL on the spot** and show them the canonical record. Don't argue from memory.
- For paywalled cites, ask the user if they have institutional access; if so, ask them to fetch the PDF and paste the relevant passage. Do not silently downgrade `paywalled_unverifiable` to `context_verified_abstract` without confirming.
- For self-cites, **always** verify, even if the user supplied them. Self-trust is the largest single source of citation bugs.
- For wrong-context findings, the conservative default is to **rewrite the surrounding prose** to match what the cite actually supports, rather than to swap in a different cite. Cite-swapping risks introducing a new wrong-context error; prose-softening doesn't.
- If a wrong-context fix needs a new cite that isn't in the bib, write the proposed citation (Scholar search link + bibkey) into `MANUAL_REVIEW_CITATIONS_TODO.md` and let the user verify and add it. Never fabricate a bib entry — even with the right metadata, an unverified entry is worse than a clear gap.
- When the user runs `haipipe-paper-edit-manual-review-values` and `haipipe-paper-edit-manual-review-citations` on the same paper, do the values pass first. Method-claim citations are easier to flag once the values pass has identified which method claims actually have code support.
