#!/usr/bin/env python3
"""Turn an echo-meeting note into a board page of kind `Meeting-<n>`.

    python3 meetingpage.py new  <board> <note.md> [--group QG] [--slug s]
    python3 meetingpage.py sync <board> <page-id>

QC10 rules this. A meeting produces two things and they go to two places: the
ARTIFACT (this page) and the CONSEQUENCES (routed onto the Q pages that own
them, which is `haipipe-board-routing`'s job, not this file's).

The page is the SAME seven sections every page has; only the source differs.
`jluo41/echo-meeting`'s summarizer fixes six headings (`### TL;DR`, `###
Diagram`, `### Key Points`, `### Decisions`, `### Action Items`, `### Open
Questions`), so the mapping below is a lookup rather than an interpretation:

    ### TL;DR            -> ## Opening          managed
    ### Diagram          -> ## Diagram          managed  (already ASCII)
    ### Key Points       -> ## Content          managed
    ### Decisions        -> ## Content          managed
    ## Conversation      -> ## Content          managed  (one ### per chapter)
    ## Transcript        -> ## Content          managed  (last division)
    ### Action Items     -> ## Items to Finish  SEEDED ONCE, then yours
    ### Open Questions   -> ## Where we are     SEEDED ONCE, then yours

The seed/managed line is the whole design. You TICK action items, so a resync
that rewrote them would eat your state; they are written at birth and never
touched again. Everything a resync may overwrite lives inside a managed span,
which is also why the imported Chinese survives `check.py`: `strip_fences(...,
prose_only=True)` skips managed spans, and "fixing" a quotation falsifies it.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from src.common import page_files  # noqa: E402

PARTS = ("head", "diagram", "body")


def start_of(part):
    return f"<!-- haipipe:meeting:{part}:start"


def end_of(part):
    return f"<!-- haipipe:meeting:{part}:end -->"


# The marker carries the hash of what was imported AND the note it came from,
# so a sync can find its own source without reading rendered content — the
# lesson skillpage.py learned when its `![[...]]` embed disappeared.
MARKER = re.compile(r"^" + re.escape(start_of("head")) +
                    r"\s+([0-9a-f]{16})(?:\s+(\S+))?", re.M)


def digest(txt):
    return hashlib.sha256(txt.encode("utf-8")).hexdigest()[:16]


def rel(board, target):
    try:
        return target.resolve().relative_to(board.resolve()).as_posix()
    except ValueError:
        return target.resolve().as_posix()


# ── reading the note ──────────────────────────────────────────────────────
def split_sections(txt, level):
    """[(heading, body)] for one heading level, fences respected."""
    out, head, buf, fence = [], None, [], False
    pat = re.compile(r"^#{%d}\s+(.+?)\s*$" % level)
    for ln in txt.split("\n"):
        if ln.lstrip().startswith("```"):
            fence = not fence
        m = None if fence else pat.match(ln)
        if m:
            if head is not None or buf:
                out.append((head, "\n".join(buf).strip("\n")))
            head, buf = m.group(1), []
            continue
        buf.append(ln)
    if head is not None or buf:
        out.append((head, "\n".join(buf).strip("\n")))
    return out


def read_note(path):
    raw = path.read_text(encoding="utf-8")
    fm = {}
    if raw.startswith("---\n"):
        end = raw.find("\n---\n", 4)
        for ln in raw[4:end].split("\n"):
            if m := re.match(r"^([a-z_]+):\s*(.*)$", ln):
                fm[m.group(1)] = m.group(2).strip()
        raw = raw[end + 5:]
    note = {"fm": fm, "title": fm.get("title", path.stem), "raw": raw}
    if m := re.search(r"^#\s+(.+?)\s*$", raw, re.M):
        note["title"] = m.group(1).strip()
    for head, body in split_sections(raw, 2):
        if head:
            note[head.strip().lower()] = body
    summary = note.get("summary", "")
    for head, body in split_sections(summary, 3):
        if head:
            note["s:" + head.strip().lower()] = body
    return note


def chapters(note):
    """The `## Conversation` chapters, in order, as (title, body)."""
    return [(h, b) for h, b in split_sections(note.get("conversation", ""), 3) if h]


def checkboxes(txt):
    """`- [ ] …` rows, continuation lines folded in, from an Action Items block."""
    rows = []
    for ln in (txt or "").split("\n"):
        if re.match(r"^\s*[-*]\s*\[[ xX]\]", ln):
            rows.append(re.sub(r"^\s*[-*]\s*\[[ xX]\]\s*", "", ln).strip())
        elif rows and ln.strip() and not ln.startswith("#"):
            rows[-1] += " " + ln.strip()
    return rows


def bullets(txt):
    rows = []
    for ln in (txt or "").split("\n"):
        if re.match(r"^\s*[-*]\s+", ln):
            rows.append(re.sub(r"^\s*[-*]\s+", "", ln).strip())
        elif rows and ln.strip() and not ln.startswith("#"):
            rows[-1] += " " + ln.strip()
    return rows


# ── the managed halves ────────────────────────────────────────────────────
def head_block(board, note, note_path, stamp):
    tldr = [l.strip() for l in note.get("s:tl;dr", "").split("\n") if l.strip()]
    fm = note["fm"]
    meta = [f"`{fm.get('created', '?')}`"]
    if lines := re.search(r"Live transcript \((\d+) lines\)", note.get("transcript", "")):
        meta.append(f"{lines.group(1)} transcript lines")
    if n := len(chapters(note)):
        meta.append(f"{n} chapters")
    meta.append(f"recorded by `{fm.get('source', 'echo-meeting')}`")
    return "\n".join(
        [f"{start_of('head')} {stamp} {rel(board, note_path)} -->"]
        + tldr
        + ["", " · ".join(meta), end_of("head")])


def diagram_block(note, stamp):
    fig = note.get("s:diagram", "").strip()
    if not fig.startswith("```"):
        fig = "```text\n" + (fig or "no diagram in the summary") + "\n```"
    return "\n".join([f"{start_of('diagram')} {stamp} -->", fig, end_of("diagram")])


def exchange(body):
    """An Obsidian `> [!quote]-` callout becomes board sentence apparatus.

    A `>` run directly under a sentence is what this board already folds into
    that sentence's drawer, so the full exchange lands where a reader expects
    it: click the chapter's own summary line and the words that produced it
    open underneath. The callout's marker line is dropped because it names an
    Obsidian mechanism, not content.
    """
    out = []
    for ln in body.split("\n"):
        if re.match(r"^>\s*\[!\w+\][-+]?", ln):
            continue
        out.append(ln)
    return "\n".join(out).strip("\n")


def body_block(note, stamp):
    rows = [f"{start_of('body')} {stamp} -->"]
    if kp := bullets(note.get("s:key points", "")):
        rows += ["### Key points", ""] + [f"- {x}" for x in kp] + [""]
    if dec := bullets(note.get("s:decisions", "")):
        rows += ["### What the meeting decided", "",
                 "Each of these belongs on the page that owns it; routing them"
                 " is a separate pass, and this list is the record it works from.",
                 ""] + [f"- {x}" for x in dec] + [""]
    for title, body in chapters(note):
        rows += [f"### {title}", "", exchange(body), ""]
    if tr := note.get("transcript", "").strip():
        rows += ["### Transcript", "", exchange(tr), ""]
    rows.append(end_of("body"))
    return "\n".join(rows)


# ── the page ──────────────────────────────────────────────────────────────
STUB = """# {title}
state: 🟡 PARTIAL · imported; nothing routed yet
owner: JL
method: three managed spans sync from the vault note; what it changed on this board is written by hand

