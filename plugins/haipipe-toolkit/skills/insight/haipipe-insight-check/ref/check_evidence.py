#!/usr/bin/env python3
"""check_evidence — does each answered question's work and report fit its ask?

Reads one InsightBoard: the four registers (MT01-MT04: each question's evidence
needs and its Queue cells), and every answering page the cells name (its
answers.yaml, runs/ tickets, results/<ticket>/ and the page text). Returns one
verdict per register cell that names a page (haipipe-insight
ref/evidence-needs.md § 4):

    OK · GAP · STALE · UNBOUND · UNPLANNED

A ✅ cell whose verdict is GAP, STALE or UNBOUND is an overclaim: exit 1.
UNPLANNED fails only under --strict. Read-only: it writes nothing.

    check_evidence.py <board> [--format text|json] [--strict]
                      [--question QK2] [--page K02-full]
"""

import argparse
import csv
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

QID = re.compile(r"\bQ[DIKW]\d+\b")
DIVISION = re.compile(r"^#{3,4} \d+ · (Q[DIKW]\d+) · (.+?)\s*$", re.M)
NEED = re.compile(r"^- (E\d+) · (compute|cite|judge) · (.+?)\s*$", re.M)
AGREED = re.compile(r"^\*\*Needs agreed\*\*:\s*(.+?)\s*$", re.M)
CELL = re.compile(r"(✅|🟡|🚫|⬜)\s*([DIKW]\d{2}-[a-z]+)(?![\w-])")
PAGE_STEM = re.compile(r"^([DIKW]\d{2}-[a-z]+)(?:-|$)")
CITE = re.compile(r"\[(Q[DIKW]\d+\.E\d+)\]")
HEADER = re.compile(r"^([a-z][a-z-]*):\s*(.*?)\s*$", re.M)
RUNG = {"D": 0, "I": 1, "K": 2, "W": 3}
KINDS_AT = {"D": {"compute"}, "I": {"compute", "cite"},
            "K": {"compute", "cite", "judge"}, "W": {"cite", "judge"}}


@dataclass
class Need:
    qid: str
    eid: str
    kind: str
    text: str
    pass_: str = ""
    from_: list = field(default_factory=list)
    retired: bool = False

    @property
    def full(self):
        return f"{self.qid}.{self.eid}"


@dataclass
class Question:
    qid: str
    name: str
    needs: list
    agreed: str
    cells: list = field(default_factory=list)   # (mark, page id)


# ── registers ────────────────────────────────────────────────────────────────
def parse_needs(qid, block):
    needs = []
    for m in NEED.finditer(block):
        eid, kind, rest = m.groups()
        parts = [p.strip() for p in rest.split(" · ")]
        n = Need(qid, eid, kind, parts[0])
        for p in parts[1:]:
            if p.startswith("pass:"):
                n.pass_ = p[5:].strip()
            elif p.startswith("from:"):
                n.from_ = [x.strip() for x in p[5:].split(",") if x.strip()]
            elif p.startswith("retired:"):
                n.retired = True
        needs.append(n)
    return needs


def parse_queue(text):
    """(qid, mark, page) for every cell token in the Queue fence.

    Row-major registers start each row with its question id; a transposed
    register names the questions in its header. Either way a token belongs to
    the column its header sits over, so tokens are placed by character column.
    """
    m = re.search(r"Queue[^\n]*\n.*?```text\n(.*?)```", text, re.S)
    if not m:
        return []
    lines = m.group(1).splitlines()
    head = next((l for l in lines if l.strip().startswith("id")), "")
    head_q = [(h.start(), h.group()) for h in QID.finditer(head)]
    out, current, started = [], None, False
    for line in lines[lines.index(head) + 1 if head in lines else 0:]:
        if not line.strip():
            if started:
                break                                    # the rows end; notes below hold tokens too
            continue
        if set(line.strip()) <= set("─-"):
            continue
        started = True
        lead = re.match(r"^(Q[DIKW]\d+)\b", line)
        if lead:
            current = lead.group(1)
        for c in CELL.finditer(line):
            if head_q:                                   # transposed: column names the question
                qid = [q for pos, q in head_q if pos <= c.start() + 1][-1:] or [head_q[0][1]]
                qid = qid[0]
            else:
                qid = current
            if qid:
                out.append((qid, c.group(1), c.group(2)))
    return out


