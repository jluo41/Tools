# Page overall: the shared Q/S layout
state: 🟡 PARTIAL · the order and identity are settled; the carve into seven faces awaits JL
owner: CC
method: one page grammar, one fixed on-stage order; each section's own rules live on its QAa face
session: cd5e7f5f-15c7-49ba-a97f-bdf90ef3f534
## Question
When one Q ruling or S lifecycle stage is opened and it alone fills the screen, how should that shared page be arranged so that someone with **no background at all** can read top to bottom once and know: what is being asked, what the substantive content is, what counts as done, and where things stand now?

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
  `board.html`'s **single-page focus mode** for Q and S: the fixed on-stage order, what is on stage / what folds, one layout serving two workflows, the group-title marker, and the Board identity mark.
  The source template `ref/q-template.md` and the whole-file authoring contract are also here.
- ↪ Covered elsewhere
  Each section's own rules live on its face: Opening `QAa1` · Diagram `QAa2` · Content `QAa3` · Items to Finish `QAa4` · Where we are `QAa5` · the folds `QAa6`.
  The sentence and everything attached to it: the `QAb` group.
  Projection (one file, two modes: scroll to read / one screen per page) is settled in `ref/board-form.md` §8, not here.
  Whether each page's **prose is well written**, and what checks that the page still renders this layout, is `QA9`.
  Q and S workflow contracts belong to their owning skills.

## Diagram

```
Focus mode: one page owns the whole screen. Read top to bottom —
intent first, status second.

  ═══ marquee bar  ≈110px, always present  (/haipipe-board · spine · close) ═══

  S-Main-7       🔴 OPEN      STAGE   🧠 JL
  S Main 7 · §6 Results                     — same title hierarchy as Q

  🧭 Opening         a plain heading, never a fold: it is always there
  the question lead ⌄ the actual prompt, always on stage, and it is the door:
                     click it and everything that explains it opens beneath
       Boundary      covered here / covered elsewhere
       Why it matters in here, Q and S alike (JL 260729)
       Stage Record  S only · optional · in here when supplied
       Stage Contract S only · Required Inputs · Writing Style · Venue
       (FLAT: one click shows all of it, no ▸ inside, and no icons on these
        headings either — they are plain words so the seven read as one list)
  ▸ 🖼 Diagram       its own section; nothing shows until clicked
       ▾ ▧ ASCII        opens with the section: the figure you almost always want
       ▸ ✏️ Excalidraw   one more click; shut, its lazy iframe never loads
  📚 Content         only what the author wrote; shape is the page's own
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
  ← QAa1       ☰ Index        QAa3 →        — pinned to the bottom

  unframed = no border · no rounded corners · no card background
```

```
copy ref/q-template.md                     source → the rendered page
┌──────────────────────────────────────────────────────────────────┐
│ # title · state · owner              required → headline/header  │
│ method                               optional → header            │
├──────────────────────────────────────────────────────────────────┤
│ ## Question  lead                    required → 🧭 Opening        │
│                rationale                      Q: 📚 Why first     │
│                                               S: Opening Why     │
│ ## Boundary                           advised → inside Opening    │
│ requires · style-from · provides       S only → 📋 contract       │
│ ## Stage Contract                      S only → inside Opening,   │
│   managed block + authored (venue contract lives here)  collapsed │
│        every Opening row starts SHUT: lead question only on stage │
│ ## Diagram                           optional → collapsed peer    │
│   ascii fence(s)                              → ▧ ASCII, open     │
│   bare excalidraw URL on its own line         → ✏️ Excalidraw, shut│
│ ## Content                       Q optional/S required → 📚       │
│        S: the stage's real product only, heading NAMES the stage  │
│   stage template                   → base subsection blueprint    │
│   venue template                   → reader/section/style overlay │
│   previous contracts               → accepted/open requirements  │
│   ### Stage Record           S optional → Opening, collapsed     │
│   ### other subsection                         Content, collapsed │
│   > Citation: / > Value: / …       → folded under their sentence  │
│ ## Items to Finish                   required → 🎯 auto-counted   │
│ ## Where we are                      required → 📍 present state  │
│ ## Files                              advised → 📎 action map     │
├──────────────────────────────────────────────────────────────────┤
│ Law · Lesson · Glossary · Discussion · Comments · Log            │
│                                  optional → supporting folds      │
└──────────────────────────────────────────────────────────────────┘
```

