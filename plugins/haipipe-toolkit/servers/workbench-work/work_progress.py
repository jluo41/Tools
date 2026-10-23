"""Goal, Plan, Execution and Results over existing work records.

A Block opts in with workbench-layout: workflow. Reading never creates plans,
changes Run status, or infers goal acceptance from completed execution counts.
"""
from collections import Counter
import json
import time
from datetime import datetime, timezone
from pathlib import Path
import os
import re
from urllib.parse import urlencode, quote

import yaml
from live import frame

VIEWS = ("Goal", "Plan", "Execution", "Results")
MODES = ("Audience Report", "Work Details")
PURPOSES = {
    "asset-contract": "Define output fields and usage rules",
    "asset-build": "Build a reference table from raw inputs",
    "asset-freeze": "Save service answers for a specific version for later reuse",
    "asset-validate": "Check output tables against field and data rules",
    "asset-parity": "Check whether frozen answers match the corresponding service answers",
    "asset-compare": "Compare outputs from two versions",
    "asset-release": "Pin the exact version of each table in the release",
    "asset-gallery": "Check outputs for different input types across the full workflow",
    "unit-test": "Check shared code behavior and compatibility",
    "eval-ab": "Compare results with and without a specific change",
    "external-corpus": "Check method performance on external data",
}
e = frame.esc


_LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)          # libyaml when present: about ten times faster
_READ = {}
_TTL = {}


def read_yaml(path):
    """A YAML or JSON file as a dict, parsed once until the file changes (JL 261021: "每一次 change 的时候，它都会花很长时间")."""
    try:
        if not path:
            return {}
        st = path.stat()
        if st.st_size > 2_000_000:
            return {}
        key = (str(path), st.st_mtime_ns, st.st_size)
        if key not in _READ:
            text = path.read_text(encoding="utf-8")
            try:
                value = json.loads(text) if path.suffix == ".json" else yaml.load(text, Loader=_LOADER)
            except yaml.YAMLError:
                value = top_level(text)
            _READ[key] = value if isinstance(value, dict) else {}
        return _READ[key]
    except (OSError, ValueError, yaml.YAMLError):
        return {}


def top_level(text):
    """A receipt YAML cannot parse still has its top-level `key: value` lines: an older receipt wrote an unquoted
    headline with a colon in it (`headline: B1 food: FAIL, ...`), and dropping the whole file read a complete Run as
    "Not recorded" (b51 j01 t12-t15, 261021)."""
    out = {}
    for line in text.splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*):[ \t]*(.*?)[ \t]*$", line)
        if m and m.group(2) and m.group(2) not in ("|", ">", "|-", ">-"):
            out.setdefault(m.group(1), None if m.group(2) == "null" else m.group(2).strip("\"'"))
    return out


def kept(key, make, seconds=8.0):
    """A value kept for a few seconds, so one page and its own 20-second refresh never rebuild it twice."""
    now = time.monotonic()
    hit = _TTL.get(key)
    if hit and now - hit[0] < seconds:
        return hit[1]
    value = make()
    _TTL[key] = (now, value)
    return value


def receipt_of(path):
    """A Run's receipt with its times under one name: a Databricks ticket's receipt says `started` and `ended`, read
    here as `started_at` and `finished_at`."""
    rec = read_yaml(path)
    alias = {k: rec[v] for k, v in (("started_at", "started"), ("finished_at", "ended")) if not rec.get(k) and rec.get(v)}
    return dict(rec, **alias) if alias else rec


def summary_line(summary):
    """A receipt's `summary:` said as one line, number first (28 tables · 1,562,150,228 rows total), when the receipt
    writes no headline of its own."""
    if not isinstance(summary, dict):
        return ""
    out = []
    for k, v in summary.items():
        words = str(k).replace("_", " ")
        if isinstance(v, bool) or v in (None, "", [], {}):
            continue
        if isinstance(v, (int, float)):
            out.append(f"{v:,} {words}")
        elif isinstance(v, str) and len(v) <= 40:
            out.append(f"{words} {v}")
        elif isinstance(v, list) and all(isinstance(x, (str, int, float)) for x in v):
            out.append(f"{words}: {', '.join(map(str, v[:3]))}" + (" …" if len(v) > 3 else ""))
    return " · ".join(out[:6])[:240]


def said_of(receipt, result):
    """A Run's key result from its own numbers when it writes no headline: its receipt's `summary:` or `counts:`, the
    tables its `outputs:` lists (patient_universe: 466,745 rows · 7 columns), else its result/metrics.json."""
    for key in ("summary", "counts"):
        line = summary_line(receipt.get(key))
        if line:
            return line
    outs = [o for o in receipt.get("outputs") or [] if isinstance(o, dict)] if isinstance(receipt.get("outputs"), list) else []
    if outs:
        return " · ".join(f"{o.get('table') or o.get('name') or 'output'}: "
                          + summary_line({k: o[k] for k in ("rows", "columns") if k in o}) for o in outs[:3])[:240]
    return summary_line(read_yaml(result / "metrics.json")) if result else ""


def text_of(path):
    try:
        return path.read_text(encoding="utf-8", errors="replace") if path else ""
    except OSError:
        return ""


def section(text, name):
    match = re.search(rf"(?ims)^##\s+{re.escape(name)}\s*\n(.*?)(?=^##\s|\Z)", text)
    return match.group(1).strip() if match else ""


def face_fields(folder):
    md = frame.face(folder)
    if not md:
        return {}
    return dict(frame.fields(md, keys=(
        "goal", "spine", "develops", "close", "input", "output", "state",
        "goal-status", "goal-scope", "workbench-layout", "emoji")))


def enabled(folder, root):
    block = frame.chain(folder, root).get("Block")
    return bool(block and face_fields(block).get("workbench-layout") == "workflow")


def goal(folder):
    fields = {k: v for k, v in face_fields(folder).items()          # a new face's `goal: open` is a placeholder, not
              if str(v).strip().lower() not in ("open", "<open>", "none", "-")}   # a goal (212 work Jobs, 261021)
    opening = section(text_of(frame.face(folder)), "Opening")
    return (fields.get("goal") or fields.get("spine") or fields.get("develops")
            or frame._first_sentence(opening, 300) or "Goal not yet specified")


SPACE_DIRS = ("_WorkSpace/", "code/", "Tools/")   # a deliverable's files said from the SPACE root: its data store, its code
# package, and the toolkit (a page or a service a Job delivers there: j01's food API page, 261021)
TICKS = {"done": "✅", "running": "🚧", "failed": "❌", "partly": "🔶", "todo": "⬜"}


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


TREE_CSS = """<style>
.dtree,.dtree ul{list-style:none;margin:0;padding-left:22px}
.dtree{padding-left:6px;margin:8px 0 4px}
.dtree li{position:relative;padding:2px 0 2px 22px;line-height:1.5}
.dtree>li{padding-top:5px}
.dtree>li::after{top:17px}
.dtree>li:last-child::before{height:17px}
.dtree details{margin:0}
.dtree li::before{content:"";position:absolute;left:0;top:0;bottom:0;border-left:1.5px solid var(--tab-line,#ced4da)}
.dtree li:last-child::before{bottom:auto;height:14px}
.dtree li::after{content:"";position:absolute;left:0;top:14px;width:17px;border-top:1.5px solid var(--tab-line,#ced4da)}
.dtree summary{list-style:none;cursor:pointer;border-radius:6px;padding:1px 4px;margin-left:-4px}
.dtree summary:hover{background:rgba(127,127,127,.08)}
.dtree summary::-webkit-details-marker{display:none}
.dtree summary::before{content:"▸";color:var(--mut,#6f6f6b);display:inline-block;width:14px}
.dtree details[open]>summary::before{content:"▾"}
.dtree .lvl{font-weight:650}
.dtree .job{font-size:15.5px}
.dtree .chip{display:inline-block;font-size:11.5px;line-height:18px;padding:0 8px;border-radius:9px;background:var(--wash,#f6f6f7);border:1px solid var(--line,#e3e3e6);color:var(--mut,#6f6f6b);margin-left:10px;vertical-align:1px}
.dtree .chip.ok{color:var(--ok,#24733d)}
.dtree .chip.part{color:var(--warn,#996b00)}
.dtree .chip.todo{background:transparent;border-style:dashed}
.dtree .m{color:var(--mut,#6f6f6b);font-size:12.5px;margin-left:10px}
.dtree .means{color:var(--fg,#1c1c1c);font-size:13px;margin:0 0 4px}
.dtree .box .lead{font-size:15px;line-height:1.6;margin:2px 0 12px;max-width:820px}   /* what the item is, read first (JL 261021) */
.dtree .box ul.means{list-style:disc;padding-left:22px}
.dtree .box ul.means li{padding:1px 0;line-height:1.55}
.dtree .box ul.means li::before,.dtree .box ul.means li::after{display:none}
.dtree .box{margin:4px 0 4px 21px;padding:6px 12px 6px 14px;border-left:3px solid var(--line,#e3e3e6);font-size:12.5px;color:var(--mut,#6f6f6b);max-width:980px}
.dtree .box h5{margin:6px 0 2px;font-size:12px;color:var(--fg,#1c1c1c);font-weight:650}
.dtree .box h5:first-child{margin-top:0}
.dtree .box .f{margin-left:20px}
.dtree .box details{margin:2px 0}
.dtree .box details>summary{margin-left:0}
.dtree .box details>:not(summary){margin-left:18px}
.dtree .hollow{display:inline-block;width:18px;text-align:center;color:var(--mut,#6f6f6b)}
.dtree-tools{display:inline-flex;margin:8px 0 2px;border:1px solid var(--line,#e3e3e6);border-radius:999px;overflow:hidden;background:var(--card,#fff)}
.dtree-tools button{all:unset;cursor:pointer;font-size:12.5px;line-height:22px;padding:0 12px;color:var(--mut,#6f6f6b)}
.dtree-tools button+button{border-left:1px solid var(--line,#e3e3e6)}
.dtree-tools button:hover{background:var(--tab-wash,#e7f5ff);color:var(--tab-on,#1864ab)}
</style>"""
TREE_TOOLS = ('<div><span class=dtree-tools><button type=button title="Open every Job and Task" onclick="this.closest(\'.dtree-wrap\')'
              '.querySelectorAll(\'details.branch\').forEach(d=>d.open=true)">▾ Open all</button><button type=button '
              'title="Fold every Job, Task and item" onclick="this.closest(\'.dtree-wrap\').querySelectorAll(\'details\')'
              '.forEach(d=>d.open=false)">▸ Fold all</button></span></div>')


def mark(state):
    """An item's mark: done, partly, running, failed; an item not started is an empty box marked todo (JL 261020:
    "如果是没完成的，就变成一个中括号 ... todo、plan 之类的")."""
    return '<span class=hollow>☐</span>' if state == "todo" else TICKS[state]


def chip(state, text):
    kind = {"done": "ok", "todo": "todo"}.get(state, "part")
    return f'<span class="chip {kind}">{e(text)}</span>'


