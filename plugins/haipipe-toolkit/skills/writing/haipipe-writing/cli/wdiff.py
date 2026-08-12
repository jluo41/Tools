#!/usr/bin/env python3
"""Word-level change records, computed rather than written.

    python3 wdiff.py record  --old "…" --new "…"          -> one ✎ line
    python3 wdiff.py apply   FILE --old "…" --new "…"     -> rewrite + anchored record
    python3 wdiff.py check   FILE                         -> audit every record

    --host board   (default)  > ✎ ~old~ *new* · WHO · YYMMDD HHMM
    --host paper              > Note: ~~old~~ **new** · WHO · WHEN

WHY THIS IS CODE AND NOT A PROMPT
A model asked to "show the diff" writes a whole-sentence swap, because that is
what a diff feels like from the inside. It also appends the record wherever it
finished writing, which silently attaches it to the wrong sentence. Both
happened on QB4 on 260801, twice each, to an author who knew the rule. So the
diff is computed by difflib and the record is inserted by position: neither is
left to judgment.

WHY THE HOST IS A FLAG AND NOT THE CALLER'S JOB
Until 0.5.0 this emitted the board dialect only, and `haipipe-paper-revise`
instructed its caller to "double the tildes and turn *new* into **inserted**
for this host". That put a hand step inside the one tool whose whole argument is
that this class of hand step gets done wrong. The computation was in one place
and the OUTPUT was not. Same difflib opcodes, two notations, one flag.

THE GRAMMAR (haipipe-board renders the board host; see ref/change-record.md)
    > ✎ <diff> · <WHO> · <YYMMDD HHMM>
`~removed~` renders as a deletion and `*added*` as an insertion. Unchanged words
stay plain, which is the whole point: a reader sees what survived.
"""
import argparse
import difflib
import re
import sys
from pathlib import Path

MARK = re.compile(r"[~*]")
RECORD = re.compile(r"^>\s*✎\s*(.*?)\s*·\s*([A-Z]{1,4})\s*·\s*(\d{6}(?:\s+\d{3,4})?)\s*$")

# One computation, two notations. `del`/`ins` are the marks that wrap a run of
# words, `lane` is the `>` prefix the record is written behind. Board is the
# default because it is the host this skill was extracted from.
HOSTS = {
    "board": {"del": "~%s~",   "ins": "*%s*",   "lane": "> ✎ "},
    "paper": {"del": "~~%s~~", "ins": "**%s**", "lane": "> Note: "},
}


def wdiff(old, new, host="board"):
    """-> the diff in `host`'s notation, with every unchanged word left plain."""
    h = HOSTS[host]
    if MARK.search(old) or MARK.search(new):
        raise SystemExit("✗ `~` and `*` are the change marks; they cannot appear in the text")
    a, b = old.split(), new.split()
    out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b).get_opcodes():
        if tag == "equal":
            out.append(" ".join(a[i1:i2]))
        elif tag == "delete":
            out.append(h["del"] % " ".join(a[i1:i2]))
        elif tag == "insert":
            out.append(h["ins"] % " ".join(b[j1:j2]))
        else:
            out.append(h["del"] % " ".join(a[i1:i2]))
            out.append(h["ins"] % " ".join(b[j1:j2]))
    return " ".join(out)


def record(old, new, who, when, host="board"):
    return "%s%s · %s · %s" % (HOSTS[host]["lane"], wdiff(old, new, host), who, when)


