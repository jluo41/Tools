# Short title (a phrase, not a sentence)
state: 🔴 OPEN
owner: CC
method: one line on how you plan to solve it (optional; delete the line if unused)

<!-- How to use: copy this file, rename to Q<group letter><number>-<slug>.md for a ruling
     or S<stage order>-<slug>.md for a lifecycle stage, replace each
     guide sentence with real content. "required / optional" at the start of each section is
     for you:
       required = leaving it out makes the question incomplete (build.py does not error, but
                  a block is missing on the page).
       optional = delete the whole section, heading included, if unused.
     The top four lines follow the same rule: # title, state, owner are required; method is
     optional (delete the whole line).
       - state takes exactly one: 🔴 OPEN (not started) · 🟡 PARTIAL (in progress) ·
         ✅ SETTLED (done) · ⏸️ ON HOLD (parked).
       - owner is who is responsible; JL shows 🧠 (decides) on the page, others show 🔧.
     Section names (Question / Boundary / Items to Finish, etc.) must be kept verbatim.
     `## Opening` is accepted as an alias for `## Question`, but the template keeps Question
     because the lead sentence must still be an actual question.
     build.py fetches content by these exact names, so any mark goes in the body, never in the
     heading line, and state: takes one status only.
     The visible on-stage hierarchy is fixed:
       Opening -> Diagram -> Content -> Items to Finish -> Where we are -> Files.
     Opening groups the Question lead + optional Boundary. Optional Diagram is its own collapsed
     section and opens only when its heading is clicked. On Q faces, the remaining Question
     paragraph becomes Content's first "Why this matters" subsection. On S faces, "Why this
     matters" moves into Opening; an optional exact direct `### Stage Record` under Content moves
     there too and starts collapsed when supplied. Explicit Content is optional for Q and required
     for S.
     Delete this comment when done (it is dropped at generation either way).
     Full writing standard: ref/writing-rules.md. English only. No em-dashes. -->

## Question
required · One lead sentence, then one plain paragraph. **Reading this section alone, a
zero-background person should understand what the question is.**

The lead renders in `🧭 Opening` with Boundary. On Q faces, the paragraph below it renders as
Content's first `Why this matters` subsection. On S faces, that paragraph renders inside Opening.

The lead sentence is the actual question, written as a question, in plain words. It stays in
Opening and is clickable.

Then one flowing paragraph: why the question is hard, what breaks while it stays open, and what
it affects downstream. build.py labels it "Why this matters": under Content for Q, inside Opening
for S. Write it as prose, not as `- Why it is hard / - What breaks` bullets.

## Boundary
optional (strongly recommended) · What this question covers and, more importantly, what it does
not. Folds into the same block as the Question, so keep each line short.

- ✅ Covered here
  One or two lines drawing the scope.
- ↪ Covered elsewhere
  One or two lines, and **name the question that does cover it** (for example "projection is
  QA3"). A bare exclusion reads as a refusal; this line's job is to redirect the reader. Use
  `↪`, not `❌` (JL 260724).

## Diagram
optional · One ascii figure showing the shape or flow of the question, right below Boundary.
If you cannot draw it, delete the whole section: empty beats wrong.

It renders as its own `🖼 Diagram` section, collapsed by default. The heading remains visible;
the figure appears only after the reader clicks it.

For a richer figure, put an excalidraw share link on **its own line** below the ascii; it embeds
as an interactive canvas (`https://app.excalidraw.com/s/...`), with a fallback link underneath.
**Keep the ascii figure:** it has zero dependencies and stays when the canvas fails to load.

## Content
S required · Q optional. The face's substantive material after orientation. Delete this explicit
section in a Q that needs no additional material.

S-only, optional: an exact direct `### Stage Record` is orientation metadata, so build.py lifts
it into Opening and keeps it collapsed when supplied. All other direct `###` sections remain
under Content.

Each direct `###` heading becomes one individually collapsible content subsection. Keep the old
stage prose under these headings rather than copying it into a second backing document.

### First content subsection
The actual content goes here.

### Second content subsection
Continue with the next coherent part of the stage.

## Items to Finish
required · A checklist, one line each, of what counts as done. Tick `- [x]` when met; the
heading auto-counts `1/2`. **Do not tick what has not been verified.**

Every item is `- ICON heading` with a folded explanation. Start the heading with an author-chosen
emoji icon (build.py never guesses one). The first indented line is a one-sentence summary; the
lines after it are the long explanation, written as a real paragraph (what it means, what
happened, why). Only the heading shows on stage; length is free in the fold.

- [ ] 🎯 First finish line
      One sentence saying exactly what this means and how it is judged met.
      The long explanation: the reasoning and history behind this line, as a paragraph.
- [ ] 🧪 Second finish line
      Written so it can be checked, not "basically there".
      The paragraph continues here.

For an S face, former Q-consumer records live here as recognizable checklist items. Keep the id,
stake, route, and answer together:

- [ ] 🔎 Q-Stage-1 · Concrete consumer question
      **Description:** What must be learned?
      **Reason:** Which content or claim depends on it, and what breaks if it fails?
      **Probe:** -> `1-probes/PPNN_topic/QX1.md`
      **Answer:** Empty until the answer lands.

Tick a consumer only after its answer landed, was interpreted, and was woven into `## Content`.
A deferred consumer closes only after a forward pointer is recorded.

## Where we are
required · The actual present state, with numbers where numbers exist (not "basically done").

Open with one concise paragraph: what has been achieved, and what is still unproven. Then dated
items, each prefixed `YYMMDD WHO ·`; build.py strips that into a muted right-aligned stamp, so the
date and person never sit in the title text. Order by date. On S faces, summarize the stage; do
not repeat every consumer answer from Items to Finish.

- 260723 CC · 🔀 What changed on this date
      One sentence naming the change.
      The paragraph: what it was before, why it changed, what it cost.

## Files
optional (strongly recommended) · Which files this question moves or depends on. Paths in
backticks; those declared in `board.md`'s `## Links` become clickable.

- `path/to/thing.py`
  Its role in this question, and where you start when this question changes.
- `path/to/generated-thing`
  If it is generated, say "do not hand-edit".

## Law
optional · folded · Rules this question has settled and will follow from now on, one per line.
Do not write intentions here as if settled. Delete the section if unused.

## Lesson
optional · folded · Traps hit and lessons learned on this question, one per line. Keep them
specific (a concrete failure attached). Delete the section if unused.

## Glossary
optional · folded · Words on this page an outsider would stumble on, one per line: `term:
explanation`. Any coined phrase must be defined here or not used. Delete the section if unused.

## Discussion
optional · folded · Loose discussion, one line each. The "➕ Add to discussion" box on the page
writes here.
> JL: discussion goes here.
>> CC0724: reply with two angle brackets and a date.

## Comments
optional · folded · Comments pinned to a sentence in the body; that sentence is highlighted on
the page. Usually written by the page's "💬 Comment" button, not by hand. Delete if unused.
- [ ] JL 「an exact sentence from the body」 · 260724 1100
      The comment, indented two spaces. Tick `[x]` when resolved; the page strikes it through.

## Log
optional (most questions have one) · folded · What changed on this question, one line each,
newest on top:
260724 1030 · what changed (`YYMMDD HHMM · ...`, time optional)
