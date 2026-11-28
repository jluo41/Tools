"""Shared Blueprint bands and independently authored Studio type requirements.

Band names and order come from the Work Blueprint's delivery/page-spec/studio-bands.json.
A type topic specifies its instances; a band does not require a type topic of its own.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

HOME = "examples/Project-Ladder/blueprint/b17_theme_work"     # the Block that defines the types


def studio_types(root: Path) -> dict:
    """Return {band digit: (emoji, name, holds)} in the shared registry's order."""
    path = Path(root) / HOME / "delivery/page-spec/studio-bands.json"
    if not path.is_file():
        return {}
    rows = json.loads(path.read_text(encoding="utf-8"))["bands"]
    return {row["band"][1]: (row["emoji"], row["name"], row.get("holds", "")) for row in rows}


def is_blueprint(block: Path) -> bool:
    """A Block that plans a tool: it sits in a Project's `blueprint/` folder."""
    return Path(block).parent.name == "blueprint"


# ── a type's requirements: the class its band's topics are instances of (JL 261127: "Just like the class and instance";
# "in the class, for the right content, it will be the describption ... the requirements, and in the studio instance,
# it will just be the real things") ──
# `<type topic>/elements.md`: `## <view>` is a top button, `### <tab>` a left tab under it; lines before the first
# heading are defaults. A view or tab has
#   what: / why: / from:   what it is, why it is there, where an instance gets it: also the right-click card's words
#   must:  then `- ` lines   what an instance must show there            check:   how to tell an instance meets it
#   mark:      a class (or key=value) on a live page (a Jobs page row), outlined there by focus.js `mark=`
#   page: / query: or file: / fragment:   a live page or SPACE file that shows it      show: / text:   a selector for it
#   `> ` lines             the pattern to follow there, as a tree: two spaces a level, `name/` a folder, names that are
#                          not fixed in 〈 〉, `  # note` a small word after the name
#   skills:    on a view: the skill folders (SPACE-relative, comma-separated) whose SKILL.md are its real left tabs
#   when:      the part is there only in this case (a skill that has a `ref/`); without the line every topic has it
#   instances: (a default)  the selector of the type's instance topics, where the same buttons and tabs are found
FIELDS = ("mark", "page", "query", "file", "fragment", "show", "text", "from", "what", "why", "check", "instances", "skills", "when")


def elements_of(topic: Path) -> list[dict]:
    """The requirements a type topic defines, in order: one dict per view (`tab` None) and per tab; [] when it has
    no elements.md."""
    path = Path(topic) / "elements.md"
    if not path.is_file():
        return []
    base, out, cur, view = {}, [], None, None
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        head = re.match(r"^(##|###)\s+(.+?)\s*$", line)
        if head:
            if head.group(1) == "##":
                view = head.group(2)
                cur = dict(base, name=view, view=view, tab=None, must=[], pattern=[])
            else:
                cur = dict(base, name=head.group(2), view=view, tab=head.group(2), must=[], pattern=[])
            out.append(cur)
            continue
        field = re.match(r"^(%s):\s*(.+?)\s*$" % "|".join(FIELDS), line)
        if field:
            (cur if cur is not None else base)[field.group(1)] = field.group(2)
        elif cur is not None and re.match(r"^- \S", line):
            cur["must"].append(line[2:].strip())
        elif cur is not None and re.match(r"^> ?\s*\S", line):
            cur["pattern"].append(line[1:].removeprefix(" ").rstrip())
    return out


def type_views(topic: Path) -> list[str]:
    """The top buttons of a type topic, in order, from its studio-views.json; [] when it has none."""
    import json
    try:
        return [v["name"] for v in json.loads((Path(topic) / "studio-views.json").read_text(encoding="utf-8"))["views"]]
    except (OSError, ValueError, KeyError, TypeError):
        return []


def _selector(mark: str) -> str:
    """focus.js's reading of one `mark=` word: a class, or key=value for [data-key="value"]."""
    m = re.fullmatch(r"([\w-]+)=([\w-]+)", mark)
    return f'[data-{m.group(1)}="{m.group(2)}"]' if m else ("." + mark if re.fullmatch(r"[\w-]+", mark) else "")


def element_view(topic: Path, root: Path) -> list:
    """[(name, url, False)] for the type's Elements view: each element shown live, laid out as an instance is."""
    from urllib.parse import parse_qsl, quote, urlencode
    from live import frame
    root, items = Path(root).resolve(), []
    for el in elements_of(topic):
        if el.get("file"):
            target = (root / el["file"]).resolve()
            if not target.is_file() or not target.is_relative_to(root):
                continue
            url = frame._file_url(target, root) + ("#" + quote(el["fragment"], safe="") if el.get("fragment") else "")
        elif el.get("page") and (root / el["page"]).is_dir():
            query = {"path": el["page"], "layout": "focus", **dict(parse_qsl(el.get("query", "")))}
            url = frame.ROUTE + "?" + urlencode(query) + ("&mark=" + quote(el["mark"], safe="=,") if el.get("mark") else "")
        else:
            continue
        items.append((el["name"], url, False))
    return items


def element_about(root: Path) -> list[dict]:
    """What a right-click says about a type's element, wherever it shows: {css, text, name, type, what, why, from}.
    A Jobs page row is found by its mark; a top button or a left tab by its name, in the type topic and in its
    instances, a tab only inside its own view (Folder under Structure is not Folder under Examples)."""
    out, home = [], Path(root) / HOME
    for topic in sorted(home.glob("s7[0-9]-studio-type-*/")):
        face = topic / f"{topic.name}.md"
        kind = re.search(r"(?m)^name:\s*(.+?)\s*$", face.read_text(encoding="utf-8", errors="ignore")) if face.is_file() else None
        views = type_views(topic)
        for el in elements_of(topic):
            words = {"name": el["name"], "type": kind.group(1) if kind else "", "what": el.get("what", ""),
                     "why": el.get("why", ""), "from": el.get("from", "")}
            css = el.get("show") or _selector(el.get("mark", ""))
            if css:                                          # on a real page: a Jobs page row, or a named selector
                out.append(dict(words, css=css, text=el.get("text") or (el["name"] if el.get("show") else "")))
            if el.get("view") not in views:
                continue
            here = [f'article[id="{topic.name}"]'] + ([el["instances"]] if el.get("instances") else [])
            if el.get("tab") is None:                        # a top button, in the type and its instances
                part = "[data-studio-view]"
            else:                                            # a left tab, inside its own view
                part = f'[data-studio-name="{el["view"]}"] .pb-item'
            out.append(dict(words, css=f':is({",".join(here)}) {part}', text=el["name"]))
    return out
