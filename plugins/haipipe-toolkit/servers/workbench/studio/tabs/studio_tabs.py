"""Studio read like Main: the page's own topics in sNN order, each a fold (`s06 · 🎨 Files pane`) that opens its Slide,
Draw, Work, Delivery in place."""
import re
from urllib.parse import urlencode

from live import frame
from live.ui_parts import PB_CSS, PB_JS, _side_tabs, open_dot


def topic_label(title):
    """A topic's name on a tab, the same in Studio and Decisions: "work skills: workbench-work" reads "Work skills"."""
    short, separator, rest = title.partition(':')
    label = short if separator and rest.strip()[:1].islower() else title
    return label[:1].upper() + label[1:]


def frame_of(title, name, href, tall=False):
    esc = frame.esc
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


def render(rows, root, group='', asks=()):
    from live import focus_page as f
    items = []
    for topic, drawings, facts in rows:
        if not f.in_group(facts, group) or not f.inside(topic, root):
            continue
        notes = frame._notes(topic)
        title = f.face_title(notes) if notes and f.inside(notes, root) else ''
        title = title or topic.name.replace('_', ' ')
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
        esc = frame.esc
        goal = f.first_sentence(facts.get('topic', ''))       # the topic's sentence: a hover on its fold, never a line
        goal = '' if goal.lstrip().startswith('<') else goal  # a template's unfilled <placeholder> is no sentence
        body = f.interaction_button([r for r in asks if r.get('topic') == topic], topic, root)   # no sentence line (JL 261125)
        buttons, content = [], []      # top-view-left-tab-right-content (ref/top-view-left-tab-right-content.md)
        for i, (name, href, image) in enumerate(views):   # (JL 261125: "this to be on the top ... these to be in the left")
            buttons.append(f'<button type="button" data-studio-view="{i}" aria-pressed="{"true" if i == 0 else "false"}">{name}</button>')
            things = parts.get(name, [])
            if len(things) > 1 or (things and 'Effect' in parts):   # a UI preview: left tabs even for one view
                eid = 'st' + re.sub(r'\W', '', topic.name) + ('' if name == 'Page' else name)
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
            content.append(f'<div data-studio-content="{i}"{" hidden" if i else ""}>{inner}</div>')
        if views:
            body += '<div class="studio-view-buttons" aria-label="Topic views">' + ''.join(buttons) + '</div>' + ''.join(content)
        m = re.match(r"s(\d+)", topic.name)
        items.append((int(m.group(1)) if m else 999, topic.name.split('-', 1)[0] if m else '', topic_label(title),
                      facts.get('stage') or '', goal,
                      '<article class="studio-topic-content" id="' + esc(topic.name) + '">' + body + '</article>'))
    if not items:
        return '<p class="mut">No Studio topics in this section.</p>'
    from live.focus_styles_bands import BAND_CSS, band_sec
    folds = ''.join(band_sec(nn or '·', (f'<span title="{frame.esc(goal)}">🎨 {frame.esc(label)}</span>' if goal else '🎨 ' + frame.esc(label))
                             + (f' <span class="row-stage">{frame.esc(stage)}</span>' if stage else ''), '', panel)
                    for _, nn, label, stage, goal, panel in sorted(items, key=lambda t: (t[0], t[1])))
    return PB_CSS + PB_JS + BAND_CSS + STYLE + '<div class="studio-master">' + folds + '</div>' + SCRIPT




STYLE = '''<style>
.studio-topic-content{min-width:0;padding:2px 8px 10px 0}
.studio-topic-content iframe{display:block;width:100%;height:540px;border:1px solid var(--line);border-radius:8px;background:var(--paper)}
.studio-topic-content img{display:block;width:100%;height:auto;border:1px solid var(--line);border-radius:8px}
.studio-view-buttons{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0}
.studio-view-buttons button{border:1px solid var(--line);border-radius:8px;padding:5px 10px;font-size:13px}
.studio-view-buttons button[aria-pressed=true]{border-color:var(--accent);background:var(--soft);color:var(--accent)}
@media(max-width:600px){.studio-topic-content iframe{height:430px}}
@media(min-width:701px){.studio-topic-content .pb-side{grid-template-columns:max-content minmax(0,1fr);gap:8px}
.studio-topic-content .pb-item{padding:5px 10px}}
</style>'''

SCRIPT = '''<script>(function(){
function start(){document.querySelectorAll('.studio-master').forEach(function(root){
 if(root.dataset.ready)return;root.dataset.ready='1';
 function load(){root.querySelectorAll('iframe[data-studio-src]').forEach(function(f){
   if(f.getBoundingClientRect().width&&f.getBoundingClientRect().height&&(!f.hasAttribute('src')||f.dataset.fresh)){
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
