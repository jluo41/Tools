---
name: haipipe-interaction
description: >-
  What passes between the work and the person, kept where they read it: what the work needs from them (questions,
  choices, feedback, clarification or a review) and what they should know (a behaviour, a limit, a choice made for
  them; collect.py know). Its question-and-answer form is a hard collection Run under the page whose work the
  answers change (runs/rNN_collect_<slug>/). Its question_collection.md holds compact questions in
  Markdown with my pick ticked; collect.py build renders them into a form where the person selects; the person
  presses Copy feedback and pastes the text back; collect.py save keeps it as result/answer_collection.md and the
  interaction ends. Applying the answers belongs to the owning Task. Trigger: ask me, questions for you, choose a
  version, review this design, collect feedback, collection Run, question_collection.md, things you should know,
  what to know, document it to the Interaction, /haipipe-interaction.
metadata:
  version: "0.10.0"
  last_updated: "2026-11-05"
  aliases: [haipipe-collect]
  # version history: ./CHANGELOG.md
---

# /haipipe-interaction · ask the person, keep what they should know

An interaction requests and records the human input a page's work needs before it can go on (JL 261031, renamed from
haipipe-collect: the name covers questions, choices, feedback, clarification and reviews). It ends when the response
is saved. Applying the response belongs to the owning Task: answered is not applied.

**The form is the conversation** (JL 261031: "I will not read you response here, i will just read this Intereaction
UI"). The person reads the form, not the chat: everything they need to decide is on the form itself (the why, what
each option means, and for a choice between screens, the screens). **Once the form is built, the chat carries no
content** (JL 261031: "after the UI is done, I will no long see any content from your response here"): the reply is
the form's link and nothing else, with no questions, picks, previews, findings or summary, since a word said only in
the chat is never read. This overrides the usual reply format (answer line, sections, summary) for that reply. Whatever the person needs goes on the form, the agent's findings in its intro or in a
question's why. **Show the options, never only name them** ("for the UI, you have differen options, you can also make
the option's preview results, liek the hmtl to be embeded here, and it will be much easeri to understand"): an option
that is a screen carries its live preview, a small HTML page beside the others; a picture when it is a drawing or a
chart; words alone only when nothing can be shown.

**One interaction, one Studio topic** (JL 261031: "the interaction page should be attached to one studio as well").
Every interaction names the sNN whose decisions its answers change, in its `for:` line, and shows on that sNN's card.
Pick the topic that owns the question, which is often not the one the talk started from: a layout question for
every page belongs to the topic about page shape, not to the Studio topic it was first noticed on. The Run sits
under the page that holds that sNN (a Block's sNN: the Block's own `runs/`; a Task's: that Task's). When no topic
fits, start one first (haipipe-studio), then ask. `new` and `check` refuse a `for:` that names no sNN.

JL 261031: "so it will be a run of collection"; "it will just be the rNN under that page"; "in that run, you generate
a question_collection.md in that run folder, and this could be rendered into the html and we can make the selection
on it"; "we are more like to generate the html based on the markdown files we have"; "for each question you asked,
try to make it as compact as possible".

```text
kind                      status       Run                     reader sees
questions and choices     built        rNN_collect_<slug>/     "Questions for you"
what you should know      built        rNN_collect_<slug>/     "📌 What you should know", state "to know"
review, clarification     not yet      (a later kind)          "Review this design", "Choose a version"
```

