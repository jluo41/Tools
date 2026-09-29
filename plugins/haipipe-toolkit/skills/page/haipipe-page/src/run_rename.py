"""Rename a Page's runs to the readable grammar, once (JL 260928).

    page.py run-names <page> --dry-run     print old → new, change nothing
    page.py run-names <page>               do it

For each run on the Page: its ticket moves to the flat `runs/<new>.<ext>`, its folder
to `results/<new>/`, and every mention inside the Page folder is rewritten (tickets,
runtime.yaml, result.yaml, the Draft and Evidence Markdown, records, scripts). The
generated `delivery/` is left alone: rebuild it with `page.py export`.

New names (`src/run_names.py`): `run-<kind>-<MMDD>-<slug>`. The day is the run's
`started_at`; the slug is the paragraph target (`p01-p02`, `c1-p2`), the Evidence
Item's slug (`score-validation`), or the ticket's Goal in a few words. Delivery
builds (`rdNN_<lane>`, `run_delivery_<lane>`) and runs of other families are kept.
"""
from __future__ import annotations

import datetime as dt
import re
from pathlib import Path

from . import run_names
from .outline_version import plan_dir
from .run_folders import FOLDERS

TEXT = {".md", ".yaml", ".yml", ".json", ".sh", ".ps1", ".py", ".txt", ".csv", ".tex", ".bib",
        ".toml", ".do", ".r", ".R", ".ipynb", ".mmd"}
SPACE_FOLDERS = tuple(FOLDERS) + ("check-run",)
_PJ = re.compile(r"^(p[._]?j\d+[._]?t\d+[._]?r\d+)(?:_(?P<slug>.*))?$", re.I)
_OLD_ITEM_KIND = {"values": "value", "displays": "display", "citations": "citation"}
# A ticket one folder deeper climbs one more level; moving it back up undoes that.
_SCRIPT_DOWN = re.compile(r'(\$\(cd "(?:\$\(dirname [^)]*\)|\$\{?\w+\}?))/\.\./\.\.(" && pwd\))')


def _page(target) -> tuple[Path, str]:
    target = Path(target)
    return (target.parent, target.stem) if target.is_file() else (target, target.name)


def _field(text: str, *names: str) -> str:
    for name in names:
        # YAML (`item: E01-…`, `- Goal: …`) or JSON (`"item": "E01-…",`)
        found = re.search(r'(?mi)^\s*(?:- )?"?%s"?\s*:\s*(.+?)\s*$' % re.escape(name), text or "")
        if found:
            return found.group(1).strip().rstrip(",").strip().strip("'\"")
    return ""


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:6000]
    except OSError:
        return ""


def _items_by_paper_run(folder: Path, stem: str) -> dict[str, str]:
    """`pj06t11r01` → `E11-VALUE-score-validation`, from the Evidence Markdown's item blocks."""
    items = plan_dir(folder) / ("%s-evidence-items.md" % stem)
    found, current = {}, None
    for line in (items.read_text(encoding="utf-8", errors="replace").splitlines() if items.is_file() else []):
        head = re.match(r"^### (E\d+-[A-Z]+-[\w-]+)", line)
        if head:
            current = head.group(1)
            continue
        if line.startswith("## "):
            current = None
        if current:
            for key in re.findall(r"\bp[._]?j\d+[._]?t\d+[._]?r\d+", line, re.I):
                found.setdefault(re.sub(r"[._]", "", key.lower()), current)
    return found


def _legacy_result(folder: Path, stem: str, old: str, item: str) -> tuple:
    """A result folder with no ticket from before the Page Run grammar: `re02_e02-<slug>` is
    Evidence Item E02's; `r03_…check…` / `…review…` is a check; `…setup…` is context."""
    evidence = re.match(r"^re\d+_e(\d+)-", old, re.I)
    if evidence:
        items = plan_dir(folder) / ("%s-evidence-items.md" % stem)
        text = items.read_text(encoding="utf-8", errors="replace") if items.is_file() else ""
        found = re.search(r"(?m)^#{3,4} (E%s-[A-Z]+-[\w-]+)" % evidence.group(1), text)
        item = item or (found.group(1) if found else "")
        return run_names.item_kind(item), item
    if re.match(r"^r\d+_", old):
        if re.search(r"check|review", old, re.I):
            return "check", item
        if re.search(r"setup|context", old, re.I):
            return "context", item
    return None, item


def _day(folder: Path, stem: str, ticket_text: str, ticket: Path):
    runtime = folder / "results" / stem / "runtime.yaml"
    for text in (_read(runtime), ticket_text):
        value = _field(text, "started_at", "started", "created_at", "created", "date")
        if re.search(r"\d{4}-\d{2}-\d{2}|^\d{6}$", value):
            return value
    dated = re.search(r"_(\d{6})$", stem)            # `r03_independent-check_260928`
    if dated:
        return dated.group(1)
    # Oldest file time of the ticket and its Result: a layout move rewrites the ticket
    # (so its own time reads as today), but `results/` is never edited.
    result = folder / "results" / stem
    files = [ticket] + ([p for p in result.rglob("*") if p.is_file()] if result.is_dir() else [])
    return dt.date.fromtimestamp(min(p.stat().st_mtime for p in files if p.exists()))


