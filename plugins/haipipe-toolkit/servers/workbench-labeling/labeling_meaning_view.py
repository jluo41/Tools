"""The 🧭 meaning Task's four steps: Frame, Prepare (the loop's report and its cases), Preferences (your answers)
and Update (the guideline your answers made)."""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import quote
from live import focus_page as F, frame
from live.ui_parts import _kv, _todo, plural_word

from live.labeling_step_parts import (_section, MV, SHOW, _bar, _chain, _empty, _flow, _link_tile, _prompt, _received, _rows,
                                      _step, _table, _turns, _view_url, _waiting_line, esc, kind)
from live.labeling_step_states import _current, _form_loop, _update_loop, states


# ── 🧭 meaning ───────────────────────────────────────────────────────────────────────────────────────────────────
def _map_html(m: dict, mark: dict | None = None) -> str:
    """One guideline version as a tree (s58 C2, C4): the question, its values, each value's rules. A rule's tag means
    one thing per view: in Report (`mark` given) the card of this loop's report that asks about it; in Update the card
    that set it (its note's "from rNN QN")."""
    branches = []
    for b in m["branches"]:
        leaves = []
        for r in b["rules"]:
            if mark is not None:
                tag, why = mark.get(r["text"].strip().lower(), ("", ""))
                tag = f"{tag} asks" if tag else ""
            else:
                tag, why = (f"from {r['tag']}" if r["tag"] else ""), r.get("cite") or r["note"]
            pill = f'<span class=ls-q title="{esc(why)}">{esc(tag)}</span>' if tag else ""
            leaves.append(f'<div class=ls-lf title="{esc(r["note"])}"><span>{esc(r["text"])}</span>{pill}</div>')
        branches.append(f'<div class=ls-br><div class=ls-bn>{esc(b["name"])}</div><div class=ls-lvs>'
                        + ("".join(leaves) or '<div class=ls-lf><span class=mut>no rule yet</span></div>') + "</div></div>")
    return (f'<div class=ls-map><div class=ls-root>{esc(m["root"] or "the question")}</div>'
            f'<div class=ls-brs>{"".join(branches)}</div></div>')


def _maps(task: Path, root: Path, on: str = "", mark: dict | None = None, sign: bool = True) -> str:
    """Every guideline version, one button each, the newest (or `on`) open: its tree, then its sign. `mark`: Report's
    {rule words: (QN, why)} for the open version; None in Update (each rule's own card)."""
    vs = MV.versions(task)
    if not vs:
        return ""
    on = on if on in dict(vs) else vs[-1][0]
    buttons = "".join(f'<button type=button class="ls-v{" on" if v == on else ""}" data-pbtab="lsmm{v}">{esc(v)}</button>'
                      for v, _ in vs)
    panels = []
    for v, path in vs:
        signed = MV.approval(task, v)                    # no person's name on a page (settled 5): the sign and when
        foot = (f"{v} · approved {signed['at']}" if signed else f"{v} · not approved yet") if sign else ""
        drawn = f"/_board/workbench?path={quote(frame.rel(path, root))}&view=focus-map"     # the drawn map, not its Markdown
        panels.append(f'<div class="pb-panel ls-mp" data-pbpanel="lsmm{v}"{"" if v == on else " hidden"}>'
                      + _map_html(MV.read_map(path), (mark if v == on else {}) if mark is not None else None)
                      + f'<p class=ls-foot>{esc(foot)} <a class=fd-btn data-pop="{esc(v)}" href="{esc(drawn)}">'
                      'Open the mind map</a></p></div>')
    return (f'<div class="pb-tabset ls-maps"><div class=ls-vrow><span>version</span>{buttons}</div>'
            + "".join(panels) + "</div>")


def _map_word(task: Path, v: str = "") -> str:
    """The guideline bar's word: its newest (or `v`) version and whether you signed it."""
    vs = dict(MV.versions(task))
    v = v if v in vs else (list(vs)[-1] if vs else "")
    if not v:
        return "nothing yet"
    return f"{v} approved" if MV.approval(task, v) else f"{v} not approved yet"


