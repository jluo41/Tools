"""The design Block on the focus page (s51 Report, s52 Work): its parts (summary, goals, Jobs, rounds, methods) and
`block_view`, which regroups their sections into the Board's views (split out of design_focus.py)."""
from __future__ import annotations

import html as html_lib
import re
from pathlib import Path

from live import design_canvas as C
from live import design_reader as R
from live import design_views as V
from live.frame import esc, pop, reader, rel, table
from live.ui_parts import _cap, _kv
from live.design_focus_parts import _section
from live.design_focus_layout import CAPTIONS, OLD_BLOCK_VIEWS
from live.design_focus_parts import (_big, _chain, _closed, _copy, _href, _link, _link_btn, _plain, _session,
                                     _step, _tabs)
from live.design_focus_design import _goal_name, _job_closed, _job_next, _pvo, d_state

# ── the Block (s51 Report, s52 Work) ────────────────────────────────────────────────────────────────────────────


def _where(j: dict) -> str:
    """Where a Job is, in a few words, from what its Runs wrote."""
    short = V._approved(j)[0]
    if short:
        return short.replace("approved", "released") + (" · closed" if _job_closed(j) else "")
    if str(j["state"]).lower() == "held":
        return "held"
    if j["ranking"]:
        return "ranked"
    if j["designs"]:
        return "designs in review"
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
        return (f'{waiting} kept design{" waits" if waiting == 1 else "s wait"} for your review; '
                f'{released} {"is" if released == 1 else "are"} released.', "waiting for you")
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
                         '<p class=mut>No Job yet: launch one in Rounds.</p>', word, waits)
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
                ("N", esc(f'{g.get("n", "")} design{"" if str(g.get("n")) == "1" else "s"} a Job, from N + 5 ideas')),
                ("rules", V._ul([str(r) for r in g.get("rules") or []]) if g.get("rules") else "the shared ones only"),
                ("leave out", esc(g.get("leave-out", "") or "—")),
                ("Jobs", " · ".join(_link(j["path"], root, j["name"]) for j in jobs) or "none yet"),
                ("signed", esc(g.get("signed") or "not yet: a Job pins only a signed goal"))])


