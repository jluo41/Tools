probe - Claim-Level Evidence Contract (DESIGN)
================================================

Status: v4.0.0 (2026-06-22) - Probe Console + lifecycle Plan/Gather/Read/Judge/Return; flat probe folders; 3 reviewer agents.
Owner:  jluo41
Scope:  the probe layer as a claim-level evidence contract. The probe owns the
        question before the work and the interpretation after. It executes no
        code; tasks and discoveries do the work and are linked by reference.


Authority
=========

This DESIGN.md is the internals/rationale doc. It must agree with the canonical
files; if they disagree, those win:

```text
PHILOSOPHY.md                       core position + policy
haipipe-probe/SKILL.md              entry point, commands, routing
haipipe-probe/ref/lifecycle-map.md  per-step contract (the implementation map)
haipipe-probe/ref/probe-yaml-schema.md  machine contract field spec
haipipe-probe/fn/*.md               one procedure per lifecycle verb
haipipe-probe/ref/probe-dashboard.md    no-arg derive-from-disk panel
haipipe-probe/ref/probe-attach.md       filing judge for scattered work
haipipe-probe/agents/README.md          the 3 Judge reviewers
```

`MENTAL_MODEL.md` (sibling) remains the boundary doc between task and probe.


Core Position
=============

A probe is not an execution unit. A probe is a claim-level evidence contract.

```text
task      runs code (internal work)
discovery inspects outside evidence
insight   preserves judged knowledge
probe     plans, gathers, reads, judges, and returns claim-level verdicts
```

The probe sits between execution and synthesis and asks one question:

```text
Does the available evidence support this claim, under what scope, and with what caveats?
```

The probe owns the question before the work and the interpretation after. It
does not own the work itself. The layer must stay small, readable, auditable. It
must not become a task runner, a literature archive, or a paper-writing layer.


Lifecycle
=========

Every probe has the same lifecycle, run inside a Probe Console:

```text
1. Plan   - define the claim and evidence needed to test it
2. Gather - call missing task/discovery work and link existing artifacts
3. Read   - summarize the gathered evidence
4. Judge  - decide what the evidence honestly supports
5. Return - send the verdict back to the source or memory
```

Two boundaries are load-bearing:

```text
Read vs Judge    Read = what did the evidence say?
                 Judge = what claim can we honestly make?
Return vs Report Report makes a result inspectable.
                 Return sends a judged verdict, with caveats, to the place that needed it.
```

`Plan` absorbs intake/framing. The input may be a paper claim gap, an
application question, a reviewer objection, a task path, a discovery note, an
insight card, or a loose idea. Plan turns it into one of: attach to an existing
probe, a new claim contract, or a standalone note.

`Gather` is evidence acquisition, not interpretation. It has two internal
actions:

```text
Call - create missing task/discovery work
Link - attach existing task/discovery/insight artifacts
```


Probe Console
=============

`/haipipe-probe <probe>` opens a Probe Console: a context-aware working session
for one active probe. It is the front door for the lifecycle.

```text
1. resolve the active probe (P.0605 | 0605 | probes/0605_slug/)
2. load probe.yaml + lifecycle artifacts
3. render status.md / a console panel
4. record active state in .probe-console.yaml
5. route later free-form user input through Plan -> Gather -> Read -> Judge -> Return
```

Console state is session state, not research evidence. It lives at the project
root, defined as the nearest directory containing `probes/` (for example
`examples/ProjB-PhyTrait-OpioidRx/`, not necessarily the repo root):

```text
.probe-console.yaml
```

The console derives the current lifecycle stage from disk:

```text
no probe.yaml contract            -> Plan
evidence missing / refs absent    -> Gather
evidence linked but no evidence.md -> Read
evidence present but no verdict.md -> Judge
verdict present but no return action -> Return
return complete                   -> closed / ready for next probe
```


Commands and Routing
====================

