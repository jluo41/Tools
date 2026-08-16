# Content plan — the contract between "who has the content" and "who renders it"

`display/` renders. It does **not** know where content came from — a paper, a grant
application, a project write-up, a talk outline someone typed by hand. Everything a
renderer needs arrives as a **content plan**: one markdown file plus a folder of figures.

```
   whoever has the content              display/ renderer
   ────────────────────────             ─────────────────────────────────
   display/skills/paper-poster    ──►   haipipe-display-poster   → A0 PDF · PPTX · SVG
   display/skills/paper-slides    ──►   haipipe-display-slides   → PDF · PPTX
   (an application, a talk, you)  ──►   same renderers, same contract
        writes the plan below                reads it, never reads the source
```

**The rule that makes this work:** a renderer never opens `main.tex`, never globs
`sections/*.tex`, never assumes a paper exists. If it needs something, it must be in
the plan. If the plan is missing something, the renderer says so and stops — it does
not go hunting.

## What you hand over

| Thing | What it is |
|---|---|
| `<plan>.md` | The content plan — one of the two shapes below |
| `figures/` | A folder of image files the plan refers to by filename |

Figures: `.pdf` / `.png` / `.jpg` / `.svg`. The renderer copies them (never symlinks —
`pdflatex` can't reliably follow symlinks across directories) and converts PDF→PNG at
300 DPI when it needs to embed them in PPTX (python-pptx cannot embed PDF).

## Shape 1 — poster content plan

Consumed by `haipipe-display-poster`. A poster shows roughly a third of a long
document, so the plan is a **selection**, already made. The renderer lays out what it
is given; it does not decide what to cut.

```markdown
# <title>
authors: <author line as it should print>
venue: <venue name>          # picks the colour scheme
size: A0 | A1
orientation: portrait | landscape
columns: 3 | 4
link: <URL for the QR code — paper, code, or project page>

## Stat callouts
Three or four headline numbers. These replace the abstract entirely — they are the
single highest-impact thing on the poster for 60-second comprehension.

- 94.2% — accuracy on the held-out cohort
- 3.1× — faster than the previous pipeline
- 12,847 — patients

## Boxes
One `### ` per box, in reading order. `col:` places it; `figure:` and `stats:` are
optional. Keep each box inside its stated word budget — the renderer will not trim.

### Background & Motivation
col: 1
words: 120-160
- <bullet>
- <bullet>

### Contributions
col: 1
words: 80
1. <numbered contribution>
2. <numbered contribution>

### Architecture
col: 2
figure: architecture.pdf
caption: <one line>
words: 80-120
- <bullet>

### Main Result
col: 3
figure: results.pdf
caption: <one line>
stats: | Model | Acc | F1 |
       | ours  | .94 | .91 |
words: 150-200

### Conclusion
col: 4
words: 60-80
- <finding>
- <next step>
```

**Total prose target: 300–500 words**, excluding figure captions and the callout
numbers. Whoever writes the plan owns that budget.

## Shape 2 — talk outline

Consumed by `haipipe-display-slides`. One `## ` per slide, in order. Slide count
should already match the talk length — the renderer does not add or drop slides.

```markdown
# <title>
authors: <author line>
venue: <venue name>
talk: oral-15min | spotlight-5min | lightning-2min   # sets the expected slide count

## <slide heading>
figure: architecture.pdf     # optional
- <bullet>
- <bullet>
notes: <what the speaker says on this slide — becomes the beamer speaker note>

## <slide heading>
- <bullet>
notes: <...>
```

## Writing rules that apply to both

These belong to whoever writes the plan, not to the renderer:

- **Never invent citations.** Only references that exist in the source's bibliography.
- **De-AI the prose** — no *delve, pivotal, underscore, noteworthy, leverage,
  facilitate, harness*.
- **Numbers must be real.** Every callout and every table cell traces to a result the
  source actually reports.

## When a renderer refuses

A renderer stops and says what is missing rather than guessing. It will refuse on: a
plan file that does not parse into the shape above, a `figure:` naming a file that is
not in `figures/`, a box with no `col:` (poster), or a talk with no slides.
