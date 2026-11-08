"""The design theme on the focus page (b12 j01, s51 to s59, JL 261101): a design Block, a Job and a Task, each Report
and Work in the cells' letters, drawn with the shared parts every theme's page uses (ui_parts: bands, numbered bars,
to-do rows with state pills, Copy prompt), as the paper's (paper_version, board_views), the labeling Task's steps
(labeling_steps) and the insight Job's (insight_focus).

    Block   Summary · Goals · Jobs · Rounds · Methods                  (s51 Report, s52 Work)
    Job     Setup · Ideas · Designs · Ranking · Release                (s54 Report, s55 Work)
    Task    by its type, one view per step (s57 Report, s58 Work):
            💡 t00 reason ideas   Inputs · Chains · Ideas · Fence check
            ✏️ one design         Draft · Verify · Revise · State
            🏆 t99 review whole   Rank · Coverage · Kept

Report is a view's 📊 Results only; Work is ⚙️ Process (🙋 what waits on you first, then the view's steps, each row
ending in its state word, its Run's prompt one Copy away) over the same Results. A person signs only at the Block
(goals, shared rules) and the Job (Review and approve, the close); no Task asks you. The Results are design_views'
own views, so the focus page and the six-Space page agree; the only write is the release, design_ladder_act.py's."""
from __future__ import annotations

import re
from pathlib import Path

from live import design_canvas as C
from live import design_reader as R
from live import design_views as V
from live import focus_draft as FD
from live.frame import esc, rel
from live.ui_parts import (GROUP_CSS, PB_CSS, PB_JS, PROCESS, PROMPT_CSS, PROMPT_JS, RESULTS, _band, _kv, _numbered, _pill,
                           _section)

BLOCK_VIEWS = (("summary", "Summary"), ("goals", "Goals"), ("jobs", "Jobs"), ("rounds", "Rounds"), ("methods", "Methods"))
JOB_VIEWS = (("setup", "Setup"), ("ideas", "Ideas"), ("designs", "Designs"), ("ranking", "Ranking"), ("release", "Release"))
TASK_STEPS = {"t00": ("💡", "reason ideas", ("Inputs", "Chains", "Ideas", "Fence check")),
              "design": ("✏️", "design", ("Draft", "Verify", "Revise", "State")),
              "t99": ("🏆", "review whole", ("Rank", "Coverage", "Kept"))}
CAPTIONS = {"summary": "where this Block stands, from what its Runs wrote", "goals": "the signed goals and the shared rules",
            "jobs": "each goal × method version × inputs version, and how far each Job has got", "rounds": "one round per inputs version",
            "methods": "how each method's predictions held up, and what they cost",
            "setup": "the three pins: goal, method, inputs", "ideas": "what was reasoned, from the fence only",
            "designs": "each design as it reads, and its verdict", "ranking": "t99's ranking and coverage",
            "release": "what was released, and its frozen predictions"}

POST_JS = """<script>(function(){if(window.inPost)return;window.inPost=1;
 document.addEventListener('click',function(ev){var b=ev.target.closest('button[data-post]');if(!b)return;ev.preventDefault();
  var body={};try{body=JSON.parse(b.dataset.body||'{}');}catch(e){}
  var row=b.closest('.sign-row')||b.parentNode;(b.dataset.fields||'').split(' ').filter(Boolean).forEach(function(n){
   var i=row.querySelector('[name="'+n+'"]');if(i)body[n]=i.type==='checkbox'?i.checked:i.value;});
  b.disabled=true;
  fetch(b.dataset.post,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})
   .then(function(x){return x.json();}).then(function(j){if(j.ok){location.reload();return;}
    b.disabled=false;b.title=j.err||'';b.textContent='✗ '+(j.err||'refused');});});
})();</script>"""
CSS = """<style>.pb-prompt.in-copy{display:inline;border:0;padding:0;margin:0;background:none}
.dz-flow{display:grid;grid-template-columns:1fr auto 1fr auto 1fr;gap:8px;align-items:stretch;margin:2px 0 8px}
.dz-flow>div{border:1px solid var(--line);border-radius:8px;padding:8px 12px;background:var(--paper);font-size:13px}
.dz-flow small{display:block;color:var(--muted);font-size:11.5px}.dz-flow b{display:block}.dz-arrow{align-self:center;color:var(--muted)}
.dz-part{margin:4px 0 8px;font-size:13px;color:var(--muted)}.sign-row{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.work-act{font:inherit;font-size:13px;border:1px solid var(--line);border-radius:6px;padding:3px 10px;background:var(--paper);cursor:pointer}
.work-act[disabled]{opacity:.55;cursor:default}
.dz-close{font-size:13px;margin:2px 0 4px}
@media(max-width:600px){.dz-flow{grid-template-columns:1fr}.dz-arrow{transform:rotate(90deg);justify-self:start}}</style>"""


