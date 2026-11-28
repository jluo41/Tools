"""chain_check.py · a paper Board's chain work → value → display → writing, checked end to end (JL 261110).

    python chain_check.py <paper Board> [--root <SPACE root>] [--json]

Prints one line per failure, `FAIL <rule> <where>: <what>` (<where> relative to the Board), then a summary line; exits 1
on any failure, 0 otherwise. It reads only: nothing under the Board is written. The rules (JL 261110):

    1 Only work computes; a value Run copies and gives ids; a display draws; a Section quotes.
    2 Every number a display prints is a value id.
    3 Pinned versions: a display Run names its value Run; a Section names the value Run it quotes; never "the newest".
    4 Things compared share a setup.                     (not checked here: a person reads it)
    5 Old-setup ids leave the list.
    6 Staleness travels down.
    7 A second, independent route recomputes the headline numbers.
    8 One check Run before a send (gate G4).              (this script is that check; paper_check.py row V11)

What it checks, per value Task of the Board's value Job (`jNN_evidence_value`), in either of two shapes:

    value map   tNN_/scripts/value_map.yaml (values_ledger.py's own shape): the value Run reads, it does not copy.
                (b) each value re-read from its work Run (values_ledger.catalog) equals the value Run's values.yaml.
    copying     tNN_/scripts/values.yaml with `sources:` and `values:` (id, from: <key>/<file>, where + column or a
                json key, transform, fmt, flag): the value Run copies each source's files into result/<key>/.
                (a) each copy is byte-identical to its work Run's file; (b) each id re-read from the work Run's own
                file (not the copy) equals values.json's value and text.
    other       any other value Task: (a) on the newest Run holding result/<dir>/SOURCE.txt copies.

and for every shape: each work Run read is complete (result/runtime.yaml status completed); (c) a work Task with a newer
completed Run than the newest one the value Job reads there makes the value Task stale (an older one passed over is on purpose);
a display or a Section on an older value Run is stale only when what it read changed or left there (its read files, its ids);
no id sits in two value Tasks; (g) a value with a `flag` (an older setup, check before quoting) fails rule 5.

The current value Run of a Task: the `RUN = "..."` constant of the value Job's src/gen_runs.py when that Run is in the
Task (the copying shape pins it there), else its newest completed Run.

    displays    (d) each display Task of the display Job: the Run its face names as printed (`printed: <run>` or
                `made-by: runs/<run>`; else its newest Run). Its run.yaml `reads:` holds no path under work/; it names
                a value Run (a reads path `<value Job>/tNN_/runs/rNN_/`, or display.yaml `value_run:`), and that Run
                is the current one; each id of result/values_used.csv (if any) equals the current value (its `value`
                column, else its `text`).
    Sections    (e) each VALUE card binding (values_ledger.bindings) names a value Run (`run:`) that is the current
                one, and its printed number agrees (values_ledger.check_binding: differs or stale fail); each path
                `<value Job>/tNN_/runs/rNN_` the writing Job's text names is the current value Run.
    rule 7      (f) the Board's or the value Job's `scripts/recompute_check.py`, or a face line `recompute: <path>`
                (board.md or the value Job's face), run with this Python from the Project folder, the Board as its
                argument; a non-zero exit fails, its output is printed.

The Project is the nearest folder above the Board that holds work/. --root is the SPACE root that SOURCE.txt paths
are relative to (default: found as values_ledger finds it; a path holding `work/` is also read from the Project).
"""
from __future__ import annotations

import argparse
import csv
import filecmp
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import paper_text as pt  # noqa: E402

RUN_RE = re.compile(r"r(\d+)_")
DONE = ("completed", "complete")
TRANSFORM = {None: lambda x: x, "pct10": lambda x: (10 ** x - 1) * 100}
CHECK_TASK = "t99_paper_value_check"
TEXT_SUFFIXES = (".md", ".tex", ".yaml", ".yml", ".txt")


# ════════════════════════════════════════════ small readers ══════════════════════════════════════════════════════════
def read_yaml(f: Path):
    try:
        return yaml.safe_load(f.read_text(encoding="utf-8")) if f.is_file() else None
    except yaml.YAMLError:
        return None


