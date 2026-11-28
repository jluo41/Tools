"""A Markdown file as left tabs: one tab per `##` section, the section on the right (hai-studio A11: inside a topic
every view reads top-view-left-tab-right-content; a long file shown whole is a wall to scroll).

A view whose one item is a Markdown file with two or more sections is laid out this way by the page itself
(studio_views.read_views), so no topic copies a file into parts and a changed file shows on the next open. The tab
is the section's own heading. The text before the first section (the title and its lead) is the first tab, named by
the file's title, when it says more than the title. A Page Face (it has an Opening section) is never split: the
Page reader shows it as a Page. A view with several items keeps each file whole: its left is taken.
"""
import re
from pathlib import Path

FENCE = re.compile(r"^\s*(```|~~~)")
ATX = re.compile(r"^##\s+(.+?)\s*#*\s*$")
PAGE_FACE = re.compile(r"(?m)^## (?:🚪 )?Opening\s*$")


def _clean(title: str) -> str:
    return re.sub(r"[`*_]", "", re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", title)).strip()


def chunks(text: str, name: str = "") -> list[tuple[str, str]]:
    """[(title, markdown)] in order: the lead (when it says more than the title), then each `##` section."""
    lines = text.split("\n")
    start = 0
    if lines and lines[0].strip() == "---":                                   # front matter stays with the lead
        start = next((i + 1 for i in range(1, len(lines)) if lines[i].strip() == "---"), 0)
    heads, fence = [], False
    for i in range(start, len(lines)):
        line = lines[i]
        if FENCE.match(line):
            fence = not fence
            continue
        if fence:
            continue
        atx = ATX.match(line)
        under = lines[i + 1] if i + 1 < len(lines) else ""
        setext = (line.strip() and re.fullmatch(r"-{3,}\s*", under) and (i == 0 or not lines[i - 1].strip())
                  and not line.lstrip().startswith(("-", "|", "*", ">", "#")))
        if atx or setext:
            heads.append((i, _clean(atx.group(1) if atx else line)))
    if not heads:
        return []
    lead = lines[start:heads[0][0]]
    top = next((ln for ln in lead if ln.startswith("# ")), "")
    said = [ln for k, ln in enumerate(lead) if ln.strip() and ln != top and not re.fullmatch(r"={3,}\s*", ln)
            and not (k + 1 < len(lead) and re.fullmatch(r"={3,}\s*", lead[k + 1]))]
    over = next((lead[k] for k in range(len(lead) - 1) if lead[k].strip() and re.fullmatch(r"={3,}\s*", lead[k + 1])), "")
    out = [(_clean(top[2:] or over) or name or "Overview", "\n".join(lines[:heads[0][0]]).strip("\n"))] if said else []
    for n, (at, title) in enumerate(heads):
        end = heads[n + 1][0] if n + 1 < len(heads) else len(lines)
        out.append((title, "\n".join(lines[at:end]).strip("\n")))
    return out


def sections_of(path: Path) -> list[str]:
    """The tab names of a Markdown file worth splitting; [] for a Page Face, a short file, or one section."""
    path = Path(path)
    if path.suffix.lower() != ".md" or path.name.endswith(".mindmap.md"):
        return []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []
    if PAGE_FACE.search(text):
        return []
    names = [title for title, _ in chunks(text, path.stem)]
    return names if len(names) >= 2 else []


def section_text(text: str, n: int, name: str = "") -> str:
    """The n-th chunk's Markdown; the whole text when there is no such chunk."""
    parts = chunks(text, name)
    return parts[n][1] if 0 <= n < len(parts) else text
