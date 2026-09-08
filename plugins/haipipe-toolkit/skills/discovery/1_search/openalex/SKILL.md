---
name: openalex
description: >-
  Structured OpenAlex literature search for Discovery acquisition. Use when
  open citation data, affiliations, funding, open-access status, or broad
  cross-discipline metadata are useful alongside arXiv and Semantic Scholar.
  OpenAlex supplies metadata; Discovery Results remain the evidence authority.
allowed-tools: Bash(*), Read, Grep, Glob, Skill
metadata:
  argument_hint: "[search-query]"
  version: "0.1.0"
  last_updated: "2026-09-07"
  source: "ARIS skills/openalex @ 0472e53"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# OpenAlex · Discovery source adapter

This adapter brings the latest ARIS OpenAlex worker into HAI Pipe without
importing its standalone output conventions. Load
`../haipipe-discovery-search/SKILL.md` for the durable Search route and
`../../haipipe-discovery/ref/paper-run-contract.md` for Result/Bib law.

## Role

OpenAlex is useful for a comprehensive, open citation graph and metadata that
may be absent from CS-focused indexes: institutions, topics, funding, work
type, citation count, and open-access status. It is a journal/index channel
and a cross-reference source, not proof that a paper was read.

## Resolve the fetcher

Use the repository's pinned ARIS helper first, then a project-local helper:

```bash
DISCOVERY_REPO=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
OPENALEX_FETCHER=""
for candidate in \
  "$DISCOVERY_REPO/Tools/references/aris/tools/openalex_fetch.py" \
  "$DISCOVERY_REPO/references/aris/tools/openalex_fetch.py" \
  "$DISCOVERY_REPO/.aris/tools/openalex_fetch.py" \
  "$DISCOVERY_REPO/tools/openalex_fetch.py"; do
  if [ -f "$candidate" ]; then
    OPENALEX_FETCHER="$candidate"
    break
  fi
done
[ -n "$OPENALEX_FETCHER" ] || {
  echo "openalex_fetch.py unavailable; skip OpenAlex and record the coverage gap" >&2
  exit 0
}
```

The pinned helper makes one request with `per_page=min(--max, 200)`; it does
not paginate or retry/back off. The CLI accepts `--max` values above 200, but a
single call still returns at most 200 rows. Keep `--max` at or below 200 for a
bounded call, or run explicit follow-up queries for a larger sweep and record
any truncation. `OPENALEX_API_KEY` is sent as the API parameter when configured;
`OPENALEX_EMAIL` alone controls the polite-pool `mailto` User-Agent (there is
no `OPENALEX_MAILTO` fallback). Never place credentials in a Run ticket or
receipt.

## Procedure

1. Parse `max`, `year`, `type`, `open-access`, `min-citations`, and `sort`.
2. Search with `python3 "$OPENALEX_FETCHER" search "QUERY" --max N`, adding
   only requested filters. For one known work, use `work` with its DOI or
   OpenAlex ID.
3. Normalize title, authors, publication year, venue, DOI, OpenAlex ID,
   arXiv ID when present, citation count, work type, topics, keywords, OA
   status, and OA URL. Mark `source=openalex`.
4. Cross-reference DOI, arXiv ID, or normalized title with Semantic Scholar,
   Crossref, arXiv, or the publisher before admission. Prefer the published
   venue metadata when the same work appears in multiple channels, while
   retaining OpenAlex affiliations/funding as supplemental fields.
5. Return the candidate harvest to `haipipe-discovery-search`. The dispatcher
   decides relevance and writes one Run/Result/Bib per admitted Subject. Do
   not format OpenAlex metadata into a BibTeX entry and do not write a Result
   from an OpenAlex row alone.

## Failure and standalone behavior

If the helper, requests dependency, or API is unavailable, report
`source-unavailable` and continue with the required channels; do not invent
metadata. A one-off call returns normalized rows inline and writes no files.
Durable retention always goes through a Discovery Task `add` operation.
