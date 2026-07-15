Citation formats + reference (haipipe-paper-probe-citation)
============================================================

Loaded on demand from SKILL.md. The entry/file templates, the CHECK-phase user
guide, and the multi-round lifecycle notes live here so the SKILL carries only the
operating logic. Hard Boundaries, the five phases, and the one-door ROUTE rule stay
in SKILL.md.


## _CITATION_ entry formats

### Candidate entry (agent-found, NOT in .bib yet)

```markdown
### 🔍 CANDIDATE for P#.S# -- Full Author List (Year). Full Paper Title.

- **Journal:** Full Journal Name Vol(Num), Pages
- **Assertion:** the specific claim this citation would support
- **Status:** 🔍 candidate
- **Source:** 🤖 agent-found (YYYY-MM-DD)
- **Target sentence:** "the sentence text where this would be placed"
- **Placement:** cite alongside "phrase" in P#.S#

> SEARCH: [Scholar](https://scholar.google.com/scholar?q=search+terms+here)
- **Summary:** 2-3 sentences: what the paper did (method, data, scale), key finding relevant to the assertion, why it matters for this manuscript.
```

Rules for a candidate entry:
- **Full paper title** in the heading (not a short description); **full author list** (not "et al.").
- **Journal with volume/number/pages** when known.
- **Scholar link** as a clickable markdown link (not a bare URL).
- **2-3 sentence summary** with method + finding + relevance (not a one-liner).
- **NO Key field on candidates** (the bibtex key is whatever Scholar generates when the human copies bibtex; the agent discovers it later by grepping .bib).
- **NO bibtex block**, **NO .bib edit**, **NO .tex edit** (plain-text description only).
- **Placement recommendation** so the human knows where to cite after verifying.

### Placed entry (verified, in .bib, placed in tex)

```markdown
### ✅ P#.S# -- Full Author List (Year). Full Paper Title.

- **Key:** `bibtex_key` (learned from .bib after human added it)
- **Journal:** Full Journal Name Vol(Num), Pages
- **Assertion:** the specific claim this citation supports
- **Status:** ✅ placed
- **Source:** 🧑 scholar-copied by USER (YYYY-MM-DD)

> ✅ SEARCH: [Scholar](https://scholar.google.com/scholar?q=...)
- **Summary:** 2-3 sentences.
```

The **Key** field appears ONLY on placed entries, and is LEARNED from .bib (grep for the paper title after the human adds it), never proposed by the agent.

### Pre-existing entry (was in .bib before _CITATION_ existed)

```markdown
### 📋 P#.S# -- Full Author List (Year). Full Paper Title.

- **Key:** `bibtex_key` (from .bib)
- **Journal:** Full Journal Name Vol(Num), Pages
- **Assertion:** the specific claim this citation supports
- **Status:** ✅ placed
- **Source:** 📋 pre-existing (provenance unknown)
- **Verified:** ⬜ not yet verified / ✅ DOI resolves, metadata matches

> SEARCH: [Scholar](https://scholar.google.com/scholar?q=...)
```

Pre-existing entries are created during AUDIT reconciliation when the agent finds `\citep{key}` in tex that isn't tracked in _CITATION_ yet. They need Phase 5 REVIEW to confirm the paper exists with correct metadata.

### Citation-issue entry (Phase 1 found a problem with an EXISTING cite)

```markdown
### ⚠️ P#.S# -- Citation issue: key may not support claim

- **Current claim:** "the sentence text"
- **Current cite:** bibtex_key
- **Problem:** description of what's wrong
- **Recommendation:** keep / replace / soften claim
- **Alternative candidates:** (if applicable)
```

### Harvest card (Phase 3 HARVEST, from an answering QA file's anchors)

```markdown
### <Full Title>
- <authors> (<year>). <venue>. [status: VERIFIED-by-discovery | 🔍 NEEDS-VERIFICATION]
- summary: <2-3 lines: what the paper does/shows>
- finding: <1-2 lines: the result that matters here, numbers kept>
- relevance: <one line: why it matters to this stage's need>
- Scholar: <link>   (unverified also get `> SEARCH: <string>`)
- source_ref: <discovery folder> (sources.md S##)
```

An entry with only identity fields (title/year/venue + one relevance clause) is a DEFECTIVE harvest -- the user must be able to eyeball WHAT each paper found without opening the discovery.

Status carries provenance -- two levels, never flattened, and these strings are VERBATIM (acceptance greps them literally):
- `status: VERIFIED-by-discovery (<method>, <date>) · 🔍 awaiting JL Scholar+bibtex` -- sources the discovery reviewer verified.
- `status: 🔍 NEEDS-VERIFICATION` -- only for sources nobody has checked.