def _b_goals(b: dict, block: Path, root: Path) -> tuple:
    goals = b["goals"]
    signed = [g for g in goals if str(g.get("signed", "")).startswith("✅")]
    unsigned = [g for g in goals if g not in signed]
    rules = _rules_file(block)
    big = _big("" if goals else "No goal yet",
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
                + ('<p class=mut style="margin:8px 0 2px">What no design may use</p>' + V._ul(rules["leave"]) if rules["leave"] else ""))
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
    released = sum(bool(V._approved(j)[0]) for j in jobs)
    big = _big("" if jobs else "No Job yet",
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
        rows.append((f'{esc(_cap(step))} · {_link(j["path"], root, j["name"])}' if state == "waiting for you" else
                     _link(j["path"], root, j["name"]),
                     f'{_goal_name(b, j["goal"])} × {C.method_words(j["method"])}, {C.version_words(j["version"])}'
                     f' × {C.inputs_words(j["inputs"])}' + ("" if state == "waiting for you" else f' · next: {step}'),
                     state, verb))
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
    return ('<span class="pb-prompt in-copy dz-pick">+ Launch a Job '
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
    res = big + _section("🔁 The rounds", _tabs("round", tabs) or '<p class=mut>No inputs version yet: inputs/inputs-vN/.</p>',
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
    nxt = (f'inputs-v{len(b["inputs"]) + 1}' if any(v["id"].startswith("inputs-v") for v in b["inputs"])
           else f'i{len(b["inputs"]) + 1}')                 # a Block on the newer names keeps them
    released = any(d["state"] == "released" for j in b["jobs"] for d in j["designs"])
    proc = _step("🔁 The next round", [
        ("Add the Exp's data", "observed/eNN: per-arm totals only, never rows",
         "done" if b["observed"] else "open" if released else "waits on a release",
         _copy("run-add-observed-<eNN>", "Block", block, root)),
        (f"Add the next inputs version {nxt}", "inputs/inputs-vN/: rules, theory, the insight handoff, frozen",
         "open" if b["observed"] else "waits on the experiment", _copy("run-add-inputs-<vN>", "Block", block, root))])
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
        out.append((r, re.sub(r"^Proposal\s*·\s*|\s*\(.*\)$", "", head), passes[-1] if passes else None))
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
    scores = list(b["scores"].values())
    hits = sum(s.get("direction") == "✓" for s in scores)
    inr = sum(s.get("in_range") == "✓" for s in scores)
    big = _big(f"{len(scores)} design{'' if len(scores) == 1 else 's'} tested: {hits} in the predicted direction, "
               f"{inr} in range" if scores else "No method scored yet: scores come after the experiment",
               "a hint, not a verdict: few arms tested" if scores else "waits on an experiment")
    pvo, n = _pvo(b, b["jobs"], root)
    book = R.book_of(block)                                   # the method's own Block
    big += (f'<p>Its methods live in {_link(book, root, book.name)}: '
            + " · ".join(dict.fromkeys(j["release"] for j in b["jobs"] if j["release"])) + '.</p>') if book else ""
    res = big + _section("🎯 Predicted vs observed", pvo or '<p class=mut>No Exp result yet: observed/eNN_<exp>/ is filled by '
                         'run-add-observed-<eNN>.</p>', f"{inr} of {len(scores)} in range" if scores else "not tested yet")
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


def _split(html: str) -> tuple:
    """(what stands before the first section, {section title: its html}) of a part's top-level sections, so a view takes
    the sections it shows from the part that builds them."""
    out, depth, start, first = {}, 0, None, None
    for m in re.finditer(r"<section\b[^>]*>|</section>", html):
        if m.group(0).startswith("</"):
            depth -= 1
            if depth == 0 and start is not None:
                chunk = html[start:m.end()]
                title = re.search(r"<h3 class=fd-h>(.*?)(?:<span|</h3>)", chunk, re.S)
                out[html_lib.unescape(_plain(title.group(1))) if title else str(len(out))] = chunk
                start = None
            continue
        if depth == 0:
            start = m.start()
            first = m.start() if first is None else first
        depth += 1
    return (html if first is None else html[:first]), out


# which part builds each section of a Board view (the buttons regrouped in plain words; every section keeps
# its builder and its words). (part, "p" process or "r" results, section title)
BOARD_LAYOUT = {
    "designs": ("summary", [("summary", "r", "📊 Where each Job stands"), ("summary", "r", "➡️ Next"),
                            ("rounds", "r", "📋 What each Job kept"), ("summary", "p", "📄 Build the summary")]),
    "goals": ("goals", [("goals", "r", "🎯 The goals"), ("goals", "r", "📏 The shared rules"),
                        ("summary", "r", "❓ What the Block asks"), ("goals", "p", "🎯 Goals and rules")]),
    "inputs": ("rounds", [("rounds", "r", "📥 Inputs versions"), ("rounds", "r", "🔁 The rounds"),
                          ("rounds", "p", "🔁 The next round")]),
    "rounds": ("jobs", [("jobs", "r", "🗺️ Goals × methods"), ("jobs", "r", "🧭 What moves across the grid"),
                        ("jobs", "r", "📋 The Jobs"), ("jobs", "p", "🧭 Each Job's next move"), ("jobs", "p", "➕ A new Job")]),
    "tests": ("methods", [("methods", "r", "🎯 Predicted vs observed"), ("methods", "r", "🏅 Method scorecard"),
                          ("methods", "r", "⏱️ What each Job cost, by method"), ("methods", "p", "📏 Score and learn")]),
}
BLOCK_PARTS = {"summary": _b_summary, "goals": _b_goals, "jobs": _b_jobs, "rounds": _b_rounds, "methods": _b_methods}


def block_view(block: Path, root: Path, key: str) -> tuple:
    """(caption, lead, process, results, after) of a Board view: its big line from its leading part, then the sections
    BOARD_LAYOUT names, each drawn by the part that owns it. A Board with a Design Method Book leaves the method
    scorecard to the Book's Scorecard."""
    key = OLD_BLOCK_VIEWS.get(key, key)
    lead_part, layout = BOARD_LAYOUT[key]
    b, built = R.board(block), {}
    for name in dict.fromkeys([lead_part] + [n for n, _k, _t in layout]):
        proc, res = BLOCK_PARTS[name](b, block, root)
        built[name] = {"p": _split(proc), "r": _split(res)}
    has_book = R.book_of(block) is not None
    proc = res = ""
    for name, kind, title in layout:
        if has_book and title == "🏅 Method scorecard":
            continue
        chunk = built[name][kind][1].get(_plain(title), "")
        if kind == "p":
            proc += chunk
        else:
            res += chunk
    return CAPTIONS[key], "", proc, built[lead_part]["r"][0] + res, ""
