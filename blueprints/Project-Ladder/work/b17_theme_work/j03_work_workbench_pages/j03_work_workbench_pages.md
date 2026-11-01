# j03 · The work pages, level by level

goal: the work theme's three pages on the focus page, each in its three sections: Block, Job and Task × Report, Work and Studio, and the parts all three share (b17-s04)
close: all nine sNN and b17-s04's six shared parts are agreed, and each names the code change for its owner (the base page, design_b02_workbench)
answers: Q01,Q02,Q03

## Topic

The work theme climbs three levels, a Block, a Job and a Task, and every page has three sections with three aims:
Report checks, Work does, Studio thinks. So the design is a 3 × 3 grid, as the paper's is (b16 j01): one Task per
level, and in each Task one sNN per section (JL 261031: "I think you should focus on the things like ... b16_theme_paper ... studio ... UI and think about how you should update the work_theme's workbench UI"). Each sNN draws its Design in haipipe-studio's five parts
through `work_ui_cells.py` and hands over its screen in its own `delivery/ui/`. b17-s04 is the shared column: what
every work page shares, the same at all three levels (the frame: path, title-&-section, view-button-list, goal-line,
both rails, the pop-out; and the right-rail's other sections: Interactions, Delivery, Related, Timeline, Files), made
by t04_shared_parts (JL 261031: "the interface and the Block UI Job UI and Task UI, there are some overlap, right?").
The code lands in the base workbench (`servers/workbench/focus_page.py`), owned by design_b02_workbench: these Tasks
name that change for its owner and never edit it here.

```text
                 Report · check    Work · do    Studio · think    shared by all three (t04)
t01 Block        s51               s52          s53               b17-s04: the frame and the
t02 Job          s54               s55          s56               right-rail's other sections,
t03 Task         s57               s58          s59               one screen draft per part
```

Reshaped 261031 from three Tasks (Block page; the rows at Job and Task; s32's element picks): t02_job_task_pages
became t02_job_page, t03_task_page is new, and t03_element_picks went to `_old/`, since each sNN's screens now
carry the looks they lean on.

Redrawn 261101 the way b16 and b15 draw theirs (JL 261101: "plase read Theme_Paper and Theme_Labeling"; "use
/haipipe-ui loop to check all the UIs here"): each sNN's Design is its section's views, lettered A, B, C, each the
same full screen (haipipe-ui "one view, one screen"), on one made-up example in the shape of board.md's `ui-block`,
`ui-job` and `ui-task` (Tools is public). Each letter goes round the Design loop: a fresh reviewer scores it on eight
rubrics, recorded in `<sNN>/review/<L>-s1-rNN.md`, until it passes; then JL looks once, then the code. Today's live
pages were scored first, in each `<sNN>/review/today-261101.md`. Result 261101: none of today's nine pages passed (6.5 to
8.8; the Block's Studio passes by the rule at 8.2 though its reviewer wrote not yet); all 14 letters passed in round 2
(8.7 to 9.7), after round 1's fixes: no state words on a map, section 1 of a Work view is where it stands, what waits
sits in the 🙋 Interactions helper at the bottom, the open tab is blue so orange means only "waits on you", short topic
names. JL then looked: "the UI you have here is not that good. please check" b16's Block UI and b15's Task UI. So the
Task, Job and Block Work and Reports were redrawn their way: each view one step of the work, read as input → who works
→ output, your part, then the results. A work Task's steps are its life in haipipe-task's `ref/lifecycle.md`: plan ▶
build ▶ run ▶ read ▶ close; Work has one view per step; Report shows the MindMap, then Plan, Build and Read, as
results only. A Job's Work sets each Task against those five steps; a Block's Work shows each Job and the step each
Task is on. All 20 letters pass (rounds r03 to r06 for the redrawn ones). Each cell's form asks one thing per letter:
build it as drawn, or keep today's page; s58's also asks whether step buttons carry their state words.

For other owners (261101), from the reviews:

- haipipe-ui SKILL.md: its Report views (MindMap · Standing · Answers · Questions) and section rule 7 differ from a
  work Block's settled Report (MindMap, then one view per delivery type, no Questions); rule 5's "at most three"
  verbs meets the five tags under an sNN (JL's own, s51-D02); its helpers list has no ✍️ Ask the agent; its Review
  brief leaves out the pass rule, so reviewers wrote "not yet" on passing scores.
- design_b02_workbench (`frame.topic_label`): a topic inside a Job or Task prints its whole path
  (`b17.j03.t01-s51:theme_work.work_workbench_pages.block_page @ block_ui_report`); sNN numbers are unique in a Block,
  so the short form `b17-s51:theme_work @ block_ui_report` is enough (every reviewer of a Studio page asked).
- design_b02_workbench (`focus_page.py`): today's Interactions button says "Interaction", a noun; the reviewers ask
  for "Answer"; a mind map on a phone shows only its root.

## Tasks

<!-- in order; new_job.py task adds each -->
1. t01_block_page · The work Block page
2. t02_job_page · The work Job page
3. t03_task_page · The work Task page
4. t04_shared_parts · The parts every work page shares
