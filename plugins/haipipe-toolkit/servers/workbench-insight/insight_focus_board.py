"""A Board on the focus page: its Answers, Questions, Jobs, Data and Handoff views, as the Report shows them and as
the Work runs them."""

from __future__ import annotations

import re
from pathlib import Path

from live import insight_plan_c as P
from live import insight_views as V
from live.frame import esc, rel, table
from live.ui_parts import _kv, _numbered
from live.insight_view_parts import _pill, _section, _side_tabs
from live.insight_focus_job import _overall_state, QA_CSS
from live.insight_focus_parts import (
    _ctable, _step, _big, _focus, _proto_work, _jlink, _pair, _written, _page_word, _dot, JOB_KEY, _cap1, _page,
    _work_page, _map_view, _parts_map, _done, MOVED, _prompt, _copy_btn)


# ── a Board: Findings · Questions · Data · Advice · Jobs ─────────────────────────────────────────────────────────
# plain words, and a Job stays a Job on its button ("round" already names an experiment round in the content)
BOARD_VIEWS = (("answers", "Findings"), ("questions", "Questions"), ("data", "Data"), ("handoff", "Advice"), ("jobs", "Jobs"))


def is_board(folder: Path) -> bool:
    face = folder / "board.md"
    if not face.is_file():
        return False
    head = face.read_text(encoding="utf-8", errors="ignore")[:2000]
    return bool(re.search(r"(?m)^board-kind:\s*insight-board", head)) or (
        bool(re.search(r"(?m)^workbench:\s*insight", head)) and P.is_plan_c(folder))


def _href(b: dict, root: Path):
    """The old six-Space views' link maker, pointed at the focus page: href(sub, space, path)."""
    return lambda sub="", space="", path=None: _focus(Path(path) if path else b["path"], root)


def _preview(b: dict, j: dict) -> bool:
    """A Job whose question version is not signed yet: its sign waits on the person (🙋 and a Sign button, no words)."""
    plan = P.release(b["prototype"], j["release"])
    return not str(plan["face"].get("signed") or "").startswith("✅")


def _sign_btn(b: dict, j: dict, root: Path) -> str:
    """🙋 Sign, to where the question version is signed (the Question Book's Work); "" once it is signed."""
    if not _preview(b, j):
        return ""
    plan = P.release(b["prototype"], j["release"])
    name = esc(plan.get("label") or plan.get("name") or j["release"])
    return (f' <span class="word you mk" title="1 waits for you">🙋</span> <a class=fd-btn data-pop="{name}" '
            f'href="{esc(_proto_work(plan["job"], root))}">Sign</a>') if plan.get("job") else ' <span class="word you mk" title="1 waits for you">🙋</span>'


def _job_state(j: dict) -> str:
    """A Job's state in a word: closed, else open."""
    return "closed" if j["state"] == "closed" else "open"


def _map_word(b: dict) -> str:
    n = sum(j["state"] != "closed" for j in b["jobs"])
    return "open" if n else "all closed"


