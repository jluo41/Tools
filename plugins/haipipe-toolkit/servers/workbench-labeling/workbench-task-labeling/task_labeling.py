"""The labeling Task's screen: what a labeling Task shows in the frame's Spaces, by its type.

One Task type, one folder (b32 s41-D15, JL 261016: "go ahead with workbench-task-labeling"). Everything a
labeling Task shows lives in servers/workbench-labeling/workbench-task-labeling/: this layout, the engine's
Labeling workbench it opens (labeling.py: Data · Labeling · Quality · Delivery, and its write door) and that
workbench's look (assets/js/10-drawer/60-workbench-labeling.js). Its manual is the skill workbench-task-labeling.
The Block and Job levels stay in ../labeling_theme.py.

A labeling Task is one of five types, read from its face's `task-type:` line (labeling_theme.TYPES): items ·
ground truth · building · scanning · score; today's one labeling Page (`task-type: labeling`) is building and
scanning at once. The frame calls spaces() for a Task of the labeling theme only (frame.task_layouts).
"""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import parse_qs, quote, urlsplit

from live.frame import Space, esc, face, rel, table
from live import labeling_theme as T
from live.labeling_theme import (BUILD_WORK, BY_SUB, DELIVER, NOTES, SCAN_WORK, TYPES, VIEW, _block_of,
                                 _engine_job, _facts, _job_for, _open, _skill_run, _view_url, types_of)

try:
    import yaml
except Exception:                               # a Run's manifest then shows its headline only
    yaml = None

L = T.L                                         # the optional haipipe-labeling package (labeling.py)

# every `task-type:` line a labeling Task may carry, and "" for an older labeling Page that names none
TASK_TYPES = ("",) + tuple(dict.fromkeys(line for t in TYPES for line in t[3]))


def _yaml_file(path: Path) -> dict:
    if yaml is None or not path.is_file():
        return {}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def _item_runs(task: Path) -> list:
    """The Task's hard Runs, oldest first: (folder, its run.yaml), each a folder with its result/ (since 261010)."""
    runs = task / "runs"
    folders = sorted(p for p in runs.glob("r[0-9][0-9]_*/") if p.is_dir()) if runs.is_dir() else []
    return [(p, _yaml_file(p / "run.yaml")) for p in folders]


def _face_part(task: Path, name: str) -> str:
    """One `### N · <name> · …` part of the face's ## Content, as paragraphs and its sketch; "" when absent."""
    md = face(task)
    text = md.read_text(encoding="utf-8", errors="ignore") if md else ""
    m = re.search(rf"(?ms)^### \d+ · {re.escape(name)}\b[^\n]*\n(.*?)(?=^#{{2,4}} |\Z)", text)
    if not m:
        return ""
    out, body = [], re.sub(r"(?m)^\*\*Division map[^\n]*\n", "", m.group(1))
    for i, part in enumerate(re.split(r"(?ms)^```[^\n]*\n(.*?)^```[ \t]*$", body)):
        if i % 2:
            out.append(f'<pre class=space-source>{esc(part.rstrip())}</pre>')
        else:
            out += [f'<p>{_code(esc(" ".join(p.split())))}</p>' for p in re.split(r"\n\s*\n", part) if p.strip()]
    return "".join(out)


def _code(text: str) -> str:
    """The face's `inline code` as <code> (on text already escaped)."""
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", text)


def _value(v) -> str:
    if isinstance(v, dict):
        return " · ".join(f"{k} {_value(x)}" for k, x in v.items())
    if isinstance(v, (list, tuple)):
        return ", ".join(_value(x) for x in v)
    return f"{v:,}" if isinstance(v, int) and not isinstance(v, bool) else str(v)


def _embedding_state(job: dict | None, block: Path | None):
    """(the labeling job's lane, its embedding state or None, a summary in words); the lane may not exist yet."""
    if job is None or block is None or L is None:
        return None, None, '<span class=mut>no labeling job in this Job yet</span>'
    try:
        page = block / parse_qs(urlsplit(str(job.get("labeling_url") or "")).query)["file"][0]
        lane = L._job_root(page)[0]
        emb = L._embedding_state(lane) if lane.is_dir() else None
        return lane, emb, L._embedding_summary(emb)
    except Exception:                               # an unreadable lane: say not built, never break the frame
        return None, None, '<span class=mut>not built</span>'


# ── The items Task, as designed in b15 s41-task-items-procedure: three steps, each a tab named the same in Work and
# Report. Work: the step itself (what we have, read from disk; the recipe or build a person signs; the prompt, which
# takes the person's notes), folded to one line once done (s41-D15); then one card per topic, a list read down
# (s41-D09). Report: the cards only. The steps run through haipipe-labeling-preparation's engine, items_task.py
# (s41-D11); a person's Sign and Agree and a Draw again go through LabelingMixin's two narrow routes.
RESULTS = ("1 · Data", "2 · Items", "3 · Embedding")
OLD_RESULT = {"Itemization": RESULTS[0], "2 · Item": RESULTS[1], "3 · Item list": RESULTS[1],
              "4 · Embedding": RESULTS[2], "Embedding": RESULTS[2]}      # links made before s41 (261014)
LIST_ROWS = 20
SAMPLE_N = 5


def _engine():
    """haipipe-labeling-preparation's items_task.py, found from this file; None when the skill is absent."""
    import importlib.util
    for base in Path(__file__).resolve().parents:
        path = base / "skills" / "2_theme" / "labeling" / "engine" / "items_task.py"
        if path.is_file():
            spec = importlib.util.spec_from_file_location("labeling_items_task", path)
            mod = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(mod)
            except Exception:
                return None
            return mod
    return None


IT = _engine()


def _fit_table(head, rows, raw=None) -> str:
    """A table whose columns size to what they hold (JL 261014: "adjust the cell width smartly"): a short column (an id,
    a number) stays on one line; the text columns share the card's width by their median length, never under 180 px,
    so every column is seen at once (JL 261014: the judged column was pushed off the card); a long cell scrolls.
    `rows` hold html cells; `raw` the same cells as plain text, to measure (else the html is measured)."""
    import re as _re
    from statistics import median as _median_
    plain = raw or [[_re.sub(r"<[^>]+>", "", str(c)) for c in r] for r in rows]
    meds, long_ = [], []
    for j, h in enumerate(head):
        lens = [len(str(r[j])) for r in plain if j < len(r)] or [0]
        meds.append(None if max(lens) <= 40 else max(_median_(lens), 20))   # None: one line
        long_.append(max(lens) > 300)
    total = sum(m for m in meds if m) or 1
    cell = "padding:5px 8px;border-bottom:1px solid var(--line);vertical-align:top;text-align:left"
    size = ["white-space:nowrap;width:1%" if m is None else f"width:{max(12, round(90 * m / total))}%" for m in meds]
    th = "".join(f'<th style="{cell};background:var(--wash);white-space:nowrap;{w}">{esc(h)}</th>'
                 for h, w in zip(head, size))

    def box(c, m, lg):
        if m is None:
            return c
        return f'<div style="min-width:180px{";max-height:9em;overflow-y:auto" if lg else ""}">{c}</div>'
    body = "".join("<tr>" + "".join(f'<td style="{cell}{";white-space:nowrap" if m is None else ""}">{box(c, m, lg)}</td>'
                                    for c, m, lg in zip(r, meds, long_)) + "</tr>" for r in rows)
    return (f'<div style="overflow-x:auto;max-width:100%"><table style="border-collapse:collapse;width:100%;'
            f'font-size:13.5px"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>')


def _kv(rows) -> str:
    """A name/value table: the names in a shaded column that does not wrap, the values beside them, bordered and
    close (JL 261014: "make the table's name column to be filled with color ... more comfortable")."""
    cell = "padding:5px 10px;border:1px solid var(--line);vertical-align:top"
    body = "".join(f'<tr><th style="{cell};background:var(--wash);font-weight:600;text-align:left;white-space:nowrap;'
                   f'width:1%">{k}</th><td style="{cell};overflow-wrap:anywhere">{v}</td></tr>' for k, v in rows)
    return f'<table style="border-collapse:collapse;width:100%;margin:6px 0 10px;font-size:14px"><tbody>{body}</tbody></table>'


def _json(path: Path):
    import json
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None
    except ValueError:
        return None


def _items_file(f: dict, root: Path) -> Path | None:
    store = f["metrics"].get("store") or f["manifest"].get("store")
    items = root / str(store) / "items.jsonl" if store else None
    return items if items and items.is_file() else None


def _item_rows(items: Path) -> list:
    """Every item as (id, words in its main text, turns before it, words after it, the item itself). The real text
    is shown (JL 261014: "here we want to put the real items to look, the real things"; b15 s41-D07)."""
    import json
    rows = []
    with open(items, encoding="utf-8") as handle:
        for line in handle:
            try:
                r = json.loads(line)
            except ValueError:
                continue
            if isinstance(r, dict):
                rows.append((str(r.get("item_id") or ""), len(str(r.get("main") or "").split()),
                             sum(1 for x in str(r.get("context_before") or "").splitlines() if x.strip()),
                             len(str(r.get("context_after") or "").split()), r))
    return rows


def _median(values: list) -> str:
    from statistics import median
    return f"{median(values):g}" if values else "—"


def _spread(values: list) -> str:
    return f"{_median(values)} median · {min(values)} to {max(values)}" if values else "—"


def _op(task: Path, run: Path) -> str:
    return IT.operation_of(task, run) if IT else ("embed" if "embedding-build" in
                                                   (_yaml_file(run / "run.yaml").get("type") or []) else "items")


