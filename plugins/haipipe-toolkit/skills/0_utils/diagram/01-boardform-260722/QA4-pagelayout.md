# Shared Q/S Face Webpage Layout
state: ✅ SETTLED
owner: CC
method: one face grammar, two workflow kinds; compass Opening owns stage orientation
session: cd5e7f5f-15c7-49ba-a97f-bdf90ef3f534
## Question
When one Q ruling or S lifecycle stage is opened and it alone fills the screen, how should that shared face be arranged so that someone with **no background at all** can read top to bottom once and know: what is being asked, what the substantive content is, what counts as done, and where things stand now?

The difficulty is that one page has to carry intent, substance, and status without making a stage look like a different product from a ruling. A Q may have no Content; an S must carry the stage's Content and its human gate. The shared reading order still matters more than the wording: Question must orient the reader before Content asks for attention, and Items to Finish must define the gap before Where we are reports progress. This matters because the board is not written for us. It exists to be discussed with colleagues, so a page the second person cannot follow is worth nothing no matter how much is on it. If it is not easy to read, writing that much is rubbish.

## Boundary
- ✅ Covered here
  `board.html`'s **single-face focus mode** for Q and S: shared section order, Content placement, what is on stage / what folds, and the type hierarchy.
- ↪ Covered elsewhere
  A separate deck for projection is `QA3`. Whether each face's **prose is well written** is `QA5`'s writing rules. Q and S workflow contracts belong to their owning skills.

## Diagram
```
Focus mode: one face owns the whole screen. Read top to bottom —
intent first, status second.

  ═══ marquee bar  ≈110px, always present  (/haipipe-board · spine · close) ═══

  S4    🟡 PARTIAL   STAGE   🧠 JL
  Display: figures and tables               — same title hierarchy as Q

  🧭 Opening         one visible orientation layer:
       Question      the actual prompt (lead only)
       Boundary      covered here / covered elsewhere
       Why it matters Q: under Content · S: open here
       Stage Record  S optional · collapsed here when supplied
  ▸ 🖼 Diagram       its own section; figure hidden until clicked
  📚 Content         Q: Why first · S: remaining stage substance
  🎯 Items to Finish    ☑ ☑ ☑ ☐   7/9      — includes Q-consumers     ← intent
  📍 Where we are       the honest present                            ← status
        each item = heading  +  [more details]  (click to open the paragraph)

  ─── below the fold, never on stage ───
  ▸ Law   ▸ Lesson   ▸ Why here   ▸ Log
  ← QA3        ☰ Index        QA5 →         — pinned to the bottom

  unframed = no border · no rounded corners · no card background
```

https://app.excalidraw.com/s/1JWkKv8oMIX/4SD9kLApiQC?element=gFrVKXlBG2d-IrA9PD7Wv

## Content
### 1 · Opening — orient the reader
Opening answers "What am I looking at, and why should I care?" before asking the reader to absorb detail. It always shows the actual Question lead and includes Boundary when the source provides one. On an S face it also shows Why this matters and offers an optional Stage Record as a collapsed detail when supplied; on a Q face, Why this matters starts Content instead. A reader should be able to state the face's purpose and scope after reading Opening alone.

#### Boundary
Boundary says both what this face decides and where adjacent concerns belong. Its `↪ Covered elsewhere` half must name the owning Q or S, because an exclusion without a destination leaves the reader stranded.

### 2 · Diagram — reveal the shape
Diagram gives one visual account of the flow, comparison, before/after, or option set. Its heading remains visible, but the figure starts hidden so a large canvas does not dominate the page before it is wanted. Keep it only when opening it replaces or clarifies prose; decoration does not earn a section.

### 3 · Content — establish the substance
Content carries the material the face exists to establish after orientation. It is required on S and optional on Q. Each direct `###` heading becomes one named, collapsible subsection so readers can see the argument's parts before choosing which details to open. On Q, Why this matters appears first; on S, an optional Stage Record moves to Opening when supplied and the remaining stage substance stays here.

### 4 · Items to Finish — define the gap
Items to Finish is the testable definition of done, not a loose task list. Every checkbox must describe a condition that another person can judge true or false, and the heading reports the completed count automatically. On S, each Q-consumer remains one complete record and closes only after its answer is interpreted and integrated into Content.

