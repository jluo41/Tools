#!/usr/bin/env python3
"""check.py — the structural half of QA9, run against one board.

QA9 rules that a change gets TWO checks on ONE trigger: a structural pass, which
is decidable by machine, and a cold read by a zero-background agent, which is
not. This file is only the first. It exists because the second cannot be
automated and the first should never have needed a human.

What it does NOT do, and cannot:
  · judge whether the prose is readable — that is the cold read
  · judge whether a page's claims about the code are TRUE. On 2026-07-26 a page
    said the drawer AI had comments "injected into its system prompt"; the
    markdown was flawless, every construct rendered, and the sentence was simply
    false for three days. A structural pass is fully compatible with a page that
    is confidently wrong.

Three families:
  BOARD     board.md: Pages against disk, declared Links resolve, ids unique
  PAGE      each Q*/S* md: required sections, state value, references resolve,
            one sentence per line, no em-dash, English-only
  SITE      the built board/ tree: local links and media resolve, tags balance,
            ids unique
  TEMPLATE  render ref/page-template.md as a Q and as an S, then assert each
            construct QA9 names produced its class. A construct the template
            never exercises is reported as a GAP, not skipped (QA9's 🕳 item).

Shares the renderer's section aliases, state tokens, and page discovery helpers
from src/common.py. The checker keeps independent structural assertions because
its job is to compare the documented contract with what the renderer accepts.

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
from urllib.parse import unquote

HERE = Path(__file__).resolve().parent.parent  # the engine dir (this file lives in cli/)
sys.path.insert(0, str(HERE))
from src.common import ALIAS, STN, aim_progress, page_files  # noqa: E402

ERROR, WARN, GAP = "ERROR", "WARN", "GAP"
STATE_LABELS = {"✅": "SETTLED", "🟡": "PARTIAL", "🔴": "OPEN", "⏸": "ON HOLD"}
# The generated Board site can link to live server routes. They do not resolve
# as files beside an HTML page, so checker must recognize them rather than
# calling the Board Home navigation a dead static href.
LIVE_ROUTE_PREFIXES = ("/_board/", "/_excalidraw", "/boards")

# Sections a page cannot be complete without. Aliases are accepted because old
# boards still use them and ALIAS is the renderer's own table.
REQUIRED = ["Opening", "Done when", "Now"]

# QA9's construct table: source form -> the class the renderer must produce.
# Kept in this order so the report reads like the table on that page.
CONSTRUCTS = [
    ("lead is the door",     "details.it.row.qd",  r'<details class="it row qd"', r"^## (?:Opening|Question)\s*$"),
    ("Opening never folds",  "div.ch.opening-head", r'class="ch opening-head"',   r"^## (?:Opening|Question)\s*$"),
    ("drawer is flat",       "div.fh",             r'<div class="fh"',            r"^## (?:Boundary|Stage Contract)\s*$"),
    ("division",             "details.csec",       r'<details class="csec"',      r"^### "),
    ("paragraph heading",    "div.ph",             r'<div class="ph"',            r"^#### "),
    ("job line",             "div.pj",             r'<div class="pj"',            r"^\([^)]+\)\s*$"),
    ("group title",          "div.gt > span.gi",   r'<div class="gt"',            r"(?m)^\*\*[^*\n]+\*\*\s*\n[-*] "),
    ("sentence apparatus",   "details.sent",       r'<details class="sent"',      r"^> (?:Citation|Value|Display|Check|Q-consumer|Link|Source|Note):"),
    ("sentence badge",       "span.sbadge",        r'class="sbadge"',             r"^> (?:Citation|Value|Display|Check|Q-consumer|Link|Source|Note):"),
    ("typed lane",           "div.lane",           r'<div class="lane"',          r"^> (?:Citation|Value|Display|Check|Q-consumer|Link|Source|Note):"),
    ("item with detail",     "details.it.row",     r'<details class="it row"',    r"(?m)^- (?:\[[ xX]\] )?.+\n {2,}\S"),
    ("aim count",            "n/m in the heading", r'\d+/\d+',                    r"(?m)^- (?:A\d+(?:\.\d+)*|P\d+(?:\.\d+)*) ·"),
    ("dated item",           "span.stmp",          r'class="stmp"',               r"^(?:- )?\d{6}(?: \d{4})? "),
    ("code block",           "details.codef",      r'<details class="it codef"',  r"^```"),
    ("excalidraw canvas",    "div.xcal",           r'<div class="xcal"',          r"^(?:/_excalidraw/|https://app\.excalidraw\.com/)"),
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


def section_text(text, canon):
    """Return one section using the renderer's alias table."""
    names = "|".join(re.escape(name) for name in alias_names(canon))
    found = re.search(rf"(?ms)^##\s+(?:{names})\s*$\n?(.*?)(?=^##\s+|\Z)", text)
    return found.group(1).strip() if found else ""


