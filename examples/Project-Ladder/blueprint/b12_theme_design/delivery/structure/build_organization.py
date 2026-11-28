"""Design Board and Design Method Book structure, drawn as b17's folder tree (trace 261127/1305).

Imports b17's shared drawing code (tree_html, organization_map, STYLE) and adds only design's own trees: the
naming rules (Structure, Draw) and examples embedded with their rules. Reads records, never writes them.

    python build_organization.py           build design-board.html and design-methodbook.html
    python build_organization.py --check   check both pages and both topics' studio-views.json
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from html import escape as esc
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
BLOCK = HERE.parents[1]
ROOT = next(p for p in HERE.parents if (p / "PRINCIPLE.md").is_file())
_spec = importlib.util.spec_from_file_location(
    "b17_organization", ROOT / "examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/build_organization.py")
org = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(org)
node = org.node

KINDS = {   # kind: (page file, Block name, example Block, topic)
    "board": ("design-board.html", "Design Board", "examples/Project-Ladder/design/Design-Example", "s01-design"),
    "book": ("design-methodbook.html", "Design Method Book",
             "examples/Project-Ladder/design/DesignMethodBook-Example", "s02-workbench-ui"),
}
METHODS = ROOT / "plugins/haipipe-toolkit/skills/3_theme/design/hai-design-method/methods"
TASK_GROUP = {"t00": "Ideas", "design": "Designs", "t99": "Review"}
NAMING = "Fixed name · 〈Name for this work〉"
TREE_CSS = "/examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/structure.css"
LEVELS = ("", "job-group", "job-name", "task-group", "task-name")

PURPOSE = {   # each folder's job, the hover on the rule tree
    "Design-〈app〉/": "a Design Board: one application in one channel, its designs and their results",
    "DesignMethodBook-〈topic〉/": "a Method Book: the design methods one kind of thing is made by",
    "board.md": "the Block's face: goals, Jobs and Studio topics",
    "inputs/": "the Board's inputs versions; in a Job, its fence: only what the method may read",
    "inputs-vN/": "one frozen inputs version: rules, theory, handoff links",
    "observed/": "what experiments returned, once per experiment",
    "eNN_〈exp〉/": "one experiment's per-arm totals (frozen)",
    "runs/": "Runs, each one try with its result",
    "jNN_〈goal〉_M0x-〈method〉-mK_inputs-vM/": "a Job: one goal × one method version × one inputs version → N designs",
    "jNN_〈job〉.md": "the Job's face: its pins (goal, method, inputs) and state",
    "t00_reason-ideas/": "the ideas the designs come from",
    "tNN_dNN_〈design〉/": "one design: its draft, checks, revisions and prediction",
    "t99_review-whole/": "the ranking of all designs; the kept ones",
    "jNN_M0x-〈method〉/": "one method type: its steps and its signed versions",
    "mK.md": "one signed version of the method",
    "proposals/": "changes proposed to the methods, from Boards and experiments",
    "sNN-〈topic〉/": "a Studio topic: a drawing or design to talk through",
    "trace/": "a record of each change, by day",
    "related/": "what came in from outside; made when first needed",
    "delivery/": "what the Block hands out: the released designs",
}


def rule_folder(kind):
    tail = (node("sNN-〈topic〉/"), node("trace/"), node("related/"), node("delivery/"))
    if kind == "book":
        return node("DesignMethodBook-〈topic〉/", node("board.md"),
                    node("jNN_M0x-〈method〉/", node("jNN_〈job〉.md"), node("mK.md")), node("proposals/"), *tail)
    task = lambda name: node(name, node("runs/"))
    return node("Design-〈app〉/", node("board.md"), node("inputs/", node("inputs-vN/")),
                node("observed/", node("eNN_〈exp〉/")), node("runs/"),
                node("jNN_〈goal〉_M0x-〈method〉-mK_inputs-vM/", node("jNN_〈job〉.md"), node("inputs/"),
                     task("t00_reason-ideas/"), task("tNN_dNN_〈design〉/"), task("t99_review-whole/")), *tail)


def rule_jobs(kind):
    if kind == "book":
        return (node("Design Method Book", node("〈Method family〉", node("M0x · 〈method〉"))),
                ("Job group · optional", "Job name"))
    job = node("〈goal〉 · 〈M0x mK〉 · 〈inputs-vM〉", node("Ideas", node("reason ideas")),
               node("Designs", node("〈design name〉")), node("Review", node("review whole")))
    return node("Design Board", node("〈Method family〉", job)), ("Job group · optional", "Job name", "Task group", "Task name")


def family(method_id):
    card = next(METHODS.glob(method_id + "-*/method.md"), None)
    m = re.search(r"(?m)^family:\s*(.+)$", card.read_text()) if card else None
    return m.group(1).strip() if m else "Methods"


def heading(folder):
    text = (folder / (folder.name + ".md")).read_text()
    h = next((x[2:].strip() for x in text.splitlines() if x.startswith("# ")), folder.name)
    return re.sub(r"^[jtd]\d+\s*·\s*", "", h)


def task_group(task):
    return TASK_GROUP["t00" if task.name.startswith("t00") else "t99" if task.name.startswith("t99") else "design"]


def jobs(kind):
    """(Job group, Job name, Job face, [(Task group, Task name, Task face)]) from the example Block's folders."""
    out = []
    for job in sorted(p for p in (ROOT / KINDS[kind][2]).iterdir() if re.match(r"^j\d\d_", p.name)):
        face = job / (job.name + ".md")
        pin = re.search(r"(?m)^method:\s*(M\d\d)", face.read_text())
        mid = pin.group(1) if pin else job.name.split("_")[1][:3]
        if kind == "board":
            pins = re.search(r"_(M\d\d)-[a-z-]+-(m\d+)_(inputs-v\d+)$", job.name)
            goal = re.search(r"(?m)^goal:\s*(G\d+)", face.read_text())
            name = f'{job.name[:3]} · {goal.group(1) if goal else ""} · {pins.group(1)} {pins.group(2)} · {pins.group(3)}'
        else:
            name = f"{job.name[:3]} · {heading(job)}"
        tasks = [(task_group(t), heading(t), t / (t.name + ".md"))
                 for t in sorted(job.iterdir()) if re.match(r"^t\d\d_", t.name)]
        out.append((family(mid), name, face, tasks))
    return out


