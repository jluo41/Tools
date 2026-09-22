# Reference: Labeling Run graph and compatibility capability tags

The subjective-label Workflow is a list of Run Specs connected by dependencies
and Routes; its execution is the native Run Instances and receipts. Building
and Scanning are capability groupings joined by the immutable Label Handoff.
P0-P5 remain serialized compatibility tags for those groupings. They do not
own Runs, gates, Routes, or an independent lifecycle. Calibration rounds,
internal Steps, and item events remain distinct domain units inside the graph.

## 1. Workflow graph overview

```text
Workflow Definition: Run Specs + dependencies + allowed Routes + completion rule
  Building Run Specs [P0-P2 compatibility tags]
    corpus-contract → round-prepare → weak-prelabel* → human-calibration
      → guideline-learn → round-measure → round-close → handoff-freeze
  immutable handoff-freeze Result (Label Handoff checksum)
  Scanning Run Specs [P3-P5 compatibility tags]
    test-gold-lock → executor-predict* → executor-score* → executor-select
      → scan-preflight → scan-shard* → risk-route → human-review → reconcile
      → audit-sample → audit-human-gold → audit-analyze → dstar-materialize
```

`subjective-label-workflow` defines the shared Run Spec graph and Routes.
`label-building-workflow` and `label-scanning-workflow` document operation
order and internal Steps for their respective Run Specs. The doors
`label-building` and `label-scanning` own semantic authority and forbidden acts.
An episode name such as Round, Test, Scan, or Audit groups domain work; it does
not add a Workflow node or Run count.

The old `state.phase`/P0-P5 labels are compatibility projections derived by
the current adapter from domain receipts. They may support existing views but
are not the Workflow frontier or routing authority. Resolve the next Run from
the Run Spec graph and native Ticket/Result/runtime receipts. Likewise a job
`hold` is a named resource/control state or Run outcome, not a side-specific
lifecycle state.

## 2. Legacy adapter labels (read-only projection)

```text
new → contracted → calibrating → frozen → testing → qualified → scanning
    → auditing → complete
```

These labels are retained for older status consumers. Each is a projection of
domain evidence, not an independently authored lifecycle state. `hold` must
name its control/Run owner and reason. A semantic change after handoff creates
a new Building Run lineage and invalidates downstream claims as required.

## 3. Contract capability group (P0 tag)

Contract validates one corpus snapshot with stable ids and text, records one
target and identified human semantic authority, declares class/region/
uncertainty schemas, reserves protected test identifiers before development,
creates the artifact scaffold, and records retrieval-cache provenance.

Contract creates no gold and does not open protected test text.

## 4. Calibration Run Specs and Round episode (P1 tag)

A round is one unit folder `rounds/round_<t>/` (`ref-assets.md` §3). It is
born as a card a person releases, begins from one closed state, and closes
only at a Checkpoint:

```text
closed G_(t-1) + D_(t-1)
        ↓ CARD released · PROSPECT written
        ↓ PREPARE
candidate pool + frozen batch + sealed weak predictions
        ↓ JUDGE
human-first locks + final human decisions
        ↓ LEARN
policy proposals + backward impact + audit/challenge evidence
        ↓ CLOSE
checkpoint → closed G_t + D_t → register cells settled → view/ rendered
        → repeat / freeze / HOLD
```

PREPARE, JUDGE, LEARN, and CLOSE are internal Steps in the calibration Runs.
Round 1 uses a declared random development batch and no model prelabels or
inherited regions. Later rounds combine targeted challenge cases with a
probability or weighted consensus-audit arm.

## 5. Human-AI Session Steps

For every item:

1. show item text and the prior closed policy without weak predictions;
2. save human-first class, region, uncertainty, evidence, and alternative;
3. lock the first-pass record;
4. reveal sealed structured comparisons when useful;
5. save the final human decision and typed change;
6. propose policy and backward-impact candidates without self-acceptance.

Sessions resume per item. Unresolved is a workflow disposition, never `NONE`.

## 6. Checkpoint Result and stopping Route

The Checkpoint Keeper validates every batch disposition, human evidence,
cumulative gold, policy changes, regression effects, audit/challenge separation,
coverage, risk, checksums, and the next route.

`round-close` may Route to `handoff-freeze` only when quality, stability,
coverage, acceptable risk, and human signoff all pass for the configured
comparable streak. A low plateau, elapsed time, round limit, or model agreement
does not satisfy that Run's exit predicate.

## 7. Handoff Run (P2 tag)

Freeze exact `G*` and `D_cal*`, verify sealed-test custody, obtain the human
signature, and materialize `handoff/label-v1.yaml`. Read
`ref-label-handoff.md` for fields and invalidation.

The handoff ends Building and is the only input authority Scanning may consume.
It carries a protected-manifest checksum, never protected ids or text.

## 8. Test Run Specs (P3 tag)

Validate the handoff; preregister candidate executors, model-family roles,
wrappers, baselines, metrics, repeats, quality floors, and selection rule;
authorize test-text release; collect and LOCK blind human `T*` before any
candidate prediction (the GOLD step); then run every candidate with gold
hidden, close every candidate prediction attempt before scoring, produce comparable
scorecards, and qualify a production route only when every required floor
passes (the SCORE step).

Public data is optional external validity and never project gold.

## 9. Production Run Specs (P4 tag)

Freeze a production manifest, run preflight, execute append-only idempotent
attempts, route declared risks to human review, and reconcile exactly one
terminal candidate per in-scope item. Production human decisions override model
outputs semantically but do not revise `G*`.

The candidate is not `D*` until `dstar-materialize` completes on its declared
passing or accepted-limit Route.

## 10. Audit Run Specs (P5 tag)

Freeze a probability audit design before inspection, collect blind human audit
gold, estimate weighted errors and intervals, inspect protected strata and
routes, and write an immutable receipt. Route to pass, repair, rescan, narrowed
human-accepted limitation, or semantic reopen.

Complete means every in-scope item has one terminal disposition and the audit
supports the exact bounded claim materialized with `D*`.

## 11. Retired names

```text
/label-init · /label-round          → /label-building
/label-evaluate · /label-complete   → /label-scanning
/label-status                       → /subjective-label status
subjective-labeling (draft name)    → label-building
subjective-scanning (draft name)    → label-scanning
```

Legacy `/sl-*` names forward through the same routes. None of them preserves
old panel-consensus, public-kappa, or static-cascade semantics.

## 12. Implementation status

This Run graph is the governing contract. Existing libraries provide partial
technical primitives and may still contain legacy code paths. Skills emit an
explicit `HOLD` when a required keeper, seal, writer, runner, reconciler, or
auditor has not shipped; they never manufacture a successful Run Result,
gate receipt, or control record.
