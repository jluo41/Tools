---
name: haipipe-discovery-search
description: "Search type specialist for the discovery layer: find AND read sources, write sources.md + notes.md. Dispatches arxiv / semantic-scholar / exa-search to find, alphaxiv / deepxiv / paper-analyzer to read. Trigger: search sources, find papers, source base, read this paper, /haipipe-discovery-search."
argument-hint: "[<discovery-folder> | \"<question>\"]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.3.0"
  last_updated: "2026-07-08"
  summary: "Type specialist owning Search: find + read sources -> sources.md + notes.md. Channel diversity mandatory: preprint channel + journal-index channel every run (OpenAlex/Crossref when S2 rate-limits); top-venue pass in full-mode novelty; coverage declaration in the sources.md preamble."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-discovery-search (type specialist)
=================================================

Owns the `Search` type: the Execute stage of a Search discovery-folder, or a one-off source hunt with no folder. Search = find + read, always together; the digested source set is a reusable, accumulating base.

Workers (pick by need; several per run is normal):

```
find   arxiv              preprint search + PDF download (no key)
       semantic-scholar   published venues, citation counts. Uses
                          SEMANTIC_SCHOLAR_API_KEY (env.sh / env.ps1) when
                          non-empty -- keyed = higher rate limits, sweep S2
                          confidently; keyless = ~1 req/s, 429s hard, fall
                          through to OpenAlex/Crossref below
       OpenAlex/Crossref  journal-index APIs, direct curl -- free, no key,
                          venue-filterable; the reliable JOURNAL channel
                          (api.openalex.org/works?search=...  /
                           api.crossref.org/works?query=...); append
                          &mailto=$OPENALEX_MAILTO when set (polite pool)
       exa-search         broad web (blogs / news / docs); requires
                          EXA_API_KEY (env.sh / env.ps1) -- empty means the
                          channel is UNAVAILABLE: skip it and record that in
                          the coverage declaration, don't burn turns on it
read   alphaxiv           fast LLM summary of one paper
       deepxiv            progressive section reading
       paper-analyzer     deep structured note
```

**CHANNEL DIVERSITY IS MANDATORY (test-2-2222: an arXiv-only sweep systematically missed NHB/PNAS/Science-tier literature -- much of it has no preprint).** Every Search run fires BOTH water bodies: the preprint channel (arxiv) AND a journal-index channel (semantic-scholar, falling through to OpenAlex/Crossref on rate-limit). Knowledge-first lookups (confirming papers the model already knows) do not count as a journal sweep -- run at least one exploratory query per axis on the journal channel too. For a 查新/novelty question in FULL mode, add a TOP-VENUE PASS: the same queries filtered to the field's flagship venues (e.g. Nature Human Behaviour, PNAS, Science, Nature Medicine -- pick per field); in light mode record the skipped pass as a coverage caveat instead.

Procedure (Execute of a Search folder)
--------------------------------------

1. Read `discovery.yaml`: the `question` and `sources` scope. If `local_first`, sweep existing `discoveries/` and project evidence BEFORE any web call.
2. FIND: dispatch the right find worker(s) — preprints -> arxiv, published venues/citations -> semantic-scholar, grey literature -> exa-search. A question spanning categories dispatches several; stop when the question is answerable, not at a source quota. WIDE sweeps (2+ channels or 3+ queries/channel), when the running context has the Agent tool: fan out `haipipe-discovery-search-worker-agent` (Haiku, cheap) one per channel in parallel instead of running every channel inline; workers return raw candidate entries + coverage notes, and the dispatcher keeps relevance curation, cross-channel dedup, and ALL file writes.
3. READ: for each kept source, extract findings through a read worker (alphaxiv for speed, deepxiv for sections, paper-analyzer for depth).
4. Write `sources.md` per `haipipe-discovery/ref/source-format.md`: one source = one subsection, full title in the heading, NEVER a table. The preamble carries the COVERAGE DECLARATION (channels searched AND channels not searched -- see source-format.md); a silent cap reads as "covered everything" when it didn't.
5. Write `notes.md`: per-source finding blocks keyed by S-id (template in the same source-format ref). `role: source_gather` centers on sources.md, `source_read` on notes.md; both files are normally written together.
6. VERIFIED means the exact title + authors + venue/id were confirmed via an independent lookup (semantic-scholar or arxiv by exact title); anything less is flagged NEEDS-VERIFICATION. Fabrication is the worst failure.
7. Return to the caller: the terminal paths, source count, and NEEDS-VERIFICATION count. discovery.yaml itself (status etc.) is the orchestrator's to write, not this skill's.

One-off calls (no folder): same FIND -> READ -> same output formats, returned INLINE — write no files, sweep local evidence first when a project is visible, and default to a handful of sources unless the caller names a number.

This skill only executes; the folder lifecycle (Plan/Report) belongs to `/haipipe-discovery`.
