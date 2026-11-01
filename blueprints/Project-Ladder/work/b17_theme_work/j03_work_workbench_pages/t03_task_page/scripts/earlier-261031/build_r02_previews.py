"""r02's option previews (b17 · j03 · t03_task_page, s58 · Task UI: Work): one small page per option, drawn in the
workbench's own look (its focus.css, inlined), so JL sees each screen and not only its name (JL 261031, on b17 r01: "I
think you should show that what is the expected UI / html looks like"). The part an option changes carries
class="diff", which the form boxes in orange.

The sample is one example work Task, t01_train_model, holding every kind of Run a work Task holds: hard Runs named as
haipipe-task-for-fit's public example names them (r02_train_baseline, r03_train_resume), with a smoke Run and a
figures Run beside them; the work theme's own soft Runs (run-build-t01, run-check-t01); and one collection Run
(r05_collect_stopping_rule). Placeholders only: no result, figure or headline is real.

The form shows a preview at half size in a frame 600 pixels tall, so what differs sits in that height: no Aim line (no
option changes it), compact rows, and two places side by side when an option adds a view.

Writes runs/r02_collect_task_work_views/option-q<N>-<k>.html; question_collection.md links each one under its option.
Rerun after changing anything here, never edit the pages:

    python build_r02_previews.py
"""
from __future__ import annotations

import html
from pathlib import Path

TASK = Path(__file__).resolve().parents[1]                       # t03_task_page
RUN = TASK / "runs" / "r02_collect_task_work_views"
TOOLS = next(p for p in TASK.parents if (p / "plugins" / "haipipe-toolkit").is_dir())
FOCUS_CSS = TOOLS / "plugins/haipipe-toolkit/servers/workbench/focus-assets/focus.css"

NAME = "t01_train_model"
CRUMB = "example work Task · … / work / bNN_<topic> / j01_model_fit / t01_train_model"
RAIL = ["Report", "Work", "Studio", "Interactions", "Delivery", "Timeline", "Files"]
ROLES = ("trial", "make", "fix", "check", "describe", "figures", "evidence", "publish")   # haipipe-run's role order
CAPTION = "Every Run in runs/, one row each; what waits for you first."

# the example Task's runs/, one dict per Run folder (its card run.yaml, its receipt result/runtime.yaml, its passes/)
RUNS = [
    {"run": "r01_train_smoke", "kind": "hard", "role": "trial", "agent": "claude", "skill": "haipipe-task-for-fit",
     "line": "a short try of the worker before the full Run", "state": "done", "passes": [("p01", "10-28", "done")]},
    {"run": "r02_train_baseline", "kind": "hard", "role": "make", "agent": "claude", "skill": "haipipe-task-for-fit",
     "line": "train the baseline setting to its stopping rule", "state": "done", "figure": True,
     "passes": [("p01", "10-28", "failed"), ("p02", "10-29", "done")]},
    {"run": "r03_train_resume", "kind": "hard", "role": "make", "agent": "JL", "skill": "haipipe-task-for-fit",
     "line": "resume training from r02's checkpoint", "state": "ready", "passes": []},
    {"run": "r04_figures_training_curves", "kind": "hard", "role": "figures", "agent": "claude",
     "skill": "haipipe-task-for-fit", "line": "draw r02's training curves", "state": "failed",
     "passes": [("p01", "10-30", "failed")]},
    {"run": "r05_collect_stopping_rule", "kind": "collect", "role": "", "agent": "JL", "skill": "haipipe-interaction",
     "line": "Stopping rule", "state": "waiting", "passes": []},
    {"run": "run-build-t01", "kind": "soft", "role": "make", "agent": "claude", "skill": "haipipe-task",
     "line": "build the worker, its config and the tickets", "state": "done",
     "passes": [("p01", "10-28", "done"), ("p02", "10-29", "done")]},
    {"run": "run-check-t01", "kind": "soft", "role": "check", "agent": "claude", "skill": "haipipe-task",
     "line": "check the close line against each receipt", "state": "queued", "passes": []},
]
BY = {r["run"]: r for r in RUNS}
WORD = {"done": ("✅ done", "ok"), "ready": ("🙋 ready: you press Run", "you"), "failed": ("❗ failed", "bad"),
        "queued": ("⬜ queued", ""), "waiting": ("🙋 waits for you", "you")}
