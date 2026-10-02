#!/usr/bin/env python3
"""check_evidence — does each answered question's work and report fit its ask?

Reads one InsightBoard: the four registers (MT01-MT04: each question's evidence
needs, their work specs and the Queue cells), every answering page the cells
name (its answers.yaml, runs/ tickets, results/<ticket>/, its plan and
Evidence Items, and its text) and the task configs those tickets call.
Returns one verdict per register cell that names a page (haipipe-insight
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
NEED = re.compile(r"^- (E\d+) · (compute|cite|judge) · (.+?)\s*$")
SPEC_LINE = re.compile(r"^\s{2,}(cut|unit|measure|by|uncertainty|rivals|output):\s*(.+?)\s*$")
SPEC_KEYS = ("cut", "unit", "measure", "by", "uncertainty", "rivals", "output")
ASK = re.compile(r"^\*\*The ask\*\*:\s*(.+?)\s*$", re.M)
COVERED = re.compile(r"^\*\*Ask covered\*\*:\s*(.+?)\s*$", re.M)
ASK_TAG = re.compile(r'\s*·\s*ask:\s*"([^"]+)"\s*$')
ASKED_KEYS = ("measure", "by")              # the two spec lines that say what is computed
CAUSAL = re.compile(r"\b(move|moves|moved|drive|drives|cause|causes|caused|impact|impacts|affect|affects|"
                    r"effect of|lift|lifts|boost|boosts|improve|improves)\b", re.I)
STOP = set("""a an the and or of on in at to for by with from as is are was were be been does do did
what which who whom whose how why when where whether that this these those it its their there than then
each every any all some per into over under across between within without rather not no only also more
most much many same other same carry carries""".split())
AGREED = re.compile(r"^\*\*Needs agreed\*\*:\s*(.+?)\s*$", re.M)
CELL = re.compile(r"(✅|🟡|🚫|⬜)\s*([DIKW]\d{2}-[a-z]+)(?![\w-])")
PAGE_STEM = re.compile(r"^([DIKW]\d{2}-[a-z]+)(?:-|$)")
INLINE = re.compile(r"\[(Q[DIKW]\d+\.E\d+)\]")
REALIZES = re.compile(r"<!-- realizes: (C\d+\.P\d+\.B\d+) -->")
HEADER = re.compile(r"^([a-z][a-z-]*):\s*(.*?)\s*$", re.M)
EXEC = re.compile(r'exec\s+"\$\{PAGE\}/([^"]+?\.sh)"')
ITEM = re.compile(r"^### (E\d+-[A-Z]+-[\w-]+) · (C\d+\.P\d+\.B\d+)", re.M)
RUNG = {"D": 0, "I": 1, "K": 2, "W": 3}
KINDS_AT = {"D": {"compute"}, "I": {"compute", "cite"},
            "K": {"compute", "cite", "judge"}, "W": {"cite", "judge"}}
OPEN_CUTS = ("the cell's partition", "each partition", "every partition", "the whole extract")


@dataclass
class Need:
    qid: str
    eid: str
    kind: str
    text: str
    pass_: str = ""
    from_: list = field(default_factory=list)
    retired: bool = False
    spec: dict = field(default_factory=dict)
    spec_ask: dict = field(default_factory=dict)    # spec key -> the ask phrase it answers

    @property
    def full(self):
        return f"{self.qid}.{self.eid}"

    def outputs(self):
        """The spec's output line as {file: [columns]}: `a.csv [x, y] ; b.json [k.v]`."""
        out = {}
        for part in self.spec.get("output", "").split(";"):
            m = re.match(r"\s*([\w./-]+)\s*(?:\[(.*?)\])?\s*$", part)
            if m and m.group(1):
                out[m.group(1)] = [c.strip() for c in (m.group(2) or "").split(",") if c.strip()]
        return out


