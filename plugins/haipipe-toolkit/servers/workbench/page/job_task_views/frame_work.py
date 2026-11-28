"""Work: the Jobs, their Tasks, each Task's Runs and what each Run found, one tree."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlencode

from live.frame_base import (ROUTE, VANILLA, _block_above, _e, _link, _reader, _rel, _title, children, face, href,
                             pop, runs_of)
from live.frame_tasks import task_card, task_type


# ── Work: the Jobs, their Tasks, each Task's Runs and what each Run found, one tree (JL 261012: "for the work, I
# want it can show the job to the task to the run results, show all the content. and there are special tasks
# that human need to interact with as well") ────────────────────────────────────────────────────────────────
def task_action(task: Path, root: Path, theme=None):
    """(label, href) when a person works inside this Task, else None: the theme's own rule (a labeling Task's
    rounds), or a draft a person writes (its face says `task-type: draft`), opened on its Work, at the step that
    waits (b32 s41)."""
    theme = theme or VANILLA
    if theme.task_action:
        got = theme.task_action(task, root)
        if got:
            return got
    if task_type(task) == "draft":
        return "✎ Write", href(task, root, theme, "Work Details")
    return None


def _short_title(md: Path | None, name: str) -> str:
    """A face's title without the folder's own name or tag in front ("t00_abstract · Abstract" -> "Abstract")."""
    title = _title(md) if md else ""
    for lead in (name, name.split("_", 1)[0]):
        title = re.sub(rf"^{re.escape(lead)}\b\s*[·:\-–]?\s*", "", title, flags=re.I) or title
    return "" if title == name else title


def _run_passes(p: Path, root: Path) -> str:
    """A soft Run's passes (passes/pNN-MMDD/pass.md), newest last, each a link to its pass; with none, what its
    card says it wrote (`writes:`, relative to its scope, the folder whose runs/ holds it)."""
    passes = sorted(d for d in (p / "passes").iterdir() if d.is_dir()) if (p / "passes").is_dir() else []
    links = [pop(_reader(d / "pass.md", root), d.name, d.name) if (d / "pass.md").is_file() else _e(d.name)
             for d in passes]
    if links:
        return f'<div class=work-files>passes: {" · ".join(links)}</div>'
    card = (p / "run.yaml").read_text(encoding="utf-8", errors="ignore") if (p / "run.yaml").is_file() else ""
    m = re.search(r"(?ms)^writes:\s*\n((?:\s*-\s.*\n?)+)", card)
    scope = p.parent.parent
    block = _block_above(scope) or scope
    wrote = []
    for w in (re.findall(r"-\s*(.+)", m.group(1)) if m else []):
        target = (scope / w.strip().strip("'\"")).resolve()
        try:
            wrote.append(target.relative_to(block.resolve()).as_posix() + ("/" if w.strip().endswith("/") else ""))
        except ValueError:
            wrote.append(w.strip())
    return (f'<div class=work-files>wrote: {" · ".join(f"<code>{_e(x)}</code>" for x in wrote[:4])}</div>' if wrote
            else '<div class="work-files mut">no pass yet</div>')


def _run_line(run: dict, root: Path) -> str:
    """One Run: its name, kind and type, status, then what it found: a hard Run's headline and result/ files, a
    soft Run's passes."""
    p = run["path"]
    res = next((p / d for d in ("result", "results") if (p / d).is_dir()), None) if p.is_dir() else None
    head = ""
    if res and (res / "headline.txt").is_file():
        head = (res / "headline.txt").read_text(encoding="utf-8", errors="ignore").strip().splitlines()[0][:240] \
            if (res / "headline.txt").read_text(encoding="utf-8", errors="ignore").strip() else ""
    files = sorted(f for f in res.rglob("*") if f.is_file() and not f.name.startswith(".")) if res else []
    link = lambda f: pop(_reader(f, root) if f.suffix == ".md" else "/" + _rel(f, root), f.name,
                         f.relative_to(res).as_posix())
    shown = " · ".join(link(f) for f in files[:6]) + (f" · +{len(files) - 6} more" if len(files) > 6 else "")
    status = run["status"] if run["status"] not in ("—", "null", "None") else ""
    rtype = run["type"] if run["type"] not in ("null", "None", "") else ""
    return (f'<li><code>{_e(run["run"])}</code> <span class=mut>{_e(run["kind"])}{" · " + _e(rtype) if rtype else ""}</span>'
            + (f' <span class="st st-{_e(status)}">{_e(status)}</span>' if status else "")
            + (f'<div class=work-head>{_e(head)}</div>' if head else "")
            + (_run_passes(p, root) if run["kind"] == "soft" and p.is_dir() else
               f'<div class=work-files>result/: {shown}</div>' if shown else
               ('<div class="work-files mut">no result/ yet</div>' if p.is_dir() else ""))
            + '</li>')