TODAY_WORD = {"done": "done", "ready": "planned", "failed": "failed", "queued": "queued", "waiting": "waiting"}

FIG = ('<svg viewBox="0 0 120 64" role="img" aria-label="figure.png, a placeholder">'
       '<rect x="0.5" y="0.5" width="119" height="63" rx="3" fill="#fff" stroke="#dee2e6"/>'
       '<polyline points="8,12 22,28 36,36 52,42 68,45 84,47 112,48" fill="none" stroke="#1864ab" stroke-width="2"/>'
       '<text x="60" y="60" font-size="7" text-anchor="middle" fill="#868e96">figure.png · placeholder</text></svg>')

PREVIEW_CSS = """
/* preview only: the page without its fixed rails; the right rail is drawn as one line under the path */
.focus-page.pv{max-width:900px;padding:14px 22px 26px}.pv h1{margin:4px 0 8px;font-size:23px}.pv .h1-section{font-size:19px}
.rail-line{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin:6px 0 0;font-size:12px}
.rail-line .rl-word{font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-right:2px}
.rail-line span.rl{padding:0 8px;border:1px solid var(--line);border-radius:5px;color:var(--muted)}
.rail-line span.rl.on{color:var(--accent);border-color:var(--accent);background:var(--soft)}
.pv .section-views{flex-wrap:wrap;gap:6px;margin:0 0 6px}
.pv .section-views span{font-size:13px;border:1px solid var(--line);border-radius:7px;padding:3px 11px;color:var(--ink);background:var(--paper)}
.pv .section-views span.on{color:var(--accent);border-color:var(--accent);background:var(--soft)}
.pv .section-views .vw{font-style:normal;margin-left:6px;font-size:11px;color:var(--muted)}
.pv .section-views .vw.you{color:light-dark(#b35c00,#e4bd62);font-weight:600}.pv .section-views .vw.ok{color:light-dark(#2b8a3e,#8ce99a)}
.pv .view-caption{margin:0 0 8px;font-size:12.5px;color:var(--muted)}
.sec{margin:0 0 10px}
.sec-h{font-size:12.5px;font-weight:700;margin:0 0 6px;padding:3px 10px;border:1px solid var(--line);border-radius:7px;background:var(--wash)}
.sec.wait>.sec-h{border-color:light-dark(#ffa94d,#b35c00);background:light-dark(#fff4e6,#3a2a12);color:light-dark(#b35c00,#ffc078)}
.role-h{font-size:10.5px;font-weight:600;letter-spacing:.05em;text-transform:uppercase;color:var(--muted);margin:6px 0 3px}
.rw{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:10px;align-items:center;border:1px solid var(--line);border-radius:9px;padding:5px 10px;margin:0 0 5px;background:var(--paper)}
.rw.wait{border-color:light-dark(#ffa94d,#b35c00)}
.rw-name{display:block;font-weight:700;font-size:13px;overflow-wrap:anywhere}
.rw-line{display:block;font-size:11.5px;color:var(--ink);opacity:.85}
.rw-meta{display:block;font-size:11px;color:var(--muted)}
.rw-who{display:block;font-size:11px;color:var(--muted)}
.rw-head{display:block;font-size:11px;color:var(--ink);background:var(--wash);border-radius:5px;padding:1px 6px;margin:2px 0}
.st{font-weight:600}.st.you{color:light-dark(#b35c00,#e4bd62)}.st.bad{color:light-dark(#c92a2a,#ff8787)}.st.ok{color:light-dark(#2b8a3e,#8ce99a)}
.rw-foot{display:flex;flex-wrap:wrap;align-items:center;gap:4px 10px;margin-top:2px}.rw-foot .rw-meta{display:inline}
.rw-verbs{display:flex;flex-wrap:wrap;gap:5px}
.vb{font-size:11px;border:1px solid var(--line);border-radius:7px;padding:0 8px;color:var(--ink);background:var(--paper)}
.vb.flag{border-color:light-dark(#ffa94d,#b35c00);color:light-dark(#b35c00,#ffc078)}
.vb.go{border-color:var(--accent);color:var(--accent)}.vb.ps{font-size:10.5px;padding:0 6px;color:var(--muted)}
.rw-pic{margin:0;width:112px}.rw-pic svg{display:block;width:112px;height:60px}
.rw-out{grid-column:1 / -1;margin:4px 0 0}.rw-out svg{display:block;width:100%;height:150px}
.rw-out figcaption{font-size:11px;color:var(--muted);margin-top:3px}
.run-group{border:1px solid var(--line);border-radius:9px;padding:4px 8px 2px;margin:0 0 5px}
.run-group>.rw-name{margin:0 0 3px}.run-group .rw{margin:0 0 3px 14px;padding:3px 9px}
.ask-box{border:1px dashed var(--line);border-radius:7px;padding:5px 10px;font-size:11.5px;color:var(--muted);margin:0 0 6px;background:var(--paper)}
.btns{display:flex;gap:6px;flex-wrap:wrap}.btn{font-size:11.5px;border:1px solid var(--accent);color:var(--accent);border-radius:7px;padding:1px 10px}
.gone{border:1px dashed var(--line);border-radius:9px;padding:9px 12px;font-size:12px;color:var(--muted);text-align:center}
.screens{display:grid;grid-template-columns:1fr;gap:12px;align-items:start}
.screen{border:1px solid var(--line);border-radius:10px;padding:8px 10px;background:var(--paper);min-width:0}
.screen-title{font-size:14px;font-weight:700;margin:0 0 5px}.screen-title span{font-weight:400;color:var(--muted);margin-left:6px;font-size:12.5px}
.screen .section-views span{font-size:11px;padding:1px 7px}.screen .view-caption{font-size:11px;margin:0 0 6px}
.file{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:8px;align-items:center;border:1px solid var(--line);border-radius:8px;padding:4px 9px;margin:0 0 5px}
.file code{font-size:11.5px}.file small{display:block;font-size:11px;color:var(--muted)}
"""


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def diff(on: bool) -> str:
    return " diff" if on else ""


