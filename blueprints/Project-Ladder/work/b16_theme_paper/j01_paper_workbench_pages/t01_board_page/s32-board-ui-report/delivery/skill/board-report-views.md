### The paper Board's Report and Work: seven views, A to G

A paper Board's Report and Work show the paper's four layers as views, one button each, in this order, with the same
letters on both (b16 s32-D12, s33-D02): the plan (A to C), what supports it (D), the evidence (E, F), the writing (G).
Idea (the many directions) and Story (the one chosen) are two views (s32-D44); Data flow and Paper flow are one,
Data + Paper Plan (s32-D28, D29); Venue is inside Story (s32-D12); Displays stands after Evidence and before Writing
(s32-D26). A view shows only when the Board has its part: no ideation topic, no Idea view; no Story topic, no Story
view; no evidence Job, no Evidence view; no display Job or display plan, no Displays view.

```text
idea      A Idea               the many directions: 🎨 Studio, then 🔀 Directions and 🎓 Theory as left tabs (no Story yet: 🧭 Direction first, 📚 Related after Theory)
story     B Story              the one chosen: 🎨 Studio, Direction, Pitch, Theory, Research Questions, Stakes and evidence, Related (related/related.md), Venues (venues/<venue>/call.md), Story by Section
plan      C Data + Paper Plan  🗄️ Data flow and 📝 Paper flow, each its topic's mind map worked on in place, then 🗺️ Roadmaps; each topic's drawing after the dashed rule
explore   D Support blocks     🧪 Work and 🔎 Discovery: the Blocks its pages name, one folder tree per Project, folding down to each Task's Runs
evidence  E Evidence           🔢 Values and 📚 Citations: a left tab per Task, the thing itself on the right
displays  F Displays           Plan (the display plan's drawing), 🖼️ Displays by Main, Supplement and Others (each its preview.pdf), 🔍 Examples
draft     G Writing            a ✍️ section per version, its Sections as left tabs to read; 📄 The assembled paper; 📮 Ready for the portal
```

**Every view ends in 🙋 Interaction, and every bar starts closed** (s32-D38, D41, D42). The last numbered section of
each Report and Work view is 🙋 Interaction: the collection Runs about this view, a left tab per question and its form
on the right, Back and Next, Copy feedback on a set's last question; with none it says so. Every section bar starts
closed (▸); what you open stays open in this browser.

**The Report is the view's own sections, 1, 2, 3; Work adds two bands, each numbered from 1** (s32-D27, from
s32-D22 and s33-D03; JL 261101: "for the Results and Process, they will just be in the Work"). ⚙️ PROCESS is how the
layer is being made, step by step (s33-D06): 📌 Open points, only when a part's face marks lines waiting for you; then
the view's own steps (Idea and Story 🚧 Open; Data + Paper Plan 🧭 Plan, ⚙️ Runs to do when the Story has a Task
Roadmap, 🗓️ Next steps to the send; Evidence 📋 Where each stands; Displays 🖼️ Where each display stands; Writing 🪜
Sections to finish); then 🧰 Skills that do it. PROCESS has no 🙋 step: the open forms show once, in 🙋 Interaction
(JL 261105: "keep only the bottom"). 📊 RESULTS is the Report's sections, drawn with the same code, so the two never
disagree. A PROCESS title names the step, never a count (s33-D08).

**The Data + Paper Plan view's PROCESS is the plan center** (s33-D07): 🗂️ Design the dataset, 📈 Design the
regressions, ⚙️ Make them run, 🖼️ Plan the displays, 🔎 Plan the reading, each one row with the skill to use, Open (the
mind map, the main analysis Job, the Story's roadmaps, the display plan) and Copy prompt; the prompt has the session
screenshot the mind map and show its plan before any change.

A state is always a coloured word: orange waits on you, blue running, green done, grey not started or open.

```text
servers/workbench/ui_parts.py            the shared pieces and their stylesheet (phone rules last)
servers/workbench/interaction_section.py 🙋 Interaction, the last section of every Report and Work view
servers/workbench-paper/board_views.py   board_report_views, board_work_views: the two bands
                        board_results.py the seven views' RESULTS
                        board_process.py PROCESS: the rows, the plan center
                        board_read.py    BOARD_VIEWS; reading the Board's topics, faces, tables and folders
                        board_evidence.py, board_interactions.py, paper_version.py
```
