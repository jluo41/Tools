"""How a chat turn is written down for people: tool cards, transcript.md, digest.md and the kept-session folder.

Split out of chat.py (2026-11-13); chat.py re-exports every name here.
"""

import json
import re
from pathlib import Path



def tool_brief(name, tin):
    """把工具调用压成一行给人看 —— 跟 CLI 弹的那个提示同一个意思。"""
    for k in ("file_path", "path", "notebook_path"):
        if tin.get(k):
            return f"{name}  {tin[k]}"
    if name == "Bash":
        return "Bash  " + str(tin.get("command", ""))[:160]
    keys = ", ".join(list(tin)[:3])
    return f"{name}  ({keys})" if keys else name


TOOL_CAP = 4000        # a card is a preview, not a full log viewer


def tool_input_preview(tin):
    """What the workbench shows in a call's IN block, truncated to a card."""
    if not isinstance(tin, dict):
        return str(tin)[:TOOL_CAP]
    if "command" in tin:                       # Bash reads best as the command
        return str(tin["command"])[:TOOL_CAP]
    try:
        return json.dumps(tin, ensure_ascii=False, indent=1)[:TOOL_CAP]
    except Exception:
        return str(tin)[:TOOL_CAP]


def tool_output_preview(content):
    """A tool result is text, a list of blocks, or neither; flatten to text."""
    if content is None:
        return ""
    if isinstance(content, str):
        return content[:TOOL_CAP]
    if isinstance(content, list):
        parts = []
        for b in content:
            if isinstance(b, dict):
                parts.append(b.get("text") or b.get("content") or "")
            else:
                parts.append(getattr(b, "text", "") or "")
        return "\n".join(str(x) for x in parts if x)[:TOOL_CAP]
    return str(content)[:TOOL_CAP]


def transcript_markdown(rows, head):
    """One kept session -> Studio Chat's transcript.md (QPf4 §1, JL 260815).

    `rows` are session_log's own rows ({"k": you|ai|tool, "t", "ts", ["name"]}),
    so the record and the live replay can never disagree about what happened.
    Pure function, so the formatter is testable without a server.
    """
    def hhmm(ts):
        return (ts or "")[11:16]

    name = head.get("name") or head.get("title") or head.get("id", "")[:8]
    lines = [
        f"# 💬 {name}",
        f"session: {head.get('id', '')}",
        f"kept: {head.get('kept', '')} · source: {head.get('source', '')}",
        "",
        "The digest is the reading path and this transcript is reference "
        "(QPf4 Content §1); decisions made here are routed onto pages as "
        "sentences, never left in this file.",
        "",
        "---",
        "",
    ]
    for r in rows:
        k = r.get("k")
        if k == "tool":
            lines.append(f"> 🔧 {r.get('name', '?')} · {r.get('t', '')}")
        elif k == "you":
            lines += [f"**You** · {hhmm(r.get('ts'))}", "", r.get("t", ""), ""]
        else:
            lines += [f"**Claude** · {hhmm(r.get('ts'))}", "", r.get("t", ""), ""]
    return "\n".join(lines).rstrip() + "\n"


def digest_markdown(rows, head):
    """One kept session -> its short reading path, without inventing decisions.

    The first human ask and final assistant outcome are durable anchors already
    present in the transcript. Any authoritative decision still belongs in the
    Page's Outline records rather than being inferred here.
    """
    name = head.get("name") or head.get("title") or head.get("id", "")[:8]
    ask = next((r.get("t", "").strip() for r in rows
                if r.get("k") == "you" and r.get("t", "").strip()), "")
    outcome = next((r.get("t", "").strip() for r in reversed(rows)
                    if r.get("k") == "ai" and r.get("t", "").strip()), "")
    tools = []
    for row in rows:
        tool = row.get("name") if row.get("k") == "tool" else None
        if tool and tool not in tools:
            tools.append(tool)

    def bounded(value, limit=4000):
        value = value or "Not recorded."
        return value if len(value) <= limit else value[:limit].rstrip() + "\n\n…"

    lines = [
        f"# 💬 {name}",
        f"session: {head.get('id', '')}",
        f"kept: {head.get('kept', '')}",
        "",
        "This is the reading path for the kept session. Authoritative decisions "
        "and edits remain in the Page; use [transcript.md](transcript.md) for the "
        "complete exchange.",
        "",
        "## Ask",
        "",
        bounded(ask),
        "",
        "## Outcome",
        "",
        bounded(outcome),
        "",
        "## Activity",
        "",
        ("Tools observed: " + ", ".join(tools) + ".") if tools
        else "No tool calls were recorded.",
    ]
    return "\n".join(lines).rstrip() + "\n"


def kept_session_dir(chat_dir, stamp, sid):
    """Stable timestamp-first folder; suffix only on a real minute collision."""
    chat_dir = Path(chat_dir)
    for index in range(1, 1000):
        name = stamp if index == 1 else f"{stamp}-{index:02d}"
        candidate = chat_dir / name
        if not candidate.exists():
            return candidate
        for record in (candidate / "digest.md", candidate / "transcript.md"):
            try:
                body = record.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if re.search(r"(?m)^session:\s*" + re.escape(sid) + r"\s*$", body):
                return candidate
    raise RuntimeError(f"too many kept-session collisions at {stamp}")
