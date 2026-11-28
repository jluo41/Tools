# Method · eFigure 2

## Message
In <the subgroup> the association with <the policy> is larger than in the whole sample, and its interval is wider,
so the paper's answer to RQ2, for whom it changes, rests on fewer units.

## Data
<The data source>, years <YYYY to YYYY>: the work Runs b90.j02.t01.r01 and b90.j02.t02.r01, each its
result/values.csv (placeholder).

## Sample
- the whole sample, 12480 units, as in Display A
- <the subgroup>, 3120 units

## Method
The main model, fitted once in everyone and once in <the subgroup>; each estimate with its 95% interval.

## Made by
- `r01_example_main/result/values.csv` (main.b, main.ci_lo, main.ci_hi, sample.n_units), the Run of `work/b90_example_paper_results/j02_example_estimates/t01_example_main/`
- `r01_example_subgroup/result/values.csv` (sub.b, sub.ci_lo, sub.ci_hi, sub.n_units), the Run of `work/b90_example_paper_results/j02_example_estimates/t02_example_subgroup/`
- `scripts/draw_subgroup_estimate.py`, the worker of `t51_display-d-subgroup-estimate/`

## Numbers
Every point and interval is read from the two values.csv files above; nothing is typed in.
