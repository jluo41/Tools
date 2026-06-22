probe - Mental Model
====================

What a probe is
===============

A probe is a CLAIM-LEVEL EVIDENCE CONTRACT, not an execution unit.

```
task       =  DO        "did this run work?"               runs code
discovery  =  LOOK OUT  "what does outside evidence say?"  inspects literature/prior art
insight    =  REMEMBER  "what do we already know?"         preserves judged knowledge
probe      =  JUDGE     "does the available evidence support this claim,
                         under what scope, with what caveats?"
```

A probe does not run code, search literature bodies, or store paper prose. It sits above those layers and asks a single question of whatever evidence exists. The probe layer stays small, readable, and auditable. It is not a task runner, a literature archive, or a paper-writing layer.

Read these for the authoritative contract; this file is the intuition:

```
../PHILOSOPHY.md
haipipe-probe/SKILL.md
haipipe-probe/ref/lifecycle-map.md
haipipe-probe/ref/probe-yaml-schema.md
```


The lifecycle - five steps
==========================

```
1. Plan    define the claim and what evidence would settle it
2. Gather  call missing task/discovery work; link existing artifacts
3. Read    summarize the gathered evidence into evidence.md + probe.yaml.result
4. Judge   run structural + integrity + claim gates into verdict.md + probe.yaml.verdict
5. Return  send the verdict back to source/memory into return.md + probe.yaml.return
```

Plan absorbs intake and framing. Input can be a paper claim gap, an application question, a reviewer objection, a task path, a discovery note, an insight card, or a loose idea. Plan turns that into an existing-probe attachment, a new claim contract, or a standalone note.

Gather has two internal actions:

```
Call  create missing task/discovery work
Link  attach existing task/discovery/insight artifacts
```

Read and Judge stay separate on purpose:

```
Read  = what did the evidence say?
Judge = what claim can we honestly make?
```

Return is not Report. Report makes a result inspectable; Return sends a judged verdict to the place that needed it: a paper claim, application answer, reviewer response, insight memory, or the next evidence need.


The Probe Console
=================

`/haipipe-probe <probe>` opens a Probe Console: a context-aware working session for one active probe.

```
1. resolve the active probe
2. load probe.yaml + lifecycle artifacts + linked refs
3. render status.md / a console panel
4. record active state in .probe-console.yaml
5. route later free-form user input through the lifecycle
```

Console state is session state, not research evidence. It lives in `.probe-console.yaml` at the PROJECT ROOT, defined as the nearest directory containing `probes/` (for example `examples/ProjB-PhyTrait-OpioidRx/`, not necessarily the repo root).

Copilot is the default mode. The console makes low-risk progress automatically (read files, summarize status, classify input, suggest links, detect missing evidence, draft text) and pauses before costly, irreversible, or claim-committing actions (creating costly tasks, PHI/full-data work, changing the claim target, declaring a final yes/no verdict, editing paper/application text, filing insight memory).


The two no-arg / file entry points
==================================

```
/haipipe-probe              no-arg DASHBOARD: a derive-from-disk preflight
/haipipe-probe file "<x>"   FILE scattered work into the evidence base
```

The dashboard orients before any step acts. Its golden rule:

```
Never report a step done because probe.yaml says so.
A step is done only when its expected artifact resolves on disk.
When stored status and disk disagree, disk wins and the gap is flagged DRIFT.
```

It runs a shallow drift check (resolve path-like refs, flag missing ones), never a heavy parse or integrity audit. The frontier is the first step whose disk predicate fails.

`/haipipe-probe file` files a loose thought or one-off work at creation time so nothing falls on the floor. Three dispositions:

```
ATTACH      work shares an existing probe's claim (entity AND outcome at claim level) -> wire as evidence
NEW         claim-bearing but no probe fits -> propose a probe.yaml stub, ask one confirm
STANDALONE  not claim-bearing (prep/infra/display) -> no probe; log reason; shows UNLINKED in dashboard
```

