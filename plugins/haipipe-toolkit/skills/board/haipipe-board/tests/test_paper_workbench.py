#!/usr/bin/env python3
"""📄 Paper Workbench: live, storage-less, one paper Board → four Spaces.

The teeth: no per-paper file is needed (the old console/ folder must not be
read), a P0 board with a plan but no Content still lists its ideas, one Codex
session per Section Page and none for Ideation/Story, gates come from named
files, and every Space carries its own Runs panel beside the content (JL 260927).
"""
import sys
import json
import shutil
import re
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent  # the engine dir
sys.path.insert(0, str(HERE))
from live.paper import collect, paper_run_types, render_paper, section_rows, session_rows, task_home  # noqa: E402
from live.paper import render_run_result, run_files, run_result_url  # noqa: E402

BOARD = """# Paper-Test · paper board
spine: one idea, told to a desk
close: every Section Page accepted
dialect: paper
paper-root: .

## Pages

### STORY · A1-Story
Story00-ideation.md
StoryA-desk-idea.md

### MAIN · Ba-DESK-Main
S-DESK-Main-1-Introduction.md

## Links

paper-root .
"""

PLAN = """# Story00-ideation · outline v0.1
outline-version: v0.1
approved: ⬜

## C1 · Direction
### C1.P1 · Object
- B1 · Define the object
  Evidence: none · boundary

## C2 · Idea 1: First idea
### C2.P1 · Design
- B1 · Freeze a denominator
  Evidence: E01-CITE-prior-art · closest work
- B2 · Separate entry from order
  Evidence: none · design

## C3 · Idea 2: Second idea
### C3.P1 · Design
- B1 · Something else
  Evidence: none · design
"""

ITEMS = """# Story00-ideation · evidence items
### E01-CITE-prior-art · C2.P1.B1 · closest prior work
- **Target**: C2.P1.B1
- **Verified**: ⬜
"""

STORY = """# StoryA-desk-idea
state: 🟡 PARTIAL

## Content

### 1 · Identity
**Study identity**: what this paper is.

```text
📛 WORKING TITLE   Traits and Prescribing
🎯 IDENTITY        tests whether a text-inferred trait predicts
                   prescribing beyond the rating
```

#### 1.1 · One-sentence identity
This paper tests whether a review-inferred trait predicts prescribing.

### 2 · Pitch

Review text may carry a signal the star rating does not show.

### 3 · Research Questions
| RQ | question | answer state |
|---|---|---|
| RQ1 | Does it hold? | ⬜ open |

### 5 · Evidence Basis and Boundaries
| E-row | RQ | status | proposition | owed work |
|---|---|---|---|---|
| E1 (C1) | RQ1 | 🔨 provisional | It holds beyond the rating | rerun on the full cohort |

### 6 · Discovery Roadmap
| D | what the paper must learn | scope | feeds |
|---|---|---|---|
| D1 | what prior work says | landscape · b01.j01 | RQ1 |
| D2 | whether it is novel | prior art | RQ1 |

### 7 · Task Roadmap
| T | evidence obligation | design | feeds |
|---|---|---|---|
| T1 | the main estimate | cohort model | RQ1 · b01.j01.t01 |
| T2 | a robustness check | alt spec | RQ1 |

### 8 · Section Narrative
| Section (target · order) | reader question | entry |
|---|---|---|
| S-DESK-Main-1-Introduction (DESK · 1) | Why now? | knows little |
| S-DESK-Main-2-Results (DESK · 2) | What was found? | knows the question |

<!-- haipipe:compile-order:start -->
main:
- S-DESK-Main-1-Introduction
- S-DESK-Main-2-Results
<!-- haipipe:compile-order:end -->
"""


