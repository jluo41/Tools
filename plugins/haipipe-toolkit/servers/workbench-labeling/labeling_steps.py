"""A 🧭 meaning or 🛠 expression Task's focus page (b15 j01 t03 s58, stage 2; JL 261101: "how will you update the
skills ... and update the workbench here ... Please make them work").

The Task's steps are the view-button-list; each view is one numbered list of closed bars: the step itself first (its
flow In → who works → Out, your sign and its prompt box), then what the step made, then 🙋 Interaction last with that
step's own forms (the rail's Interactions shows all of them; the step never repeats a form), then the next step. Where
a Task opens comes from engine/two_loops.py, the same rule /hai-labeling <Job> follows. Everything is read from the Task's own folders, in the layout
hai-labeling-interaction (meaning) and hai-labeling-expression (expression) write; the meaning layout is
engine/meaning_versions.py's, so the page and the skill read the same files:

    meaning     Frame · Prepare · Preferences · Update    Loop NN makes guideline mNN (a mind map) and labels lNN;
                                                           its Runs end in _mNN; only this Task asks you
    expression  Rewrite · Run · Evaluate · Release         round eNN under one approved meaning; its Runs end in
                                                           _mNN_eNN; it asks only how a release is used

Nothing here writes. The one write a page makes is your sign on a guideline (POST /_board/labeling/approve, labeling.py),
and the Preferences prompt, which copies the answers of the form in 🙋 Interaction with your notes (focus-assets/steps.js).
"""
from __future__ import annotations

from pathlib import Path
from live.ui_parts import _numbered

from live.labeling_step_parts import MV, NEXT, STEPS, TWO, _view_url, esc, interaction, kind, view_forms
from live.labeling_step_states import _current, _form_loop, _update_loop, states
from live.labeling_meaning_view import _meaning_turns, m_frame, m_preferences, m_report, m_update
from live.labeling_expression_view import x_view


# labeling_steps was split by responsibility into the modules below; an old name still answers from the one that holds it
SPLIT_INTO = ("labeling_expression_view", "labeling_meaning_view", "labeling_step_states", "labeling_step_parts")


def __getattr__(name: str):
    """An old name (`labeling_steps.<name>`, `from live.labeling_steps import <name>`) answers from the sibling that holds it now."""
    import importlib
    for sibling in SPLIT_INTO:
        mod = importlib.import_module(f"live.{sibling}")
        if name in vars(mod):
            return vars(mod)[name]
    raise AttributeError(f"module 'live.labeling_steps' has no attribute {name!r}")


# ── the page ─────────────────────────────────────────────────────────────────────────────────────────────────────
def default_view(task: Path) -> str:
    """Where the Task opens: the step that needs you or comes next (engine/two_loops.task_step)."""
    return TWO.task_step(task)


def view_html(task: Path, root: Path, section: str, key: str) -> str:
    """One step: its strip, one numbered list (the step itself, what it made, 🙋 Interaction), the next step."""
    steps = {k: (name, cap) for k, name, cap in STEPS[kind(task)]}
    name, caption = steps[key]
    if kind(task) == "meaning":
        loops = MV.loops(task)
        at = {"preferences": _form_loop(loops), "update": _update_loop(loops)}.get(key)
        lead = "" if key == "frame" else _meaning_turns(loops, at["n"] if at else _current(loops), "report next", task, root)
        process, results = {"frame": lambda: m_frame(task, root), "prepare": lambda: m_report(task, root, loops),
                            "preferences": lambda: m_preferences(task, root, loops),
                            "update": lambda: m_update(task, root, loops)}[key]()
    else:
        lead, process, results = x_view(task, root, key)
    body = lead + _numbered(process + results)  # Work retired (JL 261111): one list, no Process/Results heading
    body += interaction(task, root, body, view_forms(task, root, key))   # last, this step's own forms (settled 3)
    if key in NEXT:
        nxt, words = NEXT[key]
        body += f'<p class=ls-next><a href="{esc(_view_url(task, root, nxt))}">next: {esc(words)} →</a></p>'
    return f'<div class=ls-view>{body}</div>' 


def page(theme, root, folder, section: str = "", group: str = ""):
    """The Task's focus page on the shared frame (labeling_focus.task_frame): its steps, then Delivery, in Report;
    each step whole (the step, what it made, 🙋 Interaction, the next step), then its 🙋 Interactions."""
    from live import labeling_focus as LF
    root, folder = Path(root).resolve(), Path(folder).resolve()
    views = {k: name for k, name, _ in STEPS[kind(folder)]}
    return LF.task_frame(theme, root, folder, section, group, views, lambda: default_view(folder),
                         lambda view: view_html(folder, root, "work", view), states(folder, root))
