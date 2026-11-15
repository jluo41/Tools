"""The Goal tree: a face's deliverables, ticked from disk, under their Jobs and Tasks, each with the Runs that made it."""
from collections import Counter
from pathlib import Path
import os
import re
from urllib.parse import urlencode

import yaml
from live import frame
from live.work_progress_records import (
    clock, e, first_line, goal, kept, read_yaml, receipt_of, records,
    role_of, ROLE_ORDER, ROLES, said_of, section, state_of, text_of,
)
from live.work_progress_html import (
    chip, file_url, mark, means_html, nav, node, rows_table, run_link,
    run_mark, source_link, TICKS,
)


SPACE_DIRS = ("_WorkSpace/", "code/", "Tools/")   # a deliverable's files said from the SPACE root: its data store, its code
# package, and the toolkit (a page or a service a Job delivers there: j01's food API page, 261021)


def deliverables(folder):
    """A face's `## Deliverables`: a ```yaml block of `deliverables:`, each with what, kind, files (a glob or a list of
    them, SPACE-relative when it starts with _WorkSpace/ or code/, else from the face's folder), count, and the Run that makes it
    (JL 261020: "what are the deliveries? data? files? we want to have, eventually, after this block and for each job")."""
    text = section(text_of(frame.face(folder)), "Deliverables") if folder else ""
    found = re.search(r"```ya?ml\s*\n(.*?)```", text, re.S)
    try:
        items = (yaml.safe_load(found.group(1)) or {}).get("deliverables") if found else []
    except yaml.YAMLError:
        return []
    return [dict(i, owner=folder) for i in items or [] if isinstance(i, dict) and i.get("what")]


def task_of(item):
    """The Task an item sits under: its `task`, else the Task of the Run that made it, checked it, or made a part of it."""
    runs = [item.get("run"), item.get("checked_by")] + [r.get("run") for r in item.get("runs") or [] if isinstance(r, dict)]
    return item.get("task") or next((str(r).split("/")[0] for r in runs if r and "/" in str(r) and not str(r).startswith("..")), "")


def run_of(folder, ref, data):
    """A deliverable's Run, `tNN_<task>/rNN_<run>` under its face's folder or `rNN_<run>` of the folder itself."""
    if not ref:
        return None
    task_name, _, run = str(ref).rpartition("/")
    task = (folder / task_name).resolve() if task_name else folder
    rows = data.get(task)
    row = next((r for r in (rows if rows is not None else records(task) if task.is_dir() else []) if r["run"] == run), None)
    path = task / "runs" / run
    if row or not path.is_dir():
        return row
    receipt, card_ = receipt_of(path / "result/runtime.yaml"), read_yaml(path / "run.yaml")   # a Block's own Run
    return {"run": run, "task": task, "path": path, "receipt": receipt, "card": card_, "receipt_path": path / "result/runtime.yaml",
            "status": str(receipt.get("status") or card_.get("status") or "Not recorded"),
            "headline": receipt.get("headline") or first_line(path / "result/headline.txt") or said_of(receipt, path / "result")}


def item_state(item, root, data, with_hits=False):
    """✅ when every file is on disk and its Run (when named) finished; 🚧 or ❌ from that Run; 🔶 some files; ⬜ none."""
    pats = item.get("files") or []
    pats = [str(x) for x in (pats if isinstance(pats, list) else [pats])]
    hits = set()
    for pat in pats:
        base = root if pat.startswith(SPACE_DIRS) else item["owner"]
        hits.update(kept(("glob", str(base), pat), lambda: list(base.glob(pat)), seconds=30.0))   # one page's three uses, and its refresh
    need = int(item.get("count") or max(len(pats), 1))
    gate = item.get("run") or item.get("checked_by")                      # the Run that made it, else the one that checked it
    row = run_of(item["owner"], gate, data)
    ran = state_of(row) if row else None
    listed = [x.get("run") if isinstance(x, dict) else x for x in (item.get("runs") or [])]
    if not gate and listed:                     # several makers: done only when every one finished (b03 trial, 261021)
        states = [state_of(r) if r else None for r in (run_of(item["owner"], x, data) for x in listed)]
        gate, ran = True, ("running" if "running" in states else "failed" if "failed" in states else
                           "finished" if all(x == "finished" for x in states) else "unfinished")
    state = ("running" if ran == "running" else
             "done" if len(hits) >= need and (not gate or ran == "finished") else
             "partly" if hits else "failed" if ran == "failed" else "todo")      # a Run short of its gate with files on disk is partly there
    state = "partly" if state == "done" and item.get("open") else state     # something typed as still open
    return (state, len(hits), need, pats, row) + ((hits,) if with_hits else ())


