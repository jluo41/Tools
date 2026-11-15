"""The held Claude SDK clients: the OAuth token, one event loop for the process, one live client per question.

Split out of chat.py (2026-11-13); chat.py re-exports every name here and keeps HOST, HOLD_CHAT and host().
"""

import os
import re
import threading
import time



def oauth_token(root):
    """OAuth token for the SDK, or None to fall back to the ambient login."""
    tok = os.environ.get("CLAUDE_CODE_OAUTH_TOKEN")
    if tok:
        return tok.strip(), "env"
    envsh = root / "env.sh"
    if envsh.exists():
        m = re.search(r"^\s*(?:export\s+)?CLAUDE_CODE_OAUTH_TOKEN=[\"\']?([^\"\'\s#]+)",
                      envsh.read_text(encoding="utf-8", errors="ignore"), re.M)
        if m:
            return m.group(1), "env.sh"
    return None, "ambient"

class _Live:
    """One question's held ClaudeSDKClient, plus the turn context it must see.

    `ctx` is the swap point that makes holding a client safe. `can_use_tool` is a
    CONNECT-time option, so a held client keeps whichever callback it was built
    with; if that callback closed over the first request's `emit`, message two's
    permission prompt would be written into message one's dead socket. The
    callback therefore closes over this object and reads `ctx` at call time, and
    each turn swaps its own context in.
    """

    __slots__ = ("client", "fp", "ctx", "last", "lock", "sid")

    def __init__(self, client, fp):
        self.client, self.fp = client, fp
        self.sid = None                       # the conversation this client IS
        self.ctx, self.last = None, time.time()
        self.lock = threading.Lock()          # one turn at a time per question


class SessionHost:
    """QD2 M1: one event loop for the process's life, owning every live client.

    The extension holds one `claude` per session and pushes each turn into it;
    we booted one per POST, which is the whole of the 8.1s first token and the
    per-message skill-registry reload. The SDK already supports this (its own
    docstring names chat UIs as the case for ClaudeSDKClient) with one hard
    constraint: a client may not cross async runtime contexts. So every
    operation on it happens on THIS loop, and the HTTP thread only submits.
    """

    def __init__(self):
        self.loop = None
        self.sessions = {}                    # str(question path) -> _Live
        self.lock = threading.Lock()
        self._ready = threading.Event()
        threading.Thread(target=self._serve, daemon=True,
                         name="chat-session-host").start()
        self._ready.wait(10)
        threading.Thread(target=self._reaper, args=(1800, 120), daemon=True,
                         name="chat-session-reaper").start()

    def _serve(self):
        import asyncio
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self._ready.set()
        self.loop.run_forever()

    def submit(self, coro):
        """Run a coroutine on the host loop; the caller's thread blocks on it."""
        import asyncio
        return asyncio.run_coroutine_threadsafe(coro, self.loop)

    async def acquire(self, key, fp, make_client, want=""):
        """The held client for this question, reconnecting only when it must.

        `fp` fingerprints every CONNECT-time option (model, effort, tier, which
        session is resumed). The system prompt is deliberately NOT in it: it is
        fixed at connect for a real CLI session too, so a page edit mid-chat
        does not silently restart the conversation.
        """
        live = self.sessions.get(key)
        # an explicit pick from the drawer's session strip overrides reuse:
        # "new" always starts fresh, a uuid must match the one we are holding
        picked_elsewhere = bool(want) and (want == "new" or
                                           (live is not None and want != live.sid))
        if live and live.fp == fp and not picked_elsewhere:
            live.last = time.time()
            return live, False
        if live:
            await self._drop(key)
        client = await make_client()
        live = _Live(client, fp)
        with self.lock:
            self.sessions[key] = live
        return live, True

    async def _drop(self, key):
        live = self.sessions.pop(key, None)
        if not live:
            return
        try:
            await live.client.disconnect()
        except Exception:
            pass

    def evict(self, key):
        """Release a question's client from any thread.

        QD1's Law is one window per session: when the ⌨ terminal takes a
        question, the drawer's held client must let go of the same .jsonl.
        """
        if not self.sessions.get(key):
            return
        try:
            self.submit(self._drop(key)).result(timeout=20)
        except Exception:
            pass

    def reap(self, idle_s=1800):
        now = time.time()
        for key, live in list(self.sessions.items()):
            if now - live.last > idle_s and not live.lock.locked():
                self.evict(key)

    def _reaper(self, idle_s, every):
        """A held client is a live `claude` process, so idleness must end it.

        Without this, opening ten questions leaves ten processes alive for the
        life of the server. Mirrors how QD3 reaps terminals rather than trusting
        exit signals.
        """
        while True:
            time.sleep(every)
            try:
                self.reap(idle_s)
            except Exception:
                pass

    def close_all(self):
        for key in list(self.sessions):
            self.evict(key)