def state_token(value):
    """Return the renderer's normalized four-state machine token."""
    value = value.strip()
    if not value:
        return ""
    return value.split()[0].replace("\ufe0f", "")


def strip_fences(text, prose_only=False):
    """Yield (lineno, line) for lines OUTSIDE fenced code blocks.

    Every check that reads prose has to do this. A figure legitimately contains
    long lines, em-dashes and box characters, and flagging them is how a checker
    trains people to ignore it.

    `prose_only` also skips `<!-- haipipe:… -->` MANAGED SPANS (JL 260727).
    Those hold derived content: a stage's inherited contract, a skill file, a
    changelog converted into Log lines. The board did not write that text and
    cannot fix it without falsifying a quote, so style rules about the board's
    own prose do not apply to it. Converting one skill's changelog produced 79
    such warnings in a single pass, which is exactly how a checker teaches
    people to stop reading its output.
    """
    fence, managed = False, False
    for i, ln in enumerate(text.split("\n"), 1):
        st = ln.lstrip()
        if st.startswith("```"):
            fence = not fence
            continue
        if prose_only and st.startswith("<!--") and "haipipe:" in st:
            managed = ":start" in st
            continue
        if not fence and not (prose_only and managed):
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

    if not re.search(r"^#\s+\S", text, re.M):
        rep.add(ERROR, "board-missing-title", "board.md", "no `# title` line")
    for canon in ("Topic", "Pipeline", "Pages"):
        if not has_section(text, canon):
            shown = " / ".join(alias_names(canon))
            rep.add(ERROR, "board-missing-section", "board.md", f"no `## {shown}` section")

    # Not every rule is universal. The haipipe-paper board rules that `state:`
    # is about the DECISION and implementation intent lives in Aims, so
    # a ✅ page there legitimately carries unticked boxes. Detected by reading
    # what the board says about itself, which is fragile: a board has no way to
    # DECLARE which rules it opts out of, and that gap is an item on QA9.
    decision_only = bool(re.search(
        r"`?state:`?[^\n]{0,80}\b(is about|means)\b[^\n]{0,40}\bDECISION\b", text, re.I))

    for key in ("spine", "close"):
        if not re.search(rf"^{key}:\s*\S", text, re.M):
            rep.add(ERROR, "board-missing-key", "board.md",
                    f"no `{key}:` line; the board cannot say what it is for or when it ends")

    pages = {p.name: p for p in page_files(d)}
    listed = re.findall(r"^((?:[QS]|Agent-|Meeting-)[^\s/]*\.md)\s*$", text, re.M)
    for name in listed:
        if name not in pages:
            rep.add(ERROR, "pages-ghost", f"board.md -> {name}",
                    "## Pages names a file that is not on disk")
    for name in sorted(pages):
        if name not in listed:
            rep.add(WARN, "not-in-pages", name,
                    "on disk but not in ## Pages, so it renders under the ⚠️ group")
    seen = {}
    for name in sorted(pages):
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
    return pages, links, decision_only


