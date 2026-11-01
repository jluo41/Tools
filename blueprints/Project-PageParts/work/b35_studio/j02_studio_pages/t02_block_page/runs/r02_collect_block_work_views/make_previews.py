"""Write the previews of r02_collect_block_work_views (b35 s12, Block x Work).

Each preview is the real b35_studio Work page (its inline CSS, fetched from 5623) with only the view bar and the
content changed. Run: python3 make_previews.py  (needs the 5623 server; writes q<N>-<key>.html beside this file).
"""
import re
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
URL = ("http://100.121.165.84:5623/_board/workbench?layout=focus"
       "&path=blueprints/Project-PageParts/work/b35_studio&section=work")
page = urllib.request.urlopen(URL, timeout=20).read().decode()
STYLE = re.search(r"<style>.*?</style>", page, re.S).group(0)

EXTRA = """<style>
.focus-page{padding:18px 28px 30px;max-width:none}
.panels{display:grid;grid-template-columns:1fr 1fr;gap:14px;align-items:start}
.panels>*{min-width:0}
.panel{font-size:13px;line-height:1.45}
.panel .status-row{padding:8px 10px;margin:0 0 6px}
.panel .row-line{margin:2px 0}
.panel .focus-content{padding:0}
.panel{border:1px dashed var(--line);border-radius:10px;padding:10px 14px 4px}
.panel-name{font-size:12px;color:var(--muted);margin:0 0 4px}
.flag{border-color:light-dark(#ffa94d,#b35c00)!important;color:light-dark(#b35c00,#ffc078)!important}
.snn-link{color:var(--accent);text-decoration:underline}
.chip{display:inline-block;border:1px solid var(--accent);color:var(--accent);border-radius:999px;
      padding:0 9px;font-size:12px;margin-left:8px}
.none-line{color:var(--muted);font-size:13px;margin:6px 0 12px}
.where{color:var(--muted);font-size:12px;margin-left:8px}
.kid{margin-left:22px}
.pop{border:1px solid var(--line);border-radius:12px;box-shadow:0 8px 30px rgba(0,0,0,.18);
     padding:12px 16px;background:var(--paper)}
.pop-head{display:flex;justify-content:space-between;font-size:13px;color:var(--muted);margin-bottom:8px}
.fake-h1{font-size:18px;margin:4px 0 10px}
</style>"""

CRUMB = '<div class="focus-crumb">Tools-SPACE / blueprints / Project-PageParts / work / b35_studio</div>'


def bar(names, on):
    items = "".join(f'<a{" aria-current=page" if n == on else ""}>{n}</a>' for n in names)
    return f'<nav class="section-views" aria-label="Views">{items}</nav>'


def btn(text="Interaction", flag=False):
    return f'<a class="row-verb{" flag" if flag else ""}">{"🙋 " if flag else ""}{text}</a>'


def ix_row(title, run, about="s01-studio-skill", mark=""):
    return (f'<article class="status-row ix-row"><span class="row-name">{title}</span>'
            f'<p class="row-line">about <a class="snn-link">{about}</a></p>'
            f'<p class="row-meta">{mark}{run}{btn()}</p></article>')


IX = (ix_row("Studio follow-ups", "r01_collect_studio_followups")
      + ix_row("Deleting studio folders", "r02_collect_studio_removal"))
IX_DONE = (ix_row("Studio follow-ups", "r01_collect_studio_followups", mark="✅ answered · ")
           + ix_row("Deleting studio folders", "r02_collect_studio_removal", mark="✅ answered · "))

G1 = ("build what b35-s01 hands over: the haipipe-studio rule, the For: line, b35's renumbering, the scan of kinds, "
      "the s00 cleanup")
G2 = ("build what b35-s02 hands over: the Studio inside a page, an sNN's link landing on its card (s02-D05), the "
      "Studio card, the pop-outs")


def job(name, goal, meta, verbs="", link="text", snn=""):
    if link == "goal" and snn:
        goal = goal.replace(f"b35-{snn}", f'<a class="snn-link">b35-{snn}</a>')
    chip = f'<a class="chip">makes {snn}</a>' if link == "chip" and snn else ""
    return (f'<article class="status-row"><a class="row-name">{name}</a><p class="row-line">{goal}</p>'
            f'<p class="row-meta">{meta}{chip}{verbs}</p></article>')


