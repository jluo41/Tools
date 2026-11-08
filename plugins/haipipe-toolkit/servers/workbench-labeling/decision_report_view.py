"""The Decide view of a building labeling Task: this round's decision report, card by card (b15 j01 t03 s58, C2).

Drawn as the s03 slide deck draws it (version 12): the inbox of slide 17 (every card one full-width row, its question
large, its state in a pill, Open) and the decision card of slide 16 (the question, Case A beside Case B, the options
with none chosen, None of these, Defer, a comment, Save draft and Submit feedback; the interaction of s03's
decision-report prototype, template.html), in the workbench's own colours and the numbered shape of haipipe-ui:

    🔒 rules m02 · reference labels r02                    the report's base, a strip over the view
    ⚙️ Process   1 · 🙋 Decisions waiting for you          the report in one large sentence and its state word; a
                                                           row per card; "Continue later. Your draft stays saved.";
                                                           the open card (the first waiting one first) under them
    📊 Results   2 · 🪜 Earlier reports                     the other reports as a chain
    next: 🔁 Changes →

Report shows the Results only, read only: the same rows, each card with the answer of the newest submission that
settled it, then the chain (s57: "Report shows the cards only").

A card's pill says what the store's own status says (meaning_store.list_reports): from the newest submission of the
report's newest revision, Answered, More evidence requested (deferred) or Needs your judgment; with no submission, from
the newest saved draft, Draft saved or Needs your judgment. After a Save draft the page turns the pills itself.

It reads the decision store, the labeling engine's meaning_store.py (list_reports, load_report, load_draft,
list_submissions; s03 implementation-plan CONTRACTS.md v2, sections 5 and 6), loaded by path as labeling.py loads its
engine modules, and writes nothing. The form posts to POST /_board/labeling/act (decision_draft_save,
decision_feedback_submit), where the store checks every revision: a page that is out of date gets a 409, never a
silent overwrite. No option is ever chosen for the person: a radio is checked only by their click or their own saved
draft, which rides in the form's data-drafts for the browser to pick by the name it remembers.

Every piece of report text is escaped; no file system path reaches the HTML.
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

from live import frame

esc = frame.esc
ACT = "/_board/labeling/act"
STORE_NAME = "haipipe_subjective_label_meaning_store_for_focus"
SAFE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}")   # a report or actor id (meaning_contracts.IDENTIFIER_PATTERN)

WAITING, DRAFTED, DEFERRED, ANSWERED = "waiting for you", "drafted", "deferred", "answered"
ANSWER_KINDS = {"chosen", "reject_options", "rejected_options", "custom", "custom_proposal", "answered"}
DEFER_KINDS = {"defer", "deferred"}
# a card's state, as its pill says it (slide 17), and the pill's colour class
PILL = {WAITING: ("Needs your judgment", "wait"), DRAFTED: ("Draft saved", "draft"),
        DEFERRED: ("More evidence requested", "more"), ANSWERED: ("Answered", "ok")}
QUIET = "Continue later. Your draft stays saved."

TITLE_1, TITLE_2 = "🙋 Decisions waiting for you", "🪜 Earlier reports"
PROCESS, RESULTS = "⚙️ Process", "📊 Results"


# ── the store ──────────────────────────────────────────────────────────────────────────────────────────────────
_LOADED: dict = {}


def store():
    """The engine's decision store (skills/2_theme/labeling/engine/meaning_store.py), loaded by path as labeling.py
    loads calibration.py; None when it is missing or does not load. Loaded again when the file changes, so a store
    that arrives after the server started is found without a restart."""
    try:
        from host_paths import skill_dir
        path = skill_dir("labeling") / "engine" / "meaning_store.py"
        stamp = (str(path), path.stat().st_mtime_ns)
    except (ImportError, OSError):
        return None
    if _LOADED.get("stamp") == stamp:
        return _LOADED["module"]
    try:
        spec = importlib.util.spec_from_file_location(STORE_NAME, path)
        if spec is None or spec.loader is None:
            return None
        module = importlib.util.module_from_spec(spec)
        sys.modules[STORE_NAME] = module               # a dataclass in it looks its module up by name
        spec.loader.exec_module(module)
    except Exception:                                  # a broken store shows as unavailable, never a broken page
        sys.modules.pop(STORE_NAME, None)
        return None
    _LOADED.update(stamp=stamp, module=module)
    return module


def lane(task: Path) -> Path:
    """The Task's labeling lane, J (CONTRACTS section 1: `<Page>/labeling/`), as the write route resolves it."""
    return Path(task) / "labeling"