def check_face(path, name, rep, links, page_ids, decision_only=False):
    text = path.read_text(encoding="utf-8")

    if not re.search(r"^#\s+\S", text, re.M):
        rep.add(ERROR, "missing-title", name, "no `# title` line")
    for canon in REQUIRED:
        if not has_section(text, canon):
            shown = " / ".join(alias_names(canon))
            rep.add(ERROR, "missing-section", name, f"no `## {shown}` section")
    # `Skill-<unit>-<slug>` is the SKILL page kind (JL 260731), not a stage: it
    # mirrors a shipped unit and has no gate, so the stage sections are not owed.
    if name.startswith("S") and not name.startswith("Skill-"):
        for canon in ("Stage Contract", "Content"):
            if not has_section(text, canon):
                shown = " / ".join(alias_names(canon))
                rep.add(ERROR, "missing-stage-section", name,
                        f"S page has no required `## {shown}` section")

    m = re.search(r"^state:\s*(.+?)\s*$", text, re.M)
    token = state_token(m.group(1)) if m else ""
    if not m:
        rep.add(ERROR, "no-state", name, "no `state:` line")
    elif token not in STN:
        rep.add(ERROR, "bad-state", f"{name}:{text[:m.start()].count(chr(10)) + 1}",
                f"state is {m.group(1)!r}; its first token must be one of "
                + " · ".join(f"{emoji} {label}" for emoji, label in STATE_LABELS.items())
                + "; an optional human-readable suffix may follow")

    if not re.search(r"^owner:\s*\S", text, re.M):
        rep.add(ERROR, "no-owner", name, "no `owner:` line, so nobody is named as responsible")

    # A page id in backticks should resolve, either to a declared Link or to a
    # file on this board. Historical mentions of a retired id look identical to
    # live references today, which is why these are WARN: see the retired-id
    # convention item on QA9.
    for lineno, ln in strip_fences(text, prose_only=True):
        for tok in re.findall(r"`([QS][A-Za-z]*\d+[a-z]?(?:@\w+)?)`", ln):
            if tok in links or tok in page_ids:
                continue
            rep.add(WARN, "unresolved-id", f"{name}:{lineno}",
                    f"`{tok}` is neither a page on this board nor a declared Link")

    # English-only and the em-dash ban are rules about the prose THIS TEAM
    # writes. A `Meeting-<n>` page is a mirror of a meeting that happened, in
    # whatever language it happened in, and "fixing" its wording would falsify
    # the record (QC10). Its managed spans are already skipped by strip_fences;
    # this exempts the two seeded lists as well, which are the meeting's own
    # action items and open questions and are equally quotations.
    quoted = bool(re.match(r"^Meeting-\d+-", Path(name).name))
    for lineno, ln in strip_fences(text, prose_only=True):
        if "—" in ln and not quoted:
            rep.add(WARN, "em-dash", f"{name}:{lineno}", "em-dash in prose (JL 260724)")
        if re.search(r"[一-鿿]", ln) and not quoted:
            rep.add(WARN, "cjk", f"{name}:{lineno}", "CJK in a board that is English-only (JL 260724)")

    # One sentence per line: the page gives every prose line its own row, so a
    # hard wrap mid-sentence becomes a broken row the reader sees.
    #
    # Only inside prose. The `state:` / `owner:` / `method:` header is lowercase
    # and unterminated by design, and a first draft of this rule flagged three
    # lines on every page for it, which is how a checker teaches people to stop
    # reading its output.
    prev_open, in_prose = False, False
    for lineno, ln in strip_fences(text, prose_only=True):
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
    # in State renders as a decorated title in front of prose.
    lines = text.split("\n")
    fence = False
    managed = False
    for i, ln in enumerate(lines):
        st = ln.lstrip()
        if st.startswith("```"):
            fence = not fence
            continue
        if st.startswith("<!--") and "haipipe:" in st:   # derived, not our prose
            managed = ":start" in st
            continue
        if fence or managed or not re.match(r"^\*\*(.+?)\*\*\s*$", ln.strip()):
            continue
        nxt = next((x for x in lines[i + 1:i + 4] if x.strip()), "")
        # A run of #### paragraph headings is a group too (JL 260801). A long
        # division groups its paragraphs rather than leaving eleven of them in
        # one flat run, and that grouping is exactly what a group title is for;
        # the rule was only ever written against `- item` runs because that was
        # the only kind of run that existed when it was made.
        if not nxt.strip().startswith(("- ", "* ", "#### ")):
            rep.add(WARN, "bold-not-a-group-title", f"{name}:{i + 1}",
                    "a whole-line **bold** renders as a group title with 🔹, but prose follows it, "
                    "not a run of items (QA4 §3)")

    progress = aim_progress(section_text(text, "Done when"),
                            section_text(text, "Now"))
    met, total, closed = progress["met"], progress["total"], progress["closed"]
    st = token
    # Aim/state alignment is a Q ruling heuristic, not an S gate rule.
    # A lifecycle S page may pass its human gate while retaining follow-up work,
    # or show partial work before that gate. Its first emoji is authoritative.
    if not name.startswith("Q") or decision_only:
        pass          # S gate semantics, or a Q board's declared decision-only variant
    elif st == "✅" and closed != total:
        rep.add(WARN, "settled-with-open-aims", name,
                f"state is SETTLED with {total - closed} open Aim(s); on a Q every Aim must close")
    # The two staleness shapes, both real: a page that was worked on and never
    # written back reads OPEN with ticks under it (QA4a said "nothing is built
    # and nothing is decided" while the thing was running, JL 260726), and a
    # page that finished and was never closed reads PARTIAL with nothing left.
    # SKILL.md's `sync` action already requires the write-back; this is the only
    # thing that notices when a session skips it.
    elif st == "🔴" and met:
        rep.add(WARN, "open-with-met-aims", name,
                f"state is OPEN with {met}/{total} Aim(s) met; "
                "either the state is stale or the Aim State is (SKILL.md `sync`)")
    elif st == "🟡" and total and closed == total:
        rep.add(WARN, "partial-with-nothing-open", name,
                "state is PARTIAL with every Aim closed; either it is SETTLED "
                "or an Aim is missing (SKILL.md `sync`)")
    if total == 0:
        rep.add(WARN, "no-aims", name, "no Aims at all, so nothing defines done")

    check_opening(text, name, rep)
    check_group_names(text, name, rep)
    check_one_canvas(text, name, rep)
    check_division_figures(text, name, rep)
    check_comment_form(text, name, rep)
    check_file_paths(text, name, rep, path.parent)


