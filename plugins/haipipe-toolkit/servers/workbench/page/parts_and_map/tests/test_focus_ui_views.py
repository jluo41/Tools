"""UI views: the Block, Job and Task UI matrices, live examples, walks and the Skills rail."""
import re
import json
import unittest

import sys
from pathlib import Path
from host_paths import bootstrap

bootstrap()

from live import focus_page, frame  # noqa: E402

sys.path.insert(0, str(next(d for d in Path(__file__).resolve().parents if d.name == "workbench") / "tests"))  # shared fixtures
import focus_page_fixtures as fixtures  # noqa: E402


class FocusPageTest(fixtures.FocusPageCase):
    def test_a_theme_block_report_shows_its_block_job_and_task_ui_live(self):
        """JL 261031: "I think you should have these as well ... the block UI, job UI and task UI"."""
        job = self.block / 'j01_x'
        job.mkdir(exist_ok=True)
        rel = job.relative_to(self.root).as_posix()
        (self.block / 'board.md').write_text('# b01\n\ntheme: paper\nui-block: http://example.org/board?a=1&b=2\n'
                                             f'ui-job: {rel}\nui-task: javascript:alert(1)\n\n## Purpose\n\nOne line.\n')
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'report')
        bar = ' '.join(fixtures.view_names(page))                       # Main, then its own views' buttons (JL 261124)
        self.assertLess(bar.index('Questions') if 'Questions' in bar else -1, bar.index('Block UI'))
        self.assertLess(bar.index('Block UI'), bar.index('Job UI'))
        self.assertLess(bar.index('Job UI'), bar.index('Task UI'))
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'report', 'ui-block')
        self.assertNotIn('data-src="http://example.org', page)          # another server: no blank frame (261106)
        self.assertIn('lives on another server', page)
        self.assertIn('href="http://example.org/board?a=1&amp;b=2"', page)
        self.assertIn('1 · 🖥️ The page, live', page)                  # a numbered section like every view (261105)
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'report', 'ui-job')
        self.assertRegex(page, r'<iframe class="ui-page" title="Job UI[^"]*"[^>]*src="[^"]*path=' + re.escape(rel.replace('/', '%2F')))
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'report', 'ui-task')
        self.assertNotIn('src="javascript', page)                         # only http(s) or a page of this SPACE
        self.assertIn('is not a page here', page)

    def test_ui_matrix_turns_types_into_columns_and_says_a_shared_row_once(self):
        source = self.block / 'matrix.md'
        source.write_text('| Category | Block Type | Use Cases | MindMap | Status |\n|---|---|---|---|---|\n'
                          '| Work | Data | Pipelines | Sources<br>Pipeline | Jobs |\n'
                          '| Work | Models | Experiments | Questions | Runs |\n'
                          '| CoWork | Coordination | Requests | Roles | Waiting |\n'
                          '| All | Around | — | Studio<br>Files | Studio<br>Files |\n')
        html = focus_page.ui_matrix_html(source, self.root)
        self.assertIn('style="--ui-type-count:3"', html)                      # only real types reserve horizontal space
        self.assertIn('<colgroup><col class="ui-view-column"><col><col><col></colgroup>', html)
        self.assertIn('<th class="ui-category" colspan="2">Work</th>', html)   # adjacent types share their category
        self.assertIn('<th class="ui-category" colspan="1">CoWork</th>', html)
        self.assertEqual(html.count('class="ui-block-type"'), 3)               # a column per type
        self.assertIn('<th class="ui-view" scope="row">Use Cases</th><td>Pipelines</td><td>Experiments</td>', html)
        self.assertIn('Sources<br>Pipeline', html)
        self.assertEqual(html.count('class="ui-span" colspan="3"'), 1)          # the shared row, said once across them
        self.assertNotIn('<td>Around</td>', html)

    def test_ui_type_matrix_is_opt_in_and_scoped_to_its_level(self):
        job = self.block / 'j01_example'
        job.mkdir()
        rel = job.relative_to(self.root).as_posix()
        (self.block / 'board.md').write_text(f'# Example\nui-block: {rel}\nui-job: {rel}\n')
        ui = self.block / 'ui'
        ui.mkdir()
        (ui / 'block-views.md').write_text('| Block Type | MindMap | Status | Findings |\n'
                                         '|---|---|---|---|\n| Theme building | Structure | Design | Rules |\n')
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'report', 'ui-block')
        self.assertIn('1 · 📋 Block Type × View Button', page)
        self.assertIn('<h2>📐 Design</h2>', page)            # bands like Main, each numbering from 1 (JL 261125)
        self.assertIn('<h2>🖥️ Pages</h2>', page)
        self.assertIn('1 · 🖥️ The page, live', page)
        self.assertIn('class="pb-tabset pb-side"', page)     # one example keeps the same left-list/right-preview layout
        self.assertIn('data-pbtab="fUBx0"', page)
        self.assertIn('data-pbpanel="fUBx0"', page)
        self.assertIn('🙋 Interaction', page)
        self.assertNotIn('3 · 🙋 Interaction', page)
        self.assertIn('<th>MindMap</th>', page)
        self.assertIn('Theme building', page)
        self.assertNotRegex(page, r'<details[^>]*\bopen\b[^>]*>\s*<summary[^>]*>1 · 📋')
        job_page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'report', 'ui-job')
        self.assertNotIn('Theme building', fixtures.band(job_page, 'ui-job'))
        self.assertIn('1 · 🖥️ The page, live', job_page)

    def test_matrix_help_uses_authored_view_context_and_escapes_content(self):
        source = self.block / 'job-views.md'
        source.write_text('| Category | Job Type | Findings |\n|---|---|---|\n'
                          '| Work | Data | Results<br>Skills |\n')
        (self.block / 'view-guide.json').write_text(json.dumps({
            'sections': {
                'Results': {'what': '<script>alert(1)</script>', 'outcome': 'A verified output.',
                            'layout': 'Left tabs · Right content', 'example': 'Show {result}.'},
                'Skills': {'what': 'Relevant skills.'}},
            'types': {'Data': {'result': 'a dataset'}},
            'skills': {'Findings': ['hai-{level} — Check the work.']}}))
        page = focus_page.ui_matrix_html(source, self.root)
        self.assertEqual(page.count('class="matrix-section"'), 2)
        self.assertIn('data-context="Job · Data · Findings"', page)
        self.assertIn('data-example="Show a dataset."', page)
        self.assertIn('hai-job — Check the work.', page)
        self.assertIn('data-layout="Left tabs · Right content"', page)
        self.assertIn('&lt;script&gt;alert(1)&lt;/script&gt;', page)
        self.assertNotIn('<script>alert(1)</script>', page)
        self.assertIn('aria-haspopup="dialog"', page)
        self.assertIn('aria-labelledby="matrix-help-job-views"', page)

    def test_matrix_examples_use_theme_view_routes_and_keep_default_routes(self):
        ui = self.block / 'ui'
        ui.mkdir()
        source = ui / 'block-views.md'
        source.write_text('| Category | Block Type | Story | Delivery | Findings |\n|---|---|---|---|---|\n'
                          '| Paper | Paper Board | Pitch | Outputs | Answers |\n')
        guide = {'sections': {key: {'what': key} for key in ('Pitch', 'Outputs', 'Answers')},
                 'examples': {'block': {'Paper Board': self.block.relative_to(self.root).as_posix()}},
                 'view_routes': {'Story': {'section': 'report', 'group': 'story'},
                                 'Delivery': {'section': 'delivery', 'group': ''}}}
        config = ui / 'view-guide.json'
        config.write_text(json.dumps(guide))
        html = focus_page.ui_matrix_html(source, self.root)
        self.assertIn('section=report&amp;group=story', html)
        self.assertIn('section=delivery&amp;group=', html)
        self.assertIn('section=report&amp;group=findings', html)
        guide['proposed'] = True
        config.write_text(json.dumps(guide))
        self.assertNotIn('data-url="/_board', focus_page.ui_matrix_html(source, self.root))

    def test_matrix_use_cases_are_metadata_and_do_not_shift_view_routes(self):
        ui = self.block / 'ui'
        ui.mkdir()
        source = ui / 'job-views.md'
        source.write_text('| Category | Job Type | Use Cases | Overview | Status |\n'
                          '|---|---|---|---|---|\n'
                          '| Work | Job | Goal<br>Model training | Goal | Tasks |\n')
        guide = {'sections': {'Goal': {'what': 'Goal'}, 'Tasks': {'what': 'Tasks'}},
                 'examples': {'job': {'Job': self.block.relative_to(self.root).as_posix()}}}
        (ui / 'view-guide.json').write_text(json.dumps(guide))
        html = focus_page.ui_matrix_html(source, self.root)
        self.assertIn('data-context="Job · Job · Use Cases"', html)
        cases = re.findall(r'<button[^>]*data-template=[^>]*>', html)
        self.assertEqual(len(cases), 2)
        self.assertTrue(all('data-url=' not in tag for tag in cases))
        self.assertIn('No linked examples yet.', html)
        self.assertIn('data-context="Job · Job · Overview"', html)
        self.assertIn('section=report&amp;group=overview', html)
        self.assertIn('section=report&amp;group=standing', html)

    def test_matrix_type_routes_keep_same_named_views_separate(self):
        ui = self.block / 'ui'
        ui.mkdir()
        source = ui / 'job-views.md'
        source.write_text('| Category | Job Type | Values | Display |\n|---|---|---|---|\n'
                          '| Paper | Version | Items | Preview |\n| Paper | Evidence | Items | — |\n')
        ref = self.block.relative_to(self.root).as_posix()
        guide = {'sections': {'Items': {'what': 'Values'}, 'Preview': {'what': 'Conditional'}},
                 'examples': {'job': {'Version': ref, 'Evidence': ref}},
                 'view_routes': {'Values': {'section': 'report', 'group': 'values'}},
                 'type_view_routes': {'job': {'Evidence': {'Values': {'group': 'value-list'}},
                                             'Version': {'Display': {'example': False}}}}}
        (ui / 'view-guide.json').write_text(json.dumps(guide))
        html = focus_page.ui_matrix_html(source, self.root)
        self.assertIn('section=report&amp;group=values', html)
        self.assertIn('section=report&amp;group=value-list', html)
        preview = re.search(r'<button[^>]*data-title="Preview"[^>]*>', html).group()
        self.assertIn('data-url=""', preview)

    def test_ui_proposal_is_opt_in_and_topics_keep_separate_panels(self):
        example = self.block / 'b90_example'
        example.mkdir()
        ref = example.relative_to(self.root).as_posix()
        before = focus_page.ui_view(ref, 'Block UI', self.root, self.block)
        self.assertNotIn('Work Structure', before)
        ui = self.block / 'ui'
        ui.mkdir()
        (ui / 'structure.md').write_text('Proposal\n\n## Overview\nGoal\n\n## Status\nSample only\n'
                                        '\n### Data <script>\nDataset check\n\n### Release\nPackaging\n')
        page = focus_page.ui_view(ref, 'Block UI', self.root, self.block)
        self.assertIn('1 · 🧭 Work Structure', page)
        self.assertNotIn('>Proposed<', page)                 # no state word on its bar (JL 261114)
        self.assertIn('data-pbtab="proposal-topic-30"', page)
        self.assertIn('data-pbpanel="proposal-topic-31" hidden', page)
        self.assertIn('Data &lt;script&gt;', page)
        self.assertNotIn('Data <script>', page)
        self.assertIn('1 · 🖥️ The page, live', page)

    def test_proposed_matrix_does_not_link_to_unimplemented_live_views(self):
        ui = self.block / 'ui'
        ui.mkdir()
        source = ui / 'block-views.md'
        source.write_text('| Category | Block Type | Overview |\n|---|---|---|\n| Work | Execution | Goal |\n')
        guide = {'sections': {'Goal': {'what': 'An intended outcome.'}},
                 'examples': {'block': {'Execution': self.block.relative_to(self.root).as_posix()}}}
        (ui / 'view-guide.json').write_text(json.dumps(guide))
        self.assertIn('data-url="/_board/workbench?', focus_page.ui_matrix_html(source, self.root))
        guide['proposed'] = True
        (ui / 'view-guide.json').write_text(json.dumps(guide))
        self.assertIn('data-url=""', focus_page.ui_matrix_html(source, self.root))

    def test_ui_example_type_names_the_tab_without_changing_its_page(self):
        example = self.block / 'b90_example'
        example.mkdir()
        (example / 'board.md').write_text('# Example\n')
        ref = example.relative_to(self.root).as_posix()
        ui = self.block / 'ui'
        ui.mkdir()
        (ui / 'example-types.json').write_text(json.dumps({'block': {ref: '📈 Statistical Analysis'}}))
        page = focus_page.ui_view(ref, 'Block UI', self.root, self.block)
        tab = re.search(r'<button[^>]*data-pbtab="fUBx0".*?</button>', page, re.S)[0]
        self.assertIn('📈 Statistical Analysis', tab)
        self.assertNotIn('b90_example', tab)
        self.assertIn('Block UI · b90_example', page)
        self.assertIn('Open b90_example', page)
        self.assertIn('path=' + ref.replace('/', '%2F'), page)
        job = focus_page.ui_view(ref, 'Job UI', self.root, self.block)
        self.assertNotIn('📈 Statistical Analysis', job)

    def test_a_tools_blueprint_names_its_example_from_the_tools_root_in_any_space(self):
        """261105: a Tools theme Block names its placeholder as `examples/...`; inside a SPACE, Tools sits at `Tools/`,
        so the path is found from the Block's own checkout and framed by its path from the SPACE root."""
        tools = self.root / 'Tools'
        block = tools / 'examples/Project-X/blueprint/b16_theme_x'
        example = tools / 'examples/Project-X/paper/Paper-Example'
        block.mkdir(parents=True)
        example.mkdir(parents=True)
        html = focus_page.ui_view('examples/Project-X/paper/Paper-Example', 'Block UI', self.root, block)
        self.assertRegex(html, r'<iframe class="ui-page" title="Block UI[^"]*"[^>]*src="[^"]*path=Tools%2Fexamples%2FProject-X%2Fpaper%2FPaper-Example')
        for bad in ('../outside', 'examples/../../outside', '/etc', 'examples/Project-X/paper/Missing'):
            self.assertIn('is not a page here', focus_page.ui_view(bad, 'Block UI', self.root, block), bad)

    def test_each_kind_of_page_at_a_level_is_a_side_tab(self):
        """JL 261105: "they are all the task, but different UI"; "for the paper's job, we might have different versions"."""
        a, b = self.block / 'j01_x' / 't01_items', self.block / 'j01_x' / 't02_meaning'
        a.mkdir(parents=True)
        b.mkdir()
        (a / 't01_items.md').write_text('# t01 · Items\ntask-type: labeling-items\n')
        (b / 't02_meaning.md').write_text('# t02 · Meaning\ntask-type: labeling-meaning\n')
        ra, rb = (p.relative_to(self.root).as_posix() for p in (a, b))
        (self.block / 'board.md').write_text(f'# b01\n\ntheme: labeling\nui-task: {ra}\nui-task: {rb}\n\n## Purpose\n\nOne line.\n')
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'report', 'ui-task')
        self.assertIn('1 · 🖥️ The pages, live', page)
        self.assertIn('t01_items', page)
        self.assertIn('labeling items', page)                          # each tab says its kind
        self.assertIn('t02_meaning', page)
        self.assertIn('labeling meaning', page)
        self.assertIn('pb-list', page)                                  # side tabs: the kind left, the page right
        (self.block / 'walks').mkdir()
        (self.block / 'walks' / 'task.html').write_text('<!doctype html>')      # only the first kind walked
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'report', 'ui-task')
        walks = page.split('2 · 🎬 Walkthroughs', 1)[1]                    # the same tabs, in the same order (261105)
        self.assertLess(walks.index('t01_items'), walks.index('t02_meaning'))
        self.assertIn('Not recorded', walks)

    def test_work_on_a_ui_view_says_what_each_kind_still_needs(self):
        """JL 261105: "so we should update the work as well for each tab of UI, right?"."""
        a, b = self.block / 'j01_x' / 't01_items', self.block / 'j01_x' / 't02_meaning'
        a.mkdir(parents=True)
        b.mkdir()
        ra, rb = (p.relative_to(self.root).as_posix() for p in (a, b))
        (self.block / 'board.md').write_text(f'# b01\n\ntheme: labeling\nui-task: {ra}\nui-task: {rb}\n\n## Purpose\n\nOne line.\n')
        (self.block / 'walks').mkdir()
        (self.block / 'walks' / 'task.html').write_text('<!doctype html>')          # the first kind's walk
        rv = self.block / 'topic' / 'review'
        rv.mkdir(parents=True)
        (rv / 'page-s2-r01.md').write_text(f'```text\npage     http://x/_board/workbench?path={ra} (Report)\n'
                                           'score    mean 6.0/10 · not yet\n```\n')
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'work', 'ui-task')
        self.assertNotIn('🎬 Walks to record', page)
        checklist = focus_page.ui_walk_checklist(self.block, self.root, 'ui-task')
        self.assertIn('t02_meaning', checklist)
        self.assertIn('Not recorded', checklist)
        self.assertIn('Recorded', checklist)
        self.assertIn('🔍 Review rounds', page)
        self.assertIn('6.0 of 10 · not yet', page)                                # t01's newest round
        self.assertIn('not reviewed yet', page)                                   # t02's

    def test_a_theme_block_shows_its_walk_under_the_live_page(self):
        """JL 261105: "could you embed the gif as the report as well?"; "a very quick video and we can pause"."""
        job = self.block / 'j01_x'
        job.mkdir(exist_ok=True)
        (self.block / 'walks').mkdir()
        (self.block / 'walks' / 'block.html').write_text('<!doctype html><title>walk</title>')
        rel = job.relative_to(self.root).as_posix()
        (self.block / 'board.md').write_text(f'# b01\n\ntheme: paper\nui-block: {rel}\nui-job: {rel}\n\n## Purpose\n\nOne line.\n')
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'report', 'ui-block')
        self.assertIn('2 · 🎬 Walkthroughs', page)                         # the second section, under the live page
        self.assertIn('walks/block.html', page)
        self.assertIn('🙋 Interaction', page)
        self.assertNotIn('3 · 🙋 Interaction', page)                       # then Interaction, last as on every view
        empty_walk = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'report', 'ui-job')
        self.assertIn('🎬 Walkthroughs', empty_walk)
        self.assertIn('Not recorded', empty_walk)

    def test_a_live_page_written_from_its_face_opens_on_any_server(self):
        """261106: a live page's url with no leading / is from its face's folder, so a SPACE's and Tools' own server
        both open it."""
        site = self.block / 'delivery' / 'web'
        site.mkdir(parents=True)
        (site / 'index.html').write_text('<!doctype html>')
        item = {'url': 'delivery/web/index.html', 'folder': self.block / 'j01_x', 'face': self.block}
        self.assertIn('b01_study/delivery/web/index.html', frame.live_url(item, self.root))
        self.assertEqual(frame.live_url({'url': 'https://example.org/x', 'folder': self.block}, self.root), 'https://example.org/x')
        self.assertEqual(frame.live_url({'url': 'delivery/none.html', 'folder': self.block}, self.root), 'delivery/none.html')

    def test_skills_is_a_rail_section_with_the_page_s_skills(self):
        """JL 261105: "a new tab in the right rail, named 'SKILL', and we can show the most relevent skills"."""
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'skills')
        self.assertIn('>🧰 Skills<', page)
        self.assertIn('Copy prompt', page)
        self.assertIn('/hai-work', page)                         # the theme's door first
        self.assertIn('/hai-block', page)                        # then the level's skill
        self.assertIn('Copy prompt', page)
        work = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'work')
        self.assertNotIn('Skills that do it', work)                  # shown once: the rail, not every view's Process


if __name__ == '__main__':
    unittest.main()
