"""BJTR Block Board adapter.

The Task family owns Block, Job, Task, Run, and P-B-E-R semantics.  The Board
family owns presentation, navigation, and Board-level aggregation.  This
module is the narrow seam between them:

    Task/Discovery Block Board -> Job group -> Task Page

Run remains an execution address and never becomes a Board Page.
"""
import re
from pathlib import Path


KINDS = {"task-block", "discovery-block"}
_BLOCK = re.compile(r"^(b\d{2})(?:_|$)", re.I)
_JOB = re.compile(r"^(j\d{2})(?:_|$)", re.I)
_TASK_PREFIX = re.compile(r"^(t\d{2})_", re.I)
_TASK = re.compile(r"^(t\d{2})_(?P<name>[a-z0-9][a-z0-9_]*)$", re.I)


def _prefix(pattern, value):
    match = pattern.match(value)
    return match.group(1).lower() if match else ""


def _words(value):
    return re.sub(r"[_-]+", " ", value).strip()


def page_info(board_dir, page, family="task"):
    """Describe one canonical Task Page, or return ``None``.

    Detection is structural.  The Page must be the same-stem Markdown file in
    a Task folder directly below one Job folder.  Prefixes supply stable
    addresses when present, but a legacy Job name does not make the Page
    disappear.
    """
    if family not in {"task", "discovery"}:
        raise ValueError(f"unsupported BJTR Page family: {family}")
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
        "kind": family,
        "family": family,
        "group": group,
        "group_token": job_token,
        "job": job_name,
        "task": task_name,
        "reference": rel.as_posix(),
        "sort_key": (job_number, job_name.casefold(), task_number, task_name.casefold()),
    }


_ADDRESS_LINE = re.compile(r"(?m)^address_compact:\s*(b\d{2}j\d{2}t\d{2})\s*$", re.I)
_ADDRESS_SETEXT = re.compile(
    r"(?ms)^Address\s*\n-{3,}\s*\n\s*(b\d{2}[.]?j\d{2}[.]?t\d{2})\b", re.I)


def mounted_info(board_dir, page):
    """Describe one Task or Discovery Folder Page mounted on a generic Board.

    The Folder's own Page Face is read as it is; the Board contributes only
    an id and a place in the roster. The id is `T-<address>` or `D-<address>`,
    where the address is the Folder's declared `address_compact`, its legacy
    `Address` section, or the bNN/jNN/tNN parts of its path. The Board-relative
    path is the Page's identity on disk, because `t01_...` recurs under every
    Job. Returns ``None`` when the Page is not a mounted Folder Page.
    """
    from .common import mounted_folder_kind
    board_dir, page = Path(board_dir), Path(page)
    kind = mounted_folder_kind(page)
    if not kind:
        return None
    try:
        rel = page.relative_to(board_dir)
    except ValueError:
        return None
    try:
        text = page.read_text(encoding="utf-8")
    except OSError:
        text = ""
    found = _ADDRESS_LINE.search(text) or _ADDRESS_SETEXT.search(text)
    if found:
        compact = re.sub(r"[.]", "", found.group(1)).lower()
    else:
        parts = [_prefix(pat, part) for part in rel.parts[:-1]
                 for pat in (_BLOCK, _JOB, _TASK_PREFIX)]
        compact = "".join(x for x in parts if x) or page.stem
    letter = "T" if kind == "task" else "D"
    return {
        "id": f"{letter}-{compact}",
        "kind": kind,
        "family": kind,
        "group": "",
        "group_token": "",
        "job": "",
        "task": page.stem,
        "reference": rel.as_posix(),
        "sort_key": (10_000, rel.as_posix().casefold(), 0, ""),
    }


def group_token(heading):
    """Return a Task Job token from one ``## Pages`` group heading."""
    head = (heading or "").split("·", 1)[0].strip()
    match = _JOB.match(head)
    return match.group(1).lower() if match else head.casefold()
