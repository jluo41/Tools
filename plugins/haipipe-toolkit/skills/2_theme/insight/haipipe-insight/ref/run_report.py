"""run_report.py · a Run's report: what one hard Run's result shows, in a few sentences (ref/run-report.md).

An agent reads only the Run's `result/` and writes a spec; this tool lays the report out at
`runs/rNN_<segment>/report.md`, beside `result/` (the ticket's, cleared on every rerun), so a rerun keeps it. The
report pins the result's hash: a rerun that changes the result makes it stale. Another agent checks it; every number
a sentence gives must be in the table that sentence cites, or be confirmed by that agent by hand.

    run_report.py todo  <Job | Task | Run>                 the Runs whose report is missing, stale, returned or unchecked
    run_report.py write <Run> <spec.yaml> --by <agent>     lay the report out from the writer's spec
    run_report.py check <Run> --by <agent> [--accept 9,22] [--reject "why"]
    run_report.py carry <Job | Task>                       carry a checked report from an earlier Job's Run whose
                                                           result is the same (same question, segment and hash)

The spec:

    headline: <one line: what this segment's result shows>
    sentences:                                   # a few; each cites the result file its numbers come from
      - {text: "<sentence>", file: grouping_audit.csv}
    caveat: <one line: thin, refused, not checkable>   # optional

Exit 0 when done, 1 when refused (the reason is printed).
"""
from __future__ import annotations

import argparse
import bisect
import datetime
import hashlib
import re
import sys
from pathlib import Path

import yaml

RUN = re.compile(r"^r(\d{2})_(.+)$")
JOBDIR = re.compile(r"^j\d+_")
TASKDIR = re.compile(r"^t\d+_")
READABLE = ("ok", "refused", "done")              # a failed Run has nothing to read: fix and rerun its ticket
SPEC_KEYS = {"headline", "sentences", "caveat"}
SENT = re.compile(r"(?<![\w.])([-−])?(\d{1,3}(?:,\d{3})+|\d+)(\.\d+)?(\s?%)?(?![\w])")
FILENUM = re.compile(r"[-−]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?")


class Refused(Exception):
    pass


def _yaml(path: Path) -> dict:
    return (yaml.safe_load(path.read_text(encoding="utf-8")) or {}) if path.is_file() else {}


def front(md: Path) -> dict:
    text = md.read_text(encoding="utf-8") if md.is_file() else ""
    m = re.match(r"(?s)^---\n(.*?)\n---\n", text)
    return (yaml.safe_load(m.group(1)) or {}) if m else {}


def today() -> str:
    return datetime.date.today().strftime("%y%m%d")


# ── a Run and its result ────────────────────────────────────────────────────────────────────────
def receipt(run: Path) -> dict:
    return _yaml(run / "result" / "runtime.yaml")


def result_hash(run: Path) -> str:
    """The result's content: the receipt's tables_sha256 (a question Run's tables), else one digest over its status,
    its reason and every csv and json it wrote (a refused Run, a prep Run)."""
    rec = receipt(run)
    if rec.get("tables_sha256"):
        return str(rec["tables_sha256"])
    h = hashlib.sha256(f"{rec.get('status')}\n{rec.get('reason') or ''}\n".encode())
    res = run / "result"
    for f in sorted(res.rglob("*")) if res.is_dir() else []:
        if f.is_file() and f.suffix in (".csv", ".json") and "provenance" not in f.relative_to(res).parts:
            h.update(f.relative_to(res).as_posix().encode() + b"\n" + f.read_bytes())
    return h.hexdigest()


def identity(run: Path) -> tuple[str, str]:
    """(what the Run answers, its segment): a question Run's (D05, full); a prep Run's (prep-v1, smsr2)."""
    card = _yaml(run / "run.yaml")
    return str(card.get("question") or card.get("prep") or ""), str(card.get("partition") or RUN.match(run.name).group(2))


def state(run: Path) -> str:
    """missing · stale · returned · unchecked · checked, or '' for a Run with nothing to read."""
    if receipt(run).get("status") not in READABLE:
        return ""
    rep = front(run / "report.md")
    if not rep:
        return "missing"
    if str(rep.get("result-sha256")) != result_hash(run):
        return "stale"
    check = str(rep.get("check") or "")
    return "checked" if check.startswith("✅") else "returned" if check.startswith("❗") else "unchecked"