def _plans_grid(b: dict, root: Path) -> str:
    """The question versions × data versions (the Board's two clocks crossed; shown once, in Jobs, round 2): a row per plan
    (its questions, segments and sign), a column per data version, a Job in each cell: its state word, its pages as a dot
    row per DIKW level and how many are written. Stacks into cards under 600 px (round 2: "the grid scrolls sideways")."""
    versions = b["versions"]
    rels = b["prototype"]["releases"] or [{"name": n, "label": n, "questions": {}, "partitions": [], "face": {}}
                                          for n in sorted({j["release"] for j in b["jobs"]})]
    cell = {(j["release"], j["data"]): j for j in b["jobs"]}
    heads = ["question version"] + [V._vlabel(b, str(v.get("version", ""))) + (f' · locked {v["frozen"]}' if v.get("frozen") else "")
                                 for v in versions]
    rows = []
    for r in rels:
        signed = str(r["face"].get("signed") or "")
        row = [f'<b>{esc(r.get("label") or r["name"])}</b><br><span class=mut>{len(r["questions"])} questions · '
               f'{len(r.get("partitions") or [])} segments · {esc(signed if signed.startswith("✅") else "⬜")}</span>']
        for v in versions:
            j = cell.get((r["name"], v.get("version")))
            if not j:
                row.append('<span class=mut>no Job yet</span>')   # a new Job is Work's (Jobs › ➕ A new Job)
                continue
            wrote, asked = V.written_of(j["tasks"])
            row.append(f'{_jlink(j, root)} {_pill(_job_state(j))}{_sign_btn(b, j, root)}'
                       f'<br>{_strip(j)}<br><span class=mut>{V.far(wrote, asked, "written")}</span>')
        rows.append(row)
    return JOB_KEY + '<div class=in-plans>' + _ctable(heads, rows) + '</div>'


def _answers(b: dict, root: Path, work: bool = False) -> str:
    """Answers: the newest Job's X01 in one line as the view's headline, the newest
    Job's Overall Report as side tabs (each Executive answer once), then what each question found, a side tab per DIKW
    level. The question versions × data versions are Jobs' (shown once, round 2); each question's trail through the Jobs is Work's
    (`work`). Every "N of M" by the one count (insight_views.is_written)."""
    href = _href(b, root)
    if not b["jobs"]:
        return _section("🔎 Answers", "<p class=mut>No Job yet: add one in Work › Jobs.</p>", "no Job yet")
    newest = b["jobs"][-1]
    shown = next((j for j in reversed(b["jobs"]) if V._executive(j)), None)    # the newest Job with an Overall Report
    first = next((t for t in (V._executive(shown) if shown else []) if _written(t)), None)
    out = _big(str(first["face"]["answer"]) if first else "What this dataset says, Job by Job")
    if first and shown is not None:
        out += (f'<p class=in-sub>{_pill(_job_state(shown))} {_jlink(shown, root, _pair(shown))}'
                + _sign_btn(b, shown, root) + '</p>')
    if shown:
        xs = V._executive(shown)
        earlier = [j for j in b["jobs"] if V._executive(j) and j is not shown]
        lead = (f'<p class=in-sub>{_jlink(shown, root, shown["name"][:3])}\'s report'
                + (" · earlier: " + ", ".join(_jlink(j, root) for j in earlier) if earlier else "") + "</p>")
        written, asked = V.written_of(xs)
        out += _section("📄 Overall Report", lead + V._overall_tabs(shown, b, P.release(b["prototype"], shown["release"]),
                                                                      root, "bov"), V.far(written, asked, "written"))
    plan = P.release(b["prototype"], newest["release"])
    cut = next((V._part_key(x) for x in V._part_names(plan.get("partitions") or [])), "full") or "full"
    asked = V._questions(b)                              # each question by its newest Job's page (the one count)
    said = sum(bool(V.newest_task(b, q)) and _written(V.newest_task(b, q)) for q in asked)
    out += _section("🔎 Answers", V._coverage(b, root, cut, href, tabs="cov", work=work),
                    V.far(said, len(asked), "written"))
    return out


def _answering(b: dict, r: dict) -> dict | None:
    """The Job a plan's answers are read from: its newest Job; for a plan no Job runs yet (a draft), the newest Job,
    each Task of it replaced by the newest written answer of that question in any Job, so a kept question keeps its
    answer while the next plan is drafted."""
    job = next((j for j in reversed(b["jobs"]) if j["release"] == r["name"]), None)
    if job or not b["jobs"]:
        return job
    tasks = {}
    for j in b["jobs"]:                                  # each question's newest Job's page: the counts' one rule
        for t in j["tasks"]:
            tasks[t["qid"]] = t
    return dict(b["jobs"][-1], tasks=list(tasks.values()))