def read_registers(board):
    questions = {}
    for reg in sorted((board / "0-MT-meta").glob("MT0[1-4]-*/MT0[1-4]-*.md")):
        text = reg.read_text(encoding="utf-8")
        divisions = list(DIVISION.finditer(text))
        for i, d in enumerate(divisions):
            end = divisions[i + 1].start() if i + 1 < len(divisions) else len(text)
            block = text[d.end():end]
            block = re.split(r"^## ", block, flags=re.M)[0]
            ag = AGREED.search(block)
            questions[d.group(1)] = Question(d.group(1), d.group(2), parse_needs(d.group(1), block),
                                             ag.group(1) if ag else "")
        for qid, mark, page in parse_queue(text):
            questions.setdefault(qid, Question(qid, "", [], "")).cells.append((mark, page))
    return questions


# ── pages ────────────────────────────────────────────────────────────────────
def find_pages(board):
    pages = {}
    for d in sorted(board.glob("*/*/")):
        m = PAGE_STEM.match(d.name)
        md = d / f"{d.name}.md"
        if m and md.is_file():
            pages[m.group(1)] = d
    return pages


def header(text):
    head = text.split("\n## ", 1)[0]
    return {k: v for k, v in HEADER.findall(head)}


def runtime(result_dir):
    p = result_dir / "runtime.yaml"
    if not p.is_file():
        return None
    try:
        return yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return None


def has_field(path, name):
    if path.suffix == ".csv":
        with path.open(newline="", encoding="utf-8") as f:
            return name in (next(csv.reader(f), []) or [])
    if path.suffix == ".json":
        node = json.loads(path.read_text(encoding="utf-8"))
        for part in name.split("."):
            if not isinstance(node, dict) or part not in node:
                return False
            node = node[part]
        return True
    return False


def ts(v):
    """A comparable UTC second: YAML may hand back a datetime or a string."""
    return str(v).replace(" ", "T")[:19] if v else ""


# ── one cell ─────────────────────────────────────────────────────────────────
def check_cell(q, mark, pid, pages, questions):
    problems, notes = [], []
    rung = q.qid[1]
    live = [n for n in q.needs if not n.retired]
    page_dir = pages.get(pid)
    if page_dir is None:
        return "GAP", [f"page {pid} not found on the board"], notes
    text = (page_dir / f"{page_dir.name}.md").read_text(encoding="utf-8")
    if not live:
        return "UNPLANNED", [], ["no need lines under What would answer it"]
    if not q.agreed.startswith("✅"):
        notes.append("needs not agreed")
    for n in live:
        if n.kind not in KINDS_AT[rung]:
            problems.append(f"{n.full}: a {n.kind} need is not legal at rung {rung}")
        if n.kind == "compute" and not n.pass_:
            problems.append(f"{n.full}: a compute need has no pass:")
        if n.kind in ("cite", "judge") and not n.from_:
            problems.append(f"{n.full}: a {n.kind} need has no from:")
        for f in n.from_ if n.kind == "cite" else []:
            src = f.split(".")[0]
            if src not in questions:
                problems.append(f"{n.full}: cites unknown question {src}")
            elif RUNG[src[1]] > RUNG[rung] or RUNG[rung] - RUNG[src[1]] > 1:
                problems.append(f"{n.full}: cites {f}, not the same rung or one below")

    amap_path = page_dir / "answers.yaml"
    amap = (yaml.safe_load(amap_path.read_text(encoding="utf-8")) or {}) if amap_path.is_file() else {}
    binding = amap.get(q.qid)
    if not binding:
        return "UNBOUND", [f"{pid}/answers.yaml has no {q.qid} entry"] + problems, notes

    read_at = ts(header(text).get("results-read"))
    stale = []
    for n in live:
        b = binding.get(n.eid)
        if b is None:
            problems.append(f"{n.full}: not bound in answers.yaml")
            continue
        if isinstance(b, dict) and "refused" in b:
            if mark == "✅":
                problems.append(f"{n.full}: refused on a ✅ cell")
        elif n.kind == "judge":
            if b != "judge":
                problems.append(f"{n.full}: a judge need binds `judge`, found {b!r}")
        elif n.kind == "cite":
            cited = b.get("pages") if isinstance(b, dict) else None
            if not cited:
                part = pid.split("-", 1)[1]
                src = questions.get(n.from_[0].split(".")[0]) if n.from_ else None
                cited = [p for _m, p in (src.cells if src else []) if p.endswith(f"-{part}")][:1]
            if not cited:
                problems.append(f"{n.full}: no page answers {', '.join(n.from_)} on this partition")
            for cp in cited or []:
                cdir = pages.get(cp)
                if cdir is None:
                    problems.append(f"{n.full}: cited page {cp} not found")
                    continue
                cmap_p = cdir / "answers.yaml"
                cmap = (yaml.safe_load(cmap_p.read_text(encoding="utf-8")) or {}) if cmap_p.is_file() else {}
                for f in n.from_:
                    fq, fe = f.split(".")
                    if fe not in (cmap.get(fq) or {}):
                        notes.append(f"{n.full}: {cp} does not bind {f} (cite unverified)")
        else:   # compute
            if not isinstance(b, dict) or "ticket" not in b:
                problems.append(f"{n.full}: a compute need binds ticket and files")
                continue
            ticket = b["ticket"]
            if not (page_dir / "runs" / f"{ticket}.sh").is_file():
                problems.append(f"{n.full}: ticket runs/{ticket}.sh missing")
            rdir = page_dir / "results" / ticket
            rt = runtime(rdir)
            if rt is None:
                problems.append(f"{n.full}: results/{ticket}/runtime.yaml missing")
                continue
            if rt.get("status") != "ok":
                problems.append(f"{n.full}: run {ticket} status {rt.get('status')}")
            for fn in b.get("files") or []:
                fp = rdir / fn
                if not fp.is_file():
                    problems.append(f"{n.full}: results/{ticket}/{fn} missing")
                    continue
                for fld in b.get("fields") or []:
                    if fp.suffix in (".csv", ".json") and not has_field(fp, fld):
                        problems.append(f"{n.full}: {fn} has no field {fld}")
            if not b.get("files"):
                problems.append(f"{n.full}: binds no files")
            ended = ts(rt.get("ended"))
            if read_at and ended and ended > read_at:
                stale.append(f"{n.full}: {ticket} ended {ended} after results-read {read_at}")
        cited_ids = set(CITE.findall(text))
        ok_ids = {n.full} | (set(n.from_) if n.kind == "cite" else set())   # a cite need may carry its source id
        if not (isinstance(b, dict) and "refused" in b) and not (ok_ids & cited_ids):
            problems.append(f"{n.full}: not cited in the page text")
    if not read_at:
        notes.append("no results-read: line, freshness unknown")
    if problems:
        return "GAP", problems + stale, notes
    if stale:
        return "STALE", stale, notes
    return "OK", [], notes


