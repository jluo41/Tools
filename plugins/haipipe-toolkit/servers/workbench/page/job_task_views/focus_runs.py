"""A Run on the focus page: its files, data card and Run document, its rows, headline and tables."""
from __future__ import annotations

import copy
import re
import traceback
from pathlib import Path
from urllib.parse import urlencode

import yaml

from live import frame
from live.ui_parts import PB_CSS, PB_JS, _side_tabs
from live.focus_base import document, inside, markdown, page_url, plural
from live.focus_styles_bands import DC_CSS, FIT_FRAME_JS


# ── a Run's pop-out (JL 261103: "when I click a run, it will show all the information from that run folder with a pop
# out window, so we can quickly understand what happened"; drawn as b17-s58 screen P): everything in runs/<run>/, read
# in place: what happened, what it made (result/ as side tabs), how it ran (card, ticket, config), its passes ─────────
RUN_SHOW = (".md", ".txt", ".csv", ".tsv", ".json", ".yaml", ".yml", ".log", ".png", ".jpg", ".jpeg", ".svg", ".html")


RUN_BIG = 400_000                                       # a file past this is named, never read into the pop-out


def _read(path: Path, limit: int = RUN_BIG) -> str:
    try:
        if path.stat().st_size > limit:
            return ""
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def _run_file(path: Path, root: Path) -> str:
    """One result file shown as what it is: a picture, a small table, a mind map drawn, the Values tabs of a
    tables.json, or its text (round 3: a map and tables.json showed as raw text)."""
    url = frame._file_url(path, root)
    ext = path.suffix.lower()
    if ext in (".png", ".jpg", ".jpeg", ".svg"):
        return f'<a data-pop="{frame.esc(path.name)}" href="{frame.esc(url)}" target=_blank rel=noopener><img class="run-pic" src="{frame.esc(url)}" alt="{frame.esc(path.name)}"></a>'
    if ext == ".html":
        return f'<iframe class="run-frame" src="{frame.esc(url)}" title="{frame.esc(path.name)}"></iframe>'
    if path.name.endswith(".mindmap.md"):                 # a map, drawn as the page draws one, as tall as it is
        href = frame.ROUTE + "?" + urlencode({"path": frame.rel(path, root), "view": "focus-map"})
        return (f'<iframe class="find-map run-map" title="{frame.esc(path.name)}" src="{frame.esc(href)}&amp;fit=1" '
                'onload="window.fitMap&&fitMap(this)"></iframe>' + FIT_FRAME_JS)
    if path.name == "tables.json":                        # the Values tabs it holds, as the Job's Findings shows them
        values = _values_of(path, root)
        if values:
            return values
    text = _read(path)
    if not text:
        return f'<p class="mut">{frame.esc(path.name)} is large: <a href="{frame.esc(url)}" target=_blank rel=noopener>open it</a>.</p>'
    if ext in (".csv", ".tsv"):
        sep = "\t" if ext == ".tsv" else ","
        import csv as _csv, io as _io                # quoted cells keep their commas (261105: "2.35 (95% CI, 0.84 to
        rows = list(_csv.reader(_io.StringIO("\n".join(text.splitlines()[:21])), delimiter=sep))   # 3.85)" split a row)
        more = len(text.splitlines()) - 21
        head, body = rows[0], rows[1:]
        return ('<div class="run-table"><table><thead><tr>' + "".join(f"<th>{frame.esc(c)}</th>" for c in head)
                + "</tr></thead><tbody>" + "".join("<tr>" + "".join(f"<td>{frame.esc(c)}</td>" for c in r) + "</tr>" for r in body)
                + "</tbody></table></div>" + (f'<p class="mut">and {more} more rows</p>' if more > 0 else ""))
    lines = text.splitlines()
    shown = "\n".join(lines[:200])
    if ext == ".md":                                      # a report reads as a page, its marks drawn (261109: "**" and
        return (f'<div class="run-md">{markdown(shown, path.parent, root)}</div>'   # "- [x]" showed as typed)
                + (f'<p class="mut">{len(lines) - 200} more lines: <a href="{frame.esc(url)}" target=_blank rel=noopener>open the file</a></p>' if len(lines) > 200 else ""))
    return (f'<pre class="run-text">{frame.esc(shown)}</pre>'
            + (f'<p class="mut">{len(lines) - 200} more lines: <a href="{frame.esc(url)}" target=_blank rel=noopener>open the file</a></p>' if len(lines) > 200 else ""))


