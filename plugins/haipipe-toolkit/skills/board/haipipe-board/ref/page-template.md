# Short purpose title
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
       - the title is a phrase in SENTENCE CASE that says what the page is FOR (JL 260801),
         targets three to five visible words, and never exceeds six (JL 260827).
         Acronyms, identifiers, and hyphenated compounds count as one word; punctuation-only
         separators do not count. A colon does not create a second allowance: the complete
         visible title still stays within six words. The page id is not part of the title.
         Capitalize the first word and proper nouns and nothing else, so `Page Template design`
         is wrong twice over: it mixes two cases, and it names a topic instead of a purpose.
         Prefer compact titles such as `BCarrier header-line joins`, `AMI admission and CABG`,
         or `CABG regression design`. A defined term keeps its capitals (`Mounting a SPACE`). On the Index the
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
         facts belong in the Aims' `Now:` lines and the reason in
         `outline/<stem>-log.md`.
         Good: `🟡 PARTIAL · ruled, card grammar adopted · open: landing address, citation hop, tab`
       - owner is who is responsible; JL shows 🧠 (decides) on the page, others show 🔧.
     Section names (Opening / Content / Aims, etc.) must be kept verbatim.
     `## Question` is still accepted as a legacy alias for `## Opening`, but the template
     keeps Opening because that is the canon; the lead sentence is still an actual question.
     build.py fetches content by these exact names, so any mark goes in the body, never in the
     heading line, and state: takes one status only.
     The visible hierarchy is fixed, and it is the SAME for both kinds:
       Opening -> Outline -> Content -> Aims (Files lives in outline/<stem>-files.md since 260831).
     Each section answers ONE reader question, and that is the test for every sentence you
     write into it (JL 260801; the five-row contract per section, conveys · holds · source ·
     rules · omit, lives in the design board's QB4 Content parts and in /haipipe-page):
       Opening: what is this page and why should I care? (never omit) · Outline: how is this
       page structured and supported? (delete only when neither plan nor map exists) · Content: what does this
       page establish? (Q may omit, S never) · Aims: which durable target states should this
       page establish, and what is true now for each? (never omit) ·
       folds: the durable memory (each optional).
     A sentence answering another section's question is misplaced: substance in Opening
     moves to Content, contract material in Content to Stage Contract, settled flags to
     the owning Aim's `Now:` line; a durable intended result belongs in Aims, while a temporary next step belongs in an Aim's optional Plan.
     There is NO Boundary section (JL 260731, said twice): what a page covers is the
     Opening's job, and a Boundary that restates it is noise. Point at a neighbouring
     page from the prose that needs it instead.
     Opening carries the lead question. Clicking the visible paragraph opens the drawer, which
     carries "More details", "Writing Style", and the whole Stage Contract FLAT: everything is
     seen in one go and no row inside the drawer folds a second time (JL 260725). Stage Contract
     is therefore not a section of its own on the page. Outline is its own open-by-default section,
     generated only from the current versioned plan's table. Do not write a Page-level narrative map.
     A manuscript `page-type: section` is the reader-facing exception: its Opening renders only
     the visible paragraph. Page-owned prose rules live as authored W records in
     `outline/<stem>-requirement.md`, beside generated venue V records; the product Page carries no Writing Style block.
     Post-paragraph notes and Stage Contract remain source-side for drafting and CHECK.
     Opening's visible label is `🚪 Opening`; Outline keeps `🧭 Outline`, so orientation and plan
     are distinct at a glance. A bare internal address such as `C1`, `E3`, or a Run id never carries
     the Opening. State the plain-English subject first and keep an address only as a secondary,
     compact named handle, for example `primary total-MME association (Claim1.TotalMME)`.
     Content, Aims, References, Files, and every other fold start shut. On Q and S pages, everything
     after the FIRST BLANK LINE becomes the collapsed "More
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
Write the title, this Opening, and Content for someone who arrived today: the current contract in plain words, with no decision dates, no people's names, and no retired mechanisms; that story lives in `outline/<stem>-log.md`.

**Where this page sits**: the neighbouring page the reader most likely came from, and what it handles.

**Why it matters**: the stake, in the reader's terms, not the implementation's.


## Stage Contract
S required · Q delete this whole section. This section carries the explicit upstream acceptance conditions from `requires:` and the Venue references from `style-from:`. `stage.py` materializes the referenced prose rules in this page's own `## Writing Style`; do not copy an upstream page's whole Content.

It renders inside `🚪 Opening` as one collapsed row, not as a section of its own on the page.

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

`stage.py sync` may replace only that marked block. Author-owned material stays after it, so this is where any hand-written contract lives: the venue contract for a manuscript page (its venue, section type, binding blueprint, and style pointer) belongs here as its own `###` subsection, NOT in Content. On a non-Section stage, actual prose rules live in `## Writing Style`; a manuscript Section stores them as authored W records in `outline/<stem>-requirement.md`.

### Provides
State the compact, observable output this stage hands downstream. Keep it short enough for a dependent page to inherit without copying this page's Content.

## Writing Style
Non-Section compatibility only · How this page must be written, so that whoever edits it next edits to the same rules.
Renders as a plain row inside Opening's drawer, beside More details. A manuscript
`page-type: section` deletes this block and writes one authored `W<n>` record per rule in
`outline/<stem>-requirement.md` instead.

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

<!-- OUTLINE IS DERIVED: the Page automatically renders the current versioned
     outline/<stem>-outline-v<N>.md as its read-only `▤ Outline table`.
     Do not add a `## Outline` source block, paste the table, or author an ASCII
     narrative map: outline/ remains the authority for plan, evidence, feedback,
     requirement, discussion, file, and log records. -->

CONTENT IS NUMBERED ALL THE WAY DOWN (JL 260801). A division is `### 3 · Content`, a group inside it is `**3.2 · Group title**`, and a paragraph is `#### 3.2.1 · Its heading`. An ungrouped division numbers its paragraphs `#### 3.1 ·` straight through, so the DEPTH of the number says whether a group exists. Every number is followed by ` · ` and the heading's own words. The index is what makes a long division navigable and citable: `1.2.3` is something a person can point at in chat, and a bare heading is not.

EVERY FIGURE CARRIES A CAPTION LINE ABOVE IT (JL 260801). Write `**Name**: what this diagram shows.` on the line directly above the fence, one line only. A section may hold several figures, and an unlabelled one makes the reader decode it before learning what it is. The caption goes
ABOVE, because an explanation arriving after the figure arrives after the reader has started working it out.

A ROW IS A LABEL AND ITS VALUE, NEVER A CLAUSE (JL 260801, asking why the figures carried so many words). If a row could end in a period it is prose, and it belongs in the paragraph under the figure rather than inside the fence. Write `🎯 Aims   A3.1 · A3.2 · P1`, not `🎯 Aims are durable targets that stay stable when the route changes`. A figure earns its fence by being SCANNABLE, so a wall of clauses in a box is slower to read than the same clauses outside it. Draw it with `/diagram-ascii`, keep it under about 80 characters wide, and put an emoji on every box, row label and status marker.

It renders as its own `🧭 Outline` section, open by default, as the one
plan-derived `▤ Outline table`. A drawing is MATERIAL: it lives as a scene
file in the page's own `studio/draw/` folder and opens through the 🖌 Draw split
beside the page, never inline in the Outline section.

## Content
S required · Q optional. The page's substantive material after orientation. Delete this explicit section in a Q that needs no additional material.

On an S page, Content is the stage's real product and nothing else (JL 260725). For a manuscript page that means the section itself: its parts, its paragraphs, its prose. Material around it belongs elsewhere: Required Inputs and Venue go to `## Stage Contract`, manuscript page prose rules become authored W records in `outline/<stem>-requirement.md`, settled flags and corrections go to the owning Aim's `Now:` line because they report what is now true, and intended outcomes go to `## Aims`. The page heading names the stage for this reason, reading `📚 Content · Main 7 §6 Results` rather than a subsection count, so if that name does not describe what a reader finds here, this section is holding something that belongs elsewhere.

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
required · Durable target states, not a task list. Every Aim has a stable id, names the result this page is trying to make true, and carries its own current status: there is no `## States` section (merged into Aims, JL 260819; `check.py` reports a surviving one as `retired-section`).

Group Aims under the Content division they serve: the group is `### A<n> · <emoji> <name>`, carrying that division's number and name, and an emoji that lives on the GROUP and never on the division heading (`check.py` strips an emoji from a group name and not from a division, so an emoji on the heading fires `group-name-drift`)
(JL 260801, the letter fixed to `A` on 260802; `C<n>` still resolves for older boards).
One Content division may have zero, one, or several Aims. Use `P1`, `P2`, and so on only for a page-level Aim that genuinely crosses divisions.
The section heading derives its `met/total` count from each row's tick; Aims never carry checkboxes.

One Aim is ONE row: `- <tick> A<division>.<n> · target`, then a testable `**Done when:**` line, then one `**Now:**` line with the current fact.
The tick is `⬜` not started, `🔨` being worked on now, `🧠` waiting on a person or on something outside this page, `✅` met with the evidence named, or `❄️` on ice, held on purpose and thawable.
Each says its meaning by SHAPE (JL 260802); the older `🟡` `🟠` `⏸️` still parse, because rows on other boards use them, but nothing new is written with them.
`Now:` is a snapshot of right now: history belongs in
`outline/<stem>-log.md`, and future work is either an Aim or its Plan.
Add `Plan` only when the immediate route is worth preserving; Plan is temporary and may change without changing the Aim.
A live ask for a person is that Aim's `Now:` line, marked `🧠`.

### A1 · First content subsection
- 🔨 A1.1 · The first division establishes its intended reader outcome.
  **Done when:** A named reader can verify the outcome from the rendered division.
  **Now:** Active; the first cold read is scheduled and the current wording is ready.
  **Plan:** Run one cold read and revise the division where the reader hesitates.
- 🧠 A1.2 · The division's evidence is traceable.
  **Done when:** Every material claim points to its source or owning page.
  **Now:** Waiting for the source owner to confirm the evidence route.

### P · Page-level
- ⬜ P1 · The whole page reads as one coherent decision surface.
  **Done when:** Opening, Content, and Aims agree without duplicated or contradictory claims.
  **Now:** Not started; the divisions have not yet been read together.

For an S page, a former Q-consumer becomes an Aim when answering it is a required stage outcome.
Keep the Aim id, consumer id, stake, route, and acceptance condition together:

- ⬜ A2.1 · Q-Stage-1 · Resolve the concrete consumer question.
  **Done when:** The answer has landed, been interpreted, and been woven into `## Content`.
  **Now:** Not opened yet.
  **Description:** What must be learned?
  **Reason:** Which content or claim depends on it, and what breaks if it fails?
  **Probe:** Name the real route: a probe file, task folder, person, meeting, or `not opened yet`.

A deferred consumer closes only after a forward pointer is recorded.

If the page holds decisions only a person can make, add one `### Decision Now` subsection
(JL 260731), and put it FIRST, above the per-Aim groups (JL 260802): everything else in
Aims is a target and its report, and this is the one part that asks the reader to do something. One `- [ ]` row per pending decision. The machine writes the rows and closes one once the human has answered it, recording which option, who ruled and when; a row nobody has answered waits for them (JL 260802). Its shape and the rule for what earns a row are stated below.

A `### Decision Now` row earns its place only when something STOPS until it is answered. A decision that matters is usually made in conversation within minutes, so decide it, do it, and record one dated ruling in `outline/<stem>-log.md` instead of parking it here.

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

An answered decision LEAVES Aims entirely (JL 260802): the RULING goes to
`## Law` with the date, the person, and the options that were not chosen with
the reason; the CHANGE becomes one dated record in `outline/<stem>-log.md`;
and the matching Aim's tick and `Now:` line are updated in the same edit.

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
