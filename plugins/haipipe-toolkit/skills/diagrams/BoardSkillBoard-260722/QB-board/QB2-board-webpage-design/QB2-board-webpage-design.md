# Board · the webpage: what the Index shows, and how the shared surface looks
state: 🟡 PARTIAL
owner: JL
method: distinguish the Board-Webpage-Index from an opened Board-Webpage-Page, then settle what the Index must answer and how the shared surface makes it legible
session: d2199106-8b6a-499d-8c24-9db3658486b5

## Opening
How should the Board Index help a reader pick the right page in three seconds?
The Index is the top of `board.html`: the list you land on before you open anything.
One row on it is one page, and that row has to show enough to choose without opening it.
That is hard because state, owner, progress, and how the pages relate all want the same thin strip of screen.
This page rules what the Index shows, and how the surface every page shares should look.

**What the two names mean**: A Board-Webpage-Index is the view before any page is open: board name, spine, close condition, progress, Board Map, Related Folders, Section Matrix, grouped page rows, Activity.
A Board-Webpage-Page is the focused view of one page inside the same site, such as this one.
This page owns the first. `QB4` owns the second.

**Where this page sits**: The board walks down one ladder: Board, Group, Page, Section, Sentence.
`QB1` owns the board's folder on disk, and `QB3` puts a page's file beside the work it describes.
This page takes the rung a reader meets first: the Index, plus the visual language every view shares.
`QB2a` carries the pages sidebar that travels with it.

**What is settled elsewhere**: Whether a page's prose is well written, and the mechanical checks run after any change, belong to `QA9`.
Paper and venue writing style belongs to the Paper lifecycle.

**Why it matters**: A reader who cannot see what is stuck, or whose move it is, has to open every page to find out.
This board has 57 of them, and 52 of those have nothing waiting on anyone.

## Diagram

**The Index on screen**: what a reader meets at the top of the board, before any page is open.

```
┌──────────────────────────────────────────────┐
│ board name · 🦴 spine · 🏁 close condition    │
│ ▓▓▓▓▓░░░░░  N/M settled                      │  progress bar
├──────────────────────────────────────────────┤
│ 🗺 Board Map                                  │
│ ┌──── QB1 ────┐   owns    ┌──── QB4 ─────┐   │  one figure,
│ │ folder form │ ────────► │ page contract│   │  one box per page;
│ └─────────────┘           └──────┬───────┘   │  arrows are authored
│                                  owns          │  relationships only
│                           ┌──────▼───────┐   │
│                           │ QB8 sentence │   │
│                           └──────────────┘   │
├──────────────────────────────────────────────┤
│ 🗂 Related Folders   🩺 Section Matrix        │  two more folds, shut
├──────────────────────────────────────────────┤
│ QB · Delivering a board          [＋Q] [🗄]  │  group header, hover controls
│ ▸ one always-visible sentence                │  ← group intro
│   click ▸ → what this group is for, and why  │
│  ✅ QB1  Board folder shape        🔧 CC      │  ← what does a row show?
│  🟡 QB4  The page template     🔧 CC     9/20 │  ← how is completion coloured?
│  🔴 QB2a Pages sidebar           🗄 🔧 CC   0/4 │  ← hover 🗄, archive, 2 clicks
│  …                                            │
│  [＋ Group]                                   │
├──────────────────────────────────────────────┤
│  … all the page rows …                       │
├──────────────────────────────────────────────┤
│ 📈 ACTIVITY                                   │
│  WHEN  14 days   ▁▁▁▂▇▄▅▅  outer = all boards│
│                            inner = this one  │
│  WHERE Board → Group → Page, one count each  │
│  the unit is ONE UPDATE = one dated ## Log   │
│  line, so it reads every tool, not a tab     │
└──────────────────────────────────────────────┘
         ↑ in three seconds: "which page do I act on?"

  every button is only a writer into board.md:
  ＋Q       a new QXN-slug.md, listed under its group
  ＋Group   a new "### QX · title" in ## Pages, letter auto
  🗄        the file moves to _archive/, or an EMPTY group is removed
```

**How a visual change is allowed to happen**: the path from an outside taste rule to a board rule, or to a recorded rejection.

```text
🎨 outside taste rule
        ▼
🔍 scope filter    research control plane, not a marketing page
        ▼
📋 read-only audit index · page · chat · mobile · dark · no-JS
        ▼
🧪 prototypes      at most three, isolated
        ▼
👁 human comparison
   ✅ adopt ──▶ 📐 board specification + QA9 checks
   ❌ reject ─▶ 📝 this page, with the reason it does not fit
```


## Content
### 1 · Board-Webpage-Index and Board-Webpage-Page
**One site, two reader views**: what a reader gets before opening a page, and what they get after.

```text
🌐 the generated Board-Webpage
   │
   ├─ 🗂 BOARD-WEBPAGE-INDEX          👀 nothing open yet
   │     🦴 spine · 🏁 close condition · ▓▓▓░░ progress
   │     🗺 Board Map · 🗂 Related Folders · 🩺 Section Matrix
   │     📄 grouped page rows · 📈 Activity
   │                                        ⬅ QB2 owns this
   │        🖱 click one row
   └─ 📄 BOARD-WEBPAGE-PAGE           🔎 one page, focused
         🧭 Opening · 🖼 Diagram · 📚 Content
         🎯 Aims · 📍 States · 📎 Files
                                            ⬅ QB4 owns this
```
📌 Names the two views, so every later part can say which one it is talking about.

The Board-Webpage is one generated `board.html` with two reader views.
The Board-Webpage-Index is the view a reader lands on: it gives the Board name, Spine, Close condition, progress, the Board Map, Related Folders, the Section Matrix, the grouped page rows, and Activity, all before any individual page is shown.
Topic, Pipeline, and Board-Structure left the rendered Index on 260731 (JL: "I want to just remove this"); their `board.md` sections remain source-only documentation, because the spine, the Board Map, and the matrix already orient a reader.
A Board-Webpage-Page is the focused view of one page inside the same site.
This page owns the Index and the shared visual language; `QB4` owns the opened page's sections.

### 2 · Overall progress, show how far the board has moved
**Two counters, never one**: what the progress area reports, and what it refuses to mix.

```text
🎯 SETTLED Q     ▓▓▓▓▓░░░░░   decisions closed
🏁 PASSED S      ▓▓▓░░░░░░░   stage gates passed
────────────────────────────────────────────────
🚫 never added into one number
🚫 ⏸️ parked never counts as done
❓ answers      how far along is this board?
```
📌 Settles that a lifecycle stage may never inflate the question count, and a pause may never read as done.

The global progress area reports settled Q decisions and passed S gates as separate workflow signals.
It answers "how far along is this board?" without implying that a paused page is complete or allowing lifecycle stages to inflate question settlement.

### 3 · Group, explain why these pages belong together
**A group header, opened**: the one sentence on stage, and what the click reveals.

```text
📁 QA · Defining a board                         [＋Q] [🗄]
   ▸ 📖 one sentence            👁 always visible
        🖱 click ──▶ 📜 what this group is for, and why it exists
   📄 QA0 · QA1 · QA2 · QA3
──────────────────────────────────────────────────────────
✍️ source    board.md ## Pages, plain lines under the ### heading
🥇 line 1    the visible sentence
📚 the rest  the drawer
```
📌 Settles that a group explains itself, so its members do not have to be opened to learn why they are together.

Each group header names one coherent part of the board and carries a short, always-visible introduction.
Opening the introduction reveals what the group is for and why it exists.
Group controls add a Q or archive an empty group, but the explanation remains the primary reading signal.

### 4 · Page row, identify the next action
**One row, six signals**: everything a reader gets before deciding whether to open a page.

```text
📄 ONE ROW ON THE INDEX
   🚦 state      ✅ settled · 🟡 partial · 🔴 open · ⏸️ parked
   🏷 id         QB1
   📛 title      Board folder shape
   💬 comments   a badge, only when a comment is open
   👤 owner      🧠 JL decides · 🔧 CC works
   📊 finish     7/9, row tinted white ▸ green by ratio
──────────────────────────────────────────────────────────
❓ it must answer   whose move is it, and is this one stuck?
🚫 nothing else earns a place in the row
```
📌 Settles that a row carries only what a reader needs to choose, and names the question the row exists to answer.

Each row exposes only the evidence needed to choose whether to open it: workflow state, id, title, open-comment signal, owner, and finish ratio.
Its most important eventual job is to make "which page needs action, and whose action is it?" answerable within three seconds.

### 5 · Ordering, make priority legible
**Two orders, one still open**: what decides the sequence today, and what nobody has ruled.

```text
📚 ORDINARY BOARD
   ✍️ hand-written in board.md ## Pages
   ❓ whether state, unfinished work, owner or open comments
      should reorder it is UNRULED

📄 PAPER LIFECYCLE BOARD
   🌱 Seed ▸ 🔨 Work ▸ 🏛 Venue ▸ 🖼 Display
        ▸ 📖 Main ▸ 📎 Appendix ▸ 📮 Submission
   🔒 stable ownership order, NOT a claim that work is linear
   🎯 one S page per row · its blocking Q sits right after it
──────────────────────────────────────────────────────────
⚖️ any automatic sort must be explainable and must never rewrite the source
```
📌 Settles the lifecycle grouping and keeps ordinary-board sorting explicitly open.

