"""Copy prompts select a real scope/Run without writing or allocating anything."""
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from live.outline_prompts import RunPrompts
from live.outline import plan_card, _logic_map
from live.runs import _status


def page_fixture(tmp_path):
    page = tmp_path / 'Page.md'
    page.write_text('# Page\n\n## Opening\nA question.\n\n## Content\n')
    outline = tmp_path / 'outline'
    outline.mkdir()
    (outline / 'Page-outline-v1.1.md').write_text('''# Plan
## C1 · First
### C1.P1 · First paragraph
- B1 · [Point] First point
  Draft: First draft.
## C2 · Second
### C2.P1 · Second paragraph
- B1 · [Point] Second point
  Draft: Second draft with <angle> & "quotes".
''')
    return page


def row(run, status='Waiting', target='C2.P1'):
    return dict(run_id=run, status=status, target=target, version='v002', step='s003',
                ticket=None, runtime=None, audit=[])


def test_paragraph_uses_global_index_and_only_selected_excerpt(tmp_path):
    page = page_fixture(tmp_path)
    records = [row('rp-struct-01', 'Done', 'Page'), row('rp-para-02_P02')]
    before = {p: p.read_bytes() for p in tmp_path.rglob('*') if p.is_file()}
    with patch('live.outline_prompts.local_runs', return_value=records):
        prompt = RunPrompts(page).prompt('paragraph', 'C2.P1')
    assert 'Run: rp-para-02_P02' in prompt
    assert 'Page-global P02' in prompt
    assert 'Version: v002' in prompt and 'Step: s003' in prompt
    assert 'Second draft' in prompt and 'First draft' not in prompt
    assert 'Blocker:' not in prompt
    assert {p: p.read_bytes() for p in tmp_path.rglob('*') if p.is_file()} == before


def test_ambiguous_open_runs_and_missing_structure_do_not_choose_or_allocate(tmp_path):
    page = page_fixture(tmp_path)
    with patch('live.outline_prompts.local_runs', return_value=[row('rp-sec-01', target='C2'), row('rp-sec-02', target='C2')]):
        prompt = RunPrompts(page).prompt('section', 'C2')
    assert 'Run selection is ambiguous: rp-sec-01, rp-sec-02' in prompt
    assert 'rp-struct-01 is not closed' in prompt
    assert not (tmp_path / 'runs').exists()


def test_new_run_prompt_and_structure_entry_without_mermaid(tmp_path):
    page = page_fixture(tmp_path)
    prompt = RunPrompts(page).prompt('structure')
    assert 'not allocated' in prompt
    assert 'rp-struct-NN' in prompt
    assert 'Copy structure prompt' in _logic_map(page)


def test_readonly_draft_has_copy_buttons_and_escaped_payload(tmp_path):
    page = page_fixture(tmp_path)
    rendered = plan_card(page, read_only=True, minimal=True)
    assert rendered.count('aria-label="Copy section prompt"') == 2
    assert rendered.count('aria-label="Copy paragraph prompt"') == 2
    assert '&lt;angle&gt; &amp; &quot;quotes&quot;' in rendered
    assert 'action: feedback' not in rendered


def test_ready_status_and_unknown_status_are_distinct(tmp_path):
    runtime = tmp_path / 'runtime.yaml'
    runtime.write_text('status: ready\n')
    assert _status(runtime, {'status': 'ready'}) == 'Ready'
    assert _status(runtime, {'status': 'garbled'}) == 'Held'


def test_duplicate_addresses_report_blocker_instead_of_selecting_run(tmp_path):
    page = page_fixture(tmp_path)
    plan = next((tmp_path/'outline').glob('*outline*'))
    plan.write_text(plan.read_text()+'\n### C2.P1 · Duplicate\n')
    prompt = RunPrompts(page).prompt('paragraph','C2.P1')
    assert 'Address blocker: duplicate paragraph identity' in prompt


def test_legacy_address_requires_frozen_scope_reconciliation(tmp_path):
    prompt = RunPrompts(page_fixture(tmp_path)).prompt('paragraph','C2.P1')
    assert 'Confirm it against the accepted Structure and frozen Run target before editing' in prompt


def test_workflow_map_lists_run_specs_and_keeps_controller_operations_separate(tmp_path):
    from live.runs import _workflow_map_rows, _workflow_map_html
    page = page_fixture(tmp_path)
    names = {row[0] for row in _workflow_map_rows(page)}
    assert names == {'structure', 'scratch', 'section-writing', 'paragraph-writing', 'evidence-item', 'delivery'}
    assert 'controller operations' in _workflow_map_html(page)
