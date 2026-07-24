# Single Question Webpage Layout
state: 🟡 PARTIAL
owner: CC
method: intent first (what is asked · boundary · what counts as done), status second — a zero-background reader gets it in one pass
session: cd5e7f5f-15c7-49ba-a97f-bdf90ef3f534

## Question
When one question is opened and it alone fills the screen, how should that page be arranged so that someone with **no background at all** can read top to bottom once and know: what is being asked, what counts as done, and where things stand now?

- Why this is hard, and what it touches
  The difficulty is that one page has to carry two different things at once: what is being decided, and how far along it is. The order turns out to matter more than the wording. Lead with implementation detail and the reader drowns before ever learning what the question is, while the same sentences, reordered, read like a different document. This matters because the board is not written for us. It exists to be discussed with other people and handed to an RA, so a page the second person cannot follow is worth nothing no matter how much is on it. If it is not easy to read, writing that much is rubbish. The decision also reaches past this one page: section names, their order, and what sits on stage rather than folded are all produced by `build.py`, so whenever this question moves, `ref/q-template.md` and the wording of every other question on the board have to move with it.

## Boundary
- ✅ Covered here
  `board.html`'s own **single-question focus mode**: section order, section names, what is on stage / what folds, the type hierarchy.
- ↪ Covered elsewhere
  A separate deck for projection is `QA3`. Whether each question's **prose is well written** is `QA5`'s writing rules.

## Diagram
```
┌ marquee bar ≈110px ─────────────────────┐
│ /haipipe-board   │ spine · close        │  always present
├─────────────────────────────────────────┤
│ QA4  🟡 PARTIAL  🔧 CC                   │  status bar
│ Single Question Webpage Layout  ← 38px   │  .h2
│ ❓ Question   1 para + 2–4 bullets       │  .ask   ← this alone should orient
│ 🚧 Boundary   covered here / elsewhere   │  .bnd
│ ┌───── ascii figure ─────┐              │  .dia
│ 🎯 Items to Finish  ☑☑☑☐        7/9     │  .col.goal  intent first
│ 📍 Where we are                          │  .col.now   status second
│    each item:  heading  [more details]   │  ← click to open the paragraph
│ ▸ Law ▸ Lesson ▸ Why here ▸ Log          │  folded, never on stage
│ ← QA3       ☰ Index       QA5 →          │  pinned to the bottom
└─────────────────────────────────────────┘
unframed = no border · no rounded corners · no card background
```

https://app.excalidraw.com/s/1JWkKv8oMIX/4SD9kLApiQC?element=gFrVKXlBG2d-IrA9PD7Wv

## Items to Finish
- [x] Unframed
      A question opened on its own carries no border, no rounded corners, and no card background — the content sits directly on the page. This began as JL's complaint on 260722 that the page felt "boxed in" compared with the slides `/html-ppt` produces. The fix was not cosmetic: a card frame silently tells the reader they are looking at one item in a collection, which is precisely the wrong signal when the intent is that this single question should own the whole screen. Removing the frame, raising the title to 38px, and compressing the header into a thin marquee bar together changed what the page claims to be.
- [x] The gap is visible at a glance
      Someone who reads nothing but the headings should still come away with two facts: what is being asked, and how far it is from done. This is what the auto-counted `5/6` in the `Items to Finish` heading buys — it turns a checklist into a progress signal that survives not being read. The underlying idea is that most people scan a board rather than read it, and a page that only rewards full reading will be misjudged by everyone who scans.
- [x] Paging without returning to the index
      Every screen ends with one line: `← previous · ☰ Index · next →`. The reason is behavioural rather than technical — when moving on requires a trip back to the index, people stop after one question instead of reading the run. Since the questions in a group are usually meant to be read in sequence, forcing a detour between them works against the board's own structure.
- [x] Uneven lengths leave no big blank
      `Items to Finish` and `Where we are` stack vertically instead of sitting side by side. They were originally side by side, and JL asked for the change on 260723 for a plain reason: the two are almost never the same length, so one column always ended in a large area of white space, and worse, the shorter column looked finished when it had simply run out. Stacking also removes the accidental implication that the two are parallel or comparable — they are not.
- [x] Long passages can be chunked
      Body text uses `- short heading` with an indented explanation beneath it, plus full-line bold sentences acting as group titles above a run of items, and checklist entries may carry explanations of their own. This structure exists because the alternative — several unbroken paragraphs in a row — is unreadable on a projected screen and unscannable on a laptop. The explanation is folded by default and the heading is not, which is what makes it safe for an explanation to be long: it costs the scanning reader nothing.
