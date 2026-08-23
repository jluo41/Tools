"""
Regression suite for the describe-exercise RESOLVER.

Every test here is a defect that was real, or a rule that would be silently
broken by an ordinary-looking refactor. None of them assert that a model or a
matcher produces a particular string; they assert the CONTRACT.

    PYTHONPATH=. python test_exnorm.py
"""
import sys
import traceback

from exnorm import FIELDS, normalize
from exnorm.aggregate import kcal_from_met
from exnorm.alias_dict import ALIAS_CODE
from exnorm.constants import (DAILY_ROLLUP, MAX_BOUT_MINUTES, OPAQUE_CODE,
                              PER_MINUTE, PER_SESSION, PLACEHOLDER, SESSION,
                              TRUSTED)
from exnorm.dialect import ROLLUP_CODES, parse, reject_code_join
from exnorm.met_db import by_code, load, search

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


# ---------------------------------------------------------------- the bank ---

def t_bank_loads():
    rows = load()
    assert len(rows) > 1000, len(rows)
    heads = {r["major_heading"] for r in rows}
    assert len(heads) == 22, f"expected 22 major headings, got {len(heads)}"
    return f"{len(rows)} activities, {len(heads)} headings"


def t_every_alias_resolves():
    """A curated code that does not exist in the bank writes a silent MISS for
    the activity a person deliberately mapped. Cheapest possible guard."""
    missing = {k: c for k, (c, _) in ALIAS_CODE.items() if by_code(c) is None}
    assert not missing, missing
    return f"{len(ALIAS_CODE)} aliases"


def t_alias_mets_are_sane():
    """No curated pick may be below resting or above elite. A typo'd code that
    happens to exist would otherwise pass t_every_alias_resolves."""
    bad = {k: by_code(c)["met_value"] for k, (c, _) in ALIAS_CODE.items()
           if not 1.0 <= by_code(c)["met_value"] <= 15.0}
    assert not bad, bad
    return "all 1.0-15.0 MET"


# -------------------------------------------------- the code-space collision --

def t_cohort_codes_are_not_compendium_codes():
    """THE defect this package exists to prevent, and since 260822 the test is
    STRONGER: these three codes now resolve, and they must resolve to Apple's
    activity rather than to the compendium row that shares their digits.

        WellDoc 20050 = HK 50, traditional strength training
        PA Compendium 20050 = 'Eating at church', MET 1.5

    Before the code book landed, passing meant 'nothing was written'. Now it
    means 'the right thing was written', which is the claim that matters."""
    want = {"20050": "resistance", "20037": "jogging", "20020": "body weight"}
    for code, expect in want.items():
        assert by_code(code) is not None, f"{code} exists in the bank as a DIFFERENT activity"
        out = normalize([code], source_ids=20, minutes=42, weight_kg=80)[0]
        assert out["METValue"] is not None, (code, out)
        got = str(out["ActivityResolved"]).lower()
        assert "church" not in got and "singing" not in got, (code, got)
        assert expect in got, (code, expect, got)
        assert out["ActivityCode"] != code, "resolved to its own digits in the bank"
    return "resolve via Apple's enum, never to the church rows"


def t_reject_code_join_raises():
    for code in ("20050", "1001", "25"):
        try:
            reject_code_join(code)
        except ValueError:
            continue
        raise AssertionError(f"reject_code_join({code!r}) did not raise")
    return "guard is a raise, not a comment"


# ------------------------------------------------------------------ typing ---

def t_rollups_are_typed_not_resolved():
    """88,394 of 136,555 rows. Priced as bouts they say a patient did one
    11-minute workout a day for four years and never burned a calorie."""
    for _, code in ROLLUP_CODES:
        a = parse(code, 20)
        assert a.kind == DAILY_ROLLUP, (code, a)
        out = normalize([code], source_ids=20, minutes=11, weight_kg=80)[0]
        assert out["METValue"] is None and out["CaloriesBurnedEst"] is None
        assert out["ExerciseSource"] == f"not_resolvable:{DAILY_ROLLUP}"
    return f"{len(ROLLUP_CODES)} rollup codes"


