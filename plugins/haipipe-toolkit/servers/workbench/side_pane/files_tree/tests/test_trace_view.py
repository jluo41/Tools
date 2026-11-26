"""Files › a trace: its files on the real tree, each with its state (side_pane/files_tree/trace_view.py)."""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from host_paths import bootstrap

bootstrap()

from live import trace_view  # noqa: E402

FACE = """---
title: trace view
date: 2026-11-25 11:05
aim: One aim.
closed: {closed}
plan:
  - do: add
    path: P/work/b01_x/new.py
    what: a new file
  - do: edit
    path: tools/skills/s/SKILL.md
    what: a part on traces
  - do: edit
    path: tools/servers/page.py
    what: the switch
changed:
  - tools/skills/s/SKILL.md
  - tools/servers/other.py
---
"""


class TraceViewTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = root = Path(self.tmp.name).resolve()
        (root / "env.sh").write_text("")
        self.block = root / "P" / "work" / "b01_x"
        (self.block / "trace" / "261125").mkdir(parents=True)
        (self.block / "board.md").write_text("# X\n")
        for rel in ("tools/skills/s/SKILL.md", "tools/servers/page.py", "tools/servers/other.py"):
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            (root / rel).write_text("x\n")
        self.face = self.block / "trace" / "261125" / "1105_trace_view.md"

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, closed=False):
        self.face.write_text(FACE.format(closed=str(closed).lower()))
        return trace_view.read(self.face)

    def test_an_open_trace_marks_planned_touched_and_left_out_files(self):
        rows = trace_view.states(self.write(), self.root)
        self.assertEqual({p: r["state"] for p, r in rows.items()}, {
            "P/work/b01_x/new.py": "plan", "tools/skills/s/SKILL.md": "edit",
            "tools/servers/page.py": "plan", "tools/servers/other.py": "off"})

    def test_the_tree_carries_the_marks_and_a_trace_button_lights_up_one_trace(self):
        self.write()
        (self.face.parent / "1200_later.md").write_text(
            "---\ntitle: later\naim: Two.\nplan:\n  - do: edit\n    path: tools/servers/page.py\n    what: again\n---\n")
        self.face.write_text(self.face.read_text() + "\n## Prompts\n\n- **11:05** make it so\n\n## Summary\n\nIt was done.\n")
        html = trace_view.render(self.block, self.root, "<div class=file-tree>TREE</div>")
        self.assertNotIn('data-trace-view', html)                         # one tree, no Files/Timeline switch
        self.assertIn('<div class=file-tree>TREE</div>', html)
        data = json.loads(html.split('class="tm-data">')[1].split('</script>')[0])
        self.assertEqual(data["m"]["P/work/b01_x/new.py"]["s"], "plan")
        self.assertEqual(data["m"]["P/work/b01_x/new.py"]["miss"], 1)    # still to create: a + row where it will sit
        self.assertEqual(data["m"]["tools/servers/other.py"]["s"], "off")
        self.assertEqual(data["m"]["tools/servers/page.py"]["t"], "later")   # two traces, one mark: the newer when they tie
        self.assertEqual(data["m"]["tools/servers/page.py"]["w"], "edit · again")
        self.assertNotIn('tm-chip', html)                                  # no chips row
        self.assertNotIn('trace-board', html)                              # no Timeline window
        self.assertIn('class="tm-mode" aria-pressed="false" title="Trace" aria-label="Trace"><svg', html)   # the highlighter
        self.assertIn('class="tm-metro-btn" aria-pressed="true" title="Metro map"', html)                 # the branching line
        self.assertIn('<div class="tm-metro"><svg class="tm-map">', html)                                # the metro beside the tree
        self.assertIn('<div class="tm-split" title="Drag; double-click to reset"></div><div class="tm-metro">', html)  # a drag line between them
        self.assertIn("localStorage.setItem('wb:tree-width'", html)                                           # its width is kept
        self.assertIn('data-step="-1" title="Earlier"', html)                                            # step through the columns
        self.assertIn('data-z="-1" title="Zoom out"', html)                                              # by day, by trace, close up
        self.assertIn('class="tm-only" aria-pressed="false" title="Tracked only"', html)                # hide what no trace touched
        self.assertIn('data-z="1" title="Zoom in"', html)
        self.assertIn('data-step="1" title="Later"', html)
        later, view = data["traces"]
        self.assertEqual((later["hm"], view["hm"], view["day"]), ("12:00", "11:05", "11-25"))
        self.assertEqual(view["s"]["tools/servers/other.py"], "off")                                      # a station per file
        self.assertEqual(view["s"]["tools/skills/s/SKILL.md"], "edit")
        self.assertNotEqual(later["c"], view["c"])                                                        # one colour per trace
        self.assertEqual(view["pr"], ["11:05 make it so"])                                               # the card: its prompts,
        self.assertEqual(view["sum"], "It was done.")                                                     # its summary
        self.assertIn('<div class="tm-card" hidden></div>', html)                                         # under the top row
        self.assertIn('class="tm-name" aria-expanded="false" hidden></button>', html)                     # the name between the icons
        self.assertNotIn("Open ↗", html.split('class="tm-bar"')[1].split("</div>")[0])
        self.assertEqual([t["k"] for t in data["traces"]], ["1200_later", "1105_trace_view"])   # newest first
        self.assertEqual(data["current"], "1200_later")                    # the newest open trace
        self.assertIn("tools/servers/other.py", data["traces"][1]["f"])     # a trace lights its plan and its changes
        self.assertIn("tm-hit", html)
        self.assertNotIn("tm-pick", html)                                   # no dropdown: a click on a trace file picks
        self.assertEqual(data["traces"][0]["p"], "P/work/b01_x/trace/261125/1200_later.md")
        self.assertEqual(data["m"]["tools/skills/s/SKILL.md"].get("o"), 1)   # an open trace opens the tree to its files
        self.assertIn("M[k].o", html)
        also = trace_view.render(self.block, self.root, "<div class=file-tree>TREE</div>", [self.block, self.root / "tools" / "skills"])
        part = also.split('class="files-part tm-also"')[1].split("</section>")[0]
        self.assertIn('<p class="files-where" title="tools/">tools/</p>', part)   # grouped under the folder they share
        self.assertIn("> servers/page.py</a>", part)                         # each file by its path below it
        self.assertEqual(trace_view._group("plugins/x/servers/w/a.py"), "plugins/x/servers/")
        self.assertEqual(trace_view._group("AGENTS.md"), "")
        self.assertNotIn("SKILL.md", part)                                  # under a part: marked in place
        self.assertNotIn("new.py", part)                                    # under the Block

    def test_a_closed_trace_keeps_only_files_not_committed(self):
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run(["git", "-C", str(self.root), "add", "tools/servers/page.py"], check=True)
        subprocess.run(["git", "-C", str(self.root), "-c", "user.name=t", "-c", "user.email=t@example.test",
                        "commit", "-qm", "x"], check=True)
        rows = trace_view.states(self.write(closed=True), self.root)
        self.assertNotIn("tools/servers/page.py", rows)          # committed: the trace no longer shows it
        self.assertEqual(rows["tools/skills/s/SKILL.md"]["state"], "done")
        self.assertEqual(rows["tools/servers/other.py"]["state"], "off")
        kept = trace_view.states(self.write(closed=True), self.root, keep=True)
        self.assertEqual(kept["tools/servers/page.py"]["state"], "kept")  # the timeline keeps history

    def test_the_skills_part_lists_the_shared_skills_and_the_metro_zooms_five_levels(self):
        from live import work_files
        tools = Path(__file__).resolve().parents[7]                       # the Tools-SPACE root
        block = tools / "blueprints/Project-Ladder/work/b17_theme_work"
        if block.is_dir():
            names = [p.name for p in work_files.own_skills(block, tools)]
            self.assertIn("hai-trace", names)                              # skills/0_utils/ in 3 · Skills
            self.assertIn("hai-stack", names)
        self.write()
        html = trace_view.render(self.block, self.root, "<div class=file-tree>TREE</div>")
        self.assertIn("LEVELS=['day','hour','half','trace','close']", html)   # by day, hour, half hour, trace, close up
        self.assertIn('grid-template-columns:var(--tm-left,fit-content(min(34%,260px))) 7px minmax(120px,1fr)', html)  # the metro takes the free width
        self.assertIn('function colw(', html)                             # its columns spread to fill it
        from live import work_files as wf
        self.assertIn('.file-tree li{padding:0;margin:0;', wf.TYPE_STYLE)     # rows as tight as they go
        self.assertIn('clearTimeout(onlyT)', html)
        self.assertIn('function keep(){return on&&cur?files():[];}', html)       # the funnel always means one trace
        self.assertIn('if(only&&!on&&T.length){mode(true,cur||T[0].k);', html)  # none picked: the newest
        self.assertIn('else if(d.open&&d.dataset.user!==key)d.open=false;', html)  # fold all, open only its path
        self.assertIn('function reach(){if(only||!on)return;', html)       # closed on load; no other trace reopens a folder
        self.assertIn('if(r.folder&&r.open)return;', html)                 # an open folder draws no stations
        self.assertIn('.file-tree li.tm-more>button{display:block;width:100%', html)  # ⋯ is a whole row
        self.assertNotIn('tm-hide', html)                                   # and hides nothing
        self.assertIn('class="tm-more"', html)                              # untouched files beside its files fold under ⋯
        self.assertIn('.tm-wrap>.file-tree{min-width:0;overflow-x:auto', html)  # the tree scrolls sideways, names whole                       # the filter's own timer: the marks timer cannot cancel it

    def test_a_traced_file_outside_the_owned_parts_is_also_touched(self):
        root = self.root
        for rel in ("plugins/k/skills/1_base/w/ui/SKILL.md", "plugins/k/skills/1_base/w/ui/ref/a.md"):
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            (root / rel).write_text("x\n")
        marks = {"plugins/k/skills/1_base/w/ui/ref/a.md": {}, "AGENTS.md": {}}
        html = trace_view.also_touched(marks, root, [self.block])
        self.assertIn("ui/ref/a.md", html)                  # a skill the page does not own: Also touched, not Skills
        self.assertFalse(hasattr(trace_view, "touched_homes"))

    def test_a_block_without_traces_keeps_the_bar(self):
        html = trace_view.render(self.block, self.root, "TREE")
        self.assertIn('class="tm-bar"', html)
        self.assertIn("disabled", html)
        self.assertTrue(html.endswith("TREE"))

    def test_another_blocks_trace_marks_only_this_blocks_files(self):
        work = self.root / "blueprints" / "P" / "work"
        here, there = work / "b11_here", work / "b17_there"
        (here / "a.md").parent.mkdir(parents=True)
        (here / "a.md").write_text("x\n")
        (there / "trace" / "261126").mkdir(parents=True)
        (there / "trace" / "261126" / "0900_move.md").write_text(
            "---\ntitle: move\ndate: 2026-11-26 09:00\naim: a\nclosed: false\nplan:\n"
            "  - {do: edit, path: blueprints/P/work/b11_here/a.md, what: w}\n"
            "  - {do: edit, path: tools/servers/page.py, what: w}\n---\n")
        self.assertEqual([f.stem for f, _ in trace_view.visiting(here, self.root)], ["0900_move"])
        self.assertEqual(trace_view.visiting(there, self.root), [])
        html = trace_view.render(here, self.root, '<div class="file-tree"></div>')
        data = json.loads(html.split('class="tm-data">')[1].split("</script>")[0])
        self.assertEqual(sorted(data["m"]), ["blueprints/P/work/b11_here/a.md"])   # page.py is b17's business


if __name__ == "__main__":
    unittest.main()
