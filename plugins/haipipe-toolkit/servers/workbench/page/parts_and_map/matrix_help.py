"""Read-only explanations for an authored type/view matrix."""
import html
import json
import re


def guide_for(source, root):
    path = source.with_name('view-guide.json')
    if not path.resolve().is_relative_to(root.resolve()) or not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def words(value):
    return html.unescape(re.sub('<[^>]*>', '', value)).strip()


def plain(value):
    return re.sub(r'^[^A-Za-z]+', '', words(value))


def help_cell(cell, kind, view, level, guide, example_url=''):
    sections = guide.get('sections', {})
    profile = guide.get('types', {}).get(plain(kind), {})
    result = []
    for label in cell.split('<br>'):
        entry = sections.get(words(label))
        if not isinstance(entry, dict):
            result.append(label)
            continue
        override = guide.get('overrides', {}).get(level, {}).get(plain(kind), {}).get(words(label), {})
        entry = {**entry, **override}
        example = entry.get('example', '')
        for name in ('result', 'evidence'):
            example = example.replace('{' + name + '}', profile.get(name, 'the work outputs' if name == 'result' else 'supporting records'))
        skills = guide.get('skills', {}).get(plain(view), []) if plain(label) == 'Skills' else []
        if skills:
            example = '\n'.join(s.replace('{level}', level) for s in skills)
        data = {'title': words(label), 'context': f'{level.title()} · {plain(kind)} · {plain(view)}',
                'what': entry.get('what', ''), 'outcome': entry.get('outcome', ''),
                'layout': entry.get('layout', ''), 'layout-detail': entry.get('layout_detail', ''),
                'example': example, 'example-title': 'Skills for this view' if skills else entry.get('example_title', 'Example'),
                'url': example_url}
        attrs = ' '.join(f'data-{key}="{html.escape(str(value), quote=True)}"' for key, value in data.items())
        result.append(f'<button type="button" class="matrix-section" aria-haspopup="dialog" {attrs}>{label}</button>')
    return '<br>'.join(result)


def with_dialog(table, source):
    title_id = 'matrix-help-' + re.sub(r'[^a-zA-Z0-9_-]', '', source.stem)
    return ('<div class="matrix-guide">' + table +
            f'<dialog class="matrix-dialog" aria-labelledby="{title_id}">'
            '<form method="dialog"><button type="submit" autofocus>Close</button></form>'
            '<p class="matrix-context" data-field="context"></p>'
            f'<h2 id="{title_id}" data-field="title"></h2>'
            '<div data-use-case-body hidden></div>'
            '<p data-field="what"></p>'
            '<div data-block="layout"><h3>Layout</h3><p data-field="layout"></p></div>'
            '<div data-block="example"><h3 data-field="exampleTitle"></h3><p class="matrix-example" data-field="example"></p></div>'
            '<p class="matrix-open"><a data-example-link target="_blank" rel="noopener">Open example ↗</a></p>'
            '</dialog></div>' + STYLE + SCRIPT)


STYLE = '''<style>
.matrix-section{font:inherit;color:#1864ab;background:none;border:0;padding:2px 0;text-align:left;cursor:pointer;text-decoration:underline;text-decoration-color:#b4cce2;text-underline-offset:3px;line-height:inherit}
.matrix-section:hover{text-decoration-color:currentColor}
.matrix-section:focus-visible{outline:2px solid #1864ab;outline-offset:3px;border-radius:3px}
.matrix-dialog{padding:24px;overflow:auto;line-height:1.6}
.matrix-dialog[open]{display:block}
.matrix-dialog form{float:right}.matrix-dialog form button{font:inherit;padding:4px 12px;border:1px solid #ddd;border-radius:6px;background:#fff;cursor:pointer}
.matrix-dialog h2{margin:6px 0 20px;font-size:22px;clear:both}.matrix-dialog h3{font-size:14px;margin:18px 0 4px}.matrix-dialog p{margin:4px 0}
.matrix-dialog .matrix-context{font-size:13px;color:#666;padding-right:70px}.matrix-example{white-space:pre-line}
.matrix-dialog [hidden]{display:none}.matrix-dialog .matrix-open{margin-top:20px}.matrix-open a{color:#1864ab}
.use-case-example{border-top:1px solid #ddd;padding:8px 0}.use-case-example ul{padding-left:20px;margin:6px 0}
.use-case-example li{margin:6px 0;overflow-wrap:anywhere}.use-case-example a{color:#1864ab}
.use-case-path code{white-space:normal;overflow-wrap:anywhere}
</style>'''

SCRIPT = '''<script>(()=>{
const script=document.currentScript, root=script.previousElementSibling.previousElementSibling;
const dialog=root.querySelector('.matrix-dialog');let trigger=null;
root.addEventListener('click',event=>{
 const button=event.target.closest('.matrix-section');if(!button)return;
 trigger=button;
 dialog.querySelectorAll('[data-field]').forEach(node=>{node.textContent=button.dataset[node.dataset.field]||'';});
 dialog.querySelectorAll('[data-block]').forEach(node=>{node.hidden=!button.dataset[node.dataset.block];});
 const examples=dialog.querySelector('[data-use-case-body]');examples.replaceChildren();examples.hidden=true;
 const template=button.dataset.template&&root.querySelector('#'+button.dataset.template);
 if(template){examples.append(template.content.cloneNode(true));examples.hidden=false;}
 const link=dialog.querySelector('[data-example-link]'),url=button.dataset.url||'';
 const local=url.startsWith('/')&&!url.startsWith('//');link.parentElement.hidden=!local;
 if(local)link.setAttribute('href',url);else link.removeAttribute('href');
 dialog.showModal();
});
dialog.addEventListener('click',event=>{
 if(event.target!==dialog)return;const box=dialog.getBoundingClientRect();
 if(event.clientX<box.left||event.clientX>box.right||event.clientY<box.top||event.clientY>box.bottom)dialog.close();
});
dialog.addEventListener('close',()=>{if(trigger)trigger.focus({preventScroll:true});});
})();</script>'''