def _num(value) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _natural(text) -> list:
    return [(0, int(t), "") if t.isdigit() else (1, 0, t) for t in re.split(r"(\d+)", str(text)) if t]


def reports(mod, J: Path) -> list:
    """The published reports in the store's order, round then report (the newest last): one row per report id."""
    best = {}
    for row in mod.list_reports(J) or []:
        if not isinstance(row, dict) or not row.get("report_id"):
            continue
        rid = str(row["report_id"])
        if rid not in best or _num(row.get("report_revision")) >= _num(best[rid].get("report_revision")):
            best[rid] = row
    return sorted(best.values(), key=lambda r: (_natural(r.get("round_id") or ""), _natural(r["report_id"])))


def waits(row: dict) -> bool:
    """A report waits for the person while it is open or drafted, or while any of its cards still waits (a partial
    submission leaves the rest open)."""
    return str(row.get("status") or "") in ("open", "draft") or counts(row)[0] > 0


def state_word(row: dict) -> str:
    status = str(row.get("status") or "")
    return WAITING if status in ("open", "draft") else status or "published"


def counts(row: dict) -> tuple:
    c = row.get("counts") if isinstance(row.get("counts"), dict) else {}
    return _num(c.get("waiting")), _num(c.get("deferred")), _num(c.get("answered"))


def sentence(row: dict) -> str:
    """The view's main point (C2): `report-03: 1 card waits for you, 1 deferred`."""
    waiting, deferred, answered = counts(row)
    parts = []
    if waiting:
        parts.append(f"{waiting} card waits for you" if waiting == 1 else f"{waiting} cards wait for you")
    elif answered:
        parts.append(f"{answered} answered")
    if deferred:
        parts.append(f"{deferred} deferred")
    return f"{row['report_id']}: " + (", ".join(parts) or "no card waits for you")


def waiting_report(task: Path) -> bool:
    """True when the newest published report waits for the person (the building page then opens on Decide)."""
    mod = store()
    if mod is None or not lane(task).is_dir():
        return False
    try:
        rows = reports(mod, lane(task))
    except Exception:
        return False
    return bool(rows) and waits(rows[-1])


# ── what each card's answer is ─────────────────────────────────────────────────────────────────────────────────
def _keyed(value) -> dict:
    """{decision_id: entry} from a dict keyed by decision id, or a list of rows that name theirs."""
    if isinstance(value, dict):
        return {str(k): v for k, v in value.items()}
    if isinstance(value, list):
        return {str(r["decision_id"]): r for r in value if isinstance(r, dict) and r.get("decision_id")}
    return {}


def _word(value) -> str:
    """A disposition or an answer's kind, as one lower-case word."""
    if isinstance(value, dict):
        value = value.get("disposition") or value.get("kind") or value.get("status")
    return str(value or "").strip().lower()


def card_states(cards: list, subs: list, saved: dict, revision: int) -> tuple:
    """(each card's state, each card's submitted answer or None), as the store counts them (list_reports): the newest
    submission of this revision decides; with none, the newest saved draft of it (a drafted card says Draft saved);
    else every card waits. A submission or a draft of an older revision is never mapped onto this one."""
    mine = [s for s in subs or [] if isinstance(s, dict) and _num(s.get("report_revision")) == revision]
    if mine:
        sub = max(enumerate(mine), key=lambda p: (str(p[1].get("submitted_at") or ""), p[0]))[1]
        disp, ans = _keyed(sub.get("dispositions")), _keyed(sub.get("answers"))
        states, answers = [], []
        for c in cards:
            did = str(c.get("decision_id"))
            word = _word(disp.get(did)) or _word(ans.get(did))
            state = ANSWERED if word in ANSWER_KINDS else DEFERRED if word in DEFER_KINDS else WAITING
            states.append(state)
            answers.append(ans.get(did) if state != WAITING and isinstance(ans.get(did), dict) else None)
        return states, answers
    current = [d for d in saved.values() if d.get("report_revision") == revision]
    newest = max(current, key=lambda d: d.get("last_saved_at") or "", default=None)
    drafted = {did for did, a in (newest or {}).get("answers", {}).items() if a.get("kind") not in (None, "", "unanswered")}
    return [DRAFTED if str(c.get("decision_id")) in drafted else WAITING for c in cards], [None] * len(cards)