def rail() -> str:
    spans = "".join(f'<span class="rl{" on" if n == "Work" else ""}">{esc(n)}</span>' for n in RAIL)
    return f'<div class="rail-line"><span class="rl-word">Right rail</span>{spans}</div>'


def views(names: list, on: str, mark: bool = False, words: dict | None = None) -> str:
    words = words or {}
    spans = "".join(f'<span class="{"on" if n == on else ""}">{esc(n)}'
                    + (f'<i class="vw {words[n][1]}">{esc(words[n][0])}</i>' if n in words else '') + '</span>'
                    for n in names)
    return f'<nav class="section-views{diff(mark)}" aria-label="Views">{spans}</nav>'


RUNS_BAR = views(["Runs"], "Runs")


def page(title: str, body: str, *, bar: str = RUNS_BAR, caption: str = CAPTION, heading: bool = True) -> str:
    """One preview page: the path and the right rail, then (heading) the title, its view buttons and the caption."""
    top = (f'<h1>{esc(NAME)}<span class="h1-section">Work</span></h1>{bar}'
           + (f'<p class="view-caption">{esc(caption)}</p>' if caption else "")) if heading else ""
    return ("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            f"<title>{esc(title)}</title><style>{FOCUS_CSS.read_text(encoding='utf-8')}{PREVIEW_CSS}</style></head>"
            f"<body><main class=\"focus-page pv\"><div class=\"focus-crumb\">{esc(CRUMB)}</div>{rail()}{top}{body}"
            "</main></body></html>")


