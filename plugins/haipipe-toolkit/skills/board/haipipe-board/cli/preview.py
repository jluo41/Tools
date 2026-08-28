#!/usr/bin/env python3
"""One screen: what a Board Page says right now.

The three strips answer WHERE (`pagestatus.py` a group, `pagephase.py` a
phase, `pagecontext.py` the related-page packet); none answers WHAT. This
tool prints the page's own summary surfaces — the title, the Opening's
visible paragraph, the Aims joined to their States, the Content division
list — so a reader knows what the page claims before opening it. It reads
one file and never writes.

Preview is a gist, not a read: WORK ON still owes the whole-file read its
step 1 names. The Opening's visible paragraph IS the page's self-summary
by contract (haipipe-page §✍️), which is why this tool can exist at all.

    python3 preview.py <page.md | page-dir> [more pages ...]
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys


def resolve(arg: str) -> pathlib.Path:
    p = pathlib.Path(arg)
    if p.is_dir():
        cand = p / f"{p.name}.md"
        if cand.exists():
            return cand
        mds = [m for m in p.glob("*.md") if not m.name.startswith("_")]
        if len(mds) == 1:
            return mds[0]
        sys.exit(f"preview: {arg} is a folder with no obvious page file")
    if not p.exists():
        sys.exit(f"preview: {arg} does not exist")
    return p


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
    diagram = secs.get("Diagram", "")
    if diagram.strip():
        tail.append(f"🖼 diagram {len(diagram.strip().splitlines())} lines")
    files = [ln for ln in secs.get("Files", "").split("\n") if ln.strip().startswith(("-", "|"))]
    if files:
        tail.append(f"📂 {len(files)} file rows")
    log_rows = [ln.strip() for ln in secs.get("Log", "").split("\n") if ln.strip() and not ln.strip().startswith("#")]
    if log_rows:
        tail.append(f"🕰 {clip(log_rows[-1])}")
    if tail:
        out.append(" · ".join(tail))
    return "\n".join(out).rstrip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="one screen: what a Board Page says right now")
    ap.add_argument("pages", nargs="+", help="page .md file or page folder")
    args = ap.parse_args()
    for i, arg in enumerate(args.pages):
        if i:
            print("─" * 60)
        print(preview(resolve(arg)), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
