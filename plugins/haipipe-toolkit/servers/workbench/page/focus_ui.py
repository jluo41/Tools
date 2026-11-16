"""The focus page's UI views: a theme Block's page designs (matrix, structure, walks) and their to-dos."""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlencode

from live import frame, matrix_help
from live.ui_parts import PB_CSS, PB_JS, _side_tabs
from live.focus_base import UI_VIEWS, WORK_SHAPE, inside, markdown, page_level, page_url, read_face
from live.focus_styles_bands import BAND_CSS, band_sec


def ui_base(ref: str, folder: Path, root: Path) -> Path | None:
    """Where a theme Block's example path `ref` lives: this SPACE's root, else the nearest folder above the Block that
    holds it, inside the SPACE. A Tools blueprint names its placeholder from the Tools checkout's root
    (`blueprints/...`), which is the SPACE root when Tools is served on its own and `Tools/` inside a SPACE (261105)."""
    if ref.startswith(("/", ".")) or ".." in Path(ref).parts:
        return None
    for base in [root] + [p for p in Path(folder).parents if inside(p, root)]:
        page = (base / ref).resolve()
        if page.exists() and inside(page, root):
            return page
    return None


def ui_kind(page: Path) -> str:
    """A page's kind in a word or two, for its tab: its face's `task-type:` or `type:` (draft, value, labeling-meaning)."""
    face = page / f"{page.name}.md"
    text = face.read_text(encoding="utf-8", errors="ignore") if face.is_file() else ""
    m = re.search(r"(?m)^(?:task-type|type):\s*([^\s#]+)", text)
    if m:
        return m.group(1).replace("-", " ")
    words = [w for w in page.name.split("_")[1:] if not re.fullmatch(r"v\d+|desk|example", w)]
    return " ".join(words) or page_level(page).lower()   # a Job by its folder's words: "writing", "evidence value"


def ui_matrix_html(source: Path, root: Path) -> str:
    """Render the authored matrix (a row per type, a column per view) turned: a column per type, a row per view."""
    html = markdown(source.read_text(encoding="utf-8"), source.parent, root).replace('&lt;br&gt;', '<br>')
    if not re.search(r'<th>[^<]*\bCategory</th>', html):
        return html
    guide = matrix_help.guide_for(source, root)
    headings = re.findall(r'<th>(.*?)</th>', html, re.S)
    level = source.stem.removesuffix('-views')

    def explain(cell, kind, view):
        if matrix_help.plain(view) == 'Use Cases':
            if not guide:
                return cell
            from live import use_case_examples
            return '<br>'.join(use_case_examples.button(label, kind, source, root, guide, level)
                               if matrix_help.plain(label) else label for label in cell.split('<br>'))
        examples = guide.get('examples', {}).get(level, {})
        ref = examples.get(matrix_help.plain(kind), '')
        page = ui_base(ref, source.parent.parent, root) if ref else None
        group = {'MindMap': 'mindmap', 'Overview': 'overview', 'Delivery': 'delivery', 'Status': 'standing', 'Plan + Results': 'standing', 'Findings': 'findings',
                 'Project UI': 'ui-project', 'Block UI': 'ui-block', 'Job UI': 'ui-job', 'Task UI': 'ui-task', 'Run UI': 'ui-run'}.get(matrix_help.plain(view), 'mindmap')
        route = guide.get('view_routes', {}).get(matrix_help.plain(view), {})
        route = route if isinstance(route, dict) else {}
        specific = guide.get('type_view_routes', {}).get(level, {}).get(matrix_help.plain(kind), {}).get(matrix_help.plain(view), {})
        if isinstance(specific, dict):
            route = {**route, **specific}
        url = (frame.ROUTE + '?' + urlencode({'path': page.relative_to(root.resolve()).as_posix(),
               'layout': 'focus', 'section': route.get('section', 'report'), 'group': route.get('group', group)})) if page else ''
        if guide.get('proposed') or route.get('example') is False:
            url = ''  # Current examples do not implement the proposed view contract yet.
        return matrix_help.help_cell(cell, kind, view, level, guide, url)

    def turn(table):
        """The matrix turned (JL 261108: the table fits the page): a column per type under its category, a row per
        view; a row the same under every view (Around the Work) is said once, across the types. Each Category table
        is turned with its own headings, so a second family of types (a Design Method Book beside the Design Board,
        261109) keeps its own views."""
        headings = re.findall(r'<th>(.*?)</th>', table.group(0).split('</thead>')[0], re.S)
        if not any(matrix_help.plain(h) == 'Category' for h in headings):
            return table.group(0)
        rows = [re.findall(r'<td>(.*?)</td>', row, re.S)
                for row in re.findall(r'<tr>(.*?)</tr>', table.group(0).split('</thead>')[-1], re.S)]
        if not rows or any(len(row) < 3 for row in rows):
            return table.group(0)
        first = 3 if len(headings) > 2 and matrix_help.plain(headings[2]) == 'Use Cases' else 2
        spans = [r for r in rows if len(set(r[first:])) == 1 and len(r) > first + 1]
        types = [r for r in rows if r not in spans]
        groups, index = [], 0                    # adjacent types of one category share its heading
        while index < len(types):
            end = index + 1
            while end < len(types) and types[end][0] == types[index][0]:
                end += 1
            groups.append((types[index][0], end - index))
            index = end
        head = ('<thead><tr><th class="ui-view" rowspan="2"></th>'
                + ''.join(f'<th class="ui-category" colspan="{n}">{c}</th>' for c, n in groups) + '</tr><tr>'
                + ''.join(f'<th class="ui-block-type">{explain(r[1], r[1], "")}</th>' for r in types) + '</tr></thead>')
        body = ''.join('<tr><th class="ui-view" scope="row">' + headings[col] + '</th>'
                       + ''.join('<td>' + explain(r[col], r[1], headings[col]) + '</td>' for r in types) + '</tr>'
                       for col in range(2, len(headings)))
        body += ''.join(f'<tr class="ui-every"><th class="ui-view" scope="row">{r[1]}</th>'
                        f'<td class="ui-span" colspan="{len(types)}">{explain(r[first], r[1], "Every view")}</td></tr>'
                        for r in spans)
        columns = '<colgroup><col class="ui-view-column">' + '<col>' * len(types) + '</colgroup>'
        return (f'<table class="ui-turned" style="--ui-type-count:{len(types)}">'
                + columns + head + '<tbody>' + body + '</tbody></table>')

    html = re.sub(r'<table[^>]*>.*?</table>', turn, html, flags=re.S)
    return matrix_help.with_dialog(html, source) if guide else html