def answer_words(card: dict, answer: dict | None) -> str:
    """A submitted answer in words: the label of the option the person saw (the submission's own copy of the card,
    else this card's), the person's own rule, none of these, or deferred."""
    if not answer:
        return PILL[WAITING][0]
    kind = _word(answer)
    if kind == "chosen":
        oid = str(answer.get("option_id") or "")
        seen = (answer.get("card") or {}).get("options") if isinstance(answer.get("card"), dict) else None
        label = next((o.get("label") for o in (seen or card.get("options") or [])
                      if isinstance(o, dict) and str(o.get("option_id")) == oid), None)
        return "Chose: " + str(label or f"option {oid}")
    if kind in ("custom", "custom_proposal"):
        return "Own rule: " + str(answer.get("text") or "")
    if kind in ("reject_options", "rejected_options"):
        return "None of these options"
    if kind in DEFER_KINDS:
        return "Deferred: show more evidence"
    return PILL[ANSWERED][0]


# ── drafts, for the form to restore ────────────────────────────────────────────────────────────────────────────
def _clean_answers(value) -> dict:
    out = {}
    for did, a in _keyed(value).items():
        if isinstance(a, dict):
            out[did] = {k: str(a[k]) for k in ("kind", "option_id", "text", "comment") if a.get(k) not in (None, "")}
    return out


def drafts(mod, J: Path, report_id: str) -> dict:
    """{actor: the draft they saved} for one report: its draft and report revisions and its answers. The store's own
    list_drafts when it has one; else each `meaning/drafts/<report-id>/<actor-id>.json` (CONTRACTS section 1), read
    through load_draft."""
    found = []
    if hasattr(mod, "list_drafts"):
        try:
            found = [d for d in mod.list_drafts(J, report_id) or [] if isinstance(d, dict)]
        except Exception:
            found = []
    elif SAFE_ID.fullmatch(report_id):
        folder = J / "meaning" / "drafts" / report_id
        for f in sorted(folder.glob("*.json")) if folder.is_dir() else []:
            if not SAFE_ID.fullmatch(f.stem):
                continue
            try:
                d = mod.load_draft(J, report_id, f.stem)
            except Exception:
                continue
            if isinstance(d, dict):
                found.append({"actor_id": f.stem, **d})
    out = {}
    for d in found:
        actor = str(d.get("actor_id") or d.get("actor") or "")
        if actor:
            out[actor] = {"draft_revision": _num(d.get("draft_revision")), "report_revision": _num(d.get("report_revision")),
                          "answers": _clean_answers(d.get("answers")), "last_saved_at": str(d.get("last_saved_at") or "")}
    return out


# ── the shape every building view shares (haipipe-ui Salience: numbered heading bars that fold) ───────────────
def group(name: str) -> str:
    return f'<h3 class="dec-group">{esc(name)}</h3>'


def section(n, title: str, body: str, anchor: str = "", word: str = "", waits: str = "") -> str:
    """One section: a boxed heading bar `N · <emoji> name` that folds, open by default, its content under it; its state
    word on the bar's right and, while it waits on the person, that one thing under the bar, shown only while the
    section is closed (JL 261106: "every closed bar shows a state word on its right"). The fold keys on the title."""
    from live.ui_parts import word_span
    head = (f"{n} · " if n else "") + title
    return (f'<details class="dec-sec" open data-fold="{esc(head)}"' + (f' id="{esc(anchor)}"' if anchor else '')
            + f'><summary class="dec-h">{esc(head)}{word_span(word)}</summary><div class="dec-body">{body}</div></details>'
            + (f'<p class="dec-wait">{esc(waits)}</p>' if waits else ""))


def big(words: str, state: str = "") -> str:
    """The main point, large, and its state word under it."""
    cls = {WAITING: "wait", "submitted": "ok"}.get(state, "")
    return f'<p class="dec-big">{esc(words)}</p>' + (f'<p class="dec-state {cls}">{esc(state)}</p>' if state else "")


def line(words: str, cls: str = "dec-line") -> str:
    return f'<p class="{cls}">{esc(words)}</p>'


