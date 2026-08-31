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
from src.common import (ALIAS, NUMBERED_GROUP, STN, AIM_STATE_RE,  # noqa: E402
                        aim_ids, aim_progress, group_stem,
                        page_files)
from src.page_context import audit_related_rows  # noqa: E402
from src.topic_entry_contract import check_topic_entries  # noqa: E402
from src.page_evidence import check_page_evidence  # noqa: E402
from src.feedback import rounds as _rounds, parse_round, register_path, register_ids  # noqa: E402

ERROR, WARN, GAP = "ERROR", "WARN", "GAP"
MAX_PAGE_TITLE_WORDS = 6
# `Q<group><n>-<slug>` or `S-<Family>-<unit>-<slug>`, as the heading writes it.
PAGE_ID_RE = re.compile(r"Q[A-Za-z]*\d+[\w-]*|S-[\w-]+")
STATE_LABELS = {"✅": "SETTLED", "🟡": "PARTIAL", "🔴": "OPEN", "⏸": "ON HOLD"}
# The generated Board site can link to live server routes. They do not resolve
# as files beside an HTML page, so checker must recognize them rather than
# calling the Board Home navigation a dead static href.
LIVE_ROUTE_PREFIXES = ("/_board/", "/_excalidraw", "/boards")

# Sections a page cannot be complete without. Aliases are accepted because old
# boards still use them and ALIAS is the renderer's own table.
# `Now` (`## States`) RETIRED 260819 and merged into `Done when` (`## Aims`):
# one Aim is one row carrying its tick, its `Done when:` test and its `Now:`
# fact (`haipipe-page` 0.34.0). One id written in two places was one fact with
# two owners, and it produced `aim-stated-twice` and `state-without-aim` on the
# very page that ruled it. A page that still carries `## States` keeps parsing;
# `retired-section` reports it, and this list no longer DEMANDS it.
REQUIRED = ["Opening", "Done when"]

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


# A key's lowercase tail may be a WORD, not one letter: the paper board declares
# `### QCskill · Engine skills`, and a one-letter tail read that heading as `QCs`,
# which matched no folder. The group then vanished from the count and every folder
# after it was told it was numbered one too high.
GROUP_HEAD = re.compile(r"^###\s+Q([0-9][a-z]|[A-Z]+[a-z]*)\b", re.M)


