Per-stage dispatch reference (haipipe-application-probe)
==========================================================

Loaded on demand from SKILL.md.
Which rung runs which mode and lanes, seed/claims specifics, venue-scaled lane rules, and phase-status strip forms.
The MODEL — the five-step loop, the cost ladder, the states — is the constitution's (`../../../../probe/haipipe-probe/SKILL.md`); this file is the application-side per-rung detail.

Where a dispatched question goes
---------------------------------
This worker owns the intervention side of the question.
The collector agent owns the middle; the EXECUTOR owns the work:

```
the section's `q-executor:` block, VERBATIM
        |
        +-- Agent(haipipe-probe-q-executor-agent)   runs ②③④ in clean context:
        |       +-- Agent(haipipe-task-orchestrator-agent)        internal work (data, eval, display, stata, …)
        |       +-- Agent(haipipe-discovery-orchestrator-agent)   external evidence: search + read, judge, idea
        |     it returns { section → tier, target: QA-path }, having written each target:.
        |
        +-- on return, this worker writes NOTHING project-side:
              the section's `a-consumer:` is the intervention's record of what the answer MEANS;
              a CLAIM's status lives in 0-lifecycle/1c-claims/1c-claims.md, never in the probe file.
              The reusable artifact is the EXECUTOR's <task-folder>/QA/<n>-<slug>.md,
              which any consumer's MATCH can find and read (T2 REUSE).
```

Per-rung list (lane hooks = HARVESTERS: they transcribe landed evidence, never acquire; acquisition is always a question SECTION → its q-executor → the collector → the answering QA file)
----------------
Spine folder names are the intervention's `0-lifecycle/` stage folders (dual-2 numbering mirrors paper: 2-venue + 2-pitch).

- **0-seed** (venue-FREE) — mode light (→ discovery), DEFAULT RUN for a new seed: landscape / prior interventions / benchmarks / cohort sanity to sharpen the seed question. No venue pinned yet, so source anchors stay in the section's a-consumer; no citation/display lanes.
- **1a-descriptions** (venue-FREE, ladder rung) — mode light (→ task): data-profile questions ("profile the cohort", "pull engagement summary"). The `values:` lane REDIRECTS here into `_DESCRIPTIONS/DS<n>_<name>.md` profile sheets (statistic + pointer + as-of date); the 1a doc itself keeps one-line D entries. Consumes seed's FORWARD pointers at DRAFT.
- **1b-themes** (venue-FREE, ladder rung) — mode light (→ discovery; task for quick in-data confirmations): field-pattern questions ("what messaging levers does the literature name?"); the a-consumer lands grounding refs onto T entries.
- **1c-claims** (venue-FREE, ladder rung) — mode FULL (→ task + discovery): the core evidence rung; one question SECTION per GAP claim. A full-mode section's answer is read by the author, who writes the claim status into `0-lifecycle/1c-claims/1c-claims.md` — the ONLY home of a claim's status, flipping the C-line AND the Evidence Campaign row in the same pass. The `values:` lane fires here even pre-pin (verified numbers land in `_VALUES_1c-claims.md`).
- **1d-advice** (venue-FREE, ladder rung) — rarely fires: derivation is in-stage work; an advice entry exposing a NEW evidence gap routes back as a `1c-claims` question SECTION, never gathers here.
- **2-venue** — mode light: venue-level questions — channel capability, compliance constraints, prior sends on this channel.
- **2-pitch** — light, rare: anchor evidence for the theory of change if the ledger lacks it.
- **3-narrative** — rarely fires; a beat exposing a NEW evidence gap routes back to claims, never gathers here.
- **4-display** (venue-GATED: dashboard/ui-card/report; optional email; skipped sms/push/reminder/checklist) — display lane. A missing unit is NEVER commissioned from narrative/section context: it becomes a request row in the display stage's inbox and the section closes `answered-local`. Only the DISPLAY STAGE itself commissions render work for its accepted units; the hook LINKs what landed.
- **5-section-edit** (sectioned venues only) — full document probe: values + citation lanes per section, display lane where the section references units.

