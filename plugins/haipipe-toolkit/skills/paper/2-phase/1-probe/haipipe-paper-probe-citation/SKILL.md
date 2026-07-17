---
name: haipipe-paper-probe-citation
description: "citation HARVESTER (probe lane worker). One skill, one working doc (_CITATION_). Transcribes the answering QA file's source anchors into _CITATION_{stage}.md — it NEVER searches (acquisition is the probe SECTION → q-executor → Agent(haipipe-discovery-orchestrator-agent) → QA file). Plus AUDIT (gap → a new question SECTION), PLACE (auto-place keys already in .bib, flag 🔍 for CHECK), REVIEW (pre-submission 3-axis walk). Fully automatic. Hard boundary: NEVER generates bibtex, NEVER adds to .bib. Trigger: citation, cite, probe citations, harvest citations, check references, audit references, citation review, manual review citations."
argument-hint: "[verb] [section-name-or-number] [paper-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, WebFetch
# WebFetch = pointer-following ONLY (fetch a KNOWN DOI/publisher URL to verify an
# entry in Phase 5 REVIEW). WebSearch is deliberately ABSENT: finding is the
# one-door rule: the PROBE phase's DISPATCH is the only acquisition door (JL 2026-07-07).
metadata:
  version: "3.1.0"
  last_updated: "2026-07-14"
  summary: "Citation HARVESTER: AUDIT → ROUTE (gaps → question SECTIONS in 1-probes/) → CANDIDATE (harvest the answering QA file's source anchors) → PLACE → REVIEW. Never searches — one door: the PROBE phase's DISPATCH to Agent(haipipe-discovery-orchestrator-agent). Single working doc = _CITATION_. HARVEST reads the target QA file's `- state:` line first and REFUSES a `working` target (its ## Answer is empty by construction) or a state-less one, and FOLLOWS a `superseded-by:` chain (so stale sources never reach the manuscript). Read-only: NEVER writes a QA file. History: ./CHANGELOG.md."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
  predecessors:
    - "haipipe-paper-edit-check-reference (mechanical \\label/\\ref/\\cite audit) — MERGED as Phase 1"
    - "haipipe-paper-edit-manual-review-citations (pre-submission 3-axis walk) — MERGED as Phase 5"
  absorbs_feedback:
    - "2026-07-01_no-bibtex-in-citation-map.md → Rule 1"
    - "2026-07-01_citation-map-format-unified.md → _CITATION_ format spec"
    - "2026-07-01_citation-summary-depth.md → Rule 3"
    - "2026-06-30_bibtex-sync-from-citation-map.md (from section-edit/) → Rule 2"
---

Skill: haipipe-paper-probe-citation
==================================

citation probe worker for `haipipe-paper-section-edit`.
One skill owns the full citation lifecycle for one section, from gap identification through pre-submission verification.
The single working document is `_CITATION_N-section.md`.

```
/haipipe-paper-probe-citation                            → status dashboard
/haipipe-paper-probe-citation audit <section>            → Phase 1: mechanical check + gap ID
/haipipe-paper-probe-citation route <section>            → Phase 2: gaps → question SECTIONS for the hub (NO searching)
/haipipe-paper-probe-citation harvest <stage> <ref>      → Phase 3: expand the answering QA file's source anchors → _CITATION_ entries
/haipipe-paper-probe-citation place <section>            → Phase 4: auto-place verified keys, flag 🔍 for CHECK
/haipipe-paper-probe-citation review <section>           → Phase 5: pre-submission 3-axis walk
```

## Hard Boundaries

These are non-negotiable.
Every agent invoking this skill must obey them.

1. **NEVER generate bibtex.** LLM-generated bibtex is unreliable (hallucinated authors, wrong year, wrong journal, wrong pages).
   No `@article{...}` or any bibtex block ever appears in _CITATION_.
   The agent writes plain-text descriptions (title, authors, year, journal) for paper identification only.
   The human copies real bibtex from Google Scholar into .bib.

2. **NEVER add entries to .bib directly.** The `.bib` file is human-only territory.
   Only the human adds bibtex to `.bib` (by copying from Google Scholar after verification).
   The agent may place `\citep{}` in tex ONLY for keys that already exist in `.bib`.

