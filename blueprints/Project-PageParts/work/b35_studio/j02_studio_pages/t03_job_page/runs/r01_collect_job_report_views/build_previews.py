"""Write every q<N>-<key>.html preview of r01_collect_job_report_views (b35.j02.t03-s14, Job x Report).

Each preview starts from the real j02_studio_pages page served on 5623 (its head, rails, scripts and look) and
changes only the view-button-list and the content card. Tasks, Runs, sNN and states are read from disk; the Studio
rows are the live rows. Rerun it to refresh the previews; never edit a q*.html by hand.

    python3 build_previews.py
"""
import html
import re
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
JOB = HERE.parents[2]                                   # j02_studio_pages
SPACE = JOB.parents[4]                                  # Tools-SPACE
HOST = "http://100.121.165.84:5623"
REL = JOB.relative_to(SPACE).as_posix()
BLOCK_REL = JOB.parent.relative_to(SPACE).as_posix()
MARK = {"done": "✅", "running": "⏳", "waiting": "🙋", "planned": "⬜"}


def get(params: dict, route="/_board/workbench") -> str:
    with urllib.request.urlopen(HOST + route + "?" + urllib.parse.urlencode(params), timeout=30) as r:
        return r.read().decode("utf-8")


def wb(path, **kw):
    return "/_board/workbench?" + urllib.parse.urlencode({"layout": "focus", "path": path, **kw})


REPORT = get({"layout": "focus", "path": REL, "section": "report"})
STATUS = get({"layout": "focus", "path": REL, "section": "report", "group": "standing"})
STUDIO = {g: get({"layout": "focus", "path": REL, "section": "studio", "group": g}) for g in ("Block UI", "Job UI", "Task UI")}
BSTUDIO = get({"layout": "focus", "path": BLOCK_REL, "section": "studio", "group": "Studio"})
T01WORK = get({"layout": "focus", "path": REL + "/t01_build_studio_pages", "section": "work"})


# ---------------------------------------------------------------- disk facts
def tasks():
    face = (JOB / f"{JOB.name}.md").read_text()
    out = []
    for m in re.finditer(r"^\d+\. (t\d\d_\S+) · (.+)$", face, re.M):
        t = JOB / m.group(1)
        runs = []
        for r in sorted((t / "runs").iterdir()) if (t / "runs").is_dir() else []:
            card = r / "run.yaml"
            if card.is_file():
                st = re.search(r"^status:\s*(\S+)", card.read_text(), re.M)
                runs.append((r.name, st.group(1) if st else "planned"))
        snn = []
        for s in sorted(t.glob("s[0-9][0-9]-*")):
            f = s / f"{s.name}.md"
            title = f.read_text().splitlines()[0].strip() if f.is_file() else s.name
            snn.append((s.name, title))
        out.append((m.group(1), m.group(2), runs, snn))
    return out


TASKS = tasks()


def task_mark(runs):
    states = {s for _, s in runs}
    if runs and states == {"done"}:
        return "✅"
    if "waiting" in states:
        return "🙋"
    if "running" in states:
        return "⏳"
    return "⬜"


# ---------------------------------------------------------------- page pieces
def between(h, start, end, frm=0):
    i = h.index(start, frm)
    j = h.index(end, i + len(start))
    return i, j


i = REPORT.index('<style>.focus-map')
j = REPORT.index("<div class=pm>", i)
MAP_HEAD = REPORT[i:j]                                  # map styles, .focus-map and .pm-edit opening
k = REPORT.index("<script", j)
end = REPORT.index("</div></div></section>", k) + len("</div>")
MAP_TAIL = REPORT[k:end]                                # map scripts, .focus-map closing


def leaf(num, pill, text, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<li{c}><span class=pm-s>{num}</span><span class=pm-role>{html.escape(pill)}</span>'
            f'<span class=pm-w><span class=pm-t>{html.escape(text)}</span>'
            f'<button type=button class=pm-more aria-expanded=false data-empty=1>▸</button></span>'
            f'<div class=pm-detail></div></li>')


