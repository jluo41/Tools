"""Bind Insight's Job previews to shared Studio views and existing source files."""
import argparse
import json
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlsplit

import build_structure as structure

ROOT, BLOCK, SKILLS = structure.ROOT, structure.BLOCK, structure.SKILLS.rstrip('/')
CONFIG = {
    'insight-board': ('s11-insight-job-preview', 'j03', 't02', 'segment-grid', 'Segment grid', 'Question answer'),
    'question-book': ('s12-questionbook-job-preview', 'j02', 't09', 'version-changes', 'Version changes', 'Question definition'),
    'data-prep': ('s13-dataprep-job-preview', 'j01', 't01', 'steps-and-runs', 'Steps and Runs', 'Prep step'),
}


def view(name, *items):
    return dict(name=name, items=list(items))


def item(name, **source):
    return dict(name=name, **source)


def manifest(kind):
    topic, job, task, effect, label, task_type = CONFIG[kind]
    cfg = structure.CONFIG[kind]
    example = structure.EXAMPLES + cfg['example']
    prefix = structure.relative(BLOCK / topic)

    def route(**extra):
        return '/_board/workbench?' + urlencode(dict(path=example, layout='focus', section='jobs', group=job, **extra))

    contract = SKILLS + '/hai-insight/ref/' + ('dataprep.md' if kind == 'data-prep' else 'insight-ladder.md')
    task_contract = (SKILLS + '/folder-kinds/hai-insight-question/SKILL.md'
                     if kind == 'question-book' else contract)
    tasks = [item(task_type, path=task_contract)]
    if kind == 'insight-board':
        tasks.insert(0, item('Preparation', path=SKILLS + '/hai-insight/ref/dataprep.md'))
    return dict(views=[
        view('Page-Job', *[item(name, url=route(mark=mark)) for name, mark in (
            ('job-rows', 'jobs-rows,job-ttopics,job-subs'), ('job-overview', 'view=overview'),
            ('job-tasks', 'view=standing'), ('job-findings', 'view=findings'))]),
        view('Page-Task', item(task_type, url=route(task=task))),
        view('Job types', item(cfg['job_type'], path=contract)),
        view('Task types', *tasks),
        view('QuickHtml', item(label, path=prefix + '/delivery/ui/' + effect + '.html')),
        view('Draw', item('MindMap', path=prefix + '/' + topic + '.mindmap.md'),
             item('Canvas', path=prefix + '/' + topic + '.excalidraw')),
    ])


def validate(data):
    """Every binding reaches a real source; Job/Task selection never changes the Block path."""
    assert [v['name'] for v in data['views']] == [
        'Page-Job', 'Page-Task', 'Job types', 'Task types', 'QuickHtml', 'Draw']
    for v in data['views']:
        assert v['items'], v['name']
        for row in v['items']:
            if 'path' in row:
                target = (ROOT / row['path']).resolve()
                assert target.is_relative_to(ROOT) and target.is_file(), row
                continue
            parsed = urlsplit(row['url'])
            assert not parsed.scheme and not parsed.netloc and parsed.path == '/_board/workbench', row
            query = parse_qs(parsed.query)
            block = (ROOT / query['path'][0]).resolve()
            assert block.is_relative_to(ROOT) and (block / 'board.md').is_file(), row
            assert query['layout'] == ['focus'] and query['section'] == ['jobs'], row
            jobs = list(block.glob(query['group'][0] + '_*'))
            assert len(jobs) == 1 and jobs[0].is_dir(), row
            if query.get('task'):
                tasks = list(jobs[0].glob(query['task'][0] + '_*'))
                assert len(tasks) == 1 and tasks[0].is_dir(), row


def generated_files():
    out = {}
    for kind, (topic, *_) in CONFIG.items():
        data = manifest(kind)
        validate(data)
        face = (BLOCK / topic / (topic + '.md')).read_text()
        assert 's72-studio-type-block-job-ui-preview' in face, topic
        assert '\nChecklist\n' in face, topic
        out[BLOCK / topic / 'studio-views.json'] = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    changed = []
    for path, text in generated_files().items():
        if not path.is_file() or path.read_text() != text:
            changed.append(str(path.relative_to(ROOT)))
            if not args.check:
                path.write_text(text)
    if args.check and changed:
        raise SystemExit('Regenerate: ' + ', '.join(changed))
    print('Job preview source bindings are current' if args.check else 'Built the three Job preview manifests')


if __name__ == '__main__':
    main()
