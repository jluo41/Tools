---
name: haipipe-application-probe
description: "PROBE phase worker (internal). Called by application stage skills after DRAFT to collect what the draft needs but does not have -- evidence for claims, context for the seed, materialized outputs for displays. The ONLY door from application stages to /haipipe-probe (the project-side evidence gateway; probe calls discovery and task during its own Gather, deposits to insight). BOOKKEEP -> DISPATCH -> TRANSLATE, no evidence work of its own. Fully automatic, human review in CHECK only. Users invoke stage skills (seed, claims, ...), not this skill directly."
argument-hint: "[from-buffer <intervention-root> [PPNN] | stage <stage-name>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Agent
metadata:
  version: "1.0.0"
  last_updated: "2026-07-06"
  summary: "NEW worker mirroring haipipe-paper-probe's BOOKKEEP/DISPATCH/TRANSLATE contract, minus the tex doc-workers (citation/values/display tracks are venue-scaled hooks here, not sub-skills). Folderless probe: per-stage _PROBE/PPNN cards, gateway dispatch, enum supported|refuted|inconclusive."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-application-probe (internal phase worker)
=========================================================

PROBE phase worker. Called by stage skills (seed, claims, pitch, narrative, display, section-edit) after DRAFT to collect what the draft needs but does not have. Materials can be internal (values from the project's own task results, display units rendered by task-folders) or external (literature, benchmarks, field norms). The stage defines WHAT needs collecting. This skill defines HOW to get it.

The downstream lifecycles are NESTED under probe:

```
/haipipe-probe       evidence gateway (explore+gather), mode: light|full
                     light (DEFAULT): explore what is known + gather what is missing
                     full: + judge the claim (G1/G2/G3 via haipipe-probe-review)
        │
        ├── during its Gather, probe calls:
        │     /haipipe-discovery   external evidence: search+read, judge/synthesize, idea
        │     /haipipe-task        task domains: data, display, eval, stata, ... (probe picks per need)
        │
        └── at Deposit, probe files:
              /haipipe-insight     DIKW knowledge base; settled evidence is reusable
                                   across papers AND applications instead of re-collected
```

**Not user-facing.** Users invoke stage skills; each stage's PROBE phase calls this worker. `/haipipe-application probe run [PPNN]` reaches it via the router's `from-buffer` dispatch.

## What PROBE means

PROBE = collect what the draft needs but does not have:

```
Evidence gateway (project-side lifecycles):
  /haipipe-probe          sweeps insights/discoveries/tasks, dispatches
                          /haipipe-discovery (lit) and /haipipe-task (runs/data)
                          for what is missing; full mode adds claim judgment

Venue-scaled document tracks (hooks inside this worker, not sub-skills):
  values     numbers quoted in a report/dashboard artifact traced to task results
  citations  sources quoted in a report artifact (sectioned venues only)
  displays   content elements routed to /haipipe-task-for-display
Simple venues (sms/push/reminder) have no document tracks -- their PROBE phase
is claims-evidence only.
```

All routes are fully automatic dispatch. The worker collects aggressively, flags uncertain items, and moves on. Human verification happens in CHECK, not here.

## Per-stage dispatch

| Stage | probe → gateway | Notes |
|---|---|---|
| seed | 🔎 mode: light (→ discovery) | landscape / prior interventions / benchmarks to sharpen the seed; takeaways land in the plan card |
| claims | 🏋️ mode: full (→ task + discovery) | the core evidence stage: one plan per GAP claim; verdicts backfill the ledger |
| pitch | light, rare | anchor evidence for the theory of change if the ledger lacks it |
| narrative | -- | maps existing claims to beats; new gaps route back to claims |
| display | via task | element generation routed to /haipipe-task-for-display; jobs stay display-side |
| section-edit | light + document tracks | sectioned venues: values/citations traced per section |

**Probe dispatch rules (both apply to every dispatch):**

1. **Mode: light by default.** A light probe stops at Read and returns evidence to the caller -- right for context questions. Request `mode: full` only when the intervention needs a COMMITTED verdict that backfills a claim slot (the claims stage's normal case). Never start heavy for a question that only needs orientation.

2. **Reuse-before-create -- decided by the GATEWAY AGENT, not this worker.** The gateway's SWEEP scans the project's evidence base (insights/discoveries/tasks) in clean context and picks the shape: REUSED (existing artifact covers it, pure read) / ENRICHED (same-topic deltas into an existing discovery) / FRESH (new discovery/task work). No shape creates a probe folder (folderless probe): a full-mode verdict's home is the PPNN card's `## Verdict`, landed at TRANSLATE.

## From-buffer entry (the ONLY path that dispatches the umbrella's probe plans)

`Skill("haipipe-application-probe", args="from-buffer <intervention_root> [PPNN]")` -- invoked by `/haipipe-application probe run` or by a stage's own PROBE phase. The umbrella NEVER calls `/haipipe-probe` directly; this worker is the single dispatch point.

This worker does exactly three things -- BOOKKEEP, DISPATCH, TRANSLATE -- and NO evidence work of its own:

0. **RE-INVOKE PER RUN.** Every stage's PROBE phase begins by invoking THIS skill fresh via the Skill tool -- even when its text is already in context from an earlier stage of the same session. Contracts version fast; running from a stale in-context copy executes yesterday's rules.
1. **BOOKKEEP.** Read the index (`<intervention_root>/1-probe-plans/README.md`), resolve each planned item to its per-stage `_PROBE/PPNN_*.md` card (or the one named PPNN). Update cards and index rows as statuses change (`planned | dispatched | read | verdicted`).
2. **DISPATCH -- ALWAYS via `Agent(haipipe-probe-orchestrator-agent)`, no exceptions.** This includes AUDIT-shaped scopes ("re-verify the existing evidence", "double-check the refs"): the agent's SWEEP answers them from the ledger; never invent a side-channel worker. Pass the plan content + mode + project root. The worker NEVER sweeps the project itself, NEVER reads discoveries/insights inline, NEVER inlines `Skill("haipipe-probe")` -- even for a "tiny" lookup. The shape decision (reused | enriched | fresh) belongs to the AGENT's SWEEP, in clean context. Likely-reuse plans dispatch synchronously (fast); a plan that likely needs a FRESH discovery/task run (real searching, minutes) dispatches with `run_in_background` and TRANSLATE runs when it returns -- sync on a fresh run freezes the whole session for the downstream chain. Judge fresh-vs-reuse from the plan content alone; when unsure, go background. Card: `status: dispatched`, then per the agent's return.
3. **TRANSLATE (probe is application-unaware; this worker is the bilingual layer).** The worker reads NO project files; it may verify returned refs resolve with a bare `ls` (existence only, never content). Light returns -- anchored takeaways (<=5 lines, each with its source anchor) transcribe into the card (`status: read`; `refs:` = the execution artifacts the return names -- discoveries/.../sources.md, tasks/... -- always direct). Full returns -- the gateway's verdict block (G1/G2/G3 + verdict + reasoning + judged-by + date) lands in the card's `## Verdict` section, the card goes `status: verdicted`, and the claims ledger's C-line + Evidence Campaign row flip in the same TRANSLATE (enum: `supported | refuted | inconclusive`); verified numbers the return carries land in the stage's `_VALUES_` file with their anchors; sections / round logs backfill from the card, never from memory. Buffer convention: `../../../haipipe-application/fn/probe-plans.md`.

## Hard boundaries (inherited by all stages)

- The worker NEVER fabricates numbers, NEVER creates ad-hoc plots inline, NEVER writes insight cards (deposits belong to the probe/insight side).
- Never dispatch discovery/task orchestrator agents directly from a stage skill -- this worker is the ONLY door: stage -> this worker -> gateway -> discovery/task during probe's own Gather. A stage that calls `Agent(haipipe-discovery-orchestrator-agent)` or `/haipipe-probe` itself is bypassing the evidence contract (results land nowhere reviewable and die with the reply).
- All flags (uncertain values, unverified sources) resolve in CHECK, not here.

## Phase status (derived from disk)

```
probe ✅    all cards for the 🔥 stage are read/verdicted, ledger backfilled
probe 🚀    cards dispatched, returns pending
probe ⬜    needs recorded, nothing dispatched
probe --    skipped (stage had no evidence needs; logged in _LOG)
```

Strip form: `phase:   draft ✅  │  probe 🔥🚀  │  revise ⬜  │  check ⬜` (sectioned venues may split document tracks as `probe: val ⬜ cite --  disp 🚀` when section-edit runs them).

## Return contract

```
status:    ok | blocked
stage:     <stage-name>
cards:     <PPNN: planned->dispatched->read/verdicted transitions this run>
next:      <suggested command>
```

## Sibling phase workers

| Phase | Worker | Called after |
|---|---|---|
| DRAFT | haipipe-application-draft | -- |
| PROBE (this) | haipipe-application-probe | DRAFT |
| REVISE | haipipe-application-revise | PROBE |
| CHECK | haipipe-application-check | REVISE |
