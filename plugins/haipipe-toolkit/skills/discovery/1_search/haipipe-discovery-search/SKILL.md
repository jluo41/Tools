---
name: haipipe-discovery-search
description: "Search-route specialist for source-map and source-reading Discovery Pages: find candidates, resolve canonical papers/sources, and materialize one numbered .sh Run plus same-stem Result per admitted Subject. Trigger: search sources, find papers, add paper run, read this paper, source map, source reading, /haipipe-discovery-search."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.4.1"
  last_updated: "2026-09-03"
  # version history: ./CHANGELOG.md
---

# /haipipe-discovery-search · Search type specialist

Owns ACQUIRE craft for every Discovery type and contributes source-map /
source-reading article craft during SYNTHESIZE, plus one-off inline lookup.
LOAD haipipe-discovery first for the Topic workflow and
read `ref/page-types.md` for the Page promise and
`ref/paper-run-contract.md` for every durable source.

## Workers

~~~text
find   arxiv              preprints + PDF when available
       semantic-scholar   published venues and citation graph
       OpenAlex/Crossref  journal index and authoritative metadata fallback
       exa-search         broad web/grey literature when EXA_API_KEY exists
read   alphaxiv           fast paper summary
       deepxiv            progressive section reading
       paper-analyzer     deep structured analysis
~~~

Use SEMANTIC_SCHOLAR_API_KEY, EXA_API_KEY, and OPENALEX_MAILTO only when
present. Never expose them in a ticket or runtime receipt.

## Channel law

Every durable literature sweep covers BOTH a preprint channel and a
journal-index channel. Knowledge-first title confirmation does not count as a
journal sweep. Full novelty work adds a field-appropriate top-venue pass; light
mode records the omitted pass in the Topic coverage declaration.

## Durable procedure

1. Read `discovery_type` from discovery.yaml (or normalize a legacy
   Search/role pair) and the root Task Page. Sweep local Discovery Results
   before web calls when sources.local_first is true.
2. FIND candidates across the required channels. Wide mechanical sweeps may fan
   out read-only search workers; the specialist keeps relevance judgment,
   deduplication, Run allocation, and all writes.
3. RESOLVE each kept candidate to one canonical Subject: exact title, authors,
   venue/year, and DOI/arXiv/publisher URL. A secondary post or short link is a
   Trigger, not automatically the Subject.
4. ADMIT only candidates relevant enough to analyze. For each Subject call the
   Task Page's add operation: allocate the next RUNNAME and create BOTH
   runs/<RUNNAME>.sh and results/<RUNNAME>/runtime.yaml (`family: discovery`,
   matching paper/source analysis operation, `status: planned`).
   One candidate paper = one Run. A Trigger mentioning N papers fans out to N
   Runs.
5. EXECUTE each pending ticket. Dispatch the appropriate read worker and write
   the paired Result Card, facts.md, one-entry authoritative <RUNNAME>.bib, and
   the completed runtime receipt. PDF and captured Trigger text are optional.
6. CHECK the Run/Result spine. Hand completed Results to SYNTHESIZE; the
   Outline plugin's citation contract owns the deterministic Task Page Bib
   aggregation under `outline/evidence/bibex/`.
7. During SYNTHESIZE for source-map/source-reading, update the root Page:
   source-map emphasizes coverage and readable source units; source-reading
   synthesizes what selected sources say. Both keep Result links and never
   create a monolithic notes.md.
8. Return Discovery type, Run counts by state, unresolved Trigger count, Task Page path, and
   aggregate Bib path. The orchestrator owns Task Page status and CLOSE.

VERIFIED requires independent canonical identity confirmation. A fabricated or
memory-composed Bib entry is the worst failure and cannot produce
status: complete. User-supplied metadata is not a user-supplied BibTeX entry;
formatting those fields into BibTeX is still composition.

## One-off mode

Return candidates inline in ref/source-format.md shape and write no files. If
the user elects to keep a candidate, hand it to the durable add route; the
worker call itself never becomes a Run.