def make_board(root):
    b = root / "papers" / "Paper-Test"
    (b / "A1-Story" / "Story00-ideation" / "outline").mkdir(parents=True)
    (b / "A1-Story" / "StoryA-desk-idea").mkdir(parents=True)
    (b / "Ba-DESK-Main" / "S-DESK-Main-1-Introduction" / "runs").mkdir(parents=True)
    (b / "Ba-DESK-Main" / "S-DESK-Main-1-Introduction" / "results" / "run-structure-0901-outline").mkdir(parents=True)
    (b / "board.md").write_text(BOARD, encoding="utf-8")
    s00 = b / "A1-Story" / "Story00-ideation"
    (s00 / "Story00-ideation.md").write_text("# Story00\nstate: 🔴 OPEN\n\n## Opening\nq\n\n## Aims\n- ⬜ A1.1\n", encoding="utf-8")
    (s00 / "outline" / "Story00-ideation-outline-v0.1.md").write_text(PLAN, encoding="utf-8")
    (s00 / "outline" / "Story00-ideation-evidence-items.md").write_text(ITEMS, encoding="utf-8")
    (b / "A1-Story" / "StoryA-desk-idea" / "StoryA-desk-idea.md").write_text(STORY, encoding="utf-8")
    sec = b / "Ba-DESK-Main" / "S-DESK-Main-1-Introduction"
    (sec / "S-DESK-Main-1-Introduction.md").write_text("# S-DESK-Main-1-Introduction · §1 Introduction\nstate: DRAFT\n", encoding="utf-8")
    (sec / "runs" / "run-structure-0901-outline.md").write_text("ticket", encoding="utf-8")
    (sec / "runs" / "run-paragraph-0902-p01.md").write_text("ticket", encoding="utf-8")
    (sec / "runs" / "re-display-01_hero.md").write_text("ticket", encoding="utf-8")     # the Local Run E01 names
    (sec / "results" / "re-display-01_hero").mkdir(parents=True)
    (sec / "results" / "re-display-01_hero" / "runtime.yaml").write_text("status: complete\nstep: s003\n", encoding="utf-8")
    (sec / "outline").mkdir()
    (sec / "outline" / "S-DESK-Main-1-Introduction-evidence-items.md").write_text(
        "# items\n### E01-DISPLAY-hero-figure · C1.P1.B1 · the hero figure\n- **Label**: HeroFig\n- **Expected**: DISPLAY · main effect\n"
        "- **Supporting Runs**: Execution · reuse · b01j01t01r01; Execution · rerun · b01.j01.t01.r09; Discovery · reuse · b01j01t01r01\n"
        "- **Local Run**: Page · Evidence Item · reuse · re-display-01 → results/re-display-01_hero/result.yaml\n"
        "### E02-CITE-prior · C1.P1.B2 · prior work\n- **Verified**: ⬜\n"
        "#### E03-VALUE-old-number · retired from the opening\n- **Label**: OldNum\n"
        "- **Local Run**: Page · Evidence Item · reuse · run-value-0903-old → results/run-value-0903-old/result.yaml\n", encoding="utf-8")
    # a judgment Run on the Story: run-paper-claim ticket + runtime, target E1
    st = b / "A1-Story" / "StoryA-desk-idea"
    (st / "runs").mkdir(); (st / "results" / "run-paper-claim-0901-beyond-rating").mkdir(parents=True)
    (st / "runs" / "run-paper-claim-0901-beyond-rating.md").write_text("---\nfamily: paper\ntarget: E1\nrun: run-paper-claim-0901-beyond-rating\n---\n", encoding="utf-8")
    (st / "results" / "run-paper-claim-0901-beyond-rating" / "runtime.yaml").write_text("status: waiting-for-feedback\nstep: s002\n", encoding="utf-8")
    # the project's Task home: root/tasks/b01_block/ with both Task shapes
    t = root / "tasks" / "b01_block" / "j01_job" / "t01_task"            # Stata dialect: the task owns runs/ results/
    (t / "runs").mkdir(parents=True); (t / "results" / "r01_first").mkdir(parents=True); (t / "scripts").mkdir()
    (t / "t01_task.md").write_text("# t01_task\n\nstate: ✅ COMPLETE\ndevelops: the joined cohort table\n")
    (t / "runs" / "r01_first.sh").write_text("#!/bin/sh\n")
    (t / "results" / "r01_first" / "runtime.yaml").write_text("run: r01_first\nstatus: complete\n")
    dt = root / "discoveries" / "b01_evidence_board" / "j01_landscape_inquiry" / "t01_prior_work"
    (dt / "runs").mkdir(parents=True); (dt / "results" / "r01_smith2020").mkdir(parents=True)
    (root / "discoveries" / "b01_evidence_board" / "board.md").write_text("# Evidence\nboard-kind: discovery-block\n")
    (dt.parent / "_index.md").write_text("# L01 landscape\n")
    (dt / "t01_prior_work.md").write_text("# Prior work\nstate: 🟡 REPORTED\n")
    (dt / "runs" / "r01_smith2020.sh").write_text("#!/bin/sh\n")
    (dt / "discovery.yaml").write_text("kind: discovery\nstatus: reported\nquestion: |\n  Does prior work already link the trait to prescribing? And how?\nreport:\n  outcome: supports\n  confidence: medium\n")
    j = root / "tasks" / "b01_block" / "j02_flat"                         # flat shape: runs/<task>/ results/<task>/ scripts/<task>/
    (j / "runs" / "t01_flat").mkdir(parents=True); (j / "results" / "t01_flat" / "r01_go").mkdir(parents=True)
    (j / "scripts" / "t01_flat").mkdir(parents=True)
    (j / "runs" / "t01_flat" / "r01_go.sh").write_text("#!/bin/sh\n")
    (j / "results" / "t01_flat" / "r01_go" / "runtime.yaml").write_text("status: running\n")
    (j / "scripts" / "t01_flat" / "t01_flat.py").write_text('"""Rank the flat things by score."""\n')
    # the retired static prototype must NOT be a source
    (b / "console").mkdir()
    (b / "console" / "data.js").write_text("window.BOARD_CONSOLE={'ideas':['GHOST']}", encoding="utf-8")
    # what leaves the paper: delivery/ as haipipe-paper-assemble writes it, plus one page fragment
    dl = b / "delivery"
    (dl / "latex").mkdir(parents=True); (dl / "word").mkdir(); (dl / "word-feedback").mkdir()
    (dl / "paper-build.toml").write_text('[paper]\nid = "Paper-Test"\ntitle = "Traits and Prescribing"   # fallback\ndesk = "desk2026"\n'
                                         '[profile]\nvenue_label = "Test Quarterly"\n[outputs]\nmain_pdf = "latex/Paper-Test-draft.pdf"\n'
                                         'main_docx = "word/Paper-Test-draft.docx"\nsupplement_pdf = "latex/Paper-Test-supplement.pdf"\n')
    (dl / "latex" / "master.tex").write_text("\\input{sections/S-DESK-Main-2-Results}\n")
    (dl / "latex" / "Paper-Test-draft.pdf").write_bytes(b"%PDF-1.4 test")
    (dl / "word" / "Paper-Test-draft.docx").write_bytes(b"PK test")
    (dl / "word-feedback" / "Paper-Test-coauthor.docx").write_bytes(b"PK returned")
    (dl / "display-register.md").write_text("# Display register\n\nBuilt 2026-09-09 10:49 · 1 figure(s) + 0 table(s) printed.\n\n```text\n"
                                            "PRINTED    DECLARED   LABEL            UNIT                                   PAGE\n"
                                            "Figure 1   Figure 1   fig:hero         S-DESK-Main-2-Results/Display1-hero    S-DESK-Main-2-Results\n```\n")
    (dl / "build-manifest.json").write_text(json.dumps({
        "engine": "haipipe-paper-assemble 0.7.9", "built": "2026-09-09T10:49:47", "status": "DRAFT",
        "order": {"main": ["S-DESK-Main-1-Introduction", "S-DESK-Main-2-Results"], "appendix": []},
        "order_source": "compile-order block · A1-Story/StoryA",
        "pages": [{"id": "S-DESK-Main-1-Introduction", "ready": True, "reasons": [], "warnings": ["fragment may be stale"],
                   "outline": {"version": "v1.0", "approval": "✅ JL 260906 · in chat"}}],
        "readiness": {"ready": 1, "total": 2, "not_ready": [{"id": "S-DESK-Main-2-Results", "reasons": ["outline not approved (no v1.x)"]}]},   # the engine's real shape: one dict per page
        "submission_readiness": {"status": "DRAFT", "blockers": ["G4 unverified"]},
        "warnings": ["bib key smith2020 differs between two pages"], "unresolved_refs": [], "bib_entries": 7,
        "build": {"main_text_words": 1200, "main_text_word_limit": None, "citations": 5, "main_tables": 0, "main_figures": 1,
                  "checks": {"master_exists": True, "citations_resolved": False, "g6_human_decision": False}},
        "render": {"latexmk_rc": 0, "docx_rc": 0}, "evidence": {"mode": "draft", "pending_markers": [], "unaccepted_items": []}}))
    (sec / "delivery" / "latex").mkdir(parents=True, exist_ok=True)     # the one minted Section page carries a fragment
    (sec / "delivery" / "latex" / "S-DESK-Main-1-Introduction.tex").write_text("Introduction body\n")
    (sec / "delivery" / "latex" / "S-DESK-Main-1-Introduction.pdf").write_bytes(b"%PDF-1.4 page")
    return b


