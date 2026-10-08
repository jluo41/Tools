"""The Board-level Design workbench: the Brief's design tasks × folders × items, one grain up from the Page."""

import re
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from live.design import brief_rows, design_snapshot
from live import designboard
from live.designboard import (
    render_theory_embed,
    add_tasks,
    bundle_csv,
    bundle_rows,
    design_board_snapshot,
    design_boards,
    is_design_board,
    new_folder,
    papers_page,
    render_design_board,
    resolve_board,
)
from fixture_design_v2 import build_design_folder, build_insight_board, demo_specs

BRIEF = """# Design Brief
folder-kind: brief

## Opening

Three lines; the third has no folder yet.

### 8 · What to design

| line | audience | job | venue | designs | folder |
|---|---|---|---|---|---|
| R1 | all patients | prescription review | sms | 2 | `Design-01-all-patients-prescription-review-sms` |
| R2 | patients with a refill due within 7 days | refill review | ui-card | 1 | `Design-02-patients-refill-due-refill-review-ui-card` |
| R3 | young male, age 35 or under | prescription review | sms | 1 | — |
"""


def board_fixture(root: Path) -> Path:
    build_insight_board(root / "DesignWorkbench-Demo-260916-InsightBoard")
    board = root / "DesignWorkbench-Demo-260916-DesignBoard"
    board.mkdir(parents=True)
    (board / "board.md").write_text(
        "# Design Workbench Playground\nboard-kind: design-board\nreads: DesignWorkbench-Demo-260916-InsightBoard\n"
        "spine: See the entire design programme from signed input through ready candidate.\n",
        encoding="utf-8")
    brief = board / "0-BR-brief" / "BR00-brief" / "BR00-brief.md"
    brief.parent.mkdir(parents=True)
    brief.write_text(BRIEF, encoding="utf-8")
    for stem, spec in demo_specs().items():
        build_design_folder(board / "2-Design" / stem, stem, spec["title"], spec["opening"], spec["specs"])
    return board


class BriefTest(unittest.TestCase):
    def test_brief_lines_are_matched_by_header_word(self):
        rows = brief_rows(BRIEF)
        self.assertEqual([r["id"] for r in rows], ["R1", "R2", "R3"])
        self.assertEqual(rows[0]["folder"], "Design-01-all-patients-prescription-review-sms")
        self.assertEqual(rows[0]["designs"], 2)
        self.assertEqual(rows[0]["insight"], "")            # no column: the board's reads: applies
        self.assertEqual(rows[2]["folder"], "")
        self.assertEqual(rows[2]["venue"], "sms")
        self.assertEqual(brief_rows("# Brief\n\nno table here\n"), [])
        with_insight = BRIEF.replace("| designs | folder |", "| designs | insight | folder |") \
            .replace("|---|---|---|---|---|---|", "|---|---|---|---|---|---|---|") \
            .replace("| 2 | `Design-01", "| 2 | `Other-InsightBoard` | `Design-01") \
            .replace("| 1 | `Design-02", "| 1 |  | `Design-02").replace("| 1 | — |", "| 1 |  | — |")
        rows = brief_rows(with_insight)
        self.assertEqual(rows[0]["insight"], "Other-InsightBoard")
        self.assertEqual(rows[1]["insight"], "")


