import tempfile
import unittest
from pathlib import Path

import sys
from pathlib import Path as _P
sys.path.insert(0, str(_P(__file__).resolve().parent.parent))
sys.path.insert(0, str(_P(__file__).resolve().parent.parent / "cli"))

from stage import render_block, render_style_block, sync_face
from src.stage_contract import replace_managed, replace_managed_style


class StageStyleOwnershipTest(unittest.TestCase):
    def test_style_from_materializes_in_page_writing_style(self):
        with tempfile.TemporaryDirectory() as tmp:
            board = Path(tmp)
            venue = board / "STYLE.md"
            venue.write_text(
                "# Venue\n\n## Writing Style\nEnglish only. One sentence per line.\n",
                encoding="utf-8",
            )
            page = {"requires": "", "style_from": "STYLE.md"}

            contract, digest = render_block(board, page, {})
            style = render_style_block(board, page, {}, digest)

            self.assertIn("### Venue", contract)
            self.assertNotIn("### Writing Style", contract)
            self.assertIn("materialized from this source in `## Writing Style`", contract)
            self.assertIn("**Inherited requirements from `STYLE.md`**", style)
            self.assertIn("English only. One sentence per line.", style)

            source = (
                "# Stage\n\n"
                "## Writing Style\n\nAuthor-owned page rule.\n\n"
                "## Stage Contract\n\n### Provides\nOutput.\n"
            )
            synced = replace_managed(source, contract)
            synced = replace_managed_style(synced, style)
            writing, contract_section = synced.split("## Stage Contract", 1)

            self.assertIn("Author-owned page rule.", writing)
            self.assertIn("haipipe:style:start", writing)
            self.assertNotIn("### Writing Style", contract_section)
            self.assertIn("### Venue", contract_section)

    def test_sync_face_updates_both_managed_owners(self):
        with tempfile.TemporaryDirectory() as tmp:
            board = Path(tmp)
            (board / "STYLE.md").write_text(
                "# Venue\n\n## Writing Style\nUse the venue's reader language.\n",
                encoding="utf-8",
            )
            stage = board / "S-Main-1-test.md"
            stage.write_text(
                "# S Main 1 · Test\n"
                "state: 🔴 OPEN\n"
                "owner: CC\n"
                "style-from: STYLE.md\n\n"
                "## Opening\nQuestion?\n\nRationale.\n\n"
                "## Writing Style\nAuthor rule.\n\n"
                "## Stage Contract\n\n"
                "### Provides\nOutput.\n\n"
                "## Content\nStage output.\n",
                encoding="utf-8",
            )
            page = {
                "id": "S-Main-1",
                "file": stage.name,
                "requires": "",
                "style_from": "STYLE.md",
            }

            sync_face(board, page, {})
            synced = stage.read_text(encoding="utf-8")
            writing, contract_section = synced.split("## Stage Contract", 1)

            self.assertIn("Author rule.", writing)
            self.assertIn("Use the venue's reader language.", writing)
            self.assertIn("haipipe:style:start", writing)
            self.assertIn("### Venue", contract_section)
            self.assertNotIn("### Writing Style", contract_section)
            self.assertIn("### Provides\nOutput.", contract_section)


if __name__ == "__main__":
    unittest.main()