def next_link(href: str, words: str) -> str:
    return f'<p class="dec-next"><a href="{esc(href)}">next: {esc(words)} →</a></p>'


def wrap(body: str) -> str:
    return f'<div class="dec-view">{body}</div>'


# ── the Decide view ────────────────────────────────────────────────────────────────────────────────────────────
def _question(card: dict) -> str:
    return str(card.get("question") or card.get("short_title") or card.get("decision_id") or "")


def _pill(state: str, i: int) -> str:
    word, cls = PILL[state]
    return f'<span class="dec-pill {cls}" data-pill="{i}" data-state="{cls}">{esc(word)}</span>'


def _inbox(cards: list, states: list, open_i: int) -> str:
    """Slide 17: every card one full-width row, its full question large, its state in a pill, and Open, which shows
    that card under the rows (one at a time)."""
    return ('<div class="dec-inbox">' + "".join(
        f'<div class="dec-row{" on" if i == open_i else ""}" data-row="{i}"><p class="dec-rq">{esc(_question(c))}</p>'
        f'{_pill(s, i)}<button type="button" class="dec-btn main" data-open="{i}" aria-controls="dec-card-{i}" '
        f'aria-expanded="{"true" if i == open_i else "false"}" aria-label="Open: {esc(_short(_question(c)))}">Open</button></div>'
        for i, (c, s) in enumerate(zip(cards, states))) + "</div>")


def _short(text, limit=80) -> str:
    text = re.sub(r"\s+", " ", str(text or "")).strip()
    return text if len(text) <= limit else text[:limit - 1].rsplit(" ", 1)[0] + " …"


def _case(role: str, items: list) -> str:
    """Case A or Case B: each excerpt with its context before it and its signal under it. A Test case carries no
    text in a report (meaning_contracts: cited by reference only), and says so."""
    split = next((str(e.get("split")) for e in items if e.get("split")), "")
    body = "".join(
        (f'<p class="dec-ctx">{esc(e.get("context"))}</p>' if e.get("context") else "")
        + (f'<p class="dec-text">{esc(e.get("text"))}</p>' if str(e.get("text") or "").strip()
           else '<p class="dec-ctx">Its text is not shown here: a Test case is cited by reference only.</p>')
        + (f'<p class="dec-signal">{esc(e.get("signal"))}</p>' if e.get("signal") else "") for e in items)
    return (f'<figure class="dec-case"><figcaption>{esc(role)}' + (f'<small>{esc(split.capitalize())}</small>' if split else "")
            + f'</figcaption>{body}</figure>')


def _cases(card: dict) -> str:
    evidence = [e for e in card.get("evidence") or [] if isinstance(e, dict)]
    a = [e for e in evidence if e.get("role") == "case_a"]
    b = [e for e in evidence if e.get("role") == "case_b"]
    rest = [e for e in evidence if e.get("role") not in ("case_a", "case_b")]
    out = ('<div class="dec-cases">' + (_case("Case A", a) if a else "") + (_case("Case B", b) if b else "") + "</div>"
           if a or b else "")
    return out + (f'<div class="dec-cases one">{_case("Context", rest)}</div>' if rest else "")


def _choices(card: dict, i: int) -> str:
    """Slide 16's answers: each option a line, its letter and label, its effect shown once chosen; None of these (a
    box for the person's own rule); Defer; then a comment. None is chosen for the person. What each sends: chosen,
    custom (own rule written), reject_options (None of these, no rule written), defer, or unanswered."""
    name = f"dec-answer-{i}"
    opts = []
    for k, o in enumerate(o for o in card.get("options") or [] if isinstance(o, dict)):
        effect = " · ".join(str(o[f]) for f in ("effect", "scope") if o.get(f))
        opts.append(f'<label class="dec-choice"><input type="radio" name="{name}" value="chosen" autocomplete="off" '
                    f'data-option="{esc(o.get("option_id"))}"><span class="dec-letter">{chr(65 + k) if k < 26 else "·"}</span>'
                    f'<span><b>{esc(o.get("label") or o.get("option_id"))}</b>'
                    + (f'<small class="dec-effect" data-effect hidden>{esc(effect)}</small>' if effect else "") + "</span></label>")
    if card.get("none_allowed", True):
        opts.append(f'<label class="dec-choice alt"><input type="radio" name="{name}" value="none" autocomplete="off">'
                    '<span><b>None of these: write my own rule</b></span></label>'
                    '<textarea class="dec-own" data-own hidden autocomplete="off" aria-label="Your own rule" '
                    'placeholder="Your rule. Left empty, it rejects these options without one."></textarea>')
    if card.get("defer_allowed", True):
        opts.append(f'<label class="dec-choice alt"><input type="radio" name="{name}" value="defer" autocomplete="off">'
                    '<span><b>Defer: show more evidence</b></span></label>')
    out = (f'<fieldset class="dec-options"><legend class="dec-hidden">Your answer</legend>{"".join(opts)}</fieldset>'
           if opts else "")
    if card.get("comments_allowed", True):
        out += ('<label class="dec-field"><span>Comment</span><textarea data-comment autocomplete="off" '
                'placeholder="What matters to you here? What would change your answer?"></textarea></label>')
    return out


