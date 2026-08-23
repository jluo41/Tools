"""Shared constants + tiny helpers (QB5). Used by every page module AND by
serve.py — keep this file dependency-free (stdlib only, no intra-src imports)."""
import html
import json
import re
from pathlib import Path


def scene_text(scene) -> str:
    """The ONE way an Excalidraw scene is serialized (JL 260816).

    Two writers used to disagree: `cli/draw.py` wrote `indent=2` with raw
    UTF-8, `live/xcal.py` wrote `indent=1` with escapes, so a scene the split
    had saved never round-tripped through the CLI and every `draw.py retire`
    read the difference as a phantom concurrent edit. Both call this now, so a
    scene keeps one shape whichever hand last touched it. Raw UTF-8 keeps a
    Chinese label readable in a diff; the trailing newline keeps git quiet."""
    return json.dumps(scene, indent=2, ensure_ascii=False) + "\n"


# 状态标签用英文：OPEN / PARTIAL / SETTLED / ON HOLD 是 issue 追踪的通用词，
# 一眼知道什么意思，不像自造的中文缩写要人猜。
# 🗂 FOLDED is not a fifth degree of doneness, it is a different KIND of
# closed (JL 260807). ON HOLD means paused and someone will come back; FOLDED
# means this page's subject was merged into another page and nobody will. The
# page is deliberately KEPT so the merge stays traceable and its assets stay
# reachable, which is exactly why archiving it into `_archive/` is wrong: that
# hides the decision the page was kept to record. So it stays a real page, it
# stays linkable, and it only stops competing for room on the Index.
ST = {"✅": ("done", "SETTLED"), "🟡": ("wip", "PARTIAL"),
      "🔴": ("todo", "OPEN"), "⏸️": ("hold", "ON HOLD"),
      "🗂": ("folded", "FOLDED")}
STN = {k.replace("️", ""): v for k, v in ST.items()}
# 段落名用英文（两边都认：新板写英文，老板写中文照样能读）
# 一个槽位可以有多个段名：规范名 -> [别名…]。中文老名字一直认（老板子不用改就能重新生成），
# 260723 改版又加了两个新名：Done when -> 「Items to Finish」、Now -> 「Where we are」。
# 260801 JL 把这两个读者角色定成 Aims / States。旧名字永久保留为别名，
# 因为一个旧 Board 必须能在零迁移的情况下重新生成。
# "Opening" is the CANON for the lead section (JL 260731: "just one single
# Opening, Remove all the Question things from the skills"). Every existing
# page written as `## Question` keeps parsing through the alias, forever.
ALIAS = {"Opening": ["Question", "问题"], "Boundary": ["边界"], "Diagram": ["图"],
         "Stage Contract": ["Inherited Requirements", "阶段契约"],
         "Content": ["内容"],
         "Files": ["文件"],
         "Done when": ["完成线", "Items to Finish", "Aims"],
         "Now": ["现在什么样", "Where we are", "State", "States"],
         "Why here": ["为什么在这块板"],
         "Glossary": ["名词"], "Discussion": ["讨论"],
         "Law": ["规矩"], "Lesson": ["教训"], "Log": ["日志"],
         "Topic": ["主题"], "Pipeline": ["流水线"],
         "Pages": ["页面目录", "Roster", "清单"], "Links": ["链接"]}


def sec(d, key):
    """段落取值：先按规范名找，再挨个试别名（中文老名 + 新名）。"""
    if d.get(key):
        return d[key]
    for a in ALIAS.get(key, ()):
        if d.get(a):
            return d[a]
    return ""


