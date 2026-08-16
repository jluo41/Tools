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
import collections
import os
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import unquote

HERE = Path(__file__).resolve().parent.parent  # the engine dir (this file lives in cli/)
sys.path.insert(0, str(HERE))
from src.common import (ALIAS, STN, AIM_STATE_RE, aim_ids, aim_progress,  # noqa: E402
                        page_files)
from src.page_context import audit_related_rows  # noqa: E402
from src.topic_entry_contract import check_topic_entries  # noqa: E402

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
    ("drawer is flat",       "div.fh",             r'<div class="fh"',            r"^## Stage Contract\s*$"),
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


def outside_checkout(base, target):
    """True when a relative target climbs out of the git checkout `base` is in.

    A board may legitimately cite a neighbouring SPACE (`env.sh`, a platforms/
    tree) that exists on the primary machine and not in a partial checkout.
    From here such a path is UNVERIFIABLE rather than known-dead, and an ERROR
    must mean known-dead (JL 260815). Resolution is lexical: the target's
    `..` climb is compared against the checkout root without touching disk.
    """
    base = Path(base).resolve()
    root = next((p for p in (base, *base.parents) if (p / ".git").exists()), None)
    if root is None:
        return False
    try:
        candidate = (base / target).resolve()
    except OSError:
        return False
    return not str(candidate).startswith(str(root) + "/") and candidate != root


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
    listed = re.findall(r"^((?:[QS]|Agent-|Meeting-|Design-)[^\s/]*\.md)\s*$", text, re.M)
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
            if outside_checkout(d, target):
                # The target climbs out of this git checkout, so from here it
                # is UNVERIFIABLE, not known-dead: on the machine that holds
                # the neighbouring SPACE the same row resolves and stays
                # checked (JL 260815). An ERROR must mean known-dead.
                rep.add(WARN, "outside-checkout", f"board.md -> {token}",
                        f"Link target lives outside this checkout: {target}")
            else:
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
    elif len(m.group(0)) > 110:
        rep.add(WARN, "state-line-long", f"{name}:{text[:m.start()].count(chr(10)) + 1}",
                f"state line is {len(m.group(0))} chars; the row grammar (JL 260816, QPs1 §8) keeps it "
                "under 110: status word, what stands, then `open:` with a short list or a count; "
                "facts belong in States, reasons in Log")

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
        if ln.lstrip().startswith(">"):
            # a sentence's comment or edit record is a quotation of what a
            # person typed, and the record rule forbids editing it; nagging
            # about a line nobody may fix is a checker defect (260815, the
            # same reasoning that exempts Meeting pages above)
            continue
        bare = re.sub(r"`[^`]*`", "", ln)   # a code span quotes the machine
        # a double-quoted span quotes a PERSON, and the board's own record
        # rules value the exact words over the prose rules (JL 260815, the
        # ruling that extended the Meeting exemption): "为啥不按序号来排?" stays
        # verbatim, and the narration around it stays English and dash-free.
        bare = re.sub(r'"[^"\n]*"|“[^”\n]*”', "", bare)
        if "—" in bare and not quoted:
            rep.add(WARN, "em-dash", f"{name}:{lineno}", "em-dash in prose (JL 260724)")
        if re.search(r"[一-鿿]", bare) and not quoted:
            rep.add(WARN, "cjk", f"{name}:{lineno}", "CJK in a board that is English-only (JL 260724)")

    # One sentence per line: the page gives every prose line its own row, so a
    # hard wrap mid-sentence becomes a broken row the reader sees.
    #
    # Only inside prose. The `state:` / `owner:` / `method:` header is lowercase
    # and unterminated by design, and a first draft of this rule flagged three
    # lines on every page for it, which is how a checker teaches people to stop
    # reading its output.
    # A `<!-- … -->` guide comment is instructions, not page prose, and its
    # wrapping is deliberate. `ref/page-template.md` is largely one long
    # comment, so counting it flagged twelve lines on every page copied from
    # the template, which is the fastest way to teach someone to ignore a
    # checker (JL 260802).
    prev_open, in_prose, in_comment = False, False, False
    for lineno, ln in strip_fences(text, prose_only=True):
        s = ln.strip()
        if "<!--" in s:
            in_comment = "-->" not in s.split("<!--", 1)[1]
            prev_open = False
            continue
        if in_comment:
            if "-->" in s:
                in_comment = False
            prev_open = False
            continue
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

    aims_text, states_text = section_text(text, "Done when"), section_text(text, "Now")
    check_state_mirrors_aims(aims_text, states_text, name, rep)
    check_generated_block(text, name, rep)

    progress = aim_progress(aims_text, states_text)
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
    elif st == "🗂":
        # FOLDED is terminal by MERGE, not by completion, so a folded page is
        # never nagged about open Aims: its subject moved to another page and
        # its own rows will never close. Same exemption a Meeting page gets.
        pass
    elif st == "🟡" and total and closed == total:
        rep.add(WARN, "partial-with-nothing-open", name,
                "state is PARTIAL with every Aim closed; either it is SETTLED "
                "or an Aim is missing (SKILL.md `sync`)")
    if total == 0:
        rep.add(WARN, "no-aims", name, "no Aims at all, so nothing defines done")

    check_opening(text, name, rep)
    check_page_type(path, text, name, rep)
    check_group_names(text, name, rep)
    check_one_canvas(text, name, rep)
    check_division_figures(text, name, rep)
    check_comment_form(text, name, rep)
    check_file_paths(text, name, rep, path.parent)
    check_related_board_pages(path, name, text, rep)
    check_canvas_frames(text, name, rep, path.parent)
    check_duplicate_sections(text, name, rep)
    check_retired_sections(text, name, rep)
    check_evidence_pointer(text, name, rep)
    check_fence_balance(text, name, rep)


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
    # everything above the FIRST BLANK LINE is what the reader sees on stage,
    # MINUS the sentence apparatus. `page_question.py` composes the lead as
    # `" ".join(x for x in lead_lines if not x.startswith(">"))` and hands every
    # `>` line to `render_apparatus`, so a `> Citation:` or a `> ✎` record under
    # the lead is a lane the reader opens, never a clause in the paragraph.
    # Counting it as prose made the checker and the renderer disagree about the
    # same fact: one ✎ record on a 340-char lead reported it as 841 chars and
    # flagged the record's own diff as a stuffed sentence (found on QBv1, 260802).
    onstage = []
    for ln in raw:
        if not ln.strip():
            if onstage:
                break
            continue
        if ln.lstrip().startswith(">"):
            continue
        onstage.append(ln)
    prose = [ln for ln in raw if ln.strip() and not ln.lstrip().startswith(">")]
    if not prose:
        rep.add(WARN, "opening-empty", name, "Opening has a heading and no prose")
        return

    # 1 · the lead is an actual question, and it is the first thing on stage
    #
    # ...EXCEPT on a skill page. `Skill-<n>` and `Agent-<n>` mirror a unit that
    # ships elsewhere and DECIDE NOTHING, so `haipipe-page-for-skill` rules
    # the opposite: their Opening INTRODUCES the unit and may never open with a
    # question. Without this exemption the seven pages that obeyed that contract
    # each carried a WARN telling them to put the question back, and a writer
    # working the checker's list would have regressed every one of them. Found by
    # the first real dispatch of haipipe-board-reviewer-agent, 260802.
    lead = prose[0].strip()
    roster = name.startswith(("Skill-", "Agent-"))
    if roster:
        if lead.endswith("?"):
            rep.add(WARN, "skillpage-opening-is-a-question", f"{name}:1",
                    "a skill page decides nothing, so its Opening INTRODUCES "
                    "the unit and never asks (haipipe-page-for-skill); "
                    f"it reads {lead[:60]!r}")
    elif not lead.endswith("?"):
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


