# Short title in sentence case: say what this page is FOR
<!-- On an S page the title carries the page's identity first: `S <Family> <unit> · <short title>`,
     for example `S Main 7 · §6 Results`. build.py derives the Content heading from it
     (`📚 Content · Main 7 §6 Results`), so a bare phrase there produces a heading that names nothing.
     When the artifact carries its own number and it is offset from the board index, put both in the
     title as above; then the reader is never left working out which 7 is meant.
     Q pages keep the plain phrase. Delete this comment. -->
state: 🔴 OPEN
owner: CC
method: one line on how you plan to solve it (optional; delete the line if unused)

<!-- S-only metadata. Uncomment the three lines below, in this position, for an S page; delete the
     whole block for a Q page. `stage.py new` writes real values and generates the managed Stage
     Contract; never infer dependencies from Pages order. An S id resolves bare (`S-Work-1`); any
     other source needs its real filename including the extension (`QA1-dump-location.md`).
requires: S-Work-1, S-Main-0, S-Display-0
style-from: S-Venue-1, STYLE.md
provides: one compact phrase naming the downstream handoff
-->

<!-- How to use: copy this file, rename to Q<group letter><number>-<slug>.md for a decision
     or S-<Family>-<unit>-<slug>.md for a paper lifecycle page, replace each
     guide sentence with real content. "required / optional" at the start of each section is
     for you:
       required = leaving it out makes the question incomplete (build.py does not error, but
                  a block is missing on the page).
       optional = delete the whole section, heading included, if unused.
     The top four lines follow the same rule: # title, state, owner are required; method is
     optional (delete the whole line).
       - the title is a phrase in SENTENCE CASE that says what the page is FOR (JL 260801).
         Capitalize the first word and proper nouns and nothing else, so `Page Template design`
         is wrong twice over: it mixes two cases, and it names a topic instead of a purpose.
         A colon may carry a short subtitle, and that is usually where the purpose lands:
         `The page template: one grammar every page kind obeys`, `The code's shape: one Law,
         three files`. A defined term keeps its capitals (`Mounting a SPACE`). On the Index the
         title is the only line a reader gets before choosing, so a title naming only its
         subject makes them open the page to learn what the page was for.
       - the first state token is exactly one of 🔴 (not started), 🟡 (in progress),
         ✅ (done), or ⏸️ (parked). Human-readable detail may follow, such as
         `✅ SETTLED`, `✅ PINNED · MISQ 2026`, or `🟡 rendered · awaiting gate`;
         the suffix is not a fifth state and may not contradict the emoji. A new page of either
         kind starts `🔴 OPEN`. What ✅ means differs: on Q every Aim is met or explicitly held, on S that
         page's human gate passed (the index counts it under its named family).
       - the state line is a row, not a paragraph (JL 260816): after the status word come at
         most two ` · ` parts, what stands and then `open:` with a short list or a count, the
         whole line under 110 characters. A part that could end in a period is prose: the
         facts belong in States and the reason in Log.
         Good: `🟡 PARTIAL · ruled, card grammar adopted · open: landing address, citation hop, tab`
       - owner is who is responsible; JL shows 🧠 (decides) on the page, others show 🔧.
     Section names (Opening / Content / Aims / States, etc.) must be kept verbatim.
     `## Question` is still accepted as a legacy alias for `## Opening`, but the template
     keeps Opening because that is the canon; the lead sentence is still an actual question.
     build.py fetches content by these exact names, so any mark goes in the body, never in the
     heading line, and state: takes one status only.
     The visible hierarchy is fixed, and it is the SAME for both kinds:
       Opening -> Diagram -> Content -> Aims -> States -> Files.
     Each section answers ONE reader question, and that is the test for every sentence you
     write into it (JL 260801; the five-row contract per section, conveys · holds · source ·
     rules · omit, lives in the design board's QB4 Content parts and in /haipipe-page):
       Opening: what is this page and why should I care? (never omit) · Diagram: can I see
       the whole subject at once? (delete when no figure helps) · Content: what does this
       page establish? (Q may omit, S never) · Aims: which durable target states should this
       page establish? (never omit) · States: what is true now for each Aim, what waits on a human?
       (never omit) · Files: which few files continue this work? (strongly advised) ·
       folds: the durable memory (each optional).
     A sentence answering another section's question is misplaced: substance in Opening
     moves to Content, contract material in Content to Stage Contract, settled flags to
     States; a durable intended result belongs in Aims, while a temporary next step belongs in an Aim's optional Plan.
     There is NO Boundary section (JL 260731, said twice): what a page covers is the
     Opening's job, and a Boundary that restates it is noise. Point at a neighbouring
     page from the prose that needs it instead.
     Opening carries the lead question. Clicking the visible paragraph opens the drawer, which
     carries "More details", "Writing Style", and the whole Stage Contract FLAT: everything is
     seen in one go and no row inside the drawer folds a second time (JL 260725). Stage Contract
     is therefore not a section of its own on the page. Optional Diagram is its own collapsed section and opens only when its heading
     is clicked. On Q and S pages, everything after the FIRST BLANK LINE becomes the collapsed "More
       The visible paragraph is 5-6 lines and about 450 characters, 520 at the ceiling; past that a
       reader stops before the question is answered.
       Write it in PLAIN ENGLISH for a weak English reader: short sentences, ordinary words, and
       every term the page invents defined the first time it appears, on stage rather than in the drawer.
       Do NOT enumerate a growing roster in the Opening (the page kinds, the sections, the skills):
       a list that grows needs editing on every addition, and the paragraph is the one place that must
       stay true without maintenance. Name the rule, not the members.
     details" row in the Opening drawer. Explicit Content is optional for Q and required
     for S. When creating S Content, use the stage template as the base blueprint, overlay the venue
     template's reader/section/style constraints, then add accepted and unresolved requirements
     from previous Stage Contracts. Materialize the result as explicit direct `###` headings.
     Delete this comment when done (it is dropped at generation either way).
     Full writing standard: ref/writing-rules.md. English only. No em-dashes.
     One sentence per source line: the page gives every prose line its own row, so a hard wrap in
     the middle of a sentence becomes a broken line the reader sees. Let the browser wrap. -->

## Opening
How does <the thing this page decides> work, and why does it need settling now?
Those words are this board's own, so say what each one is in one clause with a real example.
Name what makes it hard, in one sentence a reader can feel.
Then say what this page decides about it.
Write the title, this Opening, and Content for someone who arrived today: the current contract in plain words, with no decision dates, no people's names, and no retired mechanisms; that story lives in `## Log`.

**Where this page sits**: the neighbouring page the reader most likely came from, and what it handles.

**Why it matters**: the stake, in the reader's terms, not the implementation's.


## Stage Contract
S required · Q delete this whole section. This section carries the explicit upstream acceptance conditions from `requires:` and the Venue references from `style-from:`. `stage.py` materializes the referenced prose rules in this page's own `## Writing Style`; do not copy an upstream page's whole Content.

It renders inside `🧭 Opening` as one collapsed row, not as a section of its own on the page.

**Do not hand-copy the markers below.** They are shown so you can recognize them; the `sha256=...`
is a real hash of the upstream sources, and a hand-written one makes the build report the page as unsynchronized. Let `stage.py new` create the block, or run `stage.py sync` to fill it. Never write your own prose between the markers either: sync replaces everything there, so hand-written contract text goes AFTER the end marker, where it is preserved.

The generated part is bounded by these markers:

**A managed Stage Contract block**: written by `stage.py`, never edited by hand.

```markdown
<!-- haipipe:contract:start sha256=... -->
### Required Inputs
...
### Venue
...
<!-- haipipe:contract:end -->
```

`stage.py sync` may replace only that marked block. Author-owned material stays after it, so this is where any hand-written contract lives: the venue contract for a manuscript page (its venue, section type, binding blueprint, and style pointer) belongs here as its own `###` subsection, NOT in Content. Actual prose rules live only in `## Writing Style`.

### Provides
State the compact, observable output this stage hands downstream. Keep it short enough for a dependent page to inherit without copying this page's Content.

## Writing Style
required · How this page must be written, so that whoever edits it next edits to the same rules.
Renders as a plain row inside Opening's drawer, beside More details.

On an S page, `stage.py new` or `stage.py sync` places inherited `style-from` rules between `haipipe:style` markers in this section. Write page-owned rules outside those markers. The sync may refresh the marked inheritance, but it never turns Stage Contract into a second style source.

**A managed Writing Style block**: the inherited prose rules `stage.py` materializes here.

```markdown
<!-- haipipe:style:start sha256=... -->
**Inherited requirements from `S-Venue-1`**: ...the resolved page prose rules...
<!-- haipipe:style:end -->
```

Write it as several **Item**: prose paragraphs rather than terse bullets, and cover both halves:
the prose rules (language, sentence shape, voice) and the per-section requirements
(what subsections this page's sections should carry, what is required, what is merely suggested).

**Language and sentences**: English only. One sentence per line, so a paragraph is consecutive lines.
Never stack three clauses behind a colon; break it into short sentences that each carry one idea.

**Voice**: Declarative, not tentative. A ruling that is the decider's carries their name and the date.

## Diagram
optional · One ascii figure showing the shape or flow of the question, right below Opening.
If you cannot draw it, delete the whole section: empty beats wrong.

CONTENT IS NUMBERED ALL THE WAY DOWN (JL 260801). A division is `### 3 · Content`, a group inside it is `**3.2 · Group title**`, and a paragraph is `#### 3.2.1 · Its heading`. An ungrouped division numbers its paragraphs `#### 3.1 ·` straight through, so the DEPTH of the number says whether a group exists. Every number is followed by ` · ` and the heading's own words. The index is what makes a long division navigable and citable: `1.2.3` is something a person can point at in chat, and a bare heading is not.

EVERY FIGURE CARRIES A CAPTION LINE ABOVE IT (JL 260801). Write `**Name**: what this diagram shows.` on the line directly above the fence, one line only. A section may hold several figures, and an unlabelled one makes the reader decode it before learning what it is. The caption goes
ABOVE, because an explanation arriving after the figure arrives after the reader has started working it out.

A ROW IS A LABEL AND ITS VALUE, NEVER A CLAUSE (JL 260801, asking why the figures carried so many words). If a row could end in a period it is prose, and it belongs in the paragraph under the figure rather than inside the fence. Write `🎯 Aims   A3.1 · A3.2 · P1`, not `🎯 Aims are durable targets that stay stable when the route changes`. A figure earns its fence by being SCANNABLE, so a wall of clauses in a box is slower to read than the same clauses outside it. Draw it with `/diagram-ascii`, keep it under about 80 characters wide, and put an emoji on every box, row label and status marker.

It renders as its own `🖼 Diagram` section, collapsed by default. The heading remains visible;
the figure appears only after the reader clicks it.

`## Diagram` holds the ascii figure and nothing else (JL 260815). A drawing is MATERIAL: it lives as a scene file in the page's own `draw/` folder and opens through the 🖌 Draw split beside the page, never inline in this section. The ascii is the half with zero dependencies — it renders with scripts off and survives every host.

**Name of the figure**: what this diagram shows.

```text
source question ──▶ decision or stage ──▶ observable handoff
```

Replace the example with this page's real figure.

## Content
S required · Q optional. The page's substantive material after orientation. Delete this explicit section in a Q that needs no additional material.

On an S page, Content is the stage's real product and nothing else (JL 260725). For a manuscript page that means the section itself: its parts, its paragraphs, its prose. Three kinds of material accumulate around a stage and belong elsewhere: Required Inputs and Venue go to `## Stage Contract`, page prose rules go to `## Writing Style`, settled flags and corrections go to `## States` because they report what is now true, and intended outcomes go to `## Aims`. The page heading names the stage for this reason, reading `📚 Content · Main 7 §6 Results` rather than a subsection count, so if that name does not describe what a reader finds here, this section is holding something that belongs in one of the other three.

Content carries exactly two heading levels, and the number carries the depth (JL 260725). A direct `###` is a division: a part that holds content of its own and folds on its own. A `####` is one paragraph inside it, always, and there is no third level: the page folds one level, so a deeper tree would collapse a whole section into a single box. Read the depth off the numbering, `§6` against `§6.1`. Write a division only when it holds something, so a flat section carries one `### §1 Introduction` over its paragraphs while a subsectioned one starts at `### §6.1`, and no page opens a box onto nothing. This makes the shape checkable without reading the prose: the subsection count is the number of `###` headings whose number contains a dot.

Each division opens with its FACE DIAGRAM (JL 260731): the first fenced ascii figure directly after the `###` heading, a short high-level sketch of the division's concept or content. Position alone marks it, no new syntax; page and group ids inside it render as links. The worked example is the design board's QB4, whose Content parts each open with theirs.

A `####` heading carries no icon. 🔹 belongs to a group title, which is a full-line `**bold**` that genuinely leads a run of items, so never write a paragraph in bold. An optional full-line `(…)` directly under a `####` heading is that paragraph's job: it renders in grey italic, stays on stage as a scan hook, and only the line immediately after the heading is read that way. Keep it to about
80 to 120 characters.

For a new S page, compose this section at creation time: stage template first, venue template second, previous Stage Contracts third. Write the resolved blueprint as direct `###` headings.
The new page owns those headings; build renders them but does not regenerate them.

A stage declares its obligations ONCE, and that one place is `## Stage Contract` (JL 260801, ruling that one name is enough). There is no Stage Record. Old pages that still carry a direct `### Stage Record` under Content keep rendering: build.py lifts it into the Stage Contract and prints it as the contract's opening lines, so no wording is lost, but nothing new is written under that name. All other direct `###` sections remain under Content.

Each direct `###` heading becomes one individually collapsible content subsection. Keep the old stage prose under these headings rather than copying it into a second backing document.

### 1 · First content subsection
**Name of the figure**: what this diagram shows.

```
📦 THE SHAPE OF THIS PART, at a glance

  🏷 a row      is a label and its value
  🚫 never      a clause that could end in a period

⚖️ draw it with /diagram-ascii · emoji on every box · under ~80 cols
```
📌 One or two lines saying what this part settles, so a reader who jumped straight here knows what they are inside before any detail arrives.

The actual content goes here, one sentence per line.

**1.1 · Example group title**
- First related fact; replace this example with real content.
- Second related fact; delete the whole group when it adds no scanning value.

A sentence can carry apparatus: `>` lines written directly beneath it fold under that sentence, which shows a badge until it is clicked. Everything starts SHUT, comments included (JL 260801), and the badge says which kind is underneath: `⚑` typed lanes, `💬` a person waiting, `✎` an edit record.
> Note: this row is attached to the sentence above it, by adjacency alone.
> Comment JL a sentence-local comment · 260729 1502
> ✎ The whole sentence with ~removed~ *added* words. · JL · 260729 1503
> Citation: typed lanes name the attachment, one of Citation, Value, Display, Check, Q-consumer, Link, Source, Note; a person's remark is `> Comment WHO …` (JL 260802), and the older `> JL:` form still renders while `check.py` warns on it.

**A lane is one source line, however long.** A wrapped continuation line becomes its own sentence row on the page, takes its own ⚑ badge, and steals every lane written below it. This is the same one-sentence-per-line rule as the prose, and it fails invisibly: the markdown looks fine and only the generated page shows the broken row.

Adjacency is the whole binding, so a lane must sit under its own sentence: placed after a paragraph it silently attaches to whatever line precedes it. A concern that belongs to the page rather than to one sentence (a missing script, a sweep still owed) has no sentence to attach to and belongs in `## Aims` when it is a durable target; a temporary action belongs in that Aim's optional `Plan`.

Use standard Markdown `![](path.png)` to show an image inline. The same form with a local `.pdf` path, `![](path.pdf)`, renders a readable PDF object with an `open PDF` fallback link. On a
Display page, `preview.pdf` remains the generated Current Float; use an explicit PDF subsection only when the reader also needs to inspect the underlying live display artifact.

### 2 · Second content subsection
**Name of the figure**: what this diagram shows.

```
📦 THE SHAPE OF THIS PART, at a glance

  🏷 a row      is a label and its value
  🚫 never      a clause that could end in a period

⚖️ draw it with /diagram-ascii · emoji on every box · under ~80 cols
```
📌 One or two lines saying what this part settles, so a reader who jumped straight here knows what they are inside before any detail arrives.

Continue with the next coherent part of the stage.

#### 2.1 · One paragraph of this division
(what this paragraph does, in one line, so the division can be scanned without being read)
The paragraph's prose starts on the line after the job line, still one sentence per line.
Delete the `####` heading and the `(…)` line together in a division that is a single block of prose rather than a run of numbered paragraphs.

## Aims
required · Durable target states, not a task list. Every Aim has a stable id and names the result this page is trying to make true.

Group Aims under the Content division they serve: the group is `### A<n> · <emoji> <name>`, carrying that division's number and name, and an emoji that lives on the GROUP and never on the division heading (`check.py` strips an emoji from a group name and not from a division, so an emoji on the heading fires `group-name-drift`), and the States group is written exactly the same way
(JL 260801, the letter fixed to `A` on 260802; `C<n>` still resolves for older boards).
One Content division may have zero, one, or several Aims. Use `P1`, `P2`, and so on only for a page-level Aim that genuinely crosses divisions.
The section heading derives its `met/total` count from `## States`; Aims themselves never carry checkboxes.

Each Aim starts `- A<division>.<n> · target`. Add a testable `Done when` line.
Add `Plan` only when the immediate route is worth preserving; Plan is temporary and may change without changing the Aim.

### A1 · First content subsection
- A1.1 · The first division establishes its intended reader outcome.
  **Done when:** A named reader can verify the outcome from the rendered division.
  **Plan:** Run one cold read and revise the division where the reader hesitates.
- A1.2 · The division's evidence is traceable.
  **Done when:** Every material claim points to its source or owning page.

### P · Page-level
- P1 · The whole page reads as one coherent decision surface.
  **Done when:** Opening, Content, Aims, and States agree without duplicated or contradictory claims.

For an S page, a former Q-consumer becomes an Aim when answering it is a required stage outcome.
Keep the Aim id, consumer id, stake, route, and acceptance condition together:

- A2.1 · Q-Stage-1 · Resolve the concrete consumer question.
  **Done when:** The answer has landed, been interpreted, and been woven into `## Content`.
  **Description:** What must be learned?
  **Reason:** Which content or claim depends on it, and what breaks if it fails?
  **Probe:** Name the real route: a probe file, task folder, person, meeting, or `not opened yet`.

A deferred consumer closes only after a forward pointer is recorded.

## States
required · The collection of factual present State records, one per Aim, plus the decisions a person still owes. It is a snapshot of right now: history belongs in `## Log`.

Mirror the Aims groups and ids so a reader can compare intent with reality without guessing.
Each Aim has exactly one current state row: `⬜` not started, `🔨` being worked on now, `🧠` waiting on a person or on something outside this page, `✅` met with the evidence named, or `❄️` on ice, held on purpose and thawable.
Each says its meaning by SHAPE (JL 260802); the older `🟡` `🟠` `⏸️` still parse, because rows on other boards use them, but nothing new is written with them.
Do not put future work here; that is either an Aim or its Plan. Record why a State changed in `## Log`.

If the page holds decisions only a person can make, add one `### Decision Now` subsection
(JL 260731), and put it FIRST, above the per-Aim groups below (JL 260802): everything else in
States is a report, and this is the one part that asks the reader to do something. One `- [ ]` row per pending decision. The machine writes the rows and closes one once the human has answered it, recording which option, who ruled and when; a row nobody has answered waits for them (JL 260802). Its shape and the rule for what earns a row are stated under the example groups.

### A1 · First content subsection
- 🔨 A1.1 · Active; the first cold read is scheduled and the current wording is ready.
- 🧠 A1.2 · Waiting for the source owner to confirm the evidence route.

### P · Page-level
- ⬜ P1 · Not started; the divisions have not yet been read together.

On S pages, summarize the stage here; do not repeat every consumer answer from Aims.

A `### Decision Now` row earns its place only when something STOPS until it is answered. A decision that matters is usually made in conversation within minutes, so decide it, do it, and record it in `## Log` instead of parking it here.

Each option takes ITS OWN LINE and says what choosing it commits you to (JL 260731). Options crammed together on one line name the choices and explain none, so the reader has to work out the consequences before deciding. Give a decision as many options as it actually has, never three by habit: a filler option is worse than none.

**A Decision Now row**: the shape used to put one choice in front of a human.

```markdown
- [ ] 🗣 The question, as the row's own title
      📍 `Part` which Content part it belongs to, so it is read beside the rule it changes
      🔔 `Why now` what raised it, in one sentence
      ⭐ `A ·` the first option, named by its CONSEQUENCE, with the star on the one CC
         recommends and the reason on that line
      `B ·` the second option, and what it commits you to
      🛑 `Blocks` what stops until it is answered, or `nothing`
      🤖 `If nobody answers` the option that takes effect, required whenever nothing is blocked
```

An answered decision LEAVES States entirely (JL 260802): the RULING goes to `## Law` with the date, the person, and the options that were not chosen with the reason; the CHANGE goes to `## Log` as one dated line; and the matching Aim's State row is updated in the same edit.

## Files
optional (strongly recommended) · The action map for this page: if I change a rule here, what do
I touch? That is a different and much shorter list than "files about this topic", and an exhaustive one is worse than a short one, because it hides the entry points. Paths in backticks; those declared in `board.md`'s `## Links` become clickable, and `check.py` resolves every one of them, so a path that rots is reported.

- `<path/to/thing.py>`
  Its role in this question, and where you start when this question changes.
- `<path/to/generated-thing>`
  If it is generated, say "do not hand-edit".

Optional `###` groups when the list has several coherent parts. The group names are a MENU of
ACTIONS and a page takes the ones that apply (JL 260731, widened 260802): `Engines` (what RUNS this page's subject; you open one to change behavior), `Contracts` (what CARRIES a rule to other
pages: a template, a loadable spec), `Checks` (what CATCHES a page breaking one), `Input files`
(what the work READS: specs, source pages, evidence), `Output files` (what a BUILD writes:
opened to check and never to edit). Engines comes first because Files is ordered by what a reader opens first, not by how the data flows.

Which group a file goes in is decided by what YOU do to it, not by what it is: edit it to change behavior -> Engines; read it, or an engine reads it -> Input files; a build wrote it
-> Output files. So a governing spec that never executes goes in **Contracts** when it carries a rule to other pages, and in Input files only when this page merely reads it, and a script whose
rules are code is an Engine. A page may add a name, and the test is that it states an ACTION, in the page's own words: a group named after a SUBJECT rots the moment that subject leaves the page. Stay flat under about three rows; omit an empty group and never invent a row to fill one.

When this Page needs a precise fragment of another Page, use the one fixed exception to action-named groups. Delete it when unused:

```markdown
### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `reads · EVIDENCE` · [QB7 §3](QB-research/QB7-literature.md)
  Why this phase needs that fragment.
```

The relation is `reads`, `constrained by`, `continues`, or `contrasts`; the phase is DRAFT, EVIDENCE, REVISE, CHECK, or ALL; the link target is Board-root-relative. The Page id must match the target, and scope is `page` or one direct Content division such as `§3.2`. `pagecontext.py` reads only phase-matching rows and follows one hop. For a division it returns the target Page identity, Opening, that division, and its matching Aims/States group; several scopes on one target share one identity and Opening. Never list a whole Page when one division is enough.

## Law
optional · folded · Rules this question has settled and will follow from now on, one per line.
Write each entry as a `- ` row opening with an emoji that says its SUBJECT (JL 260802), which the render lifts out as the row's icon, so a reader hunting one rule finds it without reading forty headings. Do not write intentions here as if settled. Delete the section if unused.

A ruling additionally carries the DATE and the PERSON, written as the row's opening stamp, so a later reader can tell a ruling from a description:

- 260723 JL · ⚖️ The rule, stated first
      One sentence naming what now binds.
      The paragraph: what it was before, why it changed, and which options were rejected and why.

## Lesson
optional · folded · Traps hit and lessons learned on this question, one per line, each a `- ` row opening with an emoji. Keep them specific (a concrete failure attached). Delete the section if unused.

## Glossary
optional · folded · Words on this page an outsider would stumble on, one `- ` row each, opening with an emoji: the TERM is bold and its definition follows a colon (JL 260802), because the term is what the reader arrived looking for. Any coined phrase must be defined here or not used.
Delete the section if unused.

## Discussion
optional · folded · Loose discussion, one line each. The "➕ Add to discussion" box on the page writes here.
> JL: discussion goes here.
>> CC0724: reply with two angle brackets and a date.

## Log
optional (most questions have one) · folded · What changed on this question, one line each, newest on top:
260724 1030 · what changed (`YYMMDD HHMM · ...`, time optional)