def para(pid, title, leaves, cls=""):
    c = f" {cls}" if cls else ""
    return (f'<div class="pm-para{c}"><div class="pm-node pm-pnode"><span class=pm-id>{html.escape(pid)}</span>'
            f'<b>{html.escape(title)}</b></div><ul class=pm-leaves>{"".join(leaves)}</ul></div>')


def mindmap(kind="runs+snn", open_detail=None):
    """kind: runs (today), runs+snn, snn, tasks (one mark each)."""
    paras = []
    for n, (tid, title, runs, snn) in enumerate(TASKS, 1):
        lv, x = [], 0
        if kind in ("runs", "runs+snn"):
            for name, st in runs:
                x += 1
                lv.append(leaf(f"{n}.{x}", st, name))
                if open_detail == name:
                    lv[-1] = lv[-1].replace("aria-expanded=false data-empty=1>▸</button></span><div class=pm-detail></div>",
                                            'aria-expanded=true>▸</button></span><div class="pm-detail diff">'
                                            '<textarea placeholder="a detail for this point"></textarea></div>')
        if kind in ("runs+snn", "snn"):
            for name, ftitle in snn:
                x += 1
                lv.append(leaf(f"{n}.{x}", "studio", name, "diff" if kind == "runs+snn" else ""))
        ttl = f"{task_mark(runs)} {title}" if kind == "tasks" else title
        paras.append(para(tid, ttl, lv, "diff" if kind == "tasks" else ""))
    return (MAP_HEAD + '<div class=pm><svg class=pm-wires aria-hidden=true></svg><div class="pm-node pm-root">'
            f'<b>{JOB.name}</b></div><div>{"".join(paras)}</div></div></div>' + MAP_TAIL)


ROWS = {}
for page in STUDIO.values():
    for art, sid in re.findall(r'(<article class="status-row studio-row" id="(s\d\d-[^"]+)">.*?</article>)', page, re.S):
        ROWS[sid] = art
S02 = re.search(r'<article class="status-row studio-row" id="s02-studio-pages">.*?</article>', BSTUDIO, re.S).group(0)


def ui_row(art, word="planned"):
    """A Studio row as a delivery row: its one word, its current version (s51-D05); none is made yet."""
    return art.replace('<span class="row-type" title="delivery type">ui</span>',
                       '<span class="row-type" title="delivery type">ui</span>'
                       f'<span class="row-stage" title="its current version">{word}</span>', 1)


def compact(art):
    """A row without its picture, so more rows fit."""
    return re.sub(r'<a class="row-thumb".*?</a>', "", art, flags=re.S)


def status_body():
    i = STATUS.index('<p class="view-caption">')
    j = STATUS.index("</div></section>", i)
    return STATUS[i:j]


def nav(labels, current=0, diff=False):
    links = "".join(f'<a href="#"{" aria-current=page" if n == current else ""}>{html.escape(l)}</a>'
                    for n, l in enumerate(labels))
    return f'<nav class="section-views{" diff" if diff else ""}" aria-label="Views">{links}</nav>'