def ui_structure_html(source: Path, root: Path) -> str:
    """An optional design proposal: second-level headings are tabs, third-level headings are topics."""
    text = source.read_text(encoding='utf-8')
    parts = re.split(r'(?m)^## (.+)\n', text)
    panels, tabs = [], []
    for index in range(1, len(parts), 2):
        title, content = parts[index:index + 2]
        topics = re.split(r'(?m)^### (.+)\n', content)
        body = markdown(topics[0], source.parent, root)
        if len(topics) > 1:
            body += _side_tabs('proposal-topic-' + str(index),
                               [(topics[i], '') for i in range(1, len(topics), 2)],
                               [markdown(topics[i + 1], source.parent, root) for i in range(1, len(topics), 2)])
        tabs.append((title, ''))
        panels.append(body)
    return (PB_CSS + '<style>@media(max-width:700px){.ui-structure pre,.ui-structure pre code'
            '{white-space:pre-wrap;overflow-wrap:anywhere}}</style><div class="ui-structure">'
            + markdown(parts[0], source.parent, root)
            + _side_tabs('work-structure', tabs, panels) + '</div>' + PB_JS)


def ui_walk_path(walk, page, index, root):
    """The same recording lookup for the player and its completion checklist."""
    if walk is None:
        return None
    candidates = ([walk.with_name(f"{walk.stem}-{page.name}.html")] if page is not None else [])
    if index == 0:
        candidates.append(walk)
    return next((p for p in candidates if inside(p, root) and p.is_file()), None)