def group_state(states):
    """A Task, Job or goal: ✅ when every item is, 🚧 while one runs, else 🔶 in progress; never ❌ for one open item
    (JL 261020: "we should not call it X, it is very negative")."""
    if states and all(s == "done" for s in states):
        return "done"
    return "running" if "running" in states else "partly" if {"done", "partly", "failed"} & set(states) else "todo"


def written(row, root):
    """The folders a Run recorded writing: its result/, its heavy.yaml paths, its metrics.json collection_root."""
    path = row.get("path")
    if not path or not path.is_dir():
        return []
    res = path / "result"
    out = [frame.rel(res, root)] if res.is_dir() else []
    out += [str(h.get("path")) for h in read_yaml(res / "heavy.yaml").get("heavy") or [] if isinstance(h, dict) and h.get("path")]
    folder = read_yaml(res / "metrics.json").get("collection_root")
    rec = row["receipt"]
    receipt = [str(w) for w in rec.get("writes") or [] if str(w).startswith("_WorkSpace/")]
    receipt += [str(rec[k]) for k in ("store",) if str(rec.get(k) or "").startswith("_WorkSpace/")]
    receipt += [str(Path(str(rec["audit_receipt"])).parent) for k in ("audit_receipt",) if str(rec.get(k) or "").startswith("_WorkSpace/")]
    return out + ([str(folder)] if folder else []) + receipt


def makers(item, hits, root, data):
    """The Runs that made an item (JL 261020: "what is one item with different runs?"): the ones it names, then any Run
    of its Job that recorded writing one of its files; each with the part it made."""
    owner, out, seen = item["owner"], [], set()

    def add(row, part):
        if row and (str(row["task"]), row["run"]) not in seen:
            seen.add((str(row["task"]), row["run"]))
            out.append((row, part))
    add(run_of(owner, item.get("run"), data), "")
    for spec in item.get("runs") or []:
        if isinstance(spec, dict):
            add(run_of(owner, spec.get("run"), data), str(spec.get("part") or ""))
    rels = [fast_rel(h, root) for h in hits]
    if rels and frame.level_of(owner) == "Job":
        for task in frame.children(owner, "Job"):
            for row in sorted(data.get(task) if data.get(task) is not None else records(task), key=lambda r: r["run"]):
                for folder in kept(("written", str(row.get("path")), row["status"]), lambda: written(row, root), seconds=30.0):
                    if any(r == folder or r.startswith(folder.rstrip("/") + "/") for r in rels):
                        add(row, folder.rstrip("/").rsplit("/", 1)[-1] if "_WorkSpace" in folder else "")
                        break
    out.sort(key=lambda m: (ROLE_ORDER.get(role_of(m[0]), len(ROLES)), m[0]["run"]))   # first passes, then retries and fixes
    return out