Dispatch rules (both apply to every dispatch)
----------------------------------------------
1. **Mode: light by default; full for claims.** A light probe stops at Read and returns evidence to the caller — right for context questions (seed landscape, venue capability, section-edit lookups). Request `mode: full` only when the intervention needs a COMMITTED claim status that flips a campaign row (claims rung's normal case). Light can escalate to full later; never start heavy for a question that only needs orientation.
2. **Reuse-before-create — the MATCH is the WORKER's, the DEPTH is the EXECUTOR's.** The worker runs ② MATCH over the bank's READABLE QA corpus (`{tasks,discoveries}/**/QA/*.md`) and READS the hits — match ON THE ANSWER, never on the topic. A hit is a T2 REUSE (point the section's `target:` at that QA file; nothing runs). Only what MATCH cannot close is dispatched, and then the EXECUTOR picks the shallowest depth in its own clean context. MOST SECTIONS SHOULD LAND ON T2: the bank fills autonomously from the executor side, so a fresh q-executor is the EXCEPTION.

Seed specifics (mode light; DEFAULT RUN for a new seed)
--------------------------------------------------------
Skip only on re-entry or minor edits, and only by an explicit logged note (`[PROBE] skipped — <reason>` in the stage _LOG; phase line shows `--`) — never silently.
The seed question needs outside context, not settled claims:

```
landscape ("what does this space look like?")   → route: discovery → landscape.md
prior interventions ("who has tried this?")     → route: discovery → sources.md
cohort sanity ("does the population exist?")    → route: task (light data probe)
```

The `a-consumer:` feeds the opportunity, mechanism hypothesis, and kill criteria in 0-seed.md.
Full evidence stays executor-side, reusable by claims.

Claims specifics (rung 1c, mode full)
--------------------------------------
Every GAP/weak claim raises one question SECTION — MATCH first (reuse-before-create), then the unmatched ones fan out by shape:

```
claim needs its status settled     → a SECTION whose q-executor is task-shaped → route: task
question needs a run / artifact     → same door (the executor picks the depth)
question needs outside context      → route: discovery
settled claim status                → 0-lifecycle/1c-claims/1c-claims.md (the ONLY home of a claim's
                                       status; the probe section carries only its `a-consumer:`)
```

At ⑤ INTERPRET the section's `a-consumer:` lands, and the CLAIM's status is written in 1c-claims.md (supported | refuted | inconclusive + confidence), flipping the C-line and the Evidence Campaign row, citing the section's `target:` QA file.
The intervention owns the NEED and the JUDGMENT; the executor owns the FACT.
The venue gate later evaluates its settlement bar (light | medium | full) against the campaign table and through 1d's derivations.

Venue-scaled lane rules (which lanes exist, decided at lane CREATION)
----------------------------------------------------------------------
- `values:` — always eligible, every venue: quoted numbers trace to task results. (Rung 1a redirects this lane into `_DESCRIPTIONS/DS<n>` sheets.)
- `sources:` — sectioned venues only (report/dashboard-like, per the venue profile); never before a sectioned venue is pinned.
- `displays:` — only if the venue's artifact has display units (panels, charts, figures).
- Simple venues (sms/push/reminder): no document lanes; PROBE is claims-evidence only.
- The checker (`check-probe-cards.sh`) is presence-driven — it FAILs OWED lane lines and scans the working docs that exist; venue-scaling lives here, at creation, not in the checker.

Section-edit worker logic
--------------------------
Read the section outline and decide which lanes fire:
- **citation** — always (every section cites).
- **values** — when the outline contains numbers, statistics, or data references; skip for pure argumentative sections.
- **display** — when the outline references figures/tables/visuals; skip otherwise.

Phase status (derive from disk)
--------------------------------
```
probe ✅    all sections for the 🔥 stage are read, ledger backfilled, no OWED lanes
probe 🚀    sections dispatched, returns pending
probe ⬜    questions recorded, nothing dispatched
probe --    skipped (stage had no evidence needs; logged in _LOG)
```

Strip form: `phase:   draft ✅  │  probe 🔥🚀  │  revise ⬜  │  check ⬜`.
Sectioned venues may split the fired lanes when section-edit runs them:

```
phase:   draft ✅  │  probe: val 🚀  cite ⬜  disp --  │  revise ⬜  │  check ⬜
```

GATE RULE (paper seed incident, JL 2026-07-07): the probe phase may NOT show ✅ while any lane is OWED.
A lane is OWED when a section carries its lane line with `harvest: OWED`, or when a return named harvestable content for a fired lane whose doc (⬜) does not exist.
`probe ✅ (cite ⬜ …)` on a sectioned venue is a contradiction: run check-probe-cards.sh, it FAILs.