def ui_walk_checklist(folder, root, view=None):
    """Recording presence is derived from files, scoped to the selected UI view."""
    sections = []
    for key, name in UI_VIEWS:
        if view and view != 'ui-' + key:
            continue
        rows = []
        refs = read_face(folder, root)['ui'].get(key, [])
        shown = [(ref, ui_base(ref, folder, root)) for ref in refs]
        shown = [(ref, page) for ref, page in shown if page is not None or re.match(r'(?i)^https?://', ref)]
        for index, (_, page) in enumerate(shown):
            if page is None:
                continue
            recorded = ui_walk_path(folder / 'walks' / f'{key}.html', page, index, root)
            label = 'Recorded' if recorded else 'Not recorded'
            rows.append(f'<li><span>{"☑" if recorded else "☐"} Record walkthrough: '
                        f'<a href="{frame.esc(page_url(page, root))}">{frame.esc(page.name)}</a>'
                        f'</span><small>{label}</small></li>')
        if rows:
            sections.append((name, '<ul class="wk-rows">' + ''.join(rows) + '</ul>'))
    if view:
        return ''.join(body for _, body in sections)
    return ''.join(f'<h3>{frame.esc(name)}</h3>{body}' for name, body in sections)


def ui_view(refs, name: str, root: Path, folder: Path | None = None, walk: Path | None = None) -> str:
    """Real pages of the theme, live in the Report (JL 261031: "I think you should have these as well ... the block
    UI, job UI and task UI"). Each ref is a path to a placeholder page (ui_base) or a full http(s) link (another SPACE's
    server, only until the theme has a placeholder). One line per kind of page at the level (JL 261105: "for the
    /haipipe-labeling, we might have the task for the item, for the labeling, for the embedding, they are all the task,
    but different UI"): several show as side tabs, the kind on the left and the page live on the right."""
    refs = [refs] if isinstance(refs, str) else list(refs)
    key = next((key for key, label in UI_VIEWS if label == name), "")
    types_file = folder / "ui" / "example-types.json" if folder else None
    types = {}
    if types_file and inside(types_file, root) and types_file.is_file():
        try:
            config = json.loads(types_file.read_text(encoding="utf-8"))
            types = config.get(key, {}) if isinstance(config, dict) else {}
            types = types if isinstance(types, dict) else {}
        except (OSError, ValueError):
            pass
    shown, missing, tabs = [], [], []
    for ref in refs:
        page = ui_base(ref, folder or root, root)
        if re.match(r"(?i)^https?://", ref):
            shown.append((ref.rstrip("/").rsplit("/", 1)[-1] or ref, "another server", ref, None))
        elif page is not None:
            href = frame.ROUTE + "?" + urlencode({"path": page.relative_to(root.resolve()).as_posix(), "layout": "focus"})
            shown.append((page.name, ui_kind(page), href, page))
        else:
            missing.append(ref)
            continue
        label = types.get(ref)
        tabs.append((label.strip(), "") if isinstance(label, str) and label.strip()
                    else (shown[-1][0], shown[-1][1]))
    if not shown:
        return "".join(f'<p class="mut">{frame.esc(name)}: <code>{frame.esc(r)}</code> is not a page here.</p>' for r in missing)

    def live(title, href):
        if re.match(r"(?i)^https?://", href):    # another server's page: a frame it cannot reach is a blank box (JL
            return (f'<p class="mut">{frame.esc(title)} lives on another server, so it cannot show here. '   # 261106)
                    f'Its theme needs a placeholder inside Tools.</p><div class="focus-actions"><a class="row-verb" '
                    f'href="{frame.esc(href)}" target="_blank" rel="noopener">Try {frame.esc(title)} there ↗</a></div>')
        return (f'<iframe class="ui-page" title="{frame.esc(name)} · {frame.esc(title)}" data-src="{frame.esc(href)}"></iframe>'
                f'<div class="focus-actions"><a class="row-verb" href="{frame.esc(href)}" target="_blank" rel="noopener">'
                f'Open {frame.esc(title)} ↗</a></div>')

    def player(title, w):
        src = frame._file_url(w, root)
        return (f'<iframe class="ui-page" title="{frame.esc(title)} · the walk" data-src="{frame.esc(src)}" style="height:640px"></iframe>'
                f'<div class="focus-actions"><a class="row-verb" href="{frame.esc(src)}" target="_blank" rel="noopener">'
                f'Open the walk ↗</a></div>')

    walks = [(t, kind, ui_walk_path(walk, p, k, root)) for k, (t, kind, _, p) in enumerate(shown)]
    # the example page fills the frame: its own 960px column and side rail go (JL 261115: "is this not wide enough?")
    wide = ("<script>(function(){function fit(f){try{var d=f.contentDocument;if(!d||d.getElementById('ui-wide'))return;"
            "var s=d.createElement('style');s.id='ui-wide';s.textContent='.focus-page{max-width:none!important;"
            "padding:12px 18px 24px!important}.focus-rail{display:none!important}';(d.head||d.documentElement).appendChild(s);}"
            "catch(e){}}document.querySelectorAll('iframe.ui-page').forEach(function(f){f.addEventListener('load',"
            "function(){fit(f);});fit(f);});})();</script>")
    live_tabs = PB_CSS + _side_tabs(f"fU{name[:1]}x", tabs, [live(t, h) for t, _, h, _ in shown]) + PB_JS + wide
    secs = [("🖥️ The page, live" if len(shown) == 1 else "🖥️ The pages, live", "", live_tabs)]
    if walk is not None:
        secs.append(("🎬 Walkthroughs", "", PB_CSS + _side_tabs(
            f"fW{name[:1]}x", tabs,
            [player(t, w) if w is not None else '<p class="mut">Not recorded</p>'
             for t, _, w in walks]) + PB_JS))
    # Optional authored comparison, owned by this blueprint rather than the shared renderer.
    matrix = folder / "ui" / f"{key}-views.md" if folder and key else None
    if matrix is not None and inside(matrix, root) and matrix.is_file():
        body = ('<style>.ui-type-views{max-width:100%;overflow-x:auto}'
                '.ui-type-views table{display:table;overflow:visible;width:100%;table-layout:auto;border-collapse:separate;border-spacing:0}'
                # Reserve real column tracks: an oversized sticky cell must not cover the first type.
                '.ui-type-views table.ui-turned{--ui-view-width:130px;--ui-type-width:180px;table-layout:fixed;max-width:none;'
                'min-width:calc(var(--ui-view-width) + var(--ui-type-count)*var(--ui-type-width))}'
                '.ui-type-views .ui-view-column{width:var(--ui-view-width)}'
                # one row the same under every view spans them once, its sections in a line (JL 261108: the table fits)
                '.ui-type-views td.ui-span br{display:none}.ui-type-views td.ui-span .matrix-section{margin:0 18px 0 0}'
                '.ui-type-views .matrix-section{white-space:normal;text-align:left}'
                '.ui-type-views th,.ui-type-views td{padding:12px 10px;text-align:left;vertical-align:top;'
                'border-bottom:1px solid var(--border,#e5e7eb);overflow-wrap:break-word;white-space:normal;line-height:1.9;box-sizing:border-box}'
                '.ui-type-views th.ui-view{font-weight:600;position:sticky;left:0;background:var(--paper,#fff);z-index:1}'
                '.ui-type-views th.ui-category{font-size:12.5px;font-weight:500;color:var(--muted,#6b7280);border-bottom:0;padding-bottom:0}'
                '.ui-type-views th.ui-block-type{font-size:15px}.ui-type-views tr.ui-every td,.ui-type-views tr.ui-every th{border-bottom:0}'
                '@media(max-width:600px){.ui-type-views table{min-width:620px}.ui-type-views th,.ui-type-views td{padding:8px;font-size:13px}'
                '.ui-type-views table.ui-turned{--ui-view-width:96px;--ui-type-width:168px}'
                '.ui-type-views th.ui-view{min-width:0;white-space:normal}}'
                '</style><div class="ui-type-views" tabindex="0" role="region" aria-label="Type and view comparison">'
                + ui_matrix_html(matrix, root) + '</div>')
        secs.insert(0, (f"📋 {name.removesuffix(' UI')} Type × View Button", "Draft", body))
    preview = folder / 'ui' / f'{key}-preview.html' if folder and key else None
    if preview and inside(preview, root) and preview.is_file():
        secs.insert(0, ('🖥️ Proposed UI', 'Proposed', live('Proposed ' + name, frame._file_url(preview, root))))
    proposal = folder / 'ui' / 'structure.md' if folder else None
    if proposal and inside(proposal, root) and proposal.is_file():
        guide = matrix_help.guide_for(proposal, root)
        secs.insert(0, ('🧭 Work Structure', 'Proposed' if guide.get('proposed', True) else 'Current', ui_structure_html(proposal, root)))
    return ui_sections(secs) + "".join(f'<p class="mut"><code>{frame.esc(r)}</code> is not a page here.</p>' for r in missing)