### 5 · Where we are — report the present
Where we are states what is true now: counts, versions, decisions reached, and work still open. It deliberately follows Items to Finish so readers learn the target before seeing implementation detail. It summarizes progress without repeating the full evidence already held in Content or the checklist.

### 6 · Files — point to the work
Files names the small set of sources, generated outputs, and implementation files needed to continue the work, with one sentence explaining why each matters. It is an action map rather than an exhaustive change list, and generated files must be labeled so nobody edits the wrong layer.

### 7 · Supporting folds — preserve history without blocking the read
Law, Lesson, Glossary, Discussion, Comments, and Log sit below the main reading path and begin folded. They preserve rules, failures, vocabulary, deliberation, pinned remarks, and change history for readers who need them, while Opening through Files remains a clean first pass. Retired Why here content is still parsed here for compatibility, but new rationale belongs in Question.

## Items to Finish
- [x] 🖼 Unframed
      A question opened on its own carries no border, no rounded corners, and no card background, so the content sits directly on the page.
      This began as JL's complaint on 260722 that the page felt boxed in compared with the slides `/html-ppt` produces. The fix was not cosmetic. A card frame quietly tells the reader they are looking at one item in a collection, which is precisely the wrong signal when the intent is that this single question owns the whole screen. Removing the frame, raising the title to 38px, and compressing the header into a thin marquee bar together changed what the page claims to be.
- [x] 👁 The gap is visible at a glance
      Someone who reads nothing but the headings still comes away knowing what is being asked and how far it is from done.
      This is what the auto-counted `5/6` in the `Items to Finish` heading buys: it turns a checklist into a progress signal that survives not being read. The assumption behind it is that most people scan a board rather than read it, so a page that only rewards full reading will be misjudged by everyone who scans.
- [x] ⏭ Paging without returning to the index
      Every screen ends with one line: `← previous · ☰ Index · next →`.
      The reason is behavioural rather than technical. When moving on requires a trip back to the index, people stop after one question instead of reading the run. Questions in a group are usually meant to be read in sequence, so forcing a detour between them works against the board's own structure.
- [x] 📐 Uneven lengths leave no big blank
      `Items to Finish` and `Where we are` stack vertically instead of sitting side by side.
      They were originally two columns, and JL asked for the change on 260723 for a plain reason: the two are almost never the same length, so one column always ended in a large patch of white space, and the shorter one looked finished when it had simply run out. Stacking also removes an accidental implication that the two are parallel or comparable, which they are not.
- [x] ✂️ Long passages can be chunked
      Body text uses `- short heading` with an indented explanation beneath it, and checklist entries can carry explanations too.
      The structure exists because the alternative, several unbroken paragraphs in a row, is unreadable on a projected screen and unscannable on a laptop. The heading stays on stage while the explanation folds, which is what makes it safe for an explanation to be long: it costs the scanning reader nothing.
- [x] 🔀 Order flipped to "intent first, status second"
      The visible hierarchy is now `Opening → Diagram → Content → Items to Finish → Where we are → Files`, verified against the rendered page rather than only the markdown. Opening carries the question lead and optional Boundary; on S it also carries Why this matters and, when supplied, an optional Stage Record. Diagram is a collapsed peer section. Q rationale starts Content; the remaining S subsections stay there.
      Before the 260723 redesign `Where we are` came first, so a reader with no background met implementation detail before learning what was being decided. That was this layout's single worst flaw, and it was invisible from the inside precisely because we already knew the goal: the detail read as context to anyone who had it and as noise to everyone else.
- [x] 🏷 Section names switched to plain language
      `Done when` became `Items to Finish` and `Now` became `Where we are`.
      The old names were compact but had to be learned; the new ones say what the section contains. Because renaming a section could have broken every existing board, `ALIAS` was added so one slot answers to several names, and old boards, including the ones with Chinese section names, regenerate untouched.
- [x] ✍️ Every question on the board rewritten to the new structure
      All 18 questions then on the board were converted, not just this one.
      Each got an actual question lead plus a rationale paragraph, `## Boundary`, and `## Files`. The renderer now places that rationale under Content rather than keeping it in Opening.
