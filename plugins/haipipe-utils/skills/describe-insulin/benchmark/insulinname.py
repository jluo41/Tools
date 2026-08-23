"""When two insulin names are the same insulin, and when they are not.

NOT A COPY OF describe-medication's drugname.py, AND THE DIFFERENCES MATTER
================================================================================
That module folds salts and drops route words, because an oral tablet and its
hydrochloride are the same drug. Insulin names break in other places:

    a DEVICE word means nothing            LANTUS SOLOSTAR == LANTUS
    a CONCENTRATION is not the molecule    TOUJEO (U-300) is insulin glargine
    a BIOSIMILAR suffix is not a new drug  glargine-yfgn IS glargine
    a PREMIX RATIO **IS** the drug         aspart != aspart 70/30
    ISOPHANE and NPH are one word          the label uses both

The last two are the ones a generic matcher gets wrong in opposite directions:
it strips 70/30 as if it were a strength, and it treats NPH and isophane as
different molecules.

TWO QUESTIONS, DELIBERATELY SEPARATE
================================================================================
    same_molecule()   is this the same insulin? SEMGLEE vs INSULIN GLARGINE: yes
    class_of()        which action curve? and that is where a wrong answer HURTS

They come apart on purpose. Getting the molecule right and the class wrong is
not possible; getting the molecule WRONG but the class right is a small error
(lispro answered as aspart moves the curve by minutes) while getting the class
wrong is a large one (a short insulin answered as a premix misplaces a second
rise by hours). One metric could not say which happened.
"""
import re
from typing import Optional, Set

# Devices, pens and pack words. None of them is part of a molecule.
DEVICE = {
    "SOLO", "SOLOSTAR", "SOLOS", "FLEX", "FLEXPEN", "FLEXTOUCH", "KWIKPEN",
    "KWIK", "KWPN", "KWK", "PEN", "VIAL", "CARTRIDGE", "TEMPO", "MAX", "JR",
    "JUNIOR", "INJ", "INJECTION", "SOLN", "SOLUTION", "SUSP", "SUSPENSION",
    "SENSOR", "DEVICE", "DISP", "DISPOSABLE",
}

# Strength. A concentration changes the CURVE, which is why the class metric
# still catches Toujeo, but it does not change which molecule was dispensed.
STRENGTH = re.compile(r"\bU-?\d+\b|\b\d+\s*UNITS?\s*/?\s*ML\b|\b\d+\s*UNIT\b", re.I)

# Biosimilars and formulation variants: a different product, the same molecule.
# -aabc is Lyumjev (lispro), -yfgn is Semglee (glargine), 'faster' is Fiasp
# (aspart). MEPS's Multum gold names the parent molecule for all three, so a
# molecule comparison must fold them -- and `variant_of` keeps what was folded
# so the report can say the answer was MORE specific rather than wrong.
VARIANT = re.compile(r"-(AABC|YFGN|AGLR|GLARGINE|LISPRO)\b|\bFASTER\b|\bU300\b", re.I)

SYNONYM = {
    "NPH": "ISOPHANE",
    "HUMAN": "",          # 'insulin human regular' == 'insulin regular'
    "RECOMBINANT": "",
    "REC": "",
    "HUM": "",
}

# A premix ratio is part of the identity. Kept, and normalised so 70/30 and
# 70-30 are one token.
RATIO = re.compile(r"\b(\d{2})\s*[/-]\s*(\d{2})\b")


def _words(name) -> Set[str]:
    s = str(name or "").upper()
    s = RATIO.sub(lambda m: f" RATIO{m.group(1)}{m.group(2)} ", s)
    s = VARIANT.sub(" ", s)
    s = STRENGTH.sub(" ", s)
    s = re.sub(r"[^A-Z0-9]+", " ", s)
    out = set()
    for w in s.split():
        w = SYNONYM.get(w, w)
        if w and w not in DEVICE:
            out.add(w)
    return out


def molecule(name) -> Set[str]:
    """The token set that identifies the molecule (or molecules, for a premix).

    'INSULIN' alone is dropped when something else survives: every name here
    contains it, so keeping it would make every pair look 50% similar.
    """
    w = _words(name)
    return (w - {"INSULIN"}) or w


def same_molecule(a, b) -> bool:
    ta, tb = molecule(a), molecule(b)
    return bool(ta) and ta == tb


def overlap(a, b) -> float:
    """Symmetric token F1 -- partial credit, the RxMap convention.

    A premix answered as one of its two components scores about 0.67 rather
    than 0, which is the honest description of that error: half right.
    """
    ta, tb = molecule(a), molecule(b)
    if not ta or not tb:
        return 0.0
    i = len(ta & tb)
    return 0.0 if not i else 2 * i / (len(ta) + len(tb))


def variant_of(pred, gold) -> Optional[str]:
    """What the prediction added that the gold did not name.

    TOUJEO answered as 'insulin glargine u300' against a gold of 'INSULIN
    GLARGINE' is not a miss and not a plain hit: it is MORE specific than the
    answer key. Recording it stops a future reader from reading the fold as a
    bug, and stops us from claiming credit for a distinction the gold cannot
    check.
    """
    if not same_molecule(pred, gold):
        return None
    extra = VARIANT.findall(str(pred or "").upper())
    flat = [x for tup in extra for x in (tup if isinstance(tup, tuple) else (tup,)) if x]
    raw = str(pred or "").upper()
    for tag in ("AABC", "YFGN", "FASTER", "U300"):
        if tag in raw and tag not in str(gold or "").upper():
            return tag.lower()
    return flat[0].lower() if flat else None


# ---------------------------------------------------------------- the class --

# Molecule -> action curve, written HERE and not read from insnorm's PK table.
# A class gold taken from the table being graded would measure nothing. These
# six assignments are the FDA labels' own families and any diabetologist can
# audit the list in one pass.
CLASS_OF = {
    frozenset({"LISPRO"}): "rapid",
    frozenset({"ASPART"}): "rapid",
    frozenset({"GLULISINE"}): "rapid",
    frozenset({"REGULAR"}): "short",
    frozenset({"ISOPHANE"}): "intermediate",
    frozenset({"GLARGINE"}): "long",
    frozenset({"DETEMIR"}): "long",
    frozenset({"DEGLUDEC"}): "ultra_long",
}


def class_of(name) -> Optional[str]:
    """The action-curve family a molecule name implies, or None if it cannot say.

    A name naming TWO molecules is a premix -- 'INSULIN ISOPHANE-INSULIN
    REGULAR' is Novolin 70/30 -- and a bare 'INSULIN' names none, which is why
    the class metric reports its own denominator instead of scoring an
    unanswerable unit as wrong.
    """
    toks = molecule(name)
    if not toks:
        return None
    hits = [c for k, c in CLASS_OF.items() if k <= toks]
    if len(hits) > 1 or any(t.startswith("RATIO") for t in toks):
        return "premix"
    return hits[0] if hits else None
