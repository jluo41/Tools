"""Item cards (workbench/ref/cards.md): the shared parser and writer, addresses, marks and the /_board/item-card writer."""
import multiprocessing
import tempfile
import time
import unittest
from pathlib import Path

from host_paths import bootstrap
bootstrap()
from live import item_address as IA, item_cards as IC  # noqa: E402
from live.item_card_route import item_card_act  # noqa: E402
from live.item_marks import card_slot, marks, rollup  # noqa: E402


def _block(root: Path) -> Path:
    """A Block page with j02_fit/t01_model/runs/r05_main."""
    block = root / "Project-X" / "work" / "b01_topic"
    (block / "j02_fit" / "t01_model" / "runs" / "r05_main").mkdir(parents=True)
    (block / "board.md").write_text("# b01 · Topic\n")
    return block


def _add_many(page: str, who: str, n: int) -> None:
    for i in range(n):
        IC.comment_act(Path(page), {"act": "add", "address": "j02", "text": f"{who} {i}"})


def _note_many(root: str, task: str, who: str, n: int) -> None:
    from live.draft_step_revise_notes import note_act
    for i in range(n):
        note_act(Path(root), {"task": task, "s": "S1", "act": "add", "text": f"{who} {i}"})


def _hold(path: str, seconds: float) -> None:
    with IC.locked(Path(path)):
        time.sleep(seconds)