def _canvas(b: dict, root: Path, work: dict | None = None) -> str:
    """The question canvas Job by Job: one side tab a Job, the
    newest first, each its question version's questions on that Job's answers; before any Job, the newest question version
    (question_canvas.py). Report reads it, Work asks from it."""
    from live import question_canvas as QC
    rels = {r["name"]: r for r in b["prototype"]["releases"]}
    if not rels:
        return ""
    href = lambda t: _focus(t["path"], root)
    props = b["prototype"]["proposals"] if work is not None else ()
    def one(r, job):
        w = dict(work, job=job["name"] if job else "", proposals=rel(b["prototype"]["path"], root) + "/proposals/") \
            if work is not None else None
        return QC.canvas(r, job, href, root, w, props)
    jobs = [j for j in reversed(b["jobs"]) if j["release"] in rels]
    if not jobs:
        r = b["prototype"]["releases"][-1]
        return one(r, _answering(b, r))
    items = [(f'{j["name"].split("_", 1)[0]} · {j["release"]} × {j["data"]}', str(j.get("moved") or "")) for j in jobs]
    return _side_tabs("qcj", items, [one(rels[j["release"]], j) for j in jobs])


def _open_proposals(b: dict) -> list:
    return [p for p in b["prototype"]["proposals"] if str(p.get("state") or "open").lower() in ("open", "proposed", "")]


def _questions_view(b: dict, root: Path, work: dict | None = None) -> str:
    """Questions: the canvas (Report explores it; Work, by the same call, asks from a pinned question), every plan's
    questions as side tabs, then the Board's own questions; each question's answer is Answers' (round 1)."""
    href = _href(b, root)
    r = b["prototype"]["releases"][-1] if b["prototype"]["releases"] else {}
    signed = str((r.get("face") or {}).get("signed") or "")
    open_ = _open_proposals(b)                            # each question's answer is Answers' (shown once, round 1)
    out = _section("❓ Questions", V._prototype_tabs(b, root, "plans"),      # the list first, then the map
                   (f'{len(open_)} idea{"" if len(open_) == 1 else "s"} open') if open_ else "every idea sorted")
    out += _section("🕸 Question map", _canvas(b, root, work),
                    "✅" if signed.startswith("✅") else "⬜")
    if b["reports"]:                                      # the Board's own questions, only when there are some
        out += _section("🧭 Board questions", V._findings(b, root, "full", href, tabs="own"),
                        V.far(sum(str(x.get("answer-status") or "").lower() in V.WRITTEN for x in b["reports"]),
                              len(b["reports"]), "answered"))
    return out


def _strip(j: dict) -> str:
    """A Job's pages as a dot row per DIKW level: the level's
    letter, a dot a question, filled once its page is written."""
    out = []
    for lv, name, _ in V.LEVELS:
        ts = [t for t in j["tasks"] if t["qid"][:1] == lv]
        if ts:
            out.append(f'<b title="{esc(name)}">{lv}</b>' + "".join(
                _dot("on" if _written(t) else "half" if str(t["face"].get("answer-status") or "").lower() == "drafted" else "off",
                     f'{t["qid"]} · {_page_word(t)}') for t in ts))
    return f'<span class=strip>{"".join(out)}</span>'


