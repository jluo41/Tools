# The sentence: one source line, and everything that attaches to it
state: ✅ SETTLED · all 16 Aims closed and JL moved the line, 260802
owner: JL
method: one sentence per source line; everything that attaches to a sentence gets its own face
session: 958e95d5-b099-4cde-b3fd-9b4b2b7ba8b5
## Opening
What is the smallest unit a board can address, and what attaches to it?
A board writes one sentence per source line, and that line is what a reader clicks.
Two things hang off it: a card on a few marked words, and `>` lines under the whole line, which take a citation, a remark, or an edit.
Nothing is stored to link either one, so position alone decides what belongs to what.
This page settles the sentence as that unit and rules everything written onto it.

**Where this page sits**: `QB4` takes the whole page and the order its sections keep, and it stops there.
This page is the next rung down the same ladder: Board, Group, Page, Section, Sentence.
The sentence is where a reader's finger actually lands, so it is the last rung and nothing sits below it.

**What "attaches" means here**: two things, and they do not attach the same way.
A lane is a record on its own line, starting with `>`, written straight beneath the sentence: `> Citation: Smith 2019`, or `> Comment JL this number moved · 260802 0110`.
A card is attached to a few words INSIDE the sentence, such as the `\citep{smith2019}` sitting in it, and clicking those words shows the reference over the line.
The sentence keeps its own words on stage; the card and the lanes both stay shut until someone clicks.

**Covered elsewhere**: `QD8` owns the generated `C/H/P/S` address and what an agent acting on one is handed, which is not an attachment: nothing is written under the sentence and nothing enters the file.
`QB5e` owns what happens once the records pile up, and `QE4` owns locks and two people writing at once.

**Why it matters**: a claim and its evidence are read together or they are not read at all.
Push the evidence to the bottom of the page and the reader has to work out which sentence it came from.
Give the sentence an id and keep the link somewhere else, and the link rots the first time the prose is rewritten.
Adjacency costs nothing to write and nothing to maintain, which is why the whole family rests on it.

## Writing Style
How this page must be written. Read it before editing, and edit to it.

**Demonstrate before explaining**: `### 1` is written in the grammar it documents, so a reader meets the sentence by using one.
A rule added to this page has to survive being shown on a live row there, not only described in prose.

**Name the parts, not the retired faces**: the card, the lanes, the remark and the edit are this page's `### 3` to `### 6`.
`QB5a` to `QB5d` and the older `QAb0` to `QAb4` still resolve through `board.md`'s alias map, so old lines keep working; nothing new is written with them.

**Name lanes and badges the way `src/body.py` renders them**: a typed lane is `> Citation:`, a person's remark is `> Comment WHO …`, an edit is `> ✎ …`.
The badge is `💬`, `✎`, or `⚑`, and a wrong glyph here teaches a reader to expect the wrong thing on every other page.

## Diagram

**The sentence and its two surfaces**: where a reader clicks, what opens there, and which face rules it.

```
✏️ ONE SOURCE LINE · TWO PLACES A READER CAN CLICK

   "The coefficient is 0.42 in the pooled model \citep{smith2019}."  ⚑ 3
    └─────────────── ② the whole line ───────────┘ └─ ① the words ─┘
                    │                                      │
                    ▼                                      ▼
   📎 the lanes · a drawer under the line     🪪 the card · opens over the line
      ⚑ > Citation: · > Value: …    §4          the reference as printed
      💬 > Comment JL …             §5          the rows of a table
      ✎ > ✎ ~old~ *new*            §6          both pictures of a figure
      🤖 the packet an agent gets   QD8
      🧹 filter · resolve · archive QB5e

   🏷 anchor    ① the marked words          ② the whole sentence
   🔢 how many  ① one thing                 ② any number, any kind
   🚦 built     ① yes · 260802             ② yes
   🔒 default   both SHUT · one click opens
   🎖 badge     💬 person waiting ▸ ✎ change ▸ ⚑ lane
```

/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/board.excalidraw&frame=QB5

## Content
### 1 · Try it yourself: every feature, live on this page
**The test sheet**: one row per feature, what you do, and what should happen if it works.

```
🖱 CLICK THESE · they are already here, in 1.1
   the underlined words in a sentence   a panel opens OVER the prose
   a sentence carrying a badge          a drawer opens UNDER the line
   a badge that reads ⚠️                 a loud row saying what is broken

✍️ DO THESE YOURSELF · on the practice line in 1.2
   select words  ▸ 💬 Comment    a > Comment row appears under the line
   select words  ▸ 🪪 Card       those words become underlined and clickable
   hover ▸ ＋     ▸ pick a kind   a typed lane appears in the drawer
   double-click  ▸ change ▸ Save  the line changes, a ✎ record appears

🎯 HOVER FOR THESE · 1.3
   a sentence   C1.P1.S1 · ＋ · 💬      its address, comment, chat
   a heading    breadcrumb · ⧉ · 🤖     its path, copy, chat
   on a phone   one ⋯ holds all of it

🚫 THESE MUST REFUSE YOU · 1.4
   a sentence written twice on one page · words that are not in the line
   the same card twice · and the composer keeps what you typed

👀 WATCH WHILE IT SAVES · 1.4
   the page must NOT jump · sections must stay open · about 0.4s
```
📌 Establishes every gesture the page rules, as something to click rather than read. Everything below is live: the rows in 1.1 already carry records, and 1.2 is yours to write on.

**1.1 · 🖱 Click these, they are already here**

#### 1.1.1 · 🪪 A card on three of its words
(click the underlined words; the panel opens over the prose and clicking away shuts it)
A card belongs to a SPAN of words inside the sentence, not to the line as a whole.
> Card SPAN of words: You clicked the words and this opened over the prose, which is the whole of what a card does. The words kept the paragraph's own font, colour and weight and took one dotted underline: no box, because a box would turn a paragraph into a row of buttons.
The record that made those words clickable is `> Card SPAN of words: …`, written under this sentence like every other lane.

