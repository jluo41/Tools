---
name: novelty-check
description: Verify research idea novelty against recent literature. Use when user says "查新", "novelty check", "有没有人做过", "check novelty", or wants to verify a research idea is novel before implementing.
argument-hint: "[method-or-idea-description]"
allowed-tools: WebSearch, WebFetch, Grep, Read, Glob, mcp__codex__codex
metadata:
  version: "0.2.0"
  last_updated: "2026-08-23"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# Novelty Check Skill

Check whether a proposed method/idea has already been done in the literature: **$ARGUMENTS**

## Constants

- REVIEWER_MODEL = `gpt-5.4` — Model used via Codex MCP. Must be an OpenAI model (e.g., `gpt-5.4`, `o3`, `gpt-4o`)

## Venue Filter (optional)

Parse `$ARGUMENTS` for a `— venues:` directive (e.g. `— venues: utd24-is`):

- If present, locate the matching venue file under `0_venue/` (e.g. `0_venue/utd24-is-venues.md` for `utd24-is`). Read it and extract the union of `S2 venue strings (any-of match)`.
- In Phase B, run a **first pass** restricted to those venues: append the venue list to every search query (e.g. `"<claim> venue:\"MIS Quarterly\" OR venue:\"Information Systems Research\" OR venue:\"Management Science\""`) and prefer hits from those journals.
- If fewer than 5 prior-art hits surface from the venue-restricted pass, expand to broad web/arXiv (Phase B as written) — record both passes separately in the report.
- In Phase D, every prior-work entry already carries a `venue:` field; add a sub-section split: **"Prior work within target venues"** vs **"Prior work outside target venues"**.
- If the venue file is missing, fail loudly with the expected path.

If no `— venues:` directive is given, skip this filter (default behavior — search broadly).

## Instructions

Given a method description, systematically verify its novelty:

### Phase A: Extract Key Claims
1. Read the user's method description
2. Identify 3-5 core technical claims that would need to be novel:
   - What is the method?
   - What problem does it solve?
   - What is the mechanism?
   - What makes it different from obvious baselines?

### Phase B: Multi-Source Literature Search
For EACH core claim, search using ALL available sources:

1. **Web Search** (via `WebSearch`):
   - Search arXiv, Google Scholar, Semantic Scholar
   - Use specific technical terms from the claim
   - Try at least 3 different query formulations per claim
   - Include year filters for 2024-2026

2. **Known paper databases**: Check against:
   - ICLR 2025/2026, NeurIPS 2025, ICML 2025/2026
   - Recent arXiv preprints (2025-2026)

3. **Read abstracts**: For each potentially overlapping paper, WebFetch its abstract and related work section

### Phase C: Cross-Model Verification
Call REVIEWER_MODEL via Codex MCP (`mcp__codex__codex`) with xhigh reasoning:
```
config: {"model_reasoning_effort": "xhigh"}
```
Prompt should include:
- The proposed method description
- All papers found in Phase B
- Ask: "Is this method novel? What is the closest prior work? What is the delta?"

### Phase D: Novelty Report
Output a structured report:

```markdown
## Novelty Check Report

### Proposed Method
[1-2 sentence description]

### Core Claims
1. [Claim 1] — Novelty: HIGH/MEDIUM/LOW — Closest: [paper]
2. [Claim 2] — Novelty: HIGH/MEDIUM/LOW — Closest: [paper]
...

### Closest Prior Work
One paper per subsection, full title in the heading — NEVER a table (paper tables are unreadable):

#### <Authors> (<Year>). <Full title>.
- venue: <venue> · <locator/URL>
- overlap: <what it already covers>
- key difference: <what stays novel>

### Overall Novelty Assessment
- Score: X/10
- Recommendation: PROCEED / PROCEED WITH CAUTION / ABANDON
- Key differentiator: [what makes this unique, if anything]
- Risk: [what a reviewer would cite as prior work]

### Suggested Positioning
[How to frame the contribution to maximize novelty perception]
```

### Important Rules
- Be BRUTALLY honest — false novelty claims waste months of research time
- "Applying X to Y" is NOT novel unless the application reveals surprising insights
- Check both the method AND the experimental setting for novelty
- If the method is not novel but the FINDING would be, say so explicitly
- Always check the most recent 6 months of arXiv — the field moves fast
- **Anti-hallucination for prior work (0.2.0).** Every paper named in the report must be VERIFIED before it appears: resolve its arXiv id via the arXiv API `id_list` (see `1_search/arxiv`), or its DOI/title via Semantic Scholar or Crossref (see `1_search/semantic-scholar`). An entry that cannot be resolved is tagged `[UNVERIFIED]` and its uncertainty surfaced — never dropped silently, and NEVER given a fabricated arXiv id, DOI, or title from memory. This is the same discipline the paper family's Explore/Seed pages assume when they bind this skill's QA output.
- **Long inputs go through a dossier file (0.2.0).** When the method description plus the Phase-B paper list outgrows a short note, write `NOVELTY_DOSSIER.md` inside the discovery-folder (method, core claims, candidate papers, the exact questions) and hand the reviewer the file path instead of pasting it inline.

## Recording the run

This layer's record is the discovery-folder itself: the verdict lands in the folder's terminal file and, when a question caused the run, in its `QA/<n>-<slug>.md` digest. The ARIS `.aris/traces/` machinery does not exist in this repo; do not hunt for `save_trace.sh`.
