"""The Task home and the Discovery home a paper Board draws on: the Block, Job, Task folder scans, the
bNN.jNN.tNN addresses, what the paper claims, and links into those folders.
Moved from paper.py, which re-exports the names its callers import from there (`from live.paper import ...`)."""
import os
import re
from pathlib import Path
from urllib.parse import urlencode

from src.themes import kind_of as theme_kind_of, theme_dirs

from live.paper_text import esc, outline_url, read, scalar


_ADDR_RE = re.compile(r"\bb(\d{2})(?:[.\s_-]?j(\d{2}))?(?:[.\s_-]?t(\d{2}))?(?:[.\s_-]?r(\d{2}))?\b")


_TASK_HOMES = ("work", "tasks", "task")  # the work Theme; one Project says tasks/, another task/
_SKIP_DIRS = {"src", "sbatch", "results", "runs", "scripts", "notebooks", "workflow",
              "QA", "board", "diagram", "config", "configs", "tests", "_tools"}
_TICKET_EXT = {".sh", ".ps1", ".cmd"}          # .cmd: a desktop where only cmd.exe runs (REACH SAFER)
_CODE_EXT = (".py", ".do", ".R")


def _head_field(path, key):
    """`key: value` in the first 40 lines of a task page (task-table's rule)."""
    try:
        for line in path.read_text(errors="replace").splitlines()[:40]:
            m = re.match(r"^%s:\s*(.*?)\s*$" % re.escape(key), line)
            if m:
                return m.group(1)
    except OSError:
        pass
    return None


def _headline(script):
    """First docstring or comment sentence of a script, at most 140 chars."""
    try:
        text = script.read_text(errors="replace")
    except OSError:
        return ""
    doc = ""
    if script.suffix == ".py":
        m = re.search(r'^\s*(?:r|u)?("""|\'\'\')(.*?)\1', text, re.S)
        doc = m.group(2) if m else ""
    else:
        for line in text.splitlines()[:15]:
            t = line.strip()
            if t.startswith(("//", "*", "#")) and not t.startswith("#!"):
                doc = t.lstrip("/*# ").strip().lstrip("=-*#").strip()
                if doc:
                    break
    para = []
    for l in doc.splitlines():
        if not l.strip():
            if para:
                break
            continue
        para.append(l.strip())
    line = re.sub(r"^[a-z]?\d{2}_\S+\s*[—:-]\s*", "", " ".join(para)).strip()
    m = re.match(r"^(.{20,}?[.!?])(?=\s+[A-Z(\[]|\s*$)", line)
    line = m.group(1) if m else line
    if len(line) < 12 or "===" in line or re.match(r"^\d+[.)]\s", line):
        return ""                     # a section marker or a stub is not what a task develops
    return line if len(line) <= 140 else line[:137] + "…"


def _run_state(receipts):
    """runtime.yaml `status:` values folded to done · running · failed · planned."""
    c = {}
    for st in receipts:
        t = (st or "?").lower()
        k = ("done" if t in ("complete", "completed", "done", "ok", "success") else
             "running" if "run" in t else "failed" if "fail" in t or "error" in t else
             "planned" if t in ("planned", "ready", "held", "hold") else t)
        c[k] = c.get(k, 0) + 1
    return c


def _fmt_state(c):
    if not c:
        return "no receipts"
    order = ("done", "running", "failed", "planned")
    keys = [k for k in order if k in c] + sorted(k for k in c if k not in order)
    return " · ".join("%s %d" % (k, c[k]) for k in keys)