def _values_of(tables: Path, root: Path) -> str:
    """The 🔢 Values side tabs of a Run's tables.json (the paper's value_tabs, the Block's code), when it is its Job's
    newest; else nothing, and the file shows as text."""
    job = tables.parents[4] if len(tables.parents) > 4 else None
    newest = sorted(job.glob("t[0-9]*_*/runs/r[0-9]*/result/tables.json")) if job else []
    if not newest or newest[-1] != tables:
        return ""
    try:
        from live import board_evidence as be
        tabs = be.value_tabs(job, root)
    except Exception:                                 # noqa: BLE001 -- the raw file still shows
        traceback.print_exc()   # in the server log, not hidden (code review 261113)
        return ""
    if not tabs:
        return ""
    return (be.VALUES_CSS + _side_tabs("rV" + re.sub(r"\W", "", tables.parent.parent.name) + "x", [(h, w) for h, w, _ in tabs],
                                       [p for _, _, p in tabs]) + be.VALUES_DIALOG + be.VALUES_JS)


def run_order(f: Path):
    """What a reader reads first: the report and summary, then tables and figures, then the rest; logs and configs last."""
    name, ext = f.name.lower(), f.suffix.lower()
    rank = (0 if name in ("run-report.md", "summary.txt", "headline.txt") else 1 if ext == ".md" else
            2 if ext in (".csv", ".tsv", ".png", ".jpg", ".jpeg", ".svg", ".html") else
            4 if ext == ".log" or "config" in name or "snapshot" in name else 3)
    return rank, str(f)


_YAML_CACHE: dict = {}                       # str(path) -> ((mtime_ns, size), parsed dict)


def _yaml(path: Path) -> dict:
    """A Run's yaml card as a dict, parsed once per file version: a Board page reads the same 1,000+ run.yaml files
    several times per render, and parsing was seconds of it. Callers get their own copy."""
    try:
        st = path.stat()
    except OSError:
        return {}
    key, stamp = str(path), (st.st_mtime_ns, st.st_size)
    hit = _YAML_CACHE.get(key)
    if hit is None or hit[0] != stamp:
        try:
            data = yaml.safe_load(_read(path)) if path.is_file() else {}
        except yaml.YAMLError:
            data = {}
        if len(_YAML_CACHE) > 50000:
            _YAML_CACHE.clear()
        hit = _YAML_CACHE[key] = (stamp, data if isinstance(data, dict) else {})
    return copy.deepcopy(hit[1])


def ref_link(ref: str, run: Path, root: Path) -> str:
    """A path a Run's card names (reads, writes, feeds), as a link: into another Run, that Run's pop-out; a file, the
    file; a folder, its page. The path may count from the served root or from a folder above the Run (a Tools
    blueprint names its paths from the Tools root, "Tools/…" from a SPACE's). Not found, its words as they are."""
    ref = str(ref).strip()
    if not ref or ref.startswith(("/", "..")) or ".." in Path(ref).parts:
        return frame.esc(ref)
    bases = [root] + [p for p in run.parents if inside(p, root)] + ([root.parent] if ref.split("/")[0] == root.name else [])
    hit = next((b / ref for b in bases if (b / ref).exists() and inside((b / ref).resolve(), root)), None)
    if hit is None:
        rel = run / ref                                  # a Run's own result/…
        hit = rel if rel.exists() and inside(rel, root) else None
    if hit is None:
        return frame.esc(ref)
    hit = hit.resolve()
    other = next((p for p in [hit, *hit.parents] if p.parent.name == "runs" and inside(p, root)), None)
    name = hit.name or ref
    if other is not None and other != run.resolve():
        return f'<a data-pop="{frame.esc(other.parent.parent.name + " · " + other.name)}" href="{frame.esc(run_url(other, root))}">{frame.esc(ref)}</a>'
    if hit.is_file():
        return f'<a data-pop="{frame.esc(name)}" href="{frame.esc(frame._file_url(hit, root))}">{frame.esc(ref)}</a>'
    if other is not None:                                # a folder of this Run's own: its files are the tabs above
        return frame.esc(ref)
    return f'<a href="{frame.esc(page_url(hit, root))}" target=_top>{frame.esc(ref)}</a>'