def _slug(kind: str, stem: str, ticket_text: str, item: str) -> str:
    suffix = stem.split("_", 1)[1] if "_" in stem else ""
    if kind in {"value", "citation", "display"}:
        return run_names.item_slug(item) if item else run_names.slugify(suffix)
    if kind in {"paragraph", "revise", "scratch"}:
        return run_names.target_slug(suffix or _field(ticket_text, "target"))
    goal = _field(ticket_text, "goal")
    suffix = re.sub(r"_\d{6}$", "", suffix)                      # drop a trailing date
    return run_names.slugify(goal or suffix or _field(ticket_text, "target")) or kind


def _aliases(old: str) -> list[str]:
    """Short forms that point at the same run: `pj06t14r01`, `p.j06.t14.r01`, `rp-para-14`, `re-value-07`."""
    out = []
    pj = _PJ.match(old)
    if pj:
        key = re.sub(r"[._]", "", pj.group(1).lower())
        parts = re.match(r"pj(\d+)t(\d+)r(\d+)", key)
        out += [key, "p.j%s.t%s.r%s" % parts.groups()]
    short = re.match(r"^((?:rp|re)-[a-z]+-\d+)[_-]", old)
    if short:
        out.append(short.group(1))
    return [a for a in out if a != old]


def plan(page) -> dict:
    """Every run on the Page with its new name; nothing is written."""
    folder, stem = _page(page)
    runs = folder / "runs"
    tickets: dict[str, list[Path]] = {}
    extras: list[Path] = []                 # `<run>.edited/` and the like: they move with their run
    for path in sorted(runs.rglob("*")) if runs.is_dir() else []:
        inside = path.relative_to(runs).parts
        if path.is_dir() and path.parent != runs and path.parent.name in SPACE_FOLDERS:
            extras.append(path)
        if not path.is_file() or path.name.startswith("."):
            continue
        if len(inside) > (2 if inside[0] in SPACE_FOLDERS else 1):
            continue                        # a file inside such a folder is not a ticket
        tickets.setdefault(path.stem, []).append(path)
    results = folder / "results"
    for path in sorted(results.iterdir()) if results.is_dir() else []:
        if path.is_dir() and path.name not in tickets:
            tickets[path.name] = []          # a result whose ticket is missing
    by_pj = _items_by_paper_run(folder, stem)
    taken = {s for s in tickets if run_names.is_run_name(s)}
    rows, kept = [], []
    candidates = []
    for old, paths in tickets.items():
        text = "\n".join(_read(p) for p in paths) or _read(folder / "results" / old / "runtime.yaml")
        if run_names.is_run_name(old):
            flat = [p for p in paths if p.parent != runs]
            if flat:
                rows.append({"old": old, "new": old, "tickets": paths, "note": "flatten only"})
            continue
        kind = run_names.kind_of(old)
        item = _field(text, "item") or _field(_read(folder / "results" / old / "result.yaml"), "item")
        pj = _PJ.match(old)
        if pj and not kind:
            item = item or by_pj.get(re.sub(r"[._]", "", pj.group(1).lower()), "")
            kind = run_names.item_kind(item)
        if kind is None and not paths:
            kind, item = _legacy_result(folder, stem, old, item)
        if kind in (None, "delivery"):
            # An older numbered build (rdNN_<lane>) stays as history: nothing reads it, and the lane's
            # one Delivery Run (run-delivery-<lane>) takes over (JL 260928).
            why = "older Delivery build, history" if kind == "delivery" else "not a Page Run"
            kept.append({"old": old, "why": why + ("; result has no ticket" if not paths else "")})
            continue
        anchor = paths[0] if paths else folder / "results" / old
        candidates.append((str(_day(folder, old, text, anchor)), old, kind, text, item, paths))
    for day, old, kind, text, item, paths in sorted(candidates, key=lambda c: (run_names.mmdd(c[0]), c[1])):
        new = run_names.mint(kind, _slug(kind, old, text, item), day=day, taken=taken)
        taken.add(new)
        rows.append({"old": old, "new": new, "tickets": paths, "kind": kind, "item": item,
                     "note": "" if paths else "result had no ticket; one is written"})
    from .page_export import RUN_NAMES, built_lanes
    fixed = [lane for lane in built_lanes(folder, stem) if RUN_NAMES[lane] not in tickets]
    by_old = {row["old"]: row for row in rows}
    for extra in extras:
        base = extra.name.split(".", 1)[0]
        if base in by_old:
            by_old[base].setdefault("extras", []).append(extra)
    return {"page": stem, "folder": folder, "moves": rows, "kept": kept, "fixed": fixed}


