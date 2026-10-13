---
name: excalidraw-read
description: >-
  Read one paper's PDF onto an Excalidraw canvas: the paper's logic as a chain (question, gap,
  method, result, claim, limit), its key passages shot from the PDF with the quoted words
  highlighted, a comment on each, and how each passage links to our paper (supports,
  contrasts, borrows, cites, gap) against our paper's own claims. Reads the parts that carry
  the argument, not every corner. A file we change, shown section by section with its
  changes, is excalidraw-revise. Use for "read this paper", "draw this paper", "screenshot
  the key parts", "how does this paper link to ours", a paper reading canvas, /excalidraw-read.
allowed-tools: Bash, Read, Edit, Write, Grep, Glob
metadata:
  version: "0.6.0"
  last_updated: "2026-10-13"
  # version history: ./CHANGELOG.md
---

# /excalidraw-read · one paper, its logic, its passages, our link

JL 261010: "a skill which will try to read a paper of its pdf, and extract the paper logic and
then screenshot the sections with the highlighted part, (no need to check every corner of them)
and then add the comments, and how that will link to our paper."

```text
paper.pdf ─▶ paper.txt ─▶ reading.yaml ──────────▶ shots/E1-p3.jpg ... ─▶ <name>.excalidraw
  (text)      the agent     logic · excerpts ·       quote found by its       Paper logic · Link to
              reads it      comments · links         words, highlighted,      our paper · Questions ·
                                                     cropped (shoot)          Excerpts (draw)
```

The canvas has four frames:
- **Paper logic**: the argument, one box per step, each naming the excerpts it rests on.
- **Link to our paper**: each of our claims with the excerpts that touch it.
- **Questions**: what the person must decide, in red.
- **Excerpts**: one card per passage: the highlighted shot, `Says:`, `Comment:`, `-> Ours`.


Steps
-----

```bash
R=Tools/plugins/haipipe-toolkit/skills/1_base/display/excalidraw-read/ref/read_paper.py
.venv/bin/python $R text <paper.pdf> --out <pdf folder>/<paper stem>/   # paper.txt, page-marked
#   read paper.txt and our paper, then write <reading folder>/reading.yaml (ref/reading-spec.md)
.venv/bin/python $R boxes <paper.pdf> --page N [--find text]           # line boxes, for a table or figure
.venv/bin/python $R all <reading folder>/reading.yaml                  # shoot + draw + .png preview
```

1. **Place the files.** The PDF and its `paper.txt` are a download: keep them in the space's
   ignored `_WorkSpace/` (a source store). The reading folder holds `reading.yaml`, `shots/`,
   the drawing and its preview. In a reading project: `<project>/notes/reads/<author>-<year>-<topic>/`.
   In a Block: a studio topic made with `haipipe-studio`.
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
5. **Pick 5 to 9 excerpts.** One per step that needs proof, plus the line that matters most
   to our paper. Copy each `quote` exactly from `paper.txt`: one or two sentences, no
   ellipsis. Each excerpt gets:
   - **`says`**: what the source claims, in our words.
   - **`comment`**: our reading of it: why it matters, a doubt, or a later correction.
   - **`link`**: one of our targets, a relation, and how we will use it.

   Keep `says` and `comment` apart: a source claim never mixes with our interpretation.
6. **Tables and figures take a box, not a quote.** `pdftotext` reads a table cell by cell
   down each column, so a row is never one run of words and cannot be quoted. Run `boxes` on
   the page, then give the excerpt `page`, a `crop` box around the table or figure, and
   `mark` boxes for the row or label that matters (PDF points, `x0 y0 x1 y1`). Crop to the
   rows and columns the point needs, not the whole table width: a card is about 1,200 px
   wide, so a full-width table shrinks its marked cells.
7. **Build and look.** `all` prints one line per excerpt (`match 1.00 ok`).
   - **Below 0.8**: the quote is "not found". Recopy it from `paper.txt`, one sentence within
     one page.
   - **Between 0.8 and 0.99**: the quote is not word for word. Check that the highlight
     covers it all.

   Open the `.png` and read every shot. To change a crop, use one of these `crop` values:
   - `lines:N` for N lines of context;
   - `block` for the whole paragraph block;
   - `page` for the whole page;
   - a box in PDF points.
