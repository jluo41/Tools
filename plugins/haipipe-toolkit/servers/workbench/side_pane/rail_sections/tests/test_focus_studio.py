"""Studio topics and sNN cards: groups, topic rows and links, delivery cards and buttons."""
import re
import unittest

import sys
from pathlib import Path
from host_paths import bootstrap

bootstrap()

from live import focus_page, frame  # noqa: E402

sys.path.insert(0, str(next(d for d in Path(__file__).resolve().parents if d.name == "workbench") / "tests"))  # shared fixtures
import focus_page_fixtures as fixtures  # noqa: E402


class FocusPageTest(fixtures.FocusPageCase):
    def test_studio_bands_contain_folds_once_in_authored_group_order(self):
        (self.block / '_studio_groups.txt').write_text('UI\nStructure\nEmpty\n')
        for name, tags in [('s01-first', ['Structure']), ('s03-third', ['UI']),
                           ('s02-second', ['Structure', 'UI']), ('s04-fourth', [])]:
            topic = self.block / name
            topic.mkdir()
            (topic / (name + '.md')).write_text('# ' + name + '\n**Tags:** ' +
                                                ', '.join('`' + tag + '`' for tag in tags) + '\n')
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'studio')
        bands = re.findall(r'<section class="studio-band".*?</section>', page, re.S)
        self.assertEqual(len(bands), 3)
        self.assertIn('>UI</h2>', bands[0])
        self.assertIn('>Structure</h2>', bands[1])
        self.assertIn('>Other</h2>', bands[2])
        self.assertLess(bands[0].index('id="s02-second"'), bands[0].index('id="s03-third"'))
        self.assertIn('id="s01-first"', bands[1])
        self.assertIn('id="s04-fourth"', bands[2])
        self.assertEqual(page.count('id="s02-second"'), 1)
        self.assertNotIn('>Empty</h2>', page)
        for band, count in zip(bands, (2, 1, 1)):
            self.assertEqual(band.count('<details class=band-sec>'), count)

    def test_studio_band_filter_keeps_secondary_tag_membership(self):
        (self.block / '_studio_groups.txt').write_text('UI\nStructure\n')
        topic = self.block / 's01-multi'
        topic.mkdir()
        (topic / 's01-multi.md').write_text('# Multi\n**Tags:** `UI`, `Structure`\n')
        page = focus_page.studio_html(focus_page.topic_rows(self.block, self.root), self.root,
                                      'Structure', tabs=True)
        self.assertIn('>Structure</h2>', page)
        self.assertNotIn('>UI</h2>', page)
        self.assertEqual(page.count('id="s01-multi"'), 1)

    def test_a_topic_folder_with_no_face_never_takes_the_page_down(self):
        # 261031 review: b11's s32-insight-element-ui/ held a drawing and a builder but no .md, and its Block's Report
        # (MindMap first) dropped the connection; a bare folder is no topic (is_topic), so the map skips it
        bare = self.block / 's32-element-ui'
        bare.mkdir()
        (bare / 'build_s32_element_ui.py').write_text('')
        (self.block / 'j01_work').mkdir()
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'report')
        self.assertIn('class="focus-map', page)
        self.assertFalse(focus_page.is_topic(bare))

    def test_an_sNN_beside_the_jobs_is_a_studio_card_with_no_page_of_its_own(self):
        # JL 261030: "we just have sNN, along side with jNN, to make it visible directly"
        topic = self.block / 's01-first'
        topic.mkdir()
        (topic / 's01-first.md').write_text('# s01 · First\n**Stage:** shaping\n')
        (self.block / 'j01_work').mkdir()
        self.assertTrue(focus_page.is_topic(topic))
        self.assertEqual(frame.topic_owner(topic), self.block)
        self.assertEqual(frame.topic_address(topic), 'b01-s01')
        self.assertEqual([p.name for p in focus_page.kids(self.block)], ['j01_work'])   # not taken for a Job
        studio = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'studio')
        self.assertIn('s01', studio)
        self.assertIn('first', studio)
        self.assertIn('<article class="studio-topic-content" id="s01-first">', studio)   # the card a link lands on
        home = focus_page.topic_home(topic, self.root)                  # JL 261031: the sNN page is retired
        self.assertIn('path=b01_study&layout=focus&section=studio', home)
        self.assertTrue(home.endswith('#s01-first'))
        page = focus_page.render(frame.Theme(name='work'), self.root, topic)   # an old link goes to the card
        self.assertIn('http-equiv="refresh"', page)
        rail = focus_page.render(frame.Theme(name='work'), self.root, self.block / 'j01_work')
        rail = rail.split('class="focus-rail left"', 1)[1].split('</nav>', 1)[0]
        self.assertIn(frame.esc(home), rail)                             # the left rail's sNN opens its card
        self.assertNotIn('studio-goal', studio)                    # no plain-text line in the fold (JL 261125)

    def test_a_block_studio_lists_its_own_sNN_in_order_each_named(self):
        # JL 261125: "we only have [s01 to s06] why we have so many these? could you just display these sNN?"
        for name, group in [('s02-second', 'Beta'), ('s01-first', 'Alpha')]:
            topic = self.block / name
            topic.mkdir()
            (topic / (name + '.md')).write_text(f'# {name[:3]} · {name[4:]}\n**Tags:** {group}\n')
        inner = self.block / 'j01_x' / 't01_y' / 's51-inner'
        inner.mkdir(parents=True)
        (inner / 's51-inner.md').write_text('# s51 · inner\n')
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'studio')
        main = page[page.index('<div class="studio-master">'):]
        self.assertLess(main.index('id="s01-first"'), main.index('id="s02-second"'))   # sNN order, not groups
        self.assertIn('<span class=bt>s01 · 🎨 First', main)                              # each row names its sNN
        self.assertNotIn('s51-inner', main)                                              # a Task's topic stays on its page
        self.assertNotIn('class="section-views', page[page.index('<main'):])             # one list, no group buttons
        task = focus_page.render(frame.Theme(name='work'), self.root, self.block / 'j01_x' / 't01_y', 'studio')
        self.assertIn('id="s51-inner"', task)

    def test_every_section_shows_its_views_above_the_purpose_and_no_count_line(self):
        """JL 261031, b10 r01: the view buttons sit above the Purpose (Q1 B), a single view keeps its bar (Q2 note),
        and no "3 topics" or "2 Jobs" line under the title (Q4 note)."""
        (self.block / 'board.md').write_text('---\ntitle: b01\n---\n# b01\n\n## Purpose\n\nOne purpose line.\n')
        topic = self.block / 'studio' / 's01-first'
        topic.mkdir(parents=True)
        (topic / 's01-first.md').write_text('# s01\n**Tags:** Alpha\n')
        for section in ('studio', 'work', 'report'):
            page = focus_page.render(frame.Theme(name='work'), self.root, self.block, section)
            main = page[page.index('<main'):]
            if section == 'studio':                                           # one list of its own sNN: no bar
                self.assertNotIn('class="section-views', main, section)       # (JL 261125)
            if 'focus-goal' in main and 'class="section-views' in main:
                self.assertLess(main.index('class="section-views'), main.index('focus-goal'), section)
            self.assertNotIn('card-sub', main, section)
            if section != 'work':                                             # Work opens on Status, whose Job rows say "3 Tasks" (JL 261104)
                self.assertNotRegex(main, r'\b\d+ (?:topics?|Jobs?|Tasks?|Runs?|events)\b', section)

    def test_a_topic_page_lists_its_previews_as_left_tabs(self):
        topic = self.block / 's01-first'
        (topic / 'ui').mkdir(parents=True)
        (topic / 's01-first.md').write_text('s01 · first\n=====\n')
        for name in ('a', 'b'):
            (topic / 'ui' / f'{name}.html').write_text('<p>x</p>')
        (topic / 's01-first.html').write_text('<nav><button data-src="ui/a.html">Metro map</button>'
                                              '<button class="old" data-src="ui/b.html">Tree</button>'
                                              '<button data-src="ui/gone.html">Gone</button></nav>')
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'studio')
        self.assertIn('>Page</button>', page)                      # the view on top (JL 261125)
        self.assertIn('<b>Metro map</b>', page)                    # the page's own previews on the left
        self.assertIn('<b>Tree</b>', page)
        self.assertNotIn('<b>Gone</b>', page)                      # a missing file is no tab
        self.assertIn('{opacity:.5}', page)                        # an earlier one reads faded
        self.assertIn('class=pb-read><button type=button class=pb-fold', page)   # the dot on the content's corner
        self.assertIn('class=open-dot', page)                       # each preview opens from its dot
        (topic / 's01-first.mindmap.md').write_text('# first\n')
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'studio')
        self.assertNotIn('>MindMap</button>', page)               # no MindMap view (JL 261125)
        self.assertNotIn('>Open Metro map ↗<', page)                # no words

    def test_an_sNN_card_shows_no_delivery_type_pill(self):
        topic = self.block / 's01-first'
        topic.mkdir()
        (topic / 's01-first.md').write_text('s01 · first\n=====\n\n**Stage:** explore\n\n**Delivery type:** skill\n')
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'studio')
        self.assertNotIn('title="delivery type"', page)            # no type pill: the UI explains itself (JL 261125)
        (topic / 's01-first.md').write_text('s01 · first\n=====\n\n**Delivery type:** deck\n')   # never a type
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'studio')
        self.assertNotIn('class="row-type"', page)

    def test_a_deliverable_with_a_url_is_a_closed_live_card_in_delivery(self):
        job = self.block / 'j01_x'
        (job / 't01_y').mkdir(parents=True)
        (job / 'j01_x.md').write_text('# x\n\n## Deliverables\n\n```yaml\ndeliverables:\n- what: The try page\n'
                                      '  task: t01_y\n  url: /_api/try/food\n- what: A table\n  task: t01_y\n```\n')
        for folder in (self.block, job, job / 't01_y'):
            html = focus_page.delivery_html(folder, self.root)
            self.assertIn('data-src="/_api/try/food"', html)              # the page itself, loaded only when opened
            self.assertIn('<details class=live-page ', html)              # closed: no `open` (AGENTS rule 15)
            self.assertNotIn(' src="/_api', html)
            self.assertNotIn('A table', html)
        other = self.block / 'j02_z'
        other.mkdir()
        self.assertEqual(focus_page.delivery_html(other, self.root), '')  # another Job has no part of it
        service = focus_page.findings_board([], self.block, self.root)    # Findings: a closed section, one tab per site
        self.assertIn('🌐 Service', service)
        self.assertIn('data-src="/_api/try/food"', service)
        self.assertNotIn('🌐 Service', focus_page.findings_board([], other, self.root))
        items = frame.delivery_items(self.block)                          # the classic view, from one reading
        self.assertEqual([(i['title'], i['fixed'], i['url']) for i in items],
                         [('The try page', ['Live page'], '/_api/try/food')])

    def test_an_sNN_with_a_delivery_gets_a_delivery_button_and_section(self):
        topic = self.block / 's01-first'
        (topic / 'delivery' / 'skill').mkdir(parents=True)
        (topic / 's01-first.md').write_text('s01 · first\n=====\n\n**Stage:** explore\n')
        (topic / 'delivery' / 'skill' / 'rule.md').write_text('the rule\n')
        (topic / 'delivery' / 'render.yaml').write_text('pieces:\n  - code: "the screen"\n    by: j01_x/t01_y\n')
        run = self.block / 'j01_x' / 't01_y' / 'runs' / 'run-a'
        run.mkdir(parents=True)
        (run / 'run.yaml').write_text('status: done\n')
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'studio')
        self.assertIn('view=focus-delivery', page)                        # a pop-out, like Draw and Mind map
        self.assertIn('· Delivery" title="Open Delivery"', page)   # its open dot pops it out
        self.assertIn('>Delivery</button>', page)         # a view button on top
        self.assertIn('✅ the screen', focus_page.delivery_document(topic, self.root))
        page = focus_page.delivery_document(topic, self.root)
        self.assertIn('✅ the screen', page)                               # a Task's Runs all done
        self.assertLess(page.index('1 · Delivery'), page.index('2 · Render'))   # the thing, then where it goes
        self.assertIn('built by t01_y, done', page)
        self.assertIn('skill/rule.md', page)                              # what it holds
        self.assertIn('<details class="deliv-file"><summary>skill/rule.md</summary>', page)   # opens in place
        self.assertIn('the rule', page)

    def test_a_builder_page_leads_back_to_the_sNN_card(self):
        topic = self.block / 's01-first'
        (topic / 'delivery' / 'web').mkdir(parents=True)
        (topic / 's01-first.md').write_text('s01 · first\n=====\n\n**Stage:** explore\n')
        (topic / 'delivery' / 'web' / 'index.html').write_text('<p>x</p>')
        (self.block / 'j01_x').mkdir()
        page = focus_page.static_page(topic, self.root, 'preview', '<p>the content</p>', 'review prototype')
        rail = page.split('class="focus-rail left"', 1)[1].split('</nav>', 1)[0]
        home = frame.esc(focus_page.topic_home(topic, self.root))
        self.assertIn(home, rail)                                        # its level's sNN, each to its card, and Jobs
        self.assertIn('j01_x', rail)
        self.assertIn(f'<a href="{home}">s01-first</a>', page)          # the path ends at its card
        self.assertIn('aria-current="page">Preview</a>', page)           # Delivery's views under the title
        self.assertIn('view=focus-delivery', page)                       # Overview: the card's Delivery pop-out
        self.assertNotIn('class="focus-goal', page)                            # no goal line under the title (block A03)
        self.assertIn('<p>the content</p>', page)

    def test_studio_rows_show_topic_line_and_preview_no_stage(self):
        topic = self.block / 'studio' / 's01-first'
        topic.mkdir(parents=True)
        (topic / 's01-first.md').write_text('# s01\n**Tags:** Alpha\n\n**Stage:** explore\n\n**Topic:** what the first topic asks\n')
        (topic / 's01-first.excalidraw').write_text('{}')
        (topic / 's01-first.png').write_bytes(b'png')
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'studio')
        self.assertIn('what the first topic asks', page)
        self.assertNotIn('class="row-stage"', page)   # no stage pill: no state word on a page (b17 trace 261127/1225)
        self.assertNotIn('rounds</span>', page)                            # no bookkeeping on the row
        self.assertIn('>Draw</button>', page)
        self.assertIn('s01-first.png', page)
        self.assertNotIn('Mind map', page)

    def test_a_topic_shows_its_address_and_hangs_on_its_job(self):
        studio = self.block / 'studio'
        for name, at in (('s01-whole', 'b01'), ('s07-one-table', 'j01'), ('s09-cut', 'j01.t03')):
            (studio / name).mkdir(parents=True)
            (studio / name / f'{name}.md').write_text(f'# {name}\n**Stage:** explore\n\n**At:** {at}\n\n**Topic:** about {name}\n')
        job = self.block / 'j01_tables'
        (job / 't03_cut').mkdir(parents=True)
        (job / 'j01_tables.md').write_text('# Tables\ngoal: Build the tables.\n')
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'studio')
        self.assertIn('id="s01-whole"', page)   # s01-D03
        self.assertIn('about s01-whole', page)
        self.assertIn('id="s07-one-table"', page)
        self.assertIn('about s07-one-table', page)                                   # a '-' inside a name becomes '_'
        self.assertIn('id="s09-cut"', page)
        work = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'work')
        self.assertNotIn('open points wait on you', work)    # Status keeps to the work's state (261106): the open
                                                             # topics are the Studio's, what waits the view's 🙋 Interaction
        page = focus_page.render(frame.Theme(name='work'), self.root, job, 'studio')        # s01-D01: the Job sees its own
        self.assertIn('about s07-one-table', page)
        self.assertIn('about s09-cut', page)
        self.assertNotIn('about s01-whole', page)

    def test_a_topic_link_lands_on_its_card_in_its_group(self):
        # JL 261031: "we will remove the single page for the studio"; the rail's sNN points to its card in section=studio
        topic = self.block / 'studio' / 's05-what-is'
        topic.mkdir(parents=True)
        (topic / 's05-what-is.md').write_text(
            's05 · What is it?\n=================\n\n**Tags:** Interface\n\n**Stage:** shaping\n\n**At:** b01\n\n'
            '**Topic:** what it is. And more words.\n')
        home = focus_page.topic_home(topic, self.root)
        self.assertIn('section=studio&group=Interface#s05-what-is', home)   # its group, so the card is on screen
        studio = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'studio', 'Interface')
        self.assertIn('id="s05-what-is"', studio)
        self.assertNotIn(frame.esc(focus_page.page_url(topic, self.root)), studio)   # nothing links the old page
        self.assertIn('id="s05-what-is"', studio)          # its line opens the face, popped out
        self.assertIn('what it is.', studio)


if __name__ == '__main__':
    unittest.main()
