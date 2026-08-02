#!/usr/bin/env python3
"""The WRITE half of QF5: once a sentence is named, does the write land clean?

    .venv/bin/python sentencewrite.py [--url http://127.0.0.1:5599] [--keep]

`sentencerun.py` asks the READ half: can the browser still NAME every sentence
on a board. This asks what happens next. A sentence operation is a promise with
three parts, and only the first of them is visible in an HTTP status:

    ① exactly ONE line is added
    ② it lands directly under its sentence, at the END of the `>` run there
    ③ every other byte of the file is untouched

A 200 proves none of those. Every regression this family has shipped in the
write path passed its status check: the line went under the wrong copy of a
repeated sentence, or above an existing record instead of below it, or a second
click wrote the record twice. So this run asserts on the RESULTING MARKDOWN and
treats the status as a hint.

It runs against its own throwaway fixture board, one line per sentence SHAPE
(plain, already carrying apparatus, ending in a code span, bold, link, CJK,
punctuation, and the same sentence twice), crossed with all five write
endpoints. The fixture is created inside --root so the ALREADY RUNNING server
can reach it, restored from a pristine copy between cells, and deleted at the
end. Nothing outside the fixture folder is ever written to, so this is safe to
run while someone is reading a real board on the same server.

No browser: this half needs none. What the browser WOULD post is a string, and
the string it computes is what `sentencerun.py` already proves.

Exit 1 if any cell fails.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent  # the engine dir (this file lives in cli/)
REPO = HERE.parents[5]          # haipipe-board/board/skills/haipipe-toolkit/plugins/Tools

WHEN = "260801 1200"            # pinned, so an expected line is a constant


# ── the fixture ───────────────────────────────────────────────────────────
# Every anchor below is a SHAPE, not an example: each one is a way a real board
# writes a sentence that has broken this path before or could. They live in one
# `## Content` run because that is where prose sentences live on a real page,
# and the write path scans source lines, not sections.

S_PLAIN = "The write test posts one line at a time and then reads the markdown back."
S_APP = "Every record the board writes hangs as a quoted line under the sentence it belongs to."
S_CODE = "Rebuilding the generated tree after an accepted write is the job of `build.py`"
S_BOLD = "A sentence operation must write **exactly one line** and leave every other byte alone."
S_LINK = "The read half of this pair is driven by [sentencerun.py](QF2-second.md)."
S_CJK = "这句话用来测试中文句子能不能被准确定位并写入记录。"
S_PUNCT = "The board's write path handles quoting & escaping without a browser in the loop."
S_DUP = "This exact sentence appears twice on this page."

FIXTURE_BOARD = """# Fixture board for the sentence WRITE test

spine: One throwaway board carrying one sentence of every shape, so sentencewrite.py can post to all five write endpoints and read the markdown back.
close: Deleted the moment the run ends. If you are reading this on disk, a run crashed before its teardown and the folder is safe to remove by hand.
## Topic
This board is machine-made and machine-deleted. Nobody reviews it, nothing links to it, and no decision on it means anything.
Its only job is to be a REAL board: a folder with a board.md, pages the server accepts as write targets, and prose the write path can anchor on.

## Pipeline
Built by sentencewrite.py, torn down by the same script.

## Pages
### QF · Fixture
QF1-shapes.md
QF2-second.md
"""

FIXTURE_Q1 = f"""# Eight sentence shapes, one per line

state: 🟡 PARTIAL
owner: CC
method: one source line per shape, so every write cell has a stable anchor that no other cell can touch

## Opening
How does a write behave against each shape of sentence a real board actually contains?

## Content
{S_PLAIN}
{S_APP}
> Note: this record existed before the run started, so a new one has to land below it.
{S_CODE}
{S_BOLD}
{S_LINK}
{S_CJK}
{S_PUNCT}
{S_DUP}
{S_DUP}

## Now
The shapes above are the whole point of the page and the padding below is not.
A built page has to carry more than a screenful of prose or build.py's own no-script assertion fails, which would make every cell red for a reason that has nothing to do with writing.
So this section says the same thing several ways, and none of its lines repeats another, because a repeated line would become a second duplicate anchor and quietly change what the duplicate cell is testing.
A board is a folder of Markdown pages plus a generated site, and the site is rebuilt after every accepted write.
The write path never rewrites the site by itself; it edits one Markdown line and then calls the builder.
That ordering is why a test can assert on the Markdown alone and still be asserting on what a reader will see.
The anchor rule is an exact string match, so anything the renderer adds to a sentence has to come back out before the string is posted.
The duplicate rule is a refusal, not a guess, because writing under the wrong copy of a repeated sentence is worse than writing nothing at all.