def _work_runs(folder: Path, root: Path) -> str:
    runs = runs_of(folder)
    if not runs:
        return '<p class="mut work-none">No Runs yet.</p>'
    return '<ul class=work-runs>' + "".join(_run_line(r, root) for r in runs) + '</ul>'


def _theme_meta(theme, folder: Path, root: Path) -> str:
    """The theme's own words on a Work card (Theme.work_meta), as ' · words', or ""."""
    try:
        extra = theme.work_meta(folder, root) if theme is not None and theme.work_meta else ""
    except Exception:                            # a theme's words never break the base's tree
        extra = ""
    return f" · {extra}" if extra else ""


def _work_task(task: Path, root: Path, theme, open_: bool = False) -> str:
    md, runs = face(task), runs_of(task)
    act = task_action(task, root, theme)
    button = f'<a class=work-act href="{_e(act[1])}">{_e(act[0])}</a> ' if act else ""
    title = _short_title(md, task.name)
    meta = ((f'{_e(title)} · ' if title else "") + f'{len(runs)} Run{"s" * (len(runs) != 1)}'
            + _theme_meta(theme, task, root))
    return (f'<details class="topic work-task{" work-human" if act else ""}"{" open" if open_ else ""}><summary>'
            f'<span class=related-head><b>{_e(task.name)}</b><br><span class=topic-meta>{meta}</span></span>'
            f'<span class=topic-pop>{button}{_link(ROUTE + "?" + urlencode({"path": _rel(task, root)}), "↗")}</span>'
            f'</summary><div class=work-body>{task_card(task, root, getattr(theme, "name", ""))}'
            f'{_work_runs(task, root)}</div></details>')


def _work_job(job: Path, root: Path, theme, open_: bool = False) -> str:
    md, tasks = face(job), children(job, "Job")
    human = sum(1 for t in tasks if task_action(t, root, theme))
    own = runs_of(job)
    n = sum(len(runs_of(t)) for t in tasks) + len(own)
    title = _short_title(md, job.name)
    meta = ((f'{_e(title)} · ' if title else "")
            + f'{len(tasks)} Task{"s" * (len(tasks) != 1)} · {n} Run{"s" * (n != 1)}'
            + (f' · {human} for a person ✎' if human else "") + _theme_meta(theme, job, root))
    body = "".join(_work_task(t, root, theme) for t in tasks)
    if own:
        body += '<p class=work-sub>the Job\'s own Runs</p>' + _work_runs(job, root)
    try:
        body += theme.work_body(job, root) if theme is not None and theme.work_body else ""
    except Exception:                            # a theme's part never breaks the base's tree
        pass
    return (f'<details class="topic work-job"{" open" if open_ else ""}><summary>'
            f'<span class=related-head><b>{_e(job.name)}</b><br><span class=topic-meta>{meta}</span></span>'
            f'<span class=topic-pop>{_link(ROUTE + "?" + urlencode({"path": _rel(job, root)}), "↗")}</span></summary>'
            f'<div class=work-body>{body or "<p class=mut>No Tasks yet.</p>"}</div></details>')


