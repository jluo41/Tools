import json
import sys
import tempfile
import unittest
from pathlib import Path


ENGINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ENGINE))

from cli.draw import SCHEMA, read_scene  # noqa: E402
from live.autodraw import autodraw  # noqa: E402
from live.chat import drawing_owner_context  # noqa: E402
from live.xcal import XcalMixin  # noqa: E402


def write_scene(path, scene):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(scene), encoding="utf-8")


def linked_fixture(root):
    draw = root / "G-one" / "draw"
    page = {
        "type": "excalidraw", "version": 2, "source": "test",
        "elements": [{"id": "p-box", "type": "rectangle", "x": 0, "y": 0,
                      "width": 100, "height": 50}],
        "appState": {}, "files": {},
        "haipipe": {"schema": SCHEMA, "kind": "page",
                    "page": {"id": "G1", "markdown": "G-one/G1.md"},
                    "migration": {"sourceIndexes": {}}},
    }
    group = {
        "type": "excalidraw", "version": 2, "source": "test",
        "elements": [{"id": "g-title", "type": "text", "text": "Group",
                      "x": 0, "y": -40}],
        "appState": {}, "files": {},
        "haipipe": {"schema": SCHEMA, "kind": "group",
                    "group": {"id": "G", "name": "G · One"},
                    "imports": [{"page": "G1", "source": "G1.excalidraw",
                                 "placement": {"x": 10, "y": 20, "scale": 1,
                                               "visible": True}}],
                    "migration": {"sourceIndexes": {}}},
    }
    write_scene(draw / "G1.excalidraw", page)
    write_scene(draw / "group.excalidraw", group)
    return draw / "group.excalidraw", draw / "G1.excalidraw"


class Live(XcalMixin):
    XMIME = {"image/png": ".png"}

    def __init__(self, root):
        self.root = root.resolve()