- [x] Order flipped to "intent first, status second"
      The on-stage order became `Question → Boundary → Diagram → Items to Finish → Where we are`, implemented in `build.py` and verified against the rendered page rather than the markdown. Before the 260723 redesign `Where we are` came first, which meant a reader with no background met implementation detail before learning what was being decided. That was this layout's single worst flaw, and it was invisible to us precisely because we already knew the goal — the detail read as context to people who had it, and as noise to everyone else.
- [x] Section names switched to plain language
      `Done when` became `Items to Finish` and `Now` became `Where we are`. The old names were compact but slightly cryptic; the new ones say what the section contains without needing to be learned. Because renaming a section could have broken every existing board, `ALIAS` was added so one slot answers to several names — old boards, including the ones with Chinese section names, regenerate untouched.
- [x] Every question on the board rewritten to the new structure
      All 18 questions then on the board were converted: `## Question` rewritten as one paragraph plus bullets, `## Boundary` and `## Files` added, and the retired `## Why here` folded into the Question bullets. The acceptance check inspected the **generated page** for the `.bnd` and `.fls` blocks rather than grepping the markdown for section names — an earlier substring check had been fooled by text sitting inside an ascii fence, and QA2 passed that way while actually missing the section.
- [ ] A zero-background reader understands one page in one pass
      The remaining bar, and the only one that tests the layout's actual claim: hand one question to a fresh agent with no prior context and have it retell what is being asked, what counts as done, and where things stand. It counts only if all three come back intact. This item exists because of what happened on 260723 — the question closed ✅ with every other box ticked and was reopened the same day, since none of those boxes represented the reader the layout is for.

## Where we are
**✅ Layout and generator are done; acceptance is two steps short.**

- Order and names (the 260723 redesign)
  The on-stage order is now fixed as `Question → Boundary → Diagram → Items to Finish → Where we are` — intent first, status second — and the two status sections were renamed to `Items to Finish` and `Where we are`. `Why here` was retired in the same pass, its job absorbed into the `## Question` bullets so that the opening section could stand alone. This was the largest single change to the layout, and it came from JL's observation that a zero-background reader could barely follow the page; the diagnosis was that the ordering, not the wording, was doing the damage.
- `## Question` became "one paragraph + bullets"
  The section is rendered through `body()`, with the first paragraph set as a 21px lead line and the bullets following beneath it. The bullets are not decoration — they carry why the question is hard, what breaks while it stays open, and what it affects downstream. The acceptance bar attached to this shape is deliberately harsh: this section alone, with nothing after it, should orient someone who has never seen the board.
- `🚧 Boundary` added
  A new section stating what the question owns and, more importantly, what it does not, naming the question that owns the excluded part. It was added because readers were repeatedly judging a question against expectations imported from a neighbouring one — asking why QA4 said nothing about writing quality, when writing quality is QA5's subject. Declaring the exclusion turned out to be more useful than declaring the ownership.
- Old boards do not break
  `ALIAS` allows a single slot to answer to several names: `Done when` maps to `Items to Finish`, `Now` maps to `Where we are`, and the original Chinese section names still resolve. This was a precondition for the rename rather than an afterthought — without it, renaming two sections would have silently emptied those blocks on every board written before the change, and the damage would only have surfaced the next time someone regenerated an old page.

**Only the last step remains:**

- Cold-read acceptance
  A fresh agent reads one page and must retell what is being asked, what counts as done, and where things stand. All 18 questions were converted to the new structure, so QA4 is no longer the only page written to the standard and the cold read will test the real state of the board rather than one hand-tuned example. Until this passes, the layout's central claim — that one page is understandable in one pass — remains asserted rather than demonstrated, which is why the question sits at 🟡 and not ✅.

## Files
- `build.py`
  The generator. On-stage order, section names, `ALIAS` (one slot, many names), the rendering and CSS of `.ask`/`.bnd`/`.fls` — change this question, change here first.
- `ref/q-template.md`
  The file copied for every new question. Its section order and guide sentences must match this question, or new questions drift back.
- `ref/board-form.md`
  The full spec: §4 section↔page mapping + required/optional, §8 on-stage order and the three-level hierarchy.
  **Division of labour:** §4 holds the *technical* mapping (name → CSS class → required/optional); this question's `## Law` holds the *meaning* of each section in prose. Neither repeats the other — the earlier attempt to keep an HTML skeleton here went stale and was removed, and that trap is what the split avoids.
- `SKILL.md`
  The "one Q file" section table + the on-stage order sentence; the section names in the `sync` write-back table must follow too.
