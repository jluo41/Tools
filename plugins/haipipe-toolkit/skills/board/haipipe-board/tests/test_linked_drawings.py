import importlib.util
import json
import unittest
from pathlib import Path
from unittest import mock

MODULE_PATH = Path(__file__).parents[1] / "cli" / "draw.py"
SPEC = importlib.util.spec_from_file_location("board_draw", MODULE_PATH)
draw = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(draw)


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def fixture_board(tmp_path):
    board = tmp_path / "board"
    write(
        board / "board.md",
        """# Linked drawing fixture

## Pages
### QA · First group
QA1-one.md
QA2-two.md
QA3-empty.md
### QB · Second group
QB1-three.md
""",
    )
    for folder, page, title in (
        ("QA-first", "QA1-one.md", "One"),
        ("QA-first", "QA2-two.md", "Two"),
        ("QA-first", "QA3-empty.md", "Empty"),
        ("QB-second", "QB1-three.md", "Three"),
    ):
        write(
            board / folder / page,
            f"# {title}\nstate: 🔴 OPEN\nowner: CC\n\n## Opening\nWhat?\n\n## Aims\n### P · Page-level\n- P1 · Exist.\n  **Done when:** It exists.\n\n## States\n### P · Page-level\n- ⬜ P1 · Not started.\n",
        )
    scene = {
        "type": "excalidraw",
        "version": 2,
        "source": "fixture",
        "elements": [
            {"id": "title-a", "type": "text", "text": "QA · First group", "x": 10, "y": 5},
            {"id": "frame-a1", "type": "frame", "name": "QA1", "x": 100, "y": 200},
            {"id": "same", "type": "text", "text": "one", "x": 120, "y": 230, "frameId": "frame-a1"},
            {"id": "frame-a2", "type": "frame", "name": "QA2", "x": 400, "y": 200},
            {"id": "arrow", "type": "arrow", "x": 420, "y": 230, "frameId": "frame-a2", "startBinding": {"elementId": "frame-a2"}},
            {"id": "relation", "type": "arrow", "x": 300, "y": 250, "startBinding": {"elementId": "frame-a1"}, "endBinding": {"elementId": "frame-a2"}},
            {"id": "title-b", "type": "text", "text": "QB · Second group", "x": 10, "y": 500},
            {"id": "frame-b1", "type": "frame", "name": "QB1", "x": 100, "y": 600},
            {"id": "same-b", "type": "text", "text": "three", "x": 120, "y": 630, "frameId": "frame-b1"},
        ],
        "appState": {"gridSize": None, "viewBackgroundColor": "#fff"},
        "files": {},
    }
    write(board / "board.excalidraw", json.dumps(scene))
    return board, scene


def append_scene_element(board, element):
    path = board / "board.excalidraw"
    scene = json.loads(path.read_text(encoding="utf-8"))
    scene["elements"].append(element)
    path.write_text(json.dumps(scene), encoding="utf-8")