@dataclass
class Question:
    qid: str
    name: str
    needs: list
    agreed: str
    cells: list = field(default_factory=list)   # (mark, page id)
    ask: str = ""
    covered: str = ""


# ── registers ────────────────────────────────────────────────────────────────
def parse_needs(qid, block):
    """Need lines, each followed by its indented work-spec lines."""
    needs, current = [], None
    for line in block.splitlines():
        m = NEED.match(line)
        if m:
            eid, kind, rest = m.groups()
            parts = [p.strip() for p in rest.split(" · ")]
            current = Need(qid, eid, kind, parts[0])
            for p in parts[1:]:
                if p.startswith("pass:"):
                    current.pass_ = p[5:].strip()
                elif p.startswith("from:"):
                    current.from_ = [x.strip() for x in p[5:].split(",") if x.strip()]
                elif p.startswith("retired:"):
                    current.retired = True
            needs.append(current)
            continue
        s = SPEC_LINE.match(line)
        if s and current is not None:
            value, tag = s.group(2), ASK_TAG.search(s.group(2))
            if tag:
                current.spec_ask[s.group(1)] = tag.group(1)
                value = value[:tag.start()].rstrip()
            current.spec[s.group(1)] = value
            continue
        if not line.startswith((" ", "\t")):
            current = None
    return needs


def parse_queue(text):
    """(qid, mark, page) for every cell token in the Queue fence's rows.

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
            if head_q:                                   # transposed: the column names the question
                qid = ([q for pos, q in head_q if pos <= c.start() + 1][-1:] or [head_q[0][1]])[0]
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
            block = re.split(r"^## ", text[d.end():end], flags=re.M)[0]
            ag = AGREED.search(block)
            ask, cov = ASK.search(block), COVERED.search(block)
            questions[d.group(1)] = Question(d.group(1), d.group(2), parse_needs(d.group(1), block),
                                             ag.group(1) if ag else "",
                                             ask=ask.group(1) if ask else "", covered=cov.group(1) if cov else "")
        for qid, mark, page in parse_queue(text):
            questions.setdefault(qid, Question(qid, "", [], "")).cells.append((mark, page))
    return questions


# ── a plan answers its ask (evidence-needs.md § 1, hard rules) ───────────────
def words(text):
    return {w for w in re.findall(r"[a-z][a-z'-]{3,}", text.lower()) if w not in STOP}


def plan_problems(q, live):
    """The hard rules that tie a question's plan to its own ask, read before any binding."""
    problems = []
    rung = q.qid[1]
    if not q.ask:
        return [f"{q.qid}: no **The ask**: line, so nothing can be traced to it"]
    if rung in "DI" and CAUSAL.search(q.ask):
        problems.append(f"{q.qid}: the ask claims a cause ('{CAUSAL.search(q.ask).group(0)}') at a rung that "
                        f"reports no cause; reword it to an association or route that half to Knowledge")
    ask_l = q.ask.lower()
    ids = {n.eid for n in live}
    if not q.covered:
        problems.append(f"{q.qid}: no **Ask covered**: line mapping each phrase of the ask to a need")
    else:
        covered_words = set()
        for part in q.covered.split(" · "):
            m = re.match(r'\s*"([^"]+)"\s*→\s*(.+?)\s*$', part)
            if not m:
                problems.append(f"{q.qid}: Ask covered part {part!r} is not '\"<phrase>\" → <needs | partial: … | refused: …>'")
                continue
            phrase, target = m.groups()
            if phrase.lower() not in ask_l:
                problems.append(f"{q.qid}: Ask covered phrase \"{phrase}\" is not in the ask")
            covered_words |= words(phrase)
            if not re.match(r"(partial|refused):\s*\S", target):
                for t in [x.strip() for x in target.split(",")]:
                    if t not in ids:
                        problems.append(f"{q.qid}: Ask covered maps \"{phrase}\" to {t}, which is not a live need")
        missing = sorted(words(q.ask) - covered_words)
        if missing:
            problems.append(f"{q.qid}: ask words no need answers: {', '.join(missing)}")
    for n in live:
        if n.kind != "compute":
            continue
        for key in ASKED_KEYS:
            phrase = n.spec_ask.get(key)
            if not phrase:
                problems.append(f"{n.full}: spec {key}: carries no ask: \"<phrase>\" naming what of the ask it computes")
            elif phrase.lower() not in ask_l:
                problems.append(f"{n.full}: spec {key}: ask phrase \"{phrase}\" is not in the ask")
    return problems


