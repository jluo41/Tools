"""Work Job Main's Overview: real records, local inspection, and no child-page navigation."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

from live import frame
from live.ui_parts import PB_CSS, PB_JS, _side_tabs


def record_title(folder: Path, root: Path) -> str:
    from live import focus_page as f

    face = frame.face(folder)
    title = f.face_title(face) if face and f.inside(face, root) else ''
    if not title and face and f.inside(face, root):
        heading = re.search(r'^#\s+(.+?)\s*$', face.read_text(encoding='utf-8'), re.M)
        title = heading.group(1) if heading else ''
    title = title or f.page_title(folder)
    return title if title.startswith(folder.name[:3]) else f'{folder.name[:3]} · {title}'


def task_groups(folder: Path, root: Path, groups: list) -> list:
    """Use the same authored Task bands as Jobs navigation, retaining ungrouped Tasks."""
    from live import focus_jobs, focus_page as f

    tasks = sorted(p for p in folder.iterdir() if p.is_dir() and re.match(r"^t\d\d[_-]", p.name)
                   and f.inside(p, root) and p.resolve().is_relative_to(folder.resolve()))
    names = focus_jobs.band_names(folder / f"{folder.name}.md")
    out = {}
    if names:
        for task in tasks:
            topic = focus_jobs.task_topic(task.name)
            out.setdefault(names.get(topic, f"t{topic}N"), []).append(task)
    else:
        covered = set()
        for name, paths in groups:
            selected = [p for p in tasks if p in paths and p not in covered]
            if selected:
                out.setdefault(name, []).extend(selected)
                covered.update(selected)
        rest = [p for p in tasks if p not in covered]
        if rest:
            out.setdefault("Tasks", []).extend(rest)
    return list(out.items())


def render(folder: Path, root: Path, data: dict, questions: list, groups: list) -> str:
    from live import focus_page as f, work_frame as wf

    scope = "jov-" + hashlib.sha256(str(folder.relative_to(root)).encode()).hexdigest()[:12]
    # Preserve the top-view selector contract; switching is scoped to this component.
    eid = "ov" + re.sub(r"\W", "", folder.name)
    grouped = task_groups(folder, root, groups)
    entries, dialogs = {}, []
    for _, paths in grouped:
        for task in paths:
            key = hashlib.sha256(str(task.relative_to(root)).encode()).hexdigest()[:12]
            title = record_title(task, root)
            face = f.read_face(task, root)
            goal = str(face.get("goal") or "")
            entries[task] = (key, title, goal)
            detail = ('<div class=jov-task-goal>' + f.markdown(goal, task, root) + '</div>') if goal else ''
            if face.get("close"):
                detail += '<h3>Close</h3>' + f.markdown(str(face["close"]), task, root)
            dialogs.append(f'<dialog class=jov-detail data-jov-detail="{key}" aria-labelledby="{scope}-{key}-title">'
                           '<button type=button class=jov-close data-jov-close>Close</button>'
                           f'<h2 id="{scope}-{key}-title">{frame.esc(title)}</h2>{detail}'
                           f'<code>{frame.esc(str(task.relative_to(root)))}/</code></dialog>')

    branches, rows = [], []
    for name, paths in grouped:
        nodes = []
        for task in paths:
            key, title, goal = entries[task]
            nodes.append(f'<button type=button class=jov-node data-jov-task="{key}">{frame.esc(title)}</button>')
            rows.append(f'<button type=button class=jov-row data-jov-task="{key}"><b>{frame.esc(title)}</b>'
                        + (f'<span>{frame.esc(goal)}</span>' if goal else '') + '</button>')
        branches.append(f'<div class=jov-branch><div class=jov-group>{frame.esc(name)}</div>'
                        '<div class=jov-leaves>' + ''.join(nodes) + '</div></div>')
    tree = f'<div class=jov-tree aria-label="Task groups"><div class=jov-root>{frame.esc(record_title(folder, root))}</div>'
    tree += ('<div class=jov-branches>' + ''.join(branches) + '</div>' if branches else '') + '</div>'
    structure = '<div class=jov-structure>' + ''.join(rows) + '</div>' if rows else tree
    maps = _side_tabs(scope + '-map', [('Topics', ''), ('Work Structure', '')], [tree, structure])
    has_requirements = bool(data['sections'].get('requirements') or data.get('close')
                            or any(q.get('acceptance') for q in questions))
    views = [('Goal', wf.goal(folder, root, data) if data.get('goal') else ''),
             ('Requirements', wf.requirements(folder, root, data, questions) if has_requirements else ''),
             ('MindMap', maps)]
    first = next(i for i, (_, body) in enumerate(views) if body)
    buttons = ''.join(f'<button type=button data-topview="{eid}-{i}" data-jov-view="{i}" '
                      f'aria-pressed="{"true" if i == first else "false"}"'
                      + ('' if body else ' disabled') + f'>{name}</button>'
                      for i, (name, body) in enumerate(views))
    panels = ''.join(f'<div data-topbody="{eid}-{i}" data-jov-panel="{i}"'
                     + ('' if i == first else ' hidden') + f'>{body}</div>' for i, (_, body) in enumerate(views))
    stage = ('<div class=jov-stage><div class=jov-toolbar><nav class=jov-views aria-label="Overview views">'
             + buttons + '</nav><button type=button class="open-dot jov-expand" data-jov-expand '
             'aria-label="Expand Overview" title="Expand Overview" aria-pressed="false"></button></div>'
             '<div class=jov-content>' + panels + '</div>' + ''.join(dialogs) + '</div>')
    body = (f'<div class=job-overview data-job-overview="{scope}">{stage}'
            '<dialog class=jov-expanded aria-label="Overview"></dialog></div>')
    return (wf.OV_CSS + PB_CSS + STYLE + wf.section(1, '📋 Brief', body)
            .replace('<details class=band-sec>', '<details class=band-sec open>', 1) + PB_JS + SCRIPT)


STYLE = '''<style>
.job-overview{color:var(--ink);position:relative}
.jov-toolbar{display:flex;align-items:center;gap:12px;margin:3px 0 20px}
.jov-views{display:flex;flex-wrap:nowrap;overflow-x:auto;scrollbar-width:thin;gap:6px;flex:1;min-width:0}.jov-views button{flex:none;white-space:nowrap}
.jov-views button{font:inherit;font-size:14px;border:1px solid transparent;border-radius:6px;background:none;color:var(--muted);padding:6px 13px;cursor:pointer}
.jov-views button[aria-pressed=true]{background:var(--soft);color:var(--accent);border-color:var(--line);font-weight:600}
.jov-views button:disabled{opacity:.4;cursor:default}
.job-overview button:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
.job-overview .jov-expand{position:static;display:grid;flex:none;cursor:pointer;background:none;border:0}
.job-overview .jov-expand::before,.job-overview .jov-expand:hover::before{content:'';width:8px;height:8px;background:var(--accent);opacity:1}
.jov-content{min-height:190px;padding:0 2px 10px}
.jov-content .wk-ov{margin:10px 0 18px;max-width:76ch}
.jov-content .pb-big{font-size:22px;line-height:1.65;letter-spacing:-.25px}
.jov-content .pb-kv{grid-template-columns:100px 1fr}
.jov-content .pb-panel{border:0;padding:0;background:none;min-height:0}
.job-overview .pb-side{grid-template-columns:150px minmax(0,1fr)}
.job-overview .pb-side>.pb-list{display:flex}
.job-overview .pb-side.jov-list-hidden{grid-template-columns:minmax(0,1fr)}
.job-overview .pb-side.jov-list-hidden>.pb-list{display:none}
.jov-tree{display:flex;flex-direction:column;align-items:center;gap:24px;padding:12px 6px 20px}
.jov-root{position:relative;border:1px solid var(--line);border-radius:6px;padding:9px 16px;text-align:center}
.jov-root:not(:last-child):after{content:"";position:absolute;top:100%;left:50%;height:24px;border-left:1px solid var(--line)}
.jov-branches{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(170px,100%),1fr));gap:22px;width:100%;border-top:1px solid var(--line)}
.jov-branch{position:relative;padding-top:18px;min-width:0}
.jov-branch:before{content:"";position:absolute;top:0;left:50%;height:18px;border-left:1px solid var(--line)}
.jov-group{border-radius:6px;background:var(--soft);color:var(--accent);text-align:center;padding:8px 10px;margin-bottom:16px;overflow-wrap:anywhere}
.jov-leaves{display:flex;flex-direction:column;gap:9px;margin-left:8px;border-left:1px solid var(--line);padding-left:12px}
.jov-node{position:relative;width:100%;text-align:left;background:var(--paper);border:1px solid var(--line);border-radius:6px;padding:9px 10px;font:inherit;font-size:13px;cursor:pointer;color:var(--ink);overflow-wrap:anywhere}
.jov-node:before{content:"";position:absolute;left:-13px;top:50%;width:12px;border-top:1px solid var(--line)}
.jov-node:hover{border-color:var(--accent);color:var(--accent)}
.jov-row{display:flex;flex-direction:column;gap:4px;text-align:left;width:100%;background:none;border:0;border-bottom:1px solid var(--line);padding:14px 2px;color:var(--ink);font:inherit;cursor:pointer}
.jov-row:hover b{color:var(--accent)}.jov-row span{font-size:13px;color:var(--muted)}
.job-overview dialog{background:var(--paper);color:var(--ink);border:1px solid var(--line);border-radius:10px;padding:28px;max-height:90vh;overflow:auto}
.job-overview dialog::backdrop{background:#16223466}
.jov-detail{width:min(760px,90vw)}.jov-detail h2{font-size:22px;padding-right:75px;margin:0 0 20px}.jov-detail h3{font-size:14px;margin:18px 0 8px}
.jov-task-goal{font-size:19px;line-height:1.6}.jov-detail code{display:block;font-size:12px;color:var(--muted);overflow-wrap:anywhere;margin-top:24px}
.jov-close{float:right;background:none;border:1px solid var(--line);border-radius:6px;padding:5px 12px;font:inherit;color:var(--ink);cursor:pointer}
.jov-expanded{width:min(1120px,94vw)}.jov-expanded .jov-content{min-height:300px}
@media(max-width:700px){.job-overview .pb-side{grid-template-columns:minmax(0,1fr)}}
@media(max-width:600px){.jov-content .pb-big{font-size:19px}.jov-content .pb-kv{grid-template-columns:1fr}.job-overview dialog{padding:18px}.jov-views button{padding:6px 9px}}
@media(pointer:coarse){.jov-views button,.jov-node,.jov-close{min-height:44px}.job-overview .jov-expand{border:14px solid var(--paper);box-sizing:content-box}}
</style>'''


SCRIPT = '''<script>
(function(){document.querySelectorAll('.job-overview').forEach(function(root){
 if(root.dataset.jovReady)return;root.dataset.jovReady='1';
 var expanded=root.querySelector('.jov-expanded'),stage=root.querySelector('.jov-stage'),placeholder=null,last=null;
 function restore(){if(placeholder){placeholder.replaceWith(stage);placeholder=null;}
  var b=root.querySelector('[data-jov-expand]');b.setAttribute('aria-pressed','false');b.title='Expand Overview';b.setAttribute('aria-label',b.title);b.focus();}
 expanded.addEventListener('close',restore);
 root.querySelectorAll('.jov-detail').forEach(function(d){d.addEventListener('close',function(){if(last)last.focus();});});
 root.addEventListener('click',function(e){var b=e.target.closest('[data-jov-view],[data-jov-task],[data-jov-expand],[data-jov-close],.pb-fold');
  if(!b||!root.contains(b))return;e.preventDefault();e.stopPropagation();
  if(b.classList.contains('pb-fold')){var hidden=b.closest('.pb-tabset').classList.toggle('jov-list-hidden');b.setAttribute('aria-expanded',hidden?'false':'true');}
  if(b.hasAttribute('data-jov-view')){root.querySelectorAll('[data-jov-view]').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false');});
   root.querySelectorAll('[data-jov-panel]').forEach(function(p){p.hidden=p.dataset.jovPanel!==b.dataset.jovView;});}
  if(b.hasAttribute('data-jov-task')){last=b;var d=root.querySelector('[data-jov-detail="'+b.dataset.jovTask+'"]');if(d)d.showModal();}
  if(b.hasAttribute('data-jov-close'))b.closest('dialog').close();
  if(b.hasAttribute('data-jov-expand')){if(expanded.open){expanded.close();return;}
   placeholder=document.createComment('Overview');stage.before(placeholder);expanded.append(stage);expanded.showModal();
   b.setAttribute('aria-pressed','true');b.title='Restore Overview';b.setAttribute('aria-label',b.title);}
 });
 root.querySelectorAll('dialog').forEach(function(d){d.addEventListener('click',function(e){if(e.target!==d)return;var r=d.getBoundingClientRect();
  if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)d.close();});});
});})();
</script>'''
