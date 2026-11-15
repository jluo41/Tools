"""The Studio chat drawer's session side: rejoin a live turn, the session map, names, logs and kept sessions.

Split out of chat.py (2026-11-13); ChatMixin in chat.py inherits ChatSessionsMixin.
"""

import json
import re
import traceback
import threading
import time
from pathlib import Path

from . import turnring
from .base import group_stem
from src.common import studio_lane_dir
from src.naming import compact_name, name_problem
from .chat_transcript import tool_brief, transcript_markdown, digest_markdown, kept_session_dir


class ChatSessionsMixin:
    def attach(self, f, p):
        """POST /_board/attach {file, cursor} → the rest of a live turn.

        The half of R1 a reader actually feels. A drawer that reloaded, was
        navigated away from, or simply came back to the tab asks for everything
        after the cursor it last saw; if nothing is running it gets a plain JSON
        `live:false` and moves on. QD3's terminal has answered this question
        since it was built (`term.py:679` replays the ring on reconnect); chat
        could not answer it at all.
        """
        turn = turnring.get(str(f))
        # `probe` asks the question WITHOUT joining the queue. The chat picker
        # (QD2 C8) needs to say "a turn is still running" before a reader
        # commits to opening anything, and a plain attach would answer that by
        # parking on the ring until the turn ended, which is the opposite of a
        # question. Same endpoint, because it is the same fact.
        if p.get("probe"):
            return {"live": turn is not None and not turn.done,
                    "ended": turn is not None and turn.done,
                    "seq": turn.seq if turn else 0}, None
        if turn is None or turn.done:
            # A FINISHED ring is deliberately not re-streamed, and the browser
            # found out why: the drawer asks on open, on focus and on a 25s
            # heartbeat, so a still-readable finished turn was re-attached and
            # its `done` re-rendered every time — one duplicate answer bubble
            # per heartbeat, for the whole grace window.
            # Once a turn has ended the transcript IS the right source, which is
            # what the 260801 sync already reads. The ring's job is the window
            # the transcript cannot cover: while the turn is still running.
            return {"live": False, "ended": turn is not None}, None
        try:
            cursor = int(p.get("cursor") or 0)
        except (TypeError, ValueError):
            cursor = 0
        self.send_response(200)
        self.send_header("Content-Type", "application/x-ndjson; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Connection", "close")
        self.end_headers()

        def sock_write(obj):
            try:
                self.wfile.write((json.dumps(obj, ensure_ascii=False) + "\n").encode())
                self.wfile.flush()
                return True
            except Exception:
                return False

        turn.drain(cursor, sock_write)
        return "STREAMED", None

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
    # 拣选器从这里列历史。本机状态，放在 SPACE 外：跟这些 session 的 jsonl 同一个目录
    # （~/.claude/projects/<proj>/haipipe-sessions.json）。SPACE 里不再生成 .haipipe-board/（JL 261009）；
    # 旧的 <root>/.haipipe-board/sessions.json 第一次读时搬过来。
    def _sess_map_path(self):
        d = self._jsonl_path("x").parent
        d.mkdir(parents=True, exist_ok=True)
        path = d / "haipipe-sessions.json"
        old = self.root / ".haipipe-board" / "sessions.json"
        if not path.exists() and old.is_file():
            path.write_text(old.read_text(encoding="utf-8"), encoding="utf-8")
        return path

    def _sess_map(self):
        try:
            return json.loads(self._sess_map_path().read_text(encoding="utf-8"))
        except Exception:
            return {}

    _SESSMAP_LOCK = threading.Lock()

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
        # RE-READ AND MERGE UNDER A LOCK, then write once.
        #
        # This was a plain read-modify-write on a file several processes share:
        # one serve.py per board is the normal case, but a checks run, a second
        # window or a stray daemon all write the same `sessions.json`, and the
        # last writer wins with whatever it happened to read minutes earlier.
        # Measured 260802: QD2's list went from three sessions to ONE, so the
        # picker offered nothing to switch to and `＋ New session` looked
        # broken while the .jsonl files were all still on disk.
        with self._SESSMAP_LOCK:
            fresh = self._sess_map()
            for k, v in fresh.items():
                if k == key:
                    continue
                m.setdefault(k, v)
            # keep anything another writer added to OUR key while we worked
            mine = {r["id"] for r in m[key]}
            for r in fresh.get(key, []):
                r = r if isinstance(r, dict) else {"id": r, "name": ""}
                if r["id"] not in mine:
                    m[key].append(r)
            m[key] = m[key][:50]
            try:
                tmp = self._sess_map_path().with_suffix(".json.tmp")
                tmp.write_text(json.dumps(m, indent=1), encoding="utf-8")
                tmp.replace(self._sess_map_path())      # atomic on POSIX
            except Exception:
                traceback.print_exc()   # in the server log, not hidden (code review 261113)
                pass

    def name_session(self, f, p):
        """POST /_board/session-name {file, id, name} → 给某段 session 改名。
        名字住在登记表（板外之物不进 .md 头部：QD1「板上只记结果」）。"""
        sid = (p.get("id") or "").strip()
        name = " ".join((p.get("name") or "").split())
        if not sid:
            return None, "缺 id"
        if name and (problem := name_problem(name, "session name")):
            return None, problem
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
                        return compact_name(t)
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
        out, err = self._session_rows(sid)
        if err:
            return {"ok": False, "err": err}
        # a very long session would blow up the drawer; keep the tail, which is
        # what "continue where I left off" actually means
        MAX = 300          # raised with tool rows: 120 was ~4 real turns
        clipped = len(out) > MAX
        return {"ok": True, "log": out[-MAX:], "clipped": clipped, "total": len(out)}

    def _session_rows(self, sid):
        """The full jsonl walk, unclipped -> (rows, err). session_log clips it
        for the drawer; keep_sessions writes all of it, because a RECORD that
        silently drops the first 300 rows is not a record (QPf4 §1)."""
        jp = self._jsonl_path(sid)

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
                    # A REPLAY SHOULD SHOW THE TOOLS A LIVE TURN SHOWED
                    # (JL 260801: "我重新打开一个过去的 session ... content 和
                    # 界面都非常差"). This used to keep assistant TEXT only, so
                    # a turn that ran ten tools replayed as one bare paragraph
                    # and the live view and the replay disagreed about what had
                    # happened. The .jsonl has the calls; hand them over and let
                    # the drawer draw the same cards it draws live.
                    if kind == "assistant":
                        blocks = (o.get("message") or {}).get("content")
                        for b in (blocks if isinstance(blocks, list) else []):
                            if isinstance(b, dict) and b.get("type") == "tool_use":
                                tin = b.get("input") if isinstance(b.get("input"), dict) else {}
                                out.append({"k": "tool",
                                            "name": b.get("name", "?"),
                                            "t": tool_brief(b.get("name", "?"), tin),
                                            "ts": o.get("timestamp")})
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
                        out.append({"k": "you", "t": txt, "ts": o.get("timestamp")})
                    else:
                        out.append({"k": "ai", "t": txt, "ts": o.get("timestamp")})
        except Exception as e:
            return [], str(e)
        return out, None

    def keep_sessions(self, f, p):
        """POST /_board/chat-keep {file} -> sessions land in studio/chat/.

        BOUNDED on purpose: only sessions the page has registered (the same
        list the picker shows), never every stray conversation, which is the
        bloat the page's own Decision row warned about. The folder name keys
        on the session's FIRST timestamp; a numeric suffix is used only if two
        different sessions began in the same minute. A re-keep recognizes the
        recorded session id and refreshes the same folder. ``digest.md`` is the
        reading path and ``transcript.md`` is the full exchange; the jsonl stays
        the source, so overwriting both is ordinary sync semantics."""
        f = Path(f)
        if f.is_dir() or f.parent.name != f.stem:
            return {"ok": False, "err": "chat/ needs a folded page "
                                        "(<name>/<name>.md, QPf1)"}
        listing, _ = self.sessions_list(f, p)
        kept, skipped = [], 0
        for row in listing.get("sessions", []):
            if not row.get("landed"):
                skipped += 1
                continue
            sid = row["id"]
            rows, err = self._session_rows(sid)
            if err or not rows:
                skipped += 1
                continue
            first_ts = next((r.get("ts") for r in rows if r.get("ts")), "")
            stamp = (first_ts[2:10].replace("-", "") + "-"
                     + first_ts[11:16].replace(":", "")) if first_ts else "undated"
            d = kept_session_dir(studio_lane_dir(f.parent, "chat"), stamp, sid)
            d.mkdir(parents=True, exist_ok=True)
            head = {"id": sid, "name": row.get("name", ""),
                    "title": row.get("title", ""),
                    "kept": time.strftime("%y%m%d %H%M"),
                    "source": str(self._jsonl_path(sid))}
            (d / "transcript.md").write_text(
                transcript_markdown(rows, head), encoding="utf-8")
            (d / "digest.md").write_text(
                digest_markdown(rows, head), encoding="utf-8")
            kept.append(d.name)
        return {"ok": True, "kept": kept, "skipped": skipped}

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
            prefix = group_stem(Path(f).name).split("-")[0]   # 7-QC-engine → QC
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
