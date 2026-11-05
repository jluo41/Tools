s22 · Word lane speed: how to make a Word draft fast without losing what it gives
=================================================================================

**Tags:** `Run and Skill`

**Stage:** explore

**For:** a deck, and the Word lane code of haipipe-paper-assemble, for whoever waits on a paper build

**Delivery type:** code

**Covers:** why the Word stage takes 28 minutes, what must stay (a display at the top of the page after its citation), and the ways to make a draft fast.

**Excluded:** the LaTeX lane (about 30 seconds, and `--pdf-only` already gives the PDF in seconds); which Word template a venue uses (s03 and the venue template checklist).

**Topic:** JL 261104: "I think the speed here is a issue, please document it well". One sentence change cost half an hour before co-authors could see Word, and JL asked three times how long it would take. The answer turned out to be a stuck Word, not slow work: 28 minutes on the stuck one, 40 to 80 seconds on a working one. What is left open is keeping it from happening again.

**Feeds:** `reports/` none yet; its form is `j02_word_lane_speed/runs/r01_collect_word_lane_speed/`


What was measured
-----------------

Paper-AgreeablePrescriptionDiscretion: 53 pages, 12 tables, 2 figures, a 656K `.docx`. Measured by Pp-AgreeableRx-Discrention and Theme_Paper on 261104.

```text
build (LaTeX done)     .docx saved       gap
02:50                  03:18             28 min
09:56                  10:24             28 min
10:33                  saves at 10:53, 10:55, 10:57, 10:59, 11:01: 2:00 apart
```

1. **Word calls, 10 minutes of 3 builds**: 14 calls, 11 of them 119.6 to 120.5 seconds, the default AppleEvent timeout; 3 shorter ones were already running when the sample began.
2. **The error**: `Microsoft Word got an error: AppleEvent timed out. (-1712)`. In `render.docx_tail`, only the last 1500 characters: 6 on 11-03 16:20 (Paper-PhyAbsence-PatientCare), 11 on 11-04 03:38 (Paper-AgreeableOpioid-Jama), 10 at 11:01 (Discretion). None on builds up to 11-01 21:10.
3. **Word itself**: `sample` shows the main thread inside an AppleEvent handler on `__psynch_mutexwait`, 2561 of 2561 samples, 0% CPU. `version` answers in 0.1 s; `name of documents` gives no answer in 30 s.
4. **Left open**: Word holds two `haipipe-measure` copies, with `~$` lock files of 11-03 15:33. Word has run since 11-02 17:48.
5. **The prints**: `pdfinfo` says LibreOffice on the Word tabs' PDFs of 11-04; the 11-01 one says Quartz (Word's own print).

What that means: a display waited 2 minutes, then fell back to right after its citing paragraph. In the 11:03 PDF, Figures 1 and 2 and Tables 1, 2, 4, B1 and D2 do not open their page. The trigger of the hang is not known; two builds opening documents together at 15:33 is a guess.

**On a working Word.** The stuck Word was gone by 11:41; who or what ended it is not known.

```text
Paper-AgreeablePrescriptionDiscretion, full build, 11:41 (one run, measured by Pp-AgreeableRx-Discrention)
  start 11:41:05 · LaTeX PDF :11 · .docx :38 · Word's PDF :41 · end :45      about 40 s, 14 displays, 52 Word pages
  printed by Word (Quartz), displays at page tops
  two more full builds: 11:42:47 to 11:44:06 and 11:44:17 to 11:45:35, about 80 s each, Word's print, 52 pages
  Table D2 is the one display in 14 that does not open its page: Table D1 runs onto that page first

placeholder, 31 pages, no other build at first (Theme_Paper, 2 rounds), seconds
  open 0.5 to 1.8 · repaginate 0.6 to 0.9 · find 0.2 to 0.5 · page end 3.7 to 4.3 (16 calls) · close 0.2 to 0.4
```

A build began near the end of the placeholder run; the timed steps were mostly before it.


