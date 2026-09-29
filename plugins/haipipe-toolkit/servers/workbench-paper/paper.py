"""📄 Paper · the Board-level Paper Workbench, live and storage-less.

    GET /_board/paper?path=<board.md>&file=board.md[#<space>[/<view>]]

The Paper Workbench is the Board-altitude sibling of the 📃 Page tab. Page shows one
Page's plan, evidence and runs; this shows one paper Board's journey through
five Spaces (haipipe-workbench-paper, JL 260916 "like haipipe-workbench-page,
you should have haipipe-workbench-paper"):

    Setup      board.md · the scaffold folders · one Codex session row per
               Section Page (JL 260916: Ideation, Story and Supporting work
               stay in the current session)
    Ideation   Story00-ideation: the Ideas (ranked) table when the page has
               one, else the plan's `Idea <n>:` divisions · evidence items ·
               the I3 admission receipt
    Story      every Story<Letter> page: C1–C8 · RQ / E / D / T / Section
               rows · compile order
    Run        every page's runs/ + results/ · gates G0–G5 read from the files
               haipipe-paper-workflow names · the Workflow map projected from
               haipipe-workbench-paper/ref/space-mapping.md

LIVE AND STORAGE-LESS, the Outline precedent: rendered from Markdown on every
open, so it can never be stale, and it needs no per-paper file. The earlier
`console/` prototype (a static data.js rebuilt by hand, one paper only) is
what this replaces. Applies to any Board whose board.md declares
`dialect: paper`; no Links key is needed.

READ-ONLY. Every row links back to the record that owns it, normally the
page's own 📃 Page route. The explicit copy controls write prompt text to
the clipboard only; the surface does not write Paper files, allocate a Run,
or infer a human tick. A gate shows a receipt when the named file exists and
`⬜ open` otherwise.
"""
import html
import json
import os
import re
from datetime import datetime
from pathlib import Path

from host_paths import SKILLS
from urllib.parse import parse_qs, quote, urlparse

from src.outline_version import latest_outline, plan_dir, version_tag
from src.plan_shape import iter_plan_bullets

_PAIRS_DIR = Path(os.environ.get("HAIPIPE_PAIRS_DIR",
                                 Path.home() / ".config" / "haipipe" / "pairs"))

_EV_RE = re.compile(r"\bE\d{2}-(?:VALUE|CITE|DISPLAY|TABLE)-[A-Za-z0-9-]+")
_DIV_RE = re.compile(r"^###\s+§?(\d+)\s*·\s*(.*?)\s*$")
_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]*\)")


# ---------------------------------------------------------------- text helpers
def esc(s):
    return html.escape("" if s is None else str(s), quote=True)


def clean(cell):
    """Markdown cell → plain text: links to their label, no emphasis marks."""
    cell = _LINK_RE.sub(r"\1", cell or "")
    cell = re.sub(r"[*_`]+", "", cell)
    return re.sub(r"\s+", " ", cell).strip()


def scalar(text, key, default=""):
    m = re.search(r"^%s:\s*(.+?)\s*$" % re.escape(key), text or "", re.M)
    return m.group(1) if m else default


def read(path):
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def table_rows(text, first_cell):
    """Every `| a | b |` row whose first cell matches `first_cell` (regex), as
    lists of cleaned cells. Header and rule rows never match a data pattern."""
    pat = re.compile(first_cell)
    rows = []
    for line in (text or "").splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [clean(c) for c in s.strip("|").split("|")]
        if cells and pat.fullmatch(cells[0]):
            rows.append(cells)
    return rows


def divisions(text):
    """`### N · Title` headings under `## Content` → [(n, title)]."""
    out, inside = [], False
    for line in (text or "").splitlines():
        if line.startswith("## "):
            inside = line[3:].strip().lower().startswith("content")
            continue
        m = _DIV_RE.match(line) if inside else None
        if m:
            out.append((int(m.group(1)), m.group(2)))
    return out


# ---------------------------------------------------------------- the board
def board_pages(board_text):
    """`## Pages` → [{"label","folder","stems"}] in roster order."""
    groups, inside, cur = [], False, None
    for line in (board_text or "").splitlines():
        if line.startswith("## "):
            inside = line[3:].strip().lower().startswith("pages")
            cur = None
            continue
        if not inside:
            continue
        if line.startswith("### ") and " · " in line:
            # `### LABEL · folder` or `### LABEL · folder · what it holds`; a heading whose
            # second part is prose names no folder, and page_file() finds the pages itself
            parts = [x.strip() for x in line[4:].split("·")]
            folder = parts[1] if re.fullmatch(r"[\w.-]+", parts[1]) else ""
            cur = {"label": parts[0], "folder": folder, "stems": []}
            groups.append(cur)
            continue
        s = line.strip()
        if cur is not None and s.endswith(".md") and " " not in s:
            cur["stems"].append(s[:-3])
    return groups


def page_file(board, folder, stem):
    """The page's Markdown: folded `<folder>/<stem>/<stem>.md` first, flat
    `<folder>/<stem>.md` second; with no folder, the one page folder of that
    name under any top-level folder. None when nothing is found."""
    if folder:
        for rel in (Path(folder) / stem / (stem + ".md"), Path(folder) / (stem + ".md")):
            if (board / rel).is_file():
                return rel
        return None
    found = sorted(board.glob("*/%s/%s.md" % (stem, stem))) + sorted(board.glob("*/%s.md" % stem))
    return found[0].relative_to(board) if found else None


def outline_url(path_param, rel_file, lens="div", **extra):
    url = "/_board/draft?path=%s&file=%s&lens=%s" % (
        quote(path_param, safe=""), quote(str(rel_file), safe=""), quote(lens, safe=""))
    for k, v in extra.items():
        if v:
            url += "&%s=%s" % (k, quote(str(v), safe=""))
    return url


def board_url(path_param, rel):
    """A plain link into the built board tree for a non-Page file."""
    base = path_param.rsplit("/", 1)[0]
    return base + "/" + str(rel)


# ---------------------------------------------------------------- collectors
SECTION_ROW = r"S-[\w-]+(?:\s*(?:\(.*\)|·.*))?"
STORY_STEM = re.compile(r"^Story(?:[A-Z]|(?!00)\d{2})(?:\b|-)")


def collect(board, path_param):
    """Read everything the four Spaces show. Pure: no writes, no network."""
    board = Path(board)
    text = read(board / "board.md")
    groups = board_pages(text)
    pages = []
    for g in groups:
        for stem in g["stems"]:
            rel = page_file(board, g["folder"], stem)
            pages.append({"group": g, "stem": stem, "rel": rel,
                          "text": read(board / rel) if rel else ""})
    story00 = next((p for p in pages if p["stem"].startswith("Story00")), None)
    # Story<Letter> is canonical; legacy numbered Stories (Story01-seed, Story02-roadmap,
    # Story03-narrative-MISQ) stay readable per haipipe-paper-ideation, so they are Stories too
    stories = [p for p in pages if STORY_STEM.match(p["stem"])]
    sections = [p for p in pages if p["stem"].startswith("S-")]
    rounds = [p for p in pages if p["stem"].startswith("RD")]
    d = {
        "title": next((l[2:].strip() for l in text.splitlines()
                       if l.startswith("# ")), board.name),
        "board": board, "path": path_param,
        "spine": scalar(text, "spine"), "close": scalar(text, "close"),
        "session": scalar(text, "session"), "dialect": scalar(text, "dialect"),
        "groups": groups, "pages": pages, "story00": story00,
        "stories": stories, "sections": sections, "rounds": rounds,
    }
    d["sessions"] = session_rows(d)
    d["ideation"] = ideation(d)
    d["story"] = [story(d, p) for p in stories]
    d["blocks"] = project_blocks(d)
    d["disc"] = project_discoveries(d)
    d["delivery"] = delivery_info(d)
    d["hero"] = hero_evidence(d)
    d["supporting"] = supporting_tree(d)
    d["gates"] = gates(d)
    return d


def paper_desk(d):
    """The desk name, read from a real B group (`Ba-MISQ-Main` → MISQ) or, before
    any Section group exists, from the Story's C8 target cell (`MISQ · 1`)."""
    for g in d["groups"]:
        m = re.match(r"^B[a-z]-(.+)-(?:Main|Appendix|Round)$", g["folder"])
        if m:
            return m.group(1)
    for p in d["stories"]:
        for c in table_rows(p["text"], r"S-[\w-]+\s*\(.*\)"):
            m = re.search(r"\(([^·)]+)", c[0])
            if m and m.group(1).strip():
                return m.group(1).strip()
    return ""


def _pairs_for(root_cwd):
    """Pair manifests registered for this workspace, keyed by lower name.
    Exact key match only: a name match is never scored here (CLAUDE.md)."""
    out = {}
    try:
        files = sorted(_PAIRS_DIR.glob("*.json"))
    except OSError:
        return out
    for f in files:
        try:
            j = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if not isinstance(j, dict) or j.get("cwd") != str(root_cwd):
            continue
        name = str(j.get("pair_name", "")).strip().lower()
        providers = j.get("providers") or {}
        codex = providers.get("codex") or {}
        claude = (providers.get("claude") or {}).get("session_id", "")
        rec = {"file": f.name, "pair": str(j.get("pair_name", "")).strip(),
               "codex": codex.get("session_id", ""),
               "updated": str(j.get("updated_at", ""))[:10]}
        out[name] = rec
        if claude:                             # exact id key: the page's own session: line
            out["claude:" + claude] = rec
            if rec["codex"]:                   # an Appendix shares one Claude session across pages
                out["pair:%s:%s" % (claude, rec["codex"])] = rec
    return out


def session_rows(d):
    """One session per Section Page (JL 260916; Claude sessions via
    `/haipipe-paper sessions`, JL 260928). The page header's `session:` line
    binds its Claude session; a pair manifest joins by that exact id, else by
    exact pair name. Ideation, Story and Supporting work stay in the current
    session, so only S- pages get rows."""
    root = d.get("root")
    pairs = _pairs_for(root) if root else {}
    rows = []
    for p in d["sections"]:
        parts = p["stem"].split("-")           # S-<desk>-<Main|Appendix>-<N>-<Title>
        desk = parts[1].lower() if len(parts) > 1 else "paper"
        title = "-".join(parts[4:] if len(parts) > 4 else parts[3:]).lower()
        plan = "paper-%s-%s" % (desk, title)
        sid = scalar(p.get("text", ""), "session")
        cx = scalar(p.get("text", ""), "codex-session")
        # the page's own (session, codex-session) pair first: Appendix pages share one Claude
        # session and each keeps its own Codex thread, so the Claude id alone picks the last pair
        hit = ((pairs.get("pair:%s:%s" % (sid, cx)) if sid and cx else None)
               or (pairs.get("claude:" + sid) if sid else None)
               or pairs.get(plan) or pairs.get(p["stem"].lower()))
        state = []
        if sid:
            state.append("claude %s" % sid[:8])
        if hit and hit["codex"]:
            state.append("codex %s · %s" % (hit["codex"][:8], hit["updated"]))
        elif cx:
            state.append("codex %s" % cx[:8])
        rows.append({"stem": p["stem"], "rel": p["rel"], "group": p["group"]["folder"],
                     "pair": hit["pair"] if hit else ("" if (sid or cx) else plan),
                     "state": " · ".join(state) or "no session · plan"})
    return rows


def idea_divisions(text):
    """`### N · Idea <n>: <research question>` divisions under Content → {n: {"title", "fields"}}
    where fields are the division's `**Field**` blocks in page order, each a
    list of paragraphs (a `- ` line stays a list item)."""
    out, cur, field = {}, None, None
    inside = False
    for line in (text or "").splitlines():
        if line.startswith("## "):
            inside = line[3:].strip().lower().startswith("content")
            cur = None
            continue
        if not inside:
            continue
        m = re.match(r"^###\s+§?\d+\s*·\s*Idea\s+(\d+)\s*:\s*(.*?)\s*$", line)
        if m:
            cur = {"title": m.group(2), "fields": []}
            out[int(m.group(1))] = cur
            field = None
            continue
        if line.startswith("### ") or line.startswith("## "):
            cur = None
            continue
        if cur is None:
            continue
        fm = re.match(r"^\*\*(.+?)\*\*\s*:?\s*(.*)$", line.strip())
        if fm:
            field = [fm.group(1).strip(), []]
            cur["fields"].append(field)
            if fm.group(2).strip():
                field[1].append(fm.group(2).strip())
            continue
        if field is not None and line.strip():
            field[1].append(line.rstrip())
    return out


def _table_headers(text, first_cell):
    """The header cells of the table whose first data row matches first_cell."""
    pat = re.compile(first_cell)
    header = None
    for line in (text or "").splitlines():
        s_ = line.strip()
        if not s_.startswith("|"):
            header = None
            continue
        cells = [clean(c) for c in s_.strip("|").split("|")]
        if all(re.fullmatch(r"-+", c or "-") for c in cells):
            continue
        if header is None:
            header = cells
            continue
        if cells and pat.fullmatch(cells[0]):
            return header
    return None