RETIRED_SECTIONS = {
    # section name -> why it went, and what does the job now
    "Boundary": "JL 260731; what a page covers is the Opening's job",
    "Question": "renamed to `## Opening` (260731)",
    "Items to Finish": "renamed to `## Aims` (260731)",
    "Where we are": "renamed to `## States` (260731)",
}


def check_evidence_pointer(text, name, rep):
    """An `### E<n>` division's QA-probe pointer must be able to BECOME a link.

    A ```fence is CODE, and the renderer never links or chips anything inside
    code. So a pointer written inside a figure is inert BY CONSTRUCTION: it
    reads exactly like a working one and there is nothing to click.

    `QBt4` shipped that way for a day. Its own Log records the decision that
    caused it: the record anatomy makes `🔗 QA-probe:` the first line of an E
    division and the caption rule makes `**Name**:` the first line of any
    division, so to avoid printing the pointer twice it was moved INSIDE the
    figure. That settled a FORMATTING collision and silently removed a
    FUNCTION. `QBt5`, written the same week with the pointer above the fence,
    rendered its link the whole time, which is what made the cause provable.

    WHY THIS RULE HAD TO EXIST. Every other link check here answers "does this
    href resolve". None of them can see a pointer that never became an href at
    all: a dead link is visible and an ungenerated link is not. That blind spot
    is the reason the same defect kept coming back, so the check is on the
    SOURCE line rather than on the rendered anchor.
    """
    # SCOPED TO AN E DIVISION, because a page that DESCRIBES the pointer is not
    # writing one. The first version flagged QC5, the page that documents this
    # very defect, for quoting the string inside an example figure. A checker
    # that fires on its own documentation is a checker people learn to ignore,
    # which is worse than the defect it catches.
    fence = in_e = False
    divisions, pointers = [], []
    for i, line in enumerate(text.split("\n"), 1):
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if not fence and line.startswith("### "):
            in_e = bool(re.match(r"^###\s+E\d+\s*·", line.strip()))
            if in_e:
                divisions.append((i, line.strip()[:60]))
        if not fence and line.startswith("## "):
            in_e = False
        if in_e and "🔗 QA-probe:" in line:
            pointers.append((i, fence))

    buried = [i for i, f in pointers if f]
    for i in buried:
        rep.add(ERROR, "evidence-pointer-in-fence", f"{name}:{i}",
                "the `🔗 QA-probe:` pointer sits inside a ``` fence, which is "
                "code, so it can never render as a link and there is nothing "
                "for a reader to click. Move it ABOVE the fence and backtick "
                "the path.")
    if divisions and not pointers:
        rep.add(ERROR, "evidence-pointer-missing", f"{name}:{divisions[0][0]}",
                f"{len(divisions)} `### E<n>` division(s) and no `🔗 QA-probe:` "
                "pointer anywhere, so the page names no record to open.")