# ── what a page is ──────────────────────────────────────────────────────────────────────────────────────────────
def level_of(folder: Path) -> str:
    """Block, Job or Task of a design Board on the ladder; "" for anything else (an older Board keeps its page)."""
    if R.is_job(folder):
        return "Job" if R.is_ladder(folder.parent) else ""
    if re.match(r"^t\d+_", folder.name) and R.is_job(folder.parent) and R.is_ladder(folder.parent.parent):
        return "Task"
    if (folder / "board.md").is_file() and R.is_ladder(folder):
        return "Block"
    return ""


def _href(root: Path):
    """design_views' links (space, sub, path) on the focus page: a folder opens its own focus page."""
    from live import focus_page as F
    return lambda space="", sub="", path=None: F.page_url(Path(path), root) if path else "#"


def _session(folder: Path) -> str:
    for face in (folder / f"{folder.name}.md", folder.parent / f"{folder.parent.name}.md", folder / "board.md",
                 folder.parent / "board.md", folder.parent.parent / "board.md"):
        if face.is_file():
            m = re.search(r"(?m)^session:\s*`?([\w.-]+)`?", face.read_text(encoding="utf-8", errors="ignore")[:4000])
            if m:
                return m.group(1)
    return folder.name


# ── the shared pieces of a view ─────────────────────────────────────────────────────────────────────────────────
def _copy(label: str, level: str, folder: Path, root: Path, fallback: str = "", verb: str = "Copy prompt") -> str:
    """A row's own Copy prompt: the run card's prompt (its agent, its sign) with this folder filled in, shown on hover."""
    text = V._kind(label, fallback, level=level)["prompt"].replace("{folder}", rel(folder, root))
    if not text:
        return ""
    tail = f'Run this in the Claude session "{_session(folder)}"; start it if it is not running.'
    return (f'<span class="pb-prompt in-copy" title="{esc(text)}"><button type=button class="fd-btn pb-copy" '
            f'data-copy="{esc(text)}" data-tail="{esc(tail)}">{esc(verb)}</button></span>')


def _todo(rows: list) -> str:
    """Rows like ui_parts._todo, each with its own buttons: [(words, sub, state, verbs html)]."""
    return '<div class=pb-todos>' + "".join(
        f'<div class=pb-todo><span class=w>{w}' + (f"<small>{esc(s)}</small>" if s else "") + "</span>"
        + _pill(state) + verbs + "</div>" for w, s, state, verbs in rows) + "</div>"


def _link(path: Path, root: Path, words: str) -> str:
    from live import focus_page as F
    return f'<a href="{esc(F.page_url(path, root))}">{esc(words)}</a>'


def _closed(r: dict | None) -> bool:
    return bool(r) and str(r.get("status", "")).lower() in ("closed", "done", "ok", "passed")


def _has(rs: list, rtype: str) -> bool:
    return any(_closed(r) for r in rs if r["type"] == rtype)


def _page(caption: str, process: str, results: str, report: bool) -> str:
    # Report is its numbered sections only; the bands live in Work (JL 261101, b11: "the Process and Results will only
    # be available in the Work Section"; b16 s32-D27)
    body = _numbered(results) if report else _band(PROCESS, _numbered(process)) + _band(RESULTS, _numbered(results))
    return (PB_CSS + GROUP_CSS + FD.CSS + PROMPT_CSS + CSS + f'<p class="view-caption">{esc(caption[:1].upper() + caption[1:])}.</p>'
            + body + PB_JS + FD.JS + PROMPT_JS + POST_JS)


def _views(keys, build, report: bool) -> dict:
    """{key: (name, build)}: Report the Results only, Work Process over Results; built only when opened."""
    out = {}
    for key, name in keys:
        def make(key=key):
            caption, process, results = build(key)
            return _page(caption, process, results, report)
        out[("report-" if report else "work-") + key] = (name, make)
    return out