3. **Auto-place only for keys already in `.bib`.** During PLACE, the agent greps `.bib` for each candidate.
   If the key exists, the agent places `\citep{}` in tex.
   If the key does NOT exist, the agent leaves the entry as 🔍 and flags it for CHECK.
   The human verifies 🔍 entries and copies bibtex to `.bib` during CHECK.

4. **`\cite{TOADD}` is the draft's citation slot** (JL ruling 2026-07-10, supersedes `[CITE: <topic>]`; treat legacy `[CITE:]` markers the same).
   The section .md carries real `\citep{key}` only for keys already in .bib; every missing citation is `\cite{TOADD}` paired with a `_CITATION_` row naming the topic.
   PROBE greps `TOADD` in the .md (and synced tex), maps each slot to its row, and finds 🔍 candidates.
   TOADD -> real-key replacement happens in the .md FIRST (then sync), and ONLY after the human's bibtex lands in .bib.
   A TOADD surviving into compiled tex fails CHECK via the broken-\cite check.

5. **NEVER remove USER comments from the outline.** Preserve `> USER:` comments verbatim.
   When a comment is resolved, add a `> CC:` response below it explaining the resolution.
   The comment itself stays.


## Provenance tracking

Every _CITATION_ entry carries a **Source** field recording how the paper was found:

```
🧑 scholar-copied    human found and copied bibtex from Scholar → .bib (SAFE)
🤖 harvested         came in through DISPATCH → discovery → the QA file's anchors → harvest
                      (SAFE -- discovery-reviewer-checked at arXiv/DOI level;
                      agent never touched .bib; human Scholar pass in CHECK)
📋 pre-existing      was already in .bib when _CITATION_ was created
                      (provenance UNKNOWN until verified via DOI/DBLP)
```

(Historical entries marked `agent-found via WebSearch` predate the 2026-07-07 one-door ruling; treat them as 📋-grade until REVIEW verifies them.)

Pre-existing entries (📋) may include LLM-generated bibtex from a prior session before the hard boundary was established.
Phase 5 REVIEW catches these by verifying existence + metadata against publisher pages.


## Five Phases (fully automatic)

```
Phase 1: AUDIT        mechanical cross-ref + identify uncited factual assertions
Phase 2: ROUTE        gaps → question SECTIONS for the hub (NO searching;
                      acquisition = the PROBE phase's DISPATCH → discovery, the only door)
Phase 3: CANDIDATE    HARVEST the answering QA file's anchors → 🔍 entries in _CITATION_
Phase 4: PLACE        auto-place keys already in .bib; flag 🔍 for CHECK
Phase 5: REVIEW       pre-submission 3-axis walk (existence, metadata, context)
```

All five phases run automatically without stopping for human input.
The agent writes 🔍 candidates and continues.
The 🔍 markers are FLAGS for CHECK to verify later, not blocking gates.

Human review happens ONLY in the CHECK phase (haipipe-paper-check).
During CHECK, the human clicks Scholar links for 🔍 entries, verifies papers, copies bibtex to .bib, and adds `> USER:` comments.
If CHECK restarts the PROBE phase, the agent reads those `> USER:` comments and responds to them.


## Harvest mode (supply-push, any stage)

The five phases above are demand-pull: the section's text needs citations, go find them.
HARVEST is the reverse direction: a question SECTION was answered and the answering QA file carries literature sources; this worker distills them into the stage's `_CITATION_` so the user can eyeball them paper-side.
Called by haipipe-paper-probe at ⑤ INTERPRET, once a section's `target:` resolves (e.g. the seed landscape question).

```
harvest <stage> <qa_file>    e.g. harvest 0-seed discoveries/D0703_seed-landscape/QA/1-cgm-fm-landscape.md
```

⚠️ **PRECONDITION — READ THE TARGET'S STATE LINE BEFORE HARVESTING (R19/R20).** A QA file is a TICKET that becomes a RECEIPT.
The normal caller (paper-probe ⑤ INTERPRET) already gates this, but the direct invocation above is published and must gate itself:

```
state=$(sed -n 's/^- state:[[:space:]]*//p' "$qa_file" | head -1)
```

```
  state: answered        ✅ HARVEST. (and it carries no `superseded-by:`)
  state: working         🚫 REFUSE. The `## Answer` is EMPTY BY CONSTRUCTION — the run is still
                         in flight. Harvesting yields ZERO anchors and reports a silent no-op,
                         which HIDES a live claim. Report "in progress since <started>" and stop.
  … superseded-by: X     🔗 FOLLOW THE CHAIN and harvest the LIVE file instead. Transcribing a
                         superseded file's sources puts STALE references into _CITATION_, and
                         PLACE then auto-places any key already in .bib INTO THE MANUSCRIPT —
                         the day-1/day-40 stale-read bug arriving through the HARVEST lane,
                         where the checker's read-target-superseded tooth cannot see it.
  NO state line          🚫 REFUSE. `state:` is MANDATORY (checker: qa-no-state).
```

This is READ-ONLY.
This worker still NEVER writes the QA file — ONE WRITER, the executor, always.

Harvest ALWAYS runs as a dispatched SUBAGENT (produce) and the calling worker reviews the result (mechanical acceptance) -- producer and reviewer are never the same context:

```
input     the section's `target:` QA file + its `sources:` lane line
          (the QA file's Answer anchors name the sources.md S## entries)
SUBAGENT  in its OWN clean context: opens the QA file, follows its anchors into
          the task-folder's sources.md, reads ONLY the anchored S## entries (no free
          browsing), expands each into a _CITATION_ entry (format below), writes
          _CITATION_{stage}.md directly, returns a one-line summary + counts
          ("12 entries, 5 VERIFIED / 7 🔍").
WORKER    mechanical acceptance, WITHOUT reading project files:
          entries == anchor count? every entry has summary/finding/anchor?
          `grep -c '@' == 0` (no bibtex)? -> log to _LOG + index on pass;
          re-dispatch the subagent with the failure note on fail.
```

The paper session never reads sources.md in either role; content-level quality is anchored upstream (sources.md is discovery-reviewer-gated) and checked by the human in CHECK via the per-card anchors.

Procedure (inside the subagent):

1. Establish the source set from the QA file's `## Answer` anchors; open the task-folder's `sources.md` and read ONLY the anchored entries.
2. Write/extend `_CITATION_{stage}.md`: NEVER tables.
   Group by literature/theme (`##`); one paper per `###` subsection, FULL title in the heading, bullet fields transcribed from the manifest.
   Harvest-card template: `ref/citation-format.md`.
   An entry with only identity fields (title/year/venue + one relevance clause) is a DEFECTIVE harvest — the user must be able to eyeball WHAT each paper found without opening the discovery.
3. Status carries provenance in the card's VERBATIM strings — acceptance greps them LITERALLY, so a semantically-equal synonym (`retrieved ✅ (discovery, ...)`, `confirmed at discovery`) is a DEFECTIVE card, and writing bare "unverified" on a discovery-verified source DISCARDS earned provenance.
   Exact strings + the two provenance levels: `ref/citation-format.md`.
   The 🔍 half never auto-clears: Scholar confirmation + bibtex are HUMAN-ONLY (discovery verification is arXiv-level, not bibtex-level).
4. Do NOT search for new papers in harvest mode -- harvest only what the probe brought back.
   Gaps noticed while harvesting become probe-plan suggestions, not fresh WebSearch calls.
5. No placement: early stages are markdown; PLACE only applies when a tex section exists.

All Hard Boundaries above apply unchanged (no bibtex, no .bib edits, 🔍 resolves in CHECK).


## Phase 1: AUDIT

Three sub-checks run together.

### 1a. Reconciliation (.bib ↔ _CITATION_ ↔ tex sync)

Read all three files and reconcile.
This is MECHANICAL (no judgment needed).

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

This reconciliation runs FIRST, before gap analysis, every time the skill is invoked.
It catches:
- Citations the human added to .bib since last round (🔍 → 📌)
- Citations added directly to tex+bib without going through _CITATION_ (→ 📋)
- Broken references from .bib cleanup or typos (→ ⚠️)

