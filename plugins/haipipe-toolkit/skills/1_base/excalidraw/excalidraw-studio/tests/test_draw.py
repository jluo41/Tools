"""A drawing made with excalidraw-studio's helpers: frames in acts, a mind map, a flow, a folder tree, density."""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from draw import FLOOR, KEY, MAP_FLOOR, Drawing  # noqa: E402

BRANCHES = [{"title": f"① principle {i}", "by": "asked 261012", "summary": "one line, read zoomed out",
             "leaves": ["a detail", "❓ an open point"]} for i in range(6)] + \
           [{"title": "🎨 the look", "by": "standing", "leaves": ["black, red, green"]}]


def test_a_drawing_in_acts():
    d = Drawing()
    one = d.frame("① The principles: one mind map")
    d.heading("🧠 The principles", "what the frame says")
    bottom = d.mind_map("a Studio drawing reads as one story", BRANCHES)
    assert bottom <= 1600                                   # the frame grows only as far as its rows need
    d.badge(one)
    two = d.frame("② The checks: one flow")
    d.heading("🔁 The checks")
    d.flow([{"title": "build", "lines": ["from disk"]}, {"title": "❓ a missing check", "lines": []},
            {"title": "write", "key": True}], 40, 200, 2480, labels=["then", "then"])
    d.text(40, 700, "\n".join(Drawing.folder_tree(Path(__file__).resolve().parents[1], open_=("scripts",))), 20,
           code=True)
    d.badge(two)
    d.acts([{"name": "Act 1 · the principles", "frames": [one["id"], two["id"]], "arrow": "checked by"}])
    assert two["x"] > one["x"] + one["width"]               # side by side, one act
    assert any(e.get("text") == "Act 1 · the principles" for e in d.els)
    assert any(e.get("backgroundColor") == KEY for e in d.els)          # the key point has the slight colour
    assert any(e.get("strokeColor") == "#e03131" for e in d.els)        # an open point is red
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "studio" / "s99-test" / "s99-test.excalidraw"
        out.parent.mkdir(parents=True)
        d.write(out, "test_draw.py")
        rows = Drawing.density_of(out)
        assert [r[0][0] for r in rows] == ["①", "②"]
        assert json.loads(out.read_text())["elements"]
        from check import check
        r = check(out)
        assert r["frames"] == 2 and r["③"].startswith("✅")             # an act named, an arrow between frames
        assert r["rows"][1]["④"].startswith("👤")                        # folder-tree lines: a person decides


def test_a_slide_draft_keeps_its_own_sizes():
    from check import check
    d = Drawing()
    f = d.frame("2 · the slides", 2250, 3956)                 # far past one screen, as a slide draft is
    d.text(40, 40, "a half-size slide", 9)
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "studio" / "s61-deck" / "s61-deck.excalidraw"
        out.parent.mkdir(parents=True)
        d.write(out, "test_draw.py")
        r = check(out)
        assert r["slide"] and "slide draft" in r["③"]
        assert all(r["rows"][0][p].startswith("🎞️") for p in ("①", "⑤", "⑥"))


def test_the_floors():
    assert FLOOR >= MAP_FLOOR > 0


def test_check_reads_what_canvas_marks():
    from check import check
    import canvas
    d = Drawing()
    one = d.frame("① a long piece read down", 2560, 3000)
    canvas.reads_down(one)                                    # canvas's own mark: customData reads = down
    d.text(40, 40, "a frame title", 60)
    d.text(40, 200, "a green change note in small words", 16, color=canvas.GREEN)
    d.key(40, 300, 400, 80)                                  # the key point
    two, three = d.frame("② the middle"), d.frame("③ the end")
    for f, x in ((one, 0), (two, 3000), (three, 6000)):
        f["x"], f["y"] = x, 0
    d.fid = None                                              # an arrow between frames is in none
    d.line([(2560, 700), (6000, 700)])                        # ① to ③, straight through ②
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "studio" / "s98-test" / "s98-test.excalidraw"
        out.parent.mkdir(parents=True)
        d.write(out, "test_draw.py")
        r = check(out)
        assert r["rows"][0]["①"].startswith("✅ read down")                # its width fits; its height may not
        assert "under 20 px: 0%" in r["rows"][0]["⑤"]                       # a green note is not counted
        assert r["③"].startswith("❌") and "runs through '② the middle'" in r["③"]


def test_chinese_is_measured_wrapped_and_counted():
    """Excalidraw cuts a text at its width, so Chinese is measured at a full em; a Chinese line wraps; two Chinese
    characters count as one word, and each folder of a path as one (asked 261012: "this is not complete")."""
    d = Drawing()
    d.frame("① 中文")
    e = d.text(0, 0, "研究主线：每一项从原件到产出", 60)
    assert e["width"] >= 14 * 60
    assert len(Drawing.wrap("表格 / 个人事实 / 原件 / 陈述 / 最终目录 / 律师组包与签字", 300, 24).split("\n")) > 1
    assert Drawing.words_in("研究主线") == 2 and Drawing.words_in("related/materials/j01") == 3
    assert Drawing.words_in("🎯 Target glucose") == 2 and Drawing.words_in("🎛️ 🗓️ ✅ done") == 1   # an emoji is no word


