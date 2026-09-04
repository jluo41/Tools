#!/usr/bin/env python3
"""The 🧭 plan card makes one Section-review packet from source records."""
import tempfile
import sys
import unittest
from pathlib import Path

ENGINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ENGINE))

from live.outline import parse_outline, plan_card, render
from live.skillmap import SkillmapMixin


PLAN = """# SM00 · outline v1
approved: ⬜

## C1 · Problem and positioning
### C1.P1 · The decision
- B1 · frame the physician decision problem
  Note: name the clinical choice before the trait signal
  Evidence: E01-VALUE-review-cohort-counts · scored physicians and reviews
  Accept: counts recompute from the frozen local Result
"""

ITEMS = """# SM00 · evidence items
page: SM00
kind: evidence-items · authored
plan: v1

### E01-VALUE-review-cohort-counts · C1.P1.B1 · review cohort counts
- **Target**: C1.P1.B1
- **Need**: the cohort counts named in the abstract
- **Expected**: VALUE · scored physicians and reviews
- **Acceptance**: counts recompute from the frozen local Result
- **Supporting Runs**: Execution · new-block · MISQ-evidence-bridge
- **Local Input**: Supporting Results only
- **Local Run**: Page · Evidence Item · new-block · MISQ-evidence-bridge → _pending/SM00/E01/result.md
- **Decide**: ☐ make / defer / drop
"""


