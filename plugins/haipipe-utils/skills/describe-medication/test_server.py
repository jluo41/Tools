"""
Test describe-medication AS A SERVICE, over the wire.

`test_mednorm.py` tests the RESOLVER. This tests what a consumer touches: a URL.
They fail differently -- a resolver that is perfect in process can still hand a
consumer a JSON parse error on a MISS row, drop a row from a batch and shift
every later row onto the wrong drug, or exceed the caller's timeout.

    python test_server.py            # against $MEDNORM_URL
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

URL = os.environ.get("MEDNORM_URL", "http://127.0.0.1:8079").rstrip("/")
PASS, FAIL = [], []
FIELDS = ["DoseValue", "DoseUnit", "DoseBasis", "DrugKey", "Ingredient",
          "BrandName", "PharmClass", "DosageForm", "Route", "NDC",
          "MedSource", "MedConf", "IsInsulin"]


def post(path, body, timeout=600):
    req = urllib.request.Request(URL + path, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, {"raw": raw[:200].decode("utf-8", "replace")}


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


def t_healthz():
    s, d = get("/healthz")
    assert s == 200 and d["ok"], d
    assert d["bank"].startswith("/"), \
        f"bank path is relative ({d['bank']}); the service would break if " \
        "started from any other directory"
    assert d["counts"]["ndc"] > 100000 and d["counts"]["lexicon"] > 800, d
    return f"v{d['version']}, {d['counts']['ndc']:,} NDC, {d['counts']['lexicon']} lexicon"


def t_one():
    s, d = post("/normalize", {"item": "612997", "dose": 39})
    assert s == 200 and set(d) == set(FIELDS), set(d) ^ set(FIELDS)
    assert d["IsInsulin"] and d["DoseUnit"] == "iu", d
    return f"{d['Ingredient']} {d['DoseValue']} {d['DoseUnit']}"


def t_batch_order():
    items = ["612997", "155744", "612997", "582255"]
    s, d = post("/normalize/batch", {"items": items, "doses": [10, 1, 40, 1]})
    assert s == 200 and d["count"] == len(items)
    r = d["results"]
    assert r[0]["Ingredient"] == r[2]["Ingredient"], "same drug"
    assert r[0]["DoseValue"] == 10 and r[2]["DoseValue"] == 40, "dose is per row"
    return "order held, dose per row"


def t_miss_is_null_not_nan():
    s, raw = post("/normalize/batch",
                  {"items": ["999999999", "zzz"], "doses": [1, 1]})
    txt = json.dumps(raw)
    assert "NaN" not in txt and "Infinity" not in txt, txt[:200]
    for r in raw["results"]:
        assert r["Ingredient"] is None
    return "2 misses, all null"


def t_three_dialects_over_the_wire():
    body = {
        "items": ["612997", "x", "Non-insulin hypoglycemic agents"],
        "doses": [39, 1.5, None],
        "payloads": [None,
                     json.dumps({"MedicationType": "Basal Insulin"}),
                     json.dumps({"MedicationName": "metformin 0.5 g"})],
    }
    s, d = post("/normalize/batch", body)
    r = d["results"]
    assert r[0]["DoseUnit"] == "iu", r[0]
    assert r[1]["IsInsulin"] and r[1]["DrugKey"] == "basal insulin", r[1]
    assert r[2]["DoseUnit"] == "mg" and r[2]["DoseValue"] == 500.0, r[2]
    return "welldoc · ohio · shanghai all correct over HTTP"


def t_sentinel_over_the_wire():
    s, d = post("/normalize", {"item": "612997", "dose": 255})
    assert d["DoseValue"] is None and d["MedConf"] == "MISS", d
    return "255 refused at the boundary too"


def t_empty_batch():
    s, d = post("/normalize/batch", {"items": []})
    assert s == 200 and d["count"] == 0
    return "200, not an error"


def t_length_mismatch_is_422():
    s, d = post("/normalize/batch", {"items": ["a", "b"], "doses": [1]})
    assert s == 422, (s, d)
    return "422 with a readable detail"


def t_malformed_never_500():
    for body in ({"nope": 1}, {"items": "not a list"}):
        s, d = post("/normalize/batch", body)
        assert 400 <= s < 500, (body, s)
    return "2 malformed bodies, all 4xx"


def t_big_batch():
    items = ["612997", "606257", "155744", "zzz"] * 5000
    t0 = time.time()
    s, d = post("/normalize/batch", {"items": items, "doses": 10})
    dt = time.time() - t0
    assert s == 200 and d["count"] == len(items)
    return f"{len(items):,} rows in {dt:.1f}s"


def t_concurrent():
    def one(_):
        return post("/normalize", {"item": "612997", "dose": 39})[1]["Ingredient"]
    with ThreadPoolExecutor(8) as ex:
        vals = set(ex.map(one, range(16)))
    assert len(vals) == 1, vals
    return f"16 calls, one answer ({vals.pop()})"


def t_latency():
    t0 = time.time()
    for _ in range(20):
        post("/normalize", {"item": "612997", "dose": 39})
    ms = (time.time() - t0) / 20 * 1000
    assert ms < 250, f"{ms:.0f} ms"
    return f"{ms:.1f} ms per call"


if __name__ == "__main__":
    print("=" * 78)
    print(f"  describe-medication service  ->  {URL}")
    print("=" * 78)
    try:
        get("/healthz")
    except Exception as e:
        print(f"  unreachable at {URL}: {e}")
        sys.exit(1)
    for name, fn in [
        ("healthz reports absolute bank paths", t_healthz),
        ("single item", t_one),
        ("batch order held, dose per row", t_batch_order),
        ("MISS crosses the wire as null", t_miss_is_null_not_nan),
        ("all three dialects over HTTP", t_three_dialects_over_the_wire),
        ("dose sentinel refused over HTTP", t_sentinel_over_the_wire),
        ("empty batch is 200", t_empty_batch),
        ("length mismatch -> 422", t_length_mismatch_is_422),
        ("malformed -> 4xx never 500", t_malformed_never_500),
        ("20,000 rows in one call", t_big_batch),
        ("16 concurrent callers agree", t_concurrent),
        ("single-call latency", t_latency),
    ]:
        check(name, fn)
    print("=" * 78)
    print(f"  {len(PASS)} passed · {len(FAIL)} failed")
    print("=" * 78)
    sys.exit(1 if FAIL else 0)
