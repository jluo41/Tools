"""The labeling Task's screen: what a labeling Task shows in the frame's Spaces, by its type.

One Task type, one folder (b32 s41-D15, JL 261016: "go ahead with workbench-task-labeling"). Everything a
labeling Task shows lives in servers/workbench-labeling/workbench-task-labeling/: this layout, the engine's
Labeling workbench it opens (labeling.py: Data · Labeling · Quality · Delivery, and its write door) and that
workbench's look (assets/js/10-drawer/60-workbench-labeling.js). Its manual is the skill workbench-task-labeling.
The Block and Job levels stay in ../labeling_theme.py.

A labeling Task is one of five types, read from its face's `task-type:` line (labeling_theme.TYPES): items ·
ground truth · building · scanning · score; today's one labeling Page (`task-type: labeling`) is building and
scanning at once. The frame calls spaces() for a Task of the labeling theme only (frame.task_layouts).
"""
from __future__ import annotations

from pathlib import Path
from live.frame import Space, esc, face, rel
from live import labeling_theme as T
from live.labeling_theme import (BUILD_WORK, BY_SUB, DELIVER, NOTES, SCAN_WORK, VIEW, _block_of, _engine_job, _facts,
                                 _job_for, _open, _skill_run, _view_url, types_of)

from live.task_labeling_read import _fold, _items_facts, _kv, _not_yet
from live.task_labeling_steps import CHIPS, _items_spaces, _prompt_box


# task_labeling was split by responsibility into the modules below; an old name still answers from the one that holds it
SPLIT_INTO = ("task_labeling_steps", "task_labeling_cards", "task_labeling_read")


def __getattr__(name: str):
    """An old name (`task_labeling.<name>`, `from live.task_labeling import <name>`) answers from the sibling that holds it now."""
    import importlib
    for sibling in SPLIT_INTO:
        mod = importlib.import_module(f"live.{sibling}")
        if name in vars(mod):
            return vars(mod)[name]
    raise AttributeError(f"module 'live.task_labeling' has no attribute {name!r}")


# ── Task: building, its four Stages (b15 s42: the map ①, the screens ②–⑪) ─────────────────────────
# A Stage is a tab in Work and Report, as an items Task's steps are (s41): Operation, what a person does (the
# Stage, its Input, the prompt), then Result, what the Stage made (one card per topic, folded). Sizes are named
# by symbol until the engine writes them (n m u r b, s42-D41); each agent step shows its reading budget (👁, s42-D43).
BUILD_TABS = ("1 · Contract", "2 · Initial Labeling Definition", "3 · Rounds", "4 · Handoff")
BUILD_SKILL = "haipipe-labeling-building"


def _items_task(task: Path) -> Path | None:
    """The items Task of the same Job: the building Task's corpus."""
    return next((t for t in sorted(task.parent.iterdir()) if t.is_dir() and t != task and types_of(t) == ("items",)), None)


def _build_states(job: dict | None) -> dict:
    """Each Stage done, next, waiting on a person, or later; read from the labeling job's own record."""
    job = job or {}
    phase = str(job.get("phase") or "")[:2]
    done = {"contract": job.get("kind") not in (None, "empty", "preparing", "repair") and job.get("n_sealed") is not None,
            "definition": bool(job.get("g0")),
            "rounds": phase in ("P2", "P3", "P4", "P5"),
            "handoff": phase in ("P3", "P4", "P5")}
    states, nexted = {}, False
    for key in ("contract", "definition", "rounds", "handoff"):
        states[key] = "done" if done[key] else ("next" if not nexted else "todo")
        nexted = nexted or not done[key]
    if states["definition"] == "next" and job.get("badge") == "Confirm meaning":
        states["definition"] = "sign"                                  # a draft waits for Sign (G0)
    if states["rounds"] == "next" and job.get("kind") == "labeling":
        states["rounds"] = "ready"                                     # a round is open: rule its picks
    return states


def _n(v, sym: str) -> str:
    return f"{sym} = {v}" if isinstance(v, int) else sym


