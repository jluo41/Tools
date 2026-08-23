"""
Regression suite for the describe-insulin RESOLVER.

    PYTHONPATH=. python test_insnorm.py
"""
import sys
import traceback

from insnorm import FIELDS, canon, normalize
from insnorm.pk_table import ALIASES, CLASSES, COMBINATIONS, PK

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


def t_table_is_consistent():
    bad_alias = [a for a, k in ALIASES.items() if k not in PK]
    bad_combo = [c for c, (k, _) in COMBINATIONS.items() if k not in PK]
    assert not bad_alias and not bad_combo, (bad_alias, bad_combo)
    bad_class = [k for k, v in PK.items() if v[0] not in CLASSES]
    assert not bad_class, bad_class
    return f"{len(PK)} products, {len(ALIASES)} aliases"


def t_pk_values_are_physiological():
    """A typo in this hand-written table is the failure mode with no symptom,
    so the shape of every row is checked rather than trusted."""
    for k, (cls, onset, peak, dur, biph, note) in PK.items():
        assert 0 < onset <= 240, (k, onset)
        assert 60 <= dur <= 3000, (k, dur)
        assert onset < dur, (k, onset, dur)
        if peak is not None:
            assert onset < peak < dur, (k, onset, peak, dur)
        assert note, f"{k} has no citation note"
    return f"{len(PK)} rows, onset < peak < duration"


def t_peakless_is_null_not_a_number():
    """Glargine and degludec have no pronounced peak. Writing a number there
    invents a shape the drug does not have."""
    for name in ("insulin glargine", "insulin degludec"):
        r = normalize([name])[0]
        assert r["PeakMin"] is None, (name, r["PeakMin"])
        assert r["DurationMin"] and r["OnsetMin"], r
    peaked = normalize(["insulin lispro"])[0]
    assert peaked["PeakMin"] is not None
    return "peakless drugs carry NULL, not 0"


def t_longest_alias_wins():
    """'insulin lispro' is a substring of 'insulin lispro-aabc'. Matching the
    shorter one would price an ultra-rapid analogue as an ordinary one."""
    a = normalize(["Insulin lispro-aabc"])[0]
    b = normalize(["Insulin lispro"])[0]
    assert a["InsulinResolved"] == "insulin lispro-aabc", a
    assert b["InsulinResolved"] == "insulin lispro", b
    assert a["OnsetMin"] != b["OnsetMin"], "the two must not collapse"
    return "aabc kept distinct from plain lispro"


def t_device_words_are_stripped():
    """The logs carry pens, cartridges and concentrations. None is a molecule."""
    for s in ("Humalog KwikPen 100 unit/mL",
              "insulin lispro (HUMALOG TEMPO PEN,U-100,INSULN) 100 unit/mL",
              "LYUMJEV TEMPO PEN"):
        r = normalize([s])[0]
        assert r["InsulinClass"] == "rapid", (s, r)
    return "pen / U-100 / INSULN ignored"


def t_class_only_inputs_resolve():
    """OhioT1DM logs a CLASS and 5,026 rows depend on this working."""
    for s, cls in (("basal insulin", "long"), ("bolus insulin", "rapid")):
        r = normalize([s])[0]
        assert r["InsulinClass"] == cls, (s, r)
        assert "class only" in PK[r["InsulinResolved"]][5], "must say it is a class"
    return "basal -> long · bolus -> rapid"


def t_combination_is_alias_not_ok():
    """Xultophy is degludec AND a GLP-1 agonist. Its insulin component is real;
    calling the row plain degludec at OK would hide the second drug."""
    r = normalize(["insulin degludec and liraglutide"])[0]
    assert r["PKConf"] == "ALIAS" and r["InsulinResolved"] == "insulin degludec", r
    assert "combination" in r["PKSource"], r["PKSource"]
    return "flagged, not silently simplified"


def t_premix_is_flagged_biphasic():
    """One (onset, peak, duration) triple describes a 70/30 mix badly; the flag
    is how a consumer knows it is approximating."""
    r = normalize(["insulin aspart 70/30"])[0]
    assert r["Biphasic"] is True and r["InsulinClass"] == "premix", r
    assert normalize(["insulin lispro"])[0]["Biphasic"] is False
    return "premix carries the envelope + a warning"


