"""Task Block Board adapter.

The Task family owns Block, Job, Task, Run, and P-B-E-R semantics.  The Board
family owns presentation, navigation, and Board-level aggregation.  This
module is the narrow seam between them:

    Block Board -> Job group -> Task Page

Run remains an execution address and never becomes a Board Page.
"""
import re
from pathlib import Path


KIND = "task-block"
_BLOCK = re.compile(r"^(b\d{2})(?:_|$)", re.I)
_JOB = re.compile(r"^(j\d{2})(?:_|$)", re.I)
_TASK = re.compile(r"^(t\d{2})_(?P<name>[a-z0-9][a-z0-9_]*)$", re.I)


def _prefix(pattern, value):
    match = pattern.match(value)
    return match.group(1).lower() if match else ""


def _words(value):
    return re.sub(r"[_-]+", " ", value).strip()


def page_info(board_dir, page):
    """Describe one canonical Task Page, or return ``None``.

    Detection is structural.  The Page must be the same-stem Markdown file in
    a Task folder directly below one Job folder.  Prefixes supply stable
    addresses when present, but a legacy Job name does not make the Page
    disappear.
    """
    board_dir = Path(board_dir)
    page = Path(page)
    try:
        rel = page.relative_to(board_dir)
    except ValueError:
        return None
    if len(rel.parts) != 3:
        return None
    job_name, task_name, filename = rel.parts
    task_match = _TASK.fullmatch(task_name)
    if not task_match or filename != f"{task_name}.md":
        return None

    block_id = _prefix(_BLOCK, board_dir.name)
    job_id = _prefix(_JOB, job_name)
    task_id = task_match.group(1).lower()
    if block_id and job_id:
        page_id = f"{block_id}{job_id}{task_id}"
    elif job_id:
        page_id = f"{job_id}{task_id}"
    else:
        page_id = f"{job_name}.{task_id}"

    job_title = _words(_JOB.sub("", job_name, count=1)) or job_name
    job_token = job_id or job_name
    group = f"{job_token} · {job_title}"
    job_number = int(job_id[1:]) if job_id else 10_000
    task_number = int(task_id[1:])
    return {
        "id": page_id,
        "kind": "task",
        "family": "task",
        "group": group,
        "group_token": job_token,
        "job": job_name,
        "task": task_name,
        "reference": rel.as_posix(),
        "sort_key": (job_number, job_name.casefold(), task_number, task_name.casefold()),
    }


def group_token(heading):
    """Return a Task Job token from one ``## Pages`` group heading."""
    head = (heading or "").split("·", 1)[0].strip()
    match = _JOB.match(head)
    return match.group(1).lower() if match else head.casefold()
