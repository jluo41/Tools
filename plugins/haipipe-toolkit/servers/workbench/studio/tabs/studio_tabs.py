"""Studio read like Main: the page's own topics in sNN order, each a fold (`s06 · 🎨 Files pane`) that opens its Slide,
Draw, Work, Delivery in place."""
import re
from urllib.parse import urlencode, urlsplit

from live import frame
from live.ui_parts import PB_CSS, PB_JS, _side_tabs, open_dot


def topic_label(title):
    """A topic's name on a tab, the same in Studio and Decisions: "work skills: workbench-work" reads "Work skills"."""
    short, separator, rest = title.partition(':')
    label = short if separator and rest.strip()[:1].islower() else title
    return label[:1].upper() + label[1:]


def frame_of(title, name, href, tall=False):
    esc = frame.esc
    from live.folder_folds import Folder, folds
    if isinstance(href, Folder):                     # a folder: one fold per file (JL 261127)
        return folds(title, href)
    if urlsplit(href).path.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg')):
        return open_dot(f'<img src="{esc(href)}" alt="{esc(title)} · {esc(name)}" loading="lazy">',
                        href, name, pop=f'{title} · {name}')
    return open_dot(f'<iframe title="{esc(title)} · {esc(name)}" data-studio-src="{esc(href)}"'
                    + (' style="height:80vh"' if tall else '') + '></iframe>', href, name, pop=f'{title} · {name}')


def page_items(page, root) -> list:
    """[(label, url, earlier)] for each `<button data-src>` a topic's own page offers (s06's Metro map, Marks + card, then
    its Earlier ones), so Studio lists them as left tabs instead of the page's own button row."""
    try:
        text = page.read_text(encoding='utf-8', errors='ignore')
    except OSError:
        return []
    out = []
    for attrs, label in re.findall(r'<button\b([^>]*\bdata-src="[^"]+"[^>]*)>([^<]+)</button>', text):
        src = re.search(r'data-src="([^"]+)"', attrs).group(1)
        earlier = bool(re.search(r'class="[^"]*\bold\b', attrs))
        if src.startswith(frame.ROUTE + '?'):        # a live page the server renders (s07: an example Block), origin-relative
            out.append((label.strip(), src.replace('&amp;', '&'), earlier))
            continue
        target = (page.parent / src).resolve()
        if re.match(r'(?i)^[a-z]+:', src) or not target.is_file():
            continue
        try:
            target.relative_to(root.resolve())
        except ValueError:
            continue
        out.append((label.strip(), frame._file_url(target, root), earlier))
    return out


def topic_emoji(face) -> str:
    """The emoji a topic's face names on its `emoji:` line, so each topic reads apart from its neighbours (JL 261127:
    "for the emojis for each studio, could they be different?"); 🎨 when it names none."""
    try:
        m = re.search(r"(?m)^emoji:\s*(\S+)\s*$", face.read_text(encoding="utf-8", errors="ignore")[:2000])
    except OSError:
        return '🎨'
    return m.group(1) if m else '🎨'


def studio_bands(owner, root=None) -> dict:
    """Blueprints share one ordered band registry; other Blocks use their own bands or tags."""
    from live.focus_jobs import band_names
    from live.studio_types import is_blueprint, studio_types
    if root and is_blueprint(owner):
        return {d: f"{e} {n}".strip() for d, (e, n, _) in studio_types(root).items()}
    face = owner / "board.md" if (owner / "board.md").is_file() else owner / f"{owner.name}.md"
    return band_names(face, "s") if face.is_file() else {}