def _scan_task(job, name, tdir):
    """One Task, in either shape: `<job>/<task>/` (Stata dialect, its own
    runs/ results/ scripts/) or the flat `<job>/{runs,results,scripts}/<task>/`."""
    if tdir is not None:
        page = tdir / (name + ".md")
        runs_dir, res_dir, code_dir = tdir / "runs", tdir / "results", tdir / "scripts"
    else:
        page = job / "scripts" / name / (name + ".md")
        runs_dir, res_dir, code_dir = job / "runs" / name, job / "results" / name, job / "scripts" / name
    if not page.is_file():
        alt = (code_dir / "README.md") if code_dir.is_dir() else None
        page = alt if alt and alt.is_file() else None
    # a ticket is a file in runs/, or runs/<run>/<run>.<ext> (one folder per Run): never a Result file
    tickets = sorted(x for x in runs_dir.rglob("*") if x.is_file() and x.suffix in _TICKET_EXT
                     and (x.parent == runs_dir or x.parent.name == x.stem)) if runs_dir.is_dir() else []
    receipts, receipt_map = [], {}
    # one folder per Run (haipipe-run 0.31.0): runs/<run>/result/ beside the older results/<run>/
    folders = [(x.name, x / "result") for x in sorted(runs_dir.iterdir())
               if x.is_dir() and (x / "result").is_dir()] if runs_dir.is_dir() else []
    folders += [(x.name, x) for x in sorted(res_dir.iterdir()) if x.is_dir()] if res_dir.is_dir() else []
    if folders:
        for run_name, run_dir in folders:
            r = run_dir / "runtime.yaml"
            if r.is_file():
                st = _head_field(r, "status") or "?"
                receipts.append(st)
                receipt_map[run_name] = st                # Discovery: runs/<run>/result/ or results/<run>/
                tk = _head_field(r, "ticket")             # Stata dialect: the receipt names its ticket
                if tk:
                    receipt_map[Path(tk.strip().strip('"')).stem] = st
    develops = _head_field(page, "develops") if page else None
    src = "page"
    if not develops and code_dir.is_dir():
        code = sorted(x for x in code_dir.iterdir() if x.is_file() and x.suffix in _CODE_EXT and not x.name.startswith("_"))
        own = [x for x in code if x.stem == name] or code
        develops, src = (_headline(own[0]) if own else ""), (own[0].name if own else "")
    state = (_head_field(page, "state") if page else None) or ""
    home = tdir if tdir is not None else (code_dir if code_dir.is_dir() else runs_dir)
    return {"name": name, "addr": "", "dir": home, "page": page, "tickets": len(tickets),
            "ticket_list": [(x.stem, x) for x in tickets], "receipt_map": receipt_map,
            "receipts": _run_state(receipts), "develops": develops or "", "develops_src": src, "state": state}


def scan_task_tree(tasks):
    """Block → Job → Task read off the folder. Names are checked against
    <b|j|t>NN_ and everything else is skipped, never guessed."""
    blocks = []
    if tasks is None or not tasks.is_dir():
        return blocks
    for b in sorted(x for x in tasks.iterdir() if x.is_dir() and re.match(r"^b\d{2}_", x.name)):
        jobs = []
        for j in sorted(x for x in b.iterdir() if x.is_dir() and re.match(r"^j\d{2}_", x.name)):
            direct = sorted(x for x in j.iterdir() if x.is_dir() and re.match(r"^t\d{2}_", x.name) and x.name not in _SKIP_DIRS)
            tasks_ = [_scan_task(j, t.name, t) for t in direct]
            if not direct:
                stems = set()
                for sub in ("runs", "scripts", "results", "notebooks"):
                    if (j / sub).is_dir():
                        stems |= {x.name for x in (j / sub).iterdir() if x.is_dir() and re.match(r"^t\d{2}_", x.name)}
                tasks_ = [_scan_task(j, n, None) for n in sorted(stems)]
            for t in tasks_:
                t["addr"] = b.name[:3] + j.name[:3] + t["name"][:3]
            jobs.append({"name": j.name, "addr": b.name[:3] + j.name[:3], "dir": j, "tasks": tasks_,
                         "shape": "task folders" if direct else "runs/ · scripts/ · results/ per task"})
        blocks.append({"name": b.name, "addr": b.name[:3], "dir": b, "jobs": jobs})
    return blocks