def j01(link="text"):
    return job("j01_studio_delivery_type", G1, "✅ done · ⬜ open", link=link, snn="s01")


def j02(link="text"):
    return job("j02_studio_pages", G2, "⬜ open", btn(flag=True), link=link, snn="s02")


TASKS = [("t01_build_studio_pages", "build the Studio's UI as s02's agreed screen drafts show it", False),
         ("t02_block_page", "say how the Studio part shows in a Block page's Report, Work and Studio", True),
         ("t03_job_page", "say how the Studio part shows in a Job page's Report, Work and Studio", True),
         ("t04_task_page", "say how the Studio part shows in a Task page's Report, Work and Studio", True)]


def task_rows(only_waiting=False):
    out = ""
    for name, goal, waits in TASKS:
        if only_waiting and not waits:
            continue
        out += (f'<article class="status-row kid"><a class="row-name">{name}</a><p class="row-line">{goal}</p>'
                f'<p class="row-meta">⬜ open{btn(flag=True) if waits else ""}</p></article>')
    return out


def none_line(names):
    return f'<p class="none-line">No Job makes these yet: {" · ".join(names)}</p>'


def cap(text):
    return f'<p class="view-caption">{text}</p>'


def screen(names, on, body):
    return (CRUMB + '<h1>b35_studio<span class="h1-section">Work</span></h1>' + bar(names, on)
            + f'<section class="focus-card"><div class="focus-content">{body}</div></section>')


def panels(names, views):
    """Each view as its own small panel, its button on, so options that differ in views show every view."""
    out = ""
    for on, body in views:
        head = f'<p class="panel-name">{on} open</p>{bar(names, on)}' if on in names \
            else f'<p class="panel-name">{on}</p>'
        out += f'<div class="panel">{head}<div class="focus-content">{body}</div></div>'
    return (CRUMB + '<h1>b35_studio<span class="h1-section">Work</span></h1>'
            + f'<div class="panels">{out}</div>')


def write(name, title, body):
    html = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" '
            f'content="width=device-width,initial-scale=1"><title>{title}</title>{STYLE}{EXTRA}</head>'
            f'<body><main class="focus-page">{body}</main></body></html>')
    (HERE / name).write_text(html)


def run_row(name, where, mark, flag=False):
    return (f'<article class="status-row"><span class="row-name">{name}</span><span class="where">{where}</span>'
            f'<p class="row-meta">{mark}{btn(flag=True) if flag else ""}</p></article>')


SKILL = ["s01", "s03", "s04", "s05", "s09", "s21"]
UI = ["s02", "s08", "s11 to s19"]
SKILL_CAP = "The work that makes this Block's skill deliveries: " + ", ".join(SKILL) + "."
UI_CAP = "The work that makes this Block's ui deliveries: s02, s08, s11 to s19."
SKILL_VIEW = cap(SKILL_CAP) + IX + j01() + none_line(["s03", "s04", "s05", "s09", "s21"])
UI_VIEW = cap(UI_CAP) + j02() + none_line(["s08"])

# Q1 · the view list
write("q1-a.html", "Q1 A", screen(["Progress"], "Progress",
      cap("Its Jobs, and what this Block asks.") + IX + j01() + j02()))
write("q1-b.html", "Q1 B", panels(["Jobs", "Runs"], [
    ("Jobs", cap("One row per Job.") + j01() + j02()),
    ("Runs", cap("Runs not yet done, here and below; then this Block's own.")
     + run_row("r01_collect_block_report_views", "t02 · j02", "⬜ planned", True)
     + run_row("r02_collect_block_work_views", "t02 · j02", "⬜ planned", True)
     + run_row("run-fix-s00-links", "t05 · j01", "⬜ planned")
     + run_row("r01_collect_studio_followups", "b35", "✅ done")
     + run_row("r02_collect_studio_removal", "b35", "✅ done"))]))