def _meaning_turns(loops: list, now_n: int, now_word: str = "", task: Path | None = None, root: Path | None = None) -> str:
    """Each loop's box opens that loop (round 2: Loop 1's decisions were on the rail only): a loop whose form waits
    opens Preferences, where it is answered; an answered loop pops out its form, the decision record."""
    def where(lp) -> tuple:
        if task is None:
            return "", False
        form = lp["collect"] / f"{lp['collect'].name}.html" if lp.get("collect") is not None else None
        if lp["state"] == "waiting for you":
            return _view_url(task, root, "preferences"), False
        if form is not None and form.is_file() and F.inside(form, root):
            return frame._file_url(form, root), True
        if lp["state"] == "answered; Update next" or lp["state"].startswith("made "):
            return _view_url(task, root, "update"), False
        return "", False
    turns = [(f"Loop {lp['n']}", lp["state"], lp["n"] == now_n, *where(lp)) for lp in loops]
    if now_n and all(lp["n"] != now_n for lp in loops):
        turns.append((f"Loop {now_n}", now_word or "next", True, ""))
    return _turns("🧭 meaning loops", turns)


def _draws(lp: dict | None) -> dict:
    """This loop's drawn sets, {typical | hard | blind: [item ids]} (the draw Run's draws.json); {} before a draw."""
    path = lp["draw"] / "result" / "draws.json" if lp is not None and lp.get("draw") is not None else None
    if path is None or not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8")).get("sets") or {}
    except ValueError:
        return {}


def _cases(task: Path, root: Path, lp: dict | None) -> tuple[str, str, str]:
    """This loop's typical, hard and random cases (use case 2: the draw Run's draws.json and signals.jsonl), each a
    table: item, why it was drawn, its current label, the card that shows it."""
    sets = _draws(lp)
    if not sets:
        return "", "", ""
    out = lp["draw"] / "result"
    sig = {}
    if (out / "signals.jsonl").is_file():
        for raw in (out / "signals.jsonl").read_text(encoding="utf-8").splitlines():
            try:
                row = json.loads(raw)
            except ValueError:
                continue
            sig[row.get("item_id")] = row
    cards = MV.cards_by_item(MV.report_json(lp["runs"]))
    now = _labels_now(task)

    def table(key: str, why: bool, hide: bool) -> str:
        ids = sets.get(key) or []
        if not ids:
            return ""
        rows = []
        for i in ids[:SHOW]:
            s = sig.get(i, {})
            label = "hidden until you judge it" if hide else (now.get(i) or s.get("label") or s.get("majority") or "no majority")
            card = cards.get(i)
            cells = [f"<span class=nw>{esc(i)}</span>"] + ([esc(", ".join(s.get("flags") or []) or "flagged")] if why else [])
            rows.append(tuple(cells + [esc(label), f"<span class=nw>{esc(card)}</span>" if card else "<span class=mut>no card</span>"]))
        more = esc(f"{len(ids) - SHOW} more in {lp['draw'].name}'s draws.json") if len(ids) > SHOW else ""
        head = ("item", "why flagged", "current label", "card") if why else ("item", "current label", "card")
        return _table(head, rows, more)

    return table("typical", False, False), table("hard", True, False), table("blind", False, True)


def _labels_now(task: Path) -> dict:
    """{item: label} from the newest Update's labels.jsonl (lNN), so a case shows what the last loop decided."""
    for run in reversed(MV.runs(task)):
        path = run / "result" / "labels.jsonl"
        if MV.role(run) == "update" and path.is_file():
            out = {}
            for raw in path.read_text(encoding="utf-8").splitlines():
                try:
                    row = json.loads(raw)
                except ValueError:
                    continue
                if row.get("item_id"):
                    out[row["item_id"]] = row.get("label") or "no majority"
            return out
    return {}