# ── the Block (s51 Report, s52 Work) ────────────────────────────────────────────────────────────────────────────
def _job_next(j: dict) -> tuple:
    """A Job's next move and its state word, in the method's order."""
    from live.design_ladder_act import ready
    if V._approved(j)[0]:                             # released: the close is yours to sign, then it is done
        return ("closed", "done") if _job_closed(j) else ("close the Job", "waiting for you")
    if j["ranking"] and ready(j["path"])[0]:          # a release ready for your sign comes first
        return "review and approve", "waiting for you"
    if not (j["goal"] and j["method"] and j["manifest"]):
        return "set up its pins", "next"
    if not (_closed(j["reason"]) and j["ideas"]):
        return "reason ideas (t00)", "next"
    if not j["designs"]:
        return "check the fence, open the design Tasks", "next"
    undone = [d for d in j["designs"] if not d["verifies"] or d["verifies"][-1]["status"] != "passed"]
    if undone and d_state(undone[0]) != "dropped":
        return f'{len(undone)} designs to generate, verify or revise', "next"
    if not (_closed(j["rank"]) and j["ranking"]):
        return "review the whole (t99)", "next"
    if ready(j["path"])[0]:
        return "review and approve", "waiting for you"
    return "nothing ready to release", "open"


def _job_closed(j: dict) -> bool:
    """Closed: its face says so, or its run-close Run has closed (a person signed it)."""
    return str(j["state"]).lower() == "closed" or any(r["type"] == "close" and _closed(r) for r in j["runs"])


def d_state(d: dict) -> str:
    return str(d.get("state") or "")


def _block_waits(b: dict, block: Path, root: Path) -> str:
    rows = []
    for g in b["goals"]:
        if not str(g.get("signed", "")).startswith("✅"):
            rows.append((f'Sign the goal {esc(g.get("id", ""))} {esc(g.get("name", ""))}', "a Job pins only a signed goal",
                         "waiting for you", _copy("run-add-goal-<goal>", "Block", block, root)))
    for j in b["jobs"]:
        step, state = _job_next(j)
        if state == "waiting for you" and step == "close the Job":
            rows.append((f'Close {_link(j["path"], root, j["name"])}', "its designs are released or dropped; you sign the close",
                         state, _copy(f'run-close-{j["id"]}', "Job", j["path"], root,
                                      "Close {folder} once its designs are released; frozen.")))
        elif state == "waiting for you":
            rows.append((f'Review and approve {_link(j["path"], root, j["name"])}', "one sign freezes the predictions and releases",
                         state, _link_btn(j["path"], root, "work", "work-release", "Review")))
    return _section("🙋 Waits on you" if rows else "🙋 Nothing waits on you", _todo(rows) if rows else "<span hidden></span>")


def _link_btn(path: Path, root: Path, section: str, group: str, verb: str) -> str:
    from live import focus_page as F
    return f'<a class=fd-btn href="{esc(F.page_url(path, root, section, group))}">{esc(verb)}</a>'


def _goal_name(b: dict, gid: str) -> str:
    g = next((g for g in b["goals"] if g.get("id") == gid), None)
    return C.goal_words(g) if g else (gid or "no goal yet")


def goal_line(folder: Path, goal: str) -> str:
    """The goal-line of a design Job or Task in words: its pinned goal id (G01) becomes the goal's aim."""
    if not re.match(r"^G\d+$", str(goal or "").strip()) or not level_of(folder) in ("Job", "Task"):
        return ""
    jdir = folder if level_of(folder) == "Job" else folder.parent
    b = R.board(R.block_of(jdir.parent) or jdir.parent, with_jobs=False)
    return _goal_name(b, goal.strip())