def check_fence_balance(text, name, rep):
    """An unclosed FENCE swallows the rest of the page, silently.

    Everything after it renders as code: Aims, States, Files and Log come out
    as raw markdown inside one grey box. The page still builds, still passes
    every other check, and still reports 0 errors. JL found it by LOOKING at
    the rendered `QBt5-for-value` on 260807, where a slice edit had removed one
    fence's opening line and left its closing one, so parity was inverted from
    that point to the end of the file.

    Cheap to check and impossible to catch by reading, which is what earns it a
    rule: the damage shows at the BOTTOM of the page and the cause is in the
    middle.
    """
    opens, state, managed = [], False, False
    for i, line in enumerate(text.split("\n"), 1):
        st = line.lstrip()
        # MANAGED SPANS ARE NOT THIS PAGE'S PROSE. A generated mirror page
        # carries another unit's bytes verbatim, fences included, so counting
        # them made parity odd on two pages that render perfectly. Measured
        # 260807: the rule's first version flagged Skill-6 and Skill-8, and
        # both were checked in the RENDERED html and found intact.
        if st.startswith("<!--") and "haipipe:" in st:
            managed = ":start" in st
            continue
        if managed:
            continue
        if st.startswith(FENCE):
            state = not state
            if state:
                opens.append(i)
            elif opens:
                opens.pop()
    if state and opens:
        rep.add(ERROR, "fence-unclosed", "%s:%d" % (name, opens[-1]),
                "a fence is never closed, so every section below it renders as "
                "code. The page still builds and every other check still "
                "passes, which is why this one exists.")


