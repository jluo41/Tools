# Shared Q/S source template
state: ✅ SETTLED
owner: CC
method: mirror QA4's rendered face contract in one copyable Q/S markdown source

## Question
I open an empty `QA9-xxx.md` or `S4-display.md`: what do I put in it so the generated face follows QA4? Which sections are required for Q, which are required for S, and which can be deleted wholesale?

The generator only recognizes a fixed set of section names, so misspell one and that section **silently disappears, no error**; silent failure is the hardest kind to debug. Without a clear template, everyone writes a different-shaped face and the page turns messy, while colleagues and future agents touch this file every day. QA2 is the authoring side of QA4's reading contract: when QA4 changes Opening, Content placement, or the on-stage order, this template must follow in the same change or newly written Q and S faces drift back to the old shape.

## Boundary
- ✅ Covered here
  **The inside of one Q or S source file**: which sections exist, which are required versus optional for each workflow kind, what goes in each, and what `ref/q-template.md` looks like.
- ↪ Covered elsewhere
  Which files are in the folder and how a face attaches to the board: that is `QA1`. The rendered reading order, folding, and visual hierarchy are `QA4`. How the words inside each section should be written is `QA5`.

## Diagram
```
copy ref/q-template.md                     source → QA4 rendered face
┌──────────────────────────────────────────────────────────────────┐
│ # title · state · owner              required → headline/header  │
│ method                               optional → header            │
├──────────────────────────────────────────────────────────────────┤
│ ## Question  lead                    required → 🧭 Opening        │
│                rationale                      Q: 📚 Why first     │
│                                               S: Opening Why     │
│ ## Boundary                           advised → inside Opening    │
│ ## Diagram                           optional → collapsed peer    │
│ ## Content                       Q optional/S required → 📚       │
│   ### Stage Record           S optional → Opening, collapsed     │
│   ### other subsection                         Content, collapsed │
│ ## Items to Finish                   required → 🎯 auto-counted   │
│ ## Where we are                      required → 📍 present state  │
│ ## Files                              advised → 📎 action map     │
├──────────────────────────────────────────────────────────────────┤
│ Law · Lesson · Glossary · Discussion · Comments · Log            │
│                                  optional → supporting folds      │
└──────────────────────────────────────────────────────────────────┘
```

## Content
The metadata block above the sections is required for identity: title, state, and owner become the index row and face header; method is optional. The seven mappings below mirror QA4's visible sequence.

### 1 · Opening source — Question plus optional Boundary
Write `## Question` as one actual question lead followed by one rationale paragraph. The lead renders in Opening. On Q, the rationale becomes Content's first Why this matters subsection; on S, it remains open inside Opening. An optional `## Boundary` joins the same Opening and redirects excluded concerns to their owning Q or S.

### 2 · Diagram source — an optional collapsed peer
Write one useful ASCII figure and, optionally, one Excalidraw share link under `## Diagram`. QA4 renders the section between Opening and Content with the body hidden until clicked. Delete the whole source section when the visual adds no understanding.

### 3 · Content source — Q optional, S required
Use direct `###` headings for coherent substantive parts; each becomes one collapsible Content subsection. On S, an optional exact direct `### Stage Record` is orientation metadata and moves into Opening collapsed when supplied, while every other subsection remains under Content. Do not maintain a second live copy of stage substance.

### 4 · Items to Finish source — testable completion
Write `## Items to Finish` as checkboxes that another person can judge true or false. The rendered heading counts them automatically. On S, each former Q-consumer stays together as one recognizable record and closes only after its answer is interpreted and integrated into Content.

### 5 · Where we are source — the present state
Write one concise current-state paragraph followed by dated change items when useful. Report what is true now with numbers where numbers exist; do not restate the full checklist or every S-consumer answer.

### 6 · Files source — the action map
List only the sources, outputs, and implementation files needed to continue, with one line explaining each role. Mark generated files explicitly so the reader does not hand-edit the wrong layer.

### 7 · Supporting source sections — optional history
Law, Lesson, Glossary, Discussion, Comments, and Log are optional source sections rendered as supporting folds below the main path. Retired `## Why here` remains parse-compatible for old boards but must not be added to new files; its job now belongs to the Question rationale.

## Items to Finish
- [x] A shared blank template under `ref/` that can be copied as-is
      `ref/q-template.md` can seed either `Q<group><number>-<slug>.md` or `S<order>-<slug>.md`. It carries all 13 recognized `##` sections, and its usage comment is dropped at build time rather than leaking into the page.
- [x] One guide line at the top of every section: what to write here, and how long
      The first line of each section's body IS the guide sentence (what + how long); you overwrite it as you fill in.
- [x] Mark which sections are required and which optional
      Title, state, owner, Question, Items to Finish, and Where we are are required for both kinds. Method and Diagram are optional; Boundary and Files are optional but strongly advised. Explicit Content is optional for Q and required for S. Markers stay in guide text, never in a recognized heading or metadata key.