def work_tree(level: str, folder: Path, root: Path, theme=None, jobs: list | None = None) -> str:
    """Block: one card per Job; Job: one card per Task, open; Task: its Runs. Each opens down to its Runs and
    what each found (its headline, its result/ files); a Task a person works in carries its button (✎ Write,
    🏷 Label) and a mark."""
    theme = theme or VANILLA
    if level == "Block":                         # `jobs`: a theme's filter of them (cowork's open · waiting · done)
        jobs = children(folder, "Block") if jobs is None else jobs
        return ''.join(_work_job(j, root, theme) for j in jobs) if jobs else ""
    if level == "Job":
        tasks = children(folder, "Job")
        own = runs_of(folder)
        return (''.join(_work_task(t, root, theme, open_=True) for t in tasks)
                + (('<p class=work-sub>the Job\'s own Runs</p>' + _work_runs(folder, root)) if own else ""))
    act = task_action(folder, root, theme)
    return ((f'<p><a class=work-act href="{_e(act[1])}">{_e(act[0])}</a> <span class=mut>a person works in this '
             'Task</span></p>' if act else "") + _work_runs(folder, root))


WORK_CSS = """
/* shared looks a theme's Spaces may use (b15 s41, 261014): a scoreboard, its numbers large and labels small; cards side
   by side, one marked .key */
.stat-row{display:flex;flex-wrap:wrap;gap:10px 44px;margin:8px 0 4px}.stat-row>div{min-width:84px}
.stat-row b{display:block;font-size:30px;line-height:1.2;font-weight:700;color:var(--fg)}.stat-row span{color:var(--mut);font-size:13px}
.stat-line{font-size:16px;margin:6px 0 18px}
.card-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:10px;margin:8px 0 14px}
.card-row>div{border:1px solid var(--line);border-radius:10px;padding:10px 12px;background:var(--card);min-width:0;font-size:13.5px;line-height:1.5}
.card-row>div.key{border-color:var(--tab-on);background:var(--tab-wash)}.card-row h4{margin:0 0 2px;font-size:14px}.card-row .mut{margin:0 0 6px}
.card-row code{overflow-wrap:anywhere}
.work-body{padding:6px 14px 10px}.work-task{margin:6px 0}.work-runs{margin:6px 0 4px;padding-left:18px}
.work-runs li{margin:4px 0}.work-head{font-size:14px;margin:2px 0}.work-files{font-size:13px}
.work-files a{text-decoration:none}.work-sub{color:var(--mut);font-size:13px;margin:10px 0 2px}
.work-act{display:inline-block;padding:2px 10px;border:1px solid var(--tab-on);border-radius:6px;color:var(--tab-on);
background:var(--tab-wash);text-decoration:none;font-size:13px}.work-human>summary b::after{content:" ✎";color:var(--tab-on)}
.workflow-view .work-table-scroll{overflow-x:auto;max-width:100%}
.workflow-view .wf-table{width:100%;overflow-wrap:anywhere}
.workflow-view details{margin:10px 0}.workflow-view summary{overflow-wrap:anywhere}
.workflow-view .work-execution-table{table-layout:fixed}
.work-execution-table th:nth-child(1){width:22%}.work-execution-table th:nth-child(2){width:9%}
.work-execution-table th:nth-child(3){width:11%}.work-execution-table th:nth-child(4){width:17%}
.work-execution-table th:nth-child(5){width:9%}.work-execution-table th:nth-child(6){width:32%}
@media(max-width:720px){.workflow-view .work-table-scroll>.wf-table{min-width:700px}}
.work-none{margin:6px 0}.st{font-size:12px;padding:0 6px;border:1px solid var(--line);border-radius:999px}
.st-done,.st-ok,.st-answered{color:var(--ok);border-color:var(--ok)}.st-failed,.st-error{color:var(--miss);border-color:var(--miss)}
"""
