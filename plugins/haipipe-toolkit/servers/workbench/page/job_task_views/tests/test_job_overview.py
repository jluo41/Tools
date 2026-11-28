"""The real Overview uses the selected Job's records and keeps inspection inside its Block."""
import re
import tempfile
import unittest
from pathlib import Path

from host_paths import bootstrap

bootstrap()

from live import focus_page, job_overview, work_frame  # noqa: E402


class JobOverviewTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.block = self.root / 'Project' / 'work' / 'b01_example'
        self.job = self.block / 'j11_checks'
        self.job.mkdir(parents=True)
        (self.block / 'board.md').write_text('# Example\n')
        (self.job / 'j11_checks.md').write_text(
            '# Real checks\ngoal: Validate the supplied CSV.\nclose: Both reports agree.\n'
            'bands: t0N Validation · t1N Reporting\n')
        self.t1 = self.task(self.job, 't01_columns', 'Column rules', 'Check actual column names.')
        self.t2 = self.task(self.job, 't11_report', 'HTML result', 'Write the actual report.')

    def task(self, job, name, title, goal):
        p = job / name
        p.mkdir()
        (p / f'{name}.md').write_text(f'# {title}\ngoal: {goal}\n')
        return p

    def render(self, folder=None, data=None, groups=None):
        folder = folder or self.job
        data = data if data is not None else focus_page.read_face(folder, self.root)
        groups = groups if groups is not None else work_frame.topics_for(folder, self.root, [])
        return job_overview.render(folder, self.root, data, [], groups)

    def test_authored_bands_group_real_tasks(self):
        self.assertEqual(job_overview.task_groups(self.job, self.root, []),
                         [('Validation', [self.t1]), ('Reporting', [self.t2])])
        page = self.render()
        for text in ('Validation', 'Reporting', 'Column rules', 'HTML result',
                     'Validate the supplied CSV.', 'Both reports agree.', 'Check actual column names.'):
            self.assertIn(text, page)
        self.assertNotIn('Task Group 1', page)

    def test_each_task_button_has_a_local_detail_and_no_child_navigation(self):
        page = self.render()
        buttons = re.findall(r'<button[^>]*data-jov-task="([^"]+)"', page)
        details = re.findall(r'<dialog[^>]*data-jov-detail="([^"]+)"', page)
        self.assertEqual(set(buttons), set(details))
        self.assertEqual(len(details), 2)
        self.assertNotIn('href=', page)
        self.assertNotIn('history.', page)
        self.assertNotIn('location.', page)
        self.assertIn('Project/work/b01_example/j11_checks/t01_columns/', page)

    def test_scopes_do_not_collide_for_same_job_name_in_different_blocks(self):
        other = self.root / 'Other' / 'work' / 'b02_example' / self.job.name
        other.mkdir(parents=True)
        (other.parent / 'board.md').write_text('# Another block\n')
        (other / f'{other.name}.md').write_text('# Another job\ngoal: Independent goal.\n')
        self.task(other, 't01_columns', 'Other columns', 'Different data.')
        a, b = self.render(), self.render(other)
        self.assertNotEqual(re.search(r'data-job-overview="([^"]+)"', a)[1],
                            re.search(r'data-job-overview="([^"]+)"', b)[1])
        self.assertTrue(set(re.findall(r' id="([^"]+)"', a)).isdisjoint(
            re.findall(r' id="([^"]+)"', b)))
        self.assertIn("root.querySelectorAll('[data-jov-panel]')", a)

    def test_missing_content_does_not_invent_goal_or_requirements(self):
        data = focus_page.read_face(self.job, self.root)
        data.update(goal='', close='')
        data['sections'].pop('requirements', None)
        page = self.render(data=data)
        self.assertRegex(page, r'data-jov-view="0"[^>]* disabled>Goal')
        self.assertRegex(page, r'data-jov-view="1"[^>]* disabled>Requirements')
        self.assertRegex(page, r'data-jov-view="2"[^>]*aria-pressed="true"')
        self.assertNotIn('No goal recorded', page)
        self.assertNotIn('No requirements recorded', page)

    def test_only_tasks_owned_by_the_job_enter_the_diagram(self):
        external = self.root / 't02_unrelated'
        external.mkdir()
        (self.job / 't02_link').symlink_to(external, target_is_directory=True)
        grouped = job_overview.task_groups(self.job, self.root, [('Unrelated', [external])])
        self.assertEqual([p for _, paths in grouped for p in paths], [self.t1, self.t2])

    def test_unbanded_tasks_keep_their_authored_groups_and_remaining_tasks(self):
        face = self.job / f'{self.job.name}.md'
        face.write_text('# Checks\ngoal: Test.\n')
        grouped = job_overview.task_groups(self.job, self.root, [('Named question', [self.t1])])
        self.assertEqual(grouped, [('Named question', [self.t1]), ('Tasks', [self.t2])])

    def test_authored_overview_override_still_wins(self):
        face = self.job / f'{self.job.name}.md'
        face.write_text('# Checks\ngoal: Test.\n\n## Review Content\n\n### Owned section\n\nAuthored content.\n')
        data = focus_page.read_face(self.job, self.root)
        page = work_frame.overview(self.job, self.root, data, [], [])
        self.assertIn('Authored content.', page)
        self.assertNotIn('data-job-overview=', page)


if __name__ == '__main__':
    unittest.main()
