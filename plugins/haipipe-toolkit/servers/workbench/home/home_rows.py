"""The SPACE Home's Block rows: one folded card per Block, its Studio topics and its Jobs with their Runs."""

from __future__ import annotations

import html
import re
from pathlib import Path
from urllib.parse import quote

from live.home_boards import KIND_ICON, home_folder_path


def block_link(card: dict[str, object], slug_counts: dict[str, int]) -> str:
    """`/w/<block>` when its slug is unique; otherwise the frame's long address (an ambiguous
    slug is a 404). Both open the base frame."""
    if card.get("linked_space"):
        return str(card["href"])
    slug = str(card.get("slug") or "")
    if slug and slug_counts.get(slug, 0) == 1:
        return "/w/" + quote(slug, safe="")
    return str(card["href"])


def _numbered(node: dict[str, object]) -> str:
    """A Block's, topic's or Job's face title, led by its folder number (b01, s01, j02) when the title lacks it
    (JL 261019: "could we show the bNN before Physician Ground Truth Tasks as well?")."""
    title = str(node.get("title") or node.get("name") or "")
    number = re.match(r"^([bsj]\d+)", str(node.get("folder") or node.get("name") or ""))
    tag = number.group(1).lower() if number else ""
    # said once: a title that starts with it (a heading-less face falls back to "b01_x") or names it elsewhere
    if number and not (title.lower().startswith(tag) or re.search(rf"\b{tag}\b", title.lower())):
        title = f"{number.group(1)} · {title}"
    return title



def _stage_pill(stage: str) -> str:
    """The workbench's stage pill (frame._topic_row): four steps, filled up to the topic's stage."""
    from live.frame import STAGES
    if stage not in STAGES:
        return '<span class="stage stage-none" title="No **Stage:** line yet">no stage</span>'
    at = STAGES.index(stage)
    steps = "".join(f'<b class="{"on" if k <= at else ""}"></b>' for k in range(len(STAGES)))
    return (f'<span class="stage stage-{stage}" title="Stage {at + 1} of {len(STAGES)}: {stage} (its **Stage:** '
            f'line)"><i class="stage-steps">{steps}</i>{stage}</span>')


def _topic_rows(topics: list[dict[str, object]]) -> str:
    """A Block's Studio topics as the workbench's Studio list draws them (JL 261012: "it is more like this ... and
    I can preview the content of the draw as well"): one folded row each, its folder name, tags, ↗ to the topic
    in the Studio and its stage; opened, its first drawing, live, loaded only then."""
    rows = []
    for topic in topics:
        name = html.escape(str(topic.get("folder") or topic.get("name") or ""))
        chips = "".join(f'<span class="chip">{html.escape(str(tag))}</span>' for tag in topic.get("tags") or [])
        draw = str(topic.get("draw") or "")
        body = (f'<iframe class="st-frame" title="{name}" data-src="{html.escape(draw, quote=True)}" '
                f'referrerpolicy="no-referrer"></iframe>' if draw else '<p class="topic-none">No drawing yet.</p>')
        rows.append(f'<details class="topic"><summary title="{html.escape(_numbered(topic), quote=True)}">'
                    f'<b>{name}</b>{f"<span class=topic-tags>{chips}</span>" if chips else ""}'
                    f'<span class="topic-pop"><a href="{html.escape(str(topic.get("href") or ""), quote=True)}" '
                    f'title="Open this topic in the Studio">↗</a></span>{_stage_pill(str(topic.get("stage") or ""))}'
                    f'</summary>{body}</details>')
    return f'<div class="topic-rows">{"".join(rows)}</div>'




def _task_runs(task: str, href: str, title: str, status: str, runs: list) -> str:
    """One Task inside an opened Job row: its name (the link), title and status, and under it its hard Runs, one
    aligned line each (mark · Run · status · finish day), as the Studio's Runs part draws them. No count or tally
    (AGENTS.md § Page words): each Run's own state is on its line."""
    name = f'<b>{html.escape(task)}</b>'
    name = f'<a href="{html.escape(href, quote=True)}">{name}</a>' if href else name
    meta = title
    pill = f'<span class="job-st job-st-{html.escape(status)}">{html.escape(status)}</span>' if status else ""
    if not runs:
        return f'<div class="rn-task">{name}<span class="rn-meta">{html.escape(meta)}</span>{pill}</div>'
    from live import frame
    return (f'<div class="rn-task">{name}<span class="rn-meta">{html.escape(meta)}</span>{pill}</div>'
            f'<div class="rn-grid">{frame.run_cells(runs)}</div>')


