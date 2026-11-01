"""Write the previews of r01_collect_block_report_views (b35 s11 · Block × Report).

Each preview starts from the real b35_studio page on the host (its head, inline CSS, path, title, Purpose and rails)
and changes only the view-button-list and the content. Run with the system python3 (Playwright shoots map.png):

    python3 build_previews.py

Never edit a q*.html by hand; change this script and rerun it.
"""
import html
import re
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
HOST = "http://100.121.165.84:5623"
B35 = "blueprints/Project-PageParts/work/b35_studio"
PAGE = f"{HOST}/_board/workbench?layout=focus&path={B35}"
Q = "%2F"


def get(url):
    return urllib.request.urlopen(url, timeout=60).read().decode("utf-8")


report = get(PAGE + "&section=report&group=mindmap")
studio = get(PAGE + "&section=studio&group=Studio")
WIRES = re.search(r"<script>\s*\(function\(\)\{if\(window\.__pmMap\).*?</script>", report, re.S).group(0)
MAP = re.search(r'<div class="focus-map">.*?</div></div></div></div>', report, re.S).group(0)
MAP = re.sub(r"<script>.*?</script>", "", MAP, flags=re.S)
MAP = MAP.replace('class=pm-edit', 'class=pm-view').replace('data-endpoint="/_board/mindmap"', '')
MAP = MAP.replace(" data-edit=", " data-was=")          # a preview never edits the real map

EXTRA = """<style>
.pv-panel{border:1px solid #dee2e6;border-radius:8px;padding:8px 12px;margin:0 0 10px}
.pv-panel>h3{margin:0 0 4px;font-size:14px}
.pv-panel .glance-list{margin:0;font-size:13px}
.pv-panel .glance-list li{padding:0;margin:0;border:0;line-height:1.55}
.pv-panel .pv-sub{margin:6px 0 2px}
.pv-map img{width:100%;height:150px;object-fit:cover;object-position:left top;display:block}
.pv-word{display:inline-block;margin-left:6px;padding:0 6px;border:1px solid #ced4da;border-radius:10px;font-size:12px;color:#495057}
.pv-to{color:#495057;font-size:13px;margin:2px 0}
.pv-sub{margin:12px 0 4px;font-size:14px}
.pv-tasknn{list-style:none;margin:4px 0 0;padding:0;font-size:12px}
.pv-tasknn li{padding:1px 0}
.pv-pop{position:fixed;inset:40px 60px;background:#fff;border:1px solid #868e96;border-radius:10px;box-shadow:0 8px 30px rgba(0,0,0,.25);z-index:50;display:flex;flex-direction:column}
.pv-pop header{padding:6px 12px;border-bottom:1px solid #dee2e6;font-size:13px;display:flex;justify-content:space-between}
.pv-pop iframe{flex:1;border:0;width:100%}
.pv-dim{position:fixed;inset:0;background:rgba(0,0,0,.25);z-index:40}
</style>"""

# the real sNN of b35, as their faces and delivery folders say (word: review-guide.md "draft for review", else planned)
SKILL = [
    ("s01-studio-skill", "What a Studio is, and what each sNN delivers", "haipipe-studio SKILL.md, its opening", "draft", "haipipe-studio"),
    ("s03-mindmap-leaf-drawing", "One leaf, one drawing", "haipipe-mindmap SKILL.md, mmsketch.py, mmmap.py", "draft", "haipipe-mindmap"),
    ("s04-delivery-gallery", "Delivery gallery: one real delivery per kind", "haipipe-delivery ref/gallery.md", "draft", "haipipe-delivery"),
    ("s05-studio-gallery", "Studio gallery: one real sNN per kind", "haipipe-studio ref/gallery.md", "draft", "haipipe-studio"),
    ("s09-delivery-skill", "Delivery skill: built, accepted, sent", "haipipe-delivery's guide: where it goes, its version, a checklist", "draft", "haipipe-delivery"),
    ("s21-studio-skills", "The skills b35 covers", "the map of b35's skills", "planned", "every b35 skill"),
]
T = "j02_studio_pages/"
UI = [
    ("s02-studio-pages", "The Studio on every page", "focus_page.py, focus.css: the Studio inside every page", "draft", "Every page"),
    ("s08-mindmap-page", "Mind map page: read and edit in place", "an interactive map page", "draft", "Every page"),
] + [(f"s{n}-{lv.lower()}-ui-{sec.lower()}", f"{lv} UI: {sec}", f"the rules for the Studio part in a {lv} page's {sec}",
      "planned", f"{lv} page", task)
     for lv, task, nums in (("Block", "t02_block_page", (11, 12, 13)), ("Job", "t03_job_page", (14, 15, 16)),
                            ("Task", "t04_task_page", (17, 18, 19)))
     for n, sec in zip(nums, ("Report", "Work", "Studio"))]


