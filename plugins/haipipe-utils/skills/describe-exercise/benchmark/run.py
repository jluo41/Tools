#!/usr/bin/env python3
"""
Grade describe-exercise.

    python run.py --freeze --full     # first time: build the corpus, grade all
    python run.py --full
    python run.py --n 2000 --tag probe

Corpus in  _ExerciseInfo/2-corpus/
Runs   in  _ExerciseInfo/6-benchmark/runs/
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from spec import SPEC

from xbench.grade import cli

ROOT = Path("/home/jluo41/WellDoc-SPACE")
INFO = ROOT / "_WorkSpace/0-RawDataStore/0-EventNorm/_ExerciseInfo"

if __name__ == "__main__":
    cli(SPEC, corpus_dir=INFO / "2-corpus", out_dir=INFO / "6-benchmark", root=ROOT)
