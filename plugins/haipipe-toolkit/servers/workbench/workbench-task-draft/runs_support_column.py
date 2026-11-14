"""The Supporting Runs column of the Run Space: supporting Runs grouped by the
Job and Task that made them, one card per group (moved verbatim from runs.py).
"""
from __future__ import annotations

import html
import re
from pathlib import Path

# runs.py imports this module after it defines these helpers, so load it through live.runs.


def _support_group(row: dict) -> tuple[str, str]:
    """Return a stable Task-level grouping key and short reader label."""
    value = str(row.get("compact_id") or row.get("global_id") or row.get("run_id", ""))
    match = re.search(r"b(\d+)j(\d+)t(\d+)(?:r\d+)?", value.replace(".", ""), re.I)
    if not match:
        return "unassigned", "Unassigned"
    block, job, task = match.groups()
    return f"b{block}j{job}t{task}", f"T{int(task):02d}"


def _support_group_detail(group: dict, root: Path, page_src: Path,
                          selected_run: str = "") -> str:
    """Keep the Task card compact while retaining every child Result on demand."""
    members = []
    for row in group["rows"]:
        member_label = "%s · %s" % (row.get("run_id", "Run"), _run_action(row))
        opened = " open" if row.get("run_id") == selected_run else ""
        members.append(
            '<details class=support-member%s><summary><code>%s</code></summary>%s</details>' %
            (opened, html.escape(member_label), _detail(row, root, page_src))
        )
    return '<div class=support-group-detail>%s</div>' % "".join(members)


def _support_groups(rows: list[dict]) -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = {}
    for row in rows:
        key, _label = _support_group(row)
        groups.setdefault(key, []).append(row)
    return groups


def _support_column(title: str, rows: list[dict], root: Path, page_src: Path,
                   selected_run: str = "") -> str:
    groups = _support_groups(rows)
    if not groups:
        return '<section class=support-column><h3>%s</h3><div class=lane-empty>No %s Run yet.</div></section>' % (
            html.escape(title), html.escape(title))
    cards = []
    for index, (key, members) in enumerate(sorted(groups.items())):
        _group_key, label = _support_group(members[0])
        group_id = f"support-{title.lower()}-{index}"
        expanded = bool(selected_run and any(row.get("run_id") == selected_run for row in members))
        status = min((row.get("status", "Held") for row in members),
                     key=lambda value: _state_order().get(value, 9))
        action = _short_text(members[0].get("outcome") or members[0].get("target") or
                             "%d supporting results" % len(members))
        count_label = "Run" if len(members) == 1 else "Runs"
        cards.append(
            '<article class=run-card><div class=run-card-summary data-key="%s" data-run="%s" '
            'tabindex="0" role="button" aria-expanded="%s">'
            '<div class=run-card-name>%s · %d %s</div>'
            '<span class="run-state-dot %s" title="%s" aria-label="Status: %s">●</span>'
            '<div class=run-card-action>%s</div></div>'
            '<div class=run-card-detail data-key="%s"%s>%s</div></article>' % (
                html.escape(group_id), html.escape(members[0].get("run_id", "")),
                "true" if expanded else "false", html.escape(label), len(members), count_label,
                html.escape(status.lower()), html.escape(status), html.escape(status),
                html.escape(action), html.escape(group_id), "" if expanded else " hidden",
                _support_group_detail({"rows": members}, root, page_src, selected_run),
            )
        )
    return '<section class=support-column><h3>%s</h3><div class=run-cards>%s</div></section>' % (
        html.escape(title), "".join(cards))
# looked up when called, never at import: the old module re-exports this file's names, so either can be imported first
def _detail(*args, **kwargs):
    from live.runs import _detail as real
    return real(*args, **kwargs)


def _run_action(*args, **kwargs):
    from live.runs import _run_action as real
    return real(*args, **kwargs)


def _short_text(*args, **kwargs):
    from live.runs import _short_text as real
    return real(*args, **kwargs)


def _state_order():
    from live.runs import _STATE_ORDER
    return _STATE_ORDER
