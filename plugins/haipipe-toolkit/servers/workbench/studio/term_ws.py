"""The terminal's wire layer: the ttyd reverse proxy and the own-PTY WebSocket terminus.

Split out of term.py (2026-11-13) by responsibility; behaviour unchanged.
TermMixin in term.py inherits TermWireMixin, so serve.py still composes `TermMixin`.
"""

import base64
import hashlib
import json
import os
import re
import threading
import time

from .base import TERMS
from .term_pty import labeling_tui_hold, pty_resize, ws_send


class TermWireMixin:
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
        reason = labeling_tui_hold(t.get("file") or "")
        if reason:
            return self.send_error(423, reason + " · TUI is read-only at this gate")
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


    # ---- 自有 PTY 的 WebSocket 终点：/_term/<key>/ws --------------------
    def ws_term(self, key):
        """握手 + 帧循环。线协议照 ttyd：见 TERMS 注释。新客户端先整段回放 ring。"""
        t = TERMS.get(key)
        if not t or t.get("kind") != "pty":
            return self.send_error(404, "no such terminal")
        reason = labeling_tui_hold(t.get("file") or "")
        if reason:
            return self.send_error(423, reason + " · TUI is read-only at this gate")
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
                    reason = labeling_tui_hold(t.get("file") or "")
                    if reason:
                        ws_send(client, b"0\r\n" + reason.encode("utf-8") +
                                b"\r\nTUI is read-only at this gate.\r\n")
                        break
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