# ── pages ────────────────────────────────────────────────────────────────────
def find_pages(board):
    pages = {}
    for d in sorted(board.glob("*/*/")):
        m = PAGE_STEM.match(d.name)
        if m and (d / f"{d.name}.md").is_file():
            pages[m.group(1)] = d
    return pages


def header(text):
    head = re.split(r"(?m)^## ", text, maxsplit=1)[0]
    return {k: v for k, v in HEADER.findall(head)}


def load_yaml(path):
    if not path.is_file():
        return None
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
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


def ticket_config(page_dir, ticket):
    """The task config a page ticket ends up running, or None."""
    path = page_dir / "runs" / f"{ticket}.sh"
    m = EXEC.search(path.read_text(encoding="utf-8")) if path.is_file() else None
    if not m:
        return None
    task_ticket = (page_dir / m.group(1)).resolve()
    cfg = task_ticket.parent.parent / "scripts" / "config" / f"{task_ticket.stem}.yaml"
    return cfg if cfg.is_file() else None


def page_citations(page_dir, text):
    """Which need ids the page cites, and the Evidence Item artifacts per need.

    A new page cites through its plan: an Evidence Item carries `**Need**: <id>`
    and its heading names the Bullet it serves; a realized Page sentence of that
    Bullet is the citation. A judge need is a Bullet whose Evidence line reads
    `none · judge <id>`. A page written before the contract may carry inline
    `[<id>]` tags instead.
    """
    cited = set(INLINE.findall(text))
    realized = set(REALIZES.findall(text))
    artifacts = {}
    draft = page_dir / "draft"
    items = draft / f"{page_dir.name}-evidence-items.md"
    if items.is_file():
        body = items.read_text(encoding="utf-8")
        heads = list(ITEM.finditer(body))
        for i, h in enumerate(heads):
            chunk = body[h.end():heads[i + 1].start() if i + 1 < len(heads) else len(body)]
            need = re.search(r"\*\*Need\*\*:\s*(.+)", chunk)
            art = re.search(r"\*\*Artifact\*\*:\s*`([^`]+)`", chunk)
            for nid in (re.findall(r"Q[DIKW]\d+\.E\d+", need.group(1)) if need else []):
                if art:
                    artifacts.setdefault(nid, set()).add(art.group(1))
                if h.group(2) in realized:
                    cited.add(nid)
    plans = sorted(draft.glob(f"{page_dir.name}-draft-v*.md")) if draft.is_dir() else []
    for plan in plans[:1]:
        para = bullet = None
        for line in plan.read_text(encoding="utf-8").split("\n## 2 ·", 1)[0].splitlines():
            ph = re.match(r"^### (C\d+\.P\d+)\b", line)
            if ph:
                para, bullet = ph.group(1), None
                continue
            b = re.match(r"^- (?:\[[ xX]\]\s*)?B(\d+)\s*·", line)
            if b and para:
                bullet = f"{para}.B{b.group(1)}"
                continue
            j = re.match(r"^\s+Evidence:\s*none\s*·\s*judge\s+(Q[DIKW]\d+\.E\d+)", line)
            if j and bullet and bullet in realized:
                cited.add(j.group(1))
    return cited, artifacts


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
    unspecced = [n.full for n in live if n.kind == "compute" and not n.spec]
    if unspecced:
        return "UNPLANNED", [], [f"compute need(s) without a work spec: {', '.join(unspecced)}"]
    if not q.agreed.startswith("✅"):
        notes.append("needs not agreed")
    problems.extend(plan_problems(q, live))
    part = pid.split("-", 1)[1]
    for n in live:
        if n.kind not in KINDS_AT[rung]:
            problems.append(f"{n.full}: a {n.kind} need is not legal at rung {rung}")
        if n.kind == "compute":
            if not n.pass_:
                problems.append(f"{n.full}: a compute need has no pass:")
            missing = [k for k in SPEC_KEYS if not n.spec.get(k)]
            if missing:
                problems.append(f"{n.full}: work spec lacks {', '.join(missing)}")
            elif not n.outputs():
                problems.append(f"{n.full}: work spec names no output file")
            cut = n.spec.get("cut", "")
            if cut and cut not in OPEN_CUTS and cut != part:
                problems.append(f"{n.full}: spec cut is {cut}, page {pid} is on {part}")
        if n.kind in ("cite", "judge") and not n.from_:
            problems.append(f"{n.full}: a {n.kind} need has no from:")
        for f in n.from_ if n.kind == "cite" else []:
            src = f.split(".")[0]
            if src not in questions:
                problems.append(f"{n.full}: cites unknown question {src}")
            elif RUNG[rung] - RUNG[src[1]] != 1 and not (src[1] == rung and part == "cross"):
                problems.append(f"{n.full}: cites {f}; a cite reads one rung below "
                                f"(the same rung only on a cross page)")
            else:
                target = next((m for m in questions[src].needs if m.full == f), None)
                if "." in f and target is None:
                    problems.append(f"{n.full}: cites {f}, which {src} does not list")
                elif target is not None and target.retired:
                    problems.append(f"{n.full}: cites {f}, which is retired; cite its reissued need")

    binding = (load_yaml(page_dir / "answers.yaml") or {}).get(q.qid)
    if not binding:
        return "UNBOUND", [f"{pid}/answers.yaml has no {q.qid} entry"] + problems, notes

    read_at = ts(header(text).get("results-read"))
    cited, artifacts = page_citations(page_dir, text)
    stale = []
    for n in live:
        b = binding.get(n.eid)
        if b is None:
            problems.append(f"{n.full}: not bound in answers.yaml")
            continue
        refused = isinstance(b, dict) and "refused" in b
        if refused and mark == "✅":
            problems.append(f"{n.full}: refused on a ✅ cell")
        if n.kind == "judge" and not refused:
            if b != "judge":
                problems.append(f"{n.full}: a judge need binds `judge`, found {b!r}")
        elif n.kind == "cite" and not refused:
            cited_pages = b.get("pages") if isinstance(b, dict) else None
            if not cited_pages:
                src = questions.get(n.from_[0].split(".")[0]) if n.from_ else None
                cited_pages = [p for _m, p in (src.cells if src else []) if p.endswith(f"-{part}")][:1]
            if not cited_pages:
                problems.append(f"{n.full}: no page answers {', '.join(n.from_)} on this partition")
            for cp in cited_pages or []:
                cdir = pages.get(cp)
                if cdir is None:
                    problems.append(f"{n.full}: cited page {cp} not found")
                    continue
                cmap = load_yaml(cdir / "answers.yaml") or {}
                for f in n.from_:
                    fq, fe = f.split(".")
                    if fe not in (cmap.get(fq) or {}):
                        notes.append(f"{n.full}: {cp} does not bind {f} (cite unverified)")
        else:   # a compute need, or any refusal: both rest on a run
            tickets = ([b["ticket"]] if isinstance(b, dict) and b.get("ticket") else []) + \
                (list(b.get("tickets") or []) if isinstance(b, dict) else [])
            if not tickets:
                problems.append(f"{n.full}: " + ("a refusal needs its probe run (ticket and files)" if refused
                                                  else "a compute need binds ticket and files"))
                continue
            for ticket in tickets:
                stale += check_ticket(n, b, ticket, page_dir, problems, artifacts, read_at, refused)
        ok_ids = {n.full} | (set(n.from_) if n.kind == "cite" else set())
        if not refused and not (ok_ids & cited):
            problems.append(f"{n.full}: not cited by the page (no realized Evidence Item, judge Bullet or tag)")
    if not read_at:
        notes.append("no results-read: line, freshness unknown")
    if problems:
        return "GAP", problems + stale, notes
    if stale:
        return "STALE", stale, notes
    return "OK", [], notes