class OutlineReviewPacketTest(unittest.TestCase):
    def _page(self, root):
        page_dir = Path(root) / "SM00-abstract"
        outline = page_dir / "outline"
        outline.mkdir(parents=True)
        page = page_dir / "SM00-abstract.md"
        page.write_text(
            "# SM00 · Abstract\n\n## Opening\nWhat must this abstract establish?\n\n"
            "## Content\n### 1 · Different heading on purpose\nA current sentence.\n"
            "### 2 · Extra current section\nAnother current sentence.\n\n"
            "## Aims\n- A1.1 · Review the shape.\n\n## States\n- ⬜ A1.1 · Waiting.\n",
            encoding="utf-8",
        )
        (outline / "SM00-abstract-outline-v1.md").write_text(PLAN, encoding="utf-8")
        (outline / "SM00-abstract-evidence-items.md").write_text(ITEMS, encoding="utf-8")
        (outline / "SM00-abstract-feedback.md").write_text(
            "# SM00 · feedback\npage: SM00-abstract\n"
            "kind: feedback · generated\nstatus: 1 of 1 open · 0 landed · 1 round(s)\n\n"
            "The Round's own words, copied. To argue, open a thread.\n\n"
            "## RD01 · MISQ feedback cycle\n"
            "**🔴 rewrite** · Reviewer · [source.md](source.md)\n\n"
            "**Ask** · Keep the clinical decision visible.\n\n"
            "**Order** · problem → evidence → contribution.\n\n"
            "**Gate** · Use a checked value.\n\n"
            "### S0-PP1 · Reposition the opening\n"
            "- **From**: R01\n"
            "- **Feedback**: Begin with the physician decision problem.\n"
            "- **Work**: Rewrite the opening sentence.\n"
            "- **State**: open\n"
            "- **Landed**: —\n"
            "  ↳ R01 · routes SM00-abstract\n",
            encoding="utf-8",
        )
        (outline / "SM00-abstract-evidence.md").write_text(
            "# SM00 · evidence\n\n### E01 · review cohort counts\n"
            "- **Status**: specified\n",
            encoding="utf-8",
        )
        (outline / "SM00-abstract-requirement.md").write_text(
            "# SM00 · requirement\npage: SM00-abstract\n"
            "kind: requirement · generated venue + authored page writing\n\n"
            "# --- requirement:begin (generated) ---\n"
            "REQUIREMENT, MEASURED 260902 1200. GENERATED; do not hand-edit.\n"
            "# --- requirement:end ---\n\n"
            "# --- writing:begin (authored) ---\n"
            "### W1 · Keep estimates and intervals together\n"
            "- **Rule**: Report each estimate with its 95% confidence interval.\n"
            "- **Applies**: Results sentences.\n"
            "- **Source**: Section reporting contract.\n"
            "# --- writing:end ---\n",
            encoding="utf-8",
        )
        (outline / "SM00-abstract-log.md").write_text(
            "# SM00 · log\n\n### 260903 1200 · Outline grouped\n",
            encoding="utf-8",
        )
        skill = outline / "skill"
        skill.mkdir()
        (skill / "SM00-abstract.md").write_text(
            "# skill map · SM00-abstract\n\n- haipipe-page-outline\n",
            encoding="utf-8",
        )
        (skill / "SM00-abstract-skill.html").write_text(
            "<!doctype html><title>Skills</title>", encoding="utf-8"
        )
        return page

    def test_plan_header_is_compact_and_shows_the_four_outline_cycles(self):
        with tempfile.TemporaryDirectory() as directory:
            page = self._page(directory)
            body = plan_card(page)
            for wanted in (
                "✍️ plan v1", "approved: ⬜", "1 evidence item · Decisions 0/1",
                "1</b> SHAPE", "2</b> SURVEY", "3</b> LAND", "4</b> EMBED",
                "E01-VALUE-review-cohort-counts",
                "Supporting Runs", "Local Input", "Local Run", "Decide",
            ):
                self.assertIn(wanted, body)
            self.assertNotIn("PageX Bindings", body)
            for retired in ("Review this Section", "Shape ↔ Content map",
                            "Shape/content mismatch", "waiting on a person",
                            "routed record", "① <b>Shape</b>"):
                self.assertNotIn(retired, body)
            self.assertIn("E1V.ReviewCohort", body)
            self.assertNotIn("📝 E1", body)
            start = body.index('<div id="typed-ev1" popover')
            card = body[start:body.index("</div></div>", start) + len("</div></div>")]
            self.assertIn("E01-VALUE-review-cohort-counts", card)
            for field in (
                "Target", "Expected", "Acceptance", "Supporting Runs",
                "Local Input", "Local Run", "Result", "Decide",
            ):
                self.assertIn(field, card)
            self.assertNotIn("PageX Bindings", card)

    def test_outline_owns_one_internal_evidence_workspace(self):
        with tempfile.TemporaryDirectory() as directory:
            page = self._page(directory)
            rendered = render(
                "SM00", parse_outline(page.read_text(encoding="utf-8")), page,
                root=directory,
                path_q="/Board/board.md", file_q="MAIN/SM00-abstract/SM00-abstract.md",
            )
            self.assertIn("Bullet Workspace", rendered)
            self.assertIn("Evidence Workspace", rendered)
            self.assertIn("Context Workspace", rendered)
            self.assertNotIn("Plan Context", rendered)
            self.assertNotIn("Page Records", rendered)
            self.assertIn("🛠 Skills · 1", rendered)
            self.assertIn("data-lens=skills", rendered)
            self.assertIn("/SM00-abstract/outline/skill/SM00-abstract-skill.html?embed=1", rendered)
            self.assertIn("/_board/evidence?path=/Board/board.md&amp;file=MAIN/SM00-abstract/SM00-abstract.md&amp;embed=1", rendered)
            self.assertNotIn("Evidence / Survey", rendered)
            self.assertIn("🗣 Feedback", rendered)
            self.assertIn("📏 Requirement", rendered)
            self.assertIn("Keep estimates and intervals together", rendered)
            self.assertIn("<b>1</b> open", rendered)
            self.assertIn("Main ask", rendered)
            self.assertIn("Order, gate &amp; source", rendered)
            self.assertIn("Begin with the physician decision problem", rendered)
            self.assertIn("<b>Next</b>Rewrite the opening sentence", rendered)
            self.assertIn("Source &amp; routing", rendered)
            self.assertNotIn("The Round's own words", rendered)

    def test_skills_record_uses_newest_outline_log_date(self):
        with tempfile.TemporaryDirectory() as directory:
            page = self._page(directory)
            log = page.parent / "outline" / "SM00-abstract-log.md"
            log.write_text(
                "# log\n\n### 260902 1200 · earlier\n\n"
                "### 260903 0900 · later\n",
                encoding="utf-8",
            )
            self.assertEqual(SkillmapMixin._page_log_date(page), "260903")

    def test_skill_index_crosses_installed_plugin_boundaries(self):
        with tempfile.TemporaryDirectory() as directory:
            plugins = Path(directory) / "plugins"
            toolkit = plugins / "haipipe-toolkit" / "skills"
            labeling = plugins / "subjective-label" / "skills"
            for root, name in ((toolkit, "workflow-table"),
                               (labeling, "subjective-label")):
                skill = root / name
                skill.mkdir(parents=True)
                (skill / "SKILL.md").write_text(
                    f"---\nname: {name}\ndescription: fixture\n---\n",
                    encoding="utf-8",
                )
            agent_dir = plugins / "subjective-label" / "agents"
            agent_dir.mkdir()
            (agent_dir / "label-keeper-agent.md").write_text(
                "# label keeper\n", encoding="utf-8"
            )

            fake_source = (toolkit / "board" / "haipipe-board" / "live" /
                           "skillmap.py")
            fake_source.parent.mkdir(parents=True)
            roots = SkillmapMixin._skill_roots(fake_source)
            index = SkillmapMixin()._skill_index(roots)

            self.assertIn("workflow-table", index)
            self.assertIn("subjective-label", index)
            self.assertTrue(index["label-keeper-agent"]["agent"])

    def test_skills_surface_does_not_claim_a_seed_is_human_ranked(self):
        class Harness(SkillmapMixin):
            @staticmethod
            def _url_of(path):
                return "/" + Path(path).name

        with tempfile.TemporaryDirectory() as directory:
            page = self._page(directory)
            skill_dir = page.parent / "outline" / "skill"
            store = skill_dir / "SM00-abstract.md"
            state = {
                "page": page,
                "dir": skill_dir,
                "stem": "SM00-abstract",
                "store": store,
                "rows": {},
                "order": [],
                "ctx": {"path": "/Board/board.md", "file": "MAIN/SM00-abstract.md"},
            }
            Harness()._skillmap_view(state, {})
            skill_html = (skill_dir / "SM00-abstract-skill.html").read_text(
                encoding="utf-8"
            )
            self.assertIn("drag to rank · refresh appends", skill_html)
            self.assertNotIn("top = most related", skill_html)
            self.assertNotIn("last moved", skill_html)


if __name__ == "__main__":
    unittest.main()