def _build_input(key: str, task: Path, root: Path, job: dict | None) -> str:
    job = job or {}
    n_dev, m = job.get("n_dev"), job.get("n_sealed")
    if key == "contract":
        it = _items_task(task)
        f = _items_facts(it, root) if it else {"done": []}
        items = (f'<code>{esc(f["metrics"].get("store") or f["manifest"].get("store"))}</code> · '
                 f'{esc(_n(f["manifest"].get("items"), "n"))} items' if f["done"] else
                 '<span class="st st-warn">the items Task first</span>')
        return _kv([("Items", "X · " + items), ("Groups", "C · from the items Task's 📍 map"),
                    ("Final exam", esc(f"S · {_n(m, 'm')} sealed, across C, never shown")),
                    ("Agent reads", "👁 0: ids and counts")])
    if key == "definition":
        return _kv([("Pool", esc(f"X∖S · {_n(n_dev, 'n − m')} items")), ("You read", "≤ r in all passes"),
                    ("Agent reads", "👁 ≤ c_ask a pass"), ("Rounds", "never draw what you read again")])
    if key == "rounds":
        t = job.get("rounds") or 0
        return _kv([("Corpus", esc(f"U · {_n(n_dev, 'u')}: 2 labels each · gold {job.get('labeled', 0)}")),
                    ("Pools", "H · L · N · HL · LN · HN · HLN"),
                    ("Guideline", esc(f"G_{t + 1}" if t else "G_1")),
                    ("Pick", "seed → retrieve over X∖S → score v(x) → read ≤ c_pick → b"),
                    ("Agent reads", "👁 ≤ c_pick to pick · ≤ c_learn to learn")])
    return _kv([("Checkpoint", esc(f"round {job.get('rounds') or 't'}, Stop signed")),
                ("Guideline", "G* = the last G_t"), ("Gold", esc(f"D* · {job.get('labeled', 0)} rulings")),
                ("Final exam", esc(f"S · {_n(m, 'm')}, still unseen")), ("Agent reads", "👁 0")])


BUILD_STAGES = (
    ("contract", "📦 Stage 1 · Contract",
     "contract: import the items, hold back the sealed set, start guideline v0."),
    ("definition", "💬 Stage 2 · Initial Labeling Definition",
     "definition: one more pass with me through the items, group by group; keep my notes; then draft the "
     "definition and stop for my Sign."),
    ("rounds", "🔁 Stage 3 · Rounds",
     "round: label U with G_t, sort it into the 7 pools, pick round t by the funnel, and stop for my Approve."),
    ("handoff", "✍️ Stage 4 · Handoff",
     "freeze: freeze the Handoff from the last checkpoint, and stop for my Sign (G*)."),
)
BUILD_CARDS = {
    "contract": ("📚 Corpus: 🔒 S · pool X∖S", "📜 Guideline G_0", "🗂 Register: 7 pools"),
    "definition": ("💬 The talk, pass by pass", "📝 Your notes and hard cases", "📜 Guideline G_1"),
    "rounds": ("📊 The 7 pools, round by round", "🏷 Your gold", "📜 Guideline G_t", "🤝 Both labelers vs you",
               "🗂 Register: open · covered · risky"),
    "handoff": ("✍️ Handoff", "📜 Guideline G*", "🏷 Your gold, D*", "🔍 Next: scanning"),
}


def _build_cards(key: str, state: str, job: dict | None) -> str:
    """A Stage's Result: one folded card per topic; the job's record where it says something, else not yet."""
    if state != "done" and not (key == "rounds" and (job or {}).get("rounds")):
        return _not_yet("Not made yet.")
    facts = _facts(job) if job else ""
    return "".join(_fold(t, "", facts if i == 0 else _not_yet("Read in the Labeling workbench.")
                         + (f'<p>{_open(_view_url(job, VIEW[{"contract": "contract", "definition": "definition", "rounds": "rounds", "handoff": "handoff"}[key]]))}</p>'
                            if job else ""))
                   for i, t in enumerate(BUILD_CARDS[key]))


