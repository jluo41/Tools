# Specimen · one page-serving collection job (numbers ILLUSTRATIVE)

The shape of one real-looking job for the MISQ results section (page stem SM05-results). Every path
grammar is real; the coefficient values are invented for the specimen and
bind nothing.

## The batch config · one entry per stripped question

```yaml
# work/b90_page_service/j01_values_sm05_results/t01_collect_values/runs/r01_results_batch/config.yaml
batch: results_batch
questions:
  - id: adjusted-effect               # consumer-neutral Result key
    evidence_slug: agreeableness-effect   # bare slug; the run assigns <n> in creation
                                    # order and values.yaml records the final filename
    ask: "What is the estimated effect of physician agreeableness on opioid
          days supplied, in SD units, in the baseline pain-cohort model?"
    upstream: examples-2-cms/Project-Personality-OpioidRx/work/b11_CD_visit_pain_lbp/j21_C1D_reg_VisitLBP_1stPair_yr15_20_bigfive_ols/t01_C1_D_reg_VisitLBP_agre
    extract: "runs/r01_D_reg_VisitLBP_1stPair_agre_af7d_ols/result/tables/coef_table.csv#agreeable.b"
  - id: cohort-physician-count
    evidence_slug: cohort-physician-count
    ask: "How many physicians remain in the pooled five-pain-cohort analysis
          sample after exclusions?"
    upstream: examples-2-cms/Project-Personality-OpioidRx/work/b19_CD_visit_pain_pooled/j01_C1_data_VisitPain_pooled_yr15_20/t03_sample_flow_pooled
    extract: "runs/r01_sample_flow_pooled/result/sample_flow.csv#final.n_physicians"
```

## The output · values.yaml, regenerated whole per run

```yaml
# $OUTPUT_ROOT/t01_collect_values/runs/r01_results_batch/result/values.yaml
computed: "260831 1710"
upstream:                     # pin the Task that reported, not the Block; a folder
                              # with no workflow/report.yaml records its dir mtime instead
  - examples-2-cms/Project-Personality-OpioidRx/work/b11_CD_visit_pain_lbp/j21_C1D_reg_VisitLBP_1stPair_yr15_20_bigfive_ols/t01_C1_D_reg_VisitLBP_agre · report.yaml 260828
  - examples-2-cms/Project-Personality-OpioidRx/work/b19_CD_visit_pain_pooled/j01_C1_data_VisitPain_pooled_yr15_20 · no report.yaml; dir mtime 260821
values:
  - id: adjusted-effect
    question: 1-agreeableness-effect
    value: "-0.083"
    unit: "SD opioid days per SD agreeableness"
    source: "t01_C1_D_reg_VisitLBP_agre/runs/r01_D_reg_VisitLBP_1stPair_agre_af7d_ols/result/tables/coef_table.csv#agreeable.b"
    state: landed
  - id: cohort-physician-count
    question: 2-cohort-physician-count
    state: owed
    proposal: workflow/proposals.md#P1
```

## The proposal · the owed row's other half

```markdown
# workflow/proposals.md
### P1 · pooled sample flow is computed nowhere
Block: b19_CD_visit_pain_pooled (existing)
Job: j01_C1_data_VisitPain_pooled_yr15_20 (existing)
Task: t03_sample_flow_pooled (new)
Produces: $OUTPUT_ROOT/t03_sample_flow_pooled/runs/r01_sample_flow_pooled/result/sample_flow.csv#final.n_physicians
Needs: the pooled analysis table t01 already builds
```

The proposal names what would be MEASURED and where it belongs; it never says
what the count is hoped to be. The next refresh Run flips
`cohort-physician-count` to `landed`
when t03 exists and reports.

## The Page-side binding

SURVEY maps the page-serving full Run id under the VALUE Evidence Item's
`Supporting Runs`. LAND validates its `values.yaml`, freezes the selected row
in the item's one Local Input, executes the one local Page Evidence
Item Run, and binds the resulting ready VALUE `result.yaml`. EMBED appends the
Evidence Item id and owner-native local Run id beneath the target Bullet. A
later drifted supporting value reopens that binding through the same graph;
there is no Probe or PageX lane.