def project_blocks(d):
    """The Task home this paper may draw on: examples/<Project>/tasks/ (or task/)
    holding bNN blocks, scanned Block → Job → Task on every load."""
    b = d["board"]
    text = read(b / "board.md")
    project = b.parent.parent if theme_kind_of(b.parent.name) == "paper" else None
    tasks = None
    home = scalar(text, "task-home").strip()          # board.md may name the folder outright
    if home:
        cand = (b / home).resolve()
        tasks = cand if cand.is_dir() else None
    if tasks is None and project:
        for name in _TASK_HOMES:
            if (project / name).is_dir():
                tasks = project / name
                break
    tree = scan_task_tree(tasks)
    if tasks and project and tasks.parent == project:
        label = "examples/%s/%s/" % (project.name, tasks.name)
    elif tasks:
        label = home or tasks.name
    else:
        label = (("examples/%s/ has no tasks/ or task/ folder" % project.name) if project else
                 "no project task home (board is not under papers/)")
    return {"dir": tasks, "blocks": [x["name"] for x in tree], "tree": tree, "label": label,
            "claim": _addresses(scalar(text, "blocks")),
            "n_jobs": sum(len(x["jobs"]) for x in tree),
            "n_tasks": sum(len(j["tasks"]) for x in tree for j in x["jobs"])}


_RANGE_RE = re.compile(r"\b(b\d{2}[.\s_-]?j\d{2}[.\s_-]?)t(\d{2})\s*[–-]\s*t(\d{2})\b")


def _expand_ranges(text):
    """`b03.j02.t01–t05` → `b03.j02.t01 b03.j02.t02 … b03.j02.t05`: a row names a run of tasks once."""
    return _RANGE_RE.sub(lambda m: " ".join("%st%02d" % (m.group(1), n)
                                           for n in range(int(m.group(2)), int(m.group(3)) + 1)), text or "")


def _addresses(text):
    """`b02.j01 b03 b04` (or b02j01, comma-separated) → ["b02j01", "b03", "b04"]."""
    out = []
    for m in _ADDR_RE.finditer(_expand_ranges(text)):
        a = "".join(l + n for l, n in zip("bjtr", m.groups()) if n)
        if a not in out:
            out.append(a)
    return out


def paper_scope(d):
    """The Task-home addresses this paper claims: board.md `blocks:` plus every
    bNN[.jNN[.tNN]] address written on a Story Task Roadmap (§7) row. Empty = nothing claimed."""
    scope = list(d["blocks"]["claim"])
    for s in d.get("story", []):
        for cells in s["tt"]:
            for a in _addresses(" ".join(cells)):
                if a not in scope:
                    scope.append(a)
    return scope


def _discovery_yaml(path):
    """status · report.outcome · report.confidence · first sentence of question."""
    out = {"status": "", "outcome": "", "confidence": "", "question": ""}
    try:
        lines = path.read_text(errors="replace").splitlines()
    except OSError:
        return out
    sect, q = None, []
    for line in lines:
        if not line.strip():
            continue
        top = not line.startswith((" ", "\t"))
        if top:
            m = re.match(r"^([\w-]+):\s*(.*?)\s*$", line)
            sect = m.group(1) if m else None
            if m and sect == "status":
                out["status"] = m.group(2).split("#")[0].strip()
            continue
        if sect == "question":
            q.append(line.strip())
        elif sect == "report":
            m = re.match(r"^\s+(outcome|confidence):\s*(.*?)\s*$", line)
            if m:
                out[m.group(1)] = m.group(2).split("#")[0].strip()
    text = " ".join(q)
    m = re.match(r"^(.{20,}?[.?!])(?=\s+[A-Z(\[]|\s*$)", text)
    out["question"] = m.group(1) if m else text
    return out


