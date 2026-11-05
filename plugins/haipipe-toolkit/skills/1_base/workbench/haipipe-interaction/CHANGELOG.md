haipipe-interaction · Changelog
===============================

0.10.0 · 2026-11-05 · what you should know

- JL 261105: "it should include both ask question and keep what you should know". New `collect.py know`: a notes Run,
  one per topic, state "to know", waiting on nothing; `applied` flags a note settled. Workbench: `focus_page.interactions`
  gives the state and `interaction_item` a Read button; the empty section's words name both kinds.

0.9.2 · 2026-11-04 · one look

- JL 261104: "make this to be the standard items for any of them". The rail and the pop-out draw the same section as a view's bottom; a Run with no built form keeps its plain row.

0.9.1 · 2026-11-04 · a question's why reads in full black

- JL 261104: "the font color is not that readable". `.lead`, `.why`, `.because` and the sketch now use the page's text colour; a waiting form takes it at its next build.

0.9.0 · 2026-11-04 · every view ends in Interaction

- JL 261104: "could you try to make this section at the bottom for each of the view? not matter for the block, or job or task". The form and its record are unchanged; the paper Displays row gave way to it.

0.8.7 · 2026-11-04 · a Story's questions have a place

- A paper Board's Idea + Story ends in 🙋 Interaction (workbench-paper 0.46.0); the form and its record are unchanged.

0.8.6 · 2026-11-03 · a paper's display questions have a place

- JL 261103: "please update ... the /haipipe-interaction as well". A question about a paper's displays (which
  version, which layout, keep or drop) is a collection Run in `j01_evidence_display/runs/` or the display Task's
  `runs/`; the paper workbench shows it in G · Displays, 4 · Interaction, and haipipe-paper's checklist line V8 waits
  on it. SKILL.md's Where it shows lists the entry.

0.8.5 · 2026-11-03 · the combined page stops growing

- JL 261103: "why this box of Q1 is increasing along the way?". `bundle`'s page resized each form every 1.5 s to its
  document's scrollHeight + 8 px; a document is never shorter than its frame, so every form grew 8 px a round, forever.
  It now measures the content's own bottom (fixed pop-outs left out) and changes the height only when it differs by
  more than 2 px. Checked in Chrome on b16's answer_all.html: 8 forms, the same heights 6 s apart, each ending at its
  last line.




## [0.8.4] — 2026-11-03

A preview pops out when clicked (JL 261103 on the ScalingGlucose display form: "could you make the options here to be
pop out when I click them?"): the click still picks the option, and the preview opens over the form at full width;
Close, a click outside it or Esc shuts it. Open ↗ still opens it alone in a new tab. `preview_html`, the `.pop` style,
`hpPop` in the form's script.

## [0.8.3] — 2026-11-01

A form with nothing picked, from b15's flow simulation (Tools blueprint b15_theme_labeling, j01 t03
runs/r02_simulate_task_workflow): a labeling decision report never preselects an option, and three things read wrong.
- The form's head said "My pick is selected"; with no pick it now says "Nothing is picked for you".
- The answer file said "Answer: A, changed from my pick ." when nothing had been picked; it now says "Answer: A.".
- `save` builds the form again, its build stamp kept, so the answered form reopens read only with the person's picks
  (it showed Copy feedback until someone rebuilt it).
Tests: test_a_form_with_nothing_picked_says_so_and_answers_without_my_pick, test_a_form_with_my_pick_keeps_its_words.

## [0.8.2] — 2026-10-31

Two rules from JL's first answers to b17's theme-alignment form (261031):
- One column per option. 0.6.8 said to set two places side by side; JL: "why we have two columns? I think we should
  just have one columns for each of them". Two screens at half size were unreadable, so the places now stack, one
  under the other. b17's nine waiting cell forms were rebuilt that way (36 of 131 previews had two columns).
- No bookkeeping questions. Three of that form's four questions asked about topic numbers and folders, and JL answered
  each "I don't understand". The agent decides numbers, folder names and renames; a question asks in the words of what
  the person sees.

## [0.8.1] — 2026-10-31

See answers opens a page, never raw Markdown (JL 261031: "the UI here doesn't good"): the workbench's button opens
the answered form (focus_page.interaction_item, focus_draft.ix_item); `record` writes each chat record a read-only
page, `<run>.html` (record_page). The five existing records were rewritten.

