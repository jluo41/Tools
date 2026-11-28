"""Rebuild a version Job's Narrative rows from its Section plans (hai-paper ref/must-check.md M-D19).

While Sections draft, each Section's own plan is the truth for that Section (M-D09); the version's `## Narrative`
table (one row per Section, first cell the Task folder) is the starting version. When the Sections are good, one
step proposes new rows from the plans: the ordered moves (the plan's parts, or its paragraphs when it has one part,
each with the displays it calls), the displays, and the claims (`claim-ids:` on the plan, else on the Section face).
Only those three cells are rebuilt; the others are kept as written. `--apply` writes the rows into the Narrative
and removes `narrative-approved:` so the person signs it once with `page.py sign-narrative`. It never writes a
Section plan or the Story; the Story claim lines that would follow are printed for review only.
"""
from __future__ import annotations

import difflib
import re
from pathlib import Path

from .outline_version import latest_outline, plan_dir

REBUILT = {"ordered moves": "moves", "moves": "moves", "displays": "displays", "claims": "claims"}
PART = re.compile(r"^(?:-|#{2,3})\s+(C\d+)\s*·\s*(.+?)\s*$")
PARA = re.compile(r"^(?:-|#{3,4})\s+(C\d+)\.P\d+\s*·\s*(.+?)(?:\s*·\s*[Ss]\d+[a-z]*(?:\s+to\s+[Ss]\d+[a-z]*)?)?\s*$")
PARA_HEAD = re.compile(r"^#{3,4}\s+(C\d+)\.P\d+\s*·")
DISPLAY = re.compile(r"\bE\d+-DISPLAY-([a-z]+)(\d+)\b", re.I)
NAMES = {"fig": "Figure {}", "edf": "Extended Data Fig. {}", "edt": "Extended Data Table {}",
         "tab": "Table {}", "table": "Table {}"}
SHOWN = re.compile(r"(Extended Data (?:Fig\.?|Figure|Table)|Figure|Table)\s+(\d+)")


def _cells(line: str) -> list:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _row(cells: list) -> str:
    return "| " + " | ".join(cells) + " |"


def _face(job: Path) -> Path:
    job = Path(job).expanduser().resolve()
    return job if job.is_file() else job / f"{job.name}.md"


def narrative_table(text: str):
    """(header cells, {section: (line index, cells)}) for the `## Narrative` table whose first column is Section."""
    lines = text.splitlines()
    start = next((i for i, l in enumerate(lines) if re.match(r"^## Narrative\b", l)), None)
    if start is None:
        return None, {}
    header, rows = None, {}
    for i in range(start + 1, len(lines)):
        line = lines[i].strip()
        if line.startswith("## "):
            break
        if not line.startswith("|"):
            if header and rows:
                break
            continue
        cells = _cells(line)
        if header is None:
            if cells and cells[0].lower() == "section":
                header = [c.lower() for c in cells]
            continue
        if cells[0] and not set(cells[0]) <= set("-: "):
            rows[cells[0].strip("`")] = (i, cells)
    return header, rows


def _plain(title: str) -> str:
    """A title as a table cell: a `|` inside it (a caption's "Fig. 1 | Title") reads as a colon."""
    return re.sub(r"\s*\|\s*", ": ", title)


def _display_order(name: str) -> tuple:
    rank = next((k for k, w in enumerate(("Figure", "Table", "Extended Data Fig.", "Extended Data Table"))
                 if name.rsplit(" ", 1)[0] == w), 9)
    return rank, int(name.rsplit(" ", 1)[-1]) if name.rsplit(" ", 1)[-1].isdigit() else 0, name


def display_name(kind: str, n: str) -> str:
    return NAMES.get(kind.lower(), kind + " {}").format(n)


def claim_ids(text: str) -> list:
    """Claim ids a `claim-ids:` line states: each `·` item that opens with `C<N>` or `C<N> to C<M>`."""
    m = re.search(r"(?m)^claim-ids:\s*(.+)$", text or "")
    if not m:
        return []
    out = []
    for seg in m.group(1).split("·"):
        seg = re.sub(r"^\s*Story claims\s+", "", seg).strip()
        r = re.match(r"C(\d+)\s+to\s+C(\d+)\b", seg)
        if r:
            out += [f"C{k}" for k in range(int(r.group(1)), int(r.group(2)) + 1)]
        elif re.match(r"C\d+\b", seg):
            out.append(re.match(r"C\d+", seg).group(0))
    return sorted(set(out), key=lambda c: int(c[1:]))


def section_plan(folder: Path) -> dict | None:
    """{moves, displays, claims, parts} read from the Section's newest plan, or None when it has none."""
    plan = latest_outline(plan_dir(folder), folder.name)
    if plan is None:
        return None
    text = plan.read_text(encoding="utf-8", errors="ignore")
    body = re.split(r"(?m)^## \d+ · (?:Scratch|Draft)\b", text, maxsplit=1)[0]
    parts, paras, shows, current = {}, [], {}, None
    for line in body.splitlines():
        m = PARA.match(line)
        if m:
            if PARA_HEAD.match(line):
                current = m.group(1)
            if _plain(m.group(2)) not in [t for _, t in paras]:
                paras.append((m.group(1), _plain(m.group(2))))
            continue
        m = PART.match(line)
        if m:
            parts.setdefault(m.group(1), _plain(m.group(2)))
            continue
        for kind, n in DISPLAY.findall(line):
            if current:
                seen = shows.setdefault(current, [])
                name = display_name(kind, n)
                if name not in seen:
                    seen.append(name)
    def move(title, ids):
        calls = [d for i in ids for d in shows.get(i, []) if d.lower() not in title.lower()]
        calls = list(dict.fromkeys(calls))
        return title + (f" ({', '.join(calls)})" if calls else "")
    if len(parts) > 1:
        moves = [move(t, [c]) for c, t in parts.items()]
    else:
        moves = [move(t, []) for _, t in paras]
    displays = sorted({d for c in parts or shows for d in shows.get(c, [])}, key=_display_order)
    face = folder / f"{folder.name}.md"
    claims = claim_ids(text) or claim_ids(face.read_text(encoding="utf-8", errors="ignore") if face.is_file() else "")
    return {"plan": plan.name, "moves": " → ".join(moves), "displays": ", ".join(displays) or "none",
            "claims": ", ".join(claims) or "none", "parts": parts, "shows": shows}


