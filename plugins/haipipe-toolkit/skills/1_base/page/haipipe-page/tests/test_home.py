#!/usr/bin/env python3
"""Read-only discovery and rendering checks for the SPACE Board Home."""
import io
import re
import tempfile
import unittest
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent.parent  # the engine dir
sys.path.insert(0, str(HERE))
from live.home import (FOLD_OPEN_MAX, HomeMixin, board_slug, discover_boards,
                       render_home, resolve_short, resolve_workbench)


class SpaceHomeTest(unittest.TestCase):
    def test_public_route_is_boards_not_the_private_api_namespace(self):
        request = HomeMixin()
        request.path = "/"
        self.assertTrue(request.is_home_request())
        request.path = "/boards/"
        self.assertTrue(request.is_home_request())
        request.path = "/_board/home"
        self.assertFalse(request.is_home_request())

    def test_discovers_real_boards_and_ignores_generated_or_archived_ones(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            board = root / "project" / "diagram" / "01-topic"
            (board / "QA-design").mkdir(parents=True)
            (board / "board").mkdir()
            (board / "board.md").write_text("# A <Board>\nspine: Find & settle it\n")
            (board / "QA-design" / "QA1-question.md").write_text("# Q\nstate: ✅ SETTLED\n")
            (board / "board" / "index.html").write_text("ok")
            archived = root / "_archive" / "old"; archived.mkdir(parents=True)
            (archived / "board.md").write_text("# Do not show\n")
            cards = discover_boards(root)
            self.assertEqual(len(cards), 1)
            self.assertEqual(cards[0]["title"], "A <Board>")
            self.assertEqual(cards[0]["settled"], 1)
            self.assertTrue(cards[0]["ready"])
            page = render_home(root)
            self.assertIn("<title>SPACE Home</title>", page)
            self.assertIn("<h1>SPACE Home</h1>", page)
            self.assertNotIn("Fusion Space", page)
            self.assertNotIn('class="workspace-title"', page)
            self.assertIn("A &lt;Board&gt;", page)
            self.assertIn('class="t">A &lt;Board&gt;</span>', page)
            self.assertIn('class="ir home-row"', page)
            self.assertIn('id="board-list"', page)
            self.assertIn('placeholder="Search boards"', page)
            self.assertIn('class="board-list project-groups"', page)
            self.assertIn('class="project-group"', page)
            self.assertIn('<span class="project-name">SPACE / Shared</span>', page)
            self.assertIn('href="/w/topic"', page)    # no declared workbench: the base frame opens it
            self.assertIn('<span class="home-folder">/Task/01-topic</span>', page)
            self.assertNotIn("Open board", page)
            self.assertNotIn("JJ-LUO", page)
            self.assertNotIn("Physician-SPACE", page)
            self.assertNotIn('class="summary"', page)
            self.assertNotIn('class="kind-section"', page)
            self.assertNotIn('class="row-status"', page)
            self.assertNotIn('class="row-pages"', page)
            self.assertNotIn('class="row-path"', page)
            self.assertEqual(cards[0]["kind"], "Task Board")

    def test_home_can_be_branded_for_a_space(self):
        with tempfile.TemporaryDirectory() as tmp:
            page = render_home(Path(tmp), "Physician-SPACE", "https://physician.jjluo.com")
            self.assertIn("<h1>Physician-SPACE</h1>", page)
            self.assertNotIn('class="workspace-title"', page)
            self.assertNotIn("Fusion Space", page)
            self.assertNotIn("https://physician.jjluo.com", page)

    def test_project_owner_survives_a_server_started_in_a_project_subroot(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            project = workspace / "examples-2-lm" / "Proj10-LLM-Baseline"
            (project / "project.yaml").parent.mkdir(parents=True)
            (project / "project.yaml").write_text(
                "schema: haipipe-project/v1\n"
                "id: Proj10-LLM-Baseline\n"
                "profile: research\n"
                "state: active\n")
            discoveries = project / "discoveries"
            board = discoveries / "b00_source_intake"
            (board / "QA-intake").mkdir(parents=True)
            (board / "board.md").write_text("# Source Intake\nspine: s\n")
            (board / "QA-intake" / "QA1-source.md").write_text("# Q\nstate: 🔴 OPEN\n")

            cards = discover_boards(discoveries)
            self.assertEqual(len(cards), 1)
            self.assertEqual(cards[0]["project"], "Proj10-LLM-Baseline")
            self.assertEqual(cards[0]["project_scope"], "project")
            page = render_home(discoveries)
            self.assertNotIn("SPACE / Shared", page)
            self.assertIn(
                '<span class="project-name">Proj10-LLM-Baseline</span>', page)

    def test_groups_task_discovery_paper_design_and_skill_boards_with_skill_precedence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            def add_board(relative, title):
                board = root / relative
                (board / "QA-group").mkdir(parents=True)
                (board / "board").mkdir()
                (board / "board.md").write_text(f"# {title}\nspine: Test type\n")
                (board / "QA-group" / "QA1-question.md").write_text("# Q\nstate: 🟡 PARTIAL\n")
                (board / "board" / "index.html").write_text("index")

            add_board("project/diagram/01-task", "Task")
            add_board("examples/Project-A/discoveries/b01_evidence", "Discovery")
            add_board("papers/Paper-A/0-lifecycle", "Paper")
            add_board("examples/Project-A/applications/App-A/B01-App-DesignBoard",
                      "Design")
            add_board("Tools/plugins/example/skills/diagrams/01-paper-skill", "Paper Skill")
            cards = {card["title"]: card for card in discover_boards(root)}
            self.assertEqual(cards["Task"]["kind"], "Task Board")
            self.assertEqual(cards["Discovery"]["kind"], "Discovery Board")
            self.assertEqual(cards["Paper"]["kind"], "Paper Board")
            self.assertEqual(cards["Design"]["kind"], "Design Board")
            self.assertEqual(cards["Paper Skill"]["kind"], "Skill Board")
            page = render_home(root)
            for title in ("Task", "Discovery", "Paper", "Design", "Paper Skill"):
                self.assertIn(f'class="t">{title}</span>', page)
            for project in ("Project-A", "SPACE / Shared", "Tools &amp; Skills"):
                self.assertIn(f'<span class="project-name">{project}</span>', page)
            self.assertIn('<section class="space-section" data-space-key="examples"', page)
            self.assertIn('<section class="space-section" data-space-key="Tools"', page)
            self.assertLess(
                page.index('data-space-key="examples"'),
                page.index('data-space-key="Tools"'))
            self.assertNotIn("Task Boards", page)
            self.assertNotIn("Discovery Boards", page)
            self.assertNotIn("Paper Boards", page)
            self.assertNotIn("Design Boards", page)
            self.assertNotIn("Skill Boards", page)

    def test_canonical_designboard_suffix_wins_except_for_skill_boards(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            def add_board(relative, title):
                board = root / relative
                board.mkdir(parents=True)
                (board / "board.md").write_text(f"# {title}\nspine: s\n")

            add_board("examples/Project-A/papers/Paper-A/B01-App-DesignBoard",
                      "Canonical Design")
            add_board("examples/Project-A/diagram/B01-App-DesignBoard-backup",
                      "Backup")
            add_board("Tools/plugins/demo/skills/diagrams/B01-App-DesignBoard",
                      "Skill Design")
            cards = {card["title"]: card["kind"]
                     for card in discover_boards(root)}
            self.assertEqual(cards["Canonical Design"], "Design Board")
            self.assertEqual(cards["Backup"], "Task Board")
            self.assertEqual(cards["Skill Design"], "Skill Board")

    def test_groups_boards_by_project_before_board_kind(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            def add_board(project, relative, title):
                owner = root / "examples" / project
                owner.mkdir(parents=True, exist_ok=True)
                (owner / "project.yaml").write_text(
                    "schema: haipipe-project/v1\n"
                    f"id: {project}\nprofile: research\n"
                    "git_mode: workspace\nstate: active\nmission: test\n")
                board = owner / relative
                (board / "QA-group").mkdir(parents=True)
                (board / "board").mkdir()
                (board / "board.md").write_text(
                    f"# {title}\nspine: Project-owned board\n")
                (board / "QA-group" / "QA1-question.md").write_text(
                    "# Q\nstate: 🟡 PARTIAL\n")
                (board / "board" / "index.html").write_text("index")

            add_board("Project-One", "diagram/01-task", "One Task")
            add_board("Project-One", "papers/Paper-A/0-paperboard", "One Paper")
            add_board("Project-Two", "diagram/01-task", "Two Task")

            cards = discover_boards(root)
            self.assertEqual(
                {card["project"] for card in cards},
                {"Project-One", "Project-Two"})
            one = [card for card in cards if card["project"] == "Project-One"]
            self.assertEqual({card["kind"] for card in one},
                             {"Task Board", "Paper Board"})

            page = render_home(root)
            for title in ("One Task", "One Paper", "Two Task"):
                self.assertIn(f'class="t">{title}</span>', page)
            self.assertIn('<span class="project-name">Project-One</span>', page)
            self.assertIn('<span class="project-name">Project-Two</span>', page)
            self.assertLess(
                page.index('<span class="project-name">Project-One</span>'),
                page.index('<span class="project-name">Project-Two</span>'))
            self.assertNotIn("Task Boards", page)
            self.assertNotIn("Paper Boards", page)

    def test_projects_are_collapsible_and_reorderable_without_new_source_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            board = root / "examples" / "Project-One" / "diagram" / "01-topic"
            (board / "QA-topic").mkdir(parents=True)
            (root / "examples" / "Project-One" / "project.yaml").write_text(
                "id: Project-One\n")
            (board / "board.md").write_text("# Topic\nspine: s\n")
            (board / "QA-topic" / "QA1-question.md").write_text("# Q\nstate: 🔴 OPEN\n")

            page = render_home(root)
            self.assertIn('<details class="project-group"', page)
            self.assertIn('class="project-grip"', page)
            self.assertNotIn('class="project-move', page)
            self.assertIn("localStorage", page)
            self.assertIn("restoreOrder", page)
            self.assertIn("saveOrder", page)
            self.assertIn("restoreCollapsed", page)
            self.assertIn("saveCollapsed", page)
            self.assertIn("pointerdown", page)
            self.assertIn("pointermove", page)
            self.assertIn("pointerup", page)
            self.assertIn("addEventListener('toggle'", page)
            # one Project: the Space view starts with it open (FOLD_OPEN_MAX)
            self.assertIn(' role="listitem" open>', page)
            self.assertIn('class="space-projects"', page)
            self.assertIn("project-collapsed:v3", page)

    def test_index_only_lists_boards_that_can_be_opened(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            ready = root / "project" / "diagram" / "01-ready"
            (ready / "QA-design").mkdir(parents=True)
            (ready / "board.md").write_text("# Ready Board\nspine: s\n")
            (ready / "QA-design" / "QA1-question.md").write_text("# Q\nstate: 🔴 OPEN\n")

            pending = root / "project" / "diagram" / "02-pending"
            pending.mkdir(parents=True)
            (pending / "board.md").write_text("# Pending Board\nspine: s\n")

            page = render_home(root)
            self.assertIn('class="t">Ready Board</span>', page)
            self.assertIn('<span class="home-folder">/Task/01-ready</span>', page)
            self.assertNotIn("Pending Board", page)

    def test_legacy_examples_project_groups_without_a_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            board = root / "examples-nlp" / "Legacy-Project" / "diagram" / "01-topic"
            (board / "QA-group").mkdir(parents=True)
            (board / "board.md").write_text("# Legacy\nspine: s\n")
            (board / "QA-group" / "QA1-question.md").write_text(
                "# Q\nstate: 🔴 OPEN\n")
            card = discover_boards(root)[0]
            self.assertEqual(card["project"], "Legacy-Project")
            self.assertEqual(card["project_path"],
                             "examples-nlp/Legacy-Project")

    def test_nested_examples_folder_does_not_create_a_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            board = root / "Tools" / "plugins" / "demo" / "examples" / "Fixture" / "diagram" / "01-topic"
            (board / "QA-group").mkdir(parents=True)
            (board / "board.md").write_text("# Tool example\nspine: s\n")
            (board / "QA-group" / "QA1-question.md").write_text(
                "# Q\nstate: 🔴 OPEN\n")
            card = discover_boards(root)[0]
            self.assertEqual(card["project"], "Tools & Skills")
            self.assertEqual(card["project_scope"], "shared")

    def test_manifest_fields_strip_inline_comments_and_nearest_manifest_wins(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            outer = root / "examples" / "Outer"
            inner = outer / "papers" / "Inner"
            outer.mkdir(parents=True)
            inner.mkdir(parents=True)
            (outer / "project.yaml").write_text(
                "id: Outer # outer project\nprofile: research\nstate: active\n")
            (inner / "project.yaml").write_text(
                "id: 'Inner # One' # nearest project\n"
                "profile: hybrid # valid comment\nstate: active\n")
            board = inner / "diagram" / "01-topic"
            (board / "QA-group").mkdir(parents=True)
            (board / "board.md").write_text("# Inner board\nspine: s\n")
            (board / "QA-group" / "QA1-question.md").write_text(
                "# Q\nstate: 🔴 OPEN\n")
            card = discover_boards(root)[0]
            self.assertEqual(card["project"], "Inner # One")
            self.assertEqual(card["project_profile"], "hybrid")
            self.assertEqual(card["project_path"],
                             "examples/Outer/papers/Inner")

    def test_fixture_boards_are_not_discovered(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for segment in ("_fixture", "fixtures"):
                board = root / "Tools" / segment / "01-topic"
                board.mkdir(parents=True)
                (board / "board.md").write_text("# Fixture\nspine: s\n")
            self.assertEqual(discover_boards(root), [])

    def test_non_project_space_and_tools_buckets_are_explicit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for relative, title in (("diagram/01-space", "Space"),
                                    ("Tools/plugins/demo/skills/diagrams/01-tool", "Tool")):
                board = root / relative
                (board / "QA-group").mkdir(parents=True)
                (board / "board.md").write_text(f"# {title}\nspine: s\n")
                (board / "QA-group" / "QA1-question.md").write_text(
                    "# Q\nstate: 🔴 OPEN\n")
            owners = {card["title"]: card["project"]
                      for card in discover_boards(root)}
            self.assertEqual(owners,
                             {"Space": "SPACE / Shared",
                              "Tool": "Tools & Skills"})


class SpaceViewTest(unittest.TestCase):
    """The Space view: Project -> Theme -> Block card, a kind filter kept in the
    URL, Project folds, and cards that open the Block's workbench."""

    @staticmethod
    def add_board(root, relative, title, head=""):
        board = root / relative
        (board / "QA-group").mkdir(parents=True)
        (board / "board.md").write_text(f"# {title}\n{head}spine: s\n")
        (board / "QA-group" / "QA1-question.md").write_text("# Q\nstate: 🔴 OPEN\n")
        return board

    def project(self, root, name):
        owner = root / "examples" / name
        owner.mkdir(parents=True, exist_ok=True)
        (owner / "project.yaml").write_text(f"id: {name}\n")
        return f"examples/{name}"

    def full_project(self, root):
        base = self.project(root, "Project-A")
        # created out of order on purpose: the view orders the Themes, not the disk
        self.add_board(root, f"{base}/designs/B01_DesignBoard-X", "Design X")
        self.add_board(root, f"{base}/insights/Prototype-Insight-X", "Insight X")
        self.add_board(root, f"{base}/paper/Paper-X", "Paper X", "dialect: paper\n")
        self.add_board(root, f"{base}/cowork/b01_partner", "CoWork X",
                       "board-kind: cowork-block\n")
        self.add_board(root, f"{base}/discoveries/b01_evidence", "Discovery X",
                       "board-kind: discovery-block\n")
        self.add_board(root, f"{base}/tasks/b02_model", "Task Two",
                       "board-kind: task-block\nstate: 🟡 OPEN · free text never shown\n")
        self.add_board(root, f"{base}/tasks/b01_data", "Task One",
                       "board-kind: task-block\n")
        return base

    def test_blocks_group_by_theme_in_contract_order_with_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.full_project(root)
            page = render_home(root)
            order = [page.index(f'data-theme="{theme}"') for theme in
                     ("tasks", "discoveries", "cowork", "paper", "insights", "designs")]
            self.assertEqual(order, sorted(order))
            self.assertIn('<span class="theme-name">tasks</span>\n  '
                          '<span class="theme-count" aria-label="2 blocks">2</span>', page)
            self.assertIn('<span class="project-count" aria-label="7 blocks">7</span>', page)
            self.assertLess(page.index('class="t">Task One</span>'),
                            page.index('class="t">Task Two</span>'))
            for kind in ("task", "discovery", "cowork", "paper", "insight", "design"):
                self.assertIn(f'data-kind="{kind}"', page)
            # the card: kind emoji, title, folder, and only the state word
            self.assertIn('<span class="home-folder">/Design/B01_DesignBoard-X</span>', page)
            self.assertIn('<span class="home-state" title="Board state">🟡 OPEN</span>', page)
            self.assertNotIn("free text never shown", page)

    def test_shared_buckets_group_by_the_theme_their_kind_lives_in(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.add_board(root, "Tools/plugins/demo/skills/diagrams/01-tool", "Tool")
            self.add_board(root, "notes/01-space", "Space note")
            page = render_home(root)
            self.assertIn('<span class="project-name">Tools &amp; Skills</span>', page)
            self.assertIn('<span class="project-name">SPACE / Shared</span>', page)
            self.assertIn('data-theme="skills"', page)
            self.assertIn('data-theme="work"', page)       # a task Board's Theme is work/ (b03 s01-D28)

    def test_kind_filter_hides_other_kinds_and_is_written_as_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.full_project(root)
            plain = render_home(root)
            self.assertIn('data-kind="all" aria-pressed="true"', plain)
            self.assertNotIn("data-kind=\"labeling\"", plain)    # only the kinds present
            page = render_home(root, kind="task")
            self.assertIn('data-kind="all" aria-pressed="false"', page)
            self.assertIn('href="?" data-kind="task" aria-pressed="true"', page)
            self.assertIn('href="?kind=task,paper" data-kind="paper"', page)
            rows = re.findall(r'<a class="ir home-row"[^>]*>', page)
            self.assertEqual(len(rows), 7)
            for row in rows:
                self.assertEqual('data-kind="task"' in row, " hidden" not in row, row)
            self.assertRegex(page, r'data-theme="paper" aria-label="paper" hidden>')
            self.assertRegex(page, r'data-theme="tasks" aria-label="tasks">')
            both = render_home(root, kind="paper,task")
            self.assertIn('href="?kind=paper" data-kind="task" aria-pressed="true"', both)
            # an unknown kind is no filter, not an empty page
            self.assertEqual(render_home(root, kind="bogus"), plain)
            self.assertEqual(render_home(root, kind="all"), plain)

    def test_serve_home_reads_the_kind_from_the_query(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.full_project(root)

            class Request(HomeMixin):
                command = "GET"
                def send_response(self, code): self.code = code
                def send_header(self, *_): pass
                def end_headers(self): pass

            request = Request()
            request.root, request.path, request.wfile = root, "/?kind=paper", io.BytesIO()
            request.serve_home()
            body = request.wfile.getvalue().decode("utf-8")
            self.assertEqual(request.code, 200)
            self.assertIn('data-kind="paper" aria-pressed="true"', body)

    def test_projects_start_open_only_when_the_view_is_small(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for index in range(FOLD_OPEN_MAX + 1):
                base = self.project(root, f"Project-{index}")
                self.add_board(root, f"{base}/tasks/b01_t{index}", f"T{index}")
            self.add_board(root, "examples/Project-0/papers/Paper-Z", "Paper Z",
                           "dialect: paper\n")
            many = render_home(root)
            self.assertEqual(many.count('<details class="project-group"'), FOLD_OPEN_MAX + 1)
            self.assertNotIn(' role="listitem" open>', many)
            # the paper filter leaves one Project in view: it starts open
            few = render_home(root, kind="paper")
            details = re.findall(r'<details class="project-group"[^>]*>', few)
            shown = [tag for tag in details if " hidden" not in tag]
            self.assertEqual(len(shown), 1)
            self.assertTrue(shown[0].endswith(' open>'))
            self.assertEqual(len(details) - len(shown), FOLD_OPEN_MAX)
            self.assertIn("project-collapsed:v3", few)
            self.assertIn('<summary class="project-summary"', few)

    def test_cards_open_the_block_workbench_when_the_short_route_resolves(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base = self.full_project(root)
            # the same folder name in two Projects: /w/ would be ambiguous (404)
            other = self.project(root, "Project-B")
            self.add_board(root, f"{base}/tasks/b09_shared", "Shared A", "board-kind: task-block\n")
            self.add_board(root, f"{other}/tasks/b09_shared", "Shared B", "board-kind: task-block\n")
            self.add_board(root, f"{other}/tasks/b10_plain", "Plain")   # no workbench
            page = render_home(root)
            hrefs = dict(re.findall(
                r'<a class="ir home-row" href="([^"]+)".*?class="t">([^<]+)</span>', page, re.S))
            by_title = {title: href for href, title in hrefs.items()}
            self.assertEqual(by_title["Task One"], "/w/b01_data")
            self.assertEqual(by_title["Paper X"], "/w/paper-x")
            self.assertEqual(by_title["Discovery X"], "/w/b01_evidence")
            self.assertTrue(by_title["Shared A"].startswith("/_board/workbench?path="))
            self.assertEqual(by_title["Plain"], "/w/b10_plain")       # the frame opens any Block
            for title, href in by_title.items():
                if href.startswith("/w/"):
                    target, reason = resolve_workbench(root, href[3:])
                    self.assertIsNotNone(target, (title, reason))


class ShortRouteTest(unittest.TestCase):
    """QE2 · `/b/<slug>[/<page-id>]`, the route that replaces the long path.

    JL measured a strip's link at 131 characters on 260802, 78 of them the path
    from the SPACE root down to the board folder. These lock in the two things
    that make the short form safe to print: it resolves to the SAME file the
    long URL names, and an id that resolves to nothing is a miss rather than a
    redirect to the wrong page.
    """

    def fixture(self, tmp):
        root = Path(tmp)
        board = root / "unit" / "diagram" / "01-topic-260722"
        (board / "QA-design").mkdir(parents=True)
        (board / "board" / "QA").mkdir(parents=True)
        (board / "board.md").write_text("# /the-board: a title\nspine: s\n")
        (board / "QA-design" / "QA1-question.md").write_text("# Q\nstate: 🔴 OPEN\n")
        (board / "board" / "index.html").write_text("index")
        (board / "board" / "QA.html").write_text("group")
        (board / "board" / "QA" / "QA1-question.html").write_text("page")
        return root, board

    def test_slug_drops_the_ordinal_and_the_date(self):
        self.assertEqual(board_slug("01-boardform-260722"), "boardform")
        self.assertEqual(board_slug("0-lifecycle"), "lifecycle")
        self.assertEqual(
            board_slug("0-lifecycle", "Paper-Personality2Opioid-MISQ2026"),
            "personality2opioid-misq2026-lifecycle")
        self.assertEqual(
            board_slug("0-paperboard", "Paper-Personality2Opioid-MISQ2026"),
            "personality2opioid-misq2026-paperboard")
        self.assertEqual(board_slug("01-boardform-260722", "diagrams"), "boardform")
        self.assertEqual(board_slug("plain"), "plain")

    def test_ambiguous_slug_is_a_miss_not_a_random_board(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for owner in ("Paper-One", "Paper-Two"):
                board = root / owner / "0-paperboard"
                (board / "board").mkdir(parents=True)
                (board / "board.md").write_text("# Paper\nspine: s\n")
                (board / "board" / "index.html").write_text("index")
            self.assertIsNone(resolve_short(root, "paperboard"))

    def test_resolves_index_page_and_group(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, board = self.fixture(tmp)
            # the Board lands in the base frame (JL 261007); on an --only host, its own workbench or
            # its board.md; a page opens in the live reader; a group code opens the Board
            base = "/unit/diagram/01-topic-260722"
            self.assertEqual(resolve_short(root, "topic"), "/_board/workbench?path=unit/diagram/01-topic-260722")
            self.assertEqual(resolve_short(root, "topic", only={"page"}), f"{base}/board.md")
            self.assertEqual(resolve_short(root, "topic", "QA1"),
                             f"/_board/page?path={base}/QA-design/QA1-question.md")
            self.assertEqual(resolve_short(root, "topic", "QA", only={"page"}), f"{base}/board.md")

    def test_the_full_folder_name_still_resolves(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, _ = self.fixture(tmp)
            self.assertEqual(resolve_short(root, "01-topic-260722"),
                             resolve_short(root, "topic"))

    def test_an_unknown_board_or_page_is_a_miss_not_a_wrong_redirect(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, _ = self.fixture(tmp)
            self.assertIsNone(resolve_short(root, "nosuchboard"))
            self.assertIsNone(resolve_short(root, "topic", "QZ9"))
            self.assertIsNone(resolve_short(root, ""))

    def test_the_route_matcher_accepts_only_its_own_shape(self):
        request = HomeMixin()
        for path, expected in [
            ("/b/topic", ("topic", "")),
            ("/b/topic/QA1", ("topic", "QA1")),
            ("/b/topic/QA1/", ("topic", "QA1")),
        ]:
            request.path = path
            self.assertEqual(request.short_request(), expected, path)
        for path in ("/b", "/b/", "/b/topic/QA1/extra", "/boards", "/bogus/x"):
            request.path = path
            self.assertIsNone(request.short_request(), path)


if __name__ == "__main__":
    unittest.main()