/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/board.excalidraw&frame=QAa0

## Content
### 1 · The base page and its Content variants
One frame, many kinds: the base page belongs to this skill (the metadata head, the fixed on-stage order, the folds, the sentence grammar, the renderer), and a page KIND redefines only what `## Content` holds and how it is composed.
JL stated the rule in chat on 260729: the kinds today are Question and Stage, Display and Task are the candidates, Skills is already a third, and "the only thing changed is the content structure, other things won't change".
A variant ships in the skill set that owns its domain, not here: `haipipe-paper-stage` already does exactly this for S pages, since its stage templates are what `stage.py new` composes into Content, and a future `haipipe-paper-display` or a task variant extends the same way, a new blueprint under the same frame.

#### The kinds, counted against the code
- Question, the base kind
  Content optional and free-shaped since 260729 (`QAa3` §3); nothing composes it, the author does.
- Stage, the first variant, and it already lives in another family
  Content required, composed at creation by `stage.py new` from the stage template, the venue overlay, and previous Stage Contracts; the templates live under `paper/1-lifecycle/haipipe-paper-stage`, so the extension pattern JL names has already shipped once.
- The Skill roster, a generated variant
  `skillpage.py` derives Content from the unit's own definition file inside a managed span and its Log from the CHANGELOG; the frame is untouched, which is why it needed no renderer work.
- Display, a candidate, not yet a kind
  Today `S-Display-*` on the MISQ lifecycle board is a naming family of ordinary S pages; it becomes a kind the day a display blueprint ships as its own door, and `paper/1-lifecycle/4-display/ref/` is where that material sits.
- Task, a candidate
  A task folder's plan, build, execute, report contract is a ready-made blueprint; nothing exists yet.

#### What a variant may declare, and what it may never touch
A variant declares three things: its Content blueprint and who composes it at creation, the typed records it contributes INTO frame sections (S puts a Stage Contract row in Opening and Q-consumer records in Items to Finish), and its closure semantics (Q settles, S gates).
It may never add, remove, or reorder sections, change the folds, change the sentence grammar, or touch the render machinery.
The mechanical proof that the base stays ignorant of its variants already exists one layer down: `src/dialect_paper.py` opens with "THIS MODULE IS DELETABLE", and `build.py` asserts that every board not declaring `dialect: paper` renders byte-identical with it gone.
One reconciliation is JL's to confirm: his sentence says only Content changes, and the S kind visibly reaches Opening and Items to Finish today; this face reads those as the variant's Content contract SHOWING in other sections, provenance in Opening and acceptance in Items, contributions into the frame rather than changes of it.

### 2 · The source template and the whole-file contract
`ref/q-template.md` is the deliverable: adding a page of either kind means copying it, and it carries all 14 recognized `##` sections with one guide line each.
The metadata block above the sections is required for identity: title, state, and owner become the index row and page header; method is optional.
The first emoji on the `state:` line is the machine status and must be one of ✅, 🟡, 🔴, or ⏸️; readable detail may follow it, so `✅ PINNED · MISQ 2026` remains the same machine state as `✅ SETTLED`.
S additionally declares explicit `requires`, `style-from`, and `provides`; dependency is never inferred from Pages order.
The eight source-to-render mappings live in the second Diagram fence above.

#### The Files source
List only the sources, outputs, and implementation files needed to continue, with one line explaining each role.
Mark generated files explicitly so the reader does not hand-edit the wrong layer.

#### The whole-file source laws
Section names must be kept verbatim: `build.py` takes the whole string after `## ` as the key, so `## Question (required)` silently yields nothing; required/optional markers go into the first body line, never the heading.
Requiredness is workflow-aware: both kinds require title, `state`, `owner`, `## Question`, `## Items to Finish`, `## Where we are`; `## Stage Contract` and `## Content` are required for S; Q deletes Stage Contract and may omit Content; `## Boundary` and `## Files` are strongly advised.
Renaming a section must go through `ALIAS`, fold order is fixed by `build.py`, and Log is reverse-chronological.

### 3 · Files: point to the work
Files names the small set of sources, generated outputs, and implementation files needed to continue the work, with one sentence explaining why each matters.
It is an action map rather than an exhaustive change list, and generated files must be labeled so nobody edits the wrong layer.