def page(base, title, labels, current, body, section="Report", extra_css="", dialog=None, bar_diff=False):
    h = base
    h = re.sub(r'<title>.*?</title>', f"<title>{html.escape(title)}</title>", h, count=1)
    h = re.sub(r'<nav class="section-views[^"]*" aria-label="Views">.*?</nav>', nav(labels, current, bar_diff).replace("\\", "\\\\"), h, count=1, flags=re.S)
    h = re.sub(r'<span class="h1-section"[^>]*>[^<]*</span>', f'<span class="h1-section">{section}</span>', h, count=1)
    i = h.index('<section class="focus-card">')
    j = h.index("</section><footer", i) + len("</section>")
    h = h[:i] + f'<section class="focus-card"><div class="focus-content">{body}</div></section>' + h[j:]
    css = ('<style>.diff{outline:2px solid #f08c00;outline-offset:3px;border-radius:6px}'
           '.panel{flex:1;min-width:0;border:1px solid var(--line);border-radius:10px;padding:8px 10px;overflow:hidden}'
           '.panel>.panel-name{font-size:12px;font-weight:700;color:var(--muted);margin:0 0 6px}'
           '.panel>.zoom{zoom:.62}.panel .pm-wires{display:none}.panels{display:flex;gap:12px;align-items:flex-start}'
           '.task-line{border:1px solid var(--line);border-radius:10px;padding:10px 14px;margin:0 0 8px}'
           '.task-line b{margin-right:8px}.task-line .row-verbs{flex-wrap:wrap}'
           '.pop-frame{width:100%;height:380px;border:1px solid var(--line);border-radius:8px;background:var(--paper)}'
           + extra_css + '</style></head>')
    h = h.replace("</head>", css, 1)
    if dialog:
        ttl, src = dialog
        h = h.replace('<dialog id="focus-viewer">', '<dialog id="focus-viewer" open class="diff" style="position:fixed;'
                      'inset:0;margin:auto;width:78vw;height:76vh;z-index:9">', 1)
        h = h.replace("<span data-viewer-title></span>", f"<span data-viewer-title>{html.escape(ttl)}</span>", 1)
        h = h.replace('<iframe title="Content preview"></iframe>', f'<iframe title="Content preview" src="{html.escape(src)}"></iframe>', 1)
    return h


def caption(t):
    return f'<p class="view-caption">{html.escape(t)}</p>'


def panel(name, inner, cls=""):
    return f'<div class="panel {cls}"><p class="panel-name">{name}</p><div class="zoom">{inner}</div></div>'


def write(name, h):
    (HERE / name).write_text(h)
    print("wrote", name)


# ---------------------------------------------------------------- the views' bodies
def ui_view(kind="target+tasks"):
    out = [caption("What it hands over, its sNN of type ui, each with its one word.")]
    if kind == "target+tasks":
        out.append('<h3 class="focus-sub diff">What this Job makes</h3>' + ui_row(S02))
        for tid, title, runs, snn in TASKS:
            if snn:
                out.append(f'<h3 class="focus-sub">{tid} · {html.escape(title)}</h3>')
                out += [ui_row(ROWS[s]) for s, _ in snn if s in ROWS]
    elif kind == "flat":
        for tid, title, runs, snn in TASKS:
            out += [ui_row(ROWS[s]) for s, _ in snn if s in ROWS]
    elif kind == "task-lines":
        for tid, title, runs, snn in TASKS:
            if not snn:
                continue
            tags = "".join(f'<a class="row-verb" href="{wb(REL, section="studio", group=ft.split(": ")[0].split(" · ")[-1])}#{s}">'
                           f'{s.split("-")[0]} {html.escape(ft.split(": ")[-1])} · planned</a>' for s, ft in snn)
            out.append(f'<div class="task-line diff"><b>{tid}</b>{html.escape(title)}<p class="row-verbs">{tags}</p></div>')
    return "".join(out)


def first_ui_rows(n=2):
    rows = [ui_row(compact(S02))] + [ui_row(compact(ROWS[s])) for _, _, _, snn in TASKS for s, _ in snn if s in ROWS]
    return "".join(rows[:n])


MAPCAP = caption("How it is built, as a map: its parts, and what each must find out.")

# Q1 · the view list: each option shows its views as panels, side by side
write("q1-a.html", page(REPORT, "Q1 A", ["MindMap", "Status"], 0,
      '<div class="panels">' + panel("MindMap", mindmap("runs")) + panel("Status", status_body(), "diff") + "</div>", bar_diff=True))
write("q1-b.html", page(REPORT, "Q1 B", ["MindMap", "UI"], 0,
      '<div class="panels">' + panel("MindMap", mindmap("runs+snn")) + panel("UI", first_ui_rows(3), "diff") + "</div>", bar_diff=True))
