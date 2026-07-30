# Shared Q/S source template
state: 🟡 PARTIAL
owner: CC
method: mirror QA4 and materialize S Content from stage, venue, and upstream contracts

## Question
When I open an empty ruling page such as `QA9-xxx.md` or lifecycle stage page such as `S-Main-4-theory.md`, what must I write so the generated page follows QA4?
On this Board, Q means a question whose answer becomes a ruling, while S means one stage of a paper lifecycle whose completion requires its own gate.
The generator only recognizes a fixed set of section names, so misspell one and that section **silently disappears, no error**; silent failure is the hardest kind to debug.
Without a clear template, everyone writes a different-shaped page and the page turns messy, while colleagues and future agents touch this file every day.
QA2 is the authoring side of QA4's reading contract: when QA4 changes Opening, Content placement, or the on-stage order, this template must follow in the same change or newly written Q and S pages drift back to the old shape.
For a new S page, filling the template should not begin from a generic empty Content block.
The creator should resolve the owning stage template, overlay the venue template, then bring in the accepted and unresolved requirements named by previous Stage Contracts.
It writes the result as explicit `###` headings so the page remains understandable and editable without rerunning the source templates at render time.

## Boundary
- ✅ Covered here: the inside of one Q or S source file, including required and optional sections and the shape of `ref/q-template.md`.
- ↪ Covered elsewhere: `QA1` owns folder membership, `QAa0` owns the rendered hierarchy (its sections are the QAa faces since 260729), and `QA9` owns readability and post-change checks.

## Diagram

```
copy ref/q-template.md                     source → QA4 rendered page
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

/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/fig/board.excalidraw&frame=QA2

## Content
The metadata block above the sections is required for identity: title, state, and owner become the index row and page header; method is optional.
The first emoji on the `state:` line is the machine status and must be one of ✅, 🟡, 🔴, or ⏸️; readable detail may follow it, so `✅ PINNED · MISQ 2026` remains the same machine state as `✅ SETTLED`.
S additionally declares explicit `requires`, `style-from`, and `provides`; dependency is never inferred from Pages order.
The eight mappings below mirror QA4's visible sequence.

### 1 · Opening source: Question plus optional Boundary
Write `## Question` as one actual question lead followed by one rationale paragraph.
The lead renders in Opening.
On Q, the rationale becomes Content's first Why this matters subsection; on S, it becomes a collapsed Why this matters row inside Opening.
An optional `## Boundary` joins the same Opening and redirects excluded concerns to their owning Q or S.

### 2 · Stage Contract source: S requirements and writing style
S pages use `stage.py new` or `stage.py sync` to generate the managed part of `## Stage Contract` from explicit `requires` and `style-from` metadata.
The managed markers protect authored Content; an author-owned `### Provides` after the markers states the compact output inherited downstream.
Anything else hand-written also belongs after the markers, which is where a manuscript page's venue contract lives: `replace_managed` rewrites only the marked span, so an authored subsection survives every sync (verified across the MISQ pages on 260725).
The whole section renders as one collapsed row inside Opening, so it is a source section without being a page section.
Q pages delete this section and the S-only metadata.

### 3 · Diagram source: an optional collapsed peer
Write one useful ASCII figure and, optionally, one Excalidraw share link under `## Diagram`.
QA4 renders the section between Opening and Content with the body hidden until clicked.
Delete the whole source section when the visual adds no understanding.

Write ONE `## Diagram` section, not two.
The renderer splits it into `▧ ASCII`, which opens with the section, and `✏️ Excalidraw`, which takes one more click (QA4 §2, JL 260726).
The rule that decides the halves is the one already governing the body: a bare Excalidraw URL alone on its own line is the canvas, and every other line is the figure.
So do not add `### ASCII` or `### Excalidraw` headings here; a `###` inside `## Diagram` is not a recognized construct and would render as ordinary prose inside the figure half.
Put the URL below the figure with nothing else on the line, exactly as before, and a URL written inside a fence stays in the figure where it was drawn.

### 4 · Content source: Q optional, S required
Use direct `###` headings for coherent substantive parts; each becomes one collapsible Content subsection.
On S, an optional exact direct `### Stage Record` is orientation metadata and moves into Opening collapsed when supplied, while every other subsection remains under Content.
Do not maintain a second live copy of stage substance.
Content holds the stage's real product and nothing else: the inherited contract goes to `## Stage Contract`, settled flags and corrections to `## Where we are`, and anything still owed to `## Items to Finish`.
The rendered heading names the stage rather than counting subsections, so a name that does not describe what a reader finds there is the signal that something has crept in.

