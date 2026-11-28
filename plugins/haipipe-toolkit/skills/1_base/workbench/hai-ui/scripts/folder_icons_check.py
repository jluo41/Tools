"""Check hai-ui A05 to A07: the Files pane's icons, parts and traces.

  A05  one icon table: no server module but side_pane/files_tree/file_icons.py maps a file suffix to an icon; .py is Python's mark;
       no module but page/parts_and_map/state_marks.py draws a state mark
  A06  the Files pane groups real paths as Block, Maintain: <kind>, Read-From and Touch; numbers are role-local positions
       and each parent path is relative to the SPACE (needs --url)
  A07  every trace file has its aim and plan (do, path, what) written; a closed one has its Check and Summary;
       a Block page with traces marks its files on the one tree, with no switch and no grey row titles (needs --url)

Run from the Tools-SPACE root:
  python3 plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/scripts/folder_icons_check.py [--url http://host:port]
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

import yaml

ROOT = Path.cwd()
SERVERS = ROOT / "plugins/haipipe-toolkit/servers"
ICONS = SERVERS / "workbench/side_pane/files_tree/file_icons.py"
SUFFIX_ICON = re.compile(r"""["']\.[a-z0-9]{1,10}["']\s*:\s*["'][^\w\s"'<]{1,4}["']""")
ROLES = {"Block": "block", "Maintain": "maintain", "Read-From": "readfrom", "Touch": "touch"}
KINDS = ("ServerUI", "Skills", "Block-Example", "Blueprint Blocks", "OneDrive")   # Maintain: <kind>, one part each


def check_one_table() -> list[str]:
    bad = []
    for path in SERVERS.rglob("*.py"):
        if "tests" in path.parts or path == ICONS:
            continue
        if SUFFIX_ICON.search(path.read_text(encoding="utf-8", errors="replace")):
            bad.append(f"A05 {path.relative_to(ROOT)}: its own suffix-to-icon table; use file_icons.file_icon")
    marks = SERVERS / "workbench/page/parts_and_map/state_marks.py"
    for path in SERVERS.rglob("*.py"):              # a state's drawn mark: one table too (JL 261126)
        if "tests" in path.parts or path == marks:
            continue
        if 'class="state-mark"' in path.read_text(encoding="utf-8", errors="replace"):
            bad.append(f"A05 {path.relative_to(ROOT)}: draws its own state mark; use state_marks.STATE_MARKS")
    text = ICONS.read_text(encoding="utf-8")
    if '".py": PYTHON_ICON' not in text or "#3776AB" not in text:
        bad.append("A05 file_icons.py: .py does not map to Python's own mark")
    return bad


def traces() -> list[Path]:
    return sorted(p for p in ROOT.glob("examples/**/trace/[0-9]*/[0-9]*_*.md"))


def check_traces() -> list[str]:
    bad = []
    for face in traces():
        rel = face.relative_to(ROOT)
        text = face.read_text(encoding="utf-8")
        try:
            meta = yaml.safe_load(text.split("---", 2)[1]) if text.startswith("---") else None
        except yaml.YAMLError:
            meta = None
        if not isinstance(meta, dict):
            bad.append(f"A07 {rel}: no front matter")
            continue
        if not meta.get("aim"):
            bad.append(f"A07 {rel}: no aim")
        plan = meta.get("plan") or []
        if not plan:
            bad.append(f"A07 {rel}: no plan")
        for item in plan:
            if not (isinstance(item, dict) and item.get("do") in ("add", "edit", "move", "delete")
                    and item.get("path") and item.get("what")):
                bad.append(f"A07 {rel}: a plan line without do, path and what: {item}")
        if meta.get("closed"):
            body = text.split("---", 2)[2]
            for part in ("Check", "Summary"):
                m = re.search(rf"^## {part}\n(.*?)(?=^## |\Z)", body, re.M | re.S)
                if not (m and m.group(1).strip()):
                    bad.append(f"A07 {rel}: closed with an empty ## {part}")
            for item in plan:   # a move names its new place in path: (from <old> in what:), so a closed one is on disk
                if isinstance(item, dict) and item.get("do") == "move" and not (ROOT / str(item.get("path", "")).rstrip("/")).exists():
                    bad.append(f"A07 {rel}: a closed move whose path is not on disk: {item.get('path')}")
    return bad


def panel(url: str, block: str) -> str:
    q = urllib.parse.urlencode({"path": block, "layout": "focus", "panel": "files"})
    with urllib.request.urlopen(f"{url}/_board/workbench?{q}", timeout=20) as r:
        return r.read().decode("utf-8", "replace")


def check_parts(html: str, block: str, root: Path = ROOT) -> list[str]:
    """Check rendered Files roles and source paths, independently of display position."""
    bad, seen = [], []
    parts = re.findall(r'<section class="(files-part\b[^"]*)"[^>]*>(.*?)</section>', html, re.S)
    for classes, body in parts:
        heading = re.search(r"<h3>(.*?)</h3>", body, re.S)
        title = unescape(re.sub(r"<[^>]+>", "", heading[1])).strip() if heading else ""
        role, _, kind = title.partition(": ")
        if (role not in ROLES or "files-" + ROLES[role] not in classes.split()
                or (kind not in KINDS if role == "Maintain" else bool(kind))):
            bad.append(f"A06 {block}: unrecognized Files role {title!r}")
            continue
        seen.append(title)
        role_name, role = role, title
        where = re.findall(r'<p class="files-where"[^>]*>(.*?)</p>', body, re.S)
        if not where or any(not unescape(p).strip() for p in where):
            bad.append(f"A06 {block}: {role} has no SPACE-relative parent path")
        for parent in where:
            parent = Path(unescape(parent).strip())
            if parent.is_absolute() or ".." in parent.parts:
                bad.append(f"A06 {block}: {role} parent path is not relative to the SPACE")
        sources = re.findall(r'data-(?:folder-path|path)="([^"]+)"', body)
        if not sources:
            bad.append(f"A06 {block}: {role} has no source-backed rows")
        for path in re.findall(r'data-folder-path="([^"]+)"', body):
            path = unescape(path)
            target = (root / path).resolve()
            if Path(path).is_absolute() or not target.is_relative_to(root.resolve()) or not target.is_dir():
                bad.append(f"A06 {block}: {role} folder is not a real SPACE directory: {path}")
        role = role_name
        if role == "Block" and block not in map(unescape, sources):
            bad.append(f"A06 {block}: Block part does not contain its owning folder")
        numbered = (re.findall(r'<li data-n="([^"]+)"', body) if role in ("Maintain", "Read-From") else
                    re.findall(r'<p class="files-where" data-n="([^"]+)"', body) if role == "Touch" else [])
        if role != "Block" and (not numbered or numbered != [str(n) for n in range(1, len(numbered) + 1)]):
            bad.append(f"A06 {block}: {role} row numbers do not follow their display order")
    if seen.count("Block") != 1:
        bad.append(f"A06 {block}: Files must contain one Block part")
    for role in dict.fromkeys(seen):
        if seen.count(role) > 1:
            bad.append(f"A06 {block}: Files repeats the {role} part")
    return bad


def check_pane(url: str) -> list[str]:
    bad = []
    blocks = sorted({f.parents[2].relative_to(ROOT).as_posix() for f in traces()}) or [
        "examples/Project-Ladder/blueprint/b17_theme_work"]
    for block in blocks:
        try:
            html = panel(url, block)
        except OSError as e:
            bad.append(f"A06 {block}: the Files panel did not open ({e})")
            continue
        bad += check_parts(html, block)
        if 'class="tm-data"' not in html and any((ROOT / block / "trace").glob("[0-9]*/[0-9]*_*.md")):
            bad.append(f"A07 {block}: traces but no marks on the Files tree")
        if "data-trace-view=" in html:
            bad.append(f"A07 {block}: a Files/Timeline switch; the marks belong on the one tree")
        if "className='sc-what'" in html or "__scopeWhat" in html:
            bad.append(f"A07 {block}: grey titles on folder rows; they belong on the hover card")
    return bad


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url", help="a running workbench, e.g. http://127.0.0.1:5623")
    a = ap.parse_args()
    bad = check_one_table() + check_traces() + (check_pane(a.url.rstrip("/")) if a.url else [])
    for line in bad:
        print("❗", line)
    print(f"{'❗' if bad else '✅'} folder icons: {len(traces())} trace files, {len(bad)} problems")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
