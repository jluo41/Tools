"""The Block's Audience Report (s11): Summary, Rounds, Questions, Predicted vs observed, Method scorecard, Cost
(split from design_views.py, which re-exports every name here)."""
from __future__ import annotations

import re
from pathlib import Path

from live.frame import esc, pop, reader, rel, table
from live.design_views_parts import _st, _fold, _pairs, _qrow, _qhead, _mins, _job_link, _live, _pred, _passed, _cost
from live.design_views_channel import as_it_reads


# a Block question as a row (the same row the paper and insight Boards draw):
# Question (pill, mark, its title, the question, More) │ Task Work (the Jobs it rests on, numbered) │ Report (pill, status,
# title, its opening)
_MARK = {"answered": "✅", "partial": "🟡", "open": "🟡"}
_WORD = {"answered": "Answered", "partial": "Partly answered", "open": "Not answered yet"}


def _pill(text: str) -> str:
    return f'<span class="item-kind">{esc(text)}</span>'


def _report_page(q: dict, b: dict) -> Path | None:
    """A Block question's report Page: its `report:` folder's .md, or the .md itself."""
    rep = b["path"] / str(q.get("report", "")).rstrip("/") if q.get("report") else None
    if rep and rep.is_file():
        return rep
    return next(iter(sorted(rep.glob("*.md"))), None) if rep and rep.is_dir() else None


def _q_status(q: dict, b: dict) -> str:
    """Where a question stands: the register's answer-status, else its report's header (haipipe-report: the report's
    writer moves it), else open."""
    if q.get("answer-status"):
        return str(q["answer-status"])
    page = _report_page(q, b)
    m = re.search(r"(?m)^answer-status:\s*(\w+)", page.read_text(encoding="utf-8", errors="ignore")) if page else None
    return m.group(1) if m else "open"


def _q_asks(q: dict) -> str:
    return str(q.get("asks") or q.get("question") or "")


def _q_evidence(q: dict) -> list:
    """The Jobs a question rests on: `evidence:` (the design register), else `work:` (haipipe-report's)."""
    return [str(e).split("_")[0] for e in (q.get("evidence") or q.get("work") or [])]


def _opening(page: Path) -> str:
    """A report's Opening: its first paragraph that is not a header line or a heading."""
    text = page.read_text(encoding="utf-8", errors="ignore")
    return next((p.strip() for p in text.split("\n\n")[1:] if p.strip() and not p.lstrip().startswith(("#", "---"))), "")


def _report_side(q: dict, b: dict, root: Path) -> str:
    page = _report_page(q, b)
    status = _q_status(q, b)
    if page is None:
        return f'<p>{_pill("Report")} <span class=mut>{esc(_WORD.get(status, status))}</span></p><p class=mut>No report yet</p>'
    text = page.read_text(encoding="utf-8", errors="ignore")
    head = next((l[2:].strip() for l in text.splitlines() if l.startswith("# ")), page.stem)
    opening = _opening(page)
    return (f'<p>{_pill("Report")} <span class=mut>{esc(_WORD.get(status, status))}</span></p>'
            f'<p class=rp-title><b>{pop(reader(page, root), head, head + " ↗")}</b></p>'
            + (f'<p class=rp-text>{esc(opening)}</p>' if opening else "")
            + f'<p class=mut>report {esc(page.stem.split("_")[0])}</p>')


