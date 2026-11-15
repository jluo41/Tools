"""One question drawn three ways (its logic, its work, its report) and the Overall answer: the executive line, its
sections, its cited figures, and the tabs that hold them."""

from __future__ import annotations

import re
from pathlib import Path

from live import insight_plan_c as P
from live.frame import esc, pop, rel
from live.insight_view_parts import (
    _st, _run_link, _open, LEVEL_WORD, _job_link, _rlabel, _vlabel, page_word, _task_link, far, _side_tabs)


# ── a question's row, Question │ Work │ Report, in the old board's richer style ─────
STEP = {"compute": "🧮 Compute", "cite": "📎 Reuse", "reuse": "📎 Reuse", "answer": "⚓ Answer", "judge": "⚓ Answer"}
_SPEC: dict = {}


def _spec(q: dict) -> dict:
    """The question's question.md front matter (name, ask, needs, ...), read once per change."""
    f = q.get("file")
    if not f or not Path(f).is_file():
        return {}
    key = (str(f), Path(f).stat().st_mtime)
    if key not in _SPEC:
        _SPEC[key] = P.front(Path(f))
    return _SPEC[key]


def _leads(report, k: int = 3) -> list:
    """A generated run report's lead lines (each need's point, first), without their table names."""
    if not report or not Path(report).is_file():
        return []
    lines = Path(report).read_text(encoding="utf-8", errors="ignore").splitlines()
    return [re.sub(r"\s*\(`[^`]+`\)$", "", x[2:]) for x in lines if x.startswith("- ")][:k]


def _cap(text: str) -> str:
    return (text[:1].upper() + text[1:]) if text else ""


def _q_logic(qid: str, q: dict, mark: str, root: Path, word: str = "") -> str:
    s = _spec(q)
    more = [(k, s.get(k)) for k in ("ask", "why", "answer") if isinstance(s.get(k), str) and s.get(k)]
    asked = (s.get("partitions") or {}).get("asked") if isinstance(s.get("partitions"), dict) else ""
    more += [("asked on", asked if isinstance(asked, str) else ", ".join(asked))] if asked else []
    body = "".join(f'<p><span class=mut>{esc(k)}:</span> {esc(v)}</p>' for k, v in more)
    cited = sorted({str(n["from"]).split(".")[0] for n in _needs(q) if isinstance(n.get("from"), str)
                    and re.match(r"^[DIKWX]\d+", str(n["from"]))})
    builds = ""
    if cited:
        by = {}
        for c in cited:
            by.setdefault(c[0], []).append(str(int(c[1:])))
        builds = ("<p class=mut>builds on " + "; ".join(f"{LEVEL_WORD[k]} questions {', '.join(v)}" for k, v in by.items())
                  + "</p>")
    from live.ui_parts import _pill
    return (f'<p class=q-head><span class=chip>Question {int(qid[1:])}</span> '
            + (_pill(word) if word else esc(mark)) + '</p>'
            + (f'<p><b>{esc(s.get("name"))}</b></p>' if s.get("name") else "")
            + f'<p>{esc(_cap(s.get("question") or q.get("question") or ""))}</p>' + builds
            + f'<details><summary class=mut>More</summary>{body}<p>{_open(q.get("file"), root, qid, "question.md")}</p></details>')


def _needs(q: dict) -> list:
    """The question's live needs (a retired or superseded one left out), in order."""
    return [n for n in (_spec(q).get("needs") or {}).values() if isinstance(n, dict) and not n.get("retired")]


def _goes(n: dict) -> str:
    """Where a step's result goes, or comes from: its tables, the need it reuses, or the page."""
    if n.get("output"):
        return " · ".join(n["output"])
    if isinstance(n.get("from"), str):
        return f"from {n['from']}"
    if n.get("kind") in ("judge", "answer"):
        return "made on the page"
    return ""


def _q_work(q: dict, trail: list) -> str:
    steps = "".join(f'<li><b>{esc(STEP.get(n.get("kind"), _cap(str(n.get("kind") or "step"))))}</b> · {esc(n.get("what", ""))}'
                    + (f' → <span class=mut>{esc(_goes(n))}</span>' if _goes(n) else "") + "</li>" for n in _needs(q))
    return (f'<details><summary><span class=chip>Task Work</span> <span class=mut>its steps</span></summary>'   # no count
            f'<ol>{steps}</ol></details>'
            + "".join(f'<p class=mut>{line}</p>' for line in trail))


