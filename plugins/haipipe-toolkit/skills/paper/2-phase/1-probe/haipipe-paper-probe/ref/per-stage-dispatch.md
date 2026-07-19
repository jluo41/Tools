Per-stage dispatch reference (haipipe-paper-probe)
====================================================

Loaded on demand from SKILL.md. Which stage runs which workers/mode, stage
specifics, section-edit worker logic, and phase-status strip forms.

Where a dispatched question goes
---------------------------------
This worker owns the paper side of the question. The EXECUTOR owns the work:

```
the section's `q-executor:` block, VERBATIM
        |
        +-- Agent(haipipe-task-orchestrator-agent)        internal work: 9 task domains
        |                                                 (data, nn, end, individual, fit,
        |                                                  eval, display, stata, agent)
        +-- Agent(haipipe-discovery-orchestrator-agent)   external evidence: search + read,
        |                                                 judge/synthesize, idea
        |     The SWEEP is ② MATCH, and dispatch goes DIRECT to the two
        |        orchestrators above.
        |
        +-- on return, this worker writes NOTHING project-side:
              the section's `a-consumer:` is the paper's record of what the answer
              MEANS; the CLAIM's status lives in 0-lifecycle/1b-claims/1b-claims.md.
              The reusable artifact is the EXECUTOR's <task-folder>/QA/<n>-<slug>.md,
              which any paper's MATCH can find and read (T2 REUSE).
```