def _build_spaces(folder: Path, root: Path, sub: str, job: dict | None) -> tuple:
    """(Work Details html, Report html, open tab, run types) for a building Task's four Stages."""
    states = _build_states(job)
    tab = sub if sub in BUILD_TABS else next((BUILD_TABS[i] for i, (k, _, _) in enumerate(BUILD_STAGES)
                                              if states[k] != "done"), BUILD_TABS[-1])
    i = BUILD_TABS.index(tab)
    key, title, words = BUILD_STAGES[i]
    state = states[key]
    t = rel(folder, root)
    prompt = f"/{BUILD_SKILL} {t} {words}"
    sign = ""
    if job and state in ("sign", "ready"):                             # the person's Sign and rulings: the engine's door
        sign = f'<p>{_open(_view_url(job, VIEW[{"definition": "definition", "rounds": "rounds"}[key]]), "✍ open it in the Labeling workbench ↗")}</p>'
    body = ("<h4>Input</h4>" + _build_input(key, folder, root, job) + sign
            + _prompt_box(prompt, folder, root, key, open_=state != "done"))
    step = (f'<details class="topic work-task items-step"{"" if state == "done" else " open"}><summary>'
            f'<span class=related-head><b>{esc(title)}</b> {CHIPS[state]}</span></summary>'
            f'<div class=work-body>{body}</div></details>')
    part = lambda name: f'<h3 style="margin:18px 0 6px">{name}</h3>'
    cards = _not_yet("The Stages before first.") if state == "todo" else _build_cards(key, state, job)
    runs = tuple({"label": f"run-{k}-<task>", "doing": tt.split(" · ", 1)[-1],
                  "prompt": f"/{BUILD_SKILL} {t} {w}", "skills": [BUILD_SKILL]} for k, tt, w in BUILD_STAGES)
    return part("Operation") + step + part("Result") + cards, part("Result") + cards, tab, runs


# ── Task: building, scanning, or today's one Page that is both ──────────────────────────────────
def _task_spaces(folder: Path, root: Path, sub: str) -> dict:
    types = types_of(folder)
    md, block = face(folder), _block_of(folder)
    if not md or not block:
        return {}
    if types == ("items",):
        return _items_spaces(folder, root, sub)
    if types and not {"building", "scanning"} & set(types):
        return {name: Space(note=NOTES[types[0]]) for name in ("Description", "Work Details")}
    job = _engine_job(folder, root) if types else _job_for(md, block, root)
    if job is None:
        return {}                                   # not a labeling job's Page: vanilla
    build, scan = "building" in types or not types, "scanning" in types or not types
    work = tuple(VIEW[v] for v in (BUILD_WORK if build else ()) + (SCAN_WORK if scan else ()))
    deliver = tuple(v for v, on in zip(DELIVER, (build, scan)) if on)
    described = VIEW["contract"] if build else VIEW["handoff"]
    out = {}
    d_names = ("Scope", described[2])
    d_sub = sub if sub in d_names else "Scope"
    out["Description"] = Space(
        html="" if d_sub == "Scope" else (_facts(job) + f'<p>{_open(_view_url(job, described))}</p>'),
        subspaces=d_names, open=d_sub, run_types=(_skill_run(described),) if d_sub != "Scope" else ())
    scan_names = tuple(VIEW[v][2] for v in SCAN_WORK) if scan else ()
    if build and sub not in scan_names:                                 # the four Stages (s42), then scanning's views
        html, report, tab, runs = _build_spaces(folder, root, sub, job)
        out["Work Details"] = Space(html=html, subspaces=BUILD_TABS + scan_names, open=tab, run_types=runs, page=True)
        out["Audience Report"] = Space(html=report, subspaces=BUILD_TABS, open=tab, page=True, note="Results only.")
    else:
        names = (BUILD_TABS if build else ()) + tuple(v[2] for v in work if v[1] in SCAN_WORK)
        w = BY_SUB[sub] if sub in scan_names else VIEW[SCAN_WORK[0]]
        out["Work Details"] = Space(
            html=(f'<p class=mut>{esc(w[3])}.</p>{_facts(job)}<p>{_open(_view_url(job, w))}</p>'),
            subspaces=names, open=w[2], run_types=(_skill_run(w),))
    dnames = ("Files",) + tuple(v[2] for v in deliver)
    if sub in dnames[1:]:
        dv = BY_SUB[sub]
        out["Delivery"] = Space(html=f'<p class=mut>{esc(dv[3])}.</p>{_facts(job)}<p>{_open(_view_url(job, dv))}</p>',
                                subspaces=dnames, open=sub, run_types=(_skill_run(dv),))
    else:
        out["Delivery"] = Space(subspaces=dnames, open="Files")    # Files: the vanilla delivery/ list
    return out


def spaces(folder: Path, root: Path, sub: str = "") -> dict:
    """{Space: Space} for a labeling Task; {} (vanilla) without the labeling package or for a Task that is no
    labeling job's."""
    if T.L is None:
        return {}
    return _task_spaces(Path(folder).resolve(), Path(root).resolve(), sub)