# a Run's use case from the `type:` its run.yaml already holds (b17 delivery/page-spec/run-views.md): one Run type, every theme
RUN_USE_CASE = {'data': '🗃️ Data build', 'case': '🗃️ Data build', 'fit': '🧪 Model fitting', 'train': '🧪 Model fitting',
                'eval': '📏 Evaluation', 'evaluate': '📏 Evaluation', 'reg': '📈 Regression', 'describe': '📖 Description',
                'description': '📖 Description', 'value': '🔢 Values', 'delivery': '📦 Delivery',
                'paper-analysis': '📄 Paper analysis', 'citation': '📚 Citation check', 'display': '📊 Display',
                'section': '✍️ Writing', 'paragraph': '✍️ Writing', 'write': '✍️ Writing', 'revise': '✍️ Writing',
                'partition': '✂️ Partition', 'generate': '💡 Generate', 'verify': '✅ Verify', 'collect': '🙋 Collection',
                'draw': '🖍️ Drawing'}


def run_identity_html(run: Path, card: dict) -> str:
    """The line under a Run's title, as under a Block's, Job's or Task's (JL 261109: "could we also do the run type and
    use case"): 🧪 Run, and its use case from its type; a type not in the table shows as written."""
    declared = str(card.get("type") or ("collect" if "_collect_" in run.name else "")).strip()
    use = RUN_USE_CASE.get(declared.casefold(), declared if declared and declared.casefold() not in ("null", "none") else "")
    fields = [("Run type", "🧪 Run")] + ([("Use case", use)] if use else [])
    return '<dl class="job-identity">' + "".join(f"<div><dt>{k}</dt><dd>{frame.esc(v)}</dd></div>" for k, v in fields) + "</dl>"


def data_card(run: Path) -> dict:
    """A Run's result/data-card.yaml (generated by the project's data_card tool from the Task's scripts/data_card.yaml):
    {inputs: [{table, from, columns}], outputs: [{table, row, key, rows, size, columns: [{name, type, means}]}]}."""
    card = _yaml(run / "result" / "data-card.yaml")
    return card if isinstance(card, dict) and (card.get("inputs") or card.get("outputs")) else {}


def data_card_html(card: dict, compact: bool = False) -> str:
    """What a Run read and what it wrote (JL 261109: "cannot see what the output data's columns look like, and what is
    the input"): each input table with the columns it uses; each output table with its row, key, size and a
    Column | Type | Meaning table. `compact` (a Task's Runs) keeps the outputs only."""
    if not card:
        return ""
    esc, out = frame.esc, []
    words = lambda v: ", ".join(map(str, v)) if isinstance(v, list) else str(v or "")
    if not compact:
        for x in card.get("inputs") or []:
            if not isinstance(x, dict):
                continue
            cols = "".join(f"<code>{esc(c)}</code> " for c in (x.get("columns") or []))
            out.append('<div class="dc-table"><p class="dc-name"><span class="dc-tag">in</span> '
                       f'<code>{esc(x.get("table", ""))}</code></p>'
                       + (f'<p class="dc-meta">{esc(x["from"])}</p>' if x.get("from") else "")
                       + (f'<p class="dc-cols">{cols}</p>' if cols else "") + "</div>")
    for x in card.get("outputs") or []:
        if not isinstance(x, dict):
            continue
        rows = x.get("rows")
        size = " · ".join(s for s in ((f"{rows:,} rows" if isinstance(rows, int) else "rows not read back yet"),
                                       str(x.get("size") or "")) if s)
        meta = " · ".join(s for s in ((f'one row = {x["row"]}' if x.get("row") else ""),
                                       (f'key {words(x["key"])}' if x.get("key") else ""), size) if s)
        cols = [c for c in (x.get("columns") or []) if isinstance(c, dict)]
        table = ('<div class="run-table"><table><thead><tr><th>Column</th><th>Type</th><th>Meaning</th></tr></thead><tbody>'
                 + "".join(f'<tr><td><code>{esc(c.get("name", ""))}</code></td><td>{esc(c.get("type", ""))}</td>'
                           f'<td>{esc(c.get("means", ""))}</td></tr>' for c in cols) + "</tbody></table></div>") if cols else ""
        out.append('<div class="dc-table"><p class="dc-name"><span class="dc-tag out">out</span> '
                   f'<code>{esc(x.get("table", ""))}</code></p><p class="dc-meta">{esc(meta)}</p>{table}</div>')
    return "".join(out)