def check_group_order(d, text, rep):
    """The group folders must read on disk in board.md's `## Pages` order.

    `## Pages` is the ONLY authority on order; the number a folder carries is
    derived from it (JL 260816). Letters carry identity and cannot carry order,
    which is how `QC-engine/` came to sort four rows above `QPs-page-structure/`
    on a board that read them the other way round.

    A board is numbered or it is not, and the middle is the only real defect: one
    numbered folder among bare ones means two orderings disagree and a reader
    cannot tell which is live. A wholly unnumbered board is the pre-260816 shape,
    reported as a WARN so it gets migrated rather than blocked.

    A folder is a GROUP folder only when its name, minus any number, starts with
    a `Q<key>` that board.md declares. That is what keeps a paper's
    `0-lifecycle/` out of this check: `0-seed/`, `1-work/` and `3-display/` are
    SUBJECT folders whose numbers carry lifecycle order, and they answer to a
    different rule entirely.
    """
    names = "|".join(re.escape(n) for n in alias_names("Pages"))
    m = re.search(rf"^##\s+({names})\s*$", text, re.M)
    if not m:
        return
    end = text.find("\n## ", m.end())
    keys = GROUP_HEAD.findall(text[m.end():end if end != -1 else len(text)])
    if not keys:
        return
    pos = {k: i + 1 for i, k in enumerate(keys)}
    # longest key first, so QAa wins over QA on `QAa-something/`
    by_len = sorted(keys, key=len, reverse=True)

    found = []                      # (folder, key, declared number or None)
    for p in sorted(d.iterdir()):
        if not p.is_dir() or p.name.startswith(("_", ".")) or p.name in ("board", "fig"):
            continue
        num = NUMBERED_GROUP.match(p.name)
        stem = group_stem(p.name)
        key = next((k for k in by_len
                    if stem == f"Q{k}" or stem.startswith(f"Q{k}-")), None)
        if key:
            found.append((p.name, key, int(num.group(1)) if num else None))
    if not found:
        return

    bare = [f for f, _, n in found if n is None]
    if len(bare) == len(found):
        rep.add(WARN, "groups-not-numbered", "board.md",
                f"{len(found)} group folders carry no reading-order number "
                f"(JL 260816); rename each to `<N>-<folder>` in ## Pages order "
                f"and rewrite the paths that cite them. regroup.py numbers a "
                f"board it is still FOLDING and cannot renumber this one")
        return
    for f in bare:
        rep.add(ERROR, "group-number-missing", f,
                "some group folders are numbered and this one is not, so the "
                "folder listing declares two different orders")
    for f, key, n in found:
        if n is None:
            continue
        want = pos[key]
        if n != want:
            rep.add(ERROR, "group-number-order", f,
                    f"numbered {n} but Q{key} is #{want} in ## Pages; "
                    f"board.md decides the order, the folder follows it")


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

    # `store:` is OPTIONAL and declares where work COMMISSIONED by this board
    # writes its generated output: results, notebooks and QA digests. A probe
    # dispatching from one of this board's pages passes it as RESULT_STORE, so
    # the executor is told a PATH and never learns which consumer it serves.
    # Absent means this board commissions nothing that produces files, and a
    # task it dispatches keeps output in its own folder (JL 260823).
    store = re.search(r"^store:\s*(\S.*?)\s*$", text, re.M)
    if store:
        target = store.group(1)
        if target.startswith("~") or ".." in target.split("/"):
            rep.add(ERROR, "board-store-path", f"board.md -> {target}",
                    "a `store:` must be repo-relative or absolute with no `..` and no "
                    "`~`; a dispatching probe resolves it once and hands the executor "
                    "an absolute path, so a climbing path resolves differently "
                    "depending on who dispatched")
    # `reads:` (JL 260824, the design family): the board's evidence whitelist.
    # Each entry is a sibling board's folder name; a direction card's grant and
    # a unit's evidence must sit inside it, so a name that resolves to nothing
    # makes the whole chain unverifiable.
    reads = re.search(r"^reads:\s*(\S.*?)\s*$", text, re.M)
    if reads:
        for entry in [e.strip() for e in reads.group(1).split("\u00b7")]:
            if not entry:
                continue
            if entry.startswith("~") or ".." in entry.split("/"):
                rep.add(ERROR, "board-reads-path", f"board.md -> {entry}",
                        "a `reads:` entry must be a plain sibling-board name or a "
                        "repo-relative path with no `..` and no `~`")
                continue
            # repo-relative means from the CHECKOUT ROOT, never the invoker's
            # cwd: the same board must check identically from anywhere.
            _rr = _repo_root(d)
            cand = [d.parent / entry] + ([_rr / entry] if _rr else [])
            if not any(c.is_dir() for c in cand):
                rep.add(ERROR, "board-reads-target", f"board.md -> {entry}",
                        "a `reads:` entry names no board on disk; the grant chain "
                        "(reads -> card grant -> unit evidence) starts here, so a "
                        "dead entry makes every citation under it unverifiable")

    pages = {p.name: p for p in page_files(d)}
    # `[MIAD]\d` admits the Application runtime ids (M00-meta.md, I01-<slug>.md,
    # A00-brief.md, D01-<slug>.md) that PAGENAME now discovers; without it every
    # runtime board reported all of its own pages as not-in-pages (260820).
    listed = re.findall(
        r"^((?:[QS]|[A-Z]{1,2}\d|Agent-|Meeting-|Design-)[^\s/]*\.md)\s*$", text, re.M)
    for name in listed:
        if name not in pages:
            rep.add(ERROR, "pages-ghost", f"board.md -> {name}",
                    "## Pages names a file that is not on disk")
    for name in sorted(pages):
        if name not in listed:
            rep.add(WARN, "not-in-pages", name,
                    "on disk but not in ## Pages, so it renders under the ⚠️ group")
    check_group_order(d, text, rep)
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

    title_match = re.search(r"^#\s+(\S.*?)\s*$", text, re.M)
    if not title_match:
        rep.add(ERROR, "missing-title", name, "no `# title` line")
    else:
        title = title_match.group(1)
        # The heading is written `{id} · {title}` (src/page_board.py), and the
        # page id is not part of the title, so drop a leading id-shaped token.
        head, sep, tail = title.partition("\u00b7")
        if sep and PAGE_ID_RE.fullmatch(head.strip()):
            title = tail.strip()
        # Visible words are semantic tokens, not punctuation-only separators.
        # A hyphenated compound, slash-joined identifier, or acronym is one word.
        words = re.findall(r"[A-Za-z0-9]+(?:[-/][A-Za-z0-9]+)*", title)
        if len(words) > MAX_PAGE_TITLE_WORDS:
            line = text[:title_match.start()].count("\n") + 1
            rep.add(WARN, "title-too-long", f"{name}:{line}",
                    f"title has {len(words)} visible words; target 3-5 and keep the whole "
                    f"title at or below {MAX_PAGE_TITLE_WORDS} (JL 260827)")
    for canon in REQUIRED:
        # `Done when` is satisfied by the page's PLAN once the page migrated to
        # haipipe-plugin-outline 0.16.0 and kept no copy.
        if canon == "Done when" and page_aims_text(text, path)[1]:
            continue
        if not has_section(text, canon):
            shown = " / ".join(alias_names(canon))
            rep.add(ERROR, "missing-section", name, f"no `## {shown}` section")
    # `Skill-<unit>-<slug>` is the SKILL page kind (JL 260731), not a stage: it
    # mirrors a shipped unit and has no gate, so the stage sections are not owed.
    # Stage ids are exactly what parse.py can classify as a stage: `S-<Word>-`
    # or the legacy shorthand S<d>. A bare startswith("S") also claimed
    # application families like SD00-seed and SA01-<slug> (260821), which are
    # not stages; SM/SA shorthands left parse.py the same day.
    if re.match(r"S(?:-|\d)", name):
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

    aims_text, in_plan = page_aims_text(text, path)
    states_text = section_text(text, "Now")
    check_state_mirrors_aims(aims_text, states_text, name, rep)
    check_generated_block(text, name, rep, path)
    check_evidence_file(path, name, rep)
    check_discussion_file(path, name, rep)
    check_requirement_file(text, path, name, rep)
    check_retired_blocks(text, name, rep)

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
    check_feedback_coverage(path, text, name, rep)
    check_plan_arc(path, name, rep)
    check_page_type(path, text, name, rep)
    check_group_names(text, name, rep)
    check_one_canvas(text, name, rep)
    check_division_figures(text, name, rep)
    check_comment_form(text, name, rep)
    check_file_paths(text, name, rep, path.parent, path=path)
    check_related_board_pages(path, name, text, rep)
    check_canvas_frames(text, name, rep, path.parent)
    check_duplicate_sections(text, name, rep)
    check_retired_sections(text, name, rep)
    check_evidence_pointer(text, name, rep)
    check_page_evidence(path, text, name, rep, ERROR, WARN)
    check_fence_balance(text, name, rep)
    check_content_attribution(text, name, rep)
    check_section_sentences(text, path, name, rep)


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
    "Where we are": "renamed to `## States` (260731), then merged into `## Aims` (260819)",
    # The 260819 merge named only the OLD name above, so `RETIRED_SECTIONS.get`
    # returned None for the CURRENT one and the comment at the head of this file
    # ("`retired-section` reports it") described behaviour the table did not
    # have. 1,026 lines of a retired section passed silently on the MISQ paper
    # board for eleven days (JL 260830).
    "Files": "moved to `outline/<stem>-files.md` (JL 260831, QPf12 row 3): one "
             "`### F<n> · <what it is for>` record per file with `Path` and `Role`; a "
             "Related Board Page is a record with `Role: related` and its row verbatim under it",
    "States": "merged into `## Aims` (260819): one Aim row carries its tick, "
              "its `Done when:` test and its `Now:` fact. Live asks "
              "(`### Needs JL · tick these`) become that Aim's `Now:` line",
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


def check_content_attribution(text, name, rep):
    """The OFFICIAL-DOCUMENT rule: Content states rules, never attributions.

    Ruled 260820, reading the compiled PDF: "don't say too much 'JL' or
    'YYMMDD', this is the official document." A bare six-digit date code or a
    person's name as authority inside `## Content` (or the Diagram caption) is
    a Log row wearing prose: the reader of the document cannot parse it and
    should not have to. Who and when live in `## Log`, `## Discussion`, and
    tick lines. Fenced blocks are skipped, because a fence may carry a frozen
    transcription another pen owns; the CHECK judge reads those by eye.
    New authority names join the name pattern here when the board gains them.
    """
    body = re.search(r"(?ms)^## (?:Content|Diagram)\b.*?(?=^## (?!Content|Diagram)|\Z)",
                     text)
    spans = re.findall(r"(?ms)^## (?:Content|Diagram)\b[^\n]*\n(.*?)(?=^## |\Z)",
                       text)
    if not spans:
        return
    date_re = re.compile(r"\b26[01]\d{3}\b")
    name_re = re.compile(r"\bJL\b")
    offset = 0
    for span in spans:
        start = text.index(span, offset)
        offset = start + len(span)
        base = text[:start].count("\n") + 1
        fenced = False
        for i, line in enumerate(span.split("\n")):
            st = line.lstrip()
            if st.startswith(FENCE):
                fenced = not fenced
                continue
            if fenced or st.startswith(">") or st.startswith("<!--"):
                continue
            hits = []
            if date_re.search(line):
                hits.append("a bare date code")
            if name_re.search(line):
                hits.append("a person named as authority")
            if hits:
                rep.add(WARN, "content-attribution", "%s:%d" % (name, base + i),
                        "Content is the official document and this line carries "
                        + " and ".join(hits) + "; state the rule itself and move "
                        "the who/when to a Log row (haipipe-page-draft, the "
                        "present-tense rule).")


_NUM_RE = re.compile(r"\d{1,3}(?:,\d{3})+|\b\d+\.\d+\b|\b\d+(?:\.\d+)?\s*(?:million|thousand|billion|percent|%)")


