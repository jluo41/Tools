"""Write every q<N>-<key>.html preview of r01_collect_task_report_views (s17 · Task UI: Report).

Each preview starts from the live Task page's own CSS (curl of 5623, Report of t02_block_page) and changes only the
view-button-list and the content area. Rerun it; never edit the previews by hand.
"""
import re
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = ("http://100.121.165.84:5623/_board/workbench?layout=focus"
        "&path=blueprints/Project-PageParts/work/b35_studio/j02_studio_pages/")
LIVE = urllib.request.urlopen(BASE + "t02_block_page&section=report", timeout=20).read().decode()
STYLES = "".join(re.findall(r"<style.*?</style>", LIVE, flags=re.S))
WIRES = next(m for m in re.findall(r"<script>.*?</script>", LIVE, flags=re.S) if "pm-wires" in m)

EXTRA = """<style>
.focus-page{padding-top:14px}h1{margin:6px 0 10px}
.pv-panels{display:flex;gap:12px;align-items:flex-start}
.pv-panel{flex:1;min-width:0;border:1px solid var(--line);border-radius:8px;padding:8px 10px;overflow:hidden}
.pv-panel>h4{margin:0 0 6px;font-size:12px;font-weight:600;color:var(--accent)}
.pm{grid-template-columns:170px auto;gap:0 26px}.pm-root b{font-size:15px}.pm-para{grid-template-columns:180px auto;gap:0 24px}.pm-leaves li .pm-s{display:none}\n.pv-panel{overflow:auto}.pv-panel .pm{grid-template-columns:90px auto;gap:0 18px;padding:2px}.pv-panel .pm-para{grid-template-columns:96px auto;gap:0 16px}.pv-panel .pm-root{padding:6px 8px}.pv-panel .pm-root b{font-size:11px;margin:0}.pv-panel .pm-pnode{padding:4px 6px;font-size:11px}.pv-panel .pm-leaves li{font-size:11px;padding:1px 0}.pv-panel .pm-role{min-width:0;font-size:10px;margin-right:4px}.pv-panel .pm-s{display:none}.pv-panel .glance-list li{font-size:12.5px;padding:3px 0}
.pv-panel .focus-sub{margin:8px 0 2px;font-size:11px}.pv-panel .view-caption{font-size:12px;margin:0 0 6px}
.pv-from{font-size:11px;color:var(--muted);margin:0 0 4px}
.res{border-bottom:1px solid var(--line);padding:7px 0}.res b{font-weight:600}
.res .ask{display:block;font-size:12.5px;color:var(--muted);font-style:italic}
.res .files{display:block;font-size:12px;color:var(--muted)}.res .files code{font-size:11.5px}
.pv-panel .res{padding:4px 0;font-size:12.5px}
.empty-line{color:var(--muted);font-size:14px}
.pm-detail.open{display:block}
.pv-pop{position:relative;border:1px solid var(--line);border-radius:10px;box-shadow:0 10px 30px #0003;
 background:var(--paper);padding:6px 10px 10px;margin:-150px 10px 0 60px}
.pv-pop header{display:flex;justify-content:space-between;font-size:13px;margin-bottom:6px}
.pv-dim{opacity:.35}
.studio-row.pv-target{outline:2px solid var(--accent);outline-offset:4px;background:var(--soft)}
.row-stage,.row-type{margin-left:8px;font-size:12px;color:var(--muted)}.row-verbs{font-size:12px;color:var(--muted)}
.row-verbs .row-verb{margin-right:12px}.studio-row p{margin:4px 0}
</style>"""

T02 = dict(name="t02_block_page", folder="t02_block_page",
           aim="say how the Studio part shows in a Block page's Report, Work and Studio, so every Theme builds "
               "it the same way")
T01 = dict(name="t01_build_studio_pages", folder="t01_build_studio_pages",
           aim="build the Studio's UI as s02's agreed screen drafts show it: the Studio inside a page, and an sNN's "
               "link landing on its card (s02-D05)")

SNN = [("s11", "Block UI: Report", "block_ui_report", "how the Studio part shows in a Block page's Report."),
       ("s12", "Block UI: Work", "block_ui_work", "how the Studio part shows in a Block page's Work."),
       ("s13", "Block UI: Studio", "block_ui_studio", "how the Studio part shows in a Block page's Studio.")]
RUNS_T02 = [("r01_collect_block_report_views", "s11"), ("r02_collect_block_work_views", "s12"),
            ("r03_collect_block_studio_views", "s13")]
RUNS_T01 = [  # newest first; all done 261030 (their run.yaml and pass p01-1030)
    ("run-build-studio-in-a-page", "JL 261030: \"we just have sNN, along side with jNN, to make it visible directly\"",
     "Status view and sNN beside the Jobs", ["servers/workbench/focus_page.py", "servers/workbench/frame.py"]),
    ("run-build-snn-page", "JL 261029: \"so I think studio should have a page as well\"",
     "an sNN beside the Jobs opens its own page", ["servers/workbench/focus_page.py"]),
    ("run-build-popout-size", "JL 261030: \"could you make the margin here to be smaller?\"",
     "the pop-out fills 96% x 94%", ["servers/workbench/focus-assets/focus.css"]),
    ("run-build-card-picture", "JL 261030: \"go ahead and work on that\"",
     "the card shows the drawing's start", ["s01-studio-skill/build_s01_studio_skill.py"]),
]


