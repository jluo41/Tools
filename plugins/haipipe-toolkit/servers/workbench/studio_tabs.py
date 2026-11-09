"""Studio's existing topic assets, selected on the left and read on the right."""
from urllib.parse import urlencode

from live import frame
from live.ui_parts import PB_CSS, PB_JS, _side_tabs


def topic_label(title):
    """A topic's name on a tab, the same in Studio and Decisions: "work skills: workbench-work" reads "Work skills"."""
    short, separator, rest = title.partition(':')
    label = short if separator and rest.strip()[:1].islower() else title
    return label[:1].upper() + label[1:]


def render(rows, root, group='', asks=()):
    from live import focus_page as f
    items, panels = [], []
    for topic, drawings, facts in rows:
        if not f.in_group(facts, group) or not f.inside(topic, root):
            continue
        notes = frame._notes(topic)
        title = f.face_title(notes) if notes and f.inside(notes, root) else ''
        title = title or topic.name.replace('_', ' ')
        views = []
        deck = topic / (topic.name + '.slides.html')
        if deck.is_file() and f.inside(deck, root):
            views.append(('Slide', frame._file_url(deck, root), ''))
        drawings = [p for p in drawings if p.is_file() and f.inside(p, root)]
        if drawings:
            previews = [drawings[0].with_suffix('.png'), topic / (topic.name + '.png')]
            preview = next((p for p in previews if p.is_file() and f.inside(p, root)), None)
            views.append(('Draw', frame._draw_url(drawings[0], root), frame._file_url(preview, root) if preview else ''))
        mind = topic / (topic.name + '.mindmap.md')
        if mind.is_file() and f.inside(mind, root):
            views.append(('MindMap', frame.ROUTE + '?' + urlencode({'view': 'focus-map', 'path': frame.rel(mind, root)}), ''))
        if f.is_topic(topic) and f.work_root(topic) is not None:
            views.append(('Work', frame.ROUTE + '?' + urlencode({'view': 'focus-part', 'part': 'work', 'path': frame.rel(topic, root)}), ''))
        if f.is_topic(topic) and (topic / 'delivery').is_dir():
            views.append(('Delivery', frame.ROUTE + '?' + urlencode({'view': 'focus-delivery', 'path': frame.rel(topic, root)}), ''))
        esc = frame.esc
        heading = (f'<h3><a data-pop="{esc(title)}" href="{esc(frame.reader(notes, root))}">{esc(title)}</a></h3>'
                   if notes and f.inside(notes, root) else f'<h3>{esc(title)}</h3>')
        goal = f.first_sentence(facts.get('topic', ''))
        state = ('<span class="row-stage">' + esc(facts['stage']) + '</span>') if facts.get('stage') else ''
        dtype = ('<span class="row-type" title="delivery type">' + esc(facts['dtype']) + '</span>') if facts.get('dtype') else ''
        body = heading + state + dtype + (f'<p>{esc(goal)}</p>' if goal else '')
        body += f.interaction_button([r for r in asks if r.get('topic') == topic], topic, root)
        buttons, content = [], []
        for i, (name, href, image) in enumerate(views):
            buttons.append(f'<button type="button" data-studio-view="{i}" aria-pressed="{"true" if i == 0 else "false"}">{name}</button>')
            media = (f'<img src="{esc(image)}" alt="{esc(title)} drawing" loading="lazy">' if image else
                     f'<iframe title="{esc(title)} · {name}" data-studio-src="{esc(href)}"></iframe>')
            content.append(f'<div data-studio-content="{i}"{" hidden" if i else ""}>' + media
                           + f'<p><a class="row-verb" data-pop="{esc(title)} · {name}" href="{esc(href)}">Open {name} ↗</a></p></div>')
        body += ('<div class="studio-view-buttons" aria-label="Topic views">' + ''.join(buttons) + '</div>' + ''.join(content)
                 if views else '<p class="mut">No preview available yet.</p>')
        items.append((topic_label(title), facts.get('stage') or ''))   # its stage under its name, as Status had it
        panels.append('<article class="studio-topic-content" id="' + esc(topic.name) + '">' + body + '</article>')
    if not items:
        return '<p class="mut">No Studio topics in this section.</p>'
    options = ''.join(f'<option value="{i}">{frame.esc(title)}</option>' for i, (title, _) in enumerate(items))
    return (PB_CSS + STYLE + '<div class="studio-master"><select class="studio-topic-select" aria-label="Studio topic">'
            + options + '</select>' + _side_tabs('studio-topic-', items, panels) + '</div>' + PB_JS + SCRIPT)


