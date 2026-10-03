"""One Task Run's exact Result, using the existing Paper result appearance."""
from live.runs import local_runs
from live.paper import _RESULT_PAGE, _csv_view, _md_view
from live.taskboard import _source_url, _e


def render_task_run(page, root, key):
    # The Task reader resolves redirected stores and Ticket/Result pairing.
    # Never fall back to another Run's files when this Run has no Result.
    matches = [row for row in local_runs(page)
               if (row.get('global_id') or row['run_id']) == key]
    if len(matches) != 1:
        raise ValueError('The selected Run no longer has a unique record')
    row = matches[0]
    result = row.get('result_path')
    files, truncated = [], False
    if result and result.is_dir():
        for path in result.rglob('*'):
            if (not path.is_file() or path.is_symlink()
                    or not path.resolve().is_relative_to(result.resolve())
                    or any(part.startswith('.') for part in path.relative_to(result).parts)):
                continue
            if len(files) == 300:
                truncated = True
                break
            files.append(path)
        files.sort(key=lambda p: p.relative_to(result).as_posix())
    elif result and result.is_file():
        files = [result]
    body = [f'<h1>{_e(row["run_id"])}</h1>',
            f'<p class="mut">{_e(row.get("status", "Unknown"))} · {_e(row.get("target", ""))}</p>']
    links = []
    for source, title in ((row.get('ticket'), 'Ticket'), (row.get('runtime'), 'Receipt')):
        url = _source_url(source, root)
        if url:
            links.append(f'<a href="{_e(url)}" target="_blank" rel="noopener">{title} ↗</a>')
    body.append('<div class="links">' + ''.join(links) + '</div>')
    if row.get('outcome'):
        body.append('<p>' + _e(row['outcome']) + '</p>')
    for finding in row.get('audit', []):
        body.append('<p class="mut">' + _e(finding) + '</p>')
    rendered = 0
    file_links = []
    for path in files:
        url = _source_url(path, root)
        label = path.relative_to(result).as_posix() if result.is_dir() else path.name
        file_links.append('<li>' + (f'<a href="{_e(url)}" target="_blank" rel="noopener">{_e(label)}</a>'
                                  if url else _e(label) + ' · outside the served root') + '</li>')
        if not url or path == row.get('runtime') or rendered >= 12:
            continue
        inner = ''
        if path.suffix.lower() in {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'}:
            inner = f'<img loading="lazy" src="{_e(url)}" alt="{_e(label)}" style="max-width:100%;height:auto">'
        elif path.suffix.lower() in {'.csv', '.tsv'}:
            inner = _csv_view(path)
        elif path.suffix.lower() in {'.md', '.txt', '.json', '.yaml', '.yml'} and path.stat().st_size <= 200_000:
            text = path.read_text(encoding='utf-8', errors='replace')
            inner = _md_view(text) if path.suffix.lower() == '.md' else '<pre>' + _e(text) + '</pre>'
        if inner:
            body.append(f'<section class="doc"><h3>{_e(label)}</h3>{inner}</section>')
            rendered += 1
    if not rendered:
        body.append('<p class="mut">No Result preview yet. Available files are listed below.</p>')
    body.append('<h2>Files</h2><ul class="files">' + ''.join(file_links) + '</ul>')
    if truncated:
        body.append('<p class="mut">First 300 files shown.</p>')
    body.append('<details><summary>Result source</summary><code>' + _e(result or 'No Result recorded') + '</code></details>')
    return _RESULT_PAGE.format(title=_e(row['run_id']), body='\n'.join(body))
