# Application Design Philosophy

An intervention is a delivery contract, not a drafting folder.

Tasks run code. Probes judge claims. Discoveries inspect outside evidence. The application sits downstream and asks: which judged evidence does this intervention select, and how does it become a deployable artifact for THIS venue and THIS audience?

## Lifecycle

```text
enter > 0-seed > 1-claims > [venue] > 2-pitch > 3-narrative° > 4-display° > 5-section-edit°
        > draft(artifact) > review > deploy > round/iterate          (° = venue-gated)
```

All stages are markdown (argument documents need no compilation). Each stage answers one question:

| Stage | Question |
|---|---|
| 0-seed | Why might this intervention work? |
| 1-claims | What must be true, and which PP verdicts settle it? (venue-FREE) |
| 2-pitch | What is this intervention selling? (one minute, to the pinned venue + audience) |
| 3-narrative | How do claims compose into the output's arc? |
| 4-display | What content element carries each claim, and what job does each unit do? |
| 5-section-edit | Does each section's prose do its job? (per-section DRAFT-PROBE-REVISE-CHECK) |

Two axes stay orthogonal: **layer/frontier** (which stage has the active work) and **maturity** (how real the intervention is: prospect, drafted, deployed, iterating, retired).

The venue (output modality) gates stages 3-5 and sets the claims SETTLEMENT depth; the audience shapes tone within that structure. Simple venues (sms/push/reminder) run seed > claims > venue > pitch > draft. `review` is the gate that decides which earlier stage is broken.

## Venue coupling

Seed and claims are venue-FREE: the ledger's truth does not change when the channel changes. Venue pins the modality in STATUS.md between claims and pitch and writes the venue stage doc `0-lifecycle/2-venue/2-venue.md`, whose Artifact Principles are the downstream contract the venue-ALIGNED stages read. Pitch, narrative, display, and section-edit are venue-ALIGNED: they rewrite on retarget. Retargeting sms -> dashboard keeps the claims ledger and deepens its required settlement; it never invalidates it.

## Evidence routing

For claim-related evidence, the application RAISES QUESTIONS. A stage's DRAFT raises them; the PROBE phase collects them into probe files (`1-probes/PPNN_<topic>.md`, one file per topic, one SECTION per question), MATCHes each against the answers the bank already holds, and COMMISSIONS only what is missing — straight to the task/discovery orchestrators. Direct task/discover for non-claim utility work only.

The application does not execute code, search literature directly, or store raw results. **It never writes in the bank at all** (LAW 1: a consumer session never executes task/discovery work inline).

## Boundaries

```text
task        executes internal work            ─┐ the two EXECUTORS. Same shape, same rules.
discovery   checks outside evidence           ─┘ Both PROBE-UNAWARE: they answer plain
                                                 questions through their own `qa` verb and
                                                 write the answer as <task-folder>/QA/<n>-<slug>.md
probe       the application-level Q/A MAP: it binds each question to a QA file by PATH.
            It JUDGES NOTHING — a claim's status lives in 1-claims.md, per-consumer,
            private. ("Verdict" is retired as a probe field.)
application selects evidence, shapes it for a venue + audience, delivers, iterates
```

The probe CAUSES a QA file to exist; the EXECUTOR AUTHORS it. That one hop is the wall: it is
what keeps the evidence REUSABLE (a fact written in general language serves every consumer)
instead of consumer-shaped (a fact written around one intervention's claims serves only it).

## Intervention Console

`/haipipe-application` inside an intervention opens the Intervention Console: a context-aware working session for one active intervention. The console resolves the root, derives current state from disk (not stored status), renders a dashboard, records session state in `.intervention-console.yaml`, and routes follow-up input through the lifecycle.

## Copilot policy

Auto: read files, summarize status, classify input, draft stage docs, detect open needs.

Ask first: costly task/PHI work, claim verdicts, deploy to a live channel, opening/closing rounds.

## Folder model

```text
STATUS.md                     0-lifecycle/{0..5}/
0-sections/ (sectioned venues) 0-artifacts/<slug>-v{N}.md
1-probes/PPNN_<topic>.md      1-rounds/vYYMMDD/
data/contract.yaml
```

`0-` = source of truth. `1-` = process.

## Design prompt

Use this when revising or implementing the application skill:

```text
You are designing the haipipe-application layer.

Treat an intervention as a delivery contract, not a drafting folder.
The intervention lifecycle is the stage spine:
0-seed > 1-claims > [venue] > 2-pitch > 3-narrative > 4-display > 5-section-edit,
then draft(artifact) > review > deploy > round/iterate.
The venue gates stages 3-5 and sets claims settlement depth; seed and
claims are venue-FREE and survive retargeting.

For each lifecycle stage, specify: what question it answers, which skill
procedure owns it, which files it reads/writes, whether it calls
task/probe/discovery, what artifact it produces, what machine state
it updates, and when it must stop and ask the user.

Keep the intervention folder fixed:
STATUS.md, 0-lifecycle/<stage>/<stage>.md (+ _LOG), 0-sections/,
0-artifacts/<slug>-v{N}.md, 1-probes/PPNN_<topic>.md,
1-rounds/vYYMMDD/{README,discussion,decisions,todo,applied}.md.

Preserve boundaries:
- for claim-related evidence, the application RAISES QUESTIONS; the PROBE phase
  matches them against the bank and commissions only what is missing, straight
  to the task/discovery orchestrators; direct task/discover for non-claim only
- a stage's DRAFT raises the questions; the PROBE phase binds each to a QA file
- the application does not execute code, search literature, or store raw results,
  and NEVER writes under tasks/ or discoveries/
```
