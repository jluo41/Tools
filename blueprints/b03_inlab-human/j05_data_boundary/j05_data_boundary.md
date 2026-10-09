# j05 · The data boundary

job-of: b03_inlab-human (261009)
spine: What may enter a bundle or the console: de-identified cases only, outcome fields scrubbed from the patient store, study data kept in the study's repository.
close: Each recorded question has a report Page with an answer status, and every answered question names the change that settled it.

## Topic

The plugin never de-identifies for you. The patient-store extractor scrubs outcome fields (Label, Split,
ground_truth) from every table, which caught a real gold leak; per-patient scores and responses stay in the
study repository, never in the plugin.

## Questions

```yaml
questions:
- id: Q01
  title: What may enter a bundle or the console, and who checks?
  question: Cases must be de-identified before they enter a bundle or the console, and the plugin does not check
    it. What check runs at the boundary, and what does it refuse?
  hypothesis: A boundary check in the bundle builder and the patient-store extractor that refuses identifying columns
    and outcome fields, with its own test.
  acceptance: Answered when a bundle or store with an identifying or outcome column is refused by a tested check.
  work: []
  report: reports/q01_boundary_check/q01_boundary_check.md
```