def _foot(card: dict) -> str:
    """The rest, small, at the card's foot: the rule today and what an answer here applies to."""
    parts = [("Current rule", card.get("current_rule")),
             ("Applies to", str(card.get("approval_scope") or "").replace("_", " "))]
    shown = [f"<span><b>{esc(k)}</b> {esc(v)}</span>" for k, v in parts if v]
    return f'<p class="dec-foot">{"".join(shown)}</p>' if shown else ""


def _card(card: dict, i: int, open_i: int, state: str, body: str) -> str:
    """Slide 16's decision card: its number and kind with its pill, its question large, why now, Case A beside Case B,
    then `body` (the answers in Work, the submitted answer in Report), then its foot."""
    kind = str(card.get("question_type") or "").replace("_", " ")
    return (f'<section class="dec-card" id="dec-card-{i}" aria-labelledby="dec-q-{i}" data-decision="{esc(card.get("decision_id"))}"'
            + ("" if i == open_i else " hidden")
            + f'><p class="dec-chead"><span>Decision {i + 1:02d}' + (f" · {esc(kind)}" if kind else "") + f"</span>{_pill(state, i)}</p>"
            + f'<h4 class="dec-cq" id="dec-q-{i}">{esc(_question(card))}</h4>'
            + (f'<p class="dec-why">{esc(card["why_now"])}</p>' if card.get("why_now") else "")
            + _cases(card) + body + _foot(card) + "</section>")


def _chain(rows: list) -> str:
    """The earlier reports, oldest first, each its words in a box and its state over it."""
    if not rows:
        return line("None: this is the first report.")
    steps = []
    for k, row in enumerate(rows):
        waiting, deferred, answered = counts(row)
        submitted = str(row.get("status")) == "submitted"
        parts = ([f"{answered} decided"] if answered else []) + ([f"{deferred} deferred"] if deferred else []) \
            + ([f"{waiting} waiting"] if waiting and not submitted else [])
        role = "done" if submitted else state_word(row)
        steps.append(('<span class="dec-arrow" aria-hidden="true">→</span>' if k else "")
                     + f'<div class="dec-step"><span class="dec-role">{esc(role)}</span><div class="dec-box">'
                     f'{esc(row["report_id"])} · {esc(", ".join(parts) or "nothing decided")}</div></div>')
    return '<div class="dec-chain">' + "".join(steps) + "</div>"


def _strip(base: dict) -> str:
    """The report's base, one quiet strip over the view: the rules and the reference labels it was written against."""
    return (f'<p class="dec-strip">🔒 rules {esc(base.get("meaning_version") or "not recorded")} · reference labels '
            f'{esc(base.get("reference_version") or "not recorded")}</p>')


def _answer_html(card: dict, answer: dict | None, state: str) -> str:
    """Report's answer line: the submitted answer in words and its comment, else the card's state."""
    if not answer:
        return f'<dl class="dec-kv dec-answer"><dt>Answer</dt><dd>{esc(PILL[state][0])}</dd></dl>'
    comment = answer.get("comment")
    return (f'<dl class="dec-kv dec-answer"><dt>Answer</dt><dd>{esc(answer_words(card, answer))}'
            + (f'<br><small class="dec-comment">Comment: {esc(comment)}</small>' if comment else "") + "</dd></dl>")


def _unavailable(read_only: bool, words: str, state: str, more: str = "") -> str:
    return group(RESULTS if read_only else PROCESS) + section(1, TITLE_1, big(words, state) + (line(more) if more else ""),
                                                              word="nothing yet" if state.startswith("nothing") else state)


