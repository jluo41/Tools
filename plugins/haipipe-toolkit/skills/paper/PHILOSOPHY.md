# Paper Design Philosophy

This document defines the design philosophy for the `haipipe-paper` layer. It is
the reference for future paper skill updates, especially the Paper Console and
the Paper Lifecycle Map. It mirrors `../probe/PHILOSOPHY.md` applied to delivery.

## Core Position

A paper is not a writing folder. A paper is a delivery contract.

Tasks run code. Probes judge claims. Discoveries inspect outside evidence.
Insights preserve judged knowledge. A paper sits downstream of all of them and
asks:

```text
Which judged evidence does this paper select, and how does it become a
venue-shaped, submittable manuscript?
```

One paper folder equals one delivery thread. The paper layer owns this paper's
story, claim wording, displays, paragraph minimap, and section prose. It does
not own evidence. When a claim lacks support, the paper records a delivery need
and routes it to probe/task/discovery/insight, then backfills the verdict. The
paper never fakes project work.

## Lifecycle

The paper lifecycle is the stage spine, not a new set of verbs. It is defined in
`ref/paper-lifecycle.md` and is the same spine the folder uses:

```text
enter ▸ 0-seed → 1-pitch → 2-claims → 3-narrative → 4-figures-tables → 5-minimap
        ▸ write/edit → review → submit ↻ round/respond → present
```

Each `0-lifecycle/<stage>/` stage is a standalone-compilable `.tex` file. That
file is the stage contract. The spine is the specification; `0-sections/` is the
realization.

Each stage answers one question and owns one file:

```text
0-seed           Why might this paper exist?
1-pitch          What is the paper selling?
2-claims         Which claims are supported, weak, or GAP?
3-narrative      How do claims become a manuscript arc?
4-figures-tables What figure/table carries each claim?
5-minimap        What job does each paragraph do, and what anchors it?
```

Two axes stay orthogonal:

```text
layer / frontier  where the active work is (which stage)
maturity          how real the paper is (prospectus ... published)
```

`2-claims` and `4-figures-tables` are the two stages where the paper reaches out
for evidence. `review` is the gate that decides which earlier stage is broken.

## Paper Console

`/haipipe-paper` inside a paper opens a Paper Console: a context-aware working
session for one active paper.

The console:

```text
1. resolves the paper root
2. derives current state from disk, not from stored status
3. renders a dashboard panel
4. records session state in .paper-console.yaml at the paper root
5. routes later free-form user input through the lifecycle
```

`enter` and `status` are aliases for opening the console. Console state is
session state, not manuscript content.

## Folder Model

The paper folder is fixed in `README.md` and `ref/paper-lifecycle.md`:

```text
STATUS.md
0-lifecycle/{0-seed,1-pitch,2-claims,3-narrative,4-figures-tables,5-minimap}/
0-sections/
0-displays/displayNN-<slug>/
1-rounds/vYYMMDD/
1-compile.sh
```

The `0-` prefix is source of truth. The `1-` prefix is process. Do not
reintroduce retired names (see the README retired-names table).

## File Roles

```text
STATUS.md            current layer, maturity, active round
0-lifecycle/*/*.tex  one stage contract per stage, standalone-compilable
0-sections/*.tex     realized manuscript prose
0-displays/*/        one display unit per figure/table family
1-rounds/vYYMMDD/    dated work round: discussion, decisions, todo, applied
.paper-console.yaml  console session state at the paper/project root
```

Evidence, code, and raw results do not live in the paper. They live in
task/probe/discovery/insight and are linked by reference.

## Copilot Policy

Default mode is copilot. The Paper Console may automatically:

```text
read files
summarize status and the disk frontier
classify user input
draft or revise a stage .tex (seed/pitch/claims/narrative/display-map/minimap)
plan section work
detect open needs and suggest routes
```

It must ask before:

```text
calling costly task/PHI/full-data work
committing a claim verdict or downgrading a claim
editing prose across many sections at once
compiling-to-submit or packaging a submission
opening or closing a revision round destructively
filing insight memory as accepted knowledge
```

Auto mode is a later policy on the same lifecycle, not a separate workflow.

## Paper Lifecycle Map

The Paper Lifecycle Map is the implementation map for this layer. It connects
each lifecycle stage to its skill procedure, question, reads, writes, external
calls, human output, machine state, and stop gate. It lives in:

```text
ref/lifecycle-map.md
```

The derive-from-disk dashboard contract lives in:

```text
ref/paper-dashboard.md
```

Every future paper skill change should preserve both contracts.

## Boundaries

```text
task      executes internal work
discovery checks outside evidence
probe     judges claim-level verdicts
insight   stores judged knowledge
paper     selects evidence, sets story/claims/displays/minimap, writes prose, delivers
```

The paper calls probe/task/discovery during `2-claims`, `4-figures-tables`, and
`review`, and may call insight during respond/return. The paper does not execute
code, search literature bodies directly, or store raw results as its own
artifact.

## Design Prompt

Use this prompt when revising or implementing the paper skill:

```text
You are designing the haipipe-paper layer.

Treat a paper as a delivery contract, not a writing folder.
The paper lifecycle is the stage spine:
0-seed -> 1-pitch -> 2-claims -> 3-narrative -> 4-figures-tables -> 5-minimap,
then write/edit -> review -> submit -> round/respond -> present.
Do not invent a parallel set of verbs.

For each lifecycle stage, specify:
- what question this stage answers
- which skill procedure and related skills own it
- which files it reads
- which files it writes
- whether it may call task, probe, discovery, or insight
- what human-readable artifact it produces
- what machine-readable state it updates
- when it must stop and ask the user

Keep the paper folder fixed:
STATUS.md, 0-lifecycle/<stage>/<stage>.tex, 0-sections/,
0-displays/displayNN-<slug>/, 1-rounds/vYYMMDD/{README,discussion,decisions,todo,applied}.md.

Design the Paper Console so /haipipe-paper opens the active paper, derives
current state from disk, renders the frontier, and routes follow-up input
through the lifecycle. Make low-risk progress automatically; pause before
costly, irreversible, or claim-committing actions.

Preserve boundaries:
- task executes internal work
- discovery checks outside evidence
- probe judges claim verdicts
- insight stores judged knowledge
- paper selects evidence and turns it into a venue-shaped manuscript
```
