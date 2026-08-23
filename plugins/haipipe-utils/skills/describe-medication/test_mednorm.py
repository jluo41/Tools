"""
Regression suite for the describe-medication RESOLVER.

Every test is a defect that was real, or a rule an ordinary refactor would break
in silence. None assert that a matcher produces one particular string; they
assert the CONTRACT.

    PYTHONPATH=. python test_mednorm.py
"""
import json
import sys
import traceback

from mednorm import FIELDS, normalize
from mednorm import bank
from mednorm.aggregate import is_insulin
from mednorm.constants import (CLASS_ONLY, CODED, COUNT, DOSE_SENTINELS, G, IU,
                               MG, NAMED, PER_ADMIN, PLACEHOLDER, SENTINEL,
                               TRUSTED)
from mednorm.dialect import parse

PASS, FAIL = [], []


def check(name, fn):
    try:
        note = fn()
        PASS.append(name)
        print(f"  PASS  {name}" + (f"  ({note})" if note else ""))
    except Exception as e:
        FAIL.append(name)
        print(f"  FAIL  {name}\n        {type(e).__name__}: {e}")
        if "-v" in sys.argv:
            traceback.print_exc()


def ohio(kind):
    return json.dumps({"MedicationType": kind})


def sh(name):
    return json.dumps({"MedicationName": name})


# ------------------------------------------------------------- the banks -----

def t_banks_load():
    s = bank.stats()
    assert s["ndc"] > 100000 and s["lexicon"] > 800, s
    return f"{s['ndc']:,} NDC · {s['generic']:,} generic · {s['lexicon']} lexicon ids"


def t_ndc_segmentation():
    """Our NDCs arrive in four lengths and the segmentation is not recorded.
    Assuming one of them resolved 9.5%; trying all three resolved 26.2%."""
    assert bank.ndc_candidates("00169255013") == ["001692550"]
    assert len(bank.ndc_candidates("0002823500")) == 3, "10-digit needs 3 tries"
    assert bank.ndc_candidates("001692550") == ["001692550"], "9-digit is already the head"
    return "9 / 10 / 11 digit all handled"


def t_prefix_refuses_combinations():
    """'lisinopril' prefixes 'lisinopril and hydrochlorothiazide'. Returning
    that would put a second active ingredient into the record."""
    assert bank.by_generic_prefix("lisinopril") is None
    assert bank.by_generic_prefix("insulin") is None, "far too ambiguous"
    hit = bank.by_generic_prefix("ATORVASTATIN")
    assert hit and "torvastatin" in hit["Ingredient"], hit
    return "combination and ambiguous prefixes refused"


# ------------------------------------------------------------ the dialects ---

def t_three_dialects_type_correctly():
    assert parse("612997", 39).kind == CODED
    assert parse(None, 1.5, ohio("Basal Insulin")).kind == CLASS_ONLY
    assert parse("Non-insulin hypoglycemic agents", None,
                 sh("metformin 0.5 g")).kind == NAMED
    return "welldoc_id · ohio_type · shanghai_text"


def t_shanghai_grams_normalise():
    """'metformin 0.5 g' and 'metformin 500 mg' are one prescription. Left
    unnormalised they sort into two buckets three orders of magnitude apart."""
    it = parse("Non-insulin hypoglycemic agents", None, sh("metformin 0.5 g"))
    assert it.unit == MG and abs(it.dose - 500.0) < 1e-9, it
    return "0.5 g -> 500 mg"


def t_shanghai_multi_drug():
    """736 rows carry more than one drug in one string -- the same shape as
    describe-food's item_list."""
    it = parse("Non-insulin hypoglycemic agents", None,
               sh("liraglutide 1.2 mg, acarbose 50 mg, metformin 0.5 g"))
    assert len(it.components) == 3, it.components
    return "3 components kept"


def t_shanghai_bare_number_is_a_dose():
    """A CSII row's name is the DOSE; the drug is named by the category."""
    it = parse("CSII - basal insulin (Novolin R, IU / H)", 0.6, sh("0.6"))
    assert it.key == "Novolin R" and it.dose == 0.6 and it.unit == IU, it
    return "category names the drug, string is the dose"


def t_ohio_class_never_reaches_the_bank():
    """'Basal Insulin' is a therapeutic class. No product directory can resolve
    it, and calling that a bank miss blames the bank for the log's silence."""
    r = normalize([None], doses=[1.5], payloads=[ohio("Basal Insulin")])[0]
    assert r["Ingredient"] is None
    assert r["MedSource"].startswith("class_only:"), r["MedSource"]
    assert r["IsInsulin"] is True, "still routable to describe-insulin"
    assert r["DrugKey"] == "basal insulin", r["DrugKey"]
    return "class typed, not missed"


# --------------------------------------------------------------- sentinels ---

