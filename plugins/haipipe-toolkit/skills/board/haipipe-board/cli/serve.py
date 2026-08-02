#!/usr/bin/env python3
"""Serve boards AND accept comment writes — from the machine the files live on.

    python3 serve.py [--root DIR] [--port 5599]

Why this exists (JL, 260723): the first design had the browser write the .md
itself via the File System Access API. That cannot work here — the browser runs
on JL's laptop, the board files live on this server (Remote-SSH). The folder
picker would show the laptop's disk, which has none of this.

So the write moves to the side that actually has the files. This server already
serves the page; now it also takes two small POSTs and edits the markdown, then
regenerates board/ so a plain reload shows the rendered comment.

    POST /_board/comment   {path, file, who, sentence, text} -> append directly under sentence
    POST /_board/edit-sentence {path, file, sentence, replacement, who}
                                                      -> replace one sentence + append its diff
    POST /_board/resolve   {path, quote, done}        -> flip - [ ] <-> - [x]
    POST /_board/chat      {path, file, message, model, effort}
                                                      -> one turn with claude_agent_sdk
    POST /_board/stop      {path, file}                -> ask that turn to stop
    POST /_board/term      {path, file}                -> start a ttyd for that question
    POST /_board/release   {path, file}                -> hand the session back
    POST /_board/structure {path, op, ...}             -> add/archive groups and questions
                            op: add_group {title, letter?, hook?, body?}
                                add_question {group, title}
                                archive_question {q}     (moves to _archive/, never deletes)
                                archive_group {group}    (only when it lists no questions)
    POST /_board/activity  {path, op, span, page, ...} -> focus-time span / aggregates

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
  · binds 127.0.0.1 unless --host says otherwise. There is no auth of any kind
    and /_term/ is a real shell, so every address you bind to is an address that
    can run commands as you. A tailnet address (100.x) keeps that inside your own
    devices; 0.0.0.0 hands it to the whole local network.
  · the target must sit inside --root, in a folder containing board.md
    · the filename must match Q*.md or S*.md
  · writes are limited to sentence-adjacent comments, one-sentence edits, and
    the pre-existing narrowly scoped page actions below
"""
import argparse
import atexit
import difflib
import hashlib
import itertools
import base64
import json
import urllib.parse
import os
import shutil
import signal
import re
import sqlite3
import subprocess
import sys
import threading
import time
import datetime as dt
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote

HERE = Path(__file__).resolve().parent.parent  # the engine dir (this file lives in cli/)
sys.path.insert(0, str(HERE))
from src.common import QNAME, page_files, q_files, vet_pagepath, vet_qpath  # noqa: E402

# 正在跑的对话：文件路径 -> 一个「请停下」的旗子。
# POST /_board/stop 把旗子立起来，chat 循环在下一条消息处收工，

# ── QC8: the live layer lives in live/, one module per area ──────────────────
# serve.py is now what build.py became on 260724: a thin CLI plus the routing
# table.  Each area is a mixin; the class below is only their assembly order.
from live.base import BaseMixin, HOLD, TERMS, RUNS, ASKS, ALWAYS, ASK_SEQ
from live.activity import ActivityMixin
from live.home import HomeMixin
from live.write import WriteMixin
from live.chat import ChatMixin
from live import chat as live_chat
from live.term import (TermMixin, kill_all_terms, reap_stale_terms, term_key,
                       spawn_pty, pty_pump, pty_resize, ws_send)
from live.xcal import XcalMixin
from live.shell import ShellMixin
from live import base
# re-exported so the console (boards_api.py) keeps importing them from serve
# exactly as before (QE3's Law: one implementation, the console is a pipe).
from live.structure import structure_op, Q_STUB, _slugify, page_id_of   # noqa: F401
from live.chat import (prime_context, board_prime_context,              # noqa: F401
                       group_folder,
                       status_strip_context, tool_brief, oauth_token,
                       MODELS, EFFORTS, DEFAULT_MODEL, DEFAULT_EFFORT,
                       CHAT_RULES, FULL_RULES,
                       BOARD_CHAT_RULES, BOARD_FULL_RULES, READONLY, WRITE_TOOLS)


