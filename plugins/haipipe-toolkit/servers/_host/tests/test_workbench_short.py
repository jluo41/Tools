"""`/w/<board>[/<page>[/<tab>]]` · the short workbench address, and `file=` derivation.

The `/b/` twin already has its tests in the Board engine (`tests/test_home.py`);
these cover what `/w/` adds: the board-level route chosen from `board.md`, the
page-level tab map, the redirect target the server composes, and the `target()`
fallback that derives `file=` from `path=` so callers stop composing it by hand.
"""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from host_paths import bootstrap
bootstrap()

from live.home import (HomeMixin, WORKBENCH_TABS, board_by_slug,  # noqa: E402
                       board_workbench_route, resolve_workbench)
from live.base import BaseMixin  # noqa: E402
import server_config  # noqa: E402
from host_registry import WORKBENCH_ROUTES, route_allowed  # noqa: E402


def fixture(tmp: str, board_md: str = "# /topic: a title\nspine: s\n"):
    root = Path(tmp).resolve()
    board = root / "unit" / "diagram" / "01-topic-260722"
    (board / "1-QA-design").mkdir(parents=True)
    (board / "board").mkdir()
    (board / "board.md").write_text(board_md)
    (board / "1-QA-design" / "QA1-question.md").write_text("# Q\nstate: 🔴 OPEN\n")
    folded = board / "2-QB-work" / "QB1-folded"
    folded.mkdir(parents=True)
    (folded / "QB1-folded.md").write_text("# Folded\n\n## Opening\n\ntext\n")
    (board / "board" / "index.html").write_text("index")
    return root, board


class RouteMatcherTest(unittest.TestCase):
    def test_accepts_only_its_own_shape(self):
        request = HomeMixin()
        for path, expected in [
            ("/w/topic", ("topic", "", "")),
            ("/w/topic/QA1", ("topic", "QA1", "")),
            ("/w/topic/QA1/runs", ("topic", "QA1", "runs")),
            ("/w/topic/QA1/runs/", ("topic", "QA1", "runs")),
            ("/w/topic/QA1/runs?run=rp-struct-01", ("topic", "QA1", "runs")),
        ]:
            request.path = path
            self.assertEqual(request.workbench_request(), expected, path)
        for path in ("/w", "/w/", "/w/topic/QA1/runs/extra", "/b/topic", "/workbench/x"):
            request.path = path
            self.assertIsNone(request.workbench_request(), path)