- [x] Adding either workflow kind begins from the same source
      Copy the template and rename it without consulting an existing board. The usage comment explains Q and S filenames, their distinct closure semantics, and the optional exact `### Stage Record` and Q-consumer rules that apply only to S.
- [x] Template follows QA4's current shared-face hierarchy
      The source-to-page mapping is now `Opening → Diagram → Content → Items to Finish → Where we are → Files`. Question is a lead plus rationale paragraph, Boundary is optional inside Opening, Q rationale starts Content, S rationale sits in Opening, an optional S Stage Record joins it when supplied, and Supporting folds stay below the main read.
- [x] A zero-background agent can create one valid Q and one valid S
      Given only `ref/q-template.md`, a fresh agent must fill one Q and one S, then explain where every source section renders, which sections differ in requiredness, and why the two workflow kinds do not share closure semantics.
      Passed 260725 through two fresh-context runs. The first rendered a Q and S correctly but exposed that Stage Record's optionality was only implied; after the wording was repaired across QA2, QA4, and the template, a second reader rendered one Q plus S variants with and without Stage Record and found no material contradiction.

## Where we are
**Settled. QA2 now describes the same shared Q/S face contract as QA4, the actual `ref/q-template.md` implements that hierarchy, and a fresh-context render test passed for Q plus S faces both with and without optional Stage Record.**

- 260725 CC · 🧪 Shared-template acceptance passed
  A first clean reader built and rendered one Q and one S, recovering the visible order, rationale placement, Content requiredness, and distinct closure semantics; it found one mild ambiguity about whether Stage Record was required. After “S-only, optional” was made explicit, a second clean reader rendered three faces and confirmed that Stage Record moves into Opening collapsed when supplied and leaves no placeholder when absent.

- What the template looks like
  The top block is `# title / state / owner / method`, followed by 13 recognized `##` sections. The usage comment explains the shared source grammar, Q/S differences, and QA4's visible order; every section then carries replaceable guide text.
- Current alignment with QA4
  Opening is generated from Question plus optional Boundary; Diagram is a collapsed peer; explicit Content supplies collapsible subsections; Items to Finish, Where we are, and Files follow; the remaining sections become supporting folds.
- Requiredness by workflow kind
  Both Q and S require title, state, owner, Question, Items to Finish, and Where we are. Explicit Content is optional for Q and required for S; Stage Record is an optional S-only subsection within that Content. Method, Diagram, and supporting folds are optional; Boundary and Files are optional but strongly advised.
- What remains
  The old cold read covered a Q-only predecessor. The revised test must exercise both Q and S from the current template and confirm the rendered result, not merely parse the markdown.

## Files
- `ref/q-template.md`
  The deliverable itself: adding a question means copying it.
- `build.py`
  `ALIAS` / `sec()` decide which section names are recognized; a misspelled name silently yields nothing.
- `ref/board-form.md`
  §4 section↔page mapping + required/optional.
- `QA4-pagelayout.md`
  The rendered face contract this source template must mirror.

## Law
- Section names must be kept verbatim
  build.py takes the whole string after `## ` as the key (`ln[3:].strip()`), so `## Question (required)` is not found. Required/optional markers therefore go into the first body line, never the heading line.
- Requiredness is workflow-aware
  Both kinds require `# title`, `state`, `owner`, `## Question`, `## Items to Finish`, and `## Where we are`. `## Content` is optional for Q and required for S. `## Boundary` and `## Files` are optional but strongly advised; method, Diagram, and supporting folds are optional.
- On-stage order is fixed
  `Opening → Diagram → Content → Items to Finish → Where we are → Files`, intent first, status second, as settled by QA4. Opening is generated from the Question lead plus optional Boundary.
- QA2 changes with QA4
  QA2 is the authoring contract and QA4 is the rendered reading contract. Any QA4 ruling that changes section placement, requiredness, or visible order must update `ref/q-template.md` and this face in the same change, followed by a fresh-context Q/S creation test.
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
  The first template only marked the `##` sections, so a cold-reading agent had to guess whether state/owner were required. Only after adding them to the usage comment was it clear.
- Stale self-contradictions in the template must be purged
  The template still said "newest Log lines at the bottom" long after reverse order was settled at 1120, exactly the kind of stale sentence a zero-background reader spots first.

## Glossary
required: without it the Q file is invalid. The generator raises no error, but a block is missing on the page.
optional: if unused, delete the whole section including the heading; leave no empty shell.

## Discussion
> JL: I want to understand whether QA4 and QA2 are aligned or not.
>> CC0725: they were aligned in intent, and the live template had most current behavior, but QA2 still documented the older Q-only page: no Content in its diagram or Law, Question shown as a question-mark lead, and no S-specific requiredness. QA2 now mirrors QA4 as the source side of one shared Q/S contract; the fresh Q/S creation test is the remaining gate.

## Log
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
