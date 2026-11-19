"""A Page Task in the frame: the seven step tabs, plan, evidence, displays, cards and review."""
from __future__ import annotations

import json
import os
import re
import shutil
import tempfile
import unittest
import zipfile
from html import unescape
from urllib.parse import parse_qs, unquote, urlparse
from pathlib import Path

from host_paths import bootstrap
bootstrap()

from live import frame  # noqa: E402
from live import task_draft  # noqa: E402
from live.frame_view import FrameMixin  # noqa: E402
from frame_fixtures import project, tiny_deck  # noqa: E402,F401


class PageTaskTest(unittest.TestCase):
    # A Page Task on the frame (task_draft.draft_task_spaces, b03 s13 / b16 s13): the Page's own views, embedded.
    def test_a_draft_task_opens_the_seven_step_tabs(self):
        # b32 s41 (JL 261015, 4 · Display JL 261020): Work is Studio · 1 · Plan · 2 · Write · 3 · Evidence · 4 · Display ·
        # 5 · Revise · Delivery, each
        # Operation over Result read from the Task's files; Report has the same tabs, Results only, plus Table and
        # Questions; Description is the face alone; Runs and Delivery keep the Page's own views
        from urllib.parse import parse_qs, unquote, urlparse
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            board = root / "Project-X/paper/Paper-Demo"
            section = board / "Ba-Desk-Main/S-Desk-Main-1-Intro"
            (section / "draft" / "records").mkdir(parents=True)
            (board / "board.md").write_text("# Paper\n\ndialect: paper\n")
            (section / "S-Desk-Main-1-Intro.md").write_text("# S-Desk-Main-1-Intro · Intro\n\nreader-question: Why now?\n")
            (section / "draft" / "records" / "S-Desk-Main-1-Intro-requirement.md").write_text("V1 · at most 900 words\n")
            spaces = task_draft.draft_task_spaces(section, root)
            self.assertEqual({k: v.subspaces for k, v in spaces.items()}, task_draft.DRAFT_TASK_SUBS)
            self.assertEqual(spaces["Work Details"].subspaces, ("Studio", "1 · Plan", "2 · Write", "3 · Evidence",
                                                                "4 · Display", "5 · Revise", "Delivery"))
            work = spaces["Work Details"]
            self.assertEqual(work.open, "1 · Plan")                              # nothing written: the plan is next
            self.assertIn("Operation", work.html)
            self.assertIn("Result", work.html)
            self.assertIn("/haipipe-draft ", work.html)                          # the prompt, with its notes box
            self.assertIn('data-field="your notes"', work.html)
            self.assertIn("Why now?", work.html)                                # Input, read from the face
            self.assertIn("at most 900 words", work.html)                       # the Requirement, a card of 1 · Plan
            self.assertIn("Rubric", work.html)
            self.assertEqual(spaces["Audience Report"].open, "1 · Plan")
            self.assertNotIn("Operation", spaces["Audience Report"].html)        # Report: the Results only
            self.assertEqual(spaces["Description"].html, "")                    # the vanilla face and fields
            # a draft with §1 waits for the Sign; once written, Write is done and Revise is next
            (section / "draft" / "S-Desk-Main-1-Intro-draft-v0.1.md").write_text(
                "# Intro · draft v0.1\n\napproved: ⬜\n\n## 1 · Structure\n\n### C1.P1 · Why now\n"
                "- B1 · S1 · [Need] The problem grows\n\n## 3 · Draft\n\n### C1.P1 · Why now\n"
                "- B1 · S1 · The problem grows ⟦pending⟧.\n")
            states = task_draft.draft_task_spaces(section, root)["Work Details"]
            self.assertEqual(states.open, "1 · Plan")
            self.assertIn("✍ sign", states.html)
            write = task_draft.draft_task_spaces(section, root, "2 · Write")["Work Details"]
            self.assertIn("The problem grows", write.html)
            self.assertIn("⟦pending⟧", write.html)
            self.assertEqual(task_draft.draft_task_spaces(section, root, "Draft-Scratch")["Work Details"].open,
                             "2 · Write")                                       # an old link lands on its step
            table = task_draft.draft_task_spaces(section, root, "Table")["Audience Report"]
            src = re.search(r'src="([^"]+)"', table.html).group(1)
            q = parse_qs(urlparse(src.replace("&amp;", "&")).query)
            self.assertEqual(urlparse(src).path, "/_board/draft")
            self.assertEqual((q["path"][0], q["file"][0], q["embed"][0], q["space"][0], q["view"][0]),
                             ("Project-X/paper/Paper-Demo/board.md", "Ba-Desk-Main/S-Desk-Main-1-Intro/S-Desk-Main-1-Intro.md",
                              "1", "bullet", "table"))
            (board / "delivery" / "Ba-Desk-Main/S-Desk-Main-1-Intro" / "latex" / "draft-bibliography").mkdir(parents=True)
            (board / "delivery" / "Ba-Desk-Main/S-Desk-Main-1-Intro" / "latex" / "S-Desk-Main-1-Intro.tex").write_text("x")
            (board / "delivery" / "Ba-Desk-Main/S-Desk-Main-1-Intro" / "latex" / "draft-bibliography" / "S-Desk-Main-1-Intro.bib").write_text("x")
            runs = task_draft.draft_task_spaces(section, root)["Runs"]               # the Page Runs view, embedded (s13)
            self.assertEqual((runs.subspaces, runs.page), ((), True))
            self.assertIn("/_board/runs?", runs.html)
            self.assertIn("embed=1", runs.html)
            deliv = task_draft.draft_task_spaces(section, root)["Delivery"]          # item cards, no third row (s13 1b)
            self.assertEqual((deliv.subspaces, deliv.page), ((), True))
            self.assertIn("<h2>Deliveries</h2>", deliv.html)                    # one card per kind, its result inside
            self.assertIn("📄 LaTeX", deliv.html)
            self.assertIn("S-Desk-Main-1-Intro.pdf is not compiled yet; the piece:", deliv.html)
            self.assertIn("draft-bibliography/S-Desk-Main-1-Intro.bib", deliv.html)
            self.assertIn("not built yet: run Build", deliv.html)                # Word, Web … not built
            self.assertEqual([k["label"] for k in deliv.run_types], ["run-delivery-<target>", "run-check-<page>"])
            self.assertTrue(all(isinstance(x, str) and not x.startswith("[") for k in deliv.run_types for x in k["skills"]))
            step = task_draft.draft_task_spaces(section, root, "Delivery")["Work Details"]   # the Delivery step: 4 boxes
            self.assertIn("1 of 4 · build", step.html)
            self.assertIn("4 of 4 · read back", step.html)
            merged = frame.spaces_for(frame.Theme(name="paper", spaces=lambda *a: task_draft.draft_task_spaces(section, root)),
                                      "Task", section, root)["Delivery"]
            self.assertEqual((merged.subspaces, [k["label"] for k in merged.run_types]),
                             ((), ["run-delivery-<target>", "run-check-<page>"]))

    def test_the_plan_is_one_mind_map_of_section_one(self):
        # JL 261020: "merge them together ... draw the mind map for the plan": the Section and its arc in the middle,
        # each part (when there are several), each paragraph with the question it hands on, each Bullet a leaf
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            board = root / "Project-X/paper/Paper-Demo"
            section = board / "Ba-Desk-Main/S-Desk-Main-2-Methods"
            (section / "draft").mkdir(parents=True)
            (board / "board.md").write_text("# Paper\n\ndialect: paper\n")
            (section / "S-Desk-Main-2-Methods.md").write_text("# S-Desk-Main-2-Methods · Methods\n")
            (section / "draft" / "S-Desk-Main-2-Methods-draft-v0.1.md").write_text(
                "# Methods · draft v0.1\n\napproved: ⬜\narc: Design first, then the data.\n\n## 1 · Structure\n\n"
                "### Structure Overview\n\n- C1 · Study Design\n- C1.P1 · The design\n  → S1 · cross-sectional\n"
                "  → C2.P2: what is a query?\n- C2 · Queries\n- C2.P2 · The queries\n  → S2 · the unit\n\n"
                "### C1.P1 · The design\n- B1 · S1 · [Design] A cross-sectional comparison\n"
                "  Note: the review board ⟦check⟧\n\n### C2.P2 · The queries\n- B1 · S2 · [Unit] A query is 1 specialty\n")
            html = task_draft.draft_task_spaces(section, root, "1 · Plan")["Work Details"].html
            self.assertIn('<div class="pm pm-folds">', html)              # the map, its paragraphs foldable
            self.assertNotIn("Bullets, one job each", html)                    # merged into the one map
            self.assertIn("Design first, then the data.", html)                 # the arc, in the middle
            self.assertEqual(html.count('class="pm-node pm-cnode"'), 2)         # two parts: C1, C2
            self.assertIn('data-raw="what is a query?"', html)                 # the hand-on, on the arrow (↓ in CSS)
            self.assertIn('<li data-s="s1" title="the review board ⟦check⟧">', html)
            self.assertIn("pm-flag", html)                                      # the ⟦check⟧ in its note, in red
            self.assertIn("A query is 1 specialty", html)
            # JL 261020: "how could I operate and edit it?": each piece typed into in place, written into §1
            from live import draft_steps
            self.assertIn('data-edit=words data-raw="A cross-sectional comparison"', html)
            self.assertIn('data-edit=role data-raw="Unit"', html)
            draft = section / "draft" / "S-Desk-Main-2-Methods-draft-v0.1.md"
            act = lambda **p: draft_steps.plan_act(root, {"task": "Project-X/paper/Paper-Demo/Ba-Desk-Main/"
                                                           "S-Desk-Main-2-Methods", "file": draft.name, **p})
            self.assertEqual(act(what="words", s="S2", was="A query is 1 specialty", value="A query is 1 city")[0], 200)
            self.assertIn("- B1 · S2 · [Unit] A query is 1 city\n", draft.read_text())
            self.assertEqual(act(what="words", s="S2", was="A query is 1 specialty", value="x")[0], 409)   # stale
            self.assertEqual(act(what="para", p="C1.P1", was="The design", value="The study design")[0], 200)
            self.assertIn("- C1.P1 · The study design\n", draft.read_text())
            self.assertIn("### C1.P1 · The study design\n", draft.read_text())
            self.assertEqual(act(what="add", after="S1", value="Two arms", role="Arms")[0], 200)
            self.assertIn("  Note: the review board ⟦check⟧\n- B2 · s1a · [Arms] Two arms\n", draft.read_text())
            self.assertEqual(act(what="move", s="s1a", p="C2.P2")[0], 200)
            self.assertIn("[Unit] A query is 1 city\n- B2 · s1a · [Arms] Two arms\n", draft.read_text())
            self.assertEqual(act(what="drop", s="s1a", was="Two arms")[0], 200)
            self.assertNotIn("Two arms", draft.read_text())
            self.assertEqual(draft_steps.plan_act(root, {"task": "Project-X"}, read_only=True)[0], 403)
            # JL 261020: "How could I add the P here or add the S here?": ＋ point under each paragraph's points,
            # ＋ paragraph after each paragraph; the paragraphs after a new one move down a number everywhere
            self.assertEqual(html.count("data-add=point"), 2)
            self.assertEqual(html.count("data-add=para "), 2)
            self.assertEqual(act(what="add", after="S2", p="C2.P2", value="Last in P2")[0], 200)
            self.assertIn("- B2 · s2a · Last in P2", draft.read_text())
            self.assertEqual(act(what="addpara", after="C1.P1", value="The setting")[0], 200)
            text = draft.read_text()
            self.assertIn("- C1.P1 · The study design\n  → S1 · cross-sectional\n- C1.P2 · The setting\n"
                          "  → C2.P3: what is a query?\n", text)                # it takes over the hand-on
            self.assertIn("### C1.P2 · The setting\n\n### C2.P3 · The queries\n", text)
            self.assertEqual(act(what="add", after="", p="C1.P2", value="Where it ran")[0], 200)   # its first point
            self.assertIn("### C1.P2 · The setting\n- B1 · s1a · Where it ran\n", draft.read_text())
            self.assertEqual(act(what="ask", p="C1.P1", was="", value="where was it run?")[0], 200)
            self.assertIn("  → S1 · cross-sectional\n  → C1.P2: where was it run?\n", draft.read_text())
            # a newer draft written under an open page (JL 261020: "why the content is not saved here?"): a change of
            # words still lands, in the newest draft, checked by its old words; a change placed by S ids is refused
            newer = section / "draft" / "S-Desk-Main-2-Methods-draft-v0.2.md"
            newer.write_text(draft.read_text())
            code, reply = act(what="para", p="C1.P1", was="The study design", value="The design")
            self.assertEqual((code, reply["file"]), (200, newer.name))
            self.assertIn("### C1.P1 · The design\n", newer.read_text())
            self.assertEqual(act(what="add", after="S1", p="C1.P1", value="x")[0], 409)
            newer.unlink()
            # JL 261020: "这里可不可以找一些 examples?" then "here I will expect it to be a frame of the sNN studio": no
            # example yet gives the prompt that finds them; a Studio topic naming the Task with reads/<pNN>/reading.yaml
            # opens as a frame onto its own drawing, and the rubric sets each paper's paragraphs beside ours
            self.assertIn("Copy prompt · find examples", html)
            topic = board / "studio" / "s26-methods-examples"
            (topic / "reads" / "p01-lee2025").mkdir(parents=True)
            (topic / "s26-methods-examples.md").write_text(
                "s26 · Methods examples (Ba-Desk-Main/S-Desk-Main-2-Methods)\n\n```yaml\nrelated:\n  papers:\n"
                "  - id: p01\n    item: Lee et al. 2025\n```\n")
            (topic / "s26-methods-examples.excalidraw").write_text('{"type": "excalidraw", "elements": []}')
            (topic / "reads" / "p01-lee2025" / "reading.yaml").write_text(
                "section:\n  name: Methods\n  key:\n  - 2 paragraphs · about 300 words\n"
                "logic:\n- role: method\n  text: 'P1 · Design first'\n  how:\n  - 'Size: about 120 words'\n")
            html = task_draft.draft_task_spaces(section, root, "1 · Plan")["Work Details"].html
            self.assertIn("📚 Examples · how 1 published papers write their Methods", html)
            self.assertIn('class=st-frame title="s26-methods-examples" data-src="/_excalidraw/?board=', html)
            self.assertIn("Lee et al. 2025", html)                               # the rubric's column
            self.assertIn("Design first", html)                                  # its paragraph, beside ours
            # JL 261020: "every time I copy it, and I paste it to any session, it will trigger that session to work":
            # a Copy prompt ends with the Task's session (its face's `session:`, else its Job's)
            # JL 261020: one session per Task, shared by its steps, named for it ("j01jamaim-full-t01-intro"), never
            # its Job's; started under that name when it is not running yet
            self.assertIn('data-tail="Run this in the Claude session &quot;Paper-Demo: Ba-Desk-Main-S-Desk-Main-2-Methods'
                          '&quot;; start it if it is not running."', html)
            (section / "S-Desk-Main-2-Methods.md").write_text("# S-Desk-Main-2-Methods · Methods\n\nsession: Sec-Methods\n")
            html = task_draft.draft_task_spaces(section, root, "1 · Plan")["Work Details"].html
            self.assertIn('data-tail="Run this in the Claude session &quot;Sec-Methods&quot;; start it if it is not '
                          'running."', html)

    def test_each_step_tab_carries_its_own_runs(self):
        # b16 s13 Decided 4-5 (JL 261007), then b32 s41: the Report's tabs are for reading and carry no run types;
        # Questions asks and answers; each Work step has its own run cards
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            board = root / "Project-X/paper/Paper-Demo"
            section = board / "Ba-Desk-Main/S-Desk-Main-1-Intro"
            (section / "reports" / "q01_why").mkdir(parents=True)
            (board / "board.md").write_text("# Paper\n\ndialect: paper\n")
            (section / "S-Desk-Main-1-Intro.md").write_text("# Intro\n")
            (section / "reports/q01_why/q01_why.md").write_text("# Why this order?\n\nanswer-status: open\n")
            theme = frame.themes()["paper"]

            def runs(sub, space):
                spaces = json.loads(frame.frame_json(theme, root, section, sub))["spaces"]
                return next(s["run_types"] for s in spaces if s["name"] == space)
            self.assertEqual(runs("Table", "Audience Report"), [])
            self.assertEqual(runs("2 · Write", "Audience Report"), [])
            page = frame.render(theme, root, section, "Audience Report", "Table")
            self.assertNotIn("read only: its content is changed", page)   # no note in the Runs panel (JL 261008)
            self.assertEqual(runs("Questions", "Audience Report"), ["run-ask-<qNN>", "run-report-<qNN>"])   # named by its Run
            self.assertEqual(runs("Studio", "Work Details"), ["run-draw-<sNN>"])
            self.assertEqual(runs("1 · Plan", "Work Details"), ["run-structure-<slug>"])
            self.assertEqual(runs("2 · Write", "Work Details"), ["run-scratch-<target>", "run-section-<slug>"])
            self.assertEqual(runs("4 · Display", "Work Details"), ["run-display-<slug>"])
            self.assertEqual(runs("5 · Revise", "Work Details"),
                             ["run-section-<slug>", "run-paragraph-<slug>", "run-revise-<target>"])
            self.assertIn("run-citation-<slug>", runs("3 · Evidence", "Work Details"))
            self.assertEqual([r.split("-")[:2] for r in runs("", "Description")], [["run", "face"]])
            spaces = frame.spaces_for(theme, "Task", section, root, "Questions")
            self.assertIn("Why this order?", spaces["Audience Report"].html)
            self.assertIn("Rubric", task_draft.draft_task_spaces(section, root, "1 · Plan")["Work Details"].html)

    def test_the_evidence_step_lists_every_open_point_beside_its_sentence(self):
        # JL 261021 ("我们的 evidence 该怎么把这些不确定的 ... 都加上去"): each ⟦…⟧ in §3 and each §1 point with
        # `Evidence: none` is an OPEN <n> row beside its sentence, card or no card, and all of them in one fold
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            task = root / "Project-X/work/b01_topic/j01_job/t01_intro"
            (task / "draft").mkdir(parents=True)
            (task / "t01_intro.md").write_text("# t01_intro · Intro\n\nfolder-kind: task\ntask-type: draft\n")
            (task / "draft" / "t01_intro-draft-v0.1.md").write_text(
                "# Intro · draft v0.1\n\napproved: ✅\n\n## 1 · Structure\n\n### C1.P1 · Why\n- B1 · S1 · [Stakes] Why\n"
                "  Evidence: none · paper-owned reasoning, hedged\n- B2 · S2 · [Uptake] How many\n\n"
                "## 3 · Draft\n\n### C1.P1 · Why\n- B1 · S1 · It may matter.\n"
                "- B2 · S2 · About 1 in 6 adults ⟦check: KFF poll, 2024⟧ ask, ⟦pending T4: ⟦x⟧ times chance⟧.\n")
            html = task_draft.draft_task_spaces(task, root, "3 · Evidence")["Work Details"].html
            self.assertIn("OPEN 1</b></td><td style=\"width:1%;padding:5px 8px 5px 0\">⚪", html)    # S1: no evidence
            self.assertIn("to check</span> · <span class=mut>KFF poll, 2024", html)                     # S2: a source to verify
            self.assertIn("waits on a Run</span> · <span class=mut>T4: ⟦x⟧ times chance", html)           # one nested mark
            self.assertIn("<b>❓ Open points</b>", html)              # no tally in the label (AGENTS.md § Page words)
            self.assertIn("→ next", html)                       # no cards.yaml yet: the step's prompt makes them

    def test_a_draft_tasks_display_step_sets_each_display_beside_the_sentence_that_calls_it(self):
        # b34 s41 Open 1 (JL 261020: "a new display view after the 3 - Evidence?"): 4 · Display reads display/Display<n>-*/,
        # links a unit to the sentences that call it by its label (Table 1), and lists a call with no unit, not made yet
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            task = root / "Project-X/work/b01_topic/j01_job/t03_results"
            (task / "draft").mkdir(parents=True)
            (task / "t03_results.md").write_text("# t03_results · Results\n\nfolder-kind: task\ntask-type: draft\n")
            (task / "draft" / "t03_results-draft-v0.1.md").write_text(
                "# Results · draft v0.1\n\napproved: ✅\n\n## 1 · Structure\n\n### C1.P1 · Sample\n- B1 · S1 · Sample\n\n"
                "## 3 · Draft\n\n### C1.P1 · Sample\n- B1 · S1 · We drew 12 queries (Table 1).\n"
                "- B2 · S2 · Overlap was low (Figure 1).\n")
            unit = task / "display" / "Display1-queries"
            unit.mkdir(parents=True)
            (unit / "README.md").write_text("# Display1-queries · Table 1\n\nkind: table\nlabel: Table 1\nclaim: the queries\n")
            html = task_draft.draft_task_spaces(task, root, "4 · Display")["Work Details"].html
            self.assertIn("🖼 Stage 4 · Display", html)
            self.assertIn('data-s="s1"><b style="color:#e8590c">DISPLAY 1</b> · Table 1 · queries', html)
            self.assertIn("planned, not built", html)                                 # no assets yet
            self.assertIn('<b style="color:#e8590c">Figure 1</b> <span class=st>⬜ not made yet', html)

    def test_a_jobs_work_card_shows_each_draft_tasks_seven_steps(self):
        # b32 s41 (JL 261020: "apply it to" the version's Work): each draft Task's card carries its seven steps, a
        # chip each, a link each into that tab; the ✎ Write button opens the Task's Work at the step that waits
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            job = root / "Project-X/work/b01_topic/j01_job"
            (job / "t01_note" / "draft").mkdir(parents=True)
            (job / "t01_note" / "t01_note.md").write_text("# t01_note · Note\n\nfolder-kind: task\ntask-type: draft\n")
            (job / "t01_note" / "draft" / "t01_note-draft-v0.1.md").write_text(
                "# Note · draft v0.1\n\napproved: ⬜\n\n## 1 · Structure\n\n### C1.P1 · Why\n- B1 · S1 · [Need] Why\n")
            (job.parent / "board.md").write_text("# Topic\n")
            tree = frame.work_tree("Job", job, root, frame.VANILLA)
            self.assertIn("work-steps", tree)
            for step in task_draft.STEPS:
                self.assertIn(f">{step} ", tree.replace("&amp;", "&"))
            self.assertIn("✍ sign", tree)                                       # §1 written, not signed
            self.assertIn("sub=1+%C2%B7+Plan", tree)                            # a link into the Task's tab
            label, link = frame.task_action(job / "t01_note", root)
            self.assertEqual(label, "✎ Write")
            self.assertIn("space=Work+Details", link)

    def test_a_comment_on_a_paragraph_sits_at_its_heading(self):
        # JL 261021: "比如说这个 paragraph 也可以加 comments 呢？" A comment on C2.P10 is saved like a sentence's and its
        # card carries data-p, so it aligns to the paragraph heading (which gets its own +)
        from live import draft_steps
        c = {"n": "6", "target": "C2.P10", "state": "open", "quote": "", "thread": [("Note", "2026-10-21 23:40", "why")]}
        html = draft_steps._note_card(c, [])
        self.assertIn('data-s="C2.P10"', html)
        self.assertIn('data-p="C2.P10"', html)
        self.assertNotIn("data-p", draft_steps._note_card({**c, "target": "S4"}, []))
        self.assertIn("h4[data-p]", draft_steps.NOTES_JS)

    def test_a_card_on_a_whole_part_sits_at_its_first_paragraph(self):
        # JL 261021, of a `Section question · C2 · …` card above the text: "我想知道它是不是应该也当成一个 card 之类的，
        # 放到右边去？" It goes on the right with the others, at C2's first paragraph, before that paragraph's cards
        from live import draft_steps
        d = {"text": [("Draft", "### C1.P1 · Question\n- B1 · S1 · One.\n\n### C2.P4 · Importance\n- B1 · S4 · Two.\n"
                                "- B2 · S5 · Three.\n")]}
        self.assertEqual(draft_steps._first_para("C2", d), "C2.P4")
        whole, para, own = (draft_steps._reading_key(h, d) for h in
                            ("Section question · C2 · room", "Review · C2.P4 · flow", "Edit · S4 · word"))
        self.assertLess(draft_steps._reading_key("Edit · S1 · word", d), whole)
        self.assertLess(whole, para)
        self.assertLess(para, own)
        html = draft_steps._revise_card("Section question · C2 · room", {"why": "w", "state": "proposed"}, "t", "p", "C2.P4")
        self.assertIn('data-p="C2.P4"', html)

    def test_a_value_evidence_card_reads_as_the_sentence_says_it(self):
        # JL 261021, of the Abstract beside the Introduction: a value card's line shows "1,983 requests", the words in
        # the sentence, never an item id such as "VALUE 1.1 queries in fold00"; a pending one says what it still needs
        from live import draft_steps
        c = {"kind": "value", "label": "VALUE 1", "source": "b03.j02.t03"}
        it = {"run": "r11", "anchor": ["1,983 requests", "sent 1,983 requests"], "what": "queries in fold00", "state": "have"}
        need = {"need": "overlap between agents, from a Run", "state": "need"}
        html = draft_steps._ev_side_card("S2", [(c, it, 1), (c, need, 2)], None, "In this study of 1,983 requests, ...")
        peek = html.split("rv-peek")[1].split("</span>")[0]
        self.assertIn("1,983 requests", peek)
        self.assertNotIn("sent 1,983", peek)
        self.assertNotIn("VALUE 1.1", peek)
        self.assertIn("pending: overlap between agents", peek)

    def test_an_anchor_is_boxed_only_in_the_sentences_its_item_names(self):
        # MISQ t05 (261022): S36a's anchor "1 percent" was boxed inside "1.41 percent" in S5b and "26.91 percent" in S4,
        # and S36a's "88.5" carried its card name onto S5b's 88.5; a sentence boxes only its own items' anchors
        from live import draft_steps
        ev = {"cards": [{"kind": "value", "label": "VALUE 1", "items": [
                  {"for": ["5b"], "anchor": ["1.41", "88.5"], "state": "have"}]},
                        {"kind": "value", "label": "VALUE 2", "items": [
                  {"for": ["36a"], "anchor": ["1 percent", "88.5"], "state": "have"}]}]}
        marks = draft_steps._marks(ev)
        s5b = draft_steps._sentence("B2 · S5b · from 1.41 percent in cancer to 88.5 in LBP", marks)
        s36a = draft_steps._sentence("B4 · S36a · about 1 percent in cancer (mean 88.5)", marks)
        self.assertNotIn("VALUE 2", s5b)
        self.assertIn("VALUE 1", s5b)
        self.assertIn("VALUE 2", s36a)
        self.assertNotIn("VALUE 1", s36a)
        self.assertEqual(s5b.count("<mark"), 2)

    def test_a_revise_card_is_accepted_rejected_or_edited_in_place(self):
        # b32 s41-D31/D32 (JL 261020: "我想要那种可以交互的感觉"): 5 · Revise shows the cards by pass with their buttons;
        # card_act writes only the card's State (or its Expected), and refuses a card that changed since it was shown
        from live import draft_steps
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            task = root / "Project-X/work/b01_topic/j01_job/t01_note"
            (task / "draft" / "records").mkdir(parents=True)
            (task.parents[1] / "board.md").write_text("# Topic\n")
            (task / "t01_note.md").write_text("# t01_note · Note\n\nfolder-kind: task\ntask-type: draft\n")
            (task / "draft" / "t01_note-draft-v0.1.md").write_text(
                "# Note · draft v0.1\n\n## 3 · Draft\n\n### C1.P1 · Why\n- B1 · S1 · The problem grows.\n")
            cards = task / "draft" / "records" / "t01_note-revise.md"
            cards.write_text("# t01_note · Revise cards\n\n## Pass 1 · 261020 · on draft v0.1\n\n### Edit · S1 · a number\n\n"
                             "Why: open on a number\nOriginal: The problem grows.\nExpected: The problem grows by 10%.\n"
                             "State: proposed\n")
            html = task_draft.draft_task_spaces(task, root, "5 · Revise")["Work Details"].html
            self.assertIn('data-pass="Pass 1 · 261020 · on draft v0.1"', html)   # the pass's title went 261115; its cards keep it
            self.assertIn("data-card-act=confirm", html)                         # a choice, then Confirm (JL 261021)
            self.assertIn("data-card-act=reject>Discard</button>", html)   # Discard, not a drop-it option (JL 261115)
            self.assertIn('<li data-s="s1"', html)                               # a card lights its sentence
            rel = task.relative_to(root).as_posix()
            ask = {"task": rel, "pass": "Pass 1 · 261020 · on draft v0.1", "card": "Edit · S1 · a number"}
            self.assertEqual(draft_steps.card_act(root, {**ask, "state": "accepted", "was": "proposed"})[0], 200)
            # ✓ Accept writes the words into the Draft at once (JL 261114), so the card reads written
            self.assertIn("State: written · ", cards.read_text())
            self.assertIn("- B1 · S1 · The problem grows by 10%.", (task / "draft" / "t01_note-draft-v0.1.md").read_text())
            self.assertEqual(draft_steps.card_act(root, {**ask, "state": "rejected", "was": "proposed"})[0], 409)
            code, res = draft_steps.card_act(root, {**ask, "state": "accepted", "was": "written",
                                                    "expected": "The problem grows by 12%."})
            self.assertEqual((code, "<ins" in res["change"]), (200, True))
            self.assertIn("Expected: The problem grows by 12%.", cards.read_text())
            # its Original is no longer the sentence, so the edited words wait on the card and the Draft keeps 10%
            self.assertIn("- B1 · S1 · The problem grows by 10%.", (task / "draft" / "t01_note-draft-v0.1.md").read_text())
            self.assertEqual(draft_steps.card_act(root, {**ask, "task": "../..", "state": "accepted"})[0], 400)
            self.assertEqual(draft_steps.card_act(root, {**ask, "state": "accepted"}, read_only=True)[0], 403)

    def test_a_comment_on_a_sentence_is_answered_by_a_pass_and_closed_by_its_person(self):
        # JL 261021 ("我选中一个句子 ... 点个加号就能加注释 ... 放到 Revise 的那一栏里面"; "你的 change 怎么跟我的 comments
        # 一起来做交互"): note_act writes the comment, a pass's card names it (Answers:), the person closes it
        from live import draft_steps
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            task = root / "Project-X/work/b01_topic/j01_job/t01_note"
            (task / "draft" / "records").mkdir(parents=True)
            (task.parents[1] / "board.md").write_text("# Topic\n")
            (task / "t01_note.md").write_text("# t01_note · Note\n\nfolder-kind: task\ntask-type: draft\n")
            (task / "draft" / "t01_note-draft-v0.1.md").write_text(
                "# Note · draft v0.1\n\n## 3 · Draft\n\n### C1.P1 · Why\n- B1 · S1 · The problem grows.\n"
                "- B2 · S2 · It costs money.\n")
            rel = task.relative_to(root).as_posix()
            notes = task / "draft" / "records" / "t01_note-comments.md"
            code, res = draft_steps.note_act(root, {"task": rel, "act": "add", "s": "S2", "quote": "costs",
                                                    "text": "how  much?"})
            self.assertEqual((code, res["n"], res["state"]), (200, "1", "open"))
            self.assertIn("### Comment 1 · s2\nQuote: costs\nState: open\n- Note · ", notes.read_text())
            self.assertEqual(draft_steps.note_act(root, {"task": rel, "act": "add", "s": "S9; rm", "text": "x"})[0], 400)
            # 🤔 on selected words (JL 261115): an issue saved at once, no reason typed, read by the Section session
            code, res = draft_steps.note_act(root, {"task": rel, "act": "add", "s": "S1", "quote": "grows", "text": "🤔 issue"})
            self.assertEqual(code, 200)
            self.assertRegex(notes.read_text(), r"### Comment 2 · s1\nQuote: grows\nState: open\n- Note · [^\n]*: 🤔 issue\n")
            self.assertEqual(draft_steps.note_act(root, {"task": rel, "act": "delete", "n": "2"})[1]["html"], "")
            draft_steps.note_act(root, {"task": rel, "act": "add", "s": "S1", "text": "fine"})
            self.assertEqual(draft_steps.note_act(root, {"task": rel, "act": "delete", "n": "2"})[1]["html"], "")
            # a pass answers it: a card that names it, a Reply line, State: answered
            (task / "draft" / "records" / "t01_note-revise.md").write_text(
                "# t01_note · Revise cards\n\n## Pass 1 · 261021 · on draft v0.1\n\n### Edit · S2 · the cost\n\n"
                "Why: your comment\nAnswers: Comment 1\nOriginal: It costs money.\nExpected: It costs $5 a year.\n"
                "State: written\n")
            notes.write_text(notes.read_text().replace("State: open", "State: answered")
                             + "- Reply · 2026-10-21 15:00: S2 now gives the cost (card S2).\n")
            html = task_draft.draft_task_spaces(task, root, "5 · Revise")["Work Details"].html
            self.assertIn('data-n="1" data-s="s2"', html)
            self.assertIn("<b>AI</b>", html)                                      # the pass's reply, marked AI
            self.assertIn("💬 answers Comment 1", html)                        # the card names the comment
            self.assertIn('data-card="Edit · S2 · the cost">Edit · S2 · the cost</a>', html)                       # and the comment its card
            self.assertIn("how much?", html)                                     # its thread, the person's note
            self.assertIn("S2 now gives the cost (card S2).", html)               # and the pass's reply
            self.assertLess(html.index('data-n="1" data-s="s2"'), html.index('data-card="Edit · S2 · the cost'))
            self.assertEqual(draft_steps.note_act(root, {"task": rel, "act": "delete", "n": "1"})[0], 409)
            self.assertEqual(draft_steps.note_act(root, {"task": rel, "act": "done", "n": "1", "was": "open"})[0], 409)
            code, res = draft_steps.note_act(root, {"task": rel, "act": "done", "n": "1", "was": "answered"})
            self.assertEqual((code, res["state"]), (200, "done"))
            code, res = draft_steps.note_act(root, {"task": rel, "act": "reply", "n": "1", "text": "and per patient?"})
            self.assertEqual((code, res["state"]), (200, "open"))
            self.assertEqual(notes.read_text().count("- Note · "), 2)
            self.assertEqual(draft_steps.note_act(root, {"task": rel, "act": "add", "s": "S1", "text": "x"},
                                                  read_only=True)[0], 403)

    def test_an_edit_card_offers_options_and_a_person_picks_one(self):
        # JL 261021 ("可以用 A、B、C 几个不同的方法去修改，propose 一些选项"): a card's Option lines show with Use buttons;
        # card_act with an option writes its words as Expected, the letter as Chosen, and the card accepted
        from live import draft_steps
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            task = root / "Project-X/work/b01_topic/j01_job/t01_note"
            (task / "draft" / "records").mkdir(parents=True)
            (task.parents[1] / "board.md").write_text("# Topic\n")
            (task / "t01_note.md").write_text("# t01_note · Note\n\nfolder-kind: task\ntask-type: draft\n")
            (task / "draft" / "t01_note-draft-v0.1.md").write_text(
                "# Note · draft v0.1\n\n## 3 · Draft\n\n### C1.P1 · Why\n- B1 · S1 · The problem grows by 10%.\n")
            cards = task / "draft" / "records" / "t01_note-revise.md"
            cards.write_text("# t01_note · Revise cards\n\n## Pass 2 · 261021 · on draft v0.1\n\n### Edit · S1 · the number\n"
                             "Why: two ways (R2)\nOriginal: The problem grows.\nExpected: The problem grows by 10%.\n"
                             "Option A (the number first): The problem grows by 10%.\n"
                             "Option B (the cause first): Costs make the problem grow.\nChosen: A\n"
                             "State: written · 2026-10-21 17:00\n")
            html = task_draft.draft_task_spaces(task, root, "5 · Revise")["Work Details"].html
            self.assertIn('data-opt="B"', html)                                   # every option listed (JL 261021); the chip went 261113
            self.assertIn('value="B"', html)
            self.assertIn('<label class="rv-choice sel" data-opt="A"', html)
            self.assertNotIn('data-opt="drop"', html)                     # Discard replaces the drop-it option
            self.assertNotIn("Show the 1 finished", html)                       # a choice still open is not finished
            ask = {"task": task.relative_to(root).as_posix(), "pass": "Pass 2 · 261021 · on draft v0.1",
                   "card": "Edit · S1 · the number", "was": "written", "state": "accepted",
                   "expected": "Costs make the problem grow.", "option": "B"}
            self.assertEqual(draft_steps.card_act(root, ask)[0], 200)
            text = cards.read_text()
            self.assertIn("Expected: Costs make the problem grow.", text)
            self.assertIn("Chosen: B", text)
            self.assertIn("State: accepted · ", text)

    def test_a_display_shows_under_the_sentence_that_calls_it(self):
        # JL 261021 ("如果我们有图片或者表格的话 ... PNG TO EMBED UNDER THAT SENTENCE"): a unit's preview.png sits under the
        # first sentence that calls it, in Write, Evidence, Display and Revise alike; an unbuilt one says so
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            task = root / "Project-X/work/b01_topic/j01_job/t01_note"
            (task / "draft" / "records").mkdir(parents=True)
            (task.parents[1] / "board.md").write_text("# Topic\n")
            (task / "t01_note.md").write_text("# t01_note · Note\n\nfolder-kind: task\ntask-type: draft\n")
            (task / "draft" / "t01_note-draft-v0.1.md").write_text(
                "# Note · draft v0.1\n\n## 3 · Draft\n\n### C1.P1 · Why\n- B1 · S1 · The problem grows.\n"
                "- B2 · S2 · Figure 1 shows it; Table 2 counts it.\n- B3 · S3 · Figure 1 again.\n")
            unit = task / "display" / "Display1-growth"
            unit.mkdir(parents=True)
            (unit / "README.md").write_text("# Display1-growth · Figure 1\n\nshown as: Figure 1\nclaim: It grows.\n")
            (unit / "preview.png").write_bytes(b"\x89PNG\r\n\x1a\n")
            (task / "draft" / "records" / "t01_note-revise.md").write_text(
                "# t01_note · Revise cards\n\n## Pass 1 · 261021 · on draft v0.1\n\n### Edit · S1 · x\nWhy: y\n"
                "Original: a\nExpected: b\nState: proposed\n")
            for step in ("5 · Revise", "4 · Display"):
                html = task_draft.draft_task_spaces(task, root, step)["Work Details"].html
                at = html.index('<li data-s="s2"')                     # ids are written s (M-D01)
                self.assertLess(at, html.index('<li class="disp-embed"><figure>'), step)      # under S2, not S3
                self.assertLess(html.index('<li class="disp-embed"><figure>'), html.index('<li data-s="s3"'), step)
                self.assertIn("display/Display1-growth/preview.png", html)
                self.assertIn("<b>Table 2</b> · no unit in display/ yet", html)
            html = task_draft.draft_task_spaces(task, root, "5 · Revise")["Work Details"].html
            self.assertNotIn("data-cards-kind=", html)                           # no kind chips (JL 261113)
            self.assertNotIn("data-cards-all=accept", html)                      # no Accept all (JL 261021)
            self.assertNotIn("data-cards-done", html)                            # no Show finished

    def test_the_review_report_scores_each_sentence(self):
        # JL 261021 ("让 AI 也来评评每句话，作为一个 reviewer"): a report's `Sentences:` lines become a table, one row each
        from live import draft_steps
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "t01_note-revise.md"
            path.write_text("# t01_note · Revise cards\n\n## Pass 2 · 261021 · on draft v0.1\n\n### Revise review report\n"
                            "Verdict: two joins are weak.\nReadability: NEEDS WORK · 7/10 · long · Fix: split\n"
                            "Sentences:\n- S1 · logic 9/10 · read 9/10 · link: opens the paragraph, carried · none · Fix: none\n"
                            "- S2 · logic 6/10 · read 8/10 · link: cause, weak · the colon promises a cause, the rest gives a "
                            "cost · Fix: It costs $5 a year.\nFlow P1: S1 the need → S2 its cost · weakest join S1 to S2\n")
            html = draft_steps._review_report(path)
            self.assertIn("Each sentence, in its context:", html)
            self.assertIn("logic ★7.5 · read ★8.5/10 · 1 of 2 pass (8 or more on both, no broken link)", html)
            # beside the text, a sentence with a problem gets the reviewer's card; one with none gets no card
            task = Path(tmp) / "Project-X/work/b01_topic/j01_job/t01_note"
            (task / "draft" / "records").mkdir(parents=True)
            (task.parents[1] / "board.md").write_text("# Topic\n")
            (task / "t01_note.md").write_text("# t01_note · Note\n\nfolder-kind: task\ntask-type: draft\n")
            (task / "draft" / "t01_note-draft-v0.1.md").write_text(
                "# Note · draft v0.1\n\n## 3 · Draft\n\n### C1.P1 · Why\n- B1 · S1 · The need.\n- B2 · S2 · It costs.\n")
            (task / "draft" / "records" / "t01_note-revise.md").write_text(path.read_text())
            html = task_draft.draft_task_spaces(task, Path(tmp), "5 · Revise")["Work Details"].html
            # every sentence gets its Logic card beside it, and each paragraph its flow (JL 261021: "logic comments ...
            # 应该是放到右边的")
            self.assertIn('class="rv-card rv-rev" data-s="s2" data-state="review"', html)   # its ★ card
            self.assertIn('class="rv-card rv-rev" data-s="s1" data-state="review"', html)
            self.assertIn("It costs $5 a year.", html)
            self.assertIn("The logic needs work", html)                     # the link said in plain words (261113)
            self.assertIn("✂ weakest join", html)                            # drawn between S1 and S2 (JL 261115)
            self.assertIn('data-p="C1.P1"', html)
            self.assertNotIn("data-cards-kind=", html)                          # no filter chips (JL 261113)
            # an older pass's line has one score
            path.write_text(path.read_text().split("Sentences:")[0] + "Sentences:\n- S1 · 6/10 · link: weak · odd · Fix: X.\n")
            self.assertIn("read ★6.0/10 · 0 of 1 pass (8 or more, no broken link)", draft_steps._review_report(path))

    def test_a_theme_may_add_its_own_views_after_the_pages(self):
        # b16 s13 (JL 261007): paper adds Reviews after Table · Reading · Questions; the Space stays the
        # theme's, so the base's extra Page-view tabs do not come back and its run types are kept as set
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            section = root / "Project-X/paper/Paper-Demo/Ba-Desk-Main/S-Desk-Main-1-Intro"
            section.mkdir(parents=True)
            (section.parents[1] / "board.md").write_text("# Paper\n\ndialect: paper\n")
            (section / "S-Desk-Main-1-Intro.md").write_text("# Intro\n")

            def spaces(level, folder, root, sub):
                out = task_draft.draft_task_spaces(folder, root, sub)
                ar = out["Audience Report"]
                out["Audience Report"] = frame.Space(html=ar.html, open=ar.open, run_types=ar.run_types,
                                                     subspaces=ar.subspaces + ("Reviews",))
                return out
            theme = frame.Theme(name="paper", label="Paper", spaces=spaces)
            ar = frame.spaces_for(theme, "Task", section, root)["Audience Report"]
            self.assertEqual(ar.subspaces, task_draft.DRAFT_TASK_SUBS["Audience Report"] + ("Reviews",))
            self.assertEqual(ar.run_types, ())
            self.assertTrue(frame.lays_out_page("Audience Report", ar.subspaces))
            self.assertFalse(frame.lays_out_page("Audience Report", ("Reviews", "Table")))

    def test_a_draft_task_type_opens_the_draft_layout_in_any_theme(self):
        # b32 s03 (JL 261014): the face's `task-type: draft` picks the base's draft layout, whatever the theme;
        # another type keeps the theme's (here vanilla) layout, and a theme's own Space goes on top
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            job = root / "Project-X/work/b01_topic/j01_job"
            for name, kind in (("t01_note", "draft"), ("t02_data", "data")):
                (job / name).mkdir(parents=True)
                (job / name / f"{name}.md").write_text(f"# {name}\n\nfolder-kind: task\ntask-type: {kind}\n")
            (job.parent / "board.md").write_text("# Topic\n")
            self.assertEqual((frame.task_type(job / "t01_note"), frame.task_type(job / "t02_data")), ("draft", "data"))
            draft = frame.spaces_for(frame.VANILLA, "Task", job / "t01_note", root)
            data = frame.spaces_for(frame.VANILLA, "Task", job / "t02_data", root)
            self.assertEqual(draft["Work Details"].subspaces, task_draft.DRAFT_TASK_SUBS["Work Details"])
            self.assertNotEqual(data["Work Details"].subspaces, task_draft.DRAFT_TASK_SUBS["Work Details"])
            mine = frame.Space(html="<p>mine</p>")
            themed = frame.spaces_for(frame.Theme(name="t", spaces=lambda *a: {"Idea Studio": mine}), "Task",
                                      job / "t01_note", root)
            self.assertEqual(themed["Audience Report"].subspaces, task_draft.DRAFT_TASK_SUBS["Audience Report"])
            self.assertEqual(frame.task_action(job / "t01_note", root)[0], "✎ Write")
            self.assertIsNone(frame.task_action(job / "t02_data", root))
            # the older `page-type:` alone no longer marks a draft (s03-D04, 261015): the face says task-type
            (job / "t03_old").mkdir()
            (job / "t03_old" / "t03_old.md").write_text("# t03_old\n\npage-type: section\n")
            self.assertIsNone(frame.task_action(job / "t03_old", root))

    def test_the_page_view_embeds_without_its_own_chrome(self):
        from live.outline import EMBED_HTML
        self.assertIn("wb-embed", EMBED_HTML)
        for hidden in (".spaces", ".space-split>.runs-panel", ".draft-mode-switcher", "body>header"):
            self.assertIn(hidden, EMBED_HTML)


if __name__ == "__main__":
    unittest.main()
