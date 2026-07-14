Per-stage dispatch reference (haipipe-application-probe)
==========================================================

Loaded on demand from SKILL.md. Which stage raises which questions, stage specifics, venue-scaled lane rules, and phase-status strip forms.

Constitution: `../../../../../probe/haipipe-probe/SKILL.md` (v8.0.0). This file is a per-stage
addendum, never a second source of truth for the model.

Why this phase is called PROBE
-------------------------------

The phase is named after what it produces: the PROBE FILES —
`<intervention_root>/1-probes/PPNN_<topic>.md`, one file per topic, one SECTION per question the
DRAFT raised. The phase COLLECTS questions and BINDS each to an answer. It does not do evidence
work; it dispatches it.

The executor layers sit BELOW, and they are probe-UNAWARE:

```
   📄 the PROBE phase (this worker)      raises + binds questions
        │  hands the `commission` block, VERBATIM, to:
        │
        ├── Agent(haipipe-task-orchestrator-agent)        internal execution
        └── Agent(haipipe-discovery-orchestrator-agent)   external evidence
                  │  each runs its own `qa` gate: ① QA SCAN ② DIGEST ③ P-B-E-R
                  ▼
            <leaf>/QA/<n>-<slug>.md      the answer, in GENERAL language
                  │
                  ▼
   📄 the section's `target:` points at that FILE; `reading:` interprets it;
      the CLAIM's status flips in 1-claims.md — never in the probe file.
```

💀 The probe GATEWAY (`Agent(haipipe-probe-orchestrator-agent)`) is RETIRED. There is no
"evidence gateway" tier any more: its SWEEP became this worker's MATCH step, and its dispatch is
now the direct Agent() call above.

Per-stage list (which questions a stage raises, and how deep)
--------------------------------------------------------------

Spine folder names are the intervention's `0-lifecycle/` stage folders (dual-2 numbering mirrors paper: 2-venue + 2-pitch).
A section's `serves:` field is what binds it to a stage — never its path. All probe files live FLAT in `1-probes/`, one cross-stage pool.

- **0-seed** (venue-FREE) — DEFAULT RUN for a new seed: landscape / prior interventions / benchmarks / cohort sanity, to sharpen the seed question. Mostly discovery-shaped. No venue pinned yet: source anchors stay in the section's `reading`; no citation/display lanes.
- **1-claims** (venue-FREE) — the core evidence stage; one question per GAP claim. The `reading` feeds the claim, and the CLAIM'S STATUS FLIPS IN `1-claims.md` (`supported | refuted | inconclusive` + confidence + claim_type + G1/G2/G3). There is no `## Verdict` block and no `verdicted` state — both are DELETED. Verified numbers land in `_VALUES_1-claims.md` (values lane fires here even pre-pin).
- **2-venue** — venue-level questions: channel capability, compliance constraints, prior sends on this channel.
- **2-pitch** — rare: anchor evidence for the theory of change if the ledger lacks it.
- **3-narrative** — rarely fires; a beat exposing a NEW evidence gap becomes a `serves: 1-claims` section, never gathers here.
- **4-display** (venue-GATED: dashboard/ui-card/report; optional email; skipped sms/push/reminder/checklist) — display lane. Unit GENERATION is commissioned like any other question: a section whose commission asks for a unit that does not exist dispatches to the task orchestrator; the hook only LINKS what landed into `_DISPLAY_4-display.md` + the artifact.
- **5-section-edit** (sectioned venues only) — full document probe: values + citation lanes per section, display lane where the section references units.

Dispatch rules
---------------

