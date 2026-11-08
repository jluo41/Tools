"""Does a theme's placeholder Block show all of its UI? (JL 261105: "based on the blocks in the blueprints, we can see all
the UI what will be applied to others. This is the prototype.")

Walks the placeholder Block and every Job and Task under it on a running workbench: every section on the right rail,
every view of each, and lists each place the page shows an empty state ("Nothing … yet", "No … yet", a section word
"nothing yet") instead of content. On the prototype every one of them is a gap: fill it with placeholder content
made by its generator (a ticket, collect.py, a delivery), never by hand.

    python prototype_coverage.py <origin> <path from the served root> [--sections report,work,studio,delivery,interactions]
    python prototype_coverage.py http://127.0.0.1:5602 Tools/blueprints/Project-Ladder/work/b90_example_paper_results

Standard library only. Exit 0 when nothing is empty, 1 when there are gaps.
"""
from __future__ import annotations

import argparse
import html
import re
import sys
import urllib.parse
import urllib.request

EMPTY = re.compile(r"class=\"?mut\"?[^>]*>\s*((?:Nothing|No |Not )[^<]{0,90})")   # an empty state starts a sentence: a
#                                                         lowercase "no two alike" label is not one (261108)   # a bar's state word repeats its body
ASKED = "Nothing asked yet."         # a view's own 🙋 with no item: covered when any page shows a form (JL 261105-06)
VIEW = re.compile(r'class="section-views.*?</nav>', re.S)
GROUP = re.compile(r'group=([A-Za-z0-9_-]+)')
CHILD = re.compile(r'path=([^&"]+)')


def get(origin: str, path: str, section: str = "", group: str = "") -> str:
    q = {"layout": "focus", "path": path}
    if section:
        q["section"] = section
    if group:
        q["group"] = group
    url = f"{origin}/_board/workbench?{urllib.parse.urlencode(q)}"
    with urllib.request.urlopen(url, timeout=60) as r:
        return r.read().decode("utf-8", errors="replace")


def views(page: str) -> list:
    bar = VIEW.search(page)
    return list(dict.fromkeys(GROUP.findall(bar.group(0)))) if bar else [""]


def children(origin: str, path: str) -> list:
    """The Jobs and Tasks under the Block, from the page's own links (jNN_ then tNN_ folders one level down each)."""
    page = get(origin, path, "work")
    found = set()
    for ref in CHILD.findall(page):
        ref = urllib.parse.unquote(html.unescape(ref))
        rest = ref[len(path):].strip("/") if ref.startswith(path + "/") else ""
        parts = rest.split("/") if rest else []
        if parts and re.match(r"j\d+_", parts[0]):
            found.add(f"{path}/{parts[0]}")
            if len(parts) > 1 and re.match(r"t\d+_", parts[1]):
                found.add(f"{path}/{parts[0]}/{parts[1]}")
    return sorted(found)


def gaps(origin: str, path: str, sections: list) -> tuple:
    """(empty places, the (section, view) pairs the page has)."""
    out, seen = [], set()
    for section in sections:
        first = get(origin, path, section)
        for group in views(first):
            page = get(origin, path, section, group) if group else first
            main = page.split('class="focus-card', 1)[-1]
            seen.add((section, group or "-"))
            for msg in dict.fromkeys(m.strip() for m in EMPTY.findall(main)):
                out.append((section, group or "-", html.unescape(msg)))
    return out, seen


def level(rel: str) -> str:
    """Block, Job or Task, from the page's path under the prototype."""
    return {0: "Block", 1: "Job"}.get(len([p for p in rel.split("/") if p]), "Task")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("origin")
    ap.add_argument("path")
    ap.add_argument("--sections", default="report,work,studio,delivery,interactions")
    a = ap.parse_args()
    sections = a.sections.split(",")
    found = {}
    for page in [a.path] + children(a.origin, a.path):
        found[page[len(a.path):].strip("/")] = gaps(a.origin, page, sections)
    # a place empty here but shown filled on another page of the same level is covered: the prototype shows that part
    # once (JL 261105: "we can see all the UI"), so a form need not sit on every page
    any_form = any(sec == "interactions" and grp == "waiting" and not any(m.startswith("Nothing") for s2, g2, m in rows
                   if (s2, g2) == (sec, grp)) for _, (rows, seen) in found.items() for sec, grp in seen)

    def shown_elsewhere(rel, sec, grp, msg):           # another page of this level shows this view without this empty place
        if msg == ASKED and any_form:
            return True
        return any(level(other) == level(rel) and other != rel and (sec, grp) in seen
                   and (sec, grp, msg) not in set(rows) for other, (rows, seen) in found.items())

    total = 0
    for rel, (rows, _) in found.items():
        real = [(sec, grp, msg) for sec, grp, msg in rows if not shown_elsewhere(rel, sec, grp, msg)]
        covered = len(rows) - len(real)
        total += len(real)
        name = rel or "(the Block)"
        print(f"{name}: {'✅ nothing empty' if not real else f'{len(real)} empty'}"
              + (f" · {covered} shown filled on another {level(rel)}" if covered else ""))
        for sec, grp, msg in real:
            print(f"   {sec} · {grp} · {msg}")
    print(f"\n{'✅ the prototype shows every part' if not total else f'❌ {total} empty places: fill each with placeholder content'}")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
