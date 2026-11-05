"""Earlier rounds wait behind one closed fold, with no count (JL 261103); their tabs and panels stay."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_host"))
import live  # noqa: E402,F401
from live.board_results import _fold_earlier  # noqa: E402
from live.ui_parts import _side_tabs  # noqa: E402


def _tabs():
    return _side_tabs("d", [("The paper", "x"), ("Earlier round · 1", "v2"), ("Earlier round · 2", "v1")], ["a", "b", "c"])


def test_older_tabs_sit_in_a_closed_fold_with_no_count():
    html = _fold_earlier(_tabs(), "d", 1, 3)
    fold = html[html.index("<details"):html.index("</details>")]
    assert "<details class=pb-earlier" in html and " open" not in fold.split(">")[0]
    assert ">Earlier rounds</summary>" in fold
    assert 'data-pbtab="d1"' in fold and 'data-pbtab="d2"' in fold and 'data-pbtab="d0"' not in fold
    assert html.count("data-pbpanel=") == 3


def test_nothing_older_nothing_folded_and_only_older_stays_open():
    assert "<details" not in _fold_earlier(_tabs(), "d", 3, 3)
    assert "<details class=pb-earlier style=\"flex-basis:100%\" open>" in _fold_earlier(_tabs(), "d", 0, 3)


def test_each_tab_flags_its_state():
    """JL 261104: "could you flag each tab' status?": can it be read now, and what is not final yet."""
    import board_results as br
    man = {"status": "DRAFT", "portal": {"uploads": [{"state": "ready"}, {"state": "draft"}]},
           "cover_letter": {"checks": [{"ok": False}]}}
    assert br._tab_flag("latex", man, None, False) == "✅ Read now · draft"
    assert br._tab_flag("latex", man, None, True) == "⏳ Rebuilding: last build shown"
    assert br._tab_flag("word", man, None, False, stand_in=True) == "❗ Word stuck: layout not final"
    assert br._tab_flag("word", man, None, True) == "⏳ Rebuilding: do not open"
    assert br._tab_flag("letter", man, None, False) == "❗ 1 checks open"
    assert br._tab_flag("portal", man, None, False) == "⬜ 1 of 2 uploads ready"