def _mark(lp: dict | None) -> dict:
    """{rule words: (QN, why)} for the rules this loop's report asks about: a card whose current_rule quotes a rule."""
    report = MV.report_json(lp["runs"]) if lp else None
    out = {}
    for i, card in enumerate((report or {}).get("cards") or [], 1):
        rule = re.sub(r"^R\d+:\s*", "", str(card.get("current_rule") or "")).strip().rstrip(".").lower()
        if rule and rule not in ("none yet", "none"):
            out.setdefault(rule, (f"Q{i}", f"asked in report-{lp['n']:02d}, Q{i}"))
    return out


def m_frame(task: Path, root: Path) -> tuple[str, str]:
    rec = MV.frame_record(task)
    prompt = _prompt(task, root, "frame", "Frame", "your rough idea", (
        f"Use /haipipe-labeling-interaction on {task.name}, step Frame: read the items and the old labels' sources this "
        "Job names, surface the assumptions in my idea below, then ask me the three frame questions (what to judge, "
        "which standard, who decides) as a frame form; record my answers as the frame."),
        (("Goal", "what the labels are for"), ("Use cases", "where they will be used"), ("Constraints", "data, time, who decides")))
    process = _step("🎯 Frame the labeling task", _flow(
        ("Rough idea + prepared items", "goals · use cases · constraints", "items, context, old labels"),
        ("🤖 Agent", "inspect items; surface assumptions", rec["run"].name if rec else "a frame Run, rNN_collect_frame"),
        ("Initial task agreement", "purpose · target population", "provisional labels")) + prompt, states(task)["frame"],
        _waiting_line(task, root, "frame", "🙋 The frame questions wait for your answers"), "not framed yet")
    if not rec or not rec["decisions"]:
        word = "waiting for you" if rec and rec["state"] == "waiting" else "not framed yet"
        results = _section("📜 Initial task agreement", _empty(f"Nothing to show yet ({word}): this view will show what "
                                                               "we judge, agreed before any rule."), "not agreed yet")
        return process, results                       # its form is this view's 🙋 Interaction (settled 3), never here
    first, rest = rec["decisions"][0], rec["decisions"][1:]
    results = _section("📜 Initial task agreement",
                       f'<p class=pb-big>{esc(first["decision"])}</p><p class=pb-state>agreed as frame f01</p>', "agreed")
    if rest:
        results += _section("❓ What you confirmed", _kv([(d["title"], esc(d["decision"])) for d in rest]),
                            f"{len(rest)} confirmed")
    return process, results


def m_report(task: Path, root: Path, loops: list) -> tuple[str, str]:
    n = _current(loops)
    lp = next((x for x in loops if x["n"] == n), None)
    collect = lp.get("collect") if lp else None
    prompt = _prompt(task, root, "prepare", "Prepare", f"Loop {n}'s report", (
        f"Use /haipipe-labeling-interaction on {task.name}, Loop {n}: prepare interaction report-{n:02d} from my sources, "
        "earlier decisions and any round report, its cases grouped typical, hard and random. Flags are hypotheses: no "
        "rule or label changes until I answer."))
    process = _step(f"🔍 Prepare Loop {n}'s report", _flow(          # the loop's words, not the file's (round 4)
        ("Human sources + reports", "ideas · notes · decisions", "earlier round reports · cases"),
        ("🤖 Alignment Agent", "/haipipe-labeling-interaction", collect.name if collect else f"rNN_collect_report_m{n:02d}"),
        (f"Loop {n}'s report", "cards with evidence", "for you to decide")) + prompt, states(task)["prepare"],
        f"🙋 Press {lp['draw'].name}: its ticket is ready" if lp and lp.get("draw") is not None else "", "next")
    maps = _maps(task, root, mark=_mark(lp))
    results = _section("🧠 Guideline rules, as a mind map", maps or _empty(
        "No guideline yet: Loop 1's Update writes m01, the rules as a mind map."), _map_word(task))
    # each loop's interaction report is this view's 🙋 Interaction, its last section (settled 3; round 2)
    typical, hard, blind = _cases(task, root, lp)
    sets = _draws(lp)
    count = lambda key: plural_word(len(sets[key]), "case", "cases") if sets.get(key) else "nothing yet"
    results += _section("📌 Typical cases", typical or _empty("No cases drawn yet for this loop."), count("typical"))
    results += _section("⚠️ Hard cases", hard or _empty("No flagged cases drawn yet for this loop."), count("hard"))
    results += _section("🎲 Random cases", blind or _empty("No random cases drawn yet for this loop."), count("blind"))
    return process, results