def run_document(run: Path, root: Path) -> str:
    """The Run's pop-out: 1 what happened (its headline and state), 2 what it made (result/ as side tabs, the report
    first, each file drawn as what it is), 3 how it ran (run.yaml in words, each path it reads or writes a link, its
    ticket, its config), 4 its passes (each with its log's last lines)."""
    card = _yaml(run / "run.yaml")
    result = run / "result"
    receipt = _yaml(result / "runtime.yaml")
    first = sorted((f for f in result.glob("*") if f.suffix.lower() in (".md", ".txt") and f.name != "headline.txt"),
                   key=run_order) if result.is_dir() else []   # no headline: the report's own first line says it
    summary = next((ln.strip(" #") for f in first[:1] for ln in _read(f).splitlines() if ln.strip()), "")
    status = str(receipt.get("status") or card.get("status") or "not run yet")
    if "_collect_" in run.name:                          # a form: its title and where it stands, never its target's
        form = (run / "question_collection.md")          # address (round 3: "r02's pop-out headline an id")
        title = next((ln[2:].strip() for ln in _read(form).splitlines() if ln.startswith("# ")), "") if form.is_file() else ""
        word = {"waiting": "waiting for you", "done": "answered", "complete": "answered", "planned": "not sent yet"}.get(status, status)
        head = f"{title} · {'answered' if (result / 'answer_collection.md').is_file() else word}" if title else ""
    else:
        head = (_read(result / "headline.txt").strip() or str(receipt.get("headline") or "") or summary
                or str(card.get("says") or card.get("ask") or ""))
    when = " to ".join(str(receipt[k])[:16].replace("T", " ") for k in ("started_at", "finished_at") if receipt.get(k))
    fail = str(receipt.get("failure") or "")
    passes = sorted((d for d in (run / "passes").glob("*") if d.is_dir()), reverse=True) if (run / "passes").is_dir() else []
    state = " · ".join(x for x in (status, when, f"newest pass {passes[0].name}" if passes else "") if x)
    sec = []
    sec.append('<h3 class="focus-sub">1 · 📌 What happened</h3>'
               + (f'<p class="run-head">{frame.esc(head)}</p>' if head else '<p class="mut">No headline written.</p>')
               + f'<p class="run-state">{frame.esc(state)}</p>' + (f'<p class="run-fail">{frame.esc(fail)}</p>' if fail else ""))
    dcard = data_card(run)                               # what it read and wrote, right after what happened (261109)
    n = 2
    if dcard:
        sec.append(f'<h3 class="focus-sub">{n} · 🔄 Data in and out · result/data-card.yaml</h3>' + DC_CSS + data_card_html(dcard))
        n += 1
    files = []
    if result.is_dir():
        found = sorted((f for f in result.rglob("*") if f.is_file() and f.suffix.lower() in RUN_SHOW   # headline.txt is part 1 already
                        and f.name not in ("runtime.yaml", "headline.txt", "data-card.yaml")
                        and inside(f, root)), key=run_order)
        files = found[:24]
    if files:                                            # side tabs, the one kind of tabs (round 3: "file tabs on top")
        names = [f.relative_to(result).as_posix() for f in files]
        sec.append(f'<h3 class="focus-sub">{n} · 📊 What it made · result/</h3>'
                   + _side_tabs("rT", [(n.removesuffix(".mindmap.md"), _file_kind(f)) for n, f in zip(names, files)],
                                [f'<div class=find-verbs><a href="{frame.esc(frame._file_url(f, root))}" target=_blank rel=noopener>'
                                 f'Open {frame.esc(f.name)} ↗</a></div>' + _run_file(f, root) for f in files]))
    else:
        outs = [x.get("table") for x in (dcard.get("outputs") or []) if isinstance(x, dict) and x.get("table")]
        said = ("No report or table in result/: it holds only its receipt and data card; the tables it wrote stay where "
                "Data in and out names them." if outs else "Nothing made yet.")   # say what is missing (261109)
        sec.append(f'<h3 class="focus-sub">{n} · 📊 What it made · result/</h3><p class="mut">{said}</p>')
    n += 1
    words = [("what it does", card.get("says") or card.get("role") or card.get("type")), ("kind", card.get("kind")),
             ("who", card.get("agent")), ("skill", card.get("skill")), ("reads", card.get("reads") or card.get("inputs")),
             ("writes", card.get("writes")), ("feeds", card.get("feeds")), ("ticket", card.get("ticket"))]
    linked = ("reads", "writes", "feeds")
    cell = lambda k, v: (", ".join(ref_link(x, run, root) for x in (v if isinstance(v, list) else [v])) if k in linked
                         else frame.esc(", ".join(map(str, v)) if isinstance(v, list) else str(v)))
    ticket = run / str(card.get("ticket") or "")
    if not ticket.is_file():
        ticket = next((f for f in sorted(run.glob(run.name + ".*")) if f.suffix in (".sh", ".ps1", ".cmd", ".md")), None)
    shown = ticket is not None and ticket.is_file() and inside(ticket, root)   # its fold below names it (261109: twice)
    rows = "".join(f'<tr><th>{frame.esc(k)}</th><td>{cell(k, v)}</td></tr>' for k, v in words if v and not (k == "ticket" and shown))
    config = next((f for f in (run / "config.yaml", run / "config.do") if f.is_file()), None)
    how = f'<table class="run-card">{rows}</table>' if rows else '<p class="mut">No run.yaml.</p>'
    for label, f in (("ticket", ticket), ("config", config)):
        if f and f.is_file() and inside(f, root):
            how += f'<details><summary>{label}: {frame.esc(f.name)}</summary>{_run_file(f, root)}</details>'
    sec.append(f'<h3 class="focus-sub">{n} · 🎫 How it ran · run.yaml, ticket, config</h3>' + how)
    n += 1
    if passes:
        items = ""
        for d in passes:
            title = (re.search(r"(?m)^#\s*(.+)$", _read(d / "pass.md")) or [None, ""])[1]
            title = re.sub(r"^" + re.escape(d.name) + r"\s*[·:-]?\s*", "", title)   # "p01-1031 p01-1031 · ..." (261109)
            log = next((f for f in sorted(d.rglob("*.log"), key=lambda f: f.stat().st_mtime, reverse=True)), None)
            tail = "\n".join(_read(log).splitlines()[-5:]) if log else ""
            items += (f'<li><b>{frame.esc(d.name)}</b> <span class="mut">{frame.esc(title)}</span>'
                      + (f'<pre class="run-text">{frame.esc(tail)}</pre>' if tail else "") + '</li>')
        sec.append(f'<h3 class="focus-sub">{n} · 🔁 Passes · passes/</h3><ul class="run-passes">{items}</ul>')
    css = ('<style>.job-identity{display:flex;flex-wrap:wrap;gap:8px 24px;margin:-4px 0 14px;font-size:13px;line-height:1.6}'
           '.job-identity>div{display:flex;gap:4px 8px}.job-identity dt{color:var(--muted)}.job-identity dd{margin:0;font-weight:600}'
           '.run-head{font-size:20px;margin:6px 0 2px}.run-state{color:var(--muted);margin:0 0 6px}.run-fail{color:#c92a2a}'
           '.run-pic{max-width:100%;height:auto}.run-frame{width:100%;height:480px;border:0}'
           '.run-text{white-space:pre-wrap;overflow-wrap:anywhere;font-size:12px;max-height:420px;overflow:auto;margin:0}.run-md{max-height:520px;overflow:auto;overflow-wrap:anywhere;font-size:14px;line-height:1.55}.run-md>:first-child{margin-top:0}'
           '.run-table{overflow:auto;max-height:420px;max-width:100%}.run-table table,.run-card{border-collapse:collapse;font-size:12px}'
           '.run-table td,.run-table th,.run-card td,.run-card th{border-bottom:1px solid var(--line);padding:3px 8px;text-align:left;vertical-align:top}'
           '.run-card td{overflow-wrap:anywhere}.run-card th{color:var(--muted);font-weight:400;white-space:nowrap}'
           '.run-card a{color:var(--accent);text-decoration:underline}'
           '.run-passes{list-style:none;padding:0}.find-verbs{margin:0 0 8px;font-size:13px}'
           '.find-map{display:block;width:100%;height:220px;border:1px solid var(--line);border-radius:8px}'
           '@media(max-width:600px){.run-table table,.run-table thead,.run-table tbody,.run-table tr,.run-table td,.run-table th'
           '{display:revert!important}}</style>')
    return document(f"{run.name} · Run", PB_CSS + css + '<main class="focus-page"><h1>' + frame.esc(run.name)
                    + '<span class="h1-section">Run</span></h1>' + run_identity_html(run, card) + '<p class="view-caption">Everything in runs/'
                    + frame.esc(run.name) + '/: what it made first, then how it ran.</p><section class="focus-card">'
                    + '<div class="focus-content">' + "".join(sec) + '</div></section></main>' + PB_JS)