## Done when
- [ ] JL「{S_PLAIN}」resolve fixture row
- [ ] JL「{S_APP}」resolve fixture row
- [ ] JL「{S_CODE.replace('`', '')}」resolve fixture row
- [ ] JL「{S_BOLD.replace('**', '')}」resolve fixture row
- [ ] JL「The read half of this pair is driven by sentencerun.py.」resolve fixture row
- [ ] JL「{S_CJK}」resolve fixture row
- [ ] JL「{S_PUNCT}」resolve fixture row
- [ ] JL「{S_DUP}」resolve fixture row
- [ ] JL「{S_DUP}」resolve fixture row

## Discussion
> CC: this line was here before the run, so an appended thought has to land after it.

## Log
260801 fixture written by sentencewrite.py.
"""

FIXTURE_Q2 = f"""# The second page, which the write test must never touch

state: 🔴 OPEN
owner: CC
method: a second page carrying a copy of the duplicated sentence, to prove the duplicate refusal is per FILE and not per board

## Opening
Does a sentence repeated on ANOTHER page of the same board change what happens on this one?

## Content
{S_DUP}
A board resolves a write against one file, the one the page names, so a sentence that also exists elsewhere on the board is not a duplicate.
This page also exists so the fixture is a board with more than one page, which is what every real board is.
Nothing in the run posts to this file, so if it ever comes back changed, some write leaked out of its target.

## Log
260801 fixture written by sentencewrite.py.
"""

FIXTURE = {"board.md": FIXTURE_BOARD,
           "QF1-shapes.md": FIXTURE_Q1,
           "QF2-second.md": FIXTURE_Q2}


# ── the shapes, and what each endpoint should do to them ──────────────────
# `posted` is what a browser sends: the RENDERED text, so the markdown the
# renderer consumed (backticks, stars, link syntax) is gone. `source` is the
# line as it sits in the file. They differ exactly for the three markdown
# shapes, which is the whole reason those shapes are here.

SHAPES = [
    ("plain", S_PLAIN, S_PLAIN, False),
    ("apparatus", S_APP, S_APP, False),
    ("code-span",
     "Rebuilding the generated tree after an accepted write is the job of build.py",
     S_CODE, False),
    ("bold",
     "A sentence operation must write exactly one line and leave every other byte alone.",
     S_BOLD, False),
    ("link", "The read half of this pair is driven by sentencerun.py.", S_LINK, False),
    ("cjk", S_CJK, S_CJK, False),
    ("punct", S_PUNCT, S_PUNCT, False),
    ("twice", S_DUP, S_DUP, True),
]

ENDPOINTS = ["sentence", "comment", "edit-sentence", "discuss", "resolve"]

PAGE = "QF1-shapes.md"


# ── the oracle: where a record BELONGS, written from the rule, not the code ──

def record_slot(lines, i):
    """Where a new record for the sentence on line `i` belongs.

    The rule is "directly under the sentence, at the end of any `>` run already
    there": a reader scans a sentence's apparatus top to bottom and the newest
    record is the bottom one. Deliberately NOT imported from live/write.py: an
    oracle that shares the implementation cannot catch the implementation."""
    j = i + 1
    while j < len(lines) and lines[j].lstrip().startswith(">"):
        j += 1
    return j


def discuss_slot(lines):
    """Where a free-standing thought belongs: the end of the `## Discussion`
    section, above the blank line that separates it from the next heading."""
    di = next((i for i, ln in enumerate(lines) if re.match(r"^## Discussion\b", ln)), None)
    if di is None:
        return None
    j = di + 1
    while j < len(lines) and not re.match(r"^## ", lines[j]):
        j += 1
    while j > di + 1 and not lines[j - 1].strip():
        j -= 1
    return j


def anchor_index(text, source, first=False):
    """Line index of one fixture sentence. The fixture owns its own text, so
    this matches exactly rather than re-deriving the server's fuzzy matcher."""
    lines = text.split("\n")
    hits = [i for i, ln in enumerate(lines) if ln.strip() == source.strip()]
    if not hits or (len(hits) > 1 and not first):
        raise SystemExit(f"fixture is broken: {len(hits)} lines equal {source[:40]!r}")
    return hits[0]


# ── HTTP ──────────────────────────────────────────────────────────────────