def m_preferences(task: Path, root: Path, loops: list) -> tuple[str, str]:
    lp = _form_loop(loops)
    if lp is None:
        n = _current(loops)
        process = _section("🙋 Collect preferences", _flow(
            (f"Loop {n}'s report", "earlier decisions", "evidence beside each card"),
            ("🙋 You", "confirm · clarify · revise · defer", f"rNN_collect_report_m{n:02d}"),
            ("Decision record", "preference · reason", "scope · version"))
            + _bar(f"No report waits for you: Prepare makes Loop {n}'s.", "", "wait"), "no report yet")
        return process, _section("🗒 Cards", _empty("Nothing to show yet: this view will show the report's cards and "
                                                     "your answers."), "nothing yet")
    n, run = lp["n"], lp["collect"]
    st, form = MV.state(run), run / f"{run.name}.html"
    if st == "waiting" and form.is_file():            # the form itself is this view's 🙋 Interaction (settled 3): the
        part = _prompt(task, root, "preferences", "Preferences", "send my answers", (   # prompt sends its answers
            f"Use /haipipe-labeling-interaction on {task.name}, Loop {n}: save my answers to report-{n:02d} ({run.name}: "
            "the block at the end, from its 'haipipe-interaction answers' line) with my notes, then start Update."),
            (("your notes", "optional: context for the decision record"),), cls="ls-send",
            attrs=f' data-form="{esc(frame._file_url(form, root))}"')
    elif st == "done":
        saved = run / "result" / "answer_collection.md"
        part = _bar(f"✅ Loop {n} · report-{n:02d} answered {_received(saved)}", "", "done")
    else:
        part = _bar(f"Loop {n} · report-{n:02d}'s form is not built yet: Prepare builds it.", "", "wait")
    process = _step("🙋 Collect preferences", _flow(
        (f"Loop {n}'s report", "earlier decisions", "evidence beside each card"),
        ("🙋 You", "confirm · clarify · revise · defer", run.name),
        ("Decision record", "preference · reason", "scope · version")) + part,
        ("waiting for you", "you") if st == "waiting" and form.is_file() else ("answered", "ok") if st == "done"
        else ("form not built yet", ""),
        _waiting_line(task, root, "preferences", f"🙋 Loop {n}'s report waits for your answers"))
    if st != "done":                                   # the step's Out: the decision record, once saved
        return process, _section("📦 Decision record", _empty(
            f"Not saved yet: Copy prompt sends your answers to report-{n:02d}, and the chat saves them here."),
            "not saved yet")
    picks, flags = {a["q"]: a for a in MV.answers(run / "result" / "answer_collection.md")}, MV.applied(run)
    rows = []
    for q, title in MV.questions(run):
        a, flag = picks.get(q), flags.get(q)
        said = ""
        if a:
            said = (f"{a['pick']} · {a['text']}" if a["pick"] and a["pick"] != "own" else a["text"] or "no option picked")
            said += f" · note: {a['note']}" if a["note"] else ""
        rows.append((f"{q} · {title}", said, flag[0] if flag else "saved", "", "", False))
    applied = sum(1 for f in flags.values() if f[0] == "applied")
    return process, _section("📦 Decision record", _todo(rows), f"{len(rows)} saved, {applied} applied" if rows else "saved")


