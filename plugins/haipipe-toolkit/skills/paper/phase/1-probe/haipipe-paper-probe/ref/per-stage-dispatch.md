Per-stage dispatch reference (haipipe-paper-probe)
====================================================

Loaded on demand from SKILL.md. Which stage runs which workers, stage
specifics, section-edit worker logic, and phase-status strip forms.

Where a dispatched question goes
---------------------------------
This worker owns the paper side of the question. The EXECUTOR owns the work:

```
the entries still owed after ② MATCH, handed as a SET
        |
        +-- Agent(haipipe-probe-q-executor-agent)         isolated stake-free collector
              |
              +-- Agent(haipipe-task-orchestrator-agent)        internal work
              +-- Agent(haipipe-discovery-orchestrator-agent)   external evidence
                  The collector sends each `### q-executor` VERBATIM according
                  to the authoritative route settled at ② MATCH.
        |
        +-- on return, this worker writes NOTHING bank-side:
              the entry's `### a-executor` copies the answer in, and each Q-consumer's
              a-consumer (in its stage doc) is the paper's record of what the answer
              MEANS; the CLAIM's status lives in 0-lifecycle/1-work/S-Work-1-claims.md.
              The reusable artifact is the EXECUTOR's <task-folder>/QA/<n>-<slug>.md,
              which any paper's PROBE-time MATCH can find and read (`bank: reuse`).