Reader-facing words stay concrete: the form's head says "Questions for you". On a workbench page a row that holds
interactions carries one button, "Interaction", with no count and no "Questions for you" or "Answered" tag (JL 261031,
b16 t01 r04 Q3: "we will not have the answered & questions for you"); when a question on it waits for the person it
is flagged, "🙋 Interaction" with an orange edge (JL 261031: "if there are some questions i need to answer, cuold you
flag them as well"), and plain once nothing waits. "Interactions" is the name
of the workbench's inbox on the right rail (JL 261031), never a label on a form.
`/haipipe-collect`, the old name, still opens this skill (`aliases:`).

```text
collect.py new   <page> <slug> --title T --for F [--person P] [--feeds a,b]
                                                        runs/rNN_collect_<slug>/: run.yaml, question_collection.md
collect.py check <run>                                  the questions' problems; nothing written
collect.py build <run>                                  the Markdown rendered into the form; the card says waiting
collect.py save  <run> [file]                           the pasted picks into result/answer_collection.md; done
collect.py close <run>                                  finish a save that stopped halfway; the answers stay as they are
collect.py applied <run> Q1 [Q2…] --by "…" [--state "in progress"]
                                                        record what applied each answer: its flag on the form
collect.py record <page> <slug> --title T --for F --decision "title :: what was decided :: their words" [...]
          [--applied-by "…"]                            a decision made in the chat, kept as a done interaction
collect.py know <page> <slug> --title T --for F --note "title :: what to know :: where to read it" [...]
                                                        what the person should know, kept and shown; waits on nothing
collect.py bundle <page>                                one page answering every waiting form at or below the page:
                                                        <page>/runs/answer_all.html (GENERATED; rerun it)
collect.py save-all [file] [--root SPACE]               the combined page's one paste, each form saved to its Run
collect.py audit <top> [--fix]                          every set at or below a folder: one theme, one set
```

**One theme, one set** (JL 261031: "why each question set just a few questions? we can have longer question list";
"each question set should have a things like theme ... we don't want to have some many short questions list"): a set's
theme is its Studio topic. Ask a topic's open choices together, up to 20 questions in one set, never a new short set
per turn; a topic's chat decisions all go into its one record (`record` appends to it, its lines the decisions
themselves). `collect.py audit <top> [--fix]` checks every set at or below a folder: a topic's records split over
several Runs (--fix merges them into one, `rNN_collect_<theme>_decisions`, and updates links to the old names), more
than one waiting set for a topic, an old record whose lines read "What was decided?" (--fix rewrites it), a set with
no topic, and three or more short waiting sets under one Job (answer them on one page with bundle).

**Combine, actively** (JL 261031: "should actively think about combine the different interactions in to one page"):
when more than one form waits for the person on a page or below it, the link they get is the combined page, never a
list of separate forms. `bundle` writes it: every waiting form in place, one under the other, each form's own Copy
hidden, and one "Copy all answers" that joins every form's text; the person pastes once and `save-all` splits the
paste at each form's first line and saves each to the Run its `form:` path names (a block that fails is named, the
others still save). Rebuild the bundle whenever a form is added, rebuilt or answered.

Run it with the SPACE's `.venv/bin/python` (PyYAML). `<page>` is the Block, Job or Task folder whose work the
answers change; `<run>` is the Run folder. `--feeds` lists, as SPACE-relative paths, the Runs that will apply the
answers; `--person` is who answers; `--for` is its Studio topic's address (below). `--title` and `--for` are required.

Older notes may name this skill's first forms: `config.yaml`, `result/feedback.md`, cNN forms in `result/collect/`,
a `because:` field. Those changed the same day (CHANGELOG.md); the Run kind kept the word `collect` (`collect.py`,
`type: collect`, `rNN_collect_`, `question_collection.md`), since its first kind is a collection of answers.

## 🔁 The loop

```text
1 new     the agent allocates the Run under the page whose work the answers change
2 write   the agent writes question_collection.md: compact cards, my pick ticked
3 build   check, then build: the form is rendered from the Markdown (GENERATED; never edited by hand)
4 try     open it on the SPACE's host: a change marks its card, Copy fills the text; then Back to my picks
5 link    the reply is the workbench link, nothing else: the Block's Interactions section
          (/_board/workbench?path=<Block>&layout=focus&section=interactions), or the sNN's Studio row; never the
          bare form file (JL 261031: "应该直接给我 block 链接或者 studio 链接对吧？"). Every word is on the form
6 answer  the person keeps or changes each pick, adds notes, presses Copy feedback, pastes it into the chat
7 save    collect.py save: result/answer_collection.md, the same Markdown with their picks; status done
          ── the interaction ends here ──
8 apply   the owning Task's Runs (the card's feeds:) apply the answers and record each decision where its
          owner keeps decisions; that is their work, not this skill's
9 flag    whoever applied an answer runs collect.py applied <run> QN --by "<what changed, real names>": the form
          shows "✅ applied <date>" on that question, and the workbench's list shows it too (JL 261031: "if we
          already fix them, then give them the flags"). Handed to another owner: --state "in progress" --by "<who
          does what>"; that owner reruns applied QN when done, which replaces the line. Both records are required:
          the decision where its owner keeps decisions (step 8), and the flag here
```