def check_retired_sections(text, name, rep):
    """A section JL retired must not come back, and must not merely be ALIASED.

    `src/common.py` still maps the old names so old pages keep rendering. That
    kindness is exactly why 45 of 55 pages sat on the pre-260731 vocabulary for
    two days while a skill claimed they had all been converted: the render
    looked right, so nothing ever said otherwise. A rename the renderer forgives
    is a rename no one finishes. This check is what makes it finishable.
    """
    for i, line in enumerate(text.split("\n"), 1):
        head = line.strip()
        if not head.startswith("## "):
            continue
        why = RETIRED_SECTIONS.get(head[3:].strip())
        if why:
            # WARN, not ERROR: ERROR is reserved for silent DATA LOSS
            # (`duplicate-section`). This is visible drift, and four sibling
            # boards carry 217 rows of it that are not this sweep's to fix.
            rep.add(WARN, "retired-section", f"{name}:{i}",
                    f"`{head}` was retired: {why}")


def check_duplicate_sections(text, name, rep):
    """A repeated `## ` heading SILENTLY DISCARDS everything under the first.

    `split_sections` in `src/parse.py` builds a dict, so the later block wins
    and the earlier one never reaches the render. Nothing reported it: the
    page looks whole in the editor and is short on the page. QB2a carried two
    `## Where we are` headings for two days, and roughly 4.6 KB of dated
    post-mortems under the first had never been seen by anyone (found by a
    fresh-context agent on 260802, not by any check).

    This is an ERROR rather than a warning because it is silent data loss.
    """
    seen, fence = {}, False
    for i, ln in enumerate(text.split("\n"), 1):
        if ln.lstrip().startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        m = re.match(r"^##\s+(\S.*?)\s*$", ln)
        if not m:
            continue
        head = m.group(1)
        if head in seen:
            rep.add(ERROR, "duplicate-section", f"{name}:{i}",
                    f"`## {head}` also at line {seen[head]}; the render keeps "
                    "only the LAST one and silently drops everything under the "
                    "first (QB4 §8.2.2)")
        else:
            seen[head] = i


_FRAMES = {}


def _canvas_frames(board_dir):
    """Frame names in the board's own `board.excalidraw`, cached per board."""
    root = Path(board_dir)
    for _ in range(4):                      # a page sits in a group folder
        scene = root / "board.excalidraw"
        if scene.exists():
            break
        root = root.parent
    else:
        return None
    key = str(scene)
    if key not in _FRAMES:
        try:
            data = json.loads(scene.read_text(encoding="utf-8"))
            _FRAMES[key] = {e.get("name", "") for e in data.get("elements", [])
                            if e.get("type") == "frame"}
        except Exception:
            _FRAMES[key] = None
    return _FRAMES[key]


