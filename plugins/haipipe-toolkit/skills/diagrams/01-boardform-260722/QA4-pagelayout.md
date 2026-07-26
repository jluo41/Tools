# Shared Q/S Face Webpage Layout
state: 🟡 PARTIAL
owner: CC
method: one face grammar; compose S Content from stage, venue, and upstream contracts
session: cd5e7f5f-15c7-49ba-a97f-bdf90ef3f534
## Question
When one Q ruling or S lifecycle stage is opened and it alone fills the screen, how should that shared face be arranged so that someone with **no background at all** can read top to bottom once and know: what is being asked, what the substantive content is, what counts as done, and where things stand now?

The difficulty is that one page has to carry intent, substance, and status without making a stage look like a different product from a ruling.
A Q may have no Content; an S must carry the stage's Content and its human gate.
The shared reading order still matters more than the wording: Question must orient the reader before Content asks for attention, and Items to Finish must define the gap before Where we are reports progress.
This matters because the board is not written for us.
It exists to be discussed with colleagues, so a page the second person cannot follow is worth nothing no matter how much is on it.
If it is not easy to read, writing that much is rubbish.

For an S page, layout alone is not enough: its Content blueprint should be created from the owning stage template, refined by the venue template, and constrained by accepted outputs and open requirements inherited from previous stages.
Those sources compose one explicit page; they are not competing templates and are not re-read on every render.

## Boundary
- ✅ Covered here
  `board.html`'s **single-face focus mode** for Q and S: shared section order, Content placement, what is on stage / what folds, and the type hierarchy.
- ↪ Covered elsewhere
  Projection (one file, two modes: scroll to read / one screen per face) is settled in `ref/board-form.md` §8, not here.
  Whether each face's **prose is well written**, and what checks that the page still renders this layout, is `QA9`.
  Q and S workflow contracts belong to their owning skills.

## Diagram
```
Focus mode: one face owns the whole screen. Read top to bottom —
intent first, status second.

  ═══ marquee bar  ≈110px, always present  (/haipipe-board · spine · close) ═══

  S-Main-7       🔴 OPEN      STAGE   🧠 JL
  S Main 7 · §6 Results                     — same title hierarchy as Q

  🧭 Opening         a plain heading, never a fold: it is always there
  the question lead ⌄ the actual prompt, always on stage, and it is the door:
                     click it and everything that explains it opens beneath
       Boundary      covered here / covered elsewhere
       Why it matters Q: under Content · S: in here
       Stage Record  S only · optional · in here when supplied
       Stage Contract S only · Required Inputs · Writing Style · Venue
       (FLAT: one click shows all of it, no ▸ inside, and no icons on these
        headings either — they are plain words so the seven read as one list)
  ▸ 🖼 Diagram       its own section; figure hidden until clicked
  📚 Content         Q: Why first · S: explicit composed blueprint
       Stage template    base subsections · artifacts · gate
       Venue template    reader · section · length · style constraints
       Previous stages   accepted inputs · unresolved requirements
       ### §6.1 …        one fold per division, numbered for depth
           #### P1 …     paragraphs always one level in, no 🔹
           (its job)     grey italic, on stage, one line only
  🎯 Items to Finish    ☑ ☑ ☑ ☐   7/9      — includes Q-consumers     ← intent
  📍 Where we are       the honest present                            ← status
        each item = heading  +  [more details]  (click to open the paragraph)

  ─── below the fold, never on stage ───
  ▸ Law   ▸ Lesson   ▸ Why here   ▸ Log
  ← QA2        ☰ Index        QA6 →         — pinned to the bottom

  unframed = no border · no rounded corners · no card background
```

https://app.excalidraw.com/s/1JWkKv8oMIX/4SD9kLApiQC?element=gFrVKXlBG2d-IrA9PD7Wv

## Content
### 1 · Opening — orient the reader
Opening answers "What am I looking at, and why should I care?" before asking the reader to absorb detail.
The 🧭 Opening heading never folds and the question lead never folds: both are always on stage, and the lead is the door (JL 260725).
Clicking the lead opens everything that explains it: Boundary, and on an S face also Why this matters, an optional Stage Record, and the Stage Contract; on a Q face, Why this matters starts Content instead.
The fold belongs on the sentence rather than on the section name, because a collapsed row reading only "🧭 Opening" announces nothing: a reader cannot tell that the ruling's scope is inside it, which is the fold-works-and-is-invisible failure the 260724 item Law already forbids.
A long question sentence with a caret beside it does announce itself, and it is the thing a reader wants explained, so the sentence is the honest handle.
Behind that one click everything is flat (JL 260725: "I don't want to have >"): Boundary always rendered as a plain heading plus its rows, and Why this matters, Stage Record, and the Stage Contract's Required Inputs, Writing Style, and venue section now render the same way instead of each sitting behind its own ▸.
The version that kept them as nested disclosures read as though the material were missing, because opening the lead revealed a list of shut doors rather than the orientation itself; one door is a disclosure, two doors in a row is a search.
Those seven headings also carry no icons (JL 260725): two of them had one and five did not, and a list where some entries are decorated reads as though the decorated ones were a different kind of thing.
Plain words are the consistent choice here because the drawer is one flat list of orientation, not a set of sections a reader navigates between.
The drawer is typeset as Content, not as chrome (JL 260725): its headings take Content's subsection size and weight with a rule between blocks, and its prose takes Content's size, colour, and leading.
It had been set in small accent-blue capitals over 12.5px muted grey, which is the page's metadata voice, and that voice was telling the reader this material was incidental when the venue contract and the required inputs are among the most consequential things on an S page.
The lead question is bold, which is what separates it from that prose: it is the one sentence always on stage and the handle for the drawer, so it should not read as the first line of what it opens.
A reader should be able to state the face's purpose and scope after reading Opening alone.

