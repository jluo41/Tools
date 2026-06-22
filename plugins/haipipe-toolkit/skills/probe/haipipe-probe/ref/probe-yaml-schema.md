# probe.yaml Schema

`probe.yaml` is the machine-readable state for one claim-level evidence
contract. It is not a task result archive and not a discovery archive.

The probe lifecycle is:

```text
Plan -> Gather -> Read -> Judge -> Return
```

This schema stores the structured state needed by those steps.

## Location

```text
probes/<MMDD>_<slug>/probe.yaml
```

Examples:

```text
probes/0605_discretion-gradient/probe.yaml
probes/0621_trait-diabetes/probe.yaml
```

Canonical ref:

```text
P.<MMDD>      # P.0605
```

Same-day collisions append a lowercase suffix:

```text
P.0605b
probes/0605b_trait-diabetes/
```

## Top-Level Fields

| Field | Type | Owner Step | Required | Purpose |
|---|---|---|---|---|
| `id` | string | Plan | yes | canonical probe ref, e.g. `P.0605` |
| `slug` | string | Plan | yes | short folder slug |
| `title` | string | Plan | yes | human title |
| `status` | enum | any | yes | lifecycle status |
| `created_at` | ISO string | Plan | yes | creation timestamp |
| `updated_at` | ISO string | any | yes | last update timestamp |
| `tags` | list | Plan | no | organization without group folders |
| `source` | mapping | Plan | no | where the need came from |
| `claim` | mapping | Plan | yes | hypothesis and target claim |
| `evidence_plan` | mapping | Plan | yes | needed evidence |
| `evidence_refs` | mapping | Gather | no | linked artifacts |
| `calls` | list | Gather | no | requested task/discovery work |
| `result` | mapping | Read | no | evidence summary |
| `verdict` | mapping | Judge | no | claim support verdict |
| `return` | mapping | Return | no | backfill/memory/next action |

## Status Values

```text
planned
gathering
waiting_for_evidence
ready_to_read
read
judged
returned
loop_needed
blocked
closed
```

## Skeleton

```yaml
id: P.0605
slug: discretion-gradient
title: Agreeableness effect attenuates as clinical discretion falls
status: planned
created_at: 2026-06-05T00:00:00-04:00
updated_at: 2026-06-05T00:00:00-04:00
tags:
  - opioid
  - agreeableness
  - clinical-discretion

source:
  type: paper_claim_gap      # paper_claim_gap|application_question|reviewer_objection|human_idea|task|discovery|insight
  ref: paper/Paper-Personality2Opioid-MISQ2026
  question: "Does the agreeableness prescribing signal vanish where guidelines are clear?"
  return_target: paper/Paper-Personality2Opioid-MISQ2026

claim:
  hypothesis: >
    Perceived physician Agreeableness raises opioid prescribing intensity, and
    the effect attenuates as clinical discretion falls.
  target_sentence: >
    Agreeableness is associated with higher opioid prescribing intensity in
    high-discretion encounters but not in guideline-dictated encounters.
  falsification: >
    The claim is weakened if the trait coefficient is similar or larger in
    low-discretion cohorts than high-discretion cohorts, or if real-data
    estimates are null across all cohorts.
  scope: >
    Medicare opioid prescribing cohorts with comparable SPEC5 controls.

evidence_plan:
  required:
    tasks:
      - role: high_discretion_regression
        question: "Estimate Agreeableness effect in low back pain cohort."
      - role: low_discretion_regression
        question: "Estimate Agreeableness effect in cancer cohort."
    discoveries:
      - role: prior_art_check
        question: "Has prior work already shown personality effects varying by clinical discretion?"
  optional:
    tasks: []
    discoveries: []
  success_criteria:
    support: >
      Coefficients decrease along the discretion axis and remain strongest in
      high-discretion cohorts, with real-data evidence.
    partial: >
      Direction is consistent but noisy, incomplete, or supported only on
      synthetic/plumbing evidence.
    refute: >
      Low-discretion cohorts show equal/larger effects or the high-discretion
      signal disappears.

evidence_refs:
  tasks: []
  discoveries: []
  insights: []

calls: []

result: null
verdict: null
return: null
```