def check_canvas_frames(text, name, rep, board_dir=None):
    """A `&frame=<id>` that names no frame in `board.excalidraw` links to nothing.

    `serve_frame()` 404s, but the page still LOOKS like it has a drawing, so the
    gap only shows when someone clicks. Three fresh-context agents hit this on
    260802 from three different pages, which is how it got measured at all.
    """
    frames = _canvas_frames(board_dir)
    if not frames:
        return
    for i, line in enumerate(text.split("\n"), 1):
        if line.lstrip().startswith(("#", ">")):
            continue
        for m in re.finditer(r"[&?]frame=([A-Za-z0-9_-]+)", line):
            fid = m.group(1)
            if fid not in frames:
                rep.add(WARN, "dead-canvas-frame", f"{name}:{i}",
                        f"`frame={fid}` names no frame in `board.excalidraw`, "
                        "so the link 404s (QB4 §2.7)")


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
        # Climb to the board root instead of assuming it is one level up: a
        # folded page (`<name>/<name>.md`, JL 260815) sits one level deeper,
        # and the fixed `[d, d.parent]` silently dropped board-relative
        # resolution for every folded page.
        roots.append(d)
        for p in d.resolve().parents:
            roots.append(p)
            if (p / "board.md").is_file():
                break
        root = next((p for p in d.resolve().parents
                     if (p / "pyproject.toml").is_file()), None)
        if root:
            roots.append(root)
    # EVERY backticked path in the row, not only the first. A row written
    # `- `a.py` · `b.py`` had its second path silently unchecked, which is how
    # QB5 reported one dead path while carrying five (260802).
    for row in re.finditer(r"(?m)^\s*[-*]\s+(`[^`]+`(?:\s*[·,]\s*`[^`]+`)*)", block):
        for m in re.finditer(r"`([^`]+)`", row.group(1)):
            raw = m.group(1).strip()
            for cand in raw.split(" · "):
                cand = cand.strip().strip("`")
                if not cand or " " in cand or not re.search(r"[./]", cand):
                    continue
                if any((r / cand).exists() for r in roots):
                    continue
                if "*" in cand or "<" in cand or ">" in cand:
                    # a glob (assets/css/*.css) or an angle-bracketed placeholder
                    # (<path/to/thing.py>) names a shape, not a file. The template
                    # is copied for every new page, so its example rows must not
                    # arrive pre-broken (JL 260802).
                    continue
                if cand.split("/")[0].startswith("."):
                    # runtime state (`.haipipe-board/activity.sqlite3`) exists
                    # only after the server has run; its absence proves nothing
                    continue
                if board_dir and outside_checkout(Path(board_dir), cand):
                    rep.add(WARN, "outside-checkout", f"{name} · Files",
                            f"`{cand}` lives outside this checkout")
                    continue
                rep.add(WARN, "dead-file-path", f"{name} · Files",
                        f"`{cand}` does not resolve from the engine, the board, "
                        "or the repo root (QB4 §6.3.1)")


def check_related_board_pages(path, name, text, rep):
    """Validate the typed, scoped Page links under Files (QB4 §6.4).

    Ordinary Files rows may point anywhere the work continues. A Related Board
    Pages row is narrower: its target must be a real Page on this Board, its
    visible Page id must agree with that source, and its requested Content scope
    must exist. Those facts are deterministic, so malformed context never waits
    for an agent to discover it during DRAFT, PROBE, REVISE, or CHECK.
    """
    for finding in audit_related_rows(path, text):
        level = ERROR if finding.level == "ERROR" else WARN
        rep.add(level, finding.code, f"{name}:{finding.line}", finding.message)


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
        # `Card` joins the named lanes (JL 260802). Without it, `> Card SPAN
        # of words: …` matched the bare-initials shape as author "C", so every
        # span card on the board reported itself as a legacy comment.
        if m and not re.match(r"^>\s*(Citation|Value|Display|Check|Q-consumer|"
                              r"Link|Source|Note|Comment|Card)\b", ln, re.I):
            rep.add(WARN, "old-comment-form", f"{name} · Content",
                    f"`> {m.group(1)}:` is the legacy sentence-comment form; "
                    f"write `> Comment {m.group(1)} …` (QB4 §3.3.3)")


# One marker pair per generator, so two blocks can share a page: `form:` is
# section-stats.py, `units:` is dash.py, `evidence:` is evidence.py. They shared
# one pair until 260806, when dash.py silently deleted both other blocks from
# three pages on its first run. The checker reads whichever names it finds.
GEN_BEGIN = re.compile(r"^# --- (\w+):begin \(generated\) ---$", re.M)
GEN_MEASURED = re.compile(r"MEASURED\s+(20\d\d-\d\d-\d\d|\b2\d{5}\b)")
GEN_REGEN = re.compile(r"(?m)^\s*regenerate:\s*(\S+)")
ANY_DATE = re.compile(r"(20\d\d-\d\d-\d\d|\b2\d{5}\b)")


