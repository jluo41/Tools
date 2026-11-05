### The paper Board's Report and Work: six views, A to F

A paper Board's Report and Work show the paper's four layers as views, one button each, in this order, with the same
letters on both (b16 s32-D12, s33-D02). Idea (the many directions) and Story (the one chosen) are two views, s32-D44; Data flow and Paper flow one view, Data + Paper Plan (s32-D28, s32-D29, JL 261104). Venue is inside Story (s32-D12); Displays is its own view, after Evidence and
before Writing (s32-D26). A view shows only when the Board has its
part: no ideation topic, no Idea view; no Story topic, no Story view; no evidence Job, no Evidence view.

```text
idea      A Idea                                           the idea topic, for the many directions: Studio, Directions as left tabs, Theory
story     B Story                                          the one direction chosen: Studio, Direction, Pitch, Theory, Research Questions, Stakes and evidence, Related (related/related.md), Venues (venues/<venue>/call.md), Story by Section
plan      B Data + Paper Plan                              1 · Data flow, 2 · Paper flow: each topic's mind map, the window's full width
explore   C Support blocks                                 the work and discovery Blocks its pages name, as folder trees
evidence  D Evidence                                       j02 values · j03 citations, as side tabs
          E Displays                                       1 · the display plan against the venue, 2 · j01's displays, each its preview.pdf
writing   F Writing                                        each jNN_writing_v<MMDD>_<desk>: its Sections, the assembled paper
```

**The Report is the view's own sections, 1, 2, 3; Work adds two bands, each numbered from 1** (s32-D27, from
s32-D22 and s33-D03; JL 261101: "for the Results and Process, they will just be in the Work"). RESULTS is what the
layer has made: the view's own
sections (numbered bars with one emoji each, the main point large under 1, side tabs, the flow map,
folder trees). PROCESS is how it is being made, step by step (s33-D06): 1 · 🙋 the decisions waiting for you, one row per question with its state pill and Answer; 2 · the view's own things to do (Data + Paper Plan
🧭 Plan, then ⚙️ Runs to do when the Story has a Task Roadmap, then 🗓️ Next steps, Evidence 📋 Where each stands, Displays 🖼️ Where each display stands, Writing 🪜 Sections, else 🚧
Open); 3 · 🧰 Skills that do it (Work only). A PROCESS title names
the step, never a count (s33-D08). Work reads PROCESS first; its RESULTS are the Report's sections, drawn with the
same code, so they never disagree. The decisions made are on the Report's Interactions page. The drawing and the mind map stay at the bottom, after a dashed rule.

**The Data + Paper Plan view's PROCESS is the plan center** (s33-D07): 🗂️ Design the dataset, 📈 Design the regressions, ⚙️ Make them run, 🔎
Plan the reading, each one row with the skill to use, Open (the mind map, the main analysis Job, the Story's
roadmaps) and Copy prompt; the prompt has the session screenshot the mind map and show its plan before any change.

A state is always a coloured word: orange waits on you, blue running, green done, grey not started or open.

```text
servers/workbench/ui_parts.py            the shared pieces and their stylesheet (phone rules last)
servers/workbench-paper/board_views.py   board_report_views, board_work_views: the two bands
                        board_results.py the six views' RESULTS
                        board_process.py PROCESS: the rows, the plan center
                        board_read.py    reading the Board's topics, faces, tables and folders
                        board_evidence.py, board_interactions.py, paper_version.py
```