# QB4 §1 states seven rules for the Opening and NOT ONE of them was checked, so
# the same Opening was written wrong four times in one day and a second session
# wrote the same mistake back while the first was fixing it (JL 260801: "为什么
# 你不 follow 我们现在的 guideline 呢？还是我们 skill 没有强调这一点？"). Four of
# the seven are mechanical, so they belong here rather than in a reviewer's head.
# The other three (one idea, not interchangeable, reads alone) need a reader,
# which is QF1's second instrument.
# QB4 §1 sets no sentence quota: one central idea controls the length. This is
# the ceiling that catches Content leaking into the Opening, and it allows the
# bearing JL asked for on 260801 (2-3 lines placing the page) plus its stake.
OPENING_MAX_PITCH = 10
OPENING_MAX_CLAUSES = 3        # commas plus semicolons before a sentence sprawls
# The ON-STAGE paragraph is everything above ## Opening's FIRST BLANK LINE, and
# it is the only prose a reader gets without clicking. JL 260801 capped it at
# 4-5 sentences, about five lines on screen; measured on the joined render, that
# is roughly 450 characters, and this ceiling leaves a little air above it.
OPENING_MAX_STAGE_CHARS = 520


def check_opening(text, name, rep):
    """The mechanical half of QB4 §1's Opening contract."""
    body = section_text(text, "Opening")
    if not body:
        rep.add(WARN, "opening-empty", name,
                "no Opening at all; QB4 §1 says every page of every kind opens")
        return
    # strip_fences yields (lineno, line): a figure may legitimately be long
    raw = [ln.rstrip() for _, ln in strip_fences(body, prose_only=True)]
    # everything above the FIRST BLANK LINE is what the reader sees on stage
    onstage = []
    for ln in raw:
        if not ln.strip():
            if onstage:
                break
            continue
        onstage.append(ln)
    prose = [ln for ln in raw if ln.strip()]
    if not prose:
        rep.add(WARN, "opening-empty", name, "Opening has a heading and no prose")
        return

    # 1 · the lead is an actual question, and it is the first thing on stage
    lead = prose[0].strip()
    if not lead.endswith("?"):
        rep.add(WARN, "opening-lead-not-a-question", f"{name}:1",
                "the Opening lead must be one actual question (QB4 §1); "
                f"it reads {lead[:60]!r}")

    # 2 · the ON-STAGE paragraph is what a reader sees, and it is capped
    #     (JL 260801). build.py splits ## Opening on its FIRST BLANK LINE:
    #     above it is the visible paragraph, below it is the More details
    #     drawer. So the budget is measured on the lines above that blank
    #     line, joined the way the renderer joins them, not on the section.
    stage_para = " ".join(x.strip() for x in onstage).strip()
    if stage_para and len(stage_para) > OPENING_MAX_STAGE_CHARS:
        rep.add(WARN, "opening-paragraph-too-long", f"{name}:1",
                f"the on-stage paragraph is {len(stage_para)} chars against a "
                f"ceiling of {OPENING_MAX_STAGE_CHARS} (QB4 §1: 4-5 sentences, "
                "about five lines on screen); move the extra below the first "
                "blank line and it lands in More details")
    # The old line-count ceiling is retired (JL 260801). It counted every prose
    # line in ## Opening, which conflates the on-stage paragraph with the More
    # details drawer; the drawer is behind a click and has no budget. The
    # on-stage character ceiling above is the rule that replaced it.

    # 3 · no attribution parentheticals: a date belongs in the Log
    for i, ln in enumerate(prose):
        if re.search(r"\((?:JL|CC)[^)]*\d{6}[^)]*\)", ln):
            rep.add(WARN, "opening-attribution", f"{name}:{i + 1}",
                    "attribution parenthetical in the Opening; QB4 §1 puts the date in the Log")

    # 4 · one idea per sentence, because a stuffed sentence is unreadable
    #     (JL 260801, on one sentence that fed the reader everything at once)
    for i, ln in enumerate(onstage or [lead]):
        for sent in re.split(r"(?<=[.?!])\s+", ln):
            n = sent.count(",") + sent.count(";") + sent.count(":")
            if n > OPENING_MAX_CLAUSES and len(sent) > 140:
                rep.add(WARN, "opening-sentence-stuffed", f"{name}:{i + 1}",
                        f"one sentence carrying {n} clauses in {len(sent)} chars; "
                        "split it, the Opening is read cold")


