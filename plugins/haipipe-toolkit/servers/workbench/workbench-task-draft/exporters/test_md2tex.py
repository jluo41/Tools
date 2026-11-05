#!/usr/bin/env python3
"""Regression checks for md2tex's refuse-to-regress guard (261103).

A refused Section keeps its OLD fragment, and the paper build prints it, so a
refusal must be a visible failure (exit 2, `REFUSED`, the dropped keys named),
and an intended drop passes only with --accept-dropped-keys when another
Section still cites the key or a revise card removed it.
"""

from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from pathlib import Path

import md2tex


def page_text(sentences):
    """A minimal Section Page: one paragraph per sentence."""
    paras = "\n\n".join("#### P%d. Point\n\n%s" % (i, s) for i, s in enumerate(sentences, 1))
    return "# Section\n\n## Content\n\n### 1 · Introduction\n\n%s\n\n## Aims\n" % paras


class RefuseToRegressTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name) / "Paper-T"
        self.group = self.root / "j11_writing_v1103_desk"
        self.out = self.root / "delivery" / "latex"
        self.out.mkdir(parents=True)

    def tearDown(self):
        self._tmp.cleanup()

    def page(self, stem, sentences):
        d = self.group / stem
        d.mkdir(parents=True, exist_ok=True)
        path = d / (stem + ".md")
        path.write_text(page_text(sentences), encoding="utf-8")
        return path

    def export(self, page, *flags):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = md2tex.main([str(page), "--paper-root", str(self.root), "-o", str(self.out), *flags])
        return code, buf.getvalue()

    def fragment(self, stem):
        return (self.out / (stem + ".tex")).read_text(encoding="utf-8")

    def first_export(self):
        intro = self.page("t01_intro", [
            "Physicians differ \\citep{alpha2020}.",
            "Guidelines help \\citep{beta2021}.",
            "Some cases are unclear \\citep{gamma2022}.",
        ])
        code, _ = self.export(intro)
        self.assertEqual(code, 0)
        return intro

    def test_refusal_is_reported_and_exits_nonzero(self):
        intro = self.first_export()
        intro.write_text(page_text(["Physicians differ \\citep{alpha2020}."]), encoding="utf-8")
        code, log = self.export(intro)
        self.assertEqual(code, 2)
        self.assertIn("REFUSED t01_intro", log)
        self.assertIn("beta2021, gamma2022", log)
        self.assertIn("--accept-dropped-keys", log)
        self.assertIn("OLD words", log)
        self.assertNotIn("✅ " + str(self.out), log)
        # the old words stay on disk, which is exactly why it must be loud
        self.assertIn("beta2021", self.fragment("t01_intro"))

    def test_flag_accepts_a_key_cited_in_another_section(self):
        intro = self.first_export()
        self.page("t02_methods", ["We follow the guideline \\citep{beta2021}.",
                                  "Unclear cases \\citep{gamma2022}."])
        intro.write_text(page_text(["Physicians differ \\citep{alpha2020}."]), encoding="utf-8")
        code, log = self.export(intro, "--accept-dropped-keys")
        self.assertEqual(code, 0, log)
        self.assertIn("dropped key beta2021 accepted, cited in t02_methods", log)
        self.assertNotIn("beta2021", self.fragment("t01_intro"))

    def test_flag_accepts_a_key_a_revise_card_removed(self):
        intro = self.first_export()
        records = intro.parent / "draft" / "records"
        records.mkdir(parents=True)
        (records / "t01_intro-revise.md").write_text(
            "# t01_intro · Revise cards\n\n## Round 261103 r1\n\n"
            "### Edit · S2 · C1.P2.B1 · the guideline sentence goes\n"
            "Original: Guidelines help \\citep{beta2021}.\nExpected: Guidelines help.\n"
            "State: written\n\n"
            "### Edit · S3 · C1.P3.B1 · removed\n"
            "Original: Some cases are unclear \\citep{gamma2022}.\n"
            "State: written\n", encoding="utf-8")
        intro.write_text(page_text(["Physicians differ \\citep{alpha2020}.", "Guidelines help."]),
                         encoding="utf-8")
        code, log = self.export(intro, "--accept-dropped-keys")
        self.assertEqual(code, 0, log)
        self.assertIn("beta2021 accepted, removed by revise card 'Edit · S2 · C1.P2.B1'", log)
        self.assertIn("gamma2022 accepted, removed by revise card 'Edit · S3 · C1.P3.B1'", log)

    def test_flag_still_refuses_an_unexplained_drop(self):
        intro = self.first_export()
        self.page("t02_methods", ["We follow the guideline \\citep{beta2021}."])
        intro.write_text(page_text(["Physicians differ \\citep{alpha2020}."]), encoding="utf-8")
        code, log = self.export(intro, "--accept-dropped-keys")
        self.assertEqual(code, 2)
        self.assertIn("REFUSED t01_intro: --accept-dropped-keys cannot explain 1 of 2", log)
        self.assertIn("gamma2022", log)
        self.assertIn("gamma2022", self.fragment("t01_intro"))   # nothing written

    def test_drop_check_names_the_keys_for_a_paper_build(self):
        intro = self.first_export()
        intro.write_text(page_text(["Physicians differ \\citep{alpha2020}."]), encoding="utf-8")
        frag = self.out / "t01_intro.tex"
        plain = md2tex.drop_check(str(intro), str(frag), str(self.root))
        self.assertEqual(plain["refused"], ["beta2021", "gamma2022"])
        other = self.page("t02_methods", ["Guideline \\citep{beta2021}."])
        judged = md2tex.drop_check(str(intro), str(frag), str(self.root), accept=True, others=[str(other)])
        self.assertEqual(judged["accepted"], {"beta2021": "cited in t02_methods"})
        self.assertEqual(judged["refused"], ["gamma2022"])


if __name__ == "__main__":
    unittest.main()