Write one sentence per source line, because the page gives each prose line its own row.
A sentence may carry apparatus: `>` lines written directly beneath it fold under that sentence, with typed lanes naming the attachment (`> Citation:`, `> Value:`, `> Display:`, `> Check:`, `> Q-consumer:`, `> Link:`, `> Source:`, `> Note:`) and `> JL:` / `> CC:` threads joining the same drawer.
Adjacency is the only binding, so a lane placed after a paragraph attaches to whatever line precedes it; the full grammar is `QA8`.

For S creation, use this precedence:

1. Stage template defines the base jobs, artifacts, and gate.
2. Venue template refines reader expectations, section conventions, length, terminology, claim boundaries, and style without deleting stage-required work.
3. Previous Stage Contracts add accepted inputs and unresolved requirements.
4. The creator writes the resolved structure into this page as explicit direct `###` headings.

These are creation inputs, not three live backing documents.
`build.py` only renders the materialized Markdown.
`requires` and `style-from` continue to expose dependency and writing provenance in Stage Contract, while Content remains author-owned.

### 5 · Items to Finish source: testable completion
Write `## Items to Finish` as checkboxes that another person can judge true or false.
The rendered heading counts them automatically.
On S, each former Q-consumer stays together as one recognizable record and closes only after its answer is interpreted and integrated into Content.

### 6 · Where we are source: the present state
Write one concise current-state paragraph followed by dated change items when useful.
Report what is true now with numbers where numbers exist; do not restate the full checklist or every S-consumer answer.

### 7 · Files source: the action map
List only the sources, outputs, and implementation files needed to continue, with one line explaining each role.
Mark generated files explicitly so the reader does not hand-edit the wrong layer.

### 8 · Supporting source sections: optional history
Law, Lesson, Glossary, Discussion, Comments, and Log are optional source sections rendered as supporting folds below the main path.
Retired `## Why here` remains parse-compatible for old boards but must not be added to new files; its job now belongs to the Question rationale.

## Items to Finish
- [ ] 🧩 The template's guide text learns the 260729 additions
      The 🧩 Skills item shape inside Where we are (owned with `QAa5`), and the QA0 board-map page every board opens with (owned with `QA0`).
      A template change is a graduation, so it follows JL's confirmation of the QAa carve, never precedes it.
- [x] 📄 A shared blank template under `ref/` that can be copied as-is
      `ref/q-template.md` can seed either `Q<group><number>-<slug>.md` or `S-<Family>-<unit>-<slug>.md`.
      It carries all 14 recognized `##` sections, and its usage comment is dropped at build time rather than leaking into the page.
- [x] 🧭 One guide line at the top of every section: what to write here, and how long
      The first line of each section's body IS the guide sentence (what + how long); you overwrite it as you fill in.
- [x] 🏷 Mark which sections are required and which optional
      Title, state, owner, Question, Items to Finish, and Where we are are required for both kinds.
      Method and Diagram are optional; Boundary and Files are optional but strongly advised.
      Explicit Stage Contract and Content are required for S; Q deletes Stage Contract and may omit Content.
      Markers stay in guide text, never in a recognized heading or metadata key.
- [x] 🔀 Adding either workflow kind begins from the same source
      Copy the template and rename it without consulting an existing board.
      The usage comment explains Q and S filenames, their distinct closure semantics, and the optional exact `### Stage Record` and Q-consumer rules that apply only to S.
- [x] 🧱 Template follows QA4's current shared-page hierarchy
      The Q mapping is `Opening → Diagram → Content → Items to Finish → Where we are → Files`; S carries `## Stage Contract` inside Opening as a collapsed disclosure (JL 260725).
      Question is a lead plus rationale paragraph, Boundary is optional inside Opening, Q rationale starts Content, S rationale sits in Opening, an optional S Stage Record joins it when supplied, and Supporting folds stay below the main read.
      On S every Opening row now starts collapsed, so the template says the lead question is the only thing on stage.
