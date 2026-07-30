# Short title (a phrase, not a sentence)
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
       - the first state token is exactly one of 🔴 (not started), 🟡 (in progress),
         ✅ (done), or ⏸️ (parked). Human-readable detail may follow, such as
         `✅ SETTLED`, `✅ PINNED · MISQ 2026`, or `🟡 rendered · awaiting gate`;
         the suffix is not a fifth state and may not contradict the emoji. A new page of either
         kind starts `🔴 OPEN`. What ✅ means differs: on Q every checkbox is closed, on S that
         page's human gate passed (the index counts it under its named family).
       - owner is who is responsible; JL shows 🧠 (decides) on the page, others show 🔧.
     Section names (Question / Boundary / Items to Finish, etc.) must be kept verbatim.
     `## Opening` is accepted as an alias for `## Question`, but the template keeps Question
     because the lead sentence must still be an actual question.
     build.py fetches content by these exact names, so any mark goes in the body, never in the
     heading line, and state: takes one status only.
     The visible hierarchy is fixed, and it is the SAME for both kinds:
       Opening -> Diagram -> Content -> Items to Finish -> Where we are -> Files.
     Opening groups the Question lead + optional Boundary. On an S page it also carries "Why this
     matters", an optional `### Stage Record`, and the whole Stage Contract, and EVERY one of
     those rows starts collapsed (JL 260725), so the lead question is the only thing on stage and
     each layer of orientation is one click away. Stage Contract is therefore not a section of its
     own on the page. Optional Diagram is its own collapsed section and opens only when its heading
     is clicked. On Q pages, the remaining Question paragraph becomes Content's first "Why this
     matters" subsection, which does start open. Explicit Content is optional for Q and required
     for S. When creating S Content, use the stage template as the base blueprint, overlay the venue
     template's reader/section/style constraints, then add accepted and unresolved requirements
     from previous Stage Contracts. Materialize the result as explicit direct `###` headings.
     Delete this comment when done (it is dropped at generation either way).
     Full writing standard: ref/writing-rules.md. English only. No em-dashes.
     One sentence per source line: the page gives every prose line its own row, so a hard wrap in
     the middle of a sentence becomes a broken line the reader sees. Let the browser wrap. -->

## Question
required · One lead sentence, then one plain paragraph. **Reading this section alone, a
zero-background person should understand what the question is.**

The lead renders in `🧭 Opening` with Boundary. On Q pages, the paragraph below it renders as
the `Why this matters` row inside Opening's drawer, on Q and S alike (JL 260729).

The lead sentence is the actual question, written as a question, in plain words. It stays in
Opening and is clickable.

Then one flowing paragraph: why the question is hard, what breaks while it stays open, and what
it affects downstream. build.py labels it "Why this matters", inside Opening for Q and S alike
for S. Write it as prose, not as `- Why it is hard / - What breaks` bullets.

## Boundary
optional (strongly recommended) · What this question covers and, more importantly, what it does
not. Folds into the same block as the Question, so keep each line short.

- ✅ Covered here
  One or two lines drawing the scope.
