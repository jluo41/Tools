"""The 🛠 expression Task's steps: one view per step of a round (Rewrite, Run, Evaluate) and Release, with its
final labels."""
from __future__ import annotations

import json
import re
from pathlib import Path
from live import focus_page as F, frame
from live.ui_parts import _todo, plural_word

from live.labeling_step_parts import (_section, MV, _bar, _empty, _flow, _open, _prompt, _rerun, _step, _table, _turns,
                                      _view_url, esc, kind)
from live.labeling_step_states import _xruns, states


# a model run shows its state as a mark beside its name, never a word
RUN_MARK = {"done": "✅", "complete": "✅", "running": "🏃", "waiting": "🙋", "failed": "❗", "error": "❗"}

def _round(run: Path | None) -> str:
    m = re.search(r"_e(\d\d)$", run.name) if run is not None else None
    return f"e{m.group(1)}" if m else ""


def _json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None
    except ValueError:
        return None


def _meaning_strip(task: Path, root: Path) -> tuple[str, str]:
    """(the strip, the approved version or "") from the Job's meaning Task: expression runs only on a signed meaning."""
    got = MV.approved_meaning(task.parent)
    if got:
        mt, v, signed = got
        return (f'<div class=ls-strip>🔒 approved meaning {esc(v)} · fixed during rewriting · signed '
                f'{esc(signed["at"])}</div>', v)
    meaning = next((t for t in sorted(task.parent.iterdir()) if t.is_dir() and kind(t) == "meaning"), None)
    link = (f'<a class=fd-btn href="{esc(_view_url(meaning, root, "update"))}">Open meaning\'s Update</a>' if meaning else "")
    return _bar("⏳ No approved meaning yet: expression waits for your sign in 🧭 meaning's Update", link, "wait"), ""


def _round_turn(task: Path, root: Path, xr: dict, e: str, now: bool) -> tuple:
    """One round's box: its state read from its own Runs (round 2: e02 said "report sent" while Release said
    "released"), opening its round report in the pop-out."""
    mine = {role: [r for r in runs if _round(r) == e] for role, runs in xr.items()}
    rel, ev = (mine["release"] or [None])[-1], (mine["evaluate"] or [None])[-1]
    if rel is not None and MV.release_sign(rel):
        word = "released"
    elif rel is not None and MV.state(rel) == "done":
        word = "waits for your sign"
    elif ev is not None and MV.state(ev) == "done":
        word = "report sent"
    else:
        word = "in progress" if now else "done"
    report = ev / "result" / "round_report.md" if ev is not None else None
    href = frame._file_url(report, root) if report is not None and report.is_file() and F.inside(report, root) else ""
    return e, word, now, href, bool(href)