def t_rollup_verdict_is_namespace_keyed():
    """'20903' is a roll-up because EntrySourceID 20 issued it. The same digits
    from another vendor are a different thing and must not inherit the verdict."""
    assert parse("20903", 20).kind == DAILY_ROLLUP
    assert parse("20903", 37).kind == OPAQUE_CODE
    assert parse("20903", None).kind == OPAQUE_CODE
    return "ns20 only"


def t_four_kinds_have_four_sources():
    """Rule 5: PROVENANCE NEVER FOLDS. 'not a bout', 'named nothing', 'no
    codebook here' and 'the compendium does not list it' are four different
    failures with four different fixes. Collapsing them was the food bug.

    Google_Fit stands in for the third: it is the one namespace still without a
    book, 1,210 rows."""
    got = {
        normalize(["20903"], source_ids=20)[0]["ExerciseSource"],
        normalize(["Unknown"])[0]["ExerciseSource"],
        normalize(["30007"], source_ids=37)[0]["ExerciseSource"],
        normalize(["qqqzzz"])[0]["ExerciseSource"],
    }
    assert len(got) == 4, got
    return " | ".join(sorted(got))


def t_placeholders_typed_not_dropped():
    for raw in ("Unknown", "Other", "", None, "nan"):
        a = parse(raw)
        assert a.kind == PLACEHOLDER, (raw, a)
        assert a.raw == raw, "the log's own words must survive"
    return "5 placeholder spellings"


def t_namespace_prefix_door():
    """A caller with no EntrySourceID column can still pass the namespace
    through the string, which is what keeps the door a list-of-strings."""
    assert parse("src20:20903", None).kind == DAILY_ROLLUP
    assert parse("20:20903", None).kind == DAILY_ROLLUP
    assert parse("src37:20903", None).kind == OPAQUE_CODE
    return "src20: prefix == source_ids=20"


# -------------------------------------------------------------- the ladder ---

def t_fuzzy_never_writes_a_value():
    """'Sports' -- 714 rows -- head-anchors at score 1.0 onto 'Sports
    spectator, very excited', MET 3.3. A patient who logged Sports was not
    watching one. WEAK must carry the candidate and withhold the number."""
    out = normalize(["Sports"], minutes=30, weight_kg=80)[0]
    assert out["ExerciseConf"] == "WEAK", out
    assert out["METValue"] is None and out["CaloriesBurnedEst"] is None
    assert out["ActivityResolved"], "the candidate must ride along for curation"
    return f"suggests {out['ActivityCode']}, writes nothing"


def t_only_trusted_writes():
    """Rule 3, mechanically: no row outside TRUSTED may carry a MET."""
    probes = ["Walking", "Sports", "Unknown", "20903", "qqqzzz", "Yoga", "Golf"]
    for r in normalize(probes, source_ids=20, minutes=30, weight_kg=80):
        if r["METValue"] is not None:
            assert r["ExerciseConf"] in TRUSTED, r
        else:
            assert r["ExerciseConf"] not in TRUSTED or r["ExerciseConf"] == "MISS", r
    return f"{len(probes)} probes"


def t_no_heading_only_match():
    """A category word is not evidence for a member of the category. Merged
    heading+description tokens scored 'sports' at 1.0 against 'Judo'."""
    for hit in search("judo", 5):
        assert "judo" in hit["activity_description"].lower() or hit["__score"] < 1.0, hit
    assert search("religious") == [] or all(
        "religio" in h["activity_description"].lower() for h in search("religious")), \
        "matched a heading with no description support"
    return "description tokens only"


def t_good_is_unreachable():
    """The bank is a third-party mirror, not the publisher. Nothing it produces
    may be stamped GOOD until someone replaces the file."""
    probes = ["Walking", "Running", "Yoga", "Golf", "Tennis", "Bicycling",
              "Swimming", "Sports", "Hiking", "Dancing"]
    confs = {r["ExerciseConf"] for r in normalize(probes)}
    assert "GOOD" not in confs, confs
    return f"observed {sorted(confs)}"


# --------------------------------------------------------------- the basis ---