ATTACH and STANDALONE auto-apply and report; NEW is a commitment and takes a confirm. Every decision appends a row to `probes/FILING.md`.


The flat probe folder
=====================

Probe folders are flat. Do not create probe group folders. Organize with tags, source refs, status, and `_index.md`.

```
probes/
├── _index.md
├── 0605_discretion-gradient/
│   ├── probe.yaml      machine-readable contract: refs + structured result/verdict/return
│   ├── status.md       human-readable Probe Console panel
│   ├── evidence.md     Read output: what the gathered evidence says
│   ├── verdict.md      Judge output: claim support, confidence, caveats
│   └── return.md       Return output: where the verdict went or should go
└── 0621_trait-diabetes/
    └── ...
```

Optional sidecars only when useful:

```
gather.md              complex call/link decisions
INTEGRITY_AUDIT.md     long independent integrity audit
CLAIMS_FROM_RESULTS.md claim-verifier output (Judge gate 3)
```

No code, notebooks, raw literature bodies, heavy results, or plots in probe folders. Those live in task/discovery/insight and are linked by reference. One probe folder equals one claim-level thread. Canonical ref is `P.<MMDD>` (for example `P.0605`); same-day collisions append a lowercase suffix (`P.0605b`).


Judge - builder is not judge
============================

Judge is the claim-commitment gate. It runs three INDEPENDENT reviewers so the planner cannot rubber-stamp its own work:

```
1. structural  required evidence exists, compared roles comparable, results match the
               intended contrast, discovery verdicts accounted for, caveats cover confounds
               -> probe-structural-reviewer-agent (or inline by a fresh reviewer)

2. integrity   provenance of outcome/ground truth, metric/table consistency, no phantom
               results, claim scope matches evidence scope, no leakage
               -> probe-integrity-auditor-agent (Codex, PATHS only so the builder can't rationalize)

3. claim       yes/partial/no/blocked, confidence, supported vs unsupported scope, caveats,
               next needs
               -> claim-verifier-agent (Codex)
```

Hard rule: integrity = fail BLOCKS the claim gate. Output is `verdict.md` plus the structured `probe.yaml.verdict` block. Judge stops if integrity fails, required evidence is missing, the claim would overreach, or a final yes/no needs user approval.


How probe relates to the other layers
=====================================

Evidence is the shared, durable core of a project. It holds four sibling folders:

```
project-root/
├── probes/        claim-level evidence contracts (this layer)
├── tasks/         executed internal work (code + results)
├── discoveries/   outside-evidence checks (literature, prior art)
└── insights/      judged knowledge (DIKW cards)
```

Probe READS the others; the others do not reference probes. Delete a probe and tasks/discoveries are untouched; delete a linked task and the probe's ref goes stale (the dashboard flags it as DRIFT). Tasks/discoveries are atomic; one task can be cited by several probes. Probe calls task/discovery during Gather and may call insight during Return.

DELIVERY lifecycles are SIBLINGS that consume the evidence core, not layers above it:

```
                       ┌──────────────────────────────────────────┐
                       │  EVIDENCE CORE (durable, shared)          │
                       │  probes / tasks / discoveries / insights  │
                       └──────────────────────────────────────────┘
                            ^                          ^
                            │ calls probe from a       │ calls probe from a
                            │ claims-ledger gap        │ claims-ledger gap
                   ┌────────┴────────┐        ┌────────┴──────────────┐
                   │ paper-lifecycle │        │ application-lifecycle  │
                   │ (a delivery)    │        │ (a delivery)           │
                   └─────────────────┘        └────────────────────────┘
```

A delivery (paper, application) keeps a claims ledger. When a claim has an evidence gap, the delivery calls a probe; the probe judges and returns a verdict the delivery files back into the ledger. Multiple papers can share the SAME evidence core; they do not share framing.

The old "narrative" was a separate live LAYER above probes. It is retired. Narrative now survives only as a STAGE inside a delivery lifecycle. Papers share evidence, not narrative framing.