def ui_sections(secs: list) -> str:
    """A theme Block's Block UI · Job UI · Task UI view as numbered sections like every view (JL 261105: "why not make
    this to be a section as well?"): 1 · 🖥️ the page, live, 2 · 🎬 the walk (haipipe-ui walk_player.py: "a very quick
    video and we can pause in the middle"), then 🙋 Interaction, last as everywhere. Each starts closed; a frame loads
    when its section opens and its side tab shows."""
    return (BAND_CSS + "".join(band_sec(n, title, word if word in ('Proposed', 'on another server') else "", body, cls="ui-sec") for n, (title, word, body) in enumerate(secs, 1))
        + "<script>document.querySelectorAll('details.ui-sec').forEach(function(d){function load(){if(!d.open)return;"
          "d.querySelectorAll('iframe[data-src]:not([src])').forEach(function(f){var p=f.closest('.pb-panel');"
          "if(!p||!p.hidden)f.src=f.dataset.src;});}d.addEventListener('toggle',load);"
          "d.addEventListener('click',function(){setTimeout(load);});});"
          # picking a kind in one section picks it in the other (the pages and their walks keep one order)
          "(function(){var busy=false;document.addEventListener('click',function(e){if(busy)return;"
          "var it=e.target.closest('details.ui-sec .pb-list > *');if(!it)return;var list=it.parentNode,"
          "k=Array.prototype.indexOf.call(list.children,it);busy=true;"
          "document.querySelectorAll('details.ui-sec .pb-list').forEach(function(l){if(l!==list&&l.children[k]&&"
          "l.children.length===list.children.length)l.children[k].click();});busy=false;});})();</script>")


