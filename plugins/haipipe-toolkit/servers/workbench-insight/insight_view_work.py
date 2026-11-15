"""A Job's Work: its six steps (Launch, Run, Write, Check, Compare, Close), each a work panel over its result,
and the results they sit on (the segment table, the current answers, this Job against the previous one)."""

from __future__ import annotations

from pathlib import Path

from live import insight_plan_c as P
from live.frame import esc, pop, rel, table
from live.insight_view_overall import _spec, _q_logic, _q_work, _q_report
from live.insight_view_parts import (
    LEVELS, STATUS, _kind, run_cards, _card_kind, _rows, _st, _fold, _chip, run_url, _run_link, _open,
    _qwr_head, _qwr, _by_level, _release_links, _label, LEVEL_WORD, MARK, _rlabel, _vlabel, _runs_table, _band,
    RUN_LEVELS, _rtype, _closed, is_written, _task_link, far, mark)


def _cut_table(j: dict) -> str:
    """Each segment's n, power and the questions it refused, from the Job's hard Runs' cards."""
    cuts = {}
    for t in j["tasks"]:
        for run in t["hard"]:
            c = cuts.setdefault(run.get("partition"), {"n": run.get("n", "—"), "power": set(), "refused": []})
            c["power"].add(str(run.get("power", "—")))
            if run.get("status") == "refused":
                c["refused"].append(t["qid"])
    rows = [(f'<b>{esc(p)}</b>', "<span class=mut>— (a test across the segments)</span>" if p == "cross" else esc(c["n"]),
             esc(" · ".join(sorted(c["power"]))),
             f'<span class=st-warn>{esc(", ".join(c["refused"]))}</span>' if c["refused"] else "<span class=mut>—</span>")
            for p, c in cuts.items()]
    return table(("partition", "n", "power", "refused"), rows)


def _job_current(j: dict, b: dict, r: dict, root: Path, part: str) -> str:
    rows = {}
    for t in j["tasks"]:
        if t["qid"][:1] == "X":                              # the Executive answers: the Overall Report's
            continue
        q = r["questions"].get(t["qid"], {})
        run = next((x for x in t["hard"] if x.get("partition") == part), None)
        f = t["face"]
        cites = t["qid"][:1] == "W" and not t["hard"]        # Wisdom reads the answers below
        if cites:
            trail = ['cites the answers below; no run of its own']
        elif run:
            trail = [f'<code>{esc(j["name"])}</code> › <code>{esc(t["name"])}</code> ▸ '
                     f'{_run_link(run, root)} · {_st(run.get("status"))}']
        else:
            trail = ["not asked on this segment"]
        mark = MARK.get(str((run or {}).get("status")), "·") if run else ("retired" if _spec(q).get("retired") else "·")
        page = (f'<p class=mut>{_task_link(t, root)}'
                + (f' · CHECK {esc(f["check"])}' if f.get("check") else "") + "</p>"
                if t.get("page") and f.get("answer") and "answer" not in (run or {}) else "")
        if cites:
            report = (f'<p><span class=chip>Report</span> {_st(f.get("answer-status") or "open")}</p>'
                      f'<p>{esc(f.get("answer") or "the counsel is written on its page, signed by a person")}</p>{page}')
        else:
            report = _q_report(_spec(q).get("name") or t["qid"], run, root, _label(part), page)
        rows.setdefault(t["qid"][:1], []).append(_qwr(_q_logic(t["qid"], q, mark, root), _q_work(q, trail), report,
                                                      f'question-{t["qid"]}'))
    work_head = "Task Work · the difference test" if part == "cross" else f"Task Work · its run on {_label(part)}"
    n = next((x.get("n") for t in j["tasks"] for x in t["hard"] if x.get("partition") == part and x.get("status") == "ok"), None)
    size = "compares the segments" if part == "cross" else (f"{n:,} rows" if isinstance(n, int) else "")
    head = f'<h3>{esc(_label(part))}{(" · " + esc(size)) if size else ""}</h3>'
    return head + _by_level(rows, _qwr_head(work_head, "Report · what it found"), links=_release_links(r.get("job"), root, r.get("label", "")))


