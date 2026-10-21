"""Revise view: one box per paragraph, pre-filled with its Draft, edited in place.

Each Save maps the box's lines onto the paragraph's Bullets and writes the changed
Draft fields into the selected Outline. The first Save opens the paragraph's
Revise run (one ticket keeping the text before); later Saves change only the
Draft; close-run writes the change ledger the All-runs view draws as red/green
cards (JL 260928: records at the two ends). Tokens guard against saving from a
page rendered before someone else's edit.
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
from src.run_lifecycle import close_run
from src.run_folders import find_ticket, result_dir  # noqa: E402  one folder per Run (0.125)
import re

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
    assert '>First draft.\nSecond draft.</textarea>' in body    # each sentence a row (JL 261020)
    assert 'data-paragraph="C1.P2"' in body and 'data-points="1"' in body
    assert '&quot;address&quot;:&quot;C1.P1.B1&quot;' in body
    assert 'class="revise-status"' in body  # no Save button: a box saves when you leave it (JL 261020)
    page_html = render('Page', parse_outline(page.read_text()), page, draft_mode='revise')
    assert 'data-draft-mode=revise' in page_html
    assert '<button type=button class="draft-mode-tab on" data-draft-mode=revise>Revise</button>' in page_html
    assert 'Page.interactive-writing.revise' not in page_html  # no explanation note (JL 260927)


def test_read_only_host_shows_a_disabled_box_without_save(tmp_path):
    page = page_fixture(tmp_path)
    body = plan_card(page, read_only=True)
    assert 'class="revise-status"' not in body and 'beforeunload' not in body
    assert body.count('class="revise-box"') == 2 and body.count(' disabled>') == 2
    assert save_revise(page, payload(page, 'C1.P1', 'x'), read_only=True) == (
        None, 'This host is read-only; Revise saves are disabled')


def test_save_maps_lines_to_bullets_and_opens_a_revise_run_with_a_ledger(tmp_path):
    page = page_fixture(tmp_path)
    result, err = save_revise(page, payload(page, 'C1.P1', 'First draft, sharpened.\nSecond draft.', why='Sharper claim.'))
    assert err is None, err
    run = result['run']
    assert re.fullmatch(r'run-revise-c1-p1', run) and result['name'] == run
    assert [c['address'] for c in result['changed']] == ['C1.P1.B1']
    assert result['text'] == 'First draft, sharpened.\nSecond draft.'
    drafts = read_drafts(page)
    assert drafts['C1.P1.B1']['text'] == 'First draft, sharpened.'
    assert drafts['C1.P1.B2']['text'] == 'Second draft.'
    assert result['bullets'][0]['record'] == record_token(drafts['C1.P1.B1'])
    plan = (tmp_path / 'outline' / 'Page-outline-v1.1.md').read_text()
    # a saved Bullet is written Draft-first; an undrafted one keeps its point on the dash line
    assert '- B1 · First draft, sharpened.\n  Point: [Point] First point\n' in plan and 'approved: ✅' in plan
    assert '- B1 · [Point] Third point\n' in plan and 'Draft:' not in plan
    # while open: one ticket (with the text before), no results/ and no log line
    ticket = find_ticket(tmp_path, run).read_text()
    assert 'status: open' in ticket and 'target: C1.P1' in ticket and 'C1.P1.B1 · First draft.' in ticket
    assert not (tmp_path / 'results').exists()
    rows = {row['run_id']: row for row in local_runs(page)}
    assert rows[run]['status'] == 'Running'
    assert _page_writing_subspace(rows[run]) == 'Revise'
    # close: the ledger, the runtime and one log line
    closed = close_run(page, run)
    assert closed['changes'] == 1
    ledger = (result_dir(tmp_path, run) / 'v001.md').read_text()
    for needle in ('## Step s001', '#### Track changes', '##### R01 · wording', '###### Before\nFirst draft.\n',
                   '###### After\nFirst draft, sharpened.\n', '###### Why\nSharper claim.\n', '###### Decision\naccept\n'):
        assert needle in ledger, needle
    runtime = (result_dir(tmp_path, run) / 'runtime.yaml').read_text()
    assert 'mode: revise\n' in runtime and 'status: complete\n' in runtime and 'target: C1.P1\n' in runtime
    assert 'status: closed' in find_ticket(tmp_path, run).read_text()
    assert run + ' closed' in (tmp_path / 'outline' / 'records' / 'Page-log.md').read_text()
    space = render_runs(page, '', '')
    assert 'Revise · C1.P1' in space and 'class=track-card' in space and '<b>Decision</b><br>accept' in space


def test_extra_lines_join_the_last_bullet_and_missing_lines_clear(tmp_path):
    page = page_fixture(tmp_path)
    result, err = save_revise(page, payload(page, 'C1.P1', 'One.\nTwo.\nThree.'))
    assert err is None and [c['address'] for c in result['changed']] == ['C1.P1.B1', 'C1.P1.B2']
    first = result['run']
    assert read_drafts(page)['C1.P1.B2']['text'] == 'Two. Three.'
    result, err = save_revise(page, payload(page, 'C1.P1', 'Only one now.'))
    assert err is None and read_drafts(page)['C1.P1.B1']['text'] == 'Only one now.'
    assert result['run'] == first                     # the open run continues
    assert 'C1.P1.B2' not in read_drafts(page)
    close_run(page, first)
    ledger = (result_dir(tmp_path, first) / 'v001.md').read_text()
    assert '###### Before\nFirst draft.\n\n###### After\nOnly one now.\n' in ledger
    assert '##### R02 · deletion' in ledger and '###### After\n(removed)\n' in ledger
    # a first sentence for an undrafted paragraph opens its own run and closes as a first draft
    result, err = save_revise(page, payload(page, 'C1.P2', 'A first sentence.'))
    assert err is None and re.fullmatch(r'run-revise-c1-p2', result['run'])
    close_run(page, result['run'])
    assert '##### R01 · first draft' in (result_dir(tmp_path, result['run']) / 'v001.md').read_text()


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
    assert not (tmp_path / 'results').exists()        # records wait for close


def test_post_action_revise_reaches_save_and_edit_actions_point_at_the_view(tmp_path):
    page = page_fixture(tmp_path)

    class Host(OutlineMixin):
        root = tmp_path

        def target(self, p):
            return ('Page.md', str(tmp_path))

    host = Host()
    body, err = host.plug_outline({'action': 'revise', **payload(page, 'C1.P1', 'Via POST.\nSecond draft.')})
    assert err is None and body['run'].startswith('run-revise-')
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
    assert err is None and result['run'].startswith('run-revise-')
    assert read_drafts(page)['C1.P2.B1']['text'] == 'Third point, rewritten on the Page.'
    close_run(page, result['run'])
    ledger = (result_dir(tmp_path, result['run']) / 'v001.md').read_text()
    assert '##### R01 · wording' in ledger
    assert '###### Before\nThird point, already written on the Page.\n' in ledger
    assert "the Page's own sentence where no Draft existed" in ledger


def test_sentences_split_and_a_point_keeps_its_run_of_sentences(tmp_path):
    assert split_sentences('First claim. Second claim, e.g. with Dr. Smith (p. 3.5)! Third? Done.') == [
        'First claim.', 'Second claim, e.g. with Dr. Smith (p. 3.5)!', 'Third?', 'Done.']
    assert split_sentences('Cited \\cite{a.b} here. Next.') == ['Cited \\cite{a.b} here.', 'Next.']
    assert box_text(['One. Uno.', '', 'Two.']) == 'One.\nUno.\nTwo.'
    page = page_fixture(tmp_path)
    save_revise(page, payload(page, 'C1.P1', 'First one. First two.\n\nSecond draft.'))
    assert read_drafts(page)['C1.P1.B1']['text'] == 'First one. First two.'
    body = plan_card(page)
    assert '>First one.\nFirst two.\nSecond draft.</textarea>' in body
    result, err = save_revise(page, payload(page, 'C1.P1', 'First one.\nFirst two, edited.\n\nSecond draft.'))
    assert err is None and [c['address'] for c in result['changed']] == ['C1.P1.B1']
    assert read_drafts(page)['C1.P1.B1']['text'] == 'First one. First two, edited.'
    assert result['text'] == 'First one.\nFirst two, edited.\nSecond draft.'


DRAFT_FIRST = '''# Plan
approved: ✅
## C1 · First
### C1.P1 · First paragraph
- B1 · S1 · Physicians treating comparable patients decide differently.
  Point: [Problem] Comparable patients can receive different decisions.
  Note: Opens with the phenomenon.
  Evidence: none · paper-owned framing
- B2 · S2 · [Gap] Interpersonal orientation is underexamined.
  Note: Not drafted yet.
'''


def test_draft_first_bullets_read_like_classic_ones_and_survive_a_save(tmp_path):
    from src.plan_shape import canonical_plan, split_bullet_block, render_bullet
    classic = canonical_plan(DRAFT_FIRST)
    assert ('- B1 · S1 · [Problem] Comparable patients can receive different decisions.\n'
            '  Note: Opens with the phenomenon.\n  Evidence: none · paper-owned framing\n'
            '  Draft: Physicians treating comparable patients decide differently.\n') in classic
    assert canonical_plan(classic) == classic
    assert '- B2 · S2 · [Gap] Interpersonal orientation is underexamined.\n  Note: Not drafted yet.' in classic
    # the round trip back to Draft-first is exact
    lines = DRAFT_FIRST.splitlines()
    assert render_bullet(*split_bullet_block(lines[4], lines[5:8])) == lines[4:8]
    page = page_fixture(tmp_path)
    plan = tmp_path / 'outline' / 'Page-outline-v1.1.md'
    plan.write_text(DRAFT_FIRST)
    blocks = {b['address']: b for b in iter_plan_bullets(plan.read_text())}
    assert blocks['C1.P1.B1']['head'] == 'S1 · [Problem] Comparable patients can receive different decisions.'
    assert blocks['C1.P1.B1']['draft'] == 'Physicians treating comparable patients decide differently.'
    assert blocks['C1.P1.B2']['draft'] == ''
    body = plan_card(page, path_q='/Board/board.md', file_q='Page.md')
    assert '>Physicians treating comparable patients decide differently.</textarea>' in body
    result, err = save_revise(page, payload(page, 'C1.P1', 'Physicians decide differently.\n\nInterpersonal orientation is overlooked.'))
    assert err is None, err
    text = plan.read_text()
    assert ('- B1 · S1 · Physicians decide differently.\n'
            '  Point: [Problem] Comparable patients can receive different decisions.\n'
            '  Note: Opens with the phenomenon.\n  Evidence: none · paper-owned framing\n'
            '- B2 · S2 · Interpersonal orientation is overlooked.\n'
            '  Point: [Gap] Interpersonal orientation is underexamined.\n  Note: Not drafted yet.\n') in text
    assert 'Draft:' not in text


def test_outline_tidy_writes_draft_first_and_moves_old_versions_to_previous(tmp_path):
    import importlib.util
    from src.outline_version import latest_outline, find_version
    spec = importlib.util.spec_from_file_location('page_cli', Path(__file__).resolve().parents[1] / 'cli' / 'page.py')
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)
    page = page_fixture(tmp_path)
    outline = tmp_path / 'outline'
    (outline / 'Page-outline-v1.0.md').write_text('# old\n')
    (outline / 'Page-outline-v0.1.md').write_text('# older\n')
    (tmp_path / 'runs').mkdir(exist_ok=True)
    (tmp_path / 'runs' / 'rp-sec-01.sh').write_text('--plan "$PAGE_DIR/outline/Page-outline-v1.0.md"\n')
    (outline / 'Page-log.md').write_text('# log\n')
    (outline / 'Page-logic.mmd').write_text('flowchart TD\n')
    (tmp_path / 'runs' / 'rp-sec-02.sh').write_text('see outline/Page-log.md\n')
    dry = cli.outline_tidy(page, dry_run=True)
    assert dry['draft_first'] and dry['to_previous'] == ['Page-outline-v0.1.md', 'Page-outline-v1.0.md', 'Page-logic.mmd']
    assert dry['to_records'] == ['Page-log.md']
    assert (outline / 'Page-outline-v1.0.md').exists()
    result = cli.outline_tidy(page)
    assert sorted(result['moved']) == ['previous/Page-logic.mmd', 'previous/Page-outline-v0.1.md', 'previous/Page-outline-v1.0.md', 'records/Page-log.md']
    assert 'outline/records/Page-log.md' in (tmp_path / 'runs' / 'rp-sec-02.sh').read_text()
    assert sorted(p.name for p in outline.glob('*-outline-*.md')) == ['Page-outline-v1.1.md']
    assert result['repointed'] == 2
    assert 'outline/previous/Page-outline-v1.0.md' in (tmp_path / 'runs' / 'rp-sec-01.sh').read_text()
    assert latest_outline(outline, 'Page').name == 'Page-outline-v1.1.md'
    assert find_version(outline, 'Page-outline-v1.0.md') == outline / 'previous' / 'Page-outline-v1.0.md'
    text = (outline / 'Page-outline-v1.1.md').read_text()
    assert '- B1 · First draft.\n  Point: [Point] First point\n' in text and 'Draft:' not in text
    assert read_drafts(page)['C1.P1.B2']['text'] == 'Second draft.'
    again = cli.outline_tidy(page)
    assert again['draft_first'] is False and again['moved'] == []


def test_blank_lines_inside_a_multi_line_draft_survive_both_shapes():
    from src.plan_shape import draft_first_plan, canonical_plan
    classic = ('## C1 · A\n### C1.P1 · B\n- B1 · [Model] The model is stated.\n  Note: n\n'
               '  Draft: We estimate:\n  \n  $$\n  Y = X\n  $$\n')
    first = draft_first_plan(classic)
    assert first.startswith('## C1 · A\n### C1.P1 · B\n- B1 · We estimate:\n  \n  $$\n  Y = X\n  $$\n  Point: [Model] The model is stated.\n  Note: n')
    assert [b['draft'] for b in iter_plan_bullets(first)] == [b['draft'] for b in iter_plan_bullets(classic)] == ['We estimate:\n\n$$\nY = X\n$$']
    assert draft_first_plan(first) == first and canonical_plan(canonical_plan(first)) == canonical_plan(first)


def test_free_prose_goes_back_to_the_points_it_reads_like():
    """JL 261020: "How could we make the editing to be more easier and free style here?" The box is prose; a Save
    gives each point the run of sentences, in order, most like what it held, and drops nothing."""
    from live.outline_revise import _text_to_bullets
    pts = ['B1', 'B2', 'B3']
    old = ['Patients search online for a physician.', 'An agent names physicians itself.',
           'Earlier audits checked a few names by hand.']
    assert _text_to_bullets(' '.join(old), pts, old) == dict(zip(pts, old))
    added = _text_to_bullets(' '.join(old[:1] + ['A new idea sits here.'] + old[1:]), pts, old)
    assert added['B2'] == old[1] and added['B3'] == old[2] and 'A new idea sits here.' in added['B1']
    edited = _text_to_bullets(' '.join([old[0], 'An AI agent now names the physicians itself.', old[2]]), pts, old)
    assert edited['B2'] == 'An AI agent now names the physicians itself.' and edited['B3'] == old[2]
    dropped = _text_to_bullets(' '.join([old[0], old[2]]), pts, old)
    assert dropped == {'B1': old[0], 'B2': '', 'B3': old[2]}
    assert _text_to_bullets('One. Two. Three.', ['B1', 'B2'], ['', '']) == {'B1': 'One.', 'B2': 'Two. Three.'}
    # a row ends a sentence: a line typed without its full stop stays its own sentence
    assert _text_to_bullets('One\nTwo', ['B1', 'B2'], ['One.', 'Two.']) == {'B1': 'One', 'B2': 'Two'}
    # a ⟦pending⟧ mark alone is its own sentence, so it stays its own point (found on a JAMA IM Results draft)
    assert split_sentences('Overlap was low (Figure 1). ⟦pending T4: x times chance⟧.') == [
        'Overlap was low (Figure 1).', '⟦pending T4: x times chance⟧.']
    marks = ['Overlap was low (Figure 1).', '⟦pending T4: x times chance⟧.']
    assert _text_to_bullets(' '.join(marks), ['B1', 'B2'], marks) == {'B1': marks[0], 'B2': marks[1]}


SECTIONED = '''# Plan
approved: ⬜

## 1 · Structure · Bullet Point Table

### Structure Overview

- C1 · First
- C1.P1 · Opening
  → S1 to S3 · three points
- C1.P2 · Closing
  → S4 · one point

### C1.P1 · Opening
- B1 · S1 · [Point] One
- B2 · S2 · [Point] Two
- B3 · S3 · [Point] Three

### C1.P2 · Closing
- B1 · S4 · [Point] Four

## 2 · Scratch · What to write here

### C1.P1 · Opening

### C1.P2 · Closing

## 3 · Draft · Reading and Revise

### C1.P1 · Opening
- B1 · S1 · Patients search online for a physician.
- B2 · S2 · An agent names physicians itself.
- B3 · S3 · Earlier audits checked a few names by hand.

### C1.P2 · Closing
- B1 · S4 · We compared them.
'''


def sectioned_fixture(tmp_path):
    page = tmp_path / 'Page.md'
    page.write_text('# Page\n\n## Opening\nA question.\n')
    (tmp_path / 'outline').mkdir()
    (tmp_path / 'outline' / 'Page-outline-v1.1.md').write_text(SECTIONED)
    return page


def rows_payload(page, paragraph, rows):
    return {'paragraph': paragraph, 'display': paragraph, 'bullets': bullets(page, paragraph),
            'text': '\n'.join(r['text'] for r in rows), 'rows': rows}


def test_each_row_shows_its_sentence_id_and_a_new_row_gets_the_next_free_one(tmp_path):
    """JL 261020: "could we make each sentences to be auto generate the sentence id as well?" Each row carries its
    Bullet and shows its sentence id; a row the person makes is a new Bullet with the id before it plus a letter."""
    page = sectioned_fixture(tmp_path)
    body = plan_card(page, path_q='/Board/board.md', file_q='Page.md')
    assert '<div data-b="C1.P1.B2" data-s="S2">An agent names physicians itself.</div>' in body
    rows = [{'b': 'C1.P1.B1', 'text': 'Patients search online for a physician.'},
            {'b': 'C1.P1.B2', 'text': 'An agent names physicians itself.'},
            {'b': '', 'text': 'A new sentence typed after it.'},
            {'b': 'C1.P1.B3', 'text': 'Earlier audits checked a few names by hand. Then one more inside the row.'}]
    result, err = save_revise(page, rows_payload(page, 'C1.P1', rows))
    assert err is None, err
    assert [(r['s'], r['text']) for r in result['rows']] == [
        ('S1', 'Patients search online for a physician.'), ('S2', 'An agent names physicians itself.'),
        ('S2a', 'A new sentence typed after it.'), ('S3', 'Earlier audits checked a few names by hand.'),
        ('S3a', 'Then one more inside the row.')]
    assert [c['address'] for c in result['changed']] == ['C1.P1.B4', 'C1.P1.B5']
    plan = (tmp_path / 'outline' / 'Page-outline-v1.1.md').read_text()
    # the point in section 1 (for the person to rename), the sentence in section 3, never renumbered
    assert '- B2 · S2 · [Point] Two\n- B4 · S2a · [Added] A new sentence typed after it\n- B3 · S3 · [Point] Three' in plan
    assert '- B4 · S2a · A new sentence typed after it.\n- B3 · S3 · Earlier' in plan
    # sent again as shown: nothing changes, no second copy
    again, err = save_revise(page, rows_payload(page, 'C1.P1', [{'b': r['b'], 'text': r['text']} for r in result['rows']]))
    assert err is None and again['changed'] == []
    # rows that lost their ids, and two rows joined, still find their Bullets
    lost = [{'b': '', 'text': r['text']} for r in result['rows']]
    assert save_revise(page, rows_payload(page, 'C1.P1', lost))[0]['changed'] == []
    joined = [{'b': r['b'], 'text': r['text']} for r in result['rows']]
    joined[0]['text'] += ' ' + joined.pop(1)['text']
    assert save_revise(page, rows_payload(page, 'C1.P1', joined))[0]['changed'] == []
    # a deleted row empties its Bullet and keeps its slot
    gone, err = save_revise(page, rows_payload(page, 'C1.P1', [r for r in lost if not r['text'].startswith('Then')]))
    assert [(c['address'], c['text']) for c in gone['changed']] == [('C1.P1.B5', '')]


def test_a_new_paragraph_opens_on_one_empty_row_and_its_sentences_get_ids(tmp_path):
    """JL 261020: "How could I add a new paragraph?" `add-paragraph` puts an empty paragraph after one; its Revise
    form opens on one empty row, and what is typed there becomes its first Bullets."""
    from live.outline_revise import add_paragraph
    page = sectioned_fixture(tmp_path)
    result, err = add_paragraph(page, {'after': 'C1.P1'})
    assert err is None and result['paragraph'] == 'C1.P3'
    plan = (tmp_path / 'outline' / 'Page-outline-v1.1.md').read_text()
    assert '  → S1 to S3 · three points\n- C1.P3 · New paragraph\n- C1.P2 · Closing' in plan
    assert plan.count('### C1.P3 · New paragraph') == 3                     # sections 1, 2 and 3
    assert plan.index('### C1.P3') < plan.index('### C1.P2 · Closing')
    body = plan_card(page, path_q='/Board/board.md', file_q='Page.md')
    form = re.search(r'<form class="revise-form" data-paragraph="C1.P3".*?</form>', body, re.S).group(0)
    assert 'data-bullets="[]"' in form and 'class="revise-rows blank"' in form and '<div><br></div>' in form
    typed, err = save_revise(page, {'paragraph': 'C1.P3', 'display': 'C1.P3', 'bullets': [], 'text': 'x',
                                    'rows': [{'b': '', 'text': 'First new sentence. Second new one.'}]})
    assert err is None, err
    assert [(r['b'], r['s']) for r in typed['rows']] == [('C1.P3.B1', 'S3a'), ('C1.P3.B2', 'S3b')]
    assert save_revise(page, {'paragraph': 'C1.P9', 'bullets': [], 'text': '', 'rows': []})[1] == 'C1.P9 is not in the plan; reload'
    assert add_paragraph(page, {'after': 'C1.P9'}) == (None, 'C1.P9 is not in the plan; reload')


def test_an_empty_planned_point_takes_the_next_new_sentence_before_a_bullet_is_added(tmp_path):
    from live.outline_revise import _rows_to_bullets
    mapped, inserts = _rows_to_bullets([{'b': '', 'text': 'One. Two. Three.'}], ['P.B1', 'P.B2'], ['', ''])
    assert mapped == {'P.B1': 'One.', 'P.B2': 'Two.'} and inserts == [('P.B2', ['Three.'])]
    # a row naming a Bullet out of order is a copy, typed as new
    mapped, inserts = _rows_to_bullets([{'b': 'P.B2', 'text': 'B.'}, {'b': 'P.B1', 'text': 'A.'}], ['P.B1', 'P.B2'], ['A.', 'B.'])
    assert mapped == {'P.B1': '', 'P.B2': 'B.'} and inserts == [('P.B2', ['A.'])]


def test_a_save_waits_when_the_plan_and_the_text_disagree_on_a_sentence_id():
    # t01, 261020: a point put in after S2 took B3 and shifted the rest, so a save made the text's S3 into S2a.
    # A sentence's id in §3 must match its point's (the same B) in §1, or nothing is saved.
    from live.outline_revise import _id_clash
    good = ('# T\n\n## 1 · Structure\n\n### C1.P1 · One\n- B1 · S1 · [A] first\n- B2 · S2 · [B] second\n'
            '- B3 · S1a · [N] a new point, no sentence yet\n\n## 3 · Draft\n\n### C1.P1 · One\n'
            '- B1 · S1 · First.\n- B2 · S2 · Second.\n')
    assert _id_clash(good) == ''
    shifted = good.replace('- B2 · S2 · [B] second\n- B3 · S1a · [N] a new point, no sentence yet',
                           '- B2 · S1a · [N] a new point, no sentence yet\n- B3 · S2 · [B] second')
    assert 'C1.P1.B2 is S1a in the plan but S2 in the text' in _id_clash(shifted)
