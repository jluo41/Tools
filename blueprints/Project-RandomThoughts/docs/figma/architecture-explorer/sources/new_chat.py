"""A Block's chat sessions: `cNN_<slug>/`, one folder per kept session, numbered in time order (haipipe-chat).

    python new_chat.py new <block> --slug <slug> --title '<title>' --from <session.jsonl> [--summary '…']
                           [--session NAME] [--provider claude|codex] [--cards a b …] [--date YYYY-MM-DD] [--dry-run]
    python new_chat.py new <block> --slug <slug> --title '<title>' --ask '…' --answer '…' --changed a b …
    python new_chat.py refresh <block>/cNN_<slug> --from <session.jsonl>
    python new_chat.py list  <block>
    python new_chat.py check <block>

A chat is kept as QAs: one question the person asked, its answer, and what it produced (scripts/qa.py). `new` writes
the next `cNN_<slug>/cNN_<slug>.md` beside the Block's Jobs and Studio topics: front matter (session, provider, date,
goal, paths, cards), `# cNN · <title>`, a summary when given, `## QA` (a few lines a turn). Paths are
written relative to the SPACE root (the nearest folder above holding env.sh or .server_config), else to the Block,
so the Session view joins the chat to the folders it changed. No transcript is kept. `refresh` rewrites a chat's
face from its session as it now stands; the Stop hook (`chat_hook.py`) runs it once when each answer ends, for a
session saved with `--from`. `check` exits 1 when a chat has no face, no date or no goal, or names a
path that is not on disk.
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

import qa

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


def face_text(nn: int, title: str, meta: dict, summary: str, qas: list[dict]) -> str:
    """The face: front matter, # cNN · <title>, a summary when given, ## QA (a few lines a turn)."""
    head = yaml.safe_dump(meta, sort_keys=False, allow_unicode=True).strip()
    lines = [f"---\n{head}\n---", "", f"# c{nn:02d} · {title}", ""]
    if summary:
        lines += [summary, ""]
    lines += qa.markdown(qas)
    return "\n".join(lines).rstrip() + "\n"


def collect(a, block: Path) -> tuple[list[dict], list[str]]:
    """The QAs (from --from, else one QA from --ask, --answer and --changed) and every path they produced."""
    if a.source:
        qas = qa.from_session(Path(a.source))
    else:
        qas = [{"q": a.ask, "time": "", "answer": a.answer, "outputs": list(a.changed)}] if a.ask else []
    paths = []
    for p in [*(o for q in qas for o in q["outputs"]), *a.changed]:
        r = space_relative(p, block)
        if r not in paths:
            paths.append(r)
    return qas, paths


def cmd_new(a) -> int:
    block = Path(a.block).resolve()
    if not is_block(block):
        sys.exit(f"{block}: not a Block (no board.md, not bNN_)")
    if not SLUG.match(a.slug):
        sys.exit(f"slug {a.slug!r}: lower-case words joined by _")
    nn = next_number(block)
    folder = block / f"c{nn:02d}_{a.slug}"
    write(folder, nn, a, block, a.date or dt.date.today().isoformat())
    return 0


def registry() -> Path:
    """Which session is kept as which chat: {session id: cNN folder}. Machine state, never in a repository."""
    return Path(os.environ.get("HAIPIPE_CHAT_REGISTRY") or Path.home() / ".claude" / "haipipe-chat" / "kept.json")


def register(session_id: str, folder: Path) -> None:
    reg = registry()
    kept = json.loads(reg.read_text()) if reg.is_file() else {}
    kept[session_id] = str(folder.resolve())
    reg.parent.mkdir(parents=True, exist_ok=True)
    reg.write_text(json.dumps(kept, indent=1, sort_keys=True))


def write(folder: Path, nn: int, a, block: Path, date: str) -> None:
    qas, paths = collect(a, block)
    meta = {"session": a.session or "", "provider": a.provider, "date": date, "goal": a.title,
            "paths": paths, "cards": list(a.cards)}
    text = face_text(nn, a.title, meta, a.summary, qas)
    if a.dry_run:
        print(f"would write {folder.name}/{folder.name}.md\n\n{text}")
        return
    folder.mkdir(exist_ok=True)
    (folder / f"{folder.name}.md").write_text(text, encoding="utf-8")
    if a.source:
        register(Path(a.source).stem, folder)    # the Stop hook refreshes it when each answer ends (chat_hook.py)
    if not getattr(a, "quiet", False):
        print(folder)


def cmd_refresh(a) -> int:
    """Rewrite a chat's face from its session as it now stands (a re-keep); its number, title and date stay."""
    folder = Path(a.chat).resolve()
    m = CHAT.match(folder.name)
    read = read_face(folder) if m else None
    if read is None:
        sys.exit(f"{folder}: not a chat folder with its face")
    meta, body = read
    old = re.search(r"(?ms)^## Summary\s*$(.*?)(?=^## |\Z)", body) or re.search(r"(?ms)^# c\d+ · .*?$(.*?)(?=^## |\Z)", body)
    summary = a.summary or (old.group(1).strip() if old else "")
    a.title = a.title or str(meta.get("goal") or folder.name)
    a.session = a.session or str(meta.get("session") or "")
    a.cards = a.cards or list(meta.get("cards") or [])
    a.summary = summary
    write(folder, int(m.group(1)), a, folder.parent, str(meta.get("date") or dt.date.today().isoformat()))
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
    r = sub.add_parser("refresh")
    r.add_argument("chat")
    for p, need in ((n, True), (r, False)):
        p.add_argument("--title", required=need, default="")
        p.add_argument("--from", dest="source", default="", help="a Claude Code session .jsonl: its QAs")
        p.add_argument("--ask", default="", help="without --from: the one question")
        p.add_argument("--answer", default="", help="without --from: its answer")
        p.add_argument("--summary", default="")
        p.add_argument("--changed", nargs="*", default=[])
        p.add_argument("--cards", nargs="*", default=[])
        p.add_argument("--session", default="")
        p.add_argument("--provider", default="claude", choices=("claude", "codex"))
        p.add_argument("--date", default="")
        p.add_argument("--dry-run", action="store_true")
        p.add_argument("--quiet", action="store_true")
    for name in ("list", "check"):
        sub.add_parser(name).add_argument("block")
    a = ap.parse_args(argv)
    return {"new": cmd_new, "refresh": cmd_refresh, "list": cmd_list, "check": cmd_check}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
