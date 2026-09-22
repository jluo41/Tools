"""Revise view: one box per paragraph, pre-filled with its Draft, edited in place.

Each Save maps the box's lines onto the paragraph's Bullets, writes the changed
Draft fields into the selected Outline, and extends the paragraph's Revise Run
with a change ledger Step that Run Space renders as red/green cards. Tokens
guard against saving from a page rendered before someone else's edit.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from live.outline import plan_card, render, parse_outline, OutlineMixin
from live.outline_preview import read_drafts, bullet_token, record_token
from live.outline_revise import save_revise, split_sentences, box_text
from live.runs import local_runs, _page_writing_subspace
from live.runs import render as render_runs
from src.plan_shape import iter_plan_bullets

PLAN = '''# Plan
approved: ✅
## C1 · First
### C1.P1 · First paragraph
- B1 · [Point] First point
  Draft: First draft.
- B2 · [Point] Second point
  Draft: Second draft.
### C1.P2 · Second paragraph
- B1 · [Point] Third point
'''


def page_fixture(tmp_path):
    page = tmp_path / 'Page.md'
    page.write_text('# Page\n\n## Opening\nA question.\n\n## Content\n### 1 · First\nProse.\n')
    outline = tmp_path / 'outline'
    outline.mkdir()
    (outline / 'Page-outline-v1.1.md').write_text(PLAN)
    return page


def bullets(page, paragraph):
    plan = page.parent / 'outline' / 'Page-outline-v1.1.md'
    drafts = read_drafts(page)
    return [{'address': b['address'], 'bullet': bullet_token(b), 'record': record_token(drafts.get(b['address']))}
            for b in iter_plan_bullets(plan.read_text()) if b['address'].startswith(paragraph + '.')]


def payload(page, paragraph, text, **extra):
    return {'paragraph': paragraph, 'display': paragraph, 'text': text, 'bullets': bullets(page, paragraph), **extra}


def test_render_has_one_box_per_paragraph_prefilled_with_the_draft(tmp_path):
    page = page_fixture(tmp_path)
    body = plan_card(page, path_q='/Board/board.md', file_q='Page.md')
    assert body.count('<form class="revise-form"') == 2
    assert body.count('class="revise-box"') == 2
    assert 'data-paragraph="C1.P1"' in body and 'data-points="2"' in body
    assert '>First draft.\n\nSecond draft.</textarea>' in body
    assert 'data-paragraph="C1.P2"' in body and 'data-points="1"' in body
    assert '&quot;address&quot;:&quot;C1.P1.B1&quot;' in body
    assert 'data-revise-save' in body
    page_html = render('Page', parse_outline(page.read_text()), page, draft_mode='revise')
    assert 'data-draft-mode=revise' in page_html
    assert '<button type=button class="draft-mode-tab on" data-draft-mode=revise>Revise</button>' in page_html
    assert 'Revise · Page.interactive-writing.revise' in page_html


def test_read_only_host_shows_a_disabled_box_without_save(tmp_path):
    page = page_fixture(tmp_path)
    body = plan_card(page, read_only=True)
    assert 'data-revise-save' not in body and 'beforeunload' not in body
    assert body.count('class="revise-box"') == 2 and body.count(' disabled>') == 2
    assert save_revise(page, payload(page, 'C1.P1', 'x'), read_only=True) == (
        None, 'This host is read-only; Revise saves are disabled')


def test_save_maps_lines_to_bullets_and_opens_a_revise_run_with_a_ledger(tmp_path):
    page = page_fixture(tmp_path)
    result, err = save_revise(page, payload(page, 'C1.P1', 'First draft, sharpened.\nSecond draft.', why='Sharper claim.'))
    assert err is None, err
    assert result['run'] == 'rp-revise-01_C1.P1' and result['step'] == 's001'
    assert [c['address'] for c in result['changed']] == ['C1.P1.B1']
    assert result['text'] == 'First draft, sharpened.\n\nSecond draft.'
    drafts = read_drafts(page)
    assert drafts['C1.P1.B1']['text'] == 'First draft, sharpened.'
    assert drafts['C1.P1.B2']['text'] == 'Second draft.'
    assert result['bullets'][0]['record'] == record_token(drafts['C1.P1.B1'])
    plan = (tmp_path / 'outline' / 'Page-outline-v1.1.md').read_text()
    assert '  Draft: First draft, sharpened.\n' in plan and 'approved: ✅' in plan
    ledger = (tmp_path / 'results' / 'rp-revise-01_C1.P1' / 'v001.md').read_text()
    for needle in ('## Step s001', '#### Track changes', '##### R01 · wording', '###### Before\nFirst draft.\n',
                   '###### After\nFirst draft, sharpened.\n', '###### Why\nSharper claim.\n', '###### Decision\naccept\n'):
        assert needle in ledger, needle
    runtime = (tmp_path / 'results' / 'rp-revise-01_C1.P1' / 'runtime.yaml').read_text()
    assert 'mode: revise\n' in runtime and 'status: running\n' in runtime and 'target: C1.P1\n' in runtime
    assert 'interaction: human-revise' in (tmp_path / 'runs' / 'rp-revise-01_C1.P1.md').read_text()
    rows = {row['run_id']: row for row in local_runs(page)}
    assert rows['rp-revise-01_C1.P1']['status'] == 'Running'
    assert _page_writing_subspace(rows['rp-revise-01_C1.P1']) == 'Revise'
    space = render_runs(page, '', '')
    assert 'Revise · C1.P1' in space and 'class=track-card' in space and '<b>Decision</b><br>accept' in space


def test_extra_lines_join_the_last_bullet_and_missing_lines_clear(tmp_path):
    page = page_fixture(tmp_path)
    result, err = save_revise(page, payload(page, 'C1.P1', 'One.\nTwo.\nThree.'))
    assert err is None and [c['address'] for c in result['changed']] == ['C1.P1.B1', 'C1.P1.B2']
    assert read_drafts(page)['C1.P1.B2']['text'] == 'Two. Three.'
    result, err = save_revise(page, payload(page, 'C1.P1', 'Only one now.'))
    assert err is None and read_drafts(page)['C1.P1.B1']['text'] == 'Only one now.'
    assert 'C1.P1.B2' not in read_drafts(page)
    ledger = (tmp_path / 'results' / 'rp-revise-01_C1.P1' / 'v001.md').read_text()
    assert ledger.count('## Step s') == 2 and '##### R04 · deletion' in ledger and '###### After\n(removed)\n' in ledger
    # a first sentence for an undrafted paragraph gets its own Run number and a first-draft card
    result, err = save_revise(page, payload(page, 'C1.P2', 'A first sentence.'))
    assert err is None and result['run'] == 'rp-revise-02_C1.P2'
    assert '##### R01 · first draft' in (tmp_path / 'results' / 'rp-revise-02_C1.P2' / 'v001.md').read_text()


def test_stale_tokens_bad_payloads_and_no_op_saves(tmp_path):
    page = page_fixture(tmp_path)
    stale = payload(page, 'C1.P1', 'New.')
    assert save_revise(page, payload(page, 'C1.P1', 'Moved on.\nSecond draft.'))[1] is None
    _, err = save_revise(page, stale)
    assert 'changed in another editor' in err
    _, err = save_revise(page, {**payload(page, 'C1.P1', 'x'), 'bullets': bullets(page, 'C1.P2')})
    assert 'inside C1.P1' in err
    _, err = save_revise(page, {'paragraph': 'nope', 'text': '', 'bullets': []})
    assert 'C<n>.P<m>' in err
    _, err = save_revise(page, payload(page, 'C1.P1', '<!-- hidden -->'))
    assert 'prose' in err
    result, err = save_revise(page, payload(page, 'C1.P1', 'Moved on.\nSecond draft.'))
    assert err is None and result['changed'] == [] and result['run'] == ''
    assert not (tmp_path / 'results' / 'rp-revise-02_C1.P1').exists()


def test_post_action_revise_reaches_save_and_edit_actions_point_at_the_view(tmp_path):
    page = page_fixture(tmp_path)

    class Host(OutlineMixin):
        root = tmp_path

        def target(self, p):
            return ('Page.md', str(tmp_path))

    host = Host()
    body, err = host.plug_outline({'action': 'revise', **payload(page, 'C1.P1', 'Via POST.\nSecond draft.')})
    assert err is None and body['run'] == 'rp-revise-01_C1.P1'
    assert read_drafts(page)['C1.P1.B1']['text'] == 'Via POST.'
    _, err = host.plug_outline({'action': 'edit-preview'})
    assert 'Revise view' in err


def test_box_starts_from_page_sentences_when_no_draft_exists(tmp_path):
    page = page_fixture(tmp_path)
    page.write_text('# Page\n\n## Opening\nA question.\n\n## Content\n### 1 · First\n'
                    'Third point, already written on the Page. <!-- realizes: C1.P2.B1 -->\n')
    body = plan_card(page, path_q='/Board/board.md', file_q='Page.md')
    assert '>Third point, already written on the Page.</textarea>' in body
    same = payload(page, 'C1.P2', 'Third point, already written on the Page.')
    result, err = save_revise(page, same)
    assert err is None and result['changed'] == [] and result['text'] == 'Third point, already written on the Page.'
    result, err = save_revise(page, payload(page, 'C1.P2', 'Third point, rewritten on the Page.'))
    assert err is None and result['run'] == 'rp-revise-01_C1.P2'
    assert read_drafts(page)['C1.P2.B1']['text'] == 'Third point, rewritten on the Page.'
    ledger = (tmp_path / 'results' / 'rp-revise-01_C1.P2' / 'v001.md').read_text()
    assert '##### R01 · wording' in ledger
    assert '###### Before\nThird point, already written on the Page.\n' in ledger
    assert "the Page's own sentence where no Draft existed" in ledger


def test_sentences_get_their_own_lines_and_blank_lines_separate_points(tmp_path):
    assert split_sentences('First claim. Second claim, e.g. with Dr. Smith (p. 3.5)! Third? Done.') == [
        'First claim.', 'Second claim, e.g. with Dr. Smith (p. 3.5)!', 'Third?', 'Done.']
    assert split_sentences('Cited \\cite{a.b} here. Next.') == ['Cited \\cite{a.b} here.', 'Next.']
    assert box_text(['One. Uno.', '', 'Two.']) == 'One.\nUno.\n\nTwo.'
    page = page_fixture(tmp_path)
    save_revise(page, payload(page, 'C1.P1', 'First one. First two.\n\nSecond draft.'))
    assert read_drafts(page)['C1.P1.B1']['text'] == 'First one. First two.'
    body = plan_card(page)
    assert '>First one.\nFirst two.\n\nSecond draft.</textarea>' in body
    result, err = save_revise(page, payload(page, 'C1.P1', 'First one.\nFirst two, edited.\n\nSecond draft.'))
    assert err is None and [c['address'] for c in result['changed']] == ['C1.P1.B1']
    assert read_drafts(page)['C1.P1.B1']['text'] == 'First one. First two, edited.'
    assert result['text'] == 'First one.\nFirst two, edited.\n\nSecond draft.'
