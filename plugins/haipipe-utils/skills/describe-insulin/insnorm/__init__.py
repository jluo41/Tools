"""
describe-insulin: an insulin product name becomes pharmacokinetic parameters.

    from insnorm import normalize
    normalize(["Insulin lispro-aabc"])
    # [{'InsulinClass': 'rapid', 'OnsetMin': 10, 'PeakMin': 57,
    #   'DurationMin': 300, 'Biphasic': False,
    #   'InsulinResolved': 'insulin lispro-aabc',
    #   'PKSource': 'label_table:insulin lispro-aabc', 'PKConf': 'OK'}]

Second half of a CHAIN. describe-medication resolves a logged row to a DrugKey;
this skill consumes that string. They are not siblings a caller chooses between:
nothing can tell whether MedicationID 612997 is insulin until it has been
resolved, so the order is fixed.

They are also not nested, which is why this is its own skill: 5,445 rows -- all
5,026 of OhioT1DM's and 419 of Shanghai's -- resolve HERE and nowhere in
describe-medication, because they name a class or a product the FDA Directory
does not list. Counted per cohort in `_InsInfo/README.md`.
"""
from .client import (DEFAULT_TRANSPORT, DEFAULT_URL, FIELDS, TRANSPORTS,
                     TRUSTED, canon, normalize)
from .pk_table import CLASSES

__all__ = ["normalize", "FIELDS", "CLASSES", "TRUSTED", "TRANSPORTS", "canon",
           "DEFAULT_TRANSPORT", "DEFAULT_URL"]
__version__ = "0.1.0"