- [x] 🧩 One renderer accepts Q and S
      `Q*.md` and `S*.md` are recursively discovered, parsed into the same face data, rendered by the same page function, and accepted by comment/chat write-back.
      S faces carry a visible STAGE badge; question settlement and stage gates are counted separately so a gated lifecycle cannot inflate the ruling bar.
- [x] 🧭 Opening sits above Content
      Opening is the first visible section and contains the actual question lead plus optional Boundary. The compass marks orientation rather than implying that every face is an unanswered question.
      On Q, the rest of Question becomes Content's first "Why this matters" subsection. Older files keep `## Question`; `## Opening` is also accepted as its alias.
- [x] 🗂 Stage orientation moves into Opening
      On S, "Why this matters" is initially open inside Opening. An optional exact direct `### Stage Record`, when supplied, is lifted from explicit Content into the same Opening and starts collapsed.
      All remaining stage subsections stay under Content, so status context moves up without mixing the substantive record into the lead.
- [x] 🖼 Diagram is its own collapsed section
      Optional Diagram is a peer section between Opening and Content. Its heading stays visible while the ASCII or Excalidraw figure remains hidden until the reader clicks it.
      Native `<details>` preserves the no-script fallback: the figure remains in the HTML and can still be opened with all JavaScript stripped.
- [x] 🔎 Q-consumer moved into Items to Finish
      A stage consumer is a recognizable checklist record retaining its Q id, Description, Reason, Probe, and Answer.
      Its box closes only after the answer landed, was interpreted, and was woven into Content; deferred closes only after a forward pointer is recorded.
- [x] 🧪 A zero-background reader understands one page in one pass
      Hand one Q face and one S face to a fresh agent with no prior context and have it retell what is being asked, what Content establishes, what counts as done, and where things stand.
      Passed 260725 after three fresh-context reads. The first two recovered the template but exposed stale filenames, ambiguous gates, missing finish records, and contradictory asset paths; those were repaired. The third recovered QD2's full ruling, S4's 13-record closure map, live asset truth, appendix handoff, and Q/S closure semantics with no blocking ambiguity.
- [x] 📚 Every visible section explains its eventual purpose
      Content now names the intended reader outcome for Opening, Diagram, Content, Items to Finish, Where we are, Files, and the supporting folds. These meanings were moved out of Law because they describe how to read the page, not a hidden implementation constraint.

## Where we are
Settled. The shared Q/S layout now presents five section rows: compass Opening, collapsed Diagram, Content, Items to Finish, and Where we are; Files follows as the action map. Content now explains the eventual job of every section in seven named subsections, instead of burying those meanings under Law. Opening contains Question and optional Boundary on both kinds; S additionally carries open Why this matters and, when supplied, an optional collapsed Stage Record. The live MISQ board remains 14 Q + 8 S with separate progress and no lifecycle log sidecars.

- 260725 JL · 📚 Section purposes moved into Content
  JL asked for each Q-webpage section to explain what it is ultimately for. QA4 now exposes seven named Content subsections covering the full reading path and its supporting folds; Law keeps only the rules that govern that path.

- 260725 JL · 🧭 Stage orientation moved into Opening
  JL asked to place S0's Why this matters and Stage Record in Opening and replace its question mark. Opening now uses a compass; S stage orientation moves there while Q rationale stays under Content.

- 260725 JL · 🖼 Diagram became a collapsed peer section
  JL asked for Diagram to read as a section and stay hidden before clicking. The renderer now places a native `🖼 Diagram` disclosure between Opening and Content; only its heading is visible initially.

- 260725 JL · ❓ Question became Opening at the visual level
  JL asked for the first page layer to read like an opening before Content, Items to Finish, and Where we are. The renderer keeps the question lead and Boundary in Opening, moves the explanatory remainder into Content, and preserves source compatibility. The later Diagram ruling gives Diagram its own collapsed row.

- 260725 CC · 🧪 Cold-read acceptance passed
  Two fresh readers found real content-ledger ambiguities rather than template failures; the board was revised after each pass. A third reader recovered Question, Content, every finish/defer record, current state, asset truth, and closure semantics for both workflow kinds, then returned PASS.