def render(rows, root, group='', asks=()):
    from live import focus_page as f
    from live.frame_groups import studio_group_order
    items, group_order = [], []
    for topic, drawings, facts in rows:
        if not f.in_group(facts, group) or not f.inside(topic, root):
            continue
        for name in studio_group_order(frame.topic_owner(topic) or topic.parent):
            if name not in group_order:
                group_order.append(name)
        tags = facts.get('tags') or []
        tags = [tags] if isinstance(tags, str) else tags
        named = studio_bands(frame.topic_owner(topic) or topic.parent, root)   # the board's sNN bands win over tags
        decade = re.match(r"s(\d)\d", topic.name)
        band = group or (named.get(decade.group(1)) if named and decade else None) \
            or next((name for name in group_order if name in tags), None) or next(iter(tags), 'Other')
        if named and decade and band in named.values() and band not in group_order:
            group_order[:0] = list(dict.fromkeys(n for _, n in sorted(named.items()) if n not in group_order))
        notes = frame._notes(topic)
        title = f.face_title(notes) if notes and f.inside(notes, root) else ''
        title = title or topic.name.replace('_', ' ')
        mark = topic_emoji(notes) if notes and f.inside(notes, root) else '🎨'
        views = []
        page = topic / (topic.name + '.html')         # a topic may carry its own page (a replay day, a report): shown first
        if page.is_file() and f.inside(page, root):
            views.append(('Page', frame._file_url(page, root), ''))
        deck = topic / (topic.name + '.slides.html')
        if deck.is_file() and f.inside(deck, root):
            views.append(('Slide', frame._file_url(deck, root), ''))
        things = page_items(page, root) if views and views[0][0] == 'Page' else []
        parts = {'Page': things}
        live = [t for t in things if t[1].startswith(frame.ROUTE + '?')]
        quick = [t for t in things if not t[1].startswith(frame.ROUTE + '?')]
        if live and quick:       # a UI preview: Page holds the server's own pages, Effect the quick html in delivery/ui/
            parts = {'Page': live, 'Effect': quick}
            views.insert(1, ('Effect', quick[0][1], ''))
        drawings = [p for p in drawings if p.is_file() and f.inside(p, root)]
        if drawings:
            previews = [drawings[0].with_suffix('.png'), topic / (topic.name + '.png')]
            preview = next((p for p in previews if p.is_file() and f.inside(p, root)), None)
            views.append(('Draw', frame._draw_url(drawings[0], root), frame._file_url(preview, root) if preview else ''))
        # no MindMap view: its .mindmap.md stays in Files (JL 261125: "I think I can delete the mindmap")
        if f.is_topic(topic) and f.work_root(topic) is not None:
            views.append(('Work', frame.ROUTE + '?' + urlencode({'view': 'focus-part', 'part': 'work', 'path': frame.rel(topic, root)}), ''))
        if f.is_topic(topic) and (topic / 'delivery').is_dir():
            views.append(('Delivery', frame.ROUTE + '?' + urlencode({'view': 'focus-delivery', 'path': frame.rel(topic, root)}), ''))
        from live import studio_views
        authored = studio_views.read_views(topic, root)
        if authored is not None:
            views, parts = authored
        from live.studio_types import element_view
        shown = element_view(topic, root)                # a Studio Type topic: its elements live, laid out as an instance
        if shown and authored is None:                   # its own views win: a type is laid out as its instances are
            views = [('Elements', shown[0][1], '')] + [v for v in views if v[0] != 'Elements']
            parts = dict(parts, Elements=shown)
        esc = frame.esc
        goal = f.first_sentence(facts.get('topic', ''))       # the topic's sentence: a hover on its fold, never a line
        goal = '' if goal.lstrip().startswith(('<', '〈')) else goal  # a template's unfilled <placeholder> is no sentence
        body = f.interaction_button([r for r in asks if r.get('topic') == topic], topic, root)   # no sentence line (JL 261125)
        buttons, content = [], []      # top-view-left-tab-right-content (ref/top-view-left-tab-right-content.md)
        for i, (name, href, image) in enumerate(views):   # (JL 261125: "this to be on the top ... these to be in the left")
            things = parts.get(name, [])
            faded = ' class="old"' if things and all(old for _, _, old in things) else ''   # nothing real in it: the button reads faded
            buttons.append(f'<button type="button" data-studio-view="{i}" aria-pressed="{"true" if i == 0 else "false"}"{faded}>{esc(name)}</button>')
            if len(things) > 1 or (things and 'Effect' in parts):   # a UI preview: left tabs even for one view
                eid = 'st' + re.sub(r'\W', '', topic.name) + (str(i) if authored is not None else ('' if name == 'Page' else name))
                inner = _side_tabs(eid, [(label, '') for label, _, _ in things],
                                   [frame_of(title, label, url) for label, url, _ in things])
                inner += ''.join(f'<style>[data-pbtab="{eid}{k}"]{{opacity:.5}}[data-pbtab="{eid}{k}"]:hover,'
                                 f'[data-pbtab="{eid}{k}"].on{{opacity:1}}</style>'
                                 for k, (_, _, old) in enumerate(things) if old)     # an earlier version reads faded
            elif image:
                inner = open_dot(f'<img src="{esc(image)}" alt="{esc(title)} drawing" loading="lazy">', href, name,
                                 pop=f'{title} · {name}')
            else:
                inner = frame_of(title, name, href, tall=name == 'Page')
            content.append(f'<div data-studio-content="{i}" data-studio-name="{esc(name)}"{" hidden" if i else ""}>{inner}</div>')
        if views:
            body += '<div class="studio-view-buttons" aria-label="Topic views">' + ''.join(buttons) + '</div>' + ''.join(content)
        m = re.match(r"s(\d+)", topic.name)
        items.append((int(m.group(1)) if m else 999, topic.name.split('-', 1)[0] if m else '', topic_label(title),
                      facts.get('stage') or '', goal,
                      '<article class="studio-topic-content" id="' + esc(topic.name) + '">' + body + '</article>', band, mark))
    if not items:
        return '<p class="mut">No Studio topics in this section.</p>'
    from live.focus_styles_bands import BAND_CSS, band_sec
    bands = {}
    for _, nn, label, stage, goal, panel, band, mark in sorted(items, key=lambda t: (t[0], t[1])):
        fold = band_sec(nn or '·', (f'<span title="{frame.esc(goal)}">{mark} {frame.esc(label)}</span>' if goal else f'{mark} ' + frame.esc(label))
                        , '', panel)   # no stage pill: a page shows no state word (b17 trace 261127/1225)
        bands.setdefault(band, []).append(fold)
    names = list(dict.fromkeys(name for name in group_order if name in bands))   # two decades may share one band name
    names += [name for name in bands if name not in names and name != 'Other']
    if 'Other' in bands:
        names.append('Other')
    folds = ''.join(f'<section class="studio-band" aria-labelledby="studio-band-{i}">'
                    f'<h2 id="studio-band-{i}">{frame.esc(name)}</h2>' + ''.join(bands[name]) + '</section>'
                    for i, name in enumerate(names))
    return PB_CSS + PB_JS + BAND_CSS + STYLE + '<div class="studio-master">' + folds + '</div>' + SCRIPT