# New Aims are durable target records, not tasks. Their state lives in the
# separate States section. A0.1 points at a Content division; P1 is the explicit
# page-level escape hatch for a target that crosses divisions. Old checkbox
# pages remain a first-class input and are counted by the same helper.
# `Q-<unit><Kind>-<n>` is here because a CONTRACT prescribes it, not because a
# page invented it: `haipipe-page-for-stage/SKILL.md:251` says the stage
# owns the id pattern and names this shape, "NOT A<n>". Parsing only A/P meant
# the engine could not read the ids its own contract required, so `QBt6`
# rendered `1/2 Aims met` off the two P rows while its States judged eight, and
# three of its four Aim groups rendered with no counter at all.
#
# It does not bite the live paper TODAY, and that is worth being exact about:
# 19 of its pages carry Q- ids, and all 19 sit inside legacy `- [ ]` checkboxes,
# which `aim_progress` counts on a separate branch that never looks at an id.
# What this unblocks is the migration off checkboxes: 94 Q- ids across those 19
# pages would have gone invisible the moment they became canonical rows.
AIM_ID = r"(?:A\d+(?:\.\d+)*|P\d+(?:\.\d+)*|Q-[A-Za-z][A-Za-z0-9]*-\d+(?:\.\d+)*)"
AIM_RE = re.compile(rf"(?m)^\s*[-*]\s+({AIM_ID})\s+·\s+\S")
# An Aim row's status glyph. 🔨 / 🧠 / ❄️ replaced 🟡 / 🟠 / ⏸️ on 260802,
# because the old set carried two of its five meanings in HUE ALONE: 🟡 and 🟠
# are one shape in two colours, indistinguishable in greyscale and to a
# colour-blind reader, and nothing about orange says "a person must answer".
# The new three say their meaning by shape: 🔨 work in progress, 🧠 waiting on
# the person who decides (the same glyph the `owner:` line already uses for
# JL), ❄️ on ice, deliberately held and thawable. The OLD three still parse,
# because 42 rows across the boards use them.
# This is the AIM row vocabulary only. The page `state:` line keeps its own
# ✅ / 🟡 / 🔴 / ⏸️ set, which means something different and is checked apart.
# Values are stored WITHOUT the variation selector, because the parser strips
# it: `❄️` arrives as `❄`, and a count against the selector form would silently
# read zero. Every canonical value below is the bare codepoint.
AIM_STATUS_ALIAS = {"🟡": "🔨", "🟠": "🧠", "⏸": "❄", "⏸️": "❄", "❄️": "❄"}
AIM_STATE_RE = re.compile(
    rf"(?m)^\s*[-*]\s*(⬜|🔨|🧠|✅|❄️?|🟡|🟠|⏸️?)\s+({AIM_ID})\s+·\s+\S"
)


def aim_ids(text):
    """Stable Aim ids in authored order, without duplicates."""
    return list(dict.fromkeys(AIM_RE.findall(text or "")))


def aim_progress(aims, state=""):
    """Return one progress record for canonical Aims or a legacy checklist.

    Canonical Aim completion is read only from States. Legacy pages keep their
    checkbox semantics so changing the reader vocabulary never falsifies an
    old Board's progress bar.
    """
    boxes = re.findall(r"(?m)^\s*[-*]\s*\[([ xX])\]", aims or "")
    if boxes:
        met = sum(1 for value in boxes if value.lower() == "x")
        return dict(mode="legacy", total=len(boxes), met=met, hold=0,
                    active=0, waiting=0, open=len(boxes) - met,
                    closed=met, ids=[])

    ids = aim_ids(aims)
    states = {}
    for emoji, aim_id in AIM_STATE_RE.findall(state or ""):
        e = emoji.replace("️", "")
        states[aim_id] = AIM_STATUS_ALIAS.get(e, e)
    values = [states.get(aim_id, "⬜") for aim_id in ids]
    met = values.count("✅")
    hold = values.count("❄")
    active = values.count("🔨")
    waiting = values.count("🧠")
    open_ = len(values) - met - hold - active - waiting
    return dict(mode="aims", total=len(ids), met=met, hold=hold,
                active=active, waiting=waiting, open=open_,
                closed=met + hold, ids=ids)


