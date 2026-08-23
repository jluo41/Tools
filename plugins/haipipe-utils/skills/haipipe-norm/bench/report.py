"""Write a run into an _XInfo folder's 6-benchmark layer.

WHY THE RUNS ARE NOT IN 2-corpus
================================================================================
`2-corpus` is the RULER: a frozen gold, built once, never edited, and a change
to it invalidates every comparison ever made against it. `6-benchmark` is the
READING: there are many, they are dated, and the whole point is to line them up
over time.

They were in one folder -- `_FoodInfo/2-corpus/bench_gate_b.json` -- and mixing
them means a reader cannot tell which file is the measurement and which is the
thing measured.
"""
import datetime
import json
import pathlib
import subprocess
from typing import Dict, List

SCHEMA = pathlib.Path(__file__).resolve().parent / "schema.json"

STATUS = {"PASS": "✅", "FAIL": "❌", "NA": "➖", "ERROR": "💥"}


def git_head(root: pathlib.Path) -> str:
    try:
        h = subprocess.run(["git", "-C", str(root), "rev-parse", "--short", "HEAD"],
                           capture_output=True, text=True, timeout=10).stdout.strip()
        d = subprocess.run(["git", "-C", str(root), "status", "--porcelain",
                            "--untracked-files=no"],
                           capture_output=True, text=True, timeout=20).stdout.strip()
        return h + ("-dirty" if d else "")
    except Exception:                                            # noqa: BLE001
        return "unknown"


def stamp(run: Dict, tag: str, root: pathlib.Path, when: str) -> Dict:
    """A number with no commit behind it is not a measurement."""
    return {"bench": "B1_contract", "tag": tag, "at": when,
            "git_head": git_head(root), **run}


def write_bench(dest: pathlib.Path, runs: List[Dict], tag: str) -> pathlib.Path:
    """One folder, one or more members. `_MedInfo` holds two: a chain shares an
    _XInfo folder, so a folder is not a member."""
    dest = pathlib.Path(dest)
    (dest / "runs").mkdir(parents=True, exist_ok=True)
    for r in runs:
        (dest / "runs" / f"{tag}-contract-{r['noun']}.json").write_text(
            json.dumps(r, indent=1, default=str) + "\n")

    latest = {"schema": "bench-v1", "bench": "B1_contract", "tag": tag,
              "at": runs[0]["at"], "git_head": runs[0]["git_head"],
              "members": {r["noun"]: _summary(r) for r in runs}}
    (dest / "_contract.json").write_text(json.dumps(latest, indent=1) + "\n")

    # README.md in this folder belongs to the noun's own benchmark generator and
    # is NOT ours to rewrite: B1 is one metric among that scorecard's four, not
    # the scorecard. We write our own page beside it.
    (dest / "CONTRACT.md").write_text(render(dest, runs, tag))
    return dest


def _summary(r: Dict) -> Dict:
    return {"verdict": r["verdict"], "n_checks_failed": r["n_checks_failed"],
            "n_fixtures": r["n_fixtures"], "n_records": r["n_records"],
            "n_skipped": r.get("n_skipped", 0),
            "checks": {k: v["status"] for k, v in r["checks"].items()}}


def _ids(runs):
    seen = []
    for r in runs:
        for k in sorted(r["checks"]):
            if k not in seen:
                seen.append(k)
    return seen


def grid(runs: List[Dict]) -> List[str]:
    ids = _ids(runs)
    w = max(len(r["noun"]) for r in runs) + 2
    head = f"{'check':<6}{'asserts':<58}" + "".join(f"{r['noun'][:9]:>{w}}" for r in runs)
    lines = [head, "─" * len(head)]
    for cid in ids:
        asserts = next((r["checks"][cid]["asserts"] for r in runs if cid in r["checks"]), "")
        name = next((r["checks"][cid]["name"] for r in runs if cid in r["checks"]), "")
        lines.append(f"{cid:<6}{(name + ' · ' + asserts)[:57]:<58}"
                     + "".join(f"{STATUS.get(r['checks'].get(cid, {}).get('status'), '  ·'):>{w}}"
                               for r in runs))
    return lines