One probe, full lifecycle (illustrative)
========================================

```
[Plan]    Paper claim gap: "Agreeableness effect attenuates as discretion falls."
          /haipipe-probe plan ...
          writes probe.yaml with claim + evidence_plan; status: planned

[Gather]  /haipipe-probe gather P.0605 ...
          Call  -> haipipe-task: low-discretion regression (missing comparator)
          Link  -> existing high-discretion regression table; prior-art discovery
          writes probe.yaml.evidence_refs + calls; status: gathering / waiting_for_evidence

[Read]    /haipipe-probe read P.0605
          summarizes linked tables, missingness, contradictions, scope
          writes evidence.md + probe.yaml.result; status: read

[Judge]   /haipipe-probe judge P.0605
          structural + integrity(Codex, paths-only) + claim(Codex) gates
          writes verdict.md + probe.yaml.verdict; status: judged

[Return]  /haipipe-probe return P.0605
          backfills the paper claim / files insight memory / emits next need
          writes return.md + probe.yaml.return; status: returned
```

probe.yaml is the canonical record of the contract. The evidence itself lives in the task/discovery/insight folders it links.


FAQ
===

Q: I have a notebook that aggregates runs into a plot. Where does it go?
A: A task (a display-type task-folder). Aggregation is code; it belongs to task. The probe links the plot as evidence; the plain-English claim lives in the probe verdict.

Q: Can one task be referenced by two probes?
A: Yes. Tasks are atomic; probes compose. The same task path can be linked as evidence by multiple probes.

Q: probe.yaml has a result block with numbers. Is it a result archive?
A: No. result is a Read summary that references evidence living in task/discovery folders. It does not own or move artifacts.

Q: Where do daily working notes go now?
A: There is no per-probe daily log in v4. The current state lives in status.md (panel) and the structured probe.yaml blocks. Scattered thoughts get filed via `/haipipe-probe file` into FILING.md.

Q: What about exploratory work not tied to any claim?
A: It stays in tasks/discoveries unlinked, or is filed STANDALONE. Not every run needs a probe; probes exist for claims.

Q: Where does paper prose / framing live?
A: In the delivery lifecycle (paper-lifecycle / application-lifecycle), not in the probe. The probe returns a judged verdict; the delivery writes the prose.


Retired in v4 (do not use)
==========================

The following v3 concepts are GONE. They are listed only so old references are recognizable as legacy:

```
sandwich lifecycle                          -> replaced by Plan/Gather/Read/Judge/Return
8 stages (design/bridge/run/aggregate/      -> the 5 lifecycle verbs
  review/claim/fileK/explore)
Mode A / Mode B                             -> single copilot policy on one lifecycle
arms / aggregation / run_specs /            -> probe no longer runs or aggregates; it links evidence
  paired-t-as-the-point
inspect / explore specialists               -> removed
idea-creator / idea-reviewer / explorer     -> removed
  agents
three-layer pyramid with narrative          -> evidence core + delivery siblings; narrative is a
  as a live layer                              stage inside a delivery, not a layer
```

Legacy verb aliases still route for compatibility: design->plan, bridge/dispatch->gather, harvest->read, post/resume->read+judge, review->judge, file->gather/plan.


One-line rules of thumb
=======================

- New code or run?             -> tasks/ (never probes/)
- New outside-evidence check?  -> discoveries/ (never probes/)
- New claim to test?           -> probes/<MMDD>_<slug>/probe.yaml (Plan)
- Missing evidence?            -> Gather Call (task/discovery), then Link
- "What did the evidence say?" -> Read -> evidence.md
- "What can we honestly claim?"-> Judge -> verdict.md (integrity=fail blocks claim)
- "Where does the verdict go?" -> Return -> return.md (backfill / file memory / next need)
- Scattered thought or one-off work? -> /haipipe-probe file (ATTACH / NEW / STANDALONE)
- Lost the thread?             -> /haipipe-probe (no-arg dashboard, disk wins over stored state)
