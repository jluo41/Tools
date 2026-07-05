---
name: haipipe-discovery-search
description: "Search type specialist for the discovery layer: find AND read sources, write sources.md + notes.md. Dispatches arxiv / semantic-scholar / exa-search to find, alphaxiv / deepxiv / paper-analyzer to read. Trigger: search sources, find papers, source base, read this paper, /haipipe-discovery-search."
argument-hint: "[<discovery-folder> | \"<question>\"]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.0.0"
  last_updated: "2026-07-03"
  summary: "Type specialist owning Search: find + read sources -> sources.md + notes.md."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-discovery-search (type specialist)
=================================================

Owns the `Search` type: the Execute stage of a Search discovery-folder, or a one-off source hunt with no folder. Search = find + read, always together; the digested source set is a reusable, accumulating base.

Workers (pick by need; several per run is normal):

```
find   arxiv              preprint search + PDF download
       semantic-scholar   published venues, citation counts
       exa-search         broad web (blogs / news / docs)
read   alphaxiv           fast LLM summary of one paper
       deepxiv            progressive section reading
       paper-analyzer     deep structured note
```

Procedure (Execute of a Search folder)
--------------------------------------

1. Read `discovery.yaml`: the `question` and `sources` scope. If `local_first`, sweep existing `discoveries/` and project evidence BEFORE any web call.
2. FIND: dispatch the right find worker(s) — preprints -> arxiv, published venues/citations -> semantic-scholar, grey literature -> exa-search. A question spanning categories dispatches several; stop when the question is answerable, not at a source quota.
3. READ: for each kept source, extract findings through a read worker (alphaxiv for speed, deepxiv for sections, paper-analyzer for depth).
4. Write `sources.md` per `haipipe-discovery/ref/source-format.md`: one source = one subsection, full title in the heading, NEVER a table.
5. Write `notes.md`: per-source finding blocks keyed by S-id (template in the same source-format ref). `role: source_gather` centers on sources.md, `source_read` on notes.md; both files are normally written together.
6. VERIFIED means the exact title + authors + venue/id were confirmed via an independent lookup (semantic-scholar or arxiv by exact title); anything less is flagged NEEDS-VERIFICATION. Fabrication is the worst failure.
7. Return to the caller: the terminal paths, source count, and NEEDS-VERIFICATION count. discovery.yaml itself (status etc.) is the orchestrator's to write, not this skill's.

One-off calls (no folder): same FIND -> READ -> same output formats, returned INLINE — write no files, sweep local evidence first when a project is visible, and default to a handful of sources unless the caller names a number.

This skill only executes; the folder lifecycle (Plan/Report) belongs to `/haipipe-discovery`.