#### 1.1.2 · ⚑ A sentence carrying three typed lanes
(click anywhere on the sentence; the drawer opens under it and the badge said how many were there)
This sentence carries three typed lanes, and none of them is stored anywhere but on the lines below it.
> Citation: `### 4` rules what may attach to a sentence and how the drawer renders it.
> Value: 3 lanes are attached here, which is the number the badge counts.
> Display: the figure in `## Diagram` draws these lanes as the second of the sentence's two surfaces.

#### 1.1.3 · 💬 A sentence someone is waiting on
(the badge reads 💬 rather than ⚑, because a person waiting outranks a filed record)
A person's remark is written `> Comment WHO …`, and the badge turns 💬 because someone is owed an answer.
> Comment CC this row exists so the 💬 badge has something real to count · 260802 1400

#### 1.1.4 · ✎ A sentence that was changed
(one line replaced, one record of what moved, and the old wording stored nowhere)
An edit replaces the source line and leaves one record of what moved, which is why the old wording is never stored a second time.
> ✎ An edit replaces the source line and leaves one record of ~the change~ *what moved*, which is why the old wording is never stored a second time. · CC · 260802 1400

#### 1.1.5 · ⚠️ A card whose words are not in its sentence
(deliberately broken, because a miss the reader cannot see is the one failure this grammar may not have)
Nothing in this line matches what the record below claims to point at, so open the drawer and it says so.
> Card a phrase that is not here: This card names words the sentence above does not contain. Instead of disappearing, it renders as this row and turns that sentence's badge into ⚠️.

**1.2 · ✍️ Do these yourself, on the practice line**

#### 1.2.1 · 💬 Write a comment
(select any words inside a sentence, then use the floating button that appears)
Select a few words with the mouse and a 💬 Comment button appears just below them.
Click it, pick or type your initials, write the comment, and press Save.
A `> Comment WHO 「the words you selected」: …` row lands directly under that sentence, and the page repaints in about 0.4 seconds without you touching reload.
The words you picked are kept in the record, so a remark about three words in a long line says which three; select nothing in particular and the row is written without the quote.

#### 1.2.2 · 🪪 Put a card on a few words
(the same selection, the other button; it is offered only when the words are really in the sentence)
With words selected, click 🪪 Card instead, type what should open, and press Save.
Those exact words become underlined on the page and clicking them opens your panel.
If 🪪 Card does not appear, the selection crosses two sentences or sits inside a figure, and a card there could only ever fail.

#### 1.2.3 · ⚑ Add a typed lane
(hover the sentence, click the ＋ in the rail on its right, and choose the kind)
Hovering a sentence reveals `C1.P1.S1 ＋ 💬` on the right; the `＋` opens a small form.
Pick a kind from the dropdown, which starts on `JL` and must be changed to `Citation`, `Value`, `Note` or another kind if you want a typed lane rather than a remark.
Type the text and Save, and the row appears in that sentence's drawer.

#### 1.2.4 · ✎ Edit the sentence
(double-click it, change the words, Save; a single click stays free for selecting and copying)
Double-click any sentence and an editor opens with the current wording already in it.
Change what you like, put your initials in the small box, and Save.
The source line is replaced and one `> ✎` record appears beside it showing only the words that moved.

#### 1.2.5 · 🧪 The practice line, which is here to be written on
(nothing on this line matters, so comment on it, card it, lane it, and edit it freely)
The pooled estimate settled near the middle of the range during the second half of the study period.
> Comment JL 「settled near the middle」: This remark was written by selecting only these four words, and the record kept them, so a reader knows which part of the line is being questioned · 260802 1738

**1.3 · 🎯 Hover for these**

#### 1.3.1 · The sentence rail and the heading rail
(both stay invisible until the pointer is on them, so they never sit on the prose)
Hovering a sentence shows its generated address, a `＋` for a comment, and a `💬` that focuses this page's chat on that exact line.
Hovering a `##` or `###` heading shows its breadcrumb, a `⧉` that copies the section as clean plain text, and a `🤖` that focuses the chat on the heading instead.
Clicking `💬` or `🤖` costs no model turn: it fills a focus card, and the location travels with your next message.

#### 1.3.2 · On a phone there is no hover
(one quiet `⋯` holds everything the rail would have shown)
A touch device shows a single `⋯` beside the sentence, which expands to the full address plus Comment, Chat and Edit.
Nothing is lost and nothing sits permanently on top of the prose.

**1.4 · 🚫 What must refuse you, and what to watch while it saves**

#### 1.4.1 · Three refusals worth trying on purpose
(each one answers with a reason and leaves what you typed in the box)
Write a card on words that are not in the sentence and the server refuses, because it matches the exact source line.
Write the same card on the same words twice and it refuses rather than filing a duplicate.
Act on a sentence that appears twice on one page and every writer refuses, rather than guessing which copy you meant.