def folder(row):
    return f"{B35}/{T}{row[5]}/{row[0]}" if len(row) > 5 else f"{B35}/{row[0]}"


def esc(s):
    return html.escape(s, quote=True)


def card_url(row):
    path, name = folder(row).rsplit("/", 1)
    return f"/_board/workbench?path={path.replace('/', Q)}&layout=focus&section=studio#{name}"


def tags(row):
    f, n = folder(row), row[0]
    fq = f.replace("/", Q)
    return ('<p class="row-verbs">'
            f'<a class="row-verb main" href="/{f}/{n}.slides.html">Slide</a>'
            f'<a class="row-verb" href="/_excalidraw/?board={fq}{Q}{n}.excalidraw">Draw</a>'
            f'<a class="row-verb" href="/_board/workbench?view=focus-map&amp;path={fq}{Q}{n}.mindmap.md">Mind map</a>'
            f'<a class="row-verb" href="/_board/workbench?view=focus-part&amp;part=work&amp;path={fq}">Work</a>'
            f'<a class="row-verb" href="/_board/workbench?view=focus-delivery&amp;path={fq}">Delivery</a></p>')


def row_html(row, cls=""):
    """One delivery in a Report view: its sNN, its title, its one word; the thing it hands over; the tags below."""
    return (f'<article class="status-row studio-row{cls}" id="{row[0]}"><div>'
            f'<p class="row-title"><a class="row-name" href="{card_url(row)}">{row[0]}</a> {esc(row[1])}'
            f'<span class="pv-word">{row[3]}</span></p>'
            f'<p class="pv-to">hands over: {esc(row[2])}</p>{tags(row)}</div></article>')


def line(row, kind=False):
    mark = "⬜"
    return (f'<li>{mark} <a href="{card_url(row)}"><b>{row[0]}</b></a> {esc(row[1])} '
            f'<span class="mut">· {"skill" if kind == "skill" else "ui" if kind == "ui" else ""}{" · " if kind else ""}{row[3]}</span></li>')


def page(views, current, caption, content, diff_bar=False, tail=""):
    """The real page with its bar and content replaced; scripts removed (the map's wires come back when drawn)."""
    s = report
    bar = (f'<nav class="section-views{" diff" if diff_bar else ""}" aria-label="Views">'
           + "".join('<a href="#"' + (' aria-current="page"' if v == current else '') + f'>{v}</a>' for v in views) + "</nav>")
    s = re.sub(r'<nav class="section-views".*?</nav>', lambda m: bar, s, flags=re.S)
    start = s.index('<section class="focus-card">')
    end = s.index("</section><footer>", start)
    body = f'<section class="focus-card"><div class="focus-content"><p class="view-caption">{esc(caption)}</p>{content}</div>'
    s = s[:start] + body + s[end:]
    s = re.sub(r"<script>.*?</script>", "", s, flags=re.S)
    wires = WIRES if "class=pm " in content or "class=pm>" in content else ""
    return s.replace("</head>", EXTRA + "</head>").replace("</body>", tail + wires + "</body>")