def screen(section: str, inner: str, *, bar: str = "", caption: str = "", mark: bool = False) -> str:
    """One place of the page drawn small, so two can sit side by side."""
    cap = f'<p class="view-caption">{esc(caption)}</p>' if caption else ""
    return (f'<section class="screen{diff(mark)}"><div class="screen-title">{esc(NAME)}<span>{esc(section)}</span>'
            f'</div>{bar}{cap}{inner}</section>')


def sec(name: str, inner: str, *, wait: bool = False, mark: bool = False) -> str:
    """A view's section: its heading bar, its content below it (b32 s42-D09)."""
    return f'<section class="sec{" wait" if wait else ""}{diff(mark)}"><h3 class="sec-h">{esc(name)}</h3>{inner}</section>'


# ── one Run row ─────────────────────────────────────────────────────────────────────────────────────────────────
def verbs(r: dict, passes: str = "word") -> str:
    out = []
    if r["kind"] == "collect":
        out.append('<span class="vb flag">🙋 Interaction</span>' if r["state"] == "waiting"
                   else '<span class="vb">Interaction</span>')
    else:
        if r["state"] == "ready":
            out.append(f'<span class="vb go" title="bash …/runs/{esc(r["run"])}/{esc(r["run"])}.sh">Copy command</span>')
        out.append('<span class="vb">Open</span>')
        if r["kind"] == "hard" and r["state"] == "done":
            out.append('<span class="vb">Result</span>')
    if passes == "buttons":
        out += [f'<span class="vb ps diff">{esc(p)} · {esc(d)}</span>' for p, d, _ in r["passes"]]
    return f'<span class="rw-verbs">{"".join(out)}</span>'


def meta(r: dict, passes: str = "word", mark_pass: bool = False) -> str:
    word, cls = WORD[r["state"]]
    out = f'<b class="st {cls}">{esc(word)}</b>'
    if passes == "word" and r["passes"]:
        p, d, _ = r["passes"][-1]
        mark = ' class="diff"' if mark_pass else ""
        out += f' <span{mark}>· {esc(p)} · {esc(d)}</span>'
    return f'<span class="rw-meta">{out}</span>'


def row(r: dict, *, show: str = "line", passes: str = "word", pic: str = "small", mark: bool = False,
        mark_pass: bool = False, mark_pic: bool = False) -> str:
    """show: line (name, one line, state, newest pass, verbs) · who (that, then agent and skill) · bare (as today:
    name and state). pic: small (at the row's right) · big (full width under it, as today) · headline · none."""
    wait = r["state"] in ("ready", "waiting")
    cls = f'rw{" wait" if wait else ""}{diff(mark)}'
    if show == "bare":
        word = TODAY_WORD[r["state"]]
        badge = '<span class="vb">Interaction</span>' if r["kind"] == "collect" else ""
        return (f'<article class="{cls}"><div><span class="rw-name">{esc(r["run"])}</span>'
                f'<span class="rw-meta">{esc(word)} {badge}</span></div></article>')
    figure = r.get("figure") and pic in ("small", "big", "headline")
    head = (f'<span class="rw-head{diff(mark_pic)}">headline.txt · its numbers in one line (placeholder)</span>'
            if figure and pic == "headline" else "")
    who = f'<span class="rw-who">{esc(r["agent"])} · {esc(r["skill"])}</span>' if show == "who" else ""
    side = f'<figure class="rw-pic{diff(mark_pic)}">{FIG}</figure>' if figure and pic == "small" else ""
    under = (f'<figure class="rw-out{diff(mark_pic)}">{FIG}<figcaption>headline.txt · its numbers in one line '
             f'(placeholder)<br>Run {esc(r["run"])}</figcaption></figure>') if figure and pic == "big" else ""
    return (f'<article class="{cls}"><div><span class="rw-name">{esc(r["run"])}</span>'
            f'<span class="rw-line">{esc(r["line"])}</span>{head}{who}<span class="rw-foot">{meta(r, passes, mark_pass)}'
            f'{verbs(r, passes)}</span></div>{side}{under}</article>')


