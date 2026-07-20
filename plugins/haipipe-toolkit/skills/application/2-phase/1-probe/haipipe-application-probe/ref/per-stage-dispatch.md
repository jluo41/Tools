Per-stage dispatch reference (haipipe-application-probe)
==========================================================

Loaded on demand from SKILL.md.
Which rung runs which lanes, seed/claims specifics, venue-scaled lane rules, and phase-status strip forms.
The MODEL — the five-step loop, the cost ladder, the states — belongs to `probe` (`../../../../probe/haipipe-probe/SKILL.md`); this file is the application-side per-rung detail.

Where a dispatched question goes
---------------------------------
This worker owns the intervention side of the question.
The collector agent owns the middle; the EXECUTOR owns the work:

```
the entry's `### q-executor` block, VERBATIM
        |
        +-- Agent(haipipe-probe-q-executor-agent)   runs ③④ in clean context (DRAFT already MATCHed):
        |       +-- Agent(haipipe-task-orchestrator-agent)        internal work (data, eval, display, stata, …)
        |       +-- Agent(haipipe-discovery-orchestrator-agent)   external evidence: search + read, judge, idea
        |     it returns { entry → target: QA-path }, having written each target:.
        |
        +-- on return, this worker writes NOTHING project-side:
              the entry's `### a-executor` is the copy of the answer, and each Q-consumer writes
              its own a-consumer in its stage doc; a CLAIM's status lives in
              0-lifecycle/1c-claims/1c-claims.md, never in the probe file.
              The reusable artifact is the EXECUTOR's <task-folder>/QA/<n>-<slug>.md,
              which any consumer's MATCH can find and read (T2 REUSE).
```

Per-rung list (harvest is TRANSCRIPTION: landed evidence folds into the entry's `### a-executor`, never acquired; acquisition is always a question ENTRY → its `### q-executor` → the collector → the answering QA file)
----------------
Spine folder names are the intervention's `0-lifecycle/` stage folders (dual-2 numbering mirrors paper: 2-venue + 2-pitch).

- **0-seed** (venue-FREE) — (→ discovery), DEFAULT RUN for a new seed: landscape / prior interventions / benchmarks / cohort sanity to sharpen the seed question. No venue pinned yet, so source anchors stay in the entry's `### a-executor`; no citation/display lanes.
- **1a-descriptions** (venue-FREE, ladder rung) — (→ task): data-profile questions ("profile the cohort", "pull engagement summary"). The answer's numbers land INLINE in the entry's `### a-executor` (anchored to target:); the 1a doc keeps one-line Description entries. Consumes seed's FORWARD pointers at DRAFT.
- **1b-themes** (venue-FREE, ladder rung) — (→ discovery; task for quick in-data confirmations): field-pattern questions ("what messaging levers does the literature name?"); the answer's grounding refs land in the entry's `### a-executor`, feeding the T entries.
- **1c-claims** (venue-FREE, ladder rung) — (→ task + discovery): the core evidence rung; one question ENTRY per GAP claim. An entry's answer is read by the author, who writes the claim status into `0-lifecycle/1c-claims/1c-claims.md` — the ONLY home of a claim's status, flipping the C-line AND the Evidence Campaign row in the same pass. Verified numbers land INLINE in the entry's `### a-executor` (anchored to target:), even pre-pin.
- **1d-advice** (venue-FREE, ladder rung) — rarely fires: derivation is in-stage work; an advice entry exposing a NEW evidence gap routes back as a `1c-claims` question ENTRY, never gathers here.
- **2-venue** — venue-level questions: channel capability, compliance constraints, prior sends on this channel.
- **2-pitch** — rare: anchor evidence for the theory of change if the ledger lacks it.
- **3-narrative** — rarely fires; a beat exposing a NEW evidence gap routes back to claims, never gathers here.
- **4-display** (venue-GATED: dashboard/ui-card/report; optional email; skipped sms/push/reminder/checklist) — display needs. A missing unit is NEVER commissioned from narrative/section context: it becomes a request row in the display stage's inbox and the entry closes `answered-local`. Only the DISPLAY STAGE itself commissions render work for its accepted units; the harvest LINKs what landed.
- **5-section-edit** (sectioned venues only) — full document probe: one ENTRY per evidence need; the answer's numbers/citations fold INLINE into its `### a-executor`, and a referenced display unit that does not exist reroutes to the display stage.