def home_section(data: dict, theme: str) -> str:
    """The section a page opens on. Outside the paper theme the intro carries the goal, so the page opens
    on Goal & status (an explicit `home-section: goal` means the same)."""
    if data["home"] == "overview-report":
        return "overview-report"
    if data["home"] == "takeaways" or (data["home"] == "goal" and theme == "paper"):
        return data["home"]
    if data["home"] == "goal":
        return "status"
    if theme == "paper":
        return "takeaways"
    if theme in WORK_SHAPE:
        return "status"
    return "takeaways" if data["takeaways"] else "status"


def ui_todo(folder: Path, root: Path, key: str, li) -> list:
    """Latest review for each UI example; recording work belongs in Checklist."""
    pages = [p for p in (ui_base(r, folder, root) for r in read_face(folder, root)["ui"].get(key, [])) if p is not None]
    reviews = sorted(folder.rglob("review/*-s2-r*.md"),           # by round, so r02 is newer than r01 whatever
                     key=lambda p: (int((re.search(r"-s2-r(\d+)", p.name) or [0, 0])[1]), p.name))   # the file's name
    rounds = []
    for k, page in enumerate(pages):
        tail = page.relative_to(root.resolve()).as_posix().split("blueprints/", 1)[-1]
        said = ""
        for rv in reviews:                       # newest round last in name order (r01, r02, …)
            text = rv.read_text(encoding="utf-8", errors="ignore")
            line = next((ln for ln in text.splitlines() if ln.startswith("page")), "")
            if re.search(re.escape(tail) + r"(?=[&\s)]|$)", line):
                m = re.search(r"score\s+mean\s+([\d.]+)/10\s*·\s*(pass|not yet)", text)
                said = (f"{m.group(1)} of 10 · {m.group(2)}" if m else "reviewed") + f" · {rv.stem}", rv
        if said:
            rounds.append(f'<li>{frame.pop(frame.reader(said[1], root), page.name + " · review", page.name)}'
                          f'<small>{frame.esc(ui_kind(page))} · {frame.esc(said[0])}</small></li>')
        else:
            rounds.append(li(page.name, page_url(page, root), page.name, f"{ui_kind(page)} · not reviewed yet"))
    out = []
    if rounds:
        passed = sum("· pass ·" in r for r in rounds)
        reviewed = sum("not reviewed yet" not in r for r in rounds)
        word = (("passes" if passed == len(rounds) else "partly passes" if passed else "does not pass yet")
                if reviewed else "not reviewed yet")              # no tally (JL 261113); each round shows its own
        out.append(("🔍 Review rounds", word, '<ul class=wk-rows>' + "".join(rounds) + '</ul>', ""))
    return out