def _file_kind(f: Path) -> str:
    """A result file's side-tab line: what it is, in a word."""
    name, ext = f.name.lower(), f.suffix.lower()
    return ("mind map" if name.endswith(".mindmap.md") else "Values tabs" if name == "tables.json" else
            "headline" if name == "headline.txt" else "table" if ext in (".csv", ".tsv") else
            "picture" if ext in (".png", ".jpg", ".jpeg", ".svg") else "page" if ext == ".html" else
            "report" if ext == ".md" else "text")


def run_url(run: Path, root: Path) -> str:
    return frame.ROUTE + "?" + urlencode({"view": "focus-part", "part": "run", "path": frame.rel(run, root)})


RUN_MARK = {"complete": "✅ done", "completed": "✅ done", "done": "✅ done", "ok": "✅ done", "succeeded": "✅ done",
            "failed": "❌ failed", "blocked": "🔶 blocked", "running": "⏳ running", "planned": "⬜ planned",
            "waiting": "🙋 waiting for you", "answered": "✅ done"}   # a form waiting on its person: one word in Report


def run_rows(task: Path) -> list:
    """A Task's Run folders with their mark and headline: one reading for Status's tree and the mind map."""
    rows = []
    for r in sorted(d for d in (task / "runs").glob("*") if d.is_dir() and not d.name.startswith((".", "_"))):
        rt, card = r / "result" / "runtime.yaml", r / "run.yaml"
        text = rt.read_text(encoding="utf-8", errors="ignore") if rt.is_file() else ""
        st = _yaml_status(text) or _yaml_status(card.read_text(encoding="utf-8", errors="ignore") if card.is_file() else "")
        rows.append((r, RUN_MARK.get(st, "⬜ not run"), run_headline(r)))
    return rows