def x_view(task: Path, root: Path, key: str) -> tuple[str, str, str]:
    """(lead, process, results) for one expression step."""
    xr = _xruns(task)
    strip, v = _meaning_strip(task, root)
    rounds = sorted({_round(r) for r in xr["rewrite"] if _round(r)})
    now = rounds[-1] if rounds else "e01"
    last = {r: (runs[-1] if runs else None) for r, runs in xr.items()}
    turns = _turns(f"🛠 rounds under {v or 'the approved meaning'}",
                   [_round_turn(task, root, xr, e, e == now) for e in rounds] or [("e01", "next", True)])
    if v and key != "rewrite":                       # the approved meaning is read by Rewrite; said there once (round 2)
        strip = ""
    st = states(task, root)
    if key == "rewrite":
        # a round already rewritten: the prompt starts the next one (round 4: "done" still offered round e02 again)
        go = f"e{int(now[1:]) + 1:02d}" if st["rewrite"][0] == "done" and now[1:].isdigit() else now
        prompt = _prompt(task, root, "rewrite", "Rewrite", f"the whole round {go}", (
            f"Use /hai-labeling-expression on {task.name}, round {go}: rewrite the wording under meaning "
            f"{v or '<the approved mNN>'} from Train errors only, run the executors, evaluate, and stop at round report "
            f"{go}. Change no rule and ask me nothing: rule or label questions go to the round report."))
        process = _step("✏️ Rewrite expression", _flow(
            (f"Approved rules {v or 'mNN'}", "Train error analysis only", ""),
            ("🤖 Execution & Audit Agent", "wording · order · examples", last["rewrite"].name if last["rewrite"] else f"rNN_rewrite_{v or 'mNN'}_{now}"),
            (f"Expression {now}", "", "")) + prompt, st["rewrite"], empty="not run yet")
        changes = last["rewrite"] / "result" / "changes.md" if last["rewrite"] else None
        body = (F.markdown(changes.read_text(encoding="utf-8"), task, root) if changes and changes.is_file() else "")
        return strip + turns, process, _section("✏️ What the wording changed", body or _empty(
            "Nothing to show yet: this view will show what the round's rewrite changed."),
            f"{now} rewritten" if body else "nothing yet")
    if key == "run":
        process = _step("▶️ Run label executors", _flow(
            (f"{v or 'mNN'} + expression {now}", "Train + Test items", ""),
            ("🤖 Label executors", "the models this Job names", last["run"].name if last["run"] else "rNN_run_…"),
            ("Labels on Train and Test", "", "")) + _rerun(task, "Run", "rerun the executors", (
                f"To rerun this step alone (Rewrite's prompt runs the whole round): use /hai-labeling-expression on "
                f"{task.name}, step Run, round {now}: label Train and Test with {v or 'the approved meaning'} + {now} on "
                "the Job's executors; keep the reference labels hidden.")), st["run"], empty="not run yet")
        data = _json(last["run"] / "result" / "runs.json") if last["run"] else None
        items = lambda n: esc(plural_word(n, "item", "items") if isinstance(n, int) and not isinstance(n, bool) else n)
        rows = [(f'{RUN_MARK.get(str(r.get("state", "")).lower(), "⬜")} {esc(r.get("model", ""))}',
                 items(r.get("train", "")), items(r.get("test", "")))
                for r in (data or []) if isinstance(r, dict)]   # "24 items", never a bare "24"; a mark, never a state word
        return strip + turns, process, _section("▶️ Executor runs", _table(("model", "Train", "Test"), rows)
                                                if rows else _empty("Nothing to show yet: this view will show each model's run."),
                                                plural_word(len(rows), "model", "models") if rows else "nothing yet")
    if key == "evaluate":
        process = _step("🧮 Evaluate and analyze errors", _flow(
            ("Labels + reference labels", "hidden from the executors", ""),
            ("🤖 Execution & Audit Agent", "score by set; sort errors", last["evaluate"].name if last["evaluate"] else "rNN_evaluate_…"),
            (f"Round report {now}", "errors by kind", "and where the round goes")) + _rerun(
                task, "Evaluate", f"rerun round report {now}", (
                    f"To rerun this step alone (Rewrite's prompt runs the whole round): use /hai-labeling-expression "
                    f"on {task.name}, step Evaluate, round {now}: score by set and model, sort errors into the four "
                    f"kinds, and write round report {now} with its route.")), st["evaluate"], empty="not run yet")
        out = last["evaluate"] / "result" if last["evaluate"] else None
        report = out / "round_report.md" if out else None
        results = ""
        if report and report.is_file():
            head = next((ln.strip("# ").strip() for ln in report.read_text(encoding="utf-8").splitlines()
                         if ln.strip() and not ln.startswith("#")), report.name)
            meaning = next((t for t in sorted(task.parent.iterdir()) if t.is_dir() and kind(t) == "meaning"), None)
            href = _view_url(meaning, root, "prepare") if meaning else ""
            results += _section(f"📋 Round report {now}", f'<p class=pb-big>{esc(head)}</p><div class=ls-verbs>'
                                + (f'<span class="pb-pill ok">sent to meaning</span>' if "meaning" in head else "")
                                + _open(report, root, "Open the round report")
                                + (f'<a class=fd-btn href="{esc(href)}">Open in meaning</a>' if href and "meaning" in head else "")
                                + "</div>", "sent to meaning" if "meaning" in head else "written")
        errors = _json(out / "errors.json") if out else None
        if isinstance(errors, dict) and errors:
            num = lambda val: val.get("count", 0) if isinstance(val, dict) else val
            counts = {k: n for k, n in ((k, num(val)) for k, val in errors.items())
                      if isinstance(n, int) and not isinstance(n, bool)}
            total, seen = sum(counts.values()), [k for k, n in counts.items() if n]
            # the word counts the kinds that hold an error (round 2: "4 errors in 4 kinds" over tiles 0 · 0 · 0 · 4)
            word = plural_word(total, "error", "errors") + (f", all {seen[0]}" if len(seen) == 1 else
                                                            f" in {plural_word(len(seen), 'kind', 'kinds')}" if seen else "")
            results += _section("🔍 Errors, by kind", '<div class="pb-tiles ls-tiles4">' + "".join(
                f'<div class=pb-tile><span class=ls-num>{esc(val if not isinstance(val, dict) else val.get("count", ""))}</span>'
                f'<small>{esc(k)}</small></div>' for k, val in errors.items()) + "</div>", word)
        perf = _json(out / "performance.json") if out else None
        rows = [(esc(r.get("model", "")), esc(r.get("train", "")), esc(r.get("test", "")), esc(r.get("coverage", "")))
                for r in (perf or []) if isinstance(r, dict)]
        if rows:
            results += _section("📈 Labeling performance", _table(("model", "Train quality", "Test quality", "coverage"), rows),
                                plural_word(len(rows), "model", "models"))
        return strip + turns, process, results or _section(f"📋 Round report {now}", _empty(
            "Nothing to show yet: this view will show the round report, its errors by kind and each model's quality."),
            "nothing yet")
    # release
    crit = _json(last["release"] / "result" / "criteria.json") if last["release"] else None
    rows = [(str(c.get("name", "")), "", str(c.get("state", "not yet")), "", "", False) for c in (crit or []) if isinstance(c, dict)]
    rows = rows or [("Quality + coverage floors", "", "not yet", "", "", False), ("Strong-model non-regression", "", "not yet", "", "", False),
                    ("Cost per accepted item", "", "not yet", "", "", False)]
    met = all(r[2] in MV.MET for r in rows)
    out = last["release"] / "result" if last["release"] else None
    finals = out / "final_labels.jsonl" if out else None
    signed = MV.release_sign(last["release"])
    ready = bool(met and finals and finals.is_file())
    if signed:
        part = _bar(f"✅ {now} released {signed['at']}: its labels are final", "", "done big")
    elif ready:                                        # a sign needs no name (settled 5): the page shows the date
        part = _bar(f"✍️ Your sign: release {now} and its final labels",
                    f'<button type=button class=fd-btn data-approve="{esc(now)}" data-task="{esc(frame.rel(task, root))}">'
                    f'Sign release {esc(now)}</button><span class=ls-msg role=status></span>')
    else:
        part = _bar("✍️ Your sign: the release, once every criterion below is met",
                    '<button type=button class=fd-btn disabled>Sign release</button>', "wait")
    part += _prompt(task, root, "release", "Release", "check readiness", (
        f"Use /hai-labeling-expression on {task.name}, step Release: freeze {v or 'the approved meaning'} · {now} · "
        "its reference labels · the model settings, check the floors, non-regression and cost, and report pass or fail."))
    process = _step("🔒 Freeze a version and check release readiness", _flow(
        ("Frozen package", f"rules {v or 'mNN'} · expression {now}", "+ labels + model settings"),
        ("🤖 Agent + evaluation tools", "review staging evidence", "and acceptance criteria"),
        ("Pass or fail", "pass: release a qualified version", "fail: back to expression or meaning")) + part,
        ("released", "ok") if signed else ("waits for your sign", "you") if ready
        else ("criteria not met yet", "") if last["release"] else st["release"],
        f"✍️ Sign release {now} and its final labels", "not yet")
    results = _final_labels(finals, root, bool(signed)) + _section(
        "✅ Release criteria", _todo(rows), "all met" if met else "not met yet")   # each row shows its own
    results += _section("🧾 Fresh data for claims", '<p class=ls-line>claims about unseen items need data beyond the '
                                                    'audited staging set</p>', "no fresh check yet")
    return strip + turns, process, results


