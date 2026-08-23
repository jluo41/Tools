"""
Test describe-food AS A SERVICE, over the wire.

`test_foodnorm.py` tests the RESOLVER. This tests the thing a consumer actually
touches: a URL. They fail differently -- a resolver that is perfect in process
can still hand a consumer a JSON parse error on a MISS row, drop a row from a
batch and silently shift every later meal onto the wrong record, or take so long
on one cook's worth of strings that the caller times out. None of those is
visible from inside Python.

    python test_server.py                  # against $FOODNORM_URL
    FOODNORM_URL=http://host:8077 python test_server.py
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

URL = os.environ.get("FOODNORM_URL", "http://127.0.0.1:8077").rstrip("/")
PASS, FAIL = [], []


def post(path, payload, timeout=600):
    req = urllib.request.Request(URL + path, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, json.loads(r.read())


def get(path, timeout=30):
    with urllib.request.urlopen(URL + path, timeout=timeout) as r:
        return r.status, json.loads(r.read())


def check(name, fn):
    t0 = time.perf_counter()
    try:
        detail = fn() or ""
        ms = (time.perf_counter() - t0) * 1000
        PASS.append(name); print(f"  ✅ {name:<44s} {ms:7.0f} ms  {detail}")
    except Exception as e:
        ms = (time.perf_counter() - t0) * 1000
        FAIL.append((name, e)); print(f"  ❌ {name:<44s} {ms:7.0f} ms  {type(e).__name__}: {e}")


# ── 1 · the service is there and says what it is serving ────────────────────
def t_health():
    s, d = get("/healthz")
    assert s == 200, s
    assert d["status"] == "ok", d
    assert d["bank_exists"] is True, d
    assert isinstance(d["bank_rows"], int) and d["bank_rows"] > 1000, d
    return f"bank_rows={d['bank_rows']:,}"


# ── 2 · one string ──────────────────────────────────────────────────────────
def t_single():
    s, d = post("/normalize", {"food": "fried rice"})
    assert s == 200
    for k in ("Carbs", "Calories", "Protein", "Fat", "Fiber",
              "NutritionSource", "NutritionConf", "NutritionBasis"):
        assert k in d, f"missing {k}"
    # The vocabulary is MEASURED / ESTIMATED / MISS since 260822; the old
    # GOOD / PARTIAL words are retired. What this test asserts is the CONTRACT,
    # not which tier happens to answer: a real food must resolve at a tier that
    # names its own provenance, and must never come back MISS.
    assert d["NutritionConf"] in ("MEASURED", "ESTIMATED"), d
    assert d["NutritionSource"].startswith(("bank_observed", "bank_usda")), d
    assert d["NutritionCoverage"] == 1.0, d
    return f"carbs={d['Carbs']}"


# ── 3 · the batch contract: one result per input, IN ORDER ──────────────────
def t_order():
    # Distinct carb levels so a shuffle is detectable, not just a length check.
    foods = ["white rice", "butter", "lettuce", "sugar", "olive oil"]
    s, d = post("/normalize/batch", {"foods": foods})
    assert d["n"] == len(foods), d["n"]
    carbs = [r["Carbs"] for r in d["results"]]
    assert carbs[0] > 20, f"white rice should be carb-dense, got {carbs[0]}"
    assert carbs[2] < 10, f"lettuce should be carb-light, got {carbs[2]}"
    assert carbs[4] is None or carbs[4] < 5, f"olive oil should be ~0 carb, got {carbs[4]}"
    return f"{len(foods)} in order"


# ── 4 · a duplicate must return the identical record ────────────────────────
def t_dedupe():
    s, d = post("/normalize/batch", {"foods": ["fried rice; egg", "milk", "fried rice; egg"]})
    assert d["results"][0] == d["results"][2], "duplicate diverged"
    return "identical"


# ── 5 · THE JSON TRAP. A MISS carries NaN in process; a bare NaN token is not
#        valid JSON and a strict parser rejects the whole reply, so a MISS would
#        reach the caller as a parse error rather than as a MISS.
def t_miss_is_null():
    raw_req = urllib.request.Request(
        URL + "/normalize/batch",
        data=json.dumps({"foods": ["Just Carbs", "Unknown", "xiaolongbao"]}).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(raw_req, timeout=60) as r:
        body = r.read().decode()
    assert "NaN" not in body, "raw NaN token on the wire"
    d = json.loads(body)                      # strict parse must succeed
    for row in d["results"]:
        assert row["NutritionConf"] == "MISS", row
        assert row["Carbs"] is None, row
    return "3 MISS rows, all null"


# ── 6 · every cohort dialect the parser claims to handle ────────────────────
def t_dialects():
    cases = {
        "Egg 50 g\nRice 25 g\nVegetable 100 g": "per_meal",     # Shanghai, all grams
        # A WellDoc item list. Both components sit in the observed bank, so it
        # now resolves per_serving -- which is the better answer and the reason
        # the ladder exists. per_100g remains correct for anything USDA answers.
        "Toasted Bread; Decaf Coffee": "per_serving",           # WellDoc item list
        "Nacho Cheese Tortilla Chips (28g)": "per_meal",        # parenthesised portion
        "Cucumber 100g": "per_meal",                            # tight, no space
    }
    s, d = post("/normalize/batch", {"foods": list(cases)})
    for food, want, row in zip(cases, cases.values(), d["results"]):
        assert row["NutritionBasis"] == want, f"{food!r}: basis {row['NutritionBasis']} != {want}"
    return f"{len(cases)} dialects, basis correct"


# ── 7 · empty input is a valid request, not an error ────────────────────────
def t_empty():
    s, d = post("/normalize/batch", {"foods": []})
    assert s == 200 and d["n"] == 0 and d["results"] == [], d
    return "[] -> []"


# ── 8 · ONE COOK'S WORTH. Shanghai's real distinct meal strings, in one call.
def t_real_cook():
    import glob
    import pandas as pd
    paths = sorted(glob.glob("/home/jluo41/WellDoc-SPACE/_WorkSpace/1-SourceStore/Shanghai/@*/Diet.parquet"))
    if not paths:
        return "SKIPPED (no Shanghai frame)"
    names = pd.read_parquet(paths[-1])["FoodName"].dropna().astype(str).unique().tolist()
    t0 = time.perf_counter()
    s, d = post("/normalize/batch", {"foods": names}, timeout=900)
    el = time.perf_counter() - t0
    assert d["n"] == len(names), f"{d['n']} results for {len(names)} inputs"
    got = sum(1 for r in d["results"] if r["NutritionConf"] in ("MEASURED", "ESTIMATED"))
    meas = sum(1 for r in d["results"] if r["NutritionConf"] == "MEASURED")
    assert got / len(names) > 0.5, f"only {got/len(names):.1%} resolved"
    return (f"{len(names):,} strings, {got/len(names):.1%} resolved "
            f"({meas/len(names):.1%} MEASURED), {el:.1f}s")


# ── 9 · the runaway guard answers 413, not a hang or a 500 ──────────────────
def t_oversize():
    cap = get("/healthz")[1]["max_batch"]
    try:
        post("/normalize/batch", {"foods": ["rice"] * (cap + 1)}, timeout=120)
    except urllib.error.HTTPError as e:
        assert e.code == 413, f"expected 413, got {e.code}"
        return f"413 above {cap:,}"
    raise AssertionError("oversize batch was accepted")


# ── 10 · concurrent callers must not corrupt each other's answers ───────────
def t_concurrent():
    want = post("/normalize/batch", {"foods": ["white rice", "butter"]})[1]["results"]
    with ThreadPoolExecutor(max_workers=8) as ex:
        got = list(ex.map(lambda _: post("/normalize/batch",
                                         {"foods": ["white rice", "butter"]})[1]["results"],
                          range(16)))
    for i, g in enumerate(got):
        assert g == want, f"request {i} diverged"
    return "16 parallel, all identical"


# ── 11 · malformed input is a 422, never a 500 ──────────────────────────────
def t_malformed():
    for bad in ({"food": "rice"}, {"foods": "rice"}, {}):
        try:
            post("/normalize/batch", bad, timeout=30)
            raise AssertionError(f"accepted {bad}")
        except urllib.error.HTTPError as e:
            assert e.code == 422, f"{bad} -> {e.code}, want 422"
    return "3 shapes -> 422"


# ── 12 · latency a caller can plan around ───────────────────────────────────
def t_latency():
    post("/normalize", {"food": "rice"})                     # warm
    ts = []
    for _ in range(10):
        t0 = time.perf_counter(); post("/normalize", {"food": "fried rice"}); ts.append((time.perf_counter()-t0)*1000)
    ts.sort()
    assert ts[len(ts)//2] < 500, f"median {ts[len(ts)//2]:.0f} ms too slow"
    return f"median {ts[len(ts)//2]:.0f} ms, p90 {ts[8]:.0f} ms"


# ── 13-17 · the image lane, over the wire ───────────────────────────────────
#
# These are SKIPPED when no CGMacros frame is on this box, because the point is
# to push real bytes through, not a synthetic pixel.
import glob as _glob
# A SPECIFIC pair, not "the first two on disk". The first frames of this subject
# are a sealed opaque BlenderBottle: nothing edible is visible, so the engine
# correctly declines to name it, and a test built on them asserts that a
# stochastic model hallucinates on demand. These two are a plated meal.
_PAIR = ("/nvme1/group_share/0-RawDataStore/CGMacros/Source/CGMacros-001/photos/"
         "00000007-PHOTO-2020-5-1-20-48-0.jpg",
         "/nvme1/group_share/0-RawDataStore/CGMacros/Source/CGMacros-001/photos/"
         "00000008-PHOTO-2020-5-1-20-57-0.jpg")
_PHOTOS = [p for p in _PAIR if _glob.glob(p)]


def _multipart(path, fields):
    """One multipart body, stdlib only, so the suite has no client dependency."""
    boundary = "----foodnormtest"
    body = b""
    for name, (fname, data, ctype) in fields:
        body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"; "
                 f"filename=\"{fname}\"\r\nContent-Type: {ctype}\r\n\r\n").encode()
        body += data + b"\r\n"
    body += f"--{boundary}--\r\n".encode()
    req = urllib.request.Request(URL + path, data=body,
                                 headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return r.status, json.loads(r.read())


def t_image_upload():
    if not _PHOTOS:
        return "SKIPPED (no CGMacros frames)"
    fields = [("files", (f"f{i}.jpg", open(p, "rb").read(), "image/jpeg"))
              for i, p in enumerate(_PHOTOS)]
    s, d = _multipart("/normalize/image", fields)
    assert s == 200, s
    r = d["result"]
    assert d["n_frames"] == len(_PHOTOS), d
    return _assert_image_contract(r)


def _assert_image_contract(r):
    """The CONTRACT, not one naming outcome. A vision engine is stochastic and a
    frame may genuinely show no food -- this subject's first frames are a sealed
    opaque bottle -- so the test that matters is that BOTH branches stay honest:
    a named meal is fully tagged as derived, and an unnamed one claims nothing.
    Asserting a specific food name would be asserting that a model hallucinates
    on demand."""
    if r["NameSource"] == "typed":
        assert r["FoodNameResolved"] == "Unknown", r
        assert r["NutritionConf"] == "MISS", r
        assert r["Carbs"] is None, r
        assert r["NameConf"] is None, r
        return "no food visible -> clean MISS, claims nothing"
    assert r["NameSource"].startswith("claude-vision"), r["NameSource"]
    assert "|img:" in (r["NutritionSource"] or ""), r["NutritionSource"]
    assert r["FoodNameResolved"] and r["FoodNameResolved"] != "Unknown", r
    assert 0.0 <= r["NameConf"] <= 1.0, r["NameConf"]
    return f"{r['FoodNameResolved'][:36]!r} conf={r['NameConf']}"


def t_image_b64_batch():
    if not _PHOTOS:
        return "SKIPPED"
    import base64
    meals = [[base64.b64encode(open(p, "rb").read()).decode() for p in _PHOTOS]]
    s, d = post("/normalize/image/batch", {"meals": meals}, timeout=300)
    assert d["n"] == 1, d
    return "base64: " + _assert_image_contract(d["results"][0])


def t_image_rejects_non_image():
    try:
        _multipart("/normalize/image", [("files", ("x.txt", b"not an image", "text/plain"))])
    except urllib.error.HTTPError as e:
        assert e.code == 415, f"want 415, got {e.code}"
        return "text/plain -> 415"
    raise AssertionError("accepted a text/plain upload")


def t_image_rejects_too_many():
    cap = 4
    fields = [("files", (f"f{i}.jpg", b"\xff\xd8\xff" + b"0" * 100, "image/jpeg"))
              for i in range(cap + 1)]
    try:
        _multipart("/normalize/image", fields)
    except urllib.error.HTTPError as e:
        assert e.code == 413, f"want 413, got {e.code}"
        return f"{cap+1} frames -> 413"
    raise AssertionError("accepted more frames than the cap")


def t_image_rejects_empty():
    try:
        _multipart("/normalize/image", [("files", ("e.jpg", b"", "image/jpeg"))])
    except urllib.error.HTTPError as e:
        assert e.code == 422, f"want 422, got {e.code}"
        return "empty file -> 422"
    raise AssertionError("accepted an empty file")


if __name__ == "__main__":
    print("=" * 78)
    print(f"  describe-food SERVICE tests · {URL}")
    print("=" * 78)
    for name, fn in [
        ("healthz reports a real bank", t_health),
        ("POST /normalize one string", t_single),
        ("batch: one result per input, in order", t_order),
        ("batch: duplicate returns identical record", t_dedupe),
        ("MISS crosses the wire as null, not NaN", t_miss_is_null),
        ("every cohort dialect, basis correct", t_dialects),
        ("empty batch is 200, not an error", t_empty),
        ("one real cook's distinct strings", t_real_cook),
        ("oversize batch -> 413", t_oversize),
        ("16 concurrent callers agree", t_concurrent),
        ("malformed body -> 422, never 500", t_malformed),
        ("single-call latency", t_latency),
        ("image upload: real frames, derived + tagged", t_image_upload),
        ("image batch via base64", t_image_b64_batch),
        ("non-image upload -> 415", t_image_rejects_non_image),
        ("too many frames -> 413", t_image_rejects_too_many),
        ("empty file -> 422", t_image_rejects_empty),
    ]:
        check(name, fn)
    print("=" * 78)
    print(f"  {len(PASS)} passed · {len(FAIL)} failed")
    print("=" * 78)
    sys.exit(1 if FAIL else 0)
