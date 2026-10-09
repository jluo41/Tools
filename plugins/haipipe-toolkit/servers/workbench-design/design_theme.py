"""The design theme on the base frame (servers/workbench/frame.py): only what differs from vanilla.

The design ladder (Tools/blueprints/b12_theme_design, s01-design; the contract is
skills/2_theme/design/haipipe-design/ref/design-ladder.md):

    Block  bNN_<app>/                 one application, one channel: its goal list, theory, shared rules
    Job    jNN_<goal>_by-<method>/    one goal done by one design method, returning N designs
    Task   tNN_d<NN>_<slug>/          one design: Design · Rationale · Evaluation, its elements.yaml
    Run    runs/                      commission (soft) and generate (hard) at the Job; verify (hard)
                                      and revise (soft) at each design

b12's ladder as drawn 261007 (s11 · s12 · s13: a Job `jNN_<goal>_<design-method>/` pinning a goal, a registered
method version M01 – M05 and an inputs version on its face) is read by design_reader.py and drawn by design_views.py
at every level; the layout below stays for a Block whose Jobs still read `_by-<method>`.

A folder that is not on this ladder (an older Design Board with 0-BR-brief/ · 1-P-principle/ ·
2-Design/, or any other Block under a designs/ folder) gets nothing from here: it reads as vanilla,
and the older board keeps its own workbench (/_board/design-board).
"""
from __future__ import annotations

import re
from pathlib import Path

from live import design_reader as DR
from live import design_views as DV
from live.frame import ROUTE, Space, Theme, chain, children, face, href
from live.frame import esc as _e, fields as _fields, link as _link, reader as _reader, rel as _rel, table as _table
from urllib.parse import urlencode

# the 13 methods by family (servers/workbench-design/guide/method.md § 2.3), keyed by the folder's slug
FAMILY = {**{m: "Goal Only" for m in ("goal", "principle", "exploring", "slots")},
          **{m: "External" for m in ("theory", "implementation")},
          **{m: "Internal" for m in ("insight", "precedent", "revising", "tailoring", "theory-and-insight",
                                     "user-test", "co-design")}}
FAMILIES = ("Internal", "External", "Goal Only")      # Internal first: where an insight Block steers
STATES = ("passed", "verify", "revise")
DESIGN_SKILLS = ["haipipe-design", "haipipe-design-unit"]


def _kind(prompt: str, label: str) -> dict:
    return {"label": label, "prompt": prompt, "skills": DESIGN_SKILLS}


BLOCK_RUNS = (_kind("/haipipe-design add a goal × method Job to {folder}", "Add a goal × method"),
              _kind("/haipipe-design-goal set the shared rules of {folder}", "Set shared rules"),
              _kind("/haipipe-design plan the test of {folder}", "Plan the test"))
JOB_RUNS = (_kind("/haipipe-design commission {folder}", "Commission"),
            _kind("/haipipe-design-unit generate N designs for {folder}", "Generate N"),
            _kind("/haipipe-design-unit verify every design of {folder}", "Verify all"),
            _kind("/haipipe-design compare {folder} with its sibling Jobs (same goal, other methods)",
                  "Compare methods"))
TASK_RUNS = (_kind("/haipipe-design-unit verify {folder}", "Verify"),
             _kind("/haipipe-design-unit revise {folder} with feedback", "Revise"))


def method_of(job: Path) -> str:
    """The method slug of a Job, from its folder name (jNN_<goal>_by-<method>)."""
    m = re.search(r"_by-([a-z-]+)$", job.name)
    return m.group(1) if m else ""


def is_design_job(folder: Path) -> bool:
    return folder.name.startswith("j") and bool(method_of(folder))


def _sections(md: Path | None) -> dict:
    """{heading: text} of a face's ## sections."""
    if not md:
        return {}
    text = md.read_text(encoding="utf-8", errors="ignore")
    return {m.group(1).strip(): m.group(2).strip()
            for m in re.finditer(r"(?ms)^##\s+(.+?)\n(.*?)(?=^##\s|\Z)", text)}


def _field(md: Path | None, key: str) -> str:
    return dict(_fields(md, (key,))).get(key, "") if md else ""


def _go(folder: Path, root: Path, label: str) -> str:
    return _link(ROUTE + "?" + urlencode({"path": _rel(folder, root), "theme": "design"}), label)


