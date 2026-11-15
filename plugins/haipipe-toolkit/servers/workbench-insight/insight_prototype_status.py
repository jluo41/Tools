"""A Question Book's Status, what its page leads with, the steps done on it, its delivery tabs and its question
map (the hooks the shared page asks for)."""

from __future__ import annotations

from pathlib import Path

from live import insight_plan_c as P
from live import insight_views as V
from live.frame import esc, rel
from live.ui_parts import COPY_JS, _kv, copy_verb
from live.insight_view_parts import _pill, _side_tabs
from live.insight_prototype_facts import (
    ORDER, LEVEL, RUN_WORDS, _proto, _verdict, _newest_pass, _soft, _scripts, _done, q_state, q_word, _ready,
    r_word, _closed_r, tally_word, _release_of, _label, _proposals, _focus, KIND_WORD)


# ── Status ──────────────────────────────────────────────────────────────────────────────────────────────────────
def _row(words: str, sub: str, state: str, verbs: str = "") -> str:
    return (f'<div class=pb-todo><span class=w>{esc(words)}' + (f"<small>{esc(sub)}</small>" if sub else "") + "</span>"
            + _pill(state) + verbs + "</div>")


def _open_btn(href: str, label: str, words: str = "Open") -> str:
    return f'<a class=fd-btn data-pop="{esc(label)}" href="{esc(href)}" target=_blank rel=noopener>{esc(words)}</a>'


def _q_rows(qs: list, root: Path) -> str:
    rows = []
    for lv in ORDER:
        for q in (q for q in qs if q["id"][:1] == lv):
            short = str(q.get("question") or q.get("name") or "").strip()
            rows.append(_row(f'{q["id"]} · {short[:1].upper() + short[1:]}', LEVEL[lv], q_word(q),
                             _open_btn(_focus(Path(q["task"]), root), q["id"]) if q.get("task") else ""))
    return '<div class=pb-todos>' + "".join(rows) + '</div>'


def _release_runs(r: dict, root: Path) -> str:
    runs = _soft(r["job"]) if r.get("job") else {}
    rows = []
    for kind in ("review-questions", "set-segments", "sign-release"):
        run = runs.get(kind)
        if not run:
            continue
        verdict = _verdict(run)
        p = _newest_pass(run)
        rows.append(_row(RUN_WORDS[kind], run["run"], verdict or str(run.get("status") or "planned"),
                         V._open(p, root, run["run"], "its pass") if p else ""))
    return '<div class=pb-todos>' + "".join(rows) + '</div>' if rows else ""


def _release_waits(r: dict, proto: dict) -> str:
    """What a draft release waits on the person for: a proposal to triage, then its sign once every question is ready."""
    if r_word(r).startswith("closed"):
        return ""
    open_ = [p for p in _proposals(proto, r) if str(p.get("state") or "open").lower() in ("open", "proposed", "")]
    if open_:
        return f'🙋 {str(open_[0].get("title") or "").replace("-", " ")}: a proposed {KIND_WORD.get(str(open_[0].get("kind")), open_[0].get("kind") or "change")} waits for your yes or no'
    qs = list(r["questions"].values())
    if qs and all(_ready(q) for q in qs):
        return f"🙋 {_label(r)}: every question is ready; it waits for your sign"
    return ""


def _share(qs: list) -> int:
    return round(100 * sum(_ready(q) for q in qs) / len(qs)) if qs else 0


def status(folder: Path, root: Path, level: str) -> list:
    """A Question Book's Status bars: [(title, word, html, waits, share)]."""
    folder, root = Path(folder), Path(root).resolve()
    proto = _proto(folder, level)
    out = []
    if level == "Block":
        for r in reversed(proto["releases"]):
            qs = list(r["questions"].values())
            body = (_q_rows(qs, root)
                    + f'<div class=find-verbs>{_open_btn(_focus(r["job"], root), _label(r), "Open " + _label(r))}</div>')
            out.append((f"📜 {_label(r)}", tally_word(r), body, _release_waits(r, proto), _share(qs)))
    elif level == "Job":
        r = _release_of(proto, folder)
        if r:                                   # its questions are Findings' (round 2, settled: Status is the release's
            qs = list(r["questions"].values())  # state and sign); its files 📦 Delivery's
            out.append(("📜 The release", tally_word(r), _release_runs(r, root) or '<p class=mut>No Run on the release yet.</p>',
                        _release_waits(r, proto), _share(qs)))
    elif level == "Task":
        out += _task_status(folder, root, proto)
    return [(esc(x[0]),) + tuple(x[1:]) for x in out]          # a Status title is HTML (focus_page.numbered)


