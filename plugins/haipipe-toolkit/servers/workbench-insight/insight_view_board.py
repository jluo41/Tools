"""What each Space shows at an insight Board: the question map, the Question Book, the dataset and its versions,
the segments, coverage across Jobs, the Jobs, the Runs and the handoff."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import quote

from live import insight_plan_c as P
from live.frame import Space, delivery_view, esc, rel, table, themes
from live.insight_view_overall import _spec, _q_logic, _q_work, _q_report, OVERALL, _executive, _board_overall
from live.insight_view_parts import (
    LEVELS, READINGS, _kind, _next_line, _carded, _rows, _st, _fold, _run_link, _open, second_row, split,
    _qwr_head, _qwr, _by_level, _release_links, _where, _label, _part_names, _part_key, MARK, _job_link,
    _rlabel, _vlabel, WRITTEN, _runs_table, RUN_LEVELS, _rtype, is_written, written_of, page_word, _task_link, far, _side_tabs)


# ── the Board ───────────────────────────────────────────────────────────────────────────────────
def board_spaces(block: Path, root: Path, sub: str, href) -> dict:
    b = P.board(block)
    proto = b["prototype"]
    latest = proto["releases"][-1] if proto["releases"] else {"partitions": [], "name": "", "questions": {}}
    parts = _part_names(latest["partitions"])
    prel = rel(proto["path"], root) if proto["path"].exists() else str(b["face"].get("prototype", ""))
    desc = ("Map", "Question Book", "Dataset", "Partitions")
    d_open = sub if sub in desc else "Map"
    d_html = {"Map": _map, "Question Book": _prototype, "Dataset": _dataset, "Partitions": _partitions}[d_open](b, root, href)
    d_runs = {"Map": (_kind("Add a data version", "Add a data version to the Board {folder}: register the extract, frozen, "
                            "its rows counted per segment (run-add-version-data-v<M>)."),
                      _kind("Add a Job", "Add a Job to {folder}: pair a Question Book release with a data version, one clock "
                                         "moved from its neighbour (run-add-<jNN>; the Job folder jNN_question-vN-<slug>_data-vM carries the pair).", rows=_rows(b["runs"], root, "add"))),
              "Question Book": (_kind("Open the Question Book Block ↗", f"Open the Question Book Block {prel}: releases are cut there."),),
              "Dataset": (_kind("Add a data version", "Add a data version to the Board {folder} (run-add-version-data-v<M>)."),),
              "Partitions": (_kind("Propose a segment", f"Propose a segment for {prel}/proposals/ (run-propose-cut-<slug>): a segment is plan, so it lands "
                                                    "in the next release."),)}[d_open]
    told = [j for j in b["jobs"] if _executive(j)]          # Jobs whose release asks Executive questions
    a_subs = ((OVERALL,) if told else ()) + parts
    a_part, a_read = split(sub, a_subs, READINGS)
    a_html = _board_overall(b, root, href) if a_part == OVERALL else (
        second_row(href, "Audience Report", a_part, READINGS, a_read, "Reading")
        + {"Coverage": _coverage, "Tracks": _tracks, "Consistency": _consistency, "Findings": _findings}[a_read](
            b, root, _part_key(a_part), href))
    a_runs = {"Coverage": (_kind("Update the coverage", "Update the coverage of {folder}: what each Job asked and answered "
                                 "(run-coverage, reads the Jobs' receipts, never data).", rows=_rows(b["runs"], root, "coverage")),),
              "Tracks": (_kind("Draw a track", "Draw a question's track across the Jobs of {folder} (run-track-<q>).", rows=_rows(b["runs"], root, "track")),),
              "Consistency": (_kind("Check consistency", "Check consistency between two Jobs one clock apart in {folder} "
                                    "(run-consistency-<jA>-<jB>).", rows=_rows(b["runs"], root, "consistency")),),
              "Findings": (_kind("Ask a Block question", "Ask a Block question of {folder} (run-ask-<qNN>): a row in board.md ## Questions "
                                 "and reports/qNN_<topic>/."),
                           _kind("Write the report", "Write a Block question's report in {folder}/reports/qNN_<topic>/ "
                                 "(run-report-<qNN>), citing the reading it rests on.", rows=_rows(b["runs"], root, "report")),
                           _kind("Check a report", "Check a Block question's report in {folder} (run-check-<qNN>): every claim cites a Job.", run="run-check-<qNN>"))}[a_read]
    if a_part == OVERALL:                                    # written in the Job; the Board shows the latest one
        a_runs = (_kind("Open the latest Job ↗", f"Open the latest Job {rel(told[-1]['path'], root)}: its Overall Report "
                        f"is written there (run-overall-{told[-1]['name'][:3]})."),)
    rels = tuple(r["name"] for r in proto["releases"])
    w_open = sub if sub in rels else "All"
    r_views = ("All", "soft", "from below")
    r_open = sub if sub in r_views else "All"
    return _carded({
        "Description": Space(html=d_html, subspaces=desc, open=d_open, run_types=d_runs),
        "Audience Report": Space(html=a_html, subspaces=a_subs, open=a_part, run_types=a_runs,
                                 note="The latest Job's report: it is written and checked in that Job." if a_part == OVERALL else ""),
        "Idea Studio": Space(run_types=(_kind("Draw the question map", "Draw the question map of {folder} into studio/ (run-map-questions) "
                                              "(generated from the question files; view only)."),
                                        _kind("Add a topic", "Add or redraw a studio topic of {folder} (no Run: a pass in sNN-<topic>/passes/pNN-<MMDD>/): sNN-<topic>/, a pass per session."))),
        "Work Details": Space(html=_jobs(b, root, href, w_open), subspaces=("All",) + rels, open=w_open,
                              run_types=(_kind("Add a Job", "Add a Job to {folder} (run-add-<jNN>).",
                                               rows=_rows(b["runs"], root, "add")),
                                         _kind("Close a Job", "Close a Job of {folder} after its checks and its comparison "
                                                              "(run-close-<jNN>): frozen.",
                                               rows=_rows([r for j in b["jobs"] for r in j["runs"]], root, "close")))),
        "Runs": Space(html=_next_line(block) + _board_runs(b, root, r_open), subspaces=r_views, open=r_open,
                      run_types=(_kind("Add a Job", "Add a Job to {folder} (run-add-<jNN>).", rows=_rows(b["runs"], root, "add")),
                                 _kind("Update the coverage", "Update the coverage of {folder} (run-coverage).",
                                       rows=_rows(b["runs"], root, "coverage")),
                                 _kind("Check consistency", "Check consistency between two Jobs of {folder}.",
                                       rows=_rows(b["runs"], root, "consistency")))),
        "Delivery": Space(html=delivery_view(block, root, themes()["insight"]) + _handoff(b, root),   # cards (b10 s32-D18)
                          subspaces=("Handoff",), open="Handoff",
                          run_types=(_kind("Write the counsel", "Write the Wisdom counsel of {folder} from the latest Job."),
                                     _kind("Draft the handoff", "Draft the handoff of {folder} for a person to sign."))),
    }, "Block", {"Description": d_open, "Audience Report": "overall-report" if a_part == OVERALL else a_read, "Runs": r_open,
                 "Delivery": "handoff"})


def _map(b: dict, root: Path, href) -> str:
    """The two clocks crossed: a row per release (its name and slug, its questions, segments and signature), a
    column per data version (frozen date, rows), a Job in each cell with how far it has got."""
    versions = b["versions"]
    rels = b["prototype"]["releases"] or [{"name": n, "label": n, "questions": {}, "partitions": [], "face": {}}
                                          for n in sorted({j["release"] for j in b["jobs"]})]
    cell = {(j["release"], j["data"]): j for j in b["jobs"]}
    head = "".join(f'<th><b>{esc(_vlabel(b, v.get("version", "")))}</b><br><span class=mut>'
                   + esc(" · ".join(x for x in (f'frozen {v["frozen"]}' if v.get("frozen") else "",
                                                f'{v["rows"]} rows' if v.get("rows") else "") if x))
                   + "</span></th>" for v in versions)
    body = []
    for r in rels:
        signed = r["face"].get("signed") or ""
        facts = (f'{len(r["questions"])} questions · {len(r["partitions"])} segments<br>'
                 + (esc(signed) if signed else "⬜"))
        cells = [f'<td><b>{esc(r.get("label") or r["name"])}</b><br><span class=mut>{facts}</span></td>']
        for v in versions:
            j = cell.get((r["name"], v.get("version")))
            if not j:
                cells.append('<td>—</td>')                # a new Job is Work's (Jobs › ➕ A new Job), never Report's
                continue
            hard = [x for t in j["tasks"] for x in t["hard"]]
            count = {}
            for x in hard:
                count[x.get("status") or "planned"] = count.get(x.get("status") or "planned", 0) + 1
            runs = ", ".join(s for s, _ in sorted(count.items(), key=lambda kv: -kv[1]))
            done, asked = written_of(j["tasks"])
            cells.append(f'<td>{_job_link(href, j, short=True)} · {_st(j["state"])}<br><span class=mut>runs: '
                         f'{esc(runs) or "none"}<br>{far(done, asked, "answered")}</span></td>')
        body.append("<tr>" + "".join(cells) + "</tr>")
    return (f'<table class=wf-table style="width:auto"><tr><th>question version \\ data version</th>{head}</tr>'
            f'{"".join(body)}</table>')


def _prototype_tabs(b: dict, root: Path, eid: str) -> str:
    """The questions, question version by question version, as side tabs (the focus page; haipipe-ui: one kind of tabs, no count in a label):
    each question version a tab, its state word (signed or not), its questions by DIKW level as tables."""
    proto = b["prototype"]
    items, panels = [], []
    for r in reversed(proto["releases"]):                       # the newest plan first, open
        parts = []
        for lv, name, says in LEVELS:
            qs = [q for q in r["questions"].values() if q["id"][:1] == lv]
            if qs:
                rows = [(f'<b>{esc(q["id"])}</b>', _open(q["file"], root, q["id"], q["question"] or "<question>"),
                         esc(q["change"] or "—")) for q in qs]
                parts.append(f'<p class=pb-lv><b>{esc(name)}</b></p>'
                             + table(("#", "question", "change"), rows))
        signed = str(r["face"].get("signed") or "").startswith("✅")
        items.append((r.get("label") or r["name"], "✅" if signed else "1 waits for you" if parts else "⬜"))
        sign = ("" if signed or not parts or not r.get("job") else
                f'<p class=fd-wait>🙋 <a class=fd-btn data-pop="{esc(r.get("label") or r["name"])}" '
                f'href="/_board/workbench?path={quote(rel(Path(r["job"]), root))}&layout=focus&section=work&group=findings">Sign</a></p>')
        panels.append(sign + "".join(parts) or "<p class=mut>This version asks no question yet.</p>")
    return _side_tabs(eid, items, panels) if items else ""       # the ideas are the Question Book's (shown once)


def _prototype(b: dict, root: Path, href) -> str:
    proto = b["prototype"]
    out = [f'<p class=mut>The questions live in the Question Book Block: {esc(rel(proto["path"], root)) if proto["path"].exists() else "—"}'
           ' (read only here; releases are cut there).</p>']
    for k, r in enumerate(proto["releases"]):
        groups = []                     # one closed fold per DIKW level
        for lv, name, says in LEVELS:
            qs = [q for q in r["questions"].values() if q["id"][:1] == lv]
            if not qs:
                continue
            rows = [(f'<b>{esc(q["id"])}</b>', _open(q["file"], root, q["id"], q["question"] or "<question>"),
                     esc(q["change"] or "—"), _st(q["signed"] or "—")) for q in qs]
            new = sum((q["change"] or "") == "new" for q in qs)
            meta = f'{len(qs)} questions' + (f' · {new} new' if new else "")
            groups.append(f'<details class=topic><summary><b>{esc(name)} questions</b> <span class=topic-meta>{esc(meta)}</span>'
                          f'<span class=lv-link>{esc(says)}</span></summary>'
                          f'<div style="padding:4px 14px 10px">{table(("#", "question", "in this release", "signed"), rows)}</div></details>')
        meta = "✅" if str(r["face"].get("signed") or "").startswith("✅") else "⬜"
        out.append(_fold(f'release {r.get("label") or r["name"]}', meta, f'<div class=dikw>{"".join(groups)}</div>',
                         opened=k == len(proto["releases"]) - 1))
    props = [(_open(p["file"], root, p["title"]), esc(p.get("kind", "")), esc(p.get("from", "")), _st(p.get("state", "")))
             for p in proto["proposals"]]
    out.append(_fold("proposals/", "open" if props else "none", table(("proposal", "kind", "from", "state"), props)))
    return "".join(out)


def _dataset(b: dict, root: Path, href) -> str:
    on = {}
    for j in b["jobs"]:
        on.setdefault(j["data"], []).append(j)
    rows = []
    for v in b["versions"]:
        f = P.version_folder(v, root)
        man = P.data_folder(f, str(v.get("extract", "")))["manifest"] if f else {}
        rows.append((f'<b>{esc(v.get("version", ""))}</b>', f'<code>{esc(rel(f, root) + "/") if f else "—"}</code>',
                     esc(v.get("frozen") or man.get("end_date") or ""), esc(v.get("rows") or f'{man.get("n_rows", ""):,}'
                                                                           if man.get("n_rows") else v.get("rows", "")),
                     esc(v.get("new", "")), " ".join(_job_link(href, j) for j in on.get(v.get("version"), []))))
    return (f'<p class=mut>One dataset, <b>{esc(b["dataset"])}</b>, its versions frozen outside the Project, one folder each; '
            f'a new version is a new column of the Map. accumulates: {esc(b["accumulates"] or "—")}</p>'
            + table(("version", "folder", "frozen", "rows", "what is new", "Jobs on it"), rows)
            + "".join(_version(v, root, opened=k == len(b["versions"]) - 1) for k, v in enumerate(b["versions"])))


SAMPLE_N, SAMPLE_COLS = 5, 20          # rows drawn; columns shown first when a version names no preview:


def _raw(path: Path, root: Path) -> str:
    """A file under the SPACE as the host serves it (an image, a text file)."""
    from urllib.parse import quote
    return "/" + quote(rel(Path(path), root), safe="/")


def _version(v: dict, root: Path, opened: bool = True) -> str:
    """One data version, read from its folder (the folder is what a person hands over, so all of it is
    shown): its facts (manifest.json over board.md), then what the folder holds, each in a fold:
    the summary, the columns by group (data_dictionary.csv), a few rows, the figures, the documents, and the
    rest beside it. Read-only; a folder or file whose name starts with `_` is listed, never read."""
    name = str(v.get("version", ""))
    folder = P.version_folder(v, root)
    if not folder or not folder.is_dir():
        return _fold(f"{name} · its folder", "not on this machine",
                     f'<p class=mut>{esc(v.get("folder") or v.get("extract") or "no folder: or extract: in board.md")} '
                     'is not here.</p>', opened)
    d = P.data_folder(folder, str(v.get("extract", "")))
    m = d["manifest"]
    span = (" to ".join(str(x) for x in (m.get("start_date"), m.get("end_date")) if x)
            if m.get("start_date") else (f'to {m["end_date"]}' if m.get("end_date") else ""))
    facts = [(k, val) for k, val in (
        ("folder", f'<code>{esc(rel(folder, root))}/</code>'),
        ("the data", f'<code>{esc(d["data"].name)}</code>' if d["data"] else '<span class=st-warn>no single data file</span>'),
        ("rows · columns", esc(f'{m["n_rows"]:,} · {m.get("n_cols", "—")}' if m.get("n_rows") else v.get("rows", ""))),
        ("dates", esc(span)), ("frozen", esc(v.get("frozen", ""))), ("what is new", esc(v.get("new", ""))),
        ("made from", esc(" · ".join(str(x) for x in (m.get("source_set"), m.get("external_version")) if x))),
        ("built", esc(str(m.get("build_date") or "")[:10]))) if val]
    parts = [table(("fact", "value"), facts)]
    if d["summary"]:
        parts.append(_fold("summary", "cohort_summary.txt", f'<pre style="margin:0">{esc(d["summary"].strip())}</pre>', True))
    if d["dictionary"]:
        groups = {}
        for c in d["dictionary"]:
            groups.setdefault(c.get("group") or "—", []).append(c)
        rows = [(f'<b>{esc(g)}</b>' if i == 0 else "", f'<code>{esc(c.get("name", ""))}</code>', esc(c.get("dtype", "")),
                 esc(c.get("null_pct", "")), esc(c.get("n_unique", "")), esc(c.get("notes", "")))
                for g, cs in groups.items() for i, c in enumerate(cs)]
        parts.append(_fold("columns", f'{len(d["dictionary"])} in {len(groups)} groups · data_dictionary.csv',
                           table(("group", "column", "type", "null %", "distinct", "notes"), rows)))
    hide = tuple((m.get("groups") or {}).get("identity") or ())
    parts.append(_sample(v, d["data"], hide))
    if d["figures"]:
        thumbs = "".join(f'<a data-pop="{esc(f.name)}" href="{esc(_raw(f, root))}" target=_blank rel=noopener '
                         f'style="display:inline-block;width:220px;margin:0 10px 12px 0;vertical-align:top;text-decoration:none">'
                         f'<img src="{esc(_raw(f, root))}" alt="{esc(f.stem)}" loading=lazy '
                         f'style="width:220px;border:1px solid var(--line)"><br><span class=mut>{esc(f.stem)}</span></a>'
                         for f in d["figures"])
        parts.append(_fold("figures", f'{len(d["figures"])}', thumbs))
    for doc in d["docs"]:
        text = doc.read_text(encoding="utf-8", errors="replace")
        if doc.suffix.lower() == ".md":
            from live.paper import _md_view
            body = _md_view(text)
        else:
            body = f'<pre style="margin:0;white-space:pre-wrap">{esc(text[:20000])}</pre>'
        parts.append(_fold(doc.name, f"{esc(rel(doc, folder))} · a document of the version", body))
    if d["tables"]:
        parts.append(_fold("other tables", f'{len(d["tables"])}', "".join(
            f'<p><a data-pop="{esc(t.name)}" href="{esc(_raw(t, root))}" target=_blank rel=noopener>{esc(t.name)} ↗</a></p>'
            for t in d["tables"])))
    if d["other"]:
        parts.append(_fold("beside it", "listed, not read", "<p class=mut>In the folder but not part of the version "
                           "(a name that starts with _ is someone's work beside it).</p>"
                           + "".join(f'<p><code>{esc(rel(o, folder))}{"/" if o.is_dir() else ""}</code></p>' for o in d["other"])))
    return _fold(f"{name} · what its folder holds", f'{rel(folder, root)}/', "".join(parts), opened)


def _sample(v: dict, data, hide: tuple = ()) -> str:
    """A few rows of a version's data, to show what it looks like: drawn at random with a seed fixed
    per version, so the same rows on every load. One column a row, one sample row a column; the version's
    `preview:` columns (else up to SAMPLE_COLS that differ across the sample) first, the rest folded.
    Identifying columns (the dictionary's identity group, ids, zips, NPI) and free text are never shown."""
    import zlib
    name = str(v.get("version", ""))
    s = P.sample_rows(data, SAMPLE_N, zlib.crc32(name.encode()), hide) if data else {}
    if not s:
        return _fold("a few rows", "not readable here", "<p class=mut>No parquet data file in the folder.</p>")
    vals = dict(zip(s["columns"], zip(*s["rows"]))) if s["rows"] else {}
    picked = [c for c in (v.get("preview") or []) if c in vals]
    first = picked or [c for c in s["columns"] if len(set(vals[c])) > 1][:SAMPLE_COLS]
    rest = [c for c in s["columns"] if c not in first]
    heads = ("column",) + tuple(f"row {i + 1}" for i in range(len(s["rows"])))

    def grid(cols):
        return table(heads, [(f"<code>{esc(c)}</code>",) + tuple(esc(x) for x in vals[c]) for c in cols])
    why = ("the version's preview: columns" if picked else f"up to {SAMPLE_COLS} columns that differ across these rows")
    body = (f'<p class=mut>{len(s["rows"])} of {s["total"]:,} rows, drawn at random (the same {len(s["rows"])} on every load). '
            f'First {esc(why)}; dates to the day. Left out, as identifying or free text: '
            f'{esc(", ".join(s["hidden"])) or "none"}.</p>' + grid(first)
            + (_fold(f"the other {len(rest)} columns", "" if picked else "the same in these rows, or empty", grid(rest)) if rest else ""))
    return _fold("a few rows", f'{len(s["columns"])} columns shown', body)


def _partitions(b: dict, root: Path, href) -> str:
    proto = b["prototype"]
    if not proto["releases"]:
        return "<p class=mut>No release yet: the segments are defined in the Question Book's release.</p>"
    r = proto["releases"][-1]
    defs = [(f'<b>{esc(p.get("name", ""))}</b>', f'<code>{esc(_where(p))}</code>',
             esc(p.get("why", ""))) for p in r["partitions"]]
    power = (r["thresholds"].get("power") or {})
    names = [p.get("name") for p in r["partitions"] if p.get("name") != "cross"]
    counts = []
    for v in b["versions"]:
        cells = {}
        for j in (j for j in b["jobs"] if j["data"] == v.get("version")):
            for t in j["tasks"]:
                for run in t["hard"]:
                    cells.setdefault(run.get("partition"), run.get("n", "—"))
        counts.append([f'<b>{esc(v.get("version", ""))}</b>'] + [esc(cells.get(n, "—")) for n in names])
    return (f'<p class=mut>Defined in release {esc(r.get("label") or r["name"])} ({esc(rel(r["job"], root))}/partitions.md), part of the plan, '
            f'fixed before any outcome; a new or changed segment is a new release. Power floor: '
            f'{esc(power.get("smallest_effect_pp", "—"))} pp.</p>'
            + table(("partition", "where", "why"), defs)
            + '<p class=mut>Rows per data version (a row per version, a column per segment):</p>'
            + table(["version"] + names, counts))


def _questions(b: dict) -> dict:
    """Every question any release asks on a segment, by id, with the release that asks it last; the Executive ones
    are read in the Overall Report instead."""
    out = {}
    for r in b["prototype"]["releases"]:
        for qid, q in r["questions"].items():
            if qid[:1] != "X":
                out[qid] = dict(q, release=r["name"])
    return out


def newest_task(b: dict, qid: str) -> dict | None:
    """A question's Task in the newest Job that asks it: what the Board's counts read (one count, round 1)."""
    return next((t for j in reversed(b["jobs"]) for t in j["tasks"] if t["qid"] == qid), None)


def _cell(j: dict, qid: str, part: str) -> tuple:
    t = next((t for t in j["tasks"] if t["qid"] == qid), None)
    if not t:
        return None, None
    run = next((r for r in t["hard"] if r.get("partition") == part), None)
    return t, run


def _newest_word(b: dict, qid: str) -> str:
    """A question's mark on the Board, its newest Job's page in its tab's word (round 2: "rename each ✅/· to its
    tab's word"): page written, else page and its state (partial, returned, open), else not asked yet."""
    t = newest_task(b, qid)
    if not t:
        return "not asked yet"
    if is_written(t):
        return "page written"
    if any(_rtype(r) == "write" and str(r.get("status") or "").lower() in ("running", "started") for r in t.get("soft") or []):
        return "🏃"
    return page_word(t)


def _coverage(b: dict, root: Path, part: str, href, tabs: str = "", work: bool = False) -> str:
    """What each question found on one segment, Job by Job. With `tabs` (the focus page): side tabs, one per DIKW
    level with its state word, each question a two-part row (the question; what it found); with `work` (the focus
    page's Work) also its steps and its trail through the Jobs (round 2: "the path lines leave Report")."""
    rows, said_n, all_n = {}, {}, {}
    for qid, q in _questions(b).items():
        trail, n, last, said, has_runs, asked = [], 0, None, None, False, 0
        for j in b["jobs"]:
            t, run = _cell(j, qid, part)
            if not t:
                trail.append(f'<span title="{esc(j["name"])}">{esc(j["name"][:3])}</span> · not in its release')
                continue
            asked += 1
            state = run.get("status", "—") if run else t["face"].get("answer-status", "—")
            n += is_written(t)
            last = run or last
            has_runs = has_runs or bool(t["hard"])
            said = t if str(t["face"].get("answer") or "").strip() else said
            ran = (_run_link(run, root) if run
                   else "no run on this segment")
            trail.append(f'<span title="{esc(j["name"])} › {esc(t["name"])}">{esc(j["name"][:3])}</span> ▸ {ran} · '
                         f'{_st(state)} · page {esc(page_word(t))}')
        mark = MARK.get(str((last or {}).get("status")), "·")
        tally = ""                        # each Job's page says its own state in the trail
        if last is None and said:         # no Run on this segment: what it found where it is asked (a cross test), or
            cuts = ", ".join(dict.fromkeys(str(h.get("partition") or "") for h in said["hard"]))   # from the answers below
            found = (f'<p class=q-head>{esc(str(said["face"]["answer"]))}</p><p class=mut>'
                     + (f"asked on {esc(cuts)}" if cuts else "it cites the answers below it")
                     + f' · {_task_link(said, root)}</p>' + tally)
        elif not has_runs:
            found = '<p class=mut>It cites the answers below it; its page is still to write</p>' + tally
        else:
            found = _q_report(_spec(q).get("name") or qid, last, root, _label(part), tally)
        all_n[qid[:1]] = all_n.get(qid[:1], 0) + 1
        said_n[qid[:1]] = said_n.get(qid[:1], 0) + bool(newest_task(b, qid) and is_written(newest_task(b, qid)))
        if tabs:
            rows.setdefault(qid[:1], []).append(f'<div class="q-row q-two" id=question-{esc(qid)}><div class=q-l>'
                                                f'{_q_logic(qid, q, mark, root, _newest_word(b, qid))}</div><div class=q-r>{found}'
                                                + (_q_work(q, trail) if work else "") + '</div></div>')
        else:
            rows.setdefault(qid[:1], []).append(_qwr(_q_logic(qid, q, mark, root), _q_work(q, trail), found, f"question-{qid}"))
    last = b["prototype"]["releases"][-1] if b["prototype"]["releases"] else {}
    latest = last.get("job")
    if tabs:
        return _by_level(rows, "", links=_release_links(latest, root, last.get("label", "")), tabs=tabs,
                         words={lv: far(said_n.get(lv, 0), n, "written") for lv, n in all_n.items()})
    return _by_level(rows, _qwr_head("Task Work · each Job on this segment", "Report · what it found"),
                     links=_release_links(latest, root, last.get("label", "")))


def _tracks(b: dict, root: Path, part: str, href) -> str:
    rows = {}
    for qid, q in _questions(b).items():
        steps, verdicts = [], []
        for j in b["jobs"]:
            t, run = _cell(j, qid, part)
            if t:
                steps.append(f'{esc(j["name"][:3])} {_st(run.get("status") if run else t["face"].get("answer-status", "—"))}')
            v = (j["vs"].get("rows") or {}).get(qid)
            if v:
                verdicts.append(f'{esc(j["name"][:3])}: {_st(v["status"])}')
        logic = f'<p class=q-head><b>{esc(qid)}</b> {_open(q["file"], root, qid, q["question"] or "<question>")}</p>'
        rows.setdefault(qid[:1], []).append(_qwr(logic, " → ".join(steps) or "<span class=mut>—</span>",
                                                 " · ".join(verdicts) or "<span class=mut>no comparison yet</span>"))
    return ('<p class=mut>Each question Job by Job; along one release the data versions make a trend.</p>'
            + _by_level(rows, _qwr_head("Work · Job by Job", "Report · what each comparison found")))


def _consistency(b: dict, root: Path, part: str, href) -> str:
    rows = {}
    pairs = [j for j in b["jobs"] if j["vs"]]
    for qid, q in _questions(b).items():
        work, tally = [], {}
        for j in pairs:
            v = j["vs"]["rows"].get(qid)
            if not v:
                continue
            tally[v["status"]] = tally.get(v["status"], 0) + 1
            work.append(f'{esc(j["previous"][:3])} → {esc(j["name"][:3])} {_st(v["status"])} <span class=mut>{esc(v["why"])}</span>')
        logic = f'<p class=q-head><b>{esc(qid)}</b> {_open(q["file"], root, qid, q["question"] or "<question>")}</p>'
        rows.setdefault(qid[:1], []).append(_qwr(logic, "<br>".join(work) or "<span class=mut>—</span>",
                                                 " · ".join(esc(k) for k in tally) or "<span class=mut>—</span>"))
    return ('<p class=mut>Only Jobs one clock apart are compared, so each change has one cause. Each verdict is as the '
            "Job's run-compare wrote it (reports/vs-&lt;prev&gt;.md); the rule for 'held' is still open.</p>"
            + _by_level(rows, _qwr_head("Work · each step between Jobs", "Report · the verdicts")))


def _findings(b: dict, root: Path, part: str, href, tabs: str = "") -> str:
    runs = {r["run"]: r for r in b["runs"]}
    rows = {}
    for rp in b["reports"]:
        num = rp["slug"].split("_")[0]
        level = str(rp.get("level", ""))[:1].upper() or "D"
        run = runs.get(f"run-report-{num}")
        work = (f'{esc(run["run"])} {_st(run.get("status"))}' if run else '<span class=mut>no run yet</span>') \
            + '<p class=mut>reads: the Jobs\' answers</p>'
        logic = f'<p class=q-head><b>{esc(num.upper())}</b> {_open(rp["file"], root, num.upper(), P.front(rp["file"]).get("title") or rp["slug"])}</p>'
        report = f'{_st(rp.get("answer-status", "—"))} · {_open(rp["file"], root, rp["slug"], "the report")}'
        rows.setdefault(level, []).append(_qwr(logic, work, report))
    return (("" if tabs else "<p class=mut>The Block's own questions, a second D · I · K · W over the Jobs' answers; they "
             "live on the Board (board.md, reports/qNN_&lt;topic&gt;/).</p>")
            + _by_level(rows, _qwr_head("Work · the Board's soft run", "Report · what it says"), "No Block question yet.",
                        tabs=tabs, words={lv: "asked" for lv in rows}))


def _answered(j: dict) -> str:
    out = []
    for lv, _, _ in LEVELS:
        ts = [t for t in j["tasks"] if t["qid"][:1] == lv]
        if ts:
            done = sum(str(t["face"].get("answer-status") or "").lower() in WRITTEN for t in ts)
            out.append(f"{lv} {far(done, len(ts), 'written')}")
    return " · ".join(out)


def _jobs(b: dict, root: Path, href, only: str) -> str:
    rows = []
    for j in b["jobs"]:
        if only != "All" and j["release"] != only:
            continue
        rows.append((_job_link(href, j), esc(f'{_rlabel(b, j["release"])} × {_vlabel(b, j["data"])}'),
                     esc(j["moved"] or "—"), esc(_answered(j)), _st(j["state"])))
    out = [table(("Job", "pins", "the clock that moved", "pages written, by DIKW level", "state"), rows)]
    for j in (j for j in b["jobs"] if j["state"] != "closed" and (only == "All" or j["release"] == only)):
        groups = []                     # a closed fold per DIKW level, one short line per Task (a flat list of every Task was too long to use)
        for lv, name, _ in LEVELS:
            ts = [t for t in j["tasks"] if t["qid"][:1] == lv]
            if not ts:
                continue
            quick = []
            wrote = sum(str(t["face"].get("answer-status") or "").lower() in WRITTEN for t in ts)
            for t in ts:
                tally = {}
                for r in t["hard"]:
                    tally[str(r.get("status") or "—")] = tally.get(str(r.get("status") or "—"), 0) + 1
                cuts = ", ".join(str(r.get("partition")) for r in t["hard"])
                said = (" · ".join(esc(st) for st in tally) + f' <span class=mut title="{esc(cuts)}">by segment</span>'
                        ) if t["hard"] else (
                    "<span class=mut>not run</span>" if t["qid"][:1] in RUN_LEVELS else
                    "<span class=mut>cites the answers below it</span>")      # W and X have no Run of their own
                words = t["name"].split("_", 2)[-1].replace("-", " ")
                quick.append((f'<b>{esc(t["qid"])}</b>', f'<a href="{esc(href("", "", t["path"]))}">{esc(words)}</a>',
                              said, _st(t["face"].get("answer-status") or "—")))
            groups.append(f'<details class=topic><summary><b>{esc(name)} questions</b> '
                          f'<span class=topic-meta>{far(wrote, len(ts), "written")}</span></summary>'
                          f'<div style="padding:4px 14px 10px">{table(("#", "question", "runs", "page"), quick)}</div></details>')
        out.append(_fold(f'{j["name"]} · its Tasks', "", f'<div class=dikw>{"".join(groups)}</div>', opened=True))
    return "".join(out)


def _board_runs(b: dict, root: Path, view: str) -> str:
    out = []
    if view in ("All", "soft"):
        out.append(_fold("the Board's own · soft", "", _runs_table(b["runs"], root), opened=True))
    if view in ("All", "from below"):
        below = [(esc(j["name"]), esc(len(j["runs"])), esc(sum(len(t["hard"]) for t in j["tasks"])),
                  esc(sum(len(t["soft"]) for t in j["tasks"]))) for j in b["jobs"]]
        out.append(_fold("from below · each Job", f"{len(b['jobs'])} Jobs",
                         table(("Job", "its own soft", "its Tasks' hard", "its Tasks' soft"), below), opened=True))
    return "".join(out)


def _handoff(b: dict, root: Path) -> str:
    rows = [(_open(h["file"], root, h.get("counsel", h["file"].stem)), esc(h.get("job", "")), _st(h.get("signed", "—")))
            for h in b["handoffs"]]
    return ('<p class=mut>Only signed advice leaves this Board.</p>'
            + (table(("advice", "from Job", "signed"), rows) if rows else '<p class=mut>No signed advice yet.</p>'))