Dispatch rules (apply to every dispatch)
----------------------------------------------
1. **Reuse-before-create — the MATCH is DRAFT's, the DEPTH is the EXECUTOR's.** DRAFT runs ② MATCH over the bank's READABLE QA corpus (`{tasks,discoveries}/**/QA/*.md`) and READS the hits — match ON THE ANSWER, never on the topic. A hit is a T2 REUSE (`bank: reuse`; point the entry's `target:` at that QA file; nothing runs). Only what MATCH cannot close carries a `NEW` target into ③ DISPATCH, and then the EXECUTOR picks the shallowest depth in its own clean context. MOST ENTRIES SHOULD LAND ON T2: the bank fills autonomously from the executor side, so a fresh q-executor is the EXCEPTION.

Seed specifics (DEFAULT RUN for a new seed)
---------------------------------------------
Skip only on re-entry or minor edits, and only by an explicit logged note (`[PROBE] skipped — <reason>` in the stage _LOG; phase line shows `--`) — never silently.
The seed question needs outside context, not settled claims:

```
landscape ("what does this space look like?")   → route: discovery → landscape.md
prior interventions ("who has tried this?")     → route: discovery → sources.md
cohort sanity ("does the population exist?")    → route: task (quick data probe)
```

The a-consumer (in 0-seed.md) feeds the opportunity, mechanism hypothesis, and kill criteria.
Full evidence stays executor-side, reusable by claims.

Claims specifics (rung 1c)
---------------------------
Every GAP/weak claim raises one question ENTRY — MATCH first at DRAFT (reuse-before-create), then the unmatched ones fan out by shape:

```
claim needs its status settled     → an ENTRY whose q-executor is task-shaped → route: task
question needs a run / artifact     → same door (the executor picks the depth)
question needs outside context      → route: discovery
settled claim status                → 0-lifecycle/1c-claims/1c-claims.md (the ONLY home of a claim's
                                       status; the probe entry carries only its `### a-executor`)
```

At ⑤ INTERPRET the answer lands in the entry's `### a-executor` (and each Q-consumer's a-consumer in its stage doc), and the CLAIM's status is written in 1c-claims.md (supported | refuted | inconclusive + confidence), flipping the C-line and the Evidence Campaign row, citing the entry's `target:` QA file.
The intervention owns the NEED and the JUDGMENT; the executor owns the FACT.
The venue gate later evaluates its settlement bar (light | medium | full) against the campaign table and through 1d's derivations.

Harvest — no sidecar
----------------------------------------------------------------------
Every answer's numbers/citations land INLINE in the entry's `### a-executor`, anchored to `target:`
(the answering QA file, already verified) — any venue. No harvest lanes and no sidecar docs.
The checker verifies `target:` is `answered` + non-superseded; there is nothing else to harvest-check.

Section-edit worker logic
--------------------------
Read the section outline; for each evidence need raise a question ENTRY whose answer's numbers/citations land inline in its `### a-executor` (anchored to target:). No lanes.

Phase status (derive from disk)
--------------------------------
```
probe ✅    all sections for the 🔥 stage are read, ledger backfilled
probe 🚀    sections dispatched, returns pending
probe ⬜    questions recorded, nothing dispatched
probe --    skipped (stage had no evidence needs; logged in _LOG)
```

Strip form: `phase:   draft ✅  │  probe 🔥🚀  │  revise ⬜  │  check ⬜`.

GATE RULE: the probe phase may NOT show ✅ while any entry is `planned` or has an unresolved `target:` — run check-probe-cards.sh, it FAILs.
