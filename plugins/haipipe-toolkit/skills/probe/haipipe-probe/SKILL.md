---
name: haipipe-probe
description: "Probe Console and claim-level evidence lifecycle. Opens a context-aware console for one active probe, then routes free-form user input through Plan -> Gather -> Read -> Judge -> Return. A probe is a claim-level evidence contract: it plans what claim needs evidence, gathers by calling missing task/discovery work or linking existing artifacts, reads linked evidence, judges claim support, and returns the verdict to paper/application/insight memory. Trigger: probe, claim gap, evidence gap, hypothesis, link task, link discovery, judge claim, return verdict, Probe Console, /haipipe-probe."
argument-hint: "[console|plan|gather|read|judge|return|status] [probe_ref_or_path] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Workflow, Task
metadata:
  version: "4.0.0"
  last_updated: "2026-06-22"
  summary: "Probe Console + lifecycle map: Plan, Gather, Read, Judge, Return."
  changelog:
    - "4.0.0 (2026-06-22): reframe probe around Probe Console and the concise lifecycle Plan/Gather/Read/Judge/Return; flat probe folders; group folders removed."
    - "3.3.0 (2026-06-21): delivery-need inputs from paper/application and verdict backfill."
    - "3.1.0 (2026-06-19): sandwich lifecycle around discoveries/tasks."
---

# Skill: haipipe-probe

`haipipe-probe` owns the **Probe Console** and the claim-level evidence
lifecycle.

A probe is not an execution unit. A probe is a claim-level evidence contract.
Tasks run code. Discoveries inspect outside evidence. Insights preserve judged
knowledge. The probe asks:

```text
Does the available evidence support this claim, under what scope, and with what caveats?
```

Read first:

```text
../PHILOSOPHY.md
ref/lifecycle-map.md
```

---

## Probe Console

`/haipipe-probe <probe>` opens a Probe Console: a context-aware working session
for one active probe.

The console:

```text
1. resolves the active probe
2. loads probe.yaml and lifecycle artifacts
3. renders status.md / a console panel
4. records active state in .probe-console.yaml
5. routes later free-form user input through the lifecycle
```

Console state is session state, not research evidence. Store active probe state
at the **project root**, defined as the nearest directory containing `probes/`
(for example `examples/ProjB-PhyTrait-OpioidRx/`, not necessarily the repo
root):

```text
.probe-console.yaml
```

Use `status.md` inside each probe folder for the human-readable panel.

---

## Lifecycle

Every probe has the same lifecycle:

```text
1. Plan   - define the claim and evidence needed to test it
2. Gather - call missing task/discovery work and link existing artifacts
3. Read   - summarize the gathered evidence
4. Judge  - decide what the evidence supports
5. Return - send the verdict back to the source or memory
```

`Plan` absorbs intake/framing. Users may enter a paper claim gap, application
question, task path, discovery note, insight card, or loose idea.

`Gather` has two internal actions:

```text
Call - create missing task/discovery work
Link - attach existing task/discovery/insight artifacts
```

`Read` and `Judge` must stay separate:

```text
Read  = what did the evidence say?
Judge = what claim can we honestly make?
```

`Return` is not `Report`. Report makes a result inspectable. Return sends a
judged verdict back to the source that needed it.

---

## Commands

```text
/haipipe-probe <probe>                  open Probe Console for probe
/haipipe-probe console <probe>          explicit console open
/haipipe-probe                          project-level probe dashboard / active console resume

/haipipe-probe plan <args...>           Plan: create or revise claim/evidence contract
/haipipe-probe gather <probe> <args...> Gather: call/link/check evidence
/haipipe-probe read <probe>             Read: summarize linked evidence
/haipipe-probe judge <probe>            Judge: structural + integrity + claim verdict
/haipipe-probe return <probe>           Return: backfill/file memory/emit next need

/haipipe-probe status [<probe>]         render status panel
/haipipe-probe link <artifact>          alias: gather link in active console
/haipipe-probe call <kind> <need>       alias: gather call task|discovery
/haipipe-probe feedback "<text>"        capture skill feedback to feedback/ (fix later); `feedback list` shows open items
/haipipe-probe "<free text>"            route through active Probe Console if present
```

