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
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent  # the engine dir
sys.path.insert(0, str(HERE))
from live.paper import collect, paper_run_types, render_paper, section_rows, session_rows, task_home  # noqa: E402

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
    (b / "Ba-DESK-Main" / "S-DESK-Main-1-Introduction" / "results" / "rp-struct-01").mkdir(parents=True)
    (b / "board.md").write_text(BOARD, encoding="utf-8")
    s00 = b / "A1-Story" / "Story00-ideation"
    (s00 / "Story00-ideation.md").write_text("# Story00\nstate: 🔴 OPEN\n\n## Opening\nq\n\n## Aims\n- ⬜ A1.1\n", encoding="utf-8")
    (s00 / "outline" / "Story00-ideation-outline-v0.1.md").write_text(PLAN, encoding="utf-8")
    (s00 / "outline" / "Story00-ideation-evidence-items.md").write_text(ITEMS, encoding="utf-8")
    (b / "A1-Story" / "StoryA-desk-idea" / "StoryA-desk-idea.md").write_text(STORY, encoding="utf-8")
    sec = b / "Ba-DESK-Main" / "S-DESK-Main-1-Introduction"
    (sec / "S-DESK-Main-1-Introduction.md").write_text("# S-DESK-Main-1-Introduction · §1 Introduction\nstate: DRAFT\n", encoding="utf-8")
    (sec / "runs" / "rp-struct-01.md").write_text("ticket", encoding="utf-8")
    (sec / "runs" / "rp-para-02_P01.md").write_text("ticket", encoding="utf-8")
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
        "- **Local Run**: Page · Evidence Item · reuse · re-value-09_old → results/re-value-09_old/result.yaml\n", encoding="utf-8")
    # a judgment Run on the Story: rclaim ticket + runtime, target E1
    st = b / "A1-Story" / "StoryA-desk-idea"
    (st / "runs").mkdir(); (st / "results" / "rclaim-01_beyond-rating").mkdir(parents=True)
    (st / "runs" / "rclaim-01_beyond-rating.md").write_text("---\nfamily: paper\ntarget: E1\nrun: rclaim-01_beyond-rating\n---\n", encoding="utf-8")
    (st / "results" / "rclaim-01_beyond-rating" / "runtime.yaml").write_text("status: waiting-for-feedback\nstep: s002\n", encoding="utf-8")
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
            self.assertEqual(gates["G3"], "1 of 2 C8 rows have a Section page")
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

    def test_the_roadmap_is_a_tree_of_general_questions(self):
        """JL 260928: a general question → its T and D rows → their BJTR folders."""
        from live.paper import _addresses, _question_cards
        self.assertEqual(_addresses("b03.j02.t01–t03 · b03.j02.t05"),
                         ["b03j02t01", "b03j02t02", "b03j02t03", "b03j02t05"])   # a range names each task
        with tempfile.TemporaryDirectory() as tmp:
            b = make_board(Path(tmp))
            story = b / "A1-Story" / "StoryA-desk-idea" / "StoryA-desk-idea.md"
            text = story.read_text(encoding="utf-8")
            text = text.replace("| D | what the paper must learn | scope | feeds |\n|---|---|---|---|",
                                "| Q | general question | serves |\n|---|---|---|\n| Q1 | Is there an effect? | RQ1 |\n\n"
                                "| D | what the paper must learn | scope | feeds | Q |\n|---|---|---|---|---|")
            text = text.replace("| RQ1 |\n| D2 |", "| RQ1 | Q1 |\n| D2 |")
            text = text.replace("| T | evidence obligation | design | feeds |\n|---|---|---|---|",
                                "| T | evidence obligation | design | feeds | Q |\n|---|---|---|---|---|")
            text = text.replace("| RQ1 · b01.j01.t01 |", "| RQ1 · b01.j01.t01 | Q1 |")
            story.write_text(text, encoding="utf-8")
            d = collect(b, "/papers/Paper-Test/board.md")
            d["root"] = Path(tmp).resolve()                             # as render_paper sets it
            cards, loose = _question_cards(d, d["story"][0])
            self.assertEqual(len(cards), 1)
            self.assertIn('id="q-Q1" data-key="Q1"', cards[0])
            self.assertIn('id="task-T1"', cards[0]); self.assertIn('id="need-D1"', cards[0])
            self.assertIn("2 of 2 with a folder", cards[0])
            self.assertTrue(any('id="task-T2"' in c for c in loose))    # a row with no Q comes last
            self.assertTrue(any('id="need-D2"' in c for c in loose))

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
                         ["Story revise", "Claim review", "Task review", "Task runs", "Discovery runs"])
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
            self.assertEqual(rows[1]["state"], "not set up")               # a C8 row with no Section Page yet
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
            # Story › Questions: the RQ is the card; its claim is nested inside it
            self.assertIn('id="rq-RQ1" data-key="RQ1"', page)
            self.assertIn('id="claim-E1" data-key="E1"', page)
            self.assertLess(page.index('id="rq-RQ1"'), page.index('id="claim-E1"'))
            self.assertIn("It holds beyond the rating", page)
            self.assertIn("Does it hold?", page)
            # Story › Roadmap: each C7 / C6 question with the folder that answers it (JL 260928)
            self.assertIn('id="task-T1" data-key="T1"', page)
            # JL 260929: an opened question shows its B → J → T folders first: the block and each job
            # are borderless folds, open, that a person can close; no cards inside cards
            t1 = page[page.index('id="task-T1"'):page.index('id="task-T2"')]
            self.assertIn('<details class="bjt-b" open><summary>', t1)
            self.assertIn('<details class="bjt-j" open><summary>', t1)
            self.assertIn('<table class="grid bjt-t">', t1)
            self.assertEqual(t1.count('<details class="item-card"'), 1)    # the question card only
            self.assertIn('<details class="row-details"><summary>Details</summary>', page)
            self.assertIn('id="task-T2"', page)
            self.assertIn("No folder yet.", page)                           # said once, in the card
            self.assertNotIn("levels exist", page)                          # JL 260929: no header state
            self.assertIn('id="need-D1" data-key="D1"', page)
            self.assertIn('<details class="bjt-b" open><summary><span class="bjt-chev">›</span><span class="item-kind">b01</span>', page)
            self.assertIn("not this paper's: j02_flat", page)
            self.assertNotIn("Rank the flat things by score.", page)       # the unclaimed job is named, never expanded
            self.assertIn("the joined cohort table", page)                 # develops: typed on the page
            self.assertIn("1 tk · done 1", page)                           # receipt folded to done
            self.assertIn('id="disc-b01j01"', page)
            self.assertIn("Does prior work already link the trait to prescribing?", page)
            self.assertIn("supports · medium", page)
            self.assertIn("discoveries%2Fb01_evidence_board%2Fboard.md", page)   # link into the Discovery Board
            # Story Runs: the judgment run joined by its target, named in full
            self.assertIn('data-name="run-claim-01"', page)
            self.assertRegex(page, r'data-run="rclaim-01_beyond-rating" data-name="run-claim-01" data-targets="[^"]*\bE1\b[^"]*"')
            self.assertRegex(page, r'data-run="rclaim-01_beyond-rating" data-name="run-claim-01" data-targets="[^"]*\bRQ1\b')
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
            self.assertIn('data-run="rp-struct-01" data-name="run-structure-01"', page)   # the Section's own runs
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