def job_tree(rows, block):
    groups = {}
    for fam, name, face, tasks in rows:
        groups.setdefault(fam, []).append((name, tasks))
    branch = lambda name, tasks: node(name, *[node(g, *[node(t) for tg, t, _ in tasks if tg == g])
                                             for g in dict.fromkeys(tg for tg, _, _ in tasks)])
    return node(block, *[node(f, *[branch(n, t) for n, t in js]) for f, js in groups.items()])


def sources(rows):
    out = {}
    for fam, name, face, tasks in rows:
        out[(fam, name)] = (face, "")
        for g, t, tface in tasks:
            out[(fam, name, g, t)] = (tface, "")
    return out


def folder_tree(path):
    skip = {"__pycache__", "_old"}
    kids = [folder_tree(c) for c in sorted(path.iterdir()) if not c.name.startswith(".") and c.name not in skip] \
        if path.is_dir() else []
    return node(path.name + ("/" if path.is_dir() else ""), *kids)


def studio_tree(kind):
    example = ROOT / KINDS[kind][2]
    topics = [node(heading(s) if (s / (s.name + ".md")).is_file() else s.name)
              for s in sorted(example.iterdir()) if re.match(r"^s\d\d-", s.name)]
    return node(KINDS[kind][1], *topics)


def section(key, body, hidden=True):
    return f'<section id="{key}" title="{esc(NAMING)}"' + (" hidden" if hidden else "") + f">{body}</section>"


def tree_rows(tree, path=(), indexes=()):
    label, children = tree
    yield label, children, path, indexes
    for i, child in enumerate(children):
        yield from tree_rows(child, path + (child[0],), indexes + (i,))