- ↪ Covered elsewhere
  One or two lines, and **name the question that does cover it** (for example "projection is
  QA3"). A bare exclusion reads as a refusal; this line's job is to redirect the reader. Use
  `↪`, not `❌` (JL 260724).

## Stage Contract
S required · Q delete this whole section. This section carries the explicit upstream acceptance
conditions from `requires:` and the writing rules from `style-from:`. Create or refresh its
managed block with `stage.py`; do not copy an upstream page's whole Content.

It renders inside `🧭 Opening` as one collapsed row, not as a section of its own on the page.

**Do not hand-copy the markers below.** They are shown so you can recognize them; the `sha256=...`
is a real hash of the upstream sources, and a hand-written one makes the build report the page as
unsynchronized. Let `stage.py new` create the block, or run `stage.py sync` to fill it. Never write
your own prose between the markers either: sync replaces everything there, so hand-written contract
text goes AFTER the end marker, where it is preserved.

The generated part is bounded by these markers:

```markdown
<!-- haipipe:contract:start sha256=... -->
### Required Inputs
...
### Writing Style
...
<!-- haipipe:contract:end -->
```

`stage.py sync` may replace only that marked block. Author-owned material stays after it, so this
is where any hand-written contract lives: the venue contract for a manuscript page (its venue,
section type, binding blueprint, and style pointer) belongs here as its own `###` subsection, NOT
in Content.

### Provides
State the compact, observable output this stage hands downstream. Keep it short enough for a
dependent page to inherit without copying this page's Content.

## Diagram
optional · One ascii figure showing the shape or flow of the question, right below Boundary.
If you cannot draw it, delete the whole section: empty beats wrong.

It renders as its own `🖼 Diagram` section, collapsed by default. The heading remains visible;
the figure appears only after the reader clicks it.

For a richer figure, put an excalidraw share link on **its own line** below the ascii; it embeds
as an interactive excalidraw (`https://app.excalidraw.com/s/...`), with a fallback link underneath.
**Keep the ascii figure:** it has zero dependencies and stays when the excalidraw fails to load.

Opening the section shows `▧ ASCII` and leaves `✏️ Excalidraw` shut, one more click away (JL 260726).
**Write one `## Diagram`, never `###` subheadings for the two halves:** the split is computed from
the rule above (a bare excalidraw URL alone on a line is the canvas, everything else is the figure),
and a `###` in here is not a recognized construct, so it would land as prose inside the figure.

## Content
S required · Q optional. The page's substantive material after orientation. Delete this explicit
section in a Q that needs no additional material.

On an S page, Content is the stage's real product and nothing else (JL 260725). For a manuscript
page that means the section itself: its parts, its paragraphs, its prose. Three kinds of material
accumulate around a stage and belong elsewhere: the inherited venue or writing contract goes to
`## Stage Contract`, settled flags and corrections go to `## Where we are` because they report
what is now true, and anything still owed goes to `## Items to Finish`. The page heading names
the stage for this reason, reading `📚 Content · Main 7 §6 Results` rather than a subsection count,
so if that name does not describe what a reader finds here, this section is holding something
that belongs in one of the other three.

Content carries exactly two heading levels, and the number carries the depth (JL 260725). A direct
`###` is a division: a part that holds content of its own and folds on its own. A `####` is one
paragraph inside it, always, and there is no third level: the page folds one level, so a deeper
tree would collapse a whole section into a single box. Read the depth off the numbering, `§6`
against `§6.1`. Write a division only when it holds something, so a flat section carries one
`### §1 Introduction` over its paragraphs while a subsectioned one starts at `### §6.1`, and no
page opens a box onto nothing. This makes the shape checkable without reading the prose: the
subsection count is the number of `###` headings whose number contains a dot.

A `####` heading carries no icon. 🔹 belongs to a group title, which is a full-line `**bold**` that
genuinely leads a run of items, so never write a paragraph in bold. An optional full-line `(…)`
directly under a `####` heading is that paragraph's job: it renders in grey italic, stays on stage
as a scan hook, and only the line immediately after the heading is read that way. Keep it to about
80 to 120 characters.

For a new S page, compose this section at creation time: stage template first, venue template
second, previous Stage Contracts third. Write the resolved blueprint as direct `###` headings.
The new page owns those headings; build renders them but does not regenerate them.

S-only, optional: an exact direct `### Stage Record` is orientation metadata, so build.py lifts
it into Opening and keeps it collapsed when supplied. All other direct `###` sections remain
under Content.

Each direct `###` heading becomes one individually collapsible content subsection. Keep the old
stage prose under these headings rather than copying it into a second backing document.

### First content subsection
The actual content goes here, one sentence per line.

A sentence can carry apparatus: `>` lines written directly beneath it fold under that sentence, which shows a ⚑ badge until it is clicked. Human comments and edit records open by default so they remain visibly attached to their sentence.
> Note: this row is attached to the sentence above it, by adjacency alone.
> JL: a sentence-local comment · 260729 1502
> ✎ The whole sentence with ~removed~ *added* words. · JL · 260729 1503
> Citation: typed lanes name the attachment, one of Citation, Value, Display, Check, Q-consumer, Link, Source, Note; `> JL:` and `> CC:` threads join the same drawer.

**A lane is one source line, however long.** A wrapped continuation line becomes its own sentence
row on the page, takes its own ⚑ badge, and steals every lane written below it. This is the same
one-sentence-per-line rule as the prose, and it fails invisibly: the markdown looks fine and only
the generated page shows the broken row.

Adjacency is the whole binding, so a lane must sit under its own sentence: placed after a
paragraph it silently attaches to whatever line precedes it. A concern that belongs to the page
rather than to one sentence (a missing script, a sweep still owed) has no sentence to attach to
and belongs in `## Items to Finish`.

Use standard Markdown `![](path.png)` to show an image inline. The same form with a local `.pdf`
path, `![](path.pdf)`, renders a readable PDF object with an `open PDF` fallback link. On a
Display page, `preview.pdf` remains the generated Current Float; use an explicit PDF subsection
only when the reader also needs to inspect the underlying live display artifact.

### Second content subsection
Continue with the next coherent part of the stage.

#### P1. One paragraph of this division
(what this paragraph does, in one line, so the division can be scanned without being read)
The paragraph's prose starts on the line after the job line, still one sentence per line.
Delete the `####` heading and the `(…)` line together in a division that is a single block of prose rather than a run of numbered paragraphs.

## Items to Finish
required · A checklist, one line each, of what counts as done. Tick `- [x]` when met; the
heading auto-counts `1/2`. **Do not tick what has not been verified.**

Every item is `- ICON heading` with a folded explanation. Start the heading with an author-chosen
emoji icon (build.py never guesses one). The first indented line is a one-sentence summary; the
lines after it are the long explanation, written as a real paragraph (what it means, what
happened, why). Only the heading shows on stage; length is free in the fold.

- [ ] 🎯 First finish line
      One sentence saying exactly what this means and how it is judged met.
      The long explanation: the reasoning and history behind this line, as a paragraph.
- [ ] 🧪 Second finish line
      Written so it can be checked, not "basically there".
      The paragraph continues here.

For an S page, former Q-consumer records live here as recognizable checklist items. Keep the id,
stake, route, and answer together:

- [ ] 🔎 Q-Stage-1 · Concrete consumer question
      **Description:** What must be learned?
      **Reason:** Which content or claim depends on it, and what breaks if it fails?
      **Probe:** where the answer will come from. On a board laid over a paper tree that is a
      probe file, `-> 1-probes/PPNN_topic/QX1.md`; on a standalone board with no probe layer,
      name the real route instead (a task folder, a person, a meeting) or write `not opened yet`.
      **Answer:** Empty until the answer lands.

Tick a consumer only after its answer landed, was interpreted, and was woven into `## Content`.
A deferred consumer closes only after a forward pointer is recorded.

## Where we are
required · The actual present state, with numbers where numbers exist (not "basically done").

Open with one concise paragraph: what has been achieved, and what is still unproven. Then dated
items, each prefixed `YYMMDD WHO ·`; build.py strips that into a muted right-aligned stamp, so the
date and person never sit in the title text. Order by date. On S pages, summarize the stage; do
not repeat every consumer answer from Items to Finish.

- 260723 CC · 🔀 What changed on this date
      One sentence naming the change.
      The paragraph: what it was before, why it changed, what it cost.

## Files
optional (strongly recommended) · Which files this question moves or depends on. Paths in
backticks; those declared in `board.md`'s `## Links` become clickable.

- `path/to/thing.py`
  Its role in this question, and where you start when this question changes.
- `path/to/generated-thing`
  If it is generated, say "do not hand-edit".

## Law
optional · folded · Rules this question has settled and will follow from now on, one per line.
Do not write intentions here as if settled. Delete the section if unused.

## Lesson
optional · folded · Traps hit and lessons learned on this question, one per line. Keep them
specific (a concrete failure attached). Delete the section if unused.

## Glossary
optional · folded · Words on this page an outsider would stumble on, one per line: `term:
explanation`. Any coined phrase must be defined here or not used. Delete the section if unused.

## Discussion
optional · folded · Loose discussion, one line each. The "➕ Add to discussion" box on the page
writes here.
> JL: discussion goes here.
>> CC0724: reply with two angle brackets and a date.

## Log
optional (most questions have one) · folded · What changed on this question, one line each,
newest on top:
260724 1030 · what changed (`YYMMDD HHMM · ...`, time optional)
