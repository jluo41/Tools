---
name: inlab-human-report
description: "Score an in-lab reading session: join responses.jsonl with the bundle's gold outcomes and compute model accuracy on the sample, clinician blind-vs-assisted accuracy, decision-influence split by model correctness (healthy reliance vs over-reliance — the safety readout), rating distributions, and time-per-case. Emits metrics.json + a markdown report. Called by /inlab-human orchestrator; also directly. Trigger: inlab report, session metrics, reader study results, /inlab-human-report."
argument-hint: "<review_bundle.json> [--responses GLOB] [--out DIR]"
allowed-tools: Bash, Read, Write, Grep, Glob
metadata:
  version: "0.1.0"
  last_updated: "2026-07-10"
---

Skill: inlab-human-report
==========================

The only stage allowed to read `gold`. Everything it computes is derivable
from the two artifacts — if a metric needs a field we didn't collect, that is
feedback-form feedback, not an excuse to improvise.

Metrics (per feedback-form.md §"What the report derives")
---------------------------------------------------------

```
MODEL      score vs gold on this sample: AUC (if both classes present),
           per-band hit rate, calibration table (band x outcome).
CLINICIAN  blind accuracy vs assisted accuracy (estimate >= cutoff as
           classifier; also decision-level: refer-rate in pos vs neg).
INFLUENCE  delta(estimate), decision-switch rate — SPLIT BY whether the model
           was right on that case:
             model-right & moved-toward  = healthy reliance
             model-wrong & moved-toward  = over-reliance   <- the safety number
             model-right & ignored       = under-reliance
EXPLANATION rating distributions (score_plausibility, explanation_quality),
           issue-taxonomy counts, would_act_on.
SESSION    time-per-case, session block answers, verbatim quotes.
```

Procedure
---------

```
1. Load bundle + all matching responses files (default glob:
   responses_<bundle_id>_*.jsonl next to the bundle).
2. Compute metrics with a small inline python script (pandas if available,
   stdlib otherwise); write <out>/metrics.json.
3. Write <out>/report.md: metrics tables + a caveats section that ALWAYS
   states: n readers, n cases, sampling design (from bundle.sampling), and
   that this is an in-lab usefulness study, NOT production-schema validation.
4. Small n (< ~20 case-readings): report counts, not percentages; say so.
```

Return contract
---------------

```
status:    ok | blocked | failed
summary:   headline numbers (model AUC, blind->assisted delta, over-reliance count)
artifacts: [metrics.json, report.md]
next:      more readers / bigger bundle, or share report with the study team
```