#### Boundary
Boundary says both what this face decides and where adjacent concerns belong.
Its `↪ Covered elsewhere` half must name the owning Q or S, because an exclusion without a destination leaves the reader stranded.

#### Stage Contract (S only)
Stage Contract is part of Opening: one collapsed disclosure after Why this matters and Stage Record, never its own page section (JL 260725).
It tells the reader which upstream outputs this stage requires and which writing contract governs it before showing the stage's own substance.
The managed block is generated from explicit `requires` and `style-from` metadata; it links and summarizes acceptance conditions without copying upstream Content.

### 2 · Diagram — reveal the shape
Diagram gives one visual account of the flow, comparison, before/after, or option set.
Its heading remains visible, but the figure starts hidden so a large canvas does not dominate the page before it is wanted.
Keep it only when opening it replaces or clarifies prose; decoration does not earn a section.
An Excalidraw share URL on its own line may be inserted whenever a figure is worth drawing on together: it renders as a live canvas plus a plain link, so colleagues can move boxes and comment in the drawing itself instead of describing edits in prose.
It is optional and additive, an ASCII figure alone remains a complete Diagram, and the plain link is what keeps the section readable when the canvas cannot load.
An ASCII figure has to survive being copied, because copying a face into chat or an email is a thing the board exists for.
Two trees drawn side by side do not: the column boundary is whitespace, it vanishes on paste, and the right column's rows land inside the left column's branches, so the figure asserts a structure that does not exist.
Stack them instead, one complete tree at a time; columns are safe only for short parallel lists where a wrong reading is obvious at a glance.

### 3 · Content — establish the substance
Content carries the material the face exists to establish after orientation.
It is required on S and optional on Q.
Each direct `###` heading becomes one named, collapsible subsection so readers can see the argument's parts before choosing which details to open.
On Q, Why this matters appears first; on S, an optional Stage Record moves to Opening when supplied and the remaining stage substance stays here.

#### Content holds the real thing only (S)
An S page's Content is the stage's own product and nothing else (JL 260725).
For a manuscript section page that means the section itself: its parts, its paragraphs, its prose, so a reader who opens Content reads the Results section rather than a folder of working material about it.
Three kinds of material that accumulate around a stage belong outside Content: the inherited venue or writing contract goes to Stage Contract inside Opening, settled flags and corrections go to Where we are because they report what is now true, and anything still owed goes to Items to Finish.
The heading names the stage for exactly this reason, reading `📚 Content · Main 7 §6 Results` rather than a subsection count: a count invites the page to accumulate boxes, while a name asks whether what follows really is the Results section.
That label is derived from the page title, so a page whose artifact carries its own number states both: the board index number and the artifact number are usually offset, and a title like `S Main 7 · §6 Results` stops them competing on the same screen instead of leaving the reader to work out which `7` is meant.

#### Heading levels inside Content
Two levels, and the depth is carried by the numbering rather than by the heading level (JL 260725).
Every division that holds content of its own is a direct `###`, so it folds independently; everything one step inside it is `####`, always.
On a manuscript section page that reads: each subsection is `### §6.1 Main Results` and each paragraph is `#### P1. …`, while a section with no subsections carries one division for itself, `### §1 Introduction`, with its paragraphs directly under it as `#### P1. …`.
The board folds exactly one level, so a page that nested subsections under a section-level `###` would collapse a whole ten-paragraph section into a single box and lose per-subsection folding; numbering the headings keeps the hierarchy legible without asking the renderer for a second fold level.
A section-level heading appears only when it holds prose of its own, which for a flat section is its paragraphs: a page never emits a division that would open onto nothing.
The rule is checkable, which is its point: the subsection count is the number of `###` headings whose number contains a dot, so a page can be compared against the venue blueprint's declared subsection count without reading a word of the prose.

#### A paragraph heading is not a group title
`####` renders as its own level: no icon, one size below a group title, its own spacing (JL 260725).
Before that it was flattened to `**bold**` on the way in, and a full-line bold is the group-title construct, so every paragraph arrived on the page wearing 🔹 and claiming to lead a run of items.
Deleting the icon would have hidden the mistake rather than fixed it, because the page was not over-decorating a paragraph: it was calling the paragraph something it is not.
The two levels now say different things and 🔹 means only what it always meant, a sentence that leads the items beneath it, which is why a real group title such as `🔹Settled Flags` still carries it.
A full-line `(…)` written directly under a paragraph heading is that paragraph's job, and it stays on stage in grey italic: it is the scan hook that lets a reader see what each paragraph does without reading the prose, so hiding it behind a click would cost a click per paragraph to recover the thing it exists for.
Only the line immediately after the heading is read that way, and the venue template caps it at roughly 80 to 120 characters, because a job line long enough to be mistaken for prose has stopped being a scan hook.

#### Content blueprint sources
An S page's Content is composed once, when `stage.py new` creates the page, from four layers:

1. The shared board shell fixes the visible page order but does not invent disciplinary content.
2. The stage template supplies the base subsection jobs, required artifacts, and gate conditions.
3. The venue template overlays reader expectations, section conventions, length, terminology, claim boundaries, and writing style.
   It may refine the stage blueprint but cannot erase a stage-required artifact or gate.