def _latest_plan_approved(path):
    """-> True when the page's newest outline-v<N>.md carries `approved: ✅`."""
    o = path.parent / "outline"
    if not o.is_dir():
        return False
    plans = sorted(o.glob(f"{path.stem}-outline-v*.md"),
                   key=lambda q: int(re.search(r"-v(\d+)\.md$", q.name).group(1))
                   if re.search(r"-v(\d+)\.md$", q.name) else 0)
    if not plans:
        return False
    return bool(re.search(r"(?m)^approved:\s*✅", plans[-1].read_text(encoding="utf-8", errors="replace")))


def check_section_sentences(text, path, name, rep):
    """The DRAFT contract on a Section page drafted from an APPROVED plan
    (haipipe-page-draft §① §②): every Content sentence ends `<!-- realizes:
    C.P.B -->` (`sentence-without-realizes`), and every sentence that carries a
    number (a comma-grouped count, a decimal, `8.69 million`, a percentage) has
    a `> Value:` lane under it (`number-without-lane`). Gated on the approved
    plan because a page with no agreed slot plan has nothing to realize; the
    pages written before the rule stay silent until their next DRAFT."""
    if path is None or not re.search(r"(?m)^page-type:\s*section\b", text[:800]):
        return
    if not _latest_plan_approved(path):
        return
    spans = re.findall(r"(?ms)^## Content\b[^\n]*\n(.*?)(?=^## |\Z)", text)
    if not spans:
        return
    span = spans[0]
    start = text.index(span)
    base = text[:start].count("\n") + 1
    lines = span.split("\n")
    fenced = False
    for i, line in enumerate(lines):
        st = line.strip()
        if st.startswith(FENCE):
            fenced = not fenced
            continue
        if fenced or not st or st.startswith((">", "#", "<!--", "(", "**", "-", "|", "!", "["  )):
            continue
        core = re.sub(r"<!--.*?-->", "", st).strip()
        if not re.search(r"[.?!][\"')\]]*(\s*\[[^\]]*\])?\s*$", core):
            continue                      # a title line, a keyword list: not a sentence
        if "realizes:" not in st:
            rep.add(WARN, "sentence-without-realizes", "%s:%d" % (name, base + i),
                    "a Section sentence drafted from an approved plan names its slot: "
                    "end it with `<!-- realizes: C<n>.P<m>.B<k> -->` (haipipe-page-draft §①)")
        probe = re.sub(r"\[[^\]]*\]|\\cite[pt]?\{[^}]*\}", "", core)
        if _NUM_RE.search(probe):
            j, has_lane = i + 1, False
            while j < len(lines) and lines[j].strip().startswith(">"):
                if re.match(r"^>\s*Value:", lines[j].strip()):
                    has_lane = True
                    break
                j += 1
            if not has_lane:
                rep.add(WARN, "number-without-lane", "%s:%d" % (name, base + i),
                        "this sentence states a number and no `> Value:` lane follows it; "
                        "write the source page, bracket or card and its state (haipipe-page-draft §②)")


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


def _files_record_text(path):
    """The page's outline/<stem>-files.md, with each `- **Path**: `x`` row
    rewritten as a bare `- `x`` row so the Files path checks read it unchanged."""
    if not path:
        return ""
    p = Path(path); f = p.parent / "outline" / f"{p.stem}-files.md"
    if not f.is_file():
        return ""
    t = f.read_text(encoding="utf-8", errors="replace")
    return re.sub(r"(?m)^(\s*[-*])\s+\*\*Path\*\*:\s*", r"\1 ", t)

def check_file_paths(text, name, rep, board_dir=None, path=None):
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
    # Since 260831 the file map lives in outline/<stem>-files.md (JL, QPf12 row 3);
    # its `- **Path**: `x`` rows are checked with the same teeth as a page's rows.
    block = block + "\n" + _files_record_text(path)
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
    for an agent to discover it during DRAFT, EVIDENCE, REVISE, or CHECK.
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


def check_generated_block(text, name, rep, path=None):
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
    # The Log may live on the page OR, since haipipe-plugin-outline 0.16.0, in
    # `outline/<stem>-log.md`. Reading only the page made this check lose its
    # input the moment a page migrated: `latest` went "" for ever and a stale
    # form block could never be reported again. A finding count dropping because
    # a check lost its input is worse than the finding (field test, JL 260830).
    log = section_text(text, "Log")
    if path is not None:
        side = path.parent / "outline" / f"{path.stem}-log.md"
        if side.exists():
            log += "\n" + side.read_text(encoding="utf-8", errors="replace")
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



def check_evidence_file(path, name, rep):
    """`outline/<stem>-evidence.md` is DERIVED (haipipe-plugin-outline 0.17.2):
    one bullet, one line, in the Evidence Bundle's six status words, written
    only by `cli/evidence-status.py`. Two things can go wrong with a derived
    file and both are silent: it is older than the evidence it describes, or
    someone typed into it. A stale status that reads as measured is worse than
    no file (JL 260831)."""
    if path is None:
        return
    ev = path.parent / "outline" / f"{path.stem}-evidence.md"
    if not ev.exists():
        return
    text = ev.read_text(encoding="utf-8", errors="replace")
    stamp = re.search(r"MEASURED\s+(2\d{5})(?:\s+(\d{4}))?", text)
    if not stamp or "GENERATED; do not hand-edit" not in text:
        rep.add(WARN, "evidence-hand-edited", name,
                "`outline/%s` carries no `MEASURED <date>` + GENERATED line; a status "
                "nobody generated is a status somebody typed" % ev.name)
        return
    import datetime as _dt
    measured = _dt.datetime.strptime(stamp.group(1) + (stamp.group(2) or "0000"), "%y%m%d%H%M").timestamp()
    newest, newest_name = 0.0, ""
    lanes = [path.parent / "outline", path.parent / "probe", path.parent / "bibex",
             path.parent / "display", path.parent / "pagex"]
    for lane in lanes:
        if not lane.is_dir():
            continue
        for f in lane.rglob("*"):
            if f.is_file() and f != ev and f.stat().st_mtime > newest:
                newest, newest_name = f.stat().st_mtime, f.relative_to(path.parent).as_posix()
    if newest > measured + 60:
        rep.add(WARN, "evidence-stale", name,
                "`outline/%s` was measured %s %s but `%s` changed later; regenerate "
                "with `cli/evidence-status.py`" % (ev.name, stamp.group(1), stamp.group(2) or "", newest_name))


def check_discussion_file(path, name, rep):
    """`outline/<stem>-discussion.md` holds OPEN questions only (haipipe-plugin-
    outline 0.18.0, JL 260831: "the solved one go to logs, and only leave the
    one we have not solved"). A thread that is settled, decided or dropped has
    moved: its ruling is one `### YYMMDD · D<nn> …` record in `-log.md`. A
    settled thread still sitting here is the old shape, and the file it makes
    is the one nobody could read."""
    if path is None:
        return
    f = path.parent / "outline" / f"{path.stem}-discussion.md"
    if not f.exists():
        return
    text = f.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r"(?ms)^### (D\d+) · [^\n]*\n(.*?)(?=^### |\Z)", text):
        body = m.group(2)
        if re.search(r"(?m)^\s*(?:status:|- \*\*Status\*\*:)\s*(✅|🚫)", body) \
                or re.search(r"(?m)^\s*(?:settled:|- \*\*Settled\*\*:)", body) \
                or re.search(r"(?m)^\s*status:\s*✅", body):
            rep.add(WARN, "discussion-settled-thread", name,
                    f"thread `{m.group(1)}` is settled and still in `outline/{f.name}`; the discussion "
                    f"holds open questions only, so its ruling belongs in `outline/{path.stem}-log.md` "
                    f"as one dated record (haipipe-plugin-outline 0.18.0)")