def _job_tasks(j: dict, root: Path) -> tuple:
    """A Job's Tasks as dot rows by DIKW level, as Questions: closed, a level's dots and how many pages are written;
    open, a row per Task: its id, its question's words, its Runs, its page's state. (html, written, asked)."""
    rows, wrote, n = [], 0, 0
    for lv, name, _ in V.LEVELS:
        ts = [t for t in j["tasks"] if t["qid"][:1] == lv]
        if not ts:
            continue
        dots, items = [], []
        for t in ts:
            st = str(t["face"].get("answer-status") or "").lower()
            dots.append(f'<span class="dot {"on" if _written(t) else "half" if st == "drafted" else "off"}" '
                        f'title="{esc(t["qid"])} · {esc(_page_word(t))}"></span>')
            tally = {}
            for r in t["hard"]:
                tally[str(r.get("status") or "—")] = tally.get(str(r.get("status") or "—"), 0) + 1
            runs = (" ".join(dict.fromkeys(V.mark(s) for s in tally)) if t["hard"] else
                    "⬜" if lv in V.RUN_LEVELS else "cites the answers below it")
            words = t["name"].split("_", 2)[-1].replace("-", " ")
            items.append(f'<li><a class=id href="{esc(_focus(t["path"], root))}">{esc(t["qid"])}</a>'
                         f'<span class=q>{esc(words)}</span><span class=a>{esc(runs)} · page {esc(_page_word(t))}</span></li>')
        done = sum(_written(t) for t in ts)
        rows.append(f'<details{" open" if not rows else ""}><summary><span class=lv>{esc(name)}</span><span class=dots>{"".join(dots)}</span>'
                    f'<span class=tally>{V.far(done, len(ts), "written")}</span></summary><ol>{"".join(items)}</ol></details>')
        wrote, n = wrote + done, n + len(ts)
    return QA_CSS + f'<div class=qa>{"".join(rows)}</div>', wrote, n


def _jobs_view(b: dict, root: Path) -> str:
    """Jobs: each Job a row, its pins and its pages as a dot row per DIKW level; the newest Job's Tasks by level, as
    Questions; the one clock each Job moved."""
    if not b["jobs"]:
        return _section("🧷 Jobs", _plans_grid(b, root), "no Job yet")
    out = _section("🧷 Jobs", _plans_grid(b, root), _map_word(b))
    newest = b["jobs"][-1]
    html, wrote, n = _job_tasks(newest, root)
    out += _section(f"📂 Newest Job, {newest['name'][:3]}", html,
                    f"{V.far(wrote, n, 'written')} · {_job_state(newest)}")
    moved = [(j["name"][:3], esc(MOVED.get(j["moved"], j["moved"] or "—") + (f' · from {j["previous"][:3]}' if j["previous"] else "")))
             for j in b["jobs"]]
    last = b["jobs"][-1]
    return out + _section("⏱ Changes", _kv(moved),
                          f'{last["name"][:3]} moved {MOVED.get(last["moved"], last["moved"] or "—")}')


