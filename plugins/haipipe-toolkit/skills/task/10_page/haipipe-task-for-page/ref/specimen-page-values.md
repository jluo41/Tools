# Specimen · one page-serving collection job (numbers ILLUSTRATIVE)

The shape of one real-looking job for the MISQ results section (page stem SM05-results). Every path
grammar is real; the coefficient values are invented for the specimen and
bind nothing.

## The batch config · one entry per stripped question

```yaml
# tasks/b90_page_service/j01_values_sm05_results/t01_collect_values/scripts/config/r01_results_batch.yaml
batch: results_batch
questions:
  - id: adjusted-effect               # consumer-neutral Result key
    qa_slug: agreeableness-effect   # bare slug; the run assigns <n> in creation
                                    # order and values.yaml records the final filename
    ask: "What is the estimated effect of physician agreeableness on opioid
          days supplied, in SD units, in the baseline pain-cohort model?"
    upstream: examples/Project-Personality-OpioidRx/tasks/R01_Reg_TraitOpioid
    extract: "results/j02_reg_pain/r01_baseline/coef_table.csv#agreeable.b"
  - id: cohort-physician-count
    qa_slug: cohort-physician-count
    ask: "How many physicians remain in the pooled five-pain-cohort analysis
          sample after exclusions?"
    upstream: examples/Project-Personality-OpioidRx/tasks/B01_CaseData_TraitOpioid
    extract: "results/j03_cohort_build/r02_pooled/sample_flow.csv#final.n_physicians"
```

## The output · values.yaml, regenerated whole per run

```yaml
# $OUTPUT_ROOT/results/t01_collect_values/r01_results_batch/values.yaml
computed: "260831 1710"
upstream:                     # pin the JOB that reported, not the block; a folder
                              # with no workflow/report.yaml records its dir mtime instead
  - examples/Project-Personality-OpioidRx/tasks/R01_Reg_TraitOpioid/D01-reg_visitlbp_1stpair · report.yaml 260828
  - examples/Project-Personality-OpioidRx/tasks/B01_CaseData_TraitOpioid · no report.yaml; dir mtime 260821
values:
  - id: adjusted-effect
    question: 1-agreeableness-effect
    value: "-0.083"
    unit: "SD opioid days per SD agreeableness"
    source: "R01_Reg_TraitOpioid/results/j02_reg_pain/r01_baseline/coef_table.csv#agreeable.b"
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
Block: B01_CaseData_TraitOpioid (existing)
Job: j03_cohort_build (existing)
Task: t04_sample_flow (new)
Produces: $OUTPUT_ROOT/results/t04_sample_flow/r02_pooled/sample_flow.csv#final.n_physicians
Needs: the five per-cohort case files j03 already builds
```

The proposal names what would be MEASURED and where it belongs; it never says
what the count is hoped to be. The next refresh Run flips
`cohort-physician-count` to `landed`
when t04 exists and reports.

## The Page-side binding

SURVEY maps the page-serving full Run id under the VALUE Evidence Item's
`Supporting Runs`. LAND validates its `values.yaml`, freezes the selected row
and hash in the item's one Local Input, executes the one local Page Evidence
Item Run, and binds the resulting ready VALUE `result.yaml`. EMBED appends the
Evidence Item id and owner-native local Run id beneath the target Bullet. A
later drifted supporting value reopens that binding through the same graph;
there is no Probe or PageX lane.