def _status(run: Path) -> str:
    return str(_yaml_file(run / "result" / "runtime.yaml").get("status") or _yaml_file(run / "run.yaml").get("status")
               or "planned")


def _runs_of(task: Path, op: str) -> list:
    return [r for r, _ in _item_runs(task) if _op(task, r) == op]


def _done(task: Path, op: str) -> Path | None:
    done = [r for r in _runs_of(task, op) if _status(r) == "complete"]
    if op == "items":
        done = [r for r in done if (r / "result" / "manifest.yaml").is_file()]
    return done[-1] if done else None


def _open_run(task: Path, op: str) -> Path | None:
    """The newest Run of a step not yet complete (planned, signed, or failed): the one a person works on now."""
    runs = _runs_of(task, op)
    if runs and _status(runs[-1]) != "complete":
        last_done = _done(task, op)
        if last_done is None or runs[-1].name > last_done.name:
            return runs[-1]
    return None


def _signs(run: Path) -> dict | None:
    s = _yaml_file(run / "run.yaml").get("signs")
    return s if isinstance(s, dict) and s.get("by") else None


def _config(task: Path, run: Path) -> dict:
    inside = run / "config.yaml"
    return _yaml_file(inside if inside.is_file() else task / "scripts" / "config" / f"{run.name}.yaml")


def _items_facts(task: Path, root: Path) -> dict:
    """What an items Task's files say: its items Runs, the newest complete one, its manifest and metrics, its scripts."""
    runs = _item_runs(task)
    run = _done(task, "items")
    result = run / "result" if run else None
    metrics = (L._read_json(result / "metrics.json") if L is not None else _json(result / "metrics.json") or {}) \
        if result else {}
    summary = metrics.get("summary") if isinstance(metrics.get("summary"), dict) else {}
    scripts = sorted((task / "scripts").glob("*.py")) if (task / "scripts").is_dir() else []
    return {"runs": runs, "done": [run] if run else [], "run": run, "card": _yaml_file(run / "run.yaml") if run else {},
            "manifest": _yaml_file(result / "manifest.yaml") if result else {}, "metrics": metrics,
            "headline": str(summary.get("headline") or ""), "scripts": scripts,
            "config": task / "scripts" / "config" / f"{run.name}.yaml" if run else None}


def _raw_card(task: Path) -> tuple:
    """(the newest finished Run whose Result holds the Data cards, its description.json), or (None, None)."""
    for run, _ in reversed(_item_runs(task)):
        d = run / "result" / "description.json"
        if d.is_file() and _status(run) == "complete":
            card = _json(d)
            if isinstance(card, dict):
                return run, card
    return None, None


def _cell(v) -> str:
    return "<br>".join(esc(x) for x in str(v).split("\n"))


def _stats(pairs, line: str = "") -> str:
    """The numbers, smaller than the base scoreboard: they sit inside a card (JL 261014: "these are too large")."""
    cells = "".join(f'<div><b style="font-size:20px">{esc(v)}</b><span>{esc(k)}</span></div>' for v, k in pairs)
    return (f'<div class=stat-row style="gap:6px 28px">{cells}</div>'
            + (f'<p class=stat-line style="font-size:13.5px;color:var(--mut)">{esc(line)}</p>' if line else ""))


def _short(text: str, n: int = 100) -> str:
    """A card's summary line: one short line; the whole text stays inside the card."""
    text = " ".join(str(text).split())
    return text if len(text) <= n else text[:n].rsplit(" ", 1)[0].rstrip(",;·(") + " …"


def _fold(title: str, meta: str, body: str, open_: bool = False) -> str:
    """A card: its title only, folded until opened (JL 261014: "could you remove them? and make them to be hidden
    by default"); `meta` and `open_` are kept for callers and no longer drawn."""
    # an open card keeps to two thirds of the screen, a scrollbar on its right (JL 261014: "could I make a
    # scrollbar in the right?"), so a long card never pushes the rest of the page away
    return (f'<details class="topic work-task"><summary><span class=related-head><b>{esc(title)}</b></span>'
            f'</summary><div class=work-body style="max-height:85vh;overflow-y:auto">{body}</div></details>')


def _row_table(groups: list, row: dict) -> str:
    """One made-up row (synth_df) as one table (JL 261014: "we can make this to the table"): the group shaded at
    the left, spanning its columns, then each column and its value; a group's meaning is the group's hover text."""
    cell = "padding:4px 10px;border:1px solid var(--line);vertical-align:top"
    body = ""
    for grp in groups:
        cols = [c["name"] for c in grp.get("columns") or []]
        for i, c in enumerate(cols):
            head = (f'<th rowspan={len(cols)} title="{esc(grp.get("meaning") or "")}" style="{cell};background:var(--wash);'
                    f'font-weight:600;text-align:left;white-space:nowrap;width:1%">{esc(grp["name"])}</th>' if i == 0 else "")
            body += (f'<tr>{head}<td style="{cell};white-space:nowrap;width:1%"><code>{esc(c)}</code></td>'
                     f'<td style="{cell};overflow-wrap:anywhere">{_cell(row.get(c, ""))}</td></tr>')
    return f'<table style="border-collapse:collapse;width:100%;margin:6px 0 10px;font-size:14px"><tbody>{body}</tbody></table>'


RAW_ROWS = 10


def _raw_rows(root: Path, file: str) -> tuple:
    """(the header, the first RAW_ROWS rows) of the raw csv, as they are (JL 261014: "for the data I want to see the
    raw data ... to present the raw data as it is if we want"); ((), []) when it is not a readable csv."""
    import csv
    path = root / file
    if not file.endswith(".csv") or not path.is_file():
        return (), []
    with open(path, encoding="utf-8", errors="replace", newline="") as handle:
        reader = csv.reader(handle)
        head = next(reader, [])
        rows = [r for _, r in zip(range(RAW_ROWS), reader)]
    return tuple(head), rows


def _not_yet(what: str) -> str:
    return f"<p class=space-empty>{esc(what)}</p>"


def _bars(values: dict) -> str:
    """Counts as bars, largest first: a label's values (s41 🏷 Current labels)."""
    total = sum(values.values()) or 1
    cell = "padding:3px 8px;border-bottom:1px solid var(--line);vertical-align:middle"
    rows = "".join(f'<tr><td style="{cell};width:42%;overflow-wrap:anywhere">{esc(k)}</td>'
                   f'<td style="{cell};width:48%"><span style="display:inline-block;height:9px;'
                   f'width:{100 * v / total:.1f}%;background:var(--tab-on);border-radius:2px"></span></td>'
                   f'<td style="{cell};width:10%;text-align:right">{v:,}</td></tr>' for k, v in values.items())
    return (f'<table style="table-layout:fixed;width:100%;border-collapse:collapse;font-size:13.5px;margin:2px 0 10px">'
            f'<tbody>{rows}</tbody></table>')