The mechanism
-------------

`scripts/latex_room_to_docx.py` `save_docx` loops over each held display: `doc.save`, then `word_page_boundaries` copies the file to `haipipe-measure/`, opens it in Word, runs `repaginate`, `execute find` for the citing text, a binary search on `get range information` for the page end (about 17 calls, an estimate), and closes without saving. Each placed display shifts later pages, so as written nothing is reused. Purpose (0.12.2, JL 261028): each display at the top of the page after its citation.


Risks from reading the code (not reproduced)
--------------------------------------------

1. **`selection` is Word's front document**: two builds may search each other's file.
2. **One shared Word, one shared folder, no queue**: the delivery lock is per paper. The copy is named by `path.name`, so two Section builds' `t03-results.docx` can collide.
3. **The quit in `save_docx`'s `finally`**: if Word was not running at the start, it quits Word, even if another build began using it.
4. **`close d` never runs after a timeout**: a timed-out script may leave its document open in Word.


The options
-----------

```text
A  draft mode     skip measuring while editing; full placement once before a send     small
B  one pass       one Word session: repaginate once, keep it open, measure onward     medium
C  rebuild less   reuse the last placement when no text before a display changed      medium
D  a Word queue   builds take turn in Word, safe quit, unique copy names              small
E  faster page end  Word's go-to-page in place of the binary search, if timing says so  small
```

D and A are built. B, C and E would save seconds, so they are not worth building unless a much longer paper says otherwise.


Files
-----

```text
s22-word-lane-speed/
├── s22-word-lane-speed.md             this face
├── s22-word-lane-speed.excalidraw     the drawing
├── s22-word-lane-speed.png            its preview
├── build_s22_word_lane_speed.py       the builder (the person's marks are kept)
├── s22-word-lane-speed.ideas.md       its open ideas, and the deck
└── delivery/                          deck/ and render.yaml
```


Decided
-------

s22-D01 · A stuck Word is found in 30 seconds, skipped, and said in the build's report; the Word tab says when its PDF is not Word's (haipipe-paper-assemble 0.17.1, workbench-paper 0.44.6; Theme_Paper 261104, a bug fix, reversible).

s22-D03 · Builds take turns in Word, one lock per machine, and a build quits Word only if it started it and no document is open (`scripts/word_lock.py`, 0.17.2; Theme_Paper 261104; option D). A real full build of Paper-AgreeablePrescriptionDiscretion waited on it once ("waiting for Word: another build is using it") and still finished in about 80 seconds.

s22-D04 · A Word draft measures no pages: `build.py --word-draft` floats each display to the top of the page its citing text reaches; a plain build stays measured, and a draft is never sent or shared (JL 261104, form Q1 B: "we can use method B, as long as the table is at the top of that page"; assemble 0.18.0; option A). Scratch placeholder in Word: no overlap, two tables stacked, a long table moved on and left white space. Not yet run on a real paper.

s22-D02 · `build.py --pdf-only` gives the LaTeX PDF in seconds, no Word app (JL 261104, relayed by Paper-PhyAbsence: "Yes, let's focus on the pdf first"; 4 seconds on Paper-PhyAbsence-Maternity-JamaIM).


Open
----

1. How much time does `--word-draft` save on a real paper? Only its first real build will say.
2. What started the hang? Does taking turns prevent it? Only time will tell; a stuck Word now costs 30 seconds and says so.
3. Two old `~$` lock files of 11-03 15:33 stay in `haipipe-measure/` (Paper-AgreeableOpioid-Jama, Paper-PhyAbsence-Maternity-JamaIM): delete them when no build runs if those papers' measuring misbehaves.
4. Table D2 does not open its page, because the long Table D1 runs onto that page first. Accept it, or place a display after the end of the one before it?
5. Risks 1, 2 and 3 above are closed by the turn only for builds; a person using Word during a build can still move its front document.

(write here, or mark the drawing in red)
