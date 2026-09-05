"""The design family's checks, each proven to FAIL on a board broken one way.

A rule nobody has seen fail is not a rule, it is a comment that runs. Every
case here breaks a synthetic DesignBoard in exactly ONE way and asserts the
matching code fires; the suite also asserts the intact board is clean, so a
rule cannot pass by firing on everything.

Layout under test is the 260828 one-thread-one-folder shape: the design card
is `card.md` INSIDE the unit folder it commissions, `direction/` is gone, and
the two pointer fields (`landed:` on the card, `direction:` on the README)
are retired because the shared folder is the binding. The release-before-
realize law became checkable the same day: a folder whose card still says
`proposed` may hold no realization material; `workflow/` phase history is
control metadata and remains legal.

The boards are built in a temp `applications/` directory holding BOTH the
design board and the insight board it reads, because `reads:`, grants and
evidence are all written relative to that directory.
"""
import re
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from cli.check import Report, check_design_family, check_plugin_roster

PAGE = "2-DS-design/DS01-slate"
UNIT = PAGE + "/design/DU01-first"
CARD = UNIT + "/card.md"

BOARD_MD = """# Test DesignBoard

spine: one brief, one design page, one thread folder holding card and unit.
close: the unit is judged and the division awaits a person.
reads: A00_Test-InsightBoard

## Topic
A synthetic board for the design-family checks.

## Pipeline
The card is released, the unit lands beside it, the judge checks.

## Pages
DS01-slate.md
"""

CARD_MD = """# DU01 · First

state: landed
stance: follow A00·W01
depth: copy+why
thesis: Send the tested winner unchanged.
expected effect: it keeps leading on click; falsified if any concurrent arm beats it.
grant: ../../../../../A00_Test-InsightBoard/1-F-full/FW01-win/FW01-win.md
released: JL 260824
"""

README_MD = """# DU01 · First

unit: DU01-first
kind: sms
serves: DS01 division 2
depth: copy+why
state: judged

The wager lives on the card beside this file, `./card.md`.
"""

EVIDENCE_MD = """# DU01 · evidence

- path: `../../../../../A00_Test-InsightBoard/1-F-full/FW01-win/FW01-win.md`
"""


def build(root):
    """An intact applications/ dir: one insight board, one design board."""
    apps = root / "applications"
    ins = apps / "A00_Test-InsightBoard" / "1-F-full" / "FW01-win"
    ins.mkdir(parents=True)
    (ins / "FW01-win.md").write_text("# FW01 · win\n", encoding="utf-8")
    other = apps / "A00_Test-InsightBoard" / "1-F-full" / "FK01-other"
    other.mkdir(parents=True)
    (other / "FK01-other.md").write_text("# FK01 · other\n", encoding="utf-8")
    # A board that exists and is NOT named in `reads:`, so a grant reaching it
    # is outside the whitelist rather than merely dead.
    unread = apps / "A99_Unread-InsightBoard"
    unread.mkdir(parents=True)
    (unread / "board.md").write_text("# Unread\n", encoding="utf-8")

    d = apps / "B00_Test-DesignBoard"
    (d / UNIT / "content").mkdir(parents=True)
    (d / "board.md").write_text(BOARD_MD, encoding="utf-8")
    (d / PAGE / "DS01-slate.md").write_text("# Slate\n\nstate: 🟡 PARTIAL\n",
                                            encoding="utf-8")
    (d / CARD).write_text(CARD_MD, encoding="utf-8")
    (d / UNIT / "workflow").mkdir()
    (d / UNIT / "workflow" / "phase.yaml").write_text(
        "current:\n  phase: D3\n  folder-kind: design-verdict\n",
        encoding="utf-8",
    )
    (d / UNIT / "README.md").write_text(README_MD, encoding="utf-8")
    (d / UNIT / "spec.md").write_text("# spec\n", encoding="utf-8")
    (d / UNIT / "evidence.md").write_text(EVIDENCE_MD, encoding="utf-8")
    (d / UNIT / "why.md").write_text("# why\n\nSee `./card.md`.\n",
                                     encoding="utf-8")
    (d / UNIT / "content" / "copy.txt").write_text("hello\n", encoding="utf-8")
    return d


