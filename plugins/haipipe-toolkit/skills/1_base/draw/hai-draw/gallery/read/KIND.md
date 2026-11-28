---
name: read
part-of: hai-draw
description: "Reads one paper's PDF onto an Excalidraw canvas: its logic as a chain, key passages shot from the PDF with quoted words highlighted, a comment on each, and how each links to our paper. Use for a paper reading canvas. Trigger: read this paper, screenshot the key parts, /hai-draw read."
allowed-tools: Bash, Read, Edit, Write, Grep, Glob
metadata:
  version: "0.10.3"
  last_updated: "2026-10-26"
  # version history: ./CHANGELOG.md
---

# /hai-draw read · one paper, its logic, its passages, our link

Read a paper's PDF, draw its logic, show the key passages highlighted on its own pages (not every
corner), comment on each, and say how each links to our paper.

```text
paper.pdf ─▶ paper.txt ─▶ reading.yaml ──────────▶ shots/page-p3.jpg ... ─▶ 〈name〉.excalidraw
  (text)      the agent     logic · excerpts ·       quote found by its       ① the map ② your call
              reads it      comments · links         words, highlighted,      ③ … one frame a part,
                                                     pages shown (shoot)      as stairs (draw)
```

The canvas is stairs (principle ③):
- **① how much changes** (or **its logic, and our link**): the key point in the key colour (principle ⑤;
  a reading's `key`), the argument as a flow of steps, each naming its passages, and what each passage
  answers to (our target, each passage's number and verdict).
- **② 🙋 Your call**: the `open` choices in red, small on purpose.
- **③ … one frame per part**: a paper read whole is one part; a Section with `parts` is one frame per
  subsection. Its pages on the left, each read passage highlighted in place and numbered in the margin; on
  the right one note per passage, level with it, in three short lines: its verdict and label, what it
  answers to (target and review points), and `next`, what our paper does with it.
  Its key point is the tally of its passages' verdicts. `says` and `comment` stay in reading.yaml and the face.


Steps
-----

```bash
R=Tools/plugins/haipipe-toolkit/skills/1_base/draw/hai-draw/gallery/read/ref/read_paper.py
.venv/bin/python $R text <paper.pdf> --out <pdf folder>/<paper stem>/   # paper.txt, page-marked
#   read paper.txt and our paper, then write <reading folder>/reading.yaml (ref/reading-spec.md)
.venv/bin/python $R boxes <paper.pdf> --page N [--find text]           # line boxes, for a table or figure
.venv/bin/python $R all <reading folder>/reading.yaml                  # shoot + draw + .png preview
.venv/bin/python $R paras <reading folder>/reading.yaml                # shots/para-P<k>.jpg: the Section's paragraphs, each whole
.venv/bin/python $R paras <reading folder>/reading.yaml                #   with section.blocks: an abstract's blocks, each whole, its words counted
```

1. **Place the files.** The PDF and its `paper.txt` are a download: keep them in the space's
   ignored `_WorkSpace/` (a source store). The reading folder holds `reading.yaml`, `shots/`,
   the drawing and its preview. In a reading project: `〈project〉/notes/reads/〈author〉-〈year〉-〈topic〉/`.
   In a Block: a studio topic made with `hai-studio`.
2. **Read our paper first.** Take the claims the link will point at from our paper itself:
   a paper Board's claims, a Section Page's Bullets, or a story note's C1..Cn. These become
   `ours.targets`, with their real ids; never invent an id.
3. **Read the paper, not every corner.** Read the abstract, the end of the introduction (the
   contribution), the design paragraph, the main result paragraph and its figure or table, the
   discussion's first claim, and the limitations. Skip related work except the sentence that
   names the gap, and skip appendices unless the key number lives there. `text` prints the
   figure and table captions with their pages.
4. **Write the logic first.** Five to eight steps, each with a role (question, gap,
   method, result, claim, limit) and the excerpts it rests on. Each step's `text` must fit
   on one line: 85 characters at most. Longer steps push the Paper logic frame past one
   screen, and `canvas.write` warns. The logic is the paper's own argument, not our opinion
   of it.
5. **Say how each step was done.** Under a step's words, its `how`: 1 to 4 lines of 12 words or fewer with the
   paper's own numbers, the data and models in the method step that sets up the study, each procedure step in its
   method step, the measures and headline numbers in its result step. Each line starts with its label, `Data:`,
   `Model:`, `Prompt:`, `Training:`, `Evaluation:`, `Baselines:`, `Result:`, so a reader can follow the setup.
   Read in order, the chain then says both what the paper argues and how it ran.
6. **Pick 5 to 9 excerpts.** One per step that needs proof, plus the line that matters most
   to our paper. Copy each `quote` exactly from `paper.txt`: one or two sentences, no
   ellipsis. Each excerpt gets:
   - **`says`**: what the source claims, in our words.
   - **`comment`**: our reading of it: why it matters, a doubt, or a later correction.
   - **`link`**: one of our targets, a relation, and how we will use it.

   Keep `says` and `comment` apart: a source claim never mixes with our interpretation.
7. **Tables and figures take a box, not a quote.** `pdftotext` reads a table cell by cell
   down each column, so a row is never one run of words and cannot be quoted. Run `boxes` on
   the page, then give the excerpt `page`, a `crop` box around the table or figure, and
   `mark` boxes for the row or label that matters (PDF points, `x0 y0 x1 y1`). Crop to the
   rows and columns the point needs, not the whole table width: a card is about 1,200 px
   wide, so a full-width table shrinks its marked cells.
8. **Build and look.** `all` prints one line per excerpt (`match 1.00 ok`).
   - **Below 0.8**: the quote is "not found". Recopy it from `paper.txt`, one sentence within
     one page.
   - **Between 0.8 and 0.99**: the quote is not word for word. Check that the highlight
     covers it all.

   Open the `.png` and check that each highlight sits on its lines and each note stands level
   with its passage. A Section read whole takes `section:` (ref/reading-spec.md). `crop`
   (`lines:N`, `block`, `page`, or a box in PDF points) shapes only the single shots in
   `shots/〈id〉-p〈N〉.jpg`; a table or figure's `crop` box is also what it highlights when it has
   no `mark`.
9. **Put the open questions in `open`.** These are choices the person makes (which version to
   cite, whether a domain argument holds), never verdicts we reached for them.


The canvas is shared
--------------------

`draw` writes with `hai-studio`'s `canvas.write` (marks kept, as every draw.py drawing). When the
person marks the canvas in red, follow `hai-draw report`'s comment loop:
1. Read the marks.
2. Fold each decision into `reading.yaml`: change a `comment` or `link`, add an excerpt, or
   answer an `open` question.
3. Rebuild.
4. Ask the person to reload the open tab.

Never move or restyle their marks.


Rules
-----

1. **The paper's words, highlighted in place.** The left of each part frame is the PDF's pages
   themselves (`shots/page-p〈N〉[-〈part〉].jpg`, 150 dpi), every quote under a yellow marker where
   it stands. A short paper shows its pages with passages whole; past 4 pages, each is cut to its
   passages (6 lines above, 4 below). A reading's `section:` shows a Section of a paper whole,
   from its heading to the next, cut at its `parts` headings between whole lines; an opening
   with no passage joins the first part. A nine-page Section weighs about 2 MB. No retyped
   quotes on the canvas. `shots/〈id〉-p〈N〉.jpg`, each passage cropped with 3 lines of context, is
   still written for hai-draw task's readings.
2. **Every excerpt links or says why not.** An excerpt without `link` shows in red under
   "Not linked", and a target with no excerpt shows "no excerpt links here yet". Both are
   prompts, not errors.
3. **Five relations only.**
   - `supports`: it backs our claim.
   - `contrasts`: it argues the other side.
   - `borrows`: we use its method or definition.
   - `cites`: background we cite.
   - `gap`: it leaves open what we fill.
4. **Name corrections.** When a published version, erratum or correction changes a number in
   the PDF being read, say so in that excerpt's `comment` with the date. A shot of an
   outdated line must not read as current.
5. **Its own words.** A reading keeps its own word counts and sizes; a part frame reads top to bottom.
   After every build, run hai-draw's `scripts/check.py 〈drawing〉`: it names principles ⑥ and ⑦ for a
   reading and does not judge them; every other principle holds.

Needs poppler (`pdftotext`, `pdftoppm`), Pillow and PyYAML. The writer and the previewer are
`hai-studio`'s `scripts/canvas.py` and `scripts/render_png.py`. For the real Excalidraw
render of one frame, use `hai-draw report`'s `ref/render_excalidraw.py --frame "Paper logic"`.

Worked example: `〈Notes-SPACE〉/examples-1-theory/Project-Psych-Theory/notes/reads/salvi-2024-gpt4-persuasion/`.
It reads Salvi et al.'s GPT-4 persuasion trial against a megastudy paper's claims C1, C2 and C5.


A topic of papers
-----------------

Several papers on one theme can share one Studio topic: the theme first, then one row per paper, each
paper's pages whole with its passages highlighted and a numbered note level with each, then its logic and
its links to our paper.

```bash
.venv/bin/python $R text <paper.pdf> --out _WorkSpace/.../<paper>/     # as above, one per paper
#   write <topic>/reads/<id>-<paper>/reading.yaml, then: $R all <that reading.yaml>
.venv/bin/python ref/topic_drawing.py draw <topic folder>                # or the topic's own build_sNN_*.py
```

1. **The face holds the words.** A `related:` yaml block: `key`, `what`, `why`, the `papers` in reading order
   (`id`, `item` as its `related/related.md` row starts, `says` in one line, `ref` its reference: title, every
   author from Crossref or arXiv, venue, year, link) and `open` (see the script's header). Each paper's row opens
   on its reference frame.
2. **One reading per paper**, `reads/〈id〉-〈paper〉/reading.yaml`, its `paper.pdf` the Block's `related/paper/` file.
3. **Unread is red.** A paper with no reading yet shows as one red card: "PDF kept, not read yet" or "no PDF yet".
4. The page frame is hai-draw task's `transcript_frame` with `noun="paper"`, `us="Our paper"`. Worked example:
   `〈Project-SPACE〉` `Paper-LLMRecPhy-Jama/s07-related-work-audits-of-who-llms-name/`.


Boundary
--------

This kind reads one paper and draws it; it writes nothing into our paper. Adding the citation
or a claim to our paper belongs to `hai-paper` and the Page evidence skills. A Discovery
Result card for the paper belongs to `hai-discovery`. Revise mode, a file we change, is the draft
kind's (`gallery/draft/KIND.md`); it draws its pages with this kind's `ref/read_paper.py`. A question's
working scratch or report drawing is `hai-draw report`. A paper's own Section map is `hai-draw draft`.