def _elements(task: Path) -> list:
    """The element record of one design (elements.yaml): [{element, words, from, changed, ...}]."""
    path = task / "elements.yaml"
    if not path.is_file():
        return []
    try:
        import yaml
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    except Exception:
        return []
    return data if isinstance(data, list) else data.get("elements", []) if isinstance(data, dict) else []


def _state(task: Path) -> str:
    return _field(face(task), "state") or "draft"


def _message(task: Path) -> str:
    design = _sections(face(task)).get("Design", "")
    return design.splitlines()[0].strip() if design else ""


# ── Block: one application ──────────────────────────────────────────────────────────────────────
def _block(folder: Path, root: Path, sub: str) -> dict:
    jobs = [j for j in children(folder, "Block") if is_design_job(j)]
    if not jobs and not (folder / "design-goal.md").is_file():
        return {}
    out = {}
    d_sub = sub if sub in ("Goal list", "Theory", "Rules") else "Goal list"
    files = {"Theory": folder / "design-theory.md", "Rules": folder / "design-goal.md"}
    if d_sub == "Goal list":
        goals = sorted({j.name.split("_by-")[0].split("_", 1)[1] for j in jobs})
        html = _table(("goal", "Jobs (one per method)"),
                      [(_e(g), " · ".join(_go(j, root, method_of(j)) for j in jobs if f"_{g}_by-" in j.name))
                       for g in goals])
    else:
        p = files[d_sub]
        html = (f'<p>{_link(_reader(p, root), p.name)}</p>' if p.is_file()
                else f'<p class=mut>No {_e(p.name)} yet.</p>')
    out["Description"] = Space(html=html, subspaces=("Goal list", "Theory", "Rules"), open=d_sub)

    w_sub = sub if sub in ("All",) + FAMILIES else "All"
    rows = []
    for j in jobs:
        fam = FAMILY.get(method_of(j), "—")
        if w_sub not in ("All", fam):
            continue
        tasks = children(j, "Job")
        passed = sum(_state(t) in ("passed", "released") for t in tasks)
        rows.append((_go(j, root, j.name), _e(method_of(j)), _e(fam), _e(f"{passed} of {len(tasks)}"),
                     _e(_field(face(j), "state") or "—")))
    out["Work Details"] = Space(html=_table(("Job: goal × method", "method", "family", "passed", "state"), rows),
                                subspaces=("All",) + FAMILIES, open=w_sub, run_types=BLOCK_RUNS[:1])
    out["Runs"] = Space(run_types=BLOCK_RUNS[1:])
    return out


# ── Job: one goal × one method → N designs ─────────────────────────────────────────────────────
def _job(folder: Path, root: Path, sub: str) -> dict:
    if not is_design_job(folder):
        return {}
    md, tasks, out = face(folder), children(folder, "Job"), {}
    d_sub = sub if sub in ("Goal", "Method") else "Goal"
    if d_sub == "Method":
        card = folder / "method.md"
        parts = _sections(card)
        html = ("".join(f"<h2>{_e(h)}</h2><pre>{_e(t)}</pre>" for h, t in parts.items()) if parts
                else '<p class=mut>No method.md yet: the method card, frozen before the first Generate.</p>')
    else:
        rows = [(_e(k), _e(v)) for k, v in _fields(md, ("goal", "method", "family", "n", "state", "close"))] if md else []
        goal = _sections(md).get("Goal", "")
        html = _table(("field", "value"), rows) + (f"<pre>{_e(goal)}</pre>" if goal else "")
    out["Description"] = Space(html=html, subspaces=("Goal", "Method"), open=d_sub,
                               run_types=(_kind("/haipipe-design-goal frame the goal of {folder}", "Set the goal"),))

    a_sub = sub if sub in ("Elements", "Evaluation") else "Elements"
    if a_sub == "Elements":                   # the element matrix: which elements the N designs changed
        count, sources = {}, {}
        for t in tasks:
            for e in _elements(t):
                name = str(e.get("element", "?"))
                count[name] = count.get(name, 0) + (1 if e.get("changed") else 0)
                sources.setdefault(name, set()).add(str(e.get("from", "—")))
        html = _table(("element", "changed", "from", ""),
                      [(_e(n), _e(f"{c} of {len(tasks)}"), _e(" · ".join(sorted(sources[n]))), "★" if c else "")
                       for n, c in count.items()])
    else:
        html = _table(("design", "state", "evaluation"),
                      [(_go(t, root, t.name), _e(_state(t)),
                        _e((_sections(face(t)).get("Evaluation", "").splitlines() or ["—"])[0])) for t in tasks])
    out["Audience Report"] = Space(html=html, subspaces=("Elements", "Evaluation"), open=a_sub,
                                   run_types=JOB_RUNS[3:])

    w_sub = sub if sub in ("All",) + STATES else "All"
    rows = [(_go(t, root, t.name), _e(_message(t) or "—"), _e(_state(t))) for t in tasks
            if w_sub == "All" or _state(t) == w_sub]
    out["Work Details"] = Space(html=_table(("design", "the design, word for word", "state"), rows),
                                subspaces=("All",) + STATES, open=w_sub, run_types=JOB_RUNS[1:3])
    out["Runs"] = Space(run_types=JOB_RUNS[:3])
    out["Delivery"] = Space(run_types=(_kind("/haipipe-design release the passed designs of {folder}", "Release"),))
    return out


