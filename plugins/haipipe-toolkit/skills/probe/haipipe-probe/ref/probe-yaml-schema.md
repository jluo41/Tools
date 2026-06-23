# probe.yaml Schema

`probe.yaml` is the machine-readable state for one claim-level evidence
contract. It is not a task result archive and not a discovery archive.

The probe lifecycle is:

```text
Plan -> Gather -> Read -> Judge -> Deposit
```

This schema stores the structured state needed by those steps.

## Location

```text
probes/<LETTER><MMDD>_<slug>/probe.yaml
```

`<LETTER>` encodes the probe's source kind so the ref is self-describing.
Every probe is one of two letters:

```text
D   discovery-sourced   source.type: discovery        -> P.D<MMDD>
T   task-sourced         source.type: task             -> P.T<MMDD>
```

For a `source.type` that is neither `discovery` nor `task` (e.g.
`paper_claim_gap`, `human_idea`, `application_question`, `reviewer_objection`,
`insight`), derive the letter from the probe's PRIMARY `evidence_plan` kind:
mostly `required.tasks` -> `T`, mostly `required.discoveries` -> `D`. The letter
records what the claim is settled against, so it is always D or T.

Examples:

```text
probes/D0622_identity-concordance-steering/probe.yaml   # opened from a discovery
probes/T0621_trait-diabetes/probe.yaml                   # settled by task runs
```

Canonical ref:

```text
P.<LETTER><MMDD>      # P.D0622, P.T0621
```

Same-day collisions append a lowercase suffix:

```text
P.D0622b
probes/D0622b_hallucinated-physician-safety/
```

Legacy / back-compat: pre-convention probes have no letter
(`probes/0605_discretion-gradient/`, ref `P.0605`). They remain valid and
resolvable. Migrate a legacy probe to its letter (`P.0605` -> `P.T0605`) lazily,
on the next time it is touched, not in a mass rename.

## Top-Level Fields

| Field | Type | Owner Step | Required | Purpose |
|---|---|---|---|---|
| `id` | string | Plan | yes | canonical probe ref `P.<LETTER><MMDD>`, e.g. `P.D0622` (D=discovery, T=task); legacy letterless `P.0605` still valid |
| `slug` | string | Plan | yes | short folder slug |
| `title` | string | Plan | yes | human title |
| `kind` | enum | Plan | yes | `atomic` (one effect, one body of evidence) or `comparison` (claim across atomic verdicts) |
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
| `deposit` | mapping | Deposit | no | backfill/memory/next action |

## Status Values

```text
planned
gathering
waiting_for_evidence
ready_to_read
read
judged
deposited
loop_needed
blocked
closed
```

Legacy alias: `returned` is still accepted as equivalent to `deposited` for
back-compat with pre-v4.1 probes.

## Skeleton

```yaml
id: P.0605
slug: discretion-gradient
title: Agreeableness effect attenuates as clinical discretion falls
kind: comparison
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
  deposit_target: paper/Paper-Personality2Opioid-MISQ2026

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
deposit: null
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

## Deposit Block

`deposit` is written by Deposit.

```yaml
deposit:
  status: pending           # pending|deposited|filed_memory|loop_needed|skipped
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
  deposited_at: null
```

## Human Files

The probe folder should keep these human-readable files:

```text
status.md    current Probe Console panel
evidence.md  Read output
verdict.md   Judge output
deposit.md    Deposit output
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