def _task_status(task: Path, root: Path, proto: dict) -> list:
    q = next((q for r in proto["releases"] for q in r["questions"].values() if Path(q["task"]) == task.resolve()), None)
    if q is None:
        fm = P.front(task / "question.md")
        if not fm:
            return []
        q = {"id": fm.get("id", ""), "task": task, "file": task / "question.md", "agreed": fm.get("agreed", ""),
             "needs": fm.get("needs") or {}, "question": fm.get("question", ""), "ask": fm.get("ask", ""),
             "method": fm.get("method") or {}, "asked": (fm.get("partitions") or {}).get("asked"), "level": fm.get("level")}
    m = q.get("method") or {}
    needs = "<br>".join(f'{esc(k)} · {esc(str(n.get("kind") or ""))}: {esc(str(n.get("what") or ""))}'
                        for k, n in (q.get("needs") or {}).items() if isinstance(n, dict))
    asked = q.get("asked")
    scripts = " ".join(V._open(s, root, s.name) for s in _scripts(q))
    body = _kv([("ask", esc(str(q.get("ask") or "—"))), ("level", esc(str(q.get("level") or LEVEL.get(q["id"][:1], "")))),
                ("method", esc(" · ".join(str(m.get(k)) for k in ("ask", "answer", "read") if m.get(k)) or "—")),
                ("asked on", esc(", ".join(asked) if isinstance(asked, list) else str(asked or "—"))),
                ("needs", needs or "—"), ("agreed", esc(str(q.get("agreed") or "⬜"))),
                ("script", scripts or esc(q_state(q)[1]))]) + f'<p class=by>{V._open(q["file"], root, "question.md")}</p>'
    out = [("❓ The question", q_word(q), body, "")]
    runs = sorted(_soft(task).items(), key=lambda kv: list(RUN_WORDS).index(kv[0]) if kv[0] in RUN_WORDS else 99)
    rows = []
    for kind, run in runs:
        p = _newest_pass(run)
        rows.append(_row(RUN_WORDS.get(kind, kind.replace("-", " ").capitalize()), run["run"],
                         _verdict(run) or str(run.get("status") or "planned"), V._open(p, root, run["run"], "its pass") if p else ""))
    if rows:
        done = sum(_done(r) for _, r in runs)
        out.append(("🧾 Its Runs", V.far(done, len(runs), "done"),
                    '<div class=pb-todos>' + "".join(rows) + '</div>', ""))
    return out


def delivery_tabs(folder: Path, root: Path, level: str) -> list:
    """What a Question Book hands over, in 📦 Delivery's tabs: each release, the files a Board Job pins (release.yaml,
    partitions.md, thresholds.yaml) with its state; a release page, its own (round 1, 261106: "the Models · Data ·
    Website lanes fit a work Block, not a signed release"). [(tab, word, panel)]."""
    folder, root = Path(folder), Path(root).resolve()
    proto = _proto(folder, level)
    rs = list(reversed(proto["releases"]))
    if level != "Block":
        rs = [r for r in rs if r.get("job") == folder or Path(r.get("job") or "").name == folder.name
              or (level == "Task" and Path(r.get("job") or "") == folder.parent)]
    return [(_label(r), r_word(r), _handed(r, root)) for r in rs]


FILE_WORDS = (("release.yaml", "its questions, each with its Task and what changed"),
              ("partitions.md", "its segments, fixed before any outcome"),
              ("thresholds.yaml", "its power floor and its thresholds"))


def _handed(r: dict, root: Path) -> str:
    """A release's handover: each file a Board Job pins, linked, with what it holds and the release's sign."""
    rows = [f'<li>{V._open(r["job"] / f, root, f)}<small>{esc(what)}</small></li>' for f, what in FILE_WORDS
            if r.get("job") and (r["job"] / f).is_file()]
    if not rows:
        return f'<p class=mut>{esc(_label(r))} is cut from the proposals; its files are written then.</p>'
    signed = str(r["face"].get("signed") or "")
    lead_ = ("A Board Job pins these files." if signed.startswith("✅") else
             "A Board Job pins these files once a person signs this version.")
    return (f'<p class=in-sub>{esc(lead_)}</p>'
            f'<ul class=wk-rows>{"".join(rows)}</ul>')


def _cap(text: str) -> str:
    return text[:1].upper() + text[1:] if text else ""