def page(task, views, on, content, title, diff_bar=False):
    crumb = "Tools-SPACE / blueprints / Project-PageParts / work / b35_studio / j02_studio_pages / " + task["name"]
    bar = "".join(f'<a href="#"{" aria-current=page" if v == on else ""}>{v}</a>' for v in views)
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" '
            f'content="width=device-width,initial-scale=1"><title>{title}</title>{STYLES}{EXTRA}</head><body>'
            f'<main class="focus-page"><div class="focus-crumb">{crumb}</div>'
            f'<h1>{task["name"]}<span class="h1-section">Report</span></h1>'
            f'<nav class="section-views{" diff" if diff_bar else ""}" aria-label="Views">{bar}</nav>'
            f'<div class="focus-goal"><span class="goal-word">Aim</span><p>{task["aim"]}</p></div>'
            f'<section class="focus-card"><div class="focus-content">{content}</div></section></main>'
            f'{WIRES}</body></html>')


def leaf(words, role="", detail="", open_=False):
    r = f'<span class="pm-role">{role}</span>' if role else ""
    d = f'<div class="pm-detail{" open" if open_ else ""}">{detail}</div>' if detail else ""
    return f'<li><span class="pm-s"></span>{r}<span class="pm-w"><span class="pm-t">{words}</span></span>{d}</li>'


def para(name, kind, leaves, detail=""):
    d = f'<div class="pm-detail open diff">{detail}</div>' if detail else ""
    return (f'<div class="pm-para"><div class="pm-node pm-pnode"><span class="pm-id">{kind}</span><b>{name}</b>{d}'
            f'</div><ul class="pm-leaves">{"".join(leaves)}</ul></div>')


def mindmap(root, paras, caption=True):
    cap = '<p class="view-caption">How it is built, as a map: its parts, and what each must find out.</p>' if caption else ""
    return (f'{cap}<div class="focus-map"><div class="pm"><svg class="pm-wires" aria-hidden="true"></svg>'
            f'<div class="pm-node pm-root"><b>{root}</b></div><div>{"".join(paras)}</div></div></div>')


# the MindMap shapes (Q2), all on t02_block_page
def map_two_branches(states=True):
    s = [leaf(f"{n} · {t}", "explore" if states else "") for n, t, _, _ in SNN]
    r = [leaf(name, "⬜ planned" if states else "") for name, _ in RUNS_T02]
    return mindmap("t02_block_page", [para("Studio", "", s), para("Runs", "", r)])


def map_by_snn(open_s11=False):
    return mindmap("t02_block_page", [para(f"{n} · {t}", "explore · ui", [leaf(run, "⬜ planned")],
                                           detail=f"{line} Open: should a Job's sNN show here too?"
                                           if (open_s11 and n == "s11") else "")
                                      for (n, t, _, line), (run, _) in zip(SNN, RUNS_T02)])


def map_runs_only():
    return mindmap("t02_block_page", [para("Runs", "", [leaf(name, "⬜ planned") for name, _ in RUNS_T02])])


def status_html():
    s = "".join(f"<li>⬜ <b>{n}</b> {t} <span class=mut>· explore</span></li>" for n, t, _, _ in SNN)
    r = "".join(f"<li>⬜ <b>{name}</b> <span class=mut>· planned</span></li>" for name, _ in RUNS_T02)
    return (f'<p class="view-caption">Where its sNN and its Runs stand.</p><h3 class="focus-sub">Studio</h3>'
            f'<ul class="glance-list">{s}</ul><h3 class="focus-sub">Runs</h3><ul class="glance-list">{r}</ul>')


def results_html(style="ask", only_newest=False):
    rows = RUNS_T01[:1] if only_newest else RUNS_T01
    out = ['<p class="view-caption">What its done Runs found, newest first.</p>']
    for name, ask, summary, files in rows:
        files_html = '<span class="files">changed: ' + ", ".join(f"<code>{f}</code>" for f in files) + "</span>"
        if only_newest:
            out.append(f'<div class="res">✅ <b>{name}</b> <span class=mut>· done 261030 · pass p01-1030</span>'
                       f'<h3 class="focus-sub">Ask</h3><p>{ask}</p><h3 class="focus-sub">Summary</h3>'
                       f'<p>{summary}</p><h3 class="focus-sub">Changed</h3>{files_html}</div>')
        elif style == "ask":
            out.append(f'<div class="res">✅ <b>{name}</b><span class="ask">{ask}</span>{summary}</div>')
        else:
            out.append(f'<div class="res">✅ <b>{name}</b> · {summary}{files_html}</div>')
    return "".join(out)