4. Previous Stage Contracts supply accepted inputs and visibly unresolved requirements.
   They are linked and summarized, never copied whole into the new page.

Resolution order is fixed: stage first, venue second, previous contracts third; the shell fixes layout only and never competes on content.
The creator materializes the result as explicit direct `###` headings with guide text in the new Markdown, and from then on the page owns those headings.
No later pass takes them back: `build.py` is render-only and never regenerates the blueprint, and `stage.py sync` refreshes only the managed Stage Contract block, never authored Content.
A stage or venue template edit after creation surfaces as an explicit staleness warning (the stored `contract-source-hash` no longer matches); a human decides what to adopt, and nothing rewrites silently.
Stage Contract remains a separate provenance and dependency layer, not a second copy of Content.

#### Sentence apparatus
A sentence can carry hidden apparatus: `>` lines written directly beneath it fold under the sentence, which shows a ⚑ badge until clicked.
> Note: this row is the demonstration; it was hidden until you clicked the sentence above.
> Link: `QA8-sentence.md` holds the ruling; inline-marker chips are its open item.

Typed lanes name what each attachment is, and review threads join the same drawer.
> Citation: a `\cite{TOADD}` placeholder resolves here once its key lands in the paper's .bib.
> Value: a `{VAL:? …}` placeholder surfaces here with the number it owes.
> Display: a DR id points at the `0-displays/` asset the sentence relies on.
> Q-consumer: a `[Q-Section-n]` bracket binds the sentence to its probe record.
> CC: threads like this one hide with the evidence they discuss.
> Note: this line was added FROM THE PAGE via the new POST /_board/sentence endpoint (smoke test, 260725).

A `>` run that opens a section with no sentence above it renders exactly as before, and the supporting folds never fold apparatus.

### 4 · Items to Finish — define the gap
Items to Finish is the testable definition of done, not a loose task list.
Every checkbox must describe a condition that another person can judge true or false, and the heading reports the completed count automatically.
On S, each Q-consumer remains one complete record and closes only after its answer is interpreted and integrated into Content.

### 5 · Where we are — report the present
Where we are states what is true now: counts, versions, decisions reached, and work still open.
It deliberately follows Items to Finish so readers learn the target before seeing implementation detail.
It summarizes progress without repeating the full evidence already held in Content or the checklist.

### 6 · Files — point to the work
Files names the small set of sources, generated outputs, and implementation files needed to continue the work, with one sentence explaining why each matters.
It is an action map rather than an exhaustive change list, and generated files must be labeled so nobody edits the wrong layer.

### 7 · Supporting folds — preserve history without blocking the read
Law, Lesson, Glossary, Discussion, Comments, and Log sit below the main reading path and begin folded.
They preserve rules, failures, vocabulary, deliberation, pinned remarks, and change history for readers who need them, while Opening through Files remains a clean first pass.
Retired Why here content is still parsed here for compatibility, but new rationale belongs in Question.

## Items to Finish
- [x] 🖼 Unframed
      A question opened on its own carries no border, no rounded corners, and no card background, so the content sits directly on the page.
      This began as JL's complaint on 260722 that the page felt boxed in compared with the slides `/html-ppt` produces.
      The fix was not cosmetic.
      A card frame quietly tells the reader they are looking at one item in a collection, which is precisely the wrong signal when the intent is that this single question owns the whole screen.
      Removing the frame, raising the title to 38px, and compressing the header into a thin marquee bar together changed what the page claims to be.
- [x] 👁 The gap is visible at a glance
      Someone who reads nothing but the headings still comes away knowing what is being asked and how far it is from done.
      This is what the auto-counted `5/6` in the `Items to Finish` heading buys: it turns a checklist into a progress signal that survives not being read.
      The assumption behind it is that most people scan a board rather than read it, so a page that only rewards full reading will be misjudged by everyone who scans.
- [x] ⏭ Paging without returning to the index
      Every screen ends with one line: `← previous · ☰ Index · next →`.
      The reason is behavioural rather than technical.
      When moving on requires a trip back to the index, people stop after one question instead of reading the run.
      Questions in a group are usually meant to be read in sequence, so forcing a detour between them works against the board's own structure.
- [x] 📐 Uneven lengths leave no big blank
      `Items to Finish` and `Where we are` stack vertically instead of sitting side by side.
      They were originally two columns, and JL asked for the change on 260723 for a plain reason: the two are almost never the same length, so one column always ended in a large patch of white space, and the shorter one looked finished when it had simply run out.
      Stacking also removes an accidental implication that the two are parallel or comparable, which they are not.
- [x] ✂️ Long passages can be chunked
      Body text uses `- short heading` with an indented explanation beneath it, and checklist entries can carry explanations too.
      The structure exists because the alternative, several unbroken paragraphs in a row, is unreadable on a projected screen and unscannable on a laptop.
      The heading stays on stage while the explanation folds, which is what makes it safe for an explanation to be long: it costs the scanning reader nothing.
- [x] 🔀 Order flipped to "intent first, status second"
      Q uses `Opening → Diagram → Content → Items to Finish → Where we are → Files`; S carries `Stage Contract` inside Opening as a collapsed disclosure.
      Opening carries the question lead and optional Boundary; on S it also carries Why this matters and an optional Stage Record.
      Diagram is a collapsed peer section.
      Before the 260723 redesign `Where we are` came first, so a reader with no background met implementation detail before learning what was being decided.
      That was this layout's single worst flaw, and it was invisible from the inside precisely because we already knew the goal: the detail read as context to anyone who had it and as noise to everyone else.