def t_dose_sentinels_are_typed():
    """6,039 rows carry Dose 255, and the 99th percentile of the whole column
    IS 255 -- uint8 overflow, not a dose."""
    for v in DOSE_SENTINELS:
        it = parse("612997", v)
        assert it.kind == SENTINEL, (v, it.kind)
        r = normalize(["612997"], doses=[v])[0]
        assert r["DoseValue"] is None and r["MedConf"] == "MISS", (v, r)
    return f"{DOSE_SENTINELS} all refused"


def t_sentinel_ids_are_typed():
    for i in ("1999999", "777777", "0"):
        r = normalize([i], doses=[3])[0]
        assert r["MedSource"] == "not_resolvable:sentinel", (i, r["MedSource"])
    return "777777 / 1999999 / 0"


# ------------------------------------------------------------ the dose unit --

def t_unit_comes_from_the_drug():
    """Dose arrives as a bare float and no column anywhere states its unit.
    Insulin means units; a tablet means tablets. 39 is not 39 of one thing."""
    ins = normalize(["612997"], doses=[39])[0]
    tab = normalize(["155744"], doses=[1])[0]
    assert ins["DoseUnit"] == IU, ins
    assert tab["DoseUnit"] == COUNT, tab
    return "insulin -> iu · tablet -> count"


def t_logged_unit_wins():
    """Shanghai states its unit in the string. A measurement beats an
    inference."""
    r = normalize(["Non-insulin hypoglycemic agents"], doses=[None],
                  payloads=[sh("metformin 0.5 g")])[0]
    assert r["DoseUnit"] == MG and r["DoseValue"] == 500.0, r
    return "log's own unit is used"


def t_no_unit_no_basis():
    """Rule 4. A dose whose unit cannot be named must not read as summable."""
    r = normalize(["999999999"], doses=[5])[0]
    assert r["Ingredient"] is None
    assert r["DoseUnit"] is None and r["DoseBasis"] is None, r
    return "unresolved drug -> null unit AND null basis"


def t_basis_present_when_unit_is():
    r = normalize(["612997"], doses=[39])[0]
    assert r["DoseBasis"] == PER_ADMIN, r
    return PER_ADMIN


# -------------------------------------------------------------- the seam -----

def t_drugkey_survives_a_bank_miss():
    """THE defect this field exists for. Shanghai's 'Novolin R' and all of
    OhioT1DM resolve in no product directory; routing on Ingredient would send
    them nowhere, and describe-insulin is the only skill that can serve them."""
    r = normalize(["CSII - basal insulin (Novolin R, IU / H)"], doses=[0.6],
                  payloads=[sh("0.6")])[0]
    assert r["Ingredient"] is None, "the FDA file does not list it"
    assert r["DrugKey"] == "Novolin R", r["DrugKey"]
    assert r["IsInsulin"] is True
    return "bank missed, seam held"


def t_insulin_detector_needs_word_boundaries():
    """'aspart' is a substring of 'Amphetamine ASPARTate'. Five rows of
    dextroamphetamine were typed as insulin and sent to a PK table."""
    assert is_insulin("Amphetamine Aspartate") is False
    assert is_insulin("insulin aspart") is True
    assert is_insulin("Dextroamphetamine Saccharate, Amphetamine Aspartate") is False
    return "substring is not an ingredient"


# ------------------------------------------------------- provenance ----------

def t_five_failures_five_sources():
    """Rule 5: PROVENANCE NEVER FOLDS. Each of these has a different fix."""
    got = {
        normalize([None], doses=[None])[0]["MedSource"],            # nothing named
        normalize(["612997"], doses=[255])[0]["MedSource"],         # sentinel
        normalize(["999999999"], doses=[1])[0]["MedSource"],        # not in lexicon
        normalize([None], doses=[1], payloads=[ohio("Basal Insulin")])[0]["MedSource"],
        normalize(["zzzznotadrug"], doses=[1])[0]["MedSource"],     # bank miss
    }
    assert len(got) == 5, got
    return " | ".join(sorted(s.split(":")[0] for s in got))


def t_only_trusted_writes_identity():
    for r in normalize(["612997", "999999999", None, "zzzznotadrug"],
                       doses=[39, 1, 1, 1]):
        if r["Ingredient"] is not None:
            assert r["MedConf"] in TRUSTED, r
    return "rule 3 holds"


def t_good_requires_the_code():
    """GOOD is an INVARIANT, not a fact about one id: a row is GOOD if and only
    if its NDC resolved. A name match, however exact, is OK -- two products can
    share a generic name and differ in salt, strength and route.

    Asserting a particular id's TIER instead of the invariant is what made this
    test go stale: 612997 moved from OK to GOOD when the NDC segmentation was
    fixed, which is the resolver getting better, not a regression."""
    ids = ["612997", "606257", "155744", "582255", "241223", "553838"]
    out = normalize(ids, doses=[1] * len(ids))
    for i, r in zip(ids, out):
        if r["MedConf"] == "GOOD":
            assert r["MedSource"].startswith("fda_ndc:"), (i, r["MedSource"])
        if r["MedSource"].startswith(("fda_generic", "fda_brand")):
            assert r["MedConf"] == "OK", (i, r["MedConf"])
        if r["MedSource"].startswith("fda_generic_prefix"):
            assert r["MedConf"] == "ALIAS", (i, r["MedConf"])
    good = sum(1 for r in out if r["MedConf"] == "GOOD")
    return f"{good}/{len(ids)} via NDC; tier and confidence always agree"


