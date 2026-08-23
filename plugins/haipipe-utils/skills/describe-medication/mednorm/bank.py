"""
The two reference files, held in memory.

    fda_ndc_product.parquet   115,496 FDA products -- the BANK, external
    med_lexicon.parquet          871 MedicationID  -- the LEXICON, ours

Both are small enough to load whole (4.7 MB and 42 KB) and are cached, so a
service resolves a whole cook against one load.
"""
import functools
import re
from typing import Dict, Optional

import pandas as pd

from .constants import BANK, LEXICON


def norm(s) -> str:
    """Fold a drug string for comparison: lowercase, punctuation to space,
    whitespace collapsed."""
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", str(s).lower())).strip()


def ndc_candidates(ndc):
    """A logged NDC -> the 9-digit normalised heads (labeler+product) it could be.

    THE DASHES ARE THE SEGMENTATION, AND THROWING THEM AWAY RETURNS WRONG DRUGS.
    An earlier version stripped every non-digit and split by total length. For
    '13668-031-0' that produced '136680310', which shifts the product code one
    digit left and lands on a DIFFERENT REAL PRODUCT -- the row resolved, at the
    GOOD confidence tier, to celecoxib instead of topiramate. Four more like it:

        simvastatin  -> Amoxicillin and Clavulanate Potassium
        hydroxyzine  -> Methylphenidate Hydrochloride
        duloxetine   -> Pramipexole Dihydrochloride
        metformin    -> Glyburide and Metformin Hydrochloride

    A wrong answer that looks completely legitimate is the worst failure this
    package can produce, and the segmentation needed to avoid it was written in
    the string the whole time. Measured over the lexicon: 675 of 871 NDCs carry
    dashes, in three shapes -- 4-4-1 (369), 5-3-1 (220) and 5-4-0 (85), the last
    with the package segment simply truncated away.

    With dashes: labeler and product are read off directly and padded to 5 and 4.
    Without: fall back to splitting by total length, which is a guess and is why
    several candidates are returned rather than one.
    """
    raw = str(ndc).strip()
    parts = [p for p in raw.split("-")]
    if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
        return [parts[0].zfill(5) + parts[1].zfill(4)]

    n = re.sub(r"\D", "", raw)
    if len(n) == 9:
        return [n]
    if len(n) == 11:
        return [n[:9]]
    if len(n) == 10:
        return [("0" + n)[:9], (n[:5] + "0" + n[5:])[:9], n[:9]]
    if len(n) == 8:
        return ["0" + n]
    return []


@functools.lru_cache(maxsize=2)
def _fda():
    df = pd.read_parquet(BANK)
    by_ndc, by_gen, by_brand = {}, {}, {}
    for r in df.itertuples(index=False):
        rec = {
            "Ingredient": r.NONPROPRIETARYNAME,
            "BrandName": r.PROPRIETARYNAME,
            "PharmClass": r.PHARM_CLASSES,
            "DosageForm": r.DOSAGEFORMNAME,
            "Route": r.ROUTENAME,
            "Substance": getattr(r, "SUBSTANCENAME", None),
        }
        if r.ndc9 and r.ndc9 not in by_ndc:
            by_ndc[r.ndc9] = rec
        g = norm(r.NONPROPRIETARYNAME)
        if g and g not in by_gen:
            by_gen[g] = rec
        b = norm(r.PROPRIETARYNAME)
        if b and b not in by_brand:
            by_brand[b] = rec
    return by_ndc, by_gen, by_brand


@functools.lru_cache(maxsize=2)
def _lexicon() -> Dict[str, Dict]:
    df = pd.read_parquet(LEXICON)
    return {str(int(r.MedicationID)): {"MedicationName": r.MedicationName,
                                       "NDC": r.NDC}
            for r in df.itertuples(index=False)}


def lexicon_lookup(medication_id) -> Optional[Dict]:
    return _lexicon().get(str(medication_id))


def by_ndc(ndc) -> Optional[Dict]:
    book = _fda()[0]
    for c in ndc_candidates(ndc):
        if c in book:
            return book[c]
    return None


def by_generic(name) -> Optional[Dict]:
    return _fda()[1].get(norm(name))


def by_brand(name) -> Optional[Dict]:
    return _fda()[2].get(norm(name))


def by_generic_prefix(name) -> Optional[Dict]:
    """'ATORVASTATIN' -> 'Atorvastatin Calcium'. A logged name is often the
    ingredient without its salt, and the salt does not change the ingredient.

    ONLY when the prefix picks out exactly ONE ingredient. 'insulin' is a prefix
    of a dozen different insulins and must stay a miss, which is why an
    ambiguous prefix returns None rather than the first hit.
    """
    key = norm(name)
    if len(key) < 6:
        return None
    gens = _fda()[1]
    # Deduplicate on the NORMALISED ingredient. 'Atorvastatin Calcium',
    # 'ATORVASTATIN CALCIUM' and 'Atorvastatin calcium' are three raw strings
    # and one ingredient; keying on the raw string made every such drug look
    # ambiguous and returned None.
    hits = {}
    for k, v in gens.items():
        if not (k == key or k.startswith(key + " ")):
            continue
        g = norm(v["Ingredient"])
        # A COMBINATION product is a different drug, not a spelling of this one.
        # 'lisinopril' prefixes 'lisinopril and hydrochlorothiazide', and
        # returning that would put a second active ingredient into the record.
        if " and " in f" {g} " or "hctz" in g:
            return None
        # Collapse a trailing qualifier: 'atorvastatin calcium' and
        # 'atorvastatin calcium film coated' are one ingredient in two dress
        # codes. Two tokens is enough to keep salts apart
        # ('bupropion hcl' vs 'bupropion hydrobromide' stay distinct).
        hits.setdefault(" ".join(g.split()[:2]), v)
    return next(iter(hits.values())) if len(hits) == 1 else None


def stats():
    n, g, b = _fda()
    return {"ndc": len(n), "generic": len(g), "brand": len(b),
            "lexicon": len(_lexicon())}