Per-stage table (workers = HARVESTERS: they transcribe landed evidence, never
acquire; acquisition is always a question SECTION -> its `q-executor:` -> the
task/discovery orchestrator -> the answering QA file)
----------------
- **seed** -- probe mode light (-> discovery): landscape / related work / novelty to sharpen the seed question; returned sources HARVEST into _CITATION_0-seed.md. No values/display lanes.
- **resource** -- probe mode light for SCAN questions, FULL for BUILD questions (-> task + discovery): the prerequisite stage (`what must EXIST for this paper to be testable, does it exist, can it CARRY the claim?`). The stage ASKS (Q\<n\>, keyed to a demand row N\<n\>); THIS WORKER's ① ORGANIZE stage intake opens one SECTION per approved Q and writes the `-> PP<NN>` backlink into 1a-resource.md; ② MATCH then resolves it against the bank, and only an unmatched section is DISPATCHED to the task/discovery orchestrator, which picks the shape and depth in its own clean context. Two lanes, SCAN (blocking) and BUILD (non-blocking) -- see Resource specifics. `task-for-fit` and `task-for-eval` are FORBIDDEN here -- training and evaluating are claims' (resource stops at "do the ingredients exist and can they carry the claim?"). NO harvest lanes at all (see below).
- **claims** -- probe mode FULL (-> task + discovery): the core evidence stage; one question SECTION per GAP claim. A full-mode section's answer is read by the author, who writes the claim status into `0-lifecycle/1b-claims/1b-claims.md` — the ONLY home of a claim's status (there is no review gate; a probe is communication, not judgment). `## Verdict` and `verdicted` are DELETED. Claims does NOT consume seed's `[FORWARD -> ...]` pointers — RESOURCE is their sole consumer; claims only picks up the ones resource explicitly DECLINED to it (per `_LOG_1a-resource.md`).
- **pitch** -- citation lane only (anchor papers).
- **narrative** -- citation + display lanes (beats map to displays).
- **display** -- display lane. From SECTION/NARRATIVE context a missing unit is NEVER commissioned: it becomes a DR row in `0-lifecycle/4-display/_DISPLAY_REQUEST.md` (the display stage's inbox; JL 2026-07-10) and the SECTION closes `answered-local` with the a-consumer `rerouted to display stage: DRNN`. Only the DISPLAY STAGE itself commissions evidence/render work for its accepted units (via its own PROBE lanes); the harvester LINKs existing/done units.
- **section-edit** -- full document probe: citation + values + display lanes.
  (disp statuses include 📨 = DR request pending in the 4-display inbox; the
   display axis cannot pass CHECK until the row is `done` and the unit linked.)

Dispatch rules (both apply to every dispatch)
----------------------------------------------
1. **Mode: light by default.** A light probe stops at Read and returns evidence
   to the caller -- right for context questions (seed landscape, section-edit
   lookups). Request `mode: full` only when the paper needs a COMMITTED claim
   status: the author reads the answer and writes the claim status into
   `0-lifecycle/1b-claims/1b-claims.md` (claims stage's normal case). Light can
   escalate to full later; never start heavy for a question that
   only needs orientation.
2. **Reuse-before-create -- the MATCH is the WORKER's, the DEPTH is the EXECUTOR's.**
   The worker itself runs ② MATCH over the
   bank's READABLE QA corpus (`{tasks,discoveries}/**/QA/*.md`) and READS the
   hits -- R14: match ON THE ANSWER, never on the topic. A hit is a T2 REUSE
   (point the section's `target:` at that QA file; nothing runs). Only what MATCH
   cannot close is dispatched, and then the EXECUTOR picks the shallowest depth
   in its own clean context (read | new run | new script | new task-folder) -- the worker
   never learns which, and never asks. MOST SECTIONS SHOULD LAND ON T2: the bank
   fills autonomously from the executor side, so a q-executor is the EXCEPTION.
   Duplication is a mental-model tax: two half-overlapping evidence sets cost more
   than one enriched one.

Seed specifics (mode light; DEFAULT RUN for a new seed)
--------------------------------------------------------
Skip only on re-entry or minor edits, and only by an explicit logged verdict
(`[PROBE] skipped -- <reason>` in the stage _LOG; phase line shows `--`) --
never silently. The seed question needs outside context, not settled claims:

```
landscape ("what does this field look like?")  -> discovery Review -> landscape.md
related work ("who has done this?")            -> discovery Search -> sources.md
novelty ("is this idea new?")                  -> discovery novelty-check -> verdict.md
(all three via Agent(haipipe-discovery-orchestrator-agent); the task-folder's readable
 digest of each is its QA/<n>-<slug>.md, and that is what the section points at)
```

The `a-consumer:` feeds Motivations and Tentative Claim Shape in 0-seed.md. Sources the
answer brought back HARVEST into _CITATION_0-seed.md (candidates only) so the user
can eyeball them paper-side. Full evidence stays executor-side, reusable by claims.
(_DISCOVERY_{stage}.md is retired -- the probe SECTION carries the a-consumer.)
NOTE: a discovery leaf's own `verdict.md` is executor-native and SURVIVES; it is a
different thing from the deleted probe `## Verdict`.)

Resource specifics (mode light for SCAN, full for BUILD)
---------------------------------------------------------
The stage hands over paper-space QUESTIONS (Q1, Q2, ...), never PP ids and never
probe topics. THIS WORKER reads 1a-resource.md at ① ORGANIZE and opens one SECTION
per GATE-1-approved Q (`serves: resource` · `blocks: N<n>` · `target: NEW ?` ·
`state: planned` · `q-executor:` = the Q re-posed as a self-contained evidence
question), writing the `-> PP<NN>` backlink back into the Q -- the section can be
opened nowhere else, since the stage is forbidden to mint a PP id. ② MATCH then
resolves what the bank already answers; only the rest is DISPATCHED, and ⑤ INTERPRET
writes the answer back as the Q's **A**. A BUILD lands a committed answer that flips
a demand row, so it runs `mode: full`; a SCAN only needs orientation, so `mode: light`.

```
SCAN  -- minutes. GATE-BLOCKING. This is what makes the stage DECIDABLE.
    inventory / store scan            -> route: task
    capability grep                   -> route: task
      ("does code emitting metric X exist?" -- score a capability ONLY off a
       landed results/*/metrics.json KEY, never a filename match)
    access-rung / prior-art           -> route: discovery
      (rungs: PUBLIC | REGISTER | DUA | APPLICATION)
    cross-project sweep               -> route: discovery/task sweep
      (MATCH may NAME a sibling-project source as an UNREAD hypothesis;
       it may NOT consume it -- that is JL's decision at the DRAFT gate)
    HARD RULE: a SCAN question whose route exceeds ~1 HOUR is MISFILED.
    Re-route it to BUILD, or shrink the question until it fits the hour.

BUILD -- days to weeks. NON-BLOCKING, ALWAYS.
    task-for-data / task-for-algo   (ingredients; task-for-fit is claims' now)
    LONG ACQUISITIONS (a DUA or IRB application -- an ETA in MONTHS, a CALENDAR
      cost, not a compute cost)
    The SECTION carries (BUILD-lane fields, only at state: commissioned):
        state: commissioned
        owner: <name>
        eta: YYYY-MM-DD
        blocks: N<n>
        cross-project: <path | none-found>     MANDATORY -- empty is a FAIL
```

FORBIDDEN in resource: **`task-for-fit`** and **`task-for-eval`**. Those are CLAIMS
(training and evaluating are the experiment). A section whose q-executor is fit- or
eval-shaped while it `serves: resource` is mis-scoped by definition --
a bundled fit+eval entangles the
judgment (Paper-CGMtoAge's PP04: you cannot tell whether the null came from the
MODEL or from the CORPUS).

HARVEST LANES: **none**. Resource is a ledger doc with exactly two sections
(Demand + Questions), and it has NO sidecars by design -- no _CITATION_1a-resource.md,
no _VALUES_1a-resource.md, no display units. The Q's **A** IS the settled record.
So the harvest lanes never fire (no `sources:` / `values:` / `displays:` lane line is
written, and none is owed), and the phase strip reads `cite --  val --  disp --`.
Access-rung and prior-art SCANs still route through discovery; their return is
transcribed into the A, not into a _CITATION_ doc.

Claims specifics (mode full)
-----------------------------
Every GAP/weak claim raises one question SECTION -- MATCH first
(reuse-before-create), then the unmatched ones fan out by shape:

```
claim needs its status settled     -> a SECTION whose q-executor is task-shaped
                                      -> Agent(haipipe-task-orchestrator-agent)
question needs a run / artifact    -> same door (the executor picks the depth)
question needs outside context     -> Agent(haipipe-discovery-orchestrator-agent)
settled claim status               -> 0-lifecycle/1b-claims/1b-claims.md (the ONLY home
                                      of a claim's status; the probe section carries
                                      only its `a-consumer:`)
```

At ⑤ INTERPRET the section's `a-consumer:` lands, and the CLAIM's status is written in
1b-claims.md (supported | refuted | inconclusive + confidence + claim_type),
citing the section's `target:` QA file. The paper owns the NEED and the JUDGMENT; the
executor owns the FACT.
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
while any lane is OWED. A lane is OWED when a probe SECTION carries its lane line
with `harvest: OWED`, or when a return named harvestable content for a lane
whose doc (⬜) does not exist. `probe ✅ (cite ⬜ ...)` -- the exact strip the
incident shipped -- is a contradiction: run check-probe-cards.sh, it FAILs.
