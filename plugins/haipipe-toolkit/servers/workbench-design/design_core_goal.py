"""The design task: the Brief line that names a Design Folder, the venue in reader words,
the `{LINK}` slot, the board's design input, and the Goal Space counts.

Split out of design.py; design.py re-exports every name here."""
from __future__ import annotations

import re
from pathlib import Path

from host_paths import skill_dir

from live.design_core_base import _read


_TABLE_ROW = re.compile(r"^\s*\|(.+)\|\s*$")


def brief_page(board_root: Path | None) -> Path | None:
    """The Brief page under 0-BR-brief/: the list of what the board asks Design for."""
    if board_root is None:
        return None
    for page in sorted(Path(board_root).glob("0-BR-brief/*/*.md")):
        if page.name == f"{page.parent.name}.md":
            return page
    return None


def is_task_header(cells: list[str]) -> bool:
    """The Brief's design-task table names audience, job and venue in its header;
    an audience table elsewhere in the Brief is never read as the task list."""
    low = [c.strip().lower() for c in cells]
    return all(any(word in c for c in low) for word in ("audience", "job", "venue"))


def brief_rows(brief_text: str) -> list[dict]:
    """The Brief's list: one line per audience × job × venue, columns matched by header word.

    The first Markdown table whose header names ``audience``, ``job`` and ``venue`` is the list.  A
    ``folder`` cell of ``—`` or empty means no Design Folder exists yet; a
    ``designs`` cell says how many designs the line asks for.
    """
    rows: list[dict] = []
    header: list[str] | None = None
    for line in brief_text.splitlines():
        hit = _TABLE_ROW.match(line)
        if not hit:
            if header is not None and rows:
                break
            header = None
            continue
        cells = [c.strip() for c in hit.group(1).split("|")]
        if header is None:
            if is_task_header(cells):
                header = [c.lower() for c in cells]
            continue
        if all(set(c) <= set("-: ") for c in cells):
            continue
        row = {"id": "", "audience": "", "job": "", "venue": "", "folder": "", "designs": 0, "insight": "",
               "method": ""}
        for key, value in zip(header, cells):
            for name in ("audience", "job", "venue", "folder", "insight"):
                if name in key:
                    row[name] = value
            if "design" in key or "wanted" in key or "how many" in key:
                row["designs"] = int(value) if value.strip().isdigit() else 0
            if key in ("row", "id", "#", "line", "page"):
                row["id"] = value
            if "method" in key:                     # the one design method a page uses
                row["method"] = "" if value.strip() in ("—", "-", "–", "none", "(none)") else value.strip()
        if row["folder"] in ("—", "-", "–", "none", "(none)"):
            row["folder"] = ""
        row["folder"] = row["folder"].strip("`")
        row["insight"] = row["insight"].strip("`")
        if row["insight"] in ("—", "-", "–", "none", "(none)", "(board default)"):
            row["insight"] = ""
        if not row["id"]:
            row["id"] = f"R{len(rows) + 1}"
        rows.append(row)
    return rows


_VENUE_WORDS = {"sms": "SMS", "ui-card": "app card", "push": "push message", "email": "email"}


def venue_word(venue: str) -> str:
    """A Brief venue in reader words: sms -> SMS, ui-card -> app card."""
    venue = (venue or "").strip()
    return _VENUE_WORDS.get(venue.lower(), venue.replace("-", " "))


def design_title(row: dict) -> str:
    """A Design Folder's title as one plain phrase from its Brief line: 'Prescription review SMS for all patients'."""
    job = (row.get("job") or "").strip()
    head = " ".join(x for x in (job[:1].upper() + job[1:], venue_word(row.get("venue", ""))) if x) or "Design"
    audience = (row.get("audience") or "").strip()
    return f"{head} for {audience}" if audience else head


LINK_SLOT = "{LINK}"