def _ymd(token):
    """`260727` and `2026-07-27` are both in use; compare them as one shape."""
    t = token.replace("-", "")
    return t[2:] if len(t) == 8 else t


def check_generated_block(text, name, rep):
    """A measured block must say when it was measured, and not be older than
    the page it measures.

    Every other page type closes on an event: a display is accepted, a stage
    passes its gate, a skill's unit ships. A measured block has no such moment,
    which is why `for-dashboard` failed the admission test's fourth question on
    260806. What it has instead is FRESHNESS, and freshness is checkable, so the
    thing that would have been a closing rule becomes this.

    The page's own newest Log date is the reference rather than the file's
    mtime, because a clone resets every mtime and the Log travels with the file.

    Measured on the MISQ board the day the rule was written: seven of eight
    section pages carried a block measured 2026-07-27 whose page had logged work
    through 260803, and the S-Main dashboard was still reporting a section that
    had been archived. Its own prose is the argument for this check: a wrong
    measurement is worse than none, because it reads as measured.
    """
    blocks = []
    for m in GEN_BEGIN.finditer(text):
        tag = m.group(1)
        tail = text[m.end():].split(f"# --- {tag}:end ---", 1)
        blocks.append((tag, tail[0]))
    if not blocks:
        return
    log = section_text(text, "Log")
    latest = max((_ymd(d) for d in ANY_DATE.findall(log)), default="")
    for tag, block in blocks:
        _one_generated_block(tag, block, latest, name, rep)


def _one_generated_block(tag, block, latest, name, rep):
    stamp = GEN_MEASURED.search(block)
    if not stamp:
        rep.add(WARN, "generated-block-undated", name,
                "a generated block carries no `MEASURED <date>` line, so nothing "
                "can tell whether it describes the page as it stands")
    if not GEN_REGEN.search(block):
        rep.add(WARN, "generated-block-no-command", name,
                "a generated block carries no `regenerate:` line, so a reader who "
                "finds it stale has no way to refresh it")

    if stamp and latest and _ymd(stamp.group(1)) < latest:
        rep.add(WARN, "generated-block-stale", f"{name} · {tag}",
                f"the block was measured {_ymd(stamp.group(1))} and this page has "
                f"logged work through {latest}, so it measures a version that no "
                "longer exists")


def check_state_mirrors_aims(aims_text, states_text, name, rep):
    """Every Aim id carries exactly one status row in States.

    Aims say what should become true; States says what is true now, one row per
    Aim id. `aim_progress` reads the rows and defaults a missing one to ⬜, so a
    page that never wrote States renders as 0 of N and looks untouched. That is
    the failure this catches, and it was invisible until 260806, when writing
    the ten Page Type templates walked eight specimens and found five of them
    missing EVERY row: 11 of 11 on one page, 7 of 7, 6 of 6, 8 of 9, 3 of 3.

    The opposite direction is worse and this catches it too. A row for an id no
    Aim declares reads as progress on a target that does not exist; QA4 rendered
    P1 ✅ through P5 ✅ while zero of its seven slides had been accepted.

    Legacy checkbox pages are exempt: they carry their state in the box, which
    is why `aim_progress` reads them by a different path.
    """
    if re.search(r"(?m)^\s*[-*]\s*\[[ xX]\]", aims_text or ""):
        return                                  # legacy checklist, state in the box
    declared = aim_ids(aims_text)
    if not declared:
        return
    rows = [aim_id for _emoji, aim_id in AIM_STATE_RE.findall(states_text or "")]
    seen = collections.Counter(rows)

    missing = [a for a in declared if not seen[a]]
    if missing:
        shown = " · ".join(missing[:6]) + (" …" if len(missing) > 6 else "")
        rep.add(WARN, "aim-without-state", name,
                f"{len(missing)} of {len(declared)} Aim(s) carry no row in States, "
                f"so each renders as ⬜ and the page reads less done than it is: {shown}")

    twice = sorted(a for a, n in seen.items() if n > 1 and a in declared)
    if twice:
        rep.add(WARN, "aim-stated-twice", name,
                "States carries two rows for the same Aim, so which one counts is "
                f"whichever the parser met last: {' · '.join(twice)}")

    stray = sorted(a for a in seen if a not in declared)
    if stray:
        rep.add(WARN, "state-without-aim", name,
                "States reports progress on an id no Aim declares, so the page "
                f"shows work against a target that does not exist: {' · '.join(stray)}")


