---
name: haipipe-discovery-idea
description: "Idea-route specialist for ideation and novelty-verdict Discovery Pages: generate and rank grounded ideas, or check novelty against completed per-paper Results. Idea generation is Page work; every prior-work paper used as evidence gets its own numbered Run. Trigger: generate ideas, 找idea, novelty check, 查新, /haipipe-discovery-idea."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.5.0"
  last_updated: "2026-09-04"
  # version history: ./CHANGELOG.md
---

# /haipipe-discovery-idea · Idea type specialist

Owns `03 CONTENT / WRITE` craft for both article forms in the grounded ideation loop:

~~~text
ideation        -> root Page + ideas.md
novelty-verdict -> root Page + verdict.md
~~~

Workers: idea-creator and novelty-check.

## Durable procedure

1. Read `discovery_type` from discovery.yaml (or normalize its legacy
   Idea/role pair), the Task Page, and grounding Task Pages/typed records/Results
   named by sources.from_topic. Ideas must be grounded, not blue-sky.
2. For `ideation`, dispatch idea-creator and write the root Page plus ranked
   candidates to ideas.md, each with rationale, novelty hypothesis,
   testability, and links to grounding Results. Generating an idea is Page workflow and MUST
   NOT create a fake Paper Run.
3. For `novelty-verdict`, route missing prior work to D1 ACQUIRE, then dispatch
   Search across the required channels. Resolve
   every closest-prior-work paper and create one numbered paired Run/Result per
   canonical Subject. Then write verdict.md as novel | partial | preempted |
   inconclusive, and synthesize the same judgment into the root Page.
4. Every novelty claim links to completed Result Cards and exact cite keys.
   Unresolved or unverified candidates remain caveats, not evidence.
5. Run the deterministic spine check and consume the Task Page Bib already
   built by D1 SYNTHESIZE under `outline/evidence/bibex/`; do not rebuild it.
6. Return Page path, optional typed-record path, candidate count or novelty outcome,
   complete/unresolved Run counts, and aggregate Bib path. The orchestrator owns
   topic status.

The loop may repeat: generate -> check top candidates -> regenerate around what
survives. New papers allocate new Runs; old Result history is never silently
overwritten.

## One-off mode

Return ideas or a novelty verdict inline and write no files. If the result is to
be kept, route it through a durable Task Page Folder; only evidence Subjects become
Paper Runs.
