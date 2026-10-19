s21 · Revise mode: how a co-author's file becomes a side-by-side drawing
========================================================================

**Tags:** `Run and Skill`

**Stage:** agreed

**Topic:** how b31_prep_ai's s04 (Nes Mathioudakis's SHIFT Task 3.1 file and our updated draft, side by side)
was drawn on 2026-10-11, as the worked example of excalidraw-draft: the steps from a co-author's
Word file to the side-by-side drawing and the tracked Word draft, the script behind each step, and what each
step costs, in seconds per rebuild and in rounds with a person (JL 261011: "add a new sNN in
Tools/blueprints/b31_excalidraw to explain how did we draw the things here? what is the workflow are what are
the steps? how which steps are most expensive?").

**Source:** the worked example `examples-0-cowork/Project-SHIFT-Study/cowork/b31_prep_ai/studio/s04-task31-updated-draft/`
(in WellDoc-SPACE), its session passes `runs/run-draw-s04/passes/p01-1011` to `p07-1011`, and the scripts named
below. The seconds were measured once on 2026-10-11 on JL's Mac (cProfile of one rebuild); the builder reads
them from the yaml blocks here and measures nothing itself.

**Feeds:** no Question yet (b31 has no `reports/`).


Files
-----

```text
s21-revise-mode-workflow/
├── s21-revise-mode-workflow.md          this face; the yaml blocks below are the drawing's words
├── build_s21_revise_mode_workflow.py    the builder
├── s21-revise-mode-workflow.excalidraw  the drawing; a person's marks are kept on rebuild
└── s21-revise-mode-workflow.png         its preview
```

Rebuild: `python build_s21_revise_mode_workflow.py` (it writes the preview too).


What the drawing holds
----------------------

```text
frame 1  the workflow in one picture: 9 steps in 6 lanes (once, plan, draft, build, look, last), the loop back
         from your edits to the draft, step 7 opened into its 7 parts, seconds per rebuild, where the effort went
frame 2  how s04 got here on 2026-10-11: each of JL's asks, what changed, the pass; then the open points
```


The workflow
------------

Sentence mode (excalidraw-read 0.3.1, from 2026-10-11): the middle column is the updated text from the topic's
`draft/` folder (haipipe-draft's draft), not a picture of the updated pages; the Word file is built last.

```yaml
workflow_steps:
- {n: 1, lane: once, title: Copy the file in, script: "cp → related/materials/", cost: "< 1 s",
   what: "A copy of the shared OneDrive file; the original stays read only."}
- {n: 2, lane: once, title: Print it, script: word_pdf.office_pdf, cost: "1.6 s",
   what: "LibreOffice makes the PDF the left pictures are cut from; Word cannot be driven over SSH."}
- {n: 3, lane: plan, title: Plan the changes, script: "face yaml task31_file_edits", cost: "agent: long", costly: true,
   what: "21 changes: the file's words each one touches (find), why, the evidence asked, who answers."}
- {n: 4, lane: plan, title: Find the citations, script: haipipe-discovery, cost: "1.4 s per paper",
   what: "One Paper Run per paper, BibTeX from Crossref; found: on the evidence."}
- {n: 5, lane: draft, title: Seed the draft, script: "read_revise.py seed", cost: "once",
   what: "draft/<stem>-draft-v1.0.md in haipipe-draft's three sections, one Bullet per sentence, Change lines."}
- {n: 6, lane: draft, title: Write and revise, script: "haipipe-draft", cost: "agent + person", costly: true,
   what: "Each pass a new version, the old one in previous/, Before and After in records/."}
- {n: 7, lane: build, title: Draw, script: "read_revise.py draw", cost: "7.2 s",
   what: "Left: the file's page, red highlights. Middle: the draft's sentences. Right: notes. Opened below."}
- {n: 8, lane: look, title: Look and edit, script: "edits --apply", cost: "a person",
   what: "Double-click a sentence on the drawing; --apply writes it into the draft by address."}
- {n: 9, lane: last, title: Deliver, script: "read_revise.py deliver", cost: "0.6 s + 4.6 s print",
   what: "The draft against the file, word by word: tracked changes, new paragraph marks, comments; it checks itself."}
loop: {from: 8, to: 6, text: "Your edits go back into the draft (or the plan, step 3); then the drawing is rebuilt"}
```

```yaml
draw_steps:
- {k: a, title: Read the words, script: "read_pages, page_words", cost: "0.1 s",
   what: "pdftotext -bbox gives every word's box; running header and footer left out."}
- {k: b, title: Cut the sections, script: bounds_of, cost: "< 0.1 s",
   what: "The title and each Heading 1 of the .docx, found in the PDF's words."}
- {k: c, title: Render the left pages, script: "cut (pdftoppm 200 DPI)", cost: "5.9 s", red: "⚠️ most expensive: 10 renders of 4 pages; render each once",
   what: "Each section's pages rendered, cropped at the text's edge, stitched."}
- {k: d, title: Find each change's words, script: find_in, cost: "< 0.1 s", red: "⚠️ most fragile: 4 kinds of miss so far",
   what: "Exact, then a row label left out, then up to 14 words between."}
- {k: e, title: Highlight, script: "line_boxes, highlight", cost: "0.2 s",
   what: "A see-through red box per printed line of the words that change."}
- {k: f, title: Read the draft, script: "read_draft (plan_layout)", cost: "0.1 s",
   what: "The current version's sentences, Change lines and addresses."}
- {k: g, title: Lay out and write, script: "sentence_column, note, canvas.write", cost: "0.5 s",
   what: "Sentence boxes, numbers, notes in 3 columns, a person's marks kept, the preview."}
```

```yaml
seconds:                   # one sentence-mode rebuild of b31 s04, measured 2026-10-11 (cProfile); was about 20 s
- {step: "7c render the left pages", s: 5.9}
- {step: "9 print the tracked draft (last)", s: 4.6}
- {step: "2 print the original (once)", s: 1.6}
- {step: "4 one discovery Run (per paper)", s: 1.4}
- {step: "7g preview and write", s: 0.5}
- {step: "9 write and check the Word file (last)", s: 0.6}
- {step: "7e highlight", s: 0.2}
- {step: "7f read the draft", s: 0.1}
- {step: "7a read the words", s: 0.1}
```

```yaml
effort:
- {title: "The look: 9 passes, 5 ways to show the pages",
   what: "Text rows, mammoth + Chrome, textutil, then LibreOffice pictures on both sides, then the updated side as editable sentences (kept)."}
- {title: "Finding the words: 4 kinds of miss",
   what: "A running header inside a section; a side crop that cut first letters; a table row label inside a cell (b32); a row split across pages (b32)."}
- {title: "The plan: 21 changes, 10 evidence asks",
   what: "Each find appears once in the file; the file's words stay, so each change is the smallest one."}
- {title: "Writing: 2 passes, 19 sentences",
   what: "Pass 1 made 17 of our sentences professional; pass 2 lifted S6 and S7 to the task's arc. Facts and citations kept."}
- {title: "Citations: 9 searches, 5 papers, 3 discovery Tasks",
   what: "Each paper one Run with BibTeX from Crossref; a person still checks each one."}
```


How s04 got here
----------------

```yaml
rounds:                    # 2026-10-11; pass = runs/run-draw-s04/passes/pNN-1011 in b31_prep_ai
- {ask: "\"It should not be changed that much\"", did: "Light tracked edits on Nes Mathioudakis's own file (track_changes.py)", pass: "", kept: true}
- {ask: "\"I want to see the excalidraw\"", did: "Rows of text, one per change", pass: "", kept: false}
- {ask: "\"I don't want a new format!!!!\"", did: "Pictures from mammoth + Chrome, then textutil: not the file's look", pass: "", kept: false}
- {ask: "\"take screen shot of the pdf version for each section\"", did: "read_revise.py: LibreOffice prints, one picture per section", pass: "p01, p02", kept: true}
- {ask: "\"you should follow this structure\" (b21's s04)", did: "Two frames: the plan in one picture, then side by side", pass: "p03", kept: true}
- {ask: "\"Nes is HE!!! You give the full name\"", did: "Full names everywhere; a standing rule saved", pass: "", kept: true}
- {ask: "\"the font size can be much smaller ... more columns\"", did: "Notes 14 px in 3 columns, level with their words", pass: "p04", kept: true}
- {ask: "\"use the boxed with transparent to highlight\"", did: "See-through highlights instead of outlines", pass: "p05", kept: true}
- {ask: "\"this is not well\" (10 over 11)", did: "Numbers on one line share a label; close ones step left", pass: "", kept: true}
- {ask: "\"which files ... for the two columns\"; \"/haipipe-discovery\"", did: "A file line per column; 4 citations from discovery", pass: "p06", kept: true}
- {ask: "\"Nes also have a paper ... In the jama\"", did: "Mathioudakis 2025 JAMA trial, cited in change 4", pass: "p07", kept: true}
- {ask: "\"we don't have this, but use the text to replace it\"", did: "The middle column becomes the draft's sentences, editable; writing pass 1", pass: "p08", kept: true}
- {ask: "\"the draft folder following the /haipipe-draft\"", did: "draft/ with one current version, previous/ and records/", pass: "p09", kept: true}
- {ask: "\"S6 and S7 should be something high level\"", did: "Draft v1.2: the gap and the payoff of insights", pass: "p09", kept: true}
- {ask: "\"IT IS NOT GOOD WE HAVE ONE PARAGRAPH WITH 17 SENTENCES\"", did: "Long paragraphs split at the text's turns; one box per paragraph", pass: "p13", kept: true}
- {ask: "\"OKAY, PLEASE DO IT\" (delivery, the last step)", did: "read_revise.py deliver: the Word file from the draft, checked both ways", pass: "p13", kept: true}
```

```yaml
peers:
- "b21_event_cgm: the two-frame structure of its s04 (Gordon Gao's Task 2.1)."
- "b32_aid_ai: cut() at the body text's edge, the row-label retry's case, and the retry with up to 14 words between."
```

```yaml
later:
- "Render each page once and reuse it: 10 renders become 4, about 6 s become 2.5 s."
- "The side-by-side frame is 3,382 px wide, over the 2,800 rule, kept for the 3 note columns."
- "Five citations wait for a person's check (bib.verification: pending)."
- "A new file may bring a new kind of miss in finding words; the build stops and names the change."
```


Decided
-------

s21-D01 · This topic records excalidraw-draft as b31_prep_ai's s04 used it on 2026-10-11: the
    workflow, its scripts, the seconds per rebuild and the effort, read from yaml in this face (JL 261011).
s21-D02 · The workflow drawn is sentence mode (excalidraw-read 0.3.1): seed a haipipe-draft draft, write and revise
    it, draw, edit on the drawing and apply, deliver last; picture mode stays in the rounds as how it began.
s21-D03 · Delivery is built from the draft (excalidraw-read 0.4.0, now excalidraw-draft; `read_revise.py deliver`): the draft's words against
    the file's, word by word, become tracked changes, and the build checks that rejecting every change gives the file
    and accepting every change gives the draft (all three SHIFT Blocks pass, 2026-10-11).
s21-D04 · Stage → agreed (JL 261012: "I think for others sNN, we can give them to level 3 as well"): the topic records revise mode as b31's s04
    used it; its open points moved to Later, and the drawing's Open list is drawn as Later, plain.


Open
----

(none open: agreed 261012, s21-D04; 3 points moved to Later)


Later
-----

Not needed now; each comes back as a new point if it is wanted.

1. Render each page once (`read_revise.cut` renders the same page for every section that touches it).
2. Is 3,382 px wide acceptable for a side-by-side frame, or should the pictures shrink?
3. Deliver from the draft: done 2026-10-11 (`read_revise.py deliver`); b32 and b21 still point their own delivery
   scripts at it.

