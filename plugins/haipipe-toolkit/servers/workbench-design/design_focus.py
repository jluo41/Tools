"""The design theme on the focus page (b12 j01, s51 to s59, JL 261101): a design Block, a Job and a Task, each Report
and Work in the cells' letters, on the shared page rules every theme's page follows (haipipe-ui "The person's page
rules", 261106; insight_focus is the model):

  every section a numbered bar, closed until opened, its state word on its right, read from its content; what waits
  on the person under the closed bar (ui_parts._section's `word` and `waits`); the fold script on Report too.
  Report shows results only, each view's big line first; Work has the same views, each ⚙️ Process then 📊 Results, the
  Results drawn by the same function as the Report's view. A row that waits on the person but is no form (sign a goal,
  approve a release, close a Job, agree a method proposal) is a Process step with its state word, never a 🙋 section
  of its own: 🙋 Interaction is the last section of every view, added by the page itself with that view's own forms
  (view_of_item). Lists of items are side tabs, their labels with no count; the MindMap is always a view, last.

    Block   Summary · Goals · Jobs · Rounds · Methods · MindMap         (s51 Report, s52 Work)
    Job     Setup · Ideas · Designs · Ranking · Release · MindMap       (s54 Report, s55 Work)
    Task    by its type, one view per step, then MindMap (s57 Report, s58 Work):
            💡 t00 reason ideas   Inputs · Chains · Ideas · Fence check
            ✏️ one design         Draft · Verify · Revise · State      (its drafts strip above every view)
            🏆 t99 review whole   Rank · Coverage · Kept

A person signs only at the Block (goals, shared rules, a method proposal) and the Job (Review and approve, the close);
no Task asks you. The Results reuse design_views' parts, so the focus page and the six-Space page agree; the only
write is the release, design_ladder_act.py's."""
from __future__ import annotations

import re
from pathlib import Path

from live import design_canvas as C
from live import design_reader as R
from live import design_views as V
from live import focus_draft as FD
from live.frame import esc, pop, reader, rel, table
from live.ui_parts import (GROUP_CSS, PB_CSS, PB_JS, PROCESS, PROMPT_CSS, PROMPT_JS, RESULTS, _band, _kv, _numbered, _pill,
                           _section, _side_tabs)

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
MAP_CAPTION = "How it is built, as a map: its parts, and what each must find out."
# what comes after each Task step (task_views.NEXT, b12 j01): the "next: …" pointer under a Task's Work
NEXT = {"inputs": ("🔗 Chains", "chains"), "chains": ("💡 Ideas", "ideas"), "ideas": ("✅ Fence check", "fence-check"),
        "fence-check": ("✏️ the design Tasks · Draft", "design"), "draft": ("🧪 Verify", "verify"),
        "verify": ("🔁 Revise if it failed, 🪜 State if it passed", "revise"), "revise": ("🧪 Verify the new draft", "verify"),
        "state": ("🏆 review whole · Rank", "t99"), "rank": ("🧩 Coverage", "coverage"), "coverage": ("✅ Kept", "kept"),
        "kept": ("the Job · Review and approve", "release")}