### 4 · The Board identity mark
The Board mark is separate from the group-title emoji problem above.
It identifies the Board itself rather than classifying a content group, so it does not wait for the 20 mislabelled bold lines to be repaired.
JL chose the four-page mark on 260726: four overlapping rounded pages make the Board, and a transparent speech-shaped aperture makes discussion part of the same silhouette.

The source is `assets/board-mark.svg`.
`src/page_board.py` inlines that source beside the generated title and encodes the same bytes as the SVG favicon, so a built `board.html` still has no asset dependency.
The mark is 42px on the index and 24px in focused-page mode; the title remains the primary label.
Its geometry lives only in the SVG, while eight `--board-mark-*` tokens in `assets/board.css` control the four two-stop gradients.
That split keeps palette changes exact and reversible without letting different Boards drift into different marks.

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
      `Q*.md` and `S*.md` are recursively discovered, parsed into the same page data, rendered by the same page function, and accepted by comment/chat write-back.
      S pages carry a visible STAGE badge; question settlement and stage gates are counted separately so a gated lifecycle cannot inflate the ruling bar.
- [x] 🧭 Opening sits above Content
      Opening is the first visible section and contains the actual question lead plus optional Boundary.
      The compass marks orientation rather than implying that every page is an unanswered question.
      On Q, the rest of Question became Content's first "Why this matters" subsection; superseded 260729, when it joined Opening's drawer on Q too.
      Older files keep `## Question`; `## Opening` is also accepted as its alias.
- [x] 🗂 Stage orientation moves into Opening
      On S, "Why this matters" sits inside Opening and starts collapsed like every other row there (JL 260725; it was initially open until that ruling).
      An optional exact direct `### Stage Record`, when supplied, is lifted from explicit Content into the same Opening and starts collapsed.
      All remaining stage subsections stay under Content, so status context moves up without mixing the substantive record into the lead.
- [x] 🖼 Diagram is its own collapsed section
      Optional Diagram is a peer section between Opening and Content.
      Its heading stays visible while the ASCII or Excalidraw figure remains hidden until the reader clicks it.
      Native `<details>` preserves the no-script fallback: the figure remains in the HTML and can still be opened with all JavaScript stripped.
- [x] ▧ Diagram splits into ASCII and Excalidraw, ranked not paired
      The section renders `▧ ASCII` open and `✏️ Excalidraw` shut, so the figure arrives with the section and the canvas costs one more click.
      The source keeps one plain `## Diagram`; `split_diagram` in `src/page_question.py` partitions it on the same bare-URL rule `src/body.py` already uses, and a URL inside a fence stays in the figure.
      Verified on this board 260726: 30 Diagram sections, 27 with an ASCII half, 28 canvases, 2 reading "No canvas attached yet", 0 checker errors, and the 🖌 attach button relocated into the canvas row.
- [x] 📋 S requirements and writing style are visible before Content
      Stage Contract renders inside Opening, collapsed, from explicit `requires` and `style-from` metadata.
      `stage.py` owns only the managed block, build stays read-only, and stale upstream contracts appear as warnings rather than silently drifting.
- [x] 🔠 Content's heading tree renders as two distinct levels
      A division folds on its own, a paragraph heading is its own level with no icon, and the job line under it reads as grey italic rather than as prose.
      The test is that the three are told apart on the page without reading them, which is what failed before: paragraphs were flattened to bold, bold is the group-title construct, and 113 paragraphs across the MISQ board were therefore announcing themselves as sentences that lead a run of items.
      Verified on that board after the change: 113 paragraph headings, 82 job lines, and 31 group titles, with 🔹 left only on the 31.
      The depth is carried by the numbering rather than by a third heading level, so per-division folding survives on the longest pages.
- [x] 🔎 Q-consumer moved into Items to Finish
      A stage consumer is a recognizable checklist record retaining its Q id, Description, Reason, Probe, and Answer.
      Its box closes only after the answer landed, was interpreted, and was woven into Content; deferred closes only after a forward pointer is recorded.
- [x] 🧪 A zero-background reader understands one page in one pass
      Hand one Q page and one S page to a fresh agent with no prior context and have it retell what is being asked, what Content establishes, what counts as done, and where things stand.
      Passed 260725 after three fresh-context reads.
      The first two recovered the template but exposed stale filenames, ambiguous gates, missing finish records, and contradictory asset paths; those were repaired.
      The third recovered QD2's full ruling, S4's 13-record closure map, live asset truth, appendix handoff, and Q/S closure semantics with no blocking ambiguity.