def _job_rows(jobs: list[dict[str, object]], runs: list = ()) -> str:
    """A Block's Jobs as rows like its Studio rows (JL 261012, on the Job cards: "could you make it to do the same?"),
    each carrying its own hard Runs (JL 261019: "put the run status under the jobs, merge the jobs and runs ... to
    save the spaces"): one folded row each, its folder name, title, ↗ to the Job and its status (no counts: each
    Run's state is on its own line inside); opened, each Task with its Runs under it, then the Job's face, read in place and loaded
    only then."""
    by_job: dict[str, dict[str, list]] = {}
    for run in runs:
        by_job.setdefault(run[0], {}).setdefault(run[1], []).append(run)
    rows = []
    for job in jobs:
        folder = str(job.get("folder") or job.get("name") or "")
        name = html.escape(folder)
        tasks = [t for t in job.get("children") or [] if t.get("level") == "Task"]
        task_runs = by_job.get(folder, {})
        status = str(job.get("status") or "")
        status = "" if status == "unknown" else status
        meta = str(job.get("title") or "")
        pill = f'<span class="job-st job-st-{html.escape(status)}">{html.escape(status)}</span>' if status else ""
        listed = "".join(_task_runs(str(t.get("folder") or ""), str(t.get("href") or ""), str(t.get("title") or ""),
                                    "" if t.get("status") in (None, "", "unknown") else str(t["status"]),
                                    task_runs.get(str(t.get("folder") or ""), [])) for t in tasks)
        known = {str(t.get("folder") or "") for t in tasks}        # Runs kept in the Job itself (the flat layout)
        listed += "".join(_task_runs(task, "", "", "", rs) for task, rs in task_runs.items() if task not in known)
        read = str(job.get("read") or "")
        body = ((f'<div class="rn-body job-runs">{listed}</div>' if listed else "")
                + (f'<iframe class="st-frame job-frame" title="{name}" data-src="{html.escape(read, quote=True)}" '
                   f'referrerpolicy="no-referrer"></iframe>' if read else '<p class="topic-none">No face yet.</p>'))
        rows.append(f'<details class="topic"><summary><b>{name}</b><span class="topic-meta">{html.escape(meta)}</span>'
                    f'<span class="topic-pop"><a href="{html.escape(str(job.get("href") or ""), quote=True)}" '
                    f'title="Open this Job">↗</a></span>{pill}</summary>{body}</details>')
    return f'<div class="topic-rows">{"".join(rows)}</div>'


def _runs_of(block: Path) -> list:
    """The Block's hard Runs (workbench frame.hard_runs), [] when the workbench is absent."""
    try:
        from live import frame
    except ImportError:
        return []
    return frame.hard_runs(block)




def _block_groups(node: dict[str, object] | None, runs: list = ()) -> tuple[str, str, str]:
    """A Block's two groups, its Studio topics (sNN) and its Jobs (jNN) with their Runs, each a list of folded rows
    as the workbench's Studio list draws them, read from the same chart data the Chart · Progress view draws.
    Returns (the groups, their counts, their words to search)."""
    topics = list((node or {}).get("studios") or [])
    jobs = [child for child in (node or {}).get("children") or [] if child.get("level") == "Job"]
    folders = {str(job.get("folder") or job.get("name") or "") for job in jobs}
    loose = [run for run in runs if run[0] not in folders]      # Runs of Tasks that sit in no listed Job

    groups = []
    for key, label, items, empty in (
            ("studio", "🧠 Studio", topics, "No Studio topics yet"),
            ("jobs", "🗂 Jobs", jobs, "No Jobs yet")):
        if key == "studio":
            body = _topic_rows(items) if items else f'<p class="block-cards-empty">{empty}</p>'
        else:
            body = _job_rows(items, runs) if items else ("" if loose else f'<p class="block-cards-empty">{empty}</p>')
            if runs:
                from live import frame
                body += (frame.runs_list(loose) if loose else "") + f'<p class="rn-legend">{html.escape(frame.RUN_LEGEND)}</p>'
        groups.append(f'<section class="block-cards" data-group="{key}"><h4 class="block-cards-head">{label}</h4>'
                      f'{body}</section>')
    counts = ""                                                  # no counts on a page (AGENTS.md § Page words)
    words = " ".join(_numbered(item) for item in topics + jobs)
    return f'<div class="block-groups">{"".join(groups)}</div>', counts, words




def _home_row(card: dict[str, object], project_name: str, href: str,
              shown: bool, node: dict[str, object] | None = None, runs: list | None = None) -> str:
    """One Block card, folded: kind emoji, title (the link that opens the Block), folder, its counts and
    the Board's state word; open, its Studio topics and its Jobs (each with its Runs) as two groups (JL 261012)."""
    kind_key = str(card["kind_key"])
    title = html.escape(_numbered(card))            # "b01 · Physician Ground Truth Tasks", its number once
    folder = html.escape(home_folder_path(card))
    icon = html.escape(KIND_ICON.get(kind_key, str(card.get("icon") or "")))
    kind_label = html.escape(kind_key.capitalize(), quote=True)
    state = html.escape(str(card.get("board_state") or ""))
    state_html = (f'<span class="home-state" title="Board state">{state}</span>'
                  if state else "")
    groups, counts, words = _block_groups(node, runs or [])
    row_search = html.escape(
        " ".join((project_name, str(card["title"]), str(card["slug"]),
                  str(card["path"]), str(card["spine"]), str(card["kind"]),
                  kind_key, str(card.get("theme") or ""), words)),
        quote=True,
    )
    hidden = "" if shown else " hidden"
    archived = ' data-archived="1"' if card.get("archived") else ""
    return (f'''<details class="home-block" data-kind="{html.escape(kind_key, quote=True)}"
  data-block-key="{html.escape(str(card["path"]), quote=True)}" data-search="{row_search}" role="listitem"{archived}{hidden}>
  <summary class="ir home-row"><span class="home-kind" role="img"
  aria-label="{kind_label}" title="{kind_label}">{icon}</span><span class="home-copy"><a class="t" href="{html.escape(href, quote=True)}">{title}</a>
  <span class="home-folder">{folder}</span></span>{counts}{state_html}</summary>
  {groups}</details>''')