def _standing(b: dict) -> str:
    """The Block's main point, large, as the paper Board's Direction (JL 261102: the paper UI is the bar): one sentence
    and its state word."""
    jobs, ds = b["jobs"], [d for j in b["jobs"] for d in j["designs"]]
    released = sum(d["state"] == "released" for d in ds)
    waiting = sum(d["state"] == "kept" for d in ds)
    if not jobs:
        line, state = "No Job yet: a signed goal waits for its first Job.", "next: launch a Job"
    elif waiting:
        line, state = f"{waiting} kept designs wait for your review; {released} are released.", "waiting for you"
    elif released and not b["observed"]:
        line, state = (f"{released} designs released from {len(jobs)} Jobs; the experiment has not come back yet.",
                       "next: run the experiment")
    elif b["observed"] and not b["scores"]:
        line, state = "The experiment is back; its predictions are not scored yet.", "next: score it"
    elif b["scores"]:
        line, state = f"{len(b['scores'])} designs tested and scored against their predictions.", "next: the next round"
    else:
        line, state = f"{len(jobs)} Jobs at work; none released yet.", "in progress"
    close = f'<p class=dz-close><b>Done when</b> {esc(b["close"])}</p>' if b["close"] else ""
    return f'<p class=pb-big>{esc(line)}</p><p class=pb-state>{esc(state)}</p>{close}'


def block_view(block: Path, root: Path, key: str) -> tuple:
    b, href = R.board(block), _href(root)
    if key == "summary":
        proc = _section("📄 Build the summary", _todo([(
            "Build the one-page summary", "delivery/summary.pdf, from what the Runs wrote only",
            "done" if (block / "delivery" / "summary.pdf").is_file() else "open",
            _copy("run-build-summary", "Block", block, root))]))
        res = (_section("🧭 Where it stands", _standing(b))
               + _section("🗺️ Goals × methods: each Job, how far it has got", C.matrix(b, root, href))
               + _section("❓ What the Block asks", V._summary(b, root, href, jobs_table=False)))
    elif key == "goals":
        proc = _section("🎯 Goals and rules", _todo([
            ("Add a goal", "a new line in board.md ## Goals; you sign it", "open", _copy("run-add-goal-<goal>", "Block", block, root)),
            ("Set the shared rules", "design-goal.md: each rule checkable on the text alone",
             "done" if (block / "design-goal.md").is_file() else "open", _copy("run-setup-rules", "Block", block, root))]))
        res = _section("🎯 The goals", V._goals(b, href))
    elif key == "jobs":
        rows = []
        for j in b["jobs"]:
            step, state = _job_next(j)
            rows.append((_link(j["path"], root, f'{C.job_words(j)} · {j["name"]}'),
                         f'{_goal_name(b, j["goal"])} × {C.method_words(j["method"])}, {C.version_words(j["version"])}'
                         f' × {C.inputs_words(j["inputs"])} · next: {step}', state, ""))
        rows.append(("+ Launch a Job", "a signed goal × a method version × an inputs version; one clock moves at a time",
                     "open", _copy("run-add-job-<jNN>", "Block", block, root)))
        proc = _section("🧭 Each Job's next move", _todo(rows))
        res = (_section("🗺️ Goals × methods: each Job, how far it has got", C.matrix(b, root, href))
               + _section("📋 The Jobs", V._jobs(b, root, href, "All")))
    elif key == "rounds":
        proc = _section("🔁 The next round", _todo([
            ("+ Add an inputs version", "inputs/iN/: rules, theory, the insight handoff, frozen", "open",
             _copy("run-add-inputs-<iN>", "Block", block, root)),
            ("+ Add the Exp's data", "observed/eNN: per-arm totals only, never rows", "open",
             _copy("run-add-observed-<eNN>", "Block", block, root))]))
        res = _section("🔁 Rounds", V._rounds(b, root, href)) + _section("📥 Inputs versions", V._inputs(b, root, href))
    else:
        proc = _section("📏 Score and learn", _todo([
            ("Score the predictions", "each Exp arm against its frozen prediction",
             "done" if b["scores"] else "waits on an Exp" if not b["observed"] else "open",
             _copy("run-score-<eNN>", "Block", block, root)),
            ("Propose a method change", "from the scores; the registry cuts the next version", "open",
             _copy("run-propose-method-<slug>", "Block", block, root))]))
        res = (_section("🎯 Predicted vs observed", V._predicted(b, root, href))
               + _section("🏅 Method scorecard", V._scorecard(b, root, href)) + _section("⏱️ Cost", V._costs(b, root, href)))
    return CAPTIONS[key], _block_waits(b, block, root) + proc, res