- `board.html`
  Generated. **Never hand-edit** — change the md and regenerate.

## Law
- On-stage order is fixed: intent first, status second
  `Question → Boundary → Diagram → Items to Finish → Where we are`. Before the redesign Now came first and zero-background readers hit implementation detail head-on — the layout's worst flaw.
- `## Question` is one paragraph + 2–4 bullets
  The bullets carry "why hard / what breaks if left / what it affects". Acceptance bar: **this section alone orients a zero-background reader.**
- Every item explanation is a paragraph, not a clause (JL 260724)
  The `- short heading` + indented explanation pattern applies to items in **every** section, not only `## Question`, and the explanation is a real paragraph: what it means, what happened, what we understand so far, and why it ended up this way. The model is the `## Question` bullets — each one states a position and the reasoning behind it, rather than labelling a topic. This is affordable because explanations fold by default while headings stay visible, so length costs the scanning reader nothing; a one-clause explanation, by contrast, reliably drops the reasoning and the history, which are the only parts that make a decision reviewable months later. Write the heading for the person scanning and the paragraph for the person who stops.
- `## Boundary` is `✅ Covered here` / `↪ Covered elsewhere` (JL 260724)
  The second half is the one that earns the section, so it must always name the question that does cover it — a bare exclusion tells the reader nothing and reads as a refusal. The labels were originally "This question owns" and "This question does not own"; JL rejected that wording on 260724 as stiff and legalistic, and the `↪` replaced `❌` because the line's job is to redirect the reader, not to deny them.
- Foldable items carry a visible `[more details]` control (JL 260724)
  Any item with an explanation renders its heading followed by a small `[more details]` pill, which reads `hide` once open. Before this, the only cue that an item could be opened was a small `▸` triangle, and readers simply did not know there was anything beneath — the fold was working and invisible at the same time. Implemented purely in CSS via `::after`, so the zero-script invariant holds: strip every script and the paragraphs are still in the DOM and still open on click.
- Focus = a slide, not a card
  Strip border, corners, background; content flows directly; `min-height` fills the screen. Title 38px, lead 21px, body 16px, width 1000px. Pure CSS (`:target` + `:has()`).
- What is on stage, what folds
  On stage: title, Question, Boundary, Diagram (the signature figure never folds), section headings (underlined), item names, checklist boxes + names.
  Collapsed by default: item explanations, code blocks (folded to one line `</> code · N lines`).
  Sunk into the bottom fold: Why here · Discussion · Comments · Law · Lesson · Glossary · Log.
- An expand-all beside every section heading
  Opens/closes all items and code in that section at once; pure enhancement — with scripts stripped, each item still opens individually.
- Long questions scroll — never truncate, never split; no 16:9 lock, follow window height
  Locking the aspect ratio is the projection deck's business (`QA3`).
- A real space after the id in the headline
  So copying the headline yields `QA4 Single…`, not `QA4Single…`.
- Renaming sections must go through ALIAS; old boards must never break
  One slot, many names; old boards regenerate without a single edit.

**What each section is for — one paragraph each**

These say what each section *means* and what belongs in it. The technical mapping (section name → CSS class → required/optional) stays in `ref/board-form.md §4` and is not repeated here; prose *quality* is `QA5`'s business, not this question's. On the page each heading below is visible and its paragraph is folded — open the one you need.

- ❓ Question — the section that has to work alone
  One paragraph stating the actual question as a question, then two to four bullets carrying why it is hard, what breaks if it stays undecided, and what it affects downstream. This is the only section with a hard acceptance bar: a reader with no background reads this and nothing else, and can still say what is being decided. The common failure is writing a topic label — "Cohort codes", "Physician table" — which tells the reader the subject but never reveals what is actually unresolved. If the section can be read without learning that something is open, it has failed.
- 🚧 Boundary — mostly about what is *not* owned
  Two halves: what this question decides, and what it explicitly does not. The second half is the one that earns its place. Readers arrive carrying expectations from a neighbouring question, and without an explicit "this is not mine, `QAn` owns it" they will judge this question for failing to answer something it never claimed. Naming the owning question, not just the exclusion, is what makes the boundary usable rather than defensive.
- 🖼 Diagram — the one figure that never folds
  A single ascii figure carrying the shape of the problem: a flow, a comparison, a before/after, a set of options side by side. It stays on stage permanently because a figure that must be unfolded has already lost to the paragraph above it. The test is subtraction: if removing the figure costs the reader nothing, it was decoration. A good one lets you skip a paragraph of prose; a bad one restates that paragraph in box-drawing characters.
