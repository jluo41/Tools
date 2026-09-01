#!/usr/bin/env python3
"""Serve boards AND accept comment writes — from the machine the files live on.

    python3 serve.py [--root DIR] [--port PORT]

When --host, --port, --space-name, --public-url, or --auth-file is omitted,
the matching non-secret setting in <root>/.server_config/settings.env is used.
The explicit --no-auth flag disables HTTP Basic Auth for a trusted private
network such as a Tailscale tailnet.

Why this exists (JL, 260723): the first design had the browser write the .md
itself via the File System Access API. That cannot work here — the browser runs
on JL's laptop, the board files live on this server (Remote-SSH). The folder
picker would show the laptop's disk, which has none of this.

So the write moves to the side that actually has the files. This server already
serves the page; now it also takes two small POSTs and edits the markdown, then
regenerates board/ so a plain reload shows the rendered comment.

    POST /_board/comment   {path, file, who, sentence, text} -> append directly under sentence
    POST /_board/edit-sentence {path, file, sentence, replacement, who}
    POST /_board/card      {path, file, sentence, span, text} -> `> Card <span>: text`
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
  · binds 127.0.0.1 unless --host says otherwise. With --no-auth, /_term/ is a
    real shell available to every device that can reach the selected address.
    A tailnet address (100.x) keeps that inside the tailnet; 0.0.0.0 hands it
    to the whole local network.
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
from src.server_config import load_server_config, server_config_dir  # noqa: E402

# 正在跑的对话：文件路径 -> 一个「请停下」的旗子。
# POST /_board/stop 把旗子立起来，chat 循环在下一条消息处收工，

# ── QC8: the live layer lives in live/, one module per area ──────────────────
# serve.py is now what build.py became on 260724: a thin CLI plus the routing
# table.  Each area is a mixin; the class below is only their assembly order.
from live.base import BaseMixin, HOLD, TERMS, RUNS, ASKS, ALWAYS, ASK_SEQ
from live.auth import AuthMixin, AuthConfigError, host_is_loopback
from live.activity import ActivityMixin
from live.home import HomeMixin
from live.write import WriteMixin
from live.chat import ChatMixin
from live import chat as live_chat
from live.term import (TermMixin, kill_all_terms, reap_stale_terms, term_key,
                       spawn_pty, pty_pump, pty_resize, ws_send,
                       labeling_tui_hold)
from live.xcal import XcalMixin
from live.evidence import EvidenceTabMixin
from live.delivery import DeliveryTabMixin
from live.labeling import LabelingMixin
from live.shell import ShellMixin
from live.export import ExportMixin
from live.skillmap import SkillmapMixin
from live.pagex import PagexMixin
from live.meeting import MeetingMixin
from live.plugview import PlugViewMixin
from live.folderstat import FolderStatMixin
from live.outline import OutlineMixin
from live.value import ValueMixin
from live.pageruns import PageRunsMixin
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


# A proof file is EMBEDDED in an <iframe>, so it must RENDER, not download.
# `text/csv` makes some browsers offer a download instead; served as plain text
# it always renders, and the bytes on the wire are identical either way.
_INLINE_TEXT = {".csv": "text/plain", ".tsv": "text/plain", ".log": "text/plain",
                ".do": "text/plain", ".yaml": "text/plain", ".yml": "text/plain"}

# Textual payloads that `mimetypes` does not label `text/*`, and so would be
# served with no charset. See `guess_type` for the failure that made this list.
_UTF8_TYPES = {"application/javascript", "application/json", "application/xml",
               "image/svg+xml"}


class Handler(AuthMixin, BaseMixin, ActivityMixin, HomeMixin, WriteMixin, ChatMixin, TermMixin, XcalMixin, ShellMixin, ExportMixin, SkillmapMixin, PagexMixin, MeetingMixin, PlugViewMixin, FolderStatMixin, OutlineMixin, ValueMixin, EvidenceTabMixin, DeliveryTabMixin, LabelingMixin, PageRunsMixin, SimpleHTTPRequestHandler):
    root = Path(".")
    space_name = ""
    public_url = ""
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
    # A LIST MARKER IS OPTIONAL (260816). Both shapes are written on live
    # boards — `260803 · EXECUTED` and `- 260806 2215 · [REVISE-CC] swept` —
    # and only the bare one matched, so the readout was quietly showing 82% of
    # the updates (1260 counted, 276 dropped across the five skill boards).
    # Nothing caught it because the tests on this route all tested the focus
    # timer, which is now deleted, rather than the number the panel prints.
    LOG_LINE = re.compile(r"^[-*]?\s*(\d{6})(?:\s+\d{3,4})?\s*·")
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
        reason = labeling_tui_hold(t.get("file") or "")
        if reason:
            self.send_error(423, reason + " · TUI is read-only at this gate")
            return True
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
        if not self.require_auth():
            return
        if self.is_home_request():
            return self.serve_home()
        short = self.short_request()
        if short:
            return self.serve_short(*short)
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
        if self.fragment_of(self.path):
            return self.serve_fragment()
        split = self.split_of(self.path)
        if split:
            return self.serve_shell(split)
        if self.path.split("?", 1)[0] == "/_board/folderstat":
            # 📂 the page-folder's live status (never stored, so never stale)
            return self.folderstat_view()
        if self.path.split("?", 1)[0] == "/_board/outline":
            # 🧭 the page re-read per division (QPf12), same live contract
            return self.outline_view()
        if self.path.split("?", 1)[0] == "/_board/value":
            # 🔢 every number the page owes or uses, joined both ways (QPw4v)
            return self.value_view()
        if self.path.split("?", 1)[0] == "/_board/evidence":
            # 🧾 ONE surface over the four evidence lanes (JL 260831)
            return self.evidence_tab_view()
        if self.path.split("?", 1)[0] == "/_board/delivery":
            # 📤 ONE surface over the four delivery lanes (JL 260831)
            return self.delivery_tab_view()
        if self.path.split("?", 1)[0] == "/_board/labeling":
            # 🏷 canonical labeling receipts above, page chat below
            return self.labeling_view()
        if self.path.split("?", 1)[0] == "/_board/pageruns":
            # 🪜 one page's lifecycle receipts, for the Page phases stepper
            return self.pageruns_view()
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
        if self.path.startswith("/_board/skillview"):  # 🛠 the WHOLE skill, one page
            return self.serve_skillview()
        if self.path.startswith("/_board/pagexview"):  # 🔗 a borrow, with ← ☰ →
            return self.serve_pagexview()
        if self.path.startswith("/_board/mdview"):   # 🛠 a .md, rendered to read
            return self.serve_mdview()
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

    def guess_type(self, path):
        suf = os.path.splitext(str(path))[1].lower()
        if suf in _INLINE_TEXT:
            return _INLINE_TEXT[suf] + "; charset=utf-8"
        ctype = SimpleHTTPRequestHandler.guess_type(self, path)
        # A text response carrying NO charset is decoded by the browser's
        # locale default, not by UTF-8 and not by the encoding of the page that
        # linked it. Python's `mimetypes` sends a bare `text/css`, so every
        # non-ASCII glyph in a CSS `content:` rule mojibaked: the section-header
        # fold marker `▸` rendered as `â–¸`, which is windows-1252 reading the
        # three UTF-8 bytes one at a time (JL 260819). Stamp the charset on
        # everything textual this server hands out. The built stylesheet also
        # carries its own `@charset` now (src/assets.py CSS_CHARSET); this is
        # the half that fixes files already on disk without a rebuild.
        if isinstance(ctype, str) and "charset=" not in ctype and (
                ctype.startswith("text/") or ctype in _UTF8_TYPES):
            return ctype + "; charset=utf-8"
        return ctype
    def do_HEAD(self):
        if not self.require_auth():
            return
        if self.is_home_request():
            return self.serve_home()
        short = self.short_request()
        if short:
            return self.serve_short(*short)
        if self.pane_of(self.path):
            return self.head_pane()
        if self.path.split("?", 1)[0] == "/_board/folderstat":
            return self.folderstat_view(head_only=True)
        if self.path.split("?", 1)[0] == "/_board/outline":
            return self.outline_view(head_only=True)
        if self.path.split("?", 1)[0] == "/_board/value":
            return self.value_view(head_only=True)
        if self.path.split("?", 1)[0] == "/_board/evidence":
            return self.evidence_tab_view(head_only=True)
        if self.path.split("?", 1)[0] == "/_board/delivery":
            return self.delivery_tab_view(head_only=True)
        if self.path.split("?", 1)[0] == "/_board/labeling":
            return self.labeling_view(head_only=True)
        if self.path.startswith("/_term/"):
            if self._term_route():
                return
            return self.proxy_term()
        return SimpleHTTPRequestHandler.do_HEAD(self)
    def do_POST(self):
        if not self.require_auth():
            return
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
        if self.path == "/_board/autodraw":
            # ✨ the Draw tab's button: Claude authors this page's scene
            # (JL 260815). Targets a .excalidraw, so it never reaches target().
            # Threading server, so the minutes it thinks block nobody.
            try:
                from live.autodraw import autodraw
                res = autodraw(self.root, p)
            except Exception as e:
                return self.reply(500, {"ok": False, "err": f"{type(e).__name__}: {e}"})
            return self.reply(200 if res.get("ok") else 400, res)
        if self.path == "/_board/autodeck":
            # ✨ the Slides surfaces' button: Claude authors this page's deck
            # (JL 260815: the deck is the AI deck, and a button regenerates it).
            # Targets slide/<page>-deck.html, so it never reaches target().
            # Threading server, so the minutes it thinks block nobody.
            try:
                from live.autodeck import autodeck
                res = autodeck(self.root, p)
            except Exception as e:
                return self.reply(500, {"ok": False, "err": f"{type(e).__name__}: {e}"})
            return self.reply(200 if res.get("ok") else 400, res)
        if self.path == "/_board/excalidraw-save":
            # Targets a .excalidraw file, not a Q file, so it never reaches
            # target(). Also the one endpoint sendBeacon posts, on unload.
            try:
                res = self.save_excalidraw(p)
            except Exception as e:
                return self.reply(500, {"ok": False, "err": f"{type(e).__name__}: {e}"})
            status = 200 if res.get("ok") else (409 if res.get("conflict") else 400)
            return self.reply(status, res)
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
        # The DERIVED paper-facing plugins (haipipe-plugin roster):
        # each writes into the page's own plugin folder and answers with the
        # URL the right-pane tab frames. One route per plugin, one mixin.
        if self.path == "/_board/latex":      # page -> latex/<stem>.tex + .pdf
            res, err = self.export_latex(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/word":       # page -> word/<stem>.docx + PDF twin
            res, err = self.export_word(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/bibex":      # refresh the page-owned bib + view
            res, err = self.export_bibex(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/bibex-verify":   # the human ✓: one verified field
            res, err = self.bibex_verify(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/bibex-entry":    # the pen: land a person's entry
            res, err = self.bibex_entry(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        # 🛠 the skill map, bibex's twin (haipipe-plugin): the page's
        # citations into the SKILL tree, one store + one workbench view.
        if self.path == "/_board/skill":          # refresh: seed-scan + view
            res, err = self.skillmap_refresh(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/skill-order":    # the drag: rank = the order
            res, err = self.skillmap_order(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/skill-entry":    # the pen: add · ✕ · restore
            res, err = self.skillmap_entry(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        # 🔗 pagex, the THIRD citation twin (QPf11): the page's borrowings
        # from other pages, one store + symlinks re-minted from it.
        if self.path == "/_board/pagex":          # re-mint the links + view
            res, err = self.pagex_refresh(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/pagex-order":    # the drag: rank = the order
            res, err = self.pagex_order(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/pagex-entry":    # the pen: borrow · ✕ · ↩
            res, err = self.pagex_entry(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/pagex-match":    # SURVEY's read-only shortlist
            res, err = self.pagex_match(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        # 🗣 meeting (QPf14): a person's own record of a conversation, kept
        # under <page>/meeting/<YYMMDD-HHMM>/ — digest.md + transcript.md.
        if self.path == "/_board/meeting":        # the view: list kept meetings
            res, err = self.meeting_view(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/meeting-entry":  # the pen: keep a meeting
            res, err = self.meeting_entry(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        # The EVIDENCE plugins' read-only surfaces (QPf5 · QPf9): the view
        # lists the page's units or cards and writes nothing but itself.
        if self.path == "/_board/folderstat":  # 📂 the tab spec's write() twin
            res, err = self.plug_folderstat(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/outline":     # 🧭 the same live twin (QPf12)
            res, err = self.plug_outline(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/value":       # 🔢 the same live twin (QPw4v)
            res, err = self.plug_value(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/delivery":    # 📤 the same live twin (JL 260831)
            res, err = self.plug_delivery(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/evidence":    # 🧾 the same live twin (JL 260831)
            res, err = self.plug_evidence(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/labeling":    # 🏷 read-only receipt surface
            res, err = self.plug_labeling(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/display":    # list display/ units + previews
            res, err = self.plug_display(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/probe":      # list probe/ cards + states
            res, err = self.plug_probe(p)
            return self.reply(200 if not err else 400,
                              {"ok": not err, "err": err, **(res or {})})
        if self.path == "/_board/term-type":   # a surface types one line into the PTY
            res, err = self.term_type(f, p)
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
        if self.path == "/_board/chat-keep":      # sessions land in the page's chat/ (QPf4, JL 260815)
            return self.reply(200, self.keep_sessions(f, p))
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
                "/_board/card": self.add_card,
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
    ap.add_argument("--port", type=int, default=None,
                    help="listener port; root .server_config wins when omitted")
    ap.add_argument("--host", default=None,
                    help="绑哪个地址。默认只绑 loopback；给 tailnet 地址（100.x）"
                         "就能从自己别的设备直接打开，不用 VS Code 转发端口；"
                         "root .server_config wins when omitted")
    ap.add_argument("--daemon", metavar="LOGFILE",
                    help="后台跑，输出写进这个文件")
    ap.add_argument("--ttyd", action="store_true",
                    help="终端走 ttyd 旧路（保险丝；默认 serve.py 自己管 PTY）")
    ap.add_argument("--no-hold", action="store_true",
                    help="QD2 M1 fuse: boot a claude per POST like before, "
                         "instead of holding one per question")
    ap.add_argument("--auth-file", metavar="PATH",
                    help="optional username:password file; required for a non-loopback host")
    ap.add_argument("--no-auth", action="store_true",
                    help="disable HTTP Basic Auth; only use on a trusted private network")
    ap.add_argument("--space-name", default="",
                    help="display name for the SPACE Home, e.g. Physician-SPACE")
    ap.add_argument("--public-url", default="",
                    help="reader-facing URL shown by the SPACE Home")
    a = ap.parse_args()
    config = load_server_config(a.root)
    config_dir = server_config_dir(a.root)
    host = (a.host or config.get("JJLUO_BIND_HOST") or
            config.get("JJLUO_TAILSCALE_ADDRESS") or "127.0.0.1").strip()
    port = a.port
    if port is None:
        raw_port = config.get("JJLUO_LOCAL_PORT") or config.get("JJLUO_TAILSCALE_PORT")
        try:
            port = int(raw_port) if raw_port else 5599
        except ValueError:
            ap.error(f"invalid port in {config_dir / 'settings.env'}: {raw_port!r}")
    if a.no_auth:
        auth_file = None
    else:
        auth_arg = a.auth_file or config.get("JJLUO_AUTH_FILE")
        if auth_arg:
            auth_path = Path(auth_arg).expanduser()
            if not auth_path.is_absolute() and not a.auth_file:
                auth_path = Path(a.root).resolve() / auth_path
            auth_file = auth_path.resolve()
        else:
            auth_file = None
    space_name = (a.space_name or config.get("JJLUO_SPACE_NAME") or "").strip()
    public_url = (a.public_url or config.get("JJLUO_PUBLIC_URL") or
                  config.get("JJLUO_TAILSCALE_URL") or "").strip()
    if not host_is_loopback(host) and auth_file is None and not a.no_auth:
        ap.error("--auth-file is required when --host is not loopback")
    try:
        Handler.configure_auth(auth_file)
    except AuthConfigError as exc:
        ap.error(str(exc))
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
    Handler.space_name = space_name
    Handler.public_url = public_url
    base.BIND_HOST = host
    srv = ThreadingHTTPServer((host, port),
                              partial(Handler, directory=str(Handler.root)))
    # A non-loopback --host binds THAT ADDRESS ONLY, which quietly breaks the
    # path most people are actually on: a VS Code / ssh -L forward connects to
    # 127.0.0.1 on THIS machine, so a tailnet-only bind leaves the tunnel
    # pointing at a closed port and the board simply will not open (JL 260726,
    # twice in one evening). Loopback is therefore always ALSO served: it adds
    # no exposure that a local process does not already have, and it means
    # choosing a wider address never costs you the narrow one.
    loop = None
    if not host_is_loopback(host) and host != "0.0.0.0":
        try:
            loop = ThreadingHTTPServer(("127.0.0.1", port),
                                       partial(Handler, directory=str(Handler.root)))
            threading.Thread(target=loop.serve_forever, daemon=True).start()
        except OSError as e:
            print(f"   ⚠️ loopback {port} 没起来：{e}", flush=True)
    tok, src = oauth_token(Handler.root)
    try:
        import claude_agent_sdk  # noqa: F401
        sdk = "on"
    except ImportError:
        sdk = "off（这个 Python 没装 SDK，聊天接口不可用）"
    print(f"📡 http://{host}:{port}  root={Handler.root}\n"
          + ("" if not loop else
             f"   ＋ http://127.0.0.1:{port} 也在听（VS Code / ssh -L 走的是这个）\n")
          + ("" if host_is_loopback(host) else
             f"   ⚠️ 绑的不是 loopback：{host} 能到的设备都能用 /_term/ 开 shell\n")
          + f"   评论 / 状态：直接写在这台机器上\n"
          f"   认证：{('off (--no-auth; Tailscale boundary only)' if a.no_auth else ('on (' + str(len(Handler.auth_users)) + ' accounts)' if Handler.auth_users else 'off (local only)'))}\n"
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