- 260725 JL · 🧩 Q and S combined into one template
  JL asked to put Question above Content and use Q-consumer as Items to Finish.
  The renderer, shared template, board specification, and MISQ lifecycle board now follow that shape. The workflow semantics stay distinct: Q settles a ruling; S passes a human stage gate.

- 260722 JL · 🃏 The page stopped looking like a card
  JL asked for pages like the slides `/html-ppt` produces, not something boxed in, and focus mode landed the same evening.
  Border, rounded corners, and card background were removed so the content sits directly on the page, the title went to 38px, and the header was compressed into a thin marquee bar. The mechanism is pure CSS, `:target` plus `:has()`, so a question fills the screen without any script running. The reason this was not cosmetic: a card frame quietly tells the reader they are looking at one entry in a collection, which is the wrong signal when the intent is that this single question owns the screen.
- 260723 JL · 🧱 Goal and status stacked instead of side by side
  `Items to Finish` and `Where we are` were sitting in two columns, and JL asked for them stacked.
  The two are almost never the same length, so one column always ended in a large patch of white space, and the shorter one read as finished when it had simply run out. Stacking also removes an accidental implication that the two sections are parallel or comparable, which they are not: one is a target and the other is a position.
- 260723 CC · 🔀 Order flipped to intent first, sections renamed
  On-stage order became `Question → Boundary → Diagram → Items to Finish → Where we are`, and `Done when` and `Now` were renamed to `Items to Finish` and `Where we are`.
  Before this pass the page opened with `Where we are`, so a reader with no background met implementation detail before learning what was being decided. That was the layout's worst flaw and it was invisible from the inside, because anyone who already knew the goal read that detail as context rather than noise. The renames were a separate, smaller fix: the old names were compact but had to be learned, and the new ones say what the section holds.
- 260723 CC · 🚧 Boundary added, and Why here retired
  A new `## Boundary` section states what a question covers and what is covered elsewhere, while `## Why here` was absorbed into the Question rationale and now renders under Content.
  Boundary was added because readers kept judging a question against expectations carried over from a neighbouring one, for example asking why QA4 says nothing about writing quality when that is QA5's subject. Naming the question that does cover the excluded part turned out to matter more than stating what this one covers. `Why here` went away in the same pass so that the opening section could orient a reader without help from anything below it.
- 260723 CC · 🔗 ALIAS so old boards keep working
  One slot now answers to several section names, so `Done when`, `Items to Finish`, and the original Chinese names all resolve to the same block.
  This was a precondition for the rename rather than a convenience added afterwards. Without it, renaming two sections would have silently emptied those blocks on every board written before the change, and nobody would have noticed until the next time an old page was regenerated.
- 260723 CC · ✍️ All 18 questions rewritten to the new structure
  Every question then on the board was converted, not just this one.
  The acceptance check inspected the generated page for the `.bnd` and `.fls` blocks rather than grepping the markdown for section names. An earlier substring check had been fooled by text sitting inside an ascii fence, and QA2 passed that way while actually missing the section, so the check now looks at what was rendered.
- 260724 JL · 🌐 Everything on the board in English
  JL ruled that board markdown, generated pages, and artifacts are written in English.
  The questions and copied template guidance are English. Internal skill specifications may remain bilingual because they are not rendered board content.
- 260724 JL · 🖱️ Item shape: heading, one sentence, then [more details]
  An item now shows its heading and a one-sentence summary on stage, with the long explanation behind a visible `[more details]` button.
  Two complaints produced this. First, the only cue that an item could be opened was a small `▸` triangle, so readers did not know anything was there: the fold was working and invisible at the same time. Second, a heading alone gives too little to decide whether to open it. The first indented line in the markdown is now the visible summary and the remaining lines are the folded detail, styled a shade lighter so the two are distinguishable at a glance.
- 260725 CC · 🧪 Cold-read acceptance passed
  Fresh agents recovered what is asked, what Content establishes, every finish condition, current state, and the distinct Q/S closure semantics. The Opening revision was cold-read twice: the first read found this stale historical status sentence; after correction, the second clean-context read returned PASS.

## Files
- `build.py`
  The generator entry. Q/S discovery and parsing live under `src/`; output remains self-contained.
- `src/common.py`
  Q/S filename grammar, recursive discovery, and safe write-back path validation.
- `src/parse.py`
  Classifies Q as `question` and S as `stage` while preserving one parsed face shape.