def pass_rows(r: dict, mark: bool = False) -> str:
    """One row per pass, under its Run's name (Q2 B)."""
    inner = "".join(f'<article class="rw"><div class="rw-foot"><span class="rw-meta"><b class="st {WORD[s][1]}">{esc(p)} · '
                    f'{esc(d)} · {esc(WORD[s][0])}</b></span><span class="rw-verbs"><span class="vb">Open</span></span></div>'
                    '</article>'
                    for p, d, s in r["passes"]) or \
        f'<article class="rw"><div><span class="rw-meta">{esc(WORD[r["state"]][0])} · no pass yet</span></div></article>'
    return (f'<div class="run-group{diff(mark)}"><span class="rw-name">{esc(r["run"])}</span>'
            f'<span class="rw-line">{esc(r["line"])}</span>{inner}</div>')


# ── the Runs view's sections ────────────────────────────────────────────────────────────────────────────────────
def lifted(r: dict, rule: str = "tickets") -> bool:
    """Waits for you: a form waiting for its answer; with rule tickets, a built ticket whose card names you; with
    rule failed, a failed Run too."""
    if r["kind"] == "collect" and r["state"] == "waiting":
        return True
    if rule in ("tickets", "failed") and r["state"] == "ready":
        return True
    return rule == "failed" and r["state"] == "failed"


def waits(rule: str = "tickets", mark: bool = False, **kw) -> str:
    return sec("Waits for you", "".join(row(r, **kw) for r in RUNS if lifted(r, rule)), wait=True, mark=mark)


def runs(rule: str = "tickets", names: list | None = None, marked: tuple = (), each=None, **kw) -> str:
    """The other Runs under their role's heading, in haipipe-run's order; forms not waiting go last."""
    rest = [r for r in RUNS if not lifted(r, rule) and (names is None or r["run"] in names)]
    groups = [(role, [r for r in rest if r["role"] == role]) for role in ROLES]
    groups.append(("forms", [r for r in rest if r["kind"] == "collect"]))
    draw = each or (lambda r: row(r, mark=r["run"] in marked, **kw))
    body = "".join(f'<h4 class="role-h">{esc(role)}</h4>' + "".join(draw(r) for r in rows) for role, rows in groups if rows)
    return sec("Runs", body)


def ask(mark: bool = False, prompts=("plan", "build", "check")) -> str:
    buttons = "".join(f'<span class="btn">Copy prompt: {esc(p)}</span>' for p in prompts)
    return sec("Ask the agent", f'<div class="ask-box">your notes, copied with the prompt</div><div class="btns">'
                                f'{buttons}</div>', mark=mark)


def code_view() -> str:
    files = [("scripts/train.py", "the worker every Run's ticket calls"),
             ("scripts/config/_defaults.yaml", "the settings every Run shares"),
             ("runs/<run>/config.yaml", "each Run's own settings: r01 to r04"),
             ("CODE_REVIEW.md", "the review before Run: pass · 10-29"),
             ("notebooks/", "none yet")]
    return "".join(f'<div class="file"><div><code>{esc(f)}</code><small>{esc(w)}</small></div><span class="vb">Open</span>'
                   '</div>' for f, w in files)


def build_step() -> str:
    files = [("scripts/train.py", "✅ the worker"), ("runs/<run>/config.yaml", "✅ r01 to r04"),
             ("runs/<run>/<run>.sh", "✅ the tickets, r01 to r04"), ("CODE_REVIEW.md", "✅ pass · 10-29")]
    made = "".join(f'<div class="file"><div><code>{esc(f)}</code><small>{esc(w)}</small></div></div>' for f, w in files)
    return (sec("The build", made) + ask(prompts=("build",))
            + sec("Runs of this step", row(BY["run-build-t01"])))


