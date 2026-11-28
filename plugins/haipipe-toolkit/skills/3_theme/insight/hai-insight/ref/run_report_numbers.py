"""run_report_numbers · the numbers of a Run's report against its result files (ref/run-report.md; T31, T32).

A number a sentence gives is either in a file the sentence cites (as written, rounded to the sentence's decimals; a
percent may be a share) or derived: the sentence names it under `derived:` with the rule that makes it, and the rule is
computed here from the files the sentence cites. A headline gives only numbers its sentences give.

A rule (`how:`):

    count rows [in <file>] [where <cond> [and <cond>]...]
    sum | min | max | mean <column> [in <file>] [where ...]
    <arithmetic over numbers the report gives or the cited files hold>      17 / 29 · (53342 - 360) / 53342
    cond: <column> <op> <number or word>, op one of  >  >=  <  <=  ==  !=

`in <file>` is needed only when the sentence cites more than one table. A rule this cannot read stays for the checker
to confirm by hand (`--accept`); a rule it reads and that gives another number stops the report.
"""
from __future__ import annotations

import ast
import bisect
import csv
import re
from pathlib import Path

SENT = re.compile(r"(?<![\w.])([-−])?(\d{1,3}(?:,\d{3})+|\d+)(\.\d+)?(\s?%)?(?![\w])")
FILENUM = re.compile(r"[-−]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?")
AGG = re.compile(r"^(?:(count) rows|(sum|min|max|mean) (\S+))(?: in (\S+))?(?: where (.+))?$")
COND = re.compile(r"^(\S+)\s*(>=|<=|==|!=|>|<)\s*(.+)$")


class Unreadable(Exception):
    """A rule this module cannot compute: the checker confirms it by hand."""


def sentence_numbers(text: str) -> list[tuple[str, float, int, bool]]:
    """[(as written, value, decimals, percent)]; a number inside a name (D05, r01_full, 7d) is not one."""
    out = []
    for m in SENT.finditer(str(text).replace("`", " ")):
        sign, whole, frac, pct = m.groups()
        value = float(whole.replace(",", "") + (frac or "")) * (-1 if sign else 1)
        out.append((m.group(0).strip(), value, len(frac) - 1 if frac else 0, bool(pct)))
    return out


def written(value) -> tuple[str, float, int, bool] | None:
    """One number as a spec gives it (17, "23,535", "20.8%")."""
    got = sentence_numbers(str(value))
    return got[0] if len(got) == 1 else None


def file_numbers(path: Path) -> list[float]:
    text = path.read_text(encoding="utf-8", errors="replace").replace("−", "-") if path.is_file() else ""
    return sorted(float(x) for x in FILENUM.findall(text))


def traced(value: float, decimals: int, percent: bool, nums: list[float]) -> bool:
    """The value is among nums as written, rounded to its decimals, or (a percent) as a share."""
    tol = 0.5 * 10 ** -decimals + 1e-9
    for v, t in ((value, tol), (value / 100, tol / 100)) if percent else ((value, tol),):
        i = bisect.bisect_left(nums, v - t)
        if i < len(nums) and nums[i] <= v + t:
            return True
    return False


def same(w: tuple, got: float) -> bool:
    _, value, decimals, percent = w
    return traced(value, decimals, percent, [got])


