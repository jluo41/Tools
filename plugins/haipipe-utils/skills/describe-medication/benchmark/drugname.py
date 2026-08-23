"""When are two drug strings the same drug?

This file is the benchmark's most consequential judgement call, so it states
every rule it applies and nothing happens implicitly. Get it wrong in the
lenient direction and the score is inflated; wrong in the strict direction and
a correct answer reads as a miss because one side wrote the salt.

    gold   Multum Lexicon    'FLUTICASONE-SALMETEROL'   'AZELASTINE OPHTHALMIC'
    ours   FDA Directory     'Fluticasone Propionate; Salmeterol Xinafoate'

Both name the same drug. Neither string contains the other.

THE COMPARISON IS ON TOKEN SETS, NOT ON STRINGS
================================================================================
Component splitting was tried first and rejected: Multum separates a
combination with '-', and the FDA uses '-' INSIDE a name ('Insulin
lispro-aabc'). A separator that is also a letter cannot be split on. Tokens
sidestep it -- {INSULIN, LISPRO, AABC} against {INSULIN, GLARGINE} is a
partial overlap either way, and F1 says how partial.

WHAT IS REMOVED BEFORE COMPARING, AND WHY EACH
================================================================================
    salts and esters      the FDA names the marketed SALT, Multum names the
                          moiety. 'METOPROLOL SUCCINATE' and 'METOPROLOL' are
                          the same drug at every granularity this benchmark
                          scores. A salt word is removed only when it is not
                          the whole name, so CALCIUM CARBONATE survives.
    route and form        Multum appends them ('AZELASTINE OPHTHALMIC'); they
                          are not part of the identity and describe-medication
                          reports Route and DosageForm in their own columns.
    strengths and units   digits never identify a molecule.

WHAT IS DELIBERATELY NOT REMOVED
================================================================================
Stereochemistry and moiety modifiers: DEXLANSOPRAZOLE is not LANSOPRAZOLE and
INSULIN LISPRO is not INSULIN GLARGINE. Folding those would hide the class of
error most worth finding, so 'Insulin lispro-aabc' against gold 'INSULIN
GLARGINE' scores F1 0.40 and exact FALSE -- partial credit for being an
insulin, no credit for being the right one.

AND A CONSEQUENCE THAT HAS TO BE STATED PLAINLY
================================================================================
Because route words ARE removed, 'oral semaglutide' equals 'SEMAGLUTIDE' at
this granularity. So describe-medication answering `oral semaglutide` for
OZEMPIC -- which is injectable, and whose oral sibling is a different product
-- scores as RIGHT here.

That is not a leniency bug, it is the granularity working: at INGREDIENT level
they are one ingredient. A formulation error is a PRODUCT error and the product
metric is what must catch it. Which is the whole reason the benchmark reports
two granularities and never one number: each is blind to exactly what the other
sees.

The exact-match rate is the headline and F1 is reported beside it, because F1
alone rewards a wrong insulin for being an insulin.
"""
import re
from typing import Set