def aim_summary(aims, state=""):
    """Compact reader-facing States summary for a section row or sidebar."""
    progress = aim_progress(aims, state)
    if not progress["total"]:
        return "no aims"
    if progress["mode"] == "legacy":
        return f'{progress["met"]} met · {progress["open"]} open'
    parts = []
    for key, label in (("met", "met"), ("active", "active"),
                       ("waiting", "waiting"), ("open", "not started"),
                       ("hold", "on hold")):
        if progress[key]:
            parts.append(f'{progress[key]} {label}')
    return " · ".join(parts)


def stinfo(state):
    """'✅ 已定' / '⏸️ 会上没答完' -> (emoji, css-class, label)"""
    state = (state or "").strip() or "🔴"
    tok = state.split()[0]
    cls, lab = STN.get(tok.replace("️", ""), ("todo", "TODO"))
    rest = state[len(tok):].strip()
    return tok, cls, (rest or lab)


def who_class(who):
    """署名 -> 颜色。JL / CC 固定，其他同事按名字分到一个稳定的颜色。"""
    base = re.sub(r"\d+$", "", who).upper()
    if base in ("JL", "CC"):
        return base.lower()
    return "u" + str(sum(ord(c) for c in base) % 4)


def esc(s):
    return html.escape(str(s))


QNAME = re.compile(r"^Q[A-Za-z0-9]*[-_A-Za-z0-9]*\.md$")
SNAME = re.compile(r"^S[A-Za-z0-9]*[-_A-Za-z0-9]*\.md$")
# `Agent-<unit>-<slug>` is a page kind beside `Skill-<unit>` (JL 260731: "we
# will call it Agent-1 ... Below the skill"): a skill is LOADED, an agent is
# DISPATCHED, and the roster label should say which one a unit is.
# `Meeting-<unit>-<slug>` is the third kind beside them (QC10, JL 260731): not
# a decision and not a shipped unit, but the artifact a meeting leaves behind,
# mirrored from an `echo-meeting` vault note by `meetingpage.py`.
# `Design-<unit>-<slug>` replaced `Skill-<unit>-<slug>` on this family's own
# board (JL 260815: "we don't have the page for the Skill anymore. It will be
# the design"): a unit's page is a DESIGN page holding the argument plus the
# unit's material in plugins. `Skill-` stays legal so archives and other
# families' boards keep parsing.
# 260820, Application runtime boards. A ONE-OR-TWO letter family followed by a
# DIGIT: MT00-meta, D01-<slug>, I01, K01, W01 on an InsightBoard; BR00-brief,
# P01, DS01 on a DesignBoard. Generalised from a hardcoded [MIAD] set the same
# day, so a new family needs no engine edit. The required digit is what keeps
# AGENTS.md, DESIGN.md and MEMORY.md out; SKILL.md and STATUS.md do match, but
# through the pre-existing [QS] branch, which is long-standing behaviour.
PAGENAME = re.compile(
    r"^(?:[QS][A-Za-z0-9]*|[A-Z]{1,2}\d[A-Za-z0-9]*|Agent-\d+|Meeting-\d+|Design-\d+)"
    r"[-_A-Za-z0-9]*\.md$")


def _vet_path(name, pattern):
    """Board-relative page path -> clean posix string, or None."""
    name = (name or "").strip().replace("\\", "/")
    parts = [s for s in name.split("/") if s not in ("", ".")]
    if not parts or name.startswith("/") or ".." in parts:
        return None
    if not pattern.match(parts[-1]):
        return None
    return "/".join(parts)


def vet_qpath(name):
    """Board-relative Q-file path from the page -> clean posix string, or None.

    Since QC3 (JL 260724) a question may live in a subfolder of the board
    (`4-display/QD2-d01-iv-reporting.md`), so `file` payloads carry a relative
    path, not just a name. Reject anything absolute or climbing (`..`); the
    basename must still look like a Q file."""
    return _vet_path(name, QNAME)


def vet_pagepath(name):
    """Board-relative Q- or S-page path -> clean posix string, or None."""
    return _vet_path(name, PAGENAME)