- [x] 🧾 Template carries the rulings of 260725, so new pages cannot drift back
      `ref/q-template.md` was updated the same day the rulings landed: one visible hierarchy for both kinds with Stage Contract inside Opening, all Opening rows collapsed on S, the Content law with its three destinations, the named Content heading, one sentence per source line, and a worked sentence-apparatus example in the Content skeleton.
      This item exists because the template is the only file a new page inherits from.
      A ruling recorded on QA4 but missing from the template is a ruling that survives exactly until the next person copies the skeleton, which is how the old three-bullet Question shape kept reappearing after it had been retired.
- [ ] 🧬 S creation materializes a composed Content blueprint
      Given a stage template, venue template, and previous Stage Contracts, the creation path writes the resolved direct `###` headings into the new S Markdown.
      QA2 and the copyable template now state the precedence; `stage.py new` still needs to accept and materialize those template inputs.
- [x] 🧪 A zero-background agent can create one valid Q and one valid S
      Given only `ref/q-template.md`, a fresh agent must fill one Q and one S, then explain where every source section renders, which sections differ in requiredness, and why the two workflow kinds do not share closure semantics.
      Passed 260725 through two fresh-context runs.
      The first rendered a Q and S correctly but exposed that Stage Record's optionality was only implied; after the wording was repaired across QA2, QA4, and the template, a second reader rendered one Q plus S variants with and without Stage Record and found no material contradiction.

- [ ] 🧬 The ＋ button's stub is generated from this template, not written beside it
      `Q_STUB` in `serve.py` is hand-written and was 4 sections against the template's 14; it now agrees on the required and advised ones, and the two definitions still exist.
      This closes when the stub is derived from `ref/q-template.md` at runtime, keeping the required and advised headings, dropping the guidance prose, and listing the rest as a note.
      Until then the failure mode is the one JL hit: the template changes and the button does not.

## Where we are
QA2 and `ref/q-template.md` match the page as it renders: Stage Contract sits inside Opening, Content holds the stage's real product, and sentence apparatus uses typed lanes.
Two code gaps remain: `stage.py new` does not yet materialize the composed Content blueprint, and the index ＋ button still uses a separately maintained `Q_STUB`.

- 260726 JL · ▧ QA4 split Diagram in two and this side did not change
  The rendered section now ranks `▧ ASCII` above a shut `✏️ Excalidraw`, and the authoring contract stayed exactly one `## Diagram`.
  That is the interesting half of the ruling for this page: a QA4 change usually forces a template change, and this one did not, because it was a decision about arrangement rather than about what an author writes.
  What did need saying is the trap it creates: an author who reads the rendered page and infers `### ASCII` / `### Excalidraw` headings would write markdown the renderer does not read, so §3 and a new Law now forbid it in advance.
- 260726 JL · ➕ The ＋ button was a second definition of a new page, and now follows this one
  JL opened a question from the index and found no `## Diagram` in it, and asked whether this page should change.
  It should not. `## Diagram` is in the template, this page already rules it optional, and `QA4 §2` rules how it renders; nothing was violated by its absence.
  What was violated is the line above it here: Boundary and Files are "optional but strongly advised", and `Q_STUB` in `serve.py` wrote neither. That stub shared nothing with `ref/q-template.md` but the section names it happened to reuse, 4 of the template's 14.
  Fixed by making the stub follow this page rather than sit beside it: Boundary and Files are written out, and the optional sections are listed in an author note, because nobody can choose a section they never learn exists.
  The durable version is generating the stub FROM the template so the two cannot disagree again. Not done; it is the item below.
- 260726 CC · 🕳 Author notes were not dropped, though the template promised they were
  `ref/q-template.md` tells authors a note "is dropped at generation either way". The only strip lived in the Stage Contract path, so a note written anywhere else came out as escaped `&lt;!--` prose on the page.
  It went unnoticed because the template's own notes sit above the first `## `, where nothing renders. Nobody had put one in a section until the stub menu needed to.
  Worse than cosmetic: `split_sections` reads any line starting `## ` as a heading, including one inside a comment, so a note listing `## Diagram` was torn in half and left a phantom section behind.
  `parse.strip_notes` now removes notes before sectioning, protects fenced blocks so a figure may still show one on purpose, and keeps `<!-- haipipe:... -->` for the contract markers. All seven boards in the repo rebuild unchanged.

- 260725 JL · 🧬 S Content composition added
  Stage owns the base blueprint, Venue overlays outlet-specific structure and style, and previous contracts contribute accepted and unresolved inputs.
  The result becomes explicit page-owned `###` headings rather than a live render-time merge.

