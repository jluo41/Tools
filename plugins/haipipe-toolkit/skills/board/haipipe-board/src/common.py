"""Shared constants + tiny helpers (QB5). Used by every page module AND by
serve.py — keep this file dependency-free (stdlib only, no intra-src imports)."""
import html
import re

# 状态标签用英文：OPEN / PARTIAL / SETTLED / ON HOLD 是 issue 追踪的通用词，
# 一眼知道什么意思，不像自造的中文缩写要人猜。
ST = {"✅": ("done", "SETTLED"), "🟡": ("wip", "PARTIAL"),
      "🔴": ("todo", "OPEN"), "⏸️": ("hold", "ON HOLD")}
STN = {k.replace("️", ""): v for k, v in ST.items()}
# 段落名用英文（两边都认：新板写英文，老板写中文照样能读）
# 一个槽位可以有多个段名：规范名 -> [别名…]。中文老名字一直认（老板子不用改就能重新生成），
# 260723 改版又加了两个新名：Done when -> 「Items to Finish」、Now -> 「Where we are」。
# "Opening" is the CANON for the lead section (JL 260731: "just one single
# Opening, Remove all the Question things from the skills"). Every existing
# page written as `## Question` keeps parsing through the alias, forever.
ALIAS = {"Opening": ["Question", "问题"], "Boundary": ["边界"], "Diagram": ["图"],
         "Stage Contract": ["Inherited Requirements", "阶段契约"],
         "Content": ["内容"],
         "Files": ["文件"],
         "Done when": ["完成线", "Items to Finish"],
         "Now": ["现在什么样", "Where we are"],
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
PAGENAME = re.compile(
    r"^(?:[QS][A-Za-z0-9]*|Agent-\d+|Meeting-\d+)[-_A-Za-z0-9]*\.md$")


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


def q_files(d):
    """Q*.md at any depth under the board folder (QC3, JL 260724): a question
    may live INSIDE the folder it is about (its home folder), so a board can
    sit on an existing tree like a paper's 0-lifecycle/. Path segments starting
    with `_` or `.` (archives, previews) and fig/ are not part of the board."""
    for p in sorted(d.rglob("Q*.md")):
        if any(s.startswith(("_", ".")) or s == "fig"
               for s in p.relative_to(d).parts[:-1]):
            continue
        yield p


def page_files(d):
    """Q, S, Skill, Agent and Meeting pages at any depth, same exclusions."""
    for prefix in ("Q", "S", "Agent", "Meeting"):
        for p in sorted(d.rglob(f"{prefix}*.md")):
            if any(s.startswith(("_", ".")) or s == "fig"
                   for s in p.relative_to(d).parts[:-1]):
                continue
            if PAGENAME.match(p.name):
                yield p
