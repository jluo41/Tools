# reading.yaml · what the agent writes after reading

One file per paper, in the reading folder. `read_paper.py shoot` and `draw` read it; the
drawing is named after the folder unless `--name` says otherwise.

```yaml
paper:
  pdf: ../../../../../_WorkSpace/1-SourceStore/<project>/papers/<paper>.pdf   # relative to this file, or absolute
  title: "<the paper's title>"
  cite: "<authors>, <venue> <year>; <versions and corrections>"
  link: https://doi.org/<doi>                       # optional, clickable on the canvas

section:                                          # optional: one Section of the paper, shown whole on the left
  name: "§1 Introduction"                           #   the frame reads "§1 Introduction, read"
  pages: [2, 4]                                     #   its first and last page
  from: "1 Introduction"                            #   optional: its first page starts at this heading
  until: "2 Literature Review"                      #   optional: its last page stops before this heading
  key:                                              #   optional: the map's key point, in the key-point yellow
    - "11 paragraphs: 2 KEEP · 7 REWRITE · 1 CUT · 1 MOVE"   # its verdicts are drawn with their emoji
    - "about 35 to 40% of its ~930 words stays"
  parts:                                            #   optional: its subsection headings, in order: a frame each
    - "2.1 Learning from Behavioral Experiments"

ours:
  title: "<our paper's working title>"
  source: <path to our paper's board, Section Page or story note>
  targets:                                          # our claims, with the ids our paper uses
    - id: C1
      label: "<the claim in one line>"

logic:                                              # 5 to 8 steps, in the paper's order
  - role: question                                  # question | gap | method | result | claim | limit
    text: "<one line>"
    excerpts: [E1]                                  # the excerpts this step rests on

excerpts:                                           # 5 to 9
  - id: E1
    page: 3                                         # where to look first; other pages are searched if it misses
    label: "<short card title>"
    quote: "<one or two sentences copied exactly from paper.txt, within one page>"
    crop: lines:3                                   # optional: lines:N (default 3) | block | page | [x0, y0, x1, y1] in PDF points
    mark: [[x0, y0, x1, y1]]                        # optional: extra boxes to highlight (a table row, a figure label)
    says: "<the source's claim, in our words>"
    comment: "<our reading: why it matters, a doubt, a later correction>"
    link: {to: C1, relation: supports, how: "<how our paper uses it>"}   # relation: supports | contrasts | borrows | cites | gap
    next: "<what our paper does with it, 10 words at most>"           # the note's third line on the canvas

open:                                               # the person's choices, drawn in red
  - "<question>"
```

A Section of our own paper read for a redesign gives each passage a verdict: its `comment` begins with
`KEEP:`, `REWRITE:`, `CUT:` or `MOVE:`, and its `link` names the review item that hits it (`how` begins with
the review points, `R2.13, E1.1: ...`). The canvas shows only the verdict, the label, the target with those
points, and `next`; `says` and `comment` stay here and in the face.

A table row or a figure has no `quote`: `pdftotext` reads table cells down each column, so a
row is never one run of words. Give `page`, a `crop` box and `mark` boxes instead; `read_paper.py
boxes <pdf> --page N --find <text>` prints each line's box in PDF points.

```yaml
  - id: E8
    page: 10
    label: "Figure 3, the four arms"
    crop: [120, 75, 500, 285]
    mark: [[166, 186, 268, 205]]
```

Checks `load()` makes before anything is drawn: the PDF exists, excerpt ids are unique, every
`link.to` is one of `ours.targets`, and every `relation` is one of the five.

What `shoot` does with a quote:
1. Normalizes it: case, punctuation, ligatures, and words broken by a line-end hyphen.
2. Matches characters with the spaces taken out, so a word the PDF splits or joins
   differently (`CI95` as `CI` + `95`, a citation number glued to a word) still matches to
   its last word.
3. Looks on the named page first, then on every other page; accepts the closest stretch if
   at least 0.8 of its characters align.
4. Crops 3 lines of context from the quote's own column (a two-column page never mixes),
   whole lines only, padded by at most half a line gap.
5. Writes `shots/<id>-p<page>.jpg` (200 dpi, JPEG quality 85) and records `match`, `status`
   and `shot` in `shots/index.json`.
