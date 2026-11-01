"""The design ladder's three Task types (b12 s41 · s42 · s43, 261023): reason ideas (t00), one design (tNN) and review
the whole (t99), each a Work of steps in the order the method runs them, Operation over Result, as the draft and
labeling Tasks' steps and the insight Job's are (JL 261023: "for the design, for each of the task, we can have
different types of the task Workbench UI, just like the Draft Task and different Tasks in the Labeling", then
"design the work in a way that we human can operate this system as well").

A step's Operation (folded until opened) holds what it reads, what is running, the run card's prompt with your
notes and the Task's session line, and, at t99's 3 · Release, a person's own Review and approve; its Result is the
design theme's own view of what the step's Run wrote. Chips come from the files: a step is done when its Run closed
and wrote its result; the first step not done is next; a Release ready for a person reads sign. A face's
`task-type:` names the type (design_ladder.py writes it); an older face without one is typed by its folder
(t00 · tNN_dNN · t99). It copies prompts only, apart from the release, which design_ladder_act.py writes.
"""
from __future__ import annotations

import re
from pathlib import Path

from live import design_reader as R
from live.frame import Space, esc, rel

TASK_TYPES = ("design-reason", "design-item", "design-whole")
KIND_TYPE = {"t00": "design-reason", "design": "design-item", "t99": "design-whole"}
STEPS = {"design-reason": ("1 · See input", "2 · Reason", "3 · Fence check"),
         "design-item": ("1 · Generate", "2 · Verify", "3 · Revise", "4 · Predict"),
         "design-whole": ("1 · Rank", "2 · Keep", "3 · Release")}
EMOJI = {"See input": "📥", "Reason": "🧠", "Fence check": "🚧", "Generate": "✍", "Verify": "🔍", "Revise": "🔁",
         "Predict": "🎯", "Rank": "📊", "Keep": "🗂", "Release": "🙋"}
OLD = {"Chains": "2 · Reason", "Elements": "1 · Generate", "Kept · Dropped": "2 · Keep"}   # the Work views before steps
DONE = ("closed", "done", "ok", "passed")
# a step's prompt when no run card names its Run (haipipe-design-workflow/references/run-cards.md is the authority)
FALLBACK = {"reason": "Reason ideas for the Job of {folder} (② run-reason-t00): from inputs/ only, topic by topic, to N + 5 "
                      "ideas, each naming its source.",
            "open-designs": "Check the fence of {folder}'s ideas (every source in inputs/), then open one design Task per "
                            "idea (run-open-designs-jNN).",
            "generate": "Generate the design of {folder} from its idea (③ run-generate-dNN): inputs/ only.",
            "verify": "Verify the design of {folder} (④ run-verify-dNN-v<k>) in a fresh context, by another agent: T0 rules "
                      "· T1 every source in the manifest.",
            "revise": "Revise the design of {folder} from its failed verify's notes (run-revise-dNN), then verify again.",
            "rank": "Review the whole (⑤ run-rank-t99) of {folder}'s Job: rank the N + 5, keep the top N, each with its "
                    "predicted effect; another agent."}


def type_of(tdir: Path) -> str:
    """The Task's type: its face's `task-type:` when it names one of these, else read from its folder."""
    t = str(R.front(R.face(tdir)).get("task-type", ""))
    return t if t in TASK_TYPES else KIND_TYPE.get(R.kind_of(tdir), "")


def _closed(run: dict | None) -> bool:
    return bool(run) and str(run.get("status", "")).lower() in DONE