def check_ticket(n, b, ticket, page_dir, problems, artifacts, read_at, refused):
    """One bound run of a compute need (or a refusal's probe): ticket, receipt, files, columns, config."""
    stale = []
    if not (page_dir / "runs" / f"{ticket}.sh").is_file():
        problems.append(f"{n.full}: ticket runs/{ticket}.sh missing")
    rdir = page_dir / "results" / ticket
    rt = load_yaml(rdir / "runtime.yaml")
    if rt is None:
        problems.append(f"{n.full}: results/{ticket}/runtime.yaml missing")
        return stale
    if rt.get("status") != "ok":
        problems.append(f"{n.full}: run {ticket} status {rt.get('status')}")
    files = list(b.get("files") or [])
    if not files:
        problems.append(f"{n.full}: binds no files")
    required = n.outputs() if n.kind == "compute" else {}
    for fn in required:
        if fn not in files:
            problems.append(f"{n.full}: spec output {fn} is not bound")
    extra = list(b.get("fields") or [])
    for fn in files:
        fp = rdir / fn
        if not fp.is_file():
            problems.append(f"{n.full}: results/{ticket}/{fn} missing")
            continue
        for fld in required.get(fn, []) + (extra if fp.suffix in (".csv", ".json") else []):
            if not has_field(fp, fld):
                problems.append(f"{n.full}: {fn} has no column {fld}")
    if n.kind == "compute":
        cfg = ticket_config(page_dir, ticket)
        if cfg is None:
            problems.append(f"{n.full}: ticket {ticket} calls no task config")
        else:
            line = re.search(r"(?m)^answers:\s*\[([^\]]*)\]", cfg.read_text(encoding="utf-8"))
            if not line or n.full not in [x.strip() for x in line.group(1).split(",")]:
                problems.append(f"{n.full}: config {cfg.parent.parent.parent.name}/{cfg.name} "
                                f"does not list {n.full} under answers:")
            served = {x.strip().split(".")[0] for x in line.group(1).split(",") if x.strip()} if line else set()
            if served - {n.qid}:
                problems.append(f"{n.full}: run {cfg.stem} of {cfg.parent.parent.parent.name} also serves "
                                f"{', '.join(sorted(served - {n.qid}))}; a run answers one question")
            # the run must be on the population the spec's cut names (a cross page reads many)
            part = page_dir.name.split("-")[1] if "-" in page_dir.name else ""
            cut = n.spec.get("cut", "")
            want = (part if cut == "the cell's partition" else "full" if cut in ("full", "the whole extract")
                    else None if cut in OPEN_CUTS or cut == "cross" else cut)
            pop = ((load_yaml(cfg) or {}).get("population") or {}).get("name")
            if want and part != "cross" and pop and pop != want:
                problems.append(f"{n.full}: {ticket} runs on population {pop}; the spec's cut asks for {want}")
    bound_files = {f"results/{t}/{fn}" for t in ([b.get("ticket")] if b.get("ticket") else []) + list(b.get("tickets") or []) for fn in files}
    for art in artifacts.get(n.full, ()):
        if art not in bound_files:
            problems.append(f"{n.full}: Evidence Item artifact {art} is not a bound file")
    ended = ts(rt.get("ended"))
    if read_at and ended and ended > read_at:
        stale.append(f"{n.full}: {ticket} ended {ended} after results-read {read_at}")
    return stale


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