# ── the Job (s54 Report, s55 Work) ──────────────────────────────────────────────────────────────────────────────
def _job_waits(j: dict, jdir: Path, root: Path) -> str:
    from live.design_ladder_act import ready
    designs, why = ready(jdir)
    approved = V._approved(j)[0]
    rel_state = "done" if approved else "waiting for you" if designs else "waits on " + (why or "the ranking")
    rows = [("Review and approve", "read each kept design, its prediction and why; one sign freezes and releases",
             rel_state, _link_btn(jdir, root, "work", "work-release", "Review") if designs and not approved else ""),
            ("Close the Job", "once every design is released or dropped; you sign",
             "done" if _job_closed(j) else "waits on the release" if not approved else "waiting for you",
             _copy(f'run-close-{j["id"]}', "Job", jdir, root, "Close {folder} once its designs are released; frozen.")
             if approved and not _job_closed(j) else "")]
    you = any(r[2] == "waiting for you" for r in rows)
    return _section("🙋 Waits on you" if you else "🙋 Nothing waits on you", _todo(rows))


def _chain(d: dict) -> str:
    """A design's drafts in the order they ran: generate ✅ · verify v1 ✗ · revise ✅ · verify v2 ✅ (each verify
    reads the draft before it; the folders sort by name, so the order is rebuilt from the loop)."""
    mark = lambda r: " ✅" if _closed(r) else " ⏳"
    out = []
    for i, draft in enumerate(d["drafts"]):
        out.append(draft["type"] + mark(draft))
        if i < len(d["verifies"]):
            v = d["verifies"][i]
            out.append(f'verify v{i + 1} ' + ("✅" if v["status"] == "passed" else "✗" if v["status"] == "failed" else "⏳"))
    return " · ".join(out) or "not generated yet"


def _design_state(d: dict) -> str:
    if d_state(d) in ("kept", "released", "dropped"):
        return d_state(d)
    last = d["verifies"][-1] if d["verifies"] else None
    if last and last["status"] == "failed":
        return "revise next"
    if last and last["status"] == "passed":
        return "passed"
    return "verify next" if d["drafts"] else "generate next"


def job_view(jdir: Path, root: Path, key: str) -> tuple:
    j, href = R.job(jdir), _href(root)
    b = R.board(R.block_of(jdir.parent) or jdir.parent, with_jobs=False)
    jid = j["id"]
    if key == "setup":
        pins = (("Goal", bool(j["goal"]), "setup-goal"), ("Method", bool(j["method"]), "setup-method"),
                ("Inputs", bool(j["manifest"]), "setup-inputs"))
        proc = _section("📌 The three pins", _todo([
            (f"Set up the {w.lower()}", {"Goal": f'pinned: {j["goal"] or "—"}', "Method": f'{j["method"]} {j["version"]}'.strip()
                                         or "—", "Inputs": f'{j["inputs"] or "—"} · its manifest frozen'}[w],
             "done" if ok else "next", "" if ok else _copy(f"run-{t}-{jid}", "Job", jdir, root)) for w, ok, t in pins]))
        res = (_section("🎯 Goal", V._setup_strip(j) + V._job_goal(j, b, root))
               + _section("🧩 Method", V._job_method(j, b, root, href=href)) + _section("📥 Inputs", V._job_inputs(j, b, root)))
    elif key == "ideas":
        opened = bool(j["designs"]) or _has(j["runs"], "open-designs")
        proc = _section("💡 Reason, then open", _todo([
            ("Reason ideas (t00)", f'{len(j["topics"])} topics → {len(j["ideas"])} ideas, from inputs/ only',
             "done" if _closed(j["reason"]) and j["ideas"] else "next",
             "" if j["ideas"] else _copy("run-reason-t00", "Task", j["t00"] or jdir, root)),
            ("Check the fence, open the design Tasks", "another agent; one Task per idea, only after a pass",
             "done" if opened else "next" if j["ideas"] else "waits on the ideas",
             "" if opened else _copy(f"run-open-designs-{jid}", "Job", jdir, root))]))
        res = (_section("🔗 Where each design came from",
                        C.lineage(j, href) or "<p class=mut>Nothing reasoned yet.</p>")
               + _section("💡 The ideas", V._reason_ideas(j, b, root, href)))
    elif key == "designs":
        rows = [(_link(d["path"], root, f'{d["id"]} · {d["short"]}'), _chain(d), _design_state(d), "") for d in j["designs"]]
        proc = _section("✏️ Each design's next Run", _todo(rows) if rows else
                        "<p class=mut>No design Task yet: the fence check opens them.</p>")
        res = _section("✏️ The designs, as they read", V._display(j, b, root, href))
    elif key == "ranking":
        proc = _section("🏆 Review the whole (t99)", _todo([(
            "Rank, keep the top N, a predicted effect each", "another agent, in a fresh context",
            "done" if _closed(j["rank"]) and j["ranking"] else "next" if j["designs"] else "waits on the designs",
            "" if j["ranking"] else _copy("run-rank-t99", "Task", j["t99"] or jdir, root))]))
        res = _section("🏆 Ranking", V._review_whole(j, b, root, href)) + _section("🧭 Coverage", V._coverage(j))
    else:
        proc = _section("✍️ Review and approve", V._approve_panel(j, jdir, root))
        res = (_section("📄 Released designs", V._job_delivery(j, root, "designs.md"))
               + _section("🎯 Predicted vs observed", V._job_observed(j, b, root, href)))
    return CAPTIONS[key], _job_waits(j, jdir, root) + proc, res


