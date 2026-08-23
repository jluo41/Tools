"""How describe-medication declares itself to the shared B1 benchmark."""
import pathlib

from bench import Profile

from . import normalize
from .constants import IDENTITY, PROVENANCE, TRUSTED, VALUES

ROOT = pathlib.Path(__file__).resolve().parents[6]
INFO = ROOT / "_WorkSpace/0-RawDataStore/0-EventNorm/_MedInfo"


def _adapt(req):
    items = req.get("items", [req["item"]] if "item" in req else [])
    return normalize(items,
                     doses=req.get("doses", req.get("dose")),
                     payloads=req.get("payloads", req.get("payload")))


PROFILE = Profile(
    noun="medication", emoji="💊", skill="describe-medication",
    door=normalize,
    required=VALUES + IDENTITY + PROVENANCE,

    # DrugKey is EXCLUDED from governed, and rule 9 is the reason. It is the
    # seam to describe-insulin and it must survive a bank miss, or the 5,445
    # administrations the FDA Directory does not list route nowhere. DoseValue
    # is excluded too: the dose is the LOG's number, not the bank's, and a
    # failure to identify the drug is not a reason to forget how much was taken.
    # PharmClass is NOT here, and the reason is rule 9 again. OhioT1DM logs
    # 'Basal Insulin' -- a therapeutic class, never a product. No directory can
    # resolve it, so MedConf is honestly MISS, and the class is still known
    # because the LOG said it. MedSource carries `class_only:` rather than
    # `fda_ndc:`, so the two origins have not folded and rule 5 holds.
    #
    # What is left is what ONLY the bank can fill.
    governed=("Ingredient", "BrandName", "DosageForm", "Route", "NDC"),

    # 7 means seven units of insulin or seven tablets, and writing it without
    # saying which is the same defect as reading a per-100g composition as a
    # per-meal dose.
    scaled=("DoseValue",),

    conf_field="MedConf", source_field="MedSource",
    basis_field="DoseBasis",
    conf_order=["GOOD", "OK", "ALIAS", "WEAK", "MISS"],
    trusted=list(TRUSTED),

    port=8079, url_env="MEDNORM_URL",
    dest=INFO / "6-benchmark", examples=INFO / "5-api-examples",

    # An id through the lexicon, a generic name, a brand, a class the FDA does
    # not stock, and a placeholder.
    probe=["612997", "metformin", "LYUMJEV", "Basal Insulin", "Unknown"],
    adapt=_adapt,

    # The log said 5. Which drug it was is a separate question with a
    # separate answer, and failing it does not unsay the 5.
    echo={"doses": ("DoseValue", 5.0)},
)
