"""Read and check the Question │ Work │ Report rows of one level (haipipe-report, b03 s21, 261007).

A level is a Block (`board.md`), a Job or a Task (`<folder>/<folder>.md`). Its rows are what the
workbench's Audience Report draws: one per Question of the face's `## Questions` register, plus a
report folder not yet registered.

    Question   the register row: id, title, group
    Work       each Job or Task below whose face says `answers: <id>` (or a need, `<id>.E<n>`),
               then the register's own `work:` entries
    Report     reports/qNN_<topic>/qNN_<topic>.md: answer-status, its Opening, its drawing

The check (exit 1 on any error):

    error    answer-status is not open · partial · answered
    error    a face's `answers:` names a Question this level's register does not have
    error    a report's `answers:` does not name its own Question
    error    an answered report with no Opening, or with no Evidence link
    error    a report folder no register row names (register it, or say why not)
    warn     partial or answered without `results-read:` (the evidence read time)
    warn     a `## Figures` list whose drawing is missing or older than the .md or a source drawing
    warn     answered with no Work row and no Evidence link (reasoning only: say so in Limits)

    python check_report.py <level folder> [--json]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

STATES = ("open", "partial", "answered")
SKIP = {"studio", "reports", "runs", "delivery", "draft", "displays", "notebooks", "results", "scripts",
        "src", "sbatch", "tests", "workflow", "resources", "_old", "_build"}


def face(folder: Path) -> Path | None:
    """The level's face: `<folder>.md`, else a Block's `board.md`."""
    for name in (folder.name + ".md", "board.md"):
        if (folder / name).is_file():
            return folder / name
    return None


def register(md: Path | None) -> list[dict]:
    """The face's `## Questions` register: a fenced yaml `questions:` list. A register that is not
    valid yaml raises ValueError, with the parser's line."""
    if not md:
        return []
    m = re.search(r"(?ms)^## Questions[ \t]*\n.*?```ya?ml\n(.*?)```", md.read_text(encoding="utf-8", errors="ignore"))
    if not m:
        return []
    import yaml
    try:
        rows = (yaml.safe_load(m.group(1)) or {}).get("questions") or []
    except yaml.YAMLError as err:
        mark = getattr(err, "problem_mark", None)
        raise ValueError(f"its ## Questions yaml does not parse"
                         + (f" (line {mark.line + 1} of the block)" if mark else "")) from None
    return [r for r in rows if isinstance(r, dict) and r.get("id")]


