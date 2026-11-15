"""Studio topics and sNN cards: groups, topic rows and links, delivery cards and buttons."""
import re
import unittest

from host_paths import bootstrap

bootstrap()

from live import focus_page, frame  # noqa: E402

import focus_page_fixtures as fixtures  # noqa: E402


class FocusPageTest(fixtures.FocusPageCase):
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
        self.assertIn('data-pop="First" href="/', studio)          # its name opens the face, popped out

    def test_studio_group_filters_without_losing_topic_identity(self):
        for name, group in [('s01-first', 'Alpha'), ('s02-second', 'Beta')]:
            topic = self.block / 'studio' / name
            topic.mkdir(parents=True)
            (topic / (name + '.md')).write_text(f'# {name}\n**Tags:** {group}\n')
        def body(*args):                                              # the left rail and the map list every sNN
            page = re.sub(r'<nav class="focus-rail left".*?</nav>', '', focus_page.render(*args), flags=re.S)
            page = re.sub(r'<dialog id="page-drawer".*?</dialog>', '', page, flags=re.S)
            return re.sub(r'<nav class="page-tree".*?</nav>', '', page, flags=re.S)   # (JL 261030; 261031)
        page = body(frame.Theme(name='work'), self.root, self.block, 'studio', 'Beta')
        self.assertIn('s02-second', page)
        self.assertNotIn('s01-first', page)
        self.assertIn('aria-label="Views"', page)                     # the groups are Studio's views (JL 261029)
        self.assertIn('>Beta</a>', page)
        self.assertIn('>All</a>', page)                            # one button per group, no All (JL 261029)
        (self.block / 'studio' / 's03-third').mkdir()
        (self.block / 'studio' / 's03-third' / 's03-third.md').write_text('# s03\n')
        page = body(frame.Theme(name='work'), self.root, self.block, 'studio')
        self.assertIn('s01-first', page)                              # it opens on the first group
        self.assertIn('s02-second', page)
        self.assertIn('s03-third', page)                             # the ungrouped get the last button
        page = body(frame.Theme(name='work'), self.root, self.block, 'studio', 'Other')
        self.assertIn('s03-third', page)
        self.assertNotIn('s01-first', page)

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
            self.assertIn('class="section-views', main, section)              # one group, one view: still a bar
            if 'focus-goal' in main:
                self.assertLess(main.index('class="section-views'), main.index('focus-goal'), section)
            self.assertNotIn('card-sub', main, section)
            if section != 'work':                                             # Work opens on Status, whose Job rows say "3 Tasks" (JL 261104)
                self.assertNotRegex(main, r'\b\d+ (?:topics?|Jobs?|Tasks?|Runs?|events)\b', section)

    def test_an_sNN_card_shows_its_delivery_type_beside_its_stage(self):
        topic = self.block / 's01-first'
        topic.mkdir()
        (topic / 's01-first.md').write_text('s01 · first\n=====\n\n**Stage:** explore\n\n**Delivery type:** skill\n')
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'studio')
        self.assertIn('<span class="row-type" title="delivery type">skill</span>', page)
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
        self.assertIn('· Delivery" href=', page)
        self.assertIn('>Delivery</button>', page)
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
        self.assertIn('<span class="row-stage">review prototype</span>', page)
        self.assertIn('<p>the content</p>', page)

    def test_studio_rows_show_topic_line_stage_and_preview(self):
        topic = self.block / 'studio' / 's01-first'
        topic.mkdir(parents=True)
        (topic / 's01-first.md').write_text('# s01\n**Tags:** Alpha\n\n**Stage:** explore\n\n**Topic:** what the first topic asks\n')
        (topic / 's01-first.excalidraw').write_text('{}')
        (topic / 's01-first.png').write_bytes(b'png')
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'studio')
        self.assertIn('what the first topic asks', page)
        self.assertIn('<span class="row-stage">explore</span>', page)   # the stage, one word (JL 261029: overwhelmed)
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