The 🔍 half never auto-clears: Scholar confirmation + bibtex are HUMAN-ONLY (discovery verification is arXiv-level, not bibtex-level). Writing bare "unverified" on a discovery-verified source DISCARDS earned provenance and is a defective card.

### Status emoji legend (place in the _CITATION_ file header)

```
✅ = in bib + placed in tex + verified on Scholar
📌 = in bib, not yet placed in this section's tex
⚠️ = in bib but needs fix (wrong paper, metadata drift, wrong context)
🔍 = NOT in bib, candidate found by CC, needs user verification
```

### SEARCH markers (every entry ends with one)

- `> SEARCH: [Scholar](url)` -- NOT verified. User needs to click, verify, copy bibtex → .bib.
- `> ✅ SEARCH: [Scholar](url)` -- verified by user. In .bib and ready to place.
- `> ❌ SEARCH: reason` -- rejected by user. Kept as an audit trail (prevents re-finding the same wrong paper).


## _CITATION_ file organization

```markdown
# §N Section-Name: Citation Map

Density: K unique keys / S sentences = D keys/sentence.
M/S sentences carry at least one cite (R).

Venue norm: [venue-specific sentence-with-cite ratio]

[Status emoji legend]

---

## P1. Paragraph headline (N sentences)

### [emoji] P1.S2 -- Author List (Year). Paper Title.
[entry fields]

### [emoji] P1.S3 -- Author List (Year). Paper Title.
[entry fields]

---

## P2. Paragraph headline (N sentences)
...

---

## Density by paragraph

(bullet lines, one per paragraph — NEVER a markdown table; the harvest
acceptance grep `grep -c '^|' == 0` runs on this whole file)

- P1: 7 sentences · 4 cited · 5 keys · density 0.71 — <note>
- P2: 5 sentences · 1 cited · 2 keys · density 0.40 — <note>

## Open items

- [describe any remaining gaps, open question SECTIONS, or issues]
```

Organization rules:
- Group by paragraph (P1, P2, ...) matching the section outline structure.
- Preserve `> USER:` comments verbatim with `> CC:` responses below.
- Keep the density block and open items updated after each phase.


## Tips for the user (during CHECK phase)

The agent runs PROBE automatically and leaves 🔍 CANDIDATE entries in _CITATION_. You handle these during CHECK:

**Verifying a candidate:**
1. Click the `> SEARCH: [Scholar](url)` link in _CITATION_.
2. Find the paper on Scholar, read the abstract, confirm it supports the assertion.
3. Click the cite icon on Scholar, select BibTeX, copy the bibtex block.
4. Paste the bibtex into your `.bib` file.
5. In _CITATION_, change `> SEARCH:` to `> ✅ SEARCH:`.
6. If CHECK restarts PROBE, the agent auto-places the newly verified keys.

**Rejecting a candidate:** change `> SEARCH:` to `> ❌ SEARCH: reason` (e.g., "wrong paper, about nursing not physicians"). The agent marks it ❌ and keeps it as an audit trail.

**Adding a citation the agent missed:** add bibtex to .bib yourself, then add `> USER: cite [key] at P#.S# for [reason]` in _CITATION_ or the outline. The agent picks it up when PROBE restarts (Phase 1a reconciliation).

**Checking what is pending:** grep _CITATION_ for 🔍 (unverified candidates) and ⚠️ (issues); the density block shows overall coverage.


## Citation rounds across the lifecycle

Citations are not one-shot. _CITATION_ accumulates across rounds:

```
Round 0  DRAFT       author cites from memory, some placeholders
Round 1  PROBE       automatic: audit + route + candidate + place (for keys in .bib);
                     🔍 entries flagged for CHECK (not blocking)
Round 2  post-REVISE re-audit (MANDATORY after every revise round): revise rewrites
                     drift citations (sentence split → cite on wrong half; merged →
                     cite lost; reworded → context changed). Re-run Phase 1 AUDIT.
Round 3  CHECK       human reviews 🔍 entries, verifies on Scholar, copies bibtex → .bib,
                     adds > USER: comments (CHECK is the ONLY human-involved phase)
Round 4+ RESTART     if CHECK restarts PROBE, agent reads > USER: comments and responds;
                     re-runs audit + place; each round appends to _CITATION_
```

Best practices:
- _CITATION_ accumulates, never resets. Each round adds entries, updates statuses.
- Rejected entries (❌) stay — prevents re-finding the same wrong paper.
- Post-revise re-audit is mandatory (revise drift is the #1 citation regression).
- The density block updates after every round; _LOG records each round with date, action count, density change.