class DesignBoardSnapshotTest(unittest.TestCase):
    def test_identity_and_resolution(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            self.assertTrue(is_design_board(board))
            self.assertFalse(is_design_board(board.parent / "DesignWorkbench-Demo-260916-InsightBoard"))
            self.assertEqual(design_boards(Path(td)), [board])
            self.assertEqual(resolve_board(Path(td), "/DesignWorkbench-Demo-260916-DesignBoard/board.md").resolve(),
                             board.resolve())
            self.assertEqual(resolve_board(Path(td), "DesignWorkbench-Demo-260916-DesignBoard").resolve(), board.resolve())
            self.assertIsNone(resolve_board(Path(td), "/../etc/board.md"))
            # a bare link opens the only DesignBoard: the one under the root, or the root itself
            self.assertEqual(resolve_board(Path(td), "").resolve(), board.resolve())
            self.assertEqual(resolve_board(board, "").resolve(), board.resolve())

    def test_a_board_in_one_project_reads_an_insight_board_in_another(self):
        with TemporaryDirectory() as td:
            build_insight_board(Path(td) / "ProjB" / "applications" / "DesignWorkbench-Demo-260916-InsightBoard")
            project = Path(td) / "ProjA"
            board = project / "applications" / "UI-DesignBoard"
            board.mkdir(parents=True)
            (board / "board.md").write_text(
                "# UI DesignBoard\nboard-kind: design-board\n"
                "reads: ../../ProjB/applications/DesignWorkbench-Demo-260916-InsightBoard\n", encoding="utf-8")
            self.assertEqual(design_boards(project), [board])        # a Project folder served as the root
            snapshot = design_board_snapshot(board, project)
            self.assertEqual(snapshot["insight"]["status"], "bound")
            self.assertEqual(resolve_board(project, "").resolve(), board.resolve())

    def test_snapshot_stacks_folders_brief_lines_items_and_queue(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            snap = design_board_snapshot(board, Path(td))
            self.assertEqual([f["name"] for f in snap["folders"]],
                             ["Design-01-all-patients-prescription-review-sms", "Design-02-patients-refill-due-refill-review-ui-card"])
            self.assertEqual([(i["folder"], i["id"], i["state"]) for i in snap["items"]],
                             [("Design-01-all-patients-prescription-review-sms", "ITEM01", "ready"),
                              ("Design-01-all-patients-prescription-review-sms", "ITEM02", "generate failed"),
                              ("Design-02-patients-refill-due-refill-review-ui-card", "ITEM01", "generated")])
            statuses = {r["id"]: r["status"] for r in snap["brief_rows"]}
            self.assertEqual(statuses["R1"], "1 ready · 1 generate failed")
            self.assertEqual(statuses["R2"], "1 generated")
            self.assertEqual(statuses["R3"], "no folder yet")
            self.assertEqual(snap["totals"], {"lines": 3, "wanted": 4, "registered": 3, "ready": 1})
            self.assertEqual(snap["unlisted"], [])
            self.assertEqual([(i["folder"], i["id"]) for i in snap["waiting"]],
                             [("Design-01-all-patients-prescription-review-sms", "ITEM02"), ("Design-02-patients-refill-due-refill-review-ui-card", "ITEM01")])
            self.assertEqual(len(snap["ready"]), 1)
            self.assertEqual(snap["runs"][0]["id"], "run-design-adopt-0918-design-1")   # newest first
            self.assertEqual(snap["audit"], [])
            self.assertEqual(snap["insight"]["status"], "bound")
            self.assertEqual(snap["insight_names"], ["DesignWorkbench-Demo-260916-InsightBoard"])
            pages = snap["insight_space"][0]["pages"]
            self.assertEqual(pages[0]["name"], "FW01-send-salience.md")
            self.assertEqual([(name, item) for name, _rel, item in pages[0]["used_by"]],
                             [("Design-01-all-patients-prescription-review-sms", "ITEM01"),
                              ("Design-01-all-patients-prescription-review-sms", "ITEM02")])
            self.assertTrue(pages[0]["finding"].startswith("Of thirteen arms"))
            self.assertEqual(snap["relative"], "DesignWorkbench-Demo-260916-DesignBoard")

    def test_render_has_five_spaces_and_links_down_to_the_page_level(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            snap = design_board_snapshot(board, Path(td))
            rendered = render_design_board(snap)
            # the header in the Insight board's style (JL 261003): links, one band of facts, Space buttons
            for label in (">Design Tasks</button>", '<nav class="tabs spaces">',
                          "<div class=dataset>", " design tasks · ",
                          # one View per method family (JL 261003), and each task's method
                          '<button type=button data-view="all" class=on>All</button>', ">Goal Only</button>",
                          ">Internal Insights</button>", "<h2>Design tasks · Goal Only</h2>",   # the All table per family
                          "not designed this way yet", "Its methods: By goal · By principle", "<th>method</th>", "not declared",
                          "<h2>Design tasks</h2>", "<th>design task</th>",
                          "Prescription review SMS for young male, age 35 or under",
                          "no folder yet", "New Design Folder", "class=runs-panel", 'data-label="Add design tasks"',
                          "/_board/design?path=%2FDesignWorkbench-Demo-260916-DesignBoard%2Fboard.md&amp;file=2-Design%2FDesign-01-all-patients-prescription-review-sms%2FDesign-01-all-patients-prescription-review-sms.md&amp;space=design"):
                self.assertIn(label, rendered)
            for jargon in ("roster", "Roster", "handoffs signed", "check_unit", "candidate", "DS01",
                           "<b>R3</b>", "<th>line</th>"):  # a task shows by its full name, not its row id
                self.assertNotIn(jargon, rendered)
            nav = rendered.split("<nav class=\"tabs spaces\">", 1)[1].split("</nav>", 1)[0]
            for gone in ("Goal Space", ">Design Space<", "Delivery Space"):    # the theory text may name them
                self.assertNotIn(gone, nav)
            for gone in ("<h2>Insight board</h2>", "<th>insight board</th>",
                         "Waiting on", "Every Run", "Run types in this Space", "data-act=\"add-tasks\""):
                self.assertNotIn(gone, rendered)
            head = rendered.split("<header>", 1)[1].split("</header>", 1)[0]
            for count in ("wanted · ", "waiting on you:", "registered"):    # the header carries no counts
                self.assertNotIn(count, head)
            for old in ("run", "delivery", "goal", "design"):              # an old link opens Design Tasks
                self.assertIn('data-space="tasks" class=on', render_design_board(snap, old))
            # JL 261002: the theory explains the family, so it is Guide › Methods, which frames
            # this page; the board keeps one working Space
            self.assertNotIn("Theory of Design Space", nav)
            self.assertNotIn('data-space="theory"', rendered)
            theory = render_theory_embed(snap, "design-theory")
            self.assertIn("<h1>Method</h1>", theory)                       # one Method document (JL 261003)
            only = render_theory_embed(snap, "papers", ["papers"])                 # Guide › Related Paper
            self.assertNotIn('<div class=views>', only)                              # one view, no view bar
            self.assertIn('<div class="view on" data-view="papers">', only)
            self.assertNotIn('data-view="methods"', only)
            self.assertIn("5.1 · Design makes a situation better", theory)
            self.assertIn("haipipe-explain-height", theory)                  # it tells its Guide frame its height
            static = render_design_board(design_board_snapshot(board, Path(td), static=True))
            self.assertNotIn("New Design Folder", static)
            self.assertNotIn("<pre class=theory>Deduction", static)

    def test_guide_frames_the_theory_page_and_the_ui_design(self):
        # JL 261002: Guide is Description · Method · RoadMap Draw · Related Paper. Design's
        # Method gives its six steps first, then one page: the theory, the method cards and
        # the methods drawing, with no view named Design methods (JL 261003), RoadMap Draw with one drawing of skills, method, workbench and folders, and Related
        # Paper with its papers page; an earlier View key still opens the View that holds it.
        from live.workbench_guide import guide_html
        context = {"path": "/Demo/board.md", "file": "board.md"}
        description = guide_html("design", "description", context, embedded=True)
        self.assertIn("one task done by one design method", description)
        method = guide_html("design", "method", context, embedded=True)
        self.assertNotIn("Set the Design Task", method)          # the page carries the steps (JL 261003: "merge")
        self.assertIn('class="wg-explain-frame"', method)
        self.assertIn('src="/_board/design-board?embed=theory&amp;view=method&amp;views=method'
                      '&amp;path=%2FDemo%2Fboard.md"', method)
        self.assertNotIn("Design methods", method)
        roadmap = guide_html("design", "roadmap-draw", context, embedded=True)
        self.assertLess(roadmap.index('class="wg-explain-frame"'), roadmap.index('data-drawing="roadmap-draw"'))
        self.assertIn("design-workbench-ui.excalidraw", roadmap)
        self.assertIn('referrerpolicy="no-referrer"', roadmap)
        papers = guide_html("design", "related-paper", context, embedded=True)
        self.assertIn("view=papers&amp;views=papers", papers)
        self.assertNotIn("No related papers are declared", papers)            # its own page leads, no false note

    def test_theory_subset_keeps_the_order_it_is_given(self):
        import tempfile
        from live.designboard import theory_page
        with tempfile.TemporaryDirectory() as td:
            board = Path(td) / "board.md"; board.write_text("# Demo\n", encoding="utf-8")
            html = theory_page(board, Path(td), view="methods", only=["methods", "studio", "design-theory"])
        bar = re.findall(r'<button type=button data-view="([a-z-]+)"', html.split("</div>")[0])
        self.assertEqual(bar, ["methods", "studio", "design-theory"])
        with tempfile.TemporaryDirectory() as td:
            board = Path(td) / "board.md"; board.write_text("# Demo\n", encoding="utf-8")
            one = theory_page(board, Path(td), view="method", only=["method"])        # Guide's one page
            plain = theory_page(board, Path(td))                                        # Method only when asked
        self.assertNotIn("class=views", one)
        for part in ("<details class=sec-fold><summary><strong>1 · The six steps</strong>",   # each part folds,
                     "<details class=sec-fold><summary><strong>2 · Step 2 in depth: pick the method</strong>",  # all closed at first
                     "<h3>2.2 · Which method when</h3>", "3 · Step 3 in depth: what a design records",
                     "4 · Steps 4 and 6 in depth", "<summary><strong>5 · Why it works</strong>",
                     "<details class=sec-fold><summary><strong>Reference</strong>"):
            self.assertIn(part, one)                                    # the six steps as the spine (JL 261003)
        self.assertLess(one.index("<summary><strong>Method design</strong>"), one.index("1 · The six steps"))   # the drawing card first
        self.assertNotIn('data-view="method"', plain)

    def test_theory_space_has_three_views_and_papers_read_the_workbench_table(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            snap = design_board_snapshot(board, Path(td))
            table = Path(td) / "ref" / "design-papers.md"       # the workbench's own table, here a temp one
            real, designboard.PAPERS = designboard.PAPERS, table
            self.addCleanup(setattr, designboard, "PAPERS", real)
            drawing = Path(td) / "Tools" / "ref" / "design-methods.excalidraw"   # and its methods drawing
            drawing.parent.mkdir(parents=True)
            drawing.write_text('{"type": "excalidraw", "elements": []}', encoding="utf-8")
            real_studio, designboard.STUDIO = designboard.STUDIO, drawing
            self.addCleanup(setattr, designboard, "STUDIO", real_studio)
            theory = render_theory_embed(snap, "design-theory")
            # three general views, one shown at a time (JL 261001): no channel's own theories here
            for label in ('<button type=button data-view="design-theory" class=on>Design theory</button>',
                          '<button type=button data-view="methods">Design methods</button>',
                          '<button type=button data-view="studio">Methods studio</button>',
                          '<button type=button data-view="papers">Papers</button>',
                          '<div class="view on" data-view="design-theory">', "No related paper yet"):
                self.assertIn(label, theory)
            self.assertIn("2.3 · The thirteen method cards", theory)    # JL 261003: step 2 holds the cards
            self.assertIn("3 · Step 3 in depth: what a design records", theory)   # JL 261002: each element, reasoned or intuitive
            self.assertIn("R6 · The loop in full", theory)              # JL 261002: requirements + insights → Design → Exp
            self.assertIn("<span class=when>in the Exp</span>", theory)
            self.assertIn("<span class=when>in Evaluate</span>", theory)                # JL 261002: the Revise loop
            self.assertIn("The Revise loop (inner)", theory)
            # the methods studio: the drawing in the Excalidraw canvas, loaded when shown (data-src)
            self.assertRegex(theory, r'<iframe class=st-frame title="Methods studio" referrerpolicy="no-referrer" '
                                     r'data-src="/_excalidraw/\?board=[^"]+design-methods\.excalidraw&amp;edit=1"></iframe>')
            self.assertNotIn("message theories", theory.split('data-view="papers"', 1)[0].split("<nav", 1)[0])
            table.parent.mkdir(exist_ok=True)
            table.write_text(
                "Related papers\n==============\n\n"
                "| group | role | key | paper | venue | doi | why here | pdf |\n|---|---|---|---|---|---|---|---|\n"
                "| all methods | classic | ★ | Simon 1969 · The Sciences of the Artificial | MIT Press | 10.7551/mitpress/12107.001.0001 | it satisfices | none |\n"
                "| by theory | evidence | ★ | Prestwich, Sniehotta & Whittington 2013 · Does theory influence the effectiveness of health behavior interventions? | Health Psychology | 10.1037/a0032853 | theory use not reliably linked to effect | none |\n"
                "| by theory | classic |  | Michie, van Stralen & West 2011 · The behaviour change wheel | Implementation Science | 10.1186/1748-5908-6-42 | from behaviour to intervention functions | none |\n"
                "| by exploring | classic |  | Loch, Terwiesch & Thomke 2001 · Parallel and sequential testing of design alternatives | Management Science | 10.1287/mnsc.47.5.663.10480 | parallel or serial | none |\n",
                encoding="utf-8")
            papers = render_theory_embed(snap, "papers")
            # the Paper workbench's Related Papers card: the title, then who, when and which journal
            for label in ('<div class="view on" data-view="papers">',
                          '<div class="rp-head">4 papers · 2 key · 3 classic · 0 review · 1 evidence · 1 in UTD24 journals · 0 with a PDF</div>',
                          '<div class="lw-k">By exploring<span class="lw-kn">1</span></div>',
                          '<div class="lw-k">All methods<span class="lw-kn">1</span></div>',
                          '<div class="lw-k">By theory<span class="lw-kn">2</span></div>',
                          '<div class="rp-title">The Sciences of the Artificial</div>',
                          "<span>Simon · 1969 · MIT Press</span>", "<span>Prestwich et al. · 2013 · Health Psychology</span>", "<span>Michie et al. · 2011 · Implementation Science</span>",
                          'href="https://doi.org/10.1037/a0032853"', "theory use not reliably linked to effect",
                          "4 journals and publishers", "No free full text here"):
                self.assertIn(label, papers)
            # Guide frames this page to read, not to run (JL 261002): no Runs panel, no "Add a paper"
            self.assertNotIn("class=runs-panel", papers)
            # a band shows its key papers and folds the rest; a band with none shows them all (JL 261002)
            theory_band = papers.split('<div class="lw-k">By theory', 1)[1].split('<div class="lw-k">', 1)[0]
            self.assertIn("<details class=rp-more><summary>1 more paper</summary>", theory_band)
            self.assertLess(theory_band.index("Does theory influence"), theory_band.index("rp-more"))
            self.assertNotIn("rp-more", papers.split('<div class="lw-k">By exploring', 1)[1].split("</section>", 1)[0])
            # a UTD24 journal is marked on its card (JL 261002), the others are not
            self.assertEqual(papers.count('<span class=rp-utd title="on the UTD24 journal list">UTD24</span>'), 1)

    def test_design_methods_view_shows_one_card_per_method_with_ai_beside_the_literature(self):
        # JL 261002: "make each of them a card (design method card)" and add "how this can be
        # applied to AI": the doc's index names one card file per method
        with TemporaryDirectory() as td:
            root = Path(td)
            board = root / "Proj" / "designs" / "B00_Demo"
            board.mkdir(parents=True)
            ref = root / "ref"
            (ref / "methods").mkdir(parents=True)
            doc = ref / "design-methods.md"
            doc.write_text("Design methods\n==============\n\n2 · Eight methods\n-----------------\n\n"
                           "| family | method | card |\n|---|---|---|\n"
                           "| From what is known | By theory | methods/04-by-theory.md |\n"
                           "| From trying | By exploring | methods/08-by-exploring.md |\n\n"
                           "| test | asks | when | source |\n|---|---|---|---|\n"
                           "| T1 Fidelity | does what its method claims it does | now | x |\n", encoding="utf-8")
            (ref / "methods" / "04-by-theory.md").write_text(
                "By theory\n=========\n\nfamily: From what is known: the AI reads knowledge before it designs\n"
                "move: Choose a named theory and use its technique.\ncomes from: Michie 2011, Behaviour Change Wheel\n"
                "reads: goal · named theories\nreturns: the design and its mechanism\ntest now: T1 technique present\n"
                "test in use: T4 against the control\n\n\nWhat the literature says\n------------------------\n\n"
                "rationale: Link the intervention to the behaviour [Michie 2011].\n"
                "steps: 1. Name the behaviour. 2. Choose a\n  technique.\n"
                "limitations: Theory use was not linked to effect [Prestwich 2013].\n\n\n"
                "Applied to AI\n-------------\n\nagent: The agent reads a closed list of techniques.\n"
                "risk: It names a theory it does not use (ours).\nevidence on AI: No study tests it yet (ours).\n"
                "skill: haipipe-design-by-theory (proposed)\n", encoding="utf-8")
            table = ref / "design-papers.md"
            table.write_text(
                "| group | role | key | paper | venue | doi | why here | pdf |\n|---|---|---|---|---|---|---|---|\n"
                "| by theory | classic | ★ | Michie, van Stralen & West 2011 · The behaviour change wheel | Implementation Science | 10.1186/1748-5908-6-42 | functions |  |\n"
                "| by theory | evidence | ★ | Prestwich, Sniehotta & Whittington 2013 · Does theory influence | Health Psychology | 10.1037/a0032853 | not linked |  |\n",
                encoding="utf-8")
            render = designboard.method_cards(board, root, doc, table)
            page = designboard._plain_md(doc.read_text(encoding="utf-8"), render)
            self.assertEqual(page.count("<details class=\"mcard\""), 1)                  # the card that exists
            self.assertIn('no card at <code>methods/08-by-exploring.md</code>', page)  # the one that does not
            self.assertIn("<div class=mc-fam><b>From what is known</b> <span class=mut>· the AI reads knowledge before it designs</span></div>", page)
            self.assertIn('<span class="mc-status ok">tested in 1 study</span>', page)
            self.assertIn('<div class=mc-h>What the literature says</div>', page)
            self.assertIn('<div class="mc-col ai"><div class=mc-h>Applied to AI</div>', page)
            for label in ("Rationale", "Steps", "Limitations", "The agent", "AI risk", "Evidence on AI", "Skill"):
                self.assertIn(f"<dt>{label}</dt>", page)
            self.assertIn("<div class=line>1. Name the behaviour.</div><div class=line>2. Choose a technique.</div>", page)
            # a bracketed source links to its paper card; (ours) is marked; a test code is badged
            self.assertIn('<a class="cite to-paper" href="#paper-10-1037-a0032853"', page)
            self.assertIn('<span class=ours title="this workbench\'s own judgment">(ours)</span>', page)
            self.assertIn('<span class=tcode title="T1 Fidelity: does what its method claims it does">T1</span>', page)
            self.assertIn("<code>haipipe-design-by-theory</code> <span class=mut>(proposed)</span>", page)
            self.assertIn('Behaviour Change Wheel', page)                            # comes from: link and idea
            self.assertIn('<table class=mdt>', page)                                  # other tables stay tables
            # a method to add later is marked so, dashed (JL 261002: co-design "can be one thing so we can add in the future")
            (ref / "methods" / "10-by-co-design.md").write_text(
                "By co-design\n============\n\nfamily: From trying\nmove: Design with the people it is for.\n"
                "status: future: a method to add later\nreads: goal · the people it is for\n", encoding="utf-8")
            doc.write_text(doc.read_text(encoding="utf-8").replace(
                "| From trying | By exploring | methods/08-by-exploring.md |",
                "| From trying | By co-design | methods/10-by-co-design.md |"), encoding="utf-8")
            later = designboard._plain_md(doc.read_text(encoding="utf-8"), designboard.method_cards(board, root, doc, table))
            self.assertIn('<details class="mcard future" id="method-by-co-design">', later)
            self.assertIn('<span class="mc-status future" title="future: a method to add later">future · not run yet</span>', later)
            # JL 261002: a design reads design requirements, internal insights and external insights;
            # each input is coloured by its kind, the card says how it reasons, and the test in use is the Exp
            (ref / "methods" / "10-by-co-design.md").write_text(
                "By co-design\n============\n\nfamily: Making internal insights now: induction in small loops\n"
                "reasoning: induction from people's choices\nmove: Design with the people it is for.\n"
                "reads: design requirements · internal insights: signed rows · external insights: theory · the people it is for\n"
                "test in use: T4 against the control\n", encoding="utf-8")
            inputs = designboard._plain_md(doc.read_text(encoding="utf-8"),
                                           designboard.method_cards(board, root, doc, table, in_use="in the Exp"))
            for chip in ('<span class="chip in-req">design requirements</span>', '<span class="chip in-int">internal insights: signed rows</span>',
                         '<span class="chip in-ext">external insights: theory</span>', '<span class=chip>the people it is for</span>'):
                self.assertIn(chip, inputs)
            self.assertIn("<div class=mc-from><span class=lbl>reasoning</span>induction from people&#x27;s choices</div>", inputs)
            self.assertIn("<span class=when>in the Exp</span>", inputs)
            self.assertIn("<span class=when>in use</span>", later)                    # other boards keep their word
            self.assertIn("<span class=when>now</span>", later)

    def test_a_paper_card_shows_its_pdf_from_the_workbench_or_its_paper_run(self):
        # JL 261002: "find these papers' PDF files and embed them", "put them in the Tools of
        # the workbench of the design": a row's `pdf` names its copy beside the table; without
        # one, a Paper Run in the board's Project that holds the same DOI lends its own copy
        with TemporaryDirectory() as td:
            root = Path(td)
            board = root / "Proj" / "designs" / "B00_Demo"
            board.mkdir(parents=True)
            ref = root / "Tools" / "ref"
            (ref / "papers").mkdir(parents=True)
            (ref / "papers" / "dow2010_parallel.pdf").write_bytes(b"%PDF-1.4\n")
            table = ref / "design-papers.md"
            table.write_text(
                "| group | role | key | paper | venue | doi | why here | pdf |\n|---|---|---|---|---|---|---|---|\n"
                "| by exploring | evidence | ★ | Dow, Glassco & Kass 2010 · Parallel prototyping | ACM TOCHI | 10.1145/1879831.1879836 | parallel beats serial | papers/dow2010_parallel.pdf |\n"
                "| by exploring | evidence |  | Doshi & Hauser 2024 · Generative AI and creativity | Science Advances | 10.1126/sciadv.adn5290 | AI ideas converge |  |\n"
                "| by exploring | evidence |  | Loch & Terwiesch 2001 · Parallel and sequential testing | Management Science | 10.1287/mnsc.47.5.663.10480 | parallel or serial |  |\n"
                "| tests | classic | ★ | Sobek, Ward & Liker 1999 · Set-based concurrent engineering | Sloan Management Review |  | keep options alive |  |\n",
                encoding="utf-8")
            task = root / "Proj" / "discoveries" / "b01_x" / "j01_y" / "t01_z"
            for run, doi, pdf in (("r01_doshi2024_creativity", "10.1126/sciadv.adn5290", True),
                                  ("r02_loch2001_testing", "10.1287/mnsc.47.5.663.10480", False)):
                res = task / "results" / run
                res.mkdir(parents=True)
                (res / "runtime.yaml").write_text(f'run: {run}\nsubject:\n  kind: paper\n  doi: "{doi}"\n', encoding="utf-8")
                (res / f"{run}.md").write_text("# card\n", encoding="utf-8")
                (res / "abstract.md").write_text("# Retrieved abstract\n\nSource: x\n\nIdeas from an LLM made stories alike.\n",
                                                 encoding="utf-8")
                if pdf:
                    (res / "paper.pdf").write_bytes(b"%PDF-1.4\n")
            page = papers_page(board, root, table)
            self.assertIn("4 papers · 2 key · 1 classic · 0 review · 3 evidence · 1 in UTD24 journals · 2 with a PDF", page)
            kept = "/Tools/ref/papers/dow2010_parallel.pdf"
            lent = "/Proj/discoveries/b01_x/j01_y/t01_z/results/r01_doshi2024_creativity/paper.pdf"
            # each PDF loads only when its card opens (data-pdf, not src), and opens in a tab too
            for url, title in ((kept, "Parallel prototyping"), (lent, "Generative AI and creativity")):
                self.assertIn(f'<iframe class="rp-frame" title="PDF · {title}" data-pdf="{url}"></iframe>', page)
                self.assertIn(f'<a href="{url}" target="_blank" rel="noopener">Open the PDF in a new tab ↗</a>', page)
            # a card with its PDF says so in words, and the view can show only those
            self.assertEqual(page.count('<span class=rp-pdf title="the PDF opens inside this card">PDF</span>'), 2)
            self.assertEqual(page.count('<details class="rp-card has-pdf" id='), 2)
            self.assertIn("Show only the 2 papers with a PDF", page)
            self.assertIn('<section class="rp-band has-pdf">', page)
            self.assertIn('<section class="rp-band">', page)                     # Tests has no PDF
            self.assertIn("<summary>Abstract</summary><p>Ideas from an LLM made stories alike.</p>", page)
            self.assertIn('r02_loch2001_testing.md" target="_blank" rel="noopener">Paper Run ↗</a>', page)
            self.assertIn("No free full text here", page)                        # a Run without a free copy
            self.assertIn("A book or report with no DOI", page)                  # no DOI, no Run


class DesignBoardWritesTest(unittest.TestCase):
    def test_new_folder_opens_a_current_folder_and_names_it_on_the_brief(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            out = new_folder(board, "R3")
            self.assertEqual(out["folder"], "Design-03-young-male-age-prescription-review-sms")
            self.assertTrue(out["brief_updated"])
            page = board / "2-Design" / out["folder"] / f'{out["folder"]}.md'
            self.assertIn("folder-kind: design", page.read_text(encoding="utf-8"))
            text = page.read_text(encoding="utf-8")
            # the board checker's page contract holds from the first write (audit H8)
            self.assertIn("Which prescription review SMS design should we make for young male, age 35 or under?", text)
            self.assertRegex(text, r"(?m)^state: 🔴 OPEN · ")
            self.assertRegex(text, r"(?m)^owner: \S")
            self.assertTrue((page.parent / "draft" / f'{out["folder"]}-design-items.md').is_file())
            # Sparse native Boards still gain the promised presentation entry.
            board_text = (board / "board.md").read_text(encoding="utf-8")
            self.assertIn("## Pages\n" + page.relative_to(board).as_posix(), board_text)
            snap = design_board_snapshot(board, Path(td))
            r3 = next(r for r in snap["brief_rows"] if r["id"] == "R3")
            self.assertEqual(r3["folder"], out["folder"])
            self.assertEqual(r3["status"], "no Design Item yet")
            with self.assertRaises(ValueError):
                new_folder(board, "R3")          # already has a folder
            with self.assertRaises(ValueError):
                new_folder(board, "R9")          # not in the Brief

    def test_new_folder_registers_under_design_group_and_preserves_other_sections(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            board_md = board / "board.md"
            suffix = "\n## Pages\n### Brief\nExisting brief\n### Design\nExisting design\n\n## Links\nKeep these links.\n"
            board_md.write_text(board_md.read_text(encoding="utf-8") + suffix, encoding="utf-8")
            before = board_md.read_text(encoding="utf-8")
            out = new_folder(board, "R3")
            rel = f'2-Design/{out["folder"]}/{out["folder"]}.md'
            after = board_md.read_text(encoding="utf-8")
            self.assertEqual(after, before.replace("Existing design\n", f"Existing design\n{rel}\n"))
            with self.assertRaises(ValueError):
                new_folder(board, "R3")
            self.assertEqual(board_md.read_text(encoding="utf-8"), after)

    def test_new_folder_without_a_line_column_is_opened_once(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            brief = board / "0-BR-brief" / "BR00-brief" / "BR00-brief.md"
            lines = []
            for line in brief.read_text(encoding="utf-8").splitlines():
                if line.startswith("|"):
                    line = "|" + "|".join(line.strip("|").split("|")[1:]) + "|"   # drop the line column
                lines.append(line)
            brief.write_text("\n".join(lines) + "\n", encoding="utf-8")
            snap = design_board_snapshot(board, Path(td))
            open_row = next(r for r in snap["brief_rows"] if not r["folder"])
            out = new_folder(board, open_row["id"])
            self.assertTrue(out["brief_updated"])
            with self.assertRaises(ValueError):
                new_folder(board, open_row["id"])            # a second click opens nothing (audit L9)
            self.assertEqual(len(list((board / "2-Design").glob("Design-*"))), 3)

    def test_add_tasks_writes_lines_opens_folders_and_names_the_insight_board(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            out = add_tasks(board, ["young male, age 35 or under", "female, age 36 to 50", ""],
                            "prescription review", "sms", 10, "DesignWorkbench-Demo-260916-InsightBoard")
            self.assertEqual(out["lines"], ["R4", "R5"])
            self.assertEqual(out["folders"], ["Design-03-young-male-age-prescription-review-sms",
                                              "Design-04-female-age-36-prescription-review-sms"])
            brief_text = (board / "0-BR-brief" / "BR00-brief" / "BR00-brief.md").read_text(encoding="utf-8")
            self.assertIn("| insight |", brief_text)               # the column was added to the table
            rows = brief_rows(brief_text)
            self.assertEqual([r["id"] for r in rows], ["R1", "R2", "R3", "R4", "R5"])
            self.assertEqual(rows[0]["folder"], "Design-01-all-patients-prescription-review-sms")   # old lines intact
            self.assertEqual((rows[3]["audience"], rows[3]["designs"], rows[3]["insight"], rows[3]["folder"]),
                             ("young male, age 35 or under", 10, "DesignWorkbench-Demo-260916-InsightBoard",
                              "Design-03-young-male-age-prescription-review-sms"))
            snap = design_board_snapshot(board, Path(td))
            self.assertEqual(snap["totals"], {"lines": 5, "wanted": 24, "registered": 3, "ready": 1})
            # the new folder's Page level reads its own line and Insight board
            page = board / "2-Design" / out["folders"][0] / f'{out["folders"][0]}.md'
            page_snap = design_snapshot(page, Path(td))
            self.assertEqual(page_snap["goal"]["sentence"],
                             "10 prescription review SMS designs for young male, age 35 or under")
            self.assertEqual(page_snap["goal"]["insight"], "DesignWorkbench-Demo-260916-InsightBoard")
            self.assertEqual(page_snap["insight"]["status"], "bound")

    def test_add_tasks_refusals_write_nothing(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            before = (board / "0-BR-brief" / "BR00-brief" / "BR00-brief.md").read_text(encoding="utf-8")
            for args in (([""], "job", "sms", 10, ""), (["who"], "", "sms", 10, ""),
                         (["who"], "job", "", 10, ""), (["who"], "job", "sms", 0, ""),
                         (["who"], "job", "sms", 10, "No-Such-Board")):
                with self.assertRaises(ValueError):
                    add_tasks(board, *args)
            self.assertEqual((board / "0-BR-brief" / "BR00-brief" / "BR00-brief.md").read_text(encoding="utf-8"), before)
            self.assertEqual(sorted(p.name for p in (board / "2-Design").iterdir()),
                             ["Design-01-all-patients-prescription-review-sms", "Design-02-patients-refill-due-refill-review-ui-card"])

    def test_add_tasks_without_opening_folders_and_without_a_table(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            brief = board / "0-BR-brief" / "BR00-brief" / "BR00-brief.md"
            brief.write_text("# Design Brief\nfolder-kind: brief\n\n## Opening\n\nNo list yet.\n", encoding="utf-8")
            out = add_tasks(board, ["patients over 65"], "refill review", "email", 3, "", open_folders=False)
            self.assertEqual(out["lines"], ["R1"])
            self.assertEqual(out["folders"], [])
            rows = brief_rows(brief.read_text(encoding="utf-8"))
            self.assertEqual((rows[0]["id"], rows[0]["venue"], rows[0]["designs"], rows[0]["folder"]),
                             ("R1", "email", 3, ""))
            snap = design_board_snapshot(board, Path(td))
            self.assertEqual(next(r["status"] for r in snap["brief_rows"] if r["id"] == "R1"), "no folder yet")
            self.assertEqual(len(snap["unlisted"]), 2)      # the two demo folders are no longer listed


METHOD_CARD = """# M01 · Goal only

The writer sees the task and nothing from Stage 1.

## ① See input

- packet: `1-IN-inputs/IN01-goal-only/IN01-goal-only.md`

## ② Conduct process

- reasoning: freestyle, budget-limited

## ③ Check output

- grounding: only IN01
"""


def method_board_fixture(root: Path) -> Path:
    """The same board with its tasks under two method folders and no plain 2-Design/."""
    board = board_fixture(root)
    plain = board / "2-Design"
    for key, slug in (("M01", "goal-only"), ("M02", "overall-performance")):
        group = board / f"2-Design-{key}-{slug}"
        group.mkdir()
        if key == "M01":
            (group / "method.md").write_text(METHOD_CARD, encoding="utf-8")
        stem = "Design-01-all-patients-prescription-review-sms"
        spec = demo_specs()[stem]
        build_design_folder(group / stem, stem, spec["title"], spec["opening"], spec["specs"])
    import shutil
    shutil.rmtree(plain)
    return board


class MethodFoldersTest(unittest.TestCase):
    """2-Design-M<NN>-<slug>/ method folders (JL 261005): one method each, the Brief's tasks under each."""

    def test_snapshot_reads_every_method_folder(self):
        with TemporaryDirectory() as td:
            board = method_board_fixture(Path(td))
            self.assertTrue(is_design_board(board))
            snap = design_board_snapshot(board, Path(td))
            self.assertEqual([g["key"] for g in snap["methods"]], ["M01", "M02"])
            self.assertEqual(snap["methods"][0]["label"], "M01 · Goal only")
            self.assertEqual(snap["methods"][1]["label"], "M02 · overall performance")   # no card: its folder name
            r1 = snap["brief_rows"][0]
            self.assertEqual(sorted(f["method_key"] for f in r1["snapshots"]), ["M01", "M02"])
            self.assertEqual(r1["status"], "2 methods")
            self.assertEqual(snap["unlisted"], [])
            self.assertTrue(all(i["folder"].startswith(("M01 · ", "M02 · ")) for i in snap["items"]))

    def test_render_has_one_view_per_method_and_the_card(self):
        with TemporaryDirectory() as td:
            board = method_board_fixture(Path(td))
            html = render_design_board(design_board_snapshot(board, Path(td)))
            self.assertIn('data-view="m-1" class=on>M01 · Goal only</button>', html)   # the first method opens
            self.assertIn('data-view="m-2">M02 · overall performance</button>', html)
            self.assertNotIn('data-view="all"', html)                                  # no All View
            # under each method, the design unit's three steps; ② Designs opens, the card split across them
            self.assertIn('<button type=button data-step="see">① See input</button>', html)
            self.assertIn('data-step="designs" class=on>② Designs</button>', html)
            self.assertIn('<button type=button data-step="check">③ Check output</button>', html)
            self.assertIn("freestyle, budget-limited", html)                  # ② of the card
            self.assertIn("<code>1-IN-inputs/IN01-goal-only/IN01-goal-only.md</code>", html)   # ① names the packet
            self.assertIn("not on disk", html)                                # … which the fixture lacks
            self.assertIn("No <code>method.md</code> in this method folder", html)
            self.assertIn("<th>predicted click-through</th>", html)
            self.assertIn('data-method="2-Design-M02-overall-performance"', html)   # R2 is not made by M02 yet

    def test_new_folder_under_a_method_keeps_the_task_number(self):
        with TemporaryDirectory() as td:
            board = method_board_fixture(Path(td))
            out = new_folder(board, "R2", "2-Design-M02-overall-performance")
            self.assertEqual(out["rel"], "2-Design-M02-overall-performance/Design-02-patients-refill-due-refill-review-ui-card/"
                                         "Design-02-patients-refill-due-refill-review-ui-card.md")
            self.assertFalse(out["brief_updated"])               # R2 already names its folder
            page = (board / out["rel"]).read_text(encoding="utf-8")
            self.assertIn("method: M02 · overall performance", page)
            out = new_folder(board, "R3", "2-Design-M01-goal-only")   # R3 has no folder: next free number
            self.assertTrue(out["folder"].startswith("Design-03-"))
            self.assertTrue(out["brief_updated"])
            with self.assertRaises(ValueError):
                new_folder(board, "R3", "2-Design-M01-goal-only")
            with self.assertRaises(ValueError):
                new_folder(board, "R1", "2-Design-M09-none")

    def test_bundle_names_the_method(self):
        with TemporaryDirectory() as td:
            board = method_board_fixture(Path(td))
            head = bundle_csv(design_board_snapshot(board, Path(td))).splitlines()[0]
            self.assertIn("folder,method,item", head)


if __name__ == "__main__":
    unittest.main()


class BundleTest(unittest.TestCase):
    def test_bundle_has_one_row_per_design_with_its_brief_line(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            snap = design_board_snapshot(board, Path(td))
            rows = bundle_rows(snap)
            self.assertEqual([(r["folder"][:9], r["item"]) for r in rows],
                             [("Design-01", "ITEM01")])   # only a passed Verify is deliverable
            row = rows[0]
            self.assertEqual((row["line"], row["venue"], row["item"]), ("R1", "sms", "ITEM01"))
            self.assertTrue(row["text"].startswith("Hi, it's Dr. {NAME}'s office."))
            self.assertNotIn("sha256", row)          # no content hashes (JL 260928)
            csv_text = bundle_csv(snap)
            self.assertTrue(csv_text.startswith("line,who,their_job,venue,folder,item,title,state,text,draft_run,render"))
            self.assertIn(",ready,", csv_text)
            self.assertIn("Download all designs · 1 · csv", render_design_board(snap))
            self.assertNotIn("Download all designs", render_design_board(design_board_snapshot(board, Path(td), static=True)))
