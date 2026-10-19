# The revise plan · a yaml block in a studio topic's face

`read_revise.py draw <face.md> --key <key>` reads the block whose first line is `<key>:`.

```yaml
task31_file_edits:
  file: Task 3.1 - Nes Mathioudakis.docx       # beside the face, or in the Block's related/files/ (or materials/)
  pdf: Task 3.1 - Nes Mathioudakis.pdf         # optional; default: the file's name with .pdf, saved from Word
  stop_at: Examples for reference              # optional: the words that end the last section
  sections:                                    # optional: a file without Heading 1 (an IRB form) names its headings,
  - {id: 4, head: Study Procedures, name: 4 Study Procedures,       #   in order: `head` the heading's own words,
     find: Study Procedures a Study design including the sequence}  #   `name` shown, `find` the printed words
                                               #   that locate it in the PDF (default: head); `part` then names `id`
  sentences: draft/                            # optional: sentence mode, the updated text in a haipipe-draft draft
                                               #   folder (written once by `read_revise.py seed`, then the source)
  title: <frame name>                          # optional
  heading: <the frame's first line>            # optional
  intro: <one more sentence under it>          # optional
  people: {Nes Mathioudakis: Task 3.1 lead}    # optional: roles for the closing list, in its order
  change_notes:                                # optional: green ✎ notes where the drawing changed
  - {at: notes, date: 261011, text: notes smaller than the pages}   # at: left, middle, notes, or a change's id
  # optional layout, each off unless the plan names it (b21 s04, JL 261014):
  notes: {columns: 2, width: 640, title: 22, body: 18, short: true, stairs: true, step: 160}
                                               #   the notes column: fewer, wider notes; short = title, why, asks;
                                               #   stairs = each note lower and further right, an L from its sentence
  content: {width: 1400, size: 26}             #   sentence mode: the draft column's width and type size
  section_stairs: {stairs: true, step: 800, gap: 400, frames: true}
                                               #   each section `step` px right of the one before (`wrap`: back to
                                               #   the left after so many); frames: each section its own frame,
                                               #   named for it, the plan and the key in a row above, the frames
                                               #   `gap` apart, an L arrow from each frame into the next
  replies:                                     # optional: a co-author's comment and our reply, a blue note at a change
  - {at: 8, to: Gordon Gao, when: "2026-10-14, on part 4", said: "<their words>", brief: <the reply, short>,
     items: [{anchor: <words in the draft>, reply: <a comment there>}]}   # items: delivery/build_clean.py
  review:                                      # optional, sentence mode: a writing review's proposals (haipipe-writing),
    label: <one line above the first note>     #   each a red note at its sentence, a red L from it, after the changes'
    items:                                     #   notes; open until a person picks (b21 s04, JL 261014)
    - {id: W1, at: C2.P3.S1, title: <short>, change: <the proposed words>, why: <one line>, ask: "Ask JL: <question>"}
  edits:
  - id: 2                                      # a plain number, shown by the highlight and the note
    part: "1"                                  # "title", a heading number, "R" References, "F" Overview Figure,
                                               #   or the heading's own text
    title: Name the learning gap               # the note's title
    after: [Year 1]                            # optional: phrases searched in turn; find is the first match after
                                               #   (a row label printed among the cell's lines is looked past)
    find: Existing tools produce scores or doses rather than clinical context.   # the author's exact words
    new: >-                                    # what they become; absent: a comment only; "" deletes
      Existing tools produce scores or doses rather than clinical context, and patient education ...
    image: figure                              # instead of new: our figure goes in the box
    why: <one sentence>
    evidence:                                  # optional; one dict or a list
      need: <what evidence is needed>
      ask: <the question>
      who: [JL, Nes Mathioudakis]
      anchor: <the words a Word comment sits on>   # used by the tracked-changes writer, not by the drawing
      found:                                   # optional: papers a haipipe-discovery Run found for this ask;
      - {cite: "Ying et al. 2025, JAMA Network Open", run: b01.j01.t01.r01}   #   the note and the comment say "Found: ..."
```

The note's `Change:` line is worked out from `find` and `new`: `"old" becomes "new"`, `After "...words" add:
"..."`, or `Delete "..."`, on whole-word edges. `find` must appear in its section of the PDF (tokens: letters
and digits, case ignored), after its `after` phrases when given; the build stops when it does not. A line break
in `new` (a new paragraph or table line) shows in the note as " / ".


## Sentence mode

With `sentences`, the drawing's middle column is the updated text itself, one editable text box per sentence,
read from a draft folder beside the face, not a picture of the updated pages (JL 261011). The folder follows
haipipe-draft's draft (JL 261011: "we should have the draft folder following the /haipipe-draft"):

```text
draft/
├── <stem>-draft-v1.1.md        the one current version, three sections (haipipe-draft's plan_layout writes it)
├── previous/<stem>-draft-v1.0.md   each older version
└── records/<stem>-log.md       each writing pass: Before, After, why

## 1 · Structure · Bullet Point Table      per sentence: its Point, and `Change: 4 · <title>` when a planned
- B4 · [Evidence] Trials show ...           change touches it (no Change line: the file author's own sentence)
## 2 · Scratch · What to write here
## 3 · Draft · Reading and Revise          the sentences: `- B<k> · S<n> · <sentence>`, one per Bullet
```

A division `## C<n> · <name>` is matched to the file's section by name ("Challenge and Significance" is
section 1); a paragraph `### C<n>.P<m>` keeps the file's paragraphs, P counted across the whole draft.

```bash
read_revise.py seed  <face> --key <plan>            # write v1.0 once, from the tracked Word file, changes accepted;
                                                    #   no tracked file yet: it is first written from the plan
read_revise.py draw  <face> --key <plan>            # the middle column from the current version
read_revise.py deliver <face> --key <plan> [--no-pdf]  # last: the tracked Word file (plan `draft`) from the draft,
                                                      #   checked both ways, then its PDF
read_revise.py edits <face> --key <plan> [--apply]  # the sentences a person changed on the drawing; --apply
                                                    #   writes them into the Draft section by address (C3.P5.B7)
                                                    #   and takes the edited boxes off the drawing
```

haipipe-writing works on the draft (only the sentences a change touches, unless asked for more), a new pass a
new version with the old one moved to previous/; the tracked Word file is built from it last (`deliver`). A plan
whose image change says `image: figure` names the picture with `figure:` (a path beside the face).
