"""Write a theme Block's `delivery/page-spec/<level>-elements.md` from its real example pages (JL 261118: "make all the possible element
out and then put it in the Elements"), one `# <type>` per example the face names (`ui-block:` ... lines, labelled by
`delivery/page-spec/example-types.json`), so the parts are read off the live page, never guessed.

    uv run --with beautifulsoup4 python ui_elements_harvest.py <theme Block> --base http://127.0.0.1:5694 [--level task]

Each type lists its Page frame, then one `## ` per view with its section bars and the row, mark, card, tab and
paragraph kinds that view holds, then Around the Work from its rail. A part's `folder:` notes already in the file are
kept. focus_ui_elements.py draws the result.
"""
from __future__ import annotations

import functools
import json
import re
import sys
import urllib.request
from pathlib import Path
from urllib.parse import quote

from bs4 import BeautifulSoup


def spec_dir(block: Path) -> Path:
    """The Block's page spec, delivery/page-spec/ (ui/ while only that exists); the same rule as live.page_spec,
    kept here so this script runs on its own."""
    new, old = block / "delivery" / "page-spec", block / "ui"
    return old if not new.is_dir() and old.is_dir() else new

ROUTE = "/_board/workbench"
REPORT = 'section.work-section-group[aria-label="Report content"]'
FRAME = (("Path", ".focus-crumb"), ("Title and section", "h1"), ("Type line", "dl.job-identity"),
         ("🙋 Waiting tray", "[popovertarget=wait-tray]"), ("View buttons", ".section-views"),
         ("Goal line", ".focus-goal"), ("Pages rail", "nav.focus-rail.left"), ("Sections rail", "nav.focus-rail.right"))
KINDS = (("Job row", "details.job-row"), ("Task and Run row", ".fold-row"), ("Run row", "ul.wk-runs li"),
         ("Marks", ".lc-marks"), ("Question card", ".lc-ask"), ("Left tab, right content", REPORT + " .pb-tabset"),
         ("Paragraph", "p > .im-marks"), ("Result tabs", ".focus-card > .focus-content .pb-tabset"),
         ("Run table", ".run-table"))
LEVELS = ("block", "job", "task", "run")
_NUM = lambda s: re.sub(r"^\d+\s*·\s*", "", s).strip()
# (each topic's title, the frame they share, the title cleaned): numbered fold bars, a draft Task's sections, a Run's
SECTIONS = ((f"{REPORT} details.band-sec > summary .bt", f"{REPORT} details.band-sec", lambda s: bar_name(s)),
            (f"{REPORT} h3.fd-h", f"{REPORT} section.fd-sec", _NUM),
            ("h3.focus-sub", "h3.focus-sub", lambda s: re.sub(r"\s*·\s*[^·]*$", "", _NUM(s)) or _NUM(s)))


def soup(base: str, path: str, query: str = "") -> BeautifulSoup:
    url = f"{base}{ROUTE}?layout=focus&path={quote(path)}" + (f"&{query}" if query else "")
    return BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")


def words(node) -> str:
    return re.sub(r"\s+", " ", node.get_text(" ")).strip()


def bar_name(text: str) -> str:
    text = re.sub(r"^\d+\s*·\s*", "", text).replace("☆", "").strip()
    return text if len(text) <= 40 else text[:38].rstrip(" ,;") + "…"


@functools.lru_cache(maxsize=None)
def harvest(base: str, ref: str) -> list:
    """[(view, [part lines])] for one example page."""
    page = soup(base, ref)
    groups = [("Page frame", [(n, {"show": s}) for n, s in FRAME if page.select_one(s) or "popover" in s])]
    views = [(re.sub(r"^\d+\s*·\s*", "", words(a)), re.search(r"group=([\w-]+)", a["href"])[1]) for a in page.select(".section-views a")
             if "group=" in a.get("href", "")]
    for name, group in views or [("Sections", "")]:
        v = soup(base, ref, f"section=report&group={group}") if group else page
        parts = []
        for pick, frame_sel, clean in SECTIONS:                       # one Section part per frame; its bars are topics
            topics = [clean(words(h)) for h in v.select(pick)]
            topics = [x for x in topics if x]
            if topics:
                parts.append(("Section", {"show": frame_sel, "topics": topics}))
        for label, sel in KINDS:
            if label == "Result tabs" and group:                          # a Run's result files; a view's tabs are its own
                continue
            if v.select_one(sel):
                parts.append((label, {"show": sel}))
        for p in parts:
            if group:
                p[1]["view"] = group
        if parts:
            groups.append((name, parts))
    around = []
    for a in page.select("nav.focus-rail.right a"):
        sec = re.search(r"section=([\w-]+)", a.get("href", ""))
        if sec and sec[1] != "report" and sec[1] not in [x[1]["view"].split("=")[1] for x in around]:
            around.append((words(a), {"show": ".focus-content", "view": f"section={sec[1]}"}))
    if around:
        groups.append(("Around the Work", around))
    return groups