class LinkedDrawingTest(unittest.TestCase):
    def test_split_is_non_destructive_and_round_trips(self):
        import tempfile
        with tempfile.TemporaryDirectory() as root:
            board, source = fixture_board(Path(root))
            before = (board / "board.excalidraw").read_bytes()
            self.assertEqual(draw.split(board, board / "board.excalidraw", apply=True), 0)
            self.assertTrue((board / "QA-first" / "draw" / "group.excalidraw").is_file())
            self.assertTrue((board / "QA-first" / "draw" / "QA2.excalidraw").is_file())
            self.assertTrue((board / "QB-second" / "draw" / "QB1.excalidraw").is_file())
            self.assertEqual((board / "board.excalidraw").read_bytes(), before)
            self.assertEqual(draw.compose_data(board, namespace=False)["elements"], source["elements"])

    def test_compose_namespaces_ids_and_references(self):
        import tempfile
        with tempfile.TemporaryDirectory() as root:
            board, _ = fixture_board(Path(root))
            draw.split(board, board / "board.excalidraw", apply=True)
            scene = draw.compose_data(board, namespace=True)
            by_text = {element.get("text"): element for element in scene["elements"] if element.get("text")}
            self.assertEqual(by_text["one"]["id"], "QA1::same")
            arrow = next(element for element in scene["elements"] if element["type"] == "arrow")
            self.assertEqual(arrow["startBinding"]["elementId"], "QA2::frame-a2")
            self.assertEqual((arrow["x"], arrow["y"]), (420, 230))
            relation = next(element for element in scene["elements"] if element["id"] == "QA::relation")
            self.assertEqual(relation["startBinding"]["elementId"], "QA1::frame-a1")
            self.assertEqual(relation["endBinding"]["elementId"], "QA2::frame-a2")

    def test_split_refuses_any_overwrite_before_writing(self):
        import tempfile
        with tempfile.TemporaryDirectory() as root:
            board, _ = fixture_board(Path(root))
            occupied = board / "QA-first" / "draw" / "QA1.excalidraw"
            write(occupied, "mine")
            with self.assertRaisesRegex(draw.DrawError, "refusing to overwrite"):
                draw.split(board, board / "board.excalidraw", apply=True)
            self.assertEqual(occupied.read_text(encoding="utf-8"), "mine")
            self.assertFalse((board / "QB-second" / "draw" / "group.excalidraw").exists())

    def test_split_rolls_back_a_mid_write_failure(self):
        import tempfile
        with tempfile.TemporaryDirectory() as root:
            board, _ = fixture_board(Path(root))
            existing_empty_dir = board / "QA-first" / "draw"
            existing_empty_dir.mkdir()
            original = draw.write_scene_exclusive
            calls = 0

            def fail_second(path, scene):
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("injected write failure")
                original(path, scene)

            with mock.patch.object(draw, "write_scene_exclusive", side_effect=fail_second):
                with self.assertRaisesRegex(draw.DrawError, "split rolled back"):
                    draw.split(board, board / "board.excalidraw", apply=True)
            self.assertEqual(list(board.glob("*/draw/*.excalidraw")), [])
            self.assertTrue(existing_empty_dir.is_dir())

    def test_exclusive_create_never_deletes_an_existing_target(self):
        import tempfile
        with tempfile.TemporaryDirectory() as root:
            target = Path(root) / "scene.excalidraw"
            target.write_text("mine", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                draw.write_scene_exclusive(target, {"type": "excalidraw"})
            self.assertEqual(target.read_text(encoding="utf-8"), "mine")

    def test_empty_page_still_gets_an_independent_source(self):
        import tempfile
        with tempfile.TemporaryDirectory() as root:
            board, _ = fixture_board(Path(root))
            draw.split(board, board / "board.excalidraw", apply=True)
            scene = json.loads((board / "QA-first" / "draw" / "QA3.excalidraw").read_text())
            self.assertEqual(scene["haipipe"]["page"]["id"], "QA3")
            self.assertEqual(scene["elements"], [])

    def test_sync_adds_only_pages_newly_declared_by_board_md(self):
        import tempfile
        with tempfile.TemporaryDirectory() as root:
            board, _ = fixture_board(Path(root))
            draw.split(board, board / "board.excalidraw", apply=True)
            board_md = board / "board.md"
            board_md.write_text(
                board_md.read_text(encoding="utf-8").replace(
                    "QA3-empty.md\n", "QA3-empty.md\nQA4-new.md\n"
                ),
                encoding="utf-8",
            )
            write(
                board / "QA-first" / "QA4-new.md",
                "# New\nstate: 🔴 OPEN\nowner: CC\n\n## Opening\nWhat?\n",
            )
            legacy_before = (board / "board.excalidraw").read_bytes()
            existing_before = (board / "QA-first" / "draw" / "QA1.excalidraw").read_bytes()
            self.assertEqual(draw.sync(board, apply=True), 0)
            page = draw.read_scene(board / "QA-first" / "draw" / "QA4.excalidraw")
            group = draw.read_scene(board / "QA-first" / "draw" / "group.excalidraw")
            self.assertEqual(page["haipipe"]["page"]["id"], "QA4")
            self.assertEqual(page["elements"], [])
            self.assertEqual([item["page"] for item in group["haipipe"]["imports"]],
                             ["QA1", "QA2", "QA3", "QA4"])
            self.assertEqual((board / "QA-first" / "draw" / "QA1.excalidraw").read_bytes(),
                             existing_before)
            self.assertEqual((board / "board.excalidraw").read_bytes(), legacy_before)

    def test_live_group_composition_tags_and_locks_page_elements(self):
        import tempfile
        with tempfile.TemporaryDirectory() as root:
            board, _ = fixture_board(Path(root))
            draw.split(board, board / "board.excalidraw", apply=True)
            group_path = board / "QA-first" / "draw" / "group.excalidraw"
            group = draw.read_scene(group_path)
            group["haipipe"]["imports"][0]["placement"].update(
                {"x": 10, "y": 20, "scale": 2}
            )
            draw.write_scene(group_path, group)
            scene = draw.compose_group_data(group_path, runtime=True)
            page_text = next(element for element in scene["elements"]
                             if element.get("text") == "one")
            group_title = next(element for element in scene["elements"]
                               if element.get("text") == "QA · First group")
            self.assertEqual((page_text["x"], page_text["y"]), (50, 80))
            self.assertTrue(page_text["locked"])
            self.assertEqual(page_text["customData"]["haipipeRuntime"]["owner"], "QA1")
            self.assertEqual(group_title["customData"]["haipipeRuntime"]["owner"], "QA")
            self.assertFalse(group_title.get("locked", False))

    def test_split_rejects_a_dangling_group_relation(self):
        import tempfile
        with tempfile.TemporaryDirectory() as root:
            board, _ = fixture_board(Path(root))
            append_scene_element(board, {
                "id": "dangling", "type": "arrow", "x": 0, "y": 0,
                "startBinding": {"elementId": "frame-a1"},
                "endBinding": {"elementId": "missing"},
            })
            with self.assertRaisesRegex(draw.DrawError, "unresolved reference.*missing"):
                draw.split_plan(board, board / "board.excalidraw")

    def test_split_rejects_an_ownerless_group_element(self):
        import tempfile
        with tempfile.TemporaryDirectory() as root:
            board, _ = fixture_board(Path(root))
            append_scene_element(board, {
                "id": "ownerless", "type": "rectangle", "x": 0, "y": 0,
            })
            with self.assertRaisesRegex(draw.DrawError, "no unambiguous Group owner"):
                draw.split_plan(board, board / "board.excalidraw")

    def test_split_rejects_a_cross_group_relation(self):
        import tempfile
        with tempfile.TemporaryDirectory() as root:
            board, _ = fixture_board(Path(root))
            append_scene_element(board, {
                "id": "cross-group", "type": "arrow", "x": 0, "y": 0,
                "startBinding": {"elementId": "frame-a1"},
                "endBinding": {"elementId": "frame-b1"},
            })
            with self.assertRaisesRegex(draw.DrawError, "binds across Groups: QA, QB"):
                draw.split_plan(board, board / "board.excalidraw")

    def test_split_rejects_an_explicit_cross_group_relation(self):
        import tempfile
        with tempfile.TemporaryDirectory() as root:
            board, _ = fixture_board(Path(root))
            append_scene_element(board, {
                "id": "cross-explicit", "type": "arrow", "x": 0, "y": 0,
                "customData": {"haipipeOwner": "QA"},
                "startBinding": {"elementId": "frame-a1"},
                "endBinding": {"elementId": "frame-b1"},
            })
            with self.assertRaisesRegex(draw.DrawError, "owned by QA binds across Groups"):
                draw.split_plan(board, board / "board.excalidraw")

    def test_split_rejects_an_unresolved_page_binding(self):
        import tempfile
        with tempfile.TemporaryDirectory() as root:
            board, _ = fixture_board(Path(root))
            append_scene_element(board, {
                "id": "page-dangling", "type": "arrow", "x": 0, "y": 0,
                "frameId": "frame-a1",
                "startBinding": {"elementId": "missing"},
            })
            with self.assertRaisesRegex(draw.DrawError, "unresolved reference.*missing"):
                draw.split_plan(board, board / "board.excalidraw")

    def test_split_rejects_a_page_binding_to_another_page(self):
        import tempfile
        with tempfile.TemporaryDirectory() as root:
            board, _ = fixture_board(Path(root))
            append_scene_element(board, {
                "id": "page-cross", "type": "arrow", "x": 0, "y": 0,
                "frameId": "frame-a1",
                "startBinding": {"elementId": "frame-a2"},
            })
            with self.assertRaisesRegex(draw.DrawError, "binds outside QA1: frame-a2"):
                draw.split_plan(board, board / "board.excalidraw")


if __name__ == "__main__":
    unittest.main()
