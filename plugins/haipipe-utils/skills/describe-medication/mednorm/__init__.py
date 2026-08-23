"""
describe-medication: a logged medication, in a cohort's own dialect, becomes an
FDA-identified drug with a dose that states its own unit.

    from mednorm import normalize
    normalize(["612997"], doses=[39])
    # [{'DoseValue': 39.0, 'DoseUnit': 'iu', 'DoseBasis': 'per_administration',
    #   'Ingredient': 'Insulin lispro-aabc', ..., 'MedConf': 'OK',
    #   'IsInsulin': True}]

`normalize` is the whole public surface.

WHAT THIS DOES NOT DO: pharmacokinetics. An insulin row leaves here with
IsInsulin True and an ingredient name, and describe-insulin turns that into
onset / peak / duration. The seam between the two skills is the INGREDIENT
NAME -- the same trick describe-food uses, where a photo becomes a food name and
rejoins the ordinary path.
"""
from .client import DEFAULT_TRANSPORT, DEFAULT_URL, TRANSPORTS, normalize
from .constants import (BASES, FIELDS, IDENTITY, PROVENANCE, TRUSTED, TYPES,
                        UNITS, VALUES)

__all__ = ["normalize", "FIELDS", "VALUES", "IDENTITY", "PROVENANCE",
           "TYPES", "UNITS", "BASES", "TRUSTED", "TRANSPORTS",
           "DEFAULT_TRANSPORT", "DEFAULT_URL"]
__version__ = "0.1.0"
