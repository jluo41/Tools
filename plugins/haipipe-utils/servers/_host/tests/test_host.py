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


if __name__ == "__main__":
    print(f"host: {SERVE}")
    check("--list names the lanes without importing them", t_list)
    check("--only with an unknown noun exits non-zero", t_unknown_lane)
    run_insulin_only()
    run_food_without_bank()
    print("=" * 78)
    print(f"  {len(PASS)} passed · {len(FAIL)} failed")
    print("=" * 78)
    sys.exit(1 if FAIL else 0)