- [x] 📚 Every visible section explains its eventual purpose
      Content now names the intended reader outcome for Opening, Diagram, Content, Items to Finish, Where we are, Files, and the supporting folds.
      These meanings were moved out of Law because they describe how to read the page, not a hidden implementation constraint.


- [ ] 🧩 `ref/q-template.md` learns the 260729 additions
      The 🧩 Skills item shape inside Where we are (`QAa5`) and the QA0 board-map guide block (`QA0`); this face owns the template since QA2 merged into the QAa group.
- [ ] 🧠 JL confirms the carve: seven faces own the sections, this face owns the order
      Carved 260729 on JL's design (QAa group, one face per page section): Opening `QAa1` · Diagram `QAa2` (absorbing the former QA4a) · Content `QAa3` · Items to Finish `QAa4` · Where we are `QAa5` · folds `QAa6`, with the source template `QA2` moving into the group.
      Six open items moved to `QAa3` with the grammar they block on; every ticked item above stays here, because the history happened on this page.
- [ ] 🧬 JL confirms the base/variant model (§1)
      The page is a base owned by this skill; a kind redefines only Content and ships under its consumer family, `haipipe-paper-stage` today, `haipipe-paper-display` and a task variant as candidates.
      The one point to rule: whether S's Stage Contract row in Opening and its Q-consumer records in Items to Finish count as the variant's Content contract showing elsewhere, which is §1's reading, or as frame exceptions to pull back.
- [x] 🪪 The Board has one shared identity mark
      JL selected the overlapping four-page mark on 260726.
      It now lives as one transparent SVG in the skill, renders beside every generated title, and supplies the browser favicon without adding an external file dependency.
      Original plus three exact-geometry palette studies are recorded under `fig/`; changing the shipped palette touches CSS tokens, not the SVG geometry.

## Where we are
**Carved 260729 into the QAa group: this face keeps the fixed order, the two-workflow rule, and the Board mark; each section's own rules now live on its face.**
The shared Q/S reading path and inherited Stage Contract are implemented.
The shared Board identity mark is also implemented: one SVG source, one inlined header instance, one data favicon, and CSS-owned palette tokens.
Four palette studies preserve the same geometry so JL can change color without reopening the mark itself.
The open work moved with its sections: creation-time Content composition and the group-title cleanup and icon items are `QAa3`'s now.

- 260729 JL · 🧬 The page became a base with Content variants
  JL named the model in chat: Page is the base, Question, Stage, Task, Display, and Skills are variants, only the Content structure changes, and other skill sets extend it, `haipipe-paper-stage` or `haipipe-paper-display`.
  §1 records it against the code: two kinds and one generated variant already render through one frame, the stage blueprint already ships from the paper family, and the deletable paper dialect is the standing proof that the base never learns a variant.
  The five sibling QAa faces are marked frame the same round, so each section now says whether a kind may touch it.
- 260726 JL · 🪪 The Board gained its own mark
  JL chose the interlocking four-page concept and asked for it in generated `board.html` and in the `haipipe-board` skill.
  The production version is a hand-authored transparent SVG rather than the 1254px raster: `src/page_board.py` inlines it beside the title and reuses it as a data favicon, while `assets/board.css` owns the palette.
  The Original, Clinical Teal, Warm Editorial, and Graphite Aurora studies change color only, making the comparison honest.
- 260726 JL · ▧ Diagram's two halves stopped being one undifferentiated body
  JL asked for an ASCII subsection open by default and an Excalidraw subsection behind a click.
  The two were already described separately in `§2` and rendered together in one block, so the prose ranked them and the page did not.
  What the ranking buys beyond taste: a shut `<details>` never displays, so twenty-eight lazy canvas iframes stopped loading on open.
  The source did not change, which is why nothing had to be migrated: `split_diagram` partitions the rendered section on the bare-URL rule the body renderer already owned.
- 260726 JL · 🎨 QD4 merged in, and the count stopped flattering itself
  JL: "I think we can merge this one to QA4 ... I think most content in the QA4 is already done".
  Both halves of that are right, and they pull against each other. This page was 17/18 before the merge and is 17/23 after it, because the icon question was parked on another page while the grammar it depends on lived here.
  That is the same shape as the QA6 and QA7 merge earlier the same day: a split let one page look finished while the thing it defined had an unfinished half somewhere else.
  What moved: the group-title marker, the 36/5/11/20 count, and QD4's four forks. What stayed behind: nothing, QD4 is deleted.
  One tension worth recording rather than hiding: the eventual endpoint is live-layer work and the QD group owns the live layer. It sits here because the icon is a layout marker and its blocking prerequisite is this page's own `§3` rule, so the ruling and the thing it rules are together.

