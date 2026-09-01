"""Regression gates for the reload-state asset."""
import unittest
from pathlib import Path


ASSET = Path(__file__).resolve().parent.parent / "assets" / "js" / "80-restore.js"
COMMENT_WRITE = (
    Path(__file__).resolve().parent.parent
    / "assets" / "js" / "10-drawer" / "10-comment" / "30-write.js"
)


class RestoreAssetTest(unittest.TestCase):
    def test_body_observer_waits_for_dom_content_loaded(self):
        source = ASSET.read_text(encoding="utf-8")
        self.assertIn("if (!window.MutationObserver || !document.body) return;", source)
        self.assertIn("window.addEventListener('DOMContentLoaded', watchState", source)
        self.assertIn("if (document.body) watchState();", source)
        self.assertIn("typeof target.nodeType !== 'number'", source)
        self.assertIn("try {\n        watch.observe(target", source)

    def test_pending_comment_button_has_its_sync_handler(self):
        source = COMMENT_WRITE.read_text(encoding="utf-8")
        self.assertIn("async function sync()", source)
        self.assertIn("var n = await drain(true);", source)


if __name__ == "__main__":
    unittest.main()