def post(url, endpoint, payload):
    req = urllib.request.Request(f"{url}/_board/{endpoint}",
                                 data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"},
                                 method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:              # a refusal is a 400 with a body
        body = e.read()
        try:
            return e.code, json.loads(body)
        except ValueError:
            return e.code, {"ok": False, "err": body.decode("utf-8", "replace")[:200]}


# ── the case table ────────────────────────────────────────────────────────
# One row per (shape, endpoint). `want` is the promise being tested:
#   line   · one added line, exact text, at the oracle's slot
#   undo   · one added line matching a pattern PLUS the anchor rewritten
#   flip   · no line added, one character changed on one row
#   refuse · nothing written and a message saying why

def cases(shape, endpoint):
    key, posted, source, dup = shape
    tag = f"{key}/{endpoint}"
    if endpoint == "sentence":
        p = {"file": PAGE, "sentence": posted, "lane": "Note",
             "text": f"write test {tag}"}
        return p, ("refuse" if dup else "line"), f"> Note: write test {tag}"
    if endpoint == "comment":
        p = {"file": PAGE, "who": "CC", "sentence": posted,
             "text": f"write test {tag}", "when": WHEN}
        return p, ("refuse" if dup else "line"), f"> CC: write test {tag} · {WHEN}"
    if endpoint == "edit-sentence":
        p = {"file": PAGE, "sentence": posted, "replacement": posted + " Edited.",
             "who": "CC", "when": WHEN}
        # A markdown-carrying sentence is refused ON PURPOSE (live/write.py:191):
        # the browser posts rendered text, so accepting it would silently drop
        # the link, the code span or the bold from the source.
        want = "refuse" if (dup or posted != source) else "undo"
        return p, want, rf"> ✎ .+ · CC · {re.escape(WHEN)}"
    if endpoint == "discuss":
        # Not anchored to a sentence at all, so no shape can refuse it. It still
        # earns a cell per shape because the shape's own characters are what
        # travel through the body.
        p = {"file": PAGE, "who": "CC", "text": f"write test {tag}: {posted}"}
        one_line = " ".join(f"write test {tag}: {posted}".split())
        return p, "discuss", f"> CC: {one_line}"
    p = {"file": PAGE, "quote": posted, "done": True}
    return p, ("refuse" if dup else "flip"), None


def run_case(url, board_path, fixture, shape, endpoint, pristine):
    """One cell: restore, post, read the markdown back, then post again."""
    key, posted, source, dup = shape
    payload, want, expect = cases(shape, endpoint)
    payload["path"] = board_path
    f = fixture / PAGE
    before = f.read_text(encoding="utf-8")
    status, body = post(url, endpoint, payload)
    after = f.read_text(encoding="utf-8")
    err = (body or {}).get("err") or ""

    # every cell also has to leave every OTHER file alone: a write that resolves
    # the wrong file is invisible to any check that only reads its own target.
    for name, text in pristine.items():
        if name != PAGE and (fixture / name).read_text(encoding="utf-8") != text:
            return "LEAK", f"the write changed {name}, which it never named", err

    if want == "refuse":
        if body.get("ok"):
            # Say WHICH line it picked: "it guessed" is the accusation, and the
            # line it landed on is the evidence for it.
            return "WROTE", (f"status {status}, and it chose: {where(before, after)}"
                             if after != before else
                             f"status {status}, though nothing changed on disk"), err
        if after != before:
            return "BAD", "refused and wrote anyway", err
        return "REF", "", err

    if not body.get("ok"):
        return "ERR", f"status {status}", err

    # ── ① one line, ② in the right place, ③ nothing else moved ──
    bl = before.split("\n")
    if want == "line":
        at = record_slot(bl, anchor_index(before, source))
        wanted = "\n".join(bl[:at] + [expect] + bl[at:])
        if after != wanted:
            return "BAD", where(wanted, after), err
    elif want == "discuss":
        at = discuss_slot(bl)
        wanted = "\n".join(bl[:at] + [expect] + bl[at:])
        if after != wanted:
            return "BAD", where(wanted, after), err
    elif want == "undo":
        i = anchor_index(before, source)
        al = after.split("\n")
        at = record_slot(bl, i)
        if len(al) != len(bl) + 1:
            return "BAD", f"{len(al) - len(bl)} lines added, expected 1", err
        if not re.fullmatch(expect, al[at] or ""):
            return "BAD", f"the record landed wrong: line {at} is {al[at]!r}", err
        undone = al[:at] + al[at + 1:]
        undone[i] = bl[i]                       # put the original sentence back
        if "\n".join(undone) != before:
            return "BAD", where(before, "\n".join(undone)), err
        if after.split("\n")[i] != posted + " Edited.":
            return "BAD", f"the sentence itself is {after.split(chr(10))[i]!r}", err
    elif want == "flip":
        row = f"- [ ] JL「{posted}」resolve fixture row"
        i = anchor_index(before, row)
        wanted = "\n".join(bl[:i] + [row.replace("- [ ]", "- [x]", 1)] + bl[i + 1:])
        if after != wanted:
            return "BAD", where(wanted, after), err

    # ── the same operation twice must not land twice ──
    # A Save button that is clicked twice, a reload that replays a POST, an
    # agent that retries a timeout: all of them post the identical body again.
    status2, body2 = post(url, endpoint, payload)
    twice = f.read_text(encoding="utf-8")
    if twice != after:
        if want == "flip" and body2.get("ok"):
            return "OK", "", err               # flipping x to x changes nothing
        # Name the line that now exists twice, and say how many of it there are:
        # "the file changed" is not actionable, "this record is on the page 2×" is.
        rows = twice.split("\n")
        grew = [ln for ln in set(rows) if rows.count(ln) > after.split("\n").count(ln)]
        worst = max(grew, key=rows.count) if grew else ""
        return "DUP", (f"the identical POST landed again: {worst[:60]!r} is now on "
                       f"the page {rows.count(worst)}×"), err
    return "OK", "", err


# ── probes the shape × endpoint grid cannot express ───────────────────────
# Each one is a payload a REAL widget on the page can produce, aimed at a branch
# the grid never reaches. Same promise as every cell: one line, right place,
# nothing else.

PROBES = [
    # The sentence-comment box is a <textarea> (assets/js/.../10-select.js), so
    # a comment can carry a newline the moment someone presses Enter or pastes
    # two lines. `add_sentence` and `add_discuss` collapse whitespace before
    # writing; `add_comment` only strips the ends.
    ("comment", PAGE, "multi-line comment",
     {"who": "CC", "sentence": S_PLAIN, "text": "first line\nsecond line",
      "when": WHEN}),
    # The same input on the sibling endpoint, as the control that says the grid
    # above is not simply blind to newlines.
    ("discuss", PAGE, "multi-line discussion",
     {"who": "CC", "text": "first line\nsecond line"}),
    # The other branch of add_discuss: a page with no `## Discussion` at all has
    # to grow one above `## Log`, which is a different code path from appending.
    ("discuss", "QF2-second.md", "discussion section created",
     {"who": "CC", "text": "this page had no Discussion section before now"}),
]


def run_probe(url, board_path, fixture, endpoint, page, label, payload, pristine):
    payload = dict(payload, path=board_path, file=page)
    f = fixture / page
    before = f.read_text(encoding="utf-8")
    status, body = post(url, endpoint, payload)
    after = f.read_text(encoding="utf-8")
    if not body.get("ok"):
        return "ERR", f"status {status}: {body.get('err')}"
    for name, text in pristine.items():
        if name != page and (fixture / name).read_text(encoding="utf-8") != text:
            return "LEAK", f"the write changed {name}, which it never named"
    grew = len(after.split("\n")) - len(before.split("\n"))
    if label == "discussion section created":
        # one line for the heading, one for the record, one blank separator
        want = "\n".join(["## Discussion", f"> CC: {payload['text']}", ""])
        return ("OK", "") if want in after and grew == 3 else (
            "BAD", f"{grew} lines added and the new section reads "
                   f"{after[after.find('## Discussion'):][:80]!r}")
    # A record is a `>` RUN, not one line: a person who types three lines gets
    # `> WHO: first` plus a bare `>` continuation per line, which the renderer
    # folds back into ONE lane. The oracle therefore checks the GRAMMAR, not a
    # line count. What must never happen is a line that does not begin with `>`,
    # because that one is not part of the record at all: it lands in the page as
    # prose (JL 260801: "sentence 2 and 3 end up outside the comment").
    stray = [ln for ln in after.split("\n") if ln not in before.split("\n")]
    typed = len([ln for ln in payload.get("text", "").split("\n") if ln.strip()])
    escaped = [ln for ln in stray if ln.strip() and not ln.lstrip().startswith(">")]
    if escaped:
        return "BAD", f"{len(escaped)} line(s) escaped the record into the page: {escaped}"
    if grew != max(typed, 1):
        return "BAD", (f"{grew} lines added for {typed} typed line(s); "
                       f"the record reads {stray}")
    if stray and not re.match(r"^>\s*\w+:", stray[0]):
        return "BAD", f"the record does not open with a `> WHO:` head: {stray[0]!r}"
    return "OK", ""


def where(wanted, got):
    """The first line that differs, which is the only part of a 90-line file a
    reader needs in order to see what went wrong."""
    a, b = wanted.split("\n"), got.split("\n")
    for i in range(max(len(a), len(b))):
        x = a[i] if i < len(a) else "<eof>"
        y = b[i] if i < len(b) else "<eof>"
        if x != y:
            return f"line {i}: expected {x[:64]!r}, got {y[:64]!r}"
    return "files differ but no line does (line count?)"


# ── fixture lifecycle ─────────────────────────────────────────────────────

def build_fixture(fixture):
    """Write the fixture and BUILD it, because a folder the builder rejects is
    not a board and every cell after it would be red for the wrong reason."""
    if fixture.exists():
        shutil.rmtree(fixture)
    fixture.mkdir(parents=True)
    for name, text in FIXTURE.items():
        (fixture / name).write_text(text, encoding="utf-8")
    r = subprocess.run([sys.executable, str(HERE / "cli" / "build.py"), str(fixture)],
                       capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"the fixture does not build:\n{r.stdout}{r.stderr}")
    return r.stdout.strip()


def restore(fixture, pristine):
    for name, text in pristine.items():
        p = fixture / name
        if p.read_text(encoding="utf-8") != text:
            p.write_text(text, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--url", default="http://127.0.0.1:5599",
                    help="an ALREADY RUNNING serve.py; this script starts nothing")
    ap.add_argument("--root", default=str(REPO),
                    help="the --root that server was started with")
    ap.add_argument("--fixture", default="",
                    help="where to put the throwaway board (must sit inside --root)")
    ap.add_argument("--keep", action="store_true",
                    help="leave the fixture on disk for a post-mortem")
    a = ap.parse_args()

    root = Path(a.root).resolve()
    fixture = Path(a.fixture).resolve() if a.fixture else (
        root / "Tools/plugins/haipipe-toolkit/skills/diagrams/_fixture-sentencerun")
    if fixture.exists() and not a.fixture:
        fixture = fixture.with_name(fixture.name + "-tmp")
    try:
        fixture.relative_to(root)
    except ValueError:
        raise SystemExit(f"the fixture must sit inside --root, or the server "
                         f"will refuse every write: {fixture}")

    print(build_fixture(fixture))
    pristine = {n: (fixture / n).read_text(encoding="utf-8") for n in FIXTURE}
    board_path = "/" + fixture.relative_to(root).as_posix() + "/board.md"
    print(f"🎯 {board_path}\n")

    rows, probes, fails, refusals = [], [], [], {}
    try:
        for shape in SHAPES:
            cells = []
            for endpoint in ENDPOINTS:
                restore(fixture, pristine)
                code, why, err = run_case(a.url, board_path, fixture, shape,
                                          endpoint, pristine)
                cells.append(code)
                if err:
                    refusals.setdefault(err, []).append(f"{shape[0]}/{endpoint}")
                if code not in ("OK", "REF"):
                    fails.append((shape[0], endpoint, code, why))
            rows.append((shape[0], cells))
        for endpoint, page, label, payload in PROBES:
            restore(fixture, pristine)
            code, why = run_probe(a.url, board_path, fixture, endpoint, page,
                                  label, payload, pristine)
            probes.append((label, endpoint, code))
            if code != "OK":
                fails.append((label, endpoint, code, why))
    finally:
        restore(fixture, pristine)
        if not a.keep:
            shutil.rmtree(fixture, ignore_errors=True)

    head = "shape".ljust(11) + "".join(e.ljust(15) for e in ENDPOINTS)
    print(head)
    print("-" * len(head))
    for name, cells in rows:
        print(name.ljust(11) + "".join(c.ljust(15) for c in cells))
    print("\nOK  wrote one line, in the right slot, nothing else, and not twice")
    print("REF refused, as this shape must be, and wrote nothing")
    print("ERR refused a write that should have landed   "
          "BAD wrote, but not what was promised")
    print("DUP the second identical post wrote a second line   "
          "WROTE wrote where it had to refuse")
    print("LEAK changed a file the request never named")

    print("\nprobes (one payload each, aimed at a branch the grid never reaches)")
    for label, endpoint, code in probes:
        print(f"  {code:<6} {endpoint:<14} {label}")

    if refusals:
        print("\nmessages the server gave:")
        for msg, who in sorted(refusals.items()):
            print(f"  {len(who):>2}× {msg}")
            print(f"      {', '.join(who)}")

    if fails:
        print(f"\n{len(fails)} cell(s) failed:")
        for name, endpoint, code, why in fails:
            print(f"  {code:<6} {name}/{endpoint}: {why}")
        return 1
    print(f"\n✅ {len(SHAPES) * len(ENDPOINTS)} cells "
          f"({len(SHAPES)} shapes × {len(ENDPOINTS)} endpoints) + "
          f"{len(PROBES)} probes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
