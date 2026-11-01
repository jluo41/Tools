# j07 · The reference banks

job-of: b02_haipipe-utils (261009)
spine: The banks every member resolves against, kept in a SPACE's `_WorkSpace/ExternalStore`: USDA FDC with its branded and China tables, the PA Compendium mirror, the FDA NDC medbank, the insulin PK table.
close: Each recorded question has a report Page with an answer status, and every answered question names the change that settled it.

## Topic

None of these banks is in DrFirst-SPACE's ExternalStore, so here the food suite cannot open its database,
exercise fails 24 checks and medication 17, all for a missing bank rather than a wrong answer. The banks live
where the cohorts are.

## Questions

```yaml
questions:
- id: Q01
  title: Where do the banks live, and how does a SPACE get them?
  question: Which SPACE and host holds each bank and its version, how does another SPACE fetch or mount them, and
    how does a member say 'bank absent' instead of failing every check?
  hypothesis: One manifest per bank (source, version, licence, where it lives), a fetch script per bank, and suites
    that skip with one line when their bank is absent.
  acceptance: 'Answered when each bank has a manifest and a fetch path, and the suites on a SPACE without banks
    report ''skipped: no bank''.'
  work: []
  report: reports/q01_where_the_banks_live/q01_where_the_banks_live.md
```
