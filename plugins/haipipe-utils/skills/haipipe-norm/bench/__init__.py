"""
The shared benchmark engine for the describe-* family.

WHY THIS IS SHARED AND THE GOLD IS NOT
================================================================================
There are three questions to ask a normalizer, and they do not share an answer
but two of them share an ENGINE:

    B1  CONTRACT     does the door answer in the shape it promised?
                     needs NO labels.  Comparable across every noun.
    B2  GOLD         is the number right?
                     needs labels.     Comparable across NOTHING. food's 79%
                                       and medication's 86% are not the same
                                       measurement and must never be tabled
                                       side by side.
    B3  CALIBRATION  does GOOD actually beat OK?
                     needs B2's gold, but reads the DECLARED confidence_order
                     rather than a hard-coded list, so it too is written once.

So B1 and B3 live here and B2's scoring lives with its noun. This package holds
no knowledge of food, exercise, medication or insulin; what it knows is the
haipipe-norm contract, and a member declares its own instance of that contract
in `<noun>norm/bench_profile.py`.

WHAT B1 IS FOR
================================================================================
It is not a unit test. A unit test asks whether one function does what its
author meant. B1 asks whether FOUR INDEPENDENT SKILLS, written weeks apart,
still answer the same way -- and the family's whole claim, that a caller learns
one door and gets four nouns, is exactly that claim and nothing else.

The ten checks are all invariants of the contract, so a new member gets its
benchmark by declaring a profile and writing no test code at all.
"""
from .profile import Profile, load_profiles
from .contract import CHECKS, run_b1
from .report import write_bench

__all__ = ["Profile", "load_profiles", "CHECKS", "run_b1", "write_bench"]
__version__ = "1.0.0"
