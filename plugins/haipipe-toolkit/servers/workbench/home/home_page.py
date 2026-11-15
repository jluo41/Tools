"""The SPACE Home page itself: render_home draws every Project, its Themes and their Block rows,
with the kind filter, the search box and the Chart, as one self-contained HTML page."""

from __future__ import annotations

import html
from pathlib import Path
from urllib.parse import quote

from live.home_boards import (FOLD_OPEN_MAX, HOME_BRAND, KIND_ICON, KIND_THEME, discover_boards,
                              home_section, kind_query, kind_sort_key, parse_kinds, project_matches,
                              theme_sort_key)
from live.home_rows import _home_row, _runs_of, block_link


def render_home(root: Path, space_name: str = "", public_url: str = "",
                kind: str = "", project: str = "", archived: bool = False) -> str:
    """Render the Space view: every Project, its Themes, and their Block cards.

    Home offers a live hierarchy chart and an entry list. Only Boards that can be
    opened (a declared workbench, or Pages the live reader shows) are listed, so
    every card is actionable.  Inside a Project the cards group by Theme, the
    Project-root folder they sit in, in the order ``THEMES`` gives.  ``kind``
    (``?kind=task`` or ``?kind=task,paper``) filters by block type; the same
    filter runs in the browser and is written back to the address bar, so a
    link reproduces the view.  ``project`` (``?project=examples/Project-A``, or
    the folder name, or the project.yaml id) shows that one Project alone, with
    a link back to every Project; a name that matches none shows them all and
    says so (``/wb <Project>`` opens this view).  Projects start open when the
    view holds at most ``FOLD_OPEN_MAX`` of them.  Collapse choices and Project order are
    browser-local preferences, never source files or a second registry.  The
    card shows folder names, titles, kinds, the Board's state word and counts;
    never a Result value.
    """
    cards = discover_boards(root, include_page_state=False, include_linked=True)
    scoped = [card for card in cards if project_matches(card, project)] if project else []
    if scoped:
        cards = scoped
    rest = ("project=" + quote(str(scoped[0]["project_path"] if scoped[0].get("project_scope") == "project"
                                   else scoped[0]["project_key"]), safe="/:") if scoped else "")
    open_cards = [card for card in cards if card["ready"] or card.get("workbench_ready")]
    slug_counts: dict[str, int] = {}
    for card in cards:   # the same match board_by_slug makes: a slug or a full folder name
        if card.get("linked_space"):
            continue
        for key in {str(card["slug"]), str(card["name"]).lower()}:
            slug_counts[key] = slug_counts.get(key, 0) + 1

    from live.space_chart import block_nodes, chart_data, chart_parts
    chart = chart_data(root, open_cards, space_name.strip() or HOME_BRAND)
    nodes = block_nodes(chart["tree"])     # each Block's topics and Jobs, the same in the chart and the list
    present = sorted({str(card["kind_key"]) for card in open_cards}, key=kind_sort_key)
    kinds = [k for k in parse_kinds(kind) if k in present]
    selected = set(kinds)

    def listed(card):        # a legacy copy only with `?archived=1`, as the Chart's "Include legacy Blocks"
        return archived or not card.get("archived")

    def shown(card):
        return listed(card) and (not selected or card["kind_key"] in selected)

    section_groups: dict[str, dict[str, list[dict[str, object]]]] = {}
    for card in open_cards:
        section = home_section(card)
        projects = section_groups.setdefault(section, {})
        projects.setdefault(str(card["project_key"]), []).append(card)
    visible_projects = sum(any(shown(card) for card in group)
                           for projects in section_groups.values()
                           for group in projects.values())
    open_default = visible_projects <= FOLD_OPEN_MAX

    groups = []
    project_index = 0
    ordered_sections = sorted(
        section_groups,
        key=lambda section: (0 if section.lower() == "examples" else 1,
                             section.lower()),
    )
    hide_implicit_space = (
        len(ordered_sections) == 1
        and ordered_sections[0] == "SPACE"
        and open_cards
        and all(card.get("project_scope") == "project" for card in open_cards)
    )
    for section in ordered_sections:
        project_groups = section_groups[section]
        project_rows = []
        section_label = html.escape(section, quote=True)
        section_shown = False
        for project_key, group_cards in project_groups.items():
            project_name = str(group_cards[0]["project"])
            project_label = html.escape(project_name, quote=True)
            project_key_attr = html.escape(project_key, quote=True)
            group_search = html.escape(
                " ".join((project_name, str(group_cards[0]["project_path"]))),
                quote=True,
            )
            themes: dict[str, list[dict[str, object]]] = {}
            for card in group_cards:
                label = str(card["theme"] or KIND_THEME.get(str(card["kind_key"]),
                                                            str(card["kind_key"])))
                themes.setdefault(label, []).append(card)
            theme_html = []
            project_count = 0
            project_runs: list = []
            for theme in sorted(themes, key=theme_sort_key):
                theme_cards = sorted(themes[theme], key=lambda c: (
                    "/_" in "/" + str(c["path"]), str(c["path"]).lower()))
                count = sum(shown(card) for card in theme_cards)
                project_count += count
                block_runs = {str(c["path"]): _runs_of(root / str(c["path"])) for c in theme_cards}
                project_runs.extend(r for c in theme_cards if shown(c) for r in block_runs[str(c["path"])])
                rows = "".join(_home_row(card, project_name,
                                         block_link(card, slug_counts), shown(card),
                                         nodes.get(str(card["path"])), block_runs[str(card["path"])])
                               for card in theme_cards)
                theme_attr = html.escape(theme, quote=True)
                hidden = "" if count else " hidden"
                theme_html.append(
                    f'''<section class="theme-group" data-theme="{theme_attr}" aria-label="{theme_attr}"{hidden}>
  <h3 class="theme-heading"><span class="theme-name">{html.escape(theme)}</span></h3>
  <div class="theme-list" role="list">{rows}</div></section>''')
            group_id = f"project-list-{project_index}"
            project_index += 1
            section_shown = section_shown or bool(project_count)
            fold = " open" if open_default else ""
            hidden = "" if project_count else " hidden"
            project_rows.append(
                f'''<details class="project-group" data-project-key="{project_key_attr}"
  data-search="{group_search}" role="listitem"{hidden}{fold}><summary class="project-summary"
  aria-controls="{group_id}"><span class="project-grip"
  role="img" aria-label="Drag to reorder {project_label}" title="Drag to reorder">⠿</span>
  <span class="project-name">{project_label}</span>
</summary>
  <div id="{group_id}" class="project-list" aria-label="{project_label} blocks">
  {''.join(theme_html)}</div></details>''')
        section_id = f"space-title-{len(groups)}"
        hide_heading = hide_implicit_space and section == "SPACE"
        section_heading = "" if hide_heading else (
            f'<h2 class="space-heading" id="{section_id}">{section_label}</h2>')
        section_accessibility = ('aria-label="Boards"' if hide_heading else
                                 f'aria-labelledby="{section_id}"')
        groups.append(
            f'''<section class="space-section" data-space-key="{section_label}"
  data-search="{section_label}" {section_accessibility}{"" if section_shown else " hidden"}>
  {section_heading}
  <div class="space-projects" role="list" aria-label="{section_label} projects">
  {''.join(project_rows)}</div></section>''')
    if groups:
        body = "\n".join(groups)
    elif cards:
        body = '<p class="empty">No boards are ready to open.</p>'
    else:
        body = '<p class="empty">No boards found below this SPACE root.</p>'

    # The block-type toggles: `all` plus each kind present.  Each href is the view
    # that clicking it gives, so the bar works without script too.
    toggles = []
    if present:
        toggles.append(
            f'<a class="kind-toggle" role="button" href="{html.escape(kind_query((), rest), quote=True)}" data-kind="all" '
            f'aria-pressed="{"false" if selected else "true"}">all</a>')
        for key in present:
            after = selected ^ {key}
            count = sum(card["kind_key"] == key and listed(card) for card in open_cards)
            toggles.append(
                f'<a class="kind-toggle" role="button" href="{html.escape(kind_query(after, rest), quote=True)}" '
                f'data-kind="{html.escape(key, quote=True)}" '
                f'aria-pressed="{"true" if key in selected else "false"}">'
                f'<span aria-hidden="true">{KIND_ICON.get(key, "")}</span> {html.escape(key)} '
                f'<span class="kind-count">{count}</span></a>')
    kind_bar = (f'<nav class="kind-filter" aria-label="Block type">{"".join(toggles)}</nav>'
                if toggles else "")
    any_shown = any(shown(card) for card in open_cards)
    heading = html.escape(space_name.strip() or HOME_BRAND)
    title = heading
    scope_line = ""
    if scoped:
        name = html.escape(str(scoped[0]["project"]))
        title = f"{name} · {heading}"
        scope_line = (f'<p class="home-scope">Project <b>{name}</b> · '
                      f'<a href="{html.escape(kind_query(kinds), quote=True)}">all Projects</a></p>')
    elif project:
        scope_line = (f'<p class="home-scope">No Project matches “{html.escape(project)}”; '
                      'showing every Project.</p>')
    chart_markup, chart_css, chart_js = chart_parts(root, open_cards, space_name.strip() or HOME_BRAND, chart)
    try:                                           # the Runs cards' look, shared with the Studio's Runs part
        from live import frame as _frame
        run_css = _frame.RUN_CSS
    except ImportError:
        run_css = ""
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title><style>
:root{{color-scheme:light;--bg:#ffffff;--fg:#1c1c1c;--mut:#7c7c78;--line:#e4e4e7;--card:#f7f7f8;--accent:#1f5aa8;--focus:#075fbd;--radius-control:7px;--radius-surface:10px}}
@media(prefers-color-scheme:dark){{:root{{--bg:#161719;--fg:#e8e8e6;--mut:#9a9a97;--line:#2c2e33;--card:#1d1f23;--accent:#6ea8f0;--focus:#9dc8ff}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.7 -apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif}}
:where(a,input):focus-visible{{outline:3px solid var(--focus);outline-offset:3px;border-radius:var(--radius-control)}}
main{{max-width:none;margin:0;padding:34px clamp(14px,2.5vw,32px) 90px}}
.site-head{{margin:0 0 22px}}h1{{font-size:26px;line-height:1.35;margin:0;font-weight:700}}
.toolbar{{margin:0 0 12px}}.search{{display:block;max-width:420px}}.search input{{width:100%;min-height:38px;border:1px solid var(--line);border-radius:var(--radius-control);background:var(--card);color:var(--fg);font:inherit;padding:5px 9px;outline:none}}.search input::placeholder{{color:var(--mut)}}.search input:focus{{border-color:var(--accent)}}
.kind-filter{{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 0}}.kind-toggle{{display:inline-flex;align-items:center;gap:4px;min-height:30px;padding:2px 10px;border:1px solid var(--line);border-radius:999px;background:var(--card);color:var(--fg);font-size:14px;text-decoration:none}}.kind-toggle:hover{{border-color:var(--accent)}}.kind-toggle[aria-pressed="true"]{{border-color:var(--accent);background:var(--accent);color:var(--bg)}}.kind-count{{color:inherit;opacity:.7;font:12px/1 ui-monospace,Menlo,monospace}}
.board-list{{min-width:0}}.space-section{{margin:26px 0 0}}.space-heading{{margin:0;padding:0 0 7px;border-bottom:2px solid var(--fg);font-size:12px;line-height:1.4;letter-spacing:.15em;text-transform:uppercase;color:var(--mut)}}.space-projects{{min-width:0}}.project-group{{margin:17px 0 0;min-width:0}}.project-summary{{display:flex;align-items:center;gap:7px;min-height:34px;padding:0 0 7px;border-bottom:1px solid var(--line);list-style:none;cursor:pointer;color:var(--fg);font-size:16px;font-weight:700}}.project-summary::-webkit-details-marker{{display:none}}.project-summary::before{{content:"▸";width:11px;color:var(--accent);font-size:11px;line-height:1}}.project-group[open]>.project-summary::before{{content:"▾"}}.project-grip{{color:var(--mut);font:14px/1 ui-monospace,Menlo,monospace;cursor:grab;user-select:none;touch-action:none;opacity:.72}}.project-grip:active{{cursor:grabbing}}.project-name{{min-width:0;overflow-wrap:anywhere}}.project-list{{min-width:0;padding-top:2px}}.theme-group{{margin:10px 0 0 18px}}.theme-heading{{display:flex;align-items:baseline;gap:7px;margin:0;font-size:12px;line-height:1.5;letter-spacing:.08em;text-transform:lowercase;color:var(--mut);font-weight:600}}.theme-name::before{{content:"– "}}.project-group.dragging{{opacity:.55}}.project-group.drag-over>.project-summary{{border-color:var(--accent)}}.ir{{position:relative;display:flex;gap:10px;align-items:baseline;padding:9px 13px;border:1px solid var(--line);border-radius:var(--radius-surface);margin:6px 0;text-decoration:none;color:var(--fg);background:var(--card);overflow:hidden}}.ir:hover{{border-color:var(--accent)}}.home-kind{{flex:none;font-size:15px;line-height:1}}.home-copy{{display:flex;flex:1 1 220px;min-width:min(220px,100%);flex-direction:column;gap:1px}}
/* a narrow window wraps the Run counts under the title instead of squeezing the title to one letter a line (JL 261022) */
.home-row{{flex-wrap:wrap;row-gap:4px}}.ir .t{{min-width:0;overflow-wrap:anywhere;font-weight:600}}.home-folder{{min-width:0;color:var(--mut);font:12px/1.55 ui-monospace,Menlo,monospace;overflow-wrap:anywhere;word-break:break-word}}.home-state{{flex:none;color:var(--mut);font:12px/1.4 ui-monospace,Menlo,monospace;white-space:nowrap}}.empty,.no-results{{color:var(--mut);padding:14px 0}}.home-block{{margin:6px 0;min-width:0}}.home-block>.ir{{margin:0;cursor:pointer;list-style:none;align-items:center}}.home-block>.ir::-webkit-details-marker{{display:none}}.home-block>.ir::before{{content:"▸";flex:none;width:12px;color:var(--accent);font-size:15px;line-height:1}}.home-block[open]>.ir::before{{content:"▾"}}.home-block[open]>.ir{{border-radius:var(--radius-surface) var(--radius-surface) 0 0}}.ir a.t{{align-self:flex-start;color:var(--fg);text-decoration:none}}.ir a.t:hover{{color:var(--accent);text-decoration:underline}}.block-groups{{display:grid;gap:10px;padding:10px 12px 12px 26px;border:1px solid var(--line);border-top:0;border-radius:0 0 var(--radius-surface) var(--radius-surface)}}.block-cards-head{{margin:0 0 4px;font-size:12px;line-height:1.5;letter-spacing:.06em;color:var(--mut);font-weight:600}}.block-cards-empty{{margin:0;color:var(--mut);font-size:13px}}
.topic-rows .topic{{border:1px solid var(--line);border-radius:10px;background:var(--bg);margin:0 0 6px;overflow:hidden}}.topic-rows .topic>summary{{display:flex;flex-wrap:wrap;gap:6px 10px;align-items:baseline;cursor:pointer;padding:8px 12px;list-style:none}}.topic-rows .topic>summary::-webkit-details-marker{{display:none}}.topic-rows .topic>summary::before{{content:"▸";color:var(--mut)}}.topic-rows .topic[open]>summary::before{{content:"▾"}}.topic-rows .topic[open]>summary{{border-bottom:1px solid var(--line)}}.topic-rows .topic>summary>b{{font-size:15px;overflow-wrap:anywhere}}.topic-tags{{display:inline-flex;gap:6px;flex-wrap:wrap}}.topic-tags .chip{{display:inline-block;padding:0 8px;border:1px solid var(--line);border-radius:999px;color:var(--mut);font-size:12px}}.topic-pop{{margin-left:auto}}.topic-pop a{{color:var(--accent);text-decoration:none;font-size:15px}}.topic-none{{margin:8px 12px;color:var(--mut);font-size:13px}}.st-frame{{display:block;width:100%;height:520px;border:0;background:#fff}}.job-frame{{height:440px;border-top:1px solid var(--line)}}.topic-rows .topic-meta{{color:var(--mut);font-size:13px;overflow-wrap:anywhere}}.job-runs .rn-task{{flex-wrap:wrap}}.job-runs .rn-task a{{color:var(--fg);text-decoration:none}}.job-runs .rn-task a:hover{{color:var(--accent)}}.job-runs .rn-task .job-st{{align-self:center}}.job-st{{display:inline-block;padding:0 9px;border:1px solid var(--mut);border-radius:999px;color:var(--mut);font-size:12px;font-weight:600;white-space:nowrap}}.job-st-active{{color:#2b8a3e;border-color:#2b8a3e}}.job-st-open{{color:#1971c2;border-color:#1971c2}}.job-st-done{{color:#495057;border-color:#495057}}.job-st-blocked{{color:#e03131;border-color:#e03131}}
.stage{{--st:#868e96;--st-bg:#f1f3f5;display:inline-flex;align-items:center;gap:6px;font-size:12px;font-weight:600;letter-spacing:.02em;padding:2px 10px 2px 8px;border:1px solid var(--st);border-radius:999px;white-space:nowrap;color:var(--st);background:var(--st-bg)}}.stage-explore{{--st:#2b8a3e;--st-bg:#ebfbee}}.stage-shaping{{--st:#7048e8;--st-bg:#f3f0ff}}.stage-agreed{{--st:#1971c2;--st-bg:#e7f5ff}}.stage-closed{{--st:#495057;--st-bg:#f1f3f5}}@media(prefers-color-scheme:dark){{.stage{{--st-bg:transparent}}.stage-explore{{--st:#8ce99a}}.stage-shaping{{--st:#b197fc}}.stage-agreed{{--st:#74c0fc}}.stage-closed{{--st:#adb5bd}}}}.stage-steps{{display:inline-flex;gap:2px}}.stage-steps b{{width:7px;height:7px;border-radius:2px;border:1px solid var(--st);opacity:.55}}.stage-steps b.on{{background:var(--st);opacity:1}}.stage-none{{color:var(--mut);border-style:dashed;font-weight:400}}
.home-scope{{margin:4px 0 0;color:var(--mut);font-size:14px}}.home-scope b{{color:var(--fg)}}.home-scope a{{color:var(--accent)}}[hidden]{{display:none!important}}.sr-only{{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}}
@media (max-width:680px){{.home-state{{white-space:normal}}main{{padding:28px 14px 62px}}.site-head{{margin-bottom:18px}}h1{{font-size:24px}}.search input{{min-height:40px}}.ir{{padding:9px 12px}}.project-summary{{gap:5px;flex-wrap:wrap}}.theme-group{{margin-left:8px}}.block-groups{{padding-left:12px}}}}
{chart_css}{run_css}
</style></head><body><main><header class="site-head"><h1>{heading}</h1>{scope_line}</header>
<div class="toolbar"><label class="search"><span class="sr-only">Search boards</span><input id="board-filter" type="search" placeholder="Search boards" aria-label="Search boards" autocomplete="off"></label>{kind_bar}</div>
{chart_markup}
<div id="board-list" class="board-list project-groups" role="list" aria-label="Projects">{body}</div><p id="no-results" class="no-results"{" hidden" if (any_shown or not open_cards) else ""}>No matching boards.</p></main><script>
const filter = document.getElementById('board-filter');
const noResults = document.getElementById('no-results');
const groups = Array.from(document.querySelectorAll('.project-group'));
const projectLists = Array.from(document.querySelectorAll('.space-projects'));
const kindToggles = Array.from(document.querySelectorAll('.kind-toggle'));
const FOLD_OPEN_MAX = {FOLD_OPEN_MAX};
const KIND_ORDER = kindToggles.map((toggle) => toggle.dataset.kind).filter((k) => k !== 'all');
const storagePrefix = 'fusion-space:home:' + location.origin + location.pathname;
const orderStorageKey = storagePrefix + ':project-order';
// v3 keeps only the folds a person chose ({{key: open}}); every other Project
// follows the default: open when the view holds at most FOLD_OPEN_MAX Projects.
const collapsedStorageKey = storagePrefix + ':project-collapsed:v3';
let selectedKinds = new Set(kindToggles
  .filter((toggle) => toggle.dataset.kind !== 'all' && toggle.getAttribute('aria-pressed') === 'true')
  .map((toggle) => toggle.dataset.kind));
// legacy Blocks follow the Chart's "Include legacy Blocks" box, so both views count the same Blocks
let includeLegacy = {"true" if archived else "false"};

function readStorage(key, fallback) {{
  try {{
    const value = JSON.parse(window.localStorage.getItem(key) || 'null');
    return value === null ? fallback : value;
  }} catch (error) {{
    return fallback;
  }}
}}
function writeStorage(key, value) {{
  try {{ window.localStorage.setItem(key, JSON.stringify(value)); }}
  catch (error) {{ /* private browsing or a restricted origin */ }}
}}
function currentGroups() {{
  return Array.from(document.querySelectorAll('.project-group'));
}}
function saveOrder() {{
  writeStorage(orderStorageKey, currentGroups().map((group) => group.dataset.projectKey));
}}
function restoreOrder() {{
  const saved = readStorage(orderStorageKey, []);
  if (!Array.isArray(saved)) return;
  const order = new Map(saved.map((key, index) => [String(key), index]));
  projectLists.forEach((projectList) => {{
    const ordered = Array.from(projectList.children)
      .filter((child) => child.classList.contains('project-group'))
      .sort((left, right) =>
        (order.get(left.dataset.projectKey) ?? Number.MAX_SAFE_INTEGER) -
        (order.get(right.dataset.projectKey) ?? Number.MAX_SAFE_INTEGER));
    ordered.forEach((group) => projectList.appendChild(group));
  }});
}}
function foldChoices() {{
  const saved = readStorage(collapsedStorageKey, {{}});
  return saved && typeof saved === 'object' && !Array.isArray(saved) ? saved : {{}};
}}
function saveCollapsed(group) {{
  const choices = foldChoices();
  choices[group.dataset.projectKey] = group.open;
  writeStorage(collapsedStorageKey, choices);
}}
function restoreCollapsed() {{
  const choices = foldChoices();
  const visible = groups.filter((group) => !group.hidden).length;
  groups.forEach((group) => {{
    const key = group.dataset.projectKey;
    group.open = Object.prototype.hasOwnProperty.call(choices, key)
      ? Boolean(choices[key]) : visible <= FOLD_OPEN_MAX;
  }});
}}
function projectAtPoint(x, y) {{
  const node = document.elementFromPoint(x, y);
  return node ? node.closest('.project-group') : null;
}}
function placeGroup(group, target, clientY) {{
  if (!group || !target || group === target) return false;
  const projectList = group.parentElement;
  if (!projectList || target.parentElement !== projectList) return false;
  const rect = target.getBoundingClientRect();
  if (clientY < rect.top + rect.height / 2) projectList.insertBefore(group, target);
  else {{
    const reference = target.nextElementSibling;
    if (reference === group) return false;
    if (reference) projectList.insertBefore(group, reference);
    else projectList.appendChild(group);
  }}
  return true;
}}
let draggedGroup = null;
let pointerGroup = null;
let pointerId = null;
let pointerStartX = 0;
let pointerStartY = 0;
let pointerMoved = false;
function clearDragState() {{
  if (draggedGroup) draggedGroup.classList.remove('dragging');
  groups.forEach((group) => group.classList.remove('drag-over'));
  draggedGroup = null;
  pointerGroup = null;
  pointerId = null;
  pointerMoved = false;
}}
groups.forEach((group) => {{
  // Only a person's click on the fold is remembered; a fold the page opens
  // itself (a search hit, the default) is not a choice.
  const summary = group.querySelector('.project-summary');
  summary.addEventListener('click', () => {{ group.dataset.userToggle = '1'; }});
  group.addEventListener('toggle', () => {{
    if (group.dataset.userToggle !== '1') return;
    delete group.dataset.userToggle;
    saveCollapsed(group);
  }});
  const grip = group.querySelector('.project-grip');
  grip.addEventListener('click', (event) => {{
    event.preventDefault();
    event.stopPropagation();
  }});
  grip.addEventListener('pointerdown', (event) => {{
    pointerGroup = group;
    pointerId = event.pointerId;
    pointerStartX = event.clientX;
    pointerStartY = event.clientY;
    pointerMoved = false;
    draggedGroup = group;
    if (grip.setPointerCapture) grip.setPointerCapture(event.pointerId);
    event.preventDefault();
  }});
  grip.addEventListener('pointermove', (event) => {{
    if (pointerGroup !== group || pointerId !== event.pointerId) return;
    const distance = Math.hypot(event.clientX - pointerStartX,
                                event.clientY - pointerStartY);
    if (!pointerMoved && distance < 8) return;
    pointerMoved = true;
    draggedGroup = group;
    group.classList.add('dragging');
    event.preventDefault();
    groups.forEach((candidate) => candidate.classList.remove('drag-over'));
    const target = projectAtPoint(event.clientX, event.clientY);
    if (target && target !== group) target.classList.add('drag-over');
  }});
  const finishPointerDrag = (event) => {{
    if (pointerGroup !== group || pointerId !== event.pointerId) return;
    if (pointerMoved) {{
      event.preventDefault();
      const target = projectAtPoint(event.clientX, event.clientY);
      if (placeGroup(group, target, event.clientY)) saveOrder();
    }}
    if (grip.hasPointerCapture && grip.hasPointerCapture(event.pointerId))
      grip.releasePointerCapture(event.pointerId);
    clearDragState();
  }};
  grip.addEventListener('pointerup', finishPointerDrag);
  grip.addEventListener('pointercancel', finishPointerDrag);
}});
restoreOrder();
restoreCollapsed();
// A Block card folds over its two groups, Studio topics and Jobs; it starts closed, and only the
// folds a person opens are remembered ({{block path: true}}).
const blockStorageKey = storagePrefix + ':block-open:v1';
const blocks = Array.from(document.querySelectorAll('.home-block'));
function blockChoices() {{
  const saved = readStorage(blockStorageKey, {{}});
  return saved && typeof saved === 'object' && !Array.isArray(saved) ? saved : {{}};
}}
function restoreBlocks() {{
  const choices = blockChoices();
  blocks.forEach((block) => {{ block.open = Boolean(choices[block.dataset.blockKey]); }});
}}
blocks.forEach((block) => {{
  const summary = block.querySelector(':scope > summary');
  summary.addEventListener('click', (event) => {{
    if (!event.target.closest('a')) block.dataset.userToggle = '1';   // the title link opens the Block
  }});
  block.addEventListener('toggle', () => {{
    if (block.dataset.userToggle !== '1') return;
    delete block.dataset.userToggle;
    const choices = blockChoices();
    if (block.open) choices[block.dataset.blockKey] = true;
    else delete choices[block.dataset.blockKey];
    writeStorage(blockStorageKey, choices);
  }});
}});
restoreBlocks();
// a Studio row loads its drawing, a Job row its face, only when opened, as the workbench's Studio list does
document.querySelectorAll('.topic-rows details.topic').forEach((row) => {{
  row.addEventListener('toggle', () => {{
    const view = row.querySelector('iframe');
    if (row.open && view && !view.getAttribute('src')) view.src = view.dataset.src;
  }});
}});
function kindQuery(kinds) {{
  const ordered = KIND_ORDER.filter((kind) => kinds.has(kind));
  return ordered.length ? '?kind=' + ordered.join(',') : '';
}}
// a kind link keeps every other part of the address (`project=`), as the server writes it
function kindHref(kinds) {{
  const params = new URLSearchParams(location.search);
  params.delete('kind');
  const rest = params.toString();
  const kq = kindQuery(kinds);
  return kq ? kq + (rest ? '&' + rest : '') : (rest ? '?' + rest : '?');
}}
function syncKindToggles() {{
  kindToggles.forEach((toggle) => {{
    const kind = toggle.dataset.kind;
    const pressed = kind === 'all' ? selectedKinds.size === 0 : selectedKinds.has(kind);
    toggle.setAttribute('aria-pressed', pressed ? 'true' : 'false');
    const after = new Set(selectedKinds);
    if (kind !== 'all') {{ if (after.has(kind)) after.delete(kind); else after.add(kind); }}
    toggle.setAttribute('href', kindHref(kind === 'all' ? new Set() : after));
  }});
}}
function applyFilter() {{
  const query = filter.value.trim().toLowerCase();
  let visible = 0;
  groups.forEach((group) => {{
    const groupMatch = !query || group.dataset.search.toLowerCase().includes(query);
    let groupVisible = 0;
    group.querySelectorAll('.theme-group').forEach((theme) => {{
      let themeVisible = 0;
      theme.querySelectorAll('.home-block').forEach((row) => {{
        const kindMatch = selectedKinds.size === 0 || selectedKinds.has(row.dataset.kind);
        const legacyMatch = includeLegacy || row.dataset.archived !== '1';
        const match = legacyMatch && kindMatch && (groupMatch || row.dataset.search.toLowerCase().includes(query));
        row.hidden = !match;
        // a search that hits a topic or a Job opens its Block, so the hit shows
        if (match && query && row.querySelector('.block-groups').textContent.toLowerCase().includes(query)) row.open = true;
        if (match) themeVisible += 1;
      }});
      theme.hidden = themeVisible === 0;
      groupVisible += themeVisible;
    }});
    group.hidden = groupVisible === 0;
    if (query && groupVisible) group.open = true;
    visible += groupVisible;
  }});
  document.querySelectorAll('.space-section').forEach((section) => {{
    section.hidden = !Array.from(section.querySelectorAll('.project-group'))
      .some((group) => !group.hidden);
  }});
  if (!query) restoreBlocks();
  noResults.hidden = visible !== 0 || (!query && selectedKinds.size === 0);
  document.dispatchEvent(new CustomEvent('space-home-filter', {{detail: {{query, kinds: [...selectedKinds]}}}}));
}}
kindToggles.forEach((toggle) => {{
  toggle.addEventListener('click', (event) => {{
    event.preventDefault();
    const kind = toggle.dataset.kind;
    if (kind === 'all') selectedKinds = new Set();
    else if (selectedKinds.has(kind)) selectedKinds.delete(kind);
    else selectedKinds.add(kind);
    syncKindToggles();
    // the address bar carries the view, so a copied link reproduces it
    const search = kindHref(selectedKinds);
    history.replaceState(null, '', location.pathname + (search === '?' ? '' : search) + location.hash);
    applyFilter();
    if (!filter.value.trim()) restoreCollapsed();
  }});
}});
filter.addEventListener('input', applyFilter);
const legacyBox = document.getElementById('chart-archived');
if (legacyBox) legacyBox.addEventListener('change', () => {{ includeLegacy = legacyBox.checked; applyFilter(); }});
</script><script>{chart_js}</script></body></html>'''
