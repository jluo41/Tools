"""A Job's table and figure frames, and a family of Jobs drawn in one topic (draw_group); moved out of job_drawing.py.
job_drawing.py re-exports every name here, so `job_drawing.table_frame` and `python job_drawing.py group` still work."""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

from job_drawing import (BEGIN, END, GREY, INK, MAP_BUDGET, MOST_RUNS, PALETTE, W, Drawing, cell,  # noqa: F401
                         chart_frame, detail_frame, fill, finish, first_match, flow, job_info, jr, marks_of, n_of,
                         name_of, open_line, para, short, states, task_info, task_topics, topic_owner, yaml)


def table_rows(folders: list[tuple[Path, list[dict], str]], spec: dict) -> list[dict]:
    """One row per folder the spec keeps (`rows`, a glob; `skip`, globs): its id, each column's words and values,
    sorted by `sort` (`-Rows`: the column Rows, largest first)."""
    import fnmatch
    want, skip = str(spec.get("rows") or "*"), [str(s) for s in spec.get("skip") or []]
    named = all(len(runs) <= MOST_RUNS for _, runs, _ in folders)
    out = []
    for folder, runs, title in folders:
        if not fnmatch.fnmatch(folder.name, want) or any(fnmatch.fnmatch(folder.name, s) for s in skip):
            continue
        marks, cells, vals = marks_of(runs, named), [], {}
        for col in spec.get("columns") or []:
            words, v = cell(folder, col, str(spec.get("file") or ""), marks, title)
            cells.append(words)
            vals[str(col.get("label", ""))] = v
        has = not spec.get("file") or first_match(folder, str(spec["file"])) is not None
        out.append({"folder": folder, "id": folder.name[:3], "cells": cells, "vals": vals, "has": has})
    by = str(spec.get("sort") or "")
    if by:
        key, down = by.lstrip("-"), by.startswith("-")
        num = lambda v: v if isinstance(v, (int, float)) and not isinstance(v, bool) else None   # noqa: E731
        out.sort(key=lambda r: (num(r["vals"].get(key)) is None,
                                -(num(r["vals"].get(key)) or 0) if down else (num(r["vals"].get(key)) or 0)))
    return out