```

Per-stage table (workers = HARVESTERS: they transcribe landed evidence, never
acquire; acquisition is always a question ENTRY -> its `### q-executor` -> the
task/discovery orchestrator -> the answering QA file)
----------------
- **seed** (-> discovery): landscape / related work / novelty to sharpen the seed question; returned source anchors stay in the ENTRY's `### a-executor`.
- **resource** (-> task + discovery): DRAFT asks Qs keyed to N rows on `S-Work-0-resources.md`; PROBE opens and MATCHes one entry per Q, writes the `-> PP<NN>` backlink, and dispatches only within `--depth`. `task-for-fit` and `task-for-eval` are Claims work.
- **claims** (-> task + discovery): one question entry per GAP claim. The author writes claim status in `S-Work-1-claims.md`; CHECK reviews the paper judgment. Claims consumes only Resource-declined forward pointers recorded in that S page's `## Log`.
- **pitch** -- anchor-paper questions (-> discovery).
- **narrative** -- anchor-paper and display-need questions, one per beat.
- **display** -- from SECTION/NARRATIVE context a missing unit is NEVER commissioned: it becomes a DR row in `0-lifecycle/3-display/_DISPLAY_REQUEST.md` (the display stage's inbox) and the ENTRY closes `answered-local`, with each Q-consumer's a-consumer in its stage doc reading `rerouted to display stage: DRNN`. Only the DISPLAY STAGE itself commissions evidence/render work for its accepted units; ⑤ LINKs existing/done units.
- **section-edit** -- full document probe: citation, value, and display-need questions together.
  (A DR request pending in the 4-display inbox is 📨; the display axis cannot pass
   CHECK until the row is `done` and the unit linked.)

Dispatch rules (apply to every dispatch)
----------------------------------------------
1. **Reuse-before-create -- the MATCH is PROBE's, the DEPTH is the EXECUTOR's.**
   PROBE runs ② MATCH over the
   bank's READABLE QA corpus (`{tasks,discoveries}/**/QA/*.md`) and READS the
   hits -- match ON THE ANSWER, never on the topic. A hit is `bank: reuse`
   (point the entry's `target` at that QA file; nothing runs). Only what MATCH
   cannot close is dispatched by this worker, and then the EXECUTOR picks the shallowest depth
   in its own clean context (read | new run | new script | new task-folder) -- the worker
   never learns which, and never asks. MOST ENTRIES SHOULD LAND ON `reuse`: the bank
   fills autonomously from the executor side, so a dispatch is the EXCEPTION.
   Duplication is a mental-model tax: two half-overlapping evidence sets cost more
   than one enriched one.

Seed specifics (DEFAULT RUN for a new seed)
---------------------------------------------
Skip only on re-entry or minor edits, and only by an explicit logged verdict
(`[PROBE] skipped -- <reason>` in the S page's `## Log`; phase line shows `--`) --
never silently. The seed question needs outside context, not settled claims:

```
landscape ("what does this field look like?")  -> discovery Review -> landscape.md
related work ("who has done this?")            -> discovery Search -> sources.md
novelty ("is this idea new?")                  -> discovery novelty-check -> verdict.md
(all three via the q-executor collector to Agent(haipipe-discovery-orchestrator-agent); the task-folder's readable
 digest of each is its QA/<n>-<slug>.md, and that is what the entry points at)
```

The **a-consumer** (in S-Seed-0-seed.md) feeds Motivations and Tentative Claim Shape. Source anchors
the answer brought back stay in the ENTRY's `### a-executor` so the user can eyeball them
paper-side. Full evidence stays executor-side, reusable by claims.
NOTE: a discovery leaf's own `verdict.md` is executor-native and SURVIVES; it is a
different thing: it belongs to the bank, not to the probe layer.)

Resource specifics (SCAN and BUILD lanes)
-------------------------------------------
The stage hands over paper-space QUESTIONS, never PP ids or probe topics. PROBE
reads `S-Work-0-resources.md`, opens one entry per Q, writes the q-consumer,
bank binding, blocks field, q-executor, and `-> PP<NN>` backlink. Its ② MATCH
settles what the bank already answers; ③ dispatches only within `--depth`, and
⑤ writes the answer back as the Q's **A**. A BUILD lands a committed answer that flips
a demand row; a SCAN only needs orientation.

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
       it may NOT consume it without the user's explicit cross-project decision)
    HARD RULE: a SCAN question whose route exceeds ~1 HOUR is MISFILED.
    Re-route it to BUILD, or shrink the question until it fits the hour.

BUILD -- days to weeks. NON-BLOCKING, ALWAYS.
    task-for-data / task-for-algo   (ingredients; task-for-fit is claims' now)
    LONG ACQUISITIONS (a DUA or IRB application -- an ETA in MONTHS, a CALENDAR
      cost, not a compute cost)
    The ENTRY carries (BUILD-lane fields, only at state: commissioned):
        state: commissioned
        owner: <name>
        eta: YYYY-MM-DD
        blocks: N<n>
        cross-project: <path | none-found>     MANDATORY -- empty is a FAIL
```

FORBIDDEN in resource: **`task-for-fit`** and **`task-for-eval`**. Those are CLAIMS
(training and evaluating are the experiment). An entry whose `### q-executor` is fit- or
eval-shaped while its Q-consumer serves resource is mis-scoped by definition --
a bundled fit+eval entangles the
judgment (Paper-CGMtoAge's PP04: you cannot tell whether the null came from the
MODEL or from the CORPUS).

Resource is a ledger doc with exactly two sections (Demand + Questions), and no
display units. The Q's **A** IS the settled record. Access-rung and prior-art SCANs
route through discovery; their return is transcribed into the A.

Claims specifics
-----------------
Every GAP/weak claim raises one question ENTRY -- PROBE MATCHes first
(reuse-before-create), then the ones left `run`/`code`/`new` fan out by shape:

```
claim needs its status settled     -> an ENTRY whose `### q-executor` is task-shaped
                                      -> collector -> Agent(haipipe-task-orchestrator-agent)
question needs a run / artifact    -> same door (the executor picks the depth)
question needs outside context     -> collector -> Agent(haipipe-discovery-orchestrator-agent)
settled claim status               -> 0-lifecycle/1-work/S-Work-1-claims.md (the ONLY home
                                      of a claim's status; the probe entry carries
                                      only its `### a-executor`)
```

At ⑤ INTERPRET the entry's `### a-executor` is copied in and each Q-consumer's a-consumer
lands (station ②), and the CLAIM's status is written in S-Work-1-claims.md (supported |
refuted | inconclusive + confidence + claim_type), citing the entry's `target` QA file.
The paper owns the NEED and the JUDGMENT; the executor owns the FACT.
See the Evidence Routing Protocol + Delivery Need Routing sections in ../../../../haipipe-paper/SKILL.md.

Phase status (derive from disk)
--------------------------------
```
probe ⬜  no entry in 1-probes/ serves this stage
probe 🚀  entries exist, at least one not yet `read`
probe ✅  every entry serving this stage is `read` or `answered-local`
probe --  skipped (logged verdict required)
```

Strip form:

```
phase:   draft ✅  │  probe 🔥🚀  │  revise ⬜  │  check ⬜
```

GATE RULE: the probe phase may NOT show ✅ over a `check-probe-cards.sh` FAIL.
Derive the status from the checker, never from a stored value or an eyeball.
