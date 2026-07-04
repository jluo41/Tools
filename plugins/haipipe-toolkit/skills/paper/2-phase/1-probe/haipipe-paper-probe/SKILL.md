---
name: haipipe-paper-probe
description: "PROBE phase worker (internal). Called by stage skills after DRAFT to collect what the draft needs but does not have -- internal materials (values from the project's own task results, display units from task-folders) and external ones (citations, discovery lit). Document workers (citation/values/display) plus dispatch through /haipipe-probe (the project-side evidence gateway, mode light|full; probe calls discovery and task during its own Gather, deposits to insight). Fully automatic, human review in CHECK only. Users invoke stage skills (seed, claims, pitch...), not this skill directly."
argument-hint: "[stage-or-section] [paper-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.7.2"
  last_updated: "2026-07-03"
  summary: "PROBE phase worker (internal). Two route families: document workers (citation/values/display, each owning a _DOC_ needs registry) + dispatch through /haipipe-probe (mode light by default, full for claims; reuse-before-create)."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-paper-probe (internal phase worker)
====================================================

PROBE phase worker. Called by stage skills (seed, claims, pitch, narrative, display, section-edit) after DRAFT to collect what the draft needs but does not have. Materials can be internal (values traced to the project's own task results, display units rendered by task-folders) or external (citations, discovery lit, landscape). The stage defines WHAT needs collecting. This skill defines HOW to get it.

**Why this phase is called PROBE.** The phase is named after what it does: dispatch evidence needs through `/haipipe-probe`, the project-side evidence gateway (mode light|full). The previous name, GATHER, collided with probe's own internal stage 2 (probe's lifecycle is Plan → Gather → Read → Judge → Deposit); that collision is exactly why the paper phase was renamed. When this file says "probe's own Gather", it means that internal probe stage, not this paper phase.

The downstream lifecycles are NESTED under probe:

```
/haipipe-probe       claim-level evidence gateway, mode: light|full
                     light (DEFAULT): Plan → Gather → Read, output returns to caller
                     full: + Judge → Deposit (committed verdict + insight cards)
        │
        ├── during its Gather, probe calls:
        │     /haipipe-discovery   external evidence: search+read, judge/synthesize, idea
        │     /haipipe-task        9 task domains: data, nn, end, individual, fit, eval,
        │                          display, stata, agent (probe picks the right one per need)
        │
        └── at Deposit, probe files:
              /haipipe-insight     DIKW knowledge base (D/I/K/W cards); settled evidence is
                                   reusable across papers instead of re-collected
```

**Not user-facing.** Users invoke stage skills:
```
/haipipe-paper pitch        → pitch skill calls this internally for PROBE phase
/haipipe-paper narrative    → narrative skill calls this internally for PROBE phase
/haipipe-paper section-edit §3  → section-edit skill calls this internally
```

## What PROBE means

PROBE = collect what the draft needs but does not have. Two route families:

```
Document workers (paper-side, one working doc each):
  haipipe-paper-probe-citation     →  _CITATION_{stage}.md   what to cite, where
  haipipe-paper-probe-values       →  _VALUES_{stage}.md     every number, traced
  haipipe-paper-probe-display      →  _DISPLAY_{stage}.md    what displays are NEEDED
                                      (need → unit → status; the units themselves
                                       live in 0-displays/, rendered by tasks)

Evidence gateway (project-side lifecycles):
  /haipipe-probe                   →  claim-level evidence contract; during its
                                      own Gather, probe calls /haipipe-discovery
                                      (lit/landscape) and /haipipe-task (runs/data);
                                      at Deposit it files verdicts into
                                      /haipipe-insight (D/I/K/W cards)
```

All routes are fully automatic dispatch. The agent collects aggressively, flags uncertain items, and moves on. Human verification happens in CHECK, not here.

## Per-stage dispatch