def write(name, text):
    (HERE / name).write_text(text, encoding="utf-8")
    print("wrote", name)


# ---- Q1 · the view list: each view as its own small panel -------------------------------------------------------
MAPCAP = "How it is built, as a map: its parts, and what each must find out."
mini_map = ('<div class="pv-panel"><h3>MindMap</h3><p class="mut" style="margin:0">the map, as today '
            '(Q2 asks what it holds)</p></div>')


def panel(name, items, diff=True):
    return f'<div class="pv-panel{" diff" if diff else ""}"><h3>{name}</h3><ul class="glance-list">{items}</ul></div>'


skill_items = "".join(line(r) for r in SKILL)
ui_items = "".join(line(r) for r in UI)
all_items = "".join(line(r, "skill") for r in SKILL) + "".join(line(r, "ui") for r in sorted(UI))
status_m = re.search(r'<h3 class="focus-sub">Studio</h3>.*?</ul><h3 class="focus-sub">Jobs and Tasks</h3><ul class="glance-list status-now">.*?</ul>',
                     get(PAGE + "&section=report&group=standing"), re.S).group(0)
status_items = re.sub(r'<h3 class="focus-sub">(.*?)</h3>', r'<p class="pv-sub"><b>\1</b></p>', status_m)
words = {r[0]: r[3] for r in SKILL + UI}
status_plus = re.sub(r'(<b>b35[^<]*-(s\d\d):[^<]*@ ([a-z_]+)</b></a>[^<]*)<span class="mut">· ([a-z]+)</span>',
                     lambda m: m.group(1) + f'<span class="mut">· {m.group(4)}</span>'
                     + next((f'<span class="pv-word">{w}</span>' for k, w in words.items() if k.startswith(m.group(2) + "-")), ""),
                     status_items)
status_panel = lambda txt, diff: f'<div class="pv-panel{" diff" if diff else ""}"><h3>Status</h3>{txt}</div>'

write("q1-a.html", page(["MindMap", "Skill", "UI"], "MindMap", "Each view below is one button of the bar.",
                        mini_map + panel("Skill", skill_items) + panel("UI", ui_items), True))
write("q1-b.html", page(["MindMap", "Deliveries"], "MindMap", "Each view below is one button of the bar.",
                        mini_map + panel("Deliveries", all_items), True))
write("q1-c.html", page(["MindMap", "Status"], "MindMap", "Each view below is one button of the bar.",
                        mini_map + status_panel(status_plus, True), True))
write("q1-d.html", page(["MindMap", "Skill", "UI", "Status"], "MindMap", "Each view below is one button of the bar.",
                        mini_map + panel("Skill", skill_items) + panel("UI", ui_items) + status_panel(status_items, True), True))

# ---- Q2 · MindMap: the real map, changed only where the option changes it ----------------------------------------
BAR1 = ["MindMap", "Skill", "UI"]


def under_task(task, rows):
    lis = "".join(f'<li><a class="pm-role pm-open pm-draw" href="/_excalidraw/?board={folder(r).replace("/", Q)}{Q}{r[0]}.excalidraw">'
                  f'✎ {r[0]}</a> {esc(r[1])}</li>' for r in rows if r[5] == task)
    return f'<ul class="pv-tasknn diff">{lis}</ul>'


m_a = re.sub(r'(<div class=pm-para data-p="[^"]*/j02_studio_pages">)', r'<div class="diff">\1', MAP)
# close the wrapper right after the j02 paragraph (the map's last paragraph)
m_a = re.sub(r'(<div class="diff"><div class=pm-para .*?</ul></div>)', r'\1</div>', m_a, count=1, flags=re.S)
m_b = MAP
for task in ("t02_block_page", "t03_job_page", "t04_task_page"):
    m_b = re.sub(rf'(data-s="[^"]*/{task}">.*?<div class=pm-detail><p>.*?</p>)', lambda m: m.group(1) + under_task(task, UI[2:]), m_b,
                 count=1, flags=re.S)