def tree_block(tree, folder=False, purpose=False, roles=(), bindings=None):
    """Annotate the shared folder tree with roles, links and common S71 level colors."""
    if folder:
        def folders_first(item):
            label, children = item
            return node(label, *(folders_first(c) for c in sorted(children, key=lambda c: not c[0].endswith("/"))))
        tree = folders_first(tree)
    rows = list(tree_rows(tree))
    rendered = org.tree_html(tree, folder=folder)
    current = iter(rows)

    def annotate(match):
        label, children, path, indexes = next(current)
        depth = len(indexes)
        role = roles[depth - 1] if 0 < depth <= len(roles) else ""
        why = PURPOSE.get(label, "") if purpose else ""
        detail = " · ".join(part for part in (role, why) if part) or label
        if label in ("reason ideas", "review whole", "〈design name〉"):
            detail += " · " + {"reason ideas": "design-reason", "review whole": "design-whole",
                                "〈design name〉": "design-item"}[label]
        level = LEVELS[depth] if roles and depth < len(LEVELS) else ""
        node_id = "n" + "-".join(map(str, indexes))
        parent = "n" + "-".join(map(str, indexes[:-1])) if indexes else ""
        tag = "summary" if children else "span"
        attrs = {"class": "lvl" if children else "leaf lvl", "title": detail,
                 "data-node": node_id, "data-parent": parent, "data-level": level}
        label_html = esc(label)
        source = (bindings or {}).get(path)
        if source:
            url = org.source_url(source[0])
            if url:
                label_html = f'<a href="{esc(url, quote=True)}" target="_self">{label_html}</a>'
        opening = "<" + tag + " " + " ".join(f'{k}="{esc(v, quote=True)}"' for k, v in attrs.items()) + ">"
        return opening + match.group(2) + label_html + "</" + tag + ">"

    rendered = re.sub(r'(<summary>|<span class="leaf">)(<span aria-hidden="true">.*?</span> )(.*?)(</summary>|</span>)',
                      annotate, rendered)
    parents = iter((label, len(indexes)) for label, children, _, indexes in rows if children)

    def opened(_):
        label, depth = next(parents)
        keep = depth == 0 or (depth == 1 and (bool(roles) or (folder and label.startswith("j"))))
        return "<details open>" if keep else "<details>"

    rendered = re.sub(r'<details open>', opened, rendered)
    return '<div class="drawing"><ul class="tree rule"><li>' + rendered + "</li></ul></div>"


def render(kind):
    org.PURPOSE = PURPOSE                       # b17's tree_html reads the hover words from its module
    page, block, example, _ = KINDS[kind]
    jtree, headings = rule_jobs(kind)
    rows = jobs(kind)
    real = {
        "folder": tree_block(folder_tree(ROOT / example), True),
        "jobs": tree_block(job_tree(rows, block), roles=headings, bindings=sources(rows)),
        "studio": tree_block(studio_tree(kind)),
    }
    def with_example(key, body):
        return body + (f'<details class="structure-example"><summary>{esc(example.split("/")[-1])}</summary>'
                       f'<div id="{key}">{real[key]}</div></details>')
    bands = [node(f"{name} · {band}") for name, band, _ in org._studio_types()]
    rules = [section("folder-rules", with_example("folder", tree_block(rule_folder(kind), True, True)), hidden=False),
             section("jobs-rules", with_example("jobs", tree_block(jtree, roles=headings))),
             section("studio-rules", with_example("studio", tree_block(node(block, *bands))))]
    # Draw's existing bindings keep their current drawing; Structure never renders a mind map.
    drawings = [section("folder-rules-draw", tree_block(rule_folder(kind), True, True)),
                section("jobs-rules-draw", org.organization_map(tree=jtree, headings=headings)),
                section("studio-rules-draw", org.organization_map(tree=node(block, *bands), headings=("Studio Band",)))]
    script = """<script>function pick(){const hash=location.hash.slice(1),draw=hash.endsWith('-draw');
const raw=hash.replace(/-draw$/,''),want=['folder','jobs','studio'].includes(raw)?raw+'-rules':raw;
const key=document.getElementById(want+(draw?'-draw':''))?want+(draw?'-draw':''):'folder-rules';
document.body.dataset.mode=draw?'draw':'structure';document.querySelectorAll('main>section').forEach(s=>s.hidden=s.id!==key);}
addEventListener('hashchange',()=>{pick();if(window.pmDraw)requestAnimationFrame(window.pmDraw)});pick();</script>"""
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f"<title>{esc(block)} structure</title><style>{org.STYLE}</style>"
            f'<link rel="stylesheet" href="{TREE_CSS}"><style>.rule .lvl a{{color:inherit}}'
            '.content>section[hidden]{display:none!important}</style></head><body><main class="content">'
            + "".join(rules + drawings) + "</main>" + script + "</body></html>")


def manifest(kind):
    page, block, example, topic = KINDS[kind]
    path = f"examples/Project-Ladder/blueprint/b12_theme_design/delivery/structure/{page}"
    three = lambda suffix: [{"name": n, "path": path, "fragment": f + suffix} for n, f in
                            (("Folder", "folder"), ("Job / Task Organization", "jobs"), ("Studio Organization", "studio"))]
    rules = lambda draw: [dict(i, fragment=i["fragment"] + "-rules" + draw) for i in three("")]
    return [{"name": "Structure", "items": rules("") + [{"name": example.split("/")[-1], "block": example}]},
            {"name": "Draw", "items": rules("-draw")}]


def write_manifests():
    for kind, (_, _, _, topic) in KINDS.items():
        p = BLOCK / topic / "studio-views.json"
        views = json.loads(p.read_text())["views"]
        skills = [v for v in views if v["name"] == "Skills"]
        content = json.dumps({"views": manifest(kind) + skills}, indent=2, ensure_ascii=False) + "\n"
        if p.read_text() != content:
            p.write_text(content)


