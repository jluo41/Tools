"""A Block's 💼 Jobs section, the place to work (JL 261125: "so the Job will be place to work, and in the Report, we also
have Jobs, but that is for reporting"): one view button per own jNN, in number order, and the picked Job's Main (its
bands and folds) right on the Block page. Every Job is built once and switched in place, as the Report's views are
(view_bands.panes), so a switch never reloads the page. The Report keeps its Jobs fold to report how they stand."""
from __future__ import annotations

import re
from pathlib import Path

from live import frame
from live.focus_base import page_url
from live import scroll_rows

JOB = re.compile(r"^j\d\d[_-]")
# an insight Board (b11 s07, 261126): a Job is one question version on one data version, grouped by its `release:`;
# a Task is one question at one DIKW level, grouped by the level letter in its folder name (t03_I01_outcome-by-arm)
LEVEL = re.compile(r"^t\d\d_([DIKWX])\d\d_")
LEVELS = {"D": "🗂 Data", "I": "📈 Information", "K": "🧠 Knowledge", "W": "🧭 Wisdom", "X": "🎯 Executive"}
SWITCH = """<script>(function(){if(window.__jobsOn)return;window.__jobsOn=1;var mem={};
function cur(row,a){row.querySelectorAll('a').forEach(function(x){if(x===a)x.setAttribute('aria-current','page');else x.removeAttribute('aria-current');});}
function fit(r){if(r&&window.jrowFit)window.jrowFit(r);}
var jtype='';function show(row,d){row.querySelectorAll('a[data-topic]').forEach(function(x){x.hidden=x.dataset.topic!==d||(row.classList.contains('job-bar')&&jtype!==''&&x.dataset.jtype!==jtype);});}
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[data-type-to],a[data-topic-to],a[data-job-to],a[data-ttopic-to],a[data-jsub-to]');
 if(!a||e.metaKey||e.ctrlKey||e.shiftKey||e.button)return;e.preventDefault();var d=a.dataset,pane=a.closest('[data-job-pane]');
 if(d.typeTo!==undefined){jtype=d.typeTo;cur(a.parentNode,a);var tops=document.querySelector('.job-topics'),first=null;
  tops.querySelectorAll('a[data-topic-to]').forEach(function(g){g.hidden=jtype!==''&&(' '+g.dataset.types+' ').indexOf(' '+jtype+' ')<0;if(!g.hidden&&!first)first=g;});
  var on=tops.querySelector('a[aria-current]');(on&&!on.hidden?on:first).click();return;}
 if(d.topicTo!==undefined){var bar=document.querySelector('.job-bar');cur(a.parentNode,a);show(bar,d.topicTo);fit(a.parentNode);
  var p=bar.querySelector('a[data-job-to="'+(mem['j'+d.topicTo]||'')+'"]:not([hidden])')||bar.querySelector('a[data-topic="'+d.topicTo+'"]:not([hidden])');if(p)p.click();fit(bar);return;}
 if(d.jobTo!==undefined){var k=d.jobTo;mem['j'+d.topic]=k;
  document.querySelectorAll('[data-job-pane]').forEach(function(p){p.hidden=p.dataset.jobPane!==k;});cur(a.parentNode,a);fit(a.parentNode);
  history.replaceState(null,'',a.href);var on=document.querySelector('[data-job-pane="'+k+'"]');if(on)on.querySelectorAll('.jrow').forEach(fit);return;}
 if(!pane)return;var t3=pane.querySelector('.job-ttopics'),t4=pane.querySelector('.job-subs'),job=pane.dataset.jobPane;
 if(d.ttopicTo!==undefined){cur(t3,a);t4.hidden=false;show(t4,d.ttopicTo);
  var q=t4.querySelector('a[data-jsub-to="'+(mem[job+d.ttopicTo]||'')+'"]')||t4.querySelector('a[data-topic="'+d.ttopicTo+'"]');if(q)q.click();return;}
 var s=d.jsubTo;pane.querySelectorAll('[data-jsub]').forEach(function(p){if(p.closest('[data-job-pane]')===pane)p.hidden=p.dataset.jsub!==s;});
 if(s==='main'){cur(t3,t3.querySelector('a[data-jsub-to="main"]'));t4.hidden=true;return;}
 mem[job+d.topic]=s;cur(t3,t3.querySelector('a[data-ttopic-to="'+d.topic+'"]'));t4.hidden=false;show(t4,d.topic);cur(t4,t4.querySelector('[data-jsub-to="'+s+'"]'));fit(t3);fit(t4);});
window.addEventListener('load',function(){var task=new URLSearchParams(location.search).get('task');
 if(!/^t[0-9]{2}$/.test(task||''))return;var pane=document.querySelector('[data-job-pane]:not([hidden])');
 var a=pane&&pane.querySelector('.job-subs [data-jsub-to="'+task+'"]');if(a)a.click();});
})();</script>
<style>.jobs-rows{margin:0 0 4px}.row-topics{margin:-4px 0 6px!important;gap:16px!important}
.row-topics a{border:0!important;background:none!important;border-radius:0!important;padding:2px 0 3px!important;font-size:13px;font-weight:600;color:var(--muted)!important;border-bottom:2px solid transparent!important}
.row-topics a:hover{color:var(--ink)!important}.row-topics a[aria-current]{color:var(--ink)!important;border-bottom-color:var(--accent)!important}
.row-topics a.old,.job-bar a.old{opacity:.55}.row-topics a.old:hover,.row-topics a.old[aria-current],.job-bar a.old:hover,.job-bar a.old[aria-current]{opacity:1}.topic-code{color:var(--muted);font-size:12px;font-weight:400}
.job-types{margin:0 0 2px!important}.job-bar{margin-bottom:6px!important}.job-ttopics{margin-top:-14px!important}.job-subs{margin:0 0 12px!important}.job-subs .jmark{margin-left:4px;color:var(--pb-you,#b35c00);font-size:12px}</style>"""