def check_file_paths(text, name, rep, board_dir=None):
    """Every backticked path in `## Files` must resolve (JL 260802).

    Files is the action map, and a stale path is worse than no path: the
    reader only discovers it is dead after following it. Prose can be wrong
    and still read as prose; a path is either right or a dead end. QB4 itself
    carried four dead ones by 260802, because `build.py` and `stage.py` moved
    into `cli/` and `assets/board.css` was split into `assets/css/*.css`.

    Resolved against the ENGINE dir first, then the board folder, then the
    repo root, because a Files row may point at any of the three.
    """
    block = section_text(text, "Files") or ""
    roots = [HERE, HERE.parent]
    if board_dir:
        d = Path(board_dir)
        # a Files row may be written relative to the PAGE's own folder, to the
        # board root, or to the repo root; all three are legitimate and in use.
        roots += [d, d.parent]
        root = next((p for p in d.resolve().parents
                     if (p / "pyproject.toml").is_file()), None)
        if root:
            roots.append(root)
    for m in re.finditer(r"(?m)^\s*[-*]\s+`([^`]+)`", block):
        raw = m.group(1).strip()
        for cand in raw.split(" · "):
            cand = cand.strip().strip("`")
            if not cand or " " in cand or not re.search(r"[./]", cand):
                continue
            if any((r / cand).exists() for r in roots):
                continue
            if "*" in cand:            # a glob row, e.g. assets/css/*.css
                continue
            rep.add(WARN, "dead-file-path", f"{name} · Files",
                    f"`{cand}` does not resolve from the engine, the board, "
                    "or the repo root (QB4 §6.3.1)")


def check_comment_form(text, name, rep):
    """A sentence comment is written `> Comment WHO …` (JL 260802).

    The bare-initial form `> JL: …` still RENDERS, so nothing already written
    breaks, but it is not the form to write: beside `> Citation:` and
    `> Value:` a pair of initials tells a newcomer nothing about what the row
    is. Only Content is checked. `## Discussion` keeps `> JL:` / `>> CC0726:`
    deliberately: that is a THREAD with nested replies, a different grammar in
    a different section, and 156 rows across the boards use it.
    """
    content = section_text(text, "Content") or ""
    fence = False
    for i, ln in enumerate(content.split("\n"), 1):
        if ln.lstrip().startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        m = re.match(r"^>\s*([A-Z]{1,4}\d{0,4})\s*[「\"]?.*?[:：]", ln)
        if m and not re.match(r"^>\s*(Citation|Value|Display|Check|Q-consumer|"
                              r"Link|Source|Note|Comment)\b", ln, re.I):
            rep.add(WARN, "old-comment-form", f"{name} · Content",
                    f"`> {m.group(1)}:` is the legacy sentence-comment form; "
                    f"write `> Comment {m.group(1)} …` (QB4 §3.3.3)")


def check_division_figures(text, name, rep):
    """Every Content division opens with a caption line and a fenced figure.

    QB4 §3.3.1: caption, figure, short intro, in that order, before any prose.
    The figure is drawn with /diagram-ascii; the caption is `**Name**: what
    this diagram shows.` (JL 260801). Both are easy to forget on a new
    division, and neither failure reports itself at render.
    """
    content = section_text(text, "Content") or ""
    parts = re.split(r"(?m)^### (\d+) · (.+)$", content)
    for k in range(1, len(parts), 3):
        num, title, body_ = parts[k], parts[k + 1], parts[k + 2]
        lines = [l for l in body_.split("\n")]
        first = next((l for l in lines if l.strip()), "")
        fenced = any(l.lstrip().startswith("```") for l in lines)
        if not fenced:
            rep.add(WARN, "division-no-figure", f"{name} · §{num}",
                    f"{title.strip()!r} opens with no figure (QB4 §3.3.1)")
        elif not re.match(r"^\*\*[^*]+\*\*\s*:", first.strip()):
            rep.add(WARN, "division-no-caption", f"{name} · §{num}",
                    f"{title.strip()!r} has a figure with no caption line above "
                    "it (QB4 §2.2: `**Name**: what this diagram shows.`)")