def _task_work(q: dict, b: dict, root: Path, href) -> str:
    jobs = {j["id"]: j for j in b["jobs"]}
    ev = [jobs[e] for e in _q_evidence(q) if e in jobs]
    items = []
    for j in ev:
        tested = [d["id"] for d in j["designs"] if (j["id"], d["id"]) in b["scores"]]
        gives = f'{", ".join(tested)} tested' if tested else ""
        outs = [x for x in ("ranking.csv" if j["ranking"] else "", "scores.csv" if tested else "") if x]
        items.append(f'<li><b>{_job_link(href, j)}</b> · {esc(j["goal"])} × {esc(j["method"])} {esc(j["version"])} × '
                     f'{esc(j["inputs"])}' + (f' · {esc(gives)}' if gives else "")
                     + (f' <span class=mut>→ {esc(" · ".join(outs))}</span>' if outs else "") + "</li>")
    tree = "".join(f'<div style="padding-left:22px"><code>{esc(j["id"])}</code> {esc(j["name"][4:])} '
                   f'<span class=mut>▸ {len(j["designs"])} designs · {_st(j["state"])}</span></div>' for j in ev)
    return (f'<p>{_pill("Task Work")} <span class=mut>{len(items)} Job{"" if len(items) == 1 else "s"}</span></p>'
            + (f'<ol>{"".join(items)}</ol>' if items else '<p class=mut>No Job named yet</p>')
            + (f'<div class=mut style="margin-top:8px"><code>{esc(b["path"].name.split("_")[0])}</code> '
               f'{esc(b["path"].name.split("_", 1)[-1])}{tree}</div>' if ev else ""))


def _questions(b: dict, root: Path, href) -> str:
    rows = [_qhead("Question", "Task Work", "Report")]
    for n, q in enumerate(b["questions"], 1):
        status, asks = _q_status(q, b), _q_asks(q)
        more = [f'<li><b>asks</b> · {esc(asks)}</li>'] if asks else []
        more += [f'<li><b>evidence</b> · {esc(" · ".join(_q_evidence(q)))}</li>',
                 '<li><b>asked by</b> · run-propose-questions, agreed by another agent</li>'
                 if any(r["type"] == "propose-questions" for r in b["runs"])
                 else '<li><b>asked by</b> · written into board.md, no run-propose-questions</li>']
        left = (f'<p>{_pill(f"Question {n}")} {_MARK.get(status, "⬜")}</p><p><b>{esc(q.get("title", ""))}</b></p>'
                + (f'<p>{esc(asks)}</p>' if asks and asks != q.get("title") else "")
                +                 f'<details><summary class=mut>More</summary><ul>{"".join(more)}</ul></details>')
        rows.append(f'<div class=q-row id="question-{esc(q.get("id", ""))}"><div class=q-l>{left}</div>'
                    f'<div class=q-w>{_task_work(q, b, root, href)}</div><div class=q-r>{_report_side(q, b, root)}</div></div>')
    if len(rows) == 1:
        return '<p class=mut>No Block question yet: board.md ## Questions (run-propose-questions).</p>'
    return ('<p class=mut>A Block question needs evidence from two or more Jobs; one Job\'s is the Job\'s.</p>' + "".join(rows))


def _costs(b: dict, root: Path, href) -> str:
    out = []
    for j in sorted(b["jobs"], key=lambda x: x["state"] != "released"):
        if j["state"] == "held" and not _live(j["designs"]):
            out.append(_fold(j["name"], f'{esc(j["method"])} {esc(j["version"])} · {esc(j["inputs"])} · held, no designs yet',
                             f'<p class=mut>{esc(j["hold"]) or "Held: its face says why."}</p>', mono=True))
            continue
        c = _cost(j)
        body = _pairs([("tokens / design", f'{esc(c["tokens"])} <span class=mut>(usage: not in the Run receipt yet)</span>'),
                       ("time / design", esc(_mins(c["per_design"]))), ("rounds", esc(f'{c["rounds"]:.1f} drafts a design')),
                       ("first try", esc(f'{c["first"]} of {c["n"]} passed on draft 1')),
                       ("per passed", esc(_mins(c["per_passed"]))), ("read from", "each Run's started_at → finished_at")])
        out.append(_fold(j["name"], f'{esc(j["method"])} {esc(j["version"])} · {esc(j["inputs"])} · {esc(_mins(c["per_design"]))} '
                                  f'a design · {c["first"]} of {c["n"]} first try', body, opened=not out, mono=True))
    return "".join(out) or '<p class=mut>No Job yet.</p>'