def _vs_previous(j: dict, root: Path, tabs: str = "") -> str:
    """Each answer against the Job before, as its run-compare wrote it. With `tabs` (the focus page): a side tab per
    DIKW level, its word what changed there, each row's status a plain word."""
    vs = j["vs"]
    if not vs:
        return (f'<p class=mut>No comparison yet: run-compare-{esc(j["previous"][:3]) or "&lt;prev&gt;"} writes '
                'reports/vs-&lt;prev&gt;.md after every check.</p>' if j["previous"] else
                '<p class=mut>The first Job: nothing before it to compare with.</p>')
    tally = {s: 0 for s in STATUS}
    for row in vs["rows"].values():
        tally[row["status"]] = tally.get(row["status"], 0) + 1
    summary = " · ".join(s for s, n in tally.items() if n)
    chips = " ".join(_chip(s) for s in STATUS if tally.get(s))
    rows, moved = {}, {}
    full = _full_answers(j) if tabs else {}
    for qid, row in vs["rows"].items():
        status = f'<b>{esc(row["status"])}</b>' if tabs else _st(row["status"])
        if str(row["status"]).lower() != "held":
            moved.setdefault(qid[:1], []).append(row["status"])
        if tabs:                                    # each answer whole, from the two Jobs' pages (round 1: never "…")
            before, now = full.get(qid, ("", ""))
            rows.setdefault(qid[:1], []).append(
                f'<div class=vs-q><p class=vs-h><b>{esc(qid)}</b> {status}</p><dl class=vs-ab>'
                f'<dt>{esc(j["previous"][:3])}</dt><dd>{esc(before or row["previous"])}</dd>'
                f'<dt>{esc(j["name"][:3])}</dt><dd>{esc(now or row["this"])}</dd><dt>why</dt><dd>{esc(row["why"])}</dd></dl></div>')
            continue
        rows.setdefault(qid[:1], []).append(_qwr(f'<p class=q-head><b>{esc(qid)}</b></p>',
                                                 f'previous: {esc(row["previous"])}<br>this: {esc(row["this"])}',
                                                 f'{status} <span class=mut>{esc(row["why"])}</span>'))
    said = lambda xs: ("changed" if "changed" in xs else xs[0]) if xs else "all held"
    words = {lv: said([str(x).lower() for x in moved.get(lv, [])]) for lv in rows}
    if tabs:                                        # no tally line, no chips, no grey sentence (round 1)
        return VS_CSS + _by_level(rows, "", tabs=tabs, words=words) + f'<p class=vs-file>{_open(vs["file"], root, vs["file"].name)}</p>'
    return (f'<p><b>{esc(summary)}</b> · {_open(vs["file"], root, vs["file"].name)}</p><p>{chips}</p>'
            '<p class=mut>As the Job\'s run-compare wrote it; one clock moved, so "why" names its cause.</p>'
            + _by_level(rows, _qwr_head("Work · the two answers", "Report · status · why"), words=words))


VS_CSS = ("<style>.vs-q{padding:8px 2px;border-bottom:1px solid var(--line)}.vs-q:last-child{border-bottom:0}"
          ".vs-h{margin:0 0 4px;display:flex;gap:10px;align-items:baseline}.vs-ab{display:grid;grid-template-columns:44px minmax(0,1fr);"
          "gap:3px 10px;margin:0;font-size:14px;line-height:1.45}.vs-ab dt{color:var(--muted);font-size:12.5px}.vs-ab dd{margin:0;"
          "overflow-wrap:anywhere}.vs-file{font-size:13px;margin:8px 0 0}</style>")


def _full_answers(j: dict) -> dict:
    """{qid: (the previous Job's answer, this Job's answer)}, whole, from the two Jobs' Task faces; a page not
    written says so."""
    prev = j["path"].parent / j["previous"] if j.get("previous") else None
    before = {t["qid"]: t for t in (P.job(prev)["tasks"] if prev and prev.is_dir() else [])}
    now = {t["qid"]: t for t in j["tasks"]}
    said = lambda t: (str(t["face"].get("answer") or "").strip() if t else "") or ("⬜" if t else "")
    return {q: (said(before.get(q)), said(now.get(q))) for q in set(before) | set(now)}