def t_basis_needs_both():
    """Rule 4. MET is a RATE; kcal is a DOSE. Both minutes and mass, or no
    dose -- and the basis column says which."""
    both = normalize(["Walking"], minutes=30, weight_kg=80)[0]
    assert both["ExerciseBasis"] == PER_SESSION and both["CaloriesBurnedEst"]
    for kw in ({"minutes": 30}, {"weight_kg": 80}, {}):
        r = normalize(["Walking"], **kw)[0]
        assert r["ExerciseBasis"] == PER_MINUTE, (kw, r)
        assert r["CaloriesBurnedEst"] is None, (kw, r)
        assert r["METValue"] == 3.8, "the RATE is still reportable"
    return "per_session only with both"


def t_no_default_body_mass():
    """A default weight is a fabricated number wearing a plausible value."""
    r = normalize(["Walking"], minutes=30)[0]
    assert r["CaloriesBurnedEst"] is None
    for bad in (0, None, ""):
        assert normalize(["Walking"], minutes=30, weight_kg=bad)[0][
            "CaloriesBurnedEst"] is None, bad
    return "0 / None / '' all refuse"


def t_kcal_arithmetic():
    """MET x 3.5 x kg / 200 x min. 3.8 MET, 80 kg, 30 min = 159.6 kcal."""
    assert abs(kcal_from_met(3.8, 30, 80) - 159.6) < 0.05, kcal_from_met(3.8, 30, 80)
    assert abs(kcal_from_met(1.0, 60, 70) - 73.5) < 0.05
    return "159.6 kcal for a 30-min walk at 80 kg"


def t_zero_minutes_is_not_a_session():
    """57,419 rows carry ExerciseDuration 0. Zero minutes is not a bout of
    zero length; it is a duration that was never stated."""
    r = normalize(["Walking"], minutes=0, weight_kg=80)[0]
    assert r["ActiveMinutes"] is None and r["CaloriesBurnedEst"] is None
    assert r["ExerciseBasis"] == PER_MINUTE
    return "duration 0 -> per_minute"


# ----------------------------------------------------------------- the door --

def t_shape_is_constant():
    """A caller never branches on shape, only on ExerciseConf."""
    for r in normalize(["Walking", "Unknown", "20903", "zzz"], source_ids=20):
        assert set(r) == set(FIELDS), set(r) ^ set(FIELDS)
    return f"{len(FIELDS)} fields on hit and miss alike"


def t_order_and_dedupe():
    acts = ["Walking", "Yoga", "Walking", "Running", "Yoga"]
    out = normalize(acts, minutes=[10, 20, 30, 40, 50], weight_kg=80)
    assert len(out) == len(acts)
    assert out[0]["ActivityCode"] == out[2]["ActivityCode"], "same activity"
    assert out[0]["CaloriesBurnedEst"] < out[2]["CaloriesBurnedEst"], \
        "dedupe must share the RESOLUTION, never the scaling"
    return "resolution shared, scaling per row"


def t_length_mismatch_raises():
    """A silent zip truncation re-pairs every row after the missing one."""
    for kw in ({"minutes": [1]}, {"weight_kg": [1, 2, 3]}, {"source_ids": []}):
        try:
            normalize(["a", "b"], **kw)
        except ValueError:
            continue
        raise AssertionError(f"no raise for {kw}")
    return "minutes / weight_kg / source_ids"


def t_scalar_spreads():
    out = normalize(["Walking", "Yoga"], minutes=30, weight_kg=80)
    assert all(r["ActiveMinutes"] == 30 for r in out)
    return "a scalar applies to the whole batch"


def t_empty_batch():
    assert normalize([]) == []
    return "[] -> []"


def t_nan_is_not_a_quantity():
    r = normalize(["Walking"], minutes=float("nan"), weight_kg=80)[0]
    assert r["ActiveMinutes"] is None and r["ExerciseBasis"] == PER_MINUTE
    return "NaN minutes -> per_minute"


# ------------------------------------------------------------- the corpus ----