def _takeaway(run: dict) -> str:
    """The takeaway of a question on one segment: its Task face's `takeaways: {<segment>: …}`, written by
    run-write-<tNN> with the Task's page (a part per segment); '' until then."""
    path = Path(run.get("path") or "")
    task = path.parent.parent if path.parent.name == "runs" else None
    if task is None:
        return ""
    got = (P.front(task / f"{task.name}.md").get("takeaways") or {})
    return str(got.get(run.get("partition"), "") or "") if isinstance(got, dict) else ""


def _q_report(name: str, run, root: Path, cut: str, extra: str = "") -> str:
    """The Report cell: the takeaway on this segment (not the numbers, what they add up to); the
    numbers stay one click away, in a fold and on the run page."""
    if not run:
        return f'<p class=mut>Not asked on this segment</p>{extra}'
    state = str(run.get("status") or "—")
    if "answer" in run:                                    # a carried board: the segment's answering page
        title = _open(run["report"], root, run["run"], run["answer"] or "the page") if run["report"] else esc(state)
        return f'<p class=q-head><b>{title}</b></p><p class=mut>{esc(run.get("how-sure") or "")}</p>{extra}'
    n = run.get("n")
    rows = f"{n:,} rows" if isinstance(n, int) else f"{n or '—'} rows"
    if state != "ok":
        word = {"refused": "Refused", "failed": "Failed", "planned": "Not run yet"}.get(state, _cap(state))
        return (f'<p>{_st(word)} · {_run_link(run, root)}</p>'
                + (f'<p class=mut>{esc(run.get("reason") or "")}</p>' if run.get("reason") else "") + extra)
    take = _takeaway(run)
    lead = (f'<p class=q-head>{esc(take)}</p>' if take else
            f'<p class=mut>Takeaway not written yet (run-write-{esc(Path(run["path"]).parent.parent.name[:3])})</p>')
    leads = _leads(run.get("report"))
    nums = (f'<details class=q-more><summary class=mut>the numbers · {_run_link(run, root)} · {esc(rows)}</summary>'
            + "".join(f"<p>{esc(_cap(x))}</p>" for x in leads) + "</details>")
    return lead + nums + extra


# ── the Overall Report: a Job's Executive answers as one document to read ─────────────
OVERALL = "Overall Report"
CITE = re.compile(r"\(([DIKWX]\d\d) · (t\d+)\)")


def _executive(j: dict) -> list:
    """The Job's Executive Tasks (X01, X02, ...), in question order; [] when its release asks none."""
    return sorted((t for t in j["tasks"] if t["qid"][:1] == "X"), key=lambda t: t["qid"])


def _sections(page) -> list:
    """A Task page's body as [(heading, markdown)]: its `# ` title and its **The ask** line left out, since the
    report shows the question itself."""
    text = Path(page).read_text(encoding="utf-8") if page and Path(page).is_file() else ""
    text = text.split("---", 2)[2] if text.startswith("---") else text
    out, head, buf = [], "", []
    for line in text.splitlines() + ["## "]:
        if line.startswith("## "):
            if "\n".join(buf).strip():
                out.append((head, "\n".join(buf)))
            head, buf = line[3:].strip(), []
        elif not line.startswith(("# ", "**The ask**")):
            buf.append(line)
    return out


def _cites(body: str, j: dict, root: Path) -> str:
    """Each `(K01 · t30)` in a rendered page a link to that Task's page, in the pop-out."""
    tasks = {t["name"].split("_", 1)[0]: t for t in j["tasks"]}

    def link(m):
        t = tasks.get(m.group(2))
        return m.group(0) if not t else "(" + pop("/_board/insight-run?answer=" + rel(Path(t["path"]), root),
                                                  f'{t["name"]} · the page', f"{m.group(1)} · {m.group(2)}") + ")"
    return CITE.sub(link, body)


def _fig_png(part: Path, j: dict, qid: str, name) -> Path:
    """An Executive figure as ref/overall_report.py draws it: under its Task's part of the Job's delivery
    (delivery/<job>/<tNN_X..>/), else the older delivery/<job>/figures/."""
    t = next((t for t in j["tasks"] if t["qid"] == qid), None)
    here = part / t["name"] / f"{qid}-{name}.png" if t else None
    return here if here and here.is_file() else part / "figures" / f"{qid}-{name}.png"


