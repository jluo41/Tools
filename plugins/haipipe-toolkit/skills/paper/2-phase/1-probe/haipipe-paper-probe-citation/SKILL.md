---
name: haipipe-paper-probe-citation
description: "citation probe worker. One skill, one working doc (_CITATION_). Two directions: demand-pull for section-edit (AUDIT mechanical cross-ref + gap identification → SEARCH find candidates → CANDIDATE write to _CITATION_ with SEARCH markers → PLACE auto-place verified keys from .bib, flag 🔍 for CHECK → REVIEW pre-submission 3-axis walk) and supply-push HARVEST for any stage (distill sources a probe/discovery brought back into _CITATION_{stage}.md candidates, no fresh searching). Fully automatic -- no human gate. Human review happens in CHECK phase only. Hard boundary: agent NEVER generates bibtex, NEVER adds to .bib. No bibtex in _CITATION_ ever. Trigger: citation, cite, probe citations, harvest citations, check references, audit references, citation review, manual review citations."
argument-hint: "[verb] [section-name-or-number] [paper-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Agent, WebFetch, WebSearch
metadata:
  version: "1.5.1"
  last_updated: "2026-07-05"
  summary: "Unified citation probe worker. AUDIT→SEARCH→CANDIDATE→PLACE→REVIEW lifecycle (fully automatic, no human gate). Human review happens in CHECK only. Single working doc = _CITATION_ (plain text only, no bibtex ever). Absorbs check-reference + manual-review-citations."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
  predecessors:
    - "haipipe-paper-probe-citation (mechanical \\label/\\ref/\\cite audit) — MERGED as Phase 1"
    - "haipipe-paper-probe-citation (pre-submission 3-axis walk) — MERGED as Phase 5"
  absorbs_feedback:
    - "2026-07-01_no-bibtex-in-citation-map.md → Rule 1"
    - "2026-07-01_citation-map-format-unified.md → _CITATION_ format spec"
    - "2026-07-01_citation-summary-depth.md → Rule 3"
    - "2026-06-30_bibtex-sync-from-citation-map.md (from section-edit/) → Rule 2"
---

Skill: haipipe-paper-probe-citation
==================================

citation probe worker for `haipipe-paper-section-edit`. One skill owns the full citation lifecycle for one section, from gap identification through pre-submission verification. The single working document is `_CITATION_N-section.md`.

```
/haipipe-paper-probe-citation                            → status dashboard
/haipipe-paper-probe-citation audit <section>            → Phase 1: mechanical check + gap ID
/haipipe-paper-probe-citation search <section>           → Phase 2-3: find candidates, write to _CITATION_
/haipipe-paper-probe-citation place <section>            → Phase 4: auto-place verified keys, flag 🔍 for CHECK
/haipipe-paper-probe-citation review <section>           → Phase 5: pre-submission 3-axis walk
```

## Hard Boundaries

These are non-negotiable. Every agent invoking this skill must obey them.

1. **NEVER generate bibtex.** LLM-generated bibtex is unreliable (hallucinated authors, wrong year, wrong journal, wrong pages). No `@article{...}` or any bibtex block ever appears in _CITATION_. The agent writes plain-text descriptions (title, authors, year, journal) for paper identification only. The human copies real bibtex from Google Scholar into .bib.

2. **NEVER add entries to .bib directly.** The `.bib` file is human-only territory. Only the human adds bibtex to `.bib` (by copying from Google Scholar after verification). The agent may place `\citep{}` in tex ONLY for keys that already exist in `.bib`.

3. **Auto-place only for keys already in `.bib`.** During PLACE, the agent greps `.bib` for each candidate. If the key exists, the agent places `\citep{}` in tex. If the key does NOT exist, the agent leaves the entry as 🔍 and flags it for CHECK. The human verifies 🔍 entries and copies bibtex to `.bib` during CHECK.

4. **NEVER remove USER comments from the outline.** Preserve `> USER:` comments verbatim. When a comment is resolved, add a `> CC:` response below it explaining the resolution. The comment itself stays.

5. **NO bibtex in _CITATION_.** The _CITATION_ file is a plain-text MAP (what to cite, where, why). The .bib file is the DATA (actual bibtex entries). These are separate concerns. _CITATION_ contains paper descriptions for identification; .bib contains machine-readable bibtex for LaTeX. The agent never copies bibtex between the two.


## The .bib ↔ _CITATION_ separation