def check_one_canvas(text, name, rep):
    """A page attaches at most ONE Excalidraw canvas (JL 260801).

    Two forms exist and both are legal on their own: `/_excalidraw/?board=…`
    is the board's own scene, and `https://app.excalidraw.com/s/…` is a scene
    hosted elsewhere. The renderer embeds EVERY canvas URL it finds, so two
    lines silently produce two canvases and no reader can tell which is the
    current drawing.
    """
    dia = section_text(text, "Diagram") or ""
    urls, fence = [], False
    for ln in dia.split("\n"):
        if ln.lstrip().startswith("```"):
            fence = not fence
            continue
        s2 = ln.strip()
        if fence or not s2:
            continue
        if re.match(r"^(?:/_excalidraw/|https?://(?:app\.)?excalidraw\.com/)\S*$", s2):
            urls.append(s2)
    if len(urls) > 1:
        rep.add(WARN, "two-canvases", f"{name} · Diagram",
                f"{len(urls)} canvas URLs; a page attaches one (QB4 §2.7). "
                f"Keep either the board scene or the hosted link, not both")


def check_group_names(text, name, rep):
    """An Aims or States group must carry its Content division's id AND name.

    JL 260801: "could they share the same name? like the division name in the
    Content can be used by the Aims and States as well." Five of QB4's six
    groups already did; the sixth was still named for a topic its division had
    stopped carrying, and nothing reported it because nothing compared the two
    lists. `P` is exempt: a page-level target belongs to no single division.
    """
    def groups(sec_name, pat):
        block = section_text(text, sec_name) or ""
        return dict(re.findall(pat, block, re.M))

    divs = groups("Content", r"^### (\d+) · (.+)$")
    if not divs:
        return
    for sec_name in ("Aims", "States"):
        # `A<n>` is the id (JL 260802): the group holds A-records, so naming it
        # `C3` made the reader translate one letter into another for no gain.
        # `C<n>` still resolves, since older boards are full of it.
        found = groups(sec_name, r"^### A(\d+) · (.+)$")
        found.update(groups(sec_name, r"^### C(\d+) · (.+)$"))
        for gid, gname in found.items():
            want = divs.get(gid)
            gname = re.sub(r"^\W+\s*", "", gname)   # the group's own emoji
            if want is None:
                rep.add(WARN, "group-no-division", f"{name} · {sec_name} C{gid}",
                        f"`C{gid}` names no Content division on this page")
            elif want.strip() != gname.strip():
                rep.add(WARN, "group-name-drift", f"{name} · {sec_name} C{gid}",
                        f"reads {gname.strip()!r}; its division `### {gid}` is "
                        f"{want.strip()!r} (QB4 §0.5: same id, same name)")


def check_page(d, rep):
    """The built site: local hrefs resolve, tags balance, ids are unique.

    Checks the split site (QC9). The monolithic board.html was retired 260731,
    so every page is now its own file and each one is checked on its own terms:
    a broken link on QD2 used to be one finding among thousands in a 1.1MB
    document, and is now named by the file it is in.
    """
    site = d / "board"
    if not (site / "index.html").exists():
        rep.add(ERROR, "no-html", "board/index.html", "not built yet; run build.py")
        return
    pages = sorted(site.glob("*.html")) + sorted(site.glob("*/*.html"))

    for html in pages:
        name = html.relative_to(site).as_posix()
        t = html.read_text(encoding="utf-8")
        bare = re.sub(r"<script.*?</script>", "", t, flags=re.S)
        body = bare.split("<body", 1)[-1]

        # Scripts-off completeness, on the page files only: a group file and the
        # index are navigation, so they are legitimately short.
        if html.parent != site:
            plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body)).strip()
            if len(plain) < 400:
                rep.add(ERROR, "zero-script", name,
                        f"only {len(plain)} chars survive with scripts stripped; "
                        "the page depends on JS")

        # `bare`, not `t`: a URL inside JavaScript is a string in a program,
        # not a rendered resource. Check href, img/iframe src, and object data
        # together: the split-site reroot bug fixed href while leaving the
        # evidence-card image and PDF visibly broken (260801).
        resources = sorted(set(re.findall(
            r'(href|src|data)="([^"#][^"]*)"', bare)))
        for attr, href in resources:
            if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", href):
                continue
            if href.startswith(LIVE_ROUTE_PREFIXES):
                continue
            href = href.split("#", 1)[0].split("?", 1)[0]
            if not href:
                continue
            # A rendered href is URL-ENCODED and a filesystem path is not, so
            # `fig/image copy.png` ships as `fig/image%20copy.png` and this
            # check called a file that exists a dead link (found 260801, on a
            # figure pasted into board.md with a space in its name).
            href = unquote(href)
            if not (html.parent / href).exists():
                rep.add(ERROR, f"dead-{attr}", f"{name} -> {href}",
                        f"rendered {attr} does not resolve")

        ids = re.findall(r'id="([^"]+)"', t)
        for fragment in sorted(set(re.findall(r'href="#([^"]+)"', bare))):
            if fragment not in ids:
                rep.add(ERROR, "dead-fragment", f"{name} -> #{fragment}",
                        "rendered fragment does not exist in this file")
        for i in sorted({x for x in ids if ids.count(x) > 1}):
            rep.add(ERROR, "duplicate-html-id", f"{name} #{i}",
                    f"id appears {ids.count(i)} times")

        # Tag balance, counted outside <script> AND <style>. Both quote markup
        # in their comments: board.css explains the apparatus with the words
        # "native <details>", and counting that reported three unclosed tags on
        # a page whose markup was fine.
        markup = re.sub(r"<style.*?</style>", "", bare, flags=re.S)
        for tag in ("details", "section", "div"):
            o = len(re.findall(rf"<{tag}[\s>]", markup))
            c = len(re.findall(rf"</{tag}>", markup))
            if o != c:
                rep.add(ERROR, "unbalanced-tag", name,
                        f"<{tag}> opened {o} times, closed {c}")