def _states(kind: str, tdir: Path, j: dict) -> dict:
    """Each step's chip, from the files; the first step not done is next (a ready release: sign)."""
    steps = STEPS[kind]
    if kind == "design-reason":
        st = {steps[0]: "done" if j["manifest"] else "todo",
              steps[1]: "done" if _closed(j["reason"]) and j["ideas"] else "todo",
              steps[2]: "done" if j["designs"] or any(_closed(r) for r in j["runs"] if r["type"] == "open-designs")
              else "todo"}
    elif kind == "design-item":
        d = R.design(tdir)
        revises = [r for r in d["runs"] if r["type"] == "revise"]
        last = d["verifies"][-1] if d["verifies"] else None
        dropped = d["state"] == "dropped"
        pred = d["prediction"] or {}
        st = {steps[0]: "done" if d["drafts"] or any(_closed(r) for r in d["runs"] if r["type"] == "generate") else "todo",
              steps[1]: "done" if len(d["verifies"]) >= 1 + len(revises) else "todo",
              steps[2]: ("todo" if last and last["status"] == "failed" and len(revises) < len(d["verifies"])
                         else "done" if revises else "optional"),
              steps[3]: ("optional" if dropped else "done" if str(pred.get("frozen", "draft")) != "draft"
                         else "sign" if str(pred.get("predicted", "")).strip() and d["state"] == "kept" else "todo")}
    else:
        from live.design_ladder_act import ready
        released = any(_closed(r) for r in j["runs"] if r["type"] == "release")
        designs, _why = ready(j["path"])
        st = {steps[0]: "done" if _closed(j["rank"]) and j["ranking"] else "todo",
              steps[1]: "done" if any(d["state"] in ("kept", "released") for d in j["designs"]) else "todo",
              steps[2]: "done" if released and not designs else "sign" if designs else "todo"}
    nxt = next((s for s in steps if st[s] == "todo"), "")
    if nxt:
        st[nxt] = "next"
    return st


def current(st: dict) -> str:
    return next((s for s, v in st.items() if v in ("next", "sign")), list(st)[-1])


def _step(kind: str, step: str, tdir: Path, root: Path, j: dict, href):
    """(Input rows, prompts [(title, label, prompt)], the person's part, Result) for one step."""
    from live import design_views as V
    jid, word = j["id"], step.split(" · ", 1)[1]
    b = R.board(R.block_of(j["path"].parent) or j["path"].parent, with_jobs=False)
    if kind == "design-reason":
        if word == "See input":
            rows = [("Fence", f'<code>{esc(j["name"])}/inputs/</code>, the only files the method may read'),
                    ("Manifest", f'{len(j["manifest"].get("files") or j["files"])} files · sha256 each' if j["manifest"]
                     else "<span class=st-warn>not frozen yet: run-setup-inputs</span>")]
            return rows, [], "", V._job_inputs(j, b, root)
        if word == "Reason":
            r = j["reason"]
            rows = [("Target", f'N + 5 ideas, N = {esc(j["n"])}'), ("Its Run", esc(f'{r["run"]} · {r["status"]}') if r else "not yet"),
                    ("So far", f'{len(j["topics"])} topics → {len(j["ideas"])} ideas')]
            return rows, [("Prompt", "run-reason-t00")], "", V._reason_ideas(j, {}, root, href) + V._t00_ideas(j, href)
        opened = [r for r in j["runs"] if r["type"] == "open-designs"]
        rows = [("Fence check", "another agent: every idea cites only inputs/ (the first pass of run-open-designs)"),
                ("Its Run", esc(", ".join(f'{r["run"]} · {r["status"]}' for r in opened)) or "not yet"),
                ("Design Tasks", f'{len(j["designs"])} opened')]
        grid = V.table(("design", "idea", "state"), [(f'<a href="{esc(href("", "", d["path"]))}">{esc(d["id"])} · {esc(d["short"])}</a>',
                                                      esc(d["idea"]), V._st(d["state"])) for d in j["designs"]])
        return rows, [("Prompt", f"run-open-designs-{jid}")], "", grid
    if kind == "design-item":
        d = R.design(tdir)
        did = d["id"]
        if word == "Generate":
            rows = [("Idea", esc(d["idea"]) or "—"), ("Drafts", str(len(d["drafts"]))), ("Reads", "the Job's inputs/ only")]
            return rows, [("Prompt", f"run-generate-{did}")], "", V._design(d, j, href, root) + V._elements(d)
        if word == "Verify":
            last = d["verifies"][-1] if d["verifies"] else None
            rows = [("By", "another agent, in a fresh context: T0 rules · T1 sources · T2 critique (if the method asks)"),
                    ("Last", esc(f'{last["run"]} · {last["status"]}') if last else "not yet")]
            return rows, [("Prompt", f"run-verify-{did}")], "", V._tests(d, j, b, root)
        if word == "Revise":
            rows = [("When", "a verify failed: one draft more, from its notes, then verify again"),
                    ("Revisions", str(sum(1 for r in d["runs"] if r["type"] == "revise")))]
            return rows, [("Prompt", f"run-revise-{did}")], "", V._drafts(d, j, b, root)
        pred = d["prediction"] or {}
        rows = [("Predicted", esc(str(pred.get("predicted") or "—"))), ("Against", esc(str(pred.get("against") or "—"))),
                ("Frozen", esc(str(pred.get("frozen") or "draft")))]
        whole = j["t99"]
        person = (f'<p><b>🙋 A person freezes it</b> with the release, once, for every kept design: '
                  f'<a href="{esc(href("Work Details", "3 · Release", whole))}">t99 › 3 · Release</a></p>' if whole else "")
        return rows, [], person, V._task_perf(d, j, b, root)
    if word == "Rank":
        rows = [("By", "another agent: rank the N + 5, keep the top N, a predicted effect each"),
                ("Its Run", esc(f'{j["rank"]["run"]} · {j["rank"]["status"]}') if j["rank"] else "not yet")]
        return rows, [("Prompt", "run-rank-t99")], "", V._review_whole(j, {}, root, href)
    if word == "Keep":
        kept = sum(1 for d in j["designs"] if d["state"] in ("kept", "released"))
        rows = [("Kept", f'{kept} of N = {esc(j["n"])}'), ("Into the design Tasks", "the ranking projected onto each face")]
        return rows, [], "", V._kept(j, href) + V._coverage(j)
    rows = [("One sign", "freezes the kept designs' predictions and releases them (release.py)")]
    # the agent's way is its run card (it shows the kept designs, you sign in the session); yours is the panel below
    return rows, [("Prompt · through the agent", f"run-release-{jid}")], V._approve_panel(j, j["path"], root), \
        V._job_delivery(j, root, "designs.md")