def _yaml_status(text: str) -> str:
    """A receipt's or card's `status:`, its YAML quotes taken off (REACH's J21/J22 receipts write `status: "ok"`)."""
    return (re.search(r"(?m)^status:\s*(\S+)", text or "") or [None, ""])[1].strip("'\"")


def run_goal(run: Path) -> str:
    """What a Run must find out or make, in its own words: its card's `says:`, else its form's title (a collection Run),
    else its type."""
    card = _yaml(run / "run.yaml")
    said = str(card.get("says") or card.get("goal") or "").strip()
    if not said and (run / "question_collection.md").is_file():
        said = next((ln[2:].strip() for ln in (run / "question_collection.md").read_text(encoding="utf-8", errors="ignore").splitlines()
                     if ln.startswith("# ")), "")
    return said or str(card.get("type") or "").strip() or run.name.split("_", 1)[-1].replace("_", " ")


# ── a work Job's and Task's own output (round 2, 261106): a Task's Status shows what its newest Run returned (its
# headline, its Values or tables, its map), the same function in Report and Work; a Job's Status is the Block's numbered
# bars, each Task's headline on its closed row; a Job's Findings, each Task's headline as a side tab, then Values, Maps
# and Delivery, as the Block's Findings ────────────────────────────────────────────────────────────────────────────────
STAGE_WORD = {"explore": "exploring", "shaping": "shaping", "agreed": "agreed", "closed": "closed", "": "no stage"}