# A salt, ester or hydrate the marketed product carries and the moiety does not.
SALTS = {
    "HYDROCHLORIDE", "HCL", "HYDROBROMIDE", "HYDRATE", "MONOHYDRATE",
    "DIHYDRATE", "ANHYDROUS", "SODIUM", "POTASSIUM", "CALCIUM", "MAGNESIUM",
    "SULFATE", "SULPHATE", "TARTRATE", "BITARTRATE", "MALEATE", "FUMARATE",
    "DIFUMARATE", "SUCCINATE", "ACETATE", "CITRATE", "PHOSPHATE", "NITRATE",
    "MESYLATE", "BESYLATE", "TOSYLATE", "XINAFOATE", "PROPIONATE",
    "DIPROPIONATE", "FUROATE", "VALERATE", "ACETONIDE", "PAMOATE", "OXALATE",
    "CHLORIDE", "BROMIDE", "CARBONATE", "GLUCONATE", "LACTATE", "STEARATE",
    "TROMETHAMINE", "ARGININE", "SALT", "SALTS", "ANHYDROUS",
}
# Route and dosage form. describe-medication has Route and DosageForm columns;
# duplicating them inside the identity would double-count.
ROUTES = {
    "ORAL", "TOPICAL", "OPHTHALMIC", "OTIC", "NASAL", "INHALATION",
    "INHALED", "INJECTION", "INJECTABLE", "SUBCUTANEOUS", "INTRAVENOUS",
    "RECTAL", "VAGINAL", "TRANSDERMAL", "SUBLINGUAL", "BUCCAL", "SYSTEMIC",
    "TABLET", "TABLETS", "TABS", "CAPSULE", "CAPSULES", "CAPS", "SOLUTION",
    "SOLN", "SUSPENSION", "SUSP", "CREAM", "OINTMENT", "GEL", "PATCH",
    "SPRAY", "DROPS", "SYRUP", "ELIXIR", "POWDER", "LOTION", "FOAM",
    "PEN", "VIAL", "KIT", "PACK", "ER", "XR", "SR", "CR", "LA", "DR", "XL",
    "HR", "RELEASE", "EXTENDED", "DELAYED", "IMMEDIATE",
}
STOP = {"AND", "OR", "WITH", "IN", "OF", "THE", "USP", "NF"}
# Strength units. `_SPLIT` already drops the digits; the unit that trailed them
# is just as much not-a-molecule, and leaving MG in the token set made
# `metFORMIN HCl 1000 MG` unequal to `metformin hydrochloride`.
UNITS = {"MG", "MCG", "UG", "GM", "ML", "MEQ", "IU", "UNIT", "UNITS", "ACT",
         "PUFF", "BASE", "HFA", "PO", "PCT", "PERCENT"}
STOP |= UNITS

_SPLIT = re.compile(r"[^A-Za-z]+")


def tokens(name) -> Set[str]:
    """A drug string reduced to the words that identify the molecule."""
    if name is None:
        return set()
    words = [w.upper() for w in _SPLIT.split(str(name)) if w]
    if not words:
        return set()
    kept = [w for w in words if w not in ROUTES and w not in STOP and len(w) > 1]
    # A salt word is dropped only if something else survives: CALCIUM CARBONATE
    # and POTASSIUM CHLORIDE are drugs, not salts of drugs.
    body = [w for w in kept if w not in SALTS]
    return set(body) if body else set(kept)


def f1(a: Set[str], b: Set[str]) -> float:
    """Token-set F1. RxMap's partial credit for combination products."""
    if not a or not b:
        return 0.0
    hit = len(a & b)
    if not hit:
        return 0.0
    p, r = hit / len(a), hit / len(b)
    return 2 * p * r / (p + r)


def same(a, b) -> bool:
    ta, tb = tokens(a), tokens(b)
    return bool(ta) and ta == tb


def ndc9(code) -> str:
    """The labeler+product half of an NDC, which is the drug; the last segment
    is the package and two packages of one drug are one drug.

    MEPS writes an unpunctuated 11-digit 5-4-2. The FDA Directory writes a
    punctuated 4-4-2 / 5-3-2 / 5-4-1 and THE DASHES ARE THE SEGMENTATION --
    stripping them shifts the product code onto a different real product,
    which is the bug that made GOOD return the wrong drug until 260821.
    """
    s = str(code or "").strip()
    if "-" in s:
        p = s.split("-")
        if len(p) >= 2 and p[0].isdigit() and p[1].isdigit():
            return p[0].zfill(5) + p[1].zfill(4)
    n = re.sub(r"\D", "", s)
    if len(n) == 11:
        return n[:9]
    if len(n) == 10:            # ambiguous 4-4-2 / 5-3-2 / 5-4-1 without dashes
        return ("0" + n)[:9]
    if len(n) >= 9:
        return n[:9]
    return ""