class ParseWriteTest(unittest.TestCase):
    def test_a_comment_is_added_replied_closed_and_read_back_by_address(self):
        with tempfile.TemporaryDirectory() as tmp:
            block = _block(Path(tmp))
            code, res = IC.comment_act(block, {"act": "add", "address": "j02.t01", "text": "Why this split?",
                                               "quote": "the 1m model", "who": "Reviewer"})
            self.assertEqual((code, res["n"]), (200, "1"))
            path = IC.files(block)["comments"]
            self.assertEqual(path, block / "records" / "board-comments.md")
            text = path.read_text()
            self.assertIn("### Comment 1 · j02.t01\nQuote: the 1m model\nState: open\n- Note · ", text)
            self.assertIn(" · Reviewer: Why this split?", text)
            IC.comment_act(block, {"act": "reply", "n": "1", "was": "open", "text": "Same seed as r04."})
            IC.comment_act(block, {"act": "done", "n": "1", "was": "open"})
            card = IC.cards(block)["j02.t01"]["comments"][0]
            self.assertEqual(card["state"], "done")
            self.assertEqual([w for w, _, _ in card["thread"]], ["Note", "Note"])

    def test_the_was_guard_refuses_a_card_changed_on_disk(self):
        with tempfile.TemporaryDirectory() as tmp:
            block = _block(Path(tmp))
            IC.comment_act(block, {"act": "add", "address": "j02", "text": "x"})
            IC.comment_act(block, {"act": "done", "n": "1", "was": "open"})
            code, res = IC.comment_act(block, {"act": "reply", "n": "1", "was": "open", "text": "late"})
            self.assertEqual(code, 409)
            self.assertEqual(res["state"], "done")

    def test_a_check_keeps_the_words_and_an_edit_card_takes_accept(self):
        with tempfile.TemporaryDirectory() as tmp:
            block = _block(Path(tmp))
            IC.check_act(block, {"act": "check", "address": "j02.t01.r05", "words": "AUC 0.81"})
            self.assertEqual(IC.cards(block)["j02.t01.r05"]["checked"], "AUC 0.81")
            revise = IC.files(block)["revise"]
            revise.write_text("# b01 · revise\n\n## Pass 1 · 2026-11-14\n\n### Edit · j02 · plain name\n"
                              "Original: fit\nExpected: Fit the model\nState: proposed\n")
            card = IC.cards(block)["j02"]["edits"][0]
            self.assertEqual((card["state"], card["expected"], card["pass"]), ("proposed", "Fit the model", "Pass 1 · 2026-11-14"))
            code, _ = IC.edit_card_act(block, {"act": "accept", "card": card["head"], "was": "proposed"})
            self.assertEqual(code, 200)
            self.assertEqual(IC.cards(block)["j02"]["edits"][0]["state"], "accepted")
            code, _ = IC.edit_card_act(block, {"act": "reject", "card": card["head"], "was": "proposed"})
            self.assertEqual(code, 409)

    def test_a_writer_waits_for_the_lock(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "records" / "x-comments.md"
            held = multiprocessing.get_context("fork").Process(target=_hold, args=(str(path), 0.6))
            held.start()
            time.sleep(0.2)
            start = time.time()
            IC.edit(path, lambda t: (t + "x", None))
            held.join()
            self.assertGreater(time.time() - start, 0.3)
            self.assertEqual(path.read_text(), "x")
            self.assertEqual([p.name for p in path.parent.iterdir() if not p.name.startswith(".")], ["x-comments.md"])


    def test_two_writers_on_one_file_never_lose_a_card(self):
        ctx = multiprocessing.get_context("fork")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            block = _block(root)
            procs = [ctx.Process(target=_add_many, args=(str(block), w, 15)) for w in ("a", "b")]
            task = root / "P" / "t01_draft"
            (task / "draft" / "records").mkdir(parents=True)
            (task / "t01_draft.md").write_text("# t01 · Draft\n")
            procs += [ctx.Process(target=_note_many, args=(str(root), "P/t01_draft", w, 15)) for w in ("c", "d")]
            for pr in procs:
                pr.start()
            for pr in procs:
                pr.join()
            shared = IC.parse_comments(IC.files(block)["comments"])
            self.assertEqual(len(shared), 30)
            self.assertEqual(sorted(int(c["n"]) for c in shared), list(range(1, 31)))
            draft = IC.parse_comments(task / "draft" / "records" / "t01_draft-comments.md")
            self.assertEqual(len(draft), 30)
            self.assertEqual(len({c["n"] for c in draft}), 30)


class AddressTest(unittest.TestCase):
    def test_ladder_addresses_resolve_by_number_and_moved_lists_the_lost(self):
        with tempfile.TemporaryDirectory() as tmp:
            block = _block(Path(tmp))
            self.assertEqual(IA.resolve(block, "j02.t01.r05")["path"].name, "r05_main")
            self.assertTrue(IA.resolve(block, "j02")["exists"])
            self.assertFalse(IA.resolve(block, "j03.t01")["exists"])
            self.assertIsNone(IA.resolve(block, "RQ.H2")["exists"])          # named by its workbench
            self.assertTrue(IA.resolve(block, "RQ.H2", known={"RQ.H2"})["exists"])
            self.assertFalse(IA.resolve(block, "row 3")["exists"])
            for a in ("j02", "j09"):
                IC.comment_act(block, {"act": "add", "address": a, "text": "x"})
            self.assertEqual(IA.moved(block), ["j09"])
            self.assertEqual(IA.split("Project-X/work/b01_topic:j02", Path("."), Path(tmp))[1], "j02")


class MarksRouteTest(unittest.TestCase):
    def test_marks_draw_only_what_is_there_and_the_writer_returns_them(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            block = _block(root)
            self.assertNotIn("💬", marks("j02", IC.cards(block)))
            rel = block.relative_to(root).as_posix()
            code, res = item_card_act(root, {"page": rel, "address": "j02", "act": "add", "text": "Why?"})
            self.assertEqual(code, 200)
            self.assertIn("💬 1", res["marks"])
            self.assertIn('data-im-slot="j02"', res["slot"])
            self.assertIn("🙋 2", marks("j02", IC.cards(block), {"🙋": 2}))
            self.assertIn("<tr ", card_slot("j02", IC.cards(block), rel, cols=4))
            self.assertEqual(rollup(IC.cards(block)), "")                    # a comment is not orange
            self.assertIn("🙋 3", rollup(IC.cards(block), waiting=3))
            self.assertEqual(item_card_act(root, {"page": "../x", "address": "j02", "act": "add"})[0], 400)
            self.assertEqual(item_card_act(root, {"page": rel, "address": "row 3", "act": "add", "text": "x"})[0], 400)
            self.assertEqual(item_card_act(root, {"page": rel, "address": "j02", "act": "add", "text": "x"},
                                           read_only=True)[0], 403)


if __name__ == "__main__":
    unittest.main()