write("q1-c.html", "Q1 C", panels(["Skill", "UI"], [("Skill", SKILL_VIEW), ("UI", UI_VIEW)]))
write("q1-d.html", "Q1 D", panels(["Now", "Done"], [
    ("Now", cap("What is open or waits on you.") + j02() + j01()),
    ("Done", cap("What is finished, newest first; each says where it lives.")
     + run_row("t04_scan_spaces", "j01", "✅ CLOSED")
     + run_row("t03_renumber_b18", "j01", "✅ CLOSED")
     + run_row("Deleting studio folders", "b35 · about s01", "✅ answered")
     + run_row("Studio follow-ups", "b35 · about s01", "✅ answered"))]))

# Q2 · the Skill view, top to bottom
write("q2-a.html", "Q2 A", screen(["Skill", "UI"], "Skill", SKILL_VIEW))
snn_heads = ""
for s, title in [("s01", "Studio skill"), ("s03", "Mind map leaf drawing"), ("s04", "Delivery gallery"),
                 ("s05", "Studio gallery"), ("s09", "Delivery skill"), ("s21", "Studio skills")]:
    snn_heads += f'<h3 class="focus-sub">{s} · {title}</h3>'
    snn_heads += (IX + j01()) if s == "s01" else '<p class="none-line">No Job yet.</p>'
write("q2-b.html", "Q2 B", screen(["Skill", "UI"], "Skill", cap(SKILL_CAP) + snn_heads))
write("q2-c.html", "Q2 C", screen(["Skill", "UI"], "Skill", cap("The Jobs that make skill deliveries.") + j01()))

# Q3 · the UI view: a Job and its Tasks
write("q3-a.html", "Q3 A", screen(["Skill", "UI"], "UI", UI_VIEW))
write("q3-b.html", "Q3 B", screen(["Skill", "UI"], "UI", cap(UI_CAP) + j02() + task_rows() + none_line(["s08"])))
write("q3-c.html", "Q3 C", screen(["Skill", "UI"], "UI",
      cap(UI_CAP) + j02() + task_rows(only_waiting=True) + none_line(["s08"])))

# Q4 · does a Job row link its sNN (the face's Open 1)
for key, link in (("a", "goal"), ("b", "chip"), ("c", "text")):
    write(f"q4-{key}.html", f"Q4 {key.upper()}", screen(["Skill", "UI"], "Skill",
          cap(SKILL_CAP) + j01(link) + none_line(["s03", "s04", "s05", "s09", "s21"])))

# Q5 · this Block's own forms (r01, r02, both answered)
write("q5-a.html", "Q5 A", screen(["Skill", "UI"], "Skill",
      cap(SKILL_CAP) + j01() + none_line(["s03", "s04", "s05", "s09", "s21"])))
write("q5-b.html", "Q5 B", screen(["Skill", "UI"], "Skill",
      cap(SKILL_CAP) + IX_DONE + j01() + none_line(["s03", "s04", "s05", "s09", "s21"])))
write("q5-c.html", "Q5 C", screen(["Skill", "UI"], "Skill",
      cap(SKILL_CAP) + job("j01_studio_delivery_type", G1, "✅ done · ⬜ open", btn())
      + none_line(["s03", "s04", "s05", "s09", "s21"])))

# Q6 · a click on a Job's name
job_page = ('<div class="pop"><div class="pop-head"><span>opens: the j02_studio_pages page</span><span>full page</span>'
            '</div><div class="focus-crumb">… / b35_studio / j02_studio_pages</div>'
            '<div class="fake-h1">j02_studio_pages <span class="h1-section">Work</span></div>'
            + bar(["Progress"], "Progress") + task_rows() + '</div>')
pop = ('<div class="pop"><div class="pop-head"><span>j02_studio_pages · Work</span><span>Open page · ✕</span></div>'
       + task_rows() + '</div>')
write("q6-a.html", "Q6 A", panels(["Skill", "UI"], [("UI", cap(UI_CAP) + j02()), ("after the click", job_page)]))
write("q6-b.html", "Q6 B", panels(["Skill", "UI"], [("UI", cap(UI_CAP) + j02()), ("after the click", pop)]))
print("ok")