# ── a rule ──────────────────────────────────────────────────────────────────────────────────────
def _rows(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _num(x):
    try:
        return float(str(x).replace(",", ""))
    except ValueError:
        return None


def _keep(row: dict, cond: str) -> bool:
    m = COND.match(cond.strip())
    if not m or m.group(1) not in row:
        raise Unreadable(f"the condition {cond.strip()!r} names no column of the table")
    col, op, want = m.group(1), m.group(2), m.group(3).strip().strip("'\"")
    a, b = _num(row[col]), _num(want)
    if a is None or b is None:
        a, b = str(row[col]).strip(), want
        if op not in ("==", "!="):
            raise Unreadable(f"{col} {op} {want}: a word compares only with == or !=")
    return {">": a > b if isinstance(a, float) else False, ">=": a >= b if isinstance(a, float) else False,
            "<": a < b if isinstance(a, float) else False, "<=": a <= b if isinstance(a, float) else False,
            "==": a == b, "!=": a != b}[op]


def _aggregate(m: re.Match, files: dict) -> float:
    count, fn, col, name, where = m.groups()
    tables = {k: p for k, p in files.items() if p.suffix == ".csv"}
    if name:
        if name not in tables:
            raise Unreadable(f"{name} is not a table this sentence cites")
        path = tables[name]
    elif len(tables) == 1:
        path = next(iter(tables.values()))
    else:
        raise Unreadable("the sentence cites more than one table: name it, `in <file>`")
    rows = [r for r in _rows(path) if all(_keep(r, c) for c in (where.split(" and ") if where else []))]
    if count:
        return float(len(rows))
    if rows and col not in rows[0]:
        raise Unreadable(f"{col} is not a column of {path.name}")
    vals = [v for v in (_num(r[col]) for r in rows) if v is not None]
    if not vals:
        raise Unreadable(f"no number in {col} for the rows the rule keeps")
    return {"sum": sum(vals), "min": min(vals), "max": max(vals), "mean": sum(vals) / len(vals)}[fn]


def _arith(how: str, known: list[float], nums: list[float]) -> float:
    try:
        tree = ast.parse(how.replace(",", "").replace("−", "-"), mode="eval")
    except SyntaxError as e:
        raise Unreadable(f"not a rule this tool reads: {how}") from e
    ops = {ast.Add: lambda a, b: a + b, ast.Sub: lambda a, b: a - b, ast.Mult: lambda a, b: a * b,
           ast.Div: lambda a, b: a / b}

    def ev(n):
        if isinstance(n, ast.Expression):
            return ev(n.body)
        if isinstance(n, ast.BinOp) and type(n.op) in ops:
            return ops[type(n.op)](ev(n.left), ev(n.right))
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub):
            return -ev(n.operand)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            v = float(n.value)
            if not (traced(v, 0 if v == int(v) else 6, False, known) or traced(v, 0 if v == int(v) else 6, False, nums)):
                raise ValueError(f"{n.value} in `{how}` is neither a number of the report nor in the files it cites")
            return v
        raise Unreadable(f"not a rule this tool reads: {how}")
    return ev(tree)


def evaluate(how: str, files: dict, known: list[float]) -> float:
    """The number a rule gives; Unreadable when this module cannot compute it, ValueError when it names a number the
    report and its files do not hold."""
    how = " ".join(str(how).split())
    m = AGG.match(how)
    if m:
        return _aggregate(m, files)
    nums = sorted(x for p in files.values() for x in file_numbers(p))
    try:
        return _arith(how, sorted(known), nums)
    except ZeroDivisionError as e:
        raise Unreadable(f"`{how}` divides by zero") from e


# ── a report's numbers ─────────────────────────────────────────────────────────────────────────
def cited(s: dict) -> list[str]:
    return list(s.get("files") or ([s["file"]] if s.get("file") else []))


def problems(result: Path, rep: dict) -> tuple[list[str], list[str], list[str]]:
    """(untraced, wrong, by hand) for a report's front: each 'where: number' a sentence or the headline gives that no
    cited file holds; each derived number its rule computes to another value; each derived number whose rule this
    module cannot read."""
    sents = rep.get("sentences") or []
    known = [v for s in sents for _, v, _, _ in sentence_numbers(s.get("text", ""))]
    untr, wrong, hand = [], [], []
    for k, s in enumerate(sents, 1):
        files = {f: result / f for f in cited(s)}
        nums = sorted(x for p in files.values() for x in file_numbers(p))
        derived = []                                      # a derived number is checked by its rule, not looked up
        for d in s.get("derived") or []:
            w = written(d.get("value"))
            derived += [w[1]] if w else []
            try:
                got = evaluate(d.get("how", ""), files, known)
            except Unreadable as e:
                hand.append(f"sentence {k}: {d.get('value')} ({d.get('how')}: {e})")
                continue
            except ValueError as e:
                wrong.append(f"sentence {k}: {d.get('value')}: {e}")
                continue
            if not (w and same(w, got)):
                wrong.append(f"sentence {k}: {d.get('value')}: `{d.get('how')}` gives {got:g}")
        for w, v, dec, pct in sentence_numbers(s.get("text", "")):
            if not any(abs(v - x) < 1e-9 for x in derived) and not traced(v, dec, pct, nums):
                untr.append(f"{', '.join(files)}: {w}")
    pool = sorted(known)
    untr += [f"headline: {w}" for w, v, dec, pct in sentence_numbers(rep.get("headline", ""))
             if not traced(v, dec, pct, pool)]
    return untr, wrong, hand
