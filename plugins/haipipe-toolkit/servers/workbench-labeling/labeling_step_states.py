"""Where each step of a 🧭 meaning or 🛠 expression Task stands: the word on its button and on its first bar."""
from __future__ import annotations

import re
from pathlib import Path
from live import interaction_section as IX

from live.labeling_step_parts import MV, TWO, kind, view_forms


def _current(loops: list) -> int:
    """The loop Report works on: the newest loop with no guideline yet, else the next one."""
    if loops and not loops[-1]["map"]:
        return loops[-1]["n"]
    return (loops[-1]["n"] + 1) if loops else 1


def _form_loop(loops: list) -> dict | None:
    """The loop Preferences shows: the form that waits for you, else the newest form."""
    forms = [lp for lp in loops if lp.get("collect") is not None]
    waiting = [lp for lp in forms if MV.state(lp["collect"]) == "waiting"]
    return (waiting or forms or [None])[-1]


def _update_loop(loops: list) -> dict | None:
    """The loop Update shows: the newest loop whose form is answered or whose guideline is written."""
    done = [lp for lp in loops if lp["map"] or (lp.get("collect") is not None and MV.state(lp["collect"]) == "done")]
    return done[-1] if done else None


# ── 🛠 expression ────────────────────────────────────────────────────────────────────────────────────────────────
def _xruns(task: Path) -> dict:
    """{role: [Runs]} for an expression Task: rewrite, run, evaluate, release."""
    return TWO.expression_runs(task)


def _open_questions(task: Path, root: Path, key: str) -> int:
    """How many questions of this step's own forms wait for the person (the count its 🙋 Interaction says)."""
    m = re.match(r"(\d+) wait", IX.state_word(view_forms(task, root, key))[0])
    return int(m.group(1)) if m else 0


def states(task: Path, root: Path | None = None) -> dict:
    """{step: (state word, ok | you | run | "")}: where each step stands, on its button and its first heading bar.
    With `root`, a released round whose release choices still wait says so: "released · 3 wait" (round 4)."""
    out = {}
    if kind(task) == "expression":
        xr = _xruns(task)
        for key in ("rewrite", "run", "evaluate"):
            run = xr[key][-1] if xr[key] else None
            out[key] = ("done", "ok") if run is not None and MV.state(run) == "done" else \
                ("running", "run") if run is not None and MV.state(run) in ("running", "waiting") else ("", "")
        run = xr["release"][-1] if xr["release"] else None
        out["release"] = (("released", "ok") if MV.release_sign(run) else ("your sign", "you")) \
            if run is not None and MV.state(run) == "done" else ("not yet", "")
        waiting = _open_questions(task, root, "release") if root is not None else 0
        if waiting and out["release"][0] == "released":
            out["release"] = (f"released · {waiting} wait", "you")
        return out
    loops, rec = MV.loops(task), MV.frame_record(task)
    out["frame"] = (("agreed", "ok") if rec and rec["decisions"] else ("waiting for you", "you")
                    if rec and rec["state"] == "waiting" else ("next", ""))
    n = _current(loops)
    lp = next((x for x in loops if x["n"] == n), None)
    collect = lp.get("collect") if lp else None
    if collect is not None and MV.state(collect) in ("waiting", "done"):
        out["prepare"] = (f"report-{n:02d} ready", "ok")
    elif lp and (lp.get("report") is not None or lp.get("draw") is not None):
        out["prepare"] = (lp["state"], "you" if lp["state"] == "draw planned" else "run")   # a planned draw: you press it
    else:
        out["prepare"] = ("next", "")
    form = _form_loop(loops)
    out["preferences"] = (("waiting for you", "you") if form and MV.state(form["collect"]) == "waiting"
                          else ("answered", "ok") if form else ("", ""))
    up = _update_loop(loops)
    out["update"] = ((f"{up['version']} approved", "ok") if up and up["approved"] else
                     (f"sign {up['version']}", "you") if up and up["map"] else ("next", "") if up else ("", ""))
    return out
