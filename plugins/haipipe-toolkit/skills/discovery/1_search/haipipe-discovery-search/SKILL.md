---
name: haipipe-discovery-search
description: "Search type specialist for Discovery Topic Page Folders: find candidates, resolve canonical papers/sources, and materialize one numbered .sh Run plus same-stem Result per selected Subject. Builds the Topic source map from completed Results. Trigger: search sources, find papers, add paper run, read this paper, source base, /haipipe-discovery-search."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.2.0"
  last_updated: "2026-09-01"
  # version history: ./CHANGELOG.md
---

# /haipipe-discovery-search · Search type specialist

Owns Search-type Execute for a durable Discovery Topic, plus one-off inline
lookup. LOAD haipipe-discovery first for the Topic lifecycle and
ref/paper-run-contract.md for every durable source.

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

1. Read discovery.yaml and the root Topic Page. Sweep local Discovery Results
   before web calls when sources.local_first is true.
2. FIND candidates across the required channels. Wide mechanical sweeps may fan
   out read-only search workers; the specialist keeps relevance judgment,
   deduplication, Run allocation, and all writes.
3. RESOLVE each kept candidate to one canonical Subject: exact title, authors,
   venue/year, and DOI/arXiv/publisher URL. A secondary post or short link is a
   Trigger, not automatically the Subject.
4. ADMIT only candidates relevant enough to analyze. For each Subject call the
   Topic's add operation: allocate the next RUNNAME and create BOTH
   runs/<RUNNAME>.sh and results/<RUNNAME>/runtime.yaml (status: planned).
   One candidate paper = one Run. A Trigger mentioning N papers fans out to N
   Runs.
5. EXECUTE each pending ticket. Dispatch the appropriate read worker and write
   the paired Result Card, facts.md, one-entry authoritative <RUNNAME>.bib, and
   the completed runtime receipt. PDF and captured Trigger text are optional.
6. CHECK the Run/Result spine and rebuild the Topic Evidence Bib using the
   deterministic script named by the Discovery orchestrator.
7. Update the Topic Page's Source map: coverage boundary plus one readable
   Result link per source. Do not create a new monolithic notes.md.
8. Return Run counts by state, unresolved Trigger count, Topic Page path, and
   aggregate Bib path. The orchestrator owns topic status and Report.

VERIFIED requires independent canonical identity confirmation. A fabricated or
memory-composed Bib entry is the worst failure and cannot produce
status: complete. User-supplied metadata is not a user-supplied BibTeX entry;
formatting those fields into BibTeX is still composition.

## One-off mode

Return candidates inline in ref/source-format.md shape and write no files. If
the user elects to keep a candidate, hand it to the durable add route; the
worker call itself never becomes a Run.
