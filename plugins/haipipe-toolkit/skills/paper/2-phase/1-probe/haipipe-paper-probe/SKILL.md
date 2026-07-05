---
name: haipipe-paper-probe
description: "PROBE phase worker (internal). Called by stage skills after DRAFT to collect what the draft needs but does not have -- internal materials (values from the project's own task results, display units from task-folders) and external ones (citations, discovery lit). Document workers (citation/values/display) plus dispatch through /haipipe-probe (the project-side evidence gateway, mode light|full; probe calls discovery and task during its own Gather, deposits to insight). Fully automatic, human review in CHECK only. Users invoke stage skills (seed, claims, pitch...), not this skill directly."
argument-hint: "[stage-or-section] [paper-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "2.3.2"
  last_updated: "2026-07-05"
  summary: "PROBE phase worker (internal). Two route families: document workers (citation/values/display, each owning a _DOC_ needs registry) + dispatch through /haipipe-probe (mode light by default, full for claims; reuse-before-create). Harvest acceptance is MECHANICAL-FOR-REAL: run the greps, never eyeball."
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
| seed | ○ harvest | -- | -- | 🔎 probe mode: light (→ discovery) | landscape / related work / novelty to sharpen the seed question; when the probe returns sources, citation worker HARVESTs them into _CITATION_0-seed.md |
| claims | -- | -- | -- | 🏋️ probe mode: full (→ task + discovery) | the core evidence stage: probe plans per GAP claim, tasks for runs/data, verdicts backfill the ledger + deposit to insight |
| pitch | ✅ | -- | -- | -- | pitch cites anchor papers |
| narrative | ✅ | -- | ✅ | -- | narrative maps beats to displays |
| display | -- | -- | ✅ | via display worker | display worker routes unit generation to /haipipe-task |
| section-edit | ✅ | ✅ | ✅ | -- | full document probe (all three tracks) |

## Evidence routes (probe gateway)

Never search or compute inline, and never dispatch discovery/task orchestrator agents directly from a stage skill -- this worker is the ONLY door: stage -> this worker -> `/haipipe-probe` (the universal evidence gateway) -> discovery/task during probe's own Gather stage. A stage that calls `Agent(haipipe-discovery-orchestrator-agent)` or `/haipipe-probe` itself is bypassing the evidence contract (results won't land project-side as a probe).

**Probe dispatch rules (both apply to every dispatch):**

1. **Mode: light by default.** A light probe stops at Read and returns its evidence to the caller -- right for context questions (seed landscape, section-edit lookups). Request `mode: full` only when the paper needs a COMMITTED verdict that backfills a claim slot and deposits insight cards (the claims stage's normal case). A light probe can escalate to full later; never start heavy for a question that only needs orientation.

2. **Reuse-before-create -- decided by the AGENT, not this worker.** The orchestrator agent's SWEEP step (its Step 1.5) scans the project (probes, discoveries, tasks, insights) in clean context and picks one of three outcomes: (a) an existing probe covers the claim -> ENRICH it (extend its Gather, re-run Read/Judge) instead of near-duplicating; (b) an existing artifact fully covers a LIGHT plan -> REUSE DIRECTLY, no wrapper probe created (the return names the artifact; the plan's `ref:` points at it; a wrapper materializes later only if claims escalates to a committed verdict); (c) partial or no coverage -> create the probe (mode per plan), Gather Links what exists and Calls only what is missing. Full mode always gets a probe folder -- a verdict needs a home. Probe sprawl is a mental-model tax: two half-overlapping probes cost more than one enriched one.

**Seed (mode: light; DEFAULT RUN for a new seed).** Skip only on re-entry or minor edits, and only by an explicit logged verdict (`[PROBE] skipped -- <reason>` in the stage `_LOG`, phase line shows `--`) -- never silently. The seed question needs outside context, not verdicts:

```
landscape ("what does this field look like?")  → probe → discovery Review → landscape.md
related work ("who has done this?")            → probe → discovery Search → sources.md
novelty ("is this idea new?")                  → probe → discovery novelty-check (查新) → verdict.md
```

Record the probe link + 3-5 takeaway lines IN THE PLAN FILE itself (`0-lifecycle/0-seed/_PROBE/PPNN_*.md`, `status: read`); takeaways feed Motivations and Tentative Claim Shape. Sources the probe brought back are HARVESTed by the citation worker into `_CITATION_0-seed.md` (candidates only) so the user can eyeball them paper-side. Full evidence stays project-side, reusable by claims. (`_DISCOVERY_{stage}.md` is retired -- the plan file carries the takeaways.)

**Claims (mode: full).** Every GAP/weak claim emits a probe plan -- but sweep first (reuse-before-create), then probe fans out by need type:

```
claim needs a verdict / robustness check   → probe (Plan → Gather → Read → Judge)
probe needs a run / data artifact          → probe → /haipipe-task (data/algo/display/stata task types)
probe needs outside context / citation     → probe → /haipipe-discovery
finished evidence worth keeping            → /haipipe-insight (K/W cards)
```

Verdicts backfill the `_EVIDENCE_` slots in 1-claims.md (supported | weak | GAP, citing the probe verdict). The paper owns the NEED; the probe owns the VERDICT. See `../../wiki/12-evidence-routing.md` and `../../wiki/11-delivery-need.md`.

## From-buffer entry (the ONLY path that dispatches the umbrella's probe plans)

`Skill("haipipe-paper-probe", args="from-buffer <paper_root> [PPNN]")` -- invoked by `/haipipe-paper probe run` or by a stage's own PROBE phase. The umbrella NEVER calls `/haipipe-probe` directly; this worker is the single dispatch point.

This worker does exactly three things -- BOOKKEEP, DISPATCH, TRANSLATE -- and NO evidence work of its own:

1. **BOOKKEEP.** Read the index (`<paper_root>/1-probe-plans/README.md`), resolve each planned item to its per-stage `_PROBE/PPNN_*.md` file (or the one named PPNN). Update plan files and index rows as statuses change.
2. **DISPATCH -- ALWAYS via `Agent(haipipe-probe-orchestrator-agent)`, no exceptions.** This includes AUDIT-shaped scopes: "re-verify the existing set", "audit the citations", "double-check the refs" are ordinary plans for the SAME dispatch -- the agent's SWEEP answers them from the ledger (entries marked VERIFIED with method+date ARE the verification; the agent re-buys nothing). Never invent a side-channel worker (general-purpose web auditor etc.) because a scope has no named row here -- if it is evidence work, this dispatch is the only door. Pass the plan content + mode + project root. The worker NEVER sweeps the project itself, NEVER reads discoveries/probes/insights inline, NEVER inlines `Skill("haipipe-probe")` -- even for a "tiny" lookup. The reuse decision (enrich an existing probe / reuse a covering artifact directly with no wrapper / create-and-gather) belongs to the AGENT's SWEEP step, in clean context; a covering artifact the agent finds is consumed there, not re-read paper-side. Likely-reuse plans dispatch synchronously (fast); a plan that likely needs a FRESH discovery/task run (real searching, minutes) dispatches with `run_in_background` and TRANSLATE runs when it returns. Sync on a fresh run freezes the ENTIRE paper session for the whole downstream chain (live test-2-2222: 25 minutes frozen through probe -> discovery -> creator -> reviewer); "I need the return to TRANSLATE" is NOT a reason to go sync -- the background return arrives and TRANSLATE runs then. Judge fresh-vs-reuse from the plan content alone (a plan that names no covering artifact, or asks for a landscape / new searches / new task run, is fresh); when unsure, go background. Plan file: `status: dispatched`, then per the agent's return.
3. **TRANSLATE (probe is paper-unaware; this worker is the bilingual layer).** The worker reads NO project files; it may verify returned refs resolve with a bare `ls` (existence only, never content). Light returns -- anchored takeaways (<=5 lines, each with its source anchor) transcribe into the plan file (`status: read`; `ref:` = the probe folder, or the directly-reused artifact when the agent chose no-wrapper reuse). When the return carries a `pick_list`, dispatch the citation HARVEST SUBAGENT (`haipipe-paper-probe-citation` harvest form; the dispatch prompt PASSES the card-format spec explicitly -- `### <title>` heading + summary/finding/relevance/status/Scholar/source_ref bullets); it expands the picked sources.md entries into `_CITATION_{stage}.md` cards in its own clean context; this worker then does MECHANICAL ACCEPTANCE -- and mechanical means RUN THE COMMANDS, never eyeball (run-3 acceptance claimed "each has anchor + finding" while `grep -c 'finding:'` returned 0):
   - count: new `^### ` card headings == pick_list length
   - fields: every new card block greps a `- summary:` AND a `- finding:` line
   - anchors: every new card's `source_ref` names a sources.md + S##; `grep` that S## heading in that file -- it must EXIST (the agent's fresh evidence landed). An unresolvable anchor is a REJECT, not a warning
   - no bibtex: `grep -c '@' == 0` on the new cards
   One reject → re-dispatch the harvest subagent with the defect list (one retry); still failing → mark the plan file `status: read (harvest DEFECTIVE)` and surface it in the stage reply. Produce and review are never the same context. Full returns -- verdicts backfill 1-claims / sections / round logs (`status: verdicted`). Buffer convention: `../../../haipipe-paper/fn/probe-plans.md`.

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
