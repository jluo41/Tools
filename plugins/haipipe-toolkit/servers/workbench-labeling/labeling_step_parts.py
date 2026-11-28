"""The parts every 🧭 meaning or 🛠 expression step is drawn from: the engine it reads, the step table, its bars,
flows, tables, prompt and forms."""
from __future__ import annotations

import importlib.util
import traceback
import re
from pathlib import Path
from live import focus_page as F, frame, interaction_section as IX, labeling_theme as T
from live import ui_parts as UP
from live.ui_parts import PROMPT_CSS, PROMPT_JS, prompt_box, waits_on_you
SHOW = 12                                    # rows a case table shows; the rest are named in one line


def _engine(name: str):
    """hai-labeling's engine/<name>.py, found from this file; None when the skill is absent."""
    for base in Path(__file__).resolve().parents:
        path = base / "skills" / "3_theme" / "labeling" / "engine" / f"{name}.py"
        if path.is_file():
            spec = importlib.util.spec_from_file_location(f"labeling_{name}", path)
            mod = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(mod)
            except Exception:
                traceback.print_exc()
                return None
            return mod
    return None


MV = _engine("meaning_versions")
TWO = _engine("two_loops")                     # where a meaning or expression Task stands, shared with start.py

STEPS = {
    "meaning": (("frame", "Frame", "what we judge, agreed before any rule"),
                ("prepare", "Prepare", "the rules now, then the cases this loop's report asks about"),
                ("preferences", "Preferences", "this loop's interaction report: your answers"),
                ("update", "Update", "the rules your answers made, what changed, and where the loop goes")),
    "expression": (("rewrite", "Rewrite", "the wording, rewritten under a fixed meaning"),
                   ("run", "Run", "the models labeling Train and Test"),
                   ("evaluate", "Evaluate", "how the models did, and where the round report sends it"),
                   ("release", "Release", "whether the frozen version is ready")),
}
NEXT = {"frame": ("prepare", "🔍 Prepare"), "prepare": ("preferences", "🙋 Preferences"), "preferences": ("update", "🔁 Update"),
        "rewrite": ("run", "▶️ Run"), "run": ("evaluate", "📊 Evaluate"), "evaluate": ("release", "🔒 Release")}


def kind(folder) -> str:
    """meaning or expression, for a Task this page draws; "" for every other folder."""
    folder = Path(folder)
    if MV is None or TWO is None or frame.level_of(folder) != "Task":
        return ""
    types = T.types_of(folder)
    return types[0] if types in (("meaning",), ("expression",)) else ""


# ── small parts ──────────────────────────────────────────────────────────────────────────────────────────────────
def esc(x) -> str:
    return frame.esc(str(x))


def _session(task: Path) -> str:
    """The Claude session a step's prompt runs in: the Task face's `session:`, else its Job's, else the Task's name."""
    for face in (task / f"{task.name}.md", task.parent / f"{task.parent.name}.md"):
        if face.is_file():
            m = re.search(r"(?m)^session:\s*`?([\w.-]+)`?", face.read_text(encoding="utf-8", errors="ignore")[:4000])
            if m:
                return m.group(1)
    return task.name


def _flow(inn: tuple, who: tuple, out: tuple) -> str:
    """The step slide's flow: In → who works → Out, each a box with its lines (s58 views, the deck's pages 8 to 15)."""
    boxes = []
    for word, (head, *lines) in (("In", inn), ("Who works", who), ("Out", out)):
        boxes.append(f'<div class=ls-box><small>{word}</small><b>{esc(head)}</b>'
                     + "".join(f"<span>{esc(x)}</span>" for x in lines if x) + "</div>")
    return '<div class=ls-flow>' + '<span class=ls-arrow aria-hidden=true>→</span>'.join(boxes) + "</div>"


