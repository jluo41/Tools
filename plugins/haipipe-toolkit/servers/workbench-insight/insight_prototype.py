"""A Prototype's own parts on the shared work page (b11 design loop round 1, 261106: "a Prototype is insight's"). A
Prototype Block (`board-kind: prototype`) holds the questions and their scripts, one Job per release; the shared page
asks insight_focus.prototype_parts for its Findings parts (before 📦 Delivery) and insight_focus.prototype_status for
its Status bars, both here:

  Findings  the questions in words with their scripts, a side tab per release (Block) or per DIKW level (a release);
            then the proposals and the cuts, a side tab each.
  Status    each release by release.yaml's state and its sign ("closed · signed ✅ 261106", "draft · not signed yet"),
            each question by question.md and its Runs ("agreed · script reviewed"); a question its Runs, each verdict.

[(title, word, html, waits)] each, a title plain words. Read-only: nothing here writes."""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote

from live import insight_plan_c as P
from live import insight_views as V
from live.frame import esc, pop, reader, rel
from live.ui_parts import COPY_JS, _kv, _pill, _side_tabs, copy_verb

ORDER = "DIKWX"                                   # the ladder, the Executive answers last
LEVEL = {"D": "Data", "I": "Information", "K": "Knowledge", "W": "Wisdom", "X": "Executive"}
RUN_WORDS = {"plan-evidence": "Plan the evidence", "review-plan": "Review the plan", "write-script": "Write the script",
             "review-script": "Review the script", "review-questions": "Review the questions", "set-cuts": "Set the cuts",
             "sign-release": "Sign the release", "ask": "Ask the question", "triage-proposals": "Triage the proposals"}
CSS = """<style>
.pq{list-style:none;margin:0;padding:0}.pq li{padding:8px 2px;border-bottom:1px solid var(--line);font-size:14px;line-height:1.45}
.pq li:last-child{border-bottom:0}.pq .h{display:flex;flex-wrap:wrap;align-items:baseline;gap:2px 10px}
.pq .h b{font-weight:600}.pq .h .pb-pill{margin-left:auto}.pq .ask{margin:3px 0 0}
.pq .by{margin:3px 0 0;font-size:12.5px;color:var(--muted)}.pq .by a{margin-right:10px}
.pr-files{display:flex;flex-wrap:wrap;gap:4px 14px;font-size:13.5px;margin:6px 0 0}
@media(max-width:600px){.pq .h .pb-pill{margin-left:0}}
</style>"""


# ── what is on disk ─────────────────────────────────────────────────────────────────────────────────────────────
def block_of(folder: Path, level: str) -> Path:
    return {"Block": folder, "Job": folder.parent, "Task": folder.parent.parent}.get(level, folder)


def _proto(folder: Path, level: str) -> dict:
    return P.prototype_at(block_of(Path(folder), level))


def _verdict(run: dict) -> str:
    """A soft Run's newest verdict, its pass's first heading (`# agreed`, `# returned`, `# release signed ✅ 261106`)."""
    passes = sorted((Path(run["path"]) / "passes").glob("*/pass.md")) if run.get("path") else []
    head = passes[-1].read_text(encoding="utf-8", errors="ignore").lstrip().split("\n", 1)[0] if passes else ""
    return head.lstrip("# ").strip()


def _newest_pass(run: dict) -> Path | None:
    passes = sorted((Path(run["path"]) / "passes").glob("*/pass.md")) if run.get("path") else []
    return passes[-1] if passes else None


def _soft(task: Path) -> dict:
    """{type: card} of a folder's soft Runs, by the type in their name (run-review-plan-d01 -> review-plan)."""
    out = {}
    for r in P.runs(task):
        if "_collect_" in r["run"]:                       # a 🙋 form is the page's Interaction, never a step of it
            continue
        m = re.match(r"^run-(.+?)-[a-z]?\d+$", r["run"]) or re.match(r"^run-(.+?)-[a-z0-9]+$", r["run"])
        out[str(r.get("type") or (m.group(1) if m else r["run"]))] = r
    return out


def _computes(q: dict) -> bool:
    return any(isinstance(n, dict) and n.get("kind") == "compute" for n in (q.get("needs") or {}).values())


def _scripts(q: dict) -> list:
    return sorted(p for p in (Path(q["task"]) / "scripts").glob("*.py")) if q.get("task") else []


def _done(run: dict | None) -> bool:
    return bool(run) and V._closed(run)