def run_mark(row):
    """A Run's own mark (JL 261020: "这些 run 应该也要有不同的状态或者标识"): ✅ finished; 🔶 finished with searches
    unanswered or its gate missed; a receipt rebuilt from the Run's files counts the same as one its ticket wrote."""
    state = state_of(row)
    rec = row["receipt"]
    out = rec.get("outcome") if isinstance(rec.get("outcome"), dict) else {}
    asked, answered = out.get("searches_asked"), out.get("searches_answered")
    counted = f"{answered:,} of {asked:,} answered" if isinstance(asked, int) and isinstance(answered, int) else ""
    if not counted and isinstance(rec.get("expected_rows"), int) and isinstance(rec.get("stored_rows"), int):
        asked, answered = rec["expected_rows"], rec["stored_rows"]          # a CallStore receipt (bind_callstore_receipts.py)
        counted = f"{answered:,} of {asked:,} stored" + (f", audit {rec['audit_verdict']}" if rec.get("audit_verdict") else "")
    gate = str(rec.get("gate") or "")
    if state == "finished":
        if gate.startswith("missed"):
            return "🔶 finished, gate " + gate + (f"; {counted}" if counted else "")
        if counted and answered < asked:
            return f"🔶 finished, {counted}"
        return "✅ finished" + (f", {counted}" if counted and rec.get("audit_verdict") else "")
    if state == "partial":
        return "🔶 partial" + (f", {counted}" if counted else "")
    if state == "blocked" and isinstance(rec.get("repair"), dict):
        return f"📦 ran {str(rec['repair'].get('newest_file_at') or '')[:10]}, no receipt"
    return {"running": "🚧 running", "failed": "❌ failed", "blocked": "⛔ blocked", "waiting": "◌ planned"}.get(state, "⚪ no record")


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
                f'<b>{e(sub["what"])}</b><span class=m>{got} of {need} files</span><span class=m>{len(made)} Runs</span></summary>'
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
    """A delivered page's address, opened in its own tab: `url:` on a deliverable, said from this host (/_api/try/food)."""
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


def means_html(means, cls="means"):
    """What an item or batch is: a list is bullets, one short point each (JL 261021: "这里可以用 bullet points 吗"); a
    sentence stays one paragraph."""
    if isinstance(means, list):
        return f'<ul class="{cls}">' + "".join(f"<li>{e(str(x))}</li>" for x in means) + "</ul>"
    return f'<div class="{cls}">{e(str(means))}</div>'


def node(head, kids="", key="", body="", open_=False, below=""):
    """One branch of the Goal tree, a folder structure (JL 261020: "像 folder 那种 structure 的 mind map"; "could I
    collapse them"): a Job or Task folds its children; a deliverable folds its details. Everything starts folded (JL
    261021: "could you make the fold all to be default?"); what a reader opens stays open across a refresh."""
    inner = (f"<ul>{kids}</ul>" if kids else "") + (f"<div class=box>{body}</div>" if body else "")
    summary = head + (f"<div class=means>{below}</div>" if below else "")
    if not inner:
        return f"<li>{summary}</li>"
    kind = "branch" if kids else "leaf"
    return (f'<li><details class={kind}{" open" if open_ else ""} data-work-key="{e(key)}"><summary>{summary}</summary>'
            f"{inner}</details></li>")


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
            + (f'<span class=m>{got} of {need} files</span>' if need > 1 else "")
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
    return f"{sum(st == 'done' for st in states)} of {len(states)}"


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


def topic_pictures(folder, root, job=None):
    """Every Studio topic that names this Job or Task, each its picture and a link to it in the Block's Studio (JL
    261022, sending b51's s01-food-api drawing: "we also need ... job level report and task level report"). A Job's own
    `sNN-jNN-…` topic comes first, then each topic whose face names it; a Task's topic must also name its Job, or be
    that Job's own topic, since Task names repeat across Jobs. s00 is the Block's index, never a Job's or a Task's."""
    block = frame.chain(folder, root).get("Block")
    topics = list(frame.studio_inventory(block, root)) if block else []
    jnn = (job or folder).name.split("_")[0]
    own = [t for t in topics if re.match(rf"^s\d\d-{jnn}-", t[1].name)]

    def names(t):
        said = text_of(frame._notes(t[1]))
        return folder.name in said and (job is None or job.name in said or t in own)
    picked = ([] if job else own) + [t for t in topics if not t[1].name.startswith("s00") and t not in
                                     ([] if job else own) and names(t)]
    out = []
    for owner, topic, _ in picked:
        png = topic / f"{topic.name}.png"
        png = png if png.is_file() else next(iter(sorted(topic.glob("*.png"))), None)
        if not png:
            continue
        url = frame.ROUTE + "?" + urlencode({"path": frame.rel(folder, root), "studio": "1", "studio_group": "all"})
        url += "#" + frame.studio_anchor(topic, owner, block)
        out.append(f'<figure><a href="{e(url)}"><img src="{file_url(png, root)}" alt="{e(topic.name)}" loading=lazy '
                   f'style="width:100%;max-width:900px;display:block"></a><figcaption class=md-file>'
                   f'{frame.link(url, topic.name)}</figcaption></figure>')
    return "".join(out)


def job_drawing(job, root):
    """The Job's Studio drawings: its own topic, then every topic that names it (topic_pictures)."""
    return topic_pictures(job, root)


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


def render_task_about(task, root):
    """A Task's report as one rendered Markdown page, for the pop-out: its goal, close line and state, its Runs by
    role (mark, when it finished, its one-line result; each opens its own page), its Opening, what it hands on, and
    the charts its figures Runs drew, all read from disk on each open."""
    from live import page_reader
    fields, face = face_fields(task), text_of(frame.face(task))
    title = next((l[2:].strip() for l in face.splitlines() if l.startswith("# ")), task.name)
    job = frame.chain(task, root).get("Job")
    items = [i for i in deliverables(job) if task_of(i) == task.name] if job else []
    data = snapshot("Task", task)
    states = {id(i): item_state(i, root, data)[0] for i in items}
    rows = records(task)
    md = [f"# 📂 {title}", "", f"**Goal.** {goal(task)}", ""]
    if fields.get("close"):
        md += [f"**Close when.** {fields['close']}", ""]
    if fields.get("state"):
        md += [f"**State.** {fields['state']}", ""]
    done = sum(states[id(i)] == "done" for i in items)
    md += ["## Progress", "", f"{done} of {len(items)} items delivered" if items else "no items listed for this Task"]
    md[-1] += f" · {runs_n(len(rows))}" + (f" · {run_tally(rows)}" if rows else "")
    md.append("")
    if rows:
        names = {k: l for k, l, _ in ROLES}
        md += ["| Role | Run | Mark | Finished | Result |", "|---|---|---|---|---|"]
        for row in sorted(rows, key=lambda r: (ROLE_ORDER.get(role_of(r), len(ROLES)), r["run"])):
            rec = row["receipt"]
            url = frame.ROUTE + "?" + urlencode({"view": "work-run", "path": frame.rel(task, root), "run": row["run"]})
            said = str(row.get("headline") or "").split(";")[0].strip()
            said = "" if said.startswith(row["run"]) else said.replace("|", "/")
            when = clock(rec["finished_at"]) if rec.get("finished_at") else "-"
            md.append(f"| {names.get(role_of(row), 'no role')} | [{row['run']}]({url}) | {run_mark(row)} | {when} | "
                      f"{said[:160] or '-'} |")
        md.append("")
    opening = section(face, "Opening")
    if opening.strip():
        md += ["## Opening", "", opening.strip(), ""]
    html_ = page_reader.markdown_html("\n".join(md))
    if items:
        lines = ["## What it hands on", ""]
        for i in items:
            st = states[id(i)]
            means = i.get("means")
            first = (means[0] if isinstance(means, list) and means else str(means or "")).strip()
            lines.append(f"- {'☐' if st == 'todo' else TICKS[st]} **{i['what']}**" + (f": {first}" if first else ""))
        html_ += page_reader.markdown_html("\n".join(lines))
    figures = []
    for row in rows:                                   # the charts a figures Run drew, newest Run last
        if role_of(row) == "figures":
            res = task / "runs" / row["run"] / "result"
            res = res if res.is_dir() else task / "results" / row["run"]
            figures += sorted(res.glob("*.png"))[:6] if res.is_dir() else []
    if figures:
        html_ += page_reader.markdown_html("## Figures") + "".join(
            f'<figure><img src="{file_url(f, root)}" alt="{e(f.name)}" loading=lazy><figcaption class=md-file>'
            f'{e(f.parent.parent.name)} · {e(f.name)}</figcaption></figure>' for f in figures[:12])
    drawings = topic_pictures(task, root, job) if job else ""
    if drawings:                                       # the Studio topics that name this Task (JL 261022)
        html_ += page_reader.markdown_html("## Drawings") + drawings
    back = nav(task, root, "Audience Report", "Goal", "Open the Task page")
    return ('<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,'
            f'initial-scale=1"><title>Report · {e(task.name)}</title><style>{page_reader.MARKDOWN_CSS}'
            'figure{margin:.8em 0}td:nth-child(1),td:nth-child(3),td:nth-child(4){white-space:nowrap}'
            f'</style></head><body><p class=md-file>{e(task.name)} · report, read from disk · {back}</p>{html_}</body></html>')


def background_md(job):
    """A face's `## Background` as Markdown pieces and drawn timelines, in order: ("md", text) or ("html", svg)."""
    text = section(text_of(frame.face(job)), "Background")
    out = []
    for k, chunk in enumerate(re.split(r"^```[^\n]*\n(.*?)^```[ \t]*$", text, flags=re.M | re.S)):
        if k % 2 == 0:
            if chunk.strip():
                out.append(("md", chunk))
            continue
        try:
            spec = yaml.load(chunk, Loader=_LOADER)
        except yaml.YAMLError:
            spec = None
        if isinstance(spec, dict) and isinstance(spec.get("timeline"), dict):
            out.append(("html", f'<figure>{timeline_svg(spec["timeline"])}</figure>'))
        else:
            out.append(("md", f"```\n{chunk}```\n"))
    return out


def render_about(job, root):
    """A Job's overview as one rendered Markdown page, for the pop-out: its goal and close line, its progress Task by
    Task, its Topic, its Background, what it hands on, and its Studio drawing, all read from disk on each open."""
    from live import page_reader
    data = snapshot("Job", job)
    fields, face = face_fields(job), text_of(frame.face(job))
    title = next((l[2:].strip() for l in face.splitlines() if l.startswith("# ")), job.name)
    items = deliverables(job)
    states = {id(i): item_state(i, root, data)[0] for i in items}
    tasks = frame.children(job, "Job")
    rows = [r for t in tasks for r in records(t)]
    done = [i for i in items if states[id(i)] == "done"]
    md = [f"# {fields.get('emoji') or '🗂'} {title}", "", f"**Goal.** {goal(job)}", ""]
    if fields.get("close"):
        md += [f"**Close when.** {fields['close']}", ""]
    md += ["## Progress", "", f"{len(done)} of {len(items)} items delivered · {len(tasks)} Tasks"
           + (f" · Runs {run_tally(rows)}" if rows else ""), "", "| Task | What it delivers | Items | Runs |",
           "|---|---|---|---|"]
    for t in tasks:
        mine = [i for i in items if task_of(i) == t.name]
        st = group_state([states[id(i)] for i in mine]) if mine else "todo"
        tick = "☐" if st == "todo" else TICKS[st]
        url = frame.ROUTE + "?" + urlencode({"path": frame.rel(t, root), "space": "Audience Report", "sub": "Goal"})
        what = (face_fields(t).get("goal") or "").replace("|", "/")
        md.append(f"| {tick} [{t.name}]({url}) | {what} | {tally([states[id(i)] for i in mine]) if mine else '-'} | "
                  f"{run_tally(records(t)) or '-'} |")
    md.append("")
    topic = section(face, "Topic")
    if topic.strip():
        md += ["## Topic", "", topic.strip(), ""]
    html_ = page_reader.markdown_html("\n".join(md))
    pieces = background_md(job)
    if pieces:
        html_ += page_reader.markdown_html("## Background")
        html_ += "".join(page_reader.markdown_html(v) if k == "md" else v for k, v in pieces)
    if items:
        lines = ["## What it hands on", ""]
        for i in items:
            st = states[id(i)]
            means = i.get("means")
            first = (means[0] if isinstance(means, list) and means else str(means or "")).strip()
            lines.append(f"- {'☐' if st == 'todo' else TICKS[st]} **{i['what']}**" + (f": {first}" if first else ""))
        html_ += page_reader.markdown_html("\n".join(lines))
    drawing = job_drawing(job, root)
    if drawing:
        html_ += page_reader.markdown_html("## Drawings") + drawing
    back = nav(job, root, "Audience Report", "Goal", "Open the Job page")
    return ('<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,'
            f'initial-scale=1"><title>About · {e(job.name)}</title><style>{page_reader.MARKDOWN_CSS}'
            'figure{margin:.6em 0}svg{max-width:100%;height:auto}td:nth-child(1),td:nth-child(3),td:nth-child(4){white-space:nowrap}'
            f'</style></head><body><p class=md-file>{e(job.name)} · overview, read from disk · {back}</p>{html_}</body></html>')


