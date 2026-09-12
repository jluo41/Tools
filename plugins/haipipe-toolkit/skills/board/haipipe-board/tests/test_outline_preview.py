"""Rehearsal drafts round-trip without changing approved Shape or Content."""
import sys
import tempfile
import unittest
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from live.outline import plan_card, _edit_plan_bullet, _PAGE
from live.outline_preview import (save_preview, read_previews, bullet_token,
                                  record_token, content_seeds, sentence_count, reader_prose)
from src.plan_shape import iter_plan_bullets

PLAN = '''# S-test · outline v1.1
approved: ✅ JL
## C1 · Introduction
### C1.P1 · Variation
- B1 · Physician behavior varies across clinical settings
  Note: compare equivalent encounters
  Evidence: none · illustrative planning fixture
- B2 · Encounters leave different room for judgment
  Note: define discretion
  Evidence: none · illustrative planning fixture
'''


class OutlinePreviewTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.page = Path(self.tmp.name) / 'S-test.md'
        self.page.write_text('# Test\n## Content\nExisting prose. <!-- realizes: C1.P1.B1,C1.P1.B2 -->\n')
        (self.page.parent / 'outline').mkdir()
        self.plan = self.page.parent / 'outline/S-test-outline-v1.1.md'
        self.plan.write_text(PLAN)
        self.token = bullet_token(iter_plan_bullets(PLAN)[0])

    def save(self, text, previous='missing', token=None):
        return save_preview(self.page, 'C1.P1.B1', text, token or self.token, previous)

    def test_roundtrip_preserves_approved_source_and_page(self):
        before = self.page.read_bytes(), self.plan.read_bytes()
        result, error = self.save('Physicians choose differently.\nA candidate for discussion.')
        self.assertIsNone(error)
        self.assertEqual(read_previews(self.page)['C1.P1.B1']['text'],
                         'Physicians choose differently. A candidate for discussion.')
        self.assertEqual(before, (self.page.read_bytes(), self.plan.read_bytes()))
        self.assertEqual(len(list(self.plan.parent.glob('*-outline-*'))), 1)
        second, error = self.save('Revised candidate.', result['record_token'])
        self.assertIsNone(error)
        self.assertEqual(second['text'], 'Revised candidate.')

    def test_concurrent_stale_edit_is_rejected_without_losing_saved_text(self):
        result, _ = self.save('First editor saved this.')
        _, error = self.save('Second editor would overwrite it.')
        self.assertIn('another editor', error)
        self.assertEqual(read_previews(self.page)['C1.P1.B1']['text'], result['text'])

    def test_bullet_edit_marks_preview_stale_and_rejects_old_form(self):
        result, _ = self.save('A candidate sentence.')
        _edit_plan_bullet(self.page, 'edit-bullet', 'C1.P1', 'B1',
                          'Physician choices depend on the clinical context')
        _, error = self.save('Stale form.', result['record_token'])
        self.assertIn('Bullet changed', error)
        self.assertIn('Bullet changed · review this draft', plan_card(self.page))

    def test_clear_is_saved_and_does_not_restore_content_seed(self):
        result, _ = self.save('Candidate.')
        self.save('', result['record_token'])
        self.assertEqual(read_previews(self.page)['C1.P1.B1']['text'], '')
        card = plan_card(self.page)
        self.assertNotIn('>Existing prose.</textarea>', card)

    def test_shared_realization_is_seeded_once_with_explicit_cross_reference(self):
        seeds = content_seeds(self.page)
        self.assertEqual(seeds['C1.P1.B1']['text'], 'Existing prose.')
        self.assertEqual(seeds['C1.P1.B2']['shared'], 'C1.P1.B1')
        card = plan_card(self.page)
        self.assertIn('Bullet &amp; Evidence', card)
        self.assertEqual(card.count('>Existing prose.</textarea>'), 1)
        self.assertIn('Read paragraph', card)

    def test_script_like_prose_is_escaped_in_form(self):
        self.save('</textarea><script>alert(1)</script>')
        card = plan_card(self.page)
        self.assertNotIn('<script>alert(1)</script>', card)
        self.assertIn('&lt;script&gt;', card)

    def test_unknown_address_does_not_create_draft(self):
        _, error = save_preview(self.page, 'C1.P9.B1', 'Text', self.token, 'missing')
        self.assertIsNotNone(error)
        self.assertEqual(read_previews(self.page), {})

    def test_reading_first_table_hides_editors_notes_and_plan_metadata(self):
        card = plan_card(self.page)
        self.assertEqual(card.count('<details class=preview-editor>'), 2)
        self.assertEqual(card.count('<details class=point-tools>'), 2)
        self.assertIn('<span class=preview-copy>Existing prose.</span>', card)
        self.assertIn('<details class=plan-details>', card)
        self.assertNotIn('<details class=preview-editor open', card)
        self.assertIn('data-preview-cancel', card)
        self.assertIn('title="C1.P1.B1">B1</span>', card)
        # Controls and annotations remain available; source is not discarded.
        self.assertIn('compare equivalent encounters', card)
        self.assertIn('data-bullet-edit=', card)

    def test_mobile_keeps_two_columns_and_metadata_is_folded(self):
        self.assertIn('grid-template-columns:minmax(0,2fr) minmax(0,3fr)', _PAGE)
        self.assertNotIn('.point-group{{grid-template-columns:minmax(0,1fr);', _PAGE)
        self.assertNotIn("content:'Content preview'", _PAGE)
        self.assertIn('<details class=page-details><summary>Page details</summary>', _PAGE)

    def test_sentence_span_is_not_a_repeated_paragraph_heading(self):
        self.plan.write_text(PLAN.replace('C1.P1 · Variation', 'C1.P1 · Variation · S1 to S6'))
        self.assertIn('<span class=mut>Variation</span></summary>', plan_card(self.page))
        self.assertIn('S1 to S6', self.plan.read_text())

    def test_section_rejects_multiple_sentences_without_writing(self):
        self.page.write_text('page-type: section\n## Content\n')
        _, error = self.save('First sentence. Second sentence.')
        self.assertIn('one sentence', error)
        self.assertEqual(read_previews(self.page), {})
        result, error = self.save('The estimate is 2.54 MME (95% CI, 1.2 to 3.4).')
        self.assertIsNone(error)
        self.assertEqual(sentence_count(result['text']), 1)

    def test_sentence_check_ignores_citations_abbreviations_and_placeholders(self):
        for value in [r'Dr. Smith reports a difference \\citep{Smith2020}.',
                      'Barnett et al. report a difference.',
                      'U.S. prescribing differs.',
                      '[E05-VALUE-estimate: 2.54 MME pending].']:
            self.assertEqual(sentence_count(value), 1, value)
        self.assertEqual(sentence_count('One point? Another point.'), 2)
        self.assertEqual(sentence_count('一个观点。另一个观点。'), 2)

    def test_section_does_not_seed_multisentence_or_shared_spans(self):
        self.page.write_text('page-type: section\n## Content\n'
            'One. Two. <!-- realizes: C1.P1.B1 -->\n'
            'Shared. <!-- realizes: C1.P1.B2,C1.P1.B3 -->\n'
            'Single. <!-- realizes: C1.P1.B4 -->\n')
        seeds = content_seeds(self.page)
        for address in ['C1.P1.B1', 'C1.P1.B2', 'C1.P1.B3']:
            self.assertEqual(seeds[address]['text'], '')
            self.assertTrue(seeds[address]['unmapped'])
        self.assertEqual(seeds['C1.P1.B4']['text'], 'Single.')

    def test_section_duplicate_realizations_need_remapping(self):
        self.page.write_text('page-type: section\n## Content\n'
            'One. <!-- realizes: C1.P1.B1 -->\n'
            'Two. <!-- realizes: C1.P1.B1 -->\n')
        self.assertTrue(content_seeds(self.page)['C1.P1.B1']['unmapped'])

    def test_explicit_function_tag_is_visible_beside_bullet(self):
        self.plan.write_text(PLAN.replace('B1 · Physician', 'B1 · [Phenomenon] Physician'))
        self.assertIn('<span class=point-label>[Phenomenon]</span><span class=point-statement>', plan_card(self.page))

    def test_reader_copy_hides_tex_without_changing_citation_source(self):
        prose = r'Physicians differ \citep{Barnett2017}.'
        self.save(prose)
        self.assertEqual(reader_prose(prose), 'Physicians differ.')
        self.assertIn('<span class=preview-copy>Physicians differ.</span>', plan_card(self.page))
        self.assertEqual(read_previews(self.page)['C1.P1.B1']['text'], prose)

    def test_reader_compacts_evidence_placeholder_but_editor_preserves_source(self):
        self.plan.write_text(PLAN.replace(
            '  Evidence: none · illustrative planning fixture',
            '  Evidence: E33-CITE-opioid-system-stakes · support system stakes\n'
            '  Accept: support the system-level claim',
            1,
        ))
        (self.plan.parent / 'S-test-evidence-items.md').write_text(
            '# Evidence Items\n\n'
            '### E33-CITE-opioid-system-stakes · C1.P1.B1 · system stakes\n'
            '- **Target**: C1.P1.B1\n'
            '- **Label**: SystemStakes\n'
            '- **Expected**: CITE · support system stakes\n'
            '- **Acceptance**: support the system-level claim\n'
            '- **Verified**: ⬜\n'
            '- **Decide**: ☐ make\n'
        )
        self.token = bullet_token(iter_plan_bullets(self.plan.read_text())[0])
        prose = ('Decisions affect patients and systems '
                 '[E33-CITE-opioid-system-stakes: source verification pending].')
        result, _ = self.save(prose)
        for source, tail in [
            (prose, 'source verification pending].</textarea>'),
            ('Decisions affect patients and systems '
             '[E33-CITE-opioid-system-stakes pending].',
             'opioid-system-stakes pending].</textarea>'),
        ]:
            if source != prose:
                result, _ = self.save(source, result['record_token'])
            card = plan_card(self.page)
            self.assertIn('(E33C.SystemStakes)', card)
            self.assertNotIn('class="evtag warn preview-evidence"', card)
            resting = re.findall(r'<span class=preview-copy>(.*?)</span></summary>', card)
            self.assertTrue(resting)
            self.assertNotIn('[E33-CITE-opioid-system-stakes', ' '.join(resting))
            self.assertIn(tail, card)
            self.assertEqual(read_previews(self.page)['C1.P1.B1']['text'], source)