def sub(rel, pat, rep):
    def f(d):
        p = d / rel
        t = p.read_text(encoding="utf-8")
        t2 = re.sub(pat, rep, t, count=1, flags=re.M)
        assert t2 != t, f"breakage did not apply to {rel}"
        p.write_text(t2, encoding="utf-8")
    return f


BREAKS = {
    "unit-no-card": lambda d: (d / CARD).unlink(),
    "card-field-missing": sub(CARD, r"^thesis:.*$", ""),
    "card-field-empty": sub(CARD, r"^depth: .*$", "depth:"),
    "card-state-word": sub(CARD, r"^state: landed$", "state: shipped"),
    "card-released-no-wager": sub(CARD, r"^expected effect:.*$", "expected effect: tbd"),
    "card-released-unsigned": sub(CARD, r"^released: .*$", "released: ⬜"),
    "card-proposed-signed": sub(CARD, r"^state: landed$", "state: proposed"),
    "card-grant-path": sub(CARD, r"FW01-win\.md", "FW01-gone.md"),
    "card-grant-outside-reads": sub(
        CARD, r"^grant: .*$",
        "grant: ../../../../../A99_Unread-InsightBoard/board.md"),
    # release-before-realize, the law the merge made checkable: a proposed
    # card sitting in a folder that already holds realization files. The
    # workflow/ control directory built above is deliberately ignored.
    "unit-realized-before-release": sub(CARD, r"^state: landed$",
                                        "state: proposed"),
    "unit-tombstone-extra": sub(CARD, r"^state: landed$", "state: killed"),
    # the ghost pointer's old failure, wearing the new layout: landed with
    # no README beside the card.
    "card-landed-bare": lambda d: (d / UNIT / "README.md").unlink(),
    "unit-file-missing": lambda d: (d / UNIT / "spec.md").unlink(),
    "unit-no-content": lambda d: (d / UNIT / "content" / "copy.txt").unlink(),
    "unit-depth-word": sub(UNIT + "/README.md", r"^depth: .*$", "depth: full"),
    "unit-depth-no-why": lambda d: (d / UNIT / "why.md").unlink(),
    "unit-depth-extra-why": sub(UNIT + "/README.md", r"^depth: .*$", "depth: copy"),
    "unit-state-word": sub(UNIT + "/README.md", r"^state: .*$", "state: shipped"),
    "unit-dead-reference": sub(UNIT + "/why.md", r"\./card\.md", "./card-gone.md"),
    "unit-evidence-outside-grant": sub(
        UNIT + "/evidence.md", r"FW01-win/FW01-win\.md", "FK01-other/FK01-other.md"),
}


def codes(board):
    rep = Report()
    check_design_family(board, rep)
    check_plugin_roster(board, rep)
    return {row[1] for row in rep.rows}