def own_jobs(folder: Path) -> list:
    """The Block's own Job folders (jNN_…), in number order."""
    try:
        return sorted((p for p in folder.iterdir() if p.is_dir() and JOB.match(p.name)), key=lambda p: p.name)
    except OSError:
        return []


def label(job: Path, root: Path | None = None) -> str:
    """j01_work_ladder_contract reads "j01 · Work ladder contract"; an insight Job reads by its data version
    ("j02 · data-v2", "j03 · data-v2 · prep-v1" when it pins a prep version), its question version being its topic."""
    if root is not None and job_topic(job, root) != job.name[1]:
        data = face_line(job, "data")
        if data:
            prep = face_line(job, "prep")
            return f"{job.name[:3]} · {data}" + (f" · {prep}" if prep else "")
    key, _, rest = job.name.replace("-", "_").partition("_")
    rest = rest.replace("_", " ").strip()
    return f"{key} · {rest[:1].upper()}{rest[1:]}" if rest else key


def face_line(job: Path, key: str) -> str:
    """One `key: value` line from the head of a Job's face (read_face keeps only the shared keys)."""
    try:
        head = (job / f"{job.name}.md").read_text(encoding="utf-8", errors="ignore")[:3000]
    except OSError:
        return ""
    m = re.search(rf"(?m)^{key}:\s*(.+)$", head)
    return m.group(1).strip().strip("'\"") if m else ""


def job_topic(job: Path, root: Path) -> str:
    """A Job's topic: its face's `release:` (an insight Board's question version), else its decade digit."""
    return face_line(job, "release") or job.name[1]


def task_topic(name: str) -> str:
    """A Task's topic: its DIKW level letter (an insight question), else its decade digit."""
    m = LEVEL.match(name)
    return m.group(1) if m else name[1]


def goal(job: Path, root: Path) -> str:
    """A Job's goal, the hover of its button (never a line on the page)."""
    from live.focus_base import read_face
    return str(read_face(job, root).get("goal") or job.name)


def page_ctx(theme, root: Path, folder: Path):
    """A Job's or a Task's Report, drawn by the same pipeline as its own page, without its shell."""
    from live.focus_render import page_route, report_view_map, rail_sections, section_body, work_view_map
    ctx = page_route(theme, root, folder, "report", "")
    report_view_map(ctx)
    work_view_map(ctx)
    rail_sections(ctx)
    section_body(ctx)
    return ctx


def task_mark(task: Path, root: Path) -> str:
    """A Task's marks after its name: ✅ or ⏳ when it has one (open shows nothing, never the face's own 🔴), then
    🙋 N when questions wait on the person."""
    from live.focus_base import read_face, state_kind
    from live.focus_interactions import interactions
    kind = state_kind(str(read_face(task, root).get("state") or ""))
    mark = kind.split(" ", 1)[0] if kind[:1] in "⏳✅" else ""
    waits = sum(r.get("state") == "waiting" for r in interactions(task, root))
    return " ".join(m for m in (mark, f"🙋 {waits}" if waits else "") if m)


