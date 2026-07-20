# Application Design Philosophy

An intervention is a delivery contract, not a drafting folder.

Tasks run code. Probes judge claims. Discoveries inspect outside evidence. Insights preserve judged knowledge. The application sits downstream and asks: which judged evidence does this intervention select, and how does it become a deployable artifact for THIS venue and THIS audience?

## Lifecycle

```text
enter > 0-seed > [the evidence ladder: 1a-descriptions > 1b-themes > 1c-claims > 1d-advice]
        > [venue] > 2-pitch > 3-narrative° > 4-display° > 5-section-edit°
        > draft(artifact) > review > deploy > round/iterate          (° = venue-gated)
```

All stages are markdown (argument documents need no compilation). Each stage answers one question:

| Stage | Question |
|---|---|
| 0-seed | Why might this intervention work? |
| 1a-descriptions | What does the data look like, anchored and dated? (venue-FREE) |
| 1b-themes | Which patterns/topics emerge from the data and the field? (venue-FREE) |
| 1c-claims | Which claims generalize — supported, weak, GAP? (venue-FREE) |
| 1d-advice | Which design advice follow, each derived from a claim? (venue-FREE, the ladder's deliverable) |
| 2-pitch | What is this intervention selling? (one minute, to the pinned venue + audience) |
| 3-narrative | How do claims compose into the output's arc? |
| 4-display | What content element carries each claim, and what job does each unit do? |
| 5-section-edit | Does each section's prose do its job? (per-section DRAFT-PROBE-REVISE-CHECK) |

Stage 1 is the **evidence ladder** — Descriptions/Themes/Claims/Advice echo D→I→K→W. The manuscript form carries D/I in its own Methods/Results sections, so paper stops its stage 1 at claims (paper delivers K); an intervention artifact carries none of the ladder in its body and lives on dynamic data, so the application climbs one more rung to advice (application delivers W). Each rung is independently re-runnable: iterate's fresh A/B data backfills 1a, staleness tags propagate down the citation chain (A ← C ← T ← D), and only affected rungs reopen.

Two axes stay orthogonal: **layer/frontier** (which stage has the active work) and **maturity** (how real the intervention is: prospect, drafted, deployed, iterating, retired).

The venue (output modality) gates stages 3-5, sets the claims SETTLEMENT depth, and batches the ladder's gates (light venues: one combined gate at 1d); the audience shapes tone within that structure. Simple venues (sms/push/reminder) run seed > ladder > venue > pitch > draft. `review` is the gate that decides which earlier stage is broken.

## Venue coupling

Seed and the evidence ladder are venue-FREE: data truth, patterns, claims, and content-level design advice does not change when the channel changes. Venue pins the modality in STATUS.md between the ladder and pitch and writes the venue stage doc `0-lifecycle/2-venue/2-venue.md`, whose Artifact Principles are the downstream contract the venue-ALIGNED stages read (channel-HOW — distinct from 1d's design advice, which is content-WHAT). Pitch, narrative, display, and section-edit are venue-ALIGNED: they rewrite on retarget. Retargeting sms -> dashboard keeps the ladder and deepens its required settlement; it never invalidates it.

## Evidence routing

For claim-related evidence, the application always routes through probe (the single evidence door). Stages RAISE questions as entries in the flat pool `1-probes/PPNN_<topic>.md`, and each stage's PROBE phase worker binds every entry to a bank answer through the stake-free collector agent — never calling task/discover directly. Direct task/discover for non-claim utility work only.

The application does not execute code, search literature directly, or store raw results.

## Boundaries

```text
task        executes internal work
discovery   checks outside evidence
probe       binds each claim question to a bank answer (the single evidence door)
application selects evidence, climbs it to design advice (the ladder), shapes it
            for a venue + audience, delivers, iterates
```

## Intervention Console

`/haipipe-application` inside an intervention opens the Intervention Console: a context-aware working session for one active intervention. The console resolves the root, derives current state from disk (not stored status), renders a dashboard, records session state in `.intervention-console.yaml`, and routes follow-up input through the lifecycle.

## Copilot policy

Auto: read files, summarize status, classify input, draft stage docs, detect open needs.

Ask first: costly task/PHI work, claim status changes, deploy to a live channel, opening/closing rounds.

## Folder model

```text
STATUS.md                     0-lifecycle/{0..5}/
0-sections/ (sectioned venues) 0-artifacts/<slug>-v{N}.md
1-probes/                     1-rounds/vYYMMDD/
data/contract.yaml
```

`0-` = source of truth. `1-` = process.

## Design prompt

Use this when revising or implementing the application skill:

```text
You are designing the haipipe-application layer.

Treat an intervention as a delivery contract, not a drafting folder.
The intervention lifecycle is the stage spine:
0-seed > 1a-descriptions > 1b-themes > 1c-claims > 1d-advice > [venue]
> 2-pitch > 3-narrative > 4-display > 5-section-edit,
then draft(artifact) > review > deploy > round/iterate.
Stage 1 is the evidence ladder (echoes D->I->K->W; the deliverable rung is
1d: design advice derived from claims). The venue gates stages 3-5,
sets claims settlement depth, and batches the ladder's gates; seed and the
ladder are venue-FREE and survive retargeting.

For each lifecycle stage, specify: what question it answers, which skill
procedure owns it, which files it reads/writes, whether it calls
task/probe/discovery, what artifact it produces, what machine state
it updates, and when it must stop and ask the user.

Keep the intervention folder fixed:
STATUS.md, 0-lifecycle/<stage>/<stage>.md (+ _LOG; ladder rungs
1a-descriptions/ 1b-themes/ 1c-claims/ 1d-advice/ are stage folders like
any other), 0-sections/, 0-artifacts/<slug>-v{N}.md,
1-probes/,
1-rounds/vYYMMDD/{README,discussion,decisions,todo,applied}.md.

Preserve boundaries:
- for claim-related evidence, the application routes through probe (which
  calls task/discover during Gather); direct task/discover for non-claim only
- stages RAISE questions as entries in the flat pool 1-probes/, and the PROBE
  worker binds each to a bank answer via the stake-free collector agent
- the application does not execute code, search literature, or store raw results
```