def rnum(name: str) -> int:
    m = RUN_RE.match(name)
    return int(m.group(1)) if m else -1


def runs_of(task: Path) -> list:
    d = task / "runs"
    return sorted((r for r in d.iterdir() if r.is_dir() and RUN_RE.match(r.name)), key=lambda r: rnum(r.name)) if d.is_dir() else []


def status(run: Path) -> str:
    rt = read_yaml(run / "result" / "runtime.yaml")
    return str(rt.get("status", "")).strip() if isinstance(rt, dict) else ""


def complete(run: Path) -> bool:
    return status(run) in DONE


def field(text: str, name: str) -> str:
    m = re.search(rf"(?m)^{re.escape(name)}:\s*(.+?)\s*$", text)
    return m.group(1) if m else ""


def face_text(folder: Path) -> str:
    f = folder / f"{folder.name}.md"
    return f.read_text(encoding="utf-8") if f.is_file() else ""


def num(x):
    if isinstance(x, bool) or x is None:
        return x
    if isinstance(x, (int, float)):
        return float(x)
    try:
        return float(str(x).replace(",", ""))
    except ValueError:
        return x


def same(a, b) -> bool:
    if isinstance(a, list) or isinstance(b, list):
        return isinstance(a, list) and isinstance(b, list) and len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    a, b = num(a), num(b)
    if isinstance(a, float) and isinstance(b, float):
        return abs(a - b) <= 1e-9 * max(1.0, abs(a), abs(b))
    return a == b


def short(x, n=90) -> str:
    s = " ".join(str(x).split())
    return s if len(s) <= n else s[: n - 1] + "…"


class Report:
    def __init__(self, board: Path, project: Path):
        self.board, self.project = board, project
        self.fails, self.notes = [], []
        self.seen = Counter()

    def where(self, p) -> str:
        p = Path(p)
        for base in (self.board, self.project):
            try:
                return p.resolve().relative_to(base.resolve()).as_posix()
            except ValueError:
                pass
        return p.name

    def fail(self, rule: int, where, what: str):
        w = where if isinstance(where, str) else self.where(where)
        self.fails.append({"rule": rule, "where": w, "what": what})

    def note(self, line: str):
        self.notes.append(line)


# ════════════════════════════════════════════ the value Job ══════════════════════════════════════════════════════════
def value_job(board: Path):
    return next((j for j in sorted(board.glob("j[0-9]*_*")) if j.is_dir() and re.search(r"evidence_value|_values?$", j.name)), None)


def display_job(board: Path):
    return next((j for j in sorted(board.glob("j[0-9]*_*")) if j.is_dir() and re.search(r"display", j.name)), None)


def pinned_run(j02: Path):
    """The RUN constant of the value Job's src/gen_runs.py (the copying shape pins its current value Run there)."""
    for f in [j02 / "src" / "gen_runs.py", j02 / "scripts" / "gen_runs.py"]:
        if f.is_file():
            m = re.search(r"""(?m)^RUN\s*=\s*["']([^"']+)["']""", f.read_text(encoding="utf-8"))
            if m:
                return m.group(1)
    return None