def t_non_insulin_is_a_clean_miss():
    for s in ("metformin", "LISINOPRIL", "", None, "temporarily suspend insulin delivery"):
        r = normalize([s])[0]
        assert r["InsulinClass"] is None and r["PKConf"] == "MISS", (s, r)
    return "5 non-insulins refused"


def t_patient_dia_beats_the_table():
    """WellDoc measures DIA per patient for 15.7% of prescriptions. That is the
    only evidence in this whole skill that is about the actual person."""
    base = normalize(["basal insulin"])[0]
    over = normalize(["basal insulin"], dia_hours=[7.0])[0]
    assert over["DurationMin"] == 420.0 and over["PKConf"] == "GOOD", over
    assert over["OnsetMin"] == base["OnsetMin"], \
        "only DURATION is measured; onset stays the table's and must say so"
    assert "label_table" in over["PKSource"], "the table part must remain visible"
    return "GOOD only with a measured DIA"


def t_bad_dia_is_ignored_not_fatal():
    for bad in (0, -1, None, "abc", ""):
        r = normalize(["insulin lispro"], dia_hours=[bad])[0]
        assert r["PKConf"] == "OK" and r["DurationMin"] == PK["insulin lispro"][3], bad
    return "0 / -1 / None / 'abc' all fall back to the table"


def t_shape_and_order():
    out = normalize(["insulin lispro", "metformin", "insulin glargine"])
    for r in out:
        assert set(r) == set(FIELDS), set(r) ^ set(FIELDS)
    assert out[0]["InsulinClass"] == "rapid" and out[2]["InsulinClass"] == "long"
    return f"{len(FIELDS)} fields, order held"


def t_length_mismatch_raises():
    try:
        normalize(["a", "b"], dia_hours=[1])
    except ValueError:
        return "dia_hours"
    raise AssertionError("no raise")


def t_canon_is_stable():
    assert canon("Insulin Lispro-aabc") == canon("insulin lispro-aabc")
    assert canon("  NOVOLIN R  ") == "novolin r"
    return "case and whitespace folded"


def t_real_corpus_keys():
    """Every drug key that describe-medication actually emits for an insulin
    row, measured over all 247,207 of them. The one deliberate miss is a pump
    EVENT, not a drug."""
    keys = ["Insulin lispro-aabc", "Insulin lispro", "Insulin glargine",
            "bolus insulin", "insulin aspart", "Novolin R", "insulin degludec",
            "basal insulin", "insulin degludec and liraglutide",
            "insulin aspart 70/30", "insulin detemir", "Human Insulin",
            "Novolin 30R", "Insulin human", "Humulin 70/30", "insulin glulisine",
            "Novolin 50R", "insulin glarigine"]
    out = normalize(keys)
    miss = [k for k, r in zip(keys, out) if r["InsulinClass"] is None]
    assert not miss, miss
    return f"{len(keys)}/{len(keys)} real keys resolve"


if __name__ == "__main__":
    print("=" * 78)
    print("  describe-insulin resolver")
    print("=" * 78)
    for name, fn in [
        ("PK table is internally consistent", t_table_is_consistent),
        ("every PK row is physiological", t_pk_values_are_physiological),
        ("peakless drugs carry NULL", t_peakless_is_null_not_a_number),
        ("the longest alias wins", t_longest_alias_wins),
        ("device and strength words stripped", t_device_words_are_stripped),
        ("class-only inputs resolve", t_class_only_inputs_resolve),
        ("a combination is ALIAS, not OK", t_combination_is_alias_not_ok),
        ("a premix is flagged biphasic", t_premix_is_flagged_biphasic),
        ("a non-insulin is a clean miss", t_non_insulin_is_a_clean_miss),
        ("a measured DIA beats the table", t_patient_dia_beats_the_table),
        ("a bad DIA is ignored, not fatal", t_bad_dia_is_ignored_not_fatal),
        ("shape and order", t_shape_and_order),
        ("length mismatch raises", t_length_mismatch_raises),
        ("canon is stable", t_canon_is_stable),
        ("every real corpus key resolves", t_real_corpus_keys),
    ]:
        check(name, fn)
    print("=" * 78)
    print(f"  {len(PASS)} passed · {len(FAIL)} failed")
    print("=" * 78)
    sys.exit(1 if FAIL else 0)