def timeline_svg(spec):
    """A meal drawn down its timeline (JL 261021: a sketch of Item1..Item3 as lanes, t1..tN down the side, and
    bites that take some of several items at one moment): each food item a vertical lane, each time a row, each
    bite a band across the items it holds. `spec`: {items, times, bites: [{name, at, items}], title?}. `spans:
    [{name, item, from, to, aside?}]` draws the other shape, one lane over a stretch of time (an exercise activity,
    from its start to its end; `aside` dashed, as a device's day total; s22 j02, JL 261021). A span with
    `zoom: true` and the block's `zoom: {items, times, bites, ...}` draw one picture: the day on the left, and that
    span opened on the right into its own lanes and bites, joined by two dashed lines (j01, JL 261021: "你可以把这两个
    图融成一个图吗"). `rule: {question, branches: [{answer, title, then, example, today?}]}` draws the handling rule
    as a small decision at the top right, a question and a box per answer (j01, JL 261021: "假如没有时间 ... 只记了开始、
    没有记结束，这时候该怎么办？... 你在这个地方完全没有显示出来")."""
    parts, width, height, at = timeline_parts(spec)
    if not parts:
        return ""
    zoom, opened = spec.get("zoom"), next((s for s in spec.get("spans") or [] if s.get("zoom")), None)
    extra, dx, below = "", width + 70, 0
    if isinstance(spec.get("rule"), dict):                           # the handling rule, top right
        rparts, rw, rh = rule_parts(spec["rule"], dx - 14, 40, int(spec["rule"].get("width") or 660))
        extra, below = rparts, 40 + rh + 40
        width, height = max(width, dx - 14 + rw + 6), max(height, below)
    if isinstance(zoom, dict) and opened and opened.get("name") in at:
        zparts, zw, zh, _ = timeline_parts(zoom, arrow=False)
        if zparts:
            x0, y0, x1, y1 = at[opened["name"]]                      # the span that opens, on the day
            mid = (y0 + y1) / 2
            dy = max(below, mid - zh / 2)                            # under the rule, when there is one
            fx, fy = dx - 14, dy
            extra += (f'<g transform="translate({dx} {dy})">{zparts}</g>'
                     f'<rect x="{fx}" y="{fy}" width="{zw + 14}" height="{zh}" rx="12" fill="none" '
                     'stroke="currentColor" stroke-width="1.5"/>'
                     f'<line x1="{x1}" y1="{y0}" x2="{fx}" y2="{fy + 12}" stroke="currentColor" stroke-width="1.2" '
                     'stroke-dasharray="5 5"/>'
                     f'<line x1="{x1}" y1="{y1}" x2="{fx}" y2="{fy + zh - 12}" stroke="currentColor" '
                     'stroke-width="1.2" stroke-dasharray="5 5"/>')
            width, height = max(width, dx + zw + 6), max(height, dy + zh + 4)    # room for the frame's stroke
    return (f'<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" '
            f'aria-label="{e(spec.get("title") or "a meal down its timeline")}" '
            'style="max-width:100%;height:auto;color:inherit;font-family:inherit">'
            '<defs><marker id="tl-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" '
            'orient="auto"><path d="M1 1 L9 5 L1 9" fill="none" stroke="currentColor" stroke-width="1.5"/></marker></defs>'
            + parts + extra + "</svg>")


def rule_parts(rule, x, y, w=660):
    """A handling rule as a small decision: the question in a box, then one box per answer side by side, each with
    its title, what is done, and its example from the picture; the answer that holds today is filled. Returns
    (shapes, width, height)."""
    def lines(text, width_px, size=14):                          # wrap by words, about 0.53 em a letter
        out, cur, cap = [], "", max(8, int(width_px / (size * 0.53)))
        for word in str(text).split():
            if cur and len(cur) + 1 + len(word) > cap:
                out.append(cur)
                cur = word
            else:
                cur = f"{cur} {word}".strip()
        return out + [cur] if cur else out

    def block(tx, ty, rows, size=14, weight="normal"):
        return "".join(f'<text x="{tx}" y="{ty + k * size * 1.35}" font-size="{size}" font-weight="{weight}" '
                       f'fill="currentColor">{e(r)}</text>' for k, r in enumerate(rows))

    branches = rule.get("branches") or []
    qh = 44
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{qh}" rx="10" fill="none" stroke="currentColor" '
           'stroke-width="1.5"/>'
           f'<text x="{x + w / 2}" y="{y + 28}" text-anchor="middle" font-size="15" font-weight="600" '
           f'fill="currentColor">{e(rule.get("question", ""))}</text>']
    if not branches:
        return "".join(out), w, qh
    gap = 24
    bw = (w - gap * (len(branches) - 1)) / len(branches)
    by = y + qh + 46
    boxes = []
    for k, b in enumerate(branches):
        bx = x + k * (bw + gap)
        title, then = lines(b.get("title", ""), bw - 24, 14), lines(b.get("then", ""), bw - 24, 14)
        ex = lines(b.get("example", ""), bw - 24, 13)
        bh = 18 + len(title) * 19 + 6 + len(then) * 19 + (8 + len(ex) * 18 if ex else 0) + 14
        boxes.append((bx, title, then, ex, bh, b))
    bh = max(h for *_, h, _ in boxes)
    for bx, title, then, ex, _, b in boxes:
        fill = "#fff3bf" if b.get("today") else "none"
        out.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="10" fill="{fill}" stroke="currentColor" '
                   'stroke-width="1.5"/>')
        side = "start" if bx + bw / 2 >= x + w / 2 else "end"      # the answer beside its arrowhead, off the line
        out.append(f'<line x1="{x + w / 2}" y1="{y + qh}" x2="{bx + bw / 2}" y2="{by - 3}" stroke="currentColor" '
                   'stroke-width="1.5" marker-end="url(#tl-arrow)"/>'
                   f'<text x="{bx + bw / 2 + (12 if side == "start" else -12)}" y="{by - 10}" text-anchor="{side}" '
                   f'font-size="14" font-weight="600" fill="currentColor">{e(b.get("answer", ""))}</text>')
        ty = by + 22
        out.append(block(bx + 12, ty, title, 14, "600"))
        ty += len(title) * 19 + 6
        out.append(block(bx + 12, ty, then, 14))
        ty += len(then) * 19 + 8
        if ex:
            out.append(f'<g opacity="0.75">{block(bx + 12, ty, ex, 13)}</g>')
    return "".join(out), w, by - y + bh