Group order and row order tell the reader what to scan first.
Today they follow the hand-written Pages; the open design decision is whether state, unfinished work, owner, or open comments should influence that order.
Any automatic sort must remain explainable and must not silently rewrite the source.

For a paper lifecycle board, ordering has one stronger rule: named S families are the groups.
The index follows `Seed → Work → Venue → Display → Main → Appendix → Submission`, but this is stable ownership order, not a claim that execution is linear.
Pipeline owns actual edges and may revisit the independent Display layer after Narrative.
Each S row is one concrete checkable page, and a blocking Q sits immediately after the S page it governs.
Seed includes S Seed and S Literature; Main and Appendix expose every reader-facing unit instead of hiding them inside one broad section-edit stage.
A paper-level decision may sit before Seed only when it genuinely governs the full lifecycle.

### 6 · Structure controls, edit without hiding the source
**Three buttons, one writer**: what each control does to the markdown behind the page.

```text
🖱 ＋Q       ──▶ 📄 a new QXN-slug.md, listed under its group
🖱 ＋Group   ──▶ 📁 a new "### QX · title" in board.md ## Pages
🖱 🗄        ──▶ 📦 the file moves to _archive/
                    an EMPTY group is removed
                          ▼
              ✍️ POST /_board/structure   the ONE writer
                          ▼
              📝 board.md and the page files stay the source of truth
──────────────────────────────────────────────────────────────
🚫 nothing is ever deleted · every op is two-click confirmed
```
📌 Settles that the buttons only WRITE the markdown, so the page never becomes a second source of truth.

`＋Q`, `＋Group`, and archive controls are page-side writers into `board.md` and the page files.
They make the index operational while preserving markdown as the single source of truth; archive moves material rather than deleting it.

### 7 · Board chat, discuss the board as a whole
**Chat beside the Index, never instead of it**: what a conversation adds, and what it cannot replace.

```text
🤖 BOARD CHAT                    👁 THE INDEX ITSELF
   🗣 "how should we work?"         🚦 which page needs action
   🗣 "which page next?"            👤 and whose action is it
   📎 attached to board.md          📄 read straight off the rows
   ⏱ minutes                       ⏱ three seconds
──────────────────────────────────────────────────────────
⚖️ chat is deliberation; the three-second visual answer is still owed
```
📌 Settles that the chat entry is an addition to the Index, and never the way a reader finds the next action.

Board chat is the place to ask how the work should proceed or which page to examine next before opening one.
It supports deliberation, but it cannot replace the index's visual three-second answer because a reader should not need a conversation to discover the next action.

### 8 · Activity, count what changed, and where
**Two questions, two blocks**: when the work happened, and where it went.

```text
📈 ACTIVITY · renders BELOW the page cards
   ⏱ WHEN     14 days   ▁▁▁▂▇▄▅▅
                ▉ outer bar = every board
                ▏inner bar = this board
   📍 WHERE    🗂 Board ▸ 📁 Group ▸ 📄 Page, one count each
──────────────────────────────────────────────────────────
🧮 the unit    ONE UPDATE = one dated line in one page's ## Log
🚫 not read    ## States, which is status prose, not a change record
```
📌 Settles what the dashboard counts and where it sits, so the board's content leads and its measurement closes.

The ACTIVITY block sits below the page cards, so the board's content leads and the measurement of that content closes.
It answers two questions in that order: WHEN did the work happen, as a fourteen-day strip, and WHERE did it go, as Board → Group → Page.

#### 8.1 · The unit is one update, not one minute
(JL 260726: "I don't care about the time. What I care is about the numbers of updates.")
One update is one dated line in one page's `## Log`.
The first version of this measured focus time from the browser: visible non-idle spans, five-minute idle stops, per-day allocation at local midnight.
It was exact and it was measuring the wrong thing, because the timer could only ever see a browser and most work on these boards arrives through Claude Code or an editor.
A Log line is written by whoever did the work in whatever tool, and it already carries its own date, so counting them is a record rather than an observation.
That difference is why the switch recovered days of history the timer could not have: a timer cannot observe a session that already ended, while the Logs were there the whole time.
Nothing else is read, and in particular not `## States`, which also carries dated lines but is status prose rather than a change record; counting both would count one change twice.

#### 8.2 · What the ranking is for
(a count per page is only useful if it can be compared with its neighbours)
Board rows share one scale and the current board's Group and Page rows share a second, so a short page stays legible when another board dominates.
Indentation carries ownership and bar length carries the count, which is the same grammar the index itself uses.
The strip's outer bar is every board and the inner bar is this one, so a day answers "was the work here or elsewhere" without a second chart.

### 9 · The board's design read, and its dials
**The design read and its three dials**: what kind of surface this is, and how far each quality may be turned up.

```text
🎛 WHAT THIS SURFACE IS
   📚 an expert research control plane, for long-form reading
   🚦 fast state scanning · 🤝 durable collaboration
   🎓 calm, exact, academic
   🚫 not cinematic · 🚫 not promotional
   ⚙️ still useful with JavaScript removed

🎚 THE DIALS · proposed, not yet board law
   🎨 DESIGN_VARIANCE    3 to 4   stable hierarchy, limited asymmetry
   🌀 MOTION_INTENSITY   1 to 2   feedback and state transitions only
   📦 VISUAL_DENSITY     7 to 8   compact controls, readable prose
──────────────────────────────────────────────────────────────
⚖️ visual variation may never hide state, owner, dependency or completion
```
📌 Settles the kind of surface this is, and puts three numbered dials in front of JL to accept or revise.

Read this as an expert research control plane for long-form reading, fast state scanning, and durable collaboration.
The visual language should feel calm, exact, and academic rather than cinematic or promotional.
The interface must remain useful with JavaScript removed, and visual variation must never obscure state, ownership, dependencies, or completion.
The three dials above are a proposal for JL to settle, not current board law.

### 10 · What the current surface already gets right
**Six things already right**: what the audit found working, so no prototype spends effort on it.

```text
🎨 colour     1 blue accent for links · 🔴🟠🟢⚪ reserved for state
🌗 themes     light and dark share ONE hierarchy
📏 surface    820px reading column
🔤 voices     serif prose · sans UI chrome · mono identifiers
🌀 motion     short hover and disclosure feedback only
⚙️ no-JS      generated HTML stays readable with scripts stripped
```
📌 Records the baseline a prototype must not regress, so effort goes to the gaps in §11 instead.

- One blue accent carries links and interaction while red, amber, green, and gray keep semantic state roles.
- Light and dark palettes use the same hierarchy rather than changing visual language halfway through the page.
- The 820px reading surface, serif prose, sans UI chrome, and monospace identifiers give content and control different voices.
- Motion is currently limited to short hover and disclosure feedback rather than decorative animation.
- Generated HTML stays readable when all scripts are removed.

### 11 · Initial audit signals
**Six findings, three already closed**: what the first read of the stylesheet turned up, and what the pilot fixed.

```text
⌨️ focus      :focus-visible on 2 chat buttons only     ✅ fixed 260726
🌀 motion     no prefers-reduced-motion rule            ✅ fixed 260726
📐 radius     several unrelated numbers and full pills  ✅ 4 tokens added
🔲 surfaces   rounded frames nested many levels deep    ⚠️ still open
🔡 metadata   10.5px to 12.5px, never legibility-tested ⚠️ still open
🌈 contrast   designed by eye, no mechanical check      ⚠️ still open
──────────────────────────────────────────────────────────────
📄 a SOURCE-level first pass, not a finished visual or accessibility audit
```
📌 Names the concrete gaps the pilot in §13 had to aim at, and which three of them it closed.

The stylesheet carried a narrow `:focus-visible` rule for two chat-header buttons and nothing for links, disclosures, form fields, or the rest of the controls, so keyboard location was not a design primitive at all.
It carried no `prefers-reduced-motion` rule either, and its radius values ranged across several unrelated numbers and full pills.
The pilot in §13 closed all three: one shared focus ring, one reduced-motion fallback, and four semantic radius tokens.

Three findings are still open.
Rounded bordered surfaces appear at many nested levels: spine, context, index row, files, comparison column, chat, and comments.
The focused page and its major inner sections already remove these frames, which preserves the unframed reading intent `QB4` owns; the index and all-page views still need a visual comparison before any further surface reduction is justified.
Metadata commonly falls between 10.5px and 12.5px, and that density is intentional, but keyboard labels, state text, and secondary controls have never been legibility-tested.
Colour contrast is designed by eye and has not been recorded as a mechanical acceptance check.

This is a source-level first pass, not a completed visual or accessibility audit.

### 12 · Rules worth borrowing, and rules that do not fit
**One outside skill, split in two**: which of its rules may enter the board audit, and which stay out.

```text
🌍 taste-skill, an outside skill written for marketing pages
      │
      ├─ ✅ BORROW · the DISCIPLINE
      │     🔍 audit before editing · 🎨 one small vocabulary
      │     🧪 check every state · 👁 compare a real before and after
      │
      └─ ❌ REJECT · the MARKETING DEFAULTS
            🎬 hero + CTA · 🌀 cinematic motion · 🎚 8/6/4 dials
            📦 new dependencies · 🕳 hidden JS to read the page
──────────────────────────────────────────────────────────────
⚖️ it says of itself that it is NOT for dashboards or data tables
```
📌 Splits an outside skill into the part this board adopts and the part it permanently refuses, with the reason on each side.