# ── the Task (s57 Report, s58 Work), by type ────────────────────────────────────────────────────────────────────
def _flow(inn: tuple, who: tuple, out: tuple) -> str:
    box = lambda word, head, line: f'<div><small>{esc(word)}</small><b>{esc(head)}</b>{esc(line)}</div>'
    arrow = '<span class=dz-arrow aria-hidden=true>→</span>'
    return f'<div class=dz-flow>{box("In", *inn)}{arrow}{box("Who works", *who)}{arrow}{box("Out", *out)}</div>'


NONE = '<p class=dz-part>Your part: none here; an agent works, another agent checks. You sign at the Job.</p>'


def task_steps(tdir: Path) -> tuple:
    icon, typ, steps = TASK_STEPS[R.kind_of(tdir)]
    return icon, typ, steps


def task_view(tdir: Path, root: Path, step: str) -> tuple:
    j, href = R.job(tdir.parent), _href(root)
    b = R.board(R.block_of(tdir.parent.parent) or tdir.parent.parent, with_jobs=False)
    kind, jid = R.kind_of(tdir), j["id"]
    icon, typ, _steps = TASK_STEPS[kind]
    opened = bool(j["designs"]) or _has(j["runs"], "open-designs")
    if kind == "t00":
        spec = {"Inputs": (("Inputs version", j["inputs"] or "—"), ("🤖 Designer agent", "keep what step ① names"),
                           ("inputs/ + manifest.yaml", "every file the work may read"),
                           "done" if j["manifest"] else "next", f"run-setup-inputs-{jid}", "Job", tdir.parent,
                           lambda: V._job_inputs(j, b, root)),
                "Chains": (("inputs/", "goal · method · rules"), ("🤖 Designer agent", "② reason, step by step"),
                           ("chains.yaml", "each step and its source"),
                           "done" if j["topics"] else "next", "run-reason-t00", "Task", tdir, lambda: V._t00_chains(j)),
                "Ideas": (("chains.yaml", "the reasoning"), ("🤖 Designer agent", "one idea per chain's end"),
                          ("ideas.yaml", f'{len(j["ideas"])} ideas'),
                          "done" if j["ideas"] else "next", "run-reason-t00", "Task", tdir, lambda: V._t00_ideas(j, href)),
                "Fence check": (("chains.yaml", "every step's from: line"), ("🤖 Reviewer agent", "a fresh context"),
                                ("fence-check.md", "pass, then the design Tasks open"),
                                "done" if opened else "next" if j["ideas"] else "waits on the ideas",
                                f"run-open-designs-{jid}", "Job", tdir.parent,
                                lambda: V.table(("design", "idea", "state"), [(_link(d["path"], root, f'{d["id"]} · {d["short"]}'),
                                                                               esc(d["idea"]), V._st(d["state"])) for d in j["designs"]])
                                or "<p class=mut>No design Task opened yet.</p>")}
    elif kind == "design":
        d = R.design(tdir)
        did = d["id"]
        state = _design_state(d)
        k = len(V.draft_files(d))                       # drafts so far: the generate's, then one per revise pass
        revised = max(k - 1, 0)
        spec = {"Draft": ((f'Idea {d["idea"] or "—"}', "from t00's ideas.yaml, and inputs/ only"),
                          ("🤖 Designer agent", "③ conduct the method's process"), ("Draft + elements.yaml", f'{k} draft{"" if k == 1 else "s"}'),
                          "done" if d["drafts"] else "next", f"run-generate-{did}", "Task", tdir,
                          lambda: V._design(d, j, href, root) + V._elements(d)),
                "Verify": (("The last draft", "the design + elements.yaml"), ("🤖 Reviewer agent", "④ T0 rules · T1 sources, fresh"),
                           ("verdict", d["verifies"][-1]["status"] if d["verifies"] else "not yet"),
                           "done" if d["verifies"] and d["verifies"][-1]["status"] == "passed" else
                           "next" if d["drafts"] else "waits on the draft", f"run-verify-{did}-v{max(k, 1)}", "Task", tdir,
                           lambda: V._tests(d, j, b, root)),
                "Revise": (("A failed verify", "its notes"), ("🤖 Designer agent", "one more draft, then verify again"),
                           ("Draft v" + str(k + 1 if state == "revise next" else k),
                            f"{revised} revision{'' if revised == 1 else 's'}"),
                           "next" if state == "revise next" else "done" if revised else "not needed",
                           f"run-revise-{did}", "Task", tdir, lambda: V._drafts(d, j, b, root)),
                "State": (("t99's ranking", "rank and kept"), ("🤖 Reviewer agent", "⑤ at t99; you sign at the Job"),
                          ("prediction.yaml", str((d["prediction"] or {}).get("frozen") or "draft")),
                          {"kept": "kept", "released": "done", "dropped": "dropped"}.get(d_state(d), state),
                          "", "Task", tdir, lambda: V._task_perf(d, j, b, root))}
    else:
        kept = sum(1 for d in j["designs"] if d_state(d) in ("kept", "released"))
        spec = {"Rank": (("The designs", f'{len(j["designs"])} drafted'), ("🤖 Reviewer agent", "⑤ rank, a predicted effect each"),
                         ("ranking.csv", "rank · predicted · why · kept"),
                         "done" if _closed(j["rank"]) and j["ranking"] else "next" if j["designs"] else "waits on the designs",
                         "run-rank-t99", "Task", tdir, lambda: V._review_whole(j, b, root, href)),
                "Coverage": (("ranking.csv", "the kept designs"), ("🤖 Reviewer agent", "which parts of the goal they cover"),
                             ("coverage", "by goal part"), "done" if j["ranking"] else "waits on the ranking", "", "Task", tdir,
                             lambda: V._coverage(j)),
                "Kept": (("ranking.csv", "the top N"), ("🤖 Reviewer agent", "projected onto each design's face"),
                         ("kept", f'{kept} of N = {j["n"]}'), "done" if kept else "waits on the ranking", "", "Task", tdir,
                         lambda: V._kept(j, href))}
    inn, who, out, state, label, level, folder, result = spec[step]
    row = _todo([(f'{icon} {esc(step)}', f"{typ} · {who[0].split(' ', 1)[-1]}", state,
                  _copy(label, level, folder, root) if label and state in ("next", "revise next") else "")])
    part = NONE
    if kind == "t99" and step == "Kept":
        part = (f'<p class=dz-part>Your part is at the Job: {_link_btn(j["path"], root, "work", "work-release", "Review and approve")}'
                f' freezes the kept designs\' predictions and releases them.</p>')
    proc = _section(f"{icon} {step}", _flow(inn, who, out) + row + part)
    res = _section(f"📊 {step}", result() or "<p class=mut>Nothing here yet.</p>")
    return f"{typ} · {step}: what the step reads, who works, what it writes", proc, res


# ── what focus_page.py asks ─────────────────────────────────────────────────────────────────────────────────────
def views(folder: Path, root: Path, section: str, items=(), item_html=None) -> dict:
    """{key: (name, build)} for the page's Report (section "report") or Work; {} for a folder that is not a design
    Block, Job or Task on the ladder, so the base page stays."""
    root = root.resolve()
    level = level_of(folder)
    report = section == "report"
    if level == "Block":
        return _views(BLOCK_VIEWS, lambda k: block_view(folder, root, k), report)
    if level == "Job":
        return _views(JOB_VIEWS, lambda k: job_view(folder, root, k), report)
    if level == "Task":
        _icon, _typ, steps = task_steps(folder)
        return _views([(re.sub(r"\W+", "-", s.lower()), s) for s in steps],
                      lambda k: task_view(folder, root, next(s for s in steps if re.sub(r"\W+", "-", s.lower()) == k)), report)
    return {}
