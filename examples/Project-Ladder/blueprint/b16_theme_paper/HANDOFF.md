# Current Paper theme structure

Use PRINCIPLE.md and the shared Work Block renderer. The active structure Studios are:

- s01-idea-block-structure: candidate Idea Jobs and ideation assessment Tasks.
- s02-grant-block-structure: Story, Evidence, Display, Writing and Presentation for grant applications.
- s03-paper-block-structure: the same named Job groups with manuscript-specific work.

Each Studio separates Job Type, Job Name, Task Type and Task Name from its grouping. Structure and Draw use meaningful names. Main/Appendix/Explore are Display roles; versions and presentation formats are not automatically new types. Review and Submission stay within the relevant Writing Job.

Shared studio-views.json supplies Structure / Draw / Examples / Skills. Structure has Jobs & Tasks and Studio entries. Paper binds the existing Paper-Example; Idea and Grant Examples remain unbound and are omitted by the shared reader. Skills stays in this Studio. All selection remains inside the owning Block.

The three older active topics were preserved byte-for-byte under _archive/20261127/. Historical decision ids refer to those archived records, not the newly assigned s01/s02/s03 subjects. Their reports and human marks remain available.

This delivery defines and shows structure. It does not migrate research Jobs or register missing runtime types. Current Paper value/citation keys conflict with shared owners; Story, consolidated Evidence, final-asset and Presentation contracts require follow-up. The separately proposed hai-block structure function remains future work.

Guard: delivery/page-spec/check_block_structures.py. Current work receipt: trace/261127/1049_named_block_structures.md.

## Historical handoff

The following retains the earlier framework and ownership decisions as history; current guidance above takes precedence.

You are the session for the blueprint Block Tools/examples/Project-Ladder/blueprint/b16_theme_paper (read its board.md first). JL opened one Block and one session per theme (261007); you own the paper theme. Work in place in the SPACE (Tools is a symlink to ../Tools-SPACE); never commit, push, reset, clean or stash: the tree has many uncommitted changes from JL and other sessions. Chat replies follow /response-format, each section closing with its **Studio:** line. Record each Question's outcome in its report Page under reports/ (SPACE-relative paths) and keep answer-status below answered until JL settles it.

The goal
--------
Make the paper theme fit the shared ladder b10 settled (b10_project_workbench (removed 261126)), as a FOLDER STRUCTURE on disk and as a WORKBENCH UI on screen: a paper Board (Block), a version (Job), a Section (Task), and their Runs.

1. Folder structure (b10 s01, s09): the Board alone owns `studio/` (Studio topics), `related/` (what came in, kept as it came: `related.md`, `meetings/`, `papers/`, `files/`, `emails/`; each subfolder is a group; owner /hai-related, b10 s04-D08, D09) and `delivery/` (what goes out, one subfolder per source, `delivery/jNN_<version>/`). Every level owns its face `.md`, its `reports/` (every level reports, s09-D02) and its `runs/`; a Job or Task keeps no `studio/` or `delivery/` of its own.
2. Workbench UI (b10 s02, s09-D05, s04-D05): the top row `Guide · Studio | Paper Board · Version ▾ · Section ▾ | Delivery`, where Studio (with Related folded under its topic cards) and Delivery open the Board's view from any level; below it each level's work row `Description | Report | Work | Runs`, each with its third row and its Runs panel. A Section is a Page Task (the Page workflow belongs to 1_base/draft).
3. Each Studio topic carries `**Stage:** explore|shaping|agreed|closed` (b10 s09-D03); a person moves it; at most 10 topics.

Where things are
----------------
- Your Block: board.md (5 Questions), reports/q01-q05, goals/ (g03, g04), studio/ (reorganized 261011 to b10's numbers: s01-paper-tree-concept, s02-paper-studio, s03-paper-delivery, s04-paper-related, s05-paper-report, s11-s13 the level tabs, s53-paper-skills, s81-paper-guide, s32-paper-ui; groups in studio/_groups.txt). Retired s01-s04 of 261010 are frozen under _archive/20261010/studio/.
- The shared rules: b10_project_workbench/studio/ (removed 261126) s01-overall-tree-structure (the ladder, s01-D32 delivery, s01-D34 related), s02-studio-workbench-skill, s03-delivery-workbench-skill, s04-related-workbench-skill, s05-report-workbench-skill, s06-run-workbench-skill, s09-studio-block-job-task-delivery (who owns what).
- Your skills: Tools/plugins/haipipe-toolkit/skills/3_theme/paper/ (hai-paper and its -section, -story, -assemble, -comments, -venue, -workflow; workbench-paper). Base skills you borrow: hai-studio, hai-delivery, hai-report, hai-draft-*.
- Your server: Tools/plugins/haipipe-toolkit/servers/workbench-paper/ (paper_theme.py over the shared frame servers/workbench/page/block_index_page/frame.py; paper.py the old page's readers). Its tests: servers/workbench-paper/tests/.
- The real test Board: examples-2-nn/Proj11-CGM-FM/paper/Paper-ScalingGlucose-NatSeries2026 (its own git repo; board-kind paper-board). On 261011 it had studio/ s01-s03 (no Stage lines), reports/ q00-q06, delivery/j01_v1009_nmi/, version j01_v1009_nmi with Sections t00-t04 and t21; missing related/ (its one meeting still sits in meeting/), venues/ and runs/; a hidden old copy .paper-topics-1/ holds an old Job delivery. Theme folders: paper/ in Proj11, Proj21, Proj34, Proj41, ProjF; papers/ in FairGlucose, EventGlucose, Proj32 (both names read the same, s01-D29).

How to work
-----------
1. Design first, in the Studio topic that owns the point (its face's Decided and Open, its drawing, red marks for JL), then the report of the Question it answers.
2. Then build: skill contract and scaffold, then the workbench views, tested on a demo fixture in a temp dir (placeholders only). A real Project's folders (ScalingGlucose's meeting/ to related/meetings/, .paper-topics-1/, papers/ to paper/) change only when JL says so.
3. Shared code has owners. Ask before editing their files, with exact-match patches, and tell them (SendMessage; ListAgents for the live names):
   - the shared frame servers/workbench/ and servers/_host/, b10's topics: the b10_BluePrint-ProjectWorkbench sessions (-sNN Studio, -dNN Delivery and Related, -RunSkill Report and Run)
   - b16's studio/, runs/ and board.md topic lines: b16_theme_paper_sNN (261011 split); this session keeps HANDOFF.md, reports/, servers/workbench-paper/ and the paper skills
4. Rules: a generated file is never changed by hand (AGENTS.md rule 13: rerun its builder); no absolute /Users/... paths in tracked files; concept drawings carry no DrFirst content; check for PHI before reading any data file; never a git worktree.
5. Tests: the tests beside the code you change, from the SPACE root (`source .venv/bin/activate && source env.sh`); say the counts and any failure that was already there. After a server change, restart the hosts on 5602, 5622 and 5623 with their same arguments and open the real page.

Where it stands (261011)
------------------------
- Built: the paper theme draws in the shared frame; Related left Description and folds inside the Studio (paper_theme._related_space, frame.studio_related); the Delivery is the Board's (delivery/jNN_<version>/).
- Reports: Q01 partial, Q02 partial (venues open), Q03 partial (the 261007 comments rule), Q04 partial, Q05 partial; none is answered until JL says so.
- Next: settle venues (s04-paper-related), add Stage lines and related/ on ScalingGlucose with JL's go, then the paper skills' docs that still say six Spaces or Idea Studio.

Report to JL in chat as each Question finishes: what changed (files, one line each), the checks and their counts, what is left.
