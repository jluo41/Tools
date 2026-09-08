---
name: haipipe-discovery-synthesize
description: >-
  Synthesis-route specialist for Discovery Task Pages. Integrate completed
  per-source Review Results into one coherent topic article, preserving
  agreements, disagreements, gaps, limits, and exact Result/Bib lineage.
  Trigger: synthesize papers, combine literature, write a topic summary,
  build a landscape, connect findings, /haipipe-discovery-synthesize.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.1.0"
  last_updated: "2026-09-07"
  # version history: ./CHANGELOG.md
---

# /haipipe-discovery-synthesize · cross-Result synthesis

This is the live third Discovery capability family. It owns cross-Result
integration during D1 `SYNTHESIZE` and the shared Page `03 CONTENT / WRITE`
handoff. The containing `3_synthesize/` directory is a capability family, not
a Block, Job, Task, Run, or extra Page level.

The distinction is deliberate:

```text
1_search      locate, resolve, and admit candidate Subjects
2_review      inspect one completed Subject/Result and extract reliable claims
3_synthesize combine several accepted Results into the promised Task Page
```

Writing is the Page action. Synthesis is the reasoning contract: explain how
papers relate, where they converge, where they disagree, what remains absent,
and what the bounded evidence can honestly support.

## Authority and boundary

Load `haipipe-discovery` and
`workflow-phases/haipipe-discovery-inquiry/ref/workflow-table.md` first. Then
load the shared Page workflow and Outline citation authority when making Page
changes. The BJTR retrofit is
`../../haipipe-discovery/ref/bjtr-alignment.md`.

This skill may read completed Results, Review packets, Task QA, and the frozen
`discovery.yaml`. It may write only the Page artifacts owned by the current
Page phase and optional typed Task-side records declared by the Page type. It
does not allocate or execute a Discovery Run, create a shell ticket, or write
a second Bib authority.

## Route by article promise

The Synthesize route owns these canonical `discovery_type` values:

```text
topic-summary
prior-art-verdict
counterevidence-review
landscape-review
benchmark-landscape
```

`source-map` belongs to `1_search`. `source-reading` belongs to `2_review`.
If a synthesis lacks a required paper/source, return the request to D1
`ACQUIRE`; do not fill the gap with an unverified citation or an umbrella Run.

## Durable procedure

1. Read the complete BJTR Task address, manifest, Page question, boundary,
   `discovery_type`, and the current Page workflow receipt.
2. Inventory every accepted Result Card and its same-stem Bib/runtime. Use the
   full Result identity and exact cite key at first use. Treat upstream
   cross-Task Results as read-only context; a load-bearing paper must be
   re-admitted by D1 `ACQUIRE` before entering the current Task aggregate.
3. Build a synthesis map before drafting: claim or theme, supporting Results,
   opposing Results, evidence depth, unresolved gap, and the limit on the
   conclusion. Preserve disagreement instead of averaging it away.
4. Dispatch the appropriate craft worker when useful (for example
   `research-lit`, `comm-lit-review`, or `academic-researcher`), but keep the
   worker's output as a draft packet. The Page phase remains the only writer
   of Page Content, Aims, and CHECK receipts.
5. Organize the root Page by the reader's answer and themes, not by one paper
   per paragraph. A typed `summary.md`, `verdict.md`, or `landscape.md` is an
   optional compact Task-side receipt; it never replaces the root Page.
6. Build the derived aggregate Bib through the Outline citation authority.
   Never handwrite a competing `references.bib` or copy an entire Result into
   a flat notes file.
7. Return to D1 `ACQUIRE` when a factual claim has no adequate Result, a
   citation is unverified, or the evidence population changed. Only after the
   shared Page `04 CHECK` passes may D1 `CLOSE` reconcile the Task Face.

## Synthesis output contract

The completed synthesis must expose:

```text
root Page                    the human-facing article
question and boundary       what population and source rule were used
theme/claim map              each conclusion -> Result Card + exact cite key
relationship map             convergence, disagreement, extension, or gap
typed record                 summary/verdict/landscape when declared
limits and next move         what the evidence does not establish
derived Bib                  Outline-owned union of complete verified Results
```

Every factual statement is bounded by the Results' reading depth and locator
state. A synthesis can be inconclusive without being incomplete; it is
blocked when required evidence, citation verification, or Page gates remain
open.

## Run and handoff laws

- `3_synthesize` never creates `runs/`, `results/`, or a local `rNN`.
- D1 `ACQUIRE` remains the only Discovery Run commissioner: one admitted
  canonical Subject per Run and one exact same-stem Result.
- A Page division may use many Results and one Result may support many
  divisions. This many-to-many evidence relation does not create a new Run.
- New semantic direction work is a separate sibling `haipipe-ideation` route;
  it receives Result/Card/Bib pointers after synthesis and is not a Discovery
  capability family.

## One-off mode

For an inline request, return a clearly labeled synthesis packet without
writing files. Durable synthesis requires a BJTR Task Page, accepted Results,
and the shared Page workflow.