def project_discoveries(d):
    """The Discovery home this paper may draw on: examples/<Project>/discoveries/
    (or board.md `discovery-home:`), bNN evidence boards holding jNN inquiries
    holding tNN Discovery Task Pages, each with a discovery.yaml."""
    b = d["board"]
    text = read(b / "board.md")
    project = b.parent.parent if theme_kind_of(b.parent.name) == "paper" else None
    home = scalar(text, "discovery-home").strip()
    root = (b / home).resolve() if home else None
    if (root is None or not root.is_dir()) and project and theme_dirs(project, "discovery"):
        root = theme_dirs(project, "discovery")[0]          # discovery/, or the old discoveries/
    if root is not None and not root.is_dir():
        root = None
    tree = scan_task_tree(root)
    for blk in tree:
        blk["board_md"] = (blk["dir"] / "board.md") if (blk["dir"] / "board.md").is_file() else None
        for j in blk["jobs"]:
            j["index"] = (j["dir"] / "_index.md") if (j["dir"] / "_index.md").is_file() else None
            for t in j["tasks"]:
                y = t["dir"] / "discovery.yaml"
                t.update(_discovery_yaml(y) if y.is_file() else {"status": "", "outcome": "", "confidence": "", "question": ""})
                t["n_results"] = (len([x for x in (t["dir"] / "results").iterdir() if x.is_dir()]) if (t["dir"] / "results").is_dir() else 0) \
                    + (len([x for x in (t["dir"] / "runs").iterdir() if (x / "result").is_dir()]) if (t["dir"] / "runs").is_dir() else 0)
    label = (("examples/%s/%s/" % (project.name, root.name)) if root is not None and project and root.parent == project else
             home if root is not None else
             ("examples/%s/ has no discovery/ folder" % project.name) if project else
             "no discovery home (board is not under paper/)")
    return {"dir": root, "tree": tree, "label": label, "claim": _addresses(scalar(text, "discoveries")),
            "n_jobs": sum(len(x["jobs"]) for x in tree),
            "n_tasks": sum(len(j["tasks"]) for x in tree for j in x["jobs"])}


def discovery_scope(d):
    """Discovery addresses this paper claims: board.md `discoveries:` plus every
    bNN[.jNN[.tNN]] address written on a Story Discovery Roadmap (§6) row."""
    scope = list(d["disc"]["claim"])
    for s in d.get("story", []):
        for cells in s["dd"]:
            for a in _addresses(" ".join(cells)):
                if a not in scope:
                    scope.append(a)
    return scope


def _disc_lookup(d, addr):
    """b01j04 → (block, job, task|None) in the Discovery tree, or None."""
    for blk in d["disc"]["tree"]:
        if not addr.startswith(blk["addr"]):
            continue
        if len(addr) == 3:
            return blk, None, None
        for j in blk["jobs"]:
            if addr.startswith(j["addr"]):
                if len(addr) == 6:
                    return blk, j, None
                for t in j["tasks"]:
                    if t["addr"] == addr:
                        return blk, j, t
    return None


def _find(parent, prefix):
    if parent is None or not parent.is_dir():
        return None
    for x in sorted(parent.iterdir()):
        if x.name.startswith(prefix) and re.match(r"^%s(?:[_.-]|$)" % prefix, x.name):
            return x
    return None


def task_home(d, cells):
    """Read every bNN[.jNN[.tNN[.rNN]]] address on a Story row and say which
    levels exist under the project's Task home. The first address is the row's
    own keys (address · levels · path · state); `all` lists every one, because a
    row may be answered by more than one job and paper_scope() claims them all.
    No address → `no folder yet`."""
    found_all, seen = [], set()
    for cell in cells:
        for m in _ADDR_RE.finditer(_expand_ranges(cell)):
            one = _resolve_address(d, m)
            if one["address"] not in seen:
                seen.add(one["address"]); found_all.append(one)
    if not found_all:
        return {"address": "", "levels": [], "path": "", "state": "no folder yet", "all": []}
    return dict(found_all[0], all=found_all)


