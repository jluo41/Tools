# Page writing rules

This file governs Page prose. `board-form.md` owns structure;
`haipipe-page` owns section meaning and evaluation order.

## Write for a new reader

- Use plain English and concrete nouns.
- Define a necessary specialist term at first use or in `## Glossary`.
- Do not invent a label when the source already has a stable name.
- Give counts, paths, versions, or named evidence instead of “basically done.”
- Remove scaffolding phrases that could fit another Page after swapping nouns.
- Keep history, attribution, and retirement stories in
  `outline/<stem>-log.md`, not current Page prose.

## Keep each section in one role

| Section | Reader question |
|---|---|
| Opening | What is this Page, why does it matter, and what does it own? |
| Outline | How is the Page planned and supported? Generated from `outline/`. |
| Content | What does the Page establish? |
| Aims | What must become true, how is it tested, and what is true now? |

Move a sentence when it answers another section's question. Opening is
orientation, not a miniature Content section. Content is substance, not a
status report. Aims are durable targets, not a temporary task list.

## Write a focused Opening

The visible Opening is one flowing, Page-specific paragraph. It should let a
new reader name the subject, the stake, and this Page's boundary without
opening another record.

- Target roughly 450 visible characters and never exceed the checker ceiling.
- Use ordinary subject language before internal ids or Run addresses.
- Put optional supporting detail after the first blank line.
- Use labelled parts in More details; do not add one undifferentiated block.
- Do not add a separate Boundary section.

A manuscript Section uses its stricter Page-owner contract. Its reader Opening
contains only the paragraph; requirements remain in the Outline workspace.

## Number Content for navigation

```text
### 3 · Division
**3.1 · Group**
#### 3.1.1 · Paragraph
(the job this paragraph performs)
```

The number carries depth. A Page has one foldable Content-division level; do
not create a deeper heading tree. Use a bold group title only when it leads a
real list. A paragraph heading does not carry an icon.

Each Content division begins with a captioned face diagram when its Page-owner
contract requires one. A caption precedes the fence and states what the figure
shows. A figure row is a label and value, not a prose sentence. Keep ASCII
figures narrow and copy-safe; stack trees instead of drawing ambiguous columns.

## Trace prose to the plan

When the Page-owner contract uses Bullet realization, one paragraph realizes
the approved Bullets under its `C<n>.P<m>` group. A Bullet is a trace unit,
not another paragraph. Write one sentence per source line and put the exact
backlink on each sentence that realizes that Bullet:

```html
<!-- realizes: C<n>.P<m>.B<k> -->
```

A paragraph may cover several Bullets while keeping each sentence's support
local to its own Bullet. For a Section, use the owner's sentence-slot rule;
for other Pages, one Bullet may require one or more sentences within the
planned paragraph. Do not split or merge approved paragraph groups just to
satisfy a writing worker; a changed paragraph job or structure returns to SHAPE.
Headings, diagrams, machinery, and ruling tables are not prose realization units.

## Write one Aim as one row

```markdown
- 🔨 A2.1 · <durable target>
  **Done when:** <observable test>
  **Now:** <one current fact>
  **Plan:** <optional immediate route>
```

The tick and `Now:` describe the same current state. Keep only the latest fact;
record transition reasons in `outline/<stem>-log.md`. Use `Plan` only when an
immediate route is worth preserving.

A blocking human choice belongs under `### Decision Now`. Give each option its
own line, name its consequence, state what is blocked, and provide a default
when nothing blocks. Once answered, remove the pending row and record the
ruling in its durable owner.

## Preserve sentence-level records

Write one prose sentence per source line. The browser soft-wraps it. A hard
line break creates a second address and can detach the apparatus below it.

- `> Comment WHO …` records a sentence-local comment.
- `> ✎ …` records a sentence-local edit.
- `> Card <words>: …` attaches a panel to exact words in that sentence.

Never erase a human comment or edit record. A Page-wide issue belongs in Aims
or an Outline record rather than under an arbitrary sentence.

## Avoid machine-shaped prose

- No em dash.
- No empty intensifiers or ceremonial transitions.
- No fixed rhetorical checklist repeated across Pages.
- No author notes explaining the markup.
- No clause-packed figure rows.
- No heading that is a full sentence.

Titles are functional labels, not headlines. Use three to five visible words
and never exceed six. Name the Page's subject and the work or deliverable it
owns in plain, objective language. Do not put a joke, marketing phrase,
surprise, accusation, or unqualified finding in the title; put results,
caveats, and interpretation in Opening or Content, where their scope can be
stated. A heading is a lookup key: it states the rule or purpose, contains no
date, and does not refer to “this document.”

## Finish on the rendered Page

A source edit is incomplete until the Board is rebuilt and the render has been
read. Check both structure and prose:

```bash
python3 <skill>/cli/build.py <board-folder>
python3 <skill>/cli/check.py <board-folder> --strict
```

Then use a fresh-context reviewer. Ask it to report only:

1. an unreadable sentence and its failure type;
2. an undefined term;
3. a missing premise;
4. an interchangeable or templated paragraph.

The Page is ready when no part is unreadable, every remaining gap is explicit,
and the changed prose cannot be reused on another Page by replacing nouns.