# ── the previews ────────────────────────────────────────────────────────────────────────────────────────────────
def previews() -> dict:
    out = {}
    full = waits() + runs() + ask()
    # Q1 · the view list: Runs alone; Runs and Code; the Task's steps
    out["q1-a"] = page("Q1 A", full, bar=views(["Runs"], "Runs", mark=True))
    # B and C add views: the page drawn as two of its screens side by side, each with its own view buttons
    out["q1-b"] = page("Q1 B", '<div class="screens">'
                       + screen("Work", waits() + runs(names=["r01_train_smoke", "r02_train_baseline"]),
                                bar=views(["Runs", "Code"], "Runs", mark=True), caption=CAPTION)
                       + screen("Work", code_view(), bar=views(["Runs", "Code"], "Code"), mark=True,
                                caption="This Task's code: the worker, its settings, its review.") + "</div>",
                       heading=False)
    steps = {"Plan": ("done", "ok"), "Build": ("done", "ok"), "Run": ("waits for you", "you"), "Check": ("not yet", "")}
    out["q1-c"] = page("Q1 C", '<div class="screens">'
                       + screen("Work", waits() + sec("Runs of this step", "".join(
                           row(BY[n]) for n in ("r01_train_smoke", "r02_train_baseline", "r04_figures_training_curves"))),
                           bar=views(list(steps), "Run", mark=True, words=steps),
                           caption="Run: the tickets you press, and what each did.")
                       + screen("Work", build_step(), bar=views(list(steps), "Build", words=steps), mark=True,
                                caption="Build: the worker, the settings, the tickets.") + "</div>",
                       heading=False)
    # Q2 · a row per Run, or one per pass (s58's open point)
    out["q2-a"] = page("Q2 A", runs(marked=(), mark_pass=True))
    out["q2-b"] = page("Q2 B", runs(each=lambda r: pass_rows(r, mark=True)))
    out["q2-c"] = page("Q2 C", runs(passes="buttons"))
    # Q3 · what one row shows (no figure here: Q5 asks that)
    three = ["r01_train_smoke", "r04_figures_training_curves", "run-build-t01", "run-check-t01"]
    out["q3-a"] = page("Q3 A", runs(names=three, marked=tuple(three)))
    out["q3-b"] = page("Q3 B", runs(names=three, marked=tuple(three), show="who"))
    out["q3-c"] = page("Q3 C", runs(names=three, marked=tuple(three), show="bare"))
    # Q4 · what moves up into Waits for you
    out["q4-a"] = page("Q4 A", waits(mark=True) + runs())
    out["q4-b"] = page("Q4 B", waits(rule="forms", mark=True) + runs(rule="forms", marked=("r03_train_resume",)))
    out["q4-c"] = page("Q4 C", waits(rule="failed", mark=True) + runs(rule="failed"))
    # Q5 · a done Run's result on its row
    two = ["r01_train_smoke", "r02_train_baseline", "run-build-t01"]
    out["q5-a"] = page("Q5 A", runs(names=two, pic="small", mark_pic=True))
    out["q5-b"] = page("Q5 B", runs(names=two, pic="big", mark_pic=True))
    out["q5-c"] = page("Q5 C", runs(names=two, pic="headline", mark_pic=True))
    # Q6 · where Ask the agent sits
    out["q6-a"] = page("Q6 A", waits() + runs() + ask(mark=True))
    out["q6-b"] = page("Q6 B", waits() + ask(mark=True) + runs())
    out["q6-c"] = page("Q6 C", waits() + runs() + '<div class="gone diff">No Ask the agent in Work: it sits in this '
                                                  "Task's Studio.</div>")
    return out


def main() -> None:
    made = previews()
    for name, text in made.items():
        (RUN / f"option-{name}.html").write_text(text, encoding="utf-8")
    print(f"wrote {len(made)} previews into {RUN.name}/")


if __name__ == "__main__":
    main()
