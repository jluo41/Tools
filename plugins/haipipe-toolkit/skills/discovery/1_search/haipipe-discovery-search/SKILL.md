---
name: haipipe-discovery-search
description: "Search-route specialist for source-map Discovery Pages: find candidates, resolve canonical papers/sources, and hand admitted Subjects to the D1 Run contract. Trigger: search sources, find papers, add paper run, source map, /haipipe-discovery-search."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.7.0"
  last_updated: "2026-09-08"
  # version history: ./CHANGELOG.md
---

# /haipipe-discovery-search · Search type specialist

Owns D1 `ACQUIRE` search and canonical-identity craft for every Discovery type
and contributes source-map craft during `03 CONTENT / WRITE`, plus one-off
inline lookup. Per-Subject reading belongs to `2_review`; cross-Result article
composition belongs to `3_synthesize`.
The containing `1_search/` directory is a capability family, not a Block, Job,
Task, or Run. Use `../../haipipe-discovery/ref/bjtr-alignment.md` when an older
numbered description is ambiguous.
LOAD haipipe-discovery first for the Topic workflow and read
`../../haipipe-discovery/ref/page-types.md` for the Page promise and
`../../haipipe-discovery/ref/paper-run-contract.md` for every durable source.
For external provider selection and the normalized candidate packet, read
`../../haipipe-discovery/ref/external-capability-registry.md`.

## Workers

~~~text
find   arxiv              preprints + PDF when available
       semantic-scholar   published venues and citation graph
       Crossref/PubMed    DOI, journal, and biomedical metadata fallback
       medRxiv            clinical/biomedical preprints when relevant
       exa-search         broad web/grey literature when EXA_API_KEY exists
       openalex           structured cross-discipline metadata, OA, and citation graph
       gemini-search      optional alias/subproblem expansion and broad recall
read   alphaxiv           fast paper summary
       deepxiv            progressive section reading
       paper-analyzer     deep structured analysis
~~~

Use SEMANTIC_SCHOLAR_API_KEY, EXA_API_KEY, and OPENALEX_API_KEY only when
present. For OpenAlex's polite pool, use OPENALEX_EMAIL; the helper has no
OPENALEX_MAILTO fallback. Gemini credentials are used only when present.
Never expose credentials in a ticket or runtime receipt. Gemini and OpenAlex
are optional scouts; they do not replace the required preprint and
journal-index coverage or the independent identity check.

## Channel law

Every durable literature sweep covers BOTH a preprint channel and a
journal-index channel. Knowledge-first title confirmation does not count as a
journal sweep. For a clinical or biomedical scope, include medRxiv alongside
arXiv when relevant and use PubMed with Crossref as the biomedical/DOI
fallback; record each channel as searched or not searched. Full novelty work
adds a field-appropriate top-venue pass; light mode records the omitted pass in
the Topic coverage declaration.

## External provider routing

Use the `academic-paper-search` decision tree as a reference when the normal
channel set needs an additional provider. Prefer the narrowest authoritative
channel for the identity in hand: arXiv for an arXiv identifier, Crossref or
PubMed for DOI/journal metadata, OpenAlex for cross-source discovery and OA
links, and Unpaywall only for lawful full-text availability. NBER/SSRN are
optional field-specific channels, not replacements for the required preprint
and journal-index coverage.

Treat ARIS `research-lit` and AER `aer-literature` as read-only search craft:
they may propose aliases, citation chains, or an antecedents map, but the HAI
specialist still deduplicates candidates, verifies identity, records channel
coverage, and decides admission. Normalize every external hit to the registry
candidate packet before any Run is opened.

## Durable procedure

1. Read `discovery_type` from discovery.yaml (or normalize a legacy
   Search/role pair) and the root Task Page. Sweep local Discovery Results
   before web calls when sources.local_first is true.
2. FIND candidates across the required channels. Wide mechanical sweeps may fan
   out read-only search workers; the specialist keeps relevance judgment,
   deduplication, Run allocation, and all writes. For clinical/biomedical
   scope, add the relevant medRxiv and PubMed passes and use Crossref for DOI
   and journal metadata fallback. When requested or configured, add the
   optional `gemini-search` alias/subproblem sweep and `openalex`
   metadata/citation sweep. If an optional adapter is unavailable, record the
   coverage gap and continue; do not turn an optional failure into a blocked
   Task. If an external provider-routing procedure is used, record its name
   in the runtime receipt as worker detail; it does not create a new Run.
3. RESOLVE each kept candidate to one canonical Subject: exact title, authors,
   venue/year, and DOI/arXiv/PubMed/publisher URL. Use Crossref or PubMed as
   identity/index fallbacks, not as a substitute for the preprint/journal
   coverage law. A secondary post or short link is a Trigger, not automatically
   the Subject.
4. ADMIT only candidates relevant enough to analyze. For each Subject call the
   Task Page's add operation: allocate the next RUNNAME and create BOTH
   runs/<RUNNAME>.sh and results/<RUNNAME>/runtime.yaml (`family: discovery`,
   matching paper/source analysis operation, `status: planned`).
   One candidate paper = one Run. A Trigger mentioning N papers fans out to N
   Runs.
5. EXECUTE each pending ticket. Dispatch the appropriate read worker and write
   the paired Result Card, facts.md, one-entry authoritative <RUNNAME>.bib, and
   the completed runtime receipt. For a paper Subject, the new Result MUST also
   carry `result_contract: paper-source-v2` plus the source-access pair required
   by the Paper Run contract; the compatibility checker does not waive this
   creation-time requirement. PDF and captured Trigger text are optional.
6. CHECK the Run/Result spine. Hand completed Results to D1 SYNTHESIZE; the
   Outline plugin's citation contract owns the deterministic Task Page Bib
   aggregation under `outline/evidence/bibex/`.
7. During `03 CONTENT / WRITE` for source-map/source-reading, update the root Page:
   source-map emphasizes coverage and readable source units; source-reading
   synthesizes what selected sources say. Both keep Result links and never
   create a monolithic notes.md.
8. Return Discovery type, Run counts by state, unresolved Trigger count, Task Page path, and
   aggregate Bib path. The orchestrator owns Task Page status and CLOSE.

VERIFIED requires independent canonical identity confirmation. A fabricated or
memory-composed Bib entry is the worst failure and cannot produce
status: complete. User-supplied metadata is not a user-supplied BibTeX entry;
formatting those fields into BibTeX is still composition.

The external adapters are deliberately below the Discovery authority line:
Gemini broadens recall and OpenAlex supplies structured metadata, but neither
is itself a canonical Subject, a durable Run, a Result Card, or a Bib source.
The dispatcher records their contribution in coverage/runtime metadata and
uses an independent resolver before creating or completing a Run.

## One-off mode

Return candidates inline in `../../haipipe-discovery/ref/source-format.md`
shape and write no files. If
the user elects to keep a candidate, hand it to the durable add route; the
worker call itself never becomes a Run.
