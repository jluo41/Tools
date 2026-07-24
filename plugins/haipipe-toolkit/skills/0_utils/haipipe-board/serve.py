#!/usr/bin/env python3
"""Serve boards AND accept comment writes — from the machine the files live on.

    python3 serve.py [--root DIR] [--port 5599]

Why this exists (JL, 260723): the first design had the browser write the .md
itself via the File System Access API. That cannot work here — the browser runs
on JL's laptop, the board files live on this server (Remote-SSH). The folder
picker would show the laptop's disk, which has none of this.

So the write moves to the side that actually has the files. This server already
serves the page; now it also takes two small POSTs and edits the markdown, then
regenerates board.html so a plain reload shows the rendered comment.

    POST /_board/comment   {path, who, quote, text}   -> append under ## Comments
    POST /_board/resolve   {path, quote, done}        -> flip - [ ] <-> - [x]
    POST /_board/chat      {path, file, message, model, effort}
                                                      -> one turn with claude_agent_sdk
    POST /_board/stop      {path, file}                -> ask that turn to stop
    POST /_board/term      {path, file}                -> start a ttyd for that question
    POST /_board/release   {path, file}                -> hand the session back

Auth for /_board/chat is OAuth, in this order:
  1. $CLAUDE_CODE_OAUTH_TOKEN                      (long-lived, `claude setup-token`)
  2. CLAUDE_CODE_OAUTH_TOKEN= in the repo's env.sh  (same thing, kept out of git)
  3. whatever `claude` is already logged in as      (~/.claude/.credentials.json)
No API key path — this is a subscription login, not a metered key.
Needs Python 3.10+ (the SDK does). Run it with the repo's own venv:
    .venv/bin/python Tools/.../haipipe-board/serve.py --root .
That venv is uv-managed and has no pip — install into it with:
    uv pip install --python .venv/bin/python claude-agent-sdk

`path` is the browser's own location.pathname, so the client never names a file
it isn't already looking at.

Deliberately narrow, because this is a write endpoint:
  · binds 127.0.0.1 only
  · the target must sit inside --root, in a folder containing board.md
  · the filename must match Q*.md
  · the only edits possible are "append a comment block" and "flip one checkbox"
"""
import argparse
import atexit
import hashlib
import itertools
import json
import os
import signal
import re
import subprocess
import sys
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote

HERE = Path(__file__).resolve().parent
QNAME = re.compile(r"^Q[A-Za-z0-9]*[-_A-Za-z0-9]*\.md$")

# 正在跑的对话：文件路径 -> 一个「请停下」的旗子。
# POST /_board/stop 把旗子立起来，chat 循环在下一条消息处收工，
# 生成器一关，底下那个 claude 子进程也跟着结束。
RUNS = {}

# ── LAW：一个 session 同时只能有一个窗口（JL, 260723 1500）────────
# 抽屉和终端读写的是磁盘上同一个 .jsonl。两边同时开，轻则互相覆盖，
# 重则 Claude Code 自己 fork 出第二个 session，那这一题就有两段历史了。
# 所以谁在用，登记在这里；另一边想开，先让它放手。
#   HOLD[<Q 文件绝对路径>] = ("drawer" | "terminal", 附加信息)
HOLD = {}
# TERMS: key（Q 文件绝对路径的 sha1[:12]，跨所有板全局唯一）-> 这个终端
#   {"pid", "sid", "sock"(unix socket 路径), "file"(绝对路径), "board"}
# 用 key 而不是端口：多块板各有各的 QD3，靠路径 hash 天然分开，绝不撞。
TERMS = {}
TERM_DIR = Path(os.environ.get("TMPDIR", "/tmp")) / "haiboard-terms"

# ── 权限：跟 Claude Code CLI 一样，该问就问（JL, 260723 1550）──────
# 原来是硬编码「只能改这一个文件」，越界直接拒。JL 要的是正常给权限：
# 只读工具自动放行，会动东西的弹给人看，人点允许 / 总是允许 / 拒绝。
READONLY = {"Read", "Glob", "Grep", "TodoWrite", "NotebookRead", "WebFetch", "WebSearch"}
# 真正会改盘上文件的工具 —— 只有跑过这些，才配说「改动已写盘」。
WRITE_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
ASKS = {}           # 请求 id -> {"ev": Event, "ok": bool, "always": bool}
ALWAYS = {}         # <Q 文件绝对路径> -> 这一轮里「总是允许」过的工具名
ASK_SEQ = itertools.count(1)


