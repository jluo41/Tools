"""Result write boundaries plus opt-in real Chrome viewport regressions.

Run browser cases with DESIGN_RENDER_BROWSER=1 and local Chrome/Playwright.
"""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch

MODULE = Path(__file__).resolve().parents[1] / "scripts/render_screen.py"
spec = importlib.util.spec_from_file_location("design_screen_renderer", MODULE)
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)


class RenderBoundaryTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="design-render-test-")
        self.root = Path(self.tmp.name).resolve()
        self.result = self.root / "results/rd02_generate_item01"
        self.html = self.result / "content/screen.html"
        self.html.parent.mkdir(parents=True)
        self.html.write_text("<html><body><button>Review pickup</button></body></html>")
        self.png = self.result / "render/screen-v1.png"
        self.manifest = self.png.parent / "manifest.json"
        self.argv = [str(MODULE), "--result-dir", str(self.result), "--html", str(self.html),
                     "--png", str(self.png), "--manifest", str(self.manifest),
                     "--item", "ITEM01", "--candidate", "rd02_generate_item01", "--version", "1"]

    def tearDown(self):
        self.tmp.cleanup()

    def invoke(self, **options):
        args = self.argv[:]
        for name, value in options.items():
            key = "--" + name.replace("_", "-")
            if key in args:
                args[args.index(key) + 1] = str(value)
            else:
                args.extend((key, str(value)))
        with patch("sys.argv", args), contextlib.redirect_stdout(io.StringIO()):
            return renderer.main()

    def assert_refused(self, expected, **options):
        before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        with patch.object(renderer, "render") as browser:
            with self.assertRaisesRegex(SystemExit, expected):
                self.invoke(**options)
            browser.assert_not_called()
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()})

    def test_every_output_stays_in_current_result(self):
        for key in ("png", "manifest", "json"):
            with self.subTest(output=key):
                self.assert_refused("current Result", **{key: self.root / "delivery/render/escape.png"})

    def test_symlink_escape_is_rejected_before_write(self):
        elsewhere = self.root / "elsewhere"
        elsewhere.mkdir()
        self.png.parent.symlink_to(elsewhere, target_is_directory=True)
        self.assert_refused("current Result")

    def test_closed_results_cannot_be_rendered(self):
        for status in ("complete", "failed", "blocked", "superseded"):
            with self.subTest(status=status):
                (self.result / "runtime.yaml").write_text("status: " + status)
                self.assert_refused("closed Result")

    def test_overwrites_and_colliding_paths_are_rejected(self):
        self.png.parent.mkdir()
        self.png.write_bytes(b"existing picture")
        self.assert_refused("exists")
        self.png.unlink()
        self.assert_refused("distinct paths", json=self.manifest)
        measurements = self.png.parent / "measurements.json"
        measurements.write_text("{}")
        self.assert_refused("measurements file", json=measurements)

    def test_existing_source_version_is_preserved(self):
        self.manifest.parent.mkdir()
        self.manifest.write_text(json.dumps([{"source": "../content/screen.html",
                                             "candidate": "rd02_generate_item01", "version": 1}]))
        self.assert_refused("source/version already exists")

    def test_dimensions_and_manifest_shape_are_checked_before_browser(self):
        for key in ("width", "height", "scale", "version"):
            with self.subTest(key=key):
                self.assert_refused("positive", **{key: 0})
        self.manifest.parent.mkdir()
        self.manifest.write_text("{}")
        self.assert_refused("list of entries")

    def test_manifest_binds_source_and_picture_without_editing_runtime(self):
        runtime = self.result / "runtime.yaml"
        runtime.write_text("status: running\n")
        metrics = dict(page_height=844, page_width=390, viewport_width=390, viewport_height=844,
                       leftmost_edge=0, last_block_bottom=80, buttons=1, links=0, controls=0,
                       smallest_tap=48, weakest_text_contrast=10, weakest_control_border=None,
                       button_label_contrast=10, fits_one_screen=True, viewport="390x844")
        def fake_render(html, png, width, height, scale):
            png.parent.mkdir(parents=True)
            png.write_bytes(b"synthetic picture")
            return metrics
        with patch.object(renderer, "render", side_effect=fake_render):
            self.assertEqual(self.invoke(json=self.png.parent / "measurements-v1.json"), 0)
        row = json.loads(self.manifest.read_text())[0]
        self.assertEqual(row["source"], "../content/screen.html")
        self.assertEqual(row["render"], "screen-v1.png")
        self.assertEqual(row["sha256"], renderer.sha(self.html))
        self.assertEqual(row["render_sha256"], renderer.sha(self.png))
        self.assertEqual(row["measured"]["viewport_width"], 390)
        self.assertEqual(runtime.read_text(), "status: running\n")
        self.assertFalse((self.root / "delivery").exists())


@unittest.skipUnless(os.environ.get("DESIGN_RENDER_BROWSER") == "1", "set DESIGN_RENDER_BROWSER=1 for local Chrome")
class RealViewportTest(unittest.TestCase):
    def render(self, markup):
        tmp = tempfile.TemporaryDirectory(prefix="design-browser-test-")
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name)
        html, png = path / "screen.html", path / "screen.png"
        html.write_text("<!doctype html><html><head><style>html,body{margin:0}body{color:#111;background:white}</style></head><body>" + markup + "</body></html>")
        metrics = renderer.render(html, png, 390, 844, 2)
        dimensions = struct.unpack(">II", png.read_bytes()[16:24])
        return metrics, dimensions

    def test_actual_viewport_and_png_are_consistent(self):
        measured, dimensions = self.render('<button style="height:48px">Review pickup</button>')
        self.assertEqual((measured["viewport_width"], measured["viewport_height"], measured["pixel_ratio"]), (390, 844, 2))
        self.assertEqual(dimensions, (780, 1688))
        self.assertTrue(measured["fits_one_screen"])
        self.assertEqual(measured["smallest_tap"], 48)

    def test_horizontal_overflow_cannot_pass_one_screen(self):
        measured, _ = self.render('<div style="width:500px;height:50px">Too wide</div>')
        self.assertEqual(measured["page_width"], 500)
        self.assertFalse(measured["fits_one_screen"])

    def test_left_and_vertical_clipping_cannot_pass_one_screen(self):
        for markup in ('<div style="position:relative;left:-12px;width:100px">Left edge</div>',
                       '<div style="height:1000px">Tall screen</div>'):
            with self.subTest(markup=markup):
                measured, _ = self.render(markup)
                self.assertFalse(measured["fits_one_screen"])

    def test_page_scripts_are_disabled_and_controls_are_measured(self):
        measured, _ = self.render('<script>document.body.innerHTML="changed"</script>'
                                 '<select style="height:52px;color:#111;background:white;border:2px solid #111"><option>10 AM</option></select>')
        self.assertEqual(measured["controls"], 1)
        self.assertEqual(measured["scripts"], 1)
        self.assertEqual(measured["smallest_tap"], 52)
        self.assertGreater(measured["weakest_text_contrast"], 4.5)
        self.assertGreater(measured["weakest_control_border"], 3)


if __name__ == "__main__":
    unittest.main()