def check_requirement_file(text, path, name, rep):
    """`outline/<stem>-requirement.md` is DERIVED by `cli/requirement.py` from
    the VENUE division the page binds, and nothing else (JL 260831: "focus on
    the venue is sufficient"; the first generator also copied the Narrative
    row and the board rules in, and the tab was unreadable). A Section page
    that binds a division and has no file shows no 📏 chip (JL 260831: "I
    didn't see the requirement"); a file without its GENERATED line was typed."""
    if path is None or not re.search(r"(?m)^page-type:\s*section\b", text[:800]):
        return
    if not re.search(r"(?m)^structure-source:\s*\S", text[:3000]):
        return
    f = path.parent / "outline" / f"{path.stem}-requirement.md"
    if not f.exists():
        rep.add(WARN, "requirement-missing", name,
                f"this page binds a venue division and `outline/{f.name}` "
                f"does not exist; run `cli/requirement.py {path.name}`")
        return
    if "GENERATED; do not hand-edit" not in f.read_text(encoding="utf-8", errors="replace"):
        rep.add(WARN, "requirement-hand-edited", name,
                f"`outline/{f.name}` carries no GENERATED line; a requirement nobody generated is one somebody typed")
        return
    # STALE: the venue desk (its one source) is newer than the stamp; a
    # requirement that outlives a moved desk reads as binding.
    ftxt = f.read_text(encoding="utf-8", errors="replace")
    stamp = re.search(r"MEASURED\s+(2\d{5})(?:\s+(\d{4}))?", ftxt)
    if not stamp:
        return
    import datetime as _dt
    measured = _dt.datetime.strptime(stamp.group(1) + (stamp.group(2) or "0000"), "%y%m%d%H%M").timestamp()
    skills = Path(__file__).resolve().parents[3]
    srcs = []
    m = re.search(r"(?m)^structure-source:\s*(\S+)", text[:3000])
    if m:
        srcs += [q for q in (skills / m.group(1), path.parents[2] / m.group(1)) if q.exists()]
    for s in srcs:
        if s.exists() and s.stat().st_mtime > measured + 60:
            rep.add(WARN, "requirement-stale", name,
                    f"`outline/{f.name}` was measured {stamp.group(1)} {stamp.group(2) or ''} but `{s.name}` changed "
                    f"later; regenerate with `cli/requirement.py {path.name}`")
            return


def check_retired_blocks(text, name, rep):
    """`### Stage Record` is a leftover of the retired Submission-0 stage
    lifecycle ("Rollup: S Submission 0 Reconcile Unit: 1 of 9"). It renders
    as a fold that says nothing true about the page (JL 260831: "why we have
    this? we should not have this"). Delete it; nothing replaces it."""
    for m in re.finditer(r"(?m)^###\s+Stage Record\b", text):
        rep.add(WARN, "retired-block", name,
                "`### Stage Record` is a leftover of the retired stage lifecycle; delete the block")


def page_aims_text(text, path):
    """The page's Aims, wherever they live.

    Since `haipipe-plugin-outline` 0.16.0 the Aims live in the page's PLAN and
    `page.md` keeps no copy, so sourcing them from the page alone made the law
    and this checker contradict each other: obeying the law produced
    `missing-section` + `no-aims` on every migrated page (field test, JL
    260830). Page first, so an unmigrated board is untouched; plan second.
    """
    on_page = section_text(text, "Done when")
    if on_page.strip() or path is None:
        return on_page, False
    d = path.parent / "outline"
    plans = sorted(d.glob("*-outline-v*.md")) if d.is_dir() else []
    if not plans:
        return on_page, False
    plan = plans[-1].read_text(encoding="utf-8", errors="replace")
    m = re.search(r"(?m)^## Aims\b.*?$(.*)\Z", plan, re.S)
    return (m.group(1) if m else ""), bool(m)


_ROUND_CACHE = {}


def check_plan_arc(path, name, rep):
    """haipipe-page-outline §🚦 ⓪.1: `arc:` present is mechanical. It was
    parsed by nothing until NA01's field desk grepped for it (260831)."""
    if path is None:
        return
    for plan in sorted((path.parent / "outline").glob("*-outline-v*.md")):
        head = plan.read_text(encoding="utf-8", errors="replace")[:1500]
        if not re.search(r"(?m)^arc:\s*\S", head):
            rep.add(WARN, "plan-no-arc", f"{name} · {plan.name}",
                    "the plan carries no `arc:` line; a division list with no "
                    "stated argument is a table of contents (§🚦 ⓪.1)")


