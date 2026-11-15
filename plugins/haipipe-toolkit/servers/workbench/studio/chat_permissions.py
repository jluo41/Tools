"""The Studio chat's permission rules: which tools run unasked, the tier a turn gets, and the Labeling hold.

Split out of chat.py (2026-11-13); chat.py re-exports every name here.
"""

import re
from pathlib import Path



# ── 权限：跟 Claude Code CLI 一样，该问就问（JL, 260723 1550）──────
# 原来是硬编码「只能改这一个文件」，越界直接拒。JL 要的是正常给权限：
# 只读工具自动放行，会动东西的弹给人看，人点允许 / 总是允许 / 拒绝。
READONLY = {"Read", "Glob", "Grep", "TodoWrite", "NotebookRead", "WebFetch", "WebSearch"}

# A one-click Quality Check must be evidence-gathering only, even if the
# browser had previously selected Full · no ask.  TodoWrite is deliberately
# absent: a quality report does not get to mutate any session state either.
QUALITY_READONLY = {"Read", "Glob", "Grep", "NotebookRead"}


def chat_scope(payload):
    """Resolve the permission mode; Quality Check is never client-escalatable."""
    if bool(payload.get("quality_check")):
        return "scoped"
    requested = payload.get("scope")
    # A browser that names no tier gets Full · no ask (JL 260802). The old
    # default was `full`, which prompts per tool call; on a board you drive on
    # your own files that is a click you make hundreds of times to say yes.
    # Quality Check above is exempt and stays read-only whatever is asked.
    return requested if requested in ("scoped", "full", "bypass") else "bypass"


def quality_tool_allowed(name):
    """The Quality Check tool surface is deliberately evidence-only."""
    return name in QUALITY_READONLY


def chat_guard(page, payload):
    """Return (read_only, mode, reason), with Labeling HOLD server-owned.

    `quality_check` is a useful browser request; a Labeling HOLD is an artifact
    fact and therefore cannot be disabled by changing or omitting that request.
    """
    page = Path(page)
    try:
        head = page.read_text(encoding="utf-8", errors="ignore")[:4096]
        labeling_hint = bool(re.search(r"(?m)^page-type:\s*labeling\s*$", head))
    except OSError:
        labeling_hint = False
    try:
        from .labeling import labeling_chat_hold
        labeling_hold, reason = labeling_chat_hold(page)
    except Exception:
        # A known Labeling page fails closed when its receipt derivation cannot
        # be trusted. Other Page types retain their ordinary Chat permissions.
        labeling_hold = labeling_hint
        reason = ("HOLD · labeling receipts could not be safely inspected"
                  if labeling_hint else "")
    read_only = bool(payload.get("quality_check")) or labeling_hold
    mode = "scoped" if read_only else chat_scope(payload)
    return read_only, mode, reason


# 真正会改盘上文件的工具 —— 只有跑过这些，才配说「改动已写盘」。
WRITE_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
