---
name: haipipe-ui
description: >-
  The rules every workbench page must pass so a reader quickly understands it and can act on it (the five-second
  test, five rules, one verb per section: Report check, Work do, Studio think, Delivery hand over, Related take in),
  the page shape at every level (Project, Theme, Block, Job, Task), how a page design is drawn (one view, one
  screen, lettered A, B, C, settled one at a time), and the design loop: a fresh reviewer scores the drawing, then
  the live page, on twelve rubrics, and the design is revised round after round until every rubric passes. The live
  page is walked in Chrome as a person uses it (every view clicked, every canvas card hovered and pinned, every
  pop-out opened, phone width, console errors) and measured against the paper UI as the bar: modern, plain, nothing
  missing. Use to design or change a page, to check a page before calling a UI change done, to walk a page in
  Chrome, or to compare a before and after. Owns how a page looks and acts; /workbench owns what data it reads. Trigger: review the UI,
  ui rules, is this page clear, five-second test, page design, redesign this page, design loop, ui rubrics, walk the
  page in chrome, click through the ui, /haipipe-ui.
metadata:
  version: "0.5.0"
  last_updated: "2026-11-04"
  # version history: ./CHANGELOG.md
---

# /haipipe-ui · a page anyone gets in five seconds

JL 261028: "what is the rule of you to design the UI to make sure for every page, people can quickly understand
what they have and quickly operate it ... and tell the differences of the Overview, Work, and Studio, and Delivery,
and Related". This skill is that rule, and a review that checks a live page against it.

```text
/haipipe-ui                  the rules below: read before designing or changing any page
/haipipe-ui walk <url>       drive Chrome through the page as a person does; fix what breaks (Walk, below)
/haipipe-ui review <url>     a fresh reviewer screenshots the page and scores it (Review, below)
/haipipe-ui loop <topic> <L>  the Design loop on one letter: drawing, then live page, until the rubrics pass
/haipipe-ui compare <a> <b>  the same review on a before and an after, side by side
```

/workbench owns the data contract (what each page reads and writes). This skill owns only what a reader sees and
does. The look is the classic workbench's (JL 261029: "follow the css like this"): its colour tokens
(`servers/workbench/frame.py` `:root`: white ground, near-black text, blue `#1864ab` for the current thing), bold
headings, and content in white boxes with a 1 px grey border and rounded corners; a new page copies these, never
invents a palette. It never changes the style (fonts, colours, borders): a redesign moves structure, not looks (JL 261028:
"don't change the style of the old one ... propose the new structure").


## Page parts: one name each

Every page has the same eight parts, top to bottom, then the two rails. Use these names, and only these, in rules,
replies, mocks and code comments (JL 261031: "we should make these terms to be consistent").

```text
part               what it is                                              in focus_page.py
path               the folders from the SPACE down to this page            .focus-crumb
title-&-section    the page's name, then the open section's name           h1, .h1-section
view-button-list   the views of the OPEN section, right under the title    .section-views
goal-line          Mission · Purpose · Goal · Aim, one line, by level       .focus-goal
view-caption       one line: what the open view shows                      .view-caption
content            the open view itself                                    .focus-card
left-rail          change PAGE: siblings, the open page's children         .focus-rail.left
right-rail         change SECTION: Report, Work, Studio, Delivery, ...     .focus-rail.right
```

1. **view-button-list ≠ right-rail.** The right-rail switches the section; the view-button-list switches views inside it.
2. **A section never sits in a view-button-list.** Studio, Delivery, Timeline and Files are right-rail sections at every level.
3. **The view-button-list belongs to one section.** Changing section changes the whole list, never one button.
4. **On a phone** (600 px or less) both rails hide; the right-rail shows as a `.section-line` above the view-button-list.
5. **Phone rules after the base rules they change.** A phone `@media` rule placed before the base rule it changes
   loses to it; that bug failed five views on phone (b16 s32-D21), so phone rules come last in the CSS.


## The five-second test

A reader who has never seen the page looks at it for five seconds and must answer four questions:

1. **What is this?** The folder's name and its goal, in one line.
2. **Where am I?** The path from the SPACE down to this page.
3. **What is here?** The open section, named, with its content visible.
4. **What can I do?** The actions, as short verbs next to what they act on.

A page that needs a sentence of instructions to pass has failed it.


**Closed by default (JL 261104: "默认的话，大家都是合着的"):** anything that opens and closes, a section, a tree level, a map
branch or a card, starts closed on every page, and a click opens it. A walk and a review fail a page that draws one open.


## A page reads badly: compare before you change anything

JL 261104: "你早这样不就行了吗 你为啥就是一开始意识不到呢？ ... 这是一个 huge lesson". On b01 a mind map was reworded, folded,
deepened, swapped for a table and put back, because nobody looked at another Block. One comparison found the cause: 16 cards
against b35's 6, since b01 listed its 15 Jobs flat. Grouping them took about 15 lines and no new drawing. So, in this order:

1. **Open the same view on 2 or 3 other pages at the same level**, other SPACEs too, and measure them: cards or rows, height,
   sideways scroll.
