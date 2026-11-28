"""Check hai-ui A08: a UI preview topic is looked at on an example Block's live page.

A UI preview topic is a Studio topic folder sNN-<slug>/ whose face sNN-<slug>.md says `**Delivery type:** ui`.
Its page sNN-<slug>.html lists its views, one <button data-src="..."> each:
  live view   data-src="/_board/workbench?..."  (origin-relative; the server renders an example Block)
  quick view  data-src="<a file next to the page>" (an html in delivery/ui/)

  A08  every UI preview topic under examples/ has a page with at least one live view;
       a live view names no host; every quick view's file exists; two live views never share one address
       (views of one page differ by their mark=, the part each outlines).
Whether a quick view's design is in the code yet cannot be read from files, so it is not checked.

Run from the Tools-SPACE root:
  python3 plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/scripts/ui_preview_check.py [examples/<sub>]
One line per problem with ❗, then a final line; exit 1 on any problem.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path.cwd()
LIVE = "/_board/workbench?"
FACE_UI = re.compile(r"^\*\*Delivery type:\*\*\s*`?ui`?\s*$", re.M)
TOPIC = re.compile(r"^s\d\d-")
BUTTON = re.compile(r"<button\b([^>]*\bdata-src=\"([^\"]+)\"[^>]*)>([^<]*)</button>")


def ui_topics(base: Path):
    for face in sorted(base.rglob("s[0-9][0-9]-*.md")):
        topic = face.parent
        if face.stem != topic.name or not TOPIC.match(topic.name):
            continue
        if FACE_UI.search(face.read_text(encoding="utf-8", errors="replace")):
            yield topic


def check_topic(topic: Path) -> list[str]:
    rel = topic.relative_to(ROOT)
    page = topic / (topic.name + ".html")
    if not page.is_file():
        return [f"A08 {rel}: no page {page.name}, so no live view"]
    bad, live, seen = [], 0, {}
    for _attrs, src, label in BUTTON.findall(page.read_text(encoding="utf-8", errors="replace")):
        label = label.strip()
        if src.startswith(LIVE):
            live += 1
            key = src.replace("&amp;", "&")
            if key in seen:
                bad.append(f"A08 {rel}: views {seen[key]!r} and {label!r} open the same address; give each its mark=")
            seen.setdefault(key, label)
        elif re.match(r"(?i)^[a-z]+:|^//", src):
            bad.append(f"A08 {rel}: view {label!r} names a host ({src}); a live view is origin-relative")
        elif not (page.parent / src.split("?")[0].split("#")[0]).is_file():
            bad.append(f"A08 {rel}: quick view {label!r} names {src}, which is not there")
    if not live:
        bad.append(f"A08 {rel}: no live view (no data-src starting with {LIVE})")
    return bad


def main(argv: list[str]) -> int:
    base = ROOT / (argv[0] if argv else "examples")
    if not base.is_dir():
        print(f"❗ {base} is not a folder; run from the Tools-SPACE root")
        return 1
    topics = list(ui_topics(base))
    problems = [p for t in topics for p in check_topic(t)]
    for p in problems:
        print("❗", p)
    print(f"{'❗' if problems else '✅'} A08: {len(topics)} UI preview topics, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