def ideation(d):
    """The Idea Cards of Story00, one collapsed card each (JL 260916: "like the
    evidence card in haipipe-workbench-page, I can open and hide it")."""
    p = d["story00"]
    if p is None:
        return {"present": False}
    b = d["board"]
    folder = (b / p["rel"]).parent if p["rel"] else None
    out = {"present": True, "stem": p["stem"], "rel": p["rel"],
           "state": clean(scalar(p["text"], "state", "⬜ no state line")),
           "ideas": [], "source": "", "items": [], "receipts": []}
    # ① the page's own Ideas (ranked) table, when Content carries one
    rows = table_rows(p["text"], r"i\d+")
    if rows:
        out["source"] = "Content · Ideas (ranked) table"
        headers = _table_headers(p["text"], r"i\d+") or []
        for c in rows:
            fields = [(headers[i] if i < len(headers) else "col %d" % (i + 1), c[i])
                      for i in range(2, len(c)) if c[i] and c[i] not in ("—", "-")]
            out["ideas"].append({"id": c[0], "title": c[1] if len(c) > 1 else "",
                                 "verdict": c[4] if len(c) > 4 else "⬜ open",
                                 "went": c[5] if len(c) > 5 else "",
                                 "address": "", "chips": [], "bullets": [],
                                 "fields": fields, "items": []})
    # ② else the plan's `Idea <n>: <research question>` divisions (an Ideation Page before Content)
    plan = latest_outline(plan_dir(folder), p["stem"]) if folder else None
    if plan is not None:
        ptext = read(plan)
        if not out["ideas"]:
            out["source"] = "outline plan · Idea divisions (page has no Content yet)"
            seen = {}
            for blk in iter_plan_bullets(ptext):
                m = re.match(r"^Idea\s+(\d+)\s*:\s*(.*)$", blk["division_title"])
                if not m:
                    continue
                key = blk["division"]
                if key not in seen:
                    seen[key] = {"id": "i%02d" % int(m.group(1)), "title": m.group(2),
                                 "address": key, "chips": [], "bullets": [],
                                 "verdict": "⬜ open", "went": "", "fields": [], "items": []}
                    out["ideas"].append(seen[key])
                notes = [x for x in blk["continuation"] if re.match(r"^(Note|Annotation|More):", x)]
                evidence = next((x for x in blk["continuation"] if x.startswith("Evidence:")), "")
                seen[key]["bullets"].append({
                    "address": blk["address"], "bullet": blk["bullet"], "head": blk["head"],
                    "notes": [re.sub(r"^\w+:\s*", "", n) for n in notes],
                    "evidence": re.sub(r"^Evidence:\s*", "", evidence)})
                seen[key]["chips"] += [c for c in _EV_RE.findall(blk["body"])
                                       if c not in seen[key]["chips"]]
    # ③ the idea itself: the page's Idea <n> division, when Content carries one
    divs = idea_divisions(p["text"])
    for idea in out["ideas"]:
        n = re.search(r"\d+", idea["id"])
        div = divs.get(int(n.group(0))) if n else None
        idea["substance"] = div["fields"] if div else []
        if div and not idea.get("title"):
            idea["title"] = div["title"]
    # ④ the authored Evidence Item contract, with its Verified tick
    if folder:
        items = read(plan_dir(folder) / (p["stem"] + "-evidence-items.md"))
        for m in re.finditer(r"^###\s+(E\d{2}-[A-Z]+-[\w-]+)\s*·\s*(\S+)\s*·\s*(.*)$", items, re.M):
            tail = items[m.end():]
            nxt = tail.find("\n### ")
            body = tail if nxt < 0 else tail[:nxt]
            v = re.search(r"\*\*Verified\*\*:\s*(\S+)", body)
            item = {"id": m.group(1), "target": m.group(2), "desc": m.group(3).strip(),
                    "verified": v.group(1) if v else "⬜"}
            out["items"].append(item)
            for idea in out["ideas"]:
                if idea["address"] and item["target"].startswith(idea["address"] + "."):
                    idea["items"].append(item)
        # ⑤ the I3 receipt and handoff files haipipe-paper-ideation names
        for rel, what in (("workflow/selection.yaml", "I3 selection receipt"),
                          ("handoff/paper-ideation.yaml", "final handoff"),
                          ("projection/paper-ideation-sync.yaml", "working sync packet")):
            out["receipts"].append({"what": what, "rel": rel,
                                    "state": "present" if (folder / rel).is_file() else "absent"})
    return out


_ADDR_RE = re.compile(r"\bb(\d{2})(?:[.\s_-]?j(\d{2}))?(?:[.\s_-]?t(\d{2}))?(?:[.\s_-]?r(\d{2}))?\b")


_TASK_HOMES = ("tasks", "task")          # LLMRec says tasks/, OpioidRx says task/
_SKIP_DIRS = {"src", "sbatch", "results", "runs", "scripts", "notebooks", "workflow",
              "QA", "board", "diagram", "config", "configs", "tests", "_tools"}
_TICKET_EXT = {".sh", ".ps1"}
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
    tickets = sorted(x for x in runs_dir.rglob("*") if x.is_file() and x.suffix in _TICKET_EXT) if runs_dir.is_dir() else []
    receipts, receipt_map = [], {}
    if res_dir.is_dir():
        for run_dir in sorted(x for x in res_dir.iterdir() if x.is_dir()):
            r = run_dir / "runtime.yaml"
            if r.is_file():
                st = _head_field(r, "status") or "?"
                receipts.append(st)
                receipt_map[run_dir.name] = st            # Discovery: results/<run stem>/
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
        blocks.append({"name": b.name, "addr": b.name[:3], "dir": b, "jobs": jobs,
                       "board": (b / "board" / "index.html").is_file()})
    return blocks


def project_blocks(d):
    """The Task home this paper may draw on: examples/<Project>/tasks/ (or task/)
    holding bNN blocks, scanned Block → Job → Task on every load."""
    b = d["board"]
    text = read(b / "board.md")
    project = b.parent.parent if b.parent.name == "papers" else None
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
    bNN[.jNN[.tNN]] address written on a Story C7 row. Empty = nothing claimed."""
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
    project = b.parent.parent if b.parent.name == "papers" else None
    home = scalar(text, "discovery-home").strip()
    root = (b / home).resolve() if home else None
    if (root is None or not root.is_dir()) and project and (project / "discoveries").is_dir():
        root = project / "discoveries"
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
                t["n_results"] = len([x for x in (t["dir"] / "results").iterdir() if x.is_dir()]) if (t["dir"] / "results").is_dir() else 0
    label = (("examples/%s/discoveries/" % project.name) if root is not None and project and root.parent == project else
             home if root is not None else
             ("examples/%s/ has no discoveries/ folder" % project.name) if project else
             "no discovery home (board is not under papers/)")
    return {"dir": root, "tree": tree, "label": label, "claim": _addresses(scalar(text, "discoveries")),
            "n_jobs": sum(len(x["jobs"]) for x in tree),
            "n_tasks": sum(len(j["tasks"]) for x in tree for j in x["jobs"])}


def discovery_scope(d):
    """Discovery addresses this paper claims: board.md `discoveries:` plus every
    bNN[.jNN[.tNN]] address written on a Story C6 row."""
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
            run = _find(job / "results" / task.name, "r" + rnn) or _find(task / "results", "r" + rnn)
        levels.append(("r" + rnn, run))
    addr = ".".join(l for l, _ in levels)
    found = [x for x in levels if x[1] is not None]
    return {"address": addr, "levels": levels,
            "path": str(found[-1][1].relative_to(tasks.parent)) if found and tasks else "",
            "state": ("allocated · %d/%d levels exist" % (len(found), len(levels))) if found else "address named · nothing on disk"}


def story(d, p):
    t = p["text"]
    s = {"stem": p["stem"], "rel": p["rel"],
         "state": clean(scalar(t, "state", "⬜ no state line")),
         "divisions": divisions(t),
         "rq": table_rows(t, r"RQ\d+"), "rq_h": _table_headers(t, r"RQ\d+") or [],
         "e": table_rows(t, r"E-?\d+(?:\s*\(.*\))?"), "e_h": _table_headers(t, r"E-?\d+(?:\s*\(.*\))?") or [],
         "dd": table_rows(t, r"D\d+"), "dd_h": _table_headers(t, r"D\d+") or [],
         "tt": table_rows(t, r"[TB]\d+"), "tt_h": _table_headers(t, r"[TB]\d+") or [],
         "qq": table_rows(t, r"Q\d+"), "qq_h": _table_headers(t, r"Q\d+") or [],
         "sections": [], "sec_h": [], "order": []}
    s["sec_h"] = _table_headers(t, SECTION_ROW) or []
    # the Spine is C1 Identity, C2 Pitch, C4 Stakes; matched by title so a legacy numbered
    # Story part (Story02-roadmap's `1 · Mission`) does not pose as an Identity
    s["spine"] = [(n, title, parse_division(division_body(t, n)))
                  for n, title in s["divisions"]
                  if re.match(r"(identity|pitch|stakes)\b", title.strip().lower())]
    seen = set()
    for c in table_rows(t, SECTION_ROW):
        # `S-<id>`, `S-<id> (label)` or `S-<id> · §0 label` (JL 260925: MISQ's main rows)
        sid = re.split(r"\s*[(·]", c[0], maxsplit=1)[0].strip()
        if sid in seen:              # the same Section listed again in a later table
            continue
        seen.add(sid)
        page = next((x for x in d["sections"] if x["stem"] == sid), None)
        s["sections"].append({"id": sid, "target": c[0][len(sid):].strip(" ()·"),
                              "question": c[1] if len(c) > 1 else "", "cells": c, "heads": s["sec_h"],
                              "rel": page["rel"] if page else None,
                              "page_state": clean(scalar(page["text"], "state", "")) if page else ""})
    # the same rows written as records (no pipe tables in a Story, JL): `**S-<id> (N) · job**`
    # then `- **Field**: value` lines, inside the Section Narrative division
    narrative = next((n for n, title in s["divisions"] if title.strip().lower().startswith("section narrative")), None)
    for rec in (section_records(division_body(t, narrative)) if narrative is not None else []):
        if rec["id"] in seen:
            continue
        seen.add(rec["id"])
        page = next((x for x in d["sections"] if x["stem"] == rec["id"]), None)
        s["sections"].append(dict(rec, rel=page["rel"] if page else None,
                                  page_state=clean(scalar(page["text"], "state", "")) if page else ""))
    m = re.search(r"<!-- haipipe:compile-order:start -->(.*?)<!-- haipipe:compile-order:end -->", t, re.S)
    if m:
        s["order"] = [l.strip()[2:].strip() for l in m.group(1).splitlines()
                      if l.strip().startswith("- ")]
    return s


_RECORD = re.compile(r"^\*\*(S-[\w-]+)\s*(?:\(([^)]*)\))?\s*(?:·\s*(.*?))?\*\*\s*$")
_FIELD = re.compile(r"^-\s+\*\*(.+?)\*\*\s*:\s*(.*)$")


def section_records(body):
    """C8 rows written as records → the table rows' shape: {id, target, question,
    cells, heads}. `**S-<id> (N) · one job**` opens a record; its `- **Field**: value`
    lines are its cells; the Reader question field is the question."""
    out, cur = [], None
    for line in (body or "").splitlines():
        m = _RECORD.match(line.strip())
        if m:
            cur = {"id": m.group(1), "target": (m.group(2) or "").strip(), "question": "",
                   "fields": [("One job", clean(m.group(3) or ""))] if m.group(3) else []}
            out.append(cur)
            continue
        if line.startswith("#"):
            cur = None
            continue
        f = _FIELD.match(line.strip()) if cur is not None else None
        if f:
            key, value = f.group(1).strip(), clean(f.group(2))
            if key.lower() == "reader question":
                cur["question"] = value[:1].upper() + value[1:]
            else:
                cur["fields"].append((key, value))
    for r in out:
        r["cells"] = [r["id"], r["question"]] + [v for _, v in r["fields"]]
        r["heads"] = ["Section", "Reader question"] + [k for k, _ in r.pop("fields")]
    return out


def division_body(text, n):
    """The Markdown between `### n · …` and the next `### ` inside Content."""
    lines = (text or "").splitlines()
    inside, grab, out = False, False, []
    for line in lines:
        if line.startswith("## "):
            inside = line[3:].strip().lower().startswith("content")
            if grab:
                break
            continue
        if not inside:
            continue
        m = _DIV_RE.match(line)
        if m:
            if grab:
                break
            grab = int(m.group(1)) == n
            continue
        if grab:
            out.append(line)
    return "\n".join(out)


def parse_division(body):
    """A Story division → (face rows, subsections, paragraphs).
    face rows   the ```text block's `EMOJI LABEL   value` lines, continuation
                lines joined; the Story's compact identity card
    subsections `#### n.m · Title` with the paragraph under each
    paragraphs  loose prose before any subsection (the Pitch is written so)"""
    face, subs, paras = [], [], []
    in_fence, cur_sub, buf = False, None, []
    def flush():
        nonlocal buf
        t = " ".join(x.strip() for x in buf if x.strip())
        if t:
            (subs[-1][1].append(t) if cur_sub is not None else paras.append(t))
        buf = []
    for line in (body or "").splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            m = re.match(r"^\s*([^\w\s]+)?\s*([A-Z][A-Z /-]{1,24}?)\s{2,}(.*)$", line)
            if m and m.group(2).strip():
                face.append([m.group(2).strip().title(), m.group(3).strip()])
            elif face and line.strip():
                face[-1][1] += " " + line.strip()
            continue
        m = re.match(r"^####\s+(.*?)\s*$", line)
        if m:
            flush()
            cur_sub = m.group(1)
            subs.append([cur_sub, []])
            continue
        if not line.strip():
            flush()
            continue
        if line.startswith("**") and cur_sub is None and not paras:
            continue          # the division's bold lead line is a label, not content
        buf.append(line)
    flush()
    return face, subs, paras


_ABBR = ("e.g.", "i.e.", "et al.", "vs.", "cf.", "Fig.", "Eq.", "No.", "Dr.", "St.", "U.S.")


def sentences(text):
    """Split prose at sentence ends. A decimal (1.19) never splits, because the
    split needs white space after the mark; a known abbreviation rejoins."""
    parts = re.split(r"(?<=[.?!])\s+(?=[A-Z(\[“\"'])", (text or "").strip())
    out = []
    for part in parts:
        if out and out[-1].endswith(_ABBR):
            out[-1] += " " + part
        else:
            out.append(part)
    return [x for x in out if x]


def prose(paragraphs):
    """Story prose for a reading cell: paragraphs stay apart, and a long
    paragraph is set one sentence per line (display only; the source is untouched)."""
    paras = [paragraphs] if isinstance(paragraphs, str) else list(paragraphs)
    html_ = []
    for par in paras:
        sents = sentences(par)
        if len(par) > 300 and len(sents) > 1:
            html_.append('<span class="para">%s</span>' % " ".join('<span class="sent">%s</span>' % inline(x) for x in sents))
        else:
            html_.append('<span class="para">%s</span>' % inline(par))
    return " ".join(html_)


def inline(text):
    """Escape prose, then render the two inline marks a Story uses:
    `code` → <code>, **bold** → <b>. Nothing else is interpreted."""
    t = esc(text or "")
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    return t


_LOCAL_RUN_RE = re.compile(r"`?((?:re-|rp-|rd|pj|pm-|pa-|pr-)[\w.-]+)`?")
_MODES = ("reuse", "rerun", "new-run", "new run", "new-task", "new round", "registered", "complete")


def _parse_supporting(value):
    """`Execution · reuse · b03j02t01r04; Discovery · reuse · b01j01t02r02` →
    [{owner, mode, addr, raw}]. `[]` and blanks name nothing."""
    out = []
    v = (value or "").strip()
    if not v or v in ("[]", "—", "-", "none"):
        return out
    for part in v.split(";"):
        part = part.strip()
        if not part:
            continue
        toks = [t.strip().strip("`") for t in part.split("·")]
        addrs = _addresses(part)
        out.append({"owner": toks[0] if toks else "", "mode": " · ".join(toks[1:-1]) if len(toks) > 2 else "",
                    "addr": addrs[0] if addrs else "", "raw": part})
    return out


def _parse_local(value):
    """`Page · Evidence Item · reuse · pj06t01r02 → results/…/result.yaml` → {mode, run, result}."""
    v = (value or "").strip()
    left, _, right = v.partition("→")
    m = _LOCAL_RUN_RE.search(left)
    mode = next((t for t in _MODES if re.search(r"(^|·)\s*%s\s*(·|$)" % re.escape(t), left)), "")
    return {"mode": mode, "run": m.group(1) if m else "", "result": right.strip().strip("`"), "raw": v}


def _page_items(folder, stem):
    """The typed Evidence Item contract of one page: id · type · target · desc
    · Label · Expected · Supporting Runs · Local Run · Verified/Status.
    `### E…` is a live item; `#### E…` is a retired one (kept, marked). An item
    ends at the next heading of ANY level, so a retired block never leaks into
    the live item above it."""
    items = read(plan_dir(folder) / (stem + "-evidence-items.md"))
    out = []
    for m in re.finditer(r"^(#{3,4})\s+(E\d{2})-([A-Z]+)-([\w-]+)\s*·\s*(.*)$", items, re.M):
        retired = len(m.group(1)) == 4
        rest = [x.strip() for x in m.group(5).split("·")]
        target = rest[0] if (not retired and len(rest) > 1) else ""
        desc = " · ".join(rest[1:] if target else rest)
        tail = items[m.end():]
        nx = re.search(r"\n#{1,6}\s", tail)
        body = tail[:nx.start()] if nx else tail
        f = {k.strip().lower(): v.strip() for k, v in re.findall(r"^- \*\*([\w ]+)\*\*:\s*(.*)$", body, re.M)}
        out.append({"id": "%s-%s-%s" % m.group(2, 3, 4), "type": m.group(3), "target": target,
                    "desc": desc, "label": f.get("label", ""), "retired": retired,
                    "expected": f.get("expected", ""),
                    "supporting": _parse_supporting(f.get("supporting runs", "")),
                    "local": _parse_local(f.get("local run", "")),
                    "status": _item_status(f, _parse_local(f.get("local run", "")), folder)})
    return out


def _item_status(fields, local, folder):
    """An Evidence Item's state from its own lines. An explicit Status wins; else the
    Local Run's Result on disk says it is ready (items keep no Status line, so every
    card used to read "contract only", JL 260928); else a named Local Run is planned."""
    explicit = fields.get("status") or fields.get("accepted") or fields.get("verified")
    if explicit:
        return explicit
    result = (local.get("result") or "").split()
    if result and (folder / result[0]).is_file():
        return "Result ready"
    if local.get("mode") == "complete":
        return "Result not found"
    return "run planned" if local.get("run") or local.get("mode") else "contract only"


def item_name(item_id):
    """`E03-VALUE-lbp-main-effect` → `Evalue03`: type first, never a bare E03 (JL 260928)."""
    m = re.match(r"E(\d+)-([A-Z]+)", item_id or "")
    return "E%s%s" % (m.group(2).lower(), m.group(1)) if m else item_id


def hero_evidence(d):
    """The few Results the paper hangs on: every DISPLAY item on a Main or
    Appendix page (what the paper prints) and every VALUE item on the Abstract
    page (what the paper states first). Section pages keep their full Evidence Space."""
    b = d["board"]
    out = []
    for p in d["sections"]:
        folder_name = p["group"]["folder"] or (Path(p["rel"]).parts[0] if p["rel"] else "")
        if not p["rel"] or not folder_name.endswith(("-Main", "-Appendix")):
            continue
        folder = (b / p["rel"]).parent
        abstract = p["stem"].lower().endswith("abstract")
        for it in _page_items(folder, p["stem"]):
            if it["retired"]:
                continue
            if it["type"] in ("DISPLAY", "TABLE") or (abstract and it["type"] == "VALUE"):
                it.update({"page": p["stem"], "rel": p["rel"],
                           "part": "appendix" if folder_name.endswith("-Appendix") else "main",
                           "why": "printed display" if it["type"] != "VALUE" else "stated in the Abstract"})
                out.append(it)
    return out


def supporting_tree(d):
    """The owner-native Runs this paper's Evidence Items cite, as a
    Block › Job › Task › Run tree per owner (Execution = the Task home,
    Discovery = the Discovery home). Each Run lists who uses it."""
    b = d["board"]
    cited, loose = {}, []
    for p in d["pages"]:
        if not p["rel"]:
            continue
        for it in _page_items((b / p["rel"]).parent, p["stem"]):
            if it["retired"]:
                continue
            for sp in it["supporting"]:
                owner = "Discovery" if sp["owner"].lower().startswith("discover") else "Execution"
                user = {"page": p["stem"], "rel": p["rel"], "item": it["id"], "label": it["label"], "mode": sp["mode"]}
                if not sp["addr"]:
                    loose.append(dict(user, owner=owner, raw=sp["raw"]))
                    continue
                cited.setdefault((owner, sp["addr"]), []).append(user)
    trees = {"Execution": d["blocks"]["tree"], "Discovery": d["disc"]["tree"]}
    out = {"Execution": {}, "Discovery": {}, "loose": loose, "n": len(cited)}
    for (owner, addr), users in sorted(cited.items()):
        m = re.match(r"^(b\d{2})(j\d{2})?(t\d{2})?(r\d{2})?$", addr)
        if not m:
            continue
        bb, jj, tt, rr = m.groups()
        blk = next((x for x in trees[owner] if x["addr"] == bb), None)
        job = next((x for x in (blk["jobs"] if blk else []) if x["addr"] == bb + (jj or "")), None) if jj else None
        task = next((x for x in (job["tasks"] if job else []) if x["addr"] == bb + (jj or "") + (tt or "")), None) if tt else None
        found = []
        if task is not None and rr:
            found = [(stem, path) for stem, path in task["ticket_list"] if stem == rr or stem.startswith(rr + "_")]
        status = ""
        for stem, _ in found:
            status = task["receipt_map"].get(stem, status)
        node = out[owner].setdefault(bb, {"blk": blk, "jobs": {}})
        jnode = node["jobs"].setdefault(jj or "", {"job": job, "tasks": {}})
        tnode = jnode["tasks"].setdefault(tt or "", {"task": task, "runs": []})
        tnode["runs"].append({"addr": addr, "r": rr or "", "tickets": found, "status": status, "users": users,
                              "on_disk": bool(found) if rr else (task is not None if tt else job is not None)})
    return out


def gates(d):
    """G0–G5 as haipipe-paper-workflow names them, each read from a file, never
    inferred from a percentage. A gate no file can answer says so."""
    b = d["board"]
    g = []
    s00 = d["story00"]
    folder = (b / s00["rel"]).parent if s00 and s00["rel"] else None
    receipt = folder is not None and any((folder / r).is_file() for r in
                                         ("workflow/selection.yaml", "handoff/paper-ideation.yaml"))
    g.append(("G0", "Ideation → Story",
              "✅ I3 receipt · %d Story page(s)" % len(d["stories"]) if receipt
              else "⬜ open · no I3 receipt · %d Story page(s)" % len(d["stories"])))
    g.append(("G1", "Story → work", "— read on the Story's workflow records"))
    g.append(("G2", "work → Story", "— read on the Story's C5 support"))
    rows = sum(len(s["sections"]) for s in d["story"])
    minted = sum(1 for s in d["story"] for r in s["sections"] if r["rel"])
    g.append(("G3", "Story → Section",
              "%d of %d C8 rows have a Section page" % (minted, rows) if rows else "⬜ no C8 rows"))
    man = b / "delivery" / "build-manifest.json"
    if man.is_file():
        try:
            j = json.loads(man.read_text(encoding="utf-8"))
            rd = j.get("readiness") or {}
            g.append(("G4", "Section → Compile", "%s · %s/%s pages ready" % (
                j.get("status", "?"), rd.get("ready", "?"), rd.get("total", "?"))))
        except (OSError, ValueError):
            g.append(("G4", "Section → Compile", "manifest unreadable"))
    else:
        g.append(("G4", "Section → Compile", "⬜ no build · delivery/build-manifest.json absent"))
    g.append(("G5", "Round → next route", "%d Round page(s)" % len(d["rounds"])
              if d["rounds"] else "⬜ no Round yet"))
    return g


def _stamp(path):
    try:
        return datetime.fromtimestamp(Path(path).stat().st_mtime).strftime("%Y-%m-%d %H:%M")
    except OSError:
        return ""


def _mtime(path):
    try:
        return Path(path).stat().st_mtime
    except OSError:
        return 0.0


def _size(path):
    try:
        n = float(Path(path).stat().st_size)
    except OSError:
        return ""
    for u in ("B", "KB", "MB", "GB"):
        if n < 1024 or u == "GB":
            return ("%d B" % n) if u == "B" else "%.1f %s" % (n, u)
        n /= 1024.0
    return ""


def _toml_scalars(text):
    """`[section]` + `key = "value"` → {"section.key": value}; enough for paper-build.toml."""
    out, sect = {}, ""
    for line in (text or "").splitlines():
        t = line.strip()
        m = re.match(r"^\[([\w.-]+)\]", t)
        if m:
            sect = m.group(1)
            continue
        m = re.match(r'^([\w-]+)\s*=\s*"([^"]*)"', t) or re.match(r"^([\w-]+)\s*=\s*([^#\s]+)", t)
        if m:
            out[(sect + "." if sect else "") + m.group(1)] = m.group(2)
    return out


def _links(text):
    """The board's `## Links` rows: name  path."""
    out, on = {}, False
    for line in (text or "").splitlines():
        if line.startswith("## "):
            on = line.strip() == "## Links"
            continue
        m = re.match(r"^([\w-]+)\s{2,}(\S.*?)\s*$", line) if on else None
        if m:
            out[m.group(1)] = m.group(2)
    return out