def _turns(label: str, turns: list) -> str:
    """The loop's iterations as a strip: [(name, word, now, href, pop)]; the one waiting on you orange, the current one
    in the workbench's blue (a built page keeps the workbench's colours; review D3 and C2 r01). A box with `href` opens
    it, in the pop-out when `pop` (round 2: each loop box opens that loop's record, each round box its report)."""
    def cell(n, w, now, href="", pop=False):
        tag, attr = ("a", f' href="{esc(href)}"' + (f' data-pop="{esc(n)}"' if pop else "")) if href else ("span", "")
        return (f'<{tag} class="ls-turn{" you" if waits_on_you(w) else " now" if now else ""}"{attr}><b>{esc(n)}</b>'
                f'<small>{esc(w)}</small></{tag}>')
    cells = '<span class=ls-arrow aria-hidden=true>→</span>'.join(cell(*t) for t in turns)
    return f'<div class=ls-turns><span class=ls-tl>{esc(label)}</span>{cells}</div>' if turns else ""


def _bar(words: str, verbs: str = "", mode: str = "you") -> str:
    """Your part, one line: the interaction that waits on you or your sign (orange); done, or waiting on a condition
    (grey)."""
    return f'<div class="ls-bar {mode}"><span>{esc(words)}</span>{verbs}</div>'


def _section(title: str, body: str, word: str = "", waits: str = "") -> str:
    """The bar every theme shares (ui_parts._section): its word becomes a mark (ui_parts.word_span: 🙋 when it waits on
    the person, ✓ when done, else nothing), and the line under the closed bar shows only while it waits on the person."""
    return UP._section(title, body, word, waits if waits_on_you(word) else "")


def bar_word(state: tuple, empty: str = "") -> str:
    """A step's state (its button's word, ok | you | run | "") as its bar's word, which the bar shows as a mark: what
    waits on you where the step waits on you ("sign m02" → "waits for your sign", a 🙋), "done" where it is done (a
    ✓), else nothing."""
    word, cls = state
    if word and cls == "you" and not waits_on_you(word) and "wait" not in word:
        return "waits for your sign" if "sign" in word else f"{word}, waits for you"
    if word and cls == "ok":
        return "done"
    return word if waits_on_you(word) else ""


def _step(title: str, body: str, state: tuple = ("", ""), waits: str = "", empty: str = "") -> str:
    """A step: one closed section holding all of it, its flow, your part (a sign, a date) and its prompt (round 4 of
    the b15 review: a prompt card sat open under every closed Process bar), with its state word on the right of its
    bar (review C1 and C2 r01) and, while the step waits on you, the one thing that waits under the closed bar
    (JL 261106), drawn by the bar every theme shares."""
    word = bar_word(state, empty)
    return _section(title, body, word, waits if waits_on_you(word) else "")


def _waiting_line(task: Path, root: Path, key: str, fallback: str = "") -> str:
    """The one line that waits under a step's closed bar: the first open question of this step's own forms, as its
    🙋 Interaction says it ("🙋 Loop 3 report: Q1 · Blind check"; round 4: an instruction line read as a chore list);
    `fallback` when no form of this step waits."""
    return IX.state_word(view_forms(task, root, key))[1] or fallback


def _received(saved: Path) -> str:
    """When the answers came back: the `received:` line the form's answer file carries (round 4: the page read the
    file's time, a day after the guideline made from it was approved), else the file's time."""
    if saved.is_file():
        m = re.search(r"(?m)^received:\s*(.+?)\s*$", saved.read_text(encoding="utf-8", errors="ignore")[:2000])
        if m:
            return m.group(1)
    return _when(saved)


def _rerun(task: Path, step: str, asks: str, template: str) -> str:
    """A step whose prompt reruns it alone (Run, Evaluate; s58-D15, Q7): the prompt as one row, its words copied by
    Copy prompt and shown on hover, so the step's results come first (review D3 r01)."""
    tail = f'Run this in the Claude session "{_session(task)}"; start it if it is not running.'
    head = " · ".join(x for x in ("✍️ Prompt", step, asks) if x)
    return (PROMPT_CSS + f'<div class="pb-prompt ls-rerun" title="{esc(template)}"><div class=pb-ph><span>{esc(head)}</span>'
            f'<button type=button class="fd-btn pb-copy" data-copy="{esc(template)}" data-tail="{esc(tail)}">Copy prompt</button>'
            "</div></div>" + PROMPT_JS)