def work_space(tdir: Path, root: Path, sub: str, href) -> Space:
    """The Task's Work: its steps as tabs, each Operation (folded) over Result, and the step's run cards."""
    from live import design_views as V
    from live.draft_steps import _kv, _part, _prompt_box, _step_box
    kind = type_of(tdir)
    j = R.job(tdir.parent)
    st = _states(kind, tdir, j)
    sub = OLD.get(sub, sub)
    step = sub if sub in STEPS[kind] else current(st)
    rows, prompts, person, result = _step(kind, step, tdir, root, j, href)
    every = R.runs(tdir) + j["runs"] + (R.runs(j["t00"]) if j["t00"] else []) + (R.runs(j["t99"]) if j["t99"] else [])
    rtype = lambda label: re.sub(r"^run-([a-z-]+?)-(?:[dtj]\d+)$", r"\1", label)
    kinds = [V._kind(label, FALLBACK.get(rtype(label), ""), rows=V._rows(every, root, rtype(label)), level="Task")
             for _t, label in prompts]
    folder = rel(tdir, root)
    boxes = "".join(_prompt_box(k["prompt"].replace("{folder}", folder), tdir, root, f"design-{step}-{n}", title)
                    for n, ((title, _l), k) in enumerate(zip(prompts, kinds)) if k["prompt"])
    now = "".join(f'<p class=run-now style="margin:0 0 8px;padding:6px 10px;border:1px solid var(--line);border-radius:3px">'
                  f'⏳ <b>Running now</b> · {esc(r["run"])} <span class=mut>· {esc(r["status"])}</span></p>'
                  for r in R.runs(tdir) + j["runs"] if str(r["status"]).lower() in ("running", "open")
                  and any(r["run"].startswith(p) for _t, p in prompts))
    word = step.split(" · ", 1)[1]
    body = "<h4>Input</h4>" + _kv(rows) + now + boxes + person
    html = (_part("Operation") + _step_box(f"{EMOJI.get(word, '·')} {step}", st[step], body, open_=word == "Release")
            + _part("Result") + (result or "<p class=mut>Nothing here yet.</p>"))
    return Space(html=html, subspaces=STEPS[kind], open=step, run_types=tuple(kinds), page=True)


def spaces(folder: Path, root: Path, sub: str) -> dict:
    """The frame's Task-type hook: the Work of a Task whose face names one of these types (the design theme draws the
    same Work for its own Tasks, typed or not)."""
    from live import frame
    theme = frame.themes()["design"]
    href = lambda space="", sub_="", path=None: frame.href(Path(path or folder), root, theme, space, sub_)
    return {"Work Details": work_space(folder, root, sub, href)} if type_of(folder) else {}
