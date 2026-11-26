"""A focus page is built once into a file; it is built again only when something it read changed."""
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from host_paths import bootstrap

bootstrap()

from live import page_cache  # noqa: E402


class PageCacheTest(unittest.TestCase):
    def setUp(self):
        self.tmp, self.tmp_cache = tempfile.TemporaryDirectory(), tempfile.TemporaryDirectory()
        self.cache, self.block = Path(self.tmp_cache.name), Path(self.tmp.name) / "b01_example"
        (self.block / "j01_first").mkdir(parents=True)
        (self.block / "board.md").write_text("# Example\n")
        (self.block / "j01_first" / "j01_first.md").write_text("# First\n")
        self.old = os.environ.get("PAGE_CACHE_DIR")
        os.environ["PAGE_CACHE_DIR"] = str(self.cache)
        self.builds = 0

    def tearDown(self):
        if self.old is None:
            os.environ.pop("PAGE_CACHE_DIR", None)
        else:
            os.environ["PAGE_CACHE_DIR"] = self.old
        self.tmp.cleanup()
        self.tmp_cache.cleanup()

    def build(self):
        self.builds += 1
        jobs = sorted(p.name for p in self.block.iterdir() if p.is_dir())
        faces = [(self.block / j / f"{j}.md").read_text() for j in jobs if (self.block / j / f"{j}.md").is_file()]
        return f"<h1>{(self.block / 'board.md').read_text()}</h1>{jobs}{faces}"

    def open(self):
        return page_cache.serve(("root", self.block, "focus_page"), self.build)

    def touch(self, path: Path, text: str):
        path.write_text(text)
        st = path.stat()
        os.utime(path, ns=(st.st_atime_ns, st.st_mtime_ns + 10_000_000))   # a later time, however fast the disk

    def test_a_second_open_reads_the_file(self):
        first = self.open()
        self.assertEqual(self.open(), first)
        self.assertEqual(self.builds, 1)
        self.assertEqual(len(list(self.cache.glob("*.html"))), 1)

    def test_a_changed_face_builds_it_again(self):
        self.open()
        self.touch(self.block / "j01_first" / "j01_first.md", "# First, renamed\n")
        self.assertIn("renamed", self.open())
        self.assertEqual(self.builds, 2)

    def test_a_new_or_removed_folder_builds_it_again(self):
        self.open()
        (self.block / "j02_second").mkdir()
        self.assertIn("j02_second", self.open())
        (self.block / "j02_second").rmdir()
        self.assertNotIn("j02_second", self.open())
        self.assertEqual(self.builds, 3)

    def test_another_key_is_its_own_page(self):
        self.open()
        page_cache.serve(("root", self.block, "focus_page", "studio"), self.build)
        self.assertEqual(self.builds, 2)

    def test_a_page_that_runs_another_command_is_not_kept(self):
        def build():
            self.builds += 1
            return subprocess.run(["echo", "now"], capture_output=True, text=True).stdout
        page_cache.serve(("echo",), build)
        page_cache.serve(("echo",), build)
        self.assertEqual(self.builds, 2)

    def test_off_under_pytest_without_a_folder_and_with_page_cache_0(self):
        os.environ["PAGE_CACHE"] = "0"
        try:
            self.open()
            self.open()
        finally:
            os.environ.pop("PAGE_CACHE")
        self.assertEqual(self.builds, 2)


if __name__ == "__main__":
    unittest.main()
