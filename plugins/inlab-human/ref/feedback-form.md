# feedback-form — response contract (v0.1)

What `/inlab-human-review` collects, per case and per session, and the exact
`responses.jsonl` row shape. The skill asks these conversationally but records them
**structurally** — chat prose is quotable color, the JSONL row is the data.

## Design rules

1. **Blind before assisted, always.** Blind answers are captured (written to the row) before
   anything model-derived is shown. No retroactive edits to blind fields.
2. **Score and explanation are rated separately.** If a clinician distrusts the tool we must
   know *which part* — the number or the story about the number.
3. **Every case yields a complete row**, even when the clinician declines an estimate
   (`"declined"` is a value, and diagnostic in itself).

## Per-case flow and fields

### Pass 1 — BLIND (presentation block only)

| Field | Type | Prompt (gist) |
|---|---|---|
| `blind.risk_estimate` | 0–100 (or `"declined"`) | "Your gut risk that this child develops ADHD within 24 months?" |
| `blind.decision` | enum: `refer` \| `monitor_closely` \| `routine_care` | "What would you actually do at this visit?" |
| `blind.confidence` | 1–5 | "How confident are you?" |
| `blind.rationale` | free text (short) | "What drives your estimate?" |

### Reveal — model_output block (score + SHAP + narrative)

### Pass 2 — ASSISTED

| Field | Type | Prompt (gist) |
|---|---|---|
| `assisted.risk_estimate` | 0–100 | "Given the model's output, your estimate now?" |
| `assisted.decision` | same enum | "And your action now?" |
| `assisted.confidence` | 1–5 | |
| `rating.score_plausibility` | 1–5 | "Is the model's *number* clinically plausible for this case?" |
| `rating.explanation_quality` | 1–5 | "Does the *explanation* (SHAP + narrative) make clinical sense?" |
| `rating.explanation_issues` | multi: `spurious_feature` \| `missing_key_factor` \| `wrong_direction` \| `overconfident_language` \| `none` | "Anything off in the explanation?" |
| `rating.would_act_on` | 1–5 | "Would you let this output influence a real decision?" |
| `case_notes` | free text | anything else — verbatim |

## `responses.jsonl` row

One line per (reader, case), appended at case completion; never rewritten:

```jsonc
{
  "schema_version": "0.1",
  "bundle_id": "adhd-pilot-r1",
  "case_id": "C007",
  "reader_id": "R01",                      // pseudonymous; roster kept outside the repo
  "started": "...", "completed": "...",    // wall-clock, for time-per-case
  "blind":    { "risk_estimate": 35, "decision": "monitor_closely", "confidence": 3, "rationale": "..." },
  "assisted": { "risk_estimate": 60, "decision": "refer", "confidence": 4 },
  "rating":   { "score_plausibility": 4, "explanation_quality": 2,
                "explanation_issues": ["spurious_feature"], "would_act_on": 3 },
  "case_notes": "..."
}
```

## Per-session wrap-up (once, after the last case)

| Field | Type |
|---|---|
| `session.overall_trust` | 1–5 |
| `session.fit_in_workflow` | 1–5 + free text ("where in your day would this live?") |
| `session.top_concern` | free text |
| `session.keep_using` | yes / no / with-changes + free text |

Appended as one `"type": "session"` row keyed by `bundle_id` + `reader_id`.

## What the report derives from this (so we collect nothing decorative)

- Model accuracy on the sample: `model_output.risk_score` vs `gold` (AUC, calibration-in-band).
- Clinician accuracy blind vs assisted: does the model **help**, hurt, or get ignored?
- Influence: Δ(risk_estimate), decision-switch rate — split by whether the model was *right*
  (healthy reliance vs over-reliance on wrong scores — the key safety readout).
- Explanation diagnostics: `explanation_quality` distribution + issue taxonomy.
- Adoption signal: `would_act_on`, session block, time-per-case.