def term_key(f):
    """一个终端的全局唯一 id：Q 文件绝对路径的 sha1 前 12 位。
    跨所有板唯一（不同板的同名 QD3 路径不同 → key 不同），文件名安全、URL 安全。"""
    return hashlib.sha1(str(Path(f).resolve()).encode()).hexdigest()[:12]


def kill_all_terms(*_a):
    """把所有子 ttyd 一起收掉。退出时调（best-effort），killall 接口也调。"""
    for key, t in list(TERMS.items()):
        try:
            os.kill(t["pid"], signal.SIGTERM)
        except Exception:
            pass
        try:
            os.unlink(t["sock"])
        except Exception:
            pass
    TERMS.clear()


def reap_stale_terms():
    """启动时清掉上一轮遗留的 ttyd + socket。

    退出信号在 daemon + macOS 下不一定接得住，所以不靠它 —— 每次启动先扫一遍
    TERM_DIR，把还占着这些 socket 的 ttyd 杀掉、socket 删掉。保证不跨重启累积。"""
    try:
        socks = list(TERM_DIR.glob("*.sock"))
    except Exception:
        return
    if not socks:
        return
    import shutil
    want = {str(s) for s in socks}
    try:
        out = subprocess.run(["pgrep", "-f", "ttyd -i .*haiboard-terms"],
                             capture_output=True, text=True).stdout
    except Exception:
        out = ""
    for pid in out.split():
        try:
            os.kill(int(pid), signal.SIGTERM)
        except Exception:
            pass
    for s in socks:
        try:
            os.unlink(s)
        except Exception:
            pass
    del shutil, want


def prime_context(f, board, root):
    """开场定位：告诉会话它在哪块板、哪一题、这题问什么、还有几条评论没解决。
    终端用 --append-system-prompt 灌进去，抽屉拼进 system_prompt —— 一打开就知道自己在干嘛。"""
    try:
        rel = str(Path(f).resolve().relative_to(Path(root).resolve()))
    except ValueError:
        rel = f.name
    txt = Path(f).read_text(encoding="utf-8", errors="ignore")
    m = re.match(r"(Q[A-Za-z0-9]+)", f.name)
    qid = m.group(1) if m else Path(f).stem
    tm = re.search(r"^#\s+(.*)$", txt, re.M)
    title = tm.group(1).strip() if tm else ""
    qm = re.search(r"^## Question\s*\n(.*?)(?=\n## |\Z)", txt, re.S | re.M)
    qtext = " ".join(qm.group(1).split()) if qm else ""
    nopen = len(re.findall(r"^-\s*\[ \]\s", txt, re.M))
    btitle, bname = "", Path(board).name
    bmd = Path(board) / "board.md"
    if bmd.exists():
        bm = re.search(r"^#\s+(.*)$", bmd.read_text(encoding="utf-8", errors="ignore"), re.M)
        if bm:
            btitle = bm.group(1).strip()
    lines = [
        "You are opened on ONE question of a haipipe board. Orientation:",
        f"  · Board: {btitle or bname}   (folder: {bname})",
        f"  · Question: {qid} — {title}",
        f"  · This question's file (relative to your cwd = the repo root): {rel}",
    ]
    if qtext:
        lines.append(f"  · What it asks: {qtext[:280]}")
    if nopen:
        lines.append(f"  · It has {nopen} unresolved comment(s) in its ## Comments — read them before acting.")
    lines.append("Read that file for the full picture. You already know which question and board "
                 "this is; wait for the user's instruction.")
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

# 板上能选的模型。默认最好的那个 —— 这里是给人改文档用的，
# 省那点钱不如把话说对（JL, 260723）。
MODELS = {
    "opus":   "claude-opus-4-8",
    "sonnet": "claude-sonnet-5",
    "haiku":  "claude-haiku-4-5-20251001",
}
DEFAULT_MODEL, DEFAULT_EFFORT = "opus", "high"
EFFORTS = ("low", "medium", "high", "xhigh", "max")