# ── what the page leads with, what is done on it, and its map (the shared page asks; round 2, 261108) ──────────────
def lead(folder: Path, root: Path, level: str, view: str) -> str:
    """The main line a view opens with (round 2: "Status and Findings each open with a main line"): on Status the
    release's state and sign, on Findings what its questions are; '' for any other view."""
    folder, root = Path(folder), Path(root).resolve()
    proto = _proto(folder, level)
    if not proto["releases"] or level not in ("Block", "Job"):
        return ""
    if level == "Job":
        r = _release_of(proto, folder)
        if r is None:
            return ""
        rs = [r]
    else:
        rs = list(reversed(proto["releases"]))
    if view == "standing":
        words = "; ".join(_status_line(r) for r in rs)
    elif view == "findings":
        r = rs[0]
        words = _findings_line(r)
        open_ = [p for p in _proposals(proto, r if level == "Job" else None) if _is_open(p)]
        if open_ and not _closed_r(r):
            words += f'; {len(open_)} idea{"" if len(open_) == 1 else "s"} wait{"s" if len(open_) == 1 else ""} for your yes or no'
    else:
        return ""
    return f'<p class=pb-big>{esc(_cap(words))}</p>'


def _status_line(r: dict) -> str:
    signed = str(r["face"].get("signed") or "")
    if _closed_r(r):
        return f"{_label(r)} {signed}" if signed.startswith("✅") else f"{_label(r)} ⬜"
    qs = list(r["questions"].values())
    return f"{_label(r)} {V.far(sum(_ready(q) for q in qs), len(qs), 'agreed and scripted')}"


def _findings_line(r: dict) -> str:
    qs = list(r["questions"].values())
    cuts = len(r.get("partitions") or [])
    ready = sum(_ready(q) for q in qs)
    on = f" on {cuts} segment{'' if cuts == 1 else 's'}" if cuts else ""
    if qs and ready == len(qs):
        return f"{len(qs)} questions{on}"
    left = [q["id"] for q in qs if not _ready(q)]
    return f"{len(qs)} questions{on}; still to finish: {', '.join(left)}"


def _is_open(p: dict) -> bool:
    return str(p.get("state") or "open").lower() in ("open", "proposed", "")


def _skill(text: str) -> str:
    return copy_verb("Copy prompt", text, "Copies a prompt for /haipipe-insight; paste it in a Claude session")


def _li(name: str, href: str, pop: str, note: str, verb: str = "") -> str:
    return (f'<li><a href="{esc(href)}" data-pop="{esc(pop)}">{esc(name)}</a><small>{esc(note)}</small>{verb}</li>'
            if href else f'<li><span>{esc(name)}</span><small>{esc(note)}</small>{verb}</li>')


def _next_step(q: dict) -> str:
    """A question's next step in words (round 2: "K02 · script to write", never "no state")."""
    agreed, script = q_state(q)
    if agreed == "returned":
        return "method returned: revise it"
    if agreed == "to agree":
        return "method to agree"
    return {"script written": "script to review"}.get(script, script)