# ── Task: one design ────────────────────────────────────────────────────────────────────────────
def _task(folder: Path, root: Path, sub: str) -> dict:
    if not is_design_job(folder.parent):
        return {}
    parts, out = _sections(face(folder)), {}
    d_sub = sub if sub in ("Design", "Rationale", "Evaluation") else "Design"
    text = parts.get(d_sub, "")
    out["Description"] = Space(html=f"<pre>{_e(text)}</pre>" if text else f'<p class=mut>No {_e(d_sub)} section yet.</p>',
                               subspaces=("Design", "Rationale", "Evaluation"), open=d_sub)
    rows = [(_e(e.get("element", "?")), _e(e.get("words", "")), _e(e.get("from", "—")), _e(e.get("source", "")),
             _e(e.get("thinking", "—")), _e(e.get("because", ""))) for e in _elements(folder)]
    out["Work Details"] = Space(html=_table(("element", "words", "from", "source", "thinking", "because"), rows)
                                if rows else '<p class=mut>No elements.yaml yet: one entry per element.</p>',
                                subspaces=("Elements",), open="Elements", run_types=TASK_RUNS[1:])
    out["Runs"] = Space(run_types=TASK_RUNS)
    return out


# ── an older board on the frame: its method groups and Design Folders (JL 261008: "the frame has no display for
# design items") ──────────────────────────────────────────────────────────────────────────────────
# An older DesignBoard (B00_DesignBoard-<name>/ with 2-Design[-M<NN>-<slug>]/Design-NN-<slug>/) reads on the frame as
# Block · Job (a method group) · Task (one Design Folder). A Task's Work Details and Delivery frame the older page's
# own Design and Delivery Spaces in place (one card per design: Design · Rationale · Evaluation), as the frame does
# for a Page's views; its Description stays the face. Read-only, like every design view.
OLDER = {"Job": r"^2-Design(-M\d\d-[a-z0-9-]+)?$", "Task": r"^Design-\d\d-"}


def _older(folder: Path) -> bool:
    """A folder of an older DesignBoard: a method group, a Design Folder, or the Block holding them."""
    if re.match(OLDER["Job"], folder.name) or re.match(OLDER["Task"], folder.name):
        return True
    try:
        return (folder / "board.md").is_file() and any(re.match(OLDER["Job"], p.name) for p in folder.iterdir())
    except OSError:
        return False


def _old_page(folder: Path, root: Path, space: str) -> str:
    """The older Design page's Space, framed in place, with a link to open it on its own."""
    md = face(folder) or folder
    src = "/_board/design?" + urlencode({"path": _rel(md, root), "space": space})
    return (f'<iframe class=page-view src="{_e(src)}" loading=lazy title="{_e(space)}"></iframe>'
            f'<p class=mut>{_link(src, "open the older Design page on its own ↗")}</p>')


def _designs_of(group: Path) -> list:
    return sorted(p for p in group.iterdir() if p.is_dir() and re.match(OLDER["Task"], p.name))