## 📌 What the person should know (JL 261105)

JL 261105: "could you document it to the Interaction, about things you should know?"; "it should include both ask
question and keep what you should know". A thing said only in the chat is lost; keep it where they read.

```text
keep it     a behaviour they could trip on ("Banana 2" reads the 2 as part of the name), a limit of a result, a
            choice made for them, a state that is not what it looks like, a mistake they should see
not here    a question (a form), a decision they made (record), a finding that answers a Question (its report)
```

1. **One theme, one set**: `collect.py know` appends to the topic's one notes Run, in order; `for:` names its sNN as a form's does.
2. **One note, one thing**: a short title, what to know in plain words with its real names and measured numbers, where to read more.
3. **Waits on nothing**: state "to know"; it never flags the section or the button. A question goes on a form.
4. **Settled**: when it stops being true, `collect.py applied <run> QN --by "<what changed>"` flags it; its words stay.
5. **The chat still answers**: a note is an ordinary reply naming the Run; the form's link-only rule is for a form.

## 🗣 A big decision made in the chat is recorded too (JL 261031)

JL 261031: "the big decisions like this should also be recorded ... to be consistent in the future". A decision the
person makes in the chat, not on a form, gets the same record a form answer gets, so every decision is found in one
place (the topic's Interactions, the inbox) and reads the same way. Big means it changes what a page is or does (its
views, its sections, what shows where, a rule every page follows), not a wording fix or a bug.

```text
1 record   collect.py record <page> <slug> --title T --for <its sNN> --decision "title :: what :: their words"
           a done collection Run: each question answered "my own decision", their words kept word for word,
           source: chat on the card; it never waits and is never blocked by a waiting form
2 status   --applied-by "<what changed, real names>" when the change is already made (applied), or later
           collect.py applied <run> QN --by "…" [--state "in progress"], the same flags a form answer gets
3 decided  the agent also writes the decision where its owner keeps decisions (the sNN's Decided line, by hand;
           record does not), as for a form
```

`--title` names the whole record (the chat turn: "Board Report decisions"); each `--decision` title names one question
in it ("Venue with related"). The reply to the person after a record is an ordinary reply: what was decided, and the
record's Run named in its file list; there is no form to link to.