def _figure(qid: str, spec: dict, part: Path, j: dict, root: Path) -> str:
    """One figure an Executive page names (`figures:`), as ref/overall_report.py drew it into the Board's
    delivery/<job>/figures/ (a picture gives the outcome faster than the table): its outcome as a
    heading, the picture (a click opens it full size), and the answer it reads as a link."""
    title = esc(spec.get("title") or spec.get("name") or "")
    png = _fig_png(part, j, qid, spec.get("name"))
    tables = [x.get("table", "") for x in spec["rows"]] if isinstance(spec.get("rows"), list) else [spec.get("table", "")]
    src = ", ".join(dict.fromkeys(f"({m.group(2)} · {m.group(1)})" for t in tables
                                  if (m := re.match(r"^(t\d+)_([DIKWX]\d\d)_", str(t)))))
    if not png.is_file():
        return (f'<p class=rep-lead>{title}</p><p class=mut>Figure not drawn yet: ref/overall_report.py draws it '
                f'from {esc(src) or "its table"}.</p>')
    url = "/" + rel(png, root)
    return (f'<figure class=rep-fig><figcaption>{title}</figcaption><a href="{esc(url)}" target=_blank '
            f'rel=noopener><img src="{esc(url)}" alt="{title}" loading=lazy></a>'
            + (f'<p class=mut>from {_cites(esc(src), j, root)}</p>' if src else "") + "</figure>")


def _overall(j: dict, b: dict, r: dict, root: Path) -> str:
    """The Job's Overall Report (a summary to read before the Full report): its Executive answers as one document, a section per question from its Task page, each `(K01 · t30)`
    a link to the Task it rests on, its figure under its answer, and the print beside it. Read-only: an
    answer changes on its page, a figure by its page's `figures:` and ref/overall_report.py."""
    from live.page_reader import markdown_html
    xs = _executive(j)
    face = j["path"] / f'{j["name"]}.md'
    title = next((x[2:].strip() for x in face.read_text(encoding="utf-8").splitlines() if x.startswith("# ")),
                 j["name"]) if face.is_file() else j["name"]
    done = sum(bool(t["face"].get("answer")) for t in xs)
    part = b["path"] / "delivery" / j["name"]
    prints = sorted(f for f in part.glob("overall-report.*") if f.is_file()) if part.is_dir() else []
    one = (" · the print: " + " · ".join(f'<a href="/{esc(rel(f, root))}" target=_blank rel=noopener>'
                                            f'{esc(f.suffix[1:].upper())} ↗</a>' for f in prints)) if prints else \
        " · no print yet (ref/overall_report.py)"
    toc, body = [], []
    for n, t in enumerate(xs, 1):
        q = _spec(r["questions"].get(t["qid"], {}))
        name = str(q.get("name") or t["qid"])
        f = t["face"]
        first = next((x for x in f.get("figures") or [] if isinstance(x, dict)), None)
        png = _fig_png(part, j, t["qid"], first.get("name")) if first else None
        toc.append(f'<a href="#overall-{esc(t["qid"])}"><span>{n} · {esc(name)}</span>'
                   + (f'<b>{esc(first.get("title") or "")}</b><img src="/{esc(rel(png, root))}" alt="" loading=lazy>'
                      if png and png.is_file() else f'<b>{esc(f.get("answer") or "not written yet")}</b>') + "</a>")
        parts = []
        for head, md in _sections(t["page"]):
            html_ = _cites(markdown_html(md), j, root)
            parts.append(f'<details><summary>{esc(head)}</summary>{html_}</details>' if head.lower().startswith("what it rests")
                         else (f"<h4>{esc(head)}</h4>" if head and head.lower() != "answer" else "") + html_)
        body.append(f'<section id="overall-{esc(t["qid"])}"><h3>{n}. {esc(name)}</h3>'
                    f'<p class=rep-ask>{esc(_cap(str(q.get("question") or "")))}</p>'
                    + (f'<p class=rep-lead>{esc(f["answer"])}</p>' if f.get("answer") else
                       '<p class=mut>Not written yet: its page answers from the questions below it.</p>')
                    + (f'<p class=mut>How sure: {esc(f["how-sure"])}</p>' if f.get("how-sure") else "")
                    + "".join(_figure(t["qid"], spec, part, j, root) for spec in f.get("figures") or [] if isinstance(spec, dict))
                    + "".join(parts)
                    + f'<p class=mut>{_task_link(t, root)} · {esc(t["qid"])} · {_st(f.get("answer-status") or "open")}'
                      f' · CHECK {esc(f.get("check") or "not yet")}</p></section>')
    return (f'<article class=report-doc><h2>{esc(title)}</h2>'
            f'<p class=mut>{esc(_rlabel(b, j["release"]))} × {esc(_vlabel(b, j["data"]))} · <code>{esc(j["name"])}</code></p>'
            f'<p class=mut>answers {far(done, len(xs), "written")}{one}</p>'
            f'<p class=rep-glance-head>At a glance</p><nav class=rep-glance>{"".join(toc)}</nav>{"".join(body)}'
            '<p class=mut>Each answer rests on the Data, Information, Knowledge and Wisdom questions below it; a '
            '(K01 · t30) opens that Task\'s page.</p></article>')


