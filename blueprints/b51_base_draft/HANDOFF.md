You are the session for the blueprint Block Tools/blueprints/b51_base_draft (read its board.md first). JL opened it on 261011 from the b16_theme_paper session: "How do we really think about haipipe-page, it is more like the haipipe-draft, which contains the logic, sentences, and evidence, and have a subfolder of draft to work on." Work in place in the SPACE (Tools is a symlink to ../Tools-SPACE); never commit, push, reset, clean or stash: the tree has many uncommitted changes from JL and other sessions; never a git worktree. Chat replies follow /response-format, each section closing with its **Studio:** line. Record outcomes in the Block's Studio topics, not in Question reports, and write no Related question line (JL 261011: "use the Studio only"). Done on 261011: option A, haipipe-page is now haipipe-draft and "Task = Page" is gone; see studio/s01-draft-and-page for what was decided and what is open.

The goal
--------
Decide what the base layer under every theme's writing really is, and name it with JL: a draft holds its logic (the plan), its sentences and its evidence, and is worked on in a draft/ subfolder; the Page is the face a reader opens. Then make the base skills, the scaffold and the workbench say the same thing.

Where things are
----------------
- The Page family (the base layer today): Tools/plugins/haipipe-toolkit/skills/1_base/page/
  - haipipe-page (0.125.0): the Page Folder and Page Face contract, the router, page.py, src/ (common.py holds the delivery path helpers every theme uses)
  - haipipe-page-workflow (0.66.1): the lifecycle controller, context → structure (SHAPE, SURVEY) → evidence (LAND, EMBED) → writing → check, and the Writing Runs (Scratch, Revise)
  - haipipe-sentence (0.6.2): the sentence as the atomic unit, its dotted address, comment lanes, evidence cards
  - haipipe-folder, workbench-page, workbench-studio, workbench, workflow-runs, pages-example
  - agents: plugins/haipipe-toolkit/agents/haipipe-page-*-agent.md (approver, auditor, check, creator, evidence; more agents named haipipe-page-*-agent are listed in the session's agent types: context, structure, writing)
- The Page's screen: servers/workbench/task-page/ (outline.py is the Draft view, routes /_board/draft, /_board/evidence, /_board/value; the exporters page.py export uses: md2tex, md2docx, docx2pdf) and the shared frame's Page Task views (servers/workbench/frame.py PAGE_TASK_SUBS: Description Scope · Plan · Requirement · Records; Report Table · Reading · Questions; Work Draft-Scratch · Draft-Revise · Evidence-*).
- The rules every Block now follows (b10_project_workbench): Studio, Related and Delivery are the Block's alone; a Job or Task has none of its own (s09-D01, s04-D05, s03-D06). A draft's built output goes to the Block's delivery/<jNN>/<tNN>/<lane>/.
- A real draft to look at: examples-2-nn/Proj11-CGM-FM/paper/Paper-ScalingGlucose-NatSeries2026/j01_v1009_nmi/t01_introduction/ (a paper Section: face, draft/, runs/; its LaTeX in the Board's delivery/j01_v1009_nmi/t01_introduction/latex/). Old-layout papers (TimeEventDM, AnchorPK, CGMtoHbA1c) hold their only prose in .tex fragments: read, never rebuild over them.

How to work
-----------
1. Names are JL's: for "Draft" vs "Page", and any rename, propose options with a recommendation and wait for JL's pick before changing a skill name, a folder or a face field. Count a rename's reach from disk (Q03) before proposing it.
2. Design first, in a Studio topic (/haipipe-studio: studio/sNN-<topic>/, its face with Tags and Stage, its drawing and builder); the topic's face records the decisions (JL 261011: no Question reports).
3. Then build, tested on a demo draft in a temp dir (placeholders only, never real project data); real Projects change only when JL says so.
4. Shared code has owners; tell them (SendMessage; ListAgents for live names): the shared frame and b10's topics are the b10_BluePrint-ProjectWorkbench sessions (-dNN for Delivery and Related); the paper theme is b16_theme_paper (and b16_theme_paper_sNN for b16's studio/).
5. Rules: a generated file is never changed by hand (AGENTS.md rule 13); no absolute /Users/... paths in tracked files; check for PHI before reading any data file; plain words (AGENTS.md rule 9).
6. Tests: the tests beside the code you change, with `source .venv/bin/activate` from the WellDoc SPACE root; say the counts and any failure that was already there. After a server change, restart the hosts on 5602, 5622 and 5623 with their same arguments and open the real page.

First step
----------
Read the Page family's SKILL.md files and the ScalingGlucose Section folder; then reply to JL with: what the family manages today, mapped to logic · sentences · evidence · draft/ · face · built output; whether "Draft" fits, with two or three naming options and your pick; and what a rename would touch, counted. Change nothing outside this Block until JL picks.
