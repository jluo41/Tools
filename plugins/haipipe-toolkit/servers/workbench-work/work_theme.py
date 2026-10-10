"""The work theme on the base frame (servers/workbench/frame.py): only what differs from vanilla.

A work Task (s13, Tools/blueprints/b01_haipipe-toolkit/j03_project_workbench/studio/s13-task-variants): Description is Scope · Plan,
Audience Report is Draft · Report, Work Details is Code · Review · Notebooks; its Runs are grouped
by type by the frame itself. The Block and Job levels read as vanilla (Questions as
Question │ Work │ Report, the child Jobs and Tasks). Its Guide is the `work` family (once `task`, still an alias).
"""
import re
from pathlib import Path

from live.frame import Space, Theme, esc as _e, face, link as _link, reader as _reader, table as _table

TASK_RUNS = ({"label": "Plan a Task", "prompt": "/haipipe-task plan {folder}"},
             {"label": "Build the Task", "prompt": "/haipipe-task build {folder}"},
             {"label": "Run a Task", "prompt": "/haipipe-task run {folder}"},
             {"label": "Check a Task", "prompt": "/haipipe-task check {folder}"})


def _section(md: Path, word: str) -> str:
    """The text under the first heading that names `word`, as plain lines."""
    text = md.read_text(encoding="utf-8", errors="ignore")
    m = re.search(rf"(?ims)^#+[^\n]*{word}[^\n]*\n(.*?)(?=^#+ |\Z)", text)
    return m.group(1).strip() if m else ""


LEFTOVERS = {"__pycache__", "catboost_info", ".ipynb_checkpoints"}    # build leftovers, never listed


def _files(folder: Path, root: Path, pattern: str) -> list:
    return [(_link(_reader(p, root), p.relative_to(folder).as_posix()) if p.suffix == ".md"
             else _e(p.relative_to(folder).as_posix()), _e(p.stat().st_size))
            for p in sorted(folder.glob(pattern))
            if p.is_file() and p.suffix != ".pyc" and not LEFTOVERS & set(p.relative_to(folder).parts)]


def spaces(level, folder, root, sub):
    if level != "Task":
        return {}
    md = face(folder)
    out = {}
    plan = _section(md, "plan") if md else ""
    desc_sub = sub if sub in ("Scope", "Plan") else "Scope"
    out["Description"] = Space(
        html=(f"<h2>Plan</h2><pre>{_e(plan)}</pre>" if plan else '<p class=mut>No Plan section in its face yet.</p>')
        if desc_sub == "Plan" else "",
        subspaces=("Scope", "Plan"), open=desc_sub, run_types=TASK_RUNS[:1])
    ar_sub = sub if sub in ("Draft", "Report") else "Report"
    drafts = _files(folder, root, "draft/*.md")
    out["Audience Report"] = Space(
        html=_table(("draft", "bytes"), drafts) if ar_sub == "Draft" else
        (f'<p>The report is its face: {_link(_reader(md, root), md.name)}</p>' if md else ""),
        subspaces=("Draft", "Report"), open=ar_sub,
        run_types=({"label": "Write the report", "prompt": "/haipipe-task report {folder}"},))
    wd_sub = sub if sub in ("Code", "Review", "Notebooks") else "Code"
    body = {"Code": lambda: _table(("file", "bytes"), _files(folder, root, "scripts/**/*") + _files(folder, root, "workflow/**/*")
                                   + _files(folder, root, "tests/**/*")),
            "Review": lambda: (f'<p>{_link(_reader(folder / "CODE_REVIEW.md", root), "CODE_REVIEW.md")}</p>'
                               if (folder / "CODE_REVIEW.md").is_file() else '<p class=mut>No review yet.</p>'),
            "Notebooks": lambda: _table(("notebook (generated)", "bytes"), _files(folder, root, "notebooks/*.ipynb"))}
    out["Work Details"] = Space(html=body[wd_sub](), subspaces=("Code", "Review", "Notebooks"), open=wd_sub,
                                run_types=TASK_RUNS[1:2] + ({"label": "Review the Task code",
                                                             "prompt": "/haipipe-task review {folder}"},))
    out["Runs"] = Space(run_types=TASK_RUNS[2:])
    return out


# each button's Run (haipipe-run rule 6); a hard Run keeps its rNN_ name
RUN_NAMES = {"Plan a Task": "run-plan-<tNN>", "Build the Task": "run-build-<tNN>", "Run a Task": "rNN_<slug>",
             "Check a Task": "run-check-<tNN>", "Write the report": "run-write-<tNN>",
             "Review the Task code": "run-review-code-<tNN>"}

THEME = Theme(name="work", label="Work", icon="📋", guide="work", spaces=spaces, run_names=RUN_NAMES)