def run_headline(run: Path) -> str:
    """A Run's one-line result: its receipt's `headline:`, else result/headline.txt; one reading for Status, the map and
    the Findings."""
    rt = run / "result" / "runtime.yaml"
    text = rt.read_text(encoding="utf-8", errors="ignore") if rt.is_file() else ""
    line = re.search(r"(?m)^headline:.*$", text)
    try:                                         # as YAML reads it, its escapes decoded ("\xB7" is "·")
        head = str((yaml.safe_load(line.group(0)) or {}).get("headline") or "") if line else ""
    except yaml.YAMLError:
        head = (re.search(r'(?m)^headline:\s*"?(.*?)"?\s*$', text) or [None, ""])[1]
    if not head and (run / "result" / "headline.txt").is_file():
        head = (run / "result" / "headline.txt").read_text(encoding="utf-8", errors="ignore").strip().split("\n")[0]
    card = run / "result" / f"{run.name}.md"     # an older Paper Run (discovery): its Card's Readout, first sentence
    if not head and card.is_file():
        m = re.search(r"(?ms)^## Readout\s*\n(.*?)(?=^## |\Z)", card.read_text(encoding="utf-8", errors="ignore"))
        text = " ".join(m.group(1).split()) if m else ""
        head = re.split(r"(?<=[.!?])\s+", text, maxsplit=1)[0][:200]
    return head


def output_run(task: Path) -> Path | None:
    """The Task's newest Run that returned something: the newest Run, not a collection Run, with files in result/."""
    for run, _, _ in reversed(run_rows(task)):
        res = run / "result"
        if "_collect_" not in run.name and res.is_dir() and any(not p.name.startswith(".") for p in res.iterdir()):
            return run
    return None


def mark_word(mark: str) -> str:
    """'✅ done' -> 'done': a bar's state word carries no emoji."""
    return re.sub(r"^[^A-Za-z0-9]+", "", mark or "").strip()


def csv_table(path: Path, limit: int = 40) -> str:
    """A small CSV as a table, its first rows; the file itself one click away."""
    import csv
    try:
        rows = list(csv.reader(path.read_text(encoding="utf-8", errors="replace").splitlines()))
    except (OSError, csv.Error):
        return ""
    if not rows:
        return ""
    head, body = rows[0], rows[1:]
    more = len(body) - limit
    return ('<div class=wk-scroll><table class=wk-table><thead><tr>' + "".join(f'<th>{frame.esc(h)}</th>' for h in head)
            + '</tr></thead><tbody>' + "".join('<tr>' + "".join(f'<td>{frame.esc(c)}</td>' for c in r) + '</tr>'
                                               for r in body[:limit]) + '</tbody></table></div>'
            + (f'<p class=mut>{more} more rows in the file.</p>' if more > 0 else ""))


def table_section(run: Path, root: Path) -> tuple | None:
    """(title, html, word) of the tables a Run returned (its result/*.csv), a side tab each, the table drawn."""
    csvs = [p for p in sorted((run / "result").glob("*.csv")) if p.stat().st_size < RUN_BIG and inside(p, root)][:6]
    if not csvs:
        return None
    tabs, panels = [], []
    for p in csvs:
        n = max(0, len(p.read_text(encoding="utf-8", errors="replace").splitlines()) - 1)
        tabs.append((p.stem.replace("_", " "), plural(n, "row")))
        panels.append(f'<div class=find-verbs>{frame.pop(frame._file_url(p, root), p.name, p.name + " ↗")}</div>' + csv_table(p))
    # the word counts what the tabs are, its files, so it never disagrees with a headline that counts tables inside
    # them (round 3: "2 tables" under "3 source tables")
    return ("🗂️ Tables", _side_tabs("tT" + re.sub(r"\W", "", run.name) + "x", tabs, panels), plural(len(csvs), "file"))


def run_files(run: Path, root: Path) -> str:
    """A Run's result files as links that pop out, the Run itself first."""
    res = run / "result"
    files = sorted((p for p in res.iterdir() if p.is_file() and not p.name.startswith(".")), key=run_order) if res.is_dir() else []
    links = [frame.pop(run_url(run, root), f"{run.parent.parent.name} · {run.name}", f"Open {run.name} ↗")]
    links += [frame.pop(frame._file_url(p, root), p.name, p.name) for p in files[:12] if inside(p, root)]
    return '<div class=find-verbs>' + " · ".join(links) + '</div>'


def headline_section(task: Path, root: Path) -> tuple | None:
    """(title, word, body): the newest Run's headline as the bar itself, so it reads while closed; its files inside;
    None when no Run has returned anything."""
    rows = run_rows(task)
    run = output_run(task)
    if run is None:                              # nothing returned: no section (JL 261114: an empty section is not drawn)
        return None
    mark = next((m for r, m, _ in rows if r == run), "")
    head = run_headline(run)
    return "📌 " + (frame.esc(head) if head else "Headline"), mark_word(mark), run_files(run, root)
