# Paper Design Philosophy

A paper is a delivery contract, not a writing folder.

Tasks run code. Probes judge claims. Discoveries inspect outside evidence. Insights preserve judged knowledge. The paper sits downstream and asks: which judged evidence does this paper select, and how does it become a submittable manuscript?

## Lifecycle

```text
enter > 0-seed > 1-pitch > 2-claims > 3-narrative > 4-display > 5-minimap
        > write/edit > review > submit > round/respond > present
```

Each `0-lifecycle/<stage>/<stage>.tex` is standalone-compilable and answers one question:

| Stage | Question |
|---|---|
| 0-seed | Why might this paper exist? |
| 1-pitch | What is the paper selling? (one minute) |
| 2-claims | Which claims are supported, weak, or GAP? |
| 3-narrative | How do claims become a manuscript arc? |
| 4-display | What figure/table carries each claim? |
| 5-minimap | What job does each paragraph do? |

Two axes stay orthogonal: **layer/frontier** (which stage has the active work) and **maturity** (how real the paper is: prospectus, seed, working, submission-ready, published).

`2-claims` and `4-display` are the two stages where the paper reaches out for evidence. `review` is the gate that decides which earlier stage is broken.

## Evidence routing

For claim-related evidence, the paper always routes through probe (the universal evidence gateway). The probe calls task/discover during Gather. The paper buffers probe plans in `1-probe-plans/` during lifecycle work and batch-dispatches when the user is ready. Direct task/discover for non-claim utility work only.

The paper does not execute code, search literature directly, or store raw results.

## Boundaries

```text
task       executes internal work
discovery  checks outside evidence
probe      judges claim-level verdicts (universal evidence gateway)
insight    stores judged knowledge
paper      selects evidence, writes prose, delivers
```

## Paper Console

`/haipipe-paper` inside a paper opens a Paper Console: a context-aware working session for one active paper. The console resolves the paper root, derives current state from disk (not stored status), renders a dashboard, records session state in `.paper-console.yaml`, and routes follow-up input through the lifecycle.

## Copilot policy

Auto: read files, summarize status, classify input, draft stage .tex, detect open needs.

Ask first: costly task/PHI work, claim verdicts, multi-section edits, compile-to-submit, opening/closing rounds, filing insight memory.

## Folder model

```text
STATUS.md                     0-lifecycle/{0..5}/
0-sections/                   0-displays/displayNN-*/
1-probe-plans/PPNN_*.md       1-rounds/vYYMMDD/
1-compile.sh                  1-config.yaml
```

`0-` = source of truth. `1-` = process.

## Design prompt

Use this when revising or implementing the paper skill:

```text
You are designing the haipipe-paper layer.

Treat a paper as a delivery contract, not a writing folder.
The paper lifecycle is the stage spine:
0-seed > 1-pitch > 2-claims > 3-narrative > 4-display > 5-minimap,
then write/edit > review > submit > round/respond > present.

For each lifecycle stage, specify: what question it answers, which skill
procedure owns it, which files it reads/writes, whether it calls
task/probe/discovery/insight, what artifact it produces, what machine state
it updates, and when it must stop and ask the user.

Keep the paper folder fixed:
STATUS.md, 0-lifecycle/<stage>/<stage>.tex, 0-sections/,
0-displays/displayNN-<slug>/, 1-probe-plans/PPNN_<slug>.md,
1-rounds/vYYMMDD/{README,discussion,decisions,todo,applied}.md.

Preserve boundaries:
- for claim-related evidence, paper routes through probe (which calls
  task/discover during Gather); direct task/discover for non-claim only
- paper buffers probe plans in 1-probe-plans/ and batch-dispatches
- paper does not execute code, search literature, or store raw results
```