def apply(path, old, new, who, when, host="board"):
    """Replace `old` with `new` and anchor the record under the FIRST new line.

    A rewrite that splits one sentence into three anchors on the first of them,
    never on the last: the apparatus binds to the line above it, so a record
    placed at the end of a block describes a sentence it does not sit under.
    """
    p = Path(path)
    s = p.read_text()
    n = s.count(old)
    if n != 1:
        raise SystemExit("✗ the old text appears %d times; it must appear exactly once" % n)
    if old.lstrip().startswith(">"):
        # `> WHO:` and `> ✎` lines are the durable review trail and are never
        # erased (haipipe-board/ref/writing-rules.md). This tool rewrites
        # SENTENCES; a lane is somebody's signed record, not prose to improve.
        raise SystemExit("✗ that is a lane, not a sentence. Lanes are appended, never rewritten.")
    # Two guards, because they answer two questions. `mine` must GROW by one, or
    # this call did not do what it said. `keep` must never SHRINK, whichever host
    # is writing: a signed ✎ line is the durable review trail and a paper-host
    # call has no more right to destroy one than a board-host call does.
    lane = re.escape(HOSTS[host]["lane"].strip())
    mine_before = len(re.findall(r"^\s*" + lane, s, re.M))
    keep_before = len(re.findall(r"^>\s*✎", s, re.M))
    lines = new.split("\n")
    first = lines[0]
    # The DIFF covers the whole rewritten run, while the RECORD sits under its
    # first line. Diffing against the first line alone marks everything that
    # moved to a later line as deleted, which is a lie: a split sentence loses
    # nothing. Anchor and scope are two different questions.
    rec = record(old, " ".join(x.strip() for x in lines), who, when, host)

    # A sentence's apparatus is a RUN of `>` lines, and a new record joins the
    # END of it (haipipe-sentence, "The lanes"; QB4's Law: place the note
    # after any existing `> Citation:` / `> Value:` / `> Display:` lane so the
    # whole apparatus folds under one sentence). Inserting straight after the
    # sentence would split that run in two, and the second half would rebind to
    # the record instead of the sentence.
    body = s.split("\n")
    at = next(i for i, x in enumerate(body) if old.split("\n")[0] in x)
    end = at + 1
    while end < len(body) and body[end].lstrip().startswith(">"):
        end += 1
    kept = body[at + 1:end]                       # existing lanes: NEVER touched
    tail = lines[1:]
    # ANCHOR and SCOPE are two questions and the split rewrite answers them
    # differently: the diff covers the whole run, the record sits under the
    # FIRST new line. Writing `[first] + tail + kept + [rec]` put it under the
    # LAST one, so a sentence broken into three carried its record on sentence
    # three, describing words that had moved to sentence one. Invisible for four
    # releases because every rewrite the tool had been given was single-line,
    # where `tail` is empty and the two orders are the same string.
    body[at:end] = [first] + kept + [rec] + tail
    out = "\n".join(body)
    if len(re.findall(r"^>\s*✎", out, re.M)) < keep_before:
        raise SystemExit("✗ refusing to write: this edit would destroy an existing ✎ record")
    mine_after = len(re.findall(r"^\s*" + lane, out, re.M))
    if mine_after < mine_before + 1:
        raise SystemExit("✗ refusing to write: this edit would destroy %d existing record(s)"
                         % (mine_before + 1 - mine_after))
    p.write_text(out)
    return first


def anchor(lines, i):
    """-> the prose sentence a `>` line at index `i` belongs to, or "".

    A sentence's apparatus is a RUN of `>` lines and a record joins the END of
    it, so the line directly above a record is usually another lane rather than
    the sentence. Walking the run back is what makes `apply` and `check` agree:
    before 0.5.0 `check` looked one line up and rejected every record `apply`
    had correctly appended after an existing `> Citation:` lane.
    """
    j = i - 1
    while j >= 0 and lines[j].lstrip().startswith(">"):
        j -= 1
    return lines[j].strip() if j >= 0 else ""


def check(path):
    """Every record is well-formed, and its lane run sits under a real prose line."""
    lines = Path(path).read_text().splitlines()
    bad = []
    for i, ln in enumerate(lines):
        if not ln.lstrip().startswith("> ✎"):
            continue
        m = RECORD.match(ln.strip())
        if not m:
            bad.append((i + 1, "malformed: needs `> ✎ <diff> · WHO · YYMMDD HHMM`"))
            continue
        prev = anchor(lines, i)
        if not prev or prev.startswith(("#", "```", "-", "*")):
            bad.append((i + 1, "not anchored: this lane run does not sit under a prose sentence"))
        if "~" not in m.group(1) and "*" not in m.group(1):
            bad.append((i + 1, "no change marked: a record with no ~old~ or *new* says nothing"))
    return bad


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="verb", required=True)
    for v in ("record", "apply"):
        q = sub.add_parser(v)
        if v == "apply":
            q.add_argument("file")
        q.add_argument("--old", required=True)
        q.add_argument("--new", required=True)
        q.add_argument("--who", default="CC")
        q.add_argument("--when", required=True, help="YYMMDD HHMM (board) · the host's own stamp")
        q.add_argument("--host", choices=sorted(HOSTS), default="board",
                       help="which notation to emit: board `~x~ *y*`, paper `~~x~~ **y**`")
    c = sub.add_parser("check")
    c.add_argument("file")
    a = ap.parse_args()

    if a.verb == "record":
        print(record(a.old, a.new, a.who, a.when, a.host))
    elif a.verb == "apply":
        print("✅ anchored under: " + apply(a.file, a.old, a.new, a.who, a.when, a.host)[:70])
    else:
        bad = check(a.file)
        for line, why in bad:
            print("✗ %s:%d  %s" % (a.file, line, why))
        print("%s · %d record problem(s)" % (a.file, len(bad)))
        sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