def t_real_text_coverage():
    """The measured floor. All 32 free-text values that appear in
    1-SourceStore; 28 of them name an activity and must resolve. The four that
    do not name one must NOT."""
    named = ["Walk", "Walking", "Bicycling", "Running", "Run", "Swimming",
             "Swim", "Hiking", "Hike", "Yoga", "Yoga_Pilates", "Treadmill",
             "Elliptical", "Tennis", "Golf", "Dancing__Aerobics",
             "Aerobic Workout", "Cardiovascular", "Strength_training",
             "StrengthTraining", "Weights", "Home_activities",
             "Gardening__Lawn", "Skiing__Skating", "Outdoor Bike", "Bike",
             "Bootcamp", "Workout"]
    unnamed = ["Other", "Sports", "Sport", "Unknown"]
    miss = [a for a, r in zip(named, normalize(named)) if r["METValue"] is None]
    assert not miss, f"named activities that failed to resolve: {miss}"
    wrote = [a for a, r in zip(unnamed, normalize(unnamed))
             if r["METValue"] is not None]
    assert not wrote, f"unnamed strings that invented a MET: {wrote}"
    return f"{len(named)}/{len(named)} named resolve, 0/{len(unnamed)} unnamed do"


# ------------------------------------------------------------- code books ----

def t_apple_prefix_is_the_source_id():
    """The structural evidence the Apple mapping rests on: strip '20' from a
    ns20 code and the remainder is a valid HKWorkoutActivityType, for every
    code in 1-SourceStore except one contiguous private band. A wrong
    hypothesis does not miss in one clean block."""
    from exnorm import codebooks as cb
    seen = ["20052", "20013", "20037", "20050", "20020", "20063", "20016",
            "20059", "20033", "20073", "20014", "20029", "20044", "20011",
            "20035", "20057"]
    for c in seen:
        assert int(c) - cb.APPLE_PREFIX in cb.APPLE_HK, c
    for c in sorted(cb.APPLE_ROLLUP) + [cb.APPLE_UNMAPPED]:
        assert int(c) - cb.APPLE_PREFIX not in cb.APPLE_HK, c
    return f"{len(seen)} workout codes in, {len(cb.APPLE_ROLLUP)+1} private codes out"


def t_four_dialects_one_activity():
    """A patient typing 'Walk', Apple's 52, Validic's 1001 and the WellDoc app's
    100 are four dialects for one activity. They must reach the SAME compendium
    entry through ONE curated pick -- otherwise the same walk gets four METs.

    IDENTITY is what must agree, and the assertion is on ActivityCode and
    METReference. METValue is deliberately allowed to differ: once the scale
    tier exists, Apple and FitBit disagree by 68% about the energy of the same
    named walk, and reporting one number for both would be hiding a measured
    disagreement rather than resolving it. The entry is one; whose MET it is
    reported as is a second axis, and METScale names it."""
    got = normalize(["Walk", "20052", "1001", "100"], source_ids=[None, 20, 23, 1])
    assert {r["ActivityCode"] for r in got} == {"17190"}
    assert {r["METReference"] for r in got} == {3.8}, \
        "one entry must mean one published MET"
    for r in got:
        assert r["METValue"] == round(r["METReference"] * r["METScaleFactor"], 2) \
            or r["METValue"] == r["METReference"], r
    return "text / apple / validic / welldoc_app -> 17190, one reference MET"


def t_name_provenance_survives():
    """Rule 5 again. The four dialects agree on the MET and must NOT agree on
    where the name came from: a name a patient typed and a name read off a
    vendor enum are different evidence."""
    got = normalize(["Walk", "20052", "1001"], source_ids=[None, 20, 23])
    src = [r["TypeSource"] for r in got]
    assert src == ["session|text", "session|codebook:apple",
                   "session|codebook:validic"], src
    assert [r["TypeConf"] for r in got] == ["LOGGED", "CODEBOOK", "CODEBOOK"]
    return " · ".join(src)


def t_a_code_is_read_only_in_its_own_book():
    """Both WellDoc books define 1-5 identically and diverge above; Apple's 52
    is walking while Validic's 52 is nothing. A code looked up in a neighbour's
    book is the church-supper defect wearing a different hat."""
    assert normalize(["1001"], source_ids=23)[0]["METValue"] is not None
    assert normalize(["1001"], source_ids=20)[0]["METValue"] is None, \
        "Validic's 1001 must not resolve through Apple's book"
    assert normalize(["52"], source_ids=20)[0]["METValue"] is None, \
        "Apple codes carry the 20 prefix; a bare 52 is not one"
    return "no cross-book reads"


