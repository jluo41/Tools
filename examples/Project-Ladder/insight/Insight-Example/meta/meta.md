# Example · what the extract holds

Synthetic, made by `data/make_example_data.py` (seed 7); nothing in it comes from a real dataset.

- **grain**: one row is one made-up contact: its day, its arm (A or B), its group (group_1, group_2, group_3), a 0/1
  outcome and a numeric score.
- **window**: from 2026-01-05, one day per row block, 60 rows a day.
- **sources**: none; the rows are drawn from fixed rates (arm B higher than arm A).
- **limits**: group_3 is small on purpose, so a powered question refuses it; the window is short, so a daily rate is
  thin.

What each data version adds:

- **data-v1** · first ten days: 600 rows, the first extract.
- **data-v2** · all sixteen days: 960 rows; the first ten days are the same rows as data-v1 (accumulates: yes).
