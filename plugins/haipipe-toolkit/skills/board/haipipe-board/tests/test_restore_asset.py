"""Regression gates for the reload-state asset."""
import unittest
from pathlib import Path


ASSET = (Path(__file__).resolve().parents[4] / "servers" / "_host" / "assets" / "js" / "80-restore.js")


class RestoreAssetTest(unittest.TestCase):
    def test_body_observer_waits_for_dom_content_loaded(self):
        source = ASSET.read_text(encoding="utf-8")
        self.assertIn("if (!window.MutationObserver || !document.body) return;", source)
        self.assertIn("window.addEventListener('DOMContentLoaded', watchState", source)
        self.assertIn("if (document.body) watchState();", source)
        self.assertIn("typeof target.nodeType !== 'number'", source)
        self.assertIn("try {\n        watch.observe(target", source)


if __name__ == "__main__":
    unittest.main()