def kept_notes(path: Path) -> dict:
    """{(type, view, part): [note lines]}: the `folder:`, `code:`, plain and `- ` lines already written."""
    notes, kind, view, part = {}, "", "", ""
    if not path.is_file():
        return notes
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            kind, view, part = line[2:].strip(), "", ""
        elif line.startswith("## "):
            view, part = line[3:].strip(), ""
        elif line.startswith("### "):
            part = line[4:].strip()
        elif part and line.strip() and not re.match(r"^(show|text|list|page|view|example|topic):", line):
            notes.setdefault((kind, view, part), []).append(line)
            notes.setdefault(("*", view, part), []).append(line) if (kind, view, part) == list(notes)[-1] else None
    return notes


def topic_pages(block: Path, base: str) -> dict:
    """{view: (pages with a Section there, {topic: pages it is on})} over every example page at every level: a topic
    on two or more pages is the view's own (fixed), on one page that page's own (free); a view on one page says neither."""
    face = (block / "board.md").read_text(encoding="utf-8")
    seen = {}
    for ref in re.findall(r"(?m)^ui-(?:block|job|task|run):\s*(\S+)\s*$", face):
        if ref.startswith("http"):
            continue
        for view, parts in harvest(base, ref):
            for name, fields in parts:
                if name == "Section":
                    n, count = seen.get(view, (0, {}))
                    for x in set(fields["topics"]):
                        count[x] = count.get(x, 0) + 1
                    seen[view] = (n + 1, count)
    return seen


def write(block: Path, base: str, level: str) -> Path:
    face = (block / "board.md").read_text(encoding="utf-8")
    refs = re.findall(rf"(?m)^ui-{level}:\s*(\S+)\s*$", face)
    labels = {}
    types = spec_dir(block) / "example-types.json"
    if types.is_file():
        labels = json.loads(types.read_text(encoding="utf-8")).get(level, {})
    path = spec_dir(block) / f"{level}-elements.md"
    notes = kept_notes(path)
    pages = [(labels.get(r) or r.rstrip("/").rsplit("/", 1)[-1], r, harvest(base, r)) for r in refs if not r.startswith("http")]
    seen = topic_pages(block, base)
    out = []
    for kind, ref, groups in pages:
        out += [f"# {kind}", f"example: {ref}", ""]
        for view, parts in groups:
            out += [f"## {view}", ""]
            for name, fields in parts:
                out.append(f"### {name}")
                for k, v in fields.items():
                    if k != "topics":
                        out.append(f"{k}: {v}")
                for n, topic in enumerate(fields.get("topics", []), 1):
                    pages_here, count = seen.get(view, (0, {}))
                    label = "" if pages_here < 2 else " · fixed" if count.get(topic, 0) > 1 else " · free"
                    out.append(f"topic: {n} · {topic}{label}")
                out += notes.get((kind, view, name)) or notes.get(("*", view, name), [])
                out.append("")
    path.write_text("\n".join(out), encoding="utf-8")
    return path


def main(argv: list) -> int:
    args = [a for a in argv if not a.startswith("--")]
    base = next((argv[i + 1] for i, a in enumerate(argv) if a == "--base"), "http://127.0.0.1:5694")
    only = next((argv[i + 1] for i, a in enumerate(argv) if a == "--level"), "")
    block = Path(args[0]).resolve()
    for level in LEVELS:
        if not only or level == only:
            print(write(block, base, level))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
