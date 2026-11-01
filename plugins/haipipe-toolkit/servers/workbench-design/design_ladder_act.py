"""A person's own actions on the design ladder's screens (b12 s12, 261023): Review and approve a Job's release.

JL 261023: "you can design the work in a way that we human can operate this system as well", then "go ahead and do
it". Review and approve was signed through an agent ("signed: … · in chat"); here the person reads each kept design,
its prediction and its why on the Job's Delivery, ticks that they did, and approves once. The write is
haipipe-design-delivery's own `release.py` (it checks every design before it writes anything, freezes the
predictions with today's date, writes the Job's and the Block's delivery/ and marks each design released), then a
pass of `run-freeze-predictions-jNN` and `run-release-jNN` through haipipe-run's soft_run.py, each card saying
`by: a person` and `signed: ✅ <YYMMDD> · a person, in the workbench`. Board files carry no names. The route is
`POST /_board/design-ladder-act`; serve.py refuses a request from another site or with no page behind it.

    {"action": "approve", "job": <Job folder>, "attest": true}
"""
from __future__ import annotations

import contextlib
import datetime as dt
import importlib.util
import io
from pathlib import Path

from live import design_reader as DR

SKILLS = Path(__file__).resolve().parents[2] / "skills"
_RELEASE = SKILLS / "2_theme/design/haipipe-design-delivery/scripts/release.py"
_SOFT = SKILLS / "1_base/project/haipipe-run/scripts/soft_run.py"
WHO = "a person"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def today() -> str:
    return dt.date.today().strftime("%y%m%d")


def ready(job: Path) -> tuple:
    """(designs, why not): what an approval today would release, read by release.py's own dry run; ([], reason)
    when it would refuse, and ([], "") when everything is released already."""
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            return _load(_RELEASE, "haipipe_design_release").release(job, freeze=today(), dry=True), ""
    except SystemExit as e:
        return [], str(e.code or "release.py refused")


def _pass(job: Path, rtype: str, target: str, title: str, summary: str, changed: list) -> None:
    soft = _load(_SOFT, "haipipe_soft_run")
    run = job / "runs" / f"run-{rtype}-{target}"
    if not (run / "run.yaml").is_file():
        soft.new(job, rtype, target, skill="haipipe-design-delivery", agent=WHO, signs=[WHO],
                 ask="Review and approve, in the workbench", close="the release signed once")
    soft.add_pass(run, title, ask="a person, in the workbench", summary=summary, changed=changed, status="done")
    c = soft.read_card(run)
    now = dt.datetime.now().isoformat(timespec="seconds")
    c.update({"status": "closed", "by": WHO, "signed": f"✅ {today()} · {WHO}, in the workbench",
              "started_at": c.get("started_at") or now, "finished_at": now})
    soft.write_card(run, c)


def _approve(root: Path, p: dict) -> tuple:
    job = (root / str(p.get("job") or "").strip("/")).resolve()
    if not (job.is_dir() and root in job.parents and DR.is_job(job)):
        return 400, {"ok": False, "err": "no such design Job"}
    designs, why = ready(job)
    if not designs:
        return 409, {"ok": False, "err": why or "already released: nothing new"}
    with contextlib.redirect_stdout(io.StringIO()):
        out = _load(_RELEASE, "haipipe_design_release").release(job, freeze=today())
    jid = job.name.split("_", 1)[0]
    names = [d["design"] for d in out]
    changed = [f"{t.name}/prediction.yaml" for t in sorted(job.iterdir())
               if t.is_dir() and any(t.name.split("_")[1:2] == [n] for n in names)]
    _pass(job, "freeze-predictions", jid, f"predictions frozen by {WHO}", f"{len(names)} kept designs' predictions "
          f"frozen {today()}: {', '.join(names)}", changed)
    _pass(job, "release", jid, f"released by {WHO}", f"{len(names)} designs released: {', '.join(names)}",
          ["delivery/designs.json", "delivery/designs.md"])
    return 200, {"ok": True, "released": names}


def act(root: Path, p: dict, read_only: bool = False) -> tuple:
    """(status, reply) for one person's action; nothing is written unless every check passes."""
    if read_only:
        return 403, {"ok": False, "err": "this host is read-only"}
    if p.get("attest") is not True:
        return 400, {"ok": False, "err": "tick that you read each kept design first"}
    root = Path(root).resolve()
    try:
        if p.get("action") == "approve":
            return _approve(root, p)
    except SystemExit as e:                       # release.py refuses by exiting; nothing was written
        return 409, {"ok": False, "err": str(e.code or "release.py refused")}
    except (OSError, ValueError) as e:
        return 409, {"ok": False, "err": str(e)}
    return 400, {"ok": False, "err": "unknown action"}
