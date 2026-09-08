---
name: gemini-search
description: >-
  Broad AI-assisted literature discovery for a Discovery Search route. Use
  when keyword search may miss aliases, neighboring subproblems, or naming
  variants. Gemini scouts candidates; the Discovery dispatcher verifies and
  admits canonical Subjects.
allowed-tools: Bash(*), Read, Grep, Glob, Skill, mcp__gemini-cli__*
metadata:
  argument_hint: "[search-query]"
  version: "0.1.0"
  last_updated: "2026-09-07"
  source: "ARIS skills/gemini-search @ 0472e53"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# Gemini Search · Discovery source adapter

This is the HAI Pipe adapter for the latest ARIS Gemini search skill. It is a
candidate scout, not a citation authority and not a Run writer. Load
`../haipipe-discovery-search/SKILL.md` for the durable Trigger -> Subject ->
Run/Result contract.

## When to use

Use Gemini when the query has terminology drift, several aliases, adjacent
subproblems, or a broad landscape that ordinary arXiv/Semantic Scholar
keyword queries may under-cover. It is optional: a missing Gemini MCP server
or CLI never blocks the required preprint and journal-index channels.

## Procedure

1. Parse the query and optional `max`, `year`, `venues`, `code-only`, and
   `model` arguments. Default to at most 15 candidates and a recent-year
   window unless the caller sets another bound.
2. Prefer `mcp__gemini-cli__ask-gemini`. Ask Gemini to decompose the topic
   into aliases, subproblems, neighboring tasks, surveys, top venues, and
   recent preprints. Request exact title, authors, year, venue, DOI, arXiv ID,
   code URL, and a one-sentence contribution for each candidate.
3. If the MCP tool is unavailable, try the authenticated `gemini` CLI with a
   120-second timeout. If both are unavailable, return an explicit
   `source-unavailable` note and let the caller continue with other channels.
4. Normalize each response to title, authors, year, venue, DOI, arXiv ID,
   URLs, summary, and source=`gemini`. Do not trust Gemini's identifiers or
   citation counts without independent lookup.
5. Hand the harvest to `haipipe-discovery-search`. The dispatcher performs
   exact-title/DOI/arXiv verification, cross-channel deduplication, relevance
   admission, and Run allocation. One admitted Subject receives one numbered
   `runs/<RUNNAME>.sh` plus same-stem `results/<RUNNAME>/`; this adapter never
   creates a Run, Result, Bib, or standalone notes ledger.

## Verification and coverage

Gemini expands recall; it does not establish evidence. Confirm a kept paper
through arXiv, Semantic Scholar, OpenAlex, Crossref, or a publisher page before
calling it a canonical Subject. Keep both preprint and journal-index coverage
declarations even when Gemini finds a published-looking result. Record Gemini
as a contributing source in the Run receipt, not as the authoritative Bib
source unless an independent resolver supplies the exact entry.

## Standalone mode

For a one-off lookup, return normalized candidates inline and write nothing. If
the user elects to keep a candidate, route it through a Discovery Task's
`add` operation so the normal Run/Result/Bib contract applies.