- 🎯 Items to Finish — the definition of done, not a to-do list
  A checklist where each line is a condition that can be judged true or false by someone who is not you, with the heading counting ticks automatically. The binding rule is that nothing gets ticked until it has actually been verified. The subtler failure is a checklist that is complete and still proves nothing, because it never included the real user — this question hit exactly that trap: it closed ✅ with every box ticked and was reopened the same day because "a zero-background reader understands it" was not among the boxes.
- 📍 Where we are — the honest present tense
  What is true right now, with numbers wherever numbers exist: counts, versions, which of several things is built and which is not. It sits *after* the goal deliberately, because a reader who meets implementation detail before understanding the objective drowns in it — that ordering was this layout's worst flaw before the 260723 redesign. Phrases like "basically done" belong nowhere in it; either a thing is done and can be named, or it is not.
- 📎 Files — where the work actually lands
  The files this question moves or depends on, each with a line explaining why it matters here, with paths rendered as clickable links. This is not an exhaustive list of everything touched; it is the shortlist someone needs in order to start. Its real job is to close the gap between a decision written on a board and the code that decision governs, so that a settled question can be acted on without a search.
- ⚖ Law — the rules that survived the argument
  What has actually been decided and will be followed from now on, one rule per line with the reasoning behind it. Only settled things go here: writing an intention as law is how a casual preference hardens into a constraint nobody remembers agreeing to. This section carries a second job — when a question reaches ✅ SETTLED, its Law is what graduates into `SKILL.md` or `ref/`, so anything written here should be worth reading by someone who never saw the board.
- 💡 Lesson — the traps, kept specific
  What went wrong and what it cost, in enough detail that the same mistake is recognisable next time. Generic advice is worthless here; the entries that earn their place are the ones with a concrete failure attached — a checklist that was fully ticked and still wrong, an ordering that made identical text unreadable. If a lesson could have been written before the work started, it is not a lesson.
- 📖 Glossary — the terms a stranger would stumble on
  One line per word, in the form `term: explanation`. The rule attached to it is strict: any phrase invented on this board must be defined here or must not be used at all. This is what stops a board from developing a private vocabulary that only its authors can read — the exact failure that makes a handed-over board useless to the person receiving it.
- 💬 Discussion — the running argument
  Loose exchange, one line each, written as `> JL:` and answered as `>> CC0724:`. It preserves how a decision was reached, which matters when the decision is later questioned and nobody remembers what was already considered and rejected. Lines beginning `> JL:` are never deleted — when a point is resolved it gets marked resolved, not erased.
- ☑ Comments — remarks pinned to a specific sentence
  Entries in the form `- [ ] WHO 「the quoted sentence」 · YYMMDD HHMM`, with the quoted text highlighted in the body above and `[x]` marking resolved. Unresolved comments open automatically, so an open thread cannot be missed by scrolling past a collapsed block. Written by the page's comment button when the server is running, or by hand when it is not.
- 🗒 Log — what changed, newest first
  One line per change, `YYMMDD HHMM · what changed`, most recent at the top. It answers "what happened to this question since I last looked" without reading the whole page, which is the question a returning reader actually has. Entries record the change and its cause, not a restatement of the current state — the current state is what `## Where we are` is for.
- 🕳 Why here — retired, still parsed
  A section that once justified why a question deserved a page. Its job moved into `## Question`'s bullets so that the first section could orient a reader on its own. Old boards that still carry it regenerate without edits; the content is kept and sinks into the bottom fold rather than being dropped.

## Lesson
- "Settled" can be overturned by one sentence
  This question was closed ✅ on 260723 with every finish line ticked, and was knocked back to 🟡 the same day by a single remark from JL: a zero-background reader could hardly understand the page. Nothing about the work was wrong; the checklist was. It contained eight conditions about structure and not one about the person the structure exists for, so it could be completed in full while the actual goal went unmet. **A checklist that omits the real user proves nothing when fully ticked** — and the failure is invisible from the inside, because the author always reads the page with the context already in their head.
- Order beats wording for readability
  The same sentences, with `Where we are` above the goal versus below it, read like two different documents. Before the redesign the page opened with implementation detail; afterwards it opened with the question. No prose was rewritten in that pass and yet the page became readable. The general form: when a page is hard to follow, reorder before rewriting, because wording improvements applied to a bad order are largely wasted effort.
