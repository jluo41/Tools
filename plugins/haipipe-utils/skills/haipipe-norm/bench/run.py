#!/usr/bin/env python3
"""Run the family benchmark.

    source .venv/bin/activate && source env.sh
    python Tools/plugins/haipipe-utils/skills/haipipe-norm/bench/run.py --b1
    python .../run.py --b1 --only exercise --tag after-the-fix

B1 needs no service and no gold: it imports each member's door in process and
replays the request/response pairs the family already publishes as
documentation. That is the whole setup.
"""
import argparse
import collections
import datetime
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[5]
sys.path[:0] = [str(HERE.parent)] + [
    str(HERE.parents[1] / d) for d in
    ("describe-food", "describe-exercise", "describe-medication", "describe-insulin")]

from bench import load_profiles, run_b1                          # noqa: E402
from bench.cases import discover                                 # noqa: E402
from bench.report import render_layer, stamp, write_bench        # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--b1", action="store_true", help="run the contract benchmark")
    ap.add_argument("--only", nargs="*", help="member nouns; default all four")
    ap.add_argument("--tag", default=None, help="name this run")
    args = ap.parse_args()
    if not args.b1:
        ap.error("nothing to do; pass --b1")

    when = datetime.datetime.now().isoformat(timespec="seconds")
    tag = args.tag or when[:10].replace("-", "")[2:]

    profiles = load_profiles(args.only)
    runs = []
    for p in profiles:
        fixtures = discover(p.examples, p.port, p.url_env)
        skipped = []
        if p.skip:
            keep = []
            for fx in fixtures:
                why = p.skip(fx)
                (skipped.append({"case": fx["name"], "why": why}) if why
                 else keep.append(fx))
            fixtures = keep
        print(f"  {p.emoji} {p.noun:<12}{len(fixtures):>3} fixtures"
              + (f"  ({len(skipped)} skipped)" if skipped else ""), flush=True)
        r = run_b1(p, fixtures)
        r["n_skipped"] = len(skipped)
        r["skipped"] = skipped
        runs.append(stamp(r, tag, ROOT, when))

    # A chain shares an _XInfo folder, so group by destination, not by member.
    by_dest = collections.OrderedDict()
    for p, r in zip(profiles, runs):
        by_dest.setdefault(p.dest, []).append(r)
    for dest, rs in by_dest.items():
        write_bench(dest, rs, tag)
        print(f"  wrote {dest}")

    layer = ROOT / "_WorkSpace/0-RawDataStore/0-EventNorm"
    folders = [d for d in sorted(layer.iterdir())
               if d.is_dir() and (d / "_stats.json").exists()]
    (layer / "README.md").write_text(render_layer(ROOT, folders))
    print(f"  wrote {layer / 'README.md'}")

    print()
    for r in runs:
        bad = [f"{k} {v['name']}" for k, v in sorted(r["checks"].items())
               if v["status"] in ("FAIL", "ERROR")]
        mark = "✅" if r["verdict"] == "PASS" else "❌"
        print(f"  {mark} {r['noun']:<12}{r['n_fixtures']:>3} fixtures "
              f"{r['n_records']:>4} records" + ("   " + " · ".join(bad) if bad else ""))
    return 0 if all(r["verdict"] == "PASS" for r in runs) else 1


if __name__ == "__main__":
    sys.exit(main())