8. **Put the open questions in `open`.** These are choices the person makes (which version to
   cite, whether a domain argument holds), never verdicts we reached for them.


The canvas is shared
--------------------

`draw` writes with `haipipe-studio`'s `canvas.write`, so the person's own marks survive every
rebuild. Edits the person made to a seed element are kept, and deletions stay deleted. When
the person marks the canvas in red, follow `excalidraw-report`'s comment loop:
1. Read the marks.
2. Fold each decision into `reading.yaml`: change a `comment` or `link`, add an excerpt, or
   answer an `open` question.
3. Rebuild.
4. Ask the person to reload the open tab.

Never move or restyle their marks.


Rules
-----

1. **The paper's words, highlighted in place.** A shot is the PDF page itself, cropped
   around the quote with 3 lines of context from the same column, with the quote under a
   yellow marker. Shots are JPEGs, so a reading of 8 passages weighs about 2.5 MB. No
   retyped quotes on the canvas.
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
5. **Readable at 50% zoom.** The canvas keeps words at 20 px or more and frames within one
   screen, except Excerpts, which reads top to bottom. `canvas.write` prints a warning when
   either rule breaks.

Needs poppler (`pdftotext`, `pdftoppm`), Pillow and PyYAML. The writer and the previewer are
`haipipe-studio`'s `scripts/canvas.py` and `scripts/render_png.py`. For the real Excalidraw
render of one frame, use `excalidraw-report`'s `ref/render_excalidraw.py --frame "Paper logic"`.

Worked example: `Knowledge-SPACE/examples-1-theory/Project-Psych-Theory/notes/reads/salvi-2024-gpt4-persuasion/`.
It reads Salvi et al.'s GPT-4 persuasion trial against a megastudy paper's claims C1, C2 and C5.


A topic of papers
-----------------

Several papers on one theme can share one Studio topic (JL 261013: "add more sNN to show the related paper by
topics ... using /excalidraw-read"): the theme first, then one row per paper, each paper's pages whole with its
passages highlighted and a numbered note level with each, then its logic and its links to our paper.

```bash
.venv/bin/python $R text <paper.pdf> --out _WorkSpace/.../<paper>/     # as above, one per paper
#   write <topic>/reads/<id>-<paper>/reading.yaml, then: $R all <that reading.yaml>
.venv/bin/python ref/topic_drawing.py draw <topic folder>                # or the topic's own build_sNN_*.py
```

1. **The face holds the words.** A `related:` yaml block: `key`, `what`, `why`, the `papers` in reading order
   (`id`, `item` as its `related/related.md` row starts, `says` in one line, `ref` its reference: title, every
   author from Crossref or arXiv, venue, year, link) and `open` (see the script's header). Each paper's row opens
   on its reference frame (JL 261013: "for each paper, you didn't give the paper reference, the names, the authors").
2. **One reading per paper**, `reads/<id>-<paper>/reading.yaml`, its `paper.pdf` the Block's `related/paper/` file.
3. **Unread is red.** A paper with no reading yet shows as one red card: "PDF kept, not read yet" or "no PDF yet".
4. The page frame is excalidraw-task's `transcript_frame` with `noun="paper"`, `us="Our paper"`. Worked example:
   Physician-SPACE `Paper-LLMRecPhy/studio/s07-related-work-audits-of-who-llms-name/`.


Revise mode moved
-----------------

A file we change (a co-author's Word file, an IRB protocol), drawn section by section beside the updated
sentences, with the tracked Word file built last, is its own skill since 261013: `excalidraw-revise`
(`skills/1_base/display/excalidraw-revise/`). It still draws its pages with this skill's `ref/read_paper.py`.


Boundary
--------

This skill reads one paper and draws it; it writes nothing into our paper. Adding the citation
or a claim to our paper belongs to `haipipe-paper` and the Page evidence skills. A Discovery
Result card for the paper belongs to `haipipe-discovery`. A file we change is `excalidraw-revise`. A question's working scratch or
report drawing is `excalidraw-report`. A paper's own Section map is `excalidraw-section`.
