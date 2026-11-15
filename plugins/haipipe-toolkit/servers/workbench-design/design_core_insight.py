"""What a design rests on: its evidence rows, the insight rule its `because:` line names,
the Design Handoff a page says, and the Insight Space.

Split out of design.py; design.py re-exports every name here."""
from __future__ import annotations

import html
import re
from pathlib import Path

from src.themes import theme_dirs

from live.design_core_base import _SIGNED, _TITLE, _nearest_board, _read
from live.insightboard import display_id


def _relocated(folder: Path, rel: str) -> Path | None:
    """A cited page whose Insight board has moved: found by its last three path parts
    (`1-F-full/FW01-send-salience/FW01-send-salience.md`) under the nearest Project's
    `insight/` world (or the old `insights/`). The register keeps its old path, so no
    released Run goes stale."""
    tail = "/".join(Path(rel).parts[-3:])
    for up in folder.parents:
        worlds = theme_dirs(up, "insight")
        if worlds:
            hits = sorted(h for world in worlds for h in world.glob(f"*/{tail}"))
            return hits[0].resolve() if hits else None
    return None


def _evidence_rows(folder: Path, item: dict) -> list[dict]:
    """Merge register evidence lines with the roles the item's Tickets pinned."""
    rows: dict[str, dict] = {}
    from live.design_actions import split_evidence
    for line in item["evidence"]:
        role, rel = split_evidence(line)
        rows[rel] = {"role": role, "path": rel, "file": (folder / rel).resolve(), "pinned": False}
    for run in item["runs"]:
        if run["status"] == "superseded":
            continue
        for ref in run["inputs"]:
            if ref["role"] in ("base", "feedback"):
                continue
            if ref["path"].startswith("scripts/config/"):
                continue
            row = rows.setdefault(ref["path"], {"role": ref["role"], "path": ref["path"],
                                                "file": ref["file"], "pinned": False})
            row["pinned"] = True
    out = []
    for row in rows.values():
        if not row["file"].is_file():
            row["file"] = _relocated(folder, row["path"]) or row["file"]
        text = _read(row["file"]) if row["file"].is_file() else ""
        signed = _SIGNED.search(text)
        row["exists"] = row["file"].is_file()
        row["name"] = Path(row["path"]).name
        row["signed"] = (f"signed ✅ {signed.group(2)}".strip() if signed and signed.group(1) == "✅"
                         else "unsigned ⬜" if signed else "")
        out.append(row)
    return out


# `because: W01-full · W1, W3` (or the older `FW02 · W1`): the insight rows a design acts on.
_BECAUSE = re.compile(r"^([DIKW]\d{2}-[a-z]+|[A-Z][DIKW]\d{2})\s*[·:\s]\s*([A-Z]\d+(?:\s*,\s*[A-Z]\d+)*)$")


def because_rule(item: dict) -> dict:
    """The one insight rule an item says it acts on: register line `because: FW02 · W1`.

    state is "rule" (found; `rule` holds its DO / DO NOT sentence), "unknown" (named
    but not on the cited page), "ai" (`because: none`, or built from the Brief only:
    an AI idea, not from an insight) or "unnamed" (built on evidence, no rule named).
    The page is looked up among the item's evidence first, then on the same Insight board."""
    raw = (item.get("because") or "").strip()
    out = {"state": "unnamed", "ref": raw, "page": None, "rule": None}
    if raw.lower() in ("none", "no insight", "-") or (not raw and item.get("basis") != "evidence-informed"):
        return {**out, "state": "ai"}
    hit = _BECAUSE.match(raw.split(";")[0].strip())
    if not hit:
        return out if not raw else {**out, "state": "unknown"}
    pid, rid = hit.group(1), re.split(r"\s*,\s*", hit.group(2))[0]
    out["ref"] = f"{pid} · {rid}"
    page = _cited_page(item, pid)
    if page is None:
        return {**out, "state": "unknown"}
    from live.design_actions import counsel_lines
    rule = next((r for r in counsel_lines(_read(page)) if r["id"] == rid), None)
    return {**out, "state": "rule" if rule else "unknown", "page": page, "rule": rule}


def because_words(item: dict) -> str:
    """The because line as plain text, for the csv: `FW02 · W1: DO run a factorial round …`."""
    b = item.get("because_rule") or because_rule(item)
    if b["state"] == "rule":
        return f'{b["ref"]}: {"DO" if b["rule"]["do"] else "DO NOT"} {b["rule"]["text"]}'
    return {"ai": "AI idea, not from an insight", "unnamed": ""}.get(b["state"], f'{b["ref"]} (not found)')