```text
/haipipe-probe <probe>            open Probe Console for probe
/haipipe-probe console <probe>    explicit console open
/haipipe-probe                    no-arg derive-from-disk dashboard + active console resume
/haipipe-probe file "<work>"      filing judge for scattered work (attach/new/standalone)

/haipipe-probe plan <args...>     Plan
/haipipe-probe gather <probe> ... Gather (call/link/check)
/haipipe-probe read <probe>       Read
/haipipe-probe judge <probe>      Judge
/haipipe-probe return <probe>     Return

/haipipe-probe status [<probe>]   render status panel
/haipipe-probe "<free text>"      route via active console, else Plan
```

Resolution order (see SKILL.md Routing):

```text
0. resolve legacy aliases to a v4 verb first
1. v4 lifecycle verb         -> read fn/<verb>.md, execute
2. token resolves to a probe -> fn/console.md for that probe
3. active console + free text -> fn/console.md router
4. no console + free text    -> fn/plan.md
5. no args                   -> dashboard (ref/probe-dashboard.md)
```


Legacy Alias Table
==================

Legacy verbs have NO separate procedure files. The router maps each to a v4
procedure via this table, then reads that procedure.

```text
design   -> plan
bridge   -> gather call
dispatch -> gather call
harvest  -> read
post     -> read + judge
resume   -> read + judge
review   -> judge
file     -> gather link / plan   (or the probe-attach filing judge)
```


Skill Procedures (fn/)
======================

One procedure file per lifecycle verb. No code engine, no per-stage slash
commands.

```text
fn/console.md  Probe Console entrypoint and router
fn/plan.md     define/revise the claim and evidence contract
fn/gather.md   call missing work, link existing artifacts, check readiness
fn/read.md     summarize linked evidence
fn/judge.md    decide claim support through independent gates
fn/return.md   return verdict to source or memory
```


Probe Lifecycle Map
==================

The per-step contract lives in `haipipe-probe/ref/lifecycle-map.md` and is the
implementation map for this layer. Summary (the map file is authoritative):

```text
Step     Procedure       Question                          Writes
───────  ──────────────  ────────────────────────────────  ─────────────────────────────
Console  fn/console.md   which probe, what can happen next  .probe-console.yaml, status.md
Plan     fn/plan.md      what claim, what would settle it   probe.yaml(claim,evidence_plan), status.md
Gather   fn/gather.md    missing or already present         probe.yaml(evidence_refs,calls), status.md
Read     fn/read.md      what did the evidence say          evidence.md, probe.yaml.result, status.md
Judge    fn/judge.md     what claim is honestly supported   verdict.md, probe.yaml.verdict, status.md
Return   fn/return.md    where the verdict goes             return.md, probe.yaml.return, status.md
```

External calls: Gather may call `haipipe-task` / `haipipe-discovery`; Judge may
call reviewer agents / Codex; Return may call `haipipe-insight-*` and edits
paper/application only with approval. Every other step calls nothing.


Folder Model
============

Probe folders are FLAT. There are no probe group folders. Organization uses
tags, source refs, status, and `_index.md`.

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
    └── ...
```

One probe folder = one claim-level thread. Canonical ref `P.<MMDD>`; same-day
collisions append a lowercase suffix (`P.0605b`).

No code, notebooks, raw literature bodies, heavy result artifacts, or plots live
in probe folders. Those belong to task / discovery / insight and are linked by
reference.


File Schemas
============

Required files:

```text
probe.yaml   machine contract: claim, evidence_plan, evidence_refs, calls,
             result, verdict, return
