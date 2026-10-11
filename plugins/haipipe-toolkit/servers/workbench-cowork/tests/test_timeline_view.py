"""Chronology, date precision, safe sources and opt-in integration."""
import datetime as dt
from pathlib import Path
from live import frame
from live.cowork_theme import THEME
from live.timeline_view import read_events, render_report, group_timeline

TABLE = '| Date | Track | Development | Kind | Source |\n|---|---|---|---|---|\n'


def write(path, body):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body)
    return path


def test_chronology_preserves_precision_and_unknown_dates(tmp_path):
    p = write(tmp_path / 'report.md', '# History\ntimeline-as-of: 2026-10-09\n' + TABLE +
              '| TBD | Work | Undated | target | |\n'
              '| 2026-12 | Work | Month target | target | |\n'
              '| 2026-10-09 | Work | Current | observed | |\n'
              '| 2026-05-18 | Work | First | recorded | |\n'
              '| 2026-06 | Work | Invalid history | recorded | |\n'
              '| 2026-02-30 | Work | Invalid date | recorded | |\n')
    d = read_events(p)
    assert [e['date'] for e in d['events']] == ['2026-05-18', '2026-10-09', '2026-12', 'TBD']
    assert d['asof'] == dt.date(2026, 10, 9)
    html = render_report(d, tmp_path)
    assert html.index('First') < html.index('Current snapshot ·') < html.index('Month target') < html.index('Undated')
    assert 'datetime="2026-12"' in html and 'datetime="2026-12-01"' not in html
    assert 'datetime="TBD"' not in html
    assert 'Dates not set' in html and 'data-tl-filter="Work"' in html
    assert '<h3 id="timeline-report-plans">Future targets</h3><section' in html


def test_table_inside_code_fence_does_not_become_real_history(tmp_path):
    p = write(tmp_path / 'report.md', '```md\n' + TABLE + '| 2026-05-18 | Work | Example | recorded | |\n```\n')
    assert read_events(p)['events'] == []


def test_content_escaped_and_sources_confined_to_workspace(tmp_path):
    root = tmp_path / 'space'
    write(tmp_path / 'outside.md', 'private')
    write(root / 'source.md', 'source')
    p = write(root / 'report.md', '# History\n' + TABLE +
              '| 2026-05-18 | <script> | <img src=x onerror=alert(1)> | recorded | '
              '[good](source.md) [escape](../outside.md) [bad](javascript:alert) [web](https://example.test/source) |\n')
    html = render_report(read_events(p), root)
    assert '<img' not in html and '&lt;img' in html
    assert 'javascript:' not in html and 'outside.md' not in html
    assert 'source.md' in html and 'https://example.test/source' in html


def test_only_selected_group_with_event_table_uses_chronology(tmp_path):
    block = tmp_path / 'Project/cowork/b01_demo'
    write(block / 'board.md', '# Demo\nboard-kind: cowork-block\n\n## Questions\n```yaml\nquestions:\n'
          '- id: Q01\n  title: History\n  group: Timeline\n  question: What changed?\n'
          '  work: []\n  report: reports/q01_history/q01_history.md\n```\n')
    p = write(block / 'reports/q01_history/q01_history.md', '# History\nanswers: Q01\nanswer-status: partial\n'
              + TABLE + '| 2026-05-18 | Work | Began | recorded | |\n')
    chronological = frame.spaces_for(THEME, 'Block', block, tmp_path, 'Timeline')['Audience Report'].html
    ordinary = frame.spaces_for(THEME, 'Block', block, tmp_path, 'All')['Audience Report'].html
    assert 'class=tl-native' in chronological and 'class=tl-native' not in ordinary
    p.write_text('# History\nanswers: Q01\nanswer-status: open\n')
    fallback = frame.spaces_for(THEME, 'Block', block, tmp_path, 'Timeline')['Audience Report'].html
    assert 'class=tl-native' not in fallback and 'What changed?' in fallback
    assert group_timeline(block, tmp_path, [{'group':'Timeline','report':'../../../outside.md'}], 'Timeline') == ''