def check_division_figures(text, name, rep):
    """Every Content division opens with a caption line and a fenced figure.

    QB4 §3.3.1: caption, figure, short intro, in that order, before any prose.
    The figure is drawn with /diagram-ascii; the caption is `**Name**: what
    this diagram shows.` (JL 260801). Both are easy to forget on a new
    division, and neither failure reports itself at render.
    """
    content = section_text(text, "Content") or ""
    # `### §1 Demonstration` and `### 6.1 · x` are divisions too. Matching only
    # `### <digit> · ` made every §-numbered part INVISIBLE to this check, so
    # the board's figure count was understated (found by a fresh-context agent
    # on QB5, 260802, not by any check).
    parts = re.split(r"(?m)^### §?([\d.]+)(?: · | )(.+)$", content)
    for k in range(1, len(parts), 3):
        num, title, body_ = parts[k], parts[k + 1], parts[k + 2]
        lines = [l for l in body_.split("\n")]
        first = next((l for l in lines if l.strip()), "")
        fenced = any(l.lstrip().startswith("```") for l in lines)
        # A rendered media embed is a figure in the renderer's own vocabulary
        # (`img.fig`, `object.figpdf`, `.fightml`): a slide page's divisions
        # carry the live slide instead of an ascii fence, and that satisfies
        # the reader the same way (JL 260805, QA4). The caption rule below
        # still applies to it.
        media = any(re.match(r"^!\[[^\]]*\]\([^)]+\)\s*$", l.strip())
                    for l in lines)
        if not (fenced or media):
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


# ---- QB6 §5.1 rule 1: type resolution runs BEFORE any per-type rule ----
# The base contract (`haipipe-page/SKILL.md`) resolves ① to ⑤ and stops
# at the first key that matches. Step ③ is REQUIRED on its declared types and BEATS
# the filename, which is what settles the two real collisions, `S-Display-4c`
# (a stage filename, a display page) and `QA4` (a Q filename, a slide deck).
#
# Only the ③ key can be wrong in a way a machine can see, so that is what this
# rule reads. The unit segment is `[A-Za-z0-9]+` because the live board's real
# units are `Pitch`, `Seed`, `C`, `C0`, `R1`, `1a` and `Dash`; a first version
# demanded a digit and reported 25 of 59 pages on the live MISQ paper as
# claimed by nothing, which was the pattern being wrong, not the board.
FENCE = "`" * 3
PAGE_TYPE_LINE = re.compile(r"(?m)^page-type:\s*(\S+)\s*$")
# `stage` joined 260815: the restructure reduced this family's kinds to stage
# and design, and QPs3's specimen declares `page-type: stage` explicitly.
PAGE_TYPE_VALUES = ("display", "slide", "design", "section", "labeling",
                    "narrative", "dash", "view", "stage")
STEP4_STAGE = re.compile(r"^S-[A-Za-z]+-[A-Za-z0-9]+(?:-.+)?$")


