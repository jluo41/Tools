"""Copy prompts select a real scope/Run without writing or allocating anything."""
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from live.outline_prompts import RunPrompts
from live.outline import plan_card, _structure_map
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
    assert prompt.startswith('/haipipe-page run-paragraph C2.P1 (Page-global P02)')
    assert 'Run: rp-para-02_P02 · Waiting · v002 · s003' in prompt
    assert 'Next: resume' in prompt
    assert 'Second draft' in prompt and 'First draft' not in prompt
    assert 'Blocker:' not in prompt
    assert prompt.rstrip().endswith('Feedback:')
    assert {p: p.read_bytes() for p in tmp_path.rglob('*') if p.is_file()} == before


def test_prompts_are_short(tmp_path):
    page = page_fixture(tmp_path)
    with patch('live.outline_prompts.local_runs', return_value=[row('rp-struct-01', 'Done', 'Page')]):
        prompts = RunPrompts(page)
        structure = prompts.prompt('structure')
        section = prompts.prompt('section', 'C2')
        paragraph = prompts.prompt('paragraph', 'C2.P1')
    # The contract is the skill's to state; the prompt names the door, the
    # addresses, the Run and the next move, then leaves a Feedback line.
    for text in (structure, section):
        assert len(text.splitlines()) <= 9, text
        assert 'Selected Outline' not in text
    assert len(paragraph.splitlines()) <= 14, paragraph
    for word in ('Owner Skill', 'Worker Skill', 'Prerequisites', 'Space affordance', 'Bounded work'):
        assert word not in structure + section + paragraph


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
    assert prompt.startswith('/haipipe-page run-structure Page')
    assert 'Run: none yet' in prompt
    assert 'rp-struct-NN' in prompt
    top = _structure_map(page)
    assert 'aria-label="Copy run-structure prompt"' in top
    assert '>⧉ run-structure<' in top
    assert 'structure-card' in top and 'Second paragraph' in top
    assert 'Mermaid' not in top


def test_readonly_draft_has_copy_buttons_and_escaped_payload(tmp_path):
    page = page_fixture(tmp_path)
    rendered = plan_card(page, read_only=True, minimal=True)
    assert rendered.count('aria-label="Copy run-section prompt"') == 2
    assert rendered.count('aria-label="Copy run-paragraph prompt"') == 2
    assert '>⧉ run-section<' in rendered and '>⧉ run-paragraph<' in rendered
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
    assert names == {'structure', 'scratch', 'section-writing', 'paragraph-writing', 'evidence-item', 'delivery', 'revise'}
    assert 'controller operations' in _workflow_map_html(page)