def _overall_tabs(j: dict, b: dict, r: dict, root: Path, eid: str = "ov") -> str:
    """The Job's Overall Report as side tabs (one question open at a time keeps its figure beside
    its answer): each Executive question a tab, its state word on it; the open one's answer, its first figure, the
    other figures small, its page's sections, what it rests on folded; the print one click away above the tabs."""
    from live.page_reader import markdown_html
    xs = _executive(j)
    if not xs:
        return ""
    part = b["path"] / "delivery" / j["name"]
    prints = sorted(f for f in part.glob("overall-report.*") if f.is_file()) if part.is_dir() else []
    head = ('<p class=ov-print>The print: ' + " · ".join(              # the pair is the view's; its counts the bar's word
        f'<a href="/{esc(rel(f, root))}" target=_blank rel=noopener>{esc(f.suffix[1:].upper())} ↗</a>' for f in prints)
            + "</p>") if prints else ""
    items, panels = [], []
    for t in xs:
        q = _spec(r["questions"].get(t["qid"], {}))
        f = t["face"]
        figs = [x for x in f.get("figures") or [] if isinstance(x, dict)]
        first = _figure(t["qid"], figs[0], part, j, root) if figs else ""
        small = "".join(f'<a class=ov-thumb data-pop="{esc(x.get("title") or x.get("name") or "")}" href="/{esc(rel(p, root))}" '
                        f'target=_blank rel=noopener><img src="/{esc(rel(p, root))}" alt="" loading=lazy>'
                        f'<span>{esc(x.get("title") or x.get("name") or "")}</span></a>'
                        for x in figs[1:] for p in [_fig_png(part, j, t["qid"], x.get("name"))] if p.is_file())
        parts = []
        for h, md in _sections(t["page"]):
            html_ = _cites(markdown_html(md), j, root)
            parts.append(f'<details><summary>{esc(h)}</summary>{html_}</details>' if h.lower().startswith("what it rests")
                         else (f"<h4>{esc(h)}</h4>" if h and h.lower() != "answer" else "") + html_)
        items.append((f'{t["qid"]} · {q.get("name") or t["name"].split("_", 2)[-1].replace("-", " ")}', page_word(t)))
        panels.append('<div class="report-doc ov-one">'
                      f'<p class=rep-ask>{esc(_cap(str(q.get("question") or "")))}</p>'
                      + (f'<p class=rep-lead>{esc(f["answer"])}</p>' if f.get("answer") else
                         '<p class=mut>Its page answers from the questions below it; it is still to write.</p>')
                      + (f'<p class=mut>How sure: {esc(f["how-sure"])}</p>' if f.get("how-sure") else "")
                      + first + (f'<div class=ov-thumbs>{small}</div>' if small else "") + "".join(parts)
                      + f'<p class=mut>{_task_link(t, root)} · CHECK {esc(f.get("check") or "not yet")}</p></div>')
    return OV_CSS + head + _side_tabs(eid, items, panels)


OV_CSS = ("<style>.ov-print{font-size:13.5px;margin:0 0 8px}.ov-one{font-size:14.5px;max-width:none}.ov-one>*{max-width:none}.ov-one .rep-fig{max-width:620px}"
          ".ov-thumbs{display:flex;flex-wrap:wrap;align-items:flex-start;gap:10px;margin:4px 0 10px}.ov-thumb{display:block;width:150px;"
          "text-decoration:none;color:var(--mut);font-size:12px}.ov-thumb img{display:block;width:150px;border:1px solid "
          "var(--line);border-radius:6px;background:#fff}</style>")


def _board_overall(b: dict, root: Path, href) -> str:
    """The Board's Overall Report: its latest Job's, with the earlier Jobs' a click away."""
    jobs = [j for j in b["jobs"] if _executive(j)]
    j = jobs[-1]
    earlier = (" · earlier Jobs: " + ", ".join(_job_link(href, o) for o in jobs[:-1])) if jobs[1:] else ""
    return (f'<p class=mut>The latest Job\'s report, {_job_link(href, j)}{earlier}.</p>'
            + _overall(j, b, P.release(b["prototype"], j["release"]), root))