def run(board, only_q=None, only_page=None):
    questions = read_registers(board)
    pages = find_pages(board)
    rows = []
    for q in sorted(questions.values(), key=lambda q: (RUNG[q.qid[1]], int(q.qid[2:]))):
        if only_q and q.qid != only_q:
            continue
        for mark, pid in q.cells:
            if only_page and pid != only_page:
                continue
            verdict, problems, notes = check_cell(q, mark, pid, pages, questions)
            rows.append({"question": q.qid, "name": q.name, "page": pid, "mark": mark,
                         "verdict": verdict, "overclaim": mark == "✅" and verdict in ("GAP", "STALE", "UNBOUND"),
                         "problems": problems, "notes": notes,
                         "needs": [f"{n.full} {n.kind}" for n in q.needs if not n.retired]})
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("board", type=Path)
    ap.add_argument("--format", choices=("text", "json"), default="text")
    ap.add_argument("--strict", action="store_true", help="UNPLANNED cells fail too")
    ap.add_argument("--question")
    ap.add_argument("--page")
    a = ap.parse_args(argv)
    if not (a.board / "0-MT-meta").is_dir():
        print(f"{a.board}: no 0-MT-meta/, not an InsightBoard", file=sys.stderr)
        return 2
    rows = run(a.board, a.question, a.page)
    fail = [r for r in rows if r["overclaim"] or (a.strict and r["verdict"] == "UNPLANNED")]
    if a.format == "json":
        print(json.dumps({"cells": rows, "failed": len(fail)}, indent=2, ensure_ascii=False))
        return 1 if fail else 0
    counts = {}
    for r in rows:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    print(f"{a.board.name}: {len(rows)} answered cells · "
          + " · ".join(f"{k} {v}" for k, v in sorted(counts.items()))
          + f" · overclaims {sum(r['overclaim'] for r in rows)}")
    for r in rows:
        if r["verdict"] == "OK" and not r["notes"]:
            continue
        flag = "  ✗ overclaim" if r["overclaim"] else ""
        print(f"\n{r['question']} {r['name']} · {r['mark']} {r['page']} · {r['verdict']}{flag}")
        for p in r["problems"]:
            print(f"    - {p}")
        for n in r["notes"]:
            print(f"    · {n}")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
