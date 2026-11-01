"""Write this form's previews (q1-a.html ...): the real j02_studio_pages Studio page, fetched live from 5623, with
only its view bar and its content changed to show each option. Rerun it; never edit the previews by hand.

    python3 make_previews.py
"""
import re
import urllib.parse
import urllib.request
from pathlib import Path

HOST = "http://100.121.165.84:5623"
HERE = Path(__file__).resolve().parent
J = "blueprints/Project-PageParts/work/b35_studio/j02_studio_pages"
B = "blueprints/Project-PageParts/work/b35_studio"
T04 = J + "/t04_task_page"
SPACE = HERE.parents[7]                                      # Tools-SPACE


def url(path, section="studio", group=""):
    q = {"layout": "focus", "path": path, "section": section}
    if group:
        q["group"] = group
    return HOST + "/_board/workbench?" + urllib.parse.urlencode(q)


def fetch(path, group=""):
    return urllib.request.urlopen(url(path, group=group), timeout=30).read().decode("utf-8")


def cards(page):
    """id -> the <article> of each Studio card on a page."""
    return {m.group(1): m.group(0) for m in re.finditer(r'<article class="status-row studio-row" id="([^"]+)">.*?</article>', page, re.S)}


def href(group):
    return "/_board/workbench?" + urllib.parse.urlencode({"path": J, "layout": "focus", "section": "studio", "group": group})


def bar(buttons, on, diff=True):
    links = "".join(f'<a href="{href(b)}"' + (' aria-current="page"' if b == on else "") + f">{b}</a>" for b in buttons)
    return f'<nav class="section-views studio-groups{" diff" if diff else ""}" aria-label="Views">{links}</nav>'


def caption(text, diff=False):
    return f'<p class="view-caption{" diff" if diff else ""}">{text}</p>'


def heading(text, diff=False):
    return f'<h3 class="focus-sub{" diff" if diff else ""}">{text}</h3>'


def mark(article):
    return article.replace('class="status-row studio-row"', 'class="status-row studio-row diff"', 1)


BASE = fetch(J, "Block UI")
ALL = {}
for g in ("Block UI", "Job UI", "Task UI"):
    ALL.update(cards(fetch(J, g)))
S02 = cards(fetch(B, "Studio"))["s02-studio-pages"]
T04_PAGE = fetch(T04)
EXTRA_CSS = (".pv-tag{margin-left:6px;font-size:12px;padding:1px 8px;border:1px solid var(--line);border-radius:9px;"
             "color:var(--muted);vertical-align:2px}.pv-line{padding:12px 0;border-bottom:1px solid var(--line);font-size:14px}"
             ".pv-line .row-name{font-size:14px}.pv-pop{position:fixed;inset:40px 60px;background:var(--paper);"
             "border:1px solid var(--line);border-radius:10px;box-shadow:0 10px 40px rgba(0,0,0,.25);padding:10px 16px;"
             "z-index:20;overflow:hidden}.pv-pop header{display:flex;justify-content:space-between;font-size:13px;"
             "color:var(--muted);border-bottom:1px solid var(--line);padding-bottom:6px;margin-bottom:10px}"
             ".pv-pop pre{font:13px/1.5 ui-monospace,Menlo,monospace;white-space:pre-wrap;margin:0}"
             ".pv-pop img{max-width:100%;max-height:calc(100% - 40px);display:block;margin:auto}"
             ".pv-dim{position:fixed;inset:0;background:rgba(0,0,0,.35);z-index:10}")
SET = ["s11-block-ui-report", "s12-block-ui-work", "s13-block-ui-studio"]
JOB = ["s14-job-ui-report", "s15-job-ui-work", "s16-job-ui-studio"]
TSK = ["s17-task-ui-report", "s18-task-ui-work", "s19-task-ui-studio"]
TAGS = ["Block UI", "Job UI", "Task UI"]


def page(name, nav, content, base=BASE, after=""):
    html = re.sub(r'<nav class="section-views studio-groups".*?</nav>', lambda m: nav, base, count=1, flags=re.S)
    html = re.sub(r'(<div class="focus-content">).*?(</div></section><footer>)', lambda m: m.group(1) + content + m.group(2),
                  html, count=1, flags=re.S)
    html = html.replace("</style>", EXTRA_CSS + "</style>", 1)
    html = re.sub(r"<title>.*?</title>", f"<title>{name}</title>", html, count=1)
    html = html.replace("</main>", after + "</main>", 1)
    (HERE / f"{name}.html").write_text(html, encoding="utf-8")


def rows(ids, fn=lambda a, i: a):
    return "".join(fn(ALL[i], i) for i in ids)


# Q1 · the view list, its first view open
page("q1-a", bar(TAGS, "Block UI"), rows(SET))
page("q1-b", bar(["t02_block_page", "t03_job_page", "t04_task_page"], "t02_block_page"),
     caption("t02 · The Studio on a Block page", True) + rows(SET))
page("q1-c", bar(["This Job"] + TAGS, "This Job"),
     caption("What this Job makes: b35-s02, named by its goal; then its own topics.", True) + mark(S02))