## Evidence Refs

`evidence_refs` records linked artifacts. It does not move or own them.

```yaml
evidence_refs:
  tasks:
    - ref: tasks/R01_Regression_TraitOpioid/D01_reg_pipeline_visitlbp_1stpair_ols
      role: high_discretion_regression
      status: linked
      artifact: results/af14d/tables/main-ols_trait_l5_mme_ttl.csv
      note: "High-discretion cohort table."
  discoveries:
    - ref: discoveries/D0605_personality-opioid-prior-art
      role: prior_art_check
      status: requested
  insights:
    - ref: insights/K_knowledge/K03_personality-prescribing.md
      role: prior_memory
      status: linked
```

## Calls

`calls` records missing evidence work requested by the probe.

```yaml
calls:
  - type: task
    role: low_discretion_regression
    ref: tasks/R01_Regression_TraitOpioid/D21_reg_pipeline_visitcancer_1stpair_ols
    status: requested
    reason: "Needed low-discretion comparator."
  - type: discovery
    role: prior_art_check
    ref: discoveries/D0605_personality-opioid-prior-art
    status: requested
    reason: "Need outside evidence before paper claim."
```

Allowed call types:

```text
task
discovery
```

Insight is not called as evidence work during Gather. Insight may be called by
Return after the verdict is judged and approved for memory filing.

## Result Block

`result` is written by Read. It summarizes evidence; it does not commit the
claim verdict.

```yaml
result:
  status: read              # read|incomplete|blocked
  read_at: 2026-06-22T00:00:00-04:00
  evidence_summary: >
    Synthetic tables confirm plumbing across five cohorts. Substantive
    real-data evidence is not yet linked.
  task_evidence:
    - role: high_discretion_regression
      ref: tasks/...
      status: ok
      key_finding: "Table emitted on synthetic data; not substantive."
  discovery_evidence:
    - role: prior_art_check
      ref: discoveries/...
      status: missing
      key_finding: null
  missing:
    - "cms_full real-data cohort tables"
    - "prior-art discovery verdict"
  contradictions: []
  scope_notes:
    - "Synthetic evidence is plumbing-only."
```

## Verdict Block

`verdict` is written by Judge.

```yaml
verdict:
  status: partial           # yes|partial|no|blocked
  confidence: low           # high|medium|low
  structural: warn          # pass|warn|fail
  integrity: pass           # pass|warn|fail
  supported_scope: "Pipeline mechanics only."
  unsupported_scope: "Substantive agreeableness-discretion claim."
  caveats:
    - "Synthetic NPI relabel breaks substantive trait linkage."
    - "Real cms_full tables not linked."
  next_needs:
    - "Link cms_full real-data cohort tables."
    - "Complete prior-art discovery."
  judged_at: 2026-06-22T00:00:00-04:00
```

## Return Block

`return` is written by Return.

```yaml
return:
  status: pending           # pending|returned|filed_memory|loop_needed|skipped
  target:
    type: paper             # paper|application|rebuttal|insight|next_probe|none
    ref: paper/Paper-Personality2Opioid-MISQ2026
  returned_claim: >
    Current evidence confirms pipeline mechanics only; substantive claim awaits
    real-data tables.
  required_caveats:
    - "Do not use synthetic result as substantive evidence."
  actions:
    - status: skipped
      ref: insights/K_knowledge
      reason: "No judged substantive claim yet."
  returned_at: null
```

## Human Files

The probe folder should keep these human-readable files:

```text
status.md    current Probe Console panel
evidence.md  Read output
verdict.md   Judge output
return.md    Return output
```

Optional:

```text
gather.md              complex call/link decisions
INTEGRITY_AUDIT.md     long independent audit
CLAIMS_FROM_RESULTS.md claim-verifier output (Judge gate 3)
```

## Legacy Notes

Older probe files may use fields such as:

```text
design
arms
dispatch
claim
review.md
site.md
status.yaml
```

Read them during migration, but new writes should prefer the schema above.
