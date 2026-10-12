"""The QV2 defect, reproduced: five declared display units reaching LaTeX as two.

Every fixture here is built from the real failure (JL 260816) rather than from
an invented shape, so a regression reproduces the thing that actually shipped.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.page_evidence import (  # noqa: E402
    check_page_evidence, cited_ids, display_units, unit_state)


class Rep:
    def __init__(self):
        self.rows = []

    def add(self, level, code, where, message):
        self.rows.append((level, code, where, message))

    def codes(self):
        return [code for _l, code, _w, _m in self.rows]


README = """# {name}

- kind: table
- claim: a claim
- accepted: {accepted}
"""


def build_unit(root, stem, n, slug, *, intake=False, recipe=False,
               asset=False, preview=False, accepted="⬜ human review pending"):
    unit = root / f"{stem}-Display{n}-{slug}"
    unit.mkdir(parents=True)
    (unit / "README.md").write_text(README.format(name=unit.name, accepted=accepted))
    if intake:
        (unit / "intake" / "inputs").mkdir(parents=True)
        (unit / "intake" / "manifest.yaml").write_text("source: task-bank\n")
        (unit / "intake" / "inputs" / "source_data.csv").write_text("a,b\n1,2\n")
    if recipe:
        (unit / "recipe").mkdir()
        (unit / "recipe" / "build.py").write_text("# renderer-owned\n")
    if asset:
        (unit / "assets").mkdir()
        (unit / "assets" / "table-body.tex").write_text("\\toprule\n")
    if preview:
        (unit / "preview.pdf").write_bytes(b"%PDF-1.4\n")
    return unit


class PageEvidenceTest(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.board = Path(self.tmp.name)
        self.stem = "QV2-lbp-regression-results"
        self.folder = self.board / self.stem
        self.display = self.folder / "display"
        self.display.mkdir(parents=True)
        self.source = self.board / f"{self.stem}.md"

    def write_page(self, body):
        self.source.write_text(f"# Low-back-pain regression results\n\n{body}\n")
        return self.source.read_text()

    def write_tex(self, unit_names):
        tex_dir = self.folder / "latex"
        tex_dir.mkdir(exist_ok=True)
        lines = ["\\section{Results}"]
        for unit in unit_names:
            lines.append(f"\\input{{../display/{unit}/assets/table-body}}")
        tex = tex_dir / f"{self.stem}.tex"
        tex.write_text("\n".join(lines) + "\n")
        import os
        # The projection is built AFTER the source it projects.
        stamp = self.source.stat().st_mtime + 10
        os.utime(tex, (stamp, stamp))
        return tex

    def run_check(self, body, embedded):
        text = self.write_page(body)
        self.write_tex(embedded)
        rep = Rep()
        check_page_evidence(self.source, text, self.stem, rep, "ERROR", "WARN")
        return rep

    # ---------------------------------------------------------------- the case

    def test_the_qv2_defect_five_declared_two_rendered(self):
        """Three placeholder shells + two real units, all five cited in prose."""
        for n, slug in ((1, "nominal-s5-association"), (3, "analysis-design")):
            build_unit(self.display, self.stem, n, slug,
                       intake=True, recipe=True, asset=True, preview=True)
        build_unit(self.display, self.stem, 2, "ols-robustness")
        build_unit(self.display, self.stem, 4, "coefficient-trajectory",
                   intake=True)
        build_unit(self.display, self.stem, 5, "identification-provenance-gate",
                   intake=True, recipe=True)

        states = [unit_state(u) for u in display_units(self.source)]
        self.assertEqual(len(states), 5)
        self.assertEqual(sum(s["rendered"] for s in states), 2)

        rep = self.run_check(
            "Display1 is the main OLS association. Display2 is its robustness. "
            "Display3 states the design. Display4 is the trajectory. "
            "Display5 is the IV diagnostic.",
            [f"{self.stem}-Display1-nominal-s5-association",
             f"{self.stem}-Display3-analysis-design"])

        codes = rep.codes()
        self.assertEqual(codes.count("display-declared-not-rendered"), 3)
        self.assertEqual(codes.count("display-cited-not-embedded"), 3)
        self.assertIn("display-counts-split", codes)

        # The finding NAMES the step each shell is stuck on, which is the whole
        # point: "not rendered" alone does not tell anyone what to do next.
        missing = {row[2].split("Display")[1][0]: row[3]
                   for row in rep.rows if row[1] == "display-declared-not-rendered"}
        self.assertIn("① INTAKE", missing["2"])
        self.assertIn("② RENDER · no renderer-owned recipe", missing["4"])
        self.assertIn("no winning asset", missing["5"])

    def test_a_proposed_unit_is_owed_not_litter(self):
        """DRAFT may create the unit in OWED state; the claim row is the promise."""
        proposed = build_unit(self.display, self.stem, 1, "iv-estimates")
        self.assertTrue(unit_state(proposed)["proposed"])

        litter = self.display / f"{self.stem}-Display2-leftover"
        litter.mkdir()
        (litter / "README.md").write_text(f"# {litter.name}\n\n- kind: table\n")
        self.assertFalse(unit_state(litter)["proposed"])

        rep = self.run_check("Display1 will carry the IV estimates.", [])
        codes = rep.codes()
        self.assertEqual(codes.count("display-declared-no-claim"), 1)
        # The proposed unit is still owed a render, and says which step first.
        owed = [r for r in rep.rows if r[1] == "display-declared-not-rendered"]
        self.assertTrue(any("① INTAKE" in r[3] for r in owed))

    def test_both_readme_row_forms_parse(self):
        """`- claim:` and a bare `claim:` are both the unit contract's rows.

        QV2's units use the bullet; every CMSStoreBoard unit uses the bare form.
        Requiring the bullet read zero rows off 25 real units, so no claim, kind,
        or acceptance state was visible on any of them.
        """
        bare = self.display / f"{self.stem}-Display1-bare"
        bare.mkdir()
        (bare / "README.md").write_text(
            f"# {bare.name} · Cohort selection flow\n\n"
            "kind: tex\n"
            "claim: The pipeline reduces 49,287,628 candidate rows to 1,385,300.\n"
            "accepted: \u2705 JL 260816\n\n"
            "The native TikZ recipe is laid out for manuscript use.\n")
        state = unit_state(bare)
        self.assertTrue(state["proposed"])
        self.assertEqual(state["kind"], "tex")
        self.assertTrue(state["accepted"])

    def test_a_prose_sentence_with_a_colon_is_not_a_row(self):
        unit = self.display / f"{self.stem}-Display1-prose"
        unit.mkdir()
        (unit / "README.md").write_text(
            f"# {unit.name}\n\nkind: table\n\n"
            "Its values are transcribed from the logs named in the manifest, "
            "and the reason is this: the run is the only source.\n")
        self.assertFalse(unit_state(unit)["proposed"])

    def test_a_complete_page_reports_nothing(self):
        for n, slug in ((1, "main"), (2, "robustness")):
            build_unit(self.display, self.stem, n, slug,
                       intake=True, recipe=True, asset=True, preview=True)
        rep = self.run_check(
            "Display1 carries the estimate and Display2 its robustness.",
            [f"{self.stem}-Display1-main", f"{self.stem}-Display2-robustness"])
        self.assertEqual(rep.codes(), [])

    def test_rendered_but_uncited_never_reaches_a_reader(self):
        for n, slug in ((1, "main"), (2, "robustness")):
            build_unit(self.display, self.stem, n, slug,
                       intake=True, recipe=True, asset=True, preview=True)
        rep = self.run_check("Display1 carries the estimate.",
                             [f"{self.stem}-Display1-main"])
        self.assertIn("display-rendered-not-cited", rep.codes())

    def test_rendered_unit_absent_from_tex_is_an_export_fault(self):
        build_unit(self.display, self.stem, 1, "main",
                   intake=True, recipe=True, asset=True, preview=True)
        rep = self.run_check("Display1 carries the estimate.", [])
        hit = [r for r in rep.rows if r[1] == "display-cited-not-embedded"]
        self.assertEqual(len(hit), 1)
        self.assertIn("export fault", hit[0][3])

    def test_missing_title_block(self):
        build_unit(self.display, self.stem, 1, "main",
                   intake=True, recipe=True, asset=True, preview=True)
        text = self.write_page("Display1 carries the estimate.")
        tex_dir = self.folder / "latex"
        tex_dir.mkdir(exist_ok=True)
        tex = tex_dir / f"{self.stem}.tex"
        tex.write_text(f"\\input{{../display/{self.stem}-Display1-main/assets/table-body}}\n")
        import os
        stamp = self.source.stat().st_mtime + 10
        os.utime(tex, (stamp, stamp))
        rep = Rep()
        check_page_evidence(self.source, text, self.stem, rep, "ERROR", "WARN")
        self.assertIn("latex-untitled", rep.codes())

    def test_stale_projection(self):
        build_unit(self.display, self.stem, 1, "main",
                   intake=True, recipe=True, asset=True, preview=True)
        text = self.write_page("Display1 carries the estimate.")
        tex_dir = self.folder / "latex"
        tex_dir.mkdir(exist_ok=True)
        tex = tex_dir / f"{self.stem}.tex"
        tex.write_text("\\section{Results}\n"
                       f"\\input{{../display/{self.stem}-Display1-main/assets/table-body}}\n")
        import os
        stamp = self.source.stat().st_mtime - 100
        os.utime(tex, (stamp, stamp))
        rep = Rep()
        check_page_evidence(self.source, text, self.stem, rep, "ERROR", "WARN")
        self.assertIn("projection-stale", rep.codes())

    def test_accept_goes_stale_when_intake_moves(self):
        unit = build_unit(self.display, self.stem, 1, "main",
                          intake=True, recipe=True, asset=True, preview=True,
                          accepted="✅ JL 260816")
        import os
        stamp = (unit / "assets" / "table-body.tex").stat().st_mtime + 100
        os.utime(unit / "intake" / "inputs" / "source_data.csv", (stamp, stamp))
        os.utime(unit / "intake" / "manifest.yaml", (stamp, stamp))
        self.assertTrue(unit_state(unit)["stale_accept"])
        rep = self.run_check("Display1 carries the estimate.",
                             [f"{self.stem}-Display1-main"])
        self.assertIn("display-accept-stale", rep.codes())

    def test_a_page_with_no_display_folder_is_silent(self):
        import shutil
        shutil.rmtree(self.display)
        text = self.write_page("No units here.")
        rep = Rep()
        check_page_evidence(self.source, text, self.stem, rep, "ERROR", "WARN")
        self.assertEqual(rep.codes(), [])

    def test_rendered_but_unfrozen_is_provenance_not_visibility(self):
        """The CMSStoreBoard case: it prints fine, nothing traces it.

        Seven live units carried an `intake/manifest.yaml` with no
        `intake/inputs/`. Reporting those as "not rendered" would send someone
        to re-run a renderer that already worked, so the two axes are split.
        """
        unit = build_unit(self.display, self.stem, 1, "method-workflow",
                          recipe=True, asset=True, preview=True)
        (unit / "intake").mkdir()
        (unit / "intake" / "manifest.yaml").write_text("source: declared\n")
        state = unit_state(unit)
        self.assertTrue(state["rendered"])
        self.assertTrue(state["unfrozen"])
        self.assertEqual(state["missing"], "")
        rep = self.run_check("Display1 shows the method.",
                             [f"{self.stem}-Display1-method-workflow"])
        self.assertIn("display-intake-unfrozen", rep.codes())
        self.assertNotIn("display-declared-not-rendered", rep.codes())

    # -------------------------------------------------------------- the parser

    def test_a_backticked_id_quotes_instead_of_citing(self):
        """A page documenting the citation move must not report itself."""
        self.assertEqual(cited_ids("Cite it by id, as `Display3`."), set())
        self.assertEqual(cited_ids("Display3 states the design."), {"3"})

    def test_both_legal_citation_forms_resolve(self):
        """Bare inside its own page, fully qualified across pages.

        QC2-cancer cites every unit as `QC2-cancer-DisplayN` and its LaTeX
        embeds all three; matching only the bare form reported all three as
        uncited.
        """
        self.assertEqual(
            cited_ids("Figure QC2-cancer-Display1 shows every observed step."),
            {"1"})
        self.assertEqual(
            cited_ids("The workflow QC2-cancer-Display3 visualizes the method."),
            {"3"})

    def test_a_folder_name_in_a_path_is_filing_not_a_citation(self):
        self.assertEqual(
            cited_ids("built from display/QC2-cancer-Display3-method-workflow/"),
            set())

    def test_a_fenced_id_is_code_not_a_citation(self):
        text = "Intro.\n\n```text\nDisplay9 is an example\n```\n\nDisplay1 is real.\n"
        self.assertEqual(cited_ids(text), {"1"})

    def test_units_sort_by_number_not_by_string(self):
        for n in (10, 2, 1):
            build_unit(self.display, self.stem, n, f"u{n}")
        got = [u.name.split("-Display")[1].split("-")[0]
               for u in display_units(self.source)]
        self.assertEqual(got, ["1", "2", "10"])


if __name__ == "__main__":
    unittest.main()