def proposals(job: Path) -> list:
    """[(section, old row, new row, plan)] for each Narrative row whose Section folder has a plan."""
    face = _face(job)
    if not face.is_file():
        return []
    header, rows = narrative_table(face.read_text(encoding="utf-8", errors="ignore"))
    if not header:
        return []
    out = []
    for name, (_i, cells) in rows.items():
        plan = section_plan(face.parent / name) if (face.parent / name).is_dir() else None
        if plan is None:
            continue
        new = list(cells) + [""] * (len(header) - len(cells))
        for k, col in enumerate(header):
            if col in REBUILT:
                new[k] = plan[REBUILT[col]]
        out.append((name, _row(cells), _row(new[:len(header)]), plan))
    return out


def differing(job: Path) -> list:
    return [p for p in proposals(job) if p[1] != p[2]]


def _story_claims(job: Path) -> dict:
    from .folder_health import story_narrative
    story, _sface = story_narrative(_face(job).parent / "_")
    rows = {}
    for line in (story or "").splitlines():
        cells = _cells(line) if line.strip().startswith("|") else []
        if len(cells) > 1 and re.fullmatch(r"C\d+", cells[0]):
            rows[cells[0]] = cells[1]
    return rows


def _display_claims(text: str) -> dict:
    """{display name: {claim ids}} from the Narrative's `Claims to displays:` line."""
    m = re.search(r"Claims to displays:\s*(.+)", text)
    out = {}
    for seg in (m.group(1).split("·") if m else []):
        ids = set(re.findall(r"\bC\d+\b", seg.split("(")[0]))
        for kind, n in SHOWN.findall(seg):
            name = display_name({"Figure": "fig", "Table": "tab"}.get(kind, "edt" if "Table" in kind else "edf"), n)
            out.setdefault(name, set()).update(ids)
    return out


def claim_changes(job: Path, props: list) -> list:
    """[(claim id, Story line, the part heading that now states it, section)]: a part whose displays carry
    exactly one Story claim, worded differently from that claim. For review only."""
    story = _story_claims(job)
    owners = _display_claims(_face(job).read_text(encoding="utf-8", errors="ignore"))
    norm = lambda s: re.sub(r"[\W_]+", " ", s).strip().lower()
    out = []
    for name, _old, _new, plan in props:
        if len(plan["parts"]) < 2:
            continue
        for part, title in plan["parts"].items():
            sets = [owners.get(d, set()) for d in plan["shows"].get(part, [])]
            ids = set.intersection(*sets) if sets and all(sets) else set()
            if len(ids) == 1:
                cid = ids.pop()
                if cid in story and cid in plan["claims"].split(", ") and norm(story[cid]) != norm(title):
                    out.append((cid, story[cid], title, f"{name} {part}"))
    return out


def render(job: Path) -> str:
    face, props = _face(job), proposals(job)
    if not props:
        return f"{face.name}: no ## Narrative table with Section plans to rebuild from"
    lines = []
    for name, old, new, plan in props:
        if old == new:
            lines.append(f"= {name} · its row already matches {plan['plan']}")
            continue
        lines.append(f"~ {name} · rebuilt from {plan['plan']}")
        lines += list(difflib.unified_diff([old], [new], f"{face.name} ## Narrative", plan["plan"], lineterm="", n=0))
    changes = claim_changes(job, props)
    if changes:
        lines.append("~ Story claims that would follow (review only; sync-narrative never writes the Story)")
        for cid, was, now, where in changes:
            lines += [f"- {cid} | {was}", f"+ {cid} | {now}  ({where})"]
    lines.append(f"{len(differing(job))} row(s) differ; --apply writes them and leaves the Narrative to sign once "
                 "(page.py sign-narrative)")
    return "\n".join(lines)


def apply(job: Path) -> dict:
    """Write the rebuilt rows into the Narrative and mark it unsigned. Never signs."""
    face = _face(job)
    text = face.read_text(encoding="utf-8")
    _header, rows = narrative_table(text)
    lines = text.splitlines()
    changed = []
    for name, old, new, _plan in proposals(job):
        if old != new:
            lines[rows[name][0]] = new
            changed.append(name)
    if not changed:
        return {"ok": True, "changed": [], "message": "every row already matches its Section plan"}
    out = "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    cut = re.search(r"(?m)^## ", out)
    head, body = out[:cut.start()], out[cut.start():]
    head = re.sub(r"(?m)^(?:narrative-approved|story-at-sign):.*\n?", "", head)
    face.write_text(head + body, encoding="utf-8")
    return {"ok": True, "changed": changed,
            "message": f"wrote {len(changed)} row(s): {', '.join(changed)}; the Narrative is unsigned: "
                       "sign the Narrative once (page.py sign-narrative)"}