def decide_view(task: Path, root: Path, read_only: bool = False) -> str:
    """Work › Decide (read_only False) or Report › Decide (True), for one building Task, without the next link."""
    task, root = Path(task).resolve(), Path(root).resolve()
    mod = store()
    if mod is None:
        return wrap(_unavailable(read_only, "The decision store is not available", "unavailable",
                                 "This view reads the labeling engine's decision store, which this server cannot load."))
    J = lane(task)
    try:
        rows = reports(mod, J) if J.is_dir() else []
    except Exception as exc:
        return wrap(_unavailable(read_only, "The decision reports could not be read", "unavailable",
                                 f"The decision store refused this Task's lane ({type(exc).__name__})."))
    if not rows:
        return wrap(_unavailable(read_only, "No decision report yet", "nothing waits for you",
                                 "A report shows here once one is published in this Task's labeling lane."))
    newest, earlier = rows[-1], rows[:-1]
    rid = str(newest["report_id"])
    try:
        report = mod.load_report(J, rid, revision=newest.get("report_revision"))
        subs = mod.list_submissions(J, rid) or []
    except Exception as exc:
        return wrap(_unavailable(read_only, f"{rid} could not be read", "unavailable",
                                 f"The decision store refused this report ({type(exc).__name__})."))
    if not isinstance(report, dict):
        return wrap(_unavailable(read_only, f"{rid} could not be read", "unavailable"))
    revision = _num(report.get("report_revision") or newest.get("report_revision"))
    base = report.get("base") if isinstance(report.get("base"), dict) else {}
    cards = [c for c in report.get("cards") or [] if isinstance(c, dict)]
    saved = drafts(mod, J, rid)
    states, answers = card_states(cards, subs, saved, revision)
    open_i = next((i for want in (WAITING, DRAFTED) for i, s in enumerate(states) if s == want), 0)
    head = big(sentence(newest), state_word(newest))
    chain = section(2, TITLE_2, _chain(earlier), word=f"{len(earlier)} earlier" if earlier else "none yet")
    first = next((c for c, s in zip(cards, states) if s == WAITING), None)
    word, waits = state_word(newest), (f"🙋 {_question(first)}" if first is not None else "")

    if read_only:                                 # Report: each card with its answer, nothing to fill in
        panels = "".join(_card(c, i, open_i, s, _answer_html(c, a, s))
                         for i, (c, s, a) in enumerate(zip(cards, states, answers)))
        inbox = (_inbox(cards, states, open_i) + f'<div class="dec-cardbox">{panels}</div>') if cards \
            else line("This report has no cards.")
        return wrap(_strip(base) + group(RESULTS) + section(1, TITLE_1, head + inbox, word=word, waits=waits) + chain)

    submitted = any(_num(s.get("report_revision")) == revision for s in subs if isinstance(s, dict))
    panels = "".join(_card(c, i, open_i, s, _choices(c, i)) for i, (c, s) in enumerate(zip(cards, states)))
    form = (f'<div class="dec-form" data-dec-form data-act="{esc(ACT)}" data-path="{esc(frame.rel(task, root))}" '
            f'data-report="{esc(rid)}" data-revision="{revision}" data-submitted="{int(submitted)}" '
            f'data-drafts="{esc(json.dumps(saved))}">'
            + _inbox(cards, states, open_i) + line(QUIET, "dec-quiet")
            + f'<div class="dec-cardbox">{panels}'
            '<div class="dec-actions">'
            '<label class="dec-field dec-name"><span>Your name</span><input type="text" data-human maxlength="64" '
            'autocomplete="off" spellcheck="false"></label>'
            '<label class="dec-confirm"><input type="checkbox" data-confirm autocomplete="off"> I confirm these are my answers</label>'
            '<div class="dec-buttons"><button type="button" class="dec-btn save" data-save>Save draft</button>'
            '<button type="button" class="dec-btn primary" data-submit disabled>Submit feedback</button></div>'
            '<p class="dec-status" role="status" aria-live="polite" data-status></p></div></div></div>') if cards \
        else line("This report has no cards.")
    return wrap(_strip(base) + group(PROCESS) + section(1, TITLE_1, head + form, anchor="dec-cards", word=word, waits=waits)
                + group(RESULTS) + chain)