status.md    human-readable Probe Console panel
evidence.md  Read output: what gathered evidence says
verdict.md   Judge output: claim support, confidence, caveats
return.md    Return output: where the verdict went or should go
```

Optional sidecars:

```text
gather.md              only for complex call/link decisions
INTEGRITY_AUDIT.md     long independent integrity audit (Judge gate 2)
CLAIMS_FROM_RESULTS.md claim-verifier output (Judge gate 3)
```

probe.yaml - block ownership (full field spec in ref/probe-yaml-schema.md):

```text
Block          Owner step   Purpose
─────────────  ───────────  ──────────────────────────────────────────────
id/slug/title  Plan         identity
status         any          lifecycle status enum
source         Plan         where the need came from + return_target
claim          Plan         hypothesis, target_sentence, falsification, scope
evidence_plan  Plan         required/optional evidence + success_criteria
evidence_refs  Gather       linked task/discovery/insight artifacts (by ref)
calls          Gather       requested task/discovery work (type=task|discovery)
result         Read         evidence summary, missing, contradictions, scope
verdict        Judge        status/confidence/structural/integrity/scope/caveats
return         Return       target, returned_claim, required_caveats, actions
```

Insight is never a `calls` type. Insight is called by Return only, after the
verdict is judged and approved for memory filing.


Judge: builder != judge
=======================

Judge is the claim-commitment gate. It keeps three independent reviewer agents,
wired from `fn/judge.md`. The planner never grades its own claim.

```text
Gate  Agent                            Backed by         Deliverable
────  ───────────────────────────────  ────────────────  ─────────────────────────
1     probe-structural-reviewer-agent  self              verdict.md (structural) + probe.yaml.verdict.structural
2     probe-integrity-auditor-agent    Codex, paths-only INTEGRITY_AUDIT.md + probe.yaml.verdict.integrity
3     claim-verifier-agent             Codex             CLAIMS_FROM_RESULTS.md + probe.yaml.verdict
```

Order: structural -> integrity -> claim. `integrity = fail` blocks `claim`.
Integrity and claim are out-of-family: the executor passes only file PATHS;
Codex reads the files and rules, so the builder cannot rationalize its own work.

Real agent files live in `haipipe-probe/agents/reviewers/`; the plugin top-level
`agents/` holds flat symlinks for `subagent_type` dispatch. Agents are thin
pointers; judgment logic stays in `fn/judge.md`,
`ref/probe-caveats-checklist.txt`, and `ref/probe-yaml-schema.md`.


Where probe sits: evidence is the shared core
=============================================

Evidence is the shared, durable core. paper-lifecycle and application-lifecycle
are DELIVERY SIBLINGS. Each calls probe from a gap in its own claims ledger;
probe returns a judged verdict that the delivery lifecycle consumes.

```text
                 ┌──────────────────────────────────────────────┐
                 │ delivery siblings (each owns a claims ledger)  │
                 │   skills/paper/         skills/application/     │
                 └───────────────┬───────────────┬───────────────┘
                                 │ claim gap     │ claim gap
                                 ▼               ▼
                 ┌──────────────────────────────────────────────┐
                 │ probe  (claim-level evidence contract)         │
                 │   Plan -> Gather -> Read -> Judge -> Return     │
                 └───────────────┬───────────────┬───────────────┘
                          Gather │ Call/Link     │ Return (with approval)
                                 ▼               ▼
                 ┌──────────────────────────────────────────────┐
                 │ task (code) · discovery (outside) · insight     │
                 └──────────────────────────────────────────────┘
```

Consequences:

```text
- Papers share EVIDENCE, not framing. Two papers can return from the same probe
  verdict and frame it differently.
- The narrative LAYER is retired as a live peer of probe. Narrative survives
  only as a STAGE inside a delivery lifecycle, not as a layer probe answers to.