def _units(design: Path) -> int:
    return sum(1 for p in (design / "units").iterdir() if p.is_dir()) if (design / "units").is_dir() else 0


def _older_spaces(level: str, folder: Path, root: Path, sub: str) -> dict:
    if level == "Task":
        return {"Work Details": Space(html=_old_page(folder, root, "design"), subspaces=("Designs",), open="Designs"),
                "Delivery": Space(html=_old_page(folder, root, "delivery"))}
    if level == "Job":
        rows = [(_go(d, root, d.name), _e(str(_units(d))), _e(_field(face(d), "status") or "—"))
                for d in _designs_of(folder)]
        return {"Work Details": Space(html=_table(("Design Folder (one design task)", "design units", "status"), rows)
                                      if rows else '<p class=mut>No Design Folder in this method group yet.</p>')}
    groups = sorted(p for p in folder.iterdir() if p.is_dir() and re.match(OLDER["Job"], p.name))
    rows = [(_go(g, root, g.name), " · ".join(_go(d, root, d.name.split("-", 2)[1] if d.name.count("-") > 1 else d.name)
                                            for d in _designs_of(g)) or "—") for g in groups]
    board = "/_board/design-board?" + urlencode({"path": _rel(folder / "board.md", root)})
    return {"Work Details": Space(html=_table(("method group", "its Design Folders"), rows) +
                                 f'<p class=mut>{_link(board, "the older board page ↗")}</p>')}


def spaces(level, folder, root, sub):
    folder, root = Path(folder).resolve(), Path(root).resolve()
    if _older(folder):
        return _older_spaces(level, folder, root, sub)
    block = chain(folder, root).get("Block")
    if block is not None and DR.is_ladder(block):      # b12's ladder (s11 · s12 · s13): every level from the folders
        def link(space, s, target=None):
            return href(Path(target) if target else folder, root, THEME, space, s)
        view = {"Block": DV.block_spaces, "Job": DV.job_spaces, "Task": DV.task_spaces}.get(level)
        return view(folder, root, sub, link) if view else {}
    return {"Block": _block, "Job": _job, "Task": _task}.get(level, lambda *a: {})(folder, root, sub)


# every button named by the Run it makes, run-<type>-<target> (haipipe-run ref/run-types-by-space.md rule 6; the names
# are the ladder's, haipipe-design/ref/design-ladder.md § Runs). Commission and Compare methods make no ladder Run.
RUN_NAMES = {"Add a goal × method": "run-add-job-j<NN>", "Set shared rules": "run-setup-rules",
             "Plan the test": "run-plan-test-<app>", "Set the goal": "run-setup-goal-j<NN>",
             "Generate N": "run-generate-d<NN>", "Verify all": "run-verify-d<NN>-v<k>",
             "Verify": "run-verify-d<NN>-v<k>", "Revise": "run-revise-d<NN>", "Release": "run-release-j<NN>"}

# the Task ▾ dropdown on the ladder (s13): each Task named by its step, grouped by the method's step; a design reads
# "Task · d04 · reason-then-ask" (its short name, born with its idea in t00). The frame draws the groups (b03, 261008).
STEP_GROUPS = {"t00": ("Task · t00 · reason ideas", "② Reason ideas"), "t99": ("Task · t99 · review whole", "⑤ Review whole")}


def option(folder: Path):
    """(label, group) for a ladder Task in the Task ▾ dropdown, or None (the folder's name)."""
    if not re.match(r"^t\d+_", folder.name) or not DR.is_job(folder.parent):
        return None
    kind = DR.kind_of(folder)
    if kind in STEP_GROUPS:
        return STEP_GROUPS[kind]
    m = DR.DESIGN_TASK.match(folder.name)
    f = DR.front(DR.face(folder))
    short = str(f.get("name") or (m.group(3) if m else folder.name))
    dropped = " · dropped" if str(f.get("state", "")) == "dropped" else ""
    return (f"Task · d{m.group(2)} · {short}{dropped}" if m else folder.name, "③ Conduct process")


THEME = Theme(name="design", label="Design", icon="🎨", guide="design",
              level_names={"Block": "Design Board", "Job": "Design Job", "Task": "Design Task"}, spaces=spaces,
              run_names=RUN_NAMES, level_patterns=OLDER, option=option)
