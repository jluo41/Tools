# Insight Board Spaces · UI ↔ Workflow ↔ artifacts

Insight workbenches use one public naming rule:

```text
Space = the user-facing workspace surface
```

`Workspace` is not a competing reader-facing term. It may remain in legacy
query parameters, CSS classes, or internal compatibility names, but new UI
labels and current workbench prose use `Space`.

## The Insight Spaces

```text
Scope Space      choose the source, snapshot, partition, and question
Run Space        inspect Runs, Timeline, and the Workflow map
Insight Space    read D / I / K / W outputs
Evidence Space   inspect Supporting Runs, Results, and lineage
Check Space      read GI controls and mechanical findings
Delivery Space   inspect handoff eligibility and commissioned delivery work
```

These are projections, not folders and not RunTypes. The source tree remains
authoritative:

```text
board.md
0-MT-meta/MT00-meta/             source and partition scope
0-MT-meta/MT01-MT04/             question registers
1-D-data/                         observations
2-I-information/                 derivations
3-K-knowledge/                   claims
4-W-wisdom/                       counsel and handoff
```

## Run Space views

Run Space has three views. They are views inside one Space, not three more
Spaces:

```text
Runs                   actual native Run instances, their Skills, actor,
                       target, prerequisites, state and exact record paths
Timeline               recorded events and receipts
Workflow map           owed Run Specs for the selected cell, resource map,
                       and Folder trees
```

### Applicable Specs and actual Runs

The presenter reads `definition_ref` and verifies `definition_hash` from each
open Insight Runtime. It shows only selected, still-owed Specs in that frozen
`haipipe.insight-definition/v1` record. A Spec joins the selected question and
partition through its exact target/consumers, an exact target Page, or a
single-answer-target definition; declared dependencies follow that join.
An explicit different/partial cell binding never falls back to a shared Page.
Multi-target definitions with no exact join need the controller to resolve it.
Completed/reused work stays in the instance inventory and is not offered again.
A settled, refused, partial-final or ineligible Queue cell has no new answering
Spec offer. A missing or changed definition is a visible reading gap.

| Surface | Applicable work | What this surface allows |
|---|---|---|
| Insight / Answer | selected Structure and scoped Writing Specs | Copy request → paste and send |
| Evidence / Trace | selected support and typed Evidence Specs | Copy request → paste and send |
| Delivery | explicitly commissioned Delivery Specs | Copy request → paste and send |
| Page / This page | selected Specs whose exact target Page matches this Page | Copy request → paste and send |
| Run / Workflow map | same selected Specs, separate from allocations | Shown here · read-only |
| Run / Runs and Timeline | actual native instances and receipt history | Shown here · read-only |
| Scope / Register and Check | selection, registration and GI/control projections | Shown here · read-only; controls are not Runs |

A supported Spec entry names its plain-language purpose, canonical recorded
Run Type, target, owner Skill, worker Skill(s), actor, prerequisites, matching
Run/status, Runtime and frozen definition. Input pins, entry predicates,
dependencies and waiting records stay visible. Missing metadata says **not
recorded** and the copy request asks the owner to resolve it before dispatch.
Unknown Spec template projections say **Not built**. This presenter exposes no
**Start here** Run launcher. The existing `chain <question> <partition>` command
remains the execution entry through `haipipe-insight-workflow`.

The Runs view reads aggregate records from
`_runs/insight/<workflow_runtime_id>/runtime.yaml`. Managed rows require native
identity, Spec, owner, state, Ticket, Result and receipt. Reused external
Results need no new Spec or Ticket allocation. Empty inventories stay empty;
malformed or duplicate identities produce a visible reading error. Historical
Page-referenced Supporting receipts remain a separate provenance view, with
unrecorded native metadata explicitly identified. Native owners retain gate
and result authority.

### Copy request contract

Requests contain the exact Board, selected question and partition, answer Page,
bounded target, frozen definition and hash, Spec and canonical Run Type, owner
and worker Skills, actor, input/dependency/entry requirements, current matching
native Runs and next permitted action. Canonical identifiers survive display
name expansion. With no selected Spec, the chain request asks the controller to
resolve missing work before allocation. After execution, the request asks for
the actual native Run id, status, exact Result and receipt paths, and any blocker;
when no Run is allocated or resumed it requires that fact and the missing
prerequisite instead of an invented identity. Copy uses only the local clipboard;
a visible read-only text area is the fallback when clipboard access is denied.
Copying does not send, start, allocate, update a Runtime or persist any file.

Owner entry/exit rules, `mode: copilot`, prior scoped authorization and
person-reserved decisions remain effective when a user later sends the request.
A missing release, verification or signature remains a named hold. DIKW and
Folder kinds, registration, Page passes, checks, GI decisions and signatures
never become Run entries.

### Producer metadata interface

The display consumes recorded `run_type`, `owner`, `actor`, `target`, `inputs`,
`depends_on`, `entry`, plus `worker_skills` (or existing `workers`, `worker_skill`,
`worker` fields). Exact `consumers: [{question, partition}]` or target Page
addresses permit selection in a multi-target definition. These are read-side
inputs, not new native Run authority or a replacement central catalogue.
Where an owner does not publish worker/type/target metadata, that owner must
supply it; this workbench does not infer a worker from a Folder kind.

## Topic and question evolution

The reader-facing evolution model keeps three axes visible without turning
them into three competing queues:

```text
data side / partition     where the rows come from
question origin           why the question was born
  curiosity-driven        the inventory or an observed result raised it
  need-driven             a Brief, decision, or later follow-up raised it
Insight Level             what kind of answer is requested
  D → I → K → W            observe → derive → claim → counsel
```

The scheduler still computes `Question Group = partition × Insight Level`.
Origin is provenance on the stable question id, not another Question Group.
That distinction lets a reader follow one topic across partitions while also
seeing whether it was born from curiosity or from a later need.

```text
Topic / idea
  → origin record
  → stable question (QD|QI|QK|QW)
  → partition cells × Insight Level
  → Run Spec
  → allocated Run / RI
  → Result / evidence
  → answer, refusal, or follow-up question
```

The current presenter reads `topic`, `topic-id`, `parent`, `driver`, `raiser`,
`data-side`, and `partition` when a source record declares them. When those
fields are absent it says **not recorded** or **derived view**; it must not
invent a durable topic lineage from prose alone.

## R and RI relation

The canonical run contract uses `RI` for the Insight Run. `IR` is a readable
label only; it is not a second identity. The relation is nested:

```text
base R = reusable method / ticket
   └── RI (Insight Run) = base R + frozen data side/snapshot
                          + partition + question + target + acceptance
                              └── execution version → Result / receipt
```

Changing the data side, snapshot, partition, question, target, or acceptance
allocates a new RI; it does not mutate the base R and does not create a second
parallel run namespace. The Run Space therefore shows both identities in one
row whenever an RI ticket is present.

## Compatibility boundary

The old `workspace=1` query parameter and `lens=workspace` route may remain as
read-compatible aliases. They must resolve to the canonical Space selected by
the request. A new reader-facing label must never say `Workspace` when it
means one of these Spaces.