### 1b. Mechanical cross-reference audit (from check-reference)

Scan the section's tex file for marker integrity:

- Every `\cite{key}` resolves to a `@type{key, ...}` entry in the `.bib`
- No orphan bib entries cited only in this section
- No `\label`/`\ref` breaks in the section
- `\phantomsection\label{}` positioned correctly relative to `\section*{}`

Tool: run the sibling `checks.sh` (bash, stdlib only — NOT Python) on the paper root.
It audits `\label`/`\ref`/`\cite` resolution and flags bibtex leaked into markdown.

```bash
bash ../../3-check/haipipe-paper-check/checks.sh <paper-root-dir>
```

Optionally add `--md _CITATION_<stage>.md` to also scan the working doc for leaked bibtex, or `--depth N` for deeply nested layouts.
Audit criteria (as above): every `\cite` resolves to a `.bib` entry, no orphan bib entries, no `\label`/`\ref` breaks.

### 1c. Gap identification

Read the section outline and tex.
For each sentence:

- Is it a factual assertion (not "our study does X")?
- Does it have a citation?
- If cited, does the cited paper plausibly support the claim?

Output: a gap list in chat (not written to files yet).
Each gap is:
```
P#.S# | sentence text | gap type (uncited / wrong-context / weak)
```

Also process any `> USER:` comments requesting citations (e.g., "needs cite here", "find a paper about X").


## Phase 2: ROUTE (search is RETIRED — JL 2026-07-07: "search should be done with haipipe-discovery-orchestrated agent")

This worker NEVER searches.
Not WebSearch, not Semantic Scholar, not a side-channel agent — a citation found any way other than the PROBE phase's DISPATCH has no reviewer and no ledger home, and skips the mechanical acceptance that guards _CITATION_.
There is exactly ONE door for a citation to enter this document:

