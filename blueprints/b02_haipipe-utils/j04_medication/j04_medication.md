# j04 · Medication

job-of: b02_haipipe-utils (261009)
spine: `skills/describe-medication` (0.1.1): a logged medication (a WellDoc MedicationID, an OhioT1DM class, a Shanghai free-text string) to an FDA-identified drug and a dose that states its own unit.
close: Each recorded question has a report Page with an answer status, and every answered question names the change that settled it.

## Topic

The FDA NDC Directory gives an ingredient and a pharmacologic class; the lexicon maps WellDoc's MedicationIDs.
Parked: 12.6% of rows (47,320) carry a MedicationID the lexicon lacks (871 of the 1,373 ids in administrations
are covered), RxNorm is not wired in, and dose is per administration only (MedRegimen's daily totals and ratios
are not read).

## Questions

```yaml
questions:
- id: Q01
  title: How do we cover the missing ids and read the regimen?
  question: What names the 502 MedicationIDs the lexicon lacks, would RxNorm (free, no key) make two spellings of
    one molecule provably one, and should DoseBasis per_day read MedRegimen?
  hypothesis: 'RxNorm first: it closes identity across brands and strengths; the missing ids need a source outside
    this machine; the regimen is a second pass on per_day.'
  acceptance: Answered when the missing-id share is re-measured with a named source, RxNorm is wired or ruled out
    with a reason, and per_day has a decision.
  work: []
  report: reports/q01_missing_ids_and_regimen/q01_missing_ids_and_regimen.md
```
