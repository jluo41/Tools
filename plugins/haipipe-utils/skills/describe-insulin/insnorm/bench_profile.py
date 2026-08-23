"""How describe-insulin declares itself to the shared B1 benchmark.

IT REPORTS INTO ITS OWN `_InsInfo`, AND THE EARLIER REASONING WAS BACKWARDS.
This file used to say the two halves share `_MedInfo` because "splitting the
evidence would hide the rows only the second half can reach". The opposite was
true: with no folder of its own, insulin had no `1-per-cohort` page, and
`_MedInfo/_stats.json` carried `noun='medication'` on all 11 rows and insulin on
none. The 5,445 rows that resolve here and nowhere in describe-medication were
visible in a paragraph of SKILL.md and in no artifact at all.

A folder makes them countable. What a split really costs is the SEAM -- nobody
measures a handoff that spans two folders by accident -- so `_InsInfo/README.md`
carries the seam table, and it is that table, not shared housing, that holds the
chain together.
"""
import pathlib

from bench import Profile

from . import normalize
from .client import FIELDS, TRUSTED

ROOT = pathlib.Path(__file__).resolve().parents[6]
INFO = ROOT / "_WorkSpace/0-RawDataStore/0-EventNorm/_InsInfo"


def _adapt(req):
    items = req.get("items", [req["item"]] if "item" in req else [])
    return normalize(items, dia_hours=req.get("dia_hours", req.get("dia_hours")))


PROFILE = Profile(
    noun="insulin", emoji="💉", skill="describe-insulin",
    door=normalize,
    required=FIELDS,
    # `InsulinResolved` IS NOT GOVERNED, AND THAT CHANGED ON 260822.
    # Rule 3 nulls a value the confidence does not support. InsulinResolved is
    # not a value, it is the IDENTITY -- and there is now one path where the
    # identity SUCCEEDS while the numbers are unavailable: an intravenous row,
    # whose drug we know and whose subcutaneous curve does not apply. Rule 5
    # says those are two facts, so the identity survives a PK miss.
    governed=("InsulinClass", "OnsetMin", "PeakMin", "DurationMin", "Biphasic"),

    # NOT EMPTY ANY MORE, AND THE OLD CLAIM WAS WRONG.
    # This read `scaled=()` with the argument that onset, peak and duration are
    # properties of the drug that do not scale with dose, so rule 4 had nothing
    # to govern. Shanghai's 29 intravenous rows falsify it: with no
    # subcutaneous depot there is no absorption phase, and a 270-minute
    # duration is wrong by an order of magnitude. A time is not interpretable
    # without the route it was measured on, which is exactly rule 4, and
    # `PKBasis` is the column it demands. PeakMin stays out because its null is
    # meaningful on its own -- peakless -- and rule 4 governs written values.
    scaled=("OnsetMin", "DurationMin"),

    conf_field="PKConf", source_field="PKSource", basis_field="PKBasis",
    conf_order=["GOOD", "OK", "ALIAS", "MISS"],
    trusted=list(TRUSTED),

    port=8080, url_env="INSNORM_URL",
    dest=INFO / "6-benchmark", examples=INFO / "5-api-examples",

    # A rapid analogue, a peakless basal, a premix, a therapeutic class, and a
    # drug that is not insulin at all.
    probe=["Insulin lispro-aabc", "Insulin glargine", "insulin aspart 70/30",
           "basal insulin", "metformin"],

    # RULE 9 / C13: a route the caller stated is a fact whether or not the bank
    # knew the drug. Checked with a string the table cannot resolve.
    echo={"delivery": ("DeliveryMode", "pump_basal")},
    adapt=_adapt,
)
