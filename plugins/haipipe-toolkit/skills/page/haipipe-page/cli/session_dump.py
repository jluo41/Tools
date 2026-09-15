#!/usr/bin/env python3
"""Dump one assistant session to a readable Markdown transcript, read-only.

This is the intake step of ``fn/reflect.md``. It never modifies the provider
store; it only reads persisted content and writes one Markdown file.

Providers
---------
codex   ``--codex <thread-id>``  merges every rollout JSONL under
        ``$CODEX_HOME/sessions`` whose filename carries the thread id (a fork
        continues the same thread in a second file) with the ``thread_items``
        rows of ``$CODEX_HOME/thread_history_1.sqlite``.
claude  ``--claude <path.jsonl>`` reads one native Claude Code transcript
        (``~/.claude/projects/<cwd-slug>/<session-id>.jsonl``).
studio  ``--studio <transcript.md>`` copies a kept Studio Chat transcript.

Usage
-----
    session_dump.py --codex 01a0…  --name Paper-MISQ-Intro-v3 --out intro.md
    session_dump.py --codex 01a0…  --name … --out intro.md --compact 1500
    session_dump.py --claude ~/.claude/projects/-Users-me-repo/abc.jsonl --out x.md
    session_dump.py --list-codex 'Paper-MISQ%'      # find thread ids by name

``--compact N`` trims each assistant reply to N characters and drops tool
lines; the person's inputs are never trimmed.
"""
from __future__ import annotations

import argparse
import datetime as dt
import glob
import json
import os
import re
import sqlite3
import sys

CODEX_HOME = os.environ.get("CODEX_HOME", os.path.expanduser("~/.codex"))

NOISE_PREFIXES = (
    "<recommended_plugins>", "<skills_instructions>", "<in-app-browser-context",
    "<environment_context", "<permissions instructions>", "<system-reminder>",
    "<command-name>", "<local-command-stdout>", "Base directory for this skill",
    "<turn_aborted", "<user_shell_command", "<collaboration_mode",
    "<skill", "<subagent_notification", "<app-server",
)


def local(ts) -> str:
    if ts is None:
        return "?"
    if isinstance(ts, (int, float)):
        secs = ts / 1000 if ts > 1e11 else ts
        return dt.datetime.fromtimestamp(secs).strftime("%Y-%m-%d %H:%M:%S")
    try:
        return (dt.datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
                .astimezone().strftime("%Y-%m-%d %H:%M:%S"))
    except Exception:
        return str(ts)


def sort_key(ts) -> float:
    if isinstance(ts, (int, float)):
        return ts / 1000 if ts > 1e11 else float(ts)
    try:
        return dt.datetime.fromisoformat(str(ts).replace("Z", "+00:00")).timestamp()
    except Exception:
        return 0.0


def text_of(content) -> str:
    if isinstance(content, str):
        return content
    out = []
    for x in content or []:
        if isinstance(x, dict) and isinstance(x.get("text"), str):
            out.append(x["text"])
    return "\n".join(out)


def is_noise(t: str) -> bool:
    t = t.lstrip()
    return any(t.startswith(p) for p in NOISE_PREFIXES)


def clean_user(t: str) -> str:
    """Strip injected blocks; keep the person's words and name any attachments."""
    t = re.sub(r"<in-app-browser-context.*?</in-app-browser-context>\s*", "", t, flags=re.S)
    t = re.sub(r"<system-reminder>.*?</system-reminder>\s*", "", t, flags=re.S)
    m = re.search(r"## My request:\s*", t)
    if m:
        head, t = t[:m.start()], t[m.end():]
        names = [n.strip() for n in re.findall(r"^## ([^\n:]+?)(?::| *$)", head, flags=re.M)]
        names = [n for n in names if n and n.lower() != "my request"]
        if names:
            t = "[attachments: " + ", ".join(names) + "]\n" + t
    return t.strip()