def render(dest: pathlib.Path, runs: List[Dict], tag: str) -> str:
    ok = all(r["verdict"] == "PASS" for r in runs)
    L = ["# CONTRACT -- B1", "",
         "ONE metric of this noun's scorecard, and the only one that needed no",
         "gold. `README.md` beside this file is the scorecard; this page is its",
         "contract column, written by the SHARED engine so that all four members",
         "are asked exactly the same questions in exactly the same words.", "",
         "`2-corpus` next door is the ruler and is frozen. `runs/` is what the",
         "ruler said, one file per run, so they line up over time.", "",
         "GENERATED. Do not hand-edit. The producer is under git at",
         "`Tools/plugins/haipipe-utils/skills/haipipe-norm/bench/`.", "",
         "```bash",
         "source .venv/bin/activate && source env.sh",
         "python Tools/plugins/haipipe-utils/skills/haipipe-norm/bench/run.py --b1",
         "```", "",
         "", "## B1 CONTRACT", "",
         "Ten invariants of the haipipe-norm contract. **No labels are involved**,",
         "which is why B1 could run on day one and why it is the honest evidence",
         "for the word NORMALIZED: B2 measures whether an answer is right, but only",
         "B1 measures whether four skills written weeks apart are one system.", "",
         f"run `{tag}` · {runs[0]['at']} · code at `{runs[0]['git_head']}`", "",
         "```text", *grid(runs), "```", ""]

    fails = [(r, cid, c) for r in runs for cid, c in sorted(r["checks"].items())
             if c["status"] in ("FAIL", "ERROR")]
    if fails:
        L += ["", "## What failed", ""]
        for r, cid, c in fails:
            L += [f"**{r['noun']} · {cid} {c['name']}** — {c['asserts']}", "",
                  f"{c['n_bad']} of {c['n']}.", "", "```text"]
            for f in c["failures"][:6]:
                L.append("  " + json.dumps(f, default=str)[:200])
            L += ["```", ""]
    else:
        L += ["", "Every check passed on every member.", ""]

    skipped = [(r["noun"], s) for r in runs for s in r.get("skipped", [])]
    if skipped:
        L += ["", "## Not replayed, and why", "",
              "A benchmark that silently drops its hard cases reads as coverage it",
              "does not have. Every case B1 declined is here.", "", "```text"]
        for noun, s in skipped:
            L.append(f"  {noun:<12}{s['case']:<34}{s['why']}")
        L += ["```", ""]

    L += ["", "## The three benchmarks, and why only one of them is here", "",
          "```text",
          "  B1  CONTRACT     does the door answer in the shape it promised?",
          "                   no labels · comparable across every noun      ← this file",
          "  B2  GOLD         is the number right?",
          "                   needs labels · comparable across NOTHING",
          "  B3  CALIBRATION  does the most-trusted tier actually win?",
          "                   needs B2's gold, reads the declared order",
          "```", "",
          "B2's numbers are not comparable between nouns and must never be tabled",
          "side by side: food's gold is a cohort's own declared macros, insulin's is",
          "a prescriber's setting with three possible values, exercise's is",
          "back-solved from a device's proprietary model, and medication has none",
          "at all. Each is honest about its own noun and about nothing else.", ""]
    return "\n".join(L) + "\n"