def header(md: Path, key: str) -> str:
    m = re.search(rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$", md.read_text(encoding="utf-8", errors="ignore"))
    return m.group(1) if m else ""


def answered_ids(value: str) -> list[str]:
    """`answers: Q01, QK10.E1` -> ['q01', 'qk10']: a need `<id>.E<n>` links to its Question."""
    out = []
    for tok in re.split(r"[,\s\[\]]+", value or ""):
        tok = re.sub(r"(?i)\.E\d+$", "", tok.strip().strip("'\""))
        if tok:
            out.append(tok.lower())
    return out


def children(folder: Path) -> list[Path]:
    """The Jobs (of a Block) or Tasks (of a Job): direct folders with a face of their own name. A theme's
    own names (a paper's version groups, its Sections) count the same as jNN_ / tNN_."""
    if not folder.is_dir():
        return []
    return [p for p in sorted(folder.iterdir()) if p.is_dir() and p.name not in SKIP
            and not p.name.startswith((".", "_")) and (p / (p.name + ".md")).is_file()]


def section(text: str, name: str) -> str:
    m = re.search(rf"(?ms)^#{{2,3}} {re.escape(name)}[ \t]*\n(.*?)(?=^#{{1,3}} |\Z)", text)
    return re.sub(r"<!--.*?-->", "", m.group(1), flags=re.S).strip() if m else ""


def figures_stale(page: Path) -> str:
    """Why the report's generated drawing is not current, or ''."""
    text = page.read_text(encoding="utf-8", errors="ignore")
    block = re.search(r"(?ms)^## Figures\s*$(?:(?!^## ).)*?^```yaml\n(.*?)^```", text)
    if not block:
        return ""
    drawing = page.with_suffix(".excalidraw")
    if not drawing.is_file():
        return "its ## Figures drawing is not built yet"
    import yaml
    sources = [(page.parent / f["from"]) for f in (yaml.safe_load(block.group(1)) or {}).get("figures") or []
               if isinstance(f, dict) and f.get("from")]
    newer = [s.name for s in [page] + sources if s.is_file() and s.stat().st_mtime > drawing.stat().st_mtime]
    return f"its drawing is older than {', '.join(newer)}: rebuild it" if newer else ""


def rows(folder: Path) -> tuple[list[dict], list[tuple[str, str]]]:
    """(rows, findings): the Question │ Work │ Report rows of one level and what the check found."""
    folder = folder.resolve()
    md = face(folder)
    findings: list[tuple[str, str]] = []
    if not md:
        return [], [("error", f"{folder.name}: no face ({folder.name}.md or board.md)")]
    try:
        reg = register(md)
    except ValueError as err:
        return [], [("error", f"{md.name}: {err}")]
    known = {str(r["id"]).lower() for r in reg}
    reports = {q.name.split("_", 1)[0].lower(): q for q in sorted((folder / "reports").glob("q*/"))
               if q.is_dir()} if (folder / "reports").is_dir() else {}

    # Work: every Job or Task below whose face says answers:
    work: dict[str, list[str]] = {}
    kids = children(folder)
    for kid in kids + [g for k in kids for g in children(k)]:
        kmd = face(kid)
        for qid in answered_ids(header(kmd, "answers")) if kmd else []:
            if qid not in known:
                findings.append(("error", f"{kid.relative_to(folder)}: answers {qid.upper()}, which the register "
                                          f"of {md.name} does not have"))
            work.setdefault(qid, []).append(kid.relative_to(folder).as_posix())

    out = []
    for r in reg + [{"id": k.upper(), "title": ""} for k in reports if k not in known]:
        qid = str(r["id"])
        row = {"id": qid, "title": r.get("title") or "", "group": r.get("group") or "",
               "work": work.get(qid.lower(), []) + [str(w.get("path") if isinstance(w, dict) else w)
                                                    for w in (r.get("work") or []) if w],
               "report": "", "status": "open", "drawing": ""}
        if qid.lower() not in known:
            findings.append(("error", f"reports/{reports[qid.lower()].name}/: no register row names {qid}"))
        rp = r.get("report")
        page = folder / rp if rp and (folder / rp).is_file() else None
        if not page and qid.lower() in reports:
            q = reports[qid.lower()]
            page = q / (q.name + ".md") if (q / (q.name + ".md")).is_file() else None
        if page:
            text = page.read_text(encoding="utf-8", errors="ignore")
            row["report"] = page.relative_to(folder).as_posix()
            status = header(page, "answer-status") or "open"
            row["status"] = status
            where = row["report"]
            if status not in STATES:
                findings.append(("error", f"{where}: answer-status {status!r} is not one of {' · '.join(STATES)}"))
            if qid.lower() not in answered_ids(header(page, "answers")):
                findings.append(("error", f"{where}: answers: does not name {qid}"))
            evidence = re.findall(r"\]\(([^)]+)\)", section(text, "Evidence"))
            if status == "answered":
                if not section(text, "Opening"):
                    findings.append(("error", f"{where}: answered, but its Opening states no answer"))
                if not evidence:
                    findings.append(("error", f"{where}: answered, but its Evidence links nothing"))
                if not evidence and not row["work"]:
                    findings.append(("warn", f"{where}: answered with no Work and no Evidence: say so in Limits"))
            if status in ("partial", "answered") and not header(page, "results-read"):
                findings.append(("warn", f"{where}: {status}, but results-read: is not recorded"))
            stale = figures_stale(page)
            if stale:
                findings.append(("warn", f"{where}: {stale}"))
            if page.with_suffix(".excalidraw").is_file():
                row["drawing"] = page.with_suffix(".excalidraw").relative_to(folder).as_posix()
        out.append(row)
    return out, findings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("level", type=Path, help="a Block, Job or Task folder")
    ap.add_argument("--json", action="store_true", help="print the rows and findings as JSON")
    args = ap.parse_args()
    found, findings = rows(args.level)
    if args.json:
        print(json.dumps({"rows": found, "findings": [{"level": l, "text": t} for l, t in findings]}, indent=1))
    else:
        for r in found:
            print(f"{r['id']:<10} {r['status']:<9} work {len(r['work']):>2} · "
                  f"{r['report'] or 'no report yet'}{' · drawing' if r['drawing'] else ''}")
        for level, text in findings:
            print(f"{level:<6} {text}")
        if not found:
            print("no Questions at this level")
    return 1 if any(l == "error" for l, _ in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
