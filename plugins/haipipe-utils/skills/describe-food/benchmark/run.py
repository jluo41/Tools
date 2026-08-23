#!/usr/bin/env python3
"""
Grade describe-food.

    python run.py                 # 600 rows per cell per weighting
    python run.py --n 2000
    python run.py --full          # every test row, slow
    python run.py --tag gate_a    # name the run
    python run.py --freeze        # rebuild the frozen corpus first

Corpus in  _FoodInfo/2-corpus/     (frozen; a corpus that moves grades nothing)
Bank   is  _FoodInfo/6-benchmark/observed_train.parquet  (train patients only)
Runs   in  _FoodInfo/6-benchmark/runs/
"""
import os
import sys
from pathlib import Path

ROOT = Path("/home/jluo41/WellDoc-SPACE")
INFO = ROOT / "_WorkSpace/0-RawDataStore/0-EventNorm/_FoodInfo"

# BEFORE foodnorm is imported, or the bank path is already resolved and cached.
#
# The observed bank is a SECOND PATH from the test labels into the prediction:
# it is harvested from the board's own logged rows, so grading against those
# rows returns the label. Splitting patients protects the matcher and not the
# bank. Measured 260822: 98.3% of gold_macros names the train split never saw
# came back MEASURED against the full bank.
_TRAIN_BANK = INFO / "6-benchmark/observed_train.parquet"
if not _TRAIN_BANK.exists():
    sys.exit(f"missing {_TRAIN_BANK}\nrun:  python build_train_bank.py")
os.environ["FOODNORM_OBSERVED_DB"] = str(_TRAIN_BANK)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from spec import SPEC

from xbench.grade import cli

if __name__ == "__main__":
    cli(SPEC, corpus_dir=INFO / "2-corpus", out_dir=INFO / "6-benchmark", root=ROOT)
