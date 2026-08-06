# Reference: validated production routing

Production routing is the cost-and-risk policy used after calibration and sealed final
evaluation. It is not part of semantic authority and is not automatically licensed by
the existence of embeddings, a classifier, or several agreeing language models.

## 1. Entry gate

Do not label the remaining corpus through an automated route until all of the following
are true:

1. calibration has stopped under the declared conjunction of quality, stability,
   coverage, risk, and human signoff;
2. the final guideline `G*` is frozen;
3. the sealed human-gold test `T*` is complete;
4. each candidate executor or route has closed predictions on `T*`;
5. its scorecard meets the intended-use quality and protected-stratum floors;
6. the production manifest freezes policy, thresholds, budgets, and audit design.

If no candidate passes, production remains human-only or unresolved. Budget pressure
does not lower the quality gate silently.

## 2. Allowed route structure

A validated route may combine:

```text
corpus item
    │
    ├─ deterministic checks or duplicate rules
    ├─ validated small classifier or weak LM
    ├─ validated ensemble or routing rule
    └─ risk queue → human review / accepted unresolved
```

Each component must have a declared role. Retrieval, similarity, classifier confidence,
and LM agreement are routing signals. They are not gold labels by themselves.

## 3. Registration and validation

Register every candidate route before test predictions are opened:

- component model ids, versions, and families;
- guideline and wrapper checksums;
- decoding and repeat policy;
- thresholds and combination rule;
- abstention and human-escalation rule;
- expected cost and capacity;
- provenance tier assigned to accepted output;
- protected claims and selection rule.

Evaluate the whole route on `T*`. A component score cannot be substituted for the route
score. Any post-test threshold tuning invalidates that test for the modified route.

## 4. Preflight

Before a full run, execute a frozen preflight sample and report:

- expected acceptance, escalation, and unresolved rates;
- class and region mix by route;
- quality estimate linked to sealed-test evidence;
- projected cost, latency, and human-review load;
- sensitivity to threshold changes;
- known uncovered neighborhoods and drift risks.

The preflight is a deployment check, not a new opportunity to optimize `G*` against
`T*`. Material semantic problems reopen calibration and require a new evaluation plan.

## 5. Idempotent execution

Every attempt is append-only and keyed by corpus item, production run, policy version,
executor version, and attempt number. Retries do not overwrite earlier predictions.

Terminal reconciliation creates exactly one disposition for every in-scope item:

- human-confirmed;
- audited-machine;
- machine-accepted under a validated route;
- accepted unresolved;
- excluded with reason;
- invalid or failed with reason.

The system must never convert an unresolved or failed item to `NONE` merely to complete
the table.

## 6. Risk queue

Route an item to risk review when any declared condition fires, such as:

- executor disagreement or high predictive entropy;
- boundary-region hypothesis;
- low coverage or embedding novelty;
- policy reason-code mismatch;
- protected-stratum risk;
- duplicate conflict;
- out-of-scope or missing-context signal;
- production drift.

Human capacity is explicit. If the queue exceeds capacity, preserve unresolved status or
pause the run; do not relax thresholds without a new registered policy.

## 7. Final probability audit

After reconciliation, draw a probability sample from the production outputs. Include
representative coverage plus separately reported enrichment for risky routes, regions,
classes, and provenance tiers. Humans label audit items blind to machine output.

Report weighted error and intervals, class and protected-stratum findings, route-specific
errors, provenance shares, repairs, and accepted limitations. Failed claims trigger
targeted repair, re-audit, or scope reduction.

## 8. Relationship to calibration

Calibration improves the semantic parameter `G_t` and the human's own articulated
boundary through repeated human-grounded rounds. Production routing is selected only
after that process. A lower weak-model loss can motivate guideline edits during
development, but it cannot overrule human meaning or become an automatic stopping rule.

## 9. Implementation boundary

Legacy code may implement k-NN inheritance, classifier thresholds, or panel majority.
Those mechanisms are not v2-compliant production routes unless their registration,
sealed evaluation, abstention, provenance, and audit contracts are implemented and
passed. Until then, commands emit `HOLD` and list the missing evidence.
