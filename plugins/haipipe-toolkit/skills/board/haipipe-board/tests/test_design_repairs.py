"""Behavioral regressions for the Design contract and presenter repair."""
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from live import design_actions as acts
from live.design import design_snapshot, perform_action, render_design, _render_for
from live.designboard import bundle_rows, design_board_snapshot, render_design_board
from tests.fixture_design_v2 import FolderBuilder, ItemSpec, audit, digest
from tests.test_design_plugin import legacy_fixture, v2_fixture


def spec(stage="generated", **fields):
    values = dict(id="ITEM01", title="Library pickup", kind="sms",
                  goal="Make the pickup action clear", audience="members", job="review pickup",
                  content="Review your pickup time. Reply STOP to opt-out",
                  criteria=[{"id": "tone", "kind": "semantic", "description": "One clear action",
                             "observation": "Read the message as its intended recipient.",
                             "pass_when": "One next action is explicit and optional choices are clear.",
                             "fail_when": "The text presents multiple competing next actions.",
                             "not_verifiable_when": "The intended recipient or action is not supplied."}],
                  acceptance=["One clear action"], stage=stage)
    values.update(fields)
    return ItemSpec(**values)


def files(folder):
    return {str(p.relative_to(folder)): p.read_bytes() for p in folder.rglob("*") if p.is_file()}


def pin_render(folder, run):
    out = folder / "results" / run
    manifest = acts._load(out / "result.yaml")
    source = out / manifest["artifacts"][0]["path"]
    image = out / "render/screen.png"
    image.parent.mkdir()
    image.write_bytes(b"synthetic image bytes")
    index = image.parent / "manifest.json"
    index.write_text(json.dumps([{
        "item": "ITEM01", "candidate": run, "version": 1,
        "source": "../" + manifest["artifacts"][0]["path"], "sha256": digest(source),
        "render": image.name, "render_sha256": digest(image)}]))
    manifest["render_manifest"] = acts._ref(out, index)
    acts._dump(out / "result.yaml", manifest)
    return image


