# review_bundle.json — frozen-bundle contract (v0.1)

One bundle = one reading session's worth of cases, fully materialized **before** any
clinician sits down. Produced by `/inlab-human-bundle`; consumed read-only by
`/inlab-human-review`. The reader never calls a live endpoint.

## Top level

```jsonc
{
  "schema_version": "0.1",
  "bundle_id": "adhd-pilot-r1",            // stable id; appears in every response row
  "created": "2026-07-10T21:00:00-04:00",  // stamped at build time
  "model": {
    "endpoint_name": "reach.adhd.xgb",     // Endpoint_Set name
    "endpoint_version": "v0003",
    "endpoint_url_used": "http://localhost:5000/invocations",  // provenance only
    "task_description": "Risk of ADHD diagnosis within the prediction horizon, scored at a pediatric primary-care visit",
    "horizon": "24 months"
  },
  "sampling": {
    "source": "3-CaseStore/<caseset>",      // provenance of the de-id cases
    "design": "stratified: pred_band {high,med,low} x outcome {pos,neg}",
    "n_cases": 30,
    "note": "includes model-WRONG cells (high-score negatives, low-score positives)"
  },
  "blinding": {
    "case_order": "shuffled at build time",   // fixed thereafter — every reader sees same order
    "gold_hidden": true                        // reader skill must never print .gold
  },
  "cases": [ /* Case objects, see below */ ]
}
```

## Case object

Three strictly separated blocks — the review skill's reveal discipline depends on this:

| Block | Shown when | Rule |
|---|---|---|
| `presentation` | **blind pass** | raw chart data only — nothing model-derived |
| `model_output` | **assisted pass** (after blind responses are captured) | score + SHAP + narrative |
| `gold` | **never during a session** | only `/inlab-human-report` reads it |

```jsonc
{
  "case_id": "C007",                    // de-identified, stable within bundle
  "strata": { "pred_band": "high", "outcome": "pos" },   // for the report; not shown

  "presentation": {
    "demographics": { "age": "6y", "sex": "M" },          // de-id-safe granularity
    "visit_context": "well-child visit 2024-03",          // the trigger visit
    "problem_list": [ { "code": "F90.-adjacent...", "label": "...", "date": "..." } ],
    "medications":  [ { "label": "...", "start": "...", "status": "..." } ],
    "measurements": [ { "label": "...", "value": ..., "unit": "...", "date": "..." } ],
    "questionnaires": [ { "instrument": "...", "item_or_score": "...", "date": "..." } ],
    "visit_history": [ { "date": "...", "type": "...", "note_hint": "..." } ]
  },

  "model_output": {
    "risk_score": 0.72,                  // verbatim from endpoint-predict; never LLM-touched
    "risk_band": "high",                 // banding rule recorded in model block if used
    "attribution_available": true,       // false when the endpoint returns no attributions
    "shap_top": [                        // top-k attributions, signed; [] when unavailable
      { "feature": "...", "case_value": "...", "shap": 0.18 }
    ],
    "narrative": "…",                    // narrator agent output (consumes the above only;
                                         //  without SHAP it may describe, not attribute)
    "narrative_agent": "inlab-narrator-agent@<version>",
    "endpoint_response_raw": { }         // full response for audit (PostFn output verbatim)
  },

  "gold": {
    "outcome": 1,                        // did the target event occur within horizon
    "outcome_detail": "ADHD dx recorded at month 14",
    "label_source": "retrospective CaseStore label"
  }
}
```

## Invariants (build-time checks in `/inlab-human-bundle`)

1. Every case has all three blocks; `gold.outcome` ∈ {0,1}.
2. `presentation` contains **no** model-derived field (no scores, bands, SHAP echoes).
3. `model_output.risk_score` equals the endpoint-predict tool's raw response (recorded
   side-by-side in the build log for audit).
4. Case ids are de-identified and carry no dates more precise than the presentation needs.
5. Stratification cells are non-empty as designed, and at least one model-wrong cell exists.
6. The bundle validates before freeze; a frozen bundle is never edited — build a new
   `bundle_id` instead.