def _tree(j: dict, root: Path, view: str, href) -> str:
    rows = {}
    for t in j["tasks"]:
        runs = [x for x in t["hard"] + t["soft"] if view == "All" or x.get("kind") == view]
        body = _runs_table(runs, root)
        rows.setdefault(t["qid"][:1], []).append(
            _fold(t["name"], str(t["face"].get("answer-status", "")),
                  f'<p><a href="{esc(href("", "", t["path"]))}">open its Task tab ↗</a></p>' + body))
    return ''.join(_fold(f"{lv} · {name}", "", "".join(rows[lv]), opened=True)
                   for lv, name, _ in LEVELS if rows.get(lv)) or "<p class=mut>No Task yet.</p>"


# ── a Job's Work: its steps, each a work panel over its result (b11 s12, 261022) ────────────────
# The work panel opens on demand, so a person can run a step themselves. The Job's Work is
# its steps in the order a Job runs, a tab each; a tab's work panel (what the step has, the first card's prompt with
# your notes, what is running, what a person signs) stays folded until opened, its result under it. It copies
# prompts only; nothing here writes.
WORK_STEPS = ("1 · Launch", "2 · Run", "3 · Write", "4 · Check", "5 · Compare", "6 · Close")
STEP_KEY = {s: s.split(" · ")[1].lower() for s in WORK_STEPS}         # a run card's `views` word
OLD_WORK = {"All": "2 · Run", "hard": "2 · Run", "soft": "4 · Check"}    # the Job → Task → Run tree's views
STEP_EMOJI = {"launch": "🚀", "run": "🧮", "write": "✍", "check": "🔍", "compare": "🔁", "close": "🔒"}
FINAL = ("ok", "refused")                 # a hard Run's answer; a refusal is an answer
WRITE_ORDER = "DIKWX"                     # pages are written up the DIKW levels, the Executive answers last
WRITE_CARD = {"D": "Write the Data report", "I": "Write the Information report", "K": "Write the Knowledge report",
              "W": "Write the Wisdom report", "X": "Write the overall report"}


def _work_facts(j: dict) -> dict:
    """What the Job's steps stand on, from its Tasks' faces and its Runs' cards: the questions still to run, write
    and check, the Job's own Runs by type, and what is running now."""
    live = [t for t in j["tasks"] if str(t["face"].get("answer-status", "")).lower() != "retired"]
    asked = [t for t in live if t["qid"][:1] in RUN_LEVELS]
    ran = [t for t in asked if t["hard"] and all(str(x.get("status")).lower() in FINAL for x in t["hard"])]
    # a page a CHECK returned (its check: line starts ↩) is not written: 3 · Write takes it back with the reason
    returned = [t for t in live if str(t["face"].get("check") or "").startswith("↩")]
    written = [t for t in live if is_written(t)]
    checked = [t for t in written if str(t["face"].get("check") or "").startswith("✅")]
    name = lambda ts: {t["name"] for t in ts}
    own = {}
    for x in j["runs"]:
        own.setdefault(_rtype(x), []).append(x)
    every = [x for t in j["tasks"] for x in t["hard"] + t["soft"]] + j["runs"]
    running = [x for x in every if str(x.get("status")).lower() in ("running", "started")
               or (x.get("kind") == "soft" and str(x.get("status")).lower() == "open")]
    return {"live": live, "asked": asked, "ran": ran, "unrun": [t for t in asked if t["name"] not in name(ran)],
            "failed": [t for t in asked if any(str(x.get("status")).lower() == "failed" for x in t["hard"])],
            "written": written, "unwritten": [t for t in live if t["name"] not in name(written)], "returned": returned,
            "checked": checked, "unchecked": [t for t in written if t["name"] not in name(checked)],
            "own": own, "running": running, "hard": [x for t in j["tasks"] for x in t["hard"]],
            "soft": [x for t in j["tasks"] for x in t["soft"]]}


