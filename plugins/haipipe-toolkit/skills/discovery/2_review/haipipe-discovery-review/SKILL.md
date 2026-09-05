---
name: haipipe-discovery-review
description: "Review-route specialist for topic-summary, verdict, and landscape Discovery Pages: synthesize completed Paper/Source Results into the root article and optional typed record. Missing evidence becomes one numbered Run per canonical Subject. Trigger: topic summary, judge claim, prior art, counterevidence, landscape, lit review for a discovery, /haipipe-discovery-review."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.5.0"
  last_updated: "2026-09-04"
  # version history: ./CHANGELOG.md
---

# /haipipe-discovery-review · Review type specialist

Owns `03 CONTENT / WRITE` craft for `topic-summary`, `prior-art-verdict`,
`counterevidence-review`, `landscape-review`, and `benchmark-landscape`.
Every type writes the root Page; summary/verdict/landscape files are optional
typed Task-side records selected by
`../../haipipe-discovery/ref/page-types.md`.

Workers: research-lit (default multi-source), comm-lit-review
(communications), and academic-researcher (cross-discipline).

## Durable procedure

1. Read `discovery_type` from discovery.yaml (or normalize its legacy
   Review/role pair), the Task Page, and all completed
   results/*/<RUNNAME>.md plus facts.md. If sources.from_topic names another
   Discovery Task Page, read its root Page, typed record, and completed Results; never depend on
   its legacy notes.md.
2. Test evidence sufficiency. When new papers are required, route to D1 ACQUIRE;
   Search resolves candidates and adds one paired Run/Result per Subject.
   Inline worker calls and search queries are not Runs.
3. Dispatch the review worker with the output contract below. Write the root
   Page first. Write `summary.md`, `verdict.md`, or `landscape.md` only when the
   selected type declares that typed record.
4. Every evidence statement links to a Result Card and uses that Result's cite
   key. Counterevidence is retained, and scope never exceeds the underlying
   Results.
5. Run the deterministic spine check and consume the D1 SYNTHESIZE aggregate
   at `outline/evidence/bibex/`; do not create a second rebuild authority.
6. Return the Page path, optional typed-record path, outcome (or cluster/gap counts), complete and
   unresolved Run counts, and aggregate Bib path. The orchestrator owns topic
   status and CLOSE.

## Review Output Contract

~~~text
1. RESULT FIRST. Every cited paper/source maps to exactly one completed Result
   Card; link that Card at first use.
2. FULL IDENTITY. The Result owns full title, authors, venue/status, year, and a
   DOI/arXiv/publisher locator. Prose tags may be short only when unambiguous.
3. EXACT CITE KEY. Every @Key equals the paired one-entry Result Bib key and
   therefore resolves in the derived Task Page Evidence Bib.
4. PLAIN FINDING. State one jargon-free finding and its relevant anchor before
   drawing a Topic-level conclusion.
5. DISAGREEMENT SURVIVES. Conflicting Results are shown, not averaged away.
6. VERIFICATION GATE. NEEDS-VERIFICATION or unresolved Results cannot support a
   reported factual conclusion.
~~~

Use one source per subsection/card, never a wide citation table. For a
systematic review requiring a deeper protocol, escalate to the deep-research
literature pipeline while preserving this Run/Result storage contract.

For `topic-summary`, organize the Page by findings/themes rather than by paper.
It is a bounded synthesis Page, not a weaker landscape and not one giant Paper
Run.

## One-off mode

Return the verdict/landscape inline and write no files. Durable use requires a
Task Page Folder and numbered Paper Runs.