def _rows(rows: list) -> str:
    """Rows like ui_parts._todo, each state with its own colour: [(words, sub, (state, ok | you | run | ""))]."""
    return '<div class=pb-todos>' + "".join(
        f'<div class=pb-todo><span class=w>{esc(w)}' + (f"<small>{esc(sub)}</small>" if sub else "") + "</span>"
        + (f'<span class="pb-pill {cls}">{esc(state)}</span>' if state else "") + "</div>"
        for w, sub, (state, cls) in rows) + "</div>"


def _link_tile(head: str, words: str, href: str, verb: str) -> str:
    """A tile whose verb opens where the work goes next (review C4 r01: a mark with no verb)."""
    go = f'<a class=fd-btn href="{esc(href)}">{esc(verb)}</a>' if href else ""
    return f'<div class=pb-tile><b>{esc(head)}</b><span>{esc(words)}</span>{go}</div>'


def _empty(words: str) -> str:
    return f'<p class=ls-empty>{esc(words)}</p>'


def _table(head: tuple, rows: list, more: str = "") -> str:
    """A small table; cells are HTML already escaped."""
    return ('<div class=ls-tw><table class=ls-table><thead><tr>' + "".join(f"<th>{esc(h)}</th>" for h in head)
            + "</tr></thead><tbody>" + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
            + "</tbody></table></div>" + (f'<p class=ls-foot>{more}</p>' if more else ""))


def _open(path: Path, root: Path, label: str = "Open") -> str:
    return (f'<a class=fd-btn data-pop="{esc(path.name)}" href="{esc(frame._file_url(path, root))}">{esc(label)}</a>'
            if path.is_file() and F.inside(path, root) else "")


def _view_url(task: Path, root: Path, key: str, section: str = "report") -> str:
    return F.page_url(task, root, section, key)


def _when(path: Path) -> str:
    import datetime
    return datetime.datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M") if path.exists() else ""


def _chain(steps: list) -> str:
    """A sequence as boxes with arrows, each with its role word above: [(role, words)]."""
    return ('<div class=ls-chain>' + '<span class=ls-arrow aria-hidden=true>→</span>'.join(
        f'<div class=ls-box><small>{esc(r)}</small><span>{esc(w)}</span></div>' for r, w in steps) + "</div>")


SESSION_LINE = re.compile(r"<p class=pb-sess>.*?</p>", re.S)


def quiet_prompt(box: str) -> str:
    """A prompt box without its grey "Run this in the Claude session …" line (round 2: read as an instruction under
    every prompt); Copy prompt still carries the session line (its data-tail)."""
    return SESSION_LINE.sub("", box)


def _prompt(task: Path, root: Path, key: str, step: str, asks: str, template: str, fields=None, cls: str = "",
            attrs: str = "") -> str:
    box = quiet_prompt(prompt_box(template, fields, _session(task), step=step, asks=asks,
                                  key=f"notes:{frame.rel(task, root)}#{key}",
                                  upload=(frame.rel(task, root), "/_board/labeling/notes")))
    return f'<div class="{cls}"{attrs}>{box}</div>' if cls else box


# the forms a step's own 🙋 Interaction shows, by the step its Run's name points to (settled 3: each view's own forms,
# the rail's Interactions all of them); a form that names no step goes to the step that asks the person
FORM_STEPS = {"meaning": (("_collect_frame", ("frame",)), ("_collect_report", ("prepare", "preferences"))),
              "expression": (("_collect_rewrite", ("rewrite",)), ("_collect_run", ("run",)),
                             ("_collect_evaluate", ("evaluate",)), ("_collect_release", ("release",)))}
FORM_HOME = {"meaning": "preferences", "expression": "release"}


def view_forms(task: Path, root: Path, key: str) -> list:
    """This step's own collection Runs (focus_page.interactions rows), waiting first."""
    k = kind(task)

    def homes(r) -> tuple:
        return next((keys for tag, keys in FORM_STEPS.get(k, ()) if tag in r["run"]), (FORM_HOME.get(k, ""),))
    return [r for r in F.interactions(task, root) if Path(r["page"]) == task and key in homes(r)]


def interaction(task: Path, root: Path, body: str, rows: list) -> str:
    """🙋 Interaction, the view's last section, numbered after its Results (interaction_section.view_section)."""
    return IX.view_section(rows, root, IX.next_number(body), lambda r: F.interaction_where(r, task, root))