One record per chat turn that decides, its questions one per decision; the person's own words, never a summary of
them; the page and `for:` of the topic that owns the decision (the same rule as a form's). An agent relaying the
person's words from another session records them with the relay named in the words ("relayed by …").

0. **Extend before new** (JL 261031: "I don't think you need to open a new run, you can extend the current run"). A new question goes into the waiting Run the person is already reading (add its `## Q`, its previews, rebuild). Allocate a new Run only for a good reason: none waits (the last is answered: a closed Result is never reopened), or the questions change a different sNN under another page.
1. **One question, one decision.** First read the topic's `Decided` (when a topic owns the choice) and every collection Run under the page, waiting or answered: never ask twice. `new` refuses a second waiting Run for the same sNN (its `for:` address) under one page.
2. **Compact.** One short why, at most one small detail, a short question, two to four short options.
2b. **Shown.** A choice between screens gives each option its preview, indented under it: `[preview](option-a.html)`
   (a live page, drawn in the workbench's own look with placeholder text) or `![A](option-a.png)`; the form shows them
   side by side at half size, a click picks the option, Open shows it full size.
   **The previews differ where the options differ** (JL 261031: "I cannot see the differences among the three
   options"): show the part that changes, large (options that differ in views show each view as its own small
   panel); never the same screen with only a button label changed.
   **The difference sits in the frame**: the form shows a preview in a frame 600 page pixels tall (300 on screen), so
   leave out what no option changes and keep rows compact (JL 261031 on b17 r01: "show that what is the expected UI /
   html looks like"; its first previews kept B's Delivery screen below the frame, so A and B looked the same).
   **One column per option**: when an option moves something between two places, stack them, one under the other,
   never side by side (JL 261031 on b17's theme-alignment form: "why we have two columns? I think we should just
   have one columns for each of them"; two screens at half size were unreadable). A script writes the previews.
   The form draws an orange box around what differs (JL 261031: "highlight the part that are different by using the
   box"): it compares a question's previews block by block and boxes, in every option, the smallest block one has
   and another has not (changed, added or moved), then scrolls each preview to its first box. When the compare
   picks the wrong block (a swap of two blocks boxes the smaller), mark the right one `class="diff"` in each preview.
3. **My pick, and why.** Tick my pick (`- [x]`); a `Why` line with its letter (`Why B:` when B is the pick) says why it wins.
4. **Real names.** Real files, fields, sections. When a doc and the code disagree, the code wins.
5. **A note wins.** Whoever applies the answers reads each note first: a note that differs from its pick is the answer (the answer file says so beside it). A question that needs asking back is a new Run.

Ask only what is the person's to decide: a design choice, a pick between drafts, a scope cut. Decide the rest
yourself: never a topic number, a folder name, a renumbering or a rename, which are bookkeeping (JL 261031
on b17's theme-alignment form, three such questions: "I don't understand"). Ask in the words of what the person sees. A page has one collection Run waiting per sNN its `for:` names, so each Studio row
can carry its own form; the next is allocated when it comes back, so answers
never cross. A changed mind after `done` is a new Run, never a rewrite of a closed Result.

## 📝 question_collection.md

````markdown
# Report and Delivery

for: b17-s04:theme_work @ workbench_page_structure

One line of intro (optional).

## Q1 · Report or Delivery

What the paper looks like is the delivery. On b17 today, a delivery opens only from a Studio row.

```text
an optional sketch, at most six lines (or one picture: ![caption](file.png) in the Run folder)
```

**Where does a delivery show?**

- [x] A · In the Report; Delivery leaves the right rail.
- [ ] B · In both: Report previews, Delivery keeps files and sent marks.

Why A: One thing in one place.
````

An option's preview is the indented line under it, `  [preview](option-a.html)` or `  ![A](option-a.png)`, a file in
the Run folder; the answer file keeps it. `·` (a middle dot) separates `QN` from its title and an option's key from its text; `-` or `:` is read too.
`for:` names what the answers change, as the Studio writes a topic's address: `<bNN>[.jNN[.tNN]]-<sNN>:<block slug>
@ <topic slug>` (b17-s04:theme_work @ workbench_page_structure), so the workbench shows the Run on that sNN's card.
It is required: an address with no sNN (b01.j01.t01 · t01_layout) is refused.

It reads as plain Markdown in any viewer, the workbench's reader too, with my pick ticked. `<!-- … -->` lines are
notes to the writer and never reach the form. The answers come back in the same shape, so the two files read side
by side: `result/answer_collection.md` ticks the person's pick, adds `Answer: B, changed from my pick A.` and their
`> note:` lines, and keeps the pasted text word for word at the end.

Every question also ends with one standard choice the Markdown never lists: **✍ My own decision** (JL 261031: "like
I will add my decisions"). Picking it turns the note box into "Your decision (required)"; the copied line reads
`QN · <title>: my own decision` with the note under it; `save` refuses it without words and writes `Answer: my own
decision.` and `> decision: <the words>`.

## ✂️ Compact: what `check` refuses

```text
the Run      named rNN_collect_<slug>; a # title of 2 to 4 words; an intro of at most 30 words; 1 to 20 questions
its topic    a for: line naming one sNN (b17-s04:theme_work @ workbench_page_structure)
a question   ## QN · title of 1 to 3 words; a why of at most 40 words; a **question?** of at most 12 words
its options  2 to 4 "- [ ] A · text", at most 14 words each; at most one ticked, with Why A: of at most 16 words
its detail   at most one: a ```text sketch``` of at most 6 lines, or one picture in the Run folder
a preview    an option's own, indented under it: [preview](x.html) or ![K](x.png); its file in the Run folder
anything else inside a card, or a ``` block never closed, is named with its line
```

## 📁 The Run

```text
<page>/runs/r01_collect_<slug>/
├── run.yaml                        kind: hard · type: collect · skill: haipipe-interaction · agent: <person>
├── question_collection.md          the questions (written by the agent)
├── r01_collect_<slug>.html         the ticket: the form, rendered from the Markdown (collect.py build)
├── result/answer_collection.md     the answers: the same Markdown, the person's picks ticked
├── applied.md                      what applied each answer, one line per question (collect.py applied); beside
│                                   run.yaml, never in result/, so the Result stays closed
└── passes/p01-<MMDD>/pass.md       the round
```

It is hard by haipipe-run's own test: its output lands only in its own `result/`, and that Result is a judgment. Its
`status:` walks planned (allocated), waiting (the form is built), then done (the answers are saved). Saved is all
`done` says. What applied each answer is the flag in this Run's `applied.md`, beside run.yaml and outside the
closed Result; the decision itself lives where its owner keeps decisions (an sNN's Decided list); the `feeds:` Runs'
passes, when there are such Runs, hold the work. Number it with the page's other hard Runs.

**See answers opens a page, never raw Markdown** (JL 261031: "the UI here doesn't good"): an answered set's button opens its form, which shows the picks read only; a chat record gets its own read-only page, `<run>.html` (`record` writes it: each decision as a card, the person's words under it, its flag). An answered form shows the person's own picks and notes, read only, from the paste its answer file keeps; Copy
feedback is hidden. It reads `applied.md` each time it opens, so a new flag needs no rebuild; only a form built
before 0.6.6 needs one `build` to get the flag code (its questions and stamp stay). Opened as a file, a browser may
refuse to read `applied.md`: the flags then do not show, and nothing else breaks.

## 🖥 Where it shows: one record, every entry (JL 261031)

```text
Interactions (right rail)   Needs your input · Answered · All, for this Project or Block and below
Work                        the Interaction button on the Job or Task row it holds up, on its own Run row, and
                            on a row of its own at the top of Work on the Block or Job page that owns it
Studio                      the Interaction button on the sNN card its for: address names
Each view                   the last section of every Report and Work view of a Block, Job or Task, 🙋 Interaction:
                            the Runs at the page or below, a folding group each, a left tab per question, the same
                            form on the right, Back and Next (JL 261104; servers/workbench/interaction_section.py)
The one look                the Interactions rail and the Interaction button's pop-out draw this same section
                            (JL 261104: "make this to be the standard items for any of them")
```

The button pops out a list of that row's items, the waiting one first (b16 t01 r04 Q4, Q6). Each item shows its
title, its state and date, its questions, and one button: Answer (the form) or See answers (`answer_collection.md`),
opening in the same pop-out (Q5). The Interactions view draws the same items. Every entry opens the same form URL, so
a half-filled form is the same wherever it is opened, and `save` writes the one Result. The workbench reads it all
from disk: `focus_page.interactions(folder, root)` (one row per collection Run, its state from the card: waiting,
answered, planned), `interaction_button` (the one button), `interaction_items` (a row's items: about an sNN, held by
one Run, or at a page or below), `interaction_item` (one item), `interactions_html` (the view), `interaction_topic`
(the sNN its `for:` address names); the pop-out is `view=focus-part&part=interactions&path=<the row's folder>`. An
answered item shows each question's flag from `applied.md` ("✅ applied <date>", "⏳ in progress <date>") and,
when the card has `feeds:`, "Applying it belongs to …"; a question with no flag has not been applied yet.

The copied text, which `save` reads from a file anywhere or from stdin:

```text
haipipe-interaction answers · <run> · <title> · <yyyy-mm-dd hh:mm>
form: <the form's path on the host>
built: <the form's build stamp>
Q1 · <title>: <key> · <option text>[ (changed from <my pick>)]
   note: <the person's note>
         <more lines of it, indented>
Q2 · <title>: (no option picked)
```

Its first line names the Run, so `save` refuses another Run's paste; it also takes the old form's first line,
`haipipe-collect feedback · <run> · …`, as long as the paste carries this form's `built:` line: a tab left open on
an older form, or one with no stamp, is reloaded and copied again (its kept picks come back). `form:` is the form's path as the browser shows it: on a host, the path from
the SPACE root (`/blueprints/Project-Ladder/work/b17_theme_work/j03_…/t01_block_page/runs/<run>/<run>.html`);
opened as a file, its disk path. Either way it ends with the Run's own folders from its Project (a `Project-*` folder; else its
Block) down, which is how `save` tells two same-named Runs on different pages apart; hosts serve a SPACE root, never
a Project or a Block. A folder in that chain reached through a link still passes when the path leads to this Run's
own form. `built:` is the build stamp the form carries (a time, never a hash). A note runs from its `note:` line to
the next question line, at any indent and with its empty lines, since a chat may strip the spaces. The form indents a
note's later lines, so they never read as a question line. Only a note line at column 0 that starts `QN · ` reads as
one, and `save` then refuses with "answered twice" and asks to indent it. A line `save` cannot read is named
on screen; the whole paste is kept word for word either way.

`save` checks everything before it writes anything, and a failed check saves nothing:

```text
the Run       the first line names this Run and its current title
the form      it exists and was built from the current question_collection.md (a new template alone never counts)
the build     built: is the stamp of the form on disk: a tab left open on an older build is reloaded, then copied
the page      form:, when present, ends with this Run's folders from its Project down; else refused
the questions every QN is one of this Run's questions, given once, under its current title; none is left out
the picks     every pick is one of that question's options, with its current text; "(no option picked)" is fine
closed        an answer file already there closes the Run, even when an interrupted save left the card waiting
```

A save that stopped halfway, its answer file written but its card still waiting, is finished by `collect.py close`:
it first checks that the answer file is exactly what `save` writes from the paste it keeps, with the current
questions, so a file edited by hand, or one whose questions changed since, is never closed: look at that Run by
hand. Then it sets `done` and lists the round's pass, reusing one the save already wrote; it never touches the
answers.

`build` refuses an answered Run, one whose answer file exists, so a closed Result's form never changes and a rebuild
never leaves a Run stuck. If question_collection.md was edited after a save that stopped halfway, `close` refuses:
put question_collection.md back as it was at the save (git has it), then run `close`. `close` checks only that the
file agrees with itself, so an answer file forged by hand in both its body and its kept paste cannot be told from a
real save; a complete `save` never leaves that gap. A build that changes nothing keeps the form and its stamp, so a copy made before it still saves; a build
that changes the form gives it a new stamp, and earlier copies are refused. After
a rebuild, the person reloads the form: their kept picks come back by their option's text, and a pick whose option
text changed comes back as my pick. The workbench already counts the Run as
answered from its answer file. A paste with no `form:` line is matched by its first line and its build stamp, and `save` says so; only a Run
copied without edits shares a stamp, so keep the line.

A failed title or option check usually means the form was built from older questions: rebuild it and ask again. The
answer file is written whole or not at all (written aside, then moved in).
The form keeps answers in the browser that opened it, per path, and still reads answers its older build kept.
After a trial press Back to my picks: the agent's browser is often the person's own.

## ✅ Before sending the link

1. `check` prints `ok`; `build` writes the form; the card says `waiting`.
2. The form opens on the SPACE's host (the Tailscale origin, never localhost), every card and detail drawn.
3. A changed option marks its card `changed`; Copy feedback fills the text; Back to my picks clears the trial.
4. The reply holds only the link: nothing in it that the form does not already say.

Related: haipipe-run (the Run contract), haipipe-ui (how a page reads), haipipe-studio (the topic that owns the
decisions), haipipe-report (a Block's Questions: an interaction collects a person's choices, a report answers a
Question).
