"""Home lists live Blocks only: a board.md kept in an `_old/` folder is a backup or a retired Block."""
from pathlib import Path

from live.home import discover_boards


def test_old_folders_are_not_listed_as_blocks(tmp_path: Path):
    # JL 261012: "why I have these three blocks?" (b32's own board, plus two backup copies in its _old/)
    block = tmp_path / "examples-A5-visa" / "Project-EB1A" / "cowork" / "b32_eb1a_petition"
    for folder in (block, block / "_old" / "before-specific-actions-2026-10-12",
                   block.parent / "_old" / "b33_evidence"):
        folder.mkdir(parents=True)
        (folder / "board.md").write_text("# EB-1A Petition\nboard-kind: cowork-block\nspine: s\n")
    cards = discover_boards(tmp_path, include_page_state=False)
    assert [card["path"] for card in cards] == ["examples-A5-visa/Project-EB1A/cowork/b32_eb1a_petition"]


def test_a_nested_space_is_not_listed(tmp_path: Path):
    # JL 261013: a replication package (platforms/SMSDesign-SPACE/) holds its own env.sh and pinned copies of
    # Tools and a Project; their Boards belong to that SPACE's host, not to this home.
    (tmp_path / "env.sh").write_text("")
    own = tmp_path / "examples-5-design" / "Project-Application-SMSDesign" / "insight" / "Insight-SMSR2v1"
    nested = tmp_path / "platforms" / "SMSDesign-SPACE"
    for folder in (own, nested / "examples-5-design" / "Project-Application-SMSDesign" / "insight" / "Insight-SMSR2v1",
                   nested / "Tools" / "blueprints" / "b01_haipipe-toolkit"):
        folder.mkdir(parents=True)
        (folder / "board.md").write_text("# A Board\nboard-kind: insight-board\nspine: s\n")
    (nested / "env.sh").write_text("")
    cards = discover_boards(tmp_path, include_page_state=False)
    assert [card["path"] for card in cards] == ["examples-5-design/Project-Application-SMSDesign/insight/Insight-SMSR2v1"]