def with_link(text: str) -> str:
    """Show `{LINK}` where the platform puts the link: right after the ask's colon, before
    the opt-out. The stored text is unchanged; a text that already carries
    `{LINK}` is shown as it is."""
    if not text or LINK_SLOT in text:
        return text
    stop = text.rfind("Reply STOP")
    colon = (text[:stop] if stop > 0 else text).rfind(":")
    return text if colon < 0 else text[:colon + 1] + " " + LINK_SLOT + text[colon + 1:]


# The design input: Theory of Design §2 says a design starts from an aim,
# constraints and resources. The board's `design-goal.md` states them once; a task
# section overrides a line; the venue profile gives the channel's own defaults.
_INPUT_BLOCKS = ("Aim", "Venue", "Rules", "Resources", "Leave out")
_VENUE_DIR = skill_dir("design") / "venue"
_VENUE_LABEL = {"length": "Length", "cta": "Call to action", "opt-out": "Opt-out", "personalization": "Personalization",
                "links": "Link", "language": "Reading level"}


def _input_sections(text: str) -> list[tuple[str, list[tuple[str, str, str]]]]:
    """ASCII doc -> [(title, [(key, value, source)])]; a title is a line underlined by --- or ===."""
    lines, out, i = text.splitlines(), [], 0
    while i < len(lines):
        nxt = lines[i + 1].strip() if i + 1 < len(lines) else ""
        if lines[i].strip() and re.fullmatch(r"[-=]{3,}", nxt):
            out.append((lines[i].strip(), []))
            i += 2
            continue
        m = re.match(r"^([A-Za-z][\w -]*?):\s*(.*?)\s*(?:<-\s*(.*))?$", lines[i])
        if m and out:
            out[-1][1].append((m.group(1).strip(), m.group(2).strip(), (m.group(3) or "").strip()))
        i += 1
    return out


def venue_defaults(venue: str) -> dict[str, str]:
    """`- **Length:** 160 chars ...` lines under a venue README's `## Constraints`."""
    path = _VENUE_DIR / f"venue-{(venue or '').strip().lower()}" / "README.md"
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8", errors="replace")
    part = text.split("## Constraints", 1)[1].split("\n## ", 1)[0] if "## Constraints" in text else ""
    return {m.group(1).strip().lower(): m.group(2).strip()
            for m in re.finditer(r"(?m)^-\s+\*\*(.+?):\*\*\s*(.+?)\s*$", part)}


def design_input(board: Path | None, folder: Path) -> dict:
    """The board's design input with this folder's overrides: {block: [(key, value, source)]}."""
    path = board / "design-goal.md" if board else None
    if not path or not path.is_file():
        return {"path": None, "blocks": {}}
    sections = _input_sections(path.read_text(encoding="utf-8", errors="replace"))
    blocks = {title: list(rows) for title, rows in sections if title in _INPUT_BLOCKS}
    for title, rows in sections:
        if title == f"Task · {folder.name}":
            for key, value, source in rows:
                for name, lines in blocks.items():
                    if any(k == key for k, _, _ in lines):
                        blocks[name] = [(k, value, source) if k == key else (k, v, s) for k, v, s in lines]
                        break
                else:
                    blocks.setdefault("Aim", []).append((key, value, source))
    return {"path": path, "blocks": blocks}


def _goal(folder: Path, board_root: Path | None, items: list[dict]) -> dict:
    """Goal Space: the Brief line that names this folder, and the counts against it."""
    brief = brief_page(board_root)
    rows = brief_rows(_read(brief)) if brief else []
    row = next((r for r in rows if r["folder"] == folder.name), None)
    sentence = ""
    if row:
        wanted = row["designs"]
        what = " ".join(x for x in (row["job"].strip(), venue_word(row["venue"])) if x)
        head = f"{wanted} {what} design{'s' if wanted != 1 else ''}" if wanted else f"{what} designs"
        sentence = f"{head} for {row['audience'].strip()}"
    return {"brief": brief, "row": row, "sentence": sentence, "insight": row["insight"] if row else "",
            "wanted": row["designs"] if row else 0, "registered": len(items),
            "ready": sum(1 for i in items if i.get("ready"))}
