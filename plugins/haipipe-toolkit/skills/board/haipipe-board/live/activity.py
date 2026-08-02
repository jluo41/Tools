"""QC8 · focus time (QD6): the SQLite span store and its aggregates.

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
from .structure import page_id_of




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

    def activity_conn(self):
        """One short SQLite connection per request keeps ThreadingHTTPServer safe."""
        d = self.root / ".haipipe-board"
        d.mkdir(exist_ok=True)
        db = sqlite3.connect(d / "activity.sqlite3", timeout=10)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA journal_mode=WAL")
        db.execute("""
            CREATE TABLE IF NOT EXISTS activity_spans (
              span_id TEXT PRIMARY KEY,
              board TEXT NOT NULL,
              board_title TEXT NOT NULL,
              group_name TEXT NOT NULL DEFAULT '',
              page TEXT NOT NULL DEFAULT 'board',
              page_title TEXT NOT NULL DEFAULT '',
              actor TEXT NOT NULL DEFAULT '',
              source TEXT NOT NULL DEFAULT 'browser',
              started_at REAL NOT NULL,
              last_seen_at REAL NOT NULL,
              ended_at REAL,
              active_seconds REAL NOT NULL DEFAULT 0,
              changed INTEGER NOT NULL DEFAULT 0,
              change_count INTEGER NOT NULL DEFAULT 0,
              stop_reason TEXT NOT NULL DEFAULT ''
            )
        """)
        columns = {row["name"] for row in db.execute("PRAGMA table_info(activity_spans)")}
        if "stop_reason" not in columns:
            db.execute(
                "ALTER TABLE activity_spans "
                "ADD COLUMN stop_reason TEXT NOT NULL DEFAULT ''"
            )
        db.execute("""
            CREATE TABLE IF NOT EXISTS activity_ticks (
              span_id TEXT NOT NULL,
              day TEXT NOT NULL,
              seconds REAL NOT NULL DEFAULT 0,
              PRIMARY KEY (span_id, day),
              FOREIGN KEY (span_id) REFERENCES activity_spans(span_id)
            )
        """)
        db.execute("CREATE INDEX IF NOT EXISTS activity_board_idx "
                   "ON activity_spans(board, started_at)")
        for row in db.execute("""
            SELECT s.span_id, s.started_at, COALESCE(s.ended_at, s.last_seen_at) AS ended_at,
                   s.active_seconds
            FROM activity_spans AS s
            WHERE s.active_seconds > 0
              AND NOT EXISTS (
                SELECT 1 FROM activity_ticks AS t WHERE t.span_id=s.span_id
              )
        """).fetchall():
            for day, seconds in self.activity_day_parts(
                    row["started_at"], row["ended_at"], row["active_seconds"]):
                db.execute("""
                    INSERT INTO activity_ticks (span_id, day, seconds)
                    VALUES (?, ?, ?)
                    ON CONFLICT(span_id, day)
                    DO UPDATE SET seconds=seconds+excluded.seconds
                """, (row["span_id"], day, seconds))
        db.commit()
        return db

    @staticmethod
    def activity_num(row, key):
        return int(round(float(row[key] or 0)))

    @staticmethod
    def activity_day_parts(started_at, ended_at, seconds):
        """Split counted seconds across local calendar days.

        Heartbeats cap long gaps. In that case the counted interval is the tail
        nearest ``ended_at`` rather than an invented continuous idle interval.
        """
        start = float(started_at or 0)
        end = max(start, float(ended_at or start))
        total = max(0.0, float(seconds or 0))
        if total <= 0:
            return []
        elapsed = end - start
        if elapsed <= 0:
            return [(dt.datetime.fromtimestamp(end).date().isoformat(), total)]
        if total < elapsed:
            start = end - total
            elapsed = total

        parts = []
        cursor = start
        allocated = 0.0
        while cursor < end:
            local = dt.datetime.fromtimestamp(cursor)
            next_day = local.date() + dt.timedelta(days=1)
            midnight = time.mktime(dt.datetime.combine(next_day, dt.time.min).timetuple())
            boundary = min(end, midnight)
            duration = max(0.0, boundary - cursor)
            share = total - allocated if boundary >= end else total * duration / elapsed
            parts.append((local.date().isoformat(), share))
            allocated += share
            cursor = boundary
        return parts

    @staticmethod
    def log_day_iso(stamp):
        try:
            return dt.date(2000 + int(stamp[:2]), int(stamp[2:4]),
                           int(stamp[4:6])).isoformat()
        except ValueError:
            return None

    @staticmethod
    def log_pages(board):
        return [p for p in sorted(board.rglob("*.md"))
                if p.name[:1] in ("Q", "S")
                and not any(x.startswith((".", "_"))
                            for x in p.relative_to(board).parts)]

    def log_counts(self, board):
        """-> {page id: {day: updates}} for one board, from `## Log` only.

        `## Log` is the board's own record of what changed and when, so it is
        already the honest answer to "was there work here". Nothing else is
        read: legacy `## Where we are` also carries dated lines, but those are status
        prose rather than a change record, and counting both would count one
        change twice.
        """
        pages = self.log_pages(board)
        stamp = tuple((str(p), p.stat().st_mtime_ns) for p in pages)
        cached = self._log_cache.get(str(board))
        if cached and cached[0] == stamp:
            return cached[1]
        out = {}
        for path in pages:
            try:
                text = path.read_text(encoding="utf-8")
            except OSError:
                continue
            days, inside = {}, False
            for ln in text.split("\n"):
                if ln.startswith("## "):
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
                out[page_id_of(path.stem)] = {"days": days, "file": path.name}
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

    def activity_stats(self, db, current_board):
        """Board activity measured in UPDATES, counted from every page's `## Log`.

        JL 260726: "I don't care about the time. What I care is about the
        numbers of updates." The timer only ever saw a browser, and most work on
        these boards arrives through Claude Code or an editor, so the thing it
        measured was never the thing that happened. A Log line is written by
        whoever did the work, in whatever tool, and it already carries its date,
        which is why this reads days of history a timer could not have
        recovered: it is a record rather than an observation.

        One update = one dated line in one page's `## Log`.
        """
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
            "source": "dated lines in each page's ## Log",
        }

    def activity(self, payload):
        board, brel, err = self.activity_board(payload)
        if err:
            return None, err
        db = self.activity_conn()
        try:
            op = (payload.get("op") or "stats").strip().lower()
            if op == "stats":
                return self.activity_stats(db, brel), None
            if op not in ("start", "pulse", "stop"):
                return None, f"unknown activity op: {op}"
            span = (payload.get("span") or "").strip()
            if not re.fullmatch(r"[A-Za-z0-9._:-]{8,160}", span):
                return None, "invalid activity span id"
            page = (payload.get("page") or "board").strip()
            if page != "board" and not re.fullmatch(
                    r"(?:Q[A-Za-z0-9]+|S[A-Za-z0-9]+|S-[A-Za-z]+-[A-Za-z0-9]+)",
                    page):
                return None, "invalid activity page id"
            def clean(v, n):
                return re.sub(r"[\x00-\x1f]+", " ", str(v or "")).strip()[:n]
            group = clean(payload.get("group"), 160)
            page_title = clean(payload.get("title"), 200)
            actor = clean(payload.get("actor"), 8).upper()
            if not re.fullmatch(r"[A-Z0-9]{1,8}", actor):
                actor = "JL"
            stop_reason = clean(payload.get("reason"), 24).lower()
            allowed_reasons = {"idle", "hidden", "pagehide", "page-change", "stop"}
            if op == "stop" and stop_reason not in allowed_reasons:
                stop_reason = "stop"
            elif op != "stop":
                stop_reason = ""
            bm = (board / "board.md").read_text(encoding="utf-8", errors="ignore")
            mt = re.search(r"^#\s+(.+)$", bm, re.M)
            board_title = clean(mt.group(1) if mt else board.name, 240)
            received_at = time.time()
            row = db.execute("SELECT * FROM activity_spans WHERE span_id=?", (span,)).fetchone()
            if row is None:
                db.execute("""
                    INSERT INTO activity_spans
                    (span_id,board,board_title,group_name,page,page_title,actor,source,
                     started_at,last_seen_at,ended_at,active_seconds,changed,change_count,
                     stop_reason)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """, (span, brel, board_title, group, page, page_title, actor, "browser",
                      received_at, received_at, received_at if op == "stop" else None, 0,
                      1 if payload.get("changed") else 0,
                      int(bool(payload.get("changed"))), stop_reason))
            else:
                now = received_at
                if op == "stop" and stop_reason == "idle":
                    try:
                        active_until = float(payload.get("active_until"))
                    except (TypeError, ValueError):
                        active_until = received_at
                    if float(row["started_at"]) <= active_until <= received_at + 1:
                        now = max(float(row["last_seen_at"]),
                                  min(received_at, active_until))
                delta = 0
                tick_start = now
                if row["ended_at"] is None and bool(payload.get("active", True)):
                    delta = min(max(now - float(row["last_seen_at"]), 0), 45)
                    tick_start = now - delta
                db.execute("""
                    UPDATE activity_spans
                    SET board_title=?, actor=?,
                        last_seen_at=CASE WHEN ended_at IS NULL THEN ? ELSE last_seen_at END,
                        ended_at=CASE WHEN ?='stop' AND ended_at IS NULL THEN ? ELSE ended_at END,
                        active_seconds=active_seconds+?,
                        changed=CASE WHEN changed=1 OR ? THEN 1 ELSE 0 END,
                        change_count=change_count+?,
                        stop_reason=CASE WHEN ?='stop' THEN ? ELSE stop_reason END
                    WHERE span_id=?
                """, (board_title, actor, now, op, now, delta,
                      1 if payload.get("changed") else 0,
                      int(bool(payload.get("changed"))), op, stop_reason, span))
                for day, seconds in self.activity_day_parts(tick_start, now, delta):
                    db.execute("""
                        INSERT INTO activity_ticks (span_id, day, seconds)
                        VALUES (?, ?, ?)
                        ON CONFLICT(span_id, day)
                        DO UPDATE SET seconds=seconds+excluded.seconds
                    """, (span, day, seconds))
            db.commit()
            return self.activity_stats(db, brel), None
        finally:
            db.close()
