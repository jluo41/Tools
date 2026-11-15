"""Project blueprint routing and proposed-preview boundaries."""
import tempfile
import re
import unittest
from pathlib import Path

from host_paths import bootstrap
bootstrap()
from live import focus_page, frame


class ProjectUITest(unittest.TestCase):
    def test_project_and_theme_have_report_only_with_legacy_work_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            project = root / 'Example'
            theme_folder = project / 'work'
            block = theme_folder / 'b01_example'
            block.mkdir(parents=True)
            (project / 'project.yaml').write_text('id: Example\nmission: Test the Project boundary.\n')
            (project / 'project.md').write_text('# Example\n\n## Deliverables\n\nThe agreed design.\n')
            (theme_folder / 'work.md').write_text('# Work\n')
            (block / 'board.md').write_text('# Example block\nspine: Build the example.\n')
            for folder in (project, theme_folder):
                for section, group in (('', ''), ('work', ''), ('work', 'progress'), ('children', '')):
                    with self.subTest(folder=folder.name, section=section, group=group):
                        page = focus_page.render(frame.Theme(name='work'), root, folder, section, group)
                        heading = re.search(r'<h1[^>]*>(.*?)</h1>', page, re.S).group(1)
                        self.assertIn('Report', heading)
                        rails = re.findall(r'<nav[^>]*aria-label="Page sections"[^>]*>(.*?)</nav>', page, re.S)
                        self.assertTrue(rails)
                        self.assertNotIn('section=work', ''.join(rails))
                        if section:
                            self.assertIn('b01_example', page)
                            # a Project's buttons are its Themes (JL 261109); a Theme keeps its own views
                            self.assertIn('group=theme-work' if folder == project else 'group=themes', page)
            themed = focus_page.render(frame.Theme(name='work'), root, project, 'report', 'theme-work')
            self.assertIn('Review Content', themed)
            self.assertIn('b01_example', themed)
            self.assertNotIn('>Findings</a>', themed)
            delivered = focus_page.render(frame.Theme(name='work'), root, project, 'work', 'deliverables')
            self.assertIn('The agreed design.', delivered)
            self.assertIn('group=deliverables', delivered)

    def test_project_ui_is_opt_in_and_keeps_current_page_separate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            project = root / 'Example'
            project.mkdir()
            (project / 'project.yaml').write_text('id: Example\nmission: Test the Project boundary.\n')
            (project / 'project.md').write_text('# Example\n')
            board = root / 'b10_project'
            board.mkdir()
            face = board / 'board.md'
            face.write_text('# Project design\nspine: Design the Project page.\n')
            theme = frame.Theme(name='work')
            before = focus_page.render(theme, root, board, 'report')
            self.assertNotIn('>Project UI</a>', before)
            face.write_text(face.read_text() + 'ui-project: Example\n')
            ui = board / 'ui'
            ui.mkdir()
            (ui / 'project-preview.html').write_text('<h1>Proposed Project</h1>')
            (ui / 'project-views.md').write_text('| Category | Project Type | Project | Work |\n'
                '|---|---|---|---|\n| Project | Project | Themes | Blocks |\n')
            page = focus_page.render(theme, root, board, 'report', 'ui-project')
            self.assertIn('>Project UI</a>', page)
            self.assertIn('Proposed UI', page)
            self.assertIn('Project Type × View Button', page)
            self.assertIn('data-src="/b10_project/ui/project-preview.html"', page)
            self.assertIn('path=Example', page)
            self.assertIn('The page, live', page)
            self.assertNotIn('>Block UI</a>', page)

    def test_preview_cannot_escape_served_root(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as external:
            root = Path(tmp).resolve()
            project = root / 'Example'
            project.mkdir()
            (project / 'project.md').write_text('# Example\n')
            board = root / 'b10_project'
            ui = board / 'ui'
            ui.mkdir(parents=True)
            outside = Path(external) / 'private.html'
            outside.write_text('Private preview')
            (ui / 'project-preview.html').symlink_to(outside)
            result = focus_page.ui_view(['Example'], 'Project UI', root, board)
            self.assertNotIn('Proposed UI', result)
            self.assertNotIn('private.html', result)


if __name__ == '__main__':
    unittest.main()