class ValueTask:
    def __init__(self, task: Path, pin):
        self.task, self.name, self.tnn = task, task.name, task.name.split("_")[0]
        if (task / "scripts" / "value_map.yaml").is_file():
            self.shape, self.cfg = "value map", read_yaml(task / "scripts" / "value_map.yaml") or {}
        else:
            cfg = read_yaml(task / "scripts" / "values.yaml")
            if isinstance(cfg, dict) and "sources" in cfg:
                self.shape, self.cfg = "copying", cfg
            else:
                self.shape, self.cfg = "other", {}
        runs = runs_of(task)
        named = next((r for r in runs if r.name == pin), None) if pin else None
        want = "values.yaml" if self.shape == "value map" else "values.json"
        done = [r for r in runs if complete(r)]
        self.current = named or next((r for r in reversed(done) if (r / "result" / want).is_file()), None) or (done[-1] if done else None)
        self.pinned = named is not None
        self.values = {}          # id -> {value, text, flag}
        self.keys = {}            # value-map key -> id
        self.sources = []         # resolved work Run folders this Task reads

    def load_values(self):
        if not self.current:
            return
        self.values, self.keys = self.values_of(self.current)

    def run_named(self, name: str):
        return next((r for r in runs_of(self.task) if r.name == name or r.name.startswith(name + "_")), None)

    def values_of(self, run: Path) -> tuple:
        """({id: {value, text, flag}}, {value-map key: id}) of one of this Task's Runs."""
        values, keys = {}, {}
        res = run / "result"
        if self.shape == "value map":
            doc = read_yaml(res / "values.yaml") or {}
            for k, v in (doc.get("values") or {}).items():
                if isinstance(v, dict) and v.get("id"):
                    keys[k] = v["id"]
                    values[v["id"]] = {"value": v.get("value"), "text": v.get("shown", ""), "flag": v.get("flag")}
        else:
            f = res / "values.json"
            try:
                doc = json.loads(f.read_text(encoding="utf-8")) if f.is_file() else {}
            except json.JSONDecodeError:
                doc = {}
            for i, v in (doc.items() if isinstance(doc, dict) else []):
                if isinstance(v, dict):
                    values[i] = {"value": v.get("value"), "text": v.get("text", ""), "flag": v.get("flag")}
        return values, keys


def tree_same(a: Path, b: Path) -> bool:
    """A file, or every file under a folder, byte-identical in two places."""
    if a.is_file() or b.is_file():
        return a.is_file() and b.is_file() and filecmp.cmp(a, b, shallow=False)
    if not (a.is_dir() and b.is_dir()):
        return False
    fa = sorted(x.relative_to(a) for x in a.rglob("*") if x.is_file())
    fb = sorted(x.relative_to(b) for x in b.rglob("*") if x.is_file())
    return fa == fb and all(filecmp.cmp(a / x, b / x, shallow=False) for x in fa)


def moved(vt: ValueTask, run: str, subs=(), ids=()) -> list:
    """What a reader of an older value Run read that changed or left in the current one (rule 6, JL 261111: "yes,
    please change them"): each read path under result/ must be byte-identical, each quoted id hold the same value. A
    newer Run that only adds ids leaves its readers current. Nothing to compare (no path, no id) counts as moved."""
    old = vt.run_named(run)
    if old is None:
        return [f"{run} is not on disk"]
    if not (subs or ids):
        return ["it names no file or id to compare"]
    out = []
    for sub in subs:
        if not tree_same(old / "result" / sub, vt.current / "result" / sub):
            out.append(f"{sub} changed")
    then, _ = vt.values_of(old)
    for i in ids:
        if i not in vt.values:
            out.append(f"{i} left")
        elif i in then and not same(then[i]["value"], vt.values[i]["value"]):
            out.append(f"{i} moved")
    return out


def is_current(vt: ValueTask, run: str) -> bool:
    """A reader's Run name (`r01` or `r01_read_values`) is the value Task's current Run."""
    return bool(vt.current) and (vt.current.name == run or vt.current.name.startswith(run + "_"))


# ── resolving a work Run ─────────────────────────────────────────────────────────────────────────────────────────────
def from_source_txt(f: Path, project: Path, root: Path):
    """The work Run folder a SOURCE.txt ("copied from <path>/result") names."""
    if not f.is_file():
        return None
    m = re.search(r"copied from\s+(\S+)", f.read_text(encoding="utf-8"))
    if not m:
        return None
    p = m.group(1).rstrip("/")
    p = p[: -len("/result")] if p.endswith("/result") else p
    cands = [root / p]
    w = re.search(r"(?:^|/)(work/.+)$", p)
    if w:
        cands.append(project / w.group(1))
    return next((c for c in cands if c.is_dir()), cands[-1])