class PaperWorkbenchTest(unittest.TestCase):
    def test_legacy_numbered_stories_are_read_as_stories(self):
        from live.paper import STORY_STEM
        for stem in ("StoryA-desk-idea", "StoryB", "Story01-seed", "Story03-narrative-MISQ"):
            self.assertTrue(STORY_STEM.match(stem), stem)
        for stem in ("Story00-ideation", "Storyline", "S-MISQ-Main-Intro"):
            self.assertIsNone(STORY_STEM.match(stem), stem)

    def test_collects_the_spaces_from_markdown_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            b = make_board(root)
            d = collect(b, "/papers/Paper-Test/board.md")
            # Ideation: a P0 page with no Content lists the plan's Idea divisions
            ideas = d["ideation"]["ideas"]
            self.assertEqual([i["id"] for i in ideas], ["i01", "i02"])
            self.assertEqual(ideas[0]["title"], "First idea")
            self.assertEqual(len(ideas[0]["bullets"]), 2)
            self.assertEqual(ideas[0]["bullets"][0]["head"], "Freeze a denominator")
            self.assertEqual(ideas[0]["items"][0]["id"], "E01-CITE-prior-art")
            self.assertEqual(ideas[0]["chips"], ["E01-CITE-prior-art"])
            self.assertIn("Idea divisions", d["ideation"]["source"])
            self.assertEqual(d["ideation"]["items"][0]["id"], "E01-CITE-prior-art")
            self.assertEqual(d["ideation"]["receipts"][0]["state"], "absent")
            # Story: RQ rows, Section rows joined to minted pages, compile order
            s = d["story"][0]
            self.assertEqual(s["rq"][0][0], "RQ1")
            self.assertEqual([r["id"] for r in s["sections"]],
                             ["S-DESK-Main-1-Introduction", "S-DESK-Main-2-Results"])
            self.assertIsNotNone(s["sections"][0]["rel"])
            self.assertIsNone(s["sections"][1]["rel"])
            self.assertEqual(s["order"], ["S-DESK-Main-1-Introduction", "S-DESK-Main-2-Results"])
            # Supporting runs: the Evidence Items' citations, as a Block › Job › Task › Run tree
            self.assertIn("b01", d["supporting"]["Execution"])
            self.assertIn("b01", d["supporting"]["Discovery"])
            # Gates read files, never percentages
            gates = dict((g, v) for g, _n, v in d["gates"])
            self.assertTrue(gates["G0"].startswith("⬜ open"))
            self.assertEqual(gates["G3"], "1 of 2 Section Narrative rows have a Section page")
            self.assertEqual(gates["G4"], "DRAFT · 1/2 pages ready")       # read from delivery/build-manifest.json

    def test_idea_card_shows_the_idea_before_its_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            b = make_board(root)
            s00 = b / "A1-Story" / "Story00-ideation" / "Story00-ideation.md"
            s00.write_text(
                "# Story00\nstate: 🟡 PARTIAL\n\n## Content\n\n### 2 · Ideas (ranked)\n\n"
                "| id | idea | novelty | pilot | verdict | went to |\n|---|---|---|---|---|---|\n"
                "| i1 | Traits and prescribing | MEDIUM · closest work archived | SKIPPED · retrofit | ✅ PROCEED WITH CAUTION | StoryA-desk-idea |\n\n"
                "### 3 · Idea 1: Traits and prescribing\n\n**Research Question**\n\nDoes agreeableness predict prescribing beyond the rating?\n\n"
                "**Method**\n\nLink reviews to claims.\n\n"
                "**Hypothesis**\n\nAgreeableness predicts prescribing beyond the rating.\n\n"
                "**Core Claims**\n\n- Beyond-rating signal · MEDIUM\n- Discretion boundary · MEDIUM\n\n"
                "**Risk**\n\nReputation, not disposition.\n", encoding="utf-8")
            d = collect(b, "/papers/Paper-Test/board.md")
            idea = d["ideation"]["ideas"][0]
            self.assertEqual(idea["id"], "i1")
            self.assertEqual([k for k, _ in idea["substance"]], ["Research Question", "Method", "Hypothesis", "Core Claims", "Risk"])
            page = render_paper(b, root, "/papers/Paper-Test/board.md")
            self.assertIn("Agreeableness predicts prescribing beyond the rating.", page)
            self.assertIn("<li>Beyond-rating signal · MEDIUM</li>", page)
            # the idea comes before the comparison metadata inside the card
            self.assertLess(page.index("Link reviews to claims."), page.index("closest work archived"))
            # the card LEADS with the research question; the title drops to the subline
            self.assertIn('<span class="item-label">Does agreeableness predict prescribing beyond the rating?</span>', page)
            self.assertIn('<span class="item-title">Traits and prescribing</span>', page)
            self.assertNotIn("no Research Question written yet", page)

    def test_sessions_are_per_section_page_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            b = make_board(root)
            d = collect(b, "/papers/Paper-Test/board.md")
            d["root"] = root
            rows = session_rows(d)
            self.assertEqual([r["stem"] for r in rows], ["S-DESK-Main-1-Introduction"])
            self.assertEqual(rows[0]["pair"], "paper-desk-introduction")
            self.assertEqual(rows[0]["state"], "no session · plan")

    def test_task_home_falls_back_to_singular_task_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            board = make_board(root)
            shutil.move(str(root / "tasks"), str(root / "task"))
            d = collect(board, "/papers/Paper-Test/board.md")
            self.assertEqual(d["blocks"]["dir"].name, "task")
            self.assertEqual(d["blocks"]["blocks"], ["b01_block"])
            self.assertEqual(d["blocks"]["n_tasks"], 2)
            self.assertTrue(d["blocks"]["label"].endswith("/task/"))
            flat = d["blocks"]["tree"][0]["jobs"][1]
            self.assertEqual(flat["shape"], "runs/ · scripts/ · results/ per task")
            self.assertEqual(flat["tasks"][0]["develops"], "Rank the flat things by score.")
            self.assertEqual(flat["tasks"][0]["receipts"], {"running": 1})
            self.assertEqual(d["disc"]["n_tasks"], 1)
            self.assertEqual(d["disc"]["tree"][0]["jobs"][0]["tasks"][0]["outcome"], "supports")
            shutil.rmtree(board / "delivery")
            page = render_paper(board, root, "/papers/Paper-Test/board.md")
            self.assertIn("No delivery/ yet.", page)
            self.assertIn('data-space="delivery"', page)

    def test_a_row_with_two_addresses_resolves_both(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            b = make_board(root)
            d = collect(b, "/papers/Paper-Test/board.md")
            home = task_home(d, ["T9", "two jobs answer this", "alt spec. Task: b01.j01. Task: b01.j02."])
            self.assertEqual([x["address"] for x in home["all"]], ["b01.j01", "b01.j02"])   # never only the first match
            self.assertEqual(home["address"], "b01.j01")                                  # the first stays the row's own keys
            self.assertTrue(all(x["state"].startswith("allocated") for x in home["all"]))
            none = task_home(d, ["T2", "a robustness check", "alt spec"])
            self.assertEqual((none["state"], none["all"]), ("no folder yet", []))        # a row id like T2 is not an address

    def test_logic_work_tree_reads_question_blocks(self):
        """JL 260929: the question is the block. §3 holds its hypotheses, potential claims,
        potential contributions and potential work, coded 1a, 1b …, each a short name and a
        sentence. Work is named as questions and runs in stage order; the foundation every
        question stands on (§7 `every question`) sits folded inside each question, shared."""
        from live.paper import _addresses, _q_block, _rest_block, _row_ids, question_blocks, story_tree
        self.assertEqual(_addresses("b03.j02.t01–t03 · b03.j02.t05"),
                         ["b03j02t01", "b03j02t02", "b03j02t03", "b03j02t05"])   # a range names each task
        self.assertEqual(_row_ids("E1-E4, E10; RQ1–RQ3 · E01-CITE-prior · C1.P1.B1 · T2's"),
                         ["E1", "E2", "E3", "E4", "E10", "RQ1", "RQ2", "RQ3", "T2"])   # no item id, no Bullet
        with tempfile.TemporaryDirectory() as tmp:
            b = make_board(Path(tmp))
            story = b / "A1-Story" / "StoryA-desk-idea" / "StoryA-desk-idea.md"
            text = story.read_text(encoding="utf-8")
            text = text.replace("| RQ | question | answer state |\n|---|---|---|\n| RQ1 | Does it hold? | ⬜ open |\n",
                                "#### 3.1 · Question 1 · RQ1\n- **Question**: Does it hold?\n- **Answer state**: ⬜ open\n\n"
                                "**Hypotheses**\n- **1a** · Holds beyond the rating: the trait adds to the star rating. · tested by E1\n"
                                "- **1b** · A second reading: it holds on the other scale too. · tested by E2\n\n"
                                "**Potential claims**\n- **1a** · C1 · from 1a · Beyond the rating: the trait predicts prescribing beyond it.\n"
                                "  - **Role**: primary · **If it fails**: the paper narrows to the `review_text` signal alone.\n"
                                "- **1b** · C2 · from 1b · Holds twice: the second reading holds too.\n\n"
                                "**Potential contributions**\n- rests on 1a, 1b · A new signal: the trait adds to the rating.\n\n"
                                "**Potential work**\n- **D1** · for 1a, 1b\n- **T1** · for 1a\n- **T2** · for 1b\n\n"
                                "#### 3.2 · Question 2 · RQ2\n- **Question**: Is it stronger in one group?\n\n"
                                "**Hypotheses**\n- **2a** · Stronger in one group: the effect is larger there. · tested by E1\n\n"
                                "**Potential work**\n- **T1** · for 2a\n")
            text = text.replace("| rerun on the full cohort |\n",
                                "| rerun on the full cohort |\n| E2 | RQ1 | ✅ established | A second claim | owed to T2 |\n")
            text = text.replace("| T | evidence obligation | design | feeds |\n|---|---|---|---|\n"
                                "| T1 | the main estimate | cohort model | RQ1 · b01.j01.t01 |\n"
                                "| T2 | a robustness check | alt spec | RQ1 |",
                                "| T | name | question | stage | design | feeds |\n|---|---|---|---|---|---|\n"
                                "| T1 | Main estimate right? | We fit the cohort model and check the main estimate. | analysis | cohort model | RQ1 · b01.j01.t01 |\n"
                                "| T2 | Survives a check? | We rerun it on another spec. | analysis | alt spec | RQ1 |\n"
                                "| T3 | Which readings? | We list the readings used. | data | the cohort | every question |\n"
                                "| T4 | Anything left over? | We look for loose work. | figures | none | none yet |")
            story.write_text(text, encoding="utf-8")
            d = collect(b, "/papers/Paper-Test/board.md")
            d["root"] = Path(tmp).resolve()                             # as render_paper sets it
            qb = question_blocks(story.read_text(encoding="utf-8"))
            self.assertEqual([[h["id"] for h in x["hypotheses"]] for x in qb], [["1a", "1b"], ["2a"]])
            self.assertIn(("If it fails", "the paper narrows to the review_text signal alone."), qb[0]["claims"][0]["fields"])
            T = story_tree(d["story"][0])
            q = T["questions"][0]
            self.assertEqual([(c["id"], c["alias"], c["from"]) for c in q["claims"]], [("1a", "C1", ["1a"]), ("1b", "C2", ["1b"])])
            self.assertEqual([c["rests"] for c in q["contribs"]], [["1a", "1b"]])
            self.assertEqual([(i["w"], i["for"]) for i in q["items"]], [("D1", ["1a", "1b"]), ("T1", ["1a"]), ("T2", ["1b"])])
            self.assertEqual(T["shared"], ["T3"])                       # marked `every question`
            self.assertEqual(T["loose"], ["T4", "D2"])                  # named by no question
            self.assertEqual(T["up"]["T2"], ["1b", "E2", "RQ1"])        # its runs show when any of these is picked
            html_ = _q_block(d, T, q)
            self.assertIn('<span class="item-kind">Question 1</span></div><div class="lw-qtext">Does it hold?</div>', html_)
            # no group labels: each pill names its kind (JL 260930: "of no information")
            self.assertNotIn('class="lw-k', html_)
            for group in ("Hypotheses", "Potential claims", "Potential contributions", "Foundation work",
                          "This question&#x27;s work"):
                self.assertNotIn(">%s<" % group, html_)
            self.assertNotIn("shared by all", html_)
            self.assertEqual(html_.count('<div class="lw-g">'), 5)       # 3 on the left, foundation and own work
            # coded by question; a short name in bold, then the sentence (JL 260929)
            # the pill and mark on one line, the name and sentence from the next (JL 260929)
            self.assertIn('<div class="lw-h" data-key="1a"><div class="lw-top"><span class="item-kind">Hypothesis 1a</span>'
                          '<span class="lw-mark">🔨</span></div><div class="lw-body"><b class="lw-name">Holds beyond the rating</b>:'
                          ' the trait adds to the star rating.</div>', html_)
            self.assertIn('<span class="lw-mark">✅</span>', html_)                   # 1b's test is established
            self.assertIn('<span class="item-kind">Claim 1a</span></div><div class="lw-body"><b class="lw-name">Beyond the rating</b>', html_)
            self.assertNotIn(">C1<", html_)                                           # the old id stays in the file only
            self.assertIn('<div class="lw-say">from Hypothesis 1a</div>', html_)
            self.assertIn('<div class="lw-say">rests on Claims 1a and 1b</div>', html_)
            # a contribution is labelled as a claim is (JL 260930)
            self.assertIn('<span class="item-kind">Contribution 1a</span></div><div class="lw-body"><b class="lw-name">A new signal</b>', html_)
            # an empty group says so under its kind's pill
            h2 = _q_block(d, T, T["questions"][1])
            self.assertIn('<span class="item-kind">Claim</span></div><div class="lw-say">none yet</div>', h2)
            self.assertIn('<span class="item-kind">Contribution</span></div><div class="lw-say">none yet</div>', h2)
            # the foundation sits inside the question, folded, first; then this question's own work
            self.assertIn('<details class="lw-w" data-key="T3" data-for="">', html_)
            self.assertLess(html_.index('data-key="T3"'), html_.index('data-key="T1"'))
            # every work item folds; closed, it still says what it tests and how big it is
            self.assertIn('<details class="lw-w" data-key="T1" data-for="1a"><summary>', html_)
            self.assertIn('<span class="lw-size">1 task · 1 run</span>', html_)
            # stage pill and short name on one line, the plain sentence below, as a question (JL 260930)
            self.assertIn('<span class="item-kind">Analysis</span><span class="lw-wq">Main estimate right?</span></div>'
                          '<div class="lw-wtext">We fit the cohort model and check the main estimate.</div>', html_)
            self.assertIn('<span class="lw-for">for Hypotheses 1a and 1b</span>', html_)
            self.assertIn('<span class="lw-also">also for Question 2</span>', html_)   # T1 is Question 2's work too
            self.assertEqual(html_.count("also for"), 1)
            self.assertLess(html_.index("Main estimate right?"), html_.index('<span class="item-kind">Discovery</span>'))
            self.assertNotIn("⬜ open", html_)                          # the answer state is not shown
            self.assertNotIn("<summary>Details</summary>", html_)
            self.assertEqual(html_.count('<details class="item-card"'), 0)   # JL 260929: no card inside the tree
            rest = _rest_block(d, T)
            self.assertIn("Not under a question", rest)
            self.assertIn("Anything left over?", rest)
            # a Question 0 that sets the tasks lists them first and leaves out its empty groups (JL 260930)
            story.write_text(story.read_text(encoding="utf-8").replace(
                "#### 3.1 · Question 1 · RQ1\n",
                "#### 3.0 · Question 0 · RQ0\n- **Name**: The tasks\n- **Question**: We say what the model learns and is tested on.\n\n"
                "**Tasks**\n- Pretraining · Next reading: it predicts the next reading.\n"
                "- Downstream · Forecast: it continues the readings 24 steps.\n\n"
                "**Hypotheses**\n- none: it tests no guess.\n\n#### 3.1 · Question 1 · RQ1\n"), encoding="utf-8")
            d = collect(b, "/papers/Paper-Test/board.md")
            d["root"] = Path(tmp).resolve()
            T = story_tree(d["story"][0])
            q0 = T["questions"][0]
            self.assertEqual((q0["id"], [x["kind"] for x in q0["tasks"]]), ("RQ0", ["Pretraining", "Downstream"]))
            h0 = _q_block(d, T, q0)
            self.assertIn('<span class="item-kind">Question 0</span><span class="lw-qname">The tasks</span>', h0)
            self.assertIn('<div class="lw-k lw-k-task">Tasks</div><div class="lw-h"><div class="lw-top">'
                          '<span class="item-kind">Pretraining</span>', h0)
            self.assertIn('<b class="lw-name">Next reading</b>: it predicts the next reading.', h0)
            for group in ("Hypotheses", "Potential claims", "Potential contributions"):
                self.assertNotIn(">%s</div>" % group, h0)
            self.assertNotIn("shared by all", h0)

    def test_a_run_opens_its_results(self):
        """JL 260930: "for a run, how could we have a popout window to show the results of
        that run's results". A run finds its files in its own results/<run>/, else by its
        name in a shared results/, else by every word of its name, else all of results/."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            task = root / "tasks" / "b01_a" / "j01_b" / "t01_c"
            for rel, text in (("runs/run_6a2_f01.sh", "#!/bin/bash\n"), ("runs/run_fit_forecast.sh", ""),
                              ("results/figures/6a2_f01_growth.png", "png"),
                              ("results/tables/6a2_t01_long.csv", "size,rmse\n1m,20.5\n10m,19.1\n"),
                              ("results/fits_forecast/alpha.json", "{}"),
                              ("results/r02_new/summary.md", "# Fit\n\n| a | b |\n|---|---|\n| 1 | <b>2</b> |\n"),
                              ("results/r02_new/runtime.yaml", "status: complete\n"),
                              ("results/r02_new/fit_summary.md", "Fit Summary\n===========\n  Form A: L(D) = 4.92\n    R2 = 0.09\n"),
                              ("notebooks/run_6a2_f01.ipynb", "{}")):
                (task / rel).parent.mkdir(parents=True, exist_ok=True)
                (task / rel).write_text(text, encoding="utf-8")
            names = lambda r: [f.name for f in run_files(task, r)[1]]
            self.assertEqual(run_files(task, "run_6a2_f01")[0], "the files in results/ whose name holds 6a2_f01")
            self.assertEqual(names("run_6a2_f01"), ["6a2_f01_growth.png"])
            self.assertEqual(names("r02_new"), ["fit_summary.md", "runtime.yaml", "summary.md"])   # its own folder
            self.assertEqual(names("run_fit_forecast"), ["alpha.json"])                   # fits_forecast/
            self.assertTrue(run_files(task, "run_zzz")[0].startswith("all of results/"))
            self.assertEqual(len(run_files(task, "")[1]), 6)
            url = run_result_url(root, task, "run_6a2_f01")
            self.assertEqual(url, "/_board/run-result?task=tasks/b01_a/j01_b/t01_c&run=run_6a2_f01")
            page = render_run_result(root, "tasks/b01_a/j01_b/t01_c", "run_6a2_f01")
            self.assertIn('<img loading="lazy" src="/tasks/b01_a/j01_b/t01_c/results/figures/6a2_f01_growth.png"', page)
            self.assertIn('href="/tasks/b01_a/j01_b/t01_c/runs/run_6a2_f01.sh"', page)          # Run script
            self.assertIn('href="/tasks/b01_a/j01_b/t01_c/notebooks/run_6a2_f01.ipynb"', page)  # Executed notebook
            whole = render_run_result(root, "tasks/b01_a/j01_b/t01_c", "")
            self.assertIn("<td>20.5</td>", whole)                                   # a table's first rows
            self.assertIn("2 rows · 2 columns", whole)
            own = render_run_result(root, "tasks/b01_a/j01_b/t01_c", "r02_new")
            self.assertIn("<h2>Receipt</h2><pre>status: complete", own)
            self.assertIn("<td>&lt;b&gt;2&lt;/b&gt;</td>", own)                     # Markdown table, HTML escaped
            # a .md with no Markdown mark is plain text laid out by line: shown as written (JL 260930)
            self.assertIn("<pre>Fit Summary\n===========\n  Form A: L(D) = 4.92\n    R2 = 0.09\n</pre>", own)
            with self.assertRaises(ValueError):
                render_run_result(root / "tasks", "../..", "")                     # never outside the root
            # in the workbench, a run line is a link the page opens in its pop-out
            b = make_board(root)
            page = render_paper(b, root, "/papers/Paper-Test/board.md")
            self.assertIn('<div id="rr-pop" hidden>', page)
            self.assertIn("a[data-pop]", page)

    def test_roadmap_draw_is_the_storys_excalidraw_in_studio(self):
        """JL 260930: a Story tab between Spine and the logic view, named RoadMap Draw by JL,
        shows the paper's Excalidraw drawing, saved in the paper's studio/ folder."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            b = make_board(root)
            page = render_paper(b, root, "/papers/Paper-Test/board.md")
            self.assertIn('data-tab="roadmap-draw" data-label="RoadMap Draw"', page)
            self.assertIn("'story/roadmap':'story/logic-work'", page)   # the retired Roadmap tab's links still go there
            self.assertLess(page.index('data-tab="spine"'), page.index('data-tab="roadmap-draw"'))
            self.assertLess(page.index('data-tab="roadmap-draw"'), page.index('data-tab="logic-work"'))
            url = "/_excalidraw/?board=papers/Paper-Test/studio/StoryA-desk-idea.excalidraw&amp;edit=1"
            # the canvas loads when the tab shows (data-src), not with the page
            self.assertIn('<iframe class="rd-frame" title="RoadMap Draw" referrerpolicy="no-referrer" data-src="%s"></iframe>' % url, page)
            self.assertIn('<a class="rd-open" href="%s" target="_blank" rel="noopener">Open full screen ↗</a>' % url, page)
            self.assertNotIn('class="rd-file', page)                  # one drawing: no switcher
            # a pick in the logic view draws no bar (JL 260930: "I don't want this as well")
            self.assertIn(".lw-h.runs-selected,.lw-w.runs-selected{background:transparent}", page)
            self.assertNotIn(".lw-q.runs-selected>summary", page)
            self.assertNotIn(".lw-w.lw-lit{", page)
            self.assertFalse((b / "studio").exists())                 # rendering writes nothing
            # a drawing already in studio/ opens instead of a new empty one
            (b / "studio").mkdir()
            other = "/_excalidraw/?board=papers/Paper-Test/studio/overview.excalidraw&amp;edit=1"
            (b / "studio" / "overview.excalidraw").write_text('{"type":"excalidraw","elements":[]}', encoding="utf-8")
            page = render_paper(b, root, "/papers/Paper-Test/board.md")
            self.assertIn('referrerpolicy="no-referrer" data-src="%s"></iframe>' % other, page)
            self.assertNotIn('class="rd-file', page)
            # the Story's own drawing, once it exists, comes first; the others are one click away
            (b / "studio" / "StoryA-desk-idea.excalidraw").write_text('{"type":"excalidraw","elements":[]}', encoding="utf-8")
            page = render_paper(b, root, "/papers/Paper-Test/board.md")
            self.assertIn('<button type=button class="rd-file on" data-src="%s">StoryA-desk-idea</button>'
                          '<button type=button class="rd-file" data-src="%s">overview</button>' % (url, other), page)

    def test_related_papers_are_venue_cards_with_their_pdf(self):
        """JL 260930: a Story tab after the logic view lists the target venue's related papers,
        one card each, and the card opens the original PDF. The rows are the Story's §5.3
        P-board; each names the Discovery Paper Run holding the paper and its paper.pdf."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            b = make_board(root)
            (root / "venue.md").write_text("# Test Quarterly: the desk that wants both\n", encoding="utf-8")
            board_md = b / "board.md"
            board_md.write_text(board_md.read_text(encoding="utf-8").replace(
                "paper-root .\n", "paper-root .\nvenue-page  ../../venue.md\n"), encoding="utf-8")
            story = b / "A1-Story" / "StoryA-desk-idea" / "StoryA-desk-idea.md"
            story.write_text(story.read_text(encoding="utf-8") + (
                "\n| P | paper | role | question | why it matters | Discovery Run |\n|---|---|---|---|---|---|\n"
                "| P1 | Smith et al. 2020 | closest | all | The nearest study at this desk. | b01.j01.t01.r01 |\n"
                "| P2 | Jones 2021 | caution | RQ1 | A caution on the same model. | b01.j01.t01.r02 |\n"
                "| P3 | Lost 2022 | question | RQ1 | Named, never run. | b01.j01.t01.r09 |\n"), encoding="utf-8")
            res = root / "discoveries" / "b01_evidence_board" / "j01_landscape_inquiry" / "t01_prior_work" / "results"
            r1, r2 = res / "r01_smith2020", res / "r02_jones2021"
            r2.mkdir(parents=True)
            (r1 / "runtime.yaml").write_text(
                'run: r01_smith2020\nsubject:\n  kind: paper\n  title: "Traits and prescribing"\n'
                '  doi: "10.1000/t1"\n  authors: "Ann Smith; Bo Lee"\n  venue: "Test Quarterly 1, 1-9 (2020) · Article"\n'
                'analysis:\n  reading_depth: abstract\n', encoding="utf-8")
            (r1 / "source-access.json").write_text(json.dumps(
                {"links": {"publisher": "https://example.test/t1"},
                 "local_pdf": {"path": "paper.pdf", "version": "published", "source": "https://example.test/t1.pdf"}}),
                encoding="utf-8")
            (r1 / "paper.pdf").write_bytes(b"%PDF-1.4\n")
            (r1 / "r01_smith2020.bib").write_text("@article{Smith_2020, title={Traits}}\n", encoding="utf-8")
            (r1 / "abstract.md").write_text("# Retrieved abstract\n\nSource: https://example.test/t1\n\nThe trait predicts it.\n",
                                            encoding="utf-8")
            (r2 / "runtime.yaml").write_text('subject:\n  title: "A caution"\n  authors: "Cy Jones"\n', encoding="utf-8")
            (r2 / "source-access.json").write_text('{"local_pdf": null}', encoding="utf-8")
            page = render_paper(b, root, "/papers/Paper-Test/board.md")
            self.assertIn('data-tab="related" data-label="Related Papers"', page)
            self.assertLess(page.index('data-tab="logic-work"'), page.index('data-tab="related"'))   # after the logic view
            rp = page[page.index('<div class="rp-list">'):page.index('<section class=runs-panel data-space="story"')]
            self.assertIn('<div class="rp-head">3 papers · 1 with a PDF</div>', rp)
            # the target venue first, then other venues (JL 260930: "this is not limited to NMI")
            self.assertIn('<h3 class="rp-venue">At Test Quarterly<span class="lw-kn">1</span></h3>', rp)
            self.assertIn('<h3 class="rp-venue">Other venues<span class="lw-kn">2</span></h3>', rp)
            self.assertLess(rp.index('data-key="P1"'), rp.index("Other venues"))
            self.assertLess(rp.index("Other venues"), rp.index('data-key="P2"'))
            self.assertIn('<div class="lw-k lw-k-hyp">Closest to this paper<span class="lw-kn">1</span></div>', rp)
            away = rp[rp.index("Other venues"):]
            self.assertLess(away.index("For one research question"), away.index("Cautions and framing"))
            p1 = rp[rp.index('data-key="P1"'):rp.index("Other venues")]
            # closed, two plain lines (JL 260930: "too messy … no need to show all the details in the card front face")
            front = p1[:p1.index("</summary>")]
            self.assertIn('<div class="rp-title">Traits and prescribing</div>', front)
            self.assertIn('<div class="rp-sub"><span>Smith et al. · 2020 · Test Quarterly</span>'
                          '<span class="rp-marks"><span class="rp-q">All</span><span title="PDF inside">📄</span></span></div>', front)
            for inside in ("The nearest study at this desk.", "published PDF", "cited in", "Abstract", "read: abstract"):
                self.assertNotIn(inside, front)
            # open: why it matters, links, the abstract folded, then the PDF; no facts line (JL 260930: "not relevant")
            self.assertIn('<p class="rp-why">The nearest study at this desk.</p>', p1)
            self.assertNotIn("rp-facts", page)
            self.assertNotIn("cited in", page)
            self.assertIn('<details class="rp-absd"><summary>Abstract</summary><p>The trait predicts it.</p></details>', p1)
            self.assertIn('<div class="rp-group">', rp)
            # the PDF sits in the card and loads only when the card opens
            pdf = "/discoveries/b01_evidence_board/j01_landscape_inquiry/t01_prior_work/results/r01_smith2020/paper.pdf"
            self.assertIn('<iframe class="rp-frame" title="PDF · Traits and prescribing" data-pdf="%s"></iframe>' % pdf, p1)
            self.assertNotIn('data-src="%s"' % pdf, page)                   # lazy() loads every data-src in a shown pane
            self.assertIn('href="%s" target="_blank"' % pdf, p1)
            self.assertIn("details.rp-card", page)
            p2 = rp[rp.index('data-key="P2"'):]
            self.assertIn("No free full text.", p2)
            self.assertIn("no Paper Run at b01j01t01r09", rp)

    def test_related_paper_card_shows_why_we_keep_it_and_its_logic_and_work(self):
        """JL 261002: a related-paper card says why OUR paper keeps it (the P-board's `keep`
        cell, with `bears on` marks per question) and shows the paper's own logic beside its
        work, read from the Paper Run's logic-work.yaml, like Story › High-level logic."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            b = make_board(root)
            story = b / "A1-Story" / "StoryA-desk-idea" / "StoryA-desk-idea.md"
            story.write_text(story.read_text(encoding="utf-8") + (
                "\n| P | paper | role | question | why it matters | keep | bears on | Discovery Run |\n"
                "|---|---|---|---|---|---|---|---|\n"
                "| P1 | Smith et al. 2020 | closest | all | A summary. | Our baseline: it never grades the field. "
                "| RQ1 limits; RQ2 supports | b01.j01.t01.r01 |\n"
                "| P2 | Jones 2021 | caution | RQ1 | A caution. |  |  | b01.j01.t01.r02 |\n"), encoding="utf-8")
            res = root / "discoveries" / "b01_evidence_board" / "j01_landscape_inquiry" / "t01_prior_work" / "results"
            r1, r2 = res / "r01_smith2020", res / "r02_jones2021"
            r1.mkdir(parents=True, exist_ok=True)
            r2.mkdir(parents=True, exist_ok=True)
            (r1 / "runtime.yaml").write_text('subject:\n  title: "Traits"\n  authors: "Ann Smith"\n', encoding="utf-8")
            (r1 / "logic-work.yaml").write_text(
                "run: r01_smith2020\naddress: b01.j01.t01.r01\nread_from: pdf\nkind: empirical\n"
                "question: Can a trait predict it?\ndata: '2,000 people, 3 sites'\n"
                "method:\n- Survey the trait\n- 'Regress: the outcome on it'\n"
                "findings:\n- \"r = 0.4, \\\"moderate\\\"\"\n- It holds out of sample\ncontribution: A trait measure\n",
                encoding="utf-8")
            (r2 / "runtime.yaml").write_text('subject:\n  title: "A caution"\n  authors: "Cy Jones"\n', encoding="utf-8")
            page = render_paper(b, root, "/papers/Paper-Test/board.md")
            rp = page[page.index('<div class="rp-list">'):page.index('<section class=runs-panel data-space="story"')]
            p1 = rp[rp.index('data-key="P1"'):rp.index('data-key="P2"')]
            self.assertIn('<div class="rp-keep"><div class="rp-keep-h">Why we keep it</div>'
                          '<p>Our baseline: it never grades the field.</p>', p1)
            self.assertNotIn("A summary.", p1)                     # `keep` wins over `why it matters`
            self.assertIn('<span class="rp-bear rp-bear-warn"><b>RQ1</b> limits</span>', p1)
            self.assertIn('<span class="rp-bear rp-bear-ok"><b>RQ2</b> supports</span>', p1)
            self.assertIn('Their work · read from the PDF', p1)
            for kind, text in (("Question", "Can a trait predict it?"), ("Data", "2,000 people, 3 sites"),
                               ("Method 2", "Regress: the outcome on it"), ("Finding 1", 'r = 0.4, &quot;moderate&quot;'),
                               ("Finding 2", "It holds out of sample"), ("Contribution", "A trait measure")):
                self.assertIn('<span class="item-kind">%s</span></div><div class="lw-body">%s</div>' % (kind, text), p1)
            self.assertLess(p1.index("Their logic"), p1.index('class="rp-acts"'))
            p2 = rp[rp.index('data-key="P2"'):]
            self.assertIn('<p class="rp-why">A caution.</p>', p2)   # no `keep`: the old line stays
            self.assertNotIn("rp-lw", p2)                           # no logic-work.yaml: no table
            self.assertNotIn("rp-bears", p2)

    def test_roster_headings_with_a_description_or_no_folder(self):
        from live.paper import board_pages
        groups = board_pages("## Pages\n\n### Story · the idea pool and the blueprint\n\nStory00-ideation.md\n\n"
                             "### JAMA-Main · Ba-JAMA-IM-Main · reader-ordered units\n\nS-JAMA-IM-Main-1-Introduction.md\n")
        self.assertEqual([(g["folder"], g["stems"]) for g in groups],
                         [("", ["Story00-ideation"]), ("Ba-JAMA-IM-Main", ["S-JAMA-IM-Main-1-Introduction"])])
        with tempfile.TemporaryDirectory() as tmp:
            b = make_board(Path(tmp))
            from live.paper import page_file
            self.assertEqual(str(page_file(b, "", "StoryA-desk-idea")), "A1-Story/StoryA-desk-idea/StoryA-desk-idea.md")

    def test_c8_rows_written_as_records(self):
        from live.paper import section_records
        recs = section_records("#### 8.2 · What each section must do\n\n"
                               "**S-JAMA-IM-Main-Abstract (0) · the whole paper in 350 words**\n"
                               "- **Reader question**: what are the question and the result?\n"
                               "- **Moves**: 1 Key Points · 2 abstract\n\n"
                               "**S-JAMA-IM-Main-1-Introduction (1) · why it matters now**\n"
                               "- **Reader question**: why does this deserve a study?\n"
                               "#### 8.3 · Display allocation\n- **Not a field**: of any record\n")
        self.assertEqual([(r["id"], r["target"], r["question"]) for r in recs],
                         [("S-JAMA-IM-Main-Abstract", "0", "What are the question and the result?"),
                          ("S-JAMA-IM-Main-1-Introduction", "1", "Why does this deserve a study?")])
        self.assertEqual(recs[0]["heads"], ["Section", "Reader question", "One job", "Moves"])
        self.assertEqual(recs[0]["cells"][2:], ["the whole paper in 350 words", "1 Key Points · 2 abstract"])
        self.assertEqual(recs[1]["heads"], ["Section", "Reader question", "One job"])   # a later heading ends the record

    def test_run_cards_give_every_space_its_buttons(self):
        kinds = paper_run_types()
        self.assertEqual(sorted(kinds), ["delivery", "ideation", "sections", "story"])
        self.assertEqual([k["label"] for k in kinds["story"]],
                         ["Story revise", "Claim review", "Task review", "Task runs", "Discovery runs", "Redraw"])
        self.assertEqual(kinds["story"][-1]["views"], "roadmap-draw")   # RoadMap Draw's own card
        self.assertTrue(all(k["prompt"] for ks in kinds.values() for k in ks))   # each button copies a prompt
        self.assertEqual(kinds["delivery"][-1]["views"], "rounds")

    def test_sections_follow_the_compile_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            b = make_board(root)
            d = collect(b, "/papers/Paper-Test/board.md")
            d["root"] = root
            d["sessions"] = session_rows(d)
            rows = section_rows(d)
            self.assertEqual([r["id"] for r in rows], ["S-DESK-Main-1-Introduction", "S-DESK-Main-2-Results"])
            self.assertEqual((rows[0]["num"], rows[0]["name"], rows[0]["state"]), ("1", "Introduction", "DRAFT"))
            self.assertEqual(rows[1]["state"], "not set up")               # a §8 row with no Section Page yet
            self.assertEqual(rows[0]["session"]["pair"], "paper-desk-introduction")

    def test_render_needs_no_console_and_links_back_to_outline(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            b = make_board(root)
            page = render_paper(b, root, "/papers/Paper-Test/board.md")
            self.assertNotIn("GHOST", page)
            self.assertNotIn("console/", page)                              # the ghost console/ is never read
            # four Spaces, each with its Runs panel on the right; the old Setup and Run Spaces are gone
            for space in ("ideation", "story", "sections", "delivery"):
                self.assertIn('<div class="panel space-split" data-space="%s">' % space, page)
                self.assertIn('<section class=runs-panel data-space="%s"' % space, page)
            for gone in ("Setup Space", "Run Space", "backend Markdown", "copy to chat", "⧉", "Workflow map",
                         "no Research Question written yet"):
                self.assertNotIn(gone, page)
            self.assertNotIn("fetch(", page)                                   # the page makes no request of its own
            # Ideation: collapsed Idea Cards; opening one selects it for the Runs panel
            self.assertEqual(page.count('<details class="item-card" id="idea-'), 2)
            self.assertIn('id="idea-i01" data-key="i1"', page)
            self.assertIn('<span class="item-label">First idea</span>', page)
            self.assertIn("Freeze a denominator", page)                      # bullet head in the detail
            self.assertIn("<summary>Writing plan</summary>", page)            # plan Bullets are collapsed, never the lead
            self.assertIn("closest prior work", page)                        # bound evidence item
            # Story › Spine: the Story's Identity face, its subsection, and the Pitch
            self.assertIn('<div class="card spine-card" data-key="C1">', page)
            self.assertIn("<b>Working Title</b><span>Traits and Prescribing</span>", page)
            self.assertIn("tests whether a text-inferred trait predicts prescribing beyond the rating", page)
            self.assertIn("This paper tests whether a review-inferred trait predicts prescribing.", page)
            self.assertIn("Review text may carry a signal the star rating does not show.", page)
            # Story › High-level logic + Low-level work (JL 260929): each question is a block,
            # its logic on the left, its work on the right with B → J → T → R
            self.assertIn('data-tab="logic-work" data-label="High-level logic + Low-level work"', page)
            self.assertNotIn('data-tab="roadmap"', page)
            self.assertNotIn('data-tab="questions"', page)
            self.assertIn("'story/roadmap':'story/logic-work'", page)       # an old link lands here
            self.assertIn("'story/questions':'story/logic-work'", page)
            self.assertIn('<div class="lw-l">High-level logic</div><div class="lw-r">Low-level work · B → J → T → R</div>', page)
            q1 = page[page.index('<details class="qc lw-q" data-key="RQ1">'):page.index('<section class=runs-panel data-space="story"')]
            self.assertIn('<span class="item-kind">Question 1</span></div><div class="lw-qtext">Does it hold?</div>', q1)
            self.assertNotIn("⬜ open", q1)                                # no answer state (JL 260929: "confusing")
            # a Story still writing the RQ table: each §5 row naming the RQ is one hypothesis
            self.assertIn('<div class="lw-h" data-key="E1">', q1)
            self.assertIn('<span class="item-kind">Hypothesis 1</span><span class="lw-mark">🔨</span></div>'
                          '<div class="lw-body">It holds beyond the rating</div>', q1)
            self.assertIn('<span class="item-kind">Task</span><span class="lw-wq">the main estimate</span>', q1)
            self.assertNotIn("lw-wtext", q1)                              # no `name` cell: the question alone
            self.assertIn('<span class="idtag">b01</span> <b>block</b>', q1)        # B
            self.assertIn('<span class="idtag">j01</span> job', q1)                 # J
            self.assertIn('<span class="idtag">t01</span>', q1)                     # T
            # a Task's name is plain text, not a link to its raw Markdown (JL 260930); a
            # Discovery task still opens its board in Outline
            self.assertIn('<span class="idtag">t01</span> task ', q1)
            self.assertNotIn('t01_task/t01_task.md', q1)
            self.assertIn("1 run · done 1", q1)                                      # R, folded: its receipt says done
            self.assertIn("no folder yet", q1)                                       # T2 names no folder
            self.assertIn("prior_work", q1)                                          # D1's Discovery task
            self.assertIn("supports · medium", q1)                                   # and what it found
            self.assertIn("discoveries%2Fb01_evidence_board%2Fboard.md", q1)         # link into the Discovery Board
            self.assertEqual(q1.count('<details class="item-card"'), 0)             # no card inside the tree
            self.assertNotIn("levels exist", page)
            self.assertNotIn("Rank the flat things by score.", page)       # the unclaimed job is never expanded
            self.assertNotIn("<summary>Details</summary>", q1)             # plain text, no Details
            # Story Runs: the judgment run joined by its target, named in full
            self.assertIn('data-name="run-paper-claim-0901-beyond-rating"', page)
            self.assertRegex(page, r'data-run="run-paper-claim-0901-beyond-rating" data-name="run-paper-claim-0901-beyond-rating" data-targets="[^"]*\bE1\b[^"]*"')
            self.assertRegex(page, r'data-run="run-paper-claim-0901-beyond-rating" data-name="run-paper-claim-0901-beyond-rating" data-targets="[^"]*\bRQ1\b')
            self.assertIn('data-label="Task runs"', page)
            self.assertIn('data-skills="haipipe-task"', page)                # each run type names its skill (JL 260928)
            self.assertIn('data-label="Discovery runs"', page)
            self.assertIn('data-run="b01.j01.t01.r01"', page)                 # a cited Task run, keyed to the rows covering it
            # Sections: one row per C8 row in compile order; a row opens its Page workbench
            self.assertIn('<div class="sec-row" data-key="S-DESK-Main-1-Introduction"', page)
            self.assertIn("/_board/draft?path=%2Fpapers%2FPaper-Test%2Fboard.md&amp;file=Ba-DESK-Main%2FS-DESK-Main-1-Introduction%2FS-DESK-Main-1-Introduction.md&amp;lens=div", page)
            self.assertIn('data-key="S-DESK-Main-2-Results"', page)
            self.assertIn("not set up", page)
            self.assertIn("Why now?", page)                                  # the C8 row's reader question
            self.assertIn("paper-desk-introduction", page)                   # its Codex session
            self.assertIn('id="hero-E01-DISPLAY-hero-figure" data-key="S-DESK-Main-1-Introduction:E01" data-part="main"', page)
            self.assertNotIn('id="hero-E02-CITE-prior"', page)         # not hero: a CITE
            self.assertIn('data-run="run-structure-0901-outline" data-name="run-structure-0901-outline"', page)   # the Section's own runs
            self.assertIn('data-run="re-display-01_hero"', page)
            # Delivery: formats, views, checks, rounds
            self.assertIn('data-src="/papers/Paper-Test/delivery/latex/Paper-Test-draft.pdf"', page)
            self.assertIn("⬜ not built", page)                              # the supplement named but absent
            self.assertIn("delivery/word-feedback/Paper-Test-coauthor.docx", page)
            self.assertIn("1200 words", page)
            self.assertIn("1 of 2 · not ready: S-DESK-Main-2-Results", page)
            self.assertIn("fragment may be stale", page)
            self.assertIn("fig:hero", page)
            self.assertIn("bib key smith2020 differs between two pages", page)
            self.assertIn("citations resolved", page)
            self.assertIn('data-name="run-compile-260909"', page)            # the last build, as a run
            self.assertIn("No round yet.", page)
            self.assertIn('data-tab="rounds" data-label="Rounds" data-noviews', page)

if __name__ == "__main__":
    unittest.main()
