# Insight Board Spaces · UI ↔ Workflow ↔ artifacts

Insight plugins use one public naming rule:

```text
Space = the user-facing workspace surface
```

`Workspace` is not a competing reader-facing term. It may remain in legacy
query parameters, CSS classes, or internal compatibility names, but new UI
labels and current plugin prose use `Space`.

## The four Insight Spaces

```text
Scope Space      choose the source, snapshot, partition, and question
Run Space        inspect the Flow Table, Question Evolution, and Runs
Insight Space    read D / I / K / W outputs
Evidence Space   inspect Supporting Runs, Results, lineage, and handoffs
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
Flow Table             Run Spec × Space matrix and current frontier
Question Evolution     one stable QD/QI/QK/QW id across its lifecycle
Runs                   allocated Run / RI instances, triggers, actors, inputs,
                       statuses, Results, and receipts
```

The Flow Table rows are the six Insight RunTypes:

```text
I0 Meta → I1 Question → I2 Data → I3 Information → I4 Knowledge → I5 Wisdom
```

The columns are the four Spaces. A cell reports the action, state, and
artifact for that Run Spec in that Space. `workflow_runtime_id` is the runtime
envelope behind Run Space; it is not a Space label and is not itself a Run.

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
means one of these four Spaces.
