"""
Host-level checks for servers/_host/serve.py. Needs no reference bank: the
insulin lane carries its PK table in the package, and the food lane is started
against a bank path that does not exist to prove a missing bank degrades
instead of crashing.

    python servers/_host/tests/test_host.py

Same shape as every lane's test_server.py: PASS/FAIL lines, exit 1 on any FAIL.
"""
import json
import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HOST = Path(__file__).resolve().parents[1]
SERVE = HOST / "serve.py"
PASS, FAIL = [], []


def check(name, fn):
    try:
        note = fn()
        PASS.append(name)
        print(f"  PASS  {name}" + (f"  ({note})" if note else ""))
    except Exception as e:
        FAIL.append(name)
        print(f"  FAIL  {name}\n        {type(e).__name__}: {e}")


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def get(base, path, timeout=10):
    try:
        with urllib.request.urlopen(base + path, timeout=timeout) as r:
            body = r.read()
            return r.status, (json.loads(body) if body.startswith(b"{") or body.startswith(b"[") else body)
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def post(base, path, payload, timeout=30):
    req = urllib.request.Request(base + path, data=json.dumps(payload).encode(),
                                 headers={"content-type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, e.read()


class Host:
    """Run serve.py with the given args on a free port; wait for /healthz."""

    def __init__(self, *args, env=None):
        self.args = list(args)
        self.env = dict(os.environ, **(env or {}))
        self.env.pop("LOCAL_EXTERNAL_STORE", None)      # deterministic: no store unless the test gives one
        self.port = free_port()
        self.base = f"http://127.0.0.1:{self.port}"
        self.proc = None

    def __enter__(self):
        self.proc = subprocess.Popen([sys.executable, str(SERVE), "--host", "127.0.0.1",
                                      "--port", str(self.port), *self.args],
                                     env=self.env, stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT, text=True)
        for _ in range(120):
            if self.proc.poll() is not None:
                raise RuntimeError("host exited early:\n" + self.proc.stdout.read())
            try:
                urllib.request.urlopen(self.base + "/healthz", timeout=2)
                return self
            except Exception:
                time.sleep(0.5)
        raise RuntimeError("host never answered /healthz")

    def __exit__(self, *exc):
        self.proc.terminate()
        try:
            self.proc.wait(10)
        except subprocess.TimeoutExpired:
            self.proc.kill()


def t_list():
    out = subprocess.run([sys.executable, str(SERVE), "--list"], capture_output=True, text=True, timeout=60)
    assert out.returncode == 0, out.stderr
    nouns = [l.split()[0] for l in out.stdout.splitlines() if l.strip()]
    assert "insulin" in nouns, nouns
    return ", ".join(nouns)


def t_unknown_lane():
    out = subprocess.run([sys.executable, str(SERVE), "--only", "nosuch", "--port", str(free_port())],
                         capture_output=True, text=True, timeout=120)
    assert out.returncode != 0
    assert "no lane" in (out.stderr + out.stdout), out.stderr[-300:]
    return f"exit {out.returncode}"


def run_insulin_only():
    with Host("--only", "insulin") as h:
        def t_index():
            st, body = get(h.base, "/")
            assert st == 200 and list(body["lanes"]) == ["insulin"], body
            lane = body["lanes"]["insulin"]
            assert lane["prefix"] == "/insulin" and lane["url_var"] == "INSNORM_URL"
            assert "POST /normalize/batch" in lane["routes"], lane["routes"]
            assert body["failed"] == {}
            return "one lane, three routes, nothing failed"
        check("index lists exactly the mounted lane", t_index)

        def t_health():
            st, body = get(h.base, "/healthz")
            assert st == 200 and body["status"] == "ok", body
            assert body["lanes"]["insulin"]["ok"] is True
            return f"products={body['lanes']['insulin'].get('products')}"
        check("host /healthz aggregates the lane", t_health)

        def t_lane_health():
            st, body = get(h.base, "/insulin/healthz")
            assert st == 200 and body["ok"] is True, body
            return f"v{body['version']}"
        check("lane /healthz answers under its prefix", t_lane_health)

        def t_one():
            st, body = post(h.base, "/insulin/normalize", {"item": "Insulin lispro-aabc"})
            assert st == 200 and body["InsulinClass"] == "rapid", body
            return f"lispro-aabc -> {body['InsulinClass']} onset {body['OnsetMin']}"
        check("POST /insulin/normalize", t_one)

        def t_batch():
            st, body = post(h.base, "/insulin/normalize/batch", {"items": ["Novolin R", "metformin"]})
            assert st == 200 and body["count"] == 2 and len(body["results"]) == 2, body
            return "2 in, 2 out"
        check("POST /insulin/normalize/batch", t_batch)

        def t_docs():
            st, _ = get(h.base, "/insulin/docs")
            assert st == 200, st
            st, spec = get(h.base, "/insulin/openapi.json")
            assert st == 200 and "/normalize/batch" in spec["paths"], list(spec.get("paths", []))
            return "docs + openapi under the prefix"
        check("lane docs are served under its prefix", t_docs)

        def t_unmounted():
            st, _ = get(h.base, "/food/healthz")
            assert st == 404, st
            return "404"
        check("an unmounted lane is a 404, not a crash", t_unmounted)


def run_food_without_bank():
    env = {"FOODNORM_DB": "/nonexistent/usda_nutrition.sqlite"}
    with Host("--only", "food", env=env) as h:
        def t_degraded():
            st, body = get(h.base, "/healthz")
            assert st == 200 and body["status"] == "degraded", body
            if "food" in body["failed"]:
                return "food failed to import: " + body["failed"]["food"][:80]
            lane = body["lanes"]["food"]
            assert lane["ok"] is False and lane.get("bank_exists") is False, lane
            return "mounted, bank_exists=false"
        check("a missing bank degrades /healthz instead of crashing the host", t_degraded)


def run_try_page():
    """The try page (JL 261021: a small page that calls the API, with a gallery below): /try/<noun> serves it,
    /try/<noun>/gallery reads one card per input folder under $EVENTNORM_ROOT, an unmounted noun is a 404."""
    import tempfile
    with tempfile.TemporaryDirectory() as root:
        kind = Path(root) / "_InsInfo" / "0-inputs" / "01-one-name"
        kind.mkdir(parents=True)
        (kind / "input.json").write_text(json.dumps({"item": ["Novolin R"]}))
        (kind / "door.json").write_text(json.dumps([{"InsulinClass": "short"}]))
        (kind / "NOTE.md").write_text("# one insulin, named\n\nboard   **12 rows (1.0%)**\n\nSPECIMEN. Real rows. 'Novolin R'.\n")
        photo = Path(root) / "_InsInfo" / "0-inputs" / "02-photo"
        photo.mkdir(parents=True)
        (photo / "input.json").write_text(json.dumps({"item": ["Unknown"], "ImagePath": ["x/CGMacros-001/photos/p.jpg"]}))
        (photo / "NOTE.md").write_text("# a photo\n\nSPECIMEN. Real rows, from CGMacros-001.\n")
        with Host("--only", "insulin", env={"EVENTNORM_ROOT": root}) as h:
            def t_page():
                st, body = get(h.base, "/try/insulin")
                assert st == 200 and b"try it" in body, st
                st, idx = get(h.base, "/")
                assert idx["lanes"]["insulin"]["try"] == "/try/insulin", idx["lanes"]["insulin"]
                return "the page, and the index names it"
            check("GET /try/<noun> serves the try page", t_page)

            def t_gallery():
                st, g = get(h.base, "/try/insulin/gallery")
                assert st == 200 and g["folder"].endswith("_InsInfo/0-inputs"), g
                c = g["cards"][0]
                assert len(g["cards"]) == 2 and c["kind"] == "01-one-name" and c["title"] == "one insulin, named", c
                ph = g["cards"][1]
                assert ph["input"]["ImagePath"] == ["(photo, path hidden)"], ph       # never a subject's folder
                assert "CGMacros-001" not in json.dumps(g) and "CGMacros-<subject>" in ph["specimen"], ph
                assert c["board"] == "12 rows (1.0%)" and c["specimen"].startswith("SPECIMEN"), c
                assert c["input"] == {"item": ["Novolin R"]} and c["frozen"] == [{"InsulinClass": "short"}], c
                return "cards: title, board, specimen, input, frozen; a photo path and a subject id hidden"
            check("GET /try/<noun>/gallery reads the input folders", t_gallery)

            def t_unmounted():
                st, _ = get(h.base, "/try/food")
                assert st == 404, st
                return "404"
            check("the try page of an unmounted lane is a 404", t_unmounted)

            def t_no_events():
                st, g = get(h.base, "/try/insulin/events")
                assert st == 200 and g["cards"] == [], g
                return "a lane with no event door: no cards"
            check("GET /try/<noun>/events answers for every mounted lane", t_no_events)

        def t_events():
            """The event gallery's cards, read in process: record ids, a photo path and a subject id never leave."""
            import importlib.util
            f = Path(root) / "_FoodInfo" / "7-events" / "events.json"
            f.parent.mkdir(parents=True)
            row = {"CarbEntryID": "AA642FEE-8992-42F1-A461-C198BBAFC627", "ObservationCreatedBy": "932",
                   "FoodName": "Spinach", "Image path": "photos/p.jpg"}
            raw = {"type": "app_log", "file": "x/CGMacros-001/a.csv", "rows": [row]}
            f.write_text(json.dumps({"about": "a test", "cards": [{"kind": "app_log", "title": "one row", "send": {"raw": raw},
                                                                    "raw": raw, "input": {}, "output": {}}]}))
            spec = importlib.util.spec_from_file_location("host_serve", SERVE)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            os.environ["EVENTNORM_ROOT"] = root
            try:
                g = mod.events("food")
            finally:
                os.environ.pop("EVENTNORM_ROOT", None)
            c = g["cards"][0]
            r = c["send"]["raw"]["rows"][0]
            assert r["CarbEntryID"] == r["ObservationCreatedBy"] == "(id hidden)" and r["FoodName"] == "Spinach", r
            assert r["Image path"] == "(photo, path hidden)" and "CGMacros-001" not in json.dumps(g), g
            return "record ids, a photo path and a subject id hidden; the food kept"
        check("the event gallery hides what is whose", t_events)


if __name__ == "__main__":
    print(f"host: {SERVE}")
    check("--list names the lanes without importing them", t_list)
    check("--only with an unknown noun exits non-zero", t_unknown_lane)
    run_insulin_only()
    run_food_without_bank()
    run_try_page()
    print("=" * 78)
    print(f"  {len(PASS)} passed · {len(FAIL)} failed")
    print("=" * 78)
    sys.exit(1 if FAIL else 0)
