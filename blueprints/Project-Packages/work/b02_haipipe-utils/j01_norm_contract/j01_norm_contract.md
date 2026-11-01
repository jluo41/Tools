# j01 · The normalizer contract

job-of: b02_haipipe-utils (261009)
spine: `skills/haipipe-norm` (0.4.0): the five rules, the door signature `normalize(items)`, and the shared packages every member uses.
close: Each recorded question has a report Page with an answer status, and every answered question names the change that settled it.

## Topic

haipipe-norm owns what every describe-* member obeys: free text in a cohort's own dialect, typed, resolved
against a reference bank, into numbers that carry their own provenance. It also ships the shared packages:
paths.py (where a SPACE keeps its stores), dialect.py, the inputs gallery and page, and bench/, xbench/, xinfo/.

## Questions

```yaml
questions:
- id: Q01
  title: Contract only, or shared code?
  question: The README says haipipe-norm holds the contract and no code, yet it ships paths.py, dialect.py and the
    bench packages; and describe-exercise and describe-medication still find their banks with their own _find_bank
    in constants.py, falling back to a path relative to the working directory. Which is it, and does every member
    go through paths.py?
  hypothesis: 'Shared packages are the contract''s tools: every member resolves stores through paths.py, the private
    _find_bank copies go, and the README says so.'
  acceptance: Answered when exnorm and mednorm resolve through paths.py, a missing bank names the SPACE path it
    looked for, and the README matches the folder.
  work: []
  report: reports/q01_contract_or_code/q01_contract_or_code.md
```