## Opening
{head}

Write here why this meeting matters to THIS BOARD, which is the one thing the note cannot say about itself.
What it settled, what it reopened, and which pages should not be read without it.

## Diagram
{diagram}

## Content
{body}

## Items to Finish
### From the meeting
{actions}

## Where we are
Imported {stamp_date} from `{note}`.
Nothing has been routed onto the Q pages yet, so this page is the whole record so far.

### Decision Now
{questions}

## Files
### Engines
- `../../board/haipipe-board/meetingpage.py`
  Reads the note and writes the three managed spans; seeds Items and Decision Now once.

### Input files
- `{note}`
  The vault note this page mirrors, written by `jluo41/echo-meeting`.
{recording}
### Output files
- This page
  The artifact half. The consequences half is whatever routing lands on the Q pages.

## Log
{stamp_date} · Imported from `{note}` by `meetingpage.py`
"""


def render(board, note, note_path, stamp_date):
    stamp = digest(note_path.read_text(encoding="utf-8"))
    actions = checkboxes(note.get("s:action items", ""))
    quests = bullets(note.get("s:open questions", ""))
    rec = ""
    if m := re.search(r"!\[\[([^\]]+)\]\]", note.get("recording", "")):
        rec = f"- `{m.group(1)}`\n  The recording the note embeds.\n"
    return STUB.format(
        title=note["title"],
        head=head_block(board, note, note_path, stamp),
        diagram=diagram_block(note, stamp),
        body=body_block(note, stamp),
        actions="\n".join(f"- [ ] {a}" for a in actions) or
                "- [ ] Nothing was recorded as an action item",
        questions="\n".join(
            f"- [ ] {q}\n      Raised in this meeting and still open;"
            " a tick here says it is answered or has moved to its own page."
            for q in quests) or
            "- [ ] Route this meeting onto the pages it changed\n"
            "      Nothing here is owed to JL yet; this row closes when the"
            " decisions above have landed on their Q pages.",
        stamp_date=stamp_date,
        note=rel(board, note_path),
        recording=rec)


def group_home(board, group):
    """(folder, lines, span) for a `### Q<key> · title` block in board.md."""
    lines = (board / "board.md").read_text(encoding="utf-8").split("\n")
    start = None
    for i, ln in enumerate(lines):
        if re.match(rf"^###\s+{re.escape(group)}\b", ln.strip()):
            start = i
        elif start is not None and re.match(r"^###?\s+", ln.strip()):
            return _home(board, group), lines, (start, i)
    if start is None:
        return None, lines, None
    return _home(board, group), lines, (start, len(lines))


def _home(board, group):
    for d in sorted(board.iterdir()):
        if d.is_dir() and d.name.startswith(group + "-"):
            return d
    return board / group


def cmd_new(a):
    board, note_path = Path(a.board).resolve(), Path(a.note).resolve()
    if not note_path.is_file():
        return f"{note_path} is not a file"
    note = read_note(note_path)
    if note["fm"].get("type") != "meeting":
        return f"{note_path.name} has no `type: meeting` frontmatter"
    home, lines, span = group_home(board, a.group)
    if home is None:
        return f"no group {a.group!r} in board.md"
    used = [int(m.group(1)) for p in page_files(board)
            if (m := re.match(r"^Meeting-(\d+)-", p.name))]
    n = max(used, default=0) + 1
    slug = a.slug or re.sub(r"[^a-z0-9]+", "-", note_path.stem.lower()).strip("-")
    dest = home / f"Meeting-{n}-{slug}.md"
    if dest.exists():
        return f"{rel(board, dest)} already exists"
    home.mkdir(parents=True, exist_ok=True)
    dest.write_text(render(board, note, note_path, a.stamp), encoding="utf-8")
    at = span[1]
    while at > span[0] + 1 and not lines[at - 1].strip():
        at -= 1
    lines[at:at] = [dest.name]
    (board / "board.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ {rel(board, dest)}  (listed under {a.group})")
    return None


def cmd_sync(a):
    board = Path(a.board).resolve()
    page = next((p for p in page_files(board)
                 if p.stem.startswith(a.page + "-") or p.stem == a.page), None)
    if page is None:
        return f"no page {a.page!r} on this board"
    txt = page.read_text(encoding="utf-8")
    m = MARKER.search(txt)
    if not m:
        return f"{rel(board, page)} carries no managed span"
    note_path = (board / m.group(2)).resolve()
    if not note_path.is_file():
        return f"the source note is gone: {m.group(2)}"
    note = read_note(note_path)
    stamp = digest(note_path.read_text(encoding="utf-8"))
    if stamp == m.group(1):
        print(f"= {rel(board, page)}  (note unchanged)")
        return None
    blocks = {"head": head_block(board, note, note_path, stamp),
              "diagram": diagram_block(note, stamp),
              "body": body_block(note, stamp)}
    for part, new in blocks.items():
        pat = re.compile(re.escape(start_of(part)) + r".*?" +
                         re.escape(end_of(part)), re.S)
        if not pat.search(txt):
            return f"{rel(board, page)} is missing the {part} span"
        txt = pat.sub(lambda _m: new, txt, count=1)
    page.write_text(txt, encoding="utf-8")
    print(f"✅ {rel(board, page)}  (3 spans refreshed; Items and Decision Now untouched)")
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new")
    n.add_argument("board")
    n.add_argument("note")
    n.add_argument("--group", default="QG")   # the Meeting group, JL 260801
    n.add_argument("--slug", default="")
    n.add_argument("--stamp", default="")
    n.set_defaults(fn=cmd_new)
    s = sub.add_parser("sync")
    s.add_argument("board")
    s.add_argument("page")
    s.set_defaults(fn=cmd_sync)
    a = ap.parse_args()
    if getattr(a, "stamp", None) == "":
        return "pass --stamp YYMMDD (the board never guesses a date)"
    err = a.fn(a)
    if err:
        print(f"⚠️  {err}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