def _work_states(j: dict, f: dict) -> dict:
    """Each step's chip, from disk: done, or the first step not done is next; the close is a person's, so it reads
    sign once every step before it is done."""
    has = lambda kind: any(_closed(x) for x in f["own"].get(kind, []))
    first = not j["previous"]
    compare = (has("propose") or (not first and (bool(j["vs"]) or has("compare"))))
    st = {"1 · Launch": "done" if has("launch") or f["ran"] else "todo",
          "2 · Run": "done" if not f["unrun"] and not f["failed"] else "todo",
          "3 · Write": "done" if f["live"] and not f["unwritten"] else "todo",
          "4 · Check": "done" if f["written"] and not f["unchecked"] and not f["unwritten"] else "todo",
          "5 · Compare": "done" if compare else "optional" if first else "todo",
          "6 · Close": "done" if j["state"] == "closed" or has("close") else "todo"}
    nxt = next((s for s in WORK_STEPS if st[s] == "todo"), "")
    if nxt:
        st[nxt] = "sign" if nxt == WORK_STEPS[-1] else "next"
    return st


def _work_step(sub: str, j: dict, f: dict) -> str:
    """The tab a link opens: the one it names (an older tree view opens its step), else the step that comes next."""
    sub = OLD_WORK.get(sub, sub)
    if sub in WORK_STEPS:
        return sub
    st = _work_states(j, f)
    return next((s for s in WORK_STEPS if st[s] in ("next", "sign")), WORK_STEPS[-1])


def _card_prompt(label: str, folder: str, me: str, prev: str) -> str:
    """The prompt of the Job › Work Details card named `label`, the Job filled in; '' without the cards."""
    card = next((c for c in run_cards() if c["level"] == "Job" and c["space"] == "Work Details" and c["label"] == label), None)
    if not card:
        return ""
    return _card_kind(card, {"j<NN>": me, "j<prev>": prev or "j<prev>"})["prompt"].replace("{folder}", folder)


def _still(tasks: list, what: str) -> str:
    """The Tasks a prompt names, six at most: a longer list is the step's own Input, which the agent reads too."""
    names = [t["name"] for t in tasks]
    more = f" and {len(names) - 6} more (the step's Input lists them)" if len(names) > 6 else ""
    return f" {what}: {', '.join(names[:6])}{more}." if names else ""


def _names(tasks: list) -> str:
    names = [t["name"] for t in tasks]
    more = f" · and {len(names) - 8} more" if len(names) > 8 else ""
    return (esc(" · ".join(names[:8])) + more) if names else "<span class=mut>none</span>"


def _level_card(title: str, done: int, total: int, body: str, open_: bool = False, chip: str = "") -> str:
    """A result card: its title and how many of its questions are done (or its own `chip`), folded until opened."""
    cls = "st-ok" if total and done == total else "st-warn"
    return (f'<details class="topic work-task"{" open" if open_ else ""}><summary><span class=related-head>'
            f'<b>{esc(title)}</b> <span class="st {cls}">{esc(mark(chip) if chip else far(done, total, "done"))}</span></span></summary>'
            f'<div class=work-body>{body}</div></details>')


def _page_link(t: dict, root: Path) -> str:
    return pop("/_board/insight-run?answer=" + rel(Path(t["path"]), root), f'{t["name"]} · the page', t["name"] + " ↗")


def _launch_step(j, b, r, f, root, href, ask):
    launch, power = f["own"].get("launch", []), f["own"].get("power", [])
    record = (", ".join(f'{x["run"]} · {x.get("status", "—")}' for x in launch) if launch else
              "none on disk; its Runs show the Job ran" if f["ran"] else "none yet")
    rows = [("Pins", esc(f'{_rlabel(b, j["release"])} × {_vlabel(b, j["data"])}')),
            ("Hash", esc(j["face"].get("hash")) if j["face"].get("hash") else "<span class=st-warn>not recorded</span>"),
            ("Launch", esc(record)),
            ("Power", esc(", ".join(f'{x["run"]} · {x.get("status", "—")}' for x in power)) if power else
             "read inside each Run" if f["hard"] else "not measured yet")]
    parts = {x.get("partition") for x in f["hard"]}
    result = (_level_card("The pins", 1 if j["face"].get("hash") else 0, 1, _band(j, b) + _job_prototype_line(r, root), True,
                          "pinned" if j["face"].get("hash") else "no hash")
              + _level_card("Each segment: n, power, refused", 1, 1, _cut_table(j), True, "by segment" if parts else "none yet"))
    return rows, [("Prompt", ask("Run the Job"))], result


def _job_prototype_line(r: dict, root: Path) -> str:
    return f'<p class=mut>{esc(r.get("label") or r["name"])}: {esc(rel(r["job"], root)) if r["job"] else "—"} (read only).</p>'