def _rewrite(folder: Path, names: dict[str, str], moved_up=()) -> int:
    """Replace every old name (and `runs/<space>/<old>`) in the Page's text files; a file that
    only moved up keeps its name, so only its `runs/<space>/` prefix goes."""
    kept = [re.sub(r"\.(md|sh|ps1)$", "", n) for n in moved_up]
    if not names and not kept:
        return 0
    olds = sorted(names, key=len, reverse=True)
    spaces = "|".join(re.escape(s) for s in SPACE_FOLDERS)
    alt = "|".join(re.escape(o) for o in sorted(set(olds) | set(kept), key=len, reverse=True))
    path_re = re.compile(r"runs/(?:%s)/(?=(?:%s)(?![A-Za-z0-9_-]))" % (spaces, alt))
    name_re = re.compile(r"(?<![A-Za-z0-9_-])(%s)(?![A-Za-z0-9_-])" % "|".join(re.escape(o) for o in olds)) if olds else None
    changed = 0
    for path in folder.rglob("*"):
        rel = path.relative_to(folder).parts
        if not path.is_file() or path.suffix not in TEXT or not rel or rel[0] in {"delivery", ".git"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        new = path_re.sub("runs/", text)
        new = name_re.sub(lambda m: names[m.group(1)], new) if name_re else new
        if new != text:
            path.write_text(new, encoding="utf-8")
            changed += 1
    return changed


def apply(page, *, dry_run: bool = False) -> dict:
    report = plan(page)
    if dry_run:
        return report
    folder = report["folder"]
    runs, results = folder / "runs", folder / "results"
    names = {}
    for row in report["moves"]:
        old, new = row["old"], row["new"]
        for ticket in row["tickets"]:
            target = runs / (new + ticket.suffix)
            if target.exists() and target != ticket:
                raise FileExistsError("%s already exists" % target.relative_to(folder))
            moved_up = ticket.parent != runs
            ticket.rename(target)
            if moved_up and target.suffix in {".sh", ".ps1"}:
                text = target.read_text(encoding="utf-8")
                fixed = _SCRIPT_DOWN.sub(r"\1/..\2", text)
                if fixed != text:
                    target.write_text(fixed, encoding="utf-8")
        for extra in row.get("extras", []):
            target = runs / (new + extra.name[len(old):])
            if target.exists():
                raise FileExistsError("%s already exists" % target.relative_to(folder))
            extra.rename(target)
        if old != new and (results / old).is_dir():
            if (results / new).exists():
                raise FileExistsError("results/%s already exists" % new)
            (results / old).rename(results / new)
        if not row["tickets"] and (results / new).is_dir():
            runs.mkdir(exist_ok=True)
            (runs / (new + ".md")).write_text(
                "---\nrun: %s\nkind: %s\nfamily: page\nstatus: closed\n%s---\n\n# %s\n\n"
                "- Written by page.py run-names on %s: results/%s/ had no ticket (was %s).\n"
                % (new, row.get("kind", ""), ("item: %s\n" % row["item"]) if row.get("item") else "",
                   new, dt.date.today().isoformat(), new, old), encoding="utf-8")
        if old != new:
            names[old] = new
            for alias in _aliases(old):
                names.setdefault(alias, new)
    counts = {}
    for row in report["moves"]:
        for alias in _aliases(row["old"]):
            counts[alias] = counts.get(alias, 0) + 1
    names = {k: v for k, v in names.items() if k in {r["old"] for r in report["moves"]} or counts.get(k) == 1}
    # Whatever still sits in a Space folder keeps its name and moves up: runs/ ends flat.
    flattened = []
    for space in SPACE_FOLDERS:
        for item in sorted((runs / space).iterdir()) if (runs / space).is_dir() else []:
            target = runs / item.name
            if target.exists():
                continue
            item.rename(target)
            flattened.append(item.name)
            if target.is_file() and target.suffix in {".sh", ".ps1"}:
                text = target.read_text(encoding="utf-8")
                fixed = _SCRIPT_DOWN.sub(r"\1/..\2", text)
                if fixed != text:
                    target.write_text(fixed, encoding="utf-8")
    report["flattened"] = flattened
    report["files_rewritten"] = _rewrite(folder, names, moved_up=flattened)
    from .page_export import docx_author, write_ticket
    for lane in report.get("fixed", []):          # each built lane gets its one Delivery Run ticket
        write_ticket(folder, lane, docx_author(folder, report["page"]) if lane == "word" else None)
    for space in SPACE_FOLDERS:
        path = runs / space
        if path.is_dir() and not any(path.iterdir()):
            path.rmdir()
    return report


def render(report: dict) -> str:
    lines = ["%s · %d run(s) renamed, %d kept" % (report["page"], len(report["moves"]), len(report["kept"]))]
    for row in report["moves"]:
        lines.append("  %-46s → %s%s" % (row["old"], row["new"], ("  (%s)" % row["note"]) if row.get("note") else ""))
    for row in report["kept"]:
        lines.append("  %-46s   kept · %s" % (row["old"], row["why"]))
    from .page_export import RUN_NAMES
    for lane in report.get("fixed", []):
        lines.append("  %-46s   + the lane's one Delivery Run (ticket)" % RUN_NAMES[lane])
    if "files_rewritten" in report:
        lines.append("  %d file(s) rewritten; rebuild delivery with page.py export" % report["files_rewritten"])
    return "\n".join(lines)