def short_folder(item, base, root):
    """A folder said from where the tree already stands (JL 261021: "我们就已经知道它是属于哪一个 job 的哪一个 task 了，
    你就直接从 run 开始写这个路径"): inside its Task, from runs/; in the Task's copy under _WorkSpace, the same, marked so."""
    owner = item["owner"]
    task = owner / task_of(item) if task_of(item) else owner
    for home in (task, owner):
        rel = frame.rel(home, root)
        if base == rel or base.startswith(rel + "/"):
            return base[len(rel) + 1:] or "."
        mirror = "/".join(Path(rel).parts[-3:]) if len(Path(rel).parts) >= 3 else rel
        if base.startswith("_WorkSpace/") and "/" + mirror + "/" in base:
            return "_WorkSpace › " + base.split("/" + mirror + "/", 1)[1]
    return base


def fast_rel(path, root):
    """A path from the root by trimming its text: a deliverable's files come from globs under the root, so no symlink
    needs resolving (resolving each of 500,000 answer files was most of a 40-second b02 page)."""
    text, base = str(path), str(root).rstrip("/") + "/"
    return text[len(base):] if text.startswith(base) else frame.rel(path, root)


def file_lines(item, pats, hits, root):
    """An item's folder said from its Task, then every one of its files on its own line (JL 261021)."""
    rels = sorted(fast_rel(h, root) for h in hits)
    if not rels:
        return "<div>Not on disk yet. It goes to</div>" + "".join(f"<div class=f><code>{e(short_folder(item, x, root))}</code></div>" for x in pats)
    base = str(Path(rels[0]).parent) if len(rels) == 1 else os.path.commonpath(rels)
    out = f"<div>📁 <code>{e(short_folder(item, base, root))}/</code></div>"
    shown = 24                                  # every file of a small set (JL 261021: "该列就列出来")
    if len(rels) > shown:                       # thousands of answers: each folder once, with how many files it holds
        folders = Counter(r[len(base) + 1:].rsplit("/", 1)[0] for r in rels)
        out += "".join(f'<div class=f>{e(f)}/<span class=m>{n:,} files</span></div>' for f, n in sorted(folders.items())[:shown])
        return out + (f"<div class=f>… and {len(folders) - shown:,} more folders</div>" if len(folders) > shown else "")
    by_rel = {fast_rel(h, root): h for h in hits}
    for rel in rels:
        hit, name = by_rel[rel], rel[len(base) + 1:]
        readable = hit.suffix in (".md", ".csv", ".json", ".png", ".html", ".txt") and not rel.startswith("_WorkSpace/")
        out += f"<div class=f>{source_link(hit, root, name) if readable else e(name)}</div>"
    return out


def run_line(row, part, root, when=False):
    roles = {k: l.split(" ")[0] for k, l, _ in ROLES}
    return (f'<div>{roles.get(role_of(row), "▫️")} {run_link(row, root)} <span class=m>{e(run_mark(row))}</span>'
            + (f'<span class=m>{e(clock(row["receipt"].get("finished_at")))}</span>' if when else "")
            + (f'<span class=m>{e(part)}</span>' if part else "") + "</div>")


def batches(item, root, data):
    """The batches one deliverable was gathered in (JL 261021: "the google search results should have three batches,
    is that so?"): each batch its files and the Runs that wrote them, folded inside the deliverable, never an item."""
    out, specs = "", [b for b in item.get("from") or [] if isinstance(b, dict)]
    for n, spec in enumerate(specs):
        sub = dict(spec, owner=item["owner"], what=spec.get("what") or f"batch {n + 1}")
        state, got, need, pats, _, hits = item_state(sub, root, data, with_hits=True)
        made = makers(sub, hits, root, data)
        out += (f'<details data-work-key="batch-{e(item["owner"].name)}-{e(item["what"])}-{n}"><summary>{mark(state)} '
                f'<b>{e(sub["what"])}</b></summary>'
                + (means_html(spec["means"]) if spec.get("means") else "")
                + file_lines(sub, pats, hits, root) + "".join(run_line(row, part, root) for row, part in made) + "</details>")
    return (f"<h5>From {len(specs)} batches</h5>" + out) if specs else ""