def ui_view():
    rows = "".join(f'<div class="res"><b>{n} · {t}</b> <span class=mut>· ui · planned</span>'
                   f'<span class="files">deck · the rules → <code>{n}-…/delivery/ui/</code> · not made yet</span></div>'
                   for n, t, _, _ in SNN)
    return f'<p class="view-caption">What its sNN hand over, of type ui.</p>{rows}'


def panels(*items):
    return '<div class="pv-panels">' + "".join(
        f'<div class="pv-panel"><h4>{h}</h4>{body}</div>' for h, body in items) + "</div>"


T01_NOTE = '<p class="pv-from">shown on t01_build_studio_pages, the Task with done Runs</p>'

files = {}
# Q1 · the view list (each view as its own panel)
files["q1-a.html"] = page(T02, ["MindMap", "Status"], "MindMap",
                          panels(("MindMap", map_two_branches(states=False)), ("Status", status_html())), "Q1 A", diff_bar=True)
files["q1-b.html"] = page(T02, ["MindMap", "Results", "Status"], "MindMap",
                          panels(("MindMap", map_two_branches(states=False)),
                                 ("Results", T01_NOTE + results_html()), ("Status", status_html())), "Q1 B", diff_bar=True)
files["q1-c.html"] = page(T02, ["MindMap", "Results"], "MindMap",
                          panels(("MindMap (states on the leaves)", map_two_branches()),
                                 ("Results", T01_NOTE + results_html())), "Q1 C", diff_bar=True)
files["q1-d.html"] = page(T02, ["MindMap", "UI"], "MindMap",
                          panels(("MindMap (states on the leaves)", map_two_branches()), ("UI", ui_view())), "Q1 D", diff_bar=True)
# Q2 · the MindMap
files["q2-a.html"] = page(T02, ["MindMap", "Results"], "MindMap", map_two_branches(), "Q2 A")
files["q2-b.html"] = page(T02, ["MindMap", "Results"], "MindMap", map_by_snn(), "Q2 B")
files["q2-c.html"] = page(T02, ["MindMap", "Results"], "MindMap", map_runs_only(), "Q2 C")
# Q3 · Results, on t01
files["q3-a.html"] = page(T01, ["MindMap", "Results"], "Results", results_html("ask"), "Q3 A")
files["q3-b.html"] = page(T01, ["MindMap", "Results"], "Results", results_html("files"), "Q3 B")
files["q3-c.html"] = page(T01, ["MindMap", "Results"], "Results", results_html(only_newest=True), "Q3 C")
# Q4 · no Run done yet, on t02
files["q4-a.html"] = page(T02, ["MindMap"], "MindMap", map_by_snn(), "Q4 A")
files["q4-b.html"] = page(T02, ["MindMap", "Results"], "Results",
                          '<p class="view-caption">What its done Runs found, newest first.</p>'
                          '<p class="empty-line">No Run done yet. Its Runs are in <a href="#"><u>Work</u></a>.</p>',
                          "Q4 B")
files["q4-c.html"] = page(T02, ["MindMap", "Results"], "Results",
                          '<p class="view-caption">What its done Runs found, newest first.</p>' + "".join(
                              f'<div class="res">⬜ <b>{name}</b> <span class=mut>· planned · about {s}</span></div>'
                              for name, s in RUNS_T02), "Q4 C")


# Q5 · a click on s11 in the MindMap
def studio_card(n, t, slug, line, target=False):
    return (f'<article class="status-row studio-row{" pv-target" if target else ""}"><div><p class="row-title">'
            f'<span class="row-address">j02.t02-{n} · </span><b class="row-name">{slug}</b>'
            f'<span class="row-stage">explore</span><span class="row-type">ui</span></p>'
            f'<p class="row-line">{line}</p><p class="row-verbs"><span class="row-verb">Draw</span>'
            f'<span class="row-verb">Mind map</span><span class="row-verb">Work</span>'
            f'<span class="row-verb">Delivery</span><span class="row-verb">Interaction</span></p></div></article>')


studio_page = page(T02, ["Block UI"], "Block UI",
                   "".join(studio_card(*s, target=(s[0] == "s11")) for s in SNN), "Q5 A")
files["q5-a.html"] = studio_page.replace('<span class="h1-section">Report</span>',
                                         '<span class="h1-section">Studio</span>').replace(
    '<section class="focus-card">', '<section class="focus-card diff">')
files["q5-b.html"] = page(T02, ["MindMap", "Results"], "MindMap",
                          f'<div class="pv-dim">{map_by_snn()}</div><div class="pv-pop diff"><header>'
                          f'<b>s11-block-ui-report</b><span>Close</span></header>{studio_card(*SNN[0])}</div>', "Q5 B")
files["q5-c.html"] = page(T02, ["MindMap", "Results"], "MindMap", map_by_snn(open_s11=True), "Q5 C")

for name, html in files.items():
    (HERE / name).write_text(html)
print("wrote", len(files), "previews")