def q_state(q: dict) -> tuple:
    """(agreed word, script word) of a question, from question.md and its Runs: agreed · returned · to agree; script
    reviewed · script written · script to write; a question with no compute need cites the answers below it."""
    runs = _soft(Path(q["task"])) if q.get("task") else {}
    if str(q.get("agreed") or "").startswith("✅"):
        agreed = "agreed"
    elif _verdict(runs.get("review-plan", {})).startswith("returned"):
        agreed = "plan returned"
    else:
        agreed = "to agree"
    if not _computes(q):
        script = "cites the answers below"
    elif _done(runs.get("review-script")):
        script = "script reviewed"
    elif _done(runs.get("write-script")) or _scripts(q):
        script = "script written"
    else:
        script = "script to write"
    return agreed, script


def q_word(q: dict) -> str:
    return " · ".join(q_state(q))


def _ready(q: dict) -> bool:
    a, s = q_state(q)
    return a == "agreed" and s in ("script reviewed", "cites the answers below")


def r_word(r: dict) -> str:
    """A release's state and sign, as release.yaml's face holds them."""
    signed = str(r["face"].get("signed") or "")
    if str(r["face"].get("state")) == "closed" or signed.startswith("✅"):
        return "closed · " + (f"signed {signed}" if signed.startswith("✅") else "not signed")
    return "draft · not signed yet"


def _closed_r(r: dict) -> bool:
    return r_word(r).startswith("closed")


def tally_word(r: dict) -> str:
    """A Status bar's word with its tally (round 2: "draft · 8 of 9 agreed"): a closed release its sign; a draft how
    many of its questions are agreed and scripted."""
    if _closed_r(r):
        return r_word(r)
    qs = list(r["questions"].values())
    return f"draft · {sum(_ready(q) for q in qs)} of {len(qs)} agreed" if qs else "draft · no question yet"


def _release_of(proto: dict, folder: Path) -> dict | None:
    return next((x for x in proto["releases"] if x.get("job") == folder or Path(x.get("job") or "").name == folder.name), None)


def _label(r: dict) -> str:
    return r.get("label") or r["name"]


def _proposals(proto: dict, r: dict | None = None) -> list:
    """Every proposal (a Block), or a release's: those it took in, and the open ones while it is a draft."""
    ps = proto["proposals"]
    if r is None:
        return ps
    draft = not r_word(r).startswith("closed")
    return [p for p in ps if str(p.get("taken-in") or "") == r["name"]
            or (draft and str(p.get("state") or "open").lower() in ("open", "proposed", ""))]


def _p_word(p: dict) -> str:
    st = str(p.get("state") or "open").lower()
    taken = str(p.get("taken-in") or "")
    return f"taken in {P.plan_code(taken)}" if st == "taken" and taken else st


def _focus(path: Path, root: Path) -> str:
    return f"/_board/workbench?path={quote(rel(path, root))}&layout=focus"


# ── the parts ───────────────────────────────────────────────────────────────────────────────────────────────────
def _q_row(q: dict, root: Path, with_change: bool = False) -> str:
    """One question in words: its id and short question, its state; its ask; its script and its question file."""
    short = str(q.get("question") or q.get("name") or q["id"]).strip()
    ask = str(q.get("ask") or "").strip()
    links = [V._open(s, root, s.name) for s in _scripts(q)]
    links.append(pop(_focus(Path(q["task"]), root), q["id"], "its page ↗") if q.get("task") else "")
    change = str(q.get("change") or "")
    return (f'<li><div class=h><b>{esc(q["id"])}</b><span>{esc(short[:1].upper() + short[1:])}</span>{_pill(q_word(q))}</div>'
            + (f'<p class=ask>{esc(ask)}</p>' if ask and not ask.startswith("<") else "")
            + f'<p class=by>{"".join(x for x in links if x)}'
            + (f'<span>{esc(change)} in this plan</span>' if with_change and change else "") + '</p></li>')


def _by_level(qs: list, root: Path, with_change: bool = False) -> str:
    out = []
    for lv in ORDER:
        mine = [q for q in qs if q["id"][:1] == lv]
        if mine:
            out.append(f'<p class=pb-lv><b>{esc(LEVEL[lv])}</b></p><ul class=pq>'
                       + "".join(_q_row(q, root, with_change) for q in mine) + '</ul>')
    return "".join(out)


def _level_word(qs: list) -> str:
    ready = sum(_ready(q) for q in qs)
    if ready == len(qs):
        return "agreed · scripted" if any(_computes(q) for q in qs) else "agreed"
    return f"{sum(q_state(q)[0] == 'agreed' for q in qs)} of {len(qs)} agreed"


