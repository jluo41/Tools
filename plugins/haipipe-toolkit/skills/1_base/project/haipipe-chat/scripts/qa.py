"""A chat as QAs: one question the person asked, the answer, and what it produced (haipipe-chat ref/chat-contract.md).

`from_session(jsonl)` reads a Claude Code session file. One QA is one turn: the person's message, plus any message
they sent while that turn was running (a queued message, added to the same question). Its answer is the first line
of the turn's last reply (replies here put the answer on line 1). Its outputs are the files the assistant's Edit,
Write and NotebookEdit calls touched in the turn. Tool calls, tool output, thinking and injected context are left out.
"""
from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path

WRITERS = {"Edit", "Write", "NotebookEdit", "MultiEdit"}
_PASTE = re.compile(r"</?pasted_content[^>]*>")
_INJECTED = ("<system-reminder>", "<command-name>", "<local-command", "<task-notification>", "Caveat:",
             "[Request interrupted")


def _words(content) -> str:
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        return "\n\n".join(b.get("text", "").strip() for b in content
                           if isinstance(b, dict) and b.get("type") == "text" and b.get("text", "").strip())
    return ""


def _question(text: str) -> str:
    text = _PASTE.sub("", text).replace("\xa0", " ")
    text = "\n".join(line.rstrip() for line in text.strip().splitlines())
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def _answer_line(text: str) -> str:
    return next((line.strip() for line in text.splitlines() if line.strip()), "")


def _local_time(stamp: str) -> str:
    """HH:MM in local time from an ISO timestamp (a session file stores UTC)."""
    try:
        return dt.datetime.fromisoformat(stamp.replace("Z", "+00:00")).astimezone().strftime("%H:%M")
    except ValueError:
        return ""


def _rows(jsonl: Path):
    for line in jsonl.read_text(encoding="utf-8", errors="ignore").splitlines():
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict):
            yield row


def from_session(jsonl: Path) -> list[dict]:
    """[{q, time, answer, outputs}] in the order they were asked."""
    qas: list[dict] = []
    for row in _rows(jsonl):
        kind, msg, att = row.get("type"), row.get("message") or {}, row.get("attachment") or {}
        if kind == "user" and not row.get("isMeta") and isinstance(msg, dict):
            text = _words(msg.get("content"))
            if text and not text.lstrip().startswith(_INJECTED):
                qas.append({"q": _question(text), "time": _local_time(str(row.get("timestamp") or "")),
                            "answer": "", "outputs": []})
            continue
        if kind == "attachment" and att.get("type") == "queued_command" \
                and (att.get("origin") or {}).get("kind") == "human" and att.get("prompt"):
            added = _question(str(att["prompt"]))          # sent mid-turn: part of the running turn's question
            if qas:
                qas[-1]["q"] += "\n\n" + added
            else:
                qas.append({"q": added, "time": _local_time(str(att.get("timestamp") or "")), "answer": "",
                            "outputs": []})
            continue
        if kind == "assistant" and qas and isinstance(msg, dict):
            for block in msg.get("content") or []:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "text" and block.get("text", "").strip():
                    qas[-1]["answer"] = _answer_line(block["text"])
                elif block.get("type") == "tool_use" and block.get("name") in WRITERS:
                    path = (block.get("input") or {}).get("file_path") or (block.get("input") or {}).get("notebook_path")
                    if path and path not in qas[-1]["outputs"]:
                        qas[-1]["outputs"].append(path)
    return [qa for qa in qas if qa["q"]]


def _one_line(text: str, cap: int) -> str:
    flat = " ".join(text.split())
    return flat if len(flat) <= cap else flat[:cap - 2].rsplit(" ", 1)[0] + " …"


def markdown(qas: list[dict]) -> list[str]:
    """The ## QA section, three lines a turn at most: `qNN HH:MM · the question`, `→ the answer`, `⇢ the files it
    wrote` (their names; the full paths are the face's `paths:`)."""
    out = ["## QA", ""]
    for n, qa in enumerate(qas, 1):
        when = f" {qa['time']}" if qa.get("time") else ""
        out.append(f"- **q{n:02d}**{when} · {_one_line(qa['q'], 200)}")
        if qa.get("answer"):
            out.append(f"  → {_one_line(qa['answer'], 160)}")
        if qa.get("outputs"):
            out.append("  ⇢ " + ", ".join(f"`{Path(o).name}`" for o in qa["outputs"]))
    return out + [""]
