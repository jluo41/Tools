"""
Test describe-exercise AS A SERVICE, over the wire.

`test_exnorm.py` tests the RESOLVER. This tests the thing a consumer actually
touches: a URL. They fail differently. A resolver that is perfect in process can
still hand a consumer a JSON parse error on a MISS row, drop a row from a batch
and silently shift every later activity onto the wrong record, or take longer
than the caller's timeout on one cook's worth of strings. None of that is
visible from inside Python.

    python test_server.py                     # against $EXNORM_URL
    EXNORM_URL=http://host:8078 python test_server.py
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

URL = os.environ.get("EXNORM_URL", "http://127.0.0.1:8078").rstrip("/")
PASS, FAIL = [], []


def post(path, payload, timeout=600):
    req = urllib.request.Request(URL + path, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read()
        try:
            return e.code, json.loads(body)
        except Exception:
            return e.code, {"raw": body[:200].decode("utf-8", "replace")}


def get(path):
    with urllib.request.urlopen(URL + path, timeout=30) as r:
        return r.status, json.loads(r.read())


def check(name, fn):
    try:
        note = fn()
        PASS.append(name)
        print(f"  PASS  {name}" + (f"  ({note})" if note else ""))
    except Exception as e:
        FAIL.append(name)
        print(f"  FAIL  {name}\n        {type(e).__name__}: {e}")


FIELDS = ["METValue", "ActiveMinutes", "CaloriesBurnedEst", "ActivityResolved",
          "ActivityCode", "MajorHeading", "ExerciseSource", "ExerciseConf",
          "ExerciseBasis", "TypeSource", "TypeConf"]


def t_healthz():
    s, d = get("/healthz")
    assert s == 200 and d["ok"], d
    assert d["activities"] > 1000, d
    assert d["bank"].startswith("/"), \
        f"bank path is relative ({d['bank']}) -- the service would break if " \
        "started from any other directory"
    return f"v{d['version']}, {d['activities']} activities"


def t_one():
    s, d = post("/normalize", {"activity": "Walking", "minutes": 30,
                               "weight_kg": 82})
    assert s == 200, d
    assert set(d) == set(FIELDS), set(d) ^ set(FIELDS)
    assert d["ExerciseConf"] == "ALIAS" and d["ExerciseBasis"] == "per_session"
    assert 150 < d["CaloriesBurnedEst"] < 180, d
    return f"{d['CaloriesBurnedEst']} kcal"


def t_batch_order():
    """A dropped or reordered row silently shifts every later activity onto the
    wrong record -- the failure mode with no exception attached to it."""
    acts = ["Walking", "Yoga", "Running", "Walking", "Golf"]
    s, d = post("/normalize/batch", {"activities": acts,
                                     "minutes": [10, 20, 30, 40, 50],
                                     "weight_kg": 80})
    assert s == 200 and d["count"] == len(acts), d
    r = d["results"]
    assert r[0]["ActivityCode"] == r[3]["ActivityCode"], "same activity"
    assert r[3]["CaloriesBurnedEst"] > r[0]["CaloriesBurnedEst"], "40 min > 10 min"
    assert r[2]["MajorHeading"] == "Running", r[2]
    return f"{len(acts)} in, {d['count']} out, order held"


def t_miss_is_null_not_nan():
    """A bare NaN token is not valid JSON. A MISS must cross the wire as null
    or the consumer gets a parse error instead of a missing value."""
    s, raw = post("/normalize/batch", {"activities": ["Unknown", "20903", "zzz"],
                                       "source_ids": 20})
    assert s == 200
    txt = json.dumps(raw)
    assert "NaN" not in txt and "Infinity" not in txt, txt[:200]
    for r in raw["results"]:
        assert r["METValue"] is None, r
    return "3 misses, all null"


def t_the_church_collision_over_the_wire():
    """The one defect this package exists to prevent, checked at the boundary a
    consumer actually uses -- and since the Apple code book landed, the claim is
    the stronger one: these resolve, and they resolve to Apple's activity.

        WellDoc 20050 = HK 50, traditional strength training
        PA Compendium 20050 = 'Eating at church', MET 1.5
    """
    s, d = post("/normalize/batch", {"activities": ["20050", "20037", "20020"],
                                     "source_ids": 20, "minutes": 42,
                                     "weight_kg": 80})
    assert s == 200, d
    for r in d["results"]:
        got = str(r["ActivityResolved"] or "").lower()
        assert r["METValue"] is not None, r
        assert "church" not in got and "singing" not in got, r
        assert r["ActivityCode"] not in ("20050", "20037", "20020"), r
        assert r["TypeSource"] == "session|codebook:apple", r
    return "resolve via Apple's enum, never to the church rows"


def t_codebooks_over_the_wire():
    """Four dialects, one activity, one MET -- and three different name
    provenances. The consumer sees all of it in one call."""
    s, d = post("/normalize/batch", {"activities": ["Walk", "20052", "1001", "100"],
                                     "source_ids": [None, 20, 23, 1]})
    assert s == 200, d
    assert {r["ActivityCode"] for r in d["results"]} == {"17190"}, d["results"]
    assert [r["TypeSource"] for r in d["results"]] == [
        "session|text", "session|codebook:apple",
        "session|codebook:validic", "session|codebook:welldoc_app"], d["results"]
    return "text / apple / validic / welldoc_app -> 17190"


def t_rollup_over_the_wire():
    s, d = post("/normalize/batch", {"activities": ["src20:20903", "src20:20905"],
                                     "minutes": [11, 0], "weight_kg": 80})
    for r in d["results"]:
        assert r["ExerciseSource"] == "not_resolvable:daily_rollup", r
        assert r["CaloriesBurnedEst"] is None
    return "roll-ups refuse to be dosed"


def t_basis_matrix():
    """The four cells of the basis table, over HTTP."""
    cases = [({"minutes": 30, "weight_kg": 80}, "per_session"),
             ({"minutes": 30}, "per_minute"),
             ({"weight_kg": 80}, "per_minute"),
             ({}, "per_minute")]
    for kw, want in cases:
        s, d = post("/normalize", dict(activity="Walking", **kw))
        assert d["ExerciseBasis"] == want, (kw, d["ExerciseBasis"])
    return "4/4 cells"


def t_empty_batch():
    s, d = post("/normalize/batch", {"activities": []})
    assert s == 200 and d["count"] == 0, (s, d)
    return "200, not an error"


def t_length_mismatch_is_422():
    """The caller's error, not a 500."""
    s, d = post("/normalize/batch", {"activities": ["a", "b"], "minutes": [1]})
    assert s == 422, (s, d)
    return "422 with a readable detail"