- [x] 🏷 Section names switched to plain language
      `Done when` became `Items to Finish` and `Now` became `Where we are`.
      The old names were compact but had to be learned; the new ones say what the section contains.
      Because renaming a section could have broken every existing board, `ALIAS` was added so one slot answers to several names, and old boards, including the ones with Chinese section names, regenerate untouched.
- [x] ✍️ Every question on the board rewritten to the new structure
      All 18 questions then on the board were converted, not just this one.
      Each got an actual question lead plus a rationale paragraph, `## Boundary`, and `## Files`.
      The renderer now places that rationale under Content rather than keeping it in Opening.
- [x] 🧩 One renderer accepts Q and S
      `Q*.md` and `S*.md` are recursively discovered, parsed into the same face data, rendered by the same page function, and accepted by comment/chat write-back.
      S faces carry a visible STAGE badge; question settlement and stage gates are counted separately so a gated lifecycle cannot inflate the ruling bar.
- [x] 🧭 Opening sits above Content
      Opening is the first visible section and contains the actual question lead plus optional Boundary.
      The compass marks orientation rather than implying that every face is an unanswered question.
      On Q, the rest of Question becomes Content's first "Why this matters" subsection.
      Older files keep `## Question`; `## Opening` is also accepted as its alias.
- [x] 🗂 Stage orientation moves into Opening
      On S, "Why this matters" sits inside Opening and starts collapsed like every other row there (JL 260725; it was initially open until that ruling).
      An optional exact direct `### Stage Record`, when supplied, is lifted from explicit Content into the same Opening and starts collapsed.
      All remaining stage subsections stay under Content, so status context moves up without mixing the substantive record into the lead.
- [x] 🖼 Diagram is its own collapsed section
      Optional Diagram is a peer section between Opening and Content.
      Its heading stays visible while the ASCII or Excalidraw figure remains hidden until the reader clicks it.
      Native `<details>` preserves the no-script fallback: the figure remains in the HTML and can still be opened with all JavaScript stripped.
- [x] 📋 S requirements and writing style are visible before Content
      Stage Contract renders inside Opening, collapsed, from explicit `requires` and `style-from` metadata.
      `stage.py` owns only the managed block, build stays read-only, and stale upstream contracts appear as warnings rather than silently drifting.
- [x] 🔠 Content's heading tree renders as two distinct levels
      A division folds on its own, a paragraph heading is its own level with no icon, and the job line under it reads as grey italic rather than as prose.
      The test is that the three are told apart on the page without reading them, which is what failed before: paragraphs were flattened to bold, bold is the group-title construct, and 113 paragraphs across the MISQ board were therefore announcing themselves as sentences that lead a run of items.
      Verified on that board after the change: 113 paragraph headings, 82 job lines, and 31 group titles, with 🔹 left only on the 31.
      The depth is carried by the numbering rather than by a third heading level, so per-division folding survives on the longest pages.
- [ ] 🧬 S Content can be instantiated from stage and venue templates
      The creation path must resolve the stage template as the base blueprint, overlay the venue's section and writing constraints, add previous-stage requirements, and write the resulting direct `###` headings into the new Markdown.
      The composition rule is now specified here and mirrored in QA2; `stage.py new` still needs the template-resolution input and materializer.
- [x] 🔎 Q-consumer moved into Items to Finish
      A stage consumer is a recognizable checklist record retaining its Q id, Description, Reason, Probe, and Answer.
      Its box closes only after the answer landed, was interpreted, and was woven into Content; deferred closes only after a forward pointer is recorded.
- [x] 🧪 A zero-background reader understands one page in one pass
      Hand one Q face and one S face to a fresh agent with no prior context and have it retell what is being asked, what Content establishes, what counts as done, and where things stand.
      Passed 260725 after three fresh-context reads.
      The first two recovered the template but exposed stale filenames, ambiguous gates, missing finish records, and contradictory asset paths; those were repaired.
      The third recovered QD2's full ruling, S4's 13-record closure map, live asset truth, appendix handoff, and Q/S closure semantics with no blocking ambiguity.
- [x] 📚 Every visible section explains its eventual purpose
      Content now names the intended reader outcome for Opening, Diagram, Content, Items to Finish, Where we are, Files, and the supporting folds.
      These meanings were moved out of Law because they describe how to read the page, not a hidden implementation constraint.

## Where we are
Partial.
The shared Q/S reading path and inherited Stage Contract are implemented.
The next piece is creation-time Content composition: stage template as the base blueprint, venue template as the reader/section/style overlay, and previous contracts as accepted and unresolved inputs.
That rule is specified here and in QA2, but `stage.py new` does not yet materialize template- derived `###` headings.

- 260725 JL · 🚪 The lead question became the door, and Opening stopped folding
  A version earlier the same day hung the disclosure on the section name, so the page showed a shut row reading only "🧭 Opening" with the ruling's scope invisible inside it.
  JL called it back: nothing in Opening folds from its heading, and the question sentence is what you click.
  This restores the 260724 design rather than inventing one, and the `.qlead` caret CSS it needs had been sitting unused in the stylesheet the whole time.

- 260725 JL · 🔠 Content got a second heading level, and 🔹 got its meaning back
  JL asked why every paragraph on the MISQ pages carried a 🔹 and why the parenthetical line under it read like prose.
  Both came from one line: `####` was flattened to bold before rendering, and a full-line bold is the group-title construct, so a paragraph was being rendered as a sentence that leads a run of items.
  `####` is now its own level with no icon, the job line under it is grey italic, and 🔹 marks only real group titles again.