Worth borrowing:
- Infer the page kind, audience, and constraints before changing visual style.
- Audit before editing and preserve existing interaction behavior.
- Use a small, explicit type, color, spacing, and radius vocabulary.
- Treat cards, borders, shadows, and motion as semantic devices rather than decoration.
- Check contrast, focus visibility, reduced motion, responsive behavior, and all interaction states before shipping.
- Compare a real before and after instead of accepting a persuasive design description.

Does not fit this board:
- No AIDA page structure, hero section, pricing CTA, image-first composition, or marketing-page storytelling.
- No mandatory GSAP, scroll pinning, cinematic motion, or randomized layout selection.
- No default `8 / 6 / 4` dial settings.
- No blanket emoji ban, because board icons carry authored information and are already governed by the page grammar.
- No new font, framework, icon, motion, or design-system dependency merely to satisfy an aesthetic preference.
- No change that makes hidden JavaScript necessary for reading the complete board.

The default external skill explicitly says it is not for dashboards, data tables, or multi-step product UI, so its rules can inform this audit but cannot govern it unchanged.
The redesign variant is the closer model because it begins with scan, diagnose, and targeted fixes.

[taste-skill repository](https://github.com/Leonxlnx/taste-skill)
[default v2 skill](https://github.com/Leonxlnx/taste-skill/blob/main/skills/taste-skill/SKILL.md)
[redesign skill](https://github.com/Leonxlnx/taste-skill/blob/main/skills/redesign-skill/SKILL.md)

### 13 · The pilot, and what it verified
**The pilot, start to finish**: what was captured, what was changed, and what the check found.

```text
📸 CAPTURE   index · one dense page · chat drawer · 390px · dark mode
      ▼
🧪 CHANGE    at most three, CSS only
             ⌨️ one shared high-contrast :focus-visible ring
             📐 4 radius tokens: inline · control · surface · pill
             🌀 a prefers-reduced-motion fallback
      ▼
👁 VERIFY    ✅ desktop width 1440/1440 · ✅ 390px, no page h-scroll
             ✅ 3px focus ring at rgb(7,95,189), 3px offset
             ✅ motion cut to 0.01ms · ✅ 7 boards rebuilt, JS-strippable
      ▼
🎯 KEEP IT   only if state scans faster AND every old boundary still reads
──────────────────────────────────────────────────────────────────
⚠️ still owed   chat and comment interaction states
```
📌 Records the protocol the pilot ran and the measurements it produced, so a later change can be held to the same bar.

Run the first pilot on this board itself.
Capture the index, one dense Q page, the chat drawer, mobile width, and dark mode before changing CSS.
Prototype no more than three changes in one pass: visible keyboard focus, a semantic radius vocabulary, and a reduced-motion fallback.
Do not change content structure or interaction behavior during the visual comparison.
Keep a change only if a fresh reader scans state faster, reads the page comfortably, and can still identify every boundary the old styling communicated.

Verified 260726:
- Desktop computed width remained `1440 / 1440`, and the focused page kept `border: none`, `border-radius: 0`, and a transparent background.
- At `390px`, document and body scroll width both remained `390px`; only preformatted diagrams were wider, and they retain their intentional local horizontal scroll.
- One Tab from the page start landed on the Topic disclosure, which the Index still carried that day, with a solid `3px` focus ring, `3px` offset, and the dedicated light-mode focus colour `rgb(7, 95, 189)`.
- Emulated reduced motion matched successfully and cut both transition and animation duration to `0.01ms`.
- Light, dark, focused-page, index, and mobile screenshots rendered without visible regression.
- All seven active boards rebuilt successfully, and every build reported that its body survives with JavaScript stripped.

The broader baseline audit remains open because chat and comment interaction states have not yet received the same full visual comparison.

### 14 · After a page opens
**Where this page stops**: the rung it owns, and the page that owns the next one down.

```text
🗂 INDEX          ⬅ QB2 · this page
   🖱 click a row
      ▼
📄 PAGE           ⬅ QB4 · the page template
   🧭 Opening · 🖼 Diagram · 📚 Content
   🎯 Aims · 📍 States · 📎 Files
      ▼
✏️ SENTENCE       ⬅ QB8 · comments, edits, evidence cards
──────────────────────────────────────────────────────
⚖️ one principle, three owners; none of them restates another
```
📌 Draws the ownership line, so a rule about an opened page is never written twice.

This page stops at the Index and at the surface every view shares.
`QB4` owns the opened Q or S page: the order its sections keep, and what each one owes a reader.
Its seven per-section faces were folded into it on 260802, so there is one page to read instead of eight, and the older `QAa1` to `QAa6` ids still resolve through `board.md`'s `## Links`.
`QB8` carries the same ladder on into the section and the sentence.
The specifications use the same principle without mixing their responsibilities.

### 15 · Board Map, see relationships before scanning rows
**The map above the list**: what the canvas answers that a list of rows cannot.

```text
🗺 BOARD MAP · below progress, above the page rows

   ┌── QB1 ──┐   owns    ┌── QB4 ──┐
   │ folder  │ ────────▶ │ page    │
   └─────────┘           └────┬────┘
                           owns
                         ┌────▼────┐
                         │  QB8    │
                         └─────────┘

   🖊 an arrow = a relationship someone DREW and LABELLED
   🚫 boxes drawn near each other mean nothing
   🚫 the order of ## Pages means nothing
──────────────────────────────────────────────────────
📄 the text list stays underneath: searchable and action-oriented
❓ arrow vocabulary and click-to-open are UNRULED
```
📌 Settles that the map answers "how do these pages relate?", a different first question from the list's "which one do I open?".

The Board-Webpage-Index shows the Board Map directly below progress and above the text folds and page rows.
Each box is one actual Q or S page, so the map is a picture of those pages and never a second page registry.
An arrow means a relationship someone deliberately drew and labelled, for example *defines*, *governs*, *requires*, or *ships*.
Boxes that happen to sit near each other, and the order of `## Pages`, mean nothing by themselves.

Three sources were possible and one wins.
A board that declares a `## Board Map` section holding one figure uses that figure, and it beats both canvas sources (260730).
The reason is reach: a figure draws on a static host with no Excalidraw endpoint, it survives with scripts off, and since haipipe-board 0.53.0 every page id inside a figure is a real link, so a figure is the only map a reader can travel on.
A board with no `## Board Map` keeps the older behaviour: the local `board.excalidraw` scene when served through the live Board server, or a declared shared `board-map:` URL on a static host.
The text list stays underneath the map either way, because the list is the accessible, searchable, action-oriented entry point while the map answers a different first question, "how do these pages relate?".

This first surface deliberately does not infer arrows from `## Pages` or `## Pipeline`, and it does not make a box click open a page.
Both would need a settled relationship grammar and a settled interaction contract rather than a visual guess.

### 16 · Related Folders, open a related folder from the Index
**The third Index fold**: which folders it opens, and how far a click goes.

```text
🗂 RELATED FOLDERS · peer to 🗺 Board Map and 🩺 Section Matrix

   📁 skills/board/haipipe-board/   the engine that ships the board
        SKILL.md · src/ · assets/ · ref/
   📁 BoardSkillBoard-260722/       what a board folder looks like
        board.md · group folders · board.excalidraw · fig/ · board.html

   🖱 click a folder ▸ 🖱 click a file ▸ 📖 its content, inline
──────────────────────────────────────────────────────────────
🏗 built at BUILD time, so it opens with scripts stripped and on a static host
✍️ authored, never inferred: QA0 and board.md ## Links decide the list
```
📌 Settles that the Index can show the folders around the board, not only the pages inside it.

A third Index fold, peer to the Board Map and the Section Matrix, lists the folders this board TOUCHES rather than the pages it contains, so a reader can see the engine that ships the board and what a board folder itself looks like without leaving the Index.
It surfaces `QA0`'s three-folder argument as a working panel: the skill family that renders the board (`skills/board/haipipe-board/`, with `SKILL.md src/ assets/ ref/`), this board's own folder (`BoardSkillBoard-260722/`, with `board.md`, its group folders, `board.excalidraw`, `fig/`, and the generated `board.html`), and the sibling boards the same engine renders.
Two depths were possible: a static folder tree that only shows structure, or a browser whose folders open to reveal a file's content such as `SKILL.md`.
JL ruled the browser on 260731, and it shipped in haipipe-board 0.87.0 as a build-time embed rather than a live fetch, so the fold still opens with scripts stripped and on a static host.
The panel is authored, not inferred: which folders count as related and what each contains comes from `QA0` and `board.md`'s `## Links`, never from guessing.

## Aims
### A1 · 🗂 Board-Webpage-Index and Board-Webpage-Page
- A1.1 · Every component of the Index says what a reader eventually gets from it.
  **Done when:** Content names the reader outcome for orientation, progress, groups, page rows, ordering, structure controls, chat, activity, the map, and related folders, and the opened page's sections stay with `QB4`.
- A1.2 · The Index answers three questions with no click: what is this board doing, how far along is it, and which page do I act on now.
  **Done when:** All three are answerable from the Index alone, and the third is answered by looking rather than by reading every row.

### A3 · 📖 Group, explain why these pages belong together
- A3.1 · Each group introduces itself on the Index.
  **Done when:** Every group header carries one always-visible sentence, clicking it opens the longer "what this group is for" body, and the whole thing survives with scripts stripped.

### A4 · 📄 Page row, identify the next action
- A4.1 · What a row shows is settled, so nothing is on it by habit.
  **Done when:** JL has ruled the six signals in `### 4` in or out, and the row carries exactly what survived.
- A4.2 · Completion colouring cannot be misread.
  **Done when:** A parked page no longer renders the same full green as a finished one, and a cold reader tested on the Index never calls a parked page done.

### A5 · 🔢 Ordering, make priority legible
- A5.1 · Lifecycle grouping is settled and ordinary-board sorting stays explicitly open.
  **Done when:** Paper boards group by the seven named S families with each blocking Q after its S page, ordinary boards keep hand-written `## Pages` order, and any automatic sort that arrives is explainable and never rewrites the source.

### A6 · 🧱 Structure controls, edit without hiding the source
- A6.1 · Groups and pages can be added and archived from the page without the markdown stopping being the source of truth.
  **Done when:** One writer handles every op, a full add-to-archive round trip leaves `board.md` byte-identical, and nothing is ever deleted.

### A8 · 📈 Activity, count what changed, and where
- A8.1 · The dashboard answers WHEN and WHERE as two separate blocks, and closes the Index rather than opening it.
  **Done when:** A fourteen-day strip sits above a Board to Group to Page tree, both render after the page cards, and neither tries to be one clever chart.
- A8.2 · The unit is one update, counted from `## Log`, so every tool is read and no change is counted twice.
  **Done when:** Only dated `## Log` lines are counted, work done outside the browser appears, and days before the dashboard existed are counted too.
- A8.3 · The browser-span recorder has a ruled fate rather than running unread.
  **Done when:** JL has ruled delete, keep silently, or show as a secondary readout, and the code matches the ruling.

### A9 · 🎨 The board's design read, and its dials
- A9.1 · The design read and its three dials are set by JL rather than proposed by CC.
  **Done when:** JL has accepted or revised `3 to 4 / 1 to 2 / 7 to 8`, and the settled numbers are what any later prototype is measured against.

### A11 · 🔍 Initial audit signals
- A11.1 · The baseline audit covers every surface, not only the stylesheet source.
  **Done when:** Index, focused page, chat, comments, mobile width, dark mode, keyboard flow, and the script-stripped page each have screenshots and concrete findings.

### A12 · 📋 Rules worth borrowing, and rules that do not fit
- A12.1 · The borrow and reject lists are frozen rather than reopened per change.
  **Done when:** JL has ruled which outside taste rules may enter a board audit and which stay permanently out of scope.
- A12.2 · Every rule this page tries either graduates or is recorded as rejected.
  **Done when:** Adopted display rules live in `ref/board-form.md`, mechanical checks live in `QA9`, and every rejected rule keeps its reason on this page.

### A13 · 🧪 The pilot, and what it verified
- A13.1 · At most three reversible visual changes are prototyped and verified before anything is kept.
  **Done when:** The changes are CSS only, and desktop, 390px, keyboard flow, reduced motion, dark mode, and the script-stripped build are all re-measured after them.
- A13.2 · A fresh reader, not the author, decides whether the pilot helped.
  **Done when:** One fresh reader locates the next open item and explains one dense page before and after, and what improved and what regressed is written down.

### A15 · 🗺 Board Map, see relationships before scanning rows
- A15.1 · The Index shows page relationships before the page rows.
  **Done when:** The declared map renders below progress and above the rows, every box is one real page, and no arrow is inferred from `## Pages` order.
- A15.2 · The map's arrow vocabulary and click behaviour are settled.
  **Done when:** A small stable set of relationship labels is ruled, and whether a box opens its page is ruled with it.

### A16 · 🗂 Related Folders, open a related folder from the Index
- A16.1 · A reader can see the engine that ships the board, and what a board folder looks like, without leaving the Index.
  **Done when:** The fold lists the authored folders, a click opens a real file's content inline, and it still works with scripts stripped and on a static host.

### P · 🏁 Page-level validation
- P1 · A zero-background person points at the right page within three seconds.
  **Done when:** A fresh agent that sees only the Index, and is asked which page to act on, answers correctly.

## States
### Decision Now

- [ ] 🗣 Rule whether a group gets a SOURCE FILE, and therefore a real template
      📍 `Part` `### 3 · Group, explain why these pages belong together`
      🔔 `Why now` The group page now shows purpose, why, progress and members, all derived from `board.md`. That is the ceiling of what derivation can give: a group still cannot hold a decision, an open item, or a state of its own.
      ⭐ `A ·` a group gets its own markdown file with the page sections that make sense at group altitude (Opening, Aims, States with Decision Now), rendered as the group page, with the member list appended by the generator. CC recommends it, because a group is already the unit you click, a session attaches to, and a lane block describes, and the only thing it cannot do is close.
      `B ·` the group stays derived, and anything a group needs to decide is written on whichever member page is closest.
      `C ·` extend the `board.md` intro grammar instead, so a group can carry more without a new file.
      🛑 `Blocks` A3.1 only if a group is expected to close; nothing else stops today.
      🤖 `If nobody answers` B takes effect, which is today's behaviour.
      💰 `What A costs` `src/parse.py`'s Q pattern requires a number, so `QA-index.md` is discovered and then fails to parse; the existing named-Q form `Q-<Name>-<slug>` already parses and is the cheapest slot. Worth ruling in the same breath: if a group can close, does the board's settled count start counting groups, or stay pages only.
- [ ] 🗣 Rule whether a page group gets a PAGE of its own
      📍 `Part` `### 3 · Group, explain why these pages belong together`
      🔔 `Why now` JL 260731: "for the Q group, we might have a QXX-index.md as well, but this is for the whole group, not the single page, and we can click the Group and open that page if we want." This board demonstrates the gap: the QB group intro declares the ladder Board to Group to Page to Section to Sentence, then lists faces for Board, Page, and Sentence only, because the GROUP rung has no face.
      ⭐ `A ·` a real page per group, so a group closes, carries its own Aims and Decision Now, and takes comments like any page. CC recommends it, because everything on that list except closing is already built.
      `B ·` keep the intro and grow it, adding the missing affordances to the group heading itself without minting a page.
      `C ·` leave it as is, and let group-level decisions live on whichever member page is closest.
      🛑 `Blocks` nothing today.
      🤖 `If nobody answers` C takes effect.
      💰 `What A costs` a group owns four things today and none of them is a page: an intro, an anchor `#group-<token>`, a lane block, and a chat session. It lacks the three affordances that retired the `doc:` line in 260726: no `state:`, no item counts, and no place for a comment to land. `src/parse.py` needs a parser slot, not just a filename convention, and the tidiest fit is the existing named-Q form `Q-<Name>-<slug>`.
- [ ] 🗣 Rule whether board.html stays one file
      📍 `Part` `### 1 · Board-Webpage-Index and Board-Webpage-Page`
      🔔 `Why now` JL 260731: "for the board.html, all the things are in the same .html, will that be ok? Could we make it like each page, we have each html? will that be much quicker and smoother?" Measured on this board: 2.02 MB total, of which shared JS and CSS are 0.20 MB (10%) and page content is 1.78 MB across 53 pages, so one page averages 34 KB and a reader downloads roughly nine times what the page they opened actually needs. The MISQ lifecycle board is 3.12 MB. A full rebuild is 0.38s, so the build is not the cost; the browser parsing 2 to 3 MB on every load and on every live swap is.
      `A ·` one HTML file per page plus an index, which is what the question proposes.
      ⭐ `B ·` keep one file as the shareable artifact, and give the LIVE server a per-page fragment path so an update ships one page instead of the whole board. CC recommends it, and against A on its own merits rather than only on the law: page SWITCHING today is a pure CSS `:target` change with no network at all, so splitting into files would make the instant thing slower (a round trip plus a full document load plus re-running the scripts) to speed up the once-per-session thing, and it would destroy the chat drawer and terminal on every navigation, which is the entire point of `QD4`'s swap. B is also the only option that keeps `QE3`'s Law intact, that the static half stays one self-contained file a colleague can be handed and a projector can open offline.
      `C ·` leave it, and accept the parse cost.
      🛑 `Blocks` nothing; every option leaves the board readable today.
      🤖 `If nobody answers` C takes effect.
- [ ] 🗣 Confirm the SECTION MATRIX columns and cell vocabulary
      📍 `Part` `### 1 · Board-Webpage-Index and Board-Webpage-Page`
      🔔 `Why now` The matrix shipped in haipipe-board 0.75.0 and its columns have never been ruled, so they are one session's proposal that everyone now reads as a spec.
      ⭐ `A ·` confirm the seven columns as proposed (🧭 🖼 📚 🎯 📍 📎 🗄) with the cell codes recorded in the 260731 matrix entry below. Cheapest, and every cell is derived, so a column can still be changed or dropped later without touching any page.
      `B ·` change the column set now, before anyone learns to read it.
      🛑 `Blocks` nothing; the matrix renders under either answer.
      🤖 `If nobody answers` A takes effect.
- [ ] 🗣 Rule the matrix's default posture
      📍 `Part` `### 1 · Board-Webpage-Index and Board-Webpage-Page`
      🔔 `Why now` The matrix is shut by default today and nobody decided that; it was the safe choice while it was new.
      ⭐ `A ·` shut by default. The Index already opens with the progress bar and the Board Map, and the matrix is a diagnostic view rather than an orientation one.
      `B ·` open by default, so status is the first thing a reader sees and nobody has to know the fold exists.
      🛑 `Blocks` nothing.
      🤖 `If nobody answers` A takes effect, which is today's behaviour.
- [ ] 🗣 Rule what happens to the timing recorder
      📍 `Part` `### 8 · Activity, count what changed, and where`
      🔔 `Why now` `serve.py` still records browser spans into `.haipipe-board/activity.sqlite3` and nothing reads them any more, and six regression tests protect a number the page does not print.
      ⭐ `A ·` delete the recorder and its schema. CC recommends it, because a measurement nobody reads is a maintenance cost that looks like a feature.
      `B ·` keep it silently, for a later "who is looking at this board right now".
      `C ·` keep it and show it as a secondary readout beside the update counts.
      🛑 `Blocks` A8.3.
      🤖 `If nobody answers` B takes effect, which is today's behaviour.
- [ ] 🗣 Set the board design read and dials
      📍 `Part` `### 9 · The board's design read, and its dials`
      🔔 `Why now` Every later visual prototype is measured against these numbers, and they are currently CC's proposal rather than anyone's ruling.
      ⭐ `A ·` accept `3 to 4 / 1 to 2 / 7 to 8` for variance, motion, and density as drawn in `### 9`.
      `B ·` revise the numbers, which changes what a prototype is allowed to try before it is compared.
      🛑 `Blocks` A9.1, and through it the graduation of any display rule.
      🤖 `If nobody answers` A takes effect.
- [ ] 🗣 Rule how far an ascii figure may stop looking like a terminal
      📍 `Part` `### 9 · The board's design read, and its dials`
      🔔 `Why now` JL 260731, of `QB4`'s head figure: "very hard to read ... could you make it more modern?" Half of it was a defect and is fixed board-wide: emoji are not monospace, so figures arrived bent, and `body.pad_emoji` plus `pre .eu` now pin each emoji to `2ch`. The rest is taste, and taste on this surface is this page's call under the audit-first protocol in `### 9`.
      `A ·` leave `pre.asc` as it is. One flat grey code surface, 12.5px, no hierarchy. Cheapest, and it keeps a figure looking exactly like the text an author typed.
      ⭐ `B ·` give `pre.asc` typographic hierarchy only. The first line reads as a title, `═══` and `───` runs render as real hairlines, and the block gets a card surface instead of the code grey; still one `<pre>`, still copy-safe, one CSS rule and one build-time pass. CC recommends it, because it is the only option that answers "more modern" without spending the copy-survives property, and it is reversible in one rule.
      `C ·` render figures as real HTML. Cards or a grid, genuinely modern, and it costs the thing every figure rule on this board is built on: a drawing that survives being pasted into chat or mail, plus a new authoring syntax on 53 pages.
      🛑 `Blocks` nothing.
      🤖 `If nobody answers` B takes effect.

### A1 · 🗂 Board-Webpage-Index and Board-Webpage-Page
- ✅ A1.1 · Content now names the reader outcome for all ten Index components, and the opened page's sections stay with `QB4`.
- 🧠 A1.2 · The first two are answered today by the spine and the progress bar. The third is not: a reader still scans 57 rows, and the three-second visual answer is what `P1` tests.

### A3 · 📖 Group, explain why these pages belong together
- ✅ A3.1 · Shipped 260724. Every group on this board carries an intro, rendered as a native `<details>`, so the strip-scripts invariant holds.

### A4 · 📄 Page row, identify the next action
- 🧠 A4.1 · Waiting on JL. The row shows state, id, title, open-comment badge, owner, and completion colouring; nobody has ruled whether that is enough or too much.
- ⬜ A4.2 · Not started. ⏸️ ON HOLD still renders the same full green as ✅, which reads as "done".

### A5 · 🔢 Ordering, make priority legible
- ✅ A5.1 · Settled 260725. Paper boards use the seven named families with Display owning the evidence-presentation layer; ordinary boards keep hand-written `## Pages` order, and automatic priority sorting remains deliberately undecided.

### A6 · 🧱 Structure controls, edit without hiding the source
- ✅ A6.1 · Shipped 260724 as one writer, `POST /_board/structure`, with ops `add_group`, `add_question`, `archive_question`, and `archive_group`. A full add-to-archive round trip leaves `board.md` byte-identical, and refusal paths were verified over HTTP on 5599 and through the console on 8093.

### A8 · 📈 Activity, count what changed, and where
- ✅ A8.1 · Shipped 260726. Fourteen days across the top, Board to Group to Page beneath, both rendered after the page cards.
- ✅ A8.2 · Shipped 260726. Measured across the whole repo the same day: 509 updates, 8 boards, 129 pages, this board at 300 over 5 days. The 245 dated Log lines from 260722 to 260725 that the browser timer never saw are all counted.
- 🧠 A8.3 · Waiting on JL. The recorder still writes spans and nothing reads them.

### A9 · 🎨 The board's design read, and its dials
- 🧠 A9.1 · Waiting on JL. `3 to 4 / 1 to 2 / 7 to 8` is a proposal, not board law.

### A11 · 🔍 Initial audit signals
- 🔨 A11.1 · Partly done. Desktop, 390px, keyboard flow, reduced motion, dark mode, and the script-stripped build were all measured on 260726. Chat and comment interaction states have never had the same comparison.

### A12 · 📋 Rules worth borrowing, and rules that do not fit
- 🧠 A12.1 · Waiting on JL. The two lists are written in `### 12` and neither has been ruled in.
- ⬜ A12.2 · Not started. Nothing has graduated to `ref/board-form.md` or to `QA9` yet.

### A13 · 🧪 The pilot, and what it verified
- ✅ A13.1 · Ran 260726. One shared `:focus-visible` ring, four radius tokens, and a `prefers-reduced-motion` fallback; no markup, information architecture, or dependency changed.
- ⬜ A13.2 · Not started. No fresh reader has compared before and after.

### A15 · 🗺 Board Map, see relationships before scanning rows
- ✅ A15.1 · Shipped 260730. The map became an ASCII `## Board Map` figure rendered as a shuttable disclosure, which wins over both canvas sources because a figure draws on a static host and survives with scripts off.
- ⬜ A15.2 · Not started. The relationship labels and click behaviour are both unruled, so the map stays a reading surface and the text list stays the action navigator.

### A16 · 🗂 Related Folders, open a related folder from the Index
- ✅ A16.1 · Shipped 260731 as haipipe-board 0.87.0, depth B. Two folders and four files are embedded on this board, order Board Map, Related Folders, Section Matrix verified, and the body survives JavaScript stripping.

### P · 🏁 Page-level validation
- ⬜ P1 · Not started. Nothing has tested a cold reader against the Index.

The Index is now a place you can work and understand, not only view: every component says what it is for, the Board Map appears before the page rows, paper lifecycles use seven named S-family groups, the structure is editable from the page, and the Index carries its own chat.
What stays open is the reading design: the arrow vocabulary, automatic sorting, completion colouring, and the three-second test, plus the half of the visual baseline audit that chat and comment states still owe.
The dated implementation history below is the record of how it got here; each Aim's row above is the snapshot.

- What the Index looks like today
  Board name, spine, close condition, progress bar, the Board Map, the Related Folders fold, the Section Matrix, then the grouped list in `## Pages` order with each group led by its intro, and Activity last.

- What each row has today
  State badge · id · title · open-comment badge · owner · row tinted white to green by completion (`--fill`, percentage in `title`) · hover archive.

- Known defects
  ⏸️ ON HOLD renders as full green like ✅, so it reads as "done"; with 57 pages the list is one long strip with no visible priority; group order is entirely hand-maintained in `## Pages`.
  No external skill has been installed and no dependency has been added.

- 260731 CC · 🗂 RELATED FOLDERS shipped (0.87.0, depth B)
  A third Index fold, peer to the Board Map and Section Matrix, opens the folders this board touches (the shipping engine, and the board folder itself); clicking a folder then a file reads it inline.
  Built as a build-time EMBED rather than JL's literal "serve.py serves content live", because a live fetch breaks the script-stripped/static-host Law (QE3): `related_folders()` reads each listed file at build, refuses paths outside the repo root, inlines only `.md`/`.txt` under 120 KB, and shows every failure as a visible box. Renders in both `board.html` and the `board/` tree; the page list gained a 🗂 Related Folders row. Verified: order Board Map → Related Folders → Section Matrix, four files embedded, zero failures, body survives JS stripping. QC8's live endpoint is deferred for oversized folders.

- 260731 JL · 🗂 RELATED FOLDERS depth ruled: B, the clickable browser
  JL: "do the B level." The fold opens to a real file's content on click (for example `SKILL.md`), not just a static tree.

- 260731 JL · 🗂 A RELATED FOLDERS fold requested for the Index
  JL, with a screenshot of the Board Map and Section Matrix folds: add a third fold, "related folders", that opens the folders this board touches, so a reader can see the shipping skill and see what a board folder itself should look like.
  Recorded as Content §16, an Items row, and a Decision Now depth ruling: a fold peer to the Board Map and Section Matrix, sourced from `QA0`'s three folders and `## Links`. The depth (static tree vs clickable browser) is unruled; the render lives in `src/page_board.py`, so wiring it needs an engine change beyond a board-folder-only edit.

- 260731 JL · 🧹 Topic, Pipeline, and Board-Structure left the Index
  JL, quoting the three disclosure headings: "I want to just remove this."
  The renderer no longer emits the three `ctx` disclosures; `board.md` keeps `## Topic`, `## Pipeline`, and `## Board Structure` as source-only documentation, and nothing else read them.
  The Index now reads spine → Board Map → Section Matrix → ALL PAGES → Activity, and the page list's Index outline lists exactly those components.
- 260731 JL · 📇 The Index row unfolds in the page list
  JL: "for the left panel headings, what should be the index's section content? Please add them as well."
  The `🗂 Index` row now carries the same chevron and outline as a page row: 🗺 Board Map, 🩺 Section Matrix (with its page × column count), 📄 All Pages (with the page count), 📈 Activity, each present only when the board has it, each scrolling the Index to that component.
  It unfolds by default when the board opens, since the Index is the open "page" at load.
- 260731 JL · 🩺 The Index gained the SECTION MATRIX
  JL: "We want to have a dashboard to show the status of the board. Each row is a page, each column is a subsection. the cell might be some status."
  Shipped in haipipe-board 0.75.0 as a shut-by-default disclosure between the Board Map and ALL PAGES: one row per page, one column per section, every cell computed at build from the same parses the pages render from, so the matrix is derived and can never disagree with a page.
  The cell vocabulary: 🧭 present, 🖼 figure and canvas counts, 📚 `n÷·m🖼` divisions and how many open with their face diagram (the QB4c retrofit watched from one column), 🎯 `done/total`, 📍 `DN·k` owed Decision Now ticks or `e` dated entries, 📎 files and groups, 🗄 Log lines.
  A cell is a link: click it and the page opens scrolled to that section; amber marks incomplete, accent marks waiting-on-JL, muted marks absent.
- 260731 JL · 📑 The webpage gained a hideable pages page list
  JL: "I also think to added the page list so I can choose the pages more easier ... like the side bar, and then index, QA, QA1, QA2, etc ... and that page list can be hidden as well."
  Shipped in haipipe-board 0.61.0: a fixed left page list listing Index, then every group with its pages (state emoji, id, title), rendered server-side from the same listing as the index rows so it needs no script to exist.
  It lives outside `.wrap`, so the `:target` show/hide rules never touch it and it stays up in both the Index view and an open page; a group link re-targets `#group-…`, which also brings the Index back on stage.
  The ☰ toggle hides or shows it, the choice persists per board in localStorage, and with no saved choice it defaults open on wide screens and hidden on narrow ones; a jump on a narrow screen closes the overlay without persisting.
- 260730 JL · 🅰 The Board Map became ASCII, and a disclosure
  JL: "what is the section for board map?
  I think I might need the ASCII version.
  Please try it. and make it collapsable." `## Board Map` is now a board.md section holding one ``` figure, and it WINS over both canvases.
  The reason is reach: a figure draws on a static host with no Excalidraw endpoint and no share URL, it survives with scripts off, and since 0.53.0 every page id and group token inside a figure is a real link, so an ASCII map is the only map a reader can travel on.
  It renders as `<details class="board-map board-map-ascii" open>`, because a map you cannot shut pushes the index off the first screen.
  The whole map head is the handle; the caret rides the BOARD MAP kicker.
  This Board's `board-map:` URL was deleted when the figure replaced it, so there is one declared source again, with the shared canvas kept as a link inside the section.
  A board with no `## Board Map` keeps the old iframe behaviour unchanged.

- 260730 CC · 🗺 Board Map landed at the top of the Index
  The Index now embeds the Board's declared relationship canvas immediately after overall progress. This Board points at its shared Excalidraw canvas so the static Tailscale reader can load it; live Board servers default to the local `board.excalidraw` scene. Connections remain authored rather than inferred, because page order is navigation and is not a dependency claim.

- 260729 JL · 🔗 QC2 merged in here, and the QC group is now fully dissolved
  JL: "You should merge QC2 to QA10? about the Index-UI-Design?"
  The two faces were one subject seen twice: QC2 owned what the front page must SHOW, and QA10 owned how the whole surface must LOOK, and neither could settle its half without the other's.
  QC2's eight index components became §1 to §8 and its two item blocks came with them; the visual read, audit signals, borrow and reject lists and pilot became §9 to §13.
  The id kept at that time was `QA10`, because the QC group dissolved on 260729 and its remaining pages moved into QA.
  JL renamed it `QA2b` on 260730 when Board-Webpage became the explicit second branch of Board-Structure; `QA10` and `QC2` remain Links aliases so earlier citations resolve.

- 260726 JL · 🎨 The index rows lost their coloured left stripe
  JL asked for the red and green bars down the left of the index to go.
  Removed: `.ir`'s 4px `border-left` and the four `.ir.todo/.wip/.done/.hold` colour rules. The row keeps its 1px border and its hover accent.
  Nothing was lost, which is why it was safe: every row already opens with the state emoji, so the bar restated the state in a second language, and stacked down a 27-row index the bars read as a chart rather than as a list.
  Two neighbours were deliberately left alone: the pale green completion wash on each row is different information (percent done, not state), and the page's own left stripe on `.slide.q` is a different surface.

- 260726 CC · 🧪 Applied the first reversible UI taste pilot
  Added global keyboard focus, semantic radius tokens, and reduced-motion handling.
  Kept the existing focused-page framing because the source audit showed it already satisfies the proposed unframed reading direction.

- 260726 JL · 🧮 The dashboard changed its unit, and QE2 folded in here
  JL: "for the activity dashboard, I don't care about the time. What I care is about the numbers of updates."
  The timer was exact about the wrong quantity: it watched a browser tab, and most work on these boards is done through Claude Code, so the thing it measured was not the thing that happened.
  Counting dated `## Log` lines fixed the measure and the history in one move, because a record does not have to have been present to be read later.
  QE2 merged into QC2 in the same round on JL's call, which is right on ownership grounds: the dashboard is a component of the index, and this face already owns what every index component is for.
  The parked half is honest rather than hidden: the span recorder still runs and nothing reads it, and its fate is the open item above.

- 260725 JL · 🖼 Display became an independent family
  Display now owns the claim-to-display map, accepted assets, captions, statistical labels, and Main/Appendix placement.
  Pipeline still places it after Narrative; Pages order remains navigation.

- 260725 JL · 🌱 Full-name paper lifecycle families
  The paper lifecycle now reads Seed, Work, Venue, Display, Main, Appendix, Submission.
  Seed contains S Seed and S Literature; every Main section and Appendix unit is its own page; reconcile, compile, review, and submit are explicit terminal pages.
  Temporary SM/SA abbreviations retired.

- 260725 JL · 🔄 Submission is a repeatable round
  Submission keeps four stable pages.
  External review reopens affected Work, Display, Main, or Appendix pages, then the paper runs the same reconcile, compile, review, submit sequence again.

- 260725 JL · 🧭 Stage-first exposed the family model
  The MISQ paper first exposed the weakness of broad QA/QB/QC buckets and moved to one group per stage.
  That intermediate form made the stable families visible; the current rule above supersedes it with seven full-name groups and one concrete page per S row.

- 260725 JL · 📚 Index anatomy made explicit
  JL asked for Content to explain what each webpage section is for.
  This face now defines its own index components and points to QAa0 for the opened Q/S page, keeping the ownership boundary visible.

- 260725 CC · 🤖 A chatbot on the index (JL's ask)
  The bottom-right button now shows on the index too, labeled "🤖 Board chat".
  It opens the same `QD2` drawer (and the ⌨ inside it is the same `QD3` terminal), just attached to `board.md` instead of one question, so "how should we work / which question next" can be discussed right on the index.
  The three-second VISUAL answer this question owes is still owed: a chat answer takes longer than three seconds.

- 260724 CC · 🧱 Structure became editable from the front page
  Per JL's ask: ＋Q on every group header, ＋Group at the list's end, hover-🗄 archive on rows and headers, all two-click confirmed, no native dialogs.
  The buttons are writers only: board.md's `## Pages` plus the Q files stay the single source of truth, `_archive/` keeps everything recoverable, and the live watcher (QD4) swaps the updated index in under you after each op.

- 260724 CC · 📖 Group intros landed with a new Pages grammar
  Intro lines sit directly under each `### ` heading in `## Pages`; the per-group paragraphs that used to live in `## Pipeline` moved there (Pipeline keeps only the overall narrative), so nothing is said twice.

- 260731 JL · 🎨 The Board Map header now matches the Section Matrix header
  JL: "could you make this cleaner? this is so ugly", then "make these two styles consistent", with a screenshot of the two sitting one above the other and looking nothing alike.
  The map's header was a two-column flex with a large title on the left and its blurb stranded right-aligned on the right, wrapping onto two lines; the matrix's was one compact line.
  The map now uses the matrix's shape exactly: one line, one triangle, same padding, weight and size, with the blurb dropped from the header because the body already opens with the same sentence.
  Two triangles were being drawn, and finding the second one took the browser rather than the source.
  The first was the `<summary>` disclosure marker, which `list-style:none` does NOT remove because a summary is `display:list-item` and Chrome draws it through `::marker`; only leaving list-item behind kills it.
  The second was a real `::before`, and the rule meant to suppress it had the SAME specificity as the generic `details[open]>summary::before` further down the file, so the generic one won on order alone.
  Both are now beaten explicitly, and the triangle that remains is one inline arrow on the header itself.

- 260731 JL · 🔁 The tree index was a THIRD reimplementation, and JL caught it by comparing
  JL: "the ASCII here has not become real ASCII", and "compare your configuration with the original .md one, there are big differences, look carefully."
  He was right on both counts and the cause was one thing: the tree's index and page list had been hand-written instead of reusing the builders `render()` already had.
  What that silently dropped: every `.gi` group-intro block, every `.gib` body, and all six `.gidia` figures, which are the per-group lane diagrams, so the ASCII was not rendering as ASCII because it was not being rendered at all.
  The page list lost its per-page section outline the same way, 54 `.sb-out` blocks and 298 `.sb-s` rows.
  Fixed structurally rather than patched: the index loop became `index_rows()` and the page list loop became `sidebar_rows()`, each taking an href function, and both packagings now call the same one.
  A class-by-class diff of the two indexes is the check: the only remaining differences are the progress bar and the ALL PAGES hint, both deliberate, and one page list row, because the tree's Index is its own document rather than a fragment.
  Third time this family's "one grammar, never two implementations" law has caught its author in one day, which is itself the argument for the law.

- 260731 JL · 🗂 A group is the one altitude with no template, and now it has half of one
  JL: "index has a template, page has a template, should the page GROUP have a template too? Opening a group shows only a list; can it also say what this group is for?"
  He is right, and this board states the gap against itself: the QB group intro declares the ladder Board to Group to Page to Section to Sentence, then lists faces for Board, Page and Sentence only.
  What a group owns today is thin and scattered: an intro in `board.md` under its `### ` heading, an anchor, a lane block, and since 0.77.0 a chat session. None of that is a template and none of it has state.
  Shipped now, from data that already existed: the group page renders its intro as a PURPOSE line, the remaining intro lines as a "why this group exists" drawer, and the group's own settled count. The intro was in `board.md` all along and the group page simply never read it.
  Not shipped, because it needs a source file and a parser slot rather than a render change: a group with its own `## Items to Finish`, its own `### Decision Now`, and a `state:` that can close.

## Files
### ⚙️ Engines · what RUNS the Index
- `src/page_board.py`
  The Index itself: `index_rows()` and `sidebar_rows()` with `frac_done`, the Board Map panel, `related_folders()` for the Related Folders fold, the Section Matrix, and the static ACTIVITY shell emitted after the page cards.
  Runtime activity data stays an enhancement, so with no server the section reads as a sentence and the board is still complete.
  Changing what the Index SHOWS starts here.
- `cli/build.py`
  The build entry: it writes `board.html` and the `board/` tree from the `src/` renderers.
  The index pass it once held moved out in the src split: the row render to `src/page_board.py`, the `## Pages` intro parse (`gintro`) to `src/parse.py`, and the `.ir` row styles to the `assets/css/` set.
- `cli/serve.py`
  The endpoint host: `POST /_board/structure` and `POST /_board/activity` land here, and the live-layer split (`QC2c`) moved the code itself into `live/`.
- `live/structure.py`
  `structure_op()`, the one writer for add_group, add_question, archive_question and archive_group behind `POST /_board/structure`, imported by `cli/serve.py` and the console and never reimplemented.
- `live/activity.py`
  `log_counts`, `log_boards` and `activity_stats`, the update counter: `log_counts` reads only `## Log` and caches on file mtime, and `activity_stats` joins it to `## Pages` for group ownership.
- `assets/js/10-drawer/50-structure.js`
  The page-side controls: ＋Q, ＋Group, 🗄 with its two-click confirm, and the inline mini form, wired into `__boardRewire` so they survive a live swap.
- `assets/js/50-activity.js`
  The ACTIVITY render: `sampleData`, `rowHtml`, `render`, and the `.act-*` styles.
- `assets/css/10-focus.css`
  The responsive Board Map surface and the group-intro styling. The map stays on the Index only; a focused page hides it with the rest of the index.
  The stylesheet set also holds the palette, typography, density, surfaces, interaction feedback, dark mode, and responsive rules that `### 11` audits.

### 📥 Input files · what the render READS
- `board.md`
  `## Pages` decides grouping, order, AND each group's intro: plain lines under the `### ` heading, line 1 being the visible sentence.
  `## Related Folders` decides which folders the Index fold opens. If sorting ever becomes automatic, `## Pages`'s role must be redefined too.
- `board.excalidraw`
  The one canonical scene: its generated frames are pages, while authors draw and label the relationships between them. It is not a separate page registry.

### 📋 Contracts · what CARRIES a rule to other pages
- `ref/board-form.md`
  Where a settled display rule graduates, and only after the pilot and a human ruling.
- `QPs-page-structure/QPs1-overall/QPs1-overall.md`
  Owns the opened page: its section order, the unframed reading intent this audit must preserve, and automatic icon assignment. This page does not reopen the semantic role of authored icons.

### 🧪 Checks · what CATCHES a page breaking a rule
- `QF-execute/QF1-acceptance/QF1-acceptance.md`
  Owns the repeatable post-change checks a visual rule graduates into once it becomes mechanical.
- `tests/test_activity.py`
  Six regression tests protecting the browser-span recorder, which nothing displays any more. They go or stay with the Decision Now ruling on the recorder.

### 📤 Output files · what a BUILD writes
- `board/QB/QB2-board-webpage-design.html`
  ⚠️ Generated by `cli/build.py`. Never hand-edit.
- `.haipipe-board/activity.sqlite3`
  ⚠️ Written by `cli/serve.py`, gitignored, and currently read by nothing.

## Discussion
> JL: QC2 Index page design 我们在这个地方需要能够添加和删除板块，也就是说，既能添加和删除 question group，也能添加和删除 question item。 另外，在 question group 之间，也需要有一个非常短的句子来介绍一下这个 group。我想的是这样的：比如你有一个 question group（像 QC、QA 这种），下面配一个简单的介绍（sentence）。当我们点击它的时候，它就会向下展开，弹出一个下拉的介绍。 这个介绍主要用来解释这个 group 是干嘛的，以及我们为什么要在这里使用它。大概就是这样的一个意思。
>> CC0724: both shipped. (1) Group intros: every group header now carries one always-visible sentence; click the ▸ and it drops open into the longer "what this group is for, why it is here" body. It lives in board.md's ## Pages as plain lines under the ### heading (first line = the sentence, the rest = the dropdown), rendered as a native details element, so it survives script-stripping and stays hand-editable. (2) Add/delete: ＋Q on each group header, ＋Group at the end of the list, and a hover 🗄 on every row and header. All of them only write the md through one endpoint (/_board/structure in serve.py, relayed by the console); "delete" is an archive that moves the file into _archive/, so nothing is ever lost. Try it on this page: hover a group header.
> JL: I think QE2 can merge to the QC2 Index page design. And for the activity dashboard, I don't care about the time. What I care is about the numbers of updates. (260726)
>> CC0726: both done, and the second one is the bigger of the two. The timer was measuring a browser, and most work here arrives through Claude Code, so it was precise about a quantity that was not the work. One update = one dated `## Log` line reads every tool and reads backwards, which is why the four days the timer missed came back. What is left over is the recorder itself, still writing spans nobody reads; the open item above asks you to kill it or keep it.
> JL: could we have the chatbot in the index page, so we can discuss how to work in the index page. (260725)
>> CC0725: built. The bottom-right 🤖 button now shows on the index as "🤖 Board chat"; it opens the same QD2 drawer (and QD3 terminal via ⌨), attached to board.md, primed with the index's own view: spine, close condition, every page's state and open comments. It has a canned 🧭 "Which question should I act on?" button, and its 🔧 button works comments board-wide. Implementation details are recorded on QD2; this page only owns the entry point.
> JL: Content should explain, section by section, what each part of the Q webpage is eventually for: Opening, Diagram, and so on. (260725)
>> CC0725: agreed on the principle and kept the ownership clean. The index face explains the index's own components; QA4 (now QAa0 and the QAa faces) explains the parts of an opened Q/S page and is linked from the final Content subsection.
> JL: how do we make this match the paper stages? (260725)
>> CC0725: this first became stage-first, then the paper exposed a clearer stable abstraction:
>> seven full-name S families. Seed, Work, Venue, Display, Main, Appendix, and Submission are now the groups;
>> each concrete S page is a row, and its blocking Q sits directly after it.
> JL: Display should be its own group because it is important. (260725)
>> CC0725: implemented as S Display 0. It is a separate progress family and remains between Narrative and the Main/Appendix consumers in Pipeline.
> JL: Could we try taste-skill, or add a Board Q about UI design?
>> CC0726: Add the Q first and make the trial bounded. The external default is a marketing-page skill, so the board should borrow its audit discipline rather than its visual defaults.
> JL: You should merge QC2 to QA10? about the Index-UI-Design? (260729)
>> CC0729: merged, and it closes the QC dissolution that started the same day. What the front page must SHOW and how the surface must LOOK were being decided on two faces that each needed the other's answer; the three-second test is a visual claim and the visual dials only matter because a dense index has to be scannable.
> JL: 🦴 Topic — what this board is about 🔄 Pipeline — how these Qs are ordered 🧭 Board-Structure — Board-Folder and Board-Webpage I want to remove them,just keep the Map is ok.

## Law
- 🗂 **Related Folders opens a real file**: the Index fold is a clickable browser, not a static tree (JL 260731).
  JL asked for a third Index fold, beside the Board Map and Section Matrix, that opens the folders this board touches: the shipping skill engine, and what a board folder should look like.
  He ruled depth B, the clickable browser, over A, a static folder tree that only shows structure, and over C, recording the design and shipping neither depth.
  It shipped in haipipe-board 0.87.0 as a build-time EMBED rather than the live fetch B first proposed: `related_folders()` in `src/page_board.py` reads each named file at build and inlines it, so the fold still opens with scripts stripped and on a static host, which `QE3`'s Law requires. This page owns the fold and its render; `QA0` owns which folders are related and which files each opens; a live `serve.py` endpoint (`QC8`) is deferred and is needed only for folders too big to inline, above 120 KB.
- 🗂 **Index stays as it is**: the Index does not roll up open `Decision Now` rows; a reader goes to a page's States to find them (JL 260802).
  Chosen over a roll-up block on the Index and over a per-page 🗣 badge in the page list.
  The rows already live where they are owned, and a second surface listing them is a second thing that can disagree with the first. The cost is real and accepted: finding what is waiting means opening pages.

## Log
- 260806 2058 · [REVISE-CC] swept to the 260806 architecture; Files re-pointed to the src/ and live/ splits (index pass → src/page_board.py + src/parse.py, structure_op → live/structure.py, update counter → live/activity.py, ＋Q controls → assets/js/10-drawer/50-structure.js, ACTIVITY render → assets/js/50-activity.js), page count 55 → 57 with 52 waiting on nobody, and the garbled "page list page list" restored to the pages sidebar
260802 1600 · Brought up to the QB4 page contract. Title now states the page's purpose; the Opening was rewritten to the blank-line split with a visible paragraph under 450 chars and a labelled `More details`; `## Boundary` was deleted on JL's 260731 ruling and its pointers moved into the Opening drawer; all 16 Content parts gained a face figure and a caption, and §8's two paragraphs were numbered 8.1 and 8.2; `## Items to Finish` became `## Aims` with 20 Aims in 13 Content-linked groups plus P1, and `## Where we are` became `## States` with Decision Now first and one state row per Aim; `## Files` was regrouped by ACTION and three dead or duplicated rows were repaired (`QA9-acceptance.md` → `QF-execute/QF1-acceptance/QF1-acceptance.md`); the RELATED FOLDERS depth ruling left Decision Now for `## Law`, per QB4 §5.2.7; the excalidraw anchor moved off the non-existent `QA10` frame to `QA2b`; stale text corrected in §11 (three audit findings the pilot had already closed), §14 (the QAa faces were folded into QB4 on 260802), and §16 (the depth was ruled and shipped)
260802 1150 · JL ruled option C on the Index roll-up, the same day it was raised: the Index stays as it is and a reader goes to States to find an open row. Recorded in Law and removed from Decision Now, per QB4 §5.2.7, which says an answered decision leaves States entirely rather than moving down the page
260802 1130 · An Index roll-up of every open `Decision Now` row was proposed and recorded here rather than left in a chat session (JL 260802: "don't put the decision in the claude code session"). It came out of JL asking whether a human could check Decision Now and nothing else: it is the only thing that requires them, but finding the rows today means opening 53 pages to learn that 51 have nothing waiting
260731 1945 · RELATED FOLDERS shipped as haipipe-board 0.87.0: build-time-embed fold (related_folders() in src/page_board.py + `## Related Folders` grammar in parse.py + board.md + board.css), rendering in board.html and the board/ tree; 2 folders / 4 files embedded, order Board Map → Related Folders → Section Matrix verified, body survives JS strip; QC8 live endpoint deferred. Also fixed the Board Map header typo "placement is not one." → "placement is not."
260731 1930 · RELATED FOLDERS depth ruled B (clickable browser) on JL's "do the B level"; split across QB2 (fold + page_board.py render), QA0 (folder list + contents), QC8 (serve.py content endpoint)
260731 1905 · RELATED FOLDERS Index fold requested (JL): a third fold beside the Board Map and Section Matrix, opening the folders this board touches (the shipping engine + what a board folder looks like), sourced from QA0 + ## Links; recorded as Content §16, an Items row, and a Decision Now depth ruling (static tree vs clickable browser). Renderer is src/page_board.py, so wiring needs an engine change
260731 · index_rows() and sidebar_rows() extracted so the tree and the single file share one implementation; restored the 6 group-intro ascii figures and the page list's 54 section outlines the hand-written version had dropped (haipipe-board 0.84.0)
260731 · Board Map header restyled to match the Section Matrix (one line, one triangle); two stray disclosure triangles removed, one a list-item marker and one a specificity tie (haipipe-board 0.82.0)
260731 · Two JL questions opened as Decision Now rows: a page of its own for each group (the QB ladder's Group rung has no face), and whether board.html stays one file (2.02 MB, 10% shared, 34 KB per page, 0.38s build)
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260731 · Topic, Pipeline, and Board-Structure removed from the rendered Index on JL's ruling; board.md keeps the sections as source-only documentation (0.78.0)
260731 · The Index row unfolds in the page list on JL's ask: Board Map, Section Matrix, All Pages, Activity, present-only, each scrolling the Index to its component (0.78.0)
260731 · Shipped the SECTION MATRIX on JL's dashboard ask: one row per page, one column per section, cells computed at build and linking into their section; columns and default posture wait in Decision Now (0.75.0)
260731 · Shipped the hideable pages page list (Index → group → page) on JL's ask; server-rendered page list, ☰ toggle, per-board persistence, active-row highlight
260730 · Board Map became an ASCII `## Board Map` figure rendered as a shuttable disclosure, winning over both canvas sources
260730 · Rewrote `board.md ## Board Structure` around the reader's three views: Board-Folder is the source, Board-Webpage-Index is the orientation view with the Board Map, and Board-Webpage-Page is the focused Q/S view; the map is inside the Index, not a third peer object
260730 · Added the Board Map to the Board-Webpage-Index: the top view now embeds the declared shared Excalidraw canvas below progress for static Tailscale readers; arrows stay authored rather than inferred from page order
260730 · Renamed from QA10 to QA2b, "Board-Webpage Design", on JL's terminology. Defined Board-Webpage-Index versus Board-Webpage-Page; the former QA0 map moved into board.md's Board-Structure block after Pipeline and no longer renders as a Q webpage
260729 · QC2 (Index page design) merged in on JL's call, completing the 260729 dissolution of the QC group. Its eight index components became §1 to §8 and its item blocks came with them; the former QA10 visual-taste content became §9 to §13; title changed from "Visual taste without drift" to "Index page and visual design". QC2 retired to `_archive/` with a `## Links` row, so the eight pages citing it still resolve
260726 · Applied the first reversible UI taste pilot: shared `:focus-visible` ring, four radius tokens, `prefers-reduced-motion` fallback; verified at desktop and 390px, light and dark, keyboard flow, and with scripts stripped
260726 · Index rows lost their coloured left stripe on JL's call; the state emoji already carried that information and the bars read as a chart down a long index
260726 2300 · QE2 absorbed (JL: "I think it can merge to the QC2 Index page design"): `§8 Activity` added, QE2's finish lines folded in, QD8-activity-timing.md deleted and delisted from board.md. The dashboard's unit changed from focus seconds to UPDATES counted from `## Log` (JL: "I don't care about the time"), which recovered 260722-260725 that the timer never saw: 509 updates · 8 boards · 129 pages, this board 300 over 5 days. Span recorder still runs and is now unread; its fate is an open item
260726 · Opened a scoped visual-taste decision: borrow the external project's audit-first and anti-default discipline, reject its marketing-page structure, high-motion defaults, and dependency assumptions
260725 · Display separated from Work into its own family; lifecycle index now has seven S groups
260725 · Family order clarified as navigation, Pipeline as execution; Submission pages now repeat across revision rounds
260725 · Full-name S families replaced temporary S/SM/SA grouping: Seed (including Literature), Work, Venue, Main, Appendix, Submission
260725 · Lifecycle board grouping settled: stage-order groups, canonical S first, owned Q decisions after; MISQ board reorganized to match
260725 · Content now defines the index components and explicitly hands the opened Q/S page to QA4; QA4 received the parallel section-purpose map
260725 1040 · 🤖 Board chat entry landed on the index (JL's ask; it is the QD2 drawer / QD3 terminal opened on board.md, details on QD2): fab shows on the index, label switches, follow() returns to the board session
260724 1553 · JL's two asks shipped: Pages-intro grammar + details.gi render (build.py), structure_op writer + /_board/structure (serve.py, imported by boards_api), page controls ＋Q/＋Group/🗄 (board.js/css); board.md's five groups got intros, Pipeline slimmed to the narrative; round trip byte-identical, refusals verified on 5599 + 8093; 🔴 → 🟡
260724 1242 · Translated to English (JL 260724: everything on the board in English)
260723 · Opened: the QC group refocused from "needs JL's decision" to "index and structure"; the front page becomes its own question (`QA4` owns only the single-question page; the index page had no owner)
