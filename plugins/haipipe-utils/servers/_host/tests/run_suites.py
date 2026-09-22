"""
Start the host, run every mounted lane's black-box service suite against it,
and exit non-zero if any suite failed.

    python servers/_host/tests/run_suites.py --store /path/to/_WorkSpace/ExternalStore
    python servers/_host/tests/run_suites.py --only insulin              # no bank needed

Each lane's suite is servers/api-<noun>/tests/test_server.py, the same script
that sat beside the skill before the move. The one thing this runner adds is
the URL it posts to: <NOUN>NORM_URL=http://127.0.0.1:<port>/<noun>.
"""
import argparse
import json
import os
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

HOST = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HOST))
from serve import SERVERS, lane_dir, url_var  # noqa: E402


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", default=None)
    ap.add_argument("--only", default=None)
    ap.add_argument("--port", type=int, default=None)
    ap.add_argument("--timeout", type=int, default=1800, help="seconds per suite")
    a = ap.parse_args(argv)

    port = a.port or free_port()
    base = f"http://127.0.0.1:{port}"
    args = [sys.executable, str(HOST / "serve.py"), "--host", "127.0.0.1", "--port", str(port)]
    if a.store:
        args += ["--store", a.store]
    if a.only:
        args += ["--only", a.only]
    host = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    results = {}
    try:
        for _ in range(240):
            if host.poll() is not None:
                print(host.stdout.read())
                return 2
            try:
                with urllib.request.urlopen(base + "/", timeout=2) as r:
                    index = json.loads(r.read())
                break
            except Exception:
                time.sleep(0.5)
        else:
            print("host never came up")
            return 2

        for noun, err in index["failed"].items():
            results[noun] = ("IMPORT FAILED", err)
        for noun in index["lanes"]:
            suite = lane_dir(noun) / "tests" / "test_server.py"
            if not suite.exists():
                results[noun] = ("NO SUITE", str(suite))
                continue
            print(f"\n==== {noun}  {suite.relative_to(SERVERS.parent)}  {url_var(noun)}={base}/{noun}")
            env = dict(os.environ, **{url_var(noun): f"{base}/{noun}"})
            t = subprocess.run([sys.executable, str(suite)], env=env, timeout=a.timeout)
            results[noun] = ("ok" if t.returncode == 0 else f"exit {t.returncode}", "")
    finally:
        host.terminate()
        try:
            host.wait(10)
        except subprocess.TimeoutExpired:
            host.kill()

    print("\n" + "=" * 78)
    bad = 0
    for noun, (status, note) in sorted(results.items()):
        print(f"  {noun:12s} {status}  {note}")
        bad += status != "ok"
    print("=" * 78)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