write("q1-c.html", page(REPORT, "Q1 C", ["MindMap", "s02-studio-pages"], 0,
      '<div class="panels">' + panel("MindMap", mindmap("runs"))
      + panel("s02-studio-pages: what this Job makes",
              f'<iframe class="pop-frame" src="/_board/workbench?view=focus-delivery&amp;path={BLOCK_REL}/s02-studio-pages"></iframe>',
              "diff") + "</div>", bar_diff=True))
write("q1-d.html", page(REPORT, "Q1 D", ["MindMap"], 0,
      '<div class="panels">' + panel("MindMap, the only view", mindmap("runs+snn"), "diff") + "</div>", bar_diff=True))

# Q2 · the MindMap
write("q2-a.html", page(REPORT, "Q2 A", ["MindMap", "UI"], 0, MAPCAP + mindmap("runs+snn")))
write("q2-b.html", page(REPORT, "Q2 B", ["MindMap", "UI"], 0, MAPCAP + mindmap("runs")))
write("q2-c.html", page(REPORT, "Q2 C", ["MindMap", "UI"], 0, MAPCAP + mindmap("snn")))
write("q2-d.html", page(REPORT, "Q2 D", ["MindMap", "UI"], 0, MAPCAP + mindmap("tasks")))

# Q3 · the UI view
write("q3-a.html", page(REPORT, "Q3 A", ["MindMap", "UI"], 1, ui_view("target+tasks")))
write("q3-b.html", page(REPORT, "Q3 B", ["MindMap", "UI"], 1, ui_view("flat")))
write("q3-c.html", page(REPORT, "Q3 C", ["MindMap", "UI"], 1, ui_view("task-lines")))

# Q4 · a click on an sNN's name in the UI view
studio_job = STUDIO["Job UI"]
write("q4-a.html", page(studio_job, "Q4 A", ["Block UI", "Job UI", "Task UI"], 1,
      re.search(r'<div class="focus-content">(.*?)</div></section>', studio_job, re.S).group(1),
      section="Studio", extra_css="#s14-job-ui-report{outline:2px solid #f08c00;outline-offset:4px;border-radius:8px;background:var(--soft)}"))
s14 = f"{REL}/t03_job_page/s14-job-ui-report"
write("q4-b.html", page(REPORT, "Q4 B", ["MindMap", "UI"], 1, ui_view("target+tasks"),
      dialog=("s14-job-ui-report", f"/_board/page?path=/{s14}/s14-job-ui-report.md")))
write("q4-c.html", page(REPORT, "Q4 C", ["MindMap", "UI"], 1, ui_view("target+tasks"),
      dialog=("s14-job-ui-report · delivery", f"/_board/workbench?view=focus-delivery&path={s14}")))

# Q5 · a click on a Run in the MindMap
run = "run-build-card-picture"
write("q5-a.html", page(REPORT, "Q5 A", ["MindMap", "UI"], 0, MAPCAP + mindmap("runs+snn"),
      dialog=(run, f"/_board/page?path=/{REL}/t01_build_studio_pages/runs/{run}/{run}.md")))
t01 = T01WORK.replace(f'<span class="row-name">{run}</span>', f'<span class="row-name">{run}</span>', 1)
t01_body = re.search(r'<div class="focus-content">(.*?)</div></section>', t01, re.S).group(1)
t01_body = re.sub(r'(<article class="status-row")(>(?:(?!</article>).)*?' + re.escape(run) + ')',
                  r'\1 style="outline:2px solid #f08c00;outline-offset:4px;border-radius:8px;background:var(--soft)"\2',
                  t01_body, count=1, flags=re.S)
write("q5-b.html", page(T01WORK, "Q5 B", ["Progress"], 0, t01_body, section="Work"))
write("q5-c.html", page(REPORT, "Q5 C", ["MindMap", "UI"], 0, MAPCAP + mindmap("runs+snn", open_detail=run)))