- 260725 JL · 📋 New S pages inherit explicit contracts
  `requires`, `style-from`, and `provides` now drive a managed Stage Contract.
  `stage.py` creates or refreshes it, while build remains read-only and reports stale upstream sources.

- 260725 CC · 🧪 Shared-template acceptance passed
  A first clean reader built and rendered one Q and one S, recovering the visible order, rationale placement, Content requiredness, and distinct closure semantics; it found one mild ambiguity about whether Stage Record was required.
  After “S-only, optional” was made explicit, a second clean reader rendered three pages and confirmed that Stage Record moves into Opening collapsed when supplied and leaves no placeholder when absent.

## Files
- `ref/q-template.md`
  The deliverable itself: adding a question means copying it.
- `src/common.py`
  `ALIAS` / `sec()` (moved out of build.py in QB5's src/ split) decide which section names are recognized; a misspelled name silently yields nothing.
- `ref/board-form.md`
  §4 section↔page mapping + required/optional.
- `stage.py`
  Creates and synchronizes only the managed inherited-contract block.
- `QA4-pagelayout.md`
  The rendered page contract this source template must mirror.

## Law
- Section names must be kept verbatim
  build.py takes the whole string after `## ` as the key (`ln[3:].strip()`), so `## Question (required)` is not found.
  Required/optional markers therefore go into the first body line, never the heading line.
- Requiredness is workflow-aware
  Both kinds require `# title`, `state`, `owner`, `## Question`, `## Items to Finish`, and `## Where we are`.
  `## Stage Contract` and `## Content` are required for S; Q deletes Stage Contract and may omit Content.
  `## Boundary` and `## Files` are optional but strongly advised.
- State has one machine token and optional human detail
  The first emoji is exactly one of ✅, 🟡, 🔴, or ⏸️ and is the only value read by the renderer and checker.
  Text after it may explain the page-specific state but may not replace or contradict the emoji.
- On-stage order is fixed
  Q uses `Opening → Diagram → Content → Items to Finish → Where we are → Files`; S carries `Stage Contract` inside Opening as a collapsed disclosure.
  Intent stays before status.
- S Content composition has fixed precedence
  Stage template supplies the base blueprint; Venue may refine but not erase required stage work; previous Stage Contracts supply accepted and unresolved inputs.
  The resolved headings are written into the new Markdown and become author-owned.
- One `## Diagram` in the source, two subsections on the page (JL 260726)
  The author writes one section; the renderer ranks its halves as `▧ ASCII` open over `✏️ Excalidraw` shut.
  Never write `###` subheadings inside `## Diagram` to force the split: the partition is computed from the bare-URL rule, and a `###` there is not a recognized construct.
  This is the general shape of the bargain QA2 keeps making with QA4: the source stays something a person types, and arrangement is the renderer's job, which is also why this ruling migrated zero pages.
- QA2 changes with QA4
  QA2 is the authoring contract and QA4 is the rendered reading contract.
  Any QA4 ruling that changes section placement, requiredness, or visible order must update `ref/q-template.md` and this page in the same change, followed by a fresh-context Q/S creation test.
- Fold order is fixed by build.py
  On the page it is always Why here · Discussion · Comments · Law · Lesson · Glossary · Log, regardless of file order.
- Renaming a section must go through ALIAS
  One slot recognizes several names (`Done when` = `Items to Finish`, `Now` = `Where we are`, the old Chinese names still work), so old boards regenerate without touching a single character.
- Log is reverse-chronological
  Newest on top (`sort_log` reverse=True, both in md and on the page).

## Lesson
- In the usage comment, never start a line with `state:` / `owner:` / `method:`
  The meta parser (parse_q) swallows any line whose first word is one of these; the first draft corrupted the status exactly this way; writing `· state …` dodges it.
- The top four lines are outside the `##`-section required/optional rules
  The first template only marked the `##` sections, so a cold-reading agent had to guess whether state/owner were required.
  Only after adding them to the usage comment was it clear.
- Stale self-contradictions in the template must be purged
  The template still said "newest Log lines at the bottom" long after reverse order was settled at 1120, exactly the kind of stale sentence a zero-background reader spots first.

## Glossary
Q: a ruling page that closes when its finish checklist is complete.
S: a lifecycle stage page that closes when its stage-specific human gate passes.
stage template: the reusable base jobs, artifacts, and gate for one lifecycle stage.
venue template: the outlet-specific reader, section, length, terminology, and style constraints overlaid on a stage template.
previous Stage Contracts: accepted inputs and unresolved requirements explicitly named by upstream S pages.
materialize: write the resolved blueprint into the new page as ordinary, page-owned Markdown rather than merging it only while rendering.
composed Content blueprint: the direct `###` headings produced from the stage template, venue template, and previous Stage Contracts.
required: without it the source page is invalid even if the generator does not raise an error.
optional: delete the whole section, including its heading, when unused.

## Discussion
> JL: I want to understand whether QA4 and QA2 are aligned or not.
>> CC0725: they were aligned in intent, and the live template had most current behavior, but QA2 still documented the older Q-only page: no Content in its diagram or Law, Question shown as a question-mark lead, and no S-specific requiredness. QA2 now mirrors QA4 as the source side of one shared Q/S contract; the fresh Q/S creation test is the remaining gate.

## Log
260726 2230 · followed QA4's Diagram split (JL): the source still carries ONE `## Diagram`, and §3 plus a new Law now say so explicitly, including the trap of hand-writing `### ASCII` / `### Excalidraw` headings that the renderer would not read; `ref/q-template.md`'s Diagram guidance updated in the same pass
260726 · aligned the authoring contract with the renderer: the first state emoji is the four-value machine status, while a readable suffix such as `PINNED · MISQ 2026` may add page-specific detail
260726 · ＋ button's stub brought in line with this page (JL asked why a generated Q had no Diagram): Boundary and Files written out per the strongly-advised rule, optional sections offered as an author note; `parse.strip_notes` added because notes were never actually dropped and a `## ` inside one created a phantom section
260725 · `ref/q-template.md` brought up to the day's rulings: one hierarchy for both kinds, Opening fully collapsed on S, the Content law and its three destinations, venue contract placed after the managed markers, named Content heading, one sentence per line, sentence-apparatus example
260725 · Stage Contract placement updated: renders inside Opening as a collapsed disclosure, not between Opening and Diagram (JL)
260725 · S creation contract now materializes stage + venue + previous-contract inputs as page-owned Content headings
260725 · S authoring gained requires/style-from/provides metadata and managed Stage Contract creation/sync/check
260725 1150 · QB alignment pass: the "What remains" bullet no longer contradicts the settled header (the dual-kind test it demanded had already passed); ALIAS/sec() pointer repointed to src/common.py
260725 · QA2 settled after the repeated fresh-context acceptance test rendered one Q and two S variants; optional Stage Record behavior passed both present and absent cases
260725 · QA2 updated from the older Q-only description to QA4's shared Q/S contract: Opening and Content mapping, workflow-aware requiredness, 13-section source count, and fresh dual-kind acceptance gate
260724 1242 · Translated to English (JL 260724: everything on the board in English)
260723 · Rewritten to the new structure: Question expanded into "one paragraph + bullets", added `## Boundary` and `## Files`; the retired `## Why here` merged into Question
260723 · Synced with the 260723 redesign: template rewritten (new order · `Items to Finish` / `Where we are` · new `## Boundary` · Question as "paragraph + bullets" · `Why here` retired); required count 7 → 6. state ✅ → 🟡, the structure changed, the old zero-background fill test no longer counts, must re-run
260723 1450 · Cold-read acceptance: a fresh agent produced a valid card from the template alone; top four lines got required/optional + a `state` legend (in the usage comment, dodging the meta parser)
260723 1445 · Landed `ref/q-template.md`: per-section required/optional, added `## Law`/`## Lesson`, Log reversed; `board-form.md` and `SKILL.md` synced → all four finish lines reached, question SETTLED
260723 1130 · Template gains `## Lesson` (folded, for pitfalls)
260723 1120 · Log switched to reverse-chronological, newest on top (md and page)
260723 1105 · Template gains `## Comments` (inline comments with status)
260723 1010 · Template gains the item syntax (`- short heading` + indented explanation)
260723 0950 · Log lines gain time: `YYMMDD HHMM · what changed`, time optional
260723 0919 · All section names switched to English, template examples synced
260723 0910 · Template gains ## Diagram and ## Log
260722 2330 · Status words replaced the home-made ones with OPEN / PARTIAL / SETTLED / ON HOLD
260722 2325 · JL settled two rules on the spot: titles must be short phrases (≤14 chars), finish lines must be checklists
260722 2310 · Renumbered Q2 → QA2
260722 2255 · Split out of QA1 as its own question