def t_decoded_and_still_nameless():
    """Validic 25 decodes perfectly -- to 'Other'. Decoding is not naming, so it
    is a placeholder, and its TypeConf still records that a book was consulted.
    3,308 rows."""
    r = normalize(["25"], source_ids=23, minutes=30, weight_kg=80)[0]
    assert r["METValue"] is None and r["TypeSource"] == "placeholder|codebook:validic"
    assert r["TypeConf"] == "CODEBOOK"
    return "decoded, and still names nothing"


def t_20999_is_a_placeholder_not_a_missing_book():
    """1,074 rows shaped like real bouts -- 695 distinct times of day, median 33
    minutes -- but Apple's enum has no case for them. No dictionary will ever
    decode it, so it is 'nothing was named', NOT 'the book is missing'. Those
    have different fixes and must not share a value."""
    r = normalize(["20999"], source_ids=20, minutes=33, weight_kg=80)[0]
    assert r["ExerciseSource"] == f"not_resolvable:{PLACEHOLDER}", r
    assert r["ExerciseSource"] != f"not_resolvable:{OPAQUE_CODE}"
    return "unmapped-type bucket is a placeholder"


def t_whole_rollup_band():
    """20901..20906, not just the three that happened to be common. All six
    show ~1.04 rows per patient per day and CaloriesBurned zero in 100% of
    88,467 rows."""
    from exnorm import codebooks as cb
    assert len(cb.APPLE_ROLLUP) == 6, sorted(cb.APPLE_ROLLUP)
    for c in cb.APPLE_ROLLUP:
        r = normalize([c], source_ids=20, minutes=11, weight_kg=80)[0]
        assert r["ExerciseSource"] == f"not_resolvable:{DAILY_ROLLUP}", (c, r)
    return "6 codes, none dosable"


def t_double_underscore_folds():
    """A regression that cost 264 rows: 'Dancing__Aerobics' folded to
    'dancing aerobics' and no un-folding reproduced the literal key. Both sides
    of the lookup are folded by one function now."""
    from exnorm.dialect import canonical
    from exnorm.alias_dict import ALIAS_CODE
    for t in ("Dancing__Aerobics", "Gardening__Lawn", "Skiing__Skating",
              "Yoga_Pilates", "Strength_training", "Outdoor Bike"):
        assert canonical(t) in ALIAS_CODE, (t, canonical(t))
    return "6 separator dialects"


def t_curated_picks_beat_the_fuzzy_tier():
    """Each of these was curated BECAUSE the fuzzy tier's top hit was actively
    wrong. If a refactor ever routes them through search() again, this fails."""
    wrong = {"cycling": "aquatic", "mind and body": "body weight resistance",
             "preparation and recovery": "cooking", 
             "traditional strength training": "pilates"}
    for name, must_not in wrong.items():
        r = normalize([name])[0]
        assert r["ExerciseConf"] == "ALIAS", (name, r["ExerciseConf"])
        assert must_not not in str(r["ActivityResolved"]).lower(), (name, r["ActivityResolved"])
    return f"{len(wrong)} traps held"


def t_implausible_bout_loses_its_dose_not_its_met():
    """Found only by running all 136,555 real rows. A log claiming a
    4,680-minute walk produced 18,829 kcal, and that absurd number was OURS.
    The MET survives -- walking is walking however long you claim -- and the
    log's own duration is still reported. Only the dose is refused, and the
    reason is written down rather than left as a silent NULL."""
    ok = normalize(["Walking"], minutes=240, weight_kg=110)[0]
    assert ok["CaloriesBurnedEst"] and ok["ExerciseBasis"] == PER_SESSION

    bad = normalize(["Walking"], minutes=4680, weight_kg=110)[0]
    assert bad["METValue"] == 3.8, "the RATE is unaffected"
    assert bad["ActiveMinutes"] == 4680.0, "the log's claim is still reported"
    assert bad["CaloriesBurnedEst"] is None
    assert bad["ExerciseBasis"] == PER_MINUTE
    assert "bout>" in bad["ExerciseSource"], bad["ExerciseSource"]
    return "MET kept, minutes kept, dose refused, reason recorded"


