"""haipipe-board src/ (QB5): build.py and serve.py are thin entries; the code
lives here by topic — common · parse · body · page_board · page_question ·
page_stage. One grammar, assembled into pages."""

from pathlib import Path

# Board owns its orchestration; shared Page modules live only with Page.
__path__.append(str(Path(__file__).resolve().parents[3] / "page" / "haipipe-page" / "src"))