def _version_panel(b: dict, v: dict, root: Path) -> str:
    """One data version: its numbers as a card, what is new,
    its files each one click away, a few rows."""
    import zlib
    name = str(v.get("version", ""))
    folder = P.version_folder(v, root, b["path"])
    on = [j for j in b["jobs"] if j["data"] == v.get("version")]
    new = f'<p class=in-sub>{esc(_cap1(str(v.get("new"))))}</p>' if v.get("new") and not str(v["new"]).startswith("<") else ""
    if not folder or not folder.is_dir():                 # the card from board.md alone: never a dead end (round 1)
        nums = [(str(v.get("rows") or "—"), "rows"), (str(v.get("frozen") or "—"), "locked"),
                (", ".join(j["name"][:3] for j in on) or "—", "Jobs on it")]
        return new + '<div class=in-card>' + "".join(f'<div><b>{esc(a)}</b><span>{esc(k)}</span></div>' for a, k in nums) + '</div>'
    d = P.data_folder(folder, str(v.get("extract", "")))
    m = d["manifest"]
    span = " to ".join(str(x) for x in (m.get("start_date"), m.get("end_date")) if x)
    nums = [(f'{m["n_rows"]:,}' if m.get("n_rows") else str(v.get("rows") or "—"), "rows"),
            (str(m.get("n_cols") or "—"), "columns"), (span or "—", "dates"), (str(v.get("frozen") or "—"), "locked"),
            (", ".join(j["name"][:3] for j in on) or "—", "Jobs on it")]
    card = new + '<div class=in-card>' + "".join(f'<div><b>{esc(a)}</b><span>{esc(k)}</span></div>' for a, k in nums) + '</div>'
    files = [V._open(folder / f, root, f) for f in ("cohort_summary.txt", "data_dictionary.csv", "manifest.json")
             if (folder / f).is_file()]
    files += [V._open(f, root, f.name) for f in d["figures"] + d["docs"] + d["tables"]]
    if d["data"]:
        files.append(f'<span class=mut>{esc(d["data"].name)}</span>')
    s = P.sample_rows(d["data"], V.SAMPLE_N, zlib.crc32(name.encode()), tuple((m.get("groups") or {}).get("identity") or ())) \
        if d["data"] else {}
    sample = ""
    if s and s["rows"]:
        vals = dict(zip(s["columns"], zip(*s["rows"])))
        cols = [c for c in (v.get("preview") or []) if c in vals] or s["columns"][:V.SAMPLE_COLS]
        sample = (f'<p class=pb-lv><b>A few rows</b> <span title="drawn at random; identifying columns left out">'
                  f'{len(s["rows"])} of {s["total"]:,}</span></p><div class=wk-scroll>'
                  + table(tuple(cols), [tuple(esc(r[s["columns"].index(c)]) for c in cols) for r in s["rows"]]) + '</div>')
    fig = next((f for f in d["figures"] if f.suffix.lower() in (".png", ".svg", ".jpg")), None)   # shown, not only
    pic = (f'<figure class=in-fig><a href="/{esc(rel(fig, root))}" target=_blank rel=noopener data-pop="{esc(fig.name)}">'  # linked
           f'<img src="/{esc(rel(fig, root))}" alt="{esc(fig.stem)}" loading=lazy></a>'                             # (round 2)
           f'<figcaption>{esc(fig.stem.replace("_", " ").replace("-", " "))}</figcaption></figure>') if fig else ""
    return card + pic + f'<div class=in-files>{" ".join(files)}</div>' + sample


def _data_view(b: dict, root: Path) -> str:
    """Data: a side tab per data version, its new line and key numbers and files; then the segments, a side tab each."""
    vs = list(reversed(b["versions"]))
    freezes = _side_tabs("frz", [(V._vlabel(b, str(v.get("version", ""))), f'locked {v.get("frozen")}' if v.get("frozen") else "")
                                 for v in vs], [_version_panel(b, v, root) for v in vs]) if vs else ""
    # the segments the newest Job runs on (its question version), never a draft version no Job runs yet (or
    # "Fixed in v2" stands over rows counted by Jobs of v1); before any Job, the newest version's
    r = (P.release(b["prototype"], b["jobs"][-1]["release"]) if b["jobs"] else
         b["prototype"]["releases"][-1] if b["prototype"]["releases"] else {}) or {}
    floor = ((r.get("thresholds") or {}).get("power") or {}).get("smallest_effect_pp")
    return (_section("🗄 Data versions", freezes or "<p>Add a data version in Work.</p>", "all locked" if vs else "none yet")
            + _section("✂️ Segments", _cuts_tabs(b, r, root), f"smallest gap to detect: {floor} points" if floor else "fixed before any result"))


