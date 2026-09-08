---
name: haipipe-discovery-review
description: "Review-route specialist for source-reading Discovery Pages: inspect one admitted Paper/Source Result at a time, extract reliable claims and limitations, and return a verified review packet. Trigger: read this paper, review this source, inspect a Result, source reading, /haipipe-discovery-review."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.6.0"
  last_updated: "2026-09-07"
  # version history: ./CHANGELOG.md
---

# /haipipe-discovery-review · per-Subject review specialist

Owns the `source-reading` route and the review leg of D1 `ACQUIRE`: inspect one
admitted canonical Subject, identify what the source actually establishes, and
return a bounded packet for the Page or `3_synthesize` family. The containing
`2_review/` directory is a review capability family, not a Block, Job, Task,
Run, or synthesis level. Use `../../haipipe-discovery/ref/bjtr-alignment.md`
when an older numbered description is ambiguous.

Source-level deep reading may use the read workers under `1_search/`, while
multi-source craft workers are dispatched by `3_synthesize`.

## Durable procedure

1. Read the Task manifest, Page question, admission rule, and the assigned
   Result/runtime. A source-reading Page may contain one or several explicitly
   admitted sources, but each source remains a separate Subject and Run.
2. Check identity, reading depth, locators, methods, claims, limitations,
   disagreement with the source's own framing, and the exact cite key. Do not
   infer a topic conclusion from one source.
3. Return a review packet or write the source-reading Page through the current
   shared Page phase. If a required source is missing, route to D1 `ACQUIRE`;
   do not allocate a Run from inside this skill.
4. Hand accepted packets to `haipipe-discovery-synthesize` when the Page
   promise requires combining multiple Results. The synthesis family owns
   topic-level organization and Page CONTENT.

## Review Output Contract

~~~text
1. RESULT FIRST. Every cited paper/source maps to exactly one completed Result
   Card; link that Card at first use.
2. FULL IDENTITY. The Result owns full title, authors, venue/status, year, and a
   DOI/arXiv/publisher locator. Prose tags may be short only when unambiguous.
3. EXACT CITE KEY. Every @Key equals the paired one-entry Result Bib key and
   therefore resolves in the derived Task Page Evidence Bib.
4. PLAIN FINDING. State one jargon-free finding and its relevant anchor;
   leave cross-paper conclusions to `3_synthesize`.
5. DISAGREEMENT SURVIVES. Conflicting Results are shown, not averaged away.
6. VERIFICATION GATE. NEEDS-VERIFICATION or unresolved Results cannot support a
   reported factual conclusion.
~~~

Use one source per subsection/card, never a wide citation table. This skill
does not create an aggregate Bib or a cross-paper synthesis record; those are
owned by Outline and `3_synthesize`.

## One-off mode

Return the review packet inline and write no files. Durable use requires a Task
Page Folder and a D1-owned numbered Paper Run.