def _label_changes(task: Path, lp: dict) -> list:
    """Reference label changes lNN: the Update Run's result/changes.md (or gold/versions/lNN/changes.md), one row per
    `- ` line or table row."""
    paths = ([lp["update"] / "result" / "changes.md"] if lp.get("update") is not None else [])
    paths.append(task / "gold" / "versions" / f"l{lp['n']:02d}" / "changes.md")
    for path in paths:
        if path.is_file():
            rows = []
            for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
                ln = raw.strip()
                if ln.startswith("- "):
                    rows.append(ln[2:])
                elif ln.startswith("|") and not re.match(r"^\|[\s:|-]+\|$", ln) and "item" not in ln.lower()[:12]:
                    rows.append(" · ".join(c.strip() for c in ln.strip("|").split("|") if c.strip()))
            return [(path, r) for r in rows]
    return []


def _ref_labels(upd: Path | None, root: Path, n: int) -> str:
    """The reference labels lNN an Update wrote (its result/labels.jsonl): how many items, each label's count, how
    many a person reviewed; nothing when it has not run. (A .jsonl in a labeling folder is never a static file.)"""
    path = upd / "result" / "labels.jsonl" if upd is not None else None
    if path is None or not path.is_file():
        return ""
    rows = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        try:
            row = json.loads(raw)
        except ValueError:
            continue
        if isinstance(row, dict):
            rows.append(row)
    labels = sorted({str(r.get("label") or "no majority") for r in rows})
    tiles = [("items", len(rows))] + [(lab, sum(str(r.get("label") or "no majority") == lab for r in rows)) for lab in labels]
    tiles.append(("you reviewed", sum(r.get("status") == "reviewed" for r in rows)))
    body = ('<div class="pb-tiles ls-tiles4">' + "".join(f'<div class=pb-tile><span class=ls-num>{esc(v)}</span>'
                                                         f'<small>{esc(k)}</small></div>' for k, v in tiles) + "</div>")
    return _section(f"🏷 Reference labels l{n:02d}", body, plural_word(len(rows), "label", "labels"))


def _said(what: str) -> str:
    """What applying an answer did, in plain words (round 2: the row read as a raw log line, "2026-11-04 21:40 ·
    r09_update_m02: guideline m02, rule '…'"): the rule as it now reads, else the line without its time and Run."""
    m = re.search(r"\brule '([^']+)'", what)
    if m:
        return f"rule now: {m.group(1)}"
    return re.sub(r"^\d{4}-\d\d-\d\d \d\d:\d\d\s*·\s*(r\d\d_\w+:\s*)?", "", what)


def _label_words(line: str) -> str:
    """A label change without the card it cites, which the row names already: "ex-20: unsafe → safe"."""
    return re.sub(r"\s*\(r\d+ Q\d+[^)]*\)", "", line)


