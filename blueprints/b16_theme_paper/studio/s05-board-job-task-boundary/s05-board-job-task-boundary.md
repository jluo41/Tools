s05 · The Board, Job and Task boundary
======================================

**Topic:** the boundaries between a paper Board, its version Jobs and their Section Tasks: what each level
holds, and the line that says which. JL 261009 drew the first line at the venue: the Board is venue-free and
close to the work (the basic research questions, the related work, the telling), and a Job is attached to one
venue and decides which questions and results it reports, without calling the work itself. The second line,
proposed, is one Section: what only this Section needs is the Task's, what spans Sections is the Job's. The
ladder said only that each level's studio/ and reports/ hold "its own"; this topic is the line that says which
(first drawn as s05-venue-boundary, then s05-board-job-boundary, the same day; JL: "it should be the board job
and task boundary").

**Feeds:** `reports/` q01_paper_ladder · q02_venues_related_built · q04_story_into_topics


Files
-----

```text
s05-board-job-task-boundary/
├── s05-board-job-task-boundary.md          this face
├── build_s05_board_job_task_boundary.py    the builder; marks are kept on rebuild
├── s05-board-job-task-boundary.excalidraw  the drawing, in topic groups side by side. Row 1: the boundary
│                                           (1 · two lines and what each level holds, 4 · edges) · the Idea
│                                           Studio (5 · its screen at each level, each topic's question) · the
│                                           Audience Report (2 · the asks, 6 · its screen at each level, every
│                                           view and run button explained). Row 2: how the levels talk (7) · the
│                                           ScalingGlucose case (3) · open. Row 3: the shared ladder (8)
│                                           and the Story/Ideation homes (9), carried from s01 and s04
└── s05-board-job-task-boundary.png         its preview
```

Rebuild: `python build_s05_board_job_task_boundary.py`, then
`python ../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py s05-board-job-task-boundary.excalidraw s05-board-job-task-boundary.png 0.4`.


Decided
-------

s05-D01 · The Board is venue-free and close to the work: the basic research questions, their reports, the telling and the roadmaps (JL 261009)
s05-D02 · The related work lives on the Board (JL 261009)
s05-D03 · A Job is attached to one venue; it decides which questions and results to report and does not call the work (JL 261009)
s05-D04 · This topic covers all three levels: the Board, Job and Task boundary (JL 261009)
s05-D05 · Block › Audience Report gets Related Papers after Related Questions: the related papers under the question each bears on (JL 261009; built in workbench-paper 0.34.0)

s05-D06 · Story and Ideation cease being Pages; the paper Board has board.md with Questions, studio/ topics, reports/ answers and runs/ (carried from s04-D01, JL 261007)
s05-D07 · Ideation lives in studio/s01-ideation/; each telling in studio/sNN-story-<telling>/, with identity, pitch and stakes in its face and drawings beside it; an earlier telling is an ended topic (carried from s04-D02, JL 261007)
s05-D08 · Research questions live in board.md ## Questions, grouped by topic, with reports/qNN_<question>/ holding Answer, Evidence, Limits and Next; the Story's evidence, discovery and Task roadmaps become each report's Work (carried from s04-D03, JL 261007)
s05-D09 · Story and Ideation skills stay callable from Idea Studio and Audience Report; they write a topic or register a Question (carried from s04-D04, JL 261007)
s05-D10 · Each version face holds its Section Narrative and compile order in ## Narrative; the build reads that order (carried from s04-D05)


Retired topics (261010)
----------------------

JL approved removing s01-s04 from the current Studio. Their complete working copies, including s02's
uncommitted builder and drawing and s03's migration history, are preserved under
`_archive/20261010/studio/` beside this Board's studio/. These are frozen records, not current build inputs.
The retired numbers s01-s04 are not reused in this blueprint. s05 now holds s01's useful shared ladder
and all five s04 decisions. Guide, Board and report links use s05; the old migration goal is retired.
No real paper Board is migrated by this cleanup.


Open
----

1. The two lines, proposed: the venue (Board | Job: send the paper elsewhere; what must change is the Job's) and one Section (Job | Task: what only this Section needs is the Task's; what spans Sections, the Job's).
2. Each level asks its own kind of question (JL 261009: "in each three level, we might ask different questions"), proposed as frame 2: the Board asks what is true (a research question, answered by the work's Results, kept as `reports/qNN_`); the Job asks what to tell this venue and whether it is ready (J1-J5 and the comments, answered by the cut, the venue's rules and the checks); a Task asks what its reader needs (its row's reader question in the Job's `## Narrative`, answered by its sentences; its smaller asks stay in its plan).
3. `venues/<venue>/` into the Job (`jNN_…/venue/call.md`, frozen with each send): s11 (Block › Description › Venue) and Q02's hypothesis put it on the Board.
4. A telling's name drops the desk: `sNN-story-<desk>-<idea>` → `sNN-story-<idea>` (haipipe-paper-story, `paper_ladder.py`); ScalingGlucose's `s02-story-nmi-cgm-scaling-axes` → `s02-story-cgm-scaling-axes`, its venue bits (the `desk:` line, the Opening sentence, D4, the NMI-first order of §5.3) to j01.
5. The Job's standard topics, names to pick: `s01-venue-fit` · `s02-narrative-cut` · `s03-figure-plan` · `s04-response-map` (a revision).
6. Task-level `reports/`: haipipe-question calls a one-Section question too narrow ("lift it a level"); drop them from the ladder?
7. A Task's `studio/`: only `sNN-argument-flow`, when a Section's logic needs drawing?
8. Edges, proposed: a reviewer's new work and a Section's missing number are both asks the work's Tasks run; the Job only cites, the Task only binds; a Section never asks a new research question.
9. On screen: the Venue view moves from Block › Description to Job › Description; Description › Related keeps the list of every related item; Audience Report › Related Papers shows them by question.

10. Frames 5-7, proposed (JL 261009: "for each level's studio, what are the typical questions (topics)? and what are not? ... for each level's of report, what are the subviews ... why we must keep it ... how does the three level's communicated with each other"): each level's studio topics and what is not one; each Audience Report view, what it shows and why the writing needs it; what moves down, up and sideways between the levels, and the field that carries it.
11. A Questions column in the Job's `## Narrative`, so each Section names the Board Questions it carries; today a row names the Story's claims (C1-C5), not Q00-Q06.
12. A field for an ask sent up under a Board Question: a Section's gap, or a reviewer's request for new science. Nothing carries it today.
13. The Block's Audience Report › Narrative (the telling) and the Job face's `## Narrative` (the Sections' order) share a name; call the Block's view Story?
14. A Task's `studio/`: the ladder's `sNN-<topic>/` and the Page workbench's `studio/draw/` and `studio/chat/` lanes (workbench roster) would share one folder; one rule needed.

15. JL 261010 asks to see a Job's studio/ and reports/ smoothly from Block level too. Proposed: the Board's Idea Studio and Audience Report can show child items, labelled by their owning Job and version, with direct links to the same item. Decide all Jobs versus a selected version, whether Task items also appear, and which filters to keep. Each item keeps one owner; viewing it above does not copy it or turn a Job question into a Board research question. This is a design question; the workbench has not been changed to add it.
16. Carried from s04: older Story Pages still need reader support until migrated; the treatment of an earlier telling's sent and judged questions remains open. Review batches have a home in the answering version's comments reports, and each version keeps its own Narrative.

(write here, or mark the drawing in red)