def _cuts_tabs(b: dict, r: dict, root: Path) -> str:
    """The question version's segments, a side tab each (round 1: no grey paragraph): where, why, the questions that ask
    it, its rows in each data version; its files one click away."""
    parts = r.get("partitions") or []
    if not parts:
        return "<p>The segments are set in the Question Book's question version.</p>"
    items, panels = [], []
    for p in parts:
        name = str(p.get("name") or "")
        n = {}
        for v in b["versions"]:
            for j in (j for j in b["jobs"] if j["data"] == v.get("version")):
                for t in j["tasks"]:
                    for h in t["hard"]:
                        if (h.get("partition") or "") == name and isinstance(h.get("n"), int) and h["n"] > 0:
                            n.setdefault(str(v.get("version")), h["n"])
        asks = [q for q, row in r["questions"].items() if row.get("asked") == "all" or name in (row.get("asked") or [])
                or row.get("asked") == name]
        rows = ", ".join(f'{V._vlabel(b, k).split(" · ")[0]}: {c:,}' if isinstance(c, int) else f"{k}: {c}" for k, c in n.items())
        items.append((name, V._where(p)))
        panels.append(_kv([("where", f'<code>{esc(V._where(p))}</code>'), ("why", esc(str(p.get("why") or "—"))),
                           ("asked by", esc(", ".join(asks) or "—")), ("rows", esc(rows or "—"))]))
    files = [V._open(r["job"] / f, root, f) for f in ("partitions.md", "thresholds.yaml") if r.get("job") and (r["job"] / f).is_file()]
    head = (f'<p class=in-sub>Set in {esc(r.get("label") or r.get("name") or "the question version")}, before any result is seen.</p>'
            + (f'<div class=in-files>{" ".join(files)}</div>' if files else ""))
    return head + _side_tabs("cut", items, panels)


def _draft_handoff(b: dict) -> dict | None:
    """The handoff drafted and not yet signed: it waits for a person's sign before Design may read it."""
    return next((h for h in b["handoffs"] if not str(h.get("signed") or "").startswith("✅")), None)


def _sign_handoff_row(b: dict, root: Path) -> tuple | None:
    h = _draft_handoff(b)
    return (f'Sign the advice {h.get("counsel") or h["file"].stem}', "Design reads only signed advice",
            "waiting for you", V._open(h["file"], root, h["file"].name, "Read the draft")) if h else None


def _handoff_view(b: dict, root: Path) -> str:
    """Advice (the key stays `handoff`; one word on the button and inside): what the Wisdom answers advise
    so far with the draft beside them, then what was signed. Two sections, never the same count twice (review)."""
    signed = [h for h in b["handoffs"] if str(h.get("signed") or "").startswith("✅")]
    draft = _draft_handoff(b)
    wait = f'{draft.get("counsel") or draft["file"].stem} waits for your sign' if draft else ""
    out = _big("Signed advice: " + ", ".join(str(h.get("counsel") or h["file"].stem) for h in signed) if signed else
               "The advice draft waits for your sign" if draft else "No advice yet", wait if signed else "")
    j = b["jobs"][-1] if b["jobs"] else None
    w = [t for t in (j["tasks"] if j else []) if t["qid"][:1] == "W"]
    answered = [t for t in w if _written(t)]
    if j:
        r = P.release(b["prototype"], j["release"])
        lines = "".join(f'<li><b>{_jlink(dict(t), root, t["qid"])}</b>{esc(str(t["face"].get("answer") or "its page is still to write"))}'
                        f'<span class=q>{esc(str((r["questions"].get(t["qid"]) or {}).get("question") or ""))} · '
                        f'{esc(V.page_word(t))}</span></li>' for t in w)
        body = (f'<ul class=in-wl>{lines}</ul>' if w else "<p class=mut>This question version asks no Wisdom question.</p>")
        body += _kv([("from", esc(f'{V._rlabel(b, j["release"])} × {V._vlabel(b, j["data"])}')),
                     ("draft", V._open(draft["file"], root, draft["file"].name) if draft else "not written")])
        out += _section("🧠 Advice so far", body, V.far(len(answered), len(w), "written") if w else "none asked")
    if b["handoffs"]:
        out += _section("📦 Signed", V._handoff(b, root), "✅" if signed else "⬜")
    return out


BOARD_PARTS = {"answers": _answers, "questions": _questions_view, "jobs": _jobs_view, "data": _data_view, "handoff": _handoff_view}