- `src/page_question.py`
  The shared renderer, including Question above collapsible Content.
- `src/page_board.py`
  Separate question-settlement and stage-gate summaries.
- `ref/q-template.md`
  The file copied for every new question. Its section order and guide sentences must match this question, or new questions drift back.
- `ref/board-form.md`
  The full spec: §4 section↔page mapping + required/optional, §8 on-stage order and the three-level hierarchy.
  **Division of labour:** §4 holds the *technical* mapping (name → CSS class → required/optional); this question's `## Content` holds the *reader-facing purpose* of each section; `## Law` holds the rules that constrain them. The earlier attempt to keep an HTML skeleton here went stale and was removed, and that trap is what the split avoids.
- `SKILL.md`
  The shared-face rules and the distinct Q/S workflow semantics.
- `0-lifecycle/`
  Complete consumer: 14 Q rulings + 8 S lifecycle stages on one board.
- `board.html`
  Generated. **Never hand-edit**: change the md and regenerate.

## Law
- On-stage order is fixed: intent first, status second
  `Opening → Diagram → Content → Items to Finish → Where we are → Files`. Opening contains the question lead and optional Boundary. On Q, the remaining Question rationale begins Content. On S, that rationale becomes Why this matters inside Opening, and an optional exact `### Stage Record` moves there collapsed when supplied; S still requires explicit Content for the remaining substance.
- One face grammar, two workflow kinds
  Q is a ruling and closes by settlement; S is a lifecycle stage and closes at its human gate. They share the renderer and reading order, not their counters or governance.
- Opening always precedes Content
  The face must orient a zero-background reader before presenting substantive material. Opening carries the actual question lead and its scope. S also carries Why this matters there and may carry an optional collapsed Stage Record; Q carries Why this matters under Content. An optional collapsed Diagram row separates Opening from the remaining Content.
- S consumers live in Items to Finish
  Keep the Q id and Description / Reason / Probe / Answer together inside one checklist record. Tick only after answer, interpretation, and Content integration; summarize rather than duplicate in Where we are.
- `## Question` is one question lead + one rationale paragraph
  The lead is the actual prompt in Opening. The paragraph carries why it is hard, what breaks if left open, and what it affects; it renders as "Why this matters" inside Opening for S and as Content's first subsection for Q.
- Every item explanation is a paragraph, not a clause (JL 260724)
  The `- short heading` + indented explanation pattern applies to list and checklist items, and the explanation is a real paragraph: what it means, what happened, what we understand so far, and why it ended up this way. Question itself uses the lead-plus-rationale shape above, not item bullets.
- `## Boundary` is `✅ Covered here` / `↪ Covered elsewhere` (JL 260724)
  The second half is the one that earns the section, so it must always name the question that does cover it; a bare exclusion tells the reader nothing and reads as a refusal. The labels were originally "This question owns" and "This question does not own"; JL rejected that wording on 260724 as stiff and legalistic, and the `↪` replaced `❌` because the line's job is to redirect the reader, not to deny them.
- Foldable items carry a visible `[more details]` control (JL 260724)
  Any item with an explanation renders its heading followed by a small `[more details]` pill, which reads `hide` once open. Before this, the only cue that an item could be opened was a small `▸` triangle, and readers simply did not know there was anything beneath; the fold was working and invisible at the same time. Implemented purely in CSS via `::after`, so the zero-script invariant holds: strip every script and the paragraphs are still in the DOM and still open on click.
- Focus = a slide, not a card
  Strip border, corners, background; content flows directly; `min-height` fills the screen. Title 38px, lead 21px, body 16px, width 1000px. Pure CSS (`:target` + `:has()`).
- What is on stage, what folds
  On stage: title; compass Opening with the question lead and Boundary; S Why this matters; the Diagram, Content, Items to Finish, Where we are, and Files headings; item names and checklist boxes.
  Collapsed by default when present: optional S Stage Record, the entire Diagram body, item explanations, and code blocks (folded to one line `</> code · N lines`).
  Sunk into the bottom fold: Why here · Discussion · Comments · Law · Lesson · Glossary · Log.
- An expand-all beside every section heading
  Opens/closes all items and code in that section at once; pure enhancement: with scripts stripped, each item still opens individually.
