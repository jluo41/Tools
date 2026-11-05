"""The submission Job as a shipped part of haipipe-paper (JL 261103): portal_fill.py's page and states, the scaffold
`paper_ladder.py submission`, the cover letter lookup, checklist D9, and Paper-Example's placeholder Job."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
PAPER = HERE.parents[2]
SCRIPTS = PAPER / "haipipe-paper" / "scripts"
sys.path.insert(0, str(SCRIPTS))
EXAMPLE = next((p for p in HERE.parents if (p / "blueprints").is_dir()), HERE.parents[6]) / "blueprints/Project-Ladder/paper/Paper-Example"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


F = load("portal_fill", SCRIPTS / "portal_fill.py")
L = load("paper_ladder", SCRIPTS / "paper_ladder.py")
C = load("cover_letter", PAPER / "haipipe-paper-assemble" / "scripts" / "cover_letter.py")
K = load("paper_check", SCRIPTS / "paper_check.py")


def quiet(fn, *args):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*args)


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def job_on(board: Path, fields: str, values: str, name="j21_submission_v1130_desk", writing="j11_writing_v1130_desk") -> Path:
    job = board / name
    write(job / f"{name}.md", f"# {name}\n\nfor: {writing}\nvenue: Example Journal (Example Portal)\n")
    write(job / "t02_portal-walk/runs/r01_read/result/portal-fields.yaml",
          "portal: Example Portal\ndraft_saved: is pending\nsteps:\n- step: 1 All\n  fields:\n" + fields)
    write(job / "t03_portal-fill/portal-values.yaml", values)
    return job


def field(i, now=""):
    return f"  - {{id: {i}, label: {i}, kind: text, required: true, now: {json.dumps(now)}}}\n"


def built_board(tmp, title="The Built Title", words=2000, uploads=()):
    board = Path(tmp) / "Paper-X"
    delivery = board / "delivery" / "j11_writing_v1130_desk"
    write(board / "board.md", "# X\n\n## Pages\n")
    write(board / "j11_writing_v1130_desk" / "j11_writing_v1130_desk.md", "# w\n\nvenue: Example Journal\n")
    write(board / "j11_writing_v1130_desk/t00_abstract/t00_abstract.md", f"# a\n\n### Title\n\n{title}\n\n### Abstract\n\nWords.\n")
    write(delivery / "build-manifest.json", json.dumps({"build": {"main_text_words": words, "main_tables": 2, "main_figures": 3, "citations": 9},
                                                        "portal": {"folder": "portal", "uploads": list(uploads)}}))
    return board, delivery


class States(unittest.TestCase):
    def test_every_state_and_what_the_build_disagrees_with(self):
        with tempfile.TemporaryDirectory() as tmp:
            board, delivery = built_board(tmp)
            write(delivery / "portal/Up.pdf", "x")
            write(delivery / "t00_abstract/latex/t00_abstract.tex", "\\begin{abstract}An $\\approx$ 5\\% result.\\end{abstract}")
            job = job_on(board, "".join([
                field("same", "The Built Title"), field("paste"), field("up"), field("gone"), field("ask"), field("empty"),
                field("hand"), field("old_title"), field("old_words"), field("portal_words", "1,000"), field("ok_words"),
                field("tex"), field("tex_gone"), field("leave"), field("kept", "Up.pdf")]),
                "same: {value: The Built Title, check: title}\npaste: {value: words}\nup: {file: portal/Up.pdf}\n"
                "gone: {file: portal/No.pdf}\nask: {value: x, ask: 'who?'}\nhand: {value: x, disagree: true}\n"
                "old_title: {value: An Old Title, check: title}\nold_words: {value: '1,999', check: words}\n"
                "portal_words: {value: '2,000', check: words}\nok_words: {value: '2,000', check: words}\n"
                "tex: {from_tex: t00_abstract}\ntex_gone: {from_tex: t01_x}\nleave: {value: leave unchecked}\n"
                "kept: {file: portal/Up.pdf}\nnobody: {value: x}\n")
            s = F.survey(job)
            got = {r["f"]["id"]: r for r in s["rows"]}
            want = {"same": "keep", "paste": "paste", "up": "upload", "gone": "missing", "ask": "ask", "empty": "ask",
                    "hand": "differ", "old_title": "differ", "old_words": "differ", "portal_words": "differ", "ok_words": "paste",
                    "tex": "paste", "tex_gone": "missing", "leave": "keep", "kept": "keep"}
            self.assertEqual({k: r["state"] for k, r in got.items()}, want)
            self.assertEqual(got["tex"]["text"], "An ≈ 5% result.")
            self.assertEqual(got["empty"]["ask"], "no value decided yet")
            self.assertIn("The Built Title", got["old_title"]["found"][0])
            self.assertIn("1,000", got["portal_words"]["found"][0])
            self.assertEqual(s["unknown"], ["nobody"])
            html = F.page(s)
            self.assertIn("nobody", html)
            self.assertIn("<h1>Example Journal portal</h1>", html)

    def test_a_packet_file_the_build_calls_stale_disagrees(self):
        with tempfile.TemporaryDirectory() as tmp:
            board, delivery = built_board(tmp, uploads=[{"slot": "A", "files": ["A.zip"], "state": "stale", "detail": "make it again"},
                                                        {"slot": "B", "files": ["B.pdf"], "state": "draft", "detail": "not approved"}])
            write(delivery / "portal/A.zip", "x")
            write(delivery / "portal/B.pdf", "x")
            job = job_on(board, field("a") + field("b"), "a: {file: portal/A.zip}\nb: {file: portal/B.pdf}\n")
            got = {r["f"]["id"]: r for r in F.survey(job)["rows"]}
            self.assertEqual(got["a"]["state"], "differ")
            self.assertEqual(got["b"]["state"], "upload")
            self.assertIn("not approved", got["b"]["found"][0])

    def test_no_build_means_not_checked_and_the_state_stands(self):
        with tempfile.TemporaryDirectory() as tmp:
            board = Path(tmp) / "Paper-X"
            job = job_on(board, field("t"), "t: {value: A title, check: title}\n")
            r = F.survey(job)["rows"][0]
            self.assertEqual(r["state"], "paste")
            self.assertIn("Not checked", r["found"][0])

    def test_a_broken_yaml_stops_with_its_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            job = job_on(Path(tmp) / "Paper-X", field("t"), "t: {value: y, ask: who?}\n")
            with self.assertRaises(SystemExit) as got:
                F.survey(job)
            self.assertIn("portal-values.yaml", str(got.exception))

    def test_an_unknown_check_stops(self):
        with tempfile.TemporaryDirectory() as tmp:
            job = job_on(Path(tmp) / "Paper-X", field("t"), "t: {value: x, check: colour}\n")
            with self.assertRaises(SystemExit):
                F.survey(job)

    def test_yaml_no_is_the_word_no_and_values_are_escaped(self):
        with tempfile.TemporaryDirectory() as tmp:
            job = job_on(Path(tmp) / "Paper-X", field("a") + field("b"), "a: {value: No}\nb: {value: '<script>alert(1)</script>', note: '<b>'}\n")
            s = F.survey(job)
            self.assertEqual(s["rows"][0]["text"], "No")
            html = F.page(s)
            self.assertNotIn("<script>alert", html)
            self.assertIn("\\u003cscript>alert(1)", html)
            self.assertEqual(html.count("<script"), 1)         # only the sheet's own

    def test_the_newest_walk_wins_and_a_receipt_only_with_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            board = Path(tmp) / "Paper-X"
            job = job_on(board, field("old"), "new: {value: x}\n")
            write(job / "t02_portal-walk/runs/r02_read/result/portal-fields.yaml", "portal: P\ndraft_saved: d\nsteps:\n- step: s\n  fields:\n" + field("new"))
            out = Path(tmp) / "elsewhere.html"
            quiet(F.main, [str(job), "--out", str(out)])
            self.assertIn('"id": "new"', out.read_text(encoding="utf-8"))
            self.assertFalse((board / "delivery").exists())
            run = job / "t03_portal-fill/runs/r01_fill"
            quiet(F.main, [str(job), "--run", str(run), "--started-by", "a person"])
            self.assertTrue((board / "delivery" / job.name / "portal-fill.html").is_file())
            self.assertIn("completed", (run / "result/runtime.yaml").read_text(encoding="utf-8"))

    def test_the_page_can_only_copy_and_the_generator_never_reaches_out(self):
        with tempfile.TemporaryDirectory() as tmp:
            job = job_on(Path(tmp) / "Paper-X", field("a"), "a: {value: x}\n")
            html = F.page(F.survey(job))
        self.assertNotRegex(html, r"<form|fetch\(|XMLHttpRequest|https?://")
        source = (SCRIPTS / "portal_fill.py").read_text(encoding="utf-8")
        self.assertNotRegex(source, r"(?m)^\s*(?:import|from)\s+(?:socket|urllib|requests|http|selenium|playwright|subprocess)\b")


class Scaffold(unittest.TestCase):
    def board(self, tmp):
        board = Path(tmp) / "Paper-X"
        write(board / "board.md", "# X\n\nboard-kind: paper-board\n\n## Pages\n")
        write(board / "j11_writing_v1130_desk/j11_writing_v1130_desk.md", "# w\n\nvenue: <venue>\n")
        write(board / "venues/desk/call.md", "# Some Journal · desk record\n\n| what | limit | src |\n|---|---|---|\n| words | up to 3000 | x |\n"
                                             "| main limit | 5 | x |\n| format | PDF | x |\n")
        return board

    def test_it_makes_the_job_seeded_and_rollback_undoes_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            board = self.board(tmp)
            before = (board / "board.md").read_text(encoding="utf-8")
            quiet(L.main, ["submission", str(board), "--date", "1130", "--dry-run"])
            self.assertFalse((board / "j21_submission_v1130_desk").exists())
            quiet(L.main, ["submission", str(board), "--date", "1130"])
            job = board / "j21_submission_v1130_desk"
            face = (job / f"{job.name}.md").read_text(encoding="utf-8")
            self.assertIn("for: j11_writing_v1130_desk\n", face)
            self.assertIn("venue: Some Journal\n", face)
            for task in ("t01_cover-letter", "t02_portal-walk", "t03_portal-fill"):
                self.assertTrue((job / task / f"{task}.md").is_file(), task)
            self.assertTrue(os.access(job / "t03_portal-fill/runs/r01_fill_portal/r01_fill_portal.sh", os.X_OK))
            s = F.survey(job)
            says = {r["f"]["id"]: r["f"].get("says", "") for r in s["rows"]}
            self.assertIn("up to 3000", says["ms.words"])
            self.assertIn("Display limit 5", says["fi.figures"])
            self.assertEqual(s["unknown"], [])
            self.assertEqual(s["tally"]["paste"], 0)              # a starter asks; it invents nothing
            self.assertIn("j21_submission_v1130_desk", (board / "board.md").read_text(encoding="utf-8"))
            with self.assertRaises(SystemExit):                    # one Job per send
                quiet(L.main, ["submission", str(board), "--date", "1201"])
            quiet(L.main, ["rollback", str(board)])
            self.assertFalse(job.exists())
            self.assertEqual((board / "board.md").read_text(encoding="utf-8"), before)

    def test_the_ticket_runs_the_shipped_script(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "SPACE"
            (root / "plugins").mkdir(parents=True)
            os.symlink(HERE.parents[5], root / "plugins" / "haipipe-toolkit")
            board = self.board(root)
            quiet(L.main, ["submission", str(board), "--date", "1130"])
            ticket = board / "j21_submission_v1130_desk/t03_portal-fill/runs/r01_fill_portal/r01_fill_portal.sh"
            got = subprocess.run(["bash", str(ticket), "a person"], capture_output=True, text=True,
                                 env={**os.environ, "HAIPIPE_PYTHON": sys.executable})
            self.assertEqual(got.returncode, 0, got.stderr)
            self.assertRegex(got.stdout, r"^\d+ portal fields: ")
            self.assertTrue((board / "delivery/j21_submission_v1130_desk/portal-fill.html").is_file())
            self.assertIn("a person", (ticket.parent / "result/runtime.yaml").read_text(encoding="utf-8"))

    def test_a_built_packet_seeds_the_upload_fields_title_and_words(self):
        with tempfile.TemporaryDirectory() as tmp:
            board, delivery = built_board(tmp, uploads=[{"slot": "Manuscript", "files": ["M.docx"], "state": "ready"},
                                                        {"slot": "Figures", "files": ["F1.pdf", "F2.pdf"], "state": "ready"}])
            for n in ("M.docx", "F1.pdf", "F2.pdf"):
                write(delivery / "portal" / n, "x")
            write(delivery / "t00_abstract/latex/t00_abstract.tex", "Words.")
            (board / "j11_writing_v1130_desk/t00_abstract").mkdir(exist_ok=True)
            quiet(L.main, ["submission", str(board), "--date", "1130"])
            got = {r["f"]["id"]: r for r in F.survey(board / "j21_submission_v1130_desk")["rows"]}
            self.assertEqual(got["fi.manuscript"]["state"], "upload")
            self.assertEqual({got["fi.figures-1"]["state"], got["fi.figures-2"]["state"]}, {"upload"})
            self.assertEqual(got["ms.title"]["text"], "The Built Title")
            self.assertEqual(got["ms.words"]["text"], "2000")
            self.assertEqual(got["ms.abstract"]["text"], "Words.")


class Letter(unittest.TestCase):
    def test_the_build_finds_the_letter_in_either_job(self):
        with tempfile.TemporaryDirectory() as tmp:
            board = Path(tmp) / "Paper-X"
            writing = board / "j11_writing_v1130_desk"
            writing.mkdir(parents=True)
            write(board / "board.md", "# X\n\n## Pages\n")
            quiet(L.main, ["submission", str(board), "--date", "1130"])
            page = board / "j21_submission_v1130_desk/t01_cover-letter/t01_cover-letter.md"
            self.assertEqual(C.submission_letter(writing), page)    # no t3N_ letter: the scaffold made a letter Task
            self.assertIsNone(C.letter_task(writing))
            page.write_text(page.read_text(encoding="utf-8").replace("<the letter's body only", "Dear editors, the words <the letter's body only"), encoding="utf-8")
            words, where, _ = C.letter_source(page)
            self.assertEqual(where, "content")                       # read as a letter Task, though it is not a t3N_
            self.assertIn("Dear editors", words[0])
            self.assertEqual(K.submission_jobs(board, writing)[0].name, "j21_submission_v1130_desk")

    def test_a_writing_jobs_own_letter_comes_first_and_t01_only_points(self):
        with tempfile.TemporaryDirectory() as tmp:
            board = Path(tmp) / "Paper-X"
            writing = board / "j11_writing_v1130_desk"
            own = write(writing / "t31_cover-letter/t31_cover-letter.md", "# letter\n\n## Content\n\nWords.\n")
            write(board / "board.md", "# X\n\n## Pages\n")
            quiet(L.main, ["submission", str(board), "--date", "1130"])
            page = (board / "j21_submission_v1130_desk/t01_cover-letter/t01_cover-letter.md").read_text(encoding="utf-8")
            self.assertIn("words-in: ../../j11_writing_v1130_desk/t31_cover-letter", page)
            self.assertEqual(C.letter_task(writing), own)
            self.assertIsNone(C.submission_letter(writing))


class Checklist(unittest.TestCase):
    def rows(self, board):
        return {i: (m, seen) for _, i, _, m, seen in K.check(board)}

    def test_d9_walks_from_no_job_to_ready(self):
        with tempfile.TemporaryDirectory() as tmp:
            board, _ = built_board(tmp)
            self.assertEqual(self.rows(board)["D9"][0], "⬜")
            job = job_on(board, field("a") + field("b"), "a: {value: x}\nb: {value: y, ask: 'who?'}\n")
            self.assertEqual(self.rows(board)["D9"][0], "⏳")        # not built
            quiet(F.main, [str(job)])
            self.assertEqual(self.rows(board)["D9"][0], "🙋")        # a person decides
            values = job / "t03_portal-fill/portal-values.yaml"
            values.write_text("a: {value: x}\nb: {value: y}\n", encoding="utf-8")
            page = board / "delivery" / job.name / "portal-fill.html"
            os.utime(page, (page.stat().st_atime, values.stat().st_mtime - 60))
            self.assertIn("older", self.rows(board)["D9"][1])        # the values moved on
            quiet(F.main, [str(job)])
            self.assertEqual(self.rows(board)["D9"][0], "✅")
            self.assertEqual(self.rows(board)["D11"][0], "🙋")


class PaperExample(unittest.TestCase):
    JOB = EXAMPLE / "j21_submission_v1130_desk"

    def test_the_placeholder_job_shows_every_state_on_placeholders(self):
        s = F.survey(self.JOB)
        self.assertEqual({k for k, n in s["tally"].items() if n}, set(F.STATES))
        for path in (s["fields"], s["values"]):
            self.assertNotRegex(path.read_text(encoding="utf-8"), r"https?://")
        emails = re.findall(r"[\w.]+@[\w.]+", s["values"].read_text(encoding="utf-8") + s["fields"].read_text(encoding="utf-8"))
        self.assertTrue(all(e.endswith("example.org") for e in emails), emails)

    def test_it_is_a_job_the_workbench_tab_reads(self):
        self.assertTrue(re.search(r"(?m)^for:\s*j11_writing_v1130_desk\s*$", (self.JOB / f"{self.JOB.name}.md").read_text(encoding="utf-8")))
        self.assertTrue((EXAMPLE / "delivery" / self.JOB.name / "portal-fill.html").is_file())


if __name__ == "__main__":
    unittest.main()


def test_a_pdf_only_builds_word_count_says_it_is_old():
    """--pdf-only keeps the last full build's count (Paper-PhyAbsence 261104: 774 stayed while the Discussion grew)."""
    b = {"facts": {"words": 774}, "words_from": "the last full build"}
    assert load("portal_fill_w", SCRIPTS / "portal_fill.py").checked({"check": "words"}, "774", "", b)[1] == [
        "This count is from the last full build; the text may have changed. Run a full build before pasting it."]
    assert load("portal_fill_w", SCRIPTS / "portal_fill.py").checked({"check": "words"}, "774", "", {"facts": {"words": 774}}) == ([], [])
