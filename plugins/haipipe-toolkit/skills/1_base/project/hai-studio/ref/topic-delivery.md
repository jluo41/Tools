# The delivery · one topic, one idea, one delivery

Part of hai-studio's topic contract (`ref/topic-contract.md`).

A Studio runs from idea to delivery. Each topic holds one idea and ends in its own delivery, named first on its
face, in the `**For:**` line. A Block's delivery is its topics' deliveries together, listed in its `board.md`
`## Deliveries`.

## One clean thing of one type

The delivery is a deck, always, and one thing the deck is about: a skill, a draft, a display, workbench code, a data
table or a server package. A mixed delivery is several topics, one per type. No clean delivery, no topic.

The face says the type in one word, the `**Delivery type:**` line under `**For:**`. The deck is never the type,
since every topic has one. The type says what `delivery/` holds beside `deck/` and how `render.yaml` hands it over;
the workbench shows it on the topic's card.

```text
type     delivery/ holds             render.yaml hands it over as
skill    skill/ text pieces          from: to: block:   render_delivery.py writes them into a SKILL.md or ref/
ui       ui/ screen drafts           code: by:          a Task builds the screen in the workbench
code     the package's agreed spec   code: by:          a Task builds it (a script, a server package, an algorithm)
draft    web/ latex/ word/           from: rendered_by: the Theme's skill builds the Word, PDF or LaTeX
display  figure/ table/ slide/       from: rendered_by: hai-display renders the figure or table
data     the table's contract        code: by:          a Run writes the table to its store
```

## The kind of topic and its first question

The thing a topic delivers gives the topic its kind and the first question it must answer.

```text
every topic      deck (slides)           what a reader takes away, in pictures
story            story, Section plan     the claim, for which reader (a paper's Block)
question         report page             what answers it
table contract   data table              what one row means
display          figure                  what the figure shows
paper version    full paper, Word, PDF   what this send holds (a paper's version Job, assembled)
section          written Section         what this Section must say (a paper's draft Task)
label contract   schema, label contract  what one label means (a labeling Job)
items, building, scanning, score         a labeling Task's own: item set · signed Label Handoff · final labels · score
run plan         server package, code    which Runs, in what order
design           skill, tool change      what the tool should do
algorithm        algorithm code, tuner   its forward, loss and metric
ask              letter, meeting note    what we need from whom
```

## From delivery/ to where it is used

Two steps. The agreed, clean version goes into the topic's `delivery/` (never `result/`, which is messy by design).
Then a render writes it out to where it is used. `delivery/render.yaml` lists the pieces; a piece is one of three:

1. **A text piece** (`from:`, `to:`, `block:`): `render_delivery.py` writes it into its target between two marker
   lines; that region is edited only in the topic's `delivery/`.
2. **A code piece** (`code:`, `by:` a Task): built by the Task the line names, never copied.
3. **A Theme piece** (`from:`, `rendered_by:` the Theme's skill): `render_delivery.py` only reports it; the Theme's
   skill builds it (a paper's manuscript, a designs.json release).

The deck stays in `delivery/deck/`. `python $S/render_delivery.py <sNN>` checks every piece (same, differs, not
placed); `--apply` writes the ones that differ.

## One Studio, every Theme

The Studio is the same in every Theme: a topic beside the Jobs or Tasks it serves, its face, its drawing, its
`delivery/`, and a render out. A Theme plugs in by three things only: the kinds of delivery its topics make, where
the render writes, and which skill renders. The Theme's own skill renders; hai-studio never builds a paper, a
label set or a release itself.

```text
Theme      a topic delivers (Block · Job · Task)                     render writes into               rendered by
work       skill design · table contract · display, a figure         a skill, the workbench, a store  render_delivery.py, a Task
paper      story · paper version · section                           the Section page, manuscript     hai-paper-assemble
display    a figure or table, its slide rules                        the page's displays              hai-display
labeling   label contract · items, ground truth, building,           the labeling Job                 hai-labeling
           scanning, score
design     design goals · design Job · reason ideas, one design,     designs.json, the release        hai-design-delivery
           review whole
insight    question map · analysis plan, a release on a freeze ·     the Design handoff               hai-insight
           Data, Information, Knowledge, Wisdom
discovery  a question's evidence · a paper's card                    the evidence Bib                 hai-discovery
cowork     ask, a letter or meeting note                             sent to a person                 a person, hai-cowork
```