def _cite(path: Path, root: Path, cite: str) -> str:
    """A final label's card ("r08 Q5": the meaning Task's report form r08_…, its question Q5) as a link that opens that
    question in the pop-out (round 4: the cell was plain words); the words alone when no form is found."""
    m = re.match(r"^(r\d+)\s+(Q\d+)$", cite.strip())
    task = path.parents[3] if len(path.parents) > 3 else None   # <Task>/runs/<run>/result/final_labels.jsonl
    if not m or task is None or not task.parent.is_dir():
        return esc(cite)
    for meaning in (t for t in sorted(task.parent.iterdir()) if t.is_dir() and kind(t) == "meaning"):
        for run in sorted((meaning / "runs").glob(f"{m.group(1)}_collect_*")):
            form = run / f"{run.name}.html"
            if form.is_file() and F.inside(form, root):
                return (f'<a class=nw data-pop="{esc(cite)}" href="{esc(frame._file_url(form, root))}#{esc(m.group(2))}" '
                        f'title="{esc(run.name)}, {esc(m.group(2))}">{esc(cite)}</a>')
    return esc(cite)


def _final_labels(path: Path | None, root: Path, signed: bool) -> str:
    """The Job's outcome (the walkthrough, 261104: no page showed it): the counts, the file, and the rows you decided."""
    if not path or not path.is_file():
        return ""
    rows = [json.loads(ln) for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    count = lambda word: sum(r.get("label") == word for r in rows)
    yours = [r for r in rows if str(r.get("decided_by", "")).startswith(("you ", "your "))]
    tiles = (("items", len(rows)), ("unsafe", count("unsafe")), ("safe", count("safe")), ("you decided", len(yours)))
    body = ('<div class="pb-tiles ls-tiles4">' + "".join(f'<div class=pb-tile><span class=ls-num>{esc(v)}</span>'
                                                         f'<small>{esc(k)}</small></div>' for k, v in tiles) + "</div>")
    body += _table(("item", "label", "who decided", "card", "executors agree"),
                   [(esc(r["item_id"]), esc(r["label"]), esc(r["decided_by"]), _cite(path, root, r.get("cites") or ""),
                     "yes" if r.get("agree") else "no") for r in yours])
    body += f'<div class=ls-verbs>{_open(path.with_suffix(".md"), root, "Open all final labels")}</div>'
    return _section("🏷 Final labels", body, (f"{len(rows)} labels, signed" if signed else
                                             f"{len(rows)} labels, not signed yet"))