def resolve_source(s: dict, vt: ValueTask, project: Path, root: Path):
    run = str(s.get("run", "")).strip("/")
    if s.get("block"):
        return project / "work" / s["block"] / run
    hit = from_source_txt(vt.current / "result" / str(s.get("key")) / "SOURCE.txt", project, root) if vt.current else None
    if hit is not None and hit.as_posix().endswith(run):
        return hit
    card = read_yaml(vt.current / "run.yaml") if vt.current else None
    for r in (card or {}).get("reads") or [] if isinstance(card, dict) else []:
        r = str(r).split(" (")[0].strip().strip("/")
        if r.endswith(run) and (project / "work" / r).is_dir():
            return project / "work" / r
    found = [b / run for b in sorted((project / "work").glob("b*")) if (b / run).is_dir()]
    return found[0] if len(found) == 1 else None


# ── re-reading one value from its work Run's file (the copying shape) ────────────────────────────────────────────────
def cell_match(cell, want) -> bool:
    c, w = str(cell).strip(), str(want).strip()
    if c == w:
        return True
    a, b = num(c), num(w)
    return isinstance(a, float) and isinstance(b, float) and a == b


def reread(v: dict, f: Path):
    if f.suffix == ".json":
        x = json.loads(f.read_text(encoding="utf-8"))
        for k in str(v["key"]).split("."):
            x = x[int(k)] if isinstance(x, list) else x[k]
        return float(x) if isinstance(x, (int, float)) and not isinstance(x, bool) else x
    with f.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    where = v.get("where") or {}
    hits = [r for r in rows if all(cell_match(r.get(k, ""), w) for k, w in where.items())]
    if len(hits) > 1:
        hits = [r for r in hits if all(str(r.get(k, "")).strip() == str(w) for k, w in where.items())]
    if len(hits) != 1:
        raise ValueError(f"{len(hits)} rows match {where} in {f.name}; need exactly 1")
    return float(str(hits[0][v["column"]]).replace(",", ""))


# ════════════════════════════════════════════ checks ═════════════════════════════════════════════════════════════════
def check_source_runs(rep: Report, vt: ValueTask, reads_all: set):
    """A work Run read is complete; a newer completed Run in its Task makes the value Task stale (rule 6)."""
    for src in vt.sources:
        if not src.is_dir():
            rep.fail(1, vt.task, f"reads work Run {rep.where(src)}, not on disk")
            continue
        if not complete(src):
            rep.fail(1, vt.task, f"reads work Run {rep.where(src)}, not complete (status {status(src) or 'none'})")
        # stale only past the newest Run the value Job reads in this Task: a Run older than one already read was passed
        # over on purpose (a pilot, an earlier copy; Paper-ScalingGlucose 261111)
        task_runs = runs_of(src.parent.parent)
        newest = max([rnum(r.name) for r in task_runs if r.resolve() in reads_all] + [rnum(src.name)])
        newer = [r for r in task_runs if rnum(r.name) > newest and complete(r)]
        if newer:
            rep.fail(6, vt.task, f"stale: reads {src.name} of {rep.where(src.parent.parent)}; "
                                 f"a newer completed Run is there: {', '.join(r.name for r in newer)}")


def check_copies(rep: Report, run: Path, key: str, files: list, src: Path):
    """(a) every copied file is byte-identical to its work Run's file."""
    for fn in files:
        copy, orig = run / "result" / key / fn, src / "result" / fn
        if not copy.is_file():
            rep.fail(1, run, f"{key}/{fn}: the copy is missing")
        elif not orig.is_file():
            rep.fail(1, run, f"{key}/{fn}: its work Run's file is gone ({rep.where(orig)})")
        elif not filecmp.cmp(copy, orig, shallow=False):
            rep.fail(1, run, f"{key}/{fn}: the copy differs from its work Run's file ({rep.where(orig)})")
        rep.seen["copied files"] += 1