def process(folder: Path, root: Path, level: str, view: str) -> list | None:
    """A Question Book's ⚙️ Process steps on one Work view, in place of the shared ones (round 2: "sign a release and triage
    a proposal on the Question Book too"); None leaves the shared steps. [(title, word, html, waits)].

      findings  📋 the question version: triage its open proposals, then sign it, each a Copy prompt for /haipipe-insight
      standing  🚧 Next steps: each question not yet agreed and scripted, by its name and its step; "nothing to do"
                when none (never a row per Task saying "no Run waiting")"""
    folder, root = Path(folder), Path(root).resolve()
    if level not in ("Block", "Job"):
        return None
    proto = _proto(folder, level)
    r = _release_of(proto, folder) if level == "Job" else (proto["releases"][-1] if proto["releases"] else None)
    if r is None:
        return None
    where = rel(r["job"], root) if r.get("job") else rel(folder, root)
    if view == "findings":
        rows, waits = [], ""
        if not _closed_r(r):
            open_ = [p for p in _proposals(proto, r) if _is_open(p)]
            names = ", ".join(str(p.get("title") or "").replace("-", " ") for p in open_)
            pdir = rel(Path(proto["path"]) / "proposals", root)
            rows.append(_li("Sort the open ideas", V.open_url(Path(proto["path"]) / "proposals", root) if open_ else "",
                            "proposals", ("waiting for you · " + names) if open_ else "done: none open",
                            _skill(f"/haipipe-insight {pdir} triage the open proposals ({names}) for {_label(r)}: take each "
                                   "in, merge it or decline it, and say why in its file.") if open_ else ""))
            if open_:
                p = open_[0]
                waits = f'🙋 {str(p.get("title") or "").replace("-", " ")}: a proposed {KIND_WORD.get(str(p.get("kind")), p.get("kind") or "change")} waits for your yes or no'
        qs = list(r["questions"].values())
        left = [q["id"] for q in qs if not _ready(q)]
        signed = str(r["face"].get("signed") or "")
        if _closed_r(r):
            sign = f"done: signed {signed}" if signed.startswith("✅") else "your sign"
        elif left:
            sign = "waits on " + ", ".join(left)
        else:
            sign = "waiting for you"
            waits = waits or f"🙋 {_label(r)}: every question is ready; it waits for your sign"
        rows.append(_li(f"Sign {_label(r)}", V.page_link(r["job"], root) if r.get("job") else "", _label(r), sign,
                        "" if _closed_r(r) else
                        _skill(f"/haipipe-insight {where} I sign {_label(r)}: check every question is agreed and its "
                               "script reviewed, then record my sign (run-sign-release); if one is not, say which.")))
        you = sum("waiting for you" in x for x in rows)
        word = (f"{you} wait{'s' if you == 1 else ''} for you" if you else "done" if _closed_r(r) else f"waits on {', '.join(left)}"
                if left else "done")
        return [("📋 " + _cap(_label(r)), word, f'<ul class=wk-rows>{"".join(rows)}</ul>' + COPY_JS, waits)]
    if view == "standing":
        todo = [q for q in r["questions"].values() if not _ready(q)] if not _closed_r(r) else []
        if not todo:
            return [("🚧 Next steps", "nothing to do", f'<p class=mut>Nothing to do: {esc(_status_line(r))}.</p>', "")]
        rows = []
        for q in sorted(todo, key=lambda q: (ORDER.find(q["id"][:1]), q["id"])):
            short = str(q.get("question") or q.get("name") or "").strip()
            rows.append(_li(f'{q["id"]} · {_cap(short)}', _focus(Path(q["task"]), root) if q.get("task") else "",
                            q["id"], _next_step(q)))
        word = _next_step(todo[0]) if len(todo) == 1 else "to do"
        return [("🚧 Next steps", word, f'<ul class=wk-rows>{"".join(rows)}</ul>', "")]
    return None


def map_branches(folder: Path, root: Path, level: str) -> list:
    """A release's MindMap (round 2: "group its question Tasks by DIKW level, each leaf the full question", as an
    insight Job's map does): [(level, [leaf words])]; [] for any other page (the shared map draws it)."""
    if level != "Job":
        return []
    r = _release_of(_proto(Path(folder), level), Path(folder))
    if r is None:
        return []
    out = []
    for lv in ORDER:
        qs = sorted((q for q in r["questions"].values() if q["id"][:1] == lv), key=lambda q: q["id"])
        if qs:
            out.append((LEVEL[lv], [f'[{q["id"]}] ' + _cap(str(q.get("question") or q.get("ask") or q.get("name") or "").strip())
                                    for q in qs]))
    return out



# ── the questions as a network, above a Code Board's MindMap ──────────────────
def map_top(folder: Path, root: Path, level: str) -> str:
    """The question canvas, dots mode, for the newest question version (a Block) or this one (a release): one column a
    DIKW level, a line from each answer to the questions that use it; '' for any other page."""
    from live import question_canvas as QC
    folder, root = Path(folder), Path(root).resolve()
    if level not in ("Block", "Job"):
        return ""
    proto = _proto(folder, level)
    rs = list(reversed(proto["releases"])) if level == "Block" else [x for x in [_release_of(proto, folder)] if x]
    rs = [r for r in rs if r["questions"]]
    if not rs:
        return ""
    href = lambda t: _focus(Path(t["path"]), root)
    if len(rs) == 1:                                     # a release: its own questions
        return (f'<p class=pb-big>How the questions of {esc(_label(rs[0]))} build on each other</p>'
                + QC.canvas(rs[0], None, href, root, mode="code"))
    # a Question Book: one side tab a question version, the newest first
    items = [(r["name"], str(r.get("words") or r.get("slug") or "")) for r in rs]
    return (_side_tabs("qcv", items, [QC.canvas(r, None, href, root, mode="code") for r in rs]))
