Handoff · four more theme pages (insight, design, discovery, cowork) · 261108
===========================================================================

Paused on one computer to continue on another. Goal: each theme Block in `work/` (b11 insight, b12 design, b13 cowork,
b14 discovery) shows all of its theme's UI the way Theme: paper (b16), work (b17) and labeling (b15) do, and its own
page reads like Theme: paper's (Report, Work, Studio). Nothing below is committed by this session.

Where each theme stands
-----------------------

```text
theme      example (in Project-Ladder/)              ui lines  pages aligned        drawings (3x3)  walks   reviews
insight    insight/Insight-Example                   yes       yes                  yes (b11 j01)   yes     r01, r02 done (6 of 10 pass);
           + work/Prototype-b91-Example                                                                     r02 fixes done, r03 not run
design     design/Design-Example (3 Jobs)            yes       HALF (stopped)       not redrawn     no      none
discovery  discovery/b01_example_prior_work          yes       yes (work shape)     yes (b14 j01)   no      none
cowork     cowork/b01_example_data_request           yes       yes (work shape)     yes (b13 j01)   yes     r01 done (Block passes); r01 fixes
                                                                                                            done; r02 not run
```

Next, in order
--------------

1. **Design alignment, finish it.** Its agent was stopped mid-way in
   `plugins/haipipe-toolkit/servers/workbench-design/` (design_focus.py, design_views.py): the page code is changed
   and renders, but `pytest servers/workbench-design/tests` has 1 failing old test to update. The target list:
   MindMap at every level beside the design views (focus_page.py `theme.name == "design"` hook); a state word on every
   bar; no view's own 🙋 section (rows that wait become ⚙️ Process steps); Report keys without `report-`; side tabs, no
   counts; `view_of_item` and `VIEW_SKILLS` in design_focus.py; a Job face `goal: G01 · <name>` through
   design_ladder.py; the lettered parts the b12 drawings show (task_views.py coverage A1–A4, B1–B4, C1–C3).
2. **Theme pages read like paper's** (the person's 261108 "go ahead with 1 to 3"), for b11, b12, b13, b14:
   1. Answer each question in board.md ## Questions in its `reports/qNN_*/qNN_*.md` from what is now built
      (`answer-status: partial|answered`, a `state:` line, ## Opening, ## Content › 1 · Answer, and the skill or
      workbench change that settled it), as b16's reports are written.
   2. Record the decisions taken on Claude's lean as WAITING forms (collect.py new / check / build, my pick ticked) under
      `j0N_<theme>_workbench_pages/t01..t03`, at most 3 forms of at most 5 questions each:
      - **insight:**
        - a Prototype is insight's: its own Findings, Status, Delivery (releases), and Skills (/haipipe-insight)
        - inbox rows become ⚙️ Process steps
        - the Job Overall headline carries X01
        - Wisdom and Executive Tasks keep "By cut"
        - a Task's goal line is its ask
      - **design:**
        - three Jobs, one clock moved each
        - date-only placeholder signs
        - MindMap beside the design views
      - **discovery:**
        - the work shape plus Papers · Evidence Bib · Synthesis
        - a Task's parts sit in its Status
        - its headline is the synthesis
        - placeholder Paper Runs (`paper_result_build.py --placeholder`)
        - the example doubles as Paper-Example's discovery folder
      - **cowork:**
        - the work shape plus People · Messages · Next move
        - a no-Task Job reads its own state; its Status is its timeline; its MindMap maps it
        - Delivery is what was sent
        - a waiting item shows once per page
        - roles only
        - a Task only for a document written in rounds
   3. Group each theme's Studio like paper's: `_studio_groups.txt` with Structure, Levels, Run and Skill, Guide,
      Block UI, Job UI, Task UI, and each topic face's **Tags:** line.
3. **Shared hooks still asked for** (servers/workbench/focus_page.py):
   - **Insight's Prototype:**
     - `work_process` uses `prototype_process(folder, root, level, view)`
     - `prototype_lead(...)` sits above Status and Findings
     - `parts_mindmap` prefers `prototype_map_branches` on a release even with Tasks
     - optionally, a Board's own `delivery_tabs`
     The insight side is written already (servers/workbench-insight/insight_prototype.py).
   - **Cowork:**
     - a Task's Work gets a ⚙️ Process band
     - a Job's state on the Block MindMap
4. **Final review round per theme** (the person asked for speed, 261108):
   - at most 2 rounds per theme; walks once, before the final round
   - light reviews: about 6 screenshots per kind, the rest from the HTML
   - drawings at the end
   - insight's r03 is its last; cowork's r02 its last; design and discovery get r01 and r02
5. **Leftovers on paper, work and labeling** (fixes only, no new round): labeling Studio pictures 404; the
   Introduction's bibliography pop-out; "Open the plan to sign"; phone tables; "replied, text not changed"; the
   Board's Idea and Story maps.
6. **Close-out:**
   - tests: servers/workbench, workbench-paper, -insight, -design, -discovery, -cowork, -labeling, -work
   - prototype_coverage on all seven examples
   - `git grep -nE '/(Users|home)/[^/]+/'` on changed files
   - the "JL <date>" comments the mind-map renderer and new_topic.py's builder template copy into generated files
   - skill CHANGELOGs

How to run it
-------------

- **Workbenches.** Start each from the SPACE root:
  `.venv/bin/python Tools/plugins/haipipe-toolkit/servers/_host/serve.py --root . --port 5602 --no-terminal --daemon <log>`
  (the SPACE), and the same with `--root Tools --port 5623` (Tools alone, for walks and reviews). Poll a
  `/_board/workbench?layout=focus&path=…` route, never `/`. The theme pages are at
  `path=Tools/blueprints/Project-Ladder/work/b1N_theme_<theme>` (`group=ui-block|ui-job|ui-task` for the examples).
- **Coverage:** `haipipe-ui/scripts/prototype_coverage.py <origin> <example path>`.
- **Walks:** `haipipe-ui/scripts/walk_all.py <theme Block> --max-frames 60` (port 5623).
- **Reviews:** one fresh reviewer per level, the 12 rubrics of haipipe-ui SKILL.md "Design loop", files
  `<theme Block>/review/<folder>-s2-rNN.md` (first line `page http://127.0.0.1:5623/...`). Pass = every rubric ≥ 7
  and mean ≥ 8.
- **Rules kept throughout:**
  - generators only for any result, receipt, delivery or form
  - placeholders only, roles not names
  - a placeholder decision or sign says it is a placeholder
  - each theme's code in its own servers/workbench-<theme>/
- **Known baseline test failures** (not from this work):
  - workbench-cowork: `test_a_reports_drawing_lives_in_its_report_folder`
  - workbench-labeling: 2 failures