def widths_of(cols: list[str], cells: list[list[str]], total: float, size: float) -> list[float]:
    """Columns as wide as their words (an emoji counted a full em; one column at most 760 px), filling `total`: when
    they do not fit, only the widest ones give room and wrap, so a short value (a month, a count) stays on one line."""
    em = lambda s: len(re.findall(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", s)) * size * 0.5      # noqa: E731
    need = [max([Drawing.measure(c, 28)] + [min(Drawing.measure(r[k], size) + em(r[k]), 760) for r in cells]) + 44
            for k, c in enumerate(cols)]
    if sum(need) <= total:
        return [n * total / sum(need) for n in need]
    lo, hi = 120.0, max(need)                                   # one cap for the widest columns: they alone wrap
    for _ in range(40):
        cap = (lo + hi) / 2
        lo, hi = (cap, hi) if sum(min(n, cap) for n in need) < total else (lo, cap)
    return [min(n, lo) for n in need]


def table_frame(d: Drawing, info: dict, w: dict, job: Path, rows: list[dict], assets: Path,
                mark: str = "①") -> tuple[dict, list]:
    """A Job's Tasks as a table: its steps first (what was done, with its numbers), its reading as the key point, then
    one row per Task (what it holds), the columns marked `bar` drawn as bars beside it, row by row, on a log scale (a
    scoreboard, not a wall of numbers); its open points in red."""
    spec = w["table"]
    body = table_rows([(r["task"], r["runs"], str(r["title"])) for r in rows], spec)
    title = fill(spec.get("title") or f"📋 {name_of(info)}: what each Task holds", job)
    f = d.frame(f"{info['id']} {mark} {title}")
    y = jr.heading(d, title, fill(spec.get("sub") or "one row per Task, each cell read from its own files on every build", job))
    steps = w.get("flow") or []
    if steps:
        seq = [{"title": fill(s.get("title", ""), job), "lines": [fill(x, job) for x in s.get("lines") or []],
                "key": bool(s.get("key"))} for s in steps]
        labels = [fill(x, job) for x in (w.get("arrows") or [])] + ["then"] * len(seq)
        y = flow(d, seq, 40, y, W - 80, labels, title=32, leaf=28) + 50
    reading = fill(w.get("reading") or "", job).strip()
    if reading:
        kh = jr.tall("🎯 " + reading, W - 140, 30) + 44
        d.key(40, y, W - 80, kh)
        para(d, 70, y + 22, "🎯 " + reading, W - 140, 30)
        y += kh + 40
    specs = spec.get("columns") or []
    keep = [k for k, c in enumerate(specs) if not c.get("bar")]
    bars = [str(c.get("label", "")) for c in specs if c.get("bar")]
    cols = ["Task"] + [str(specs[k].get("label", "")) for k in keep]
    cells = [[b["id"]] + [b["cells"][k] for k in keep] for b in body]
    room = 620 if bars and body else 0                                  # the bars, at the right of the table
    head = y
    y = d.grid_table(40, y, cols, [{"cells": c, "dim": not b["has"]} for c, b in zip(cells, body)],
                     widths_of(cols, cells, W - 80 - room, 28), 28, pad=18)
    if room:
        top = d.rows_at[0][0]
        bx = W - 40 - room + 30
        para(d, bx, head, f"{' and '.join(bars)}, on a log scale", room - 30, 28, GREY)
        png = bars_png_rows(body, bars, [(t - top, h) for t, h in d.rows_at], room - 30, y - top,
                            assets / f"bars_{job.name[:3]}.png")
        d.picture(png, bx, top, room - 30, y - top, fid=f"img-{job.name[:3]}-bars")
    if spec.get("caption"):
        y = para(d, 40, y + 16, fill(spec["caption"], job), W - 80, 24)
    for o in w.get("open") or []:
        o = {k: fill(v, job) for k, v in o.items()} if isinstance(o, dict) else fill(o, job)
        y = para(d, 40, y + 16, open_line(o), W - 80, 28)
    return finish(d, f, y), body


def bars_png_rows(body: list[dict], bars: list[str], at: list[tuple], wpx: float, hpx: float, out: Path) -> Path:
    """Bars that line up with a table's rows (`at`: each row's top and height, from its first row): one panel per
    column in `bars`, side by side, log scale, each number at its bar's end, at the table's own type size."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(wpx / 100, hpx / 100), dpi=100)
    gap = 0.05
    cols = [[v if isinstance(v, (int, float)) and not isinstance(v, bool) else None for v in
             (b["vals"].get(label) for b in body)] for label in bars]
    span = [len(f"{max([v for v in vs if v] or [1]):,.0f}") + 4 for vs in cols]   # a panel as wide as its numbers need
    widths = [(1 - gap * (len(bars) - 1)) * s / sum(span) for s in span]
    for j, (label, vals) in enumerate(zip(bars, cols)):
        ax = fig.add_axes([sum(widths[:j]) + gap * j, 0, widths[j], 1])
        top = max([v for v in vals if v] or [1])
        colour = list(PALETTE.values())[j % 8]                       # a column its own hue, in the fixed order
        for (y, h), v in zip(at, vals):
            mid = y + h / 2
            if v:
                ax.barh(mid, v, height=min(h * 0.6, 34), color=colour, left=0.8)
            ax.text((v or 1) * 1.25 if v else 1.0, mid, f"{v:,.0f}" if v else ("0" if v == 0 else "—"),
                    va="center", fontsize=19, color="#1e1e1e")
        ax.set_xscale("log")
        ax.set_xlim(0.8, 0.8 * (max(top, 2) / 0.8) ** (1 / 0.5))   # the longest bar ends half way: room for its number
        ax.set_ylim(hpx, 0)
        ax.axis("off")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=100)
    plt.close(fig)
    return out


def figures_frame(d: Drawing, info: dict, w: dict, job: Path, body: list, mark: str = "②") -> dict | None:
    """The Job in pictures: what its Runs drew for the whole Job (`figures.pictures`, a timeline) on the left, its main
    Tasks' own pictures (`scans`, each at `scan.file` in the Task) on the right, each under its caption; the key point
    is the face's `shows`."""
    fig, scan = w.get("figures") or {}, w.get("scan") or {}
    left = []
    for p in fig.get("pictures") or []:
        hit = first_match(job, str(p.get("file", "")))
        if hit:
            left.append((hit, fill(p.get("caption") or Path(os.path.relpath(hit, job)).as_posix(), job)))
    named = {b["folder"].name: b for b in body}
    right = []
    for t in w.get("scans") or []:
        task = job / str(t)
        hit = first_match(task, str(scan.get("file") or "")) if scan.get("file") and task.is_dir() else None
        if hit:
            b = named.get(task.name)
            name = f"{task.name[:3]} · {b['cells'][0] if b else task.name}"
            right.append((hit, f"{name}: {fill(scan['caption'], task)}" if scan.get("caption") else name))
    if not (left or right):
        return None
    title = fill(fig.get("title") or f"📊 {name_of(info)} in pictures", job)
    f = d.frame(f"{info['id']} {mark} {title}")
    y = jr.heading(d, title, fill(fig.get("sub") or "the figures its Runs drew, read from disk on every build", job))
    shows = fill(w.get("shows") or "", job).strip()
    if shows:
        kh = jr.tall("🎯 " + shows, W - 140, 30) + 44
        d.key(40, y, W - 80, kh)
        para(d, 70, y + 22, "🎯 " + shows, W - 140, 30)
        y += kh + 40
    cols = [c for c in (left, right) if c]
    pw = (W - 80 - 60 * (len(cols) - 1)) / len(cols)
    ends = []
    for i, pics in enumerate(cols):
        px, yy = 40 + i * (pw + 60), y
        for k, (p, cap) in enumerate(pics):
            yy = para(d, px, yy, cap, pw, 28) + 12
            yy += d.picture(p, px, yy, pw, 1500, fid=f"img-{job.name[:3]}-{i}{k}-{p.parents[3].name[:3]}-{p.stem}") + 50
        ends.append(yy - 50)
    return finish(d, f, max(ends))


def jobs_frame(d: Drawing, title: str, jobs: list[Path], spec: dict, all_rows: dict) -> dict:
    """A family's Jobs as a table, one row per Job, each cell read from that Job's own files."""
    rows = [(j, [r for t in all_rows[j.name] for r in t["runs"]], jr.title_of(j)) for j in jobs]
    body = table_rows(rows, spec)
    head = str(spec.get("title") or f"📋 {title}: the Jobs side by side")
    f = d.frame(f"⓪ {head}")
    d.detail(f)
    y = jr.heading(d, head, str(spec.get("sub") or "one row per Job, each cell read from its own files on every build"))
    if spec.get("key"):                                                  # its slots read under the Block
        key = fill(spec["key"], jobs[0].parent)
        kh = jr.tall("🎯 " + key, W - 140, 30) + 44
        d.key(40, y, W - 80, kh)
        para(d, 70, y + 22, "🎯 " + key, W - 140, 30)
        y += kh + 40
    cols = ["Job"] + [str(c.get("label", "")) for c in spec.get("columns") or []]
    cells = [[b["id"]] + b["cells"] for b in body]
    y = d.grid_table(40, y, cols, [{"cells": c} for c in cells], widths_of(cols, cells, W - 80, 30), 30, pad=26)
    if spec.get("caption"):
        y = para(d, 40, y + 16, str(spec["caption"]), W - 80, 24)
    return finish(d, f, y)


def table_acts(d: Drawing, title: str, jobs: list[Path], all_rows: dict, words: dict, res: dict,
               assets: Path) -> tuple[list, list]:
    """One act per Job: ① its table (its steps, its reading, a row per Task with bars beside), ② its pictures; before
    them, for several Jobs, the family at a glance (a box per Job, then the Jobs as a table)."""
    each = words.get("each") or {}
    acts = []
    if len(jobs) > 1:
        row = [group_overview(d, title, jobs, all_rows, words, res)["id"]]
        if words.get("jobs_table"):
            row.append(jobs_frame(d, title, jobs, words["jobs_table"], all_rows)["id"])
        acts.append({"name": "Act 1 · the family at a glance", "frames": row, "arrow": ["side by side"]})
    for job in jobs:
        w = {**each, **(words.get(job.name) or {})}
        info = job_info(job)
        tf, body = table_frame(d, info, w, job, all_rows[job.name], assets)
        row, arrows = [tf["id"]], []
        if w.get("chart"):                                              # bars read from the Job's Runs, its words filled
            spec = {**w["chart"], **{k: fill(w["chart"][k], job) for k in ("title", "sub", "key", "caption")
                                     if w["chart"].get(k)}}
            cf = chart_frame(d, info, spec, job.parent, assets, f"{info['id']} ②")
            if cf:
                row.append(cf["id"])
                arrows.append("in a chart")
        ff = figures_frame(d, info, w, job, body, f"{'③' if len(row) > 1 else '②'}")
        if ff:
            row.append(ff["id"])
            arrows.append("in pictures")
        acts.append({"name": f"Act {len(acts) + 1} · {name_of(info)}", "frames": row, "arrow": arrows})
    between = [(a["frames"][0], b["frames"][0], "each Job" if i == 0 and len(jobs) > 1 else "next Job")
               for i, (a, b) in enumerate(zip(acts, acts[1:]))]
    return acts, between


# ── a family of Jobs in one topic (work/b03's s21-s25): an overview, then each Job explained from zero ───────
def group_cfg(face: Path) -> dict:
    """The face's `group:` yaml: per Job folder, the same words as a one-Job face's `job:` (intro, terms, inputs,
    outputs, formula, tasks, reading, sure, open)."""
    m = re.search(r"```yaml\s*\n(group:.*?)```", jr.read(face), re.S)
    if not (m and yaml):
        return {}
    try:
        return (yaml.safe_load(m.group(1)) or {}).get("group") or {}
    except Exception as err:
        print(f"{face.name}: its group: yaml does not read ({err})", file=sys.stderr)
        return {}


def group_overview(d: Drawing, title: str, jobs: list[Path], all_rows: dict, words: dict, res: dict) -> dict:
    """A family's first frame, a map: its key point, then one box per Job (its name, its Runs, what it concluded),
    three to a row at 28 px or more, joined to the key point as a tree; the conclusions shorten until ⑦'s words fit.
    Each Job's detail is its ③ frame below."""
    reading = res.get("reading") or {}
    key = str(reading.get("overview") or "").strip() or \
        f"{n_of(len(jobs), 'Job')}; each is explained from zero in its own frame below."
    start, per, gap = len(d.els), 3, 40
    for most, tell in ((200, 2), (140, 2), (140, 1), (100, 1), (70, 1), (45, 1), (0, 1), (0, 0)):
        del d.els[start:]                                    # the Runs' states go short before the conclusions do
        f = d.frame(f"⓪ {title}: every Job at a glance")
        y = jr.heading(d, title, "one box per Job: its Runs and what it concluded; each Job is explained from zero below")
        kh = jr.tall("🎯 " + key, W - 140, 30) + 44
        d.key(40, y, W - 80, kh)
        para(d, 70, y + 22, "🎯 " + key, W - 140, 30)
        above, y = (W / 2, y + kh), y + kh + 70
        boxes = []
        for job in jobs:
            runs = [r for t in all_rows[job.name] for r in t["runs"]]
            w = words.get(job.name) or {}                        # `gist`: the box's own short line, else the reading
            said = fill(w.get("gist") or w.get("reading") or reading.get(job.name) or "", job).strip()
            lines = ([f"{n_of(len(runs), 'Run')}: {states(runs)}" if tell == 2 else n_of(len(runs), "Run")]
                     if runs else ["⬜ no Run yet"]) if tell else []
            lines += [short(said, most)] if said and most else []
            name = str((res.get("labels") or {}).get(job.name) or jr.title_of(job))
            boxes.append((name if name.startswith(job.name[:3]) else f"{job.name[:3]} · {name}", lines))
        bw = (W - 80 - gap * (per - 1)) / per
        for k in range(0, len(boxes), per):
            row = boxes[k:k + per]
            hh = max(18 + jr.tall(t, bw - 40, 30) + 12 + sum(jr.tall(ln, bw - 40, 28) + 6 for ln in ls) + 16
                     for t, ls in row)
            mids = [40 + i * (bw + gap) + bw / 2 for i in range(len(row))]
            bus = y - 34                                     # the tree: from the key point (or the row above) to each Job
            d.line([(above[0], above[1] + 6), (above[0], bus)], sw=3)
            d.line([(min(mids + [above[0]]), bus), (max(mids + [above[0]]), bus)], sw=3)
            for m in mids:
                d.line([(m, bus), (m, y - 6)], sw=3)
            above = (mids[0], y + hh)
            for i, (t, ls) in enumerate(row):
                bx = 40 + i * (bw + gap)
                d.box(bx, y, bw, hh, INK, 2.5)
                yy = para(d, bx + 20, y + 18, t, bw - 40, 30) + 12
                for ln in ls:
                    yy = para(d, bx + 20, yy, ln, bw - 40, 28) + 6
            y += hh + 80
        if Drawing.words_small(d.els, f["id"])[0] <= MAP_BUDGET:
            break
    return finish(d, f, y - 80)


def draw_group(topic: Path) -> Path:
    """Redraw a family topic: job_results' overview (one row per Job, its numbers from disk), then one ③ frame per
    Job, three to a row; refresh the face's Runs ledger and the preview. The Jobs come from the face's results: yaml."""
    topic = topic.resolve()
    block = topic_owner(topic)
    face = topic / f"{topic.name}.md"
    res = jr.results_yaml(face)
    jobs = [block / str(n) for n in (res.get("jobs") or []) if (block / str(n)).is_dir()]
    if not jobs:
        raise SystemExit(f"{face}: its results: yaml names no Job (results.jobs)")
    words = group_cfg(face)
    all_rows = {j.name: jr.job_rows(block, j, res) for j in jobs}
    topics = task_topics(block)
    title = re.sub(r"^s\d+\s*·\s*", "", jr.read(face).splitlines()[0])
    d = Drawing()
    if (words.get("each") or {}).get("table") or any((words.get(j.name) or {}).get("table") for j in jobs):
        acts, between = table_acts(d, title, jobs, all_rows, words, res, topic / "assets")   # a table per Job (261013)
        return finish_group(d, topic, face, acts, between, jobs, all_rows)
    ov = group_overview(d, title, jobs, all_rows, words, res)
    frames = []
    for job in jobs:
        w = dict(words.get(job.name) or {})
        w.setdefault("reading", ((res.get("reading") or {}).get(job.name) or ""))
        tasks = [task_info(r, res) for r in all_rows[job.name]]
        made = chart_frame(d, job_info(job), w["chart"], block, topic / "assets") if w.get("chart") else None
        if made is None and w.get("detail") is True:            # a text frame only when the face asks (261012)
            made = detail_frame(d, job_info(job), tasks, topics, w, topic / "assets")
        if made:
            frames.append(made["id"])
    acts = [{"name": "Act 1 · the family at a glance", "frames": [ov["id"]]}]
    for k in range(0, len(frames), 3):
        acts.append({"name": f"Act {len(acts) + 1} · what they found",
                     "frames": frames[k:k + 3], "arrow": "next Job"})
    between = [(ov["id"], frames[0], "each Job")] if frames else []
    between += [(acts[i]["frames"][0], acts[i + 1]["frames"][0], "next Jobs") for i in range(1, len(acts) - 1)]
    return finish_group(d, topic, face, acts, between, jobs, all_rows)


def finish_group(d: Drawing, topic: Path, face: Path, acts: list, between: list, jobs: list, all_rows: dict) -> Path:
    """Lay the acts out, write the drawing (a person's marks kept) and its preview, refresh the face's Runs ledger."""
    d.acts(acts, between=between, gap=700)
    out = topic / f"{topic.name}.excalidraw"
    d.write(out, f"hai-draw job scripts/job_drawing.py group {topic.name}")
    from render_png import render
    render(out, out.with_suffix(".png"))
    text = jr.read(face)
    if BEGIN in text and END in text:
        head, rest = text.split(BEGIN, 1)
        face.write_text(head + jr.ledger(topic, jobs, all_rows) + rest.split(END, 1)[1], encoding="utf-8")
    return out
