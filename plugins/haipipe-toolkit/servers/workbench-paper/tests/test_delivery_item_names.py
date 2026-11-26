"""workbench-paper CONSTITUTION A01 (JL 261121): every Delivery item names its artifact.

JL 261121, of the Paper Board's Delivery › LaTeX list showing "The paper" and "Changes since the last round":
"call it Paper-Latex, and Paper-Latex-Diff". Every item the paper panel lists (TAB_GROUPS) is a hyphenated
artifact name, Kind-Lane[-Variant], and the full name and the shown name are the same.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_host"))

NAME = re.compile(r"^[A-Z][A-Za-z]*(-[A-Z][A-Za-z]*)*$")
SOURCE = (Path(__file__).resolve().parents[1] / "board_writing.py").read_text(encoding="utf-8")


def tab_groups():
    block = SOURCE[SOURCE.index("TAB_GROUPS = {"):]
    block = block[:block.index("\n}") + 2]
    return dict(re.findall(r'"([^"]+)":\s*\("([^"]+)",\s*"([^"]+)"\)', block) and
                [(k, (g, n)) for k, g, n in re.findall(r'"([^"]+)":\s*\("([^"]+)",\s*"([^"]+)"\)', block)])


def test_every_item_names_its_artifact():
    groups = tab_groups()
    assert groups, "TAB_GROUPS not found"
    for full, (_group, shown) in groups.items():
        assert NAME.match(full), f"not an artifact name: {full!r}"
        assert full == shown, f"shown name differs from the full name: {full!r} vs {shown!r}"


def test_jl_named_items_exist():
    groups = tab_groups()
    assert groups["Paper-Latex"] == ("LaTeX", "Paper-Latex")
    assert groups["Paper-Latex-Diff"] == ("LaTeX", "Paper-Latex-Diff")


def test_no_old_generic_names_are_written():
    for old in ("The paper · LaTeX", "The paper · Word", "The supplement · ", "The combined copy",
                "The submission portal", "Changes since the last round"):
        assert f'"{old}' not in SOURCE, f"old item name still written: {old!r}"
