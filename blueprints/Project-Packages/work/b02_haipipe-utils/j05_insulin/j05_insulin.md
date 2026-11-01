# j05 · Insulin

job-of: b02_haipipe-utils (261009)
spine: `skills/describe-insulin` (0.1.1): an insulin product (describe-medication's DrugKey, or only a class) to pharmacokinetic parameters: class, onset, peak, duration.
close: Each recorded question has a report Page with an answer status, and every answered question names the change that settled it.

## Topic

It returns population parameters for a typical subcutaneous dose, never a curve. Parked: the insulin-on-board
convolution itself, InsulinType codes 7, 8 and 9 on 4.4% of schedule rows with no codebook, and concentration
(glargine U-300's flatter, longer profile is reached only by an explicit 'Toujeo'). Its suite here: 22 pass, 1
fails (WellDoc ids through the medication lexicon, whose bank is not on this machine).

## Questions

```yaml
questions:
- id: Q01
  title: Who turns the parameters into insulin on board?
  question: The parameters exist for an insulin-on-board series. Does a RecordFn own the convolution (a per-5-minute
    series, the same shape argued for exercise intensity), and what do the InsulinType codes and U-300 change?
  hypothesis: A RecordFn owns it and reads these parameters; this skill stays parameters only; InsulinType becomes
    a check, not an input.
  acceptance: Answered when the convolution has an owner and a first series on one cohort, and the two parked items
    each have a decision.
  work: []
  report: reports/q01_insulin_on_board/q01_insulin_on_board.md
```
