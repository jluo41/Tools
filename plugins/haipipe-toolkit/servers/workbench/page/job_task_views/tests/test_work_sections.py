"""A face's own sections (work_sections.py): ## Review Content and ## Findings replace the fixed work frame."""
import unittest

import sys
from pathlib import Path
from host_paths import bootstrap

bootstrap()

from live import focus_page, work_frame, work_sections  # noqa: E402

sys.path.insert(0, str(next(d for d in Path(__file__).resolve().parents if d.name == "workbench") / "tests"))  # shared fixtures
import focus_page_fixtures as fixtures  # noqa: E402


class WorkSectionsTest(fixtures.FocusPageCase):
    def own_block(self):
        src = self.block / 'src'
        src.mkdir()
        (src / 'week.md').write_text('# The week\n\n1. Monday: the logs.\n')
        (src / 'area-01-text.md').write_text('# ✍️ Paper text\n\n- A decision.\n')
        (src / 'area-02-ui.md').write_text('# 🖼️ Page layout\n\n- Another.\n')
        self.face.write_text('# Replay\nspine: Replay the week.\n\n## Review Content\n\n### 🎯 Goal\n\nReplay it.\n\n'
                             '### 🗓️ The week\n\nembed: src/week.md\n\n## Findings\n\neach: src/area-*.md\n\n'
                             '### ❓ Still open\n\n- One question.\n')
        return focus_page.read_face(self.block, self.root)

    def test_the_face_names_the_overview_sections(self):
        data = self.own_block()
        html = work_frame.overview(self.block, self.root, data, [], [])
        self.assertIn('1 · 🎯 Goal', html)
        self.assertIn('2 · 🗓️ The week', html)
        self.assertIn('Monday: the logs.', html)
        self.assertNotIn('Requirements', html)
        self.assertEqual(html.count('The week'), 1)          # the embedded file's own title is not printed twice

    def test_each_file_is_one_findings_section_in_order(self):
        titles = [t for t, _ in work_sections.declared(self.block, self.root, self.own_block(), 'findings')]
        self.assertEqual(titles, ['✍️ Paper text', '🖼️ Page layout', '❓ Still open'])

    def test_a_face_without_them_keeps_the_fixed_frame(self):
        data = focus_page.read_face(self.block, self.root)
        self.assertEqual(work_sections.view_html(self.block, self.root, data, 'overview', work_frame.section), '')
        self.assertIn('Requirements', work_frame.overview(self.block, self.root, data, [], []))

    def test_an_embed_outside_the_root_is_not_read(self):
        self.face.write_text('# R\n\n## Review Content\n\n### Out\n\nembed: ../../etc/hosts\n')
        ((_, body),) = work_sections.declared(self.block, self.root, focus_page.read_face(self.block, self.root), 'overview')
        self.assertNotIn('localhost', body)

    def test_a_design_section_is_its_own_view(self):
        # JL 261115: the person's high-level design, written in one file, as a view of the Block
        (self.block / 'design.md').write_text('# High-level design\n\nEach city is a page.\n')
        self.face.write_text('# R\n\n## Design\n\n### High-level design\n\nembed: design.md\n')
        ((title, body),) = work_sections.declared(self.block, self.root, focus_page.read_face(self.block, self.root), 'design')
        self.assertEqual(title, 'High-level design')
        self.assertIn('Each city is a page', body)

    def test_an_html_file_is_never_framed(self):
        (self.block / 'site.html').write_text('<p>site</p>')
        self.face.write_text('# R\n\n## Review Content\n\n### Site\n\nembed: site.html\n')
        ((_, body),) = work_sections.declared(self.block, self.root, focus_page.read_face(self.block, self.root), 'overview')
        self.assertNotIn('iframe', body)

    def test_an_entry_is_a_card_on_a_timeline(self):
        """JL 261114: the replay page's look in the workbench: chips, tinted blocks, phases on one vertical line."""
        self.face.write_text('# R\n\n## Findings\n\n### Log\n\n- **12:39 to 13:51 · Theory papers**\n  - What happened.\n'
                             '- **12:53** · A decision\n  - Decided: add them\n  - JL asked: why\n'
                             '  - Session: Main paper, t01 Intro\n- Plain line\n')
        html = work_sections.view_html(self.block, self.root, focus_page.read_face(self.block, self.root), 'findings',
                                       work_frame.section)
        self.assertIn('<ul class=ws-tl>', html)
        self.assertIn('<li class=ws-ph><details class=ws-card><summary><span class=ws-tm>12:39 to 13:51</span>'
                      '<span class=ws-ti>Theory papers</span>', html)
        self.assertIn('<span class=ws-tm>12:53</span><span class=ws-ti>A decision</span><span class=ws-chips>'
                      '<span class=ws-chip>Main paper</span><span class=ws-chip>t01 Intro</span>', html)
        self.assertIn('<div class="ws-blk dd"><span class=ws-ov>Decided</span><p>add them</p></div>', html)
        self.assertIn('<div class="ws-blk ask"><span class=ws-ov>Asked</span><p>why</p></div>', html)
        self.assertIn('<li class=ws-pt>Plain line</li>', html)
        self.assertEqual(html.count('<style>'), 1)

    def test_plan_and_results_sections_follow_the_jobs(self):
        job = self.block / 'j01_logs'
        job.mkdir()
        (job / 'j01_logs.md').write_text('# j01_logs · logs\nstate: ✅ DONE\ngoal: Read them.\n')
        (self.block / 'day-1.md').write_text('# 🗓️ Mon\n\n- A phase.\n')
        self.face.write_text('# R\n\n## Plan + Results\n\neach: day-*.md\n')
        html = work_frame.status(self.block, self.root, focus_page.read_face(self.block, self.root), [])
        self.assertIn('j01', html)
        self.assertRegex(html, r'<span class=bt>[2-9] · 🗓️ Mon')     # numbered on, after the Jobs
        self.assertLess(html.index('j01'), html.index('🗓️ Mon'))

    def test_an_svg_drawing_is_inline_and_cannot_run_script(self):
        (self.block / 'map.svg').write_text('<?xml version="1.0"?><svg onload="x()"><script>x()</script>'
                                            '<circle r="3"><title>12:53 · A</title></circle></svg>')
        self.face.write_text('# R\n\n## Review Content\n\n### 🗺️ The map\n\nembed: map.svg\n')
        ((_, body),) = work_sections.declared(self.block, self.root, focus_page.read_face(self.block, self.root), 'overview')
        self.assertIn('<title>12:53 · A</title>', body)
        self.assertNotIn('x()', body)                # the file's own script and handler are gone
        self.assertNotIn('onload', body)
        self.assertIn('#focus-viewer', body)         # a click on a station opens it in the workbench pop-out
        self.assertNotIn('<?xml', body)

    def test_a_header_collects_the_entries_after_it(self):
        """JL 261114 AI-eval: a day of 136 cards opens as its phases; each phase holds its own decisions."""
        self.face.write_text('# R\n\n## Findings\n\n### Day\n\n- A takeaway.\n- **📜 The decisions**\n'
                             '- **12:53** · First\n  - Decided: one\n- **13:03** · Second\n  - Decided: two\n')
        html = work_sections.view_html(self.block, self.root, focus_page.read_face(self.block, self.root), 'findings',
                                       work_frame.section)
        head = html.index('📜 The decisions')
        self.assertLess(html.index('<li class=ws-pt>A takeaway.</li>'), head)                 # the takeaway stays on top
        self.assertLess(head, html.index('<span class=ws-ti>First</span>'))       # the entries sit inside the header
        self.assertIn('<li class=ws-ph><details class=ws-card>', html)
        self.assertEqual(html.count('<details class=ws-card>'), 3)

    def test_a_row_state_is_its_mark_with_the_word_in_the_hover(self):
        """JL 261113: no state words on a page; marks show state, the word waits behind a hover."""
        from live.ui_parts import state_mark
        from live.state_marks import STATE_MARKS     # JL 261126: the Files pane's drawn marks, one table
        self.assertEqual(state_mark('✅ done'), f'<span class="st fx-done" title="done">{STATE_MARKS["done"]}</span>')
        self.assertEqual(state_mark('⬜ not run'), f'<span class="st fx-plan" title="not run">{STATE_MARKS["plan"]}</span>')
        self.assertEqual(state_mark('In progress'), f'<span class="st fx-edit" title="In progress">{STATE_MARKS["edit"]}</span>')
        self.assertEqual(state_mark('🙋 waiting for you'),
                         f'<span class="st fx-you" title="waiting for you">{STATE_MARKS["you"]}</span>')   # pings, no words
        self.assertEqual(state_mark('🆕 new'), f'<span class="st fx-new" title="new">{STATE_MARKS["new"]}</span>')
        self.assertEqual(state_mark('❗ void'), f'<span class="st fx-void" title="void">{STATE_MARKS["void"]}</span>')
        self.assertNotIn('✅', state_mark('✅ done'))          # drawn, never the emoji
        self.assertEqual(state_mark(''), '')

    def test_a_block_with_runs_draws_its_work_map(self):
        """JL 261114: every work Block's Overview has the transit map: a line per Job, a station per Run."""
        for job, task, run, when in (('j01_data', 't01_cut', 'r01_cut', '2026-11-05T10:00:00Z'),
                                     ('j02_fit', 't01_fit', 'r01_fit', '2026-11-06T11:00:00Z')):
            res = self.block / job / task / 'runs' / run / 'result'
            res.mkdir(parents=True)
            (res / 'runtime.yaml').write_text(f"status: completed\nstarted_at: '{when}'\n")
            (self.block / job / task / f'{task}.md').write_text(f'# {task}\nstate: ✅ DONE\n')
            (self.block / job / f'{job}.md').write_text(f'# {job}\ngoal: g\n')
        html = work_frame.overview(self.block, self.root, focus_page.read_face(self.block, self.root), [], [])
        self.assertIn('2 · 🗺️ Work map', html)
        self.assertIn('data-href="', html)             # a station opens its Run's page
        self.assertIn('Thu Nov 5', html)


if __name__ == '__main__':
    unittest.main()