class Handler(BaseMixin, ActivityMixin, HomeMixin, WriteMixin, ChatMixin, TermMixin, XcalMixin, ShellMixin, SimpleHTTPRequestHandler):
    root = Path(".")
    # Logged edits are a SECOND kind of evidence, and a weaker one (QD8, JL
    # 260726: "we have so many activities in the past few dates, and they are
    # not recorded"). A timer cannot observe a browser session that already
    # ended, so every day before the timer shipped is empty while the pages'
    # own `## Log` sections record hundreds of dated changes.
    #
    # A Log line proves that a day had work. It carries NO duration. So it is
    # COUNTED and never converted into seconds, and it is drawn as its own
    # series: inventing minutes from a timestamp would make the strip look
    # complete by making it false, which is the same fabrication the reload
    # rule already refuses.
    LOG_LINE = re.compile(r"^(\d{6})(?:\s+\d{3,4})?\s*·")
    _log_cache = {}
    protocol_version = "HTTP/1.1"      # WebSocket 升级需要 1.1
    # The self-hosted Excalidraw runs in its own container on its own port, and
    # only 5599 is forwarded to JL's laptop — the same constraint that put ttyd on
    # a subpath. So it is proxied through here instead of asking for a second
    # forwarded port: an iframe at 127.0.0.1:5610 answers "refused to connect" on
    # any machine that is not the one running docker.
    #
    # The app asks for these at the ROOT, so they are proxied too; none of them
    # collides with anything a board serves.
    EXCAL_PATHS = ("/_excalidraw", "/assets/", "/favicon", "/manifest.webmanifest",
                   "/apple-touch-icon.png", "/sitemap.xml")
    # An image pasted into a scene is a base64 dataURL, and Excalidraw keeps it
    # INSIDE the file. One screenshot is megabytes of base64 that git then
    # re-diffs on every stroke, so here the bytes go to a sidecar folder beside
    # the scene and the scene keeps a pointer (JL 260726: "we can have an
    # assets folder for it"). The server rehydrates on the way out, so the
    # editor still receives the dataURL it expects and never knows.
    XMIME = {"image/png": ".png", "image/jpeg": ".jpg", "image/jpg": ".jpg",
             "image/svg+xml": ".svg", "image/gif": ".gif", "image/webp": ".webp"}
    def _term_route(self):
        """/_term/ 的分流：自有 PTY 在这里终结（/ws 走 ws_term，其余给个健康页），
        ttyd 后备照旧反代。返回 True 表示已经处理完。"""
        m = re.match(r"^/_term/([0-9a-f]{12})(/.*)?$", self.path)
        t = TERMS.get(m.group(1)) if m else None
        if not (t and t.get("kind") == "pty"):
            return False
        sub = m.group(2) or "/"
        if sub == "/ws":
            self.ws_term(m.group(1))
        else:
            body = b"PTY live"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(body)
        return True
    def end_headers(self):
        """A rebuilt page must reach the browser (JL 260802: "why is the page
        not updated automatically?").

        The watcher and the build were both working; the browser was serving a
        cached page. `_assets/*` is content-hashed with `?v=`, so it can be
        cached hard, but the HTML carries those hashes INSIDE it: cache the
        HTML and the reader keeps the old stamps too, so a CSS or JS change can
        never arrive no matter how many times the board is rebuilt.
        """
        path = getattr(self, "path", "") or ""
        if "/_assets/" in path and "?v=" in path:
            self.send_header("Cache-Control", "public, max-age=31536000, immutable")
        else:
            self.send_header("Cache-Control", "no-store, must-revalidate")
            self.send_header("Pragma", "no-cache")
        SimpleHTTPRequestHandler.end_headers(self)

    def do_GET(self):
        if self.is_home_request():
            return self.serve_home()
        # QD5 · the operating shell. Three routes, and they sit at the very top
        # because two of them are ordinary board URLs wearing a query string:
        # a pane must be recognised BEFORE the static handler serves the file.
        if self.path.split("?", 1)[0] == "/_shell":
            return self.serve_shell()
        if self.path.split("?", 1)[0] == "/_events":
            return self.serve_events()
        pane = self.pane_of(self.path)
        if pane:
            return self.serve_pane(pane)
        split = self.split_of(self.path)
        if split:
            return self.serve_shell(split)
        if self.path == "/_board/health":
            # checks/smoke.py 的探针：跑 chat 的是不是带 SDK 的解释器，只有
            # 进程自己答得出 —— ps 看到的是 venv 软链解析后的裸二进制，在外面
            # 重跑它就丢了 venv（260731 的 3.9 事故就是这么漏网的）。
            try:
                import claude_agent_sdk  # noqa: F401
                sdk = True
            except ImportError:
                sdk = False
            body = json.dumps({"ok": True, "python": sys.version.split()[0],
                               "sdk": sdk, "root": str(self.root)}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path.startswith("/_board/asset/"):
            return self.serve_asset()
        if self.path.startswith("/_term/"):
            if self._term_route():
                return
            return self.proxy_term()
        if ".excalidraw" in self.path.partition("?")[0]:
            return self.serve_frame()
        if self.path.startswith(self.EXCAL_PATHS):
            return self.proxy_excalidraw()
        # Last stop before the static handler: send the text compressed if the
        # browser asked for that (QD5 C2 P5). Falls through untouched otherwise.
        if self.try_gzip():
            return
        return SimpleHTTPRequestHandler.do_GET(self)
    def do_HEAD(self):
        if self.is_home_request():
            return self.serve_home()
        if self.pane_of(self.path):
            return self.head_pane()
        if self.path.startswith("/_term/"):
            if self._term_route():
                return
            return self.proxy_term()
        return SimpleHTTPRequestHandler.do_HEAD(self)
    def do_POST(self):
        if self.path.startswith("/_term/"):
            if self._term_route():
                return
            return self.proxy_term()
        if not self.path.startswith("/_board/"):
            return self.send_error(404)
        try:
            n = int(self.headers.get("Content-Length") or 0)
            p = json.loads(self.rfile.read(n) or b"{}")
        except Exception as e:
            return self.reply(400, {"ok": False, "err": f"请求体不是 JSON：{e}"})
        if self.path == "/_board/activity":
            try:
                res, err = self.activity(p)
            except Exception as e:
                return self.reply(500, {"ok": False, "err": f"{type(e).__name__}: {e}"})
            if err:
                return self.reply(400, {"ok": False, "err": err})
            return self.reply(200, res)
        if self.path == "/_board/answer":
            # 批准/拒绝一次工具调用 —— 不指向任何文件，所以在 target() 之前处理
            a = ASKS.get(str(p.get("id")))
            if not a:
                return self.reply(404, {"ok": False, "err": "这个请求已经过期了"})
            a["ok"] = bool(p.get("ok"))
            a["always"] = bool(p.get("always"))
            a["ev"].set()
            return self.reply(200, {"ok": True})
        if self.path == "/_board/excalidraw-save":
            # Targets a .excalidraw file, not a Q file, so it never reaches
            # target(). Also the one endpoint sendBeacon posts, on unload.
            try:
                res = self.save_excalidraw(p)
            except Exception as e:
                return self.reply(500, {"ok": False, "err": f"{type(e).__name__}: {e}"})
            return self.reply(200 if res.get("ok") else 400, res)
        if self.path == "/_board/terms":       # 列出所有在跑的终端（跨板）
            return self.reply(200, {"ok": True, "terms": self.list_terms()})
        if self.path == "/_board/killall":     # 一键全关
            n = len(TERMS)
            kill_all_terms()
            if live_chat.HOST is not None:      # held chat clients go too (QD1)
                live_chat.HOST.close_all()
            HOLD.clear()
            return self.reply(200, {"ok": True, "closed": n})
        if self.path == "/_board/structure":
            # Targets the BOARD, not one Q file, so it resolves the folder itself
            # instead of going through target() (which insists on a Q*.md name).
            page = unquote(p.get("path") or "")
            board = (self.root / page.lstrip("/")).resolve().parent
            try:
                board.relative_to(self.root.resolve())
            except ValueError:
                return self.reply(400, {"ok": False, "err": "越出了 --root"})
            if not (board / "board.md").exists():
                return self.reply(400, {"ok": False, "err": f"{board} 里没有 board.md"})
            try:
                res, err = structure_op(board, p)
            except Exception as e:
                return self.reply(500, {"ok": False, "err": f"{type(e).__name__}: {e}"})
            if err:
                return self.reply(400, {"ok": False, "err": err})
            return self.reply(200, {"ok": True, "build": self.rebuild(board),
                                    **(res or {})})
        if p.get("group"):
            # 组级会话（JL 260731）：身份是组的文件夹，不是哪个页面文件。
            # chat/term/sessions/session-name/release/stop 都吃这个 f。
            page = unquote(p.get("path") or "")
            board = (self.root / page.lstrip("/")).resolve().parent
            try:
                board.relative_to(self.root.resolve())
            except ValueError:
                return self.reply(400, {"ok": False, "err": "越出了 --root"})
            f = group_folder(board, p["group"])
            if f is None:
                return self.reply(400, {"ok": False,
                                        "err": f"这块板里找不到组 {p['group']!r} 的文件夹"})
        else:
            f, board = self.target(p)
        if f is None:
            return self.reply(400, {"ok": False, "err": board})
        if self.path == "/_board/image":
            # 存图不写 .md，也就不重建 —— 随后的 discuss/comment 写盘时才重建。
            try:
                res, err = self.save_image(board, p)
            except Exception as e:
                return self.reply(500, {"ok": False, "err": f"{type(e).__name__}: {e}"})
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/local-cmd":    # the command that lands in this session
            res, err = self.local_cmd(f, p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/term-probe":   # is this target's PTY still alive?
            res, err = self.term_probe(f)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/term":
            res, err = self.terminal(f, p, board)
            return self.reply(200 if not err else 409,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/sessions":    # 拣选器：这一题的会话清单（QD1 Law 260731）
            res, err = self.sessions_list(f, p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/session-log":    # that session's transcript (JL 260801)
            res, err = self.session_log(f, p), None
            return self.reply(200, res)
        if self.path == "/_board/session-name":   # 给 session 起名/改名（QD1 260731）
            res, err = self.name_session(f, p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/release":
            # park:true（页面 reload 的 beacon、⌨ 切回抽屉）→ 宽限停靠，进程活着；
            # 不带 park（killall、测试、显式关）→ 老样子直接杀。
            if p.get("park"):
                res, _ = self.park(f)
            else:
                res, _ = self.kill_term(f)
            return self.reply(200, {"ok": True, **(res or {})})
        if self.path == "/_board/stop":
            ev = RUNS.get(str(f))
            if ev:
                ev.set()
            return self.reply(200, {"ok": True, "stopping": bool(ev)})
        if self.path == "/_board/attach":   # QD2 R1: rejoin a turn already running
            res, err = self.attach(f, p)
            if res == "STREAMED":
                return                      # attach wrote its own NDJSON response
            return self.reply(200, {"ok": not err, "err": err, **(res or {})})
        ACTS = {"/_board/comment": self.add_comment,
                "/_board/edit-sentence": self.edit_sentence,
                "/_board/resolve": self.resolve,
                "/_board/discuss": self.add_discuss,
                "/_board/sentence": self.add_sentence,
                "/_board/diagram": self.add_diagram,
                "/_board/excalidraw": self.new_excalidraw,
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
    # 这个进程往往是从某个 Claude Code 会话的 shell 里起的：把「我是子会话」的
    # 标记就地摘掉，SDK 抽屉和 PTY 终端两条 spawn 路都不再继承它 —— 否则板上
    # 开的 claude 会关掉 transcript 落盘（QD3 Lesson，260731）。
    for _k in ("CLAUDE_CODE_CHILD_SESSION", "CLAUDE_CODE_SESSION_ID",
               "CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT", "CLAUDE_PID"):
        os.environ.pop(_k, None)
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--port", type=int, default=5599)
    ap.add_argument("--host", default="127.0.0.1",
                    help="绑哪个地址。默认只绑 loopback；给 tailnet 地址（100.x）"
                         "就能从自己别的设备直接打开，不用 VS Code 转发端口")
    ap.add_argument("--daemon", metavar="LOGFILE",
                    help="后台跑，输出写进这个文件")
    ap.add_argument("--ttyd", action="store_true",
                    help="终端走 ttyd 旧路（保险丝；默认 serve.py 自己管 PTY）")
    ap.add_argument("--no-hold", action="store_true",
                    help="QD2 M1 fuse: boot a claude per POST like before, "
                         "instead of holding one per question")
    a = ap.parse_args()
    # 260731 三次踩同一个坑：用系统 python 起 5599，页面照样 200，可 💬 每一轮
    # 都 400（claude_agent_sdk 要 3.10+）。人记不住的规矩交给代码——当前解释器
    # 没有 SDK 而 --root 下有 .venv 时，原地 exec 换成 venv 的 python 重启自己；
    # venv 也没有 SDK 就不换（防死循环），只警告一声继续跑。
    try:
        import claude_agent_sdk  # noqa: F401
    except ImportError:
        venv_py = Path(a.root).resolve() / ".venv" / "bin" / "python"
        if venv_py.exists() and Path(sys.executable).resolve() != venv_py.resolve():
            os.execv(str(venv_py), [str(venv_py)] + sys.argv)
        print("⚠️  这个 python 没有 claude_agent_sdk —— 💬 chat 会一直 400。"
              "用仓库的 .venv/bin/python 跑 serve.py。", file=sys.stderr)
    base.USE_TTYD = a.ttyd
    live_chat.HOLD_CHAT = not a.no_hold
    if a.daemon:
        daemonize(str(Path(a.daemon).resolve()))
    Handler.root = Path(a.root).resolve()
    base.BIND_HOST = a.host
    srv = ThreadingHTTPServer((a.host, a.port),
                              partial(Handler, directory=str(Handler.root)))
    # A non-loopback --host binds THAT ADDRESS ONLY, which quietly breaks the
    # path most people are actually on: a VS Code / ssh -L forward connects to
    # 127.0.0.1 on THIS machine, so a tailnet-only bind leaves the tunnel
    # pointing at a closed port and the board simply will not open (JL 260726,
    # twice in one evening). Loopback is therefore always ALSO served: it adds
    # no exposure that a local process does not already have, and it means
    # choosing a wider address never costs you the narrow one.
    loop = None
    if a.host not in ("127.0.0.1", "0.0.0.0", "localhost"):
        try:
            loop = ThreadingHTTPServer(("127.0.0.1", a.port),
                                       partial(Handler, directory=str(Handler.root)))
            threading.Thread(target=loop.serve_forever, daemon=True).start()
        except OSError as e:
            print(f"   ⚠️ loopback {a.port} 没起来：{e}", flush=True)
    tok, src = oauth_token(Handler.root)
    try:
        import claude_agent_sdk  # noqa: F401
        sdk = "on"
    except ImportError:
        sdk = "off（这个 Python 没装 SDK，聊天接口不可用）"
    print(f"📡 http://{a.host}:{a.port}  root={Handler.root}\n"
          + ("" if not loop else
             f"   ＋ http://127.0.0.1:{a.port} 也在听（VS Code / ssh -L 走的是这个）\n")
          + ("" if a.host == "127.0.0.1" else
             f"   ⚠️ 绑的不是 loopback：{a.host} 能到的设备都能用 /_term/ 开 shell\n")
          + f"   评论 / 状态：直接写在这台机器上\n"
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
