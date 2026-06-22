# Probe Design Philosophy

This document defines the design philosophy for the `haipipe-probe` layer.
It is the reference for future probe skill updates, especially the Probe
Console and the Probe Lifecycle Map.

## Core Position

A probe is not an execution unit. A probe is a claim-level evidence contract.

Tasks run code. Discoveries inspect outside evidence. Insights preserve judged
knowledge. A probe sits between them and asks:

```text
Does the available evidence support this claim, under what scope, and with what caveats?
```

The probe layer should stay small, readable, and auditable. It should not
become a task runner, literature archive, or paper-writing layer.

## Lifecycle

Every probe has the same lifecycle:

```text
1. Plan   - define the claim and evidence needed to test it
2. Gather - call missing task/discovery work and link existing artifacts
3. Read   - summarize the gathered evidence
4. Judge  - decide what the evidence supports
5. Return - send the verdict back to the source or memory
```

`Plan` absorbs intake/framing. The user may provide a claim gap, a question, a
task folder, a discovery note, an insight card, or a loose idea. The probe must
turn that input into either an existing-probe attachment, a new claim contract,
or a standalone note.

`Gather` is evidence acquisition, not interpretation. It has two internal
actions:

```text
Call - create missing task/discovery work
Link - attach existing task/discovery/insight artifacts
```

`Read` and `Judge` must stay separate. Read answers "what did the evidence
say?" Judge answers "what claim can we honestly make?"

`Return` is not `Report`. Report makes results inspectable. Return sends a
judged verdict back to the place that needed it: a paper claim, application
answer, reviewer response, insight memory, or next evidence need.

## Probe Console

`/haipipe-probe <probe>` should open a Probe Console: a context-aware working
session for one active probe.

The console loads the active probe, renders a status panel, and routes later
free-form user input through the lifecycle:

```text
Plan -> Gather -> Read -> Judge -> Return
```

The console should remember:

```text
active probe
current lifecycle stage
claim being tested
linked task/discovery/insight artifacts
missing evidence
safe next actions
risky actions that require approval
return target
```

The console should make low-risk progress automatically and pause before
costly, irreversible, or claim-committing actions.

## Folder Model

Probe folders are flat. Do not introduce probe group folders.

Recommended project layout:

```text
probes/
├── _index.md
├── 0605_discretion-gradient/
│   ├── probe.yaml
│   ├── status.md
│   ├── evidence.md
│   ├── verdict.md
│   └── return.md
└── 0621_trait-diabetes/
    ├── probe.yaml
    ├── status.md
    ├── evidence.md
    ├── verdict.md
    └── return.md
```

One probe folder equals one claim-level thread. Organization should use tags,
source references, status, and `_index.md`, not nested group folders.

## File Roles

Keep the file set minimal.

```text
probe.yaml  - machine-readable contract, refs, structured result/verdict/return
status.md   - human-readable Probe Console panel
evidence.md - Read output: what gathered evidence says
verdict.md  - Judge output: claim support, confidence, caveats
return.md   - Return output: where the verdict went or should go
```

Optional files:

```text
gather.md              - only for complex call/link decisions
INTEGRITY_AUDIT.md     - only when a long independent integrity audit is useful
CLAIMS_FROM_RESULTS.md - legacy or expanded semantic verifier output
```

Do not put code, notebooks, raw literature bodies, or heavy result artifacts in
probe folders. Those belong to task, discovery, or insight.

## Probe Lifecycle Map

The `Probe Lifecycle Map` is the implementation map for this layer. It should
connect each lifecycle step to:

```text
step
skill procedure
question
action
reads
writes
external calls
human output
machine state
stop/gate
```

The map belongs in:

```text
skills/probe/haipipe-probe/ref/lifecycle-map.md
```

Every future probe skill change should preserve the map's contract.

## Copilot Policy

Copilot mode means context-aware assistance with human gates.

The Probe Console may automatically:

```text
read files
summarize status
classify user input
suggest link targets
detect missing evidence
draft evidence/verdict/return text
```

It must ask before:

```text
creating costly tasks
running PHI/full-data work
changing the claim target
declaring a final yes/no verdict
editing paper/application text
filing insight memory as accepted knowledge
```

Auto mode can be added later as a policy on the same lifecycle. Do not fork a
separate auto workflow.

## Design Prompt

Use this prompt when revising or implementing the probe skill:

```text
You are designing the haipipe-probe layer.

Treat a probe as a claim-level evidence contract, not an execution unit.
The probe lifecycle is Plan -> Gather -> Read -> Judge -> Return.

For each lifecycle step, specify:
- what question this step answers
- which skill procedure owns it
- which files it reads
- which files it writes
- whether it may call task, discovery, or insight
- what human-readable artifact it produces
- what machine-readable state it updates
- when it must stop and ask the user

Keep probe folders flat and minimal:
probe.yaml, status.md, evidence.md, verdict.md, return.md.
Do not introduce probe group folders.

Design the Probe Console so `/haipipe-probe <probe>` loads one active probe,
renders its current state, and routes arbitrary follow-up input through the
lifecycle. The console should make low-risk progress automatically and pause
before costly, irreversible, or claim-committing actions.

Preserve boundaries:
- task executes internal work
- discovery checks outside evidence
- insight stores judged knowledge
- probe plans, gathers, reads, judges, and returns claim-level verdicts
```