def check_page_type(path, text, name, rep):
    """Exactly one key claims a page, and step ③'s key is one the table knows."""
    head = text.split("\n## ", 1)[0]
    declared = PAGE_TYPE_LINE.findall(head)
    route = re.search(r"(?m)^route:\s*(outward|inward)\s*$", head)
    if len(declared) > 1:
        rep.add(WARN, "page-type-twice", name,
                f"{len(declared)} `page-type:` lines; exactly one step may "
                "claim a page")
    for value in declared:
        if value not in PAGE_TYPE_VALUES:
            rep.add(WARN, "page-type-unknown", f"{name} -> {value}",
                    f"step ③ defines {', '.join(PAGE_TYPE_VALUES)}; `{value}` "
                    "is in no step, so this page resolves by filename instead")
    if declared and route:
        # ② wins by order, so the ③ key is dead text and says otherwise.
        rep.add(WARN, "page-type-conflict", name,
                f"carries `route: {route.group(1)}` (step ②) AND "
                f"`page-type: {declared[0]}` (step ③); ② resolves first, so "
                "the page is not the type its own key names")


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
            # The contract says a group takes the NUMBER, NAME and EMOJI of its
            # Content part (haipipe-page §241), so the part may carry one too:
            # strip both sides or an emoji'd division reads as drift (JL 260816).
            gname = re.sub(r"^\W+\s*", "", gname)   # the group's own emoji
            if want is not None:
                want = re.sub(r"^\W+\s*", "", want)
            if want is None:
                rep.add(WARN, "group-no-division", f"{name} · {sec_name} C{gid}",
                        f"`C{gid}` names no Content division on this page")
            elif want.strip() != gname.strip():
                rep.add(WARN, "group-name-drift", f"{name} · {sec_name} C{gid}",
                        f"reads {gname.strip()!r}; its division `### {gid}` is "
                        f"{want.strip()!r} (QB4 §0.5: same id, same name)")


def check_draw_folders(d, rep):
    """Every draw/ holds exactly what its owner may own (QPf2's contract).

    A page's draw/ holds that page's own scene(s), named by the page id the
    folder name starts with; a group's draw/ holds group.excalidraw. Anything
    else is a STRAY — the trace an archive or merge leaves behind (found
    260816: QPf2a's stub sat in QPf2's draw/ for a day, and Design-7/8's
    scenes hid in Design-6's). Underscore entries (_retired, _archive) are a
    person's deliberate parking and stay unjudged; the generated board/ site
    is not source and is skipped.
    """
    for draw in sorted(d.rglob("draw")):
        if not draw.is_dir():
            continue
        parts = draw.relative_to(d).parts
        if "board" in parts or any(p.startswith("_") for p in parts):
            continue
        page = draw.parent
        is_page = (page / f"{page.name}.md").is_file()
        for f in sorted(draw.iterdir()):
            if f.name.startswith("_") or (f.name == "assets" and f.is_dir()):
                continue
            where = str(f.relative_to(d))
            if f.suffix != ".excalidraw":
                rep.add(WARN, "stray-in-draw", where,
                        "not a scene; draw/ holds scenes, assets/, and _parked")
                continue
            ok = (f.name == "group.excalidraw") if not is_page else \
                (page.name == f.stem or page.name.startswith(f.stem + "-"))
            if not ok:
                rep.add(WARN, "stray-scene", where,
                        f"scene stem does not name this {'page' if is_page else 'group'}"
                        " — a leftover from an archive or merge?")


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
                if outside_checkout(html.parent, href):
                    rep.add(WARN, "outside-checkout", f"{name} -> {href}",
                            f"rendered {attr} target lives outside this checkout")
                else:
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

        # An anchor or button INSIDE a navigation row. A row is one link, and a
        # browser closes the outer `<a>` when a second one opens, so the row
        # stops navigating. The renderer now strips these (`body.nav_inline`),
        # and this is the rule that says so out loud if they return by another
        # path: a path in backticks inside a `###` heading put one in the
        # sidebar, which is copied onto every page and never rerooted, and one
        # heading on QE5 shipped 66 dead-href ERRORs across the built tree.
        for cls, inner in re.findall(
                r'<a class="(sb-p|sb-ss|sb-g|ir)[^"]*"[^>]*>(.*?)</a>', bare, re.S):
            bad = re.search(r"<(a|button)\s", inner)
            if bad:
                rep.add(ERROR, "nested-anchor", f"{name} · .{cls}",
                        f"a <{bad.group(1)}> inside a nav row; the row stops "
                        "navigating and its href is never rerooted")
                break          # one per page: the sidebar repeats on all of them

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
    check_topic_entries(d, pages, rep)
    check_draw_folders(d, rep)
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