# Every class token a chip PANEL carries. A panel's class list is
# `chipcard <kind> <state>`, so each of these is a live class on a top-layer
# element, and a bare `.<token>{}` rule anywhere in board.css also styles the
# panel. That is not hypothetical: `.fig`, written for markdown images, matched
# every figure panel and its `display:block` beat the UA rule that hides a
# closed popover, so five invisible full-width panels lay across the page and
# swallowed every click for a day (QA9, JL 260726).
# `chipcard` itself is NOT in the list: styling the panel's own base class
# bare is the correct way to style a panel. The danger is the OTHER tokens,
# which are kind and state words a page might plausibly want for something else.
PANEL_TOKENS = ("disp", "fig", "tab", "num", "val", "cite", "qref",
                "ok", "ready", "owed", "parked", "broken", "unowned", "unver", "amb")
BARE_CLASS = re.compile(r"(?m)^\s*((?:\.[A-Za-z][\w-]*\s*,\s*)*\.([A-Za-z][\w-]*))\s*\{")


def check_css(rep):
    """A bare class selector that collides with a chip panel's own classes.

    The failure this catches renders perfectly and reads perfectly: the page is
    correct, the prose is correct, and the interaction is dead. Neither of QA9's
    other two instruments can see it, which is why it gets its own.
    """
    from src import assets as _a
    for m in BARE_CLASS.finditer(_a.css()):
        for sel in m.group(1).split(","):
            tok = sel.strip().lstrip(".")
            if tok in PANEL_TOKENS:
                line = css.read_text(encoding="utf-8").count("\n", 0, m.start()) + 1
                rep.add(ERROR, "panel-class-collision", f"assets/board.css:{line}",
                        f"bare `.{tok}` also matches a chip panel "
                        f"(class=\"chipcard <kind> <state>\"); scope it to a tag "
                        f"or rename it, or it can un-hide a closed popover")


def check_template(rep, quiet):
    """Render ref/page-template.md as a Q page and as an S page, then assert.

    The template is the fixture because it is the file authors copy. Checking a
    hand-written specimen would let the template rot while the specimen passed.
    """
    tpl = HERE / "ref" / "page-template.md"
    if not tpl.exists():
        rep.add(ERROR, "no-template", "ref/page-template.md", "the fixture is missing")
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

        r = subprocess.run([sys.executable, str(HERE / "cli" / "build.py"), str(d)],
                           capture_output=True, text=True)
        if r.returncode != 0:
            rep.add(ERROR, "template-build-failed", "ref/page-template.md",
                    (r.stderr or r.stdout).strip().split("\n")[-1][:200])
            return
        # One document per page since the monolith was retired (260731). The
        # construct assertions below only ask "does this markup appear
        # somewhere", so concatenating the page files is the same question, and
        # page_slice still finds its own section boundaries inside the join.
        html = "\n".join(p.read_text(encoding="utf-8")
                         for p in sorted((d / "board").glob("*/*.html")))

        for label, cls, pattern, source_pattern in CONSTRUCTS:
            source_has = bool(re.search(source_pattern, src, re.M))
            rendered_has = bool(re.search(pattern, html))
            if not source_has:
                rep.add(GAP, "template-gap", f"ref/page-template.md · {label}",
                        f"the template source never exercises {cls}, so the construct is "
                        "documented and untested")
            elif not rendered_has:
                rep.add(ERROR, "template-renderer-drift", f"ref/page-template.md · {label}",
                        f"the template exercises this construct but the rendered fixture has no {cls}")

        if 'class="slide q' not in html:
            rep.add(ERROR, "template-no-page", "ref/page-template.md", "rendered to no page at all")
        if html.count('class="slide q') < 2:
            rep.add(ERROR, "template-one-mode", "ref/page-template.md",
                    "the fixture did not render as both a Q page and an S page")

        def page_slice(page_id):
            marker = f'id="{page_id}"'
            at = html.find(marker)
            if at < 0:
                return ""
            start = html.rfind('<section class="slide q', 0, at)
            end = html.find('<section class="slide q', at + len(marker))
            return html[start:end if end >= 0 else len(html)]

        q_html = page_slice("QT1")
        s_html = page_slice("S-Main-1")
        mode_checks = [
            ("Q rationale in Opening", q_html, r'<div class="fh">More details</div>'),
            ("Q has no Stage Contract drawer", q_html, r"^(?![\s\S]*<div class=\"fh\">Stage Contract</div>)[\s\S]*$"),
            ("Q Content heading stays plain", q_html, r"📚 Content(?!\s*·)"),
            ("S rationale in Opening", s_html, r'<div class="fh">More details</div>'),
            ("S Stage Contract in Opening", s_html, r'<div class="fh">Stage Contract</div>'),
            ("S Content heading names the stage", s_html, r"📚 Content · Main 1 Fixture"),
        ]
        for label, page_html, pattern in mode_checks:
            if not page_html or not re.search(pattern, page_html):
                rep.add(ERROR, "template-mode-contract", f"ref/page-template.md · {label}",
                        "the shared source did not render with the documented Q/S-specific placement")