class DesignRepairsTest(unittest.TestCase):
    def test_legacy_render_versions_remain_readable(self):
        rows = [{"candidate": "rd02_generate_item01", "picture": True, "version": value}
                for value in ("1", "2", "broken")]
        self.assertIs(_render_for(rows, "rd02_generate_item01"), rows[1])
        self.assertIsNone(_render_for(rows, "rd03_generate_item01"))

    def test_changed_verified_bytes_are_removed_from_page_board_and_csv(self):
        for changed in ("artifact", "checks", "result", "config", "render"):
            with self.subTest(changed=changed), TemporaryDirectory() as td:
                board, page, runs = v2_fixture(Path(td), specs=[spec("verified")])
                generated = page.parent / "results" / runs["ITEM01"]["generate"]
                verified = page.parent / "results" / runs["ITEM01"]["verify"]
                out = acts._load(generated / "result.yaml")
                if changed == "render":
                    image = pin_render(page.parent, runs["ITEM01"]["generate"])
                    # Updating a completed target manifest alone invalidates its Verify pin.
                    self.assertIsNotNone(image)
                else:
                    target = {"artifact": generated / out["artifacts"][0]["path"],
                              "checks": verified / "checks.yaml", "result": verified / "result.yaml",
                              "config": page.parent / "scripts/config" / (runs["ITEM01"]["verify"] + ".yaml")}[changed]
                    if changed == "result":
                        result = acts._load(target)
                        result["producer"] = "different-reviewer"
                        acts._dump(target, result)
                    else:
                        target.write_text(target.read_text() + "\n# changed after Verify\n")
                snapshot = design_snapshot(page, board)
                item = snapshot["items"][0]
                self.assertIsNone(item["ready"])
                self.assertEqual(item["state"], "records invalid")
                self.assertTrue(snapshot["audit"])
                self.assertIn("inspect recorded candidate", item["waiting"])
                self.assertNotIn("data-action=queue-verify", render_design(snapshot, "design"))
                projected = design_board_snapshot(board, board)
                self.assertEqual(projected["totals"]["ready"], 0)
                self.assertEqual(bundle_rows(projected), [])

    def test_historical_ids_survive_every_view_and_no_new_adopt_write_is_possible(self):
        with TemporaryDirectory() as td:
            board, page, runs = v2_fixture(Path(td))
            snapshot = design_snapshot(page, board)
            old = runs["ITEM01"]["adopt"]
            before = files(board)
            for rendered in (render_design(snapshot, "run"), render_design(snapshot, "design"),
                             render_design_board(design_board_snapshot(board, board), "run")):
                self.assertIn(old, rendered)
                self.assertIn("Adopt (historical)", rendered)
                self.assertNotIn(old.replace("_adopt_", "_delivery_"), rendered)
            self.assertIn(f'title="{old}"', render_design(snapshot, "design"))
            item = snapshot["items"][0]
            with self.assertRaisesRegex(acts.ActionError, "retired"):
                acts.adopt(page.parent, page.stem, item, item["runs"], "adopt", "JL", "again")
            self.assertEqual(before, files(board))

    def test_hold_release_preserves_two_decisions_and_four_total_runs(self):
        with TemporaryDirectory() as td:
            board, page = legacy_fixture(Path(td))
            item_spec = spec("verified")
            item_spec.slug = "item01"
            builder = FolderBuilder(page.parent, page.stem)
            builder.register("Library pickup", [item_spec])
            def item():
                return design_snapshot(page, board)["items"][0]
            first = acts.commission(page.parent, page.stem, item(), "JL", "wait", "hold")["run"]
            held = files(page.parent / "results" / first)
            self.assertEqual(item()["state"], "commission held")
            released, err = perform_action(page, {"action": "commission-release", "item": "ITEM01",
                                                 "actor": "JL", "words": "go"})
            self.assertIsNone(err)
            self.assertNotEqual(first, released["run"])
            self.assertEqual(held, files(page.parent / "results" / first))
            builder.counter = 2
            approval = page.parent / "results" / released["run"] / "decision.yaml"
            _, generated = builder.generate(item_spec, approval)
            builder.verify(item_spec, approval, generated)
            rows = item()["runs"]
            self.assertEqual([r["kind"] for r in rows], ["commission", "commission", "generate", "verify"])
            self.assertEqual(item()["state"], "ready")
            self.assertEqual(audit(page.parent), [])
            before = files(page.parent)
            _, err = perform_action(page, {"action": "commission-release", "item": "ITEM01", "actor": "JL"})
            self.assertIsNotNone(err)
            self.assertEqual(before, files(page.parent))

    def test_blocked_run_names_repair_owner_without_commission_controls(self):
        for operation in ("generate", "verify"):
            with self.subTest(operation=operation), TemporaryDirectory() as td:
                board, page, runs = v2_fixture(Path(td), specs=[spec("verified")])
                run = runs["ITEM01"][operation]
                runtime = page.parent / "results" / run / "runtime.yaml"
                receipt = acts._load(runtime)
                receipt.update(status="blocked", failure="missing allowed source")
                acts._dump(runtime, receipt)
                # Isolate this terminal record as the latest actual Run.
                if operation == "generate":
                    ver = runs["ITEM01"]["verify"]
                    (page.parent / "runs" / f"{ver}.yaml").unlink()
                snapshot = design_snapshot(page, board)
                item = snapshot["items"][0]
                self.assertEqual(item["state"], "blocked")
                self.assertIn(run, item["waiting"])
                self.assertIn("JL", item["waiting"])
                card = render_design(snapshot, "design")
                self.assertIn("missing allowed source", card)
                self.assertNotIn("data-action=commission-release", card)
                self.assertNotIn("data-action=queue-verify", card)
                self.assertIsNotNone(perform_action(page, {"action": "commission-release", "item": "ITEM01", "actor": "JL"})[1])

    def test_invalid_review_can_retry_but_completed_failed_review_requires_revision(self):
        for status, verdict, state in (("failed", "unresolved", "verify invalid"),
                                       ("complete", "fail", "verify failed")):
            with self.subTest(status=status), TemporaryDirectory() as td:
                board, page, runs = v2_fixture(Path(td), specs=[spec("verified")])
                out = page.parent / "results" / runs["ITEM01"]["verify"]
                checks = acts._load(out / "checks.yaml")
                checks["checks"][0]["status"] = verdict
                acts._dump(out / "checks.yaml", checks)
                result = acts._load(out / "result.yaml")
                result.update(verdict=verdict, checks=acts._ref(out, out / "checks.yaml"))
                acts._dump(out / "result.yaml", result)
                receipt = acts._load(out / "runtime.yaml")
                receipt.update(status=status, failure="unresolved check" if status == "failed" else None)
                acts._dump(out / "runtime.yaml", receipt)
                item = design_snapshot(page, board)["items"][0]
                self.assertEqual(item["state"], state)
                generated_bytes = files(page.parent / "results" / runs["ITEM01"]["generate"])
                retry, err = perform_action(page, {"action": "queue-verify", "item": "ITEM01"})
                if status == "failed":
                    self.assertIsNone(err)
                    self.assertNotEqual(retry["run"], runs["ITEM01"]["verify"])
                else:
                    self.assertIsNotNone(err)
                    revised, err = perform_action(page, {"action": "queue-revise", "item": "ITEM01", "feedback": "Make the action clearer"})
                    self.assertIsNone(err)
                    self.assertIn("_generate_", revised["run"])
                self.assertEqual(generated_bytes, files(page.parent / "results" / runs["ITEM01"]["generate"]))

    def test_revision_mode_uses_released_stance_despite_register_edit(self):
        for frozen_stance, current_stance, expected_mode in (("challenge", "generate", "challenge"),
                                                            ("generate", "challenge", "revise")):
            with self.subTest(frozen=frozen_stance), TemporaryDirectory() as td:
                example = spec(stance=frozen_stance,
                               expected="Member can name the next action" if frozen_stance == "challenge" else "",
                               falsified="Member cannot name the action" if frozen_stance == "challenge" else "")
                board, page, _ = v2_fixture(Path(td), specs=[example])
                register = page.parent / "outline" / f"{page.stem}-design-items.md"
                register.write_text(register.read_text().replace(f"stance: {frozen_stance}", f"stance: {current_stance}"))
                item = design_snapshot(page, board)["items"][0]
                released = next(r for r in item["runs"] if r["kind"] == "commission")
                ticket = acts._load(page.parent / "runs" / f"{released['id']}.yaml")
                frozen = acts._load(page.parent / ticket["inputs"][0]["path"])
                self.assertEqual(frozen["goal"], example.goal)
                queued = acts.queue_generate(page.parent, page.stem, item, item["runs"], feedback="Clarify the wording")
                derived = acts._load(page.parent / "scripts/config" / f"{queued['run']}.yaml")
                self.assertEqual(queued["mode"], expected_mode)
                self.assertEqual(derived["review_mode"], "self")
                self.assertEqual({k: v for k, v in derived.items() if k not in {"mode", "review_mode"}},
                                 {k: v for k, v in frozen.items() if k not in {"mode", "review_mode"}})
                self.assertEqual(audit(page.parent), [])

    def test_result_local_preview_is_read_only_and_only_verified_content_is_delivered(self):
        with TemporaryDirectory() as td:
            example = spec()
            board, page, runs = v2_fixture(Path(td), specs=[example])
            generated = runs["ITEM01"]["generate"]
            picture = pin_render(page.parent, generated)
            before = files(page.parent)
            snapshot = design_snapshot(page, board)
            self.assertEqual(snapshot["items"][0]["render"]["path"], picture.resolve())
            self.assertIsNone(snapshot["items"][0]["ready"])
            self.assertEqual(bundle_rows(design_board_snapshot(board, board)), [])
            self.assertIn("/results/", render_design(snapshot, "design"))
            self.assertEqual(before, files(page.parent))
            builder = FolderBuilder(page.parent, page.stem)
            builder.counter = 2
            example.stage = "verified"
            builder.verify(example, page.parent / "results" / runs["ITEM01"]["commission"] / "decision.yaml",
                           page.parent / "results" / generated / "result.yaml")
            self.assertEqual(audit(page.parent), [])
            rows = bundle_rows(design_board_snapshot(board, board))
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["draft_run"], generated)
            self.assertEqual(rows[0]["state"], "ready")
            self.assertFalse((page.parent / "delivery").exists())
            picture.write_bytes(b"tampered picture")
            self.assertIsNone(design_snapshot(page, board)["items"][0]["render"])
            self.assertIn("hash mismatch", " ".join(audit(page.parent)))