# the skills each view's work calls on (the rail's Skills: focus_page.page_skills reads it, 261106)
VIEW_SKILLS = {
    "summary": (("haipipe-design-workflow", "says where each Job stands and which Run is next"),
                ("haipipe-design-delivery", "builds the one-page summary from what the Runs wrote")),
    "goals": (("haipipe-design-goal", "adds a goal and sets the shared rules; a person signs each"),),
    "jobs": (("haipipe-design", "launches a Job: a signed goal × a method version × an inputs version"),
             ("haipipe-design-workflow", "says each Job's next Run and checks its gates")),
    "rounds": (("haipipe-design-goal", "adds the next inputs version, frozen"),
               ("haipipe-design-method", "adds an experiment's per-arm totals")),
    "methods": (("haipipe-design-method", "scores the predictions and proposes the next method version"),),
    "setup": (("haipipe-design-goal", "pins the goal and builds the Job's fence"),
              ("haipipe-design-method", "pins the method version")),
    "ideas": (("haipipe-design-unit", "reasons the ideas, step by step, from the fence only"),
              ("haipipe-design", "checks the fence and opens the design Tasks")),
    "designs": (("haipipe-design-unit", "generates, verifies and revises each design"),
                ("haipipe-design-workflow", "projects a draft and its verdict into the Task")),
    "ranking": (("haipipe-design-unit", "ranks the designs and keeps the top N"),
                ("haipipe-design-workflow", "projects the ranking into each prediction")),
    "release": (("haipipe-design-delivery", "freezes the predictions and releases the kept designs"),
                ("haipipe-design-workflow", "closes the Job once a person signs")),
    "inputs": (("haipipe-design-goal", "builds the fence: inputs/ and its manifest"),),
    "chains": (("haipipe-design-unit", "reasons the chains, each step with its source"),),
    "fence-check": (("haipipe-design", "opens the design Tasks after another agent's fence check"),),
    "draft": (("haipipe-design-unit", "generates the design from its idea"),),
    "verify": (("haipipe-design-unit", "verifies the draft in a fresh context"),),
    "revise": (("haipipe-design-unit", "revises what the verify named, nothing else"),),
    "state": (("haipipe-design-workflow", "projects the verdict and the rank into the Task"),),
    "rank": (("haipipe-design-unit", "ranks the passed designs, a predicted effect each"),),
    "coverage": (("haipipe-design-unit", "checks which parts of the goal the kept cover"),),
    "kept": (("haipipe-design-workflow", "projects kept or dropped onto each design's face"),),
}

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
.dz-close{font-size:13px;margin:2px 0 4px}.pb-state.you{color:light-dark(#b35c00,#ffc078)}
.dz-pick{display:flex;flex-wrap:wrap;gap:6px;align-items:center}.dz-pick select{font:inherit;font-size:13px;border:1px solid var(--line);
 border-radius:6px;padding:2px 6px;background:var(--paper);color:var(--ink)}
.dz-strip{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin:0 0 14px;font-size:13px}
.dz-strip b{font-weight:600;margin-right:4px}.dz-chip{border:1px solid var(--line);border-radius:12px;padding:2px 10px;background:var(--paper)}
.dz-chip.on{border-color:var(--accent);color:var(--accent)}.dz-chip.bad{color:light-dark(#b02a37,#ff8787)}
.dz-next{margin:18px 0 6px;font-size:14px}.dz-next b{font-weight:600}
.dz-verdict{font-size:18px;margin:2px 0 8px}.dz-text{white-space:pre-wrap;font-size:13.5px;line-height:1.5;margin:0}
@media(max-width:600px){.dz-flow{grid-template-columns:1fr}.dz-arrow{transform:rotate(90deg);justify-self:start}
 .pb-chain .pb-step{width:100%}.pb-chain .pb-arrow{transform:rotate(90deg);margin:0}}</style>"""


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
    """Rows like ui_parts._todo, each with its own buttons: [(words html, sub, state, verbs html)]."""
    return '<div class=pb-todos>' + "".join(
        f'<div class=pb-todo><span class=w>{w}' + (f"<small>{esc(s)}</small>" if s else "") + "</span>"
        + _pill(state) + verbs + "</div>" for w, s, state, verbs in rows) + "</div>"


def _plain(html: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", str(html or ""))).strip()


DONE_WORDS = ("done", "closed", "signed", "released", "passed", "kept", "not needed", "approved", "pinned", "dropped")


def _rows_word(rows: list) -> tuple:
    """(state word, waiting line) of a Process section's rows, read from the rows themselves (R1, 261106): how many wait
    for the person and the first of them; else done, running, how many are done, or the first open row's own word."""
    states = [str(r[2] or "").lower() for r in rows]
    if not rows:
        return "nothing yet", ""
    you = [r for r, s in zip(rows, states) if "waiting for you" in s]
    if you:
        return (f'{len(you)} wait{"s" if len(you) == 1 else ""} for you',
                f"🙋 {_plain(you[0][0])}" + (f": {you[0][1]}" if you[0][1] else ""))
    done = sum(s.startswith(DONE_WORDS) for s in states)
    if done == len(states):
        return "done", ""
    if any("running" in s for s in states):
        return "running", ""
    if done:
        return f"{done} of {len(states)} done", ""
    return next(str(r[2]) for r, s in zip(rows, states) if not s.startswith(DONE_WORDS)), ""


def _step(title: str, rows: list, extra: str = "") -> str:
    """A ⚙️ Process section: its rows, its state word and waiting line read from them."""
    word, waits = _rows_word(rows)
    return _section(title, _todo(rows) + extra, word, waits)


def _big(line: str, state: str = "") -> str:
    """A view's main point, large, first (haipipe-ui rule 1: seen at a glance), and its state in a word."""
    you = " you" if "for you" in state or "your" in state else ""
    return f'<p class=pb-big>{esc(line)}</p>' + (f'<p class="pb-state{you}">{esc(state)}</p>' if state else "")


def _tabs(eid: str, items: list) -> str:
    """Side tabs (the one kind of tabs, R4): [(name, state word, panel html)], no count in a name."""
    items = [i for i in items if i[2]]
    return _side_tabs(eid, [(h, w) for h, w, _ in items], [p for _, _, p in items]) if items else ""


def _chain(steps: list) -> str:
    """A row of steps, each a tile with its role above, joined by arrows: [(role, head, line)]."""
    out = []
    for k, (role, head, line) in enumerate(steps):
        if k:
            out.append('<span class=pb-arrow aria-hidden=true>→</span>')
        out.append(f'<div class=pb-step><span class=pb-role>{esc(role)}</span><div class=pb-tile><b>{esc(head)}</b>'
                   f'<span>{esc(line)}</span></div></div>')
    return '<div class=pb-chain>' + "".join(out) + '</div>'


def _tiles(items: list) -> str:
    return ('<div class=pb-tiles>' + "".join(f'<div class=pb-tile><b>{esc(a)}</b><span>{esc(b)}</span></div>'
                                            for a, b in items) + '</div>')


def _link(path: Path, root: Path, words: str) -> str:
    from live import focus_page as F
    return f'<a href="{esc(F.page_url(path, root))}">{esc(words)}</a>'


def _link_btn(path: Path, root: Path, section: str, group: str, verb: str) -> str:
    from live import focus_page as F
    return f'<a class=fd-btn href="{esc(F.page_url(path, root, section, group))}">{esc(verb)}</a>'


def _closed(r: dict | None) -> bool:
    return bool(r) and str(r.get("status", "")).lower() in ("closed", "done", "ok", "passed")


def _has(rs: list, rtype: str) -> bool:
    return any(_closed(r) for r in rs if r["type"] == rtype)


def _cap(text: str) -> str:
    return text[:1].upper() + text[1:]


def _head_css() -> str:
    return PB_CSS + GROUP_CSS + FD.CSS + PROMPT_CSS + CSS


def _page(caption: str, lead: str, process: str, results: str, report: bool, after: str = "") -> str:
    """A Report view: its lead (a design's drafts strip), its big line and numbered sections, the side tabs' script and
    the fold script (R1: every bar starts closed on Report too). A Work view: the lead, ⚙️ Process (its numbered
    steps), then 📊 Results (the Report's view, by the same function), then where the next step is."""
    body = (lead + _numbered(results) if report else
            lead + _band(PROCESS, _numbered(process)) + _band(RESULTS, _numbered(results)) + after)
    return (_head_css() + f'<p class="view-caption">{esc(_cap(caption))}.</p>' + body + PB_JS + FD.JS + PROMPT_JS + POST_JS)


def _work_map(folder: Path, root: Path):
    """The MindMap as a Work view: its Results only, the Report's map (R6: the mind map is always shown)."""
    def build():
        from live import focus_page as FP
        return _head_css() + f'<p class="view-caption">{esc(MAP_CAPTION)}</p>' + _band(RESULTS, FP.parts_mindmap(folder, root))
    return ("MindMap", build)


def _views(keys, build, report: bool, folder: Path, root: Path) -> dict:
    """{key: (name, build)}: Report the Results only under the plain key, Work Process over Results under `work-<key>`
    (R3: the rail's same-views check and rail_view read them so), the MindMap last in Work (the page adds Report's)."""
    out = {}
    for key, name in keys:
        def make(key=key):
            caption, lead, process, results, after = build(key)
            return _page(caption, lead, process, results, report, after)
        out[key if report else "work-" + key] = (name, make)
    if not report:
        out["work-mindmap"] = _work_map(folder, root)
    return out


# ── where a form belongs (R2: each view its own 🙋 Interaction) ──────────────────────────────────────────────────
ABOUT_JOB = (("ranking", r"\brank"), ("release", r"release|test.?arm|next.?test|send|freeze|predict"),
             ("ideas", r"idea|chain|fence|reason"), ("designs", r"design|draft|verify|revise"),
             ("setup", r"goal|method|input|pin|setup"))
ABOUT_BLOCK = (("goals", r"goal|rule"), ("rounds", r"round|inputs|observed|experiment"),
               ("methods", r"method|score|predict"), ("jobs", r"\bjob|launch"))


def view_of_item(row: dict, folder: Path, root: Path, level: str, keys) -> str | None:
    """The view whose 🙋 Interaction shows a form, by what it is about: at a Block, a Job's or a Task's form under Jobs,
    the Block's own by its words (goals, rounds, methods), else Summary; at a Job, a Task's form under its step's view
    (t00 Ideas, a design Designs, t99 Ranking), the Job's own by its words, else Release; at a Task, its first step's
    view unless its words name another. None leaves it to the page's default."""
    page = Path(row.get("page") or folder)
    topic = row.get("topic")
    about = " ".join(str(x or "") for x in (getattr(topic, "name", ""), row.get("about"), row.get("title"))).lower()
    keys = list(keys)

    def by_words(table_, default):
        return next((k for k, pat in table_ if k in keys and re.search(pat, about)), default)
    if level == "Block":
        return "jobs" if page != folder else by_words(ABOUT_BLOCK, "summary")
    if level == "Job":
        if page != folder:
            kind = R.kind_of(next((p for p in [page, *page.parents] if p.parent == folder), page))
            return {"t00": "ideas", "t99": "ranking"}.get(kind, "designs")
        return by_words(ABOUT_JOB, "release")
    if level == "Task":
        steps = [k for k in keys if k != "mindmap"]
        return next((k for k in steps if re.search(k.replace("-", ".?"), about)), steps[0] if steps else None)
    return None


# ── the Block (s51 Report, s52 Work) ────────────────────────────────────────────────────────────────────────────
def _job_next(j: dict) -> tuple:
    """A Job's next move and its state word, in the method's order."""
    from live.design_ladder_act import ready
    if V._approved(j)[0]:                             # released: the close is yours to sign, then it is done
        return ("closed", "done") if _job_closed(j) else ("close the Job", "waiting for you")
    if j["ranking"] and ready(j["path"])[0]:          # a release ready for your sign comes first
        return "review and approve", "waiting for you"
    if str(j["state"]).lower() == "held":
        return "held: " + _plain(j["hold"]).split(".")[0][:80], "held"
    if not (j["goal"] and j["method"] and j["manifest"]):
        return "set up its pins", "next"
    if not (_closed(j["reason"]) and j["ideas"]):
        return "reason ideas (t00)", "running" if j["reason"] and str(j["reason"]["status"]) == "running" else "next"
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


def _goal_name(b: dict, gid: str) -> str:
    g = next((g for g in b["goals"] if g.get("id") == gid), None)
    return C.goal_words(g) if g else (gid or "no goal yet")


def goal_line(folder: Path, goal: str) -> str:
    """The goal-line of a design Job or Task in words: its pinned goal (G01, or `G01 · <name>`) becomes the goal's aim."""
    gid = R.goal_pin(goal)
    if not gid or level_of(folder) not in ("Job", "Task"):
        return ""
    jdir = folder if level_of(folder) == "Job" else folder.parent
    b = R.board(R.block_of(jdir.parent) or jdir.parent, with_jobs=False)
    return _goal_name(b, gid)


def _where(j: dict) -> str:
    """Where a Job is, in a few words, from what its Runs wrote."""
    short = V._approved(j)[0]
    if short:
        return short.replace("approved", "released") + (" · closed" if _job_closed(j) else "")
    if str(j["state"]).lower() == "held":
        return "held"
    kept = sum(d_state(d) == "kept" for d in j["designs"])
    if j["ranking"]:
        return f"ranked · {kept} kept"
    if j["designs"]:
        passed = sum(1 for d in j["designs"] if d["verifies"] and d["verifies"][-1]["status"] == "passed")
        return f"{passed} of {len(j['designs'])} designs passed"
    if j["ideas"]:
        return f"{len(j['ideas'])} ideas reasoned"
    if j["reason"]:
        return f"reasoning ideas · {j['reason']['status']}"
    return "setting up" if not j["manifest"] else "set up"


def _standing(b: dict) -> tuple:
    """The Block's main point in one sentence, and its state word (as the paper Board's Direction)."""
    jobs, ds = b["jobs"], [d for j in b["jobs"] for d in j["designs"]]
    released = sum(d["state"] == "released" for d in ds)
    waiting = sum(d["state"] == "kept" for d in ds)
    if not jobs:
        return "No Job yet: a signed goal waits for its first Job.", "next: launch a Job"
    if waiting:
        return f"{waiting} kept designs wait for your review; {released} are released.", "waiting for you"
    if released and not b["observed"]:
        return (f"{released} designs released from {len(jobs)} Jobs; the experiment has not come back yet.",
                "next: run the experiment")
    if b["observed"] and not b["scores"]:
        return "The experiment is back; its predictions are not scored yet.", "next: score it"
    if b["scores"]:
        return f"{len(b['scores'])} designs tested and scored against their predictions.", "next: the next round"
    return f"{len(jobs)} Jobs at work; none released yet.", "in progress"


def _b_summary(b: dict, block: Path, root: Path) -> tuple:
    line, state = _standing(b)
    big = _big(line, state) + (f'<p class=dz-close><b>Done when</b> {esc(b["close"])}</p>' if b["close"] else "")
    nexts = [(j, *_job_next(j)) for j in b["jobs"]]
    rows = [(_link(j["path"], root, j["name"]), esc(_where(j)),
             f'{esc(step)} <span class=mut>· {esc(st)}</span>' if st != "done" else '<span class=mut>nothing next</span>')
            for j, step, st in nexts]
    yours = [(j, step) for j, step, st in nexts if st == "waiting for you"]
    agents = [(j, step) for j, step, st in nexts if st in ("next", "running")]
    released = sum(bool(V._approved(j)[0]) for j in b["jobs"])
    word = (f'{len(yours)} wait{"s" if len(yours) == 1 else ""} for you' if yours
            else f"{released} of {len(b['jobs'])} released" if b["jobs"] else "no Job yet")
    waits = f"🙋 {_cap(yours[0][1])} · {yours[0][0]['name']}" if yours else ""
    res = big + _section("📊 Where each Job stands", table(("Job", "where it is", "next"), rows) if rows else
                         '<p class=mut>No Job yet: launch one in Work › Jobs.</p>', word, waits)
    then = state.removeprefix("next: ") if state.startswith("next") else ""
    nxt = _kv([("you", " · ".join(f'{esc(step)} {_link(j["path"], root, j["id"])}' for j, step in yours)),
               ("the agents", " · ".join(f'{_link(j["path"], root, j["id"])} {esc(step)}' for j, step in agents)),
               ("then", esc(then))])
    res += _section("➡️ Next", nxt if nxt != '<dl class=pb-kv></dl>' else '<p class=mut>Nothing next: every Job is closed.</p>',
                    "your move" if yours else "the agents' move" if agents else "nothing next")
    qs = [(pop(reader(p, root), q.get("title", ""), q.get("title", "") + " ↗") if (p := V._report_page(q, b)) else esc(q.get("title", "")),
           esc(V._q_asks(q)), V._st(V._WORD.get(V._q_status(q, b), V._q_status(q, b)).lower())) for q in b["questions"]]
    answered = sum(V._q_status(q, b) == "answered" for q in b["questions"])
    res += _section("❓ What the Block asks", table(("question", "asks", "answer"), qs) if qs else
                    '<p class=mut>No Block question yet: board.md ## Questions.</p>',
                    f"{answered} of {len(qs)} answered" if qs else "no question yet")
    pdf = block / "delivery" / "summary.pdf"
    proc = _step("📄 Build the summary", [(
        "Build the one-page summary", "delivery/summary.pdf, from what the Runs wrote only",
        "done" if pdf.is_file() else "open", _copy("run-build-summary", "Block", block, root))])
    return proc, res


def _rules_file(block: Path) -> dict:
    md = block / "design-goal.md"
    text = md.read_text(encoding="utf-8", errors="ignore") if md.is_file() else ""
    field = lambda k: (re.search(rf"(?m)^{k}:\s*(.*)$", text) or [None, ""])[1].strip().strip("'\"")
    return {"path": md, "version": field("rules"), "signed": field("signed"),
            "rules": V._bullets(md, "Rules"), "leave": V._bullets(md, "Leave out")}


def _goal_panel(g: dict, b: dict, root: Path) -> str:
    jobs = [j for j in b["jobs"] if j["goal"] == g.get("id")]
    return _kv([("aim", esc(g.get("aim", ""))), ("who", esc(g.get("who", ""))), ("venue", esc(g.get("venue", ""))),
                ("N", esc(f'{g.get("n", "")} designs a Job, from N + 5 ideas')),
                ("rules", V._ul([str(r) for r in g.get("rules") or []]) if g.get("rules") else "the shared ones only"),
                ("leave out", esc(g.get("leave-out", "") or "—")),
                ("Jobs", " · ".join(_link(j["path"], root, j["name"]) for j in jobs) or "none yet"),
                ("signed", esc(g.get("signed") or "not yet: a Job pins only a signed goal"))])


def _b_goals(b: dict, block: Path, root: Path) -> tuple:
    goals = b["goals"]
    signed = [g for g in goals if str(g.get("signed", "")).startswith("✅")]
    unsigned = [g for g in goals if g not in signed]
    rules = _rules_file(block)
    big = _big(f"{len(goals)} goals, {len(signed)} signed" if goals else "No goal yet",
               f'{len(unsigned)} wait{"s" if len(unsigned) == 1 else ""} for your sign' if unsigned else "every goal signed")
    tabs = _tabs("goal", [(f'{g.get("id", "")} · {g.get("name", "") or g.get("aim", "")}',
                           "signed " + str(g["signed"]).lstrip("✅ ") if g in signed else "waits for your sign",
                           _goal_panel(g, b, root)) for g in goals])
    res = big + _section("🎯 The goals", tabs or '<p class=mut>No goal yet: board.md ## Goals.</p>',
                         f"{len(signed)} of {len(goals)} signed" if goals else "no goal yet",
                         f'🙋 Sign {unsigned[0].get("id", "")} · {unsigned[0].get("name", "")}: a Job pins only a signed goal'
                         if unsigned else "")
    if rules["path"].is_file():
        body = (_kv([("version", esc(rules["version"] or "—")), ("signed", esc(rules["signed"] or "not yet")),
                     ("file", pop(reader(rules["path"], root), "design-goal.md", "design-goal.md ↗"))])
                + '<p class=mut style="margin:8px 0 2px">Every design keeps, checked on its text alone</p>' + V._ul(rules["rules"])
                + ('<p class=mut style="margin:8px 0 2px">No design may use</p>' + V._ul(rules["leave"]) if rules["leave"] else ""))
        on = rules["signed"].startswith("✅")
        res += _section("📏 The shared rules", body, ("signed " + rules["signed"].lstrip("✅ ")) if on else "waits for your sign",
                        "" if on else "🙋 Sign the shared rules: a Job pins only signed rules")
    else:
        res += _section("📏 The shared rules", '<p class=mut>No shared rules yet: design-goal.md (run-setup-rules).</p>', "none yet")
    rows = [(f'Sign the goal {esc(g.get("id", ""))} · {esc(g.get("name", ""))}', "a Job pins only a signed goal",
             "waiting for you", _copy("run-add-goal-<goal>", "Block", block, root)) for g in unsigned]
    rows += [("Add a goal", "a new line in board.md ## Goals; a person signs it", "open",
              _copy("run-add-goal-<goal>", "Block", block, root)),
             ("Set the shared rules", "design-goal.md: each rule checkable on the text alone",
              "done" if rules["path"].is_file() else "open", _copy("run-setup-rules", "Block", block, root))]
    if rules["path"].is_file() and not rules["signed"].startswith("✅"):
        rows.append(("Sign the shared rules", "a person signs them once; a new version is r<k+1>", "waiting for you",
                     _copy("run-setup-rules", "Block", block, root)))
    return _step("🎯 Goals and rules", rows), res


def _moves(b: dict) -> list:
    """What moves across the grid: each Job against the Job before it on the same goal, one clock at a time (its face's
    `moved:`), in words."""
    rows, last = [], {}
    for j in b["jobs"]:
        a = last.get(j["goal"])
        last[j["goal"]] = j
        if a is None:
            continue
        what = []
        if (a["method"], a["version"]) != (j["method"], j["version"]):
            sees = (j["method_card"].get("steps") or {}).get("① See input", "")
            what.append(f'the method: {C.method_words(a["method"])} {C.version_words(a["version"])} → '
                        f'{C.method_words(j["method"])} {C.version_words(j["version"])}' + (f'; step ① sees {sees}' if sees else ""))
        if a["inputs"] != j["inputs"]:
            what.append(f'the inputs: {C.inputs_words(a["inputs"])} → {C.inputs_words(j["inputs"])}')
        rows.append((a, j, "; ".join(what) or "nothing: the same three pins", len(what)))
    return rows


def _b_jobs(b: dict, block: Path, root: Path) -> tuple:
    href, jobs = _href(root), b["jobs"]
    goals = sorted({j["goal"] for j in jobs})
    methods = sorted({j["method"] for j in jobs})
    released = sum(bool(V._approved(j)[0]) for j in jobs)
    big = _big(f'{len(goals)} goal{"" if len(goals) == 1 else "s"} × {len(methods)} method{"" if len(methods) == 1 else "s"}: '
               f'{len(jobs)} Job{"" if len(jobs) == 1 else "s"}' if jobs else "No Job yet",
               f"{released} of {len(jobs)} released" if jobs else "next: launch a Job")
    res = big + _section("🗺️ Goals × methods", C.matrix(b, root, href), f"{released} of {len(jobs)} released" if jobs else "no Job yet")
    moves = _moves(b)
    mrows = [(f'{_link(a["path"], root, a["id"])} → {_link(j["path"], root, j["id"])}', esc(what),
              "one clock" if n == 1 else "two clocks: not one change" if n > 1 else "none") for a, j, what, n in moves]
    res += _section("🧭 What moves across the grid", table(("from → to", "what changes", "moved"), mrows) if mrows else
                    '<p class=mut>Nothing moved yet: a second Job on a goal moves one clock.</p>',
                    " · ".join(dict.fromkeys(str(j["moved"]) for _a, j, _w, _n in moves)) if moves else "one Job a goal")
    nexts = {j["id"]: _job_next(j) for j in jobs}
    tabs = _tabs("job", [(j["name"], _where(j), V._preview(j, href, root)) for j in jobs])
    res += _section("📋 The Jobs", tabs or '<p class=mut>No Job yet.</p>',
                    f'{sum(st == "next" or st == "running" for _s, st in nexts.values())} at work' if jobs else "no Job yet")
    rows = []
    for j in jobs:
        step, state = nexts[j["id"]]
        verb = (_link_btn(j["path"], root, "work", "work-release", "Review") if step == "review and approve" else
                _copy(f'run-close-{j["id"]}', "Job", j["path"], root, "Close {folder} once its designs are released; frozen.")
                if step == "close the Job" else "")
        rows.append((_link(j["path"], root, j["name"]),
                     f'{_goal_name(b, j["goal"])} × {C.method_words(j["method"])}, {C.version_words(j["version"])}'
                     f' × {C.inputs_words(j["inputs"])} · next: {step}', state, verb))
    proc = _step("🧭 Each Job's next move", rows) if rows else _section("🧭 Each Job's next move",
                                                                        '<p class=mut>No Job yet.</p>', "no Job yet")
    proc += _step("➕ A new Job", [(_picker(b, block, root), "one clock moves at a time: a signed goal × a method version × "
                                    "an inputs version", "open", "")])
    return proc, res


def _picker(b: dict, block: Path, root: Path) -> str:
    """The new-Job pickers: goal ▾ · method ▾ · inputs ▾ and the run card's Copy prompt, the picks added to the prompt
    (PROMPT_JS reads each [data-field] in the box)."""
    goals = [g for g in b["goals"] if str(g.get("signed", "")).startswith("✅")]
    methods = [f"{m} {v}" for m, r in sorted(R.REGISTRY.items()) for v in r.get("versions", {})] or sorted(R.METHODS)
    inputs = [v["id"] for v in b["inputs"]]
    sel = lambda name, opts: (f'<select data-field="{esc(name)}" aria-label="{esc(name)}">'
                              + "".join(f'<option value="{esc(v)}">{esc(w)}</option>' for v, w in opts) + '</select>')
    text = V._kind("run-add-job-<jNN>", "", level="Block")["prompt"].replace("{folder}", rel(block, root))
    tail = f'Run this in the Claude session "{_session(block)}"; start it if it is not running.'
    return (f'<span class="pb-prompt in-copy dz-pick">+ Launch a Job '
            + sel("goal", [(g.get("id", ""), f'{g.get("id", "")} · {g.get("name", "")}') for g in goals] or [("", "no signed goal")])
            + sel("method", [(m, f'{m} · {C.method_words(m.split()[0])}') for m in methods])
            + sel("inputs", [(i, C.inputs_words(i)) for i in reversed(inputs)] or [("", "no inputs version")])
            + f'<button type=button class="fd-btn pb-copy" data-copy="{esc(text)}" data-tail="{esc(tail)}">Copy prompt</button></span>')


def _round_state(b: dict, v: dict) -> tuple:
    js = [j for j in b["jobs"] if j["inputs"] == v["id"]]
    ids = {j["id"] for j in js}
    exps = [e for e in b["observed"] if any(a.get("job") in ids for a in e["arms"])]
    n_rel = sum(d["state"] == "released" for j in js for d in j["designs"])
    n_kept = sum(d["state"] in ("kept", "released") for j in js for d in j["designs"])
    state = ("back from " + ", ".join(e["id"] for e in exps) if exps else "released" if n_rel
             else "running" if js else "no Job yet")
    return js, exps, n_rel, n_kept, state


def _b_rounds(b: dict, block: Path, root: Path) -> tuple:
    href = _href(root)
    rounds = [(k + 1, v, *_round_state(b, v)) for k, v in enumerate(b["inputs"])]
    big = _big("; ".join(f"round {k} {state}" for k, v, *_x, state in rounds).capitalize() + "." if rounds
               else "No round yet: add the first inputs version.",
               f"newest: round {rounds[-1][0]}" if rounds else "next: add an inputs version")
    tabs = []
    for k, v, js, exps, n_rel, n_kept, state in reversed(rounds):
        man = v["manifest"]
        chain = _chain([("inputs", C.inputs_words(v["id"]), f'frozen {man.get("frozen", "—")}'),
                        ("Jobs", " · ".join(j["id"] for j in js) or "none yet", f'{len(js)} on this version'),
                        ("kept", f"{n_kept} designs", f"{n_rel} released"),
                        ("experiment", ", ".join(e["id"] for e in exps) or "not run yet",
                         "per-arm totals back" if exps else "waits on a release")])
        body = chain + _kv([("it holds", esc(" · ".join(dict.fromkeys(str(x.get("part", "")) for x in man.get("parts", []))) or "—")),
                            ("new", esc(man.get("new", "") or "—")),
                            ("Jobs", " · ".join(_link(j["path"], root, j["name"]) for j in js) or "none yet")])
        tabs.append((f"Round {k} · {v['id']}", state, body))
    res = big + _section("🔁 The rounds", _tabs("round", tabs) or '<p class=mut>No inputs version yet: inputs/iN/.</p>',
                         rounds[-1][-1] if rounds else "no round yet")
    kept_rows = []
    for j in b["jobs"]:
        kept = [d for d in j["designs"] if d["state"] in ("kept", "released")]
        rel_ = sum(d["state"] == "released" for d in kept)
        words = (f'{len(kept)} design{"" if len(kept) == 1 else "s"}, ' + ("released" if rel_ == len(kept) else "waits for review")
                 if kept else "none yet: " + _job_next(j)[0])
        kept_rows.append((_link(j["path"], root, j["name"]), esc(C.inputs_words(j["inputs"])),
                          esc(" · ".join(f'{d["id"]} {d["short"]}' for d in kept) or "—"), esc(words)))
    n_kept = sum(d["state"] in ("kept", "released") for j in b["jobs"] for d in j["designs"])
    n_rel = sum(d["state"] == "released" for j in b["jobs"] for d in j["designs"])
    res += _section("📋 What each Job kept", table(("Job", "round", "kept", "where"), kept_rows) if kept_rows else
                    '<p class=mut>No Job yet.</p>', f"{n_kept} kept, {n_rel} released" if kept_rows else "no Job yet")
    res += _section("📥 Inputs versions", V._inputs(b, root, href), f'{len(b["inputs"])} frozen' if b["inputs"] else "none yet")
    nxt = f'i{len(b["inputs"]) + 1}'
    released = any(d["state"] == "released" for j in b["jobs"] for d in j["designs"])
    proc = _step("🔁 The next round", [
        (f"Add the Exp's data", "observed/eNN: per-arm totals only, never rows",
         "done" if b["observed"] else "open" if released else "waits on a release",
         _copy("run-add-observed-<eNN>", "Block", block, root)),
        (f"Add the next inputs version {nxt}", "inputs/iN/: rules, theory, the insight handoff, frozen",
         "open" if b["observed"] else "waits on the experiment", _copy("run-add-inputs-<iN>", "Block", block, root))])
    return proc, res


def _proposals(b: dict) -> list:
    """The method proposals on the Block, each waiting for a person's sign until its Run closes."""
    out = []
    for r in b["runs"]:
        if r["type"] != "propose-method":
            continue
        passes = sorted((r["path"] / "passes").glob("*/proposal.md")) if (r["path"] / "passes").is_dir() else []
        head = next((l[2:].strip() for l in passes[-1].read_text(encoding="utf-8", errors="ignore").splitlines()
                     if l.startswith("# ")), r["target"]) if passes else r["target"]
        out.append((r, re.sub(r"\s*\(.*\)$", "", head), passes[-1] if passes else None))
    return out


def _cost_table(b: dict, root: Path) -> tuple:
    rows, timed = [], 0
    for m in sorted({j["method"] for j in b["jobs"]}):
        for k, j in enumerate(j for j in b["jobs"] if j["method"] == m):
            c = V._cost(j)
            timed += c["per_design"] is not None
            rows.append((esc(f'{C.method_words(m)} {C.version_words(j["version"])}') if k == 0 else "",
                         _link(j["path"], root, j["name"]), esc(V._mins(c["per_design"])),
                         esc(f'{c["rounds"]:.1f}' if c["n"] else "—"), esc(f'{c["first"]} of {c["n"]}' if c["n"] else "—"),
                         esc(c["tokens"])))
    return rows, timed


def _b_methods(b: dict, block: Path, root: Path) -> tuple:
    href, scores = _href(root), list(b["scores"].values())
    hits = sum(s.get("direction") == "✓" for s in scores)
    inr = sum(s.get("in_range") == "✓" for s in scores)
    big = _big(f"{len(scores)} design{'' if len(scores) == 1 else 's'} tested: {hits} in the predicted direction, "
               f"{inr} in range" if scores else "No method scored yet: scores come after the experiment",
               "a hint, not a verdict: few arms tested" if scores else "waits on an experiment")
    res = big + _section("🎯 Predicted vs observed", V._predicted(b, root, href),
                         f"{inr} of {len(scores)} in range" if scores else "not tested yet")
    groups = {}
    for j in b["jobs"]:
        groups.setdefault((j["method"], j["version"]), []).append(j)
    tabs = []
    for (m, v), js in groups.items():
        live = sum((V._live(j["designs"]) for j in js), [])
        sc = [s for (jid, _), s in b["scores"].items() if jid in {j["id"] for j in js}]
        rate = f'{100 * len(V._passed(live)) // max(len(live), 1)}%'
        body = _kv([("type", esc(R.METHODS.get(m, ("", "—"))[1])), ("Jobs", " · ".join(_link(j["path"], root, j["name"]) for j in js)),
                    ("pass rate", esc(rate)), ("first try", esc(f'{sum(d["first_try"] for d in live)} of {len(live)}')),
                    ("tested", esc(f"{len(sc)} designs")), ("direction", esc(f'{sum(s.get("direction") == "✓" for s in sc)} of {len(sc)}')),
                    ("in range", esc(f'{sum(s.get("in_range") == "✓" for s in sc)} of {len(sc)}'))])
        tabs.append((f"{C.method_words(m)} · {v}", f"pass {rate}", body))
    res += _section("🏅 Method scorecard", _tabs("method", tabs) or '<p class=mut>No Job yet.</p>',
                    f"{len(groups)} method version{'' if len(groups) == 1 else 's'} at work" if groups else "no Job yet")
    rows, timed = _cost_table(b, root)
    res += _section("⏱️ What each Job cost, by method",
                    table(("method", "Job", "time a design", "drafts a design", "first try", "tokens a design"), rows)
                    + '<p class=mut>Time from each Run\'s started_at → finished_at; tokens once a receipt has usage:.</p>'
                    if rows else '<p class=mut>No Job yet.</p>', f"{timed} of {len(rows)} timed" if rows else "no Job yet")
    props = _proposals(b)
    rows = [(f'Agree the method proposal {esc(head)}', "the registry cuts the next version only when a person signs",
             "done" if _closed(r) else "waiting for you",
             pop(reader(p, root), "proposal.md", "Open") if p else "") for r, head, p in props]
    rows += [("Score the predictions", "each Exp arm against its frozen prediction",
              "done" if b["scores"] else "waits on an Exp" if not b["observed"] else "open",
              _copy("run-score-<eNN>", "Block", block, root)),
             ("Propose a method change", "from the scores; the registry cuts the next version", "open",
              _copy("run-propose-method-<slug>", "Block", block, root))]
    return _step("📏 Score and learn", rows), res


BLOCK_PARTS = {"summary": _b_summary, "goals": _b_goals, "jobs": _b_jobs, "rounds": _b_rounds, "methods": _b_methods}


def block_view(block: Path, root: Path, key: str) -> tuple:
    """(caption, lead, process, results, after) of a Block view."""
    proc, res = BLOCK_PARTS[key](R.board(block), block, root)
    return CAPTIONS[key], "", proc, res, ""


# ── the Job (s54 Report, s55 Work) ──────────────────────────────────────────────────────────────────────────────
def _chain_words(d: dict) -> str:
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


def _j_setup(j: dict, b: dict, jdir: Path, root: Path) -> tuple:
    href, jid = _href(root), j["id"]
    pins = (("Goal", bool(j["goal"]), "setup-goal"), ("Method", bool(j["method"]), "setup-method"),
            ("Inputs", bool(j["manifest"]), "setup-inputs"))
    n = sum(ok for _w, ok, _t in pins)
    big = _big(f'{_goal_name(b, j["goal"])} × {C.method_words(j["method"])}, {C.version_words(j["version"])} × '
               f'{C.inputs_words(j["inputs"])}', "all three pinned" if n == 3 else f"{n} of 3 pinned")
    man = j["manifest"]
    res = (big + _section("🎯 Goal", V._setup_strip(j) + V._job_goal(j, b, root), f'{j["goal"]} pinned' if j["goal"] else "not pinned")
           + _section("🧩 Method", V._job_method(j, b, root, href=href), f'{j["method"]} {j["version"]}' if j["method"] else "not pinned")
           + _section("📥 Inputs", V._job_inputs(j, b, root, fold=False),
                      f'{j["inputs"]} · frozen {man.get("frozen", "—")}' if man else "no fence yet"))
    proc = _step("📌 The three pins", [
        (f"Set up the {w.lower()}", {"Goal": f'pinned: {j["goal"] or "—"}', "Method": f'{j["method"]} {j["version"]}'.strip()
                                     or "—", "Inputs": f'{j["inputs"] or "—"} · its manifest frozen'}[w],
         "done" if ok else "next", "" if ok else _copy(f"run-{t}-{jid}", "Job", jdir, root)) for w, ok, t in pins])
    return proc, res


def _chain_panel(t: dict, words: dict) -> str:
    steps = t.get("steps") or []
    rows = [(esc(k + 1), esc(s.get("says", "")), esc(s.get("so", "")), esc(s.get("from", "") or t.get("from", "")))
            for k, s in enumerate(steps)]
    return (f'<p class=mut style="margin:0 0 6px">from {esc(t.get("from", ""))}</p>'
            + (table(("step", "says", "so", "from"), rows) if rows else "")
            + '<p style="margin:8px 0 0"><b>Ideas</b> ' + " · ".join(V._id(i, words.get(str(i), "")) for i in t.get("ideas", []))
            + '</p>')


def _j_ideas(j: dict, b: dict, jdir: Path, root: Path) -> tuple:
    href, jid = _href(root), j["id"]
    opened = bool(j["designs"]) or _has(j["runs"], "open-designs")
    fence = _fence_verdict(jdir)
    big = _big(f'{len(j["topics"])} chains → {len(j["ideas"])} ideas' if j["ideas"] else "No idea reasoned yet",
               ("fence check: " + fence[0]) if fence else "the fence check comes next" if j["ideas"] else "next: reason ideas (t00)")
    words = V._ideas_text(j)
    res = big + _section("🔗 Where each design came from", C.lineage(j, href) or '<p class=mut>Nothing reasoned yet.</p>',
                         f'{len(j["designs"])} designs traced' if j["designs"] else "nothing traced yet")
    tabs = _tabs("chain", [(str(t.get("title") or t.get("id", "")), str(t.get("from", "")).split(" · ")[0], _chain_panel(t, words))
                           for t in j["topics"]])
    res += _section("🔗 Chains", tabs or '<p class=mut>Nothing reasoned yet.</p>',
                    f'{len(j["topics"])} chains' if j["topics"] else "nothing yet")
    n_open = sum(1 for i in j["ideas"] if any(d["id"] == i.get("design") for d in j["designs"]))
    res += _section("💡 The ideas", V._t00_ideas(j, href) if j["ideas"] else '<p class=mut>No idea yet.</p>',
                    f'{n_open} of {len(j["ideas"])} opened as designs' if j["ideas"] else "no idea yet")
    proc = _step("💡 Reason, then open", [
        ("Reason ideas (t00)", f'{len(j["topics"])} topics → {len(j["ideas"])} ideas, from inputs/ only',
         "done" if _closed(j["reason"]) and j["ideas"] else "running" if j["reason"] and j["reason"]["status"] == "running" else "next",
         "" if j["ideas"] else _copy("run-reason-t00", "Task", j["t00"] or jdir, root)),
        ("Check the fence, open the design Tasks", "another agent; one Task per idea, only after a pass",
         "done" if opened else "next" if j["ideas"] else "waits on the ideas",
         "" if opened else _copy(f"run-open-designs-{jid}", "Job", jdir, root))])
    return proc, res


def _j_designs(j: dict, b: dict, jdir: Path, root: Path) -> tuple:
    href, ds = _href(root), j["designs"]
    kept = [d for d in ds if d_state(d) in ("kept", "released")]
    dropped = [d for d in ds if d_state(d) == "dropped"]
    revised = sum(len(d["drafts"]) > 1 for d in ds)
    big = _big(f'{len(ds)} designs: {len(kept)} kept, {len(dropped)} dropped, {revised} revised' if ds else "No design yet",
               ("released" if any(d_state(d) == "released" for d in ds) else "waits for your review" if kept
                else "at work") if ds else "the fence check opens them")
    order = kept + [d for d in ds if d not in kept and d not in dropped] + dropped
    tabs = _tabs("design", [(f'{d["id"]} · {d["short"]}', _design_state(d), V._qhead("Design", "Process (③)", "Review (④ ⑤)")
                             + V._card(d, j, href, root)) for d in order])
    res = big + _section("✏️ The designs, as they read", tabs or '<p class=mut>No design Task yet: the fence check opens them.</p>',
                         f"{len(kept)} kept of {len(ds)}" if ds else "no design yet")
    rows = [(_link(d["path"], root, f'{d["id"]} · {d["short"]}'), _chain_words(d), _design_state(d), "") for d in ds]
    proc = (_step("✏️ Each design's next Run", rows) if rows else
            _section("✏️ Each design's next Run", "<p class=mut>No design Task yet: the fence check opens them.</p>", "waits on the fence check"))
    return proc, res


def _j_ranking(j: dict, b: dict, jdir: Path, root: Path) -> tuple:
    href = _href(root)
    kept = sum(r.get("kept") == "yes" for r in j["ranking"])
    big = _big(f'Ranked {len(j["ranking"])}; kept {kept} of N = {j["n"]}' if j["ranking"] else "Not ranked yet",
               "ranked by another agent" if j["ranking"] else "waits on the designs" if not j["designs"] else "next: t99")
    res = big + _section("🏆 Ranking", V._review_whole(j, b, root, href), f"{kept} kept" if j["ranking"] else "not ranked yet")
    res += _section("🧭 Coverage", _coverage(j, root), "checked" if _coverage_md(j) else "from the kept" if j["ranking"] else "not yet")
    proc = _step("🏆 Review the whole (t99)", [(
        "Rank, keep the top N, a predicted effect each", "another agent, in a fresh context",
        "done" if _closed(j["rank"]) and j["ranking"] else "next" if j["designs"] else "waits on the designs",
        "" if j["ranking"] else _copy("run-rank-t99", "Task", j["t99"] or jdir, root))])
    return proc, res


def _frozen(j: dict) -> tuple:
    rows, frozen = [], set()
    for d in j["designs"]:
        p = d["prediction"] if isinstance(d["prediction"], dict) else {}
        if not p.get("predicted") or d_state(d) not in ("kept", "released"):
            continue
        frozen.add(str(p.get("frozen") or "draft"))
        rows.append((f'{esc(d["id"])} · {esc(d["short"])}', esc(p.get("predicted", "")), esc(p.get("against") or "the control"),
                     esc(p.get("why", "")), V._st(str(p.get("frozen") or "draft"))))
    return rows, frozen


def _j_release(j: dict, b: dict, jdir: Path, root: Path) -> tuple:
    from live.design_ladder_act import ready
    href = _href(root)
    designs, why = ready(jdir)
    approved = V._approved(j)[0]
    closed = _job_closed(j)
    tested = [d for d in j["designs"] if R.arm_of(b, j["id"], d["id"])]
    if approved:
        big = _big(f'{_cap(approved.replace("approved", "released"))}' + (f'; tested in {R.arm_of(b, j["id"], tested[0]["id"])["exp"]}'
                                                                          if tested else ""),
                   "closed" if closed else "waiting for you: the close")
    elif designs:
        big = _big(f'{len(designs)} kept design{"" if len(designs) == 1 else "s"} wait for your review and approval',
                   "waiting for you")
    else:
        big = _big("Nothing to release yet", "waits on " + (why.split(":")[0][:60] if why else "the ranking"))
    res = big + _section("📄 Released designs", V._job_delivery(j, root, "designs.md"),
                         "released" if j["delivered"] else "not yet")
    rows, frozen = _frozen(j)
    fword = ("frozen " + next(iter(frozen)) if len(frozen) == 1 and "draft" not in frozen else
             "draft: freezes at your sign" if designs else "draft" if rows else "nothing kept yet")
    res += _section("🔒 Frozen predictions", table(("design", "predicted", "against", "why", "frozen"), rows) if rows else
                    '<p class=mut>No kept design yet: t99 keeps the top N, each with its prediction.</p>', fword)
    res += _section("🎯 Predicted vs observed", V._job_observed(j, b, root, href),
                    "tested in " + R.arm_of(b, j["id"], tested[0]["id"])["exp"] if tested else "not tested yet")
    rel_state = "done" if approved else "waiting for you" if designs else "waits on " + (why.split(":")[0][:60] if why else "the ranking")
    rows = [("Review and approve", "read each kept design, its prediction and why; one sign freezes and releases", rel_state, ""),
            ("Close the Job", "once every design is released or dropped; you sign",
             "done" if closed else "waits on the release" if not approved else "waiting for you",
             _copy(f'run-close-{j["id"]}', "Job", jdir, root, "Close {folder} once its designs are released; frozen.")
             if approved and not closed else "")]
    panel = V._approve_panel(j, jdir, root, head=False) if designs or approved else ""
    return _step("✍️ Review and approve, then close", rows, panel), res


JOB_PARTS = {"setup": _j_setup, "ideas": _j_ideas, "designs": _j_designs, "ranking": _j_ranking, "release": _j_release}


def job_view(jdir: Path, root: Path, key: str) -> tuple:
    """(caption, lead, process, results, after) of a Job view."""
    j = R.job(jdir)
    b = R.board(R.block_of(jdir.parent) or jdir.parent, with_jobs=False)
    proc, res = JOB_PARTS[key](j, b, jdir, root)
    return CAPTIONS[key], "", proc, res, ""


# ── the Task (s57 Report, s58 Work), by type ────────────────────────────────────────────────────────────────────
def _flow(inn: tuple, who: tuple, out: tuple) -> str:
    box = lambda word, head, line: f'<div><small>{esc(word)}</small><b>{esc(head)}</b>{esc(line)}</div>'
    arrow = '<span class=dz-arrow aria-hidden=true>→</span>'
    return f'<div class=dz-flow>{box("In", *inn)}{arrow}{box("Who works", *who)}{arrow}{box("Out", *out)}</div>'


NONE = '<p class=dz-part>Your part: none here; an agent works, another agent checks. You sign at the Job.</p>'


def task_steps(tdir: Path) -> tuple:
    icon, typ, steps = TASK_STEPS[R.kind_of(tdir)]
    return icon, typ, steps


def _key(step: str) -> str:
    return re.sub(r"\W+", "-", step.lower())


def _section_of(path: Path, heading: str) -> str:
    """The text under a `Heading\\n-----` (or `## Heading`) in a review file, up to the next heading."""
    if not path.is_file():
        return ""
    text = path.read_text(encoding="utf-8", errors="ignore")
    m = re.search(rf"(?ms)^(?:##\s+)?{re.escape(heading)}\s*\n(?:-+\s*\n)?(.*?)(?=^\S[^\n]*\n-{{3,}}\s*$|^##\s|\Z)", text)
    return m.group(1).strip() if m else ""


def _md_lines(text: str) -> str:
    """A short Markdown body as paragraphs and bullets, its **bold** and `code` kept as plain words."""
    out, items = [], []
    clean = lambda s: esc(re.sub(r"\*\*|`", "", s))
    for line in text.splitlines():
        if line.startswith("- "):
            items.append(f"<li>{clean(line[2:])}</li>")
            continue
        if items:
            out.append("<ul style='margin:4px 0;padding-left:18px'>" + "".join(items) + "</ul>")
            items = []
        if line.strip():
            out.append(f"<p style='margin:4px 0'>{clean(line)}</p>")
    if items:
        out.append("<ul style='margin:4px 0;padding-left:18px'>" + "".join(items) + "</ul>")
    return "".join(out)


def _fence_verdict(jdir: Path) -> tuple | None:
    """(verdict, steps checked, steps outside) of the newest fence check of run-open-designs-jNN, or None."""
    run = jdir / "runs" / f"run-open-designs-{jdir.name.split('_')[0]}"
    checks = sorted((run / "passes").glob("*/fence-check.md")) if (run / "passes").is_dir() else []
    if not checks:
        return None
    text = checks[-1].read_text(encoding="utf-8", errors="ignore")
    inside = len(re.findall(r"(?m)^- .*:\s*inside\b", text))
    outside = len(re.findall(r"(?m)^- .*:\s*outside\b", text))
    return ("fail" if outside else "pass"), inside + outside, outside


def _stays_out(j: dict, b: dict, root: Path) -> tuple:
    """What stays out of the fence: the Block's inputs version files the method's step ① does not see, and what no
    design may use (the goal's leave-out, the shared rules' leave-out list)."""
    version = next((v for v in b["inputs"] if v["id"] == j["inputs"]), None)
    have = {f["name"].rstrip("/") for f in j["files"]}
    files = sorted(p.name for p in version["path"].iterdir() if p.is_file() and p.name != "manifest.yaml"
                   and p.name not in have) if version and version["path"].is_dir() else []
    seen = V._keyed(j["fence"] / "goal.md")
    leave = [x for x in ([seen.get("leave out", "")] + V._bullets(j["fence"] / "rules.md", "Leave out")) if x]
    sees = (j["method_card"].get("steps") or {}).get("① See input", "")
    body = _kv([("not in the fence", esc(" · ".join(files)) + (f' <span class=mut>(in {esc(C.inputs_words(j["inputs"]))}; '
                                                              f'{esc(C.method_words(j["method"]))}\'s step ① does not see it)</span>'
                                                              if files else "") if files else "every file of the inputs version is in"),
                ("step ① sees", esc(sees or "—")), ("no design may use", V._ul(leave) if leave else "—")])
    return body, (f'{len(files)} file{"" if len(files) == 1 else "s"} left out' if files else "nothing left out")


def _topics(j: dict) -> str:
    return _tiles([(str(t.get("title") or t.get("id", "")),
                    f'{len(t.get("ideas", []))} idea{"" if len(t.get("ideas", [])) == 1 else "s"} · from '
                    f'{str(t.get("from", "")).split(" · ")[0]}') for t in j["topics"]])


def _opened_chain(j: dict) -> str:
    ds = j["designs"]
    names = (ds[0]["name"] + (f" … {ds[-1]['name']}" if len(ds) > 1 else "")) if ds else "none yet"
    return _chain([("② ideas", "t00", (j["t00"].name if j["t00"] else "not opened")),
                   ("③ ④ designs", f'{len(ds)} design Task{"" if len(ds) == 1 else "s"}', names),
                   ("⑤ rank", "t99", j["t99"].name if j["t99"] else "not opened")])


def _feedback(d: dict) -> tuple:
    """The frozen feedback each failed verify gave, and what the revise read: (html, word)."""
    out = []
    for i, v in enumerate(d["verifies"]):
        if v["status"] != "failed":
            continue
        review = v["result"] / "review.md"
        change = _section_of(review, "What to change")
        tests = " · ".join(f"{V.TESTS.get(t, t)} {r}" for t, r in (v["card"].get("tests") or {}).items())
        out.append(f'<p style="margin:0 0 4px"><b>{esc(v["run"])}</b> <span class=mut>· {esc(tests)} · {esc(v["by"])}</span></p>'
                   + (_md_lines(change) if change else '<p class=mut>Its review names no change.</p>')
                   + (f'<p class=mut style="margin:4px 0 10px">{pop(reader(review, d["path"].parents[3]), "review.md", "review.md ↗")}</p>'
                      if review.is_file() else ""))
    if not out:
        return "", ""
    return "".join(out), f'{len(out)} failed verify' + ("" if len(out) == 1 else "s")


def _changes(d: dict, root: Path) -> tuple:
    """What each revise changed: the draft before beside the draft after, and the pass's own summary."""
    files = V.draft_files(d)
    if len(files) < 2:
        return "", ""
    venue = R.venue_of(d["path"])
    rows = []
    for k in range(1, len(files)):
        (r0, f0), (r1, f1) = files[k - 1], files[k]
        before = f0.read_text(encoding="utf-8", errors="ignore") if f0.is_file() else ""
        after = f1.read_text(encoding="utf-8", errors="ignore") if f1.is_file() else ""
        summary = _section_of(f1.parent / "pass.md", "Summary")
        rows.append((f"draft {k} → {k + 1}", V.as_read(before, venue, small=True), V.as_read(after, venue, small=True),
                     esc(summary or "—")))
    return table(("drafts", "before", "after", "what changed"), rows), f"{len(rows)} revise pass" + ("" if len(rows) == 1 else "es")


def _walk(d: dict, j: dict) -> tuple:
    """A design's state walk (haipipe-design-workflow): draft → verify → revise → passed → kept | dropped → released,
    each step with its word."""
    steps = [("③ draft", "v1", "done" if d["drafts"] else "not yet")]
    for i, v in enumerate(d["verifies"]):
        steps.append((f"④ verify v{i + 1}", v["status"], v["by"].split(" (")[0] or "another agent"))
        if v["status"] == "failed" and i + 1 < len(d["drafts"]):
            steps.append(("revise", f"v{i + 2}", "done"))
    state = d_state(d)
    steps.append(("⑤ rank", state if state in ("kept", "dropped", "released") else "not ranked yet", "by t99"))
    if state != "dropped":
        steps.append(("release", "released" if state == "released" else "not yet", "a person signs at the Job"))
    return _chain(steps), state if state in ("kept", "dropped", "released") else _design_state(d)


def _strip(d: dict) -> str:
    """The drafts strip, above every view of a design Task (b12 j01 B1 to B4): v1 · v2 · kept."""
    chips = []
    for i, _draft in enumerate(d["drafts"]):
        v = d["verifies"][i] if i < len(d["verifies"]) else None
        word = ("verify " + v["status"]) if v else "to verify"
        bad = " bad" if v and v["status"] == "failed" else ""
        on = " on" if i == len(d["drafts"]) - 1 else ""
        chips.append(f'<span class="dz-chip{bad}{on}">v{i + 1} · {esc(word)}</span>')
    state = d_state(d)
    if state in ("kept", "dropped", "released"):
        chips.append(f'<span class=dz-chip>{esc(state)} · {"by t99" if state != "released" else "at the Job"}</span>')
    if not chips:
        chips.append('<span class=dz-chip>not drafted yet</span>')
    return f'<p class=dz-strip><b>✏️ Drafts of {esc(d["id"])}</b>' + ' <span class=mut>→</span> '.join(chips) + '</p>'


def _coverage_md(j: dict) -> Path | None:
    p = j["rank"]["path"] / "result" / "coverage.md" if j["rank"] else None
    return p if p and p.is_file() else None


def _coverage(j: dict, root: Path) -> str:
    md = _coverage_md(j)
    said = _section_of(md, "Does the kept design cover the goal") if md else ""
    return V._coverage(j) + (_md_lines(said) + f'<p class=mut>{pop(reader(md, root), "coverage.md", "coverage.md ↗")}</p>'
                             if said else "")


def _next_link(tdir: Path, root: Path, key: str) -> str:
    """The "next: …" pointer under a Task's Work: the next step's view, in this Task or the next one."""
    if key not in NEXT:
        return ""
    words, to = NEXT[key]
    j = tdir.parent
    if to == "design":
        target = next((p for p in sorted(j.iterdir()) if R.DESIGN_TASK.match(p.name)), None)
        group = "work-draft"
    elif to == "t99":
        target, group = next(iter(sorted(j.glob("t99_*"))), None), "work-rank"
    elif to == "release":
        target, group = j, "work-release"
    else:
        target, group = tdir, "work-" + to
    link = _link_btn(target, root, "work", group, words) if target is not None else esc(words)
    return f'<p class=dz-next><b>next:</b> {link}</p>'


def task_view(tdir: Path, root: Path, step: str) -> tuple:
    """(caption, process, results) of one step of a Task: its flow and row, then what the step wrote."""
    j, href = R.job(tdir.parent), _href(root)
    b = R.board(R.block_of(tdir.parent.parent) or tdir.parent.parent)
    kind, jid = R.kind_of(tdir), j["id"]
    icon, typ, _steps = TASK_STEPS[kind]
    opened = bool(j["designs"]) or _has(j["runs"], "open-designs")
    if kind == "t00":
        fence = _fence_verdict(tdir.parent)

        def inputs_res():
            out, word = _stays_out(j, b, root)
            return (_section("📂 What the fence holds", V._job_inputs(j, b, root, fold=False),
                             f'{len(j["files"])} files · frozen {j["manifest"].get("frozen", "—")}' if j["manifest"] else "no fence yet")
                    + _section("🚫 What stays out", out, word))

        def fence_res():
            ds = j["designs"]
            verdict = (f'<p class=dz-verdict>{esc(fence[0])} · {fence[2]} of {fence[1]} steps outside the fence</p>'
                       if fence else '<p class=mut>Not checked yet: another agent checks the fence before any design Task opens.</p>')
            rows = [(_link(d["path"], root, f'{d["id"]} · {d["short"]}'), esc(d["idea"]), V._st(d["state"])) for d in ds]
            return (_section("✅ The verdict", verdict, fence[0] if fence else "not checked yet")
                    + _section("📂 Tasks opened", _opened_chain(j) + (table(("design", "idea", "state"), rows) if rows else ""),
                               f'{len(ds)} design Tasks' if ds else "none yet"))
        spec = {"Inputs": (("Inputs version", j["inputs"] or "—"), ("🤖 Designer agent", "keep what step ① names"),
                           ("inputs/ + manifest.yaml", "every file the work may read"),
                           "done" if j["manifest"] else "next", f"run-setup-inputs-{jid}", "Job", tdir.parent, inputs_res),
                "Chains": (("inputs/", "goal · method · rules"), ("🤖 Designer agent", "② reason, step by step"),
                           ("chains.yaml", "each step and its source"),
                           "done" if j["topics"] else "next", "run-reason-t00", "Task", tdir,
                           lambda: (_section("🔗 Reasoning chains", V._t00_chains(j), f'{len(j["topics"])} chains')
                                    + _section("🧭 Topics", _topics(j), f'{len(j["topics"])} topics'))
                           if j["topics"] else ""),
                "Ideas": (("chains.yaml", "the reasoning"), ("🤖 Designer agent", "one idea per chain's end"),
                          ("ideas.yaml", f'{len(j["ideas"])} ideas'),
                          "done" if j["ideas"] else "next", "run-reason-t00", "Task", tdir,
                          lambda: _section("💡 The ideas", V._t00_ideas(j, href), f'{len(j["ideas"])} ideas') if j["ideas"] else ""),
                "Fence check": (("chains.yaml", "every step's from: line"), ("🤖 Reviewer agent", "a fresh context"),
                                ("fence-check.md", "pass, then the design Tasks open"),
                                "done" if opened else "next" if j["ideas"] else "waits on the ideas",
                                f"run-open-designs-{jid}", "Job", tdir.parent, fence_res)}
    elif kind == "design":
        d = R.design(tdir)
        did = d["id"]
        state = _design_state(d)
        k = len(V.draft_files(d))                       # drafts so far: the generate's, then one per revise pass
        revised = max(k - 1, 0)

        def verify_res():
            fb, word = _feedback(d)
            return (_section("🧪 Tests", V._tests(d, j, b, root), d["verifies"][-1]["status"] if d["verifies"] else "not yet")
                    + _section("📝 Feedback", fb or '<p class=mut>No feedback to act on: every verify passed.</p>',
                               word or ("none needed" if d["verifies"] else "not verified yet")))

        def revise_res():
            ch, word = _changes(d, root)
            return (_section("↔️ What changed", ch or '<p class=mut>Not revised: it needed no revise.</p>', word or "not needed")
                    + _section("🔁 The loop", f'<p style="margin:0 0 6px">{esc(_chain_words(d))}</p><p class=mut>fail → revise '
                               'what the verify named → verify again, until it passes or t99 drops it</p>', state)
                    + _section("📄 Drafts", V._drafts(d, j, b, root), f'{k} draft{"" if k == 1 else "s"}' if k else "none yet"))

        def state_res():
            walk, word = _walk(d, j)
            return (_section("🪜 Its walk", walk, word)
                    + _section("📊 Its prediction", V._task_perf(d, j, b, root),
                               str((d["prediction"] or {}).get("frozen") or ("draft" if d["prediction"] else "none yet"))))
        spec = {"Draft": ((f'Idea {d["idea"] or "—"}', "from t00's ideas.yaml, and inputs/ only"),
                          ("🤖 Designer agent", "③ conduct the method's process"), ("Draft + elements.yaml", f'{k} draft{"" if k == 1 else "s"}'),
                          "done" if d["drafts"] else "next", f"run-generate-{did}", "Task", tdir,
                          lambda: (_section("📄 The design, as it reads", V._design(d, j, href, root), state)
                                   + _section("🧩 Elements and sources", V._elements(d),
                                              f'{len(d["elements"])} elements' if d["elements"] else "none yet"))),
                "Verify": (("The last draft", "the design + elements.yaml"), ("🤖 Reviewer agent", "④ T0 rules · T1 sources, fresh"),
                           ("verdict", d["verifies"][-1]["status"] if d["verifies"] else "not yet"),
                           "done" if d["verifies"] and d["verifies"][-1]["status"] == "passed" else
                           "next" if d["drafts"] else "waits on the draft", f"run-verify-{did}-v{max(k, 1)}", "Task", tdir, verify_res),
                "Revise": (("A failed verify", "its notes"), ("🤖 Designer agent", "one more draft, then verify again"),
                           ("Draft v" + str(k + 1 if state == "revise next" else k),
                            f"{revised} revision{'' if revised == 1 else 's'}"),
                           "next" if state == "revise next" else "done" if revised else "not needed",
                           f"run-revise-{did}", "Task", tdir, revise_res),
                "State": (("t99's ranking", "rank and kept"), ("🤖 Reviewer agent", "⑤ at t99; you sign at the Job"),
                          ("prediction.yaml", str((d["prediction"] or {}).get("frozen") or "draft")),
                          {"kept": "kept", "released": "done", "dropped": "dropped"}.get(d_state(d), state),
                          "", "Task", tdir, state_res)}
    else:
        kept = [d for d in j["designs"] if d_state(d) in ("kept", "released")]
        dropped = [d for d in j["designs"] if d_state(d) == "dropped"]
        failed = [d for d in j["designs"] if d["verifies"] and d["verifies"][-1]["status"] == "failed"]

        def kept_res():
            approved = V._approved(j)[0]
            to = (f'<p style="margin:0 0 6px">The kept go to the Job\'s Review and approve, where a person signs once: the '
                  f'predictions freeze and the designs are released.</p>'
                  + _link_btn(j["path"], root, "work", "work-release", "Open the Job's Release"))
            return (_section("✅ Kept and dropped", _tiles([(str(len(kept)), f'kept: the goal\'s N = {j["n"]}'),
                                                           (str(len(dropped)), "dropped, kept for the record"),
                                                           (str(len(failed)), "failed their last verify")])
                             + V._kept(j, href), f"{len(kept)} kept" if j["ranking"] else "not ranked yet")
                    + _section("➡️ To the release", to, approved.replace("approved", "released") if approved
                               else "at the Job" if kept else "waits on the ranking"))
        spec = {"Rank": (("The designs", f'{len(j["designs"])} drafted'), ("🤖 Reviewer agent", "⑤ rank, a predicted effect each"),
                         ("ranking.csv", "rank · predicted · why · kept"),
                         "done" if _closed(j["rank"]) and j["ranking"] else "next" if j["designs"] else "waits on the designs",
                         "run-rank-t99", "Task", tdir,
                         lambda: _section("🏆 Ranking", V._review_whole(j, b, root, href),
                                          f'{len(kept)} kept' if j["ranking"] else "not ranked yet")),
                "Coverage": (("ranking.csv", "the kept designs"), ("🤖 Reviewer agent", "which parts of the goal they cover"),
                             ("coverage", "by goal part"), "done" if j["ranking"] else "waits on the ranking", "", "Task", tdir,
                             lambda: _section("🧩 Goal parts", _coverage(j, root),
                                              "checked" if _coverage_md(j) else "from the kept" if j["ranking"] else "not yet")),
                "Kept": (("ranking.csv", "the top N"), ("🤖 Reviewer agent", "projected onto each design's face"),
                         ("kept", f'{len(kept)} of N = {j["n"]}'), "done" if kept else "waits on the ranking", "", "Task", tdir,
                         kept_res)}
    inn, who, out, state, label, level, folder, result = spec[step]
    row = [(f'{icon} {esc(step)}', f"{typ} · {who[0].split(' ', 1)[-1]}", state,
            _copy(label, level, folder, root) if label and state in ("next", "revise next") else "")]
    part = NONE
    if kind == "t99" and step == "Kept":
        part = (f'<p class=dz-part>Your part is at the Job: {_link_btn(j["path"], root, "work", "work-release", "Review and approve")}'
                f' freezes the kept designs\' predictions and releases them.</p>')
    proc = _step(f"{icon} {step}", row, _flow(inn, who, out) + part)
    res = result() or _section(f"📊 {step}", "<p class=mut>Nothing here yet.</p>", "nothing yet")
    return f"{typ} · {step}: what the step reads, who works, what it writes", proc, res


def _task_build(tdir: Path, root: Path, key: str, steps: tuple) -> tuple:
    step = next(s for s in steps if _key(s) == key)
    caption, proc, res = task_view(tdir, root, step)
    lead = _strip(R.design(tdir)) if R.kind_of(tdir) == "design" else ""
    return caption, lead, proc, res, _next_link(tdir, root, key)


# ── what focus_page.py asks ─────────────────────────────────────────────────────────────────────────────────────
def views(folder: Path, root: Path, section: str, items=(), item_html=None) -> dict:
    """{key: (name, build)} for the page's Report (section "report", plain keys; the page adds the MindMap last) or
    Work (`work-<key>`, its MindMap last); {} for a folder that is not a design Block, Job or Task on the ladder, so the
    base page stays. `items` and `item_html` are not drawn here: the page's own 🙋 Interaction shows each view's forms."""
    root = root.resolve()
    level = level_of(folder)
    report = section == "report"
    if level == "Block":
        return _views(BLOCK_VIEWS, lambda k: block_view(folder, root, k), report, folder, root)
    if level == "Job":
        return _views(JOB_VIEWS, lambda k: job_view(folder, root, k), report, folder, root)
    if level == "Task":
        _icon, _typ, steps = task_steps(folder)
        return _views([(_key(s), s) for s in steps], lambda k: _task_build(folder, root, k, steps), report, folder, root)
    return {}
