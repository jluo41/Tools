"""QC8 · the terminal (QD3): PTY, ring buffer, the /_term WebSocket terminus.

Moved out of serve.py on 2026-07-31 under the gate_live.py response-identical gate.
QC3's Law: a refactor moves code, features never ride along.

Split by responsibility on 2026-11-13, behaviour unchanged:
  term_pty.py  the process layer (spawn, pump, park sweep, reap, kill-all)
  term_ws.py   the wire layer (ttyd proxy, the own-PTY WebSocket terminus)
  term.py      TermMixin: one session per window, open, park, probe, list, kill
This module re-exports every name that used to live here.
"""

import os
import re
import subprocess
import threading
import time
from pathlib import Path

from . import base as _base
from .base import HERE, HOLD, RING_CAP, TERMS, TERM_DIR, group_stem

_VENDOR_XTERM = Path(__file__).resolve().parents[1] / "assets" / "vendor" / "xterm"
from .chat import chat_guard, prime_context
from .term_pty import (DYING, PARK_GRACE, _SWEEP, _sweep_parked,  # noqa: F401 (re-exported)
                       ensure_sweeper, kill_all_terms, labeling_tui_hold,
                       pty_pump, pty_resize, reap_stale_terms, spawn_pty,
                       term_key, terms_for, wait_dying, ws_send)
from .term_ws import TermWireMixin