_HANDOFF_KEY = re.compile(r"^(FINDING|STRENGTH|BOUNDARY|CONSEQUENCE|OVERREACH)\s{2,}(.*)$")
_ROLE_WORDS = {"handoff": "signed insight", "evidence": "evidence", "inspiration": "inspiration",
               "reference": "reference", "avoid": "avoid"}


_LEVEL_WORD = {"D": "Data", "I": "Information", "K": "Knowledge", "W": "Wisdom"}
_INSIGHT_PAGE = re.compile(r"^([A-Z][DIKW]\d{2})-(.+)$")
_INSIGHT_REF = re.compile(r"\b([A-Z][DIKW]\d{2})\b")


def _partitions_of(board_root: Path) -> dict[str, str]:
    """`1-F-full` -> {"F": "full"}: the data cuts an Insight board declares by folder."""
    out = {}
    for folder in board_root.glob("*"):
        cut = re.match(r"^\d+-([A-Z])-(.+)$", folder.name)
        if cut and folder.is_dir():
            out[cut.group(1)] = cut.group(2)
    return out


def name_refs(escaped: str, page: Path) -> str:
    """Name the pages a finding cites, in already-escaped text:
    `(FK03 · K1, K3)` becomes `(no generative rule · K1, K3)`, `full-K03` on hover."""
    root = page.parent.parent.parent
    parts, names = _partitions_of(root), {}
    for folder in root.glob("*/*"):
        hit = _INSIGHT_PAGE.match(folder.name)
        if hit and folder.is_dir():
            names[hit.group(1)] = hit.group(2).replace("-", " ")
    return _INSIGHT_REF.sub(lambda m: (f'<span title="{display_id(m.group(1), parts)}">{html.escape(names[m.group(1)])}</span>'
                                       if m.group(1) in names else display_id(m.group(1), parts)), escaped)


def _handoff_says(text: str) -> dict:
    """FINDING and CONSEQUENCE of a Design Handoff block, continuation lines joined;
    falls back to the first line under ## Opening."""
    from live.design_actions import counsel_lines
    out = {"finding": "", "consequence": "", "counsel": counsel_lines(text)}
    key = None
    for line in text.splitlines():
        hit = _HANDOFF_KEY.match(line)
        if hit:
            key = hit.group(1).lower()
            if key in out:
                out[key] = hit.group(2).strip()
            continue
        if key in out and line.startswith("  ") and line.strip():
            out[key] += " " + line.strip()
        elif not line.startswith("  "):
            key = None
    if not out["finding"]:
        title = _TITLE.search(text)
        opening = re.search(r"(?ms)^## Opening\s*\n(.*?)(?=^## |\Z)", text)
        first = next((l.strip() for l in opening.group(1).splitlines() if l.strip()), "") if opening else ""
        # the opening line is a question on most pages; the title says what the page found
        out["finding"] = first if first and not first.endswith("?") else (title.group(1).strip() if title else first)
    return out


def _insight_space(items: list[dict], insight: dict) -> dict:
    """Insight Space: per item, the insights that support it; then what the board offers unused."""
    used: set[Path] = set()
    per_item = []
    for item in items:
        rows = []
        for r in item["evidence_rows"]:
            says = (_handoff_says(_read(r["file"])) if r["exists"] and r["role"] in ("handoff", "evidence")
                    else {"finding": "", "consequence": "", "counsel": []})
            rows.append({**r, **says, "word": _ROLE_WORDS.get(r["role"], r["role"])})
            if r["exists"]:
                try:
                    used.add(r["file"].resolve())
                except OSError:
                    pass
        per_item.append({"item": item, "rows": rows,
                         "needed": item["basis"] == "evidence-informed" and not rows})
    unused = []
    for board in insight["boards"]:
        for h in board["handoffs"]:
            page = Path(h["page"])
            if not page.is_absolute():
                page = Path(board["board"]) / page
            try:
                resolved = page.resolve()
            except OSError:
                continue
            if resolved not in used:
                unused.append({"title": h["title"], "name": page.name, "file": page,
                               "signed": h["signature"] if h["signed"] else ""})
    return {"items": per_item, "unused": unused}


def _board_page(board: Path | None, pid: str) -> Path | None:
    hits = sorted(board.glob(f"*/{pid}-*/{pid}-*.md")) if board else []
    return hits[0] if hits else None


def _cited_page(item: dict, pid: str) -> Path | None:
    """An insight page by its id: among the item's evidence first, then on the same board."""
    files = [r["file"] for r in item.get("evidence_rows", []) if r["exists"]]
    page = next((f for f in files if f.stem.startswith(pid + "-")), None)
    for f in files if page is None else ():
        page = _board_page(_nearest_board(f), pid)
        if page:
            break
    return page