def _questions_by_release(proto: dict, root: Path) -> tuple:
    rs = list(reversed(proto["releases"]))                  # the newest release first, open
    if not rs:
        return None
    items = [(_label(r), r_word(r)) for r in rs]
    panels = [_by_level(list(r["questions"].values()), root, True) or "<p>This release asks no question yet.</p>" for r in rs]
    signed = sum(r_word(r).startswith("closed") for r in rs)
    word = " · ".join(w for w in (f"{signed} signed" if signed else "", f"{len(rs) - signed} draft" if len(rs) > signed else "") if w)
    return ("❓ Questions", word, CSS + _side_tabs("prq", items, panels), "")


def _questions_by_level(r: dict, root: Path) -> tuple | None:
    qs = list(r["questions"].values())
    lvs = [lv for lv in ORDER if any(q["id"][:1] == lv for q in qs)]
    if not lvs:
        return None
    items = [(LEVEL[lv], _level_word([q for q in qs if q["id"][:1] == lv])) for lv in lvs]
    panels = [_by_level([q for q in qs if q["id"][:1] == lv], root, True) for lv in lvs]
    return ("❓ Questions", _level_word(qs), CSS + _side_tabs("prl", items, panels), "")


def _proposals_part(ps: list, root: Path) -> tuple | None:
    if not ps:
        return None
    items, panels = [], []
    for p in ps:
        body = Path(p["file"]).read_text(encoding="utf-8", errors="ignore") if Path(p["file"]).is_file() else ""
        text = re.sub(r"(?s)^---\n.*?\n---\n", "", body).strip()
        why = " ".join(ln.strip() for ln in text.splitlines() if ln.strip() and not ln.startswith("#"))
        items.append((str(p.get("title") or "").replace("-", " ").capitalize(), _p_word(p)))
        panels.append(_kv([("kind", esc(str(p.get("kind") or "—"))), ("level", esc(str(p.get("level") or "—"))),
                           ("from", esc(str(p.get("from") or "—"))), ("state", esc(_p_word(p)))])
                      + (f'<p>{esc(why)}</p>' if why else "") + f'<p class=by>{V._open(p["file"], root, p["file"].name)}</p>')
    open_ = [p for p in ps if str(p.get("state") or "open").lower() in ("open", "proposed", "")]
    waits = (f'🙋 {str(open_[0].get("title") or "").replace("-", " ")}: a proposed {open_[0].get("kind") or "change"} '
             'waits for your triage') if open_ else ""
    word = f"{len(open_)} wait for you" if len(open_) > 1 else "1 waits for you" if open_ else "all triaged"
    return ("📮 Proposals", word, _side_tabs("prp", items, panels), waits)


def _cuts_part(r: dict, qs: list, root: Path) -> tuple | None:
    parts = r.get("partitions") or []
    if not parts:
        return None
    power = (r.get("thresholds") or {}).get("power") or {}
    floor = power.get("smallest_effect_pp")
    items, panels = [], []
    for p in parts:
        name = str(p.get("name") or "")
        asks = [q["id"] for q in qs if q.get("asked") == "all" or name in (q.get("asked") or [])
                or (name == "cross" and any(n.get("cut") == "cross" for n in (q.get("needs") or {}).values() if isinstance(n, dict)))]
        items.append((name, V._where(p)))
        panels.append(_kv([("where", f'<code>{esc(V._where(p))}</code>'), ("why", esc(str(p.get("why") or "—"))),
                           ("asked by", esc(", ".join(asks) or "—"))]))
    head = (f'<p>Fixed in {esc(_label(r))} before any outcome'       # its files are 📦 Delivery's (round 2: shown once)
            + (f'; a cut too thin to see a {esc(floor)}-point gap is refused for power' if floor else "") + '.</p>')
    return ("✂️ Cuts", f"power floor {floor} points" if floor else _label(r), head + _side_tabs("prc", items, panels), "")


def parts(folder: Path, root: Path, level: str) -> list:
    """A Prototype's Findings parts: [(title, word, html, waits)]."""
    folder, root = Path(folder), Path(root).resolve()
    proto = _proto(folder, level)
    out = []
    if level == "Block":
        out += [_questions_by_release(proto, root), _proposals_part(_proposals(proto), root)]
        if proto["releases"]:
            r = proto["releases"][-1]
            out.append(_cuts_part(r, list(r["questions"].values()), root))
    elif level == "Job":
        r = next((x for x in proto["releases"] if x.get("job") == folder or Path(x.get("job") or "").name == folder.name), None)
        if r:
            out += [_questions_by_level(r, root), _proposals_part(_proposals(proto, r), root),
                    _cuts_part(r, list(r["questions"].values()), root)]
    return [x for x in out if x]


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
    for kind in ("review-questions", "set-cuts", "sign-release"):
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
        return f'🙋 {str(open_[0].get("title") or "").replace("-", " ")}: a proposed {open_[0].get("kind") or "change"} waits for your triage'
    qs = list(r["questions"].values())
    if qs and all(_ready(q) for q in qs):
        return f"🙋 {_label(r)}: every question is ready; it waits for your sign"
    return ""