CHAT_RULES = """You are attached to ONE question on a haipipe board.

Your working directory is the WHOLE repo (the SPACE), so you can read any code
the question touches — not just the board folder. The one question you belong to
is the file given below (a path relative to the repo root). That board folder
holds `board.md` (board-level title/spine/roster) and one `QX-<slug>.md` per
question, each with fixed sections:
## Question / ## Diagram / ## Done when / ## Now / ## Why here /
## Lesson / ## Glossary / ## Discussion / ## Comments / ## Log

Scope, and it is hard:
  · You may READ anywhere in the repo.
  · You may EDIT ONLY the one question file given below. Nothing else —
    not board.md, not another question, not build.py.
  · Every change you make, add one line at the TOP of that file's ## Log:
    `YYMMDD HHMM · what changed` (newest first).
  · Unresolved comments live in ## Comments as `- [ ] WHO 「quote」 · time`.
    When you have addressed one, flip it to `- [x]` and reply under it with
    `>> CC<MMDD>: what you did`.

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

Each `QX-<slug>.md` has fixed sections: ## Question / ## Diagram / ## Done when /
## Now / ## Why here / ## Law / ## Lesson / ## Glossary / ## Discussion /
## Comments / ## Log. Unresolved comments are `- [ ] WHO 「quote」 · time`; when
you address one, flip it to `- [x]` and reply under it with `>> CC<MMDD>: ...`.

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


def esc4re(s):
    return re.escape(s)


class Handler(SimpleHTTPRequestHandler):
    root = Path(".")

    def address_string(self):
        """不做反向 DNS。父类默认会 getfqdn(client_ip)，在这台机器上每个请求
        要卡十几秒才返回 —— 页面「没反应」「chat 没 response」都是这个。"""
        return self.client_address[0]

    def log_message(self, fmt, *a):
        sys.stderr.write("%s %s\n" % (self.address_string(), fmt % a))

    # ---- helpers -----------------------------------------------------
    def reply(self, code, obj):
        raw = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def target(self, payload):
        """browser pathname + file name -> a vetted Path, or (None, reason)"""
        page = unquote(payload.get("path") or "")
        name = payload.get("file") or ""
        if not QNAME.match(name):
            return None, f"文件名不像一个 Q 文件：{name}"
        board = (self.root / page.lstrip("/")).resolve().parent
        try:
            board.relative_to(self.root.resolve())
        except ValueError:
            return None, "越出了 --root"
        if not (board / "board.md").exists():
            return None, f"{board} 里没有 board.md，不像一块板"
        f = board / name
        if not f.exists():
            return None, f"找不到 {name}"
        return f, board

    def rebuild(self, board):
        r = subprocess.run([sys.executable, str(HERE / "build.py"), str(board)],
                           capture_output=True, text=True)
        return (r.stdout or r.stderr).strip()

    # ---- the two writes ----------------------------------------------
    def add_comment(self, f, p):
        who = re.sub(r"[^A-Za-z0-9]", "", p.get("who", "JL")).upper()[:4] or "JL"
        quote = " ".join((p.get("quote") or "").split())
        text = (p.get("text") or "").strip()
        when = p.get("when") or ""
        if not quote or not text:
            return None, "引文或正文是空的"
        body = "\n".join("      " + x for x in text.split("\n"))
        block = f"- [ ] {who} “{quote}”" + (f" · {when}" if when else "") + f"\n{body}\n"
        t = f.read_text(encoding="utf-8")
        # 找 ## Comments / ## Log 时跳过 ``` 代码围栏 —— 否则会写进
        # 「md 段落→页面位置」这类示例里的 ## Comments（真踩过，QA4 260723）。
        lines = t.split("\n")
        fence = False
        ci = li = None
        for i, ln in enumerate(lines):
            if ln.lstrip().startswith("```"):
                fence = not fence
                continue
            if fence:
                continue
            if ci is None and re.match(r"^## Comments\b", ln):
                ci = i
            if li is None and re.match(r"^## Log\b", ln):
                li = i
        if ci is not None:
            lines.insert(ci + 1, block.rstrip("\n"))
            t = "\n".join(lines)
        elif li is not None:
            lines.insert(li, "## Comments\n" + block.rstrip("\n") + "\n")
            t = "\n".join(lines)
        else:
            t = t.rstrip("\n") + "\n\n## Comments\n" + block
        f.write_text(t, encoding="utf-8")
        return block, None

    def add_discuss(self, f, p):
        """往 ## Discussion 末尾追加一条自由想法（一整段 → 一条 > WHO: …）。
        跟 add_comment 一样跳 ``` 围栏找真的段；没有 ## Discussion 就在
        ## Comments / ## Log 前新建。不钉在某句话上 —— 就是自由讨论。"""
        who = re.sub(r"[^A-Za-z0-9]", "", p.get("who", "JL")).upper()[:4] or "JL"
        text = " ".join((p.get("text") or "").split())
        if not text:
            return None, "想法是空的"
        line = f"> {who}: {text}"
        t = f.read_text(encoding="utf-8")
        lines = t.split("\n")
        fence = False
        di = ci = li = None
        for i, ln in enumerate(lines):
            if ln.lstrip().startswith("```"):
                fence = not fence
                continue
            if fence:
                continue
            if di is None and re.match(r"^## Discussion\b", ln):
                di = i
            if ci is None and re.match(r"^## Comments\b", ln):
                ci = i
            if li is None and re.match(r"^## Log\b", ln):
                li = i
        if di is not None:                      # 追加到 ## Discussion 段末尾
            j = di + 1
            while j < len(lines) and not re.match(r"^## ", lines[j]):
                j += 1
            while j > di + 1 and not lines[j - 1].strip():   # 跳过段尾空行
                j -= 1
            lines.insert(j, line)
            t = "\n".join(lines)
        else:                                   # 没有就新建一段
            anchor = ci if ci is not None else li
            if anchor is not None:
                lines.insert(anchor, "## Discussion\n" + line + "\n")
                t = "\n".join(lines)
            else:
                t = t.rstrip("\n") + "\n\n## Discussion\n" + line + "\n"
        f.write_text(t, encoding="utf-8")
        return "ok", None

    def resolve(self, f, p):
        quote = " ".join((p.get("quote") or "").split())
        to = "x" if p.get("done") else " "
        t = f.read_text(encoding="utf-8")
        pat = re.compile(r"^(-\s*\[)[ xX](\]\s*[A-Z]{1,4}\d{0,4}\s*[「\"“]"
                         + esc4re(quote) + r")", re.M)
        if not pat.search(t):
            return None, "在这个文件里找不到那条评论（引文对不上）"
        f.write_text(pat.sub(r"\g<1>" + to + r"\g<2>", t, count=1), encoding="utf-8")
        return "ok", None


    # ---- one chat turn, scoped to a single question ------------------
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
                                          TextBlock, ResultMessage, StreamEvent,
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
        mode = p.get("scope") if p.get("scope") in ("scoped", "full", "bypass") else "full"
        tok, src = oauth_token(self.root)
        env = {"CLAUDE_CODE_OAUTH_TOKEN": tok} if tok else {}
        prior = self.session_of(f)
        # 同终端那条：只有磁盘上真有这段对话才 resume。头部记了 id 但从没聊过（jsonl 不存在）
        # 的空壳，resume 会失败；这时当没有，起个全新的，结束时把新 id 写回头部覆盖掉空壳。
        if prior and not self.session_landed(prior):
            prior = None
        out, sid, usd = [], None, None
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
            if name in READONLY:
                return PermissionResultAllow()
            key = str(f)
            if name in ALWAYS.get(key, set()):
                return PermissionResultAllow()
            if name in ("Edit", "Write", "MultiEdit"):
                tgt = tin.get("file_path") or tin.get("path") or ""
                try:
                    if Path(tgt).resolve() == f.resolve():
                        return PermissionResultAllow()   # 这一题自己的文件，永远放行
                except Exception:
                    pass
            # scoped 档：除了这一题的文件，别的写操作一律拒（不弹，直接不给）
            if mode == "scoped" and name not in READONLY:
                denied.append(tool_brief(name, tin))
                return PermissionResultDeny(
                    message=f"「受限」档只能改 {f.name}。要动别的，把权限切到「完整」。")
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
            # cwd 是整个 repo（SPACE），不是板文件夹 —— 会话要能读它讨论的代码。
            # 所以给系统提示的是「相对 repo 根的路径」，不再是光文件名。
            try:
                rel = str(f.resolve().relative_to(self.root.resolve()))
            except ValueError:
                rel = f.name
            prime = prime_context(f, board, self.root)
            if mode == "scoped":
                sysp = CHAT_RULES + f"\n\nThe question file you may edit: {rel}\n\n" + prime
                sources = []                 # 不加载 CLAUDE.md / skill 注册表 → 便宜
            else:
                sysp = FULL_RULES + f"\n\nThis session's question file: {rel}\n\n" + prime
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
                kw["can_use_tool"] = can_use_tool
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
            async with ClaudeSDKClient(options=opts) as client:
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
                          elif type(b).__name__ == "ToolUseBlock":
                              nm = getattr(b, "name", "?")
                              if nm in WRITE_TOOLS:
                                  wrote.append(nm)
                              emit({"t": "tool", "name": nm})
                  elif isinstance(m, ResultMessage):
                      sid = m.session_id
                      usd = getattr(m, "total_cost_usd", None)

        try:
            anyio.run(run)
        except Exception as e:
            return None, f"{type(e).__name__}: {e}"
        finally:
            RUNS.pop(str(f), None)
            self.release(f, "drawer")
        if sid:
            self.remember_session(f, sid)
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
        m = re.search(r"^session:\s*(\S+)\s*$", f.read_text(encoding="utf-8"), re.M)
        return m.group(1) if m else None

    def remember_session(self, f, sid):
        t = f.read_text(encoding="utf-8")
        if re.search(r"^session:\s*\S+\s*$", t, re.M):
            t = re.sub(r"^session:\s*\S+\s*$", f"session: {sid}", t, count=1, flags=re.M)
        elif re.search(r"^method:.*$", t, re.M):
            t = re.sub(r"^(method:.*)$", r"\1\n" + f"session: {sid}", t, count=1, flags=re.M)
        else:
            return
        f.write_text(t, encoding="utf-8")


    # ---- 反代 /_term/<port>/... -> 127.0.0.1:<port> -------------------
    def proxy_term(self):
        """把终端从 5599 转出去。

        只有 5599 被 VS Code 转发到了 JL 的笔记本上；每开一个终端就多转发一个端口
        不现实，所以 ttyd 用 -b /_term/<port> 挂在子路径上，这里原样转过去。
        ttyd 的输出走 WebSocket，所以除了普通 HTTP 还要处理 Upgrade —— 握手之后
        两边就是裸 socket 对着倒字节，不用懂 WS 帧格式。
        """
        import socket as sk
        m = re.match(r"^/_term/([0-9a-f]{12})(/.*)?$", self.path)
        if not m:
            return self.send_error(404)
        key = m.group(1)
        t = TERMS.get(key)
        if not t:
            return self.send_error(404, "no such terminal")
        try:
            up = sk.socket(sk.AF_UNIX, sk.SOCK_STREAM)
            up.settimeout(10)
            up.connect(t["sock"])              # 连的是 unix socket，不是 TCP 端口
        except Exception as e:
            return self.send_error(502, f"terminal not reachable: {e}")
        try:
            head = f"{self.command} {self.path} HTTP/1.1\r\n"
            for k, v in self.headers.items():
                if k.lower() in ("host", "accept-encoding"):
                    continue
                head += f"{k}: {v}\r\n"
            head += "Host: localhost\r\nConnection: " + \
                    ("Upgrade\r\n" if self.headers.get("Upgrade") else "close\r\n")
            up.sendall((head + "\r\n").encode())
            n = int(self.headers.get("Content-Length") or 0)
            if n:
                up.sendall(self.rfile.read(n))
            if self.headers.get("Upgrade"):
                self.pump(up)                     # WebSocket：两边裸倒
            else:
                while True:
                    b = up.recv(65536)
                    if not b:
                        break
                    self.wfile.write(b)
                self.wfile.flush()
        except Exception:
            pass
        finally:
            try:
                up.close()
            except Exception:
                pass

    def pump(self, up):
        import select
        down = self.connection
        for s in (up, down):
            s.setblocking(False)
        while True:
            r, _, x = select.select([up, down], [], [up, down], 60)
            if x or not r:
                return
            for s in r:
                try:
                    b = s.recv(65536)
                except Exception:
                    return
                if not b:
                    return
                (down if s is up else up).sendall(b)

    # ---- LAW: 一个 session 一个窗口 ---------------------------------
    def hold(self, f, who):
        cur = HOLD.get(str(f))
        if cur and cur[0] != who:
            return f"这一题的 session 正被{'终端' if cur[0]=='terminal' else '网页抽屉'}占着。" \
                   f"先把那边关掉（终端那边点『交回 session』）再开这个。"
        HOLD[str(f)] = (who, None)
        return None

    def release(self, f, who=None):
        cur = HOLD.get(str(f))
        if cur and (who is None or cur[0] == who):
            HOLD.pop(str(f), None)

    # ---- 终端：给这一题起一个 ttyd（监听 unix socket），跑 claude --resume ----
    def terminal(self, f, p, board):
        import shutil
        import time
        exe = shutil.which("ttyd")
        if not exe:
            return None, "这台机器上没有 ttyd（brew install ttyd）"
        key = term_key(f)
        cur = TERMS.get(key)
        if cur and self.alive(cur["pid"]):
            return {"url": f"/_term/{key}/", "key": key,
                    "session": cur["sid"], "reused": True}, None
        err = self.hold(f, "terminal")
        if err:
            return None, err
        sid = self.session_of(f)
        # 不再抢 TCP 端口。ttyd 监听一个 unix socket 文件（-i <路径>）——
        # 一题一个 socket，没有端口池、不会占满、也不用 SSH 转发那些内部端口
        #（它们本来也没被转发，全靠 5599 反代）。
        TERM_DIR.mkdir(parents=True, exist_ok=True)
        sock = str(TERM_DIR / f"{key}.sock")
        try:
            os.unlink(sock)                    # 清掉可能残留的旧 socket
        except OSError:
            pass
        # -b /_term/<key>：让 ttyd 认自己挂在这个子路径下，页面里的相对路径才对得上。
        base = f"/_term/{key}"
        # 一题一个 session（JL 的 LAW）。用 --resume 还是 --session-id，看**磁盘上有没有那段对话**，
        # 不是光看头部有没有 id：
        #   头部有 id 且 jsonl 存在  → --resume（接着聊）
        #   头部有 id 但 jsonl 没有  → 这是「记了 id 却从没聊过」的空壳（reserved），
        #                              --resume 会「No conversation found」→ claude 秒退 → 终端一开就死。
        #                              改用 --session-id 拿这个 id 新起，别 --resume。
        #   头部没 id               → 生成一个、写回头部、--session-id
        import uuid
        use_resume = bool(sid) and self.session_landed(sid)
        if not sid:
            sid = str(uuid.uuid4())
            self.remember_session(f, sid)
        # 开场定位：--append-system-prompt 把「你在哪块板哪一题」灌进系统提示，
        # 不占一个回合、不让它自动跑，用户一开终端 claude 就已经知道自己在干嘛。
        prime = prime_context(f, board, self.root)
        m = re.match(r"(Q[A-Za-z0-9]+)", f.name)
        tm = re.search(r"^#\s+(.*)$", f.read_text(encoding="utf-8", errors="ignore"), re.M)
        ttl = ((m.group(1) if m else f.stem) + " · " + (tm.group(1).strip() if tm else f.name))[:60]
        cmd = [exe, "-i", sock, "-W", "-b", base,
               "-t", "titleFixed=" + ttl, "-t", "fontSize=13",
               "claude", "--append-system-prompt", prime,
               "--resume" if use_resume else "--session-id", sid]
        try:
            # cwd 是整个 repo（SPACE），不是板文件夹 —— 终端里的 claude 要能碰到它讨论的代码。
            # session 也因此归档在 repo 根的 project 目录下（跟抽屉一致）。
            proc = subprocess.Popen(cmd, cwd=str(self.root),
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            self.release(f, "terminal")
            return None, f"起不来 ttyd：{e}"
        for _ in range(50):                    # 等 socket 文件出现（最多 ~1s）
            if os.path.exists(sock):
                break
            time.sleep(0.02)
        TERMS[key] = {"pid": proc.pid, "sid": sid, "sock": sock,
                      "file": str(Path(f).resolve()), "board": str(board)}
        return {"url": base + "/", "key": key, "session": sid, "reused": False,
                "note": "" if use_resume else "这一题的新 session，已经记进文件头部了"}, None

    def session_landed(self, sid):
        """那段对话的 jsonl 真的落盘了吗（cwd = root 的 project 目录下）。
        没落盘的 id 是「记了却没聊过」的空壳，--resume 会失败让 claude 秒退。"""
        proj = str(Path(self.root).resolve()).replace("/", "-")
        return (Path.home() / ".claude" / "projects" / proj / f"{sid}.jsonl").exists()

    @staticmethod
    def alive(pid):
        try:
            os.kill(pid, 0)
            return True
        except Exception:
            return False

    def kill_term(self, f):
        cur = TERMS.pop(term_key(f), None)
        if cur:
            if self.alive(cur["pid"]):
                try:
                    os.kill(cur["pid"], 15)
                except Exception:
                    pass
            try:
                os.unlink(cur["sock"])
            except OSError:
                pass
        self.release(f)
        return {"closed": bool(cur)}, None

    def list_terms(self):
        """当前在跑的所有终端 —— 多板也一起列，因为 key 是全局的。"""
        out = []
        for key, t in list(TERMS.items()):
            if not self.alive(t["pid"]):
                TERMS.pop(key, None)
                continue
            out.append({"key": key, "session": t["sid"],
                        "file": Path(t["file"]).name,
                        "board": Path(t["board"]).name,
                        "url": f"/_term/{key}/"})
        return out

    protocol_version = "HTTP/1.1"      # WebSocket 升级需要 1.1

    def serve_asset(self):
        """serve vendored xterm from the skill folder, board-location-independent.
        /_board/asset/xterm.min.js  ·  /_board/asset/xterm.css"""
        name = self.path.rsplit("/", 1)[-1].split("?")[0]
        if name not in ("xterm.min.js", "xterm.css"):
            return self.send_error(404)
        p = HERE / "vendor" / "xterm" / name
        if not p.exists():
            return self.send_error(404, "asset missing (vendor xterm not installed)")
        data = p.read_bytes()
        ctype = "text/javascript" if name.endswith(".js") else "text/css"
        self.send_response(200)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "max-age=86400")
        self.end_headers()
        self.wfile.write(data)

    def guess_type(self, path):
        # .md 当纯文本发（utf-8），这样点卡片头那个「📄 QX.md」链接是**在浏览器里直接显示
        # 原始 markdown**，而不是弹下载。默认 mimetypes 会给 text/markdown，有的浏览器会下载。
        # 同理：## Files 里链到的源码类文件（.do/.R/.sql/…）也直接在浏览器里显示，
        # 否则默认 mimetypes 不认识就变成下载（JL 260724，cms_production.do 那次）。
        p = str(path)
        if p.rsplit(".", 1)[-1].lower() in (
                "md", "do", "r", "sql", "tex", "bib", "toml", "yaml", "yml",
                "sh", "ps1", "tsv", "log", "cfg", "ini"):
            return "text/plain; charset=utf-8"
        return SimpleHTTPRequestHandler.guess_type(self, path)

    def do_GET(self):
        if self.path.startswith("/_board/asset/"):
            return self.serve_asset()
        if self.path.startswith("/_term/"):
            return self.proxy_term()
        return SimpleHTTPRequestHandler.do_GET(self)

    def do_HEAD(self):
        if self.path.startswith("/_term/"):
            return self.proxy_term()
        return SimpleHTTPRequestHandler.do_HEAD(self)

    def do_POST(self):
        if self.path.startswith("/_term/"):
            return self.proxy_term()
        if not self.path.startswith("/_board/"):
            return self.send_error(404)
        try:
            n = int(self.headers.get("Content-Length") or 0)
            p = json.loads(self.rfile.read(n) or b"{}")
        except Exception as e:
            return self.reply(400, {"ok": False, "err": f"请求体不是 JSON：{e}"})
        if self.path == "/_board/answer":
            # 批准/拒绝一次工具调用 —— 不指向任何文件，所以在 target() 之前处理
            a = ASKS.get(str(p.get("id")))
            if not a:
                return self.reply(404, {"ok": False, "err": "这个请求已经过期了"})
            a["ok"] = bool(p.get("ok"))
            a["always"] = bool(p.get("always"))
            a["ev"].set()
            return self.reply(200, {"ok": True})
        if self.path == "/_board/terms":       # 列出所有在跑的终端（跨板）
            return self.reply(200, {"ok": True, "terms": self.list_terms()})
        if self.path == "/_board/killall":     # 一键全关
            n = len(TERMS)
            kill_all_terms()
            HOLD.clear()
            return self.reply(200, {"ok": True, "closed": n})
        f, board = self.target(p)
        if f is None:
            return self.reply(400, {"ok": False, "err": board})
        if self.path == "/_board/term":
            res, err = self.terminal(f, p, board)
            return self.reply(200 if not err else 409,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/release":
            res, _ = self.kill_term(f)
            return self.reply(200, {"ok": True, **res})
        if self.path == "/_board/stop":
            ev = RUNS.get(str(f))
            if ev:
                ev.set()
            return self.reply(200, {"ok": True, "stopping": bool(ev)})
        ACTS = {"/_board/comment": self.add_comment,
                "/_board/resolve": self.resolve,
                "/_board/discuss": self.add_discuss,
                "/_board/chat": None}
        if self.path not in ACTS:
            return self.reply(404, {"ok": False, "err": "没有这个接口"})
        try:
            res, err = (self.chat(f, p, board) if self.path == "/_board/chat"
                        else ACTS[self.path](f, p))
        except Exception as e:
            return self.reply(500, {"ok": False, "err": f"{type(e).__name__}: {e}"})
        if err:
            return self.reply(400, {"ok": False, "err": err})
        if res == "STREAMED":
            return                      # 流式那条路已经自己把响应写完了
        body = {"ok": True, "file": f.name, "build": self.rebuild(board)}
        if isinstance(res, dict):
            body.update(res)
        return self.reply(200, body)


def daemonize(log):
    """双 fork 脱离终端。macOS 没有 setsid，nohup 又常被上游进程组连坐，
    所以自己来 —— 这样服务器不会跟着某个 shell 一起消失。"""
    if os.fork() > 0:
        os._exit(0)
    os.setsid()
    if os.fork() > 0:
        os._exit(0)
    fd = os.open(log, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
    os.dup2(fd, 1)
    os.dup2(fd, 2)
    os.close(os.open(os.devnull, os.O_RDONLY))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--port", type=int, default=5599)
    ap.add_argument("--daemon", metavar="LOGFILE",
                    help="后台跑，输出写进这个文件")
    a = ap.parse_args()
    if a.daemon:
        daemonize(str(Path(a.daemon).resolve()))
    Handler.root = Path(a.root).resolve()
    srv = ThreadingHTTPServer(("127.0.0.1", a.port),
                              partial(Handler, directory=str(Handler.root)))
    tok, src = oauth_token(Handler.root)
    try:
        import claude_agent_sdk  # noqa: F401
        sdk = "on"
    except ImportError:
        sdk = "off（这个 Python 没装 SDK，聊天接口不可用）"
    print(f"📡 http://127.0.0.1:{a.port}  root={Handler.root}\n"
          f"   评论 / 状态：直接写在这台机器上\n"
          f"   聊天：{sdk} · 默认 {MODELS[DEFAULT_MODEL]} / effort={DEFAULT_EFFORT}\n"
          f"   OAuth 来源：{src}"
          + ("（长期 token）" if tok else "（沿用 claude 已登录的身份）")
          + "\n   Ctrl-C 停", flush=True)
    # 启动先清上一轮遗留（主力，不依赖退出信号），退出再尽力收一次
    reap_stale_terms()
    atexit.register(kill_all_terms)
    signal.signal(signal.SIGTERM, lambda *_: (kill_all_terms(), os._exit(0)))
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        kill_all_terms()
