# b90 · Example paper results (placeholder)

board-kind: task-block
spine: The placeholder work Runs whose returned values.csv feed Tools' Paper-Example (paper/Paper-Example/j02_evidence_value); every number here is made up.
close: Paper-Example's value Tasks read every value they print from a Run here.

## Topic

Placeholder only. A work Block computes; the paper Board's j02_evidence_value reads its returned `result/values.csv`,
whose `source` column names the Runs each value was read from (here the key `r01_source` of `src/inputs.yaml`).

## Questions

The questions this example Block answers, in two groups. Every number is made up.

```yaml
questions:
- id: Q01
  title: The sample
  group: Data
  question: How many units does the returned source hold, and in which tables?
  report: reports/q01-sample.md
  work:
  - path: j01_example_source/t01_example_source
    stage: Data
    role: Returns the source tables.
- id: Q02
  title: The main association
  group: Estimates
  question: Does <the policy> move <the outcome>, and by how much?
  report: reports/q02-main-association.md
  work:
  - path: j02_example_estimates/t01_example_main
    stage: Estimate
    role: Returns every value the paper prints.
- id: Q03
  title: The subgroup
  group: Estimates
  question: Is the association larger in <the subgroup>?
  work:
  - path: j02_example_estimates/t02_example_subgroup
    stage: Estimate
    role: Returns the same association in <the subgroup>.
```

## Deliverables

The pages a host serves for this Block, one row each; a person writes them. The explorer is the page t04_deliver
handed over, served from its address in this Block's delivery, `delivery/j02_example_estimates/t04_deliver/web/`.

```yaml
deliverables:
- {what: Example explorer, url: delivery/j02_example_estimates/t04_deliver/web/index.html, service: explorer, task: j02_example_estimates/t04_deliver}
```