def check_copying(rep: Report, vt: ValueTask, project: Path, root: Path):
    srcof = {}
    for s in vt.cfg.get("sources") or []:
        src = resolve_source(s, vt, project, root)
        if src is None:
            rep.fail(1, vt.task, f"source {s.get('key')}: work Run {s.get('run')} not found under work/")
            continue
        srcof[s.get("key")] = src
        vt.sources.append(src)
        if vt.current:
            check_copies(rep, vt.current, str(s.get("key")), list(s.get("files") or []), src)
    if not vt.current:
        return
    for v in vt.cfg.get("values") or []:
        i = v.get("id")
        if v.get("flag") and not (vt.values.get(i) or {}).get("flag"):
            rep.fail(5, vt.task, f"{i}: marked to check before quoting: {short(v['flag'])}")
        if i not in vt.values:
            rep.fail(1, vt.current, f"{i}: in scripts/values.yaml, not in the Run's values.json")
            continue
        key, _, rest = str(v.get("from", "")).partition("/")
        if key not in srcof:
            continue
        if v.get("transform") not in TRANSFORM:
            rep.note(f"not re-read: {vt.name} {i} (transform {v.get('transform')} unknown to this check)")
            continue
        try:
            x = TRANSFORM[v.get("transform")](reread(v, srcof[key] / "result" / rest)) if v.get("transform") else \
                reread(v, srcof[key] / "result" / rest)
            text = v.get("fmt", "{}").format(x)
        except Exception as e:                       # a work file that no longer reads is a failure, not a crash
            rep.fail(1, vt.current, f"{i}: cannot re-read from {key}/{rest}: {short(e, 70)}")
            continue
        got = vt.values[i]
        rep.seen["ids re-read"] += 1
        if not same(x, got["value"]) or str(text) != str(got["text"]):
            rep.fail(1, vt.current, f"{i}: the work Run's file gives {text} ({x:g}), the value Run says {got['text']} "
                                    f"({got['value']})" if isinstance(x, float) else
                     f"{i}: the work Run's file gives {text}, the value Run says {got['text']}")


def check_value_map(rep: Report, vt: ValueTask, project: Path):
    for name, path in (vt.cfg.get("runs") or {}).items():
        vt.sources.append(project / str(path).strip("/"))
    for key, spec in (vt.cfg.get("values") or {}).items():
        if isinstance(spec, dict) and spec.get("flag") and not (vt.values.get(vt.keys.get(key)) or {}).get("flag"):
            rep.fail(5, vt.task, f"{spec.get('id') or key}: marked to check before quoting: {short(spec['flag'])}")
    if not vt.current:
        return
    try:
        import values_ledger as vl
        _, rows = vl.catalog(vt.task)
    except (Exception, SystemExit) as e:
        rep.fail(1, vt.task, f"its value map does not re-read from the work Runs: {short(e, 90)}")
        return
    for key, row in rows.items():
        i = vt.keys.get(key)
        if i is None:
            rep.fail(1, vt.current, f"{key}: in the value map, not in the Run's values.yaml (rerun the ticket)")
            continue
        if row["id"] != i:
            rep.fail(2, vt.current, f"{key}: the map now gives id {row['id']}, the Run recorded {i}")
        if row.get("value") is None:
            continue
        got = vt.values[i]["value"]
        rep.seen["ids re-read"] += 1
        if not same(row["value"], got):
            rep.fail(1, vt.current, f"{i}: the work Run gives {row['value']}, the value Run says {got}")


def check_other(rep: Report, vt: ValueTask, project: Path, root: Path):
    """(a) on the newest Run that holds result/<dir>/SOURCE.txt copies."""
    holder = next((r for r in reversed(runs_of(vt.task)) if list((r / "result").glob("*/SOURCE.txt"))), None)
    if holder is None:
        return
    if not complete(holder):
        rep.fail(1, holder, f"its copies' Run is not complete (status {status(holder) or 'none'})")
    for st in sorted((holder / "result").glob("*/SOURCE.txt")):
        src = from_source_txt(st, project, root)
        if src is None:
            rep.fail(1, st, "SOURCE.txt says no `copied from <path>`")
            continue
        vt.sources.append(src)
        files = sorted(p.name for p in st.parent.iterdir() if p.is_file() and p.name != "SOURCE.txt")
        check_copies(rep, holder, st.parent.name, files, src)


