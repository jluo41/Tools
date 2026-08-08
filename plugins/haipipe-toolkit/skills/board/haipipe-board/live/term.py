"""QC8 · the terminal (QD3): PTY, ring buffer, the /_term WebSocket terminus.

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

from . import base as _base
from .base import HERE, HOLD, RING_CAP, TERMS, TERM_DIR
from .chat import prime_context


def term_key(f, sid=""):
    """A terminal's globally unique id: sha1 of the page path, plus the SESSION.

    Keying on the page alone allowed exactly one PTY per page, and asking for a
    different session KILLED the running one (JL 260801: "could you make it that
    I can select multiple sessions attached to this page?"). Different sessions
    write different .jsonl files, so nothing forces them to share one terminal.

    Passing no `sid` keeps the historical page-only key, which is what the
    parked-terminal lookups and the legacy one-per-page callers still use.
    """
    base = str(Path(f).resolve())
    if sid:
        base = base + "\0" + str(sid)
    return hashlib.sha1(base.encode()).hexdigest()[:12]


def terms_for(f):
    """Every live terminal belonging to one page, newest first."""
    want = str(Path(f).resolve())
    out = []
    for key, t in list(TERMS.items()):
        if str(Path(t.get("file", "")).resolve()) == want:
            out.append((key, t))
    out.sort(key=lambda kt: kt[1].get("born", 0), reverse=True)
    return out


# release 之后紧接着的重开会撞上还没死透的旧 claude：同一段 session 被两个进程
# 抢，新的那个直接退出，终端一开就收到 close（260731 电池测出的间歇挂）。
# kill_term 把被杀的 pid 登记在这儿；下一次 spawn 前最多等 2 秒让它咽气。
DYING = {}

# ── 宽限停靠（QD3 条目⑤，JL 260731「开一会儿它自己退了」）───────────────
# 元凶：资产戳变了 → 整页 reload → pagehide beacon 打 /_board/release → 终端被杀。
# 现在 beacon 和 ⌨ 切回都带 park:true：进程和 pump 原地活着，只收 WS、放 HOLD、
# 记个 deadline；宽限内再开 = 秒接（ring 回放整屏，进程根本没死过）。
# 过了 deadline 才真杀；drawer 要开同一题的 SDK 会话时也先杀停靠的（一份 jsonl 一个进程）。
PARK_GRACE = 600
_SWEEP = {"on": False}


def _sweep_parked():
    while True:
        time.sleep(30)
        now = time.time()
        for key, t in list(TERMS.items()):
            dl = t.get("parked")
            if dl and now > dl and t.get("kind") == "pty":
                DYING[key] = t["pid"]
                TERMS.pop(key, None)
                try:
                    os.kill(t["pid"], signal.SIGTERM)
                except Exception:
                    pass
                try:
                    os.unlink(TERM_DIR / f"{key}.pid")
                except Exception:
                    pass


def ensure_sweeper():
    if not _SWEEP["on"]:
        _SWEEP["on"] = True
        threading.Thread(target=_sweep_parked, daemon=True).start()


def wait_dying(key, timeout=2.0):
    pid = DYING.pop(key, None)
    if not pid:
        return
    end = time.time() + timeout
    while time.time() < end:
        try:
            os.kill(pid, 0)
        except OSError:
            return                          # 死透了
        time.sleep(0.05)


def kill_all_terms(*_a):
    """把所有终端（自有 PTY 和 ttyd 后备）一起收掉。退出时调（best-effort），killall 接口也调。"""
    for key, t in list(TERMS.items()):
        try:
            os.kill(t["pid"], signal.SIGTERM)
        except Exception:
            pass
        if t.get("kind") == "pty":
            # fd 和客户端连接不在这儿关 —— pty_pump 是唯一的关闭者（见其注释）；
            # SIGTERM → 进程死 → pump 读到 EOF → 它来收。这儿只清 pidfile。
            try:
                os.unlink(TERM_DIR / f"{key}.pid")
            except Exception:
                pass
        else:
            try:
                os.unlink(t["sock"])
            except Exception:
                pass
    TERMS.clear()


def spawn_pty(cmd, cwd):
    """openpty + spawn；子进程经 os.login_tty 拿 slave 当 controlling tty。
    返回 (proc, master_fd)。"""
    import pty as ptymod
    import fcntl
    import struct as st
    import termios
    master, slave = ptymod.openpty()
    fcntl.ioctl(master, termios.TIOCSWINSZ, st.pack("HHHH", 30, 100, 0, 0))
    # FORCE_COLOR is deliberate, not belt-and-braces: serve.py is usually
    # restarted from a shell that has NO_COLOR set (a tmux/agent session), and
    # NO_COLOR is the standard opt-out every colour library honours, Claude
    # Code's included. Inherited, it made the board's terminal render the real
    # CLI in monochrome while TERM and COLORTERM both claimed truecolor
    # (JL 260801: "why the TUI is black and white, not colored?"). The parent's
    # preference is about the parent's stdout; this PTY is a browser window.
    env = dict(os.environ, TERM="xterm-256color", COLORTERM="truecolor",
               FORCE_COLOR="3")
    env.pop("NO_COLOR", None)
    # serve.py 常常是从某个 Claude Code 会话的 shell 里重启的，会把「我是子会话」
    # 的标记传下来 —— 板上开的 claude 一看见 CLAUDE_CODE_CHILD_SESSION 就把
    # transcript 落盘关了（260731 停靠测试的屏幕上抓到的警告）：resume、拣选器、
    # QD1 的「对话即 session」全被它悄悄废掉。板上的终端是顶级会话，标记全摘。
    for k in ("CLAUDE_CODE_CHILD_SESSION", "CLAUDE_CODE_SESSION_ID",
              "CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT", "CLAUDE_PID"):
        env.pop(k, None)
    proc = subprocess.Popen(cmd, preexec_fn=lambda: os.login_tty(slave),
                            cwd=cwd, env=env, close_fds=True)
    os.close(slave)
    return proc, master


def pty_resize(t, cols, rows):
    import fcntl
    import struct as st
    import termios
    try:
        fcntl.ioctl(t["fd"], termios.TIOCSWINSZ,
                    st.pack("HHHH", int(rows), int(cols), 0, 0))
        os.kill(t["pid"], signal.SIGWINCH)
    except Exception:
        pass


def ws_send(client, data, op=2):
    """一帧发出去（服务器侧不掩码）。op 2=binary（board.js 两种都认）、8=close、10=pong。"""
    if isinstance(data, str):
        data = data.encode()
    n = len(data)
    if n < 126:
        head = bytes([0x80 | op, n])
    elif n < 65536:
        head = bytes([0x80 | op, 126]) + n.to_bytes(2, "big")
    else:
        head = bytes([0x80 | op, 127]) + n.to_bytes(8, "big")
    with client["lock"]:
        client["conn"].sendall(head + data)


def pty_pump(key):
    """每终端一条读线程：master fd → ring buffer + 所有挂着的 WS 客户端。
    UTF-8 尾巴处理：读到半个多字节字符就扣下，跟下一批一起发 —— 客户端是
    按帧解码的（TextDecoder 不带 stream），劈开的 emoji 会变乱码（QD3 的老账）。"""
    t = TERMS.get(key)
    if not t:
        return
    carry = b""
    while True:
        try:
            data = os.read(t["fd"], 65536)
        except OSError:
            data = b""
        if not data:
            break
        data = carry + data
        carry = b""
        k = 1
        while k <= min(4, len(data)):
            b = data[-k]
            if b < 0x80:
                break                          # ASCII 收尾，完整
            if b >= 0xC0:                      # 找到首字节：看长度够不够
                need = 2 if b < 0xE0 else 3 if b < 0xF0 else 4
                if k < need:
                    carry = data[-k:]
                    data = data[:-k]
                break
            k += 1                             # 续字节，继续往前找首字节
        if not data:
            continue
        with t["lock"]:
            t["ring"] += data
            if len(t["ring"]) > RING_CAP:
                del t["ring"][:len(t["ring"]) - RING_CAP]
            clients = list(t["clients"])
        for c in clients:
            try:
                ws_send(c, b"0" + data)
            except Exception:
                with t["lock"]:
                    if c in t["clients"]:
                        t["clients"].remove(c)
    # 进程退了（/exit、崩了、被 kill）：告诉每个窗口、收干净、松开 HOLD。
    # 客户端那边两敲之后会自己 POST /_board/term 重生（--resume 接回来）。
    #
    # ⚠️ 所有权（260731 黑屏教训）：fd 只有这条线程关（kill 路径只发 SIGTERM）。
    # 否则 release 后紧跟一次重开，旧线程的收尾会 double-close 一个已被复用的
    # fd 编号 —— 关掉的可能是新终端的 master 甚至某个 WS socket，页面就是纯黑。
    # 登记表/HOLD/pidfile 是共享的：先看 key 位上还是不是自己，不是就别动 ——
    # 那是接班的新终端的东西。
    mine = TERMS.get(key) is t
    if mine:
        TERMS.pop(key, None)
    with t["lock"]:
        clients = list(t["clients"])
        t["clients"].clear()
    for c in clients:
        try:
            ws_send(c, b"0" + b"\r\n\x1b[90m[claude exited]\x1b[0m\r\n")
            ws_send(c, b"", op=8)
            c["conn"].close()
        except Exception:
            pass
    try:
        os.close(t["fd"])
    except Exception:
        pass
    try:
        os.waitpid(t["pid"], os.WNOHANG)
    except Exception:
        pass
    if mine:
        try:
            os.unlink(TERM_DIR / f"{key}.pid")
        except Exception:
            pass
        cur = HOLD.get(t["file"])
        if cur and cur[0] == "terminal":
            HOLD.pop(t["file"], None)


def reap_stale_terms():
    """启动时清掉上一轮遗留的终端（ttyd 的 socket + 自有 PTY 的 pidfile）。

    退出信号在 daemon + macOS 下不一定接得住，所以不靠它 —— 每次启动先扫一遍
    TERM_DIR。保证不跨重启累积。pidfile 那边杀之前先核对 ps 里的命令行确实是
    我们起的 claude（带 --append-system-prompt），pid 复用才不会误杀无辜。"""
    try:
        socks = list(TERM_DIR.glob("*.sock"))
        pids = list(TERM_DIR.glob("*.pid"))
    except Exception:
        return
    if socks:
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
    for pf in pids:
        try:
            pid = int(pf.read_text().strip())
            cmd = subprocess.run(["ps", "-p", str(pid), "-o", "command="],
                                 capture_output=True, text=True).stdout
            if "claude" in cmd and "--append-system-prompt" in cmd:
                os.kill(pid, signal.SIGTERM)
        except Exception:
            pass
        try:
            os.unlink(pf)
        except Exception:
            pass

class TermMixin:
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
        sid = (p.get("session") or "").strip()
        key = term_key(f, sid) if sid else term_key(f)
        cur = TERMS.get(key)
        if not cur or not self.alive(cur["pid"]):
            return None, "这一页还没有终端：先从 🔌 Plugin 开一次 TUI Chat。"
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
            ttl = (f.name.split("-")[0] + " · " + f.name)[:60]
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

    # ---- 自有 PTY 的 WebSocket 终点：/_term/<key>/ws --------------------
    def ws_term(self, key):
        """握手 + 帧循环。线协议照 ttyd：见 TERMS 注释。新客户端先整段回放 ring。"""
        t = TERMS.get(key)
        if not t or t.get("kind") != "pty":
            return self.send_error(404, "no such terminal")
        wskey = self.headers.get("Sec-WebSocket-Key")
        if not wskey:
            return self.send_error(400, "not a websocket request")
        acc = base64.b64encode(hashlib.sha1(
            (wskey + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode()).digest()).decode()
        head = ("HTTP/1.1 101 Switching Protocols\r\n"
                "Upgrade: websocket\r\nConnection: Upgrade\r\n"
                f"Sec-WebSocket-Accept: {acc}\r\n")
        if "tty" in (self.headers.get("Sec-WebSocket-Protocol") or ""):
            head += "Sec-WebSocket-Protocol: tty\r\n"
        self.connection.sendall((head + "\r\n").encode())
        self.close_connection = True
        client = {"conn": self.connection, "lock": threading.Lock()}
        first_size_done = [False]      # per connection: nudge once, on attach
        with t["lock"]:
            ring = bytes(t["ring"])
            t["clients"].append(client)
        try:
            if ring:
                ws_send(client, b"0" + ring)   # myrlin 的即时回屏
            while True:
                op, msg = self._ws_recv(client)
                if op == 8:
                    break
                if not msg:
                    continue
                c = msg[:1]
                if c == b"{":                  # 开场 JSON：auth / 尺寸（ttyd 协议）
                    try:
                        o = json.loads(msg)
                        if "columns" in o:
                            # THE FIRST size message follows a ring replay whose
                            # bytes were drawn at whatever width the LAST viewer
                            # had. Absolute cursor moves in those bytes land in
                            # the wrong cells of this viewer's grid, which is the
                            # shredded screen JL kept hitting on 260801 after
                            # every reload. Resizing to the same size is not
                            # enough: a full-screen app repaints on a CHANGE, so
                            # an identical size leaves the garbage on screen.
                            # Nudge the width by one and back, which is a real
                            # change either way, and the app repaints its whole
                            # screen at the size this browser actually has.
                            cols, rows = int(o["columns"]), int(o["rows"])
                            if not first_size_done[0]:
                                first_size_done[0] = True
                                # The nudge below repaints the SCREEN, but the
                                # ring we just replayed also went into xterm's
                                # SCROLLBACK, laid out at whatever width the
                                # previous viewer had. That history stays
                                # shredded above the repainted screen, which is
                                # what still read as "messy after a refresh"
                                # (JL 260801, after the first fix). Wipe screen
                                # AND scrollback first, so the only thing on
                                # screen is what the app draws for THIS size.
                                # A full-screen CLI owns its own transcript and
                                # redraws it, so nothing real is lost.
                                ws_send(client, b"0" + b"\x1b[H\x1b[2J\x1b[3J")
                                pty_resize(t, max(2, cols - 1), rows)
                                time.sleep(0.06)
                            pty_resize(t, cols, rows)
                    except Exception:
                        pass
                elif c == b"0":                # 输入
                    try:
                        os.write(t["fd"], msg[1:])
                    except OSError:
                        break
                elif c == b"1":                # 改尺寸
                    try:
                        o = json.loads(msg[1:])
                        pty_resize(t, o["columns"], o["rows"])
                    except Exception:
                        pass
        except (ConnectionError, OSError):
            pass
        finally:
            with t["lock"]:
                if client in t["clients"]:
                    t["clients"].remove(client)

    def _ws_read_exact(self, n):
        data = b""
        while len(data) < n:
            chunk = self.rfile.read(n - len(data))
            if not chunk:
                raise ConnectionError("ws closed")
            data += chunk
        return data

    def _ws_recv(self, client):
        """收一条完整消息（处理续帧和控制帧）。返回 (opcode, payload)。"""
        opcode, payload = None, b""
        while True:
            h = self._ws_read_exact(2)
            fin, op = h[0] & 0x80, h[0] & 0x0F
            ln = h[1] & 0x7F
            if ln == 126:
                ln = int.from_bytes(self._ws_read_exact(2), "big")
            elif ln == 127:
                ln = int.from_bytes(self._ws_read_exact(8), "big")
            mask = self._ws_read_exact(4) if (h[1] & 0x80) else b""
            data = self._ws_read_exact(ln)
            if mask:
                data = bytes(x ^ mask[i & 3] for i, x in enumerate(data))
            if op == 9:                        # ping → pong
                try:
                    ws_send(client, data, op=10)
                except Exception:
                    pass
                continue
            if op == 10:                       # pong：忽略
                continue
            if op == 8:
                return 8, b""
            if opcode is None:
                opcode = op
            payload += data
            if fin:
                return opcode, payload

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
        """serve vendored xterm from the skill folder, board-location-independent.
        /_board/asset/xterm.min.js  ·  /_board/asset/xterm.css"""
        name = self.path.rsplit("/", 1)[-1].split("?")[0]
        if name not in ("xterm.min.js", "xterm.css", "addon-unicode11.js"):
            return self.send_error(404)
        p = HERE / "vendor" / "xterm" / name
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