```
_CITATION_.md  = the MAP     agent writes    plain text (title, authors, year, link)
.bib           = the DATA    human writes    bibtex (@article{key, ...})
tex            = the OUTPUT  agent writes    \citep{key} (only for verified keys)
```

Data flow is one-directional for writes:
- Agent → _CITATION_ (candidates, status, provenance, Scholar links)
- Human → .bib (copies bibtex from Google Scholar)
- Agent → tex (places \citep{} only after human verifies AND key exists in .bib)

The agent reads .bib (to check key existence) and tex (to audit what's cited), but writes to neither .bib nor tex until verification conditions are met.

Why this matters: you can always tell where an entry came from. If bibtex is ONLY in .bib and the agent NEVER writes .bib, then every .bib entry was human-added from a publisher source. The _CITATION_ map tracks which papers were agent-found vs pre-existing, so provenance is always clear.


## Provenance tracking

Every _CITATION_ entry carries a **Source** field recording how the paper was found:

```
🧑 scholar-copied    human found and copied bibtex from Scholar → .bib (SAFE)
🤖 agent-found       agent found via WebSearch, wrote to _CITATION_ only
                      (SAFE -- agent never touched .bib; human must verify)
📋 pre-existing      was already in .bib when _CITATION_ was created
                      (provenance UNKNOWN until verified via DOI/DBLP)
```

Pre-existing entries (📋) may include LLM-generated bibtex from a prior session before the hard boundary was established. Phase 5 REVIEW catches these by verifying existence + metadata against publisher pages.


## Five Phases (fully automatic)

```
Phase 1: AUDIT        mechanical cross-ref + identify uncited factual assertions
Phase 2: SEARCH       find candidate papers for gaps
Phase 3: CANDIDATE    write 🔍 entries to _CITATION_ with > SEARCH markers
Phase 4: PLACE        auto-place keys already in .bib; flag 🔍 for CHECK
Phase 5: REVIEW       pre-submission 3-axis walk (existence, metadata, context)
```

All five phases run automatically without stopping for human input. The agent writes 🔍 candidates and continues. The 🔍 markers are FLAGS for CHECK to verify later, not blocking gates.

Human review happens ONLY in the CHECK phase (haipipe-paper-check). During CHECK, the human clicks Scholar links for 🔍 entries, verifies papers, copies bibtex to .bib, and adds `> USER:` comments. If CHECK restarts the PROBE phase, the agent reads those `> USER:` comments and responds to them.


## Harvest mode (supply-push, any stage)

The five phases above are demand-pull: the section's text needs citations, go find them. HARVEST is the reverse direction: a probe already ran and its Read output carries literature sources; this worker distills them into the stage's `_CITATION_` so the user can eyeball them paper-side. Called by haipipe-paper-probe after a gateway probe returns (e.g. the seed landscape probe).

```
harvest <stage> <probe_ref>       e.g. harvest 0-seed probes/D0703_seed-landscape
```

Harvest ALWAYS runs as a dispatched SUBAGENT (produce) and the calling worker reviews the result (mechanical acceptance) -- producer and reviewer are never the same context:

```
input     the probe agent's return: ref + pick_list
          ({anchor: sources.md S##, why: "<one line>"} per relevant source)
SUBAGENT  in its OWN clean context: opens the ref'd sources.md, reads ONLY the
          picked S## entries (no free browsing), expands each into a _CITATION_
          card (format below), writes _CITATION_{stage}.md directly, returns a
          one-line summary + counts ("12 cards, 5 VERIFIED / 7 🔍").
WORKER    mechanical acceptance, WITHOUT reading project files:
          cards == pick_list count? every card has summary/finding/anchor?
          `grep -c '@' == 0` (no bibtex)? -> log to _LOG + index on pass;
          re-dispatch the subagent with the failure note on fail.
```

The paper session never reads sources.md in either role; content-level quality is anchored upstream (sources.md is discovery-reviewer-gated) and checked by the human in CHECK via the per-card anchors.

Procedure (inside the subagent):

1. Establish the source set from the pick_list; open the ref'd discovery's `sources.md` and read only the picked entries.
2. Write/extend `_CITATION_{stage}.md`: NEVER tables. Group by literature/theme (`##` sections); one paper per `###` subsection with FULL title in the heading and bullet fields transcribed from the manifest:

```
### <Full Title>
- <authors> (<year>). <venue>. [status: VERIFIED-by-discovery | 🔍 NEEDS-VERIFICATION]
- summary: <2-3 lines: what the paper does/shows>
- finding: <1-2 lines: the result that matters here, numbers kept>
- relevance: <one line: why it matters to this stage's need>
- Scholar: <link>   (unverified also get `> SEARCH: <string>`)
- source_ref: <discovery folder> (sources.md S##)
```

An entry with only identity fields (title/year/venue + one relevance clause) is a DEFECTIVE harvest -- the user must be able to eyeball WHAT each paper found without opening the discovery. Numbered one-line entries remain acceptable ONLY for bare reference lists in the demand-pull phases, never for harvest cards.
3. Status carries provenance -- two levels, never flattened: `status: VERIFIED-by-discovery (<method>, <date>) · 🔍 awaiting JL Scholar+bibtex` for sources the discovery reviewer verified; `status: 🔍 NEEDS-VERIFICATION` only for sources nobody has checked. Writing bare "unverified" on a discovery-verified source DISCARDS earned provenance and is a defective card (test-2-2222: all 5 cards said "🔍 candidate (unverified)" while sources.md held 15/15 VERIFIED-with-method). The 🔍 half never auto-clears: Scholar confirmation + bibtex are HUMAN-ONLY (house rule -- discovery verification is arXiv-level, not bibtex-level).
4. Do NOT search for new papers in harvest mode -- harvest only what the probe brought back. Gaps noticed while harvesting become probe-plan suggestions, not fresh WebSearch calls.
5. No placement: early stages are markdown; PLACE only applies when a tex section exists.

All Hard Boundaries above apply unchanged (no bibtex, no .bib edits, 🔍 resolves in CHECK).


## Phase 1: AUDIT

Three sub-checks run together.

### 1a. Reconciliation (.bib ↔ _CITATION_ ↔ tex sync)

Read all three files and reconcile. This is MECHANICAL (no judgment needed).

```
For each \citep{key} in tex:
  key in .bib?     key in _CITATION_?   Action
  ─────────────    ──────────────────   ──────────────────────────────
  ✅ yes           ✅ yes               check status matches, OK
  ✅ yes           ❌ no                add to _CITATION_ as 📋 pre-existing
  ❌ no            ✅ yes               ⚠️ broken ref (key cited but missing from .bib)
  ❌ no            ❌ no                ⚠️ broken ref + untracked

For each entry in _CITATION_ with status 🔍:
  key now in .bib?   Action
  ────────────────   ──────────────────────────────
  ✅ yes             human added it! update 🔍 → 📌 (ready to place)
  ❌ no              still 🔍, still waiting for human verification
```

This reconciliation runs FIRST, before gap analysis, every time the skill is invoked. It catches:
- Citations the human added to .bib since last round (🔍 → 📌)
- Citations added directly to tex+bib without going through _CITATION_ (→ 📋)
- Broken references from .bib cleanup or typos (→ ⚠️)

### 1b. Mechanical cross-reference audit (from check-reference)

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

### 1c. Gap identification

Read the section outline and tex. For each sentence:

- Is it a factual assertion (not "our study does X")?
- Does it have a citation?
- If cited, does the cited paper plausibly support the claim?

Output: a gap list in chat (not written to files yet). Each gap is:
```
P#.S# | sentence text | gap type (uncited / wrong-context / weak)
```

Also process any `> USER:` comments requesting citations (e.g., "needs cite here", "find a paper about X").


## Phase 2: SEARCH

For each gap from Phase 1, search for candidate papers.

### Search routing

All evidence needs prefer routing through /haipipe-probe. Use light mode for quick lookups, full mode for claim-level questions.

| Gap type | Probe mode | Gather mechanism |
|---|---|---|
| Single paper lookup ("find the JAMA paper about X") | light | WebSearch agent |
| Targeted topic ("IS papers on physician reviews") | light | WebSearch + Semantic Scholar |
| Broad field gap (needs literature landscape) | light | /haipipe-discovery |
| Claim-level evidence question ("does H1 hold?") | full | /haipipe-probe → task/discovery |

Light probes stop at Read: the output goes directly into a _CITATION_ candidate entry. Full probes continue through Judge→Deposit and file insight cards.

For WebSearch agents within a light probe, launch them in parallel (one per gap) via the Agent tool. Each agent returns: candidate paper(s) with title, authors, year, journal, and a 2-3 sentence summary.


## Phase 3: CANDIDATE → _CITATION_

Write search results as 🔍 CANDIDATE entries in `_CITATION_N-section.md`.

### Candidate entry format (agent-found, NOT in .bib yet)

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

Rules for the candidate entry:

- **Full paper title** in the heading (not a short description)
- **Full author list** in the heading (not "et al.")
- **Journal with volume/number/pages** when known
- **Scholar link** as a clickable markdown link (not bare URL)
- **2-3 sentence summary** with method + finding + relevance (not one-liner)
- **NO Key field on candidates** (the bibtex key is determined by whatever Scholar generates when the human copies bibtex; the agent discovers it later by grepping .bib)
- **NO bibtex block** (plain-text description only; bibtex lives exclusively in .bib)
- **NO .bib edit** (never add to .bib)
- **NO .tex edit** (never place \citep{})
- **Placement recommendation** so the human knows where to cite after verifying

### Placed entry format (verified, in .bib, placed in tex)

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

### Pre-existing entry format (was in .bib before _CITATION_ existed)

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

Pre-existing entries are created during AUDIT reconciliation when the agent finds `\citep{key}` in tex that isn't tracked in _CITATION_ yet. They need verification (Phase 5 REVIEW) to confirm the paper actually exists with correct metadata.

### Status emoji legend (place in file header)

```
✅ = in bib + placed in tex + verified on Scholar
📌 = in bib, not yet placed in this section's tex
⚠️ = in bib but needs fix (wrong paper, metadata drift, wrong context)
🔍 = NOT in bib, candidate found by CC, needs user verification
```

### SEARCH markers

Every entry ends with one of:
- `> SEARCH: [Scholar](url)` -- NOT verified. User needs to click, verify, copy bibtex → .bib
- `> ✅ SEARCH: [Scholar](url)` -- verified by user. In .bib and ready to place.

### Citation issue entries

When Phase 1 finds a problem with an EXISTING citation (wrong context, metadata drift, citation doesn't hold), write it as:

```markdown
### ⚠️ P#.S# -- Citation issue: key may not support claim

- **Current claim:** "the sentence text"
- **Current cite:** bibtex_key
- **Problem:** description of what's wrong
- **Recommendation:** keep / replace / soften claim
- **Alternative candidates:** (if applicable)
```


## Phase 4: PLACE (automatic)

The agent auto-places citations for keys that already exist in `.bib` and flags the rest for CHECK.

1. **For each candidate in _CITATION_,** grep `.bib` for the paper title (or a distinctive substring):
   ```bash
   grep -i "variations in physician practice" *.bib
   # → @article{eddy1984variations,
   ```

2. **If the key IS in .bib** (already verified from a prior round or pre-existing):
   - Learn the key from .bib
   - Add `- **Key:** \`eddy1984variations\` (learned from .bib)` to the _CITATION_ entry
   - Update status: 🔍 → ✅
   - Place `\citep{key}` in the section tex at the recommended location
   - Sync the outline (add parenthetical reference)
   - Update the density table

3. **If the key is NOT in .bib** (new candidate, not yet verified):
   - Leave the entry as 🔍 CANDIDATE
   - Do NOT place `\citep{}` in tex
   - The entry's `> SEARCH: [Scholar](url)` link stays as a flag for CHECK
   - Continue to the next entry (no blocking)

The agent processes ALL candidates in one pass and moves on. Unverified 🔍 entries are resolved during the CHECK phase, where the human clicks Scholar links, verifies papers, and copies bibtex to `.bib`.


## Phase 5: REVIEW (pre-submission)

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

Google Scholar is a fallback discovery aid, never the primary source for verification. Scholar's metadata is scraped and often wrong.

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

For cite keys used in 2+ sections, check the cite is used for the same purpose in each location. The lit-review use is usually right (drafted while reading the paper); the intro use may be wrong (drafted from memory).

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
- Preserve `> USER:` comments verbatim with `> CC:` responses below
- Keep density table and open items updated after each phase


## Relation to sibling skills

```
1-probe/
  haipipe-paper-probe-citation     ← THIS (citation, _CITATION_.md)
  haipipe-paper-probe-values       ← values, _VALUES_.md
  haipipe-paper-probe-display      ← display, 0-displays/ units
```

All three follow the same shape: AUDIT → SEARCH → CANDIDATE → PLACE → REVIEW.
Each owns one working document type. All three are fully automatic (no human gate). Human review happens in CHECK only.


## Relation to other skills

| If the author wants ... | Use |
|---|---|
| Probe citations for a section (search + candidate + place) | **this skill**, Phase 1-4 (automatic) |
| Pre-submission citation walk | **this skill**, Phase 5 |
| Broad literature search (field landscape) | /haipipe-discovery |
| Claim-level evidence question | /haipipe-probe |
| Quick bib hygiene (placeholders, duplicates) | /citation-verifier |
| Cross-model autonomous citation audit | /citation-audit |


## Done criteria

citation is done when:
- [ ] All `> USER:` citation comments are resolved (candidate found or acknowledged)
- [ ] All factual assertions have citations or are explicitly uncited-by-design
- [ ] All candidates are written to _CITATION_ with > SEARCH markers
- [ ] All keys found in .bib are auto-placed in tex
- [ ] Remaining 🔍 entries are flagged for CHECK (not blocking)
- [ ] Density meets venue norm (counting placed citations)
- [ ] No ⚠️ entries remaining (all issues resolved)
- [ ] _LOG updated with citation probe summary


## Tips for the user (during CHECK phase)

The agent runs PROBE automatically and leaves 🔍 CANDIDATE entries in _CITATION_. You handle these during CHECK:

**Verifying a candidate (during CHECK):**
1. Click the `> SEARCH: [Scholar](url)` link in _CITATION_
2. Find the paper on Scholar, read the abstract, confirm it supports the assertion
3. Click the `"` cite icon on Scholar, select BibTeX, copy the bibtex block
4. Paste the bibtex into your `.bib` file (bibtex lives ONLY in .bib, never in _CITATION_)
5. In _CITATION_, change `> SEARCH:` to `> ✅ SEARCH:`
6. If CHECK restarts PROBE, the agent auto-places the newly verified keys

**Rejecting a candidate:**
- Change `> SEARCH:` to `> ❌ SEARCH: reason` (e.g., "wrong paper, about nursing not physicians")
- The agent marks it ❌ and keeps it as audit trail (prevents re-searching the same wrong paper in a later round)

**Adding a citation the agent missed:**
- Add bibtex to .bib yourself
- Add `> USER: cite [key] at P#.S# for [reason]` in _CITATION_ or the outline
- The agent picks it up when PROBE restarts (Phase 1a reconciliation)

**Checking what is pending:**
- Grep _CITATION_ for 🔍 to see unverified candidates
- Grep _CITATION_ for ⚠️ to see issues needing attention
- The density table at the bottom shows overall coverage


## Citation rounds across the lifecycle

Citations are not one-shot. _CITATION_ accumulates across multiple rounds:

```
Round 0  DRAFT       author cites from memory, some placeholders
Round 1  PROBE       automatic: audit + search + candidate + place (for keys in .bib)
                     🔍 entries flagged for CHECK (not blocking)

Round 2  post-REVISE re-audit (MANDATORY after every revise round)
                     revise rewrites can drift citations:
                     sentence split → cite lands on wrong half
                     sentence merged → cite lost
                     claim reworded → cite context changed
                     agent re-runs Phase 1 AUDIT, flags drift

Round 3  CHECK       human reviews 🔍 entries, verifies on Scholar,
                     copies bibtex → .bib, adds > USER: comments
                     (CHECK is the ONLY human-involved phase)

Round 4+  RESTART    if CHECK restarts PROBE, agent reads > USER: comments
                     and responds; re-runs audit + search + place
                     each round appends to _CITATION_
```

Best practices:
- _CITATION_ accumulates, never resets. Each round adds entries, updates statuses.
- Rejected entries (❌) stay. Prevents re-searching the same wrong paper.
- Post-revise re-audit is mandatory. Rewriting can move/lose citations.
- Density table updates after every round. Track coverage trend.
- _LOG records each citation round with date, action count, density change.


## Anti-patterns

- ❌ Putting bibtex blocks in _CITATION_ (bibtex lives ONLY in .bib)
- ❌ Proposing a bibtex key on candidate entries (the key is determined by Scholar when the human copies; the agent discovers it later by grepping .bib)
- ❌ Generating bibtex from memory or search results (hallucination risk)
- ❌ Adding entries to .bib directly (human-only operation)
- ❌ Placing \citep{} for papers whose key is not in .bib (agent checks with grep)
- ❌ Writing one-line summaries ("Evaluates the effect of X") instead of method + finding + relevance
- ❌ Using "et al." shorthand in entry headings instead of full author list
- ❌ Removing USER comments after resolving them (preserve with CC response)
- ❌ Trusting bib metadata over the publisher page (publisher page decides)
- ❌ Skipping the abstract-read for "obvious" cites (obvious ≠ verified)
- ❌ Batching fixes in Phase 5 REVIEW (one cite, one approval, no batching)
- ❌ Resetting _CITATION_ between rounds (accumulate, never reset)
- ❌ Skipping post-revise re-audit (revise drift is the #1 citation regression)