def delivery_info(d):
    """What leaves the paper: delivery/ (generated whole by haipipe-paper-assemble),
    its manifest, the compile order with every Section page's fragment and lanes,
    the display register, the checks, the Round pages and returned manuscripts."""
    b = d["board"]
    text = read(b / "board.md")
    ddir = b / "delivery"
    info = {"dir": ddir if ddir.is_dir() else None, "manifest": None, "toml": {}, "outputs": [],
            "returned": [], "order": [], "order_src": "", "pages": [], "displays": [], "display_note": "",
            "assets": [], "links": _links(text), "built": "", "stale": [], "rounds": []}
    for p in d["rounds"]:
        t = p["text"]
        folder = (b / p["rel"]).parent if p["rel"] else None
        subs = [x.name for x in sorted(folder.iterdir()) if x.is_dir() and not x.name.startswith(".")] if folder else []
        info["rounds"].append({"stem": p["stem"], "rel": p["rel"], "state": scalar(t, "state"),
                               "kind": scalar(t, "round-kind"), "from": scalar(t, "received-from"),
                               "at": scalar(t, "received-at"), "due": scalar(t, "response-due"),
                               "base": scalar(t, "base-build"), "venue": scalar(t, "venue-page"), "subs": subs})
    if info["dir"] is None:
        return info
    toml = _toml_scalars(read(ddir / "paper-build.toml"))
    info["toml"] = toml
    man = None
    if (ddir / "build-manifest.json").is_file():
        try:
            man = json.loads(read(ddir / "build-manifest.json"))
        except ValueError:
            man = {"error": "build-manifest.json is not valid JSON"}
    info["manifest"] = man
    info["built"] = (man or {}).get("built", "") or ""
    built_t = 0.0
    if info["built"]:
        try:
            built_t = datetime.fromisoformat(info["built"]).timestamp()
        except ValueError:
            built_t = 0.0
    # outputs: what paper-build.toml [outputs] names, else what sits in latex/ and word/
    named = [(k.split(".", 1)[1], v) for k, v in toml.items() if k.startswith("outputs.") and
             k.split(".", 1)[1] in ("main_pdf", "main_docx", "supplement_pdf", "supplement_docx")]
    # the cover letter shows on its own Delivery tab (_cover_panes), never beside the manuscript
    if not named:
        named = [("pdf", str(x.relative_to(ddir))) for x in sorted((ddir / "latex").glob("*.pdf")) if (ddir / "latex").is_dir()] + \
                [("docx", str(x.relative_to(ddir))) for x in sorted((ddir / "word").glob("*.docx")) if (ddir / "word").is_dir()]
    for what, rel in named:
        f = ddir / rel
        info["outputs"].append({"what": what.replace("_", " "), "rel": "delivery/" + rel, "path": f, "exists": f.is_file(),
                                "size": _size(f), "stamp": _stamp(f),
                                "stale": bool(f.is_file() and built_t and _mtime(f) + 5 < built_t)})
    if (ddir / "word-feedback").is_dir():
        for f in sorted(ddir / "word-feedback").iterdir() if False else sorted((ddir / "word-feedback").iterdir()):
            if f.is_file() and not f.name.startswith("."):
                info["returned"].append({"name": f.name, "rel": "delivery/word-feedback/" + f.name, "path": f,
                                         "size": _size(f), "stamp": _stamp(f)})
    # compile order: the manifest's, else the Story's C8 block
    order = []
    if man and isinstance(man.get("order"), dict):
        order = [(x, "main") for x in man["order"].get("main", [])] + [(x, "appendix") for x in man["order"].get("appendix", [])]
        info["order_src"] = "build-manifest.json (%s)" % (man.get("order_source") or "").split(" · ")[0]
    elif d["story"] and d["story"][0]["order"]:
        order = [(x, "main" if "-Main-" in x else "appendix") for x in d["story"][0]["order"]]
        info["order_src"] = "Story C8 compile order (no build yet)"
    info["order"] = order
    mpages = {p.get("id"): p for p in (man or {}).get("pages", []) if isinstance(p, dict)}
    by_stem = {p["stem"]: p for p in d["pages"]}
    for pid, part in order:
        pg = by_stem.get(pid)
        rel = pg["rel"] if pg else ""
        folder = (b / rel).parent if rel else None
        md_t = _mtime(b / rel) if rel else 0.0
        frag = folder / "delivery" / "latex" / (pid + ".tex") if folder else None
        lanes = []
        if folder:
            lat = folder / "delivery" / "latex"
            pdfs = [x for x in (lat.glob(pid + "*.pdf") if lat.is_dir() else [])]
            lanes.append(("📜", "latex", bool(pdfs), max((_mtime(x) for x in pdfs), default=0.0)))
            wd = folder / "delivery" / "word" / (pid + ".docx")
            lanes.append(("📝", "word", wd.is_file(), _mtime(wd)))
            web = folder / "delivery" / "web" / "index.html"
            lanes.append(("🌐", "web", web.is_file(), _mtime(web)))
        mp = mpages.get(pid, {})
        stale = bool(rel and built_t and md_t > built_t + 5)
        if stale:
            info["stale"].append(pid)
        info["pages"].append({"id": pid, "part": part, "rel": rel, "state": scalar(pg["text"], "state") if pg else "",
                              "minted": bool(rel), "frag": bool(frag and frag.is_file()),
                              "frag_stale": bool(frag and frag.is_file() and md_t > _mtime(frag) + 5),
                              "lanes": lanes, "ready": mp.get("ready"), "reasons": mp.get("reasons") or [],
                              "warnings": mp.get("warnings") or [],
                              "outline": ((mp.get("outline") or {}).get("version") or ""),
                              "approval": ((mp.get("outline") or {}).get("approval") or "").split(" · ")[0],
                              "stale": stale})
    reg = read(ddir / "display-register.md")
    m = re.search(r"^Built .*$", reg, re.M)
    info["display_note"] = m.group(0) if m else ""
    fence = re.search(r"```text\n(.*?)```", reg, re.S)
    if fence:
        for line in fence.group(1).splitlines():
            if not line.strip() or line.startswith("PRINTED"):
                continue
            cells = re.split(r"\s{2,}", line.strip())
            if len(cells) >= 4:
                info["displays"].append(cells + [""] * (5 - len(cells)))
    sa = ddir / "latex" / "submission-assets"
    if sa.is_dir():
        info["assets"] = [{"name": x.name, "rel": "delivery/latex/submission-assets/" + x.name, "path": x, "size": _size(x)}
                          for x in sorted(sa.iterdir()) if x.is_file() and not x.name.startswith(".")]
    return info


