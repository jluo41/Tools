"""ideation_drawing.py: make writes a forwarding builder and a words yaml; draw lays out ① the steps, ② the setting,
one card per lead idea and the path to G0."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import ideation_drawing as idr  # noqa: E402


def frames(path: Path) -> list[str]:
    els = json.loads(path.read_text(encoding="utf-8"))["elements"]
    return [e.get("name", "") for e in els if e.get("type") == "frame"]


def test_make_then_draw(tmp_path):
    topic = tmp_path / "studio" / "s01-ideation"
    topic.mkdir(parents=True)
    builder = idr.make(topic)
    assert builder.name == "build_s01_ideation.py"
    assert (topic / "s01-ideation-drawing.yaml").is_file()
    out = idr.draw(topic)
    names = frames(out)
    assert names[0].startswith("①") and "🪜" in names[0]
    assert names[1].startswith("②")                                 # the setting
    assert any("🔥 i01" in n for n in names)                         # the lead group's card
    assert names[-1].endswith("From here to G0")


def test_lead_cards_follow_the_first_group(tmp_path):
    topic = tmp_path / "s01-ideation"
    topic.mkdir()
    idr.make(topic)
    words = topic / "s01-ideation-drawing.yaml"
    text = words.read_text(encoding="utf-8").replace("ideas: [i01]}", "ideas: [i01, i02]}")
    text = text.replace("ideas:\n  i01:", "ideas:\n  i02:\n    short: \"Second?\"\n    why: \"w\"\n    now: \"❓ open\"\n  i01:")
    words.write_text(text, encoding="utf-8")
    names = frames(idr.draw(topic))
    assert sum("🔥" in n for n in names) == 2


def test_make_keeps_an_existing_builder(tmp_path):
    topic = tmp_path / "s01-ideation"
    topic.mkdir()
    (topic / "build_s01_ideation.py").write_text("# mine\n", encoding="utf-8")
    try:
        idr.make(topic)
    except SystemExit as e:
        assert "--force" in str(e)
    else:
        raise AssertionError("make overwrote a builder without --force")
