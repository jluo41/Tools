# j02 · Food

job-of: b02_haipipe-utils (261009)
spine: `skills/describe-food` (0.7.0): a FoodName in any cohort's dialect to USDA nutrition through the bank ladder, with a confidence word per answer.
close: Each recorded question has a report Page with an answer status, and every answered question names the change that settled it.

## Topic

FoodName resolves through a ladder of banks (USDA FDC, the branded table T3, the China table T_CN) to six
nutrients, each with its provenance and a confidence word; 0.7.0 added the word check (first pick right 74.1% to
77.1% of codes on the WellDoc answer key). The SKILL lists three open gaps.

## Questions

```yaml
questions:
- id: Q01
  title: Which foods still miss, and what closes each gap?
  question: 'Three gaps stay open: branded items inside meals of several foods (a per-100 g figure without grams
    cannot join T0''s servings), Chinese composite dishes no public composition table lists, and eight more nutrients
    the WellDoc rows carry (added sugars, sodium, four kinds of fat, cholesterol, potassium) plus a glycemic-index
    table waiting on a licence check. Which to close first, and how?'
  hypothesis: Branded items in multi-food meals first (they touch the most rows), then the extra nutrients from
    tiers that already carry them; composite dishes stay a known miss.
  acceptance: Answered when each gap has a measured row count, a chosen route or an explicit 'stays open', and the
    L3 benchmark floors still hold.
  work: []
  report: reports/q01_food_gaps/q01_food_gaps.md
```
