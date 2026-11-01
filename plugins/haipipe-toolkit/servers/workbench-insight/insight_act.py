"""A person's own actions on the insight screens (b11 s12, 261023): CHECK a page, sign a Job's close.

JL 261023: "you can design the work in a way that we human can operate this system as well", then "go ahead and do
it". Until now a person acted only through an agent ("signed: ✅ … · in chat"). Each action here re-reads the files,
checks the gate the screen shows, and writes what an agent's Run would: the page's `check:` line or the Job face's
`state: closed`, and a pass of the soft Run (`run-check-tNN`, `run-close-jNN`) through haipipe-run's soft_run.py, its
card saying `by: a person`. Board files carry no names (✅ <YYMMDD> · a person). The route is `POST
/_board/insight-act`; serve.py refuses a request from another site or with no page behind it.

    {"action": "check", "task": <Task folder>, "verdict": "pass" | "return", "why": "…", "attest": true}
    {"action": "close", "job": <Job folder>, "attest": true}
"""
from __future__ import annotations

import datetime as dt
import importlib.util
import re
from pathlib import Path

import yaml

from live import insight_plan_c as P

_SOFT = Path(__file__).resolve().parents[2] / "skills/1_base/project/haipipe-run/scripts/soft_run.py"
WRITTEN = ("written", "answered", "checked")
WHO = "a person"


def _soft():
    spec = importlib.util.spec_from_file_location("haipipe_soft_run", _SOFT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def today() -> str:
    return dt.date.today().strftime("%y%m%d")


def set_front(md: Path, fields: dict) -> None:
    """Set scalar keys of a face's front matter, each on its own line, every other line kept as it is."""
    text = md.read_text(encoding="utf-8")
    m = re.match(r"(?s)^---\n(.*?)\n---\n", text)
    if not m:
        raise ValueError(f"{md.name} has no front matter")
    lines = m.group(1).split("\n")
    for key, value in fields.items():
        line = yaml.safe_dump({key: value}, allow_unicode=True, width=10_000).strip()
        at = next((i for i, x in enumerate(lines) if re.match(rf"^{re.escape(key)}:", x)), None)
        if at is None:
            lines.append(line)
        elif re.match(rf"^{re.escape(key)}:\s*[|>]", lines[at]):
            raise ValueError(f"{md.name}: {key} is a block of lines; change it in the file")
        else:
            lines[at] = line
    md.write_text("---\n" + "\n".join(lines) + "\n---\n" + text[m.end():], encoding="utf-8")


def _pass(folder: Path, rtype: str, target: str, skill: str, signs: str, title: str, summary: str, changed: list,
          card: dict) -> Path:
    """A pass of the folder's soft Run run-<rtype>-<target> (made the first time), its card saying who did it."""
    soft = _soft()
    run = folder / "runs" / f"run-{rtype}-{target}"
    if not (run / "run.yaml").is_file():
        soft.new(folder, rtype, target, skill=skill, agent=WHO, signs=[signs],
                 ask=f"{title}, in the workbench", close="the person's verdict, written where the screen reads it")
    soft.add_pass(run, title, ask="a person, in the workbench", summary=summary, changed=changed, status="done")
    c = soft.read_card(run)
    now = dt.datetime.now().isoformat(timespec="seconds")
    c.update({"by": WHO, "started_at": c.get("started_at") or now, "finished_at": now, **card})
    soft.write_card(run, c)
    return run


def _inside(root: Path, value) -> Path | None:
    folder = (root / str(value or "").strip("/")).resolve()
    return folder if folder.is_dir() and root in folder.parents else None


def _check(root: Path, p: dict) -> tuple:
    """A person's CHECK of one written page: ✅ passes it; ↩ returns it with the reason, for 3 · Write to redo."""
    task = _inside(root, p.get("task"))
    if task is None or not P.TASK_NAME.match(task.name) or not P.JOB_NAME.match(task.parent.name):
        return 400, {"ok": False, "err": "no such question Task"}
    page = task / f"{task.name}.md"
    if not page.is_file():
        return 404, {"ok": False, "err": "this Task has no page yet"}
    face = P.front(page)
    if str(face.get("answer-status", "")).lower() not in WRITTEN or not face.get("answer"):
        return 409, {"ok": False, "err": "the page is not written yet: 3 · Write comes first"}
    if str(P.front(task.parent / f"{task.parent.name}.md").get("state", "")) == "closed":
        return 409, {"ok": False, "err": "the Job is closed: its pages are frozen"}
    made = [r for r in P.runs(task) if r["run"].startswith("run-write-") and WHO in str(r.get("by") or r.get("agent") or "")]
    if made:
        return 409, {"ok": False, "err": "a person wrote this page; another agent checks it (Copy prompt)"}
    verdict, why = str(p.get("verdict") or ""), " ".join(str(p.get("why") or "").split())
    if verdict not in ("pass", "return"):
        return 400, {"ok": False, "err": "verdict is pass or return"}
    if verdict == "return" and not why:
        return 400, {"ok": False, "err": "say why it goes back, in a line"}
    if any(c in why for c in "<>") or len(why) > 600:
        return 400, {"ok": False, "err": "plain words only, one line"}
    line = (f"✅ {today()} · {WHO}" + (f" · {why}" if why else "")) if verdict == "pass" else f"↩ {today()} · {WHO} · {why}"
    set_front(page, {"check": line})
    tnn = task.name.split("_", 1)[0]
    _pass(task, "check", tnn, "haipipe-report", "none", f"CHECK by {WHO}: {verdict}", why or "it holds",
          [_rel(page, root)], {"verdict": verdict})
    return 200, {"ok": True, "check": line}


def _rel(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root).as_posix()


def _close(root: Path, p: dict) -> tuple:
    """A person signs a Job's close once every step before it is done: the Job is frozen."""
    from live import insight_views as V
    job = _inside(root, p.get("job"))
    if job is None or not P.JOB_NAME.match(job.name) or not (job / f"{job.name}.md").is_file():
        return 400, {"ok": False, "err": "no such insight Job"}
    j = P.job(job)
    if j["state"] == "closed":
        return 409, {"ok": False, "err": "the Job is closed already"}
    st = V._work_states(j, V._work_facts(j))
    waits = [s for s in V.WORK_STEPS[:-1] if st[s] not in ("done", "optional")]
    if waits:
        return 409, {"ok": False, "err": "it waits on " + " · ".join(waits)}
    face = job / f"{job.name}.md"
    set_front(face, {"state": "closed", "signed": f"✅ {today()}"})
    jnn = job.name.split("_", 1)[0]
    _pass(job, "close", jnn, "haipipe-insight-check", WHO, f"the close, signed by {WHO}",
          "every page checked and the comparison written; the Job is frozen", [_rel(face, root)],
          {"status": "closed", "signed": f"✅ {today()} · {WHO}, in the workbench"})
    return 200, {"ok": True, "state": "closed"}


def act(root: Path, p: dict, read_only: bool = False) -> tuple:
    """(status, reply) for one person's action; nothing is written unless every check passes."""
    if read_only:
        return 403, {"ok": False, "err": "this host is read-only"}
    if p.get("attest") is not True:
        return 400, {"ok": False, "err": "tick that you read it first"}
    root = Path(root).resolve()
    try:
        if p.get("action") == "check":
            return _check(root, p)
        if p.get("action") == "close":
            return _close(root, p)
    except (OSError, ValueError) as e:
        return 409, {"ok": False, "err": str(e)}
    return 400, {"ok": False, "err": "unknown action"}