def _table(headers, rows):
    if not rows:
        return ""
    h = "".join("<th>%s</th>" % esc(x) for x in headers)
    body = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in rows)
    return '<table class="grid"><tr>%s</tr>%s</table>' % (h, body)


def _empty(msg):
    return '<div class="mut">%s</div>' % esc(msg)


def _link(d, rel, label, **extra):
    if not rel:
        return esc(label)
    return '<a href="%s">%s</a>' % (esc(outline_url(d["path"], rel, **extra)), esc(label))


def _kv(rows, cls=""):
    """Label/value rows as a table with cell edges. A row with no label, or
    whose value is itself a table or a tree, spans the full width instead of
    nesting a grid inside a narrow cell."""
    out = []
    for l, v in rows:
        wide = (not l) or "<table" in v or 'class="tree-' in v
        if wide:
            cap = ('<div class="kv-cap">%s</div>' % esc(l)) if l and "<table" not in v and 'class="tree-' not in v else ""
            out.append('<div class="item-row %s nolabel">%s<span>%s</span></div>' % (cls, cap, v))
        else:
            out.append('<div class="item-row %s"><b>%s</b><span>%s</span></div>' % (cls, esc(l), v))
    return '<div class="kv">%s</div>' % "".join(out) if out else ""


def _card(cid, kind, label, sub, where, status, status_cls, rows, key="", attrs="", body="", fold=False):
    """One collapsed card, the Evidence-card shape: chevron · kind pill · label
    with a muted subline · where · status; open = label/value rows. `key` is what
    opening the card selects in its Space's Runs panel."""
    # `body` leads the opened card; `fold` tucks the label/value rows under a closed Details line
    detail = body + (('<details class="row-details"><summary>Details</summary>%s</details>' % _kv(rows))
                     if fold and rows else _kv(rows))
    # say a thing once: a subline that is empty, a dash, or the same words as `where` is dropped
    plain = lambda h: re.sub(r"<[^>]+>", "", h or "").strip()
    subline = "" if plain(sub) in ("", "—") or plain(sub) == plain(where) else '<span class="item-title">%s</span>' % sub
    return ('<details class="item-card" id="%s"%s%s><summary><div class="item-summary">'
            '<span class="item-chevron">›</span><span class="item-kind">%s</span>'
            '<div class="item-main"><span class="item-label">%s</span>%s</div>'
            '<span class="item-where">%s</span><span class="item-status %s">%s</span>'
            '</div></summary><div class="item-detail">%s</div></details>'
            % (esc(cid), (' data-key="%s"' % esc(key)) if key else "", attrs, esc(kind), esc(label), subline,
               where, status_cls, esc(status), detail))


def _repo_rel(d, path):
    """A path as the chat needs it: relative to the repository root."""
    if not path:
        return ""
    pth = Path(path)
    if not pth.is_absolute():
        pth = d["board"] / pth
    try:
        return str(pth.resolve().relative_to(Path(d["root"]).resolve())).replace(os.sep, "/")
    except (ValueError, KeyError):
        return str(path)


def _srcd(d, path, ref, card_html):
    """Stamp a card with the Markdown it was read from (data-src) and the row
    it shows (data-ref), so `copy to chat` can cite the truth source."""
    i = card_html.find('<details class="item-card"')
    j = card_html.find(">", i) if i >= 0 else -1
    if j < 0:
        return card_html
    return card_html[:j] + ' data-src="%s" data-ref="%s"' % (esc(_repo_rel(d, path)), esc(ref)) + card_html[j:]


def _status_cls(text):
    t = (text or "").upper()
    if t.startswith("NOT ") or t.startswith("NO ") or "ABSENT" in t or "MISSING" in t:
        return "mut"
    if "✅" in t or "PROCEED" in t or "ESTABLISHED" in t or "ALLOCATED" in t or "READY" in t or "ACCEPTED" in t:
        return "ok"
    if "⚠" in t or "🔨" in t or "PROVISIONAL" in t or "PARTIAL" in t or "WAITING" in t:
        return "warn"
    return "mut"


def _open_cards(cards):
    """The same cards, opened: inside a question its folders are what the person came to see."""
    return [c.replace('<details class="item-card"', '<details class="item-card" open', 1) for c in cards]


def _skip_cols(headers, *names):
    """Header positions to leave out of a card's Details (shown elsewhere on the card)."""
    return {i for i, h in enumerate(headers) if h.strip().lower() in names}


def _fields(headers, cells, skip):
    return [(headers[i] if i < len(headers) else "col %d" % (i + 1), esc(cells[i]))
            for i in range(len(cells)) if i not in skip and cells[i] and cells[i] not in ("—", "-")]


def _field_html(paras):
    """A **Field** block: bullet lines become a list, other lines a paragraph."""
    items = [l for l in paras if l.lstrip().startswith("- ")]
    text = [l for l in paras if not l.lstrip().startswith("- ")]
    html_ = esc(" ".join(text))
    if items:
        html_ += '<ul class="item-bullets">%s</ul>' % "".join(
            "<li>%s</li>" % esc(l.lstrip()[2:]) for l in items)
    return html_


def _idea_card(d, i, x):
    substance = x.get("substance") or []
    def _first(*starts):
        return next((" ".join(v) for k, v in substance if k.lower().startswith(starts)), "")
    # The card leads with the question the Idea asks (JL 260922: "the ideation should be the
    # research question, which can trigger the reader to think"); the title drops to the subline.
    rq = _first("research question", "question")
    hyp = _first("hypothesis", "one-sentence")
    label, sub = (rq, esc(x["title"])) if rq else (x["title"], esc(hyp))
    verdict = x.get("verdict") or "⬜ open"
    went = x.get("went") if x.get("went") not in (None, "", "—", "-") else ""
    rows = [(k, _field_html(v)) for k, v in substance]
    if x["bullets"]:
        blist = []
        for bl in x["bullets"]:
            note = " ".join(bl["notes"])
            blist.append('<li><b>%s</b> %s%s%s</li>' % (
                esc(bl["bullet"]), esc(bl["head"]),
                ('<div class="item-note">%s</div>' % esc(note)) if note else "",
                ('<div class="item-note">Evidence: %s</div>' % esc(bl["evidence"])) if bl["evidence"] else ""))
        rows.append(("", '<details class="item-plan"><summary>Writing plan</summary><ul class="item-bullets">%s</ul></details>'
                     % "".join(blist)))
    if x["items"]:
        rows.append(("Evidence items", "".join(
            '<div><span class="idtag">%s</span> %s <span class="%s">%s</span></div>' % (
                esc(it["id"]), esc(it["desc"]), "ok" if "✅" in it["verified"] else "mut", esc(it["verified"]))
            for it in x["items"])))
    fields = [(l, esc(v)) for l, v in x.get("fields", []) if l.lower() not in ("verdict", "went to")]
    if fields:
        rows.append(("Comparison", "".join('<div><b class="item-sub">%s</b> %s</div>' % (esc(l), v) for l, v in fields)))
    if " · " in verdict:
        rows.append(("Verdict", esc(verdict)))
    if went:
        rows.append(("Went to", esc(went)))       # G0: where the admitted idea went
    short = verdict.split(" · ")[0].strip()       # the closed line keeps the title readable
    return _card("idea-" + x["id"], x["id"], label, sub, esc(went), short, _status_cls(verdict), rows,
                 key=_norm_key("i", x["id"]))


def _col(headers, needles, default):
    """Index of the first header naming one of `needles` (case-insensitive), else `default`."""
    for i, h in enumerate(headers):
        if any(n in h.lower() for n in needles):
            return i
    return default


def _claim_card(d, s, c, where):
    """One C5 proposition in the Evidence-card shape. Columns follow the header
    row when the table has one (`proposition`, `support state`); otherwise the
    positional E | RQ | state | proposition order."""
    eid = re.match(r"E-?\d+", c[0]).group(0)
    ip = _col(s["e_h"], ("proposition", "claim"), 3)
    ist = _col(s["e_h"], ("support", "state", "status"), 2)
    prop = c[ip] if len(c) > ip else ""
    status = c[ist] if len(c) > ist else ""
    rows = _fields(s["e_h"], c, {0, 1, ip, ist})
    return _card("claim-" + eid, c[0], prop or c[0], "", where, status, _status_cls(status), rows,
                 key=_norm_key("E", eid))


def _rq_cards(d, s):
    """One card per C3 research question; its C5 propositions (the claims) sit
    inside as nested cards. An RQ asks and a proposition states what can be
    supported, so the question is the grain and the claims are its children
    (JL 260922). E-rows whose RQ cell names no C3 row stay in one last card."""
    irq = _col(s["e_h"], ("rq", "question"), 1)
    by_rq = {}
    for c in s["e"]:
        if re.match(r"E-?\d+", c[0]):
            by_rq.setdefault(c[irq] if len(c) > irq else "", []).append(c)
    ist = _col(s["rq_h"], ("answer state", "state", "status"), -1) if s["rq_h"] else -1
    cards = []
    for r in s["rq"]:
        rid, question = r[0], (r[1] if len(r) > 1 else "")
        if 1 < ist < len(r):
            state = r[ist]
        else:
            state = r[-1] if not s["rq_h"] and len(r) > 2 else ""
        claims = by_rq.pop(rid, [])
        rows = _fields(s["rq_h"], r, {0, 1, ist})
        inner = "".join(_claim_card(d, s, c, "") for c in claims)
        if inner:
            rows.append(("", '<div class="item-cards">%s</div>' % inner))
        cards.append(_card("rq-" + rid, rid, question or rid, "", "", state, _status_cls(state), rows, key=rid))
    orphans = [c for cs in by_rq.values() for c in cs]
    if orphans:
        inner = "".join(_claim_card(d, s, c, esc((c[irq] if len(c) > irq else "") or "")) for c in orphans)
        cards.append(_card("rq-unassigned", "C5", "Claims with no research question", "", "", "", "mut",
                           [("", '<div class="item-cards">%s</div>' % inner)]))
    return cards


def _task_cards(d, s):
    cards = []
    for c in s["tt"]:
        tid = c[0]
        home = task_home(d, c)
        # JL 260929: the BJTR folders are what matters; the row's own text is folded under Details
        rows = _fields(s["tt_h"], c, {0, 1} | _skip_cols(s["tt_h"], "folder", "q"))
        table = _bjt_tree(d, [x["address"].replace(".", "") for x in home["all"]]) if home["all"] else ""
        body = table or '<div class="space-empty">No folder yet.</div>'
        # JL 260929: no address or "allocated · 2/2 levels exist" in the header; the folders say it
        cards.append(_card("task-" + tid, tid, c[1] if len(c) > 1 else tid, "", "", "", "mut",
                           rows, key=tid, body=body, fold=True))
    return cards


def _named(addr, named):
    """Is this job address answered by a question row (at job level or below)?"""
    return any(addr.startswith(a) or a.startswith(addr) for a in named)


def _unnamed_cards(d):
    """The claimed folders that no Task or Discovery question names yet (JL 260928:
    question first, then its Task and Discovery runs; one list, not two)."""
    t_named = [a for s in d["story"] for c in s["tt"] for a in _addresses(" ".join(c))]
    d_named = [a for s in d["story"] for c in s["dd"] for a in _addresses(" ".join(c))]
    scope, jobs = paper_scope(d), []
    for blk in d["blocks"]["tree"]:
        for j in blk["jobs"]:
            if not _claimed(j["addr"], scope):
                continue
            if not _named(j["addr"], t_named):
                jobs.append(j["addr"])                       # no question names this job
            else:                                            # a question names some of its tasks
                jobs += [t["addr"] for t in j["tasks"]
                         if _claimed(t["addr"], scope) and not _named(t["addr"], t_named)]
    tasks, _ = _block_cards(d, jobs) if jobs else ([], [])
    dscope = discovery_scope(d)
    djobs = [j["addr"] for blk in d["disc"]["tree"] for j in blk["jobs"]
             if _claimed(j["addr"], dscope) and not _named(j["addr"], d_named)]
    disc, _ = _disc_cards(d, djobs, _disc_feeds(d)) if djobs else ([], [])
    return tasks + disc


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


def _receipts(tasks):
    out = {}
    for t in tasks:
        for k, v in t["receipts"].items():
            out[k] = out.get(k, 0) + v
    return out


def _scoped_blocks(d, scope):
    """(block, its jobs in `scope` with their tasks in `scope`, jobs outside the paper's claim)."""
    claim = paper_scope(d)
    for blk in d["blocks"]["tree"]:
        if scope and not _claimed(blk["addr"], scope):
            continue
        jobs = [dict(j, tasks=[t for t in j["tasks"] if not scope or _claimed(t["addr"], scope)])
                for j in blk["jobs"] if not scope or _claimed(j["addr"], scope)]
        yield blk, jobs, [j for j in blk["jobs"] if not _claimed(j["addr"], claim)]


