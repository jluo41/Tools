Per-stage dispatch reference (haipipe-application-probe)
==========================================================

Loaded on demand from SKILL.md. Which stage dispatches which mode, stage specifics, venue-scaled lane rules, and phase-status strip forms.

Why this phase is called PROBE
-------------------------------
The phase is named after what it does: dispatch evidence needs through /haipipe-probe, the project-side evidence gateway (mode light|full). Paper's earlier name for the phase, GATHER, collided with probe's own internal stage 2 (probe's lifecycle is Plan -> Gather -> Read -> Judge -> Deposit); application inherited the post-rename vocabulary. "Probe's own Gather" means that internal probe stage, not this application phase.

The downstream lifecycles are NESTED under probe:

```
/haipipe-probe       evidence gateway (explore+gather), mode: light|full
        |
        +-- during its Gather, probe calls:
        |     /haipipe-discovery   external evidence: search+read, judge/synthesize, idea
        |     /haipipe-task        task domains (data, display, eval, stata, ...;
        |                          probe picks per need)
        +-- at Deposit, probe files:
              /haipipe-insight     DIKW cards; settled evidence is reusable
                                   across papers AND applications instead of re-collected
```

Per-stage list (lane hooks = HARVESTERS: they transcribe landed evidence, never acquire; acquisition is always PP card -> gateway)
----------------------------------------------------------------------------------------------------------------------------------
Spine folder names are the intervention's `0-lifecycle/` stage folders (dual-2 numbering mirrors paper: 2-venue + 2-pitch).

- **0-seed** (venue-FREE) -- mode light (-> discovery), DEFAULT RUN for a new seed: landscape / prior interventions / benchmarks / cohort sanity to sharpen the seed question. No venue pinned yet: source anchors stay in the card takeaways; no citation/display lanes.
- **1a-descriptions** (venue-FREE, ladder rung) -- mode light (-> task): data-profile probes ("profile the cohort", "pull engagement summary"); TRANSLATE lands anchored numbers (statistic + pointer + as-of date) directly as D entries -- the 1a doc IS the values doc, no separate satellite. Consumes seed's FORWARD pointers at DRAFT.
- **1b-themes** (venue-FREE, ladder rung) -- mode light (-> discovery, task for quick in-data confirmations): field-pattern probes ("what messaging levers does the literature name?"); TRANSLATE lands grounding refs onto T entries.
- **1c-claims** (venue-FREE, ladder rung) -- mode FULL (-> task + discovery): the core evidence rung; one plan per GAP claim; verdicts backfill the C-line AND the Evidence Campaign row at TRANSLATE (enum: supported | refuted | inconclusive); insight deposit optional (ladder restage R7). Verified numbers the returns carry land in `_VALUES_1c-claims.md` (values lane fires here even pre-pin). The pinned venue's settlement bar later reads THIS campaign.
- **1d-advice** (venue-FREE, ladder rung) -- rarely fires: derivation is in-stage work; an advice entry exposing a NEW evidence gap routes back as a `1c-claims/_PROBE/` card, never gathers here.
- **2-venue** -- mode light: venue-level investigation needs -- channel capability, compliance constraints, prior sends on this channel; cards in `2-venue/_PROBE/`.
- **2-pitch** -- light, rare: anchor evidence for the theory of change if the ledger lacks it.
- **3-narrative** -- rarely fires; a beat exposing a NEW evidence gap routes back to claims as a `1c-claims/_PROBE/` card, never gathers here.
- **4-display** (venue-GATED: dashboard/ui-card/report; optional email; skipped sms/push/reminder/checklist) -- display lane; unit GENERATION is commissioned like any evidence need: PP card -> gateway -> task orchestrator (SWEEP answers "does this unit already exist?"); the hook only LINKs what landed into `_DISPLAY_4-display.md` + the artifact.
- **5-section-edit** (sectioned venues only) -- full document probe: values + citation lanes per section, display lane where the section references units.

Dispatch rules (both apply to every dispatch)
----------------------------------------------
1. **Mode: light by default; full for claims verdicts; background for fresh runs.** A light probe stops at Read and returns evidence to the caller -- right for context questions (seed landscape, venue capability, section-edit lookups). Request `mode: full` only when the intervention needs a COMMITTED verdict that backfills a claim slot and deposits insight cards (claims stage's normal case). Light can escalate to full later; never start heavy for a question that only needs orientation. Likely-fresh plans (new searches / task runs) always dispatch `run_in_background=true`.
2. **Reuse-before-create -- decided by the AGENT, not the worker.** The gateway's SWEEP scans discoveries/tasks/insights in clean context and picks the shape: REUSED (existing artifact covers the need; refs point at it), ENRICHED (same-topic deltas into an existing discovery's ledger), or FRESH (new discovery/task work). No shape creates a probe folder (folderless probe); a full-mode verdict's home is the PPNN card's `## Verdict`. Duplication is a mental-model tax: two half-overlapping evidence sets cost more than one enriched one.

Seed specifics (mode light; DEFAULT RUN for a new seed)
--------------------------------------------------------
Skip only on re-entry or minor edits, and only by an explicit logged verdict (`[PROBE] skipped -- <reason>` in the stage _LOG; phase line shows `--`) -- never silently. The seed question needs outside context, not verdicts:

```
landscape ("what does this space look like?")   -> probe -> discovery Review -> landscape.md
prior interventions ("who has tried this?")     -> probe -> discovery Search -> sources.md
cohort sanity ("does the population exist?")    -> probe -> task (light data probe)
```

Takeaways feed the opportunity, mechanism hypothesis, and kill criteria in 0-seed.md. Full evidence stays project-side, reusable by claims.

Claims specifics (rung 1c, mode full)
--------------------------------------
Every GAP/weak claim emits a probe plan -- sweep first (reuse-before-create), then probe fans out by need type:

```
claim needs a verdict / robustness check   -> probe (Plan -> Gather -> Read -> Judge)
probe needs a run / data artifact          -> probe -> /haipipe-task
probe needs outside context / benchmarks   -> probe -> /haipipe-discovery
finished evidence worth keeping            -> /haipipe-insight (K/W cards; OPTIONAL deposit, ladder restage R7 -- 1d owns on-request W deposits)
```

Verdicts flip the C-line and the Evidence Campaign row in 1c-claims.md in the same TRANSLATE (enum: supported | refuted | inconclusive, citing the probe verdict). The intervention owns the NEED; the probe owns the VERDICT. The venue gate later evaluates its settlement bar (light/medium/full) against the campaign table and through 1d's derivations.

Venue-scaled lane rules (which lanes exist, decided at lane CREATION)
----------------------------------------------------------------------
- `_VALUES_` -- always eligible, every venue: quoted numbers trace to task results.
- `_CITATION_` -- sectioned venues only (report/dashboard-like, per the venue profile); never before a sectioned venue is pinned.
- `_DISPLAY_` -- only if the venue's artifact has display units (panels, charts, figures).
- Simple venues (sms/push/reminder): no document lanes; PROBE is claims-evidence only.
- The checker (`check-probe-cards.sh`) is presence-driven -- it FAILs OWED lane lines and scans working docs that exist; venue-scaling lives here, at creation, not in the checker.

Phase status (derive from disk)
--------------------------------
```
probe ✅    all cards for the 🔥 stage are read/verdicted, ledger backfilled, no OWED lanes
probe 🚀    cards dispatched, returns pending
probe ⬜    needs recorded, nothing dispatched
probe --    skipped (stage had no evidence needs; logged in _LOG)
```

Strip form: `phase:   draft ✅  │  probe 🔥🚀  │  revise ⬜  │  check ⬜`. Sectioned venues may split the fired lanes when section-edit runs them:

```
phase:   draft ✅  │  probe: val 🚀  cite ⬜  disp --  │  revise ⬜  │  check ⬜
```

GATE RULE (paper seed incident, JL 2026-07-07): the probe phase may NOT show ✅ while any lane is OWED. A lane is OWED when a PP card carries its lane line with `harvest: OWED`, or when a return named harvestable content for a fired lane whose doc (⬜) does not exist. `probe ✅ (cite ⬜ ...)` on a sectioned venue is a contradiction: run check-probe-cards.sh, it FAILs.