- Long explanations are free when they fold
  Item explanations are collapsed by default while their headings stay visible, which changes the economics of writing them. A scanning reader pays nothing for a paragraph they do not open, so the usual pressure to compress an explanation into a clause disappears — and compressed clauses are exactly what strips out the reasoning and the history that make a decision reviewable later. The rule that follows: write the heading for the scanner and the paragraph for the person who stops.

## Glossary
unframed: no border, rounded corners, or card background wrapping the content — it sits directly on the page.
group title: a full-line bold sentence in the body that leads a run of items; shown with 🔹 or the author's own emoji.

## Discussion
> JL: can this slide be more like the slides in /html-ppt? I don't want it boxed in.
>> CC0722: in focus mode the border, corners, and card background are gone, the title is at 38px, and the header is squeezed into a marquee bar.
> JL: what matters most is the Question section — one paragraph plus a few bullets. Right now a zero-background reader can hardly understand it.
>> CC0723: reordered and renamed along these lines, and added 🚧 Boundary (owns / does not own). QA4 knocked back to 🟡 pending the per-question rewrite + cold-read acceptance.

## Comments
- [x] JL “all four undecided items are settled — closing this question” · 260723 1524
      this sentence is a group title (item group name) and should look different from the items below it.
      >> CC0723: added the group-title level — a full-line bold `**…**` renders as its own layer with 🔹, one size above items, between the section heading and the items.
- [x] JL “open a Q” · 260723 1217
      could the Question section carry its label explicitly? The `.ask` line used to show only a bare `❓`.
      >> CC0723: added the small “❓ Question” label, shown like 📍 / 🎯.
- [x] JL “Now and Done when stack vertically” · 260723 1010
      this section's layout could be better — bullet-point style: one topic, then the explanation under it.
      >> CC0723: added the item syntax: write `- short heading` in md, indent two spaces below for the explanation.
- [x] JL “the skeleton a Q generates on the page” · 260723 1030
      could the slide's html template be written into this question?
      >> CC0723: the HTML skeleton + mapping table were added earlier; after the 260723 redesign the skeleton went stale and was removed — the mapping lives in `ref/board-form.md §4`, no second copy maintained here.

## Log
260724 1600 · Two JL calls: (1) foldable items now carry a visible `[more details]` pill — the `▸` triangle alone left readers unaware anything could open; pure CSS `::after`, flips to `hide`. (2) `## Boundary` labels reworded `This question owns / does not own` → `✅ Covered here` / `↪ Covered elsewhere`, swept across all 24 questions on this board and 21 on the CMS board, plus `ref/q-template.md`
260724 1530 · JL: item explanations should read like the `## Question` bullets — a real paragraph carrying what happened and what we understand, not a clause. Rewrote every item in `Items to Finish` / `Where we are` / `Lesson` to that standard, added it as a Law, and wrote it into `ref/q-template.md` so new questions inherit it
260724 1500 · `## Law` gains "What each section is for — one paragraph each": all 12 sections (+ retired `Why here`) now carry a real paragraph instead of a few words, folded on stage so the detail is there when wanted (JL 260724). `## Files` records the split from `ref/board-form.md §4` (spec vs meaning) so the stale-duplicate trap does not recur
260724 1242 · Translated to English (JL 260724: everything on the board in English)
260723 · All 18 questions on the board converted to the new structure (Question bullets + Boundary + Files + Why here retired) → only "zero-background reader understands one page" remains
260723 · Redesign: order flipped to "intent first, status second" (Question paragraph+bullets → Boundary → Diagram → Items to Finish → Where we are); `Why here` retired into Question; `🚧 Boundary` added; old names preserved via ALIAS. state ✅ → 🟡, pending per-question rewrites + cold read
260723 · Title `Single-Q slide layout` → `Single Question Webpage Layout`; file renamed `QA4-slidedesign.md` → `QA4-pagelayout.md`
260723 1720 · Closed: `## Law` written, finish line 6 ticked, state → ✅ (knocked back by JL the same day, see Lesson)
260723 1650 · Real space added after the headline id — copying no longer yields QA4Single…
260723 1630 · Code blocks fold to `</> code · N lines` by default; the `## Diagram` signature figure never folds
260723 1620 · Underline added below section headings; expand-all added on the right
260723 1400 · Item explanations moved into native `<details>`; section headings enlarged to 18px
260723 1100 · Two comments moved from Discussion into the new `## Comments`
260723 0905 · Now vs. done-when switched from side-by-side to stacked
260722 2315 · Border / corners / card background removed, title to 38px, header squeezed into the marquee bar
260722 2305 · Focus mode landed: pure CSS `:target` + `:has()`
260722 2300 · JL asked for "slides like /html-ppt, not boxed in" — question opened
