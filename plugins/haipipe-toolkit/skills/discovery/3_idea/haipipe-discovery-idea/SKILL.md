---
name: haipipe-discovery-idea
description: "Idea type specialist for Discovery Topic Page Folders: generate and rank grounded ideas, or check novelty against completed per-paper Results. Idea generation is topic-level Page work; every prior-work paper used as evidence gets its own numbered Run. Trigger: generate ideas, 找idea, novelty check, 查新, /haipipe-discovery-idea."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.2.0"
  last_updated: "2026-09-01"
  # version history: ./CHANGELOG.md
---

# /haipipe-discovery-idea · Idea type specialist

Owns both halves of the grounded ideation loop:

~~~text
idea_generation -> ideas.md
novelty_check    -> verdict.md
~~~

Workers: idea-creator and novelty-check.

## Durable procedure

1. Read discovery.yaml, the Topic Page, and grounding Topic terminals/Results
   named by sources.from_topic. Ideas must be grounded, not blue-sky.
2. For idea_generation, dispatch idea-creator and write ranked candidates to
   ideas.md, each with rationale, novelty hypothesis, testability, and links to
   grounding Results. Generating an idea is topic-level Page workflow and MUST
   NOT create a fake Paper Run.
3. For novelty_check, dispatch Search across the required channels. Resolve
   every closest-prior-work paper and create one numbered paired Run/Result per
   canonical Subject. Then write verdict.md as novel | partial | preempted |
   inconclusive.
4. Every novelty claim links to completed Result Cards and exact cite keys.
   Unresolved or unverified candidates remain caveats, not evidence.
5. Run the deterministic spine check and rebuild the Topic Evidence Bib before
   Report.
6. Return terminal path, candidate count or novelty outcome,
   complete/unresolved Run counts, and aggregate Bib path. The orchestrator owns
   topic status.

The loop may repeat: generate -> check top candidates -> regenerate around what
survives. New papers allocate new Runs; old Result history is never silently
overwritten.

## One-off mode

Return ideas or a novelty verdict inline and write no files. If the result is to
be kept, route it through a durable Topic Folder; only evidence Subjects become
Paper Runs.
