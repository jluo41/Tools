"""Files roles, source-backed paths, display numbering and links to work that touches a folder."""
import importlib.util
import re
import tempfile
import unittest
from pathlib import Path

from host_paths import bootstrap

bootstrap()

from live import work_files  # noqa: E402


def pane_checker():
    root = next(p for p in Path(__file__).resolve().parents if (p / 'PRINCIPLE.md').is_file())
    path = root / 'plugins/haipipe-toolkit/skills/1_base/workbench/hai-ui/scripts/folder_icons_check.py'
    spec = importlib.util.spec_from_file_location('folder_icons_check', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.check_parts


class RolePartsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = root = Path(self.tmp.name).resolve()
        (root / "env.sh").write_text("")
        self.project = root / "examples" / "Project-X"
        (self.project / "project.md").parent.mkdir(parents=True)
        (self.project / "project.md").write_text("# X\n")
        self.block = self.project / "work" / "b01_x"
        self.block.mkdir(parents=True)
        (self.block / "board.md").write_text("---\ntitle: x\nexamples: work/b02_a, work/b03_b\n---\n\n# X\n")
        for name in ("b02_a", "b03_b"):
            (self.project / "work" / name).mkdir()
            (self.project / "work" / name / "board.md").write_text("# A\n")
        self.code = root / "plugins" / "k" / "servers" / "w"
        self.skill = root / "plugins" / "k" / "skills" / "hai-x"
        for rel in ("side/tree/a.py", "page/b.py"):
            (self.code / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.code / rel).write_text("x\n")
        self.skill.mkdir(parents=True)
        (self.skill / "SKILL.md").write_text("x\n")

    def tearDown(self):
        self.tmp.cleanup()

    def folder(self, name, text, sub=None):
        home = (self.block / sub if sub else self.block) / name
        home.mkdir(parents=True, exist_ok=True)
        (home / (name + ".md")).write_text(text)
        return home

    def test_a_role_is_one_part_with_its_folders_numbered_inside_it(self):
        html = work_files.render(self.block, self.root)
        heads = re.findall(r"<h3>(.*?)</h3>", html)
        self.assertEqual(heads[0], "Block")                                  # the one place the work is: no number
        self.assertEqual(heads.count("Maintain: Block-Example"), 1)          # the part once, not once per folder
        self.assertNotIn("Read-From", heads)                                 # it waits for nothing and has no data
        self.assertFalse([h for h in heads if re.search(r"\d", h)])          # never 2 · Code, 3 · Skills
        part = html.split("<h3>Maintain: Block-Example</h3>")[1].split("</section>")[0]
        self.assertEqual(re.findall(r'<li data-n="(\d)"', part), ["1", "2"])  # Block-Example 1 and 2: one row each
        self.assertEqual(part.count('class="files-where"'), 1)               # one path line for rows side by side
        self.assertNotIn("files-ext", html)

    def test_a_data_store_in_a_space_folder_is_read_from(self):
        store = self.root / "_WorkSpace" / "2-RecStore" / "cohort_a"
        store.mkdir(parents=True)
        (self.block / "board.md").write_text(
            "# X\n\nexamples: work/b02_a\n\n## Data\n\n```yaml\ndata:\n"
            "  - {name: rec, where: _WorkSpace/2-RecStore/cohort_a, holds: records}\n"
            "  - {name: lake, where: catalog.schema, holds: tables}\n"            # no folder: nothing to show
            "  - {name: gone, where: _WorkSpace/absent, holds: x}\n```\n")
        html = work_files.render(self.block, self.root)
        part = html.split('class="files-part files-readfrom files-first"')[1].split("</section>")[0]
        self.assertEqual(re.findall(r'<li data-n="(\d)"', part), ["1"])       # the store; the example is maintained
        self.assertIn('data-folder-path="_WorkSpace/2-RecStore/cohort_a"', part)
        self.assertIn('title="_WorkSpace/2-RecStore/"', part)                # its own folder is the path line
        self.assertNotIn("catalog.schema", part)
        self.assertNotIn("absent", part)
        self.assertNotIn("cohort_a", html.split('class="files-part files-readfrom')[0])   # never under Maintain

    def test_maintain_is_one_part_per_kind_each_numbered_from_one(self):
        from unittest.mock import patch
        other = self.project / "blueprint" / "b12_other"
        mine = self.project / "blueprint" / "b11_mine"
        for b in (other, mine, self.project / "blueprint" / "b13_untouched"):
            b.mkdir(parents=True)
            (b / "board.md").write_text("# B\n\nexamples: work/b02_a\n")
        (mine / "trace" / "261127").mkdir(parents=True)
        (mine / "trace" / "261127" / "0900_a.md").write_text(
            "---\ntitle: a\nclosed: true\nplan:\n"
            "  - {do: edit, path: examples/Project-X/blueprint/b12_other/board.md, what: w}\n"
            "  - {do: edit, path: examples/Project-X/work/b03_b/board.md, what: w}\n---\n")
        groups = [('🖥️ Tools · UI', [self.code])]
        with patch.object(work_files, 'folder_groups', return_value=groups), \
             patch.object(work_files, 'own_skills', return_value=[self.skill]):
            html = work_files.render(mine, self.root)
        heads = re.findall(r"<h3>(.*?)</h3>", html.split('class="file-tree"')[1])
        self.assertEqual(heads[:5], ["Block", "Maintain: ServerUI", "Maintain: Skills", "Maintain: Block-Example",
                                     "Maintain: Blueprint Blocks"])
        for head, rows, where in (("Maintain: ServerUI", ["w"], "plugins/k/servers/"),
                                  ("Maintain: Skills", ["hai-x"], "plugins/k/skills/"),
                                  ("Maintain: Block-Example", ["b02_a"], "examples/Project-X/work/"),
                                  ("Maintain: Blueprint Blocks", ["b12_other"], "examples/Project-X/blueprint/")):
            part = html.split(f"<h3>{head}</h3>")[1].split("</section>")[0]
            self.assertEqual(re.findall(r'<li data-n="(\d)"', part), ["1"])   # every kind starts at one
            self.assertEqual(re.findall(r'<span title="[^"]*">([^<]+)</span>', part), rows)
            self.assertIn(f'title="{where}"', part)
        self.assertNotIn("b13_untouched", html.split("<h3>Maintain: Blueprint Blocks</h3>")[1])   # no trace: not kept
        from live import trace_view
        self.assertEqual(trace_view.blueprint_blocks(self.block, self.root), [])   # a work Block has none

    def test_a_maintained_folder_is_one_row_named_below_the_shared_path(self):
        kept = [self.code, self.skill]
        part = work_files.role_parts("Maintain", [work_files.own_row(p, self.root) for p in kept], self.root)[0]
        one, two = part.split('<li data-n="2"')
        self.assertIn("<h3>Maintain</h3>", one)
        self.assertEqual(part.count('class="files-where"'), 1)               # one path line: the folder they share
        self.assertIn('title="plugins/k/"', part)
        self.assertIn(">servers/w</span></summary>", one)                    # the folder's name ends its row: no codes
        self.assertIn(">skills/hai-x</span>", two)
        self.assertIn('data-folder-path="plugins/k/skills/hai-x"', two)      # its source path is unchanged
        self.assertNotIn("files-by", work_files.render(self.block, self.root))
        self.assertFalse((Path(work_files.__file__).parent / "touched_by.py").exists())

    def test_display_numbers_change_without_changing_folder_targets(self):
        def rows(paths):
            html = work_files.role_parts('Maintain', [work_files.own_row(p, self.root) for p in paths], self.root)[0]
            return {path: (number, url) for number, url, path in re.findall(
                r'<li data-n="(\d+)".*?data-folder-src="([^"]+)".*?data-folder-path="([^"]+)"', html, re.S)}
        before, after = rows([self.code, self.skill]), rows([self.skill, self.code])
        code = self.code.relative_to(self.root).as_posix()
        skill = self.skill.relative_to(self.root).as_posix()
        self.assertEqual(set(before), {code, skill})
        self.assertEqual(set(after), set(before))
        self.assertEqual((before[code][0], after[code][0]), ('1', '2'))
        self.assertEqual((before[skill][0], after[skill][0]), ('2', '1'))
        for path in before:
            self.assertEqual(before[path][1], after[path][1])

    def test_pane_check_accepts_current_roles_and_rejects_invalid_sources(self):
        check = pane_checker()
        block = self.block.relative_to(self.root).as_posix()
        html = work_files.render(self.block, self.root)
        self.assertEqual(check(html, block, self.root), [])
        cases = {
            'unrecognized Files role': html.replace('<h3>Block</h3>', '<h3>Invented</h3>'),
            'no SPACE-relative parent path': html.replace('class="files-where"', 'class="elsewhere"'),
            'not relative to the SPACE': html.replace('>examples/Project-X/work/</p>', '>../outside/</p>'),
            'not a real SPACE directory': html.replace(f'data-folder-path="{block}"', 'data-folder-path="absent"'),
            'display order': html.replace('<li data-n="2"', '<li data-n="8"'),
            'repeats the Maintain: Block-Example part': html + re.search(
                r'<section class="files-part files-maintain.*?</section>', html, re.S)[0],
        }
        for reason, broken in cases.items():
            with self.subTest(reason=reason):
                self.assertTrue(any(reason in error for error in check(broken, block, self.root)))


if __name__ == "__main__":
    unittest.main()