def _resolve_address(d, m):
    """One address match → which of its levels exist under the Task home."""
    tasks = d["blocks"]["dir"]
    bnn, jnn, tnn, rnn = m.groups()
    levels = []
    block = _find(tasks, "b" + bnn); levels.append(("b" + bnn, block))
    job = _find(block, "j" + jnn) if jnn else None
    if jnn:
        levels.append(("j" + jnn, job))
    task = None
    if tnn:
        task = _find(job, "t" + tnn) or _find(job / "runs" if job else None, "t" + tnn)
        levels.append(("t" + tnn, task))
    if rnn:
        run = None
        if task is not None and job is not None:
            run = (_find(task / "runs", "r" + rnn) or _find(job / "results" / task.name, "r" + rnn)
                   or _find(task / "results", "r" + rnn))
        levels.append(("r" + rnn, run))
    addr = ".".join(l for l, _ in levels)
    found = [x for x in levels if x[1] is not None]
    return {"address": addr, "levels": levels,
            "path": str(found[-1][1].relative_to(tasks.parent)) if found and tasks else "",
            "state": ("allocated · %d/%d levels exist" % (len(found), len(levels))) if found else "address named · nothing on disk"}


def _named(addr, named):
    """Is this job address answered by a question row (at job level or below)?"""
    return any(addr.startswith(a) or a.startswith(addr) for a in named)


def _unnamed_addrs(d):
    """The claimed folders that no Task or Discovery row names yet, as addresses:
    (Task-home job or task addresses, Discovery job addresses)."""
    t_named = [a for s in d["story"] for c in s["tt"] for a in _addresses(" ".join(c))]
    d_named = [a for s in d["story"] for c in s["dd"] for a in _addresses(" ".join(c))]
    scope, jobs = paper_scope(d), []
    for blk in d["blocks"]["tree"]:
        for j in blk["jobs"]:
            if not _claimed(j["addr"], scope):
                continue
            if not _named(j["addr"], t_named):
                jobs.append(j["addr"])                       # no row names this job
            else:                                            # a row names some of its tasks
                jobs += [t["addr"] for t in j["tasks"]
                         if _claimed(t["addr"], scope) and not _named(t["addr"], t_named)]
    dscope = discovery_scope(d)
    djobs = [j["addr"] for blk in d["disc"]["tree"] for j in blk["jobs"]
             if _claimed(j["addr"], dscope) and not _named(j["addr"], d_named)]
    return jobs, djobs


def _tree_url(d, path):
    """A plain server path for a Task-home file or folder (raw, outside any board)."""
    root = d["root"]
    try:
        return "/" + str(Path(path).resolve().relative_to(Path(root).resolve())).replace(os.sep, "/")
    except ValueError:
        return ""


def _claimed(addr, scope):
    """Is this block/job address inside the claim? A claim `b03` covers every
    job in b03; `b02j01` covers b02 (the block) and only j01 inside it."""
    return any(a.startswith(addr) or addr.startswith(a) for a in scope)


def _disc_link(d, blk, job, task, label):
    """A link into the Discovery Board: a Task Page opens in Outline; an inquiry
    opens its raw _index.md; the block opens its Discovery workbench (the Board's
    static site is retired, JL 261004). Outline does not serve `_index.md`."""
    url = ""
    if task is not None and task["page"] and blk["board_md"] is not None:
        url = outline_url(_tree_url(d, blk["board_md"]), task["page"].relative_to(blk["dir"]))
    elif task is not None:
        url = _tree_url(d, task["page"] or task["dir"])
    elif job is not None:
        url = _tree_url(d, job["index"] or job["dir"])
    elif blk["board_md"] is not None:
        url = "/_board/discovery-board?" + urlencode({"path": _tree_url(d, blk["board_md"])})
    return ('<a href="%s">%s</a>' % (esc(url), esc(label))) if url else esc(label)
