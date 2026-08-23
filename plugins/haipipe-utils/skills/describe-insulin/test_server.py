"""
Test describe-insulin AS A SERVICE, over the wire.

    python test_server.py            # against $INSNORM_URL
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

URL = os.environ.get("INSNORM_URL", "http://127.0.0.1:8080").rstrip("/")
PASS, FAIL = [], []
FIELDS = ["InsulinClass", "OnsetMin", "PeakMin", "DurationMin", "Biphasic",
          "InsulinResolved", "PKSource", "PKConf"]


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
    assert s == 200 and d["ok"] and d["products"] >= 15, d
    return f"v{d['version']}, {d['products']} products, {d['aliases']} aliases"


def t_one():
    s, d = post("/normalize", {"item": "Insulin lispro-aabc"})
    assert s == 200 and set(d) == set(FIELDS), set(d) ^ set(FIELDS)
    assert d["InsulinClass"] == "rapid", d
    return f"{d['InsulinResolved']} onset {d['OnsetMin']} dur {d['DurationMin']}"


def t_peakless_null_over_the_wire():
    """A peakless drug must cross the wire as null, not 0. A consumer that read
    0 would place the maximum effect at the moment of injection."""
    s, d = post("/normalize", {"item": "insulin glargine"})
    assert d["PeakMin"] is None, d
    assert "null" in json.dumps(d), d
    return "glargine PeakMin = null"


def t_chain_input_from_medication():
    """The real seam: every DrugKey describe-medication emits for insulin."""
    keys = ["Insulin lispro-aabc", "Insulin lispro", "Insulin glargine",
            "bolus insulin", "basal insulin", "Novolin R", "insulin degludec",
            "insulin aspart 70/30", "Human Insulin", "insulin detemir"]
    s, d = post("/normalize/batch", {"items": keys})
    assert s == 200 and d["count"] == len(keys)
    miss = [k for k, r in zip(keys, d["results"]) if r["InsulinClass"] is None]
    assert not miss, miss
    return f"{len(keys)}/{len(keys)} DrugKeys resolve"


def t_patient_dia_over_the_wire():
    s, d = post("/normalize", {"item": "basal insulin", "dia_hours": 7.0})
    assert d["PKConf"] == "GOOD" and d["DurationMin"] == 420.0, d
    return "measured DIA -> GOOD"


def t_non_insulin_miss():
    s, d = post("/normalize/batch", {"items": ["metformin", "LISINOPRIL"]})
    for r in d["results"]:
        assert r["InsulinClass"] is None and r["PKConf"] == "MISS", r
    return "2 non-insulins refused"


def t_empty_batch():
    s, d = post("/normalize/batch", {"items": []})
    assert s == 200 and d["count"] == 0
    return "200"


def t_length_mismatch_is_422():
    s, d = post("/normalize/batch", {"items": ["a", "b"], "dia_hours": [1]})
    assert s == 422, (s, d)
    return "422"


def t_malformed_never_500():
    for body in ({"nope": 1}, {"items": "not a list"}):
        s, d = post("/normalize/batch", body)
        assert 400 <= s < 500, (body, s)
    return "2 bodies, all 4xx"


def t_big_batch():
    items = ["Insulin lispro", "Insulin glargine", "metformin"] * 6000
    t0 = time.time()
    s, d = post("/normalize/batch", {"items": items})
    dt = time.time() - t0
    assert s == 200 and d["count"] == len(items)
    return f"{len(items):,} rows in {dt:.1f}s"


def t_concurrent():
    def one(_):
        return post("/normalize", {"item": "Insulin lispro"})[1]["DurationMin"]
    with ThreadPoolExecutor(8) as ex:
        vals = set(ex.map(one, range(16)))
    assert len(vals) == 1, vals
    return f"16 calls, one answer ({vals.pop()})"


if __name__ == "__main__":
    print("=" * 78)
    print(f"  describe-insulin service  ->  {URL}")
    print("=" * 78)
    try:
        get("/healthz")
    except Exception as e:
        print(f"  unreachable at {URL}: {e}")
        sys.exit(1)
    for name, fn in [
        ("healthz", t_healthz),
        ("single item", t_one),
        ("peakless crosses as null, not 0", t_peakless_null_over_the_wire),
        ("every DrugKey from the chain resolves", t_chain_input_from_medication),
        ("measured DIA over HTTP", t_patient_dia_over_the_wire),
        ("non-insulin is a clean miss", t_non_insulin_miss),
        ("empty batch is 200", t_empty_batch),
        ("length mismatch -> 422", t_length_mismatch_is_422),
        ("malformed -> 4xx never 500", t_malformed_never_500),
        ("18,000 rows in one call", t_big_batch),
        ("16 concurrent callers agree", t_concurrent),
    ]:
        check(name, fn)
    print("=" * 78)
    print(f"  {len(PASS)} passed · {len(FAIL)} failed")
    print("=" * 78)
    sys.exit(1 if FAIL else 0)
