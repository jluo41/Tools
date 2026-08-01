"""QC8 · the Claude Code bridge (QD2): rules, prime context, the SDK turn.

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
from .base import ALWAYS, ASKS, ASK_SEQ, HERE, RUNS, page_files
from .structure import page_id_of


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
    return requested if requested in ("scoped", "full", "bypass") else "full"


def quality_tool_allowed(name):
    """The Quality Check tool surface is deliberately evidence-only."""
    return name in QUALITY_READONLY


# 真正会改盘上文件的工具 —— 只有跑过这些，才配说「改动已写盘」。
WRITE_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}


def board_prime_context(board, root):
    """开场定位的整板版（QD5）：file=board.md 的会话不属于哪一题，属于整块板。
    给它的是索引页那份视野：spine / close / 每个 page 的状态和未解决评论数。"""
    board = Path(board)
    bmd = board / "board.md"
    txt = bmd.read_text(encoding="utf-8", errors="ignore") if bmd.exists() else ""
    tm = re.search(r"^#\s+(.*)$", txt, re.M)
    title = tm.group(1).strip() if tm else board.name
    spine = re.search(r"^spine:\s*(.*)$", txt, re.M)
    close = re.search(r"^close:\s*(.*)$", txt, re.M)
    try:
        rel = str(bmd.resolve().relative_to(Path(root).resolve()))
    except ValueError:
        rel = bmd.name
    rows, ndone, nall = [], 0, 0
    for p in page_files(board):
        t = p.read_text(encoding="utf-8", errors="ignore")
        st = re.search(r"^state:\s*(\S+)", t, re.M)
        st = st.group(1) if st else "🔴"
        ft = re.search(r"^#\s+(.*)$", t, re.M)
        nall += 1
        ndone += st.startswith("✅")
        rows.append("      · {} {} — {}".format(
            page_id_of(p.stem), st, (ft.group(1).strip() if ft else p.name),
        ))
    lines = [
        "You are opened on the WHOLE BOARD of a haipipe board — its index page, "
        "not any single question. Orientation:",
        f"  · Board: {title}   (board.md relative to your cwd = the repo root: {rel})",
    ]
    if spine:
        lines.append(f"  · Spine: {spine.group(1).strip()}")
    if close:
        lines.append(f"  · Close when: {close.group(1).strip()}")
    lines.append(f"  · Pages ({ndone}/{nall} settled):")
    lines.extend(rows)
    lines.append(
        "Board-level work is yours: which page to act on next, ## Pages order and "
        "grouping in board.md, cross-question consistency. Deep work inside one "
        "question belongs to that question's own chat. Read board.md for the full "
        "picture; wait for the user's instruction.")
    lines.extend(status_strip_context(board, "board", root))
    return "\n".join(lines)


def status_strip_context(board, focus, root):
    """Make a launched session's attachment visible in every reply (QD9)."""
    status_tool = HERE / "status.py"
    command = (
        f'python3 "{status_tool}" "{Path(board).resolve()}" '
        f'--focus "{focus}" --mode <mode> --status <status> '
        f'--next "<one concrete next action>" --root "{Path(root).resolve()}"'
    )
    return [
        "",
        "VISIBLE BOARD ATTACHMENT (mandatory):",
        "End EVERY user-visible reply with the exact three-line Markdown closing block "
        "printed by the command below. Choose the live mode, status, and next "
        "action for that reply. Put no prose after line 3.",
        f"  {command}",
        "Queue and page labels come from the Board files. Do not create or update "
        "a shared STATUS.md. Substantive outcomes still belong in the attached "
        "Board/page through the normal sync workflow.",
    ]


def group_folder(board, gname):
    """「QC · Engine」→ 这块板里的 QC-engine/ 文件夹（组的会话身份就是这个目录）。
    组标题的头一个词就是字母 id；文件夹按 <字母>- 前缀找，兼容裸字母目录。"""
    m = re.match(r"\s*([QS][A-Za-z]*\d*)", gname or "")
    if not m:
        return None
    letter = m.group(1)
    board = Path(board)
    for d in sorted(board.iterdir()):
        if d.is_dir() and not d.name.startswith(("_", ".")) \
                and (d.name == letter or d.name.startswith(letter + "-")):
            return d
    return None


def group_prime_context(f, board, root):
    """组级会话的开场定位（JL 260731：每个 question group 也要能聊）：
    这组是干嘛的、有哪些页、各自什么状态 —— 视野是一组，不是一页也不是整板。"""
    f = Path(f)
    letter = f.name.split("-")[0]
    bmd = Path(board) / "board.md"
    btxt = bmd.read_text(encoding="utf-8", errors="ignore") if bmd.exists() else ""
    bm = re.search(r"^#\s+(.*)$", btxt, re.M)
    gm = re.search(rf"^###\s+({re.escape(letter)}\b[^\n]*)$", btxt, re.M)
    gtitle = gm.group(1).strip() if gm else f.name
    try:
        rel = str(f.resolve().relative_to(Path(root).resolve()))
    except ValueError:
        rel = f.name
    rows = []
    for p in sorted(page_files(f)):
        t = p.read_text(encoding="utf-8", errors="ignore")
        st = re.search(r"^state:\s*(\S+)", t, re.M)
        ft = re.search(r"^#\s+(.*)$", t, re.M)
        rows.append("      · {} {} — {}".format(
            page_id_of(p.stem), st.group(1) if st else "🔴",
            ft.group(1).strip() if ft else p.name))
    lines = [
        "You are opened on ONE PAGE GROUP of a haipipe board — not the whole "
        "board, not a single page. Orientation:",
        f"  · Board: {(bm.group(1).strip() if bm else Path(board).name)}",
        f"  · Group: {gtitle}   (folder relative to your cwd = the repo root: {rel})",
        f"  · Its pages ({len(rows)}):",
    ]
    lines.extend(rows)
    lines.append(
        "Group-level work is yours: how these pages relate, what this group still "
        "owes, cross-page consistency INSIDE the group. Whole-board structure "
        "belongs to the board session; deep work inside one page belongs to that "
        "page's own chat. Read the pages for the full picture; wait for the "
        "user's instruction.")
    lines.extend(status_strip_context(board, letter, root))
    return "\n".join(lines)


