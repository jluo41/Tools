"""Check hai-ui A12: every section in a page's section menu shows its emoji, from one table.

  static  every section key a page's menu can hold (focus_render's rail, a theme's shared sections) has an emoji in
          servers/workbench/page/parts_and_map/section_icons.py
  --url   every example Block's live page: each item in its section menu (the title's ▾) starts with that emoji,
          a plain Block's menu and a theme Block's menu alike

Run from the Tools-SPACE root:
  python3 plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/scripts/section_icons_check.py [--url http://host:port]
Exit 0 when every rule holds; each failure is printed with ❗.
"""
from __future__ import annotations

import argparse
from html import unescape
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path.cwd()
WORKBENCH = ROOT / "plugins/haipipe-toolkit/servers/workbench"
TABLE = WORKBENCH / "page/parts_and_map/section_icons.py"
RAIL_FILES = (WORKBENCH / "page/block_index_page/focus_render.py", WORKBENCH / "page/job_task_views/work_frame.py")
RAIL_KEY = re.compile(r"""rail\.(?:append|insert)\((?:\w+,\s*)?\(\s*["'](\w+)["']""")   # focus_render's menu
SHARED = re.compile(r"(?ms)^SHARED = .*?^\)\)?$")                                    # a theme's shared sections
SHARED_KEY = re.compile(r"\(\s*'(\w+)',\s*'[^']+'\)")
MENU_ITEM = re.compile(r'role="menuitem" data-side-key="(\w+)"[^>]*>(.*?)</button>', re.S)


def table() -> dict:
    found = {}
    exec(compile(TABLE.read_text(encoding="utf-8"), str(TABLE), "exec"), found)
    return found["SECTION_ICONS"]


def check_static(icons: dict) -> list[str]:
    bad = []
    for path in RAIL_FILES:
        text = path.read_text(encoding="utf-8")
        keys = RAIL_KEY.findall(text) + [k for block in SHARED.findall(text) for k in SHARED_KEY.findall(block)]
        for key in keys:
            if key not in icons:
                bad.append(f"A12 {path.relative_to(ROOT)}: section `{key}` has no emoji in section_icons.py")
    return sorted(set(bad))


def blocks() -> list[Path]:
    return sorted(face.parent for face in (ROOT / "examples").glob("Project-*/*/b[0-9]*/board.md"))


def check_live(url: str, icons: dict) -> list[str]:
    bad = []
    for block in blocks():
        rel = block.relative_to(ROOT).as_posix()
        page = f"{url.rstrip('/')}/_board/workbench?" + urllib.parse.urlencode({"path": rel, "layout": "focus"})
        try:
            html = urllib.request.urlopen(page, timeout=30).read().decode("utf-8", "replace")
        except Exception as exc:                                     # a page that does not open is a failure too
            bad.append(f"A12 {rel}: page did not open ({exc})")
            continue
        for key, inner in MENU_ITEM.findall(html):
            text = unescape(re.sub(r"<[^>]+>", "", inner)).strip()
            if key == "files" and "<svg" in inner:                  # Files shows the folder mark (A05), not an emoji
                continue
            if key in icons and not text.startswith(icons[key]):
                bad.append(f"A12 {rel}: menu item `{text}` lacks {icons[key]}")
    return bad


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--url", help="a running workbench, e.g. http://127.0.0.1:5623")
    args = parser.parse_args()
    icons = table()
    bad = check_static(icons) + (check_live(args.url, icons) if args.url else [])
    for line in bad:
        print("❗", line)
    if not bad:
        print(f"✅ section icons: {len(icons)} sections" + (f", {len(blocks())} example Blocks" if args.url else ""))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