def m_update(task: Path, root: Path, loops: list) -> tuple[str, str]:
    lp = _update_loop(loops)
    n = lp["n"] if lp else _current(loops)
    v, run = f"m{n:02d}", (lp or {}).get("collect")
    upd = (lp or {}).get("update")
    made = bool(lp and lp["map"])
    signed = MV.approval(task, v) if made else None
    if signed:
        part = _bar(f"✅ {v} approved {signed['at']}: expression may run on it", "", "done big")
    elif made:                                         # a sign needs no name (settled 5): the page shows the date
        part = _bar(f"✍️ Your sign: approve {v} and l{n:02d}; expression starts only after it",
                    f'<button type=button class=fd-btn data-approve="{esc(v)}" data-task="{esc(frame.rel(task, root))}">'
                    f'Approve {esc(v)}</button><span class=ls-msg role=status></span>')
    else:
        part = _bar(f"✍️ Your sign: approve {v} once Update has written it", f'<button type=button class=fd-btn disabled>'
                    f'Approve {esc(v)}</button>', "wait")
    part += _prompt(task, root, "update", "Update", "apply my answers", (
        f"Use /haipipe-labeling-interaction on {task.name}, step Update, Loop {n}: read "
        f"{run.name if run else 'the form'}'s answer_collection.md; write meaning {v} and labels l{n:02d}, each rule "
        f"naming its card; recheck affected items; anything unclear becomes a card for Loop {n + 1}, never a guess. "
        "Then wait for my sign."))
    process = _step("🔁 Integrate feedback and check alignment", _flow(
        ("Your answers", f"{run.name}'s answer_collection.md" if run else "the answered form", "+ earlier decisions and rules"),
        ("🤖 Alignment Agent", "reconcile; apply approved changes", upd.name if upd else f"rNN_update_{v}"),
        (f"Guideline {v}", "rules as a mind map", f"+ reference labels l{n:02d}")) + part,
        (f"{v} approved", "ok") if signed else (f"sign {v}", "you") if made else ("next", "") if lp else ("", ""),
        f"✍️ Approve {v} and l{n:02d}: expression starts only after it", "nothing to update yet")
    if not lp:
        return process, _section("🧠 Guideline rules, as a mind map", _empty(
            "Nothing to show yet: Update runs after you answer a report."), "nothing yet")
    results = _section("🧠 Guideline rules, as a mind map", _maps(task, root, on=v, sign=False) or _empty(
        f"{v} is not written yet: the Update prompt above writes it."), _map_word(task, v) if made else "not written yet")
    flags = MV.applied(run) if run else {}
    titles = dict(MV.questions(run)) if run else {}
    cite = (run.name.split("_", 1)[0] + " ") if run else ""
    changes = [w for _, w in _label_changes(task, lp)]
    rule = re.compile(r"^R\d+: rule_change\b")            # a rule answer the guideline took, said by the row itself
    rows, used = [], set()
    for q, (st, what) in flags.items():
        mine = [w for w in changes if f"({cite}{q})" in w or f"({cite}{q}," in w]
        used.update(mine)
        rows.append((f"{q} · {titles.get(q, '')}".strip(" ·"),
                     " · ".join([_said(what)] + [f"label {_label_words(w)}" for w in mine if not rule.match(w)]),
                     ("done", "ok") if st == "applied" else ("in progress", "run")))
    rows += [(f"label {_label_words(w)}", "", ("done", "ok")) for w in changes
             if w not in used and not w.startswith("no label") and not rule.match(w)]
    applied = sum(1 for st, _ in flags.values() if st == "applied")
    results += _section("📜 What your answers changed", _rows(rows) if rows else _empty(
        "No answer applied yet: Update flags each answer it applies."),
        ("all applied" if applied == len(flags) else "in progress") if flags else plural_word(len(rows), "label change", "label changes")
        if rows else "nothing yet")
    results += _ref_labels(upd, root, n)                 # lNN shown, not only named (round 2)
    deferred = [q for q, (st, _) in flags.items() if st == "in progress"]
    expression = next((t for t in sorted(task.parent.iterdir()) if t.is_dir() and kind(t) == "expression"), None)
    results += _section("➡️ Where it goes", '<div class=pb-tiles>' + _link_tile(
        "🛠 expression", f"{v} + l{n:02d}" + ("" if signed else ", after your sign"),
        _view_url(expression, root, "rewrite") if expression and signed else "", "Open expression") + _link_tile(
        f"🔍 Loop {n + 1}'s report", (f"{len(deferred)} open card{'s' if len(deferred) != 1 else ''} asked again"
                                      if deferred else "new cases"), _view_url(task, root, "prepare"), "Open Prepare")
        + "</div>", "expression open" if signed else "opens once signed")
    hist = []
    rec = MV.frame_record(task)
    if rec:
        hist.append(("frame", f"f01 ← {rec['run'].name}"))
    for x in loops:
        if x["map"]:
            src = x.get("collect")
            hist.append((f"Loop {x['n']}", f"{x['version']} ← {src.name if src is not None else 'its answers'}"))
    if hist:
        results += _section("🧾 Meaning history", _chain(hist), plural_word(len(hist), "version", "versions"))
    return process, results