def timeline_parts(spec, arrow=True):
    """One timeline's shapes, without the <svg> around them: (shapes, width, height, {span name: its box}).
    `arrow`: the time axis ends in an arrowhead (a zoomed panel draws its axis plain)."""
    items, times, bites = spec.get("items") or [], spec.get("times") or [], spec.get("bites") or []
    clock = spec.get("clock") if isinstance(spec.get("clock"), dict) else None
    if not items or not (times or clock):
        return "", 0, 0, {}
    left, top, col, row = 200, 78, 170, 62                      # left: room for the times, clear of a bite
    width = left + col * (len(items) - 1) + 120
    x = {it: left + col * k for k, it in enumerate(items)}
    if clock:                                                    # a real clock (s22 j02, JL 261021: "默认 ... by hour"):
        def mins(t):                                             # every hour the same height, each HH:MM where its
            h, m = str(t).split(":")                             # minutes put it, labels on the whole hours only
            return int(h) * 60 + int(m)
        start, end, px = mins(clock["from"]), mins(clock["to"]), float(clock.get("hour_px", 150))
        wrap = end <= start                                      # a night: 23:00 to 07:00 runs past midnight
        end += 1440 if wrap else 0
        on = lambda v: v + 1440 if wrap and v < start else v     # a time after midnight, on the night's own line
        step = int(clock.get("mark", 60))                        # minutes between labels: 60, or 180 for a whole day
        fmt = lambda v: f"{(v // 60) % 24 if wrap else v // 60:02d}:{v % 60:02d}"   # a day ends at 24:00
        hours = [fmt(v) for v in range(-(-start // step) * step, end + 1, step)]
        marks = {s.get(k) for s in spec.get("spans") or [] for k in ("from", "to")} | {b.get("at") for b in bites}
        y = {}
        for t in (marks - {None}) | set(hours):
            try:
                y[t] = top + 36 + (on(mins(t)) - start) / 60 * px
            except (ValueError, AttributeError):
                pass
        labels = {t: y[t] for t in hours}
        height = int(top + 36 + (end - start) / 60 * px + 30)
    else:
        y = {t: top + 36 + row * k for k, t in enumerate(times)}
        labels = y
        height = top + row * len(times) + 20
    out, boxes = [], {}
    out.append(f'<text x="{left + col * (len(items) - 1) / 2}" y="22" text-anchor="middle" font-size="15" '
               f'font-weight="600" fill="currentColor">{e(spec.get("items_label") or "Food items")}</text>')
    for it, cx in x.items():                                     # a lane per food item, its name on top
        out.append(f'<text x="{cx}" y="{top - 22}" text-anchor="middle" font-size="14" fill="currentColor">{e(it)}</text>'
                   f'<line x1="{cx}" y1="{top - 10}" x2="{cx}" y2="{height - 12}" stroke="currentColor" '
                   'stroke-width="2"/>')
    out.append(f'<text x="22" y="{(top + height - 20) / 2}" font-size="14" fill="currentColor" '
               f'transform="rotate(-90 22 {(top + height - 20) / 2})" text-anchor="middle">'
               f'{e(spec.get("time_label") or "Timeline")}</text>'
               f'<line x1="40" y1="{top}" x2="40" y2="{height - 14}" stroke="currentColor" stroke-width="1.5"'
               + (' marker-end="url(#tl-arrow)"' if arrow else "") + '/>')
    for t, ty in labels.items():                                 # a row per moment (on a clock, per whole hour)
        out.append(f'<text x="{left - 90}" y="{ty + 5}" text-anchor="end" font-size="14" fill="currentColor">{e(t)}</text>')
        if clock:                                                # the hour's line across the lanes, faint
            out.append(f'<line x1="{left - 80}" y1="{ty}" x2="{left + col * (len(items) - 1) + 80}" y2="{ty}" '
                       'stroke="currentColor" stroke-width="1" stroke-dasharray="2 6" opacity="0.45"/>')
    for b in bites:                                              # a bite: a band across the items it holds
        held = [x[i] for i in b.get("items") or [] if i in x]
        if not held or b.get("at") not in y:
            continue
        x0, x1, ty = min(held) - 52, max(held) + 52, y[b["at"]]
        out.append(f'<rect x="{x0}" y="{ty - 17}" width="{x1 - x0}" height="34" rx="9" fill="#fff3bf" '
                   'stroke="currentColor" stroke-width="1.5"/>'
                   f'<text x="{(x0 + x1) / 2}" y="{ty + 5}" text-anchor="middle" font-size="14" fill="#1e1e1e">'
                   f'{e(b.get("name", ""))}</text>')
    for s in spec.get("spans") or []:                            # a span: one lane over a stretch of time
        if s.get("item") not in x or s.get("from") not in y or s.get("to") not in y:
            continue
        cx, y0, y1, aside = x[s["item"]], y[s["from"]], y[s["to"]], bool(s.get("aside"))
        y0, y1 = y0 + 3, max(y1 - 3, y0 + 33)                    # from its start to its end: back to back, never overlapping
        hw = max(58, min(col / 2 - 6, len(s.get("name", "")) * 3.8 + 9))   # wide enough for its name, within its lane
        out.append(f'<rect x="{cx - hw}" y="{y0}" width="{2 * hw}" height="{y1 - y0}" rx="9" '
                   f'fill="{"#ffffff" if aside else "#fff3bf"}" stroke="currentColor" '
                   f'stroke-width="{2.5 if s.get("zoom") else 1.5}"'
                   + (' stroke-dasharray="6 5"' if aside else "") + '/>'
                   f'<text x="{cx}" y="{(y0 + y1) / 2 + 5}" text-anchor="middle" font-size="14" fill="#1e1e1e">'
                   f'{e(s.get("name", ""))}</text>')
        boxes[s.get("name", "")] = (cx - hw, y0, cx + hw, y1)
    return "".join(out), width, height, boxes


def background_html(folder):
    """A face's `## Background`, under its goal and above the tree: what the work is for, in plain words (JL 261021:
    "可以再加一个 section，比如叫 background 啥的，介绍一下我们要实现什么"). A `- ` line is a bullet (its next lines
    continue it), anything else a paragraph; **bold** and `code` keep their look. A fenced yaml block holding
    `timeline:` is drawn as a picture (timeline_svg); another fenced block shows as it is written. The words fold
    under one "BACKGROUND · N points" line, closed by default; the pictures stay in view (JL 261021: "像这种
    background，我们可以给它 hide 一下吗"). No section, nothing drawn."""
    text = section(text_of(frame.face(folder)), "Background") if folder else ""
    if not text:
        return ""

    def inline(s):
        s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", e(s.strip()))
        return re.sub(r"`([^`]+)`", r"<code>\1</code>", s)

    def prose(chunk):
        out, bullets = [], []
        for line in chunk.splitlines():
            if line.lstrip().startswith(("- ", "* ")):
                bullets.append(line.lstrip()[2:])
            elif line.strip() and bullets and line.startswith((" ", "\t")):
                bullets[-1] += " " + line.strip()
            else:
                if bullets:
                    out.append("<ul>" + "".join(f"<li>{inline(b)}</li>" for b in bullets) + "</ul>")
                    bullets = []
                if line.strip():
                    out.append(f"<p>{inline(line)}</p>")
        if bullets:
            out.append("<ul>" + "".join(f"<li>{inline(b)}</li>" for b in bullets) + "</ul>")
        return out

    words, out, figs = [], [], []                                # the words fold away; the pictures stay in view

    def flush():                                                 # pictures in a row share one line, as a day and its
        if figs:                                                 # zoom (j01, JL 261021: "zoom in ... bite1, bite2")
            out.append('<div style="display:flex;flex-wrap:wrap;gap:8px 36px;align-items:flex-start">'
                       + "".join(figs) + "</div>" if len(figs) > 1 else figs[0])
            figs.clear()

    for k, chunk in enumerate(re.split(r"^```[^\n]*\n(.*?)^```[ \t]*$", text, flags=re.M | re.S)):
        if k % 2 == 0:                                           # the prose between fences
            if chunk.strip():
                flush()
            words += prose(chunk)
            continue
        try:
            spec = yaml.load(chunk, Loader=_LOADER)
        except yaml.YAMLError:
            spec = None
        if isinstance(spec, dict) and isinstance(spec.get("timeline"), dict):
            figs.append(f'<figure style="margin:10px 0 12px;max-width:100%">{timeline_svg(spec["timeline"])}'
                        + (f'<figcaption class=mut style="font-size:12px;max-width:900px">'
                           f'{inline(spec["timeline"]["caption"])}</figcaption>' if spec["timeline"].get("caption") else "")
                        + "</figure>")
        else:
            flush()
            out.append(f"<pre>{e(chunk.rstrip())}</pre>")
    flush()
    n = sum(w.count("<li>") for w in words) or len(words)
    folded = (f'<details data-work-key="background-{e(folder.name)}"><summary class=mut style="cursor:pointer;'
              f'font-size:12px;letter-spacing:.04em">BACKGROUND · {n} point{"s" * (n != 1)}, click to read</summary>'
              + "".join(words) + "</details>") if words else ""   # folded by default (JL 261021: "background ... hide")
    return ('<div class=goal-bg style="margin:6px 0 14px;font-size:14px;line-height:1.55">'
            + folded + "".join(out) + "</div>")


def goal_cards(level, folder, root, data, mode):
    """The Goal first, as one tree like the folders (JL 261020: "like the TODO list ... Large TODO items, and small TODO
    items, and the final check list"; "你这两个合成一块儿吧 ... 像 folder 那种 structure 的 mind map"): the goal at
    the root, then each Job, its Tasks, and each deliverable, ticked from disk and never typed."""
    if level == "Block":
        states, html_ = [], ""
        for job in frame.children(folder, "Block"):
            got, kids = task_nodes(job, deliverables(job), root, data, mode, about=True)
            states += got
            icon = face_fields(job).get("emoji") or "🗂"
            html_ += node(level_head(icon, nav(job, root, mode, "Goal", e(job.name)), got, job=True), kids,
                          key="tree-" + frame.rel(job, root))
        got, kids = items_nodes(deliverables(folder), root, data)
        if got:
            states += got
            html_ += node(level_head("🧩", "Across all Jobs", got, job=True), kids, key="tree-across")
    elif level == "Job":
        states, html_ = task_nodes(folder, deliverables(folder), root, data, mode)
    else:
        job = frame.chain(folder, root).get("Job")
        states, html_ = items_nodes([i for i in deliverables(job) if task_of(i) == folder.name] if job else [], root, data)
    accepted = face_fields(folder).get("goal-status") or "not recorded"
    state = group_state(states) if states else "todo"
    head = (f'<p class=stat-line style="margin-bottom:2px">{mark(state)} <b>{e(goal(folder))}</b>'
            f'<span class=mut style="margin-left:12px">{tally(states)} delivered</span></p>')
    if not states:
        head = f'<p class=stat-line><b>🎯 {e(goal(folder))}</b></p><p class=mut>No deliverables listed yet: add a ## Deliverables list to the face.</p>'
    head += background_html(folder)
    return (part("Goal") + TREE_CSS + CSVP_CSS + '<div class=dtree-wrap>' + head + (TREE_TOOLS + f'<ul class=dtree>{html_}</ul>' if html_ else "")
            + f'<p class=mut style="font-size:12px">Goal accepted by a person: {e(accepted)}</p></div>')


def task_folders(level, folder):
    if level == "Task":
        return [folder]
    kids = frame.children(folder, level)
    return [t for j in kids for t in frame.children(j, "Job")] if level == "Block" else kids


def first_line(path):
    """A Run's own one-line result, `result/headline.txt` (frame.py's Run reader reads the same file)."""
    text = text_of(path) if path and path.is_file() else ""
    return text.strip().splitlines()[0][:240] if text.strip() else ""


_RECORDS = {}


def records(task):
    """A Task's Run records, rebuilt only when one of its Run cards or receipts changed (reading them is most of a
    page's time; a file's date is cheap to check)."""
    stamp = []
    runs = task / "runs"
    for run in sorted(runs.iterdir()) if runs.is_dir() else []:
        for f in (run / "run.yaml", run / "result/runtime.yaml", run / "result/headline.txt"):
            try:
                stamp.append((run.name, f.name, f.stat().st_mtime_ns))
            except OSError:
                pass
    face = frame.face(task)
    key = (tuple(stamp), face.stat().st_mtime_ns if face else 0)
    hit = _RECORDS.get(str(task))
    if not hit or hit[0] != key:
        hit = _RECORDS[str(task)] = (key, _records(task))
    return hit[1]


def _records(task):
    """Join cards to the shared native reader, including redirected Result stores."""
    from live.runs import local_runs
    md = frame.face(task)
    native = local_runs(md) if md else []
    by_name = {r["ticket"].stem: r for r in native if r.get("ticket")}
    result, seen = [], set()
    for row in frame.runs_of(task):
        if row["kind"] != "hard" or row["run"] in seen:
            continue
        seen.add(row["run"])
        path = row["path"]
        card = read_yaml(path / "run.yaml") if path.is_dir() else {}
        if card.get("kind") == "soft":
            continue
        source = by_name.get(row["run"], {})
        receipt_path = source.get("runtime") or (path / "result/runtime.yaml" if path.is_dir() else None)
        receipt = receipt_of(receipt_path)
        types = card.get("type") or receipt.get("operation") or source.get("operation") or []
        types = types if isinstance(types, list) else [types]
        purpose = (card.get("goal") or card.get("aim") or source.get("goal")   # excalidraw-job writes a Run's purpose as aim
                   or next((PURPOSES[t] for t in types if t in PURPOSES), ""))
        result.append(dict(row, task=task, card=card, receipt=receipt, receipt_path=receipt_path,
                           source=source, types=types, purpose=purpose,
                           status=str(receipt.get("status") or card.get("status") or "Not recorded"),
                           target=receipt.get("target") or card.get("target") or source.get("target") or "",
                           headline=receipt.get("headline") or source.get("outcome") or first_line(path / "result/headline.txt")
                           or said_of(receipt, Path(receipt_path).parent if receipt_path else None)))
    return result


def snapshot(level, folder):
    return {task: records(task) for task in task_folders(level, folder)}


def show(value):
    if value is None or value == "" or value == [] or value == {}:
        return "Not recorded"
    if isinstance(value, (dict, list)):
        return yaml.safe_dump(value, allow_unicode=True, sort_keys=False).strip()
    return str(value)


def moment(value):
    try:
        return value if isinstance(value, datetime) else datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None


def elapsed(receipt):
    start, end = moment(receipt.get("started_at")), moment(receipt.get("finished_at"))
    live = bool(start and not end and str(receipt.get("status")).lower() == "running")
    if live and start.tzinfo:
        end = datetime.now(timezone.utc)
    if not start or not end:
        return "Not recorded"
    try:
        seconds = int((end - start).total_seconds())
    except TypeError:
        return "Not recorded"
    if seconds < 0:
        return "Conflicting timestamps"
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return ("Elapsed " if live else "") + (f"{h} h " if h else "") + (f"{m} min " if m else "") + f"{s} s"


def location(receipt):
    execution = receipt.get("execution") or {}
    execution = execution if isinstance(execution, dict) else {}
    return next((receipt[k] for k in ("host", "hostname", "machine", "platform") if receipt.get(k)),
                execution.get("host") or execution.get("platform") or "Not recorded")


def address(row, root):
    chain = frame.chain(row["task"], root)
    return " / ".join([chain[k].name for k in ("Block", "Job", "Task") if k in chain] + [row["run"]])


def run_link(row, root):
    url = frame.ROUTE + "?" + urlencode({"view": "work-run", "path": frame.rel(row["task"], root), "run": row["run"]})
    return frame.pop(url, address(row, root), row["run"])


def nav(folder, root, mode, view, label):
    url = frame.ROUTE + "?" + urlencode({"path": frame.rel(folder, root), "space": mode, "sub": view})
    return frame.link(url, label)


def source_link(path, root, label=None):
    if not path or not path.is_file() or not path.resolve().is_relative_to(root.resolve()):
        return ""
    rel = frame.rel(path, root)
    url = frame.reader(path, root) if path.suffix == ".md" else "/" + "/".join(quote(p) for p in rel.split("/"))
    return frame.pop(url, label or rel, label or path.name)


def counts(rows):
    """Runs by state, five words with their icons ("complete" and "completed" are one), then any without a record."""
    tally = Counter(state_of(r) for r in rows)
    icon = {k: l.split(" ")[0] for k, l, _ in STATE}
    out = [f"{icon[k]} {tally[k]}" for k, _, _ in STATE if tally[k]]
    return " · ".join(out + ([f"no record {tally['no record']}"] if tally["no record"] else [])) or "no Runs yet"


def plan_data(folder):
    plan = read_yaml(folder / "workflow/plan.yaml")
    specs = plan.get("run_specs") or []
    return plan, [s for s in specs if isinstance(s, dict)] if isinstance(specs, list) else []


def studio(folder, root):
    """The Studio topics of this folder as the Studio lists them (JL 261022: "update this, to the same format"): one
    folded row each, its name, its tags, ↗ and its stage, opened in place to its drawing, its part drawings as rows
    inside it (frame._topic_row). A Job or Task shows the topics that name it, and the Block's s00 first."""
    block = frame.chain(folder, root).get("Block")
    if not block:
        return ""
    rows = []
    for owner, topic, drawings in frame.studio_inventory(block, root):
        background = topic.name.startswith("s00-")
        if folder != block and not background and folder.name not in text_of(frame._notes(topic)) \
                and not owner.is_relative_to(folder):
            continue
        rows.append(frame._topic_row(topic, drawings, root, owner))
    url = frame.ROUTE + "?" + urlencode({"path": frame.rel(folder, root), "studio": "1", "studio_group": "all"})
    if not rows:
        return '<p class=mut>No Studio topic for this folder yet.</p><p>' + frame.link(url, "Open the Block's Studio") + '</p>'
    return '<div class=studio-topics-lite>' + "".join(rows) + '</div><p>' + frame.link(url, "Open the Block's Studio") + '</p>'


def runs_n(n):
    return f"{n} Run" + ("" if n == 1 else "s")


def part(name):
    """A part of a view, as the Draft page parts its tabs: Operation over Result (draft_steps._part)."""
    return f'<h3 style="margin:18px 0 6px">{e(name)}</h3>'


def card(title, body, tag="", open_=False, key=""):
    """A folded card, as the Draft page's (draft_steps._fold): an emoji title, a small grey tag, the body opened."""
    return (f'<details class="topic work-task"{" open" if open_ else ""}' + (f' data-work-key="{e(key)}"' if key else "")
            + f'><summary><span class=related-head><b>{e(title)}</b>'
            + (f' <span class=mut style="font-weight:400;font-size:12.5px">{e(tag)}</span>' if tag else "")
            + f'</span></summary><div class=work-body>{body}</div></details>')


def child_rows(level, folder, root, data, mode, view):
    """One row per Job (a Block) or Task (a Job): its goal, its Tasks or Runs, its Runs by state, its last finish. The
    number columns never wrap; the goal gives way (JL 261020: "this is not readable")."""
    nw = ' style="white-space:nowrap"'
    heads = ["Job" if level == "Block" else "Task", "Goal"] + (["Tasks"] if level == "Block" else []) + [
        "Runs", "✅", "🚧", "❌", "⛔", "◌", "last finished"]
    rows = []
    for child in frame.children(folder, level):
        tasks = [t for t in data if t == child or child in t.parents]
        runs = [r for t in tasks for r in data[t]]
        c = Counter(state_of(r) for r in runs)
        when, _ = last_finish(runs)
        g = goal(child)
        cells = [(nav(child, root, mode, view, child.name), ""), (e(g if len(g) <= 120 else g[:117] + "…"), "")]
        cells += [(e(str(len(tasks))), nw)] if level == "Block" else []
        cells += [(e(str(len(runs))), nw)] + [(e(str(c[k]) if c[k] else ""), nw)
                                             for k in ("finished", "running", "failed", "blocked", "waiting")]
        cells += [(e(when[:16].replace("T", " ")) if when else "", nw)]
        rows.append("<tr>" + "".join(f"<td{st}>{v}</td>" for v, st in cells) + "</tr>")
    if not rows:
        return "<p class=mut>Nothing here yet.</p>"
    head = "".join(f"<th{nw if i > 1 else ''}>{e(h)}</th>" for i, h in enumerate(heads))
    return f"<table class=wf-table><thead><tr>{head}</tr></thead><tbody>{''.join(rows)}</tbody></table>" + LEGEND


LEGEND = ("<p class=mut>✅ finished · 🚧 running · ❌ failed · ⛔ blocked · ◌ waiting for a person to start it. Read from each "
          "Run's receipt (runtime.yaml), else its card; a finished Run is not the goal accepted.</p>")


def clock(value):
    """A receipt's time to the minute, as a reader says it (2026-10-21 01:43)."""
    return str(value)[:16].replace("T", " ") if value else "Not recorded"


ROLES = (("trial", "🧪 trial", "a small try before the full Run"),
         ("make", "🔨 make", "makes the Task's output"),
         ("fix", "🔁 retry or fix", "asks again what a Run missed, or repairs it"),
         ("check", "🔎 check", "audits or compares an output"),
         ("describe", "📋 describe", "says what an output holds"),
         ("figures", "📊 figures", "draws results as charts"),
         ("evidence", "🧾 evidence", "one value or display for a page"),
         ("publish", "📤 publish", "releases or delivers an output"))
ROLE_ORDER = {k: i for i, (k, _, _) in enumerate(ROLES)}


def role_of(row):
    """The one job a Run does in its Task (JL 261020: "各司其职"): its card's `role:`, else what its run_type says."""
    card_ = row.get("card") or {}
    role = str(card_.get("role") or {"main": "make", "figures": "figures", "delivery": "publish"}.get(str(card_.get("run_type")), ""))
    return role if role in ROLE_ORDER else "other"


def run_rows(rows, root, full=True):
    """A Task's Runs (full): grouped by role in the order a Task lives (trial, make, fix, check, describe, figures,
    evidence, publish), the role named once at the top of its group. Not full: Runs across Tasks, as a list."""
    label = dict((k, l) for k, l, _ in STATE)
    nb = lambda v: e(v).replace(" ", "&nbsp;")                               # a state or a time never breaks in two
    if not full:
        return frame.table(("Run", "Task", "Started at", "What it says"), [
            (run_link(r, root), e(r["task"].name), nb(clock(r["receipt"].get("started_at"))),
             e(str(r["receipt"].get("failure") or r["card"].get("failure") or r["headline"] or ""))[:200]) for r in rows])
    if not rows:
        return '<p class=mut>Nothing here yet.</p>'
    names = {k: (l, why) for k, l, why in ROLES}
    rows = sorted(rows, key=lambda r: (ROLE_ORDER.get(role_of(r), len(ROLES)), r["run"]))
    body, last = [], None
    for r in rows:
        role = role_of(r)
        first = role != last
        last = role
        n = sum(1 for x in rows if role_of(x) == role)
        name, why = names.get(role, ("◻ no role", "its card names no role"))
        cell = (f'<b>{nb(name)}</b> <span class=mut>{n}</span><div class=mut style="font-size:12px">{e(why)}</div>'
                if first else "")
        cells = (cell, run_link(r, root), nb(label.get(state_of(r), "no record")), e(show(location(r["receipt"]))),
                 nb(clock(r["receipt"].get("started_at"))), nb(elapsed(r["receipt"])),
                 e("" if str(r["headline"]).startswith(r["run"]) else r["headline"]))
        style = ' style="border-top:2px solid #d0d7de"' if first and body else ""
        body.append(f"<tr{style}>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>")
    head = "".join(f"<th>{h}</th>" for h in ("Role", "Run", "Status", "Where", "Started at", "Elapsed", "Key result"))
    return f"<table class=wf-table><thead><tr>{head}</tr></thead><tbody>{''.join(body)}</tbody></table>"


RUN_MARKS = ("✅", "🔶", "🚧", "❌", "📦", "⛔", "◌", "⚪")
RUN_LEGEND = ("<p class=mut style='font-size:12px'>✅ finished · 🔶 finished, some searches unanswered or its gate missed · "
              "🚧 running · ❌ failed · 📦 ran, no receipt · ⛔ blocked · ◌ planned · ⚪ no record. From each Run's receipt "
              "(runtime.yaml), else its card; an old Run's receipt is rebuilt from the files it left (work/_tools/"
              "rebuild_receipts.py). A finished Run is not the goal accepted.</p>")


def run_tally(rows):
    """How many Runs carry each mark, in one fixed order: ✅ 10 📦 13 ❌ 1."""
    c = Counter(run_mark(r).split(" ")[0] for r in rows)
    return "  ".join(f"{m} {c[m]}" for m in RUN_MARKS if c[m])


def run_node(row, root, task=False):
    """One Run on one line: its mark, its name, and only what its receipt holds: when it finished, how long it took,
    the first words of its result (JL 261021: "result 跟 go 一样的 structure"); where it ran shows on hover."""
    mark_, word = run_mark(row).split(" ", 1)
    rec = row["receipt"]
    said = str(row.get("headline") or "").split(";")[0].strip()
    said = "" if said.startswith(row["run"]) else said
    took = elapsed(rec)
    meta = ([e(row["task"].name)] if task else []) + [e(word)] + ([e(clock(rec["finished_at"]))] if rec.get("finished_at") else []) \
        + ([e(took)] if took not in ("Not recorded", "Conflicting timestamps") else []) + ([e(said[:110])] if said else [])
    tip = f"Ran on {show(location(rec))}; started {clock(rec.get('started_at'))}"
    return f'<li><span title="{e(tip)}">{mark_} {run_link(row, root)}</span>' + "".join(f"<span class=m>{m}</span>" for m in meta) + "</li>"


def role_nodes(task, rows, root):
    """A Task's Runs by the job each does (trial, make, fix, check, describe, figures, evidence, publish), each group
    folded at first."""
    groups, names, out = {}, {k: l for k, l, _ in ROLES}, ""
    for row in rows:
        groups.setdefault(role_of(row), []).append(row)
    for role in sorted(groups, key=lambda k: ROLE_ORDER.get(k, len(ROLES))):
        rs = sorted(groups[role], key=lambda r: r["run"])
        head = f'<span class=lvl>{e(names.get(role, "◻ no role"))}</span><span class=chip>{runs_n(len(rs))}  {e(run_tally(rs))}</span>'
        out += node(head, "".join(run_node(r, root) for r in rs), key=f"runs-{task.name}-{role}")
    return out


def task_picture(task, rows):
    """The picture a Task's newest finished Run drew: its preview.png (a display Run's table or figure), else its first
    .png; None when it drew none."""
    for row in sorted(rows, key=lambda r: str(r["receipt"].get("finished_at") or ""), reverse=True):
        if state_of(row) != "finished":
            continue
        res = task / "runs" / row["run"] / "result"
        res = res if res.is_dir() else task / "results" / row["run"]
        found = sorted(res.glob("*.png")) if res.is_dir() else []
        pick = next((f for f in found if f.name == "preview.png"), found[0] if found else None)
        if pick:
            return pick
    return None


def task_run_node(task, rows, root, mode):
    head = (f'<span class=lvl>📂 {nav(task, root, mode, "Execution", e(task.name))}</span>'
            f'<span class=chip>{runs_n(len(rows))}  {e(run_tally(rows))}</span>')
    # the Task's picture shows on its folded line (JL 261023: "why I cannot see the images shown by default?")
    pic = task_picture(task, rows)
    below = (f'<a href="{file_url(pic, root)}" target=_blank rel=noopener><img src="{file_url(pic, root)}" alt="{e(pic.name)}" '
             'loading=lazy style="display:block;max-width:min(100%,760px);max-height:260px;margin:4px 0 8px;'
             'border:1px solid var(--line,#e3e3e6)"></a>') if pic else ""
    return node(head, role_nodes(task, rows, root) or "<li class=m>No Runs yet.</li>", key="runs-" + frame.rel(task, root),
                below=below)


def status_tree(level, folder, root, data, mode):
    """Every Run as one tree like the Goal's: Job, Task, the job a Run does, the Run (JL 261021: "result 跟 go 一样的
    structure 可以吗？")."""
    every = [r for rs in data.values() for r in rs]
    if level == "Block":
        html_ = ""
        for job in frame.children(folder, "Block"):
            tasks = [t for t in data if job in t.parents]
            runs = [r for t in tasks for r in data[t]]
            head = (f'<span class="lvl job">{face_fields(job).get("emoji") or "🗂"} {nav(job, root, mode, "Execution", e(job.name))}</span>'
                    f'<span class=chip>{runs_n(len(runs))}  {e(run_tally(runs))}</span>')
            html_ += node(head, "".join(task_run_node(t, data[t], root, mode) for t in tasks), key="runs-" + frame.rel(job, root))
    elif level == "Job":
        html_ = "".join(task_run_node(t, rows, root, mode) for t, rows in data.items())
    else:
        html_ = role_nodes(folder, data.get(folder, []), root)
    head = f'<p class=stat-line style="margin-bottom:2px"><b>📊 {runs_n(len(every))}</b><span class=mut style="margin-left:12px">{e(run_tally(every))}</span></p>'
    return TREE_CSS + '<div class=dtree-wrap>' + head + TREE_TOOLS + f'<ul class=dtree>{html_}</ul>' + RUN_LEGEND + '</div>'


def hot_runs(every, root):
    """What runs now and what failed, each a short list of one-line Runs with their Task."""
    out = ""
    for k, title in (("running", "🚧 Running now"), ("failed", "❌ Failed")):
        rows = [r for r in every if state_of(r) == k]
        body = f'<ul class=dtree>{"".join(run_node(r, root, task=True) for r in rows)}</ul>' if rows else "<p class=mut>None.</p>"
        out += card(f"{title} · {len(rows)}", body, "" if rows else "none", key=k)
    return out


def status_cards(level, folder, root, data, mode):
    """The Result part every view opens with: every Run as a tree, then what runs now and what failed."""
    every = [r for rs in data.values() for r in rs]
    return status_tree(level, folder, root, data, mode) + hot_runs(every, root)


def goal_view(level, folder, root, data, mode):
    report = read_yaml(folder / "workflow/report.yaml")
    summary = report.get("summary")
    body = goal_cards(level, folder, root, data, mode)
    body += part("Result") + status_cards(level, folder, root, data, mode)
    body += card("📌 Current conclusion and next step",
                 '<pre>' + e(show(summary)) + '</pre>' if summary else
                 '<p>No summary saved yet (workflow/report.yaml). ' + nav(folder, root, mode, "Results", "Read the results") + '</p>',
                 "saved" if summary else "not saved", key="conclusion")
    return body + part("Studio") + studio(folder, root)        # its own part, open (JL 261022: "the Studio section")


def plan_view(level, folder, root, data, mode):
    plan, specs = plan_data(folder)
    body = part("Operation")
    if specs:
        rows = [(e(s.get("id", "")), e(show(s.get("purpose") or s.get("goal"))), e(show(s.get("input"))),
                 e(show(s.get("result") or s.get("target"))), e(show(s.get("depends_on"))), e(show(s.get("exit_gate")))) for s in specs]
        saved = ('<p>' + source_link(folder / "workflow/plan.yaml", root, "Open the saved plan") + '</p>'
                 + frame.table(("Work item", "Purpose", "Input", "Output", "Dependencies", "Completion criteria"), rows))
    else:
        saved = '<p class=mut>No workflow/plan.yaml saved. The Result below indexes what exists; it is not an execution order.</p>'
    body += card("📋 Saved plan", saved, f"{len(specs)} work items" if specs else "none saved", open_=bool(specs), key="plan")
    if level == "Task":
        files = [p for pattern in ("scripts/**/*", "workflow/**/*", "tests/**/*", "CODE_REVIEW.md", "notebooks/*.ipynb")
                 for p in sorted(folder.glob(pattern)) if p.is_file() and not any(
                     part_.startswith(".") or part_ == "__pycache__" for part_ in p.relative_to(folder).parts)]
        body += card("🔧 Build · code, configuration and checks", '<ul>' + ''.join(
            '<li>' + source_link(p, root, p.relative_to(folder).as_posix()) + '</li>' for p in files) + '</ul>',
            f"{len(files)} files", key="build")
    body += part("Result")
    if level == "Task":
        roles = {k: l for k, l, _ in ROLES}
        rows = [(e(roles.get(role_of(r), "◻ no role")), run_link(r, root),
                 e(r["purpose"] or "Not specified. Open the Run to read its inputs and results."),
                 e(show(r["card"].get("close") or r["receipt"].get("close"))))
                for r in sorted(data[folder], key=lambda r: (ROLE_ORDER.get(role_of(r), len(ROLES)), r["run"]))]
        body += card(f"🏃 Runs and their purposes · {len(rows)}", frame.table(("Role", "Run", "Purpose", "Completion criteria"), rows),
                     counts(data[folder]), open_=True, key="purposes")
    else:
        kids = frame.children(folder, level)
        body += card(f"🗂 {'Jobs' if level == 'Block' else 'Tasks'} · {len(kids)}", child_rows(level, folder, root, data, mode, "Plan"),
                     "how the work is divided", open_=True, key="children")
    return body


def execution_view(level, folder, root, data):
    every = [r for rs in data.values() for r in rs]
    return (part("Result") + hot_runs(every, root) + status_tree(level, folder, root, data, "Audience Report")
            + '<p class=mut>Status comes from Run records, not a process health check.</p>')


def results_view(level, folder, root, data, mode, theme):
    body = part("Operation")
    report = folder / "workflow/report.yaml"
    body += card("📝 Result interpretation", '<p>' + source_link(frame.face(folder), root, "Open the description and its interpretation")
                 + '</p><p class=mut>Interpretations stay on their pages; the numbers below come from Runs and change no conclusion.</p>',
                 key="interpretation")
    body += card("🧾 Execution report", '<p>' + (source_link(report, root) or "No workflow/report.yaml saved") + '</p>',
                 "saved" if report.is_file() else "not saved", key="report")
    body += part("Result")
    for task, rows in data.items():
        chain = frame.chain(task, root)
        name = " / ".join(chain[k].name for k in ("Job", "Task") if k in chain) or task.name
        content = frame.table(("Run", "Key result", "Source"), [
            (run_link(r, root), e(r["headline"] or "No result summary recorded"),
             source_link(r["receipt_path"], root, "Run record") or "Not recorded") for r in sorted(rows, key=lambda r: r["run"])])
        # the pictures the Runs drew, shown and not only linked (JL 261023: "how do I see all the tables?");
        # a display Run writes preview.png and figure.png of the same picture, so the preview stands for both
        pics = []
        for r in sorted(rows, key=lambda r: r["run"]):
            res = task / "runs" / r["run"] / "result"
            res = res if res.is_dir() else task / "results" / r["run"]
            found = sorted(res.glob("*.png")) if res.is_dir() else []
            preview = [f for f in found if f.name == "preview.png"]
            pics += (preview or found)[:4]
        if pics:
            content += "".join(
                f'<figure style="margin:10px 0"><a href="{file_url(f, root)}" target=_blank rel=noopener><img src="{file_url(f, root)}" '
                f'alt="{e(f.name)}" loading=lazy style="max-width:100%;max-height:640px;border:1px solid var(--line)"></a>'
                f'<figcaption class=mut style="font-size:12.5px">{e(f.parent.parent.name)} · {e(f.name)}</figcaption></figure>'
                for f in pics[:8])
        content += '<p>' + source_link(frame.face(task), root, "Read the Task's interpretation") + '</p>'
        with_head = sum(1 for r in rows if r["headline"])
        # a Task's pictures show open at every level: a Job of displays reads at a glance (JL 261023, j21_paper_displays:
        # "these displays don't show the big result at a glance")
        body += card(f"📊 {name}", content, f"{with_head} of {runs_n(len(rows))} with a key result",
                     open_=level == "Task" or bool(pics),
                     key="res-" + frame.rel(task, root))
    return body + card("❓ Questions and reports", frame.report_view(level, folder, root, theme), key="questions")


# A picture opens over the page, not in a new tab (JL 261023: "pop out, not a new link"). One listener on the document,
# so it keeps working after the 20-second refresh swaps the section; Cmd/Ctrl-click still opens the file in a tab.
ZOOM = """<style>.wz-pop{position:fixed;inset:0;z-index:9999;background:rgba(20,20,20,.82);display:flex;align-items:center;
justify-content:center;cursor:zoom-out}.wz-pop img{max-width:96vw;max-height:94vh;background:#fff;box-shadow:0 6px 30px #0008;
border-radius:4px}.workflow-view img,figure img,a[href$='.png'] img{cursor:zoom-in}</style><script>(function(){
if(window.__wzPop)return;window.__wzPop=1;const pic=/\\.(png|jpe?g|gif|svg|webp)(\\?|#|$)/i;
document.addEventListener('click',ev=>{
 const img=ev.target.closest&&ev.target.closest('img');if(!img||img.closest('.wz-pop'))return;
 if(ev.metaKey||ev.ctrlKey||ev.shiftKey||ev.button)return;
 const a=img.closest('a'),href=a?a.getAttribute('href')||'':'';
 if(a?!pic.test(href):!img.closest('.workflow-view,figure'))return;
 ev.preventDefault();const box=document.createElement('div');box.className='wz-pop';
 const big=document.createElement('img');big.src=a?a.href:img.src;big.alt=img.alt;box.appendChild(big);
 const close=()=>{box.remove();document.removeEventListener('keydown',key)};
 const key=e=>{if(e.key==='Escape')close()};box.addEventListener('click',close);document.addEventListener('keydown',key);
 document.body.appendChild(box);
});})();</script>"""


REFRESH = """<script>(function(){
let timer;const selector='[data-work-progress]';
async function refresh(){
 if(document.hidden){timer=setTimeout(refresh,20000);return;}
 const current=document.querySelector(selector);if(!current)return;
 if(current.contains(document.activeElement)&&/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName)){
  timer=setTimeout(refresh,20000);return;}
 const opened=[...current.querySelectorAll('details[open][data-work-key]')].map(el=>el.dataset.workKey);
 try{const response=await fetch(location.href,{cache:'no-store'});if(!response.ok)throw Error();
  const doc=new DOMParser().parseFromString(await response.text(),'text/html');const next=doc.querySelector(selector);
  if(!next)throw Error();next.querySelectorAll('details[data-work-key]').forEach(el=>el.open=opened.includes(el.dataset.workKey));
  current.replaceWith(next);
 }catch(err){const status=current.querySelector('[data-work-refresh]');if(status)status.textContent='Refresh failed; showing the last records';}
 timer=setTimeout(refresh,20000);
}
timer=setTimeout(refresh,20000);window.addEventListener('pagehide',()=>clearTimeout(timer),{once:true});
})();</script>"""


STATE = (("running", "🚧 running", ("running", "started", "in_progress")),
         ("finished", "✅ finished", ("complete", "completed", "done", "ok", "passed")),
         ("partial", "🔶 partial", ("partial",)),      # some rows stored, the rest not (b02's binder writes it)
         ("failed", "❌ failed", ("failed", "error", "crashed")),
         ("blocked", "⛔ blocked", ("blocked",)),
         ("waiting", "◌ waiting", ("proposed", "ready", "queued", "planned")))


def state_of(row):
    """A Run's recorded status, in one of five words (or no record): what its receipt or card says, never guessed."""
    s = str(row.get("status") or "").strip().lower()
    return next((k for k, _, words in STATE if s in words), "no record")


def last_finish(rows):
    done = [(str(r["receipt"].get("finished_at") or ""), r["run"]) for r in rows if r["receipt"].get("finished_at")]
    return max(done) if done else ("", "")


def status_board(level, folder, root, data=None):
    """The Description's status (JL 261020: "show the status of each jobs and runs here ... what runs are running, and
    what runs are finished"): the Result cards every view opens with."""
    return part("Status") + status_cards(level, folder, root, data if data is not None else snapshot(level, folder), "Audience Report")


def spaces(level, folder, root, sub, theme):
    selected = sub if sub in VIEWS else "Goal"
    data = snapshot(level, folder)
    out = {}
    for mode in MODES:
        if selected == "Goal":
            body = goal_view(level, folder, root, data, mode)
        elif selected == "Plan":
            body = plan_view(level, folder, root, data, mode)
        elif selected == "Execution":
            body = execution_view(level, folder, root, data)
        else:
            body = results_view(level, folder, root, data, mode, theme)
        live = selected in ("Goal", "Execution")
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        stamp = f'<p class=mut data-work-refresh>Last read at {timestamp} · Refreshes every 20 seconds</p>' if live else ''
        body = re.sub(r"<table(?=[\s>])", "<div class=work-table-scroll><table", body).replace('</table>', '</table></div>')   # every table, classed or not, so each wrap closes
        body = f'<section class=workflow-view data-work-progress="{e(selected)}">{stamp}{body}</section>' + (REFRESH if live else '') + ZOOM
        label, verb = {"Goal": ("Define the goal and completion criteria", "plan"), "Plan": ("Create a run plan", "plan"),
                       "Execution": ("Execute the plan", "execute"), "Results": ("Write the result interpretation", "report")}[selected]
        prompt = (f"/haipipe-task {verb} {{folder}}" if level == "Task" else
                  f"Read {{folder}} and its Tasks. {label}. Preserve each Task's own plan, Runs and results.")
        run_name = "rNN_<slug>" if verb == "execute" else f"run-{verb}-{folder.name.split('_')[0]}"
        kinds = (frame.run_type(run_name, label, prompt, "haipipe-task"),)
        if selected == "Plan" and mode == "Work Details":
            kinds += (frame.run_type(f"run-build-{folder.name.split('_')[0]}", "Prepare code and configuration for the plan",
                                     "/haipipe-task build {folder}" if level == "Task" else
                                     "Build the planned Tasks under {folder} through each Task's own workflow.", "haipipe-task"),)
        if mode == "Audience Report":
            kinds = (frame.run_type(f"run-report-{folder.name.split('_')[0]}", "Update the result interpretation",
                                   "Read {folder} and its source records. Explain what the results establish and what remains open.", "haipipe-task"),)
        out[mode] = frame.Space(html=body, subspaces=VIEWS, open=selected, run_types=kinds, page=True,
                               disk=(("workflow/", "saved plan and report, when present"),
                                     ("runs/", "existing Run cards and receipts")))
    md = frame.face(folder)                                                  # Description: the face, then its status
    if md:
        rows = [(e(k), e(v)) for k, v in frame._fields(md)]
        desc = (f'<h2>{e(frame._title(md))}</h2><p class=mut>{frame.link(frame._reader(md, root), frame._rel(md, root))}</p>'
                + (frame._table(("field", "value"), rows) if rows else ""))
        head, fields = desc.split("<table", 1) if "<table" in desc else (desc, "")
        out["Description"] = frame.Space(html=head + goal_cards(level, folder, root, data, "Audience Report")
                                         + status_board(level, folder, root, data)
                                         + (part("Face fields") + "<table" + fields if fields else "") + REFRESH + ZOOM)
    return out


IMAGES = (".png", ".jpg", ".jpeg", ".svg", ".gif", ".webp")
TEXTS = (".json", ".yaml", ".yml", ".txt")


def file_url(path, root):
    return "/" + "/".join(quote(part) for part in frame.rel(path, root).split("/"))


def csv_preview(path, n=12):
    """A CSV's first rows as a table, and how big it is (JL 261021: "why I cannot do the preview of the csv")."""
    import csv
    import itertools
    try:
        with path.open(newline="", encoding="utf-8", errors="replace") as fh:
            rows = list(itertools.islice(csv.reader(fh), n + 1))
        total = sum(1 for _ in path.open(encoding="utf-8", errors="replace")) - 1 if path.stat().st_size < 30_000_000 else None
    except (OSError, csv.Error):
        return 0, 0, "<p class=mut>Could not read this file.</p>"
    if not rows:
        return 0, 0, "<p class=mut>Empty file.</p>"
    return total, len(rows[0]), rows_table(rows[0], rows[1:])


CSVP_CSS = ("<style>.csvp-wrap{overflow-x:auto;margin:4px 0 10px}"
            ".csvp{margin:0;width:auto}.csvp th,.csvp td{white-space:nowrap;padding:4px 10px;font-size:12.5px}"
            ".csvp th{position:sticky;top:0;background:var(--wash)}.csvp tr:nth-child(even) td{background:var(--wash)}"
            ".dossier{color:var(--fg);font-size:13px;line-height:1.5}.dossier h1{font-size:17px;margin:0 0 6px}"
            ".dossier h2{font-size:14px;margin:12px 0 4px}.dossier ul{margin:2px 0 6px;padding-left:18px;list-style:disc}"
            ".dtree .dossier li{padding:0;line-height:1.5}.dtree .dossier li::before,.dtree .dossier li::after{display:none}</style>")
NUMBER = re.compile(r"^-?[\d,]*\.?\d+(e-?\d+)?%?$")


def rows_table(header, rows):
    """A table that reads: one line per cell, a long value cut with its whole text on hover, numbers to the right
    (JL 261021: "things here is so hard to read")."""
    def cell(v, tag="td"):
        v = "" if v is None else str(v)
        short = v if len(v) <= 48 else v[:45] + "…"
        right = ' style="text-align:right"' if tag == "td" and NUMBER.match(v.strip() or "x") else ""
        return f'<{tag}{right} title="{e(v)}">{e(short)}</{tag}>'
    head = "".join(cell(h, "th") for h in header)
    body = "".join("<tr>" + "".join(cell(v) for v in r) + "</tr>" for r in rows)
    return f'<div class=csvp-wrap><table class="wf-table csvp"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def parquet_rows(path, n=12):
    """A data table's first rows and its size, read without loading the whole file."""
    try:
        import pyarrow.parquet as pq
        f = pq.ParquetFile(path)
        batch = next(f.iter_batches(batch_size=n), None)
        rows = batch.to_pylist() if batch is not None else []
        return f.metadata.num_rows, f.schema_arrow.names, [[r.get(c) for c in f.schema_arrow.names] for r in rows]
    except Exception:                                              # an unreadable file shows as unreadable, never breaks the page
        return None, [], []


def data_tables(row, root):
    """The data tables a Run's page shows rows of (JL 261021: "could you show some data rows as well?"): the tables
    it wrote (its heavy.yaml), and for a Run that describes a table, that table."""
    res = row["path"] / "result" if row.get("path") else None
    out = [root / str(h["path"]) for h in (read_yaml(res / "heavy.yaml").get("heavy") or [] if res else [])
           if isinstance(h, dict) and str(h.get("path", "")).endswith(".parquet")]
    if role_of(row) == "describe":
        out += [root / str(x) for x in row["card"].get("reads") or [] if str(x).endswith(".parquet") and "{" not in str(x)]
    seen = []
    return [p for p in out if p.is_file() and not (p in seen or seen.append(p))]


def data_section(row, root):
    tables = data_tables(row, root)
    if not tables:
        return ""
    out = f"<h3>Data rows · {len(tables)}</h3>"
    for path in tables:
        total, names, rows = parquet_rows(path)
        size = f"{total:,} rows × {len(names)} columns, first {len(rows)} shown" if total is not None else "could not be read"
        out += (f'<details open data-work-key="rows-{e(path.name)}"><summary><b>{e(path.name)}</b> <span class=mut>{e(size)}</span>'
                f'<div class=mut style="font-size:12px">{e(frame.rel(path, root))}</div></summary>'
                + (rows_table(names, rows) if rows else "") + "</details>")
    return out


def outputs(files, root):
    """A Run's outputs shown, not only linked: figures as pictures, tables as their first rows, small text files and the
    log folded in place; a page (.md, .html) opens in its reader."""
    figs = [p for p in files if p.suffix.lower() in IMAGES]
    csvs = [p for p in files if p.suffix.lower() == ".csv"]
    texts = [p for p in files if p.suffix.lower() in TEXTS]
    logs = [p for p in files if p.suffix.lower() == ".log"]
    pages = [p for p in files if p not in figs + csvs + texts + logs]
    out = CSVP_CSS
    if figs:
        out += f"<h3>Figures · {len(figs)}</h3><div style=\"display:grid;grid-template-columns:repeat(auto-fill,minmax(380px,1fr));gap:16px\">"
        out += "".join(f'<figure style="margin:0"><a href="{file_url(f, root)}" target=_blank rel=noopener><img src="{file_url(f, root)}" '
                       f'alt="{e(f.name)}" loading=lazy style="width:100%;border:1px solid var(--line);border-radius:8px;background:#fff"></a>'
                       f'<figcaption class=mut style="font-size:12.5px;margin-top:4px">{e(f.name)}</figcaption></figure>' for f in figs) + "</div>"
    if csvs:
        out += f"<h3>Tables · {len(csvs)}</h3>"
        for n, f in enumerate(csvs):
            total, cols, table = csv_preview(f)
            size = (f"{total:,} rows × {cols} columns" if total is not None else f"{cols} columns") + (", first 12 shown" if total and total > 12 else "")
            out += (f'<details{" open" if n < 3 else ""} data-work-key="csv-{e(f.name)}"><summary><b>{e(f.name)}</b> '
                    f'<span class=mut>{e(size)}</span> <a href="{file_url(f, root)}" target=_blank rel=noopener>open</a></summary>{table}</details>')
    if pages:
        out += "<h3>Pages</h3><ul>" + "".join(f"<li>{source_link(f, root)}</li>" for f in pages) + "</ul>"
    if texts or logs:
        out += "<h3>Records and logs</h3>"
        for f in texts + logs:
            text = text_of(f)
            text = "\n".join(text.splitlines()[-60:]) if f.suffix == ".log" else text[:4000]
            out += (f'<details data-work-key="txt-{e(f.name)}"><summary><b>{e(f.name)}</b> '
                    f'<span class=mut>{"last 60 lines" if f.suffix == ".log" else ""}</span></summary><pre>{e(text)}</pre></details>')
    return out


def browse_url(folder, root, item, **keys):
    q = {"view": "work-browse", "path": frame.rel(folder, root), "item": item}
    q.update({k: v for k, v in keys.items() if v not in (None, "")})
    return frame.ROUTE + "?" + urlencode(q)


def _parquet(path, columns=None):
    import pyarrow.parquet as pq
    return kept(("pq", str(path), path.stat().st_mtime_ns, tuple(columns or ())),
                lambda: pq.read_table(path, columns=columns, partitioning=None), seconds=600)


def fact(column, value):
    """A card's value said with its unit, so a bare number never stands alone: 58 years, 13 reviews."""
    text = str(value).replace(",", ", ") if column.endswith("_list") else str(value)
    if column.endswith("_years"):
        return f"{text} years"
    if "review_count" in column:
        return f"{text} review" + ("" if text == "1" else "s")
    return text


def render_browse(folder, root, get):
    """The finished set a deliverable describes, browsed like the site it is (JL 261021: "我在哪里可以看到我最终的 Virtual
    Set 的成品呢？"): its index level by level (state, city, page), a page's records as cards, one record whole. Its
    `browse:` spec names the set's folder, its index, the index's keys and the record's text and picture fields.
    Returns (body, content type); a picture is sent as its bytes."""
    try:
        n = int(get("item") or 0)
        item = deliverables(folder)[n]
    except (ValueError, IndexError):
        return None, ""
    spec = item.get("browse") or {}
    site = root / str(spec.get("root") or "")
    index = site / str(spec.get("index") or "")
    if not spec or not index.is_file() or not site.resolve().is_relative_to(root.resolve()):
        return None, ""
    keys = spec.get("keys") or ["state", "city", "specialty"]
    man = _parquet(index).to_pandas()
    picked = [get(k) for k in keys]
    count = spec.get("count")
    if all(picked):                                      # one page: its records
        hit = man
        for k, v in zip(keys, picked):
            hit = hit[hit[k] == v]
        if hit.empty:
            return None, ""
        page = site / str(hit.iloc[0][spec.get("file", "file_path")])
        if not page.resolve().is_relative_to(site.resolve()):
            return None, ""
        table = _parquet(page)
        if get("img") not in (None, ""):                 # a record's picture, as bytes
            row = table.slice(int(get("img")), 1).to_pylist()
            pic = row[0].get(spec.get("image")) if row else None
            return (pic, str(row[0].get("portrait_content_type") or "image/jpeg")) if pic else (None, "")
    title = "Browse · " + item["what"]
    trail = [frame.link(browse_url(folder, root, n), "All")]
    for i, k in enumerate(keys):
        if picked[i]:
            trail.append(frame.link(browse_url(folder, root, n, **dict(zip(keys[:i + 1], picked[:i + 1]))), e(picked[i])))
    body = f'<h1>{e(title)}</h1><p class=mut>{" › ".join(trail)} · {e(short_folder(item, frame.rel(site, root), root))}</p>'
    level = next((i for i, v in enumerate(picked) if not v), len(keys))
    if level < len(keys):                                # a level of the index: its values, with pages and records
        sub = man
        for k, v in zip(keys[:level], picked[:level]):
            sub = sub[sub[k] == v]
        g = sub.groupby(keys[level]).agg(pages=(keys[level], "size"), **({"records": (count, "sum")} if count in sub else {}))
        g = g.sort_values("records" if "records" in g else "pages", ascending=False)
        links = "".join(
            f'<a class=bw-item href="{e(browse_url(folder, root, n, **dict(zip(keys[:level + 1], picked[:level] + [name]))))}" '
            f'data-name="{e(str(name).lower())}"><b>{e(name)}</b><span class=mut>'
            + (f'{int(r.records):,} physicians · ' if "records" in g else "") + f'{int(r.pages):,} pages</span></a>'
            for name, r in g.iterrows())
        body += (f'<p><input class=bw-find placeholder="Find a {e(keys[level])}" oninput="const q=this.value.toLowerCase();'
                 f'document.querySelectorAll(\'.bw-item\').forEach(a=>a.style.display=a.dataset.name.includes(q)?\'\':\'none\')"> '
                 f'<span class=mut>{len(g):,} {e(keys[level])} values</span></p><div class=bw-grid>{links}</div>')
    else:                                                # one page: its records as cards, then one whole
        start = int(get("from") or 0)
        cols = [c for c in spec.get("card") or [] if c in table.schema.names]
        rows = table.select(cols).slice(start, 60).to_pylist()
        chosen = get("row")
        if chosen not in (None, ""):
            full = table.slice(int(chosen), 1).to_pylist()[0]
            from live import page_reader
            pic = f'<img src="{e(browse_url(folder, root, n, **dict(zip(keys, picked)), img=chosen))}" style="width:140px;flex:none">' \
                if full.get(spec.get("image")) else ""
            body += ('<h2>One record, whole</h2><div style="display:flex;gap:18px;align-items:flex-start">' + pic
                     + f'<div class=dossier style="flex:1;min-width:0">{page_reader.markdown_html(str(full.get(spec.get("record")) or ""))}</div></div>'
                     + f'<details><summary><b>All {len(full)} fields</b></summary>'
                     + rows_table(("field", "value"), [(k, v) for k, v in full.items() if not isinstance(v, (bytes, bytearray))])
                     + "</details>")
        cards = ""
        for i, r in enumerate(rows, start):
            link = browse_url(folder, root, n, **dict(zip(keys, picked)), row=i, **({"from": start} if start else {}))
            img = browse_url(folder, root, n, **dict(zip(keys, picked)), img=i)
            label = e(str(r.get(cols[0]) if cols else i))
            facts = " · ".join(e(fact(c, r[c])) for c in cols[1:] if r.get(c) not in (None, "", "Not reported in the held sources"))
            cards += (f'<a class=bw-card href="{e(link)}"><img loading=lazy src="{e(img)}" alt="" onerror="this.style.visibility=\'hidden\'">'
                      f'<span><b>{label}</b><br><span class=mut>{facts}</span></span></a>')
        more = (f'<p>{frame.link(browse_url(folder, root, n, **dict(zip(keys, picked)), **{"from": start + 60}), "Next 60 ▸")}</p>'
                if start + 60 < table.num_rows else "")
        body += f'<h2>{table.num_rows:,} records on this page</h2><div class=bw-cards>{cards}</div>{more}'
    css = ("<style>.bw-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:6px 14px}"
           ".bw-item{display:flex;justify-content:space-between;gap:8px;padding:4px 2px;text-decoration:none;color:var(--fg)}"
           ".bw-item:hover b{text-decoration:underline}.bw-find{font:inherit;padding:4px 10px;border:1px solid var(--line);border-radius:999px;width:260px}"
           ".bw-cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:10px 16px}"
           ".bw-card{display:flex;gap:10px;align-items:flex-start;text-decoration:none;color:var(--fg);padding:4px}"
           ".bw-card img{width:48px;height:64px;object-fit:cover;flex:none;background:var(--wash)}.bw-card:hover b{text-decoration:underline}</style>")
    page_html = ('<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">'
                 f'<title>{e(title)}</title><style>' + frame.CSS + frame.WORK_CSS + '</style>' + CSVP_CSS + css
                 + '</head><body><main>' + body + '</main></body></html>')
    return page_html, "text/html; charset=utf-8"


def render_run(folder, root, name):
    """One exact Run; name is matched against records, never used as a path."""
    row = next((r for r in records(folder) if r["run"] == name), None)
    if row is None:
        return None
    receipt, card = row["receipt"], row["card"]
    title = address(row, root)
    body = '<h1>' + e(title) + '</h1><p>' + nav(folder, root, "Audience Report", "Execution", "Back to Task · Execution") + '</p>'
    body += '<h2>Goal · Purpose and inputs</h2>' + frame.table(("Field", "Value"), [
        ("Purpose", e(row["purpose"] or "Not recorded separately")), ("Target / version", e(row["target"])),
        ("Input", '<pre>' + e(show(receipt.get("inputs") or card.get("inputs"))) + '</pre>'),
        ("Completion criteria", e(show(card.get("close") or receipt.get("close"))))])
    body += '<h2>Execution · Run record</h2>' + frame.table(("Field", "Value"), [
        ("Status", e(row["status"])), ("Execution location", e(show(location(receipt)))),
        ("Started at", e(show(receipt.get("started_at")))), ("Finished at", e(show(receipt.get("finished_at")))),
        ("Elapsed time", e(elapsed(receipt))), ("Progress", e(show(receipt.get("progress")))),
        ("Worker", e(show(receipt.get("worker") or card.get("agent")))),
        ("Code revision", e(show(receipt.get("git_sha")))), ("Exit code", e(show(receipt.get("exit_code")))),
        ("Error", e(show(receipt.get("failure"))))])
    if row["source"].get("audit"):
        body += '<h3>Record checks</h3><ul>' + ''.join('<li>' + e(note) + '</li>' for note in row["source"]["audit"]) + '</ul>'
    body += '<h2>Results · Findings and interpretation</h2><p>' + e(row["headline"] or "No result summary recorded") + '</p>'
    if "asset-parity" in row["types"]:
        body += '<p>The parity check establishes whether frozen answers match the corresponding service. It does not establish answer accuracy.</p>'
    body += '<p>' + source_link(frame.face(folder), root, "Read the full Task interpretation") + '</p>'
    result = row["source"].get("result_path")
    if not result and row["path"].is_dir():
        result = row["path"] / "result"
    files = []
    if result and result.is_dir() and result.resolve().is_relative_to(root.resolve()):
        files = [p for p in sorted(result.iterdir()) if p.is_file() and not p.is_symlink()][:60]
    body += data_section(row, root) + outputs(files, root)
    body += '<details data-work-key=passes><summary>Passes · Execution attempts within this Run</summary><pre>' + e(show(card.get("passes"))) + '</pre></details>'
    stamp = '<p class=mut data-work-refresh>Last read at ' + datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC') + ' · Refreshes every 20 seconds</p>'
    body = '<section class=workflow-view data-work-progress=Run>' + stamp + body + '</section>' + REFRESH + ZOOM
    return ('<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">'
            '<title>' + e(title) + '</title><style>' + frame.CSS + frame.WORK_CSS
            + '</style></head><body><main>' + body + '</main></body></html>')

