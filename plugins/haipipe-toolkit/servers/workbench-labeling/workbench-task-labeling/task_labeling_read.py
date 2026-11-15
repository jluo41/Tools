"""Read an items Task from disk for its screen: its Runs and their state, the raw rows, the item rows, and the
sample a person draws."""
from __future__ import annotations

import traceback
import re
from pathlib import Path
from urllib.parse import parse_qs, quote, urlsplit
from live.frame import esc, face, rel, table
from live import labeling_theme as T
from live.labeling_theme import TYPES
try:
    import yaml
except ImportError:                               # a Run's manifest then shows its headline only
    yaml = None
L = T.L                                         # the optional haipipe-labeling package (labeling.py)

# every `task-type:` line a labeling Task may carry, and "" for an older labeling Page that names none
TASK_TYPES = ("",) + tuple(dict.fromkeys(line for t in TYPES for line in t[3]))


def _yaml_file(path: Path) -> dict:
    if yaml is None or not path.is_file():
        return {}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8", errors="replace"))
    except (OSError, yaml.YAMLError):
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
        traceback.print_exc()
        return None, None, '<span class=mut>not built</span>'


# ── The items Task, as designed in b15 s41-task-items-procedure: three steps, each a tab named the same in Work and
# Report. Work: the step itself (what we have, read from disk; the recipe or build a person signs; the prompt, which
# takes the person's notes), folded to one line once done (s41-D15); then one card per topic, a list read down
# (s41-D09). Report: the cards only. The steps run through haipipe-labeling-preparation's engine, items_task.py
# (s41-D11); a person's Sign and Agree and a Draw again go through LabelingMixin's two narrow routes.
RESULTS = ("1 · Data", "2 · Items", "3 · Embedding")
OLD_RESULT = {"Itemization": RESULTS[0], "2 · Item": RESULTS[1], "3 · Item list": RESULTS[1],
              "4 · Embedding": RESULTS[2], "Embedding": RESULTS[2]}      # links made before s41 (261014)
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
                traceback.print_exc()
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


def _at(root: Path, path: str) -> Path:
    """A SPACE-relative path read from the served root (items_task.at; root / path when the engine is absent)."""
    return IT.at(root, path) if IT is not None and hasattr(IT, "at") else root / path


def _items_file(f: dict, root: Path) -> Path | None:
    store = f["metrics"].get("store") or f["manifest"].get("store")
    items = _at(root, str(store)) / "items.jsonl" if store else None
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
    path = _at(root, file)
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