- 260725 JL · 🧬 Content became a composed creation-time blueprint
  Stage supplies the base structure, Venue refines it for the target outlet, and previous Stage Contracts contribute accepted inputs and open requirements.
  The resolved headings belong to the new Markdown; build remains render-only.

- 260725 JL · 📋 Stage Contract moved inside Opening
  JL ruled the contract is orientation, not a page section of its own.
  It renders as one collapsed disclosure inside Opening, after Why this matters and Stage Record; the standalone section between Opening and Diagram is gone.

- 260725 JL · 📋 Stage Contract became an S-only page layer
  Required Inputs and Writing Style first shipped as a layer between Opening and Diagram; the move into Opening the same day supersedes that placement.
  Managed markers stay in Markdown but do not render; the author's Content remains a separate, protected layer.

- 260725 JL · 📚 Section purposes moved into Content
  JL asked for each Q-webpage section to explain what it is ultimately for.
  QA4 now exposes seven numbered Content subsections, which the page counts as eight because the automatic Why this matters joins them; the S-only Stage Contract is explained inside Opening's subsection, matching where it renders (JL 260725).

- 260725 JL · 🧭 Stage orientation moved into Opening
  JL asked to place S0's Why this matters and Stage Record in Opening and replace its question mark.
  Opening now uses a compass; S stage orientation moves there while Q rationale stays under Content.

- 260725 JL · 🖼 Diagram became a collapsed peer section
  JL asked for Diagram to read as a section and stay hidden before clicking.
  The renderer now places a native `🖼 Diagram` disclosure between Opening and Content; only its heading is visible initially.

- 260725 JL · ❓ Question became Opening at the visual level
  JL asked for the first page layer to read like an opening before Content, Items to Finish, and Where we are.
  The renderer keeps the question lead and Boundary in Opening, moves the explanatory remainder into Content, and preserves source compatibility.
  The later Diagram ruling gives Diagram its own collapsed row.

- 260725 CC · 🧪 Cold-read acceptance passed
  Two fresh readers found real content-ledger ambiguities rather than template failures; the board was revised after each pass.
  A third reader recovered Question, Content, every finish/defer record, current state, asset truth, and closure semantics for both workflow kinds, then returned PASS.

- 260725 JL · 🧩 Q and S combined into one template
  JL asked to put Question above Content and use Q-consumer as Items to Finish.
  The renderer, shared template, board specification, and MISQ lifecycle board now follow that shape.
  The workflow semantics stay distinct: Q settles a ruling; S passes a human stage gate.

- 260722 JL · 🃏 The page stopped looking like a card
  JL asked for pages like the slides `/html-ppt` produces, not something boxed in, and focus mode landed the same evening.
  Border, rounded corners, and card background were removed so the content sits directly on the page, the title went to 38px, and the header was compressed into a thin marquee bar.
  The mechanism is pure CSS, `:target` plus `:has()`, so a question fills the screen without any script running.
  The reason this was not cosmetic: a card frame quietly tells the reader they are looking at one entry in a collection, which is the wrong signal when the intent is that this single question owns the screen.
- 260723 JL · 🧱 Goal and status stacked instead of side by side
  `Items to Finish` and `Where we are` were sitting in two columns, and JL asked for them stacked.
  The two are almost never the same length, so one column always ended in a large patch of white space, and the shorter one read as finished when it had simply run out.
  Stacking also removes an accidental implication that the two sections are parallel or comparable, which they are not: one is a target and the other is a position.
- 260723 CC · 🔀 Order flipped to intent first, sections renamed
  On-stage order became `Question → Boundary → Diagram → Items to Finish → Where we are`, and `Done when` and `Now` were renamed to `Items to Finish` and `Where we are`.
  Before this pass the page opened with `Where we are`, so a reader with no background met implementation detail before learning what was being decided.
  That was the layout's worst flaw and it was invisible from the inside, because anyone who already knew the goal read that detail as context rather than noise.
  The renames were a separate, smaller fix: the old names were compact but had to be learned, and the new ones say what the section holds.
- 260723 CC · 🚧 Boundary added, and Why here retired
  A new `## Boundary` section states what a question covers and what is covered elsewhere, while `## Why here` was absorbed into the Question rationale and now renders under Content.
  Boundary was added because readers kept judging a question against expectations carried over from a neighbouring one, for example asking why QA4 says nothing about writing quality when that is QA5's subject.
  Naming the question that does cover the excluded part turned out to matter more than stating what this one covers.
  `Why here` went away in the same pass so that the opening section could orient a reader without help from anything below it.
- 260723 CC · 🔗 ALIAS so old boards keep working
  One slot now answers to several section names, so `Done when`, `Items to Finish`, and the original Chinese names all resolve to the same block.
  This was a precondition for the rename rather than a convenience added afterwards.
  Without it, renaming two sections would have silently emptied those blocks on every board written before the change, and nobody would have noticed until the next time an old page was regenerated.
- 260723 CC · ✍️ All 18 questions rewritten to the new structure
  Every question then on the board was converted, not just this one.
  The acceptance check inspected the generated page for the `.bnd` and `.fls` blocks rather than grepping the markdown for section names.
  An earlier substring check had been fooled by text sitting inside an ascii fence, and QA2 passed that way while actually missing the section, so the check now looks at what was rendered.