class ResolveWorkbenchTest(unittest.TestCase):
    def test_shares_the_slug_rule_with_b(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, board = fixture(tmp)
            self.assertEqual(board_by_slug(root, "topic"), board)
            self.assertEqual(board_by_slug(root, "01-topic-260722"), board)
            self.assertIsNone(board_by_slug(root, "nosuch"))

    def test_page_level_defaults_to_outline_and_derives_both_query_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, _ = fixture(tmp)
            url, why = resolve_workbench(root, "topic", "QA1")
            self.assertEqual(why, "ok")
            self.assertEqual(url, "/_board/outline?path=unit/diagram/01-topic-260722/"
                                  "1-QA-design/QA1-question.md&file=1-QA-design/QA1-question.md")
            url, _ = resolve_workbench(root, "topic", "QA1-question", "runs")
            self.assertTrue(url.startswith("/_board/runs?path="))
            url, _ = resolve_workbench(root, "topic", "qa1", "folder")
            self.assertTrue(url.startswith("/_board/folderstat?path="))

    def test_a_folded_page_answers_to_its_folder_name_and_file_is_board_relative(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, _ = fixture(tmp)
            url, why = resolve_workbench(root, "topic", "QB1", "delivery")
            self.assertEqual(why, "ok")
            self.assertTrue(url.endswith("&file=2-QB-work/QB1-folded/QB1-folded.md"), url)

    def test_misses_are_404_reasons_not_guesses(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, _ = fixture(tmp)
            self.assertEqual(resolve_workbench(root, "nosuch")[0], None)
            self.assertEqual(resolve_workbench(root, "topic", "QZ9")[0], None)
            url, why = resolve_workbench(root, "topic", "QA1", "studio")
            self.assertIsNone(url)
            self.assertIn("unknown tab", why)
            url, why = resolve_workbench(root, "topic")
            self.assertIsNone(url)
            self.assertIn("no board-level workbench", why)
            self.assertIsNone(resolve_workbench(root, "topic", "", "runs")[0])

    def test_board_level_route_follows_what_board_md_declares(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, board = fixture(tmp, "# Paper\nspine: s\ndialect: paper\n")
            self.assertEqual(board_workbench_route(board), "paper")
            url, why = resolve_workbench(root, "topic")
            self.assertEqual(url, "/_board/paper?path=unit/diagram/01-topic-260722/board.md&file=board.md")
        with tempfile.TemporaryDirectory() as tmp:
            root, board = fixture(tmp, "# Jobs\nspine: s\nboard-kind: labeling-board\n")
            self.assertEqual(board_workbench_route(board), "labeling-board")
        with tempfile.TemporaryDirectory() as tmp:
            root, board = fixture(tmp, "# Designs\nspine: s\nboard-kind: design-board\n")
            self.assertEqual(board_workbench_route(board), "design-board")
        with tempfile.TemporaryDirectory() as tmp:
            root, board = fixture(tmp, "# Insights\nspine: s\nboard-kind: insight-board\n")
            self.assertEqual(board_workbench_route(board), "insight-board")

    def test_every_tab_word_maps_to_a_real_get_route(self):
        served = {"outline", "runs", "pageruns", "delivery", "folderstat", "evidence",
                  "value", "design", "insight", "labeling"}
        self.assertEqual(set(WORKBENCH_TABS.values()), served)


class DeriveFileTest(unittest.TestCase):
    def resolver(self, root):
        obj = BaseMixin()
        obj.root = root
        return obj

    def test_file_is_derived_when_omitted_and_vetted_as_before(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, board = fixture(tmp)
            r = self.resolver(root)
            rel = "unit/diagram/01-topic-260722"
            for payload in ({"path": f"{rel}/1-QA-design/QA1-question.md"},
                            {"path": f"{rel}/1-QA-design/QA1-question.md", "file": ""},
                            {"path": f"{rel}/2-QB-work/QB1-folded"},
                            {"path": f"{rel}/2-QB-work/QB1-folded/QB1-folded.md"}):
                source, target = r.target(payload)
                self.assertIsNotNone(source, payload)
                self.assertEqual(target, board)
            source, target = r.target({"path": f"{rel}/board.md"})
            self.assertEqual(source, board / "board.md")
            source, target = r.target({"path": f"/{rel}/board/index.html"})
            self.assertEqual(source, board / "board.md")
            source, why = r.target({"path": f"{rel}/nowhere"})
            self.assertIsNone(source)
            self.assertIn("cannot be derived", why)
            source, why = r.target({"path": f"{rel}/1-QA-design/QA1-question.md", "file": "../../etc/passwd"})
            self.assertIsNone(source)
            source, why = r.target({"file": "x.md"})
            self.assertIsNone(source)
            self.assertIn("path must be a string", why)


class DomainsTest(unittest.TestCase):
    def test_configured_then_tailscale_then_loopback(self):
        real = server_config.tailscale_ip
        server_config.tailscale_ip = lambda: "100.64.0.9"
        try:
            got = server_config.domains({"DOMAIN": "https://board.example"}, "0.0.0.0", 5599)
            self.assertEqual(got, [("https://board.example", "configured"),
                                   ("http://100.64.0.9:5599", "tailscale"),
                                   ("http://127.0.0.1:5599", "loopback")])
            got = server_config.domains({}, "127.0.0.1", 5599)
            self.assertEqual(got, [("http://127.0.0.1:5599", "loopback")])
            got = server_config.domains({}, "100.64.0.9", 5599, public_url="http://100.64.0.9:5599/")
            self.assertEqual(got, [("http://100.64.0.9:5599", "configured"),
                                   ("http://127.0.0.1:5599", "loopback")])
        finally:
            server_config.tailscale_ip = real

    def test_settings_env_accepts_a_domain_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg = Path(tmp) / ".server_config"
            cfg.mkdir()
            (cfg / "settings.env").write_text('export DOMAIN="http://100.64.0.9:5599"\nPORT=5599\n')
            got = server_config.load_server_config(tmp)
            self.assertEqual(got["DOMAIN"], "http://100.64.0.9:5599")


class OnlyHostTest(unittest.TestCase):
    """`--only labeling`: what a labeling-only host answers and refuses."""

    def test_allowlist_keeps_reader_doors_and_the_named_workbench_only(self):
        only = frozenset({"labeling"})
        for path in ("/", "/boards", "/b/topic/QA1", "/w/topic", "/w/topic/QA1/labeling",
                     "/unit/diagram/board/index.html", "/unit/diagram/board/_assets/board.js",
                     "/_board/health", "/_board/asset/xterm.css",
                     "/_board/labeling-board?path=x", "/_board/labeling?path=x&file=y",
                     "/_board/labeling/act"):
            self.assertTrue(route_allowed(path, only), path)
        for path in ("/_shell", "/_events", "/_term/abc", "/_board/terms", "/_board/chat",
                     "/_board/outline?path=x&file=y", "/_board/structure", "/_board/write",
                     "/_board/design-board?path=x", "/_excalidraw"):
            self.assertFalse(route_allowed(path, only), path)
        self.assertTrue(route_allowed("/_board/outline?path=x", frozenset({"page"})))
        self.assertTrue(route_allowed("/_board/terms", frozenset()), "no --only means everything")

    def test_every_workbench_folder_has_a_route_row(self):
        from host_registry import workbench_folders
        names = {f.name.split("-", 1)[1] for f in workbench_folders()}
        self.assertTrue(names <= set(WORKBENCH_ROUTES), names - set(WORKBENCH_ROUTES))


class LabelingTabTest(unittest.TestCase):
    def test_labeling_tab_carries_the_three_values_the_view_checks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, board = fixture(tmp)
            (board / "board" / "QA").mkdir()
            (board / "board" / "QA" / "QA1-question.html").write_text("page")
            url, why = resolve_workbench(root, "topic", "QA1", "labeling")
            self.assertEqual(why, "ok")
            self.assertEqual(url, "/_board/labeling?path=/unit/diagram/01-topic-260722/board.md"
                                  "&file=1-QA-design/QA1-question.md"
                                  "&page=/unit/diagram/01-topic-260722/board/QA/QA1-question.html")

    def test_labeling_tab_without_a_built_page_says_so(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, _ = fixture(tmp)
            url, why = resolve_workbench(root, "topic", "QA1", "labeling")
            self.assertIsNone(url)
            self.assertIn("build.py", why)


class LabelingHostEntryTest(unittest.TestCase):
    def test_subjective_label_host_runs_the_shared_host_with_only_labeling(self):
        import subprocess
        import sys
        entry = Path(__file__).resolve().parents[4] / "subjective-label" / "servers" / "_host" / "serve.py"
        if not entry.is_file():
            self.skipTest("subjective-label is not checked out beside haipipe-toolkit")
        out = subprocess.run([sys.executable, str(entry), "--help"], capture_output=True, text=True, timeout=60)
        self.assertEqual(out.returncode, 0, out.stderr[-500:])
        self.assertIn("--only", out.stdout)
        bad = subprocess.run([sys.executable, str(entry), "--only", "nosuch", "--root", "."],
                             capture_output=True, text=True, timeout=60)
        self.assertNotEqual(bad.returncode, 0)
        self.assertIn("unknown workbench", bad.stderr)


if __name__ == "__main__":
    unittest.main()
