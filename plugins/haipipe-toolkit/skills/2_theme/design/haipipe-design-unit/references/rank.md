⑤ Review whole · `run-rank-t99`
===============================

The last step of a Job's work, in `t99_review-whole/`, by the reviewer agent in a context that generated nothing in
this Job. It looks at the designs together: which N to keep, in which order, and what each is expected to do.


What it reads
-------------

- every design Task whose last verify passed: its draft (the last generate or revise), its `elements.yaml`, its
  review;
- the Job's face `n` (N, the same as `inputs/goal.md`), `inputs/method.md` (the ⑤ choice: the ranking rule, how
  many to keep, and whether T3 pretest runs), the manifest.


What it writes
--------------

```text
runs/run-rank-t99/result/
├── ranking.csv     rank,design,predicted,why,kept
└── coverage.md     do the kept N cover the goal; no two alike; every input used where it should be;
                    T3 pretest on the kept, when the method's ⑤ asks for it
```

```text
rank,design,predicted,why,kept
1,d04,+x [lo; hi],<why it ranks here>,yes
2,d01,+x [lo; hi],<why>,yes
…
15,d09,+x [lo; hi],<why it is dropped>,no
```

`predicted` is the expected effect against the control as a direction and a range, never a single number with no
range; `kept` is `yes` or `no`, and exactly N rows say `yes`.


Rules
-----

1. **Another agent.** Rank runs where no design of this Job was generated or revised; a rank in the generating
   context is refused (return a hold).
2. **Only passed designs.** A design with no passed verify is not ranked; say which and why in `coverage.md`.
3. **A prediction is a forecast.** It is a draft until a person releases the design; the workflow projects each row
   into the Task's `prediction.yaml` (`frozen: draft`) and `state: kept | dropped`, and `run-freeze-predictions-jNN`
   freezes it at the release. Rank writes none of those.
4. **Dropped designs stay.** A dropped design keeps its Task, folded at the end; nothing is deleted.
5. **T3 lives here.** When the method's ⑤ asks for a pretest, it runs once per Job, on the kept designs, and its
   findings go in `coverage.md`; a verify never runs T3.
6. **Writes only `result/`** and `by:` · `status:` on its own card.

Check: `python3 scripts/check_unit.py --ladder-result <Job>/t99_review-whole/runs/run-rank-t99`.