def prime_context(f, board, root):
    """开场定位：告诉会话它在哪块板、哪一题、这题问什么、还有哪些未完成事项。
    终端用 --append-system-prompt 灌进去，抽屉拼进 system_prompt —— 一打开就知道自己在干嘛。
    file=board.md（QD5 整板会话）走整板那份定位，抽屉和终端共用这一个开关。"""
    if Path(f).is_dir():
        return group_prime_context(f, board, root)
    if Path(f).name == "board.md":
        return board_prime_context(board, root)
    try:
        rel = str(Path(f).resolve().relative_to(Path(root).resolve()))
    except ValueError:
        rel = f.name
    txt = Path(f).read_text(encoding="utf-8", errors="ignore")
    m = re.match(
        r"((?:Q[A-Za-z0-9]+|S-(?:Seed|Work|Venue|Display|Main|Appendix|Submission)-(?:\d+|[A-Z])|S(?:M|A)?\d+[a-z]?))",
        f.name,
        re.I,
    )
    qid = m.group(1) if m else Path(f).stem
    tm = re.search(r"^#\s+(.*)$", txt, re.M)
    title = tm.group(1).strip() if tm else ""
    qm = re.search(r"^## (?:Opening|Question)\s*\n(.*?)(?=\n## |\Z)", txt, re.S | re.M)
    qtext = " ".join(qm.group(1).split()) if qm else ""
    nitem = len(re.findall(r"^-\s*\[ \]\s", txt, re.M))
    btitle, bname = "", Path(board).name
    bmd = Path(board) / "board.md"
    if bmd.exists():
        bm = re.search(r"^#\s+(.*)$", bmd.read_text(encoding="utf-8", errors="ignore"), re.M)
        if bm:
            btitle = bm.group(1).strip()
    lines = [
        "You are opened on ONE page of a haipipe board. Orientation:",
        f"  · Board: {btitle or bname}   (folder: {bname})",
        f"  · Page: {qid} — {title}",
        f"  · This page's file (relative to your cwd = the repo root): {rel}",
    ]
    if qtext:
        lines.append(f"  · What it asks: {qtext[:280]}")
    if nitem:
        lines.append(f"  · {nitem} unticked item(s) in its ## Items to Finish.")
    lines.append("Read that file for the full picture. You already know which page and board "
                 "this is; wait for the user's instruction.")
    lines.extend(status_strip_context(board, qid, root))
    return "\n".join(lines)


def tool_brief(name, tin):
    """把工具调用压成一行给人看 —— 跟 CLI 弹的那个提示同一个意思。"""
    for k in ("file_path", "path", "notebook_path"):
        if tin.get(k):
            return f"{name}  {tin[k]}"
    if name == "Bash":
        return "Bash  " + str(tin.get("command", ""))[:160]
    keys = ", ".join(list(tin)[:3])
    return f"{name}  ({keys})" if keys else name


TOOL_CAP = 4000        # a card is a preview, not a full log viewer


def tool_input_preview(tin):
    """What the plugin shows in a call's IN block, truncated to a card."""
    if not isinstance(tin, dict):
        return str(tin)[:TOOL_CAP]
    if "command" in tin:                       # Bash reads best as the command
        return str(tin["command"])[:TOOL_CAP]
    try:
        return json.dumps(tin, ensure_ascii=False, indent=1)[:TOOL_CAP]
    except Exception:
        return str(tin)[:TOOL_CAP]


def tool_output_preview(content):
    """A tool result is text, a list of blocks, or neither; flatten to text."""
    if content is None:
        return ""
    if isinstance(content, str):
        return content[:TOOL_CAP]
    if isinstance(content, list):
        parts = []
        for b in content:
            if isinstance(b, dict):
                parts.append(b.get("text") or b.get("content") or "")
            else:
                parts.append(getattr(b, "text", "") or "")
        return "\n".join(str(x) for x in parts if x)[:TOOL_CAP]
    return str(content)[:TOOL_CAP]


# 板上能选的模型。默认最好的那个 —— 这里是给人改文档用的，
# 省那点钱不如把话说对（JL, 260723）。
MODELS = {
    "opus":   "claude-opus-5",
    "opus48": "claude-opus-4-8",
    "sonnet": "claude-sonnet-5",
    "haiku":  "claude-haiku-4-5-20251001",
}


DEFAULT_MODEL, DEFAULT_EFFORT = "opus", "high"


EFFORTS = ("low", "medium", "high", "xhigh", "max")


CHAT_RULES = """You are attached to ONE question on a haipipe board.

Your working directory is the WHOLE repo (the SPACE), so you can read any code
the question touches — not just the board folder. The one question you belong to
is the file given below (a path relative to the repo root). That board folder
holds `board.md` (board-level title/spine/pages) and one `QX-<slug>.md` per
question, each with fixed sections:
## Opening / ## Diagram / ## Content / ## Items to Finish /
## Where we are / ## Files / ## Law / ## Lesson / ## Glossary /
## Discussion / ## Log
(Old boards may still say `## Done when` for Items to Finish and `## Now` for
Where we are; both are accepted. `## Why here` is retired.)

Sentence-local review is a `>` line written DIRECTLY UNDER a sentence in the
body, bound to it by adjacency alone, and typed by its first word:
        The coefficient is 0.42 in the pooled model.
        > Check: 0.42 is from the robust-SE run, not the clustered one
        > JL: please fix this before the next draft
    Lanes are Citation, Value, Display, Check, Q-consumer, Link, Source, Note,
    plus `> JL:` and `> CC:` threads. A lane is addressed to whoever works on
    that sentence, which on this turn is you. Read them as requests about the
    sentence immediately above, not as quoted prose.

Scope, and it is hard:
  · You may READ anywhere in the repo.
  · You may EDIT ONLY the one question file given below. Nothing else —
    not board.md, not another question, not build.py.
  · Every change you make, add one line at the TOP of that file's ## Log:
    `YYMMDD HHMM · what changed` (newest first).
  · Preserve direct `> WHO:` comments and `> ✎` edit records; add new review
    feedback directly beneath the sentence it concerns.

Write the way the board is written: short topic line, then an indented
explanation. Plain language. No invented jargon. Answer in English by default;
only switch to another language if the user clearly writes to you in it."""