## [0.8.0] — 2026-10-31

One theme, one set (JL 261031: "why each question set just a few questions? we can have longer question list";
"each question set should have a things like theme"; "make it to check all the interaction question sets for now").
A set holds up to 20 questions (was 6). `record` appends a topic's chat decisions to its one record (decisions.yaml
keeps them; each line on the workbench is the decision, not "What was decided?"). New `collect.py audit <top>
[--fix]`: split records (merged, renamed rNN_collect_<theme>_decisions, links updated), several waiting sets for one
topic, old records (rewritten), sets with no topic, short waiting sets under one Job. Run over Tools blueprints and
Physician-SPACE: b16-s01's four records became r04_collect_paper_tree_concept_decisions, s32's three became t01
r05_collect_board_ui_report_decisions, the rest rewritten.

## [0.7.1] — 2026-10-31

The link the person gets is the workbench page, the Block's Interactions section or the sNN's Studio row, never the
bare form file (JL 261031: "应该直接给我 block 链接或者 studio 链接对吧？").

## [0.7.0] — 2026-10-31

Combine, actively (JL 261031: "should actively think about combine the different interactions in to one
page"): `collect.py bundle <page>` writes `<page>/runs/answer_all.html`, every waiting form at or below the page
in one page with one "Copy all answers"; `collect.py save-all` saves that one paste, each block to the Run its
`form:` path names. Each form now exposes its answer text (`window.haipipeAnswers`) for the combined page; every
waiting form was rebuilt. Test: test_one_page_answers_every_waiting_form_and_one_paste_saves_each.

## [0.6.10] — 2026-10-31

The Interaction button is flagged, "🙋 Interaction" with an orange edge, when a question on it waits for the person
(JL 261031: "if there are some questions i need to answer, cuold you flag them as well"); plain when nothing waits.
Recorded: b16 t01 r07_collect_interaction_flag.

## [0.6.9] — 2026-10-31

A big decision made in the chat is recorded too (JL 261031: "the big decisions like this should also be recorded, and
add the status ... to be consistent in the future"). `collect.py record <page> <slug> --title --for --decision "title ::
what was decided :: their words" [--applied-by]` writes a done collection Run (`source: chat`): each question answered
"my own decision", the person's words kept, one pass, and with `--applied-by` the applied flag on each question. It
never waits, so a waiting form never blocks it. SKILL.md: the section "A big decision made in the chat is recorded
too". Test: RecordTest.

## [0.6.8] — 2026-10-31

Previews: the difference sits in the frame (JL 261031, on b17's r01 form: "I think you should show that what is the
expected UI / html looks like"). The form shows a preview at half size in a frame 600 page pixels tall, and r01's first
previews kept the part that differs below it (B's Delivery screen, Q5's Answers view, Q6's Status), so the options
looked alike. 2b now says to leave out what no option changes, keep rows compact, and set two places side by side
when an option moves something between them; a script writes the previews (b17's is
`t01_block_page/scripts/build_r01_previews.py`). Docs only.

## [0.6.7] — 2026-10-31

My own decision (JL 261031, on b17's r01 form: "you should have something like others: like I will add my decisions").
- Every question ends with one standard choice the Markdown never lists, "✍ My own decision".
- Picking it turns the note box into "Your decision (required)".
- The copied line is `QN · <title>: my own decision`, and `picks()` reads it, so the answered view shows it too.
- `save` refuses it with no words, and writes `Answer: my own decision.` and `> decision: <the words>`.
- The older-form word compare leaves the choice out, so adding it makes no form stale.
- Tests: 20.

## [0.6.6] — 2026-10-31

Applied flags (JL 261031, on an answered form: "if we already fix them, then give them the flags"). `collect.py
applied <run> Q1 … --by "<what changed>" [--state "in progress"]` writes `applied.md` beside run.yaml (never in
result/), one line per question, `Q1 · applied · <yyyy-mm-dd hh:mm> · <by>`; it refuses an unanswered Run, an unknown
question and an empty --by. The form reads applied.md each time it opens and shows "✅ applied <date>" or "⏳ in
progress <date>" on the card, with a line saying what changed; when the file cannot be read it shows nothing and
Copy still works. `build` keeps the stamp whenever the questions are unchanged, a waiting Run's too (b17's note): a
template change no longer makes an open tab's paste stale, and an answered Run's form may take the new template;
a changed question on an answered Run is still refused. haipipe-project's ladder lists applied.md in a Run.
An answered form shows the person's own picks and notes, read only, from the paste its answer file keeps, and
hides Copy feedback; before, a browser other than the person's showed my picks.
From a fresh-agent test: SKILL.md no longer says "applied" is never in this Run; it names the two required
records (the decision where its owner keeps it, the flag in applied.md), the hand-over rule (--state "in progress",
the next owner reruns applied), that a new flag needs no rebuild, and that a file-opened form may lack its flags. The
workbench's item shows the flags. The docstring lists `applied`.

## [0.6.5] — 2026-10-31

The workbench shows one button, "Interaction", where it showed two tags (🙋 Questions for you, ✅ Answered): no
count, no colour (JL 261031, b16 t01 r04 Q3 to Q6). It pops out the row's items, the waiting one first; an item shows
its title, state and date, its questions, and Answer or See answers. "Where it shows" names the new functions
(`interaction_button`, `interaction_items`, `interaction_item`) and the pop-out route. The form itself is unchanged.

## [0.6.5] — 2026-10-31

The form boxes what differs between a question's previews (JL 261031: "highlight the part that are different by
using the box"): a block-by-block compare of the pages (matched children, so a moved block counts), an orange box in
every option, each preview scrolled to its first box; `class="diff"` in a preview overrides the compare. Previews load
eagerly so the compare has every page. Every waiting form was rebuilt.

## [0.6.4] — 2026-10-31

Rule 2b: the previews differ where the options differ (JL 261031: "I cannot see the differences among the three
options"; b16 r04 Q1 showed the same MindMap three times, only the view buttons changed).

## [0.6.3] — 2026-10-31

Rule 0, extend before new (JL 261031: "I don't think you need to open a new run, you can extend the
current run"). A new question joins the waiting Run the person is reading; a new Run needs a good reason (none
waits, or another sNN under another page). The b16 Interaction-button questions moved into t01's waiting r04 as
Q3 to Q6; the extra b35 r02 was removed.

## [0.6.2] — 2026-10-31

From a fresh-agent test of 0.6.0 (it attached the form to the sNN that owns the question, and was refused an
address with no sNN). `new`'s two refusals name the page even when it is given as `.` (they printed an empty name).
SKILL.md says the link-only reply overrides the usual reply format for that reply.
## [0.6.1] — 2026-10-31

A new template alone never makes a form stale. `save` compared the whole form with what the current code renders, so
the 0.5.0 template refused every paste to a form built before it, even with unchanged questions. Two forms were hit:
b35's r01_collect_studio_followups, and the PDMP paper's r01_collect_draft_decisions, whose rebuild 0.6.0 also refuses
because its `for:` names no sNN.
- Each form now carries its questions as text (`<script type="text/markdown" id="haipipe-questions">`), and `save`
  compares those.
- A form built before 0.6.1 is compared on its question cards' words, not its markup.
- A changed question is still refused.
- A read-only check: all five waiting forms save without a rebuild (b35, b32, b10, b17, the PDMP paper).
- The sNN rule (0.6.0) is untouched. Tests: 18.

## [0.6.0] — 2026-10-31

Every interaction is attached to one Studio topic (JL 261031: "the interaction page should be attached to one studio
as well"). `for:` must name an sNN (`b17-s04:theme_work @ workbench_page_structure`): `collect.py new` requires
`--for` and refuses an address with no sNN, and `check` (so `build`) names it. The rule for "one waiting Run per page
when none names an sNN" is gone; an older waiting Run with no sNN still holds its page. SKILL.md says how to pick
the topic: the one that owns the question, not the one the talk started from; with none, start one first. `save` is
unchanged, so a waiting form built before 0.6.0 still saves. Tests: 17 passed (one new).
## [0.5.1] — 2026-10-31

Once the form is built, the chat carries no content: the reply that sends it is the form's link and nothing else (JL
261031: "after the UI is done, I will no long see any content from your response here"). The loop's step 5 said "one
line per question"; it now says the link only, and "Before sending the link" checks it. The agent's findings go on
the form (its intro, a question's why).
## [0.5.0] — 2026-10-31

The form is the conversation: the person reads the form, not the chat (JL 261031: "I will not read you response here, i
will just read this Intereaction UI"), so all they need to decide is on it. Options are shown, not only named: an
option may carry its own preview, indented under it, a live page `[preview](option-a.html)` or a picture
`![A](option-a.png)`; the form shows them side by side at half size, a click picks, Open shows it full size, and the
chosen one is outlined (JL 261031: "you can also make the option's preview results, liek the hmtl to be embeded here").
`check` refuses a preview whose file is missing; the answer file keeps the preview lines.
## [0.4.8] — 2026-10-31

One waiting collection Run per sNN, not per page: `new` refuses a second only when an earlier waiting Run's `for:`
names the same sNN (or neither names one). A Task with three sNN can now carry a form on each Studio row (JL 261031:
"we should add the interaction ... then it will pop out and I can do the selection here").
## [0.4.7] — 2026-10-31

From the tester's confirming run of 0.4.6 (90 tries). No invalid paste saved, and no valid paste or interrupted save
was refused except the rare n5b.
- `close` reads past a Windows line end or a trimmed last line in the answer file (k6b2: such a file is no edit).
- The "answered twice" refusal asks to indent the line if it belongs to a note (n5b).
- SKILL.md names the by-hand way out when questions changed after an interrupted save (put question_collection.md
  back, then `close`; k9). It states the one known limit: a hand forgery of both an answer file's body and its kept
  paste (k6b3). It no longer overclaims that no Run can be left stuck.

## [0.4.6] — 2026-10-31

From the tester's third run (0.4.4; 112 tries, none of its refusals wrote anything). It confirmed all six 0.4.4
fixes and found these, now fixed:
- **k6b**: `close` closed an answer file whose body was edited by hand to contradict its kept paste. `close` now
  requires the file to be exactly what `save` writes from that paste (one function, `answer_file`).
- **k6d, k9, k10**: a rebuild, a question edit or an older save after an interrupted save left the Run stuck,
  refused by both `close` and `save`. `close` no longer re-checks the stamp or the form, which only matter while a
  paste waits, and `build` refuses an answered Run (k6e).
- **b2**: a rebuild that changes nothing kept a new stamp and refused earlier copies. It now keeps the form and its
  stamp.
- **Messages**: a paste whose `form:` names another page is told so first, without "reload" advice. The no-`form:`
  warning says the build stamp matched too.
- **Docs**: SKILL.md says an old form's paste needs the current `built:` line, a missing `form:` line is matched by
  the stamp, what `close` checks and when to look by hand, the two `build` rules, and how notes stay in the note.
  Its version line now matches this changelog (0.4.5 had left it at 0.4.4).
- **Tests**: 15.

## [0.4.5] — 2026-10-31

The compact map beside every section is gone (JL 261031: "who tmd get this??? we don't need this !!!!"), and with
it the map's 🙋. SKILL.md's "Where it shows" now lists the inbox, Work and Studio only. Work shows a record on the
row it holds up, on its own Run row, and, since the coordinator session's fix, as a row of its own on the page that
owns it.

## [0.4.4] — 2026-10-31

From the same tester's re-run of 0.4.3, its own cases plus new probes. It confirmed c1f, c4f2 and c6g are fixed and
found these, now fixed:
- **n1**: the form writes an empty line inside a two-paragraph note, which ended the note. A note now runs to the
  next question line, keeping its empty lines.
- **c4f3**: a rebuild let an old paste save under the new question. The form now carries its build stamp (a time,
  never a hash), the copied text repeats it on a `built:` line, and `save` refuses a paste from another build: reload,
  then copy again.
- **c4f4**: touching an unchanged `question_collection.md` refused a valid paste. Staleness is now checked by
  content: the form must equal what the current Markdown renders.
- **k6**: `close` now runs save's checks on the paste the answer file keeps, so a file that is no saved answer is
  never closed.
- **k2**: `close` reuses a pass the interrupted save already wrote.
- **x2, x4**: a Block folder reached through a link passes when the path leads to this Run's own form.
- **Docs**: SKILL.md says hosts serve a SPACE root, how the Project is found (`Project-*`), the `built:` line, and
  what a reload does to kept picks.
- **Tests**: 14.

## [0.4.3] — 2026-10-31

From an independent fresh agent that tried 50 times to break `save` (two same-named Runs on two pages; it read
SKILL.md, not the code). 46 tries behaved; these 3 are fixed:
- **c1f**: a `form:` path naming no page (`/runs/<run>/<run>.html`) matched both pages. `form:` must now end with
  the Run's own folders from its Project (else its Block) down. That is also the same whichever host or link serves it.
- **c4f2**: a question sentence reworded after the build let the old form's answers save under the new words. A
  form older than `question_collection.md` (file times, no hash) is now refused: rebuild and ask again.
- **c6g**: a note's later line at column 0 was dropped. A note now runs at any indent to the next blank line or
  question.
- **Also**:
  - `collect.py close` finishes a save that stopped halfway;
  - the map's 🙋 leaves a Run whose answer file exists;
  - the form keeps a pick by its option's text, so a rebuild that reorders options never moves it;
  - refusals name the Run the first line names, the folders `form:` must end with, and the unread lines;
  - "card done but no answer file" is reported as itself.
- 13 tests.

## [0.4.2] — 2026-10-31

From the Codex review relayed by physician-space-63; each bug was reproduced and fixed here.
- **Wrong page**: `save` checks the paste's `form:` path against the Run's own page. Two pages can hold Runs with
  the same name, and a paste naming one page's form had closed the other page's Run.
- **Fake options**: every pick must be one of its question's options, with that option's current text. Each QN must
  be one of the Run's questions, given once, under its current title, and the first line's title must match.
  "Z · Nonexistent choice" had been saved as an answer. "(no option picked)" and notes still save.
- **Nothing written on failure**: every check runs before any write, and the answer file is written aside, then moved in.
- **Interrupted saves**: an answer file already on disk closes the Run, even when an interrupted save left the card
  saying waiting.
- **Docs**: SKILL.md no longer claims "Answered, not yet applied" or "(not yet applied)". Saved is all `done`
  says, and whether the answers were applied is the owning Task's record. "Interactions" names only the inbox, while
  the forms and badges say "Questions for you".
- **Tests**: new regressions for the same Run name under two pages, the invalid picks and an interrupted save. No
  hashes: names and places only.

## [0.4.1] — 2026-10-31

From the fresh-agent check of the renamed skill (AGENTS.md: it ran new, check, build and save on a scratch Task):
- `save` refuses a Run already `done`. A second save had rewritten a closed Result.
- A note keeps counting when its indent is lost, and `save` names any line it cannot read.
- The answer file says beside a note that the note wins where it differs from the pick.
- `new` refuses a second waiting collection Run under one page.
- The parser reads `-` or `:` where the form writes `·`.
- SKILL.md now gives the full pasted text, the `for:` address, `--feeds` and the optional flags, and a `Why`
  with the pick's own letter. It also has a line for anyone holding an older note.
- The Interactions view no longer says "not yet applied", which nothing records. It says applying belongs to the
  `feeds:` Runs.

## [0.4.0] — 2026-10-31

Renamed from haipipe-collect (JL 261031, approved in Codex and relayed by physician-space-47). The skill now means:
"Request and record human input needed to continue a page's work". The name covers questions, choices, feedback,
clarification and reviews; the question-and-answer form is its first and only kind so far.
- **Interaction**: it ends when the response is saved. Applying the response belongs to the owning Task, so
  answered is not applied. Reader-facing words stay concrete ("Questions for you").
- **Folder**: the skill is `skills/1_base/workbench/haipipe-interaction/`. `aliases: [haipipe-collect]` keeps the
  old name working, and `~/.claude/skills/haipipe-collect` points to the new folder.
- **Kept**: `scripts/collect.py`, the Run type `collect`, `rNN_collect_<slug>`, `question_collection.md` and
  `answer_collection.md`.
- **Form**: it says "Questions for you" above its title. The copied text starts `haipipe-interaction answers ·`,
  and `save` still takes the old `haipipe-collect feedback ·`. The form keeps answers under
  `haipipe-interaction:<path>` and still reads those kept under `haipipe-collect:<path>`.
- **Display** (approved by JL the same day, relayed by physician-space-09). There is one record per interaction,
  and the workbench shows it in four places:
  - the Interactions rail item: Needs your input (the default), Answered and All, for this Project or Block and
    below;
  - a badge on the Work row the interaction holds up;
  - the map's 🙋;
  - a badge on the Studio card it is about (the coordinator session's part).
  Every entry opens the one form URL, so state is shared. See SKILL.md "Where it shows" and `servers/workbench/focus_page.py`.
- **Rebuilt and swept**: b17's r01 was rebuilt, and its card says `skill: haipipe-interaction`.
  haipipe-run, haipipe-project's ladder audit, `focus_page.py`, the workbench README and the b17 faces name the new
  skill. b35's r01 is the coordinator session's.

## [0.3.0] — 2026-10-31

The questions are Markdown (JL 261031: "you generate a question_collection.md in that run folder, and this could be
rendered into the html and we can make the selection on it"; "we are more like to generate the html based on the
markdown files we have").
- A collection Run holds `question_collection.md`, readable in any viewer. Each card is `## QN · title`, a short
  why, at most one detail (a sketch or a picture), the question in bold, `- [x] A · …` for my pick and `- [ ] B · …`
  for the others, then `Why A:`.
- `collect.py build` renders that Markdown into the form.
- `save` writes `result/answer_collection.md`: the same Markdown with the person's picks ticked, an `Answer:` line,
  their `> note:` lines, and the pasted text word for word at the end.
- `config.yaml` is gone, and `parse` and `markdown` round-trip a file unchanged.
- b17's r01 moved to `question_collection.md` the same day.

## [0.2.0] — 2026-10-31

A form is now a collection Run (JL 261031: "so it will be a run of collection"; "we will not call it a cNN, it will
just be the rNN under that page"): `runs/rNN_collect_<slug>/` under the page whose work the answers change,
`kind: hard`, `type: collect`, the person as `agent:`. `config.yaml` holds the questions, the ticket
`rNN_collect_<slug>.html` is the form, and `result/feedback.md` keeps the answers word for word. The card is written
through haipipe-run's `soft_run.write_card`, so it has the one card shape.
- New commands: `collect.py new <page> <slug>` allocates the next rNN; `save <run>` keeps the pasted answers, adds
  a pass and sets `status: done`. `build` sets `status: waiting`, which the workbench shows as waiting on you.
- Compact cards (JL 261031: "try to make it as compact as possible"): `check` refuses a long card. That means a why
  over 40 words, an ask over 12, an option over 14, a because over 16, more than one detail, a sketch over 6
  lines, or more than four options.
- The page is tighter: one-line notes, and the copied text folded under a summary.
- The cNN forms and their `result/collect/` folder are gone. b17 s04's c01 became
  `j03_work_workbench_pages/t01_block_page/runs/r01_collect_report_and_delivery/`.

## [0.1.1] — 2026-10-31

From the first fresh-agent test (AGENTS.md's skill check: it made a two-card form for s04's Open 3 and Open 6 in a
scratch folder):
- `check` now holds the limits: a form title of two to four words, at most six questions, question titles of one to
  three words, a `why` of at most 120 words, an `ask` ending in `?`, and a `because` with every pick.
- `because:` is new. It shows under the options as "Why A", so the person sees why the pick wins.
- A YAML slip prints one line with its line number, not a traceback.
- SKILL.md:
  - names the interpreter (needs PyYAML) and two YAML habits;
  - lists every mock class;
  - one form open per topic, and read `Decided` before asking;
  - when a doc and the code disagree, the code wins;
  - loop step 3 is "try", so it is not confused with `collect.py check`;
  - reset after a trial, since the page keeps answers in the browser.

## [0.1.0] — 2026-10-31

First version (JL 261031: "we might want to have a thing named /haipipe-collect, to collect the user's feedback").
`scripts/collect.py build <spec.yaml>` writes a self-contained form page from a question spec: one card per question
(why, details as a text sketch, an HTML mock or a picture, the question, its options with the recommendation
picked, a note box) and a Copy feedback button whose text the person pastes back. `collect.py check` lists a spec's
problems. SKILL.md holds the loop, the spec, the pasted-feedback text and where a form and its answers live. First
form: b17 s04 `result/collect/c01-report-and-delivery`.
