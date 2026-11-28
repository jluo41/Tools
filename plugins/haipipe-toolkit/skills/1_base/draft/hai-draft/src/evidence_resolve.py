"""Does an Evidence Item's material exist: a VALUE's named files and value ids, a DISPLAY's Result or Run, a CITE's
key in the Page's Bib. One check for two readers: the Draft Lab's 📊 chips (workbench-task-draft draft_step_support.py)
and `page.py health` row `evidence-files` (support_health.py), so a 📊❗ on the page is a FAIL at the final gate
(ScalingGlucose t02_results 261118: E06, E10, E14 named a wrong SPACE path and health still passed)."""
from __future__ import annotations

import re
from pathlib import Path

ITEM_HEAD = re.compile(r"(?m)^###\s+(E\d+[a-z]?)-(VALUE|CITE|DISPLAY|TABLE)-(\S+)\s*(?:·\s*(.*))?$")
PATH = re.compile(r"(?<![\w/])((?:[\w.-]+/)+[\w.*-]+)")
VID = re.compile(r"\bV_[A-Za-z0-9_]*[A-Za-z0-9](?![\w*])")


def _field(body: str, name: str) -> str:
    m = re.search(r"(?mi)^-\s*\*\*" + re.escape(name) + r"\*\*\s*:\s*(.*?)\s*$", body)
    return m.group(1) if m else ""


def _items_file(task: Path) -> Path | None:
    found = sorted((task / "draft").glob("*-evidence-items.md")) if (task / "draft").is_dir() else []
    return found[0] if found else None


def evidence_items(task: Path) -> list:
    """[{id, kind, slug, label, targets, expected, verified, local_input, local_run}] in file order."""
    f = _items_file(Path(task))
    if not f:
        return []
    text = f.read_text(encoding="utf-8", errors="replace")
    heads = list(ITEM_HEAD.finditer(text))
    out = []
    for i, m in enumerate(heads):
        body = text[m.end():heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        out.append({"id": m.group(1), "kind": "DISPLAY" if m.group(2) == "TABLE" else m.group(2), "slug": m.group(3),
                    "label": _field(body, "Label") or (m.group(4) or "").split(" · ")[-1],
                    "targets": [t.strip() for t in re.split(r"[,;]", _field(body, "Target")) if t.strip()],
                    "expected": _field(body, "Expected"), "verified": _field(body, "Verified"),
                    "local_input": _field(body, "Local Input"), "local_run": _field(body, "Local Run")})
    return out


def _find(path: str, task: Path) -> Path | None:
    """A path an item names, read from the Section, its version, its Board, or any folder above (an item may name
    `examples-2-nn/...` from the SPACE root)."""
    path = path.rstrip(".,;:)")
    for base in [task, *task.parents][:9]:
        p = base / path
        if p.exists():
            return p
    return None


def _read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace") if p.is_file() and p.stat().st_size < 3_000_000 else ""
    except OSError:
        return ""


def resolve(it: dict, task: Path, bib: dict, result_items: set) -> dict:
    """{state: ok | miss, why: [...]} for one item: a VALUE's named files and value ids on disk; a DISPLAY's Result
    (results/<id>/ naming the item) or its named Run; a CITE's key in the Page's Bib."""
    why, ok = [], True
    if it["kind"] == "CITE":
        key = it["label"].strip()
        if key in bib:
            why.append(f"{key}: in the Bib ({bib[key]})")
        else:
            ok = False
            why.append(f"{key}: not in draft/evidence/bibex/*.bib")
        return {"state": "ok" if ok else "miss", "why": why}
    # a path has two folders or a file's extension ("mg/dL" is a unit, not a path)
    paths = list(dict.fromkeys(p for p in PATH.findall(it["expected"] + " " + it["local_input"]) if "*" not in p
                               and not p.startswith(("results/", "src/"))
                               and (p.count("/") >= 2 or re.search(r"\.[A-Za-z]\w{0,4}$", p))))
    found = {p: _find(p, task) for p in paths}
    # "and its models/grid_counts.csv": a short path is read beside the files named before it
    near = [q if q.is_dir() else q.parent for q in found.values() if q]
    for p in [p for p, q in found.items() if q is None and p.count("/") < 2]:
        found[p] = next((b / p for b in near if (b / p).exists()), None)
    for p, at in found.items():
        if at is None:
            ok = False
            why.append(f"not found: {p}")
    if it["kind"] == "DISPLAY":
        if it["id"] in result_items:
            why.insert(0, "its DISPLAY Result is in results/")
        elif not paths or not any(found.values()):
            ok = False
            why.insert(0, "no DISPLAY Result and no Run on disk")
        return {"state": "ok" if ok else "miss", "why": why or ["its Run is on disk"]}
    ids = list(dict.fromkeys(VID.findall(it["expected"])))
    if ids:
        files = [x for p in found.values() if p for x in ([p] if p.is_file() else sorted(p.glob("values.*")) + sorted(
            p.glob("result/values.*")) + sorted(p.glob("headline.txt")))]
        text = "".join(_read(x) for x in files)
        lost = [v for v in ids if not re.search(r"(?<![\w])" + re.escape(v) + r"(?![\w])", text)]
        if lost:
            ok = False
            why.append("value ids not in the named files: " + ", ".join(lost))
        else:
            why.append(f"{len(ids)} value id{'s' * (len(ids) != 1)} found")
    if not paths:
        ok = False
        why.append("names no file")
    elif ok:
        why.insert(0, "its files are on disk")
    return {"state": "ok" if ok else "miss", "why": why}


def bib_keys(task: Path) -> dict:
    """{key: key} of the Page's own Bib files (draft/evidence/bibex/*.bib); the page shows author-year names instead."""
    out = {}
    for bib in sorted((Path(task) / "draft" / "evidence" / "bibex").glob("*.bib")):
        for k in re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", bib.read_text(encoding="utf-8", errors="replace")):
            out[k] = k
    return out