def _rank1(j: dict) -> dict | None:
    """The Job's top design by t99's ranking, or None before a rank."""
    order = sorted(j["ranking"], key=lambda r: int(r["rank"]) if str(r.get("rank", "")).isdigit() else 999)
    top = order[0].get("design") if order else None
    return next((d for d in j["designs"] if d["id"] == top), None)


def _approved(j: dict) -> tuple:
    """Who approved a Job's release and when, from its run-release Run: (short, full). `signed:` on the card says it
    in full ("<who> <YYMMDD> · in chat, all 10 at once"); an older card only says "signed by <who>" in `by:`."""
    r = next((r for r in j["runs"] if r["type"] == "release" and r["status"] == "closed"), None)
    if not r:
        return "", ""
    card = r["card"]
    full = str(card.get("signed") or "")
    if full.startswith("✅"):                  # a person's sign carries no name: ✅ <YYMMDD> · a person (261023)
        return "approved " + full.split("·")[0].strip(), full
    # an older card names the signer ("<who> 261012 · in chat …", or "signed by <who>" in by:); a page never shows a
    # name (a sign is ✅ <YYMMDD>, b12 j01; no personal marks on a board), so only its date is shown, and the hover
    # keeps the card's words after the name
    day = re.search(r"\b(\d{6})\b", full) or re.search(r"(\d{2})-(\d{2})-(\d{2})", str(card.get("finished_at", ""))[2:10])
    day = (day.group(1) if day.lastindex == 1 else "".join(day.groups())) if day else ""
    rest = full.split("·", 1)[1].strip() if "·" in full else ""
    return ("approved ✅ " + day if day else "approved"), ("✅ " + day + (" · " + rest if rest else "")).strip()


def _summary(b: dict, root: Path, href, jobs_table: bool = True) -> str:
    """The Block on one page, for a reader with five minutes, so the first page is the overview
    and summary: the goal, what the Block questions answer so far (the bottom line), one row per Job (its
    method, state and who approved it, top design and prediction, the reason on hover), what the experiment returned,
    and the next step, in plain words: ids such as M04 m3 or i1 only on hover (the demo: "without naming every part").
    Bottom up from the files the Runs wrote; it claims nothing new. No design cards and no long reasons here (JL
    261012: "do we really need to report this anywhere?"): each design's page and its Job's Review whole show them."""
    jobs = b["jobs"]
    if not jobs:
        return '<p class=mut>No Job yet: launch one from Description › Map.</p>'
    goals = "".join(f'<p><b>{esc(g.get("aim") or g.get("id", ""))}</b> <span class=mut>· {esc(g.get("who", ""))} · '
                    f'{esc(g.get("venue", ""))} · {esc(g.get("n", ""))} designs a Job</span></p>'
                    for g in b["goals"])
    answers = []
    for q in b["questions"]:
        status, page = _q_status(q, b), _report_page(q, b)
        if status in ("partial", "answered") and page:
            answers.append(f'<p>{_MARK.get(status, "")} <b>{pop(reader(page, root), q.get("title", ""), q.get("title", "") + " ↗")}</b> '
                           f'<span class=mut>({esc(_WORD.get(status, status).lower())})</span>'
                           + (f' {esc(_opening(page))}' if jobs_table else "") + '</p>')
    ranked = [j for j in jobs if j["ranking"]]
    released = sum(d["state"] == "released" for j in jobs for d in j["designs"])
    scores = list(b["scores"].values())
    waiting = [j for j in ranked if any(d["state"] == "kept" for d in j["designs"])]
    if waiting:
        nxt = ("a person reviews and approves " + " · ".join(_job_link(href, j) for j in waiting)
               + ": one sign freezes each kept design's prediction and releases it (each Job's Review and approve)")
    elif released and not b["observed"]:
        nxt = "launch the experiment with the released designs; each arm's result comes back here"
    elif b["observed"] and not scores:
        nxt = "score each tested design against its frozen prediction"
    else:
        nxt = "the next round, with new inputs (Rounds)"
    rows = []
    for j in jobs:
        d, n_kept = _rank1(j), sum(x["state"] in ("kept", "released") for x in j["designs"])
        n_rel = sum(x["state"] == "released" for x in j["designs"])
        short, full = _approved(j) if n_rel else ("", "")
        state = (f'<span title="{esc(j["hold"])}" style="border-bottom:1px dotted">held</span>' if j["state"] == "held"
                 else _st(f"released {n_rel}") + (f' <span class=mut title="{esc(full)}" style="border-bottom:1px dotted">'
                                                   f'{esc(short)}</span>' if short else "")
                 if n_rel else "kept · waiting for review" if n_kept
                 else "ranked" if j["ranking"] else esc(j["state"]))
        codes = f'{j["method"]} {j["version"]} · inputs {j["inputs"]}'
        rows.append((_job_link(href, j), f'<span title="{esc(codes)}" style="border-bottom:1px dotted">'
                     f'{esc(j["method_name"] or j["method"])}</span>',
                     esc(f'{n_kept} kept of {len(j["designs"])}') if j["designs"] else "—", state,
                     f'<a href="{esc(href("", "", d["path"]))}">{esc(d["id"])} · {esc(d["short"])}</a>' if d else "—",
                     _pred(d["prediction"], "cell") if d else "—"))
    hits = sum(s.get("direction") == "✓" for s in scores)
    inr = sum(s.get("in_range") == "✓" for s in scores)
    # on the focus page the goal × method matrix above already shows the goal and each Job's row (shown once)
    return ((goals if jobs_table else "") + "".join(answers)
            + (f'<p><b>Next:</b> {nxt}.</p>' if jobs_table else "")
            + (table(("Job", "method", "designs", "state", "top design", "predicted"), rows) if jobs_table else "")
            + (f'<p>Experiment results: {len(scores)} designs tested · direction right {hits} of {len(scores)} · in range '
               f'{inr} of {len(scores)} <span class=mut>(Predicted vs observed)</span></p>' if scores else "")
            + (f'<p class=mut>Done when: {esc(b["close"])}</p>' if b["close"] and jobs_table else "")
            + (f'<p>{pop("/" + rel(pdf, root), "summary.pdf", "One-page PDF ↗")} <span class=mut>for readers outside the '
               f'workbench (haipipe-design-delivery summary.py)</span></p>' if jobs_table and (pdf := b["path"] / "delivery" / "summary.pdf").is_file()
               else ""))