STYLE = '''<style>
.studio-band{margin:0 0 24px}.studio-band>h2{display:flex;align-items:center;gap:12px;font-size:16px;font-weight:600;margin:20px 0 12px}
.studio-band>h2:after{content:'';flex:1;border-top:1px solid var(--line)}
.studio-topic-content{min-width:0;padding:2px 8px 10px 0}
.studio-topic-content .pb-list{min-width:0;overflow-x:auto;scrollbar-width:thin;padding-bottom:4px}   /* a fixed column: a long name scrolls */
.studio-topic-content .pb-item{width:max-content;min-width:100%;white-space:nowrap}
.studio-topic-content iframe{display:block;width:100%;height:540px;border:1px solid var(--line);border-radius:8px;background:var(--paper)}
.studio-topic-content .pb-read iframe{border:0;border-radius:0}   /* one frame: the left tabs' reading pane */
.studio-topic-content img{display:block;width:100%;height:auto;border:1px solid var(--line);border-radius:8px}
.studio-view-buttons{display:flex;flex-wrap:nowrap;overflow-x:auto;scrollbar-width:thin;gap:6px;margin:6px 0;padding-bottom:2px}   /* one row, scrolls sideways, never wraps (b17 trace 261127/1530) */
.studio-view-buttons button{flex:none;white-space:nowrap;border:1px solid var(--line);border-radius:8px;padding:5px 10px;font-size:13px}
.studio-view-buttons button[aria-pressed=true]{border-color:var(--accent);background:var(--soft);color:var(--accent)}
.studio-view-buttons button.old{opacity:.5}.studio-view-buttons button.old:hover,.studio-view-buttons button.old[aria-pressed=true]{opacity:1}
@media(max-width:600px){.studio-topic-content iframe{height:430px}}
@media(max-width:700px){.studio-topic-content .pb-list{flex-wrap:nowrap}.studio-topic-content .pb-item{min-width:0;flex:none}}   /* phone: one scrolling row */
@media(min-width:701px){.studio-topic-content .pb-side{grid-template-columns:max-content minmax(0,1fr);gap:8px}   /* as wide as its names, */
.studio-topic-content .pb-list{max-width:170px}   /* up to 170px: a longer name scrolls inside the list */
.studio-topic-content .pb-item{padding:5px 10px}}
</style>'''