class Dump:
    def __init__(self) -> None:
        self.events: list[tuple] = []   # (ts, kind, text)
        self._seen: set = set()
        self.sources: list[str] = []

    def add(self, ts, kind: str, text: str) -> None:
        text = (text or "").strip()
        if not text:
            return
        sig = (kind, re.sub(r"\s+", " ", text)[:400])
        if sig in self._seen:
            return
        self._seen.add(sig)
        self.events.append((ts, kind, text))

    # ---- codex -----------------------------------------------------------
    def read_codex(self, tid: str) -> None:
        files = sorted(glob.glob(f"{CODEX_HOME}/sessions/**/*{tid}*.jsonl", recursive=True))
        self.sources += files
        for fp in files:
            with open(fp, errors="replace") as fh:
                for line in fh:
                    try:
                        ev = json.loads(line)
                    except Exception:
                        continue
                    ts = ev.get("timestamp")
                    p = ev.get("payload") or {}
                    if not isinstance(p, dict):
                        continue
                    t, pt = ev.get("type"), p.get("type")
                    if t == "response_item" and pt == "message":
                        txt = text_of(p.get("content"))
                        if p.get("role") == "user":
                            txt = clean_user(txt)
                            if txt and not is_noise(txt):
                                self.add(ts, "USER", txt)
                        elif p.get("role") == "assistant":
                            self.add(ts, "ASSISTANT", txt)
                    elif t == "response_item" and pt in ("custom_tool_call", "function_call"):
                        s = p.get("input") or p.get("arguments") or ""
                        if isinstance(s, dict):
                            s = json.dumps(s, ensure_ascii=False)
                        patches = re.findall(r"\*\*\* (Update|Add|Delete) File: ([^\\\n\"]+)", s)
                        if patches:
                            self.add(ts, "PATCH", "\n".join(f"{a[0]} {b.strip()}" for a, b in patches))
                        else:
                            m = re.search(r"cmd\W{1,4}([^\n]{0,220})", s) or re.search(r"command\W{1,4}([^\n]{0,220})", s)
                            self.add(ts, "TOOL", f"{p.get('name', 'tool')}: {(m.group(1) if m else s[:220]).strip()}")
                    elif t == "event_msg" and pt == "task_complete" and p.get("last_agent_message"):
                        self.add(ts, "ASSISTANT", p["last_agent_message"])
        db_path = f"{CODEX_HOME}/thread_history_1.sqlite"
        if os.path.exists(db_path):
            try:
                db = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
                rows = db.execute(
                    "SELECT item_type, item_json, created_at_ms FROM thread_items "
                    "WHERE thread_id=? ORDER BY rollout_ordinal", (tid,)).fetchall()
                if rows:
                    self.sources.append(f"{db_path} · thread_items · {len(rows)} rows")
                for it, js, ms in rows:
                    try:
                        item = json.loads(js)
                    except Exception:
                        continue
                    ts = dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc).isoformat()
                    if it == "userMessage":
                        txt = clean_user(text_of(item.get("content") or item.get("text")))
                        if txt and not is_noise(txt):
                            self.add(ts, "USER", txt)
                    elif it == "agentMessage":
                        self.add(ts, "ASSISTANT", text_of(item.get("content") or item.get("text")))
                    elif "patch" in it.lower() or it == "fileChange":
                        paths = re.findall(r'"path"\s*:\s*"([^"]+)"', json.dumps(item, ensure_ascii=False))
                        if paths:
                            self.add(ts, "PATCH", "\n".join("U " + x for x in dict.fromkeys(paths)))
            except Exception as exc:  # read-only best effort
                print(f"sqlite skipped: {exc}", file=sys.stderr)

    # ---- claude ----------------------------------------------------------
    def read_claude(self, path: str) -> None:
        self.sources.append(path)
        with open(path, errors="replace") as fh:
            for line in fh:
                try:
                    ev = json.loads(line)
                except Exception:
                    continue
                ts = ev.get("timestamp")
                msg = ev.get("message") or {}
                content = msg.get("content")
                if ev.get("type") == "user":
                    if isinstance(content, list) and any(isinstance(c, dict) and c.get("type") == "tool_result" for c in content):
                        continue
                    txt = clean_user(text_of(content))
                    if txt and not is_noise(txt):
                        self.add(ts, "USER", txt)
                elif ev.get("type") == "assistant":
                    txt = text_of(content)
                    if txt:
                        self.add(ts, "ASSISTANT", txt)
                    for c in content if isinstance(content, list) else []:
                        if isinstance(c, dict) and c.get("type") == "tool_use":
                            inp = c.get("input") or {}
                            fp = inp.get("file_path")
                            if c.get("name") in ("Write", "Edit") and fp:
                                self.add(ts, "PATCH", f"U {fp}")
                            else:
                                self.add(ts, "TOOL", f"{c.get('name')}: {json.dumps(inp, ensure_ascii=False)[:220]}")

    # ---- studio ----------------------------------------------------------
    def read_studio(self, path: str) -> None:
        self.sources.append(path)
        with open(path, errors="replace") as fh:
            self.add(None, "RAW", fh.read())

    # ---- write -----------------------------------------------------------
    def write(self, out: str, name: str, ident: str, compact: int | None) -> dict:
        self.events.sort(key=lambda e: sort_key(e[0]))
        users = [e for e in self.events if e[1] == "USER"]
        n_ass = sum(1 for e in self.events if e[1] == "ASSISTANT")
        n_tool = sum(1 for e in self.events if e[1] == "TOOL")
        n_patch = sum(1 for e in self.events if e[1] == "PATCH")
        span = (local(self.events[0][0]), local(self.events[-1][0])) if self.events else ("?", "?")
        with open(out, "w") as f:
            f.write(f"# Session transcript · {name}\n\n")
            f.write(f"- identity: `{ident}`\n- sources: {len(self.sources)}\n")
            for s in self.sources:
                f.write(f"    - {s}\n")
            f.write(f"- span: {span[0]} → {span[1]}\n")
            f.write(f"- user turns: {len(users)} · assistant messages: {n_ass} · tool calls: {n_tool} · patch events: {n_patch}\n")
            if compact:
                f.write(f"- compact: assistant replies trimmed to {compact} characters; tool lines dropped; inputs verbatim\n")
            f.write("\n## Your inputs, verbatim, in order\n\n")
            for i, e in enumerate(users, 1):
                f.write(f"### U{i:02d} · {local(e[0])}\n\n{e[2]}\n\n")
            f.write("\n---\n\n## Full timeline\n\n")
            ui = 0
            for ts, kind, text in self.events:
                if kind == "USER":
                    ui += 1
                    f.write(f"\n### U{ui:02d} · USER · {local(ts)}\n\n{text}\n\n")
                elif kind == "ASSISTANT":
                    body = text if not compact or len(text) <= compact else text[:compact] + " …[trimmed]"
                    f.write(f"#### ASSISTANT · {local(ts)}\n\n{body}\n\n")
                elif kind == "TOOL" and not compact:
                    f.write(f"- 🔧 {local(ts)} `{text[:240]}`\n")
                elif kind == "PATCH":
                    f.write(f"- ✏️ {local(ts)} files:\n" + "\n".join("    - " + x for x in text.splitlines()) + "\n")
                elif kind == "RAW":
                    f.write(text + "\n")
        return {"out": out, "users": len(users), "assistant": n_ass, "tools": n_tool,
                "patches": n_patch, "span": span, "kb": os.path.getsize(out) // 1024}


def list_codex(pattern: str) -> None:
    db = sqlite3.connect(f"file:{CODEX_HOME}/state_5.sqlite?mode=ro", uri=True)
    rows = db.execute(
        "SELECT id, COALESCE(name,title), datetime(updated_at_ms/1000,'unixepoch','localtime'), archived, cwd "
        "FROM threads WHERE COALESCE(name,title) LIKE ? ORDER BY updated_at_ms DESC", (pattern,)).fetchall()
    for tid, name, upd, arch, cwd in rows:
        print(f"{upd}  {'arch' if arch else 'live'}  {tid}  {name}  ({cwd})")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--codex", metavar="THREAD_ID")
    src.add_argument("--claude", metavar="JSONL")
    src.add_argument("--studio", metavar="TRANSCRIPT_MD")
    src.add_argument("--list-codex", metavar="NAME_LIKE", help="list Codex threads whose name matches (SQL LIKE)")
    ap.add_argument("--name", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--compact", type=int, default=None, metavar="N")
    a = ap.parse_args()
    if a.list_codex:
        list_codex(a.list_codex)
        return 0
    d = Dump()
    if a.codex:
        d.read_codex(a.codex); ident = a.codex
    elif a.claude:
        d.read_claude(a.claude); ident = a.claude
    else:
        d.read_studio(a.studio); ident = a.studio
    name = a.name or os.path.basename(ident)
    out = a.out or re.sub(r"[^A-Za-z0-9._-]+", "-", name) + ".md"
    r = d.write(out, name, ident, a.compact)
    print(f"{name}: users={r['users']} assistant={r['assistant']} tools={r['tools']} patches={r['patches']} "
          f"span={r['span'][0]} → {r['span'][1]} -> {r['out']} ({r['kb']} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
