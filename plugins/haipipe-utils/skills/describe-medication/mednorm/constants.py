"""
The fixed vocabulary of this normalizer: what a logged medication row can BE,
how sure we are, and on what scale a dose is reported.
"""
import os
from pathlib import Path


def _find(rel):
    """Resolve a store-relative path. EXPLICIT env var, then the workspace's
    LOCAL_EXTERNAL_STORE, then a walk up from this file. Always absolute -- a
    service must be startable from any directory."""
    explicit = os.environ.get("MEDNORM_DB")
    if explicit:
        p = Path(explicit) / rel if Path(explicit).is_dir() else Path(explicit)
        return p.resolve()
    roots = []
    store = os.environ.get("LOCAL_EXTERNAL_STORE")
    if store:
        roots.append(Path(store))
        roots += [a / store for a in Path(__file__).resolve().parents]
    roots += [a / "_WorkSpace" / "ExternalStore" for a in Path(__file__).resolve().parents]
    for r in roots:
        if (r / rel).exists():
            return (r / rel).resolve()
    return (Path("_WorkSpace/ExternalStore") / rel).resolve()


BANK = _find(Path("medbank") / "fda_ndc_product.parquet")   # FDA, external
LEXICON = _find(Path("medbank") / "med_lexicon.parquet")    # ours

# --------------------------------------------------------- what a row IS -----
# Rule 2 of haipipe-norm: TYPE, DO NOT DELETE.
CODED = "coded"            # a WellDoc MedicationID. resolvable via the lexicon.
NAMED = "named"            # a drug name in text. Shanghai, or a resolved id.
CLASS_ONLY = "class_only"  # OhioT1DM's 'Basal Insulin' -- a CLASS, never a product.
                           #   It can never reach the FDA bank and must not read
                           #   as a bank miss; describe-insulin serves it directly.
SENTINEL = "sentinel"      # 255 / -1 / 999 in Dose, or a placeholder id.
PLACEHOLDER = "placeholder"
TYPES = (CODED, NAMED, CLASS_ONLY, SENTINEL, PLACEHOLDER)

# ------------------------------------------------------ how sure we are ------
# Rule 3: only these may be written into value columns.
GOOD, OK, ALIAS, WEAK, MISS = "GOOD", "OK", "ALIAS", "WEAK", "MISS"
TRUSTED = (GOOD, OK, ALIAS)

# GOOD is REACHABLE here, unlike in describe-exercise, and the difference is the
# bank: this one is the FDA's own file, fetched from accessdata.fda.gov, not a
# third-party mirror. An NDC that resolves in the Directory is as good as this
# kind of evidence gets, so tier A earns GOOD. A name-string match does not: two
# products can share a generic name and differ in salt, strength and route.

# ------------------------------------------------------------ the scale ------
# Rule 4: BASIS IS A COLUMN.
#
# `Dose` arrives as a bare float with NO unit column anywhere in the pipeline,
# and the unit is a property of the DRUG, not of the log:
#     insulin      median 7    -> international units
#     everything   median 1    -> tablets / actuations taken, NOT milligrams
# Writing 7 without saying which is the same defect as reading a per-100g
# nutrition composition as a per-meal dose.
IU, MG, G, ML, COUNT = "iu", "mg", "g", "mL", "count"
UNITS = (IU, MG, G, ML, COUNT, None)

PER_ADMIN = "per_administration"   # this one event
PER_DAY = "per_day"                # a daily total (regimen rows)
BASES = (PER_ADMIN, PER_DAY, None)

# uint8 overflow and its friends. 6,039 rows carry Dose 255 and the 99th
# percentile of the whole column IS 255, which is what gives it away.
DOSE_SENTINELS = (-1.0, 255.0, 999.0)

# The 13 fields every result carries, hit or miss.
VALUES = ("DoseValue", "DoseUnit", "DoseBasis")
# DrugKey is THE SEAM to describe-insulin, and it is the one identity field that
# survives a bank miss. Ingredient is the FDA's word for the drug and is null
# whenever the Directory does not list it -- which is exactly the case for
# Shanghai's 'Novolin R' and 'insulin degludec' and for all of OhioT1DM. Routing
# on Ingredient alone would send those rows nowhere, so DrugKey carries the best
# string we have: the FDA ingredient when there is one, otherwise the words the
# log itself used. describe-insulin consumes DrugKey, never Ingredient.
IDENTITY = ("DrugKey", "Ingredient", "BrandName", "PharmClass", "DosageForm",
            "Route", "NDC")
PROVENANCE = ("MedSource", "MedConf", "IsInsulin")
FIELDS = VALUES + IDENTITY + PROVENANCE