def _rounds(b: dict, root: Path, href) -> str:
    """The Block's memory, one round per inputs version (each round's results feed the
    next design): what the version holds, its Jobs and where they stand, what was released, what an Exp returned."""
    if not b["inputs"]:
        return '<p class=mut>No inputs version yet: Description › Inputs (run-add-inputs-i1).</p>'
    out = []
    for k, v in enumerate(b["inputs"]):
        man = v["manifest"]
        js = [j for j in b["jobs"] if j["inputs"] == v["id"]]
        ids = {j["id"] for j in js}
        n_rel = sum(d["state"] == "released" for j in js for d in j["designs"])
        n_kept = sum(d["state"] in ("kept", "released") for j in js for d in j["designs"])
        exps = [e for e in b["observed"] if any(a.get("job") in ids for a in e["arms"])]
        scored = [s for (jid, _), s in b["scores"].items() if jid in ids]
        body = _pairs([("inputs", f'<code>{esc(v["id"])}</code> · frozen {esc(man.get("frozen", "—"))} · {esc(man.get("new", ""))}'),
                       ("it holds", esc(" · ".join(dict.fromkeys(str(x.get("part", "")) for x in man.get("parts", []))) or "—")),
                       ("Jobs", "<br>".join(f'{_job_link(href, j)} {_st(j["state"])}' for j in js) or "—"),
                       ("released", esc(f"{n_rel} of {n_kept} kept designs")),
                       ("Exp results", " · ".join(esc(e["name"]) for e in exps)
                        or "<span class=mut>none yet: run-add-observed-eNN</span>"),
                       ("scored", esc(f"{len(scored)} designs") if scored else "—")])
        meta = (f'{len(js)} Jobs · {n_rel} released · ' + (esc("Exp " + ", ".join(e["id"] for e in exps)) if exps else "no Exp yet"))
        out.append(_fold(f'Round {k + 1} · {v["id"]}', meta, body, opened=k == len(b["inputs"]) - 1))
    nxt = (f'inputs-v{len(b["inputs"]) + 1}' if any(v["id"].startswith("inputs-v") for v in b["inputs"])
           else f'i{len(b["inputs"]) + 1}')                 # a Block on the newer names keeps them
    return ('<p class=mut>One round per inputs version: what it saw, what it made, what came back. A later version '
            'starts new Jobs (moved: inputs); a released design is never edited.</p>' + "".join(out)
            + f'<p class=mut>Next round: inputs version <code>{nxt}</code> (run-add-inputs-{nxt}) once an Exp has returned, '
              "holding its results and the insight Board's newer data version.</p>")


