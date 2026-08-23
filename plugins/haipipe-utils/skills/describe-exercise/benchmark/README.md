describe-exercise / benchmark
================================================================================

The noun-specific half. The harness is shared: `haipipe-norm/xbench`.

```text
  taxonomy.py                 KIND x LABEL. Classifies from the CODEBOOKS only,
                              never by calling the resolver, so the corpus is a
                              fact about the data and not about dialect.py.
  spec.py                     the NounSpec, including the augment that joins
                              Weight.parquet and back-solves the device MET
  check_gold_independence.py  ⚠️ RUN THIS FIRST. Exits non-zero if any vendor's
                              logged kcal turns out to be a MET-table lookup,
                              which would make the gold the prediction.
  run.py                      the CLI
```

Data lives under `_ExerciseInfo/`, where `6-benchmark/code` symlinks back here.

```bash
source .venv/bin/activate && source env.sh
python check_gold_independence.py && python run.py --freeze --full
```

WHY THIS NOUN HAD TO BUILD ITS OWN GOLD
--------------------------------------------------------------------------------
No public corpus of free-text exercise logs coded to the Compendium exists
(searched 260822). T1DEXI is the closest and carries no MET label. So the gold
is back-solved from vendor kcal, and the independence check is not optional
paranoia -- it is the only thing standing between this benchmark and the trap
describe-food fell into.

WHAT THE HEADLINE MEANS
--------------------------------------------------------------------------------
r 0.440 against a ceiling of 0.683. The ceiling is the best any activity-name-
only predictor can reach on this gold, because the Compendium publishes one
number per activity and two people doing the same activity do not burn the same
energy. Quote the 0.440 without the 0.683 and it reads as a weak resolver
rather than a mostly-saturated one.
