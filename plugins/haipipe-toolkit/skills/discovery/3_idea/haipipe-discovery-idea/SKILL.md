---
name: haipipe-discovery-idea
description: "Idea type specialist for the discovery layer: the ideation loop — generate + rank candidate claims (idea_generation -> ideas.md) and evaluate their novelty (novelty_check -> verdict.md). Dispatches idea-creator and novelty-check. Trigger: generate ideas, 找idea, novelty check, 查新, /haipipe-discovery-idea."
argument-hint: "[<discovery-folder> | \"<direction-or-idea>\"]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.0.0"
  last_updated: "2026-07-03"
  summary: "Type specialist owning Idea: generate -> ideas.md, novelty_check -> verdict.md."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-discovery-idea (type specialist)
===============================================

Owns the `Idea` type: the Execute stage of an Idea discovery-folder, or a one-off brainstorm. Idea covers BOTH halves of the ideation loop — invent, then evaluate what was invented. `role:` picks the terminal: idea_generation -> `ideas.md`, novelty_check -> `verdict.md`.

Workers: `idea-creator` (brainstorm + rank), `novelty-check` (is this idea already published? 查新).

Procedure (Execute of an Idea folder)
-------------------------------------

1. Read `discovery.yaml`: the `question`/direction, `role`, and grounding (`sources.from_source_folder` usually names the Search or Review folder this builds on — read its terminal first; ideas must be grounded, not blue-sky).
2. idea_generation: dispatch `idea-creator`; write `ideas.md` — ranked candidates, each with rationale, a novelty tag (NOVEL | PARTIAL | SEEN vs a named ref), and testability. Template: `haipipe-discovery/ref/discovery-yaml-schema.md`.
3. novelty_check: dispatch `novelty-check` against the specific candidate idea; write `verdict.md` (novel | partial | preempted | inconclusive, with the closest prior work as one-paper-one-subsection, never a table).
4. The loop composes: generate -> check the top candidates -> regenerate around what survives. Each pass stays inside its own folder and role.
5. Return to the caller: the terminal path, candidate count (or the novelty outcome), and the NEEDS-VERIFICATION count. discovery.yaml itself is the orchestrator's to write, not this skill's.

One-off calls (no folder): same generate/check flow, returned INLINE in the terminal's format — write no files.

This skill only executes; the folder lifecycle (Plan/Report) belongs to `/haipipe-discovery`.