Legacy aliases remain valid:

```text
design   -> plan
bridge   -> gather call
dispatch -> gather call
harvest  -> read
post     -> read + judge
resume   -> read + judge
review   -> judge
file     -> gather link / plan, depending on input
```

---

## Skill Procedures

Each lifecycle verb has one procedure file:

```text
fn/console.md   Probe Console entrypoint and router
fn/plan.md      define/revise the claim and evidence contract
fn/gather.md    call missing work, link existing artifacts, check readiness
fn/read.md      summarize linked evidence
fn/judge.md     decide claim support through independent gates
fn/return.md    return verdict to source or memory
```

Legacy verbs (`design`/`bridge`/`harvest`/`dispatch`/`post`/`resume`/`review`/
`file`) have no separate files: the router maps them to the v4 procedures above
via the alias table in Commands, then reads that procedure.

Utility verb (not a lifecycle step):

```text
fn/feedback.md   capture skill feedback into feedback/ ; `feedback list` reviews open items
```

When implementing or revising a step, use the `Probe Lifecycle Map`:

```text
ref/lifecycle-map.md
```

---

## Probe Folder

Probe folders are flat. Do not create probe group folders.

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

File roles:

```text
probe.yaml  machine-readable contract, refs, structured result/verdict/return
status.md   human-readable Probe Console panel
evidence.md Read output: what gathered evidence says
verdict.md  Judge output: claim support, confidence, caveats
return.md   Return output: where the verdict went or should go
```

Optional:

```text
gather.md              only for complex call/link decisions
INTEGRITY_AUDIT.md     long independent integrity audit, when useful
CLAIMS_FROM_RESULTS.md claim-verifier output (Judge gate 3)
```

No code, notebooks, raw literature bodies, heavy result artifacts, or plots live
in probe folders. Those belong to task, discovery, or insight and are linked by
reference.

---

## Routing

Route arguments in this order:

```text
0. Resolve legacy-verb aliases to their v4 verb first (Commands alias table):
   design->plan, bridge/dispatch->gather, harvest->read, post/resume->read+judge,
   review->judge, file->gather/plan. There are no fn/<legacy>.md files.
1. If first token is a v4 lifecycle verb (or the utility verb `feedback`), read fn/<verb>.md and execute that procedure.
2. If first token resolves to a probe, open fn/console.md for that probe.
3. If active console exists and input is free text, route via fn/console.md.
4. If no active console exists and input is free text, route to fn/plan.md.
5. If no args, render project-level probe dashboard and active console state.
```

Resolver accepts:

```text
P.0605
0605
probes/0605_discretion-gradient/
```

Resolve relative to the active project root. If the current working directory is
inside a nested project, prefer that project's `probes/`. If multiple project
roots contain a matching probe ref, ask the user to choose.

If a probe ref appears only in `probes/FILING.md` as a proposal such as
`P.06xx_trait-diabetes`, do not treat it as an existing probe. Ask whether to
create/select the actual probe before linking artifacts.

---

## Boundaries

```text
task      executes internal work
discovery checks outside evidence
insight   stores judged knowledge
probe     plans, gathers, reads, judges, and returns claim-level verdicts
```

Probe may call task/discovery during `Gather`. Probe may call insight during
`Return`. Probe does not execute code, search literature bodies directly, or
store final paper prose as its own artifact.

For artifact-first inputs, `Gather` must apply `ref/probe-attach.md` before
editing `evidence_refs`. If the artifact does not strongly match the active
probe, propose an existing/new probe and ask before changing anything.

---

## Copilot Policy

Default mode is `copilot`.

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

Auto mode should be implemented later as a policy on the same lifecycle, not as
a separate workflow.

---

## Return Contract

Every procedure returns a short tail:

```text
status:    ok | blocked | failed
summary:   1-3 sentences
artifacts: [paths read/written/created]
next:      suggested next command or question
```