def _predicted(b: dict, root: Path, href) -> str:
    jobs = {j["id"]: j for j in b["jobs"]}
    rows = [_qhead("Design", "Predicted · frozen at release", "Observed · the Exp, its arm")]
    tested = []
    for e in b["observed"]:
        for a in e["arms"]:
            j, did = jobs.get(a.get("job", "")), a.get("design", "")
            d = next((x for x in j["designs"] if x["id"] == did), None) if j else None
            if not d:
                continue
            tested.append(d["path"])
            p, s = d["prediction"], b["scores"].get((j["id"], did), {})
            rows.append(_qrow(f'<b>{_job_link(href, j)} · <a href="{esc(href("", "", d["path"]))}">{esc(did)}</a></b>'
                              + as_it_reads(d["message"], d["path"], root),
                              f'{_pred(p)}<p class=mut>frozen {esc(p.get("frozen", "—"))}</p>'
                              f'<p class=mut>{esc(j["method"])} {esc(j["version"])} · {esc(j["inputs"])}</p>',
                              f'{esc(a.get("observed", "—"))} <span class=mut>· arm {esc(a.get("arm", ""))} of {esc(e["id"])}</span>'
                              f'<p>direction {_st(s.get("direction", "—"))} · in range {_st(s.get("in_range", "—"))}</p>'
                              f'<p class=mut>{esc(s.get("run", ""))} · totals per arm, never rows</p>'))
    if len(rows) == 1:
        return '<p class=mut>No Exp result yet: observed/eNN_<exp>/ is filled by run-add-observed-<eNN>.</p>'
    return "".join(rows)


def _scorecard(b: dict, root: Path, href) -> str:
    groups = {}
    for j in b["jobs"]:
        groups.setdefault((j["method"], j["version"]), []).append(j)
    out = []
    for (m, v), js in groups.items():
        live = sum((_live(j["designs"]) for j in js), [])
        scores = [s for (jid, _), s in b["scores"].items() if jid in {j["id"] for j in js}]
        hit = sum(s.get("direction") == "✓" for s in scores)
        inr = sum(s.get("in_range") == "✓" for s in scores)
        rate = f'{100 * len(_passed(live)) // max(len(live), 1)}%'
        body = _pairs([("Jobs", " · ".join(_job_link(href, j) for j in js)), ("pass rate", esc(rate)),
                       ("first try", esc(f'{sum(d["first_try"] for d in live)} of {len(live)}')),
                       ("tested", esc(f"{len(scores)} designs")), ("direction", esc(f"{hit} of {len(scores)}")),
                       ("in range", esc(f"{inr} of {len(scores)}")), ("tokens per passed", "—")])
        out.append(_fold(f"{m} {v}", f'{esc(" · ".join(j["name"] for j in js))} · pass {esc(rate)} · predictions '
                                     f'{inr} of {len(scores)} in range', body, opened=not out, mono=True))
    return ('<p class=mut>Summed from each Exp\'s scores.csv; with few arms tested, a match is only a hint.</p>'
            + ("".join(out) or '<p class=mut>No Job yet.</p>'))