def t_malformed_never_500():
    for body in ({"nope": 1}, {"activities": "not a list"},
                 {"activities": ["a"], "minutes": "abc"}):
        s, d = post("/normalize/batch", body)
        assert 400 <= s < 500, (body, s, d)
    return "3 malformed bodies, all 4xx"


def t_real_cook():
    """One cohort's worth of DISTINCT activity strings, the way a SourceFn
    would send them."""
    acts = ["Walk", "Walking", "Bicycling", "Running", "Run", "Swimming",
            "Swim", "Hiking", "Hike", "Yoga", "Yoga_Pilates", "Treadmill",
            "Elliptical", "Tennis", "Golf", "Dancing__Aerobics",
            "Aerobic Workout", "Cardiovascular", "Strength_training",
            "StrengthTraining", "Weights", "Home_activities",
            "Gardening__Lawn", "Skiing__Skating", "Outdoor Bike", "Bike",
            "Bootcamp", "Workout", "Other", "Sports", "Sport", "Unknown"]
    t0 = time.time()
    s, d = post("/normalize/batch", {"activities": acts, "minutes": 30,
                                     "weight_kg": 80})
    dt = time.time() - t0
    assert s == 200 and d["count"] == len(acts)
    got = sum(1 for r in d["results"] if r["METValue"] is not None)
    assert got == 28, f"expected 28 of 32 to resolve, got {got}"
    return f"32 strings, {got} resolved, {dt*1000:.0f} ms"


def t_big_batch():
    """136,555 rows is what a real Exercise cook holds. The service must not
    fall over on one cohort's worth in a single call."""
    acts = (["Walking", "Yoga", "20903", "Sports"] * 5000)
    t0 = time.time()
    s, d = post("/normalize/batch", {"activities": acts, "minutes": 30,
                                     "weight_kg": 80, "source_ids": 20})
    dt = time.time() - t0
    assert s == 200 and d["count"] == len(acts), (s, d.get("count"))
    return f"{len(acts):,} rows in {dt:.1f}s"


def t_concurrent():
    """Eight callers must agree. lru_cache on the bank is shared state."""
    def one(i):
        s, d = post("/normalize", {"activity": "Walking", "minutes": 30,
                                   "weight_kg": 80})
        return d["CaloriesBurnedEst"]
    with ThreadPoolExecutor(8) as ex:
        vals = set(ex.map(one, range(16)))
    assert len(vals) == 1, vals
    return f"16 calls, one answer ({vals.pop()})"


def t_latency():
    t0 = time.time()
    for _ in range(20):
        post("/normalize", {"activity": "Walking", "minutes": 30, "weight_kg": 80})
    ms = (time.time() - t0) / 20 * 1000
    assert ms < 250, f"{ms:.0f} ms per call"
    return f"{ms:.1f} ms per call"


if __name__ == "__main__":
    print("=" * 78)
    print(f"  describe-exercise service  ->  {URL}")
    print("=" * 78)
    try:
        get("/healthz")
    except Exception as e:
        print(f"  service unreachable at {URL}: {e}")
        print("  start it: Tools/plugins/haipipe-utils/skills/describe-exercise/run_server.sh")
        sys.exit(1)
    for name, fn in [
        ("healthz reports an absolute bank path", t_healthz),
        ("single activity", t_one),
        ("batch order held, resolution deduped", t_batch_order),
        ("MISS crosses the wire as null, not NaN", t_miss_is_null_not_nan),
        ("the church collision, over the wire", t_the_church_collision_over_the_wire),
        ("code books over the wire", t_codebooks_over_the_wire),
        ("daily roll-ups refuse to be dosed", t_rollup_over_the_wire),
        ("the four basis cells", t_basis_matrix),
        ("empty batch is 200", t_empty_batch),
        ("length mismatch -> 422", t_length_mismatch_is_422),
        ("malformed body -> 4xx, never 500", t_malformed_never_500),
        ("one real cook's distinct strings", t_real_cook),
        ("20,000 rows in one call", t_big_batch),
        ("16 concurrent callers agree", t_concurrent),
        ("single-call latency", t_latency),
    ]:
        check(name, fn)
    print("=" * 78)
    print(f"  {len(PASS)} passed · {len(FAIL)} failed")
    print("=" * 78)
    sys.exit(1 if FAIL else 0)