- 260724 JL · 🌐 Everything on the board in English
  JL ruled that board markdown, generated pages, and artifacts are written in English.
  The questions and copied template guidance are English.
  Internal skill specifications may remain bilingual because they are not rendered board content.
- 260724 JL · 🖱️ Item shape: heading, one sentence, then [more details]
  An item now shows its heading and a one-sentence summary on stage, with the long explanation behind a visible `[more details]` button.
  Two complaints produced this.
  First, the only cue that an item could be opened was a small `▸` triangle, so readers did not know anything was there: the fold was working and invisible at the same time.
  Second, a heading alone gives too little to decide whether to open it.
  The first indented line in the markdown is now the visible summary and the remaining lines are the folded detail, styled a shade lighter so the two are distinguishable at a glance.
- 260725 CC · 🧪 Cold-read acceptance passed
  Fresh agents recovered what is asked, what Content establishes, every finish condition, current state, and the distinct Q/S closure semantics.
  The Opening revision was cold-read twice: the first read found this stale historical status sentence; after correction, the second clean-context read returned PASS.

## Files
- `build.py`
  The generator entry.
  Q/S discovery and parsing live under `src/`; output remains self-contained.
- `src/common.py`
  Q/S filename grammar, recursive discovery, and safe write-back path validation.
- `src/parse.py`
  Classifies Q as `question` and S as `stage` while preserving one parsed face shape.
- `src/page_question.py`
  The shared renderer, including S Stage Contract before Diagram and Content.
- `src/page_board.py`
  Separate question-settlement and stage-gate summaries.
- `ref/q-template.md`
  The file copied for every new question.
  Its section order and guide sentences must match this question, or new questions drift back.
- `ref/board-form.md`
  The full spec: §4 section↔page mapping + required/optional, §8 on-stage order and the three-level hierarchy. **Division of labour:** §4 holds the *technical* mapping (name → CSS class → required/optional); this question's `## Content` holds the *reader-facing purpose* of each section; `## Law` holds the rules that constrain them.
  The earlier attempt to keep an HTML skeleton here went stale and was removed, and that trap is what the split avoids.
- `SKILL.md`
  The shared-face rules and the distinct Q/S workflow semantics.
- `stage.py`
  Explicit writer for managed S requirements and writing-style contracts.
- `0-lifecycle/`
  Complete consumer: 14 Q rulings + 28 S lifecycle pages on one board.
- `board.html`
  Generated. **Never hand-edit**: change the md and regenerate.

## Law
- On-stage order is fixed: intent first, status second
  Q uses `Opening → Diagram → Content → Items to Finish → Where we are → Files`.
  S carries `Stage Contract` inside Opening (collapsed), then follows the same sequence.
  Opening contains the question lead and optional Boundary; S still requires explicit Content for its own substance.
- One face grammar, two workflow kinds
  Q is a ruling and closes by settlement; S is a lifecycle stage and closes at its human gate.
  They share the renderer and reading order, not their counters or governance.
- Opening always precedes Content
  The face must orient a zero-background reader before presenting substantive material.
  Opening carries the actual question lead and its scope.
  S also carries Why this matters, an optional Stage Record, and the Stage Contract there, all collapsed; Q carries Why this matters under Content.
  An optional collapsed Diagram row separates Opening from the remaining Content.
- The lead question is the door, and Opening itself never folds (JL 260725)
  The 🧭 Opening heading and the lead sentence are always on stage; clicking the sentence opens Boundary and, on S, Why this matters, Stage Record, and Stage Contract.
  A version that hung the fold on the section name instead was reverted the same day: a shut row reading only "🧭 Opening" gives the reader nothing to decide with, and the 260724 Law about invisible folds applies to a section heading exactly as it applies to an item.
  Put the handle on the thing a reader wants explained, which is the question itself, not on the label above it.
  One door, and behind it everything is flat: no row inside the drawer folds again, because a second layer of ▸ makes the material read as missing rather than as filed, which is exactly how JL described it.
  The drawer's headings carry no icons, because two of the seven did and five did not, and partial decoration reads as a type distinction that is not there.
  The lead keeps its original markup, a `<p class="qlead">` inside the summary, so the serif face and the 18px/21px sizing keep matching; moving that class onto the summary silently dropped both rules.
- S consumers live in Items to Finish
  Keep the Q id and Description / Reason / Probe / Answer together inside one checklist record.
  Tick only after answer, interpretation, and Content integration; summarize rather than duplicate in Where we are.
- S Content holds the stage's real product only (JL 260725)
  Content is the thing the stage makes, so on a manuscript page it is the section itself and nothing else.
  Inherited contract material (the venue contract, the writing style, upstream requirements) belongs to Stage Contract inside Opening; settled flags and corrections belong to Where we are; open work belongs to Items to Finish.
  The Content heading names the stage (`📚 Content · Main 7 §6 Results`) instead of counting subsections, because a name is a test the page can fail and a count is not.
- Content carries two heading levels, and the number carries the depth (JL 260725)
  Every division that holds content of its own is a direct `###` and folds on its own; everything one step inside it is `####`, with no exceptions.
  Depth is read off the numbering, `§6` against `§6.1`, rather than off the heading level, because the board folds exactly one level and a third level would cost per-subsection folding on the longest pages.
  A division is emitted only when it holds prose of its own, so a flat section carries one `### §1 Introduction` over its paragraphs and a subsectioned one goes straight to `### §6.1`, and no page opens a box onto nothing.
  This makes the shape checkable without reading the prose: the subsection count is the number of `###` headings whose number contains a dot.