def t_the_bound_is_on_duration_not_on_the_product():
    """What the bound actually guarantees, stated honestly.

    An earlier version of this test asserted no estimate could exceed 6,000
    kcal. That was a claim the design does not make: a 200 kg adult jogging the
    full 240 minutes really is ~6,300 kcal, which is a big number for an
    unusual person, not an absurd one. The bound refuses IMPLAUSIBLE DURATIONS;
    it does not cap the product, and pretending otherwise would mean silently
    discarding a real bout by a heavy patient.

    What IS true, and is the useful claim: across all 136,555 real rows the
    largest surviving estimate is 3,726 kcal, inside an adult's whole-day total
    energy expenditure. That is a property of this corpus, verified by
    scratchpad/realrun, not a guarantee of the arithmetic."""
    ceiling = normalize(["Running"], minutes=MAX_BOUT_MINUTES, weight_kg=90)[0]
    assert ceiling["CaloriesBurnedEst"] < 4000, ceiling
    over = normalize(["Running"], minutes=MAX_BOUT_MINUTES + 1, weight_kg=90)[0]
    assert over["CaloriesBurnedEst"] is None
    return (f"a 90 kg adult at the {MAX_BOUT_MINUTES:g}-min bound is "
            f"{ceiling['CaloriesBurnedEst']:.0f} kcal; one minute more is refused")


if __name__ == "__main__":
    print("=" * 78)
    print("  describe-exercise resolver")
    print("=" * 78)
    for name, fn in [
        ("bank loads, 22 major headings", t_bank_loads),
        ("every curated alias exists in the bank", t_every_alias_resolves),
        ("every curated MET is physiologically sane", t_alias_mets_are_sane),
        ("cohort codes never join to compendium codes", t_cohort_codes_are_not_compendium_codes),
        ("reject_code_join is a raise", t_reject_code_join_raises),
        ("daily roll-ups typed, never resolved", t_rollups_are_typed_not_resolved),
        ("roll-up verdict is namespace-keyed", t_rollup_verdict_is_namespace_keyed),
        ("four kinds keep four distinct sources", t_four_kinds_have_four_sources),
        ("placeholders typed, not dropped", t_placeholders_typed_not_dropped),
        ("src20: prefix carries the namespace", t_namespace_prefix_door),
        ("fuzzy tier never writes a value", t_fuzzy_never_writes_a_value),
        ("only TRUSTED writes a MET", t_only_trusted_writes),
        ("no heading-only match", t_no_heading_only_match),
        ("GOOD is unreachable on a mirror bank", t_good_is_unreachable),
        ("per_session needs minutes AND mass", t_basis_needs_both),
        ("no default body mass", t_no_default_body_mass),
        ("kcal arithmetic", t_kcal_arithmetic),
        ("duration 0 is not a bout", t_zero_minutes_is_not_a_session),
        ("result shape is constant", t_shape_is_constant),
        ("order preserved, resolution deduped", t_order_and_dedupe),
        ("length mismatch raises", t_length_mismatch_raises),
        ("scalar spreads over the batch", t_scalar_spreads),
        ("empty batch", t_empty_batch),
        ("NaN is not a quantity", t_nan_is_not_a_quantity),
        ("all 32 real free-text values", t_real_text_coverage),
        ("apple prefix is the EntrySourceID", t_apple_prefix_is_the_source_id),
        ("four dialects, one activity, one MET", t_four_dialects_one_activity),
        ("name provenance survives the fold", t_name_provenance_survives),
        ("a code is read only in its own book", t_a_code_is_read_only_in_its_own_book),
        ("decoded and still nameless", t_decoded_and_still_nameless),
        ("20999 is a placeholder, not a missing book", t_20999_is_a_placeholder_not_a_missing_book),
        ("the whole 209xx rollup band", t_whole_rollup_band),
        ("double-underscore dialects fold", t_double_underscore_folds),
        ("curated picks beat the fuzzy tier", t_curated_picks_beat_the_fuzzy_tier),
        ("implausible bout loses its dose, not its MET", t_implausible_bout_loses_its_dose_not_its_met),
        ("the bound is on duration, not the product", t_the_bound_is_on_duration_not_on_the_product),
    ]:
        check(name, fn)
    print("=" * 78)
    print(f"  {len(PASS)} passed · {len(FAIL)} failed")
    print("=" * 78)
    sys.exit(1 if FAIL else 0)