STYLE = '''<style>
.studio-topic-select{display:none}
.studio-master>.pb-side{grid-template-columns:180px minmax(0,1fr)}
.studio-master>.pb-side>.pb-read{max-height:none}
.studio-topic-content{min-width:0}.studio-topic-content h3{font-size:18px;margin:2px 0 8px}
.studio-topic-content>p{font-size:14px}
.studio-view-buttons{display:flex;flex-wrap:wrap;gap:6px;margin:12px 0}
.studio-view-buttons button{border:1px solid var(--line);border-radius:8px;padding:5px 10px;font-size:13px}
.studio-view-buttons button[aria-pressed=true]{border-color:var(--accent);background:var(--soft);color:var(--accent)}
.studio-topic-content iframe{display:block;width:100%;height:540px;border:1px solid var(--line);border-radius:8px;background:var(--paper)}
.studio-topic-content img{display:block;width:100%;height:auto;border:1px solid var(--line);border-radius:8px}
@media(max-width:600px){.studio-master>.pb-side{display:block}.studio-master>.pb-side>.pb-list{display:none}
.studio-topic-select{display:block;width:100%;min-height:44px;font:inherit;color:var(--ink);background:var(--paper);border:1px solid var(--line);border-radius:8px;padding:8px;margin:8px 0}
.studio-topic-content iframe{height:430px}}
</style>'''

SCRIPT = '''<script>(function(){
function start(){document.querySelectorAll('.studio-master').forEach(function(root){
 if(root.dataset.ready)return;root.dataset.ready='1';
 var select=root.querySelector('select'),tabs=Array.from(root.querySelectorAll(':scope>.pb-tabset>.pb-list>[data-pbtab]'));
 function load(){root.querySelectorAll('iframe[data-studio-src]').forEach(function(f){
   if(f.getBoundingClientRect().width&&f.getBoundingClientRect().height&&!f.hasAttribute('src'))f.src=f.dataset.studioSrc;
 });}
 select.addEventListener('change',function(){tabs[Number(select.value)].click();});
 root.addEventListener('click',function(e){
   var topic=e.target.closest('[data-pbtab]');if(topic&&tabs.includes(topic))select.value=String(tabs.indexOf(topic));
   var button=e.target.closest('[data-studio-view]');if(button){var panel=button.closest('.studio-topic-content');
     panel.querySelectorAll('[data-studio-view]').forEach(function(b){b.setAttribute('aria-pressed',String(b===button));});
     panel.querySelectorAll('[data-studio-content]').forEach(function(p){p.hidden=p.dataset.studioContent!==button.dataset.studioView;});
   }
   requestAnimationFrame(load);
 });
 root.closest('details')?.addEventListener('toggle',load);
 function fromHash(){var id=decodeURIComponent(location.hash.slice(1)), article=id&&document.getElementById(id);
   if(article&&root.contains(article)){var panel=article.closest('[data-pbpanel]'), index=Array.from(root.querySelectorAll(':scope>.pb-tabset>.pb-read>[data-pbpanel]')).indexOf(panel);
     if(index>=0&&tabs[index])tabs[index].click();}}
 window.addEventListener('hashchange',fromHash);fromHash();
 new IntersectionObserver(load).observe(root);load();
});}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start);else start();
})();</script>'''