def _bjt_tree(d, scope, block_rows=True):
    """Block → Job → Task as folds with no boxes (JL 260929: "套这么多感觉跟棺材一样", then "我想让它
    能够合上去"): the block and each job are a borderless fold (arrow · pill · name · counts), opened by
    default, indented one step; a job opens to its one task table. Jobs outside the paper's own
    claim are named once, muted."""
    out = []
    pill = lambda a: '<span class="item-kind">%s</span>' % esc(a)
    head = "".join("<th>%s</th>" % h for h in ("addr", "task", "develops", "runs", "state"))
    fold = lambda cls, summary, body: ('<details class="%s" open><summary><span class="bjt-chev">›</span>%s</summary>%s</details>'
                                       % (cls, summary, body))
    for blk, jobs, other in _scoped_blocks(d, scope):
        inner = []
        for j in jobs:
            trs = []
            for t in j["tasks"]:
                url = _tree_url(d, t["page"] or t["dir"])
                name = ('<a href="%s">%s</a>' % (esc(url), esc(t["name"]))) if url and t["page"] else esc(t["name"])
                dev = esc(t["develops"]) if t["develops"] else '<span class="mut">?</span>'
                if t["develops"] and t["develops_src"] != "page":
                    dev = '<i title="from %s, not typed on the page">%s</i>' % (esc(t["develops_src"]), dev)
                runs = (esc("%d tk · %s" % (t["tickets"], _fmt_state(t["receipts"]))) if (t["tickets"] or t["receipts"])
                        else '<span class="mut">—</span>')
                state = esc(t["state"]) if t["state"] else '<span class="mut">%s</span>' % ("no state: line" if t["page"] else "no page")
                trs.append('<tr><td><span class="idtag">%s</span></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'
                           % (esc(t["addr"]), name, dev, runs, state))
            body = ('<table class="grid bjt-t"><tr>%s</tr>%s</table>' % (head, "".join(trs)) if trs
                    else '<div class="bjt-o mut">no tNN_ task under this job</div>')
            jurl = _tree_url(d, j["dir"])
            inner.append(fold("bjt-j", '%s <b>%s</b> <span class="mut">· %d task(s) · %d ticket(s) · %s</span> %s'
                              % (pill(j["addr"][3:]), esc(j["name"]), len(j["tasks"]), sum(t["tickets"] for t in j["tasks"]),
                                 esc(_fmt_state(_receipts(j["tasks"]))), ('<a href="%s">folder</a>' % esc(jurl)) if jurl else ""),
                              body))
        if other:
            inner.append('<div class="bjt-o mut">not claimed · not this paper\'s: %s</div>'
                         % esc(" · ".join(j["name"] for j in other)))
        if block_rows:
            tasks = [t for j in jobs for t in j["tasks"]]
            board = ('<a href="%s">board</a>' % esc(_tree_url(d, blk["dir"] / "board" / "index.html"))) if blk["board"] else ""
            out.append(fold("bjt-b", '%s <b>%s</b> <span class="mut">· %d job(s) · %d task(s) · %s</span> %s'
                            % (pill(blk["addr"]), esc(blk["name"]), len(jobs), len(tasks),
                               esc(_fmt_state(_receipts(tasks))), board), "".join(inner)))
        else:
            out += inner
    return '<div class="bjt">%s</div>' % "".join(out) if out else ""


def _block_cards(d, scope):
    """One collapsed card per bNN block in `scope`; open = the block's one Job → Task table
    (`_bjt_tree` without its block fold: the card header is the block)."""
    cards, skipped = [], [b["name"] for b in d["blocks"]["tree"] if scope and not _claimed(b["addr"], scope)]
    for blk, jobs, other in _scoped_blocks(d, scope):
        tasks = [t for j in jobs for t in j["tasks"]]
        state = _receipts(tasks)
        where = ('<a href="%s">board</a>' % esc(_tree_url(d, blk["dir"] / "board" / "index.html"))) if blk["board"] else ""
        sub = "%d job(s) · %d task(s) · %d ticket(s)" % (len(jobs), len(tasks), sum(t["tickets"] for t in tasks)) + (
            (" · %d job(s) not claimed" % len(other)) if other else "")
        body = _bjt_tree(d, [a for a in scope if a.startswith(blk["addr"])] or [blk["addr"]], block_rows=False)
        cards.append(_srcd(d, blk["dir"], blk["addr"], _card("block-" + blk["addr"], blk["addr"], blk["name"], esc(sub),
                           where, _fmt_state(state), "ok" if state.get("done") and len(state) == 1 else ("warn" if state else "mut"),
                           [], body=body or _empty("no job in this block"))))
    return cards, skipped


def _disc_link(d, blk, job, task, label):
    """A link into the Discovery Board: a Task Page opens in Outline; an inquiry
    opens its built board page (board/jNN.html), else its raw _index.md; the
    block opens the board itself. Outline does not serve `_index.md`."""
    url = ""
    if task is not None and task["page"] and blk["board_md"] is not None:
        url = outline_url(_tree_url(d, blk["board_md"]), task["page"].relative_to(blk["dir"]))
    elif task is not None:
        url = _tree_url(d, task["page"] or task["dir"])
    elif job is not None:
        built = blk["dir"] / "board" / (job["name"][:3] + ".html")
        url = _tree_url(d, built if built.is_file() else (job["index"] or job["dir"]))
    elif blk["board_md"] is not None:
        built = blk["dir"] / "board" / "index.html"
        url = _tree_url(d, built) if built.is_file() else outline_url(_tree_url(d, blk["board_md"]), "board.md")
    return ('<a href="%s">%s</a>' % (esc(url), esc(label))) if url else esc(label)


def _disc_join(d, cells):
    """The Discovery jobs/tasks a C6 row names by address, as links; '' when none."""
    out = []
    for a in _addresses(" ".join(cells)):
        hit = _disc_lookup(d, a)
        if hit:
            blk, job, task = hit
            out.append(_disc_link(d, blk, job, task, (task or job or blk)["name"]))
        else:
            out.append('<span class="warn">%s ✗ not in the Discovery home</span>' % esc(a))
    return " · ".join(out)


def _disc_cards(d, scope, feeds):
    """One collapsed card per claimed Discovery job; open = its Task Pages."""
    cards, skipped = [], []
    for blk in d["disc"]["tree"]:
        for j in blk["jobs"]:
            if scope and not _claimed(j["addr"], scope):
                skipped.append(j["name"])
                continue
            st, oc = {}, {}
            for t in j["tasks"]:
                st[t["status"] or "?"] = st.get(t["status"] or "?", 0) + 1
                if t["outcome"]:
                    oc[t["outcome"]] = oc.get(t["outcome"], 0) + 1
            fmt = lambda c: " · ".join("%s %d" % kv for kv in sorted(c.items(), key=lambda kv: -kv[1])) or "—"
            trs = []
            for t in j["tasks"]:
                runs = "%d run(s)" % max(t["tickets"], t["n_results"]) if (t["tickets"] or t["n_results"]) else "—"
                trs.append(('<span class="idtag">%s</span>' % esc(t["addr"]),
                            _disc_link(d, blk, j, t, t["name"]),
                            esc(t["question"]) if t["question"] else '<span class="mut">no question in discovery.yaml</span>',
                            esc(runs), esc(t["status"] or "?"),
                            esc((t["outcome"] + ((" · " + t["confidence"]) if t["confidence"] else "")) if t["outcome"] else "—")))
            rows = [("tasks", _table(["addr", "task page", "question", "runs", "status", "outcome"], trs) or _empty("no tNN_ Discovery Task under this job"))]
            back = feeds.get(j["addr"], [])
            rows.append(("feeds", (" · ".join('<span class="idtag">%s</span>' % esc(x) for x in back)) if back
                         else '<span class="mut">no C6 row names this job yet · write %s in a D-row cell</span>' % esc("%s.%s" % (blk["addr"], j["name"][:3]))))
            rows.append(("index", ('<a href="%s">_index.md</a>' % esc(_tree_url(d, j["index"]))) if j["index"] else '<span class="mut">no _index.md</span>'))
            where = _disc_link(d, blk, None, None, "board") if blk["board_md"] else ""
            cards.append(_srcd(d, j["dir"], j["addr"], _card("disc-" + j["addr"], j["addr"], j["name"],
                               esc("%d task page(s) · %d run(s) · %s" % (len(j["tasks"]), sum(max(t["tickets"], t["n_results"]) for t in j["tasks"]), fmt(st))),
                               where, fmt(oc) if oc else "no outcome yet", "ok" if oc and not st.get("blocked") else ("warn" if st.get("blocked") else "mut"), rows)))
    return cards, skipped


def _disc_feeds(d):
    """Discovery job address → the C6 rows that name it."""
    feeds = {}
    for s in d.get("story", []):
        for cells in s["dd"]:
            for a in _addresses(" ".join(cells)):
                hit = _disc_lookup(d, a)
                if hit and hit[1] is not None:
                    feeds.setdefault(hit[1]["addr"], []).append(cells[0])
    return feeds


def _hero_cards(d):
    cards = []
    for it in d["hero"]:
        short = it["id"].split("-")[0]
        rows = [("Need", esc(it["desc"])), ("Expected", esc(it["expected"] or "—")),
                ("Bullet", esc(it["target"]))]
        if it["supporting"]:
            rows.append(("Supporting", "<br>".join(
                "%s · <code>%s</code>" % (esc(s["owner"]), esc(s["addr"] or s["raw"])) for s in it["supporting"])))
        rows.append(("Page", _link(d, it["rel"], "Open ↗", lens="evidence", focus=it["id"])))
        cards.append(_card("hero-" + it["id"], it["type"], it["label"] or it["id"],
                           esc(item_name(it["id"]) + " · " + it["page"]), "", it["status"], _status_cls(it["status"]), rows,
                           key="%s:%s" % (it["page"], short), attrs=' data-part="%s"' % it["part"]))
    return cards


def _cards_card(title, cards, empty):
    return ('<h3 class="space-h">%s</h3>%s' % (esc(title), '<div class="item-cards">%s</div>' % "".join(cards)
                                               if cards else '<div class="space-empty">%s</div>' % esc(empty)))


def _run_tickets(runs):
    """A page's run tickets: flat `runs/`, or its Space folders (Page 0.118).

    `runs/supporting-run/` holds a generated index of Runs kept elsewhere, not tickets.
    """
    return sorted((f for f in runs.rglob("*") if f.is_file() and not f.name.startswith(".")
                   and "supporting-run" not in f.relative_to(runs).parts), key=lambda f: f.name)


def _file_link(d, path, label):
    url = _tree_url(d, path) if path else ""
    return ('<a href="%s">%s</a>' % (esc(url), esc(label))) if url else esc(label)


def _yn(v):
    return '<span class="ok">✓</span>' if v else '<span class="warn">✗</span>'


def _not_ready_ids(rd):
    """`readiness.not_ready` from build-manifest.json: the engine writes one
    {"id", "reasons"} dict per page (build_delivery.py), older manifests a bare
    id string. Either way the Delivery card names the page, never the dict."""
    out = []
    for x in rd.get("not_ready") or []:
        out.append(str(x.get("id", "?")) if isinstance(x, dict) else str(x))
    return out


# ---------------------------------------------------------------- render
# The Page workbench's grammar (JL 260927; the drawing is
# servers/workbench-paper/studio/paper-workbench-design.excalidraw): four Spaces,
# each with its tabs and views, the content on the left and its own Runs panel on
# the right. Nothing on screen explains itself: no source lines, counts or hints.
SPACES = (("ideation", "Ideation Space"), ("story", "Story Space"),
          ("sections", "Sections Space"), ("delivery", "Delivery Space"))
STORY_TABS = (("spine", "Spine"), ("questions", "Questions"), ("roadmap", "Roadmap"))
SECTION_TABS = (("main", "Main"), ("appendix", "Appendix"))
SECTION_VIEWS = (("table", "Table"), ("narrative", "Narrative"), ("evidence", "Evidence"))
DELIVERY_TABS = (("latex", "LaTeX"), ("word", "Word"), ("cover", "Cover letter"), ("rounds", "Rounds"))
DELIVERY_VIEWS = (("preview", "Preview"), ("artifacts", "Artifacts"), ("checks", "Checks"))

_CARDS = SKILLS / "paper" / "haipipe-paper-workflow" / "ref" / "run-cards.md"
_BUTTON = re.compile(r"^🔘 BUTTON\s+(?P<label>.+?)\s+·\s+(?P<space>[A-Z][A-Za-z]+)\s+·\s+"
                     r"(?P<pattern>\S.*?)(?:\s+·\s+views\s+(?P<views>[\w ]+?))?\s*$")
_PROMPT = re.compile(r"^💬 PROMPT\s+(?P<prompt>.+?)\s*$")


def paper_run_types(path=_CARDS):
    """The paper's Run cards → {space: [{label, pattern, views, prompt, skills}]} in
    card order. Each button takes the first `💬 PROMPT` after it and the `🧩 SKILL`
    line before that prompt; pattern `-` means the button only copies a prompt
    (its runs live with another owner)."""
    out, pending = {}, []
    for line in read(path).splitlines():
        m = _BUTTON.match(line)
        if m:
            t = {"label": m["label"], "space": m["space"].lower(), "pattern": m["pattern"].strip(),
                 "views": " ".join((m["views"] or "").split()), "prompt": "", "skills": []}
            out.setdefault(t["space"], []).append(t)
            pending.append(t)
            continue
        m = re.match(r"^🧩 SKILL\s+(.+?)\s*$", line)
        if m:
            for t in pending:
                t["skills"] = [s.strip() for s in m.group(1).split("·") if s.strip()]
            continue
        m = _PROMPT.match(line)
        if m:
            for t in pending:
                t["prompt"] = m["prompt"]
            pending = []
    return out


def _page_runs(d, page):
    """One Page's runs as the Page workbench reads them (live.runs.local_runs)."""
    if not page or not page.get("rel"):
        return []
    from live.runs import local_runs
    try:
        return local_runs(d["board"] / page["rel"])
    except Exception:  # noqa: BLE001  a broken ticket must not blank a Space
        return []


def _norm_key(kind, value):
    """`i01` → `i1`, `E-05` → `E5`: selection keys compare by number."""
    m = re.match(r"^%s-?0*(\d+)$" % kind, (value or "").strip())
    return "%s%s" % (kind, m.group(1)) if m else (value or "").strip()


def _bucket(kinds, rows, place):
    """rows → one list per run type. A row goes to the type whose ticket pattern
    matches; `place(row)` names a type for rows no pattern takes (or None)."""
    from live.runs_panel import _number, _ticket_name
    buckets = [[] for _ in kinds]
    for row in sorted(rows, key=_number, reverse=True):
        name = _ticket_name(row)
        hit = next((i for i, k in enumerate(kinds)
                    if k["pattern"] != "-" and re.search(k["pattern"], name)), None)
        if hit is None:
            label = place(row)
            hit = next((i for i, k in enumerate(kinds) if k["label"] == label), None)
        if hit is not None:
            buckets[hit].append(row)
    return buckets


def _panel(d, space, kinds, buckets, fill, whole):
    from live.runs_panel import panel_markup
    return panel_markup(space, kinds, buckets, base=Path(d["root"]),
                        fill=lambda row: row.get("_fill") or fill, whole=whole)


def _tag(rows, keys=(), fill=None):
    """Mark rows for the paper's panels: selection keys, no format filter, prompt fill."""
    out = []
    for row in rows:
        row = dict(row)
        row["_keys"] = " ".join(k for k in list(keys) + row.get("_keys", "").split() if k)
        row["_views"] = ""
        if fill:
            row["_fill"] = fill
        out.append(row)
    return out


def _ideation_panel(d, kinds):
    page = d["story00"]
    fill = {"page": page["stem"] if page else "Story00", "paper": d["board"].name}
    rows = []
    for row in _page_runs(d, page):
        rows += _tag([row], [_norm_key("i", row.get("target"))], fill)
    return _panel(d, "ideation", kinds, _bucket(kinds, rows, lambda r: None), fill, "every idea")


def _claim_rq(s):
    """C5 claim number → the RQ its row names."""
    irq = _col(s["e_h"], ("rq", "question"), 1)
    out = {}
    for c in s["e"]:
        m = re.match(r"E-?\d+", c[0])
        if m:
            out[_norm_key("E", m.group(0))] = c[irq] if len(c) > irq else ""
    return out


