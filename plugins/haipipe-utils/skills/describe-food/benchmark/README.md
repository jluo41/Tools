describe-food / benchmark
================================================================================

The noun-specific half of describe-food's benchmark. The harness is shared:
`haipipe-norm/xbench`. This directory declares only the three things xbench
cannot know.

```text
  taxonomy.py          SHAPE x LABEL -- how this noun's corpus is celled.
                       Moved here 260822 from the AY1_foodrec_v1 task; the old
                       path is a shim that re-exports from this file.
  spec.py              the NounSpec: which columns, what is circular, what
                       "the number is right" means (carb share of energy)
  build_train_bank.py  a TRAIN-PATIENTS-ONLY copy of the observed food bank
  run.py               the CLI

  build_units.py       ⭐ 260822. The UNIT INVENTORY: 2-corpus/, one folder per
                       corpus. A Diet row is a MEAL, so this is the only place
                       on the board that runs split_meal() to turn rows into
                       the THINGS the door is actually asked to resolve.
  check_gold_independence.py
                       ⭐ 260822. The gate. Three failure modes, and a POSITIVE
                       CONTROL that must fail or the run is void.
  build_cgmacros_ruler.py
                       ⭐ 260822. E4, through STAGE 0. The only L1 gold on the
                       board and the only ruler the TEXT door cannot reach.
```

Data -- the frozen corpus, the train bank, the runs, the report -- lives under
`_WorkSpace/0-RawDataStore/0-EventNorm/_FoodInfo/`, where `6-benchmark/code` is
a symlink back to this directory.

```bash
source .venv/bin/activate && source env.sh
python build_train_bank.py
python build_units.py                  # the inventories -> 2-corpus/
python check_gold_independence.py      # the gate; exits 1 on contamination
python build_cgmacros_ruler.py         # the photo ruler; --replay to re-score free
python run.py --full
```

WHY build_train_bank.py EXISTS
--------------------------------------------------------------------------------
foodnorm's T0 tier resolves against `foodbank_observed`, harvested from the
board's own logged food strings. Splitting patients protects the matcher, not
the bank. Against the production bank, 98.3% of gold_macros names the train
split never saw still came back MEASURED. So the benchmark builds its own bank
from train patients only and points `FOODNORM_OBSERVED_DB` at it, importing
every rule from the real builder so the two can differ only in which patients
they saw.

WHY check_gold_independence.py CARRIES A POSITIVE CONTROL
--------------------------------------------------------------------------------
Three separate contaminations were shipped and then caught on this noun, each
one only after a number came back too good:

```text
  written by the door   Shanghai. NutritionSource is non-null in the frame.
  same table            FNDDS. Our USDA sqlite ships survey_fndds_food, one row
                        per FNDDS code. 0.31 carb MAE, median exactly 0.00.
  same upstream vendor   WellDoc. Splitting PATIENTS does not split SOURCES: the
                        T0 bank holds FatSecret's number for 'banana' and
                        FatSecret supplied the patient's label. 79.5% of units
                        matched to within 0.01 g.
```

A detector for those is easy to write and easy to write WRONG, and a wrong one
is worse than none because it certifies. So the gate re-resolves FNDDS against
the production bank, where the leak is still present, and REQUIRES that reading
to come back CONTAMINATED. It reads 90.5% exact, median 0.00. If it ever reads
INDEPENDENT the detector is broken and every other line of the report is void.

WHY build_cgmacros_ruler.py BANKS ITS NAMES
--------------------------------------------------------------------------------
The model call is the expensive part of the photo lane and the least likely
thing to need repeating: every methodology fix downstream -- a different bank, a
corrected gold filter, a calibration -- changes what happens AFTER the name. So
every name is written to `2-corpus/CGMacros/_names_book.json` and `--replay`
re-scores from it without touching the model. Without that, each correction
costs a fresh run of the same photos, which is how a benchmark quietly becomes
too expensive to correct.

Auth is OAuth through the `claude` CLI, never an API key; `imagename` strips the
three key variables from the subprocess so a proxy in env.sh cannot take over.