page("q1-d", bar(["Topics"], "Topics"),
     heading("Block UI", True) + rows(SET) + heading("Job UI", True) + rows(JOB) + heading("Task UI", True) + rows(TSK))

# Q2 · the This Job view
VIEW = ["This Job"] + TAGS
own_s02 = S02.replace('<span class="row-stage">', '<span class="pv-tag diff">made by j02</span><span class="row-stage">', 1)
page("q2-a", bar(VIEW, "This Job", False),
     caption("What this Job makes: b35-s02, named by its goal; then its own topics.") + own_s02)
page("q2-b", bar(TAGS, "Block UI", True), rows(SET))
s02_link = (f'<p class="pv-line diff">Makes <a class="row-name" href="/_board/workbench?'
            f'{urllib.parse.urlencode({"path": B, "layout": "focus", "section": "studio", "group": "Studio"})}#s02-studio-pages">'
            'b35-s02:studio @ studio_pages</a> (opens its card on b35_studio)</p>')
page("q2-c", bar(VIEW, "This Job", False), s02_link + '<p class="mut">No topic of its own yet.</p>')

# Q3 · a Tag view (Block UI shown): what heads its cards
VIEW_ON = lambda on: bar(VIEW, on, False)
page("q3-a", VIEW_ON("Block UI"), rows(SET))
page("q3-b", VIEW_ON("Block UI"), heading("t02_block_page · The Studio on a Block page", True) + rows(SET))
page("q3-c", VIEW_ON("Block UI"), caption("How the Studio part shows on a Block page: its Report, Work and Studio.", True) + rows(SET))


# Q4 · the card's address (Job UI shown)
def short(article, kind):
    m = re.search(r'<span class="row-address">([^<]*)</span>(<a class="row-name"[^>]*>)([^<]*)</a>', article)
    if not m:
        return article
    full, a_open, name = m.groups()
    snn = re.search(r"-(s\d+):", full).group(1)
    task = re.search(r"\.(t\d+)-s", full).group(1)
    if kind == "full":
        new = f'<span class="row-address diff">{full}</span>{a_open}{name}</a>'
    elif kind == "task":
        new = f'<span class="row-address diff">{task}-{snn} @ </span>{a_open}{name}</a>'
    else:
        new = f'<span class="diff">{a_open}{snn} · {name}</a><span class="pv-tag">{task}</span></span>'
    return article.replace(m.group(0), new, 1)


page("q4-a", VIEW_ON("Job UI"), rows(JOB, lambda a, i: short(a, "full")))
page("q4-b", VIEW_ON("Job UI"), rows(JOB, lambda a, i: short(a, "task")))
page("q4-c", VIEW_ON("Job UI"), rows(JOB, lambda a, i: short(a, "where")))


# Q5 · how much of a Task's card shows (Task UI shown)
def line_only(article, i):
    title = re.search(r'<p class="row-title">(.*?)</p>', article, re.S).group(1)
    return f'<p class="pv-line diff">{title}</p>'


def no_verbs(article, i):
    return mark(re.sub(r'<p class="row-verbs">.*?</p>', "", article, count=1, flags=re.S))


page("q5-a", VIEW_ON("Task UI"), rows(TSK, lambda a, i: mark(a)))
page("q5-b", VIEW_ON("Task UI"), rows(TSK, no_verbs))
page("q5-c", VIEW_ON("Task UI"), rows(TSK, line_only))

# Q6 · a click on a card's name (s17 on the Job page's Task UI view)
face = (SPACE / T04 / "s17-task-ui-report" / "s17-task-ui-report.md").read_text(encoding="utf-8")
face = face.split("\nFiles\n")[0].strip()
face = face.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
pop_face = (f'<div class="pv-dim"></div><div class="pv-pop diff"><header><span>s17-task-ui-report</span><span>Close</span></header>'
            f"<pre>{face}</pre></div>")
pop_draw = ('<div class="pv-dim"></div><div class="pv-pop diff"><header><span>s17-task-ui-report · drawing</span><span>Close</span></header>'
            f'<img src="/{T04}/s17-task-ui-report/s17-task-ui-report.png" alt="s17 drawing"></div>')
page("q6-a", VIEW_ON("Task UI"), rows(TSK), after=pop_face)
t04_cards = cards(T04_PAGE)
t04_rows = "".join(mark(t04_cards[i]).replace('class="status-row studio-row diff"',
                                               'class="status-row studio-row diff" style="outline:2px solid var(--accent);'
                                               'outline-offset:4px;border-radius:8px;background:var(--soft)"')
                   if i == "s17-task-ui-report" else t04_cards[i] for i in TSK if i in t04_cards)
page("q6-b", re.search(r'<nav class="section-views studio-groups".*?</nav>', T04_PAGE, re.S).group(0), t04_rows, base=T04_PAGE)
page("q6-c", VIEW_ON("Task UI"), rows(TSK), after=pop_draw)
print("wrote", sorted(p.name for p in HERE.glob("q*.html")))