- task never references probe. The dependency is one-way: probe reads tasks.
```


Boundaries (task <-> probe)
===========================

Full rules in `MENTAL_MODEL.md`. Short version:

```text
Rule 1  probes/ has NO code.            All computation lives in tasks/.
Rule 2  probe.yaml is the contract.     Source metrics live in tasks/.../ results.
Rule 3  One-way dependency.             Probes READ tasks; tasks do NOT reference probes.
Rule 4  Tasks are atomic.               One task can serve multiple probes.
```

probe may call task/discovery during Gather, and insight during Return. probe
does not execute code, search literature bodies directly, or store final paper
prose as its own artifact.


No-arg Dashboard
================

`/haipipe-probe` with no args is a derive-from-disk preflight
(`ref/probe-dashboard.md`). Golden rule:

```text
Never report a step as done because probe.yaml says so.
A step is done only when its expected artifact resolves on disk.
When stored status and disk disagree, disk wins and the gap is flagged DRIFT.
```

The shallow drift check is always on: read probe.yaml, extract path-like refs
(tasks/ discoveries/ insights/ probes/ paper/ applications/), resolve them
against the project root, mark missing refs as DRIFT. It does NOT parse heavy
artifacts or run integrity audits. The frontier is the first step whose disk
predicate fails. The dashboard also surfaces UNLINKED EVIDENCE: task/discovery
folders not linked to any active probe.


Filing scattered work
=====================

`/haipipe-probe file "<work>"` is the filing judge (`ref/probe-attach.md`). It
runs at the moment work is created so nothing falls on the floor unfiled. Three
dispositions:

```text
ATTACH      shares an existing probe's claim topic -> wire as that probe's evidence
NEW         claim-bearing but no probe fits        -> propose a probe.yaml stub, ASK
STANDALONE  not claim-bearing (infra/prep/display) -> no probe; log reason
```

ATTACH/STANDALONE auto-apply and report. NEW is a commitment: propose a filled
stub and take one confirm; never auto-create a probe. STRONG match for a
relational claim (X affects Y) requires BOTH halves (driver AND outcome) in a
claim-level field; one half alone is not strong. Every decision appends one line
to `probes/FILING.md`. A `P.06xx_*` row in FILING.md is a proposal, not an
existing probe; ask before materializing it.

Also auto-invoked by `haipipe-data` (on task create) and `haipipe-discovery` (on
discovery create).


Copilot Policy
==============

Default mode is `copilot`: context-aware assistance with human gates. The
console may automatically read files, summarize status, classify input, suggest
link targets, detect missing evidence, and draft evidence/verdict/return text.

It must ask before:

```text
creating costly tasks
running PHI/full-data work
changing the claim target
declaring a final yes/no verdict
editing paper/application text
filing insight memory as accepted knowledge
```

Auto mode, if added, is a policy on the same lifecycle, not a forked workflow.


Return Contract
===============

Every procedure returns a short tail:

```text
status:    ok | blocked | failed
summary:   1-3 sentences
artifacts: [paths read/written/created]
next:      suggested next command or question
```


Decision Log
============

2026-06-11  Created: DESIGN.md v1.0.0 (internals doc, parallel to task/DESIGN.md).
            MENTAL_MODEL.md remains the boundary doc.
2026-06-11  v2.0.0 - 5-stage lifecycle (Design/Materialize/Harvest/Judge/Insight),
            DIKW cascade in the Insight stage, loop-back Judge -> Explore -> Design.
2026-06-11  v3.0.0 - hub-centric consolidation. Lifecycle specialists folded into
            fn/ under the hub; only explore + inspect kept standalone skills.
2026-06-22  v4.0.0 - REFRAME. A probe is recast as a claim-level evidence
            contract, not an execution unit: it owns the question before the work
            and the interpretation after; tasks/discoveries do the work, linked
            by reference; insights preserve judged knowledge.
            - Lifecycle compressed to Plan -> Gather -> Read -> Judge -> Return,
              run inside a Probe Console (/haipipe-probe <probe>) with
              .probe-console.yaml state at the project root (nearest dir with probes/).
            - Probe folders flattened to probe.yaml + status.md + evidence.md +
              verdict.md + return.md. Group folders removed; no code/notebooks/
              heavy artifacts in probe folders (linked by reference).
            - Judge keeps builder != judge with 3 independent reviewers
              (structural -> integrity -> claim; integrity=fail blocks claim).
            - Evidence is the shared durable core; paper/application are delivery
              SIBLINGS that call probe from a claims-ledger gap. Papers share
              EVIDENCE not framing.
            - No-arg /haipipe-probe = derive-from-disk dashboard (golden rule:
              never trust stored verdict; shallow drift check always on).
              /haipipe-probe file = filing judge for scattered work.
            - Legacy verbs (design/bridge/dispatch/harvest/post/resume/review/file)
              get no separate files; the router maps them via the alias table.
            RETIRED in v4 (legacy vocabulary only): the sandwich lifecycle and its
            8 stages, Design/Materialize/Harvest/Open/Post/Insight stage names,
            Mode A / Mode B Design, arms / aggregation / run_specs,
            probe-lifecycle.workflow.js, the inspect and explore standalone skills,
            the idea-creator / idea-reviewer / explorer agents, the v3 templates
            (probe-status-template, probe-entry-template, etc.), and the
            three-layer pyramid with narrative as a live layer (narrative now
            survives only as a stage inside a delivery lifecycle).
