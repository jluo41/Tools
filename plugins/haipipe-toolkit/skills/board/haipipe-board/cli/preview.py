#!/usr/bin/env python3
"""One screen: what a board, a group, or a page SAYS right now.

The three strips answer WHERE (`pagestatus.py` a group, `pagephase.py` a
phase, `pagecontext.py` the related-page packet); none answers WHAT. This
tool prints the summary surfaces the contracts already require — a page's
title, Opening visible paragraph, Aims joined to States; a board's spine,
Topic paragraph and roster — so a reader knows what the thing claims
before opening it. It reads files and never writes.

Three grains, resolved from what the path is:

    a page file or page folder    the full page preview
    a group folder                one compact line per page
    a board folder (board.md)     spine + Topic + every group's lines

Preview is a gist, not a read: WORK ON still owes the whole-file read its
step 1 names. The Opening's visible paragraph IS the page's self-summary
by contract (haipipe-page §✍️), which is why this tool can exist at all.

    python3 preview.py <board | group | page> [more ...]
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys


SKIP_DIRS = {"board", "fig"}
MARKERS = "✅🟡🔨⬜❌"


def page_dirs(group: pathlib.Path) -> list[pathlib.Path]:
    return sorted(d for d in group.iterdir()
                  if d.is_dir() and not d.name.startswith(("_", "."))
                  and (d / f"{d.name}.md").exists())


def groups_of(board: pathlib.Path) -> list[pathlib.Path]:
    return sorted(d for d in board.iterdir()
                  if d.is_dir() and not d.name.startswith(("_", "."))
                  and d.name not in SKIP_DIRS and page_dirs(d))


def sections(text: str) -> tuple[str, dict[str, str]]:
    """head (everything before the first ##) and each ## section's body."""
    parts = re.split(r"(?m)^## ", text)
    head, out = parts[0], {}
    for part in parts[1:]:
        name, _, body = part.partition("\n")
        out[name.strip()] = body
    return head, out


def visible_paragraph(body: str) -> list[str]:
    """The Opening's visible paragraph: the lines above the first blank line."""
    lines = []
    for line in body.strip("\n").split("\n"):
        if not line.strip():
            break
        lines.append(line.rstrip())
    return lines


def subheads(body: str) -> list[str]:
    return [m.group(1).strip() for m in re.finditer(r"(?m)^### (.+)$", body)]


def state_rows(body: str) -> dict[str, list[str]]:
    """Aim id -> its state lines, from the ## States section."""
    rows: dict[str, list[str]] = {}
    for m in re.finditer(r"(?m)^### (\S+)[^\n]*\n((?:(?!^###)[^\n]*\n?)*)", body):
        aim_id = m.group(1)
        for line in m.group(2).split("\n"):
            line = line.strip().lstrip("- ").strip()
            if line:
                rows.setdefault(aim_id, []).append(line)
    return rows


def clip(s: str, n: int = 160) -> str:
    return s if len(s) <= n else s[: n - 2].rstrip() + " …"


def preview(path: pathlib.Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    head, secs = sections(text)
    out = []

    title = next((ln for ln in head.split("\n") if ln.startswith("# ")), "# (no title)")
    ptype = re.search(r"(?m)^page-type:\s*(\S+)", head)
    ident = f"{path.stem} · {ptype.group(1) if ptype else 'type by filename'} · {len(text.splitlines())} lines"
    out += [ident, title[2:].strip(), ""]

    opening = visible_paragraph(secs.get("Opening", ""))
    if opening:
        out.append("⚡ Opening")
        out += [f"   {ln}" for ln in opening]
        out.append("")

    aims, states = subheads(secs.get("Aims", "")), state_rows(secs.get("States", ""))
    if aims:
        out.append("🎯 Aims → States")
        for aim in aims:
            aim_id = aim.split(" ")[0]
            rows = states.get(aim_id, ["(no state row)"])
            more = f"  (+{len(rows) - 1} more rows)" if len(rows) > 1 else ""
            out.append(f"   {aim}  —  {clip(rows[0])}{more}")
        out.append("")

    divisions = subheads(secs.get("Content", ""))
    if divisions:
        out.append("📑 Content")
        out += [f"   {d}" for d in divisions]
        out.append("")

    tail = []
    diagram = secs.get("Outline", secs.get("Diagram", ""))
    if diagram.strip():
        tail.append(f"🧭 outline map {len(diagram.strip().splitlines())} lines")
    files = [ln for ln in secs.get("Files", "").split("\n") if ln.strip().startswith(("-", "|"))]
    if files:
        tail.append(f"📂 {len(files)} file rows")
    log_rows = [ln.strip() for ln in secs.get("Log", "").split("\n") if ln.strip() and not ln.strip().startswith("#")]
    if log_rows:
        tail.append(f"🕰 {clip(log_rows[-1])}")
    if tail:
        out.append(" · ".join(tail))
    return "\n".join(out).rstrip() + "\n"


def page_line(md: pathlib.Path, w: int = 24) -> str:
    """One compact roster line: id, type, state tally, title."""
    text = md.read_text(encoding="utf-8", errors="ignore")
    head, secs = sections(text)
    title = next((ln[2:].strip() for ln in head.split("\n") if ln.startswith("# ")), "(no title)")
    title = re.sub(r"^\S+ · ", "", title)  # the id repeats the folder name
    ptype = re.search(r"(?m)^page-type:\s*(\S+)", head)
    tally = {}
    for rows in state_rows(secs.get("States", "")).values():
        for row in rows:
            if row and row[0] in MARKERS:
                tally[row[0]] = tally.get(row[0], 0) + 1
    marks = " ".join(f"{m}{n}" for m, n in sorted(tally.items(), key=lambda kv: MARKERS.index(kv[0]))) or "—"
    return f"{md.stem:<{w}} {ptype.group(1) if ptype else '·':<11} {marks:<8} {clip(title, 66)}"


def preview_group(group: pathlib.Path) -> str:
    pages = page_dirs(group)
    out = [f"{group.name} · {len(pages)} pages", ""]
    w = max(len(d.name) for d in pages) + 1
    out += [f"   {page_line(d / (d.name + '.md'), w)}" for d in pages]
    return "\n".join(out) + "\n"


def preview_board(board: pathlib.Path) -> str:
    text = (board / "board.md").read_text(encoding="utf-8", errors="ignore")
    head, secs = sections(text)
    title = next((ln[2:].strip() for ln in head.split("\n") if ln.startswith("# ")), "(no title)")
    dialect = re.search(r"(?m)^dialect:\s*(\S+)", head)
    close = re.search(r"(?m)^close:\s*(.+)$", head)
    groups = groups_of(board)
    npages = sum(len(page_dirs(g)) for g in groups)
    out = [f"{board.name} · dialect {dialect.group(1) if dialect else '·'} · {npages} pages",
           title, ""]
    topic = visible_paragraph(secs.get("Topic", ""))
    if topic:
        out.append("⚡ Topic")
        out += [f"   {ln}" for ln in topic]
        out.append("")
    w = max((len(d.name) for g in groups for d in page_dirs(g)), default=24) + 1
    for g in groups:
        out.append(f"📋 {g.name}")
        out += [f"   {page_line(d / (d.name + '.md'), w)}" for d in page_dirs(g)]
        out.append("")
    if close:
        out.append(f"🎯 close: {clip(close.group(1))}")
    log_rows = [ln.strip() for ln in secs.get("Log", "").split("\n") if ln.strip() and not ln.strip().startswith("#")]
    if log_rows:
        out.append(f"🕰 {clip(log_rows[-1])}")
    return "\n".join(out).rstrip() + "\n"


def dispatch(arg: str) -> str:
    p = pathlib.Path(arg)
    if not p.exists():
        sys.exit(f"preview: {arg} does not exist")
    if p.is_file():
        return preview(p)
    if (p / "board.md").exists():
        return preview_board(p)
    if (p / f"{p.name}.md").exists():
        return preview(p / f"{p.name}.md")
    if page_dirs(p):
        return preview_group(p)
    mds = [m for m in p.glob("*.md") if not m.name.startswith("_")]
    if len(mds) == 1:
        return preview(mds[0])
    sys.exit(f"preview: {arg} holds no board.md, no page file, no page folders")


def main() -> int:
    ap = argparse.ArgumentParser(description="one screen: what a board, group, or page says right now")
    ap.add_argument("paths", nargs="+", help="board folder, group folder, page folder, or page .md")
    args = ap.parse_args()
    for i, arg in enumerate(args.paths):
        if i:
            print("─" * 60)
        print(dispatch(arg), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