class DesignFamilyTest(unittest.TestCase):
    def test_intact_board_is_clean(self):
        with TemporaryDirectory() as td:
            self.assertEqual(codes(build(Path(td))), set())

    def test_every_rule_fires_on_its_own_breakage(self):
        silent = []
        for name, breaker in BREAKS.items():
            with TemporaryDirectory() as td:
                d = build(Path(td))
                breaker(d)
                if name not in codes(d):
                    silent.append(name)
        self.assertEqual(silent, [], f"rules that never fired: {silent}")

    def test_proposed_folder_with_card_and_phase_control_is_clean(self):
        """workflow/ phase metadata is control, not premature realization."""
        with TemporaryDirectory() as td:
            d = build(Path(td))
            u = d / UNIT
            for f in ["README.md", "spec.md", "evidence.md", "why.md"]:
                (u / f).unlink()
            (u / "content" / "copy.txt").unlink()
            (u / "content").rmdir()
            sub(CARD, r"^state: landed$", "state: proposed")(d)
            sub(CARD, r"^released: .*$", "released: ⬜")(d)
            self.assertEqual(codes(d), set())

    def test_record_mode_excuses_pre_contract_vocabulary(self):
        """A record board holds an artifact older than the words for it."""
        with TemporaryDirectory() as td:
            d = build(Path(td))
            sub("board.md", r"^reads: .*$", "mode: record")(d)
            sub(CARD, r"^stance: .*$", "stance: — · pre-contract")(d)
            sub(CARD, r"^grant: .*$", "grant: none, the source carries no run")(d)
            sub(CARD, r"^released: .*$", "released: field test 250901, historical")(d)
            sub(UNIT + "/evidence.md", r"^- path: .*$", "NONE.")(d)
            sub(UNIT + "/README.md", r"^state: .*$", "state: historical-record")(d)
            self.assertEqual(codes(d), set())

    def test_live_board_still_rejects_that_vocabulary(self):
        """The same board without `mode: record` is not excused."""
        with TemporaryDirectory() as td:
            d = build(Path(td))
            sub(UNIT + "/README.md", r"^state: .*$", "state: historical-record")(d)
            self.assertIn("unit-state-word", codes(d))

    def test_result_bank_counts_as_inside_the_read(self):
        """A grant may cite the store bank of a board named in `reads:`."""
        with TemporaryDirectory() as td:
            root = Path(td)
            d = build(root)
            (root / ".git").write_text("gitdir: elsewhere\n", encoding="utf-8")
            bank = (root / "_WorkSpace" / "InsightBoardResult"
                    / "A00_Test-InsightBoard" / "T01")
            bank.mkdir(parents=True)
            (bank / "rates.csv").write_text("a,b\n", encoding="utf-8")
            sub(CARD, r"^grant: .*$",
                "grant: ../../../../../../_WorkSpace/InsightBoardResult/"
                "A00_Test-InsightBoard/T01/rates.csv")(d)
            self.assertNotIn("card-grant-outside-reads", codes(d))

    def test_repo_relative_read_resolves_from_repo_root_not_cwd(self):
        """A repo-relative `reads:` entry must not depend on the checker's cwd.

        The live break (260828): B00 whitelists its discovery bank as
        `designs/<project>/discoveries`, and the checker resolved that entry
        with bare `Path(entry)` — correct only when invoked FROM the repo
        root, and 8 phantom errors from anywhere else.
        """
        from cli.check import check_board
        with TemporaryDirectory() as td:
            root = Path(td)
            d = build(root)
            (root / ".git").mkdir()
            bank = (root / "discoveries" / "b01_topic_bank"
                    / "j01_topic_inquiry" / "t01_topic_page" / "QA")
            bank.mkdir(parents=True)
            (bank / "1-answer.md").write_text("# QA\n", encoding="utf-8")
            sub("board.md", r"^reads: .*$",
                "reads: A00_Test-InsightBoard · discoveries")(d)
            sub(CARD, r"^grant: .*$",
                "grant: ../../../../../A00_Test-InsightBoard/1-F-full/FW01-win/"
                "FW01-win.md · ../../../../../../discoveries/b01_topic_bank/"
                "j01_topic_inquiry/t01_topic_page/QA/"
                "1-answer.md")(d)
            rep = Report()
            check_board(d, rep)
            check_design_family(d, rep)
            self.assertEqual({row[1] for row in rep.rows}, set())

    def test_submodule_git_file_does_not_shadow_the_checkout_root(self):
        """`_repo_root` takes the OUTERMOST .git, not the nearest one."""
        from cli.check import _repo_root
        with TemporaryDirectory() as td:
            root = Path(td)
            (root / ".git").mkdir()
            inner = root / "designs" / "Sub"
            inner.mkdir(parents=True)
            (inner / ".git").write_text("gitdir: ../../.git/modules/Sub\n",
                                        encoding="utf-8")
            deep = inner / "applications" / "B00"
            deep.mkdir(parents=True)
            self.assertEqual(_repo_root(deep), root)

    def test_bare_path_is_not_matched_from_its_middle(self):
        """`../../x.md` must not also yield the dead string `./../x.md`."""
        from cli.check import _cited_paths
        self.assertEqual(_cited_paths("see `../../design/DU01-a/card.md` there"),
                         ["../../design/DU01-a/card.md"])


if __name__ == "__main__":
    unittest.main()