class TermMixin(TermWireMixin):
    # ---- LAW: 一个 session 一个窗口 ---------------------------------
    def hold(self, f, who):
        cur = HOLD.get(str(f))
        # A HOLD outlives the thing that took it: a terminal that was reaped,
        # crashed, or lost its page leaves "the terminal owns this session"
        # standing forever, and every later chat turn on that page is refused.
        # The drawer then showed nothing useful, so it read as a dead drawer
        # rather than as a lock (JL 260731, hit repeatedly). If the holder is a
        # terminal and no live terminal exists for this file, the claim is void.
        if cur and cur[0] == "terminal" and who != "terminal":
            t = TERMS.get(term_key(f))
            if not t or not self.alive(t["pid"]):
                HOLD.pop(str(f), None)
                cur = None
        if cur and cur[0] != who:
            return f"这一题的 session 正被{'终端' if cur[0]=='terminal' else '网页抽屉'}占着。" \
                   f"先把那边关掉（终端那边点『交回 session』）再开这个。"
        if who == "drawer":
            # 抽屉要在这段 jsonl 上开 SDK 会话：停靠中的 PTY（没有窗口，但进程活着）
            # 必须先死 —— 一份 jsonl 同时只许一个进程写（QD1 的 Law）。
            t = TERMS.get(term_key(f))
            if t and t.get("parked"):
                self.kill_term(f)
        HOLD[str(f)] = (who, None)
        return None

    def term_type(self, f, p):
        """POST /_board/term-type {file, session, text} -> type into THIS page's PTY.

        `local_cmd` above explains why the server cannot start a program on the
        reader's machine. This is the other half, and it is the half that was
        missing: the terminal this page already owns runs HERE, on the server, and
        writing to its master fd is exactly what a keystroke does. So a button can
        run a command after all, as long as the command goes where the person's own
        terminal already is rather than where their screen is (JL 260808).

        It opens no new exposure: `/_term/<key>/` already carries this same PTY over
        a websocket on this same listener. What it adds is a named door for one line
        of text, so a surface does not have to speak the terminal's wire protocol.
        """
        reason = labeling_tui_hold(f)
        if reason:
            return None, reason + " · TUI is read-only at this gate"
        sid = (p.get("session") or "").strip()
        key = term_key(f, sid) if sid else term_key(f)
        cur = TERMS.get(key)
        if not cur or not self.alive(cur["pid"]):
            return None, "这一页还没有终端：先从 🔌 Workbench 开一次 TUI Chat。"
        if cur.get("kind") != "pty" or cur.get("fd") is None:
            return None, "这个终端不是自有 PTY，暂时只能复制命令。"
        text = (p.get("text") or "").strip()
        if not text:
            return None, "没有要输入的命令。"
        if "\n" in text or "\r" in text:
            return None, "一次只送一行：多行命令请在终端里自己敲。"
        try:
            os.write(cur["fd"], (text + "\r").encode("utf-8"))
        except Exception as e:
            return None, f"写不进终端：{e}"
        return {"ok": True, "key": key, "sent": text}, None

    def local_cmd(self, f, p):
        """POST /_board/local-cmd {path, file, session} -> the commands that put
        THIS session in a terminal, wherever the reader actually is.

        JL 260801 asked for a button that opens a terminal on their own machine.
        The first attempt had the server run `osascript`, which is wrong twice
        over, and the second reason only became clear when JL said "我是 SSH 到
        你这个桌面上的，我是在另外一台电脑上":

          · a GUI window opened by this server appears on THIS Mac's screen,
            which is not the screen the reader is sitting at;
          · and it cannot even do that: from an SSH session there is no Aqua
            session to talk to, and the call BLOCKS rather than failing, which
            would have tied up a server thread on every click.

        A browser cannot start a program on the machine that is merely viewing a
        page, and no amount of server-side effort changes that. What the server
        CAN do is know exactly which command lands in this session, including
        the ssh hop back to itself, so one paste in any terminal on any machine
        gets there. That is the honest primitive; the copy button is the door.
        """
        reason = labeling_tui_hold(f)
        if reason:
            return None, reason + " · TUI is read-only at this gate"
        import getpass
        import shlex
        import socket

        sid = (p.get("session") or "").strip() or self.session_of(f)
        if not sid:
            return None, "这一题还没有 session：先说一句话，或者开一次终端。"
        root = str(Path(self.root).resolve())
        here = f"cd {shlex.quote(root)} && claude --resume {shlex.quote(sid)}"

        # the address this server is reachable on, so the ssh line is copy-ready
        host = _base.BIND_HOST or ""
        if host in ("", "0.0.0.0", "127.0.0.1", "localhost"):
            try:
                host = socket.gethostname()
            except Exception:
                host = "localhost"
        user = getpass.getuser()
        remote = f"ssh -t {user}@{host} {shlex.quote(here)}"
        return {"session": sid, "here": here, "remote": remote,
                "host": host, "user": user}, None

    def term_probe(self, f):
        """POST /_board/term-probe {path, file} -> is THIS target's PTY still there?

        The client used to answer this itself by matching `/_board/terms`
        basenames, which is wrong for a group or board terminal: those register
        under a FOLDER (`QD-working`) while the drawer's `cq.file` is
        `board.md`, so the names never matched and a reload silently decided no
        terminal existed (JL 260801, reported twice). `term_key` is the only
        thing that knows the real identity, so ask it here.

        A PARKED terminal counts as there: parking is what a reload does, and
        the whole point is to come back to it.
        """
        reason = labeling_tui_hold(f)
        if reason:
            return {"live": False, "terminals": [], "blocked": reason}, None
        live = [(k, x) for k, x in terms_for(f) if self.alive(x["pid"])]
        if not live:
            return {"live": False, "terminals": []}, None
        def winsize(x):
            """The PTY's ACTUAL window size, read back from the kernel.

            The browser's grid and this number MUST be equal. When they drift,
            the app wraps at one width while xterm lays out at another and every
            redraw lands in the wrong cells, which is the shredded screen JL
            sent on 260801. Reporting it here makes that a number a test can
            assert instead of a screenshot someone has to judge.
            """
            try:
                import fcntl
                import struct as _st
                import termios
                buf = fcntl.ioctl(x["fd"], termios.TIOCGWINSZ, b"\0" * 8)
                rows, cols = _st.unpack("HHHH", buf)[:2]
                return {"cols": cols, "rows": rows}
            except Exception:
                return None

        k0, t0 = live[0]
        return {"live": True, "parked": bool(t0.get("parked")), "key": k0,
                "winsize": winsize(t0),
                "terminals": [{"key": k, "session": x["sid"],
                               "name": x.get("name") or "",
                               "parked": bool(x.get("parked")),
                               "born": x.get("born", 0)} for k, x in live]}, None

    def park(self, f):
        """宽限停靠：进程和 pump 不动，收掉 WS 窗口、放 HOLD、记 deadline。
        宽限内 POST /_board/term 秒接同一个进程；过了 deadline 清扫线程真杀。"""
        key = term_key(f)
        t = TERMS.get(key)
        if not (t and t.get("kind") == "pty" and self.alive(t["pid"])):
            return {"parked": False}, None
        with t["lock"]:
            clients = list(t["clients"])
            t["clients"].clear()
        for c in clients:
            try:
                ws_send(c, b"", op=8)
                c["conn"].close()
            except Exception:
                pass
        t["parked"] = time.time() + PARK_GRACE
        self.release(f, "terminal")
        ensure_sweeper()
        return {"parked": True, "grace": PARK_GRACE}, None

    def release(self, f, who=None):
        cur = HOLD.get(str(f))
        if cur and (who is None or cur[0] == who):
            HOLD.pop(str(f), None)

    # ---- 终端：给这一题起一个 claude PTY（默认自有；--ttyd 走旧路）----
    def terminal(self, f, p, board):
        import shutil
        import time
        reason = labeling_tui_hold(f)
        if reason:
            return None, reason + " · TUI is read-only at this gate"
        # QD1's Law is one window per session. A held chat client (QD2 M1) owns
        # the same .jsonl, so it must let go before the PTY opens on it.
        try:
            from .chat import HOST as _CHAT_HOST
            if _CHAT_HOST is not None:
                _CHAT_HOST.evict(str(f))
        except Exception:
            pass
        # Resolve WHICH session this terminal is for before keying on it, so a
        # page can hold several at once and asking for another no longer kills
        # the one you are using (JL 260801).
        want = (p.get("session") or "").strip()
        if want and want != "new":
            target_sid = want
        elif want == "new":
            target_sid = ""                      # a fresh id is minted below
        else:
            target_sid = self.session_of(f) or ""
        key = term_key(f, target_sid) if target_sid else term_key(f)
        cur = TERMS.get(key)
        if cur and self.alive(cur["pid"]):
            if False:                            # never kill a sibling terminal
                pass
            else:
                # 复用（含从停靠中接回）：HOLD 要重新拿 —— park 的时候放掉了
                err = self.hold(f, "terminal")
                if err:
                    return None, err
                cur.pop("parked", None)
                return {"url": f"/_term/{key}/", "key": key,
                        "session": cur["sid"], "reused": True}, None
        err = self.hold(f, "terminal")
        if err:
            return None, err
        sid = self.session_of(f)
        if want == "new":
            sid = None                          # 走下面「铸新 id」的分支
        elif want and self.session_landed(want):
            sid = want                          # 选中的历史 → resume 它
        # 一题一个 current session（QD1 的 Law）。用 --resume 还是 --session-id，
        # 看**磁盘上有没有那段对话**，不是光看头部有没有 id：
        #   有 id 且 jsonl 存在  → --resume（接着聊）
        #   有 id 但 jsonl 没有  → 空壳，--resume 会秒退；改用 --session-id 新起
        #   没 id               → 生成一个、写回头部、--session-id
        import uuid
        use_resume = bool(sid) and self.session_landed(sid)
        if not sid:
            sid = str(uuid.uuid4())
        # The key was provisional while the session was still unknown (a "new"
        # request has no id until here). Re-key on the real session, or a second
        # terminal would land on the first one's key and take its place.
        key = term_key(f, sid)
        base = f"/_term/{key}"
        # 开哪段，哪段就是 current（修正后的 Law）：头部跟着换，旧的进登记表
        if sid != self.session_of(f):
            self.remember_session(f, sid, name=p.get("name"))
        else:
            self.record_session(f, sid)
        # 开场定位：--append-system-prompt 把「你在哪块板哪一题」灌进系统提示，
        # 不占一个回合、不让它自动跑，用户一开终端 claude 就已经知道自己在干嘛。
        prime = prime_context(f, board, self.root)
        if Path(f).is_dir():                     # 组级终端（JL 260731）：目录没有 # 标题
            ttl = (group_stem(f.name).split("-")[0] + " · " + f.name)[:60]
        else:
            m = re.match(r"(Q[A-Za-z0-9]+)", f.name)
            tm = re.search(r"^#\s+(.*)$", f.read_text(encoding="utf-8", errors="ignore"), re.M)
            ttl = ((m.group(1) if m else f.stem) + " · " + (tm.group(1).strip() if tm else f.name))[:60]
        note = "" if use_resume else "这一题的新 session，已经记进文件头部了"
        base = f"/_term/{key}"
        claude_cmd = ["claude", "--append-system-prompt", prime,
                      "--resume" if use_resume else "--session-id", sid]
        TERM_DIR.mkdir(parents=True, exist_ok=True)

        # base.USE_TTYD 而不是 from .base import USE_TTYD：serve.py 的 main 在
        # 运行时才写 base.USE_TTYD = a.ttyd，按名字导入会把默认值冻死、--ttyd 失灵；
        # 裸名 USE_TTYD 则直接 NameError；terminal() 里的局部变量 base（/_term 子路径）又会遮住模块名，所以别名 _base（260731 拆分后第一个终端就是这么崩的）。
        wait_dying(key)                     # 旧进程没死透就 resume 同一段，会秒退
        if not _base.USE_TTYD:
            # 自有 PTY（QD3m §8）：serve.py 自己 openpty + spawn，WS 在 ws_term 终结。
            # cwd 是整个 repo（SPACE）—— 终端里的 claude 要能碰到它讨论的代码。
            if not shutil.which("claude"):
                self.release(f, "terminal")
                return None, "这台机器上找不到 claude CLI"
            try:
                proc, master = spawn_pty(claude_cmd, str(self.root))
            except Exception as e:
                self.release(f, "terminal")
                return None, f"起不来 PTY：{e}"
            (TERM_DIR / f"{key}.pid").write_text(str(proc.pid))
            TERMS[key] = {"kind": "pty", "pid": proc.pid, "sid": sid, "fd": master,
                          "ring": bytearray(), "clients": [], "lock": threading.Lock(),
                          "file": str(Path(f).resolve()), "board": str(board), "ttl": ttl,
                          "born": time.time(), "name": (p.get("name") or "")}
            threading.Thread(target=pty_pump, args=(key,), daemon=True).start()
            return {"url": base + "/", "key": key, "session": sid,
                    "reused": False, "note": note}, None

        # ttyd 后备（--ttyd）：unix socket + 反代，QD3 的旧路，验收期的保险丝。
        exe = shutil.which("ttyd")
        if not exe:
            self.release(f, "terminal")
            return None, "这台机器上没有 ttyd（brew install ttyd）"
        sock = str(TERM_DIR / f"{key}.sock")
        try:
            os.unlink(sock)                    # 清掉可能残留的旧 socket
        except OSError:
            pass
        cmd = [exe, "-i", sock, "-W", "-b", base,
               "-t", "titleFixed=" + ttl, "-t", "fontSize=13"] + claude_cmd
        try:
            proc = subprocess.Popen(cmd, cwd=str(self.root),
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            self.release(f, "terminal")
            return None, f"起不来 ttyd：{e}"
        for _ in range(50):                    # 等 socket 文件出现（最多 ~1s）
            if os.path.exists(sock):
                break
            time.sleep(0.02)
        TERMS[key] = {"kind": "ttyd", "pid": proc.pid, "sid": sid, "sock": sock,
                      "file": str(Path(f).resolve()), "board": str(board)}
        return {"url": base + "/", "key": key, "session": sid, "reused": False,
                "note": note}, None

    @staticmethod
    def alive(pid):
        try:
            os.kill(pid, 0)
            return True
        except Exception:
            return False

    def kill_term(self, f):
        key = term_key(f)
        cur = TERMS.pop(key, None)
        if cur:
            if self.alive(cur["pid"]):
                DYING[key] = cur["pid"]
                try:
                    os.kill(cur["pid"], 15)
                except Exception:
                    pass
            if cur.get("kind") == "pty":
                # fd/客户端连接留给 pty_pump 收（唯一关闭者）；这儿只清 pidfile。
                try:
                    os.unlink(TERM_DIR / f"{key}.pid")
                except OSError:
                    pass
            else:
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
                        "path": str(t["file"]),          # to match a page exactly
                        "name": t.get("name") or "",
                        "born": t.get("born", 0),
                        "parked": bool(t.get("parked")),
                        "board": Path(t["board"]).name,
                        "url": f"/_term/{key}/"})
        return out

    def serve_asset(self):
        """serve vendored xterm from the studio workbench folder, board-location-independent.
        /_board/asset/xterm.min.js  ·  /_board/asset/xterm.css"""
        name = self.path.rsplit("/", 1)[-1].split("?")[0]
        if name not in ("xterm.min.js", "xterm.css", "addon-unicode11.js"):
            return self.send_error(404)
        p = _VENDOR_XTERM / name
        if not p.exists():
            return self.send_error(404, "asset missing (vendor xterm not installed)")
        data = p.read_bytes()
        ctype = "text/javascript" if name.endswith(".js") else "text/css"
        # xterm.min.js is 477 KB and this route bypasses `try_gzip`, which only
        # covers files that exist under --root; vendored assets do not. So the
        # single largest thing this server hands out was the one thing crossing
        # the forward uncompressed, on every cold open of a chat (QD5 C2 P5,
        # measured 260802 — it gzips better than 3 to 1).
        enc = None
        if len(data) > 1024 and "gzip" in (self.headers.get("Accept-Encoding") or "").lower():
            import gzip as _gzip
            data, enc = _gzip.compress(data, 6), "gzip"
        self.send_response(200)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        if enc:
            self.send_header("Content-Encoding", enc)
            self.send_header("Vary", "Accept-Encoding")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "max-age=86400")
        self.end_headers()
        self.wfile.write(data)
