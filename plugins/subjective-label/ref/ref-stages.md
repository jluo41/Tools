# Reference: two-side lifecycle and state machine

The subjective-label family has two sibling sides joined by one immutable Label
Handoff. The scales are journey phase, calibration round, round step, and item
event. They have different units and closure rules.

## 1. Family lifecycle

```text
🏗 Label Building
P0 Contract → P1 Round × N → P2 Freeze → signed Label Handoff
                                              │
                                              ▼
🔍 Label Scanning
P3 Test → P4 Scan → P5 Audit → complete
```

`subjective-label-workflow` declares the phase numbers and gates and owns the
crossing. `label-building-workflow` and `label-scanning-workflow` order the
steps inside their side. The doors `label-building` and `label-scanning` own
the law: authority, human gates, verbs, forbidden acts.

Canonical states:

```text
new
→ contracted
→ calibrating
→ frozen            (handoff signed)
→ testing
→ qualified
→ scanning
→ auditing
→ complete
```

`hold` is an explicit side state with a reason and owner. A semantic change
after handoff creates a new Building lineage and invalidates downstream claims
as required.

## 2. P0 Contract

Contract validates one corpus snapshot with stable ids and text, records one
target and identified human semantic authority, declares class/region/
uncertainty schemas, reserves protected test identifiers before development,
creates the artifact scaffold, and records retrieval-cache provenance.

Contract creates no gold and does not open protected test text.

## 3. P1 Calibration Round

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

PREPARE, JUDGE, LEARN, and CLOSE are round steps, not journey phases. Round 1
uses a declared random development batch and no model prelabels or inherited
regions. Later rounds combine targeted challenge cases with a probability or
weighted consensus-audit arm.

## 4. Human-AI Session

For every item:

1. show item text and the prior closed policy without weak predictions;
2. save human-first class, region, uncertainty, evidence, and alternative;
3. lock the first-pass record;
4. reveal sealed structured comparisons when useful;
5. save the final human decision and typed change;
6. propose policy and backward-impact candidates without self-acceptance.

Sessions resume per item. Unresolved is a workflow disposition, never `NONE`.

## 5. Checkpoint and stopping

The Checkpoint Keeper validates every batch disposition, human evidence,
cumulative gold, policy changes, regression effects, audit/challenge separation,
coverage, risk, checksums, and the next route.

Calibration may route to P2 Freeze only when quality, stability, coverage,
acceptable risk, and human signoff all pass for the configured comparable
streak. A low plateau, elapsed time, round limit, or model agreement does not
pass.

## 6. P2 Freeze

Freeze exact `G*` and `D_cal*`, verify sealed-test custody, obtain the human
signature, and materialize `handoff/label-v1.yaml`. Read
`ref-label-handoff.md` for fields and invalidation.

The handoff ends Building and is the only input authority Scanning may consume.
It carries a protected-manifest checksum, never protected ids or text.

## 7. P3 Test

Validate the handoff; preregister candidate executors, model-family roles,
wrappers, baselines, metrics, repeats, quality floors, and selection rule;
authorize test-text release; collect and LOCK blind human `T*` before any
candidate prediction (the GOLD step); then run every candidate with gold
hidden, close every prediction run before scoring, produce comparable
scorecards, and qualify a production route only when every required floor
passes (the SCORE step).

Public data is optional external validity and never project gold.

## 8. P4 Scan

Freeze a production manifest, run preflight, execute append-only idempotent
attempts, route declared risks to human review, and reconcile exactly one
terminal candidate per in-scope item. Production human decisions override model
outputs semantically but do not revise `G*`.

The candidate is not `D*` until P5 closes.

## 9. P5 Audit

Freeze a probability audit design before inspection, collect blind human audit
gold, estimate weighted errors and intervals, inspect protected strata and
routes, and write an immutable receipt. Route to pass, repair, rescan, narrowed
human-accepted limitation, or semantic reopen.

Complete means every in-scope item has one terminal disposition and the audit
supports the exact bounded claim materialized with `D*`.

## 10. Retired names

```text
/label-init · /label-round          → /label-building
/label-evaluate · /label-complete   → /label-scanning
/label-status                       → /subjective-label status
subjective-labeling (draft name)    → label-building
subjective-scanning (draft name)    → label-scanning
```

Legacy `/sl-*` names forward through the same routes. None of them preserves
old panel-consensus, public-kappa, or static-cascade semantics.

## 11. Implementation status

This lifecycle is the governing contract. Existing libraries provide partial
technical primitives and may still contain legacy code paths. Skills emit an
explicit `HOLD` when a required keeper, seal, writer, runner, reconciler, or
auditor has not shipped; they never manufacture a successful phase receipt.