- A paragraph heading is not a group title (JL 260725)
  `####` is its own level with no icon; a full-line `**bold**` is a group title and keeps 🔹.
  Flattening `####` to bold made every paragraph claim to lead a run of items, which is a false statement about the page rather than surplus decoration.
  A full-line `(…)` immediately under a paragraph heading is that paragraph's job and stays on stage in grey italic, because a scan hook behind a click cannot be scanned.
- An ASCII figure must survive being copied
  Copying a face into chat or an email is a use the board is for, so a figure whose meaning lives in whitespace is broken by its own purpose.
  Never draw two trees side by side: the column boundary disappears on paste and the right column's rows read as branches of the left one.
- S Content is composed at creation and owned by the page (JL 260725)
  `stage.py new` resolves the stage template first, the venue overlay second, and previous Stage Contracts third, then writes the result as direct `###` headings with guide text.
  Render never regenerates them, sync touches only the managed Stage Contract block, and a stage or venue template edit after creation surfaces as a staleness warning instead of a silent rewrite.
- `## Question` is one question lead + one rationale paragraph
  The lead is the actual prompt in Opening.
  The paragraph carries why it is hard, what breaks if left open, and what it affects; it renders as "Why this matters" inside Opening for S and as Content's first subsection for Q.
- Every item explanation is a paragraph, not a clause (JL 260724)
  The `- short heading` + indented explanation pattern applies to list and checklist items, and the explanation is a real paragraph: what it means, what happened, what we understand so far, and why it ended up this way.
  Question itself uses the lead-plus-rationale shape above, not item bullets.
- `## Boundary` is `✅ Covered here` / `↪ Covered elsewhere` (JL 260724)
  The second half is the one that earns the section, so it must always name the question that does cover it; a bare exclusion tells the reader nothing and reads as a refusal.
  The labels were originally "This question owns" and "This question does not own"; JL rejected that wording on 260724 as stiff and legalistic, and the `↪` replaced `❌` because the line's job is to redirect the reader, not to deny them.
- Foldable items carry a visible `[more details]` control (JL 260724)
  Any item with an explanation renders its heading followed by a small `[more details]` pill, which reads `hide` once open.
  Before this, the only cue that an item could be opened was a small `▸` triangle, and readers simply did not know there was anything beneath; the fold was working and invisible at the same time.
  Implemented purely in CSS via `::after`, so the zero-script invariant holds: strip every script and the paragraphs are still in the DOM and still open on click.
- Focus = a slide, not a card
  Strip border, corners, background; content flows directly; `min-height` fills the screen.
  Title 38px, lead 21px, body 16px, width 1000px.
  Pure CSS (`:target` + `:has()`).
- What is on stage, what folds
  On stage: title; compass Opening with the question lead; the Diagram, Content, Items to Finish, Where we are, and Files headings.
  Behind the lead question's single click, shown flat: Boundary, S Why this matters, the optional S Stage Record, and the S Stage Contract with its Required Inputs, Writing Style, and venue section.
  Collapsed by default elsewhere: the entire Diagram body, item explanations, and code blocks (folded to one line `</> code · N lines`).
  Sunk into the bottom fold: Why here · Discussion · Comments · Law · Lesson · Glossary · Log.
- Every section folds from its own heading (JL 260725)
  Content, Items to Finish, Where we are, and Files became native disclosures, the mechanism Diagram already used, so a long page can be collapsed down to its section names.
  They open by default because the reading path must survive a reader who never clicks; Diagram alone still starts shut.
  Opening is the one section that does not fold from its heading, because a page whose first section can be shut can be opened showing nothing; its lead sentence carries the fold instead.
  Folding is display only: the text stays in the DOM, so Ctrl-F, the section ⧉ copy, and the zero-script fallback are all unaffected, and the auto-counted `7/9` stays readable on a folded Items to Finish.
- An expand-all beside every section heading
  Opens/closes all items and code in that section at once; pure enhancement: with scripts stripped, each item still opens individually.
- Long questions scroll: never truncate, never split; no 16:9 lock, follow window height
  Locking the aspect ratio would be projection's business; projection is settled (one file, two modes) in `ref/board-form.md` §8.
- A real space after the id in the headline
  So copying the headline yields `QA4 Single…`, not `QA4Single…`.
- Renaming sections must go through ALIAS; old boards must never break
  One slot, many names; old boards regenerate without a single edit.

## Lesson
- "Settled" can be overturned by one sentence
  This question was closed ✅ on 260723 with every finish line ticked, and was knocked back to 🟡 the same day by a single remark from JL: a zero-background reader could hardly understand the page.
  Nothing about the work was wrong; the checklist was.
  It contained eight conditions about structure and not one about the person the structure exists for, so it could be completed in full while the actual goal went unmet. **A checklist that omits the real user proves nothing when fully ticked**, and the failure is invisible from the inside, because the author always reads the page with the context already in their head.
- Order beats wording for readability
  The same sentences, with `Where we are` above the goal versus below it, read like two different documents.
  Before the redesign the page opened with implementation detail; afterwards it opened with the question.
  No prose was rewritten in that pass and yet the page became readable.
  The general form: when a page is hard to follow, reorder before rewriting, because wording improvements applied to a bad order are largely wasted effort.
- Long explanations are free when they fold
  Item explanations are collapsed by default while their headings stay visible, which changes the economics of writing them.
  A scanning reader pays nothing for a paragraph they do not open, so the usual pressure to compress an explanation into a clause disappears, and compressed clauses are exactly what strips out the reasoning and the history that make a decision reviewable later.
  The rule that follows: write the heading for the scanner and the paragraph for the person who stops.