def design_adapter(theme, folder: Path):
    """Optional Design content; other themes keep the shared fallback unchanged."""
    if theme.name == "design":
        from live import design_jobs
        if design_jobs.applies(folder):
            return design_jobs
    return None


def job_pane(theme, root: Path, job: Path) -> str:
    """One Job (s07, JL 261125: "should we call it the main?"; "how about we get the tasks to be the view as well"):
    its own view buttons, Main (the Job's Report bands) and then one per Task; a Task's view is its page, its bands and
    folds, with its open dot."""
    from live.ui_parts import open_dot
    adapter = design_adapter(theme, job.parent)
    main = adapter.main(job, root) if adapter else page_ctx(theme, root, job).body
    subs = [("main", "Main", "", main)]
    topics = {}
    for t in sorted(p for p in job.iterdir() if p.is_dir() and re.match(r"^t\d\d[_-]", p.name)):
        try:
            inner = adapter.task_body(t, root) if adapter else page_ctx(theme, root, t).body
        except Exception as exc:                          # one broken Task never blanks the others
            inner = f'<p class="mut">{frame.esc(t.name)} could not be drawn: {frame.esc(type(exc).__name__)}</p>'
        subs.append((t.name[:3], label(t), task_mark(t, root), open_dot(inner, page_url(t, root), t.name)))
        topics[t.name[:3]] = adapter.task_topic(t) if adapter else task_topic(t.name)
    if len(subs) == 1:
        return f'<div data-jsub="main">{main}</div>' if adapter else main
    names = adapter.TASK_TOPICS if adapter else band_names(job / f"{job.name}.md")
    decades = list(dict.fromkeys(topics[k] for k, _, _, _ in subs[1:]))
    if adapter:
        decades.sort(key=list(adapter.TASK_TOPICS).index)
    if all(d in LEVELS for d in decades):        # DIKW levels read in ladder order
        decades.sort(key=list(LEVELS).index)
    row3 = ('<nav class="section-views jrow row-topics job-ttopics" aria-label="Task topics">'
            '<a href="#" data-jsub-to="main" aria-current="page">Main</a>'
            + "".join(f'<a href="#" data-ttopic-to="{d}">' + (frame.esc(names[d]) if adapter else topic_label(LEVELS[d], "", d, d) if d in LEVELS else topic_label(names.get(d, "Tasks"), "t", d))
                      + "</a>" for d in decades) + "</nav>")
    row4 = ('<nav class="section-views jrow job-subs" aria-label="Tasks" hidden>'
            + "".join(f'<a href="#" data-jsub-to="{k}" data-topic="{topics[k]}">{frame.esc(n)}'
                      + (f' <span class="jmark">{frame.esc(m)}</span>' if m else "") + "</a>" for k, n, m, _ in subs[1:]) + "</nav>")
    return row3 + row4 + "".join(f'<div data-jsub="{k}"{"" if i == 0 else " hidden"}>{h}</div>' for i, (k, _, _, h) in enumerate(subs))


def band_names(face: Path, letters: str = "jt") -> dict:
    """{decade: name} from a face's `bands:` line (`bands: j0N Earlier design · j1N Workbench`); `letters` picks
    the kind: Jobs and Tasks (j, t) by default, Studio topics with "s"."""
    try:
        line = re.search(r"(?mi)^bands:\s*(.+)$", face.read_text(encoding="utf-8", errors="ignore"))
    except OSError:
        return {}
    return {m.group(1): m.group(2).strip() for m in re.finditer(rf"\b[{letters}](\d)N\s+([^·,;]+)", line.group(1))} if line else {}


def topic_label(name: str, letter: str, decade: str, code: str = "") -> str:
    """A topic word: its name, then its code small and grey ("Workbench · j1N", "📈 Information · I"); a decade with
    no name reads "j1N"."""
    code = code or f"{letter}{decade}N"
    return f'{frame.esc(name)} <span class="topic-code">· {code}</span>' if name else code


def closed(job: Path, root: Path) -> bool:
    """A Job its face calls closed, done or superseded."""
    from live.focus_base import read_face
    state = str(read_face(job, root).get("state") or "") or face_line(job, "state")   # an insight face: `state:` in its --- head
    return bool(re.search(r"(?i)closed|superseded|\bdone\b|✅", state))


