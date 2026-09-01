"""The item table · `outline/<stem>-items.md` · read, derive, count.

ONE module for the two surfaces that read the table (`cli/evidence-status.py`
writes the joined twin file; `src/page_phase.py` draws the strip), so the
ladder word a person sees is computed in one place. The grammar is
`haipipe-plugin-outline/ref/item-table.md`; the law it serves (JL 260901,
"evidence is linked to the runs!!!"): every evidence number is answered by a
RUN at a real tasks/ address; the run computes, the page interprets.

    LADDER    owed → bound → landed → folded → accepted  (+ stale · deferred · dropped · blocked)
    OUTCOMES  found · rerun · new-run · new-task · new-job · new-block · person · none
    CYCLES    SHAPE · SURVEY · LAND · EMBED · WRITE  (the OUTLINE part, then the DRAFT part)
"""
from __future__ import annotations

import re
from pathlib import Path

LADDER = ("owed", "bound", "landed", "folded", "accepted", "stale", "deferred", "dropped", "blocked")
EMOJI = {"owed": "⬜", "bound": "🔗", "landed": "🟢", "folded": "📌", "accepted": "✅",
         "stale": "⚠️", "deferred": "⏸", "dropped": "✖", "blocked": "⛔"}
OUTCOMES = ("found", "rerun", "new-run", "new-task", "new-job", "new-block", "person", "none")
CYCLES = ("SHAPE", "SURVEY", "LAND", "EMBED", "WRITE")
# the five marks a plan bullet may end with (haipipe-plugin-outline §📐)
MARKS = {"🎯": "aim", "📚": "cite", "📮": "probe", "🧮": "value", "🖼": "display"}

_REC_RE = re.compile(r"^###\s+(C\d+\.P\d+\.B\d+)\s*·\s*(.*)$")
_LABEL_RE = re.compile(r"^-\s+\*\*([^*]+?)\*\*\s*[:：]\s*(.*)$")


def repo_root(start: Path) -> Path:
    """The checkout root: the first ancestor holding pyproject.toml AND code/
    (the marker a script never creates, CLAUDE.md). Falls back to `start`."""
    for p in [start] + list(start.parents):
        if (p / "pyproject.toml").is_file() and (p / "code").is_dir():
            return p
    return start


def items_path(page_md: Path) -> Path:
    return page_md.parent / "outline" / f"{page_md.stem}-items.md"


def read_items(page_md: Path) -> dict:
    """-> {address: row} from outline/<stem>-items.md, {} when there is none.

    row = head · need · route · run · decide (the four authored labels, verbatim)
          + outcome · address · result (parsed from Run) · decision (parsed from Decide)
    """
    f = items_path(page_md)
    if not f.is_file():
        return {}
    rows, cur = {}, None
    for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
        m = _REC_RE.match(line)
        if m:
            cur = {"head": m.group(2).strip(), "need": "", "route": "", "run": "", "decide": ""}
            rows[m.group(1)] = cur
            continue
        if cur is None:
            continue
        m = _LABEL_RE.match(line)
        if m:
            key = m.group(1).strip().lower()
            if key in ("need", "route", "run", "decide"):
                cur[key] = m.group(2).strip()
    for r in rows.values():
        parts = [p.strip() for p in r["run"].split("·")]
        r["outcome"] = parts[0].lower() if parts and parts[0].lower() in OUTCOMES else ""
        rest = "·".join(parts[1:]) if len(parts) > 1 else ""
        # `<address> [· note] → <result file>`: the arrow is LAND's one append
        addr, _, result = rest.partition("→")
        r["address"] = addr.split("·")[0].strip()
        r["result"] = result.strip()
        d = r["decide"].lower()
        r["decision"] = ("make" if "☑" in d and "make" in d else
                         "defer" if "☑" in d and "defer" in d else
                         "drop" if "☑" in d and "drop" in d else "")
    return rows


def resolve(path_str: str, root: Path, page_dir: Path):
    """The result file a row points at, or None. Repo-relative first."""
    if not path_str:
        return None
    p = Path(path_str)
    for cand in ([p] if p.is_absolute() else [root / p, page_dir / p, Path.cwd() / p]):
        if cand.exists():
            return cand
    return None