| Stage | citation | values | display | probe → discovery/task | Notes |
|---|---|---|---|---|---|
| seed | -- | -- | -- | 🔎 probe mode: light (→ discovery) | landscape / related work / novelty to sharpen the seed question |
| claims | -- | -- | -- | 🏋️ probe mode: full (→ task + discovery) | the core evidence stage: probe plans per GAP claim, tasks for runs/data, verdicts backfill the ledger + deposit to insight |
| pitch | ✅ | -- | -- | -- | pitch cites anchor papers |
| narrative | ✅ | -- | ✅ | -- | narrative maps beats to displays |
| display | -- | -- | ✅ | via display worker | display worker routes unit generation to /haipipe-task |
| section-edit | ✅ | ✅ | ✅ | -- | full document probe (all three tracks) |

## Evidence routes (probe gateway)

Never search or compute inline, and never dispatch discovery/task orchestrator agents directly from a stage skill -- this worker is the ONLY door: stage -> this worker -> `/haipipe-probe` (the universal evidence gateway) -> discovery/task during probe's own Gather stage. A stage that calls `Agent(haipipe-discovery-orchestrator-agent)` or `/haipipe-probe` itself is bypassing the evidence contract (results won't land project-side as a probe).

**Probe dispatch rules (both apply to every dispatch):**

