Per-stage dispatch reference (haipipe-paper-probe)
====================================================

Loaded on demand from SKILL.md. Which stage runs which workers/mode, stage
specifics, section-edit worker logic, and phase-status strip forms.

Why this phase is called PROBE
-------------------------------
The phase is named after what it does: dispatch evidence needs through
/haipipe-probe, the project-side evidence gateway (mode light|full). The
previous name, GATHER, collided with probe's own internal stage 2 (probe's
lifecycle is Plan -> Gather -> Read -> Judge -> Deposit); that collision is
why the paper phase was renamed. "Probe's own Gather" means that internal
probe stage, not this paper phase.

The downstream lifecycles are NESTED under probe:

```
/haipipe-probe       evidence gateway (explore+gather), mode: light|full
        |
        +-- during its Gather, probe calls:
        |     /haipipe-discovery   external evidence: search+read, judge/synthesize, idea
        |     /haipipe-task        9 task domains (data, nn, end, individual, fit,
        |                          eval, display, stata, agent)
        +-- at Deposit, probe files:
              /haipipe-insight     DIKW cards; settled evidence is reusable
                                   across papers instead of re-collected
```

Per-stage table (workers = HARVESTERS: they transcribe landed evidence,
never acquire; acquisition is always PP card -> gateway)
----------------
- **seed** -- probe mode light (-> discovery): landscape / related work / novelty to sharpen the seed question; returned sources HARVEST into _CITATION_0-seed.md. No values/display lanes.
- **claims** -- probe mode FULL (-> task + discovery): the core evidence stage; probe plans per GAP claim (INCLUDING seed's `[FORWARD -> CLAIMS]` pointers, consumed at stage open — see haipipe-paper-claims), verdicts backfill the ledger + deposit to insight.
- **pitch** -- citation lane only (anchor papers).
- **narrative** -- citation + display lanes (beats map to displays).
- **display** -- display lane. From SECTION/NARRATIVE context a missing unit is NEVER commissioned: it becomes a DR row in `0-lifecycle/4-display/_DISPLAY_REQUEST.md` (the display stage's inbox; JL 2026-07-10) and the card closes `answered-local (rerouted: DRNN)`. Only the DISPLAY STAGE itself commissions evidence/render work for its accepted units (via its own PROBE lanes); the harvester LINKs existing/done units.
- **section-edit** -- full document probe: citation + values + display lanes.
  (disp statuses include 📨 = DR request pending in the 4-display inbox; the
   display axis cannot pass CHECK until the row is `done` and the unit linked.)

Dispatch rules (both apply to every dispatch)
----------------------------------------------
1. **Mode: light by default.** A light probe stops at Read and returns evidence
   to the caller -- right for context questions (seed landscape, section-edit
   lookups). Request `mode: full` only when the paper needs a COMMITTED verdict
   that backfills a claim slot and deposits insight cards (claims stage's
   normal case). Light can escalate to full later; never start heavy for a
   question that only needs orientation.
2. **Reuse-before-create -- decided by the AGENT, not the worker.** The
   gateway's SWEEP scans discoveries/tasks/insights in clean context and picks
   the shape: REUSED (existing artifact covers the need; refs point at it),
   ENRICHED (same-topic deltas into an existing discovery's ledger), or FRESH
   (new discovery/task work). No shape creates a probe folder (folderless
   refactor 2026-07-05); a full-mode verdict's home is the PPNN card's
   `## Verdict`. Duplication is a mental-model tax: two half-overlapping
   evidence sets cost more than one enriched one.

Seed specifics (mode light; DEFAULT RUN for a new seed)
--------------------------------------------------------
Skip only on re-entry or minor edits, and only by an explicit logged verdict
(`[PROBE] skipped -- <reason>` in the stage _LOG; phase line shows `--`) --
never silently. The seed question needs outside context, not verdicts:

```
landscape ("what does this field look like?")  -> probe -> discovery Review -> landscape.md
related work ("who has done this?")            -> probe -> discovery Search -> sources.md
novelty ("is this idea new?")                  -> probe -> discovery novelty-check -> verdict.md
```

Takeaways feed Motivations and Tentative Claim Shape in 0-seed.md. Sources the
probe brought back HARVEST into _CITATION_0-seed.md (candidates only) so the
user can eyeball them paper-side. Full evidence stays project-side, reusable
by claims. (_DISCOVERY_{stage}.md is retired -- the PP card carries takeaways.)

Claims specifics (mode full)
-----------------------------
Every GAP/weak claim emits a probe plan -- sweep first (reuse-before-create),
then probe fans out by need type:

```
claim needs a verdict / robustness check   -> probe (Plan -> Gather -> Read -> Judge)
probe needs a run / data artifact          -> probe -> /haipipe-task
probe needs outside context / citation     -> probe -> /haipipe-discovery
finished evidence worth keeping            -> /haipipe-insight (K/W cards)
```

Verdicts backfill the _EVIDENCE_ slots in 1-claims.md (supported | weak | GAP,
citing the probe verdict). The paper owns the NEED; the probe owns the VERDICT.
See ../../../../wiki/12-evidence-routing.md + ../../../../wiki/11-delivery-need.md.

Section-edit worker logic
--------------------------
Read the section outline and decide which document workers run:
- **citation** -- always (every section cites).
- **values** -- when the outline contains numbers, statistics, or data references; skip for pure argumentative sections.
- **display** -- when the outline references figures/tables/visuals; skip otherwise.
When no worker is named, run all applicable in order: citation -> values -> display.

Phase status (derive from disk)
--------------------------------
```
cite ✅  _CITATION_ exists, all entries placed (no 🔍 remaining)
cite 🚀  _CITATION_ exists, work in progress
cite 🔍N _CITATION_ has N unverified candidates
cite ⬜  _CITATION_ does not exist

val ✅   _VALUES_ exists, all verified   · val --  skipped (no numbers)
val 🚀   in progress                     · val ⬜  does not exist

disp ✅  every need linked to a rendered unit · disp --  skipped (no displays)
disp 🚀  needs recorded, units in progress    · disp ⬜  does not exist
```

Strip form (cite/val/disp sub-tracks belong to the probe phase):

```
phase:   draft ✅  │  probe: cite 🔥🚀  val --  disp --  │  revise ⬜  │  check ⬜
```

GATE RULE (JL 2026-07-07, the seed incident): the probe phase may NOT show ✅
while any lane is OWED. A lane is OWED when a PP card carries its lane line
with `harvest: OWED`, or when a return named harvestable content for a lane
whose doc (⬜) does not exist. `probe ✅ (cite ⬜ ...)` -- the exact strip the
incident shipped -- is a contradiction: run check-probe-cards.sh, it FAILs.