def _supporting_rows(d, s, fill):
    """The Task and Discovery runs this paper's Evidence Items cite, as run rows
    keyed by the C7 and C6 rows whose addresses cover them."""
    q_of = {c[0]: _q_of(s["tt_h"], c) for c in s["tt"]}
    q_of.update({c[0]: _q_of(s["dd_h"], c) for c in s["dd"]})
    covers = [(c[0], _addresses(" ".join(c))) for c in s["tt"] + s["dd"]]
    rows = []
    for owner in ("Execution", "Discovery"):
        for node in d["supporting"][owner].values():
            for jnode in node["jobs"].values():
                for tnode in jnode["tasks"].values():
                    for r in tnode["runs"]:
                        dotted = ".".join(re.findall(r"[bjtr]\d{2}", r["addr"]))
                        ticket = r["tickets"][0][1] if r["tickets"] else None
                        keys = [row for row, addrs in covers if any(r["addr"].startswith(a) for a in addrs)]
                        keys += sorted({q_of[k] for k in keys if q_of.get(k)})
                        users = sorted({u["page"] + " " + u["item"].split("-")[0] for u in r["users"]})
                        st = (r["status"] or "").lower()
                        rows.append({"run_id": dotted, "global_id": dotted, "ticket": ticket,
                                     "status": "done" if st in ("complete", "completed", "done") else (st or "unknown"),
                                     "target": owner + " · " + dotted, "goal": "used by " + ", ".join(users),
                                     "result": "", "_display": dotted, "_keys": " ".join(keys)})
    return _tag(rows, (), fill)


def _story_panel(d, kinds):
    rows = []
    for s in d["story"]:
        fill = {"page": s["stem"], "paper": d["board"].name}
        rq = _claim_rq(s)
        for row in _page_runs(d, s):
            name = str(row.get("run_id") or row.get("global_id") or "")
            target = str(row.get("target") or "")
            if re.search(r"(^|\s)rclaim-", name):
                e = _norm_key("E", target)
                rows += _tag([row], [e, rq.get(e, "")], fill)
            elif re.search(r"(^|\s)rtask-", name):
                rows += _tag([row], [target], fill)
            elif not re.search(r"(^|\s)(ridea|rnarra)-", name):
                rows += _tag([row], [], fill)
        rows += _supporting_rows(d, s, fill)
    first = d["story"][0]["stem"] if d["story"] else "the Story"
    fill = {"page": first, "paper": d["board"].name}
    # a supporting run goes under its owner: a Task folder's run or a Discovery folder's run
    buckets = _bucket(kinds, rows, lambda r: "Discovery runs" if str(r.get("target", "")).startswith("Discovery · ")
                      else "Task runs" if str(r.get("target", "")).startswith("Execution · ") else None)
    return _panel(d, "story", kinds, buckets, fill, "the Story")


def _sections_panel(d, kinds, sections):
    from live.runs_panel import _name_by_item, _paper_run_key, _ticket_item, row_space
    from live.space_views import run_tabs
    rows = []
    part = {sec["id"]: sec["part"] for sec in sections}
    for s in d["story"]:
        fill = {"page": s["stem"], "paper": d["board"].name}
        for row in _page_runs(d, s):
            if re.search(r"(^|\s)rnarra-", str(row.get("run_id") or "")):
                sid = str(row.get("target") or "").strip()
                rows += [dict(x, _views=part.get(sid, "")) for x in _tag([row], [sid], fill)]
    for sec in sections:
        if not sec["page"]:
            continue
        fill = {"page": sec["id"], "paper": d["board"].name}
        page_src = d["board"] / sec["page"]["rel"]
        try:
            served_by = run_tabs(page_src)
        except Exception:  # noqa: BLE001
            served_by = {}
        evidence = []
        for row in _page_runs(d, sec["page"]):
            where = row_space(row)
            keys = [sec["id"]]
            if where == "evidence":
                served = served_by.get(_paper_run_key(str(row.get("run_id") or "")))
                if served:
                    row = dict(row, _served=served)
                item = (served or {}).get("item") or _ticket_item(row)
                if item:
                    keys.append("%s:%s" % (sec["id"], item))
            tagged = _tag([row], keys, fill)[0]
            tagged["target"] = ("%s %s" % (sec["id"], row.get("target") or "")).strip()
            tagged["_views"] = sec["part"]
            tagged["_place"] = {"evidence": "Evidence runs", "delivery": "Delivery runs"}.get(where, "Draft runs")
            (evidence if where == "evidence" else rows).append(tagged)
        _name_by_item(evidence)
        rows += evidence
    fill = {"page": "{target}", "paper": d["board"].name}
    buckets = _bucket(kinds, rows, lambda r: r.get("_place"))
    return _panel(d, "sections", kinds, buckets, fill, "each Section")


def _delivery_panel(d, kinds):
    dv, rows = d["delivery"], []
    man = dv["manifest"] or {}
    if man and dv["built"]:
        stamp = re.sub(r"\D", "", dv["built"])[2:8]
        rows.append({"run_id": "compile-" + stamp, "global_id": "compile-" + stamp, "status": "done",
                     "target": "the whole paper", "result": "delivery/build-manifest.json",
                     "result_path": dv["dir"], "goal": "%s · built %s" % (man.get("status") or "", dv["built"]),
                     "_display": "run-compile-" + stamp, "_place": "Build"})
    for r in d["rounds"]:
        fill = {"page": r["stem"], "paper": d["board"].name}
        for row in _page_runs(d, r):
            rows += [dict(x, _place="Response") for x in _tag([row], [r["stem"]], fill)]
    cover = _cover(d)
    if cover is not None:                             # the build's one fixed cover-letter run
        rows.append({"run_id": "run-delivery-coverletter", "global_id": "run-delivery-coverletter",
                     "status": "done" if cover.get("ready") else "held", "target": cover.get("round") or "the letter",
                     "result": ((cover.get("outputs") or {}).get("pdf") or ""), "result_path": dv["dir"],
                     "goal": "from " + (cover.get("from") or "?"), "_display": "run-delivery-coverletter",
                     "_place": "Cover letter", "_views": "cover"})
    rows = _tag(rows)
    fill = {"page": d["board"].name, "paper": d["board"].name}
    return _panel(d, "delivery", kinds, _bucket(kinds, rows, lambda r: r.get("_place")), fill, "the manuscript")


# ---- the Spaces --------------------------------------------------------------
def _space(space, main, panel, tabs=(), views=(), noviews=()):
    """One Space: its tabs and views over the content, its Runs panel beside it."""
    tab_row = ('<div class="space-tabs">%s</div>' % "".join(
        '<button type=button class="space-tab%s" data-tab="%s" data-label="%s"%s>%s</button>'
        % (" on" if i == 0 else "", k, esc(label), " data-noviews" if k in noviews else "", esc(label))
        for i, (k, label) in enumerate(tabs))) if tabs else ""
    view_row = ('<div class="space-views"><span class="space-views-label">View</span>%s</div>' % "".join(
        '<button type=button class="space-view%s" data-view="%s">%s</button>' % (" on" if i == 0 else "", k, esc(label))
        for i, (k, label) in enumerate(views))) if views else ""
    return ('<div class="panel space-split" data-space="%s"><div class="space-main">%s%s%s</div>%s</div>'
            % (space, tab_row, view_row, main, panel))


def _pane(html_, tab="", view=""):
    return '<div class="space-pane"%s%s>%s</div>' % (
        (' data-tab="%s"' % tab) if tab else "", (' data-view="%s"' % view) if view else "", html_)


def _cards(cards, empty):
    return '<div class="item-cards">%s</div>' % "".join(cards) if cards else '<div class="space-empty">%s</div>' % esc(empty)


def render_ideation(d, kinds):
    i = d["ideation"]
    if not i["present"]:
        main = _pane('<div class="space-empty">No Story00-ideation page yet.</div>')
    else:
        main = _pane(_cards([_idea_card(d, i, x) for x in i["ideas"]], "No idea yet."))
    return _space("ideation", main, _ideation_panel(d, kinds))


def _spine_html(d):
    out = []
    many = sum(1 for s in d["story"] if re.match(r"^Story[A-Z]", s["stem"])) > 1
    for s in d["story"]:
        if many:
            out.append('<h3 class="story-name">%s</h3>' % esc(s["stem"]))
        for n, title, (face, subs, paras) in s["spine"]:
            rows = [(k, inline(v)) for k, v in face]
            if paras:
                rows.append(("", prose(paras)))
            rows += [(sub, prose(pg)) for sub, pg in subs if pg]
            out.append('<div class="card spine-card" data-key="C%d"><h2>C%d · %s<span class="tally">%s</span></h2>%s</div>'
                       % (n, n, esc(title), _link(d, s["rel"], "Open ↗", focus="C%d" % n),
                          _kv(rows, "spine-row") or '<div class="space-empty">Empty.</div>'))
    return "".join(out) or '<div class="space-empty">No Story yet.</div>'


def _dd_cards(d, s):
    """One card per C6 row: what the paper must learn, and the inquiry it names."""
    cards = []
    for c in s["dd"]:
        rows = _fields(s["dd_h"], c, {0, 1} | _skip_cols(s["dd_h"], "folder", "q"))
        addrs = [a for a in _addresses(" ".join(c)) if _disc_lookup(d, a)]
        folders, _ = _disc_cards(d, addrs, _disc_feeds(d)) if addrs else ([], [])
        body = ('<div class="item-cards">%s</div>' % "".join(_open_cards(folders)) if folders
                else '<div class="space-empty">No folder yet.</div>')
        cards.append(_card("need-" + c[0], c[0], c[1] if len(c) > 1 else "", "", "", "", "mut",
                           rows, key=c[0], body=body, fold=True))
    return cards


def _q_of(headers, row):
    """The general question a T or D row names in its `Q` column ('' when none)."""
    i = next((k for k, h in enumerate(headers) if h.strip().upper() == "Q"), None)
    return row[i].strip() if i is not None and i < len(row) else ""


def _question_cards(d, s):
    """JL 260928: a few general questions; under each, its T and D questions; under each
    of those, the BJTR folders that answer it. A T or D row with no Q comes last."""
    tasks = dict(zip((c[0] for c in s["tt"]), _task_cards(d, s)))
    needs = dict(zip((c[0] for c in s["dd"]), _dd_cards(d, s)))
    q_of = {c[0]: _q_of(s["tt_h"], c) for c in s["tt"]}
    q_of.update({c[0]: _q_of(s["dd_h"], c) for c in s["dd"]})
    has = {c[0]: bool(task_home(d, c)["all"]) for c in s["tt"]}
    has.update({c[0]: any(_disc_lookup(d, a) for a in _addresses(" ".join(c))) for c in s["dd"]})
    cards = []
    for q in s["qq"]:
        mine = [k for k, v in q_of.items() if v == q[0]]
        inner = [tasks[k] for k in mine if k in tasks] + [needs[k] for k in mine if k in needs]
        with_folder = sum(1 for k in mine if has[k])
        rows = [("Rows", esc(" · ".join(mine) or "none yet"))]
        if inner:
            rows.append(("Questions", '<div class="item-cards">%s</div>' % "".join(inner)))
        rq = " · ".join(q[2:3]) if len(q) > 2 else ""
        status = "%d of %d with a folder" % (with_folder, len(mine)) if mine else "no T or D yet"
        cards.append(_card("q-" + q[0], q[0], q[1] if len(q) > 1 else q[0], "", esc(rq), status,
                           "ok" if mine and with_folder == len(mine) else ("warn" if with_folder else "mut"),
                           rows, key=q[0]))        # its runs carry Q<n> among their keys
    loose = [tasks[k] for k, v in q_of.items() if not v and k in tasks] + \
            [needs[k] for k, v in q_of.items() if not v and k in needs]
    return cards, loose


def render_story(d, kinds):
    if not d["story"]:
        empty = '<div class="space-empty">No Story yet.</div>'
        return _space("story", "".join(_pane(empty, k) for k, _ in STORY_TABS), _story_panel(d, kinds), STORY_TABS)
    questions = [c for s in d["story"] for c in _rq_cards(d, s)]
    roadmap = []
    if any(s["qq"] for s in d["story"]):
        general, loose = [], []
        for s in d["story"]:
            g, l = _question_cards(d, s)
            general += g
            loose += l
        roadmap.append('<h3 class="space-h">Questions</h3>' + _cards(general, ""))
        if loose:
            roadmap.append('<h3 class="space-h">No general question yet</h3>' + _cards(loose, ""))
    else:                                            # a Story with no Q table: T and D rows as they are
        tasks = [c for s in d["story"] for c in _task_cards(d, s)]
        needs = [c for s in d["story"] for c in _dd_cards(d, s)]
        roadmap.append('<h3 class="space-h">Task questions</h3>' + _cards(tasks, "No C7 row yet."))
        if needs:
            roadmap.append('<h3 class="space-h">Discovery questions</h3>' + _cards(needs, ""))
    unnamed = _unnamed_cards(d)
    if unnamed:
        roadmap.append('<h3 class="space-h">Folders no question names yet</h3>' + _cards(unnamed, ""))
    main = (_pane(_spine_html(d), "spine")
            + _pane(_cards(questions, "No research question yet."), "questions")
            + _pane("".join(roadmap), "roadmap"))
    return _space("story", main, _story_panel(d, kinds), STORY_TABS)


def section_rows(d):
    """Every Section of the paper in compile order: the Story's C8 rows joined to
    their Section Pages, then any Section Page no C8 row names."""
    by_id, heads = {}, {}
    for s in d["story"]:
        for r in s["sections"]:
            by_id.setdefault(r["id"], r)
            heads.setdefault(r["id"], r.get("heads") or s["sec_h"])
    order = next((s["order"] for s in d["story"] if s["order"]), [])
    ids = [x for x in order] + [x for x in by_id if x not in order]
    ids += [p["stem"] for p in d["sections"] if p["stem"] not in ids]
    pages = {p["stem"]: p for p in d["sections"]}
    sessions = {r["stem"]: r for r in d.get("sessions", [])}
    out = []
    for sid in ids:
        page = pages.get(sid)
        page = page if page and page["rel"] else None
        # S-<desk>-<Main|Appendix>-[<N>-]<Title>; a desk may carry a hyphen (JAMA-IM)
        m = re.match(r"^S-.+?-(?:Main|Appendix)-(?:([0-9]+|[A-Z])-)?(.+)$", sid)
        num, name = ((m.group(1) or ""), m.group(2).replace("-", " ")) if m else ("", sid)
        c8_num = (by_id.get(sid) or {}).get("target", "")
        if not num and re.fullmatch(r"[0-9]+|[A-Z]", c8_num):
            num = c8_num                    # a record's `(0)`: the Abstract's place in the order
        version = ""
        if page:
            plan = latest_outline(plan_dir((d["board"] / page["rel"]).parent), sid)
            version = version_tag(plan) if plan else ""
        state = clean(scalar(page["text"], "state", "")).split("·")[0].strip() if page else "not set up"
        out.append({"id": sid, "part": "appendix" if "-Appendix-" in sid else "main", "num": num,
                    "name": name, "page": page, "version": version, "state": state,
                    "row": by_id.get(sid), "heads": heads.get(sid, []), "session": sessions.get(sid)})
    return out


