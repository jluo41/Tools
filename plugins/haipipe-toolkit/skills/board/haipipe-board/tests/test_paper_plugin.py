#!/usr/bin/env python3
"""📄 Paper Plugin: live, storage-less, one paper Board → five Spaces.

The teeth: no per-paper file is needed (the old console/ folder must not be
read), a P0 board with a plan but no Content still lists its ideas, one Codex
session row per Section Page and none for Ideation/Story, gates come from
named files, and the Workflow map is projected from the skill's ref table.
"""
import sys
import json
import shutil
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent  # the engine dir
sys.path.insert(0, str(HERE))
from live.paper import collect, render_paper, session_rows, task_home  # noqa: E402

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


class PaperPluginTest(unittest.TestCase):
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
            # Run: tickets joined to results by stem
            runs = {r["run"]: r for r in d["runs"]}
            self.assertEqual(runs["rp-struct-01"]["result"], "Run + Result")
            self.assertEqual(runs["rp-para-02_P01"]["result"], "Run exists · Result missing")
            self.assertEqual(runs["rp-para-02_P01"]["kind"], "Page Writing · paragraph")
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
                "### 3 · Idea 1: Traits and prescribing\n\n**Method**\n\nLink reviews to claims.\n\n"
                "**Hypothesis**\n\nAgreeableness predicts prescribing beyond the rating.\n\n"
                "**Core Claims**\n\n- Beyond-rating signal · MEDIUM\n- Discretion boundary · MEDIUM\n\n"
                "**Risk**\n\nReputation, not disposition.\n", encoding="utf-8")
            d = collect(b, "/papers/Paper-Test/board.md")
            idea = d["ideation"]["ideas"][0]
            self.assertEqual(idea["id"], "i1")
            self.assertEqual([k for k, _ in idea["substance"]], ["Method", "Hypothesis", "Core Claims", "Risk"])
            page = render_paper(b, root, "/papers/Paper-Test/board.md")
            self.assertIn("Agreeableness predicts prescribing beyond the rating.", page)
            self.assertIn("<li>Beyond-rating signal · MEDIUM</li>", page)
            # the idea comes before the comparison metadata inside the card
            self.assertLess(page.index("Link reviews to claims."), page.index("closest work archived"))
            self.assertIn('<span class="item-title">Agreeableness predicts prescribing beyond the rating.</span>', page)

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
            self.assertIn("no delivery/ yet · G4 open", page)
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
            self.assertEqual((none["state"], none["all"]), ("no address yet", []))        # a row id like T2 is not an address

    def test_render_needs_no_console_and_links_back_to_outline(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            b = make_board(root)
            page = render_paper(b, root, "/papers/Paper-Test/board.md")
            self.assertNotIn("GHOST", page)
            self.assertNotIn("console/index.html", page)                    # the ghost console/ is a folder on disk, never a plugin store
            self.assertIn("📁 console/", page)                               # so the real folder tree shows it, marked not in the map
            self.assertIn("not in the map", page)
            self.assertIn(" page(s)</span>", page)
            self.assertIn("backend Markdown:", page)
            self.assertEqual(page.count("backend Markdown<span"), 5)         # one footer per Space, naming its files
            self.assertIn("papers/Paper-Test/A1-Story/Story00-ideation/Story00-ideation.md", page)
            self.assertIn("papers/Paper-Test/delivery/build-manifest.json", page)
            for chip in ("Setup Space", "Ideation Space", "Story Space", "Run Space"):
                self.assertIn(chip, page)
            self.assertIn("/_board/outline?path=%2Fpapers%2FPaper-Test%2Fboard.md&amp;file=A1-Story%2FStory00-ideation%2FStory00-ideation.md&amp;lens=div", page)
            self.assertIn("&amp;lens=run&amp;run=rp-struct-01", page)
            self.assertNotIn("lens=div&amp;lens=run", page)
            self.assertIn("paper-desk-introduction", page)
            # Idea Cards: collapsed <details>, like Outline's Evidence cards
            self.assertEqual(page.count('<details class="item-card" id="idea-'), 2)
            self.assertNotIn('<details class="item-card" id="idea-i01" open', page)
            self.assertIn('<span class="item-label">First idea</span>', page)
            self.assertIn("Freeze a denominator", page)          # bullet head in the detail
            self.assertIn("closest prior work", page)            # bound evidence item
            self.assertIn('id="idea-i02"', page)
            # Story Space card lists
            self.assertIn('id="claim-E1"', page)
            self.assertIn("It holds beyond the rating", page)
            self.assertIn("Does it hold?", page)                       # RQ joined into the claim card
            self.assertIn("rclaim-01_beyond-rating", page)              # judgment Run joined by target
            self.assertIn("waiting-for-feedback · s002", page)
            self.assertIn('id="task-T1"', page)
            self.assertIn("b01 ✓", page); self.assertIn("j01 ✓", page); self.assertIn("t01 ✓", page)
            self.assertIn('id="task-T2"', page)
            self.assertIn("no address yet", page)
            # Task home tree: one card per block, both Task shapes read off the folder
            self.assertIn('id="block-b01"', page)
            self.assertIn("b01_block", page)
            self.assertIn("1 job(s) · 1 task(s) · 1 ticket(s) · 1 job(s) not claimed", page)   # T1's b01.j01.t01 claims j01 only
            self.assertIn("not this paper's: j02_flat", page)
            self.assertNotIn("Rank the flat things by score.", page)       # the unclaimed job is named, never expanded
            self.assertIn("the joined cohort table", page)                 # develops: typed on the page
            self.assertIn("1 tk · done 1", page)                           # receipt folded to done
            self.assertIn("C7 addresses b01j01t01", page)
            # Discovery needs join the Discovery home by address; D2 names none
            self.assertIn('id="disc-b01j01"', page)
            self.assertIn("j01_landscape_inquiry", page)
            self.assertIn("Does prior work already link the trait to prescribing?", page)
            self.assertIn("supports · medium", page)
            self.assertIn("no address yet", page)
            self.assertIn("t01_prior_work", page)
            self.assertIn("discoveries%2Fb01_evidence_board%2Fboard.md", page)   # Outline link into the Discovery Board
            self.assertIn('id="section-S-DESK-Main-2-Results"', page)
            self.assertIn("no rnarra Run yet", page)
            self.assertIn('id="hero-E01-DISPLAY-hero-figure"', page)   # hero: a Main-page DISPLAY
            self.assertNotIn('id="hero-E02-CITE-prior"', page)         # not hero: a CITE
            self.assertIn("Claims &amp; Hypothesis", page)
            # Spine carries the Story's Identity face, its subsection, and the Pitch
            self.assertIn("<b>Working Title</b><span>Traits and Prescribing</span>", page)
            self.assertIn("tests whether a text-inferred trait predicts prescribing beyond the rating", page)
            self.assertIn("This paper tests whether a review-inferred trait predicts prescribing.", page)
            self.assertIn("Review text may carry a signal the star rating does not show.", page)
            self.assertIn("Task Roadmap", page)
            self.assertIn("Workflow map", page)
            # the map joined to the folder tree: each Run-Type names its folder on THIS board, each slot resolves
            self.assertIn("Folder tree × Run-Type", page)
            self.assertIn("folder on this board", page)
            self.assertIn("A1-Story/StoryA-desk-idea/", page)                 # the story slot resolved
            self.assertIn("Ba-DESK-Main/", page)
            self.assertIn("Bb-DESK-Appendix/", page)                          # pattern shown as missing
            self.assertIn("the project homes · Task home · Discovery home", page)   # the homes box, outside the paper folder
            self.assertIn("the Task home · 1 block(s)", page)                 # the real tree: the claimed block and its jobs
            self.assertIn("📁 b01_block/", page)
            self.assertIn("📁 j01_job/", page)
            self.assertIn("📁 StoryA-desk-idea/", page)
            self.assertIn('<ul class="tree">', page)                           # a real nested tree, not a table
            self.assertIn('<span class="idtag rt">paper.story.shape</span>', page)
            self.assertIn('<span class="tn-note">outline/ ', page)             # a page folder's row: its counts, the page named once (by the folder)
            # the tree is complete and bare: every folder opens to its files; no holds text, no explanation table
            self.assertIn("📁 runs/", page)
            self.assertIn("r01_first.sh", page)
            self.assertIn("📁 r01_first/", page)
            self.assertIn("runtime.yaml", page)
            self.assertNotIn('class="tn-holds"', page)
            self.assertNotIn("tn-explain", page)
            # copy to chat: every card and Spine division cites the Markdown it was read from; nothing is written
            self.assertIn('data-board="papers/Paper-Test/board.md"', page)
            self.assertIn('data-src="papers/Paper-Test/A1-Story/StoryA-desk-idea/StoryA-desk-idea.md" data-ref="C5 · E1"', page)
            self.assertIn('data-ref="C7 · T1"', page)
            self.assertIn('data-ref="C1 · Identity"', page)
            self.assertIn('data-src="tasks/b01_block" data-ref="b01"', page)
            self.assertIn("copy to chat", page)
            self.assertNotIn("fetch(", page)                                   # the page makes no request of its own
            # Run Space: three run types, Supporting Runs as a Block › Job › Task › Run tree
            self.assertLess(page.index('data-space="run">Run Space'), page.index('data-space="delivery">Delivery Space'))
            self.assertIn('id="pruns-S-DESK-Main-1-Introduction"', page)       # Page Runs: rp-struct-01 + rp-para-02_P01
            self.assertIn("1 of 2 with a Result", page)
            self.assertIn('id="eruns-S-DESK-Main-1-Introduction"', page)       # Evidence Runs: E01 joined to its Local Run
            self.assertIn("re-display-01_hero", page)
            self.assertIn("complete · s003", page)
            self.assertIn("1 of 2 item(s) have a Local Run", page)             # E02 names none, and must not
            self.assertIn("OldNum <span class=\"mut\">· retired</span>", page)   # inherit the retired #### block under it
            self.assertIn("1 retired item(s)", page)
            self.assertIn('id="sup-exec-b01"', page)                           # Supporting: Execution tree
            self.assertIn("r01_first", page)                                   # the ticket the address resolves to
            self.assertIn("✗ no r09 ticket on disk", page)                     # cited, not on disk
            self.assertIn('id="sup-disc-b01"', page)                           # Supporting: Discovery tree
            self.assertIn("r01_smith2020", page)
            self.assertIn("HeroFig", page)                                     # used by: the item's Label
            # Delivery Space: manuscript, compile order, displays, checks, rounds
            self.assertIn('data-space="delivery"', page)
            self.assertIn("Delivery Space", page)
            self.assertIn("Traits and Prescribing", page)                   # paper-build.toml title
            self.assertIn("venue Test Quarterly", page)
            self.assertIn("DRAFT · built 2026-09-09T10:49:47", page)
            self.assertIn("delivery/latex/Paper-Test-draft.pdf", page)
            self.assertIn("⬜ not built", page)                              # the supplement named but absent
            self.assertIn("delivery/word-feedback/Paper-Test-coauthor.docx", page)
            self.assertIn("1200 words · no declared limit", page)
            self.assertIn("1 of 2 ready · not ready: S-DESK-Main-2-Results", page)
            self.assertIn("S-DESK-Main-2-Results ✗ not minted", page)       # in the compile order, no page yet
            self.assertIn("delivery/build.py", page)
            self.assertIn("v1.0 ✅ JL 260906", page)                        # outline version + approval on the page row
            self.assertIn("fragment may be stale", page)
            self.assertIn("fig:hero", page)
            self.assertIn("bib key smith2020 differs between two pages", page)
            self.assertIn("citations resolved", page)
            self.assertIn("no Round yet", page)
            self.assertIn("no venue-page Links row", page)
            # Setup speaks the paper's own names: the desk is DESK, delivery/ is not a setup row
            self.assertIn("Ba-DESK-Main/", page)
            self.assertIn("Bb-DESK-Appendix/", page)
            self.assertIn("Bc-DESK-Round/", page)
            self.assertNotIn("B?-", page)
            setup_panel = page[page.index('data-space="setup"'):page.index('data-space="ideation"')]
            self.assertNotIn("Ba-&lt;desk&gt;", setup_panel)              # Setup names the desk; the Folder tree shows the pattern beside the real name
            self.assertNotIn("<td><span class=\"path\">delivery/</span></td>", page)
            # the Outline type scale, not the old console's
            self.assertIn("h1{font-size:17px", page)
            self.assertNotIn("font-size:29px", page)


if __name__ == "__main__":
    unittest.main()
