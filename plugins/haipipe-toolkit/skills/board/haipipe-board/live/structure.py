"""QC8 · index shape (QB2): add a question, add a group, archive.

Moved out of serve.py on 2026-07-31 under the gate_live.py response-identical gate.
QC3's Law: a refactor moves code, features never ride along.
"""

import base64
import datetime as dt
import difflib
import hashlib
import itertools
import json
import os
import re
import shutil
import signal
import socket
import sqlite3
import struct
import subprocess
import sys
import threading
import time
import urllib.parse
from pathlib import Path
from urllib.parse import unquote

from . import base
from .base import _now_stamp, q_files, vet_qpath


def _slugify(t):
    s = re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")
    return "-".join(s.split("-")[:5])[:48] or "question"


# The skeleton the ＋ button writes. Opening, Items to Finish, and Where we are
# are required; Files is optional but strongly advised; everything else is
# optional. There is no separate Boundary section: Opening states the scope.
#
# Advised sections are written OUT, so declining one is a deletion rather than an
# omission. Optional ones are listed in a comment instead: an author cannot choose
# a section they never learn exists (JL 260726, after a new page arrived with no
# Diagram and nothing said one was available), and a comment is dropped at render,
# so the page never shows a box opened onto nothing.
Q_STUB = """# {title}
state: 🔴 OPEN
owner: JL

## Opening
{title}: restate this as one plain question a zero-background reader understands.

Then one paragraph on what this page covers, why it is hard, what breaks while it stays open, and which neighbouring page owns anything excluded. This file is a stub from the index page's ＋ button;
writing standard: ref/writing-rules.md (English only, no em-dashes).

<!-- Optional sections, in the order they render. Uncomment the ones this page
     earns and delete this comment; empty beats wrong, so leave out what you
     cannot fill (grammar: ref/q-template.md, layout: QA4).

## Diagram      one ascii figure of the shape or flow, collapsed on the page.
                An excalidraw share URL alone on a line embeds as a canvas.
## Content      ### is a division that folds, #### is one paragraph inside it.
## Law          rules this page has settled.
## Lesson       traps hit, with the concrete failure attached.
## Glossary     words an outsider would stumble on: `term: explanation`.
## Discussion   loose threads, `> JL:` and `>> CC0726:`.
-->

## Items to Finish
- [ ] 🎯 Name what counts as done
      One sentence saying exactly how this line is judged met.

## Where we are
Nothing yet: the question was just opened.

## Files
- `path/to/thing`
  Its role in this question, and where you start when this question changes.

## Log
{stamp} · Opened from the index page (＋ Question)
"""


def page_id_of(stem):
    """A page's id from its filename stem, numbered OR named.

    `stem.split("-")[0]` was right while every page was `QA4-slug`; a named
    family (`Q-Skill-haipipe-board`, JL 260727) collapses to `Q` under that
    rule, so every skill page reported as one row called `Q` in the activity
    tree. The named form keeps `Q-<Family>-<rest>` whole, which is the id
    `parse.py` assigns and therefore the id everything else already uses.
    """
    m = re.match(r"^(Q-[A-Z][A-Za-z]*-.+)$", stem)
    if m:
        return m.group(1)
    m = re.match(r"^(S-[A-Za-z]+-[0-9A-Za-z]+)", stem)
    return m.group(1) if m else stem.split("-")[0]