def _page_home(p):
    """True when directory p is a folded page's home: `<name>/<name>.md`."""
    return (p / f"{p.name}.md").is_file()


def _in_plugin(p, d):
    """True when p is not board material because a PLUGIN holds it.

    Inside a folded page's folder every subfolder that is not itself a folded
    page is a plugin (JL 260815: "each subfolder will also be the plugin in
    that page"), and discovery never enters one. Child pages keep nesting, so
    a lifecycle tree still works. A page file lying directly beside the page's
    own md is a stray for the same reason. Without this rule a `skill/` plugin
    holding a unit snapshot would surface as a ghost page, because
    `PAGENAME.match("SKILL.md")` is true."""
    parts = p.relative_to(d).parts
    cur = d
    for seg in parts[:-1]:
        nxt = cur / seg
        if cur != d and _page_home(cur) and not _page_home(nxt):
            return True
        cur = nxt
    return cur != d and _page_home(cur) and p.name != f"{cur.name}.md"


def q_files(d):
    """Q*.md at any depth under the board folder (QC3, JL 260724): a question
    may live INSIDE the folder it is about (its home folder), so a board can
    sit on an existing tree like a paper's 0-lifecycle/. Path segments starting
    with `_` or `.` (archives, previews) and fig/ are not part of the board."""
    for p in sorted(d.rglob("Q*.md")):
        if any(s.startswith(("_", ".")) or s == "fig"
               for s in p.relative_to(d).parts[:-1]):
            continue
        if _in_plugin(p, d):
            continue
        yield p


def page_files(d):
    """Q, S, Design, Agent, Meeting and Application runtime pages at any depth,
    same exclusions. A legacy Skill-* page still rides the S glob, and the
    M/I/A/D globs are wide on purpose: PAGENAME does the real filtering."""
    for prefix in tuple("QSABCDEFGHIJKLMNOPRTUVWXYZ") + ("Agent", "Meeting", "Design"):
        for p in sorted(d.rglob(f"{prefix}*.md")):
            if any(s.startswith(("_", ".")) or s == "fig"
                   for s in p.relative_to(d).parts[:-1]):
                continue
            if _in_plugin(p, d):
                continue
            if PAGENAME.match(p.name):
                yield p


GROUPNUM = re.compile(r"^\d+-")
NUMBERED_GROUP = re.compile(r"^(\d+)-Q")


def group_stem(name):
    """`7-QC-engine` -> `QC-engine`. The NUMBER orders the folder on disk, the
    LETTER is still the group's identity, so every reader strips the number
    first (JL 260816).

    The number exists because letters carry identity and cannot carry order: on
    disk `QC-engine/` sorted four rows above `QPs-page-structure/` while board.md
    read them the other way round, and a folder that contradicts the board it
    stores is a folder nobody trusts. `## Pages` order stays the only authority;
    the number is DERIVED from it and `check.py` fails when the two disagree.

    An unnumbered folder passes through unchanged, so a board written before
    260816 keeps working with no migration."""
    return GROUPNUM.sub("", str(name))


def board_is_numbered(board):
    """Does this board already number its group folders?

    A board is numbered or it is not; there is no useful third state, and the
    WRITERS must not manufacture one. `＋Q` opening a single new group asks this
    first and follows whatever the board already does, so a legacy board never
    grows one numbered folder among eight bare ones. `regroup.py` is the
    exception and always numbers, because it lays down the whole set at once.

    The test requires `<N>-Q`, not a bare `<N>-`, because a paper's
    `0-lifecycle/` is numbered for an entirely different reason: `0-seed/`,
    `1-work/`, `3-display/` are SUBJECT folders whose numbers carry lifecycle
    order. Reading those as group numbering would have `＋Q` renumbering a
    board that never opted in."""
    return any(d.is_dir() and NUMBERED_GROUP.match(d.name)
               for d in Path(board).iterdir())