def main():
    ap = argparse.ArgumentParser(description="structural half of QA9")
    ap.add_argument("board", help="the board folder")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 on any ERROR (JL's ruling on blocking is open; default reports)")
    ap.add_argument("--quiet", action="store_true", help="findings only, no summary")
    ap.add_argument("--no-template", action="store_true",
                    help="skip the template fixture (it shells out to build.py)")
    ap.add_argument("--summary", action="store_true",
                    help="score instead of a list: findings per rule and the "
                         "worst pages, so 'how are we doing' is one command")
    a = ap.parse_args()

    d = Path(a.board).resolve()
    rep = Report()
    pages, links, decision_only = check_board(d, rep)
    page_ids = set()
    for name in pages:
        m = re.match(r"([QS][A-Za-z0-9]*\d+[a-z]?)", name)
        if m:
            page_ids.add(m.group(1))
    for name, p in sorted(pages.items()):
        check_face(p, name, rep, links, page_ids, decision_only)
    check_page(d, rep)
    check_css(rep)
    if not a.no_template:
        check_template(rep, a.quiet)

    order = {ERROR: 0, WARN: 1, GAP: 2}
    if a.summary:
        # The findings ARE the measurement (QB4 §9). A list of 285 rows says
        # nothing about whether the board is improving; a count per rule and a
        # worst-pages column does, and a page at zero is the one to copy.
        import collections
        by_code, by_page = collections.Counter(), collections.Counter()
        for level, code, where, _ in rep.rows:
            by_code[(level, code)] += 1
            by_page[where.split(" ·")[0].split(" ->")[0]] += 1
        print(f"{len(pages)} pages · {len(rep.rows)} findings\n")
        print(f"{'rule':<26} {'level':<6} {'count':>6}")
        print("-" * 40)
        for (level, code), n in sorted(by_code.items(), key=lambda x: -x[1]):
            print(f"{code:<26} {level:<6} {n:>6}")
        clean = [n for n in sorted(pages) if not by_page.get(n)]
        print(f"\n{'page':<40} {'findings':>8}")
        print("-" * 50)
        for name, n in by_page.most_common(8):
            print(f"{name:<40} {n:>8}")
        print(f"\nclean pages: {len(clean)} of {len(pages)}")
        if clean:
            print("  " + " · ".join(clean[:8]) + ("  …" if len(clean) > 8 else ""))
        return 1 if (a.strict and rep.counts().get(ERROR)) else 0
    for level, code, where, msg in sorted(rep.rows, key=lambda r: (order[r[0]], r[1], r[2])):
        print(f"{where:<44} {level:<5} {code:<24} {msg}")

    c = rep.counts()
    if not a.quiet:
        print(f"\n{len(pages)} pages · "
              f"{c.get(ERROR, 0)} error · {c.get(WARN, 0)} warn · {c.get(GAP, 0)} gap")
        if not rep.rows:
            print("nothing structural to report. The cold read is the other half; "
                  "this says nothing about whether the page can be read.")
    return 1 if (a.strict and c.get(ERROR)) else 0


if __name__ == "__main__":
    sys.exit(main())
