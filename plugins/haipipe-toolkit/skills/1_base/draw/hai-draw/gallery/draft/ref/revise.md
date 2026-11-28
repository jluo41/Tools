# Revise mode · a file we change, its sections, the changes, the Word file

Each section of their file is shown as its PDF picture, what changes in it and why, and the updated text as
one editable box per sentence. It draws with hai-draw read's page helpers (`read_paper.py`).

```text
their file (.docx) ─▶ related/files/ copy + PDF ─▶ the plan (face yaml) ─▶ draft/ sentences ─▶ drawing
                       (LibreOffice prints it)      find · new · why ·       (seed, once)        plan · side by side
                                                    evidence · who                 │
                                                                                   └─▶ deliver: tracked .docx
                                                                                       reject all = the file
                                                                                       accept all = the draft
```

```text
frame 1  the plan in one picture (one screen): shared file ─▶ our copy ─▶ the plan ─▶ tracked Word file ─▶ ? back
         words per part (file today, updated draft) · who answers the comments · open questions
frame 2  side by side, per section (read down):
         the file today (red highlight) │ updated draft, one sentence per box (green) │ change · why · who answers
```


Commands
--------

```bash
R=Tools/plugins/haipipe-toolkit/skills/1_base/draw/hai-draw/gallery/draft/ref/read_revise.py
.venv/bin/python $R seed    <face> --key <plan>    # the sentence draft, once; first the tracked file from the plan
.venv/bin/python $R draw    <face> --key <plan>    # the drawing
.venv/bin/python $R edits   <face> --key <plan> [--apply]   # sentences a person changed on the drawing
.venv/bin/python $R deliver <face> --key <plan> [--no-pdf]  # last: the tracked Word file, checked, then its PDF
```

A topic keeps a small builder beside its face that calls these (b21's `build_s04_task21_updated_draft.py` is
the shortest; b01_irb's `build_s03_for_cir2_changes.py` adds `--base`, below).


Steps
-----

1. **Their file first.** Copy it into the Block's `related/files/` (hai-related's folder; the older
   `related/materials/` is read too), list it in `related/related.md`, and print it to PDF beside the copy with
   LibreOffice (the Codex document runtime, `read_revise.office_pdf`), which keeps the file's fonts, colours,
   header and margins. A mammoth or textutil print shows a new format, not their file. The shared original is
   never written. A file of our own that was filed with Track Changes on (an IRB protocol after its last
   change) is first copied with those changes accepted: that is the file as it stands today.
2. **The plan is a yaml block in the topic's face** (`ref/revise-spec.md`): each change names its section
   (`part`), the author's exact words (`find`, with `after` when the words repeat), what they become (`new`),
   why, and the evidence needed with who answers. The author's words stay: only what differs is a change. A
   change with no `new` is a mark only (gray): its words are still to be written.
3. **Sections.** A section is the title block or one Heading 1. A file without Heading 1 (an IRB form, whose
   numbered headings are plain lines) lists its headings in the plan's `sections`, in order, each with the
   heading's own words (`head`), a short `name`, and the printed words that find it in the PDF (`find`, with the
   line after it when the heading alone repeats; a form prints "a." before its first prompt).
4. **The updated text is a draft** (`sentences: draft/`), in hai-draft's draft grammar, one Bullet per
   sentence. `seed` writes v1.0 once from the tracked Word file (plan `draft`) with its changes accepted; when
   that file does not exist yet, `seed` first writes it from the plan's changes (`track_changes.write_tracked`).
   From then on the draft is the source: hai-draft-writing works on it, a person edits sentences on the drawing
   and `edits --apply` folds them in by address (C3.P5.B7).
5. **One row per section**, cut from the PDF between its heading and the next (`stop_at` ends the last);
   running headers and footers are left out, the sides cut at the text's edge. See-through boxes, like a marker
   pen, sit on the words: red on the words that change, gray where only a comment sits; they are multiplied into the picture, so the ink stays
   black. Each note reads `Why:`, and in red `Evidence needed: ... (who)`. No evidence ids.
6. **Notes small, three columns**: note words 14 px, titles 16,
   `canvas.aside`; three columns 360 px wide, each note in the column where it sits highest, level with its
   words. A first-column note gets an arrow; one further right carries the highlight's number. The frame is about
   3,320 px wide, over `canvas.FRAME_MAX`'s 2,800 on purpose (principle ① differs here), and reads down.
7. **Delivery, the last step** (`deliver`): the draft's words against the file's, word by word, become the
   smallest tracked changes by the plan's author (`ref/track_changes.py`); a draft paragraph that starts inside a
   file paragraph becomes a tracked new paragraph mark; each evidence item becomes a comment on its `anchor`; the
   plan's image changes and guidance deletions are kept. It checks itself: rejecting every change gives the file,
   accepting every change gives the draft; it stops if either fails. Then it prints the PDF with LibreOffice.
8. **Files and citations**: each picture column names its file under its heading; a change's evidence may carry
   `found:`, papers a `hai-discovery` Run found, shown as "Found: ..." in its note and Word comment.
9. **Checked**: the build stops when a change's words are not in its section (a table row's label printed among
   a cell's lines is looked past, with `after`); `canvas.write` warns about oversized frames and small text.
10. **Read it as a reader** (hai-studio `ref/reader-review.md`): the reviewer answers what the file is, what
    changes and why, who answers what by when, and what happens next; its gaps go into the plan
    (`plan_heading`, `send`, `open`) and the build runs again.


Worked examples
---------------

- `<world>/Project-<Name>/cowork/b31_prep_ai/s04-task31-updated-draft/`: a co-author's
  Task 3.1 file, a co-author's draft (b32 s04 and b21 s04 are the same shape).
- `<world>/Project-<Name>/cowork/b01_irb/s03-for-cir2-changes/`: the study protocol (eForm A)
  for CIR 2, a Change in Research; its own filed file, `sections` for the form's headings, the tracked file
  first written from the plan, `deliver` into `delivery/j04_cir2_epic_data/`.

Design topic: `Tools/examples/Project-PageParts/work/b31_excalidraw/s21-revise-mode-workflow/` (b31 s21).


Boundary
--------

| Owner | Owns |
|---|---|
| `hai-draw draft` (Revise mode, this page) | the plan's grammar, the side-by-side drawing, the tracked Word file and its checks |
| `hai-draw read` | reading one paper and linking it to ours; its `read_paper.py` cuts and draws the pages here |
| `hai-draw draft` (Map mode, `ref/map.md`) | a paper's own Section map (paper, Sections, paragraphs, Bullets, evidence) |
| `hai-draft` | the draft folder's grammar (`plan_layout`) that the sentences live in |
| `hai-draft-writing` | rewriting the sentences a change touches |
| `hai-studio` | the topic folder, its face, its builder's writer (`canvas.write`) and sessions |
| `hai-related` | the copy in `related/files/` and its row |

A person accepts or rejects the tracked changes in Word; this mode never accepts them, never writes the shared
original, and never sends the file.