def check_displays(rep: Report, board: Path, j02: Path, vts: dict, ids: dict):
    job = display_job(board)
    if job is None:
        rep.note("no display Job: displays not checked")
        return
    j02name = j02.name if j02 else "j02_evidence_value"
    ref = re.compile(rf"{re.escape(j02name)}/(t\d+[^/\s]*)/runs/(r\d+[^/\s`'\")]*)")
    for task in pt.tasks(job):
        runs = runs_of(task)
        if not runs:
            continue
        face = face_text(task)
        name = re.sub(r"^runs/", "", field(face, "printed").split()[0]) if field(face, "printed") else ""
        if not name:
            m = re.match(r"(?:runs/)?(r\d+\S*)", field(face, "made-by"))
            name = m.group(1).rstrip("/") if m else ""
        run = next((r for r in runs if r.name == name or r.name.startswith(name + "_")), None) if name else runs[-1]
        if run is None:
            rep.fail(3, task, f"its face names {name} as printed, not on disk")
            continue
        rep.seen["display Runs"] += 1
        card = read_yaml(run / "run.yaml")
        card = card if isinstance(card, dict) else {}
        disp = read_yaml(run / "result" / "display.yaml")
        disp = disp if isinstance(disp, dict) else {}
        reads = [str(r).split(" (")[0].strip() for r in (card.get("reads") or [])]
        for r in reads:
            if re.search(r"(?:^|/)work/", r):
                rep.fail(1, run, f"reads work/ directly ({short(r, 80)}); a display reads the value Job's copies only")
        named = {}
        for r in reads:
            m = ref.search(r)
            if m:
                named.setdefault(m.group(1), m.group(2))
        used = run / "result" / "values_used.csv"
        rows = []
        if used.is_file():
            with used.open(newline="", encoding="utf-8") as fh:
                rows = list(csv.DictReader(fh))
        if disp.get("value_run"):
            for t in {r.get("value_task") for r in rows if r.get("value_task")}:
                named.setdefault(t, str(disp["value_run"]))
        if not named:
            if not card and not disp:
                rep.fail(3, run, "no run.yaml: names no value Run")
            else:
                rep.fail(3, run, "names no value Run (no reads path into the value Job, no value_run)")
        subs = {}
        for r in reads:                                 # the paths under result/ it read, per value Task
            m = re.search(rf"{re.escape(j02name)}/(t\d+[^/\s]*)/runs/r\d+[^/\s]*/result/(\S+)", r)
            if m:
                subs.setdefault(m.group(1), []).append(m.group(2).rstrip("/"))
        for t, r in sorted(named.items()):
            vt = vts.get(t)
            if vt is None:
                rep.fail(3, run, f"reads value Task {t}, not on disk")
            elif not is_current(vt, r):
                mine = [x.get("id", "").strip() for x in rows if x.get("id") and (x.get("value_task") in (None, "", t))]
                why = moved(vt, r, subs.get(t, []), mine)
                if why:
                    rep.fail(6, run, f"stale: reads {t}/{r}, and in {vt.current.name if vt.current else 'none'} "
                                     f"{'; '.join(why[:3])}{' …' if len(why) > 3 else ''}")
        if not rows:
            continue
        col = "value" if "value" in rows[0] else "text" if "text" in rows[0] else "shown" if "shown" in rows[0] else None
        for row in rows:
            i = (row.get("id") or "").strip()
            if not i:
                continue
            vt = vts.get(row.get("value_task") or "") or next((vts[t] for t in ids.get(i, []) if t in vts), None)
            cur = vt.values.get(i) if vt else None
            rep.seen["display ids"] += 1
            if cur is None:
                rep.fail(2, used, f"{i}: not an id of the current value Run{f' of {vt.name}' if vt else ''}")
            elif col == "value" and not same(row["value"], cur["value"]):
                rep.fail(2, used, f"{i}: prints {row['value']}, the current value is {cur['value']}")
            elif col in ("text", "shown") and str(row[col]).strip() != str(cur["text"]).strip():
                rep.fail(2, used, f"{i}: prints {row[col]}, the current value is {cur['text']}")


def writing_jobs(board: Path, j02):
    out = []
    try:
        import values_ledger as vl
        p = vl.paper_of(j02) if j02 else None
        if p and p.job:
            out.append(p.job)
    except (Exception, SystemExit):
        pass
    newest = pt.writing_job(board)
    if newest and newest not in out:
        out.append(newest)
    return out


