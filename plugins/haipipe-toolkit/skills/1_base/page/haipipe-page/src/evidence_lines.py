"""The evidence lines under a Page sentence: derived, never typed (JL 260928).

A Page sentence carries what backs it on `>` lines, one lane each:

    > Value: E12-VALUE-cohort-baselines · results/re-value-04_cohort-baselines/result.yaml
    > Citation: E25-CITE-score-validation-study · results/re-cite-01_…/result.yaml · luo2026mapping
    > Display: E13-DISPLAY-cohort-overview · results/re-display-02_cohort-overview/result.yaml
    > Supporting Run: b03j02t01r04 · r04_D_reg_VisitLBP_1stPair_agre_af14d_ols · Execution · E12-VALUE-cohort-baselines

Every fact is already recorded. The Draft's `## 1 · Structure` names each Bullet's
Evidence Items (its `Evidence:`, `Answered:` and `Drawn:` lines); the Evidence
Markdown binds each item to its Result (`Local Run … → results/…`) and names its
Supporting Runs. `page.py adopt` writes these lines from those records. A `>`
line that names no Evidence Item (a person's note, a review mark) is not derived
and stays as written. Deliverables never print any of them: md2tex drops every
`>` line and md2docx keeps only its own evidence comments.
"""
from __future__ import annotations

import re
from pathlib import Path

from .item_table import compact_global_run, read_items, repo_root, run_registry

LANE = {"VALUE": "Value", "CITE": "Citation", "DISPLAY": "Display", "TABLE": "Display"}
NAMED = re.compile(r"^\s*(?:Evidence|Answered|Drawn):\s*(E\d+-([A-Z]+)-[\w-]+)", re.M)
OWNED = re.compile(r"^>\s*(?:(?:Value|Citation|Display):\s*E\d+-[A-Z]+-[\w-]+|Supporting Run:)")
_BIB_KEY = re.compile(r"@\w+\s*\{\s*([^,\s]+)\s*,")


def _cite_keys(folder: Path, result: str) -> list[str]:
    """The citation keys a CITE Result supplies: its `payload.sources[].cite`, else
    the keys of its `payload.bibliography` file."""
    from .page_evidence import _result_document
    manifest = folder / result
    document = _result_document(manifest) if manifest.is_file() else {}
    payload = document.get("payload") if isinstance(document, dict) else None
    if not isinstance(payload, dict):
        return []
    keys = [str(s.get("cite", "")).strip().lstrip("@") for s in payload.get("sources") or []
            if isinstance(s, dict)]
    if not any(keys) and isinstance(payload.get("bibliography"), str):
        bib = manifest.parent / payload["bibliography"].replace("<resolved-result>/", "")
        if bib.is_file():
            keys = _BIB_KEY.findall(bib.read_text(encoding="utf-8", errors="replace"))
    return list(dict.fromkeys(k for k in keys if k))


def _supporting(declared: str) -> list[tuple[str, str]]:
    """`Execution · reuse · b03j02t01r04; Discovery · reuse · b01j01t04r01` → [(address, kind)]."""
    out = []
    for entry in (part.strip() for part in (declared or "").split(";")):
        parts = [p.strip() for p in entry.split("·")]
        compact = compact_global_run(parts[2]) if len(parts) >= 3 else ""
        if compact:
            out.append((compact, parts[0] or "Task"))
    return out


_COMPACT = re.compile(r"b(\d+)j(\d+)t(\d+)r(\d+)")


def _local_run_name(page_src: Path, compact: str, run_kind: str) -> str:
    """The Run's ticket stem looked up in the Page's own Project and world first.

    A compact address is not unique across a SPACE: `b01j01t01r01` is a census Run in
    one Project's `tasks/` and a Paper Run in another's `discoveries/` (REACH-SPACE
    261005), and the SPACE-wide registry keeps only one of them. An Execution Run lives
    in `tasks/`, a Discovery Run in `discoveries/`; '' when the Project has no single match.
    """
    match = _COMPACT.fullmatch(compact or "")
    if not match:
        return ""
    world = "discoveries" if run_kind.strip().lower().startswith("discovery") else "tasks"
    project = next((d for d in Path(page_src).resolve().parents
                    if (d / world).is_dir() and ((d / "project.yaml").is_file() or (d / "README.md").is_file())),
                   None)
    if project is None:
        return ""
    b, j, t, r = match.groups()
    hits = {p.stem for p in (project / world).glob(f"b{b}_*/j{j}_*/t{t}_*/runs/r{r}_*")
            if p.is_file() and not p.name.startswith(".")}
    return hits.pop() if len(hits) == 1 else ""


def derive(page_src: Path, blocks: list) -> dict[str, list[str]] | None:
    """Bullet address → its evidence lines, in the order the Bullet names its items,
    Supporting Run lines last. None when no Bullet names an Evidence Item: such a
    Draft predates the fields, and its Page's lines are left alone."""
    page_src = Path(page_src)
    named = {}
    for block in blocks:
        text = "\n".join([block.get("body") or ""] + list(block.get("continuation") or []))
        named[block["address"]] = list(dict.fromkeys(NAMED.findall(text)))
    if not any(named.values()):
        return None
    items = read_items(page_src)
    registry = run_registry(str(repo_root(page_src.parent)))
    out: dict[str, list[str]] = {}
    for address, names in named.items():
        lines, runs = [], {}
        for full, kind in names:
            row = items.get(full) or {}
            result = str(row.get("result") or "").strip().strip("`")
            if row.get("decision") in {"drop", "defer"} or not result or not LANE.get(kind):
                continue
            line = "> %s: %s · %s" % (LANE[kind], full, result)
            if kind == "CITE":
                keys = _cite_keys(page_src.parent, result)
                line += (" · " + ", ".join(keys)) if keys else ""
            lines.append(line)
            for compact, run_kind in _supporting(row.get("supporting_runs", "")):
                runs.setdefault(compact, (run_kind, []))[1].append(full)
        for compact, (run_kind, fed) in runs.items():
            name = _local_run_name(page_src, compact, run_kind)
            if not name:
                ticket = (registry.get(compact) or {}).get("ticket", "")
                name = Path(ticket).stem if ticket else ""
            lines.append("> Supporting Run: %s%s · %s · %s"
                         % (compact, (" · " + name) if name else "", run_kind, ", ".join(fed)))
        out[address] = lines
    return out


def owned(line: str, cite_keys: set[str] = frozenset()) -> bool:
    """Is this `>` line one `derive` writes? Also a hand `> Citation: <key> · …` line whose
    key a derived Citation line now carries, so one source is not cited twice."""
    stripped = line.strip()
    if OWNED.match(stripped):
        return True
    hand = re.match(r"^>\s*Citation:\s*([^·]+?)\s*(?:·|$)", stripped)
    return bool(hand and hand.group(1) in cite_keys)


def cite_keys_of(lines: list[str]) -> set[str]:
    keys = set()
    for line in lines:
        if line.startswith("> Citation:"):
            parts = [p.strip() for p in line.split("·")]
            if len(parts) >= 3:
                keys.update(k.strip() for k in parts[2].split(","))
    return keys
