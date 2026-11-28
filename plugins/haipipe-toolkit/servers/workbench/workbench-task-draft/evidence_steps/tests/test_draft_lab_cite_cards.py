"""Draft Lab against hai-paper ref/must-check.md M-D20: every CITE evidence item of a Section whose
evidence/cards.yaml holds no card for it still gets its ❝ card beside its sentence, from its bound Run, else the
citation Job's citations.csv row (with the discovery Run's reference), else its BibTeX marked "not read yet".
Every case runs on a temp Board."""
from __future__ import annotations

import re
import tempfile
import unittest
from pathlib import Path

from host_paths import bootstrap
bootstrap()

from live import task_draft  # noqa: E402

BOARD = "Project-X/paper/Paper-Demo"
DRAFT = ("# Note · draft v1.0\n\n## 3 · Draft\n\n### C1.P1 · Work · s1 to s3\n"
         "- B1 · s1 · Scaling helps language models \\citep{kaplan2020}.\n"
         "- B2 · s2 · Glucose models grew \\citep{Lutsker_2026}.\n"
         "- B3 · s3 · A sentence with no citation.\n")
ITEM = ("### {id}-CITE-{slug} · {target} · {key}\n- **Target**: {target}\n- **Label**: {key}\n"
        "- **Expected**: CITE · the Discovery Run's BibTeX: {bib}\n- **Verified**: ⬜ a person checks\n"
        "- **Local Input**: {bib}\n{extra}\n")
LUTSKER = ("@article{Lutsker_2026, title={A foundation model for continuous glucose monitoring data}, "
           "journal={Nature}, author={Lutsker, Guy and Sapir, Gal and Segal, Eran}, year={2026}, "
           "DOI={10.1038/s41586-025-09925-9} }")
CSV = ("key,group,status,cited_in,sentences,bib_entry,bib_in,in_reference_bib,doi,doi_conflict,title,year,doi_record,"
       "verified,cite_card,card_gaps,discovery_runs\n"
       "kaplan2020,t01_scaling_laws,card-only,,1,yes,,yes,,,Scaling Laws for Neural Language Models,2020,,"
       "nobody yet,,,b01.j03.t01.r01\n")
KAPLAN_BIB = ("@misc{kaplan2020,\n  title = {Scaling Laws for Neural Language Models},\n"
              "  author = {Kaplan, Jared and McCandlish, Sam and Henighan, Tom},\n  year = {2020},\n"
              "  eprint = {2001.08361}\n}\n")
BOUND = ("- **Local Run**: Page · Evidence Item · reuse · P.j03.t01.r01 → "
         "j03_evidence_cite/t01_scaling_laws/runs/r01_check_citations/result/citations.csv\n")


def _paper(root: Path, kaplan_extra: str = "") -> Path:
    board = root / BOARD
    task = board / "j11_writing_v1" / "t01_note"
    (task / "draft" / "records").mkdir(parents=True)
    (board / "board.md").write_text("# Paper\n")
    (task / "t01_note.md").write_text("# t01_note · Note\n\nfolder-kind: task\ntask-type: draft\n")
    (task / "draft" / "t01_note-draft-v1.0.md").write_text(DRAFT)
    (task / "draft" / "t01_note-evidence-items.md").write_text(
        "# t01_note · evidence items\n\n"
        + ITEM.format(id="E01", slug="kaplan2020", target="C1.P1.B1", key="kaplan2020", bib="@misc{kaplan2020,",
                      extra=kaplan_extra)
        + ITEM.format(id="E02", slug="lutsker-2026", target="C1.P1.B2", key="Lutsker_2026", bib=LUTSKER, extra=""))
    check = board / "j03_evidence_cite/t01_scaling_laws/runs/r01_check_citations/result"
    check.mkdir(parents=True)
    (check / "citations.csv").write_text(CSV)
    disc = root / "Project-X/discovery/b01_lit/j03_papers/t01_scaling/runs/r01_kaplan2020/result"
    disc.mkdir(parents=True)
    (disc / "r01_kaplan2020.bib").write_text(KAPLAN_BIB)
    (disc / "r01_kaplan2020.md").write_text("# Kaplan 2020\n")
    return task


def _html(root: Path, task: Path) -> str:
    return task_draft.draft_task_spaces(task, root, "5 · Revise")["Work Details"].html


def _card(html: str, addr: str) -> str:
    m = re.search(r'(?s)<div class="rv-card rv-ev" data-s="' + re.escape(addr) + r'".*?</div></div>', html)
    return m.group(0) if m else ""


class CiteCardTest(unittest.TestCase):
    def test_every_cite_item_gets_a_card_without_any_cards_yaml(self):
        with tempfile.TemporaryDirectory() as tmp:
            task = _paper(Path(tmp))
            html = _html(Path(tmp), task)
            self.assertEqual(len(re.findall(r'class="rv-card rv-ev"', html)), 2)
            self.assertFalse((task / "evidence" / "cards.yaml").exists())
            self.assertEqual(_card(html, "s3"), "")             # no item, no card

    def test_a_checked_key_reads_its_discovery_run_and_names_the_check_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            task = _paper(Path(tmp))
            card = _card(_html(Path(tmp), task), "s1")
            self.assertIn('data-cite="1"', card)
            self.assertIn("❝︎ Kaplan et al. (2020).", card)             # from the discovery Run's .bib
            self.assertIn("https://arxiv.org/abs/2001.08361", card)
            self.assertIn(">P.j03.t01.r01</a>", card)
            self.assertIn("result/citations.csv", card)
            self.assertIn(">b01.j03.t01.r01</a>", card)
            self.assertNotIn("not read yet", card)

    def test_a_key_no_run_checked_shows_its_bibtex_and_not_read_yet(self):
        with tempfile.TemporaryDirectory() as tmp:
            task = _paper(Path(tmp))
            card = _card(_html(Path(tmp), task), "s2")
            self.assertIn("❝︎ Lutsker et al. (2026).", card)            # from the item's own BibTeX
            self.assertIn("https://doi.org/10.1038/s41586-025-09925-9", card)
            self.assertIn("<i>Nature</i>", card)
            self.assertIn("not read yet", card)
            self.assertIn("Lutsker et al. 2026", card)                  # the side card's line

    def test_a_bound_item_shows_its_run_found_or_not(self):
        with tempfile.TemporaryDirectory() as tmp:
            task = _paper(Path(tmp), BOUND)
            self.assertIn("✅ Run <a", _card(_html(Path(tmp), task), "s1"))
        with tempfile.TemporaryDirectory() as tmp:
            task = _paper(Path(tmp), BOUND.replace("t01_scaling_laws", "t09_gone"))
            card = _card(_html(Path(tmp), task), "s1")
            self.assertIn("❗ Run P.j03.t01.r01", card)

    def test_an_item_a_cards_yaml_card_holds_is_not_drawn_twice(self):
        from live.draft_step_cite_items import cite_entries
        from live.draft_steps_common import read_draft
        with tempfile.TemporaryDirectory() as tmp:
            task = _paper(Path(tmp))
            d = read_draft(task)
            ev = {"cards": [{"kind": "cite", "items": [{"item": "E01-CITE-kaplan2020"}, {"cite": "Lutsker_2026"}]}]}
            self.assertEqual(cite_entries(task, d, ev), [])
            self.assertEqual(len(cite_entries(task, d, {"cards": []})), 2)


if __name__ == "__main__":
    unittest.main()