def _run_step(j, b, r, f, root, href, ask):
    states = dict.fromkeys(str(x.get("status") or "planned").lower() for x in f["hard"])
    rows = [("Questions run", far(len(f["ran"]), len(f["asked"]), "run", "not run yet")
             + " (the Data, Information and Knowledge questions)"),
            ("Runs on disk", esc(" · ".join(states)) or "none"),
            ("Still to run", _names(f["unrun"]))]
    parts = []
    for x in f["hard"]:
        p = x.get("partition") or x["run"].split("_", 1)[-1]
        if p not in parts:
            parts.append(p)
    cards = []
    for lv in RUN_LEVELS:
        ts = [t for t in f["asked"] if t["qid"][:1] == lv]
        if not ts:
            continue
        grid = []
        for t in ts:
            by = {(x.get("partition") or x["run"].split("_", 1)[-1]): x for x in t["hard"]}
            grid.append((f'<a href="{esc(href("", "", t["path"]))}">{esc(t["name"])}</a>',) + tuple(
                pop(run_url(by[p]["path"], root), by[p]["run"], MARK.get(str(by[p].get("status")), "·")) if p in by
                else "<span class=mut>·</span>" for p in parts))
        done = sum(1 for t in ts if t["name"] in {x["name"] for x in f["ran"]})
        cards.append(_level_card(f"{lv} · {LEVEL_WORD[lv]}", done, len(ts), table(("Task",) + tuple(_label(p) for p in parts), grid)))
    cards.append(_level_card("Every Run, by Task", len(f["ran"]), len(f["asked"]), _tree(j, root, "All", href)))
    return rows, [("Prompt", ask("Run a segment") + _still(f["unrun"], "Still to run, or to retire"))], "".join(cards)


def _write_step(j, b, r, f, root, href, ask):
    # a page is ready to write once its own Runs answered (W and X cite the answers below them); the rest wait on 2 · Run
    ran = {t["name"] for t in f["ran"]}
    ready = [t for t in f["unwritten"] if t["qid"][:1] not in RUN_LEVELS or t["name"] in ran]
    waiting = [t for t in f["unwritten"] if t not in ready]
    lv = next((t["qid"][:1] for t in sorted(ready, key=lambda t: WRITE_ORDER.find(t["qid"][:1]))), "")
    rows = [("Pages written", far(len(f["written"]), len(f["live"]), "written")),
            ("Next DIKW level", esc(f"{lv} · {LEVEL_WORD[lv]}") if lv else "<span class=mut>none ready to write</span>"),
            ("Still to write", _names(ready))] + ([("Returned by CHECK", _names(f["returned"]))] if f["returned"] else []) \
        + ([("Waiting on 2 · Run", _names(waiting))] if waiting else [])
    back = [t for t in f["returned"] if t["qid"][:1] == lv]
    prompts = [("Prompt", ask(WRITE_CARD[lv]) + _still([t for t in ready if t["qid"][:1] == lv], "Still to write")
                + (_still(back, "Returned by CHECK") + " Rewrite each from the reason on its check: line, then empty that "
                   "line." if back else ""))] if lv else []
    done = {t["name"] for t in f["written"]}
    cards = []
    for level in WRITE_ORDER:
        ts = [t for t in f["live"] if t["qid"][:1] == level]
        if ts:
            rows_ = [(_page_link(t, root), _st("↩ returned" if t in f["returned"] else t["face"].get("answer-status") or "open"),
                      esc(t["face"].get("answer") or "—")) for t in ts]
            cards.append(_level_card(f"{level} · {LEVEL_WORD[level]}", sum(t["name"] in done for t in ts), len(ts),
                                     table(("Task", "page", "its answer"), rows_)))
    return rows, prompts, "".join(cards)