class LinkedLiveTest(unittest.TestCase):
    def test_missing_folded_page_scene_mints_only_in_studio_draw(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = root / "G-one" / "G1-page" / "G1-page.md"
            page.parent.mkdir(parents=True)
            page.write_text("# Page\n", encoding="utf-8")
            live = Live(root)
            canonical = page.parent / "studio" / "draw" / "G1.excalidraw"
            legacy = page.parent / "draw" / "G1.excalidraw"

            scene = live.mint_page_scene(canonical)

            self.assertIsNotNone(scene)
            self.assertTrue(canonical.is_file())
            self.assertIsNone(live.mint_page_scene(legacy))
            self.assertFalse(legacy.exists())

    def test_chat_receives_the_same_group_and_page_owner_addresses(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _, _ = linked_fixture(root)
            markdown = root / "G-one" / "G1.md"
            markdown.write_text("# Page\n", encoding="utf-8")
            group_context = "\n".join(drawing_owner_context(root / "G-one", root))
            page_context = "\n".join(drawing_owner_context(markdown, root))
            self.assertIn("G-one/draw/group.excalidraw", group_context)
            self.assertIn("G1 -> G-one/draw/G1.excalidraw", group_context)
            self.assertIn("Drawing owner: Page G1 -> G-one/draw/G1.excalidraw",
                          page_context)
            self.assertIn("Never edit the derived composed scene", group_context)

    def test_chat_names_flat_folded_draw_as_read_only_migration_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = root / "G-one" / "G1-page" / "G1-page.md"
            page.parent.mkdir(parents=True)
            page.write_text("# Page\n", encoding="utf-8")
            legacy = page.parent / "draw" / "G1.excalidraw"
            write_scene(legacy, {
                "type": "excalidraw", "version": 2, "elements": [],
                "appState": {}, "files": {},
            })
            (page.parent / "studio" / "draw").mkdir(parents=True)

            context = "\n".join(drawing_owner_context(page, root))

            self.assertIn("G-one/G1-page/draw/G1.excalidraw", context)
            self.assertIn("READ ONLY", context)
            self.assertIn("studio/draw", context)

            canonical = page.parent / "studio" / "draw" / "G1.excalidraw"
            write_scene(canonical, {
                "type": "excalidraw", "version": 2, "elements": [],
                "appState": {}, "files": {},
            })
            context = "\n".join(drawing_owner_context(page, root))
            self.assertIn("G-one/G1-page/studio/draw/G1.excalidraw", context)
            self.assertNotIn("Legacy Page drawing", context)

    def test_canonical_open_migrates_legacy_scene_without_changing_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = root / "G-one" / "G1-page" / "G1-page.md"
            page.parent.mkdir(parents=True)
            page.write_text("# Page\n", encoding="utf-8")
            legacy = page.parent / "draw" / "G1.excalidraw"
            source = {
                "type": "excalidraw", "version": 2,
                "elements": [{"id": "kept", "type": "text", "text": "mine"}],
                "appState": {}, "files": {},
                "haipipe": {"schema": SCHEMA, "kind": "page",
                            "page": {"id": "G1", "markdown": "G-one/G1-page/G1-page.md"}},
            }
            write_scene(legacy, source)
            before = legacy.read_bytes()
            canonical = page.parent / "studio" / "draw" / "G1.excalidraw"

            migrated = Live(root).mint_page_scene(canonical)

            self.assertEqual(migrated["elements"][0]["text"], "mine")
            self.assertTrue(canonical.is_file())
            self.assertEqual(legacy.read_bytes(), before)

    def test_linked_save_refuses_a_flat_folded_page_scene(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = root / "G-one" / "G1-page" / "G1-page.md"
            page.parent.mkdir(parents=True)
            page.write_text("# Page\n", encoding="utf-8")
            legacy = page.parent / "draw" / "G1.excalidraw"
            source = {
                "type": "excalidraw", "version": 2, "elements": [],
                "appState": {}, "files": {},
                "haipipe": {"schema": SCHEMA, "kind": "page",
                            "page": {"id": "G1", "markdown": "G-one/G1-page/G1-page.md"}},
            }
            write_scene(legacy, source)
            live = Live(root)

            result = live.save_linked_page(
                {"owner_kind": "page", "owner_id": "G1", "elements": [],
                 "base_revision": live.scene_revision(legacy)},
                legacy, source,
            )

            self.assertFalse(result["ok"])
            self.assertIn("read-only", result["err"])

            generated = autodraw(root, {
                "scene": str(legacy.relative_to(root)), "prompt": "draw it"
            })
            self.assertFalse(generated["ok"])
            self.assertIn("read-only", generated["err"])

    def test_group_runtime_composes_every_page_and_names_the_save_owner(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            group_path, _ = linked_fixture(root)
            live = Live(root)
            scene = live.linked_runtime_scene(group_path, read_scene(group_path))
            self.assertEqual(scene["haipipe"]["runtime"]["owner"], "G")
            self.assertEqual(scene["haipipe"]["runtime"]["ownerKind"], "group")
            self.assertEqual(scene["haipipe"]["imports"][0]["board"],
                             "G-one/draw/G1.excalidraw")
            page_element = next(e for e in scene["elements"]
                                if e["customData"]["haipipeRuntime"]["kind"] == "page")
            self.assertTrue(page_element["locked"])
            self.assertEqual((page_element["x"], page_element["y"]), (10, 20))

    def test_page_save_changes_only_the_page_and_rejects_a_stale_base(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            group_path, page_path = linked_fixture(root)
            live = Live(root)
            group_before = group_path.read_bytes()
            page_scene = read_scene(page_path)
            revision = live.scene_revision(page_path)
            payload = {"board": "G-one/draw/G1.excalidraw", "owner_kind": "page",
                       "owner_id": "G1", "mode": "page-source",
                       "base_revision": revision,
                       "elements": [{"id": "p-box", "type": "rectangle", "x": 7,
                                     "y": 0, "width": 100, "height": 50}]}
            saved = live.save_linked_page(payload, page_path, page_scene)
            self.assertTrue(saved["ok"])
            self.assertEqual(read_scene(page_path)["elements"][0]["x"], 7)
            self.assertEqual(group_path.read_bytes(), group_before)
            stale = live.save_linked_page(payload, page_path, read_scene(page_path))
            self.assertTrue(stale["conflict"])
            self.assertEqual(read_scene(page_path)["elements"][0]["x"], 7)

    def test_arrange_changes_only_group_placement(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            group_path, page_path = linked_fixture(root)
            live = Live(root)
            page_before = page_path.read_bytes()
            revision = live.group_revision(group_path)
            saved = live.save_linked_group(
                {"owner_kind": "group", "owner_id": "G", "mode": "arrange",
                 "base_revision": revision,
                 "placement": {"page": "G1", "x": 90, "y": 120,
                               "scale": 1.5, "visible": False}},
                group_path, read_scene(group_path))
            self.assertTrue(saved["ok"])
            placement = read_scene(group_path)["haipipe"]["imports"][0]["placement"]
            self.assertEqual(placement, {"x": 90.0, "y": 120.0, "scale": 1.5,
                                         "visible": False})
            self.assertEqual(page_path.read_bytes(), page_before)

    def test_group_layer_save_ignores_imported_page_elements(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            group_path, page_path = linked_fixture(root)
            live = Live(root)
            page_before = page_path.read_bytes()
            composed = live.linked_runtime_scene(group_path, read_scene(group_path))
            elements = composed["elements"]
            group_element = next(e for e in elements
                                 if e["customData"]["haipipeRuntime"]["kind"] == "group")
            page_element = next(e for e in elements
                                if e["customData"]["haipipeRuntime"]["kind"] == "page")
            group_element["text"] = "Changed Group"
            page_element["x"] = 999
            saved = live.save_linked_group(
                {"owner_kind": "group", "owner_id": "G", "mode": "group-source",
                 "base_revision": composed["haipipe"]["runtime"]["revision"],
                 "elements": elements}, group_path, read_scene(group_path))
            self.assertTrue(saved["ok"])
            self.assertEqual(read_scene(group_path)["elements"][0]["text"], "Changed Group")
            self.assertEqual(page_path.read_bytes(), page_before)


if __name__ == "__main__":
    unittest.main()