def _histogram(h: dict, what: str) -> str:
    """A histogram as an svg: bars by bin, the bin edges under them (s41 📈 Statistics)."""
    counts, edges = h.get("counts") or [], h.get("edges") or []
    if not counts:
        return ""
    w, hh, pad = 460, 150, 26
    bw = (w - 2 * pad) / len(counts)
    top = max(counts) or 1
    bars = "".join(f'<rect x="{pad + i * bw + 1:.1f}" y="{hh - pad - (c / top) * (hh - 2 * pad):.1f}" '
                   f'width="{bw - 2:.1f}" height="{(c / top) * (hh - 2 * pad):.1f}" fill="#4e79a7">'
                   f'<title>{edges[i]}–{edges[i + 1] - 1}: {c}</title></rect>' for i, c in enumerate(counts))
    ticks = "".join(f'<text x="{pad + i * bw:.1f}" y="{hh - 8}" font-size="10" fill="#6f6f6b">{e}</text>'
                    for i, e in enumerate(edges[:-1]) if i % max(1, len(counts) // 5) == 0)
    return (f'<figure style="margin:6px 0"><svg viewBox="0 0 {w} {hh}" width="100%" style="max-width:{w}px" role="img" '
            f'aria-label="{esc(what)}">{bars}{ticks}</svg><figcaption class=mut>{esc(what)}</figcaption></figure>')


def _sample_url(task: Path, root: Path, kind: str) -> str:
    return f"/_board/labeling/sample?task={quote(rel(task, root))}&kind={kind}"


def _draw_again(task: Path, root: Path, kind: str, target: str) -> str:
    return (f'<button type=button class=work-act data-fetch="{esc(_sample_url(task, root, kind))}" '
            f'data-target="{target}">Draw again</button>')


def _sample_fold(head: str, body: str) -> str:
    """One drawn row or item, folded (JL 261014: "could I collapse this?"): its name only, no grey preview (JL 261014:
    "No need to have this small words, remove all of them"); opened, the whole chat and its labels."""
    return (f'<details class="topic work-task"><summary><span class=related-head><b>{esc(head)}</b></span></summary>'
            f'<div class=work-body>{body}</div></details>')


def sample_html(task: Path, root: Path, kind: str, seed: int, n: int = SAMPLE_N) -> str:
    """Random rows of the raw data, or random items, as a table: Draw again reads them live, writes nothing
    (s41-D12). The raw rows show the unit, the text and the answers; every other column stays in the raw file."""
    if IT is None:
        return _not_yet("The preparation engine is not installed.")
    try:
        s = IT.sample(task, kind, seed, n, root=root)
    except (SystemExit, Exception) as e:              # an unreadable file: say so, never break the frame
        return _not_yet(f"Could not draw: {e}")
    rows = s.get("rows") or []
    if not rows:
        return _not_yet("Nothing to draw yet.")
    if kind == "items":                         # one card per item: before, the judged text marked, after
        strip = lambda label, text, key=False: (
            f'<div style="margin:6px 0;padding:6px 10px;border-radius:8px;{"background:var(--tab-wash)" if key else ""}">'
            f'<span class=mut><code>{label}</code></span><br>{_cell(text)}</div>')
        cards = "".join(_sample_fold(
            str(r.get("item_id")),
            (strip("context_before", r["context_before"]) if r.get("context_before") else "")
            + strip("main · judged", r.get("main", ""), True)
            + (strip("context_after", r["context_after"]) if r.get("context_after") else "")) for r in rows)
        return cards
    else:                                       # one card per row: the chat full width, the answers on one line
        _, card = _raw_card(task)
        card = card or {}
        unit = (card.get("grain") or {}).get("unit")
        texts = sorted((card.get("text_to_label") or {}).get("columns") or [],
                       key=lambda t: -(t.get("lines_median") or 1))          # the turns before, then the reply
        labels = card.get("labels") or []
        expert = [lb["column"] for lb in labels if lb.get("who") == "expert"]
        rater = [lb["column"] for lb in labels if lb.get("who") != "expert"]
        main_rater = [k for k in rater if re.search(r"overall|verdict", k, re.I)][:1]

        def grid(names, r):                       # a label per cell: its name small and grey, its value bold
            cells = "".join(f'<div style="padding:4px 8px;border:1px solid var(--line);border-radius:6px">'
                            f'<div class=mut style="font-size:11.5px;overflow-wrap:anywhere">{esc(k.replace("_", " "))}'
                            f'</div><b style="overflow-wrap:anywhere">{_cell(r.get(k, "")) or "—"}</b></div>' for k in names)
            return (f'<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:6px;'
                    f'margin:4px 0 8px">{cells}</div>')
        cards = []
        for r in rows:
            head = f"row {r.get('row')}" + (f" · {unit} {r.get(unit)}" if unit else "")
            chat = "".join(
                f'<div style="margin:6px 0;padding:6px 10px;border-radius:8px;'
                f'{"background:var(--tab-wash)" if i == len(texts) - 1 else ""}">'
                f'<span class=mut><code>{esc(t["column"])}</code></span><br>{_cell(r.get(t["column"], ""))}</div>'
                for i, t in enumerate(texts))
            rest = [k for k in rater if k not in main_rater]
            labs = ((f'<p class=mut style="margin:6px 0 0">experts</p>' + grid(expert, r) if expert else "")
                    + (f'<p class=mut style="margin:6px 0 0">this rater</p>' + grid(main_rater, r)
                       if main_rater else "")
                    + (f'<details><summary class=mut>{len(rest)} more</summary>'
                       + grid(rest, r) + "</details>" if rest else ""))
            cards.append(_sample_fold(head, chat + labs))
        body = "".join(cards) or table(("row",), [(esc(r.get("row")),) for r in rows])
        return body
    return f"<div class=dl-src>{body}</div>"


# ── step 1 · Data: the Data cards ──────────────────────────────────────────────────────────────────
def _data_cards(task: Path, root: Path, job, block) -> str:
    run, card = _raw_card(task)
    if not card:
        return _not_yet("Step 1 fills this.")
    t, g = card.get("table") or {}, card.get("grain") or {}
    proof = g.get("proof") or {}
    out = []
    seed = (card.get("samples") or {}).get("seed", 7)
    out.append(_fold("🎲 Random samples", f"{SAMPLE_N} real rows, seed {seed}, kept in {run.name}'s result; Draw again "
                     "reads others live and writes nothing",
                     f'<p>{_draw_again(task, root, "raw", "sample-raw")}</p>'
                     f'<div id=sample-raw>{sample_html(task, root, "raw", int(seed))}</div>', open_=True))
    bg = card.get("background") or {}
    if bg:
        out.append(_fold("📖 Background", " · ".join(re.split(r"\s*[(;]", str(bg.get(k)))[0] for k in ("who", "license")
                                                     if bg.get(k)),
                         _kv([(esc(k), _code(esc(str(v)))) for k, v in bg.items()])))
    units = [(f"{v:,}", k[len("distinct_"):].removesuffix("_id") + "s") for k, v in proof.items()
             if k.startswith("distinct_") and v != t.get("rows")]
    size = t.get("bytes")
    raw = _raw_rows(root, str(t.get("file") or ""))
    basic = (_stats([(f'{t.get("rows", 0):,}', "rows"), (str(t.get("columns", "—")), "columns"), *units],
)
             + _kv([("one row", esc(g.get("one_row_is") or "—")), ("the file", f'<code>{esc(t.get("file"))}</code>'),
                                ("size", esc(f"{size / 1e6:.1f} MB" if size else "—")),
                                ("read by", f"<code>{esc(run.name)}</code>")]
                     + [(esc(k.replace("_", " ")), esc(f"{v:,}" if isinstance(v, int) else str(v))) for k, v in proof.items()])
             + (_fold("Raw rows", f'the first {len(raw[1])} of {t.get("rows", 0):,}; real values, '
                      "the labels included",
                      _fit_table(raw[0], [[_cell(v) for v in r] for r in raw[1]], raw[1]))
                if raw[1] else ""))
    out.append(_fold("📊 Basic description", f'{t.get("rows", 0):,} rows · {t.get("columns", "—")} columns'
                     + "".join(f" · {v} {k}" for v, k in units), basic, open_=True))
    groups = card.get("groups") or []
    rows = (card.get("synth_df") or {}).get("rows") or []
    if rows:
        out.append(_fold("🧩 One row (made up)", "", _row_table(groups, rows[0])))
    labels = card.get("labels") or []
    if labels:
        who = {}
        for lb in labels:
            who[lb.get("who") or "?"] = who.get(lb.get("who") or "?", 0) + 1
        out.append(_fold("🏷 Current labels", f"{len(labels)} answer columns: "
                         + " · ".join(f"{n} {w}" for w, n in who.items()),
                         "".join(f"<h4 style=\"margin:12px 0 2px;font-size:14px\"><code>{esc(lb['column'])}</code> "
                                 f"· {esc(lb.get('who'))}</h4>{_bars(lb.get('values') or {})}"
                                 for lb in labels)))
    text = (card.get("text_to_label") or {}).get("columns") or []
    if text:
        out.append(_fold("💬 Text to label", " · ".join(f"{x['column']}: {x.get('words_median')} words"
                                                           for x in text),
                         table(("column", "values", "words: median · min · max", "lines, median"),
                               [(f"<code>{esc(x['column'])}</code>", esc(f"{x.get('values', 0):,}"),
                                 esc(f"{x.get('words_median')} · {x.get('words_min')} · {x.get('words_max')}"),
                                 esc(x.get("lines_median"))) for x in text])))
    columns = "".join(f"<h4 title=\"{esc(grp.get('meaning') or '')}\">{esc(grp['name'])}</h4>" + table(
        ("column", "filled", "distinct", "typical values"),
        [(f"<code>{esc(c['name'])}</code>", esc(f"{c.get('filled', 0):.0%}"), esc(f"{c.get('distinct', 0):,}"),
          esc(c.get("typical") or "")) for c in grp.get("columns") or []]) for grp in groups)
    gotchas = card.get("gotchas") or []
    out.append(_fold("⚠️ Watch out", f"{proof.get('exact_duplicate_rows', 0)} duplicate rows · {len(gotchas)} "
                     f"{'thing' if len(gotchas) == 1 else 'things'} to watch", ("<ul>" + "".join(f"<li>{esc(x)}</li>" for x in gotchas) + "</ul>" if gotchas else "")
                     + _fold(f'{t.get("columns", "")} columns', f"{len(groups)} groups", columns)))
    return "".join(out)


# ── step 2 · Items: the items' cards ───────────────────────────────────────────────────────────────
def _items_cards(task: Path, root: Path, job, block) -> str:
    f = _items_facts(task, root)
    if not f["done"]:
        return _not_yet("Step 2 fills this, after Sign.")
    m, items = f["manifest"], _items_file(f, root)
    every = _item_rows(items) if items else []
    res = f["run"] / "result"
    stats, check = _json(res / "stats.json") or {}, _json(res / "check.json")
    out = [_fold("🎲 Random items", f"{SAMPLE_N} items, each drawn before │ judged │ after; Draw again reads others live",
                 f'<p>{_draw_again(task, root, "items", "sample-items")}</p>'
                 f'<div id=sample-items>{sample_html(task, root, "items", 7)}</div>', open_=True)]
    n_items = m.get("items", len(every))
    pairs = [(f"{n_items:,}" if isinstance(n_items, int) else str(n_items), "items")]
    if every:
        pairs += [(_median([r[1] for r in every]), "words judged, median"),
                  (_median([r[2] for r in every]), "turns before, median")]
    if job and job.get("n_sealed") not in (None, "—"):
        pairs.append((str(job["n_sealed"]), "held back"))
    head = ("item", "context before", "main (judged)", "words", "turns")
    rowfmt = lambda r: (f"<code>{esc(r[0])}</code>", _cell(r[4].get('context_before', '')),
                        _cell(r[4].get("main", "")), esc(r[1]), esc(r[2]))
    listing = (_fold(f"All {len(every)} items", "as they are", _fit_table(head, [rowfmt(r) for r in every]))
               if every else "")
    out.append(_fold("📊 Items", " · ".join(f"{v} {k}" for v, k in pairs),
                     _stats(pairs) + _kv([("One item", esc(str(m.get("item") or "—")))]) + listing, open_=True))
    if stats or every:
        wj = stats.get("words_judged") or {}
        tb = stats.get("turns_before") or {}
        if not wj and every and IT:
            w, t = [r[1] for r in every], [r[2] for r in every]
            wj = {"min": min(w), "median": _median(w), "max": max(w), "histogram": IT.histogram(w)}
            tb = {"min": min(t), "median": _median(t), "max": max(t), "histogram": IT.histogram(t)}
        body = (_histogram(wj.get("histogram") or {}, f"words judged: {wj.get('min')} · {wj.get('median')} · "
                                                        f"{wj.get('max')} (min · median · max)")
                + _histogram(tb.get("histogram") or {}, f"turns before: {tb.get('min')} · {tb.get('median')} · "
                                                          f"{tb.get('max')}")
                + (_kv([("shortest", " · ".join(f"<code>{esc(i)}</code>" for i in stats.get("shortest") or [])),
                                    ("longest", " · ".join(f"<code>{esc(i)}</code>" for i in stats.get("longest") or []))])
                   if stats.get("shortest") else ""))
        out.append(_fold("📈 Statistics", "words judged and turns before, as histograms; the shortest and longest", body))
    if every:
        first = every[0][4]
        out.append(_fold("🧩 One item", f"{every[0][0]}: before │ judged │ after", (
            "<div class=card-row>"
            f"<div><h4>before</h4>{_cell(first.get('context_before', ''))}</div>"
            f"<div class=key><h4>judged</h4>"
            f"{_cell(first.get('main', ''))}</div>"
            f"<div><h4>after</h4>"
            f"{_cell(first.get('context_after') or '') or '<span class=mut>none</span>'}</div></div>")))
    if check:
        names = (("ids_unique", "ids unique"), ("one_item_per_unit", "one item per unit"),
                 ("nothing_judged_empty", "nothing judged empty"), ("no_key_inside", "no label inside"))
        out.append(_fold("✅ Check", "passed" if check.get("passed") else "FAILED",
                         table(("check", ""), [(esc(w), '<span class="st st-ok">✓</span>' if check.get(k)
                                               else '<span class="st st-warn">✗</span>') for k, w in names])))
    store = root / str(f["metrics"].get("store") or m.get("store") or "")
    kept = [(f"<code>{esc(p.name)}</code>", esc(f"{sum(1 for _ in open(p, encoding='utf-8')):,} rows"))
            for p in (store / "items.ground-truth.jsonl", store / "items.raters.jsonl") if p.is_file()]
    if kept or m.get("kept_out"):
        out.append(_fold("🏷 Labels kept out", "",
                         table(("file", ""), kept)))
    older = [r.name for r in _runs_of(task, "items") if r != f["run"]]
    version = _kv([("store", f'<code>{esc(f["metrics"].get("store") or m.get("store") or "—")}</code>'),
                               ("made by", f'<code>{esc(f["run"].name)}</code>' + (f' · {esc(f["headline"])}'
                                                                                 if f["headline"] else "")),
                               ("revises", esc(m.get("revise_of") or "—")), ("what changed", esc(m.get("changed") or "—")),
                               ("the notes it was given", _cell(m.get("notes") or "—"))]
                    + [(esc(k), esc(_value(v))) for k, v in m.items()
                       if k not in {"source", "transform", "item", "items", "store", "kept_out", "revise_of", "changed",
                                    "notes"}])
    out.append(_fold("📦 Version", f'{Path(str(f["metrics"].get("store") or m.get("store") or "")).name or "—"}'
                     + (f" · earlier: {', '.join(older)}" if older else ""), version))
    return "".join(out)


# ── step 3 · Embedding: the map, then its cards ────────────────────────────────────────────────────
PALETTE = ("#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f", "#edc948", "#b07aa1", "#ff9da7", "#9c755f", "#bab0ac")


def _embed_runs(task: Path) -> list:
    """The items Task's own embedding Runs, oldest first: (folder, card, complete?)."""
    return [(r, _yaml_file(r / "run.yaml"), _status(r) == "complete" and (r / "result" / "map.json").is_file())
            for r in _runs_of(task, "embed")]


_MAP3D: dict = {}


def _map3d(res: Path, man: dict, root: Path) -> list:
    """The 3-D places: the Run's map3d.json; a Run made before it existed gets them from its vectors, worked out
    here and kept in memory, never written into its result (AGENTS.md rule 0)."""
    got = _json(res / "map3d.json")
    if got:
        return got
    vec = root / str(man.get("vectors") or "")
    if not man.get("vectors") or not vec.is_file():
        return []
    key = (str(vec), vec.stat().st_mtime)
    if key not in _MAP3D:
        try:
            import sys
            import numpy as np
            sys.path.insert(0, str(Path(IT.__file__).parent))
            from embedding_build import _map_3d
            ids = [p["item_id"] for p in _json(res / "map.json") or []]
            xyz = _map_3d(np.load(vec).astype("float32"), int(man.get("seed") or 0), str(man.get("map") or "tsne"))
            _MAP3D[key] = [{"item_id": i, "x": x, "y": y, "z": z} for i, (x, y, z) in zip(ids, xyz)]
        except Exception:                                            # no numpy or sklearn here: the 2-D map only
            _MAP3D[key] = []
    return _MAP3D[key]


def _item_texts(root: Path, man: dict) -> dict:
    """item id → (the turns before, the judged text), from the items the build embedded."""
    import json
    path = root / str(man.get("items_store") or "") / "items.jsonl"
    out = {}
    if man.get("items_store") and path.is_file():
        for line in open(path, encoding="utf-8"):
            try:
                r = json.loads(line)
            except ValueError:
                continue
            out[str(r.get("item_id"))] = (str(r.get("context_before") or ""), str(r.get("main") or ""))
    return out


MAP_JS = r"""<style>.imap button.on{background:var(--tab-wash);border-color:var(--tab-on);color:var(--tab-on)}</style><script>(function(){document.querySelectorAll('.imap:not([data-on])').forEach(function(w){w.dataset.on=1;
var D=JSON.parse(w.querySelector('.imap-data').textContent),svg=w.querySelector('svg'),g=svg.querySelector('g'),cv=w.querySelector('canvas'),
pick=w.querySelector('.imap-pick'),vb=svg.viewBox.baseVal,view={x:0,y:0,k:1},cam={yaw:.6,pitch:.35,zoom:1},focus=null,sel=null,spin=false,dots=[].slice.call(svg.querySelectorAll('circle'));
function esc(t){return String(t).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
var tip=w.querySelector('.imap-tip');function showTip(id,x,y){var t=D.items[id]||['',''];tip.innerHTML='<b>'+esc(id)+'</b> · G'+(D.group[id]+1)+(t[0]?'<div style="white-space:pre-wrap;margin-top:4px;padding-left:8px;border-left:3px solid var(--line)">'+esc(t[0])+'</div>':'')+'<div style="white-space:pre-wrap;margin-top:6px;padding:4px 8px;border-radius:6px;background:var(--tab-wash)">'+esc(t[1])+'</div>';tip.hidden=false;var r=tip.getBoundingClientRect();tip.style.left=Math.max(8,Math.min(x+14,innerWidth-r.width-8))+'px';tip.style.top=Math.max(8,(y+14+r.height>innerHeight?y-14-r.height:y+14))+'px';}function hideTip(){tip.hidden=true;}function three(){return cv&&!cv.hidden;}
function apply(){g.setAttribute('transform','translate('+view.x+' '+view.y+') scale('+view.k+')');var r=(5/Math.sqrt(view.k)).toFixed(2);
 dots.forEach(function(c){c.setAttribute('r',c.dataset.item===sel?r*1.8:r);c.style.opacity=(focus!==null&&c.dataset.group!==focus)?.12:.9;
 c.setAttribute('stroke',c.dataset.item===sel?'#000':'none');});draw();}
function choose(id){sel=id;var t=D.items[id]||['',''],gr=D.group[id];
 pick.innerHTML='<p><b>'+esc(id)+'</b> · G'+(gr+1)+'</p>'+(t[0]?'<div style="white-space:pre-wrap;max-height:12em;overflow-y:auto;padding:6px 10px;border-left:3px solid var(--line)">'+esc(t[0])+'</div>':'')
  +'<div style="white-space:pre-wrap;padding:6px 10px;margin-top:6px;border-radius:8px;background:var(--tab-wash)">'+esc(t[1])+'</div>';pick.hidden=false;apply();}
function zoomAt(px,py,f){var k=Math.min(16,Math.max(1,view.k*f));view.x=px-(px-view.x)*(k/view.k);view.y=py-(py-view.y)*(k/view.k);view.k=k;if(k===1){view.x=0;view.y=0;}apply();}
var drag=null;svg.addEventListener('pointerdown',function(e){drag={x:e.clientX,y:e.clientY,vx:view.x,vy:view.y,m:false};});
svg.addEventListener('pointermove',function(e){if(!drag)return;var dx=e.clientX-drag.x,dy=e.clientY-drag.y;if(!drag.m&&Math.abs(dx)+Math.abs(dy)<5)return;drag.m=true;
 var b=svg.getBoundingClientRect();view.x=drag.vx+dx*vb.width/b.width;view.y=drag.vy+dy*vb.height/b.height;apply();});
svg.addEventListener('pointerup',function(e){var m=drag&&drag.m;drag=null;if(!m&&e.target.dataset&&e.target.dataset.item)choose(e.target.dataset.item);});
svg.addEventListener('pointerleave',function(){drag=null;hideTip();});svg.addEventListener('mouseover',function(e){if(!drag&&e.target.dataset&&e.target.dataset.item)showTip(e.target.dataset.item,e.clientX,e.clientY);});svg.addEventListener('mouseout',function(e){if(e.target.dataset&&e.target.dataset.item)hideTip();});
svg.addEventListener('wheel',function(e){if(!e.ctrlKey&&!e.metaKey)return;e.preventDefault();var b=svg.getBoundingClientRect();
 zoomAt((e.clientX-b.left)*vb.width/b.width,(e.clientY-b.top)*vb.height/b.height,e.deltaY<0?1.15:1/1.15);},{passive:false});
function size(){var w=cv.clientWidth||800,d=devicePixelRatio||1;cv.width=w*d;cv.height=w*.55*d;cv.style.height=(w*.55)+'px';}
function proj(x,y,z){var cy=Math.cos(cam.yaw),sy=Math.sin(cam.yaw),cp=Math.cos(cam.pitch),sp=Math.sin(cam.pitch),x1=x*cy-z*sy,z1=x*sy+z*cy,y1=y*cp-z1*sp,z2=y*sp+z1*cp,f=3.2/(3.2-z2*.9),s=Math.min(cv.width,cv.height)*.4*cam.zoom;
 return{x:cv.width/2+x1*f*s,y:cv.height/2-y1*f*s,z:z2,f:f};}
function draw(){if(!cv||!three())return;var c=cv.getContext('2d'),d=devicePixelRatio||1;c.clearRect(0,0,cv.width,cv.height);c.strokeStyle='#adb5bd';c.fillStyle='#495057';c.lineWidth=1.2*d;c.font=(13*d)+'px sans-serif';[[1,0,0],[0,1,0],[0,0,1]].forEach(function(a,i){var p1=proj(-a[0],-a[1],-a[2]),p2=proj(a[0],a[1],a[2]);c.beginPath();c.moveTo(p1.x,p1.y);c.lineTo(p2.x,p2.y);c.stroke();c.fillText(D.axis+' '+(i+1),p2.x+4*d,p2.y-4*d);});
 var q=D.p3.map(function(p){var o=proj(p[1],p[2],p[3]);o.id=p[0];o.g=D.group[p[0]];return o;}).sort(function(a,b){return a.z-b.z;});
 q.forEach(function(o){o.r=Math.max(2,4.5*o.f*Math.sqrt(cam.zoom))*d;c.globalAlpha=(focus!==null&&String(o.g)!==focus)?.1:(.5+.5*(o.z+1)/2);
  c.fillStyle=D.colors[o.g%D.colors.length];c.beginPath();c.arc(o.x,o.y,o.r,0,6.2832);c.fill();if(o.id===sel){c.globalAlpha=1;c.lineWidth=3*d;c.strokeStyle='#000';c.stroke();}});
 c.globalAlpha=1;cv.__q=q;}
function loop(){if(!spin||!three())return;cam.yaw+=.006;draw();requestAnimationFrame(loop);}
function near(e){var b=cv.getBoundingClientRect(),d=devicePixelRatio||1,mx=(e.clientX-b.left)*d,my=(e.clientY-b.top)*d,best=null,bd=1e9;(cv.__q||[]).forEach(function(p){var dd=Math.hypot(p.x-mx,p.y-my);if(dd<Math.max(p.r+4*d,10*d)&&dd<=bd){best=p;bd=dd;}});return best;}
var d3=null;if(cv){cv.addEventListener('pointerdown',function(e){d3={x:e.clientX,y:e.clientY,m:false};});
 cv.addEventListener('pointermove',function(e){if(!d3){var h=near(e);if(h)showTip(h.id,e.clientX,e.clientY);else hideTip();cv.style.cursor=h?'pointer':'grab';return;}hideTip();var dx=e.clientX-d3.x,dy=e.clientY-d3.y;if(!d3.m&&Math.abs(dx)+Math.abs(dy)<4)return;d3.m=true;
  cam.yaw+=dx*.01;cam.pitch=Math.max(-1.45,Math.min(1.45,cam.pitch+dy*.01));d3.x=e.clientX;d3.y=e.clientY;draw();});
 cv.addEventListener('pointerup',function(e){var o=d3;d3=null;if(!o||o.m)return;var best=near(e);if(best)choose(best.id);});
 cv.addEventListener('pointerleave',function(){d3=null;hideTip();});
 cv.addEventListener('wheel',function(e){if(!e.ctrlKey&&!e.metaKey)return;e.preventDefault();cam.zoom=Math.max(.5,Math.min(6,cam.zoom*(e.deltaY<0?1.12:1/1.12)));draw();},{passive:false});}
w.querySelectorAll('[data-dim]').forEach(function(b){b.onclick=function(){var t=b.dataset.dim==='3';w.querySelectorAll('[data-dim]').forEach(function(x){x.classList.toggle('on',x===b);});
 svg.style.display=t?'none':'';cv.hidden=!t;w.querySelector('[data-spin]').hidden=!t;if(t){size();draw();}else{spin=false;}};});
var sp=w.querySelector('[data-spin]');if(sp)sp.onclick=function(){spin=!spin;sp.classList.toggle('on',spin);if(spin)requestAnimationFrame(loop);};
w.querySelectorAll('[data-zoom]').forEach(function(b){b.onclick=function(){var z=b.dataset.zoom;
 if(three()){if(z==='reset')cam={yaw:.6,pitch:.35,zoom:1};else cam.zoom=Math.max(.5,Math.min(6,cam.zoom*(z==='in'?1.3:1/1.3)));draw();return;}
 if(z==='reset'){view={x:0,y:0,k:1};apply();}else zoomAt(vb.width/2,vb.height/2,z==='in'?1.5:1/1.5);};});
w.querySelectorAll('[data-g]').forEach(function(b){b.onclick=function(){focus=focus===b.dataset.g?null:b.dataset.g;
 w.querySelectorAll('[data-g]').forEach(function(x){x.classList.toggle('on',x.dataset.g===focus);});apply();};});
});})();</script>"""


def _map_card(points: list, p3: list, groups: list, texts: dict, method: str = "tsne") -> str:
    """The items on an interactive map (JL 261014: "one for 2-D and one for 3-D ... the interactive one"; the
    labeling job's old map): 2-D drags and zooms, 3-D turns and spins; a group's button lights it; a dot clicked
    shows its item."""
    import json
    if not points:
        return ""
    xs, ys = [p["x"] for p in points], [p["y"] for p in points]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    w, h, pad = 1000, 560, 32
    sx = lambda v: pad + (v - x0) / ((x1 - x0) or 1) * (w - 2 * pad)
    sy = lambda v: pad + (v - y0) / ((y1 - y0) or 1) * (h - 2 * pad)
    dots = "".join(f'<circle cx="{sx(p["x"]):.1f}" cy="{sy(p["y"]):.1f}" r="5" fill="{PALETTE[p["group"] % 10]}" '
                   f'data-item="{esc(p["item_id"])}" data-group="{p["group"]}" style="cursor:pointer"></circle>' for p in points)
    axis = {"tsne": "t-SNE", "pca": "PC", "umap": "UMAP"}.get(method.lower(), method.upper())
    axes = (f'<path d="M{pad} {pad} V{h - pad} H{w - pad}" fill="none" stroke="#adb5bd" stroke-width="1.2"/>'
            f'<text x="{w - pad}" y="{h - 4}" text-anchor="end" font-size="13" fill="#495057">{esc(axis)} 1 →</text>'
            f'<text x="{pad + 4}" y="{pad - 4}" font-size="13" fill="#495057">↑ {esc(axis)} 2</text>')
    data = {"axis": axis, "colors": PALETTE, "group": {str(p["item_id"]): p["group"] for p in points},
            "p3": [[str(r["item_id"]), r["x"], r["y"], r["z"]] for r in p3],
            "items": {k: [v[0], v[1]] for k, v in texts.items()}}
    blob = json.dumps(data).replace("</", "<\\/")
    btn = lambda attr, word, on=False: (f'<button type=button class="work-act{" on" if on else ""}" {attr}>{word}</button>')
    legend = "".join(btn(f'data-g="{g["group"]}"', f'<svg width="10" height="10"><circle cx="5" cy="5" r="5" '
                         f'fill="{PALETTE[g["group"] % 10]}"/></svg> G{g["group"] + 1} {esc(g.get("size", ""))}')
                     for g in groups)
    bar = (((btn("data-dim=2", "2-D", True) + btn("data-dim=3", "3-D") + btn("data-spin hidden", "Spin")) if p3 else "")
           + btn("data-zoom=in", "+") + btn("data-zoom=out", "−") + btn("data-zoom=reset", "Reset"))
    return (f'<div class=imap><p style="display:flex;gap:6px;flex-wrap:wrap">{bar}</p>'
            f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px;touch-action:none;cursor:grab;'
            f'border:1px solid var(--line);border-radius:8px" role="img" aria-label="the items on the map">{axes}<g>{dots}</g></svg>'
            + (f'<canvas hidden style="display:block;width:100%;max-width:{w}px;border:1px solid var(--line);'
               f'border-radius:8px;touch-action:none;cursor:grab"></canvas>' if p3 else "")
            + f'<p style="display:flex;gap:6px;flex-wrap:wrap">{legend}</p><div class=imap-pick hidden></div><div class=imap-tip hidden style="position:fixed;z-index:50;'
            f'max-width:560px;max-height:90vh;overflow:hidden;padding:6px 10px;background:var(--bg);border:1px solid var(--line);border-radius:8px;'
            f'box-shadow:0 2px 8px rgba(0,0,0,.15);font-size:13px;pointer-events:none"></div>'
            f'<script type=application/json class=imap-data>{blob}</script></div>'
            + MAP_JS)


def _text_cell(texts: dict, i: str) -> str:
    """An item's id over its judged text, for a table."""
    return f"<code>{esc(i)}</code><br>{_cell((texts.get(str(i)) or ('', ''))[1])}"


def _embedding_cards(task: Path, root: Path, job, block) -> str:
    built = [r for r in _embed_runs(task) if r[2]]
    if not built:
        lane, emb, summary = _embedding_state(job, block)
        builds = (emb or {}).get("builds") or [] if isinstance(emb, dict) else []
        if builds:                                     # an older build on the labeling job's lane
            src = _view_url(job, VIEW["embedding"])
            return (_fold("📍 Map", "built on the labeling job's lane",
                          f'<iframe class=page-view src="{esc(src)}" loading=lazy title="Embedding"></iframe>'
                          f'<p class=mut>{_open(src, "open it on its own ↗")}</p>', open_=True))
        return _not_yet("Step 3 fills this, after Agree.")
    run, card, _ = built[-1]
    res = run / "result"
    points = _json(res / "map.json") or []
    groups = _json(res / "groups.json") or []
    dups = _json(res / "duplicates.json") or []
    far = _json(res / "outliers.json") or []
    man = _yaml_file(res / "manifest.yaml")
    dot = lambda g: (f'<svg width="12" height="12" aria-hidden="true"><circle cx="6" cy="6" r="5" '
                     f'fill="{PALETTE[g % 10]}"/></svg>')
    model = str(man.get("model", "")).split("/")[-1]
    texts = _item_texts(root, man)
    out = [_fold("📍 Map", "", _map_card(points, _map3d(res, man, root), groups, texts, str(man.get("map") or "tsne"))),
           _fold("🧩 Groups", "",
                 table(("group", "items", "top words", "typical items"),
                       [(f"{dot(g['group'])} G{g['group'] + 1}", esc(g.get("size", "")),
                         esc(" · ".join(g.get("keywords") or [])),
                         " · ".join(f"<code>{esc(i)}</code>" for i in g.get("typical") or [])) for g in groups])),
           _fold("📏 Near-duplicates", "",
                 _fit_table(("item", "item", "cosine"), [(_text_cell(texts, d["a"]), _text_cell(texts, d["b"]),
                                                          esc(d["cosine"])) for d in dups]) if dups else
                 "<p>none</p>"),
           _fold("🧭 Outliers", "",
                 _fit_table(("item", "group", "closeness"),
                            [(_text_cell(texts, o["item_id"]), f"G{o['group'] + 1}", esc(o["to_its_group"]))
                             for o in far]) if far else "<p>none</p>")]
    rows = [("model", esc(man.get("model", "—"))), ("vector size", esc(man.get("dim", "—"))),
            ("input", esc(man.get("input", "—"))), ("map", esc(str(man.get("map", "—")).upper())),
            ("seed", esc(man.get("seed", "—"))), ("items", f'<code>{esc(man.get("items_store", "—"))}</code>'),
            ("vectors", f'<code>{esc(man.get("vectors", "—"))}</code>'), ("Run", f"<code>{esc(run.name)}</code>")]
    others = built[:-1]
    out.append(_fold("⚙️ Builds", f"{model} · {run.name}" + (f" · {len(others)} more" if others else "")
                     + "; another model is another Run, side by side",
                     _kv(rows + ([("earlier", esc(" · ".join(r[0].name for r in others)))] if others else []))
                     ))
    return "".join(out)


# ── the steps: state from disk, what we have, the proposal to sign, the prompt that takes notes ───────
ITEM_STEPS = (
    ("raw", "📥 Step 1 · Data", "describe", _data_cards),
    ("make", "🧱 Step 2 · Items", "items", _items_cards),
    ("embed", "🗺 Step 3 · Embedding", "embed", _embedding_cards),
)
SKILL = "haipipe-labeling-preparation"


def _step_states(task: Path, root: Path, job: dict | None, block: Path | None) -> dict:
    lane, emb, _ = _embedding_state(job, block)
    builds = (emb or {}).get("builds") or [] if isinstance(emb, dict) else []
    done = {"raw": _raw_card(task)[1] is not None,                  # each step done by its own Run only
            "make": bool(_items_facts(task, root)["done"]),
            "embed": bool(builds) or any(r[2] for r in _embed_runs(task))}
    states, nexted = {}, False
    for key, _, op, _ in ITEM_STEPS:                                 # the first step not done is next
        states[key] = "done" if done[key] else ("next" if not nexted else "todo")
        nexted = nexted or not done[key]
        if states[key] == "todo" and key == "embed" and done["make"]:
            states[key] = "next"                                       # items made before Data cards existed
        if states[key] != "todo":
            open_ = _open_run(task, op)
            if open_ is not None and op in ("items", "embed"):
                states[key] = "ready" if _signs(open_) else "sign"       # a proposal waits for the person
    return states


def _prompt(key: str, state: str, task: Path, root: Path, again: bool = False) -> str:
    t = rel(task, root)
    op = {"raw": "describe", "make": "items", "embed": "embed"}[key]
    open_ = _open_run(task, op)
    if again:
        f = _items_facts(task, root)
        version = Path(str(f["metrics"].get("store") or f["manifest"].get("store") or "the items")).name
        return f"/{SKILL} {t} revise: read my notes on {version}, plan the revised recipe, and stop for my Sign."
    if key == "raw":
        return f"/{SKILL} {t} describe: plan and run the describe Run, then fill the Data cards. No items."
    if state in ("sign", "ready") and open_ is not None:
        word = "Sign" if op == "items" else "Agree"
        return (f"/{SKILL} {t} {op}: " + (f"I {word} {open_.name} on the screen first; then " if state == "sign" else "")
                + f"run {open_.name} and settle it.")
    if key == "make":
        return f"/{SKILL} {t} items: plan the items Run from the Data cards, and stop for my Sign."
    return f"/{SKILL} {t} embed: plan the embedding Run, and stop for my Agree."


def _what_we_have(key: str, task: Path, root: Path, job) -> str:
    if key == "raw":
        data = IT.job_data(task, root) if IT else {"dataset": "", "data": ""}
        files = IT.data_files(root, data["data"]) if IT and data["data"] else []
        rows = [("Dataset", esc(data["dataset"] or "—")),
                ("Folder", f'<code>{esc(data["data"])}</code>' if data["data"] else
                 '<span class=mut>no <code>data:</code> line in the Job</span>'),
                ("Files", " · ".join(f"<code>{esc(p.name)}</code> {p.stat().st_size / 1e6:.1f} MB" for p in files)
                 or '<span class="st st-warn">not found</span>')]
        return _kv(rows)
    if key == "make":
        run, card = _raw_card(task)
        if not card:
            return _not_yet("Step 1 first.")
        t, proof = card.get("table") or {}, (card.get("grain") or {}).get("proof") or {}
        unit = (card.get("grain") or {}).get("unit")
        return _kv([("Data", f"the Data cards, from <code>{esc(run.name)}</code>"),
                                ("Rows", esc(f'{t.get("rows", 0):,} rows' + (f' · {proof.get("distinct_" + unit, 0):,} '
                                                                            f'{unit}' if unit else ""))),
                                ("Kept out", esc(" · ".join(lb["column"] for lb in card.get("labels") or []) or "—"))])
    f = _items_facts(task, root)
    if not f["done"]:
        return _not_yet("Step 2 first.")
    return _kv([("Items", f'<code>{esc(f["metrics"].get("store") or f["manifest"].get("store"))}</code> · '
                                      f'{esc(f["manifest"].get("items", "—"))} items, from <code>{esc(f["run"].name)}</code>'),
                            ("Text", esc(str(f["manifest"].get("item") or "—")))])


def _sign_box(task: Path, root: Path, run: Path, word: str) -> str:
    s = _signs(run)
    if s:
        return f'<p><span class="st st-ok">✓ {esc(word)}</span> by {esc(s["by"])} · {esc(s.get("at", ""))}</p>'
    body = esc('{"action": "sign", "task": "%s", "run": "%s"}' % (rel(task, root), run.name))
    return (f'<p class=sign-row><input name=by class=sign-by placeholder="your name" size=18> '
            f'<button type=button class=work-act data-post="/_board/labeling/items" data-body="{body}" '
            f'data-fields="by">{"Agree" if word == "agreed" else "Sign"}</button></p>')


def _proposal(key: str, task: Path, root: Path) -> str:
    """The recipe (Step 2) or the build (Step 3) the agent proposed, for a person to sign or agree."""
    op = {"make": "items", "embed": "embed"}.get(key)
    run = _open_run(task, op) if op else None
    if run is None:
        return _as_signed(key, task, root)
    c = _config(task, run)
    if op == "items":
        r = c.get("recipe") or {}
        cb = r.get("context_before") or {}
        rows = [("One item", esc(f"one {r.get('unit')}") + f" · id <code>{esc(r.get('item_id'))}</code>"),
                ("Judged", f"<code>{esc(r.get('main'))}</code>"),
                ("Before", (f"<code>{esc(cb.get('column'))}</code>" + (" · turns: " + esc(", ".join(
                    f"{k} → {v}" for k, v in (cb.get("turns") or {}).items())) if cb.get("turns") else ""))
                 if cb else "none"),
                ("After", f"<code>{esc((r.get('context_after') or {}).get('column'))}</code>"
                 if r.get("context_after") else "none"),
                ("Kept out", esc(f"{len(r.get('keep_out') or [])} columns: " + ", ".join((r.get("keep_out") or [])[:6])
                                 + (f" and {len(r['keep_out']) - 6} more" if len(r.get("keep_out") or []) > 6 else ""))),
                ("Group", esc(f"the {r.get('group')}, never split" if r.get("group") else "—")),
                ("Writes", f"<code>{esc(c.get('out'))}</code>")]
        if c.get("revise_of"):
            rows.insert(0, ("Revises", f"<code>{esc(c['revise_of'])}</code>"))
            ch = str(c.get("changed") or "")
            rows.append(("Changed", '<span class="st st-warn">not typed yet</span>' if not ch or ch.startswith("<typed")
                         else esc(ch)))
        title, word = f"Recipe · {run.name}", "signed"
    else:
        rows = [("Model", esc(c.get("model"))), ("Embeds", esc("the judged text alone" if c.get("input") == "main"
                                                             else "the judged text with its turns before")),
                ("Map", esc(str(c.get("map") or "").upper())), ("Groups", esc(c.get("groups") or "chosen by fit")),
                ("Items", f"<code>{esc(c.get('items'))}</code>")]
        title, word = f"Build · {run.name}", "agreed"
    if c.get("notes"):
        rows.append(("Your notes", _cell(c["notes"])))
    failed = _status(run) == "failed"
    return (f'<div class="topic work-task"><div class=work-body><h4>{esc(title)}</h4>'
            + _kv(rows) + _sign_box(task, root, run, word)
            + (f'<p class="st st-warn">✗ failed: <code>{esc(rel(run / "result" / "runtime.yaml", root))}'
               '</code></p>' if failed else "") + "</div></div>")


def _as_signed(key: str, task: Path, root: Path) -> str:
    """A done step's recipe or build, as the person signed it; an older Run's from the face's Method part."""
    if key == "make":
        f = _items_facts(task, root)
        if not f["run"]:
            return ""
        c = _config(task, f["run"])
        s = _signs(f["run"])
        r = c.get("recipe")
        rows = ([("One item", esc(f"one {r.get('unit')}") + f" · id <code>{esc(r.get('item_id'))}</code>"),
                 ("Judged", f"<code>{esc(r.get('main'))}</code>"),
                 ("Before", f"<code>{esc((r.get('context_before') or {}).get('column'))}</code>"
                  if r.get("context_before") else "none"),
                 ("Kept out", esc(f"{len(r.get('keep_out') or [])} columns"))] if isinstance(r, dict)
                else [("one item", esc(f["manifest"].get("item") or "—"))])
        rows += [("script", " · ".join(f'<code>{esc(x.relative_to(task).as_posix())}</code>' for x in f["scripts"]))
                 ] if f["scripts"] else []
        rows += [("signed", esc(f"{s['by']} · {s.get('at', '')}") if s else '—'),
                 ("its settings", f'<code>{esc(rel(f["config"], root))}</code>' if f["config"] and f["config"].is_file()
                  else "—")]
        return (f'<h4>Recipe, signed · {esc(f["run"].name)}</h4>' + _kv(rows)
                + _face_part(task, "Method"))
    if key == "embed":
        built = [r for r in _embed_runs(task) if r[2]]
        if not built:
            return ""
        run = built[-1][0]
        c, s = _config(task, run), _signs(run)
        return (f'<h4>Build, agreed · {esc(run.name)}</h4>' + _kv([
            ("model", esc(c.get("model") or _yaml_file(run / "result" / "manifest.yaml").get("model") or "—")),
            ("agreed", esc(f"{s['by']} · {s.get('at', '')}") if s else '<span class=mut>—</span>')]))
    return ""


def _prompt_box(prompt: str, task: Path, root: Path, key: str, open_: bool = True) -> str:
    """The prompt, yours to add to (s41-D14): what you type under it is its `user feedback:` line, copied with it
    (JL 261014: "It will be our part of the prompt"); a pasted image is kept in the Task's notes/, its path written in."""
    k = f"{rel(task, root)}#{key}"
    return (f'<details class=run-prompt-box{" open" if open_ else ""}><summary>Prompt '
            f'<button type=button class="run-copy work-act" data-copy="{esc(prompt)}">Copy prompt</button></summary>'
            f'<pre class=run-prompt style="margin-bottom:0;border-bottom-left-radius:0;border-bottom-right-radius:0">'
            f'{esc(prompt)}</pre>'
            '<label style="display:block;margin:0;padding:4px 10px 0;background:var(--wash)">'
            '<code>user feedback:</code></label>'
            f'<textarea class=run-notes rows=3 data-key="notes:{esc(k)}" data-folder="{esc(rel(task, root))}" '
            'data-upload="/_board/labeling/notes" '
            'placeholder="notes, a row, an image" '
            'style="width:100%;box-sizing:border-box;margin:0;border:1px solid var(--line);border-top:0;'
            'background:var(--wash);font:13px/1.45 ui-monospace,Menlo,monospace;padding:6px 10px"></textarea></details>')


CHIPS = {"done": '<span class="st st-ok">✓ done</span>', "next": '<span class="st st-warn">→ next</span>',
         "sign": '<span class="st st-warn">✍ sign</span>',
         "ready": '<span class="st st-warn">→ run</span>', "todo": '<span class=st>· later</span>'}


def _step_box(i: int, task: Path, root: Path, job, state: str) -> str:
    key, title, op, _ = ITEM_STEPS[i]
    body = ("<h4>Input</h4>" + _what_we_have(key, task, root, job) + _proposal(key, task, root)
            + _prompt_box(_prompt(key, state, task, root), task, root, key, open_=state != "done"))
    return (f'<details class="topic work-task items-step"{"" if state == "done" else " open"}><summary>'
            f'<span class=related-head><b>{esc(title)}</b> {CHIPS[state]}</span></summary><div class=work-body>{body}</div></details>')


def _again_box(task: Path, root: Path) -> str:
    """Step 2 again (s41-D14): the items as they are, and the revise prompt that takes the person's notes."""
    f = _items_facts(task, root)
    version = Path(str(f["metrics"].get("store") or f["manifest"].get("store") or "")).name
    body = (_kv([("Items", esc(f"{version} · {f['manifest'].get('items', '—')} items")),
                             ("Recipe", esc(str(f["manifest"].get("item") or "—")))])
            + _prompt_box(_prompt("make", "done", task, root, again=True), task, root, "again"))
    return (f'<details class="topic work-task items-step"><summary><span class=related-head><b>🧱 Revise the items</b>'
            f'</span></summary><div class=work-body>{body}</div></details>')


def _items_spaces(folder: Path, root: Path, sub: str) -> dict:
    from live.frame import href
    job, block = _engine_job(folder, root), _block_of(folder)
    r_sub = OLD_RESULT.get(sub, sub)
    r_sub = r_sub if r_sub in RESULTS else RESULTS[0]
    i = RESULTS.index(r_sub)
    states = _step_states(folder, root, job, block)
    key = ITEM_STEPS[i][0]
    state = states[key]
    cards = (_not_yet("The steps before first.") if state == "todo"
             else ITEM_STEPS[i][3](folder, root, job, block))
    again = _again_box(folder, root) if key == "make" and state in ("done",) else ""
    after = (f'<p><a class=chip href="{esc(href(folder, root, T.THEME, "Work Details", RESULTS[i + 1]))}">next: '
             f'{esc(ITEM_STEPS[i + 1][1])} →</a></p>' if i + 1 < len(ITEM_STEPS) else
             '')
    steps = tuple({"label": f"run-{op}-<task>", "doing": title.split(" · ", 1)[-1],
                   "prompt": _prompt(k, states[k], folder, root), "skills": [SKILL]} for k, title, op, _ in ITEM_STEPS)
    # page=True: these views are the whole row; the base's Draft, Evidence and Value views stay off (an items Task
    # has no Draft plan; JL 261014: "we don't need draft")
    # two parts (JL 261014): Operation, what a person does (the step, its prompt; the revise box), then Result,
    # what the step made (the cards)
    part = lambda name: f'<h3 style="margin:18px 0 6px">{name}</h3>'
    operation = part("Operation") + _step_box(i, folder, root, job, state) + again
    result = part("Result") + cards
    return {"Audience Report": Space(html=result, subspaces=RESULTS, open=r_sub, page=True,
                                     note="Results only."),
            "Work Details": Space(html=operation + result + after,
                                  subspaces=RESULTS, open=r_sub, run_types=steps, page=True),
            "Description": Space(note=NOTES["items"])}


# ── Task: building, its four Stages (b15 s42: the map ①, the screens ②–⑪) ─────────────────────────
# A Stage is a tab in Work and Report, as an items Task's steps are (s41): Operation, what a person does (the
# Stage, its Input, the prompt), then Result, what the Stage made (one card per topic, folded). Sizes are named
# by symbol until the engine writes them (n m u r b, s42-D41); each agent step shows its reading budget (👁, s42-D43).
BUILD_TABS = ("1 · Contract", "2 · Initial Labeling Definition", "3 · Rounds", "4 · Handoff")
BUILD_SKILL = "haipipe-labeling-building"


def _items_task(task: Path) -> Path | None:
    """The items Task of the same Job: the building Task's corpus."""
    return next((t for t in sorted(task.parent.iterdir()) if t.is_dir() and t != task and types_of(t) == ("items",)), None)


def _build_states(job: dict | None) -> dict:
    """Each Stage done, next, waiting on a person, or later; read from the labeling job's own record."""
    job = job or {}
    phase = str(job.get("phase") or "")[:2]
    done = {"contract": job.get("kind") not in (None, "empty", "preparing", "repair") and job.get("n_sealed") is not None,
            "definition": bool(job.get("g0")),
            "rounds": phase in ("P2", "P3", "P4", "P5"),
            "handoff": phase in ("P3", "P4", "P5")}
    states, nexted = {}, False
    for key in ("contract", "definition", "rounds", "handoff"):
        states[key] = "done" if done[key] else ("next" if not nexted else "todo")
        nexted = nexted or not done[key]
    if states["definition"] == "next" and job.get("badge") == "Confirm meaning":
        states["definition"] = "sign"                                  # a draft waits for Sign (G0)
    if states["rounds"] == "next" and job.get("kind") == "labeling":
        states["rounds"] = "ready"                                     # a round is open: rule its picks
    return states


def _n(v, sym: str) -> str:
    return f"{sym} = {v}" if isinstance(v, int) else sym


def _build_input(key: str, task: Path, root: Path, job: dict | None) -> str:
    job = job or {}
    n_dev, m = job.get("n_dev"), job.get("n_sealed")
    n = n_dev + m if isinstance(n_dev, int) and isinstance(m, int) else None
    if key == "contract":
        it = _items_task(task)
        f = _items_facts(it, root) if it else {"done": []}
        items = (f'<code>{esc(f["metrics"].get("store") or f["manifest"].get("store"))}</code> · '
                 f'{esc(_n(f["manifest"].get("items"), "n"))} items' if f["done"] else
                 '<span class="st st-warn">the items Task first</span>')
        return _kv([("Items", "X · " + items), ("Groups", "C · from the items Task's 📍 map"),
                    ("Final exam", esc(f"S · {_n(m, 'm')} sealed, across C, never shown")),
                    ("Agent reads", "👁 0: ids and counts")])
    if key == "definition":
        return _kv([("Pool", esc(f"X∖S · {_n(n_dev, 'n − m')} items")), ("You read", "≤ r in all passes"),
                    ("Agent reads", "👁 ≤ c_ask a pass"), ("Rounds", "never draw what you read again")])
    if key == "rounds":
        t = job.get("rounds") or 0
        return _kv([("Corpus", esc(f"U · {_n(n_dev, 'u')}: 2 labels each · gold {job.get('labeled', 0)}")),
                    ("Pools", "H · L · N · HL · LN · HN · HLN"),
                    ("Guideline", esc(f"G_{t + 1}" if t else "G_1")),
                    ("Pick", "seed → retrieve over X∖S → score v(x) → read ≤ c_pick → b"),
                    ("Agent reads", "👁 ≤ c_pick to pick · ≤ c_learn to learn")])
    return _kv([("Checkpoint", esc(f"round {job.get('rounds') or 't'}, Stop signed")),
                ("Guideline", "G* = the last G_t"), ("Gold", esc(f"D* · {job.get('labeled', 0)} rulings")),
                ("Final exam", esc(f"S · {_n(m, 'm')}, still unseen")), ("Agent reads", "👁 0")])


BUILD_STAGES = (
    ("contract", "📦 Stage 1 · Contract",
     "contract: import the items, hold back the sealed set, start guideline v0."),
    ("definition", "💬 Stage 2 · Initial Labeling Definition",
     "definition: one more pass with me through the items, group by group; keep my notes; then draft the "
     "definition and stop for my Sign."),
    ("rounds", "🔁 Stage 3 · Rounds",
     "round: label U with G_t, sort it into the 7 pools, pick round t by the funnel, and stop for my Approve."),
    ("handoff", "✍️ Stage 4 · Handoff",
     "freeze: freeze the Handoff from the last checkpoint, and stop for my Sign (G*)."),
)
BUILD_CARDS = {
    "contract": ("📚 Corpus: 🔒 S · pool X∖S", "📜 Guideline G_0", "🗂 Register: 7 pools"),
    "definition": ("💬 The talk, pass by pass", "📝 Your notes and hard cases", "📜 Guideline G_1"),
    "rounds": ("📊 The 7 pools, round by round", "🏷 Your gold", "📜 Guideline G_t", "🤝 Both labelers vs you",
               "🗂 Register: open · covered · risky"),
    "handoff": ("✍️ Handoff", "📜 Guideline G*", "🏷 Your gold, D*", "🔍 Next: scanning"),
}


def _build_cards(key: str, state: str, job: dict | None) -> str:
    """A Stage's Result: one folded card per topic; the job's record where it says something, else not yet."""
    if state != "done" and not (key == "rounds" and (job or {}).get("rounds")):
        return _not_yet("Not made yet.")
    facts = _facts(job) if job else ""
    return "".join(_fold(t, "", facts if i == 0 else _not_yet("Read in the Labeling workbench.")
                         + (f'<p>{_open(_view_url(job, VIEW[{"contract": "contract", "definition": "definition", "rounds": "rounds", "handoff": "handoff"}[key]]))}</p>'
                            if job else ""))
                   for i, t in enumerate(BUILD_CARDS[key]))


def _build_spaces(folder: Path, root: Path, sub: str, job: dict | None) -> tuple:
    """(Work Details html, Report html, open tab, run types) for a building Task's four Stages."""
    states = _build_states(job)
    tab = sub if sub in BUILD_TABS else next((BUILD_TABS[i] for i, (k, _, _) in enumerate(BUILD_STAGES)
                                              if states[k] != "done"), BUILD_TABS[-1])
    i = BUILD_TABS.index(tab)
    key, title, words = BUILD_STAGES[i]
    state = states[key]
    t = rel(folder, root)
    prompt = f"/{BUILD_SKILL} {t} {words}"
    sign = ""
    if job and state in ("sign", "ready"):                             # the person's Sign and rulings: the engine's door
        sign = f'<p>{_open(_view_url(job, VIEW[{"definition": "definition", "rounds": "rounds"}[key]]), "✍ open it in the Labeling workbench ↗")}</p>'
    body = ("<h4>Input</h4>" + _build_input(key, folder, root, job) + sign
            + _prompt_box(prompt, folder, root, key, open_=state != "done"))
    step = (f'<details class="topic work-task items-step"{"" if state == "done" else " open"}><summary>'
            f'<span class=related-head><b>{esc(title)}</b> {CHIPS[state]}</span></summary>'
            f'<div class=work-body>{body}</div></details>')
    part = lambda name: f'<h3 style="margin:18px 0 6px">{name}</h3>'
    cards = _not_yet("The Stages before first.") if state == "todo" else _build_cards(key, state, job)
    runs = tuple({"label": f"run-{k}-<task>", "doing": tt.split(" · ", 1)[-1],
                  "prompt": f"/{BUILD_SKILL} {t} {w}", "skills": [BUILD_SKILL]} for k, tt, w in BUILD_STAGES)
    return part("Operation") + step + part("Result") + cards, part("Result") + cards, tab, runs


# ── Task: building, scanning, or today's one Page that is both ──────────────────────────────────
def _task_spaces(folder: Path, root: Path, sub: str) -> dict:
    types = types_of(folder)
    md, block = face(folder), _block_of(folder)
    if not md or not block:
        return {}
    if types == ("items",):
        return _items_spaces(folder, root, sub)
    if types and not {"building", "scanning"} & set(types):
        return {name: Space(note=NOTES[types[0]]) for name in ("Description", "Work Details")}
    job = _engine_job(folder, root) if types else _job_for(md, block, root)
    if job is None:
        return {}                                   # not a labeling job's Page: vanilla
    build, scan = "building" in types or not types, "scanning" in types or not types
    work = tuple(VIEW[v] for v in (BUILD_WORK if build else ()) + (SCAN_WORK if scan else ()))
    deliver = tuple(v for v, on in zip(DELIVER, (build, scan)) if on)
    described = VIEW["contract"] if build else VIEW["handoff"]
    out = {}
    d_names = ("Scope", described[2])
    d_sub = sub if sub in d_names else "Scope"
    out["Description"] = Space(
        html="" if d_sub == "Scope" else (_facts(job) + f'<p>{_open(_view_url(job, described))}</p>'),
        subspaces=d_names, open=d_sub, run_types=(_skill_run(described),) if d_sub != "Scope" else ())
    scan_names = tuple(VIEW[v][2] for v in SCAN_WORK) if scan else ()
    if build and sub not in scan_names:                                 # the four Stages (s42), then scanning's views
        html, report, tab, runs = _build_spaces(folder, root, sub, job)
        out["Work Details"] = Space(html=html, subspaces=BUILD_TABS + scan_names, open=tab, run_types=runs, page=True)
        out["Audience Report"] = Space(html=report, subspaces=BUILD_TABS, open=tab, page=True, note="Results only.")
    else:
        names = (BUILD_TABS if build else ()) + tuple(v[2] for v in work if v[1] in SCAN_WORK)
        w = BY_SUB[sub] if sub in scan_names else VIEW[SCAN_WORK[0]]
        out["Work Details"] = Space(
            html=(f'<p class=mut>{esc(w[3])}.</p>{_facts(job)}<p>{_open(_view_url(job, w))}</p>'),
            subspaces=names, open=w[2], run_types=(_skill_run(w),))
    dnames = ("Files",) + tuple(v[2] for v in deliver)
    if sub in dnames[1:]:
        dv = BY_SUB[sub]
        out["Delivery"] = Space(html=f'<p class=mut>{esc(dv[3])}.</p>{_facts(job)}<p>{_open(_view_url(job, dv))}</p>',
                                subspaces=dnames, open=sub, run_types=(_skill_run(dv),))
    else:
        out["Delivery"] = Space(subspaces=dnames, open="Files")    # Files: the vanilla delivery/ list
    return out


def spaces(folder: Path, root: Path, sub: str = "") -> dict:
    """{Space: Space} for a labeling Task; {} (vanilla) without the labeling package or for a Task that is no
    labeling job's."""
    if T.L is None:
        return {}
    return _task_spaces(Path(folder).resolve(), Path(root).resolve(), sub)