def t_ndc_dashes_are_the_segmentation():
    """The defect a benchmark found before the benchmark existed. Stripping the
    dashes from '13668-031-0' shifts the product code one digit and lands on a
    DIFFERENT REAL PRODUCT, at the GOOD tier: topiramate resolved to celecoxib,
    hydroxyzine to methylphenidate, duloxetine to pramipexole."""
    assert bank.ndc_candidates("13668-031-0") == ["136680031"], \
        bank.ndc_candidates("13668-031-0")
    assert bank.ndc_candidates("0054-0124-2") == ["000540124"]
    assert bank.ndc_candidates("54629-0038-") == ["546290038"], "empty package segment"
    hit = bank.by_ndc("10702-010-0")
    assert hit and "hydroxyzine" in hit["Ingredient"].lower(), hit
    return "4-4-1 / 5-3-1 / 5-4-0 all read off the dashes"


# ----------------------------------------------------------------- the door --

def t_shape_is_constant():
    for r in normalize(["612997", "zzz", None], doses=[39, 1, None]):
        assert set(r) == set(FIELDS), set(r) ^ set(FIELDS)
    return f"{len(FIELDS)} fields on hit and miss alike"


def t_order_and_dose_are_per_row():
    """Duplicates share the RESOLUTION and must never share the DOSE."""
    out = normalize(["612997", "612997"], doses=[10, 40])
    assert out[0]["Ingredient"] == out[1]["Ingredient"]
    assert out[0]["DoseValue"] == 10 and out[1]["DoseValue"] == 40, out
    return "resolution shared, dose not"


def t_length_mismatch_raises():
    for kw in ({"doses": [1]}, {"payloads": ["a", "b", "c"]}):
        try:
            normalize(["a", "b"], **kw)
        except ValueError:
            continue
        raise AssertionError(f"no raise for {kw}")
    return "doses / payloads"


def t_empty_batch():
    assert normalize([]) == []
    return "[] -> []"


def t_real_corpus_floor():
    """The measured floor over the identities that actually appear. Falling
    below this means a resolution path regressed."""
    ids = ["612997", "606257", "606209", "448625", "551714", "241223",
           "155744", "553838", "272192", "582255"]
    out = normalize(ids, doses=[10] * len(ids))
    named = sum(1 for r in out if r["Ingredient"])
    assert named == len(ids), [r["MedSource"] for r in out if not r["Ingredient"]]
    return f"{named}/{len(ids)} top ids resolve"


if __name__ == "__main__":
    print("=" * 78)
    print("  describe-medication resolver")
    print("=" * 78)
    for name, fn in [
        ("both banks load", t_banks_load),
        ("NDC segmentation tried all ways", t_ndc_segmentation),
        ("prefix tier refuses combinations", t_prefix_refuses_combinations),
        ("three dialects type correctly", t_three_dialects_type_correctly),
        ("Shanghai grams normalise to mg", t_shanghai_grams_normalise),
        ("Shanghai multi-drug keeps components", t_shanghai_multi_drug),
        ("Shanghai bare number is a dose", t_shanghai_bare_number_is_a_dose),
        ("Ohio class never reaches the bank", t_ohio_class_never_reaches_the_bank),
        ("dose sentinels are typed, not dosed", t_dose_sentinels_are_typed),
        ("sentinel ids are typed", t_sentinel_ids_are_typed),
        ("the unit comes from the drug", t_unit_comes_from_the_drug),
        ("a logged unit wins", t_logged_unit_wins),
        ("no unit -> no basis", t_no_unit_no_basis),
        ("basis present when unit is", t_basis_present_when_unit_is),
        ("DrugKey survives a bank miss", t_drugkey_survives_a_bank_miss),
        ("insulin detector uses word boundaries", t_insulin_detector_needs_word_boundaries),
        ("five failures keep five sources", t_five_failures_five_sources),
        ("only TRUSTED writes an identity", t_only_trusted_writes_identity),
        ("GOOD requires the NDC", t_good_requires_the_code),
        ("NDC dashes are the segmentation", t_ndc_dashes_are_the_segmentation),
        ("result shape is constant", t_shape_is_constant),
        ("order held, dose per row", t_order_and_dose_are_per_row),
        ("length mismatch raises", t_length_mismatch_raises),
        ("empty batch", t_empty_batch),
        ("real corpus floor", t_real_corpus_floor),
    ]:
        check(name, fn)
    print("=" * 78)
    print(f"  {len(PASS)} passed · {len(FAIL)} failed")
    print("=" * 78)
    sys.exit(1 if FAIL else 0)
