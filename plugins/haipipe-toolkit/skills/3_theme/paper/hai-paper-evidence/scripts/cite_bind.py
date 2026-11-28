"""cite_bind.py · bind a Section's CITE evidence items to the citation Run that checked each key.

    python cite_tasks.py bind <Section Task>            print the diff (dry run)
    python cite_tasks.py bind <Section Task> --apply    write draft/<stem>-evidence-items.md

A Section's evidence lives in draft/<stem>-evidence-items.md, one `### E<nn>-CITE-<slug>` item per cited paper. For
each, the key is the BibTeX key its Local Input or Expected holds, else its Label. The citation Job's Runs
(`jNN_evidence_cite/tNN_<group>/runs/rNN_check_citations/result/citations.csv`, written by `cite_tasks.py run`) say
which Run checked which key: a claim group's own Run first, the paper-wide t99 after, the newest Run of a Task first.

An item with no Local Run gets one, in the line the Draft Lab and `page.py health` read:

    - **Local Run**: Page · Evidence Item · reuse · P.j03.t01.r01 → j03_evidence_cite/t01_scaling_laws/runs/r01_check_citations/result/citations.csv

and, when it names none and the check names the paper's discovery Run, its Supporting Runs:

    - **Supporting Runs**: Discovery · reuse · b01.j03.t01.r01

An item that already names a Local Run is kept as it is. A key no Run has checked is listed, never bound: run
`cite_tasks.py gen` and the citation Job's tickets first. Nothing outside the one items file is written.
"""
from __future__ import annotations

import csv
import difflib
import re
from pathlib import Path

ITEM = re.compile(r"(?m)^###\s+(E\d+[a-z]?)-CITE-(\S+)[^\n]*$")
FIELD = re.compile(r"(?mi)^-\s*\*\*([^*]+)\*\*\s*:\s*(.*?)\s*$")
BIB_HEAD = re.compile(r"@\w+\s*\{\s*([^,\s]+)\s*,")


def _num(name: str) -> str:
    return (re.match(r"[a-z](\d+)", name) or [None, ""])[1]


def checks(board: Path) -> dict:
    """{key: (Board-relative citations.csv, P.jNN.tNN.rNN, its row)}."""
    files = sorted(Path(board).glob("j*/t*/runs/*/result/citations.csv"),
                   key=lambda f: (f.parents[3].name.startswith("t99"), f.parents[3].name,
                                  -int(_num(f.parents[1].name) or 0)))
    out = {}
    for f in files:
        run, task, job = f.parents[1], f.parents[3], f.parents[4]
        addr = f"P.j{_num(job.name)}.t{_num(task.name)}.r{_num(run.name)}"
        with f.open(encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                if r.get("key"):
                    out.setdefault(r["key"], (f.relative_to(board).as_posix(), addr, r))
    return out


def items_file(task: Path) -> Path:
    found = sorted((task / "draft").glob("*-evidence-items.md"))
    if not found:
        raise SystemExit(f"{task}: no draft/<stem>-evidence-items.md")
    return found[0]


def bind_text(text: str, seen: dict) -> tuple:
    """(new text, [(item, key, what was done)]) for one items file."""
    heads = list(ITEM.finditer(text))
    out, notes, last = [], [], 0
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        nxt = re.search(r"(?m)^#{1,6}\s", text[m.end():end])     # a retired sub-heading ends the item
        end = m.end() + nxt.start() if nxt else end
        body = text[m.end():end]
        fields = {k.strip().lower(): v for k, v in FIELD.findall(body)}
        name = f"{m.group(1)}-CITE-{m.group(2)}"
        bib = BIB_HEAD.search(fields.get("local input", "") + " " + fields.get("expected", ""))
        key = bib.group(1) if bib else fields.get("label", "").strip()
        out.append(text[last:m.end()])
        last = end
        if "retired" in fields.get("target", "").lower():
            out.append(body)
            notes.append((name, key, "retired: left as it is"))
            continue
        local = fields.get("local run", "")
        if local and not local.startswith(("\u2014", "-")):
            out.append(body)
            notes.append((name, key, "keeps its Local Run"))
            continue
        hit = seen.get(key)
        if not hit:
            out.append(body)
            notes.append((name, key, "no citation Run checked this key: run cite_tasks.py gen, then its tickets"))
            continue
        path, addr, row = hit
        add = [f"- **Local Run**: Page · Evidence Item · reuse · {addr} → {path}"]
        disc = [d.strip() for d in (row.get("discovery_runs") or "").split(",") if d.strip()]
        if disc and not fields.get("supporting runs"):
            add.insert(0, "- **Supporting Runs**: " + "; ".join(f"Discovery · reuse · {d}" for d in disc))
        lines = body.split("\n")
        lines = [ln for ln in lines if not re.match(r"(?i)^-\s*\*\*Local Run\*\*\s*:", ln)]   # an empty one goes
        at = next((j + 1 for j in range(len(lines) - 1, -1, -1)
                   if re.match(r"(?i)^-\s*\*\*Local Input\*\*", lines[j])), None)
        if at is None:
            at = next((j + 1 for j in range(len(lines) - 1, -1, -1) if FIELD.match(lines[j])), 1)
        out.append("\n".join(lines[:at] + add + lines[at:]))
        notes.append((name, key, f"bound to {addr}"))
    out.append(text[last:])
    return "".join(out), notes


def bind(task: Path, apply: bool = False) -> int:
    task = Path(task).resolve()
    f = items_file(task)
    board = task.parent.parent
    seen = checks(board)
    if not seen:
        raise SystemExit(f"{board}: no citation Run result (j*/t*/runs/*/result/citations.csv); run cite_tasks.py gen")
    old = f.read_text(encoding="utf-8")
    new, notes = bind_text(old, seen)
    for name, key, what in notes:
        print(f"{name:44} {key[:40]:40} {what}")
    if new == old:
        print("nothing to bind")
        return 0
    if not apply:
        rel = f.relative_to(board).as_posix()
        print("".join(difflib.unified_diff(old.splitlines(True), new.splitlines(True), f"a/{rel}", f"b/{rel}")))
        print("dry run: rerun with --apply to write it")
        return 0
    f.write_text(new, encoding="utf-8")
    print(f"wrote {f}")
    return 0