- 260726 JL · 🖼 Diagram's Excalidraw half got written down as a mechanism
  Two lines said a share URL "may be inserted" and rendered "as a live excalidraw plus a plain link", which told a reader it existed without telling them how to do it.
  JL asked for the how: `§2` now splits into the ASCII figure the section owes and the optional excalidraw, and the excalidraw paragraph gives the exact rule the code enforces, one URL alone on its own line, plus what it renders, why the fallback link is not redundant, and why empty is the normal state.
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
  Classifies Q as `question` and S as `stage` while preserving one parsed page shape.
- `src/page_question.py`
  The shared renderer, including S Stage Contract before Diagram and Content.
- `src/page_board.py`
  Separate question-settlement and stage-gate summaries, plus Board-mark and favicon inlining.
- `assets/board-mark.svg`
  The one hand-authored source for the Board identity mark.
- `assets/board.css`
  The Board-mark palette tokens and its index/focused sizes, alongside the rest of the shared page styling.
- `fig/board-mark-palettes.svg`
  The four exact-geometry palette studies; the PNG beside it is the rendered review sheet.
- `ref/q-template.md`
  The file copied for every new question.
  Its section order and guide sentences must match this question, or new questions drift back.
- `ref/board-form.md`
  The full spec: §4 section↔page mapping + required/optional, §8 on-stage order and the three-level hierarchy. **Division of labour:** §4 holds the *technical* mapping (name → CSS class → required/optional); this question's `## Content` holds the *reader-facing purpose* of each section; `## Law` holds the rules that constrain them.
  The earlier attempt to keep an HTML skeleton here went stale and was removed, and that trap is what the split avoids.
- `SKILL.md`
  The shared-page rules and the distinct Q/S workflow semantics.
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
- One page grammar, two workflow kinds
  Q is a ruling and closes by settlement; S is a lifecycle stage and closes at its human gate.
  They share the renderer and reading order, not their counters or governance.
- Opening always precedes Content
  The page must orient a zero-background reader before presenting substantive material.
  Opening carries the actual question lead and its scope.
  Why this matters sits in Opening's drawer on Q and S alike (JL 260729; until then Q carried it under Content); S adds an optional Stage Record and the Stage Contract, all collapsed.
  An optional collapsed Diagram row separates Opening from the remaining Content.
- The lead question is the door, and Opening itself never folds (JL 260725)
  The 🧭 Opening heading and the lead sentence are always on stage; clicking the sentence opens Boundary and, on S, Why this matters, Stage Record, and Stage Contract.
  A version that hung the fold on the section name instead was reverted the same day: a shut row reading only "🧭 Opening" gives the reader nothing to decide with, and the 260724 Law about invisible folds applies to a section heading exactly as it applies to an item.
  Put the handle on the thing a reader wants explained, which is the question itself, not on the label above it.
  One door, and behind it everything is flat: no row inside the drawer folds again, because a second layer of ▸ makes the material read as missing rather than as filed, which is exactly how JL described it.
  The drawer's headings carry no icons, because two of the seven did and five did not, and partial decoration reads as a type distinction that is not there.
  The lead keeps its original markup, a `<p class="qlead">` inside the summary, so the serif page and the 18px/21px sizing keep matching; moving that class onto the summary silently dropped both rules.
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
- Diagram renders as ▧ ASCII open over ✏️ Excalidraw shut (JL 260726)
  The two halves are ranked, not paired: the figure is what a reader came for, and the canvas is where colleagues draw together, so equal weight would misdescribe them.
  The split is a RENDER decision and the source stays one plain `## Diagram`, which is why no page had to be migrated and a page that later gains a canvas splits itself.
  A bare Excalidraw URL alone on a line is the canvas and every other line is the figure; a URL inside a fence stays in the figure, where its author drew it.
  The canvas row is emitted even when empty because the 🖌 attach button lives there, and scriptless it still says truthfully that no canvas is attached.
- An ASCII figure must survive being copied
  Copying a page into chat or an email is a use the board is for, so a figure whose meaning lives in whitespace is broken by its own purpose.
  Never draw two trees side by side: the column boundary disappears on paste and the right column's rows read as branches of the left one.