def _check_step(j, b, r, f, root, href, ask):
    soft = lambda t, kind: next((x for x in t["soft"] if _rtype(x) == kind), None)
    rows = [("Still to check", _names(f["unchecked"]))]      # a check shows on its page's row, never as a tally
    prompts = [("Prompt · alignment", ask("Check alignment") + _still(f["unchecked"], "Still to check")),
               ("Prompt · CHECK", ask("Check a report") + _still(f["unchecked"], "Still to check"))]
    done = {t["name"] for t in f["checked"]}
    cards = []
    for level in WRITE_ORDER:
        ts = [t for t in f["written"] if t["qid"][:1] == level]
        if ts:
            cell = lambda x: _run_link(x, root, x["run"]) + " " + _st(x.get("status")) if x else "<span class=mut>—</span>"
            rows_ = [(_page_link(t, root), _st(t["face"]["check"]) if t["name"] in done else _check_form(t, root),
                      cell(soft(t, "check-alignment")), cell(soft(t, "check"))) for t in ts]
            left = sum(t["name"] not in done for t in ts)
            cards.append(_level_card(f"{level} · {LEVEL_WORD[level]}", len(ts) - left, len(ts),
                                     table(("Task", "CHECK", "alignment", "its check Run"), rows_),
                                     chip="to check" if left else "checked"))
    return rows, prompts, "".join(cards) or "<p class=mut>No page is written yet: 3 · Write comes first.</p>"


def _check_form(t: dict, root: Path) -> str:
    """A person's CHECK of one page, folded in its row (a person can do the CHECK without an agent):
    read the page ↗ and its Runs, tick that you did, then ✅ Pass or ↩ Return with a reason.
    POST /_board/insight-act writes the page's check: line and a pass of run-check-tNN (insight_act.py)."""
    import json
    body = lambda verdict: esc(json.dumps({"action": "check", "task": rel(Path(t["path"]), root), "verdict": verdict}))
    btn = lambda verdict, word: (f'<button type=button class=work-act data-post="/_board/insight-act" '
                                 f'data-body="{body(verdict)}" data-fields="attest why">{word}</button>')
    return (f'<details class=check-it><summary>not yet · check it</summary><p class=sign-row style="margin:6px 0">'
            f'<label><input type=checkbox name=attest> I read the page and its Runs\' results</label> '
            f'<input name=why placeholder="why, if it goes back" size=24> {btn("pass", "✅ Pass")} {btn("return", "↩ Return")}'
            f'</p></details>')


def _compare_step(j, b, r, f, root, href, ask):
    prev = j["previous"]
    propose = f["own"].get("propose", [])
    rows = [("Job before", esc(prev) if prev else "<span class=mut>none: the first Job</span>"),
            ("Comparison", _open(j["vs"]["file"], root, j["vs"]["file"].name) if j["vs"] else "<span class=mut>not written</span>"),
            ("Proposals filed", esc(", ".join(f'{x["run"]} · {x.get("status", "—")}' for x in propose)) if propose else
             "<span class=mut>none</span>")]
    prompts = ([("Prompt · compare", ask("Compare with the Job before"))] if prev else []) + [
        ("Prompt · propose", ask("Propose questions"))]
    result = _vs_previous(j, root) + (_level_card("Proposals filed", sum(_closed(x) for x in propose), len(propose),
                                                  _runs_table(propose, root), True) if propose else "")
    return rows, prompts, result


def _close_step(j, b, r, f, root, href, ask):
    st = _work_states(j, f)
    waits = [s for s in WORK_STEPS[:-1] if st[s] not in ("done", "optional")]
    close = f["own"].get("close", [])
    rows = [("State", _st(j["state"])), ("Waits on", esc(" · ".join(waits)) if waits else "<span class=st-ok>nothing</span>"),
            ("The close", esc(", ".join(f'{x["run"]} · {x.get("status", "—")}' for x in close)) if close else
             "<span class=mut>not yet: a person signs it</span>")]
    frozen = [("Pages", "every page as it reads now"), ("Runs", "every Run and its receipt"),
              ("Comparison", _open(j["vs"]["file"], root, j["vs"]["file"].name) if j["vs"] else "<span class=mut>none</span>")]
    return rows, [("Prompt", ask("Close the Job"))], _level_card("What the close freezes", len(WORK_STEPS) - 1 - len(waits),
                                                                 len(WORK_STEPS) - 1, _kv_table(frozen), True)


