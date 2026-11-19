"""Interactions: one record serves the inbox, the work and the map; bars carry their state words."""
import re
import unittest
from pathlib import Path

from host_paths import bootstrap

bootstrap()

from live import focus_page, frame  # noqa: E402

import focus_page_fixtures as fixtures  # noqa: E402


class FocusPageTest(fixtures.FocusPageCase):
    def test_one_interaction_record_serves_the_inbox_work_and_the_map(self):
        """JL 261031 (relayed): one record per interaction; an Interactions view that defaults to Needs your input,
        with Answered and All; Work and the map open the same record; answered is not applied."""
        empty = focus_page.render(frame.Theme(name='work'), self.root, self.block)   # always on the rail (JL 261031)
        self.assertNotIn('No Interactions linked to this view.', empty)   # an empty section is hidden (JL 261113)
        self.assertIn('>Delivery<', empty)                                     # Delivery too (JL 261031)
        self.assertNotIn('Nothing handed over yet', focus_page.render(frame.Theme(name='work'), self.root, self.block, 'report', 'delivery'))
        topic = self.block / 's01-first'
        topic.mkdir()
        (topic / 's01-first.md').write_text('s01 · First idea\n=====\n')
        job = self.block / 'j01_tables'
        task = job / 't01_cut'
        task.mkdir(parents=True)
        (job / 'j01_tables.md').write_text('# j01 · Tables\n\ngoal: Make the tables.\n')
        (task / 't01_cut.md').write_text('# t01 · Cut\nstate: 🔴 OPEN\n')
        wait = task / 'runs' / 'r01_collect_cut_choices'
        wait.mkdir(parents=True)
        (wait / 'run.yaml').write_text('run: r01_collect_cut_choices\nkind: hard\ntype: collect\nstatus: waiting\n')
        (wait / 'question_collection.md').write_text('# Cut choices\n\nfor: b01-s01:study @ first\n\n## Q1 · Cut\n\nWhy.\n\n'
                                                     '**Which cut first?**\n\n- [x] A · Age\n- [ ] B · Sex\n\nWhy A: x.\n')
        (wait / 'r01_collect_cut_choices.html').write_text('<!doctype html>')
        done = job / 'runs' / 'r01_collect_old_choices'
        (done / 'result').mkdir(parents=True)
        (done / 'run.yaml').write_text('run: r01_collect_old_choices\nkind: hard\ntype: collect\nstatus: done\n'
                                       'feeds:\n- b01_study/j01_tables/t01_cut/runs/run-make-x\n')
        (done / 'question_collection.md').write_text('# Old choices\n\n## Q1 · Old\n\nWhy.\n\n**Which one?**\n\n- [x] A · a\n- [ ] B · b\n')
        (done / 'result' / 'answer_collection.md').write_text('# Old choices · answers\n\nreceived: 2026-10-31 12:05\n')
        rows = focus_page.interactions(self.block, self.root)
        self.assertEqual([(r['run'], r['state']) for r in rows],
                         [('r01_collect_cut_choices', 'waiting'), ('r01_collect_old_choices', 'answered')])
        self.assertEqual(rows[0]['topic'], topic)                                 # its for: address names s01
        self.assertEqual(rows[0]['asks'], [('Q1', 'Cut', 'Which cut first?')])
        form = 'href="/b01_study/j01_tables/t01_cut/runs/r01_collect_cut_choices/r01_collect_cut_choices.html"'
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'interactions')
        self.assertIn('data-ixq="Q1"', page)                       # the rail item says something waits, never a count
        self.assertIn('aria-current="page">All</a>', page)          # the default view: all of them (JL 261031)
        self.assertIn('>Answered</a>', page)
        self.assertIn('>All</a>', page)
        self.assertIn('<b>Cut choices</b>', page)
        self.assertIn('data-ixq="Q1"><b>Q1 · Cut</b>', page)                      # what it asks
        self.assertIn('Asked by <a href=', page)                                  # who asked, in words (round 3)
        self.assertIn('title="t01_cut">Cut</a> · about', page)                   # its folder name on hover only
        self.assertIn('>First idea</a>', page)                                    # what it is about, by its title
        self.assertNotIn('<small class=ix-addr>j01 · t01</small>', page)
        self.assertIn(form.replace('href=', 'src='), page)
        self.assertIn('<b>Old choices</b>', page)                               # All shows the answered too
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'interactions', 'waiting')
        self.assertIn('<b>Cut choices</b>', page)
        self.assertNotIn('Old choices', page)
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'interactions', 'answered')
        self.assertIn('<b>Old choices</b>', page)
        self.assertIn('answered · 2026-10-31', page)                               # its state and date, no colour tag
        self.assertIn('Applying it belongs to run-make-x.', page)                 # answered is not applied
        self.assertIn('>See answers</a>', page)
        self.assertNotIn('<b>Cut choices</b>', page)
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'interactions', 'all')
        self.assertIn('<b>Cut choices</b>', page)
        self.assertIn('<b>Old choices</b>', page)
        self.assertIn('>See answers</a>', focus_page.render(frame.Theme(name='work'), self.root, self.block, 'interactions'))   # no form built: its plain row
        # one button, "Interaction", wherever an item shows; no count and no tag (JL 261031, b16 t01 r04 Q3-Q6); 🙋 when one waits
        button = lambda holder: ('data-pop="' + holder.name + ' · Interaction" href="/_board/workbench?view=focus-part&amp;'
                                 'part=interactions&amp;path=' + str(holder.relative_to(self.root)).replace('/', '%2F') + '"')
        for page in (focus_page.render(frame.Theme(name='work'), self.root, self.block, 'studio'),):
            self.assertIn('Interaction</a>', page)
            self.assertIn('>🙋 Interaction</a>', page)       # a waiting question flags it (JL 261031: "flag them as well")
            self.assertNotIn('Questions for you', page)
            self.assertNotIn('Answered</a>', page.replace('>Answered</a>', ''))
        # a Plan + Results row whose Job or Task waits on the person carries 🙋 N, and its card is the question form
        # itself (JL 261116: "for the interactions, it can be ... the question card"); a row with nothing waiting, none
        self.assertIn('data-im-open="j01~ask">🙋 1<', focus_page.render(frame.Theme(name='work'), self.root, self.block, 'work'))
        self.assertNotIn('🙋 Answer', focus_page.render(frame.Theme(name='work'), self.root, self.block, 'work'))
        self.assertIn(button(topic), focus_page.render(frame.Theme(name='work'), self.root, self.block, 'studio'))
        listed = focus_page.part_document(topic, self.root, 'interactions')      # the pop-out: the topic's items
        self.assertIn('<b>Cut choices</b>', listed)
        self.assertIn('data-ixq="Q1"><b>Q1 · Cut</b>', listed)                     # the standard look: a tab per question
        self.assertIn('waiting for you', listed)
        self.assertIn(form.replace('href=', 'src=') + '></iframe>', listed)          # its own form, on the right
        self.assertNotIn('Old choices', listed)                                    # not about s01
        listed = focus_page.part_document(job, self.root, 'interactions')        # a Job: the items at it or below
        self.assertLess(listed.index('Cut choices'), listed.index('Old choices'))  # the waiting one first

    def test_interaction_closes_every_view_at_every_level(self):
        """JL 261104: "at the bottom for each of the view? not matter for the block, or job or task"; "the standard"."""
        job = self.block / 'j01_tables'
        task = job / 't01_cut'
        task.mkdir(parents=True)
        (job / 'j01_tables.md').write_text('# j01 · Tables\n\ngoal: Make the tables.\n')
        (task / 't01_cut.md').write_text('# t01 · Cut\nstate: 🔴 OPEN\n')
        for page in (self.block, job, task):                                     # none asked: hidden (JL 261113)
            for section in ('report', 'work'):
                self.assertNotIn('🙋 Interactions</span></summary>',
                              focus_page.render(frame.Theme(name='work'), self.root, page, section))
        run = task / 'runs' / 'r01_collect_cut'
        run.mkdir(parents=True)
        (run / 'run.yaml').write_text('run: r01_collect_cut\nkind: hard\ntype: collect\nstatus: waiting\nview: status\n')
        (run / 'question_collection.md').write_text('# Cut\n\n## Q1 · Cut\n\nWhy.\n\n**Which?**\n\n- [x] A · a\n- [ ] B · b\n')
        (run / 'r01_collect_cut.html').write_text('<!doctype html>')
        theme = frame.Theme(name='work')
        # The explicit Status assignment is shared at every level; the rail keeps every item.
        for page, view in ((self.block, 'standing'), (job, 'standing'), (task, 'standing')):
            for section, group in (('report', view), ('work', view), ('interactions', '')):
                html = focus_page.render(theme, self.root, page, section, group)
                if section != 'interactions':
                    self.assertIn('🙋 Interactions</span><span class="word you mk" title="1 waits for you">🙋 1</span>', html, (page.name, section))
                self.assertNotIn('🙋 Cut: Q1 · Cut</p>', html, (page.name, section))
                self.assertIn('data-ixq="Q1"', html, (page.name, section))
                if section == 'work':                  # shown once: Process no longer repeats it (JL 261105)
                    self.assertNotIn('Waiting on you', html, page.name)
                    # once in the view's 🙋 Interaction, and once in each row card that waits on it (JL 261116)
                    self.assertEqual(html.count('data-ixq="Q1"'), 1 + html.count('lc-ask" data-im-slot'), page.name)
        other = focus_page.render(theme, self.root, self.block, 'report', 'mindmap')
        self.assertNotIn('data-ixq="Q1"', other)  # Child inbox belongs to Status; rail aggregates it.
        self.assertIn('data-ixq="Q1"', focus_page.part_document(job, self.root, 'interactions'))
        from live import interaction_section as IX     # numbered after a work band's numbered folds (261105)
        body = '<h3 class=wk-band>📊 Results</h3><details class=band-sec><summary>1 · A</summary></details>' \
               '<details class=band-sec><summary><span class=bt>2 · B</summary></details>'
        self.assertEqual(IX.next_number(body), 3)
        self.assertEqual(IX.next_number('<h3 class=pb-group>RESULTS</h3><section class=fd-sec><h3 class=fd-h>4 · X</h3>'), 5)
        self.assertEqual(IX.next_number('<p>no numbered section</p>'), 0)

    def test_a_bar_carries_its_state_word_and_what_waits_shows_under_it_closed(self):
        """JL 261106: "every closed bar shows a state word on its right, and a section that waits on you also shows that
        one item under its closed bar"; the fold remembers a bar by its title alone, never its word."""
        from live import interaction_section as IX, ui_parts
        from live.focus_draft import JS
        # JL 261114: a bar carries a mark, never a state word: what waits is an orange 🙋 N (the sentence on hover),
        # a finished section a quiet ✓, any other state nothing
        self.assertEqual(ui_parts._section('1 · 🔢 Values', '<p>b</p>', '2 wait for you', '🙋 Q1 · Which?'),
                         '<section class=fd-sec><h3 class=fd-h>1 · 🔢 Values<span class="word you mk" title="2 wait for you">🙋 2</span></h3>'
                         '<p class=fd-wait>🙋 Q1 · Which?</p><p>b</p></section>')
        self.assertIn('class="word ok mk"', ui_parts.word_span('answered'))
        self.assertEqual(ui_parts.word_span('nothing yet'), '')
        self.assertEqual(ui_parts.word_span('3 of 5 done'), '')
        self.assertEqual(ui_parts._section('X', '<p>b</p>', 'done'), '<section class=fd-sec><h3 class=fd-h>X<span class="word ok mk" aria-label="done">✓</span></h3><p>b</p></section>')
        self.assertTrue(ui_parts._numbered(ui_parts._section('X', '<p>b</p>', 'done')).startswith('<section class=fd-sec><h3 class=fd-h>1 · X<span'))
        self.assertEqual(IX.next_number(ui_parts._numbered(ui_parts._section('X', '<p>b</p>', 'done'))), 2)
        for script in (JS, IX.FOLD):                   # the waiting line stays out of the fold; the key skips the word
            self.assertIn("contains('fd-wait')", script)
            self.assertIn("querySelectorAll('.word')", script)
        rows = [('Plan', '', 'done', '', '', False), ('Draw', '', 'waiting for you', '', '', False), ('Run', '', 'not started', '', '', False)]
        self.assertEqual(ui_parts.todo_word(rows), ('1 waits for you', '🙋 Draw'))
        self.assertEqual(ui_parts.todo_word(rows[:1] + rows[2:]), ('1 of 2 done', ''))
        self.assertEqual(ui_parts.todo_word(rows[:1]), ('done', ''))
        self.assertEqual(ui_parts.todo_word([]), ('nothing yet', ''))

    def test_paper_numbered_bars_carry_no_tally(self):
        """The paper and work placeholders in Tools (blueprints/Project-Ladder) are the prototypes every project gets
        (JL 261105): no numbered bar of any Report or Work view carries a check or progress tally, or an empty-state
        word (AGENTS § Page words, JL 261113); "N wait(s) for you" stays, since that count is the answer."""
        tools = Path(__file__).resolve().parents[5]
        base = tools / 'blueprints' / 'Project-Ladder'
        board, block = base / 'paper' / 'Paper-Example', base / 'work' / 'b90_example_paper_results'
        if not (board.is_dir() and block.is_dir()):
            self.skipTest('the Tools placeholders are not in this checkout')
        pages = [board] + [j for j in sorted(board.glob('j[0-9]*_*')) if j.is_dir()]
        pages += [next(iter(sorted(j.glob('t00_*'))), None) for j in sorted(board.glob('j1[0-9]_*'))]   # one Section a version
        # Work omits boilerplate availability words; paper retains its contract.
        bar = re.compile(r'<h3 class=fd-h>(\d+ · .*?)</h3>|<details class="?band-sec[^>]*><summary>(\d+ · .*?)</summary>', re.S)
        tally = re.compile(r'\d+ of \d+|to fix|nothing yet|not built yet|keys verified|plans signed|paragraphs ·'
                           r'|all current|need a look|\d+ differs?\b')
        # drawn by shared page code every theme uses (view_section's empty word, ui_parts.todo_word); their owners decide
        shared = ('🙋 Interaction', '🧭 Walk and fill')
        found, seen = [], 0
        for page in (p for p in pages if p is not None):
            theme = frame.themes().get(frame.theme_of(page, tools), frame.VANILLA)
            for section in ('report', 'work'):
                nav = re.search(r'<nav class="section-views".*?</nav>', focus_page.render(theme, tools, page, section), re.S)
                for view in dict.fromkeys(re.findall(r'group=([^"&]+)', nav[0]) if nav else ['']):
                    for m in bar.finditer(focus_page.render(theme, tools, page, section, view)):
                        seen += 1
                        title = m.group(1) or m.group(2)
                        word = re.search(r'<span class=(?:word|"word you")>([^<]+)</span>', title)
                        if word and tally.search(word.group(1)) and not any(s in title for s in shared):
                            found.append(f'{page.name} {section} {view}: {re.sub("<[^>]+>", " ", title)[:80]}')
        self.assertGreater(seen, 100)
        self.assertEqual(found, [])


if __name__ == '__main__':
    unittest.main()