SCRIPT = '''<script>(function(){
function start(){document.querySelectorAll('.studio-master').forEach(function(root){
 if(root.dataset.ready)return;root.dataset.ready='1';
 // a frame in a closed fold has a size in current browsers, so its size alone does not say it shows: every fold
 // around it must be open, or all topics load at once and each one's own scroll pulls this page back to it
 function shown(f){for(var d=f.closest('details');d;d=d.parentElement&&d.parentElement.closest('details'))if(!d.open)return false;
   var r=f.getBoundingClientRect();return r.width&&r.height;}
 function load(){root.querySelectorAll('iframe[data-studio-src]').forEach(function(f){
   if(shown(f)&&(!f.hasAttribute('src')||f.dataset.fresh)){
     var again=f.dataset.fresh;delete f.dataset.fresh;   // the same src set again does not reload, so navigate it
     if(again){try{f.contentWindow.location.replace(new URL(f.dataset.studioSrc,location.href).href);return;}catch(x){}}
     f.src=f.dataset.studioSrc;}
 });}
 root.addEventListener('click',function(e){
   // a view or a left tab picked: its frame opens again at its own address, so clicks made in it earlier do not carry
   var pick=e.target.closest('[data-studio-view],.studio-topic-content [data-pbtab]'),art=pick&&pick.closest('.studio-topic-content');
   if(art)art.querySelectorAll('iframe[data-studio-src][src]').forEach(function(f){f.dataset.fresh='1';});
   var button=e.target.closest('[data-studio-view]');if(button){var panel=button.closest('.studio-topic-content');
     panel.querySelectorAll('[data-studio-view]').forEach(function(b){b.setAttribute('aria-pressed',String(b===button));});
     panel.querySelectorAll('[data-studio-content]').forEach(function(p){p.hidden=p.dataset.studioContent!==button.dataset.studioView;});
   }
   requestAnimationFrame(load);   // a view picked, a side tab shown (PB_JS) or a fold opened: its frame loads now
 });
 root.addEventListener('toggle',function(){requestAnimationFrame(load);},true);
 function fromHash(){var id=decodeURIComponent(location.hash.slice(1)), article=id&&document.getElementById(id);
   if(article&&root.contains(article)){var fold=article.closest('details');if(fold){fold.open=true;fold.scrollIntoView({block:'start'});}}}
 window.addEventListener('hashchange',fromHash);fromHash();
 new IntersectionObserver(load).observe(root);load();
});}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start);else start();
})();</script>'''
