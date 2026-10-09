# j03 · Exercise

job-of: b02_haipipe-utils (261009)
spine: `skills/describe-exercise` (0.5.0): a logged activity (free text or vendor code) to a PA Compendium MET, and kcal when minutes and body mass are known.
close: Each recorded question has a report Page with an answer status, and every answered question names the change that settled it.

## Topic

Over all 136,555 Exercise rows, 95.3% of the 42,799 resolvable rows resolve (the rest are device roll-ups and
rows that name nothing). It refuses the code join that would price 1,218 workouts as a church supper, and keeps
the daily roll-ups out of the MET denominator. Parked: Google_Fit's 24 opaque codes, Validic 9002's blank label,
the fuzzy tier that cannot name 'Sports', a confidence capped at OK because the bank is a mirror, and a bare
noun read as moderate effort.

## Questions

```yaml
questions:
- id: Q01
  title: Can MET come from the log itself, not only the book?
  question: 'Two routes need no Compendium name: CaloriesBurned with body mass and minutes back-solves MET for 24,253
    WellDoc rows, and CGMacros carries 657,789 rows of device-estimated MET at one-minute cadence. Should exercise
    use them, and as what tier?'
  hypothesis: Yes, as tiers of their own, ranked above the bare-noun default and labelled as device or back-solved,
    never mixed with a Compendium pick.
  acceptance: Answered when both routes are measured against the Compendium picks on the rows that have both, and
    a tier order is chosen.
  work: []
  report: reports/q01_met_from_the_log/q01_met_from_the_log.md
```