def ordered(jobs: list, root: Path) -> list:
    """[(job, faded, divider_before)] as the buttons read (s07 drawing, JL 261125): the newest decade first (j1N before
    j0N), a line between decades; an earlier decade or a closed Job reads faded, and closed ones go last."""
    top = max(job_topic(j, root) for j in jobs)
    rows = sorted(sorted(jobs, key=lambda j: j.name, reverse=job_topic(jobs[0], root) != jobs[0].name[1]),
                  key=lambda j: job_topic(j, root), reverse=True)        # newest topic first; insight: newest Job first
    rows = sorted(rows, key=lambda j: closed(j, root))
    out, last = [], None
    for j in rows:
        group = "closed" if closed(j, root) else job_topic(j, root)
        out.append((j, closed(j, root) or job_topic(j, root) < top, last is not None and group != last))
        last = group
    return out


def job_type(job: Path) -> str:
    """A Job's type, its face's `job-type:` (code, doc, check, ...); its group is the Block's `bands:` (b17 trace 261127/1310)."""
    return face_line(job, "job-type")


def type_row(rows: list) -> str:
    """The Job type row above the group row: All, then each type its Jobs name; nothing when no Job names one."""
    types = list(dict.fromkeys(t for t in (job_type(j) for j, _, _ in rows) if t))
    if not types:
        return ""
    return ('<nav class="section-views jrow row-topics job-types" aria-label="Job types">'
            '<a href="#" data-type-to="" aria-current="page">All</a>'
            + "".join(f'<a href="#" data-type-to="{frame.esc(t)}">{frame.esc(t)}</a>' for t in types) + "</nav>")


def _types_attr(types: set) -> str:
    """A group button's ` data-types="check code"`: the Job types inside it, for the type row's filter; none, nothing."""
    types = sorted(types - {""})
    return f' data-types="{frame.esc(" ".join(types))}"' if types else ""


def section(theme, root: Path, folder: Path, group: str = "") -> tuple:
    """(bar, body) of the Jobs section: a button per Job, one line each, then every Job's body, the picked one shown."""
    jobs = own_jobs(folder)
    if not jobs:
        return "", ""
    adapter = design_adapter(theme, folder)
    rows = [(j, closed(j, root), False) for j in sorted(jobs, key=lambda j: (closed(j, root), j.name))] if adapter else ordered(jobs, root)
    key = lambda j: j.name.split("_", 1)[0].split("-", 1)[0]
    keys = [key(j) for j, _, _ in rows]
    shown = group if group in keys else keys[0]
    topic = {key(j): adapter.topic(j)[0] if adapter else job_topic(j, root) for j, _, _ in rows}
    names, decades = band_names(folder / "board.md"), sorted(set(topic.values()), reverse=True)
    if adapter:
        names = dict(adapter.topic(j) for j in jobs)
        decades = list(dict.fromkeys(topic.values()))
    row1 = ('<nav class="section-views jrow row-topics job-topics" aria-label="Job topics">'
            + "".join(f'<a href="#" data-topic-to="{frame.esc(d)}"'
                      + _types_attr({job_type(j) for j, _, _ in rows if topic[key(j)] == d})
                      + (' class="old"' if not adapter and d < decades[0] else "")
                      + (' aria-current="page"' if d == topic[shown] else "") + f'>{frame.esc(names[d]) if adapter else topic_label(names.get(d, ""), "j", d) if d.isdigit() else frame.esc(d)}</a>'
                      for d in decades) + "</nav>")
    row2 = ('<nav class="section-views jrow job-bar" aria-label="Jobs">'
            + "".join(f'<a href="{frame.esc(page_url(folder, root, "jobs", key(j)))}" data-job-to="{key(j)}" data-topic="{frame.esc(topic[key(j)])}"'
                      f' title="{frame.esc(goal(j, root))}"' + (f' data-jtype="{frame.esc(job_type(j))}"' if job_type(j) else "")
                      + (' class="old"' if closed(j, root) else "")
                      + (' aria-current="page"' if key(j) == shown else "")
                      + (" hidden" if topic[key(j)] != topic[shown] else "") + f'>{frame.esc(adapter.label(j) if adapter else label(j, root))}</a>' for j, _, _ in rows) + "</nav>")
    row0 = "" if adapter else type_row(rows)
    bar = f'<div class="jobs-rows">{row0}{row1}{row2}</div>'
    panes = []
    for j, _, _ in rows:
        try:
            body = job_pane(theme, root, j)
        except Exception as exc:                          # one broken Job never blanks the others
            body = f'<p class="mut">{frame.esc(j.name)} could not be drawn: {frame.esc(type(exc).__name__)}</p>'
        panes.append(f'<div class="job-pane" data-job-pane="{key(j)}"{"" if key(j) == shown else " hidden"}>{body}</div>')
    return bar, "".join(panes) + scroll_rows.CSS + scroll_rows.JS + SWITCH
