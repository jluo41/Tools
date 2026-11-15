"""The terminal's process layer: PTY spawn, ring-buffer pump, parking, reaping.

Split out of term.py (2026-11-13) by responsibility; behaviour unchanged.
term.py re-exports every name here, so `from live.term import ...` keeps working.
"""

import hashlib
import os
import signal
import subprocess
import threading
import time
from pathlib import Path

from .base import HOLD, RING_CAP, TERMS, TERM_DIR
from .chat import chat_guard

def labeling_tui_hold(f) -> str:
    """Return the server-owned Labeling HOLD reason for any TUI door."""
    _, _, reason = chat_guard(Path(f), {})
    return reason


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