#### 1.4.2 · What a good save looks like
(the reader's place is the thing most easily lost, so it is the thing to watch)
When you press Save the page must not jump: the scroll position holds and every section you opened stays open.
The new row or card appears on its own in about 0.4 seconds, and you should never need to press reload.
If the whole page flashes and returns you to the top, that is the defect this page fixed on 260802 and it has come back.


### 2 · Two surfaces: the card on the words, the lanes under the line
**What each surface is for**: the thing it holds, how many it holds, and what it costs the sentence.

```
🪪 THE CARD                      📎 THE LANES
──────────────────────────────   ──────────────────────────────
anchored on   a few words        anchored on   the whole line
opens         over the prose     opens         a drawer below it
holds         one thing          holds         any number
answers       "what is this?"    answers       "what do we know
                                                about this line?"
kinds         a reference · a    kinds         Citation · Value ·
              table's rows · a                 Display · Check ·
              figure's pictures                Q-consumer · Link ·
                                               Source · Note ·
                                               Comment · ✎ edit
ruled in      §3                 ruled in      §4 · §5 · §6
```
📌 Establishes the CONTRAST and stops there: what each surface is for, and why neither can do the other's job. How each one works is `### 3` and `### 4`.

#### 2.1 · Why they stay two things and not one
(merging them would either bury the reference or force a remark to claim words it is not about)
The card answers what a phrase IS, and the lanes answer what is known about the LINE.
Put the reference in the drawer and it sits under twelve unrelated rows, so the reader stops opening it.
Put a remark on a span and the writer has to pick words for a thought that was about the whole claim.
So the anchor differs by design: the card takes the words, the lanes take the line, and neither one has to pretend to be the other.

### 3 · The card: what may attach, and how it renders
**Where a card comes from**: two sources, one panel, and what each costs the sentence.

```
🪪 TWO SOURCES · ONE PANEL

  ✍️ a record        > Card the words: what to show
     span from       the record, quoted
     prose pays      nothing
     written by      typing the line · or select + 🪪 Card

  📐 a paper marker  \citep{} \cite{TOADD} {VAL:? …} [Q-X-n]
                     displayNN \ref{tab:|fig:}
     span from       the marker itself
     prose pays      nothing new · the author wrote it anyway
     written by      the build, resolved against .bib 1-probes/ displays/

  🎨 render   a button in the words · a native popover panel
  🚫 never    a box · a colour · a weight the prose does not have
```
📌 Establishes the card end to end: where one comes from, what it costs the sentence, and what the render refuses.

#### 3.1 · The words stay prose
(a box around them would turn a paragraph into a row of buttons)
A marker chip replaced text nobody wanted to read, so it may look like a control.
A card sits on words the author wrote and the reader is in the middle of reading, so it may not.
It keeps the sentence's own font, colour and weight, and takes one dotted accent underline.
The hover deepens that hint and never touches the text, which is the axis every chip on the page gives ground on.

#### 3.2 · The panel is real body text, not a tooltip
(a tooltip lives in an attribute, which the zero-script assertion cannot count)
The panel is a native `popover`, opened by `popovertarget` alone, so no script is involved.
Its content is counted by the build's survive-with-scripts-deleted assertion, it is findable with Ctrl-F, and it prints.
The `title=` stays underneath as the floor for anything that does not support `popover`.
Both were measured at 258 marker cards on the MISQ board, the paper board this was first rolled out on, and `tests/drive_sentence.py`, the recorded browser run, proves the record kind on a fixture.

#### 3.3 · What the render refuses
(a miss the reader cannot see is the one failure this grammar may not have)
Words the renderer cannot find in the sentence above become a loud row in the drawer, and that sentence's badge turns ⚠️.
Words that straddle markup are refused the same way, because splicing a button across a tag would emit broken HTML.
The write refuses earlier and for the same reason: the sentence must be found exactly once, the words must really be in that line, and the same card may not be written twice.
A refused write keeps the composer open with the typed text still in it.

### 4 · The lanes: the kinds, the drawer, and the badge
**One line, one record**: the first word names the kind, and the badge names what is underneath.

```
📎 THE KINDS · the first word decides
   📚 Citation   🔢 Value    🖼 Display   ⚠️ Check
   🔎 Q-consumer 🔗 Link     📄 Source    📝 Note
   💬 Comment WHO …          ✎ ~old~ *new* · WHO · time

🎖 THE BADGE · what is underneath, not just how many
   💬 a person is waiting   outranks
   ✎ a change was recorded  outranks
   ⚑ a typed lane is filed
   ⚠️ a card names words that are not there

🔒 the drawer is SHUT on load · always
```
📌 Establishes the lane half: the kinds, what holds them together, and why the drawer may stay shut.

#### 4.1 · A record is a run, not a line
(a multi-line paste keeps its shape instead of leaking into the page as prose)
A `>` line directly under a sentence attaches to it, and blank lines between them are tolerated.
Bare `>` lines after a typed head continue the same record, which is how a comment or a card can run to several lines.
Every writer builds its record through one `_record_lines`, which keeps continuations, turns a blank line into a single `>` break, and strips a leading `>` from typed text so a paste cannot forge a reply from someone else.
Before that, the second line of a multi-line comment landed in the page as PROSE, became a new writable anchor, and carried the timestamp away from the comment it belonged to.

#### 4.2 · The drawer stays shut, and the badge is why that is allowed
(an invisible fold is a broken fold, so the badge is the visible control that answers it)
A person's comment used to spring the drawer open, on the 260724 rule that a fold nobody can see is broken.
With every section shut, one burst-open comment block was the only loud thing on a calm page.
The badge answers the same rule better: it hangs at the sentence end, says how many rows are underneath, and says WHICH KIND, which `⚑ 2` never could.
It is a zero-width inline block, so the browser breaks the line exactly as it would with no badge present; measured over 111 window widths from 360px to 1800px with zero cases of it leaving its sentence's last line.

#### 4.3 · Writing one from the page
(double-click any sentence, or use the row that ends every open drawer)
`POST /_board/sentence` finds the exact sentence line and appends `> Lane: text` at the end of its existing run.
Double-click answers on a bare sentence and on one that already has a drawer; the drawer's own ➕ row is reachable only once it is open, so on an evidenced sentence the learned gesture used to do nothing, silently.
Where the form goes still differs: a bare sentence takes it `afterend`, and a drawer must take it at the end of its BODY, because inserting after the summary's `p` puts the form inside `<summary>`, where every click toggles the drawer.
Copy is section-level rather than per-sentence: every section heading carries a ⧉ that copies the whole section as clean plain text.

### 5 · A person's remark: `> Comment WHO`
**What a remark is**: one adjacent record, and the queue it replaced.

```
🗣 select a sentence → 💬 Comment → POST /_board/comment
                                       │
                        > Comment JL text · 260802 1400
                                       │
                              rebuild · swap · done

✅ any initials · the author and time are kept
✅ fold prose too · Law, Lesson, Glossary, Discussion all anchor
✅ a screenshot pastes straight in, uploaded to fig/
🗑 the page-bottom queue is DEAD: not read, not shown, not migrated
```
📌 Establishes the remark: why it sits under the line, and what it replaced.

#### 5.1 · Why it sits under the sentence
(a page-bottom queue makes the reader rebuild the context the writer already had)
A remark is written directly beneath the words it addresses, and nothing is stored to link them.
A queue at the foot of the page forces the reader to work out which sentence each entry came from, and it goes stale the moment the prose moves.
`> Comment WHO …` is the form to write, because beside `> Citation:` and `> Value:` a bare pair of initials said nothing about what the row was.
A remark made by selecting part of a line keeps those words: `> Comment JL 「the words」: …` renders them quoted ahead of the text (JL 260802, who asked whether a selection was recorded anywhere; it was not, and the words were thrown away after the highlight).
Selecting words does NOT make a card: a card answers what a phrase IS and holds one thing, while a remark is a person talking about the line, so the two stay apart and 🪪 Card is the button that makes the other one.
The older `> JL: …` still renders so nothing already written breaks, and `check.py` warns on it inside Content.

#### 5.2 · `## Discussion` is a different grammar and is untouched
(a thread with nested replies is not a note on one sentence)
`## Discussion` keeps `> JL:` with its `>> CC0726:` replies, because that is a conversation rather than a remark pinned to a line.
Fold prose is otherwise commentable like main text: the three blanket guards in `board.js` narrowed to what genuinely cannot anchor, so Law, Lesson, Glossary and Discussion prose all take sentence comments.
What stays excluded is rendered apparatus, which `serve.py` refuses to anchor on anyway.

### 6 · Changing a sentence: one line replaced, one record beside it
**The one-write result**: what the source looks like after an edit.

```
The coefficient is 0.42 in the clustered pooled model.
> ✎ The coefficient is 0.42 in the *clustered* pooled model. · JL · 260729 1502

📝 the old wording is never stored a second time
📝 there is no History section · every further edit adds one more row
📝 a comment or lane already below the sentence stays below it
🚫 refused: a duplicate sentence · a sentence carrying markdown decoration
```
📌 Establishes the edit: what one write leaves behind, and what it refuses to touch.

#### 6.1 · Why the diff is word-level and computed
(a model asked to show a diff writes a whole-sentence swap, which shows nothing that survived)
`~old~` renders struck through and `*new*` renders inserted, and they are a change record rather than ordinary emphasis.
`haipipe-writing`'s `cli/wdiff.py` computes them, and the same function emits the paper's `> Note:` notation from one flag.
The board had its own copy that agreed byte for byte, which is luck rather than construction, so `live/write.py` now calls the shared one and keeps its copy only as the fallback for a checkout without `haipipe-writing` beside it.
`tests/test_change_diff.py` compares the two over ten pairs on every run, so the day they drift is a red test rather than a review trail going quietly wrong.

#### 6.2 · What the anchor taught the whole family
(the badge lives INSIDE the `<p>`, so reading `textContent` posted a sentence that was not in any file)
Every writer here matches an exact source line, so one wrong character means the line can never be found.
The ⚑ badge became a zero-width span inside the paragraph, and all three writers read `p.textContent` raw, so an evidenced sentence posted `…below the read.⚑ 1` and the server was right to refuse it.
There is now ONE reader, `window.__boardSentenceText`, and the edit, lane and comment paths all use it.
It deletes buttons, because a marker chip's label is not the source text, with exactly one exception: a span card's label IS the source text, so that one is unwrapped instead.

### 7 · Why adjacency, and not new syntax
**Three ways to link a record to a sentence**: what each costs, and what breaks it.

```
🔗 HOW A RECORD FINDS ITS SENTENCE

  ✅ adjacency          the > line directly under the sentence
     cost              nothing · a line an author could have typed
     breaks when       the line moves without its records

  ❌ an id in the prose  a marker the reader has to look past
     cost              a second thing to keep in step
     breaks when       the prose is rewritten

  ❌ a sidecar file      one more file per page
     cost              two files to edit instead of one
     breaks when       anyone touches the .md by hand

⚖️ the whole family rests on the first row
```
📌 Establishes why nothing new was invented: the files already carried `>` runs under the sentences they discussed.

#### 7.1 · The convention was already there
(the paper unit docs wrote review threads under a sentence long before a board rendered them)
The paper unit docs already write review threads and `> Check:` blocks under the sentence they discuss.
Those files gained the behavior with zero edits the first time their board rebuilt.
That is the test this page keeps: every attached record is one line an author could have typed by hand.

#### 7.2 · Adjacency is a real binding, not a habit
(a lane placed after a paragraph attaches to the last sentence of it, which is not the one it is about)
A `>` line attaches to the sentence above it and to nothing else: no marker, no id, no sidecar file.
The MISQ rollout found the failure this creates.
A lane sat after a paragraph while its own prose said "the sentence above", so it had silently attached to the wrong sentence and had to be moved.
A concern that belongs to the whole page has no sentence to attach to, and it belongs in `## Aims`, or in that Aim's `Plan` when the move is temporary.

#### 7.3 · One lane is one source line
(a wrapped lane becomes its own row on the page and captures every lane below it)
A lane is one source line, however long it runs.
Wrap it and the second half becomes its own sentence row, takes its own badge, and captures every lane written beneath it.
The markdown looks fine and only the rendered page shows the broken row, which is the same one-sentence-per-line rule the prose already obeys.

### 8 · What still has its own page
**After the fold**: what this page now owns outright, and the two things that did not belong in it.

```
🚪 THIS PAGE          the sentence, and everything written onto it
   §3 the card · §4 the lanes · §5 the remark · §6 the edit

📤 MOVED OUT
   QD8   the generated address, and what an agent is handed
         a machine POINTING AT a location is not a thing attached
         to a sentence, and its consumer is the chat drawer

📄 STILL ITS OWN PAGE
   QB5e  filter · resolve · archive · restore · purge
         nothing in it is built, and its identity question is open

🗄 ARCHIVED 260802   _archive/QB5a  QB5b  QB5c
   old ids still resolve through board.md's Links table
```
📌 Establishes where each part of the old family went, so a link written under the five-face naming still lands somewhere real.

#### 8.1 · Why the five faces folded
(the split was carved for a model that 260802 replaced)
The faces were carved on 260729, when the sentence was one thing with five attachments and a page for each.
The card ruling turned it into TWO surfaces, and the split stopped carrying that: `QB5a` ended up owning both while its own title still said "click a sentence", which is the lane gesture.
`QB4` met the identical shape and folded its seven section faces into its own Content on 260801, so this page followed the precedent rather than inventing a second answer.
Folding three faces in brings this page to roughly half the size `QB4` already carries, so the cost is a longer page and the gain is one place to look.

#### 8.2 · Why the address left instead of folding in
(it answers a different question, and its consumer is somewhere else)
`QD8` gives every heading and Content sentence a generated `C/H/P/S` address and rules what an agent acting on that location is handed.
That is not an attachment: nothing is written under the sentence, and nothing is written into the file at all, because the addresses are made at render time and stored nowhere.
Its readers are the chat drawer and the routing verb, both of which live in the working lane, so it sits beside `QD1`'s one session per page rather than under the sentence.

#### 8.3 · Why the lifecycle stayed a page
(an unbuilt design with an open identity question is exactly what a page is for)
`QB5e` rules what happens as records pile up: typed views, record states, previewed cleanup, archive, restore, and purge.
None of it is built, and it carries the one identity question the family has not answered, which is whether an attached record needs a durable key of its own.
A render address says where a record appears in the current render, so archive and restore cannot use one, and that fork has to stay visible rather than be buried in a division of this page.


## Aims
### A1 · 🧪 Try it yourself: every feature, live on this page
- A1.1 · A reader can exercise every gesture this page rules without reading the rest of it.
  **Done when:** `### 1` carries one live row per thing that can be clicked and one written instruction per thing a person does themselves, and every one of them works on the rendered page.
- A1.2 · A reader has somewhere safe to practise.
  **Done when:** `### 1.2.5` is a sentence that carries nothing and says it is there to be written on.

### A2 · 🪪 Two surfaces: the card on the words, the lanes under the line
- A2.1 · The two surfaces stay apart: a card anchors to marked words, a lane anchors to the whole line.
  **Done when:** Every face states which of the two it rules, and none of them describes a card as a thing a sentence click opens.
- A2.2 · A reader can put a card on any words they pick, not only on a marker the build already resolves.
  **Done when:** A span selected on a rendered page gains a card, the write lands in the markdown, and the same click reopens it after a rebuild.
- A2.3 · The lane's kinds stay an open list, so new work costs a first word and nothing else.
  **Done when:** Every kind named in `### 4` renders with its own glyph, and adding one touches only `src/body.py`'s `LANE` pattern.
- A2.4 · Saving a record keeps the reader exactly where they were, on EVERY write path.
  **Done when:** A recorded browser run shows the scroll position and every open section unchanged across a save, on all four: the card, the comment, the edit, and the typed lane.
- A2.5 · No write ever waits for a person to press reload.
  **Done when:** Each of the four paths repaints from the write itself, and the run measures how long each took.

### A3 · 🎴 The card: what may attach, and how it renders
- A3.1 · A card renders as the words themselves, never as a control sitting in the prose.
  **Done when:** A card's button matches its paragraph's font, colour and weight, carries no box, and is distinguished only by an underline.
- A3.2 · A card's content is readable with every script deleted.
  **Done when:** The build's survive-with-scripts-deleted assertion counts the panel text, and a run confirms it on a real page.
- A3.3 · A card that cannot bind says so where the reader is looking.
  **Done when:** Words absent from the sentence render a visible row and turn that sentence's badge to ⚠️, and the three write refusals each keep the composer open.

### A4 · 📎 The lanes: the kinds, the drawer, and the badge
- A4.1 · A record keeps whatever shape the person typed, however many lines it runs to.
  **Done when:** One `_record_lines` serves the comment, lane, card and discussion writers, and a multi-line save produces one `>` run with nothing loose.
- A4.2 · The drawer stays shut on load and the badge says what is underneath.
  **Done when:** Every sentence drawer is shut on a fresh render, and the badge names the kind rather than only the count.

### A5 · 🗣 A person's remark: `> Comment WHO`
- A5.1 · A remark is written under the exact sentence it is about, and survives every rebuild.
  **Done when:** A selection saves a `> Comment WHO` row beneath its source sentence, and no page-bottom queue exists anywhere.

### A6 · ✎ Changing a sentence: one line replaced, one record beside it
- A6.1 · An edit replaces one source line and leaves one readable record of what moved.
  **Done when:** The saved source holds the final sentence plus one whole-sentence diff row, with no History section and no second copy of the old wording.
- A6.2 · One computation serves every word-level diff on the board.
  **Done when:** The board's `✎` diff and `haipipe-writing`'s `wdiff.py` are one implementation rather than two that agree.
- A6.3 · The `QE4` boundary is honored: locks and multi-writer stay there.
  **Done when:** This page rules the single-sentence write and names `QE4` for concurrency, with no lock rule written here.

### A7 · 🔗 Why adjacency, and not new syntax
- A7.1 · Adjacency stays the only binding between a sentence and its records.
  **Done when:** Every attached record on this board is one line an author could have typed, with no id in the prose and no second file.

### A8 · 🗺 What still has its own page
- A8.1 · Every part of the old five-face family has one findable home.
  **Done when:** `QB5a` `QB5b` `QB5c` are folded in and archived, `QB5d` lives in the working lane, `QB5e` stands alone, and every old id still resolves.

## States
### A1 · 🧪 Try it yourself: every feature, live on this page
- ✅ A1.1 · Rebuilt 260802 on JL's ask for a showcase and a test sheet in one. Five live rows to click (card, three lanes, a remark, a change, a broken card), four written procedures (comment, card, lane, edit), the hover rails and the touch menu, three refusals worth trying, and what a good save looks like.
- ✅ A1.2 · `### 1.2.5` is a bare sentence that says on its face that nothing on it matters.

### A2 · 🪪 Two surfaces: the card on the words, the lanes under the line
- ✅ A2.1 · `### 2` and the `## Diagram` figure split the two anchors, and `### 3` and `### 4` now rule one each. The face that owned both, and mis-titled itself "click a sentence", was archived when the family folded on 260802, so nothing describes a card as a thing a sentence click opens.
- ✅ A2.2 · Built and driven 260802. JL delegated the ruling ("You make the best decision and I will just check it how it works on the board") and CC ruled option D, which none of A, B or C had proposed: the record names its own span, `> Card <the words>: <text>`, so the prose pays nothing. `src/body.py` renders it, `live/write.py`'s `add_card` writes it behind `POST /_board/card`, and 🪪 Card appears beside 💬 Comment on any selection whose words are really in the sentence. Proven in JL's own Chrome by `tests/drive_sentence.py`, now 36 checks green, including select, write, reopen, and three refusals.
- ✅ A2.3 · Eight typed kinds plus `> Comment WHO` and `> ✎` all render from their first word, through the single `LANE` pattern at `src/body.py:704`. `Card` joins them as the one record that renders inside the sentence instead of under it.
- ✅ A2.4 · Measured on all four. Card 883 to 883 with 16 sections open before and after; comment 1204 to 1204; edit 1925 to 1925 with 16 to 16; typed lane unchanged across the save. A window flag set before the edit is still there after it, which is how the run proves it SWAPPED rather than reloaded.
- ✅ A2.5 · All four repaint in 0.4s. Two were broken until 260802 and neither had ever been tested past the point where it could not fail. Editing called `location.reload()` on save, and even after that was replaced the swap silently refused, because the editor's own textarea sits inside `div.wrap` and the swap will not run while a textarea in there holds text: the `> ✎` record reached the markdown and the page sat unchanged until somebody pressed reload. Adding a typed lane never asked for a repaint at all and waited on the background poll, which backs off to five seconds on a page nobody has touched. Both forms now CLOSE first and then ask.

### A3 · 🎴 The card: what may attach, and how it renders
- ✅ A3.1 · Measured in Chrome, not eyeballed: the card's button reports the same font, colour and weight as its paragraph, `border: none`, and a dotted underline.
- ✅ A3.2 · The panel is a native `popover` and its text is counted with every script deleted. 258 marker cards measured on the MISQ board; the record kind driven on the fixture.
- ✅ A3.3 · A card naming absent words renders its row and turns that sentence's badge ⚠️. All three write refusals answer with a reason and leave the typed text in the composer.

### A4 · 📎 The lanes: the kinds, the drawer, and the badge
- ✅ A4.1 · One `_record_lines` has served all four writers since 260801, and a three-line card body arrives whole in its panel.
- ✅ A4.2 · Every sentence drawer is shut on a fresh render and the badge names the kind. Verified over 111 window widths that it never takes a line of its own.

### A5 · 🗣 A person's remark: `> Comment WHO`
- ✅ A5.1 · Shipped and settled. A selection writes `> Comment WHO … · time` beneath its sentence; the page-bottom queue and its status lifecycle were deleted on 260729 and are not read, shown, or migrated.

### A6 · ✎ Changing a sentence: one line replaced, one record beside it
- ✅ A6.1 · Shipped 260729. One source line is replaced and one `> ✎` row records what moved; a duplicate sentence and a decorated sentence are both refused rather than guessed at.
- ✅ A6.2 · Wired 260802 on JL's standing go, which is the row's own default. `live/write.py`'s `_change_diff` now calls `haipipe-writing`'s `wdiff(host="board")`, looked up by path rather than imported so every unit in the family stays deletable from every other. The local computation survives as the fallback, and `tests/test_change_diff.py` compares the two over ten pairs on every run, so the day they drift is the day a test goes red instead of a review trail going quietly wrong.
- ✅ A6.3 · Honored. This page rules the single-sentence write and names `QE4` for locks and concurrent writers, writing no lock rule of its own.

### A7 · 🔗 Why adjacency, and not new syntax
- ✅ A7.1 · Settled and live on every board. `src/body.py` binds a `>` run to the plain sentence above it and reads nothing else.

### A8 · 🗺 What still has its own page
- ✅ A8.1 · Executed 260802 on JL's go. `QB5a` `QB5b` `QB5c` folded into `### 3` to `### 6` and archived, `QB5d` moved to `QD8`, `QB5e` left standing, and every retired id aliased in `board.md`'s Links table.

## Files
### ⚙️ Engines · what RUNS this subject
- `src/body.py`
  RENDER, both surfaces. The `LANE` pattern and the adjacency walk that folds a `>` run under the sentence above it, the badge that names which kind is underneath, and `_chip`, which turns a marked span into a button and its card into a `popover` panel.
- `src/dialect_paper.py`
  RESOLVE. What a marked span is looked up against before it can become a card: the paper's `.bib`, its `1-probes/`, and its `displays/`.
- `cli/serve.py`
  WRITE. The routes that add a remark, add a typed lane, or replace one sentence, each anchored on an exact source line.
- `assets/js/40-sentence/00-apparatus.js`
  The controls a reader touches: the generated address, the `＋` Comment row, the `💬` Chat action, and the `⋯` menu on touch.

### 🗄 Archived · the faces this page absorbed on 260802
- `QB-delivery/_archive/QB5a-evidence-card.md`
  Became `### 3` and `### 4`. Its design history stays here rather than being rewritten.
- `QB-delivery/_archive/QB5b-comments.md` · `QB-delivery/_archive/QB5c-editing.md`
  Became `### 5` and `### 6`.

### 🧪 Checks · what CATCHES a page breaking a rule
- `cli/check.py`
  Owns `old-comment-form`, which warns when a sentence comment inside Content still uses the bare `> JL:` shape.
- `tests/drive_sentence.py` · `tests/fixture_board.py`
  The recorded browser drive: it builds a throwaway board, serves it, moves the real mouse through every gesture, and writes one screenshot and one row per step. It is the only check that can see a correct file on a wrong page, which is how every sentence defect so far reached JL.

## Lesson
- 260802 JL · 🔍 A test that stops where the code cannot fail is not a test
  JL: "did you test the things that, when I add comments, or I do the editing, the page refresh, and only I do the refresh, it will be updated?"
  The run had a step called "double-click opens the sentence editor", and it checked exactly that: the editor opened.
  Everything after the opening was untested, and that is where both defects were, one of them a `location.reload()` the whole session had been trying to remove.
  A step now follows each write to the thing a reader would actually look for: the row appearing, a window flag proving the frame was not thrown away, and the scroll and open sections after the save.

- 260802 CC · 🚧 The guard that protects your typing also blocks your save
  The swap refuses to run while any textarea inside `div.wrap` holds text, which is what stops a rebuild from eating a half-written comment.
  A save form is inside `div.wrap` and still holds what was just saved, so asking for the repaint before closing the form asks for something that can only be refused.
  It had never shown before because the edit path used to reload, which meets no guards at all, so replacing the reload with the correct call is what exposed it.
  Both forms close first and then ask, and the rule is that a writer clears its own draft before it asks for the page back.

- 260802 CC · 🧪 A test that writes into the page it is testing is not a test
  The first browser drive drove `QB5` itself, and did two unforgivable things at once.
  It left five cards on a page a person reads, and its second run found the sentences already carrying what the first run had written, so a pass and a break became the same result.
  `tests/fixture_board.py` now builds a two-page board in a temp folder with one paragraph shaped per gesture, including a sentence written twice so an ambiguous anchor can be driven at all.
  The run serves it on a free port, drives it, and deletes it.

- 260802 CC · 🎯 The fold restore was keyed on what the SCREEN said, not on what the page said
  A comment saved at scroll 1112 came back at 171 with every section shut, while a card saved at 883 came back at 883.
  `board.js` decorates a summary after each render, so the old one read "📚 Content C1 ⧉ 🤖" and the freshly fetched one read "📚 Content", and the keys never matched.
  Nothing reported it because the text fallback only runs when the drawer COUNT changed, which happens exactly when a sentence gains its FIRST record: the comment path, and nothing else.
  Both sides are now read with the runtime decoration stripped, the same way `sentenceText` reads a sentence for its anchor.

- 260801 JL · 🧪 The family's operations now have a run of their own
  JL: "I feel the sentences part is almost crash", after three separate sentence defects reached him in a week.
  `QF5` owns the answer: seventeen shapes a sentence can take, crossed with the six operations that read one, and five assertions per cell.
  Its first tier is written and was red on its first run, which is the only evidence a test is worth keeping.

## Glossary
- ✏️ **sentence**: one source line of prose, and the smallest thing on a board a person can point at, comment on, or edit.
- 🪪 **card**: the panel that opens over the prose when a reader clicks a marked span of words, such as the reference behind a `\citep{}`.
- 📎 **attached record**: a line starting with `>` written directly under a sentence, which belongs to that sentence and to no other.
- 🖱 **span**: a few words inside a sentence, taken together, which is what a card is anchored to and what a lane is not.
- ⚑ **typed lane**: an attached record whose first word names its kind, such as `> Citation:` or `> Value:`.
- 🎖 **badge**: the small mark at the end of a sentence saying how many records sit under it and which kind, such as `⚑ 3` or `💬 1`.
- 🔘 **chip**: the button a card renders as. On a span card it keeps the prose's own font, colour and weight; on a paper marker it replaces the marker's text.
- 📐 **paper board**: a board whose pages are the stages of a paper being written, which is the only kind that resolves markers into cards.
- 🗂 **apparatus**: the technical name for all the records attached beneath one sentence; the panel a reader opens is called Sentence details.
- 🔗 **adjacency**: the rule that position alone binds a record to its sentence, with no id in the prose and no second file.
- 🪞 **face**: a page carrying one part of a subject, whose id is its parent's id plus a letter, as `QB2a` is a face of `QB2`. This page had five until 260802; a face is folded back in once it stops carrying a subject of its own.

## Log
260802 2200 · JL moved the decorated-sentence ruling here from `QC4a`, where CC had put it by anchoring to `live/write.py` instead of to the page that owns the gesture. `### 8` already claimed `§6 the edit` for this page. The misplacement had hidden that this page went ✅ SETTLED while `### 6`'s figure recorded the refusal as a fact, and it covers 44.8% of the board; whether the ✅ survives is part of the row
260802 · 🧪 `### 1` rebuilt as a showcase AND a test sheet, on JL's ask for a showcase of every feature that also instructs the reader how to try each one. It opens with one figure listing every gesture, then four groups: rows that are already live and only need clicking, procedures a person carries out themselves on a practice line that exists for the purpose, the controls that appear only on hover and what replaces them on a phone, and the three refusals worth triggering on purpose plus what a good save looks like. A deliberately broken card was added so the ⚠️ badge and its loud row can be seen rather than described
260802 · 🔎 A fresh reviewer read the folded page cold and returned `revise` with 28 findings; 26 were real and are fixed. The three that mattered were contradictions the fold created and nobody had reread for: the Opening's last sentence still said this page "hands each attachment to its own page", which is the pre-fold model and the one paragraph a reader gets without clicking; `### 6.1` still described the `✎` diff as two implementations agreeing by luck, hours after `A6.2` recorded it wired; and a live pointer aimed at a `### Decision Now` row whose heading was left behind empty, which the render drops entirely. `### 2` was also a compressed copy of `### 3` and `### 4` in nine places, so its mechanism paragraphs went and it is now the contrast alone; the card demonstration moved into `### 1`, where "try it on this row" had been covering only the lanes. Four 📌 lines advertising which archived face each division came from are gone, since that belongs here. Also added: the canonical `**Covered elsewhere**` part the `## Boundary` ruling requires, Glossary rows for `badge`, `chip` and `paper board`, and first-use definitions for the MISQ board and the drive. One finding did NOT survive: it asked for the section emoji to move onto the `###` division headings, which `check.py` reports as `group-name-drift` on all sixteen Aims and States groups, so only its real half was taken, that `A2` and `A3` had both been using 🪪
260802 · ✅ SETTLED. JL moved the state line after the five faces folded, the card shipped, all four write paths were proven to repaint without a manual reload, and the `✎` diff became one computation. Sixteen Aims across eight divisions, all closed
260802 · 🔗 One computation for the `✎` record. The board's `_change_diff` and `haipipe-writing`'s `cli/wdiff.py` had both computed it with difflib and agreed byte for byte, which is luck rather than construction. The board now calls `wdiff(host="board")`, found by path so the two units stay deletable from each other, and keeps its own copy as the fallback that answers when `haipipe-writing` is absent. `tests/test_change_diff.py` compares the fallback against the shared function over ten pairs, including an empty side and a full replacement, so drift is a red test rather than a silently different review trail
260802 · 🌐 A second recorded drive opened, `tests/drive_board.py`, 16 checks green against the REAL board rather than a fixture: the Index lists pages and no longer lists the folded faces, all six touched pages open and carry their subject, QB5 renders its eight divisions, its demonstration cards open on the real page, an id inside the prose navigates, and the page still reads with every script deleted at 420px wide. Its first run reported three false reds because it read `innerText`, which reports only what is on screen while every section is folded shut; it reads `textContent` now, and its detail line said "found X" whether or not X was found, which made a red row read like a green one
260802 · 🔍 The other two write paths were never tested past the point they could not fail, and both were broken (JL asked directly whether a comment or an edit needs a manual reload). EDITING called `location.reload()` on save, throwing away the scroll and every open section; replacing it with the swap then exposed a second defect, that the swap refuses to run while a textarea inside `div.wrap` holds text, so the `> ✎` record reached the markdown and the page did not change until somebody pressed reload. ADDING A TYPED LANE never asked for a repaint at all and sat waiting for the background poll, which backs off to five seconds. Both forms now close before asking. The run grew to 36 checks, four of them following the edit and the lane all the way to the repainted row, and all four paths now land in 0.4s
260802 · 🗺 The five faces FOLDED, on JL's go ("ok go, and work on it and test it"), option C. `QB5a` `QB5b` `QB5c` became this page's `### 3` to `### 6` and were archived; `QB5d` moved to `QD8` in the working lane, because a generated address is how a machine POINTS AT a location rather than a thing attached to a sentence, and its readers are the chat drawer and the routing verb; `QB5e` stayed its own page, since nothing in it is built and its identity question is open. Same shape and same answer as `QB4`'s seven section faces on 260801. Aims and States rebuilt to eight groups mirroring the eight divisions, every live cross-reference on eight sibling pages repointed, and every retired id aliased in `board.md`'s Links table so nothing already written breaks. Board 54 pages to 51
260802 · 🪪 The span card SHIPPED, and the ruling behind it. JL delegated the choice ("You make the best decision"); CC ruled option D, which the three drafted options had missed: the record names its own span, `> Card <the words>: <text>`, so the prose gains nothing and the binding is the same exact-text match the write layer already uses one level up. `src/body.py` (`CARD_LANE`, `_split_cards`, `_wrap_span`, a `head=` on `_chip`), `live/write.py` (`add_card`, three refusals), `cli/serve.py` (`POST /_board/card`), `assets/css/60-chips.css` (the words stay prose: no box, one dotted underline), and a 🪪 Card button beside 💬 Comment. `sentenceText` had to learn ONE exception: it deletes every button, because a paper chip's label is not the source text, and a span card's label IS
260802 · 🎯 Saving stopped throwing the reader back to the top (JL: he asked how to make this smooth, because adding a comment and hitting save made the whole thing refresh). A pane used to `location.reload()` on every write; it now runs the same drawer-preserving swap the single-document path always had, and the writer asks for it immediately instead of waiting up to 800ms for the poll. The swap's fold restore was also keyed on decorated summary text and never matched, which is why only the comment path looked bad. Measured: scroll and open sections unchanged across both saves, both landing in 0.4s
260802 · 🧪 `tests/drive_sentence.py` opened: a recorded Chrome drive over its own throwaway board, one screenshot and one row per gesture, 14 of 14 green. It exists because every sentence defect that reached JL had passed the unit tests first
260802 · JL split the sentence into TWO surfaces: a card reached by clicking the marked words, and the lanes reached by clicking the whole line, taking a citation, a comment, or any other kind. Written as the new `### 2`, with the Opening, the `## Diagram` figure, and `### 4.1` brought to it; old `### 2` and `### 3` became `### 3` and `### 4`, and Aims and States gained `A2` and renumbered to match. One Decision Now row opened: how a span carries a card when adjacency can only bind a whole line
260802 · Rebuilt to the page contract: `Boundary` deleted with its pointers moved into the Opening's More details, `Items to Finish` and `Where we are` became `Aims` and `States` with three groups mirroring Content, Content renumbered `### 1` to `### 3` with a captioned face figure each, `Files` regrouped and its five dead face paths repaired, and a Writing Style plus a Glossary added. The 260801 JL record moved verbatim from the old `Where we are` into `## Lesson`
260802 · Comment and badge wording brought to the 260802 rulings: a person's remark is written `> Comment WHO …` (the bare `> JL:` still renders, and `check.py` warns on it inside Content), attached records start SHUT, and the badge names which kind is under the sentence, `💬` a person waiting over `✎` a change over `⚑` a typed lane. The demonstration was split into one live row per badge kind so all three can be clicked
260802 · Legacy ids `QAb0`-`QAb4` and `QA6` replaced by `QB5` and `QB5a`-`QB5e` throughout the prose and Files; the alias map in `board.md` still resolves the old ones, so nothing already written breaks
260801 · `QF5` opened as the sentence family's test face: the shape matrix, the operation matrix, and the four tiers, with tier 1 running today
260731 1905 · Sentence-tail ⚑N badge no longer strands on its own line: renderer now glues it to the last word inside the `<p>` (`.snw` nowrap wrapper in body.py + board.css), so it sits at the sentence end and wraps together with the last word when space is tight
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260729 · Added §1 Demonstration so one sentence exposes Evidence, Comment, Chat, Edit, address, and the QAb4 lifecycle boundary before the reader enters the detailed family map
260729 · Added QAb4 as the independent Sentence details lifecycle face for filters, statuses, cleanup, archive, restore, and purge
260729 · Opened as the sentence family's front door when QAb was carved (JL: QAb0 overview, QAb1 evidence card, QAb2 editing)