def example_section(item, root):
    """One real example of what a deliverable holds (JL 261021: "它 eventually 不应该是产生一个所谓的 set 吗？那这一个 set
    包含一个医生的什么东西，我怎么能看到呢？"): its first rows, then its first record whole, as a reader of it sees it,
    with its picture and every field."""
    ex = item.get("example")
    if not isinstance(ex, dict) or not ex.get("file"):
        return ""
    browse = ""
    if item.get("browse") and frame.level_of(item["owner"]) in ("Job", "Block"):
        n = next((i for i, x in enumerate(deliverables(item["owner"])) if x["what"] == item["what"]), 0)
        browse = f'<div style="margin:2px 0 6px">🔎 {frame.link(browse_url(item["owner"], root, n), "Browse the whole set")}</div>'
    path = root / str(ex["file"])
    if not path.is_file():
        return "<h5>One example</h5><div class=m style='margin-left:0'>Not on disk yet.</div>"
    import base64
    from live import page_reader
    if path.suffix.lower() == ".csv":
        # A CSV example needs only the standard library, so it shows on a host without pyarrow.
        import csv
        with path.open(newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        names = list(rows[0].keys()) if rows else []
        cols = [c for c in ex.get("columns") or names[:8] if c in names]
        return (f"<h5>One example</h5>{browse}<div>{e(str(ex.get('says') or ''))}</div>"
                f"<div class=m style='margin-left:0'>📄 {e(short_folder(item, frame.rel(path, root), root))} · "
                f"{len(rows):,} rows × {len(names)} columns, first {min(12, len(rows))} shown</div>"
                + rows_table(cols, [[r.get(c) for c in cols] for r in rows[:12]]))
    try:
        import pyarrow.parquet as pq
        table = kept(("example", str(path), path.stat().st_mtime_ns), lambda: pq.read_table(path, partitioning=None), seconds=300)
    except Exception as err:   # noqa: BLE001 - a missing reader or an unreadable file becomes a note, never a broken page
        return f"<h5>One example</h5><div class=m style='margin-left:0'>Cannot read {e(path.name)}: {e(type(err).__name__)}.</div>"
    cols = [c for c in ex.get("columns") or table.schema.names[:8] if c in table.schema.names]
    first = table.slice(0, 1).to_pylist()[0] if table.num_rows else {}
    out = (f"<h5>One example</h5>{browse}<div>{e(str(ex.get('says') or ''))}</div>"
           f"<div class=m style='margin-left:0'>📄 {e(short_folder(item, frame.rel(path, root), root))} · "
           f"{table.num_rows:,} rows × {table.num_columns} columns, first {min(12, table.num_rows)} shown</div>"
           + rows_table(cols, [[r.get(c) for c in cols] for r in table.select(cols).slice(0, 12).to_pylist()]))
    if not first:
        return out
    pic = first.get(ex.get("image")) if ex.get("image") else None
    kind = first.get("portrait_content_type") or "image/jpeg"
    img = (f'<img src="data:{e(str(kind))};base64,{base64.b64encode(pic).decode()}" alt="portrait" style="width:120px;flex:none">'
           if isinstance(pic, (bytes, bytearray)) and pic else "")
    text = page_reader.markdown_html(str(first.get(ex.get("record")) or "")) if ex.get("record") else ""
    out += ("<h5>One record, whole</h5>"
            f'<div style="display:flex;gap:16px;align-items:flex-start">{img}<div class=dossier style="flex:1;min-width:0">{text}</div></div>')
    fields = [(k, v) for k, v in first.items() if not isinstance(v, (bytes, bytearray))]
    out += (f'<details data-work-key="fields-{e(item["what"])}"><summary><b>All {len(first)} fields of this record</b></summary>'
            + rows_table(("field", "value"), [(k, v) for k, v in fields]) + "</details>")
    return out


def picture_of(hits, root):
    """A drawn deliverable shown, not only listed (JL 261023: "a drawing Task, and I cannot see its result?"): the
    preview.png beside its files, else the first .png among them; a set of thousands shows nothing here."""
    if not hits or len(hits) > 24:
        return ""
    folders = sorted({h.parent for h in hits})
    pics = [f / "preview.png" for f in folders if (f / "preview.png").is_file()] or sorted(
        h for h in hits if h.suffix.lower() == ".png")
    return "".join(f'<h5>What it looks like</h5><a href="{file_url(p, root)}" target=_blank rel=noopener>'
                   f'<img src="{file_url(p, root)}" alt="{e(p.name)}" loading=lazy style="max-width:100%;max-height:720px;'
                   f'border:1px solid var(--line)"></a>' for p in pics[:2])


def open_link(url):
    """A delivered page's address, opened in its own tab: `url:` on a deliverable, said from this host (/_api/try/meal)."""
    return f'<a href="{e(str(url))}" target=_blank rel=noopener>🔗 open it</a>'


def details_box(item, pats, hits, root, data):
    """What an opened item shows: where to open it (its `url:`), where its data is put, the Runs that made it, the batches
    it was gathered in, what is still open, who reads it."""
    out = (f'<h5>Open</h5><div>{open_link(item["url"])} <span class=mut>{e(str(item["url"]))}</span></div>'
           if item.get("url") else "")
    out += "<h5>Where</h5>" + file_lines(item, pats, hits, root) + example_section(item, root)
    out += picture_of(hits, root)
    made = makers(item, hits, root, data)
    if made or item.get("note"):
        out += "<h5>Made by</h5>" + "".join(run_line(row, part, root) for row, part in made)
        out += f'<div class=m style="margin-left:0">{e(item["note"])}</div>' if item.get("note") else ""
    out += batches(item, root, data)
    check = run_of(item["owner"], item.get("checked_by"), data)
    if check:                                  # a Run that rebuilt or compared it, never one that wrote it (JL 261021)
        out += "<h5>Checked by</h5>" + run_line(check, "", root, when=True)
    still = item.get("open")
    still = still if isinstance(still, list) else [still] if still else []
    out += ("<h5>Still open</h5>" + "".join(f"<div>🔶 {e(str(x))}</div>" for x in still)) if still else ""
    used = item.get("used_by")
    used = used if isinstance(used, list) else [used] if used else []
    return out + (f"<h5>Read by</h5><div>{e('; '.join(map(str, used)))}</div>" if used else "")


def item_node(item, root, data, key=""):
    """A deliverable, folded to one line: its mark, its short name, its kind and file count, the first words of its
    result (JL 261021: "默认关闭的状态下越简洁越好"); opened, what it holds, where it is, the Runs that made it, who reads it."""
    state, got, need, pats, row, hits = item_state(item, root, data, with_hits=True)
    link = ""
    if item.get("opens"):                                # a view a reader opens: ticked only when it really opens
        mates = deliverables(item["owner"])
        n = next((i for i, x in enumerate(mates) if x["what"] == item["opens"]), None)
        target = mates[n] if n is not None else {}
        index = root / str((target.get("browse") or {}).get("root") or "") / str((target.get("browse") or {}).get("index") or "")
        if target.get("browse") and index.is_file():
            link = frame.link(browse_url(item["owner"], root, n), "🔎 open it")
        elif state == "done":
            state = "todo"
    if item.get("url") and not link:                    # a page or a service it delivers: where to open it (JL 261021:
        link = open_link(item["url"])                   # "那我这个怎么打开这个 set 呢？... 没有给我链接？")
    said = str((row or {}).get("headline") or "").split(";")[0].strip()
    said = "" if row and said.startswith(row["run"]) else said              # a reader's line, never "<run>: key=value"
    head = (f'{mark(state)} <b>{e(item["what"])}</b>'
            + (f'<span class=chip>{e(item["kind"])}</span>' if item.get("kind") else "")
            + (chip("todo", "todo") if state == "todo" else "")
            + (f'<span class=m>{link}</span>' if link else "")
            + (f'<span class=m>{e(said[:110])}</span>' if said else ""))
    means = ("<h5>What it is</h5>" + means_html(item["means"], "means lead")         # big enough to read (JL 261021:
             if item.get("means") else "")                                        # "make this part a little big")
    return state, node(head, key=key, body=means + details_box(item, pats, hits, root, data), open_=False)   # folded: one line (JL 261021)


def items_nodes(items, root, data):
    def key(i, n):                              # the item as written and its face's date: an edit shows at once
        face = frame.face(i["owner"])
        return ("item", str(i["owner"]), n, repr(sorted((k, str(v)) for k, v in i.items() if k != "owner")),
                face.stat().st_mtime_ns if face else 0)
    made = [kept(key(i, n), lambda i=i, n=n: item_node(i, root, data, key=f"tree-{i['owner'].name}-{n}-{i['what']}"), seconds=5.0)
            for n, i in enumerate(items)]
    return [st for st, _ in made], "".join(h for _, h in made)


def tally(states):
    """One state word for a group of deliverables, never "N of M" (AGENTS.md Page words, JL 261113)."""
    done = sum(st == "done" for st in states)
    return "done" if states and done == len(states) else "not started" if not any(st != "todo" for st in states) else "in progress"


def level_head(icon, name, states, job=False):
    state = group_state(states) if states else "todo"
    return (f'<span class="lvl{" job" if job else ""}">{icon} {name}</span>'
            + chip(state, f"{TICKS[state] if state != 'todo' else '☐'} {tally(states)}" if states else "no deliverables listed"))


def task_nodes(job, items, root, data, mode, about=False):
    """A Job's deliverables under their Tasks, in folder order; one that names no Task, or a Task not made yet, sits
    under the Job itself, never dropped (Proj11 261022: planned Tasks hid their items and the Job read ✅).
    With `about`, the Job's own overview row comes first, above its Tasks (job_about)."""
    tasks = frame.children(job, "Job")
    made = {t.name for t in tasks}
    states, html_ = items_nodes([i for i in items if task_of(i) not in made], root, data)
    task_states = []
    for task in tasks:
        mine = [i for i in items if task_of(i) == task.name]
        if mine:
            got, kids = items_nodes(mine, root, data)
            states += got
            task_states.append(group_state(got))
            html_ += node(level_head("📂", nav(task, root, mode, "Goal", e(task.name)), got), task_about(task, root) + kids,
                          key="tree-" + frame.rel(task, root))
    if about:
        html_ = job_about(job, root, mode, states, task_states) + html_
    return states, html_


def job_about(job, root, mode, states, task_states):
    """The first row under a Job, above its Tasks: one line that pops out the Job's overview page (render_about)
    (JL 261022: "在所有 task 上面 ... 点一下，然后 pop out ... 一个 markdown file"; "这个 markdown file 是 render 得好的")."""
    url = frame.ROUTE + "?" + urlencode({"view": "work-about", "path": frame.rel(job, root)})
    return node(f'📄 {frame.pop(url, f"About · {job.name}", "About this Job")}<span class=m>{e(goal(job)[:110])}</span>')


def task_about(task, root):
    """A Task's first row, above its items: one line that pops out the Task's report (render_task_about), as a Job's
    does (JL 261022: "给 task 也来一个这种 report（pop out report）")."""
    url = frame.ROUTE + "?" + urlencode({"view": "work-about", "path": frame.rel(task, root)})
    return node(f'📄 {frame.pop(url, f"Report · {task.name}", "About this Task")}<span class=m>{e(goal(task)[:110])}</span>')


def browse_url(folder, root, item, **keys):
    q = {"view": "work-browse", "path": frame.rel(folder, root), "item": item}
    q.update({k: v for k, v in keys.items() if v not in (None, "")})
    return frame.ROUTE + "?" + urlencode(q)
