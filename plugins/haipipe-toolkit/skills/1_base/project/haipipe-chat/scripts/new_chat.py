"""A Block's chat sessions: `cNN_<slug>/`, one folder per kept session, numbered in time order (haipipe-chat).

    python new_chat.py new <block> --slug <slug> --title '<title>' [--ask '…'] [--summary '…']
                           [--changed a b …] [--cards a b …] [--session NAME] [--provider claude|codex]
                           [--transcript <session.jsonl>] [--date YYYY-MM-DD] [--dry-run]
    python new_chat.py list  <block>
    python new_chat.py check <block>

`new` writes the next `cNN_<slug>/cNN_<slug>.md` beside the Block's Jobs and Studio topics: front matter (session,
provider, date, goal, paths, cards), then `# cNN · <title>`, `## Ask`, `## Summary`, `## Changed`. `--changed`
paths that exist are written relative to the SPACE root (the nearest folder above holding env.sh or
.server_config), so the Session view joins the chat to the folders it changed. `--transcript` renders a Claude
Code session file into `transcript.md` beside the face (kept for reference; a page never links it). `list` prints
the chats in number order. `check` exits 1 when a chat has no face, no date or no goal, or names a path that is
not on disk.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

import yaml

SLUG = re.compile(r"^[a-z0-9][a-z0-9_]*$")
CHAT = re.compile(r"^c(\d{2,})_([a-z0-9][a-z0-9_]*)$")       # cNN_<slug>/, beside a Block's jNN_ and sNN-
SPACE_MARKS = ("env.sh", ".server_config")


def space_root(folder: Path) -> Path | None:
    for p in [folder, *folder.parents]:
        if any((p / m).is_file() for m in SPACE_MARKS):
            return p
    return None


def is_block(folder: Path) -> bool:
    return folder.is_dir() and ((folder / "board.md").is_file() or bool(re.match(r"^b\d+_", folder.name)))


def chats(block: Path) -> list[Path]:
    """The Block's chat folders, in number order."""
    return sorted((p for p in block.iterdir() if p.is_dir() and CHAT.match(p.name)),
                  key=lambda p: int(CHAT.match(p.name).group(1)))


def next_number(block: Path) -> int:
    used = [int(CHAT.match(p.name).group(1)) for p in chats(block)]
    return max(used) + 1 if used else 1


def space_relative(raw: str, block: Path) -> str:
    """A path as the Session view reads it: SPACE-relative when it exists (else relative to the Block), or as given."""
    top = space_root(block)
    for base in (Path.cwd(), block):
        p = Path(raw) if Path(raw).is_absolute() else base / raw
        if p.exists():
            p = p.resolve()
            if top and p.is_relative_to(top.resolve()):
                return p.relative_to(top.resolve()).as_posix()
            return Path(os.path.relpath(p, block.resolve())).as_posix()    # no SPACE root: from the Block, never absolute
    return raw


def _text(content) -> str:
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        return "\n\n".join(c.get("text", "").strip() for c in content
                           if isinstance(c, dict) and c.get("type") == "text" and c.get("text", "").strip())
    return ""


def transcript_markdown(jsonl: Path, title: str) -> str:
    """The person's and the assistant's words from a Claude Code session file; tool calls and results left out."""
    out = [f"# {title} · transcript", "", f"source: `{jsonl.name}`", ""]
    for line in jsonl.read_text(encoding="utf-8", errors="ignore").splitlines():
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        msg = row.get("message") if isinstance(row, dict) else None
        if not isinstance(msg, dict) or row.get("type") not in ("user", "assistant"):
            continue
        words = _text(msg.get("content"))
        if words:
            out += [f"## {'You' if row['type'] == 'user' else 'Assistant'}", "", words, ""]
    return "\n".join(out).rstrip() + "\n"


def face_text(nn: int, title: str, meta: dict, ask: str, summary: str, changed: list[str]) -> str:
    head = yaml.safe_dump(meta, sort_keys=False, allow_unicode=True).strip()
    lines = [f"---\n{head}\n---", "", f"# c{nn:02d} · {title}", "", "## Ask", "", ask or "", "",
             "## Summary", "", summary or "", "", "## Changed", ""]
    lines += [f"- `{p}`" for p in changed]
    return "\n".join(lines).rstrip() + "\n"


def cmd_new(a) -> int:
    block = Path(a.block).resolve()
    if not is_block(block):
        sys.exit(f"{block}: not a Block (no board.md, not bNN_)")
    if not SLUG.match(a.slug):
        sys.exit(f"slug {a.slug!r}: lower-case words joined by _")
    nn = next_number(block)
    folder = block / f"c{nn:02d}_{a.slug}"
    paths = [space_relative(p, block) for p in a.changed]
    meta = {"session": a.session or "", "provider": a.provider, "date": a.date or dt.date.today().isoformat(),
            "goal": a.title, "paths": paths, "cards": list(a.cards)}
    text = face_text(nn, a.title, meta, a.ask, a.summary, paths)
    if a.dry_run:
        print(f"would write {folder.name}/{folder.name}.md\n\n{text}")
        return 0
    folder.mkdir()
    (folder / f"{folder.name}.md").write_text(text, encoding="utf-8")
    if a.transcript:
        (folder / "transcript.md").write_text(transcript_markdown(Path(a.transcript), a.title), encoding="utf-8")
    print(folder)
    return 0


def read_face(folder: Path) -> tuple[dict, str] | None:
    face = folder / f"{folder.name}.md"
    if not face.is_file():
        return None
    text = face.read_text(encoding="utf-8", errors="ignore")
    if text.startswith("---\n"):
        head, sep, body = text[4:].partition("\n---")
        if sep:
            try:
                meta = yaml.safe_load(head) or {}
                return (meta if isinstance(meta, dict) else {}), body
            except yaml.YAMLError:
                pass
    return {}, text


def cmd_list(a) -> int:
    for folder in chats(Path(a.block).resolve()):
        meta, _ = read_face(folder) or ({}, "")
        print(f"{folder.name}  {meta.get('date', ''):<10}  {meta.get('goal', '')}")
    return 0


def problems(block: Path) -> list[str]:
    found, top = [], space_root(block)
    for folder in chats(block):
        read = read_face(folder)
        if read is None:
            found.append(f"{folder.name}/ has no face {folder.name}.md")
            continue
        meta, _ = read
        for key in ("date", "goal"):
            if not meta.get(key):
                found.append(f"{folder.name}: no {key}:")
        for raw in meta.get("paths") or []:
            if not any(b and (b / str(raw)).exists() for b in (top, block)):
                found.append(f"{folder.name}: {raw} is not on disk")
    return found


def cmd_check(a) -> int:
    found = problems(Path(a.block).resolve())
    for line in found:
        print(line)
    return 1 if found else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new")
    n.add_argument("block")
    n.add_argument("--slug", required=True)
    n.add_argument("--title", required=True)
    n.add_argument("--ask", default="")
    n.add_argument("--summary", default="")
    n.add_argument("--changed", nargs="*", default=[])
    n.add_argument("--cards", nargs="*", default=[])
    n.add_argument("--session", default="")
    n.add_argument("--provider", default="claude", choices=("claude", "codex"))
    n.add_argument("--transcript", default="")
    n.add_argument("--date", default="")
    n.add_argument("--dry-run", action="store_true")
    for name in ("list", "check"):
        sub.add_parser(name).add_argument("block")
    a = ap.parse_args(argv)
    return {"new": cmd_new, "list": cmd_list, "check": cmd_check}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
