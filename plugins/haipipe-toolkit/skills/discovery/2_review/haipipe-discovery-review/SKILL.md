---
name: haipipe-discovery-review
description: "Review type specialist for Discovery Topic Page Folders: synthesize completed Paper/Source Results into a verdict or landscape. Missing evidence is added as one numbered Paper Run per canonical Subject. Trigger: judge claim, prior art, counterevidence, landscape, lit review for a discovery, /haipipe-discovery-review."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.2.0"
  last_updated: "2026-09-01"
  # version history: ./CHANGELOG.md
---

# /haipipe-discovery-review · Review type specialist

Owns Review-type Execute. role selects judge (prior_art_check,
counterevidence -> verdict.md) or synthesize (landscape_review,
benchmark_landscape -> landscape.md).

Workers: research-lit (default multi-source), comm-lit-review
(communications), and academic-researcher (cross-discipline).

## Durable procedure

1. Read discovery.yaml, the Topic Page, and all completed
   results/*/<RUNNAME>.md plus facts.md. If sources.from_topic names another
   Discovery Topic, read its terminal and completed Results; never depend on
   its legacy notes.md.
2. Test evidence sufficiency. When new papers are required, dispatch Search to
   resolve candidates and add one paired Run/Result per canonical Subject.
   Inline worker calls and search queries are not Runs.
3. Dispatch the review worker with the output contract below. Judge roles write
   verdict.md; synthesize roles write landscape.md.
4. Every evidence statement links to a Result Card and uses that Result's cite
   key. Counterevidence is retained, and scope never exceeds the underlying
   Results.
5. Run the deterministic spine check and Bib aggregation before returning.
6. Return the terminal path, outcome (or cluster/gap counts), complete and
   unresolved Run counts, and aggregate Bib path. The orchestrator owns topic
   status and Report.

## Review Output Contract

~~~text
1. RESULT FIRST. Every cited paper/source maps to exactly one completed Result
   Card; link that Card at first use.
2. FULL IDENTITY. The Result owns full title, authors, venue/status, year, and a
   DOI/arXiv/publisher locator. Prose tags may be short only when unambiguous.
3. EXACT CITE KEY. Every @Key equals the paired one-entry Result Bib key and
   therefore resolves in the derived Topic Evidence Bib.
4. PLAIN FINDING. State one jargon-free finding and its relevant anchor before
   drawing a Topic-level conclusion.
5. DISAGREEMENT SURVIVES. Conflicting Results are shown, not averaged away.
6. VERIFICATION GATE. NEEDS-VERIFICATION or unresolved Results cannot support a
   reported factual conclusion.
~~~

Use one source per subsection/card, never a wide citation table. For a
systematic review requiring a deeper protocol, escalate to the deep-research
literature pipeline while preserving this Run/Result storage contract.

## One-off mode

Return the verdict/landscape inline and write no files. Durable use requires a
Topic Folder and numbered Paper Runs.