- Long questions scroll: never truncate, never split; no 16:9 lock, follow window height
  Locking the aspect ratio is the projection deck's business (`QA3`).
- A real space after the id in the headline
  So copying the headline yields `QA4 Single…`, not `QA4Single…`.
- Renaming sections must go through ALIAS; old boards must never break
  One slot, many names; old boards regenerate without a single edit.

## Lesson
- "Settled" can be overturned by one sentence
  This question was closed ✅ on 260723 with every finish line ticked, and was knocked back to 🟡 the same day by a single remark from JL: a zero-background reader could hardly understand the page. Nothing about the work was wrong; the checklist was. It contained eight conditions about structure and not one about the person the structure exists for, so it could be completed in full while the actual goal went unmet. **A checklist that omits the real user proves nothing when fully ticked**, and the failure is invisible from the inside, because the author always reads the page with the context already in their head.
- Order beats wording for readability
  The same sentences, with `Where we are` above the goal versus below it, read like two different documents. Before the redesign the page opened with implementation detail; afterwards it opened with the question. No prose was rewritten in that pass and yet the page became readable. The general form: when a page is hard to follow, reorder before rewriting, because wording improvements applied to a bad order are largely wasted effort.
- Long explanations are free when they fold
  Item explanations are collapsed by default while their headings stay visible, which changes the economics of writing them. A scanning reader pays nothing for a paragraph they do not open, so the usual pressure to compress an explanation into a clause disappears, and compressed clauses are exactly what strips out the reasoning and the history that make a decision reviewable later. The rule that follows: write the heading for the scanner and the paragraph for the person who stops.

## Glossary
unframed: no border, rounded corners, or card background wrapping the content; it sits directly on the page.
group title: a full-line bold sentence in the body that leads a run of items; shown with 🔹 or the author's own emoji.

## Discussion
> JL: can this slide be more like the slides in /html-ppt? I don't want it boxed in.
>> CC0722: in focus mode the border, corners, and card background are gone, the title is at 38px, and the header is squeezed into a marquee bar.
> JL: what matters most is the Question section: one paragraph plus a few bullets. Right now a zero-background reader can hardly understand it.
>> CC0723: reordered and renamed along these lines, and added 🚧 Boundary (owns / does not own). QA4 knocked back to 🟡 pending the per-question rewrite + cold-read acceptance.
> JL: maybe we can combine Q, and S as one template.
>> CC0725: one renderer now serves both. Question sits above Content; S consumers live under Items to Finish; Q settlement and S gates remain separate.
> JL: Question can be something like Opening; then Content, Items to Finish, and Where we are.
>> CC0725: Opening became the visible first layer. At that point it contained Question, Boundary, and Diagram; the later Diagram ruling below supersedes that grouping.
>> CC0725: the remaining Question explanation becomes Content's first subsection. Diagram is now a separate collapsed section.
> JL: how to make the Diagram one section as well, and make it hidden before clicking?
>> CC0725: Diagram is now a peer-level native disclosure between Opening and Content. Its heading stays visible and its figure starts collapsed.
> JL: for Why this matters and Stage Record on S0, I think they can go to Opening. Change the Opening icon too, not a question mark.
>> CC0725: Opening now uses a compass. On S faces, Why this matters is open there and an exact Stage Record is collapsed there; Q faces keep Why this matters under Content.
> JL: Content should explain what every section in the Q webpage is eventually for: 1 Opening, 2 Diagram, and so on.
>> CC0725: moved the section meanings out of Law and into seven numbered Content subsections. The visible reading path is explained first; the lower historical sections are grouped as Supporting folds.

## Comments
- [x] JL “all four undecided items are settled, closing this question” · 260723 1524
      this sentence is a group title (item group name) and should look different from the items below it.
      >> CC0723: added the group-title level: a full-line bold `**…**` renders as its own layer with 🔹, one size above items, between the section heading and the items.
- [x] JL “open a Q” · 260723 1217
      could the Question section carry its label explicitly? The `.ask` line used to show only a bare `❓`.
      >> CC0723: added the small “❓ Question” label. Superseded 260725 first by peer-level Opening, then by the current “🧭 Opening” heading.