def _share(qs: list) -> int:
    return round(100 * sum(_ready(q) for q in qs) / len(qs)) if qs else 0


def status(folder: Path, root: Path, level: str) -> list:
    """A Prototype's Status bars: [(title, word, html, waits, share)]."""
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
        out.append(("🧾 Its Runs", "done" if done == len(runs) else f"{done} of {len(runs)} done",
                    '<div class=pb-todos>' + "".join(rows) + '</div>', ""))
    return out


def delivery_tabs(folder: Path, root: Path, level: str) -> list:
    """What a Prototype hands over, in 📦 Delivery's tabs: each release, the files a Board Job pins (release.yaml,
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
              ("partitions.md", "its cuts, fixed before any outcome"),
              ("thresholds.yaml", "its power floor and its thresholds"))


def _handed(r: dict, root: Path) -> str:
    """A release's handover: each file a Board Job pins, linked, with what it holds and the release's sign."""
    rows = [f'<li>{V._open(r["job"] / f, root, f)}<small>{esc(what)}</small></li>' for f, what in FILE_WORDS
            if r.get("job") and (r["job"] / f).is_file()]
    if not rows:
        return f'<p class=mut>{esc(_label(r))} is cut from the proposals; its files are written then.</p>'
    return (f'<p class=in-sub>{esc(_cap(r_word(r)))}: a Board Job pins these files.</p>'
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
            words += f'; {len(open_)} proposal{"" if len(open_) == 1 else "s"} wait{"s" if len(open_) == 1 else ""} for your triage'
    else:
        return ""
    return f'<p class=pb-big>{esc(_cap(words))}</p>'


def _status_line(r: dict) -> str:
    signed = str(r["face"].get("signed") or "")
    if _closed_r(r):
        return f"{_label(r)}: closed, signed {signed}" if signed.startswith("✅") else f"{_label(r)}: closed, not signed"
    qs = list(r["questions"].values())
    return f"{_label(r)}: a draft, {sum(_ready(q) for q in qs)} of {len(qs)} questions agreed and scripted, not signed yet"


def _findings_line(r: dict) -> str:
    qs = list(r["questions"].values())
    cuts = len(r.get("partitions") or [])
    ready = sum(_ready(q) for q in qs)
    on = f" on {cuts} cut{'' if cuts == 1 else 's'}" if cuts else ""
    if qs and ready == len(qs):
        return f"{len(qs)} questions agreed and scripted{on}"
    left = [q["id"] for q in qs if not _ready(q)]
    return f"{len(qs)} questions{on}: {ready} agreed and scripted, {', '.join(left)} still to finish"


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
    if agreed == "plan returned":
        return "plan returned: revise it"
    if agreed == "to agree":
        return "plan to agree"
    return {"script written": "script to review"}.get(script, script)


def process(folder: Path, root: Path, level: str, view: str) -> list | None:
    """A Prototype's ⚙️ Process steps on one Work view, in place of the shared ones (round 2: "sign a release and triage
    a proposal on the Prototype too"); None leaves the shared steps. [(title, word, html, waits)].

      findings  📋 the analysis plan: triage its open proposals, then sign it, each a Copy prompt for /haipipe-insight
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
            rows.append(_li("Triage the open proposals", V.open_url(Path(proto["path"]) / "proposals", root) if open_ else "",
                            "proposals", ("waiting for you · " + names) if open_ else "done: none open",
                            _skill(f"/haipipe-insight {pdir} triage the open proposals ({names}) for {_label(r)}: take each "
                                   "in, merge it or decline it, and say why in its file.") if open_ else ""))
            if open_:
                p = open_[0]
                waits = f'🙋 {str(p.get("title") or "").replace("-", " ")}: a proposed {p.get("kind") or "change"} waits for your triage'
        qs = list(r["questions"].values())
        left = [q["id"] for q in qs if not _ready(q)]
        signed = str(r["face"].get("signed") or "")
        if _closed_r(r):
            sign = f"done: signed {signed}" if signed.startswith("✅") else "closed, not signed"
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
        word = _next_step(todo[0]) if len(todo) == 1 else f"{len(todo)} to do"
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