def structure_op(board, p):
    """The index's shape as ONE writer (QC2): add/archive groups and questions.

    Deliberately module-level and self-free, like the comment writers, so the
    console (boards_api.py) can import it instead of reimplementing (QE3 Law).
    All edits go through board.md's ## Pages plus the Q files themselves.
    Archive NEVER deletes: files move to _archive/ inside the board folder and
    stay recoverable by hand.
    """
    op = (p.get("op") or "").strip()
    bp = board / "board.md"
    lines = bp.read_text(encoding="utf-8").split("\n")
    ps = next(
        (i for i, ln in enumerate(lines)
         if re.match(r"^## (?:Pages|Roster)\b", ln)),
        None,
    )
    if ps is None:
        return None, "board.md has no ## Pages section"
    pend = next((i for i in range(ps + 1, len(lines)) if lines[i].startswith("## ")),
                len(lines))
    heads = []                              # (line idx, letter, full heading)
    for i in range(ps + 1, pend):
        m = re.match(r"^### Q([0-9][a-z]|[A-Z]+[a-z]?)\b", lines[i].strip())
        if m:
            heads.append((i, m.group(1), lines[i].strip()[4:].strip()))

    def block_end(hi):                      # lines belonging to the group at hi
        j = hi + 1
        while j < pend and not lines[j].strip().startswith("### "):
            j += 1
        return j

    def write():
        bp.write_text("\n".join(lines), encoding="utf-8")

    if op == "add_group":
        title = " ".join((p.get("title") or "").split())
        if not title:
            return None, "the group needs a title"
        used = {l for _, l, _ in heads}
        letter = (p.get("letter") or "").strip().upper().lstrip("Q")
        if not letter:
            letter = next((c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if c not in used), "")
        if not letter or letter in used:
            return None, f"group letter Q{letter or '?'} is taken or invalid"
        block = [f"### Q{letter} · {title}"]
        hook = " ".join((p.get("hook") or "").split())
        if hook:
            block.append(hook)
        for ln in (p.get("body") or "").split("\n"):
            if ln.strip():
                block.append(ln.strip())
        at = pend                           # append at the section's true tail
        while at > ps + 1 and not lines[at - 1].strip():
            at -= 1
        lines[at:at] = block
        write()
        return {"group": f"Q{letter} · {title}", "letter": letter}, None

    if op == "add_question":
        g = (p.get("group") or "").strip()
        title = " ".join((p.get("title") or "").split())
        if not title:
            return None, "the question needs a title"
        m = re.match(r"^Q?([0-9][a-z]|[A-Z]+[a-z]?)", g)
        hit = next(((i, l, h) for i, l, h in heads
                    if (m and l == m.group(1)) or h == g), None)
        if not hit:
            return None, f"no group matches {g!r} (heading must start with ### Q<letter>)"
        hi, letter, heading = hit
        pat = re.compile(rf"^Q{letter}(\d+)")
        nums = [int(mm.group(1)) for f in q_files(board)
                if (mm := pat.match(f.name))]
        nums += [int(mm.group(1)) for ln in lines[ps:pend]
                 if (mm := pat.match(ln.strip()))]
        fname = f"Q{letter}{max(nums, default=0) + 1}-{_slugify(title)}.md"
        # 🪄 The new page follows its group (QA1, JL 260726). It used to always
        # land at the board root, so on a board whose groups are folders every
        # new page was born in the wrong place and had to be moved by hand.
        #
        # The rule is "where does this group already live", never "a folder
        # named QA". That makes it right for BOTH reasons a page sits in a
        # folder: the folder is the GROUP (a flat design board that grew), or
        # the folder is the SUBJECT (QC3, a board sitting on an existing tree
        # such as a paper's 0-lifecycle/). On a flat board every sibling is at
        # the root, so the file stays at the root and nothing changes: this
        # follows a decision the board already made rather than making one.
        # A group whose pages disagree, or which has none yet, falls back to
        # the root, because guessing between two homes is worse than the wart.
        listed = {ln.strip() for ln in lines[hi + 1:block_end(hi)]
                  if ln.strip().endswith(".md")}
        homes = {x.parent for x in q_files(board) if x.name in listed}
        if len(homes) == 1:
            home = homes.pop()
        elif homes:
            home = board                    # the group disagrees with itself
        else:
            # An empty group opens its own folder, named `Q<letter>-<slug of the
            # heading>` (JL 260726: group folders are the default, and "I want
            # the QA-xx with some names, not just QA"). A bare `QA/` is a second
            # copy of the id; the title is the part a reader cannot reconstruct.
            slug = re.sub(r"[^a-z0-9]+", "-",
                          heading.split("·", 1)[-1].strip().lower()).strip("-")
            home = board / (f"Q{letter}-{slug}" if slug else f"Q{letter}")
        f = home / fname
        if f.exists():
            return None, f"{f.relative_to(board).as_posix()} already exists"
        home.mkdir(parents=True, exist_ok=True)
        f.write_text(Q_STUB.format(title=title, stamp=_now_stamp()), encoding="utf-8")
        at = block_end(hi)                  # list it at the end of its group
        while at > hi + 1 and not lines[at - 1].strip():
            at -= 1
        lines[at:at] = [fname]              # ## Pages stays bare filenames
        write()
        return {"file": f.relative_to(board).as_posix(), "group": heading}, None

    if op == "archive_question":
        name = vet_qpath(p.get("q"))
        if not name:
            return None, f"not a Q file name: {p.get('q')!r}"
        f = board / name
        if not f.exists():
            return None, f"not found: {name}"
        arch = board / "_archive"
        arch.mkdir(exist_ok=True)
        dest = arch / name.rsplit("/", 1)[-1]   # nested pages flatten here
        if dest.exists():
            dest = arch / f"{f.stem}-{time.strftime('%y%m%d%H%M%S')}.md"
        note = f"{_now_stamp()} · Archived from the index page (moved to _archive/)"
        t = f.read_text(encoding="utf-8")
        mm = re.search(r"^## Log\s*$", t, re.M)
        if mm:                              # Log is newest-first: insert right below
            t = t[:mm.end()] + "\n" + note + t[mm.end():]
        else:
            t = t.rstrip("\n") + "\n\n## Log\n" + note + "\n"
        f.write_text(t, encoding="utf-8")
        shutil.move(str(f), str(dest))
        base = name.rsplit("/", 1)[-1]          # Pages lists bare filenames
        lines[ps:pend] = [ln for ln in lines[ps:pend]
                          if ln.strip() not in (name, base)]
        write()
        return {"file": name, "to": f"_archive/{dest.name}"}, None

    if op == "archive_group":
        g = (p.get("group") or "").strip()
        m = re.match(r"^Q?([0-9][a-z]|[A-Z]+[a-z]?)", g)
        hit = next(((i, l, h) for i, l, h in heads
                    if (m and l == m.group(1)) or h == g), None)
        if not hit:
            return None, f"no group matches {g!r}"
        hi, letter, heading = hit
        j = block_end(hi)
        while j > hi + 1 and not lines[j - 1].strip():   # keep section padding
            j -= 1
        left = [ln.strip() for ln in lines[hi + 1:j] if ln.strip().endswith(".md")]
        if left:
            return None, (f"{heading} still lists {len(left)} question(s): "
                          "archive them first")
        del lines[hi:j]
        write()
        return {"group": heading}, None

    return None, f"unknown op: {op or '(empty)'}"