class StructureRows(HTMLParser):
    def __init__(self):
        super().__init__()
        self.section = ""
        self.rows = {}
        self.links = []
        self.maps = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "section":
            self.section = attrs.get("id", "")
        if self.section not in ("folder-rules", "jobs-rules", "studio-rules"):
            return
        if "data-node" in attrs:
            self.rows.setdefault(self.section, []).append(attrs)
        if tag == "a":
            self.links.append(attrs.get("href", ""))
        if "pm-map" in attrs.get("class", "") or (tag == "iframe" and "focus-map" in attrs.get("src", "")):
            self.maps.append(self.section)

    def handle_endtag(self, tag):
        if tag == "section":
            self.section = ""


def check_structure(html, kind):
    parsed = StructureRows()
    parsed.feed(html)
    errors = []
    if parsed.maps:
        errors.append("Structure contains a mind map")
    for key in ("folder-rules", "jobs-rules", "studio-rules"):
        if not parsed.rows.get(key) or any(not row.get("title") for row in parsed.rows[key]):
            errors.append(f"{key}: missing folder-tree rows or hover meanings")
    jtree, _ = rule_jobs(kind)
    expected = list(tree_rows(jtree)) + list(tree_rows(job_tree(jobs(kind), KINDS[kind][1])))
    actual = parsed.rows.get("jobs-rules", [])
    if len(actual) != len(expected):
        errors.append("Job tree drops or duplicates records")
    for row, (_, _, _, indexes) in zip(actual, expected):
        depth = len(indexes)
        parent = "n" + "-".join(map(str, indexes[:-1])) if indexes else ""
        if depth > (4 if kind == "board" else 2) or row.get("data-parent") != parent:
            errors.append("Job tree changes ownership or adds an absent level")
        if depth < len(LEVELS) and row.get("data-level") != LEVELS[depth]:
            errors.append("Job tree uses the wrong shared level color")
    expected_links = [org.source_url(face) for face, _ in sources(jobs(kind)).values()]
    if sorted(parsed.links) != sorted(expected_links):
        errors.append("Job/Task source links differ from actual records")
    if TREE_CSS not in html or not (ROOT / TREE_CSS.lstrip("/")).is_file():
        errors.append("Missing shared S71 level stylesheet")
    return errors


def check():
    problems = []
    for kind, (page, block, example, topic) in KINDS.items():
        html = (HERE / page).read_text()
        if "<table" in html:
            problems.append(f"{page}: an HTML table; Structure is a tree")
        for key in ("folder-rules", "jobs-rules", "studio-rules", "folder", "jobs", "studio"):
            if f'id="{key}"' not in html:
                problems.append(f"{page}: no section {key}")
        problems.extend(f"{page}: {error}" for error in check_structure(html, kind))
        if html != render(kind):
            problems.append(f"{page}: stale; run build_organization.py")
        views = json.loads((BLOCK / topic / "studio-views.json").read_text())["views"]
        if [v["name"] for v in views] != ["Structure", "Draw", "Skills"]:
            problems.append(f"{topic}: views are not Structure, Draw, Skills")
        if views[:2] != manifest(kind):
            problems.append(f"{topic}: studio-views.json differs from the builder's")
        for v in next(v for v in views if v["name"] == "Skills")["items"]:
            if not (ROOT / v["path"]).is_file():
                problems.append(f"{topic}: skill file missing {v['path']}")
        if kind == "board" and "Task group" not in html:
            problems.append(f"{page}: no Task group level")
        if kind == "book" and "Task group" in html:
            problems.append(f"{page}: the Book stops at Job name")
        if html.count('class="structure-example"') != 3:
            problems.append(f"{page}: each rule must keep its corresponding example")
        if re.search(r'target=(?:"_blank"|_blank)', html):
            problems.append(f"{page}: source selections must open in the Block preview, not a popup")
        for name, band, _ in org._studio_types():
            if esc(f"{name} · {band}") not in html:
                problems.append(f"{page}: missing shared Band {band}")
        if not (ROOT / example / "board.md").is_file():
            problems.append(f"{page}: live example has no Block face")
    for p in problems:
        print("❗", p)
    print(("❗" if problems else "✅") + f" design structure: {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(check())
    for kind, (page, *_) in KINDS.items():
        (HERE / page).write_text(render(kind))
    write_manifests()
    print("Built design-board.html and design-methodbook.html; wrote both studio-views.json.")