def bullets(plan_text: str):
    """Walk the plan: (address, head, kind, refs, folded) for every bullet.

    A bullet is its `- B<n> ·` or `- S<n> ·` head line PLUS its folded
    continuation lines (`  Note: … 🎯 A1.1`): the end mark normally sits on the
    Note line, so a walker that reads heads alone finds no marks at all.
    `folded` is whether EMBED has appended an `Answered:` line. 🎯 annotates
    a bullet and never changes its evidence kind. S<n> and B<n> are ONE
    address, keyed canonically as B.
    """
    lines = plan_text.splitlines()
    c = p = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^## C(\d+)\b", line)
        if m:
            c, p = int(m.group(1)), 0; i += 1; continue
        m = re.match(r"^### C(\d+)\.P(\d+)\b", line)
        if m:
            c, p = int(m.group(1)), int(m.group(2)); i += 1; continue
        if re.match(r"^## Aims\b", line):
            break
        m = re.match(r"^- (?:\[[ xX]\] )?[BS](\d+)\s*·\s*(.*)$", line)
        if not m:
            i += 1; continue
        b, head = int(m.group(1)), m.group(2).strip()
        body, j = m.group(2), i + 1
        folded = False
        while j < len(lines) and lines[j].startswith("  ") and not lines[j].lstrip().startswith("- "):
            if lines[j].strip().startswith("Answered:"):
                folded = True
            body += " " + lines[j].strip(); j += 1
        i = j
        hit, hit_at = None, -1
        aim_hit, aim_at = None, -1
        for emo, kind in MARKS.items():
            at = body.rfind(emo)
            if at < 0:
                continue
            if kind == "aim":
                if at > aim_at:
                    aim_hit, aim_at = (emo, kind), at
                continue
            if at > hit_at:
                hit, hit_at = (emo, kind), at
        if hit is None and aim_hit is not None:
            hit, hit_at = aim_hit, aim_at
        if hit is None:
            yield f"C{c}.P{p}.B{b}", head, None, [], folded
            continue
        emo, kind = hit
        refs = re.findall(r"(?<![A-Za-z0-9-])(PP\d+(?:\.v\d+)?|Display\d+)", body[hit_at + len(emo):])
        yield f"C{c}.P{p}.B{b}", head, kind, refs, folded


def item_status(row, lane_ok: bool, lane_accepted: bool, folded: bool, page_accepted: bool,
                plan_mtime: float, root: Path, page_dir: Path) -> str:
    """One ladder word for one bullet. `row` is the table record or None.
    `lane_ok` / `lane_accepted` is what the lane itself says (a verified key, an
    answered card, a drawn unit) for pages the table does not cover."""
    if row is None:
        if lane_accepted or (lane_ok and page_accepted):
            return "accepted"
        return "landed" if lane_ok else "owed"
    if row["decision"] == "defer":
        return "deferred"
    if row["decision"] == "drop":
        return "dropped"
    if row["outcome"] == "none":
        return "blocked"
    result = resolve(row["result"], root, page_dir)
    landed = bool(result) or (row["outcome"] == "person" and lane_ok)
    if landed and folded:
        if page_accepted:
            return "accepted"
        if result and result.stat().st_mtime > plan_mtime + 60:
            return "stale"
        return "folded"
    if landed:
        return "landed"
    if row["address"] and row["decision"] == "make":
        return "bound"
    return "owed"


def cycle_now(approved: bool, rows: dict, statuses, n_marks: int) -> str:
    """The cycle the OUTLINE part is in, from the plan tick and the table alone."""
    if n_marks == 0:
        return "WRITE" if approved else "SHAPE"
    if not rows:
        return "SHAPE" if not approved else "SURVEY"
    if len(rows) < n_marks or any(r["decision"] == "" for r in rows.values()):
        return "SURVEY"
    if any(s in ("owed", "bound") for s in statuses):
        return "LAND"
    if any(s in ("landed", "stale") for s in statuses):
        return "EMBED"
    return "WRITE" if approved else "SHAPE"


def summarize(page_md: Path, plan: Path, lane=None) -> dict:
    """Counts for a strip: the table joined to the plan, no live server.

    `lane(kind, ref) -> (ok, accepted)` is optional: the outline tab's own
    disk join when the caller has it; without it a row lands only through its
    `→ <file>` pointer, which is the table's own law anyway.
    """
    plan_txt = plan.read_text(encoding="utf-8", errors="replace")
    page_txt = page_md.read_text(encoding="utf-8", errors="replace")
    approved = bool(re.search(r"^approved:\s*✅", plan_txt, re.M))
    page_accepted = bool(re.search(r"^accepted:\s*✅", page_txt, re.M))
    rows = read_items(page_md)
    root, page_dir = repo_root(page_md.parent), page_md.parent
    counts, statuses, n_marks = {w: 0 for w in LADDER}, [], 0
    for addr, _head, kind, refs, folded in bullets(plan_txt):
        if kind is None or kind == "aim":
            continue
        n_marks += 1
        ok, acc = lane(kind, (refs or [""])[0]) if lane else (False, False)
        st = item_status(rows.get(addr), ok, acc, folded, page_accepted,
                         plan.stat().st_mtime, root, page_dir)
        counts[st] += 1; statuses.append(st)
    return {"marks": n_marks, "rows": len(rows),
            "decided": sum(1 for r in rows.values() if r["decision"]),
            "counts": counts, "cycle": cycle_now(approved, rows, statuses, n_marks),
            "approved": approved}
