#!/usr/bin/env python3
"""Serve read-only Pages and explicit Board workbench workspaces.

    python3 serve.py [--root DIR] [--port PORT]

When --host, --port, --space-name, --public-url, or --auth-file is omitted,
the matching non-secret setting in <root>/.server_config/settings.env is used.
The explicit --public-read flag allows anonymous generated Board pages and
the read-only Page Design and InsightBoard projections while keeping interactive tools
authenticated. Login is off by default on loopback and tailnet (100.64.0.0/10)
hosts; it turns on when --auth-file (or settings AUTH_FILE without NO_AUTH)
names an auth file. A LAN or 0.0.0.0 host still needs --auth-file or --no-auth.
--no-terminal can be combined with no login when only the Page surfaces are needed.

Page prose is read-only. Retired comment, sentence, edit-sentence, card,
resolve, and discuss endpoints return 405, including requests from older tabs.
Copy Page context into an agent conversation to request source changes.
The explicit workbench workspaces keep their own APIs:

    POST /_board/chat      {path, file, message, model, effort}
                                                      -> one turn with claude_agent_sdk
    POST /_board/stop      {path, file}                -> ask that turn to stop
    POST /_board/term      {path, file}                -> start a ttyd for that question
    POST /_board/release   {path, file}                -> hand the session back
    POST /_board/draft     {path, file}                -> live Draft URL (the old
                            /_board/outline address still answers);
                            action=edit-bullet|append-bullet edits Markdown
                            through the bounded Shape editor
    POST /_board/design    {path, file}                -> live Design Folder URL;
    POST /_board/design-act {path, file, action, item, actor, words, ...}
                                                       -> one Design register row, human decision Run
                                                          (commission/adopt), or planned agent Ticket;
                            read-only Plan/Create/Review/Run/Delivery overview
    POST /_board/design-board {path}                   -> live Board-level Design URL (design tasks × folders × items);
    POST /_board/design-board-act {path, action: new-folder | add-tasks, ...}
    GET  /_board/design-bundle?path=<board.md>           -> csv of every design with its state (send the adopted rows)
                                                       -> open a Design Folder for one roster row
    POST /_board/insight-board {path}                  -> live Board-level Insight URL;
                            read-only Scope/Insight/Check/Delivery, one dataset
    GET  /_board/insight-run?board=&task=&call=        -> one task call's results (the run pop-out)
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
    .venv/bin/python plugins/haipipe-toolkit/servers/_host/serve.py --root .
That venv is uv-managed and has no pip — install into it with:
    uv pip install --python .venv/bin/python claude-agent-sdk

`path` is the browser's own location.pathname, so the client never names a file
it isn't already looking at.

Deliberately narrow, because this is a write endpoint:
  · --public-read exposes generated Board pages/assets and the read-only
    `/_board/design` Page Design and `/_board/insight-board` InsightBoard projections anonymously; writes, chat, terminals,
    Home, and other workspace paths stay authenticated.
  · binds 127.0.0.1 unless --host says otherwise. With --no-auth, /_term/ is a
    real shell available to every device that can reach the selected address;
    --no-terminal disables that route and its PTY control endpoints.
    A tailnet address (100.x) keeps that inside the tailnet; 0.0.0.0 hands it
    to the whole local network.
  · the target must sit inside --root, in a folder containing board.md
    · the filename must match a recognized native or mounted Board Page
  · writes are limited to sentence-adjacent comments, one-sentence edits,
    bounded Outline Bullet edits, and the pre-existing narrowly scoped page
    actions below
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

HOST = Path(__file__).resolve().parent  # plugins/haipipe-toolkit/servers/_host
sys.path.insert(0, str(HOST))
from host_paths import bootstrap  # noqa: E402
bootstrap()                                     # the skill grammar (src/) and cli/ helpers
from src.common import QNAME, page_files, q_files, vet_pagepath, vet_qpath  # noqa: E402
from server_config import (configured_domain, domains, load_server_config,  # noqa: E402
                           server_config_dir)
from host_registry import WORKBENCH_ROUTES, route_allowed, static_path_allowed  # noqa: E402

# 正在跑的对话：文件路径 -> 一个「请停下」的旗子。
# POST /_board/stop 把旗子立起来，chat 循环在下一条消息处收工，

# ── QC8: the live layer is the `live` namespace over every server folder ─────
# serve.py is now what build.py became on 260724: a thin CLI plus the routing
# table.  Each area is a mixin; the class below is only their assembly order.
# `live.<module>` resolves into servers/workbench, servers/workbench-*, or a
# sibling workbench's servers/workbench-* (see _host/live/__init__.py).
from live.base import BaseMixin, HOLD, TERMS, RUNS, ASKS, ALWAYS, ASK_SEQ
from live.auth import AuthMixin, AuthConfigError, host_is_loopback
try:
    from live.share import ShareMixin  # --share: emailed-code sign-in, access per Block (b10 s52)
except ModuleNotFoundError as _no_share:  # a toolkit exported without the share door (export/profiles): never shares
    if _no_share.name != "live.share":
        raise

    class ShareMixin:
        share = share_codes = share_user = None

        @classmethod
        def configure_share(cls, root):
            raise ValueError("this toolkit has no share door")
from live.activity import ActivityMixin
from live.home import HomeMixin
from live.write import WriteMixin
from live.chat import ChatMixin
from live import chat as live_chat
from live.term import (TermMixin, kill_all_terms, reap_stale_terms, term_key,
                       spawn_pty, pty_pump, pty_resize, ws_send,
                       labeling_tui_hold)
from live.xcal import XcalMixin
from live.api_proxy import ApiProxyMixin
from live.evidence import EvidenceTabMixin
from live.delivery import DeliveryTabMixin
from live.labeling import LabelingMixin
from live.page_reader import PageReaderMixin
from live.export import ExportMixin
from live.plugview import PlugViewMixin
from live.folderstat import FolderStatMixin
from live.design import DesignMixin
from live.designboard import DesignBoardMixin
from live.taskboard import TaskBoardMixin
from live.workbench_guide import WorkbenchGuideMixin
from live.shared_workbench import SharedWorkbenchMixin
from live.frame_view import FrameMixin
from live.insightboard import InsightBoardMixin
from live.outline import OutlineMixin
from live.paper import PaperWorkbenchMixin
from live.value import ValueMixin
from live.pageruns import PageRunsMixin
from live.runs import RunsTabMixin
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
                ".do": "text/plain", ".yaml": "text/plain", ".yml": "text/plain",
                # code opened from a mind map card's ↗ (JL 261026: "为什么这个 py file 打不开了"): `text/x-python`
                # makes Chrome download it; as plain text it shows in the pop-out
                ".py": "text/plain", ".sh": "text/plain", ".r": "text/plain", ".sql": "text/plain", ".toml": "text/plain"}

# Textual payloads that `mimetypes` does not label `text/*`, and so would be
# served with no charset. See `guess_type` for the failure that made this list.
_UTF8_TYPES = {"application/javascript", "application/json", "application/xml",
               "image/svg+xml"}


# Old page-view addresses live in serve_routes.py; re-exported here for callers of serve.
from serve_routes import PAGE_VIEW_ROUTES, new_route_name  # noqa: E402,F401
from serve_post import PostMixin  # noqa: E402
from slow_watch import SlowWatchMixin  # noqa: E402

STAMP_KEEP = 10.0                        # seconds a Draft folder's newest-change stamp is reused across tabs
_STAMPS: dict = {}                       # folder -> (time, stamp)
from serve_cli import daemonize, main  # noqa: E402,F401


class Handler(SlowWatchMixin, PostMixin, ShareMixin, AuthMixin, BaseMixin, ActivityMixin, HomeMixin, WriteMixin, ChatMixin, TermMixin, XcalMixin, ApiProxyMixin, PageReaderMixin, ExportMixin, PlugViewMixin, FolderStatMixin, InsightBoardMixin, DesignMixin, DesignBoardMixin, TaskBoardMixin, WorkbenchGuideMixin, SharedWorkbenchMixin, FrameMixin, OutlineMixin, PaperWorkbenchMixin, ValueMixin, EvidenceTabMixin, DeliveryTabMixin, LabelingMixin, PageRunsMixin, RunsTabMixin, SimpleHTTPRequestHandler):
    root = Path(".")
    space_name = ""
    public_url = ""
    terminal_enabled = True
    only = frozenset()          # `--only labeling`: workbenches this host serves; empty = all
    TERMINAL_BOARD_PATHS = frozenset({
        "/_board/terms", "/_board/killall", "/_board/term-type",
        "/_board/local-cmd", "/_board/term-probe", "/_board/term",
        "/_board/release",
    })
    # Current log records are ``### YYMMDD HHMM · ...`` under ``draft/records/``.
    # The optional list-marker form keeps historical Page-level logs readable.
    LOG_LINE = re.compile(r"^(?:#{3,4}\s+|[-*]?\s*)(\d{6})(?:\s+\d{3,4})?\s*·")
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
    EXCAL_ICONS = ("/favicon", "/apple-touch-icon.png")
    # An image pasted into a scene is a base64 dataURL, and Excalidraw keeps it
    # INSIDE the file. One screenshot is megabytes of base64 that git then
    # re-diffs on every stroke, so here the bytes go to a sidecar folder beside
    # the scene and the scene keeps a pointer (JL 260726: "we can have an
    # assets folder for it"). The server rehydrates on the way out, so the
    # editor still receives the dataURL it expects and never knows.
    XMIME = {"image/png": ".png", "image/jpeg": ".jpg", "image/jpg": ".jpg",
             "image/svg+xml": ".svg", "image/gif": ".gif", "image/webp": ".webp"}

    def is_terminal_request(self):
        path = self.path.split("?", 1)[0]
        return (path == "/_term" or path.startswith("/_term/") or
                path in self.TERMINAL_BOARD_PATHS)

    def reject_disabled_terminal(self):
        if not self.terminal_enabled and self.is_terminal_request():
            self.send_error(404, "terminal disabled")
            return True
        return False

    def reject_outside_only(self):
        """404 for anything a `--only <workbench>` host does not serve."""
        if self.only and not route_allowed(self.path, self.only):
            self.send_error(404, "not served by this host (--only %s)" % ",".join(sorted(self.only)))
            return True
        return False

    def reject_private_static(self, *, fallback=False):
        """Reject direct file reads that would bypass a Workbench's custody checks."""
        path = self.path.split("?", 1)[0]
        if not fallback and path.startswith(("/_", "/w/", "/b/")):
            return False
        if not static_path_allowed(self.root, Path(self.translate_path(self.path))):
            self.send_error(404, "not found")
            return True
        return False

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

    def redirect_moved_block(self):
        """An old address of a Block that moved into a Project (JL 261028: Tools' examples/bNN_* now live at
        examples/Project-<X>/work/bNN_*): send it to the new place, so old links and bookmarks still open.
        Only when the old path is gone and exactly one `<folder>/*/work/bNN_*` matches it. Also (JL 261127) Tools'
        old `blueprints/` folder is `examples/`, and the theme Blocks left `work/` for `blueprint/`: an old address
        lands on the new folder, or on the one Block of that number under `examples/<Project>/<theme folder>/`."""
        import re as _re
        parts = urllib.parse.urlsplit(self.path)
        root = Path(self.root)

        def moved(rel):
            rel = rel.strip("/")
            if (root / rel).exists():
                return None
            renamed = _re.sub(r"(^|/)blueprints(?=/|$)", r"\1examples", rel)
            if renamed != rel and (root / renamed).exists():
                return renamed
            rel = renamed
            m = _re.match(r"^(.*?)(?:^|/)(b\d{2}_[^/]+)(/.*)?$", rel)
            if not m:
                return None
            head, block, tail = m.group(1), m.group(2), m.group(3) or ""
            base = root / head if head else root
            hits = [h for h in base.glob(f"*/work/{block}") if h.is_dir()] \
                or [h for h in root.glob(f"examples/*/*/{block}") if h.is_dir()]
            return (hits[0].relative_to(root).as_posix() + tail) if len(hits) == 1 else None

        new_path = moved(urllib.parse.unquote(parts.path)) if not parts.path.startswith("/_") else None
        query, changed = [], False
        for k, v in urllib.parse.parse_qsl(parts.query, keep_blank_values=True):
            if k == "path" and (n := moved(v)):
                v, changed = n, True
            query.append((k, v))
        if not new_path and not changed:
            return False
        target = urllib.parse.urlunsplit(("", "", "/" + urllib.parse.quote(new_path) if new_path else parts.path,
                                          urllib.parse.urlencode(query, safe="/"), parts.fragment))
        self.send_response(301)
        self.send_header("Location", target)
        self.send_header("Content-Length", "0")
        self.end_headers()
        return True

    def float_view(self):
        """GET /_board/float?path=<a unit's float.pdf or preview.pdf>: its page 1 as PNG, the typeset float a display
        box shows (src/float_image.py; must-check M-D18), from a cache outside the paper folder. Only such a PDF inside
        the root; when it cannot be rasterized, the unit's preview.png or assets/figure.png."""
        from urllib.parse import parse_qs, urlsplit
        from src.float_image import NAMES, float_png
        rel = (parse_qs(urlsplit(self.path).query).get("path") or [""])[0].strip("/")
        root = Path(self.root).resolve()
        pdf = (root / rel).resolve()
        if not (rel and pdf.name in NAMES and root in pdf.parents and static_path_allowed(root, pdf) and pdf.is_file()):
            return self.send_error(404, "not found")
        png = float_png(pdf) or next((x for x in (pdf.parent / "preview.png", pdf.parent / "assets" / "figure.png")
                                      if x.is_file()), None)
        if not png:
            return self.send_error(404, "not found")
        body = png.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "image/png")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def draft_stamp_view(self):
        from urllib.parse import parse_qs, urlsplit
        rel = (parse_qs(urlsplit(self.path).query).get("path") or [""])[0].strip("/")
        newest = 0.0
        hit = _STAMPS.get((str(self.root), rel))          # every open tab of a Draft polls this every few seconds:
        if hit and time.monotonic() - hit[0] < STAMP_KEEP:  # tabs on one page share one walk, looked up before any
            newest = hit[1]                               # path is resolved
        elif rel and (folder := (Path(self.root).resolve() / rel).resolve()).is_dir() \
                and Path(self.root).resolve() in folder.parents:
            # results/ and data/ hold run output a Draft page never shows; walking them on every poll hung a host
            skip = {"runs", "delivery", "_archive", "__pycache__", "workflow", "previous", "results", "data",
                    "node_modules"}
            for dirpath, dirs, files in os.walk(folder):
                dirs[:] = [d for d in dirs if d not in skip and not d.startswith(".")]
                for f in files:
                    if f.endswith((".md", ".yaml", ".yml", ".csv", ".bib")):
                        try:
                            newest = max(newest, os.stat(os.path.join(dirpath, f)).st_mtime)
                        except OSError:
                            pass
            _STAMPS[(str(self.root), rel)] = (time.monotonic(), newest)
        body = json.dumps({"stamp": newest}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self.path = new_route_name(self.path)
        if not self.require_request_auth():
            return
        if self.redirect_moved_block():
            return
        if self.reject_disabled_terminal():
            return
        if self.reject_outside_only():
            return
        if self.is_api_request():                # the normalizer APIs and their try pages, behind this login
            return self.proxy_api()
        if self.is_home_request():
            return self.serve_home()
        short = self.short_request()
        if short:
            return self.serve_short(*short)
        workbench = self.workbench_request()
        if workbench:
            return self.serve_workbench(*workbench)
        if self.path.split("?", 1)[0] == "/workbench/labeling":
            return self.labeling_page_view()
        if self.reject_private_static():
            return
        if self.path.split("?", 1)[0] == "/_board/page":
            # 📖 one Page, live, in the Page engine's reader (the retired site's replacement)
            return self.page_reader_view()
        if self.path.split("?", 1)[0] == "/_board/paper-board":
            # 📄 Board-level Paper Workbench, rendered live from the paper board
            return self.paper_view()
        if self.path.split("?", 1)[0] == "/_board/run-result":
            # 📄 one Task run's results, the Paper Workbench's pop-out (JL 260930)
            return self.run_result_view()
        if self.path.split("?", 1)[0] == "/_board/design":
            # 🎨 one live projection over the selected Design Page-Folder
            return self.design_view()
        if self.path.split("?", 1)[0] == "/_board/design-board":
            # 🎨 the same workbench one grain up: the Brief's design tasks × folders × items
            return self.design_board_view()
        if self.path.split("?", 1)[0] == "/_board/work-board":
            return self.task_board_view()
        if self.path.split("?", 1)[0] == "/_board/guide":
            return self.guide_view()
        if self.path.split("?", 1)[0] == "/_board/shared":
            return self.shared_view()
        if self.path.split("?", 1)[0] == "/_board/workbench":
            # 🧭 the base frame: Guide · Block · Job ▾ · Task ▾ × the six Spaces, in the folder's theme
            return self.workbench_frame_view()
        if self.path.split("?", 1)[0] == "/_board/design-bundle":
            # 🎨 every design on the board with its state, as one csv; the send system takes the adopted rows
            return self.design_bundle_view()
        if self.path.split("?", 1)[0] == "/_board/insight-board":
            # 🔎 one live projection over the whole InsightBoard
            return self.insight_board_view()
        if self.path.split("?", 1)[0] == "/_board/insight":
            # 🔎 one page of an InsightBoard as a document, the workbench's pop-out
            return self.insight_page_view()
        if self.path.split("?", 1)[0] == "/_board/insight-run":
            # 🔎 one task call's results, the Insight workbench's run pop-out
            return self.insight_run_view()
        if self.path.split("?", 1)[0] == "/_board/labeling/sample":
            # 🏷 an items Task's Draw again: random rows or items, read live (b15 s41-D12)
            return self.labeling_sample_view()
        if self.path.split("?", 1)[0].startswith("/_board/labeling/form/"):
            # 🏷 a meaning Task's interaction form: a static GET never reads a labeling folder (b15 s58)
            return self.labeling_form_view()
        if self.path.split("?", 1)[0] == "/_board/labeling-board":
            # 🏷 every labeling job on this Board; click one to zoom in
            return self.labeling_board_view()
        if self.path.split("?", 1)[0] == "/_board/labeling":
            # 🏷 four Spaces over one labeling/ lane
            return self.labeling_view()
        if self.path.split("?", 1)[0] == "/_board/float":
            return self.float_view()          # 🖼 a display's typeset float, page 1 as PNG
        if self.path.split("?", 1)[0] == "/_board/draft-stamp":
            # 🔄 the newest change time of one page folder's text and records, so an open page reloads itself when an
            # agent or another tab writes (JL 261114: "How to make the UI to be auto refreshed to show the changes?")
            return self.draft_stamp_view()
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
        if self.path.startswith(self.EXCAL_ICONS) and "/_excalidraw" not in (self.headers.get("Referer") or ""):
            # A workbench page has no icon of its own: the browser's default, not Excalidraw's mark
            # (JL 261003: "just the default one"). Only the Excalidraw app still gets its icons. A page head that
            # names no icon still makes the browser ask: an empty 204, never a 404 in the console (round 2 review).
            self.send_response(204)
            self.send_header("Content-Length", "0")
            self.send_header("Cache-Control", "max-age=86400")
            self.end_headers()
            return
        if self.path.startswith(self.EXCAL_PATHS):
            return self.proxy_excalidraw()
        # Last stop before the static handler: send the text compressed if the
        # browser asked for that (QD5 C2 P5). Falls through untouched otherwise.
        if self.reject_private_static(fallback=True):
            return
        if self.try_range():                     # a video asking for part of itself (live/base.py)
            return
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
        self.path = new_route_name(self.path, "HEAD")
        if not self.require_request_auth():
            return
        if self.redirect_moved_block():
            return
        if self.reject_disabled_terminal():
            return
        if self.reject_outside_only():
            return
        if self.is_home_request():
            return self.serve_home()
        short = self.short_request()
        if short:
            return self.serve_short(*short)
        workbench = self.workbench_request()
        if workbench:
            return self.serve_workbench(*workbench)
        if self.path.split("?", 1)[0] == "/workbench/labeling":
            return self.labeling_page_view(head_only=True)
        if self.reject_private_static():
            return
        if self.path.split("?", 1)[0] == "/_board/page":
            return self.page_reader_view(head_only=True)
        if self.path.split("?", 1)[0] == "/_board/paper-board":
            return self.paper_view(head_only=True)
        if self.path.split("?", 1)[0] == "/_board/run-result":
            return self.run_result_view(head_only=True)
        if self.path.split("?", 1)[0] == "/_board/design":
            return self.design_view(head_only=True)
        if self.path.split("?", 1)[0] == "/_board/design-board":
            return self.design_board_view(head_only=True)
        if self.path.split("?", 1)[0] == "/_board/work-board":
            return self.task_board_view(head_only=True)
        if self.path.split("?", 1)[0] == "/_board/guide":
            return self.guide_view(head_only=True)
        if self.path.split("?", 1)[0] == "/_board/shared":
            return self.shared_view(head_only=True)
        if self.path.split("?", 1)[0] == "/_board/workbench":
            return self.workbench_frame_view(head_only=True)
        if self.path.split("?", 1)[0] == "/_excalidraw/_hai-xcal.js":
            return self.proxy_excalidraw(head_only=True)
        if self.path.split("?", 1)[0] == "/_board/design-bundle":
            return self.design_bundle_view(head_only=True)
        if self.path.split("?", 1)[0] == "/_board/insight-board":
            return self.insight_board_view(head_only=True)
        if self.path.split("?", 1)[0] == "/_board/insight":
            return self.insight_page_view(head_only=True)
        if self.path.split("?", 1)[0] == "/_board/insight-run":
            return self.insight_run_view(head_only=True)
        if self.path.split("?", 1)[0] == "/_board/labeling/sample":
            return self.labeling_sample_view(head_only=True)
        if self.path.split("?", 1)[0].startswith("/_board/labeling/form/"):
            return self.labeling_form_view(head_only=True)
        if self.path.split("?", 1)[0] == "/_board/labeling-board":
            return self.labeling_board_view(head_only=True)
        if self.path.split("?", 1)[0] == "/_board/labeling":
            return self.labeling_view(head_only=True)
        if self.path.startswith("/_term/"):
            if self._term_route():
                return
            return self.proxy_term()
        if self.reject_private_static(fallback=True):
            return
        return SimpleHTTPRequestHandler.do_HEAD(self)


if __name__ == "__main__":
    main(Handler)