def runs_under(folder: Path) -> list[Path]:
    """The hard Runs under a Job, a Task or a Run, in folder order."""
    folder = Path(folder).resolve()
    if RUN.match(folder.name) and folder.parent.name == "runs":
        return [folder]
    tasks = [folder] if TASKDIR.match(folder.name) else sorted(       # a Job holds runs/ of its own: read its Tasks
        p for p in folder.iterdir() if p.is_dir() and TASKDIR.match(p.name))
    return [r for t in tasks for r in sorted((t / "runs").glob("r[0-9][0-9]_*"))
            if r.is_dir() and (r / "run.yaml").is_file()]


# ── numbers: a sentence's against its file's ──────────────────────────────────────────────────
def sentence_numbers(text: str) -> list[tuple[str, float, int, bool]]:
    """[(as written, value, decimals, percent)]; a number inside a name (D05, r01_full, 7d) is not one."""
    out = []
    for m in SENT.finditer(text.replace("`", " ")):
        sign, whole, frac, pct = m.groups()
        value = float(whole.replace(",", "") + (frac or "")) * (-1 if sign else 1)
        out.append((m.group(0).strip(), value, len(frac) - 1 if frac else 0, bool(pct)))
    return out


def file_numbers(path: Path) -> list[float]:
    text = path.read_text(encoding="utf-8", errors="replace").replace("−", "-")
    return sorted(float(x) for x in FILENUM.findall(text))


def traced(value: float, decimals: int, percent: bool, nums: list[float]) -> bool:
    """The value is in the file as written, rounded to the sentence's decimals, or (a percent) as a share."""
    tol = 0.5 * 10 ** -decimals + 1e-9
    for v in (value, value / 100) if percent else (value,):
        t = tol if v == value else tol / 100
        i = bisect.bisect_left(nums, v - t)
        if i < len(nums) and nums[i] <= v + t:
            return True
    return False


def untraced(run: Path, sentences: list) -> list[str]:
    """Each number a sentence gives that its cited file does not hold: 'file: number'."""
    out, cache = [], {}
    for s in sentences:
        f = run / "result" / s["file"]
        nums = cache.setdefault(f, file_numbers(f) if f.is_file() else [])
        out += [f"{s['file']}: {w}" for w, v, d, p in sentence_numbers(s["text"]) if not traced(v, d, p, nums)]
    return out


# ── write · check · carry ─────────────────────────────────────────────────────────────────────
def render(run: Path, fields: dict) -> str:
    """The report: its front (what check and the pages read) and the same, laid out to read."""
    rec = receipt(run)
    what, seg = fields["question"], fields["segment"]
    lines = [f"# {what} · {seg}", "", fields["headline"], ""]
    if rec.get("status") == "refused":
        lines += [f"**Refused**: {rec.get('reason') or ''}", ""]
    lines += [f"- {s['text'].strip().rstrip('.')} (`{s['file']}`)." for s in fields["sentences"]]
    if fields.get("caveat"):
        lines += ["", f"**Caveat**: {fields['caveat']}"]
    if fields.get("carried-from"):
        lines += ["", f"Carried from `{fields['carried-from']}`: the same result."]
    return ("---\n" + yaml.safe_dump(fields, sort_keys=False, allow_unicode=True, width=10_000) + "---\n\n"
            + "\n".join(lines).rstrip() + "\n")


def write(run: Path, spec: dict, by: str) -> Path:
    run = Path(run).resolve()
    status = receipt(run).get("status")
    if status not in READABLE:
        raise Refused(f"{run.name} is {status or 'not run'}: a report reads an ok, refused or done Run; fix and rerun its ticket")
    bad = sorted(set(spec) - SPEC_KEYS)
    if bad:
        raise Refused(f"unknown key(s) {bad}; a spec holds {sorted(SPEC_KEYS)}")
    if not str(spec.get("headline") or "").strip():
        raise Refused("headline: the one line is missing")
    sents = spec.get("sentences") or []
    if not sents:
        raise Refused("sentences: at least one, each citing the result file its numbers come from")
    for k, s in enumerate(sents, 1):
        if not isinstance(s, dict) or set(s) != {"text", "file"}:
            raise Refused(f"sentence {k}: {{text, file}}")
        f = (run / "result" / s["file"]).resolve()
        if not f.is_file() or (run / "result").resolve() not in f.parents:
            raise Refused(f"sentence {k}: {run.name}/result/{s['file']} is not a file of this Run")
    what, seg = identity(run)
    fields = {"run": run.name, "question": what, "segment": seg, "status": status, "result-sha256": result_hash(run),
              "written-by": by, "written": today(), "check": "", "headline": str(spec["headline"]).strip(),
              "sentences": [{"text": str(s["text"]).strip(), "file": s["file"]} for s in sents]}
    if str(spec.get("caveat") or "").strip():
        fields["caveat"] = str(spec["caveat"]).strip()
    (run / "report.md").write_text(render(run, fields), encoding="utf-8")
    return run / "report.md"