def check_sections(rep: Report, board: Path, j02, vts: dict):
    if j02 is None:
        return
    by_tnn = {vt.tnn: vt for vt in vts.values()}
    try:                                                # (e) VALUE card bindings, as values_ledger reads them
        import values_ledger as vl
        paper = vl.paper_of(j02)
        for b in paper.binds:
            it, h = b["item"], b["holder"]
            vt = by_tnn.get(b["task"])
            rep.seen["Section bindings"] += 1
            label = it.get("value") or it.get("key") or "a binding"
            if vt is None:
                rep.fail(2, h, f"{label}: bound to {j02.name}.{b['task']}, no such value Task")
                continue
            if not it.get("run"):
                rep.fail(3, h, f"{label}: the binding names no value Run")
            elif not is_current(vt, str(it["run"])):
                quoted = [it["value"]] if it.get("value") else []
                why = moved(vt, str(it["run"]), (), quoted)
                if why:
                    rep.fail(6, h, f"stale: {label} reads {vt.name}/{it['run']}, and in "
                                   f"{vt.current.name if vt.current else 'none'} {'; '.join(why)}")
            if vt.shape == "value map":
                try:
                    _, values = vl.catalog(vt.task)
                except (Exception, SystemExit):
                    continue
                for r in vl.check_binding(b, values, paper.texts, paper.disp_rows):
                    if r["status"] == "differs":
                        rep.fail(2, h, f"{r['id'] or label} at {r['where']}: prints {r['printed']}, the value is {r['value']}")
                    elif r["status"] == "stale":
                        rep.fail(2, h, f"{label} at {r['where']}: {r['note']}")
    except (Exception, SystemExit) as e:
        rep.note(f"VALUE card bindings not read ({type(e).__name__}: {short(e, 60)})")
    ref = re.compile(rf"{re.escape(j02.name)}/(t\d+[^/\s]*)/runs/(r\d+[^/\s`'\")\]]*)")
    for job in writing_jobs(board, j02):              # (e) every value Run path the writing Job's text names
        for f in sorted(job.rglob("*")):
            rel = f.relative_to(job).parts
            if not f.is_file() or f.suffix not in TEXT_SUFFIXES or "runs" in rel or "superseded" in f.name \
                    or any(p.startswith(("_", ".")) for p in rel):
                continue
            seen = set()
            text = f.read_text(encoding="utf-8", errors="replace")
            for m in ref.finditer(text):
                t, r = m.group(1), m.group(2).rstrip(".,;:")
                if (t, r) in seen:
                    continue
                seen.add((t, r))
                rep.seen["Section references"] += 1
                vt = vts.get(t)
                if vt is None:
                    rep.fail(3, f, f"names {t}/{r}, no such value Task")
                elif not is_current(vt, r):
                    old = vt.run_named(r)
                    then = vt.values_of(old)[0] if old else {}
                    quoted = [i for i in then if re.search(rf"(?<![\w-]){re.escape(i)}(?![\w-])", text)]
                    why = moved(vt, r, (), quoted)
                    if why:
                        rep.fail(6, f, f"stale: names {t}/{r}, and in {vt.current.name if vt.current else 'none'} "
                                       f"{'; '.join(why[:3])}{' …' if len(why) > 3 else ''}")


def check_recompute(rep: Report, board: Path, j02, project: Path):
    hooks = []
    for folder in [board] + ([j02] if j02 else []):
        s = folder / "scripts" / "recompute_check.py"
        if s.is_file():
            hooks.append(s)
        said = field(face_text(folder) if folder != board else (board / "board.md").read_text(encoding="utf-8")
                     if (board / "board.md").is_file() else "", "recompute")
        if said:
            p = (folder / said.split()[0]).resolve()
            if not p.is_file():
                rep.fail(7, folder / f"{folder.name}.md" if folder != board else board / "board.md",
                         f"recompute: {said.split()[0]} is not on disk")
            elif p not in hooks:
                hooks.append(p)
    if not hooks:
        rep.note("rule 7: no recompute hook (scripts/recompute_check.py, or a face line `recompute: <path>`)")
    for h in hooks:
        rep.seen["recompute hooks"] += 1
        try:
            p = subprocess.run([sys.executable, str(h), str(board)], cwd=project, capture_output=True, text=True, timeout=3600)
            out, rc = (p.stdout + p.stderr).rstrip(), p.returncode
        except subprocess.TimeoutExpired:
            out, rc = "timed out after an hour", -1
        for line in out.splitlines():
            rep.note(f"  | {line}")
        if rc != 0:
            rep.fail(7, h, f"the recompute check exited {rc}")