- [x] JL “Now and Done when stack vertically” · 260723 1010
      this section's layout could be better. Bullet-point style: one topic, then the explanation under it.
      >> CC0723: added the item syntax: write `- short heading` in md, indent two spaces below for the explanation.
- [x] JL “the skeleton a Q generates on the page” · 260723 1030
      could the slide's html template be written into this question?
      >> CC0723: the HTML skeleton + mapping table were added earlier; after the 260723 redesign the skeleton went stale and was removed: the mapping lives in `ref/board-form.md §4`, no second copy maintained here.

## Log
260725 · QA2/QA4 alignment pass made optional Boundary and optional S Stage Record explicit; fresh Q/S template render passed with Stage Record both present and absent
260725 · Section purposes moved from Law into seven numbered Content subsections: Opening, Diagram, Content, Items to Finish, Where we are, Files, and Supporting folds
260725 · Opening icon changed to compass; S Why this matters and Stage Record moved into Opening
260725 · Diagram became a peer-level native details section, collapsed by default
260725 · Opening fresh-agent loop passed: first read verified the hierarchy but caught a stale QA4 status sentence; after correction the second clean-context read returned PASS
260725 · visible hierarchy first simplified to Opening → Content → Items to Finish → Where we are; later the same day Diagram became its own collapsed peer section
260725 · QA4 settled after the required fresh-agent loop: two ambiguity-finding reads drove corrections; the third returned PASS with the full QD2/S4 model intact
260725 · QA4 widened from a single-question page to the shared Q/S face; Content inserted after Diagram, Q-consumer moved into Items to Finish, separate workflow counts shipped, and the MISQ board migrated to 14 Q + 8 S
260724 1600 · Two JL calls: (1) foldable items now carry a visible `[more details]` pill: the `▸` triangle alone left readers unaware anything could open; pure CSS `::after`, flips to `hide`. (2) `## Boundary` labels reworded `This question owns / does not own` → `✅ Covered here` / `↪ Covered elsewhere`, swept across all 24 questions on this board and 21 on the CMS board, plus `ref/q-template.md`
260724 1530 · JL: item explanations should read like the `## Question` bullets: a real paragraph carrying what happened and what we understand, not a clause. Rewrote every item in `Items to Finish` / `Where we are` / `Lesson` to that standard, added it as a Law, and wrote it into `ref/q-template.md` so new questions inherit it
260724 1500 · `## Law` gains "What each section is for: one paragraph each": all 12 sections (+ retired `Why here`) now carry a real paragraph instead of a few words, folded on stage so the detail is there when wanted (JL 260724). `## Files` records the split from `ref/board-form.md §4` (spec vs meaning) so the stale-duplicate trap does not recur
260724 1242 · Translated to English (JL 260724: everything on the board in English)
260723 · All 18 questions on the board converted to the new structure (Question bullets + Boundary + Files + Why here retired) → only "zero-background reader understands one page" remains
260723 · Redesign: order flipped to "intent first, status second" (Question paragraph+bullets → Boundary → Diagram → Items to Finish → Where we are); `Why here` retired into Question; `🚧 Boundary` added; old names preserved via ALIAS. state ✅ → 🟡, pending per-question rewrites + cold read
260723 · Title `Single-Q slide layout` → `Single Question Webpage Layout`; file renamed `QA4-slidedesign.md` → `QA4-pagelayout.md`
260723 1720 · Closed: `## Law` written, finish line 6 ticked, state → ✅ (knocked back by JL the same day, see Lesson)
260723 1650 · Real space added after the headline id: copying no longer yields QA4Single…
260723 1630 · Code blocks fold to `</> code · N lines` by default; Diagram stayed open at that time, superseded by the collapsed-section ruling on 260725
260723 1620 · Underline added below section headings; expand-all added on the right
260723 1400 · Item explanations moved into native `<details>`; section headings enlarged to 18px
260723 1100 · Two comments moved from Discussion into the new `## Comments`
260723 0905 · Now vs. done-when switched from side-by-side to stacked
260722 2315 · Border / corners / card background removed, title to 38px, header squeezed into the marquee bar
260722 2305 · Focus mode landed: pure CSS `:target` + `:has()`
260722 2300 · JL asked for "slides like /html-ppt, not boxed in"; question opened
