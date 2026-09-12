"""QC8 · shared state, the request floor, and the helpers every mixin calls.

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
import struct
import subprocess
import sys
import threading
import time
import urllib.parse
from pathlib import Path
from urllib.parse import unquote

from http.server import SimpleHTTPRequestHandler

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
from src.common import (QNAME, group_stem, page_files, q_files,  # noqa: E402
                        registered_page_source, vet_pagepath, vet_qpath)


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
#   自有 PTY（默认，QD3m §8）: {"kind":"pty","pid","sid","fd"(master),"ring",
#                               "clients","lock","file","board"}
#   ttyd 后备（--ttyd）      : {"kind":"ttyd","pid","sid","sock","file","board"}
# 用 key 而不是端口：多块板各有各的 QD3，靠路径 hash 天然分开，绝不撞。
TERMS = {}


TERM_DIR = Path(os.environ.get("TMPDIR", "/tmp")) / "haiboard-terms"


USE_TTYD = False
# the address serve.py bound to, so a copy-ready ssh line can name it
BIND_HOST = ""        # the address serve.py bound to (set in main), for copy-ready ssh lines


RING_CAP = 262144       # 每个终端回放缓冲的上限（myrlin 的重连即时回屏）


ASKS = {}           # 请求 id -> {"ev": Event, "ok": bool, "always": bool}


ALWAYS = {}         # <Q 文件绝对路径> -> 这一轮里「总是允许」过的工具名


ASK_SEQ = itertools.count(1)


def esc4re(s):
    return re.escape(s)


def _now_stamp():
    return time.strftime("%y%m%d %H%M")

class BaseMixin:
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
        """Return (source, Board folder or standalone source rebuild target)."""
        raw_path, raw_name = payload.get("path"), payload.get("file")
        if not isinstance(raw_path, str) or not isinstance(raw_name, str):
            return None, "path and file must be strings"
        page = unquote(raw_path.split("?", 1)[0].split("#", 1)[0])
        name = raw_name.strip().replace("\\", "/")
        parts = name.split("/")
        if (not name or any(part in {"", ".", ".."} for part in parts)
                or ":" in name or "\x00" in name or not name.endswith(".md")):
            return None, f"unsafe Page source: {raw_name!r}"
        root = self.root.resolve()
        try:
            location = (root / page.lstrip("/")).resolve()
            location.relative_to(root)
        except (ValueError, OSError, RuntimeError):
            return None, "越出了 --root"
        folder = location if location.is_dir() else location.parent
        ancestors = []
        while folder == root or root in folder.parents:
            ancestors.append(folder)
            if folder == root:
                break
            folder = folder.parent

        def safe_file(candidate, boundary):
            try:
                candidate.resolve().relative_to(boundary)
                return candidate.is_file()
            except (ValueError, OSError, RuntimeError):
                return False

        board = next((p for p in ancestors if safe_file(p / "board.md", root)), None)
        if board is not None:
            source = board / name
            if not safe_file(source, board):
                return None, f"找不到安全的 Page source: {name}"
            if (name == "board.md" or vet_pagepath(name)
                    or registered_page_source(source.parent) == source):
                return source, board
            return None, f"Page source is not registered: {name}"

        for folder in ancestors:
            source = folder / name
            if not safe_file(source, root):
                continue
            manifest = source.parent / "page.toml"
            if manifest.exists() or manifest.is_symlink():
                allowed = registered_page_source(source.parent) == source
            else:
                allowed = source.name == f"{source.parent.name}.md" and source.name != "board.md"
                if allowed:
                    try:
                        allowed = bool(re.search(r"^## (?:🚪 )?Opening\s*$",
                                                 source.read_text(encoding="utf-8"), re.M))
                    except (OSError, UnicodeError):
                        allowed = False
            if allowed:
                return source, source
        return None, f"not a registered or same-stem standalone Page Face: {name}"

    def rebuild(self, board):
        """Build a Board container or one Page, surfacing subprocess failure."""
        target = Path(board).resolve()
        if target.name == "board.md" and target.is_file():
            target = target.parent
        if target.is_dir() and (target / "board.md").is_file():
            cmd = [sys.executable, str(HERE / "cli" / "build.py"), str(target)]
        else:
            page_cli = HERE.parents[1] / "page" / "haipipe-page" / "cli" / "page.py"
            cmd = [sys.executable, str(page_cli), "build", str(target)]
        r = subprocess.run(cmd, capture_output=True, text=True,
                           cwd=str(target if target.is_dir() else target.parent))
        output = "\n".join(part.strip() for part in (r.stdout, r.stderr) if part and part.strip())
        if r.returncode:
            raise RuntimeError(f"build failed (exit {r.returncode}): {output}")
        return output

    # ── the wire (QD5 C2 P5, 260802) ─────────────────────────────────────
    # A board page is 163 KB and 67% of it is the sidebar repeated on every page;
    # the index is 244 KB and the largest page 451 KB. None of it was ever
    # compressed, and the reader is usually on the far end of a VS Code or ssh
    # forward, where bytes are the whole cost — the server itself answers in
    # 2 to 6 ms. Text this repetitive compresses 5 to 7 times, so this is the
    # cheapest large win available and it needs no change to what is built.
    #
    # Deliberately narrow: GET only, text only, and only above 1 KB, because
    # compressing a small file costs more than it saves. HEAD is left to the
    # parent on purpose — the panes poll with HEAD and only read `Last-Modified`
    # from it (QD5 C4 P3), so there is nothing there worth compressing.
    GZ_SUFFIX = (".html", ".css", ".js", ".json", ".svg", ".md", ".txt", ".map")
    _gz_cache = {}

    def try_gzip(self):
        """Serve a static text file compressed. True if it was handled here."""
        if self.command != "GET":
            return False
        if "gzip" not in (self.headers.get("Accept-Encoding") or "").lower():
            return False
        clean = self.path.split("?", 1)[0].split("#", 1)[0]
        if not clean.endswith(self.GZ_SUFFIX):
            return False
        try:
            fs = Path(self.translate_path(self.path))
            st = fs.stat()
        except OSError:
            return False
        if not fs.is_file() or st.st_size < 1024:
            return False
        # REVALIDATION STILL HAS TO WORK. The tree's speed rests on an unchanged
        # page coming back as a 0-byte 304 (see end_headers below), and that is
        # the parent's job, which this path is bypassing — so do it here too.
        ims = self.headers.get("If-Modified-Since")
        if ims and not self.headers.get("If-None-Match"):
            try:
                import email.utils
                when = email.utils.parsedate_to_datetime(ims)
                if when.tzinfo is None:
                    when = when.replace(tzinfo=dt.timezone.utc)
                if int(st.st_mtime) <= int(when.timestamp()):
                    self.send_response(304)
                    self.send_header("Last-Modified", self.date_time_string(st.st_mtime))
                    self.send_header("Vary", "Accept-Encoding")
                    self.end_headers()
                    return True
            except (TypeError, ValueError, OverflowError):
                pass
        key = (str(fs), st.st_mtime_ns, st.st_size)
        body = self._gz_cache.get(key)
        if body is None:
            import gzip as _gzip
            try:
                body = _gzip.compress(fs.read_bytes(), 6)
            except OSError:
                return False
            # A board is rebuilt constantly, so every entry goes stale the
            # moment it is written; keep a handful and drop the lot when full
            # rather than pretend this is a cache with a policy.
            if len(self._gz_cache) > 64:
                self._gz_cache.clear()
            self._gz_cache[key] = body
        self.send_response(200)
        self.send_header("Content-Type", self.guess_type(str(fs)))
        self.send_header("Content-Encoding", "gzip")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Last-Modified", self.date_time_string(st.st_mtime))
        self.send_header("Vary", "Accept-Encoding")
        self.end_headers()
        self.wfile.write(body)
        return True

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

    def end_headers(self):
        # A `.excalidraw` scene is fetched by the Excalidraw app running on ANOTHER
        # origin (the self-hosted one, `#url=http://127.0.0.1:5599/…`), so without
        # this header the editor loads and the drawing silently does not.
        # Scoped to scene files: nothing else here is meant to be read cross-origin.
        if self.path.endswith((".excalidraw", ".excalidraw.svg", ".excalidraw.png")):
            self.send_header("Access-Control-Allow-Origin", "*")
        # A board is REBUILT constantly, and it was served with no Cache-Control
        # at all, which lets a browser apply heuristic caching and hand back a
        # copy from before the last build. That is indistinguishable from "the
        # fix did not work", and it cost a round of exactly that confusion
        # (JL 260726: "why now I cannot open them"). The page is local and
        # cheap; correctness beats a saved kilobyte every time.
        # `no-store` was the sledgehammer for that, and the tree changed the
        # arithmetic (JL 260801: "why does it take a long time to navigate").
        # A board is no longer one file you open once: every click fetches a
        # page, 82% of whose bytes are the sidebar the router then throws away.
        # `no-cache` keeps the guarantee that mattered, because it means
        # REVALIDATE BEFORE USE, not "may be stale": the browser still asks the
        # server on every navigation, and an unchanged page comes back as a
        # 0-byte 304 instead of 136 KB. `no-store` forbade even keeping the copy
        # that makes that possible.
        if self.path.split("?", 1)[0].endswith((".html", ".css", ".js", ".md")):
            self.send_header("Cache-Control", "no-cache, must-revalidate")
        SimpleHTTPRequestHandler.end_headers(self)