def test_principle_7_few_words_in_a_workflow():
    """A workflow of short names passes ⑦; the same steps carrying detail lines fail it, by the badge and by check."""
    from check import check_frame
    from draw import SMALL
    for lines, ok in (([], True), ([f"detail line {i} about this step in small words" for i in range(4)], False)):
        d = Drawing()
        f = d.frame("① a workflow")
        d.heading("🔁 A workflow")
        steps = [{"title": f"step {i}", "lines": lines} for i in range(5)]
        d.flow(steps, 40, 200, 2480, title=34, leaf=SMALL - 4, labels=["then"] * 4)
        d.key(40, 700, 600, 80)
        d.badge(f)
        row = check_frame(d.els, f)
        assert row["kind"] == "map" and row["⑦"].startswith("✅" if ok else "❌"), row["⑦"]
        badge = [e["text"] for e in d.els if str(e.get("text", "")).startswith(("✅ a map", "❌ a map"))]
        assert badge and badge[0].startswith("✅" if ok else "❌")


def test_a_node_that_starts_like_the_badge_is_counted():
    from check import check
    d = Drawing()
    f = d.frame("① a map")
    d.text(40, 22, "a frame title", 60)
    d.key(40, 200, 600, 120)
    d.text(60, 220, "📊 ⑥ A text frame's density, measured", 38)        # a node, not the badge
    d.text(60, 420, "🪶 ⑦ Few words in a workflow", 38)
    for i in range(3):
        d.box(40 + 700 * i, 600, 500, 120)
        d.line([(540 + 700 * i, 660), (740 + 700 * i, 660)])
    d.badge(f)
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "studio" / "s97-test" / "s97-test.excalidraw"
        out.parent.mkdir(parents=True)
        d.write(out, "test_draw.py")
        row = check(out)["rows"][0]
        assert row["kind"] == "map" and row["words"] == 3 + 6 + 6          # the title and both nodes (their emoji are no words); not the badge


def test_s00_keeps_its_own_words():
    from check import check
    d = Drawing()
    f = d.frame("① the index")
    d.text(40, 22, "an index", 60)
    d.key(40, 200, 600, 120)
    for i in range(3):
        d.box(40 + 700 * i, 600, 500, 120)
        d.line([(540 + 700 * i, 660), (740 + 700 * i, 660)])
    d.text(40, 900, " ".join(["topic"] * 260), 21)                        # far past 200 words, all small
    d.badge(f)
    with tempfile.TemporaryDirectory() as tmp:
        for folder, own in (("s00-background-and-index", True), ("s07-a-topic", False)):
            out = Path(tmp) / "studio" / folder / f"{folder}.excalidraw"
            out.parent.mkdir(parents=True)
            d.write(out, "test_draw.py")
            row = check(out)["rows"][0]
            assert row["⑦"].startswith("🗂️") if own else row["⑦"].startswith("❌")


def test_a_detail_frame_is_measured_by_6_not_7():
    """The same wordy map fails ⑦; marked Drawing.detail it is held to ⑥'s text floor instead."""
    from check import check_frame
    from draw import FLOOR
    rows = []
    for mark in (False, True):
        d = Drawing()
        f = d.frame("r04 · a video in full")
        d.heading("r04 · a video in full")
        steps = [{"title": f"step {i}", "lines": [f"what the video says at this step, in full words, part {k}" for k in range(4)]}
                 for i in range(5)]
        d.flow(steps, 40, 200, 2480, title=34, leaf=28, labels=["then"] * 4)
        d.key(40, 900, 600, 80)
        if mark:
            Drawing.detail(f)
        f["height"] = 1000
        d.badge(f)
        rows.append(check_frame(d.els, f))
    assert rows[0]["kind"] == "map" and rows[0]["⑦"].startswith("❌")
    assert rows[1]["⑦"].startswith("📖") and "floor 88" in rows[1]["⑥"]     # 120 × (24 / 28)², its leaves at 28 px
    assert Drawing.detail_floor([], "none") == FLOOR


def test_a_small_frame_that_explains_is_not_held_to_a_screen():
    """JL 261013: "主次分明 … 一个很大的 frame，然后有一些小的 frame 是解释这些大的 frame 的" and "大小有致". A frame marked
    canvas.explains may be small and roomy: check.py's ① (a third of a screen), ⑥ and ⑦ do not hold it; ⑤ needs no key
    point of its own. An unmarked frame of the same size still fails ①."""
    from check import check
    from draw import canvas
    d = Drawing()
    small = d.frame("② a small note", 900, 500)
    d.text(40, 30, "One note that explains the main frame.", 30)
    canvas.explains(small)
    plain = d.frame("③ a small frame, not marked", 900, 500)
    d.text(40, 30, "One note, unmarked.", 30)
    out = Path(tempfile.mkdtemp()) / "t.excalidraw"
    d.write(out, "test")
    rows = {r["name"][0]: r for r in check(out)["rows"]}
    assert rows["②"]["①"].startswith("✅ small on purpose") and rows["②"]["⑥"].startswith("—")
    assert rows["②"]["⑤"].startswith("✅")
    assert rows["③"]["①"].startswith("❌")
