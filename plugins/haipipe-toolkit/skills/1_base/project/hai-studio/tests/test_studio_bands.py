"""Blueprint bands are data shared by the writer, renderer and structure model."""
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))
import new_topic

ROOT = next(p for p in SKILL.parents if (p / "plugins/haipipe-toolkit").is_dir())
sys.path.insert(0, str(ROOT / "plugins/haipipe-toolkit/servers/_host"))
from host_paths import bootstrap
bootstrap()
from live import studio_types


class SharedBandsTest(unittest.TestCase):
    def test_writer_and_page_agree_without_any_type_faces(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            block = root / "examples/Project-Test/blueprint/b01_test"
            block.mkdir(parents=True)
            (block / "board.md").write_text("# Test\nbands: s7N Local override\n")
            registry = root / studio_types.HOME / "delivery/page-spec/studio-bands.json"
            registry.parent.mkdir(parents=True)
            registry.write_text(json.dumps({"bands": [
                {"band": "s7N", "name": "Studio Type", "emoji": "🏷️"},
                {"band": "s9N", "name": "Guide", "emoji": "🧭"}]}))
            self.assertEqual(new_topic.studio_types(block),
                             {key: value[1] for key, value in studio_types.studio_types(root).items()})
            self.assertEqual(new_topic.titled(block, 71, "Specialized type"), "Studio Type: Specialized type")
            self.assertEqual(new_topic.titled(block, 99, "Using this Block"), "Guide: Using this Block")
            self.assertFalse(list(block.glob("s7*")))

    def test_actual_work_does_not_inherit_blueprint_bands(self):
        with tempfile.TemporaryDirectory() as tmp:
            block = Path(tmp) / "work/b01_actual"
            block.mkdir(parents=True)
            (block / "board.md").write_text("# Test\nbands: s0N Learning topics\n")
            self.assertEqual(new_topic.titled(block, 1, "Example"), "Learning topics: Example")
            self.assertEqual(new_topic.titled(block, 71, "Example"), "Example")

    def test_repository_consumers_and_active_types(self):
        home = ROOT / studio_types.HOME
        spec = importlib.util.spec_from_file_location("structure_bands_check", home / "delivery/structure/build_organization.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        page = studio_types.studio_types(ROOT)
        self.assertEqual(new_topic.studio_types(home), {d: n for d, (_, n, _) in page.items()})
        self.assertEqual(module.BLUEPRINT_BANDS,
                         tuple((f"{e} {n}".strip(), f"s{d}N", h) for d, (e, n, h) in page.items()))
        for number in (75, 77, 79):
            self.assertFalse(list(home.glob(f"s{number}-studio-type-*")))
        for number in (71, 72, 73, 74, 76, 78):
            self.assertEqual(len(list(home.glob(f"s{number}-studio-type-*"))), 1)
        self.assertTrue((home / "s99-guide-view/s99-guide-view.md").is_file())