1. **Mode: light by default.** A light probe stops at Read and returns its evidence to the caller -- right for context questions (seed landscape, section-edit lookups). Request `mode: full` only when the paper needs a COMMITTED verdict that backfills a claim slot and deposits insight cards (the claims stage's normal case). A light probe can escalate to full later; never start heavy for a question that only needs orientation.

2. **Reuse-before-create.** Before opening a new probe, sweep what exists: `1-probe-plans/` (the cross-paper index), the project's probe folders, and the insight KB. If an existing probe covers the claim (same topic, compatible scope), ENRICH it -- extend its Gather with the new evidence need, re-run Read/Judge -- instead of creating a near-duplicate. Create a new probe only when no existing one covers the topic; when the match is ambiguous, ask rather than fork. Probe sprawl is a mental-model tax: two half-overlapping probes cost more than one enriched one.

**Seed (mode: light; DEFAULT RUN for a new seed).** Skip only on re-entry or minor edits, and only by an explicit logged verdict (`[PROBE] skipped -- <reason>` in the stage `_LOG`, phase line shows `--`) -- never silently. The seed question needs outside context, not verdicts:

```
landscape ("what does this field look like?")  → probe → discovery Review → landscape.md
related work ("who has done this?")            → probe → discovery Search → sources.md
novelty ("is this idea new?")                  → probe → discovery novelty-check (查新) → verdict.md
```

Record the probe/discovery link + 3-5 takeaway lines in `_DISCOVERY_0-seed.md` next to the seed artifact; takeaways feed Motivations and Tentative Claim Shape. Full evidence stays project-side, reusable by claims.

**Claims (mode: full).** Every GAP/weak claim emits a probe plan -- but sweep first (reuse-before-create), then probe fans out by need type:

```
claim needs a verdict / robustness check   → probe (Plan → Gather → Read → Judge)
probe needs a run / data artifact          → probe → /haipipe-task (data/algo/display/stata task types)
probe needs outside context / citation     → probe → /haipipe-discovery
finished evidence worth keeping            → /haipipe-insight (K/W cards)
```

Verdicts backfill the `_EVIDENCE_` slots in 1-claims.md (supported | weak | GAP, citing the probe verdict). The paper owns the NEED; the probe owns the VERDICT. See `../../wiki/12-evidence-routing.md` and `../../wiki/11-delivery-need.md`.

## From-buffer entry (the ONLY path that dispatches the umbrella's probe plans)

`Skill("haipipe-paper-probe", args="from-buffer <paper_root> [PPNN]")` -- invoked by `/haipipe-paper probe run` or by a stage's own PROBE phase. The umbrella NEVER calls `/haipipe-probe` directly; this worker is the single dispatch point. It reads the planned items in `<paper_root>/1-probe-plans/` (or the one named PPNN), applies reuse-before-create per plan, dispatches each to `/haipipe-probe` with the plan's mode, updates the plan file (`status: dispatched`, `probe_ref: <active probe>`), and returns a dispatch summary (plans dispatched / enriched / skipped + refs). Verdicts later backfill 1-claims / sections / round logs per the buffer convention (`../../../haipipe-paper/fn/probe-plans.md`).

## Section-edit dispatch logic

For section-edit, read the section outline and determine which workers to run:

| Worker | Run when | Skip when |
|---|---|---|
| citation | always | never (every section cites) |
| values | outline contains numbers, statistics, or data references | pure argumentative section with no quantitative claims |
| display | outline references figures, tables, or visual elements | no display callouts in the outline |

When no specific worker is named, run all applicable workers in order: citation → values → display.

## Hard boundaries (inherited by all workers)

- Agent NEVER generates bibtex, NEVER adds to .bib
- Agent NEVER fabricates numbers
- Agent NEVER creates ad-hoc plots inline
- _CITATION_ is plain text only, no bibtex blocks
- All flags (🔍 unverified citations, ⚠️ uncertain values) resolve in CHECK, not here

## Phase status

Derive probe status from disk:

```
cite ✅    _CITATION_ exists, all entries placed (no 🔍 remaining)
cite 🚀    _CITATION_ exists, work in progress
cite 🔍N   _CITATION_ has N unverified candidates
cite ⬜    _CITATION_ does not exist

val ✅     _VALUES_ exists, all entries verified
val 🚀     _VALUES_ exists, work in progress
val --     skipped (section has no numbers)
val ⬜     _VALUES_ does not exist

disp ✅    _DISPLAY_ exists, every need linked to a rendered unit
disp 🚀    _DISPLAY_ exists, needs recorded, units in progress
disp --    skipped (section has no displays)
disp ⬜    _DISPLAY_ does not exist
```

Strip form (the cite/val/disp sub-tracks belong to the probe phase):

```
phase:   draft ✅  │  probe: cite 🔥🚀  val --  disp --  │  revise ⬜  │  check ⬜
```

## Relation to other phases

```
DRAFT → PROBE (this) → REVISE → CHECK
         │
         ├── haipipe-paper-probe-citation   → _CITATION_.md
         ├── haipipe-paper-probe-values     → _VALUES_.md
         ├── haipipe-paper-probe-display    → _DISPLAY_.md (+ units in 0-displays/)
         └── /haipipe-probe                 → discovery/task during its Gather,
                                              insight cards at Deposit
```

PROBE reads the DRAFT outline to know what to collect. REVISE reads PROBE outputs to weave citations and values into prose. CHECK verifies all PROBE flags.

## Return contract

```
status:    ok | blocked
section:   <section-name>
workers:   cite <status> │ val <status> │ disp <status>
next:      <suggested command>
```


## Who calls this skill

Stage skills call this as their PROBE phase:

| Stage skill | What this skill collects |
|---|---|
| haipipe-paper-seed | light: probe → discovery (landscape / related work / novelty) |
| haipipe-paper-claims | HEAVY: probe plans per GAP claim; probe → task (runs/data) + discovery (lit); verdicts backfill _EVIDENCE_ |
| haipipe-paper-pitch | citation audit for anchor papers |
| haipipe-paper-narrative | citation + display needs per beat |
| haipipe-paper-display | routes display units to task-folders |
| haipipe-paper-section-edit | full document probe (citation + values + display) |

## Sibling phase workers

| Phase | Worker | Called after |
|---|---|---|
| DRAFT | haipipe-paper-draft | -- |
| PROBE (this) | haipipe-paper-probe | DRAFT |
| REVISE | haipipe-paper-revise | PROBE |
| CHECK | haipipe-paper-check | REVISE |