2. **Name the one difference that makes this page read worse.** It is usually the content's shape (too many items, no
   groups), not the wording or the styling.
3. **Fix that difference with what the page already has**: the same renderer, and the data it already holds (b01's `bands:`).
4. **Keep the kind of view the reader named.** Asked about a mind map, leave a mind map. A new kind of drawing, or the
   same change on every page, is the reader's choice, never yours.
5. **Make one change, look at it live beside the page you compared with, then report.** If the reader still dislikes it,
   go back to step 1; don't stack a second patch on the first.
6. **Write the shape down** in the skill that owns the view, so the next page starts from it (a map: `haipipe-mindmap`,
   "The Block map").


## Five rules

1. **Where am I, on top.** The path, then the title-&-section, then the view-button-list, then the goal-line
   (Mission for a Project and above, Purpose for a Theme or Block, Goal for a Job, Aim for a Task). Nothing else
   lives up there: no section buttons, no level dropdowns, no counts, and no count line under the title; a
   right-rail item carries none either (JL 261031, b10-s33-D05: "Don't add N topics, N jobs, they are useless,
   they will change along the way"). A PROCESS title names the step, never a count ("🙋 Decisions waiting for
   you", not "🙋 7 decisions waiting for you"; JL's rule "labels carry no counts", decided 261101): the pills carry
   each row's state.
2. **One place, one job.** left-rail: change page (siblings, the current page's children indented). right-rail:
   change section. Under the title-&-section: the view-button-list of the open section (JL 261029: the buttons stay
   on top; JL 261031, b10-s33-D04: Studio's groups too, "if it is the view based, we will put it above the
   Purpose"), then the goal-line (the same in every view), then the view-caption. Centre: content. Every section
   has a view-button-list, one button naming it when it has one view, so the goal-line never moves.
   Both rails are pale short lines until hovered (JL 261028: "I don't want to make them too obvious").
3. **Every section has a verb** (the Sections table below): it decides what the section holds. On screen the
   title-&-section shows only the name, on paper pages too (JL 261031, b10-s33-D06: "no verb, like every page"),
   and its right-rail item says in a few words what it holds ("its Jobs", "what happened when"), never a count.
4. **Content first.** No instruction paragraphs (they go in Guide). What a section holds shows directly, one item
   per line (JL 261028: "要么你就把它列出来 要么就把它去掉"). A fold may close a group of items (JL 261102: "group
   them by topics and then we can open and close them"), but its closed row still says something: a mark row and a
   tally (a dot per item, "21 of 24 answered"), and the most important group opens by default. A large view (a drawing, a mind
   map, slides) opens in a popup over the page and closes back to the same place. One exception: a view's
   sections (a heading each) fold by their heading, open by default, the reader's choice kept in the browser (JL
   261031: "for the view page's subsection, could they be like collapse as well"); nothing opens folded.
5. **Every mark has a word.** No unlabeled dot, pill, bar or icon: a state is a word ("explore", "agreed",
   "waiting for you"). A row of dots, a strip or a progress bar is allowed when a tally in words sits beside it
   and each mark has a hover title (JL 261102 liked the matrix cells' pages bar and X D I K W strip); a meaning held
   only in a hover title fails, since a reader and a screenshot never see it. An action is a verb button on its row (`Draw`, `Mind map`, `Slides`, `Open`), at most three.
   Names are the real folder and file names.


## The person's page rules (a checklist)

What the person has asked for again and again (261029 to 261105), in one place. The walk checks each on the live page,
and a reviewer scores Plain, Modern and Complete against it. A page that breaks one is not done.

1. **Seen at a glance.** The main point first and largest ("一眼就能看出来这东西是干啥的"); never a page of headings.
2. **Few words, nothing missing.** Short and fully presented: cut words, never information.
3. **Closed by default.** Every numbered section starts closed and opens on a click ("默认的话，大家都是合着的"); a large
   thing opens in the pop-out. The mind map is the one thing always shown, and a Section's Text view stays open (it is
   the text itself). A closed bar still says where it stands (261106): its **state word** on the right (answered,
   2 wait for you, 3 of 5 done, nothing yet, current), read from the section's own content, never a fixed decoration;
   a section that waits on the person also shows **that one waiting item under its closed bar**, outside the fold
   (Findings' answer waiting for agreement, 🙋 Interaction's first open question, a Process step's first waiting row).
   Paper bars: `ui_parts._section(title, body, word, waits)` (`<span class=word>`, `<p class=fd-wait>`); work bars:
   `focus_page.band_sec` (`<p class=band-wait>` after the fold). The fold remembers a bar by its title alone. A count
   may be a state word when it is the answer ("2 wait for you"), never part of a title.
4. **Left tabs, right content.** A list of items is side tabs: the names on the left, each with its state word, the
   open one's content on the right, each side with its own scroll.
5. **One standard part, everywhere.** The same part looks the same at Block, Job and Task, on every theme; 🙋
   Interaction is the last section of every Report and Work view, and it shows **that view's own items** (261106): on a
   paper Board the forms whose `for:` topic is one of the view's parts (a form about no part by where it was asked: an
   evidence Job's under Evidence or Displays, the rest under Writing); on a work page the forms at a Question's work
   under Findings, the forms below the page under Status, the page's own under MindMap; on a version, Section or
   evidence Job page its own forms (`focus_page.view_items`). The rail's Interactions keeps everything at the page or
   below; an empty view says "Nothing asked yet.".
6. **Report shows; Work does the same views.** Work is Process, then the same Results the Report draws, by the same code;
   switching sections keeps the view.
7. **Embed the real thing.** A drawing, a site, a paper or a map is shown in place, never described; every address is a
   link.
8. **An emoji and a plain name for each section; one question per view.** Two views that answer different questions
   are two buttons; one that repeats another goes.
9. **Flag what needs the person.** A question waiting, a proposal to agree, a fixed thing: each marked where it shows.
10. **Delete what is not needed.** Shown once: no step repeats a section (Process never repeats 🙋 Interaction, 261105);
    an unneeded line, row or view is removed, not kept "just in case".

How to work on a page: walk it in Chrome before showing it; when it reads badly, compare it with a page at the same
level first and name the one difference (0.4.3); keep what was agreed on a rebuild; record a big decision on the
topic's face so it holds.


## Sections: one verb each

```text
section    verb        holds                                         its view-button-list
Report     check       the results and the progress                MindMap · Status · Findings (Block, Job, Task; a
                                                                    theme's own views replace them, as a paper Board's
                                                                    Idea to Writing); MindMap · Findings · Themes ·
                                                                    Status above the Block
Work       do          the same views as Report (work theme,         same buttons as Report (· Deliverables);
                       paper Board): Process, then the same Results  elsewhere Progress (· Deliverables)
Studio     think       sNN topics: slides, drawing, mind map        one button per group, no All; Other last;
                                                                    Topics when no topic has a group
Interactions answer  every interaction at this page or below       All · Needs your input · Answered (always on the
                                                                    rail, Project to Task; "nothing asked yet" when empty)
Delivery   hand over   what leaves this folder for someone else     its lanes, each previewed; always on the rail
Related    take in     meetings, papers, emails that came in        Related (one button)
Timeline   look back   what happened when: commits, Runs, passes    Timeline (one button)
Skills     use         the skills that work on it, most relevant    Skills (one button): side tabs, each skill's line,
                       first: theme, level, its views', its Runs'     version, SKILL.md and a Copy prompt on this folder
Files      browse      the folder itself, its tree                  Folder (one button)
```

1. **Report** is what we know and how far we are (JL 261029: Overview became Report); **Work** is what we did and are doing; **Studio** is how we think about it.
2. **Delivery** goes out; **Related** came in. A section with nothing in it does not show.
3. **Studio groups** are the view-button-list, one per group, opening on the first; no "All" (JL 261029:
   "we don't have All, we just have each for each group"); topics with no group sit under a last button, "Other".
   An sNN has no page of its own (JL 261031, b35-s02-D05): a link to it, the left-rail's included, opens its card in
   its level's Studio, under its group, outlined; the card's name and line open its face, its picture its slide,
   every button in the pop-out.
4. **Timeline** is its own section on the rail (JL 261029), built from git, Run receipts and passes; never a folder. **Questions**
   (hypotheses, acceptance) is its own view: what we plan to learn, kept apart from what we know.
5. **Files** (the folder tree) is its own section on the rail (JL 261029: "the files should be in the right
   rail"): where you put your hands on the actual files.
6. **No two views repeat.** Above the Block, Report's views each answer one question: MindMap how it is built,
   Findings what was found (each answer's first sentence; proposals waiting for you first), Themes what each Block
   is for, Status how far each Block has got. Every view says what it shows in one line above its content.
   A Block, Job or Task has its own MindMap too: what it must find out, its Jobs or Tasks or Runs, its topics. A Job's
   map draws each Task with what it must find out (its goal, a `finds out` leaf) and a Task's map each Run with its
   `says:` (261106, decided on the lean): never the Run tree with its marks, which Status shows.
   A Block's Status groups its Jobs by band (j0N, j1N, ...; `bands:` in board.md names them) as numbered sections that
   start closed: `N · <emoji> <band>`, one state word, then a thin bar (JL 261104: "I prefer to me make it like the sections").
   Words sit left of the bar and every bar has one width on the right edge, so long words never push a bar out of line.
   Opened, one row per Job, and a Job's row opens to its Tasks and Runs, the same `fold_tree` as Work, each name opening
   its pop-out (JL 261104: "each job each row, and we can collapse them out to see the tasks and runs"; "这个做得很好").
   No next-step sentences on these rows (JL 261104: "I don't want this, just delete them").
   A Block that designs a theme (`theme:` in board.md) adds **Block UI · Job UI · Task UI** after Questions (JL 261031):
   each is a real page of that theme, live in a frame, named by `ui-block:`, `ui-job:`, `ui-task:` in the face. A Tools
   theme Block names a placeholder inside Tools by its path from the Tools root (`blueprints/Project-Ladder/...`): the
   workbench finds it from the Block's own checkout, so it frames in any SPACE (`Tools/blueprints/...` there) and on a
   Tools server alike (261105). Tools is public, so never a real project's page; an http(s) link to another machine's
   server only until the theme has a placeholder, since it breaks off that machine. Pick a full example, one with
   Tasks, Runs and Results (paper: Paper-Example; labeling: b02_labeling_walkthrough; work:
   b90_example_paper_results), never the first folder on disk; a level the theme does not have gets no button.
   One line per kind of page at a level (JL 261105: "they are all the task, but different UI"; "for the paper's job,
   we might have different versions"): repeat `ui-task:` (or `ui-job:`) for each kind, the first the one walked, and
   the view shows them as side tabs, the kind on the left (its `task-type:`, or a Job's folder words) and the page live
   on the right. A paper Board's Jobs: the writing version, the display, value and citation Jobs, the submission; its
   Tasks: a Section, the cover letter, a display, a value set, a citation, a portal step. A kind of page with no
   example on the prototype is a gap to fill (labeling has no items or embedding Task yet). Work on each of these
   views is ⚙️ Process, then the same Results: 🎬 Walks to record (each kind with no walk yet) and 🔍 Review rounds
   (each kind's newest round, read from its review file's `page` and `score` lines, or "not reviewed yet").
   A work page has no Questions view (JL 261104: "we don't need the questions"). A work Block's **Findings** is a quick
   overview of the results it got and what it hands over (JL 261104: "the quick overview of the results we get from that
   block"), shaped like a paper Board's Evidence: numbered closed sections, each with side tabs, a list on the left and
   the content on the right (JL 261104: "left tab panel right content"). 🔢 Values first, when a Job holds a `tables.json`;
   then the Questions by `group:` (one section, Answers, with fewer than two groups), each panel what it asks, its answer's
   words and the first result line of each Task under its `work:`; then 🧠 Maps, one tab per mind map in a Task's newest
   `runs/*/result/maps/` (JL 261104); last 📦 Delivery, tabs Models · Data · Website (JL
   261104: "fold / merge the delivery to the Findings"). Delivery stays on the rail too.
7. **Work has the same views as Report** (work theme, Block, Job and Task; JL 261104: "why we have the progress? it
   should have the same view to the report"), as on a paper Board: ⚙️ Process first (closed: 🙋 waiting on you, the
   view's things to do, 🧰 skills), then 📊 Results, the Report's view drawn by the same code. Work opens on Status, whose
   rows add each Task's output and the Answer button; a Task's Results are its Runs with their output. A paper version
   (a writing Job) does the same (261106, decision 1): its Report is its Work's six views, Draft-Main · Draft-Appendix ·
   Display-Main · Display-Appendix · Values · Citations, results only, MindMap first; a Draft view's Results are each
   Section's text, one side tab per Section (t00 to t19 main, t20 to t39 appendix), and its Process the Sections' step
   words. A paper Board's evidence and submission Jobs have views of their own, never the old Progress view (261106):
   display Job Plan · Displays · Examples; value Job Values · Check (its t99 check Task); citation Job Citations · Check;
   submission Job Cover letter · Portal (`servers/workbench-paper/paper_jobs.py`).
8. **Report shows, Work asks** (JL 261102: "the questions should be in the Work, for the report, we just show the
   report"). A Report view may be explored (hover, pin, compare, folds, a share link) but holds no Ask box, Copy
   prompt, propose or sign control; those live in the same letter's Work view, over the same picture.


## The page at each level

```text
level     its page          opens on    Work lists           Studio and Delivery show
Project   project.md        Work        its Themes           its own + every Block's
Theme     <theme>.md        Work        its Blocks           every Block's
Block     board.md          Report      its Jobs             its own + its Jobs' and Tasks'
Job       jNN_<job>.md      Work        its Tasks            its own + its Tasks'
Task      tNN_<task>.md     Work        its Runs (+ draft)   its own
```

Rolled-up items carry where they live (`s22 · j02`). A Block opens on Report because its Questions are what it
exists to answer; every other level opens where its goal is judged, its Work. A draft Task (`task-type: draft`, b32 s42) has a
view-button-list per section: Work is 1 · Plan · 2 · Write · 3 · Evidence · 4 · Display · 5 · Revise · Runs, each
step's state a word on its button; Report is MindMap (the paper content) · Text (sentence by sentence) · Status; Studio and Delivery stay on the
right-rail. Under each view the content is sections, a heading each, never folds (JL 261031).


## Rows

1. One item, one row, full width: its real name, one line of what it is, its state word, its verbs.
2. A drag handle, an edit control or a group picker shows only on hover or focus.
3. A row's picture (a figure, a drawing preview) shows in the row; a click opens it large in the popup.
4. **A Studio row shows four things** (JL 261029: "the information here is a bit overwhelmed"): its picture (the
   lead idea slide, else the drawing), its name `b17-s04:theme_work @ workbench_page_structure`, the one line it asks,
   its stage as one word; then Slides, Draw, Mind map. Rounds, open ideas and tags stay behind the name.
5. **A to-do row** (PROCESS, b16 s33-D06, from b15 s58): one full-width row per thing to do: its words, its state as
   a coloured pill (orange waits on you, blue running, green done, grey not started or open), and one verb (Answer,
   Open, Open Plan).
6. **A plan row** (Data + Paper Plan's PROCESS, the plan center, b16 s33-D07): one step of the plan per row: its name, "use
   /<skill>", Open (the thing the step works on) and Copy prompt (the prompt sends a session to that thing and asks
   for the plan before any change).


## Designing a page: one view, one screen

How a page's design is drawn and settled in its Studio topic, before any code changes (JL 261031: "we might want
to update them one by one ... you should have the A, B, C, D"; "could you make each of them to be the same size and
format"; "for the UI, what is the principle"). One topic per page level × section, numbered in the theme Block's own
sNN band like any Studio topic (b16 s32 to s40: Board, version, Section × Report, Work, Studio). `<level>` below is
the page's own word in that theme (the paper theme says board, version, section). A theme's page may have views of
its own instead of the table above (the paper Board's seven views, Idea and Story to Writing, Venue inside it,
s32-D12); they still pass the five rules, and
no view repeats another or a right-rail section (Timeline, Delivery, Interactions stay sections).

1. **One view, one screen.** Draw every view of the section as the full screen it will be: window, path,
   title-&-section, view-button-list with this view marked, then its sections as heading bars, one line under each.
   Never one big sample beside tiny thumbnails: a view drawn small is a view nobody reviewed. The drawing marks the
   open view in orange so it reads at a glance; the built page keeps the workbench's own blue (rule: never restyle).
2. **Same size, same format.** Every screen is as tall as the longest view, three to a row, so the reader compares
   views, not drawing styles. Words are placeholders (a Tools blueprint is public); names are the real field names.
3. **Letters.** Views are lettered A, B, C … in button order. The letter names the screen, its decision
   (`sNN-DNN`) and its delivery file. When Report and Work list the same views (the paper Board), they share
   letters, so A means the same view on both; otherwise each section letters its own list from A.
4. **One round per letter.** A round settles one letter: decide it, build it in the workbench code, check it live in
   Chrome, then mark the screen with a green `✎ <YYMMDD>` note. Then the next letter. Nothing is settled in bulk.
5. **Done means a file.** A letter is ✅ only when `delivery/ui/<level>-<section>/<L>-<view>.html` exists, written by
   the topic's builder; nobody ticks it by hand. The topic hands over two pieces: the screen code (into the theme's
   workbench server) and the views' manual (`delivery/skill/<level>-<section>-views.md`, rendered into the theme's
   workbench skill), both named in `delivery/render.yaml`.

```text
s32 board · Report    A Idea ✅   B Story ✅   C Data + Paper Plan ⬜   D Support blocks ⬜ … G Writing ⬜
round p01  A ─▶ code ─▶ checked live ─▶ ✎ 261031 ─▶ delivery/ui/board-report/A-idea.html
```

The model builder is `blueprints/Project-Ladder/work/b16_theme_paper/j01_paper_workbench_pages/paper_ui_cells.py`
(`VIEWS`, `screens`, `AGREED`); another theme's page-UI topics copy it. Each letter goes through the Design loop
below, on its drawing first and on the live page after, before its ✅.


## 🔁 Design loop (a must)

A design is not done when it is drawn or built: it goes round until every rubric passes, so the page is one people
can use (JL 261031: "make it design again and again, until the different rubrics are met"). The same loop as
`/haipipe-display`'s revise loop, with the page rubrics below.

```text
stage 1 drawing ─▶ review r01 ─▶ pass? ─ yes ─▶ 🙋 JL looks once ─▶ build ─▶ stage 2 live page, same loop ─▶ ✅
                      ▲              │ no (fewer than 4 rounds)
                      └─ rNN ◀────── revise the three fixes, re-render
after r04 with no pass ─▶ stop; hand JL the open rubrics and the three fixes
```

1. **Two stages, one loop each.** Stage 1 reviews the drawing (the letter's screen in the topic's PNG), before
   any code. Stage 2 reviews the live page (`scripts/shoot.py`, 1440 px and 390 px), after the code. Rounds count
   from r01 again at each stage, at most four per stage.
2. **Re-render.** The topic sits beside its face in the theme Block (b16: `j01_paper_workbench_pages/t0N_*/sNN-*/`);
   its own builder `build_sNN_<topic>.py` redraws the `.excalidraw` and the PNG (it calls the shared cells file,
   `paper_ui_cells.py` for b16). Change the cells file or the builder, never the drawing by hand.
3. **Blind review.** Each round spawns a NEW general-purpose agent (Agent tool; never the designer, never the round
   before's reviewer, never haipipe-studio-reviewer-agent, whose brief is different) with the Review brief below,
   pasted verbatim, and only the picture(s), the letter's address, and the settled decisions it must not undo (the
   face's `sNN-DNN` lines and JL's own request for this round). A fix that would undo one is not applied: it goes
   to JL as a question (b16 s32 B r01 asked to split Venue out of Story again, the merge JL had just asked for).
   Reviewers disagree from round to round (a round asked to open the first fold; the next marked that open fold a
   wall of text), so a fix applied in an earlier round goes to the next reviewer as settled too, named with the
   round that asked for it; a reviewer who would undo it raises it as a question, and a rubric that dips only because
   of such a reversal is not a regression.
4. **Record.** The review text goes verbatim to `<topic>/review/<L>-s<stage>-rNN.md` (for example
   `review/B-s1-r02.md`). When a round passes, the letter's decision line in the face (`sNN-DNN`) names that file.
5. **Revise** the three fixes the review names, re-render, and go round with a new reviewer.
6. **Pass rule.** Every rubric 7/10 or more, and the mean 8/10 or more. A rubric that does not apply at a stage
   (Phone at stage 1) is marked n/a and left out of the mean. After round 4 with no pass, stop.
7. **Between the stages, JL looks once.** When stage 1 passes, show JL the passed screen and its scores and wait:
   JL's yes is the "decide it" of a round. On that yes, build the code, then run stage 2 to a pass without stopping
   again; the builder then writes `delivery/ui/<level>-<section>/<L>-<view>.html` and the letter gets its ✅.

The designer never scores its own design, and a pass is not acceptance: it lets JL decide.

```text
rubric       asks                                                                   from
1 Glance     the four five-second questions, answered from the picture alone        five-second test
2 Place      top in order; left-rail pages, right-rail sections, centre content     rules 1, 2
3 Lean       no instructions, counts, ids, crumbs or fold arrows; one item a line;   rules 1, 4
             a PROCESS title names the step, never a count
4 Words      every mark a word; verbs on rows, at most three; real names            rule 5
5 One job    each view answers one question; nothing shown twice, no rail section   section rules 1, 6
6 Same look  the workbench's colours and boxes; reads like its sibling pages        the look, above
7 Phone      at 390 px: rails hidden, section-line shown, nothing cut off;          page parts 4, 5
             phone @media rules after the base rules they change
8 Salience   the view's main point first and largest; content shown (a picture,     JL 261031
             tiles, a chain), not only headings; the rest smaller, below
9 Works      the reader tasks done in few clicks, no dead end; every click, hover,  JL 261102, Walk
             pin, tab and pop-out does what its word says; no console error; a
             broken step or a task it could not do caps it at 4
10 Modern    reads like the paper UI: cards and air, one clear hierarchy, pictures   JL 261102, the bar
             and chains over tables of text, nothing cramped or wrapped badly
11 Plain     a word budget: one line under a heading, no paragraph over two lines,   JL 261102
             no grey sentence; detail waits behind a hover, a pin or a click
12 Complete  every field the view's data holds is reachable, shown or one click     JL 261102
             away; a redesign that drops one fails, however clean it looks
```

Rubrics 9 to 12 are stage 2 only (n/a on a drawing), scored from the walk (JL 261102: "make it modern layout, and
do not make it too word, hard to read, and do not miss the information").

Salience (JL 261031: "it should highlight the main point ... the layout should be great, to show the content
saliently, currently it is very boring"): a view whose sections hold only a heading and a gray line fails it,
however clean. The shape that passes, kept the same in every view (JL 261031: "I still want each section to be the
[heading bar] ... seems to be ordered"; "at the bottom, we should check the Interaction, Draw"):

1. **Two bands, RESULTS and PROCESS.** Every Board view is two bands, each numbered from 1: RESULTS is the view's
   own sections, PROCESS is how the layer is being made, step by step (the view's to-dos, each a to-do row; Data +
   Paper Plan's is the plan center, in plan rows; 📌 Open points first when a part's face marks some). The open forms
   are never a PROCESS step: they show once, in the view's last section 🙋 Interaction (261105, "keep only the
   bottom"). Report reads RESULTS first, Work PROCESS first;
   RESULTS is drawn by the same code on both, so the two never disagree (b16 s32-D22, s33-D03).
2. **Numbered heading bars, in reading order.** Every section is a boxed bar `▾ 1 · 🧭 <name>`, `▾ 2 · …`, folding
   by its heading; the numbers, from 1 in each band, make the view read in order. Each section name has one emoji,
   the same in every view (🧭 Direction, 💡 Pitch, ❓ Questions, 🏛️ Venues, 🖼️ The drawing, 🧠 The mind map …),
   always beside its word. A PROCESS title names the step, never a count.
3. **The main point is section 1**, shown large under its bar: one sentence and its state word, no coloured edge
   (JL 261031: "I don't want to have this").
4. **Content shows as what it is** under each bar: things a reader compares as cards side by side, a sequence as
   a chain of boxes with arrows and role words (target, fallback 1), dated steps as a timeline with a state mark
   each (✅ done, ⏳ running, ⬜ not started), a plain part as one line.
5. **Side tabs, the one kind of tabs in a view** (JL 261104: "please change all type of these into this style"; they
   replace the card tabs of JL 261031): the list on the left, the first open, one open at a time, the open item's
   content on the right, its Open button inside (RQ1, RQ2, RQ3; each direction considered; each journal; each Section,
   display, value set; each related paper, its PDF embedded). `_grouped_tabs` adds a small group name above each group.
   The general pattern is master–detail; the standard parts are `tablist`, `tab` and `tabpanel`. In Report, a panel shows
   the thing to read, never the steps that make it ("we just report the report").
6. **Helpers at the bottom**, unnumbered, after a dashed rule: the drawing and the mind map only. 🖼️ The drawing
   (its picture, Slides · Draw), 🧠 The mind map (a button that opens it in the pop-out; drawn inline it repeated the
   face). 🙋 Interaction is not a helper: it is the last numbered section of every Report and Work view (261104), the
   one place a form shows (261105; it was PROCESS 1 from b16 s32-D22 to 261105).

`paper_ui_cells.py` draws this (`band`, `sec_block` with `big`, `cardtabs`, `cardtabchain`, `chain_only`,
`narrative`, `sidetabs`, `todo`, `one_line`, `ask`, `picture`). The live code: `servers/workbench/ui_parts.py` holds the
shared pieces (`_side_tabs`, `_band`, `_pill`, `_todo`, `_plan_html`, `PB_CSS`), and
`servers/workbench-paper/board_*.py` the views: `board_results.py` one view function per paper part (`idea_view` to
`writing_view`), `board_process.py` the PROCESS band, `board_views.py` the two bands put together (`banded`).
`focus_draft.py` is the draft Task page only. b16 s32's seven views A to G are drawn and built this way.


## Walk (Chrome: the page as a person uses it)

A screenshot never clicks, hovers or opens anything, so a still-shot review passed a canvas whose hover lit up the
wrong links (JL 261102: "call it in the chrome and you click it and you review it yourself"). Before any stage-2
score, the builder walks the live page in the person's Chrome through the claude-in-chrome tools (load them in one
ToolSearch: `tabs_context_mcp`, `tabs_create_mcp`, `navigate`, `computer`, `read_page`, `find`,
`read_console_messages`, `resize_window`, `gif_creator`), in a new tab of its own.

```text
open ─▶ every view button ─▶ every interactive thing ─▶ 390 px ─▶ console ─▶ the paper bar ─▶ notes + GIF
```

1. **Reader tasks first.** Before clicking, write 3 to 5 tasks a person has on each view, as goals, not clicks
   ("find what K15 rests on", "which Job moved the method", "what will Stage 2.5 send"). Do each from the page alone
   and record the clicks it took, any dead end, and any task it could not do. Works is scored from these tasks; the
   steps below then catch what the tasks did not touch.
2. **Every view.** Click each button of the view-button-list and each right-rail section; screenshot each, the
   whole view (scroll it), not the first screen only.
3. **Every interactive thing**, one at a time, saying what should happen before checking that it did: hover a
   canvas card (what lights up, and is it right), click to pin and walk its chips, open a side tab and a
   pop-out and close it again, a `#…` share link, a fold, a search box, a Copy prompt (it copies, it posts nothing).
   Never press a button that writes (a sign, Review and approve, a release) unless the person asked: name it and skip.
4. **Phone.** Resize to 390 px wide: rails hidden, section-line shown, nothing cut off or scrolling sideways. A
   maximized or full-screen window ignores `resize_window` (the first design walk, 261102): check the screenshot's
   width, and if it did not change, shoot the phone view with `scripts/shoot.py --width 390` instead. Headless
   Chrome's `--window-size=390,…` is not a 390 px viewport either (Chrome keeps a minimum window width, then crops,
   so every view looks cut off on the right): the true check is the DevTools protocol,
   `Emulation.setDeviceMetricsOverride(width=390, mobile=true)` then `Page.captureScreenshot`, over Chrome's
   `--remote-debugging-port` (the same port also walks clicks with `Runtime.evaluate` when the extension drops).
5. **Console.** Read the console once at the start (tracking begins at the first read), reload, then read errors
   only; any error is a broken step.
6. **The paper bar.** Open the paper UI's matching view (the paper Board's view of the same job: its Story or
   Writing side tabs for a list of things compared, its Data + Paper Plan rows for steps) and say, per view, where the
   page falls short of it, in words: "denser than paper's Story side tabs", "no picture where paper shows one".
7. **Notes and the walk video.** One line per step: `✅ | ❌ | ⚠️ <what was done> → <what happened>`. The video is
   recorded by script, one per kind of page (JL 261105: "a very quick video and we can pause in the middle"; "they are
   all the task, but different UI"):

   ```bash
   python scripts/walk_all.py <theme Block> [--origin http://127.0.0.1:<Tools server>]   # every ui-* kind, one walk each
   uv run --no-project --with playwright python scripts/walk_shoot.py <page url> <frames>  # one page: frames + captions
   python scripts/walk_player.py <frames | walk.gif> <out.html> --title …                  # the player: pause, step, speed
   ```

   `walk_shoot.py` opens a fresh browser that can only read (GET), visits each section and view, opens each closed bar,
   clicks side tabs and a pop-out, outlines each target, and writes `NN.jpg`, `captions.txt`, `notes.md` (✅/❌ per step)
   and `errors.txt` (page errors). A theme Block keeps the players as `walks/<level>-<folder>.html` (the first kind also
   `walks/<level>.html`); its Report's Block UI · Job UI · Task UI show them as 2 · 🎬 The walks, the same side tabs as
   1 · 🖥️ The pages, live, and its Work lists the kinds with no walk yet. Record on a server rooted at Tools, so the page
   path names no SPACE. Rerun `walk_all.py` after every round; an empty recording never replaces a walk. Fix every ❌
   and re-walk before any review; a ⚠️ (works, but confusing) goes to the review. The script records; it does not
   judge: reader tasks, hovering a canvas and the paper bar stay the Chrome walk's (steps 1, 3 and 6).
8. **Builder walks, a fresh reviewer scores.** The walk proves it works; it is not a score (the builder knows what
   each mark means). The Review below then scores the page, from its own Chrome walk when it has the tools, else
   from the walk's screenshots, notes and GIF.
9. **Tools is public.** A walk of a real project's page stays in the session; what is saved into Tools (a review
   file, a GIF) comes from a Tools placeholder page only (Review, below), or quotes no real names, texts or numbers.

When Chrome does not answer (no extension, a tab error twice), stop and say so; never fall back to calling a still
screenshot a walk.


## Review (one round of the loop)

Run after every UI change, before calling it done (AGENTS: "wire green is not UI green"). The reviewer must be a
fresh subagent that did not build the page: whoever built it already knows what each mark means. At stage 1 the
reviewer gets the drawing instead of a screenshot, skips step 1, and its `page` line names the letter instead of
a URL (`s32-board-ui-report · B · stage 1`).

**Review on Tools' own placeholder page, never a real one** (JL 261101: "you are working with the Tools"). Tools is
public, and a review quotes what it sees, so a stage-2 review screenshots a theme's placeholder: the paper Board
`blueprints/Project-Ladder/paper/Paper-Example`, the work Block `blueprints/Project-Ladder/work/b90_example_paper_results`,
the labeling Block `blueprints/Project-Ladder/labeling/b02_labeling_walkthrough`. On a server rooted at Tools the path
is as written; on a SPACE's server it is under `Tools/`, e.g.
`http://127.0.0.1:<port>/_board/workbench?path=Tools/blueprints/Project-Ladder/paper/Paper-Example&layout=focus&section=work&group=work-plan`.
Their faces hold `<…>` placeholders only. A bug seen only on a real paper is diagnosed by a new session in that paper's
own SPACE, which reports back the Tools file and line; the reviewer never opens the real paper.

1. Walk the page (Walk, above), or read the builder's walk notes and GIF; then screenshot it at 1440 px wide (and once
   at 390 px for a phone):

   ```bash
   uv run --with playwright python <this skill>/scripts/shoot.py <url> <out.png> --width 1440
   ```

   The whole page is the default (`--viewport` takes only the first screen): b16 s32 A and B's first live round,
   shot at the first 1000 px, left everything below the fold unscored.

2. Look at the screenshot first, the HTML only after. Answer the four five-second questions from the picture
   alone, in one line each, and say which you could not answer.
3. Check the five rules and the section table: pass or fail each, with the exact thing on screen that fails.
4. Score each rubric of the Design loop out of 10, with the exact thing on screen behind any score below 10; a
   question not answerable from the picture costs Glance 3 points, a partly answerable one 1. Give the mean.
5. Name the three fixes that would raise the lowest rubrics most, each as "move/remove/rename <thing> to <place>".
6. For Complete, list the view's data (the fields its reader function reads) and mark each shown, one click away,
   or missing.

Return format, under 300 words:

```text
page     <url>, or <topic> · <L> · stage 1
answers  what: … · where: … · here: … · do: …
rules    1 ✅|❌ … · 2 … · 3 … · 4 … · 5 …
tasks    each reader task: done in N clicks | dead end at <what> | could not
walk     N steps · N ✅ · N ❌ · N ⚠️ (the ❌ and ⚠️ named)
bar      where it falls short of the paper UI, in words
rubrics  Glance N · Place N · Lean N · Words N · One job N · Same look N · Phone N|n/a · Salience N ·
         Works N|n/a · Modern N|n/a · Plain N|n/a · Complete N|n/a
score    mean N/10 · pass|not yet
fixes    1. … 2. … 3. …
```


## Files

`scripts/shoot.py` takes the screenshot (the installed Google Chrome, headless, through Playwright); the walk uses
the person's Chrome through the claude-in-chrome tools, no script. `CHANGELOG.md` records changes.
