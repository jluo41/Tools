"""An insight page's DO / DO NOT counsel as lines and rules, and the draft request the queue runner reads
(split out of design_actions.py)."""
from __future__ import annotations

import re
from pathlib import Path

from live.design import plan_folder
from live.design_actions_files import ActionError, _now


# ------------------------------------------------------------- rules + draft --

_COUNSEL = re.compile(r"^\s*(W\d+)\s+(DO NOT|DO)\s+(.+?)(?:\s{2,}\S.*)?$")


def counsel_lines(text: str) -> list[dict]:
    """The DO / DO NOT counsel lines of an insight page, in order.  A rule that
    wraps goes on at the column its DO started in; only that column is read,
    so a side column's own wrap is not glued on (FW01's W3 used to end "on the")."""
    rows, col = [], None
    for line in text.splitlines():
        hit = _COUNSEL.match(line)
        if hit:
            rows.append({"id": hit.group(1), "do": hit.group(2) == "DO", "text": hit.group(3).strip()})
            col = hit.start(2)
        elif col and not line[:col].strip() and line[col:col + 1].strip():
            rows[-1]["text"] += " " + re.split(r"\s{2,}", line[col:].strip())[0]
        else:
            col = None
    for row in rows:
        row["text"] = row["text"].rstrip(".")
    return rows


def counsel_rules(text: str) -> list[str]:
    """Acceptance rules implied by the counsel: every DO NOT becomes a 'does not …' rule.

    Quote the phrase to ban ("does not say 'urgent'") and it compiles to an
    ``excludes`` check; left unquoted, the reviewer judges it (semantic)."""
    return [f"does not {row['text'][0].lower() + row['text'][1:]}" for row in counsel_lines(text) if not row["do"]]


def draft_request_path(folder: Path, stem: str) -> Path:
    return plan_folder(folder) / f"{stem}-draft-request.md"


def request_draft(folder: Path, stem: str, goal: dict, insight_rows: list[dict], missing: int,
                  actor: str = "") -> dict:
    """Ask the agent to draft the missing Design Items: one request file the queue runner reads."""
    if missing < 1:
        raise ActionError("the register already has every design the Brief asks for")
    path = draft_request_path(folder, stem)
    if path.is_file():
        raise ActionError(f"a draft request is already open: {path.name}")
    lines = [f"# draft request · {stem}", "",
             f"asked-by: {actor or 'person'}", f"asked-at: {_now()}", f"items: {missing}",
             f"goal: {goal.get('sentence') or '(no Brief line)'}", ""]
    if goal.get("row"):
        row = goal["row"]
        lines += [f"venue: {row['venue']}", f"audience: {row['audience']}", f"job: {row['job']}", ""]
    lines.append("## insights to draw on")
    lines.append("")
    if insight_rows:
        for r in insight_rows:
            lines.append(f"- {r.get('word', r.get('role', 'insight'))} · {r.get('path', r.get('name', ''))}"
                         + (f" · {r['signed']}" if r.get("signed") else ""))
            if r.get("finding"):
                lines.append(f"  finding: {r['finding']}")
            if r.get("consequence"):
                lines.append(f"  then: {r['consequence']}")
            for c in r.get("counsel") or []:
                lines.append(f"  {'DO' if c['do'] else 'DO NOT'} {c['text']}")
    else:
        lines.append("- none · design from the Brief only")
    lines += ["", "## the agent writes",
              "", f"{missing} new Design Item blocks appended to the register through `design_actions.add_item`,",
              "each with its own goal, stance, basis, expected, falsified, evidence line, and acceptance rules",
              "(every DO NOT above becomes a rule). Then this file is removed.", ""]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    return {"request": path.as_posix(), "items": missing}


def open_draft_request(folder: Path, stem: str) -> dict | None:
    path = draft_request_path(folder, stem)
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    field = lambda key: (re.search(rf"(?m)^{key}:\s*(.*)$", text) or [None, ""])[1]
    return {"path": path, "items": int(field("items") or 0), "asked_by": field("asked-by"), "asked_at": field("asked-at")}
