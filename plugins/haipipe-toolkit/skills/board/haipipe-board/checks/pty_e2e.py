#!/usr/bin/env python3
"""End-to-end test of serve.py's own-PTY terminal (QD3's engine; the plan was
QD3m §8 before that page merged into QD3, 260801).

Speaks the ttyd wire protocol exactly like assets/board.js connectWS():
handshake with subprotocol 'tty', auth JSON, size JSON, input '0'+data,
resize '1'+json; output frames lead with '0'.
"""
import base64
import hashlib
import json
import os
import socket
import sys
import time
import urllib.request

# Overridable so checks/run.py can aim this at a throwaway fixture board —
# a standing check must never rewrite a real page's `session:` header.
HOST = os.environ.get("CHECK_HOST", "127.0.0.1")
PORT = int(os.environ.get("CHECK_PORT", "5599"))
BOARD = os.environ.get(
    "CHECK_BOARD", "Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722")
FILE = os.environ.get("CHECK_FILE", "QD-working/QD3-chat-terminal.md")


def post(path, payload):
    r = urllib.request.urlopen(urllib.request.Request(
        f"http://{HOST}:{PORT}{path}", json.dumps(payload).encode(),
        {"Content-Type": "application/json"}), timeout=30)
    return json.loads(r.read())


def ws_connect(key):
    s = socket.create_connection((HOST, PORT), timeout=120)
    wskey = base64.b64encode(os.urandom(16)).decode()
    s.sendall((f"GET /_term/{key}/ws HTTP/1.1\r\nHost: {HOST}:{PORT}\r\n"
               "Upgrade: websocket\r\nConnection: Upgrade\r\n"
               f"Sec-WebSocket-Key: {wskey}\r\nSec-WebSocket-Version: 13\r\n"
               "Sec-WebSocket-Protocol: tty\r\n\r\n").encode())
    head = b""
    while b"\r\n\r\n" not in head:
        head += s.recv(4096)
    head, _, rest = head.partition(b"\r\n\r\n")
    assert b"101" in head.split(b"\r\n")[0], head
    want = base64.b64encode(hashlib.sha1(
        (wskey + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode()).digest()).decode()
    assert want.encode() in head, "bad Sec-WebSocket-Accept"
    assert b"Sec-WebSocket-Protocol: tty" in head, "subprotocol not echoed"
    return s, rest


def ws_send(s, text, op=1):
    data = text.encode() if isinstance(text, str) else text
    mask = os.urandom(4)
    n = len(data)
    if n < 126:
        h = bytes([0x80 | op, 0x80 | n])
    else:
        h = bytes([0x80 | op, 0x80 | 126]) + n.to_bytes(2, "big")
    s.sendall(h + mask + bytes(b ^ mask[i & 3] for i, b in enumerate(data)))


def ws_recv(s, buf):
    def need(n):
        nonlocal buf
        while len(buf) < n:
            chunk = s.recv(65536)
            if not chunk:
                raise ConnectionError("closed")
            buf += chunk
        out, buf = buf[:n], buf[n:]
        return out
    h = need(2)
    op, ln = h[0] & 0x0F, h[1] & 0x7F
    if ln == 126:
        ln = int.from_bytes(need(2), "big")
    elif ln == 127:
        ln = int.from_bytes(need(8), "big")
    data = need(ln)
    return op, data, buf


def drain_until(s, buf, needle, timeout):
    got = b""
    end = time.time() + timeout
    s.settimeout(5)
    while time.time() < end:
        try:
            op, data, buf = ws_recv(s, buf)
        except socket.timeout:
            continue
        if op == 8:
            break
        if data[:1] == b"0":
            got += data[1:]
        if needle and needle in got:
            return got, buf, True
    return got, buf, not needle


t0 = time.time()
j = post("/_board/term", {"path": f"/{BOARD}/board.html", "file": FILE})
assert j["ok"], j
key, sid = j["key"], j["session"]
print(f"① term spawned · key={key} · session={sid[:8]}… · reused={j['reused']}")

s, buf = ws_connect(key)
print("② WS handshake OK (101 + accept + subprotocol tty)")
ws_send(s, json.dumps({"AuthToken": ""}))
ws_send(s, json.dumps({"columns": 100, "rows": 30}))

got, buf, _ = drain_until(s, buf, None, 12)
assert len(got) > 100, f"no boot output ({len(got)} bytes)"
print(f"③ claude TUI booted · {len(got)} bytes of output streamed")

# A fixture cwd is brand-new, so a fresh claude shows the folder-trust dialog
# and the TUI is blocked until it is answered (found when the turn below timed
# out against an identically-sized boot screen). Enter accepts; a stray Enter
# on an already-ready prompt is an empty input and harmless.
if b"trust" in got.lower():
    ws_send(s, "0\r")
    got_t, buf, _ = drain_until(s, buf, None, 6)
    print(f"③b trust dialog accepted · {len(got_t)} bytes repaint")

ws_send(s, "0reply with exactly PTYOK and nothing else")
time.sleep(0.6)
ws_send(s, "0\r")
got2, buf, hit = drain_until(s, buf, b"PTYOK", 90)
assert hit, f"PTYOK not seen in {len(got2)} bytes"
print(f"④ real turn ran through the PTY · PTYOK came back · {len(got2)} bytes")

ws_send(s, "1" + json.dumps({"columns": 120, "rows": 40}))
time.sleep(1)
got3, buf, _ = drain_until(s, buf, None, 3)
print(f"⑤ resize op accepted · {len(got3)} bytes repaint followed")

s2, buf2 = ws_connect(key)
ws_send(s2, json.dumps({"AuthToken": ""}))
s2.settimeout(5)
op, data, buf2 = ws_recv(s2, buf2)
assert data[:1] == b"0" and len(data) > 1000, f"ring replay missing ({len(data)} bytes)"
assert b"PTYOK" in data, "replay does not contain the session's earlier output"
print(f"⑥ second client got instant ring replay · {len(data)} bytes incl. PTYOK")
s2.close()

j = post("/_board/release", {"path": f"/{BOARD}/board.html", "file": FILE})
assert j["ok"] and j["closed"], j
time.sleep(0.5)
terms = post("/_board/terms", {})["terms"]
assert not any(t["key"] == key for t in terms), terms
print(f"⑦ released clean · no orphan in /_board/terms · total {time.time()-t0:.0f}s")
print("ALL PASS")
