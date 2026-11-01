One topic, one idea, one delivery (261030)
------------------------------------------

A Studio runs from idea to delivery (JL 261030: "studio: from idea to delivery"; "one studio, one idea and one
delivery"). Each topic, s01 as much as s07, holds one idea and ends in its own delivery, named first on its face
(`**For:**`, "so one studio should link to a delivery, this is the outcome oriented"). A Block's delivery is its
topics' deliveries together, listed in its `board.md` `## Deliveries`.

The thing is **one clean thing of one type**: a skill, a draft, a display, workbench code, a data table, a server
package (JL 261030: "so each studio with a clear delivery, right? either skills or draft, or display"). A mixed
delivery is several sNN, one per type; no clean delivery, no sNN ("is the delivery is not clean or is not one type, we
will not treat it as a studio"). b35 went from seven sNN to three this way (b35 board.md `## Deliveries`).

Its face says which type in one word, the `**Delivery type:**` line under `**For:**` (JL 261030: "for each delivery,
we should also say what is the type, give the main delivery type"; "we should also add this to the skill, that what
type of delivery we want to render"). The deck is never the type, since every sNN has one. The type says what
`delivery/` holds besides `deck/`, and how `render.yaml` hands it over; the workbench shows it on the sNN's card,
beside its stage:

```text
type     delivery/ holds             render.yaml hands it over as
skill    skill/ text pieces          from: to: block:  render_delivery.py writes them into SKILL.md or ref/
ui       ui/ screen drafts           code: by:         a Task builds the screen in the workbench
code     the package's agreed spec   code: by:         a Task builds it (a script, a server package, an algorithm)
draft    web/ latex/ word/           from: rendered_by: the Theme's skill builds the Word, PDF or LaTeX
display  figure/ table/ slide/       from: rendered_by: haipipe-display renders the figure or table
data     the table's contract        code: by:         a Run writes the table to its store
```

A delivery is a deck, always, and the thing the deck is about (JL 261030: "delivery could be: slide (a must) and the
associated skills, code, or figures, draft, etc."). The thing gives the topic its kind and its first question (b35-s01, a scan of every `studio/` topic and `delivery/`
folder in the eight SPACEs, 261030):

```text
every topic      deck (slides)          a must: what a reader takes away, in pictures
story            story, Section plan    the claim, for which reader (a paper's Block)
question         report page            what answers it
table contract   data table             what one row means
display          figure                 what the figure shows
paper version    full paper, Word, PDF  what this send holds (a paper's version Job, assembled)
section          written Section        what this Section must say (a paper's draft Task)
label contract   schema, label contract what one label means (a labeling Job, b15 s13)
items, building, scanning, score       a labeling Task's own: item set · signed Label Handoff · final labels · score
run plan         server package, code   which Runs, in what order
design           skill, tool change     what the tool should do
algorithm        algorithm code, tuner  its forward, loss and metric (hainn L1-L2)
ask              letter, meeting note   what we need from whom
```