```
Phase-1 gap  →  a question SECTION in 1-probes/PPNN_<topic>.md (serves / target /
                state / q-executor/a-consumer)
             →  the PROBE hub (haipipe-paper-probe) runs ② MATCH against the bank's
                QA corpus first — a citation already established by an existing
                discovery is a T2 REUSE and costs one grep and one read
             →  only if MATCH cannot close it, the hub DISPATCHES the section's
                `q-executor:` block, VERBATIM, to
                Agent(haipipe-discovery-orchestrator-agent)
             →  the executor runs its own qa gate; sources land in
                discoveries/<discovery-group>/<discovery-folder>/sources.md, reviewer-checked, and the readable
                digest lands at discoveries/<discovery-group>/<discovery-folder>/QA/<n>-<slug>.md
             →  the section's `target:` points at that QA FILE; its `## Answer`
                anchors ([→ sources.md#S02]) are what this worker transcribes
                → HARVEST (below) → _CITATION_ entries
```

Phase 2 therefore produces question SECTIONS, not papers: for each Phase-1 gap write the one-line Need (+ Why + Route hint: single-lookup → ENRICH; landscape → discovery Review; claim question → mode full) and hand the list to the hub.
"light"/"full" are the PROBE FILE's `mode:` (light = the answer is read and interpreted; full = the author additionally writes the claim status into 1-claims.md from the answer) — never an inline shortcut tier.

**Paper-local sweep BEFORE raising any question** (JL 2026-07-10: "you can check previous stage's _CITATION instead of do the heavy one").
A gap is only a gap if the paper hasn't already solved it: before opening a new question SECTION, grep the OTHER stages' `_CITATION_*.md` maps (pitch, narrative, sibling sections), the .bib, AND prior stages' `answered | read | answered-local` probe SECTIONS for the topic — their `target:` / `sources:` lanes point at an already-reviewed `discoveries/<discovery-group>/<discovery-folder>/QA/<n>-<slug>.md` and the `sources.md` it anchors (pointer-following: the section names the path, so reading it is legal here).
A match is ADOPTED — copy the entry into this section's _CITATION_ with `Note: adopted from _CITATION_<stage>.md`, keeping its status and provenance: a ✅/📌 elsewhere means the key is in .bib → re-grep the .bib to confirm (HB3 — the sibling's verdict is a pointer, not proof), then PLACE it here; a 🔍 there stays 🔍 here (same candidate, same pending human verification — no re-discovery).
Only gaps that survive this sweep become probe-plan suggestions.
This is not searching: the maps are the paper's own curated indexes.


## Phase 3: CANDIDATE → _CITATION_

Write harvested results (from the answering QA file's source anchors, via HARVEST above) as 🔍 CANDIDATE entries in `_CITATION_N-section.md`.

Entry formats — **candidate** · **placed** · **pre-existing** · **citation-issue** — plus the status-emoji legend and the `> SEARCH:` markers: **`ref/citation-format.md`**.

Load-bearing rules (kept here because PLACE and CHECK depend on them):
- A candidate carries NO bibtex block and NO Key field — the key is LEARNED from .bib later, never proposed by the agent.
- NO .bib edit and NO `\citep{}` placement on a candidate — that is PLACE's job, and only for a key already in .bib.
- The Key field appears ONLY on a placed entry.


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
   - Replace the matching `\cite{TOADD}` in the section .MD with `\citep{key}` (md-first, per Hard Boundary 4), then sync to tex
   - Update the density table

3. **If the key is NOT in .bib** (new candidate, not yet verified):
   - Leave the entry as 🔍 CANDIDATE
   - Do NOT place `\citep{}` in tex
   - The entry's `> SEARCH: [Scholar](url)` link stays as a flag for CHECK
   - Continue to the next entry (no blocking)

The agent processes ALL candidates in one pass and moves on.
Unverified 🔍 entries are resolved during the CHECK phase, where the human clicks Scholar links, verifies papers, and copies bibtex to `.bib`.


## Phase 5: REVIEW (pre-submission)

The slow, paranoid, human-paced verification pass.
Run before a top-tier submission when one wrong-context cite is a desk-reject risk.

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

Google Scholar is a fallback discovery aid, never the primary source for verification.
Scholar's metadata is scraped and often wrong.

**One cite at a time.
One human approval per fix.
No batching.**

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

For cite keys used in 2+ sections, check the cite is used for the same purpose in each location.
The lit-review use is usually right (drafted while reading the paper); the intro use may be wrong (drafted from memory).

### Wrong-context audit patterns

High-risk patterns to actively hunt:
- Famous-author proxy cites (Kahneman, Cialdini cited for a specific claim)
- "Standard practice" cites (one paper standing in for a whole literature)
- Method-claim cites (cited method ≠ implemented method)
- Self-cites (easiest to get wrong due to self-trust)


## _CITATION_ file organization

Group by paragraph (P1, P2, …) matching the section outline; a Density block at the end (bullet lines, NEVER a markdown table — the acceptance grep `grep -c '^|' == 0` runs on the whole file); an Open items block; `> USER:` comments preserved verbatim with `> CC:` responses below.
Full file template: **`ref/citation-format.md`**.


## Relation to sibling skills

Three HARVESTERS in `1-probe/`, one working-doc each, all fully automatic (human review in CHECK only) — they follow pointers the answering QA file names, never find things:
- `haipipe-paper-probe-citation` (THIS) — _CITATION_.md — AUDIT → ROUTE → CANDIDATE(harvest) → PLACE → REVIEW
- `haipipe-paper-probe-values` — _VALUES_.md — same lifecycle
- `haipipe-paper-probe-display` — 0-displays/ units — AUDIT → PLAN(route) → LINK(harvest) → REVIEW

ANY citation acquisition (single lookup, topic, landscape, claim) goes through the PROBE hub → DISPATCH to Agent(haipipe-discovery-orchestrator-agent) — the only door.


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


## User guide + lifecycle rounds

The CHECK-phase user guide (verify / reject / add a candidate; check what's pending) and the multi-round accumulation model (DRAFT → PROBE → mandatory post-REVISE re-audit → CHECK → RESTART; _CITATION_ accumulates and never resets, rejected ❌ entries stay): **`ref/citation-format.md`**.