def render_layer(root: pathlib.Path, folders: List[pathlib.Path]) -> str:
    """`0-EventNorm/README.md` -- the one page above all the nouns."""
    rows, tag, at, head = [], "", "", ""
    for f in folders:
        b = f / "6-benchmark" / "_contract.json"
        s = f / "_stats.json"
        stats = json.loads(s.read_text()) if s.exists() else []
        live = [x for x in stats if x.get("rows")]
        n_rows = sum(x["rows"] for x in live)
        n_res = sum(x.get("denominator", {}).get("resolvable", x["rows"]) for x in live)
        n_w = sum(x.get("coverage", {}).get("value_written", 0) for x in live)
        order = next((x.get("confidence_order") for x in live if x.get("confidence_order")), [])
        bench = json.loads(b.read_text()) if b.exists() else {}
        tag = bench.get("tag", tag) or tag
        at = bench.get("at", at) or at
        head = bench.get("git_head", head) or head
        # ONE MEMBER PER _XInfo FOLDER since insulin moved to `_InsInfo`, so
        # every line now carries its own counts. The guard stays: if a chain is
        # ever housed together again, the counts belong to the table and not to
        # each member, and repeating them would invent a corpus twice.
        for i, (noun, m) in enumerate((bench.get("members") or {"?": {}}).items()):
            first = (i == 0)
            rows.append((f.name if first else "", noun, len(live) if first else "",
                         n_rows if first else None, n_res if first else None,
                         n_w if first else None, order,
                         m.get("verdict", "-"), m.get("n_checks_failed", "-")))

    w = "{:<16}{:<12}{:>4}{:>10}{:>10}{:>10}{:>9}  {:<10}{:>8}"
    lines = [w.format("folder", "member", "coh", "rows", "solvable", "written",
                      "of solv", "B1", "failed"),
             "─" * 91]
    for name, noun, ncoh, nr, nres, nw, order, verdict, nf in rows:
        lines.append(w.format(
            name, noun, str(ncoh), f"{nr:,}" if nr else "",
            f"{nres:,}" if nres else "", f"{nw:,}" if nw else "",
            f"{nw / nres:.1%}" if nres else "",
            f"{STATUS.get(verdict, '·')} {verdict}", str(nf)))

    vocab = []
    for f in folders:
        s = f / "_stats.json"
        if not s.exists():
            continue
        st = [x for x in json.loads(s.read_text()) if x.get("rows")]
        o = next((x.get("confidence_order") for x in st if x.get("confidence_order")), None)
        t = next((x.get("trusted") for x in st if x.get("trusted")), None)
        if o:
            vocab.append(f"  {f.name:<16}{' / '.join(o):<38}trusted: {' / '.join(t or [])}")

    return "\n".join([
        "# 0-EventNorm", "",
        "Every logged EVENT a cohort records -- what was eaten, what was done,",
        "what was taken -- normalized against a reference bank into numbers that",
        "carry their own provenance.", "",
        "One folder per noun, all the same six layers, all written by",
        "`haipipe-norm/xinfo`. A reader who has read one can read the rest.", "",
        "GENERATED. Do not hand-edit. The producers are under git at",
        "`Tools/plugins/haipipe-utils/skills/`.", "",
        "", "## The nouns", "", "```text", *lines, "```", "",
        "`solvable` is the HONEST DENOMINATOR: rows that could have been resolved",
        "at all. `B1` is the contract benchmark -- no labels, same ten checks for",
        "every member. The three coverage columns are NOT comparable between rows:",
        "they answer 'how much of this noun did we resolve', and the nouns are",
        "different questions.", "",
        "", "## Confidence is per noun, and the order is declared", "",
        "There is no one vocabulary and imposing one was tried and rejected.",
        "describe-food ranks whether a value was MEASURED or modelled;",
        "describe-medication ranks how likely a match is to be right. Different",
        "questions. What every member must declare is an ORDER, so the shared",
        "benchmark reads it instead of hard-coding a family default.", "",
        "```text", *vocab, "```", "",
        "", "## Layers", "", "```text",
        "  1-per-cohort     one page per cohort: what goes in, and what comes out",
        "  2-corpus         the gradeable subset and its frozen gold -- the RULER",
        "  3-reference      symlinks to the banks in ExternalStore. never copies",
        "  4-contract       the record's JSON Schema and worked specimens",
        "  5-api-examples   real request/response pairs against the running service",
        "  6-benchmark      what the ruler said -- the READINGS, one file per run",
        "```", "",
        f"B1 last run: `{tag}` · {at} · code at `{head}`", "",
    ]) + "\n"
