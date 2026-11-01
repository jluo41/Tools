haipipe-ui · Changelog
======================

## [0.3.0] - 2026-11-01

- Review on Tools' placeholder Board (blueprints/Project-Ladder/paper/Paper-Example, Tools server 5623), never a real paper; a real-paper bug is diagnosed by a new session in that paper's SPACE (JL 261101).

Two bands (b16 s32-D22, s33-D03): every Board view is RESULTS and PROCESS, each numbered from 1; Report reads RESULTS
first, Work PROCESS first, and RESULTS is drawn by the same code on both. Two new rows: the to-do row (words, a
coloured state pill, one verb; s33-D06, from b15 s58) and the plan row (Open, "use /<skill>", Copy prompt; s33-D07).
A PROCESS title names the step, never a count (JL's rule "labels carry no counts", decided 261101). Phone `@media`
rules come after the base rules they change (that bug failed five views on phone, s32-D21). The helpers after the
dashed rule are the drawing and the mind map only; Interactions moved into PROCESS 1. Pointers now name the code
where it lives: `servers/workbench/ui_parts.py` and `servers/workbench-paper/board_*.py`; `focus_draft.py` is the
draft Task page only. The paper Board's views are seven, A to G, Venue inside Story (s32-D12).
`scripts/shoot.py` takes the whole page by default; `--viewport` takes only the first screen.

## [0.2.3] — 2026-11-01

Side tabs (JL 261101: "in the left there is a panel, and we can read the content quickly"): the list on the left, the
open item's content on the right, for content that is read; in Report a panel shows the thing, not its steps.

## [0.2.2] — 2026-11-01

The name card tabs (JL 261031: "we will use the cards-tab"): cards that act as a view-button-list, their detail in a
panel below; a card-tab chain when arrows join them. The mind map helper is a button that opens the map (drawn
inline it repeated the face). All seven paper Board views, A to G, are drawn and built in this shape.

## [0.2.1] — 2026-10-31

An eighth rubric, Salience (JL 261031: "it should highlight the main point ... currently it is very boring"): the
view's main point first and largest, its content shown rather than only headings. Five drawn blocks for it: lead,
tiles, chain, ask, more. b16 s32 B passed round 2 as equal heading bars, which is why the rubric exists.
Then JL's shape for every view: numbered heading bars in reading order, the main point large under section 1,
content under each bar as tiles, a chain or a line, and the helpers (Interactions, drawing, mind map) at the
bottom after a dashed rule.
One emoji per section name, the same in every view; no blue edge on the main point.
Tiles that each hold more (the RQs) act as a view-button-list, the open one's detail below them.
The Review's screenshots are full-page (`--full`); a first-screen shot left half of s32 A and B unscored.

## [0.2.0] — 2026-10-31

The Design loop (JL 261031: "add the haipipe-ui loop design, to make it design again and again, until the different
rubrics are met"). Each letter of a page design goes round: a fresh blind reviewer scores it on seven rubrics (Glance,
Place, Lean, Words, One job, Same look, Phone), the designer revises the three named fixes, a new reviewer goes again;
pass is every rubric 7 or more and the mean 8 or more, at most 4 rounds, the same shape as /haipipe-display's revise
loop. Two stages: the drawing first, the live page after. Reviews are kept as `<topic>/review/<L>-s<stage>-rNN.md`.
The Review now scores the rubrics instead of subtracting from 10, and is one round of the loop.
From a fresh-agent dry run (`loop s32-board-ui-report B`): the loop now names where the topic lives and that its
own builder re-renders it, that the reviewer is a new general-purpose agent, that a passing review is named on the
letter's decision line, that rounds restart at each stage, the stage-1 `page` line, and that JL looks once between
the stages, then the code is built and stage 2 runs to a pass.
From the loop's first real round (b16 s32 B r01): the reviewer also gets the settled decisions, and a fix that
would undo one goes to JL as a question instead of being applied.

## [0.1.12] — 2026-10-31

New section "Designing a page: one view, one screen" (JL 261031: "what is the principle of designing the UI? ...
could you add it to the /haipipe-ui"). A page's design topic draws every view as the same full screen, lettered A, B,
C, Report and Work sharing letters; one round settles one letter (code, live check, green note); ✅ comes only from
the builder's `delivery/ui/<level>-<section>/<L>-<view>.html`. Model: b16 j01 `paper_ui_cells.py` (s32 to s40).
From a fresh-agent dry run (a cowork Block Report): the section now says how the topic is numbered, what `<level>`
means, that a theme may have its own views if none repeats another or a rail section, when Report and Work share
letters, and that orange marks the open view only in the drawing (the page keeps its blue).

## [0.1.11] — 2026-10-31

A theme Block's Report gains Block UI · Job UI · Task UI after Questions (JL 261031: "I think you should have these as
well ... the block UI, job UI and task UI"; "you need to think about what UI you need to use as well"). Each shows one
real, full page of the theme live (`ui-block:`, `ui-job:`, `ui-task:` in board.md; focus_page.ui_view). The seven
theme Blocks of Project-Ladder (b11 to b17) name theirs; cowork has no Task level, so no Task UI.

Interactions is always on the right rail, from a Project down to a Task, and opens on All (JL 261031: "in the right
rail, we should have a section named the Interaction, to show all the interaction under this page"); before, it showed
only when something had been asked. Its rail line says "🙋 waits on you", "nothing waits on you" or "nothing asked yet".
Delivery is always on the rail too (JL 261031: "we also missed the delivery here"): "nothing handed over yet" until
the folder's delivery/ holds something.

## [0.1.10] — 2026-10-31

JL's answers to the page-layout form (b10 runs/r01_collect_page_layout; b10-s33-D04 to D08). Every section's
view-button-list sits under the title-&-section and above the goal-line, Studio's groups included, and a section
with one view keeps a one-button list, so the goal-line never moves. No count line under the title and no count in a
right-rail item. Rule 3: a section's verb lives in its right-rail item; the title shows only the name, paper pages
too. The Sections table names Related, Timeline and Files' one button, and gains Interactions (its verb, answer). From a
fresh-agent check of two live pages: rule 3 now says the verb sits in the Sections table and the right-rail item
says what a section holds, since the rail lines are not verbs.

## [0.1.9] — 2026-10-31

An sNN has no page of its own (JL 261031: "first we will remove the single page for the studio"; b35-s02-D05): rule 3 says a link to an sNN, the left rail's included, opens its card in its level's Studio under its group, outlined, and the card's name, line and picture open in the pop-out.

## [0.1.8] — 2026-10-31

Page parts get one name each (JL 261031: "we should make these terms to be consistent"; "the view-button-list are not the right rail"): path, title-&-section, view-button-list, goal-line, view-caption, content, left-rail, right-rail, with the `focus_page.py` class each maps to. Rules 1 and 2 and the sections table use these names. A section (Studio, Delivery, Timeline, Files) never sits in a view-button-list. A draft Task's view-button-lists: Work is the five steps and Runs, Report is MindMap · Text · Status; under each view, sections. Rule 4: a view's sections fold by their heading, open by default (JL 261031).

## [0.1.7] — 2026-10-29

Studio groups are view buttons, one per group, no "All", an "Other" button for the ungrouped (JL 261029). A Studio row shows four things: picture (lead slide first), name, one line, stage word; then Slides, Draw, Mind map.

## [0.1.6] · 2026-10-29 · Overview is Report

- The section Overview is now Report, verb "check": the results and the progress (JL 261029: "我们现在就把这个 overview
  改成 report ... check 这个 progress 的 status"). Its view Report became Standing and Summary became Findings, so no
  page reads Report › Report; `section=overview`, `group=summary` and `group=report` still open the same views.

## [0.1.5] · 2026-10-29 · the line under the title has a name; no two views repeat

- The one line under a page's title carries its kind's word: Mission (Project and above), Purpose (Theme, Block),
  Goal (Job), Aim (Task) (JL 261029: "能不能给这段话这类话起个名字").
- An upper level's Overview views each answer their own question: MindMap the shape, Summary the numbers and what
  happened last, Themes what each Block is for, Status how far each Block has got (JL 261029: "为什么感觉它每个 view 都是一样的").
- Each view says what it shows in one line above its content (JL 261029: "每一个 view 的 mission 都是一样的吗"); the
  view buttons stay right under the title, the mission under them (JL 261029: "你要把那个 view button 放在上面").
- Summary says what was found, never counts (JL 261029: "这种没有信息含量的东西 ... 有啥屁用"): each answer's first
  sentence, the proposals waiting for a decision first, then one line naming what has no answer yet.
- A Block, Job and Task get a MindMap view (JL 261029: "WE SHOULD HAVE THE MINIMAP AS WELL"); Report stays the default.

## [0.1.4] · 2026-10-29 · one look: the classic workbench's

- The focus page takes the classic workbench's tokens, bold headings and bordered white boxes (JL 261029); the skill
  says a new page copies them and never invents a palette.

## [0.1.3] · 2026-10-29 · Files on the rail; rows you can scan

- Files is its own right-rail section (verb: browse), no longer a view of Work.
- A list row is the real name, one line of what it is (the goal's first clause), facts as words with numbers, and
  the page's picture; a rail's open panel has its own background and border.

## [0.1.2] · 2026-10-28 · from the first after-review (8/10)

- Overview's views are Report · Questions · Timeline; Context and Pipeline sit inside Report. Where a page stands
  (done when, status, waiting) shows once, in Overview's Report, never repeated in Work.

## [0.1.1] · 2026-10-28 · scoring made exact

- From the first blind review (b17 Studio, 0/10): the score has a floor of 0, and a question only partly answerable
  costs 1, not 2.

## [0.1.0] · 2026-10-28 · first version

- JL 261028: one rule for every page: the five-second test, five rules, one verb per section (Overview read, Work
  do, Studio think, Delivery hand over, Related take in), the page at each level, and a blind review that
  screenshots a live page (`scripts/shoot.py`) and scores it out of 10.