FULL_RULES = """You are a full Claude Code session attached to ONE question on a
haipipe board. Your working directory is the WHOLE repo (the SPACE) — you have
the full toolbelt, may call skills, and may reach any file the question is about.

The one question you belong to is the file given below (a path relative to the
repo root). This session belongs to that question: prefer to keep your board
edits inside its `QX-<slug>.md`, and whatever you change there, add one line at
the TOP of its `## Log`: `YYMMDD HHMM · what changed`.

Each `QX-<slug>.md` has fixed sections: ## Opening / ## Diagram / ## Done when /
## Now / ## Why here / ## Law / ## Lesson / ## Glossary / ## Discussion /
## Log. Preserve direct `> WHO:` comments and `> ✎` edit records beneath the
sentence they concern.

Write the way the board is written: short topic line, then an indented
explanation. Plain language, no invented jargon. Answer in English by default;
only switch to another language if the user clearly writes to you in it."""


BOARD_CHAT_RULES = """You are attached to the WHOLE BOARD of a haipipe board —
the index page, not one question.

Your working directory is the WHOLE repo (the SPACE), so you can read any code
the board discusses. The board folder given below holds `board.md` (title ·
`spine:` · `close:` · ## Topic / ## Pipeline / ## Pages) and one `QX-<slug>.md`
or `SN-<slug>.md` per page.

Scope, and it is hard:
  · You may READ anywhere in the repo.
  · You may EDIT ONLY markdown files INSIDE the board folder (board.md and the
    page files). Nothing outside it, and never board/ because it is generated.
  · Board-level work is yours: which page to act on next, ## Pages order,
    grouping and group intros, cross-question consistency. Deep work inside one
    question belongs to that question's own chat.
  · Every page you change, add one line at the TOP of its ## Log:
    `YYMMDD HHMM · what changed` (newest first).
  · Preserve direct `> WHO:` comments and `> ✎` edit records beneath the
    sentence they concern.

Write the way the board is written: short topic line, then an indented
explanation. Plain language. No invented jargon. Answer in English by default;
only switch to another language if the user clearly writes to you in it."""


BOARD_FULL_RULES = """You are a full Claude Code session attached to the WHOLE
BOARD of a haipipe board — the index page, not one question. Your working
directory is the WHOLE repo (the SPACE) — you have the full toolbelt, may call
skills, and may reach any file the board is about.

The board folder given below holds `board.md` (title · `spine:` · `close:` ·
## Topic / ## Pipeline / ## Pages) and one `QX-<slug>.md` or `SN-<slug>.md`
per page. Board-level work is yours: which page to act on next, the Pages section,
cross-question edits. Never hand-edit board/ because it is generated. Whatever
page you change, add one line at the TOP of its `## Log`:
`YYMMDD HHMM · what changed`. Preserve direct `> WHO:` comments and `> ✎`
edit records beneath the sentence they concern.

Write the way the board is written: short topic line, then an indented
explanation. Plain language, no invented jargon. Answer in English by default;
only switch to another language if the user clearly writes to you in it."""


def oauth_token(root):
    """OAuth token for the SDK, or None to fall back to the ambient login."""
    tok = os.environ.get("CLAUDE_CODE_OAUTH_TOKEN")
    if tok:
        return tok.strip(), "env"
    envsh = root / "env.sh"
    if envsh.exists():
        m = re.search(r"^\s*(?:export\s+)?CLAUDE_CODE_OAUTH_TOKEN=[\"\']?([^\"\'\s#]+)",
                      envsh.read_text(encoding="utf-8", errors="ignore"), re.M)
        if m:
            return m.group(1), "env.sh"
    return None, "ambient"

class _Live:
    """One question's held ClaudeSDKClient, plus the turn context it must see.

    `ctx` is the swap point that makes holding a client safe. `can_use_tool` is a
    CONNECT-time option, so a held client keeps whichever callback it was built
    with; if that callback closed over the first request's `emit`, message two's
    permission prompt would be written into message one's dead socket. The
    callback therefore closes over this object and reads `ctx` at call time, and
    each turn swaps its own context in.
    """

    __slots__ = ("client", "fp", "ctx", "last", "lock", "sid")

    def __init__(self, client, fp):
        self.client, self.fp = client, fp
        self.sid = None                       # the conversation this client IS
        self.ctx, self.last = None, time.time()
        self.lock = threading.Lock()          # one turn at a time per question


class SessionHost:
    """QD2 M1: one event loop for the process's life, owning every live client.

    The extension holds one `claude` per session and pushes each turn into it;
    we booted one per POST, which is the whole of the 8.1s first token and the
    per-message skill-registry reload. The SDK already supports this (its own
    docstring names chat UIs as the case for ClaudeSDKClient) with one hard
    constraint: a client may not cross async runtime contexts. So every
    operation on it happens on THIS loop, and the HTTP thread only submits.
    """

    def __init__(self):
        self.loop = None
        self.sessions = {}                    # str(question path) -> _Live
        self.lock = threading.Lock()
        self._ready = threading.Event()
        threading.Thread(target=self._serve, daemon=True,
                         name="chat-session-host").start()
        self._ready.wait(10)
        threading.Thread(target=self._reaper, args=(1800, 120), daemon=True,
                         name="chat-session-reaper").start()

    def _serve(self):
        import asyncio
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self._ready.set()
        self.loop.run_forever()

    def submit(self, coro):
        """Run a coroutine on the host loop; the caller's thread blocks on it."""
        import asyncio
        return asyncio.run_coroutine_threadsafe(coro, self.loop)

    async def acquire(self, key, fp, make_client, want=""):
        """The held client for this question, reconnecting only when it must.

        `fp` fingerprints every CONNECT-time option (model, effort, tier, which
        session is resumed). The system prompt is deliberately NOT in it: it is
        fixed at connect for a real CLI session too, so a page edit mid-chat
        does not silently restart the conversation.
        """
        live = self.sessions.get(key)
        # an explicit pick from the drawer's session strip overrides reuse:
        # "new" always starts fresh, a uuid must match the one we are holding
        picked_elsewhere = bool(want) and (want == "new" or
                                           (live is not None and want != live.sid))
        if live and live.fp == fp and not picked_elsewhere:
            live.last = time.time()
            return live, False
        if live:
            await self._drop(key)
        client = await make_client()
        live = _Live(client, fp)
        with self.lock:
            self.sessions[key] = live
        return live, True

    async def _drop(self, key):
        live = self.sessions.pop(key, None)
        if not live:
            return
        try:
            await live.client.disconnect()
        except Exception:
            pass

    def evict(self, key):
        """Release a question's client from any thread.

        QD1's Law is one window per session: when the ⌨ terminal takes a
        question, the drawer's held client must let go of the same .jsonl.
        """
        if not self.sessions.get(key):
            return
        try:
            self.submit(self._drop(key)).result(timeout=20)
        except Exception:
            pass

    def reap(self, idle_s=1800):
        now = time.time()
        for key, live in list(self.sessions.items()):
            if now - live.last > idle_s and not live.lock.locked():
                self.evict(key)

    def _reaper(self, idle_s, every):
        """A held client is a live `claude` process, so idleness must end it.

        Without this, opening ten questions leaves ten processes alive for the
        life of the server. Mirrors how QD3 reaps terminals rather than trusting
        exit signals.
        """
        while True:
            time.sleep(every)
            try:
                self.reap(idle_s)
            except Exception:
                pass

    def close_all(self):
        for key in list(self.sessions):
            self.evict(key)


