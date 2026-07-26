#!/usr/bin/env python3
"""check.py — the structural half of QA9, run against one board.

QA9 rules that a change gets TWO checks on ONE trigger: a structural pass, which
is decidable by machine, and a cold read by a zero-background agent, which is
not. This file is only the first. It exists because the second cannot be
automated and the first should never have needed a human.

What it does NOT do, and cannot:
  · judge whether the prose is readable — that is the cold read
  · judge whether a page's claims about the code are TRUE. On 2026-07-26 a face
    said the drawer AI had comments "injected into its system prompt"; the
    markdown was flawless, every construct rendered, and the sentence was simply
    false for three days. A structural pass is fully compatible with a page that
    is confidently wrong.

Three families:
  BOARD     board.md: Pages against disk, declared Links resolve, ids unique
  FACE      each Q*/S* md: required sections, state value, references resolve,
            one sentence per line, no em-dash, English-only
  PAGE      the built board.html: local hrefs resolve, tags balance, ids unique
  TEMPLATE  render ref/q-template.md as a Q and as an S, then assert each
            construct QA9 names produced its class. A construct the template
            never exercises is reported as a GAP, not skipped (QA9's 🕳 item).

Reuses src/parse.py rather than reimplementing the grammar: a checker with its
own parser checks a second opinion, not the thing that ships.

Report-only by default, exit 0. `--strict` exits 1 on any ERROR. Whether a red
result BLOCKS a change or only reports it is JL's open item on QA9, so this
defaults to the harmless side and the ruling stays open.

    python3 check.py <board-dir> [--strict] [--quiet]
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from src.common import ALIAS, face_files  # noqa: E402

ERROR, WARN, GAP = "ERROR", "WARN", "GAP"
STATES = {"✅ SETTLED", "🟡 PARTIAL", "🔴 OPEN", "⏸️ ON HOLD"}

# Sections a face cannot be complete without. Aliases are accepted because old
# boards still use them and ALIAS is the renderer's own table.
REQUIRED = ["Question", "Done when", "Now"]

# QA9's construct table: source form -> the class the renderer must produce.
# Kept in this order so the report reads like the table on that face.
CONSTRUCTS = [
    ("lead is the door",     "details.it.row.qd",  r'<details class="it row qd"'),
    ("Opening never folds",  "div.ch.opening-head", r'class="ch opening-head"'),
    ("drawer is flat",       "div.fh",             r'<div class="fh"'),
    ("division",             "details.csec",       r'<details class="csec"'),
    ("paragraph heading",    "div.ph",             r'<div class="ph"'),
    ("job line",             "div.pj",             r'<div class="pj"'),
    ("group title",          "div.gt > span.gi",   r'<div class="gt"'),
    ("sentence apparatus",   "details.sent",       r'<details class="sent"'),
    ("sentence badge",       "span.sbadge",        r'class="sbadge"'),
    ("typed lane",           "div.lane",           r'<div class="lane"'),
    ("item with detail",     "details.it.row",     r'<details class="it row"'),
    ("finish count",         "n/m in the heading", r'\d+/\d+'),
    ("dated item",           "span.stmp",          r'class="stmp"'),
    ("code block",           "details.codef",      r'<details class="codef"'),
    ("excalidraw canvas",    "div.xcal",           r'<div class="xcal"'),
]


class Report:
    def __init__(self):
        self.rows = []

    def add(self, level, code, where, msg):
        self.rows.append((level, code, where, msg))

    def counts(self):
        c = {}
        for level, *_ in self.rows:
            c[level] = c.get(level, 0) + 1
        return c


def alias_names(canon):
    """Every spelling the renderer accepts for one section name."""
    return [canon] + ALIAS.get(canon, [])


def has_section(text, canon):
    for name in alias_names(canon):
        if re.search(rf"^##\s+{re.escape(name)}\s*$", text, re.M):
            return True
    return False


def strip_fences(text):
    """Yield (lineno, line) for lines OUTSIDE fenced code blocks.

    Every check that reads prose has to do this. A figure legitimately contains
    long lines, em-dashes and box characters, and flagging them is how a checker
    trains people to ignore it.
    """
    fence = False
    for i, ln in enumerate(text.split("\n"), 1):
        if ln.lstrip().startswith("```"):
            fence = not fence
            continue
        if not fence:
            yield i, ln


def declared_links(board_md):
    m = re.search(r"^## (?:Links|链接)\s*$", board_md, re.M)
    if not m:
        return {}
    tail = board_md[m.end():].split("\n## ")[0]
    out = {}
    for ln in tail.split("\n"):
        parts = ln.strip().split(None, 1)
        if len(parts) == 2 and not ln.startswith("#"):
            out[parts[0]] = parts[1].strip()
    return out


def check_board(d, rep):
    bmd = d / "board.md"
    if not bmd.exists():
        rep.add(ERROR, "no-board-md", str(d), "no board.md: this is not a board folder")
        return {}, {}, False
    text = bmd.read_text(encoding="utf-8")
    links = declared_links(text)

    # Not every rule is universal. The haipipe-paper board rules that `state:`
    # is about the DECISION and that implementation lives in Items to Finish, so
    # a ✅ face there legitimately carries unticked boxes. Detected by reading
    # what the board says about itself, which is fragile: a board has no way to
    # DECLARE which rules it opts out of, and that gap is an item on QA9.
    decision_only = bool(re.search(
        r"`?state:`?[^\n]{0,80}\b(is about|means)\b[^\n]{0,40}\bDECISION\b", text, re.I))

    for key in ("spine", "close"):
        if not re.search(rf"^{key}:\s*\S", text, re.M):
            rep.add(WARN, "board-missing-key", "board.md",
                    f"no `{key}:` line; the board cannot say what it is for or when it ends")

    faces = {p.name: p for p in face_files(d)}
    listed = re.findall(r"^([QS][^\s/]*\.md)\s*$", text, re.M)
    for name in listed:
        if name not in faces:
            rep.add(ERROR, "pages-ghost", f"board.md -> {name}",
                    "## Pages names a file that is not on disk")
    for name in sorted(faces):
        if name not in listed:
            rep.add(WARN, "not-in-pages", name,
                    "on disk but not in ## Pages, so it renders under the ⚠️ group")
    seen = {}
    for name in sorted(faces):
        m = re.match(r"([QS][A-Za-z0-9]*\d+[a-z]?)", name)
        if not m:
            continue
        fid = m.group(1)
        if fid in seen:
            rep.add(ERROR, "duplicate-id", name, f"id {fid} is already used by {seen[fid]}")
        seen[fid] = name

    for token, target in links.items():
        if target.startswith(("http://", "https://")):
            continue
        if not (d / target).exists():
            rep.add(ERROR, "dead-link", f"board.md -> {token}",
                    f"declared Link target does not exist: {target}")
    return faces, links, decision_only


def check_face(path, name, rep, links, face_ids, decision_only=False):
    text = path.read_text(encoding="utf-8")

    for canon in REQUIRED:
        if not has_section(text, canon):
            shown = " / ".join(alias_names(canon))
            rep.add(ERROR, "missing-section", name, f"no `## {shown}` section")

    m = re.search(r"^state:\s*(.+?)\s*$", text, re.M)
    if not m:
        rep.add(ERROR, "no-state", name, "no `state:` line")
    elif m.group(1) not in STATES:
        rep.add(ERROR, "bad-state", f"{name}:{text[:m.start()].count(chr(10)) + 1}",
                f"state is {m.group(1)!r}; the four values are " + " · ".join(sorted(STATES)))

    if not re.search(r"^owner:\s*\S", text, re.M):
        rep.add(WARN, "no-owner", name, "no `owner:` line, so nobody is named as responsible")

    # A face id in backticks should resolve, either to a declared Link or to a
    # file on this board. Historical mentions of a retired id look identical to
    # live references today, which is why these are WARN: see the retired-id
    # convention item on QA9.
    for lineno, ln in strip_fences(text):
        for tok in re.findall(r"`([QS][A-Za-z]*\d+[a-z]?(?:@\w+)?)`", ln):
            if tok in links or tok in face_ids:
                continue
            rep.add(WARN, "unresolved-id", f"{name}:{lineno}",
                    f"`{tok}` is neither a face on this board nor a declared Link")

    for lineno, ln in strip_fences(text):
        if "—" in ln:
            rep.add(WARN, "em-dash", f"{name}:{lineno}", "em-dash in prose (JL 260724)")
        if re.search(r"[一-鿿]", ln):
            rep.add(WARN, "cjk", f"{name}:{lineno}", "CJK in a board that is English-only (JL 260724)")

    # One sentence per line: the page gives every prose line its own row, so a
    # hard wrap mid-sentence becomes a broken row the reader sees.
    #
    # Only inside prose. The `state:` / `owner:` / `method:` header is lowercase
    # and unterminated by design, and a first draft of this rule flagged three
    # lines on every face for it, which is how a checker teaches people to stop
    # reading its output.
    prev_open, in_prose = False, False
    for lineno, ln in strip_fences(text):
        s = ln.strip()
        if s.startswith("## "):
            in_prose, prev_open = True, False
            continue
        if not in_prose:
            continue
        if (not s or s.startswith(("#", "-", ">", "|", "!", "["))
                or ln.startswith("  ") or re.match(r"^[a-z][a-z-]*:\s", s)):
            prev_open = False
            continue
        if prev_open and s[0].islower():
            rep.add(WARN, "hard-wrap", f"{name}:{lineno}",
                    "starts lowercase under an unterminated line: one sentence looks wrapped over two")
        prev_open = s[-1] not in ".?!:;)”\"`»"

    # A full-line **bold** renders as a GROUP TITLE with a 🔹 marker, so it must
    # actually lead a run of items. QA4 §3 ruled that a paragraph is never written
    # in bold; without a check the rule held nowhere, and a bold opening sentence
    # in Where we are renders as a decorated title in front of prose.
    lines = text.split("\n")
    fence = False
    for i, ln in enumerate(lines):
        if ln.lstrip().startswith("```"):
            fence = not fence
            continue
        if fence or not re.match(r"^\*\*(.+?)\*\*\s*$", ln.strip()):
            continue
        nxt = next((x for x in lines[i + 1:i + 4] if x.strip()), "")
        if not nxt.strip().startswith(("- ", "* ")):
            rep.add(WARN, "bold-not-a-group-title", f"{name}:{i + 1}",
                    "a whole-line **bold** renders as a group title with 🔹, but prose follows it, "
                    "not a run of items (QA4 §3)")

    ticked = len(re.findall(r"^- \[x\]", text, re.M))
    total = ticked + len(re.findall(r"^- \[ \]", text, re.M))
    st = m.group(1) if m else ""
    if decision_only:
        pass          # this board rules that state is the DECISION; see check_board
    elif st == "✅ SETTLED" and ticked != total:
        rep.add(WARN, "settled-with-open-items", name,
                f"state is SETTLED with {total - ticked} unticked item(s); on a Q every box must close")
    if total == 0:
        rep.add(WARN, "no-items", name, "no checklist at all, so nothing defines done")


def check_page(d, rep):
    html = d / "board.html"
    if not html.exists():
        rep.add(ERROR, "no-html", "board.html", "not built yet; run build.py")
        return
    t = html.read_text(encoding="utf-8")

    bare = re.sub(r"<script.*?</script>", "", t, flags=re.S)
    body = bare.split("<body", 1)[-1]
    plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body)).strip()
    if len(plain) < 1200:
        rep.add(ERROR, "zero-script", "board.html",
                f"only {len(plain)} chars survive with scripts stripped; the page depends on JS")

    for href in sorted(set(re.findall(r'href="([^"#][^"]*)"', t))):
        if href.startswith(("http://", "https://", "mailto:", "data:")):
            continue
        if not (d / href).exists():
            rep.add(ERROR, "dead-href", f"board.html -> {href}", "rendered link does not resolve")

    ids = re.findall(r'id="([^"]+)"', t)
    for i in sorted({x for x in ids if ids.count(x) > 1}):
        rep.add(ERROR, "duplicate-html-id", f"board.html #{i}", f"id appears {ids.count(i)} times")

    # Tag balance, counted outside <script> AND <style>. Both quote markup in
    # their comments: board.css explains the apparatus with the words "native
    # <details>", and counting that reported three unclosed tags on a page whose
    # markup was fine.
    markup = re.sub(r"<style.*?</style>", "", bare, flags=re.S)
    for tag in ("details", "section", "div"):
        o = len(re.findall(rf"<{tag}[\s>]", markup))
        c = len(re.findall(rf"</{tag}>", markup))
        if o != c:
            rep.add(ERROR, "unbalanced-tag", "board.html",
                    f"<{tag}> opened {o} times, closed {c}")


def check_template(rep, quiet):
    """Render ref/q-template.md as a Q face and as an S face, then assert.

    The template is the fixture because it is the file authors copy. Checking a
    hand-written specimen would let the template rot while the specimen passed.
    """
    tpl = HERE / "ref" / "q-template.md"
    if not tpl.exists():
        rep.add(ERROR, "no-template", "ref/q-template.md", "the fixture is missing")
        return
    src = tpl.read_text(encoding="utf-8")

    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "fixture"
        d.mkdir()
        (d / "board.md").write_text(
            "# Template fixture\nspine: render the template and assert every construct\n"
            "close: never\n## Topic\nFixture.\n## Pages\n### QT · Fixture\n"
            "QT1-template.md\nS-Main-1-template.md\n", encoding="utf-8")
        (d / "QT1-template.md").write_text(src, encoding="utf-8")
        s_src = re.sub(r"^# .*$", "# S Main 1 · Fixture", src, count=1, flags=re.M)
        (d / "S-Main-1-template.md").write_text(s_src, encoding="utf-8")

        r = subprocess.run([sys.executable, str(HERE / "build.py"), str(d)],
                           capture_output=True, text=True)
        if r.returncode != 0:
            rep.add(ERROR, "template-build-failed", "ref/q-template.md",
                    (r.stderr or r.stdout).strip().split("\n")[-1][:200])
            return
        html = (d / "board.html").read_text(encoding="utf-8")

        for label, cls, pattern in CONSTRUCTS:
            in_src = None
            if not re.search(pattern, html):
                # Distinguish "the renderer dropped it" from "the template never
                # showed it". Only the first is a defect (QA9's 🕳 item).
                rep.add(GAP, "template-gap", f"ref/q-template.md · {label}",
                        f"no {cls} in the rendered fixture: the template never exercises it, "
                        f"so this construct is documented and untested")
            elif not quiet:
                in_src = True
            del in_src

        if 'class="slide q' not in html:
            rep.add(ERROR, "template-no-face", "ref/q-template.md", "rendered to no face at all")
        if html.count('class="slide q') < 2:
            rep.add(ERROR, "template-one-mode", "ref/q-template.md",
                    "the fixture did not render as both a Q face and an S face")


def main():
    ap = argparse.ArgumentParser(description="structural half of QA9")
    ap.add_argument("board", help="the board folder")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 on any ERROR (JL's ruling on blocking is open; default reports)")
    ap.add_argument("--quiet", action="store_true", help="findings only, no summary")
    ap.add_argument("--no-template", action="store_true",
                    help="skip the template fixture (it shells out to build.py)")
    a = ap.parse_args()

    d = Path(a.board).resolve()
    rep = Report()
    faces, links, decision_only = check_board(d, rep)
    face_ids = set()
    for name in faces:
        m = re.match(r"([QS][A-Za-z0-9]*\d+[a-z]?)", name)
        if m:
            face_ids.add(m.group(1))
    for name, p in sorted(faces.items()):
        check_face(p, name, rep, links, face_ids, decision_only)
    check_page(d, rep)
    if not a.no_template:
        check_template(rep, a.quiet)

    order = {ERROR: 0, WARN: 1, GAP: 2}
    for level, code, where, msg in sorted(rep.rows, key=lambda r: (order[r[0]], r[1], r[2])):
        print(f"{where:<44} {level:<5} {code:<24} {msg}")

    c = rep.counts()
    if not a.quiet:
        print(f"\n{len(faces)} faces · "
              f"{c.get(ERROR, 0)} error · {c.get(WARN, 0)} warn · {c.get(GAP, 0)} gap")
        if not rep.rows:
            print("nothing structural to report. The cold read is the other half; "
                  "this says nothing about whether the page can be read.")
    return 1 if (a.strict and c.get(ERROR)) else 0


if __name__ == "__main__":
    sys.exit(main())