def check_feedback_coverage(path, text, name, rep):
    """Both directions of the Round⇄page join (haipipe-page-outline ⓪ COLLECT).

    Forward: every §2B row a Round routes to this page appears in the page's
    outline/feedback/<RD>.md. Reverse: every register row names a real Round
    row. A page that never ran OUTLINE never collected, so G7 must not close on
    a Round whose targets carry no register (field test, JL 260831)."""
    if path is None or re.search(r"(?m)^page-type:\s*round\b", text[:600]):
        return
    board = path.parents[2]
    if board not in _ROUND_CACHE:
        _ROUND_CACHE[board] = [(rd, parse_round(rd)) for rd in _rounds(board)]
    pid = path.stem.split("-")[0]
    for rd, data in _ROUND_CACHE[board]:
        routed = {r["id"] for r in data["rows"].get(pid, [])}
        if not routed:
            continue
        reg = register_path(path)
        if not reg.exists():
            rep.add(WARN, "feedback-uncollected", name,
                    f"{rd.stem.split('-')[0]} routes {len(routed)} row(s) here and "
                    f"`outline/{reg.name}` does not exist; run "
                    f"`cli/feedback.py collect` (OUTLINE ⓪)")
            continue
        have = register_ids(reg)
        # the OTHER direction the law promises (haipipe-page-outline ⓪): an
        # OPEN register row is served by a plan bullet carrying `Routed:` or
        # declined in the plan's header (`declined: <RD> <id> · <reason>`).
        # NA01's field desk (260831) found this tooth missing while the plugin
        # text claimed "both directions".
        plans = sorted((path.parent / "outline").glob("*-outline-v*.md"))
        plan = plans[-1].read_text(encoding="utf-8", errors="replace") if plans else ""
        rdid = rd.stem.split("-")[0]
        served = set(re.findall(rf"(?m)^\s+Routed:\s*{rdid}\s+(\S+)", plan))
        declined = set(re.findall(rf"(?m)^declined:\s*{rdid}\s+(\S+)", plan))
        open_rows = {r["id"] for r in data["rows"].get(pid, []) if r["state"] == "open"}
        for rid in sorted((open_rows & have) - served - declined):
            rep.add(WARN, "feedback-unserved", f"{name} · {reg.name}",
                    f"open row `{rid}` is served by no plan bullet (`Routed: {rdid} {rid}`) "
                    f"and not declined (`declined: {rdid} {rid} · <reason>`)")
        for rid in sorted(routed - have):
            rep.add(WARN, "feedback-coverage", f"{name} · {reg.name}",
                    f"Round row `{rid}` is routed here and missing from the register")
        for rid in sorted(have - routed):
            rep.add(WARN, "feedback-coverage", f"{name} · {reg.name}",
                    f"register row `{rid}` names no row the Round routes here")


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
    # Since the 260819 merge the tick sits on the Aim row itself; a page that
    # still carries `## States` is read the old way, so an unmigrated board
    # keeps its findings and a migrated one stops reading as "all ⬜".
    src = states_text if (states_text or "").strip() else aims_text
    rows = [aim_id for _emoji, aim_id in AIM_STATE_RE.findall(src or "")]
    seen = collections.Counter(rows)

    missing = [a for a in declared if not seen[a]]
    if missing:
        shown = " · ".join(missing[:6]) + (" …" if len(missing) > 6 else "")
        rep.add(WARN, "aim-without-state", name,
                f"{len(missing)} of {len(declared)} Aim(s) carry no tick, on the row or in States, "
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
# 260820, Application two-board split: `meta` joined as the InsightBoard head;
# `intervention` was renamed to the already-listed `design`, and `artifact` was
# absorbed into a per-division `accepted:` row. Both are dropped, so a page still
# carrying either key now reports page-type-unknown and gets migrated.
# 260824, paper journey 0.5.0: `roadmap` and `collection` joined as the two
# working pages of the establish loop (the Seed states the gaps, the Roadmap
# plans the errands, the Collection registers the receipts).
PAGE_TYPE_VALUES = ("display", "slide", "design", "opening", "venue", "seed",
                    "section", "round", "labeling", "narrative", "dash", "task", "insight",
                    "meta", "question", "data", "information", "knowledge",
                    "wisdom", "brief", "principle", "view", "stage", "ideation",
                    "roadmap", "collection")
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

    # ORDINAL, not the printed number (JL 260831, QPf12 row 2: Aims "should map
    # to the content"): `A<n>` is the n-th direct `###` division of Content,
    # whatever its label, because a section page numbers `### §3.1 · …` and a
    # paper page writes `### Title`, and the 🧭 tab's `C<n>` addresses count the
    # same way. On a `### 1 · …` page ordinal and printed number coincide, so
    # nothing an older board reports changes there.
    content = section_text(text, "Content") or ""
    divs, fence = {}, False
    for ln in content.split("\n"):
        if ln.lstrip().startswith("```"):
            fence = not fence
        if fence or not re.match(r"^### \S", ln):
            continue
        title = re.sub(r"^### (?:§?[\d.]+(?: · | ))?", "", ln).strip()
        divs[str(len(divs) + 1)] = title
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
                rep.add(WARN, "group-no-division", f"{name} · {sec_name} A{gid}",
                        f"there is no Content division #{gid} on this page (ordinal: the {gid}th `###` heading under Content)")
            elif want.strip() != gname.strip():
                rep.add(WARN, "group-name-drift", f"{name} · {sec_name} A{gid}",
                        f"reads {gname.strip()!r}; Content division #{gid} is "
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


CARD_FIELDS = ["state", "stance", "depth", "thesis", "expected effect",
               "grant", "released"]   # `landed:` retired 260828: the card and
                                      # its unit share a folder, so the folder
                                      # IS the binding and a pointer would only
                                      # be one more thing that can dangle
CARD_STATES = {"proposed", "released", "landed", "killed"}
UNIT_STATES = {"draft", "judged"}          # accepted@v<N> is matched separately
DEPTHS = {"copy", "copy+why", "copy+why+expectation"}


def _repo_root(d):
    """The OUTERMOST checkout root, for evidence written repo-relative.

    Not the nearest: boards live inside submodules, and a submodule carries a
    `.git` FILE that satisfies `.exists()` just as a directory does. Stopping
    at the first hit returns the submodule, whose tree has no `_WorkSpace`, so
    every result-bank citation then reads as outside the grant.
    """
    found = None
    for p in [d] + list(d.parents):
        if (p / ".git").exists():
            found = p
    return found


def _resolve_cited(raw, base, root):
    """A cited path resolves either against its own file or against the repo."""
    raw = raw.strip().strip("`").rstrip(".,;:")
    if not raw or raw.startswith(("http", "#", "~")):
        return None
    for cand in [base / raw] + ([root / raw] if root else []):
        try:
            if cand.exists():
                return cand.resolve()
        except OSError:
            pass
    return None


def _cited_paths(text):
    """Every path-looking token in a page, backticked or bare.

    The bare pattern must not be allowed to start INSIDE a path: `../../x.md`
    also matches from its second character, which yields `./../x.md`, a string
    that resolves to nothing and reads as a dead link. That false positive
    fired on twenty-three real units the first time this ran.
    """
    out = []
    for m in re.finditer(r'`([^`\s]+\.(?:md|csv|txt|parquet|json))[^`]*`', text):
        out.append(m.group(1))
    for m in re.finditer(r'(?<![`\w./])((?:\.\.?/|designs/|_WorkSpace/|examples/)'
                         r'[^\s`)\]]+\.(?:md|csv|txt|parquet|json))', text):
        out.append(m.group(1))
    return list(dict.fromkeys(out))


def _card_field(text, key):
    m = re.search(r'^' + re.escape(key) + r':[ \t]*(.*)$', text, re.M)
    return m.group(1).strip() if m else None


def check_design_family(d, rep):
    """The design family's laws, given teeth (JL 260824).

    Until this ran, the family had eight written laws and two checks, both of
    them about `reads:`. A session on 260824 produced four real defects and a
    human or an agent caught every one: a dispatch packet that over-quoted its
    grant, a duplicate message counted twice, a grant path one directory short,
    and a unit citing its own card through a dead link. The last of those broke
    the plugin's first law, that the wager lives on the card and the unit cites
    it, and nothing mechanical noticed. These checks are that gap closed.

    A board may declare `mode: record` on board.md. A record board holds a
    pre-contract artifact, so its cards carry a historical `released:` and may
    have no stance and no grant; the vocabulary was written after the thing it
    describes, and forcing the words would forge a provenance. Everything
    structural is still checked on a record board: files, depth, resolvable
    references, and the evidence-within-grant chain when a grant exists.
    """
    bmd = d / "board.md"
    if not bmd.is_file():
        return
    btext = bmd.read_text(encoding="utf-8")
    record = (_card_field(btext, "mode") or "").strip() == "record"
    root = _repo_root(d)
    reads = _card_field(btext, "reads") or ""
    read_dirs = set()
    for entry in [e.strip() for e in reads.split("·") if e.strip()]:
        # A board named in `reads:` is two places on disk: its page tree, and
        # the result bank its tasks write to. A grant that cites the bank is
        # citing that board's own evidence, so both count as inside the read.
        # A repo-relative entry resolves from the checkout root, never the
        # invoker's cwd: the same board must check identically from anywhere.
        cands = [d.parent / entry]
        if root:
            cands += [root / entry,
                      root / "_WorkSpace" / "InsightBoardResult" / entry]
        for cand in cands:
            if cand.is_dir():
                read_dirs.add(cand.resolve())

    for units_dir in sorted(d.rglob("design")):
        if not units_dir.is_dir():
            continue
        parts = units_dir.relative_to(d).parts
        if "board" in parts or any(p.startswith("_") for p in parts):
            continue
        page = units_dir.parent
        if not page.name.startswith("DS"):
            continue

        for unit in sorted(p for p in units_dir.iterdir() if p.is_dir()):
            if unit.name.startswith("_"):
                continue
            uname = f"{page.name} · {unit.name}"

            # ── the card, first file of the thread (260828: one thread, one
            # folder — the card is card.md inside the unit it commissions) ──
            card = unit / "card.md"
            if not card.is_file():
                rep.add(ERROR, "unit-no-card", uname,
                        "a thread folder without card.md names no bet; the card "
                        "is the folder's birth certificate and its first file")
                continue
            ctext = card.read_text(encoding="utf-8")
            vals = {k: _card_field(ctext, k) for k in CARD_FIELDS}

            for k in CARD_FIELDS:
                if vals[k] is None:
                    rep.add(ERROR, "card-field-missing", uname,
                            f"a design card declares `{k}:`; without it the bet is "
                            "not written down, which is the one thing the card is for")
                elif not vals[k]:
                    rep.add(ERROR, "card-field-empty", uname,
                            f"`{k}:` is present but empty")

            state = (vals["state"] or "").split()[0] if vals["state"] else ""
            if state and state not in CARD_STATES:
                rep.add(ERROR, "card-state-word", uname,
                        f"`state: {state}` is not on the ladder "
                        f"{' · '.join(sorted(CARD_STATES))}")

            # Law: release before realize, now checkable as folder purity.
            siblings = [f.name for f in unit.iterdir()
                        if f.name not in {"card.md"} and not f.name.startswith(".")]
            if state == "proposed" and siblings:
                rep.add(ERROR, "unit-realized-before-release",
                        f"{uname} -> {' · '.join(sorted(siblings)[:4])}",
                        "the card still says proposed but the folder already holds "
                        "more than card.md; realizing an unreleased card passes a "
                        "person's gate mechanically")
            if state == "killed" and siblings:
                rep.add(WARN, "unit-tombstone-extra", uname,
                        "a killed thread is a tombstone: card.md and nothing else")

            # Law: no expected effect, no release.
            eff = (vals["expected effect"] or "").strip()
            if state in {"released", "landed"} and len(eff) < 12:
                rep.add(ERROR, "card-released-no-wager", uname,
                        "a card at `released` or `landed` must say what it is for and "
                        "what would falsify it; releasing a card with no wager is "
                        "designing for design's sake, which this plugin exists to stop")

            # Law: release is a person's act, recorded.
            rel = (vals["released"] or "").strip()
            if state in {"released", "landed"} and rel in {"", "⬜", "-", "—"}:
                rep.add(ERROR, "card-released-unsigned", uname,
                        "`state:` says released but `released:` carries no signature; "
                        "a release with nobody's name on it passed no gate")
            if state == "proposed" and rel not in {"", "⬜", "-", "—"}:
                rep.add(ERROR, "card-proposed-signed", uname,
                        "`released:` is signed while `state:` still says proposed")

            # Law: the grant narrows, never widens.
            grant_paths = set()
            graw = (vals["grant"] or "").strip()
            if graw and not graw.lower().startswith("none"):
                for raw in _cited_paths(graw) or [t for t in graw.split() if "/" in t]:
                    hit = _resolve_cited(raw, unit, root)
                    if hit is None:
                        rep.add(ERROR, "card-grant-path", f"{uname} -> {raw}",
                                "a grant entry resolves to nothing, so every citation "
                                "under it is unverifiable")
                        continue
                    grant_paths.add(hit)
                    if read_dirs and not any(
                            r == hit or r in hit.parents for r in read_dirs)                             and d.resolve() not in hit.parents:
                        rep.add(ERROR, "card-grant-outside-reads", f"{uname} -> {raw}",
                                "a grant entry sits outside every board named in "
                                "`reads:`; the chain must narrow at each level")
            elif not record and state in {"released", "landed"}                     and not (vals["stance"] or "").startswith("ignore"):
                rep.add(WARN, "card-grant-none", uname,
                        "a card with no grant may cite nothing; only an `ignore` "
                        "card is normally born that way")

            # ── the realization, when the state says there is one ────────────
            if state in {"proposed", "killed"}:
                continue
            readme = unit / "README.md"
            if state == "landed" and not readme.is_file():
                rep.add(ERROR, "card-landed-bare", uname,
                        "`state: landed` but the folder holds no README.md; a "
                        "landing with no unit behind it is the ghost pointer's "
                        "old failure wearing the new layout")
            if not readme.is_file():
                continue
            rtext = readme.read_text(encoding="utf-8")
            depth = (_card_field(rtext, "depth") or "").strip()
            ustate = (_card_field(rtext, "state") or "").strip()

            for req in ["spec.md", "evidence.md"]:
                if not (unit / req).is_file():
                    rep.add(ERROR, "unit-file-missing", f"{uname} -> {req}",
                            "the unit contract names card, README, spec, evidence "
                            "and content/")
            if not (unit / "content").is_dir() or not any((unit / "content").iterdir()):
                rep.add(ERROR, "unit-no-content", uname,
                        "content/ is the artifact itself; an empty one is not a design")
            if depth and depth not in DEPTHS:
                rep.add(ERROR, "unit-depth-word", uname,
                        f"`depth: {depth}` is not one of {' · '.join(sorted(DEPTHS))}")
            if depth.startswith("copy+why") and not (unit / "why.md").is_file():
                rep.add(ERROR, "unit-depth-no-why", uname,
                        f"`depth: {depth}` promises a why.md and there is none")
            if depth == "copy" and (unit / "why.md").is_file():
                rep.add(WARN, "unit-depth-extra-why", uname,
                        "`depth: copy` carries a why.md it did not declare")
            if ustate and not record and ustate not in UNIT_STATES                     and not re.match(r"accepted@v\d+$", ustate):
                rep.add(ERROR, "unit-state-word", uname,
                        f"`state: {ustate}` is not draft, judged or accepted@v<N>")

            # Every relative reference inside the unit must resolve. The
            # cross-folder pointer that dangled on 260824 is structurally gone,
            # but a dead reference anywhere still breaks the chain of custody.
            for f in sorted(unit.rglob("*.md")):
                ftext = f.read_text(encoding="utf-8")
                for raw in _cited_paths(ftext):
                    if not raw.startswith("."):
                        continue
                    if _resolve_cited(raw, f.parent, root) is None:
                        rep.add(ERROR, "unit-dead-reference",
                                f"{uname} · {f.name} -> {raw}",
                                "a relative reference inside a unit resolves to "
                                "nothing, and every citation under it is "
                                "unverifiable")

            # Law: evidence within grant. Only citations that leave this board
            # are evidence; a pointer inside the unit's own folder is structure.
            ev = unit / "evidence.md"
            if ev.is_file():
                if graw and not graw.lower().startswith("none"):
                    for raw in _cited_paths(ev.read_text(encoding="utf-8")):
                        hit = _resolve_cited(raw, ev.parent, root)
                        if hit is None or d.resolve() in hit.parents:
                            continue
                        if hit not in grant_paths:
                            rep.add(ERROR, "unit-evidence-outside-grant",
                                    f"{uname} -> {raw}",
                                    "this unit cites evidence its card never granted; "
                                    "the chain reads -> grant -> evidence narrows at "
                                    "every step and this widens it")


def check_insight_family(d, rep):
    """The insight family's first teeth (JL 260828, fieldtest rounds 1-2).

    Two live runs on A00 produced eighteen frictions caught by a human or a
    cold agent and none by machinery. The three mechanical ones land here:
    a Design Handoff whose signature gate has no row to test (round 1 #2),
    a refusal token spelled three ways on one board (round 2 F7/F12), and a
    settled-partial cell whose licensing sentence the cited page does not
    know it carries (round 2 F14). Each is proven to FAIL in
    tests/test_insight_family.py before being trusted.
    """
    for md in sorted(d.rglob("*.md")):
        parts = md.relative_to(d).parts
        if "board" in parts or any(pt.startswith("_") for pt in parts):
            continue
        try:
            text = md.read_text(encoding="utf-8")
        except OSError:
            continue
        m = re.search(r"^page-type:\s*(\w+)", text, re.M)
        ptype = m.group(1) if m else ""
        name = md.name

        if ptype == "wisdom":
            # A deferring W page exports no handoff and owes no signature; the
            # SERVES row is the handoff's marker (for-wisdom 0.3.0).
            if re.search(r"^SERVES\b", text, re.M):
                if not re.search(r"^signed:", text, re.M):
                    rep.add(ERROR, "wisdom-handoff-no-signed-row", name,
                            "a Design Handoff carries a `signed:` row (for-wisdom "
                            "0.3.0); without one the signature gate GI5 has nothing "
                            "to test, which is how two settled cells fell back on a "
                            "version bump")
                elif re.search(r"^signed:\s*⬜", text, re.M):
                    rep.add(WARN, "wisdom-handoff-unsigned", name,
                            "the handoff's `signed:` row is ⬜ — GI5 blocks, and a "
                            "DesignBoard binding this handoff is non-conformant "
                            "until a person signs")

        if ptype == "meta":
            check_partition_register(text, name, rep)

        if ptype == "question":
            for bad in re.findall(r"🚫\s?F\s?only\b|🚫F-only", text):
                rep.add(WARN, "refusal-token-legacy", name,
                        f"`{bad}` is not the token: a mark's spelling includes its "
                        "spacing and the canonical form is `🚫 F-only` "
                        "(for-question 0.4.1); a checker grepping the token misses "
                        "every legacy cell")
            lmq = re.search(r"^## Log\s*$", text, re.M)
            queue_side = text[:lmq.start()] if lmq else text
            # ## Log is excluded: a receipt QUOTING a retired token is a
            # mention, not a mark (round 4 friction 2 — the sweep's own
            # receipt tripped the rule it was satisfying).
            spaced = len(re.findall(r"[🟡🚫⬜](?=[A-Za-z])", queue_side))
            if spaced:
                rep.add(WARN, "mark-spacing-legacy", name,
                        f"{spaced} cell mark(s) run straight into a word (🟡BI03, "
                        "🚫thin, ⬜OPEN): a mark's spelling includes its spacing "
                        "(insight-workflow §Marks), and two spellings in one "
                        "column defeat the mark; re-spell in an authorized sweep "
                        "that re-pads the table")
            # One Queue row holds one cell per PARTITION COLUMN, so a single
            # line may carry several `final` cells; matching once per line
            # missed every column after the first on live A00 (QI3·C, QI7·C).
            hits = []
            for line in text.splitlines():
                lm = re.match(r"(Q[DIKW]\d+)", line)
                if lm:
                    for pid in re.findall(r"🟡\s*([A-Z]{1,3}\d{2})\s+final", line):
                        hits.append((lm.group(1), pid))
            for qid, pid in hits:
                cited = next((c for c in d.rglob(f"{pid}-*/{pid}-*.md")
                              if "board" not in c.relative_to(d).parts), None)
                if cited is None:
                    rep.add(ERROR, "partial-final-ghost-page", name,
                            f"`🟡 {pid} final` cites a page this board does not hold")
                else:
                    ctext = cited.read_text(encoding="utf-8")
                    lm = re.search(r"^## Log\s*$", ctext, re.M)
                    log = ctext[lm.end():] if lm else ""
                    # WARN, not ERROR, deliberately: a missing receipt is
                    # repairable debt on a settled decision, not broken
                    # structure — but it is scanned in ## Log ONLY, because a
                    # dated line elsewhere is prose, not a receipt (round 3
                    # friction 10: checker weaker than statute both ways).
                    if not re.search(rf"^\d{{6}} .*{qid}.*final|^\d{{6}} .*final.*{qid}",
                                     log, re.M):
                        rep.add(WARN, "partial-final-no-page-receipt", name,
                                f"`{qid}` leans on a sentence in {pid} and {pid}'s "
                                "## Log does not record it: the flip leaves TWO "
                                "receipts (insight-workflow §Marks), because a "
                                "citation invisible from the cited end cannot "
                                "carry staleness")


PARTITION_KEYWORDS = {
    "where", "and", "or", "not", "in", "eq", "ne", "lte", "gte", "declared",
    "unfiltered", "rows", "of", "no", "its", "own", "none", "null", "true",
    "false", "template", "row", "the", "test", "partition", "that", "passed",
    "contains", "every", "below", "fails", "clause", "construction", "which",
    "exempts", "from", "seated", "yaml", "cross", "full",
}


def _partition_rows(text):
    """MT00's partition register as (letter, name, population text, percent).

    Returns [] when the register does not parse. A rule that guesses at a
    layout it does not recognise reports noise, and noise is how a checker
    gets ignored.
    """
    m = re.search(r"\*\*Partitions\*\*.*?```text\n(.*?)```", text, re.S)
    if not m:
        return []
    rows, cur = [], None
    for line in m.group(1).splitlines():
        head = re.match(r"^([A-Z])\s{2,}(\S+)\s+(.*)$", line)
        if head:
            cur = [head.group(1), head.group(2), head.group(3)]
            rows.append(cur)
        elif cur is not None and line.strip():
            cur[2] += " " + line.strip()
    out = []
    for letter, nm, body in rows:
        pm = re.search(r"·\s*([\d.]+)\s*%", body)
        out.append((letter, nm, body, float(pm.group(1)) if pm else None))
    return out


def _filter_columns(body):
    """The column identifiers a partition's population block filters on."""
    body = re.sub(r"[\d,]+ of [\d,]+ rows.*", " ", body)
    body = re.sub(r"\S+\.yaml|\S+/", " ", body)
    return {w for w in re.findall(r"\b[a-z][a-z0-9_]{2,}\b", body)
            if w not in PARTITION_KEYWORDS}


def check_partition_register(text, name, rep):
    """The partition test's clause ① made mechanical (JL 260828, a live breach).

    `haipipe-insight-workflow` calls the three admission clauses "each
    mechanically checkable" and until 260828 none of the three was checked by
    anything. A00 registered `J · minorityzip` and `L · lowincome`, ran to
    136.79% coverage across seven subgroup partitions, grew a page under one,
    and this checker stayed green for the whole window; a human reader caught
    it. Clause ① is the one with a proof that needs no judgment: disjoint
    subgroups of ONE extract cannot cover more than the extract.

    F is the template and X is the cross group, and both are excluded by the
    statute itself — F "fails ① by construction, which the test exempts it
    from", and X holds no rows of its own.
    """
    rows = [r for r in _partition_rows(text) if r[0] not in ("F", "X")]
    if len(rows) < 2:
        return

    pcts = [r[3] for r in rows if r[3] is not None]
    if len(pcts) == len(rows):
        total = sum(pcts)
        # 100.5 not 100.0: the register prints rounded percentages, and a rule
        # that fires on rounding is a rule people learn to skip.
        if total > 100.5:
            named = " + ".join(f"{r[0]}·{r[1]} {r[3]:.2f}%" for r in rows)
            rep.add(ERROR, "partition-sum-over-100", name,
                    f"registered subgroup partitions cover {total:.2f}% of the "
                    f"extract ({named}) — disjoint groups of ONE extract cannot "
                    "exceed 100%, so clause ① is broken on arithmetic alone "
                    "(insight-workflow §The partition test): a coverage gap is "
                    "legal where an overlap never is, and overlapping groups "
                    "make every X contrast double-count the people they share")

    cols = {r[0]: _filter_columns(r[2]) for r in rows}
    for letter, nm, _, _ in rows:
        mine = cols[letter]
        if not mine:
            continue
        if all(not (mine & cols[other]) for other in cols if other != letter):
            rep.add(WARN, "partition-cross-cutting", name,
                    f"`{letter} · {nm}` filters on {sorted(mine)}, a column no "
                    "sibling partition filters on: a cut sharing no axis with "
                    "its siblings slices ACROSS them, which is a COVARIATE and "
                    "belongs in an I-page column, never a group "
                    "(insight-workflow §The partition test, the covariate row)")

    # A third rule was written and DROPPED the same hour: "a filter column MT00
    # names nowhere outside its own register". It fired four times on a
    # corrected A00 over `patient_gender`, which the page discusses at length in
    # prose without ever declaring as a column, and it passed `age` only because
    # substring matching found it inside "coverage". A rule that needs prose to
    # say a column's name in one exact place reports a documentation habit, not
    # a defect — and the covariate rule above already catches the case that
    # motivated it, since an unregistered filter column is almost always a
    # column no sibling shares.


def check_plugin_roster(d, rep):
    """A page subfolder is board material only if the roster names it.

    The roster states this as its own opening law, and it has been broken three
    times: `outline/` was real storage for four days before it had a row,
    `direction/` and `design/` shipped with contracts and no row, and
    `render/` shipped a SKILL that pointed at "the row this plugin expands"
    while that row did not exist. Prose could not stop it; a scan can.
    """
    roster = HERE.parent / "haipipe-plugin" / "ref" / "roster.md"
    if not roster.is_file():
        return
    names = set(re.findall(r'^\|\s*`([a-z_]+)/`', roster.read_text(encoding="utf-8"), re.M))
    if not names:
        return
    for md in sorted(d.rglob("*.md")):
        parts = md.relative_to(d).parts
        if "board" in parts or any(p.startswith("_") for p in parts):
            continue
        page = md.parent
        if md.stem != page.name:
            continue
        # A unit INSIDE a plugin lane (`display/S-Display-1a/…`, `probe/PP01/…`)
        # also keeps a `<name>/<name>.md`, and its `assets/`, `candidates/`,
        # `source/`, `versions/` are that plugin's own anatomy, not page
        # folders. The roster governs the page's direct children only; walking
        # into a lane reported 36 false rows on the MISQ board (JL 260831).
        if any(part in names for part in parts[:-1]):
            continue
        for sub in sorted(p for p in page.iterdir() if p.is_dir()):
            if sub.name.startswith("_") or sub.name in names:
                continue
            rep.add(WARN, "plugin-not-rostered", f"{page.name}/{sub.name}/",
                    "this subfolder is not on the plugin roster, so no surface, "
                    "writer or boundary is declared for it; add the row first")


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

    # A stale build is indistinguishable from link rot in this report: on 260829
    # a 9-day-old render shipped 184 dead-href ERRORs that a rebuild took to 0,
    # because the site still pointed at page-types deleted upstream. Say so
    # first, so nobody debugs the sources for a finding the build owns.
    built = (site / "index.html").stat().st_mtime
    newer = [f for f in d.rglob("*.md")
             if "/board/" not in f.as_posix() and f.stat().st_mtime > built]
    if newer:
        rep.add(WARN, "board-build-stale", "board/index.html",
                f"{len(newer)} source .md newer than the render "
                f"(e.g. {newer[0].relative_to(d).as_posix()}); run build.py before "
                f"trusting dead-href or completeness findings")

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


def print_rules():
    """The rulebook, derived from this file's own rep.add calls.

    The 260828 field test found the checker's laws teachable only through
    error text, discovered after writing (friction F11). This prints every
    finding code with its message template BEFORE anyone writes, from the
    same source the findings come from, so the roster cannot drift.
    """
    src = Path(__file__).read_text(encoding="utf-8")
    rules = {}
    for m in re.finditer(r'rep\.add\(\s*(ERROR|WARN|GAP),\s*"([a-z0-9-]+)"', src):
        level, code = m.group(1), m.group(2)
        # the call text: balance parens from the match to its closing one
        depth, i = 0, m.start()
        while i < len(src):
            if src[i] == "(":
                depth += 1
            elif src[i] == ")":
                depth -= 1
                if depth == 0:
                    break
            i += 1
        call = src[m.start():i]
        literals = re.findall(r'"((?:[^"\\]|\\.)*)"', call)[1:]  # drop the code itself
        msg = " ".join(s for s in literals
                       if len(re.sub(r"\{[^}]*\}", "", s).split()) >= 2)
        entry = rules.setdefault((level, code), {"msg": msg, "sites": 0})
        entry["sites"] += 1
        if not entry["msg"]:
            entry["msg"] = msg
    order = {ERROR: 0, WARN: 1, GAP: 2}
    print(f"{len(rules)} finding codes, derived from this file's rep.add calls\n")
    for (level, code), e in sorted(rules.items(), key=lambda kv: (order[kv[0][0]], kv[0][1])):
        sites = f" ({e['sites']} sites)" if e["sites"] > 1 else ""
        print(f"{level:<6} {code:<26} {e['msg'] or '(message is fully computed)'}{sites}")


def main():
    ap = argparse.ArgumentParser(description="structural half of QA9")
    ap.add_argument("board", nargs="?", help="the board folder")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 on any ERROR (JL's ruling on blocking is open; default reports)")
    ap.add_argument("--quiet", action="store_true", help="findings only, no summary")
    ap.add_argument("--no-template", action="store_true",
                    help="skip the template fixture (it shells out to build.py)")
    ap.add_argument("--summary", action="store_true",
                    help="score instead of a list: findings per rule and the "
                         "worst pages, so 'how are we doing' is one command")
    ap.add_argument("--rules", action="store_true",
                    help="print every finding code and its message, no board "
                         "needed: the laws, readable before writing")
    a = ap.parse_args()

    if a.rules:
        print_rules()
        return 0
    if not a.board:
        ap.error("a board folder is required unless --rules")

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
    check_design_family(d, rep)
    check_insight_family(d, rep)
    check_plugin_roster(d, rep)
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
