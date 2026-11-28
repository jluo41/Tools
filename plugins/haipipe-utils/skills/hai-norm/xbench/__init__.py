"""
xbench -- the benchmark harness every describe-* normalizer shares.

    from xbench import NounSpec, freeze, grade, compare

WHY IT IS ONE PACKAGE AND NOT FOUR COPIES
================================================================================
`xinfo/schema.json` already says it: before the shared shape existed, _FoodInfo
and _ExerciseInfo had exactly two keys in common and a calibration benchmark
would have been written four times. The same is true of the harness. Four
things here are noun-agnostic and each was a real defect somewhere:

    the split rule       hash PatientID, never sample rows (a patient logs the
                         same string many times, so a row split grades memory)
    the circularity ban  a label the normalizer itself wrote may never be
                         graded. xbench RAISES if a spec tries.
    row and dedup        both, always, never one. They disagree, and on
                         describe-food they disagree in OPPOSITE DIRECTIONS on
                         two different cells.
    the honest denominator
                         a coverage claim needs a denominator of rows that
                         COULD have resolved.

WHAT STAYS WITH THE NOUN
================================================================================
Three things, declared in a NounSpec: how to cell the corpus, where the label
lives and what makes it circular, and what "the number is right" means. A meal
is graded on carb share of energy, an insulin on hours. Nothing else.

THE THREE QUESTIONS, KEPT APART
================================================================================
    Q1 COVERAGE   of the rows that could resolve, how many got a trusted value?
                  Needs no gold. Runs today for every noun.
    Q2 IDENTITY   did we pick the right entry out of the bank?
                  Needs HAND gold. A machine may not label it.
    Q3 VALUE      is the number right?
                  Needs a number measured on a person. Where only self-gold
                  exists, this compares two estimates and must say so.

A run that reports Q1 and calls it accuracy is the failure this docstring is
here to prevent.
"""
from .spec import NounSpec
from .split import split_of, TEST_FRACTION
from .freeze import freeze
from .grade import grade
from .compare import compare

__all__ = ["NounSpec", "split_of", "TEST_FRACTION", "freeze", "grade", "compare"]