- S Content is composed at creation and owned by the page (JL 260725)
  `stage.py new` resolves the stage template first, the venue overlay second, and previous Stage Contracts third, then writes the result as direct `###` headings with guide text.
  Render never regenerates them, sync touches only the managed Stage Contract block, and a stage or venue template edit after creation surfaces as a staleness warning instead of a silent rewrite.
- `## Question` is one question lead + one rationale paragraph
  The lead is the actual prompt in Opening.
  The paragraph carries why it is hard, what breaks if left open, and what it affects; it renders as "Why this matters" inside Opening on Q and S alike (JL 260729).
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
  Behind the lead question's single click, shown flat and in this order: Boundary, Why this matters (Q and S alike, JL 260729), the optional S Stage Record, and the S Stage Contract with its Required Inputs, Writing Style, and venue section.
  Collapsed by default elsewhere: the entire Diagram body, item explanations, and code blocks (folded to one line `</> code · N lines`).
  Inside Diagram there is one more ranking: opening the section shows ▧ ASCII and leaves ✏️ Excalidraw shut.
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

- One face, both projections (JL 260729)
  The page markdown and the rendered page are one thing seen twice, so each QAa face owns its section in BOTH: what an author writes and what the reader sees.
  A render decision and its authoring contract change in the same edit, on the same face, and `ref/q-template.md` follows in that same change.
  This replaces the retired two-face sync law ("QA2 changes with QA4"), whose only job was keeping apart what belongs together.

## Lesson
- In the usage comment of the template, never start a line with `state:` / `owner:` / `method:`
  The meta parser swallows any line whose first word is one of these; the first draft corrupted the status exactly this way; writing `· state …` dodges it.