1. **CHEAPEST DOOR FIRST — and most sections should never reach an agent.** Walk the cost ladder in order: T0 JOIN (another stage already asks this — add my `serves:`) · T1 LOCAL (my own registries answer it — `answered-local`) · T2 REUSE (an existing QA file answers it — point the section) · T3 ENRICH (the leaf exists, was never asked this) · T4 FRESH (no leaf). **Only T3/T4 summon an agent.** The bank fills AUTONOMOUSLY from executor sessions (R17), so in a healthy project most answers exist before anyone asks: a commission is the EXCEPTION, not the norm. A probe file whose every section is T3/T4 is a smell — say so.
2. **MATCH ON THE ANSWER, NEVER ON THE TOPIC (R14).** A QA file counts as a hit only if it LITERALLY ANSWERS the question. Two leaves that both "characterize the cohort" can hold zero overlapping facts. READ the QA file. Topic similarity is not evidence — if it does not answer the question, it is a T3 ENRICH: dispatch it, do not point at it.
3. **The DEPTH is the executor's private business (R15).** Read / new run / new script / new leaf — the executor picks the shallowest that answers the question. This worker never learns which, and never asks. It hands a question and gets back a QA-file path.
4. **Background the fresh work.** Likely-fresh dispatches (a new search, a landscape, a task run) always carry `run_in_background=true`; a sync fresh run froze a session 25 minutes. If `<project_root>/discoveries/` is empty, EVERY question is T4 — background them all. The label in the reply must match the call.

Seed specifics (DEFAULT RUN for a new seed)
--------------------------------------------

Skip only on re-entry or minor edits, and only by an explicit logged verdict (`[PROBE] skipped -- <reason>` in the stage `_LOG`; phase line shows `--`) — never silently. The seed question needs outside context, not settled claims:

```
landscape ("what does this space look like?")   -> discovery orchestrator -> landscape.md -> QA/
prior interventions ("who has tried this?")     -> discovery orchestrator -> sources.md   -> QA/
cohort sanity ("does the population exist?")    -> task orchestrator      -> results/     -> QA/
```

The `reading` of each section feeds the opportunity, the mechanism hypothesis, and the kill criteria in `0-seed.md`. The evidence itself stays project-side, reusable by claims — and by every sibling consumer.

Claims specifics (the core evidence stage)
-------------------------------------------

Every GAP/weak claim raises a question. MATCH first (the ladder above), then dispatch what is left:

```
the claim needs a run / data artifact       -> Agent(haipipe-task-orchestrator-agent)
the claim needs outside context / benchmarks-> Agent(haipipe-discovery-orchestrator-agent)
the answer already exists in the bank       -> T2: point target: at the QA file. Nothing runs.
```

At INTERPRET, the `reading` lands in the section and the claims ledger flips in the SAME pass — the C-line AND its Evidence Campaign row, in `0-lifecycle/1-claims/1-claims.md`. **That file is where a claim's status lives.** The probe file holds the evidence's MEANING for this intervention; it does not hold a verdict, because "verdict" is not a probe field any more.

The intervention owns the CLAIM. The executor owns the FACT. The probe file is the only document that speaks both.

Venue-scaled lane rules (which lanes exist, decided at lane CREATION)
----------------------------------------------------------------------

- `values:` — always eligible, every venue: quoted numbers trace to task results.
- `sources:` — sectioned venues only (report/dashboard-like, per the venue profile); never before a sectioned venue is pinned. Pre-pin, source anchors live in the section's `reading`.
- `displays:` — only if the venue's artifact has display units (panels, charts, figures).
- Simple venues (sms/push/reminder): no document lanes; PROBE is claims-evidence only.
- The checker (`check-probe-cards.sh`) is presence-driven — it FAILs OWED lane lines and scans the working docs that exist; venue-scaling lives here, at creation, not in the checker.

Phase status (derive from disk)
--------------------------------

```
probe ✅    every section for the 🔥 stage is read (or answered-local), the ledger is
            backfilled, no OWED lanes, no overdue commissioned section
probe 🚀    sections commissioned, answers pending (a FUTURE-eta build is HONEST here)
probe ⬜    questions raised, nothing matched or dispatched
probe --    skipped (stage raised no questions; logged in _LOG)
```

Strip form: `phase:   draft ✅  │  probe 🔥🚀  │  revise ⬜  │  check ⬜`. Sectioned venues may split the fired lanes when section-edit runs them:

```
phase:   draft ✅  │  probe: val 🚀  cite ⬜  disp --  │  revise ⬜  │  check ⬜
```

GATE RULE (JL 2026-07-07): the probe phase may NOT show ✅ while any lane is OWED, any section is
`planned`, or any `commissioned` section is OVERDUE. `probe ✅ (cite ⬜ ...)` on a sectioned venue
is a contradiction: run `check-probe-cards.sh` — it FAILs.