def board_report_views(block: Path, root: Path) -> dict:
    """{key: (name, build)}: an insight Board's Report in its five letters, numbered sections only; {} for any other
    folder. The Board's facts are insight_plan_c's; nothing here writes."""
    if not is_board(block):
        return {}
    root = root.resolve()
    views = {}
    for key, name in BOARD_VIEWS:
        def build(key=key):
            return _page(_numbered(BOARD_PARTS[key](P.board(block), root)))
        views[key] = (name, build)
    return views


# ── a Board's Work (b11 j01 s52): the Report's letters, ⚙️ Process then 📊 Results ──────────────────────────────────
def _board_x(block: Path, root: Path) -> dict:
    b = P.board(block)
    folder = rel(block, root)
    return {"b": b, "root": root, "folder": folder, "session": _session_of(block),
            "newest": b["jobs"][-1] if b["jobs"] else None}


def _session_of(folder: Path) -> str:
    face = folder / "board.md"
    if face.is_file():
        m = re.search(r"(?m)^session:\s*`?([\w.-]+)`?", face.read_text(encoding="utf-8", errors="ignore")[:4000])
        if m:
            return m.group(1)
    return folder.name


def _bw_answers(x: dict) -> str:
    j = x["newest"]
    if not j:
        return ""
    state = _overall_state(V._work_facts(j))
    verb = _copy_btn(V._card_prompt("Write the overall report", rel(j["path"], x["root"]), j["name"][:3], j["previous"][:3]),
                     x["session"]) if state == "ready" else ""
    return _step("✍️ The Overall Report", [(f'Write the Overall Report for {j["name"][:3]}', "in the Job, from the answers below it",
                                           state, verb)])


def _bw_questions(x: dict) -> str:
    """Your acts on the next plan (sign it, triage the proposals; both in the Question Book), then new questions."""
    b, root, j = x["b"], x["root"], x["newest"]
    proto = b["prototype"]
    rows = []
    if proto["releases"]:
        r = proto["releases"][-1]
        go = (f'<a class=fd-btn data-pop="{esc(r.get("label") or r["name"])}" href="{esc(_proto_work(r["job"], root))}">Sign in the Question Book</a>'
              if r.get("job") else "")
        signed = str(r["face"].get("signed") or "")
        rows.append((f'Sign {r.get("label") or r["name"]}', "in the Question Book",
                     _done(signed) if signed.startswith("✅") else "waiting for you", "" if signed.startswith("✅") else go))
    open_ = _open_proposals(b)
    if proto["proposals"]:
        pgo = (f'<a class=fd-btn data-pop="ideas" href="{esc(_proto_work(proto["path"], root))}">Open the ideas</a>'
               if open_ and proto["path"].exists() else "")
        rows.append(("Sort the open ideas", "into one batch for the next question version · in the Question Book",
                     "waiting for you" if open_ else "done", pgo))
    out = _step("📋 The next question version", rows) if rows else ""
    new = [("Propose questions", "the gaps and weak answers, as ideas for the next question version",
            "ready" if j else "waits on a Job", _copy_btn(_prompt("Block", "Propose questions", x["folder"]), x["session"]) if j else ""),
           ("Ask a Board question", "a question over the Jobs' answers (board.md ## Questions)", "ready",
            _copy_btn(_prompt("Block", "Ask a Block question", x["folder"]), x["session"]))]
    return out + _step("❓ New questions", new)


def _job_steps(x: dict) -> str:
    """Each Job, its steps (the theme drawing's Board Work › Jobs): a row per Job, each step's state, Open on a Job
    still open."""
    root = x["root"]
    word = lambda s: {"done": "done", "optional": "—", "next": "next", "sign": "your sign", "todo": "to do"}.get(s, s)
    rows = []
    for j in reversed(x["b"]["jobs"]):
        st = V._work_states(j, V._work_facts(j))
        rows.append((_jlink(j, root, f'{j["name"][:3]} · {P.plan_code(j["release"])} × {P.freeze_code(j["data"])}'),)
                    + tuple(esc(word(st[s])) for s in ("2 · Run", "3 · Write", "4 · Check", "6 · Close"))
                    + ("" if j["state"] == "closed" else
                       f'<a class=fd-btn href="{esc(_focus(j["path"], root, "work"))}">Open {esc(j["name"][:3])}</a>',))
    return table(("Job", "Runs", "pages", "checks", "close", ""), rows) if rows else ""