- Stale self-contradictions in the template must be purged
  The template still said "newest Log lines at the bottom" long after reverse order was settled, exactly the kind of stale sentence a zero-background reader spots first.
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
> JL: could group-title icons be assigned in realtime by an LLM?
>> CC0723: yes, serve.py already has an LLM. But "realtime" forks: button-triggered (recommended: cheap, controllable) against auto-on-save (expensive, edits your md while you type). build.py stays dumb; clever work goes to the LLM layer.
>> CC0726 (proposal, JL's to accept): the three forks may already be answered by precedent. Every write affordance built on this board since is button-triggered and none overwrites what a human wrote: the comment layer, `QA8`'s ➕ lane, `QC2`'s ＋Q and ＋Group, and `QD7`'s 🖌 excalidraw, which replaces only its own line. Scope has the same answer four times: the page the button sits on. If that reads right, trigger, overwrite policy and scope close as written down rather than as newly decided, leaving the model choice and the build. Not ticked, because QD4 warned about `QD1` being overturned after I picked for you.
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
>> CC0725: Opening now uses a compass. On S pages, Why this matters is open there and an exact Stage Record is collapsed there; Q pages keep Why this matters under Content.
> JL: Content should explain what every section in the Q webpage is eventually for: 1 Opening, 2 Diagram, and so on.
>> CC0725: moved the section meanings out of Law and into seven numbered Content subsections. The visible reading path is explained first; the lower historical sections are grouped as Supporting folds.

## Log
260729 · The base/variant model added as Content §1 (JL, in chat): the page is a base and a page kind is a Content variant shipping under its consumer family; the kinds counted against the code, the variant contract stated, the five sibling faces marked frame, and the Stage Contract / Q-consumer reconciliation left as JL's open item
260729 · Content cleaned on JL's ask ("I don't want the carved-to sections, keep the headings simple"): the seven carved-to stubs deleted, since Boundary already names each face, and the four real sections renumbered §1-§4 with plain headings
260729 · Why this matters unified into Opening for Q (JL, decided on QAa1); Content became per-page flexible (decided on QAa3); this face's Diagram and Law updated to match
260729 · QA2 (the source template face) merged into the QAa faces on JL's call: the source and the render are one subject per face, so each face gained a "The source" division, and this face took the whole-file contract, the template items, the source->render mapping table, and the Q_STUB item. The two-face sync law retired with it; QA2's file is archived with its history
260729 · Renamed QA4 -> QAa0 and carved into the QAa group on JL's design (one face per page section): §1 Opening -> `QAa1`, §2 Diagram -> `QAa2` (which also absorbed QA4a), §3 Content + §8 group-title marker -> `QAa3`, §4 -> `QAa4`, §5 -> `QAa5` (plus the new 🧩 Skills subsection convention), §7 -> `QAa6`. Six open items moved to `QAa3`; all ticked items and the full history stay here. The word "ruling" gives way to "decision" board-wide (JL 260729). Earlier Log lines below cite the old id and the old § numbers; they are history and were not rewritten
260726 2230 · `🖼 Diagram` split into `▧ ASCII` (open) + `✏️ Excalidraw` (shut) per JL: `split_diagram` + `render_diagram` in `src/page_question.py`, `.dsub` styling in `assets/board.css`, and `wireXcal` retargeted at `.dsub-x > .dsubb` so the 🖌 attach button lives in the canvas row; source markdown unchanged, so 30 sections re-rendered with 0 checker errors and 28 lazy iframes stopped loading on open; QA2 and `ref/q-template.md` updated in the same pass
260726 · QD4 merged in (JL): `§8` added with the marker, the 36/5/11/20 count and the blocked automation; QD4's four items absorbed plus a new cleanup item that blocks them; 17/18 -> 17/23, which is the honest number now that the icon question sits with the grammar it depends on
260726 · `§2 Diagram` split into two paragraphs (JL: how do we add the excalidraw link and embed it?): the ASCII figure the section owes, and the optional excalidraw whose default is empty; the excalidraw paragraph now carries the one-URL-alone-on-a-line rule from `src/body.py`, the 440px / 520px render, the `↗ Open in Excalidraw` fallback, and the reason the fallback and the ASCII both stay
260725 · Opening's drawer switched from chrome type to Content type (JL: "the display here is not good"): headings now 15px/650 with a rule between blocks and prose at Content's size and colour, matching `.csec>summary` and `.cbody p` exactly; the lead question went bold so the handle reads apart from what it opens
260725 · Opening's drawer headings lost their icons (JL: make them read consistent): `🚧 Boundary` and `📋 Stage Contract` were the only two of seven with one, so all seven are now plain words. The `✅ Covered here` / `↪ Covered elsewhere` pair inside Boundary was left alone: it is a 260724 ruling of JL's own and lives in the markdown of all 78 pages
260725 · Opening's drawer went flat (JL "I don't want to have >" / "why other information are gone"): Why this matters, Stage Record and the Stage Contract's three parts render as plain `.fh` headings like Boundary always did, so one click shows Required Inputs, Writing Style and the venue section instead of three more shut rows; the lead's `<p class="qlead">` markup was restored byte-for-byte so the serif page and 18px/21px sizing match the original again
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
260725 · Reading pass (JL): Stage Contract moved inside Opening as a collapsed disclosure (not a separate section); one sentence per source line swept across all prose; page prose switched to a serif reading stack
260725 · Content blueprint sources tightened per handoff.md: `stage.py new` named as the composer, resolution order fixed (stage → venue → previous contracts), sync-protection of authored Content and the `contract-source-hash` staleness signal made explicit; matching Law record added
260725 1630 · QA3 (projection) retired as a page; three cross-refs repointed from QA3 to the settled projection ruling in ref/board-form.md §8, bottom-nav example neighbor QA3 → QA2
260725 · S Content composition specified: stage blueprint + venue overlay + previous contracts; automation remains open
260725 · S pages gained a visible Stage Contract between Opening and Diagram; managed markers stay hidden
260725 · QA2/QA4 alignment pass made optional Boundary and optional S Stage Record explicit; fresh Q/S template render passed with Stage Record both present and absent
260725 · Section purposes moved from Law into seven numbered Content subsections: Opening, Diagram, Content, Items to Finish, Where we are, Files, and Supporting folds
260725 · Opening icon changed to compass; S Why this matters and Stage Record moved into Opening
260725 · Diagram became a peer-level native details section, collapsed by default
260725 · Opening fresh-agent loop passed: first read verified the hierarchy but caught a stale QA4 status sentence; after correction the second clean-context read returned PASS
260725 · visible hierarchy first simplified to Opening → Content → Items to Finish → Where we are; later the same day Diagram became its own collapsed peer section
260725 · QA4 settled after the required fresh-agent loop: two ambiguity-finding reads drove corrections; the third returned PASS with the full QD2/S4 model intact
260725 · QA4 widened from a single-question page to the shared Q/S page; Content inserted after Diagram, Q-consumer moved into Items to Finish, separate workflow counts shipped, and the MISQ board migrated to 14 Q + 8 S
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