def check(run: Path, by: str, accept: tuple = (), reject: str = "") -> str:
    run = Path(run).resolve()
    md = run / "report.md"
    rep = front(md)
    if not rep:
        raise Refused(f"{run.name} has no report: write it first")
    if by == rep.get("written-by"):
        raise Refused(f"{by} wrote this report: another agent checks it")
    st = state(run)
    if st == "stale":
        raise Refused(f"{run.name}'s result changed after its report was written: write it again first")
    if reject:
        rep["check"] = f"❗ {today()} {by}: {reject}"
    else:
        left = [u for u in untraced(run, rep.get("sentences") or []) if u.split(": ", 1)[1] not in accept]
        if left:
            raise Refused("not in the cited file: " + "; ".join(left) + ". Confirm each by hand against the "
                          "tables and pass --accept, or return the report with --reject")
        rep["check"] = f"✅ {today()} {by}"
        if accept:
            rep["accepted"] = list(accept)
    md.write_text(render(run, rep), encoding="utf-8")
    return rep["check"]


def earlier(run: Path) -> Path | None:
    """A checked, current report of the same question on the same segment, in another Job of this Board, whose
    result is this Run's."""
    task, job = run.parent.parent, run.parent.parent.parent
    board, (what, seg), mine = job.parent, identity(run), result_hash(run)
    for other in sorted(p for p in board.iterdir() if p.is_dir() and JOBDIR.match(p.name) and p != job):
        for cand in runs_under(other):
            if identity(cand) == (what, seg) and state(cand) == "checked" and result_hash(cand) == mine:
                return cand
    return None


def carry(folder: Path) -> list[Path]:
    root = _space_root(Path(folder).resolve())
    done = []
    for run in runs_under(folder):
        if state(run) not in ("missing", "stale"):
            continue
        src = earlier(run)
        if src is None:
            continue
        rep = front(src / "report.md")
        rep.update(run=run.name, **{"carried-from": (src / "report.md").relative_to(root).as_posix()})
        (run / "report.md").write_text(render(run, rep), encoding="utf-8")
        done.append(run)
    return done


def _space_root(p: Path) -> Path:
    """The SPACE the Run sits in (the folder holding env.sh), so a path a report prints is SPACE-relative."""
    return next((a for a in (p, *p.parents) if (a / "env.sh").is_file()), p)


def todo(folder: Path) -> list[tuple[str, Path]]:
    return [(st, r) for r in runs_under(folder) for st in [state(r)] if st not in ("", "checked")]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("action", choices=("todo", "write", "check", "carry"))
    ap.add_argument("folder")
    ap.add_argument("spec", nargs="?")
    ap.add_argument("--by", default="")
    ap.add_argument("--accept", default="", help="numbers confirmed by hand, comma-separated as written")
    ap.add_argument("--reject", default="")
    a = ap.parse_args(argv)
    folder = Path(a.folder).resolve()
    try:
        if a.action == "todo":
            for st, r in todo(folder):
                print(f"{st:<10} {r.relative_to(folder) if r != folder else r.name}")
        elif a.action == "carry":
            for r in carry(folder):
                print(f"carried    {r.relative_to(folder)}")
        elif not a.by:
            raise Refused("--by <agent>: who writes or checks it")
        elif a.action == "write":
            if not a.spec:
                raise Refused("write <Run> <spec.yaml> --by <agent>")
            print(write(folder, _yaml(Path(a.spec)), a.by))
        else:
            acc = tuple(x.strip() for x in re.split(r"[;|]|,(?!\d{3})", a.accept) if x.strip())
            print(f"{folder.name}: {check(folder, a.by, acc, a.reject)}")
    except Refused as e:
        print(f"refused: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