def _bw_jobs(x: dict) -> str:
    j = x["newest"]
    out = ""
    if j:
        st = V._work_states(j, V._work_facts(j))
        step = next((s for s in V.WORK_STEPS if st[s] in ("next", "sign")), "")
        word = (f'{j["name"][:3]} next: {step.split(" · ")[-1].lower()}' if step else "every Job closed"
                if all(o["state"] == "closed" for o in x["b"]["jobs"]) else "done")
        out += _section("🪜 Each Job, its steps", _job_steps(x), word)
    return out + _step("➕ A new Job", [("Add a Job", "a signed question version × a data version, one clock moved", "ready",
                                        _copy_btn(_prompt("Block", "Add a Job", x["folder"]), x["session"]))])


def _bw_data(x: dict) -> str:
    return _step("🗄 Data versions and segments", [
        ("Add a data version", "a new extract, locked, its rows counted per segment", "ready",
         _copy_btn(_prompt("Block", "Add a data version", x["folder"]), x["session"])),
        ("Propose a segment", "to the next question version: a segment is set before any result is seen", "ready",
         _copy_btn(_prompt("Block", "Propose a segment", x["folder"]), x["session"]))])


def _bw_handoff(x: dict) -> str:
    j = x["newest"]
    w = [t for t in (j["tasks"] if j else []) if t["qid"][:1] == "W"]
    done = [t for t in w if _written(t)]
    ready = bool(w) and len(done) == len(w)
    state = "ready" if ready else "waits on the Wisdom answers" if w else "no Wisdom question yet"
    sign = _sign_handoff_row(x["b"], x["root"])
    signed = any(str(h.get("signed") or "").startswith("✅") for h in x["b"]["handoffs"])
    return _step("🤝 Advice", [
        ("Write the advice", "from the latest Job's Wisdom answers", "done" if sign or signed else state,
         _copy_btn(_prompt("Block", "Write the counsel", x["folder"]), x["session"]) if ready and not (sign or signed) else ""),
        sign or ("Draft the advice", "for a person to sign; Design reads it by its pair",
                 "done" if signed else "waits on the advice", "")])


BOARD_PROC = {"answers": _bw_answers, "questions": _bw_questions, "jobs": _bw_jobs, "data": _bw_data, "handoff": _bw_handoff}


def board_work_views(block: Path, root: Path, items=(), item_html=None) -> dict:
    """{key: (name, build)}: an insight Board's Work in the Report's letters, ⚙️ Process then 📊 Results (the Report's
    view by the same function; Questions' canvas there in its asking mode), the MindMap last; {} for any other folder.
    `items` and `item_html` are no longer drawn here: the page's own 🙋 Interaction shows each view's forms (R2)."""
    if not is_board(block):
        return {}
    root = root.resolve()
    views = {}
    for key, name in BOARD_VIEWS:
        def build(key=key):
            x = _board_x(block, root)
            if key == "questions":
                res = _questions_view(x["b"], root, {"board": x["folder"],
                                                      "tail": f'Run this in the Claude session "{x["session"]}"; start it if it is not running.'})
            elif key == "answers":                      # the trail through the Jobs is Work's (round 2)
                res = _answers(x["b"], root, work=True)
            else:
                res = BOARD_PARTS[key](x["b"], root)
            return _work_page(BOARD_PROC[key](x), res)
        views["work-" + key] = (name, build)
    views["work-mindmap"] = _map_view(_parts_map(block, root))
    return views
