# Changelog

## 0.7.0 · 2026-10-14 · Stairs: the map, your call, one frame a part; the pages left, short notes right

- JL 261014, on the notes beside the pages: "this things are too wordy, I feel you didn't follow the principles of
  draw design, right?" The drawing now follows excalidraw-studio's principles and passes its `check.py`: stairs (each
  frame lower and further right, an act named at its left, a named arrow down to the next); ① the map: the key point
  in the key-point yellow (a reading's `key`), the argument as a flow, what each passage answers to; ② 🙋 your call,
  in red; then one frame per part. Each note is three lines of 28 px or more: verdict and label, target and review
  points, and the excerpt's new `next` (10 words at most). `says` and `comment` stay in reading.yaml and the face.
- JL 261014: "for the section like s15, we have more subsection, I think we can use the stair to show each subsection
  as well, to seperate them". A `section:`'s new `parts` (its subsection headings, in order) cut it into one frame
  per subsection, cut between whole lines; an opening with no passage joins the first part. Each part's key point
  is its passages' verdict tally.
- JL 261014, on the seven Section readings of Paper-TestToLearn-MS2026 (s10 to s16) drawn as two columns of excerpt
  cards: "not this version"; "what we want is still the screenshot in the left, and the comments in the right". The
  Excerpts cards are gone: the PDF's pages sit on the left with every passage highlighted where it stands and
  numbered in the margin, and one note per passage on the right, level with it, as `topic_drawing.py` and
  excalidraw-task's `transcript_frame` already drew a paper or a transcript.
- `shoot` also writes `shots/page-p<N>.jpg` and `shots/pages.json` (each passage's height on its page): a short paper's
  pages with passages whole, a long one's cut to them, a running header ("DRAFT") dropped.
- A reading's optional `section:` (`name`, `pages`, `from`, `until`) shows one Section whole, from its heading to the
  next one's, so our own draft can be read paragraph by paragraph against its review. Badges on touching lines stack.

## 0.6.0 · 2026-10-13 · A topic of papers

- JL 261013: "add more sNN to show the related paper by topics, just like ... s52-t06 ... using /excalidraw-read";
  "we might want to see the most relevant papers in the details". New `ref/topic_drawing.py draw <topic>`: a
  Studio topic of several papers on one theme, its face's `related:` yaml the words, each paper's reading in
  `reads/<id>-<paper>/`. Act 1 is the theme (key point, what the papers share, why it matters, one card per
  paper, the open choices in red); then one row per paper: its pages whole with the read passages highlighted
  and a numbered note level with each (excalidraw-task's `transcript_frame`, which gains `noun` and `us`), then
  its logic and the links to our paper. A paper not read yet is one red card. First used on Paper-LLMRecPhy
  s06 to s10.
- Each paper's row starts with its reference frame (JL 261013: "for each paper, you didn't give the paper
  reference, the names, the authors"): title, every author, venue and year, link, PDF, deep read and the version
  read, from the face's `ref:` block; the theme's cards carry each full title.

## 0.5.0 · 2026-10-13 · Revise mode is its own skill

- JL 261013: "I think we want to have the /excalidraw-revise, a new skill for this type of tasks". The revise
  mode (`ref/read_revise.py`, `ref/track_changes.py`, `ref/revise-spec.md`) moved to `excalidraw-revise`; this
  skill keeps reading one paper, and `ref/read_paper.py`, which the revise drawing still uses for its pages.

## 0.4.0 · 2026-10-11 · Delivery from the draft; one box per paragraph

- JL 261011: "OKAY, PLEASE DO IT" (the delivery, the last step). `read_revise.py deliver` writes the plan's `draft`
  Word file from the topic's draft: the draft's words against the original file's, word by word (difflib), become
  the smallest tracked changes, each find made unique in the file (else located after the nearest untouched
  paragraph); a draft paragraph that starts inside a file paragraph becomes a tracked new paragraph mark; the
  plan's image changes and its deletions of guidance are kept; each evidence item is a comment on its anchor (or on
  the first words of its sentence when the anchor's words changed). It checks that rejecting every change gives the
  file and accepting every change gives the draft, then prints the PDF with LibreOffice. All three SHIFT Blocks
  pass both checks (b31 20 changes, b21 14, b32 27).
- A comment anchor that is not in the draft, or appears more than once, is reported with the reason before its comment
  moves to the first words of its sentence (asked by b21_event_cgm, whose table repeated three anchors).
- `ref/track_changes.py`: b31_prep_ai's tracked-changes writer, shared here, with `split` (cut a paragraph before a
  phrase; its new mark is a tracked insertion).
- JL 261011: "IT IS NOT GOOD WE HAVE ONE PARAGRAPH WITH 17 SENTENCES". The middle column draws one box per draft
  paragraph, labelled `P<n> · <brief>`; a section's heading counts its paragraphs.

## 0.3.2 · 2026-10-11 · Seed fixes found on b32

- A line break inside a Word cell or paragraph is read as a space (a table cell had "issued.Q4" run together).
- A change whose part is named by its heading ("References", "Overview Figure") is tagged like one named by id.
- A change of punctuation only (",") tags the sentence its new text sits in.
  Found by the agent that moved b32_aid_ai's s04 to sentence mode; checked by reseeding b32 (all 26 changes with
  text tagged) and b31 (unchanged) on copies.

## 0.3.1 · 2026-10-11 · Sentence mode reads a haipipe-draft draft

- JL 261011: "we should have the draft folder following the /haipipe-draft". The sentence draft is now a Page
  draft folder: `draft/<stem>-draft-v<G>.<S>.md` (one current version, three sections, written and read through
  haipipe-draft's own `plan_layout`), `previous/` for older versions, `records/` for the writing log. A Bullet is
  a sentence (`- B<k> · S<n> · <sentence>` in `## 3 · Draft`); its Point and `Change:` line sit in `## 1 ·
  Structure`. Paragraphs follow the file's. `seed` writes v1.0; `edits --apply` writes by address (C3.P5.B7).
- The one-line-per-sentence file of 0.3.0 is retired (b31's moved into `draft/`).

## 0.3.0 · 2026-10-11 · Revise mode: the updated text as sentences

- JL 261011, on the updated page's picture: "we don't have this, but use the text to replace it"; "The
  Sentences of para, should come from the draft of the sNN"; "the draft is something together with the
  haipipe-writing"; "the delivery, we can think about it in the last step".
- Plan key `sentences`: the middle column becomes one editable text box per sentence, read from a draft file in
  the topic (format in `ref/revise-spec.md` § Sentence mode); changed sentences green with their change numbers,
  notes level with them; no updated PDF is printed or rendered (a rebuild of b31 s04 went from about 20 s to 7 s).
- `read_revise.py seed` writes that file once from the tracked Word file, each sentence tagged with the changes
  whose added words fall in it; `edits --apply` folds a person's sentence edits into it. Built on the sentence
  reader (`draft_units`, `split_sentences`) and `edits` command added the same day by the b31_prep_ai_content
  session.

## 0.2.1 · 2026-10-11 · Revise mode: notes smaller, in three columns

- JL 261011, on the notes column: "The content or the font size, can be much smaller, than the main content
  AND the comments can be much wider, in the right part. more columns".
- Notes at 14 px (titles 16), marked `canvas.aside` so `small_text` leaves them out; three columns of 360 px,
  each note in the column where it sits highest, level with its words; a change quotes at most 24 words.
  A first-column note has an arrow; further right, the number matches. The section frame is about 3,320 px
  wide, over FRAME_MAX's 2,800, as asked.
- `change_notes` in the plan: green ✎ notes at a column or a change.
- Highlights instead of outlines (JL 261011: "How about we just use the boxed with transparent to highlight the
  text part"): one see-through box per printed line, multiplied into the page picture (red removed, green
  added, gray comment only), as paper mode marks its quotes; `outline` and `draw_marks` are gone.
- Each picture column names its file under its heading (JL 261011: "you should put which files we are using
  here, for the two columns"): the original's path from the Block and its PDF, the plan's `draft` path.
- `found:` on an evidence item: papers a haipipe-discovery Run found, drawn as a black "Found: ..." line in the
  note before the red ask (JL 261011: "for the citations, you should add them as well").
- Sentence band (JL 261011: "in this area, you will put each sentence for the above section"): under each
  section's pictures, the updated draft's sentences read from the tracked Word file with every change accepted
  (`draft_units`: guidance in italics left out, a table row one unit, a reference one unit), one editable text
  box each, its built text in customData; green where a tracked change falls. New command `edits` lists the
  sentences a person changed (Before, After, the change). Writing them back into the plan is not built yet.
- Margin numbers (JL 261011, on 10 and 11 drawn over each other: "this is not well"): centred on their first
  line; two changes on one line share one label ("10 11"); a number on the next line steps left. GAP2 50 to 80.
- A change whose words a table row's label splits (LibreOffice prints a two-line cell's "Year 3" between the
  lines; found by b32) is found again with the `after` label's words left out.

## 0.2.0 · 2026-10-11 · Revise mode: a file we change, section by section

- JL 261011: "take screen shot of the pdf version for each section and then say what to modify and what to
  change", and, on where it belongs: "for the /excalidraw-read, this should be what we want to have".
- New `ref/read_revise.py draw <face.md> --key <plan>`: one screenshot per section of the PDF Word makes of a
  co-author's file, each planned change's words in a numbered red outline, an arrow to Change · Why ·
  Evidence needed; then the evidence asks by who can answer. Its look is b31_prep_ai s03's "The Task 3.1
  file today" frame; it reuses read_paper.py's drawing helpers and haipipe-studio's canvas.write.
- New `ref/revise-spec.md`: the plan's yaml. SKILL.md: section "Revise mode: a file we change".
- Same day, following b21_event_cgm's s04 (JL: "you should follow this structure"): two frames, the plan in one
  picture and the file today | updated draft | notes per section; `--updated-pdf`, `after`, line breaks as " / ",
  running headers and footers left out, sides cut at the text's edge (b32 kept the page tops at the text's edge).
  Both PDFs printed by LibreOffice through the Codex document runtime.
- First use: b31_prep_ai s04-task31-updated-draft (Nes Mathioudakis's Task 3.1 file, 20 changes, 7 sections).

## 0.1.2 · 2026-10-10 · Highlights to the last word, crops without slivers

From a fresh-context validation on Matz et al. 2024 (9 excerpts):
- `find()` matches characters with spaces removed, not a window of words as long as the quote: a word the
  bounding-box text splits (`CI95` as `CI` + `95`) had ended the highlight one or two words early while
  the status said `ok`. The four quotes that matched at 0.94 to 0.95 now match at 1.00.
- `lines:N` context is cut at the middle between neighbouring lines (pdftotext's line boxes overlap by
  about 2 pt). This replaces 0.1.1's whole-line loop, which grew each side by one line per pass, so
  `lines:3` took 6 lines.
- SKILL.md: a logic step fits one line (85 characters), and a match between 0.8 and 0.99 means checking
  the highlight; `.jpg` shots named throughout; stdout is line-buffered, so lines print in order.
- Confirmed by the Project11-TimeSeries session on DLinear (7 of 7 at 1.00, a table read as `ok (region)`);
  its note that a full-width table crop shrinks the marked cells became a line in step 6.

## 0.1.1 · 2026-10-10 · Tables, two columns, long paths, size

From a fresh-context validation on DLinear by the Knowledge-Base session Project11-TimeSeries:
- A table row cannot be quoted (pdftotext reads cells down each column): an excerpt may give `page`, a
  `crop` box and `mark` boxes instead of a quote; new `boxes` subcommand prints a page's line boxes.
- `lines:N` context stays in the quote's column, takes whole lines, and pads by at most half a line gap
  (it had pulled the other column's heading and half a line into the shot).
- A long `ours.source` or `paper.link` path wraps at "/" inside its frame.
- Shots are JPEG (quality 85), embedded as JPEG; the preview renders at 0.45 in 256 colours. The worked
  example went from 4.7 MB to 2.5 MB with one more excerpt.

## 0.1.0 · 2026-10-10 · A paper read onto a canvas

- JL 261010: "a skill which will try to read a paper of its pdf, and extract the paper logic and then
  screenshot the sections with the highlighted part, (no need to check every corner of them) and then add
  the comments, and how that will link to our paper."
- `ref/read_paper.py`: `text` (page-marked `paper.txt` and figure captions), `shoot` (each quote found by
  its words through `pdftotext -bbox-layout`, highlighted, cropped to 3 lines of context, `shots/`),
  `draw` (four frames through `haipipe-studio`'s merge-safe `canvas.write`, a `.png` preview), `all`.
- `ref/reading-spec.md`: the `reading.yaml` the agent writes: paper, our targets, logic, excerpts, open.
- Worked example: Salvi et al. (GPT-4 persuasion) read against a megastudy paper's C1, C2 and C5; 7 of 7
  quotes matched at 1.00; a person's mark survived a rebuild; real Excalidraw renders the drawing.