def _section_table(d, rows):
    out = []
    for r in rows:
        opener = ('<a class="sec-open" href="%s">Open ↗</a>' % esc(outline_url(d["path"], r["page"]["rel"]))
                  if r["page"] else "")
        out.append('<div class="sec-row" data-key="%s" tabindex="0" title="%s"><span class="sec-num">%s</span>'
                   '<span class="sec-name">%s</span><span class="sec-ver">%s</span>'
                   '<span class="sec-state %s">%s</span>%s</div>'
                   % (esc(r["id"]), esc(r["id"]), esc(r["num"]), esc(r["name"]), esc(r["version"]),
                      _status_cls(r["state"]) if r["page"] else "warn", esc(r["state"]), opener))
    return '<div class="sec-list">%s</div>' % "".join(out) if out else '<div class="space-empty">No Section yet.</div>'


def _narrative_cards(d, rows):
    cards = []
    for r in rows:
        c8 = r["row"]
        fields = _fields(r["heads"], c8["cells"], {0, 1}) if c8 else []
        if r["session"]:
            sess = r["session"]
            if not sess["pair"]:                # a Claude session with no Codex pair yet
                fields.append(("Session", esc(sess["state"])))
            else:
                fields.append(("Session", '<code>%s</code>%s' % (esc(sess["pair"]), "" if sess["state"].startswith("no ")
                                                                  else " · " + esc(sess["state"]))))
        label = (c8["question"] if c8 and c8["question"] else r["name"])
        cards.append(_card("section-" + r["id"], r["num"] or "·", label, esc("%s %s" % (r["num"], r["name"])).strip(),
                           "", r["state"], _status_cls(r["state"]) if r["page"] else "warn", fields, key=r["id"]))
    return cards


def render_sections(d, kinds):
    rows = section_rows(d)
    main = ""
    for tab, _ in SECTION_TABS:
        mine = [r for r in rows if r["part"] == tab]
        hero = [c for c in _hero_cards(d) if ('data-part="%s"' % tab) in c]
        main += (_pane(_section_table(d, mine), tab, "table")
                 + _pane(_cards(_narrative_cards(d, mine), "No Section yet."), tab, "narrative")
                 + _pane(_cards(hero, "No Display or Value yet."), tab, "evidence"))
    return _space("sections", main, _sections_panel(d, kinds, rows), SECTION_TABS, SECTION_VIEWS)


def _outputs(d, suffix):
    return [o for o in d["delivery"]["outputs"] if o["rel"].endswith(suffix)]


def _output_rows(d, outs):
    rows = []
    for o in outs:
        st = ("✅ built" + (" · stale" if o["stale"] else "")) if o["exists"] else "⬜ not built"
        rows.append((esc(o["what"]), _file_link(d, o["path"], o["rel"]) if o["exists"] else esc(o["rel"]),
                     '<span class="%s">%s</span>' % (_status_cls(st), esc(st)), esc(o["size"]), esc(o["stamp"])))
    return rows


def _checks_html(d):
    dv = d["delivery"]
    man = dv["manifest"] or {}
    if not man:
        return '<div class="space-empty">No build yet.</div>'
    build, sub, rd = man.get("build") or {}, man.get("submission_readiness") or {}, man.get("readiness") or {}
    facts = []
    if build:
        facts += [("main text", "%s words%s" % (build.get("main_text_words", "?"), (" · limit %s" % build["main_text_word_limit"])
                                                if build.get("main_text_word_limit") else "")),
                  ("citations", "%s cited · %s bib entries" % (build.get("citations", "?"), man.get("bib_entries", "?"))),
                  ("displays", "%s main table(s) · %s main figure(s)" % (build.get("main_tables", "?"), build.get("main_figures", "?"))),
                  ("pages ready", "%s of %s%s" % (rd.get("ready", "?"), rd.get("total", "?"),
                                                   (" · not ready: " + ", ".join(_not_ready_ids(rd))) if rd.get("not_ready") else "")),
                  ("submission", "%s%s" % (sub.get("status", "?"), (" · " + "; ".join(sub.get("blockers") or [])) if sub.get("blockers") else ""))]
    if dv["stale"]:
        facts.append(("changed since build", ", ".join(dv["stale"])))
    g4 = next((v for g, _, v in d["gates"] if g == "G4"), "")
    if g4:
        facts.append(("G4 compile", g4))
    crs = [(esc(k.replace("_", " ")), _yn(v) if isinstance(v, bool) else '<span class="mut">%s</span>' % esc(str(v)))
           for k, v in (build.get("checks") or {}).items()]
    render = man.get("render") or {}
    if render:
        crs.append(("latexmk", _yn(render.get("latexmk_rc") == 0)))
        crs.append(("docx", _yn(render.get("docx_rc") == 0)))
    pages = []
    for i, p in enumerate(dv["pages"], 1):
        notes = list(p["reasons"]) + list(p["warnings"]) + (["changed since build"] if p["stale"] else [])
        pages.append((esc(p["id"]), _yn(p["frag"]),
                      _yn(p["ready"]) if p["ready"] is not None else '<span class="mut">—</span>', esc("; ".join(notes))))
    # engine ≥0.8 writes each unresolved \ref as {"page", "ref"}; older manifests wrote a bare string
    warns = [w if isinstance(w, str) else json.dumps(w, ensure_ascii=False) for w in (man.get("warnings") or [])] + [
        "unresolved \\ref: " + (x if isinstance(x, str) else "%s (%s)" % (x.get("ref", "?"), x.get("page", "?")))
        for x in (man.get("unresolved_refs") or [])]
    return (_kv([(k, esc(v)) for k, v in facts], "spine-row")
            + _table(["check", "result"], crs)
            + _table(["page", "fragment", "ready", "notes"], pages)
            + (('<ul class="item-bullets">%s</ul>' % "".join("<li>%s</li>" % esc(w) for w in warns)) if warns else ""))


def _preview_html(d, suffix):
    outs = [o for o in _outputs(d, suffix) if o["exists"]]
    if not outs:
        return '<div class="space-empty">Not built yet.</div>'
    main = next((o for o in outs if "main" in o["what"]), outs[0])
    if suffix == ".pdf":
        return '<iframe class="space-frame" title="%s" data-src="%s"></iframe>' % (esc(main["rel"]), esc(_tree_url(d, main["path"])))
    # JL 260929 "for the word, why we cannot preview it": the paper build draws a PDF twin of each .docx
    # beside it (<stem>.pdf, from the package itself); Preview shows it under one line naming the .docx
    twin = Path(main["path"]).with_suffix(".pdf")
    if twin.is_file():
        stale = twin.stat().st_mtime < Path(main["path"]).stat().st_mtime
        return ('<p class="mut">%s · %s · %s%s</p><iframe class="space-frame" title="%s" data-src="%s"></iframe>'
                % (_file_link(d, main["path"], main["rel"]), esc(main["size"]), esc(main["stamp"]),
                   " · the preview is older than the .docx; rebuild" if stale else "",
                   esc(main["rel"]), esc(_tree_url(d, twin))))
    return _kv([("file", _file_link(d, main["path"], main["rel"])), ("size", esc(main["size"])),
                ("written", esc(main["stamp"])),
                ("preview", '<span class="mut">none yet: the next paper build draws it</span>')], "spine-row")


def _artifacts_html(d, suffix):
    dv = d["delivery"]
    html_ = _table(["what", "file", "state", "size", "written"], _output_rows(d, _outputs(d, suffix)))
    if suffix == ".pdf":
        drs = [(esc(r[0]), esc(r[1]), '<code>%s</code>' % esc(r[2]), esc(r[3]), esc(r[4])) for r in dv["displays"]]
        html_ += _table(["printed", "declared", "label", "unit", "page"], drs)
        html_ += _table(["asset", "size"], [(_file_link(d, a["path"], a["name"]), esc(a["size"])) for a in dv["assets"]])
    else:
        html_ += _table(["returned", "size", "written"], [(_file_link(d, r["path"], r["rel"]), esc(r["size"]), esc(r["stamp"]))
                                                         for r in dv["returned"]])
    return html_ or '<div class="space-empty">Not built yet.</div>'


def _round_cards(d):
    cards = []
    for r in d["delivery"]["rounds"]:
        rows = [(k, esc(v)) for k, v in (("kind", r["kind"]), ("received", " · ".join(x for x in (r["from"], r["at"]) if x)),
                                          ("response due", r["due"]), ("base build", r["base"]),
                                          ("folders", " · ".join(r["subs"]))) if v]
        rows.append(("page", _link(d, r["rel"], "Open ↗")))
        if r["state"]:
            rows.insert(0, ("state", esc(r["state"])))
        cards.append(_card("round-" + r["stem"], r["stem"][:4], r["stem"], esc(r["kind"]), "",
                           r["state"].split("·")[0].strip(), _status_cls(r["state"]), rows, key=r["stem"]))
    venue = d["delivery"]["links"].get("venue-page", "")
    tail = _kv([("venue", _file_link(d, (d["board"] / venue).resolve(), Path(venue).stem))], "spine-row") if venue else ""
    return _cards(cards, "No round yet.") + tail


def _cover(d):
    """The cover letter as the paper build recorded it (haipipe-paper-assemble 0.9.0,
    run-delivery-coverletter): build-manifest.json `cover_letter`, or None."""
    man = d["delivery"]["manifest"] or {}
    return man.get("cover_letter") if isinstance(man.get("cover_letter"), dict) else None


def _cover_panes(d):
    """Cover letter tab (JL 260929: one more delivery item). The words live on the submission
    Round page's Cover letter division; the paper build writes the letter and its checks; this
    tab only reads that record."""
    cover = _cover(d)
    if cover is None:
        empty = ('<div class="space-empty">No cover letter built yet: add a <code>[coverletter]</code> '
                 'block to delivery/paper-build.toml and run the build.</div>')
        return "".join(_pane(empty, "cover", v) for v, _ in DELIVERY_VIEWS)
    base = d["delivery"]["dir"]
    outs = {k: (base / v) if v and not Path(v).is_absolute() else (Path(v) if v else None)
            for k, v in (cover.get("outputs") or {}).items()}
    src = cover.get("source") or ""
    head = '<div class="space-h">%s · %s%s</div>' % (
        esc(cover.get("round") or "letter"), "ready" if cover.get("ready") else "not ready",
        (" · " + _link(d, src.split("/draft/")[0] + "/" + Path(src.split("/draft/")[0]).name + ".md", "Open ↗",
                       lens="div")) if src else "")
    pdf = outs.get("pdf")
    preview = head + (('<iframe class="space-frame" title="cover letter" data-src="%s"></iframe>'
                       % esc(_tree_url(d, pdf))) if pdf and pdf.is_file() else '<div class="space-empty">Not built yet.</div>')
    files = [(_file_link(d, f, f.name), esc(_stamp(f))) for f in outs.values() if f and f.is_file()]
    artifacts = head + (_table(["file", "written"], files) if files else '<div class="space-empty">Not built yet.</div>')
    rows = [(esc(c.get("check", "")), '<span class="%s">%s</span>' % ("ok" if c.get("ok") else "warn", "✅" if c.get("ok") else "⚠️"),
             esc(c.get("detail", ""))) for c in cover.get("checks") or []]
    checks = head + (_table(["check", "", "detail"], rows) or '<div class="space-empty">No checks recorded.</div>')
    return (_pane(preview, "cover", "preview") + _pane(artifacts, "cover", "artifacts")
            + _pane(checks, "cover", "checks"))


def render_delivery(d, kinds):
    main = ""
    for tab, suffix in (("latex", ".pdf"), ("word", ".docx")):
        if d["delivery"]["dir"] is None:
            empty = '<div class="space-empty">No delivery/ yet.</div>'
            main += "".join(_pane(empty, tab, v) for v, _ in DELIVERY_VIEWS)
            continue
        main += (_pane(_preview_html(d, suffix), tab, "preview") + _pane(_artifacts_html(d, suffix), tab, "artifacts")
                 + _pane(_checks_html(d), tab, "checks"))
    main += _cover_panes(d)
    main += _pane(_round_cards(d), "rounds")
    return _space("delivery", main, _delivery_panel(d, kinds), DELIVERY_TABS, DELIVERY_VIEWS, noviews=("rounds",))


_PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>
:root{{--bg:#ffffff;--fg:#1c1c1c;--mut:#7c7c78;--line:#e4e4e7;--card:#fff;
 --warn:#b3541e;--ok:#3a7d44;--acc:#3e5c84;--soft:#f6f7f9}}
@media(prefers-color-scheme:dark){{:root{{--bg:#161719;--fg:#e8e8e6;
 --mut:#9a9a97;--line:#2c2e33;--card:#1d1f23;--warn:#e0955a;--ok:#7dbb87;
 --acc:#7d9cc4;--soft:#1b1d21}}}}
body{{margin:0;padding:18px;background:var(--bg);color:var(--fg);
 font:16px/1.65 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}}
h1{{font-size:20px;margin:0 0 2px}} .mut{{color:var(--mut)}}
.spaces{{display:flex;gap:6px;margin:10px 0 10px;flex-wrap:wrap}}
.space{{font:600 13px -apple-system,sans-serif;border:1px solid var(--line);border-radius:9px;padding:5px 12px;
 cursor:pointer;background:var(--card);color:var(--fg);white-space:nowrap}}
.space.on{{border-color:var(--acc);color:var(--acc)}}
.panel{{display:none}} .panel.on{{display:block}}
.panel.on.space-split{{display:flex;align-items:flex-start;gap:16px}}
.space-views[hidden]{{display:none}}
.space-frame{{height:calc(100vh - 170px)}}
.space-h{{font-size:15px;margin:18px 0 6px}} .space-h:first-child{{margin-top:0}}
.story-name{{font:600 13px ui-monospace,Menlo,monospace;color:var(--mut);margin:14px 0 6px}}
.ok{{color:var(--ok);font-weight:600}} .warn{{color:var(--warn);font-weight:600}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin:0 0 14px}}
.card h2{{font-size:17px;margin:0 0 8px;display:flex;gap:8px;align-items:baseline}}
.card h2 .tally{{margin-left:auto;flex:none;font-size:13px;font-weight:500}}
.spine-card{{cursor:pointer}}
.runs-selected.spine-card,.item-card.runs-selected{{border-color:var(--acc);box-shadow:0 0 0 1px var(--acc)}}
table.grid{{width:100%;font-size:14.5px;line-height:1.55;border:1px solid var(--line);border-radius:9px;
 border-collapse:separate;border-spacing:0;overflow:hidden;margin:6px 0 12px}}
table.grid th{{text-align:left;background:var(--soft);font:600 11.5px -apple-system,sans-serif;text-transform:uppercase;
 letter-spacing:.03em;padding:9px 11px;border-bottom:1px solid var(--line);border-right:1px solid var(--line);opacity:.8}}
table.grid td{{padding:9px 11px;border-bottom:1px solid var(--line);border-right:1px solid var(--line);vertical-align:top}}
table.grid th:last-child,table.grid td:last-child{{border-right:0}} table.grid tr:last-child td{{border-bottom:0}}
.idtag,.path{{font:500 12.5px ui-monospace,Menlo,monospace;color:var(--mut)}} .path{{overflow-wrap:anywhere}}
.bjt details>summary{{list-style:none;cursor:pointer;display:flex;flex-wrap:wrap;align-items:baseline;gap:6px;padding:6px 2px;line-height:1.5}}
.bjt details>summary::-webkit-details-marker{{display:none}} .bjt summary b{{font-weight:650}}
.bjt-chev{{color:var(--mut);display:inline-block;width:1em;text-align:center;transition:transform .12s ease}}
.bjt details[open]>summary>.bjt-chev{{transform:rotate(90deg)}}
.bjt-j,.bjt-b>.bjt-o{{margin-left:22px}} .bjt>.bjt-j,.bjt>.bjt-o{{margin-left:0}}
table.grid.bjt-t{{width:calc(100% - 22px);margin:2px 0 10px 22px}} .bjt-o{{font-size:13px;padding:4px 2px}}
code{{font:12.5px ui-monospace,Menlo,monospace}}
.sec-list{{display:grid;border:1px solid var(--line);border-radius:10px;overflow:hidden}}
.sec-row{{display:grid;grid-template-columns:2.4em minmax(0,1fr) 4.5em 12em 4.5em;gap:10px;align-items:baseline;
 padding:9px 12px;border-top:1px solid var(--line);cursor:pointer}}
.sec-row:first-child{{border-top:0}}
.sec-row:hover{{background:var(--soft)}}
.sec-row.runs-selected{{background:color-mix(in srgb,var(--acc) 9%,var(--card));box-shadow:inset 3px 0 0 var(--acc)}}
.sec-num,.sec-ver{{font:500 13px ui-monospace,Menlo,monospace;color:var(--mut)}} .sec-name{{font-weight:600}}
.sec-state{{font-size:13px;overflow-wrap:anywhere}} .sec-open{{font-size:13px;text-align:right;white-space:nowrap}}
.item-cards{{display:grid;gap:9px;margin:0 0 12px}}
.item-card{{border:1px solid var(--line);border-radius:10px;background:var(--bg);overflow:hidden;margin:0}}
.item-card:hover{{border-color:#b8c4d2}}
.item-card>summary{{list-style:none;cursor:pointer;padding:0}}
.item-card>summary::-webkit-details-marker{{display:none}}
.item-summary{{display:grid;grid-template-columns:1.1em auto minmax(0,1fr) auto fit-content(34%);align-items:start;gap:10px;padding:12px 13px;min-width:0}}
.item-chevron{{color:var(--mut);font-size:18px;line-height:1.2;transition:transform .12s ease}}
.item-card[open]>summary .item-chevron{{transform:rotate(90deg)}}
.item-kind{{color:var(--acc);font:650 12px ui-monospace,Menlo,monospace;border:1px solid var(--acc);border-radius:999px;
 padding:1px 8px;white-space:nowrap}}
.item-main{{min-width:0;display:grid}}
.item-label{{font-weight:650;font-size:15.5px;line-height:1.4}} .item-title{{color:var(--mut);font-size:13.5px}}
.item-where{{color:var(--mut);font-size:12px;white-space:nowrap}} .item-status{{font-weight:650;font-size:14px;line-height:1.4;overflow-wrap:anywhere}}
.item-detail{{border-top:1px solid var(--line);padding:10px 12px 13px}}
.item-detail td .idtag,.item-detail td:first-child{{white-space:nowrap}}
.row-details{{margin-top:8px}} .row-details>summary{{cursor:pointer;color:var(--mut);font-size:12px;list-style:none}}
.row-details>summary::before{{content:"▸ "}} .row-details[open]>summary::before{{content:"▾ "}}
.item-bullets{{margin:0;padding-left:1.1em;font-size:14.5px}} .item-bullets li{{margin:2px 0}}
.item-bullets b{{font:500 12px ui-monospace,Menlo,monospace;color:var(--mut)}}
.item-note{{color:var(--mut);font-size:12.5px;line-height:1.45}} .item-sub{{color:var(--mut);font-size:12px;text-transform:uppercase;margin-right:4px}}
.item-plan>summary{{cursor:pointer;color:var(--mut);font-size:13px}}
.kv{{border:1px solid var(--line);border-radius:9px;overflow:hidden;margin:8px 0 10px;background:var(--card)}}
.kv>.item-row{{display:grid;grid-template-columns:11.5em minmax(0,1fr);border-top:1px solid var(--line);font-size:14.5px;line-height:1.6}}
.kv>.item-row:first-child{{border-top:0}}
.kv>.item-row>b{{background:var(--soft);border-right:1px solid var(--line);padding:11px 12px;font-size:11.5px;line-height:1.45;
 text-transform:uppercase;letter-spacing:.03em;font-weight:700;opacity:.75}}
.kv>.item-row>span{{padding:10px 14px;min-width:0;overflow-wrap:anywhere}}
.kv>.item-row.spine-row{{font-size:16px;line-height:1.75}}
.kv>.item-row.nolabel{{grid-template-columns:minmax(0,1fr)}}
.kv-cap{{background:var(--soft);border-bottom:1px solid var(--line);padding:6px 12px;font:700 11.5px -apple-system,sans-serif;
 text-transform:uppercase;letter-spacing:.03em;opacity:.75}}
.para{{display:block;max-width:86ch}} .para+.para{{margin-top:12px}} .sent{{display:block}} .sent+.sent{{margin-top:7px}}
.tree-job{{font-size:14.5px;margin:12px 0 4px;font-weight:650}} .tree-task{{font-size:14px;margin:8px 0 4px 18px}}
.tree-runs{{margin:0 0 6px 36px;border-left:2px solid var(--line);padding-left:10px}}
a{{color:var(--acc);text-decoration:none}} a:hover{{text-decoration:underline}}
@media(max-width:620px){{.kv>.item-row{{grid-template-columns:minmax(0,1fr)}}
 .kv>.item-row>b{{border-right:0;border-bottom:1px solid var(--line);padding:6px 12px}}
 .sec-row{{grid-template-columns:2em minmax(0,1fr) auto}} .sec-ver,.sec-state{{display:none}}
 .item-summary{{grid-template-columns:1.1em auto minmax(0,1fr) fit-content(40%)}} .item-where{{display:none}}}}
{space_css}{panel_css}
/* the paper's 12px type floor (JL 260918) holds inside the Runs panel too */
.runs-panel button,.run-list button{{font-size:12px!important}} .run-state{{font-size:12px}} .space-views-label{{font-size:12px}}
</style></head><body data-paper="{paper_id}">
<h1>📄 {title}</h1>
<div class="spaces">{space_chips}</div>
{panels}
<script>{panel_js}</script>
<script>
(function(){{
 var DEFAULT='{default_space}';
 /* the pre-260927 routes (five Spaces) still land on the view that holds their content */
 var ALIAS={{'setup':'sections','run':'sections','run/page':'sections/table','run/evidence':'sections/evidence',
  'run/supporting':'story/roadmap','run/gates':'delivery/latex/checks','run/workflow':'story',
  'ideation/pool':'ideation','ideation/evidence':'ideation','ideation/admission':'ideation',
  'story/claims':'story/questions','story/tasks':'story/roadmap','story/sections':'sections/narrative',
  'story/evidence':'sections/evidence','delivery/manuscript':'delivery/latex/artifacts',
  'delivery/sections':'sections/table','delivery/displays':'delivery/latex/artifacts',
  'delivery/checks':'delivery/latex/checks','setup/sessions':'sections/narrative'}};
 var panels={{}};
 document.querySelectorAll('.panel[data-space]').forEach(function(p){{panels[p.dataset.space]=p;}});
 function emit(name,detail){{document.dispatchEvent(new CustomEvent(name,{{detail:detail}}));}}
 function clearSel(p){{p.querySelectorAll('.runs-selected').forEach(function(x){{x.classList.remove('runs-selected');}});}}
 function lazy(p){{p.querySelectorAll('iframe[data-src]').forEach(function(f){{
  if(!f.closest('[hidden]')&&!f.getAttribute('src'))f.setAttribute('src',f.dataset.src);}});}}
 function pick(space,parts){{
  var p=panels[space];if(!p)return;
  document.querySelectorAll('.space').forEach(function(c){{c.classList.toggle('on',c.dataset.space===space);}});
  Object.keys(panels).forEach(function(k){{panels[k].classList.toggle('on',k===space);}});
  var tabs=[].slice.call(p.querySelectorAll('.space-tab')),views=[].slice.call(p.querySelectorAll('.space-view'));
  function has(list,key,v){{return list.some(function(x){{return x.dataset[key]===v;}});}}
  function cur(list,key){{var on=list.filter(function(x){{return x.classList.contains('on');}})[0]||list[0];return on?on.dataset[key]:'';}}
  var tab=cur(tabs,'tab'),view=cur(views,'view');
  parts.forEach(function(x){{if(has(tabs,'tab',x))tab=x;else if(has(views,'view',x))view=x;}});
  tabs.forEach(function(x){{x.classList.toggle('on',x.dataset.tab===tab);}});
  views.forEach(function(x){{x.classList.toggle('on',x.dataset.view===view);}});
  var tb=tabs.filter(function(x){{return x.dataset.tab===tab;}})[0],noviews=!!(tb&&tb.hasAttribute('data-noviews'));
  var row=p.querySelector('.space-views');if(row)row.hidden=noviews;
  p.querySelectorAll('.space-pane').forEach(function(q){{
   q.hidden=!((!q.dataset.tab||q.dataset.tab===tab)&&(noviews||!q.dataset.view||q.dataset.view===view));}});
  lazy(p);
  if(p.dataset.tab!==tab||p.dataset.vw!==view){{
   if(p.dataset.tab!==undefined){{clearSel(p);emit('space-target',{{space:space,target:''}});}}
   p.dataset.tab=tab;p.dataset.vw=view;}}
  emit('space-scope',{{space:space,view:tab||view,label:tb?tb.dataset.label:'',mode:noviews?tab:(view||tab)}});
 }}
 function route(){{
  var h=decodeURIComponent((location.hash||'').slice(1));
  if(ALIAS[h])h=ALIAS[h];else if(ALIAS[h.split('/')[0]])h=ALIAS[h.split('/')[0]];
  var parts=h.split('/');
  pick(panels[parts[0]]?parts[0]:DEFAULT,parts.slice(1));
 }}
 document.addEventListener('click',function(ev){{
  var c=ev.target.closest('.space,.space-tab,.space-view');
  if(c){{
   var p=c.closest('.panel'),space=c.dataset.space||(p&&p.dataset.space);
   var parts=c.dataset.space?[]:[c.dataset.tab||c.dataset.view];
   pick(space,parts);
   var q=panels[space],t=q.dataset.tab,v=q.dataset.vw;
   history.replaceState(null,'','#'+space+(t?'/'+t:'')+(v?'/'+v:''));
   return;
  }}
  if(ev.target.closest('a,button,summary,.runs-panel'))return;
  var el=ev.target.closest('.sec-row[data-key],.spine-card[data-key]');if(!el)return;
  var panel=el.closest('.panel'),same=el.classList.contains('runs-selected');
  clearSel(panel);if(!same)el.classList.add('runs-selected');
  emit('space-target',{{space:panel.dataset.space,target:same?'':el.dataset.key}});
 }});
 document.addEventListener('keydown',function(ev){{var r=ev.target.closest&&ev.target.closest('.sec-row');if(r&&ev.key==='Enter')r.click();}});
 /* Opening a card selects it for the Runs panel; closing it hands the selection back to the card around it. */
 document.addEventListener('toggle',function(ev){{
  var c=ev.target;if(!c.matches||!c.matches('details.item-card[data-key]'))return;
  var p=c.closest('.panel');if(!p)return;
  if(c.open){{clearSel(p);c.classList.add('runs-selected');emit('space-target',{{space:p.dataset.space,target:c.dataset.key}});return;}}
  if(!c.classList.contains('runs-selected'))return;
  c.classList.remove('runs-selected');
  var up=c.parentElement.closest('details.item-card[data-key][open]');
  if(up)up.classList.add('runs-selected');
  emit('space-target',{{space:p.dataset.space,target:up?up.dataset.key:''}});
 }},true);
 window.addEventListener('hashchange',route);route();
}})();
</script></body></html>"""


def render_paper(board, root, path_param):
    from live.runs_panel import PANEL_CSS, PANEL_JS
    from live.space_views import SPACE_CSS
    d = collect(board, path_param)
    d["root"] = Path(root).resolve()
    d["sessions"] = session_rows(d)          # needs root for the pair lookup
    kinds = paper_run_types()
    chips = "".join('<button type=button class="space" data-space="%s">%s</button>' % (k, l) for k, l in SPACES)
    panels = (render_ideation(d, kinds.get("ideation", [])) + render_story(d, kinds.get("story", []))
              + render_sections(d, kinds.get("sections", [])) + render_delivery(d, kinds.get("delivery", [])))
    default = "story" if d["story"] else "ideation"
    return _PAGE.format(title=esc(d["title"]), space_chips=chips, panels=panels, default_space=default,
                        space_css=SPACE_CSS, panel_css=PANEL_CSS, panel_js=PANEL_JS,
                        paper_id=esc(d["board"].name))


# ---------------------------------------------------------------- the route
class PaperWorkbenchMixin:
    """GET /_board/paper — the Board-level Paper Workbench, rendered live."""

    def paper_view(self, head_only=False):
        q = parse_qs(urlparse(self.path).query)
        p = {"path": (q.get("path") or [""])[0], "file": (q.get("file") or [""])[0]}
        got = self.target(p)
        if got[0] is None:
            return self._paper_send(("<h1>📄 paper</h1><p>%s</p>" % esc(got[1])).encode("utf-8"), 404, head_only)
        source, board = got
        if Path(source).name != "board.md":
            return self._paper_send("<h1>📄 paper</h1><p>Paper Workbench requires file=board.md.</p>".encode("utf-8"), 400, head_only)
        if scalar(read(Path(board) / "board.md"), "dialect").strip() != "paper":
            return self._paper_send("<h1>📄 paper</h1><p>This Board is not a paper Board (board.md has no <code>dialect: paper</code>).</p>".encode("utf-8"), 400, head_only)
        try:
            page = render_paper(board, self.root, p["path"])
        except Exception as exc:  # a render bug is a named row, never a blank pane
            return self._paper_send(("<h1>📄 paper</h1><p>render failed: %s</p>" % esc(exc)).encode("utf-8"), 500, head_only)
        return self._paper_send(page.encode("utf-8"), 200, head_only)

    def _paper_send(self, body, code, head_only):
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(body)
