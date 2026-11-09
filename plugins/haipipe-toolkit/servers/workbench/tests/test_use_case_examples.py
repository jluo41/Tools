"""Use cases link to existing pages without widening the served filesystem."""
import json
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from host_paths import bootstrap
bootstrap()
from live import use_case_examples as cases


def make_page(root):
    block = root / 'work/b01_demo'
    job = block / 'j01_job'
    task = job / 't01_task'
    task.mkdir(parents=True)
    (block / 'board.md').write_text('# Demo')
    (job / 'j01_job.md').write_text('# Job')
    (task / 't01_task.md').write_text('# Task')
    return block, job, task


def mapping(rows):
    return {'job': {'Job': {'Data preparation': rows}}}


def test_public_examples_preserve_block_job_task_links(tmp_path):
    block, job, task = make_page(tmp_path)
    source = tmp_path / 'job-views.md'
    guide = {'use_cases': mapping([{'path': str(job.relative_to(tmp_path)), 'label': 'Blueprint example'}])}
    rows = cases.examples(source, tmp_path, guide, 'job', 'Job', 'Data preparation')
    assert len(rows) == 1
    assert rows[0]['block'] == block and rows[0]['job'] == job and rows[0]['tasks'] == [task]
    markup = cases.button('Data preparation', 'Job', source, tmp_path, guide, 'job')
    assert 'Blueprint example' in markup and '<summary>Tasks</summary>' in markup
    assert 'Block · b01_demo' in markup and 'Task · t01_task' in markup
    assert 'target="_blank" rel="noopener"' in markup
    assert 'data-url=' not in markup


def test_external_sources_require_private_allowlist_and_configured_origin(tmp_path):
    root = tmp_path / 'served'; root.mkdir()
    external = tmp_path / 'other'
    block, job, task = make_page(external)
    settings = external / '.server_config'; settings.mkdir()
    (settings / 'settings.env').write_text('DOMAIN=https://example.test\n')
    source = root / 'job-views.md'
    row = {'space': 'other', 'path': str(job.relative_to(external))}
    guide = {'use_cases': mapping([row])}
    assert cases.examples(source, root, guide, 'job', 'Job', 'Data preparation') == []
    local = root / '.server_config'; local.mkdir()
    config = {'spaces': {'other': {'root': str(external)}}, 'matrices': {'job-views.md': mapping([row])}}
    (local / 'workbench-examples.json').write_text(json.dumps(config))
    result = cases.examples(source, root, guide, 'job', 'Job', 'Data preparation')
    assert len(result) == 1 and result[0]['origin'] == 'https://example.test'
    assert 'https://example.test/_board/workbench?' in cases._link(result[0], job, 'Job')
    row['preview_available'] = False
    (local / 'workbench-examples.json').write_text(json.dumps(config))
    unavailable = cases.button('Data preparation', 'Job', source, root, guide, 'job')
    assert 'Preview unavailable. Source folder verified.' in unavailable
    assert '<a href=' not in unavailable
    row.pop('preview_available')
    (local / 'workbench-examples.json').write_text(json.dumps(config))
    (settings / 'settings.env').write_text('DOMAIN=javascript:alert(1)\n')
    result = cases.examples(source, root, guide, 'job', 'Job', 'Data preparation')
    assert not result[0]['can_open']
    assert '<a' not in cases._link(result[0], job, 'Job')


def test_paths_cannot_escape_and_missing_pages_are_not_linked(tmp_path):
    root = tmp_path / 'served'; root.mkdir()
    external = tmp_path / 'other'
    block, job, task = make_page(external)
    (root / 'shortcut').symlink_to(job, target_is_directory=True)
    guide = {'use_cases': mapping([{'path': p} for p in ['../other/work/b01_demo/j01_job', str(job), 'shortcut', 'missing']])}
    source = root / 'job-views.md'
    assert cases.examples(source, root, guide, 'job', 'Job', 'Data preparation') == []
    config = root / '.server_config'; config.mkdir()
    (config / 'workbench-examples.json').write_text('{"matrices": []}')
    assert cases.examples(source, root, guide, 'job', 'Job', 'Data preparation') == []


def test_case_notes_explain_gaps_and_escape_markup(tmp_path):
    source = tmp_path / 'task-views.md'
    guide = {'use_case_notes': {'task': {'Task': {'Individual analysis': 'Example needed <script>alert(1)</script>'}}}}
    markup = cases.button('Individual analysis', 'Task', source, tmp_path, guide, 'task')
    assert 'Example needed' in markup
    assert 'No linked examples yet' not in markup
    assert '<script>' not in markup
    assert '&lt;script&gt;' in markup
    assert 'No linked examples yet' in cases.button('Other', 'Task', source, tmp_path, guide, 'task')