TURN_GATE = {}         # question path -> the live turn's can_use_tool closure
HOST = None            # built on first use; --no-hold leaves it None (QD3m §8's
                       # --ttyd pattern: the old path stays reachable until JL
                       # has clicked through the new one)
HOLD_CHAT = os.environ.get("HAIBOARD_NO_HOLD", "") == ""


def host():
    global HOST
    if HOST is None:
        HOST = SessionHost()
    return HOST




class ChatMixin:
    def chat(self, f, p, board):  # noqa: C901
        """Run ONE turn of claude_agent_sdk against this question file.

        Cost control (the smoke test cost $0.92 with defaults): cwd is the board
        folder, not the repo, and setting_sources is empty — so the project's
        CLAUDE.md and the whole skill registry are NOT loaded. The model gets
        CHAT_RULES plus this one file's name, and nothing else.
        """
        msg = (p.get("message") or "").strip()
        if not msg:
            return None, "消息是空的"
        try:
            import anyio
            from claude_agent_sdk import (ClaudeSDKClient, ClaudeAgentOptions, AssistantMessage,
                                          TextBlock, ResultMessage, StreamEvent, UserMessage,
                                          PermissionResultAllow, PermissionResultDeny)
        except ImportError:
            return None, ("这个 Python 没装 claude_agent_sdk（要 3.10+）。"
                          "用仓库的 .venv/bin/python 跑 serve.py；"
                          "装的话：uv pip install --python .venv/bin/python claude-agent-sdk")

        model = MODELS.get(p.get("model") or DEFAULT_MODEL) or MODELS[DEFAULT_MODEL]
        effort = p.get("effort") if p.get("effort") in EFFORTS else DEFAULT_EFFORT
        # 权限档（JL 260723）：三档，默认「完整·问我」＝ 跟 CLI 一样。
        #   scoped  只这一题的文件 · 不加载技能 · 便宜（$0.24）
        #   full    全工具 + 全技能 · 逐个问你（CLI 默认行为）· 贵（~$0.9）
        #   bypass  全工具 + 全技能 · 什么都不问（= --dangerously-skip-permissions）
        quality_check = bool(p.get("quality_check"))
        mode = chat_scope(p)
        # 整板会话（QD5）：f 是 board.md 而不是某一题。规则、开场定位、
        # 「自动放行哪些写」三处跟着换；session 照旧记在 f（= board.md）头部。
        is_board = f.name == "board.md"
        # 组级会话（JL 260731）：f 是组的文件夹。权限面 = 这个文件夹里的 .md；
        # 规则复用整板那份措辞，但把「板」缩成「组」；session 记在登记表（目录无头部）。
        is_group = Path(f).is_dir()
        tok, src = oauth_token(self.root)
        env = {"CLAUDE_CODE_OAUTH_TOKEN": tok} if tok else {}
        prior = self.session_of(f)
        # 拣选器（QD1 Law 260731）：浏览器可以点名要哪一段历史，或者要求全新的一段。
        #   session:"new"     → 不 resume，跑完把新 id 写回头部（成为 current）
        #   session:"<uuid>"  → resume 选中的那段（落过盘才算数），跑完它成为 current
        #   不带 session      → 老样子，接头部里的 current
        want = (p.get("session") or "").strip()
        if want == "new":
            prior = None
        elif want:
            prior = want
        # 同终端那条：只有磁盘上真有这段对话才 resume。头部记了 id 但从没聊过（jsonl 不存在）
        # 的空壳，resume 会失败；这时当没有，起个全新的，结束时把新 id 写回头部覆盖掉空壳。
        if prior and not self.session_landed(prior):
            prior = None
        out, sid, usd = [], None, None
        # HOLD stops the drawer and the terminal fighting over one session, but
        # two drawer turns on the same question passed it, and with a HELD client
        # the second one silently queued behind the first forever (found by
        # driving the real page: 70s on "Thinking" for a one-word reply).
        if str(f) in RUNS:
            return None, "这一题已经有一轮在跑了，等它结束或按 ⏹ 停掉。"
        err = self.hold(f, "drawer")
        if err:
            return None, err
        stop = threading.Event()
        RUNS[str(f)] = stop
        stream = bool(p.get("stream"))
        if stream:                       # 流式：不等跑完，边出边发
            self.send_response(200)
            self.send_header("Content-Type", "application/x-ndjson; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Connection", "close")
            self.end_headers()

        def emit(obj):
            if not stream:
                return
            try:
                self.wfile.write((json.dumps(obj, ensure_ascii=False) + "\n").encode())
                self.wfile.flush()
            except Exception:
                stop.set()               # 浏览器断了 -> 也把这一轮停掉

        denied = []
        wrote = []          # 这一轮真的改过盘上文件的写工具名（决定要不要说「已写盘」）
        thought = [False]   # 思考是否已经逐字流过（流过了就别再整块补一遍）

        async def can_use_tool(name, tin, ctx):
            """权限闸门 —— 跟 Claude Code CLI 一个行为：该问就问。

            所有工具调用都必须走这里：写进 `allowed_tools` 的工具会在这个回调之前
            就被自动放行，`permission_mode` 一旦不是 `default` 也一样绕过
            （这两个坑是 haichat-inlab 注释里写明的）。所以两个都不给。

            走到这里之后的规则就跟 CLI 一样了：
              · 只读的直接放行
              · 会动东西的弹给人看，人点「允许 / 总是允许 / 拒绝」
              · 这一题自己的那个文件，默认就放行（本来就是来改它的）
            没人接（非流式、或者 5 分钟没人点）就拒 —— 默认安全那一侧。
            """
            if quality_check and not quality_tool_allowed(name):
                denied.append(tool_brief(name, tin))
                return PermissionResultDeny(
                    message="Quality Check is read-only: it may inspect evidence but cannot write or run tools.")
            if name in READONLY:
                return PermissionResultAllow()
            key = str(f)
            if name in ALWAYS.get(key, set()):
                return PermissionResultAllow()
            if name in ("Edit", "Write", "MultiEdit"):
                tgt = tin.get("file_path") or tin.get("path") or ""
                try:
                    rt = Path(tgt).resolve()
                    # 一题的会话：自己的那个文件永远放行。
                    # 整板会话（QD5）：板文件夹里的任何 .md 都算「自己的」——
                    # board.md 和所有 page 都是它的工作面；board.html 不是 .md，自然进不来。
                    if is_group:
                        ok = (rt.suffix == ".md"
                              and rt.is_relative_to(f.resolve()))
                    elif is_board:
                        ok = (rt.suffix == ".md"
                              and rt.is_relative_to(Path(board).resolve()))
                    else:
                        ok = rt == f.resolve()
                    if ok:
                        return PermissionResultAllow()
                except Exception:
                    pass
            # scoped 档：出了自己的工作面，别的写操作一律拒（不弹，直接不给）
            if mode == "scoped" and name not in READONLY:
                denied.append(tool_brief(name, tin))
                return PermissionResultDeny(
                    message=("「受限」档只能改这个组文件夹里的 .md。要动别的，把权限切到「完整」。"
                             if is_group else
                             "「受限」档只能改这块板文件夹里的 .md。要动别的，把权限切到「完整」。"
                             if is_board else
                             f"「受限」档只能改 {f.name}。要动别的，把权限切到「完整」。"))
            # full 档：跟 CLI 一样，弹给你点
            if not stream:
                denied.append(tool_brief(name, tin))
                return PermissionResultDeny(
                    message="这一轮没开流式，没法问你，先拒了。")
            def ask_detail():
                """What the VS Code extension shows before you allow: the actual
                proposed change, not just the tool name (JL 260724, duplicating
                the plugin). Truncated — a gate preview, not a full diff view."""
                cap = 4000
                try:
                    if name == "Edit":
                        return {"file": tin.get("file_path", ""),
                                "old": str(tin.get("old_string", ""))[:cap],
                                "new": str(tin.get("new_string", ""))[:cap]}
                    if name == "Write":
                        tgt = Path(tin.get("file_path", ""))
                        old = (tgt.read_text(encoding="utf-8", errors="replace")[:cap]
                               if tgt.exists() else "")
                        return {"file": str(tgt), "old": old,
                                "new": str(tin.get("content", ""))[:cap]}
                    if name == "MultiEdit":
                        eds = [{"old": str(e.get("old_string", ""))[:800],
                                "new": str(e.get("new_string", ""))[:800]}
                               for e in (tin.get("edits") or [])[:6]]
                        return {"file": tin.get("file_path", ""), "edits": eds,
                                "count": len(tin.get("edits") or [])}
                    if name == "Bash":
                        return {"command": str(tin.get("command", ""))[:1200]}
                except Exception:  # noqa: BLE001 — a broken preview must not block the gate
                    return None
                return None

            rid = str(next(ASK_SEQ))
            ASKS[rid] = {"ev": threading.Event(), "ok": False, "always": False}
            emit({"t": "ask", "id": rid, "tool": name,
                  "brief": tool_brief(name, tin), "detail": ask_detail()})
            await anyio.to_thread.run_sync(lambda: ASKS[rid]["ev"].wait(300))
            a = ASKS.pop(rid, {})
            if a.get("always"):
                ALWAYS.setdefault(key, set()).add(name)
            if a.get("ok"):
                return PermissionResultAllow()
            denied.append(tool_brief(name, tin))
            return PermissionResultDeny(message="你没有批准这一步。")

        async def run():
            nonlocal sid, usd
            # scoped 档要真的关掉「能动机器」的工具。can_use_tool 在
            # permission_mode=default 下对 Bash 这类不一定会被调用（实测 Bash
            # 直接放行了），所以用 disallowed_tools 硬关 —— 这条是 SDK 层的黑名单，
            # 不经过回调，最稳。scoped 只留读 + 改这一题的文件。
            SCOPED_OFF = ["Bash", "BashOutput", "KillShell", "Task",
                          "WebFetch", "WebSearch", "Skill"]
            if quality_check:
                SCOPED_OFF += ["Edit", "Write", "MultiEdit", "TodoWrite"]
            # cwd 是整个 repo（SPACE），不是板文件夹 —— 会话要能读它讨论的代码。
            # 所以给系统提示的是「相对 repo 根的路径」，不再是光文件名。
            try:
                rel = str(f.resolve().relative_to(self.root.resolve()))
            except ValueError:
                rel = f.name
            prime = prime_context(f, board, self.root)
            try:
                brel = str(Path(board).resolve().relative_to(self.root.resolve()))
            except ValueError:
                brel = str(board)
            if mode == "scoped":
                sysp = ((BOARD_CHAT_RULES + f"\n\nThe GROUP folder you may edit .md files in: {rel}\n\n")
                        if is_group else
                        (BOARD_CHAT_RULES + f"\n\nThe board folder you may edit .md files in: {brel}\n\n")
                        if is_board else
                        (CHAT_RULES + f"\n\nThe question file you may edit: {rel}\n\n")) + prime
                sources = []                 # 不加载 CLAUDE.md / skill 注册表 → 便宜
            else:
                sysp = ((BOARD_FULL_RULES + f"\n\nThis session's GROUP folder: {rel}\n\n")
                        if is_group else
                        (BOARD_FULL_RULES + f"\n\nThis session's board folder: {brel}\n\n")
                        if is_board else
                        (FULL_RULES + f"\n\nThis session's question file: {rel}\n\n")) + prime
                sources = ["user", "project", "local"]   # 加载技能 → Skill 工具可用
            kw = dict(
                cwd=str(self.root),
                system_prompt=sysp,
                setting_sources=sources,
                include_partial_messages=stream,   # 要逐字流式就得开这个
                max_turns=30 if mode != "scoped" else 12,
                env=env,
                resume=prior or None,
                model=model,
                effort=effort,
                # 显式开思考并给预算 —— 客户端收进折叠块。实测 effort 和 thinking 能并存，
                # 都会有 thinking_delta 流出来（adaptive 会让简单问题跳过，所以用 enabled）。
                thinking={"type": "enabled", "budget_tokens": 6000},
            )
            if mode == "scoped":
                kw["disallowed_tools"] = SCOPED_OFF   # 硬关，不经过 can_use_tool
            if mode == "bypass":
                # 全放行：permission_mode 一旦不是 default，can_use_tool 会被绕过，
                # 所以这里干脆不给回调，让它一路无提示地跑。
                kw["permission_mode"] = "bypassPermissions"
            else:
                # scoped / full：钉死 default + 走 can_use_tool（写 allowed_tools 或
                # 换 permission_mode 都会绕过回调 —— haichat-inlab 注释里的坑）。
                kw["permission_mode"] = "default"
                # A HELD client keeps the callback it was built with (M1), so it
                # cannot close over this request's emit. It calls through a
                # stable shim that reads whichever turn is live right now.
                async def gate(name, tin, gctx):
                    cb = TURN_GATE.get(str(f))
                    if cb is None:
                        return PermissionResultDeny(message="这一题当前没有在跑的对话。")
                    return await cb(name, tin, gctx)
                kw["can_use_tool"] = gate
            opts = ClaudeAgentOptions(**kw)
            # 用 ClaudeSDKClient，不用 query()。
            #
            # 为什么：can_use_tool 的「放不放行」是通过 stdin 那条控制通道回给 CLI 的。
            # query(prompt=<一次性的 async generator>) 在生成器吐完那一条消息之后就把
            # 输入流关了 —— 通道一关，后面模型再问「我能不能 Edit」就没人接得上，
            # CLI 等到超时报 `AbortError: Stream closed`。
            # 读操作往往赶在关闭之前问完，所以表现是「读得了、写就挂」。
            # ClaudeSDKClient 在整轮里把连接一直开着，回调才有地方回。
            # （haichat-inlab 用的也是 ClaudeSDKClient，不是 query。）
            # 等待期的真话（JL 260724「show the real things」）：boot 阶段一个事件都
            # 没有，页面只能挂一句假的「…thinking」。这里把真实阶段发出去。
            if stream:
                emit({"t": "stage",
                      "text": ("booting claude — the full tier loads the whole skill "
                               "registry, the first message is the slow one"
                               if sources else "booting claude (scoped — quick)")})
            async def drive(client, fresh):
              nonlocal sid, usd
              if stream:
                  emit({"t": "stage", "text": ("session up — sending your message"
                                               if fresh else "session already up")})
              await client.query(msg)
              async for m in client.receive_response():
                  if stop.is_set():
                      out.append("⏹ 已按你的要求停下。")
                      break
                  if isinstance(m, StreamEvent):
                      # 逐字增量。形状照 haichat-inlab 那边读到的：
                      # content_block_delta -> delta.type == "text_delta"
                      ev = getattr(m, "event", None) or {}
                      if ev.get("type") == "content_block_delta":
                          d = ev.get("delta") or {}
                          if d.get("type") == "text_delta" and d.get("text"):
                              emit({"t": "delta", "text": d["text"]})
                          elif d.get("type") == "thinking_delta" and d.get("thinking"):
                              # 思考过程，逐字发；客户端收进一个可折叠块
                              thought[0] = True
                              emit({"t": "think", "text": d["thinking"]})
                  elif isinstance(m, AssistantMessage):
                      for b in m.content:
                          bn = type(b).__name__
                          if bn in ("ThinkingBlock", "RedactedThinkingBlock"):
                              # 兜底：没走逐字流的思考（或整块到达），一次性发过去
                              tx = getattr(b, "thinking", "") or getattr(b, "text", "")
                              if tx and not thought[0]:
                                  emit({"t": "think", "text": tx})
                          elif isinstance(b, TextBlock) and b.text.strip():
                              out.append(b.text)
                              # 开了逐字流的话，这段文字已经一个字一个字发过了
                              if not stream:
                                  emit({"t": "text", "text": b.text})
                          elif type(b).__name__ in ("ToolUseBlock", "ServerToolUseBlock"):
                              nm = getattr(b, "name", "?")
                              if nm in WRITE_TOOLS:
                                  wrote.append(nm)
                              # The plugin shows a card per call: what it is, and
                              # what it was given. We used to send the name alone
                              # and the drawer threw it away on the next event
                              # (JL 260731, comparing the two side by side).
                              emit({"t": "tool", "name": nm,
                                    "id": getattr(b, "id", ""),
                                    "brief": tool_brief(nm, getattr(b, "input", {}) or {}),
                                    "input": tool_input_preview(getattr(b, "input", {}) or {})})
                  elif isinstance(m, UserMessage):
                      # the other half of the card: what the tool answered
                      for b in (m.content if isinstance(m.content, list) else []):
                          if type(b).__name__ in ("ToolResultBlock", "ServerToolResultBlock"):
                              emit({"t": "tool_result",
                                    "id": getattr(b, "tool_use_id", ""),
                                    "is_error": bool(getattr(b, "is_error", False)),
                                    "output": tool_output_preview(getattr(b, "content", None))})
                  elif isinstance(m, ResultMessage):
                      sid = m.session_id
                      usd = getattr(m, "total_cost_usd", None)

            if not HOLD_CHAT:                     # --no-hold: the pre-M1 path
                async with ClaudeSDKClient(options=opts) as client:
                    await drive(client, True)
                return
            # M1: reuse this question's client when nothing connect-time changed.
            # The system prompt is deliberately out of the fingerprint — it is
            # fixed at connect for a real CLI session too, so editing the page
            # mid-conversation must not silently restart it.
            # The fingerprint covers CONNECT-time options only. It must NOT
            # include `prior`: turn one has no session, turn two resumes the id
            # turn one just wrote into the page header, so folding it in made
            # every turn look different and silently reconnected every time
            # (caught by the stage line still saying "booting" on turn two).
            # A held client IS the conversation; only an explicit pick moves it.
            fp = (model, effort, mode, is_board, bool(stream))
            key = str(f)

            async def make():
                c = ClaudeSDKClient(options=opts)
                await c.connect()
                return c

            live, fresh = await host().acquire(key, fp, make, want=want)
            TURN_GATE[key] = can_use_tool
            live.lock.acquire()          # visible to reap(): this one is in use
            try:
                await drive(live.client, fresh)
            finally:
                if live.lock.locked():
                    live.lock.release()
                TURN_GATE.pop(key, None)
                live.last = time.time()
                if sid:
                    live.sid = sid            # what this held client now IS

        try:
            if HOLD_CHAT:
                # every operation on a held client must happen on the ONE loop
                # that owns it (the SDK forbids crossing async runtime contexts)
                fut = host().submit(run())
                try:
                    fut.result()
                finally:
                    # The browser going away (a reload, a closed tab) aborts the
                    # HTTP side but NOT the coroutine: it keeps running on the
                    # host loop with the client still mid-turn, and the next
                    # query queues behind it forever. Stop it, and drop the
                    # client, because its state is no longer known.
                    if not fut.done():
                        stop.set()
                        fut.cancel()
                        host().evict(str(f))
            else:
                anyio.run(run)
        except Exception as e:
            return None, f"{type(e).__name__}: {e}"
        finally:
            RUNS.pop(str(f), None)
            self.release(f, "drawer")
        if sid:
            self.remember_session(f, sid, name=p.get("name"))
        # 只有真改过盘上文件才重新生成 html —— 读一读、聊两句不该触发 rebuild
        build = self.rebuild(board) if wrote else ""
        if stream:
            emit({"t": "done", "text": "\n\n".join(out).strip(),
                  "session": sid, "usd": usd, "model": model, "scope": mode,
                  "effort": effort, "denied": denied, "stopped": stop.is_set(),
                  "wrote": bool(wrote), "build": build})
            return "STREAMED", None
        return {"text": "\n\n".join(out).strip(),
                "session": sid, "usd": usd, "auth": src, "denied": denied, "scope": mode,
                "wrote": bool(wrote), "stopped": stop.is_set(),
                "model": model, "effort": effort}, None

    # session id 就记在 Q 文件头部，跟 state/owner/method 并列
    def session_of(self, f):
        # 组（目录）没有头部行：current = 登记表最新的那条（record 插在最前）
        if Path(f).is_dir():
            rows = self._sess_map().get(str(Path(f).resolve()), [])
            r = rows[0] if rows else None
            return (r.get("id") if isinstance(r, dict) else r) or None
        m = re.search(r"^session:\s*(\S+)\s*$", f.read_text(encoding="utf-8"), re.M)
        return m.group(1) if m else None

    # ---- 会话登记（QD1 Law 修正，JL 260731：一题多 session，一个 current）----
    # 头部 `session:` 只记 CURRENT；这里登记这一题铸造过的每一个 id，
    # 拣选器从这里列历史。放 .haipipe-board/（跟 activity 一样，本机状态，gitignored）。
    def _sess_map_path(self):
        d = self.root / ".haipipe-board"
        d.mkdir(exist_ok=True)
        return d / "sessions.json"

    def _sess_map(self):
        try:
            return json.loads(self._sess_map_path().read_text(encoding="utf-8"))
        except Exception:
            return {}

    def record_session(self, f, sid, name=None):
        """登记条目从裸 id 升级成 {id, name}（JL 260731：session 要有名字，
        Qxxx-干什么用的）。旧表里的裸字符串就地迁移；name=None 不覆盖已有名。"""
        if not sid:
            return
        m = self._sess_map()
        key = str(Path(f).resolve())
        rows = [r if isinstance(r, dict) else {"id": r, "name": ""}
                for r in m.get(key, [])]
        old = next((r for r in rows if r["id"] == sid), None)
        if old:
            rows.remove(old)
            if not name:
                name = old.get("name", "")
        rows.insert(0, {"id": sid, "name": name or ""})   # 最新的在前
        m[key] = rows[:50]
        try:
            self._sess_map_path().write_text(json.dumps(m, indent=1),
                                             encoding="utf-8")
        except Exception:
            pass

    def name_session(self, f, p):
        """POST /_board/session-name {file, id, name} → 给某段 session 改名。
        名字住在登记表（板外之物不进 .md 头部：QD1「板上只记结果」）。"""
        sid = (p.get("id") or "").strip()
        name = " ".join((p.get("name") or "").split())[:80]
        if not sid:
            return None, "缺 id"
        self.record_session(f, sid, name=name or " ")     # 单空格 = 显式清名
        return {"id": sid, "name": name}, None

    def _jsonl_path(self, sid):
        proj = str(Path(self.root).resolve()).replace("/", "-")
        return Path.home() / ".claude" / "projects" / proj / f"{sid}.jsonl"

    def _session_title(self, sid):
        """第一条用户消息的开头 —— myrlin discover() 的取名法，照设计重写，不抄码。"""
        try:
            with open(self._jsonl_path(sid), encoding="utf-8", errors="ignore") as fh:
                for _ in range(200):
                    ln = fh.readline()
                    if not ln:
                        break
                    try:
                        o = json.loads(ln)
                    except Exception:
                        continue
                    if o.get("type") != "user":
                        continue
                    c = (o.get("message") or {}).get("content")
                    if isinstance(c, list):
                        c = " ".join(b.get("text", "") for b in c
                                     if isinstance(b, dict) and b.get("type") == "text")
                    if isinstance(c, str) and c.strip():
                        t = " ".join(c.split())
                        if t.startswith("<"):          # 跳过注入的 reminder 块
                            continue
                        return t[:90]
        except Exception:
            pass
        return ""

    def session_log(self, f, p):
        """POST /_board/session-log {file, id} -> that session's transcript.

        JL 260801: "when I load the previous session I only see the priming
        line, I cannot see previous chat history." The drawer replays a log it
        keeps in localStorage PER PAGE, so picking a different session showed
        the page's log rather than the session's, and a session started in a
        terminal or on another machine had no log in this browser at all.

        The .jsonl on disk is the only honest source, so read it: user text and
        assistant text, in order, skipping the machinery a reader never typed
        (tool calls, tool results, injected reminder blocks, and the priming
        message the board itself sends).
        """
        sid = (p.get("id") or "").strip()
        if not sid or sid == "new":
            return {"ok": True, "log": []}
        jp = self._jsonl_path(sid)
        if not jp.exists():
            return {"ok": True, "log": [], "hollow": True}

        def text_of(msg):
            c = (msg or {}).get("content")
            if isinstance(c, str):
                return c
            if isinstance(c, list):
                return "\n".join(b.get("text", "") for b in c
                                 if isinstance(b, dict) and b.get("type") == "text")
            return ""

        out, seen_first_user = [], False
        try:
            with open(jp, encoding="utf-8", errors="ignore") as fh:
                for ln in fh:
                    try:
                        o = json.loads(ln)
                    except Exception:
                        continue
                    kind = o.get("type")
                    if kind not in ("user", "assistant"):
                        continue
                    txt = text_of(o.get("message")).strip()
                    if not txt:
                        continue
                    if kind == "user":
                        # a reminder block, or a tool result echoed back as user
                        if txt.startswith("<") or txt.startswith("[Request interrupted"):
                            continue
                        # the board primes every session with its own opening
                        # message; replaying it would put words in JL's mouth
                        if not seen_first_user and (
                                "You are attached to" in txt
                                or "This chat sees" in txt
                                or txt.startswith("Board:")):
                            seen_first_user = True
                            continue
                        seen_first_user = True
                        out.append({"k": "you", "t": txt})
                    else:
                        out.append({"k": "ai", "t": txt})
        except Exception as e:
            return {"ok": False, "err": str(e)}
        # a very long session would blow up the drawer; keep the tail, which is
        # what "continue where I left off" actually means
        MAX = 120
        clipped = len(out) > MAX
        return {"ok": True, "log": out[-MAX:], "clipped": clipped, "total": len(out)}

    def sessions_list(self, f, p):
        """POST /_board/sessions {file} → 这一题的会话清单：current 在第一行，
        其余按最后动笔时间新→旧；hollow（记了 id 但 jsonl 没落盘）也列出来标明。"""
        cur = self.session_of(f)
        raw = self._sess_map().get(str(Path(f).resolve()), [])
        names = {}
        ids, seen = [], set()
        for r in ([{"id": cur}] if cur else []) + list(raw):
            if isinstance(r, str):
                r = {"id": r, "name": ""}
            sid = r.get("id")
            if sid and sid not in seen:
                seen.add(sid)
                ids.append(sid)
            if sid and r.get("name", "").strip():
                names[sid] = r["name"].strip()
        # 页面 id 前缀（JL 260731：Qxxx-这是干嘛的）：名字显示成 QD3m-fix-black-screen
        if Path(f).is_dir():
            prefix = Path(f).name.split("-")[0]        # QC-engine → QC
        else:
            m = re.match(r"((?:[QS][A-Za-z0-9]+|Skill-\d+|Agent-\d+))", Path(f).name)
            prefix = m.group(1) if m else Path(f).stem
        out = []
        for sid in ids:
            jp = self._jsonl_path(sid)
            row = {"id": sid, "current": sid == cur, "landed": jp.exists()}
            if sid in names:
                row["name"] = f"{prefix}-{names[sid]}"
            if row["landed"]:
                st = jp.stat()
                row["mtime"] = int(st.st_mtime)
                row["size"] = st.st_size
                row["title"] = self._session_title(sid)
            out.append(row)
        out.sort(key=lambda r: (not r["current"], -(r.get("mtime") or 0)))
        return {"current": cur, "prefix": prefix, "sessions": out}, None

    def remember_session(self, f, sid, name=None):
        # 换 current 的时候把旧的登进历史，新的也登上 —— 拣选器两边都要看得见
        old = self.session_of(f)
        if old and old != sid:
            self.record_session(f, old)
        self.record_session(f, sid, name=name)
        if Path(f).is_dir():
            return                      # 组（目录）没有头部 session: 行，登记表就是 current
        t = f.read_text(encoding="utf-8")
        if re.search(r"^session:\s*\S+\s*$", t, re.M):
            t = re.sub(r"^session:\s*\S+\s*$", f"session: {sid}", t, count=1, flags=re.M)
        else:
            # Q/S page 挂在 method: 后面；board.md（QD5 整板会话）没有 method:，
            # 挂在 close: 或 spine: 后面 —— 都是头部行，session 跟它们并列。
            for anchor in ("method", "close", "spine"):
                if re.search(rf"^{anchor}:.*$", t, re.M):
                    t = re.sub(rf"^({anchor}:.*)$", r"\1\n" + f"session: {sid}",
                               t, count=1, flags=re.M)
                    break
            else:
                return
        f.write_text(t, encoding="utf-8")

    def session_landed(self, sid):
        """那段对话的 jsonl 真的落盘了吗（cwd = root 的 project 目录下）。
        没落盘的 id 是「记了却没聊过」的空壳，--resume 会失败让 claude 秒退。"""
        proj = str(Path(self.root).resolve()).replace("/", "-")
        return (Path.home() / ".claude" / "projects" / proj / f"{sid}.jsonl").exists()