- A new body level inherits none of the fixes the old one accumulated
  The paragraph heading shipped with the same base spacing as the group title but without the patch that focus mode had needed, so `.q:target .ph` at (0,3,0) outranked `.ph:first-child` at (0,2,0) and the first paragraph after a section heading opened 22px below it instead of 2px.
  JL saw it as inconsistency rather than as a gap, which is the more useful description: it only appeared where a section began with a heading, so some sections read tight and others split open with no visible cause, and an inconsistency with no visible cause is what makes a page feel unreliable rather than merely imperfect.
  The same bug had already been found and patched once for group titles, and the patch was invisible to whoever added the next level.
  Both are now handled by one selector so they cannot drift apart again, and the general form is worth keeping: when a construct is split into two, every accumulated exception has to be split with it, because exceptions live where nobody looks for them.

## Glossary
unframed: no border, rounded corners, or card background wrapping the content; it sits directly on the page.
group title: a full-line bold sentence in the body that leads a run of items; shown with 🔹 or the author's own emoji.
division: any Content part that folds on its own, written as a direct `###`; a manuscript subsection is one, and so is a flat section standing over its own paragraphs.
paragraph heading: a `####` line naming one paragraph inside a division; it carries no icon and is one size below a group title, which is the distinction that was invisible while it rendered as bold.
job line: the full-line `(…)` directly under a paragraph heading, saying what that paragraph does; it stays on stage in grey italic as a scan hook.

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
260725 · Opening's drawer switched from chrome type to Content type (JL: "the display here is not good"): headings now 15px/650 with a rule between blocks and prose at Content's size and colour, matching `.csec>summary` and `.cbody p` exactly; the lead question went bold so the handle reads apart from what it opens
260725 · Opening's drawer headings lost their icons (JL: make them read consistent): `🚧 Boundary` and `📋 Stage Contract` were the only two of seven with one, so all seven are now plain words. The `✅ Covered here` / `↪ Covered elsewhere` pair inside Boundary was left alone: it is a 260724 ruling of JL's own and lives in the markdown of all 78 faces
260725 · Opening's drawer went flat (JL "I don't want to have >" / "why other information are gone"): Why this matters, Stage Record and the Stage Contract's three parts render as plain `.fh` headings like Boundary always did, so one click shows Required Inputs, Writing Style and the venue section instead of three more shut rows; the lead's `<p class="qlead">` markup was restored byte-for-byte so the serif face and 18px/21px sizing match the original again
260725 · Opening stopped being a fold and the lead question became the door (JL "no > in the Opening, it will always be there; but the question statement will be clickable"): `🧭 Opening` is a plain heading again, the lead sentence is a `<summary>` with the caret pinned right, and Boundary / Why this matters / Stage Record / Stage Contract open beneath it. Restores the 260724 `.qlead` design, whose CSS was still in the stylesheet unused
260725 · `####` became a first-class paragraph heading (no 🔹, its own level) and the full-line `(…)` under it became the job line (grey italic, on stage); Law, Glossary, the Content sketch and the finish record now carry the two levels, which until now existed only in `src/body.py` and `assets/board.css`
260725 · Content heading example became `📚 Content · Main 7 §6 Results`: an S title may carry the artifact's own number when it is offset from the board index, so the two numbers stop competing
260725 · Law added: an ASCII figure must survive being copied, so two trees are never drawn side by side (the column boundary is whitespace and disappears on paste)
260725 · Lesson added: a new body level inherits none of the fixes the old one accumulated, from `.q:target .ph` (0,3,0) outranking `.ph:first-child` (0,2,0) and opening a 22px gap under section headings in focus mode
260725 · Every section (Content, Items to Finish, Where we are, Files) folds from its own heading like Diagram; all open by default, expand-all and the ⧉ copy no longer toggle the section
260725 · Opening rows all start collapsed on S (JL "all the things here should be hidden"): Why this matters no longer auto-opens, and neither does the contract's first part; the lead question is the only thing on stage
260725 · Law added: S Content holds the stage's real product only (venue contract to Stage Contract, settled flags to Where we are, open work to Items to Finish); Content heading now names the stage instead of counting subsections
260725 · Diagram documented as optionally carrying an Excalidraw share URL, so a figure can be discussed and redrawn in place
260725 · Stage Contract explanation merged into Opening's Content subsection (JL: not a new section in the webpage); subsections renumbered to seven; sentence hover tint added
260725 · Sentence apparatus demo added to Content (QA8 v1: `>` lanes fold under the sentence they follow)
260725 · Reading pass (JL): Stage Contract moved inside Opening as a collapsed disclosure (not a separate section); one sentence per source line swept across all prose; face prose switched to a serif reading stack
260725 · Content blueprint sources tightened per handoff.md: `stage.py new` named as the composer, resolution order fixed (stage → venue → previous contracts), sync-protection of authored Content and the `contract-source-hash` staleness signal made explicit; matching Law record added
260725 1630 · QA3 (projection) retired as a face; three cross-refs repointed from QA3 to the settled projection ruling in ref/board-form.md §8, bottom-nav example neighbor QA3 → QA2
260725 · S Content composition specified: stage blueprint + venue overlay + previous contracts; automation remains open
260725 · S pages gained a visible Stage Contract between Opening and Diagram; managed markers stay hidden
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
