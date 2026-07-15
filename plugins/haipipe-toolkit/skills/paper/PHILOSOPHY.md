# Paper Design Philosophy

A paper is a delivery contract, not a writing folder.

Tasks run code. Discoveries inspect outside evidence. Both are EXECUTORS, and both answer a plain question through their own `qa` verb, returning `<task-folder>/QA/<n>-<slug>.md`. A PROBE is a PAPER-LEVEL document (`1-probes/PPNN_<topic>.md`) that binds each of the paper's questions to one of those answers BY PATH; the settled CLAIM STATUS lands in the paper's own `0-lifecycle/1-claims/1-claims.md`. The paper sits downstream and asks: which judged evidence does this paper select, and how does it become a submittable manuscript?

## Lifecycle

```text
enter > 0-seed > 1-resource > 1-claims > [venue] > 2-pitch > 3-narrative > 4-display
        > 5-section-edit > review > submit > round/respond > present
```

`1-resource` and `1-claims` share the number 1, deliberately, exactly as `2-venue` and `2-pitch` already do. The number is decoration; the spine key is the bare name `resource`, and `stage-strip.sh` strips the digit before matching. Nothing renumbers.

Early stages are markdown (argument documents need no compilation); display and section-edit carry tex. Each stage answers one question:

| Stage | Question |
|---|---|
| 0-seed | Why might this paper exist? |
| 1-resource | What must EXIST for this paper to be testable, does it exist, and can it CARRY the claim? (data, model checkpoints, producing-code) |
| 1-claims | Which claims are supported, weak, or GAP? |
| 2-pitch | What is the paper selling? (one minute, to the pinned venue) |
| 3-narrative | How do claims become a manuscript arc? |
| 4-display | What figure/table carries each claim? |
| 5-section-edit | Does each section's prose do its job? (per-section DRAFT-PROBE-REVISE-CHECK) |

Two axes stay orthogonal: **layer/frontier** (which stage has the active work) and **maturity** (how real the paper is: seed, working, submission-ready, published).

`1-resource`, `1-claims` and `4-display` are the three stages where the paper reaches out for evidence. They cleave cleanly: a question that CHANGES what exists on disk (`task-for-data` / `task-for-algo` / `task-for-fit`) is RESOURCE; a question that READS what exists and MOVES A CLAIM'S STATUS (`task-for-eval`) is CLAIMS. Resource may never commission `task-for-eval`. `review` is the gate that decides which earlier stage is broken.

## Evidence routing

For claim-related evidence, the paper always routes through the PROBE phase. It raises its questions as SECTIONS in `1-probes/`, MATCHes each against the bank's QA corpus (most close there, for free), and dispatches only what MATCH cannot close — handing the section's `commission:` block, VERBATIM, to the task/discovery orchestrators. A standalone utility question a human wants goes to the bank's own `/haipipe-task qa` door, never proxied by the paper.

The paper does not execute code, search literature directly, or store raw results.

## Boundaries

```text
task       executes internal work
discovery  checks outside evidence
probe      the paper's Q/A map: one SECTION per question, bound BY PATH to the
           executor's answering QA file. It does not judge — the claim's status
           lands in the paper's 0-lifecycle/1-claims/1-claims.md
paper      selects evidence, writes prose, delivers
```

## Paper Console

`/haipipe-paper` inside a paper opens a Paper Console: a context-aware working session for one active paper. The console resolves the paper root, derives current state from disk (not stored status), renders a dashboard, records session state in `.paper-console.yaml`, and routes follow-up input through the lifecycle.

## Copilot policy

Auto: read files, summarize status, classify input, draft stage .tex, detect open needs.

Ask first: costly task/PHI work, claim verdicts, multi-section edits, compile-to-submit, opening/closing rounds.

## Folder model

```text
STATUS.md                     0-lifecycle/{0..5}/
0-sections/                   0-displays/displayNN-*/
1-probes/PPNN_*.md       1-rounds/vYYMMDD/
1-compile.sh                  1-config.yaml
```

`0-` = source of truth. `1-` = process.

## Design prompt

Use this when revising or implementing the paper skill:

```text
You are designing the haipipe-paper layer.

Treat a paper as a delivery contract, not a writing folder.
The paper lifecycle is the stage spine:
0-seed > 1-resource > 1-claims > [venue] > 2-pitch > 3-narrative > 4-display >
5-section-edit, then review > submit > round/respond > present. Seed, resource
and claims are venue-FREE; pitch through section-edit are venue-ALIGNED.
(resource and claims SHARE the number 1, as venue and pitch already share 2.
The number is decoration; the spine key is the bare name. Never renumber.)

For each lifecycle stage, specify: what question it answers, which skill
procedure owns it, which files it reads/writes, whether it calls
task/probe/discovery, what artifact it produces, what machine state
it updates, and when it must stop and ask the user.

Keep the paper folder fixed:
STATUS.md, 0-lifecycle/<stage>/<stage>.tex, 0-sections/,
0-displays/displayNN-<slug>/, 1-probes/PPNN_<topic>.md,
1-rounds/vYYMMDD/{README,discussion,decisions,todo,applied}.md.

Preserve boundaries:
- for claim-related evidence, paper routes through a stage's PROBE phase; there
  is no direct task/discover — a standalone utility question uses the bank's own door
- paper raises questions as sections in 1-probes/, MATCHes, then dispatches
- paper does not execute code, search literature, or store raw results
```