m_c = re.sub(r'<div class=pm-para data-p="[^"]*/j0\d_[a-z_]+">.*?</ul></div>(<div class=pm-q>.*?</div>)?', "", MAP, flags=re.S)
m_c = re.sub(r'(<div class=pm-para data-p="[^"]*/group/Skills">)', r'<div class="diff">\1', m_c)
m_c = re.sub(r'(<div class="diff"><div class=pm-para .*?</ul></div>)', r'\1</div>', m_c, count=1, flags=re.S)
write("q2-a.html", page(BAR1, "MindMap", MAPCAP, m_a))
write("q2-b.html", page(BAR1, "MindMap", MAPCAP, m_b))
write("q2-c.html", page(BAR1, "MindMap", MAPCAP, m_c))

# ---- Q3 · Skill: one row per delivery, three orders ------------------------------------------------------------
SKCAP = "What each sNN hands over to a skill, and its one word."
write("q3-a.html", page(BAR1, "Skill", SKCAP, '<div class="diff">' + "".join(row_html(r) for r in SKILL) + "</div>"))
by_skill = ""
for target in ("haipipe-studio", "haipipe-mindmap", "haipipe-delivery", "every b35 skill"):
    by_skill += f'<h3 class="focus-sub diff">{target}</h3>' + "".join(row_html(r) for r in SKILL if r[4] == target)
write("q3-b.html", page(BAR1, "Skill", SKCAP, by_skill))
by_word = ""
for w in ("draft", "planned"):
    by_word += f'<h3 class="focus-sub diff">{w}</h3>' + "".join(row_html(r) for r in SKILL if r[3] == w)
write("q3-c.html", page(BAR1, "Skill", SKCAP, by_word))

# ---- Q4 · UI: one row per delivery; by level, or by section ----------------------------------------------------
UICAP = "What each sNN hands over to the workbench's pages, and its one word."
write("q4-a.html", page(BAR1, "UI", UICAP, '<div class="diff">' + "".join(row_html(r) for r in UI) + "</div>"))
by_level = ""
for lv in ("Every page", "Block page", "Job page", "Task page"):
    by_level += f'<h3 class="focus-sub diff">{lv}</h3>' + "".join(row_html(r) for r in UI if r[4] == lv)
write("q4-b.html", page(BAR1, "UI", UICAP, by_level))
by_sec = '<h3 class="focus-sub diff">Every page</h3>' + "".join(row_html(r) for r in UI[:2])
for sec in ("Report", "Work", "Studio"):
    by_sec += f'<h3 class="focus-sub diff">{sec}</h3>' + "".join(row_html(r) for r in UI[2:] if r[1].endswith(sec))
write("q4-c.html", page(BAR1, "UI", UICAP, by_sec))

# ---- Q5 · a click on a row's sNN name --------------------------------------------------------------------------
s01 = SKILL[0]
studio_page = re.sub(r"<script>.*?</script>", "", studio, flags=re.S)
studio_page = studio_page.replace('class="status-row studio-row" id="s01-studio-skill"',
                                  'class="status-row studio-row diff" id="s01-studio-skill" style="outline:3px solid #1864ab;outline-offset:3px"')
write("q5-a.html", studio_page.replace("</head>", EXTRA + "</head>"))
pop = lambda title, src: (f'<div class="pv-dim"></div><div class="pv-pop diff"><header><b>{esc(title)}</b><span>✕ close</span></header>'
                          f'<iframe src="{src}"></iframe></div>')
skill_view = "".join(row_html(r) for r in SKILL)
write("q5-b.html", page(BAR1, "Skill", SKCAP, skill_view,
                        tail=pop("s01-studio-skill · its delivery", f"/{B35}/s01-studio-skill/delivery/deck/index.html")))
write("q5-c.html", page(BAR1, "Skill", SKCAP, skill_view,
                        tail=pop("s01-studio-skill.md", f"/_board/page?path=%2F{B35.replace('/', Q)}{Q}s01-studio-skill{Q}s01-studio-skill.md")))