# ════════════════════════════════════════════ the whole chain ════════════════════════════════════════════════════════
def chain(board: Path, root=None, recompute: bool = True) -> Report:
    """The whole chain read once; `recompute=False` skips the rule-7 hook (paper_check.py's quick row)."""
    board = Path(board).resolve()
    project = next((p for p in [board, *board.parents] if (p / "work").is_dir()), None)
    if project is None:
        raise SystemExit(f"{board}: no folder above it holds work/ (not inside a Project)")
    root = Path(root).resolve() if root else pt.server_root(board)
    rep = Report(board, project)
    j02 = value_job(board)
    vts = {}
    if j02 is None:
        rep.note("no value Job (jNN_evidence_value): values not checked")
    else:
        pin = pinned_run(j02)
        for t in pt.tasks(j02):
            if t.name == CHECK_TASK:
                continue
            vt = ValueTask(t, pin)
            vts[t.name] = vt
            if not runs_of(t):
                continue
            if vt.current is None:
                rep.fail(1, t, "no completed value Run")
            elif not complete(vt.current):
                rep.fail(1, vt.current, f"the current value Run is not complete (status {status(vt.current) or 'none'})")
            vt.load_values()
            rep.seen[f"{vt.shape} value Tasks"] += 1
        for vt in vts.values():
            if vt.shape == "copying":
                check_copying(rep, vt, project, root)
            elif vt.shape == "value map":
                check_value_map(rep, vt, project)
            else:
                check_other(rep, vt, project, root)
            for i, v in vt.values.items():
                if v.get("flag"):
                    rep.fail(5, vt.current, f"{i}: marked to check before quoting: {short(v['flag'])}")
        reads_all = {s.resolve() for vt in vts.values() for s in vt.sources if s.is_dir()}
        for vt in vts.values():
            check_source_runs(rep, vt, reads_all)
    ids = {}
    for vt in vts.values():
        for i in vt.values:
            ids.setdefault(i, []).append(vt.name)
    for i, ts in sorted(ids.items()):
        if len(ts) > 1:
            rep.fail(2, j02, f"{i} is in two value Tasks: {', '.join(ts)}")
    rep.seen["value ids"] = len(ids)
    check_displays(rep, board, j02, vts, ids)
    check_sections(rep, board, j02, vts)
    if recompute:
        check_recompute(rep, board, j02, project)
    return rep


def summary(rep: Report) -> str:
    by = Counter(f["rule"] for f in rep.fails)
    seen = ", ".join(f"{n} {k}" for k, n in rep.seen.items())
    if not rep.fails:
        return f"chain_check {rep.board.name}: the chain holds; checked {seen}"
    rules = ", ".join(f"rule {r}: {by[r]}" for r in sorted(by))
    return f"chain_check {rep.board.name}: {len(rep.fails)} failure{'s' * (len(rep.fails) != 1)} ({rules}); checked {seen}"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("board", type=Path, help="the paper Board folder")
    ap.add_argument("--root", type=Path, help="the SPACE root SOURCE.txt paths are relative to")
    ap.add_argument("--json", action="store_true", help="print one JSON document instead of lines")
    a = ap.parse_args(argv)
    rep = chain(a.board, a.root)
    if a.json:
        print(json.dumps({"board": rep.board.name, "failures": rep.fails, "notes": rep.notes,
                          "checked": dict(rep.seen), "summary": summary(rep)}, indent=2, ensure_ascii=False))
    else:
        for f in rep.fails:
            print(f"FAIL {f['rule']} {f['where']}: {f['what']}")
        for n in rep.notes:
            print(n)
        print(summary(rep))
    return 1 if rep.fails else 0


if __name__ == "__main__":
    sys.exit(main())
