"""Read Board update counts from Page outline log records."""

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

from . import base
from .structure import page_id_of
from src.common import page_files




class ActivityMixin:
    # ---- local activity timing (QD8) --------------------------------
    def activity_board(self, payload):
        """Resolve the board from the page already open in the browser."""
        page = unquote(payload.get("path") or "")
        board = (self.root / page.lstrip("/")).resolve().parent
        try:
            rel = board.relative_to(self.root.resolve()).as_posix()
        except ValueError:
            return None, None, "activity path is outside --root"
        if not (board / "board.md").exists():
            return None, None, f"{board} has no board.md"
        return board, rel, None



    @staticmethod
    def log_day_iso(stamp):
        try:
            return dt.date(2000 + int(stamp[:2]), int(stamp[2:4]),
                           int(stamp[4:6])).isoformat()
        except ValueError:
            return None

    @staticmethod
    def log_sources(board):
        """Return ``(Page source, log source, current-record?)`` rows."""
        sources = []
        for page in page_files(board):
            record = page.parent / "outline" / f"{page.stem}-log.md"
            sources.append((page, record if record.is_file() else page,
                            record.is_file()))
        return sources

    def log_counts(self, board):
        """Return Page update counts from current logs, with a legacy fallback."""
        sources = self.log_sources(board)
        stamp = tuple((str(log), log.stat().st_mtime_ns)
                      for _page, log, _current in sources)
        cached = self._log_cache.get(str(board))
        if cached and cached[0] == stamp:
            return cached[1]
        out = {}
        for page, path, current in sources:
            try:
                text = path.read_text(encoding="utf-8")
            except OSError:
                continue
            days, inside = {}, current
            for ln in text.split("\n"):
                if not current and ln.startswith("## "):
                    inside = ln[3:].strip().casefold() == "log"
                    continue
                if not inside:
                    continue
                m = self.LOG_LINE.match(ln.strip())
                if not m:
                    continue
                day = self.log_day_iso(m.group(1))
                if day:
                    days[day] = days.get(day, 0) + 1
            if days:
                out[page_id_of(page.stem)] = {"days": days, "file": page.name}
        self._log_cache[str(board)] = (stamp, out)
        return out

    # what cannot contain a board.md, so the walk never enters it
    SKIP_DIRS = {".git", ".venv", "node_modules", "__pycache__", "_archive",
                 "board", "_WorkSpace", "site-packages", ".pytest_cache",
                 "dist", "build"}
    _boards_cache = (0.0, None)
    _boards_lock = threading.Lock()

    def log_boards(self):
        """Every board under --root, so the across-boards ranking is real.

        PRUNE IN PLACE, AND CACHE THE ANSWER (260802). `rglob` descends
        everywhere and the skip list was applied to the RESULTS, so finding ten
        `board.md` files walked the whole repository: 366,951 entries through
        `.venv`, `node_modules`, `.git`, `_WorkSpace` and the generated `board/`
        tree under every board. `/boards` was fixed this way earlier the same
        day; this copy of the same walk was missed, and it is on a far hotter
        path — every page in every pane posts `op=stats` as it loads.

        What that cost is not "slow": measured here, `POST /_board/activity`
        never returned inside 60 s, so each one held one of the browser's SIX
        connections per origin until it gave up. With a few tabs open every
        socket was held by a walk, and JL's next CLICK sat in Chrome's queue
        showing "Provisional headers are shown" for one to two minutes. The
        page was never slow to serve; it never got a socket to be served on.

        The cache is the second half. Ten tabs loading at once asked ten times
        for an answer that changes when a board is created, which is rarely, so
        one walk is shared for two seconds and the rest are free.
        """
        now = time.monotonic()
        stamp, cached = ActivityMixin._boards_cache
        if cached is not None and now - stamp < 2.0:
            return cached
        with ActivityMixin._boards_lock:
            stamp, cached = ActivityMixin._boards_cache
            if cached is not None and time.monotonic() - stamp < 2.0:
                return cached
            found = []
            for dirpath, dirnames, filenames in os.walk(self.root):
                dirnames[:] = [d for d in dirnames
                               if d not in self.SKIP_DIRS and not d.startswith((".", "_"))]
                if "board.md" not in filenames:
                    continue
                here = Path(dirpath)
                found.append((here.relative_to(self.root).as_posix(), here))
            found.sort()
            ActivityMixin._boards_cache = (time.monotonic(), found)
            return found

    def board_title(self, path):
        try:
            for ln in (path / "board.md").read_text(encoding="utf-8").split("\n"):
                if ln.startswith("# "):
                    return ln[2:].split("——")[0].split(" — ")[0].strip()
        except OSError:
            pass
        return path.name

    def activity_stats(self, current_board):
        """Board activity measured as dated Page log records."""
        today = dt.date.today()
        first = today - dt.timedelta(days=13)
        window = [(first + dt.timedelta(days=i)).isoformat() for i in range(14)]
        recent = set(window)
        week = set(window[-7:])

        boards, per_day, here_day = [], {}, {}
        counts_here = {}
        for rel, path in self.log_boards():
            counts = self.log_counts(path)
            total = sum(sum(v["days"].values()) for v in counts.values())
            if not total:
                continue
            mine = rel == current_board
            if mine:
                counts_here = counts
            span, in_window = set(), 0
            for v in counts.values():
                for day, n in v["days"].items():
                    span.add(day)
                    if day in recent:
                        in_window += n
                        per_day[day] = per_day.get(day, 0) + n
                        if mine:
                            here_day[day] = here_day.get(day, 0) + n
            boards.append({
                "board": rel, "title": self.board_title(path),
                "updates": total, "recent": in_window,
                "days": len(span), "pages": len(counts),
                "last": max(span) if span else "",
            })
        boards.sort(key=lambda b: (-b["updates"], b["board"]))

        days = [{"day": d, "updates": per_day.get(d, 0),
                 "here": here_day.get(d, 0)} for d in window]

        # Group ownership comes from the board's own ## Pages, the same source
        # the index orders by, so a page is filed exactly where a reader
        # already expects to find it.
        from src.parse import parse_dir  # noqa: E402  (heavy, and only needed here)
        groups, titles = {}, {}
        board_dir = self.root / current_board
        try:
            _meta, pages, _warn = parse_dir(board_dir)
            for pg in pages:
                groups[pg["id"]] = pg.get("group") or ""
                titles[pg["id"]] = pg.get("title") or pg["id"]
        except Exception:
            pass

        tree = {}
        for pid, v in counts_here.items():
            total = sum(v["days"].values())
            if not total:
                continue
            g = groups.get(pid) or "Not in ## Pages"
            row = tree.setdefault(g, {"group": g, "updates": 0, "pages": []})
            row["updates"] += total
            row["pages"].append({
                "page": pid, "title": titles.get(pid, v["file"]),
                "updates": total,
                "recent": sum(n for d, n in v["days"].items() if d in recent),
                "last": max(v["days"]),
            })
        for row in tree.values():
            row["pages"].sort(key=lambda x: (-x["updates"], x["page"]))
        group_rows = sorted(tree.values(), key=lambda x: -x["updates"])
        here = next((b for b in boards if b["board"] == current_board), {
            "board": current_board, "title": self.board_title(board_dir),
            "updates": 0, "recent": 0, "days": 0, "pages": 0, "last": "",
        })
        return {
            "ok": True,
            "unit": "updates",
            "days": days,
            "boards": boards,
            "current": {**here, "groups": group_rows},
            "totals": {
                "today": per_day.get(today.isoformat(), 0),
                "week": sum(n for d, n in per_day.items() if d in week),
                "updates": sum(b["updates"] for b in boards),
                "boards": len(boards),
                "pages": sum(b["pages"] for b in boards),
            },
            "source": "dated records in each Page outline log",
        }

    def activity(self, payload):
        """Return read-only update counts for the Board containing the Page."""
        board, brel, err = self.activity_board(payload)
        if err:
            return None, err
        op = (payload.get("op") or "stats").strip().lower()
        if op != "stats":
            return None, f"unknown activity op: {op}"
        return self.activity_stats(brel), None