def _close_sign(j: dict, st: dict, folder: str) -> str:
    """🙋 Sign the close: a person's own sign once every step before it is done (POST /_board/insight-act, close)."""
    import json
    if j["state"] == "closed":
        return f'<p><span class="st st-ok">✓ closed</span> {esc(j["face"].get("signed") or "")}</p>'
    waits = [s for s in WORK_STEPS[:-1] if st[s] not in ("done", "optional")]
    if waits:
        return (f'<p><b>🙋 Sign the close</b> <button type=button class=work-act disabled>Sign the close</button> '
                f'<span class=mut>it waits on {esc(" · ".join(waits))}</span></p>')
    body = esc(json.dumps({"action": "close", "job": folder}))
    return (f'<p class=sign-row><b>🙋 Sign the close</b> <label><input type=checkbox name=attest> I read what the close '
            f'freezes</label> <button type=button class=work-act data-post="/_board/insight-act" data-body="{body}" '
            f'data-fields="attest">Sign the close</button></p>')


def _kv_table(rows: list) -> str:
    from live.draft_steps import _kv
    return _kv(rows)


WORK_PARTS = {"launch": _launch_step, "run": _run_step, "write": _write_step, "check": _check_step,
              "compare": _compare_step, "close": _close_step}
WORK_RUNNING = {"launch": ("launch", "power"), "run": ("partition", "cross", "pool"), "write": ("write", "overall"),
                "check": ("check", "check-alignment"), "compare": ("compare", "propose"), "close": ("close",)}


def _work_view(j: dict, b: dict, r: dict, f: dict, step: str, jdir: Path, root: Path, href) -> str:
    """One step tab: its work panel (Input, what is running, the prompt with your notes, the sign), folded until
    opened, then its Result."""
    from live.draft_steps import _kv, _part, _prompt_box, _step_box
    key = STEP_KEY[step]
    st = _work_states(j, f)
    folder, me, prev = rel(jdir, root), j["name"][:3], j["previous"][:3]
    rows, prompts, result = WORK_PARTS[key](j, b, r, f, root, href, lambda label: _card_prompt(label, folder, me, prev))
    now = "".join(f'<p class=run-now style="margin:0 0 8px;padding:6px 10px;border:1px solid var(--line);border-radius:3px">'
                  f'🏃 {_run_link(x, root, x["run"])} <span class=mut>'
                  f'{("since " + esc(x["started_at"])) if x.get("started_at") else ""}</span></p>'
                  for x in f["running"] if _rtype(x) in WORK_RUNNING[key])
    sign = (_close_sign(j, st, folder) if key == "close" else
            '<p><b>🙋 Or check a page yourself</b>: open its row in the Result below, read the page and its Runs, '
            'then ✅ Pass or ↩ Return with the reason.</p>' if key == "check" else "")
    body = ("<h4>Input</h4>" + _kv(rows) + now
            + "".join(_prompt_box(p, jdir, root, f"job-{key}-{k}", title) for k, (title, p) in enumerate(prompts) if p) + sign)
    return (_part("Operation") + _step_box(f"{STEP_EMOJI[key]} {step}", st[step], body)
            + _part("Result") + (result or "<p class=mut>Nothing here yet.</p>"))


def _work_kinds(j: dict, f: dict, root: Path) -> tuple:
    """The Work Space's buttons before the cards pick them (each keeps its past Runs): the cards of the open step."""
    pick = lambda xs, *kinds: [x for x in xs if _rtype(x) in kinds]
    return (_kind("Run the Job", "", rows=_rows(pick(j["runs"], "launch"), root)),
            _kind("Measure the power", "", rows=_rows(pick(j["runs"], "power"), root)),
            _kind("Run a segment", "", rows=_rows(f["hard"], root)),
            _kind("Pool or split", "", rows=_rows(pick(f["soft"], "pool"), root)),
            _kind("Write a report", "", rows=_rows(pick(f["soft"], "write"), root)),
            _kind("Write the overall report", "", rows=_rows(pick(j["runs"], "overall"), root)),
            _kind("Check alignment", "", rows=_rows(pick(f["soft"], "check-alignment"), root)),
            _kind("Check a report", "", rows=_rows(pick(f["soft"], "check"), root)),
            _kind("Compare with the Job before", "", rows=_rows(pick(j["runs"], "compare"), root)),
            _kind("Propose questions", "", rows=_rows(pick(j["runs"], "propose"), root)),
            _kind("Close the Job", "", rows=_rows(pick(j["runs"], "close"), root)))
